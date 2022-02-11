# dyanmic_pc_data
# |- charts
# |
# |- longdress
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
import fnmatch
import subprocess as sp
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as mticker

def execute_encode(scope_curr_experiment_path, scope_experiment, scope_dataset_name):
    experiment_name = scope_experiment['name']

    compressed_path = os.path.join(scope_curr_experiment_path, "compressed")
    reconstructed_path = os.path.join(scope_curr_experiment_path, "reconstructed")
    uncompressed_path = os.path.join(dir, scope_dataset_name, "Ply")

    if not Path(compressed_path).is_dir():
        os.mkdir(compressed_path)

    if not Path(reconstructed_path).is_dir():
        os.mkdir(reconstructed_path)

    ply_count_reconstructed = len(fnmatch.filter(os.listdir(reconstructed_path), '*.ply'))
    ply_count_raw = len(fnmatch.filter(os.listdir(uncompressed_path), '*.ply'))

    # append uncompressed, reconstructed, compressed path to encode command => execute
    if ply_count_raw != ply_count_reconstructed:
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
    for f in os.listdir(metrics_path):
        os.remove(os.path.join(metrics_path, f))

    ply_compare_multiple_cmd = ['python3', 'ply_compare_multiple.py',
                                reference_path,
                                decompressed_path,
                                os.path.join(compressed_path, experiment_name + ".bin"),
                                metrics_path]

    sp.run(ply_compare_multiple_cmd)


def generate_indiv_charts(scope_curr_experiment_path, scope_experiment, scope_dataset_name):
    experiment_name = scope_experiment['name']

    metrics_path = os.path.join(scope_curr_experiment_path, "metrics/")
    indiv_charts_path = os.path.join(scope_curr_experiment_path, "charts/")

    if not Path(indiv_charts_path).is_dir():
        os.mkdir(indiv_charts_path)

    #open summary csv in metrics_path of the form <scope_dataset_name>_experiments_<experiment_name>_summary.csv
    #create chart for each column with y axis as metric, x axis as frame no. (based on star frame no.) => save in charts_path with name & chart title: <scope_dataset_name>_<experiment_name>_<metric>
    df = pd.read_csv(metrics_path + scope_dataset_name + "_experiments_" + experiment_name + "_summary.csv")
    df = df[['acd12_p2pt', 'acd21_p2pt', 'cd_p2pt', 'cdpsnr_p2pt', 'h_p2pt', 'y_cpsnr', 'u_cpsnr', 'v_cpsnr']]
    df['frame'] = df.index + int(start_frame_no[scope_dataset_name])
    df = df.set_index(['frame'])

    for metric in df.columns:
        #clear plot
        plt.clf()
        #set x axis to only show int
        plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(1))

        metric_name = metric_name_map[metric]
        y_points = df[metric].values
        x_points = df.index.values

        plt.title(scope_dataset_name + "_" + experiment_name + "_" + metric_name)
        plt.xlabel("Frame Number")
        plt.ylabel(metric_name)
        plt.plot(x_points, y_points, marker='.')
        plt.grid()
        plt.savefig(indiv_charts_path + scope_dataset_name + "_" + experiment_name + "_" + metric_name + ".png", bbox_inches='tight') #bbox prevents cutoff portions of image


def collate_quality_charts():
    #for each dataset, create new chart for quality metric, put all experiments wrt frame no. in the chart
    for dataset_name in datasets:
        charts_path = os.path.join(dir, dataset_name, "charts/")

        if not Path(charts_path).is_dir():
            os.mkdir(charts_path)

        for metric in metric_name_map.keys():
            metric_name = metric_name_map[metric]
            # clear plot
            plt.clf()
            # set x axis to only show int
            plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(1))
            plt.title(dataset_name + "_" + metric_name + "_combined")
            plt.xlabel("Frame Number")
            plt.ylabel(metric_name)

            #iterate through each experiment for the dataset_name, add to plot, use frame no. as index
            for experiment in experiments:
                experiments_path = os.path.join(dir, dataset_name, "experiments")
                curr_experiment_path = os.path.join(experiments_path, experiment['name'])
                metrics_path = os.path.join(curr_experiment_path, "metrics/")
                df = pd.read_csv(metrics_path + dataset_name + "_experiments_" + experiment['name'] + "_summary.csv")
                df['frame'] = df.index + int(start_frame_no[dataset_name])

                y_points = df[metric].values
                x_points = df['frame'].values

                plt.plot(x_points, y_points, marker='.', label=experiment['name'])
                plt.legend()
                plt.grid()

            plt.savefig(charts_path + "/" + dataset_name + "_" + metric_name + "_combined.png",
                        bbox_inches='tight')  # bbox prevents cutoff portions of image



if __name__ == '__main__':
    # logging.basicConfig(filename="latest_run.log", level=logging.INFO)

    for dataset_name in datasets:
        # if experiments folder doesnt exist, create one for each dataset
        experiments_path = os.path.join(dir, dataset_name, "experiments")
        if not Path(experiments_path).is_dir():
            os.mkdir(experiments_path)

        for experiment in experiments:
            # if particualar experiment folder doesnt exist, create it within the experiment folder
            curr_experiment_path = os.path.join(experiments_path, experiment['name'])
            if not Path(curr_experiment_path).is_dir():
                os.mkdir(curr_experiment_path)

            # f'--uncompressedDataPath={dir + "/" + }',
            # f'--compressedStreamPath={bin_file}',
            # f'--reconstructedDataPath={rec_file}',
            # startframenumber
            execute_encode(curr_experiment_path, experiment,
                           dataset_name)

            print("Encoding done for: ", experiment['name'], " for dataset: ", dataset_name)

            # f'--compressedStreamPath={bin_file}',
            # f'--reconstructedDataPath={rec_file}',
            # startframenumber
            execute_decode(curr_experiment_path, experiment,
                           dataset_name)

            print("Decoding done for: ", experiment['name'], " for dataset: ", dataset_name)

            compute_metrics(curr_experiment_path, experiment,
                            dataset_name)

            print("Metrics computed and summarized for: ", experiment['name'], " for dataset: ", dataset_name)

            generate_indiv_charts(curr_experiment_path, experiment,
                            dataset_name)

            print("Individual quality metric charts generated for : ", experiment['name'], " for dataset: ", dataset_name)


    collate_quality_charts()
    print("Generated collated quality metrics charts by dataset")
    #
    # # collate metrics into quality vs rate
    # collate_quality_rate(datasets, experiments)  # check if chart alr exists, if yes then add to it, else create
    #
    # print("Quality vs rate collated for: ", experiment['name'], " for dataset: ", dataset_name)
