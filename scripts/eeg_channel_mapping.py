# ==============================================================================
# Copyright (c) 2026 Ankit Sengupta. All rights reserved.
# 
# This source code is licensed under the Research & Non-Commercial Attribution 
# License (RNCA) found in the LICENSE file in the root directory of this project.
# 
# If you use, evaluate, or substantially derive from this code in an academic 
# publication, you MUST provide appropriate citation to the original author 
# and repository. See CITATION.cff for citation details.
# ==============================================================================

"""
ZuCo 2.0 EEG Channel Mapping Script

This script generates the exact channel mapping used for the extracted ZuCo 2.0 dataset.
The original dataset was recorded using a 128-channel Geodesic Sensor Net (EGI).
During standard preprocessing, 23 artifact-heavy channels (face, neck, EOG) were removed, 
leaving 105 channels.

Removed Channels (1-indexed based on EGI 128 standard):
- EOG (Eye) Channels: 8, 14, 21, 25
- Face/Neck Boundary Channels: 43, 48, 49, 56, 63, 68, 73, 81, 88, 94, 99, 107, 113, 119, 120, 125, 126, 127, 128

This script generates a list of the 105 remaining channels in the exact order they appear 
in your extracted `.h5` files.
"""

import json
import os

def generate_zuco_mapping():
    # Total channels in the original cap
    total_original_channels = 128
    
    # The 23 channels removed during preprocessing (1-indexed)
    removed_channels = {
        8, 14, 21, 25, 43, 48, 49, 56, 63, 68, 73, 81, 88, 94, 99, 107, 
        113, 119, 120, 125, 126, 127, 128
    }

    mapping = []
    current_index = 0
    
    # Iterate through original 1-128 electrodes
    for original_electrode in range(1, total_original_channels + 1):
        if original_electrode not in removed_channels:
            # We assign standard EGI names like "E1", "E2"
            electrode_name = f"E{original_electrode}"
            
            # Map standard 10-20 system names to key electrodes (Standard EGI mapping)
            if original_electrode == 11:
                electrode_name = "Fz (E11)"
            elif original_electrode == 36:
                electrode_name = "C3 (E36)"
            elif original_electrode == 104:
                electrode_name = "C4 (E104)"
            elif original_electrode == 62:
                electrode_name = "Pz (E62)"
            elif original_electrode == 75:
                electrode_name = "Oz (E75)"
            
            mapping.append({
                "matrix_index": current_index,
                "electrode_name": electrode_name,
                "original_egi_number": original_electrode
            })
            current_index += 1

    return mapping

def save_mapping():
    mapping = generate_zuco_mapping()
    
    # Make sure we got exactly 105 channels
    assert len(mapping) == 105, f"Expected 105 channels, but got {len(mapping)}!"
    
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(output_dir, "zuco_channel_mapping.json")
    
    with open(output_file, 'w') as f:
        json.dump(mapping, f, indent=4)
        
    print(f"Successfully generated mapping for {len(mapping)} channels.")
    print(f"Saved to: {output_file}")
    
    print("\n--- Example Mapping ---")
    print("Matrix Index 0 maps to:", mapping[0]['electrode_name'])
    print("Matrix Index 50 maps to:", mapping[50]['electrode_name'])
    print("Matrix Index 104 maps to:", mapping[104]['electrode_name'])
    
    print("\nHow to use this in PyTorch:")
    print("eeg_matrix = f['eeg'][:] # Shape: (105, 500)")
    print("fz_channel_data = eeg_matrix[9, :] # Matrix Index 9 is Fz (E11)")

if __name__ == "__main__":
    save_mapping()
