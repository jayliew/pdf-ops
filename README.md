# pdf-ops
PDF ops

# TODO

In `list_pdf_fields.pdf`: 

Add fallback method of detecting field labels by spatial proximity. E.g. Use the widget's bounding box (widget.rect) to define a search area (e.g., to the left for horizontal labels). Then extract text from that area using page.get_textbox() for simple cases or page.get_text("words")/page.get_text("blocks") for more precision (filtering by intersection or distance). Adjust the search rectangle based on your PDF's layout—labels are often left-aligned or above fields.

E.g.

<python>
import fitz  # PyMuPDF

doc = fitz.open("your_form.pdf")
for page in doc:
    for widget in page.widgets():
        field_name = widget.field_name
        field_rect = widget.rect
        
        # Define search rect for label (e.g., 200 units left, same height + padding)
        label_rect = fitz.Rect(
            field_rect.x0 - 200,  # Left offset
            field_rect.y0 - 5,    # Slight top padding
            field_rect.x0,        # Up to field's left edge
            field_rect.y1 + 5     # Slight bottom padding
        )
        
        # Extract text from the label area (simple method)
        label_text = page.get_textbox(label_rect).strip()
        
        # Alternative: Use "words" for more granular control
        # words = page.get_text("words")  # List of [x0, y0, x1, y1, word, ...]
        # nearby_words = [w[4] for w in words if fitz.Rect(w[:4]).intersects(label_rect)]
        # label_text = " ".join(nearby_words).strip()
        
        print(f"Field: {field_name}, Visible Label: {label_text or 'None'}")
doc.close()
</python>