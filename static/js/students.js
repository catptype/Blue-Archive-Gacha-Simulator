let allSchools = document.getElementsByClassName("school-icon");
let allStudents = document.getElementsByClassName("student-card");
const delay = 10;
var isExecuting = false;

function selectSchool(element) {
    if (isExecuting) {
        console.log('showStudent is running ...');
        return;
    }

    isExecuting = true;

    let onclickID = element.id;

    for (let schoolEL of allSchools) {
        if (schoolEL.classList.contains("activated")) {
            schoolEL.classList.remove("activated");
        }

        if (schoolEL.id === onclickID) {
            schoolEL.classList.add("activated");
        }
    }

    hideAllStudents();

    if (onclickID === "all") {
        showAllStudents();
    } else {
        showStudents(onclickID);
    }
}

function hideAllStudents() {
    for (let student of allStudents) {
        if (!student.classList.contains("hidden")) {
            student.classList.add("hidden");
        }      
    }
}

function showAllStudents() {
    var i = 0;

    for (let student of allStudents) {
        if (student.classList.contains("hidden")) {
            setTimeout(() => {
                student.classList.remove("hidden");
            }, i * delay);
            i += 1;
        }      
    }

    setTimeout(() => {
        isExecuting = false;
    }, i * delay);
}

function showStudents(school) {
    var i = 0;

    for (let student of allStudents) {
        if (student.getAttribute("school") === school) {
            setTimeout(() => {
                student.classList.remove("hidden");
            }, i * delay);
            i += 1;
        }
    }

    setTimeout(() => {
        isExecuting = false;
    }, i * delay);
}