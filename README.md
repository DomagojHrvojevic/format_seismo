# format_seismo
Preprocessing seismological data

### Instalation
```
pip install format_seizmo
```

## Modules

### solohr
Formatting seismological data gathered by Smartsolo portable seismograph to hourly timestep.
Smartsolo instrument writes seismological data in .MiniSeed format.


* data_path_static ->             path to folder containing folders of smartsolo stations data
                                for example: '/mnt/smartsolo_data/Paklenica-NET'

* data_path_dynamic ->            path to folder containing mseed files of smartsolo stations (changes depending on processed station)
                                for example:    '/mnt/smartsolo_data/Paklenica-NET/Lovinac/20250322113540'

* save_path ->                    path for saving hourly formatted SANDI mseed data

