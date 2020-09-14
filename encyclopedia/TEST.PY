entries = ['CSS', 'Django', 'Git', 'HTML', 'Python']
title = 'css2'



if any(title.lower() == val.lower() for val in entries):
    print("Nice")
else:
    print('Taken')