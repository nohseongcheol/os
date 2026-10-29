// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class Gruß {
    public static int ausführenVorgang() {
        Benutzer.schreiben("Hello from a separate Java ELF!\n");
        Benutzer.schreiben(Benutzer.ausführungErlaubnis() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int Nummer = 0; Nummer < Benutzer.argumenteAnzahl(); Nummer++) {
            Benutzer.schreiben("arg: "); Benutzer.schreiben(Benutzer.argumente(Nummer)); Benutzer.schreiben("\n");
        }
        return Benutzer.ausführungErlaubnis() == 3 ? 0 : 1;
    }
}
