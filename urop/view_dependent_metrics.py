import cv2 as cv
import subprocess as sp
import open3d as o3d  # 0.14.1, don't use 0.15
import open3d.visualization.rendering as rendering
import numpy as np
import os

magick_dir = '/temp/pranav/PCCArena/' + 'urop'


def view_dependent_metrics(ref_pc_path, target_pc_path, evl_path):
    ref_dir, ref_file_name = os.path.split(ref_pc_path)
    name_without_extension = os.path.splitext(ref_file_name)[0]

    parent_ref_dir = os.path.abspath(os.path.join(ref_dir, '..'))
    ground_truth_path = os.path.join(parent_ref_dir, 'views/', name_without_extension)

    # modify name as decompressed ply has dec not vox10 in name
    subs = name_without_extension.split('_')
    name_without_extension = subs[0] + "_dec_" + subs[2]
    target_dir, target_file_name = os.path.split(target_pc_path)
    parent_target_dir = os.path.abspath(os.path.join(target_dir, '..'))
    target_path = os.path.join(parent_target_dir, 'views/', name_without_extension)

    # ground_truth_path AND target_path += 'up' down etc + '.png' ; then assign to vars
    temp_img_path_name = os.path.join(parent_target_dir, 'views/', name_without_extension + "_TEMP")

    ssim_up, psnr_up = caculate_metric_ignore_background(magick_dir, ground_truth_path + 'up.png',
                                                         target_path + 'up.png', temp_img_path_name + 'up')
    ssim_down, psnr_down = caculate_metric_ignore_background(magick_dir, ground_truth_path + 'down.png',
                                                             target_path + 'down.png', temp_img_path_name + 'down')
    ssim_left, psnr_left = caculate_metric_ignore_background(magick_dir, ground_truth_path + 'left.png',
                                                             target_path + 'left.png', temp_img_path_name + 'left')
    ssim_right, psnr_right = caculate_metric_ignore_background(magick_dir, ground_truth_path + 'right.png',
                                                               target_path + 'right.png', temp_img_path_name + 'right')
    ssim_front, psnr_front = caculate_metric_ignore_background(magick_dir, ground_truth_path + 'front.png',
                                                               target_path + 'front.png', temp_img_path_name + 'front')
    ssim_back, psnr_back = caculate_metric_ignore_background(magick_dir, ground_truth_path + 'back.png',
                                                             target_path + 'back.png', temp_img_path_name + 'back')

    avg_ssim = (ssim_up + ssim_down + ssim_left + ssim_right + ssim_front + ssim_back) / 6.0
    avg_psnr = (psnr_up + psnr_down + psnr_left + psnr_right + psnr_front + psnr_back) / 6.0

    lines = [f"SSIM up: {ssim_up}",
             f"SSIM down: {ssim_down}",
             f"SSIM left: {ssim_left}",
             f"SSIM right: {ssim_right}",
             f"SSIM front: {ssim_front}",
             f"SSIM back: {ssim_back}",
             #
             f"PSNR up: {psnr_up}",
             f"PSNR down: {psnr_down}",
             f"PSNR left: {psnr_left}",
             f"PSNR right: {psnr_right}",
             f"PSNR front: {psnr_front}",
             f"PSNR back: {psnr_back}",

             f"Avg PSNR: {avg_psnr}",
             f"Avg SSIM: {avg_ssim}",
             "\n"]

    return lines


    # return [f"Avg SSIM: {avg_ssim}",
    #         f"Avg PSNR: {avg_psnr}",
    #         "\n"]


