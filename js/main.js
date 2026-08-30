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

// Форма обратного звонка → отправляем заявку студии в WhatsApp
function sendCallback(e, form) {
  e.preventDefault();
  var phone = (form.phone.value || "").trim();
  if (!phone) return false;
  var text = encodeURIComponent("Здравствуйте! Перезвоните мне, пожалуйста: " + phone);
  window.open("https://api.whatsapp.com/send/?phone=79080976558&text=" + text, "_blank");
  form.reset();
  var btn = form.querySelector("button");
  if (btn) {
    var old = btn.innerHTML;
    btn.innerHTML = "Заявка отправлена ✓";
    setTimeout(function () { btn.innerHTML = old; }, 3000);
  }
  return false;
}

// Плавный скролл по якорям
document.querySelectorAll('a[href^="#"]').forEach(function (a) {
  a.addEventListener("click", function (e) {
    var t = document.querySelector(a.getAttribute("href"));
    if (t) { e.preventDefault(); t.scrollIntoView({ behavior: "smooth" }); }
  });
});
