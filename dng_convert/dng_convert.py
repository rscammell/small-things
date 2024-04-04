#!/usr/bin/env python3
# A simple tool for batch converting DNG image files to JPG/PNG/GIF formats.
# (C) Rupert Scammell <rupert.scammell@gmail.com>
# This software is licensed under the 3-clause BSD license specified at https://opensource.org/license/BSD-3-clause
# Version 1.1
# April, 2024

# Dependencies: pillow-heif module from PIP for HEIC file support
# TODO: Option to recursively scan source directory (currently top-level only)
# TODO: Option to retain EXIF information in output files
# TODO: Option to check for existence of output file and skip/overwrite.

import argparse
import os
from PIL import Image

def dng_convert(indir, outdir, filetype):
    
    # One could easily extend the list of supported filetypes to the larger set supported by pillow (i.e. https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html )
    if filetype not in ["jpg","png", "gif"]:
        print(f"Invalid filetype {filetype} specified. Setting to jpg.")
        filetype = "jpg"
    else:
        print(f"Target filetype for conversion is {filetype}")
        
    if not os.path.exists(outdir):
        print(f"{outdir} output directory does not exist. Creating directory.")
        os.makedirs(outdir)
    else:
        print(f"Output directory: {outdir}")
        
    # Get the list of .DNG files in the source directory by extension
    print("Scanning for DNG files...")
    dng_files = [f for f in os.listdir(args.indir) if (f.lower().endswith(".dng"))]
    
    if len(dng_files) == 0:
        print("No DNG files to convert.")
    else:    
        print(f"DNG files to convert: {dng_files}")

    # Loop through each .DNG file
    for dng_file in dng_files:
        try:
            # Open the .DNG file
            img = Image.open(os.path.join(args.indir, dng_file))

            # Convert the image to RGB mode
            img = img.convert("RGB")

            # Save the image in the desired format in the output directory
            outfile = os.path.splitext(dng_file)[0] + f".{filetype}"
            img.save(os.path.join(args.outdir, outfile))
            print(f"Converted {dng_file} to {outfile}")
        except:
            print(f"Unable to process {dng_file} .")
            import traceback
            traceback.print_exc()
            

    print ("Scanning for HEIC files...")
    heic_files = [f for f in os.listdir(args.indir) if (f.lower().endswith(".heic"))]

    if len(heic_files) == 0:
        print("No HEIC files to convert. Ending program.")
    else:    
        print(f"HEIC files to convert: {heic_files}")

    # Loop through each .HEIC file
    import pillow_heif
    pillow_heif.register_heif_opener()
    
    for heic_file in heic_files:
        try:
            # Read the HEIC file
            img = Image.open(os.path.join(args.indir, heic_file))

            # Save the image in the desired format in the output directory
            outfile = os.path.splitext(heic_file)[0] + f".{filetype}"
            img.save(os.path.join(args.outdir, outfile))
            print(f"Converted {heic_file} to {outfile}")
        except:
            print(f"Unable to process {heic_file} .")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert .DNG or .HEIC files to .jpg or .png or .gif files (.jpg is the default)")
    parser.add_argument("--indir", required=True, type=str, help="Source directory containing .DNG and/or .HEIC files")
    parser.add_argument("--outdir", required=True, type=str, help="Destination directory for output files")
    parser.add_argument("--filetype", required=False, type=str, default="jpg", help="Image output format (either jpg, png or gif). If invalid or unspecified, will default to jpg.")
    args = parser.parse_args()

    dng_convert(args.indir, args.outdir, args.filetype)
    
    
    
