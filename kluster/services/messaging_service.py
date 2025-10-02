from typing import List
from dataclasses import dataclass
from sqlalchemy import and_, or_
from kluster.models import db, Message, MessageThread
import structlog

log = structlog.get_logger()

@dataclass
class Conversation:
    thread_id: int
    other_user_id: int
    last_message_at: str

class MessagingService:
    @staticmethod
    def _normalize_pair(a: int, b: int) -> tuple[int, int]:
        return (a, b) if a < b else (b, a)

    @staticmethod
    def get_or_create_thread(user_a: int, user_b: int) -> MessageThread:
        a, b = MessagingService._normalize_pair(user_a, user_b)
        thr = MessageThread.query.filter_by(user_a_id=a, user_b_id=b).first()
        if thr:
            return thr
        thr = MessageThread(user_a_id=a, user_b_id=b)
        db.session.add(thr)
        db.session.commit()
        log.info("thread_created", user_a=a, user_b=b, thread_id=thr.id)
        return thr

    @staticmethod
    def send(sender_id: int, receiver_id: int, body: str) -> Message:
        thr = MessagingService.get_or_create_thread(sender_id, receiver_id)
        msg = Message(thread_id=thr.id, sender_id=sender_id, body=body)
        db.session.add(msg)
        db.session.commit()
        log.info("message_sent", thread_id=thr.id, sender_id=sender_id)
        return msg

    @staticmethod
    def thread_messages(thread_id: int) -> List[Message]:
        return Message.query.filter_by(thread_id=thread_id).order_by(Message.created_at.asc()).all()

    @staticmethod
    def list_user_threads(user_id: int) -> List[MessageThread]:
        return MessageThread.query.filter(
            or_(MessageThread.user_a_id == user_id, MessageThread.user_b_id == user_id)
        ).order_by(MessageThread.created_at.desc()).all()
