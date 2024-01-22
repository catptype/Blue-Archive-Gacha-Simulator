var isExecuting = false;

function toggleVisible(id) {
    if (isExecuting) {
        console.log('toggleVisible is running ...');
        return;
    }
    isExecuting = true;

    element = document.getElementById(id);
    element.querySelector('.hamburger').classList.toggle('opened');
    element.querySelector('.detail-content').classList.toggle('hidden');
    
    setTimeout(() => {
        isExecuting = false;
    }, 400);
}