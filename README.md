# format_seismo
Preprocessing seismological data

## Instalation
Install from PyPI:
```bash
pip install format_seizmo
```

## Import
Import the `format_seismo` library in python code:
```python
import format_seismo as fs
```

## Functions
### solohr
Formats seismological data gathered by a SmartSolo portable seismograph into an hourly time-step format.
SmartSolo instruments store seismological data in MiniSEED format (_.mseed_ extension).
Call the function `solohr()` with the following arguments:
```python
fs.solohr(IN_path, OUT_path=None, station_code='CODE', station_net='NET', language='cro', silent=False)
```

* `IN_path:`   Path to a folder containing all _.mseed_ files of a single smartsolo station.

* `OUT_path:`  _(Optional)_ Path to the folder where formatted _.mseed_ files will be saved. If set to `None` (default value), output will be stored in a newly created subdirectory `/hourly_formatted_data` inside `IN_path`.

* `station_code:`  _(Optional)_ Deault is `'CODE'`. Used in the filename and metadata of the formatted _.mseed_ files.

* `staton_net:` _(Optional)_ Default is `'NET'`. Used in metadata of the formatted _.mseed_ files.

* `language:`  _(optional)_ Default is `'cro'` (Croatian). Language used in naming folders in the output path. Supported languages are:
  * `deu` German
  * `spa` Spanish
  * `fra` French
  * `zho` Chinese (Simplified)
  * `eng` English

* `silent:` _(optional)_ If set to True, suppresses terminal output. Default is False.
<br>

__Note__ <br>
This function processes data for __one station__ at a time.
If you have multiple stations, wrap this function in a loop.

__Example__ <br>
Importing and calling the `solohr()` function:
```python
import format_seismo as fs
fs.solohr('/mnt/raw_solo_data', '/mnt/formatted_solo_data', station_code='STAT', station_net='NET', language='eng')
```
Part of the function output:
```bash
UserWarning: Warning: Default network code 'NET' is used. Please provide a valid network code.
Working on station: STAT, network: NET, component: Z
Directory  mnt/formatted_solo_data/year_2025/month_07/day_04/hour_17  created.
Formatted file stat_z_250_20250704_1700.mseed
Directory  mnt/formatted_solo_data/year_2025/month_07/day_04/hour_18  created.
Formatted file stat_z_250_20250704_1800.mseed
Directory  mnt/formatted_solo_data/year_2025/month_07/day_04/hour_19  created.
Formatted file stat_z_250_20250704_1900.mseed
Directory  mnt/formatted_solo_data/year_2025/month_07/day_04/hour_20  created.
Formatted file stat_z_250_20250704_2000.mseed
Directory  mnt/formatted_solo_data/year_2025/month_07/day_04/hour_21  created.
Formatted file stat_z_250_20250704_2100.mseed
...
```

Part of the output directory tree:
```bash
user@DESKTOP:/mnt/formatted_solo_data$ tree
.
└── year_2025
    └── month_07
        ├── day_04
        │   ├── hour_17
        │   │   ├── stat_e_250_20250704_1700.mseed
        │   │   ├── stat_n_250_20250704_1700.mseed
        │   │   └── stat_z_250_20250704_1700.mseed
        │   ├── hour_18
        │   │   ├── stat_e_250_20250704_1800.mseed
        │   │   ├── stat_n_250_20250704_1800.mseed
        │   │   └── stat_z_250_20250704_1800.mseed
        │   ├── hour_19
        │   │   ├── stat_e_250_20250704_1900.mseed
        │   │   ├── stat_n_250_20250704_1900.mseed
        │   │   └── stat_z_250_20250704_1900.mseed
        │   ├── hour_20
        │   │   ├── stat_e_250_20250704_2000.mseed
        │   │   ├── stat_n_250_20250704_2000.mseed
        │   │   └── stat_z_250_20250704_2000.mseed
        │   ├── hour_21
        │   │   ├── stat_e_250_20250704_2100.mseed
        │   │   ├── stat_n_250_20250704_2100.mseed
        │   │   └── stat_z_250_20250704_2100.mseed
        │   ├── hour_22
        │   │   ├── stat_e_250_20250704_2200.mseed
        │   │   ├── stat_n_250_20250704_2200.mseed
        │   │   └── stat_z_250_20250704_2200.mseed
        │   └── hour_23
        │       ├── stat_e_250_20250704_2300.mseed
        │       ├── stat_n_250_20250704_2300.mseed
        │       └── stat_z_250_20250704_2300.mseed
        ├── day_05
        │   ├── hour_00
        │   │   ├── stat_e_250_20250705_0000.mseed
        │   │   ├── stat_n_250_20250705_0000.mseed
        │   │   └── stat_z_250_20250705_0000.mseed
...
```
