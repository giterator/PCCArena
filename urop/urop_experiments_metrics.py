# dyanmic_pc_data
# |- charts
# |
# |- longdress
# |   |-charts
# |   |- Ply
# |   |- experiments
# |       |- exp1
# |           |- compressed
# |           |- decompressed
# |           |- reconstructed
# |           |- metrics
# |           |-charts
# |
# |-loot
# |   |-charts
# |   |- Ply
# |   |- experiments
# |       |- exp1
# |           |- compressed
# |           |- decompressed
# |           |- reconstructed
# |           |- metrics
# |           |-charts
# |
# |- redandblack
# |   |-charts
# |   |- Ply
# |   |- experiments
# |       |- exp1
# |           |- compressed
# |           |- decompressed
# |           |- reconstructed
# |           |- metrics
# |           |-charts
# |
# |- solder
# |   |-charts
# |   |- Ply
# |   |- experiments
# |       |- exp1
# |           |- compressed
# |           |- decompressed
# |           |- reconstructed
# |           |- metrics
# |           |-charts

# import logging
from pathlib import Path
import os
from experiments_params import *
from view_dependent_metrics import *

import fnmatch
import subprocess as sp
import matplotlib.pyplot as plt
import pandas as pd

import matplotlib.ticker as mticker
import matplotlib.path as mpath
from matplotlib.lines import Line2D

import multiprocessing
from joblib import Parallel, delayed
import numpy as np
import shutil
from adjustText import adjust_text


def execute_encode(scope_curr_experiment_path, scope_experiment, scope_dataset_name):
    experiment_name = scope_experiment['name']

    compressed_path = os.path.join(scope_curr_experiment_path, "compressed")
    reconstructed_path = os.path.join(scope_curr_experiment_path, "reconstructed")
    uncompressed_path = os.path.join(dir, scope_dataset_name, "Ply")

    if not Path(compressed_path).is_dir():
        os.mkdir(compressed_path)

    if not Path(reconstructed_path).is_dir():
        os.mkdir(reconstructed_path)

    # ply_count_reconstructed = len(fnmatch.filter(os.listdir(reconstructed_path), '*.ply'))
    # ply_count_raw = len(fnmatch.filter(os.listdir(uncompressed_path), '*.ply'))

    # append uncompressed, reconstructed, compressed path to encode command => execute
    bin_name = os.path.join(compressed_path, experiment_name + '.bin')
    if not Path(bin_name).is_file():  # ply_count_raw != ply_count_reconstructed:
        # del contents of reconstructed & compressed
        for f in os.listdir(compressed_path):
            os.remove(os.path.join(compressed_path, f))

        for f in os.listdir(reconstructed_path):
            os.remove(os.path.join(reconstructed_path, f))

        uncompressed_param = "--uncompressedDataPath=" + os.path.join(uncompressed_path,
                                                                      scope_dataset_name + "_vox10_%04d.ply")
        compressed_param = "--compressedStreamPath=" + os.path.join(compressed_path, experiment_name + ".bin")
        reconstructed_param = "--reconstructedDataPath=" + os.path.join(reconstructed_path,
                                                                        scope_dataset_name + "_rec_%04d.ply")

        start_frame_param = '--startFrameNumber=' + start_frame_no[scope_dataset_name]

        command = scope_experiment['encode'] + [start_frame_param, reconstructed_param, compressed_param,
                                                uncompressed_param]
        sp.run(command, cwd=VPCC_dir)


