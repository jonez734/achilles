import cv2
from pyzbar import pyzbar
import numpy as np
import argparse
from pathlib import Path


def decode_barcode(image, filename=""):
    barcodes = pyzbar.decode(image)
    found = False
    for barcode in barcodes:
        barcode_data = barcode.data.decode("utf-8")
        barcode_type = barcode.type
        print(f"[{filename}] Found {barcode_type} barcode: {barcode_data}")

        (x, y, w, h) = barcode.rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(
            image,
            barcode_data,
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2,
        )
        found = True
    if not found:
        print(f"[{filename}] No barcode detected.")
    return found


def deskew_and_crop(image, resize_dims=None):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 200)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) == 0:
        return image

    largest_contour = max(contours, key=cv2.contourArea)
    rect = cv2.minAreaRect(largest_contour)
    angle = rect[-1]

    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    deskewed = cv2.warpAffine(
        image, matrix, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE
    )

    box = cv2.boxPoints(rect)
    box = np.int0(box)
    ones = np.ones((box.shape[0], 1))
    points = np.hstack([box, ones])
    rotated_points = matrix.dot(points.T).T

    x, y, w, h = cv2.boundingRect(rotated_points.astype(np.int32))
    cropped = deskewed[y : y + h, x : x + w]

    if resize_dims:
        cropped = cv2.resize(cropped, resize_dims, interpolation=cv2.INTER_AREA)

    return cropped


def process_folder(
    input_dir, output_dir, resize_dims=None, save_images=False, preview=False
):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for img_file in input_dir.glob("*.[jp][pn]g"):
        print(f"Processing {img_file.name}...")
        image = cv2.imread(str(img_file))
        cropped = deskew_and_crop(image, resize_dims)

        if save_images is True:
            output_path = output_dir / f"{img_file.stem}_cropped.jpg"
            cv2.imwrite(str(output_path), cropped)
            print(f"Saved cropped image: {output_path}")
        else:
            print(f"Skipped saving for {img_file.name}")

        decode_barcode(cropped, img_file.name)

        if preview:
            cv2.imshow("Preview", cropped)
            key = cv2.waitKey(0)
            if key == ord("q"):
                print("Quitting preview mode.")
                break

    if preview:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch barcode deskew, resize, decode")
    parser.add_argument(
        "--input", required=True, help="Input directory containing images"
    )
    parser.add_argument(
        "--output", required=True, help="Output directory for cropped images"
    )
    parser.add_argument(
        "--resize",
        nargs=2,
        type=int,
        metavar=("WIDTH", "HEIGHT"),
        help="Resize cropped images to (width height)",
    )
    parser.add_argument(
        "--save", action="store_true", help="Save cropped images to output directory"
    )
    parser.add_argument(
        "--preview", action="store_true", help="Show cropped images in a preview window"
    )

    args = parser.parse_args()
    resize_dims = tuple(args.resize) if args.resize else None

    process_folder(
        args.input,
        args.output,
        resize_dims=resize_dims,
        save_images=args.save,
        preview=args.preview,
    )
