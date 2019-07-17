import os
import ntpath
from time import sleep
from zipfile import ZipFile

import kaggle
import numpy.random as rng


def fetch_random_dataset(threshold=.5):
    MAX_PAGES = 1000  # holding value for the last page of datasets
    while True:
        random_page = rng.randint(1, MAX_PAGES)
        response = kaggle.api.dataset_list(page=random_page)
        if response:
            dataset = rng.choice(response)
            if dataset.usabilityRating > threshold:
                return dataset
            else:
                continue
        else:
            MAX_PAGES = random_page - 1
            sleep(.1)
            continue


def download_dataset(dataset):
    for attr in dir(dataset):
        if attr[:2] != "__":
            print("\t", attr, ":", getattr(dataset, attr))
    file_path = os.path.join(".", "data", dataset.title)
    kaggle.api.dataset_download_files(
        dataset.ref,
        path=file_path,
        force=True,
        unzip=False,
    )
    file_name = ntpath.basename(dataset.ref) + ".zip"
    zip_path = os.path.join(file_path, file_name)
    ZipFile(zip_path).extractall()


def main():
    dataset = fetch_random_dataset()
    download_dataset(dataset)


if __name__ == "__main__":
    main()
