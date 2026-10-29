// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Abfrage von Startinformationen und Vergabe/Rückgabe fester 4-KiB-Aufgabenbereiche; kein allgemeiner physischer Seitenverwalter. */
public final class Speicherraum {
    static int[] abschnittWert = new int[8192];
    static int[] benutzenWert = new int[8];

    static int ganzzahlAnalysieren(int adresse) {
        return Gerät.speicherLesen(adresse) | (Gerät.speicherLesen(adresse + 1) << 8)
            | (Gerät.speicherLesen(adresse + 2) << 16) | (Gerät.speicherLesen(adresse + 3) << 24);
    }

    static int obererSpeicherGröße() {
        int systemInformation = Gerät.startvorgangInformation();
        if (Gerät.startvorgangMarkierung() != 0x2badb002 || systemInformation == 0 || (ganzzahlAnalysieren(systemInformation) & 1) == 0) return -1;
        return ganzzahlAnalysieren(systemInformation + 8);
    }

    static int speichergerätZuteilen() {
        for (int Nummer = 0; Nummer < benutzenWert.length; Nummer++) {
            if (benutzenWert[Nummer] == 0) {
                benutzenWert[Nummer] = 1;
                for (int platzEintrag = 0; platzEintrag < 1024; platzEintrag++) abschnittWert[Nummer * 1024 + platzEintrag] = 0;
                return Nummer;
            }
        }
        return -1;
    }

    static boolean zurückkehrenErgebnis(int Nummer) {
        if (Nummer < 0 || Nummer >= benutzenWert.length || benutzenWert[Nummer] == 0) return false;
        benutzenWert[Nummer] = 0;
        return true;
    }

    static int benutztEintragAnzahl() {
        int elementeintragAnzahl = 0;
        for (int Nummer = 0; Nummer < benutzenWert.length; Nummer++) elementeintragAnzahl += benutzenWert[Nummer];
        return elementeintragAnzahl;
    }
}
