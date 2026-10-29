// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class DatenKommunikation {
    static int zifferWert(String Text) {
        if (Text == null || Text.length() == 0) return -1;
        int ergebnis = 0;
        for (int Nummer = 0; Nummer < Text.length(); Nummer++) {
            int Wert = Text.charAt(Nummer) - '0';
            if (Wert < 0 || Wert > 9 || ergebnis > 6553) return -1;
            ergebnis = ergebnis * 10 + Wert;
            if (ergebnis > 65535) return -1;
        }
        return ergebnis;
    }
    static int adresse(String Text) {
        if (Text == null) return 0;
        int Wert = 0, ergebnis = 0, unterteilWert = 0, ziffern = 0;
        for (int Nummer = 0; Nummer <= Text.length(); Nummer++) {
            int Zeichen = Nummer == Text.length() ? '.' : Text.charAt(Nummer);
            if (Zeichen == '.') {
                if (ziffern == 0 || unterteilWert == 4) return 0;
                ergebnis = (ergebnis << 8) | Wert; unterteilWert++; Wert = 0; ziffern = 0;
            } else {
                if (Zeichen < '0' || Zeichen > '9') return 0;
                Wert = Wert * 10 + Zeichen - '0';
                if (++ziffern > 3 || Wert > 255) return 0;
            }
        }
        return unterteilWert == 4 ? ergebnis : 0;
    }
    public static int ausführenVorgang() {
        if (Benutzer.argumenteAnzahl() != 3) { Benutzer.schreiben("Usage: run udp IP PORT TEXT\n"); return 2; }
        int adresse = adresse(Benutzer.argumente(0)), portWert = zifferWert(Benutzer.argumente(1));
        String inhaltswertWert = Benutzer.argumente(2);
        if (adresse == 0 || portWert < 1 || inhaltswertWert.length() > 1024) { Benutzer.schreiben("Bad destination\n"); return 2; }
        int kennwertWert = Benutzer.netzwerkÖffnen(0);
        if (kennwertWert < 0) { Benutzer.schreiben("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] Daten = new int[1024];
        for (int Nummer = 0; Nummer < inhaltswertWert.length(); Nummer++) Daten[Nummer] = inhaltswertWert.charAt(Nummer);
        if (Benutzer.datenSenden(kennwertWert, adresse, portWert, Daten, inhaltswertWert.length()) < 0) {
            Benutzer.schreiben("UDP SEND FAILED\n"); Benutzer.netzwerkSchließen(kennwertWert); return 4;
        }
        Benutzer.schreiben("UDP SENT\n");
        int empfangenWertLänge = Benutzer.datenEmpfangen(kennwertWert, Daten, 1500);
        boolean gleichText = empfangenWertLänge == inhaltswertWert.length() && Benutzer.gesendetAdresse(kennwertWert) == adresse && Benutzer.gesendetPort(kennwertWert) == portWert;
        if (gleichText) for (int Nummer = 0; Nummer < empfangenWertLänge; Nummer++) if (Daten[Nummer] != inhaltswertWert.charAt(Nummer)) gleichText = false;
        Benutzer.netzwerkSchließen(kennwertWert);
        if (empfangenWertLänge < 0) { Benutzer.schreiben("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        Benutzer.schreiben(gleichText ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return gleichText ? 0 : 6;
    }
}