def caculate_metric_ignore_background(
        binary_path: str,  # binary path of magick
        input_filename1: str,  # ground truth
        input_filename2: str,  # target
        mask_file_name: str  # tmp file name for mask background
):
    output_filename_ssim = f"{mask_file_name}_mask_ssim.png"
    output_filename_psnr = f"{mask_file_name}_mask_psnr.png"

    img = cv.imread(input_filename1)
    rows, cols, _ = img.shape
    # Note that we assume two input files have the same dimension
    img2 = cv.imread(input_filename2)

    # print("file names for parallel PSNR_SSIM: ", flush=True)
    # print(input_filename1, flush=True)
    # print(input_filename2, flush=True)
    # print(output_filename_ssim, flush=True)
    # print(output_filename_psnr, flush=True)
    # print(f"{mask_file_name}_ssim.png", flush=True)
    # print(f"{mask_file_name}_psnr.png\n", flush=True)

    grey = 127
    threshold = 1.1  # background flactuate in new open3d rendering method
    for i in range(rows):
        for j in range(cols):
            if (
                    (
                            abs(img.item(i, j, 0) - grey) < threshold and
                            abs(img.item(i, j, 1) - grey) < threshold and
                            abs(img.item(i, j, 2) - grey) < threshold
                    ) and (
                    abs(img2.item(i, j, 0) - grey) < threshold and
                    abs(img2.item(i, j, 1) - grey) < threshold and
                    abs(img2.item(i, j, 2) - grey) < threshold
            )
            ):
                img.itemset((i, j, 0), 0)
                img.itemset((i, j, 1), 0)
                img.itemset((i, j, 2), 0)
            else:
                img.itemset((i, j, 0), 255)
                img.itemset((i, j, 1), 255)
                img.itemset((i, j, 2), 255)

    cv.imwrite(output_filename_ssim, img)  # output mask file
    cv.imwrite(output_filename_psnr, img)  # output mask file

    if not os.path.exists(output_filename_ssim):
        print("SSIM MASK IS NOT PRESENT AFTER WRITING: ", output_filename_ssim, flush=True)
    if not os.path.exists(output_filename_psnr):
        print("PSNR MASK IS NOT PRESENT AFTER WRITING", output_filename_psnr, flush=True)
    if not os.path.exists(input_filename1):
        print("INPUT FILE1 IS NOT PRESENT", input_filename1, flush=True)
    if not os.path.exists(input_filename2):
        print("INPUT FILE 2 IS NOT PRESENT", input_filename2, flush=True)

    out1 = sp.run(
        [
            f"{binary_path}/magick",
            "compare",
            "-metric",
            "ssim",
            "-read-mask",
            f"{output_filename_ssim}",
            input_filename1, input_filename2,
            f"{mask_file_name}_ssim.png"  # f"hat_diff_{output_filename}
        ], capture_output=True, text=True
    )
    # print("out1 msg: " + out1.stderr, flush=True)

    out2 = sp.run(
        [
            f"{binary_path}/magick",
            "compare",
            "-metric",
            "psnr",
            "-read-mask",
            f"{output_filename_psnr}",
            input_filename1,
            input_filename2,
            f"{mask_file_name}_psnr.png"  # f"hat_diff_{output_filename}
        ],
        capture_output=True, text=True
    )
    # print("out2 msg: " + out2.stderr, flush=True)

    # remove intermediate file
    sp.run(["rm", f"{output_filename_ssim}"])
    sp.run(["rm", f"{output_filename_psnr}"])
    sp.run(["rm", f"{mask_file_name}_ssim.png"])
    sp.run(["rm", f"{mask_file_name}_psnr.png"])
    return float(out1.stderr), float(out2.stderr)


############################################################################################################

def generate_png_from_ply(
        ply: str,  # ply file path
        point_size: float,  # default is 3
        saved_path: str
):
    pointcloud = o3d.io.read_point_cloud(ply)
    material = rendering.MaterialRecord()
    material.shader = "defaultUnlit"
    material.point_size = point_size

    render = rendering.OffscreenRenderer(2048, 2048, headless=True)
    # the last value is 'alpha', the transparency
    render.scene.set_background(np.array([0.5, 0.5, 0.5, 1.0]))
    render.scene.add_geometry("pcd", pointcloud, material)
    camera = 1500  # camera distance ; need to use 3000 for basketball & dancer
    # camera point to
    camera_point = pointcloud.get_axis_aligned_bounding_box().get_center()

    # we now render 6 images from +- xyz axis

    # right
    render.setup_camera(
        60, camera_point, camera_point + [camera, 0, 0],
        [0, 1, 0]
    )
    img = render.render_to_image()
    o3d.io.write_image(saved_path + "right.png", img, 9)

    # left
    render.setup_camera(
        60, camera_point, camera_point + [-camera, 0, 0],
        [0, 1, 0]
    )
    img = render.render_to_image()
    o3d.io.write_image(saved_path + "left.png", img, 9)

    # up
    render.setup_camera(
        60, camera_point, camera_point + [0, camera, 0],
        [0, 1, 0]
    )
    img = render.render_to_image()
    o3d.io.write_image(saved_path + "up.png", img, 9)

    # down
    render.setup_camera(
        60, camera_point, camera_point + [0, -camera, 0],
        [0, 1, 0]
    )
    img = render.render_to_image()
    o3d.io.write_image(saved_path + "down.png", img, 9)

    # front
    render.setup_camera(
        60, camera_point, camera_point + [0, 0, camera],
        [0, 1, 0]
    )
    img = render.render_to_image()
    o3d.io.write_image(saved_path + "front.png", img, 9)

    # back
    render.setup_camera(
        60, camera_point, camera_point + [0, 0, -camera],
        [0, 1, 0]
    )
    img = render.render_to_image()
    o3d.io.write_image(saved_path + "back.png", img, 9)
    # # note that the new rendering method may fail without err message
    # # I just retry until it success
    # while(os.path.getsize(filename_png + "006.png") < file_size):
    #    # just render again until success
    #    img = render.render_to_image()
    #    o3d.io.write_image(filename_png + "006.png", img, 9)
