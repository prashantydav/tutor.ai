

import PyPDF2
from datasets import load_dataset
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec
from pinecone import ServerlessSpec

import os
import time
import torch
from tqdm.auto import tqdm
from sentence_transformers import SentenceTransformer
from apiKey import *
import requests
import json
