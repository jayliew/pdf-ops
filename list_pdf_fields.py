#!/usr/bin/env python3
"""
PDF Form Fields Lister

This script uses PyMuPDF (fitz) to extract and display all form fields
from a PDF file given its absolute path.

Usage:
    python list_pdf_fields.py /path/to/your/file.pdf
"""

import sys
import os
import fitz  # PyMuPDF


def list_pdf_form_fields(pdf_path):
    """
    Extract and display all form fields from a PDF file.
    
    Args:
        pdf_path (str): Absolute path to the PDF file
        
    Returns:
        list: List of form field dictionaries
    """
    try:
        # Open the PDF document
        doc = fitz.open(pdf_path)
        
        print(f"Processing PDF: {pdf_path}")
        print(f"Number of pages: {len(doc)}")
        print("-" * 50)
        
        all_fields = []
        
        # Iterate through each page
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Get form fields (widgets) on this page
            widgets = page.widgets()
            
            if widgets:
                print(f"\nPage {page_num + 1}:")
                print("=" * 20)
                
                for widget in widgets:
                    # Get /TU entry (tooltip/alternate description) from widget's PDF object
                    tu_entry = None
                    try:
                        # Access the widget's PDF object to check for /TU entry
                        widget_obj = widget.xref
                        if widget_obj > 0:
                            widget_dict = doc.xref_get_key(widget_obj, "TU")
                            if widget_dict[0] == "name":  # /TU exists
                                tu_entry = doc.xref_get_key(widget_obj, "TU")[1]
                                # Remove parentheses if it's a string literal
                                if tu_entry.startswith("(") and tu_entry.endswith(")"):
                                    tu_entry = tu_entry[1:-1]
                    except:
                        tu_entry = None
                    
                    field_info = {
                        'page': page_num + 1,
                        'field_name': widget.field_name,
                        'field_type': widget.field_type_string,
                        'field_value': widget.field_value,
                        'field_label': getattr(widget, 'field_label', None),
                        'tooltip': tu_entry,
                        'rect': widget.rect,
                        'is_signed': getattr(widget, 'is_signed', None)
                    }
                    
                    all_fields.append(field_info)
                    
                    # Display field information
                    print(f"  Field Name: {field_info['field_name']}")
                    if field_info['field_label'] is not None:
                        print(f"  Field Label: {field_info['field_label']}")
                    if field_info['tooltip'] is not None:
                        print(f"  Tooltip (/TU): {field_info['tooltip']}")
                    print(f"  Field Type: {field_info['field_type']}")
                    print(f"  Field Value: {field_info['field_value']}")
                    print(f"  Position: {field_info['rect']}")
                    if field_info['is_signed'] is not None:
                        print(f"  Is Signed: {field_info['is_signed']}")
                    print()
        
        # Close the document
        doc.close()
        
        # Summary
        print("-" * 50)
        print(f"Total form fields found: {len(all_fields)}")
        
        if not all_fields:
            print("No form fields found in this PDF.")
        
        return all_fields
        
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return []


def main():
    """Main function to handle command line arguments and execute the script."""
    
    if len(sys.argv) != 2:
        print("Usage: python list_pdf_fields.py <absolute_path_to_pdf_file>")
        print("Example: python list_pdf_fields.py /Users/username/Documents/form.pdf")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    
    # Validate the file path
    if not os.path.isabs(pdf_path):
        print("Error: Please provide an absolute path to the PDF file.")
        sys.exit(1)
    
    if not os.path.exists(pdf_path):
        print(f"Error: File does not exist: {pdf_path}")
        sys.exit(1)
    
    if not pdf_path.lower().endswith('.pdf'):
        print("Error: File must be a PDF (.pdf extension)")
        sys.exit(1)
    
    # Process the PDF file
    fields = list_pdf_form_fields(pdf_path)
    
    # Optional: Save results to a text file
    if fields:
        output_file = os.path.splitext(pdf_path)[0] + "_form_fields.txt"
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"Form Fields Report for: {pdf_path}\n")
                f.write("=" * 50 + "\n\n")
                
                for field in fields:
                    f.write(f"Page: {field['page']}\n")
                    f.write(f"Field Name: {field['field_name']}\n")
                    if field['field_label'] is not None:
                        f.write(f"Field Label: {field['field_label']}\n")
                    if field['tooltip'] is not None:
                        f.write(f"Tooltip (/TU): {field['tooltip']}\n")
                    f.write(f"Field Type: {field['field_type']}\n")
                    f.write(f"Field Value: {field['field_value']}\n")
                    f.write(f"Position: {field['rect']}\n")
                    if field['is_signed'] is not None:
                        f.write(f"Is Signed: {field['is_signed']}\n")
                    f.write("-" * 30 + "\n")
                
                f.write(f"\nTotal form fields: {len(fields)}\n")
            
            print(f"\nReport saved to: {output_file}")
            
        except Exception as e:
            print(f"Warning: Could not save report file: {e}")


if __name__ == "__main__":
    main()