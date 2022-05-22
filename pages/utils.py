import numpy as np 
import pandas as pd 
from PIL import Image
import streamlit as st

def arr2PIL(arr):
    arr = (arr+1)/2*255
    arr = arr.astype('uint8')
    img = Image.fromarray(arr)
    return img



#if __name__ == '__main__':
   
