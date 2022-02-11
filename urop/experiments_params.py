dir = '/mnt/d/NUS/Volumetric_Video_Streaming_UROP/dynamic_pc_data/'
VPCC_dir = '/mnt/c/Users/prana/My Documents/GitHub/mpeg-pcc-tmc2/'

datasets = ['longdress', 'loot', 'redandblack', 'soldier']
start_frame_no = {'longdress': '1051', 'loot': '1000', 'redandblack': '1450', 'soldier': '0536'}

metric_name_map = {'acd12_p2pt': 'Asym. Chamfer dist. (1->2) p2pt',
                   'acd21_p2pt': 'Asym. Chamfer dist. (2->1) p2pt',
                   'cd_p2pt': 'Chamfer dist. p2pt',
                   'cdpsnr_p2pt': 'CD-PSNR (dB) p2pt',
                   'h_p2pt': 'Hausdorff distance p2pt',
                   'y_cpsnr': 'Y-CPSNR (dB)',
                   'u_cpsnr': 'U-CPSNR (dB)',
                   'v_cpsnr': 'V-CPSNR (dB)'}

common_encode_cmd = ['./bin/PccAppEncoder',
                     '--configurationFolder=cfg/',
                     '--config=cfg/common/ctc-common.cfg',
                     '--config=cfg/condition/ctc-all-intra.cfg',
                     '--config=cfg/rate/ctc-r3.cfg',
                     '--nbThread=40',
                     '--colorTransform=0',
                     '--keepIntermediateFiles',
                     '--frameCount=2',
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
     'decode': common_decode_cmd
     },

    # 2DD
    {'name': '2DD_lodX=2_lodY=1_OM=4',
     'encode': common_encode_cmd + ['--levelOfDetailX=2', '--levelOfDetailY=1', '--occupancyPrecision=4'],
     'decode': common_decode_cmd
     },

    {'name': '2DD_lodX=2_lodY=1_OM=1',
     'encode': common_encode_cmd + ['--levelOfDetailX=2', '--levelOfDetailY=1', '--occupancyPrecision=1'],
     'decode': common_decode_cmd
     },

    # 3DD
    {'name': '3DD_2_noQuantize_OM=4',
     'encode': common_encode_cmd + ['--occupancyPrecision=4', '--threeDDPointsPerVoxel=2', '--threeDD'],
     'decode': common_decode_cmd
     },

    {'name': '3DD_2_Quantize=2_OM=4',
     'encode': common_encode_cmd +
               ['--occupancyPrecision=4', '--threeDDPointsPerVoxel=2', '--threeDD', '--downscalePC=2'],
     'decode': common_decode_cmd + ['--upscalePC=2']
     },

    {'name': '3DD_2_noQuantize_OM=1',
     'encode': common_encode_cmd + ['--occupancyPrecision=1', '--threeDDPointsPerVoxel=2', '--threeDD'],
     'decode': common_decode_cmd
     },

    {'name': '3DD_2_Quantize=2_OM=1',
     'encode': common_encode_cmd +
               ['--occupancyPrecision=1', '--threeDDPointsPerVoxel=2', '--threeDD', '--downscalePC=2'],
     'decode': common_decode_cmd + ['--upscalePC=2']
     }
]
