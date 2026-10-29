// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), ein Sendepuffer und ein 8-KiB-Empfangsring. Verwendet Abfragen statt Interrupts. */
public final class Netzwerktreiber {
    static int einAusgabeBasisAdresse = 0;
    static int positionEmpfangen = 0, übertragenPlatz = 0;
    static int[] gerätAdresse = new int[6];
    static int übertragenAnzahl = 0, anzahlEmpfangen = 0, fehlerAnzahl = 0;

    static int einstellungenLesen(int gerätNummer, int position) {
        Gerät.einAusgabeGanzzahlSchreiben(0xcf8, 0x80000000 | (gerätNummer << 11) | position);
        return Gerät.einAusgabeGanzzahlLesen(0xcfc);
    }

    static boolean vorbereiten() {
        int gerätNummer = -1;
        for (int Nummer = 0; Nummer < 32; Nummer++) {
            if (einstellungenLesen(Nummer, 0) == 0x813910ec) { gerätNummer = Nummer; break; }
        }
        if (gerätNummer < 0) return false;
        int standardwertWert = einstellungenLesen(gerätNummer, 0x10);
        if ((standardwertWert & 1) == 0 || (standardwertWert & 0xfffffffc) < 0x100 || (standardwertWert & 0xfffffffc) > 65535) return false;
        einAusgabeBasisAdresse = standardwertWert & 0xfffc;
        int befehl = einstellungenLesen(gerätNummer, 4);
        Gerät.einAusgabeGanzzahlSchreiben(0xcf8, 0x80000004 | (gerätNummer << 11));
        Gerät.einAusgabeKurzSchreiben(0xcfc, befehl | 5); // I/O und Busmaster aktivieren; PCI-Statusbits unverändert lassen.
        Gerät.einAusgabeByteSchreiben(einAusgabeBasisAdresse + 0x52, 0);
        if (!wertZurücksetzen()) { einAusgabeBasisAdresse = 0; return false; }
        for (int Nummer = 0; Nummer < 6; Nummer++) gerätAdresse[Nummer] = Gerät.einAusgabeByteLesen(einAusgabeBasisAdresse + Nummer);
        return true;
    }

    static boolean wertZurücksetzen() {
        Gerät.einAusgabeByteSchreiben(einAusgabeBasisAdresse + 0x37, 0x10);
        int ausführenVorgang = Gerät.millisekunden();
        while ((Gerät.einAusgabeByteLesen(einAusgabeBasisAdresse + 0x37) & 0x10) != 0)
            if (Gerät.millisekunden() - ausführenVorgang > 100) return false;
        positionEmpfangen = 0; übertragenPlatz = 0;
        Gerät.einAusgabeGanzzahlSchreiben(einAusgabeBasisAdresse + 0x30, Gerät.netzwerkSpeicher());
        for (int Nummer = 0; Nummer < 4; Nummer++) Gerät.einAusgabeGanzzahlSchreiben(einAusgabeBasisAdresse + 0x20 + Nummer * 4, Gerät.netzwerkSpeicher() + 12288);
        Gerät.einAusgabeKurzSchreiben(einAusgabeBasisAdresse + 0x3c, 0);
        Gerät.einAusgabeKurzSchreiben(einAusgabeBasisAdresse + 0x3e, 0xffff);
        Gerät.einAusgabeByteSchreiben(einAusgabeBasisAdresse + 0x37, 0x0c);
        Gerät.einAusgabeGanzzahlSchreiben(einAusgabeBasisAdresse + 0x44, 0x0000e78a); // Eigene Adresse und Rundsendungen annehmen; zusammenhängende Ablage beim Umlauf, 8 KiB.
        Gerät.einAusgabeGanzzahlSchreiben(einAusgabeBasisAdresse + 0x40, 0x03000600);
        return true;
    }

    static int senden(int[] Daten, int Länge) {
        if (einAusgabeBasisAdresse == 0) return -19;
        if (Länge < 14 || Länge > 1514) return -90;
        int zustandPort = einAusgabeBasisAdresse + 0x10 + übertragenPlatz * 4;
        int ausführenVorgang = Gerät.millisekunden();
        while ((Gerät.einAusgabeGanzzahlLesen(zustandPort) & 0x2000) == 0)
            if (Gerät.millisekunden() - ausführenVorgang > 100) return -110;
        int größe = Länge < 60 ? 60 : Länge;
        for (int Nummer = 0; Nummer < größe; Nummer++)
            Gerät.speicherSchreiben(Gerät.netzwerkSpeicher() + 12288 + Nummer, Nummer < Länge ? Daten[Nummer] : 0);
        Gerät.einAusgabeGanzzahlSchreiben(zustandPort, größe | 0x00080000);
        ausführenVorgang = Gerät.millisekunden();
        while ((Gerät.einAusgabeGanzzahlLesen(zustandPort) & 0xe0008000) == 0)
            if (Gerät.millisekunden() - ausführenVorgang > 100) return -110;
        if ((Gerät.einAusgabeGanzzahlLesen(zustandPort) & 0x8000) == 0) { fehlerAnzahl++; return -5; }
        übertragenPlatz = (übertragenPlatz + 1) & 3;
        übertragenAnzahl++;
        return Länge;
    }

    static int empfangen(int[] Daten) {
        if (einAusgabeBasisAdresse == 0) return 0;
        if ((Gerät.einAusgabeByteLesen(einAusgabeBasisAdresse + 0x3e) & 0x50) != 0) {
            fehlerAnzahl++;
            if (!wertZurücksetzen()) einAusgabeBasisAdresse = 0;
            return 0;
        }
        if ((Gerät.einAusgabeByteLesen(einAusgabeBasisAdresse + 0x37) & 1) != 0) return 0;
        int kopfWert = Gerät.netzwerkSpeicher() + positionEmpfangen;
        int statuswertWert = Ausführungsverwaltung.kurzWert(kopfWert), größe = Ausführungsverwaltung.kurzWert(kopfWert + 2);
        if (größe == 0xfff0) return 0; // DMA läuft.
        if (größe < 4 || größe > 1518) {
            fehlerAnzahl++;
            if (!wertZurücksetzen()) einAusgabeBasisAdresse = 0;
            return 0;
        }
        int Länge = größe - 4;
        if ((statuswertWert & 1) != 0) {
            for (int Nummer = 0; Nummer < Länge; Nummer++) Daten[Nummer] = Gerät.speicherLesen(kopfWert + 4 + Nummer);
            anzahlEmpfangen++;
        } else { Länge = 0; fehlerAnzahl++; }
        positionEmpfangen = (positionEmpfangen + größe + 4 + 3) & ~3;
        positionEmpfangen &= 8191;
        Gerät.einAusgabeKurzSchreiben(einAusgabeBasisAdresse + 0x38, (positionEmpfangen - 16) & 65535);
        Gerät.einAusgabeKurzSchreiben(einAusgabeBasisAdresse + 0x3e, 0x000f);
        return Länge;
    }
}
