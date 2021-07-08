#!/usr/bin/env python3

#Math is based on http://www.brucelindbloom.com/index.html?Math.html
import math
import argparse
import string
import sys

def hex_to_rgb(hexcode):
    hexcode = hexcode.lstrip('#')
    length = len(hexcode)
    return tuple(int(hexcode[i:(i + length//3)], 16) for i in range(0, length, length//3))

def rgb_to_xyz(rgb_color):
    r = inverse_srgb_companding(rgb_color[0] / 255.0)
    g = inverse_srgb_companding(rgb_color[1] / 255.0)
    b = inverse_srgb_companding(rgb_color[2] / 255.0)

    x = (0.4124564 * r + 0.3575761 * g + 0.1804375 * b)
    y = (0.2126729 * r + 0.7151522 * g + 0.0721750 * b)
    z = (0.0193339 * r + 0.1191920 * g + 0.9503041 * b)
    return (x, y, z)

def inverse_srgb_companding(x):
    if (x <= 0.04045):
        return x / 12.92
    else:
        return ((x + 0.055) / 1.055)**2.4

def xyz_to_lab(xyz_color)
    #Using standard illuminant D65 - XYZ needs to be scaled. 
    #Existing color differences seem to be based on supplementary 10° observer.
    #TODO: Change this to standard 2° observer, once the page generator is done.
    x = pivot_xyz((xyz_color[0]*100)/95.047)
    y = pivot_xyz((xyz_color[1]*100)/100.000)
    z = pivot_xyz((xyz_color[2]*100)/108.883)

    l = 116 * y - 16
    a = 500 * (x - y)
    b = 200 * (y - z)

    return (l, a, b)

def pivot_xyz(x):
    if x > 0.008856:
        return x**(1.0/3.0)
    else:
        return (903.3 * x + 16.0)/116.0

#Existing color differences are calculated from CIE94 delta.
#TODO: Switch to CIEDE2000, once the page generator is done
def delta_e_cie94(lab_color1, lab_color2):
    K_1 = 0.045
    K_2 = 0.015
    K_L = 1
    K_C = 1
    K_H = 1

    C_1 = math.sqrt(lab_color1[1]**2 + lab_color1[2]**2)
    C_2 = math.sqrt(lab_color2[1]**2 + lab_color2[2]**2)

    S_L = 1
    S_C = 1 + K_1 * C_1
    S_H = 1 + K_2 * C_1

    deltaa = lab_color1[1] - lab_color2[1]
    deltab = lab_color1[2] - lab_color2[2]

    deltaL = lab_color1[0] - lab_color2[0]
    deltaC = C_1 - C_2
    deltaH = math.sqrt(deltaa**2 + deltab**2 - deltaC**2)

    deltaE = math.sqrt((deltaL/(K_L*S_L))**2 + (deltaC / (K_C * S_C))**2 + (deltaH / (K_H * S_H))**2)

    return deltaE

def hex_to_lab(hexcolor):
    return xyz_to_lab(rgb_to_xyz(hex_to_rgb(hexcolor)))

def is_valid_hexcolor(str1):
    return all(c in string.hexdigits for c in str1) and((len(str1) == 6  and not str1.startswith('#')) or (len(str1) == 7 and str1.startswith('#')))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Calculates the CIE94 delta of two hexadecimal colors.')
    parser.add_argument('reference', metavar='Reference', type=str, help='the hexcode of the reference color')
    parser.add_argument('sample', metavar='Sample', type=str, help='the hexcode of the sample color')
    args = parser.parse_args()

    if not is_valid_hexcolor(args.reference):
        print("Reference color is not a valid hexcolor: '{0}'.".format(args.reference))
        sys.exit()

    if not is_valid_hexcolor(args.sample):
        print("Sample color is not a valid hexcolor: '{0}'.".format(args.sample))
        sys.exit()

    lab1 = hex_to_lab(args.reference)
    lab2 = hex_to_lab(args.sample)
    print(delta_e_cie94(lab1, lab2))
