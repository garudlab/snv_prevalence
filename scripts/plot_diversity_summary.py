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
import prevalence_utils
import scipy.stats as stats
import scipy.special as special

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.gridspec as gridspec
from matplotlib.lines import Line2D

import calculate_predicted_prevalence_mapgd
import calculate_predicted_prevalence


import plot_utils

species_color_map, ordered_species_list = plot_utils.get_species_color_map()


prevalence_dict_mapgd = calculate_predicted_prevalence_mapgd.load_predicted_prevalence_dict_all()

#prevalence_dict_mapgd = calculate_predicted_prevalence_mapgd.load_predicted_prevalence_subsample_dict()

species_list = list(prevalence_dict_mapgd.keys())
species_list.sort()


#fig, ax = plt.subplots(figsize=(4,4))

clade_type = 'no_strains'
#clade_type = 'all'
pi_type = 'pi_include_boundary'
variant_type = '4D'
max_n_occurances = 7

fig = plt.figure(figsize = (11, 8)) #
#fig.subplots_adjust(bottom= 0.1)

ax_f = plt.subplot2grid((2, 2), (0, 0), colspan=1)
ax_f_mean = plt.subplot2grid((2, 2), (0, 1), colspan=1)
ax_f_mean_vs_var = plt.subplot2grid((2, 2), (1, 0), colspan=1)
#ax_f_prevalence = plt.subplot2grid((2, 2), (1, 0), colspan=1)
ax_f_max_vs_prevalence = plt.subplot2grid((2, 2), (1, 1), colspan=1)

ax_f.text(-0.1, 1.02, 'a', fontsize=10, fontweight='bold', ha='center', va='center', transform=ax_f.transAxes)
ax_f_mean.text(-0.1, 1.02, 'b', fontsize=10, fontweight='bold', ha='center', va='center', transform=ax_f_mean.transAxes)
#ax_f_prevalence.text(-0.1, 1.02, 'c', fontsize=10, fontweight='bold', ha='center', va='center', transform=ax_f_prevalence.transAxes)
ax_f_max_vs_prevalence.text(-0.1, 1.02, 'd', fontsize=10, fontweight='bold', ha='center', va='center', transform=ax_f_max_vs_prevalence.transAxes)


if clade_type == 'all':
    min_prevalence = 0.3
else:
    min_prevalence = 0.1


# sort species names
species_n_sites_list = []
for species_name in species_list:
    observed_prevalence_mapgd = prevalence_dict_mapgd[species_name][clade_type][pi_type][variant_type]['observed_prevalence_mapgd']
    observed_prevalence_mapgd = numpy.asarray(observed_prevalence_mapgd)
    n_sites = sum(observed_prevalence_mapgd >= min_prevalence)
    species_n_sites_list.append((species_name, n_sites))

species_n_sites_list.sort(key=lambda tup: tup[1])
species_n_sites_list = species_n_sites_list[::-1]
species_list_to_plot = [s[0] for s in species_n_sites_list]



means_all = []
variances_all = []
f_max_all = []
prevalence_all = []
n_non_zero_f_all = []

