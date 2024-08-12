import streamlit as st
import pandas as pd
from io import BytesIO

from api_caller import APICaller


api_caller = APICaller()

st.header("API実行ツール", divider=True)

uploaded_file = st.file_uploader("xlsxファイルをアップロードしてください。", type="xlsx")

if uploaded_file is not None:
    results = []

    df = pd.read_excel(uploaded_file, header=1)

    option = st.selectbox(
        "実行したいカラム名を選択してください。",
        df.columns,
        index=None,
    )

    if option is not None:
        for i, row in df.iterrows():
            result = api_caller.call_api(row[option])
            results.append(result)

        df[f"{option}_result"] = results
        # st.write(df)

        df.to_excel(buf := BytesIO(), index=False)
        st.download_button(
            "実行結果をダウンロード",
            buf.getvalue(),
            f"{option}_results.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
