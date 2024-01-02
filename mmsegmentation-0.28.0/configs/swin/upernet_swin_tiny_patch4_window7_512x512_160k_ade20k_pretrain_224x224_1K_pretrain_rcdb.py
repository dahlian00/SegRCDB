_base_ = [
    '../_base_/models/upernet_swin_pretrain_segrcdb.py', '../_base_/datasets/rcdb.py',
    '../_base_/default_runtime.py', '../_base_/schedules/schedule_300.py'
]

#checkpoint_file = "/groups/gae50924/shinoda/mmsegmentation/data/convert_swin_base_patch4_window7_224_imagenet1k_300ep.pth" # noqa
model = dict(
    backbone=dict(
        #init_cfg=dict(type='Pretrained', checkpoint=checkpoint_file),
        init_cfg=None,
        #frozen_stages=4,
        embed_dims=96,
        depths=[2, 2, 6, 2],
        num_heads=[3, 6, 12, 24],
        window_size=7,
        use_abs_pos_embed=False,
        drop_path_rate=0.3,
        patch_norm=True),
    decode_head=dict(in_channels=[96, 192, 384, 768], num_classes=255),
    auxiliary_head=dict(in_channels=384, num_classes=255))

# AdamW optimizer, no weight decay for position embedding & layer norm
# in backbone
optimizer = dict(
    _delete_=True,
    type='AdamW',
    lr=0.0006,
    betas=(0.9, 0.999),
    weight_decay=0.01,
    paramwise_cfg=dict(
        custom_keys={
            'absolute_pos_embed': dict(decay_mult=0.),
            'relative_position_bias_table': dict(decay_mult=0.),
            'norm': dict(decay_mult=0.),
            #'head': dict(lr_mult=10.)
        }))

lr_config = dict(
    _delete_=True,
    policy='poly',
    warmup='linear',
    warmup_iters=1500,
    warmup_ratio=1e-6,
    power=1.0,
    min_lr=0.0,
    by_epoch=False)

# By default, models are trained on 8 GPUs with 2 images per GPU
data = dict(samples_per_gpu=4)
