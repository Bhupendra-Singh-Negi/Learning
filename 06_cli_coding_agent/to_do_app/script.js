const todoInput = document.getElementById('todoInput');
const addBtn = document.getElementById('addBtn');
const todoList = document.getElementById('todoList');

let todos = JSON.parse(localStorage.getItem('todos')) || [];

function renderTodos() {
    todoList.innerHTML = '';
    todos.forEach((todo, index) => {
        const li = document.createElement('li');
        li.innerHTML = `<div class="todo-text ${todo.completed ? 'completed' : ''}" onclick="toggleComplete(${index})">${todo.text}</div>
            <div class="actions">
                <button class="edit-btn" onclick="editTodo(${index})">Edit</button>
                <button class="delete-btn" onclick="deleteTodo(${index})">Delete</button>
            </div>
        `;
        todoList.appendChild(li);
    });
}

function addTodo() {
    const text = todoInput.value.trim();
    if (text === '') return;
    todos.push({ text, completed: false });
    saveTodos();
    todoInput.value = '';
}

function deleteTodo(index) {
    todos.splice(index, 1);
    saveTodos();
}

function editTodo(index) {
    const newText = prompt('Edit your todo:', todos[index].text);
    if (newText !== null && newText.trim() !== '') {
        todos[index].text = newText.trim();
        saveTodos();
    }
}

function toggleComplete(index) {
    todos[index].completed = !todos[index].completed;
    saveTodos();
}

function saveTodos() {
    localStorage.setItem('todos', JSON.stringify(todos));
    renderTodos();
}

addBtn.addEventListener('click', addTodo);

todoInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') addTodo();
});

renderTodos();