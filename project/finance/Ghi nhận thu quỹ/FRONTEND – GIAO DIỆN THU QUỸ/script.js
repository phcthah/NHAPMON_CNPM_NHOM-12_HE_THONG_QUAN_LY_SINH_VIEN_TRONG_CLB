const api = 'http://localhost:3000/api/thu-quy';

const form = document.getElementById('form');
const msg = document.getElementById('msg');
const list = document.getElementById('list');

form.onsubmit = async (e) => {
    e.preventDefault();

    const data = {
        HoTen: document.getElementById('HoTen').value,
        Ban: document.getElementById('Ban').value,
        SoTien: document.getElementById('SoTien').value,
        LyDo: document.getElementById('LyDo').value,
        ThoiGianNop: document.getElementById('ThoiGianNop').value
    };

    const res = await fetch(api, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });

    const r = await res.json();
    msg.innerText = r.message;

    form.reset();
    load();
};

async function load() {
    const res = await fetch(api);
    const data = await res.json();

    list.innerHTML = '';
    data.forEach(i => {
        list.innerHTML += `
        <tr>
            <td>${i.HoTen}</td>
            <td>${i.Ban}</td>
            <td>${i.SoTien}</td>
            <td>${i.LyDo || ''}</td>
            <td>${i.ThoiGianNop}</td>
        </tr>`;
    });
}

load();
