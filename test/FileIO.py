import os
import csv
import tqdm

class FileIO:
    def __init__(self) -> None:
        pass

    def Read(self, filePath, lineDelimiter: str = '') -> list:
        """
        File reader

        Parameters
        ----------
        filePath: str
            File path. Include extension.
        lineDelimiter: (Optional) str
            The delimiter for each line.
        
        Returns
        ----------
        data: list
            Read data
        """

        with open(filePath, encoding='UTF-8') as f:
            data = [s.strip() for s in f.readlines()]

            if lineDelimiter != '':
                data = [l.split(lineDelimiter) for l in data]
        
        return data