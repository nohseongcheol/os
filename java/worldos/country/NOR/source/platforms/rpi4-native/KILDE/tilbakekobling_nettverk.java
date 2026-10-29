// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 lag_VERDI: 단일 kjerne_VERDI 안의 IPv4/UDP 루프백 overføre_VERDI.
 * ekstern_VERDI IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * avslutte_en_samtale_peke 8개, 끝점당 datagram 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class tilbakekobling_nettverk {
    static int[] bruk_VERDI = new int[8];
    static int[] port_VERDI = new int[8];
    static int[] e_post = new int[8];
    static int[] frontkamera_VERDI = new int[8];
    static int[] vare_ANTALL = new int[8];
    static int[] MOTTATT_AVKAST_port = new int[8];
    static int[] lengde_VERDI = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] data = new int[32 * 512];
    static int[] Frem_VERDI = new int[512];
    static int Neste_deltaker = 49152;
    static int bekrefte(int INDEKS) { return INDEKS >= 32 && INDEKS < 40 && bruk_VERDI[INDEKS - 32] != 0 ? INDEKS - 32 : -1; }
    static boolean 겹침(int INDEKS) {
        for (int åpning_oppføring = 0; åpning_oppføring < 8; åpning_oppføring++) if (bruk_VERDI[åpning_oppføring] != 0 && port_VERDI[åpning_oppføring] == INDEKS) return true;
        return false;
    }
    static int 임시창구() {
        for (int 시도 = 0; 시도 < 16; 시도++) {
            int 후보 = Neste_deltaker++;
            if (Neste_deltaker > 65535) Neste_deltaker = 49152;
            if (!겹침(후보)) return 후보;
        }
        return -98;
    }
    public static int åpne_oppføring(int område_VERDI_0e9a97ab, int 종류, int kontraktverdi) {
        if (område_VERDI_0e9a97ab != 2) return -97;
        if (종류 != 2 || (kontraktverdi != 0 && kontraktverdi != 17)) return -93;
        for (int åpning_oppføring = 0; åpning_oppføring < 8; åpning_oppføring++) if (bruk_VERDI[åpning_oppføring] == 0) {
            bruk_VERDI[åpning_oppføring] = 1; port_VERDI[åpning_oppføring] = 0; e_post[åpning_oppføring] = 0; frontkamera_VERDI[åpning_oppføring] = 0; vare_ANTALL[åpning_oppføring] = 0; MOTTATT_AVKAST_port[åpning_oppføring] = 0;
            return åpning_oppføring + 32;
        }
        return -24;
    }
    public static int BIND_deltaker(int INDEKS, int nettverks_ID, int deltaker_portnummer) {
        int åpning_oppføring = bekrefte(INDEKS);
        if (åpning_oppføring < 0) return -9;
        if (nettverks_ID != 0 && nettverks_ID != 0x7f000001) return -99;
        if (port_VERDI[åpning_oppføring] != 0 || deltaker_portnummer < 0 || deltaker_portnummer > 65535) return -22;
        if (deltaker_portnummer == 0) deltaker_portnummer = 임시창구();
        if (deltaker_portnummer < 0) return deltaker_portnummer;
        if (겹침(deltaker_portnummer)) return -98;
        port_VERDI[åpning_oppføring] = deltaker_portnummer; e_post[åpning_oppføring] = nettverks_ID; return 0;
    }
    public static int 자료넣기(int INDEKS, int VERDI) {
        if (INDEKS < 0 || INDEKS >= 512) return -22;
        Frem_VERDI[INDEKS] = VERDI & 255; return 0;
    }
    public static int 자료읽기(int INDEKS) { return INDEKS >= 0 && INDEKS < 512 ? Frem_VERDI[INDEKS] : -22; }
    public static int sende(int INDEKS, int nettverks_ID, int deltaker_portnummer, int Størrelse) {
        int åpning_oppføring = bekrefte(INDEKS);
        if (åpning_oppføring < 0) return -9;
        if (nettverks_ID != 0x7f000001) return -101;
        if (deltaker_portnummer < 1 || deltaker_portnummer > 65535) return -22;
        if (Størrelse < 0 || Størrelse > 512) return -90;
        if (port_VERDI[åpning_oppføring] == 0) {
            int KR = BIND_deltaker(INDEKS, 0x7f000001, 0);
            if (KR < 0) return KR;
        }
        int mål_VERDI = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (bruk_VERDI[후보] != 0 && port_VERDI[후보] == deltaker_portnummer) mål_VERDI = 후보;
        if (mål_VERDI < 0) return -111;
        if (vare_ANTALL[mål_VERDI] == 4) return -11;
        int posisjonsindeks = mål_VERDI * 4 + (frontkamera_VERDI[mål_VERDI] + vare_ANTALL[mål_VERDI]) % 4;
        for (int byte_VERDI = 0; byte_VERDI < Størrelse; byte_VERDI++) data[posisjonsindeks * 512 + byte_VERDI] = Frem_VERDI[byte_VERDI];
        lengde_VERDI[posisjonsindeks] = Størrelse; 보낸창구[posisjonsindeks] = port_VERDI[åpning_oppføring]; vare_ANTALL[mål_VERDI]++;
        return Størrelse;
    }
    public static int motta(int INDEKS, int kapasitet_VERDI) {
        int åpning_oppføring = bekrefte(INDEKS);
        if (åpning_oppføring < 0) return -9;
        if (kapasitet_VERDI < 0 || kapasitet_VERDI > 512) return -22;
        if (vare_ANTALL[åpning_oppføring] == 0) return -11;
        int posisjonsindeks = åpning_oppføring * 4 + frontkamera_VERDI[åpning_oppføring];
        int Størrelse = lengde_VERDI[posisjonsindeks] < kapasitet_VERDI ? lengde_VERDI[posisjonsindeks] : kapasitet_VERDI;
        for (int byte_VERDI = 0; byte_VERDI < Størrelse; byte_VERDI++) Frem_VERDI[byte_VERDI] = data[posisjonsindeks * 512 + byte_VERDI];
        MOTTATT_AVKAST_port[åpning_oppføring] = 보낸창구[posisjonsindeks]; frontkamera_VERDI[åpning_oppføring] = (frontkamera_VERDI[åpning_oppføring] + 1) % 4; vare_ANTALL[åpning_oppføring]--;
        return Størrelse;
    }
    public static int 창구읽기(int INDEKS) { int åpning_oppføring = bekrefte(INDEKS); return åpning_oppføring < 0 ? -9 : port_VERDI[åpning_oppføring]; }
    public static int 주소읽기(int INDEKS) { int åpning_oppføring = bekrefte(INDEKS); return åpning_oppføring < 0 ? -9 : e_post[åpning_oppføring]; }
    public static int avsender_deltaker(int INDEKS) { int åpning_oppføring = bekrefte(INDEKS); return åpning_oppføring < 0 ? -9 : MOTTATT_AVKAST_port[åpning_oppføring]; }
    public static int Lukk(int INDEKS) {
        int åpning_oppføring = bekrefte(INDEKS); if (åpning_oppføring < 0) return -9;
        bruk_VERDI[åpning_oppføring] = 0; vare_ANTALL[åpning_oppføring] = 0; port_VERDI[åpning_oppføring] = 0; return 0;
    }
}
