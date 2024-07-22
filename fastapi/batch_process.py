from fastapi import FastAPI, Request
from typing import List
import asyncio
import torch

from model_template import CustomTorchModel, InputData, ModelPath
from fastapi.openapi.models import Response


app = FastAPI()


class BatchProcessor:
    def __init__(self, batch_size : int):
        self.batch_size = batch_size
        self.queue = list()
        self.lock = asyncio.Lock()


    async def process_batch(self):
        while 1:
            if len(self.queue) >= self.batch_size:
                batch = self.queue[:self.batch_size]
                self.queue = self.queue[self.batch_size:]

                results = self.ml_inference(batch) # include the ML inference logic

                for request, response in results:
                    request.response = response
            await asyncio.sleep(1)
    

    # TODO: Implement ML interfacing logic
    def ml_inference(self, batch: List[Request]):
        inputs = torch.tensor([data.json()['features'] for data in batch], dtype=torch.float32)
        with torch.no_grad():
            outputs = model(inputs).numpy()
        # return [(req, {"result": "dummy result"}) for req in batch]
        return [(req, {"result": output.tolist()}) for req, output in zip(batch, outputs)]


batch_processor = BatchProcessor(batch_size=10)

model = CustomTorchModel()
m_pth = input()
model.load_state_dict(torch.load(f'{m_pth}'))



@app.on_event("startup")
async def startup_event():
    asyncio.create_task(batch_processor.process_batch())


@app.post("/inference")
async def inference(data: InputData, request: Request) -> Response:
    async with batch_processor.lock:
        batch_processor.queue.append((request, data))
    # batch_processor.queue.append(request)
    return await request.response # this will keep request open till processing is over

