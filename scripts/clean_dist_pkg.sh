#!/bin/bash

echo "Executing clean_dist_pkg.sh..."

cd $path_module

dir_to_delete1=./$source_code_dist_dir_path/
file_to_delete=./$dist_archive_file_name

echo "Removing distribution file..."
rm -rf $dir_to_delete1 $file_to_delete
