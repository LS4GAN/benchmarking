## Train
### Notes:
1. We use `display_id 0` to disable display of intermediate training result.
2. It seems that CycleGAN can use more than one GPU, we can use more than to gpu_ids, e.g. `--gpu_ids 1 2`
3. CycleGAN is symmetric which means we can get both translators in one training.
4. For benchmarking purpose, we try to let the train process to see ~1M images.
Since CycleGAN uses batch size 1, training on 1M images means running for 1M iterations.
The selfie2anime datasets is small, and hence we can train on the entire dataset in each epoch.
However, for the two large CelebA datasets, if we run through the entire dataset in each epoch
and use the formula `1M / ((trainA + trainB) / 2)` to estimate the total epochs needed,
we will end up running only approximately 13 epochs.
Since CycleGAN is scheduled by default to run 200 epochs,
I modified the source code so that it load 5000 randomly sampled images in epoch (`--max_dataset_size 5000 --shuffle`).

### Commands
- selfie2anime: 
  > `python train.py --gpu_ids [gpu_ids] --display_id 0 --dataroot [path_to_selfie2anime] --name selfie2anime`
- gender: 
  > `python train.py --gpu_ids [gpu_ids] --display_id 0 --load_size 256 --preprocess scale_width_and_crop --max_dataset_size 5000 --shuffle  --dataroot [path_to_gender] --name gender`
- glasses: 
  > `python train.py --gpu_ids [gpu_ids] --display_id 0 --load_size 256 --preprocess scale_width_and_crop --max_dataset_size 5000 --shuffle  --dataroot [path_to_glasses] --name glasses`

### Separate the generators for test
CycleGAN is symmetric and we can get both generators from domain A to B and B to A in one training. The latest A-to-B generator is saved to `checkpoints/[name]/latest_net_G_A.pth` and the latest B-to-A generator is saved to `checkpoints/[name]/latest_net_G_B.pth`. Here `[name]` is the parameter `--name` in the train command.
In order to run test, we need to save the generators to separate folders. 
- `checkpoints/selfie2anime/latest_net_G_A.pth` -> `checkpoints/selfie2anime/latest_net_G.pth`
- `checkpoints/selfie2anime/latest_net_G_B.pth` -> `checkpoints/anime2selfie/latest_net_G.pth`
- `checkpoints/gender/latest_net_G_A.pth` -> `checkpoints/male2female/latest_net_G.pth`
- `checkpoints/gender/latest_net_G_B.pth` -> `checkpoints/female2male/latest_net_G.pth`
- `checkpoints/glasses/latest_net_G_A.pth` -> `checkpoints/rmvGlasses/latest_net_G.pth`
- `checkpoints/glasses/latest_net_G_B.pth` -> `checkpoints/addGlasses/latest_net_G.pth`

## Test commands
The `--name` parameter is the subfolder name under `checkpoints`
- selfie to anime: 
  > `python test.py --gpu_ids [gpu_ids] --results_dir results --model test --no_dropout --dataroot [path_to_selfie2anime]/testA --name selfie2anime
- anime to selfie: 
  > `python test.py --gpu_ids [gpu_ids] --results_dir results --model test --no_dropout --dataroot [path_to_selfie2anime]/testB --name anime2selfie

- male to female: 
  > `python test.py --gpu_ids [gpu_ids] --results_dir results --model test --no_dropout --load_size 256 --preprocess scale_width_and_crop --dataroot [path_to_gender]/testA --name male2female`
- female to male: 
  > `python test.py --gpu_ids [gpu_ids] --results_dir results --model test --no_dropout --load_size 256 --preprocess scale_width_and_crop --dataroot [path_to_gender]/testB --name female2male`
 
- remove glasses: 
  > `python test.py --gpu_ids [gpu_ids] --results_dir results --model test --no_dropout --load_size 256 --preprocess scale_width_and_crop --dataroot [path_to_glasses]/testA --name rmvGlasses`
- add glasses: 
  > `python test.py --gpu_ids [gpu_ids] --results_dir results --model test --no_dropout --load_size 256 --preprocess scale_width_and_crop --dataroot [path_to_glasses]/testB --name addGlasses`
