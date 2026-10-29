// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 lag_VÆRDI: 단일 kerne_VÆRDI 안의 IPv4/UDP 루프백 overføre_VÆRDI.
 * ekstern_VÆRDI IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * afslutte_et_opkald_pege 8개, 끝점당 datagram 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class tilbagekobling_netværk {
    static int[] brug_VÆRDI = new int[8];
    static int[] port_VÆRDI = new int[8];
    static int[] mail = new int[8];
    static int[] frontvendt_VÆRDI = new int[8];
    static int[] vare_TÆL = new int[8];
    static int[] MODTAGET_VED_UDLØB_port = new int[8];
    static int[] varighed_VÆRDI = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] data = new int[32 * 512];
    static int[] Frem_VÆRDI = new int[512];
    static int Næste_slutpunkt = 49152;
    static int bekræfte(int INDEKS) { return INDEKS >= 32 && INDEKS < 40 && brug_VÆRDI[INDEKS - 32] != 0 ? INDEKS - 32 : -1; }
    static boolean 겹침(int INDEKS) {
        for (int udvidelsesstik_post = 0; udvidelsesstik_post < 8; udvidelsesstik_post++) if (brug_VÆRDI[udvidelsesstik_post] != 0 && port_VÆRDI[udvidelsesstik_post] == INDEKS) return true;
        return false;
    }
    static int 임시창구() {
        for (int 시도 = 0; 시도 < 16; 시도++) {
            int 후보 = Næste_slutpunkt++;
            if (Næste_slutpunkt > 65535) Næste_slutpunkt = 49152;
            if (!겹침(후보)) return 후보;
        }
        return -98;
    }
    public static int åbne_post_81b8d99b(int område_VÆRDI_0e9a97ab, int 종류, int kontraktværdi) {
        if (område_VÆRDI_0e9a97ab != 2) return -97;
        if (종류 != 2 || (kontraktværdi != 0 && kontraktværdi != 17)) return -93;
        for (int udvidelsesstik_post = 0; udvidelsesstik_post < 8; udvidelsesstik_post++) if (brug_VÆRDI[udvidelsesstik_post] == 0) {
            brug_VÆRDI[udvidelsesstik_post] = 1; port_VÆRDI[udvidelsesstik_post] = 0; mail[udvidelsesstik_post] = 0; frontvendt_VÆRDI[udvidelsesstik_post] = 0; vare_TÆL[udvidelsesstik_post] = 0; MODTAGET_VED_UDLØB_port[udvidelsesstik_post] = 0;
            return udvidelsesstik_post + 32;
        }
        return -24;
    }
    public static int BIND_slutpunkt(int INDEKS, int netværks_id, int slutpunkt_portnummer) {
        int udvidelsesstik_post = bekræfte(INDEKS);
        if (udvidelsesstik_post < 0) return -9;
        if (netværks_id != 0 && netværks_id != 0x7f000001) return -99;
        if (port_VÆRDI[udvidelsesstik_post] != 0 || slutpunkt_portnummer < 0 || slutpunkt_portnummer > 65535) return -22;
        if (slutpunkt_portnummer == 0) slutpunkt_portnummer = 임시창구();
        if (slutpunkt_portnummer < 0) return slutpunkt_portnummer;
        if (겹침(slutpunkt_portnummer)) return -98;
        port_VÆRDI[udvidelsesstik_post] = slutpunkt_portnummer; mail[udvidelsesstik_post] = netværks_id; return 0;
    }
    public static int 자료넣기(int INDEKS, int VÆRDI) {
        if (INDEKS < 0 || INDEKS >= 512) return -22;
        Frem_VÆRDI[INDEKS] = VÆRDI & 255; return 0;
    }
    public static int 자료읽기(int INDEKS) { return INDEKS >= 0 && INDEKS < 512 ? Frem_VÆRDI[INDEKS] : -22; }
    public static int maile(int INDEKS, int netværks_id, int slutpunkt_portnummer, int Størrelse) {
        int udvidelsesstik_post = bekræfte(INDEKS);
        if (udvidelsesstik_post < 0) return -9;
        if (netværks_id != 0x7f000001) return -101;
        if (slutpunkt_portnummer < 1 || slutpunkt_portnummer > 65535) return -22;
        if (Størrelse < 0 || Størrelse > 512) return -90;
        if (port_VÆRDI[udvidelsesstik_post] == 0) {
            int KR = BIND_slutpunkt(INDEKS, 0x7f000001, 0);
            if (KR < 0) return KR;
        }
        int destination_VÆRDI = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (brug_VÆRDI[후보] != 0 && port_VÆRDI[후보] == slutpunkt_portnummer) destination_VÆRDI = 후보;
        if (destination_VÆRDI < 0) return -111;
        if (vare_TÆL[destination_VÆRDI] == 4) return -11;
        int positionsindeks = destination_VÆRDI * 4 + (frontvendt_VÆRDI[destination_VÆRDI] + vare_TÆL[destination_VÆRDI]) % 4;
        for (int byte_VÆRDI = 0; byte_VÆRDI < Størrelse; byte_VÆRDI++) data[positionsindeks * 512 + byte_VÆRDI] = Frem_VÆRDI[byte_VÆRDI];
        varighed_VÆRDI[positionsindeks] = Størrelse; 보낸창구[positionsindeks] = port_VÆRDI[udvidelsesstik_post]; vare_TÆL[destination_VÆRDI]++;
        return Størrelse;
    }
    public static int modtage(int INDEKS, int kapacitet_VÆRDI) {
        int udvidelsesstik_post = bekræfte(INDEKS);
        if (udvidelsesstik_post < 0) return -9;
        if (kapacitet_VÆRDI < 0 || kapacitet_VÆRDI > 512) return -22;
        if (vare_TÆL[udvidelsesstik_post] == 0) return -11;
        int positionsindeks = udvidelsesstik_post * 4 + frontvendt_VÆRDI[udvidelsesstik_post];
        int Størrelse = varighed_VÆRDI[positionsindeks] < kapacitet_VÆRDI ? varighed_VÆRDI[positionsindeks] : kapacitet_VÆRDI;
        for (int byte_VÆRDI = 0; byte_VÆRDI < Størrelse; byte_VÆRDI++) Frem_VÆRDI[byte_VÆRDI] = data[positionsindeks * 512 + byte_VÆRDI];
        MODTAGET_VED_UDLØB_port[udvidelsesstik_post] = 보낸창구[positionsindeks]; frontvendt_VÆRDI[udvidelsesstik_post] = (frontvendt_VÆRDI[udvidelsesstik_post] + 1) % 4; vare_TÆL[udvidelsesstik_post]--;
        return Størrelse;
    }
    public static int 창구읽기(int INDEKS) { int udvidelsesstik_post = bekræfte(INDEKS); return udvidelsesstik_post < 0 ? -9 : port_VÆRDI[udvidelsesstik_post]; }
    public static int 주소읽기(int INDEKS) { int udvidelsesstik_post = bekræfte(INDEKS); return udvidelsesstik_post < 0 ? -9 : mail[udvidelsesstik_post]; }
    public static int afsender_slutpunkt(int INDEKS) { int udvidelsesstik_post = bekræfte(INDEKS); return udvidelsesstik_post < 0 ? -9 : MODTAGET_VED_UDLØB_port[udvidelsesstik_post]; }
    public static int Luk(int INDEKS) {
        int udvidelsesstik_post = bekræfte(INDEKS); if (udvidelsesstik_post < 0) return -9;
        brug_VÆRDI[udvidelsesstik_post] = 0; vare_TÆL[udvidelsesstik_post] = 0; port_VÆRDI[udvidelsesstik_post] = 0; return 0;
    }
}
