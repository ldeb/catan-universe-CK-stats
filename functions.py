from PIL import Image
import pyscreenshot as ImageGrab
import numpy as np
import datetime
import sys, os, shutil
# from sys import stdout

DEBUG = False
dot_pos =       [(12,74), (38,74), (12,86), (24,86), (38,86), (12,98), (38,98)]
valid_colors_web =  ['d79e31','008ba9','458d32', '000000'];
valid_colors_app =  ['d3a105','2c8bad','4a8f1b', '000000'];

dice_decal =    74-12
borders_web =       [(24, 60), (50, 74), (24 + dice_decal, 60),(60, 74), (56,50),(81, 22)]
borders_app =   [(24, 60), (51, 74), (24 + dice_decal, 60),(60, 74), (56,50),(82, 22)]
MODE = 'web'

# SYS stuff: removes images
def clean_images(dirpath):
    print('cleaning images...')
    for the_file in os.listdir(dirpath):
        if the_file != 'index.php':
            file_path = os.path.join(dirpath, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)

# PIL stuff
def compare(file1, file2):
  im = [None, None] # to hold two arrays
  for i, f in enumerate([file1, file2]):
    im[i] = (np.array(Image.open(f)
                 #.convert('L')            # convert to grayscale using PIL
                 .resize((32,32), resample=Image.BICUBIC)) # reduce size and smooth a bit using PIL
                 ).astype(np.int)   # convert from unsigned bytes to signed int using numpy
  return np.abs(im[0] - im[1]).sum()

def change_contrast(img, level):
    factor = (259 * (level + 255)) / (255 * (259 - level))
    def contrast(c):
        return 128 + factor * (c - 128)
    return img.point(contrast)

# screenshot
def take_screenshot(screenshot_coords):
    top_x = screenshot_coords[0]
    top_y = screenshot_coords[1]
    width = 112
    bottom_x = top_x + width
    bottom_y = top_y + width
    return ImageGrab.grab(bbox=(top_x, top_y, bottom_x, bottom_y))

def rgb2hex(r, g, b):
    return '{:02x}{:02x}{:02x}'.format(r, g, b)

def get_color(im, coords):
    rgb_im = im.convert('RGB')
    r, g, b = rgb_im.getpixel(coords)
    col_hex = rgb2hex(r, g, b)
    return col_hex

def get_number_dice(im, dice_num):
    number = 0
    if dice_num == 1:
        x_decal = 0
    else:
        x_decal = dice_decal

    im = change_contrast(im, 200)
    rgb_im = im.convert('RGB')
    num = 2
    for coords in dot_pos:
        color_detected = get_color(im, (coords[0] + x_decal, coords[1]))
        passed = ( color_detected == '000000' )
        if passed:
            number = number + 1
        # print( '{}  {}   {}'.format( (coords[0] + x_decal, coords[1]), passed, color_detected) )
    if number > 6:
        number = 0
    # print( '={}'.format(number) )
    return number

def get_number(im):
    return get_number_dice(im, 1) + get_number_dice(im, 2)

def delete_file(file_path):
    try:
        os.unlink(file_path)
    except Exception as e:
        print(e)

def rename_file(file_path, new_file_path):
    try:
        os.rename(file_path, new_file_path)
    except Exception as e:
        print(e)

def valid_borders(im):
    global MODE
    im = change_contrast(im, 300)
    im = im.convert('RGB').convert('L')
    if DEBUG:
        im.save( os.path.join('web/temp.png'), 'PNG')

    if MODE == 'app':
        borders = borders_app
    else:
        borders = borders_web
    for border_coords in borders:
        if get_color(im, border_coords) != 'ffffff':
            return False

    return True
    # if get_color(im, (24, 60)) == 'ffffff':                         # left dice top
    #     if get_color(im, (50, 74)) == 'ffffff':                     # left dice right
    #         if get_color(im, (24 + dice_decal, 60)) == 'ffffff':    # right dice top
    #             if get_color(im, (60, 74)) == 'ffffff':             # right dice left
    #                 # if get_color(im, (56,50)) == 'ffffff':          # top dice bottom
    #                     return True
    #                 #     return get_color(im, (80, 22)) == 'ffffff'  # top dice right
    #                 # else:
    #                 #     return False
    #             else:
    #                 return False
    #         else:
    #             return False
    #     else:
    #         return False
    # else:
    #     return False

def valid_img(im):
    global MODE
    # valid dice colors
    color_special = get_color(im, (59, 37))
    color_left = get_color(im, (24, 74))
    color_right = get_color(im, (24 + dice_decal, 74))
    print('color: {}, left: {}, right: {}'.format(color_special,color_left,color_right))
    valid = False
    if MODE == 'app':
        valid_colors = valid_colors_app
    else:
        valid_colors = valid_colors_web
    valid = color_special in valid_colors and color_left == 'ffffff' and (color_right in ['ff0015', 'ff0000'])
    # valid borders (dice zoom)
    if valid == False:
        print('Undetected colors!')
    else:
        valid = valid_borders(im)
        if valid == False:
            print('Undetected borders!')

    if valid:
        return color_special
    else:
        return None