def execute_decode(scope_curr_experiment_path, scope_experiment, scope_dataset_name):
    experiment_name = scope_experiment['name']

    compressed_path = os.path.join(scope_curr_experiment_path, "compressed")
    decompressed_path = os.path.join(scope_curr_experiment_path, "decompressed")
    uncompressed_path = os.path.join(dir, scope_dataset_name, "Ply")

    if not Path(decompressed_path).is_dir():
        os.mkdir(decompressed_path)

    ply_count_decompressed = len(fnmatch.filter(os.listdir(decompressed_path), '*.ply'))
    ply_count_raw = len(fnmatch.filter(os.listdir(uncompressed_path), '*.ply'))

    if ply_count_raw != ply_count_decompressed:
        # del contents of decompressed
        for f in os.listdir(decompressed_path):
            os.remove(os.path.join(decompressed_path, f))

        compressed_param = "--compressedStreamPath=" + os.path.join(compressed_path, experiment_name + ".bin")
        decompressed_param = "--reconstructedDataPath=" + os.path.join(decompressed_path,
                                                                       scope_dataset_name + "_dec_%04d.ply")
        start_frame_param = '--startFrameNumber=' + start_frame_no[scope_dataset_name]

        command = scope_experiment['decode'] + [start_frame_param, decompressed_param, compressed_param]
        sp.run(command, cwd=VPCC_dir)


def compute_metrics(scope_curr_experiment_path, scope_experiment, scope_dataset_name):
    experiment_name = scope_experiment['name']

    metrics_path = os.path.join(scope_curr_experiment_path, "metrics/")
    compressed_path = os.path.join(scope_curr_experiment_path, "compressed")
    decompressed_path = os.path.join(scope_curr_experiment_path, "decompressed")
    reference_path = os.path.join(dir, scope_dataset_name, "Ply/")

    if not Path(metrics_path).is_dir():
        os.mkdir(metrics_path)
    # for f in os.listdir(metrics_path):
    #     os.remove(os.path.join(metrics_path, f))

    ply_compare_multiple_cmd = ['python3', 'ply_compare_multiple.py',
                                reference_path,
                                decompressed_path,
                                os.path.join(compressed_path, experiment_name + ".bin"),
                                metrics_path]

    sp.run(ply_compare_multiple_cmd, cwd=PCCArena_dir)


def generate_indiv_charts(scope_curr_experiment_path, scope_experiment, scope_dataset_name):
    experiment_name = scope_experiment['name']

    metrics_path = os.path.join(scope_curr_experiment_path, "metrics/")
    indiv_charts_path = os.path.join(scope_curr_experiment_path, "charts/")

    if not Path(indiv_charts_path).is_dir():
        os.mkdir(indiv_charts_path)
    for f in os.listdir(indiv_charts_path):
        os.remove(os.path.join(indiv_charts_path, f))

    # open summary csv in metrics_path of the form <scope_dataset_name>_experiments_<experiment_name>_summary.csv
    # create chart for each column with y axis as metric, x axis as frame no. (based on star frame no.) => save in charts_path with name & chart title: <scope_dataset_name>_<experiment_name>_<metric>
    df = pd.read_csv(metrics_path + scope_dataset_name + "_experiments_" + experiment_name + "_summary.csv")
    # df = df[['acd12_p2pt', 'acd21_p2pt', 'cd_p2pt', 'cdpsnr_p2pt', 'h_p2pt', 'y_cpsnr', 'u_cpsnr', 'v_cpsnr']]
    df = df[list(metric_name_map.keys())]
    # df['frame'] = df.index + int(start_frame_no[scope_dataset_name])
    # df = df.set_index(['frame'])
    #
    for metric in df.columns:
        # clear plot
        plt.clf()
        plt.figure(figsize=(20, 8))
        # set x axis to only show int
        plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(1))
        #
        metric_name = metric_name_map[metric]
        y_points = df[metric].values
        x_points = np.arange(start=1, stop=len(y_points) + 1, step=1)
        #
        plt.title(scope_dataset_name + "_" + experiment_name + "_" + metric_name)
        plt.xlabel("Frame Number")
        plt.ylabel(metric_name)
        plt.plot(x_points, y_points, marker='.')
        plt.grid()
        plt.xticks(x_points[::5], rotation='vertical')
        plt.savefig(indiv_charts_path + scope_dataset_name + "_" + experiment_name + "_" + metric_name + ".png",
                    bbox_inches='tight')  # bbox prevents cutoff portions of image


