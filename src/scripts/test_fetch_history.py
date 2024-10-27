import sys
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()
# Get the SRC_PATH from the environment variable
src_path = os.getenv('SRC_PATH')

print(f"SRC_PATH: {src_path}")

if src_path:
    # Add the src path to sys.path
    sys.path.append(os.path.abspath(src_path))

from pipeline.extract.vnstock_lib import VnstockLibExtractor

extractor = VnstockLibExtractor()
df_all = extractor.get_all_stock_quote_histories_df()

df_all.to_json(f'{src_path}/test_data_gitignore/stock_quote_histories_df.json', orient='records')
