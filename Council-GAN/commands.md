## Train
Council-GAN provided pretrained model for selfie to anime, male to female, and removing glasses. So we only train for the opposite directions using the configuration files in the configs folder.

## Test
Note: The command provided by the repo is wrong. Replace `--output_folder` with `--output_path` for the output to be saved properly.

### Test commands for the 3 tasks with pretrained model provided by Council-GAN
- selfie to anime: 
  > `python test_on_folder.py --config pretrain/anime/256/anime2face_council_folder.yaml --output_path [path_to_test_output] --checkpoint pretrain/anime/256/01000000 --input_folder [path_to_selfie2anime]/testA [--num_style 1]`
- male to female: 
  > `python test_on_folder.py --config pretrain/m2f/256/male2female_council_folder.yaml --output_path [path_to_test_output] --checkpoint pretrain/m2f/256/01000000 --input_folder [path_to_gender]/testA [--num_style 1]`
- remove glasses: 
  > `python test_on_folder.py --config pretrain/glasses_removal/128/galsses_council_folder.yaml --output_path [path_to_test_output] --checkpoint pretrain/glasses_removal/128/01000000 --input_folder [path_to_glasses]/testA [--num_style 1]`

### Test commands for the 3 tasks with pretrained models we trained
