// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Eingeschränkte JVM in Ring 3. Prüft Datei-, Stapel-, Referenz- und Sprunggrenzen zur Laufzeit. */
public final class VirtuelleJavaMaschine {
    static int[] Datei = new int[16384], dateiNameText = new int[64];
    static int[] konstanteKennzeichen = new int[512], konstanteErsterWert = new int[512], konstanteZweiterWert = new int[512], zeichenketteVerweis = new int[512];
    static int[] methodeNameText = new int[32], methodeTyp = new int[32], methodeZugriff = new int[32];
    static int[] methodeStarten = new int[32], methodeEnde = new int[32], methodeStapel = new int[32], methodeLokalvariablen = new int[32];
    static int[] methodeArgumentAnzahl = new int[32], methodeArgumentTyp = new int[512], methodeZurückkehren = new int[32];
    static int[] grenzstelleWert = new int[16384];
    static int[] lokalWert = new int[4096], lokalTyp = new int[4096], operandStapelWert = new int[4096], operandStapelTyp = new int[4096];
    static int[] rahmenMethode = new int[32], rahmenPosition = new int[32], rahmenStapel = new int[32];
    static int[] speicherhaldeWert = new int[8192];
    static int größe, positionLesen, konstanteAnzahl, methodeAnzahl, klasseName, rahmenIndex = -1, speicherhaldeEndePosition = 1, zurückkehrenTyp;
    static boolean fehler;

