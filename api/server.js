// Bitcoin Price API - Simple Server
const express = require('express');
const app = express();

app.use(express.json());

// Returns random Bitcoin price between 50,000 - 200,000 USD
app.get('/price', (req, res) => {
  const price = Math.floor(Math.random() * 150000) + 50000;
  console.log(`Bitcoin price: $${price}`);
  res.json({ price });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Bitcoin API running on port ${PORT}`);
});