def get_screen_infos(im):
    color = valid_img(im)
    if color == None:
        return None

    dice1 = get_number_dice(im, 1)
    dice2 = get_number_dice(im, 2)

    results = {'color': color, 'dice1': dice1, 'dice2': dice2}
    return results

def new_image_action2(screen_info, res, dirpath, filename):
    print('Color: {}'.format(screen_info['color']))
    number = screen_info['dice1'] + screen_info['dice2']
    print('Number: {}'.format(number))

    file_path = os.path.join(dirpath, filename  + '.png')
    filename = '{}-{}-hex{}-{}'.format(filename, res, screen_info['color'], number)
    # rename current to save compare score and color
    rename_file(file_path, os.path.join(dirpath, filename + '.png'))

    res = {'filename': filename}
    return res

#
# def new_image_action(im, res, dirpath, filename):
#     # get color
#     # color = get_color(im, (59, 37))
#     color = valid_img(im)
#     # stop here if not in valid colors
#     if color == None:
#     # if color not in valid_colors:
#         # delete current file
#         file_path = os.path.join(dirpath, filename  + '.png')
#         if not DEBUG:
#             delete_file(file_path)
#         print('Undetected dices!')
#         return None
#     else:
#
#         print('Color: {}'.format(color))
#         number = get_number(im)
#         # stop here if not in valid number
#             # return None
#         print('Number: {}'.format(number))
#         file_path = os.path.join(dirpath, filename  + '.png')
#         filename = '{}-{}-hex{}-{}'.format(filename, res, color, number)
#         # rename current to save compare score and color
#         rename_file(file_path, os.path.join(dirpath, filename + '.png'))
#         #return filename
#
#         res = {'filename': filename}
#         return res

# watch
def watch(screenshot_coords, action, dirpath, lastfilename, lastfileimage, nb):
    # global lastfilename, nb
    global MODE
    if action == 'app':
        MODE = 'app';
    # NOM FICHIER
    today = datetime.datetime.today()
    filename = today.strftime("%Y%m%d%H%M%S")
    file_path = os.path.join(dirpath, filename  + '.png')

    # SCREENSHOT
    # print('taking screenshot... ' + filename + '.png')

    try:
        im = take_screenshot(screenshot_coords)      # im.show()
        im.save( os.path.join(dirpath + filename + '.png'), 'PNG')
    except Exception as e:
        print(e)
    # compare 2 last screenshots
    if lastfilename != '':
        lastfile_path = os.path.join(dirpath, lastfilename  + '.png')
        try:
            res = compare(file_path, lastfile_path)
            if res < 1000:    # same image
                try:
                    # delete current file
                    delete_file(file_path)
                except Exception as e:
                    print(e)
            else:
                print('--------------------------------------\nScreenshot taken: ' + filename + '.png')
                # second verification
                screen_info = get_screen_infos(im)
                last_screen_info = get_screen_infos(lastfileimage)
                print(screen_info)
                print(last_screen_info)
                if screen_info == None or last_screen_info == None :
                    print('Undetected dices!')
                    try:
                        # delete current file
                        delete_file(file_path)
                    except Exception as e:
                        print(e)
                elif screen_info["dice1"] == last_screen_info["dice1"] and screen_info["dice2"] == last_screen_info["dice2"] and screen_info["color"] == last_screen_info["color"]:
                    print('Excatly the same dices, ignoring last one, scrore: {}'.format(res))
                    try:
                        # delete current file
                        delete_file(file_path)
                    except Exception as e:
                        print(e)
                else:
                    print('Comparaison score: {}'.format(res))
                    # rename current to save compare score and color
                    # results = new_image_action(im, res, dirpath, filename)
                    results = new_image_action2(screen_info, res, dirpath, filename)
                    if results != None:
                        lastfilename = results['filename'];
                        lastfileimage = im
                        # nb = results['nb']
                        nb = nb + 1
                        print('NBTOT: {}'.format(nb))


        except Exception as e:
            print(e)

    else:
        print('--------------------------------------\nScreenshot taken: ' + filename + '.png')
        # results = new_image_action(im, 0, dirpath, filename)
        screen_info = get_screen_infos(im)
        if screen_info != None:
            results = new_image_action2(screen_info, 0, dirpath, filename)
            if results != None:
                lastfilename = results['filename'];
                lastfileimage = im
                nb = nb + 1
                print('NBTOT: {}'.format(nb))
        else:
            # delete current file
            file_path = os.path.join(dirpath, filename  + '.png')
            if not DEBUG:
                delete_file(file_path)
            print('Undetected dices!')

    sys.stdout.flush()

    results = {'lastfilename': lastfilename, 'lastfileimage': lastfileimage, 'nb': nb}
    return results