species_list_to_plot_good = []
for species_name in species_list_to_plot:

    f_mapgd = prevalence_dict_mapgd[species_name][clade_type][pi_type][variant_type]['f_no_zeros_mapgd']
    f_mapgd = numpy.asarray(f_mapgd)

    n_non_zero_f = prevalence_dict_mapgd[species_name][clade_type][pi_type][variant_type]['n_non_zero_frequencies']
    n_non_zero_f = numpy.asarray(n_non_zero_f)

    f_mean_mapgd = prevalence_dict_mapgd[species_name][clade_type][pi_type][variant_type]['f_mean_mapgd']
    f_mean_mapgd = numpy.asarray(f_mean_mapgd)

    f_var_mapgd = prevalence_dict_mapgd[species_name][clade_type][pi_type][variant_type]['f_var_mapgd']
    f_var_mapgd = numpy.asarray(f_var_mapgd)

    f_max_mapgd = prevalence_dict_mapgd[species_name][clade_type][pi_type][variant_type]['f_max_mapgd']
    f_max_mapgd = numpy.asarray(f_max_mapgd)

    observed_prevalence_mapgd = prevalence_dict_mapgd[species_name][clade_type][pi_type][variant_type]['observed_prevalence_mapgd']
    observed_prevalence_mapgd = numpy.asarray(observed_prevalence_mapgd)

    if len(f_mapgd) == 0:
        continue

    f_mean_mapgd_to_plot = f_mean_mapgd[observed_prevalence_mapgd >= min_prevalence]
    f_var_mapgd_to_plot = f_var_mapgd[observed_prevalence_mapgd >= min_prevalence]

    f_mapgd_log10 = numpy.log10(f_mapgd)
    f_mapgd_log10_rescaled = (f_mapgd_log10 - numpy.mean(f_mapgd_log10)) / numpy.std(f_mapgd_log10)
    hist_f, bin_edges_f = numpy.histogram(f_mapgd_log10_rescaled, density=True, bins=20)
    bins_mean_f = [0.5 * (bin_edges_f[i] + bin_edges_f[i+1]) for i in range(0, len(bin_edges_f)-1 )]
    bins_mean_f = numpy.asarray(bins_mean_f)
    hist_f_to_plot = hist_f[hist_f>0]
    bins_mean_f_to_plot = bins_mean_f[hist_f>0]

    ax_f.scatter(bins_mean_f_to_plot, hist_f_to_plot, alpha=0.9, s=10, c=species_color_map[species_name])
    # label=figure_utils.get_pretty_species_name(species_name)


    f_mean_mapgd_log10 = numpy.log10(f_mean_mapgd)
    f_mean_mapgd_log10_rescaled = (f_mean_mapgd_log10 - numpy.mean(f_mean_mapgd_log10)) / numpy.std(f_mean_mapgd_log10)
    hist_f_mean, bin_edges_f_mean = numpy.histogram(f_mean_mapgd_log10_rescaled, density=True, bins=20)
    bins_mean_f_mean = [0.5 * (bin_edges_f_mean[i] + bin_edges_f_mean[i+1]) for i in range(0, len(bin_edges_f_mean)-1 )]
    bins_mean_f_mean = numpy.asarray(bins_mean_f)

    hist_f_mean_to_plot = hist_f_mean[hist_f_mean>0]
    bins_mean_f_mean_to_plot = bins_mean_f_mean[hist_f_mean>0]

    ax_f_mean.scatter(bins_mean_f_mean_to_plot, hist_f_mean_to_plot, alpha=0.9, s=10, c=species_color_map[species_name])

    #observed_prevalence_mapgd_no_zeros = observed_prevalence_mapgd[observed_prevalence_mapgd>0]
    #observed_prevalence_mapgd_log10 = numpy.log10(observed_prevalence_mapgd_no_zeros)
    #observed_prevalence_mapgd_log10_rescaled = (observed_prevalence_mapgd_log10 - numpy.mean(observed_prevalence_mapgd_log10)) / numpy.std(observed_prevalence_mapgd_log10)
    #hist_observed_prevalence_mapgd, bin_edges_observed_prevalence_mapgd = numpy.histogram(observed_prevalence_mapgd_log10_rescaled, density=True, bins=20)
    #bins_mean_observed_prevalence_mapgd = [0.5 * (bin_edges_observed_prevalence_mapgd[i] + bin_edges_observed_prevalence_mapgd[i+1]) for i in range(0, len(bin_edges_observed_prevalence_mapgd)-1 )]
    #ax_f_prevalence.scatter(bins_mean_observed_prevalence_mapgd, hist_observed_prevalence_mapgd, alpha=0.9, s=10, c=species_color_map[species_name])


    # taylors law
    ax_f_mean_vs_var.scatter(f_mean_mapgd_to_plot, f_var_mapgd_to_plot, alpha=1, s=12, c=species_color_map[species_name])
    means_all.extend(f_mean_mapgd_to_plot.tolist())
    variances_all.extend(f_var_mapgd_to_plot.tolist())

    set_n_non_zero_f = list(set(n_non_zero_f))
    set_n_non_zero_f.sort()

    prob_prevalence = [sum(n_non_zero_f==n)/len(n_non_zero_f) for n in set_n_non_zero_f]

    #ax_f_prevalence.plot(set_n_non_zero_f, prob_prevalence, lw=2, ls='-', marker='o', c=species_color_map[species_name], alpha=0.9)

    f_max_all.extend(f_max_mapgd.tolist())
    prevalence_all.extend(observed_prevalence_mapgd.tolist())
    n_non_zero_f_all.extend(n_non_zero_f.tolist())

    # fmax occupancy
    # plot mean?
    #for i in set(n_non_zero_f):
    #    ax_f_max_vs_prevalence.scatter(numpy.mean(f_max_mapgd[n_non_zero_f==i]), i, alpha=0.8, s=10, c=species_color_map[species_name])

    idx_to_plot = numpy.random.choice(len(f_max_mapgd), size=min([len(f_max_mapgd), 1000]), replace=False)
    f_max_mapgd_to_plot = f_max_mapgd[idx_to_plot]
    n_non_zero_f_to_plot = n_non_zero_f[idx_to_plot]
    ax_f_max_vs_prevalence.scatter(f_max_mapgd_to_plot, n_non_zero_f_to_plot, alpha=0.2, s=10, c=species_color_map[species_name])
    #print(figure_utils.get_pretty_species_name(species_name), len(f_max_mapgd))

    species_list_to_plot_good.append(species_name)



