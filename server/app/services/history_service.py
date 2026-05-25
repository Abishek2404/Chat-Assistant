from collections import defaultdict


class HistoryService:
    def __init__(self, max_pairs: int = 5) -> None:
        self.max_messages = max_pairs * 2
        self._history: dict[str, list[dict[str, str]]] = defaultdict(list)

    def get_formatted_history(self, session_id: str) -> str:
        messages = self._history.get(session_id, [])
        return "\n".join(f"{item['role']}: {item['content']}" for item in messages)

    def add_pair(self, session_id: str, user_message: str, assistant_reply: str) -> None:
        self._history[session_id].append({"role": "User", "content": user_message})
        self._history[session_id].append(
            {"role": "Assistant", "content": assistant_reply}
        )
        self._history[session_id] = self._history[session_id][-self.max_messages :]


history_service = HistoryService()
