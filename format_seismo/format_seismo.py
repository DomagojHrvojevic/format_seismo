import pandas as pd
import obspy as ob
import numpy as np
import warnings
import os
import gc

def solohr(IN_path, OUT_path=None, station_code='CODE', station_net='NET', language='cro'):

    #check if IN_path and OUT_path are provided
    if IN_path == '':
        raise ValueError("Input data path cannot be empty.")
    if OUT_path is None:
        OUT_path = IN_path + '/hourly_formatted_data'
        warnings.warn(f"Warning: OUT_path not specified. Using default path: {OUT_path}")

    #check if station_code and station_net are provided
    if station_code == 'CODE':
        warnings.warn("Warning: Default station code 'CODE' is used. Please provide a valid station code.")
    if station_net == 'NET':
        warnings.warn("Warning: Default network code 'NET' is used. Please provide a valid network code.")

    #check what language user chose
    if language == 'cro': #Croatian
        year = 'godina_'; month = 'mjesec_'; day = 'dan_'; hour = 'sat_'
    elif language == 'deu':  #German
        year = 'jahr_'; month = 'monat_'; day = 'tag_'; hour = 'stunde_'
    elif language == 'spa':  #Spanish
        year = 'año_'; month = 'mes_'; day = 'día_'; hour = 'hora_'
    elif language == 'fra':  #French
        year = 'année_'; month = 'mois_'; day = 'jour_'; hour = 'heure_'     
    elif language == 'zho':  #Chinese (Simplified)
        year = '年_'; month = '月_'; day = '日_'; hour = '时_'
    elif language == 'eng': #English
        year = 'year_'; month = 'month_'; day = 'day_'; hour = 'hour_'
    
    #list of smartsolo and regular components (Z=Z, X=N, Y=E)
    components_100Hz_125Hz = ['HHZ','HHN','HHE']
    components_50Hz = ['BHZ','BHN','BHE']
    smartsolo_components = ['Z','X','Y']

    #all files in data folder
    mseed_files = os.listdir(IN_path)

    #extract only miniseed data files (smartsolo instrument writes seismo data in MiniSeed format):
    mseed_files = [i for i in mseed_files if 'MiniSeed' in i]

    #smartsolo files grouped by components and sorted by name (equivalent to time):
    smartsolo_files_z = sorted([i for i in mseed_files if 'Z' in i])
    smartsolo_files_x = sorted([i for i in mseed_files if 'X' in i])
    smartsolo_files_y = sorted([i for i in mseed_files if 'Y' in i])
    smartsolo_files = [smartsolo_files_z,smartsolo_files_x,smartsolo_files_y]

    #loop through list of lists of mseed data by components
    for count_1,mseed_files_by_components in enumerate(smartsolo_files):

        #print info for user to know which step of data formatting is being processed
        print(f'Working on station: {station_code}, network: {station_net}, component: {components_100Hz_125Hz[count_1][-1]}')

        #loop list of mseed files of one component
        for count_2,mseed_file in enumerate(mseed_files_by_components):
            
            #reed all mseed files together for each component separately
            if count_2 == 0:
                file = ob.read(IN_path + f'/{mseed_file}')
            else:
                file += ob.read(IN_path + f'/{mseed_file}')

        #merge traces of all smartsolo mseed files of one component and fill gaps with zeroes
        if len(file) > 1:
            file.merge(method=0, fill_value=None)
        if isinstance(file[0].data, np.ma.masked_array):
            file[0].data = file[0].data.filled()

        #starting and ending time (UTCDateTime), sampling_rate
        start_time = file[0].stats.starttime
        end_time = file[0].stats.endtime
        sampling_rate = file[0].stats.sampling_rate

        #depending on sampling_rate, components have H or B in thein naming
        if sampling_rate == 50:
            components = components_50Hz
        else:
            components = components_100Hz_125Hz

        #starting time is first full hour of start_date that contains data
        current_time_start = ob.UTCDateTime(start_time.year,start_time.month,start_time.day,start_time.hour)
        #while loop from start_time to end_time with delta = 1 hour
        while current_time_start <= end_time:

            #add 1 hour (3600s) to determine ending date of one sandi file
            current_time_end = current_time_start + 3600
            
            #new stream object that is cut at given time interval: current_time_start <-> current_time_end
            file_cut = file.slice(current_time_start, current_time_end)

            #horizontal or vertical component depending on location of string element in smartsolo_components list
            component = components[smartsolo_components.index([i for i in smartsolo_components if i in file_cut[0].stats.channel][0])]

            #update headers in cut/hourly file
            file_cut[0].stats.network = station_net
            file_cut[0].stats.station = station_code
            file_cut[0].stats.channel = component

            #output file name
            out_file = station_code.lower() + '_' + component[-1].lower() + '_' + str('%03i' % file_cut[0].stats.sampling_rate) + "_" + str('%04i' % current_time_start.year) + str('%02i' % current_time_start.month) + str('%02i' % current_time_start.day) + "_" + str('%02i' % current_time_start.hour) + '00.mseed'

            #output data folder
            out_folder = OUT_path + f'/{year}' + str(current_time_start.year) + f'/{month}' + str('%02i' % current_time_start.month) + f'/{day}' + str('%02i' % current_time_start.day) + f'/{hour}' + str('%02i' % current_time_start.hour)

            #if folder doesn't exist, create it
            if not os.path.exists(out_folder):
                os.makedirs(out_folder)
                print("Directory ", out_folder, " created.")

            #write hourly data
            file_cut.write(f'{out_folder}/{out_file}', format='MSEED')
            print("Formatted file", out_file)

            #remove file_cut variable
            file_cut.clear()

            #add 1 hour (3600s)
            current_time_start += 3600 

        #clear cache and clear memory
        file.clear(); gc.collect()
        
    return
