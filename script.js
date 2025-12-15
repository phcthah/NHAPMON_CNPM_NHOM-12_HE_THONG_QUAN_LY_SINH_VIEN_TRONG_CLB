document.getElementById('taskForm').addEventListener('submit', async function(event) {
    event.preventDefault(); // Ngăn chặn form submit truyền thống
    
    const statusPopup = document.getElementById('statusPopup');
    statusPopup.style.display = 'none'; // Ẩn popup cũ

    const taskData = {
        title: document.getElementById('title').value,
        description: document.getElementById('description').value,
        startDate: document.getElementById('startDate').value,
        startTime: document.getElementById('startTime').value,
        endDate: document.getElementById('endDate').value,
        endTime: document.getElementById('endTime').value,
        type: document.getElementById('type').value,
        assignee: document.getElementById('assignee').value,
        priority: document.getElementById('priority').value,
    };

    try {
        // Gọi API Backend (giả sử chạy trên http://localhost:3000)
        const response = await fetch('http://localhost:3000/api/tasks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(taskData),
        });

        if (response.ok) {
            // Popup thông báo khi tạo thành công
            statusPopup.textContent = '✅ Tạo lịch/nhiệm vụ thành công!';
            statusPopup.className = 'popup success';
            document.getElementById('taskForm').reset(); // Xóa form

            // TODO: Hiển thị lịch sau khi tạo (cập nhật list #taskList)
            // Cần gọi API GET để lấy lại danh sách mới hoặc thêm trực tiếp vào DOM.

        } else {
            // Popup thông báo khi tạo thất bại
            const errorData = await response.json();
            statusPopup.textContent = `❌ Lỗi: ${errorData.message || 'Không thể tạo nhiệm vụ.'}`;
            statusPopup.className = 'popup error';
        }
    } catch (error) {
        console.error('Lỗi kết nối:', error);
        statusPopup.textContent = '❌ Lỗi kết nối với máy chủ Backend.';
        statusPopup.className = 'popup error';
    }
    
    statusPopup.style.display = 'block'; // Hiển thị popup
});                                                        