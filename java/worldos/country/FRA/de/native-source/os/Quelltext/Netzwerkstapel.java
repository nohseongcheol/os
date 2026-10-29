// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Statisches IPv4/ARP/UDP. Höchstens vier Kommunikationsports mit je einem Datagramm. */
public final class Netzwerkstapel {
    static final int eigenAdresse = 0xc0a80064; /* ip.conf:IP */
    static final int netzwerkMaske = 0xffffff00; /* ip.conf:NETMASK */
    static final int netzübergangWert = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] eingabeRahmen = new int[1536], ausgabeRahmen = new int[1536];
    static int[] ports = new int[4], empfangenWertLänge = new int[4], empfangenWertAdresse = new int[4], empfangenWertPortNummer = new int[4];
    static int[] empfangenWertDaten = new int[4096], gefundenGerät = new int[6];
    static int adresseNachFinden = 0, gefundenAdresse = 0, bezeichnerWert = 0, verworfenAnzahl = 0;

    static int ganzzahl16(int[] rahmenIndex, int position) { return (rahmenIndex[position] << 8) | rahmenIndex[position + 1]; }
    static int ganzzahl32(int[] rahmenIndex, int position) { return (ganzzahl16(rahmenIndex, position) << 16) | ganzzahl16(rahmenIndex, position + 2); }
    static void ablegen16Bit(int[] rahmenIndex, int position, int Wert) { rahmenIndex[position] = (Wert >>> 8) & 255; rahmenIndex[position + 1] = Wert & 255; }
    static void ablegen32Bit(int[] rahmenIndex, int position, int Wert) { ablegen16Bit(rahmenIndex, position, Wert >>> 16); ablegen16Bit(rahmenIndex, position + 2, Wert); }
    static int summeWert(int[] rahmenIndex, int ausführenVorgang, int Länge, int Wert) {
        for (int Nummer = 0; Nummer < Länge; Nummer += 2)
            Wert += (rahmenIndex[ausführenVorgang + Nummer] << 8) | (Nummer + 1 < Länge ? rahmenIndex[ausführenVorgang + Nummer + 1] : 0);
        while ((Wert >>> 16) != 0) Wert = (Wert & 65535) + (Wert >>> 16);
        return Wert;
    }
    static int scheinKopfKontrollsumme(int abgangWert, int ankunftWert, int Länge) {
        return (abgangWert >>> 16) + (abgangWert & 65535) + (ankunftWert >>> 16) + (ankunftWert & 65535) + 17 + Länge;
    }

    static void bereinigenProzess() {
        for (int Nummer = 0; Nummer < 4; Nummer++) {
            ports[Nummer] = 0; empfangenWertLänge[Nummer] = -1; empfangenWertAdresse[Nummer] = 0; empfangenWertPortNummer[Nummer] = 0;
        }
        for (int Nummer = 0; Nummer < 64; Nummer++) if (Netzwerktreiber.empfangen(eingabeRahmen) == 0) break;
    }
    static int Nummer(int kennwertWert) { return kennwertWert >= 3 && kennwertWert < 7 && ports[kennwertWert - 3] != 0 ? kennwertWert - 3 : -1; }
    static int öffnen(int portNummer) {
        if (Netzwerktreiber.einAusgabeBasisAdresse == 0) return -19;
        if (portNummer < 0 || portNummer > 65535) return -22;
        if (portNummer != 0) for (int Nummer = 0; Nummer < 4; Nummer++) if (ports[Nummer] == portNummer) return -98;
        for (int Nummer = 0; Nummer < 4; Nummer++) if (ports[Nummer] == 0) {
            if (portNummer == 0) {
                portNummer = 49152;
                boolean überlappungen = true;
                while (überlappungen) {
                    überlappungen = false;
                    for (int vorderseiteWert = 0; vorderseiteWert < 4; vorderseiteWert++) if (ports[vorderseiteWert] == portNummer) überlappungen = true;
                    if (überlappungen) portNummer++;
                }
            }
            ports[Nummer] = portNummer; empfangenWertLänge[Nummer] = -1;
            return Nummer + 3;
        }
        return -24;
    }
    static int schließen(int kennwertWert) {
        int platzEintrag = Nummer(kennwertWert);
        if (platzEintrag < 0) return -9;
        ports[platzEintrag] = 0; empfangenWertLänge[platzEintrag] = -1;
        return 0;
    }
    static int gegenstelleAdresse(int kennwertWert) { int platzEintrag = Nummer(kennwertWert); return platzEintrag < 0 ? -9 : empfangenWertAdresse[platzEintrag]; }
    static int gegenstellePortNummer(int kennwertWert) { int platzEintrag = Nummer(kennwertWert); return platzEintrag < 0 ? -9 : empfangenWertPortNummer[platzEintrag]; }

    static void äußerlichKopf(int artWert, boolean rundrufWert) {
        for (int Nummer = 0; Nummer < 6; Nummer++) {
            ausgabeRahmen[Nummer] = rundrufWert ? 255 : gefundenGerät[Nummer];
            ausgabeRahmen[6 + Nummer] = Netzwerktreiber.gerätAdresse[Nummer];
        }
        ablegen16Bit(ausgabeRahmen, 12, artWert);
    }
    static void anfrageAdresse(int zielWert) {
        äußerlichKopf(0x0806, true);
        ablegen16Bit(ausgabeRahmen, 14, 1); ablegen16Bit(ausgabeRahmen, 16, 0x0800);
        ausgabeRahmen[18] = 6; ausgabeRahmen[19] = 4; ablegen16Bit(ausgabeRahmen, 20, 1);
        for (int Nummer = 0; Nummer < 6; Nummer++) {
            ausgabeRahmen[22 + Nummer] = Netzwerktreiber.gerätAdresse[Nummer]; ausgabeRahmen[32 + Nummer] = 0;
        }
        ablegen32Bit(ausgabeRahmen, 28, eigenAdresse); ablegen32Bit(ausgabeRahmen, 38, zielWert);
        Netzwerktreiber.senden(ausgabeRahmen, 42);
    }
    static void prozessAdresse(int Länge) {
        if (Länge < 42 || ganzzahl16(eingabeRahmen, 14) != 1 || ganzzahl16(eingabeRahmen, 16) != 0x0800
            || eingabeRahmen[18] != 6 || eingabeRahmen[19] != 4 || ganzzahl32(eingabeRahmen, 38) != eigenAdresse) { verworfenAnzahl++; return; }
        int artWert = ganzzahl16(eingabeRahmen, 20), gegenstelleWert = ganzzahl32(eingabeRahmen, 28);
        if (artWert == 2 && gegenstelleWert == adresseNachFinden) {
            for (int Nummer = 0; Nummer < 6; Nummer++) {
                if (eingabeRahmen[6 + Nummer] != eingabeRahmen[22 + Nummer] || eingabeRahmen[32 + Nummer] != Netzwerktreiber.gerätAdresse[Nummer]) return;
            }
            for (int Nummer = 0; Nummer < 6; Nummer++) gefundenGerät[Nummer] = eingabeRahmen[22 + Nummer];
            gefundenAdresse = gegenstelleWert;
        } else if (artWert == 1) {
            äußerlichKopf(0x0806, false);
            ablegen16Bit(ausgabeRahmen, 14, 1); ablegen16Bit(ausgabeRahmen, 16, 0x0800);
            ausgabeRahmen[18] = 6; ausgabeRahmen[19] = 4; ablegen16Bit(ausgabeRahmen, 20, 2);
            for (int Nummer = 0; Nummer < 6; Nummer++) {
                ausgabeRahmen[Nummer] = eingabeRahmen[22 + Nummer]; ausgabeRahmen[32 + Nummer] = eingabeRahmen[22 + Nummer];
                ausgabeRahmen[22 + Nummer] = Netzwerktreiber.gerätAdresse[Nummer];
            }
            ablegen32Bit(ausgabeRahmen, 28, eigenAdresse); ablegen32Bit(ausgabeRahmen, 38, gegenstelleWert);
            Netzwerktreiber.senden(ausgabeRahmen, 42);
        }
    }

    static void prozessRahmen(int Länge) {
        if (Länge < 14 || Länge > eingabeRahmen.length) { verworfenAnzahl++; return; }
        boolean selbstVerweis = true, rundrufWert = true;
        for (int Nummer = 0; Nummer < 6; Nummer++) {
            if (eingabeRahmen[Nummer] != Netzwerktreiber.gerätAdresse[Nummer]) selbstVerweis = false;
            if (eingabeRahmen[Nummer] != 255) rundrufWert = false;
        }
        if (!selbstVerweis && !rundrufWert) return;
        if (ganzzahl16(eingabeRahmen, 12) == 0x0806) { prozessAdresse(Länge); return; }
        if (ganzzahl16(eingabeRahmen, 12) != 0x0800) return;
        if (Länge < 34 || (eingabeRahmen[14] >>> 4) != 4) { verworfenAnzahl++; return; }
        int kopfLänge = (eingabeRahmen[14] & 15) * 4, gesamtwertLänge = ganzzahl16(eingabeRahmen, 16);
        if (kopfLänge < 20 || kopfLänge > 60 || gesamtwertLänge < kopfLänge + 8 || gesamtwertLänge > Länge - 14
            || (ganzzahl16(eingabeRahmen, 20) & 0x3fff) != 0 || eingabeRahmen[23] != 17
            || ganzzahl32(eingabeRahmen, 30) != eigenAdresse || summeWert(eingabeRahmen, 14, kopfLänge, 0) != 65535) { verworfenAnzahl++; return; }
        int ausführenVorgang = 14 + kopfLänge, datenLänge = ganzzahl16(eingabeRahmen, ausführenVorgang + 4);
        if (datenLänge < 8 || datenLänge != gesamtwertLänge - kopfLänge || datenLänge > 1032) { verworfenAnzahl++; return; }
        int abgangWert = ganzzahl32(eingabeRahmen, 26);
        if (ganzzahl16(eingabeRahmen, ausführenVorgang + 6) != 0 && summeWert(eingabeRahmen, ausführenVorgang, datenLänge, scheinKopfKontrollsumme(abgangWert, eigenAdresse, datenLänge)) != 65535) {
            verworfenAnzahl++; return;
        }
        int zielWert = ganzzahl16(eingabeRahmen, ausführenVorgang + 2);
        for (int platzEintrag = 0; platzEintrag < 4; platzEintrag++) if (ports[platzEintrag] != 0 && ports[platzEintrag] == zielWert) {
            if (empfangenWertLänge[platzEintrag] >= 0) { verworfenAnzahl++; return; }
            empfangenWertLänge[platzEintrag] = datenLänge - 8; empfangenWertAdresse[platzEintrag] = abgangWert; empfangenWertPortNummer[platzEintrag] = ganzzahl16(eingabeRahmen, ausführenVorgang);
            for (int Nummer = 0; Nummer < datenLänge - 8; Nummer++) empfangenWertDaten[platzEintrag * 1024 + Nummer] = eingabeRahmen[ausführenVorgang + 8 + Nummer];
            return;
        }
    }

    static void überprüfen() {
        for (int Nummer = 0; Nummer < 16; Nummer++) {
            int Länge = Netzwerktreiber.empfangen(eingabeRahmen);
            if (Länge == 0) return;
            prozessRahmen(Länge);
        }
    }
    static int adresseFinden(int adresse) {
        if (adresse == 0 || adresse == -1 || (adresse >>> 28) >= 14 || (adresse >>> 24) == 127 || adresse == eigenAdresse) return -101;
        int nächsterElementeintrag = (adresse & netzwerkMaske) == (eigenAdresse & netzwerkMaske) ? adresse : netzübergangWert;
        if (nächsterElementeintrag == gefundenAdresse) return 0;
        adresseNachFinden = nächsterElementeintrag;
        int ausführenVorgang = Gerät.millisekunden(), nächsterAnfrage = ausführenVorgang;
        while (Gerät.millisekunden() - ausführenVorgang < 1000) {
            if (Gerät.millisekunden() - nächsterAnfrage >= 0) { anfrageAdresse(nächsterElementeintrag); nächsterAnfrage += 300; }
            überprüfen();
            if (gefundenAdresse == nächsterElementeintrag) return 0;
            Gerät.kurzzeitigTunAbgeben();
        }
        return -110;
    }
    static int senden(int kennwertWert, int adresse, int portNummer, int[] Daten, int Länge) {
        int platzEintrag = Nummer(kennwertWert);
        if (platzEintrag < 0) return -9;
        if (Netzwerktreiber.einAusgabeBasisAdresse == 0) return -19;
        if (portNummer < 1 || portNummer > 65535 || Länge < 0 || Länge > 1024) return -22;
        int ergebnis = adresseFinden(adresse);
        if (ergebnis < 0) return ergebnis;
        äußerlichKopf(0x0800, false);
        ausgabeRahmen[14] = 0x45; ausgabeRahmen[15] = 0; ablegen16Bit(ausgabeRahmen, 16, 28 + Länge);
        ablegen16Bit(ausgabeRahmen, 18, bezeichnerWert++); ablegen16Bit(ausgabeRahmen, 20, 0x4000);
        ausgabeRahmen[22] = 64; ausgabeRahmen[23] = 17; ablegen16Bit(ausgabeRahmen, 24, 0);
        ablegen32Bit(ausgabeRahmen, 26, eigenAdresse); ablegen32Bit(ausgabeRahmen, 30, adresse);
        ablegen16Bit(ausgabeRahmen, 24, ~summeWert(ausgabeRahmen, 14, 20, 0));
        ablegen16Bit(ausgabeRahmen, 34, ports[platzEintrag]); ablegen16Bit(ausgabeRahmen, 36, portNummer);
        ablegen16Bit(ausgabeRahmen, 38, Länge + 8); ablegen16Bit(ausgabeRahmen, 40, 0);
        for (int Nummer = 0; Nummer < Länge; Nummer++) ausgabeRahmen[42 + Nummer] = Daten[Nummer] & 255;
        int kontrollsumme = (~summeWert(ausgabeRahmen, 34, Länge + 8, scheinKopfKontrollsumme(eigenAdresse, adresse, Länge + 8))) & 65535;
        ablegen16Bit(ausgabeRahmen, 40, kontrollsumme == 0 ? 65535 : kontrollsumme);
        ergebnis = Netzwerktreiber.senden(ausgabeRahmen, Länge + 42);
        return ergebnis < 0 ? ergebnis : Länge;
    }
    static int empfangen(int kennwertWert, int[] Daten, int kapazitätWert, int grenzwertWert) {
        int platzEintrag = Nummer(kennwertWert);
        if (platzEintrag < 0) return -9;
        int ausführenVorgang = Gerät.millisekunden();
        while (true) {
            überprüfen();
            int Länge = empfangenWertLänge[platzEintrag];
            if (Länge >= 0) {
                empfangenWertLänge[platzEintrag] = -1;
                if (Länge > kapazitätWert) return -90;
                for (int Nummer = 0; Nummer < Länge; Nummer++) Daten[Nummer] = empfangenWertDaten[platzEintrag * 1024 + Nummer];
                return Länge;
            }
            if (grenzwertWert == 0) return -11;
            if (Gerät.millisekunden() - ausführenVorgang >= grenzwertWert) return -110;
            Gerät.kurzzeitigTunAbgeben();
        }
    }
    static void statuswertWert() {
        Zeichenterminal.schreiben(Netzwerktreiber.einAusgabeBasisAdresse == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        Zeichenterminal.schreiben("TX: "); Zeichenterminal.nummerSchreiben(Netzwerktreiber.übertragenAnzahl);
        Zeichenterminal.schreiben(" RX: "); Zeichenterminal.nummerSchreiben(Netzwerktreiber.anzahlEmpfangen);
        Zeichenterminal.schreiben(" DROP: "); Zeichenterminal.nummerSchreiben(verworfenAnzahl);
        Zeichenterminal.schreiben("\n");
    }
}
