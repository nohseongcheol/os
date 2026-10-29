// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Erste Netzwerkschicht: IPv4/UDP-Schleifenübertragung innerhalb eines Kernels. Externe IP-Adressen liefern ENETUNREACH; kein Ersatz für Ethernet/IP-Pakettreiber. Acht Endpunkte, je vier Datagramme mit jeweils 512 Byte. Alle Aufrufe sind nicht blockierend. */
public final class RückschleifeNetzwerk {
    static int[] benutzenWert = new int[8];
    static int[] portWert = new int[8];
    static int[] adresse = new int[8];
    static int[] vorderseiteWert = new int[8];
    static int[] elementeintragAnzahl = new int[8];
    static int[] empfangenWertPort = new int[8];
    static int[] Länge = new int[32];
    static int[] gesendetPort = new int[32];
    static int[] Daten = new int[32 * 512];
    static int[] vorwärtsWert = new int[512];
    static int nächsterEndpunkt = 49152;
    static int überprüfen(int Nummer) { return Nummer >= 32 && Nummer < 40 && benutzenWert[Nummer - 32] != 0 ? Nummer - 32 : -1; }
    static boolean überlappungen(int Nummer) {
        for (int platzEintrag = 0; platzEintrag < 8; platzEintrag++) if (benutzenWert[platzEintrag] != 0 && portWert[platzEintrag] == Nummer) return true;
        return false;
    }
    static int vorläufigPort() {
        for (int versuchWert = 0; versuchWert < 16; versuchWert++) {
            int kandidat = nächsterEndpunkt++;
            if (nächsterEndpunkt > 65535) nächsterEndpunkt = 49152;
            if (!überlappungen(kandidat)) return kandidat;
        }
        return -98;
    }
    public static int eintragErstellen(int gebietWert, int artWert, int vertragWert) {
        if (gebietWert != 2) return -97;
        if (artWert != 2 || (vertragWert != 0 && vertragWert != 17)) return -93;
        for (int platzEintrag = 0; platzEintrag < 8; platzEintrag++) if (benutzenWert[platzEintrag] == 0) {
            benutzenWert[platzEintrag] = 1; portWert[platzEintrag] = 0; adresse[platzEintrag] = 0; vorderseiteWert[platzEintrag] = 0; elementeintragAnzahl[platzEintrag] = 0; empfangenWertPort[platzEintrag] = 0;
            return platzEintrag + 32;
        }
        return -24;
    }
    public static int AusführbündelPacken(int Nummer, int netzwerkAdresse, int endpunktPortNummer) {
        int platzEintrag = überprüfen(Nummer);
        if (platzEintrag < 0) return -9;
        if (netzwerkAdresse != 0 && netzwerkAdresse != 0x7f000001) return -99;
        if (portWert[platzEintrag] != 0 || endpunktPortNummer < 0 || endpunktPortNummer > 65535) return -22;
        if (endpunktPortNummer == 0) endpunktPortNummer = vorläufigPort();
        if (endpunktPortNummer < 0) return endpunktPortNummer;
        if (überlappungen(endpunktPortNummer)) return -98;
        portWert[platzEintrag] = endpunktPortNummer; adresse[platzEintrag] = netzwerkAdresse; return 0;
    }
    public static int datenAblegen(int Nummer, int Wert) {
        if (Nummer < 0 || Nummer >= 512) return -22;
        vorwärtsWert[Nummer] = Wert & 255; return 0;
    }
    public static int datenLesen(int Nummer) { return Nummer >= 0 && Nummer < 512 ? vorwärtsWert[Nummer] : -22; }
    public static int senden(int Nummer, int netzwerkAdresse, int endpunktPortNummer, int größe) {
        int platzEintrag = überprüfen(Nummer);
        if (platzEintrag < 0) return -9;
        if (netzwerkAdresse != 0x7f000001) return -101;
        if (endpunktPortNummer < 1 || endpunktPortNummer > 65535) return -22;
        if (größe < 0 || größe > 512) return -90;
        if (portWert[platzEintrag] == 0) {
            int ergebnis = AusführbündelPacken(Nummer, 0x7f000001, 0);
            if (ergebnis < 0) return ergebnis;
        }
        int zielWert = -1;
        for (int kandidat = 0; kandidat < 8; kandidat++) if (benutzenWert[kandidat] != 0 && portWert[kandidat] == endpunktPortNummer) zielWert = kandidat;
        if (zielWert < 0) return -111;
        if (elementeintragAnzahl[zielWert] == 4) return -11;
        int positionIndex = zielWert * 4 + (vorderseiteWert[zielWert] + elementeintragAnzahl[zielWert]) % 4;
        for (int byteWert = 0; byteWert < größe; byteWert++) Daten[positionIndex * 512 + byteWert] = vorwärtsWert[byteWert];
        Länge[positionIndex] = größe; gesendetPort[positionIndex] = portWert[platzEintrag]; elementeintragAnzahl[zielWert]++;
        return größe;
    }
    public static int empfangen(int Nummer, int kapazitätWert) {
        int platzEintrag = überprüfen(Nummer);
        if (platzEintrag < 0) return -9;
        if (kapazitätWert < 0 || kapazitätWert > 512) return -22;
        if (elementeintragAnzahl[platzEintrag] == 0) return -11;
        int positionIndex = platzEintrag * 4 + vorderseiteWert[platzEintrag];
        int größe = Länge[positionIndex] < kapazitätWert ? Länge[positionIndex] : kapazitätWert;
        for (int byteWert = 0; byteWert < größe; byteWert++) vorwärtsWert[byteWert] = Daten[positionIndex * 512 + byteWert];
        empfangenWertPort[platzEintrag] = gesendetPort[positionIndex]; vorderseiteWert[platzEintrag] = (vorderseiteWert[platzEintrag] + 1) % 4; elementeintragAnzahl[platzEintrag]--;
        return größe;
    }
    public static int endpunktPortLesen(int Nummer) { int platzEintrag = überprüfen(Nummer); return platzEintrag < 0 ? -9 : portWert[platzEintrag]; }
    public static int adresseLesen(int Nummer) { int platzEintrag = überprüfen(Nummer); return platzEintrag < 0 ? -9 : adresse[platzEintrag]; }
    public static int absenderEndpunkt(int Nummer) { int platzEintrag = überprüfen(Nummer); return platzEintrag < 0 ? -9 : empfangenWertPort[platzEintrag]; }
    public static int schließen(int Nummer) {
        int platzEintrag = überprüfen(Nummer); if (platzEintrag < 0) return -9;
        benutzenWert[platzEintrag] = 0; elementeintragAnzahl[platzEintrag] = 0; portWert[platzEintrag] = 0; return 0;
    }
}
