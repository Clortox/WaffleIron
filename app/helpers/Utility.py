from flask import make_response, jsonify

from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
import io
import datetime

# Generates a Document object containing all the info for the Syllabus
def generateSyllabus(professor, course, CRN):
    # Compile time settings
    # Table style setting; this table style
    table_style = 'Light Shading Accent 1' #blue alternating
    #table_style = 'Light Shading' # grey alternating

    doc = Document()

    # add metadata
    doc.core_properties.author = professor.user_flashlineID
    doc.core_properties.language = 'English'
    doc.core_properties.title = course.course_name + ' ' + \
        course.course_semester + ' ' + course_year + ' Syllabus'
    doc.core_properties.comments = 'Made with the waffle iron'
    doc.core_properties.category = 'Syllabus'
    doc.core_properties.created = datetime.datetime.now()
    doc.core_properties.modifier = datetime.datetime.now()
    doc.core_properties.identifier = CRN.CRN

    doc.add_heading(course.course_name, 0)
    doc.add_heading('CRN: ' + CRN.CRN + ' - ' + \
            course.course_semester + ' ' + course_year, 1)

    doc.add_paragraph('\n')

    contact_table = doc.add_table(rows=len(user_contactfields), cols=2, \
            style=table_style)
    contact_table.alignment = WD_TABLE_ALIGNMENT.CENTER

    # contact table
    for i in range(0, len(professor.user_contactfields)):
        row = contact_table.rows[i].cells
        p = row[0].add_paragraph(user_contactfields[i][0])
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p = row[1].add_paragraph(user_contactfields[i][1])
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # course fields
    for i in range(0, len(course.course_fields)):
        doc.add_heading(course.course_fields[i][0], level=1)
        doc.add_paragraph(course_fields[i][1])

    return doc

def docToBase64(doc):
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return b64decode(buffer.getvalue())

# Jsonifies the passed object, and makes a response object out of it
def sendResponse(result):
    resp = make_response(jsonify(result))
    resp.mimetype = 'application/json'
    return resp
