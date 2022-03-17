# dir = '/mnt/d/NUS/Volumetric_Video_Streaming_UROP/dynamic_pc_data/'
# VPCC_dir = '/mnt/c/Users/prana/My Documents/GitHub/mpeg-pcc-tmc2/'
# PCCArena_dir ='/mnt/d/NUS/Volumetric_Video_Streaming_UROP/PCCArena/'

# dir = '/home/p/pranav/dynamic_pc_data/'
# VPCC_dir = '/home/p/pranav/mpeg-pcc-tmc2/'
# PCCArena_dir = '/home/p/pranav/PCCArena/'

import matplotlib.path as mpath
from matplotlib.lines import Line2D

dir = '/temp/pranav/dynamic_pc_data/'
VPCC_dir = '/temp/pranav/mpeg-pcc-tmc2/'
PCCArena_dir = '/temp/pranav/PCCArena/'
magick_dir = PCCArena_dir + 'urop/'

datasets = ['longdress', 'loot', 'redandblack', 'soldier']
start_frame_no = {'longdress': '1051', 'loot': '1000', 'redandblack': '1450', 'soldier': '0536'}

metric_name_map = {'acd12_p2pt': 'Asym. Chamfer dist. (1-2) p2pt',
                   'acd21_p2pt': 'Asym. Chamfer dist. (2-1) p2pt',
                   'cd_p2pt': 'Chamfer dist. p2pt',
                   'cdpsnr_p2pt': 'CD-PSNR (dB) p2pt',
                   'h_p2pt': 'Hausdorff distance p2pt',
                   'y_cpsnr': 'Y-CPSNR (dB)',
                   'u_cpsnr': 'U-CPSNR (dB)',
                   'v_cpsnr': 'V-CPSNR (dB)',
                   ##############################################2D metrics######################################################
                   'ssim_up': 'SSIM up',
                   'ssim_down': 'SSIM down',
                   'ssim_left': 'SSIM left',
                   'ssim_right': 'SSIM right',
                   'ssim_front': 'SSIM front',
                   'ssim_back': 'SSIM back',

                   'psnr_up': 'PSNR up',
                   'psnr_down': 'PSNR down',
                   'psnr_left': 'PSNR left',
                   'psnr_right': 'PSNR right',
                   'psnr_front': 'PSNR front',
                   'psnr_back': 'PSNR back',
                   # 'ssim': 'Avg SSIM',
                   # 'psnr': 'Avg PSNR'
                   }

common_encode_cmd = ['./bin/PccAppEncoder',
                     '--configurationFolder=cfg/',
                     '--config=cfg/common/ctc-common.cfg',
                     '--config=cfg/condition/ctc-all-intra.cfg',
                     '--config=cfg/rate/ctc-r3.cfg',
                     '--nbThread=10',
                     '--colorTransform=0',
                     '--keepIntermediateFiles',
                     '--frameCount=300',
                     '--computeChecksum=0',
                     '--computeMetrics=0'
                     ]

common_decode_cmd = ['./bin/PccAppDecoder',
                     '--nbThread=40',
                     '--inverseColorSpaceConversionConfig=cfg/hdrconvert/yuv420torgb444.cfg',
                     '--colorTransform=0',
                     '--computeMetrics=0',
                     '--computeChecksum=0',
                     '--keepIntermediateFiles',
                     ]

