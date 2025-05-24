import google.generativeai as genai
from typing import Optional
from dotenv import load_dotenv

class GeminiClient:
    def __init__(self, api_key: str):
        """
        Inicializa el cliente de Gemini

        Args:
            api_key (str): Tu API key de Google AI Studio
        """
        load_dotenv()

        genai.configure(api_key=api_key)
        # Configuramos el modelo predeterminado (Gemini Pro)
        self.model = genai.GenerativeModel('gemini-pro')

    def get_response(self,
                     prompt: str,
                     temperature: float = 0.7,
                     max_output_tokens: int = 1000) -> Optional[str]:
        """
        Envía una consulta a Gemini y obtiene la respuesta

        Args:
            prompt (str): El mensaje o pregunta para Gemini
            temperature (float): Controla la creatividad (0-1)
            max_output_tokens (int): Máximo número de tokens en la respuesta

        Returns:
            str: La respuesta de Gemini
        """
        try:
            # Configurar los parámetros de generación
            generation_config = {
                'temperature': temperature,
                'max_output_tokens': max_output_tokens,
            }

            # Generar la respuesta
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )

            return response.text

        except Exception as e:
            print(f"Error al hacer la consulta: {str(e)}")
            return None

    async def get_response_stream(self, prompt: str) -> Optional[str]:
        """
        Versión asíncrona que devuelve la respuesta en streaming

        Args:
            prompt (str): El mensaje o pregunta para Gemini

        Returns:
            str: La respuesta de Gemini
        """
        try:
            response = await self.model.generate_content(
                prompt,
                stream=True
            )

            full_response = ""
            async for chunk in response:
                if chunk.text:
                    print(chunk.text, end="", flush=True)
                    full_response += chunk.text

            return full_response

        except Exception as e:
            print(f"Error al hacer la consulta: {str(e)}")
            return None