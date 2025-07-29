from unsloth import FastLanguageModel
from typing import Callable
from transformers.generation.streamers import TextStreamer
from unsloth.chat_templates import get_chat_template
import socketio
import time

from .constants import BIND

class CallbackStreamer(TextStreamer):
    def __init__(self, streamer: TextStreamer, callback: Callable[[str, bool], None]=None):
        super().__init__(streamer.tokenizer, skip_prompt=streamer.skip_prompt, **streamer.decode_kwargs)
        self.callback = callback
        self.full_result = []

    def on_finalized_text(self, text: str, stream_end: bool = False):
        """Prints the new text to stdout. If the stream is ending, also prints a newline."""
        self.full_result.append(text)
        if self.callback:
            self.callback(text, stream_end)
        else:
            print(text, flush=True, end="" if not stream_end else None)

    def get_full_result(self):
        return "".join(self.full_result)
    
class Llm:
    def __init__(self):
        max_seq_length = 2048 # Choose any! We auto support RoPE Scaling internally!
        dtype = None # None for auto detection. Float16 for Tesla T4, V100, Bfloat16 for Ampere+
        load_in_4bit = True # Use 4bit quantization to reduce memory usage. Can be False.

        model, tokenizer = FastLanguageModel.from_pretrained(
            model_name = "unsloth/mistral-7b-instruct-v0.3-bnb-4bit",
            max_seq_length = max_seq_length,
            dtype = dtype,
            load_in_4bit = load_in_4bit,
        )
        self.model = model
        self.tokenizer = get_chat_template(
            tokenizer,
            chat_template = "mistral", # Supports zephyr, chatml, mistral, llama, alpaca, vicuna, vicuna_old, unsloth
            mapping = {
                "role" : "from",
                "content" : "value",
                "user" : "human",
                "assistant" : "gpt"
            },
            # map_eos_token = True, # Maps <|im_end|> to </s> instead # doesn't work?
        )

        FastLanguageModel.for_inference(model) # Enable native 2x faster inference

    def Ask(self, message:str, on_response_chunk: Callable[[str, bool], None]):
        messages = [
            {"from": "human", "value": message},
        ]
        inputs = self.tokenizer.apply_chat_template(
            messages,
            tokenize = True,
            add_generation_prompt = True, # Must add for generation
            return_tensors = "pt",
        ).to("cuda")

        streamer = CallbackStreamer(
            streamer=TextStreamer(self.tokenizer, skip_prompt = False),
            callback=on_response_chunk,
        )
        outputs = self.model.generate(
            input_ids=inputs,
            max_new_tokens=128,
            use_cache=True,
            streamer = streamer,
            temperature=1.0,
        )

def NewAgent():
    # Create a Socket.IO client instance
    sio = socketio.Client()
    llm = Llm()

    # Define event handlers
    @sio.event
    def connect():
        print('Connected to server')

    @sio.event
    def disconnect():
        print('Disconnected from server')

    @sio.event
    def your_event_name(data):
        print('Received data:', data)

    # Connect to the server
    sio.connect(f'http://{BIND}')

    # Emit an event to the server
    sio.emit('client_event', {'message': 'Hello Server!'})
    
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        sio.disconnect()
 