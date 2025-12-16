const form = document.getElementById("registerForm");
const popup = document.getElementById("popup");
const popupMessage = document.getElementById("popupMessage");

function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function isValidMSSV(mssv) {
    return /^[0-9]{7,10}$/.test(mssv);
}

form.addEventListener("submit", function (e) {
    e.preventDefault();

    let isValid = true;
    document.querySelectorAll(".error").forEach(e => e.textContent = "");

    const hoten = document.getElementById("hoten").value.trim();
    const mssv = document.getElementById("mssv").value.trim();
    const email = document.getElementById("email").value.trim();

    if (!isValidMSSV(mssv)) {
        document.querySelector("#mssv + .error").textContent = "MSSV không hợp lệ";
        isValid = false;
    }

    if (!isValidEmail(email)) {
        document.querySelector("#email + .error").textContent = "Email không đúng định dạng";
        isValid = false;
    }

    if (!isValid) return;

    const data = {
        hoten,
        mssv,
        email,
        sdt: document.getElementById("sdt").value,
        khoa: document.getElementById("khoa").value,
        nganh: document.getElementById("nganh").value,
        khoaHoc: document.getElementById("khoaHoc").value,
        gioiTinh: document.getElementById("gioiTinh").value
    };

    fetch("http://localhost:3000/member/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(result => {
        if (result.success) {
            showPopup("Đăng ký thành công – vui lòng chờ duyệt");
            form.reset();
        } else {
            showPopup(result.message || "Đăng ký thất bại");
        }
    })
    .catch(() => {
        showPopup("Không thể kết nối server");
    });
});

function showPopup(message) {
    popupMessage.textContent = message;
    popup.classList.remove("hidden");
}

function closePopup() {
    popup.classList.add("hidden");
}
