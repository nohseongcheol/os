// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Kleines eigenes Speicherformat mit Prüfsummen und zwei Kopien. Dauerhafte Übernahme nur bei fsync/sync. */
public final class Dateibeständigkeit {
    static int aktuellBewahrtKopieren = -1, erzeugungsstufeNummer = 0;
    static int[] dateiTabelle = new int[1024];
    static int prüfsummeBytes(int Wert, int Daten) { return (Wert ^ Daten) * 16777619; }
    static void datenLöschenInhalt() {
        for (int Nummer = 0; Nummer < 512; Nummer++) Speichergeräteanschluss.abschnittDaten[Nummer] = 0;
    }
    static int tabelleGanzzahl(int position) {
        return dateiTabelle[position] | dateiTabelle[position + 1] << 8 | dateiTabelle[position + 2] << 16 | dateiTabelle[position + 3] << 24;
    }
    static void tabelleGanzzahlSchreiben(int position, int Wert) {
        for (int Nummer = 0; Nummer < 4; Nummer++) dateiTabelle[position + Nummer] = (Wert >>> (Nummer * 8)) & 255;
    }
    static boolean tabellePrüfen() {
        for (int Datei = 0; Datei < 8; Datei++) {
            int Länge = 0;
            for (int platzEintrag = 0; platzEintrag < 64; platzEintrag++) ArbeitsspeicherDateisystem.Name[platzEintrag] = dateiTabelle[Datei * 72 + platzEintrag];
            while (Länge < 64 && ArbeitsspeicherDateisystem.Name[Länge] != 0) Länge++;
            if (Länge == 0) continue;
            if (!ArbeitsspeicherDateisystem.namePrüfen(ArbeitsspeicherDateisystem.Name, Länge)
                || tabelleGanzzahl(Datei * 72 + 64) < 0 || tabelleGanzzahl(Datei * 72 + 64) > 16384) return false;
            for (int vorderseiteWert = 0; vorderseiteWert < Datei; vorderseiteWert++) {
                boolean gleichText = dateiTabelle[vorderseiteWert * 72 + Länge] == 0;
                for (int platzEintrag = 0; platzEintrag < Länge; platzEintrag++) if (dateiTabelle[vorderseiteWert * 72 + platzEintrag] != ArbeitsspeicherDateisystem.Name[platzEintrag]) gleichText = false;
                if (gleichText) return false;
            }
        }
        return true;
    }
    static int bewahrtKopierenPrüfen(int bewahrtKopieren) {
        int abschnittStarten = 1 + bewahrtKopieren * 259;
        if (Speichergeräteanschluss.lesen(abschnittStarten) < 0 || Speichergeräteanschluss.ganzzahlAnalysieren(0) != 0x4a4b534e) return -1;
        int erzeugungsstufeWert = Speichergeräteanschluss.ganzzahlAnalysieren(4), kontrollsumme = Speichergeräteanschluss.ganzzahlAnalysieren(8);
        if (erzeugungsstufeWert < 1 || Speichergeräteanschluss.ganzzahlAnalysieren(12) != (erzeugungsstufeWert ^ kontrollsumme ^ 0x4a4b534e)) return -1;
        int prüfsummeDatei = 0x811c9dc5;
        for (int abschnittWert = 0; abschnittWert < 258; abschnittWert++) {
            if (Speichergeräteanschluss.lesen(abschnittStarten + 1 + abschnittWert) < 0) return -1;
            for (int platzEintrag = 0; platzEintrag < 512; platzEintrag++) {
                int Wert = Speichergeräteanschluss.abschnittDaten[platzEintrag];
                prüfsummeDatei = prüfsummeBytes(prüfsummeDatei, Wert);
                if (abschnittWert < 2) dateiTabelle[abschnittWert * 512 + platzEintrag] = Wert;
            }
        }
        return prüfsummeDatei == kontrollsumme && tabellePrüfen() ? erzeugungsstufeWert : -1;
    }
    static int laden(int bewahrtKopieren) {
        int abschnittStarten = 1 + bewahrtKopieren * 259;
        for (int abschnittWert = 0; abschnittWert < 2; abschnittWert++) {
            if (Speichergeräteanschluss.lesen(abschnittStarten + 1 + abschnittWert) < 0) return -5;
            for (int platzEintrag = 0; platzEintrag < 512; platzEintrag++) dateiTabelle[abschnittWert * 512 + platzEintrag] = Speichergeräteanschluss.abschnittDaten[platzEintrag];
        }
        for (int Datei = 0; Datei < 8; Datei++) {
            for (int platzEintrag = 0; platzEintrag < 64; platzEintrag++) ArbeitsspeicherDateisystem.namenListe[Datei * 64 + platzEintrag] = dateiTabelle[Datei * 72 + platzEintrag];
            ArbeitsspeicherDateisystem.größeListe[Datei] = dateiTabelle[Datei * 72] == 0 ? 0 : tabelleGanzzahl(Datei * 72 + 64);
            ArbeitsspeicherDateisystem.erlaubnisBerechtigungen[Datei] = tabelleGanzzahl(Datei * 72 + 68) & 511;
            for (int abschnittWert = 0; abschnittWert < 32; abschnittWert++) {
                if (Speichergeräteanschluss.lesen(abschnittStarten + 3 + Datei * 32 + abschnittWert) < 0) return -5;
                int adresse = Gerät.dateiSpeicher() + Datei * 16384 + abschnittWert * 512;
                for (int platzEintrag = 0; platzEintrag < 512; platzEintrag++) Gerät.speicherSchreiben(adresse + platzEintrag, Speichergeräteanschluss.abschnittDaten[platzEintrag]);
            }
        }
        return 0;
    }
    static void vorbereiten() {
        if (Speichergeräteanschluss.lesen(0) < 0 || Speichergeräteanschluss.ganzzahlAnalysieren(0) != 0x54534b4a
            || Speichergeräteanschluss.ganzzahlAnalysieren(4) != 0x3145524f || Speichergeräteanschluss.ganzzahlAnalysieren(8) != 2048
            || Speichergeräteanschluss.ganzzahlAnalysieren(12) != 0x3153464a) {
            Zeichenterminal.schreiben("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        Speichergeräteanschluss.istVerfügbar = true;
        int ersterOrdnungszahl = bewahrtKopierenPrüfen(0), zweiterOrdnungszahl = bewahrtKopierenPrüfen(1);
        if (ersterOrdnungszahl < 0 && zweiterOrdnungszahl < 0) { Zeichenterminal.schreiben("STORE ready; no valid snapshot\n"); return; }
        aktuellBewahrtKopieren = ersterOrdnungszahl >= zweiterOrdnungszahl ? 0 : 1; erzeugungsstufeNummer = ersterOrdnungszahl >= zweiterOrdnungszahl ? ersterOrdnungszahl : zweiterOrdnungszahl;
        if (laden(aktuellBewahrtKopieren) < 0) {
            Zeichenterminal.schreiben("STORE read failed; halted to preserve files\n"); Gerät.anhaltenAusführung();
        }
        Zeichenterminal.schreiben("STORE restored generation "); Zeichenterminal.nummerSchreiben(erzeugungsstufeNummer); Zeichenterminal.Zeichen(10);
    }
    static int synchronisieren() {
        if (!Speichergeräteanschluss.istVerfügbar) return -19;
        if (erzeugungsstufeNummer == 2147483647) return -75;
        int nächsterElementeintrag = aktuellBewahrtKopieren == 0 ? 1 : 0, abschnittStarten = 1 + nächsterElementeintrag * 259;
        // Vor dem neuen Inhalt den alten commit ungültig machen und den Gerätezwischenspeicher leeren.
        datenLöschenInhalt();
        if (Speichergeräteanschluss.schreiben(abschnittStarten) < 0 || Speichergeräteanschluss.leerenAusgabe() < 0) return -5;
        for (int platzEintrag = 0; platzEintrag < 1024; platzEintrag++) dateiTabelle[platzEintrag] = 0;
        for (int Datei = 0; Datei < 8; Datei++) if (ArbeitsspeicherDateisystem.namenListe[Datei * 64] != 0) {
            for (int platzEintrag = 0; platzEintrag < 64; platzEintrag++) dateiTabelle[Datei * 72 + platzEintrag] = ArbeitsspeicherDateisystem.namenListe[Datei * 64 + platzEintrag];
            tabelleGanzzahlSchreiben(Datei * 72 + 64, ArbeitsspeicherDateisystem.größeListe[Datei]);
            tabelleGanzzahlSchreiben(Datei * 72 + 68, ArbeitsspeicherDateisystem.erlaubnisBerechtigungen[Datei]);
        }
        int prüfsummeDatei = 0x811c9dc5;
        for (int abschnittWert = 0; abschnittWert < 258; abschnittWert++) {
            for (int platzEintrag = 0; platzEintrag < 512; platzEintrag++) {
                int Wert = 0;
                if (abschnittWert < 2) Wert = dateiTabelle[abschnittWert * 512 + platzEintrag];
                else {
                    int Datei = (abschnittWert - 2) / 32, position = (abschnittWert - 2) % 32 * 512 + platzEintrag;
                    if (dateiTabelle[Datei * 72] != 0 && position < ArbeitsspeicherDateisystem.größeListe[Datei])
                        Wert = Gerät.speicherLesen(Gerät.dateiSpeicher() + Datei * 16384 + position);
                }
                Speichergeräteanschluss.abschnittDaten[platzEintrag] = Wert; prüfsummeDatei = prüfsummeBytes(prüfsummeDatei, Wert);
            }
            if (Speichergeräteanschluss.schreiben(abschnittStarten + 1 + abschnittWert) < 0) return -5;
        }
        if (Speichergeräteanschluss.leerenAusgabe() < 0) return -5;
        datenLöschenInhalt(); Speichergeräteanschluss.ganzzahlWertSchreiben(0, 0x4a4b534e);
        Speichergeräteanschluss.ganzzahlWertSchreiben(4, erzeugungsstufeNummer + 1); Speichergeräteanschluss.ganzzahlWertSchreiben(8, prüfsummeDatei);
        Speichergeräteanschluss.ganzzahlWertSchreiben(12, (erzeugungsstufeNummer + 1) ^ prüfsummeDatei ^ 0x4a4b534e);
        if (Speichergeräteanschluss.schreiben(abschnittStarten) < 0 || Speichergeräteanschluss.leerenAusgabe() < 0) return -5;
        aktuellBewahrtKopieren = nächsterElementeintrag; erzeugungsstufeNummer++;
        return 0;
    }
}