x_range = numpy.linspace(-4, 3, 10000)

k = 2.0
k_digamma = special.digamma(k)
k_trigamma = special.polygamma(1,k)
gammalog = k*k_trigamma*x_range - numpy.exp(numpy.sqrt(k_trigamma)*x_range + k_digamma) - numpy.log(special.gamma(k)) + k*k_digamma + numpy.log10(numpy.exp(1))


ax_f.plot(x_range, 10**gammalog, 'k', label='Gamma', lw=2)


ax_f.set_xlabel('Rescaled ' + r'$\mathrm{log}_{10}$' + ' SNV frequencies', fontsize=11)
ax_f.set_ylabel('Probability density', fontsize=12)
#ax_f.set_ylim([-0.02, 1.23])
ax_f.set_ylim([0.007, 1.04])

ax_f.set_yscale('log', basey=10)
ax_f.legend(loc='upper left', fontsize=11)


ax_f_mean.set_xlabel('Rescaled ' + r'$\mathrm{log}_{10}$' + ' mean\nSNV frequency across hosts', fontsize=11)
ax_f_mean.set_ylabel('Probability density', fontsize=12)
#ax_f_mean.set_ylim([-0.02, 0.9])
ax_f_mean.set_yscale('log', basey=10)



if len(means_all) > 0:

    means_all = numpy.asarray(means_all)
    variances_all = numpy.asarray(variances_all)

    means_log10_all = numpy.log10(means_all)
    variances_log10_all = numpy.log10(variances_all)

    means_log10_all_test = means_log10_all[means_log10_all > numpy.log10(4*(10**-2))]
    variances_log10_all_test = variances_log10_all[means_log10_all > numpy.log10(4*(10**-2))]

    if len(means_log10_all_test) > 0:

        slope, intercept, r_value, p_value, std_err = stats.linregress(means_log10_all_test, variances_log10_all_test)
        print(slope, intercept)

        #x_log10_range =  numpy.linspace(min(means_log10_all) , max(means_log10_all) , 10000)
        x_log10_range =  numpy.linspace(min(means_log10_all) , max(means_log10_all) , 10000)
        y_log10_fit_range = (slope*x_log10_range + intercept)
        ax_f_mean_vs_var.plot(10**x_log10_range, 10**y_log10_fit_range, c='k', lw=2.5, linestyle='--', zorder=2, label=r'$\sigma^{{2}}_{{f}} \sim \bar{{f}}\,^{{{}}}$'.format(round(slope, 1)))

        #ax_f_mean_vs_var.legend(loc='upper left', fontsize=11)





#ax_f_prevalence.set_xlabel('Number of hosts where SNV is present', fontsize=12)
#ax_f_prevalence.set_xlabel('SNV prevalence across hosts, ' + r'$\bar{f}$', fontsize=11)
#ax_f_prevalence.set_ylabel('Fraction of SNVs , ' + r'$\sigma^{2}_{f}$', fontsize=11)
#ax_f_prevalence.set_ylabel('Fraction of SNVs', fontsize=12)

#ax_f_mean_vs_var.set_xlim([0.02, 0.3])
#ax_f_mean_vs_var.set_ylim([0.01, 0.2])

#ax_f_mean_vs_var.set_xlim([0.007, 0.35])
#ax_f_mean_vs_var.set_ylim([0.0004, 0.2])

#ax_f_prevalence.set_xscale('log', basex=10)
#ax_f_prevalence.set_yscale('log', basey=10)

ax_f_mean_vs_var.set_xscale('log', basex=10)
ax_f_mean_vs_var.set_yscale('log', basey=10)

ax_f_mean_vs_var.set_xlabel('Mean SNV frequency across hosts', fontsize=12)
ax_f_mean_vs_var.set_ylabel('Variance of SNV frequency across hosts', fontsize=11)

#if clade_type == 'all':
#    ax_f_prevalence.set_xlim([0.9, 32])
#else:
#    ax_f_prevalence.set_xlim([0.9, 16])
#ax_f_mean_vs_var.xaxis.set_tick_params(labelsize=5)