def collate_quality_charts_only_quantize():
    # for each dataset, create new chart for quality metric, put all experiments wrt frame no. in the chart
    for dataset_name in datasets:
        charts_path = os.path.join(dir, dataset_name, "charts/")
        #
        # if not Path(charts_path).is_dir():
        #     os.mkdir(charts_path)
        # for f in os.listdir(charts_path):
        #     os.remove(os.path.join(charts_path, f))
        #
        for metric in metric_name_map.keys():
            metric_name = metric_name_map[metric]
            # clear plot
            plt.clf()
            plt.figure(figsize=(20, 5))
            # set x axis to only show int
            plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(1))
            plt.title(dataset_name + "_" + metric_name + "_combined_quantize")
            plt.xlabel("Frame Number")
            plt.ylabel(metric_name)
            #
            # iterate through each experiment for the dataset_name, add to plot, use frame no. as index
            for experiment in experiments:
                if "_Quantize=" in experiment['name'] and dataset_name in experiment['data']:
                    experiments_path = os.path.join(dir, dataset_name, "experiments")
                    curr_experiment_path = os.path.join(experiments_path, experiment['name'])
                    metrics_path = os.path.join(curr_experiment_path, "metrics/")
                    df = pd.read_csv(
                        metrics_path + dataset_name + "_experiments_" + experiment['name'] + "_summary.csv")
                    df['frame'] = df.index + int(start_frame_no[dataset_name])
                    #
                    y_points = df[metric].values
                    x_points = np.arange(start=1, stop=len(y_points) + 1, step=1)
                    #
                    plt.plot(x_points, y_points, marker='.', label=experiment['name'])
                    # plt.legend()
                    plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
                    plt.grid()
                #
            plt.xticks(x_points[::5], rotation='vertical')
            plt.savefig(charts_path + "/" + dataset_name + "_" + metric_name + "_combined_quantize.png",
                        bbox_inches='tight')  # bbox prevents cutoff portions of image


def collate_quality_charts_without_quantize():
    # for each dataset, create new chart for quality metric, put all experiments wrt frame no. in the chart
    for dataset_name in datasets:
        charts_path = os.path.join(dir, dataset_name, "charts/")
        #
        if not Path(charts_path).is_dir():
            os.mkdir(charts_path)
        for f in os.listdir(charts_path):
            os.remove(os.path.join(charts_path, f))
        #
        for metric in metric_name_map.keys():
            metric_name = metric_name_map[metric]
            # clear plot
            plt.clf()
            plt.figure(figsize=(20, 5))
            # set x axis to only show int
            plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(1))
            plt.title(dataset_name + "_" + metric_name + "_combined_without_quantize")
            plt.xlabel("Frame Number")
            plt.ylabel(metric_name)
            #
            # iterate through each experiment for the dataset_name, add to plot, use frame no. as index
            for experiment in experiments:
                if "_Quantize=" not in experiment['name'] and dataset_name in experiment['data']:
                    experiments_path = os.path.join(dir, dataset_name, "experiments")
                    curr_experiment_path = os.path.join(experiments_path, experiment['name'])
                    metrics_path = os.path.join(curr_experiment_path, "metrics/")
                    df = pd.read_csv(
                        metrics_path + dataset_name + "_experiments_" + experiment['name'] + "_summary.csv")
                    df['frame'] = df.index + int(start_frame_no[dataset_name])
                    #
                    y_points = df[metric].values
                    x_points = np.arange(start=1, stop=len(y_points) + 1, step=1)
                    #
                    plt.plot(x_points, y_points, marker='.', label=experiment['name'])
                    # plt.legend()
                    plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
                    plt.grid()
                #
            plt.xticks(x_points[::5], rotation='vertical')
            plt.savefig(charts_path + "/" + dataset_name + "_" + metric_name + "_combined_without_quantize.png",
                        bbox_inches='tight')  # bbox prevents cutoff portions of image


