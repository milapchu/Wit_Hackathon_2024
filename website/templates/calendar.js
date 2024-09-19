let currentDate = new Date();

function generateCalendar(date, tasks = []) {
    const calendarBody = document.getElementById("calendarBody");
    const monthYear = document.getElementById("monthYear");

    // Clear previous calendar cells
    calendarBody.innerHTML = "";

    // Get month and year
    const month = date.getMonth();
    const year = date.getFullYear();

    // Set the month and year in the header
    const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    monthYear.textContent = `${monthNames[month]} ${year}`;

    // Get the first day and number of days in the month
    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    // Create the rows and cells for the calendar
    let row = document.createElement("tr");
    let day = 1;

    // Add empty cells before the first day of the month
    for (let i = 0; i < firstDay; i++) {
        const cell = document.createElement("td");
        cell.textContent = "";
        row.appendChild(cell);
    }

    // Add the days of the month
    for (let i = firstDay; i < 7; i++) {
        const cell = document.createElement("td");
        cell.textContent = day;
        
        // Check if there is a task on this day
        const taskForDay = tasks.find(task => new Date(task.date).getDate() === day);
        if (taskForDay) {
            const taskDiv = document.createElement("div");
            taskDiv.textContent = taskForDay.taskName; // Show task name in the cell
            cell.appendChild(taskDiv);
        }

        row.appendChild(cell);
        day++;
    }
    calendarBody.appendChild(row);

    // Continue adding rows and days
    while (day <= daysInMonth) {
        row = document.createElement("tr");
        for (let i = 0; i < 7 && day <= daysInMonth; i++) {
            const cell = document.createElement("td");
            cell.textContent = day;

            // Check if there is a task on this day
            const taskForDay = tasks.find(task => new Date(task.date).getDate() === day);
            if (taskForDay) {
                const taskDiv = document.createElement("div");
                taskDiv.textContent = taskForDay.taskName;
                cell.appendChild(taskDiv);
            }

            row.appendChild(cell);
            day++;
        }
        calendarBody.appendChild(row);
    }
}

// Go to the previous month
function prevMonth() {
    currentDate.setMonth(currentDate.getMonth() - 1);
    generateCalendar(currentDate);
}

// Go to the next month
function nextMonth() {
    currentDate.setMonth(currentDate.getMonth() + 1);
    generateCalendar(currentDate);
}

// Generate the current month when the page loads
generateCalendar(currentDate);
