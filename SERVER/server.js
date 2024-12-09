const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path');
const jwt = require('jsonwebtoken');
const nodemailer = require('nodemailer');
const crypto = require('crypto'); // For generating random strings

const app = express();
const port = 5000;

app.use(bodyParser.json());

// Serve static files from the public directory
app.use(express.static(path.join(__dirname, 'public')));

// Mock database file path
const usersFilePath = path.join(__dirname, 'login', 'login.json');
const dataDir = path.join(__dirname, 'data');

// Ensure data directory exists
if (!fs.existsSync(dataDir)) {
    fs.mkdirSync(dataDir);
}

// Load users from file or initialize as empty object
const loadUsers = () => {
    if (fs.existsSync(usersFilePath)) {
        const data = fs.readFileSync(usersFilePath, 'utf8');
        return JSON.parse(data);
    }
    return {};
};

// Save users to file
const saveUsers = (users) => {
    fs.writeFileSync(usersFilePath, JSON.stringify(users, null, 2));
};

// Generate random string
const generateRandomString = (length = 8) => {
    return crypto.randomBytes(length).toString('hex');
};

// JWT Secret
const jwtSecret = 'your_jwt_secret';

// Function to send email
const sendEmail = (email, subject, text) => {
    const transporter = nodemailer.createTransport({
        service: 'Gmail',
        auth: {
            user: 'your-email@gmail.com',
            pass: 'your-email-password'
        }
    });

    const mailOptions = {
        from: 'your-email@gmail.com',
        to: email,
        subject: subject,
        text: text
    };

    transporter.sendMail(mailOptions, (error, info) => {
        if (error) {
            console.error(`Error sending email: ${error}`);
        } else {
            console.log(`Email sent: ${info.response}`);
        }
    });
};
// Utility functions for database operations
function loadDBConfig() {
    const configPath = path.join(__dirname, 'DB', 'db_config.json');
    const rawData = fs.readFileSync(configPath);
    return JSON.parse(rawData);
}

function saveDBConfig(config) {
    const configPath = path.join(__dirname, 'DB', 'db_config.json');
    fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
}

function listDatabases() {
    const config = loadDBConfig();
    return config.databases;
}

function listTables(dbName) {
    const dbPath = path.join(__dirname, 'DB', dbName, 'list.json');
    const rawData = fs.readFileSync(dbPath);
    const db = JSON.parse(rawData);
    return db.tables;
}

function viewTableData(dbName, tableName) {
    const tablePath = path.join(__dirname, 'DB', dbName, tableName);
    const files = fs.readdirSync(tablePath);
    const data = files.filter(file => file.endsWith('.json')).map(file => {
        const rawData = fs.readFileSync(path.join(tablePath, file));
        return JSON.parse(rawData);
    });
    return data;
}

function createDatabase(dbName) {
    const config = loadDBConfig();
    if (config.databases.includes(dbName)) {
        throw new Error(`Database ${dbName} already exists.`);
    }
    config.databases.push(dbName);
    saveDBConfig(config);

    const dbPath = path.join(__dirname, 'DB', dbName);
    fs.mkdirSync(dbPath);
    fs.writeFileSync(path.join(dbPath, 'list.json'), JSON.stringify({ tables: [] }, null, 2));
}

function createTable(dbName, tableName) {
    const dbPath = path.join(__dirname, 'DB', dbName);
    const listPath = path.join(dbPath, 'list.json');

    const dbConfig = JSON.parse(fs.readFileSync(listPath));
    if (dbConfig.tables.includes(tableName)) {
        throw new Error(`Table ${tableName} already exists in database ${dbName}.`);
    }
    dbConfig.tables.push(tableName);
    fs.writeFileSync(listPath, JSON.stringify(dbConfig, null, 2));

    const tablePath = path.join(dbPath, tableName);
    fs.mkdirSync(tablePath);
    fs.writeFileSync(path.join(tablePath, 'table_config.json'), JSON.stringify({ columns: {} }, null, 2));
}

function insertData(dbName, tableName, data) {
    const tablePath = path.join(__dirname, 'DB', dbName, tableName);
    const timestamp = Date.now().toString();
    fs.writeFileSync(path.join(tablePath, `${timestamp}.json`), JSON.stringify(data, null, 2));
}

// API routes
app.get('/list-databases', (req, res) => {
    const databases = listDatabases();
    res.json(databases);
});

app.get('/list-tables', (req, res) => {
    const dbName = req.query.dbName;
    const tables = listTables(dbName);
    res.json(tables);
});

