import pandas as pd
import os
from config import App


def create_file(data):
   FILE = App.EXCEL_FILEPATH
   try:
      new_df = pd.DataFrame(data)
      if os.path.exists(FILE):
         old_df = pd.read_excel(FILE)
         concat_df = pd.concat([old_df, new_df])  #łączymy ze sobą stare i nowe dataframe
         concat_df.to_excel(FILE, index=False)
      else:
         new_df.to_excel(FILE, index=False)
   except Exception as err:
      print(err)


def create_file2(data2):
   FILE2 = App.EXCEL_FILEPATH2
   try:
      new_df = pd.DataFrame(data2)
      if os.path.exists(FILE2):
         old_df = pd.read_excel(FILE2)
         concat_df = pd.concat([old_df, new_df])        #łączymy ze sobą stare i nowe dataframe
         print(concat_df)
         concat_df.to_excel(FILE2, index=False)
      else:
         new_df.to_excel(FILE2, index=False)
   except Exception as err:
      print(err)


