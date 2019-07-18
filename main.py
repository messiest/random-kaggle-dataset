import os
import ntpath
from time import sleep
from itertools import count
from zipfile import ZipFile
from itertools import count

import kaggle
import numpy.random as rng


def fetch_random_dataset(threshold=.75):
    print("Fetching random Kaggle Dataset...")
    MAX_PAGES = 1000  # holding value for the last page of datasets
    for i in count(start=1, step=1):
        random_page = rng.randint(1, MAX_PAGES)
        response = kaggle.api.dataset_list(
            page=random_page,
            file_type='csv',
        )
        if response:
            dataset = rng.choice(response)
            if dataset.usabilityRating > threshold:
                return dataset
            else:
                continue
        else:
            MAX_PAGES = random_page - 1  # restrict range of rng on failure
            sleep(.1)
            continue


def download_dataset(dataset, data_dir='./data'):
    file_path = os.path.join(data_dir, dataset.ref.split('/')[1])
    meta = kaggle.api.dataset_metadata(dataset.ref, path=file_path)
    kaggle.api.dataset_download_files(
        dataset.ref,
        path=file_path,
        force=True,
        unzip=False,
    )
    file_name = ntpath.basename(dataset.ref) + ".zip"
    zip_file = os.path.join(file_path, file_name)
    ZipFile(zip_file).extractall(path=file_path)

    os.remove(zip_file)  # clean up

    for attr in dir(dataset):  # print the attributes for debugging purposes
        if attr[:2] != "__":
            print("\t", attr, ":", getattr(dataset, attr))


def main():
    dataset = fetch_random_dataset()
    download_dataset(dataset)


if __name__ == "__main__":
    main()
