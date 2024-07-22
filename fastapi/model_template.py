from typing import List, Dict
import torch
import asyncio

from pydantic import BaseModel

class InputData(BaseModel):
    features: List[float]


class ModelPath(BaseModel):
    model_path: str

    def get_path():
        return input("Provide file path: ")


class CustomTorchModel(torch.nn.Module):
    def __init__(self):
        super(CustomTorchModel, self).__init__()
        self.fc = torch.nn.Linear(10, 1)
        self.attributes = list()
        self.modl_pth = ModelPath() | str
        self.pth = self.modl_pth.get_path()
    

    @classmethod
    def forward(self, x):
        '''Customize behavior of forward function based
        on the details of model and how it interfaces with FastAPI
        for inference.'''
        return self.fc(x)
    

    def display_metrics(self):
        print(f"CustomTorchModel({self.attributes})")
