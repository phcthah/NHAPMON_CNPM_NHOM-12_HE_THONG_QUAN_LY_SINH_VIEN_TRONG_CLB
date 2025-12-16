const express = require('express');
const mysql = require('mysql2');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

const db = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: '',
    database: 'clb'
});

app.post('/api/thu-quy', (req, res) => {
    const { HoTen, Ban, SoTien, LyDo, ThoiGianNop } = req.body;

    if (!HoTen || !Ban || !SoTien || !ThoiGianNop) {
        return res.status(400).json({ message: 'Vui lòng nhập đầy đủ thông tin' });
    }

    if (isNaN(SoTien)) {
        return res.status(400).json({ message: 'Số tiền phải là số' });
    }

    const sql = `
        INSERT INTO THU_QUY (HoTen, Ban, SoTien, LyDo, ThoiGianNop)
        VALUES (?, ?, ?, ?, ?)
    `;

    db.query(sql, [HoTen, Ban, SoTien, LyDo, ThoiGianNop], err => {
        if (err) return res.status(500).json({ message: 'Lỗi lưu dữ liệu' });
        res.json({ message: 'Ghi nhận thu quỹ thành công' });
    });
});

app.get('/api/thu-quy', (req, res) => {
    db.query('SELECT * FROM THU_QUY', (err, results) => {
        if (err) return res.status(500).json({ message: 'Lỗi lấy dữ liệu' });
        res.json(results);
    });
});

app.listen(3000, () => {
    console.log('Server chạy http://localhost:3000');
});
