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
import shutil



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


def organize_classes(input_path, output_path, file_dict, ext='.png'):
    for file_stem, target in file_dict.items():
        print(file_stem)
        target = str(target)
        print(target)
        if not os.path.exists(os.path.join( output_path, target)):
            os.makedirs(os.path.join( output_path, target))
        shutil.copy( os.path.join( input_path, file_stem+ext ), os.path.join( output_path, target, file_stem+ext ) )
    return None


def organize_dataset(csv_path, input_path, output_path):
    labels = pd.read_csv(csv_path)
    file_dict = dict(zip(labels['patientId'].values, labels['Target'].values))
    organize_classes(input_path, output_path, file_dict)

