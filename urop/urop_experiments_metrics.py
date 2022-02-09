# dyanmic_pc_data
# |
# |- longdress
# |   |- Ply
# |   |- experiments
# |       |- exp1
# |           |- compressed
# |           |- decompressed
# |           |- reconstructed
# |           |- metrics
# |
# |-loot
# |   |- Ply
# |   |- experiments
# |       |- exp1
# |           |- compressed
# |           |- decompressed
# |           |- reconstructed
# |           |- metrics
# |
# |- redandblack
# |   |- Ply
# |   |- experiments
# |       |- exp1
# |           |- compressed
# |           |- decompressed
# |           |- reconstructed
# |           |- metrics
# |
# |- solder
# |   |- Ply
# |   |- experiments
# |       |- exp1
# |           |- compressed
# |           |- decompressed
# |           |- reconstructed
# |           |- metrics

import logging
import yaml

from urop.experiments_params import *

if __name__ == '__main__':
    logging.basicConfig(filename="latest_run.log", level=logging.INFO)


    for dataset in datasets:
        #if experiments folder doesnt exist, create one for each dataset

        for experiment in experiments:
            #if particualar experiment folder doesnt exist, create it within the experiment folder

            # f'--uncompressedDataPath={dir + "/" + }',
            # f'--compressedStreamPath={bin_file}',
            # f'--reconstructedDataPath={rec_file}',
            execute_command(experiment["encode"]) #append the compressed & recondtructed & uncomrpessed paths to the command; internally, check for no. of plys in reconstructs vs raw || presence of bin?; define reconstruct path & compressed path internally, check if compressed & reconstruct folders alr exist

            logging.info("Ecnoding done for: ", experiment name, " for dataset: ", dataset)

            # f'--compressedStreamPath={bin_file}',
            # f'--reconstructedDataPath={rec_file}',
            execute_command(experiment["decode"]) #append the comrpessed & decompressed paths to the command. internally, check for no. of plys in decomrpessed vs raw ; define decomrpessed path & compressed path internally, check if decomrepssed folder alr exists

            logging.info("Decoding done for: ", experiment name, " for dataset: ", dataset)

            compute_metrics() #internally do ply_compare_multiple and summarize, since this is a fairly fast process, just delete all metric files in the folder and redo. if metrics folder doesnt exist, create it

            logging.info("Metrics computed and summarized for: ", experiment name, " for dataset: ", dataset)

            generate_indiv_charts() #generate charts for each quality metric against frame no. ; delete existing chart is exist then create new

            logging.info("Individual quality metric charts generated for : ", experiment name, " for dataset: ", dataset)

    # collate metrics into quality vs rate
    collate_quality_rate(datasets, experiments)  # check if chart alr exists, if yes then add to it, else create

    logging.info("Quality vs rate collated for: ", experiment name, " for dataset: ", dataset)

