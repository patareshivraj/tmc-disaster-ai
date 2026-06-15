from .models import AIPredictionLog, ChatbotLog

class AuditTrailEngine:
    @staticmethod
    def get_prediction_audit(prediction_id):
        try:
            log = AIPredictionLog.objects.get(prediction_id=prediction_id)
            return {
                "prediction_id": str(log.prediction_id),
                "timestamp": log.timestamp.isoformat(),
                "module": log.module_name,
                "input": log.input_payload,
                "output": log.output_payload,
                "confidence": log.confidence_score,
                "status": log.status,
                "error": log.error_message
            }
        except AIPredictionLog.DoesNotExist:
            return None

    @staticmethod
    def get_chatbot_audit(log_id):
        try:
            log = ChatbotLog.objects.get(log_id=log_id)
            return {
                "log_id": str(log.log_id),
                "timestamp": log.timestamp.isoformat(),
                "question": log.question,
                "intent": log.intent,
                "answer": log.answer,
                "modules_used": log.modules_used,
                "confidence": log.confidence,
                "status": log.status
            }
        except ChatbotLog.DoesNotExist:
            return None
