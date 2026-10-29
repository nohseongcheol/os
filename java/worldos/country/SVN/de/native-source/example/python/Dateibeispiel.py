from Deutsch import Ausgabe, dateiSchreiben, dateiLesen, textKodieren, textDekodieren
Daten = "PYTHON Datei: de 😀\n"
dateiSchreiben("python.txt", textKodieren(Daten))
textWertLesen = textDekodieren(dateiLesen("python.txt"))
assert textWertLesen == Daten
Ausgabe(textWertLesen, endung="")
