import os
import sys
import torch
import argparse

# sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from engine.monocon_engine import MonoconEngine
from utils.engine_utils import tprint, move_data_device, load_cfg, generate_random_seed, set_random_seed
from utils.kitti_convert_utils import kitti_3d_to_file

from tqdm import tqdm

# Arguments
parser = argparse.ArgumentParser('MonoCon Inference for KITTI 3D Object Detection Dataset')
parser.add_argument('--config_file',
                    type=str,
                    help="Path of the config file (.yaml)")
parser.add_argument('--checkpoint_file',
                    type=str,
                    help="Path of the checkpoint file (.pth)")
parser.add_argument('--gpu_id', type=int, default=0, help="Index of GPU to use for inference")
parser.add_argument('--output_dir',
                    type=str,
                    help="Path of the directory to save the submission file")

args = parser.parse_args()

# Load Config
cfg = load_cfg(args.config_file)
cfg.GPU_ID = args.gpu_id

# Set Random Seed
seed = cfg.get('SEED', -1)
seed = generate_random_seed(seed)
set_random_seed(seed)

tprint(f"Using Random Seed {seed}")


# Initialize Engine
engine = MonoconEngine(cfg, auto_resume=False, is_test=True)
engine.load_checkpoint(args.checkpoint_file, verbose=True)


# Inference
tprint("Mode: Inference")
engine.model.eval()

# Ensure output directory exists
out_path = args.output_dir
if not os.path.exists(out_path):
    os.makedirs(out_path)

# Inference on the Test Set
for test_data in tqdm(engine.test_loader, desc="Running Inference..."):
    test_data = move_data_device(test_data, engine.current_device)
    inference_results = engine.model.batch_eval(test_data)
    
    # Use your utility function to convert inference results to KITTI format
    kitti_3d_to_file(inference_results, test_data['img_metas'], out_path, single_file=False)

tprint("Inference Completed. Results saved in:", out_path)