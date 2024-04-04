# dng_convert

A simple command line tool for batch converting DNG and HEIC image files to JPG/PNG/GIF formats, compatible with Windows, Linux, and likely macOS.
I wrote this script to simplify the processing of RAW (DNG) and HEIC format files commonly produced by iOS, but it should work for any files of this type.

Usage is simple:
```python dng_convert.py --indir <directory containing DNG and/or HEIC files> --outdir <desired output directory> --filetype <optional; accepts 'jpg', 'gif', or 'png' (no quotes). Will default to 'jpg' if not specified>```

The tool requires [pillow-heif](https://pypi.org/project/pillow-heif/) for HEIC support.

dng_convert is offered under the 3-clause BSD license included in [LICENSE.md](LICENSE.md)

Contributions from the community welcomed!