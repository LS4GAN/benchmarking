#!/usr/bin/env python
"""
Process U-GAT-IT output
"""
import os
import argparse
import shutil
from pathlib import Path

from concurrent.futures import ProcessPoolExecutor
from functools import partial
from tqdm import tqdm

from PIL import Image

IMG_EXTENSIONS = [
    '.jpg', '.JPG', '.jpeg',
    '.JPEG', '.png', '.PNG',
    '.ppm', '.PPM', '.bmp', '.BMP'
]

def is_image_file(filename):
    """
    Test whether a filename has an image extension.
    """
    return any(filename.endswith(extension) for extension in IMG_EXTENSIONS)


def parse_fname(path):
    """
    Get the name stem and extension.
    Note: If a file has two dots,
    the extension is everything after the first dot.
    """
    name = Path(path).name
    tokens = name.split('.')
    stem = tokens[0]
    extensions = '.'.join(tokens[1:])
    return stem, extensions


def get_image_paths(image_folder):
    """
    Get full paths to all image files in a folder.
    """
    image_paths = []
    for root, _, fnames in sorted(os.walk(image_folder)):
        for fname in fnames:
            if is_image_file(fname):
                path = os.path.join(root, fname)
                image_paths.append(path)
    return image_paths


def process(image_path, output_folder, resize_resample):
    """
    The output of U-GAT-IT is very specific.
    It has seven images stack vertically.
    Each image is 256 x 256.
    The translated image is the fifth one.
    After we get the wanted crop, we have to scale it
    back to ratio (width : height = 178 : 218).
    The final output is the center crop of the
    ratio-corrected image.
    """
    image = Image.open(image_path).convert('RGB')
    left, top, right, bottom = 0, 4 * 256, 256, 5 * 256
    image = image.crop((left, top, right, bottom))

    height = 314
    if resize_resample == 'bilinear':
        image = image.resize((256, height), resample=Image.BILINEAR)
    else:
        image = image.resize((256, height), resample=Image.BICUBIC)
    top = (height - 256) // 2
    image = image.crop((0, top, 256, top + 256))

    stem, ext = parse_fname(image_path)
    save_fname = f'{stem}.{ext}'
    image.save(Path(output_folder)/save_fname)


def process_folder(image_folder, output_folder, max_workers, resize_resample):
    """
    Process image files use multiprocessors.
    """
    image_paths = get_image_paths(image_folder)
    func = partial(
        process,
        output_folder   = output_folder,
        resize_resample = resize_resample
    )

    progbar = tqdm(total=len(image_paths))
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        for _ in executor.map(func, image_paths):
            progbar.update()

def main():
    """
    main
    """
    parser = argparse.ArgumentParser('How do you want to process your image?')
    parser.add_argument(
        'data_root',
        type = str,
        help = 'The path to the U-GAT-IT test output.'
    )
    parser.add_argument(
        '--resize_resample',
        type    = str,
        choices = {'bilinear', 'bicubic'},
        default = 'bilinear',
        help    = 'Resample method for image resize (default=bilinear).'
    )
    parser.add_argument(
        '--max_workers',
        type    = int,
        default = 8,
        help    = 'Number of concurrent works to process a folder of image (default = 8).'
    )
    args = parser.parse_args()
    data_root       = args.data_root
    resize_resample = args.resize_resample
    max_workers     = args.max_workers


    assert data_root.exists(), 'data root does not exist.'
    input_folder = data_root/'test'

    output_folder = data_root/'test_processed'
    if output_folder.exists():
        shutil.rmtree(output_folder)

    output_folder.mkdir(parents=True)
    for subfolder in ['A2B', 'B2A']:
        input_subfolder  = input_folder/subfolder
        output_subfolder = output_folder/subfolder
        output_subfolder.mkdir()
        process_folder(input_subfolder, output_subfolder, max_workers, resize_resample)


if __name__ == '__main__':
    main()
