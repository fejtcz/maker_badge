# Define text limits and parameters
nameScale = 3
nameLimit = 12
nameConstant = 0
nameLetterOffset = 16
surnameScale = 3
surnameLimit = 12
surnameConstant = 0
surnameLetterOffset = 16
companyNameScale = 2
companyNameLimit = 17
companyNameConstant = 4
companyNameLetterOffset = 11

# Collect user input
name = input("Enter name: ")
if len(name) > nameLimit:
    print("Name is too long!")
    exit()
surname = input("Enter surname: ")
if len(surname) > surnameLimit:
    print("Surname is too long!")
    exit()
companyName = input("Enter company name: ")
if len(companyName) > companyNameLimit:
    print("Company name is too long!")
    exit()

# Generate namecard file
try:
    with open('./namecard', 'w') as namecard:
        namecard.write(name + ',' + str(nameScale) + ',' +
                       str(round((((nameLimit - len(name)) / 2) * nameLetterOffset) + nameConstant)) + ',20\n')
        namecard.write(surname + ',' + str(surnameScale) + ',' +
                       str(round((((surnameLimit - len(surname)) / 2) * surnameLetterOffset) + surnameConstant)) + ',55\n')
        namecard.write(companyName + ',' + str(companyNameScale) + ',' +
                       str(round((((companyNameLimit - len(companyName)) / 2) * companyNameLetterOffset) + companyNameConstant)) + ',90\n')
        namecard.close()
        print('\nNamecard was create :-)\n')
except Exception:
    print('\nCan\'t generate namecard!\n')
