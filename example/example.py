# -*- coding: utf-8 -*-
from __future__ import (
    division,
    print_function,
)

import matplotlib
matplotlib.use('Agg')

import skimage.data
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import cv2
import sys
import time
import selectivesearch


def main():
    # loading astronaut image
    try:
        sys.argv[1]
    except:
        img = skimage.data.astronaut()
    else:
        img = cv2.imread(sys.argv[1])
    
    print(img.shape[0]+"x"+img.shape[1])
    start = time.time()
    # perform selective search
    img_lbl, regions = selectivesearch.selective_search(
        img, scale=200, sigma=0.9, min_size=10)

    print(len(regions))

    candidates = set()
    for r in regions:
        # excluding same rectangle (with different segments)
        if r['rect'] in candidates:
            continue
        # excluding regions smaller than 2000 pixels
        if r['size'] < 2000:
            continue
        # distorted rects
        x, y, w, h = r['rect']
        if w / h > 1.2 or h / w > 1.2:
            continue
        candidates.add(r['rect'])

    # draw rectangles on the original image
    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(6, 6))
    ax.imshow(img)
    end = time.time()
    print(candidates)
    for x, y, w, h in candidates:
        print(x, y, w, h)
        rect = mpatches.Rectangle(
            (x, y), w, h, fill=False, edgecolor='red', linewidth=1)
        ax.add_patch(rect)
        color = (0.0, 255.0, 0.0)
        pt1 = (x, y+h)
        pt2 = (x+w, y)
        cv2.rectangle(img, pt1, pt2, color)
    print("Time elapsed:")
    print(end - start)
    plt.show()

    # save drawn image to file
    cv2.imwrite("_RESULT_.jpg", img)

if __name__ == "__main__":
    main()
