// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Prüft ELF32 in schreibgeschützten Ausführungsbündeln, übergibt Argumente und führt jeweils einen Benutzerprozess aus. */
public final class Ausführungsverwaltung {
    static final int benutzerProgrammStarten = 0x04000000;
    static final int benutzerEnde = 0x04400000;
    static final int abbildEndeAdresse = 0x04200000;
    static final int argumentStarten = 0x04300000;
    static int argumentAnzahl = 0;
    static int[] argumentAdresse = new int[16];

    static boolean beschneiden(int adresse, int Länge) {
        return adresse >= benutzerProgrammStarten && adresse < benutzerEnde && Länge >= 0 && Länge <= benutzerEnde - adresse;
    }

    static int Zahl(int adresse) { return Speicherraum.ganzzahlAnalysieren(adresse); }
    static int kurzWert(int adresse) { return Gerät.speicherLesen(adresse) | Gerät.speicherLesen(adresse + 1) << 8; }
    static void nummerSchreiben(int adresse, int Wert) {
        for (int Nummer = 0; Nummer < 4; Nummer++) Gerät.speicherSchreiben(adresse + Nummer, Wert >>> (Nummer * 8));
    }

    static int gruppeAnzahl() {
        int adresse = Gerät.AusführdateiBündel();
        int größe = Gerät.ausführdateiBündelGröße();
        if (größe < 8 || Zahl(adresse) != 0x50414b4a) return 0;
        int elementeintragAnzahl = Zahl(adresse + 4);
        return elementeintragAnzahl >= 0 && elementeintragAnzahl <= 32 && elementeintragAnzahl <= (größe - 8) / 24 ? elementeintragAnzahl : 0;
    }

    static void eintragListe() {
        for (int Nummer = 0; Nummer < gruppeAnzahl(); Nummer++) {
            int eintragWert = Gerät.AusführdateiBündel() + 8 + Nummer * 24;
            for (int zeichenWert = 0; zeichenWert < 16 && Gerät.speicherLesen(eintragWert + zeichenWert) != 0; zeichenWert++)
                Zeichenterminal.Zeichen(Gerät.speicherLesen(eintragWert + zeichenWert));
            Zeichenterminal.schreiben("\n");
        }
    }

    static int eintragFinden(int[] Eingabewert, int ausführenVorgang, int Länge) {
        if (Länge <= 0 || Länge >= 16) return 0;
        for (int Nummer = 0; Nummer < gruppeAnzahl(); Nummer++) {
            int eintragWert = Gerät.AusführdateiBündel() + 8 + Nummer * 24;
            boolean gleichText = Gerät.speicherLesen(eintragWert + Länge) == 0;
            for (int zeichenWert = 0; zeichenWert < Länge; zeichenWert++)
                if (Eingabewert[ausführenVorgang + zeichenWert] != Gerät.speicherLesen(eintragWert + zeichenWert)) gleichText = false;
            if (gleichText) return eintragWert;
        }
        return 0;
    }

    static int validieren(int Datei, int Länge) {
        if (Länge < 52 || Zahl(Datei) != 0x464c457f || Gerät.speicherLesen(Datei + 4) != 1
            || Gerät.speicherLesen(Datei + 5) != 1 || Gerät.speicherLesen(Datei + 6) != 1
            || kurzWert(Datei + 16) != 2 || kurzWert(Datei + 18) != 3 || Zahl(Datei + 20) != 1
            || kurzWert(Datei + 40) != 52 || kurzWert(Datei + 42) != 32) return -8;
        int eintragPunktWert = Zahl(Datei + 24);
        int tabellePosition = Zahl(Datei + 28);
        int elementeintragAnzahl = kurzWert(Datei + 44);
        if (elementeintragAnzahl == 0 || elementeintragAnzahl > 16 || tabellePosition < 52 || tabellePosition > Länge - elementeintragAnzahl * 32) return -8;
        boolean istAusführdatei = false;
        for (int Nummer = 0; Nummer < elementeintragAnzahl; Nummer++) {
            int Tabelle = Datei + tabellePosition + Nummer * 32;
            int artWert = Zahl(Tabelle);
            if (artWert == 2 || artWert == 3) return -8; // Keine Unterstützung für dynamisches Binden oder einen Interpreter.
            if (artWert != 1) continue;
            int position = Zahl(Tabelle + 4), adresse = Zahl(Tabelle + 8), dateiGröße = Zahl(Tabelle + 16), speicherGröße = Zahl(Tabelle + 20);
            int ausrichtenWert = Zahl(Tabelle + 28);
            if (adresse < benutzerProgrammStarten || adresse >= abbildEndeAdresse || speicherGröße < 0 || speicherGröße > abbildEndeAdresse - adresse
                || dateiGröße < 0 || dateiGröße > speicherGröße || position < 0 || (dateiGröße > 0 && position > Länge - dateiGröße)
                || (ausrichtenWert != 0 && (ausrichtenWert < 0 || (ausrichtenWert & (ausrichtenWert - 1)) != 0
                    || ((adresse - position) & (ausrichtenWert - 1)) != 0))) return -8;
            for (int vorderseiteWert = 0; vorderseiteWert < Nummer; vorderseiteWert++) {
                int vorherigElementeintrag = Datei + tabellePosition + vorderseiteWert * 32;
                if (Zahl(vorherigElementeintrag) == 1 && speicherGröße > 0 && Zahl(vorherigElementeintrag + 20) > 0
                    && adresse < Zahl(vorherigElementeintrag + 8) + Zahl(vorherigElementeintrag + 20) && Zahl(vorherigElementeintrag + 8) < adresse + speicherGröße) return -8;
            }
            if ((Zahl(Tabelle + 24) & 1) != 0 && eintragPunktWert >= adresse && eintragPunktWert - adresse < dateiGröße) istAusführdatei = true;
        }
        return istAusführdatei ? eintragPunktWert : -8;
    }

