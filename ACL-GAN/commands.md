# YAML file naming convention:
- `[AtoB].yaml` includes `selfie2anime.yaml`, `male2female.yaml`, `rmvGlasses.yaml`
- `[BtoA].yaml` includes `anime2selfie.yaml`, `female2male.yaml`, `addGlasses.yaml`

## Train commands
- domain A to domain B: 
  > `python train.py --config configs/[AtoB].yaml`
- domain B to domain A:
  > `python train.py --config configs/[BtoA].yaml`

## Test commands:
- domain A to domain B: 
  > `python test_batch.py --config configs/[AtoB].yaml --input_folder [path_to_gender_dataset]/testA/ --checkpoint [path_to_pretrained_generator] --output_folder [path_to_output_images]`
- domain B to domain A: 
  > `python test_batch.py --config configs/[BtoA].yaml --input_folder [path_to_gender_dataset]/testB/ --checkpoint [path_to_pretrained_generator] --output_folder [path_to_output_images]`
