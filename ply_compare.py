from algs_wrapper.base import Base
import argparse
from evaluator.evaluator import Evaluator
from algs_wrapper.VPCC import VPCC

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="Wrapper for user to evaluate point clouds.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        'ref_pc',
        help="The reference point cloud. Use point cloud with normal "
             "to calculate the p2plane metrics."
    )
    parser.add_argument(
        'target_pc',
        help="The target point cloud."
    )
    parser.add_argument(
        'target_pc_bin',
        help="The bin of target point cloud."
    )
    parser.add_argument(
        'evl_log',
        help="Log file."
    )
    args = parser.parse_args()

    vpcc = VPCC()
    # eval._evaluate_and_log(
    #     ref_pcfile= "D:/NUS/Volumetric_Video_Streaming_UROP/test_data/reconstructed/test_rec_1051.ply",
    #     target_pcfile= "D:/NUS/Volumetric_Video_Streaming_UROP/test_data/reconstructed/test_rec_3DD_1051.ply",
    #     evl_log= "D:/NUS/Volumetric_Video_Streaming_UROP/test_data/reconstructed/rec_3DD_1051_CMP_rec_1051")

    vpcc._evaluate_and_log(
        ref_pcfile=args.ref_pc,
        target_pcfile=args.target_pc,
        evl_log=args.evl_log,
        bin_file=args.target_pc_bin)
