import numpy as np
from numpy import dtype, uint8

class lena(object):
    def __init__(self, pallete):
        self.pallete = pallete

    # Open the file for reading
    def read_file(self, my_file):
        stream = open(my_file, 'rb')
        img = np.fromfile(stream, dtype=(uint8, 3))
        return img

    # Create a dither matrix
    def dither_matrix_row(self, row, mat):
        my_row = []
        for i in range(128):
            for j in mat[row]:
                my_row.append(j)
        return my_row

    # Span the 4 X 4 dither matrix from the book in 512 X 512
    def dither_matrix(self, first, second, third, fourth):
        dither = []
        total_length = 0
        all_rows = [first, second, third, fourth]
        for i in range(len(all_rows)):
            total_length += len(all_rows[i])

        for i in range(128):
            dither.append(first)
            dither.append(second)
            dither.append(third)
            dither.append(fourth)
        dither = np.reshape(dither, (-1, 512))
        return dither

    # Transform the image
    def quantize(self, img_array, dither_array):
        quantized_array = []
        for i in range(512):
            for j in range(512):
                if img_array[i][j] > dither_array[i][j]:
                    quantized_array.append(255)
                else:
                    quantized_array.append(0)
        temp_array = np.zeros(len(quantized_array), dtype=(uint8))
        for i in range(len(quantized_array)):
            temp_array[i] = quantized_array[i]
        return temp_array

    # Combine all three red, green and blue
    def combine_rgb(self, r, g, b):
        rgb = np.zeros(len(r), dtype=(uint8, 3))
        for i in range(len(r)):
            rgb[i][0] = r[i]
            rgb[i][1] = g[i]
            rgb[i][2] = b[i]
        return rgb

    # Scale dither matrix from 0 to 255 (8 bit) red and green
    # Add 1 to the dither multiply by 16 and subtract 1
    def scaled_dither(self, dither):
        dither = np.add(dither, 1)
        dither = np.dot(dither, 16)
        dither = np.add(dither, -1)
        return dither


if __name__ == '__main__':
    # 4 X 4 dither matrix from the book
    pallete = np.array([
        [0, 8, 2, 10],
        [12, 4, 14, 6],
        [3, 11, 1, 9],
        [15, 7, 13, 5]]
        )
    # Instantiate lena with the pallete
    lena = lena(pallete)
     
    # File must be a .data extension
    file_to_open = raw_input('Enter a .data file: ')

    #img = lena.read_file('LennaRGB512.data')
    img = lena.read_file(file_to_open)

    # Initialize red, green, blue arrays with zeros
    red = np.zeros(len(img), dtype=(uint8))
    green = np.zeros(len(img), dtype=(uint8))
    blue = np.zeros(len(img), dtype=(uint8))

    # Create the three channels for red, green and blue
    for i in range(len(img)):
        red[i] = img[i][0]    # Red channel
        green[i] = img[i][1]  # Green channel
        blue[i] = img[i][2]   # Blue channel

    # Convert linear arrays to 512 X 512
    red = np.reshape(red, (-1, 512))
    green = np.reshape(green, (-1, 512))
    blue = np.reshape(blue, (-1, 512))

    # Populate pallete along rows
    first = lena.dither_matrix_row(0, pallete)
    second = lena.dither_matrix_row(1, pallete)
    third = lena.dither_matrix_row(2, pallete)
    fourth = lena.dither_matrix_row(3, pallete)

    # Populate entire matrix using rows
    my_dither = lena.dither_matrix(first, second, third, fourth)

    # Scale dither matrix from 0 to 255 (8 bit)
    my_scaled_dither = lena.scaled_dither(my_dither)

    # Quantize the arrays
    quantized_lena_red = lena.quantize(red, my_scaled_dither)
    quantized_lena_green = lena.quantize(green, my_scaled_dither)
    quantized_lena_blue = lena.quantize(blue, my_scaled_dither)

    # Combine three layers of red, green and blue
    quantized_lena_rgb = lena.combine_rgb(
        quantized_lena_red,
        quantized_lena_green,
        quantized_lena_blue
        )

    # Save the new file
    quantized_lena_rgb.tofile(file_to_open + '_3bit.data')
