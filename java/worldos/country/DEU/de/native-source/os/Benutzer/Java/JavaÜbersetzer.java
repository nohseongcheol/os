// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Eingeschränkter Java-Quellübersetzer im Gast; erzeugt Standard-Klassendateien der Version 49. */
public final class JavaÜbersetzer {
    static int[] Quelltext = new int[16384], Ausgabe = new int[16384], kodeWert = new int[4096];
    static int[] wortzeichenArt = new int[2048], wortzeichenPosition = new int[2048], wortzeichenLänge = new int[2048];
    static int[] konstanteWert = new int[4096], konstanteVersatzwert = new int[512];
    static int[] Zeichen = new int[512], dateiNameText = new int[64];
    static int[] eingefügtKode = new int[16];
    static int quelltextGröße, wortzeichenAnzahl, position, kodeGröße, konstanteGröße, konstanteAnzahl = 1, ausgabeGröße, zeichenLänge;
    static boolean fehler;
    static int klasseWortzeichen, klasseKonstante, elternknotenKonstante, kodeKonstante;
    static int[] methodeEintragName = new int[32], methodeZurückkehren = new int[32], methodeArgumentAnzahl = new int[32];
    static int[] methodeArgumentName = new int[512], methodeArgumentTyp = new int[512];
    static int[] methodeRumpf = new int[32], methodeEnde = new int[32], methodeKode = new int[32];
    static int[] methodeLänge = new int[32], methodeLokalvariablen = new int[32], methodeNameKonstante = new int[32], methodeDeskriptorKonstante = new int[32];
    static int[] methodeZugriff = new int[32];
    static int methodeAnzahl, aktuellMethode, lokalAnzahl, tiefeWert, ausdruckTiefe;
    static int[] lokalName = new int[128], lokalTyp = new int[128], lokalTiefe = new int[128];

