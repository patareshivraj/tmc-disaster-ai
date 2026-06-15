from .models import AIPredictionLog, ChatbotLog

class LoggingService:
    @staticmethod
    def log_prediction(module_name, request_source, input_payload, output_payload, confidence, response_time, status, error_message, endpoint, user='system'):
        return AIPredictionLog.objects.create(
            module_name=module_name,
            request_source=request_source,
            input_payload=input_payload,
            output_payload=output_payload,
            confidence_score=confidence,
            response_time_ms=response_time,
            status=status,
            error_message=error_message,
            api_endpoint=endpoint,
            user_identifier=user
        )
        
    @staticmethod
    def log_chatbot(question, intent, modules_used, answer, confidence, response_time, status):
        return ChatbotLog.objects.create(
            question=question,
            intent=intent,
            modules_used=modules_used,
            answer=answer,
            confidence=confidence,
            response_time_ms=response_time,
            status=status
        )
