DOCUMENTATION
=============

This is to act as a general purpose place to document how to interact with
written components


Document Generation
===================

The application provides two API endpoints for handling documents,
`/document/docx/<CRN>` and `/document/excel`.

TODO
----

* Authentication checking for endpoint access?

/document/docx/<CRN>
-------------------

* <CRN> is of type `int` and refers to a class CRN
* Accepts only GET requests
* Returns a `.docx` file containing the generated syllabus for the CRN
* Generated files are not cached as of this writing

/document/excel/
----------------

* Accepts only POST requests
* Expects an uploaded `.xlsx` file, with name `excelFile`
* Returns a json dictionary of format `{ CRN : ExcelData }`, where `ExcelData`
  is an object defined in `app/models/ExcelData.py`
* When the json object is returned, all data is guaranteed to be placed into
  the database
