import os
from tqdm import tqdm
import argparse
from glob import glob
import pandas as pd
import webvtt


class GetDataFromVTT:
    def __init__(self, filename):
        self.filename = filename
        self.read()
        self.process()

    def read(self):
        self.captions = webvtt.read(self.filename)
        pass

    def process(self):
        self.records = [
            {
                "text": caption.text,
                "start": caption.start,
                "end": caption.end
            }
            for caption in self.captions
        ]
        
    def get_records(self):
        return self.records

    def get_dataframe(self):
        return pd.DataFrame(self.records)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dataset generator")
    parser.add_argument("path", default="./vtt", help="Path to VTT files")
    parser.add_argument("output", default="dataset.csv", help="Path to Output CSV file")
    args = parser.parse_args()

    filenames = glob(os.path.join(args.path, "*.vtt"))

    caption_dfs = []
    files = tqdm(filenames)
    for filename in files:
        files.set_description(filename)
        files.refresh()
        extractor = GetDataFromVTT(filename)
        df = extractor.get_dataframe()
        df["filename"] = filename
        caption_dfs.append(df)

    df = pd.concat(caption_dfs)
    df.to_csv(args.output)