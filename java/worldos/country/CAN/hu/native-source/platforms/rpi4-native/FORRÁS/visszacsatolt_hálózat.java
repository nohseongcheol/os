// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 réteg_ÉRTÉK: 단일 kernel_ÉRTÉK 안의 IPv4/UDP 루프백 átvisz_ÉRTÉK.
 * külső_ÉRTÉK IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * megszüntet_pont 8개, 끝점당 datagram 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class visszacsatolt_hálózat {
    static int[] használ_ÉRTÉK = new int[8];
    static int[] port_ÉRTÉK = new int[8];
    static int[] CÍM = new int[8];
    static int[] elülső_kamera_ÉRTÉK = new int[8];
    static int[] cikk_DARAB = new int[8];
    static int[] KAPOTT_port = new int[8];
    static int[] hossz_ÉRTÉK = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] adat = new int[32 * 512];
    static int[] Előre_ÉRTÉK = new int[512];
    static int Tovább_végpont = 49152;
    static int igazol(int INDEX) { return INDEX >= 32 && INDEX < 40 && használ_ÉRTÉK[INDEX - 32] != 0 ? INDEX - 32 : -1; }
    static boolean 겹침(int INDEX) {
        for (int tárolóhely_bejegyzés = 0; tárolóhely_bejegyzés < 8; tárolóhely_bejegyzés++) if (használ_ÉRTÉK[tárolóhely_bejegyzés] != 0 && port_ÉRTÉK[tárolóhely_bejegyzés] == INDEX) return true;
        return false;
    }
    static int 임시창구() {
        for (int 시도 = 0; 시도 < 16; 시도++) {
            int 후보 = Tovább_végpont++;
            if (Tovább_végpont > 65535) Tovább_végpont = 49152;
            if (!겹침(후보)) return 후보;
        }
        return -98;
    }
    public static int készít_bejegyzés(int régió_ÉRTÉK, int Altípus_ÉRTÉK, int szerződés_értéke) {
        if (régió_ÉRTÉK != 2) return -97;
        if (Altípus_ÉRTÉK != 2 || (szerződés_értéke != 0 && szerződés_értéke != 17)) return -93;
        for (int tárolóhely_bejegyzés = 0; tárolóhely_bejegyzés < 8; tárolóhely_bejegyzés++) if (használ_ÉRTÉK[tárolóhely_bejegyzés] == 0) {
            használ_ÉRTÉK[tárolóhely_bejegyzés] = 1; port_ÉRTÉK[tárolóhely_bejegyzés] = 0; CÍM[tárolóhely_bejegyzés] = 0; elülső_kamera_ÉRTÉK[tárolóhely_bejegyzés] = 0; cikk_DARAB[tárolóhely_bejegyzés] = 0; KAPOTT_port[tárolóhely_bejegyzés] = 0;
            return tárolóhely_bejegyzés + 32;
        }
        return -24;
    }
    public static int BIND_végpont(int INDEX, int hálózati_azonosító, int végpont_portszám) {
        int tárolóhely_bejegyzés = igazol(INDEX);
        if (tárolóhely_bejegyzés < 0) return -9;
        if (hálózati_azonosító != 0 && hálózati_azonosító != 0x7f000001) return -99;
        if (port_ÉRTÉK[tárolóhely_bejegyzés] != 0 || végpont_portszám < 0 || végpont_portszám > 65535) return -22;
        if (végpont_portszám == 0) végpont_portszám = 임시창구();
        if (végpont_portszám < 0) return végpont_portszám;
        if (겹침(végpont_portszám)) return -98;
        port_ÉRTÉK[tárolóhely_bejegyzés] = végpont_portszám; CÍM[tárolóhely_bejegyzés] = hálózati_azonosító; return 0;
    }
    public static int 자료넣기(int INDEX, int ÉRTÉK) {
        if (INDEX < 0 || INDEX >= 512) return -22;
        Előre_ÉRTÉK[INDEX] = ÉRTÉK & 255; return 0;
    }
    public static int 자료읽기(int INDEX) { return INDEX >= 0 && INDEX < 512 ? Előre_ÉRTÉK[INDEX] : -22; }
    public static int küld(int INDEX, int hálózati_azonosító, int végpont_portszám, int Méret) {
        int tárolóhely_bejegyzés = igazol(INDEX);
        if (tárolóhely_bejegyzés < 0) return -9;
        if (hálózati_azonosító != 0x7f000001) return -101;
        if (végpont_portszám < 1 || végpont_portszám > 65535) return -22;
        if (Méret < 0 || Méret > 512) return -90;
        if (port_ÉRTÉK[tárolóhely_bejegyzés] == 0) {
            int KR = BIND_végpont(INDEX, 0x7f000001, 0);
            if (KR < 0) return KR;
        }
        int cél_ÉRTÉK = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (használ_ÉRTÉK[후보] != 0 && port_ÉRTÉK[후보] == végpont_portszám) cél_ÉRTÉK = 후보;
        if (cél_ÉRTÉK < 0) return -111;
        if (cikk_DARAB[cél_ÉRTÉK] == 4) return -11;
        int helyzetindex = cél_ÉRTÉK * 4 + (elülső_kamera_ÉRTÉK[cél_ÉRTÉK] + cikk_DARAB[cél_ÉRTÉK]) % 4;
        for (int bájt_ÉRTÉK = 0; bájt_ÉRTÉK < Méret; bájt_ÉRTÉK++) adat[helyzetindex * 512 + bájt_ÉRTÉK] = Előre_ÉRTÉK[bájt_ÉRTÉK];
        hossz_ÉRTÉK[helyzetindex] = Méret; 보낸창구[helyzetindex] = port_ÉRTÉK[tárolóhely_bejegyzés]; cikk_DARAB[cél_ÉRTÉK]++;
        return Méret;
    }
    public static int fogad(int INDEX, int kapacitás_ÉRTÉK) {
        int tárolóhely_bejegyzés = igazol(INDEX);
        if (tárolóhely_bejegyzés < 0) return -9;
        if (kapacitás_ÉRTÉK < 0 || kapacitás_ÉRTÉK > 512) return -22;
        if (cikk_DARAB[tárolóhely_bejegyzés] == 0) return -11;
        int helyzetindex = tárolóhely_bejegyzés * 4 + elülső_kamera_ÉRTÉK[tárolóhely_bejegyzés];
        int Méret = hossz_ÉRTÉK[helyzetindex] < kapacitás_ÉRTÉK ? hossz_ÉRTÉK[helyzetindex] : kapacitás_ÉRTÉK;
        for (int bájt_ÉRTÉK = 0; bájt_ÉRTÉK < Méret; bájt_ÉRTÉK++) Előre_ÉRTÉK[bájt_ÉRTÉK] = adat[helyzetindex * 512 + bájt_ÉRTÉK];
        KAPOTT_port[tárolóhely_bejegyzés] = 보낸창구[helyzetindex]; elülső_kamera_ÉRTÉK[tárolóhely_bejegyzés] = (elülső_kamera_ÉRTÉK[tárolóhely_bejegyzés] + 1) % 4; cikk_DARAB[tárolóhely_bejegyzés]--;
        return Méret;
    }
    public static int 창구읽기(int INDEX) { int tárolóhely_bejegyzés = igazol(INDEX); return tárolóhely_bejegyzés < 0 ? -9 : port_ÉRTÉK[tárolóhely_bejegyzés]; }
    public static int 주소읽기(int INDEX) { int tárolóhely_bejegyzés = igazol(INDEX); return tárolóhely_bejegyzés < 0 ? -9 : CÍM[tárolóhely_bejegyzés]; }
    public static int feladó_végpont(int INDEX) { int tárolóhely_bejegyzés = igazol(INDEX); return tárolóhely_bejegyzés < 0 ? -9 : KAPOTT_port[tárolóhely_bejegyzés]; }
    public static int Bezárás(int INDEX) {
        int tárolóhely_bejegyzés = igazol(INDEX); if (tárolóhely_bejegyzés < 0) return -9;
        használ_ÉRTÉK[tárolóhely_bejegyzés] = 0; cikk_DARAB[tárolóhely_bejegyzés] = 0; port_ÉRTÉK[tárolóhely_bejegyzés] = 0; return 0;
    }
}
