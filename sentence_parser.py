# -*- coding: utf-8 -*-
#! /usr/bin/python3

# INL 2016
# Podział tekstu na zdania

import sys
import codecs

abbrevs = [
    'a',
    'alb',
    'amer',
    'anat',
    'ang',
    'antr',
    'ar',
    'archeol',
    'archit',
    'astr',
    'austr',
    'austral',
    'B',
    'białorus',
    'biol',
    'blm',
    'blp',
    'bot',
    'bułg',
    'C',
    'celt',
    'chem',
    'chiń',
    'chrześc',
    'cz',
    'czas',
    'czes',
    'D',
    'daw',
    'dk',
    'druk',
    'dziec',
    'e',
    'egip',
    'ekon',
    'elektr',
    'etn',
    'euf',
    'film',
    'filoz',
    'fiń',
    'fiz',
    'fizjol',
    'fot',
    'fr',
    'fraz',
    'fragm',
    'genet',
    'geogr',
    'geol',
    'geom',
    'godz'
    'gr',
    'gw',
    'hand',
    'hebr',
    'hind',
    'hist',
    'hiszp',
    'hol',
    'im',
    'imiesł',
    'in',
    'inf',
    'inform',
    'inż',
    'irl',
    'iron',
    'isl',
    'itd',
    'itp',
    'jap',
    'jęz',
    'kg',
    'km',
    'lit',
    'lm',
    'łac',
    'M',
    'm',
    'mat',
    'med',
    'meteor',
    'min',
    'm',
    'miner',
    'mit',
    'mit',
    'mit',
    'mit',
    'mors',
    'm',
    'Ms',
    'muz',
    'N',
    'n',
    'ndk',
    'ndm',
    'n',
    'nieos',
    'niem',
    'nm',
    'norw',
    'np',
    'obelż',
    'odm',
    'ok',
    'os',
    'p',
    'płd',
    'płn',
    'p',
    'pocz',
    'poet',
    'pol',
    'polit',
    'poł',
    'popr',
    'por',
    'port',
    'posp',
    'pot',
    'praw',
    'prof',
    'przen',
    'przestarz',
    'przesz',
    'przym',
    'przysł',
    'przysłów',
    'przysz',
    'psychol',
    'r',
    'reg',
    'rel',
    'rodz',
    'roln',
    'ros',
    'rub',
    'rum',
    'rzad',
    'rzecz',
    'rzym',
    'sek',
    'skand',
    'skrót',
    'słowac',
    'socjol',
    'sport',
    'st',
    'starop',
    'staroż',
    'szt',
    'szwedz',
    'śr',
    'środ',
    'św',
    'Św',
    't',
    'teatr',
    'techn',
    'temp',
    'ter',
    'tj',
    'tur',
    'tur',
    'tys',
    'tzn',
    'uczn',
    'ukr',
    'ur',
    'urb',
    'W',
    'w',
    'węg',
    'wg',
    'wł',
    'wojsk',
    'wsch',
    'wsp',
    'współ',
    'wulg',
    'wym',
    'zach',
    'zdr',
    'zgr',
    'zm',
    'zn',
    'zool',
    'zwł',
    'ż',
    'żart',
    'żegl'
]

if len(sys.argv) < 2:
    exit('''Musisz podać ścieżkę do pliku z tekstem. Ścieżka wyjściowego
            pliku XML jest opcjonalna. W przypadku braku podania wynik
            zostanie wypisany na standardowe wyjście.\n
            Użycie:\n
            python sentence_parser.py <plik wejściowy> [plik wyjściowy]''')
text_path = sys.argv[1]
xml_path = sys.argv[2] if len(sys.argv) >= 3 else None
try:
    with open(text_path, encoding='utf-8') as f:
        text = f.read()
except:
    exit('Nie można było otworzyć pliku.')


