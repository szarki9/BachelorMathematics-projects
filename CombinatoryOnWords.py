from termcolor import colored
import string, random, time
alphabet = list(string.ascii_lowercase)


def game():
    welcome()
    play_again = 'T'

    while(play_again[0] == 'T' or play_again[0] == 't'):
        game_mode = game_mode_choose()
        max_length = get_max_length()
        alphabet_size = get_alphabet_size()
        letters = alphabet[:alphabet_size]
        print("Będziemy budować słowa z liter: ")
        print(letters)
        word = ''
        if game_mode != 4:
            first_letter = get_new_letter(letters)
            word = str(first_letter)
            print_our_word2(word, 0)
        word = go_to_game_mode(word, letters, max_length, game_mode)
        play_again = input('Czy chcesz zagrać jeszcze raz? Jeśli tak, wpisz "T" i naciśnij Enter?')

    if play_again[0] != 'T' and play_again[0] != 't':
        print("Dzięki za grę! Do zobaczenia ponownie!")
    return word


def player1_move(word, letters):
    place = input("Graczu 1, podaj miejsce: ")
    marker = 0
    while(marker<1):
        while (place.isnumeric() == False or (place.isnumeric()==True and (int(place)<0))):
            print("To nie jest liczba naturalna :(")
            place = input("Graczu 1, podaj miejsce: ")
        place = int(place)
        if(place>len(word)):
            print("Za duże :( Miejsce nie powinno przekraczać długości słowa.")
            place = input("Graczu 1, podaj miejsce: ")
        else: marker = 1
    return place


def player2_move(word, letters, place):
    a = word[:place]
    b = word[place:]
    if place==0: print("Graczu 2, wstaw literę na początek słowa.")
    elif place==len(word): print("Graczu 2, wstaw literę na koniec słowa.")
    else: print('Graczu 2, wstaw literę w miejsce "_": ' + a + "_" + b + ".")
    new_letter = get_new_letter(letters)
    word = word[:place] + new_letter + word[place:]
    print_our_word2(word, place)
    return word


def comp1_move(word):
    place = random.randint(0, len(word))
    if word != '':
        print("Komputer 1 wybrał miejsce nr " + str(place) + ".")
    return place


def comp2_move(word, letters, place):
    new_letter = letters[random.randint(0, len(letters) - 1)]
    print("Komputer 2 wybrał literę " + new_letter +'.')
    word = word[:place] + new_letter + word[place:]
    print_our_word2(word, place)
    return word


def repetitions(word):
    length = len(word)
    n = int(length/2)
    #print(length,n)
    for frag_len in range(2, n+1):
        for index in range(length-2*frag_len+1):
            a = word[index:index+frag_len]
            b = word[index+frag_len:index+2*frag_len]
            #print(frag_len, index, a, b)
            if(a==b): return True
    return False


def get_max_length():
    max_length = input("Podaj długość rozgrywki = długość słowa (liczbę naturalną większą niż 1): ")
    while (max_length.isnumeric() == False or (max_length.isnumeric() == True and (int(max_length) <= 1))):
        print("To nie jest liczba naturalna większa niż 1 :(")
        max_length = input("Podaj długość rozgrywki = długość słowa (liczbę naturalną): ")
    max_length = int(max_length)
    return max_length-1


def get_alphabet_size():
    alphabet_size = input("Podaj długość alfabetu (liczę naturalną od 3 do 26): ")
    while (alphabet_size.isnumeric() == False or (alphabet_size.isnumeric() == True and (int(alphabet_size) > 27 or int(alphabet_size) < 3))):
        print("To nie jest liczba naturalna od 3 do 26 :(")
        alphabet_size = input("Podaj długość alfabetu (liczę naturalną od 3 do 26): ")
    alphabet_size = int(alphabet_size)
    return alphabet_size


def get_new_letter(letters):
    new_letter = input("Podaj literę: ")
    while (new_letter not in letters):
        print("To nie jest litera z powyższej listy. Podaj literę, która występuje w alfabecie do litery " + letters[-1] + ".")
        new_letter = input("Podaj literę: ")
    return new_letter


def human_vs_human(word, letters, max_length):
    while (len(word) <= max_length):
        place = player1_move(word, letters)
        word = player2_move(word, letters, place)
        if (repetitions(word)):
            print("Repetycja! Gracz 2 wygrał!")
            return word
    print("Nie było repetycji. Wygrał gracz 1.")
    return word


