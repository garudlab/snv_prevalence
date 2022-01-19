#!/bin/bash



#. /u/local/Modules/default/init/modules.sh
#module load python/2.7
# redo this one
# Bacteroides_ovatus_58035
declare -a all_species=('Alistipes_finegoldii_56071' 'Alistipes_onderdonkii_55464' 'Alistipes_putredinis_61533' 'Alistipes_shahii_62199' 'Bacteroidales_bacterium_58650' 'Bacteroides_caccae_53434' 'Bacteroides_cellulosilyticus_58046' 'Bacteroides_fragilis_54507' 'Bacteroides_ovatus_58035' 'Bacteroides_stercoris_56735' 'Bacteroides_thetaiotaomicron_56941' 'Bacteroides_uniformis_57318' 'Bacteroides_vulgatus_57955' 'Bacteroides_xylanisolvens_57185' 'Barnesiella_intestinihominis_62208' 'Dialister_invisus_61905' 'Eubacterium_rectale_56927' 'Oscillibacter_sp_60799' 'Parabacteroides_distasonis_56985' 'Parabacteroides_merdae_56972' 'Ruminococcus_bicirculans_59300' 'Ruminococcus_bromii_62047')


for species in "${all_species[@]}"
do
    echo "$species"
    qsub -N ${species} /u/home/w/wrshoema/project-ngarud/snv_prevalence/scripts/qsub_prevalence/qsub_predicted_prevalence.sh ${species}
done



#for species in "${all_species[@]}"
#do
#    echo "$species"
#    qsub -N ${species} /u/home/w/wrshoema/project-ngarud/snv_prevalence/scripts/qsub_prevalence/species/qsub_predicted_prevalence_${species}.sh
#done



#qsub -N Alistipes_finegoldii_56071 /u/home/w/wrshoema/project-ngarud/snv_prevalence/scripts/qsub_prevalence/qsub_predicted_prevalence.sh Alistipes_finegoldii_56071
# qrsh -l h_rt=3:00:00,h_data=24G


#qsub -N Bacteroides_vulgatus_57955 /u/home/w/wrshoema/project-ngarud/snv_prevalence/scripts/qsub_prevalence/qsub_predicted_prevalence.sh Bacteroides_vulgatus_57955

#qsub -N Alistipes_finegoldii_56071 /u/home/w/wrshoema/project-ngarud/snv_prevalence/scripts/qsub_prevalence/qsub_predicted_occupancy.sh Alistipes_finegoldii_56071
