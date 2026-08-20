const frontendHost = window.location.hostname;
const API_URL = window.location.port === "8000"
    ? window.location.origin
    : ["localhost", "127.0.0.1", "0.0.0.0", "::1"].includes(frontendHost)
    ? "http://127.0.0.1:8000"
    : `${window.location.protocol}//${frontendHost.replace(
        /-\d+\.app\.github\.dev$/,
        "-8000.app.github.dev"
    )}`;

window.onload = () => {
    loadTasks();
};


async function loadTasks() {

    try {
        const response = await fetch(`${API_URL}/tasks`);

        if (!response.ok) {
            throw new Error(`Request failed with status ${response.status}`);
        }

        const tasks = await response.json();

        const taskList =
            document.getElementById("taskList");

        taskList.innerHTML = "";

        tasks.forEach(task => {

        taskList.innerHTML += `

        <li class="task-item">

            <span class="task-title ${
                task.completed ? "completed" : ""
            }">
                ${task.title}
            </span>

            <div class="actions">

                ${
                    !task.completed
                    ? `<button
                         class="complete-btn"
                         onclick="completeTask(${task.id})">
                         Complete
                       </button>`
                    : ""
                }

                <button
                    class="edit-btn"
                    onclick="editTask(${task.id},
                    '${task.title}')">
                    Edit
                </button>

                <button
                    class="delete-btn"
                    onclick="deleteTask(${task.id})">
                    Delete
                </button>

            </div>

        </li>

        `;
        });
    } catch (error) {
        console.error("Unable to load tasks:", error);
        document.getElementById("taskList").innerHTML =
            "<li class=\"task-item\">Unable to connect to the backend.</li>";
    }

}


async function addTask() {

    const taskInput =
        document.getElementById("taskInput");

    const title = taskInput.value.trim();

    if (!title) {
        alert("Enter a task");
        return;
    }

    try {
        const response = await fetch(
            `${API_URL}/tasks`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    title: title
                })
            }
        );

        if (!response.ok) {
            throw new Error(`Request failed with status ${response.status}`);
        }

        taskInput.value = "";
        await loadTasks();
    } catch (error) {
        console.error("Unable to add task:", error);
        alert("Unable to add task. Make sure the backend is running.");
    }
}


async function deleteTask(id) {

    const confirmDelete =
        confirm("Delete this task?");

    if (!confirmDelete) return;

    await fetch(
        `${API_URL}/tasks/${id}`,
        {
            method: "DELETE"
        }
    );

    loadTasks();
}


async function completeTask(id) {

    await fetch(
        `${API_URL}/tasks/${id}/complete`,
        {
            method: "PATCH"
        }
    );

    loadTasks();
}


async function editTask(id, oldTitle) {

    const newTitle =
        prompt("Edit Task", oldTitle);

    if (
        newTitle === null ||
        newTitle.trim() === ""
    ) {
        return;
    }

    await fetch(
        `${API_URL}/tasks/${id}`,
        {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                title: newTitle
            })
        }
    );

    loadTasks();
}