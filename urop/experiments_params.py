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

datasets = ['longdress', 'loot', 'redandblack']  # , 'soldier']
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
                   # 'ssim_up': 'SSIM up',
                   # 'ssim_down': 'SSIM down',
                   # 'ssim_left': 'SSIM left',
                   # 'ssim_right': 'SSIM right',
                   'ssim_front': 'SSIM front',
                   # 'ssim_back': 'SSIM back',

                   # 'psnr_up': 'PSNR up',
                   # 'psnr_down': 'PSNR down',
                   # 'psnr_left': 'PSNR left',
                   # 'psnr_right': 'PSNR right',
                   'psnr_front': 'PSNR front',
                   # 'psnr_back': 'PSNR back',
                   #
                   # 'avg_ssim': 'Avg SSIM',
                   # 'avg_psnr': 'Avg PSNR'
                   }

common_encode_cmd = ['./bin/PccAppEncoder',
                     '--configurationFolder=cfg/',
                     '--config=cfg/common/ctc-common.cfg',
                     '--config=cfg/condition/ctc-all-intra.cfg',
                     '--config=cfg/rate/ctc-r3.cfg',
                     '--nbThread=10',
                     '--colorTransform=0',
                     # '--keepIntermediateFiles',
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
                     # '--keepIntermediateFiles',
                     ]