def collate_quality_charts():
    # for each dataset, create new chart for quality metric, put all experiments wrt frame no. in the chart
    for dataset_name in datasets:
        charts_path = os.path.join(dir, dataset_name, "charts/")
        #
        if not Path(charts_path).is_dir():
            os.mkdir(charts_path)
        for f in os.listdir(charts_path):
            os.remove(os.path.join(charts_path, f))
        #
        for metric in metric_name_map.keys():
            metric_name = metric_name_map[metric]
            # clear plot
            plt.clf()
            plt.figure(figsize=(20, 5))
            # set x axis to only show int
            plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(1))
            plt.title(dataset_name + "_" + metric_name + "_combined")
            plt.xlabel("Frame Number")
            plt.ylabel(metric_name)
            #
            # iterate through each experiment for the dataset_name, add to plot, use frame no. as index
            for experiment in experiments:
                experiments_path = os.path.join(dir, dataset_name, "experiments")
                curr_experiment_path = os.path.join(experiments_path, experiment['name'])
                metrics_path = os.path.join(curr_experiment_path, "metrics/")
                df = pd.read_csv(metrics_path + dataset_name + "_experiments_" + experiment['name'] + "_summary.csv")
                df['frame'] = df.index + int(start_frame_no[dataset_name])
                #
                y_points = df[metric].values
                x_points = np.arange(start=1, stop=len(y_points) + 1, step=1)
                #
                plt.plot(x_points, y_points, marker='.', label=experiment['name'])
                # plt.legend()
                plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
                plt.grid()
                #
            plt.xticks(x_points[::5], rotation='vertical')
            plt.savefig(charts_path + "/" + dataset_name + "_" + metric_name + "_combined.png",
                        bbox_inches='tight')  # bbox prevents cutoff portions of image


