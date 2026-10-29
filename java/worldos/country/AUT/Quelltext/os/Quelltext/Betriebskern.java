// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Java-Einstieg nach dem tatsächlichen Systemstart, unabhängig von JVM und Host-Betriebssystem. */
public final class Betriebskern {
    static int gesamtwertWert(int endung) {
        int summeWert = 0;
        for (int Nummer = 1; Nummer <= endung; Nummer++) summeWert += Nummer;
        return summeWert;
    }

    static boolean Prüfungen() {
        int[] werte = new int[4];
        werte[2] = gesamtwertWert(10);
        int negativWert = -7;
        int mindestwertWert = 0x80000000;
        int divisionErgebnis = -1;
        int Nummer = Speicherraum.speichergerätZuteilen();
        boolean durchgangWert = werte[0] == 0 && werte[2] == 55 && werte.length == 4
            && negativWert / 3 == -2 && negativWert % 3 == -1 && mindestwertWert / divisionErgebnis == mindestwertWert
            && mindestwertWert % divisionErgebnis == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && Nummer >= 0 && Speicherraum.zurückkehrenErgebnis(Nummer) && !Speicherraum.zurückkehrenErgebnis(Nummer);
        Zeichenterminal.schreiben(durchgangWert ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return durchgangWert;
    }

    public static void ausführenVorgang() {
        Zeichenterminal.vorbereiten();
        Zeichenterminal.schreiben("JKOROS NATIVE JAVA\n");
        Zeichenterminal.schreiben("Java 기계어 betriebskernWert ausführenVorgang\n");
        if (Gerät.startvorgangMarkierung() != 0x2badb002) {
            Zeichenterminal.schreiben("BAD MULTIBOOT MAGIC\n");
            Gerät.anhaltenAusführung();
        }
        if (!Prüfungen()) Gerät.anhaltenAusführung();
        if (Speicherraum.obererSpeicherGröße() < 15360) {
            Zeichenterminal.schreiben("At least 16 MiB RAM required\n");
            Gerät.anhaltenAusführung();
        }
        Gerät.benutzerProgrammVorbereiten();
        Zeichenterminal.schreiben("USER ELF: ring 3 / paging / int 0x80\n");
        Netzwerktreiber.vorbereiten();
        Netzwerkstapel.bereinigenProzess();
        ArbeitsspeicherDateisystem.vorbereiten();
        Dateibeständigkeit.vorbereiten();
        Befehlsinterpreter.ausführenVorgang();
    }
}
