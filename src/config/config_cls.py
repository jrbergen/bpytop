from distutils.util import strtobool
from enum import Enum
from pathlib import Path
from typing import List, Dict, Union, TYPE_CHECKING, Tuple, Optional

import psutil

from bpytop import __VERSION__, errlog
from src.static.default_bpytop_config import DEFAULT_CONF
from src.static.paths import Paths
from src.utils import get_system_string

if TYPE_CHECKING:
    from src.cli import CliArgs

SYSTEM: str = get_system_string()


class LogLevels(str, Enum):
    ERROR = 'ERROR'
    WARNING = 'WARNING'
    INFO = 'INFO'
    DEBUG = 'DEBUG'


class SortingOptions(str, Enum):
    PID: str = "pid"
    PROGRAM: str = "program"
    ARGUMENTS: str = "arguments"
    THREADS: str = "threads"
    USER: str = "user"
    MEMORY: str = "memory"
    CPU_LAZY: str = "cpu lazy"
    CPU_RESPONSIVE: str = "cpu responsive"


class BoxNames(str, Enum):
    CPU: str = 'cpu'
    MEM: str = 'mem'
    NET: str = 'net'
    PROC: str = 'proc'


class TempScales(str, Enum):
    CELSIUS: str = 'celsius'
    FAHRENHEIT: str = 'fahrenheit'
    KELVIN: str = 'kelvin'
    RANKINE: str = 'rankine'


class CPUSensors:
    DEFAULT_SENSORS = ['Auto']

    def __init__(self):
        self._sensorlist = self.DEFAULT_SENSORS
        self.add_psutil_sensors()

    def add_psutil_sensors(self):
        if hasattr(psutil, "sensors_temperatures"):
            try:
                _temps = psutil.sensors_temperatures()
                if _temps:
                    for _name, _entries in _temps.items():
                        for _num, _entry in enumerate(_entries, 1):
                            if hasattr(_entry, "current"):
                                self._sensorlist.append(
                                    f'{_name}:{_num if _entry.label == "" else _entry.label}')
            except Exception as err:
                errlog.debug(err)

    def __iter__(self):
        yield from self._sensorlist

    def __contains__(self, key):
        return key in self._sensorlist


class ConfigStates(str, Enum):
    INITIALIZED: str = '_initalized'
    RECREATE: str = 'recreate'
    CHANGED: str = 'changed'


