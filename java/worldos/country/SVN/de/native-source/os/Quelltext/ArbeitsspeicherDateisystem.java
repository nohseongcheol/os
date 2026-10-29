// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Acht Dateien bleiben während der Sitzung erhalten. Fehler beim Bearbeiten oder Übersetzen bewahren vorhandene Dateien. */
public final class ArbeitsspeicherDateisystem {
    static final int höchstwertGröße = 16384;
    static int[] namenListe = new int[8 * 64];
    static int[] größeListe = new int[8];
    static int[] anzahlÖffnen = new int[8], erlaubnisBerechtigungen = new int[8];
    static int[] Name = new int[64];
    static int[] bearbeitenWert = new int[höchstwertGröße];
    static boolean istBearbeitend = false;
    static boolean überlaufWert = false;
    static int bearbeitenGröße = 0;

    static boolean namePrüfen(int[] zeichenWert, int Länge) {
        if (Länge < 1 || Länge > 63) return false;
        for (int Zahl = 0; Zahl < Länge; Zahl++) {
            int Wert = zeichenWert[Zahl];
            if (!(Wert >= 'a' && Wert <= 'z') && !(Wert >= 'A' && Wert <= 'Z')
                && !(Wert >= '0' && Wert <= '9') && Wert != '_' && Wert != '-' && Wert != '.') return false;
        }
        return zeichenWert[0] != '.';
    }

    static int eintragFinden(int[] zeichenWert, int Länge) {
        if (!namePrüfen(zeichenWert, Länge)) return -22;
        for (int Zahl = 0; Zahl < 8; Zahl++) {
            boolean gleichText = namenListe[Zahl * 64 + Länge] == 0;
            for (int platzEintrag = 0; platzEintrag < Länge; platzEintrag++) if (namenListe[Zahl * 64 + platzEintrag] != zeichenWert[platzEintrag]) gleichText = false;
            if (gleichText) return Zahl;
        }
        return -2;
    }

    static int ablegenDatenWert(int[] zeichenWert, int Länge, int[] Daten, int größe) {
        if (!namePrüfen(zeichenWert, Länge) || größe < 0 || größe > Daten.length) return -22;
        if (größe > höchstwertGröße) return -90;
        int Nummer = eintragFinden(zeichenWert, Länge);
        if (Nummer == -2) {
            for (int Zahl = 0; Zahl < 8 && Nummer < 0; Zahl++) if (namenListe[Zahl * 64] == 0 && anzahlÖffnen[Zahl] == 0) Nummer = Zahl;
            if (Nummer >= 0) erlaubnisBerechtigungen[Nummer] = 438;
        }
        if (Nummer < 0) return -28;
        int adresse = Gerät.dateiSpeicher() + Nummer * höchstwertGröße;
        for (int Zahl = 0; Zahl < größe; Zahl++) Gerät.speicherSchreiben(adresse + Zahl, Daten[Zahl]);
        for (int Zahl = 0; Zahl < 64; Zahl++) namenListe[Nummer * 64 + Zahl] = Zahl < Länge ? zeichenWert[Zahl] : 0;
        größeListe[Nummer] = größe;
        return größe;
    }

    static void eintragListe() {
        for (int Zahl = 0; Zahl < 8; Zahl++) if (namenListe[Zahl * 64] != 0) {
            for (int platzEintrag = 0; platzEintrag < 64 && namenListe[Zahl * 64 + platzEintrag] != 0; platzEintrag++) Zeichenterminal.Zeichen(namenListe[Zahl * 64 + platzEintrag]);
            Zeichenterminal.schreiben("  "); Zeichenterminal.nummerSchreiben(größeListe[Zahl]); Zeichenterminal.schreiben("byteWert\n");
        }
        Zeichenterminal.schreiben(Speichergeräteanschluss.istVerfügbar ? "Datei 8칸, 파일당 16384바이트; sync로 ablegenDatenWert 장치에 보존\n"
            : "vorläufigWert Datei 8칸, 파일당 16384바이트; erneutVersuchenWert 시작하면 사라짐\n");
    }

