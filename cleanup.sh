# This bash script cleans noisy files

find . | grep -E "(_pycache_|\.pyc|\.pyo$|mitype.egg-info)" | xargs rm -rf