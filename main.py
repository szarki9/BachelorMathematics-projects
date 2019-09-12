import sys
import PySimpleGUI as sg
import tkinter as Tk, tkinter.font as tkFont
import random, math


def find_index(wanted_number, current_series):
    number_index = [(i, el.index(wanted_number)) for i, el in enumerate(current_series) if wanted_number in el]
    return number_index[0][0]


def get_data_randomly():
    x = random.randint(15, 35)  # tutaj dałam jakieś randomowe ograniczenia, można to ofc zmienić
    k = random.randint(3, 6)
    level = random.randint(1, 3)
    return x, k, level


def create_series_with_colour(x):
    series = random.sample(range(1, 3 * x), x)
    col = "black"
    series.sort()
    series_to_colour = [[series[0], col]]
    for i in range(1, x - 1):
        series_to_colour.append([series[i], col])
    return series_to_colour


def append_series_with_colour(current_series, number, colour):
    number = int(number)  # w funkcji ruchu komputera i uzytkownika sprawdzana jest poprawnosc danych
    number_index = [(i, el.index(number)) for i, el in enumerate(current_series) if number in el]
    number_index = number_index[0][0]
    current_series[number_index][1] = colour
    return current_series


def find_col_series(current_series, col_a, col_b):
    one_col_series = []
    for i in range(len(current_series)):
        if current_series[i][1] == col_a or current_series[i][1] == col_b:
            one_col_series.append(current_series[i][0])
    return one_col_series


def find_monochrome(current_series, col_a, col_b, ary_len):
    one_col_series = find_col_series(current_series, col_a, col_b)
    mono_series = []
    len_one_col = len(one_col_series)
    for k in range(len_one_col):  # iterujemy po kazdym wyrazie od poczatku
        for n in range(k + 1, len_one_col,
                       1):  # ustalamy roznice, petla po roznicach dla ustalonego pierwszego wyrazu (w poprzedniej petli)
            diff = one_col_series[n] - one_col_series[k]
            monochrome_series = []
            monochrome_series.append(one_col_series[k])  # wpisujemy pierwszy wyraz do ciagu
            for j in range(k,
                           len_one_col):  # sprawdzamy czy istnieją kolejne wyrazy dla tej ustalonej roznicy, iterujemy od wyrazu ktory ustalilismy
                for i in range(j + 1,
                               len_one_col):  # petla przechodzi dla kazdego wyrazu po ustalonym, patrzac czy sa roznice
                    if one_col_series[i] - one_col_series[j] == diff \
                            and one_col_series[i] - monochrome_series[-1] == diff:
                        monochrome_series.append(one_col_series[i])  # jak sa to przypisuje ostatni wyraz
                        # potem patrzymy na kolejny wyraz ciagu
            if len(monochrome_series) >= ary_len:
                mono_series.append(monochrome_series)
    return mono_series  # zwracamy tablicę ciagów arytmetycznych jednego koloru


def check_monochrome_series(current_series, col_a, col_b, ary_len):
    x = False
    winning_series = []
    all_mono_series = find_monochrome(current_series, col_a, col_b, ary_len)
    if len(all_mono_series) != 0:
        x = True
        winning_series = all_mono_series[0]
    return x, winning_series


def find_blank_series(series, current_series):
    blank_series = []
    norm_col = "black"
    for k in range(len(series)):
        index = [(i, el.index(series[k])) for i, el in enumerate(current_series) if series[k] in el]
        index = index[0][0]
        if current_series[index][1] == norm_col:
            blank_series.append(series[k])
    return blank_series


def num_of_coloured(series, current_series, color):
    color_series = []
    for k in range(len(series)):
        index = [(i, el.index(series[k])) for i, el in enumerate(current_series) if series[k] in el]
        index = index[0][0]
        if current_series[index][1] == color:
            color_series.append(series[k])
    return len(color_series)


def computer_move(current_series, comp_level, ary_len):
    # print("Teraz komputer wykonuje ruch.")
    comp_level = int(comp_level)
    if comp_level == 1:
        current_series = computer_strategy_1(current_series, ary_len)
    elif comp_level == 2:
        current_series = computer_strategy_2(current_series, ary_len)
    elif comp_level == 3:
        current_series = computer_strategy_3(current_series, ary_len)
    return current_series


