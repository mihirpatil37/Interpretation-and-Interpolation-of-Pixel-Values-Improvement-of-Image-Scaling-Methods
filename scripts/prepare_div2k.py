"""Create bicubic low-resolution versions of DIV2K high-resolution images.

Example:
    python scripts/prepare_div2k.py --hr-dir data/DIV2K/DIV2K_valid_HR
        --out-dir data/DIV2K/DIV2K_valid_LR_bicubic --scales 2 4
"""

import argparse
from pathlib import Path

from PIL import Image

from srlab.degrade import bicubic_downscale


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create bicubic LR images from HR images."
    )
    parser.add_argument(
        "--hr-dir", type=Path, required=True, help="Folder with HR .png images"
    )
    parser.add_argument(
        "--out-dir", type=Path, required=True, help="Folder to write LR images to"
    )
    parser.add_argument(
        "--scales", type=int, nargs="+", default=[2, 4], help="Scale factors, e.g. 2 4"
    )
    parser.add_argument(
        "--overwrite", action="store_true", help="Recreate files that already exist"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    hr_paths = sorted(args.hr_dir.glob("*.png"))
    if not hr_paths:
        raise SystemExit(f"No .png images found in {args.hr_dir}")
    print(f"Found {len(hr_paths)} HR images in {args.hr_dir}")

    for scale in args.scales:
        scale_dir = args.out_dir / f"X{scale}"
        scale_dir.mkdir(parents=True, exist_ok=True)

        created, skipped = 0, 0
        for i, hr_path in enumerate(hr_paths, start=1):
            lr_path = scale_dir / f"{hr_path.stem}x{scale}.png"
            if lr_path.exists() and not args.overwrite:
                skipped += 1
                continue

            with Image.open(hr_path) as hr_img:
                hr = hr_img.convert("RGB")
                lr_img = bicubic_downscale(hr, scale)
                lr_img.save(lr_path)
                created += 1

            if i % 100 == 0 or i == len(hr_paths):
                print(f"  x{scale}: {i}/{len(hr_paths)}")

        print(f"x{scale}: created {created}, skipped {skipped} -> {scale_dir}")


if __name__ == "__main__":
    main()