def collate_quality_rate():
    charts_path = os.path.join(dir, "charts/")

    if Path(charts_path).is_dir():
        shutil.rmtree(charts_path)

    if not Path(charts_path).is_dir():
        os.mkdir(charts_path)

    # compute list of <dataset>_<experiment name> : bin_size
    exp_size = {}
    for dataset_name in datasets:
        experiments_path = os.path.join(dir, dataset_name, "experiments")

        dataset_charts_path = os.path.join(charts_path, dataset_name + '/')
        if not Path(dataset_charts_path).is_dir():
            os.mkdir(dataset_charts_path)
        for f in os.listdir(dataset_charts_path):
            os.remove(os.path.join(dataset_charts_path, f))

        for experiment in experiments:
            ##########################################################
            if dataset_name in experiment['data']:
                ##########################################################
                curr_experiment_path = os.path.join(experiments_path, experiment['name'])
                compressed_path = os.path.join(curr_experiment_path, "compressed")
                bin_path = os.path.join(compressed_path, experiment['name'] + ".bin")
                # Getting size in MB
                bin_size = os.path.getsize(bin_path) / (1024.0 * 1024.0)
                # Convert size to 3 decimal places
                # bin_size = "{:.3f}".format(bin_size)
                #
                exp_size[dataset_name + "_" + experiment['name']] = bin_size
    #

    # for combined experiments
    # for metric in metric_name_map.keys():
    #     metric_name = metric_name_map[metric]
    #     for dataset_name in datasets:
    #         dataset_charts_path = os.path.join(charts_path, dataset_name + '/')
    #         # clear plot
    #         plt.clf()
    #         plt.title(dataset_name + "_" + metric_name + "_VS_rate")
    #         plt.xlabel("Rate (MB)")
    #         plt.ylabel(metric_name)
    #         texts = []
    #         #
    #         experiments_path = os.path.join(dir, dataset_name, "experiments")
    #         for experiment in experiments:
    #             curr_experiment_path = os.path.join(experiments_path, experiment['name'])
    #             metrics_path = os.path.join(curr_experiment_path, "metrics/")
    #             df = pd.read_csv(metrics_path + dataset_name + "_experiments_" + experiment['name'] + "_summary.csv")
    #             #
    #             avg_metric = df[metric].mean()
    #             bin_size = exp_size[dataset_name + "_" + experiment['name']]
    #             #add point to scatter plot
    #             plt.scatter(bin_size, avg_metric, label=experiment['name'], marker=experiment['marker'], edgecolors=experiment['edgecolors'], facecolors=experiment['facecolors'])
    #             # annotate points
    #             texts.append(plt.annotate("(" + str(int(bin_size)) + "," + str(np.format_float_positional(avg_metric, precision=3)) + ")", (bin_size, avg_metric)))
    #
    #         plt.grid()
    #         plt.legend()
    #         adjust_text(texts)
    #         #save plot
    #         plt.savefig(dataset_charts_path + dataset_name + "_" + metric_name + "_VS_rate.png", bbox_inches='tight')  # bbox prevents cutoff portions of image

    # splitting OM=1 & OM=4 charts
    for metric in metric_name_map.keys():
        metric_name = metric_name_map[metric]
        for dataset_name in datasets:
            dataset_charts_path = os.path.join(charts_path, dataset_name + '/')
            # clear plot
            plt.clf()
            #
            plt.figure(figsize=(20, 5))
            #
            plt.title(dataset_name + "_" + metric_name + "_VS_rate")
            plt.xlabel("Rate (MB)")
            plt.ylabel(metric_name)
            texts = []
            #
            experiments_path = os.path.join(dir, dataset_name, "experiments")
            for experiment in experiments:
                if 'OM=1' in experiment['name'] and dataset_name in experiment['data']:
                    curr_experiment_path = os.path.join(experiments_path, experiment['name'])
                    metrics_path = os.path.join(curr_experiment_path, "metrics/")
                    df = pd.read_csv(
                        metrics_path + dataset_name + "_experiments_" + experiment['name'] + "_summary.csv")
                    #
                    avg_metric = df[metric].mean()
                    bin_size = exp_size[dataset_name + "_" + experiment['name']]
                    # add point to scatter plot
                    plt.scatter(bin_size, avg_metric, label=experiment['name'], marker=experiment['marker'],
                                edgecolors=experiment['edgecolors'], facecolors=experiment['facecolors'])
                    # annotate points
                    texts.append(plt.annotate("(" + str(np.format_float_positional(bin_size, precision=3)) + "," + str(
                        np.format_float_positional(avg_metric, precision=3)) + ")", (bin_size, avg_metric)))

            #
            plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
            #
            plt.grid()

            adjust_text(texts)
            # save plot
            plt.savefig(dataset_charts_path + dataset_name + "_" + metric_name + "_VS_rate_OM=1.png",
                        bbox_inches='tight')  # bbox prevents cutoff portions of image

    for metric in metric_name_map.keys():
        metric_name = metric_name_map[metric]
        for dataset_name in datasets:
            dataset_charts_path = os.path.join(charts_path, dataset_name + '/')
            # clear plot
            plt.clf()
            #
            plt.figure(figsize=(20, 7))
            #
            plt.title(dataset_name + "_" + metric_name + "_VS_rate")
            plt.xlabel("Rate (MB)")
            plt.ylabel(metric_name)
            texts = []
            #
            experiments_path = os.path.join(dir, dataset_name, "experiments")
            for experiment in experiments:
                if ('OM=4' in experiment['name'] and dataset_name in experiment['data']) or experiment[
                    'name'] == 'vanilla_r2' or experiment['name'] == 'vanilla_r1':
                    curr_experiment_path = os.path.join(experiments_path, experiment['name'])
                    metrics_path = os.path.join(curr_experiment_path, "metrics/")
                    df = pd.read_csv(
                        metrics_path + dataset_name + "_experiments_" + experiment['name'] + "_summary.csv")
                    #
                    avg_metric = df[metric].mean()
                    bin_size = exp_size[dataset_name + "_" + experiment['name']]
                    # add point to scatter plot
                    ##################################################
                    label_name = experiment['name']
                    if label_name == 'vanilla_OM=4':
                        label_name = 'vanilla_r3_GQP=24_AQP=32'
                    elif label_name == 'vanilla_r2':
                        label_name = 'vanilla_r2_GQP=28_AQP=37'
                    elif label_name == 'vanilla_r1':
                        label_name = 'vanilla_r1_GQP=32_AQP=42'
                    elif label_name == '2DD_lodX=2_lodY=1_OM=4' or label_name == '2DD_lodX=1_lodY=2_OM=4' \
                            or label_name == '2DD_lodX=2_lodY=2_OM=4' or label_name == '3DD_2_noQuantize_OM=4' \
                            or label_name == '3DD_2_Quantize=2_OM=4' or label_name == '3DD_4_noQuantize_OM=4':
                        label_name = label_name + '_R3'
                    ##################################################
                    plt.scatter(bin_size, avg_metric, label=label_name, marker=experiment['marker'],
                                edgecolors=experiment['edgecolors'], facecolors=experiment['facecolors'])
                    # annotate points
                    texts.append(plt.annotate("(" + str(np.format_float_positional(bin_size, precision=3)) + "," + str(
                        np.format_float_positional(avg_metric, precision=3)) + ")", (bin_size, avg_metric)))

            #
            plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
            #
            plt.grid()

            adjust_text(texts)
            # save plot
            plt.savefig(dataset_charts_path + dataset_name + "_" + metric_name + "_VS_rate_OM=4.png",
                        bbox_inches='tight')  # bbox prevents cutoff portions of image


