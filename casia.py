import glob
import struct
import zipfile

from codecs import decode
from math import ceil
from os import listdir, makedirs, remove
from os.path import isdir, isfile
from time import clock
from urllib.request import urlretrieve

import numpy as np

from scipy.misc import toimage

from tqdm import tqdm

__author__ = 'Lucas Kjaero'

DATASETS = {
        "competition-gnt": "http://www.nlpr.ia.ac.cn/databases/Download/competition/competition-gnt.zip",
        "HWDB1.1trn_gnt_P1": "http://www.nlpr.ia.ac.cn/databases/Download/feature_data/HWDB1.1trn_gnt_P1.zip",
        "HWDB1.1trn_gnt_P2": "http://www.nlpr.ia.ac.cn/databases/Download/feature_data/HWDB1.1trn_gnt_P2.zip",
        "HWDB1.1tst_gnt": "http://www.nlpr.ia.ac.cn/databases/download/feature_data/HWDB1.1tst_gnt.zip"
}


class DLProgress(tqdm):
    """ Class to show progress on dataset download """
    # Progress bar code adapted from a Udacity machine learning project.
    last_block = 0

    def hook(self, block_num=1, block_size=1, total_size=None):
        self.total = total_size
        self.update((block_num - self.last_block) * block_size)
        self.last_block = block_num


class CASIA:
    """
    Class to read the dataset for all learning functions. Anything you need should be in here.
    Don't call other functions unless you're sure you need to.
    """
    def __init__(self):
        assert get_datasets() is True, "Datasets aren't properly loaded, " \
                                       "rerun to try again or download datasets manually."

    def load_all(self):
        """
        Generator to load all images in the dataset. Yields (image, character) pairs until all images have been loaded.
        :return: (Pillow.Image.Image, string) tuples
        """
        for dataset in DATASETS:
            for image, label in load_gnt_dir(dataset):
                yield image, label



"""
Below here is implementation functions for CASIA. None of these should need to be called by themselves.
"""

"""
Dataset Downloaders
"""


def get_datasets():
    """
    Make sure the datasets are present. If not, downloads and extracts them.
    Attempts the download five times because the file hosting is unreliable.
    :return:
    """
    success = True

    for dataset in DATASETS:
        # If the dataset is present, no need to download anything.
        if not isdir(dataset):

            # Try 5 times to download. The download page is unreliable, so we need a few tries.
            was_error = False
            for iteration in range(5):
                if iteration > 0 or was_error is True:
                    was_error = get_dataset(dataset)

            if was_error:
                print("\nThis recognizer is trained by the CASIA handwriting database.")
                print("If the download doesn't work, you can get the files at %s" % DATASETS[dataset])
                print("If you have download problems, "
                      "wget may be effective at downloading because of download resuming.")
                success = False

    return success


def get_dataset(dataset):
    """
    Checks to see if the dataset is present. If not, it downloads and unzips it.
    """
    was_error = False
    zip_path = dataset + ".zip"

    # Download zip files if they're not there
    if not isfile(zip_path):
        try:
            with DLProgress(unit='B', unit_scale=True, miniters=1, desc=dataset) as pbar:
                urlretrieve(DATASETS[dataset], zip_path, pbar.hook)
        except Exception as ex:
            print("Error downloading %s: %s" % (dataset, ex))
            was_error = True

    # Unzip the data files
    if not isdir(dataset):
        try:
            with zipfile.ZipFile(zip_path) as zip_archive:
                zip_archive.extractall(path=dataset)
                zip_archive.close()
        except Exception as ex:
            print("Error unzipping %s: %s" % (zip_path, ex))
            # Usually the error is caused by a bad zip file. Delete it so the program will try to download it again.
            remove(zip_path)
            was_error = True

    return was_error

"""
GNT FILE READERS
"""


def load_gnt_dir(dataset_path):
    """
    Load a directory of gnt files. Yields the image and label in tuples.
    :param dataset_path: The directory to search in.
    :return:  Yields (image, label) pairs
    """
    for path in glob.glob(dataset_path + "/*.gnt"):
        for image, label in load_gnt_file(path):
            yield image, label


def load_gnt_file(filename):
    """
    Load characters and images from a given GNT file.
    :param filename: The file path to load.
    :return: (image: np.array, character) tuples
    """
    print("Loading file: %s" % filename)

    # Thanks to nhatch for the code to read the GNT file, available at https://github.com/nhatch/casia
    with open(filename, "rb") as f:
        while True:
            packed_length = f.read(4)
            if packed_length == b'':
                break

            length = struct.unpack("<I", packed_length)[0]
            raw_label = struct.unpack(">cc", f.read(2))
            width = struct.unpack("<H", f.read(2))[0]
            height = struct.unpack("<H", f.read(2))[0]
            photo_bytes = struct.unpack("{}B".format(height * width), f.read(height * width))

            # Comes out as a tuple of chars. Need to be combined. Encoded as gb2312, gotta convert to unicode.
            label = decode(raw_label[0] + raw_label[1], encoding="gb2312")
            # Create an array of bytes for the image, match it to the proper dimensions, and turn it into a PIL image.
            image = toimage(np.array(photo_bytes).reshape(height, width))

            yield image, label
