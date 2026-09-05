/*
 * Drift check. Is this wiki behind what the site and the zoompilot
 * repo publish? Two signals:
 *
 *   1. Release notes. The zoompilot.ai release page shows the
 *      current release version (the page promises it matches
 *      version.h on published main). The wiki changelog must carry
 *      the same newest version.
 *   2. Upstream docs. Commits that touch docs/zoompilot on the
 *      zoompilot repo (develop) mirror into docs/technical/ by
 *      hand. A commit the check has not seen means those pages may
 *      lag.
 *
 * Findings go to one issue, titled "Wiki drift: ...". A clear run
 * closes that issue. Signal 2 records the commit it saw in
 * .github/drift-state.json, so each docs change raises one flag.
 *
 * Run by .github/workflows/drift-check.yml. A local run without
 * REPO set is a dry run: it prints findings and touches nothing.
 *
 *     node .github/scripts/drift-check.mjs
 *
 * REPO ("owner/name") and GITHUB_TOKEN turn on the issue edits and
 * the state file write.
 */
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const root = join(here, "..", "..");
const statePath = join(here, "..", "drift-state.json");

const REPO = process.env.REPO;
const TOKEN = process.env.GITHUB_TOKEN;
const ISSUE_TITLE = "Wiki drift: release notes or upstream docs moved";

const ghHeaders = {
  Accept: "application/vnd.github+json",
  ...(TOKEN ? { Authorization: `Bearer ${TOKEN}` } : {}),
};
const gh = (path, method, body) =>
  fetch(`https://api.github.com${path}`, {
    method: method ?? "GET",
    headers: ghHeaders,
    ...(body ? { body: JSON.stringify(body) } : {}),
  });

/* ---- signal 1: newest release version ---- */

const page = await (
  await fetch("https://zoompilot.ai/release-notes")
).text();
const liveVer = page.match(/<b class="ver">([^<]+)<\/b>/)?.[1];
if (!liveVer) {
  throw new Error("could not read the release version from zoompilot.ai — page markup changed?");
}

const logText = readFileSync(
  join(root, "docs", "releases", "changelog.md"),
  "utf8",
);
const wikiVer = logText.match(/^## (\d{4}\.\d{2}\.\d{2}-\d+)/m)?.[1];

const releaseDrift = Boolean(liveVer && wikiVer && liveVer !== wikiVer);
console.log(`release: live ${liveVer} / wiki ${wikiVer} -> ${releaseDrift ? "DRIFT" : "ok"}`);

/* ---- signal 2: docs/zoompilot tip on develop ---- */

const commits = await (
  await gh(
    "/repos/zoompilot/zoompilot/commits?sha=develop&path=docs/zoompilot&per_page=1",
  )
).json();
const tip = Array.isArray(commits) ? commits[0] : undefined;

const state = existsSync(statePath)
  ? JSON.parse(readFileSync(statePath, "utf8"))
  : {};
const docsDrift = Boolean(tip && tip.sha && tip.sha !== state.docsZoompilotSha);
console.log(
  `docs: tip ${tip?.sha?.slice(0, 9)} seen ${state.docsZoompilotSha?.slice(0, 9) ?? "never"} -> ${docsDrift ? "DRIFT" : "ok"}`,
);

/* files the tip commit touched, for the issue body */
let files = [];
if (docsDrift && tip) {
  const detail = await (
    await gh(`/repos/zoompilot/zoompilot/commits/${tip.sha}`)
  ).json();
  files = (detail.files ?? [])
    .map((f) => f.filename)
    .filter((f) => f.startsWith("docs/zoompilot/"))
    .map((f) => f.replace("docs/zoompilot/", ""));
}

/* ---- report ---- */

function issueBody() {
  const rel = [
    "## Release notes",
    "",
    `zoompilot.ai current release: **${liveVer}**`,
    `Newest release in \`docs/releases/changelog.md\`: **${wikiVer}**`,
  ];
  const docs = docsDrift
    ? [
        "",
        "## Upstream docs",
        "",
        "New commits touch `docs/zoompilot` on develop. The technical",
        "pages mirror these by hand:",
        "",
        `- [\`${tip.sha.slice(0, 9)}\`](https://github.com/zoompilot/zoompilot/commit/${tip.sha}) ${tip.commit.committer.date.slice(0, 10)} ${tip.commit.message.split("\n")[0]}`,
        ...(files.length ? [`  files: ${files.join(", ")}`] : []),
      ]
    : [];
  return [
    ...rel,
    ...(docsDrift ? docs : []),
    "",
    "## What to do",
    "",
    "1. Add the release to the site repo's `src/data/changelog.js`,",
    "   copying the notes on zoompilot.ai. Then run `npm run",
    "   sync:wiki` from the site repo, and push both repos.",
    "2. Mirror the upstream doc changes into `docs/technical/*.md`,",
    "   then run the sync again to refresh the route library.",
    "",
    "This issue closes itself on the first clear run.",
  ].join("\n");
}

const findings = [releaseDrift && "release notes", docsDrift && "upstream docs"].filter(
  Boolean,
);

if (!REPO) {
  console.log(
    findings.length
      ? `dry run, would flag: ${findings.join(", ")}`
      : "dry run, clear",
  );
  process.exit(0);
}

const issues = await (await gh(`/repos/${REPO}/issues?state=open&per_page=50`)).json();
const open = (Array.isArray(issues) ? issues : []).find(
  (i) => i.title === ISSUE_TITLE && !i.pull_request,
);

if (findings.length) {
  if (open) {
    if (open.body !== issueBody()) {
      await gh(`/repos/${REPO}/issues/${open.number}`, "PATCH", {
        body: issueBody(),
      });
      console.log(`updated issue #${open.number}`);
    } else {
      console.log(`issue #${open.number} already current`);
    }
  } else {
    const made = await (
      await gh(`/repos/${REPO}/issues`, "POST", {
        title: ISSUE_TITLE,
        body: issueBody(),
      })
    ).json();
    console.log(`opened issue #${made.number}`);
  }
} else if (open) {
  await gh(`/repos/${REPO}/issues/${open.number}/comments`, "POST", {
    body: `Clear as of ${new Date().toISOString().slice(0, 10)}: release ${wikiVer} is current, docs tip ${tip?.sha.slice(0, 9)} recorded.`,
  });
  await gh(`/repos/${REPO}/issues/${open.number}`, "PATCH", {
    state: "closed",
  });
  console.log(`closed issue #${open.number}`);
}

/* record the docs tip we just handled, so it flags once */
if (tip?.sha && tip.sha !== state.docsZoompilotSha) {
  writeFileSync(
    statePath,
    JSON.stringify({ docsZoompilotSha: tip.sha }, null, 2) + "\n",
  );
  console.log(`state -> ${tip.sha.slice(0, 9)}`);
}
