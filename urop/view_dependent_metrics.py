import cv2 as cv
import subprocess as sp
import open3d as o3d  # 0.14.1, don't use 0.15
import open3d.visualization.rendering as rendering
import numpy as np
import os
magick_dir = '/temp/pranav/PCCArena/' + 'urop/'


def view_dependent_metrics(ref_pc_path, target_pc_path):
    ref_dir, ref_file_name = os.path.split(ref_pc_path)
    name_without_extension = os.path.splitext(ref_file_name)[0]
    subs = name_without_extension.split('_')
    name_without_extension = subs[0] + "_dec_" + subs[2]

    parent_ref_dir = os.path.abspath(os.path.join(ref_dir, '..'))
    ground_truth_path = os.path.join(parent_ref_dir, 'views/', name_without_extension)

    target_dir, target_file_name = os.path.split(target_pc_path)
    parent_target_dir = os.path.abspath(os.path.join(target_dir, '..'))
    target_path = os.path.join(parent_target_dir, 'views/', name_without_extension)

    # ground_truth_path AND target_path += 'up' down etc + '.png' ; then assign to vars
    temp_img_path_name = os.path.join(parent_target_dir, 'views/', name_without_extension + "_TEMP")

    ssim_up, psnr_up = caculate_metric_ignore_background(magick_dir, ground_truth_path + 'up.png',
                                                         target_path + 'up.png', temp_img_path_name)
    ssim_down, psnr_down = caculate_metric_ignore_background(magick_dir, ground_truth_path + 'down.png',
                                                             target_path + 'down.png', temp_img_path_name)
    ssim_left, psnr_left = caculate_metric_ignore_background(magick_dir, ground_truth_path + 'left.png',
                                                         target_path + 'left.png', temp_img_path_name)
    ssim_right, psnr_right = caculate_metric_ignore_background(magick_dir, ground_truth_path + 'right.png',
                                                         target_path + 'right.png', temp_img_path_name)
    ssim_front, psnr_front = caculate_metric_ignore_background(magick_dir, ground_truth_path + 'front.png',
                                                         target_path + 'front.png', temp_img_path_name)
    ssim_back, psnr_back = caculate_metric_ignore_background(magick_dir, ground_truth_path + 'back.png',
                                                         target_path + 'back.png', temp_img_path_name)

    return [f"SSIM up: {ssim_up}",
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
            "\n"]

    # return [f"Avg SSIM: {avg_ssim}",
    #         f"Avg PSNR: {avg_psnr}",
    #         "\n"]


def caculate_metric_ignore_background(
        binary_path: str,  # binary path of magick
        input_filename1: str,  # ground truth
        input_filename2: str,  # target
        mask_file_name: str  # tmp file name for mask background
):
    output_filename = f"{mask_file_name}_mask.png"

    img = cv.imread(input_filename1)
    rows, cols, _ = img.shape
    # Note that we assume two input files have the same dimension
    img2 = cv.imread(input_filename2)

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

    cv.imwrite(output_filename, img)  # output mask file
    out1 = sp.run(
        [
            f"{binary_path}/magick",
            "compare",
            "-metric",
            "ssim",
            "-read-mask",
            f"{output_filename}",
            input_filename1, input_filename2,
            f"hat_diff_{output_filename}"
        ], capture_output=True, text=True
    )
    out2 = sp.run(
        [
            f"{binary_path}/magick",
            "compare",
            "-metric",
            "psnr",
            "-read-mask",
            f"{output_filename}",
            input_filename1,
            input_filename2,
            f"hat_diff_{output_filename}"
        ],
        capture_output=True, text=True
    )
    # remove intermediate file
    sp.run(["rm", f"{output_filename}"])
    sp.run(["rm", f"hat_diff_{output_filename}"])
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
