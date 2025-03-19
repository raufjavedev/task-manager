class Task:
    def __init__(self, id, user_id, title, description, status, due_date, created_at):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.status = status
        self.due_date = due_date
        self.created_at = created_at

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "due_date": self.due_date,
            "created_at": self.created_at
        }