    static void fehlschlagWert(String maschinenwortText) {
        if (!fehler) { Benutzer.schreiben("JVM error: "); Benutzer.schreiben(maschinenwortText); Benutzer.zeichenWertSchreiben(10); }
        fehler = true;
    }
    static boolean beschneiden(int ausführenVorgang, int Länge) { return ausführenVorgang >= 0 && Länge >= 0 && ausführenVorgang <= größe - Länge; }
    static int byteWert() {
        if (!beschneiden(positionLesen, 1)) { fehlschlagWert("truncated class file"); return 0; }
        return Datei[positionLesen++];
    }
    static int kurzWert() { return byteWert() << 8 | byteWert(); }
    static int Ganzzahl() { return kurzWert() << 16 | kurzWert(); }
    static void bytesÜberspringen(int Länge) { if (!beschneiden(positionLesen, Länge)) fehlschlagWert("invalid attribute size"); else positionLesen += Länge; }
    static boolean konstantePrüfen(int Zahl, int artWert) {
        if (Zahl <= 0 || Zahl >= konstanteAnzahl || konstanteKennzeichen[Zahl] != artWert) { fehlschlagWert("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean textBereich(int ausführenVorgang, int Länge, String maschinenwortText) {
        if (!beschneiden(ausführenVorgang, Länge) || Länge != maschinenwortText.length()) return false;
        for (int Zahl = 0; Zahl < Länge; Zahl++) if (Datei[ausführenVorgang + Zahl] != maschinenwortText.charAt(Zahl)) return false;
        return true;
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
    static void attributÜberspringen() {
        int elementeintragAnzahl = kurzWert();
        for (int Zahl = 0; Zahl < elementeintragAnzahl && !fehler; Zahl++) { konstantePrüfen(kurzWert(), 1); bytesÜberspringen(Ganzzahl()); }
    }
    static int befehlLänge(int Wert) {
        if (Wert == 16 || Wert == 18 || Wert == 21 || Wert == 25 || Wert == 54 || Wert == 58 || Wert == 188) return 2;
        if (Wert == 17 || Wert == 19 || Wert == 132 || Wert >= 153 && Wert <= 167
            || Wert >= 178 && Wert <= 184 || Wert == 187 || Wert == 189 || Wert == 192 || Wert == 198 || Wert == 199) return 3;
        if (Wert >= 0 && Wert <= 8 || Wert >= 26 && Wert <= 29 || Wert >= 42 && Wert <= 46 || Wert == 50
            || Wert >= 59 && Wert <= 62 || Wert >= 75 && Wert <= 79 || Wert == 83 || Wert == 87 || Wert == 89 || Wert == 95
            || Wert == 96 || Wert == 100 || Wert == 104 || Wert == 108 || Wert == 112 || Wert == 116
            || Wert == 120 || Wert == 122 || Wert == 124 || Wert == 126 || Wert == 128 || Wert == 130
            || Wert >= 145 && Wert <= 147 || Wert == 172 || Wert == 176 || Wert == 177 || Wert == 190) return 1;
        return 0;
    }
    static void klasseLesen() {
        if (Ganzzahl() != 0xcafebabe) fehlschlagWert("not a class file");
        int nebenversionÜberarbeitung = kurzWert(), versionWert = kurzWert();
        if (versionWert < 45 || versionWert > 52 || nebenversionÜberarbeitung != 0) fehlschlagWert("supported class versions: 45..52, minor 0");
        konstanteAnzahl = kurzWert();
        if (konstanteAnzahl < 1 || konstanteAnzahl > 512) { fehlschlagWert("constant pool limit (511)"); return; }
        for (int Zahl = 1; Zahl < konstanteAnzahl && !fehler; Zahl++) {
            int artWert = byteWert(); konstanteKennzeichen[Zahl] = artWert;
            if (artWert == 1) { konstanteZweiterWert[Zahl] = kurzWert(); konstanteErsterWert[Zahl] = positionLesen; bytesÜberspringen(konstanteZweiterWert[Zahl]); }
            else if (artWert == 3) konstanteErsterWert[Zahl] = Ganzzahl();
            else if (artWert == 7 || artWert == 8) konstanteErsterWert[Zahl] = kurzWert();
            else if (artWert == 9 || artWert == 10 || artWert == 12) { konstanteErsterWert[Zahl] = kurzWert(); konstanteZweiterWert[Zahl] = kurzWert(); }
            else fehlschlagWert("unsupported constant type");
        }
        int erlaubnisWert = kurzWert();
        if ((erlaubnisWert & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) fehlschlagWert("unsupported class flags");
        klasseName = klasseNameText(kurzWert());
        if (!maschinenwortText(klasseNameText(kurzWert()), "java/lang/Object")) fehlschlagWert("inheritance unsupported");
        if (kurzWert() != 0) fehlschlagWert("interfaces unsupported");
        if (kurzWert() != 0) fehlschlagWert("fields unsupported");
        methodeAnzahl = kurzWert();
        if (methodeAnzahl < 1 || methodeAnzahl > 32) { fehlschlagWert("method count limit (32)"); return; }
        for (int Zahl = 0; Zahl < methodeAnzahl && !fehler; Zahl++) {
            methodeZugriff[Zahl] = kurzWert(); methodeNameText[Zahl] = kurzWert(); methodeTyp[Zahl] = kurzWert();
            konstantePrüfen(methodeNameText[Zahl], 1); deskriptorLesen(Zahl);
            if ((methodeZugriff[Zahl] & (0x100 | 0x400 | 0x20)) != 0) fehlschlagWert("native, abstract and synchronized methods unsupported");
            if ((methodeZugriff[Zahl] & 8) == 0 && !maschinenwortText(methodeNameText[Zahl], "<init>")) fehlschlagWert("instance methods unsupported");
            if (maschinenwortText(methodeNameText[Zahl], "<clinit>")) fehlschlagWert("class initializers unsupported");
            for (int vorderseiteWert = 0; vorderseiteWert < Zahl; vorderseiteWert++) if (passendMaschinenwort(methodeNameText[vorderseiteWert], methodeNameText[Zahl]) && passendMaschinenwort(methodeTyp[vorderseiteWert], methodeTyp[Zahl])) fehlschlagWert("duplicate method");
            int elementeintragAnzahl = kurzWert();
            for (int attributWert = 0; attributWert < elementeintragAnzahl && !fehler; attributWert++) {
                int Name = kurzWert(), Länge = Ganzzahl(), ausführenVorgang = positionLesen;
                if (!beschneiden(ausführenVorgang, Länge)) { fehlschlagWert("truncated method attribute"); break; }
                if (maschinenwortText(Name, "Code")) {
                    if (methodeStarten[Zahl] != 0) fehlschlagWert("duplicate Code attribute");
                    methodeStapel[Zahl] = kurzWert(); methodeLokalvariablen[Zahl] = kurzWert(); int kodeLänge = Ganzzahl();
                    if (methodeStapel[Zahl] > 128 || methodeLokalvariablen[Zahl] > 128 || methodeLokalvariablen[Zahl] < methodeArgumentAnzahl[Zahl]
                        || kodeLänge < 1 || kodeLänge > 8192) fehlschlagWert("method memory limits exceeded");
                    methodeStarten[Zahl] = positionLesen; bytesÜberspringen(kodeLänge); methodeEnde[Zahl] = positionLesen;
                    if (kurzWert() != 0) fehlschlagWert("exception handlers unsupported");
                    attributÜberspringen();
                    if (positionLesen != ausführenVorgang + Länge) fehlschlagWert("Code attribute size mismatch");
                } else bytesÜberspringen(Länge);
            }
            if (methodeStarten[Zahl] == 0) fehlschlagWert("missing Code attribute");
            int platzEintrag = methodeStarten[Zahl];
            while (platzEintrag < methodeEnde[Zahl] && !fehler) {
                int Länge = befehlLänge(Datei[platzEintrag]);
                if (Länge == 0 || Länge > methodeEnde[Zahl] - platzEintrag) { fehlschlagWert("unsupported or truncated bytecode"); break; }
                grenzstelleWert[platzEintrag] = Zahl + 1; platzEintrag += Länge;
            }
            // Ungültige Sprungziele auch in nie ausgeführten Pfaden abweisen.
            platzEintrag = methodeStarten[Zahl];
            while (platzEintrag < methodeEnde[Zahl] && !fehler) {
                int Wert = Datei[platzEintrag];
                if (Wert >= 153 && Wert <= 167 || Wert == 198 || Wert == 199) {
                    int zielWert = platzEintrag + (short)(Datei[platzEintrag + 1] << 8 | Datei[platzEintrag + 2]);
                    if (zielWert < methodeStarten[Zahl] || zielWert >= methodeEnde[Zahl] || grenzstelleWert[zielWert] != Zahl + 1) fehlschlagWert("invalid branch target");
                }
                platzEintrag += befehlLänge(Wert);
            }
        }
        if (!fehler) attributÜberspringen();
        if (positionLesen != größe) fehlschlagWert("extra class file data");
    }
    static int speichergerätZuteilen(int artWert, int Länge) {
        if (Länge < 0 || Länge > speicherhaldeWert.length - speicherhaldeEndePosition - 2) { fehlschlagWert("object heap exhausted or negative array size"); return 0; }
        int verweis = speicherhaldeEndePosition; speicherhaldeEndePosition += Länge + 2; speicherhaldeWert[verweis] = artWert; speicherhaldeWert[verweis + 1] = Länge;
        return verweis;
    }
    static boolean objektWert(int verweis, int artWert) {
        if (verweis < 1 || verweis >= speicherhaldeEndePosition - 1 || speicherhaldeWert[verweis] != artWert) { fehlschlagWert("null or invalid object reference"); return false; }
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
        if (rahmenIndex == 31) { fehlschlagWert("call stack limit (32)"); return; }
        int nächsterElementeintrag = rahmenIndex + 1;
        for (int Zahl = 0; Zahl < 128; Zahl++) lokalTyp[nächsterElementeintrag * 128 + Zahl] = 0;
        for (int Zahl = methodeArgumentAnzahl[Funktion] - 1; Zahl >= 0; Zahl--) {
            lokalWert[nächsterElementeintrag * 128 + Zahl] = werteSubtrahieren(methodeArgumentTyp[Funktion * 16 + Zahl]); lokalTyp[nächsterElementeintrag * 128 + Zahl] = methodeArgumentTyp[Funktion * 16 + Zahl];
        }
        rahmenIndex = nächsterElementeintrag; rahmenMethode[rahmenIndex] = Funktion; rahmenPosition[rahmenIndex] = methodeStarten[Funktion]; rahmenStapel[rahmenIndex] = 0;
    }
    static void zurückkehrenErgebnis(int typWert) {
        if (typWert != methodeZurückkehren[rahmenMethode[rahmenIndex]]) { fehlschlagWert("return type mismatch"); return; }
        int Wert = typWert == 0 ? 0 : werteSubtrahieren(typWert);
        rahmenIndex--; if (rahmenIndex >= 0 && typWert != 0) wertAblegen(Wert, typWert);
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
                if (Wert < 1 || Wert > 127) { fehlschlagWert("file stream paths currently require ASCII"); return; }
                datenstromDateiName[platzEintrag] = Wert;
            }
            datenstromDateiName[Länge] = 0;
            int deskriptorEintrag = Benutzer.dateiDeskriptorÖffnen(datenstromDateiName, Ausgabe ? (fortsetzungWert ? 1089 : 577) : 0);
            if (deskriptorEintrag < 0) { fehlschlagWert("FileNotFoundException: file open failed"); return; }
            speicherhaldeWert[datenstromWert + 2] = deskriptorEintrag; speicherhaldeWert[datenstromWert + 3] = 1;
            return;
        }
        if (befehl != 182) { fehlschlagWert("invalid file stream invocation"); return; }
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
            if (ergebnis < -1) fehlschlagWert("IOException: read failed"); else wertAblegen(ergebnis, 1);
        } else if (Benutzer.einsDateiByteSchreiben(deskriptorEintrag, Wert) != 1) fehlschlagWert("IOException: write failed");
    }
    static void methodeAufrufVorgang(int Nummer, int befehl) {
        if (!konstantePrüfen(Nummer, 10)) return;
        int eigentümerWert = klasseNameText(konstanteErsterWert[Nummer]), Name = verweisName(konstanteZweiterWert[Nummer]), formatWert = verweisTyp(konstanteZweiterWert[Nummer]);
        if (fehler) return;
        if (passendMaschinenwort(eigentümerWert, klasseName)) {
            if (befehl != 184) { fehlschlagWert("only static user methods are supported"); return; }
            for (int Zahl = 0; Zahl < methodeAnzahl; Zahl++) if (passendMaschinenwort(Name, methodeNameText[Zahl]) && passendMaschinenwort(formatWert, methodeTyp[Zahl])) {
                if ((methodeZugriff[Zahl] & 8) == 0) fehlschlagWert("method is not static"); else aufrufen(Zahl);
                return;
            }
            fehlschlagWert("NoSuchMethodError"); return;
        }
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
        fehlschlagWert("unsupported library method");
    }
    static int datenfeldPlatz(int verweis, int feldindexWert, int typWert) {
        if (!objektWert(verweis, typWert)) return 0;
        if (feldindexWert < 0 || feldindexWert >= speicherhaldeWert[verweis + 1]) { fehlschlagWert("ArrayIndexOutOfBoundsException"); return 0; }
        return verweis + 2 + feldindexWert;
    }
    static void befehlAusführen() {
        int restwertDaten = 500000;
        while (rahmenIndex >= 0 && !fehler) {
            if (--restwertDaten == 0) { fehlschlagWert("instruction limit (500000)"); break; }
            int ausführenVorgang = rahmenPosition[rahmenIndex], Wert = befehlscodeByteLesen();
            if (fehler) break;
            if (Wert == 0) continue;
            if (Wert == 1) { wertAblegen(0, 2); continue; }
            if (Wert >= 2 && Wert <= 8) { wertAblegen(Wert - 3, 1); continue; }
            if (Wert == 16) { wertAblegen((byte)befehlscodeByteLesen(), 1); continue; }
            if (Wert == 17) { wertAblegen((short)befehlscodeKurzLesen(), 1); continue; }
            if (Wert == 18 || Wert == 19) {
                int Zahl = Wert == 18 ? befehlscodeByteLesen() : befehlscodeKurzLesen();
                if (Zahl <= 0 || Zahl >= konstanteAnzahl) fehlschlagWert("invalid ldc constant");
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
            if (Wert == 46 || Wert == 50) {
                int feldindexWert = werteSubtrahieren(1), verweis = werteSubtrahieren(2), platzEintrag = datenfeldPlatz(verweis, feldindexWert, Wert == 46 ? 2 : 3);
                if (!fehler) wertAblegen(speicherhaldeWert[platzEintrag], Wert == 46 ? 1 : 2); continue;
            }
            if (Wert == 79 || Wert == 83) {
                int elementeintragElement = werteSubtrahieren(Wert == 79 ? 1 : 2), feldindexWert = werteSubtrahieren(1), verweis = werteSubtrahieren(2), platzEintrag = datenfeldPlatz(verweis, feldindexWert, Wert == 79 ? 2 : 3);
                if (Wert == 83 && elementeintragElement != 0) objektWert(elementeintragElement, 1);
                if (!fehler) speicherhaldeWert[platzEintrag] = elementeintragElement; continue;
            }
            if (Wert == 87) { werteSubtrahieren(0); continue; }
            if (Wert == 89) { int ersterOperand = werteSubtrahieren(0), typWert = zurückkehrenTyp; wertAblegen(ersterOperand, typWert); wertAblegen(ersterOperand, typWert); continue; }
            if (Wert == 95) { int ersterOperand = werteSubtrahieren(0), ersterOperandTyp = zurückkehrenTyp, zweiterOperand = werteSubtrahieren(0), zweiterOperandTyp = zurückkehrenTyp; wertAblegen(ersterOperand, ersterOperandTyp); wertAblegen(zweiterOperand, zweiterOperandTyp); continue; }
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
            if (Wert == 178) {
                int Zahl = befehlscodeKurzLesen(); if (!konstantePrüfen(Zahl, 9)) continue;
                if (!maschinenwortText(klasseNameText(konstanteErsterWert[Zahl]), "java/lang/System") || !maschinenwortText(verweisName(konstanteZweiterWert[Zahl]), "out")
                    || !maschinenwortText(verweisTyp(konstanteZweiterWert[Zahl]), "Ljava/io/PrintStream;")) fehlschlagWert("unsupported static field");
                else wertAblegen(-1, 2); continue;
            }
            if (Wert == 182 || Wert == 183 || Wert == 184) { methodeAufrufVorgang(befehlscodeKurzLesen(), Wert); continue; }
            if (Wert == 187) {
                int Name = klasseNameText(befehlscodeKurzLesen());
                if (maschinenwortText(Name, "java/lang/StringBuilder")) wertAblegen(speichergerätZuteilen(4, 1), 2);
                else if (maschinenwortText(Name, "java/io/FileInputStream") || maschinenwortText(Name, "java/io/FileOutputStream")) {
                    int verweis = speichergerätZuteilen(maschinenwortText(Name, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!fehler) { speicherhaldeWert[verweis + 2] = -1; wertAblegen(verweis, 2); }
                } else fehlschlagWert("unsupported object construction");
                continue;
            }
            if (Wert == 188 || Wert == 189) {
                if (Wert == 188) { if (befehlscodeByteLesen() != 10) fehlschlagWert("only int[] newarray is supported"); }
                else if (!maschinenwortText(klasseNameText(befehlscodeKurzLesen()), "java/lang/String")) fehlschlagWert("only String[] anewarray is supported");
                int Länge = werteSubtrahieren(1); wertAblegen(speichergerätZuteilen(Wert == 188 ? 2 : 3, Länge), 2); continue;
            }
            if (Wert == 190) {
                int verweis = werteSubtrahieren(2);
                if (verweis < 1 || verweis >= speicherhaldeEndePosition - 1 || (speicherhaldeWert[verweis] != 2 && speicherhaldeWert[verweis] != 3)) fehlschlagWert("null or invalid array");
                else wertAblegen(speicherhaldeWert[verweis + 1], 1); continue;
            }
            if (Wert == 192) {
                int Name = klasseNameText(befehlscodeKurzLesen()), verweis = werteSubtrahieren(2);
                if (!maschinenwortText(Name, "java/lang/String")) fehlschlagWert("unsupported checkcast");
                else if (verweis != 0) objektWert(verweis, 1);
                wertAblegen(verweis, 2); continue;
            }
            fehlschlagWert("unsupported bytecode");
        }
    }
    public static int ausführenVorgang() {
        if (Benutzer.argumenteAnzahl() == 1 && JavaWerkzeug.gleichText(Benutzer.argumente(0), "-version")) {
            Benutzer.schreiben("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (Benutzer.argumenteAnzahl() < 1) { Benutzer.schreiben("Usage: java CLASS [ARGS]\n"); return 2; }
        int Länge = JavaWerkzeug.Name(dateiNameText, Benutzer.argumente(0));
        if (Länge < 1 || Länge > 57) { Benutzer.schreiben("java: invalid class name\n"); return 2; }
        dateiNameText[Länge] = '.'; dateiNameText[Länge + 1] = 'c'; dateiNameText[Länge + 2] = 'l'; dateiNameText[Länge + 3] = 'a'; dateiNameText[Länge + 4] = 's'; dateiNameText[Länge + 5] = 's';
        größe = Benutzer.dateiLesen(dateiNameText, Datei);
        if (größe < 0) { Benutzer.schreiben("java: cannot read class: "); JavaWerkzeug.nummerSchreiben(größe); Benutzer.zeichenWertSchreiben(10); return 1; }
        klasseLesen(); if (fehler) return 1;
        int zeichenName = konstanteText(klasseName);
        if (!fehler && speicherhaldeWert[zeichenName + 1] != Länge) fehlschlagWert("class name does not match file");
        for (int Zahl = 0; Zahl < Länge && !fehler; Zahl++) if (speicherhaldeWert[zeichenName + 2 + Zahl] != dateiNameText[Zahl]) fehlschlagWert("class name does not match file");
        int eintragPunktWert = -1;
        for (int Zahl = 0; Zahl < methodeAnzahl; Zahl++) if (maschinenwortText(methodeNameText[Zahl], "main") && maschinenwortText(methodeTyp[Zahl], "([Ljava/lang/String;)V") && (methodeZugriff[Zahl] & 9) == 9) eintragPunktWert = Zahl;
        if (eintragPunktWert < 0) fehlschlagWert("public static void main(String[] args) required");
        if (fehler) return 1;
        int argumente = speichergerätZuteilen(3, Benutzer.argumenteAnzahl() - 1);
        for (int Zahl = 1; Zahl < Benutzer.argumenteAnzahl() && !fehler; Zahl++) speicherhaldeWert[argumente + 1 + Zahl] = wirtssystemZeichen(Benutzer.argumente(Zahl));
        rahmenIndex = 0; rahmenMethode[0] = eintragPunktWert; rahmenPosition[0] = methodeStarten[eintragPunktWert]; lokalWert[0] = argumente; lokalTyp[0] = 2;
        befehlAusführen(); return fehler ? 1 : 0;
    }
}
