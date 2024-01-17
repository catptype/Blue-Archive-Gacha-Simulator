var isExecuting = false;

function toggleVisible(element) {
    if (isExecuting) {
        console.log('toggleVisible is running ...');
        return;
    }
    isExecuting = true;
    element.querySelector('.hamburger').classList.toggle('opened');
    element.querySelector('.detail-container').classList.toggle('hidden');
    
    setTimeout(() => {
        isExecuting = false;
    }, 400);
}