def human_vs_comp(word, letters, max_lenght):
  while (len(word) <= max_lenght):
    place = player1_move(word, letters)
    word = comp2_move(word, letters, place)
    if (repetitions(word)):
            print("Repetycja! Gracz 2 wygrał!")
            return word
  print("Nie było repetycji. Wygrał gracz 1.")
  return word


def comp_vs_comp(word, letters, max_lenght):
  while (len(word) <= max_lenght):
    place = comp1_move(word)
    time.sleep(2.5)
    word = comp2_move(word, letters, place)
    time.sleep(2.5)
    if (repetitions(word)):
            print("Repetycja! Komputer 2 wygrał!")
            return word
  print("Nie było repetycji. Wygrał komputer 1.")
  return word


def comp_vs_human(word, letters, max_lenght):
  while (len(word) <= max_lenght):
    place = comp1_move(word)
    word = player2_move(word, letters, place)
    if (repetitions(word)):
            print("Repetycja! Gracz 2 wygrał!")
            return word
  print("Nie było repetycji. Wygrał gracz 1.")
  return word


def go_to_game_mode(word, letters, max_lenght, level):
  if level==1:
    return human_vs_human(word, letters, max_lenght)
  elif level==2:
    return human_vs_comp(word, letters, max_lenght)
  elif level==3:
    return comp_vs_human(word, letters, max_lenght)
  elif level==4:
    return comp_vs_comp(word, letters, max_lenght)


def game_mode_choose():
    print("Wybierz poziom tryb gry: ")
    level = input(
        "1. Gra dwuosobowa, 2. Gra człowiek kontra komputer, 3. Gra komputer kontra człowiek, 4. Symulacja gry komputer kontra komputer:")
    while level.isdigit() == 0 or (int(level) != 1 and int(level) != 2 and int(level) != 3 and int(level) != 4):
        level = input("Podaj poprawną wartość! Możesz wybrać 1,2,3 lub 4. Podaj jeszcze raz:")
    return int(level)


def welcome():
    print("Cześć, gracze! Zagramy w grę.")


def our_word(word):
    n = len(word)
    word_a_list = list()
    word_b_list = list()
    for k in range(n):
        for l in range(len(str(k))):
            word_a_list.append('_')
        word_a_list.append(word[k])
    for l in range(len(str(n+1))):
        word_a_list.append('_')
    for k in range(n):
        word_b_list.append(str(k))
        word_b_list.append('_')
    word_b_list.append(str(n))
    word_a = ''.join(word_a_list)
    word_b = ''.join(word_b_list)
    return word_a, word_b


def print_our_word(word):
    x, y = our_word(word)
    print('Nasze słowo to: ' + word + '.')
    print(x)
    print(y)


def our_word2(word, place):
    n = len(word)
    word_a_list = list()
    word_b_list = list()
    for k in range(n):
        for l in range(len(str(k))):
            word_a_list.append('_')
        word_a_list.append(word[k])
        if k == int(place):
            new_place = len(word_a_list)
    for l in range(len(str(n+1))):
        word_a_list.append('_')
    for k in range(n):
        word_b_list.append(str(k))
        word_b_list.append('_')
    word_b_list.append(str(n))
    word_a = ''.join(colored(word_a_list[index], 'red') if index == new_place
                     else word_a_list[index]
                     for index in range(len(word_a_list)))
    word_b = ''.join(word_b_list)
    return word_a, word_b



def print_our_word2(word, place):
    #x, y = Our_Word2(word, place)
    x, y = our_word(word)
    word_col = list(word)
    col_word = ''.join(colored(word_col[index], 'red') if index == place
                     else word_col[index]
                     for index in range(len(word_col)))
    print('Nasze słowo to: ' + col_word + '.')
    print(x)
    print(y)


game()

#Print_Our_Word('marchewkowyburak')
#Print_Our_Word2('marchewkowyburak', 7)



#list = ["bubu", "orooro", "butbu", "abubu", "asbubu", "imdsfgbubu","iamdsfgbubu", "matematemate", "matemate"]
#for x in list:
#    print(x + ": " + str(Repetitions(x)))