    static void befehl(int[] Eingabewert, int ausführenVorgang, int Länge, int aktion) {
        while (ausführenVorgang < Länge && Eingabewert[ausführenVorgang] == ' ') ausführenVorgang++;
        int endung = Länge;
        while (endung > ausführenVorgang && Eingabewert[endung - 1] == ' ') endung--;
        int Zahl = endung - ausführenVorgang;
        if (Zahl < 1 || Zahl > 63) { Zeichenterminal.schreiben("올바르지 않은 Datei Name\n"); return; }
        for (int platzEintrag = 0; platzEintrag < 64; platzEintrag++) Name[platzEintrag] = platzEintrag < Zahl ? Eingabewert[ausführenVorgang + platzEintrag] : 0;
        int Nummer = eintragFinden(Name, Zahl);
        if (Nummer == -22) { Zeichenterminal.schreiben("올바르지 않은 Datei Name\n"); return; }
        if (aktion == 0) {
            istBearbeitend = true; bearbeitenGröße = 0; überlaufWert = false;
            Zeichenterminal.schreiben("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (Nummer < 0) Zeichenterminal.schreiben("파일을 찾을 Zahl 없습니다\n");
        else if (aktion == 1) {
            int adresse = Gerät.dateiSpeicher() + Nummer * höchstwertGröße;
            for (int platzEintrag = 0; platzEintrag < größeListe[Nummer]; platzEintrag++) Zeichenterminal.Zeichen(Gerät.speicherLesen(adresse + platzEintrag));
            Zeichenterminal.Zeichen(10);
        } else { namenListe[Nummer * 64] = 0; größeListe[Nummer] = 0; Zeichenterminal.schreiben("파일을 지웠습니다\n"); }
    }

    static boolean istExakt(int[] Eingabewert, int Länge, String wortgruppeWert) {
        if (Länge != wortgruppeWert.length()) return false;
        for (int platzEintrag = 0; platzEintrag < Länge; platzEintrag++) if (Eingabewert[platzEintrag] != wortgruppeWert.charAt(platzEintrag)) return false;
        return true;
    }

    static void bearbeitetZeile(int[] Eingabewert, int Länge, boolean zeileÜberlauf) {
        if (istExakt(Eingabewert, Länge, ".cancel")) {
            istBearbeitend = false; Zeichenterminal.schreiben("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (istExakt(Eingabewert, Länge, ".save")) {
            istBearbeitend = false;
            if (überlaufWert) { Zeichenterminal.schreiben("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int Zahl = 0;
            while (Zahl < 64 && Name[Zahl] != 0) Zahl++;
            int ergebnis = ablegenDatenWert(Name, Zahl, bearbeitenWert, bearbeitenGröße);
            Zeichenterminal.schreiben(ergebnis >= 0 ? "보존한 byteWert Zahl: " : "보존 fehlschlagWert: ");
            Zeichenterminal.nummerSchreiben(ergebnis); Zeichenterminal.Zeichen(10);
        } else if (zeileÜberlauf || Länge + 1 > höchstwertGröße - bearbeitenGröße) überlaufWert = true;
        else {
            for (int Zahl = 0; Zahl < Länge; Zahl++) bearbeitenWert[bearbeitenGröße++] = Eingabewert[Zahl];
            bearbeitenWert[bearbeitenGröße++] = 10;
        }
    }

    static void Beispiele(String Datei, String inhaltswertWert) {
        for (int Zahl = 0; Zahl < 64; Zahl++) Name[Zahl] = Zahl < Datei.length() ? Datei.charAt(Zahl) : 0;
        for (int Zahl = 0; Zahl < inhaltswertWert.length(); Zahl++) bearbeitenWert[Zahl] = inhaltswertWert.charAt(Zahl);
        ablegenDatenWert(Name, Datei.length(), bearbeitenWert, inhaltswertWert.length());
    }

    static void vorbereiten() {
        Beispiele("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int gruppeWert = Gerät.javaDateiBündel(), größe = Gerät.javaDateiBündelGröße();
        if (größe < 8 || Ausführungsverwaltung.Zahl(gruppeWert) != 0x464a4b4a) { Zeichenterminal.schreiben("올바르지 않은 Java Datei gruppeWert\n"); return; }
        int elementeintragAnzahl = Ausführungsverwaltung.Zahl(gruppeWert + 4);
        if (elementeintragAnzahl < 0 || elementeintragAnzahl > 8 || elementeintragAnzahl > (größe - 8) / 72) { Zeichenterminal.schreiben("올바르지 않은 Java Datei eintragListe\n"); return; }
        for (int Zahl = 0; Zahl < elementeintragAnzahl; Zahl++) {
            int eintragWert = gruppeWert + 8 + Zahl * 72, Länge = 0;
            for (int platzEintrag = 0; platzEintrag < 64; platzEintrag++) Name[platzEintrag] = Gerät.speicherLesen(eintragWert + platzEintrag);
            while (Länge < 64 && Name[Länge] != 0) Länge++;
            int position = Ausführungsverwaltung.Zahl(eintragWert + 64), dateiGröße = Ausführungsverwaltung.Zahl(eintragWert + 68);
            if (!namePrüfen(Name, Länge) || dateiGröße < 0 || dateiGröße > höchstwertGröße || position < 8 + elementeintragAnzahl * 72 || position > größe - dateiGröße) {
                Zeichenterminal.schreiben("올바르지 않은 Java Datei eintragWert\n"); return;
            }
            for (int platzEintrag = 0; platzEintrag < dateiGröße; platzEintrag++) bearbeitenWert[platzEintrag] = Gerät.speicherLesen(gruppeWert + position + platzEintrag);
            if (ablegenDatenWert(Name, Länge, bearbeitenWert, dateiGröße) < 0) { Zeichenterminal.schreiben("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
