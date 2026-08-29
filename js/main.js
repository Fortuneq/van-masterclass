// Прокрутка каруселей отзывов стрелками
document.querySelectorAll("[data-slide]").forEach(function (btn) {
  btn.addEventListener("click", function () {
    var track = document.getElementById("reviews-track") ||
                document.getElementById("stories-track");
    var scope = btn.closest("section");
    if (scope) track = scope.querySelector(".reviews-track, .stories-track") || track;
    if (!track) return;
    var card = track.firstElementChild;
    var step = card ? card.getBoundingClientRect().width + 22 : 320;
    track.scrollBy({
      left: btn.dataset.slide === "next" ? step : -step,
      behavior: "smooth"
    });
  });
});

// В аккордеоне держим открытым только один пункт
document.querySelectorAll(".accordion").forEach(function (acc) {
  acc.querySelectorAll("details").forEach(function (d) {
    d.addEventListener("toggle", function () {
      if (!d.open) return;
      acc.querySelectorAll("details[open]").forEach(function (o) {
        if (o !== d) o.open = false;
      });
    });
  });
});

// Плавный скролл по якорям
document.querySelectorAll('a[href^="#"]').forEach(function (a) {
  a.addEventListener("click", function (e) {
    var t = document.querySelector(a.getAttribute("href"));
    if (t) { e.preventDefault(); t.scrollIntoView({ behavior: "smooth" }); }
  });
});
