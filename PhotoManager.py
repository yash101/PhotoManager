import exifread
from os import path, listdir, walk, makedirs
import sys
from datetime import datetime
import calendar
import hashlib

from Config import Config
from TimestampExtractor import TimestampExtractor

import shutil
import sqlite3

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

        self.init_database()
    
    def get_inpath(self, p):
        return path.join(self.indir, p)

    def get_outpath(self, p):
        return path.join(self.outdir, p)
    
    def init_database(self):
        with open(self.get_outpath('photomgr.db'), 'a'):
            pass
        self.db = sqlite3.connect(self.get_outpath('photomgr.db'))
        self.db_cursor = self.db.cursor()

        self.db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS photo (
                filepath            TEXT                NOT NULL    UNIQUE,
                timestamp           INTEGER             NOT NULL,
                coordsX             REAL                                    DEFAULT NULL,
                coordsY             REAL                                    DEFAULT NULL,
                fileSize            INTEGER             NOT NULL,
                cryptoHash          TEXT                                    DEFAULT NULL,
                imageHash           TEXT                                    DEFAULT NULL
            );
        """)

    def import_photos(self):
        if self.recursive:
            for root, _, fils in walk(self.indir, topdown = True, followlinks = False):
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

        dt = TimestampExtractor.getTimestamp(filepath)
        timestamp = dt.utctimetuple()

        rel_path = path.join(str(timestamp.tm_year), calendar.month_name[timestamp.tm_mon], str(timestamp.tm_mday).zfill(2))
        base_path = path.join(
            self.outdir,
            rel_path
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

        size = None
        sha256 = hashlib.sha256()
        try:
            with open(filepath, 'rb') as f:
                for blk in iter(lambda: f.read(4096), b''):
                    sha256.update(blk)
        
            size = path.getsize(filepath)

            if self.db is not None:
                self.db.execute(
                    'INSERT INTO photo VALUES (filepath, timestamp, fileSize, cryptoHash, imageHash)',
                    (rel_path, dt.timestamp(), size, sha256.hexdigest(), '')
                )
        except:
            print(sys.exc_info())