    static int befehlAusführen(int[] Eingabewert, int ausführenVorgang, int Länge) {
        while (ausführenVorgang < Länge && Eingabewert[ausführenVorgang] == ' ') ausführenVorgang++;
        int endung = ausführenVorgang;
        while (endung < Länge && Eingabewert[endung] != ' ') endung++;
        int eintragWert = eintragFinden(Eingabewert, ausführenVorgang, endung - ausführenVorgang);
        if (eintragWert == 0) return -2;
        int position = Zahl(eintragWert + 16), größe = Zahl(eintragWert + 20);
        if (position < 8 + gruppeAnzahl() * 24 || größe < 52 || position > Gerät.ausführdateiBündelGröße() - größe) return -8;
        int Datei = Gerät.AusführdateiBündel() + position;
        int eintragPunktWert = validieren(Datei, größe);
        if (eintragPunktWert < 0) return eintragPunktWert;
        Gerät.benutzerLöschenInhaltInhalt();
        int tabellePosition = Zahl(Datei + 28), elementeintragAnzahl = kurzWert(Datei + 44);
        for (int Nummer = 0; Nummer < elementeintragAnzahl; Nummer++) {
            int Tabelle = Datei + tabellePosition + Nummer * 32;
            if (Zahl(Tabelle) != 1) continue;
            int ursprünglich = Datei + Zahl(Tabelle + 4), zielWert = Zahl(Tabelle + 8), dateiGröße = Zahl(Tabelle + 16);
            for (int byteWert = 0; byteWert < dateiGröße; byteWert++) Gerät.speicherSchreiben(zielWert + byteWert, Gerät.speicherLesen(ursprünglich + byteWert));
        }
        argumentAnzahl = 0;
        int ablegenDatenWert = argumentStarten;
        while (endung < Länge) {
            while (endung < Länge && Eingabewert[endung] == ' ') endung++;
            if (endung == Länge) break;
            if (argumentAnzahl == argumentAdresse.length) return -22;
            ausführenVorgang = endung;
            while (endung < Länge && Eingabewert[endung] != ' ') endung++;
            argumentAdresse[argumentAnzahl++] = ablegenDatenWert;
            nummerSchreiben(ablegenDatenWert, endung - ausführenVorgang);
            for (int zeichenWert = ausführenVorgang; zeichenWert < endung; zeichenWert++) nummerSchreiben(ablegenDatenWert + 4 + (zeichenWert - ausführenVorgang) * 4, Eingabewert[zeichenWert]);
            ablegenDatenWert += 4 + (endung - ausführenVorgang) * 4;
        }
        Netzwerkstapel.bereinigenProzess();
        Dateideskriptorverwaltung.prozessStarten();
        int ergebnis = Gerät.benutzerProgrammAusführenVorgang(eintragPunktWert, benutzerEnde - 16);
        Dateideskriptorverwaltung.bereinigenProzess();
        Netzwerkstapel.bereinigenProzess();
        return ergebnis;
    }
}
