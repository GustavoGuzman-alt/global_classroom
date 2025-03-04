# processors/document_processor.py

import os
import tempfile
import shutil
from utils.translation import translate_document

def process_single_document(doc_path, target_language='ne'):
    temp_dir = tempfile.mkdtemp()
    try:
        shutil.copy(doc_path, temp_dir)
        process_documents_in_folder(temp_dir, target_language)
        base, ext = os.path.splitext(os.path.basename(doc_path))
        output_file = f"{base}_translated{ext}"
        src = os.path.join(temp_dir, output_file)
        if os.path.exists(src):
            shutil.copy(src, os.path.dirname(doc_path))
    finally:
        shutil.rmtree(temp_dir)
    # Instead of a blocking message box, return a success message.
    return "Document processing completed successfully."

def process_documents_in_folder(folder_path, target_language='ne'):
    for filename in os.listdir(folder_path):
        if filename.endswith(".docx"):
            file_path = os.path.join(folder_path, filename)
            try:
                translated_doc = translate_document(file_path, target_language=target_language)
                name, ext = os.path.splitext(filename)
                new_filename = f"{name}_translated{ext}"
                new_file_path = os.path.join(folder_path, new_filename)
                translated_doc.save(new_file_path)
                print(f"Translated '{filename}' to '{new_filename}' successfully.")
            except Exception as e:
                print(f"Error processing '{filename}': {e}")
        else:
            print(f"Skipping non-Word file: '{filename}'")
