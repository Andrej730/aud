from AudFile import AudFile
import arrow
import os
from AudLib import setupLogger

logger = setupLogger()

class AudDir:
    '''
    A wrapper for a directory path to ease use
    '''
    extensions = [".wav", ".mp3", ".ogg", ".flv"]
    files = []
    output_directory = "_Processed"
    count = 0
    dir = ""

    def __init__(self, _dir, _output_directory="_Processed"):
        '''
        Initialization
        '''
        self.dir = _dir
        self.update()

    def __len__(self):
        return self.count

    def __getitem__(self, _index):
        return self.files[_index]

    def __contains__(self, value):
        ret = False
        if value in self.files:
            ret = True
        return ret

    def update(self):
        self.files=[]
        _files = os.listdir(self.dir)
        for _file in _files:
            _file = AudFile(os.path.abspath(self.dir + '\\' + _file))
            if os.path.isfile(str(_file)):
                logger.error(_file)
                if str(_file.extension).lower() in str(self.extensions).lower():
                    self.count += 1
                    self.files.append(_file)

    ### UTILITIES ###
    def log(self, _dirpath):
        '''
        log the files that match the list of extensions into a meta file
        '''
        output = ""
        path = os.path.abspath(_dirpath)
        _files = os.listdir(path)
        ## Analyse each file
        for file in _files:
            filepath = os.path.abspath(file)
            if filepath.suffix in self.extensions:
                output += '' + str(path) + "\\" + str(filepath) + '\n'

        ## Summary of files
        output += '\n\nSUMMARY\n'
        output += "Count: " + str(self.count) + '\n'
        output += "Timestamp: " + str(arrow.now())
        self.writeFile(_dirpath, "meta", output)

    def writeFile(self, _dirpath, _name, _content, _filetype=".txt"):
        '''
        A quick helper to create a simple file cleanly
        '''
        file = open(_dirpath + "/" + _name + _filetype, "w")
        file.write(_content)
        file.close()

    ### SET METHODS ###
    def setOutputDir(self, _dirpath):
        '''
        Select an output directory
        '''
        if (Path(_dirpath).is_dir()):
            self.output_directory = _dirpath

    ### OS IO METHODS ###
    def renameUpper(self):
        '''
        Rename file to UPPERCASE
        '''
        for file in self.files:
            file.renameUpper()
        self.update()

    def renameLower(self):
        '''
        Rename file to lowercase
        '''
        for file in self.files:
            file.renameLower()
        self.update()

    def renameReplaceSpaces(self):
        '''
        Rename file to replace_all_spaces_with_underscored
        '''
        for file in self.files:
            file.renameReplaceSpaces()
        self.update()

    def renamePrepend(self, _prefix):
        for file in self.files:
            file.renameReplaceSpaces(_prefix)
        self.update()

    ### UNORGANIZED METHODS ###
    def convertTo(self, _target_samplerate=44100, _target_bitdepth=16):
        for file in self.files:
            file.convertTo(_target_samplerate, _target_bitdepth)

    def pad(self, _in=0.0, _out=0.0):
        for file in self.files:
            file.pad(_in, _out)

    def fade(self, _in=0.0, _out=0.0, _type='log|lin', _ratio=0.0):
        for file in self.files:
            file.fade(_in, _out, _type, _ratio)

    def move(self, _target_directory):
        for file in self.files:
            file.move(_target_directory)
        self.update()

    def metadata(self, tags):
        for file in self.files:
            file.metadata(tags)
