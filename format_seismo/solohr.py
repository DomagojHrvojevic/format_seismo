#!/usr/bin/python3

#data paths
save_path = '/mnt/d/smartsolo_data/SANDI_PODACI'
data_path_static = '/mnt/d/smartsolo_data'
smartsolo_stations_metadata = '/mnt/d/smartsolo_data/smartsolo_stations.txt'

#list of smartsolo and regular components (Z=Z, X=N, Y=E)
components_100Hz_125Hz = ['HHZ','HHN','HHE']
components_50Hz = ['BHZ','BHN','BHE']
smartsolo_components = ['Z','X','Y']

#smartsolo stations metadata
stations_csv = pd.read_csv(smartsolo_stations_metadata)

#loop through all smartsolo stations
for i_d in stations_csv['ID'][1:]:

    #necessary informations for data analysis
    station_net = stations_csv.loc[stations_csv['ID'] == i_d].iloc[0]['network']
    station = stations_csv.loc[stations_csv['ID'] == i_d].iloc[0]['Kod_postaje']
    location_name = stations_csv.loc[stations_csv['ID'] == i_d].iloc[0]['names']

    #new data path depending on where data is stored:
    data_path_dynamic = data_path_static + f'/{station_net}/{location_name}/{i_d}'

    #all files in data folder
    mseed_files = os.listdir(data_path_dynamic)

    #extract only miniseed data files (smartsolo instrument writes seismo data in MiniSeed format):
    mseed_files = [i for i in mseed_files if 'MiniSeed' in i]

    #smartsolo files grouped by components and sorted by name (equivalent to time):
    smartsolo_files_z = sorted([i for i in mseed_files if 'Z' in i])
    smartsolo_files_x = sorted([i for i in mseed_files if 'X' in i])
    smartsolo_files_y = sorted([i for i in mseed_files if 'Y' in i])
    smartsolo_files = [smartsolo_files_z,smartsolo_files_x,smartsolo_files_y]

    #loop through list of lists of mseed data by components
    for coun,mseed_files_by_components in enumerate(smartsolo_files):

        #print info for user to know which step of data formatting is being processed
        print(f'Working on station: {station}, network: {station_net}, component: {components_100Hz_125Hz[coun][-1]}')

        #loop list of mseed files of one component
        for count,mseed_file in enumerate(mseed_files_by_components):
            
            #reed all mseed files together for each component separately
            if count == 0:
                file = ob.read(data_path_dynamic + f'/{mseed_file}')
            else:
                file += ob.read(data_path_dynamic + f'/{mseed_file}')

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
        if sampling_rate == 100 or sampling_rate == 125:
            components = components_100Hz_125Hz
        elif sampling_rate == 50:
            components = components_50Hz

        #while loop from start_time to end_time with delta = 1 hour
        current_time_start = ob.UTCDateTime(start_time.year,start_time.month,start_time.day,start_time.hour) #starting time is first full hour of start_date that contains data
        while current_time_start <= end_time:

            #add 1 hour (3600s) to determine ending date of one sandi file
            current_time_end = current_time_start + 3600
            
            #new stream object that is cut at given time interval: current_time_start <-> current_time_end
            file_cut = file.slice(current_time_start, current_time_end)

            #horizontal or vertical component depending on location of string element in smartsolo_components list
            component = components[smartsolo_components.index([i for i in smartsolo_components if i in file_cut[0].stats.channel][0])]

            #update headers in cut/hourly file
            file_cut[0].stats.network = station_net
            file_cut[0].stats.station = station
            file_cut[0].stats.channel = component

            #output file name
            out_file = station.lower() + '_' + component[-1].lower() + '_' + str('%03i' % file_cut[0].stats.sampling_rate) + "_" + str('%04i' % current_time_start.year) + str('%02i' % current_time_start.month) + str('%02i' % current_time_start.day) + "_" + str('%02i' % current_time_start.hour) + '00.mseed'

            #output data folder
            out_folder = save_path + '/godina_' + str(current_time_start.year) + '/mjesec_' + str('%02i' % current_time_start.month) + '/dan_' + str('%02i' % current_time_start.day) + '/sat_' + str('%02i' % current_time_start.hour)

            #if folder doesn't exist, create it
            if not os.path.exists(out_folder):
                os.makedirs(out_folder)
                print("Directory " , out_folder,  " created.")

            #write hourly data
            file_cut.write(f'{out_folder}/{out_file}', format='MSEED')
            print(out_file)

            #remove file_cut variable
            file_cut.clear()

            #add 1 hour (3600s)
            current_time_start += 3600 

        #clear cache	
        file.clear()
