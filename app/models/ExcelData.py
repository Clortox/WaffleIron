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
    # This will bese inserted as a list when there are several different
    # meeting places
    building = ''
    room = ''
    # This will be true when there are more than one meeting places
    multipleMeetingPlaces = False

    # meeting time, raw string from excel file, multiple times will be
    # inserted as a list instead of a string
    time = ''
    # This will be true when there is more than one meeting time
    multipleMeetingTimes = False

    # days the class meets, (IE TR, MWF)
    # This will be inserted as a list when there are several different times
    # with different meet days
    meetingDays = ''
    # This will be true when the above is a list; IE more than one meeting time
    multipleMeetingDays = False


exceldata=ExcelData()
