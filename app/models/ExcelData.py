# This class represents one row in the imported excel sheet. It consists of a
# preset group of values that are populated by parseExcelFile
class ExcelData():
    def __init__(self):
        pass

    # these effictivly serve as default values. They will be overwritten

    # CRN and course number (IE CS49999)
    CRN = 0
    courseNumber = 0

    section = 0
    title = ''
    instructorEmail = ''

    # building abbreviation and room number
    building = ''
    room = ''

    # meeting time, raw string from excel file
    time = ''

    # this is a seperated version of the above string
    beginTime = ''
    endTime = ''

    # days the class meets, (IE TR, MWF)
    meetingDays = ''


exceldata=ExcelData()
