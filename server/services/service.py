from openai import OpenAI
from dotenv import load_dotenv
import requests
import os
import json

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
exchange_api = os.getenv('EXCHANGE_RATE_API_KEY')
client = OpenAI(api_key=api_key)

class Service:
    def __init__(self, prompt):
        self.prompt = prompt


    def convert(self, source_currency, target_currency):
        url = f'https://v6.exchangerate-api.com/v6/{exchange_api}/latest/{source_currency}'
        response = requests.get(url)
        conversion = response.json()['conversion_rates'].get(target_currency)
        return conversion


    def model_interaction(self):
        try:
            tools = [{
                'type': 'function',
                'function': {
                    'name': 'convert',
                    'description': 'Converts an amount from source currency to target currency',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'amount': {'type': 'number'},
                            'source_currency': {'type': 'string'},
                            'target_currency': {'type': 'string'}
                        },
                        'required': ['amount', 'source_currency', 'target_currency'],
                    }
                }
            }]

            input_messages = [{'role': 'user', 'content': self.prompt}]

            response = client.chat.completions.create(
                model='gpt-4.1-nano',
                messages=input_messages,
                tools=tools,
                tool_choice='auto'
            )

            tool_call = response.choices[0].message.tool_calls[0]
            args = json.loads(tool_call.function.arguments)

            rate = self.convert(args['source_currency'], args['target_currency'])
            amount = args['amount']
            total = round(amount * rate, 3)

            input_messages.append({'role': 'assistant', 'tool_calls': [tool_call]})
            input_messages.append({
                'role': 'tool',
                'tool_call_id': tool_call.id,
                'content': f"{amount} {args['source_currency']} = {total} {args['target_currency']}"
            })

            response_2 = client.chat.completions.create(
                model="gpt-4.1-nano",
                messages=input_messages,
            )

            return response_2.choices[0].message.content
        except Exception as e:
            print(f'Service exception: {e}')