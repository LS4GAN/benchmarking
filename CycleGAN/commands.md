## Train commands
Notes:
1. Here we set `display_id` to be 0 so as to not display intermediate training result.
2. It seems that CycleGAN can use more than one GPU, we can use more than to gpu_ids, e.g. `--gpu_ids 1 2`
3. CycleGAN is symmetric which means we can get both translators in one training.
4. For benchmarking purpose, we try to let the train process to see ~1M images.
Since CycleGAN uses batch size 1, training on 1M images means runs for 1M iterations.
The selfie2anime datasets is small, and hence we can train on the entire dataset in each epoch.
However, for the two large CelebA datasets, if we run through the entire dataset in each epoch
and use the formula 1M / ((trainA + trainB) / 2) to estimate the total epochs needed,
we will end up running only approximately 13 epochs.
Since CycleGAN is scheduled by default to run 200 epochs,
I modified the source code so that it load 5000 randomly sampled images in epoch.

- selfie2anime: `python train.py --dataroot [path_to_selfie2anime_dataset] --name selfie2anime --gpu_ids [gpu_ids] --display_id 0`
- gender: `python train.py --dataroot [path_to_gender] --name gender --gpu_ids [gpu_id] --display_id 0 --max_dataset_size 5000 --shuffle --load_size 256 --preprocess scale_width_and_crop`
- glasses: `python train.py --dataroot [path_to_glasses] --name glasses --gpu_ids [gpu_id] --display_id 0 --max_dataset_size 5000 --shuffle --load_size 256 --preprocess scale_width_and_crop`

## Test commands
selfie to anime: python test.py --dataroot /data/datasets/cyclegan_benchmarking/datasets/selfie2anime/testA --name selfie2anime_pretrained_[bs] --gpu_ids 0 --results_dir results --model test --no_dropout
anime to selfie: python test.py --dataroot /data/datasets/cyclegan_benchmarking/datasets/selfie2anime/testB --name anime2selfie_pretrained_[bs] --gpu_ids 0 --results_dir results --model test --no_dropout
