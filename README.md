# SegRCDB (ICCV2023)
<a href='https://openaccess.thecvf.com/content/ICCV2023/html/Shinoda_SegRCDB_Semantic_Segmentation_via_Formula-Driven_Supervised_Learning_ICCV_2023_paper.html'><img src='https://img.shields.io/badge/Paper-PDF-red'></a> &nbsp; 
<a href='https://dahlian00.github.io/SegRCDBPage/'><img src='https://img.shields.io/badge/Project-Page-Green'></a> &nbsp; 
The repository contains the official SegRCDB generation code.
Details are described in the following paper: 
> [**SegRCDB: Semantic Segmentation via Formula-Driven Supervised Learning**](https://openaccess.thecvf.com/content/ICCV2023/html/Shinoda_SegRCDB_Semantic_Segmentation_via_Formula-Driven_Supervised_Learning_ICCV_2023_paper.html),  
> Risa Shinoda, Ryo Hayamizu, Kodai Nakashima, Nakamasa Inoue, Rio Yokota, Hirokatsu Kataoka
> *ICCV 2023*

# Changelog
2023/09/29: Released SegRCDB generation code and pretrained models.

# Requirements
- Python 3 (worked at 3.7)
- noise (worked at 1.2.2)
- PIL (worked at 9.0.0)

# SegRCDB generation
Run the script to generate SegRCDB with the following command.

```shell
$ bash make_SegRCDB.sh
```

The folder structure is constructed as follows. The input images, annotation images, and category parameters are created in the ```image/```, ```mask/```, and ```param/``` folders, respectively. 

```
./
  SegRCDB-dataset/
    image/
      000000.png
      000001.png
      000002.png
      000003.png
      ...
    mask/
      000000.png
      000001.png
      000002.png
      000003.png
      ...
    param/
      00001.csv
      00002.csv
      00003.csv
      00004.csv
      ...
```
If you want to change the SegRCDB generation parameter, we have prepared some options.   
To determine the SegRCDB class parameter:

```
python SegRCDB_params.py \
  --save_root=${SAVEDIR} # save folder name (default: "./SegRCDB-dataset")
  --numof_classes=${CLASS} # number of class (default: 254)
  --vertex_num=${VERTEX} # maximum number of vertex (default: 500)
  --perlin_min=${PERLIN_MIN} # minimum number of Perlin noise (default: 0)
  --perlin_max=${PERLIN_MAX} # maximum number of Perlin noise (default: 4)
  --line_num_min=${LINE_MIN} # minimum number of polygons each instance has (default: 1)
  --line_num_max=${LINE_MAX} # maximum number of polygons each instance has (default: 50)
  --line_width=${LINE_WIDTH} # line width of polygons (default: 0.1)
  --radius_min=${RADIUS_MIN} # minimum radius from the center of the polygon to its vertices (default: 0)
  --radius_max=${RADIUS_MAX} # maximum radius from the center of the polygon to its vertices (default: 50)
  --oval_rate=${OVAL_RATE} # scaling of the polygon in the horizontal and vertical directions (default: 2)
```
For the input image and annotation rendering:
```
python SegRCDB_render.py \
  --save_root=${SAVEDIR} # save folder name (default: "./SegRCDB-dataset")
  --numof_thread=${THREAD} # thread number
  --thread_num=${i} 
  --numof_classes=${CLASS}  # number of class (default: 254)
  --numof_images=${IMAGES} #the number of images (default: 1000)
  --instance_num=${INSTANCE_PER_IMAGE} # number of instances per image (default: 32)
  --start_pos=${POSITION} # range of the center position of the instance (default: 512)
  --mode=${MODE} # SegRCDB mask type (see the paper for the details, default: M1)
```

You can change the dataset folder name with --save_root. For faster execution, you should run the bash as follows. You must adjust the thread parameter --numof_thread in the script depending on your computational resource.

# Pre-trained weights
Download pre-training models : [**Google Drive**](https://drive.google.com/drive/folders/1MGDnq6kZEzxgKquVnSO-B0UpT4N3ylwY?usp=sharing).

We used [MMSegmentation](https://github.com/open-mmlab/mmsegmentation) , and trained on Swin-base and UPerNet. 


# Citation
If you find our work useful for your research, please consider citing our paper:
```bibtex
@InProceedings{Shinoda_2023_ICCV,
  author    = {Shinoda, Risa and Hayamizu, Ryo and Nakashima, Kodai and Inoue, Nakamasa and Yokota, Rio and Kataoka, Hirokatsu},
  title     = {SegRCDB: Semantic Segmentation via Formula-Driven Supervised Learning},
  booktitle = {Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)},
  month     = {October},
  year      = {2023},
  pages     = {20054-20063}
}
```

## Terms of use
The authors affiliated in National Institute of Advanced Industrial Science and Technology (AIST), Tokyo Denki University (TDU), and Tokyo Institute of Technology (TITech) are not responsible for the reproduction, duplication, copy, sale, trade, resell or exploitation for any commercial purposes, of any portion of the images and any portion of derived the data. In no event will we be also liable for any other damages resulting from this data or any derived data.