# array of dicts where each dict has 3 keys: folder name, encoder command, decoder command
experiments = [
    # vanilla
    {'name': 'vanilla_OM=4',
     'encode': common_encode_cmd + ['--occupancyPrecision=4'],
     'decode': common_decode_cmd,

     'marker': 'o',
     'facecolors': 'blue',
     'edgecolors': 'blue'
     },

    # 2DD
    {'name': '2DD_lodX=2_lodY=1_OM=4',
     'encode': common_encode_cmd + ['--levelOfDetailX=2', '--levelOfDetailY=1', '--occupancyPrecision=4'],
     'decode': common_decode_cmd,

     'marker': 's',
     'facecolors': 'orange',
     'edgecolors': 'orange'
     },

    {'name': '2DD_lodX=2_lodY=1_OM=1',
     'encode': common_encode_cmd + ['--levelOfDetailX=2', '--levelOfDetailY=1', '--occupancyPrecision=1'],
     'decode': common_decode_cmd,

     'marker': 's',
     'facecolors': 'orange',
     'edgecolors': 'orange'
     },

    {'name': '2DD_lodX=1_lodY=2_OM=4',
     'encode': common_encode_cmd + ['--levelOfDetailX=1', '--levelOfDetailY=2', '--occupancyPrecision=4'],
     'decode': common_decode_cmd,

     'marker': 'D',
     'facecolors': 'orange',
     'edgecolors': 'orange'
     },

    {'name': '2DD_lodX=1_lodY=2_OM=1',
     'encode': common_encode_cmd + ['--levelOfDetailX=1', '--levelOfDetailY=2', '--occupancyPrecision=1'],
     'decode': common_decode_cmd,

     'marker': 'D',
     'facecolors': 'orange',
     'edgecolors': 'orange'
     },
    #############################################################
    {'name': '2DD_lodX=2_lodY=2_OM=4',
     'encode': common_encode_cmd + ['--levelOfDetailX=2', '--levelOfDetailY=2', '--occupancyPrecision=4'],
     'decode': common_decode_cmd,

     'marker': mpath.Path.unit_regular_star(8),
     'facecolors': 'none',
     'edgecolors': 'orange'
     },

    {'name': '2DD_lodX=2_lodY=2_OM=1',
     'encode': common_encode_cmd + ['--levelOfDetailX=2', '--levelOfDetailY=2', '--occupancyPrecision=1'],
     'decode': common_decode_cmd,

     'marker': mpath.Path.unit_regular_star(8),
     'facecolors': 'none',
     'edgecolors': 'orange'
     },
    #############################################################

    # 3DD
    {'name': '3DD_2_noQuantize_OM=4',
     'encode': common_encode_cmd + ['--occupancyPrecision=4', '--threeDDPointsPerVoxel=2', '--threeDD'],
     'decode': common_decode_cmd,

     'marker': '^',
     'facecolors': 'red',
     'edgecolors': 'red'
     },

    {'name': '3DD_2_Quantize=2_OM=4',
     'encode': common_encode_cmd +
               ['--occupancyPrecision=4', '--threeDDPointsPerVoxel=2', '--threeDD', '--downscalePC=2'],
     'decode': common_decode_cmd + ['--upscalePC=2'],

     'marker': 'v',
     'facecolors': 'red',
     'edgecolors': 'red'
     },

    {'name': '3DD_2_noQuantize_OM=1',
     'encode': common_encode_cmd + ['--occupancyPrecision=1', '--threeDDPointsPerVoxel=2', '--threeDD'],
     'decode': common_decode_cmd,

     'marker': '^',
     'facecolors': 'red',
     'edgecolors': 'red'
     },

    {'name': '3DD_2_Quantize=2_OM=1',
     'encode': common_encode_cmd +
               ['--occupancyPrecision=1', '--threeDDPointsPerVoxel=2', '--threeDD', '--downscalePC=2'],
     'decode': common_decode_cmd + ['--upscalePC=2'],

     'marker': 'v',
     'facecolors': 'red',
     'edgecolors': 'red'
     },
    ########################################################
    {'name': '3DD_4_noQuantize_OM=4',
     'encode': common_encode_cmd + ['--occupancyPrecision=4', '--threeDDPointsPerVoxel=4', '--threeDD'],
     'decode': common_decode_cmd,

     'marker': '^',
     'facecolors': 'none',
     'edgecolors': 'red'
     },
    {'name': '3DD_4_noQuantize_OM=1',
     'encode': common_encode_cmd + ['--occupancyPrecision=1', '--threeDDPointsPerVoxel=4', '--threeDD'],
     'decode': common_decode_cmd,

     'marker': '^',
     'facecolors': 'none',
     'edgecolors': 'red'
     }
    #########################################################
]
