import os
import sys

from PyPDF2 import PdfFileReader
from PyPDF2 import PdfFileWriter


class PDFCompressor(object):

    def compress(self, file_full_path):
        print("Compressor starts with [{}].".format(file_full_path))
        if not os.path.isfile(file_full_path):
            print("[{}] is not a file.".format(file_full_path))
            return

        original_file_size = os.path.getsize(file_full_path)
        backup_path = file_full_path + '.bak'
        if os.path.isfile(backup_path):
            print("Failed to back up original file...")
            return

        with open(file_full_path, 'rb') as original_file:
            with open(backup_path, 'wb') as backup_file:
                backup_file.write(original_file.read())

        reader = PdfFileReader(open(backup_path, 'rb'))
        writer = PdfFileWriter()
        for i in range(reader.getNumPages()):
            original_page = reader.getPage(i)
            original_page.compressContentStreams()
            writer.addPage(original_page)
        writer.write(open(file_full_path, 'wb'))

        compressed_file_size = os.path.getsize(file_full_path)

        print("Compressor ends with [{}].".format(file_full_path))
        print("Original File size:{:,}KB".format(int(original_file_size / 1024)))
        print("Compressed File size:{:,}KB".format(int(compressed_file_size / 1024)))
        return


if __name__ == '__main__':
    if 2 > len(sys.argv):
        print("Please put file full path.")
        print("Usage: $ python3 compressor.py [FILE_FULL_PATH]")
    else:
        PDFCompressor().compress(sys.argv[1])
