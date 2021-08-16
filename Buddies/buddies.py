''' Who's your buddy ?'''

from datetime import timedelta, date, datetime
import unicodedata

NAME_LIST = [
    'Émeline', 'Anna', 'Prunelle', 'Thibault', 'Zacharie', 'Alix', 'Kenza',
    'Morgan', 'Selim', 'Stéphane', 'Antoine', 'Jean-Rémi', 'Jean', 'Krystelle',
    'Xavier', 'Bilel', 'Julien'
]

QUESTIONS = [[
    "Pour connaitre ton/tes buddies (0) ou l'ensemble des binômes (1) ? "
],
             [
                 "Pour avoir ton buddy de demain",
                 "Pour avoir ton buddy d'un jour précis",
                 "Pour avoir tes buddies de la semaine",
                 "Pour avoir tes buddies par semaine de batch (entre 1 et 7)",
                 "Pour avoir ton calendrier de buddies",
                 "Pour savoir quand quelqu'un sera ton buddy"
             ],
             [
                 "Pour avoir les binômes de demain",
                 "Pour avoir les binômes d'un jour précis",
                 "Pour avoir les binômes de la semaine",
                 "Pour avoir les binômes par semaine de batch (entre 1 et 7)",
                 "Pour avoir le calendrier des binômes"
             ]]


def name_norm(name):
    """Normalise le nom : quel que soit sa forme (sans accent, sans majuscule)
    met en forme le nom tel qu'il apparaît dans la liste (accents, majuscule)
    retourne une chaîne vide si ne trouve pas le nom dans la liste"""
    for elem in NAME_LIST:
        if unicodedata.normalize('NFKD', elem.lower()).encode('ASCII','ignore').decode() == \
            unicodedata.normalize('NFKD', name.lower()).encode('ASCII','ignore').decode():
            return elem
    return ""


def date_search(delta):
    """Retourne le +delta-ième jour ouvré"""
    day_origin = date(2021, 7, 5)
    while delta != 0:
        if day_origin.weekday() < 5:
            delta -= 1
        day_origin += timedelta(1)
    return day_origin


def buddy_date(name, buddy):
    """Retourne la ou les dates auxquelles name et buddy seront buddies
    sur l'intervalle 05/07 -> 20/08/21"""
    pos_ini = NAME_LIST.index(name)
    delta = (NAME_LIST.index(buddy) + pos_ini - 5 + len(NAME_LIST)) % 17
    # une fois qu'on a le delta on est obligé de parcourir le calendrier pour
    # ne compter que les jours ouvrables (sauter les week-end) : fonction date_search
    date1 = date_search(delta)
    dates = date1.strftime('%A %d/%m/%Y')
    date1 += timedelta(17)
    while date1 < date(2021, 8, 23):
        delta += 17
        dates += "\n" + date_search(delta).strftime('%A %d/%m/%Y')
        date1 += timedelta(17)
    return dates


def buddy_name(name, day_target):
    """retourne le nom du buddy à la date indiquée"""
    day_origin = date(2021, 7, 5)  # date de la remise à zéro des compteurs
    # nombre de jours ouvrés entre le 05/07 et le jour demandé
    # attention, pour simplifier la boucle le compteur passe à 1 dès premier jour
    nbr_days = 0
    while True:
        if day_origin.weekday() < 5:
            nbr_days += 1
        if day_origin == day_target:
            break
        day_origin += timedelta(1)
    # recherche du nom du buddy correspondant dans la liste
    i_bud = (len(NAME_LIST) - NAME_LIST.index(name) + 4 + nbr_days) % 17
    return NAME_LIST[(i_bud)]


def buddy_day(day_target):
    ''' retourne la liste des buddy à la date indiquée '''
    buddy_liste = []
    for i in sorted(NAME_LIST):
        buddy = buddy_name(i, day_target)
        if i[0] < buddy[0]:
            pair = (i, buddy)
        else:
            pair = (buddy, i)
        buddy_liste.append(pair)
    return set(buddy_liste)


def buddy_week(batch_week_number, name=NAME_LIST):
    ''' Affiche les dates du batch (entre 1 et 7) et les buddies de la personne ou tous les binomes'''
    day_origin = date(2021, 7, 5)
    day_target = day_origin + timedelta(7) * (batch_week_number - 1)
    for i in range(5):
        if name == NAME_LIST:
            print(day_target, ':\n', buddy_day(day_target))
        else:
            print(day_target, ':\n', buddy_name(name, day_target))
        print('\n')
        day_target += timedelta(1)
    return '\n'


def tomorrow():
    ''' Retourne la date du lendemain'''
    auj = date.today()
    if auj.weekday() == 4:
        demain = auj + timedelta(3)
    elif auj.weekday() == 5:
        demain = auj + timedelta(2)
    else:
        demain = auj + timedelta(1)
    return demain


def this_week():
    ''' Renvoie le numéro de semaine associé, la semaine suivante si la requête est effectuée samedi ou dimanche'''
    auj = date.today()
    day_origin = date(2021, 7, 2)
    for i in range(1, 8):
        for j in range(7):
            if auj != day_origin:
                day_origin += timedelta(1)
            else:
                break
        if auj == day_origin:
            week = i
            break
    print(day_origin)
    return week


def buddy_calendar(name=NAME_LIST):
    ''' Affiche les buddies ou binômes pour toutes les dates '''
    for week in range(1, 8):
        buddy_week(week, name)
    return '\n'


def which(all_or_not):
    ''' Demande à l'utilisateur ce qu'il souhaite savoir'''
    name = ''
    arg2 = ''
    if all_or_not:
        for i, j in enumerate(QUESTIONS[2]):
            print(i, ':', j)
        wish = int(input())
    else:
        for i, j in enumerate(QUESTIONS[1]):
            print(i, ':', j)
        wish = int(input())
        name = input('Prénom ?\n')
        name = name_norm(name)
    if wish == 5:
        arg2 = input("Prénom du buddy ?")
        arg2 = name_norm(arg2)
    elif wish == 1:
        arg2 = input(
            "Quelle date ?(JJ/MM/AAAA entre 05/07/2021 et 20/08/2021 inclus)")
        arg2 = datetime.strptime(arg2, '%d/%m/%Y')
        arg2 = arg2.date()
    elif wish == 3:
        arg2 = int(input("Quelle semaine ? (entre 1 et 7)"))
    return all_or_not, wish, arg2, name


def which_buddies(all_or_not, wish, arg2, name):
    ''' Renvoie à l'utilisateur ce qu'il souhaite savoir'''
    if wish == 0:
        if all_or_not:
            return buddy_day(tomorrow())
        else:
            return buddy_name(name, tomorrow())
    elif wish == 1:
        if all_or_not:
            return buddy_day(arg2)
        else:
            return buddy_name(name, arg2)
    elif wish == 2:
        if all_or_not:
            return buddy_week(this_week())
        else:
            return buddy_week(this_week(), name)
    elif wish == 3:
        if all_or_not:
            return buddy_week(arg2)
        else:
            return buddy_week(arg2, name)
    elif wish == 4:
        if all_or_not:
            return buddy_calendar()
        else:
            return buddy_calendar(name)
    elif wish == 5:
        return buddy_date(name, arg2)
    else:
        print("Hum... that's not possible")


if __name__ == '__main__':
    all_or_not = int(input(QUESTIONS[0][0]))
    all_or_not, wish, arg2, name = which(all_or_not)
    print(which_buddies(all_or_not, wish, arg2, name))
