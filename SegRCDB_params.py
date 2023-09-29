import math
from PIL import Image, ImageDraw
import random
import os
import argparse
import csv

########################################################################################
def conf():
    parser = argparse.ArgumentParser()
    parser.add_argument("--save_root", default="./SegRCDB-dataset",type=str, help="path to image file save directory")
    parser.add_argument("--numof_classes", default=254, type=int, help="SegRCDB category number")
    # Category parameter setting
    parser.add_argument("--vertex_num", default=500, type=int, help="")
    parser.add_argument("--line_width", default=0.01, type=float, help="")
    parser.add_argument("--perlin_min", default=0, type=int, help="")
    parser.add_argument("--perlin_max", default=4, type=int, help="")
    parser.add_argument("--radius_min", default=0, type=int, help="")
    parser.add_argument("--radius_max", default=50, type=int, help="")
    parser.add_argument("--line_num_min", default=1, type=int, help="")
    parser.add_argument("--line_num_max", default=50, type=int, help="")
    parser.add_argument("--oval_rate", default=2, type=int, help="")

    args = parser.parse_args()
    return args
args = conf()

# Parameter search
vertex_number = 3
gray = 0
numof_classes = args.numof_classes
random.seed(0)

# Parameter define
for cat in range(args.numof_classes):

    if not os.path.exists(os.path.join(args.save_root, "param")):
        os.makedirs(os.path.join(args.save_root, "param"))

    # Prameter search per category
    while True:
        vertex_number = int(random.expovariate(1 / (args.vertex_num / 5)))

        if (vertex_number > 2 and vertex_number <= args.vertex_num):
            break

    line_draw_num = random.randint(args.line_num_min , args.line_num_max)
    perlin_noise_coefficient = random.uniform(args.perlin_min, args.perlin_max)
    line_width = random.uniform(0.0, args.line_width)
    start_rad = random.randint(args.radius_min, args.radius_max)
    oval_rate_x = random.uniform(1, args.oval_rate)
    oval_rate_y = random.uniform(1, args.oval_rate)
    gray = gray + 1

    # csv file save
    with open(os.path.join(args.save_root, "param/%05d.csv" % (cat + 1)), 'w') as f:
        param = {'Category_num':(cat + 1), 'Vertex': vertex_number, 'Perlin_noise': perlin_noise_coefficient, 'line_width': line_width, \
                    'Center_rad': start_rad, 'Line_num': line_draw_num, 'Oval_rate_x': oval_rate_x, 'Oval_rate_y': oval_rate_y, \
                    'Color_Gray': gray, \
                }
        writer = csv.writer(f)
        for k, v in param.items():
            writer.writerow([k, v])

    print('define Category:' + str(cat + 1))

