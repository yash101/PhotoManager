import exifread
from os import path, listdir, walk, makedirs
import sys
from datetime import datetime
import calendar

from Config import Config
from FileMapper import getCreationTimestamp

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

        if ext not in supported_filetypes:
            print(f'Skipping {filepath}: unknown filetype')

        try:

            year, month, day, hour, minute, second = None, None, None, None, None, None
            # get the exif data
            with open(filepath, 'rb') as fil:
                tags = {}
                try:
                    tags = exifread.process_file(fil)
                except:
                    pass

                # for tag in tags:
                #     if tag not in ['JPEGThumbnail', 'TIFFThumbnail']:
                #         print(f'k: {tag}; v: {tags[tag]}')
                
                if 'EXIF DateTimeOriginal' in tags:
                    try:
                        dt = tags['EXIF DateTimeOriginal']
                        parts = str(dt).replace(' ', ':').split(':')
                        year, month, day, hour, minute, second = parts[0], parts[1], parts[2], parts[3], parts[4], parts[5]
                    except KeyboardInterrupt:
                        raise KeyboardInterrupt
                    except:
                        pass
                elif 'EXIF DateTimeDigitized' in tags:
                    try:
                        dt = tags['EXIF DateTimeDigitized']
                        parts = str(dt).replace(' ', ':').split(':')
                        year, month, day, hour, minute, second = parts[0], parts[1], parts[2], parts[3], parts[4], parts[5]
                    except KeyboardInterrupt:
                        raise KeyboardInterrupt
                    except:
                        pass
                else:
                    try:
                        tstmp = getCreationTimestamp(filepath)
                        dt = datetime.fromtimestamp(tstmp)
                        year, month, day, hour, minute, second = (
                            dt.year,
                            dt.month,
                            dt.day,
                            dt.hour,
                            dt.minute,
                            dt.second
                        )
                    except KeyboardInterrupt:
                        raise KeyboardInterrupt
                    except:
                        pass
            
            if year is not None:
                new_home = path.join(
                    self.outdir,
                    str(year),
                    calendar.month_name[int(month)],
                    str(day).zfill(2)
                )

                try:
                    makedirs(new_home)
                except FileExistsError:
                    pass

                final_path = path.join(new_home, path.basename(filepath))

                if self.verbose:
                    print(f'{filepath} -> {final_path}')
                shutil.copy2(
                    filepath,
                    new_home
                )

        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except:
            raise
            # print(f'Failed processing {filepath} due to error')
            # print(sys.exc_info()[0])