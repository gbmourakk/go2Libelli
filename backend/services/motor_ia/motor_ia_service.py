class MotorIAService:
    def execute(self, modo, base):
        base = (base or "").strip()
        if not base:
            raise ValueError("Nada para gerar: envie um tema ou conteúdo.")

        if modo == "resumo":
            return (
                f'Resumo de "{base}": '
                "(texto de demonstração — integração com IA externa ainda não configurada)."
            )

        if modo == "atividades":
            return (
                f'3 atividades sobre "{base}":\n'
                "1. Explique o conceito principal.\n"
                "2. Resolva um exemplo prático.\n"
                "3. Compare o conceito com outro tema relacionado.\n"
                "(texto de demonstração — integração com IA externa ainda não configurada)."
            )

        if modo == "explicar":
            return (
                f'Explicação sobre "{base}": '
                "(texto de demonstração — integração com IA externa ainda não configurada)."
            )

        raise ValueError("Modo inválido. Use 'resumo', 'atividades' ou 'explicar'.")
