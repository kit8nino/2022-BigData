from datetime import date
print(len('Боковая Полина Максимовна') * (date(2002, 7, 30) - date(1997, 11, 27)).days % 5 + 1)