def computer_strategy_1(current_series, ary_len):
    col = "red"
    norm_col = "black"
    x = check_monochrome_series(current_series, col, norm_col, ary_len)[0]
    blank_nums = find_col_series(current_series, norm_col, norm_col)
    if x is True:
        series = find_monochrome(current_series, col, norm_col, ary_len)[
            0]  # wybiera pierwszy ciag, a nie najmniejszy wyraz
        blank_series = find_blank_series(series, current_series)
        num = random.choice(blank_series)
        append_series_with_colour(current_series, num, col)
    elif x is False:
        blank_series = find_blank_series(blank_nums, current_series)
        num = random.choice(blank_series)
        append_series_with_colour(current_series, num, col)
    # print("Komputer pokolorował pole z numerem " + str(num) + ".")
    return current_series


def computer_strategy_2(current_series, ary_len):
    komp_col = "red"
    czl_col = "green"
    norm_col = "black"
    blank_nums = find_col_series(current_series, norm_col, norm_col)
    x = check_monochrome_series(current_series, komp_col, norm_col, ary_len)[0]
    y = check_monochrome_series(current_series, czl_col, norm_col, ary_len)[0]
    if x is True:
        series = find_monochrome(current_series, komp_col, norm_col, ary_len)[
            0]  # wybiera pierwszy ciag, a nie najmniejszy wyraz
        blank_series = find_blank_series(series, current_series)
        num = random.choice(blank_series)
        append_series_with_colour(current_series, num, komp_col)
    elif x is False:
        if y is True:
            series = find_monochrome(current_series, czl_col, norm_col, ary_len)[0]
            blank_series = find_blank_series(blank_nums, series)
            num = random.choice(blank_series)
            append_series_with_colour(current_series, num, komp_col)
        elif y is False:
            blank_series = find_blank_series(blank_nums, current_series)
            num = random.choice(blank_series)
            append_series_with_colour(current_series, num, komp_col)
    # print("Komputer pokolorował pole z numerem " + str(num) + ".")
    return current_series


def find_max_number_of_coloured(current_series, col_a, col_b, ary_len):
    wanted_series = find_monochrome(current_series, col_a, col_b, ary_len)
    colors_num = []
    for i in range(len(wanted_series)):
        colors_num.append(num_of_coloured(wanted_series[i], current_series, col_a))  #tabela dlugosci poszczegolnych ciagow
    if len(colors_num) == 0:
        max_num = 0
        index_max = 0
    else:
        max_num = max(colors_num)
        index_max = colors_num.index(max(colors_num))
    return max_num, index_max


def computer_strategy_3(current_series, ary_len):
    komp_col = "red"
    czl_col = "green"
    norm_col = "black"
    x = check_monochrome_series(current_series, komp_col, norm_col, ary_len)[0]
    y = check_monochrome_series(current_series, czl_col, norm_col, ary_len)[0]
    blank_nums = find_col_series(current_series, norm_col, norm_col)
    human_col_num = find_max_number_of_coloured(current_series, czl_col, norm_col, ary_len)[0]
    if x is True and human_col_num != ary_len - 1:
        series = find_monochrome(current_series, komp_col, norm_col, ary_len)
        index = find_max_number_of_coloured(current_series, komp_col, norm_col, ary_len)[1]
        blank_series = find_blank_series(series[index], current_series)
        num = blank_series[math.floor(len(blank_series) / 2)]
        append_series_with_colour(current_series, num, komp_col)
    elif x is True and human_col_num == ary_len - 1:
        series = find_monochrome(current_series, czl_col, norm_col, ary_len)
        index = find_max_number_of_coloured(current_series, czl_col, norm_col, ary_len)[1]
        blank_series = find_blank_series(series[index], current_series)
        num = random.choice(blank_series)
        append_series_with_colour(current_series, num, komp_col)
    elif x is False:
        if y is True:
            series = find_monochrome(current_series, czl_col, norm_col, ary_len)
            index = find_max_number_of_coloured(current_series, czl_col, norm_col, ary_len)[1]
            blank_series = find_blank_series(series[index], current_series)
            num = random.choice(blank_series)
            append_series_with_colour(current_series, num, komp_col)
        elif y is False:
            blank_series = find_blank_series(blank_nums, current_series)
            num = random.choice(blank_series)
            append_series_with_colour(current_series, num, komp_col)
    # print("Komputer pokolorował pole z numerem " + str(num) + ".")
    return current_series


