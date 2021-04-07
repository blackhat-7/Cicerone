from torchvision import transforms
from functools import lru_cache
import torch
from torch.utils.data import DataLoader
from torch.utils.data import Dataset
from torch.utils.data.sampler import SubsetRandomSampler
import numpy as np
import os
import torchvision
import tarfile
import zipfile
import torch.nn as nn
from torchvision.datasets.utils import download_url
from torchvision.datasets import ImageFolder
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from torchvision import transforms
import warnings
import joblib
from PIL import Image
from torchvision.models import resnet18, resnet34, resnet152, inception_v3

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
batch_size = 128
image_size = (256, 256)
valid_size = 0.15
test_size = 0.0

class Cicerone_Inception():
    def __init__(self):
        self.model = torch.load('inception.model')
        self.classes = ['Ad Dimaniyat Islands',
                        'Al Alam Palace',
                        'Al Mirani Fort',
                        'Al Sawadi Beach',
                        'Arabian Oryx Sanctuary',
                        'Ayn Athum, Salalah',
                        'Ayn Razat',
                        'Bahla Fort',
                        'Bait Al Baranda Museum',
                        'Bait Al Zubair Museum',
                        'Bandar Al Khairan Viewpoint',
                        'Bimmah Sinkhole',
                        'Fazayah Beach',
                        'Fins Beach',
                        "Ghalya's Museum of Modern Art",
                        'Hawana Aqua Park',
                        'Jebel Shams',
                        'Jebel al Harim',
                        'Jibreen Castle',
                        'Khuriya Muriya Islands',
                        'Majlis al Jinn',
                        'Mughsail Beach',
                        'Musandam Oman',
                        'Musandam Peninsula',
                        'Muscat Beach',
                        'Muscat Gate Museum',
                        'Mutrah Corniche',
                        'Mutrah Fort',
                        'Mutrah Souq',
                        'Nakhal Fort, Oman',
                        'Nizwa Fort',
                        'Qurum Beach',
                        'Qurum Natural Park',
                        'Ras Al Jinz Turtle Reserve',
                        'Royal Opera House Muscat',
                        'Snake Gorge Canyon',
                        'Sultan Qaboos Grand Mosque',
                        'Telegraph Island',
                        'The Chedi Muscat',
                        'The Museum of the Frankincense Land',
                        'The National Museum of Oman',
                        'Wadi Ash Shab',
                        'Wadi Darbat',
                        'Wadi Dayqah Dam',
                        'Yitti Beach']

    def predict_image_path(self, image_path):
        from torchvision import transforms
        from PIL import Image
        import torch
        image_size=(299,299)
        tm = transforms.Compose([
            transforms.Resize(image_size),
            transforms.CenterCrop(image_size),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

        image = Image.open(image_path)

        image = tm(image)
        image = image.unsqueeze(0) 

        with torch.no_grad():
            out = self.model(image.cpu())
            index = out.numpy().argmax()
        return self.classes[index]

import joblib
def predict(image_path):
    loaded_model = joblib.load('cicerone_inception.model')
    return loaded_model.predict_image_path(image_path)