def single_vpcc_experiment(experiments_path, experiment, dataset_name):
    #############################################################################
    if dataset_name not in experiment['data']:
        return
    #############################################################################

    # if particualar experiment folder doesnt exist, create it within the experiment folder
    curr_experiment_path = os.path.join(experiments_path, experiment['name'])
    if not Path(curr_experiment_path).is_dir():
        os.mkdir(curr_experiment_path)

    execute_encode(curr_experiment_path, experiment,
                   dataset_name)

    print("Encoding done for: ", experiment['name'], " for dataset: ", dataset_name)

    execute_decode(curr_experiment_path, experiment,
                   dataset_name)

    print("Decoding done for: ", experiment['name'], " for dataset: ", dataset_name)


def vpcc_compute(dataset_name):
    experiments_path = os.path.join(dir, dataset_name, "experiments")
    if not Path(experiments_path).is_dir():
        os.mkdir(experiments_path)

    # Parallel(n_jobs=30)(delayed(
    #     single_vpcc_experiment)(experiments_path, experiment, dataset_name)
    #                     for experiment in experiments)

    pool = multiprocessing.Pool(processes=10)
    for experiment in experiments:
        pool.apply(single_vpcc_experiment, (experiments_path, experiment, dataset_name))
    # pool.apply_async(runBamHashWorker, (element, ))
    pool.close()
    pool.join()


