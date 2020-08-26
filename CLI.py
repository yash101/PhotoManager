import argparse

from PhotoManager import PhotoManager

parser = argparse.ArgumentParser(description = 'Photo Manager CLI')
parser.add_argument('-v', '--verbose', type = str, help = "verbosity")
parser.add_argument('-r', '--recurse', type = bool, default = True, help = 'Recursively search input directory')
parser.add_argument('-i', '--indir', type = str, default = '.', help = 'Input directory to import from')
parser.add_argument('-o', '--outdir', type = str, required = True, help = 'Output directory to import from')

args = parser.parse_args()

pm = PhotoManager(
    args.verbose,
    args.recurse,
    args.indir,
    args.outdir
)

pm.import_photos()