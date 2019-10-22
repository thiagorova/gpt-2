"""
This module aims to be an adapter between our API and our file system to store transcripted files until next user poll
"""
import os, errno, json, string
from random import choice

class ResultFile():
    """
    this class handles all file related actions (aka: uploading audio files and removing then once they are no longer needed)
    """
    path = str(os.getcwd() + "/result/")
    @staticmethod
    def build_filename(filename):
      folder_location = ResultFile.path
      if not os.path.exists(folder_location):
        try:
          os.makedirs(folder_location)
        except OSError as e:
          if e.errno != errno.EEXIST:
            raise
      return folder_location + str(filename) + ".txt"

    @staticmethod
    def create_file():
        """
        saves the file for future processing
        """
        filename = ''.join(choice(string.ascii_lowercase + string.digits) for x in range(12))
        final_filename= ResultFile.build_filename(filename)
        output_file = open(final_filename, 'w')
        output_file.write("")
        output_file.close()
        return filename

    @staticmethod
    def write_to_file(filename, file_data):
      """
      writes the result of the transcription to the result file
      """
      filepath = ResultFile.build_filename(filename)
      output_file = open(filepath, 'w')
      output_file.write(json.dumps(file_data))
      output_file.close()

    @staticmethod
    def is_file_done(filename):
      """
      tests if transcription has finished by testing if there is any content in the result file
      """
      filepath = ResultFile.build_filename(filename)
      try:
        return os.stat(filepath).st_size != 0
      except:
        return False

    @staticmethod
    def get_file(filename):
      """
      gets transcription result
      """
      filepath = ResultFile.build_filename(filename)
      output_file = open(filepath, 'r')
      return json.loads(output_file.read())

    @staticmethod
    def erase_file(filename):
        """
        deletes a file previously uploaded (we do NOT keep audio files)
        """
        filepath = ResultFile.build_filename(filename)
        os.remove(filepath)