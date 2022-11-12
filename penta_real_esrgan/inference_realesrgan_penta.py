import cv2
import glob
import os
from basicsr.archs.rrdbnet_arch import RRDBNet
from basicsr.utils.download_util import load_file_from_url

from realesrgan import RealESRGANer
from realesrgan.archs.srvgg_arch import SRVGGNetCompact


def super_resolution(
    input_dir="input",
    output_dir="output",
    output_filename="esrgan",
    model_name="RealESRGAN_x4plus",
    denoise_strength=0.5,
    outscale=4,
    model_path=None,
    suffix=0,
    tile=0,
    tile_pad=10,
    pre_pad=0,
    face_enhance=False,
    fp32=False,
    alpha_upsampler="realesrgan",
    ext="auto",
    gpu_id=None,
):
    """Models: RealESRGAN_x4plus | RealESRNet_x4plus | RealESRGAN_x4plus_anime_6B | RealESRGAN_x2plus | realesr-animevideov3 | realesr-general-x4v3"""

    # determine models according to model names
    model_name = model_name.split(".")[0]
    if model_name == "RealESRGAN_x4plus":  # x4 RRDBNet model
        model = RRDBNet(
            num_in_ch=3,
            num_out_ch=3,
            num_feat=64,
            num_block=23,
            num_grow_ch=32,
            scale=4,
        )
        netscale = 4
        file_url = [
            "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth"
        ]
    elif model_name == "RealESRNet_x4plus":  # x4 RRDBNet model
        model = RRDBNet(
            num_in_ch=3,
            num_out_ch=3,
            num_feat=64,
            num_block=23,
            num_grow_ch=32,
            scale=4,
        )
        netscale = 4
        file_url = [
            "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.1/RealESRNet_x4plus.pth"
        ]
    elif model_name == "RealESRGAN_x4plus_anime_6B":  # x4 RRDBNet model with 6 blocks
        model = RRDBNet(
            num_in_ch=3, num_out_ch=3, num_feat=64, num_block=6, num_grow_ch=32, scale=4
        )
        netscale = 4
        file_url = [
            "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth"
        ]
    elif model_name == "RealESRGAN_x2plus":  # x2 RRDBNet model
        model = RRDBNet(
            num_in_ch=3,
            num_out_ch=3,
            num_feat=64,
            num_block=23,
            num_grow_ch=32,
            scale=2,
        )
        netscale = 2
        file_url = [
            "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth"
        ]
    elif model_name == "realesr-animevideov3":  # x4 VGG-style model (XS size)
        model = SRVGGNetCompact(
            num_in_ch=3,
            num_out_ch=3,
            num_feat=64,
            num_conv=16,
            upscale=4,
            act_type="prelu",
        )
        netscale = 4
        file_url = [
            "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-animevideov3.pth"
        ]
    elif model_name == "realesr-general-x4v3":  # x4 VGG-style model (S size)
        model = SRVGGNetCompact(
            num_in_ch=3,
            num_out_ch=3,
            num_feat=64,
            num_conv=32,
            upscale=4,
            act_type="prelu",
        )
        netscale = 4
        file_url = [
            "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-general-wdn-x4v3.pth",
            "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-general-x4v3.pth",
        ]

    # determine model paths
    if model_path is not None:
        model_path = model_path
    else:
        model_path = os.path.join("weights", model_name + ".pth")
        if not os.path.isfile(model_path):
            ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
            for url in file_url:
                # model_path will be updated
                model_path = load_file_from_url(
                    url=url,
                    model_dir=os.path.join(ROOT_DIR, "weights"),
                    progress=True,
                    file_name=None,
                )

    # use dni to control the denoise strength
    dni_weight = None
    if model_name == "realesr-general-x4v3" and denoise_strength != 1:
        wdn_model_path = model_path.replace(
            "realesr-general-x4v3", "realesr-general-wdn-x4v3"
        )
        model_path = [model_path, wdn_model_path]
        dni_weight = [denoise_strength, 1 - denoise_strength]

    # restorer
    upsampler = RealESRGANer(
        scale=netscale,
        model_path=model_path,
        dni_weight=dni_weight,
        model=model,
        tile=tile,
        tile_pad=tile_pad,
        pre_pad=pre_pad,
        half=not fp32,
        gpu_id=None,
    )

    if face_enhance:  # Use GFPGAN for face enhancement
        from gfpgan import GFPGANer

        face_enhancer = GFPGANer(
            model_path="https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.3.pth",
            upscale=outscale,
            arch="clean",
            channel_multiplier=2,
            bg_upsampler=upsampler,
        )
    os.makedirs(output_dir, exist_ok=True)

    if os.path.isfile(input_dir):
        paths = [input_dir]
    else:
        paths = sorted(glob.glob(os.path.join(input_dir, "*")))

    for idx, path in enumerate(paths):
        imgname, extension = os.path.splitext(os.path.basename(path))
        print("Testing", idx, imgname)

        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        if len(img.shape) == 3 and img.shape[2] == 4:
            img_mode = "RGBA"
        else:
            img_mode = None

        try:
            if face_enhance:
                _, _, output = face_enhancer.enhance(
                    img, has_aligned=False, only_center_face=False, paste_back=True
                )
            else:
                output, _ = upsampler.enhance(img, outscale=outscale)
        except RuntimeError as error:
            print("Error", error)
            print(
                "If you encounter CUDA out of memory, try to set --tile with a smaller number."
            )
        else:
            if ext == "auto":
                extension = extension[1:]
            else:
                extension = ext
            if img_mode == "RGBA":  # RGBA images should be saved in png format
                extension = "png"
            if suffix == "":
                save_path = os.path.join(output_dir, f"{imgname}.{extension}")
            else:
                save_path = os.path.join(
                    output_dir, f"{output_filename}_{imgname}.{extension}"
                )
            cv2.imwrite(save_path, output)
