# Dataset Constitution
SAVEDIR="./SegRCDB-dataset"
THREAD=40
CLASS=254
IMAGES=20000
INSTANCE_PER_IMAGE=32

# RCDB Parameters
VERTEX=500
PERLIN_MIN=0
PERLIN_MAX=4
LINE_MIN=1
LINE_MAX=50
LINE_WIDTH=0.1
RADIUS_MIN=0
RADIUS_MAX=50
OVAL_RATE=2
POSITION=512
MODE="M1"

if [ ! -d ${SAVEDIR} ]; then
  mkdir ${SAVEDIR}
fi

python SegRCDB_params.py \
  --save_root=${SAVEDIR} --numof_classes=${CLASS} \
  --vertex_num=${VERTEX} --perlin_min=${PERLIN_MIN} --perlin_max=${PERLIN_MAX} \
  --line_num_min=${LINE_MIN} --line_num_max=${LINE_MAX} --line_width=${LINE_WIDTH} \
  --radius_min=${RADIUS_MIN} --radius_max=${RADIUS_MAX} --oval_rate=${OVAL_RATE} &

wait

# Multi-thread processing
for ((i=0 ; i<${THREAD} ; i++))
do
  python SegRCDB_render.py \
  --save_root=${SAVEDIR} --numof_thread=${THREAD} --thread_num=${i} \
  --numof_classes=${CLASS} --numof_images=${IMAGES} --instance_num=${INSTANCE_PER_IMAGE} \
  --start_pos=${POSITION} --mode=${MODE} &

done
wait