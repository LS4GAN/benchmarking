# Benchmarking algorithms for the paper on UVCGAN

<img src="https://user-images.githubusercontent.com/22546248/156432368-41097ddc-357e-4776-8909-77bfd08157d6.jpg" width="800" alt="generator"/>

In this repo, we discuss how benchmarking results are produced for the paper on UVCGAN. 
- [UVCGAN: UNet Vision Transformer cycle-consistent GAN for unpaired image-to-image translation](https://arxiv.org/abs/2203.02557) 
- [UVCGAN GitHub repo](https://github.com/LS4GAN/uvcgan)

## Summary
We studied four benchmarking algorithms ACL-GAN, Council-GAN, CycleGAN, and U-GAT-IT. We made several minor modifications to the benchmarking algorithms
to make comparison easier. Here are links to the paper, the original repo, and the forked (modified) repo:
1. ACL-GAN:     [paper](https://arxiv.org/pdf/2003.04858.pdf), [GitHub repo](https://github.com/hyperplane-lab/ACL-GAN), [Modified GitHub repo](https://github.com/pphuangyi/ACL-GAN/tree/pphuangyi)
3. Council-GAN: [paper](https://openaccess.thecvf.com/content_CVPR_2020/papers/Nizan_Breaking_the_Cycle_-_Colleagues_Are_All_You_Need_CVPR_2020_paper.pdf), [GitHub repo](https://github.com/Onr/Council-GAN), [Modified GitHub repo](https://github.com/pphuangyi/Council-GAN/tree/pphuangyi)
4. CycleGAN:    [paper](https://arxiv.org/pdf/1703.10593.pdf), [GitHub repo](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix), [Modified GitHub repo](https://github.com/pphuangyi/pytorch-CycleGAN-and-pix2pix/tree/pphuangyi)
5. U-GAT-IT:    [paper](https://arxiv.org/pdf/1907.10830.pdf), [GitHub repo](https://github.com/znxlwm/UGATIT-pytorch), [Modified GitHub repo](https://github.com/pphuangyi/UGATIT-pytorch/tree/pphuangyi)
    
The detailed list of modifications to each repo can be found in the section of [List of modifications](#list-of-modifications).

## How benchmarking results are produced
We used pretrained models whenever they are provided by the authors. 
We train a model from scratch in the following two cases:
1. the algorithm wasn't tested on a dataset;
2. the algorithm was tested on a dataset but the authors didn't provide a pretrained model. 

In the first case, we used the default parameters whenever possible and made only necessary changes such dataset location and image resizing and cropping.
In the second case, we used the parameters provided by the paper. 

Here is the link to all [pre-trained models](https://zenodo.org/record/6329717#.YijFfHrMK3A) we trained from scratch. 
We only included the _generators_ which can be used to generator translationed images, but not the _discriminators_. 
The pretrained models that can be downloaded from the link are listed below.
The number in the parenthesis indicate the case. 
1. **ACL-GAN**: 
    > linux download: `wget wget https://zenodo.org/record/6329717/files/ACL-GAN_pretrained_models.zip` (total size: 596.5 MB)
    - selfie-to-anime(1)
    - anime-to-selfie(2, use selfie-to-anime parameters) 
    - male-to-female(1)
    - female-to-male(2, use male-to-female parameters)
    - remove glasses(1)
    - add glasses(2, use remove glasses parameters)
2. **Council-GAN**: (pretrained models for selfie-to-anime, male-to-female, and remove glasses are provided)
    > linux download: `wegt https://zenodo.org/record/6329717/files/Council-GAN_pretrained_models.zip` (total size: 776.3 MB)
    - anime-to-selfie(2, use selfie-to-anime parameters) 
    - female-to-male(2, use male-to-female parameters)
    - add glasses(2, use remove glasses parameters)
3. **CycleGAN**: CycleGAN wasn't tested on any of the datasets so we trained **all** of them from scratch.
    > linux download: `wget https://zenodo.org/record/6329717/files/CycleGAN_pretrained_models.zip` (total size: 253.8 MB)
5. **U-GAT-IT**: `TensorFlow` models for selfie-to-anime and anime-to-selfie are provided (see [U-GAT-IT](#u-gat-it) for mor detail)
    - male-to-female and female-to-male (2, use the default parameters)
      > linux download: `wget https://zenodo.org/record/6329717/files/U-GAT-IT_gender_params_1000000.zip` (for gender only, size: 1.7G)
    - remove and add glasses (2, use the default parameters)
      > linux download: `wget https://zenodo.org/record/6329717/files/U-GAT-IT_glasses_params_1000000.zip` (for glasses only, size: 1.7G)


### ACL-GAN
ACL-GAN worked on all three datasets, but it only studied translation in one direction (selfie to anime, male to female, removing glasses). It also only provided the configuration file for the male to female task and didn't provide any pretrained model. We generated the configuration files for the other two tasks (selfie to anime, removing glasses) using parameters provided in the paper. Since ACL-GAN is an asymmetric model, we have to train each direction individually. For translation in the opposite directions, we use exactly the same parameter except for `data_root` (dataset location) and `data_kind` (the name of the task). All configuration files can be found [here](https://github.com/LS4GAN/benchmarking/tree/main/ACL-GAN/configs).

**NOTE:** since ACL-GAN didn't implemented a switch to switch domain A and B, we have to manually generate datasets that with domain A and B switched. So in case you want to reproduce the results with the configuration files for anime to selfie, female to male, and adding glasses, please first generate the domain-reversed datasets for them.

### Council-GAN
Council-GAN is also an asymmetric model. It works with all the three datasets but also only in one direction (selfie to anime, male to female, removing glasses). Council-GAN provided configuration files and pretrained models for the three tasks. 

We construct the configuration files for B to A translation using the same parameters as those for A to B except for parameters `do_a2b` and `do_b2a`. We can set `do_a2b` to `False` and `do_b2a` to `True` so as to use same dataset without reversing the two domains as needed for ACL-GAN. 

For some reason, Council-GAN also trained for removing glasses with shrinked images. More precisely, Council-GAN first resizes an image so that the width=128 and then take a 128x128 random crop as input. We used the pretrained model for removing glasses, but had to do postprocessing to enlarge the image. For adding glasses, we decided to load image with width resized to 256 and then take a 256x256 random crop as input (`new_size: 256`, `crop_image_height: 256`, `crop_image_width: 256`). The configuration files for anime to selfie, female to male, and adding glasses can be found [here](https://github.com/LS4GAN/benchmarking/tree/main/Council-GAN/configs).

### CycleGAN
CycleGAN does not use configuration files. Please find the train and test commands and more detail about the algorithm [here](https://github.com/LS4GAN/benchmarking/blob/main/CycleGAN/commands.md)

### U-GAT-IT
U-GAT-IT hard coded a lot of parameters, and hence the train and test commands are extremely simple. 
U-GAT-IT provided pretrained model for the selfie2anime dataset but it was in TensorFlow. 
And the zip file provided is also corrupted. Luckikly, we can use `fastjar` to extract zip file with the following command : 
> `fastjar -v -v -v -x -f ~/Downloads/100_epoch_selfie2anime_checkpoint.zip` 
We provide train and test commands for the gender and glasses dataset [here](https://github.com/LS4GAN/benchmarking/blob/main/U-GAT-IT/commands.md).

U-GAT-IT's hard-coded image preprocessing didn't provide individual control to width and height. 
In the train phase, U-GAT-IT first resizes the image to have a size 286 x 286 (and hence mess up the aspect ratio for non-squared images) and takes a random crop of 256 x256. In the testing phase, it resizes the image to 256 x 256. U-GAT-IT also output more than just the translated images. 
In order to pick up only the translated image and restore its aspect ratio, we have to process the U-GAT-IT's test output using this [script](https://github.com/LS4GAN/benchmarking/blob/main/U-GAT-IT/process_ugatit.py). 
The script does the following:
- take the fifth image in the image stack (`image.crop(left=0, top=4 * 256, right=256, bottom=5 * 256`);
- resize back to ratio (`image.resize(256, 314)`);
- take the center crop (`image.crop(left=0, top=(314 - 256) / 2, right=256, bottom=(314 + 256) / 2)`).

## List of modifications 
> Modifications can be found in the modified GitHub repos in the [Summary](#summary) section.
1. **ACL-GAN**: 
    - Modified the `focus_translation` function in `test_batch.py`. There used to be a mismatch in tensor size;
    - Removed the restriction of testing only 3000 images;
    - (around line 160) Modified size of the tensor named `images` so that it matches with the tensor named `outputs_til`.
3. **Council-GAN**: Modified the test output to have the same file name as the input.
4. **CycleGAN**:
    - CycleGAN output random crops in the test phase. Since most other algorithms use center crop, I modified the code to output center crops in the test phase.
    - The training of CycleGAN is scheduled for running 200 epochs. By default, CycleGAN runs through the whole dataset in each epoch. This works well for relatively smaller selfie2anime dataset, but can take too long for the two CelebA datasets. Also, since all the other algorithms train on around 1M images and CycleGAN doesn't have the control to do so, I added the a parameter so that a fixed number of random samples could be loaded for each epoch. So if we load 5000 images per epoch and let CycleGAN run for 200 epoches, it also sees 1M images during training.
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
We calculate the scores using the [`torch-fidelity`](https://github.com/toshas/torch-fidelity/releases/tag/v0.3.0) package
<img src="https://user-images.githubusercontent.com/22546248/156433246-65ff3d24-6df9-4e17-bb9f-23736bbfc291.png" width="800" alt="fid-kid">

Find more details of how benchmarking results are generated here: [ACL-GAN](#acl-gan), [Council-GAN](#council-gan), [CycleGAN](#cyclegan), [U-GAT-IT](#u-gat-it).
Find what modifications we did to the benchmarking algorithms [here](#list-of-modifications).


## Sample test output comparison
<img src="https://user-images.githubusercontent.com/22546248/156432283-39390ec5-28a0-41d9-8674-b7d15a46e692.jpg" width="800" alt="sample images"/>

## Running time (in hours) comparison 
<table>
    <tr>
        <th></th><th>Selfie to Anime</th><th>Anime to Selfie</th><th>Male to Female</th><th>Female to Male</th><th>Remove Glasses</th><th>Add Glasses</th>
    </tr>
    <tr>
        <td><b>ACL-GAN</b></td><td>~45</td><td>~45</td><td>~45</td><td>~45</td><td>~42</td><td>~42</td>
    </tr>
    <tr>
        <td><b>Council-GAN</b></td><td>-</td><td>~450</td><td>-</td><td>~450</td><td>-</td><td>~450</td>
    </tr>
    <tr>
        <td><b>CycleGAN</b></td><td colspan="2">~36</td><td colspan="2">~36</td><td colspan="2">~40</td>
    </tr>
    <tr>
        <td><b>U-GAT-IT</b></td><td colspan="2">-</td><td colspan="2">~140</td><td colspan="2">~141</td>
    </tr>
    <tr>
        <td><b>UVCGAN</b></td><td colspan="2">(@Dmitrii)</td><td colspan="2">(@Dmitrii)</td><td colspan="2">(@Dmitrii)</td>
    </tr>
</table>

## More sample images, both good and bad
1. Selfie to Anime
<img src="https://user-images.githubusercontent.com/22546248/156852263-138caffd-4be5-4cfe-9751-04f336d4e336.png" alt="Selfie to Anime" width="800">
2. Anime to Selfie 
<img src="https://user-images.githubusercontent.com/22546248/156852411-45211cb6-3968-4b1d-b0c9-ee49b2fea13b.png" alt="Anime to Selfie" width="800">
3. Male to Female 
<img src="https://user-images.githubusercontent.com/22546248/156852477-bb07b336-b0db-49b1-98dd-22e8abd28d12.png" alt="Male to Female" width="800">
4. Female to Male 
<img src="https://user-images.githubusercontent.com/22546248/156852545-ccaa05fe-c3fa-4421-b579-7178c4697e03.png" alt="Female to Male" width="800">
5. Remove Glasses 
<img src="https://user-images.githubusercontent.com/22546248/156852590-f7a5f7ea-871e-4610-817b-d395b17cff5f.png" alt="Remove Glasses" width="800">
6. Add Glasses 
<img src="https://user-images.githubusercontent.com/22546248/156852642-addfdbf7-dc57-4813-a0ee-0906849add40.png" alt="Add Glasses" width="800">
