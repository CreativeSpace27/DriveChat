import json
from langchain.tools import tool
from drive_service import search_drive

@tool
def google_drive_search(q_parameter: str, order_by: str = "modifiedTime desc"):
    """
    Search for files. 
    q_parameter: A valid 'q' string (e.g., "mimeType = 'application/pdf'").
    order_by: How to sort (default is 'modifiedTime desc' for newest first).
    """
    files = search_drive(q_parameter, order_by)
    
    if not files:
        return "No files found."
        
    results_string = "Found files:\n"
    for file in files:
        results_string += f"- {file['name']} (Last modified: {file['modifiedTime']}) Link: {file.get('webViewLink')}\n"
    
    return results_string