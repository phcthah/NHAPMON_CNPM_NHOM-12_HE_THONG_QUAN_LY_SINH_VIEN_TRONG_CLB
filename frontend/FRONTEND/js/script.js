document.getElementById("banForm").addEventListener("submit", function (e) {
    e.preventDefault();

    const tenBan = document.getElementById("tenBan").value;
    const moTa = document.getElementById("moTa").value;

    const data = {
        ten_ban: tenBan,
        mo_ta: moTa
    };

    console.log("Dữ liệu gửi đi:", data);

    // Ví dụ gọi API backend (mở sau)
    /*
    fetch("http://localhost:3000/api/ban", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(result => alert("Tạo thành công"))
    .catch(err => console.error(err));
    */
});
