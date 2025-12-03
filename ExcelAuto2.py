import streamlit as st
import pandas as pd

st.title("A1 vs A2 Excel Checker (60-Day Validation)")

# Upload Excel files
a1_file = st.file_uploader("Upload a1.xlsx", type=["xlsx"])
a2_file = st.file_uploader("Upload a2.xlsx", type=["xlsx"])

# Given date input
gd = st.date_input("Select Given Date (gd)")

if st.button("Process"):
    if not a1_file or not a2_file:
        st.error("Please upload both a1.xlsx and a2.xlsx")
    else:
        # Read Excel files
        a1 = pd.read_excel(a1_file)
        a2 = pd.read_excel(a2_file)

        # Convert column A to string
        a1['A'] = a1['A'].astype(str).str.strip()
        a2['A'] = a2['A'].astype(str).str.strip()

        # Convert a2 B column to date (IMPORTANT FIX)
        a2['B'] = pd.to_datetime(a2['B'], errors='coerce', dayfirst=True)

        # Convert gd input to datetime
        gd_date = pd.to_datetime(gd)

        result_list = []

        # Compare row by row
        for index, row in a1.iterrows():
            a1_value = row['A']

            # If A exists in A2
            if a1_value in a2['A'].values:

                matched_row = a2[a2['A'] == a1_value].iloc[0]
                date_in_a2 = matched_row['B']

                if pd.notna(date_in_a2):
                    # Difference between A2 date and GD
                    diff = (date_in_a2 - gd_date).days

                    if diff > 60:
                        result_list.append("TRUE")
                    else:
                        result_list.append("NO")
                else:
                    result_list.append("NO")
            else:
                result_list.append("No Match")

        # Add result column to A1
        a1['Result'] = result_list

        # Save to a3.xlsx
        output_file = "a3.xlsx"
        a1.to_excel(output_file, index=False)

        # Display download button
        with open(output_file, "rb") as f:
            st.success("Processing Completed!")
            st.download_button(
                label="Download a3.xlsx",
                data=f,
                file_name="a3.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

