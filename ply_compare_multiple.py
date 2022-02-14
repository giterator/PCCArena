import argparse

from algs_wrapper.VPCC import VPCC

import os
import sys
import glob
from evaluator.summary import summarize_one_setup
import fnmatch
import multiprocessing
from joblib import Parallel, delayed

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
    if (len(target_pcs_path) == existing_log_files_count):
        print("metric log files already exist")
        # summarize the log files into 1
        summarize_one_setup(args.evl_log, color=True)
        print("Completed summary of evaluation")
        sys.exit()

    existing_metric_files = glob.glob(args.evl_log + "/*")

    for f in existing_metric_files:
        os.remove(f)

    ################################################################
    #generating the list of files is done out of order, need to sort
    ref_pcs_path.sort()
    ref_pcs_name.sort()
    target_pcs_path.sort()
    target_pcs_name.sort()
    # Parallel run of evaluate_and_log => UNTESTED
    Parallel(n_jobs=multiprocessing.cpu_count())(delayed(
        vpcc._evaluate_and_log(
            ref_pcfile=ref_pcs_path[i],
            target_pcfile=target_pcs_path[i],
            evl_log=args.evl_log + "metrics_" + ref_pcs_name[i] + "_" + target_pcs_name[i] + ".log",
            bin_file=args.target_bin)
        for i in range(0, len(target_pcs_path))))
    ################################################################

    for i in range(0, len(target_pcs_path)):
        vpcc._evaluate_and_log(
            ref_pcfile=ref_pcs_path[i],
            target_pcfile=target_pcs_path[i],
            evl_log=args.evl_log + "metrics_" + ref_pcs_name[i] + "_" + target_pcs_name[i] + ".log",
            bin_file=args.target_bin)

        print("Completed individual evaluation for frames: ", ref_pcs_name[i], " and ", target_pcs_name[i])

    # summarize the log files into 1
    summarize_one_setup(args.evl_log, color=True)
    print("Completed summary of evaluation")
