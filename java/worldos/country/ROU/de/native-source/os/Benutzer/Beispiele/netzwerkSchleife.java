// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Prüft das tatsächliche Umlaufen des RTL8139-Empfangsrings mit maximal großen und ungerade langen Datagrammen. */
public final class netzwerkSchleife {
    public static int ausführenVorgang() {
        if (Benutzer.argumenteAnzahl() != 1) { Benutzer.schreiben("Usage: run stress PORT\n"); return 2; }
        String Text = Benutzer.argumente(0);
        int portWert = 0;
        for (int Nummer = 0; Nummer < Text.length(); Nummer++) {
            if (Text.charAt(Nummer) < '0' || Text.charAt(Nummer) > '9' || portWert > 6553) return 2;
            portWert = portWert * 10 + Text.charAt(Nummer) - '0';
        }
        if (portWert < 1 || portWert > 65535) return 2;
        int kennwertWert = Benutzer.netzwerkÖffnen(0);
        if (kennwertWert < 0) return 3;
        int[] Daten = new int[1024];
        for (int wiederholungsschrittOrdnungszahl = 0; wiederholungsschrittOrdnungszahl < 24; wiederholungsschrittOrdnungszahl++) {
            int Länge = 1024 - (wiederholungsschrittOrdnungszahl & 1);
            for (int Nummer = 0; Nummer < Länge; Nummer++) Daten[Nummer] = (Nummer + wiederholungsschrittOrdnungszahl) & 255;
            if (Benutzer.datenSenden(kennwertWert, 0x0a000202, portWert, Daten, Länge) != Länge) return 4;
            if (Benutzer.datenEmpfangen(kennwertWert, Daten, 300) != Länge) return 5;
            for (int Nummer = 0; Nummer < Länge; Nummer++) if (Daten[Nummer] != ((Nummer + wiederholungsschrittOrdnungszahl) & 255)) return 6;
        }
        Benutzer.netzwerkSchließen(kennwertWert);
        Benutzer.schreiben("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