    static void fehlschlagWert(String grundWert) {
        if (!fehler) {
            Benutzer.schreiben("javac error: "); Benutzer.schreiben(grundWert);
            Benutzer.schreiben(" at line ");
            int zeile = 1, endung = position < wortzeichenAnzahl ? wortzeichenPosition[position] : quelltextGröße;
            for (int Zahl = 0; Zahl < endung; Zahl++) if (Quelltext[Zahl] == 10) zeile++;
            JavaWerkzeug.nummerSchreiben(zeile); Benutzer.zeichenWertSchreiben(10);
        }
        fehler = true;
    }
    static boolean zeichenWert(int Wert) { return Bezeichnerzeichenregeln.ersterZeichen(Wert); }
    static boolean zifferWert(int Wert) { return Wert >= '0' && Wert <= '9'; }
    static boolean namenGleich(int ersterOperand, int zweiterOperand) {
        if (ersterOperand < 0 || zweiterOperand < 0 || ersterOperand >= wortzeichenAnzahl || zweiterOperand >= wortzeichenAnzahl || wortzeichenLänge[ersterOperand] != wortzeichenLänge[zweiterOperand]) return false;
        for (int Zahl = 0; Zahl < wortzeichenLänge[ersterOperand]; Zahl++) if (Quelltext[wortzeichenPosition[ersterOperand] + Zahl] != Quelltext[wortzeichenPosition[zweiterOperand] + Zahl]) return false;
        return true;
    }
    static boolean maschinenwortWert(int wortzeichenWert, String maschinenwortText) {
        if (wortzeichenWert < 0 || wortzeichenWert >= wortzeichenAnzahl || wortzeichenLänge[wortzeichenWert] != maschinenwortText.length()) return false;
        for (int Zahl = 0; Zahl < maschinenwortText.length(); Zahl++) if (Quelltext[wortzeichenPosition[wortzeichenWert] + Zahl] != maschinenwortText.charAt(Zahl)) return false;
        return true;
    }
    static int artWert() { return position < wortzeichenAnzahl ? wortzeichenArt[position] : 0; }
    static boolean empfangen(int Wert) { if (artWert() != Wert) return false; position++; return true; }
    static void anforderungWert(int Wert) { if (!empfangen(Wert)) fehlschlagWert("unexpected token"); }
    static boolean entnehmenMaschinenwort(String maschinenwortText) { if (!maschinenwortWert(position, maschinenwortText)) return false; position++; return true; }
    static void erfordernMaschinenwort(String maschinenwortText) { if (!entnehmenMaschinenwort(maschinenwortText)) fehlschlagWert(maschinenwortText); }
    static int bezeichnerWert() {
        int ergebnis = position;
        if (artWert() != 256) fehlschlagWert("identifier required"); else position++;
        String reserviertWörter = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int ausführenVorgang = 0;
        for (int Zahl = 0; Zahl <= reserviertWörter.length(); Zahl++) {
            if (Zahl == reserviertWörter.length() || reserviertWörter.charAt(Zahl) == ' ') {
                boolean gleichText = Zahl - ausführenVorgang == wortzeichenLänge[ergebnis];
                for (int platzEintrag = ausführenVorgang; gleichText && platzEintrag < Zahl; platzEintrag++) if (reserviertWörter.charAt(platzEintrag) != Quelltext[wortzeichenPosition[ergebnis] + platzEintrag - ausführenVorgang]) gleichText = false;
                if (gleichText) fehlschlagWert("reserved word cannot be an identifier");
                ausführenVorgang = Zahl + 1;
            }
        }
        return ergebnis;
    }
    static void schneidenWert() {
        int Zahl = 0;
        while (Zahl < quelltextGröße && !fehler) {
            int Wert = Quelltext[Zahl], ausführenVorgang = Zahl, artWert = Wert;
            if (Wert == 32 || Wert == 9 || Wert == 10 || Wert == 13) { Zahl++; continue; }
            if (Wert == '/' && Zahl + 1 < quelltextGröße && Quelltext[Zahl + 1] == '/') {
                while (Zahl < quelltextGröße && Quelltext[Zahl] != 10) Zahl++;
                continue;
            }
            if (Wert == '/' && Zahl + 1 < quelltextGröße && Quelltext[Zahl + 1] == '*') {
                Zahl += 2;
                while (Zahl + 1 < quelltextGröße && !(Quelltext[Zahl] == '*' && Quelltext[Zahl + 1] == '/')) Zahl++;
                if (Zahl + 1 >= quelltextGröße) { fehlschlagWert("unterminated comment"); break; }
                Zahl += 2; continue;
            }
            if (zeichenWert(Wert)) { artWert = 256; while (Zahl < quelltextGröße && Bezeichnerzeichenregeln.fortsetzungZeichen(Quelltext[Zahl])) Zahl++; }
            else if (zifferWert(Wert)) { artWert = 257; while (Zahl < quelltextGröße && zifferWert(Quelltext[Zahl])) Zahl++; }
            else if (Wert == '"' || Wert == '\'') {
                artWert = Wert == '"' ? 258 : 259; Zahl++;
                while (Zahl < quelltextGröße && Quelltext[Zahl] != Wert && Quelltext[Zahl] != 10 && Quelltext[Zahl] != 13) {
                    if (Quelltext[Zahl] == '\\') Zahl++;
                    Zahl++;
                }
                if (Zahl >= quelltextGröße || Quelltext[Zahl] != Wert) { fehlschlagWert("unterminated literal"); break; }
                Zahl++;
            } else {
                Zahl++;
                if (Zahl < quelltextGröße) {
                    int nächsterElementeintrag = Quelltext[Zahl];
                    if (Wert == '=' && nächsterElementeintrag == '=') artWert = 300;
                    if (Wert == '!' && nächsterElementeintrag == '=') artWert = 301;
                    if (Wert == '<' && nächsterElementeintrag == '=') artWert = 302;
                    if (Wert == '>' && nächsterElementeintrag == '=') artWert = 303;
                    if (Wert == '&' && nächsterElementeintrag == '&') artWert = 304;
                    if (Wert == '|' && nächsterElementeintrag == '|') artWert = 305;
                    if (Wert == '+' && nächsterElementeintrag == '+') artWert = 306;
                    if (Wert == '-' && nächsterElementeintrag == '-') artWert = 307;
                    if (Wert == '+' && nächsterElementeintrag == '=') artWert = 308;
                    if (Wert == '-' && nächsterElementeintrag == '=') artWert = 309;
                    if (Wert == '*' && nächsterElementeintrag == '=') artWert = 310;
                    if (Wert == '/' && nächsterElementeintrag == '=') artWert = 311;
                    if (Wert == '%' && nächsterElementeintrag == '=') artWert = 312;
                    if (artWert >= 300) Zahl++;
                }
            }
            if (wortzeichenAnzahl == wortzeichenArt.length - 1) { fehlschlagWert("too many tokens (2047 maximum)"); break; }
            wortzeichenArt[wortzeichenAnzahl] = artWert; wortzeichenPosition[wortzeichenAnzahl] = ausführenVorgang; wortzeichenLänge[wortzeichenAnzahl++] = Zahl - ausführenVorgang;
        }
    }
    static void konstanteByteSchreiben(int Wert) {
        if (konstanteGröße == konstanteWert.length) { fehlschlagWert("constant pool too large"); return; }
        konstanteWert[konstanteGröße++] = Wert & 255;
    }
    static void konstanteKurzSchreiben(int Wert) { konstanteByteSchreiben(Wert >> 8); konstanteByteSchreiben(Wert); }
    static int konstanteRegister(int ausführenVorgang) {
        for (int Zahl = 1; Zahl < konstanteAnzahl; Zahl++) {
            int vorderseiteWert = konstanteVersatzwert[Zahl], Länge = (Zahl + 1 < konstanteAnzahl ? konstanteVersatzwert[Zahl + 1] : ausführenVorgang) - vorderseiteWert;
            if (Länge != konstanteGröße - ausführenVorgang) continue;
            boolean gleichText = true;
            for (int platzEintrag = 0; platzEintrag < Länge; platzEintrag++) if (konstanteWert[vorderseiteWert + platzEintrag] != konstanteWert[ausführenVorgang + platzEintrag]) gleichText = false;
            if (gleichText) { konstanteGröße = ausführenVorgang; return Zahl; }
        }
        if (konstanteAnzahl == konstanteVersatzwert.length) { fehlschlagWert("too many constants"); return 0; }
        konstanteVersatzwert[konstanteAnzahl] = ausführenVorgang;
        return konstanteAnzahl++;
    }
    static void textAnhängen(int Wert) {
        if (zeichenLänge == Zeichen.length) { fehlschlagWert("text too long"); return; }
        Zeichen[zeichenLänge++] = Wert;
    }
    static void maschinenwortAnhängen(String maschinenwortText) { for (int Zahl = 0; Zahl < maschinenwortText.length(); Zahl++) textAnhängen(maschinenwortText.charAt(Zahl)); }
    static int zeichenKonstante() {
        int ausführenVorgang = konstanteGröße; konstanteByteSchreiben(1); konstanteKurzSchreiben(0);
        for (int Zahl = 0; Zahl < zeichenLänge; Zahl++) {
            int Wert = Zeichen[Zahl];
            if (Wert > 0 && Wert < 128) konstanteByteSchreiben(Wert);
            else if (Wert < 2048) { konstanteByteSchreiben(192 | Wert >> 6); konstanteByteSchreiben(128 | Wert & 63); }
            else { konstanteByteSchreiben(224 | Wert >> 12); konstanteByteSchreiben(128 | Wert >> 6 & 63); konstanteByteSchreiben(128 | Wert & 63); }
        }
        if (fehler) return 0;
        int Länge = konstanteGröße - ausführenVorgang - 3;
        konstanteWert[ausführenVorgang + 1] = Länge >> 8; konstanteWert[ausführenVorgang + 2] = Länge & 255;
        return konstanteRegister(ausführenVorgang);
    }
    static int maschinenwortKonstante(String maschinenwortText) { zeichenLänge = 0; maschinenwortAnhängen(maschinenwortText); return zeichenKonstante(); }
    static int wortzeichenKonstante(int wortzeichenWert) {
        zeichenLänge = 0;
        for (int Zahl = 0; Zahl < wortzeichenLänge[wortzeichenWert]; Zahl++) textAnhängen(Quelltext[wortzeichenPosition[wortzeichenWert] + Zahl]);
        return zeichenKonstante();
    }
    static int verweis(int artWert, int ersterOperand, int zweiterOperand) {
        int ausführenVorgang = konstanteGröße; konstanteByteSchreiben(artWert); konstanteKurzSchreiben(ersterOperand);
        if (artWert == 9 || artWert == 10 || artWert == 12) konstanteKurzSchreiben(zweiterOperand);
        return konstanteRegister(ausführenVorgang);
    }
    static int externVerweis(int artWert, String eigentümerWert, String Name, String beschreibungWert) {
        int eigentümerBezeichner = verweis(7, maschinenwortKonstante(eigentümerWert), 0);
        int nameAnzahl = maschinenwortKonstante(Name), formatAnzahl = maschinenwortKonstante(beschreibungWert);
        return verweis(artWert, eigentümerBezeichner, verweis(12, nameAnzahl, formatAnzahl));
    }
    static void wertAusgeben(int Wert) {
        if (kodeGröße == kodeWert.length) { fehlschlagWert("bytecode too large"); return; }
        kodeWert[kodeGröße++] = Wert & 255;
    }
    static void befehl(int Wert, int argumente) { wertAusgeben(Wert); wertAusgeben(argumente >> 8); wertAusgeben(argumente); }
    static void numerischKonstante(int Wert) {
        if (Wert >= -1 && Wert <= 5) { wertAusgeben(Wert + 3); return; }
        int ausführenVorgang = konstanteGröße; konstanteByteSchreiben(3); konstanteKurzSchreiben(Wert >>> 16); konstanteKurzSchreiben(Wert);
        befehl(19, konstanteRegister(ausführenVorgang));
    }
    static int verzweigung(int befehl) { int ergebnis = kodeGröße; befehl(befehl, 0); return ergebnis; }
    static void bindenWert(int verzweigung, int zielobjektObjekt) {
        if (fehler) return;
        int entfernungWert = zielobjektObjekt - verzweigung;
        if (entfernungWert < -32768 || entfernungWert > 32767 || verzweigung < 0 || verzweigung + 2 >= kodeGröße) { fehlschlagWert("invalid branch"); return; }
        kodeWert[verzweigung + 1] = entfernungWert >> 8 & 255; kodeWert[verzweigung + 2] = entfernungWert & 255;
    }
    static void vergleichWert(int befehl) {
        int wahrWert = verzweigung(befehl); wertAusgeben(3); int endung = verzweigung(167);
        bindenWert(wahrWert, kodeGröße); wertAusgeben(4); bindenWert(endung, kodeGröße);
    }
    static int formatWert() {
        if (entnehmenMaschinenwort("void")) return 0;
        if (entnehmenMaschinenwort("int")) return 1;
        if (entnehmenMaschinenwort("boolean")) return 2;
        if (entnehmenMaschinenwort("char")) return 5;
        if (entnehmenMaschinenwort("FileInputStream")) return 6;
        if (entnehmenMaschinenwort("FileOutputStream")) return 7;
        if (entnehmenMaschinenwort("String")) { if (empfangen('[')) { anforderungWert(']'); return 4; } return 3; }
        fehlschlagWert("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void formatHinzufügen(int typWert) {
        if (typWert == 0) textAnhängen('V');
        if (typWert == 1) textAnhängen('I');
        if (typWert == 2) textAnhängen('Z');
        if (typWert == 3) maschinenwortAnhängen("Ljava/lang/String;");
        if (typWert == 4) maschinenwortAnhängen("[Ljava/lang/String;");
        if (typWert == 5) textAnhängen('C');
        if (typWert == 6) maschinenwortAnhängen("Ljava/io/FileInputStream;");
        if (typWert == 7) maschinenwortAnhängen("Ljava/io/FileOutputStream;");
    }
    // Der eingeschränkte Übersetzer unterstützt throws-Deklarationen. Ausnahmebehandlungsrümpfe benötigen javac auf dem Host.
    static void ausnahmeNameLesen() {
        boolean KoreanischBündel = entnehmenMaschinenwort("Deutsch");
        if (KoreanischBündel) { anforderungWert('.'); erfordernMaschinenwort("eigen"); anforderungWert('.'); }
        if (!KoreanischBündel && (entnehmenMaschinenwort("Exception") || entnehmenMaschinenwort("IOException"))) return;
        if (entnehmenMaschinenwort("ausnahme") || entnehmenMaschinenwort("AusführungAusnahme") || entnehmenMaschinenwort("EingabeAusgabeAusnahme") || entnehmenMaschinenwort("WartenZeitüberschreitungAusnahme") || entnehmenMaschinenwort("AdresseNachschlagenAusnahme") || entnehmenMaschinenwort("FehlendDateiAusnahme") || entnehmenMaschinenwort("KommunikationAusnahme") || entnehmenMaschinenwort("UngültigArgumentAusnahme") || entnehmenMaschinenwort("NummerFormatFehlschlag") || entnehmenMaschinenwort("GrenzenAusnahme") || entnehmenMaschinenwort("DatenfeldGrenzenAusnahme") || entnehmenMaschinenwort("ZeichenketteGrenzenAusnahme") || entnehmenMaschinenwort("NullverweisVerweisAusnahme") || entnehmenMaschinenwort("ArithmetikFehlschlag") || entnehmenMaschinenwort("StatuswertAusnahme") || entnehmenMaschinenwort("TypTypumwandlungAusnahme") || entnehmenMaschinenwort("NegativDatenfeldGrößeFehlschlag") || entnehmenMaschinenwort("DatenfeldAblegenDatenFehlschlag") || entnehmenMaschinenwort("AusführungsfadenStatuswertAusnahme") || entnehmenMaschinenwort("WartenUnterbrochenAusnahme")) return;
        fehlschlagWert("unsupported throws type");
    }
    static void deklarationLesen() {
        while (entnehmenMaschinenwort("import")) {
            if (maschinenwortWert(position, "Deutsch")) ausnahmeNameLesen();
            else {
                erfordernMaschinenwort("java"); anforderungWert('.'); erfordernMaschinenwort("io"); anforderungWert('.');
                if (!(entnehmenMaschinenwort("FileInputStream") || entnehmenMaschinenwort("FileOutputStream") || entnehmenMaschinenwort("IOException"))) fehlschlagWert("unsupported import");
            }
            anforderungWert(';');
        }
        entnehmenMaschinenwort("public"); entnehmenMaschinenwort("final"); erfordernMaschinenwort("class"); klasseWortzeichen = bezeichnerWert();
        klasseKonstante = verweis(7, wortzeichenKonstante(klasseWortzeichen), 0);
        elternknotenKonstante = verweis(7, maschinenwortKonstante("java/lang/Object"), 0); kodeKonstante = maschinenwortKonstante("Code"); anforderungWert('{');
        while (!fehler && artWert() != '}') {
            if (methodeAnzahl == 32) { fehlschlagWert("too many methods"); break; }
            int zugriffEintrag = entnehmenMaschinenwort("public") ? 1 : entnehmenMaschinenwort("private") ? 2 : 0; erfordernMaschinenwort("static");
            int Funktion = methodeAnzahl++;
            methodeZugriff[Funktion] = zugriffEintrag | 8;
            methodeZurückkehren[Funktion] = formatWert(); methodeEintragName[Funktion] = bezeichnerWert(); anforderungWert('(');
            for (int vorderseiteWert = 0; vorderseiteWert < Funktion; vorderseiteWert++) if (namenGleich(methodeEintragName[vorderseiteWert], methodeEintragName[Funktion])) fehlschlagWert("duplicate method (overloading unsupported)");
            while (!fehler && artWert() != ')') {
                int Zahl = methodeArgumentAnzahl[Funktion];
                if (Zahl == 16) { fehlschlagWert("too many parameters"); break; }
                int typWert = formatWert(); if (typWert == 0) fehlschlagWert("void parameter");
                methodeArgumentTyp[Funktion * 16 + Zahl] = typWert; methodeArgumentName[Funktion * 16 + Zahl] = bezeichnerWert();
                methodeArgumentAnzahl[Funktion]++;
                if (!empfangen(',')) break;
            }
            anforderungWert(')');
            if (entnehmenMaschinenwort("throws")) {
                do { ausnahmeNameLesen(); } while (!fehler && empfangen(','));
            }
            methodeRumpf[Funktion] = position; anforderungWert('{');
            int verschachtelungWert = 1;
            while (position < wortzeichenAnzahl && verschachtelungWert > 0) {
                if (artWert() == '{') verschachtelungWert++;
                if (artWert() == '}') verschachtelungWert--;
                position++;
            }
            if (verschachtelungWert != 0) fehlschlagWert("unclosed method body");
            methodeEnde[Funktion] = position;
            methodeNameKonstante[Funktion] = wortzeichenKonstante(methodeEintragName[Funktion]);
            zeichenLänge = 0; textAnhängen('(');
            for (int Zahl = 0; Zahl < methodeArgumentAnzahl[Funktion]; Zahl++) formatHinzufügen(methodeArgumentTyp[Funktion * 16 + Zahl]);
            textAnhängen(')'); formatHinzufügen(methodeZurückkehren[Funktion]); methodeDeskriptorKonstante[Funktion] = zeichenKonstante();
        }
        anforderungWert('}'); if (position != wortzeichenAnzahl) fehlschlagWert("extra input after class");
    }
    static int lokalFinden(int Name) {
        for (int Zahl = lokalAnzahl - 1; Zahl >= 0; Zahl--) if (lokalTiefe[Zahl] >= 0 && namenGleich(lokalName[Zahl], Name)) return Zahl;
        fehlschlagWert("unknown variable"); return 0;
    }
    static int lokalHinzufügen(int Name, int typWert) {
        for (int Zahl = 0; Zahl < lokalAnzahl; Zahl++) if (lokalTiefe[Zahl] >= 0 && namenGleich(lokalName[Zahl], Name)) fehlschlagWert("duplicate local variable");
        if (lokalAnzahl == 128) { fehlschlagWert("too many locals"); return 0; }
        lokalName[lokalAnzahl] = Name; lokalTyp[lokalAnzahl] = typWert; lokalTiefe[lokalAnzahl] = tiefeWert;
        return lokalAnzahl++;
    }
    static boolean ganzzahlTyp(int typWert) { return typWert == 1 || typWert == 5; }
    static void lokalLesen(int Zahl) { wertAusgeben(lokalTyp[Zahl] <= 2 || lokalTyp[Zahl] == 5 ? 21 : 25); wertAusgeben(Zahl); }
    static void lokalSchreiben(int Zahl) { wertAusgeben(lokalTyp[Zahl] <= 2 || lokalTyp[Zahl] == 5 ? 54 : 58); wertAusgeben(Zahl); }
    static void typÜberprüfen(int tatsächlichDaten, int erwartung) { if (tatsächlichDaten != erwartung && !(tatsächlichDaten == 5 && erwartung == 1)) fehlschlagWert("type mismatch"); }
    static void zeichenWertLesen(int wortzeichenWert) {
        zeichenLänge = 0; int ausführenVorgang = wortzeichenPosition[wortzeichenWert] + 1, endung = wortzeichenPosition[wortzeichenWert] + wortzeichenLänge[wortzeichenWert] - 1;
        while (ausführenVorgang < endung && !fehler) {
            int Wert = Quelltext[ausführenVorgang++];
            if (Wert == '\\') {
                if (ausführenVorgang == endung) { fehlschlagWert("invalid escape"); break; }
                Wert = Quelltext[ausführenVorgang++];
                if (Wert == 'n') Wert = 10;
                else if (Wert == 'r') Wert = 13;
                else if (Wert == 't') Wert = 9;
                else if (Wert == 'b') Wert = 8;
                else if (Wert == 'f') Wert = 12;
                else if (Wert != '\\' && Wert != '"' && Wert != '\'') fehlschlagWert("unsupported escape");
            }
            textAnhängen(Wert);
        }
    }
    static int ganzzahlAnalysieren(int wortzeichenWert, boolean negativWert) {
        if (wortzeichenLänge[wortzeichenWert] > 1 && Quelltext[wortzeichenPosition[wortzeichenWert]] == '0') fehlschlagWert("octal literals unsupported");
        int Wert = 0;
        for (int Zahl = 0; Zahl < wortzeichenLänge[wortzeichenWert]; Zahl++) {
            int zifferElementeintrag = Quelltext[wortzeichenPosition[wortzeichenWert] + Zahl] - '0';
            if (Wert < -214748364 || Wert == -214748364 && zifferElementeintrag > (negativWert ? 8 : 7)) fehlschlagWert("integer literal out of range");
            Wert = Wert * 10 - zifferElementeintrag;
        }
        return negativWert ? Wert : -Wert;
    }
    static int hauptAusdruck() {
        if (entnehmenMaschinenwort("new")) {
            int typWert = formatWert();
            if (typWert != 6 && typWert != 7) { fehlschlagWert("only file streams supported by new in source"); return 0; }
            String eigentümerWert = typWert == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            befehl(187, verweis(7, maschinenwortKonstante(eigentümerWert), 0)); wertAusgeben(89);
            anforderungWert('('); typÜberprüfen(ausdruckWert(), 3); boolean fortsetzungWert = false;
            if (empfangen(',')) { if (typWert != 7) fehlschlagWert("input stream constructor arguments"); typÜberprüfen(ausdruckWert(), 2); fortsetzungWert = true; }
            anforderungWert(')');
            befehl(183, externVerweis(10, eigentümerWert, "<init>", fortsetzungWert ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return typWert;
        }
        if (empfangen('(')) { int typWert = ausdruckWert(); anforderungWert(')'); return typWert; }
        if (artWert() == 257) { numerischKonstante(ganzzahlAnalysieren(position++, false)); return 1; }
        if (artWert() == 258) { zeichenWertLesen(position++); befehl(19, verweis(8, zeichenKonstante(), 0)); return 3; }
        if (artWert() == 259) { zeichenWertLesen(position++); if (zeichenLänge != 1) fehlschlagWert("character literal length"); numerischKonstante(Zeichen[0]); return 5; }
        if (entnehmenMaschinenwort("true")) { wertAusgeben(4); return 2; }
        if (entnehmenMaschinenwort("false")) { wertAusgeben(3); return 2; }
        if (entnehmenMaschinenwort("Deutsch")) {
            anforderungWert('.'); erfordernMaschinenwort("eigen"); anforderungWert('.');
            String eigentümerWert = "", methodeWert = "", beschreibungWert = ""; int ersterOperand = 0, zweiterOperand = 0, dritterOperand = 0, vierterOperand = 0, fünfterOperand = 0, ergebnis = 0;
            if (entnehmenMaschinenwort("Ausgabe")) {
                eigentümerWert = "Deutsch/eigen/Ausgabe"; anforderungWert('.');
                if (entnehmenMaschinenwort("zeileSchreiben")) { methodeWert = "zeileSchreiben"; beschreibungWert = "(Ljava/lang/String;)V"; ersterOperand = 3; }
                else if (entnehmenMaschinenwort("schreiben")) { methodeWert = "schreiben"; beschreibungWert = "(Ljava/lang/String;)V"; ersterOperand = 3; }
                else if (entnehmenMaschinenwort("nummerSchreiben")) { methodeWert = "nummerSchreiben"; beschreibungWert = "(I)V"; ersterOperand = 1; }
                else fehlschlagWert("unknown Korean output method");
            } else if (entnehmenMaschinenwort("Zeichen")) {
                eigentümerWert = "Deutsch/eigen/Zeichen"; anforderungWert('.'); ersterOperand = 3;
                if (entnehmenMaschinenwort("Länge")) { methodeWert = "Länge"; beschreibungWert = "(Ljava/lang/String;)I"; ergebnis = 1; }
                else if (entnehmenMaschinenwort("kodePunktAnzahl")) { methodeWert = "kodePunktAnzahl"; beschreibungWert = "(Ljava/lang/String;)I"; ergebnis = 1; }
                else if (entnehmenMaschinenwort("ganzzahlAnalysieren")) { methodeWert = "ganzzahlAnalysieren"; beschreibungWert = "(Ljava/lang/String;)I"; ergebnis = 1; }
                else if (entnehmenMaschinenwort("ganzzahlWertSchreiben")) { methodeWert = "ganzzahlWertSchreiben"; beschreibungWert = "(I)Ljava/lang/String;"; ersterOperand = 1; ergebnis = 3; }
                else if (entnehmenMaschinenwort("gleichText")) { methodeWert = "gleichText"; beschreibungWert = "(Ljava/lang/String;Ljava/lang/String;)Z"; zweiterOperand = 3; ergebnis = 2; }
                else if (entnehmenMaschinenwort("einsetzenText")) { methodeWert = "einsetzenText"; beschreibungWert = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; zweiterOperand = 3; ergebnis = 3; }
                else if (entnehmenMaschinenwort("schneidenWert")) { methodeWert = "schneidenWert"; beschreibungWert = "(Ljava/lang/String;II)Ljava/lang/String;"; zweiterOperand = 1; dritterOperand = 1; ergebnis = 3; }
                else fehlschlagWert("unknown Korean text method");
            } else if (entnehmenMaschinenwort("Datei")) {
                eigentümerWert = "Deutsch/eigen/Datei"; anforderungWert('.'); ersterOperand = 3;
                if (entnehmenMaschinenwort("lesen")) { methodeWert = "lesen"; beschreibungWert = "(Ljava/lang/String;)Ljava/lang/String;"; ergebnis = 3; }
                else if (entnehmenMaschinenwort("schreiben")) { methodeWert = "schreiben"; beschreibungWert = "(Ljava/lang/String;Ljava/lang/String;)V"; zweiterOperand = 3; }
                else fehlschlagWert("unknown Korean file method");
            } else if (entnehmenMaschinenwort("Bildschirm")) {
                eigentümerWert = "Deutsch/eigen/Bildschirm"; anforderungWert('.');
                if (entnehmenMaschinenwort("breiteWert")) { methodeWert = "breiteWert"; beschreibungWert = "()I"; ergebnis = 1; }
                else if (entnehmenMaschinenwort("höheWert")) { methodeWert = "höheWert"; beschreibungWert = "()I"; ergebnis = 1; }
                else if (entnehmenMaschinenwort("rechteck")) { methodeWert = "rechteck"; beschreibungWert = "(IIIII)V"; ersterOperand = 1; zweiterOperand = 1; dritterOperand = 1; vierterOperand = 1; fünfterOperand = 1; }
                else if (entnehmenMaschinenwort("eintragTilgen")) { methodeWert = "eintragTilgen"; beschreibungWert = "(I)V"; ersterOperand = 1; }
                else if (entnehmenMaschinenwort("abwarten")) { methodeWert = "abwarten"; beschreibungWert = "()V"; }
                else fehlschlagWert("unknown Korean framebuffer method");
            } else fehlschlagWert("unsupported Korean library class");
            anforderungWert('('); if (ersterOperand != 0) typÜberprüfen(ausdruckWert(), ersterOperand);
            if (zweiterOperand != 0) { anforderungWert(','); typÜberprüfen(ausdruckWert(), zweiterOperand); }
            if (dritterOperand != 0) { anforderungWert(','); typÜberprüfen(ausdruckWert(), dritterOperand); }
            if (vierterOperand != 0) { anforderungWert(','); typÜberprüfen(ausdruckWert(), vierterOperand); }
            if (fünfterOperand != 0) { anforderungWert(','); typÜberprüfen(ausdruckWert(), fünfterOperand); }
            anforderungWert(')'); befehl(184, externVerweis(10, eigentümerWert, methodeWert, beschreibungWert)); return ergebnis;
        }
        if (entnehmenMaschinenwort("Integer")) {
            anforderungWert('.'); erfordernMaschinenwort("parseInt"); anforderungWert('('); typÜberprüfen(ausdruckWert(), 3); anforderungWert(')');
            befehl(184, externVerweis(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Name = bezeichnerWert();
        if (empfangen('(')) {
            int Funktion = -1;
            for (int Zahl = 0; Zahl < methodeAnzahl; Zahl++) if (namenGleich(Name, methodeEintragName[Zahl])) Funktion = Zahl;
            if (Funktion < 0) { fehlschlagWert("unknown static method"); return 0; }
            int Zahl = 0;
            while (!fehler && artWert() != ')') {
                if (Zahl >= methodeArgumentAnzahl[Funktion]) { fehlschlagWert("too many arguments"); break; }
                typÜberprüfen(ausdruckWert(), methodeArgumentTyp[Funktion * 16 + Zahl++]); if (!empfangen(',')) break;
            }
            anforderungWert(')'); if (Zahl != methodeArgumentAnzahl[Funktion]) fehlschlagWert("argument count mismatch");
            befehl(184, verweis(10, klasseKonstante, verweis(12, methodeNameKonstante[Funktion], methodeDeskriptorKonstante[Funktion])));
            return methodeZurückkehren[Funktion];
        }
        int lokalGültigkeitsbereich = lokalFinden(Name), typWert = lokalTyp[lokalGültigkeitsbereich]; lokalLesen(lokalGültigkeitsbereich);
        while (!fehler) {
            if (empfangen('[')) { typÜberprüfen(typWert, 4); typÜberprüfen(ausdruckWert(), 1); anforderungWert(']'); wertAusgeben(50); typWert = 3; }
            else if (empfangen('.')) {
                if (typWert == 6 || typWert == 7) {
                    String eigentümerWert = typWert == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (entnehmenMaschinenwort("close")) { anforderungWert('('); anforderungWert(')'); befehl(182, externVerweis(10, eigentümerWert, "close", "()V")); typWert = 0; }
                    else if (typWert == 6 && entnehmenMaschinenwort("read")) { anforderungWert('('); anforderungWert(')'); befehl(182, externVerweis(10, eigentümerWert, "read", "()I")); typWert = 1; }
                    else if (typWert == 7 && entnehmenMaschinenwort("write")) { anforderungWert('('); typÜberprüfen(ausdruckWert(), 1); anforderungWert(')'); befehl(182, externVerweis(10, eigentümerWert, "write", "(I)V")); typWert = 0; }
                    else { fehlschlagWert("unsupported file stream method"); }
                    continue;
                }
                erfordernMaschinenwort("length");
                if (typWert == 4) { wertAusgeben(190); typWert = 1; }
                else { typÜberprüfen(typWert, 3); anforderungWert('('); anforderungWert(')'); befehl(182, externVerweis(10, "java/lang/String", "length", "()I")); typWert = 1; }
            } else break;
        }
        return typWert;
    }
    static int einstelligWert() {
        if (++ausdruckTiefe > 64) { fehlschlagWert("expression nesting too deep"); ausdruckTiefe--; return 0; }
        int typWert;
        if (empfangen('!')) { typÜberprüfen(einstelligWert(), 2); vergleichWert(153); typWert = 2; }
        else if (empfangen('-')) {
            if (artWert() == 257) numerischKonstante(ganzzahlAnalysieren(position++, true));
            else { typÜberprüfen(einstelligWert(), 1); wertAusgeben(116); }
            typWert = 1;
        } else if (empfangen('+')) { typÜberprüfen(einstelligWert(), 1); typWert = 1; }
        else typWert = hauptAusdruck();
        ausdruckTiefe--; return typWert;
    }
    static int multiplikationAusdruck() {
        int typWert = einstelligWert();
        while (!fehler && (artWert() == '*' || artWert() == '/' || artWert() == '%')) {
            int kodierungWert = artWert(); position++; typÜberprüfen(typWert, 1); typÜberprüfen(einstelligWert(), 1);
            wertAusgeben(kodierungWert == '*' ? 104 : kodierungWert == '/' ? 108 : 112); typWert = 1;
        }
        return typWert;
    }
    static int additionAusdruck() {
        int typWert = multiplikationAusdruck();
        while (!fehler && (artWert() == '+' || artWert() == '-')) {
            int kodierungWert = artWert(); position++; int grenzstelleWert = kodeGröße, rückseiteWertTyp = multiplikationAusdruck();
            if (kodierungWert == '+' && (typWert == 3 || rückseiteWertTyp == 3)) { zusammenfügenWerte(grenzstelleWert, typWert, rückseiteWertTyp); typWert = 3; }
            else { typÜberprüfen(typWert, 1); typÜberprüfen(rückseiteWertTyp, 1); wertAusgeben(kodierungWert == '+' ? 96 : 100); typWert = 1; }
        }
        return typWert;
    }
    static int angehängtVerweis(int typWert) {
        if (typWert != 1 && typWert != 2 && typWert != 3 && typWert != 5) fehlschlagWert("unsupported concatenation type");
        return externVerweis(10, "java/lang/StringBuilder", "append", typWert == 1 ? "(I)Ljava/lang/StringBuilder;"
            : typWert == 2 ? "(Z)Ljava/lang/StringBuilder;" : typWert == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void zusammenfügenWerte(int grenzstelleWert, int vorderseiteWertTyp, int rückseiteWertTyp) {
        // Erzeugten Code vor dem rechten Operanden einfügen, damit der bereits berechnete linke Wert zuerst per append angefügt wird.
        // Relative Sprungabstände im rechten Ausdruck bleiben erhalten, weil der gesamte Bereich gemeinsam verschoben wird.
        int endung = kodeGröße;
        befehl(187, verweis(7, maschinenwortKonstante("java/lang/StringBuilder"), 0)); wertAusgeben(89);
        befehl(183, externVerweis(10, "java/lang/StringBuilder", "<init>", "()V")); wertAusgeben(95); befehl(182, angehängtVerweis(vorderseiteWertTyp));
        if (fehler) return;
        int Länge = kodeGröße - endung;
        for (int Zahl = 0; Zahl < Länge; Zahl++) eingefügtKode[Zahl] = kodeWert[endung + Zahl];
        for (int Zahl = endung - 1; Zahl >= grenzstelleWert; Zahl--) kodeWert[Zahl + Länge] = kodeWert[Zahl];
        for (int Zahl = 0; Zahl < Länge; Zahl++) kodeWert[grenzstelleWert + Zahl] = eingefügtKode[Zahl];
        befehl(182, angehängtVerweis(rückseiteWertTyp)); befehl(182, externVerweis(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int vergleichAusdruck() {
        int typWert = additionAusdruck();
        while (!fehler && (artWert() == '<' || artWert() == '>' || artWert() == 302 || artWert() == 303)) {
            int kodierungWert = artWert(); position++; typÜberprüfen(typWert, 1); typÜberprüfen(additionAusdruck(), 1);
            vergleichWert(kodierungWert == '<' ? 161 : kodierungWert == '>' ? 163 : kodierungWert == 302 ? 164 : 162); typWert = 2;
        }
        return typWert;
    }
    static int gleichheitAusdruck() {
        int typWert = vergleichAusdruck();
        while (!fehler && (artWert() == 300 || artWert() == 301)) {
            int kodierungWert = artWert(); position++; int rückseiteWertTyp = vergleichAusdruck();
            if (typWert == 0 || rückseiteWertTyp == 0) fehlschlagWert("void expression");
            if (!(ganzzahlTyp(typWert) && ganzzahlTyp(rückseiteWertTyp))) typÜberprüfen(rückseiteWertTyp, typWert);
            vergleichWert((typWert <= 2 || typWert == 5 ? 159 : 165) + (kodierungWert == 301 ? 1 : 0)); typWert = 2;
        }
        return typWert;
    }
    static int logischUnd() {
        int typWert = gleichheitAusdruck();
        while (!fehler && empfangen(304)) {
            typÜberprüfen(typWert, 2); int ersterOperand = verzweigung(153); typÜberprüfen(gleichheitAusdruck(), 2); int zweiterOperand = verzweigung(153);
            wertAusgeben(4); int endung = verzweigung(167); bindenWert(ersterOperand, kodeGröße); bindenWert(zweiterOperand, kodeGröße); wertAusgeben(3); bindenWert(endung, kodeGröße); typWert = 2;
        }
        return typWert;
    }
    static int ausdruckWert() {
        int typWert = logischUnd();
        while (!fehler && empfangen(305)) {
            typÜberprüfen(typWert, 2); int ersterOperand = verzweigung(154); typÜberprüfen(logischUnd(), 2); int zweiterOperand = verzweigung(154);
            wertAusgeben(3); int endung = verzweigung(167); bindenWert(ersterOperand, kodeGröße); bindenWert(zweiterOperand, kodeGröße); wertAusgeben(4); bindenWert(endung, kodeGröße); typWert = 2;
        }
        return typWert;
    }
    static void zuweisungWert(boolean deklarationErlauben) {
        if (maschinenwortWert(position, "int") || maschinenwortWert(position, "boolean") || maschinenwortWert(position, "String") || maschinenwortWert(position, "char")
            || maschinenwortWert(position, "FileInputStream") || maschinenwortWert(position, "FileOutputStream")) {
            if (!deklarationErlauben) fehlschlagWert("declaration not allowed here");
            int typWert = formatWert(), Name = bezeichnerWert(); anforderungWert('='); typÜberprüfen(ausdruckWert(), typWert);
            lokalSchreiben(lokalHinzufügen(Name, typWert)); return;
        }
        int Name = bezeichnerWert(), lokalGültigkeitsbereich = lokalFinden(Name);
        if (empfangen('=')) { typÜberprüfen(ausdruckWert(), lokalTyp[lokalGültigkeitsbereich]); lokalSchreiben(lokalGültigkeitsbereich); }
        else if (artWert() >= 308 && artWert() <= 312) {
            int kodierungWert = artWert(); position++; lokalLesen(lokalGültigkeitsbereich); int grenzstelleWert = kodeGröße, rückseiteWertTyp = ausdruckWert();
            if (kodierungWert == 308 && lokalTyp[lokalGültigkeitsbereich] == 3) zusammenfügenWerte(grenzstelleWert, 3, rückseiteWertTyp);
            else {
                typÜberprüfen(lokalTyp[lokalGültigkeitsbereich], 1); typÜberprüfen(rückseiteWertTyp, 1);
                wertAusgeben(kodierungWert == 308 ? 96 : kodierungWert == 309 ? 100 : kodierungWert == 310 ? 104 : kodierungWert == 311 ? 108 : 112);
                if (lokalTyp[lokalGültigkeitsbereich] == 5) wertAusgeben(146);
            }
            lokalSchreiben(lokalGültigkeitsbereich);
        }
        else if (artWert() == 306 || artWert() == 307) {
            typÜberprüfen(lokalTyp[lokalGültigkeitsbereich], 1); wertAusgeben(132); wertAusgeben(lokalGültigkeitsbereich); wertAusgeben(artWert() == 306 ? 1 : 255); position++;
            if (lokalTyp[lokalGültigkeitsbereich] == 5) { lokalLesen(lokalGültigkeitsbereich); wertAusgeben(146); lokalSchreiben(lokalGültigkeitsbereich); }
        } else fehlschlagWert("assignment or postfix increment required");
    }
    static void bildschirmAusgabe() {
        erfordernMaschinenwort("System"); anforderungWert('.'); erfordernMaschinenwort("out"); anforderungWert('.');
        boolean zeilenumbruch = entnehmenMaschinenwort("println"); if (!zeilenumbruch) erfordernMaschinenwort("print"); anforderungWert('(');
        befehl(178, externVerweis(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean leerwertArgument = artWert() == ')';
        int typWert = leerwertArgument ? 0 : ausdruckWert(); anforderungWert(')'); anforderungWert(';');
        String beschreibungWert = typWert == 0 ? "()V" : typWert == 1 ? "(I)V" : typWert == 2 ? "(Z)V" : typWert == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (typWert == 4 || typWert >= 6 || typWert == 0 && (!zeilenumbruch || !leerwertArgument)) fehlschlagWert("unsupported print argument");
        befehl(182, externVerweis(10, "java/io/PrintStream", zeilenumbruch ? "println" : "print", beschreibungWert));
    }
    static boolean anweisungWert() {
        if (fehler) return false;
        if (tiefeWert > 32) { fehlschlagWert("statement nesting too deep"); return false; }
        if (empfangen('{')) {
            tiefeWert++; boolean zurückkehrenErgebnis = false;
            while (!fehler && artWert() != '}') { if (zurückkehrenErgebnis) fehlschlagWert("unreachable statement"); zurückkehrenErgebnis = anweisungWert(); }
            anforderungWert('}'); for (int Zahl = 0; Zahl < lokalAnzahl; Zahl++) if (lokalTiefe[Zahl] == tiefeWert) lokalTiefe[Zahl] = -1;
            tiefeWert--; return zurückkehrenErgebnis;
        }
        if (empfangen(';')) return false;
        if (entnehmenMaschinenwort("return")) {
            int typWert = artWert() == ';' ? 0 : ausdruckWert(); typÜberprüfen(typWert, methodeZurückkehren[aktuellMethode]); anforderungWert(';');
            wertAusgeben(typWert == 0 ? 177 : typWert <= 2 || typWert == 5 ? 172 : 176); return true;
        }
        if (entnehmenMaschinenwort("if")) {
            anforderungWert('('); typÜberprüfen(ausdruckWert(), 2); anforderungWert(')'); int falschWert = verzweigung(153);
            tiefeWert++; boolean ersterOperand = steuerungAnweisung(); tiefeWert--;
            if (entnehmenMaschinenwort("else")) { int endung = verzweigung(167); bindenWert(falschWert, kodeGröße); tiefeWert++; boolean zweiterOperand = steuerungAnweisung(); tiefeWert--; bindenWert(endung, kodeGröße); return ersterOperand && zweiterOperand; }
            bindenWert(falschWert, kodeGröße); return false;
        }
        if (entnehmenMaschinenwort("while")) {
            int ausführenVorgang = kodeGröße; anforderungWert('('); typÜberprüfen(ausdruckWert(), 2); anforderungWert(')'); int endung = verzweigung(153);
            tiefeWert++; steuerungAnweisung(); tiefeWert--; bindenWert(verzweigung(167), ausführenVorgang); bindenWert(endung, kodeGröße); return false;
        }
        if (entnehmenMaschinenwort("for")) {
            tiefeWert++; anforderungWert('('); if (artWert() != ';') zuweisungWert(true); anforderungWert(';');
            int bedingung = kodeGröße; if (artWert() == ';') wertAusgeben(4); else typÜberprüfen(ausdruckWert(), 2); anforderungWert(';');
            int endung = verzweigung(153), rumpfText = verzweigung(167), auffrischen = kodeGröße;
            if (artWert() != ')') zuweisungWert(false); anforderungWert(')'); bindenWert(verzweigung(167), bedingung); bindenWert(rumpfText, kodeGröße);
            steuerungAnweisung(); bindenWert(verzweigung(167), auffrischen); bindenWert(endung, kodeGröße);
            for (int Zahl = 0; Zahl < lokalAnzahl; Zahl++) if (lokalTiefe[Zahl] == tiefeWert) lokalTiefe[Zahl] = -1;
            tiefeWert--; return false;
        }
        if (maschinenwortWert(position, "System")) { bildschirmAusgabe(); return false; }
        if (artWert() == 256 && position + 1 < wortzeichenAnzahl && (wortzeichenArt[position + 1] == '(' || wortzeichenArt[position + 1] == '.')) {
            int typWert = ausdruckWert(); if (typWert != 0) wertAusgeben(87); anforderungWert(';'); return false;
        }
        zuweisungWert(true); anforderungWert(';'); return false;
    }
    static boolean steuerungAnweisung() {
        if (maschinenwortWert(position, "int") || maschinenwortWert(position, "boolean") || maschinenwortWert(position, "char") || maschinenwortWert(position, "String")
            || maschinenwortWert(position, "FileInputStream") || maschinenwortWert(position, "FileOutputStream")) fehlschlagWert("local declaration requires braces");
        return anweisungWert();
    }
    static void klasseByteAusgeben(int Wert) { if (ausgabeGröße == Ausgabe.length) fehlschlagWert("class file too large"); else Ausgabe[ausgabeGröße++] = Wert & 255; }
    static void klasseKurzAusgeben(int Wert) { klasseByteAusgeben(Wert >> 8); klasseByteAusgeben(Wert); }
    static void klasseGanzzahlAusgeben(int Wert) { klasseKurzAusgeben(Wert >>> 16); klasseKurzAusgeben(Wert); }
    static void klasseSchreiben() {
        klasseGanzzahlAusgeben(0xcafebabe); klasseKurzAusgeben(0); klasseKurzAusgeben(49); klasseKurzAusgeben(konstanteAnzahl);
        for (int Zahl = 0; Zahl < konstanteGröße; Zahl++) klasseByteAusgeben(konstanteWert[Zahl]);
        klasseKurzAusgeben(0x21); klasseKurzAusgeben(klasseKonstante); klasseKurzAusgeben(elternknotenKonstante); klasseKurzAusgeben(0); klasseKurzAusgeben(0); klasseKurzAusgeben(methodeAnzahl);
        for (int Zahl = 0; Zahl < methodeAnzahl; Zahl++) {
            klasseKurzAusgeben(methodeZugriff[Zahl]); klasseKurzAusgeben(methodeNameKonstante[Zahl]); klasseKurzAusgeben(methodeDeskriptorKonstante[Zahl]); klasseKurzAusgeben(1); klasseKurzAusgeben(kodeKonstante);
            klasseGanzzahlAusgeben(12 + methodeLänge[Zahl]); klasseKurzAusgeben(128); klasseKurzAusgeben(methodeLokalvariablen[Zahl]); klasseGanzzahlAusgeben(methodeLänge[Zahl]);
            for (int platzEintrag = 0; platzEintrag < methodeLänge[Zahl]; platzEintrag++) klasseByteAusgeben(kodeWert[methodeKode[Zahl] + platzEintrag]);
            klasseKurzAusgeben(0); klasseKurzAusgeben(0);
        }
        klasseKurzAusgeben(0);
    }
    public static int ausführenVorgang() {
        if (Benutzer.argumenteAnzahl() == 1 && JavaWerkzeug.gleichText(Benutzer.argumente(0), "-version")) {
            Benutzer.schreiben("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (Benutzer.argumenteAnzahl() != 1) { Benutzer.schreiben("Usage: javac FILE.java\n"); return 2; }
        int nameGröße = JavaWerkzeug.Name(dateiNameText, Benutzer.argumente(0));
        if (nameGröße < 6 || nameGröße > 62 || dateiNameText[nameGröße - 5] != '.' || dateiNameText[nameGröße - 4] != 'j'
            || dateiNameText[nameGröße - 3] != 'a' || dateiNameText[nameGröße - 2] != 'v' || dateiNameText[nameGröße - 1] != 'a') {
            Benutzer.schreiben("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        quelltextGröße = Benutzer.dateiLesen(dateiNameText, Quelltext);
        if (quelltextGröße < 0) { Benutzer.schreiben("javac: cannot read source: "); JavaWerkzeug.nummerSchreiben(quelltextGröße); Benutzer.zeichenWertSchreiben(10); return 1; }
        quelltextGröße = JavaWerkzeug.quelltextDekodieren(Quelltext, quelltextGröße);
        if (quelltextGröße < 0) { Benutzer.schreiben("javac error: invalid UTF-8 source\n"); return 1; }
        schneidenWert(); if (!fehler) deklarationLesen();
        if (!fehler) {
            if (wortzeichenLänge[klasseWortzeichen] != nameGröße - 5) fehlschlagWert("class name must match file name");
            for (int Zahl = 0; Zahl < nameGröße - 5; Zahl++) if (Quelltext[wortzeichenPosition[klasseWortzeichen] + Zahl] != dateiNameText[Zahl]) fehlschlagWert("class name must match file name");
        }
        for (aktuellMethode = 0; aktuellMethode < methodeAnzahl && !fehler; aktuellMethode++) {
            position = methodeRumpf[aktuellMethode]; methodeKode[aktuellMethode] = kodeGröße; lokalAnzahl = 0; tiefeWert = 0;
            for (int Zahl = 0; Zahl < methodeArgumentAnzahl[aktuellMethode]; Zahl++) lokalHinzufügen(methodeArgumentName[aktuellMethode * 16 + Zahl], methodeArgumentTyp[aktuellMethode * 16 + Zahl]);
            boolean zurückkehrenErgebnis = anweisungWert();
            if (!zurückkehrenErgebnis && methodeZurückkehren[aktuellMethode] != 0) fehlschlagWert("missing return");
            // Der Zusammenführungspunkt nach einem Sprung muss eine tatsächliche Anweisung sein (Prüfer der Version 49).
            if (methodeZurückkehren[aktuellMethode] == 0) wertAusgeben(177);
            else { boolean Ganzzahl = methodeZurückkehren[aktuellMethode] <= 2 || methodeZurückkehren[aktuellMethode] == 5; wertAusgeben(Ganzzahl ? 3 : 1); wertAusgeben(Ganzzahl ? 172 : 176); }
            if (position != methodeEnde[aktuellMethode]) fehlschlagWert("invalid method body");
            methodeLokalvariablen[aktuellMethode] = lokalAnzahl; methodeLänge[aktuellMethode] = kodeGröße - methodeKode[aktuellMethode];
        }
        if (fehler) return 1;
        klasseSchreiben(); if (fehler) return 1;
        dateiNameText[nameGröße - 4] = 'c'; dateiNameText[nameGröße - 3] = 'l'; dateiNameText[nameGröße - 2] = 'a';
        dateiNameText[nameGröße - 1] = 's'; dateiNameText[nameGröße] = 's'; dateiNameText[nameGröße + 1] = 0;
        int ergebnis = Benutzer.dateiSchreiben(dateiNameText, Ausgabe, ausgabeGröße);
        if (ergebnis < 0) { Benutzer.schreiben("javac: cannot save class: "); JavaWerkzeug.nummerSchreiben(ergebnis); Benutzer.zeichenWertSchreiben(10); return 1; }
        Benutzer.schreiben("Compiled: "); for (int Zahl = 0; dateiNameText[Zahl] != 0; Zahl++) Benutzer.zeichenWertSchreiben(dateiNameText[Zahl]);
        Benutzer.schreiben(" (JVM class version 49)\n"); return 0;
    }
}
