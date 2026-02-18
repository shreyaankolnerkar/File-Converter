from io import BytesIO

import pandas as pd


def csv_to_excel(csv_bytes: bytes) -> bytes:
    df = pd.read_csv(BytesIO(csv_bytes))

    output = BytesIO()
    df.to_excel(output, index=False, engine="openpyxl")

    output.seek(0)
    return output.read()
