import math
from PIL import Image, ImageDraw
import random
import noise
import os
import argparse
import csv

def conf():
    parser = argparse.ArgumentParser()
    parser.add_argument("--save_root", default="./SegRCDB-dataset",type=str, help="path to image file save directory")
    parser.add_argument("--numof_classes", default=1000, type=int, help="SegRCDB category number")
    parser.add_argument("--numof_images", default=1000, type=int, help="SegRCDB instance number")
    parser.add_argument("--instance_num", default=32, type=int, help="Number of polygons in a image")
    parser.add_argument("--image_size", default=512, type=int)
    parser.add_argument("--numof_thread", default=1, type=int, help="")
    parser.add_argument("--thread_num", default=0, type=int, help="")
    parser.add_argument("--start_pos", default=512, type=int, help="")
    # render mode
    parser.add_argument("--mode", default="M1",type=str, help="SegRCDB render mode")
    # Display on screen
    parser.add_argument("--display", action='store_true', help="Display the generated images")
    args = parser.parse_args()
    return args

args = conf()
vertex_x = []
vertex_y = []
point_x = []
point_y = []
Noise_x = []
Noise_y = []
im = []
xys=[]
mask = []
vertex_number = 3
images = args.numof_images / args.numof_thread
random.seed(args.thread_num + 1)

if not os.path.exists(os.path.join(args.save_root, "image")):
    os.makedirs(os.path.join(args.save_root, "image"), exist_ok=True)
if not os.path.exists(os.path.join(args.save_root, "mask")):
    os.makedirs(os.path.join(args.save_root, "mask"), exist_ok=True)

# Prameter search per category
for k2 in range(int(images)):
    im.append(Image.new('RGB', (args.image_size, args.image_size), (0, 0, 0)))
    mask.append(Image.new('RGB', (args.image_size, args.image_size), (0, 0, 0)))
    draw = ImageDraw.Draw(im[k2])
    mask_draw = ImageDraw.Draw(mask[k2])

    for k1 in range(args.instance_num):
        vertex_x.clear()
        vertex_y.clear()
        cat = random.randint(1, (args.numof_classes))

        with open(os.path.join(args.save_root, "param/%05d.csv" % cat), 'r') as f:
            reader = csv.reader(f)
            l = [row for row in reader]

        class_num = int(l[0][1])
        vertex_number = int(l[1][1])
        perlin_noise_coefficient = float(l[2][1])
        line_width = float(l[3][1])
        start_rad = float(l[4][1])
        line_draw_num = int(l[5][1])
        oval_rate_x = float(l[6][1])
        oval_rate_y = float(l[7][1])
        g = int(l[8][1])
        start_pos_h = (args.image_size + random.randint(-1 * args.start_pos, args.start_pos)) / 2
        start_pos_w = (args.image_size + random.randint(-1 * args.start_pos, args.start_pos)) / 2
        angle = (math.pi * 2) / vertex_number

        for vertex in range(vertex_number):
            vertex_x.append(math.cos(angle * vertex) * start_rad * oval_rate_x + start_pos_w)
            vertex_y.append(math.sin(angle * vertex) * start_rad * oval_rate_y + start_pos_h)
        
        vertex_x.append(vertex_x[0])
        vertex_y.append(vertex_y[0])

        for line_draw in range(line_draw_num):
            gray = random.randint(0, 255)
            Noise_x.clear()
            Noise_y.clear()

            for vertex in range(vertex_number):
                Noise_x.append(random.uniform(0 , 10000))
                Noise_x[vertex] = noise.pnoise1(Noise_x[vertex]) * perlin_noise_coefficient * 2 - perlin_noise_coefficient

            for vertex in range(vertex_number):
                Noise_y.append(random.uniform(0 , 10000))
                Noise_y[vertex] = noise.pnoise1(Noise_y[vertex]) * perlin_noise_coefficient * 2 - perlin_noise_coefficient

            for vertex in range(vertex_number):
                vertex_x[vertex] -= math.cos(angle * vertex) * (Noise_x[vertex] - line_width)
                vertex_y[vertex] -= math.sin(angle * vertex) * (Noise_y[vertex] - line_width)

            vertex_x[vertex_number] = vertex_x[0]
            vertex_y[vertex_number] = vertex_y[0]

            for vertex in range(vertex_number):
                xys = [(vertex_x[vertex], vertex_y[vertex]), (vertex_x[vertex + 1], vertex_y[vertex + 1])]

                if vertex == 0:
                    points = xys
                else:
                    points.extend(xys)

            if args.mode == "M1":
                for i in range(vertex_number):
                    mask_draw.line((vertex_x[i], vertex_y[i], vertex_x[i + 1], vertex_y[i + 1]) , fill = (g, g, g), width = 1)
                if line_draw == line_draw_num - 1:
                    mask_save = mask[k2].convert("L")
                    mask_save.save(args.save_root + "/mask/%06d.png" % ((images * args.thread_num + k2)), quality = 95)

            elif args.mode == "M2":
                if line_draw == 0:
                    mask_hole = points
                elif line_draw == line_draw_num - 1:
                    mask_draw.polygon(points, fill = (g, g, g))
                    mask_draw.polygon(mask_hole, fill = (0, 0, 0))
                    mask_hole.append(mask_hole[0])
                    points.append(points[0])
                    for i in range(vertex_number*2-1):
                        mask_draw.line((mask_hole[i][0], mask_hole[i][1], mask_hole[i+1][0], mask_hole[i+1][1]), fill = (g, g, g), width = 1)
                    for i in range(vertex_number*2-1):
                        mask_draw.line((points[i][0], points[i][1], points[i+1][0], points[i+1][1]), fill = (g, g, g), width = 1)
                    mask_save = mask[k2].convert("L")
                    mask_save.save(args.save_root + "/mask/%06d.png" % ((images * args.thread_num + k2)), quality = 95)

            elif args.mode == "M3":
                if line_draw == line_draw_num - 1:
                    for i in range(vertex_number):
                        mask_draw.polygon(points, fill = (g, g, g))
                    mask_save = mask[k2].convert("L")
                    mask_save.save(args.save_root + "/mask/%06d.png" % ((images * args.thread_num + k2)), quality = 95)

            for i in range(vertex_number):
                draw.line((vertex_x[i], vertex_y[i], vertex_x[i + 1], vertex_y[i + 1]) , fill = (gray, gray, gray), width = 1)
                
        if not args.display:
            im[k2].save(args.save_root + "/image/%06d.png" % ((images * args.thread_num + k2)), quality = 95)
        else:
            im[k2].show()
