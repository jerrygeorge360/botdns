import io
import os
from groq import Groq
from dotenv import load_dotenv
from abc import ABC, abstractmethod
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
groq_key = os.getenv("GROQ_KEY")


class LLMBase(ABC):
    @abstractmethod
    def __init__(self): ...

    @abstractmethod
    def generate_response(self, content: str) -> str | None: ...


class LLMClient(LLMBase):
    def __init__(self):
        self._client = None
        self._config = {'instruction': '', 'model': None}

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, value):
        self._client = value

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        self._config = value

    def generate_response(self, content: str) -> str | None:
        try:
            chat_completion = self._client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": f"{self.config['instruction']}\n\n{content}"
                    }
                ],
                model=self._config['model']
            )
            result = chat_completion.choices[0].message.content
            logger.info("Model response (%s): %s", self._config['model'], result)
            return result
        except Exception as e:
            logger.error("Error in LLM response generation: %s", str(e))
            return None

    @staticmethod
    def write_to_memory(data: str) -> io.StringIO:
        buffer = io.StringIO(data)
        buffer.seek(0)
        return buffer




def generate_summary(data: str, instruction: str) -> io.StringIO | None:
    try:
        client = Groq(api_key=groq_key)
        model = 'llama-3.3-70b-versatile'

        llm = LLMClient()
        llm.client = client
        llm.config = {
            "model": model,
            "instruction": instruction
        }

        result = llm.generate_response(data)
        if not result:
            logger.error("LLM failed to generate summary.")
            return None

        return llm.write_to_memory(result)

    except Exception as e:
        logger.error("Single-stage AI summary failed: %s", str(e))
        return None
