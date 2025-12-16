let departments = [];

document.getElementById("departmentForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const tenBan = document.getElementById("tenBan").value.trim();
  const moTa = document.getElementById("moTa").value;
  const loai = document.getElementById("loai").value;
  const message = document.getElementById("message");

  if (tenBan === "") {
    message.style.color = "red";
    message.innerText = "❌ Tên Ban/Tiểu ban không được để trống";
    return;
  }

  const isExist = departments.some(d => d.tenBan === tenBan);
  if (isExist) {
    message.style.color = "red";
    message.innerText = "❌ Ban/Tiểu ban đã tồn tại";
    return;
  }

  departments.push({ tenBan, moTa, loai });
  message.style.color = "green";
  message.innerText = "✅ Thêm thành công";

  renderTable();
  resetForm();
});

function renderTable() {
  const table = document.getElementById("departmentTable");
  table.innerHTML = "";

  departments.forEach((item, index) => {
    table.innerHTML += `
      <tr>
        <td>${index + 1}</td>
        <td>${item.tenBan}</td>
        <td>${item.moTa || "-"}</td>
        <td>${item.loai}</td>
      </tr>
    `;
  });
}

function resetForm() {
  document.getElementById("departmentForm").reset();
}
