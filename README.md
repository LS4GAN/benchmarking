# Benchmarking algorithms for the paper on UVCGAN
<img src="https://user-images.githubusercontent.com/22546248/156432368-41097ddc-357e-4776-8909-77bfd08157d6.jpg" width="800" alt="generator"/>

In this repo, we discuss how benchmarking results are produced for the paper on UVCGAN ([GitHub repo](https://github.com/LS4GAN/uvcgan)).

## Summary
We studied four benchmarking algorithms ACL-GAN, Council-GAN, CycleGAN, and U-GAT-IT. We made several minor modifications to the benchmarking algorithms
to make comparison easier. Here are links to the paper, the original repo, and the forked (modified) repo:
1. ACL-GAN:     [paper](https://arxiv.org/pdf/2003.04858.pdf), [GitHub repo](https://github.com/hyperplane-lab/ACL-GAN), [Modified GitHub repo](https://github.com/pphuangyi/ACL-GAN)
3. Council-GAN: [paper](https://openaccess.thecvf.com/content_CVPR_2020/papers/Nizan_Breaking_the_Cycle_-_Colleagues_Are_All_You_Need_CVPR_2020_paper.pdf), [GitHub repo](https://github.com/Onr/Council-GAN), [Modified GitHub repo]
4. CycleGAN:    [paper](https://arxiv.org/pdf/1703.10593.pdf), [GitHub repo](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix), [Modified GitHub repo](https://github.com/pphuangyi/pytorch-CycleGAN-and-pix2pix)
5. U-GAT-IT:    [paper](https://arxiv.org/pdf/1907.10830.pdf), [GitHub repo](https://github.com/znxlwm/UGATIT-pytorch), [Modified GitHub repo](https://github.com/pphuangyi/UGATIT-pytorch)
    
The detailed list of modifications to each repo can be found in the section of [List of modifications](#list-of-modifications).

## How benchmarking results are produced
We used pretrained models whenever they are provided. 
In case an algorithm didn't work on a dataset or it did but didn't provide a pretrained model, we generated it. 
Here is the link to all [pre-trained models]
### ACL-GAN
ACL-GAN worked on all three datasets, but it only studied translation in one direction (selfie to anime, male to female, removing glasses). It also only provided the configuration file for the male to female task and didn't provide any pretrained model. We generated the configuration files for the other two tasks (selfie to anime, removing glasses) using parameters provided in the paper. Since ACL-GAN is an asymmetric model, we have to train each direction individually. For translation in the opposite directions, we use exactly the same parameter except for `data_root` (dataset location) and `data_kind` (the name of the task). All configuration files can be found [here](https://github.com/LS4GAN/benchmarking/tree/main/ACL-GAN/configs).

**NOTE:** since ACL-GAN didn't implemented a switch to switch domain A and B, we have to manually generate datasets that with domain A and B switched. So in case you want to reproduce the results with the configuration files for anime to selfie, female to male, and adding glasses, please first generate the domain-reversed datasets for them.

### Council-GAN
Council-GAN is also an asymmetric model. It works with all the three datasets but also only in one direction (selfie to anime, male to female, removing glasses). Council-GAN provided configuration files and pretrained models for the three tasks. 

We construct the configuration files for B to A translation using the same parameters as those for A to B except for parameters `do_a2b` and `do_b2a`. We have to set `do_a2b` to `False` and `do_b2a` to `True` so that we can use the same dataset as that for A to B translation without reversing the two domains as we did for ACL-GAN. 

For some reason, Council-GAN also trained for removing glasses with shrinked images. More precisely, Council-GAN first resizes an image so that the width=128 and then take a 128x128 random crop as input. We used the pretrained model for removing glasses, but had to do postprocessing to enlarge the image. For adding glasses, we decided to load image with width resized to 256 and then take a 256x256 random crop as input (`new_size: 256`, `crop_image_height: 256`, `crop_image_width: 256`). The configuration files for anime to selfie, female to male, and adding glasses can be found [here](https://github.com/LS4GAN/benchmarking/tree/main/Council-GAN/configs).

### CycleGAN
CycleGAN does not use configuration files. Please find the train and test command and their more detail about the algorithm [here](https://github.com/LS4GAN/benchmarking/blob/main/CycleGAN/commands.md)

### U-GAT-IT
U-GAT-IT hard coded a lot of parameters, and hence the train and test commands are extremely simple. U-GAT-IT provided pretrained model for the selfie2anime dataset but it was in TensorFlow. And the zip file is also corrupted. But, fastjar can extract it using the following command : 
> `fastjar -v -v -v -x -f ~/Downloads/100_epoch_selfie2anime_checkpoint.zip` 
We provide train and test commands for the gender and glasses dataset [here](https://github.com/LS4GAN/benchmarking/blob/main/U-GAT-IT/commands.md).

Since U-GAT-IT hard-coded the preprocessing part didn't provide individual control to width and height. 
In the train phase, U-GAT-IT first resizes the image to have a size 286 x 286 (and hence mess up the aspect ratio for non-squared images) and takes a random crop of 256 x256. In the testing phase, it resizes the image to 256 x 256. U-GAT-IT also output more than just the translated images. 
In order to pick up only the translated image and restore its aspect ratio, we have to process the U-GAT-IT's test output using this [script](https://github.com/LS4GAN/benchmarking/blob/main/U-GAT-IT/process_ugatit.py). 
The script does the following:
- take the fifth image in the image stack (`image.crop(left=0, top=4 * 256, right=256, bottom=5 * 256`);
- resize back to ratio (`image.resize(256, 314)`);
- take the center crop (`image.crop(left=0, top=(314 - 256) / 2, right=256, bottom=(314 + 256) / 2)`).

## List of modifications
1. **ACL-GAN**: 
    - Modified the `focus_translation` function in `test_batch.py`. There used to be mismatch in tensor size;
    - Removed the restriction of testing only 3000 images;
    - (around line 160) Modified size of the tensor named `images` so that it matches with the tensor named `outputs_til`.
3. **Council-GAN**: Modified the test output to have the same file name as the input.
4. **CycleGAN**:
    - CycleGAN output random crops in the test phase. Since most other algorithms use center crop, I modified the code to output center crops in the test phase.
    - The training of CycleGAN is scheduled for running 200 epochs. By default, CycleGAN runs through the whole dataset in each epoch. This works well for relatively smaller dataset, but can take too long for the two CelebA datasets. Also, since all the other algorithms train on around 1M images and CycleGAN doesn't have the control to do so, I added the a parameter so that a fixed number of random samples could be loaded for each epoch. So if we load 5000 images per epoch and let CycleGAN run for 200 epoches, it also sees 1M images during training.
    - Modified the test output to have the same file name as the input.
5. **U-GAT-IT**: Modified the test output to have the same file name as the input.

## Datasets
We compare the algorithms on three datasets:
1. **Sefie2Anime**: 
    - 256x256 images, domain A = selfie, domain B = anime,
    - `trainA`: 3400, `trainB`: 3400, `testA`: 100, `testB`: 100
    - more information of the dataset can be found [here](https://paperswithcode.com/dataset/selfie2anime) or from the U-GAT-IT paper. 

2. **CelebA-gender**:
    - 178x218 images, domain A = male, domain B = female,
    - `tarinA`: 68261, `trainB`: 94509, `testA`: 16173, `testB`: 23656
    - The dataset is derived from the [CelebA](https://mmlab.ie.cuhk.edu.hk/projects/CelebA.html) dataset
        by splitting according to the attribute `male`;

3. **CelebA-glasses**: 
    - 178x218 images, domain A = with glasses, domain B = without glasses,
    - `tarinA`: 10421, `trainB`: 152249, `testA`: 2672, `testB`: 37157
    - The dataset is derived from the [CelebA](https://mmlab.ie.cuhk.edu.hk/projects/CelebA.html) dataset
        by splitting according to the attribute `glasses`;

Both the gender and glasses datasets are downloaded with the code provided by the CouncilGAN [GitHub repo](https://github.com/Onr/Council-GAN). Note that the original CelebA images are compressed with the `jpg` format, and with the so-called `jpg` artifacts. However, the images downloaded from CouncilGAN have extension `png`. We suspect that the images were processed to improve quality.

## FID and KID scores comparison
To uniformize the comparison, for the two CelebA datasets which
contains non-square images, we resized the test output
to have width 256 and took center crop where the face of
a character is most likely located. To calculate the FID/KID scores,
we also resized the images in the test partition of gender and
glasses datasets and took the central crops.
We used the python [`PIL`](https://pillow.readthedocs.io/en/latest/index.html) package for processing images
and used `BILINEAR` as the `resample` method in the resize function.
<img src="https://user-images.githubusercontent.com/22546248/156433246-65ff3d24-6df9-4e17-bb9f-23736bbfc291.png" width="800" alt="fid-kid">


## Sample test output comparison
<img src="https://user-images.githubusercontent.com/22546248/156432283-39390ec5-28a0-41d9-8674-b7d15a46e692.jpg" width="800" alt="sample images"/>

## Model size comparison
## Running time comparison 
