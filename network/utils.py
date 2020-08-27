import os
import pydicom
import pandas as pd
import matplotlib.pyplot as plt
from shutil import copyfile
import pydicom
import numpy as np
import base64
import io
import traceback
import sys
from PIL import Image


def dicom_to_png(input_path, output_path):
    dcms = os.listdir(input_path)
    for dcm in dcms:
        full_path = os.path.join(input_path, dcm)
        try:
            dcm_file = pydicom.dcmread(full_path)
            output = os.path.join(output_path, dcm.rstrip('.dcm')+'.png')
            arr = dcm_file.pixel_array
            if 0x20500020 in dcm_file and dcm_file[0x20500020].value == 'INVERSE':
                arr = arr.max() - arr
            elif 0x00280004 in dcm_file and dcm_file[0x00280004].value == 'MONOCHROME1':
                arr = arr.max() - arr
            plt.imsave(output, arr, cmap='gray')
        except:
            print("Dicom file corrupted")
    return None


