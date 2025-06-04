// test.js
const db = require('./modules/db');

(async () => {
  const res = await db.query('SELECT * FROM gmail_profiles LIMIT 1');
  console.log(res.rows);
})();