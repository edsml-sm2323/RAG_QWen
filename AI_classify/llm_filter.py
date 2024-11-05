import openai
from openai import OpenAIError
import torch
import os
from transformers import AutoModelForSequenceClassification, AutoTokenizer

class LLM_filter:
    def __init__(self, model_path, local, device=None):
        self.model = None
        self.tokenizer = None
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.local = local
        self.model_path = model_path

    def load_model_tokenizer(self, model=None, key=None):
        try:
            if self.local:
                if not os.path.exists(self.model_path):
                    raise FileNotFoundError(f"Model path '{self.model_path}' not found.")
                self.model = AutoModelForSequenceClassification.from_pretrained(self.model_path).to(self.device)
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
                print(f"Model and tokenizer loaded successfully from '{self.model_path}' on device '{self.device}'.")
            else:
                if not key:
                    raise ValueError("API key is required for remote model.")
                openai.api_key = key
                self.model_name = model
                print(f"API model ({self.model_name}) will be used.")
        except Exception as e:
            print(f"Error loading model/tokenizer: {e}")
            raise

    def model_predict(self, text):
        if self.local:
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512).to(self.device)
            outputs = self.model(**inputs)
            predictions = outputs.logits.argmax(dim=-1).item()
            return predictions == 1
        else:
            # 将 text 参数填入 AIfilter_Prompt 中
            AIfilter_Prompt = f"""
                            You are an Artificial Intelligence (AI) patent classifier. For each provided text consisting of a patent title and abstract, determine whether the text is related to AI.
                            Here are some examples of texts and responses:

                            Text: Tilt latch mechanism for hung windows a dual function lock a tilt latch assembly and tilt latch for use on a hung or double hung window are provided the lock includes a base a handle and a tilt latch actuating mechanism the tilt latch assembly includes a lock left and right latches and an extensible member the tilt latch actuating mechanism is adapted to receive the extensible member and has a null zone between locked and unlocked positions of the handle in the null zone no substantial movement of the extensible member as the handle is rotated from the locked to unlocked positions the tilt latch actuating mechanism causes the extensible member to move in a direction toward the lock as the handle is rotated from the unlocked position to a tilt position.
                            Response: False

                            Text: Motor control apparatus with magnetic flux controller and machine learning apparatus and method therefor a machine learning apparatus that learns a condition associated with a gain of a magnetic flux controller and a time constant of a magnetic flux estimator in a motor control apparatus includes a state observation unit that observes a state variable defined by at least one of data relating to an acceleration of a motor data relating to a jerk of the motor and data relating to an acceleration time of the motor and a learning unit that learns the condition associated with the gain of the magnetic flux controller and the time constant of the magnetic flux estimator in accordance with a training data set defined by the state variable. 
                            Response: True

                            Text: Bipolar forceps a bipolar forceps may include a first forceps arm having a first forceps arm aperture a first forceps jaw and a first forceps arm conductor tip a second forceps arm having a second forceps arm aperture a second forceps jaw and a second forceps arm conductor tip and an input conductor isolation mechanism having a first forceps arm housing and a second forceps arm housing the first forceps arm may be disposed in the first forceps arm housing and the second forceps arm may be disposed in the second forceps arm housing an application of a force to a lateral portion of the forceps arms may be configured to close the forceps jaws a reduction of a force applied to a lateral portion of the forceps arms may be configured to open the forceps jaws.
                            Response: False

                            Text: Unique part identifiers a method of providing a unique identifier for a manufactured part includes defining a boundary area on at least one surface of the manufactured part recording surface properties within a portion of the boundary area interpreting the recorded surface properties with a pattern recognition algorithm to create the unique identifier and storing the unique identifier in a database.
                            Response: True

                            Based on these examples, answer whether the following text is related to AI technology.
                            Text: "{text}"

                            Please respond with only "True" or "False" without any additional explanation or labels.
                        """

            try:
                response = openai.ChatCompletion.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": AIfilter_Prompt}],
                    temperature=0.0
                )
                result = response['choices'][0]['message']['content'].strip()
                return result == "True"
            except OpenAIError as e:
                print(f"Error in API call: {e}")
                return False
