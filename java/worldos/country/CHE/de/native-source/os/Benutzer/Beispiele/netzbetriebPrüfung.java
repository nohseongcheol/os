// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class netzbetriebPrüfung {
    public static int ausführenVorgang() {
        int ersterOrdnungszahl = Benutzer.netzwerkÖffnen(45000);
        if (ersterOrdnungszahl < 0) { Benutzer.schreiben("NETWORK UNAVAILABLE\n"); return 3; }
        int[] Daten = new int[8];
        boolean durchgangWert = Benutzer.netzwerkÖffnen(45000) == -98
            && Benutzer.datenEmpfangen(ersterOrdnungszahl, Daten, 0) == -11
            && Benutzer.datenEmpfangen(ersterOrdnungszahl, Daten, 50) == -110
            && Benutzer.datenEmpfangen(ersterOrdnungszahl, Daten, 3000) == -22
            && Benutzer.datenSenden(ersterOrdnungszahl, 0x0a000202, 9, Daten, 9) == -90
            && Benutzer.datenEmpfangen(ersterOrdnungszahl, null, 0) == -14
            && Benutzer.netzwerkSchließen(ersterOrdnungszahl) == 0 && Benutzer.netzwerkSchließen(ersterOrdnungszahl) == -9;
        Benutzer.schreiben(durchgangWert ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return durchgangWert ? 0 : 1;
    }
}
