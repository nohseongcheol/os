// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Eingeschränkte JVM auf ARM64 EL0. Prüft Datei-, Stapel-, Referenz- und Sprunggrenzen zur Laufzeit. */
public final class VirtuelleJavaMaschine {
    static int[] Datei = new int[16 * 16384], vorläufigDatei = new int[16384], dateiNameText = new int[512];
    static int[] konstanteKennzeichen = new int[8192], konstanteErsterWert = new int[8192], konstanteZweiterWert = new int[8192], zeichenketteVerweis = new int[8192];
    static int[] methodeNameText = new int[512], methodeTyp = new int[512], methodeZugriff = new int[512], methodeEigentümer = new int[512];
    static int[] methodeStarten = new int[512], methodeEnde = new int[512], methodeStapel = new int[512], methodeLokalvariablen = new int[512];
    static int[] methodeArgumentAnzahl = new int[512], methodeArgumentTyp = new int[8192], methodeZurückkehren = new int[512];
    static int[] grenzstelleWert = new int[16 * 16384];
    static int[] lokalWert = new int[16384], lokalTyp = new int[16384], operandStapelWert = new int[16384], operandStapelTyp = new int[16384];
    static int[] rahmenMethode = new int[128], rahmenPosition = new int[128], rahmenStapel = new int[128], rahmenBefehlswort = new int[128], rahmenInitialisieren = new int[128];
    static int[] klasseDefinitionName = new int[16], klasseDefinitionGröße = new int[16], klasseDefinitionElternknoten = new int[16], klasseDefinitionStatuswert = new int[16], klassePlatzAnzahl = new int[16], klasseDefinitionInitialisieren = new int[16];
    static int[] klasseSchnittstelle = new int[16 * 16], klasseSchnittstelleAnzahl = new int[16];
    static int[] platzName = new int[512], platzTyp = new int[512], platzEigentümer = new int[512], platzErlaubnisse = new int[512], platzPosition = new int[512], platzDaten = new int[512];
    static int[] startenAbfangen = new int[1024], endeAbfangen = new int[1024], positionAbfangen = new int[1024], klasseAbfangen = new int[1024], methodeAbfangen = new int[1024];
    static int[] speicherhaldeWert = new int[32768], speicherhaldeBreite = new int[32768], speicherhaldeMerkzeichen = new int[32768], speicherhaldeVerweis = new int[32768], fürDarstellenWarten = new int[32768];
    static int[] vorläufigVerweis = new int[256], datenfeldElement = new int[32768], ablegenDatenGanzzahl = new int[256];
    static int größe, positionLesen, methodeAnzahl, klasseName, rahmenIndex = -1, speicherhaldeEndePosition = 1, zurückkehrenTyp;
    static int klasseDefinitionAnzahl, platzAnzahl, anzahlAbfangen, aktuellAnalysiertKlasse, ausgelöstObjekt, vorläufigAnzahl, darstellenAnzahl, sammlungAnzahl;
    static int aktuellAusführungsfaden, ausführungsfadenAnzahl = 1, eintragKlasseDefinition;
    static int[] ausführungsfadenRahmen = new int[4], ausführungsfadenStatuswert = new int[4], ausführungsfadenObjekt = new int[4], ausführungsfadenZielobjekt = new int[4], fürAusführungsfadenWarten = new int[4];
    static boolean fehler, anfrageÄndern;
    static int[] sperreEigentümer = new int[32768], sperreTiefe = new int[32768], rahmenSperre = new int[128], klasseSperre = new int[16], klasseAusführungsfaden = new int[16];

