# Unpublished Copyright (c) 2014 Jeffrey Weiner, All Rights Reserved.
#
# NOTICE: All information contained herein is, and remains the property of Jeffrey
# Weiner. The intellectual and technical concepts contained herein are
# proprietary to Jeffrey Weiner and may be covered by U.S. and Foreign Patents,
# patents in process, and are protected by trade secret or copyright law.
# Dissemination of this information or reproduction of this material is strictly
# forbidden unless prior written permission is obtained from Jeffrey Weiner.
#
# The copyright notice above does not evidence any actual or intended
# publication or disclosure of this source code, which includes  information
# that is confidential and/or proprietary, and is a trade secret, of Jeffrey
# Weiner. ANY REPRODUCTION, MODIFICATION, DISTRIBUTION, PUBLIC PERFORMANCE,
# OR PUBLIC DISPLAY OF OR THROUGH USE OF THIS SOURCE CODE WITHOUT THE EXPRESS
# WRITTEN CONSENT OF JEFFREY WEINER IS STRICTLY PROHIBITED, AND IN VIOLATION OF
# APPLICABLE LAWS AND INTERNATIONAL TREATIES. THE RECEIPT OR POSSESSION OF THIS
# SOURCE CODE AND/OR RELATED INFORMATION DOES NOT CONVEY OR IMPLY ANY RIGHTS TO
# REPRODUCE, DISCLOSE OR DISTRIBUTE ITS CONTENTS, OR TO MANUFACTURE, USE, OR
# SELL ANYTHING THAT IT MAY DESCRIBE, IN WHOLE OR IN PART.

import numpy as np
import h5py
import glob
from fullsweeper import fullsweeper
from matplotlib import pyplot as plt

def test_int_down(inarray):
    '''

    function to test if data set integrates down with increasing number of samples
    input is 1 dim array, output is a dictionary

    '''
    ncuts=np.int(np.fix(np.log2(len(inarray))))

    #first take max power of 2 subset of input array
    d=inarray[:2**ncuts]

    outstds=[]
    outnpts=[]
    for i in range(ncuts):
        d=np.reshape(d,(2**i,2**(ncuts-i)))
        outstds.append(np.std(np.mean(d,axis=1)))
        outnpts.append(2**(ncuts-i))

    out = {}
    out['stdev']=np.array(outstds)
    out['npoints']=np.array(outnpts)
    return out

def is_outlier(points, thresh=3.5):
    """
    Source: https://github.com/joferkington/oost_paper_code/blob/master/utilities.py
    
    Returns a boolean array with True if points are outliers and False 
    otherwise.

    Parameters:
    -----------
        points : An numobservations by numdimensions array of observations
        thresh : The modified z-score to use as a threshold. Observations with
            a modified z-score (based on the median absolute deviation) greater
            than this value will be classified as outliers.

    Returns:
    --------
        mask : A numobservations-length boolean array.

    References:
    ----------
        Boris Iglewicz and David Hoaglin (1993), "Volume 16: How to Detect and
        Handle Outliers", The ASQC Basic References in Quality Control:
        Statistical Techniques, Edward F. Mykytka, Ph.D., Editor. 
    """
    if len(points.shape) == 1:
        points = points[:,None]
    median = np.median(points, axis=0)
    diff = np.sum((points - median)**2, axis=-1)
    diff = np.sqrt(diff)
    med_abs_deviation = np.median(diff)

    modified_z_score = 0.6745 * diff / med_abs_deviation

    return modified_z_score > thresh

def plot_waterfall(data, percent_overlap):
    """
    input:
    data - 2d array of spectrum data in which each row represents a subsweep
    column 0: time in seconds
    column 1: start frequency in Hz
    column 2: frequency step in Hz
    column 3: bin size
    columns 4-end: intensity in dBm
    percent_overlap - fraction indicating the amount by which subsweeps overlap
                      percent_overlap of > 0.5 is not supported

    Creates a waterfall plot of the fullsweeps in data
    """
    fullsweeps = fullsweeper(data, percent_overlap)
    fullsweeps[:,0] += -fullsweeps[0,0]
    
    times = fullsweeps[:,0]
    freqs = (fullsweeps[0,1] + fullsweeps[0,2]*np.arange(len(fullsweeps[0,3:])))/1e6
    intensities = fullsweeps[:,3:]        
    
    plt.xlim(freqs[0], freqs[-1])
    plt.ylim(times[0], times[-1])
    plt.pcolormesh(freqs, times, intensities)
    plt.gca().invert_yaxis()
    
    plt.colorbar(label = 'intensity $($V$^2)$')
    plt.xlabel('frequency $($MHz$)$')
    plt.ylabel('time $($s$)$')
    plt.title('Intensity v.s. Frequency and Time')
    plt.show()

def plot_fullsweeps(data, percent_overlap):
    """
    input:
    data - 2d array of spectrum data in which each row represents a subsweep
    column 0: time in seconds
    column 1: start frequency in Hz
    column 2: frequency step in Hz
    column 3: bin size
    columns 4-end: intensity in dBm
    percent_overlap - fraction indicating the amount by which subsweeps overlap
                      percent_overlap of > 0.5 is not supported

    Creates a line plot of fullsweep intensity as a function of frequency
    """
    fullsweeps = fullsweeper(data, percent_overlap)
    fullsweeps[:,0] += -fullsweeps[0,0]
    
    freqs = (fullsweeps[0,1] + fullsweeps[0,2]*np.arange(len(fullsweeps[0,3:])))/1e6
    for i in fullsweeps:
        intensities = i[3:]
        plt.plot(freqs, intensities, '-', label = str(math.ceil(i[0])) + ' s')
    
    plt.xlim(freqs[0], freqs[-1])
    plt.legend()
    plt.xlabel('frequency $($MHz$)$')
    plt.ylabel('intensity $($V$^2)$')
    plt.title('Intensity v.s. Frequency of Fullsweeps')
    plt.show()

def concatenate_data(dir, concatenated_file_name):
    """
    input: 
    dir - directory string
    concatenated_file_name - name for the concatenated data file that is created

    output: concatenated data file containing data from all hdf files in the
            specified directory; file does not contain acquisition info
    """
    filenames = glob.glob(dir + '/*.h5')
    files = [h5py.File(i) for i in filenames]

    num_rows = np.sum(len(i['Spectrum_Data'][:,0]) for i in files)
    num_cols = len(files[0]['Spectrum_Data'][0,:])
    concatenated_file = h5py.File(concatenated_file_name, 'w')
    concatenated_data = concatenated_file.create_dataset('Spectrum_Data', \
                                                         (num_rows, num_cols))
    
    beg = 0
    for i in files:
        if (len(i['Spectrum_Data'][:,0]) != 0):
            concatenated_file['Spectrum_Data'][beg:beg+len(i['Spectrum_Data'][:,0]),:] \
            = i['Spectrum_Data']
            beg += len(i['Spectrum_Data'][:,0]) 