# relationship between f_max and prevalence
f_max_log10_all = numpy.log10(f_max_all)
n_non_zero_f_all = numpy.asarray(n_non_zero_f_all)
#prevalence_log10_all = numpy.log10(prevalence_all)
hist, bin_edges = numpy.histogram(f_max_log10_all, density=True, bins=40)
bins_mean = [0.5 * (bin_edges[i] + bin_edges[i+1]) for i in range(0, len(bin_edges)-1 )]

f_max_log10_bins = []
#prevalence_log10_bins = []
prevalence_bins = []
n_non_zero_f_bins = []
for i in range(0, len(bin_edges)-1):
    idx_i = (f_max_log10_all > bin_edges[i]) & (f_max_log10_all <= bin_edges[i+1])
    f_max_log10_bins.append(numpy.mean(f_max_log10_all[idx_i]))
    n_non_zero_f_bins.append(numpy.mean(n_non_zero_f_all[idx_i]))
    #prevalence_log10_bins.append(numpy.median(prevalence_log10_all[idx_i]))

f_max_bins = 10**numpy.asarray(f_max_log10_bins)
#prevalence_bins = 10**numpy.asarray(prevalence_log10_bins)

ax_f_max_vs_prevalence.plot(f_max_bins, n_non_zero_f_bins, c='k', lw = 3, ls ='--', label = 'Mean across species', zorder=2)
ax_f_max_vs_prevalence.set_xlabel('Max. SNV frequency within a host, ' + r'$f_{max}$', fontsize=11)
ax_f_max_vs_prevalence.set_ylabel('Number of hosts where SNV is present', fontsize=11)
ax_f_max_vs_prevalence.set_xscale('log', basex=10)
#ax_f_max_vs_prevalence.set_yscale('log', basey=10)
ax_f_max_vs_prevalence.set_xlim([min(f_max_all)*0.8, max(f_max_all)*1.1])
#ax_f_max_vs_prevalence.set_ylim([min(prevalence_all)*0.8, max(prevalence_all)*1.1])
ax_f_max_vs_prevalence.set_ylim([0.9, max_n_occurances+0.1])


#ax_f_mean_vs_var.legend(loc='upper left', fontsize=10)
ax_f_max_vs_prevalence.legend(loc='upper left', fontsize=10)


#ax_f.legend(loc='upper left', fontsize=10)

#ax_f.legend(loc='upper left', bbox_to_anchor = (-1.9, 0.55), fontsize=10)
species_list_to_plot_good.sort()
legend_elements_all = []
for species_name in species_list_to_plot_good:
    legend_elements_all.append(Line2D([0], [0], color = 'none', marker='o', markerfacecolor=species_color_map[species_name], markeredgecolor='none', label=figure_utils.get_pretty_species_name(species_name),  markersize=10.5 ))
#leg = plt.legend([circle, club],["circle", "club"], loc = "center left", bbox_to_anchor = (1, 0.5), numpoints = 1)
leg = plt.legend(handles=legend_elements_all,  bbox_to_anchor=(1, 1.85))#, numpoints = 1)


#legend_elements = []

# make the legend with species_list_to_plot



#ax_f_mean_vs_var.legend(loc='upper left', fontsize=10)
#ax_f_max_vs_prevalence.legend(loc='upper left', fontsize=10)

# all the legends

#legend_elements = [Line2D([0], [0], color = 'none', marker='o', markerfacecolor='darkgrey', markeredgecolor='none', label="Species",  markersize=8)]
# Create the figure
#markerfacecolor='darkgrey',
#handles_ax_f, labels_ax_f = ax_f.get_legend_handles_labels()

#ax_f.legend(handles=legend_elements, loc='upper left')

#ax_f_mean.legend(handles=legend_elements, loc='upper left')


# where some data has already been plotted to ax
#handles_ax_f_mean_vs_var, labels_ax_f_mean_vs_var = ax_f_mean_vs_var.get_legend_handles_labels()
# handles is a list, so append manual patch
#handles_ax_f_mean_vs_var.extend(legend_elements)
#ax_f_mean_vs_var.legend(handles=handles_ax_f_mean_vs_var, loc='upper left')


#handles_ax_f_max_vs_prevalence, labels_ax_f_max_vs_prevalence = ax_f_max_vs_prevalence.get_legend_handles_labels()
#handles_ax_f_max_vs_prevalence.extend(legend_elements)
#ax_f_max_vs_prevalence.legend(handles=handles_ax_f_max_vs_prevalence, loc='upper left')




fig.tight_layout()
fig.subplots_adjust(wspace=0.22, hspace=0.25)
fig.savefig("%sdiversity_summary_%s_%s.png" % (config.analysis_directory, clade_type, variant_type), format='png', bbox_extra_artists=(leg,), bbox_inches = "tight", pad_inches = 0.2, dpi = 600)
plt.close()
