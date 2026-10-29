// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Eingeschränkte interaktive Shell-Grammatik. Pipes laufen nacheinander; die Umgebung wird innerhalb derselben Shell geteilt. */
public final class BefehlshülleSatzbau {
    static int[] Quelltext = new int[4 * 4096], artWert = new int[4 * 128], ausführenVorgang = new int[4 * 128], endung = new int[4 * 128];
    static int[] variableName = new int[16 * 32], variableDaten = new int[16 * 256], namenlänge = new int[16], wertLänge = new int[16];
    static int[] skriptWert = new int[4 * 16384];
    static int statuswertWert, tiefeWert, geschrieben;
    static boolean istVerbindend, skriptEnde, erweiterungFehler;
    static boolean nameZeichen(int zeichenKode) { return zeichenKode >= 'a' && zeichenKode <= 'z' || zeichenKode >= 'A' && zeichenKode <= 'Z' || zeichenKode == '_' || zeichenKode >= 128; }
    static boolean nameNachsilbe(int zeichenKode) { return nameZeichen(zeichenKode) || zeichenKode >= '0' && zeichenKode <= '9'; }
    static void fehler(String Text) { Platine.umschaltenEinAusgabe(0); TerminalEinAusgabe.schreiben("befehl wertAnalysieren: "); TerminalEinAusgabe.schreiben(Text); TerminalEinAusgabe.Zeichen(10); statuswertWert = 2; }
    static int lesen(int eintragAnzahl, int tiefe) {
        int aktuellIndex = 0, gesamtwertAnzahl = 0, basisPosition = tiefe * 4096, besondersZeichen = tiefe * 128;
        while (aktuellIndex < eintragAnzahl) {
            while (aktuellIndex < eintragAnzahl && (Quelltext[basisPosition + aktuellIndex] == 32 || Quelltext[basisPosition + aktuellIndex] == 9)) aktuellIndex++;
            if (aktuellIndex == eintragAnzahl || Quelltext[basisPosition + aktuellIndex] == '#') break;
            if (gesamtwertAnzahl == 128) { fehler("낱말이 너무 많습니다"); return -1; }
            int positionStarten = aktuellIndex, zeichenKode = Quelltext[basisPosition + aktuellIndex], datenArt = 0;
            if (zeichenKode == ';') { datenArt = 1; aktuellIndex++; }
            else if (zeichenKode == '&') { if (aktuellIndex + 1 >= eintragAnzahl || Quelltext[basisPosition + aktuellIndex + 1] != '&') { fehler("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } datenArt = 2; aktuellIndex += 2; }
            else if (zeichenKode == '|') { aktuellIndex++; datenArt = aktuellIndex < eintragAnzahl && Quelltext[basisPosition + aktuellIndex] == '|' ? 3 : 4; if (datenArt == 3) aktuellIndex++; }
            else if (zeichenKode == '>') { aktuellIndex++; datenArt = aktuellIndex < eintragAnzahl && Quelltext[basisPosition + aktuellIndex] == '>' ? 6 : 5; if (datenArt == 6) aktuellIndex++; }
            else if (zeichenKode == '<') { datenArt = 7; aktuellIndex++; }
            else {
                int anführungszeichen = 0;
                while (aktuellIndex < eintragAnzahl) {
                    zeichenKode = Quelltext[basisPosition + aktuellIndex];
                    if (zeichenKode == '`' && anführungszeichen != 39 || zeichenKode == '$' && anführungszeichen != 39 && aktuellIndex + 1 < eintragAnzahl && Quelltext[basisPosition + aktuellIndex + 1] == '(') { fehler("befehl ergebnis 치환은 지원하지 않습니다"); return -1; }
                    if (zeichenKode == '\\' && anführungszeichen != 39) { if (++aktuellIndex == eintragAnzahl) { fehler("zeile 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } aktuellIndex++; continue; }
                    if (zeichenKode == anführungszeichen) { anführungszeichen = 0; aktuellIndex++; continue; }
                    if (anführungszeichen == 0 && (zeichenKode == 39 || zeichenKode == 34)) { anführungszeichen = zeichenKode; aktuellIndex++; continue; }
                    if (anführungszeichen == 0 && (zeichenKode == 32 || zeichenKode == 9 || zeichenKode == ';' || zeichenKode == '&' || zeichenKode == '|' || zeichenKode == '<' || zeichenKode == '>')) break;
                    aktuellIndex++;
                }
                if (anführungszeichen != 0) { fehler("따옴표가 닫히지 않았습니다"); return -1; }
                if (aktuellIndex < eintragAnzahl && (Quelltext[basisPosition + aktuellIndex] == '>' || Quelltext[basisPosition + aktuellIndex] == '<')) {
                    boolean numerischWert = aktuellIndex > positionStarten;
                    for (int schleifeIndex = positionStarten; schleifeIndex < aktuellIndex; schleifeIndex++) if (Quelltext[basisPosition + schleifeIndex] < '0' || Quelltext[basisPosition + schleifeIndex] > '9') numerischWert = false;
                    if (numerischWert) { fehler("번호를 지정한 Datei deskriptorEintrag eingabeAusgabe 전환은 지원하지 않습니다"); return -1; }
                }
            }
            artWert[besondersZeichen + gesamtwertAnzahl] = datenArt; ausführenVorgang[besondersZeichen + gesamtwertAnzahl] = positionStarten; endung[besondersZeichen + gesamtwertAnzahl] = aktuellIndex; gesamtwertAnzahl++;
        }
        boolean lexikalischMaschinenwort = false;
        for (int schleifeIndex = 0; schleifeIndex < gesamtwertAnzahl; schleifeIndex++) {
            int vorläufigDaten = artWert[besondersZeichen + schleifeIndex];
            if (vorläufigDaten == 0) lexikalischMaschinenwort = true;
            else if (vorläufigDaten >= 5) { if (++schleifeIndex == gesamtwertAnzahl || artWert[besondersZeichen + schleifeIndex] != 0) { fehler("eingabeAusgabe 전환에 Datei 이름이 필요합니다"); return -1; } }
            else { if (!lexikalischMaschinenwort || schleifeIndex == gesamtwertAnzahl - 1 && vorläufigDaten != 1) { fehler("명령이 빠졌습니다"); return -1; } lexikalischMaschinenwort = false; }
        }
        if (gesamtwertAnzahl > 0 && !lexikalischMaschinenwort && artWert[besondersZeichen + gesamtwertAnzahl - 1] != 1) { fehler("명령이 빠졌습니다"); return -1; }
        return gesamtwertAnzahl;
    }
    static boolean bereichText(int[] datenDatenfeld, int lokalStarten, int eintragAnzahl, String zeichenPosition) {
        if (eintragAnzahl != zeichenPosition.length()) return false; for (int schleifeIndex = 0; schleifeIndex < eintragAnzahl; schleifeIndex++) if (datenDatenfeld[lokalStarten + schleifeIndex] != zeichenPosition.charAt(schleifeIndex)) return false; return true;
    }
    static void wertAblegen(int byteDaten) {
        if (geschrieben >= Befehlsinterpreter.wortzeichenWert.length) { if (!erweiterungFehler) fehler("변수를 펼친 명령이 너무 깁니다"); erweiterungFehler = true; return; }
        Befehlsinterpreter.wortzeichenWert[geschrieben++] = byteDaten;
    }
    static void variableWert(int[] datenDatenfeld, int positionStarten, int eintragAnzahl) {
        if (bereichText(datenDatenfeld, positionStarten, eintragAnzahl, "PWD")) { wertAblegen('/'); for (int schleifeIndex = 0; schleifeIndex < SpeicherDateien.aktuellLänge; schleifeIndex++) wertAblegen(SpeicherDateien.aktuellElementeintrag[schleifeIndex]); return; }
        if (bereichText(datenDatenfeld, positionStarten, eintragAnzahl, "HOME")) { wertAblegen('/'); return; }
        if (bereichText(datenDatenfeld, positionStarten, eintragAnzahl, "?")) {
            int datenWert = statuswertWert, ziffer = 100; boolean hatGestartet = false;
            while (ziffer > 0) { int nachlaufendWert = datenWert / ziffer; if (nachlaufendWert != 0 || hatGestartet || ziffer == 1) { wertAblegen('0' + nachlaufendWert); hatGestartet = true; } datenWert %= ziffer; ziffer /= 10; } return;
        }
        for (int schleifeIndex = 0; schleifeIndex < 16; schleifeIndex++) if (namenlänge[schleifeIndex] == eintragAnzahl) {
            boolean vergleichen = true; for (int innerlichPosition = 0; innerlichPosition < eintragAnzahl; innerlichPosition++) if (variableName[schleifeIndex * 32 + innerlichPosition] != datenDatenfeld[positionStarten + innerlichPosition]) vergleichen = false;
            if (vergleichen) { for (int innerlichPosition = 0; innerlichPosition < wertLänge[schleifeIndex]; innerlichPosition++) wertAblegen(variableDaten[schleifeIndex * 256 + innerlichPosition]); return; }
        }
    }
    static boolean maschinenwortWert(int lexikalischMaschinenwortIndex, int tiefe) {
        int mauszeigerLesen = ausführenVorgang[tiefe * 128 + lexikalischMaschinenwortIndex], endePosition = endung[tiefe * 128 + lexikalischMaschinenwortIndex], basisPosition = tiefe * 4096, anführungszeichen = 0;
        if (mauszeigerLesen < endePosition && Quelltext[basisPosition + mauszeigerLesen] == '~' && (mauszeigerLesen + 1 == endePosition || Quelltext[basisPosition + mauszeigerLesen + 1] == '/')) { wertAblegen('/'); mauszeigerLesen++; }
        while (mauszeigerLesen < endePosition) {
            int zeichenKode = Quelltext[basisPosition + mauszeigerLesen++];
            if (zeichenKode == anführungszeichen) { anführungszeichen = 0; continue; }
            if (anführungszeichen == 0 && (zeichenKode == 39 || zeichenKode == 34)) { anführungszeichen = zeichenKode; continue; }
            if (zeichenKode == '\\' && anführungszeichen != 39) { int nächsterPosition = Quelltext[basisPosition + mauszeigerLesen++]; if (anführungszeichen == 34 && nächsterPosition != '$' && nächsterPosition != '"' && nächsterPosition != '\\') wertAblegen('\\'); wertAblegen(nächsterPosition); continue; }
            if (zeichenKode == '$' && anführungszeichen != 39 && mauszeigerLesen < endePosition) {
                boolean geschweifteKlammer = Quelltext[basisPosition + mauszeigerLesen] == '{'; if (geschweifteKlammer) mauszeigerLesen++;
                int beginn = mauszeigerLesen;
                if (mauszeigerLesen < endePosition && Quelltext[basisPosition + mauszeigerLesen] == '?') mauszeigerLesen++;
                else while (mauszeigerLesen < endePosition && nameNachsilbe(Quelltext[basisPosition + mauszeigerLesen])) mauszeigerLesen++;
                if (geschweifteKlammer && (mauszeigerLesen == endePosition || Quelltext[basisPosition + mauszeigerLesen] != '}')) { fehler("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (mauszeigerLesen == beginn && !geschweifteKlammer) { wertAblegen('$'); continue; }
                variableWert(Quelltext, basisPosition + beginn, mauszeigerLesen - beginn); if (geschweifteKlammer) mauszeigerLesen++; continue;
            }
            wertAblegen(zeichenKode);
        }
        return !erweiterungFehler;
    }
    static int umgebungEinstellungen(int argumentIndex, boolean entfernen) {
        int lokalStarten = Befehlsinterpreter.beginnendPunkt[argumentIndex], endePosition = lokalStarten + Befehlsinterpreter.Länge[argumentIndex], gleichheitPosition = lokalStarten;
        while (gleichheitPosition < endePosition && Befehlsinterpreter.wortzeichenWert[gleichheitPosition] != '=') gleichheitPosition++;
        int eintragAnzahl = gleichheitPosition - lokalStarten;
        if (eintragAnzahl < 1 || eintragAnzahl > 31 || !nameZeichen(Befehlsinterpreter.wortzeichenWert[lokalStarten]) || !entfernen && gleichheitPosition == endePosition || endePosition - gleichheitPosition - 1 > 255) return 2;
        for (int schleifeIndex = lokalStarten; schleifeIndex < gleichheitPosition; schleifeIndex++) if (!nameNachsilbe(Befehlsinterpreter.wortzeichenWert[schleifeIndex])) return 2;
        if (bereichText(Befehlsinterpreter.wortzeichenWert, lokalStarten, eintragAnzahl, "PWD") || bereichText(Befehlsinterpreter.wortzeichenWert, lokalStarten, eintragAnzahl, "HOME")) return 2;
        int warGefunden = -1, istLeerwertStatuswert = -1;
        for (int schleifeIndex = 0; schleifeIndex < 16; schleifeIndex++) {
            if (namenlänge[schleifeIndex] == 0) istLeerwertStatuswert = schleifeIndex;
            if (namenlänge[schleifeIndex] != eintragAnzahl) continue;
            boolean vergleichen = true; for (int innerlichPosition = 0; innerlichPosition < eintragAnzahl; innerlichPosition++) if (variableName[schleifeIndex * 32 + innerlichPosition] != Befehlsinterpreter.wortzeichenWert[lokalStarten + innerlichPosition]) vergleichen = false;
            if (vergleichen) warGefunden = schleifeIndex;
        }
        if (entfernen) { if (warGefunden >= 0) namenlänge[warGefunden] = 0; return 0; }
        if (warGefunden < 0) warGefunden = istLeerwertStatuswert; if (warGefunden < 0) return 1;
        namenlänge[warGefunden] = eintragAnzahl; wertLänge[warGefunden] = endePosition - gleichheitPosition - 1;
        for (int schleifeIndex = 0; schleifeIndex < eintragAnzahl; schleifeIndex++) variableName[warGefunden * 32 + schleifeIndex] = Befehlsinterpreter.wortzeichenWert[lokalStarten + schleifeIndex];
        for (int schleifeIndex = gleichheitPosition + 1; schleifeIndex < endePosition; schleifeIndex++) variableDaten[warGefunden * 256 + schleifeIndex - gleichheitPosition - 1] = Befehlsinterpreter.wortzeichenWert[schleifeIndex];
        return 0;
    }
    static void umgebungAnzeigen() {
        TerminalEinAusgabe.schreiben("HOME=/\nPWD="); SpeicherDateien.aktuellSchreiben(); TerminalEinAusgabe.Zeichen(10);
        for (int schleifeIndex = 0; schleifeIndex < 16; schleifeIndex++) if (namenlänge[schleifeIndex] > 0) {
            for (int innerlichPosition = 0; innerlichPosition < namenlänge[schleifeIndex]; innerlichPosition++) Platine.seriellSchreiben(variableName[schleifeIndex * 32 + innerlichPosition]); TerminalEinAusgabe.Zeichen('=');
            for (int innerlichPosition = 0; innerlichPosition < wertLänge[schleifeIndex]; innerlichPosition++) Platine.seriellSchreiben(variableDaten[schleifeIndex * 256 + innerlichPosition]); TerminalEinAusgabe.Zeichen(10);
        }
    }
    static void befehlAusführen(int[] datenDatenfeld, int versatzStarten, int eintragAnzahl, int tiefe) {
        if (tiefe >= 4 || eintragAnzahl > 4096) { fehler("befehl 파일의 verschachtelungWert 또는 zeile Länge 제한을 넘었습니다"); return; }
        for (int schleifeIndex = 0; schleifeIndex < eintragAnzahl; schleifeIndex++) Quelltext[tiefe * 4096 + schleifeIndex] = datenDatenfeld[versatzStarten + schleifeIndex];
        int gesamtwertAnzahl = lesen(eintragAnzahl, tiefe); if (gesamtwertAnzahl < 0) return;
        int mauszeigerLesen = 0, bedingungErfüllt = 1;
        while (mauszeigerLesen < gesamtwertAnzahl) {
            int gruppeEnde = mauszeigerLesen;
            while (gruppeEnde < gesamtwertAnzahl && (artWert[tiefe * 128 + gruppeEnde] == 0 || artWert[tiefe * 128 + gruppeEnde] >= 4)) gruppeEnde++;
            boolean ausführen = bedingungErfüllt == 1 || bedingungErfüllt == 2 && statuswertWert == 0 || bedingungErfüllt == 3 && statuswertWert != 0;
            if (ausführen) {
                boolean vorherigElementeintragIndex = false;
                while (mauszeigerLesen < gruppeEnde) {
                    int nächsterPosition = mauszeigerLesen; while (nächsterPosition < gruppeEnde && artWert[tiefe * 128 + nächsterPosition] != 4) nächsterPosition++;
                    boolean datenstromVerbinden = nächsterPosition < gruppeEnde; int eingabeSeite = -1, ausgabeSeite = -1, ausgehendBetriebsart = 0;
                    Befehlsinterpreter.wortzeichenAnzahl = 0; geschrieben = 0; erweiterungFehler = false;
                    for (int schleifeIndex = mauszeigerLesen; schleifeIndex < nächsterPosition; schleifeIndex++) {
                        int datenArt = artWert[tiefe * 128 + schleifeIndex];
                        if (datenArt >= 5) { if (datenArt == 7) { if (eingabeSeite >= 0) { fehler("Eingabewert 전환이 겹쳤습니다"); return; } eingabeSeite = ++schleifeIndex; } else { if (ausgabeSeite >= 0) { fehler("Ausgabe 전환이 겹쳤습니다"); return; } ausgabeSeite = ++schleifeIndex; ausgehendBetriebsart = datenArt; } continue; }
                        if (Befehlsinterpreter.wortzeichenAnzahl == 32) { fehler("인수가 너무 많습니다"); return; }
                        int argumentIndex = Befehlsinterpreter.wortzeichenAnzahl++; Befehlsinterpreter.beginnendPunkt[argumentIndex] = geschrieben;
                        if (!maschinenwortWert(schleifeIndex, tiefe)) return;
                        Befehlsinterpreter.Länge[argumentIndex] = geschrieben - Befehlsinterpreter.beginnendPunkt[argumentIndex];
                    }
                    istVerbindend = vorherigElementeintragIndex || datenstromVerbinden || eingabeSeite >= 0 || ausgabeSeite >= 0;
                    if (istVerbindend && (Befehlsinterpreter.gleichText(0, "vi") || Befehlsinterpreter.gleichText(0, "edit") || Befehlsinterpreter.gleichText(0, "load") || Befehlsinterpreter.gleichText(0, "gui") || Befehlsinterpreter.gleichText(0, "terminal") || Befehlsinterpreter.gleichText(0, "sh") || Befehlsinterpreter.gleichText(0, "source"))) { fehler("interaktiv 명령과 befehl 파일은 eingabeAusgabe 전환이나 datenstromWert 연결에 쓸 Zahl 없습니다"); return; }
                    BefehlshülleEinAusgabe.ausführenVorgang(vorherigElementeintragIndex, datenstromVerbinden);
                    for (int umleitung = 0; umleitung < 2; umleitung++) {
                        int eintragPosition = umleitung == 0 ? eingabeSeite : ausgabeSeite; if (eintragPosition < 0) continue;
                        int positionStarten = geschrieben; if (!maschinenwortWert(eintragPosition, tiefe)) { BefehlshülleEinAusgabe.endung(); return; }
                        int verarbeitetWert = SpeicherDateien.pfadStarten(geschrieben - positionStarten);
                        for (int innerlichPosition = positionStarten; verarbeitetWert >= 0 && innerlichPosition < geschrieben; innerlichPosition++) verarbeitetWert = SpeicherDateien.pfadByte(innerlichPosition - positionStarten, Befehlsinterpreter.wortzeichenWert[innerlichPosition]);
                        if (verarbeitetWert >= 0) verarbeitetWert = SpeicherDateien.öffnen(umleitung == 0 ? 0 : ausgehendBetriebsart == 6 ? 1089 : 577);
                        if (verarbeitetWert < 0) { BefehlshülleEinAusgabe.endung(); Befehlsinterpreter.fehler(verarbeitetWert); statuswertWert = 1; return; }
                        if (umleitung == 0) BefehlshülleEinAusgabe.eingabeDatei = verarbeitetWert; else BefehlshülleEinAusgabe.ausgabeDatei = verarbeitetWert;
                    }
                    BefehlshülleEinAusgabe.interaktivErlauben = tiefe == 0 && mauszeigerLesen == 0 && nächsterPosition == gesamtwertAnzahl;
                    tiefeWert = tiefe; Befehlsinterpreter.ergebnis = 0; Platine.umschaltenEinAusgabe(1);
                    Befehlsinterpreter.befehl();
                    Platine.terminal(3);
                    int zurückgegebenWert = Befehlsinterpreter.ergebnis, datenstromFehler = BefehlshülleEinAusgabe.fehlschlagWert;
                    BefehlshülleEinAusgabe.endung(); istVerbindend = false;
                    statuswertWert = datenstromFehler < 0 ? 1 : zurückgegebenWert;
                    if (datenstromFehler < 0) { Befehlsinterpreter.fehler(datenstromFehler); return; }
                    if (skriptEnde || zurückgegebenWert == -1005) return;
                    vorherigElementeintragIndex = true; mauszeigerLesen = nächsterPosition + 1;
                }
            }
            if (gruppeEnde < gesamtwertAnzahl) bedingungErfüllt = artWert[tiefe * 128 + gruppeEnde];
            mauszeigerLesen = gruppeEnde + 1;
        }
    }
    static void dateiAusführen() {
        if (Befehlsinterpreter.wortzeichenAnzahl != 2 || tiefeWert >= 3) { Befehlsinterpreter.ergebnis = 2; TerminalEinAusgabe.schreiben("사용법: sh Datei (verschachtelungWert tiefeWert <= 3)\n"); return; }
        int tiefe = tiefeWert + 1, verarbeitetWert = Befehlsinterpreter.pfad(1); if (verarbeitetWert >= 0) verarbeitetWert = SpeicherDateien.öffnen(0);
        if (verarbeitetWert < 0) { Befehlsinterpreter.fehler(verarbeitetWert); return; }
        int eintragAnzahl = 0, byteDaten;
        while ((byteDaten = SpeicherDateien.lesen(verarbeitetWert)) != 256 && byteDaten >= 0 && eintragAnzahl < 16384) skriptWert[tiefe * 16384 + eintragAnzahl++] = byteDaten;
        SpeicherDateien.schließen(verarbeitetWert); Platine.umschaltenEinAusgabe(0);
        for (int mauszeigerLesen = 0; mauszeigerLesen < eintragAnzahl && !skriptEnde;) {
            int endePosition = mauszeigerLesen; while (endePosition < eintragAnzahl && skriptWert[tiefe * 16384 + endePosition] != 10) endePosition++;
            int gültigLänge = endePosition - mauszeigerLesen; if (gültigLänge > 0 && skriptWert[tiefe * 16384 + endePosition - 1] == 13) gültigLänge--;
            befehlAusführen(skriptWert, tiefe * 16384 + mauszeigerLesen, gültigLänge, tiefe); mauszeigerLesen = endePosition + 1;
        }
        Befehlsinterpreter.ergebnis = statuswertWert; skriptEnde = false; tiefeWert = tiefe - 1;
    }
}
