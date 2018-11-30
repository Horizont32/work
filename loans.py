deviders = []
loan_list = []
names_list = []
sum_join = []

def input_names_sums(num = input('Количество участников тусы: ', )):
    [[names_list.append(input('Введите имя ' + str(i + 1) + ' участника ')),
      sum_join.append(input(str(names_list[i]) + ' внес, р: '))]
     for i in range(int(num))]
    return [[names_list.append(input('Введите имя ' + str(i + 1) + ' участника ')),
             sum_join.append(input(str(names_list[i]) + ' внес, р: '))]
            for i in range(int(num))]


# kek()

for i, name in enumerate(names_list):
    print(i, name, sum_join[i])
# def