app.get('/view-table-data', (req, res) => {
    const dbName = req.query.dbName;
    const tableName = req.query.tableName;
    const data = viewTableData(dbName, tableName);
    res.json(data);
});

app.post('/create-database', (req, res) => {
    const dbName = req.body.dbName;
    try {
        createDatabase(dbName);
        res.json({ message: `Database ${dbName} created successfully.` });
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
});

app.post('/create-table', (req, res) => {
    const { dbName, tableName } = req.body;
    try {
        createTable(dbName, tableName);
        res.json({ message: `Table ${tableName} created successfully in database ${dbName}.` });
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
});

app.post('/insert-data', (req, res) => {
    const { dbName, tableName, data } = req.body;
    try {
        insertData(dbName, tableName, data);
        res.json({ message: `Data inserted into table ${tableName} in database ${dbName}.` });
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
});

// Register user
app.post('/register', (req, res) => {
    const { username, email } = req.body;
    const users = loadUsers();
    if (users[username]) {
        return res.status(400).json({ message: 'User already exists' });
    }

    users[username] = { email, token: null };
    saveUsers(users);
    res.status(201).json({ message: 'User registered successfully' });
});

// Login user
app.post('/login', (req, res) => {
    const { username, email } = req.body;
    const users = loadUsers();
    const user = users[username];

    if (!user || user.email !== email) {
        return res.status(400).json({ message: 'Invalid username or email' });
    }

    const token = jwt.sign({ username }, jwtSecret, { expiresIn: '1h' });
    user.token = token;
    saveUsers(users);

    res.json({ message: 'Login successful', token });
});

// Forgot password
app.post('/forgot-password', (req, res) => {
    const { email } = req.body;
    const users = loadUsers();
    const user = Object.values(users).find(u => u.email === email);

    if (!user) {
        return res.status(400).json({ message: 'Email not found' });
    }

    const token = jwt.sign({ email }, jwtSecret, { expiresIn: '1h' });
    sendEmail(email, 'Password Reset', `Your password reset token is ${token}`);
    res.json({ message: 'Password reset email sent' });
});

// Encrypt data
app.post('/encrypt', (req, res) => {
    const { data, key } = req.body;
    const cipher = crypto.createCipher('aes-256-cbc', key);
    let encrypted = cipher.update(data, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    res.json({ encryptedData: encrypted });
});

// Decrypt data
app.post('/decrypt', (req, res) => {
    const { encryptedData, key } = req.body;
    const decipher = crypto.createDecipher('aes-256-cbc', key);
    let decrypted = decipher.update(encryptedData, 'hex', 'utf8');
    decrypted += decipher.final('utf8');
    res.json({ decryptedData: decrypted });
});

// Endpoint to send data to the main user
app.post('/send-data', (req, res) => {
    const { token, data } = req.body;
    const users = loadUsers();
    const user = Object.values(users).find(u => u.token === token);

    if (!user) {
        return res.status(400).json({ message: 'Invalid token' });
    }

    const userDir = path.join(dataDir, token);
    if (!fs.existsSync(userDir)) {
        fs.mkdirSync(userDir);
    }

    let filePath;
    do {
        const randomFileName = `${generateRandomString()}.json`;
        filePath = path.join(userDir, randomFileName);
    } while (fs.existsSync(filePath));

    fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
    res.json({ message: 'Data sent successfully', filePath });
});

// Endpoint to retrieve data using token
app.post('/retrieve-data', (req, res) => {
    const { token } = req.body;
    const userDir = path.join(dataDir, token);

    if (!fs.existsSync(userDir)) {
        return res.status(404).json({ message: 'No data found for this token' });
    }

    const files = fs.readdirSync(userDir).filter(file => file.endsWith('.json'));

    if (files.length === 0) {
        return res.status(404).json({ message: 'No more data available' });
    }

    const randomFile = files[Math.floor(Math.random() * files.length)];
    const data = fs.readFileSync(path.join(userDir, randomFile), 'utf8');

    // Send the data
    res.json({ data: JSON.parse(data), filename: randomFile });

    // Delete the file after sending
    fs.unlinkSync(path.join(userDir, randomFile));

    // Delete the folder if it is empty
    if (fs.readdirSync(userDir).length === 0) {
        fs.rmdirSync(userDir);
    }
});


app.listen(port, '0.0.0.0', () => {
    console.log(`Server running on http://0.0.0.0:${port}`);
});
