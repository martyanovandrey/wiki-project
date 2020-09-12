myList = ['CSS', 'Django', 'Git', 'HTML', 'Python']
yo = 'cs'


matching = [s for s in myList if yo.lower() in s.lower()]
print(matching)