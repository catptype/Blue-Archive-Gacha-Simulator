var isExecuting = false;

function selectSchool(element) {
    if (isExecuting) {
        console.log('showStudent is running ...');
        return;
    }

    isExecuting = true;

    let onclickID = element.id;
    let allSchools = document.getElementsByClassName("school-icon");

    for (let schoolEL of allSchools) {
        if (schoolEL.classList.contains("activated")) {
            schoolEL.classList.remove("activated");
        }

        if (schoolEL.id === onclickID) {
            schoolEL.classList.add("activated");
        }
    }

    if (onclickID === "all") {
        showAllStudents()
    } else {
        showStudents(onclickID);
    }
}

function showAllStudents() {
    let allStudents = document.getElementsByClassName("student-card");
    for (let student of allStudents) {
        if (student.classList.contains("hidden")) {
            student.classList.remove("hidden");
        }      
    }
    isExecuting = false;
}

function showStudents(school) {
    let allStudents = document.getElementsByClassName("student-card");
    const delay = 20;
    var i = 0;

    for (let student of allStudents) {
        if (student.getAttribute("school") === school) {
            setTimeout(() => {
                student.classList.remove("hidden");
            }, i * delay);
            i += 1;
        } else {
            student.classList.add("hidden");
        }
    }

    setTimeout(() => {
        isExecuting = false;
    }, i * delay);
}