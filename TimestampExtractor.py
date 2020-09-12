import datetime
import dateutil.parser
import time
import os.path
import exifread
import ffmpeg
import Config

class TimestampExtractor():
    @staticmethod
    def getTimestamp(filename):
        try:
            return TimestampExtractor.getTimestampExif(filename)
        except:
            pass

        try:
            return TimestampExtractor.getTimestampHeic(filename)
        except:
            pass

        try:
            return TimestampExtractor.getTimestampFFMPEG(filename)
        except:
            pass

        try:
            return TimestampExtractor.getTimestampOs(filename)
        except:
            
            return datetime.datetime(time.time())

    @staticmethod
    def getTimestampExif(filename):
        try:
            with open(filename, 'rb') as f:
                tags = exifread.process_file(f)

                tstr = None
                if 'EXIF DateTimeOriginal' in tags:
                    tstr = tags['EXIF DateTimeOriginal']
                else:
                    tstr = tags['EXIF DateTimeDigitized']

                parts = str(tstr).replace(' ', ':').split(':')
                return datetime.datetime(
                    int(parts[0]),
                    int(parts[1]),
                    int(parts[2]),
                    int(parts[3]),
                    int(parts[4]),
                    int(parts[5]),
                    tzinfo = datetime.timezone.utc
                )

        except:
            raise Exception

    @staticmethod
    def getTimestampHeic(filename):
        try:
            with open(filename, 'rb') as f:
                tags = exifread.process_file(f)

                tstr = None
                if 'EXIF DateTimeOriginal' in tags:
                    tstr = tags['EXIF DateTimeOriginal']
                else:
                    tstr = tags['EXIF DateTimeDigitized']

                parts = str(tstr).replace(' ', ':').split(':')
                return datetime.datetime(
                    int(parts[0]),
                    int(parts[1]),
                    int(parts[2]),
                    int(parts[3]),
                    int(parts[4]),
                    int(parts[5]),
                    tzinfo = datetime.timezone.utc
                )

        except:
            raise Exception

    @staticmethod
    def getTimestampFFMPEG(filename):
        probe = ffmpeg.probe(filename, cmd = Config.Config.ffprobe_cmd)
        timestamp = probe['streams'][0]['tags']['creation_time']

        return dateutil.parser.isoparse(timestamp)


    @staticmethod
    def getTimestampOs(filename):
        try:
            return datetime.datetime.fromtimestamp(os.path.getctime(filename))
        except:
            return datetime.datetime.fromtimestamp(os.path.getmtime(filename))