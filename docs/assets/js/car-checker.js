/*
 * "Is my Mazda supported?" — the steering-motor question for
 * docs/getting-started/supported-cars.md.
 *
 * The matrix on this page answers every listed platform. This block
 * answers the one question a table cannot: which steering motor is in
 * THIS car. That is what the steering envelope keys on, and it is the
 * route for Mazdas outside the platform list.
 */
(function () {
  "use strict";

  var mount = document.getElementById("zp-car-checker");
  if (!mount) return;

  mount.innerHTML = "";
  mount.className = "zp-checker";

  function option(value, label) {
    var o = document.createElement("option");
    o.value = value;
    o.textContent = label;
    return o;
  }

  var form = document.createElement("div");
  form.className = "zp-checker-form";

  var labelMotor = document.createElement("label");
  labelMotor.textContent = "Which steering motor is in the car?";
  var motor = document.createElement("select");
  motor.appendChild(option("", "Choose…"));
  motor.appendChild(option("stock", "Original motor, never swapped"));
  motor.appendChild(option("swap", "2022–25 CX-5 motor swapped in"));
  motor.appendChild(option("unsure", "Not sure"));
  labelMotor.appendChild(motor);
  form.appendChild(labelMotor);
  mount.appendChild(form);

  var out = document.createElement("div");
  out.className = "zp-checker-out";
  out.setAttribute("role", "status");
  mount.appendChild(out);

  function verdict(title, body, good) {
    out.innerHTML = "";
    var t = document.createElement("strong");
    t.textContent = title;
    if (good === true) t.classList.add("is-good");
    if (good === false) t.classList.add("is-bad");
    var p = document.createElement("p");
    /* body may carry one {{EPS_SWAP}} placeholder for the eps-swap
     * page link; this page and eps-swap are siblings, and the wiki
     * builds with directory URLs, so the relative link is the page
     * directory name */
    p.innerHTML = body.replace(
      /\{\{EPS_SWAP\}\}/g,
      '<a href="eps-swap/">the EPS swap</a>',
    );
    out.appendChild(t);
    out.appendChild(p);
    out.hidden = false;
  }

  motor.addEventListener("change", function () {
    if (motor.value === "swap") {
      verdict(
        "Supported — the swap is what does it.",
        "The 2022-25 CX-5 EPS motor identifies by firmware: steering works" +
          " down to 0 mph and alpha longitudinal turns on — radar and AEB" +
          " off while it is on. The pre-2021 CX-9 is the one exception:" +
          " its radar does not publish the track frames, so alpha long" +
          " stays off.",
        true,
      );
    } else if (motor.value === "stock") {
      verdict(
        "Supported — on the stock steering envelope.",
        "zoompilot runs on the stock motor with the stock torque envelope:" +
          " no steer-to-zero. {{EPS_SWAP}} unlocks steering down to 0 mph" +
          " and alpha longitudinal, radar and AEB off while it is on. The" +
          " pre-2021 CX-9 is the one exception: it keeps alpha long off.",
        true,
      );
    } else if (motor.value === "unsure") {
      verdict(
        "Check the motor first.",
        "Support depends on which steering motor the car has, not just the" +
          " model year. {{EPS_SWAP}} explains what to look for, or ask on" +
          " the Discord with your model year.",
      );
    } else {
      out.hidden = true;
    }
  });
})();
