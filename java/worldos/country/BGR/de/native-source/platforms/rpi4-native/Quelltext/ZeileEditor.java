// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Einfügen, Löschen, Pfeiltasten, Befehlsverlauf und Tab-Vervollständigung erhalten UTF-8-Bytegrenzen. */
public final class ZeileEditor {
    static boolean befehlZeile;
    static int[] protokolldateiAufzeichnung = new int[16 * 1024], protokolldateiLänge = new int[16], ablegenDatenWert = new int[4096], kandidat = new int[64];
    static int protokolldateiAnzahl, protokolldateiAufzeichnungEnde, wertSuchen, abgelegtLänge, größe, mauszeigerWert, kandidatAnzahl, kandidatLänge, fensterStarten;
    static boolean waagerechtPositionAnzeigen;
    static String befehleListe = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd absichernBefehlshülle EntferntDarstellen run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] befehlKandidat = new int[128];
    static void befehlKandidatHinzufügen(String eintragListe, int positionStarten, int endePosition, int eingabeLänge) {
        int byteAnzahl=0;
        for(int positionIndex=positionStarten;positionIndex<endePosition;positionIndex++) {
            int zeichenKode=eintragListe.charAt(positionIndex);
            if(zeichenKode>=0xd800 && zeichenKode<=0xdbff && positionIndex+1<endePosition)zeichenKode=0x10000+((zeichenKode-0xd800)<<10)+eintragListe.charAt(++positionIndex)-0xdc00;
            int Zahl=zeichenKode<128?1:zeichenKode<2048?2:zeichenKode<65536?3:4;
            if(byteAnzahl+Zahl>62)return;
            for(int folgeWert=Zahl-1;folgeWert>=0;folgeWert--)befehlKandidat[byteAnzahl++]=Zahl==1?zeichenKode:folgeWert==Zahl-1?(Zahl==2?0xc0:Zahl==3?0xe0:0xf0)|(zeichenKode>>(6*folgeWert)):0x80|((zeichenKode>>(6*folgeWert))&63);
        }
        if(byteAnzahl<eingabeLänge)return;
        for(int positionIndex=0;positionIndex<eingabeLänge;positionIndex++)if(befehlKandidat[positionIndex]!=Befehlsinterpreter.zeile[positionIndex])return;
        kandidatAnzahl++;kandidatLänge=byteAnzahl+1;
        for(int positionIndex=0;positionIndex<byteAnzahl;positionIndex++)kandidat[positionIndex]=befehlKandidat[positionIndex];kandidat[byteAnzahl]=' ';
    }
    static int vorderseiteWert(int mauszeigerLesen) { if (mauszeigerLesen > 0) { mauszeigerLesen--; while (mauszeigerLesen > 0 && (Befehlsinterpreter.zeile[mauszeigerLesen] & 192) == 128) mauszeigerLesen--; } return mauszeigerLesen; }
    static int rückseiteWert(int mauszeigerLesen) { if (mauszeigerLesen < größe) { mauszeigerLesen++; while (mauszeigerLesen < größe && (Befehlsinterpreter.zeile[mauszeigerLesen] & 192) == 128) mauszeigerLesen++; } return mauszeigerLesen; }
    static int breiteSpannweite(int positionStarten, int zielWertIndex) {
        int zeichenzellen = 0;
        for (int schleifeIndex = positionStarten; schleifeIndex < zielWertIndex; schleifeIndex++) { int byteDaten = Befehlsinterpreter.zeile[schleifeIndex]; if ((byteDaten & 192) == 128) continue; zeichenzellen += byteDaten >= 196 ? 2 : 1; }
        return zeichenzellen;
    }
    static void erneutVersuchenWert() {
        TerminalEinAusgabe.schreiben("\r\u001b[2K");
        TerminalEinAusgabe.schreiben(befehlZeile ? "jkoros-native> " : "edit> ");
        sichtbarZeilen();
    }
    // Innerhalb einer physischen Zeile nach links und rechts gehen. Eine lange Befehlszeile darf beim Neuzeichnen keine Ausgabe darüber löschen.
    static int sichtbarBreite() { int spaltenliste = Platine.terminal(13) & 65535; return spaltenliste - (befehlZeile ? 18 : 9); }
    static void sichtbarZeilen() {
        if (mauszeigerWert < fensterStarten) fensterStarten = mauszeigerWert;
        while (breiteSpannweite(fensterStarten, mauszeigerWert) > sichtbarBreite()) fensterStarten = rückseiteWert(fensterStarten);
        int endePosition = fensterStarten;
        while (endePosition < größe && breiteSpannweite(fensterStarten, rückseiteWert(endePosition)) <= sichtbarBreite()) endePosition = rückseiteWert(endePosition);
        TerminalEinAusgabe.schreiben("\r\u001b["); TerminalEinAusgabe.Zahl(befehlZeile ? 16 : 7); TerminalEinAusgabe.schreiben("G\u001b[K");
        if (fensterStarten > 0) TerminalEinAusgabe.Zeichen('<');
        for (int schleifeIndex = fensterStarten; schleifeIndex < endePosition; schleifeIndex++) Platine.seriellSchreiben(Befehlsinterpreter.zeile[schleifeIndex]);
        TerminalEinAusgabe.Zeichen(endePosition < größe ? '>' : ' ');
        TerminalEinAusgabe.schreiben("\u001b["); TerminalEinAusgabe.Zahl(breiteSpannweite(mauszeigerWert, endePosition) + 1); TerminalEinAusgabe.Zeichen('D');
        waagerechtPositionAnzeigen = fensterStarten > 0 || endePosition < größe || breiteSpannweite(0, größe) > sichtbarBreite();
    }
    static void protokolldateiAnhängen() {
        if (!befehlZeile || größe == 0 || größe > 1024) return;
        if (protokolldateiAnzahl > 0) {
            int letzterPosition = (protokolldateiAufzeichnungEnde + 15) % 16; boolean istDerselbe = protokolldateiLänge[letzterPosition] == größe;
            for (int schleifeIndex = 0; istDerselbe && schleifeIndex < größe; schleifeIndex++) if (protokolldateiAufzeichnung[letzterPosition * 1024 + schleifeIndex] != Befehlsinterpreter.zeile[schleifeIndex]) istDerselbe = false;
            if (istDerselbe) return;
        }
        protokolldateiLänge[protokolldateiAufzeichnungEnde] = größe; for (int schleifeIndex = 0; schleifeIndex < größe; schleifeIndex++) protokolldateiAufzeichnung[protokolldateiAufzeichnungEnde * 1024 + schleifeIndex] = Befehlsinterpreter.zeile[schleifeIndex];
        protokolldateiAufzeichnungEnde = (protokolldateiAufzeichnungEnde + 1) % 16; if (protokolldateiAnzahl < 16) protokolldateiAnzahl++;
    }
    static void protokolldateiBewegung(int änderungsbetragWert) {
        if (!befehlZeile) return;
        if (wertSuchen == 0 && änderungsbetragWert > 0) { abgelegtLänge = größe; for (int schleifeIndex = 0; schleifeIndex < größe; schleifeIndex++) ablegenDatenWert[schleifeIndex] = Befehlsinterpreter.zeile[schleifeIndex]; }
        int nächsterPosition = wertSuchen + änderungsbetragWert; if (nächsterPosition < 0 || nächsterPosition > protokolldateiAnzahl) return; wertSuchen = nächsterPosition;
        if (wertSuchen == 0) { größe = abgelegtLänge; for (int schleifeIndex = 0; schleifeIndex < größe; schleifeIndex++) Befehlsinterpreter.zeile[schleifeIndex] = ablegenDatenWert[schleifeIndex]; }
        else { int bewahrtPlatz = (protokolldateiAufzeichnungEnde + 16 - wertSuchen) % 16; größe = protokolldateiLänge[bewahrtPlatz]; for (int schleifeIndex = 0; schleifeIndex < größe; schleifeIndex++) Befehlsinterpreter.zeile[schleifeIndex] = protokolldateiAufzeichnung[bewahrtPlatz * 1024 + schleifeIndex]; }
        mauszeigerWert = größe; erneutVersuchenWert();
    }
    static void protokolldateiAnzeigen() {
        for (int eintragAnzahl = 0; eintragAnzahl < protokolldateiAnzahl; eintragAnzahl++) {
            int bewahrtPlatz = (protokolldateiAufzeichnungEnde + 16 - protokolldateiAnzahl + eintragAnzahl) % 16; TerminalEinAusgabe.Zahl(eintragAnzahl + 1); TerminalEinAusgabe.schreiben("  ");
            for (int schleifeIndex = 0; schleifeIndex < protokolldateiLänge[bewahrtPlatz]; schleifeIndex++) Platine.seriellSchreiben(protokolldateiAufzeichnung[bewahrtPlatz * 1024 + schleifeIndex]); TerminalEinAusgabe.Zeichen(10);
        }
    }
    static void kandidatHinzufügen(int[] datenDatenfeld, int positionStarten, int eintragAnzahl, int vorsilbe, int gesamtwertAnzahl, boolean verzeichnisNummer) {
        if (eintragAnzahl < gesamtwertAnzahl || eintragAnzahl > 62) return;
        for (int schleifeIndex = 0; schleifeIndex < gesamtwertAnzahl; schleifeIndex++) if (datenDatenfeld[positionStarten + schleifeIndex] != Befehlsinterpreter.zeile[vorsilbe + schleifeIndex]) return;
        kandidatAnzahl++; kandidatLänge = eintragAnzahl + 1;
        for (int schleifeIndex = 0; schleifeIndex < eintragAnzahl; schleifeIndex++) kandidat[schleifeIndex] = datenDatenfeld[positionStarten + schleifeIndex]; kandidat[eintragAnzahl] = verzeichnisNummer ? '/' : ' ';
    }
    static void abgeschlossenWert() {
        if (!befehlZeile || mauszeigerWert != größe) return;
        int beginnendPunkt = größe; while (beginnendPunkt > 0 && Befehlsinterpreter.zeile[beginnendPunkt - 1] != ' ') beginnendPunkt--;
        for (int schleifeIndex = beginnendPunkt; schleifeIndex < größe; schleifeIndex++) if (Befehlsinterpreter.zeile[schleifeIndex] == '/' || Befehlsinterpreter.zeile[schleifeIndex] == '"' || Befehlsinterpreter.zeile[schleifeIndex] == 39 || Befehlsinterpreter.zeile[schleifeIndex] == '\\') return;
        kandidatAnzahl = 0; int eintragAnzahl = größe - beginnendPunkt;
        if (beginnendPunkt == 0) {
            for(int listeIndex=0;listeIndex<2;listeIndex++) {
                String eintragListe=listeIndex==0?befehleListe:Verwaltungsbefehle.abgeschlossenMaschinenwort();
                int mauszeigerLesen=0;
                while(mauszeigerLesen<eintragListe.length()) {
                    int endePosition=mauszeigerLesen;while(endePosition<eintragListe.length() && eintragListe.charAt(endePosition)!=' ')endePosition++;
                    befehlKandidatHinzufügen(eintragListe,mauszeigerLesen,endePosition,eintragAnzahl);mauszeigerLesen=endePosition+1;
                }
            }
        } else {
            SpeicherDateien.pfadStarten(1); SpeicherDateien.pfadByte(0, '.'); SpeicherDateien.wertNormalisieren();
            for (int schleifeIndex = 0; schleifeIndex < SpeicherDateien.dateiAnzahl; schleifeIndex++) {
                int positionStarten = SpeicherDateien.eintragStarten(SpeicherDateien.Name, schleifeIndex * 64, SpeicherDateien.namenlänge[schleifeIndex]);
                if (positionStarten >= 0) kandidatHinzufügen(SpeicherDateien.Name, schleifeIndex * 64 + positionStarten, SpeicherDateien.namenlänge[schleifeIndex] - positionStarten, beginnendPunkt, eintragAnzahl, false);
            }
            for (int schleifeIndex = 0; schleifeIndex < 16; schleifeIndex++) {
                int positionStarten = SpeicherDateien.eintragStarten(SpeicherDateien.verzeichnisName, schleifeIndex * 64, SpeicherDateien.verzeichnisLänge[schleifeIndex]);
                if (positionStarten >= 0) kandidatHinzufügen(SpeicherDateien.verzeichnisName, schleifeIndex * 64 + positionStarten, SpeicherDateien.verzeichnisLänge[schleifeIndex] - positionStarten, beginnendPunkt, eintragAnzahl, true);
            }
        }
        if (kandidatAnzahl != 1) { Platine.seriellSchreiben(7); return; }
        for (int schleifeIndex = eintragAnzahl; schleifeIndex < kandidatLänge && größe < Befehlsinterpreter.zeile.length - 1; schleifeIndex++) {
            if (kandidat[schleifeIndex] == ' ' && schleifeIndex != kandidatLänge - 1) Befehlsinterpreter.zeile[größe++] = '\\';
            Befehlsinterpreter.zeile[größe++] = kandidat[schleifeIndex];
        }
        mauszeigerWert = größe; erneutVersuchenWert();
    }
    static int maskierenLesen() {
        int beginnendPunkt = Platine.millisekunden();
        while (Platine.millisekunden() - beginnendPunkt < 80) { int byteDaten = Platine.seriellLesen(); if (byteDaten >= 0) return byteDaten; Platine.prozessorAbgeben(); }
        return -1;
    }
    static void maskierenWert() {
        int erster = maskierenLesen(); if (erster != '[' && erster != 'O') return;
        int eintragAnzahl = 0, endePosition = -1;
        for (int schleifeIndex = 0; schleifeIndex < 12; schleifeIndex++) { int byteDaten = maskierenLesen(); if (byteDaten < 0) return; if (byteDaten >= '0' && byteDaten <= '9') eintragAnzahl = eintragAnzahl * 10 + byteDaten - '0'; else { endePosition = byteDaten; break; } }
        if (endePosition == 'A') protokolldateiBewegung(1);
        else if (endePosition == 'B') protokolldateiBewegung(-1);
        else if (endePosition == 'C') { mauszeigerWert = rückseiteWert(mauszeigerWert); erneutVersuchenWert(); }
        else if (endePosition == 'D') { mauszeigerWert = vorderseiteWert(mauszeigerWert); erneutVersuchenWert(); }
        else if (endePosition == 'H' || endePosition == '~' && (eintragAnzahl == 1 || eintragAnzahl == 7)) { mauszeigerWert = 0; erneutVersuchenWert(); }
        else if (endePosition == 'F' || endePosition == '~' && (eintragAnzahl == 4 || eintragAnzahl == 8)) { mauszeigerWert = größe; erneutVersuchenWert(); }
        else if (endePosition == '~' && eintragAnzahl == 3 && mauszeigerWert < größe) {
            int nächsterPosition = rückseiteWert(mauszeigerWert); for (int schleifeIndex = nächsterPosition; schleifeIndex < größe; schleifeIndex++) Befehlsinterpreter.zeile[schleifeIndex - nächsterPosition + mauszeigerWert] = Befehlsinterpreter.zeile[schleifeIndex]; größe -= nächsterPosition - mauszeigerWert; erneutVersuchenWert();
        }
        else if (endePosition == '~' && (eintragAnzahl == 5 || eintragAnzahl == 6)) Platine.terminal(eintragAnzahl == 5 ? 5 : 6);
        else if (endePosition == '~' && eintragAnzahl == 24 && befehlZeile) { Befehlsinterpreter.terminal(true); }
    }
    static int lesen() {
        if (!fensterSitzung.fortsetzungLesen) { größe = mauszeigerWert = wertSuchen = fensterStarten = 0; waagerechtPositionAnzeigen = false; }
        else { fensterSitzung.fortsetzungLesen = false; erneutVersuchenWert(); } boolean überlauf = false;
        while (true) {
            int byteDaten = Platine.seriellLesen(); if (byteDaten == -4096) return -3;
            if (Platine.terminal(14) != 0) erneutVersuchenWert(); if (byteDaten < 0) { Platine.prozessorAbgeben(); continue; }
            if (byteDaten == 10 && Befehlsinterpreter.vorherigZeile) { Befehlsinterpreter.vorherigZeile = false; continue; } Befehlsinterpreter.vorherigZeile = byteDaten == 13;
            if (byteDaten == 27) { maskierenWert(); continue; }
            if (byteDaten == 3) { TerminalEinAusgabe.schreiben("^C\n"); return -1; }
            if (byteDaten == 4 && größe == 0 && befehlZeile) { if (Platine.terminal(2) != 0) Befehlsinterpreter.terminal(true); return -1; }
            if (byteDaten == 13 || byteDaten == 10) { TerminalEinAusgabe.Zeichen(10); if (!überlauf) protokolldateiAnhängen(); return überlauf ? -2 : größe; }
            if (byteDaten == 9 && befehlZeile) { abgeschlossenWert(); continue; }
            if (byteDaten == 1 || byteDaten == 5) { mauszeigerWert = byteDaten == 1 ? 0 : größe; erneutVersuchenWert(); continue; }
            if (byteDaten == 8 || byteDaten == 127 || byteDaten == 21) {
                if (byteDaten == 21) { for (int schleifeIndex = mauszeigerWert; schleifeIndex < größe; schleifeIndex++) Befehlsinterpreter.zeile[schleifeIndex - mauszeigerWert] = Befehlsinterpreter.zeile[schleifeIndex]; größe -= mauszeigerWert; mauszeigerWert = 0; }
                else if (mauszeigerWert > 0) { int davorÄndern = vorderseiteWert(mauszeigerWert); for (int schleifeIndex = mauszeigerWert; schleifeIndex < größe; schleifeIndex++) Befehlsinterpreter.zeile[schleifeIndex - mauszeigerWert + davorÄndern] = Befehlsinterpreter.zeile[schleifeIndex]; größe -= mauszeigerWert - davorÄndern; mauszeigerWert = davorÄndern; }
                erneutVersuchenWert(); continue;
            }
            if (byteDaten == 11) { größe = mauszeigerWert; erneutVersuchenWert(); continue; }
            if (byteDaten < 32 && byteDaten != 9) continue;
            if (größe == Befehlsinterpreter.zeile.length) { überlauf = true; continue; }
            for (int schleifeIndex = größe; schleifeIndex > mauszeigerWert; schleifeIndex--) Befehlsinterpreter.zeile[schleifeIndex] = Befehlsinterpreter.zeile[schleifeIndex - 1];
            Befehlsinterpreter.zeile[mauszeigerWert++] = byteDaten; größe++;
            if (mauszeigerWert == größe && !waagerechtPositionAnzeigen && breiteSpannweite(0, größe) <= sichtbarBreite()) Platine.seriellSchreiben(byteDaten);
            else if (mauszeigerWert == größe) sichtbarZeilen(); else erneutVersuchenWert();
        }
    }
}
