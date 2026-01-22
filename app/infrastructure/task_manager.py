
from typing import Dict, Any, Optional
import uuid

class TaskManager:
    """
    Background tasklarning statusini kuzatish uchun oddiy in-memory menejer.
    Production uchun Redis/Celery ishlatish kerak, lekin MVP uchun shu yetadi.
    """
    _tasks: Dict[str, Dict[str, Any]] = {}

    def create_task(self) -> str:
        task_id = str(uuid.uuid4())
        self._tasks[task_id] = {
            "status": "pending",
            "progress": 0,
            "message": "Jarayon boshlanmoqda...",
            "result": None,
            "error": None
        }
        return task_id

    def update_task(self, task_id: str, status: str = None, progress: int = None, message: str = None, result: Any = None, error: str = None):
        if task_id in self._tasks:
            if status: self._tasks[task_id]["status"] = status
            if progress is not None: self._tasks[task_id]["progress"] = progress
            if message: self._tasks[task_id]["message"] = message
            if result: self._tasks[task_id]["result"] = result
            if error: 
                self._tasks[task_id]["error"] = error
                self._tasks[task_id]["status"] = "failed"

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        return self._tasks.get(task_id)

task_manager = TaskManager()
