import exifread
from os import path, listdir, walk, makedirs
import sys
from datetime import datetime
import calendar

from Config import Config
from TimestampExtractor import TimestampExtractor

import shutil

class PhotoManager():
    def __init__(
        self,
        verbosity = None,
        recursive = True,
        indir = '.',
        outdir = None
    ):
        self.verbose = True
        self.recursive = recursive
        self.indir = indir
        self.outdir = outdir
    
    def get_inpath(self, p):
        return path.join(self.indir, p)

    def get_outpath(self, p):
        return path.join(self.outdir, p)

    def import_photos(self):
        if self.recursive:
            for root, dirs, fils in walk(self.indir, topdown = True, followlinks = False):
                for fil in fils:
                    self.import_photo(path.join(root, fil))
        else:
            files = listdir(self.indir)

            for f in files:
                self.import_photo(f)

    def import_photo(self, filepath):
        parts = filepath.split('.')
        ext = filepath.split('.')[-1]
        if len(parts) == 1 and filepath[0] is not '.':
            if self.verbose:
                ext = ''

        supported_filetypes = Config.supported_img_filetypes + Config.supported_video_filetypes + Config.supported_audio_filetypes

        if ext.lower() not in supported_filetypes:
            print(f'Skipping {filepath}: unknown filetype')
            makedirs(path.join(self.outdir, 'miscellaneous'))
            
            return

        timestamp = TimestampExtractor.getTimestamp(filepath).utctimetuple()

        base_path = path.join(
            self.outdir,
            str(timestamp.tm_year),
            calendar.month_name[timestamp.tm_mon],
            str(timestamp.tm_mday).zfill(2)
        )

        try:
            makedirs(base_path)
        except FileExistsError:
            pass

        final_path = path.join(base_path, path.basename(filepath))

        if self.verbose:
            print(f'{filepath} -> {final_path}')

        shutil.copy2(
            filepath,
            final_path
        )