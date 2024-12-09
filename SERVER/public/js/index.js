document.getElementById('login-button').addEventListener('click', login);
document.getElementById('list-databases').addEventListener('click', listDatabases);
document.getElementById('list-tables').addEventListener('click', listTables);
document.getElementById('view-data').addEventListener('click', viewTableData);

let token = '';

function login() {
    token = document.getElementById('token').value;
    if (token) {
        document.getElementById('login-section').classList.add('hidden');
        document.getElementById('database-section').classList.remove('hidden');
        document.getElementById('table-section').classList.remove('hidden');
        document.getElementById('data-section').classList.remove('hidden');
    } else {
        alert('Please enter a valid token');
    }
}

function listDatabases() {
    fetch(`/list-databases`)
        .then(response => response.json())
        .then(databases => {
            const databasesList = document.getElementById('databases-list');
            databasesList.innerHTML = '';
            databases.forEach(db => {
                const li = document.createElement('li');
                li.textContent = db;
                databasesList.appendChild(li);
            });
        });
}

function listTables() {
    const dbName = document.getElementById('database-name').value;
    fetch(`/list-tables?dbName=${dbName}`)
        .then(response => response.json())
        .then(tables => {
            const tablesList = document.getElementById('tables-list');
            tablesList.innerHTML = '';
            tables.forEach(table => {
                const li = document.createElement('li');
                li.textContent = table;
                tablesList.appendChild(li);
            });
        });
}

function viewTableData() {
    const dbName = document.getElementById('database-name').value;
    const tableName = document.getElementById('table-name').value;
    fetch(`/view-table-data?dbName=${dbName}&tableName=${tableName}`)
        .then(response => response.json())
        .then(data => {
            const tableDataDiv = document.getElementById('table-data');
            tableDataDiv.innerHTML = generateTableHTML(data);
        });
}

function generateTableHTML(data) {
    if (data.length === 0) return '<p>No data available.</p>';

    let tableHTML = '<table class="min-w-full bg-white border">';
    tableHTML += '<thead><tr>';
    Object.keys(data[0]).forEach(key => {
        tableHTML += `<th class="px-4 py-2 border">${key}</th>`;
    });
    tableHTML += '</tr></thead><tbody>';
    data.forEach(row => {
        tableHTML += '<tr>';
        Object.values(row).forEach(value => {
            tableHTML += `<td class="px-4 py-2 border">${value}</td>`;
        });
        tableHTML += '</tr>';
    });
    tableHTML += '</tbody></table>';

    return tableHTML;
}