    static void fehlschlagWert(String maschinenwortText) {
        if (fehler) return;
        int kategorieKode = 0;
        if (JavaWerkzeug.gleichText(maschinenwortText, "ArithmeticException: / by zero")) kategorieKode = 4;
        if (JavaWerkzeug.gleichText(maschinenwortText, "NullPointerException") || JavaWerkzeug.gleichText(maschinenwortText, "null or invalid array")) kategorieKode = 5;
        if (JavaWerkzeug.gleichText(maschinenwortText, "ArrayIndexOutOfBoundsException")) kategorieKode = 7;
        if (JavaWerkzeug.gleichText(maschinenwortText, "StringIndexOutOfBoundsException")) kategorieKode = 8;
        if (JavaWerkzeug.gleichText(maschinenwortText, "NumberFormatException")) kategorieKode = 10;
        if (JavaWerkzeug.gleichText(maschinenwortText, "FileNotFoundException: file open failed")) kategorieKode = 12;
        if (JavaWerkzeug.gleichText(maschinenwortText, "IOException: stream closed") || JavaWerkzeug.gleichText(maschinenwortText, "IOException: read failed") || JavaWerkzeug.gleichText(maschinenwortText, "IOException: write failed")) kategorieKode = 11;
        if (JavaWerkzeug.gleichText(maschinenwortText, "ClassCastException")) kategorieKode = 14;
        if (JavaWerkzeug.gleichText(maschinenwortText, "NegativeArraySizeException")) kategorieKode = 15;
        if (kategorieKode != 0 && rahmenIndex >= 0) { ausnahmeAuslösen(kategorieKode, maschinenwortText); return; }
        Benutzer.schreiben("JVM error: "); Benutzer.schreiben(maschinenwortText); Benutzer.zeichenWertSchreiben(10); fehler = true;
    }
    static boolean beschneiden(int ausführenVorgang, int Länge) {
        if (ausführenVorgang < 0 || ausführenVorgang >= Datei.length || Länge < 0) return false;
        int klasseDefinition = ausführenVorgang / 16384;
        return ausführenVorgang % 16384 <= klasseDefinitionGröße[klasseDefinition] && Länge <= klasseDefinitionGröße[klasseDefinition] - ausführenVorgang % 16384;
    }
    static int byteWert() {
        if (!beschneiden(positionLesen, 1)) { fehlschlagWert("truncated class file"); return 0; }
        return Datei[positionLesen++];
    }
    static int kurzWert() { return byteWert() << 8 | byteWert(); }
    static int Ganzzahl() { return kurzWert() << 16 | kurzWert(); }
    static void bytesÜberspringen(int Länge) { if (!beschneiden(positionLesen, Länge)) fehlschlagWert("invalid attribute size"); else positionLesen += Länge; }
    static boolean konstantePrüfen(int Zahl, int artWert) {
        if (Zahl <= 0 || Zahl >= konstanteKennzeichen.length || konstanteKennzeichen[Zahl] != artWert) { fehlschlagWert("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean textBereich(int ausführenVorgang, int Länge, String maschinenwortText) {
        if (!beschneiden(ausführenVorgang, Länge)) return false;
        int mauszeigerLesen = ausführenVorgang, endung = ausführenVorgang + Länge;
        for (int schleifeIndex = 0; schleifeIndex < maschinenwortText.length(); schleifeIndex++) {
            int zeichenKode = maschinenwortText.charAt(schleifeIndex);
            if (zeichenKode > 0 && zeichenKode < 128) { if (mauszeigerLesen >= endung || Datei[mauszeigerLesen++] != zeichenKode) return false; }
            else if (zeichenKode < 2048) {
                if (mauszeigerLesen + 2 > endung || Datei[mauszeigerLesen++] != (192 | (zeichenKode >> 6)) || Datei[mauszeigerLesen++] != (128 | (zeichenKode & 63))) return false;
            } else if (mauszeigerLesen + 3 > endung || Datei[mauszeigerLesen++] != (224 | (zeichenKode >> 12)) || Datei[mauszeigerLesen++] != (128 | ((zeichenKode >> 6) & 63)) || Datei[mauszeigerLesen++] != (128 | (zeichenKode & 63))) return false;
        }
        return mauszeigerLesen == endung;
    }
    static boolean maschinenwortText(int konstanteWert, String maschinenwortText) { return konstantePrüfen(konstanteWert, 1) && textBereich(konstanteErsterWert[konstanteWert], konstanteZweiterWert[konstanteWert], maschinenwortText); }
    static boolean passendMaschinenwort(int ersterOperand, int zweiterOperand) {
        if (!konstantePrüfen(ersterOperand, 1) || !konstantePrüfen(zweiterOperand, 1) || konstanteZweiterWert[ersterOperand] != konstanteZweiterWert[zweiterOperand]) return false;
        for (int Zahl = 0; Zahl < konstanteZweiterWert[ersterOperand]; Zahl++) if (Datei[konstanteErsterWert[ersterOperand] + Zahl] != Datei[konstanteErsterWert[zweiterOperand] + Zahl]) return false;
        return true;
    }
    static int klasseNameText(int Zahl) { return konstantePrüfen(Zahl, 7) && konstantePrüfen(konstanteErsterWert[Zahl], 1) ? konstanteErsterWert[Zahl] : 0; }
    static int verweisName(int Zahl) { return konstantePrüfen(Zahl, 12) && konstantePrüfen(konstanteErsterWert[Zahl], 1) ? konstanteErsterWert[Zahl] : 0; }
    static int verweisTyp(int Zahl) { return konstantePrüfen(Zahl, 12) && konstantePrüfen(konstanteZweiterWert[Zahl], 1) ? konstanteZweiterWert[Zahl] : 0; }
    static int deskriptorTyp(int endung, boolean leerwertTyp) {
        if (positionLesen >= endung) { fehlschlagWert("invalid descriptor"); return 0; }
        int Wert = byteWert();
        if (Wert == 'V' && leerwertTyp) return 0;
        if (Wert == 'I' || Wert == 'B' || Wert == 'C' || Wert == 'S' || Wert == 'Z') return 1;
        if (Wert == '[') { deskriptorTyp(endung, false); return 2; }
        if (Wert == 'L') {
            int ausführenVorgang = positionLesen;
            while (positionLesen < endung && Datei[positionLesen] != ';') positionLesen++;
            if (positionLesen == endung || positionLesen == ausführenVorgang) fehlschlagWert("invalid reference descriptor");
            else positionLesen++;
            return 2;
        }
        fehlschlagWert("unsupported descriptor type"); return 0;
    }
    static void deskriptorLesen(int Funktion) {
        int vorherigElementeintrag = positionLesen, Zahl = methodeTyp[Funktion];
        if (!konstantePrüfen(Zahl, 1)) return;
        positionLesen = konstanteErsterWert[Zahl]; int endung = positionLesen + konstanteZweiterWert[Zahl];
        if (byteWert() != '(') fehlschlagWert("invalid method descriptor");
        int elementeintragAnzahl = 0;
        while (!fehler && positionLesen < endung && Datei[positionLesen] != ')') {
            if (elementeintragAnzahl == 16) { fehlschlagWert("too many method arguments"); break; }
            methodeArgumentTyp[Funktion * 16 + elementeintragAnzahl++] = deskriptorTyp(endung, false);
        }
        if (positionLesen >= endung || byteWert() != ')') fehlschlagWert("invalid method descriptor");
        methodeZurückkehren[Funktion] = deskriptorTyp(endung, true); methodeArgumentAnzahl[Funktion] = elementeintragAnzahl;
        if (positionLesen != endung) fehlschlagWert("invalid method descriptor");
        positionLesen = vorherigElementeintrag;
    }
    static int konstanteIndexLesen() { int Wert = kurzWert(); return Wert == 0 ? 0 : aktuellAnalysiertKlasse * 512 + Wert; }
    static int befehlscodeKonstanteLesen() { return methodeEigentümer[rahmenMethode[rahmenIndex]] * 512 + befehlscodeKurzLesen(); }
    static void attributÜberspringen() {
        int elementeintragAnzahl = kurzWert();
        for (int Zahl = 0; Zahl < elementeintragAnzahl && !fehler; Zahl++) { konstantePrüfen(konstanteIndexLesen(), 1); bytesÜberspringen(Ganzzahl()); }
    }
    static int befehlLänge(int Wert) {
        if (Wert == 16 || Wert == 18 || Wert == 21 || Wert == 25 || Wert == 54 || Wert == 58 || Wert == 188) return 2;
        if (Wert == 17 || Wert == 19 || Wert == 132 || Wert >= 153 && Wert <= 167
            || Wert >= 178 && Wert <= 184 || Wert == 187 || Wert == 189 || Wert == 192 || Wert == 193 || Wert == 198 || Wert == 199) return 3;
        if (Wert == 185 || Wert == 200) return 5;
        if (Wert >= 0 && Wert <= 8 || Wert >= 26 && Wert <= 29 || Wert >= 42 && Wert <= 46 || Wert >= 50 && Wert <= 53
            || Wert >= 59 && Wert <= 62 || Wert >= 75 && Wert <= 79 || Wert >= 83 && Wert <= 95
            || Wert == 96 || Wert == 100 || Wert == 104 || Wert == 108 || Wert == 112 || Wert == 116
            || Wert == 120 || Wert == 122 || Wert == 124 || Wert == 126 || Wert == 128 || Wert == 130
            || Wert >= 145 && Wert <= 147 || Wert == 172 || Wert == 176 || Wert == 177 || Wert == 190 || Wert == 191
            || Wert == 194 || Wert == 195) return 1;
        return 0;
    }
    static int positionGanzzahl(int mauszeigerLesen) {
        if (!beschneiden(mauszeigerLesen, 4)) { fehlschlagWert("truncated bytecode operand"); return 0; }
        return Datei[mauszeigerLesen] << 24 | Datei[mauszeigerLesen + 1] << 16 | Datei[mauszeigerLesen + 2] << 8 | Datei[mauszeigerLesen + 3];
    }
    static int längeLesen(int mauszeigerLesen, int ausführenVorgang, int endung) {
        int Wert = Datei[mauszeigerLesen], Länge = befehlLänge(Wert);
        if (Wert == 170 || Wert == 171) {
            int basisPosition = mauszeigerLesen + 1;
            while ((basisPosition - ausführenVorgang) % 4 != 0) basisPosition++;
            if (endung - basisPosition < (Wert == 170 ? 12 : 8)) return 0;
            int eintragAnzahl = Wert == 170 ? positionGanzzahl(basisPosition + 8) - positionGanzzahl(basisPosition + 4) + 1 : positionGanzzahl(basisPosition + 4);
            if (eintragAnzahl < 0 || eintragAnzahl > 2048) return 0;
            Länge = basisPosition - mauszeigerLesen + (Wert == 170 ? 12 + 4 * eintragAnzahl : 8 + 8 * eintragAnzahl);
        }
        if (Wert == 196 && mauszeigerLesen + 1 < endung) {
            int maschinenwortDaten = Datei[mauszeigerLesen + 1]; Länge = maschinenwortDaten == 132 ? 6 : (maschinenwortDaten == 21 || maschinenwortDaten == 25 || maschinenwortDaten == 54 || maschinenwortDaten == 58) ? 4 : 0;
        }
        return Länge > 0 && Länge <= endung - mauszeigerLesen ? Länge : 0;
    }
    static void zielWertPrüfen(int zielWert, int Funktion) {
        if (zielWert < methodeStarten[Funktion] || zielWert >= methodeEnde[Funktion] || grenzstelleWert[zielWert] != Funktion + 1) fehlschlagWert("invalid branch target");
    }
    static void klasseLesen(int klasseDefinition) {
        aktuellAnalysiertKlasse = klasseDefinition; positionLesen = klasseDefinition * 16384; größe = positionLesen + klasseDefinitionGröße[klasseDefinition];
        if (Ganzzahl() != 0xcafebabe) { fehlschlagWert("not a class file"); return; }
        int nebenversionÜberarbeitung = kurzWert(), versionWert = kurzWert();
        if (versionWert < 45 || versionWert > 52 || nebenversionÜberarbeitung != 0) { fehlschlagWert("supported class versions: 45..52, minor 0"); return; }
        int konstanteAnzahl = kurzWert(), basisPosition = klasseDefinition * 512;
        if (konstanteAnzahl < 1 || konstanteAnzahl > 512) { fehlschlagWert("constant pool limit (511)"); return; }
        for (int eintragAnzahl = 1; eintragAnzahl < konstanteAnzahl && !fehler; eintragAnzahl++) {
            int Zahl = basisPosition + eintragAnzahl, artWert = byteWert(); konstanteKennzeichen[Zahl] = artWert;
            if (artWert == 1) { konstanteZweiterWert[Zahl] = kurzWert(); konstanteErsterWert[Zahl] = positionLesen; bytesÜberspringen(konstanteZweiterWert[Zahl]); }
            else if (artWert == 3) konstanteErsterWert[Zahl] = Ganzzahl();
            else if (artWert == 7 || artWert == 8) konstanteErsterWert[Zahl] = konstanteIndexLesen();
            else if (artWert == 9 || artWert == 10 || artWert == 11 || artWert == 12) { konstanteErsterWert[Zahl] = konstanteIndexLesen(); konstanteZweiterWert[Zahl] = konstanteIndexLesen(); }
            else fehlschlagWert("unsupported constant type");
        }
        int erlaubnisWert = kurzWert();
        if ((erlaubnisWert & (0x2000 | 0x4000)) != 0) fehlschlagWert("annotation/enum class unsupported");
        klasseDefinitionName[klasseDefinition] = klasseNameText(konstanteIndexLesen());
        klasseDefinitionElternknoten[klasseDefinition] = klasseNameText(konstanteIndexLesen());
        int schnittstelleAnzahl = kurzWert(); if (schnittstelleAnzahl > 16) { fehlschlagWert("interface count limit"); return; }
        klasseSchnittstelleAnzahl[klasseDefinition] = schnittstelleAnzahl;
        for (int schleifeIndex = 0; schleifeIndex < schnittstelleAnzahl; schleifeIndex++) klasseSchnittstelle[klasseDefinition * 16 + schleifeIndex] = klasseNameText(konstanteIndexLesen());
        int feldAnzahl = kurzWert();
        if (feldAnzahl > 512 - platzAnzahl) { fehlschlagWert("field count limit (512)"); return; }
        for (int schleifeIndex = 0; schleifeIndex < feldAnzahl && !fehler; schleifeIndex++) {
            int dateiIndex = platzAnzahl++; platzEigentümer[dateiIndex] = klasseDefinition; platzErlaubnisse[dateiIndex] = kurzWert(); platzName[dateiIndex] = konstanteIndexLesen(); platzTyp[dateiIndex] = konstanteIndexLesen();
            konstantePrüfen(platzName[dateiIndex], 1); konstantePrüfen(platzTyp[dateiIndex], 1);
            int bewahrtWert = positionLesen; positionLesen = konstanteErsterWert[platzTyp[dateiIndex]]; int kategorieKode = deskriptorTyp(positionLesen + konstanteZweiterWert[platzTyp[dateiIndex]], false); positionLesen = bewahrtWert;
            if ((platzErlaubnisse[dateiIndex] & 8) == 0) platzPosition[dateiIndex] = klassePlatzAnzahl[klasseDefinition]++;
            int attributDaten = kurzWert();
            for (int innerlichPosition = 0; innerlichPosition < attributDaten && !fehler; innerlichPosition++) {
                int nameKonstante = konstanteIndexLesen(), gültigLänge = Ganzzahl();
                if (maschinenwortText(nameKonstante, "ConstantValue") && gültigLänge == 2) {
                    int datenWert = konstanteIndexLesen();
                    if (kategorieKode == 1 && konstantePrüfen(datenWert, 3)) platzDaten[dateiIndex] = konstanteErsterWert[datenWert];
                    else if (kategorieKode == 2 && konstantePrüfen(datenWert, 8)) platzDaten[dateiIndex] = konstanteText(konstanteErsterWert[datenWert]);
                } else bytesÜberspringen(gültigLänge);
            }
        }
        int elementeintragAnzahl = kurzWert();
        if (elementeintragAnzahl > 512 - methodeAnzahl) { fehlschlagWert("method count limit (512)"); return; }
        for (int schleifeIndex = 0; schleifeIndex < elementeintragAnzahl && !fehler; schleifeIndex++) {
            int Zahl = methodeAnzahl++; methodeEigentümer[Zahl] = klasseDefinition;
            methodeZugriff[Zahl] = kurzWert(); methodeNameText[Zahl] = konstanteIndexLesen(); methodeTyp[Zahl] = konstanteIndexLesen();
            konstantePrüfen(methodeNameText[Zahl], 1); deskriptorLesen(Zahl);
            if ((methodeZugriff[Zahl] & 8) == 0) {
                if (methodeArgumentAnzahl[Zahl] == 16) { fehlschlagWert("too many instance method arguments"); return; }
                for (int vergleichPosition = methodeArgumentAnzahl[Zahl]; vergleichPosition > 0; vergleichPosition--) methodeArgumentTyp[Zahl * 16 + vergleichPosition] = methodeArgumentTyp[Zahl * 16 + vergleichPosition - 1];
                methodeArgumentTyp[Zahl * 16] = 2; methodeArgumentAnzahl[Zahl]++;
            }
            if ((methodeZugriff[Zahl] & 0x100) != 0) fehlschlagWert("user native method unsupported");
            if (maschinenwortText(methodeNameText[Zahl], "<clinit>")) klasseDefinitionInitialisieren[klasseDefinition] = Zahl + 1;
            for (int vorderseiteWert = 0; vorderseiteWert < Zahl; vorderseiteWert++) if (methodeEigentümer[vorderseiteWert] == klasseDefinition && passendMaschinenwort(methodeNameText[vorderseiteWert], methodeNameText[Zahl]) && passendMaschinenwort(methodeTyp[vorderseiteWert], methodeTyp[Zahl])) fehlschlagWert("duplicate method");
            int attributAnzahl = kurzWert();
            for (int attributWert = 0; attributWert < attributAnzahl && !fehler; attributWert++) {
                int Name = konstanteIndexLesen(), Länge = Ganzzahl(), ausführenVorgang = positionLesen;
                if (!beschneiden(ausführenVorgang, Länge)) { fehlschlagWert("truncated method attribute"); break; }
                if (maschinenwortText(Name, "Code")) {
                    if (methodeStarten[Zahl] != 0) fehlschlagWert("duplicate Code attribute");
                    methodeStapel[Zahl] = kurzWert(); methodeLokalvariablen[Zahl] = kurzWert(); int kodeLänge = Ganzzahl();
                    if (methodeStapel[Zahl] > 128 || methodeLokalvariablen[Zahl] > 128 || methodeLokalvariablen[Zahl] < methodeArgumentAnzahl[Zahl]
                        || kodeLänge < 1 || kodeLänge > 8192) fehlschlagWert("method memory limits exceeded");
                    methodeStarten[Zahl] = positionLesen; bytesÜberspringen(kodeLänge); methodeEnde[Zahl] = positionLesen;
                    int abfangendAnzahl = kurzWert();
                    if (abfangendAnzahl > 1024 - anzahlAbfangen) { fehlschlagWert("exception table limit"); return; }
                    for (int innerlichPosition = 0; innerlichPosition < abfangendAnzahl; innerlichPosition++) {
                        int fehlerVerweis = anzahlAbfangen++; methodeAbfangen[fehlerVerweis] = Zahl;
                        startenAbfangen[fehlerVerweis] = methodeStarten[Zahl] + kurzWert(); endeAbfangen[fehlerVerweis] = methodeStarten[Zahl] + kurzWert();
                        positionAbfangen[fehlerVerweis] = methodeStarten[Zahl] + kurzWert(); int kodiertWert = konstanteIndexLesen(); klasseAbfangen[fehlerVerweis] = kodiertWert == 0 ? 0 : klasseNameText(kodiertWert);
                    }
                    attributÜberspringen();
                    if (positionLesen != ausführenVorgang + Länge) fehlschlagWert("Code attribute size mismatch");
                } else bytesÜberspringen(Länge);
            }
            if ((methodeZugriff[Zahl] & 0x400) != 0) continue;
            if (methodeStarten[Zahl] == 0) fehlschlagWert("missing Code attribute");
            int platzEintrag = methodeStarten[Zahl];
            while (platzEintrag < methodeEnde[Zahl] && !fehler) {
                int Länge = längeLesen(platzEintrag, methodeStarten[Zahl], methodeEnde[Zahl]);
                if (Länge == 0) { fehlschlagWert("unsupported or truncated bytecode"); break; }
                grenzstelleWert[platzEintrag] = Zahl + 1; platzEintrag += Länge;
            }
            platzEintrag = methodeStarten[Zahl];
            while (platzEintrag < methodeEnde[Zahl] && !fehler) {
                int Wert = Datei[platzEintrag];
                if (Wert >= 153 && Wert <= 167 || Wert == 198 || Wert == 199) zielWertPrüfen(platzEintrag + (short)(Datei[platzEintrag + 1] << 8 | Datei[platzEintrag + 2]), Zahl);
                if (Wert == 200) zielWertPrüfen(platzEintrag + positionGanzzahl(platzEintrag + 1), Zahl);
                if (Wert == 170 || Wert == 171) {
                    int mauszeigerLesen = platzEintrag + 1; while ((mauszeigerLesen - methodeStarten[Zahl]) % 4 != 0) mauszeigerLesen++;
                    zielWertPrüfen(platzEintrag + positionGanzzahl(mauszeigerLesen), Zahl);
                    int eintragAnzahl = Wert == 170 ? positionGanzzahl(mauszeigerLesen + 8) - positionGanzzahl(mauszeigerLesen + 4) + 1 : positionGanzzahl(mauszeigerLesen + 4);
                    mauszeigerLesen += Wert == 170 ? 12 : 8;
                    for (int innerlichPosition = 0; innerlichPosition < eintragAnzahl; innerlichPosition++) zielWertPrüfen(platzEintrag + positionGanzzahl(mauszeigerLesen + innerlichPosition * (Wert == 170 ? 4 : 8) + (Wert == 170 ? 0 : 4)), Zahl);
                }
                platzEintrag += längeLesen(platzEintrag, methodeStarten[Zahl], methodeEnde[Zahl]);
            }
            for (int innerlichPosition = 0; innerlichPosition < anzahlAbfangen; innerlichPosition++) if (methodeAbfangen[innerlichPosition] == Zahl) {
                zielWertPrüfen(startenAbfangen[innerlichPosition], Zahl); zielWertPrüfen(positionAbfangen[innerlichPosition], Zahl);
                if (endeAbfangen[innerlichPosition] != methodeEnde[Zahl]) zielWertPrüfen(endeAbfangen[innerlichPosition], Zahl);
                if (startenAbfangen[innerlichPosition] >= endeAbfangen[innerlichPosition]) fehlschlagWert("invalid exception range");
            }
        }
        if (!fehler) attributÜberspringen();
        if (positionLesen != größe) fehlschlagWert("extra class file data");
    }
    static int speichergerätZuteilen(int artWert, int Länge) { return neuSpeicher(artWert, Länge); }
    static boolean objektWert(int verweis, int artWert) {
        if (!istGültigObjekt(verweis)) return false;
        if (speicherhaldeWert[verweis] != artWert) { fehlschlagWert("object type mismatch"); return false; }
        return true;
    }
    static int konstanteText(int Nummer) {
        if (!konstantePrüfen(Nummer, 1)) return 0;
        if (zeichenketteVerweis[Nummer] != 0) return zeichenketteVerweis[Nummer];
        int verweis = speichergerätZuteilen(1, konstanteZweiterWert[Nummer]); if (fehler) return 0;
        int endung = konstanteErsterWert[Nummer] + konstanteZweiterWert[Nummer], Zahl = konstanteErsterWert[Nummer], Länge = 0;
        while (Zahl < endung && !fehler) {
            int Wert = Datei[Zahl++];
            if (Wert == 0) fehlschlagWert("invalid modified UTF-8");
            else if (Wert >= 192 && Wert <= 223 && Zahl < endung) {
                int nächsterElementeintrag = Datei[Zahl++];
                if ((nächsterElementeintrag & 192) != 128) fehlschlagWert("invalid modified UTF-8");
                Wert = (Wert & 31) << 6 | nächsterElementeintrag & 63;
                if (Wert != 0 && Wert < 128) fehlschlagWert("overlong modified UTF-8");
            } else if (Wert >= 224 && Wert <= 239 && Zahl + 1 < endung) {
                int ersterOperand = Datei[Zahl++], zweiterOperand = Datei[Zahl++];
                if ((ersterOperand & 192) != 128 || (zweiterOperand & 192) != 128) fehlschlagWert("invalid modified UTF-8");
                Wert = (Wert & 15) << 12 | (ersterOperand & 63) << 6 | zweiterOperand & 63;
                if (Wert < 2048) fehlschlagWert("overlong modified UTF-8");
            } else if (Wert >= 128) fehlschlagWert("invalid modified UTF-8");
            speicherhaldeWert[verweis + 2 + Länge++] = Wert;
        }
        speicherhaldeWert[verweis + 1] = Länge; zeichenketteVerweis[Nummer] = verweis; return verweis;
    }
    static int wirtssystemZeichen(String Wert) {
        int verweis = speichergerätZuteilen(1, Wert.length()); if (fehler) return 0;
        for (int Zahl = 0; Zahl < Wert.length(); Zahl++) speicherhaldeWert[verweis + 2 + Zahl] = Wert.charAt(Zahl);
        return verweis;
    }
    static void textSchreiben(int verweis) {
        if (verweis == 0) { Benutzer.schreiben("null"); return; }
        if (!objektWert(verweis, 1)) return;
        for (int Zahl = 0; Zahl < speicherhaldeWert[verweis + 1]; Zahl++) Benutzer.zeichenWertSchreiben(speicherhaldeWert[verweis + 2 + Zahl]);
    }
    static int zifferZeichen(int Wert) {
        int verweis = speichergerätZuteilen(1, 11); if (fehler) return 0;
        int Länge = 0;
        if (Wert < 0) speicherhaldeWert[verweis + 2 + Länge++] = '-'; else Wert = -Wert;
        int positionIndex = 1000000000; boolean ausführenVorgang = false;
        while (positionIndex != 0) {
            int Zahl = -(Wert / positionIndex);
            if (Zahl != 0 || ausführenVorgang || positionIndex == 1) { speicherhaldeWert[verweis + 2 + Länge++] = '0' + Zahl; ausführenVorgang = true; }
            Wert %= positionIndex; positionIndex /= 10;
        }
        speicherhaldeWert[verweis + 1] = Länge; return verweis;
    }
    static int ganzzahlDekodieren(int verweis) {
        if (!objektWert(verweis, 1)) return 0;
        int Länge = speicherhaldeWert[verweis + 1], Zahl = 0, Wert = 0; boolean negativWert = false;
        if (Länge > 0 && (speicherhaldeWert[verweis + 2] == '-' || speicherhaldeWert[verweis + 2] == '+')) { negativWert = speicherhaldeWert[verweis + 2] == '-'; Zahl++; }
        if (Zahl == Länge) fehlschlagWert("NumberFormatException");
        for (; Zahl < Länge && !fehler; Zahl++) {
            int zifferWert = speicherhaldeWert[verweis + 2 + Zahl] - '0';
            if (zifferWert < 0 || zifferWert > 9 || Wert < -214748364 || Wert == -214748364 && zifferWert > (negativWert ? 8 : 7)) fehlschlagWert("NumberFormatException");
            Wert = Wert * 10 - zifferWert;
        }
        return negativWert ? Wert : -Wert;
    }
    static void wertAblegen(int Wert, int typWert) {
        if (fehler) return;
        if (rahmenIndex < 0 || rahmenStapel[rahmenIndex] >= methodeStapel[rahmenMethode[rahmenIndex]]) { fehlschlagWert("operand stack overflow"); return; }
        int platzEintrag = rahmenIndex * 128 + rahmenStapel[rahmenIndex]++; operandStapelWert[platzEintrag] = Wert; operandStapelTyp[platzEintrag] = typWert;
    }
    static int werteSubtrahieren(int typWert) {
        if (fehler) return 0;
        if (rahmenIndex < 0 || rahmenStapel[rahmenIndex] < 1) { fehlschlagWert("operand stack underflow"); return 0; }
        int platzEintrag = rahmenIndex * 128 + --rahmenStapel[rahmenIndex]; zurückkehrenTyp = operandStapelTyp[platzEintrag];
        if (typWert != 0 && zurückkehrenTyp != typWert) fehlschlagWert("operand type mismatch");
        if (zurückkehrenTyp == 2) wertSchützen(operandStapelWert[platzEintrag]);
        return operandStapelWert[platzEintrag];
    }
    static void lokalLesen(int Nummer, int typWert) {
        if (Nummer >= methodeLokalvariablen[rahmenMethode[rahmenIndex]] || Nummer < 0 || lokalTyp[rahmenIndex * 128 + Nummer] != typWert) { fehlschlagWert("invalid or uninitialized local"); return; }
        wertAblegen(lokalWert[rahmenIndex * 128 + Nummer], typWert);
    }
    static void lokalSchreiben(int Nummer, int typWert) {
        if (Nummer >= methodeLokalvariablen[rahmenMethode[rahmenIndex]] || Nummer < 0) { fehlschlagWert("local index out of range"); return; }
        int Wert = werteSubtrahieren(typWert); lokalWert[rahmenIndex * 128 + Nummer] = Wert; lokalTyp[rahmenIndex * 128 + Nummer] = typWert;
    }
    static int befehlscodeByteLesen() {
        int position = rahmenPosition[rahmenIndex];
        if (position < methodeStarten[rahmenMethode[rahmenIndex]] || position >= methodeEnde[rahmenMethode[rahmenIndex]]) { fehlschlagWert("instruction pointer out of range"); return 0; }
        rahmenPosition[rahmenIndex]++; return Datei[position];
    }
    static int befehlscodeKurzLesen() { return befehlscodeByteLesen() << 8 | befehlscodeByteLesen(); }
    static void bewegenWert(int position) {
        int Funktion = rahmenMethode[rahmenIndex];
        if (position < methodeStarten[Funktion] || position >= methodeEnde[Funktion] || grenzstelleWert[position] != Funktion + 1) fehlschlagWert("invalid branch target");
        else rahmenPosition[rahmenIndex] = position;
    }
    static void aufrufen(int Funktion) {
        if (rahmenIndex % 32 == 31) { fehlschlagWert("call stack limit (32)"); return; }
        int nächsterElementeintrag = rahmenIndex + 1;
        for (int Zahl = 0; Zahl < 128; Zahl++) lokalTyp[nächsterElementeintrag * 128 + Zahl] = 0;
        for (int Zahl = methodeArgumentAnzahl[Funktion] - 1; Zahl >= 0; Zahl--) {
            lokalWert[nächsterElementeintrag * 128 + Zahl] = werteSubtrahieren(methodeArgumentTyp[Funktion * 16 + Zahl]); lokalTyp[nächsterElementeintrag * 128 + Zahl] = methodeArgumentTyp[Funktion * 16 + Zahl];
        }
        if (fehler) return;
        rahmenIndex = nächsterElementeintrag; rahmenInitialisieren[rahmenIndex] = 0; rahmenMethode[rahmenIndex] = Funktion; rahmenPosition[rahmenIndex] = methodeStarten[Funktion]; rahmenStapel[rahmenIndex] = 0;
    }
    static void zurückkehrenErgebnis(int typWert) {
        if (typWert != methodeZurückkehren[rahmenMethode[rahmenIndex]]) { fehlschlagWert("return type mismatch"); return; }
        int Wert = typWert == 0 ? 0 : werteSubtrahieren(typWert);
        if (rahmenInitialisieren[rahmenIndex] != 0) klasseDefinitionStatuswert[rahmenInitialisieren[rahmenIndex] - 1] = 2;
        if (rahmenSperre[rahmenIndex] != 0) { sperreFreigeben(rahmenSperre[rahmenIndex]); rahmenSperre[rahmenIndex] = 0; }
        rahmenIndex--; if (rahmenIndex >= aktuellAusführungsfaden * 32 && typWert != 0) wertAblegen(Wert, typWert);
    }
    static int[] datenstromDateiName = new int[64];
    static void dateiDatenstromAufrufVorgang(int eigentümerWert, int Name, int formatWert, int befehl) {
        boolean Ausgabe = maschinenwortText(eigentümerWert, "java/io/FileOutputStream");
        int artWert = Ausgabe ? 6 : 5;
        if (befehl == 183 && maschinenwortText(Name, "<init>")) {
            boolean fortsetzungWert = false;
            if (Ausgabe && maschinenwortText(formatWert, "(Ljava/lang/String;Z)V")) fortsetzungWert = werteSubtrahieren(1) != 0;
            else if (!maschinenwortText(formatWert, "(Ljava/lang/String;)V")) { fehlschlagWert("unsupported file stream constructor"); return; }
            int dateiEintragName = werteSubtrahieren(2), datenstromWert = werteSubtrahieren(2);
            if (!objektWert(dateiEintragName, 1) || !objektWert(datenstromWert, artWert) || fehler) return;
            if (speicherhaldeWert[datenstromWert + 3] != 0) { fehlschlagWert("file stream already initialized"); return; }
            int Länge = speicherhaldeWert[dateiEintragName + 1];
            if (Länge < 1 || Länge > 63) { fehlschlagWert("invalid file name length"); return; }
            for (int platzEintrag = 0; platzEintrag < Länge; platzEintrag++) {
                int Wert = speicherhaldeWert[dateiEintragName + 2 + platzEintrag];
                if (Wert < 1) { fehlschlagWert("invalid file stream path"); return; }
                datenstromDateiName[platzEintrag] = Wert;
            }
            datenstromDateiName[Länge] = 0;
            int deskriptorEintrag = Benutzer.dateiDeskriptorÖffnen(datenstromDateiName, Ausgabe ? (fortsetzungWert ? 1089 : 577) : 0);
            if (deskriptorEintrag < 0) { fehlschlagWert("FileNotFoundException: file open failed"); return; }
            speicherhaldeWert[datenstromWert + 2] = deskriptorEintrag; speicherhaldeWert[datenstromWert + 3] = 1;
            return;
        }
        if (befehl != 182) { fehlschlagWert("invalid file stream invocation"); return; }
        if ((Ausgabe && maschinenwortText(Name, "write") || !Ausgabe && maschinenwortText(Name, "read"))
            && (maschinenwortText(formatWert, Ausgabe ? "([B)V" : "([B)I") || maschinenwortText(formatWert, Ausgabe ? "([BII)V" : "([BII)I"))) {
            boolean beschneidenWert = maschinenwortText(formatWert, Ausgabe ? "([BII)V" : "([BII)I");
            int eintragAnzahl = beschneidenWert ? werteSubtrahieren(1) : 0, beginnendPunkt = beschneidenWert ? werteSubtrahieren(1) : 0, datenDatenfeld = werteSubtrahieren(2), objektVerweis = werteSubtrahieren(2);
            if (!objektWert(datenDatenfeld, 20) || !objektWert(objektVerweis, artWert)) return;
            if (!beschneidenWert) eintragAnzahl = speicherhaldeWert[datenDatenfeld + 1];
            if (beginnendPunkt < 0 || eintragAnzahl < 0 || beginnendPunkt > speicherhaldeWert[datenDatenfeld + 1] - eintragAnzahl) { ausnahmeAuslösen(6, "file buffer bounds"); return; }
            if (speicherhaldeWert[objektVerweis + 3] == 0 || speicherhaldeWert[objektVerweis + 2] < 0) { fehlschlagWert("IOException: stream closed"); return; }
            int abgeschlossenAnzahl = 0;
            while (abgeschlossenAnzahl < eintragAnzahl && !fehler) {
                int zurückgegebenWert = Ausgabe ? Benutzer.einsDateiByteSchreiben(speicherhaldeWert[objektVerweis + 2], speicherhaldeWert[datenDatenfeld + 2 + beginnendPunkt + abgeschlossenAnzahl]) : Benutzer.einsDateiByteLesen(speicherhaldeWert[objektVerweis + 2]);
                if (zurückgegebenWert < 0) { fehlschlagWert(Ausgabe ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!Ausgabe && zurückgegebenWert == 256) break;
                if (!Ausgabe) speicherhaldeWert[datenDatenfeld + 2 + beginnendPunkt + abgeschlossenAnzahl] = (byte)zurückgegebenWert;
                abgeschlossenAnzahl++;
            }
            if (!Ausgabe) wertAblegen(eintragAnzahl != 0 && abgeschlossenAnzahl == 0 ? -1 : abgeschlossenAnzahl, 1);
            return;
        }
        if (Ausgabe && maschinenwortText(Name, "flush") && maschinenwortText(formatWert, "()V")) { int objektVerweis = werteSubtrahieren(2); if (objektWert(objektVerweis, artWert) && speicherhaldeWert[objektVerweis + 2] < 0) fehlschlagWert("IOException: stream closed"); return; }
        int aktion = -1, Wert = 0;
        if (maschinenwortText(Name, "close") && maschinenwortText(formatWert, "()V")) aktion = 0;
        if (!Ausgabe && maschinenwortText(Name, "read") && maschinenwortText(formatWert, "()I")) aktion = 1;
        if (Ausgabe && maschinenwortText(Name, "write") && maschinenwortText(formatWert, "(I)V")) { aktion = 2; Wert = werteSubtrahieren(1); }
        if (aktion < 0) { fehlschlagWert("unsupported file stream method"); return; }
        int datenstromWert = werteSubtrahieren(2);
        if (!objektWert(datenstromWert, artWert) || fehler) return;
        if (speicherhaldeWert[datenstromWert + 3] == 0) { fehlschlagWert("uninitialized file stream"); return; }
        int deskriptorEintrag = speicherhaldeWert[datenstromWert + 2];
        if (aktion == 0) {
            if (deskriptorEintrag >= 0 && Benutzer.dateiDeskriptorSchließen(deskriptorEintrag) < 0) fehlschlagWert("IOException: close failed");
            speicherhaldeWert[datenstromWert + 2] = -1; return;
        }
        if (deskriptorEintrag < 0) { fehlschlagWert("IOException: stream closed"); return; }
        if (aktion == 1) {
            int ergebnis = Benutzer.einsDateiByteLesen(deskriptorEintrag);
            if (ergebnis < -1) fehlschlagWert("IOException: read failed"); else wertAblegen(ergebnis == 256 ? -1 : ergebnis, 1);
        } else if (Benutzer.einsDateiByteSchreiben(deskriptorEintrag, Wert) != 1) fehlschlagWert("IOException: write failed");
    }
    static void methodeAufrufVorgang(int Nummer, int befehl) {
        if (Nummer <= 0 || Nummer >= konstanteKennzeichen.length || (konstanteKennzeichen[Nummer] != 10 && konstanteKennzeichen[Nummer] != 11)) { fehlschlagWert("invalid method reference"); return; }
        int eigentümerWert = klasseNameText(konstanteErsterWert[Nummer]), Name = verweisName(konstanteZweiterWert[Nummer]), formatWert = verweisTyp(konstanteZweiterWert[Nummer]);
        if (fehler) return;
        if (standardwertAufrufen(eigentümerWert, Name, formatWert, befehl)) return;
        if (maschinenwortText(eigentümerWert, "java/io/FileInputStream") || maschinenwortText(eigentümerWert, "java/io/FileOutputStream")) {
            dateiDatenstromAufrufVorgang(eigentümerWert, Name, formatWert, befehl); return;
        }
        if (befehl == 184 && maschinenwortText(eigentümerWert, "java/lang/Integer") && maschinenwortText(Name, "parseInt") && maschinenwortText(formatWert, "(Ljava/lang/String;)I")) {
            wertAblegen(ganzzahlDekodieren(werteSubtrahieren(2)), 1); return;
        }
        if (befehl == 182 && maschinenwortText(eigentümerWert, "java/io/PrintStream") && (maschinenwortText(Name, "println") || maschinenwortText(Name, "print"))) {
            int typWert = 0, Wert = 0;
            if (maschinenwortText(formatWert, "(I)V")) { typWert = 1; Wert = werteSubtrahieren(1); }
            else if (maschinenwortText(formatWert, "(Z)V")) { typWert = 2; Wert = werteSubtrahieren(1); }
            else if (maschinenwortText(formatWert, "(C)V")) { typWert = 3; Wert = werteSubtrahieren(1); }
            else if (maschinenwortText(formatWert, "(Ljava/lang/String;)V")) { typWert = 4; Wert = werteSubtrahieren(2); }
            else if (!maschinenwortText(formatWert, "()V") || !maschinenwortText(Name, "println")) fehlschlagWert("unsupported print descriptor");
            if (werteSubtrahieren(2) != -1) fehlschlagWert("invalid PrintStream receiver");
            if (fehler) return;
            if (typWert == 1) JavaWerkzeug.nummerSchreiben(Wert);
            if (typWert == 2) Benutzer.schreiben(Wert == 0 ? "false" : "true");
            if (typWert == 3) Benutzer.zeichenWertSchreiben(Wert & 65535);
            if (typWert == 4) textSchreiben(Wert);
            if (maschinenwortText(Name, "println")) Benutzer.zeichenWertSchreiben(10);
            return;
        }
        if (befehl == 182 && maschinenwortText(eigentümerWert, "java/lang/String")) {
            if (maschinenwortText(Name, "length") && maschinenwortText(formatWert, "()I")) {
                int verweis = werteSubtrahieren(2); if (objektWert(verweis, 1)) wertAblegen(speicherhaldeWert[verweis + 1], 1); return;
            }
            if (maschinenwortText(Name, "charAt") && maschinenwortText(formatWert, "(I)C")) {
                int feldindexWert = werteSubtrahieren(1), verweis = werteSubtrahieren(2);
                if (objektWert(verweis, 1)) {
                    if (feldindexWert < 0 || feldindexWert >= speicherhaldeWert[verweis + 1]) fehlschlagWert("StringIndexOutOfBoundsException"); else wertAblegen(speicherhaldeWert[verweis + 2 + feldindexWert], 1);
                }
                return;
            }
        }
        if (maschinenwortText(eigentümerWert, "java/lang/StringBuilder")) {
            if (befehl == 183 && maschinenwortText(Name, "<init>") && maschinenwortText(formatWert, "()V")) { objektWert(werteSubtrahieren(2), 4); return; }
            if (befehl == 182 && maschinenwortText(Name, "toString") && maschinenwortText(formatWert, "()Ljava/lang/String;")) {
                int verweis = werteSubtrahieren(2); if (objektWert(verweis, 4)) wertAblegen(speicherhaldeWert[verweis + 2] == 0 ? wirtssystemZeichen("") : speicherhaldeWert[verweis + 2], 2); return;
            }
            if (befehl == 182 && maschinenwortText(Name, "append")) {
                int Text = 0;
                if (maschinenwortText(formatWert, "(I)Ljava/lang/StringBuilder;")) Text = zifferZeichen(werteSubtrahieren(1));
                else if (maschinenwortText(formatWert, "(Z)Ljava/lang/StringBuilder;")) Text = wirtssystemZeichen(werteSubtrahieren(1) == 0 ? "false" : "true");
                else if (maschinenwortText(formatWert, "(C)Ljava/lang/StringBuilder;")) {
                    int Wert = werteSubtrahieren(1); Text = speichergerätZuteilen(1, 1); if (!fehler) speicherhaldeWert[Text + 2] = Wert & 65535;
                }
                else if (maschinenwortText(formatWert, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { Text = werteSubtrahieren(2); if (Text == 0) Text = wirtssystemZeichen("null"); }
                else { fehlschlagWert("unsupported StringBuilder append"); return; }
                int verweis = werteSubtrahieren(2); if (!objektWert(verweis, 4) || !objektWert(Text, 1)) return;
                int vorderseiteWert = speicherhaldeWert[verweis + 2], vorderseiteWertLänge = vorderseiteWert == 0 ? 0 : speicherhaldeWert[vorderseiteWert + 1], rückseiteWertLänge = speicherhaldeWert[Text + 1];
                int neuText = speichergerätZuteilen(1, vorderseiteWertLänge + rückseiteWertLänge); if (fehler) return;
                for (int Zahl = 0; Zahl < vorderseiteWertLänge; Zahl++) speicherhaldeWert[neuText + 2 + Zahl] = speicherhaldeWert[vorderseiteWert + 2 + Zahl];
                for (int Zahl = 0; Zahl < rückseiteWertLänge; Zahl++) speicherhaldeWert[neuText + 2 + vorderseiteWertLänge + Zahl] = speicherhaldeWert[Text + 2 + Zahl];
                speicherhaldeWert[verweis + 2] = neuText; wertAblegen(verweis, 2); return;
            }
        }
        int klasseDefinition = klasseDefinitionFinden(eigentümerWert); if (klasseDefinition < 0 || fehler) return;
        int dateiIndex = methodeFinden(klasseDefinition, Name, formatWert);
        if (dateiIndex < 0) {
            for (int zeichenKode = klasseDefinition, eintragAnzahl = 0; zeichenKode >= 0 && eintragAnzahl < 16; eintragAnzahl++, zeichenKode = elternknotenKlasse(zeichenKode))
                if (maschinenwortText(klasseDefinitionElternknoten[zeichenKode], "java/lang/Thread")) { ausführungsfadenAufrufen(Name, formatWert, befehl); return; }
            fehlschlagWert("NoSuchMethodError"); return;
        }
        if (((methodeZugriff[dateiIndex] & 8) != 0) != (befehl == 184)) { fehlschlagWert("method static/instance mismatch"); return; }
        if (befehl == 184) { if (!initialisieren(methodeEigentümer[dateiIndex], rahmenBefehlswort[rahmenIndex])) return; }
        else {
            int mauszeigerLesen = rahmenStapel[rahmenIndex] - methodeArgumentAnzahl[dateiIndex];
            if (mauszeigerLesen < 0 || operandStapelTyp[rahmenIndex * 128 + mauszeigerLesen] != 2) { fehlschlagWert("invalid method receiver"); return; }
            int objektVerweis = operandStapelWert[rahmenIndex * 128 + mauszeigerLesen];
            if (!istGültigObjekt(objektVerweis)) return;
            if (speicherhaldeWert[objektVerweis] < 32 || !enthältKlasse(speicherhaldeWert[objektVerweis] - 32, eigentümerWert)) { fehlschlagWert("method receiver type mismatch"); return; }
            if (befehl != 183) dateiIndex = methodeFinden(speicherhaldeWert[objektVerweis] - 32, Name, formatWert);
        }
        if (dateiIndex < 0 || (methodeZugriff[dateiIndex] & 0x400) != 0) { fehlschlagWert("AbstractMethodError"); return; }
        int sperreVerweis = 0;
        if ((methodeZugriff[dateiIndex] & 32) != 0) {
            if (befehl == 184) { int zeichenKode = methodeEigentümer[dateiIndex]; if (klasseSperre[zeichenKode] == 0) klasseSperre[zeichenKode] = speichergerätZuteilen(8, 0); sperreVerweis = klasseSperre[zeichenKode]; }
            else sperreVerweis = operandStapelWert[rahmenIndex * 128 + rahmenStapel[rahmenIndex] - methodeArgumentAnzahl[dateiIndex]];
            if (!sperreErwerben(sperreVerweis)) { if (!fehler) rahmenPosition[rahmenIndex] = rahmenBefehlswort[rahmenIndex]; return; }
        }
        aufrufen(dateiIndex); if (!fehler) rahmenSperre[rahmenIndex] = sperreVerweis;
    }
    static boolean kannAblegenDatenDatenfeld(int datenfeldVerweis, int datenWert) {
        if (datenWert == 0 || datenfeldElement[datenfeldVerweis] == 0) return true;
        boolean istErfolgreich = datenfeldElement[datenfeldVerweis] == -1 ? (datenWert > 0 && datenWert < speicherhaldeEndePosition && speicherhaldeWert[datenWert] == 1) : passendObjekt(datenWert, datenfeldElement[datenfeldVerweis]);
        if (!istErfolgreich && !fehler) ausnahmeAuslösen(17, "array element type mismatch");
        return istErfolgreich;
    }
    static int datenfeldPlatz(int verweis, int feldindexWert, int typWert) {
        if (!objektWert(verweis, typWert)) return 0;
        if (feldindexWert < 0 || feldindexWert >= speicherhaldeWert[verweis + 1]) { fehlschlagWert("ArrayIndexOutOfBoundsException"); return 0; }
        return verweis + 2 + feldindexWert;
    }
    static void befehlAusführen() {
        int restwertDaten = 500000, fragmentWert = 100;
        while (true) {
            if (fehler) { if (ausgelöstObjekt != 0) kennwertAusnahme(); if (fehler || rahmenIndex < aktuellAusführungsfaden * 32) break; }
            if (rahmenIndex < aktuellAusführungsfaden * 32 || anfrageÄndern || --fragmentWert == 0) { if (!umschaltenAusführungsfaden()) break; fragmentWert = 100; }
            if (rahmenIndex == 0 && klasseDefinitionStatuswert[eintragKlasseDefinition] != 2 && !initialisieren(eintragKlasseDefinition, rahmenPosition[rahmenIndex])) continue;
            if (rahmenIndex == aktuellAusführungsfaden * 32 && aktuellAusführungsfaden != 0 && (methodeZugriff[rahmenMethode[rahmenIndex]] & 32) != 0 && rahmenSperre[rahmenIndex] == 0) {
                int objektVerweis = ausführungsfadenZielobjekt[aktuellAusführungsfaden]; if (!sperreErwerben(objektVerweis)) { if (fehler) break; continue; } rahmenSperre[rahmenIndex] = objektVerweis;
            }
            vorläufigAnzahl = 0;
            if (--restwertDaten == 0) { fehlschlagWert("instruction limit (500000)"); break; }
            int ausführenVorgang = rahmenPosition[rahmenIndex]; rahmenBefehlswort[rahmenIndex] = ausführenVorgang; int Wert = befehlscodeByteLesen();
            if (fehler) break;
            if (Wert == 0) continue;
            if (Wert == 1) { wertAblegen(0, 2); continue; }
            if (Wert >= 2 && Wert <= 8) { wertAblegen(Wert - 3, 1); continue; }
            if (Wert == 16) { wertAblegen((byte)befehlscodeByteLesen(), 1); continue; }
            if (Wert == 17) { wertAblegen((short)befehlscodeKurzLesen(), 1); continue; }
            if (Wert == 18 || Wert == 19) {
                int Zahl = methodeEigentümer[rahmenMethode[rahmenIndex]] * 512 + (Wert == 18 ? befehlscodeByteLesen() : befehlscodeKurzLesen());
                if (Zahl <= 0 || Zahl >= konstanteKennzeichen.length) fehlschlagWert("invalid ldc constant");
                else if (konstanteKennzeichen[Zahl] == 3) wertAblegen(konstanteErsterWert[Zahl], 1);
                else if (konstanteKennzeichen[Zahl] == 8) wertAblegen(konstanteText(konstanteErsterWert[Zahl]), 2);
                else fehlschlagWert("unsupported ldc constant");
                continue;
            }
            if (Wert == 21 || Wert == 25) { lokalLesen(befehlscodeByteLesen(), Wert == 21 ? 1 : 2); continue; }
            if (Wert >= 26 && Wert <= 29) { lokalLesen(Wert - 26, 1); continue; }
            if (Wert >= 42 && Wert <= 45) { lokalLesen(Wert - 42, 2); continue; }
            if (Wert == 54 || Wert == 58) { lokalSchreiben(befehlscodeByteLesen(), Wert == 54 ? 1 : 2); continue; }
            if (Wert >= 59 && Wert <= 62) { lokalSchreiben(Wert - 59, 1); continue; }
            if (Wert >= 75 && Wert <= 78) { lokalSchreiben(Wert - 75, 2); continue; }
            if (Wert == 46 || Wert >= 50 && Wert <= 53) {
                int eintragPosition = werteSubtrahieren(1), objektVerweis = werteSubtrahieren(2), kategorieKode = Wert == 46 ? 2 : Wert == 50 ? 3 : Wert == 51 ? 20 : Wert == 52 ? 22 : 23;
                if (Wert == 51 && objektVerweis > 0 && objektVerweis < speicherhaldeEndePosition && speicherhaldeWert[objektVerweis] == 21) kategorieKode = 21;
                int mauszeigerLesen = datenfeldPlatz(objektVerweis, eintragPosition, kategorieKode); if (!fehler) wertAblegen(speicherhaldeWert[mauszeigerLesen], Wert == 50 ? 2 : 1); continue;
            }
            if (Wert == 79 || Wert >= 83 && Wert <= 86) {
                int eintragVerweis = werteSubtrahieren(Wert == 83 ? 2 : 1), eintragPosition = werteSubtrahieren(1), objektVerweis = werteSubtrahieren(2), kategorieKode = Wert == 79 ? 2 : Wert == 83 ? 3 : Wert == 84 ? 20 : Wert == 85 ? 22 : 23;
                if (Wert == 84 && objektVerweis > 0 && objektVerweis < speicherhaldeEndePosition && speicherhaldeWert[objektVerweis] == 21) kategorieKode = 21;
                int mauszeigerLesen = datenfeldPlatz(objektVerweis, eintragPosition, kategorieKode);
                if (!fehler && kategorieKode == 3 && !kannAblegenDatenDatenfeld(objektVerweis, eintragVerweis)) continue;
                if (!fehler) speicherhaldeWert[mauszeigerLesen] = kategorieKode == 20 ? (byte)eintragVerweis : kategorieKode == 21 ? eintragVerweis & 1 : kategorieKode == 22 ? (char)eintragVerweis : kategorieKode == 23 ? (short)eintragVerweis : eintragVerweis;
                continue;
            }
            if (Wert >= 87 && Wert <= 95) { stapelBefehlswort(Wert); continue; }
            if (Wert == 96 || Wert == 100 || Wert == 104 || Wert == 108 || Wert == 112 || Wert == 120
                || Wert == 122 || Wert == 124 || Wert == 126 || Wert == 128 || Wert == 130) {
                int zweiterOperand = werteSubtrahieren(1), ersterOperand = werteSubtrahieren(1), ergebnis = 0;
                if ((Wert == 108 || Wert == 112) && zweiterOperand == 0) { fehlschlagWert("ArithmeticException: / by zero"); continue; }
                if (Wert == 96) ergebnis = ersterOperand + zweiterOperand;
                if (Wert == 100) ergebnis = ersterOperand - zweiterOperand;
                if (Wert == 104) ergebnis = ersterOperand * zweiterOperand;
                if (Wert == 108) ergebnis = ersterOperand / zweiterOperand;
                if (Wert == 112) ergebnis = ersterOperand % zweiterOperand;
                if (Wert == 120) ergebnis = ersterOperand << zweiterOperand;
                if (Wert == 122) ergebnis = ersterOperand >> zweiterOperand;
                if (Wert == 124) ergebnis = ersterOperand >>> zweiterOperand;
                if (Wert == 126) ergebnis = ersterOperand & zweiterOperand;
                if (Wert == 128) ergebnis = ersterOperand | zweiterOperand;
                if (Wert == 130) ergebnis = ersterOperand ^ zweiterOperand;
                wertAblegen(ergebnis, 1); continue;
            }
            if (Wert == 116) { wertAblegen(-werteSubtrahieren(1), 1); continue; }
            if (Wert == 132) {
                int lokalGültigkeitsbereich = befehlscodeByteLesen(), erhöhenSchrittSchritt = (byte)befehlscodeByteLesen(); lokalLesen(lokalGültigkeitsbereich, 1); wertAblegen(werteSubtrahieren(1) + erhöhenSchrittSchritt, 1); lokalSchreiben(lokalGültigkeitsbereich, 1); continue;
            }
            if (Wert >= 145 && Wert <= 147) {
                int Zahl = werteSubtrahieren(1); wertAblegen(Wert == 145 ? (byte)Zahl : Wert == 146 ? (char)Zahl : (short)Zahl, 1); continue;
            }
            if (Wert >= 153 && Wert <= 167 || Wert == 198 || Wert == 199) {
                int zielWert = ausführenVorgang + (short)befehlscodeKurzLesen(); boolean sollFortfahren = Wert == 167;
                if (Wert >= 153 && Wert <= 158) {
                    int Zahl = werteSubtrahieren(1); sollFortfahren = Wert == 153 ? Zahl == 0 : Wert == 154 ? Zahl != 0 : Wert == 155 ? Zahl < 0 : Wert == 156 ? Zahl >= 0 : Wert == 157 ? Zahl > 0 : Zahl <= 0;
                } else if (Wert >= 159 && Wert <= 166) {
                    int zweiterOperand = werteSubtrahieren(Wert >= 165 ? 2 : 1), ersterOperand = werteSubtrahieren(Wert >= 165 ? 2 : 1);
                    sollFortfahren = Wert == 159 || Wert == 165 ? ersterOperand == zweiterOperand : Wert == 160 || Wert == 166 ? ersterOperand != zweiterOperand : Wert == 161 ? ersterOperand < zweiterOperand : Wert == 162 ? ersterOperand >= zweiterOperand : Wert == 163 ? ersterOperand > zweiterOperand : ersterOperand <= zweiterOperand;
                } else if (Wert == 198 || Wert == 199) { int Zahl = werteSubtrahieren(2); sollFortfahren = Wert == 198 ? Zahl == 0 : Zahl != 0; }
                if (sollFortfahren) bewegenWert(zielWert); continue;
            }
            if (Wert == 172 || Wert == 176 || Wert == 177) { zurückkehrenErgebnis(Wert == 172 ? 1 : Wert == 176 ? 2 : 0); continue; }
            if (Wert >= 178 && Wert <= 181) { feldAufrufen(befehlscodeKonstanteLesen(), Wert, ausführenVorgang); continue; }
            if (Wert >= 182 && Wert <= 185) {
                int kodiertWert = befehlscodeKonstanteLesen();
                if (Wert == 185) { int gesamtwertAnzahl = befehlscodeByteLesen(); if (gesamtwertAnzahl == 0 || befehlscodeByteLesen() != 0) { fehlschlagWert("invalid invokeinterface operands"); continue; } }
                methodeAufrufVorgang(kodiertWert, Wert); continue;
            }
            if (Wert == 187) { neuObjekt(klasseNameText(befehlscodeKonstanteLesen()), ausführenVorgang); continue; }
            if (Wert == 188 || Wert == 189) {
                int kategorieKode = 3, baustein = 0;
                if (Wert == 188) { int vorläufigDaten = befehlscodeByteLesen(); kategorieKode = vorläufigDaten == 10 ? 2 : vorläufigDaten == 8 ? 20 : vorläufigDaten == 4 ? 21 : vorläufigDaten == 5 ? 22 : vorläufigDaten == 9 ? 23 : 0; }
                else baustein = klasseNameText(befehlscodeKonstanteLesen());
                if (kategorieKode == 0) { fehlschlagWert("unsupported primitive array type"); continue; }
                int gültigLänge = werteSubtrahieren(1), objektVerweis = speichergerätZuteilen(kategorieKode, gültigLänge); if (!fehler) datenfeldElement[objektVerweis] = baustein; wertAblegen(objektVerweis, 2); continue;
            }
            if (Wert == 190) {
                int objektVerweis = werteSubtrahieren(2);
                if (istGültigObjekt(objektVerweis)) { int vergleichPosition = speicherhaldeWert[objektVerweis]; if (vergleichPosition != 2 && vergleichPosition != 3 && (vergleichPosition < 20 || vergleichPosition > 23)) fehlschlagWert("not an array"); else wertAblegen(speicherhaldeWert[objektVerweis + 1], 1); }
                continue;
            }
            if (Wert == 191) {
                int objektVerweis = werteSubtrahieren(2); if (istGültigObjekt(objektVerweis)) { if (speicherhaldeWert[objektVerweis] != 9) fehlschlagWert("athrow requires supported Throwable"); else { ausgelöstObjekt = objektVerweis; fehler = true; } }
                continue;
            }
            if (Wert == 192 || Wert == 193) {
                int nameKonstante = klasseNameText(befehlscodeKonstanteLesen()), objektVerweis = werteSubtrahieren(2); boolean vergleichen = passendObjekt(objektVerweis, nameKonstante);
                if (Wert == 193) wertAblegen(objektVerweis != 0 && vergleichen ? 1 : 0, 1);
                else { if (!vergleichen && !fehler) fehlschlagWert("ClassCastException"); wertAblegen(objektVerweis, 2); }
                continue;
            }
            if (Wert == 170 || Wert == 171) {
                int mauszeigerLesen = ausführenVorgang + 1, dateiIndex = rahmenMethode[rahmenIndex], tasteVerweis = werteSubtrahieren(1);
                while ((mauszeigerLesen - methodeStarten[dateiIndex]) % 4 != 0) mauszeigerLesen++;
                int zielobjektAdresse = positionGanzzahl(mauszeigerLesen);
                if (Wert == 170) { int niedrigWert = positionGanzzahl(mauszeigerLesen + 4), hochWert = positionGanzzahl(mauszeigerLesen + 8); if (tasteVerweis >= niedrigWert && tasteVerweis <= hochWert) zielobjektAdresse = positionGanzzahl(mauszeigerLesen + 12 + (tasteVerweis - niedrigWert) * 4); }
                else { int gesamtwertAnzahl = positionGanzzahl(mauszeigerLesen + 4); for (int schleifeIndex = 0; schleifeIndex < gesamtwertAnzahl; schleifeIndex++) if (positionGanzzahl(mauszeigerLesen + 8 + schleifeIndex * 8) == tasteVerweis) zielobjektAdresse = positionGanzzahl(mauszeigerLesen + 12 + schleifeIndex * 8); }
                bewegenWert(ausführenVorgang + zielobjektAdresse); continue;
            }
            if (Wert == 200) { bewegenWert(ausführenVorgang + positionGanzzahl(ausführenVorgang + 1)); continue; }
            if (Wert == 194 || Wert == 195) {
                int objektVerweis = werteSubtrahieren(2);
                if (Wert == 195) sperreFreigeben(objektVerweis);
                else if (!sperreErwerben(objektVerweis) && !fehler) { wertAblegen(objektVerweis, 2); rahmenPosition[rahmenIndex] = ausführenVorgang; }
                continue;
            }
            if (Wert == 196) {
                int befehlKode = befehlscodeByteLesen(), eintragPosition = befehlscodeKurzLesen();
                if (befehlKode == 21 || befehlKode == 25) lokalLesen(eintragPosition, befehlKode == 21 ? 1 : 2);
                else if (befehlKode == 54 || befehlKode == 58) lokalSchreiben(eintragPosition, befehlKode == 54 ? 1 : 2);
                else if (befehlKode == 132) { int änderungsbetragWert = (short)befehlscodeKurzLesen(); lokalLesen(eintragPosition, 1); wertAblegen(werteSubtrahieren(1) + änderungsbetragWert, 1); lokalSchreiben(eintragPosition, 1); }
                else fehlschlagWert("unsupported wide opcode");
                continue;
            }
            fehlschlagWert("unsupported bytecode");
        }
    }
    static int klasseDefinitionFinden(int Name) {
        for (int schleifeIndex = 0; schleifeIndex < klasseDefinitionAnzahl; schleifeIndex++) if (klasseDefinitionName[schleifeIndex] != 0 && passendMaschinenwort(klasseDefinitionName[schleifeIndex], Name)) return schleifeIndex;
        return klasseDefinitionLaden(konstanteText(Name));
    }
    static int klasseDefinitionLaden(int nameZeichenkette) {
        if (!objektWert(nameZeichenkette, 1)) return -1;
        int Länge = speicherhaldeWert[nameZeichenkette + 1];
        if (Länge < 1 || Länge > 505 || klasseDefinitionAnzahl == 16) { fehlschlagWert("class name/count limit"); return -1; }
        for (int schleifeIndex = 0; schleifeIndex < Länge; schleifeIndex++) { int zeichenKode = speicherhaldeWert[nameZeichenkette + 2 + schleifeIndex]; dateiNameText[schleifeIndex] = zeichenKode == '/' ? '.' : zeichenKode; }
        dateiNameText[Länge] = '.'; dateiNameText[Länge + 1] = 'c'; dateiNameText[Länge + 2] = 'l'; dateiNameText[Länge + 3] = 'a'; dateiNameText[Länge + 4] = 's'; dateiNameText[Länge + 5] = 's'; dateiNameText[Länge + 6] = 0;
        int größe = Benutzer.dateiLesen(dateiNameText, vorläufigDatei);
        if (größe < 0) { fehlschlagWert("ClassNotFoundException"); return -1; }
        int klasseDefinition = klasseDefinitionAnzahl++; klasseDefinitionGröße[klasseDefinition] = größe;
        for (int schleifeIndex = 0; schleifeIndex < größe; schleifeIndex++) Datei[klasseDefinition * 16384 + schleifeIndex] = vorläufigDatei[schleifeIndex];
        klasseLesen(klasseDefinition); if (fehler) return -1;
        int tatsächlichDaten = konstanteText(klasseDefinitionName[klasseDefinition]);
        if (!texteGleich(tatsächlichDaten, nameZeichenkette, true)) { fehlschlagWert("class name does not match file"); return -1; }
        int elternknotenWert = klasseDefinitionElternknoten[klasseDefinition];
        if (elternknotenWert != 0 && !maschinenwortText(elternknotenWert, "java/lang/Object") && !maschinenwortText(elternknotenWert, "java/lang/Thread")) {
            // Registrierte Klassen werden nicht erneut geladen; Vererbungszyklen werden ausdrücklich abgewiesen.
            int oberkanteWert = klasseDefinitionFinden(elternknotenWert);
            if (fehler || oberkanteWert < 0) return -1;
            int mauszeigerLesen = oberkanteWert, stufeAnzahl = 0;
            while (mauszeigerLesen >= 0 && stufeAnzahl++ < 16) {
                if (mauszeigerLesen == klasseDefinition) { fehlschlagWert("cyclic inheritance"); return -1; }
                mauszeigerLesen = elternknotenKlasse(mauszeigerLesen);
            }
            int versatzStarten = klassePlatzAnzahl[oberkanteWert];
            for (int dateiIndex = 0; dateiIndex < platzAnzahl; dateiIndex++) if (platzEigentümer[dateiIndex] == klasseDefinition && (platzErlaubnisse[dateiIndex] & 8) == 0) platzPosition[dateiIndex] += versatzStarten;
            klassePlatzAnzahl[klasseDefinition] += versatzStarten;
        }
        return klasseDefinition;
    }
    static int elternknotenKlasse(int klasseDefinition) {
        int Name = klasseDefinitionElternknoten[klasseDefinition];
        for (int schleifeIndex = 0; schleifeIndex < klasseDefinitionAnzahl; schleifeIndex++) if (Name != 0 && klasseDefinitionName[schleifeIndex] != 0 && passendMaschinenwort(klasseDefinitionName[schleifeIndex], Name)) return schleifeIndex;
        return -1;
    }
    static int methodeFinden(int klasseDefinition, int Name, int formatWert) {
        for (int tiefeWert = 0; klasseDefinition >= 0 && tiefeWert < 16; tiefeWert++, klasseDefinition = elternknotenKlasse(klasseDefinition)) {
            for (int schleifeIndex = 0; schleifeIndex < methodeAnzahl; schleifeIndex++) if (methodeEigentümer[schleifeIndex] == klasseDefinition && passendMaschinenwort(methodeNameText[schleifeIndex], Name) && passendMaschinenwort(methodeTyp[schleifeIndex], formatWert)) return schleifeIndex;
        }
        return -1;
    }
    static int nameMethode(int klasseDefinition, String Name, String formatWert) {
        for (int tiefeWert = 0; klasseDefinition >= 0 && tiefeWert < 16; tiefeWert++, klasseDefinition = elternknotenKlasse(klasseDefinition))
            for (int schleifeIndex = 0; schleifeIndex < methodeAnzahl; schleifeIndex++) if (methodeEigentümer[schleifeIndex] == klasseDefinition && maschinenwortText(methodeNameText[schleifeIndex], Name) && maschinenwortText(methodeTyp[schleifeIndex], formatWert)) return schleifeIndex;
        return -1;
    }
    static int typArt(int Name) { return Datei[konstanteErsterWert[Name]] == 'L' || Datei[konstanteErsterWert[Name]] == '[' ? 2 : 1; }
    static boolean initialisieren(int klasseDefinition, int befehlStarten) {
        if (klasseDefinition < 0 || fehler) return false;
        if (klasseDefinitionStatuswert[klasseDefinition] == 3) { fehlschlagWert("NoClassDefFoundError: initialization failed"); return false; }
        if (klasseDefinitionStatuswert[klasseDefinition] == 1 && klasseAusführungsfaden[klasseDefinition] != aktuellAusführungsfaden) { rahmenPosition[rahmenIndex] = befehlStarten; anfrageÄndern = true; return false; }
        if (klasseDefinitionStatuswert[klasseDefinition] != 0) return true;
        int oberkanteWert = elternknotenKlasse(klasseDefinition);
        if (oberkanteWert >= 0 && !initialisieren(oberkanteWert, befehlStarten)) return false;
        klasseDefinitionStatuswert[klasseDefinition] = 1; klasseAusführungsfaden[klasseDefinition] = aktuellAusführungsfaden;
        if (klasseDefinitionInitialisieren[klasseDefinition] != 0) {
            rahmenPosition[rahmenIndex] = befehlStarten;
            aufrufen(klasseDefinitionInitialisieren[klasseDefinition] - 1); if (!fehler) rahmenInitialisieren[rahmenIndex] = klasseDefinition + 1;
            return false;
        }
        klasseDefinitionStatuswert[klasseDefinition] = 2; return true;
    }
    static void feldAufrufen(int Nummer, int befehl, int ausführenVorgang) {
        if (!konstantePrüfen(Nummer, 9)) return;
        int eigentümerWert = klasseNameText(konstanteErsterWert[Nummer]), Name = verweisName(konstanteZweiterWert[Nummer]), formatWert = verweisTyp(konstanteZweiterWert[Nummer]);
        if (maschinenwortText(eigentümerWert, "java/lang/System") && (maschinenwortText(Name, "out") || maschinenwortText(Name, "err")) && maschinenwortText(formatWert, "Ljava/io/PrintStream;") && befehl == 178) { wertAblegen(-1, 2); return; }
        int klasseDefinition = klasseDefinitionFinden(eigentümerWert); if (klasseDefinition < 0 || fehler) return;
        int gefundenWert = -1;
        for (int mauszeigerLesen = klasseDefinition, tiefeWert = 0; mauszeigerLesen >= 0 && tiefeWert < 16 && gefundenWert < 0; tiefeWert++, mauszeigerLesen = elternknotenKlasse(mauszeigerLesen))
            for (int dateiIndex = 0; dateiIndex < platzAnzahl; dateiIndex++) if (platzEigentümer[dateiIndex] == mauszeigerLesen && passendMaschinenwort(platzName[dateiIndex], Name) && passendMaschinenwort(platzTyp[dateiIndex], formatWert)) gefundenWert = dateiIndex;
        if (gefundenWert < 0) { fehlschlagWert("NoSuchFieldError"); return; }
        boolean statischWert = befehl == 178 || befehl == 179;
        if (statischWert != ((platzErlaubnisse[gefundenWert] & 8) != 0)) { fehlschlagWert("field static/instance mismatch"); return; }
        if (statischWert && !initialisieren(platzEigentümer[gefundenWert], ausführenVorgang)) return;
        int typWert = typArt(formatWert), Wert = 0;
        if (befehl == 179 || befehl == 181) Wert = werteSubtrahieren(typWert);
        if (statischWert) { if (befehl == 178) wertAblegen(platzDaten[gefundenWert], typWert); else if (!fehler) platzDaten[gefundenWert] = Wert; return; }
        int objektVerweis = werteSubtrahieren(2);
        if (!istGültigObjekt(objektVerweis)) return;
        if (speicherhaldeWert[objektVerweis] < 32 || !enthältKlasse(speicherhaldeWert[objektVerweis] - 32, eigentümerWert)) { fehlschlagWert("field receiver type mismatch"); return; }
        int bewahrtPlatz = objektVerweis + 2 + platzPosition[gefundenWert];
        if (befehl == 180) wertAblegen(speicherhaldeWert[bewahrtPlatz], typWert);
        else if (!fehler) { speicherhaldeWert[bewahrtPlatz] = Wert; speicherhaldeVerweis[bewahrtPlatz] = typWert == 2 ? 1 : 0; }
    }
    static boolean enthältKlasse(int klasseDefinition, int Name) {
        for (int tiefe = 0; klasseDefinition >= 0 && tiefe < 16; tiefe++, klasseDefinition = elternknotenKlasse(klasseDefinition)) {
            if (passendMaschinenwort(klasseDefinitionName[klasseDefinition], Name) || (klasseDefinitionElternknoten[klasseDefinition] != 0 && passendMaschinenwort(klasseDefinitionElternknoten[klasseDefinition], Name))) return true;
            for (int innerlichPosition = 0; innerlichPosition < klasseSchnittstelleAnzahl[klasseDefinition]; innerlichPosition++) if (passendMaschinenwort(klasseSchnittstelle[klasseDefinition * 16 + innerlichPosition], Name)) return true;
        }
        return false;
    }
    static boolean texteGleich(int ersterDaten, int byteDaten, boolean pfad) {
        if (ersterDaten == byteDaten) return true;
        if (ersterDaten <= 0 || byteDaten <= 0 || speicherhaldeWert[ersterDaten] != 1 || speicherhaldeWert[byteDaten] != 1 || speicherhaldeWert[ersterDaten + 1] != speicherhaldeWert[byteDaten + 1]) return false;
        for (int schleifeIndex = 0; schleifeIndex < speicherhaldeWert[ersterDaten + 1]; schleifeIndex++) {
            int waagerechteKoordinateKoordinate = speicherhaldeWert[ersterDaten + 2 + schleifeIndex], senkrechteKoordinateKoordinate = speicherhaldeWert[byteDaten + 2 + schleifeIndex];
            if (pfad) { if (waagerechteKoordinateKoordinate == '.') waagerechteKoordinateKoordinate = '/'; if (senkrechteKoordinateKoordinate == '.') senkrechteKoordinateKoordinate = '/'; }
            if (waagerechteKoordinateKoordinate != senkrechteKoordinateKoordinate) return false;
        }
        return true;
    }
    static boolean istGültigObjekt(int objektVerweis) {
        if (objektVerweis == 0) { fehlschlagWert("NullPointerException"); return false; }
        if (objektVerweis < 1 || objektVerweis >= speicherhaldeEndePosition || speicherhaldeBreite[objektVerweis] < 2 || speicherhaldeWert[objektVerweis] == 0) { fehlschlagWert("invalid object reference"); return false; }
        return true;
    }
    static void wertSchützen(int objektVerweis) {
        if (objektVerweis > 0 && objektVerweis < speicherhaldeEndePosition && speicherhaldeBreite[objektVerweis] >= 2 && vorläufigAnzahl < vorläufigVerweis.length) vorläufigVerweis[vorläufigAnzahl++] = objektVerweis;
    }
    static void wertAnzeigen(int objektVerweis) {
        if (objektVerweis > 0 && objektVerweis < speicherhaldeEndePosition && speicherhaldeBreite[objektVerweis] >= 2 && speicherhaldeWert[objektVerweis] != 0 && speicherhaldeMerkzeichen[objektVerweis] == 0) {
            speicherhaldeMerkzeichen[objektVerweis] = 1; fürDarstellenWarten[darstellenAnzahl++] = objektVerweis;
        }
    }
    static void abfallEinsammeln() {
        darstellenAnzahl = 0; sammlungAnzahl++;
        for (int positionPrüfen = 1; positionPrüfen < speicherhaldeEndePosition; positionPrüfen += speicherhaldeBreite[positionPrüfen]) speicherhaldeMerkzeichen[positionPrüfen] = 0;
        for (int schleifeIndex = 0; schleifeIndex < zeichenketteVerweis.length; schleifeIndex++) wertAnzeigen(zeichenketteVerweis[schleifeIndex]);
        for (int schleifeIndex = 0; schleifeIndex < platzAnzahl; schleifeIndex++) if ((platzErlaubnisse[schleifeIndex] & 8) != 0 && typArt(platzTyp[schleifeIndex]) == 2) wertAnzeigen(platzDaten[schleifeIndex]);
        for (int vorläufigDaten = 0; vorläufigDaten < ausführungsfadenAnzahl; vorläufigDaten++) {
            wertAnzeigen(ausführungsfadenObjekt[vorläufigDaten]); wertAnzeigen(ausführungsfadenZielobjekt[vorläufigDaten]);
            int oberkantePosition = vorläufigDaten == aktuellAusführungsfaden ? rahmenIndex : ausführungsfadenRahmen[vorläufigDaten];
            for (int dateiIndex = vorläufigDaten * 32; dateiIndex <= oberkantePosition; dateiIndex++) {
                for (int innerlichPosition = 0; innerlichPosition < methodeLokalvariablen[rahmenMethode[dateiIndex]]; innerlichPosition++) if (lokalTyp[dateiIndex * 128 + innerlichPosition] == 2) wertAnzeigen(lokalWert[dateiIndex * 128 + innerlichPosition]);
                for (int innerlichPosition = 0; innerlichPosition < rahmenStapel[dateiIndex]; innerlichPosition++) if (operandStapelTyp[dateiIndex * 128 + innerlichPosition] == 2) wertAnzeigen(operandStapelWert[dateiIndex * 128 + innerlichPosition]);
            }
        }
        for (int schleifeIndex = 0; schleifeIndex < bildschirmVerweis.length; schleifeIndex++) wertAnzeigen(bildschirmVerweis[schleifeIndex]);
        for (int schleifeIndex = 0; schleifeIndex < späterAnzahl; schleifeIndex++) wertAnzeigen(zeitplanSpäter[schleifeIndex]);
        for (int schleifeIndex = 0; schleifeIndex < ablegenDatenGanzzahl.length; schleifeIndex++) wertAnzeigen(ablegenDatenGanzzahl[schleifeIndex]);
        for (int schleifeIndex = 0; schleifeIndex < klasseDefinitionAnzahl; schleifeIndex++) wertAnzeigen(klasseSperre[schleifeIndex]);
        for (int positionPrüfen = 1; positionPrüfen < speicherhaldeEndePosition; positionPrüfen += speicherhaldeBreite[positionPrüfen]) if (sperreTiefe[positionPrüfen] > 0) wertAnzeigen(positionPrüfen);
        wertAnzeigen(ausgelöstObjekt);
        for (int schleifeIndex = 0; schleifeIndex < vorläufigAnzahl; schleifeIndex++) wertAnzeigen(vorläufigVerweis[schleifeIndex]);
        while (darstellenAnzahl > 0) {
            int objektVerweis = fürDarstellenWarten[--darstellenAnzahl], kategorieKode = speicherhaldeWert[objektVerweis];
            for (int schleifeIndex = objektVerweis + 2; schleifeIndex < objektVerweis + speicherhaldeBreite[objektVerweis]; schleifeIndex++) if (kategorieKode == 3 || kategorieKode == 4 || speicherhaldeVerweis[schleifeIndex] != 0) wertAnzeigen(speicherhaldeWert[schleifeIndex]);
        }
        for (int positionPrüfen = 1; positionPrüfen < speicherhaldeEndePosition; positionPrüfen += speicherhaldeBreite[positionPrüfen]) if (speicherhaldeMerkzeichen[positionPrüfen] == 0) speicherhaldeWert[positionPrüfen] = 0;
        for (int positionPrüfen = 1; positionPrüfen < speicherhaldeEndePosition; positionPrüfen += speicherhaldeBreite[positionPrüfen]) if (speicherhaldeWert[positionPrüfen] == 0) {
            while (positionPrüfen + speicherhaldeBreite[positionPrüfen] < speicherhaldeEndePosition && speicherhaldeWert[positionPrüfen + speicherhaldeBreite[positionPrüfen]] == 0) { int nächsterPosition = positionPrüfen + speicherhaldeBreite[positionPrüfen]; speicherhaldeBreite[positionPrüfen] += speicherhaldeBreite[nächsterPosition]; speicherhaldeBreite[nächsterPosition] = 0; }
            if (positionPrüfen + speicherhaldeBreite[positionPrüfen] == speicherhaldeEndePosition) { speicherhaldeEndePosition = positionPrüfen; break; }
        }
    }
    static int neuSpeicher(int artWert, int Länge) {
        if (Länge < 0) { fehlschlagWert("NegativeArraySizeException"); return 0; }
        if (Länge > speicherhaldeWert.length - 3) { fehlschlagWert("object heap exhausted"); return 0; }
        int erforderlichAnzahl = Länge + 2, objektVerweis = 0;
        if (erforderlichAnzahl <= speicherhaldeWert.length - speicherhaldeEndePosition) { objektVerweis = speicherhaldeEndePosition; speicherhaldeEndePosition += erforderlichAnzahl; }
        else {
            abfallEinsammeln();
            for (int mauszeigerLesen = 1; mauszeigerLesen < speicherhaldeEndePosition; mauszeigerLesen += speicherhaldeBreite[mauszeigerLesen]) if (speicherhaldeWert[mauszeigerLesen] == 0 && speicherhaldeBreite[mauszeigerLesen] >= erforderlichAnzahl) { objektVerweis = mauszeigerLesen; break; }
            if (objektVerweis != 0) {
                int verbleibendLänge = speicherhaldeBreite[objektVerweis] - erforderlichAnzahl;
                if (verbleibendLänge >= 2) { speicherhaldeBreite[objektVerweis + erforderlichAnzahl] = verbleibendLänge; speicherhaldeWert[objektVerweis + erforderlichAnzahl] = 0; }
                else erforderlichAnzahl += verbleibendLänge;
            } else if (erforderlichAnzahl <= speicherhaldeWert.length - speicherhaldeEndePosition) { objektVerweis = speicherhaldeEndePosition; speicherhaldeEndePosition += erforderlichAnzahl; }
        }
        if (objektVerweis == 0) { fehlschlagWert("object heap exhausted"); return 0; }
        for (int schleifeIndex = 0; schleifeIndex < erforderlichAnzahl; schleifeIndex++) { speicherhaldeWert[objektVerweis + schleifeIndex] = 0; speicherhaldeVerweis[objektVerweis + schleifeIndex] = 0; speicherhaldeBreite[objektVerweis + schleifeIndex] = 0; }
        datenfeldElement[objektVerweis] = 0;
        speicherhaldeBreite[objektVerweis] = erforderlichAnzahl; speicherhaldeWert[objektVerweis] = artWert; speicherhaldeWert[objektVerweis + 1] = Länge; wertSchützen(objektVerweis); return objektVerweis;
    }
    static int ausnahmeKlasse(String nameKonstante) {
        if (JavaWerkzeug.gleichText(nameKonstante, "java/lang/Throwable")) return 1;
        if (JavaWerkzeug.gleichText(nameKonstante, "java/lang/Exception")) return 2;
        if (JavaWerkzeug.gleichText(nameKonstante, "java/lang/RuntimeException")) return 3;
        if (JavaWerkzeug.gleichText(nameKonstante, "java/lang/ArithmeticException")) return 4;
        if (JavaWerkzeug.gleichText(nameKonstante, "java/lang/NullPointerException")) return 5;
        if (JavaWerkzeug.gleichText(nameKonstante, "java/lang/IndexOutOfBoundsException")) return 6;
        if (JavaWerkzeug.gleichText(nameKonstante, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (JavaWerkzeug.gleichText(nameKonstante, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (JavaWerkzeug.gleichText(nameKonstante, "java/lang/IllegalArgumentException")) return 9;
        if (JavaWerkzeug.gleichText(nameKonstante, "java/lang/NumberFormatException")) return 10;
        if (JavaWerkzeug.gleichText(nameKonstante, "java/io/IOException")) return 11;
        if (JavaWerkzeug.gleichText(nameKonstante, "java/io/FileNotFoundException")) return 12;
        if (JavaWerkzeug.gleichText(nameKonstante, "java/lang/IllegalStateException")) return 13;
        if (JavaWerkzeug.gleichText(nameKonstante, "java/lang/ClassCastException")) return 14;
        if (JavaWerkzeug.gleichText(nameKonstante, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int ausnahmeKonstante(int Name) {
        for (int schleifeIndex = 1; schleifeIndex <= 41; schleifeIndex++) if (maschinenwortText(Name, ausnahmeName(schleifeIndex))) return schleifeIndex;
        return 0;
    }
    static String ausnahmeName(int identitätWert) {
        if (identitätWert == 40) return "java/lang/InterruptedException";
        if (identitätWert == 41) return "Deutsch/eigen/WartenUnterbrochenAusnahme";
        if (identitätWert == 39) return "java/net/SocketException";
        if (identitätWert == 20) return "Deutsch/eigen/ausnahme";
        if (identitätWert == 21) return "Deutsch/eigen/AusführungAusnahme";
        if (identitätWert == 22) return "Deutsch/eigen/EingabeAusgabeAusnahme";
        if (identitätWert == 23) return "Deutsch/eigen/WartenZeitüberschreitungAusnahme";
        if (identitätWert == 24) return "Deutsch/eigen/AdresseNachschlagenAusnahme";
        if (identitätWert == 25) return "Deutsch/eigen/FehlendDateiAusnahme";
        if (identitätWert == 26) return "Deutsch/eigen/KommunikationAusnahme";
        if (identitätWert == 27) return "Deutsch/eigen/UngültigArgumentAusnahme";
        if (identitätWert == 28) return "Deutsch/eigen/NummerFormatFehlschlag";
        if (identitätWert == 29) return "Deutsch/eigen/GrenzenAusnahme";
        if (identitätWert == 30) return "Deutsch/eigen/DatenfeldGrenzenAusnahme";
        if (identitätWert == 31) return "Deutsch/eigen/ZeichenketteGrenzenAusnahme";
        if (identitätWert == 32) return "Deutsch/eigen/NullverweisVerweisAusnahme";
        if (identitätWert == 33) return "Deutsch/eigen/ArithmetikFehlschlag";
        if (identitätWert == 34) return "Deutsch/eigen/StatuswertAusnahme";
        if (identitätWert == 35) return "Deutsch/eigen/TypTypumwandlungAusnahme";
        if (identitätWert == 36) return "Deutsch/eigen/NegativDatenfeldGrößeFehlschlag";
        if (identitätWert == 37) return "Deutsch/eigen/DatenfeldAblegenDatenFehlschlag";
        if (identitätWert == 38) return "Deutsch/eigen/AusführungsfadenStatuswertAusnahme";
        if (identitätWert == 1) return "java/lang/Throwable"; if (identitätWert == 2) return "java/lang/Exception";
        if (identitätWert == 3) return "java/lang/RuntimeException"; if (identitätWert == 4) return "java/lang/ArithmeticException";
        if (identitätWert == 5) return "java/lang/NullPointerException"; if (identitätWert == 6) return "java/lang/IndexOutOfBoundsException";
        if (identitätWert == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (identitätWert == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (identitätWert == 9) return "java/lang/IllegalArgumentException"; if (identitätWert == 10) return "java/lang/NumberFormatException";
        if (identitätWert == 11) return "java/io/IOException"; if (identitätWert == 12) return "java/io/FileNotFoundException";
        if (identitätWert == 17) return "java/lang/ArrayStoreException";
        if (identitätWert == 18) return "java/net/UnknownHostException";
        if (identitätWert == 19) return "java/net/SocketTimeoutException";
        if (identitätWert == 16) return "java/lang/IllegalThreadStateException";
        if (identitätWert == 13) return "java/lang/IllegalStateException"; if (identitätWert == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int ausnahmeElternknoten(int identitätWert) {
        if (identitätWert == 40) return 2;
        if (identitätWert == 41) return 40;
        if (identitätWert == 39) return 11;
        if (identitätWert == 1) return 0;
        if (identitätWert == 2) return 1;
        if (identitätWert == 3) return 2;
        if (identitätWert == 4) return 3;
        if (identitätWert == 5) return 3;
        if (identitätWert == 6) return 3;
        if (identitätWert == 7) return 6;
        if (identitätWert == 8) return 6;
        if (identitätWert == 9) return 3;
        if (identitätWert == 10) return 9;
        if (identitätWert == 11) return 2;
        if (identitätWert == 12) return 11;
        if (identitätWert == 13) return 3;
        if (identitätWert == 14) return 3;
        if (identitätWert == 15) return 3;
        if (identitätWert == 16) return 9;
        if (identitätWert == 17) return 3;
        if (identitätWert == 18) return 11;
        if (identitätWert == 19) return 11;
        if (identitätWert == 20) return 2;
        if (identitätWert == 21) return 3;
        if (identitätWert == 22) return 11;
        if (identitätWert == 23) return 22;
        if (identitätWert == 24) return 22;
        if (identitätWert == 25) return 22;
        if (identitätWert == 26) return 22;
        if (identitätWert == 27) return 9;
        if (identitätWert == 28) return 27;
        if (identitätWert == 29) return 6;
        if (identitätWert == 30) return 29;
        if (identitätWert == 31) return 29;
        if (identitätWert == 32) return 5;
        if (identitätWert == 33) return 4;
        if (identitätWert == 34) return 13;
        if (identitätWert == 35) return 14;
        if (identitätWert == 36) return 15;
        if (identitätWert == 37) return 17;
        if (identitätWert == 38) return 16;
        return 0;
    }
    static boolean enthältAusnahme(int tatsächlichWert, int gewünscht) {
        for (int tiefeWert = 0; tatsächlichWert != 0 && tiefeWert < 16; tiefeWert++, tatsächlichWert = ausnahmeElternknoten(tatsächlichWert))
            if (tatsächlichWert == gewünscht) return true;
        return false;
    }
    static void ausnahmeAuslösen(int identitätWert, String liesmichVerweis) {
        int objektVerweis = neuSpeicher(9, 2); if (fehler) return;
        speicherhaldeWert[objektVerweis + 2] = identitätWert; speicherhaldeWert[objektVerweis + 3] = wirtssystemZeichen(liesmichVerweis); speicherhaldeVerweis[objektVerweis + 3] = 1;
        ausgelöstObjekt = objektVerweis; fehler = true;
    }
    static boolean passendObjekt(int objektVerweis, int Name) {
        if (objektVerweis == 0) return true;
        if (!istGültigObjekt(objektVerweis)) return false;
        int kategorieKode = speicherhaldeWert[objektVerweis];
        if (maschinenwortText(Name, "java/lang/Object")) return true;
        if (kategorieKode >= 32) return enthältKlasse(kategorieKode - 32, Name);
        if (kategorieKode == 9) { int zielobjektAdresse = ausnahmeKonstante(Name); return zielobjektAdresse != 0 && enthältAusnahme(speicherhaldeWert[objektVerweis + 2], zielobjektAdresse); }
        if (kategorieKode == 1) return maschinenwortText(Name, "java/lang/String") || maschinenwortText(Name, "java/lang/CharSequence");
        if (kategorieKode == 4) return maschinenwortText(Name, "java/lang/StringBuilder") || maschinenwortText(Name, "java/lang/CharSequence");
        if (kategorieKode == 10) return maschinenwortText(Name, "java/util/ArrayList") || maschinenwortText(Name, "java/util/List");
        if (kategorieKode == 11) return maschinenwortText(Name, "java/util/HashMap") || maschinenwortText(Name, "java/util/Map");
        if (kategorieKode == 12) return maschinenwortText(Name, "java/lang/Integer") || maschinenwortText(Name, "java/lang/Number");
        if (kategorieKode >= 24 && kategorieKode <= 28 && speicherhaldeWert[objektVerweis + 13] != 0) return koreanischBildschirmKlasse(Name) == kategorieKode || maschinenwortText(Name, "Deutsch/eigen/BildschirmElement");
        if (kategorieKode >= 24 && kategorieKode <= 28) return (koreanischBildschirmKlasse(Name) == 0 && bildschirmKlasse(Name) == kategorieKode) || maschinenwortText(Name, "java/awt/Component") || maschinenwortText(Name, "java/awt/Container") || maschinenwortText(Name, "javax/swing/JComponent");
        if (kategorieKode == 29) return maschinenwortText(Name, speicherhaldeWert[objektVerweis + 3] != 0 ? "Deutsch/eigen/AktionMitteilung" : "java/awt/event/ActionEvent");
        if (kategorieKode == 30) return maschinenwortText(Name, "java/awt/FlowLayout") || maschinenwortText(Name, "java/awt/LayoutManager");
        if (kategorieKode == 17) return maschinenwortText(Name, "java/net/Socket");
        if (kategorieKode == 18) return maschinenwortText(Name, "java/net/ServerSocket");
        if (kategorieKode == 19) return maschinenwortText(Name, speicherhaldeWert[objektVerweis + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (kategorieKode == 14) return maschinenwortText(Name, "java/net/InetAddress");
        if (kategorieKode == 15) return maschinenwortText(Name, "java/net/DatagramSocket");
        if (kategorieKode == 16) return maschinenwortText(Name, "java/net/DatagramPacket");
        if (kategorieKode == 13) return maschinenwortText(Name, speicherhaldeWert[objektVerweis + 3] != 0 ? "Deutsch/eigen/hintergrundarbeiter" : "java/lang/Thread");
        if (kategorieKode == 2) return maschinenwortText(Name, "[I"); if (kategorieKode == 20) return maschinenwortText(Name, "[B"); if (kategorieKode == 21) return maschinenwortText(Name, "[Z");
        if (kategorieKode == 22) return maschinenwortText(Name, "[C"); if (kategorieKode == 23) return maschinenwortText(Name, "[S");
        if (kategorieKode != 3) return false;
        if (maschinenwortText(Name, "[Ljava/lang/Object;")) return true;
        int baustein = datenfeldElement[objektVerweis];
        if (baustein == -1) return maschinenwortText(Name, "[Ljava/lang/String;") || maschinenwortText(Name, "[Ljava/lang/CharSequence;");
        if (baustein == 0) return false;
        if (datenfeldKlassenVergleichAnstellen(baustein, Name)) return true;
        if ((maschinenwortText(baustein, "java/lang/String") || maschinenwortText(baustein, "java/lang/StringBuilder")) && maschinenwortText(Name, "[Ljava/lang/CharSequence;")) return true;
        for (int schleifeIndex = 0; schleifeIndex < klasseDefinitionAnzahl; schleifeIndex++) if (passendMaschinenwort(klasseDefinitionName[schleifeIndex], baustein)) {
            for (int zeichenKode = schleifeIndex, tiefe = 0; zeichenKode >= 0 && tiefe < 16; tiefe++, zeichenKode = elternknotenKlasse(zeichenKode)) {
                if (datenfeldKlassenVergleichAnstellen(klasseDefinitionElternknoten[zeichenKode], Name)) return true;
                for (int innerlichPosition = 0; innerlichPosition < klasseSchnittstelleAnzahl[zeichenKode]; innerlichPosition++) if (datenfeldKlassenVergleichAnstellen(klasseSchnittstelle[zeichenKode * 16 + innerlichPosition], Name)) return true;
            }
        }
        return false;
    }
    static boolean datenfeldKlassenVergleichAnstellen(int nameKonstante, int deskriptor) {
        int positionPrüfen = konstanteErsterWert[deskriptor], eintragAnzahl = konstanteZweiterWert[deskriptor];
        if (nameKonstante == 0 || eintragAnzahl < 4 || Datei[positionPrüfen] != '[' || Datei[positionPrüfen + 1] != 'L' || Datei[positionPrüfen + eintragAnzahl - 1] != ';' || konstanteZweiterWert[nameKonstante] != eintragAnzahl - 3) return false;
        for (int schleifeIndex = 0; schleifeIndex < eintragAnzahl - 3; schleifeIndex++) if (Datei[konstanteErsterWert[nameKonstante] + schleifeIndex] != Datei[positionPrüfen + 2 + schleifeIndex]) return false;
        return true;
    }
    static void kennwertAusnahme() {
        if (ausgelöstObjekt == 0) return;
        fehler = false;
        while (rahmenIndex >= aktuellAusführungsfaden * 32) {
            int dateiIndex = rahmenMethode[rahmenIndex], mauszeigerLesen = rahmenBefehlswort[rahmenIndex];
            for (int schleifeIndex = 0; schleifeIndex < anzahlAbfangen; schleifeIndex++) if (methodeAbfangen[schleifeIndex] == dateiIndex && mauszeigerLesen >= startenAbfangen[schleifeIndex] && mauszeigerLesen < endeAbfangen[schleifeIndex]
                && (klasseAbfangen[schleifeIndex] == 0 || passendObjekt(ausgelöstObjekt, klasseAbfangen[schleifeIndex]))) {
                rahmenPosition[rahmenIndex] = positionAbfangen[schleifeIndex]; rahmenStapel[rahmenIndex] = 0; wertAblegen(ausgelöstObjekt, 2); ausgelöstObjekt = 0; return;
            }
            if (rahmenInitialisieren[rahmenIndex] != 0) klasseDefinitionStatuswert[rahmenInitialisieren[rahmenIndex] - 1] = 3;
            if (rahmenSperre[rahmenIndex] != 0) { sperreFreigeben(rahmenSperre[rahmenIndex]); rahmenSperre[rahmenIndex] = 0; }
            rahmenIndex--;
        }
        Benutzer.schreiben("Uncaught ");
        if (speicherhaldeWert[ausgelöstObjekt] == 9) { Benutzer.schreiben(ausnahmeName(speicherhaldeWert[ausgelöstObjekt + 2])); Benutzer.schreiben(": "); textSchreiben(speicherhaldeWert[ausgelöstObjekt + 3]); }
        else Benutzer.schreiben("user exception");
        Benutzer.zeichenWertSchreiben(10); ausgelöstObjekt = 0; fehler = true;
    }
    // Diese JVM erlaubt derzeit nur Stapelwerte der category-1 (int/reference).
    static void stapelBefehlswort(int befehlKode) {
        int ersterDaten = werteSubtrahieren(0), ersterFormat = zurückkehrenTyp;
        if (befehlKode == 87) return;
        if (befehlKode == 89) { wertAblegen(ersterDaten, ersterFormat); wertAblegen(ersterDaten, ersterFormat); return; }
        int byteDaten = werteSubtrahieren(0), zweiterFormat = zurückkehrenTyp;
        if (befehlKode == 88) return;
        if (befehlKode == 90) { wertAblegen(ersterDaten, ersterFormat); wertAblegen(byteDaten, zweiterFormat); wertAblegen(ersterDaten, ersterFormat); return; }
        if (befehlKode == 92) { wertAblegen(byteDaten, zweiterFormat); wertAblegen(ersterDaten, ersterFormat); wertAblegen(byteDaten, zweiterFormat); wertAblegen(ersterDaten, ersterFormat); return; }
        if (befehlKode == 95) { wertAblegen(ersterDaten, ersterFormat); wertAblegen(byteDaten, zweiterFormat); return; }
        int zeichenKode = werteSubtrahieren(0), dritterFormat = zurückkehrenTyp;
        if (befehlKode == 91) { wertAblegen(ersterDaten, ersterFormat); wertAblegen(zeichenKode, dritterFormat); wertAblegen(byteDaten, zweiterFormat); wertAblegen(ersterDaten, ersterFormat); return; }
        if (befehlKode == 93) { wertAblegen(byteDaten, zweiterFormat); wertAblegen(ersterDaten, ersterFormat); wertAblegen(zeichenKode, dritterFormat); wertAblegen(byteDaten, zweiterFormat); wertAblegen(ersterDaten, ersterFormat); return; }
        int nachlaufendWert = werteSubtrahieren(0), vierterFormat = zurückkehrenTyp;
        wertAblegen(byteDaten, zweiterFormat); wertAblegen(ersterDaten, ersterFormat); wertAblegen(nachlaufendWert, vierterFormat); wertAblegen(zeichenKode, dritterFormat); wertAblegen(byteDaten, zweiterFormat); wertAblegen(ersterDaten, ersterFormat);
    }
    static void neuObjekt(int nameKonstante, int beginnendPunkt) {
        int kategorieKode = 0, gültigLänge = 0, ausnahmeVerweis = ausnahmeKonstante(nameKonstante);
        if (maschinenwortText(nameKonstante, "java/lang/StringBuilder")) { kategorieKode = 4; gültigLänge = 1; }
        if (maschinenwortText(nameKonstante, "java/io/FileInputStream")) { kategorieKode = 5; gültigLänge = 2; }
        if (maschinenwortText(nameKonstante, "java/io/FileOutputStream")) { kategorieKode = 6; gültigLänge = 2; }
        if (ausnahmeVerweis != 0) { kategorieKode = 9; gültigLänge = 2; }
        if (maschinenwortText(nameKonstante, "java/util/ArrayList")) { kategorieKode = 10; gültigLänge = 2; }
        if (maschinenwortText(nameKonstante, "java/util/HashMap")) { kategorieKode = 11; gültigLänge = 2; }
        if (maschinenwortText(nameKonstante, "java/lang/Integer")) { kategorieKode = 12; gültigLänge = 1; }
        if (maschinenwortText(nameKonstante, "java/net/Socket")) { kategorieKode = 17; gültigLänge = 5; }
        if (maschinenwortText(nameKonstante, "java/net/ServerSocket")) { kategorieKode = 18; gültigLänge = 5; }
        if (maschinenwortText(nameKonstante, "java/net/DatagramSocket")) { kategorieKode = 15; gültigLänge = 3; }
        if (maschinenwortText(nameKonstante, "java/net/DatagramPacket")) { kategorieKode = 16; gültigLänge = 4; }
        if (maschinenwortText(nameKonstante, "java/lang/Thread") || maschinenwortText(nameKonstante, "Deutsch/eigen/hintergrundarbeiter")) { kategorieKode = 13; gültigLänge = 2; }
        if (maschinenwortText(nameKonstante, "java/lang/Object")) { kategorieKode = 8; }
        if (kategorieKode == 0 && bildschirmKlasse(nameKonstante) != 0) { kategorieKode = bildschirmKlasse(nameKonstante); gültigLänge = 12; }
        if (kategorieKode == 0) {
            int zeichenKode = klasseDefinitionFinden(nameKonstante); if (zeichenKode < 0 || fehler || !initialisieren(zeichenKode, beginnendPunkt)) return;
            kategorieKode = 32 + zeichenKode; gültigLänge = klassePlatzAnzahl[zeichenKode];
        }
        int objektVerweis = speichergerätZuteilen(kategorieKode, gültigLänge); if (fehler) return;
        if (kategorieKode == 13 && maschinenwortText(nameKonstante, "Deutsch/eigen/hintergrundarbeiter")) speicherhaldeWert[objektVerweis + 3] = 1;
        if (kategorieKode >= 24 && kategorieKode <= 28 && koreanischBildschirmKlasse(nameKonstante) != 0) speicherhaldeWert[objektVerweis + 13] = 1;
        if (kategorieKode == 5 || kategorieKode == 6 || kategorieKode == 15 || kategorieKode == 17 || kategorieKode == 18) speicherhaldeWert[objektVerweis + 2] = -1;
        if (kategorieKode == 9) speicherhaldeWert[objektVerweis + 2] = ausnahmeVerweis;
        wertAblegen(objektVerweis, 2);
    }
    static boolean werteGleich(int ersterDaten, int byteDaten) {
        if (ersterDaten == byteDaten) return true;
        if (ersterDaten == 0 || byteDaten == 0 || ersterDaten < 0 || byteDaten < 0 || ersterDaten >= speicherhaldeEndePosition || byteDaten >= speicherhaldeEndePosition) return false;
        if (speicherhaldeWert[ersterDaten] == 1 && speicherhaldeWert[byteDaten] == 1) return texteGleich(ersterDaten, byteDaten, false);
        return speicherhaldeWert[ersterDaten] == 12 && speicherhaldeWert[byteDaten] == 12 && speicherhaldeWert[ersterDaten + 2] == speicherhaldeWert[byteDaten + 2];
    }
    static int textFragment(int objektVerweis, int positionStarten, int endePosition) {
        if (!objektWert(objektVerweis, 1)) return 0;
        if (positionStarten < 0 || endePosition < positionStarten || endePosition > speicherhaldeWert[objektVerweis + 1]) { fehlschlagWert("StringIndexOutOfBoundsException"); return 0; }
        int zurückgegebenWert = speichergerätZuteilen(1, endePosition - positionStarten); if (fehler) return 0;
        for (int schleifeIndex = positionStarten; schleifeIndex < endePosition; schleifeIndex++) speicherhaldeWert[zurückgegebenWert + 2 + schleifeIndex - positionStarten] = speicherhaldeWert[objektVerweis + 2 + schleifeIndex];
        return zurückgegebenWert;
    }
    static int textZusammenführen(int ersterDaten, int byteDaten) {
        if (!objektWert(ersterDaten, 1) || !objektWert(byteDaten, 1)) return 0;
        int eintragAnzahl = speicherhaldeWert[ersterDaten + 1], methodeIndex = speicherhaldeWert[byteDaten + 1], zurückgegebenWert = speichergerätZuteilen(1, eintragAnzahl + methodeIndex); if (fehler) return 0;
        for (int schleifeIndex = 0; schleifeIndex < eintragAnzahl; schleifeIndex++) speicherhaldeWert[zurückgegebenWert + 2 + schleifeIndex] = speicherhaldeWert[ersterDaten + 2 + schleifeIndex];
        for (int schleifeIndex = 0; schleifeIndex < methodeIndex; schleifeIndex++) speicherhaldeWert[zurückgegebenWert + 2 + eintragAnzahl + schleifeIndex] = speicherhaldeWert[byteDaten + 2 + schleifeIndex];
        return zurückgegebenWert;
    }
    static boolean standardwertAufrufen(int eigentümer, int nameKonstante, int deskriptorKonstante, int befehlKode) {
        if (maschinenwortText(eigentümer, "Deutsch/eigen/Argumente") && befehlKode == 184) {
            if (maschinenwortText(nameKonstante, "elementeintragAnzahl") && maschinenwortText(deskriptorKonstante, "()I")) { wertAblegen(Benutzer.argumenteAnzahl() - 1, 1); return true; }
            if (maschinenwortText(nameKonstante, "Text") && maschinenwortText(deskriptorKonstante, "(I)Ljava/lang/String;")) {
                int ordnungszahlIndex = werteSubtrahieren(1);
                if (ordnungszahlIndex < 0 || ordnungszahlIndex >= Benutzer.argumenteAnzahl() - 1) ausnahmeAuslösen(29, "befehlAusführen argumente 범위를 벗어났습니다");
                else wertAblegen(wirtssystemZeichen(Benutzer.argumente(ordnungszahlIndex + 1)), 2);
                return true;
            }
            fehlschlagWert("지원하지 않는 Deutsch befehlAusführen argumente aufrufen"); return true;
        }
        if (maschinenwortText(eigentümer, "Deutsch/eigen/hintergrundarbeiter")) { prozessAusführungsfaden(nameKonstante, deskriptorKonstante, befehlKode, true); return true; }
        if (koreanischBildschirmEigentümer(eigentümer)) { koreanischBildschirmAufrufen(eigentümer, nameKonstante, deskriptorKonstante, befehlKode); return true; }
        if (bildschirmEigentümer(eigentümer)) { bildschirmAufrufen(eigentümer, nameKonstante, deskriptorKonstante, befehlKode); return true; }
        if (maschinenwortText(eigentümer, "java/net/Socket") || maschinenwortText(eigentümer, "java/net/ServerSocket") || maschinenwortText(eigentümer, "java/io/InputStream") || maschinenwortText(eigentümer, "java/io/OutputStream")) { datenstromAufrufen(eigentümer, nameKonstante, deskriptorKonstante, befehlKode); return true; }
        if (maschinenwortText(eigentümer, "Deutsch/eigen/betriebskernWert") && befehlKode == 184) {
            if (maschinenwortText(nameKonstante, "bildschirmBreite") && maschinenwortText(deskriptorKonstante, "()I")) { wertAblegen(Benutzer.bildschirmBreite(), 1); return true; }
            if (maschinenwortText(nameKonstante, "bildschirmHöhe") && maschinenwortText(deskriptorKonstante, "()I")) { wertAblegen(Benutzer.bildschirmHöhe(), 1); return true; }
            if (maschinenwortText(nameKonstante, "millisekunden") && maschinenwortText(deskriptorKonstante, "()I")) { wertAblegen(Benutzer.millisekunden(), 1); return true; }
            if (maschinenwortText(nameKonstante, "fürAbbildWarten") && maschinenwortText(deskriptorKonstante, "()I")) { wertAblegen(Benutzer.fürAbbildWarten(), 1); return true; }
            if (maschinenwortText(nameKonstante, "rechteck") && maschinenwortText(deskriptorKonstante, "(IIIII)I")) { int bildpunktFarbe = werteSubtrahieren(1), höheWert = werteSubtrahieren(1), breiteWert = werteSubtrahieren(1), senkrechteKoordinateKoordinate = werteSubtrahieren(1), waagerechteKoordinateKoordinate = werteSubtrahieren(1); wertAblegen(Benutzer.rechteck(waagerechteKoordinateKoordinate, senkrechteKoordinateKoordinate, breiteWert, höheWert, bildpunktFarbe), 1); return true; }
        }
        if (maschinenwortText(eigentümer, "java/net/InetAddress") || maschinenwortText(eigentümer, "java/net/DatagramPacket") || maschinenwortText(eigentümer, "java/net/DatagramSocket")) { netzwerkAufrufen(eigentümer, nameKonstante, deskriptorKonstante, befehlKode); return true; }
        if (maschinenwortText(eigentümer, "java/lang/Thread")) { ausführungsfadenAufrufen(nameKonstante, deskriptorKonstante, befehlKode); return true; }
        if (maschinenwortText(eigentümer, "java/lang/Object")) {
            if (maschinenwortText(nameKonstante, "<init>") && maschinenwortText(deskriptorKonstante, "()V") && befehlKode == 183) { istGültigObjekt(werteSubtrahieren(2)); return true; }
            if (maschinenwortText(nameKonstante, "equals") && maschinenwortText(deskriptorKonstante, "(Ljava/lang/Object;)Z")) { int byteDaten = werteSubtrahieren(2), ersterDaten = werteSubtrahieren(2); if (istGültigObjekt(ersterDaten)) wertAblegen(ersterDaten == byteDaten ? 1 : 0, 1); return true; }
        }
        if (ausnahmeKonstante(eigentümer) != 0) {
            if (maschinenwortText(nameKonstante, "<init>") && befehlKode == 183 && (maschinenwortText(deskriptorKonstante, "()V") || maschinenwortText(deskriptorKonstante, "(Ljava/lang/String;)V"))) {
                int eingabeaufforderung = maschinenwortText(deskriptorKonstante, "()V") ? 0 : werteSubtrahieren(2), objektVerweis = werteSubtrahieren(2);
                if (objektWert(objektVerweis, 9)) { speicherhaldeWert[objektVerweis + 3] = eingabeaufforderung; speicherhaldeVerweis[objektVerweis + 3] = 1; } return true;
            }
            if ((maschinenwortText(nameKonstante, "getMessage") || maschinenwortText(nameKonstante, "beschreibung")) && maschinenwortText(deskriptorKonstante, "()Ljava/lang/String;")) { int objektVerweis = werteSubtrahieren(2); if (objektWert(objektVerweis, 9)) wertAblegen(speicherhaldeWert[objektVerweis + 3], 2); return true; }
        }
        if (maschinenwortText(eigentümer, "java/lang/String")) {
            if (befehlKode == 182 && maschinenwortText(nameKonstante, "getBytes") && (maschinenwortText(deskriptorKonstante, "()[B") || maschinenwortText(deskriptorKonstante, "(Ljava/lang/String;)[B"))) {
                int kodierungName = maschinenwortText(deskriptorKonstante, "()[B") ? 0 : werteSubtrahieren(2), objektVerweis = werteSubtrahieren(2);
                if (!objektWert(objektVerweis, 1)) return true;
                if (kodierungName != 0 && !texteGleich(kodierungName, wirtssystemZeichen("UTF-8"), false) && !texteGleich(kodierungName, wirtssystemZeichen("UTF8"), false) && !texteGleich(kodierungName, wirtssystemZeichen("utf-8"), false)) { ausnahmeAuslösen(11, "only UTF-8 encoding is supported"); return true; }
                int eintragAnzahl = speicherhaldeWert[objektVerweis + 1], zurückgegebenWert = speichergerätZuteilen(20, eintragAnzahl * 3), benutztAnzahl = 0; if (fehler) return true;
                for (int innerlichPosition = 0; innerlichPosition < eintragAnzahl; innerlichPosition++) {
                    int zeichenKode = speicherhaldeWert[objektVerweis + 2 + innerlichPosition];
                    if (zeichenKode >= 0xd800 && zeichenKode <= 0xdbff && innerlichPosition + 1 < eintragAnzahl && speicherhaldeWert[objektVerweis + 3 + innerlichPosition] >= 0xdc00 && speicherhaldeWert[objektVerweis + 3 + innerlichPosition] <= 0xdfff) zeichenKode = 0x10000 + ((zeichenKode - 0xd800) << 10) + speicherhaldeWert[objektVerweis + 2 + ++innerlichPosition] - 0xdc00;
                    else if (zeichenKode >= 0xd800 && zeichenKode <= 0xdfff) zeichenKode = '?';
                    if (zeichenKode < 128) speicherhaldeWert[zurückgegebenWert + 2 + benutztAnzahl++] = zeichenKode;
                    else { int byteAnzahl = zeichenKode < 2048 ? 2 : zeichenKode < 65536 ? 3 : 4; speicherhaldeWert[zurückgegebenWert + 2 + benutztAnzahl++] = (byte)((byteAnzahl == 2 ? 192 : byteAnzahl == 3 ? 224 : 240) | zeichenKode >> (6 * (byteAnzahl - 1))); for (int vergleichPosition = byteAnzahl - 1; vergleichPosition > 0; vergleichPosition--) speicherhaldeWert[zurückgegebenWert + 2 + benutztAnzahl++] = (byte)(128 | zeichenKode >> (6 * (vergleichPosition - 1)) & 63); }
                }
                speicherhaldeWert[zurückgegebenWert + 1] = benutztAnzahl; wertAblegen(zurückgegebenWert, 2); return true;
            }
            if (befehlKode == 184 && maschinenwortText(nameKonstante, "valueOf") && maschinenwortText(deskriptorKonstante, "(I)Ljava/lang/String;")) { wertAblegen(zifferZeichen(werteSubtrahieren(1)), 2); return true; }
            if (befehlKode != 182) return false;
            if (maschinenwortText(nameKonstante, "equals") && maschinenwortText(deskriptorKonstante, "(Ljava/lang/Object;)Z")) { int byteDaten = werteSubtrahieren(2), ersterDaten = werteSubtrahieren(2); if (objektWert(ersterDaten, 1)) wertAblegen(texteGleich(ersterDaten, byteDaten, false) ? 1 : 0, 1); return true; }
            if (maschinenwortText(nameKonstante, "isEmpty") && maschinenwortText(deskriptorKonstante, "()Z")) { int ersterDaten = werteSubtrahieren(2); if (objektWert(ersterDaten, 1)) wertAblegen(speicherhaldeWert[ersterDaten + 1] == 0 ? 1 : 0, 1); return true; }
            if (maschinenwortText(nameKonstante, "substring") && (maschinenwortText(deskriptorKonstante, "(I)Ljava/lang/String;") || maschinenwortText(deskriptorKonstante, "(II)Ljava/lang/String;"))) {
                boolean zweiterWert = maschinenwortText(deskriptorKonstante, "(II)Ljava/lang/String;"); int endePosition = zweiterWert ? werteSubtrahieren(1) : 0, beginnendPunkt = werteSubtrahieren(1), ersterDaten = werteSubtrahieren(2);
                if (objektWert(ersterDaten, 1)) wertAblegen(textFragment(ersterDaten, beginnendPunkt, zweiterWert ? endePosition : speicherhaldeWert[ersterDaten + 1]), 2); return true;
            }
            if (maschinenwortText(nameKonstante, "concat") && maschinenwortText(deskriptorKonstante, "(Ljava/lang/String;)Ljava/lang/String;")) { int byteDaten = werteSubtrahieren(2), ersterDaten = werteSubtrahieren(2); wertAblegen(textZusammenführen(ersterDaten, byteDaten), 2); return true; }
            if (maschinenwortText(nameKonstante, "hashCode") && maschinenwortText(deskriptorKonstante, "()I")) { int ersterDaten = werteSubtrahieren(2), prüfsummeWert = 0; if (objektWert(ersterDaten, 1)) { for (int schleifeIndex = 0; schleifeIndex < speicherhaldeWert[ersterDaten + 1]; schleifeIndex++) prüfsummeWert = prüfsummeWert * 31 + speicherhaldeWert[ersterDaten + 2 + schleifeIndex]; wertAblegen(prüfsummeWert, 1); } return true; }
            if (maschinenwortText(nameKonstante, "toString") && maschinenwortText(deskriptorKonstante, "()Ljava/lang/String;")) { int ersterDaten = werteSubtrahieren(2); if (objektWert(ersterDaten, 1)) wertAblegen(ersterDaten, 2); return true; }
        }
        if (maschinenwortText(eigentümer, "java/lang/Integer")) {
            if (befehlKode == 184 && maschinenwortText(nameKonstante, "valueOf") && maschinenwortText(deskriptorKonstante, "(I)Ljava/lang/Integer;")) { int datenWert = werteSubtrahieren(1), objektVerweis = datenWert >= -128 && datenWert <= 127 ? ablegenDatenGanzzahl[datenWert + 128] : 0; if (objektVerweis == 0) { objektVerweis = speichergerätZuteilen(12, 1); if (!fehler) { speicherhaldeWert[objektVerweis + 2] = datenWert; if (datenWert >= -128 && datenWert <= 127) ablegenDatenGanzzahl[datenWert + 128] = objektVerweis; } } wertAblegen(objektVerweis, 2); return true; }
            if (befehlKode == 183 && maschinenwortText(nameKonstante, "<init>") && maschinenwortText(deskriptorKonstante, "(I)V")) { int datenWert = werteSubtrahieren(1), objektVerweis = werteSubtrahieren(2); if (objektWert(objektVerweis, 12)) speicherhaldeWert[objektVerweis + 2] = datenWert; return true; }
            if (befehlKode == 182 && maschinenwortText(nameKonstante, "intValue") && maschinenwortText(deskriptorKonstante, "()I")) { int objektVerweis = werteSubtrahieren(2); if (objektWert(objektVerweis, 12)) wertAblegen(speicherhaldeWert[objektVerweis + 2], 1); return true; }
            if (befehlKode == 184 && maschinenwortText(nameKonstante, "toString") && maschinenwortText(deskriptorKonstante, "(I)Ljava/lang/String;")) { wertAblegen(zifferZeichen(werteSubtrahieren(1)), 2); return true; }
        }
        if (maschinenwortText(eigentümer, "java/lang/Math") && befehlKode == 184) {
            if (maschinenwortText(nameKonstante, "abs") && maschinenwortText(deskriptorKonstante, "(I)I")) { int wertLesen = werteSubtrahieren(1); wertAblegen(wertLesen < 0 ? -wertLesen : wertLesen, 1); return true; }
            if ((maschinenwortText(nameKonstante, "min") || maschinenwortText(nameKonstante, "max")) && maschinenwortText(deskriptorKonstante, "(II)I")) { int byteDaten = werteSubtrahieren(1), ersterDaten = werteSubtrahieren(1); wertAblegen(maschinenwortText(nameKonstante, "min") ? (ersterDaten < byteDaten ? ersterDaten : byteDaten) : (ersterDaten > byteDaten ? ersterDaten : byteDaten), 1); return true; }
        }
        if (maschinenwortText(eigentümer, "java/lang/System") && befehlKode == 184) {
            if (maschinenwortText(nameKonstante, "gc") && maschinenwortText(deskriptorKonstante, "()V")) { abfallEinsammeln(); return true; }
            if (maschinenwortText(nameKonstante, "arraycopy") && maschinenwortText(deskriptorKonstante, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int eintragAnzahl = werteSubtrahieren(1), zielWertIndex = werteSubtrahieren(1), byteDaten = werteSubtrahieren(2), positionStarten = werteSubtrahieren(1), ersterDaten = werteSubtrahieren(2);
                if (istGültigObjekt(ersterDaten) && istGültigObjekt(byteDaten)) {
                    int kategorieKode = speicherhaldeWert[ersterDaten];
                    if (speicherhaldeWert[byteDaten] != kategorieKode || (kategorieKode != 2 && kategorieKode != 3 && (kategorieKode < 20 || kategorieKode > 23))) fehlschlagWert("arraycopy type mismatch");
                    else if (eintragAnzahl < 0 || positionStarten < 0 || zielWertIndex < 0 || positionStarten > speicherhaldeWert[ersterDaten + 1] - eintragAnzahl || zielWertIndex > speicherhaldeWert[byteDaten + 1] - eintragAnzahl) fehlschlagWert("ArrayIndexOutOfBoundsException");
                    else if (ersterDaten == byteDaten && zielWertIndex > positionStarten) { for (int schleifeIndex = eintragAnzahl - 1; schleifeIndex >= 0; schleifeIndex--) speicherhaldeWert[byteDaten + 2 + zielWertIndex + schleifeIndex] = speicherhaldeWert[ersterDaten + 2 + positionStarten + schleifeIndex]; }
                    else { for (int schleifeIndex = 0; schleifeIndex < eintragAnzahl && !fehler; schleifeIndex++) { int datenWert = speicherhaldeWert[ersterDaten + 2 + positionStarten + schleifeIndex]; if (kategorieKode != 3 || kannAblegenDatenDatenfeld(byteDaten, datenWert)) speicherhaldeWert[byteDaten + 2 + zielWertIndex + schleifeIndex] = datenWert; } }
                }
                return true;
            }
        }
        if (maschinenwortText(eigentümer, "java/util/ArrayList") || maschinenwortText(eigentümer, "java/util/List") || maschinenwortText(eigentümer, "java/util/HashMap") || maschinenwortText(eigentümer, "java/util/Map")) {
            sammlungAufrufen(eigentümer, nameKonstante, deskriptorKonstante, befehlKode); return true;
        }
        return false;
    }
    static void sammlungErweitern(int objektVerweis, int erforderlichAnzahl) {
        int vorherigWert = speicherhaldeWert[objektVerweis + 2], kapazitätDaten = vorherigWert == 0 ? 0 : speicherhaldeWert[vorherigWert + 1];
        if (kapazitätDaten >= erforderlichAnzahl) return;
        int nächsterPosition = kapazitätDaten < 8 ? 8 : kapazitätDaten * 2; if (nächsterPosition < erforderlichAnzahl) nächsterPosition = erforderlichAnzahl;
        int datenDatenfeld = speichergerätZuteilen(3, nächsterPosition); if (fehler) return;
        for (int schleifeIndex = 0; schleifeIndex < kapazitätDaten; schleifeIndex++) speicherhaldeWert[datenDatenfeld + 2 + schleifeIndex] = speicherhaldeWert[vorherigWert + 2 + schleifeIndex];
        speicherhaldeWert[objektVerweis + 2] = datenDatenfeld; speicherhaldeVerweis[objektVerweis + 2] = 1;
    }
    static void sammlungAufrufen(int eigentümer, int nameKonstante, int deskriptorKonstante, int befehlKode) {
        boolean zugeordnetVerweis = maschinenwortText(eigentümer, "java/util/HashMap") || maschinenwortText(eigentümer, "java/util/Map"); int kategorieKode = zugeordnetVerweis ? 11 : 10;
        if (maschinenwortText(nameKonstante, "<init>") && befehlKode == 183 && maschinenwortText(deskriptorKonstante, "()V")) { int objektVerweis = werteSubtrahieren(2); if (objektWert(objektVerweis, kategorieKode)) sammlungErweitern(objektVerweis, 8); return; }
        if (befehlKode != 182 && befehlKode != 185) { fehlschlagWert("invalid collection invocation"); return; }
        if (maschinenwortText(nameKonstante, "size") && maschinenwortText(deskriptorKonstante, "()I") || maschinenwortText(nameKonstante, "isEmpty") && maschinenwortText(deskriptorKonstante, "()Z")) {
            int objektVerweis = werteSubtrahieren(2); if (objektWert(objektVerweis, kategorieKode)) wertAblegen(maschinenwortText(nameKonstante, "size") ? speicherhaldeWert[objektVerweis + 3] : speicherhaldeWert[objektVerweis + 3] == 0 ? 1 : 0, 1); return;
        }
        if (maschinenwortText(nameKonstante, "clear") && maschinenwortText(deskriptorKonstante, "()V")) { int objektVerweis = werteSubtrahieren(2); if (objektWert(objektVerweis, kategorieKode)) { int datenDatenfeld = speicherhaldeWert[objektVerweis + 2]; for (int schleifeIndex = 0; schleifeIndex < speicherhaldeWert[datenDatenfeld + 1]; schleifeIndex++) speicherhaldeWert[datenDatenfeld + 2 + schleifeIndex] = 0; speicherhaldeWert[objektVerweis + 3] = 0; } return; }
        if (!zugeordnetVerweis && maschinenwortText(nameKonstante, "add") && maschinenwortText(deskriptorKonstante, "(Ljava/lang/Object;)Z")) {
            int datenWert = werteSubtrahieren(2), objektVerweis = werteSubtrahieren(2); if (!objektWert(objektVerweis, 10)) return;
            int eintragAnzahl = speicherhaldeWert[objektVerweis + 3]; sammlungErweitern(objektVerweis, eintragAnzahl + 1); if (!fehler) { speicherhaldeWert[speicherhaldeWert[objektVerweis + 2] + 2 + eintragAnzahl] = datenWert; speicherhaldeWert[objektVerweis + 3] = eintragAnzahl + 1; wertAblegen(1, 1); } return;
        }
        if (!zugeordnetVerweis && (maschinenwortText(nameKonstante, "get") || maschinenwortText(nameKonstante, "remove")) && maschinenwortText(deskriptorKonstante, "(I)Ljava/lang/Object;") || !zugeordnetVerweis && maschinenwortText(nameKonstante, "set") && maschinenwortText(deskriptorKonstante, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean istZugewiesen = maschinenwortText(nameKonstante, "set"); int datenWert = istZugewiesen ? werteSubtrahieren(2) : 0, eintragPosition = werteSubtrahieren(1), objektVerweis = werteSubtrahieren(2);
            if (!objektWert(objektVerweis, 10)) return;
            int eintragAnzahl = speicherhaldeWert[objektVerweis + 3], datenDatenfeld = speicherhaldeWert[objektVerweis + 2];
            if (eintragPosition < 0 || eintragPosition >= eintragAnzahl) { ausnahmeAuslösen(6, "list index"); return; }
            int vorherigWert = speicherhaldeWert[datenDatenfeld + 2 + eintragPosition];
            if (istZugewiesen) speicherhaldeWert[datenDatenfeld + 2 + eintragPosition] = datenWert;
            if (maschinenwortText(nameKonstante, "remove")) { for (int schleifeIndex = eintragPosition + 1; schleifeIndex < eintragAnzahl; schleifeIndex++) speicherhaldeWert[datenDatenfeld + 1 + schleifeIndex] = speicherhaldeWert[datenDatenfeld + 2 + schleifeIndex]; speicherhaldeWert[datenDatenfeld + 1 + eintragAnzahl] = 0; speicherhaldeWert[objektVerweis + 3] = eintragAnzahl - 1; }
            wertAblegen(vorherigWert, 2); return;
        }
        if (zugeordnetVerweis && (maschinenwortText(nameKonstante, "get") || maschinenwortText(nameKonstante, "remove")) && maschinenwortText(deskriptorKonstante, "(Ljava/lang/Object;)Ljava/lang/Object;") || zugeordnetVerweis && maschinenwortText(nameKonstante, "put") && maschinenwortText(deskriptorKonstante, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || zugeordnetVerweis && maschinenwortText(nameKonstante, "containsKey") && maschinenwortText(deskriptorKonstante, "(Ljava/lang/Object;)Z")) {
            boolean istEinfügung = maschinenwortText(nameKonstante, "put"), entfernen = maschinenwortText(nameKonstante, "remove");
            int datenWert = istEinfügung ? werteSubtrahieren(2) : 0, tasteVerweis = werteSubtrahieren(2), objektVerweis = werteSubtrahieren(2); if (!objektWert(objektVerweis, 11)) return;
            int eintragAnzahl = speicherhaldeWert[objektVerweis + 3], datenDatenfeld = speicherhaldeWert[objektVerweis + 2], warGefunden = -1;
            for (int schleifeIndex = 0; schleifeIndex < eintragAnzahl; schleifeIndex++) if (werteGleich(tasteVerweis, speicherhaldeWert[datenDatenfeld + 2 + 2 * schleifeIndex])) { warGefunden = schleifeIndex; break; }
            int vorherigWert = warGefunden < 0 ? 0 : speicherhaldeWert[datenDatenfeld + 3 + 2 * warGefunden];
            if (istEinfügung) {
                if (warGefunden < 0) { sammlungErweitern(objektVerweis, (eintragAnzahl + 1) * 2); datenDatenfeld = speicherhaldeWert[objektVerweis + 2]; warGefunden = eintragAnzahl; if (!fehler) speicherhaldeWert[objektVerweis + 3] = eintragAnzahl + 1; }
                if (!fehler) { speicherhaldeWert[datenDatenfeld + 2 + 2 * warGefunden] = tasteVerweis; speicherhaldeWert[datenDatenfeld + 3 + 2 * warGefunden] = datenWert; }
            }
            if (entfernen && warGefunden >= 0) { for (int schleifeIndex = warGefunden + 1; schleifeIndex < eintragAnzahl; schleifeIndex++) { speicherhaldeWert[datenDatenfeld + 2 * schleifeIndex] = speicherhaldeWert[datenDatenfeld + 2 + 2 * schleifeIndex]; speicherhaldeWert[datenDatenfeld + 1 + 2 * schleifeIndex] = speicherhaldeWert[datenDatenfeld + 3 + 2 * schleifeIndex]; } speicherhaldeWert[datenDatenfeld + 2 * eintragAnzahl] = 0; speicherhaldeWert[datenDatenfeld + 1 + 2 * eintragAnzahl] = 0; speicherhaldeWert[objektVerweis + 3] = eintragAnzahl - 1; }
            if (maschinenwortText(nameKonstante, "containsKey")) wertAblegen(warGefunden >= 0 ? 1 : 0, 1); else wertAblegen(vorherigWert, 2);
            return;
        }
        fehlschlagWert("unsupported collection method");
    }
    static boolean sperreErwerben(int objektVerweis) {
        if (!istGültigObjekt(objektVerweis)) return false;
        if (sperreTiefe[objektVerweis] != 0 && sperreEigentümer[objektVerweis] != aktuellAusführungsfaden + 1) { anfrageÄndern = true; return false; }
        sperreEigentümer[objektVerweis] = aktuellAusführungsfaden + 1; sperreTiefe[objektVerweis]++; return true;
    }
    static void sperreFreigeben(int objektVerweis) {
        if (!istGültigObjekt(objektVerweis)) return;
        if (sperreTiefe[objektVerweis] == 0 || sperreEigentümer[objektVerweis] != aktuellAusführungsfaden + 1) { ausnahmeAuslösen(13, "monitor not owned"); return; }
        if (--sperreTiefe[objektVerweis] == 0) sperreEigentümer[objektVerweis] = 0;
    }
    static boolean umschaltenAusführungsfaden() {
        ausführungsfadenRahmen[aktuellAusführungsfaden] = rahmenIndex;
        if (rahmenIndex < aktuellAusführungsfaden * 32) ausführungsfadenStatuswert[aktuellAusführungsfaden] = 3;
        for (int schleifeIndex = 0; schleifeIndex < ausführungsfadenAnzahl; schleifeIndex++) if (ausführungsfadenStatuswert[schleifeIndex] == 2 && ausführungsfadenStatuswert[fürAusführungsfadenWarten[schleifeIndex]] == 3) ausführungsfadenStatuswert[schleifeIndex] = 1;
        for (int schleifeIndex = 1; schleifeIndex <= ausführungsfadenAnzahl; schleifeIndex++) {
            int nächsterPosition = (aktuellAusführungsfaden + schleifeIndex) % ausführungsfadenAnzahl;
            if (ausführungsfadenStatuswert[nächsterPosition] == 1) { aktuellAusführungsfaden = nächsterPosition; rahmenIndex = ausführungsfadenRahmen[nächsterPosition]; anfrageÄndern = false; return true; }
        }
        for (int schleifeIndex = 0; schleifeIndex < ausführungsfadenAnzahl; schleifeIndex++) if (ausführungsfadenStatuswert[schleifeIndex] != 3) { fehlschlagWert("thread deadlock"); return false; }
        return false;
    }
    static void ausführungsfadenAufrufen(int nameKonstante, int deskriptorKonstante, int befehlKode) { prozessAusführungsfaden(nameKonstante, deskriptorKonstante, befehlKode, false); }
    static void prozessAusführungsfaden(int nameKonstante, int deskriptorKonstante, int befehlKode, boolean Deutsch) {
        if (befehlKode == 184 && maschinenwortText(nameKonstante, Deutsch ? "aufgabeAbgeben" : "yield") && maschinenwortText(deskriptorKonstante, "()V")) { anfrageÄndern = true; return; }
        if (befehlKode == 184 && maschinenwortText(nameKonstante, "currentThread") && maschinenwortText(deskriptorKonstante, "()Ljava/lang/Thread;")) { wertAblegen(ausführungsfadenObjekt[aktuellAusführungsfaden], 2); return; }
        if (befehlKode == 183 && maschinenwortText(nameKonstante, "<init>") && (maschinenwortText(deskriptorKonstante, "()V") || maschinenwortText(deskriptorKonstante, Deutsch ? "(LDeutsch/eigen/AusführbarAufgabe;)V" : "(Ljava/lang/Runnable;)V"))) {
            int zielobjektAdresse = maschinenwortText(deskriptorKonstante, "()V") ? 0 : werteSubtrahieren(2), objektVerweis = werteSubtrahieren(2);
            if (!istGültigObjekt(objektVerweis)) return;
            if (speicherhaldeWert[objektVerweis] == 13) { speicherhaldeWert[objektVerweis + 2] = zielobjektAdresse; speicherhaldeVerweis[objektVerweis + 2] = 1; }
            else if (zielobjektAdresse != 0) fehlschlagWert("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (befehlKode == 182 && (maschinenwortText(nameKonstante, Deutsch ? "aufgabeStarten" : "start") || maschinenwortText(nameKonstante, Deutsch ? "abwarten" : "join")) && maschinenwortText(deskriptorKonstante, "()V") || befehlKode == 182 && maschinenwortText(nameKonstante, Deutsch ? "istLebendig" : "isAlive") && maschinenwortText(deskriptorKonstante, "()Z")) {
            int objektVerweis = werteSubtrahieren(2); if (!istGültigObjekt(objektVerweis)) return;
            int identitätWert = -1; for (int schleifeIndex = 0; schleifeIndex < ausführungsfadenAnzahl; schleifeIndex++) if (ausführungsfadenObjekt[schleifeIndex] == objektVerweis) identitätWert = schleifeIndex;
            if (maschinenwortText(nameKonstante, Deutsch ? "istLebendig" : "isAlive")) { wertAblegen(identitätWert >= 0 && ausführungsfadenStatuswert[identitätWert] != 3 ? 1 : 0, 1); return; }
            if (maschinenwortText(nameKonstante, Deutsch ? "abwarten" : "join")) { if (identitätWert >= 0 && ausführungsfadenStatuswert[identitätWert] != 3) { fürAusführungsfadenWarten[aktuellAusführungsfaden] = identitätWert; ausführungsfadenStatuswert[aktuellAusführungsfaden] = 2; anfrageÄndern = true; } return; }
            if (identitätWert >= 0) { ausnahmeAuslösen(Deutsch ? 38 : 16, "thread already started"); return; }
            if (ausführungsfadenAnzahl == 4) { fehlschlagWert("thread limit (4 including main)"); return; }
            int zielobjektAdresse = speicherhaldeWert[objektVerweis] == 13 ? speicherhaldeWert[objektVerweis + 2] : objektVerweis;
            int dateiIndex = zielobjektAdresse > 0 && speicherhaldeWert[zielobjektAdresse] >= 32 ? nameMethode(speicherhaldeWert[zielobjektAdresse] - 32, Deutsch ? "aufgabeAusführen" : "run", "()V") : -1;
            if (zielobjektAdresse != 0 && dateiIndex < 0) { fehlschlagWert("Runnable.run required"); return; }
            identitätWert = ausführungsfadenAnzahl++; ausführungsfadenObjekt[identitätWert] = objektVerweis; ausführungsfadenZielobjekt[identitätWert] = zielobjektAdresse;
            int rahmen = identitätWert * 32; ausführungsfadenRahmen[identitätWert] = dateiIndex < 0 ? rahmen - 1 : rahmen; ausführungsfadenStatuswert[identitätWert] = dateiIndex < 0 ? 3 : 1;
            if (dateiIndex >= 0) { rahmenMethode[rahmen] = dateiIndex; rahmenPosition[rahmen] = methodeStarten[dateiIndex]; lokalWert[rahmen * 128] = zielobjektAdresse; lokalTyp[rahmen * 128] = 2; }
            return;
        }
        fehlschlagWert("unsupported Thread method");
    }
    static int[] netzwerkVorläufigWert = new int[514], adresseText = new int[16];
    static int lokalAdresse() { return adresseObjekt(0x7f000001); }
    static int adresseObjekt(int Wert) { int objektVerweis = speichergerätZuteilen(14, 1); if (!fehler) speicherhaldeWert[objektVerweis + 2] = Wert; return objektVerweis; }
    static int adresseDekodieren(int objektVerweis) {
        if (objektVerweis == 0 || texteGleich(objektVerweis, wirtssystemZeichen("localhost"), false)) return 0x7f000001;
        if (!objektWert(objektVerweis, 1)) return 0;
        int datenWert = 0, gesamtwertAnzahl = 0, adresseByte = 0, ziffern = 0, eintragAnzahl = speicherhaldeWert[objektVerweis + 1];
        for (int schleifeIndex = 0; schleifeIndex <= eintragAnzahl; schleifeIndex++) {
            int zeichenKode = schleifeIndex == eintragAnzahl ? '.' : speicherhaldeWert[objektVerweis + 2 + schleifeIndex];
            if (zeichenKode == '.') { if (ziffern == 0 || gesamtwertAnzahl == 4) { ausnahmeAuslösen(18, "numeric IPv4 address required; DNS unavailable"); return 0; } datenWert = datenWert << 8 | adresseByte; gesamtwertAnzahl++; adresseByte = ziffern = 0; }
            else { if (zeichenKode < '0' || zeichenKode > '9' || ++ziffern > 3 || (adresseByte = adresseByte * 10 + zeichenKode - '0') > 255) { ausnahmeAuslösen(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (gesamtwertAnzahl != 4) { ausnahmeAuslösen(18, "invalid IPv4 address"); return 0; } return datenWert;
    }
    static int adresseZeichen(int datenWert) {
        int eintragAnzahl = 0;
        for (int verschieben = 24; verschieben >= 0; verschieben -= 8) {
            int adresseByte = datenWert >>> verschieben & 255;
            if (adresseByte >= 100) adresseText[eintragAnzahl++] = '0' + adresseByte / 100;
            if (adresseByte >= 10) adresseText[eintragAnzahl++] = '0' + adresseByte / 10 % 10;
            adresseText[eintragAnzahl++] = '0' + adresseByte % 10; if (verschieben != 0) adresseText[eintragAnzahl++] = '.';
        }
        int objektVerweis = speichergerätZuteilen(1, eintragAnzahl); if (!fehler) for (int schleifeIndex = 0; schleifeIndex < eintragAnzahl; schleifeIndex++) speicherhaldeWert[objektVerweis + 2 + schleifeIndex] = adresseText[schleifeIndex]; return objektVerweis;
    }
    static void netzwerkAufrufen(int eigentümer, int nameKonstante, int deskriptorKonstante, int befehlKode) {
        if (maschinenwortText(eigentümer, "java/net/InetAddress")) {
            if (befehlKode == 184 && maschinenwortText(nameKonstante, "getLoopbackAddress") && maschinenwortText(deskriptorKonstante, "()Ljava/net/InetAddress;")) { wertAblegen(lokalAdresse(), 2); return; }
            if (befehlKode == 184 && maschinenwortText(nameKonstante, "getByName") && maschinenwortText(deskriptorKonstante, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int datenWert = adresseDekodieren(werteSubtrahieren(2)); if (ausgelöstObjekt == 0 && !fehler) wertAblegen(adresseObjekt(datenWert), 2); return;
            }
            if (befehlKode == 182 && maschinenwortText(nameKonstante, "getHostAddress") && maschinenwortText(deskriptorKonstante, "()Ljava/lang/String;")) { int objektVerweis = werteSubtrahieren(2); if (objektWert(objektVerweis, 14)) wertAblegen(adresseZeichen(speicherhaldeWert[objektVerweis + 2]), 2); return; }
        }
        if (maschinenwortText(eigentümer, "java/net/DatagramPacket")) {
            if (befehlKode == 183 && maschinenwortText(nameKonstante, "<init>") && (maschinenwortText(deskriptorKonstante, "([BI)V") || maschinenwortText(deskriptorKonstante, "([BILjava/net/InetAddress;I)V"))) {
                boolean zielWertVerweis = maschinenwortText(deskriptorKonstante, "([BILjava/net/InetAddress;I)V"); int portNummer = zielWertVerweis ? werteSubtrahieren(1) : 0, adresseVerweis = zielWertVerweis ? werteSubtrahieren(2) : 0;
                int eintragAnzahl = werteSubtrahieren(1), datenDatenfeld = werteSubtrahieren(2), objektVerweis = werteSubtrahieren(2);
                if (!objektWert(objektVerweis, 16) || !objektWert(datenDatenfeld, 20)) return;
                if (eintragAnzahl < 0 || eintragAnzahl > speicherhaldeWert[datenDatenfeld + 1] || portNummer < 0 || portNummer > 65535) { ausnahmeAuslösen(9, "invalid datagram length/port"); return; }
                if (adresseVerweis != 0 && !objektWert(adresseVerweis, 14)) return;
                speicherhaldeWert[objektVerweis + 2] = datenDatenfeld; speicherhaldeVerweis[objektVerweis + 2] = 1; speicherhaldeWert[objektVerweis + 3] = eintragAnzahl;
                speicherhaldeWert[objektVerweis + 4] = adresseVerweis; speicherhaldeVerweis[objektVerweis + 4] = 1; speicherhaldeWert[objektVerweis + 5] = portNummer; return;
            }
            if (befehlKode == 182 && maschinenwortText(nameKonstante, "setLength") && maschinenwortText(deskriptorKonstante, "(I)V")) {
                int eintragAnzahl = werteSubtrahieren(1), objektVerweis = werteSubtrahieren(2); if (!objektWert(objektVerweis, 16)) return;
                if (eintragAnzahl < 0 || eintragAnzahl > speicherhaldeWert[speicherhaldeWert[objektVerweis + 2] + 1]) ausnahmeAuslösen(9, "invalid datagram length"); else speicherhaldeWert[objektVerweis + 3] = eintragAnzahl; return;
            }
            if (befehlKode == 182 && (maschinenwortText(nameKonstante, "getData") && maschinenwortText(deskriptorKonstante, "()[B") || maschinenwortText(nameKonstante, "getLength") && maschinenwortText(deskriptorKonstante, "()I") || maschinenwortText(nameKonstante, "getAddress") && maschinenwortText(deskriptorKonstante, "()Ljava/net/InetAddress;") || maschinenwortText(nameKonstante, "getPort") && maschinenwortText(deskriptorKonstante, "()I"))) {
                int objektVerweis = werteSubtrahieren(2); if (!objektWert(objektVerweis, 16)) return;
                int eintragPosition = maschinenwortText(nameKonstante, "getData") ? 2 : maschinenwortText(nameKonstante, "getLength") ? 3 : maschinenwortText(nameKonstante, "getAddress") ? 4 : 5;
                wertAblegen(speicherhaldeWert[objektVerweis + eintragPosition], eintragPosition == 2 || eintragPosition == 4 ? 2 : 1); return;
            }
        }
        if (maschinenwortText(eigentümer, "java/net/DatagramSocket")) {
            if (befehlKode == 183 && maschinenwortText(nameKonstante, "<init>") && (maschinenwortText(deskriptorKonstante, "()V") || maschinenwortText(deskriptorKonstante, "(I)V"))) {
                int portNummer = maschinenwortText(deskriptorKonstante, "()V") ? 0 : werteSubtrahieren(1), objektVerweis = werteSubtrahieren(2); if (!objektWert(objektVerweis, 15)) return;
                if (portNummer < 0 || portNummer > 65535) { ausnahmeAuslösen(9, "invalid port"); return; }
                int geöffnetDateiNummer = Benutzer.netzwerkÖffnen(portNummer); if (geöffnetDateiNummer < 0) ausnahmeAuslösen(39, "UDP socket/bind failed"); else speicherhaldeWert[objektVerweis + 2] = geöffnetDateiNummer; return;
            }
            if (befehlKode == 182 && maschinenwortText(nameKonstante, "setSoTimeout") && maschinenwortText(deskriptorKonstante, "(I)V")) {
                int millisekundenWert = werteSubtrahieren(1), objektVerweis = werteSubtrahieren(2); if (!objektWert(objektVerweis, 15)) return;
                if (millisekundenWert < 0) ausnahmeAuslösen(9, "negative timeout"); else speicherhaldeWert[objektVerweis + 3] = millisekundenWert; return;
            }
            if (befehlKode == 182 && maschinenwortText(nameKonstante, "getLocalPort") && maschinenwortText(deskriptorKonstante, "()I")) { int objektVerweis = werteSubtrahieren(2); if (objektWert(objektVerweis, 15)) wertAblegen(speicherhaldeWert[objektVerweis + 2] < 0 ? -1 : Benutzer.netzwerkPort(speicherhaldeWert[objektVerweis + 2]), 1); return; }
            if (befehlKode == 182 && maschinenwortText(nameKonstante, "isClosed") && maschinenwortText(deskriptorKonstante, "()Z")) { int objektVerweis = werteSubtrahieren(2); if (objektWert(objektVerweis, 15)) wertAblegen(speicherhaldeWert[objektVerweis + 2] < 0 ? 1 : 0, 1); return; }
            if (befehlKode == 182 && maschinenwortText(nameKonstante, "close") && maschinenwortText(deskriptorKonstante, "()V")) { int objektVerweis = werteSubtrahieren(2); if (objektWert(objektVerweis, 15) && speicherhaldeWert[objektVerweis + 2] >= 0) { Benutzer.dateiDeskriptorSchließen(speicherhaldeWert[objektVerweis + 2]); speicherhaldeWert[objektVerweis + 2] = -1; } return; }
            if (befehlKode == 182 && (maschinenwortText(nameKonstante, "send") || maschinenwortText(nameKonstante, "receive")) && maschinenwortText(deskriptorKonstante, "(Ljava/net/DatagramPacket;)V")) {
                int paket = werteSubtrahieren(2), objektVerweis = werteSubtrahieren(2); if (!objektWert(paket, 16) || !objektWert(objektVerweis, 15)) return;
                int datenDatenfeld = speicherhaldeWert[paket + 2], gültigLänge = speicherhaldeWert[paket + 3], geöffnetDateiNummer = speicherhaldeWert[objektVerweis + 2];
                if (geöffnetDateiNummer < 0) { ausnahmeAuslösen(39, "socket closed"); return; }
                if (maschinenwortText(nameKonstante, "send")) {
                    if (!objektWert(speicherhaldeWert[paket + 4], 14)) return;
                    if (gültigLänge > 512) { ausnahmeAuslösen(11, "datagram limit (512 bytes)"); return; }
                    for (int schleifeIndex = 0; schleifeIndex < gültigLänge; schleifeIndex++) netzwerkVorläufigWert[schleifeIndex] = speicherhaldeWert[datenDatenfeld + 2 + schleifeIndex];
                    if (Benutzer.netzwerkSenden(geöffnetDateiNummer, speicherhaldeWert[speicherhaldeWert[paket + 4] + 2], speicherhaldeWert[paket + 5], netzwerkVorläufigWert, gültigLänge) < 0) ausnahmeAuslösen(11, "UDP send failed");
                } else {
                    int eintragAnzahl = Benutzer.netzwerkEmpfangen(geöffnetDateiNummer, netzwerkVorläufigWert, gültigLänge > 512 ? 512 : gültigLänge);
                    if (eintragAnzahl == -11) {
                        int aktuellZeit = Benutzer.millisekunden();
                        if (speicherhaldeWert[objektVerweis + 4] == 0) speicherhaldeWert[objektVerweis + 4] = aktuellZeit + 1;
                        if (speicherhaldeWert[objektVerweis + 3] > 0 && aktuellZeit - (speicherhaldeWert[objektVerweis + 4] - 1) >= speicherhaldeWert[objektVerweis + 3]) { speicherhaldeWert[objektVerweis + 4] = 0; ausnahmeAuslösen(19, "receive timed out"); return; }
                        wertAblegen(objektVerweis, 2); wertAblegen(paket, 2); rahmenPosition[rahmenIndex] = rahmenBefehlswort[rahmenIndex]; anfrageÄndern = true; return;
                    }
                    speicherhaldeWert[objektVerweis + 4] = 0;
                    if (eintragAnzahl < 0) { ausnahmeAuslösen(11, "UDP receive failed"); return; }
                    for (int schleifeIndex = 0; schleifeIndex < eintragAnzahl; schleifeIndex++) speicherhaldeWert[datenDatenfeld + 2 + schleifeIndex] = (byte)netzwerkVorläufigWert[schleifeIndex];
                    speicherhaldeWert[paket + 3] = eintragAnzahl; speicherhaldeWert[paket + 4] = adresseObjekt(netzwerkVorläufigWert[513]); speicherhaldeVerweis[paket + 4] = 1; speicherhaldeWert[paket + 5] = netzwerkVorläufigWert[512];
                }
                return;
            }
        }
        fehlschlagWert("unsupported java.net method");
    }
    static boolean fürDatenstromWarten(int objektVerweis) {
        int aktuellZeit = Benutzer.millisekunden();
        if (speicherhaldeWert[objektVerweis + 5] == 0) speicherhaldeWert[objektVerweis + 5] = aktuellZeit + 1;
        if (speicherhaldeWert[objektVerweis + 3] > 0 && aktuellZeit - (speicherhaldeWert[objektVerweis + 5] - 1) >= speicherhaldeWert[objektVerweis + 3]) { speicherhaldeWert[objektVerweis + 5] = 0; ausnahmeAuslösen(19, "stream wait timed out"); return false; }
        rahmenPosition[rahmenIndex] = rahmenBefehlswort[rahmenIndex]; anfrageÄndern = true; return true;
    }
    static void datenstromAufrufen(int eigentümer, int nameKonstante, int deskriptorKonstante, int befehlKode) {
        boolean seiteEmpfangen = maschinenwortText(eigentümer, "java/net/ServerSocket"), istDatenstrom = maschinenwortText(eigentümer, "java/io/InputStream") || maschinenwortText(eigentümer, "java/io/OutputStream");
        if (!istDatenstrom && befehlKode == 183 && maschinenwortText(nameKonstante, "<init>")) {
            boolean istLeerwertStatuswert = maschinenwortText(deskriptorKonstante, "()V"), benannt = maschinenwortText(deskriptorKonstante, "(Ljava/lang/String;I)V"), adressiert = maschinenwortText(deskriptorKonstante, "(Ljava/net/InetAddress;I)V");
            if (!(istLeerwertStatuswert || seiteEmpfangen && maschinenwortText(deskriptorKonstante, "(I)V") || !seiteEmpfangen && (benannt || adressiert))) { fehlschlagWert("unsupported socket constructor"); return; }
            int portNummer = istLeerwertStatuswert ? 0 : werteSubtrahieren(1), adresseVerweis = benannt || adressiert ? werteSubtrahieren(2) : 0, objektVerweis = werteSubtrahieren(2);
            if (!objektWert(objektVerweis, seiteEmpfangen ? 18 : 17)) return;
            if (portNummer < 0 || portNummer > 65535) { ausnahmeAuslösen(9, "invalid port"); return; }
            if (adressiert && !objektWert(adresseVerweis, 14)) return;
            int netzwerkAdresse = benannt ? adresseDekodieren(adresseVerweis) : adressiert ? speicherhaldeWert[adresseVerweis + 2] : 0x7f000001;
            if (fehler || ausgelöstObjekt != 0) return;
            int geöffnetDateiNummer = Benutzer.datenstromSteuerung(0, 0, 0); if (geöffnetDateiNummer < 0) { ausnahmeAuslösen(39, "socket slots exhausted"); return; }
            int verarbeitetWert = istLeerwertStatuswert ? 0 : seiteEmpfangen ? Benutzer.datenstromSteuerung(1, geöffnetDateiNummer, portNummer) : Benutzer.datenstromVerbinden(geöffnetDateiNummer, netzwerkAdresse, portNummer);
            if (verarbeitetWert < 0) { Benutzer.dateiDeskriptorSchließen(geöffnetDateiNummer); ausnahmeAuslösen(39, "socket bind/connect failed"); return; }
            speicherhaldeWert[objektVerweis + 2] = geöffnetDateiNummer; speicherhaldeWert[objektVerweis + 4] = portNummer; speicherhaldeWert[objektVerweis + 6] = istLeerwertStatuswert ? 0 : 1; return;
        }
        if (!istDatenstrom && maschinenwortText(nameKonstante, "setSoTimeout") && maschinenwortText(deskriptorKonstante, "(I)V")) { int millisekundenWert = werteSubtrahieren(1), objektVerweis = werteSubtrahieren(2); if (!objektWert(objektVerweis, seiteEmpfangen ? 18 : 17)) return; if (millisekundenWert < 0) ausnahmeAuslösen(9, "negative timeout"); else speicherhaldeWert[objektVerweis + 3] = millisekundenWert; return; }
        if (!istDatenstrom && maschinenwortText(nameKonstante, "close") && maschinenwortText(deskriptorKonstante, "()V")) { int objektVerweis = werteSubtrahieren(2); if (objektWert(objektVerweis, seiteEmpfangen ? 18 : 17) && speicherhaldeWert[objektVerweis + 2] >= 0) { Benutzer.dateiDeskriptorSchließen(speicherhaldeWert[objektVerweis + 2]); speicherhaldeWert[objektVerweis + 2] = -1; } return; }
        if (!istDatenstrom && (maschinenwortText(nameKonstante, "getLocalPort") || maschinenwortText(nameKonstante, "getPort") || maschinenwortText(nameKonstante, "isClosed") || maschinenwortText(nameKonstante, "isConnected"))) {
            int objektVerweis = werteSubtrahieren(2); if (!objektWert(objektVerweis, seiteEmpfangen ? 18 : 17)) return;
            wertAblegen(maschinenwortText(nameKonstante, "isClosed") ? speicherhaldeWert[objektVerweis + 2] < 0 ? 1 : 0 : maschinenwortText(nameKonstante, "isConnected") ? speicherhaldeWert[objektVerweis + 6] : maschinenwortText(nameKonstante, "getPort") ? speicherhaldeWert[objektVerweis + 4] : speicherhaldeWert[objektVerweis + 2] < 0 ? -1 : Benutzer.datenstromSteuerung(4, speicherhaldeWert[objektVerweis + 2], 0), 1); return;
        }
        if (seiteEmpfangen && maschinenwortText(nameKonstante, "accept") && maschinenwortText(deskriptorKonstante, "()Ljava/net/Socket;")) {
            int objektVerweis = werteSubtrahieren(2); if (!objektWert(objektVerweis, 18)) return; int geöffnetDateiNummer = Benutzer.datenstromSteuerung(3, speicherhaldeWert[objektVerweis + 2], 0);
            if (geöffnetDateiNummer == -11) { if (fürDatenstromWarten(objektVerweis)) wertAblegen(objektVerweis, 2); return; }
            speicherhaldeWert[objektVerweis + 5] = 0; if (geöffnetDateiNummer < 0) { ausnahmeAuslösen(11, "accept failed"); return; }
            int zurückgegebenWert = speichergerätZuteilen(17, 5); if (fehler) { Benutzer.dateiDeskriptorSchließen(geöffnetDateiNummer); return; } speicherhaldeWert[zurückgegebenWert + 2] = geöffnetDateiNummer; speicherhaldeWert[zurückgegebenWert + 4] = Benutzer.datenstromSteuerung(5, geöffnetDateiNummer, 0); speicherhaldeWert[zurückgegebenWert + 6] = 1; wertAblegen(zurückgegebenWert, 2); return;
        }
        if (!seiteEmpfangen && !istDatenstrom && ((maschinenwortText(nameKonstante, "getInputStream") && maschinenwortText(deskriptorKonstante, "()Ljava/io/InputStream;")) || (maschinenwortText(nameKonstante, "getOutputStream") && maschinenwortText(deskriptorKonstante, "()Ljava/io/OutputStream;")))) {
            int objektVerweis = werteSubtrahieren(2); if (!objektWert(objektVerweis, 17)) return; if (speicherhaldeWert[objektVerweis + 2] < 0 || speicherhaldeWert[objektVerweis + 6] == 0) { ausnahmeAuslösen(39, "socket is not connected"); return; }
            int zurückgegebenWert = speichergerätZuteilen(19, 4); if (fehler) return; speicherhaldeWert[zurückgegebenWert + 2] = objektVerweis; speicherhaldeVerweis[zurückgegebenWert + 2] = 1; speicherhaldeWert[zurückgegebenWert + 3] = maschinenwortText(nameKonstante, "getInputStream") ? 0 : 1; wertAblegen(zurückgegebenWert, 2); return;
        }
        if (istDatenstrom) {
            boolean hatLesen = maschinenwortText(nameKonstante, "read"), istSchreibenVorgang = maschinenwortText(nameKonstante, "write"), block = maschinenwortText(deskriptorKonstante, "([B)I") || maschinenwortText(deskriptorKonstante, "([B)V"), istTeilfeld = maschinenwortText(deskriptorKonstante, "([BII)I") || maschinenwortText(deskriptorKonstante, "([BII)V");
            int eintragAnzahl = istTeilfeld ? werteSubtrahieren(1) : 0, versatzStarten = istTeilfeld ? werteSubtrahieren(1) : 0, datenDatenfeld = block || istTeilfeld ? werteSubtrahieren(2) : 0;
            int datenWert = istSchreibenVorgang && maschinenwortText(deskriptorKonstante, "(I)V") ? werteSubtrahieren(1) : 0, objektVerweis = werteSubtrahieren(2);
            if (!objektWert(objektVerweis, 19)) return; int elternknotenVerweis = speicherhaldeWert[objektVerweis + 2], geöffnetDateiNummer = speicherhaldeWert[elternknotenVerweis + 2];
            if (geöffnetDateiNummer < 0) { ausnahmeAuslösen(11, "stream closed"); return; }
            if (maschinenwortText(nameKonstante, "close") && maschinenwortText(deskriptorKonstante, "()V")) { Benutzer.dateiDeskriptorSchließen(geöffnetDateiNummer); speicherhaldeWert[elternknotenVerweis + 2] = -1; return; }
            if (maschinenwortText(nameKonstante, "flush") && maschinenwortText(deskriptorKonstante, "()V")) return;
            if ((!hatLesen && !istSchreibenVorgang) || hatLesen != (speicherhaldeWert[objektVerweis + 3] == 0)) { fehlschlagWert("unsupported stream operation"); return; }
            if (block || istTeilfeld) { if (!objektWert(datenDatenfeld, 20)) return; if (block) eintragAnzahl = speicherhaldeWert[datenDatenfeld + 1]; if (versatzStarten < 0 || eintragAnzahl < 0 || versatzStarten > speicherhaldeWert[datenDatenfeld + 1] - eintragAnzahl) { ausnahmeAuslösen(6, "stream array bounds"); return; } }
            else eintragAnzahl = 1;
            if (eintragAnzahl == 0) { if (hatLesen) wertAblegen(0, 1); return; }
            int abgeschlossenAnzahl = istSchreibenVorgang ? speicherhaldeWert[objektVerweis + 4] : 0, verarbeitetWert = 0;
            while (abgeschlossenAnzahl < eintragAnzahl) {
                verarbeitetWert = hatLesen ? Benutzer.einsDateiByteLesen(geöffnetDateiNummer) : Benutzer.einsDateiByteSchreiben(geöffnetDateiNummer, block || istTeilfeld ? speicherhaldeWert[datenDatenfeld + 2 + versatzStarten + abgeschlossenAnzahl] : datenWert);
                if (verarbeitetWert < 0 || hatLesen && verarbeitetWert == 256) break;
                if (hatLesen && (block || istTeilfeld)) speicherhaldeWert[datenDatenfeld + 2 + versatzStarten + abgeschlossenAnzahl] = (byte)verarbeitetWert;
                abgeschlossenAnzahl++; if (hatLesen && !(block || istTeilfeld)) break;
            }
            if (verarbeitetWert == -11 && (istSchreibenVorgang || abgeschlossenAnzahl == 0)) {
                speicherhaldeWert[objektVerweis + 4] = abgeschlossenAnzahl;
                if (fürDatenstromWarten(elternknotenVerweis)) { wertAblegen(objektVerweis, 2); if (block || istTeilfeld) wertAblegen(datenDatenfeld, 2); if (istTeilfeld) { wertAblegen(versatzStarten, 1); wertAblegen(eintragAnzahl, 1); } if (istSchreibenVorgang && !(block || istTeilfeld)) wertAblegen(datenWert, 1); } return;
            }
            speicherhaldeWert[objektVerweis + 4] = 0; speicherhaldeWert[elternknotenVerweis + 5] = 0;
            if (verarbeitetWert < 0 && verarbeitetWert != -11) { ausnahmeAuslösen(11, "stream I/O failed"); return; }
            if (hatLesen) wertAblegen(abgeschlossenAnzahl == 0 && verarbeitetWert == 256 ? -1 : block || istTeilfeld ? abgeschlossenAnzahl : verarbeitetWert, 1); return;
        }
        fehlschlagWert("unsupported Socket/ServerSocket method");
    }
    static int[] bildschirmVerweis = new int[32], vorläufigBildschirmText = new int[256], zeitplanSpäter = new int[8];
    static int späterAnzahl;
    static int[] späterKoreanischWert = new int[8];
    static boolean istBehandlungEreignis;
    static int koreanischBildschirmKlasse(int nameKonstante) {
        if (maschinenwortText(nameKonstante, "Deutsch/eigen/fenster")) return 24;
        if (maschinenwortText(nameKonstante, "Deutsch/eigen/beschriftung")) return 26;
        if (maschinenwortText(nameKonstante, "Deutsch/eigen/schaltfläche")) return 27;
        if (maschinenwortText(nameKonstante, "Deutsch/eigen/TextFeld")) return 28;
        if (maschinenwortText(nameKonstante, "Deutsch/eigen/AktionMitteilung")) return 29;
        return 0;
    }
    static boolean koreanischBildschirmEigentümer(int nameKonstante) {
        return koreanischBildschirmKlasse(nameKonstante) != 0 || maschinenwortText(nameKonstante, "Deutsch/eigen/BildschirmElement") || maschinenwortText(nameKonstante, "Deutsch/eigen/EreignisWarteschlange");
    }
    static int bildschirmKlasse(int nameKonstante) {
        int KoreanischKlasse = koreanischBildschirmKlasse(nameKonstante); if (KoreanischKlasse != 0) return KoreanischKlasse;
        if (maschinenwortText(nameKonstante, "javax/swing/JFrame")) return 24;
        if (maschinenwortText(nameKonstante, "javax/swing/JPanel")) return 25;
        if (maschinenwortText(nameKonstante, "javax/swing/JLabel")) return 26;
        if (maschinenwortText(nameKonstante, "javax/swing/JButton")) return 27;
        if (maschinenwortText(nameKonstante, "javax/swing/JTextField")) return 28;
        if (maschinenwortText(nameKonstante, "java/awt/event/ActionEvent")) return 29;
        if (maschinenwortText(nameKonstante, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean bildschirmEigentümer(int nameKonstante) {
        return bildschirmKlasse(nameKonstante) != 0 || maschinenwortText(nameKonstante, "java/awt/Component") || maschinenwortText(nameKonstante, "java/awt/Container") || maschinenwortText(nameKonstante, "javax/swing/JComponent") || maschinenwortText(nameKonstante, "javax/swing/AbstractButton") || maschinenwortText(nameKonstante, "javax/swing/text/JTextComponent") || maschinenwortText(nameKonstante, "javax/swing/SwingUtilities");
    }
    static boolean bildschirmObjekt(int objektVerweis) { if (!istGültigObjekt(objektVerweis)) return false; if (speicherhaldeWert[objektVerweis] < 24 || speicherhaldeWert[objektVerweis] > 28) { fehlschlagWert("unsupported Swing receiver"); return false; } return true; }
    static void bildschirmZeichenSetzen(int objektVerweis, int textVerweis) {
        if (textVerweis != 0 && !objektWert(textVerweis, 1)) return;
        int eintragAnzahl = textVerweis == 0 ? 0 : speicherhaldeWert[textVerweis + 1]; if (eintragAnzahl > 254) { ausnahmeAuslösen(9, "GUI text limit"); return; }
        for (int schleifeIndex = 0; schleifeIndex < eintragAnzahl; schleifeIndex++) vorläufigBildschirmText[schleifeIndex] = speicherhaldeWert[textVerweis + 2 + schleifeIndex];
        if (Benutzer.bildschirmText(speicherhaldeWert[objektVerweis + 2], vorläufigBildschirmText, eintragAnzahl) < 0) { ausnahmeAuslösen(9, "GUI text too long/invalid"); return; }
        speicherhaldeWert[objektVerweis + 3] = textVerweis; speicherhaldeVerweis[objektVerweis + 3] = 1;
    }
    static int bildschirmZeichenLesen(int objektVerweis) {
        int identitätWert = speicherhaldeWert[objektVerweis + 2], eintragAnzahl = Benutzer.bildschirmVerbindung(8, identitätWert, 0, 0, 0, 0), benutztAnzahl = 0;
        if (eintragAnzahl < 0) { fehlschlagWert("GUI text read failed"); return 0; }
        for (int schleifeIndex = 0; schleifeIndex < eintragAnzahl; schleifeIndex++) { int kodiertWert = Benutzer.bildschirmVerbindung(9, identitätWert, schleifeIndex, 0, 0, 0); if (kodiertWert >= 65536) { kodiertWert -= 65536; vorläufigBildschirmText[benutztAnzahl++] = 0xd800 | kodiertWert >> 10; vorläufigBildschirmText[benutztAnzahl++] = 0xdc00 | kodiertWert & 1023; } else vorläufigBildschirmText[benutztAnzahl++] = kodiertWert; }
        int zurückgegebenWert = speichergerätZuteilen(1, benutztAnzahl); if (!fehler) for (int schleifeIndex = 0; schleifeIndex < benutztAnzahl; schleifeIndex++) speicherhaldeWert[zurückgegebenWert + 2 + schleifeIndex] = vorläufigBildschirmText[schleifeIndex]; return zurückgegebenWert;
    }
    /* Erzeugt Objekte der deutschen API direkt und verbindet sie mit der Kernelgrafik, ohne Swing-Objekte oder Adapter. */
    static void koreanischBildschirmAufrufen(int eigentümer, int nameKonstante, int deskriptorKonstante, int befehlKode) {
        if (maschinenwortText(eigentümer, "Deutsch/eigen/EreignisWarteschlange")) {
            if (befehlKode == 184 && maschinenwortText(nameKonstante, "späterAufrufen") && maschinenwortText(deskriptorKonstante, "(LDeutsch/eigen/AusführbarAufgabe;)V")) {
                int AufgabeAktion = werteSubtrahieren(2); if (!istGültigObjekt(AufgabeAktion)) return;
                if (späterAnzahl == 8) { fehlschlagWert("Bildschirm Aufgabe 대기열이 가득 찼습니다"); return; }
                späterKoreanischWert[späterAnzahl] = 1; zeitplanSpäter[späterAnzahl++] = AufgabeAktion; return;
            }
            if (befehlKode == 184 && maschinenwortText(nameKonstante, "istEreignisVerteilend") && maschinenwortText(deskriptorKonstante, "()Z")) { wertAblegen(istBehandlungEreignis ? 1 : 0, 1); return; }
            fehlschlagWert("지원하지 않는 Deutsch Bildschirm 일정 aufrufen"); return;
        }
        if (maschinenwortText(eigentümer, "Deutsch/eigen/AktionMitteilung")) {
            int mitteilung = werteSubtrahieren(2); if (!objektWert(mitteilung, 29) || speicherhaldeWert[mitteilung + 3] == 0) return;
            if (maschinenwortText(nameKonstante, "ereignisQuelltext") && maschinenwortText(deskriptorKonstante, "()LDeutsch/eigen/BildschirmElement;")) wertAblegen(speicherhaldeWert[mitteilung + 2], 2);
            else if (maschinenwortText(nameKonstante, "befehlText") && maschinenwortText(deskriptorKonstante, "()Ljava/lang/String;")) wertAblegen(bildschirmZeichenLesen(speicherhaldeWert[mitteilung + 2]), 2);
            else if (maschinenwortText(nameKonstante, "Nummer") && maschinenwortText(deskriptorKonstante, "()I")) wertAblegen(1001, 1);
            else fehlschlagWert("지원하지 않는 Deutsch aktion mitteilung aufrufen"); return;
        }
        if (befehlKode == 183 && maschinenwortText(nameKonstante, "<init>")) {
            int artWert = koreanischBildschirmKlasse(eigentümer), empfängerWert = 0, waagerechtPosition = 0, senkrechtPosition = 0, breiteSpannweite = 0, höheWert = 0;
            if (artWert == 24 && maschinenwortText(deskriptorKonstante, "(Ljava/lang/String;II)V")) {
                höheWert = werteSubtrahieren(1); breiteSpannweite = werteSubtrahieren(1); waagerechtPosition = (Benutzer.bildschirmBreite() - breiteSpannweite) / 2; senkrechtPosition = (Benutzer.bildschirmHöhe() - höheWert) / 2;
            } else if ((artWert == 26 || artWert == 28) && maschinenwortText(deskriptorKonstante, "(Ljava/lang/String;IIII)V") || artWert == 27 && maschinenwortText(deskriptorKonstante, "(Ljava/lang/String;IIIILDeutsch/eigen/AktionEmpfänger;)V")) {
                if (artWert == 27) empfängerWert = werteSubtrahieren(2);
                höheWert = werteSubtrahieren(1); breiteSpannweite = werteSubtrahieren(1); senkrechtPosition = werteSubtrahieren(1); waagerechtPosition = werteSubtrahieren(1);
            } else { fehlschlagWert("지원하지 않는 Deutsch Bildschirm 생성자"); return; }
            int Text = werteSubtrahieren(2), elementWert = werteSubtrahieren(2); if (!bildschirmObjekt(elementWert)) return;
            if (breiteSpannweite < 1 || höheWert < 1 || waagerechtPosition < 0 || senkrechtPosition < 0 || breiteSpannweite > Benutzer.bildschirmBreite() - waagerechtPosition || höheWert > Benutzer.bildschirmHöhe() - senkrechtPosition) { ausnahmeAuslösen(27, "Bildschirm 영역을 벗어난 크기입니다"); return; }
            int Nummer = Benutzer.bildschirmVerbindung(0, artWert - 23, 0, 0, 0, 0);
            if (Nummer < 1 || Nummer > 32) { fehlschlagWert("Bildschirm elementWert 자리가 가득 찼습니다"); return; }
            speicherhaldeWert[elementWert + 2] = Nummer; bildschirmVerweis[Nummer - 1] = elementWert;
            speicherhaldeWert[elementWert + 5] = waagerechtPosition; speicherhaldeWert[elementWert + 6] = senkrechtPosition; speicherhaldeWert[elementWert + 7] = breiteSpannweite; speicherhaldeWert[elementWert + 8] = höheWert; speicherhaldeWert[elementWert + 10] = 2;
            speicherhaldeWert[elementWert + 4] = empfängerWert; speicherhaldeVerweis[elementWert + 4] = 1; speicherhaldeWert[elementWert + 12] = 1;
            Benutzer.bildschirmVerbindung(1, Nummer, waagerechtPosition, senkrechtPosition, breiteSpannweite, höheWert);
            if (artWert == 24) Benutzer.bildschirmVerbindung(7, Nummer, 2, 0, 0, 0);
            bildschirmZeichenSetzen(elementWert, Text); return;
        }
        if (befehlKode != 182) { fehlschlagWert("잘못된 Deutsch Bildschirm aufrufen befehl"); return; }
        if (maschinenwortText(nameKonstante, "textSchreiben") && maschinenwortText(deskriptorKonstante, "(Ljava/lang/String;)V")) {
            int Text = werteSubtrahieren(2), elementWert = werteSubtrahieren(2); if (bildschirmObjekt(elementWert)) bildschirmZeichenSetzen(elementWert, Text); return;
        }
        if (maschinenwortText(nameKonstante, "textLesen") && maschinenwortText(deskriptorKonstante, "()Ljava/lang/String;")) {
            int elementWert = werteSubtrahieren(2); if (bildschirmObjekt(elementWert)) wertAblegen(bildschirmZeichenLesen(elementWert), 2); return;
        }
        if (maschinenwortText(nameKonstante, "aktionEmpfängerSetzen") && maschinenwortText(deskriptorKonstante, "(LDeutsch/eigen/AktionEmpfänger;)V")) {
            int empfängerWert = werteSubtrahieren(2), elementWert = werteSubtrahieren(2);
            if (bildschirmObjekt(elementWert)) { speicherhaldeWert[elementWert + 4] = empfängerWert; speicherhaldeVerweis[elementWert + 4] = 1; speicherhaldeWert[elementWert + 12] = 1; } return;
        }
        if (maschinenwortText(nameKonstante, "elementHinzufügen") && maschinenwortText(deskriptorKonstante, "(LDeutsch/eigen/BildschirmElement;)V")) {
            int kindWert = werteSubtrahieren(2), elternknotenWert = werteSubtrahieren(2); if (!bildschirmObjekt(kindWert) || !bildschirmObjekt(elternknotenWert)) return;
            if (Benutzer.bildschirmVerbindung(2, speicherhaldeWert[elternknotenWert + 2], speicherhaldeWert[kindWert + 2], 0, 0, 0) < 0) { ausnahmeAuslösen(27, "잘못된 Bildschirm 부모입니다"); return; }
            speicherhaldeWert[kindWert + 11] = elternknotenWert; speicherhaldeVerweis[kindWert + 11] = 1; return;
        }
        if (maschinenwortText(nameKonstante, "grenzenSetzen") && maschinenwortText(deskriptorKonstante, "(IIII)V")) {
            int höheWert = werteSubtrahieren(1), breiteSpannweite = werteSubtrahieren(1), senkrechtPosition = werteSubtrahieren(1), waagerechtPosition = werteSubtrahieren(1), elementWert = werteSubtrahieren(2); if (!bildschirmObjekt(elementWert)) return;
            if (Benutzer.bildschirmVerbindung(1, speicherhaldeWert[elementWert + 2], waagerechtPosition, senkrechtPosition, breiteSpannweite, höheWert) < 0) { ausnahmeAuslösen(27, "Bildschirm 영역을 벗어난 자리입니다"); return; }
            speicherhaldeWert[elementWert + 5] = waagerechtPosition; speicherhaldeWert[elementWert + 6] = senkrechtPosition; speicherhaldeWert[elementWert + 7] = breiteSpannweite; speicherhaldeWert[elementWert + 8] = höheWert; return;
        }
        if ((maschinenwortText(nameKonstante, "fensterAnzeigen") || maschinenwortText(nameKonstante, "schließen")) && maschinenwortText(deskriptorKonstante, "()V")) {
            boolean sichtbarkeitWert = maschinenwortText(nameKonstante, "fensterAnzeigen"); int elementWert = werteSubtrahieren(2); if (!bildschirmObjekt(elementWert)) return;
            if (Benutzer.bildschirmVerbindung(sichtbarkeitWert ? 3 : 4, speicherhaldeWert[elementWert + 2], sichtbarkeitWert ? 1 : 0, 0, 0, 0) < 0) { fehlschlagWert("화면은 interaktiv 명령에서 실행해야 합니다"); return; }
            speicherhaldeWert[elementWert + 9] = sichtbarkeitWert ? 1 : 0; return;
        }
        if (maschinenwortText(nameKonstante, "istSichtbar") && maschinenwortText(deskriptorKonstante, "()Z")) { int elementWert = werteSubtrahieren(2); if (bildschirmObjekt(elementWert)) wertAblegen(speicherhaldeWert[elementWert + 9], 1); return; }
        fehlschlagWert("지원하지 않는 Deutsch Bildschirm methodeWert");
    }
    static void bildschirmAufrufen(int eigentümer, int nameKonstante, int deskriptorKonstante, int befehlKode) {
        if (maschinenwortText(eigentümer, "javax/swing/SwingUtilities")) {
            if (befehlKode == 184 && maschinenwortText(nameKonstante, "invokeLater") && maschinenwortText(deskriptorKonstante, "(Ljava/lang/Runnable;)V")) { int objektVerweis = werteSubtrahieren(2); if (!istGültigObjekt(objektVerweis)) return; if (späterAnzahl == 8) { fehlschlagWert("invokeLater queue full"); return; } zeitplanSpäter[späterAnzahl++] = objektVerweis; return; }
            if (befehlKode == 184 && maschinenwortText(nameKonstante, "isEventDispatchThread") && maschinenwortText(deskriptorKonstante, "()Z")) { wertAblegen(istBehandlungEreignis ? 1 : 0, 1); return; }
            fehlschlagWert("unsupported SwingUtilities method"); return;
        }
        if (maschinenwortText(eigentümer, "java/awt/event/ActionEvent")) {
            int objektVerweis = werteSubtrahieren(2); if (!objektWert(objektVerweis, 29)) return;
            if (maschinenwortText(nameKonstante, "getSource") && maschinenwortText(deskriptorKonstante, "()Ljava/lang/Object;")) wertAblegen(speicherhaldeWert[objektVerweis + 2], 2);
            else if (maschinenwortText(nameKonstante, "getActionCommand") && maschinenwortText(deskriptorKonstante, "()Ljava/lang/String;")) wertAblegen(bildschirmZeichenLesen(speicherhaldeWert[objektVerweis + 2]), 2);
            else if (maschinenwortText(nameKonstante, "getID") && maschinenwortText(deskriptorKonstante, "()I")) wertAblegen(1001, 1);
            else fehlschlagWert("unsupported ActionEvent method"); return;
        }
        if (befehlKode == 183 && maschinenwortText(nameKonstante, "<init>")) {
            int spaltenliste = 0, textVerweis = 0;
            if (maschinenwortText(deskriptorKonstante, "(I)V")) spaltenliste = werteSubtrahieren(1);
            else if (maschinenwortText(deskriptorKonstante, "(Ljava/lang/String;I)V")) { spaltenliste = werteSubtrahieren(1); textVerweis = werteSubtrahieren(2); }
            else if (maschinenwortText(deskriptorKonstante, "(Ljava/lang/String;)V")) textVerweis = werteSubtrahieren(2);
            else if (maschinenwortText(deskriptorKonstante, "(Ljava/awt/LayoutManager;)V")) werteSubtrahieren(2);
            else if (!maschinenwortText(deskriptorKonstante, "()V")) { fehlschlagWert("unsupported Swing constructor"); return; }
            int objektVerweis = werteSubtrahieren(2); if (!istGültigObjekt(objektVerweis)) return;
            if (speicherhaldeWert[objektVerweis] == 30) { fehlschlagWert("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!bildschirmObjekt(objektVerweis) || spaltenliste < 0) return;
            int identitätWert = Benutzer.bildschirmVerbindung(0, speicherhaldeWert[objektVerweis] - 23, 0, 0, 0, 0);
            if (identitätWert < 1 || identitätWert > 32) { fehlschlagWert("GUI widget slots exhausted"); return; }
            speicherhaldeWert[objektVerweis + 2] = identitätWert; bildschirmVerweis[identitätWert - 1] = objektVerweis; speicherhaldeWert[objektVerweis + 5] = speicherhaldeWert[objektVerweis] == 24 ? 130 : 16; speicherhaldeWert[objektVerweis + 6] = speicherhaldeWert[objektVerweis] == 24 ? 110 : 16;
            speicherhaldeWert[objektVerweis + 7] = speicherhaldeWert[objektVerweis] == 24 ? 380 : 220; speicherhaldeWert[objektVerweis + 8] = speicherhaldeWert[objektVerweis] == 24 ? 240 : 28; speicherhaldeWert[objektVerweis + 10] = 1;
            bildschirmZeichenSetzen(objektVerweis, textVerweis); return;
        }
        if (maschinenwortText(nameKonstante, "setText") || maschinenwortText(nameKonstante, "setTitle")) { int textVerweis = werteSubtrahieren(2), objektVerweis = werteSubtrahieren(2); if (bildschirmObjekt(objektVerweis) && maschinenwortText(deskriptorKonstante, "(Ljava/lang/String;)V")) bildschirmZeichenSetzen(objektVerweis, textVerweis); return; }
        if (maschinenwortText(nameKonstante, "getText") || maschinenwortText(nameKonstante, "getTitle")) { int objektVerweis = werteSubtrahieren(2); if (bildschirmObjekt(objektVerweis) && maschinenwortText(deskriptorKonstante, "()Ljava/lang/String;")) wertAblegen(bildschirmZeichenLesen(objektVerweis), 2); return; }
        if (maschinenwortText(nameKonstante, "addActionListener") && maschinenwortText(deskriptorKonstante, "(Ljava/awt/event/ActionListener;)V")) { int verweisEmpfangen = werteSubtrahieren(2), objektVerweis = werteSubtrahieren(2); if (bildschirmObjekt(objektVerweis)) { speicherhaldeWert[objektVerweis + 4] = verweisEmpfangen; speicherhaldeVerweis[objektVerweis + 4] = 1; } return; }
        if (maschinenwortText(nameKonstante, "getContentPane") && maschinenwortText(deskriptorKonstante, "()Ljava/awt/Container;")) { int objektVerweis = werteSubtrahieren(2); if (bildschirmObjekt(objektVerweis)) wertAblegen(objektVerweis, 2); return; }
        if (maschinenwortText(nameKonstante, "setLayout") && maschinenwortText(deskriptorKonstante, "(Ljava/awt/LayoutManager;)V")) { int anordnungVerweis = werteSubtrahieren(2), objektVerweis = werteSubtrahieren(2); if (bildschirmObjekt(objektVerweis) && anordnungVerweis != 0) fehlschlagWert("only absolute layout (null) is supported"); return; }
        if (maschinenwortText(nameKonstante, "add") && (maschinenwortText(deskriptorKonstante, "(Ljava/awt/Component;)Ljava/awt/Component;") || maschinenwortText(deskriptorKonstante, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean anordnungBedingung = maschinenwortText(deskriptorKonstante, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (anordnungBedingung) werteSubtrahieren(2);
            int kindVerweis = werteSubtrahieren(2), objektVerweis = werteSubtrahieren(2); if (!bildschirmObjekt(kindVerweis) || !bildschirmObjekt(objektVerweis)) return;
            if (Benutzer.bildschirmVerbindung(2, speicherhaldeWert[objektVerweis + 2], speicherhaldeWert[kindVerweis + 2], 0, 0, 0) < 0) { ausnahmeAuslösen(9, "invalid GUI parent"); return; }
            speicherhaldeWert[kindVerweis + 11] = objektVerweis; speicherhaldeVerweis[kindVerweis + 11] = 1; if (!anordnungBedingung) wertAblegen(kindVerweis, 2); return;
        }
        if (maschinenwortText(nameKonstante, "setBounds") && maschinenwortText(deskriptorKonstante, "(IIII)V")) {
            int höheWert = werteSubtrahieren(1), breiteWert = werteSubtrahieren(1), senkrechteKoordinateKoordinate = werteSubtrahieren(1), waagerechteKoordinateKoordinate = werteSubtrahieren(1), objektVerweis = werteSubtrahieren(2); if (!bildschirmObjekt(objektVerweis)) return;
            if (Benutzer.bildschirmVerbindung(1, speicherhaldeWert[objektVerweis + 2], waagerechteKoordinateKoordinate, senkrechteKoordinateKoordinate, breiteWert, höheWert) < 0) { ausnahmeAuslösen(9, "GUI bounds"); return; }
            speicherhaldeWert[objektVerweis + 5] = waagerechteKoordinateKoordinate; speicherhaldeWert[objektVerweis + 6] = senkrechteKoordinateKoordinate; speicherhaldeWert[objektVerweis + 7] = breiteWert; speicherhaldeWert[objektVerweis + 8] = höheWert; return;
        }
        if (maschinenwortText(nameKonstante, "setSize") && maschinenwortText(deskriptorKonstante, "(II)V")) {
            int höheWert = werteSubtrahieren(1), breiteWert = werteSubtrahieren(1), objektVerweis = werteSubtrahieren(2); if (!bildschirmObjekt(objektVerweis)) return;
            if (Benutzer.bildschirmVerbindung(1, speicherhaldeWert[objektVerweis + 2], speicherhaldeWert[objektVerweis + 5], speicherhaldeWert[objektVerweis + 6], breiteWert, höheWert) < 0) ausnahmeAuslösen(9, "GUI size"); else { speicherhaldeWert[objektVerweis + 7] = breiteWert; speicherhaldeWert[objektVerweis + 8] = höheWert; } return;
        }
        if (maschinenwortText(nameKonstante, "setLocationRelativeTo") && maschinenwortText(deskriptorKonstante, "(Ljava/awt/Component;)V")) { int relativ = werteSubtrahieren(2), objektVerweis = werteSubtrahieren(2); if (!bildschirmObjekt(objektVerweis)) return; if (relativ != 0) { fehlschlagWert("only screen centering supported"); return; } speicherhaldeWert[objektVerweis + 5] = (Benutzer.bildschirmBreite() - speicherhaldeWert[objektVerweis + 7]) / 2; speicherhaldeWert[objektVerweis + 6] = (Benutzer.bildschirmHöhe() - speicherhaldeWert[objektVerweis + 8]) / 2; Benutzer.bildschirmVerbindung(1, speicherhaldeWert[objektVerweis + 2], speicherhaldeWert[objektVerweis + 5], speicherhaldeWert[objektVerweis + 6], speicherhaldeWert[objektVerweis + 7], speicherhaldeWert[objektVerweis + 8]); return; }
        if (maschinenwortText(nameKonstante, "setDefaultCloseOperation") && maschinenwortText(deskriptorKonstante, "(I)V")) { int richtlinie = werteSubtrahieren(1), objektVerweis = werteSubtrahieren(2); if (bildschirmObjekt(objektVerweis)) { if (richtlinie < 0 || richtlinie > 3) ausnahmeAuslösen(9, "close policy"); else { speicherhaldeWert[objektVerweis + 10] = richtlinie; Benutzer.bildschirmVerbindung(7, speicherhaldeWert[objektVerweis + 2], richtlinie, 0, 0, 0); } } return; }
        if (maschinenwortText(nameKonstante, "setVisible") && maschinenwortText(deskriptorKonstante, "(Z)V")) { int datenWert = werteSubtrahieren(1), objektVerweis = werteSubtrahieren(2); if (bildschirmObjekt(objektVerweis)) { int verarbeitetWert = Benutzer.bildschirmVerbindung(3, speicherhaldeWert[objektVerweis + 2], datenWert, 0, 0, 0); if (verarbeitetWert < 0) fehlschlagWert("Swing requires a standalone interactive command"); else speicherhaldeWert[objektVerweis + 9] = datenWert; } return; }
        if (maschinenwortText(nameKonstante, "dispose") && maschinenwortText(deskriptorKonstante, "()V")) { int objektVerweis = werteSubtrahieren(2); if (bildschirmObjekt(objektVerweis)) { Benutzer.bildschirmVerbindung(4, speicherhaldeWert[objektVerweis + 2], 0, 0, 0, 0); speicherhaldeWert[objektVerweis + 9] = 0; } return; }
        if (maschinenwortText(nameKonstante, "repaint") || maschinenwortText(nameKonstante, "validate")) { int objektVerweis = werteSubtrahieren(2); if (!bildschirmObjekt(objektVerweis) || !maschinenwortText(deskriptorKonstante, "()V")) return; Benutzer.bildschirmVerbindung(1, speicherhaldeWert[objektVerweis + 2], speicherhaldeWert[objektVerweis + 5], speicherhaldeWert[objektVerweis + 6], speicherhaldeWert[objektVerweis + 7], speicherhaldeWert[objektVerweis + 8]); return; }
        if (maschinenwortText(nameKonstante, "isVisible") && maschinenwortText(deskriptorKonstante, "()Z")) { int objektVerweis = werteSubtrahieren(2); if (bildschirmObjekt(objektVerweis)) wertAblegen(speicherhaldeWert[objektVerweis + 9], 1); return; }
        fehlschlagWert("unsupported Swing method (native subset)");
    }
    static void zustellenEreignis(int zielobjektAdresse, int ereignisNummer, boolean Deutsch) {
        if (zielobjektAdresse < 1 || speicherhaldeWert[zielobjektAdresse] < 32) { fehlschlagWert("Java event listener required"); return; }
        int dateiIndex = nameMethode(speicherhaldeWert[zielobjektAdresse] - 32, ereignisNummer == 0 ? (Deutsch ? "aufgabeAusführen" : "run") : (Deutsch ? "aktionEmpfangen" : "actionPerformed"), ereignisNummer == 0 ? "()V" : (Deutsch ? "(LDeutsch/eigen/AktionMitteilung;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (dateiIndex < 0) { fehlschlagWert("event callback missing"); return; }
        aktuellAusführungsfaden = 0; ausführungsfadenAnzahl = 1; rahmenIndex = 0; ausführungsfadenStatuswert[0] = 1; rahmenStapel[0] = 0; rahmenSperre[0] = rahmenInitialisieren[0] = 0; anfrageÄndern = false;
        for (int schleifeIndex = 0; schleifeIndex < 128; schleifeIndex++) { lokalWert[schleifeIndex] = lokalTyp[schleifeIndex] = 0; }
        rahmenMethode[0] = dateiIndex; rahmenPosition[0] = methodeStarten[dateiIndex]; lokalWert[0] = zielobjektAdresse; lokalTyp[0] = 2;
        if (ereignisNummer != 0) { lokalWert[1] = ereignisNummer; lokalTyp[1] = 2; }
        istBehandlungEreignis = true; befehlAusführen(); istBehandlungEreignis = false;
    }
    static void bildschirmEreignisse() {
        while (!fehler) {
            if (späterAnzahl > 0) { int zielobjektAdresse = zeitplanSpäter[0], Deutsch = späterKoreanischWert[0]; for (int schleifeIndex = 1; schleifeIndex < späterAnzahl; schleifeIndex++) { zeitplanSpäter[schleifeIndex - 1] = zeitplanSpäter[schleifeIndex]; späterKoreanischWert[schleifeIndex - 1] = späterKoreanischWert[schleifeIndex]; } zeitplanSpäter[--späterAnzahl] = 0; späterKoreanischWert[späterAnzahl] = 0; zustellenEreignis(zielobjektAdresse, 0, Deutsch != 0); continue; }
            if (Benutzer.bildschirmVerbindung(6, 0, 0, 0, 0, 0) == 0) return;
            int ereignisNummer = Benutzer.bildschirmVerbindung(5, 0, 0, 0, 0, 0); if (ereignisNummer == 0) continue;
            if (ereignisNummer < 0) { fehlschlagWert("GUI event I/O failed"); return; }
            int identitätWert = ereignisNummer & 65535; if (identitätWert < 1 || identitätWert > 32) continue; int objektVerweis = bildschirmVerweis[identitätWert - 1]; if (objektVerweis == 0) continue;
            if ((ereignisNummer & 65536) != 0) {
                if (speicherhaldeWert[objektVerweis + 10] != 0) speicherhaldeWert[objektVerweis + 9] = 0;
                if (speicherhaldeWert[objektVerweis + 10] == 3) for (int schleifeIndex = 0; schleifeIndex < 32; schleifeIndex++) if (bildschirmVerweis[schleifeIndex] != 0 && speicherhaldeWert[bildschirmVerweis[schleifeIndex]] == 24) Benutzer.bildschirmVerbindung(4, schleifeIndex + 1, 0, 0, 0, 0);
            } else if (speicherhaldeWert[objektVerweis + 4] != 0) {
                int liesmichVerweis = speichergerätZuteilen(29, 2); if (fehler) return; speicherhaldeWert[liesmichVerweis + 2] = objektVerweis; speicherhaldeWert[liesmichVerweis + 3] = speicherhaldeWert[objektVerweis + 12]; speicherhaldeVerweis[liesmichVerweis + 2] = 1; zustellenEreignis(speicherhaldeWert[objektVerweis + 4], liesmichVerweis, speicherhaldeWert[objektVerweis + 12] != 0);
            }
        }
    }
    public static int ausführenVorgang() {
        if (Benutzer.argumenteAnzahl() == 1 && JavaWerkzeug.gleichText(Benutzer.argumente(0), "-version")) {
            Benutzer.schreiben("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (Benutzer.argumenteAnzahl() < 1) { Benutzer.schreiben("Usage: java CLASS [ARGS]\n"); return 2; }
        eintragKlasseDefinition = klasseDefinitionLaden(wirtssystemZeichen(Benutzer.argumente(0))); if (fehler || eintragKlasseDefinition < 0) return 1;
        int eintragPunktWert = nameMethode(eintragKlasseDefinition, "ausführenVorgang", "()V");
        boolean koreanischEintrag = eintragPunktWert >= 0 && (methodeZugriff[eintragPunktWert] & 9) == 9;
        if (!koreanischEintrag) eintragPunktWert = nameMethode(eintragKlasseDefinition, "main", "([Ljava/lang/String;)V");
        if (eintragPunktWert < 0 || (methodeZugriff[eintragPunktWert] & 9) != 9) fehlschlagWert("public static void ausführenVorgang() or main(String[] args) required");
        if (fehler) return 1;
        int argumente = speichergerätZuteilen(3, Benutzer.argumenteAnzahl() - 1); datenfeldElement[argumente] = -1;
        for (int Zahl = 1; Zahl < Benutzer.argumenteAnzahl() && !fehler; Zahl++) speicherhaldeWert[argumente + 1 + Zahl] = wirtssystemZeichen(Benutzer.argumente(Zahl));
        rahmenIndex = 0; rahmenMethode[0] = eintragPunktWert; rahmenPosition[0] = methodeStarten[eintragPunktWert]; lokalWert[0] = koreanischEintrag ? 0 : argumente; lokalTyp[0] = koreanischEintrag ? 0 : 2;
        ausführungsfadenStatuswert[0] = 1; ausführungsfadenObjekt[0] = speichergerätZuteilen(13, 2);
        befehlAusführen(); if (!fehler) bildschirmEreignisse(); return fehler ? 1 : 0;
    }
}