def possible_series(current_series, ary_len):
    if check_monochrome_series(current_series, "black", "green", ary_len)[0] == True or \
            check_monochrome_series(current_series, "black", "red", ary_len)[0] == True or check_monochrome_series(
            current_series, "black", "black", ary_len) == True:
        x = True
    else:
        x = False
    return x


location = (400,200)
layout = [
            [sg.Text('Witamy w grze Szemeredi\'ego', font=("Century Schoolbook L", "30"))],
            [sg.Text('Podaj swoje imie', size=(20, 1)), sg.Input()],
            [sg.Frame(layout=[
                [sg.Radio('Wylosuj dla mnie zasady ', "RADIO1", default=True, size=(30,1), key='Losowanie'),
                 sg.Radio('Sam wybiorę zasady', "RADIO1", size=(30,1), key='Wybieranie')]
                            ], title='Zasady gry',title_color='blue', relief=sg.RELIEF_SUNKEN, tooltip='Wybierz swoją opcję')],
            [sg.Text('Podstawowe zasady gry: ', font=("Century Schoolbook L", "15"))],
            [sg.Text('Komputer wraz z użytkownikiem kolorują na zmianę wybrane liczby z podanego zbioru', font=("Century Schoolbook L", "10"), justification='right')],
            [sg.Text('pamiętając o tym, że można wybierać tylko liczbę niepokolorowaną. ', font=("Century Schoolbook L", "10"))],
            [sg.Text('Wygrywa ten, który jako pierwszy z pokolorowanych liczb stworzy arytmetyczny ciąg monochromatyczny* ', font=("Century Schoolbook L", "10"))],
            [sg.Button('Dalej'), sg.Button('Przeczytaj dokładniejszy opis'), sg.Button('Exit')]
        ]
starting_layout = layout

starting_window = sg.Window('Window Title', layout, location=location)

main_list=[]
level = 0
target_length = 0
temp_values = []
kto = ''
imie = ''

