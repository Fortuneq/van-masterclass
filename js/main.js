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

// Мобильное меню по бургеру
(function () {
  var burger = document.querySelector(".burger");
  var nav = document.querySelector(".nav");
  if (!burger || !nav) return;
  function close() {
    nav.classList.remove("open");
    burger.classList.remove("active");
    document.body.classList.remove("menu-open");
  }
  burger.addEventListener("click", function () {
    var open = nav.classList.toggle("open");
    burger.classList.toggle("active", open);
    document.body.classList.toggle("menu-open", open);
  });
  nav.querySelectorAll("a").forEach(function (a) {
    a.addEventListener("click", close);
  });
})();

// Форма обратного звонка → заявка уходит на сервер студии
function sendCallback(e, form) {
  e.preventDefault();
  var phone = (form.phone.value || "").trim();
  if (!phone) return false;
  var btn = form.querySelector("button");
  var old = btn.innerHTML;
  btn.disabled = true;
  btn.innerHTML = "Отправляем…";
  fetch("/api/lead", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ phone: phone, page: location.pathname })
  }).then(function (r) {
    if (!r.ok) throw new Error("bad");
    form.reset();
    btn.innerHTML = "Заявка принята ✓";
  }).catch(function () {
    btn.innerHTML = "Позвоните: 8 908 097 65 58";
  }).finally(function () {
    btn.disabled = false;
    setTimeout(function () { btn.innerHTML = old; }, 4000);
  });
  return false;
}

// Плавный скролл по якорям
document.querySelectorAll('a[href^="#"]').forEach(function (a) {
  a.addEventListener("click", function (e) {
    var t = document.querySelector(a.getAttribute("href"));
    if (t) { e.preventDefault(); t.scrollIntoView({ behavior: "smooth" }); }
  });
});
