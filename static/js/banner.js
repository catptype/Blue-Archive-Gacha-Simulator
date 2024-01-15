let bannerIdx = 1;
showBanner(bannerIdx);

// Next/previous controls
function updateIndex(n) {
    showBanner(bannerIdx += n);
}

// Thumbnail image controls
function currentSlide(n) {
    showBanner(bannerIdx = n);
}

function showBanner(n) {
  let i;
  let slides = document.getElementsByClassName("gacha-banner");
  let dots = document.getElementsByClassName("dot");
  if (n > slides.length) {bannerIdx = 1}
  if (n < 1) {bannerIdx = slides.length}
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[bannerIdx-1].style.display = "block";
  dots[bannerIdx-1].className += " active";
}