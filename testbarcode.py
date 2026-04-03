import cv2
from pyzbar import pyzbar


def decode_upc(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use pyzbar to decode the UPC
    barcodes = pyzbar.decode(gray)

    # Iterate over the detected barcodes
    for barcode in barcodes:
        # Extract the UPC data and barcode type
        upc_data = barcode.data.decode("utf-8")
        barcode_type = barcode.type

        # Print the results
        print("UPC: {}".format(upc_data))
        print("Barcode Type: {}".format(barcode_type))


# Provide the path to your flattened UPC image
image_path = "./pringles-upc.png"

# Call the function to decode the UPC
decode_upc(image_path)

# Make sure you have the necessary libraries installed before running this code. You can install them using the following command:

# pip install opencv-python pyzbar

# Replace "path/to/your/image.png" with the actual path to your PNG image file containing the flattened UPC. The code will decode the UPC and print the results, including the UPC data and barcode type.

# Note: Ensure that the image is of sufficient quality and clarity for accurate barcode recognition.