if __name__ == '__main__':
    # logging.basicConfig(filename="latest_run.log", level=logging.INFO)

    ###########################################################################################
    pool = multiprocessing.Pool(processes=30)
    # pool.map(vpcc_compute, datasets)

    # with multiprocessing.Pool(processes=30) as pool:
    #     for dataset_name in datasets:
    #         pool.apply_async(vpcc_compute, args=dataset_name)
    # pool.close()
    # pool.join()

    for dataset_name in datasets:
        # if experiments folder doesnt exist, create one for each dataset
        experiments_path = os.path.join(dir, dataset_name, "experiments")
        if not Path(experiments_path).is_dir():
            os.mkdir(experiments_path)

        #############################################
        # Parallel(n_jobs=multiprocessing.cpu_count())(delayed(
        #     single_vpcc_experiment)(experiments_path, experiment, dataset_name)
        #     for experiment in experiments)
        for experiment in experiments:
            pool.apply_async(single_vpcc_experiment, (experiments_path, experiment, dataset_name))
    pool.close()
    pool.join()

    ###########################################################################################

    # Compute and store screenshots of 6 views of all PCs
    # for reference plys
    for dataset_name in datasets:
        ply_dir = os.path.join(dir, dataset_name, "Ply")
        view_dir = os.path.join(dir, dataset_name, "views")
        if not Path(view_dir).is_dir():
            os.mkdir(view_dir)
        num_views = len(fnmatch.filter(os.listdir(view_dir), '*.png'))
        num_ref = len(fnmatch.filter(os.listdir(ply_dir), '*.ply'))

        if num_views != 6 * num_ref:
            for f in os.listdir(view_dir):
                os.remove(os.path.join(view_dir, f))
            ##
            Parallel(n_jobs=30)(delayed(  # multiprocessing.cpu_count()
                generate_png_from_ply)(os.path.join(ply_dir, ply), 3, os.path.join(view_dir, os.path.splitext(ply)[0]))
                                for ply in os.listdir(ply_dir))
            # for ply in os.listdir(ply_dir):
            #     generate_png_from_ply(ply, "3", os.path.join(view_dir, os.path.splitext(ply)[0]))

    # for decompressed plys
    for dataset_name in datasets:
        experiments_path = os.path.join(dir, dataset_name, "experiments")
        for experiment in experiments:
            ##########################################################
            if dataset_name in experiment['data']:
                ##########################################################
                curr_experiment_path = os.path.join(experiments_path, experiment['name'])
                ply_dir = os.path.join(curr_experiment_path, "decompressed")
                view_dir = os.path.join(curr_experiment_path, "views")
                if not Path(view_dir).is_dir():
                    os.mkdir(view_dir)
                # num_views = len(fnmatch.filter(os.listdir(view_dir), '*.png'))
                # num_ref = len(fnmatch.filter(os.listdir(ply_dir), '*.ply'))

                summary_metrics_path = os.path.join(curr_experiment_path, 'metrics',
                                                    dataset_name + "_" + "experiments" + "_" + experiment[
                                                        'name'] + "_summary.csv")

                if not Path(summary_metrics_path).is_file():  # num_views != 6 * num_ref:
                    print("gnerating view pngs for: ", dataset_name, experiment['name'], flush=True)
                    for f in os.listdir(view_dir):
                        os.remove(os.path.join(view_dir, f))
                    ##
                    Parallel(n_jobs=30)(delayed(  # multiprocessing.cpu_count()
                        generate_png_from_ply)(os.path.join(ply_dir, ply), 3,
                                               os.path.join(view_dir, os.path.splitext(ply)[0]))
                                        for ply in os.listdir(ply_dir))

    # Compute metrics after VPCC is done for all experiments
    for dataset_name in datasets:
        experiments_path = os.path.join(dir, dataset_name, "experiments")
        for experiment in experiments:
            ##########################################################
            if dataset_name in experiment['data']:
                ##########################################################
                curr_experiment_path = os.path.join(experiments_path, experiment['name'])
                compute_metrics(curr_experiment_path, experiment,
                                dataset_name)

                print("Metrics computed and summarized for: ", experiment['name'], " for dataset: ", dataset_name)

                generate_indiv_charts(curr_experiment_path, experiment,
                                      dataset_name)

                print("Individual quality metric charts generated for : ", experiment['name'], " for dataset: ",
                      dataset_name)

    # collate_quality_charts()
    collate_quality_charts_without_quantize()
    collate_quality_charts_only_quantize()
    print("Generated collated quality metrics charts by dataset")
    #
    # collate metrics into quality vs rate
    collate_quality_rate()

    print("Quality vs rate collated for all datasets")
