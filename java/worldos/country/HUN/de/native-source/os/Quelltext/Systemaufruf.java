// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Aufruf über das int-0x80-Gatter. Alle Benutzerzeiger und Längen vor dem Zugriff prüfen. */
public final class Systemaufruf {
    static int[] vorläufigPuffer = new int[1024];

    static int datenfeldLänge(int adresse) {
        if (!Ausführungsverwaltung.beschneiden(adresse, 4)) return -14;
        int Länge = Ausführungsverwaltung.Zahl(adresse);
        if (Länge < 0 || Länge > (Ausführungsverwaltung.benutzerEnde - adresse - 4) / 4) return -14;
        return Länge;
    }

    public static int prozessWertEintrag(int Nummer, int ersterOperand, int zweiterOperand, int dritterOperand, int vierterOperand, int fünfterOperand) {
        if (Nummer == 30) return Dateideskriptorverwaltung.dateiÖffnen(ersterOperand, zweiterOperand, dritterOperand);
        if (Nummer == 31) return Dateideskriptorverwaltung.dateiLesen(ersterOperand, zweiterOperand, dritterOperand);
        if (Nummer == 32) return Dateideskriptorverwaltung.dateiSchreiben(ersterOperand, zweiterOperand, dritterOperand);
        if (Nummer == 33) return Dateideskriptorverwaltung.dateiSchließen(ersterOperand);
        if (Nummer == 34) return Dateideskriptorverwaltung.dateiPositionieren(ersterOperand, zweiterOperand, dritterOperand);
        if (Nummer == 35) return Dateideskriptorverwaltung.duplikatDeskriptor(ersterOperand, 0, false, 0);
        if (Nummer == 36) return Dateideskriptorverwaltung.duplikatDeskriptor(ersterOperand, zweiterOperand, true, 0);
        if (Nummer == 37) return Dateideskriptorverwaltung.dateiZustandLesen(ersterOperand, zweiterOperand);
        if (Nummer == 38) return Dateideskriptorverwaltung.dateiEintragNameEntfernen(ersterOperand);
        if (Nummer == 39) return Dateideskriptorverwaltung.dateiLängeSetzen(ersterOperand, zweiterOperand);
        if (Nummer == 40) return Dateideskriptorverwaltung.steuerungDeskriptor(ersterOperand, zweiterOperand, dritterOperand);
        if (Nummer == 41) return Dateideskriptorverwaltung.endpunktErstellen(ersterOperand, zweiterOperand, dritterOperand);
        if (Nummer == 42) return Dateideskriptorverwaltung.adresseZuordnen(ersterOperand, zweiterOperand, dritterOperand);
        if (Nummer == 43) return Dateideskriptorverwaltung.datagrammDatenSenden(ersterOperand, zweiterOperand, dritterOperand, vierterOperand, fünfterOperand);
        if (Nummer == 44) return Dateideskriptorverwaltung.datagrammDatenEmpfangen(ersterOperand, zweiterOperand, dritterOperand, vierterOperand, fünfterOperand);
        if (Nummer == 45) return Dateideskriptorverwaltung.netzbuchseAdresseLesen(ersterOperand, zweiterOperand, dritterOperand);
        if (Nummer == 46) return Dateideskriptorverwaltung.empfangenZeitüberschreitungSetzen(ersterOperand, zweiterOperand);
        if (Nummer == 47) {
            int deskriptorWert = Dateideskriptorverwaltung.deskriptorFinden(ersterOperand);
            if (deskriptorWert < 0) return -9;
            if (Dateideskriptorverwaltung.artWert[deskriptorWert] != 2) return -22;
            return Dateibeständigkeit.synchronisieren();
        }
        if (Nummer == 1) {
            int Länge = datenfeldLänge(ersterOperand);
            if (Länge < 0) return Länge;
            if (Länge > 4096) return -90;
            for (int zeichenWert = 0; zeichenWert < Länge; zeichenWert++) Zeichenterminal.Zeichen(Ausführungsverwaltung.Zahl(ersterOperand + 4 + zeichenWert * 4) & 65535);
            return Länge;
        }
        if (Nummer == 2) return Ausführungsverwaltung.argumentAnzahl;
        if (Nummer == 3) return ersterOperand >= 0 && ersterOperand < Ausführungsverwaltung.argumentAnzahl ? Ausführungsverwaltung.argumentAdresse[ersterOperand] : 0;
        if (Nummer == 10) return Netzwerkstapel.öffnen(ersterOperand);
        if (Nummer == 11) {
            int Länge = datenfeldLänge(vierterOperand);
            if (Länge < 0) return Länge;
            if (fünfterOperand < 0 || fünfterOperand > Länge || fünfterOperand > 1024) return -90;
            for (int position = 0; position < fünfterOperand; position++) vorläufigPuffer[position] = Ausführungsverwaltung.Zahl(vierterOperand + 4 + position * 4) & 255;
            return Netzwerkstapel.senden(ersterOperand, zweiterOperand, dritterOperand, vorläufigPuffer, fünfterOperand);
        }
        if (Nummer == 12) {
            int Länge = datenfeldLänge(zweiterOperand);
            if (Länge < 0) return Länge;
            if (dritterOperand < 0 || dritterOperand > 2000) return -22;
            int ergebnis = Netzwerkstapel.empfangen(ersterOperand, vorläufigPuffer, Länge < 1024 ? Länge : 1024, dritterOperand);
            if (ergebnis >= 0) for (int position = 0; position < ergebnis; position++) Ausführungsverwaltung.nummerSchreiben(zweiterOperand + 4 + position * 4, vorläufigPuffer[position]);
            return ergebnis;
        }
        if (Nummer == 13) return Netzwerkstapel.schließen(ersterOperand);
        if (Nummer == 14) return Netzwerkstapel.eigenAdresse;
        if (Nummer == 15) return Netzwerkstapel.gegenstelleAdresse(ersterOperand);
        if (Nummer == 16) return Netzwerkstapel.gegenstellePortNummer(ersterOperand);
        if (Nummer == 22) {
            if (ersterOperand < 0 || ersterOperand > 65535) return -22;
            Zeichenterminal.Zeichen(ersterOperand); return 1;
        }
        if (Nummer == 20 || Nummer == 21) {
            int nameGröße = datenfeldLänge(ersterOperand), datenGröße = datenfeldLänge(zweiterOperand);
            if (nameGröße < 0 || datenGröße < 0) return -14;
            if (nameGröße < 1 || nameGröße > 64) return -22;
            int Länge = 0;
            while (Länge < nameGröße && Ausführungsverwaltung.Zahl(ersterOperand + 4 + Länge * 4) != 0) {
                ArbeitsspeicherDateisystem.Name[Länge] = Ausführungsverwaltung.Zahl(ersterOperand + 4 + Länge * 4);
                Länge++;
            }
            if (!ArbeitsspeicherDateisystem.namePrüfen(ArbeitsspeicherDateisystem.Name, Länge)) return -22;
            if (Nummer == 20) {
                int Datei = ArbeitsspeicherDateisystem.eintragFinden(ArbeitsspeicherDateisystem.Name, Länge);
                if (Datei < 0) return Datei;
                int größe = ArbeitsspeicherDateisystem.größeListe[Datei];
                if (größe > datenGröße) return -90;
                int adresse = Gerät.dateiSpeicher() + Datei * ArbeitsspeicherDateisystem.höchstwertGröße;
                for (int Zahl = 0; Zahl < größe; Zahl++) Ausführungsverwaltung.nummerSchreiben(zweiterOperand + 4 + Zahl * 4, Gerät.speicherLesen(adresse + Zahl));
                return größe;
            }
            if (dritterOperand < 0 || dritterOperand > datenGröße) return -22;
            if (dritterOperand > ArbeitsspeicherDateisystem.höchstwertGröße) return -90;
            for (int Zahl = 0; Zahl < dritterOperand; Zahl++) ArbeitsspeicherDateisystem.bearbeitenWert[Zahl] = Ausführungsverwaltung.Zahl(zweiterOperand + 4 + Zahl * 4) & 255;
            return ArbeitsspeicherDateisystem.ablegenDatenWert(ArbeitsspeicherDateisystem.Name, Länge, ArbeitsspeicherDateisystem.bearbeitenWert, dritterOperand);
        }
        return -38;
    }
}