while True:
    event, values = starting_window.Read()
    print(event, values)
    if event is None or event == 'Exit':
        break
    if (event == 'Dalej') and values['Wybieranie']:
        if len(values) >= 3:
            imie = values[0]
        layout = [
            [sg.Text('Witaj  ', font=("Century Schoolbook L", "17")), sg.Text(imie, font=("Century Schoolbook L", "15"))],
            [sg.Frame(layout=[
                [sg.Radio('Ja zacznę', "RADIO1", default=True, size=(30, 1), key='Gracz'),
                 sg.Radio('Niech zacznie komputer ', "RADIO1", size=(30, 1), key='Komputer')]
            ], title='Kto zaczyna ', title_color='blue', relief=sg.RELIEF_SUNKEN, tooltip='Wybierz swoją opcję')],
            [sg.Frame('Parametry', [
                                            [sg.Text('Liczność podzbioru',
                                                      font=("Century Schoolbook L", "10"), pad=(20,5)),
                                             sg.Text('Długość ciągu',
                                                      font=("Century Schoolbook L", "10"), pad=(20,5)),
                                             sg.Text('Poziom gry',
                                                      font=("Century Schoolbook L", "10"), pad=(20,5))

                                            ],
                                             [
                                             sg.Slider(range=(8, 50), orientation='v', size=(8, 25), default_value=25, pad=(45,5), key='licznosc'),
                                             sg.Slider(range=(3, 8), orientation='v', size=(8, 25), default_value=5, pad=(40,5), key='dlugosc'),
                                             sg.Slider(range=(1, 3), orientation='v', size=(8, 25), default_value=2, pad=(50,5), key='poziom')
                                            ]
                                        ]
                      )],

        [sg.Button('Zacznij grę'), sg.Button('Cofnij'), sg.Button('Exit')]
                  ]

        window1 = sg.Window('Window Title', location=location).Layout(layout)
        starting_window.Close()
        starting_window = window1

    if (event == 'Dalej') and values['Losowanie']:
        print(len(values))
        if len(values) >= 3:
            imie = values[0]
        randoms = get_data_randomly()
        print(randoms)
        print(values)
        temp_values.append(int(randoms[0]))
        temp_values.append(int(randoms[1]))
        temp_values.append(int(randoms[2]))
        temp_values.append(random.randint(0, 1))
        if temp_values[3] == 1:
            temp_computer_starts = True
        else:
            temp_computer_starts = False
        layout = [
            [sg.Text('Witamy w grze Szermerdiego', font=("Century Schoolbook L", "30"))],
            [sg.Text('Witaj  ', font=("Century Schoolbook L", "17")),
             sg.Text(imie, font=("Century Schoolbook L", "15"))],
            [sg.Text('Będziemy losować liczby z ciągu długości ', font=("Century Schoolbook L", "12")),
             sg.Text(randoms[0], font=("Century Schoolbook L", "12"))],
            [sg.Text('Wygrywa ciąg długości ', font=("Century Schoolbook L", "12")),
             sg.Text(randoms[1], font=("Century Schoolbook L", "12"))],
            [sg.Text('Poziom komputera jest ustawiony na ', font=("Century Schoolbook L", "12")),
             sg.Text(randoms[2], font=("Century Schoolbook L", "12"))],
            [sg.Text('Zaczyna ', font=("Century Schoolbook L", "12")),
             sg.Text(kto, font=("Century Schoolbook L", "12"))],
            [sg.Button('Zacznij grę'), sg.Button('Exit'), sg.Button('Cofnij')]
        ]
        print(values)

        window1 = sg.Window('Window Title', location=location).Layout(layout)
        starting_window.Close()
        starting_window = window1

    if event == 'Cofnij':
        layout = starting_layout
        window1 = sg.Window('Window Title', location=location).Layout(layout)
        starting_window.Close()
        starting_window = window1

    if event == 'Przeczytaj dokładniejszy opis':
        layout = [

            [sg.Text('Szczegółowy opis zasad: ', font=("Century Schoolbook L", "30"))],
            [sg.Text('Dokłady opis zasad: ', font=("Century Schoolbook L", "15"))],
            [sg.Text('1. Pierwsze zadanie polega na ustaleniu danych wejściowych – liczb naturalnych „x”, „k”', font=("Century Schoolbook L", "10"))],
            [sg.Text('oraz „z" - jednej liczby ze zbioru A={1, 2, 3}.  ', justification='center', font=("Century Schoolbook L", "10"))],
            [sg.Text('x  - oznacza liczność podzbioru liczb naturalnych jaki będzie wylosowany ', font=("Century Schoolbook L", "10"))],
            [sg.Text('przez komputer – jego właśnie elementy będą kolorowane, ', font=("Century Schoolbook L", "10"))],
            [sg.Text('k - informuje o długości ciągu monochromatycznego niezbędnego do zwycięstwa,', font=("Century Schoolbook L", "10"))],
            [sg.Text('z - ostatnia liczba odpowiada za poziom gry gracza komputerowego.', font=("Century Schoolbook L", "10"))],
            [sg.Text('2. Następnym krokiem jest dokonanie wyboru przez użytkownika „Kto będzie zaczynał grę?”',font=("Century Schoolbook L", "10"))],
            [sg.Text('* w naszym przykładzie załóżmy, że bedzie zaczynał gracz', font=("Century Schoolbook L", "10"))],
            [sg.Text('3. Po otrzymaniu tych informacji komputer losuje ciąg podanej długości,'
                     ' który będziemy chcieli kolorować.', font=("Century Schoolbook L", "10"))],
            [sg.Text('* Jeżeli z wylosowanego ciągu nie uda się stworzyć monochromatycznego ciągu arytmetycznego, ', font=("Century Schoolbook L", "10"))],
            [sg.Text('komputer wylosuje i sprawdzi ciąg jeszcze raz.', font=("Century Schoolbook L", "10"))],
            [sg.Text('Jeżeli dane będą poprawne przejdziemy do następnego kroku gry.', font=("Century Schoolbook L", "10"))],
            [sg.Text('4. Gracz i komputer na zmianę wybierają liczby, które chcieliby pokolować ', font=("Century Schoolbook L", "10"))],
            [sg.Text('5. Gra trwa do momentu gry:', font=("Century Schoolbook L", "10"))],
            [sg.Text('# jeden z graczy pokoloruje liczby tworzące arytmetyczny ciąg monochromatyczny długości k,', font=("Century Schoolbook L", "10"))],
            [sg.Text('# w trakcie rozgrywki nie będzie już możliwości utworzenia ciągu niezbędnego do wygrania z ', font=("Century Schoolbook L", "10"))],
            [sg.Text(' zakolorowanych i pozostałych liczb przez żadnego z graczy.', font=("Century Schoolbook L", "10"))],
            [sg.Button('Exit'), sg.Button('Cofnij')]


        ]

        window1 = sg.Window('Window Title', location=location).Layout(layout)
        starting_window.Close()
        starting_window = window1
    if event == 'Zacznij grę':
        print(values)
        print(len(values))
        if len(values) == 0:
            level = int(temp_values[2])
        else:
            level = int(values["poziom"])

        if len(values) == 0:
            target_length = int(temp_values[1])
        else:
            target_length = int(values["dlugosc"])

        if len(values) == 0:
            starting_amount = int(temp_values[0])
        else:
            starting_amount = int(values["licznosc"])

        if len(values) == 0:
            computer_starts = temp_values[3]
        else:
            computer_starts = values["Komputer"]

        print(temp_values)
        print(kto)
        print(values)
        # level = int(temp_values["poziom"])
        # target_length = int(temp_values["dlugosc"])
        if computer_starts == True:
            main_list = create_series_with_colour(starting_amount)
            while(check_monochrome_series(main_list, "black", "black", target_length)[0] == False):
                main_list = create_series_with_colour(starting_amount)
            main_list = computer_move(main_list, level, target_length)
        else:
            while (check_monochrome_series(main_list, "black", "black", target_length)[0] == False):
                main_list = create_series_with_colour(starting_amount)
        print(starting_amount)
        print(main_list)
        layout = [
            [sg.Text('Wybierz swoją liczbę', font=("Century Schoolbook L", "30"))],
            *[[sg.Text(main_list[x][0], text_color=main_list[x][1])
                for x in range(len(main_list))]],
            [sg.Text('Wpisz poniżej wybraną liczbę i naciśnij przycisk "Koloruj":', font=("Century Schoolbook L", "10"))],
            [sg.Input(do_not_clear=False, key='_IN_')],
            [sg.Button('Koloruj'), sg.Button('Cofnij'), sg.Button('Exit')]
        ]

        window1 = sg.Window('Window Title', location=location).Layout(layout)
        starting_window.Close()
        starting_window = window1
    if event == 'Koloruj':
        still_possible = True
        winner = ''
        if values["_IN_"] == '':
            print('brak podanej liczby')
            main_text = 'Musisz podać jakąś liczbę '
        elif int(values["_IN_"]) not in [main_list[x][0] for x in range(len(main_list))]:
            print([main_list[x][0] for x in range(len(main_list))])
            print('nie jest w liscie')
            main_text = """Podana liczba nie wystepuję w liście,
                        którą kolorujemy - wybierz inną liczbę"""
        elif main_list[find_index(int(values["_IN_"]), main_list)][1] == 'black':
            place = find_index(int(values["_IN_"]), main_list)
            main_list[place][1]='green'
            if check_monochrome_series(main_list, "green", "green", target_length)[0] is True:
                winner = 'Gracz'
                print('Winnerem jest gracz')

                layout = [
                    [sg.Text('Gratulacje! Wygrywasz tę rozgrywkę!', font=("Century Schoolbook L", "20"))],
                    *[[sg.Text(main_list[x][0], text_color=main_list[x][1])
                       for x in range(len(main_list)) if main_list[x][0] in check_monochrome_series(main_list, "green", "green", target_length)[1]]],
                    [sg.Text('Czy chcesz zagrać jeszcze raz?', font=("Century Schoolbook L", "12"))],

                    [sg.Button('Zagraj jeszcze raz'), sg.Button('Exit')]
                ]
                print(check_monochrome_series(main_list, "green", "green", target_length))

                window1 = sg.Window('Window Title', location=location).Layout(layout)
                starting_window.Close()
                starting_window = window1

            # elif possible_series(main_list, target_length) is False:
            #     winner = 'Nikt'
            #     print('Zagraj jeszcze raz')
            main_text = 'Wybierz swoją liczbę'
            if winner != 'Gracz' and possible_series(main_list, target_length):
                main_list = computer_move(main_list, level, target_length)
                print(main_list)
                if check_monochrome_series(main_list, "red", "red", target_length)[0] is True:
                    winner = 'Komputer'
                    print('Winnerem jest komputer')

                    layout = [
                        [sg.Text('Niestety, tym razem wygrał komputer', font=("Century Schoolbook L", "20"))],
                        *[[sg.Text(main_list[x][0], text_color=main_list[x][1])
                           for x in range(len(main_list)) if main_list[x][0] in check_monochrome_series(main_list, "red", "red", target_length)[1]]],

                        [sg.Text('Czy chcesz zagrać jeszcze raz?', font=("Century Schoolbook L", "12"))],

                        [sg.Button('Zagraj jeszcze raz'), sg.Button('Exit')]
                    ]
                    print(check_monochrome_series(main_list, "red", "red", target_length))

                    window1 = sg.Window('Window Title', location=location).Layout(layout)
                    starting_window.Close()
                    starting_window = window1

            # elif possible_series(main_list, target_length) is False:
            #     winner = 'Nikt'
            #     print('Zagraj jeszcze raz')
            elif possible_series(main_list, target_length) == False and len(winner) == 0:
                still_possible = False
                layout = [
                    [sg.Text('Niestety, w tej sytuacji żaden z graczy nie stworzy już ciagu zadanej długości', font=("Century Schoolbook L", "20"))],
                    [sg.Text('Czy chcesz zagrać jeszcze raz?', font=("Century Schoolbook L", "12"))],

                    [sg.Button('Zagraj jeszcze raz'), sg.Button('Exit')]
                ]

                window1 = sg.Window('Window Title', location=location).Layout(layout)
                starting_window.Close()
                starting_window = window1


        elif main_list[find_index(int(values["_IN_"]), main_list)][1] == 'red' or main_list[find_index(int(values["_IN_"]), main_list)][1] == 'green':
            main_text = 'Podana liczba jest już pokolorowana, wybierz inną'

        if len(winner) == 0 and still_possible:
            layout = [
                [sg.Text(main_text, font=("Century Schoolbook L", "30"))],
                *[[sg.Text(main_list[x][0], text_color=main_list[x][1])
                   for x in range(len(main_list))]],
                [sg.Text('Wpisz poniżej wybraną liczbę i naciśnij przycisk "Koloruj":', font=("Century Schoolbook L", "10"))],
                [sg.Input(do_not_clear=False, key='_IN_')],
                [sg.Button('Koloruj'), sg.Button('Cofnij'), sg.Button('Exit')]
            ]

        window1 = sg.Window('Window Title', location=location).Layout(layout)
        starting_window.Close()
        starting_window = window1
    if event == 'Zagraj jeszcze raz':

        layout = [
            [sg.Text('Witamy w grze Szemeredi\'ego', font=("Century Schoolbook L", "30"))],
            [sg.Text('Witaj  ', font=("Century Schoolbook L", "17")), sg.Text(imie, font=("Century Schoolbook L", "15"))],
            [sg.Frame(layout=[
                [sg.Radio('Wylosuj dla mnie zasady ', "RADIO1", default=True, size=(30, 1), key='Losowanie'),
                 sg.Radio('Sam wybiorę zasady', "RADIO1", size=(30, 1), key='Wybieranie')]
            ], title='Zasady gry', title_color='blue', relief=sg.RELIEF_SUNKEN, tooltip='Wybierz swoją opcję')],
            [sg.Text('Podstawowe zasady gry: ', font=("Century Schoolbook L", "15"))],
            [sg.Text('Komputer wraz z użytkownikiem kolorują na zmianę wybrane liczby z podanego zbioru',
                     font=("Century Schoolbook L", "10"), justification='right')],
            [sg.Text('pamiętając o tym, że można wybierać tylko liczbę niepokolorowaną. ',
                     font=("Century Schoolbook L", "10"))],
            [sg.Text(
                'Wygrywa ten, który jako pierwszy z pokolorowanych liczb stworzy arytmetyczny ciąg monochromatyczny* ',
                font=("Century Schoolbook L", "10"))],
            [sg.Button('Dalej'), sg.Button('Przeczytaj dokładniejszy opis'), sg.Button('Exit')]
        ]

        window1 = sg.Window('Window Title', location=location).Layout(layout)
        starting_window.Close()
        starting_window = window1





starting_window.Close()
#
# root = Tk.Tk()
# print(tkFont.families())
# print(tkFont.names())
#
# if values[2]:
#     starting_window = sg.Window('Window Title', layout + layout_two)
#     event, values = starting_window.Read()