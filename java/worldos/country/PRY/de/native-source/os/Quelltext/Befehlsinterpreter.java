// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Kleiner serieller/PS2-Befehlsinterpreter ohne Plattenschreibzugriffe. */
public final class Befehlsinterpreter {
    static int[] Eingabewert = new int[128];
    static int Länge = 0;
    static boolean zurückkehrenNachVorherigZeile = false;
    static boolean zeileÜberlauf = false;

    static boolean befehl(String Name) {
        if (Länge < Name.length()) return false;
        for (int Nummer = 0; Nummer < Name.length(); Nummer++)
            if (Eingabewert[Nummer] != Name.charAt(Nummer)) return false;
        return Länge == Name.length() || Eingabewert[Name.length()] == ' ';
    }

    static void hilfeAnzeigen() {
        Zeichenterminal.schreiben("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        Zeichenterminal.schreiben("apps | run NAME [ARGS] | net\n");
        Zeichenterminal.schreiben("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        Zeichenterminal.schreiben("sync (연결된 JKSTORE1 ablegenDatenWert 장치에 Datei 보존)\n");
    }

    static void prozessWertEintrag() {
        if (Länge == 0) return;
        if (befehl("help")) hilfeAnzeigen();
        else if (befehl("sync")) {
            int ergebnis = Dateibeständigkeit.synchronisieren();
            Zeichenterminal.schreiben("Sync: "); Zeichenterminal.nummerSchreiben(ergebnis); Zeichenterminal.Zeichen(10);
        }
        else if (befehl("ls")) ArbeitsspeicherDateisystem.eintragListe();
        else if (befehl("edit")) ArbeitsspeicherDateisystem.befehl(Eingabewert, 4, Länge, 0);
        else if (befehl("cat")) ArbeitsspeicherDateisystem.befehl(Eingabewert, 3, Länge, 1);
        else if (befehl("rm")) ArbeitsspeicherDateisystem.befehl(Eingabewert, 2, Länge, 2);
        else if (befehl("java") || befehl("javac")) {
            int ergebnis = Ausführungsverwaltung.befehlAusführen(Eingabewert, 0, Länge);
            Zeichenterminal.schreiben("Exit: "); Zeichenterminal.nummerSchreiben(ergebnis); Zeichenterminal.Zeichen(10);
        }
        else if (befehl("apps")) Ausführungsverwaltung.eintragListe();
        else if (befehl("net")) Netzwerkstapel.statuswertWert();
        else if (befehl("run")) {
            int ergebnis = Ausführungsverwaltung.befehlAusführen(Eingabewert, 3, Länge);
            Zeichenterminal.schreiben("Exit: "); Zeichenterminal.nummerSchreiben(ergebnis); Zeichenterminal.schreiben("\n");
        } else if (befehl("info")) {
            Zeichenterminal.schreiben("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (befehl("mem")) {
            Zeichenterminal.schreiben("obererSeiteRand Speicher adresseGebiet(KiB): "); Zeichenterminal.nummerSchreiben(Speicherraum.obererSpeicherGröße());
            Zeichenterminal.schreiben("\n배열 동적 Speicher adresseGebiet(byteWert): "); Zeichenterminal.nummerSchreiben(Gerät.datenfeldNutzung());
            Zeichenterminal.schreiben(" / 262144\n작업 adresseGebiet abschnittWert: "); Zeichenterminal.nummerSchreiben(Speicherraum.benutztEintragAnzahl());
            Zeichenterminal.schreiben(" / 8 (각 4096바이트)\n");
        } else if (befehl("alloc")) {
            int Nummer = Speicherraum.speichergerätZuteilen();
            Zeichenterminal.schreiben("abschnittWert Nummer: "); Zeichenterminal.nummerSchreiben(Nummer); Zeichenterminal.schreiben("\n");
        } else if (befehl("free")) {
            if (Länge == 6 && Eingabewert[4] == ' ' && Eingabewert[5] >= '0' && Eingabewert[5] <= '7') {
                Zeichenterminal.schreiben(Speicherraum.zurückkehrenErgebnis(Eingabewert[5] - '0') ? "반환됨\n" : "할당되지 않은 abschnittWert\n");
            } else Zeichenterminal.schreiben("사용법: free 0..7\n");
        } else if (befehl("echo")) {
            for (int Nummer = 5; Nummer < Länge; Nummer++) Zeichenterminal.Zeichen(Eingabewert[Nummer]);
            Zeichenterminal.Zeichen(10);
        } else if (befehl("clear")) Zeichenterminal.eintragTilgen();
        else if (befehl("test")) Betriebskern.Prüfungen();
        else if (befehl("halt")) {
            Zeichenterminal.schreiben("HALTED\n");
            Gerät.anhaltenAusführung();
        } else Zeichenterminal.schreiben("알 Zahl 없는 명령입니다. help를 입력하세요.\n");
    }

    static void undSchreibenAnnehmen(int Wert) {
        if (Wert == 10 && zurückkehrenNachVorherigZeile) { zurückkehrenNachVorherigZeile = false; return; }
        zurückkehrenNachVorherigZeile = Wert == 13;
        if (Wert == 10 || Wert == 13) {
            Zeichenterminal.Zeichen(10);
            if (ArbeitsspeicherDateisystem.istBearbeitend) ArbeitsspeicherDateisystem.bearbeitetZeile(Eingabewert, Länge, zeileÜberlauf);
            else prozessWertEintrag();
            Länge = 0;
            zeileÜberlauf = false;
            Zeichenterminal.schreiben(ArbeitsspeicherDateisystem.istBearbeitend ? "...> " : "jkoros> ");
        } else if (Wert == 8 || Wert == 127) {
            if (Länge > 0) {
                Länge--;
                Zeichenterminal.seriellByte(8); Zeichenterminal.seriellByte(32); Zeichenterminal.seriellByte(8);
                Zeichenterminal.bildschirmZeichen(8);
            }
        } else if (Wert >= 32 && Wert < 127 && Länge < Eingabewert.length) {
            Eingabewert[Länge++] = Wert;
            Zeichenterminal.Zeichen(Wert);
        } else if (Wert >= 32 && Wert < 127) zeileÜberlauf = true;
    }

    static void ausführenVorgang() {
        hilfeAnzeigen();
        Zeichenterminal.schreiben("READY\njkoros> ");
        while (true) {
            int Wert = Zeichenterminal.seriellLesen();
            if (Wert < 0) Wert = Tastatur.lesen();
            if (Wert >= 0) undSchreibenAnnehmen(Wert);
            else { Netzwerkstapel.überprüfen(); Gerät.kurzzeitigTunAbgeben(); }
        }
    }
}
