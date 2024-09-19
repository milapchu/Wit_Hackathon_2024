let currentDate = new Date();

function generateCalendar(date, tasks = []) {
    const calendarBody = document.getElementById("calendarBody");
    const monthYear = document.getElementById("monthYear");

    // Clear previous calendar content
    calendarBody.innerHTML = "";

    const month = date.getMonth();
    const year = date.getFullYear();

    // Array of month names
    const monthNames = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];
    monthYear.textContent = `${monthNames[month]} ${year}`;

    // Get the first day of the month and the number of days in the month
    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    // Create rows for the calendar
    let row = document.createElement("tr");
    let day = 1;

    // Add empty cells before the first day of the month
    for (let i = 0; i < firstDay; i++) {
        const cell = document.createElement("td");
        cell.textContent = "";
        row.appendChild(cell);
    }

    // Add cells for the days of the month
    for (let i = firstDay; i < 7; i++) {
        const cell = document.createElement("td");
        cell.textContent = day;

        // Check if there is a task on this day
        const taskForDay = tasks.find(task => {
            return new Date(task.date).getDate() === day &&
                new Date(task.date).getMonth() === month &&
                new Date(task.date).getFullYear() === year;
        });

        if (taskForDay) {
            const taskDiv = document.createElement("div");
            taskDiv.textContent = taskForDay.taskName; // Show task name in the cell
            taskDiv.classList.add("task");
            cell.appendChild(taskDiv);
        }

        row.appendChild(cell);
        day++;
    }
    calendarBody.appendChild(row);

    // Create remaining rows for the month
    while (day <= daysInMonth) {
        row = document.createElement("tr");
        for (let i = 0; i < 7 && day <= daysInMonth; i++) {
            const cell = document.createElement("td");
            cell.textContent = day;

            const taskForDay = tasks.find(task => {
                return new Date(task.date).getDate() === day &&
                    new Date(task.date).getMonth() === month &&
                    new Date(task.date).getFullYear() === year;
            });

            if (taskForDay) {
                const taskDiv = document.createElement("div");
                taskDiv.textContent = taskForDay.taskName;
                taskDiv.classList.add("task");
                cell.appendChild(taskDiv);
            }

            row.appendChild(cell);
            day++;
        }
        calendarBody.appendChild(row);
    }
}

function prevMonth() {
    currentDate.setMonth(currentDate.getMonth() - 1);
    generateCalendar(currentDate);
}

function nextMonth() {
    currentDate.setMonth(currentDate.getMonth() + 1);
    generateCalendar(currentDate);
}

// Initialize the calendar when the page loads
generateCalendar(currentDate);

