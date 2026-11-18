// // const taskContainer = document.querySelector(".task-category");
// // const test = document.querySelector("ul");

// // taskContainer.addEventListener("click", (e) => {
// //   console.log("world")
// //   if (
// //     e.target.classList.contains("delete-btn") ||
// //     e.target.parentElement.classList.contains("delete-btn")
// //   ) {
// //     let task = e.target.closest(".task");
// //     task.remove();
// //   }
// //   if (!test.innerHTML.includes("li")) {
// //     test.innerHTML = "<li>No tasks yet.</li>";
// //   }
// // });


// // let deleteTask = document.querySelectorAll(".delete-btn");

// // deleteTask.forEach((deleted) => {
// //     deleted.addEventListener
// const taskContainerAll = document.querySelectorAll(".task-category");
// const taskParentAll = document.querySelectorAll("ul");
// const forms = document.forms;

// // create elements
// const createTaskBtn = document.createElement("button");
// createTaskBtn.className = "delete-btn";
// createTaskBtn.innerHTML = '<ion-icon name="trash-outline"></ion-icon>';



// // createTaskBtn.classList.add("delete-btn");
// // createTaskBtn.toggle("delete-btn");

// // console.log(forms["add-task-form"]);
// forms["add-task-form"].addEventListener("submit", (e) => {
//   e.preventDefault();
//   const createTask = document.createElement("li");
//   createTask.className = "task";
//   createTask.appendChild(createTaskBtn);
//   console.log(createTask);
//   createTask.innerHTML =
//     forms["add-task-form"].querySelector("input").value + createTask.innerHTML;
//   if (forms["add-task-form"].querySelector("#categories").value === "Work") {
//     taskParentAll[0].appendChild(createTask);
//   } else if (forms["add-task-form"].querySelector("#categories").value === "School"){
//     taskParentAll[1].appendChild(createTask);
//   } else if (forms["add-task-form"].querySelector("#categories").value === "Grocery"){
//     taskParentAll[2].appendChild(createTask);
//   } else if (forms["add-task-form"].querySelector("#categories").value === "General"){
//     taskParentAll[3].appendChild(createTask);
//   }

// });

// // Loop through all task-categories
// taskContainerAll.forEach((taskContainer) => {
//   taskContainer.addEventListener("click", (e) => {
//     if (
//       e.target.parentElement.className === "delete-btn" ||
//       e.target.className === "delete-btn"
//     ) {
//       e.target.closest(".task").remove();
//     }
//     if (e.target.className === "delete-all-btn"){
//       e.target.previousElementSibling.children.remove();
//     }

//     taskParentAll.forEach((taskParent) => { 
//       if (!taskParent.innerHTML.includes("li")) {
//         taskParent.innerHTML = "<li>No tasks yet.</li>";
//       }
//     });
//   });
// });
const taskContainerAll = document.querySelectorAll(".task-category");
const taskParentAll = document.querySelectorAll("ul");
const forms = document.forms;

// create elements

// append elements

// createTaskBtn.classList.add("delete-btn");
// createTaskBtn.toggle("delete-btn");

// console.log(forms["add-task-form"]);
forms["add-task-form"].addEventListener("submit", (e) => {
  e.preventDefault();
  taskParentAll.forEach((taskParent) => {
    if (taskParent.firstElementChild.className === "test") {
      taskParent.firstElementChild.remove();
      // console.log("fine fine");
    }
  });

  const createTask = document.createElement("li");
  createTask.className = "task";
  const createTaskBtn = document.createElement("button");
  createTaskBtn.className = "delete-btn";
  createTaskBtn.innerHTML = '<ion-icon name="trash-outline"></ion-icon>';
  createTask.appendChild(createTaskBtn);
  // console.log(createTask); 
  createTask.innerHTML =
    forms["add-task-form"].querySelector("input").value + createTask.innerHTML;
  if (forms["add-task-form"].querySelector("#categories").value === "Work") {
    taskParentAll[0].appendChild(createTask);
  }
  if (forms["add-task-form"].querySelector("#categories").value === "School") {
    taskParentAll[1].appendChild(createTask);
  }
  if (forms["add-task-form"].querySelector("#categories").value === "Grocery") {
    taskParentAll[2].appendChild(createTask);
  }
  if (forms["add-task-form"].querySelector("#categories").value === "General") {
    taskParentAll[3].appendChild(createTask);
  }
});

// Loop through all task-categories
taskContainerAll.forEach((taskContainer) => {
  taskContainer.addEventListener("click", (e) => {
    if (
      e.target.parentElement.className === "delete-btn" ||
      e.target.className === "delete-btn"
    ) {
      e.target.closest(".task").remove();
    }

    if (e.target.className === "delete-all-btn") {
      let test = e.target.previousElementSibling.children;
      test = Array.from(test);
      test.forEach((sibling) => {
        sibling.remove();
      });
    }
    taskParentAll.forEach((taskParent) => {
      if (taskParent.children.length === 0) {
        taskParent.innerHTML = '<li class="test">No tasks yet.</li>';
      }
    });
  });
});

