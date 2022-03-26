import argparse

from algs_wrapper.VPCC import VPCC
import open3d as o3d
import os
import sys
import glob
from evaluator.summary import summarize_one_setup
import fnmatch
import multiprocessing
from joblib import Parallel, delayed
from urop.view_dependent_metrics import *
from pathlib import Path

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Wrapper for user to evaluate multiple pairs of point clouds.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        'ref_folder',
        help="The reference point cloud. Use point cloud with normal "
             "to calculate the p2plane metrics."
    )
    parser.add_argument(
        'target_folder',
        help="The target point cloud."
    )
    parser.add_argument(
        'target_bin',
        help="The bin of target point cloud."
    )
    parser.add_argument(
        'evl_log',
        help="Log file."
    )
    args = parser.parse_args()

    vpcc = VPCC()

    ##read in all paths of plys in ref_folder & target_folder in lists
    ref_pcs_path = []
    ref_pcs_name = []
    for root, dirs, files in os.walk(args.ref_folder):
        for file in files:
            if file.endswith('.ply'):
                ref_pcs_path.append(os.path.join(root, file))
                ref_pcs_name.append(file[:-4])

    target_pcs_path = []
    target_pcs_name = []
    for root, dirs, files in os.walk(args.target_folder):
        for file in files:
            if file.endswith('.ply'):
                target_pcs_path.append(os.path.join(root, file))
                target_pcs_name.append(file[:-4])

    # run loop of evaluate_and_log to generate set of log files

    if len(ref_pcs_path) < len(target_pcs_path):
        print("no. of reference plys are less than target plys")
        print("no. of reference plys: ", len(ref_pcs_path))
        print("no. of target plys: ", len(target_pcs_path))
        sys.exit()

    existing_log_files_count = len(fnmatch.filter(os.listdir(args.evl_log), '*.log'))
    # if (len(target_pcs_path) == existing_log_files_count):
    #     print("metric log files already exist")
    #     # summarize the log files into 1
    #     summarize_one_setup(args.evl_log, color=True)
    #     print("Completed summary of evaluation")
    #     sys.exit()

    ################################################################
    # generating the list of files is done out of order, need to sort
    ref_pcs_path.sort()
    ref_pcs_name.sort()
    target_pcs_path.sort()
    target_pcs_name.sort()
    ###############################################################

    if len(target_pcs_path) != existing_log_files_count:
        # del all log files
        existing_metric_files = glob.glob(args.evl_log + "/*.log")
        for f in existing_metric_files:
            os.remove(f)

        Parallel(n_jobs=30)(delayed(  # multiprocessing.cpu_count()
            vpcc._evaluate_and_log)(
            ref_pcfile=ref_pcs_path[i],
            target_pcfile=target_pcs_path[i],
            evl_log=args.evl_log + "metrics_" + ref_pcs_name[i] + "_" + target_pcs_name[i] + ".log",
            bin_file=args.target_bin)
                            for i in range(0, len(target_pcs_path)))
    ################################################################

    # for i in range(0, len(target_pcs_path)):
    #     vpcc._evaluate_and_log(
    #         ref_pcfile=ref_pcs_path[i],
    #         target_pcfile=target_pcs_path[i],
    #         evl_log=args.evl_log + "metrics_" + ref_pcs_name[i] + "_" + target_pcs_name[i] + ".log",
    #         bin_file=args.target_bin)

    ### Computing PSNR & SSIM ###
    existing_txt_count = len(fnmatch.filter(os.listdir(args.evl_log), '*.txt'))
    if len(target_pcs_path) != existing_txt_count:
        # for i in range(0, len(target_pcs_path)):
        #     view_dependent_metrics(ref_pcs_path[i], target_pcs_path[i], args.evl_log)

        # Parallel(n_jobs=30)(delayed(view_dependent_metrics)(ref_pcs_path[i], target_pcs_path[i], args.evl_log) for i in
        #                     range(0, len(target_pcs_path)))

        # pool = multiprocessing.Pool(processes=30)
        # for i in range(0, len(target_pcs_path)):
        #     pool.apply_async(view_dependent_metrics,
        #                      args=(ref_pcs_path[i], target_pcs_path[i], args.evl_log))
        with multiprocessing.Pool(processes=30) as pool:
            results = list(
                pool.apply_async(view_dependent_metrics, args=(ref_pcs_path[i], target_pcs_path[i], args.evl_log)) for i
                in range(0, len(target_pcs_path)))
            results = [r.get() for r in results]
        pool.close()
        pool.join()

        #multithread writing of 2D metrics to file
        Parallel(n_jobs=30)(delayed(write_metric_to_file)(
            args.evl_log + "metrics_" + ref_pcs_name[i] + "_" + target_pcs_name[i] + ".txt", results[i]) for i in
                            range(0, len(target_pcs_path)))

    print("Completed individual evaluation for frames")


############################################################################
    alg_name = Path(args.evl_log).parents[2].stem
    ds_name = Path(args.evl_log).parents[1].stem
    rate = Path(args.evl_log).parents[0].stem
    summary_csv = (
        Path(args.evl_log).joinpath(f'{alg_name}_{ds_name}_{rate}_summary.csv')
    )

    if not summary_csv.is_file():
        # del all csv files
        existing_metric_files = glob.glob(args.evl_log + "/*.csv")
        for f in existing_metric_files:
            os.remove(f)
        # summarize the log files into 1
        summarize_one_setup(args.evl_log, color=True)
    print("Completed summary of evaluation")
