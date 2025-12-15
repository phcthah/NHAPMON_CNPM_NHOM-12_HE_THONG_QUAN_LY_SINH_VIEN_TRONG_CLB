import json
from datetime import datetime
from typing import List


class CommunicationService:
    def __init__(self, storage_path="notifications.json"):
        self.storage_path = storage_path

    def _load_notifications(self):
        """Load notifications from JSON file"""
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []  # Chưa có file thì tạo list rỗng

    def _save_notifications(self, notifications):
        """Save notifications to JSON file"""
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(notifications, f, ensure_ascii=False, indent=4)

    def send_notification(self, recipient: str, title: str, message: str):
        """
        Gửi thông báo tới một người.
        """
        notification = {
            "recipient": recipient,
            "title": title,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }

        notifications = self._load_notifications()
        notifications.append(notification)
        self._save_notifications(notifications)

        print(f"📨 Đã gửi thông báo đến {recipient}")

    def send_group_notification(self, recipients: List[str], title: str, message: str):
        """
        Gửi thông báo tới nhiều người.
        """
        for recipient in recipients:
            self.send_notification(recipient, title, message)

        print(f"📢 Đã gửi thông báo đến {len(recipients)} người.")

    def get_all_notifications(self):
        """
        Lấy toàn bộ thông báo đã lưu.
        """
        return self._load_notifications()
