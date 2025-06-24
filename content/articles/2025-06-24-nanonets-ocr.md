---
Title: NanoNets OCR for Handwritten Notes
Date: 2025-06-24 07:00
Category: Machine Learning
Tags: ai, ml, llm
Slug: 2025-06-24-nanonets-ocr
Status: draft
---

Prompt:

```
Extract the text from the above document as if you were reading it naturally. 

Return the tables in html format.

Return the equations in LaTeX representation.

If there is an image in the document and image caption is not present, add a small description of the image inside the <img></img> tag; otherwise, add the image caption inside <img></img>.

Watermarks should be wrapped in brackets. Ex: <watermark>OFFICIAL COPY</watermark>. 

Page numbers should be wrapped in brackets. Ex: <page_number>14</page_number> or <page_number>9/22</page_number>. 

Prefer using ☐ and ☑ for check boxes.
```
