from services.motor_ia.motor_ia_service import MotorIAService

class GerarTextoLivreService:
    def execute(self, prompt, modo="resumo"):
        return MotorIAService().execute(modo, prompt)
