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

def plot_fullsweeps(data, percent_overlap):
    fullsweeps = fullsweeper(data, percent_overlap)
    fullsweeps[:,0] += -fullsweeps[0,0]
    
    freqs = (fullsweeps[0,1] + np.arange(len(fullsweeps[0,3:])))/1e6
    for i in fullsweeps:
        intensities = i[3:]
        plt.plot(freqs, intensities, '-', label = str(math.ceil(i[0])) + ' s')
        
    plt.legend()
    plt.xlabel('frequency $($MHz$)$')
    plt.ylabel('intensity $($Volts$^2)$')
    plt.title('Intensity v.s. Frequency of Fullsweeps')
    plt.show()

def concatenate_data(dir, concatenated_file_name):
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