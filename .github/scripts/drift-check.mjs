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
 *      hand. The check lists every upstream commit newer than the
 *      wiki's last commit on docs/technical/, so the flag stays up
 *      until a real mirror commit lands here.
 *
 * Findings go to one issue, titled "Wiki drift: ...". A run where
 * both signals are clear closes that issue.
 *
 * Run by .github/workflows/drift-check.yml. A local run without
 * REPO set is a dry run: it prints findings and touches nothing.
 *
 *     node .github/scripts/drift-check.mjs
 *
 * REPO ("owner/name") and GITHUB_TOKEN turn on the issue edits.
 */
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const root = join(here, "..", "..");

const REPO = process.env.REPO || "zoompilot/wiki";
const DRY = !process.env.REPO;
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
  throw new Error(
    "could not read the release version from zoompilot.ai — page markup changed?",
  );
}

const logText = readFileSync(
  join(root, "docs", "releases", "changelog.md"),
  "utf8",
);
const wikiVer = logText.match(/^## (\d{4}\.\d{2}\.\d{2}-\d+)/m)?.[1];

const releaseDrift = liveVer !== wikiVer;
console.log(
  `release: live ${liveVer} / wiki ${wikiVer} -> ${releaseDrift ? "DRIFT" : "ok"}`,
);

/* ---- signal 2: upstream docs vs the wiki's technical pages ---- */

/* committer dates are ISO 8601 UTC, so string compare works */
const wikiTech = await (
  await gh(`/repos/${REPO}/commits?sha=main&path=docs/technical&per_page=1`)
).json();
const wikiTechDate = wikiTech[0]?.commit?.committer?.date;
if (!wikiTechDate) {
  throw new Error("could not read the last docs/technical commit on this repo");
}
console.log(`wiki technical pages last touched ${wikiTechDate}`);

const docsCommits = [];
for (let p = 1; p <= 3 && docsCommits.length < 10; p++) {
  const batch = await (
    await gh(
      `/repos/zoompilot/zoompilot/commits?sha=develop&path=docs/zoompilot&per_page=30&page=${p}`,
    )
  ).json();
  if (!Array.isArray(batch)) break;
  for (const c of batch) {
    if (c.commit.committer.date <= wikiTechDate) {
      p = 4; // stop paging
      break;
    }
    docsCommits.push(c);
  }
}
const docsDrift = docsCommits.length > 0;
console.log(
  `docs: ${docsCommits.length} upstream commit(s) newer than the wiki -> ${docsDrift ? "DRIFT" : "ok"}`,
);

/* files per commit, for the issue body (details calls, capped) */
for (const c of docsCommits.slice(0, 5)) {
  const detail = await (
    await gh(`/repos/zoompilot/zoompilot/commits/${c.sha}`)
  ).json();
  c.files = (detail.files ?? [])
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
        "Commits touch `docs/zoompilot` on develop that are newer than",
        `this wiki's last docs/technical/ commit (${wikiTechDate.slice(0, 10)}).`,
        "The technical pages mirror these by hand:",
        "",
        ...docsCommits.map(
          (c) =>
            `- [\`${c.sha.slice(0, 9)}\`](https://github.com/zoompilot/zoompilot/commit/${c.sha}) ${c.commit.committer.date.slice(0, 10)} ${c.commit.message.split("\n")[0]}${c.files ? `\n  files: ${c.files.join(", ")}` : ""}`,
        ),
      ]
    : [];
  return [
    ...rel,
    ...docs,
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

const findings = [
  releaseDrift && "release notes",
  docsDrift && "upstream docs",
].filter(Boolean);

if (DRY) {
  console.log(
    findings.length
      ? `dry run, would flag: ${findings.join(", ")}`
      : "dry run, clear",
  );
  process.exit(0);
}

const issues = await (
  await gh(`/repos/${REPO}/issues?state=open&per_page=50`)
).json();
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
    body: `Clear as of ${new Date().toISOString().slice(0, 10)}: release ${wikiVer} is current, and the technical pages are newer than every docs/zoompilot commit.`,
  });
  await gh(`/repos/${REPO}/issues/${open.number}`, "PATCH", {
    state: "closed",
  });
  console.log(`closed issue #${open.number}`);
}
