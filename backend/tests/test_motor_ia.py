import os
import sys
import types
import unittest
from unittest.mock import patch

from services.motor_ia.motor_ia_service import ErroMotorIA, MotorIAService


class FakeClient:
    prompt = None
    model = None
    response = 'Texto gerado pelo Gemini'
    error = None

    def __init__(self, **kwargs):
        assert kwargs['api_key'] == 'CHAVE_APENAS_TESTE'

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    @property
    def models(self):
        return self

    def generate_content(self, model, contents):
        FakeClient.model, FakeClient.prompt = model, contents
        if FakeClient.error:
            raise FakeClient.error
        return types.SimpleNamespace(text=FakeClient.response)


class TestMotorIA(unittest.TestCase):
    def setUp(self):
        self.env = patch.dict(os.environ, {'GEMINI_API_KEY': 'CHAVE_APENAS_TESTE',
                                          'GEMINI_MODEL': 'gemini-2.5-flash'})
        self.env.start()
        self.genai = types.ModuleType('google.genai')
        self.genai.Client = FakeClient
        self.google = types.ModuleType('google')
        self.google.genai = self.genai
        self.modules = patch.dict(sys.modules, {'google': self.google, 'google.genai': self.genai})
        self.modules.start()
        FakeClient.response = 'Texto gerado pelo Gemini'
        FakeClient.error = None

    def tearDown(self):
        self.modules.stop()
        self.env.stop()

    def test_resumo(self):
        texto = MotorIAService().execute('resumo', 'Equações do primeiro grau')
        self.assertEqual(texto, 'Texto gerado pelo Gemini')
        self.assertIn('resumo', FakeClient.prompt.lower())
        self.assertIn('Equações do primeiro grau', FakeClient.prompt)
        self.assertEqual(FakeClient.model, 'gemini-2.5-flash')

    def test_quiz(self):
        MotorIAService().execute('atividades', 'Fotossíntese')
        self.assertIn('5 perguntas', FakeClient.prompt)
        self.assertIn('GABARITO', FakeClient.prompt)

    def test_explica(self):
        MotorIAService().execute('explicar', 'SQL')
        self.assertIn('didática', FakeClient.prompt)

    def test_sem_chave(self):
        os.environ.pop('GEMINI_API_KEY')
        with self.assertRaisesRegex(ErroMotorIA, 'GEMINI_API_KEY'):
            MotorIAService().execute('resumo', 'Texto')

    def test_validacoes(self):
        with self.assertRaises(ValueError):
            MotorIAService().execute('invalido', 'Texto')
        with self.assertRaises(ValueError):
            MotorIAService().execute('resumo', '   ')
        with self.assertRaises(ValueError):
            MotorIAService().execute('resumo', 'A' * 30001)

    def test_limite(self):
        FakeClient.error = RuntimeError('429 resource exhausted')
        with self.assertRaisesRegex(ErroMotorIA, 'Limite'):
            MotorIAService().execute('resumo', 'Texto')

    def test_nao_vaza_chave(self):
        FakeClient.error = RuntimeError('falhou CHAVE_APENAS_TESTE')
        with self.assertRaises(ErroMotorIA) as info:
            MotorIAService().execute('resumo', 'Texto')
        self.assertNotIn('CHAVE_APENAS_TESTE', str(info.exception))

    def test_resposta_vazia(self):
        FakeClient.response = ''
        with self.assertRaisesRegex(ErroMotorIA, 'não retornou texto'):
            MotorIAService().execute('resumo', 'Texto')


if __name__ == '__main__':
    unittest.main()
