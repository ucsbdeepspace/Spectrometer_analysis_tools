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

def concatenate_data(dir, concatenated_file_name):
    filenames = glob.glob(dir + '/*.h5')
    files = [h5py.File(i) for i in filenames]

    num_rows = np.sum(len(i['Spectrum_Data'][:,0]) for i in files)
    num_cols = len(files[0]['Spectrum_Data'][0,:])
    concatenated_file = h5py.File(name, 'w')
    concatenated_data = concatenated_file.create_dataset('Spectrum_Data', \
                                                         (num_rows, num_cols))
    
    beg = 0
    for i in files:
        if (len(i['Spectrum_Data'][:,0]) != 0):
            concatenated_file['Spectrum_Data'][beg:beg+len(i['Spectrum_Data'][:,0]),:] \
            = i['Spectrum_Data']
            beg += len(i['Spectrum_Data'][:,0]) 