# --- HELPER FUNCTION: SAVE TO GOOGLE SHEETS ---
def save_to_google_sheets(data_dict):
    """Save quiz results to Google Sheets"""
    try:
        # --- PERBAIKAN #1: Gunakan scope modern ---
        scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        # Load credentials from Streamlit secrets
        # --- PERBAIKAN #2: Ganti nama metode ---
        credentials = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"], scopes=scope
        )
        
        # Authorize and open spreadsheet
        client = gspread.authorize(credentials)
        spreadsheet_url = st.secrets["google_sheets"]["spreadsheet_url"]
        sheet = client.open_by_url(spreadsheet_url).sheet1
        
        # Get existing data to check if header exists
        existing_data = sheet.get_all_values()
        
        # If sheet is empty, add headers
        if len(existing_data) == 0:
            headers = list(data_dict.keys())
            sheet.append_row(headers)
        
        # Append new row
        values = list(data_dict.values())
        sheet.append_row(values)
        
        return True
    except Exception as e:
        st.error(f"Error saving to Google Sheets: {str(e)}")
        # Tampilkan error yang lebih detail di konsol untuk debugging
        print(f"Full error: {e}") 
        return False
