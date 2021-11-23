from __future__ import division
import sys
import numpy
import pickle
import bz2
import gzip
import config
import math
import os.path

import diversity_utils
import figure_utils
import parse_midas_data

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.gridspec as gridspec

from scipy.stats import gamma, gaussian_kde

import calculate_predicted_prevalence_mapgd

data_directory = config.data_directory
allowed_variant_types = set(['1D','4D'])

#clade_types = ['all','largest_clade', 'no_strains']
#clade_types = ['just_strains']

#clade_type = 'all'

#prevalence_dict = calculate_predicted_prevalence_mapgd.load_predicted_prevalence_subsample_dict()
prevalence_dict_mapgd = calculate_predicted_prevalence_mapgd.load_predicted_prevalence_dict_all()


species_list = list(prevalence_dict_mapgd.keys())
species_list.sort()

n_species_row=5

nested_species_list = [species_list[x:x+n_species_row] for x in range(0, len(species_list), n_species_row)]


def make_plot(clade_type, pi_type, variant_type='4D'):

    gs = gridspec.GridSpec(nrows=len(nested_species_list), ncols=2*n_species_row)
    fig = plt.figure(figsize = (40, 20))

    #mre_all = []

    for column_idx, column in enumerate(nested_species_list):

        for row_idx, row in enumerate(column):

            ax = fig.add_subplot(gs[column_idx, row_idx])

            #prevalence_dict_mapgd[species_name][clade_type][pi_type][location_aa_i]
            predicted_prevalence = prevalence_dict_mapgd[row][clade_type][pi_type][variant_type]['predicted_prevalence_mapgd']
            predicted_prevalence = numpy.asarray(predicted_prevalence)

            observed_prevalence = prevalence_dict_mapgd[row][clade_type][pi_type][variant_type]['observed_prevalence_mapgd']
            observed_prevalence = numpy.asarray(observed_prevalence)

            f_max = prevalence_dict_mapgd[row][clade_type][pi_type][variant_type]['f_max_mapgd']
            f_max = numpy.asarray(f_max)

            predicted_prevalence_no_zeros = predicted_prevalence[(observed_prevalence>0) & (predicted_prevalence>0) & (f_max<1.0) ]
            observed_prevalence_no_zeros = observed_prevalence[(observed_prevalence>0) & (predicted_prevalence>0) & (f_max<1.0) ]
            f_max_no_zeros = f_max[(observed_prevalence>0) & (predicted_prevalence>0) & (f_max<1.0) ]


            predicted_prevalence_all = prevalence_dict_mapgd[row][clade_type][pi_type][variant_type]['predicted_prevalence_all']
            predicted_prevalence_all = numpy.asarray(predicted_prevalence_all)

            observed_prevalence_all = prevalence_dict_mapgd[row][clade_type][pi_type][variant_type]['observed_prevalence_all']
            observed_prevalence_all = numpy.asarray(observed_prevalence_all)

            f_max_all = prevalence_dict_mapgd[row][clade_type][pi_type][variant_type]['f_max_all']
            f_max_all = numpy.asarray(f_max_all)

            predicted_prevalence_all_no_zeros = predicted_prevalence_all[(observed_prevalence_all>0) & (predicted_prevalence_all>0) & (f_max_all<1.0) ]
            observed_prevalence_all_no_zeros = observed_prevalence_all[(observed_prevalence_all>0) & (predicted_prevalence_all>0) & (f_max_all<1.0) ]
            f_max_all_no_zeros = f_max_all[(observed_prevalence_all>0) & (predicted_prevalence_all>0) & (f_max_all<1.0) ]


            #f_max_no_zeros = f_max[(observed_prevalence>0) & (predicted_prevalence>0)]
            if len(observed_prevalence_no_zeros) == 0:
                continue

            all_ = numpy.concatenate([predicted_prevalence_no_zeros,observed_prevalence_no_zeros])

            re = numpy.absolute(observed_prevalence_no_zeros - predicted_prevalence_no_zeros) / observed_prevalence_no_zeros
            re_all = numpy.absolute(observed_prevalence_all_no_zeros - predicted_prevalence_all_no_zeros) / observed_prevalence_all_no_zeros

            mre = numpy.mean(re)
            mre_all = numpy.mean(re_all)

            #print(clade_type, numpy.mean(re - mre_all))

            #mre_all.append(mre)

            #xy = numpy.vstack([observed_prevalence_no_zeros, predicted_prevalence_no_zeros])

            # Calculate the point density
            #try:
            #    xy = numpy.vstack([observed_prevalence_no_zeros, predicted_prevalence_no_zeros])
            #    z = gaussian_kde(xy)(xy)
            #    # Sort the points by density, so that the densest points are plotted last
            #    idx = z.argsort()
            #    x, y, z = observed_prevalence[idx], predicted_prevalence[idx], z[idx]
            #    ax.scatter(x, y, c=z, cmap="Blues", s=90, alpha=0.9, edgecolor='', zorder=1)

            #except:
            #    pass

            xy = numpy.vstack([observed_prevalence_no_zeros, predicted_prevalence_no_zeros])
            z = gaussian_kde(xy)(xy)
            # Sort the points by density, so that the densest points are plotted last
            idx = z.argsort()
            x, y, z = observed_prevalence[idx], predicted_prevalence[idx], z[idx]
            ax.scatter(x, y, c=z, cmap="Blues", s=90, alpha=0.9, edgecolor='', zorder=1)


            #ax.scatter(observed_prevalence, predicted_prevalence, c='dodgerblue', s=90, alpha=0.9, edgecolor='', zorder=1)

            max_ = max(all_)*1.1
            min_ = min(all_)*0.8

            #print(min(f_max_no_zeros))

            ax.plot([min_, max_],[min_, max_], ls='--', lw=2, c='k', zorder=2)
            ax.set_xlim([min_, max_])
            ax.set_ylim([min_, max_])


            ax.set_xscale('log', basex=10)
            ax.set_yscale('log', basey=10)

            ax.set_title(figure_utils.get_pretty_species_name(row), fontsize=12, fontweight='bold', color='k' )


            if (row_idx == 0):
                ax.set_ylabel('Predicted SNV prevalence', fontsize=12)


            if column_idx == len(nested_species_list)-1:
                ax.set_xlabel('Observed SNV prevalence', fontsize=12)


            if column_idx == len(nested_species_list)-2:

                if row_idx > len(nested_species_list[-1])-1:

                    ax.set_xlabel('Observed SNV prevalence', fontsize=12)


    #mre_all = numpy.asarray(mre_all)
    #print(sum(mre_all < 0.5) / len(mre_all))

    fig.tight_layout()
    fig.subplots_adjust(hspace=0.2)
    # dpi = 600
    fig.savefig("%spredicted_observed_prevalence_mapgd_%s_%s_%s.png" % (config.analysis_directory, clade_type, pi_type, variant_type), format='png', bbox_inches = "tight", pad_inches = 0.4)
    plt.close()


#clade_types = ['all','largest_clade', 'no_strains']
clade_types = ['just_strains']
pi_types = ['pi_exclude_boundary', 'pi_include_boundary']

#for allowed_variant_type in allowed_variant_types:
##    for clade_type in clade_types:
#        for pi_type in pi_types:
for clade_type in clade_types:
    make_plot(clade_type, 'pi_include_boundary', variant_type='4D')