class Config:
    """Holds all config variables and functions for loading from and saving to disk"""
    keys: Tuple[str, ...] = \
        ("color_theme", "update_ms", "proc_sorting", "proc_reversed",
         "proc_tree", "check_temp",
         "draw_clock", "background_update", "custom_cpu_name",
         "proc_colors", "proc_gradient", "proc_per_core",
         "proc_mem_bytes", "disks_filter",
         "update_check", "log_level", "mem_graphs", "show_swap",
         "swap_disk", "show_disks", "use_fstab", "net_download",
         "net_upload", "net_auto",
         "net_color_fixed", "show_init", "theme_background",
         "net_sync", "show_battery", "tree_depth", "cpu_sensor",
         "show_coretemp", "proc_update_mult",
         "shown_boxes", "net_iface", "only_physical",
         "truecolor", "io_mode", "io_graph_combined", "io_graph_speeds",
         "show_io_stat",
         "cpu_graph_upper", "cpu_graph_lower", "cpu_invert_lower",
         "cpu_single_graph", "show_uptime", "temp_scale", "show_cpu_freq")

    conf_dict: Dict[str, Union[str, int, bool]] = {}
    color_theme: str = "Default"
    theme_background: bool = True
    truecolor: bool = True
    shown_boxes: str = "cpu mem net proc"
    update_ms: int = 2000
    proc_update_mult: int = 2
    proc_sorting: str = "cpu lazy"
    proc_reversed: bool = False
    proc_tree: bool = False
    tree_depth: int = 3
    proc_colors: bool = True
    proc_gradient: bool = True
    proc_per_core: bool = False
    proc_mem_bytes: bool = True
    cpu_graph_upper: str = "total"
    cpu_graph_lower: str = "total"
    cpu_invert_lower: bool = True
    cpu_single_graph: bool = False
    show_uptime: bool = True
    check_temp: bool = True
    cpu_sensor: str = "Auto"
    show_coretemp: bool = True
    temp_scale: str = "celsius"
    show_cpu_freq: bool = True
    draw_clock: str = "%X"
    background_update: bool = True
    custom_cpu_name: str = ""
    disks_filter: str = ""
    update_check: bool = True
    mem_graphs: bool = True
    show_swap: bool = True
    swap_disk: bool = True
    show_disks: bool = True
    only_physical: bool = True
    use_fstab: bool = False
    show_io_stat: bool = True
    io_mode: bool = False
    io_graph_combined: bool = False
    io_graph_speeds: str = ""
    net_download: str = "10M"
    net_upload: str = "10M"
    net_color_fixed: bool = False
    net_auto: bool = True
    net_sync: bool = False
    net_iface: str = ""
    show_battery: bool = True
    show_init: bool = False
    log_level: str = "WARNING"

    warnings: List[str] = []
    info: List[str] = []

    sorting_options: Enum = SortingOptions

    log_levels: LogLevels = LogLevels
    cpu_percent_fields: List = ["total"]
    cpu_percent_fields.extend(getattr(psutil.cpu_times_percent(), "_fields", []))
    temp_scales: Enum = TempScales

    cpu_sensors: List[str] = CPUSensors()

    changed: bool = False
    recreate: bool = False
    config_file: Path = Path()

    _initialized: bool = False

    ERROR_VALUE: str = '_error_'

    def __init__(self, path: Path, cliargs: CliArgs):
        self.cliargs = cliargs
        self.config_file = path

        conf: Dict[str, Union[str, int, bool]] = self.load_config()
        if "version" not in conf.keys():
            self.recreate = True
            self.info.append(f'Config file malformatted or missing, will be recreated on exit!')
        elif conf["version"] != __VERSION__:
            self.recreate = True
            self.info.append(f'Config file version and bpytop version missmatch, will be recreated on exit!')
        for key in self.keys:
            if key in conf.keys() and conf[key] != self.ERROR_VALUE:
                setattr(self, key, conf[key])
            else:
                self.recreate = True
                self.conf_dict[key] = getattr(self, key)
        self._initialized = True

    def __setattr__(self, name, value):
        if self._initialized:
            object.__setattr__(self, ConfigStates.CHANGED, True)
        object.__setattr__(self, name, value)
        if name not in ConfigStates.__members__:
            self.conf_dict[name] = value

    def get_conf_filepath(self) -> Union[Path, None]:
        if self.config_file.exists():
            return self.config_file
        elif SYSTEM == "BSD" and Paths.CONFIG_FILE_BSD.exists():
            return Paths.CONFIG_FILE_BSD
        elif SYSTEM != "BSD" and Paths.CONFIG_FILE_OTHER_PLATFORMS.exists():
            return Paths.CONFIG_FILE_OTHER_PLATFORMS

    def load_config(self) -> Dict[str, Union[str, int, bool]]:
        """Load config from file, set correct types for values and return a dict"""
        new_config: Dict[str, Union[str, int, bool]] = {}

        conf_file: Optional[Path] = self.get_conf_filepath()

        if conf_file:
            new_config = self.read_cfg_from_file(conf_file=conf_file,
                                                 new_config=new_config)
            return self.validate_config(new_config=new_config)

    def read_cfg_from_file(self,
                           conf_file: Path,
                           new_config: Dict[str, Union[str, int, bool]]
                           ) -> Dict[str, Union[str, int, bool]]:

        try:
            with open(conf_file, "r") as f:
                for line in f:
                    line = line.strip()

                    if line.startswith("#? Config"):
                        new_config["version"] = line[line.find("v. ") + 3:]
                        continue

                    if '=' not in line:
                        continue
                    key, line = line.split('=', maxsplit=1)

                    if key not in self.keys:
                        continue
                    line = line.strip('"')

                    if type(getattr(self, key)) == int:
                        try:
                            new_config[key] = int(line)
                        except ValueError:
                            self.warnings.append(f'Config key "{key}" should be an integer!')

                    if type(getattr(self, key)) == bool:
                        try:
                            new_config[key] = bool(strtobool(line))
                        except ValueError:
                            self.warnings.append(f'Config key "{key}" can only be True or False!')

                    if type(getattr(self, key)) == str:
                        new_config[key] = str(line)

        except Exception as e:
            errlog.exception(str(e))
        return new_config

    def validate_config(self,
                        new_config: Dict[str, Union[str, int, bool]]
                        ) -> Dict[str, Union[str, int, bool]]:

        return self._check_proc_sorted(
            self._check_log_level(
                self._check_update_ms(
                    self._check_net_names(
                        self._check_cpu_sensor(
                            self._check_shown_boxes(
                                self._check_cpu_graph(
                                    self._check_temp_scales(new_config=new_config)
                                )
                            )
                        )
                    )
                )
            )
        )

    def save_config(self):
        """Save current config to config file if difference in values or version, creates a new file if not found"""
        if not self.changed and not self.recreate:
            return
        try:
            writemode = 'w' if self.config_file.exists() else 'x'
            with open(self.config_file, writemode) as f:
                f.write(DEFAULT_CONF.substitute(self.conf_dict))
        except Exception as err:
            errlog.exception(str(err))

    def _check_proc_sorted(self, new_config: Dict,
                           cfgkey: str = 'proc_sorting'
                           ) -> Dict[str, Union[str, int, bool]]:

        if cfgkey in new_config and not new_config[cfgkey] in self.sorting_options:
            new_config[cfgkey] = self.ERROR_VALUE
            self.warnings.append(
                f'Config key {cfgkey!r} didn\'t get an acceptable value!')
        return new_config

    def _check_log_level(self, new_config: Dict[str, Union[str, int, bool]],
                         cfgkey: str = 'log_level'
                         ) -> Dict[str, Union[str, int, bool]]:

        if cfgkey in new_config and not new_config[cfgkey] in self.log_levels:
            new_config[cfgkey] = self.ERROR_VALUE
            self.warnings.append(f'Config key {cfgkey} didn\'t get an acceptable value!')
        return new_config

    def _check_update_ms(self, new_config: Dict[str, Union[str, int, bool]],
                         min_val: int = 100,
                         cfgkey: str = 'update_ms'
                         ) -> Dict[str, Union[str, int, bool]]:

        if cfgkey in new_config and int(new_config[cfgkey]) < min_val:
            new_config[cfgkey] = min_val
            self.warnings.append(f'Config key "update_ms" can\'t be lower than 100!')
        return new_config

    def _check_net_names(self, new_config: Dict[str, Union[str, int, bool]],
                         cfgkeys: Tuple[str, ...] = ('net_download', 'net_upload')
                         ) -> Dict[str, Union[str, int, bool]]:

        for net_name in cfgkeys:
            if net_name in new_config and not new_config[net_name][0].isdigit():  # type: ignore
                new_config[net_name] = self.ERROR_VALUE
        return new_config

    def _check_cpu_sensor(self, new_config: Dict[str, Union[str, int, bool]],
                          cfgkey: str = 'cpu_sensor'
                          ) -> Dict[str, Union[str, int, bool]]:

        if cfgkey in new_config and not new_config[cfgkey] in self.cpu_sensors:
            new_config[cfgkey] = self.ERROR_VALUE
            self.warnings.append(f'Config key {cfgkey!r} does not contain an available sensor!')
        return new_config

    def _check_shown_boxes(self, new_config: Dict[str, Union[str, int, bool]],
                           cfgkey: str = 'shown_boxes'
                           ) -> Dict[str, Union[str, int, bool]]:

        if cfgkey in new_config and new_config[cfgkey] != "":
            for box in new_config[cfgkey].split():  # type: ignore
                if box not in BoxNames.__members__:
                    new_config[cfgkey] = self.ERROR_VALUE
                    self.warnings.append(f'Config key {cfgkey!r} contains invalid box names!')
                    break
        return new_config

    def _check_cpu_graph(self, new_config: Dict[str, Union[str, int, bool]],
                         cfgkeys: Tuple[str, ...] = ("cpu_graph_upper",
                                                     "cpu_graph_lower",)
                         ) -> Dict[str, Union[str, int, bool]]:

        for cpu_graph in cfgkeys:
            if cpu_graph in new_config and new_config[cpu_graph] not in self.cpu_percent_fields:
                new_config[cpu_graph] = self.ERROR_VALUE
                self.warnings.append(f'Config key {cpu_graph!r} does not contain an available cpu stat attribute!')
        return new_config

    def _check_temp_scales(self, new_config: Dict[str, Union[str, int, bool]],
                           cfgkey: str = 'temp_scale'
                           ) -> Dict[str, Union[str, int, bool]]:

        if cfgkey in new_config and not new_config[cfgkey] in self.temp_scales.__members__:
            new_config[cfgkey] = self.ERROR_VALUE
            self.warnings.append(f'Config key {cfgkey!r} does not contain a recognized temperature scale!')
        return new_config
