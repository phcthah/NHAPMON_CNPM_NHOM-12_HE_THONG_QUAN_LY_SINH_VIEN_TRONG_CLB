document.getElementById("registerForm").addEventListener("submit", function(e) {
  e.preventDefault();

  const fullname = document.getElementById("fullname").value;
  const studentId = document.getElementById("studentId").value;
  const email = document.getElementById("email").value;
  const department = document.getElementById("department").value;

  if (!fullname || !studentId || !email || !department) {
    alert("Vui lòng nhập đầy đủ thông tin!");
    return;
  }

  alert("Đăng ký thành công! Vui lòng chờ CLB xét duyệt.");

  // Sau này gửi API backend tại đây
});