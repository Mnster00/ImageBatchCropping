# Image Cropper

Image Cropper is a user-friendly Windows application that allows you to easily crop multiple images to a specified size from the same position. This tool is perfect for batch processing, ensuring consistency across all your images by applying the same crop area to every picture in a folder.

![Image Cropper Overview](https://github.com/Mnster00/ImageBatchCropping/blob/main/2.png)

## Key Features

- Crop multiple images simultaneously at the same position
- Specify custom crop dimensions applicable to all images
- Easy-to-use graphical interface
- Supports common image formats (PNG, JPEG, BMP, GIF)
- Automatically saves cropped images in a separate folder

## System Requirements

- Windows 

## Installation

1. Go to the [Releases page](https://github.com/Mnster00/ImageBatchCropping/releases) of this repository.
2. Download the latest `batchimgcrop_v1.zip` file.

## How to Use

1. Double-click on `ImageCropper.exe` to launch the application.
2. Click the "Browse" button to select a folder containing the images you want to crop.
3. Enter the desired width and height (in pixels) for your cropped images.
4. Click on the displayed image to set the center point of your crop area. This point will be used for all images.
5. Click the "Crop Images" button to process all images in the selected folder.

![Usage Steps 1](https://github.com/Mnster00/ImageBatchCropping/blob/main/2.png)
![Usage Steps 2](https://github.com/Mnster00/ImageBatchCropping/blob/main/3.png)
![Usage Steps 3](https://github.com/Mnster00/ImageBatchCropping/blob/main/4.png)
![Usage Steps 4](https://github.com/Mnster00/ImageBatchCropping/blob/main/5.png)
![Usage Steps_5](https://github.com/Mnster00/ImageBatchCropping/blob/main/6.png)

**Important**: The crop area you define will be applied to all images in the folder. Make sure your images have similar layouts for best results.

Cropped images will be saved in a new folder named "cropped_images" within the original folder.

## Example Use Case

Imagine you have 100 product photos, all taken from the same angle but with slight variations in position. With Image Cropper, you can:
1. Set the crop dimensions (e.g., 500x500 pixels).
2. Choose the center point that works best for most images.
3. Crop all 100 images at once, ensuring the main product is in the same position in every resulting image.

