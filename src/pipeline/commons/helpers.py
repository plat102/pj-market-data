import pandas as pd

def convert_dataframe_to_json(df: pd.DataFrame) -> str:
    """
    Convert a pandas DataFrame to a JSON string.

    Parameters:
    df (pd.DataFrame): The DataFrame to convert.

    Returns:
    str: The JSON string representation of the DataFrame.
    """
    return df.to_json(orient='records', lines=True)
    
def convert_dataframe_to_dict(df: pd.DataFrame) -> dict:
    """
    Convert a pandas DataFrame to a dictionary.

    Parameters:
    df (pd.DataFrame): The DataFrame to convert.

    Returns:
    dict: The dictionary representation of the DataFrame.
    """
    return df.to_dict(orient='records')

def convert_dataframe_to_json_file(df: pd.DataFrame, file_path: str) -> None:
    """
    Convert a pandas DataFrame to a JSON string and save it to a file.

    Parameters:
    df (pd.DataFrame): The DataFrame to convert.
    file_path (str): The path to the file where the JSON string will be saved.
    """
    json_str = df.to_json(orient='records', lines=True)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(json_str)
        