# Benchmarking algorithms for the paper on UVCGAN
In this repo, we discuss how benchmarking results are produced for the paper on UVCGAN ([GitHub repo](https://github.com/LS4GAN/uvcgan)).

## Summary
We studied four benchmarking algorithms
1. ACL-GAN:     [paper](https://arxiv.org/pdf/2003.04858.pdf), [GitHub repo](https://github.com/hyperplane-lab/ACL-GAN)
3. Council-GAN: [paper](https://openaccess.thecvf.com/content_CVPR_2020/papers/Nizan_Breaking_the_Cycle_-_Colleagues_Are_All_You_Need_CVPR_2020_paper.pdf), [GitHub repo](https://github.com/Onr/Council-GAN)
4. CycleGAN:    [paper](https://arxiv.org/pdf/1703.10593.pdf), [GitHub repo](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix)
5. U-GAT-IT:    [paper](https://arxiv.org/pdf/1907.10830.pdf), [GitHub repo](https://github.com/znxlwm/UGATIT-pytorch)

We made several minor modifications to the benchmarking algorithms
to uniformize the comparison. Here are links to the forked repo:
1. ACL-GAN:     [Modified GitHub repo](https://github.com/pphuangyi/ACL-GAN)
2. Council-GAN: [Modified GitHub repo]
3. CycleGAN:    [Modified GitHub repo](https://github.com/pphuangyi/pytorch-CycleGAN-and-pix2pix)
4. U-GAT-IT:    [Modified GitHub repo](https://github.com/pphuangyi/UGATIT-pytorch)

The detailed list of modifications to each repo can be found
in the section of [List of modifications].

## Pretrained models:
We used pretrained models whenever they are provided. 
In case an algorithm did work on a dataset or it did but didn't provide a pretrained model, we generated the pretrained model. 
Here is the link to the [pre-trained models]
### ACL-GAN
ACL-GAN worked on all three datasets, but it only studied translation in one direction (selfie to anime, male to female, removing glasses). It also only provided the configuration file for the male to female task and didn't provide any pretrained model. We generated the configuration files for the other two tasks (selfie to anime, removing glasses) using parameters provided in the paper. Since ACL-GAN is an asymmetric model, we have to train each direction individually. For translation in the opposite directions, we use exactly the same parameter except for `data_root` (dataset location) and `data_kind` (the name of the task). All configuration files can be found [here](https://github.com/LS4GAN/benchmarking/tree/main/ACL-GAN/configs).

**NOTE:** since ACL-GAN didn't implemented a switch to switch domain A and B, we have to manually generate datasets that with domain A and B switched. So in case you want to reproduce the results with the configuration files for anime to selfie, female to male, and adding glasses, please first generate the domain-reversed datasets for them.

### Council-GAN
Council-GAN is also an asymmetric model. It works with all the three datasets but also only in one direction (selfie to anime, male to female, removing glasses). Council-GAN provided configuration files and pretrained models for the three tasks. 

We construct the configuration files for B to A translation using the same parameters as those for A to B except for parameters `do_a2b` and `do_b2a`. We have to set `do_a2b` to `False` and `do_b2a` to `True` so that we can use the same dataset as that for A to B translation without reversing the two domains as we did for ACL-GAN. 

For some reason, Council-GAN also trained for removing glasses with shrinked images. More precisely, Council-GAN first resizes an image so that the width=128 and then take a 128x128 random crop as input. We used the pretrained model for removing glasses, but had to do postprocessing to enlarge the image. For adding glasses, we decided to load image with width resized to 256 and then take a 256x256 random crop as input (`new_size: 256`, `crop_image_height: 256`, `crop_image_width: 256`). The configuration files for anime to selfie, female to male, and adding glasses can be found [here](https://github.com/LS4GAN/benchmarking/tree/main/Council-GAN/configs).

### CycleGAN
CycleGAN does not use configuration files. Please find the train and test command [here](https://github.com/LS4GAN/benchmarking/blob/main/CycleGAN/commands.md)

### U-GAT-IT

## Test outputs
Links to raw and processed [test output]:

## List of modifications
1. ACL-GAN:
2. Council-GAN:
3. CycleGAN:
4. U-GAT-IT:

## Datasets
We compare the algorithms on three datasets:
1. Sefie2Anime: [anime dataset link]
    - 256x256 images, domain A = selfie, domain B = anime,
    - `trainA`: 3400, `trainB`: 3400, `testA`: 100, `testB`: 100
    - more information of the dataset can be find:

2. CelebA-gender: [gender dataset link]
    - 178x218 images, domain A = male, domain B = female,
    - `tarinA`: 68261, `trainB`: 94509, `testA`: 16173, `testB`: 23656
    - The dataset is derived from the [CelebA](https://mmlab.ie.cuhk.edu.hk/projects/CelebA.html) dataset
        by splitting according to the attribute `male`;

3. CelebA-glasses: [glasses dataset link]
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
The code for processing the images can be found here

## Sample test output comparison

## Model size comparison
## Running time comparison 
