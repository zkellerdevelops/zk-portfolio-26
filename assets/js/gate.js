/* Lightweight client-side password gate.
   NOTE: This is NOT real security — the protected content ships in the page
   source and is discoverable by anyone who views source. It only mirrors the
   original Webflow password prompt as a soft gate. Password: "thinkbig". */
(function () {
  var PASSWORD = "thinkbig";
  var KEY = "zk-unlocked";

  function unlock() {
    document.body.classList.add("unlocked");
    try { sessionStorage.setItem(KEY, "1"); } catch (e) {}
  }

  document.addEventListener("DOMContentLoaded", function () {
    if (sessionStorage.getItem(KEY) === "1") { unlock(); return; }
    var form = document.getElementById("gate-form");
    if (!form) return;
    var input = document.getElementById("gate-input");
    var error = document.getElementById("gate-error");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (input.value === PASSWORD) {
        unlock();
      } else {
        error.textContent = "Incorrect password. Try again.";
        input.value = "";
        input.focus();
      }
    });
  });
})();
