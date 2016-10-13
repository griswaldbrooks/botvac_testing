# Plot Scan
`plot_scan` is a command-line tool to visualize Neato Botvac LDS scans
from a file, which can be found in the `lds_tools` subpackage.
It is meant to parse the output of the Botvac Command Line Interface (CLI)
and extract any LDS scans presented from the use of the `getldsscan` command.

For example, when running the command on the file [lds_scan.txt](example_outputs/lds_scan.txt)
```
$ plot_scan lds_scan.txt
```
It will produce the following output
![Single LDS scan image](example_output/lds_scan1.png)

Saving the output of the Botvac CLI after `getldsscan` is called is sufficient
and should not require any manual processing.
For example, when running the command on the file [lds_scan_dirty1.txt](example_outputs/lds_scan_dirty1.txt)
```
$ plot_scan lds_scan_dirty1.txt
```
It will still produce the LDS scan.
![Single LDS scan image from dirty.](example_output/lds_scan2.png)

# Multiple Scans
If the text file presented to `plot_scans` contains multiple scans,
it will present each scan sequentially. The scan found at the top of the file
is assumed to be the first scan, until the last scan found at the bottom of
the file.
`plot_scan` does not automatically replay each scan, but takes keyboard inputs
to advance the display of each scan.
  - 'd' key will go to the next scan.
  - 'a' key will go to the previous scan.

The scan index will be presented on the terminal.
