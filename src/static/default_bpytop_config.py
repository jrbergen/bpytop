"""This is the template used to create the config file"""

from string import Template
from bpytop import __VERSION__

DEFAULT_CONF: Template = Template(f'#? Config file for bpytop v. {__VERSION__}' + """

#* Color theme, looks for a .theme file in "/usr/[local/]share/bpytop/themes" and "~/.config/bpytop/themes", "Default" for builtin DEFAULT theme.
#* Prefix name by a plus sign (+) for a theme located in user themes folder, i.e. color_theme="+monokai"
color_theme="$color_theme"

#* If the theme set background should be shown, set to False if you want terminal background transparency
theme_background=$theme_background

#* Sets if 24-bit truecolor should be used, will convert 24-bit colors to 256 color (6x6x6 color cube) if false.
truecolor=$truecolor

#* Manually set which boxes to show. Available values are "cpu mem net proc", seperate values with whitespace.
shown_boxes="$shown_boxes"

#* Update time in milliseconds, increases automatically if set below internal loops processing time, recommended 2000 ms or above for better sample times for graphs.
update_ms=$update_ms

#* Processes update multiplier, sets how often the process list is updated as a multiplier of "update_ms".
#* Set to 2 or higher to greatly decrease bpytop cpu usage. (Only integers)
proc_update_mult=$proc_update_mult

#* Processes sorting, "pid" "program" "arguments" "threads" "user" "memory" "cpu lazy" "cpu responsive",
#* "cpu lazy" updates top process over time, "cpu responsive" updates top process directly.
proc_sorting="$proc_sorting"

#* Reverse sorting order, True or False.
proc_reversed=$proc_reversed

#* Show processes as a tree
proc_tree=$proc_tree

#* Which depth the tree view should auto collapse processes at
tree_depth=$tree_depth

#* Use the cpu graph colors in the process list.
proc_colors=$proc_colors

#* Use a darkening gradient in the process list.
proc_gradient=$proc_gradient

#* If process cpu usage should be of the core it's running on or usage of the total available cpu power.
proc_per_core=$proc_per_core

#* Show process memory as bytes instead of percent
proc_mem_bytes=$proc_mem_bytes

#* Sets the CPU stat shown in upper half of the CPU graph, "total" is always available, see:
#* https://psutil.readthedocs.io/en/latest/#psutil.cpu_times for attributes available on specific platforms.
#* Select from a list of detected attributes from the options menu
cpu_graph_upper="$cpu_graph_upper"

#* Sets the CPU stat shown in lower half of the CPU graph, "total" is always available, see:
#* https://psutil.readthedocs.io/en/latest/#psutil.cpu_times for attributes available on specific platforms.
#* Select from a list of detected attributes from the options menu
cpu_graph_lower="$cpu_graph_lower"

#* Toggles if the lower CPU graph should be inverted.
cpu_invert_lower=$cpu_invert_lower

#* Set to True to completely disable the lower CPU graph.
cpu_single_graph=$cpu_single_graph

#* Shows the system uptime in the CPU box.
show_uptime=$show_uptime

#* Check cpu temperature, needs "osx-cpu-temp" on MacOS X.
check_temp=$check_temp

#* Which sensor to use for cpu temperature, use options menu to select from list of available sensors.
cpu_sensor=$cpu_sensor

#* Show temperatures for cpu cores also if check_temp is True and sensors has been found
show_coretemp=$show_coretemp

#* Which temperature scale to use, available values: "celsius", "fahrenheit", "kelvin" and "rankine"
temp_scale="$temp_scale"

#* Show CPU frequency, can cause slowdowns on certain systems with some versions of psutil
show_cpu_freq=$show_cpu_freq

#* Draw a clock at top of screen, formatting according to strftime, empty string to disable.
draw_clock="$draw_clock"

#* Update main ui in background when menus are showing, set this to false if the menus is flickering too much for comfort.
background_update=$background_update

#* Custom cpu model name, empty string to disable.
custom_cpu_name="$custom_cpu_name"

#* Optional filter for shown disks, should be full path of a mountpoint, separate multiple values with a comma ",".
#* Begin line with "exclude=" to change to exclude filter, oterwise defaults to "most include" filter. Example: disks_filter="exclude=/boot, /home/user"
disks_filter="$disks_filter"

#* Show graphs instead of meters for memory values.
mem_graphs=$mem_graphs

#* If swap memory should be shown in memory box.
show_swap=$show_swap

#* Show swap as a disk, ignores show_swap value above, inserts itself after first disk.
swap_disk=$swap_disk

#* If mem box should be split to also show disks info.
show_disks=$show_disks

#* Filter out non physical disks. Set this to False to include network disks, RAM disks and similar.
only_physical=$only_physical

#* Read disks list from /etc/fstab. This also disables only_physical.
use_fstab=$use_fstab

#* Toggles if io stats should be shown in regular disk usage view
show_io_stat=$show_io_stat

#* Toggles io mode for disks, showing only big graphs for disk read/write speeds.
io_mode=$io_mode

#* Set to True to show combined read/write io graphs in io mode.
io_graph_combined=$io_graph_combined

#* Set the top speed for the io graphs in MiB/s (10 by DEFAULT), use format "device:speed" seperate disks with a comma ",".
#* Example: "/dev/sda:100, /dev/sdb:20"
io_graph_speeds="$io_graph_speeds"

#* Set fixed values for network graphs, DEFAULT "10M" = 10 Mibibytes, possible units "K", "M", "G", append with "bit" for bits instead of bytes, i.e "100mbit"
net_download="$net_download"
net_upload="$net_upload"

#* Start in network graphs auto rescaling mode, ignores any values set above and rescales down to 10 Kibibytes at the lowest.
net_auto=$net_auto

#* Sync the scaling for download and upload to whichever currently has the highest scale
net_sync=$net_sync

#* If the network graphs color gradient should scale to bandwith usage or auto scale, bandwith usage is based on "net_download" and "net_upload" values
net_color_fixed=$net_color_fixed

#* Starts with the Network Interface specified here.
net_iface="$net_iface"

#* Show battery stats in top right if battery is present
show_battery=$show_battery

#* Show init screen at startup, the init screen is purely cosmetical
show_init=$show_init

#* Enable check for new version from github.com/aristocratos/bpytop at start.
update_check=$update_check

#* Set loglevel for "~/.config/bpytop/error.log" levels are: "ERROR" "WARNING" "INFO" "DEBUG".
#* The level set includes all lower levels, i.e. "DEBUG" will show all logging info.
log_level=$log_level
""")