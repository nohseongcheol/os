import Deutsch

def grüßen(Name):
    gruß = "안녕하세요 " + Name
    Deutsch.dateiSchreiben("Gruß.txt", gruß)
    Deutsch.Ausgabe(Deutsch.textDekodieren(Deutsch.dateiLesen("Gruß.txt")))

grüßen("누리")
