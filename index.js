const express = require('express');
const app = express();

const PORT = 3000;

app.get('/api/user', (req, res) => {
    const user = {
        id: 1,
        name: 'John Doe',
        email: 'john.doe@example.com'
    };

    res.json(user);
});

// Start the server and listen for incoming requests
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
