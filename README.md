# Benchmarking algorithms for the paper on UVCGAN
## Summary
We studied four benchmarking algorithms
1. ACL-GAN:     [acl-paper], [acl-raw-repo]
2. Council-GAN: [cou-paper], [cou-raw-repo]
3. CycleGAN:    [cyc-paper], [cyc-raw-repo]
4. U-GAT-IT:    [uga-paper], [uga-raw-repo]

We made several minor modifications to the benchmarking algorithms
to uniformize the comparison. Here are links to the forked repo:
1. ACL-GAN:     [acl modified repo]
2. Council-GAN: [cou modified repo]
3. CycleGAN:    [cyc modified repo]
4. U-GAT-IT:    [uga modified repo]
The detailed list of modifications to each repo can be found
in the section of [List of modifications].

- Links to [pre-trained models]:
- Links to raw and processed [test output]:

Please find configuration files and/or train/test command in folders for each algorithm.

## List of modifications
1. ACL-GAN:
    -
2. Council-GAN:
    -
3. CycleGAN:
    -
4. U-GAT-IT:

## Datasets
We compare the algorithms on three datasets:
1. Sefie2Anime: [anime dataset link]
    - 256x256 images, field A = selfie, field B = anime,
    - trainA: 3400, trainB: 3400, testA: 100, testB: 100
    - more information of the dataset can be find:

2. CelebA-gender: [gender dataset link]
    - 178x218 images, field A = male, field B = female,
    - tarinA:, trainB:, testA:, testB:
    - more information

3. CelebA-glasses: [glasses dataset link]
    - 178x218 images, field A = with glasses, field B = without glasses,
    - tarinA:, trainB:, testA:, testB:
    - more information

To uniformize the comparison, for the two CelebA datasets which
contains non-square images, we resized the test output
to have width 256 and took center crop where the face of
a character is most likely located. To calculate the FID/KID scores,
we also resized the images in the test partition of gender and
glasses datasets and took the central crops.
We used the python [`PIL`] package for processing images
and used `BILINEAR` as the `resample` method in the resize function.
The code for processing the images can be found here

# FID and KID scores comparison
# Sample test output comparison

[acl-paper]:
[acl-raw-repo]:
[cou-paper]:
[cou-raw-repo]:
[cyc-paper]:
[cyc-raw-repo]:
[uga-paper]:
[uga-raw-repo]:
[acl modified repo]:
[cou modified repo]:
[cyc modified repo]:
[uga modified repo]:
[test output]:
[pre-trained models]:
[`PIL`]:
