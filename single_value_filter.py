"""
Applies single value filter to image
"""
import cv2
import numpy as np

BASE = r'/Users/Andrew1/Documents/filters'

def main(fname, ext= 'jpeg', color_hue = 0, constant_value = True, switch = False):
    # Read Image and convert to RGB then HSV
    raw_im = cv2.imread(fname + '.' + ext)
    im_rgb = cv2.cvtColor(raw_im, cv2.COLOR_BGR2RGB)

    hsv_image = cv2.cvtColor(im_rgb, cv2.COLOR_RGB2HSV)

    # Set value as constant to the average value
    edited_hsv = hsv_image.copy()

    if constant_value:
        values = hsv_image[:,:,2]
        average_value = values.mean() 
        print(average_value)   
        edited_hsv[:,:,2] = average_value

    # Project to single hue dim
    hues = np.asarray(edited_hsv[:,:,0]).astype(int)
    thetas = (hues * 2) - color_hue
    c_saturations = edited_hsv[:,:,1] / 255

    def find_lam(theta, c_saturation):
        return np.cos(np.radians(theta)) * c_saturation

    lams = find_lam(thetas, c_saturations)

    neg_mask = lams <= 0 

    single_dim_hsv = edited_hsv.copy()

    if not switch:
        single_dim_hsv[:,:,0] = (color_hue // 2)
        single_dim_hsv[neg_mask, 0] = (color_hue // 2) + 90
    elif switch:
        single_dim_hsv[:,:,0] = (color_hue // 2) + 90
        single_dim_hsv[neg_mask, 0] = (color_hue // 2) 

    single_dim_hsv[:,:,1] = np.abs(lams) * 255

    # Convert back and save
    im = single_dim_hsv

    im = cv2.cvtColor(im, cv2.COLOR_HSV2RGB)

    cv2.imwrite(f'filtered_{fname}_{color_hue}_{"const" if constant_value else ""}.jpg',  cv2.cvtColor(im, cv2.COLOR_RGB2BGR))
    return im

if __name__ == '__main__':

    fname = 'beach'
    ext = 'jpeg'

    color_hue = 270 # 0 for red # 280 for purple
    constant_value = True
    switch = True

    main(fname, 
         ext=ext, 
         color_hue=color_hue, 
         constant_value=constant_value,
         switch=switch)