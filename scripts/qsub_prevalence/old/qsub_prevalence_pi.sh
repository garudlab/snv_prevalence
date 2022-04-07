#!/bin/bash
#$ -N prevalence_pi
#$ -e /u/project/ngarud/wrshoema/negative_selection_microbiome/scripts/prevalence_pi_error
#$ -o /u/project/ngarud/wrshoema/negative_selection_microbiome/scripts/prevalence_pi_output
#$ -l h_data=24G
#$ -l time=36:00:00
#$ -l highp
#$ -m bea

. /u/local/Modules/default/init/modules.sh

module unload python
#module load python/3.6.1
module load python/2.7.13

#python3 /u/project/ngarud/wrshoema/negative_selection_microbiome/scripts/calculate_linkage_disequilibria.py

#python3 /u/project/ngarud/wrshoema/negative_selection_microbiome/scripts/calculate_linkage_disequilibria.py --species Bacteroides_vulgatus_57955 --lower_threshold 0.5 --upper_threshold 0.7


python /u/project/ngarud/wrshoema/negative_selection_microbiome/scripts/loop_over_species_wrapper.py all python /u/project/ngarud/wrshoema/negative_selection_microbiome/scripts/calculate_pangenom_pi.py



#python loop_over_species_wrapper.py Bacteroides_vulgatus_57955 python calculate_per_gene_dnds.py
