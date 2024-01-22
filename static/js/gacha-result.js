const items = document.getElementsByClassName('result-item');
const showAll = document.getElementById('show-all');
const drawAgain = document.getElementById('draw-again');
const delay = 100;

function showCurrentItem(element) {
    var isShowAll = true;
    if (!element.classList.contains('showed')) {
        element.classList.add('showed');
    }

    for (let item of items) {
        if (!item.classList.contains('showed')) {
            showAll = false;
        }
    }

    if (isShowAll) {
        setTimeout(() => {
            showAll.classList.add('hidden');
            drawAgain.classList.remove('hidden');
        }, 500);
    }
}

function showAllItems() {
    var i = 0;

    showAll.classList.add('hidden');
    drawAgain.classList.remove('hidden');
    drawAgain.classList.add('hold');

    for (let item of items) {
        setTimeout(() => {
            item.classList.add('showed')
        }, i * delay);
        i += 1;
    }

    setTimeout(() => {
        drawAgain.classList.remove('hold');
    }, (i * delay) + 500);
}