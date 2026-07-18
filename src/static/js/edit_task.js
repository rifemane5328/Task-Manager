document.addEventListener("show.bs.modal", function (event) {
        // Беремо з кнопки дані про поточне завдання для передзаповнення полів
        const btn = event.relatedTarget;

        const task = JSON.parse(btn.dataset.task);
        const taskId = task.id;
        const role = task.user_role;
        const adminFields = document.querySelectorAll(".admin-field");

        // Ховаємо адміністратороські поля якщо користувач учасник
        if (role === 'member') {
            adminFields.forEach(field => field.classList.add('d-none'));
        } else {
            adminFields.forEach(field => field.classList.remove('d-none'));
        };

        const form = document.querySelector("#taskForm");
        const urlTemplate = form.dataset.urlTemplate;
        console.log(urlTemplate)
        const formTitle = document.querySelector("#formTitle");
        const formDesc = document.querySelector("#formDesc");
        const formDeadline = document.querySelector("#formDeadline");
        const formPriority = document.querySelector("#formPriority");
        const formStatus = document.querySelector("#formStatus");
        const formCategory = document.querySelector("#formCategory");
        const formAssignedTo = document.querySelector("#formAssignedTo");

        form.action = urlTemplate.replace('0', taskId);
        formTitle.value = task.title;
        formDesc.value = task.description;
        formDeadline.value = task.deadline;
        formPriority.value = task.priority;
        formStatus.value = task.status;
        formCategory.value = String(task.category_id);

        const teamMembersDict = JSON.parse(document.getElementById('team-members-data').textContent)
        // Потрібно зробити альтернативний варіант для завдань команди, там немає task.team_id
        const CurrentTeamMembers = teamMembersDict[task.team_id] || [];

        // Очищаємо тег select перед заповненням
        formAssignedTo.innerHTML = '<option value="">Немає</option>';

        // Створюємо тег option для кожного учасника команди
        CurrentTeamMembers.forEach(member => {
            const option = document.createElement('option');
            option.value = member.id;
            option.textContent = member.name;
            formAssignedTo.appendChild(option);
        });
        formAssignedTo.value = String(task.assigned_to_id);
    });