# array of dicts where each dict has 3 keys: folder name, encoder command, decoder command
experiments = [
    # # vanilla r3
    # {'name': 'vanilla_OM=4',
    #  'encode': common_encode_cmd + ['--occupancyPrecision=4'],
    #  'decode': common_decode_cmd,
    #
    #  'marker': 'o',
    #  'facecolors': 'black',
    #  'edgecolors': 'black',
    #  'data': datasets
    #  },
    #
    # # vanilla r2
    # {'name': 'vanilla_r2',
    #  'encode': common_encode_cmd + ['--occupancyPrecision=4', '--config=cfg/rate/ctc-r2.cfg'],
    #  'decode': common_decode_cmd,
    #
    #  'marker': 's',
    #  'facecolors': 'black',
    #  'edgecolors': 'black',
    #  'data': datasets
    #  },

    # vanilla r1
    {'name': 'vanilla_r1',
     'encode': common_encode_cmd + ['--occupancyPrecision=4', '--config=cfg/rate/ctc-r1.cfg', '--minimumImageWidth=512',
                                    '--minimumImageHeight=512'],
     'decode': common_decode_cmd,

     'marker': '^',
     'facecolors': 'black',
     'edgecolors': 'black',
     'data': datasets,
     'label': 'HEVC R1 GQP=32 AQP=42'
     },

    ###########
    # vanilla RC
    {'name': 'vanilla_rc_OM=4_GQP=36_AQP=47',
     'encode': common_encode_cmd + ['--occupancyPrecision=4', '--geometryQP=36', '--attributeQP=47',
                                    '--minimumImageWidth=512', '--minimumImageHeight=512'],
     'decode': common_decode_cmd,

     'marker': '*',
     'facecolors': 'black',
     'edgecolors': 'black',
     'data': datasets,
     'label': 'HEVC GQP=36 AQP=47'
     },

    # vanilla RC
    {'name': 'vanilla_rc_OM=4_GQP=40_AQP=52',
     'encode': common_encode_cmd + ['--occupancyPrecision=4', '--geometryQP=40', '--attributeQP=52',
                                    '--minimumImageWidth=512', '--minimumImageHeight=512'],
     'decode': common_decode_cmd,

     'marker': 'p',
     'facecolors': 'black',
     'edgecolors': 'black',
     'data': datasets,
     'label': 'HEVC GQP=40 AQP=52'
     },
    ######################

    # # vanilla RC
    # {'name': 'vanilla_rc_OM=4_GQP=27_AQP=35',
    #  'encode': common_encode_cmd + ['--occupancyPrecision=4', '--geometryQP=27', '--attributeQP=35'],
    #  'decode': common_decode_cmd,
    #
    #  'marker': '*',
    #  'facecolors': 'blue',
    #  'edgecolors': 'blue',
    #  'data': datasets
    #  },
    # #########################################################################
    # # vanilla RC
    # {'name': 'vanilla_rc_OM=4_GQP=26_AQP=34',
    #  'encode': common_encode_cmd + ['--occupancyPrecision=4', '--geometryQP=26', '--attributeQP=34'],
    #  'decode': common_decode_cmd,
    #
    #  'marker': 'p',
    #  'facecolors': 'blue',
    #  'edgecolors': 'blue',
    #  'data': datasets
    #  },
    # # vanilla RC
    # {'name': 'vanilla_rc_OM=4_GQP=26_AQP=35',
    #  'encode': common_encode_cmd + ['--occupancyPrecision=4', '--geometryQP=26', '--attributeQP=35'],
    #  'decode': common_decode_cmd,
    #
    #  'marker': 'P',
    #  'facecolors': 'blue',
    #  'edgecolors': 'blue',
    #  'data': datasets
    #  },
    # # vanilla RC
    # {'name': 'vanilla_rc_OM=4_GQP=27_AQP=34',
    #  'encode': common_encode_cmd + ['--occupancyPrecision=4', '--geometryQP=27', '--attributeQP=34'],
    #  'decode': common_decode_cmd,
    #
    #  'marker': 'X',
    #  'facecolors': 'blue',
    #  'edgecolors': 'blue',
    #  'data': datasets
    #  },
    # #####################################################################
    # # vanilla RC
    # {'name': 'vanilla_rc_OM=4_GQP=28_AQP=33',
    #  'encode': common_encode_cmd + ['--occupancyPrecision=4', '--geometryQP=28', '--attributeQP=33'],
    #  'decode': common_decode_cmd,
    #
    #  'marker': '>',
    #  'facecolors': 'blue',
    #  'edgecolors': 'blue',
    #  'data': ['longdress']
    #  },
    #
    # # vanilla RC
    # {'name': 'vanilla_rc_OM=4_GQP=27_AQP=33',
    #  'encode': common_encode_cmd + ['--occupancyPrecision=4', '--geometryQP=27', '--attributeQP=33'],
    #  'decode': common_decode_cmd,
    #
    #  'marker': 'D',
    #  'facecolors': 'blue',
    #  'edgecolors': 'blue',
    #  'data': ['longdress']
    #  },
    #
    # # vanilla RC
    # {'name': 'vanilla_rc_OM=4_GQP=25_AQP=33',
    #  'encode': common_encode_cmd + ['--occupancyPrecision=4', '--geometryQP=25', '--attributeQP=33'],
    #  'decode': common_decode_cmd,
    #
    #  'marker': '<',
    #  'facecolors': 'blue',
    #  'edgecolors': 'blue',
    #  'data': ['loot', 'soldier']
    #  },
    #
    # # vanilla RC
    # {'name': 'vanilla_rc_OM=4_GQP=26_AQP=32',
    #  'encode': common_encode_cmd + ['--occupancyPrecision=4', '--geometryQP=26', '--attributeQP=32'],
    #  'decode': common_decode_cmd,
    #
    #  'marker': 'v',
    #  'facecolors': 'blue',
    #  'edgecolors': 'blue',
    #  'data': ['redandblack']
    #  },
    #
    # # vanilla RC
    # {'name': 'vanilla_rc_OM=4_GQP=26_AQP=33',
    #  'encode': common_encode_cmd + ['--occupancyPrecision=4', '--geometryQP=26', '--attributeQP=33'],
    #  'decode': common_decode_cmd,
    #
    #  'marker': 'o',
    #  'facecolors': 'blue',
    #  'edgecolors': 'blue',
    #  'data': ['redandblack']
    #  },
    #
    # # vanilla RC
    # {'name': 'vanilla_rc_OM=4_GQP=30_AQP=38',
    #  'encode': common_encode_cmd + ['--occupancyPrecision=4', '--geometryQP=30', '--attributeQP=38'],
    #  'decode': common_decode_cmd,
    #
    #  'marker': '^',
    #  'facecolors': 'blue',
    #  'edgecolors': 'blue',
    #  'data': ['longdress', 'soldier']
    #  },
    #
    # # vanilla RC
    # {'name': 'vanilla_rc_OM=4_GQP=29_AQP=39',
    #  'encode': common_encode_cmd + ['--occupancyPrecision=4', '--geometryQP=29', '--attributeQP=39'],
    #  'decode': common_decode_cmd,
    #
    #  'marker': 'D',
    #  'facecolors': 'blue',
    #  'edgecolors': 'blue',
    #  'data': ['loot']
    #  },
    #
    # # vanilla RC
    # {'name': 'vanilla_rc_OM=4_GQP=25_AQP=34',
    #  'encode': common_encode_cmd + ['--occupancyPrecision=4', '--geometryQP=25', '--attributeQP=34'],
    #  'decode': common_decode_cmd,
    #
    #  'marker': 's',
    #  'facecolors': 'blue',
    #  'edgecolors': 'blue',
    #  'data': ['loot']
    #  },
    #
    # # vanilla RC
    # {'name': 'vanilla_rc_OM=4_GQP=32_AQP=40',
    #  'encode': common_encode_cmd + ['--occupancyPrecision=4', '--geometryQP=32', '--attributeQP=40'],
    #  'decode': common_decode_cmd,
    #
    #  'marker': mpath.Path.unit_regular_star(8),
    #  'facecolors': 'blue',
    #  'edgecolors': 'blue',
    #  'data': ['redandblack']
    #  },
    # ########################################################################
    # # vanilla RC
    # {'name': 'vanilla_rc_OM=4_GQP=32_AQP=38',
    #  'encode': common_encode_cmd + ['--occupancyPrecision=4', '--geometryQP=32', '--attributeQP=38'],
    #  'decode': common_decode_cmd,
    #
    #  'marker': 'P',
    #  'facecolors': 'green',
    #  'edgecolors': 'green',
    #  'data': ['longdress']
    #  },
    #
    # # vanilla RC
    # {'name': 'vanilla_rc_OM=4_GQP=30_AQP=41',
    #  'encode': common_encode_cmd + ['--occupancyPrecision=4', '--geometryQP=30', '--attributeQP=41'],
    #  'decode': common_decode_cmd,
    #
    #  'marker': 'p',
    #  'facecolors': 'green',
    #  'edgecolors': 'green',
    #  'data': ['loot']
    #  },
    #
    # # vanilla RC
    # {'name': 'vanilla_rc_OM=4_GQP=32_AQP=39',
    #  'encode': common_encode_cmd + ['--occupancyPrecision=4', '--geometryQP=32', '--attributeQP=39'],
    #  'decode': common_decode_cmd,
    #
    #  'marker': 's',
    #  'facecolors': 'green',
    #  'edgecolors': 'green',
    #  'data': ['soldier']
    #  },
    #####################################################################
    # # R3
    # # 2DD
    # {'name': '2DD_lodX=2_lodY=1_OM=4',
    #  'encode': common_encode_cmd + ['--levelOfDetailX=2', '--levelOfDetailY=1', '--occupancyPrecision=4'],
    #  'decode': common_decode_cmd,
    #
    #  'marker': 's',
    #  'facecolors': 'orange',
    #  'edgecolors': 'orange',
    #  'data': datasets
    #  },
    #
    # # R3
    # {'name': '2DD_lodX=2_lodY=1_OM=1',
    #  'encode': common_encode_cmd + ['--levelOfDetailX=2', '--levelOfDetailY=1', '--occupancyPrecision=1'],
    #  'decode': common_decode_cmd,
    #
    #  'marker': 's',
    #  'facecolors': 'orange',
    #  'edgecolors': 'orange',
    #  'data': datasets
    #  },
    #
    # # R3
    # {'name': '2DD_lodX=1_lodY=2_OM=4',
    #  'encode': common_encode_cmd + ['--levelOfDetailX=1', '--levelOfDetailY=2', '--occupancyPrecision=4'],
    #  'decode': common_decode_cmd,
    #
    #  'marker': 'D',
    #  'facecolors': 'orange',
    #  'edgecolors': 'orange',
    #  'data': datasets
    #  },
    #
    # # R3
    # {'name': '2DD_lodX=1_lodY=2_OM=1',
    #  'encode': common_encode_cmd + ['--levelOfDetailX=1', '--levelOfDetailY=2', '--occupancyPrecision=1'],
    #  'decode': common_decode_cmd,
    #
    #  'marker': 'D',
    #  'facecolors': 'orange',
    #  'edgecolors': 'orange',
    #  'data': datasets
    #  },
    # #############################################################
    # # R3
    # {'name': '2DD_lodX=2_lodY=2_OM=4',
    #  'encode': common_encode_cmd + ['--levelOfDetailX=2', '--levelOfDetailY=2', '--occupancyPrecision=4'],
    #  'decode': common_decode_cmd,
    #
    #  'marker': mpath.Path.unit_regular_star(8),
    #  'facecolors': 'none',
    #  'edgecolors': 'orange',
    #  'data': datasets
    #  },
    #
    # # R3
    # {'name': '2DD_lodX=2_lodY=2_OM=1',
    #  'encode': common_encode_cmd + ['--levelOfDetailX=2', '--levelOfDetailY=2', '--occupancyPrecision=1'],
    #  'decode': common_decode_cmd,
    #
    #  'marker': mpath.Path.unit_regular_star(8),
    #  'facecolors': 'none',
    #  'edgecolors': 'orange',
    #  'data': datasets
    #  },
    # #############################################################
    #
    # # 3DD
    # # R3
    # {'name': '3DD_2_noQuantize_OM=4',
    #  'encode': common_encode_cmd + ['--occupancyPrecision=4', '--threeDDPointsPerVoxel=2', '--threeDD'],
    #  'decode': common_decode_cmd,
    #
    #  'marker': '^',
    #  'facecolors': 'red',
    #  'edgecolors': 'red',
    #  'data': datasets
    #  },
    #
    # # R3
    # {'name': '3DD_2_Quantize=2_OM=4',
    #  'encode': common_encode_cmd +
    #            ['--occupancyPrecision=4', '--threeDDPointsPerVoxel=2', '--threeDD', '--downscalePC=2'],
    #  'decode': common_decode_cmd + ['--upscalePC=2'],
    #
    #  'marker': 'v',
    #  'facecolors': 'red',
    #  'edgecolors': 'red',
    #  'data': datasets
    #  },
    #
    # # R3
    # {'name': '3DD_2_noQuantize_OM=1',
    #  'encode': common_encode_cmd + ['--occupancyPrecision=1', '--threeDDPointsPerVoxel=2', '--threeDD'],
    #  'decode': common_decode_cmd,
    #
    #  'marker': '^',
    #  'facecolors': 'red',
    #  'edgecolors': 'red',
    #  'data': datasets
    #  },
    #
    # # R3
    # {'name': '3DD_2_Quantize=2_OM=1',
    #  'encode': common_encode_cmd +
    #            ['--occupancyPrecision=1', '--threeDDPointsPerVoxel=2', '--threeDD', '--downscalePC=2'],
    #  'decode': common_decode_cmd + ['--upscalePC=2'],
    #
    #  'marker': 'v',
    #  'facecolors': 'red',
    #  'edgecolors': 'red',
    #  'data': datasets
    #  },
    # ########################################################
    # # R3
    # {'name': '3DD_4_noQuantize_OM=4',
    #  'encode': common_encode_cmd + ['--occupancyPrecision=4', '--threeDDPointsPerVoxel=4', '--threeDD'],
    #  'decode': common_decode_cmd,
    #
    #  'marker': '^',
    #  'facecolors': 'none',
    #  'edgecolors': 'red',
    #  'data': datasets
    #  },
    # # R3
    # {'name': '3DD_4_noQuantize_OM=1',
    #  'encode': common_encode_cmd + ['--occupancyPrecision=1', '--threeDDPointsPerVoxel=4', '--threeDD'],
    #  'decode': common_decode_cmd,
    #
    #  'marker': '^',
    #  'facecolors': 'none',
    #  'edgecolors': 'red',
    #  'data': datasets
    #  },
    ########################################################
    # R1 2DD
    # {'name': '2DD_lodX=2_lodY=1_OM=4_r1',
    #  'encode': common_encode_cmd + ['--levelOfDetailX=2', '--levelOfDetailY=1', '--occupancyPrecision=4',
    #                                 '--config=cfg/rate/ctc-r1.cfg', '--minimumImageWidth=512', '--minimumImageHeight=512'],
    #  'decode': common_decode_cmd,
    #
    #  'marker': 's',
    #  'facecolors': 'cyan',
    #  'edgecolors': 'cyan',
    #  'data': datasets
    #  },
    #
    # {'name': '2DD_lodX=1_lodY=2_OM=4_r1',
    #  'encode': common_encode_cmd + ['--levelOfDetailX=1', '--levelOfDetailY=2', '--occupancyPrecision=4',
    #                                 '--config=cfg/rate/ctc-r1.cfg', '--minimumImageWidth=512', '--minimumImageHeight=512'],
    #  'decode': common_decode_cmd,
    #
    #  'marker': 'D',
    #  'facecolors': 'cyan',
    #  'edgecolors': 'cyan',
    #  'data': datasets
    #  },
    #
    # {'name': '2DD_lodX=2_lodY=2_OM=4_r1',
    #  'encode': common_encode_cmd + ['--levelOfDetailX=2', '--levelOfDetailY=2', '--occupancyPrecision=4',
    #                                 '--config=cfg/rate/ctc-r1.cfg', '--minimumImageWidth=512', '--minimumImageHeight=512'],
    #  'decode': common_decode_cmd,
    #
    #  'marker': mpath.Path.unit_regular_star(8),
    #  'facecolors': 'none',
    #  'edgecolors': 'cyan',
    #  'data': datasets
    #  },

    # R1 3DD
    {'name': '3DD_2_noQuantize_OM=4_r1',
     'encode': common_encode_cmd + ['--occupancyPrecision=4', '--threeDDPointsPerVoxel=2', '--threeDD',
                                    '--config=cfg/rate/ctc-r1.cfg', '--minimumImageWidth=512',
                                    '--minimumImageHeight=512'],
     'decode': common_decode_cmd,

     'marker': '^',
     'facecolors': 'magenta',
     'edgecolors': 'magenta',
     'data': datasets,
     'label': '3DD R1 Downsample=2'
     },

    {'name': '3DD_2_Quantize=2_OM=4_r1',
     'encode': common_encode_cmd +
               ['--occupancyPrecision=4', '--threeDDPointsPerVoxel=2', '--threeDD', '--downscalePC=2',
                '--config=cfg/rate/ctc-r1.cfg', '--minimumImageWidth=512', '--minimumImageHeight=512'],
     'decode': common_decode_cmd + ['--upscalePC=2'],

     'marker': 'v',
     'facecolors': 'magenta',
     'edgecolors': 'magenta',
     'data': datasets,
     'label': '3DD R1 Downsample=2 ScaleGeometry=2'
     },

    {'name': '3DD_4_noQuantize_OM=4_r1',
     'encode': common_encode_cmd + ['--occupancyPrecision=4', '--threeDDPointsPerVoxel=4', '--threeDD',
                                    '--config=cfg/rate/ctc-r1.cfg', '--minimumImageWidth=512',
                                    '--minimumImageHeight=512'],
     'decode': common_decode_cmd,

     'marker': '^',
     'facecolors': 'none',
     'edgecolors': 'magenta',
     'data': datasets,
     'label': '3DD R1 Downsample=4'
     },
    #########################################################

    # R1 2DD WITH INTERPOLATE
    {'name': '2DD_INT_lodX=2_lodY=1_OM=4_r1',
     'encode': common_encode_cmd + ['--levelOfDetailX=2', '--levelOfDetailY=1', '--occupancyPrecision=4',
                                    '--config=cfg/rate/ctc-r1.cfg', '--minimumImageWidth=512',
                                    '--minimumImageHeight=512'],
     'decode': common_decode_cmd + ['--int2DD'],

     'marker': 's',
     'facecolors': 'yellow',
     'edgecolors': 'yellow',
     'data': datasets,
     'label': '2DD R1 DownsampleX=2'
     },

    {'name': '2DD_INT_lodX=1_lodY=2_OM=4_r1',
     'encode': common_encode_cmd + ['--levelOfDetailX=1', '--levelOfDetailY=2', '--occupancyPrecision=4',
                                    '--config=cfg/rate/ctc-r1.cfg', '--minimumImageWidth=512',
                                    '--minimumImageHeight=512'],
     'decode': common_decode_cmd + ['--int2DD'],

     'marker': 'D',
     'facecolors': 'yellow',
     'edgecolors': 'yellow',
     'data': ['longdress', 'redandblack'],  # , 'soldier'] #LOOT CAUSES SEG FAULT when decoding WHY???
     'label': '2DD R1 DownsampleY=2'
     },

    {'name': '2DD_INT_lodX=2_lodY=2_OM=4_r1',
     'encode': common_encode_cmd + ['--levelOfDetailX=2', '--levelOfDetailY=2', '--occupancyPrecision=4',
                                    '--config=cfg/rate/ctc-r1.cfg', '--minimumImageWidth=512',
                                    '--minimumImageHeight=512'],
     'decode': common_decode_cmd + ['--int2DD'],

     'marker': mpath.Path.unit_regular_star(8),
     'facecolors': 'none',
     'edgecolors': 'yellow',
     'data': datasets,
     'label': '2DD R1 DownsampleX=2 DownsampleY=2'
     },
    ##########
    # # R2 2DD WITH INTERPOLATE
    # {'name': '2DD_INT_lodX=2_lodY=1_OM=4_r2',
    #  'encode': common_encode_cmd + ['--levelOfDetailX=2', '--levelOfDetailY=1', '--occupancyPrecision=4',
    #                                 '--config=cfg/rate/ctc-r2.cfg'], #, '--minimumImageWidth=1', '--minimumImageHeight=1'],
    #  'decode': common_decode_cmd + ['--int2DD'],
    #
    #  'marker': 's',
    #  'facecolors': 'magenta',
    #  'edgecolors': 'magenta',
    #  'data': datasets
    #  },
    #
    # {'name': '2DD_INT_lodX=1_lodY=2_OM=4_r2',
    #  'encode': common_encode_cmd + ['--levelOfDetailX=1', '--levelOfDetailY=2', '--occupancyPrecision=4',
    #                                 '--config=cfg/rate/ctc-r2.cfg'], # '--minimumImageWidth=1', '--minimumImageHeight=1'],
    #  'decode': common_decode_cmd + ['--int2DD'],
    #
    #  'marker': 'D',
    #  'facecolors': 'magenta',
    #  'edgecolors': 'magenta',
    #  'data': datasets
    #  },
    #
    # {'name': '2DD_INT_lodX=2_lodY=2_OM=4_r2',
    #  'encode': common_encode_cmd + ['--levelOfDetailX=2', '--levelOfDetailY=2', '--occupancyPrecision=4',
    #                                 '--config=cfg/rate/ctc-r2.cfg'], # '--minimumImageWidth=1', '--minimumImageHeight=1'],
    #  'decode': common_decode_cmd + ['--int2DD'],
    #
    #  'marker': mpath.Path.unit_regular_star(8),
    #  'facecolors': 'none',
    #  'edgecolors': 'magenta',
    #  'data': datasets
    #  },
    # ##########

    # # R3  2DD WITH INTERPOLATE
    # {'name': '2DD_INT_lodX=2_lodY=1_OM=4_r3',
    #  'encode': common_encode_cmd + ['--levelOfDetailX=2', '--levelOfDetailY=1', '--occupancyPrecision=4'], #'--minimumImageWidth=1', '--minimumImageHeight=1'],
    #  'decode': common_decode_cmd + ['--int2DD'],
    #
    #  'marker': 's',
    #  'facecolors': 'green',
    #  'edgecolors': 'green',
    #  'data': datasets
    #  },
    #
    # {'name': '2DD_INT_lodX=1_lodY=2_OM=4_r3',
    #  'encode': common_encode_cmd + ['--levelOfDetailX=1', '--levelOfDetailY=2', '--occupancyPrecision=4'], #'--minimumImageWidth=1', '--minimumImageHeight=1'],
    #  'decode': common_decode_cmd + ['--int2DD'],
    #
    #  'marker': 'D',
    #  'facecolors': 'green',
    #  'edgecolors': 'green',
    #  'data': datasets
    #  },
    #
    # {'name': '2DD_INT_lodX=2_lodY=2_OM=4_r3',
    #  'encode': common_encode_cmd + ['--levelOfDetailX=2', '--levelOfDetailY=2', '--occupancyPrecision=4'], #'--minimumImageWidth=1', '--minimumImageHeight=1'],
    #  'decode': common_decode_cmd + ['--int2DD'],
    #
    #  'marker': mpath.Path.unit_regular_star(8),
    #  'facecolors': 'none',
    #  'edgecolors': 'green',
    #  'data': datasets
    #  },
    #
    #
    # # R2 2DD
    # {'name': '2DD_lodX=2_lodY=1_OM=4_r2',
    #  'encode': common_encode_cmd + ['--levelOfDetailX=2', '--levelOfDetailY=1', '--occupancyPrecision=4',
    #                                 '--config=cfg/rate/ctc-r2.cfg'],
    #  'decode': common_decode_cmd,
    #
    #  'marker': 's',
    #  'facecolors': 'red',
    #  'edgecolors': 'red',
    #  'data': datasets
    #  },
    #
    # {'name': '2DD_lodX=1_lodY=2_OM=4_r2',
    #  'encode': common_encode_cmd + ['--levelOfDetailX=1', '--levelOfDetailY=2', '--occupancyPrecision=4',
    #                                 '--config=cfg/rate/ctc-r2.cfg'],
    #  'decode': common_decode_cmd,
    #
    #  'marker': 'D',
    #  'facecolors': 'red',
    #  'edgecolors': 'red',
    #  'data': datasets
    #  },
    #
    # {'name': '2DD_lodX=2_lodY=2_OM=4_r2',
    #  'encode': common_encode_cmd + ['--levelOfDetailX=2', '--levelOfDetailY=2', '--occupancyPrecision=4',
    #                                 '--config=cfg/rate/ctc-r2.cfg'],
    #  'decode': common_decode_cmd,
    #
    #  'marker': mpath.Path.unit_regular_star(8),
    #  'facecolors': 'none',
    #  'edgecolors': 'red',
    #  'data': datasets
    #  },
]