def parse_paragraphs(text):
    '''Funkcja dzieli tekst na paragrafy i zwraca listę, w której,
       każdy element jest paragrafem.'''
    paragraphs = []
    lines = [line.strip() for line in text.split('\n')]
    for line in lines:
        # jeżeli jest to pierwszy paragraf, pusta linia lub poprzednia
        # linia była pusta dodaj nowy paragraf
        if len(paragraphs) == 0 or line == '' or paragraphs[-1] == '':
            paragraphs.append(line)
        # jeśli linia zaczyna się z małej litery połącz ją z poprzednim
        # paragrafem
        elif line[0].islower():  # or ('.' in paragraphs[-1]):  ?
            paragraphs[-1] += ' ' + line
        # w przeciwnym przypadku dodaj linię do poprzedniego paragrafu
        else:
            paragraphs[-1] += '\n' + line
    # usuń puste linie
    paragraphs = [p for p in paragraphs if p != '']
    return paragraphs


def last_word(sentence):
    '''Funkcja znajduje ostatnie słowo w zdaniu.
       Szuka od końca znaku, który nie jest literą lub cyfrą'''
    for i in range(-1, -len(sentence) - 1, -1):
        if sentence[i] in ' ,./<>?;'':"[]{}\|-=_+()!@#$%^&*`‘~':
            if i == -1:
                return ''
            return sentence[i + 1:]
    return sentence


def parse_sentences(paragraphs):
    '''Funkcja parsuje paragrafy na zdania.
       Zwraca listę, której każdy element reprezentuje
       paragraf - jest listą, zawierającą zdania'''
    result = []
    for p in paragraphs:
        lines = p.split('\n')
        result.append([])
        for line in lines:
            # jeśli nie ma kropki w zdaniu oznacza, że jest to tytuł
            if '.' not in line:
                result[-1].append(line)
                continue
            # upraszczamy, zamieniając zdania pytające i rozkazujące
            # na zwykłe zdania
            line.replace('!', '.')
            line.replace('?', '.')
            tokens = line.split('.')
            for i, copy in enumerate(tokens):
                token = copy.strip()
                if token == '':
                    continue
                if i == 0:
                    result[-1].append(token)
                    continue
                # ostatnie słowo ostatniego zdania
                last = last_word(result[-1][-1])
                # jeżeli ostatnie słowo jest skrótem zdanie zostaje
                # dołączone do poprzedniego
                if last in abbrevs:
                    result[-1][-1] += '. ' + token
                # jeżeli ostatnie słowo jest liczbą zostaje dołączone do
                # poprzedniego
                elif last.isdigit():
                    if copy[0].isdigit():
                        result[-1][-1] += '.' + token
                    else:
                        result[-1][-1] += '. ' + token
                # jeżeli ostatnie słowo jest z dużej litery i ma 1 lub 2 litery
                # oznacza to, że jest skrótem imienia lub nazwiska
                elif last.istitle() and len(last) <= 2:  # and token.istitle():
                    result[-1][-1] += '. ' + token
                # w przeciwnym razie zdanie zostaje dodane jako nowe zdanie
                else:
                    result[-1].append(token)
    return result


def sentences_to_xml(paragraphs):
    '''Funkcja zwraca tekst w formacie XML'''
    result = '<?xml version="1.0" encoding="UTF-8"?>\n\
<text>\n'
    for i, p in enumerate(paragraphs, start=1):
        result += '  <p xml:id="{0}-p">\n'.format(i)
        for j, s in enumerate(p, start=1):
            result += '    <s xml:id="{0}-{1}-s">{2}.</s>\n'.format(i, j, s)
        result += '  </p>\n'
    result += '</text>'
    return result


paragraphs = parse_paragraphs(text)
result = parse_sentences(paragraphs)

xml = sentences_to_xml(result)
if xml_path is None:
    # sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    # print(xml)
    print(xml.encode(sys.stdout.encoding, errors='replace'))
else:
    with open(xml_path, mode='w', encoding='utf-8') as out:
        out.write(xml)
