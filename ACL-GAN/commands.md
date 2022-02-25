male to female (batch_size=3): CUDA_VISIBLE_DEVICES=0 python test_batch.py --config configs/male2female.yaml --input_folder /data/datasets/cyclegan_benchmarking/datasets/celeba_male2female/testA/ --checkpoint outputs/male2female/checkpoints/gen_00350000.pt --output_folder results/male2female/atob/

female to male (batch_size=3): CUDA_VISIBLE_DEVICES=0 python test_batch.py --config configs/female2male.yaml --input_folder /data/datasets/cyclegan_benchmarking/datasets/celeba_male2female/testB/ --checkpoint outputs/female2male/checkpoints/gen_00350000.pt --output_folder results/female2female
