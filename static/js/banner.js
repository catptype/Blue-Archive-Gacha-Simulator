const selectorContainer = document.getElementById("gacha-selector");
const dots = document.getElementsByClassName("dot");
const maxIdx = selectorContainer.children[0].children.length;
let currentIndex = 0;
var isExecuting = false;
updateIndex(0)

function clearDots() {
    for (let dot of dots) {
    if (dot.classList.contains("actived"))
      dot.classList.remove("actived");
  }
}

function updateIndex(idx) {
    if (isExecuting) {
        console.log('Gacha selector is scrolling ...');
        return;
    }
    isExecuting = true;
    currentIndex += idx;

    if (currentIndex < 0) {
        currentIndex = 0;
    } else if (currentIndex >= maxIdx) {
        currentIndex = maxIdx - 1;
    }
    clearDots()
    dots[currentIndex].classList.add("actived");
    selectorContainer.scrollLeft = currentIndex * selectorContainer.offsetWidth;
    setTimeout(() => {
        isExecuting = false;
    }, 400);
}

function jumpIndex(idx) {
    if (isExecuting) {
        console.log('Gacha selector is scrolling ...');
        return;
    }
    isExecuting = true;
    currentIndex = idx;

    if (currentIndex < 0) {
        currentIndex = 0;
    } else if (currentIndex >= maxIdx) {
        currentIndex = maxIdx - 1;
    }

    clearDots()
    dots[currentIndex].classList.add("actived");
    selectorContainer.scrollLeft = currentIndex * selectorContainer.offsetWidth;
    setTimeout(() => {
        isExecuting = false;
    }, 400);
}