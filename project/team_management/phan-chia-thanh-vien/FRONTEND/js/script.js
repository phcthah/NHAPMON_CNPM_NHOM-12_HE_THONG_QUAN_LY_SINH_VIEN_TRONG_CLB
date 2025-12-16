// Lấy dữ liệu từ API và hiển thị
async function loadData() {
  const banSelect = document.getElementById('ban');
  const memberList = document.getElementById('member-list');

  // Ví dụ gọi API
  const bans = await fetch('/api/bans').then(res => res.json());
  bans.forEach(b => {
    const option = document.createElement('option');
    option.value = b.id;
    option.textContent = b.tenBan;
    banSelect.appendChild(option);
  });

  const members = await fetch('/api/members').then(res => res.json());
  members.forEach(m => {
    const li = document.createElement('li');
    li.innerHTML = `<input type="checkbox" value="${m.id}"> ${m.name}`;
    memberList.appendChild(li);
  });
}

document.getElementById('save-btn').addEventListener('click', () => {
  const selectedBan = document.getElementById('ban').value;
  const selectedMembers = Array.from(document.querySelectorAll('#member-list input:checked'))
                               .map(cb => cb.value);
  // Gửi dữ liệu lên backend
  fetch('/api/assign', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({banId: selectedBan, members: selectedMembers})
  }).then(res => res.json())
    .then(data => alert(data.message));
});

loadData();

