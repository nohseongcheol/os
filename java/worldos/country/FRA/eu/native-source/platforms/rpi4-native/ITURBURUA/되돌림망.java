// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 maila_balio: 단일 nukleo_balio 안의 IPv4/UDP 루프백 transferitu_balio.
 * 외부 IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * amaitu_p 8개, 끝점당 전문 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class 되돌림망 {
    static int[] 사용 = new int[8];
    static int[] ataka_balio = new int[8];
    static int[] helbide = new int[8];
    static int[] aurrekoa_balio = new int[8];
    static int[] elementu_ZENBATU = new int[8];
    static int[] RECEIVED_ataka = new int[8];
    static int[] luzera_balio = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] datuak = new int[32 * 512];
    static int[] Aurrera_balio = new int[512];
    static int Hurrengoa_amaiera_puntu = 49152;
    static int egiaztatu(int INDIZE) { return INDIZE >= 32 && INDIZE < 40 && 사용[INDIZE - 32] != 0 ? INDIZE - 32 : -1; }
    static boolean 겹침(int INDIZE) {
        for (int 칸 = 0; 칸 < 8; 칸++) if (사용[칸] != 0 && ataka_balio[칸] == INDIZE) return true;
        return false;
    }
    static int 임시창구() {
        for (int 시도 = 0; 시도 < 16; 시도++) {
            int 후보 = Hurrengoa_amaiera_puntu++;
            if (Hurrengoa_amaiera_puntu > 65535) Hurrengoa_amaiera_puntu = 49152;
            if (!겹침(후보)) return 후보;
        }
        return -98;
    }
    public static int sortu_sarrera(int 영역, int 종류, int kasu_balio) {
        if (영역 != 2) return -97;
        if (종류 != 2 || (kasu_balio != 0 && kasu_balio != 17)) return -93;
        for (int 칸 = 0; 칸 < 8; 칸++) if (사용[칸] == 0) {
            사용[칸] = 1; ataka_balio[칸] = 0; helbide[칸] = 0; aurrekoa_balio[칸] = 0; elementu_ZENBATU[칸] = 0; RECEIVED_ataka[칸] = 0;
            return 칸 + 32;
        }
        return -24;
    }
    public static int lotu_amaiera_puntu(int INDIZE, int sare_helbide, int amaiera_puntu_ataka_zenbaki) {
        int 칸 = egiaztatu(INDIZE);
        if (칸 < 0) return -9;
        if (sare_helbide != 0 && sare_helbide != 0x7f000001) return -99;
        if (ataka_balio[칸] != 0 || amaiera_puntu_ataka_zenbaki < 0 || amaiera_puntu_ataka_zenbaki > 65535) return -22;
        if (amaiera_puntu_ataka_zenbaki == 0) amaiera_puntu_ataka_zenbaki = 임시창구();
        if (amaiera_puntu_ataka_zenbaki < 0) return amaiera_puntu_ataka_zenbaki;
        if (겹침(amaiera_puntu_ataka_zenbaki)) return -98;
        ataka_balio[칸] = amaiera_puntu_ataka_zenbaki; helbide[칸] = sare_helbide; return 0;
    }
    public static int 자료넣기(int INDIZE, int balio) {
        if (INDIZE < 0 || INDIZE >= 512) return -22;
        Aurrera_balio[INDIZE] = balio & 255; return 0;
    }
    public static int 자료읽기(int INDIZE) { return INDIZE >= 0 && INDIZE < 512 ? Aurrera_balio[INDIZE] : -22; }
    public static int bidali(int INDIZE, int sare_helbide, int amaiera_puntu_ataka_zenbaki, int Tamaina) {
        int 칸 = egiaztatu(INDIZE);
        if (칸 < 0) return -9;
        if (sare_helbide != 0x7f000001) return -101;
        if (amaiera_puntu_ataka_zenbaki < 1 || amaiera_puntu_ataka_zenbaki > 65535) return -22;
        if (Tamaina < 0 || Tamaina > 512) return -90;
        if (ataka_balio[칸] == 0) {
            int EMAITZA = lotu_amaiera_puntu(INDIZE, 0x7f000001, 0);
            if (EMAITZA < 0) return EMAITZA;
        }
        int helburu_balio_a0fbc067 = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (사용[후보] != 0 && ataka_balio[후보] == amaiera_puntu_ataka_zenbaki) helburu_balio_a0fbc067 = 후보;
        if (helburu_balio_a0fbc067 < 0) return -111;
        if (elementu_ZENBATU[helburu_balio_a0fbc067] == 4) return -11;
        int kargu_INDIZE = helburu_balio_a0fbc067 * 4 + (aurrekoa_balio[helburu_balio_a0fbc067] + elementu_ZENBATU[helburu_balio_a0fbc067]) % 4;
        for (int byte_balio = 0; byte_balio < Tamaina; byte_balio++) datuak[kargu_INDIZE * 512 + byte_balio] = Aurrera_balio[byte_balio];
        luzera_balio[kargu_INDIZE] = Tamaina; 보낸창구[kargu_INDIZE] = ataka_balio[칸]; elementu_ZENBATU[helburu_balio_a0fbc067]++;
        return Tamaina;
    }
    public static int 받기(int INDIZE, int ahalmen_balio) {
        int 칸 = egiaztatu(INDIZE);
        if (칸 < 0) return -9;
        if (ahalmen_balio < 0 || ahalmen_balio > 512) return -22;
        if (elementu_ZENBATU[칸] == 0) return -11;
        int kargu_INDIZE = 칸 * 4 + aurrekoa_balio[칸];
        int Tamaina = luzera_balio[kargu_INDIZE] < ahalmen_balio ? luzera_balio[kargu_INDIZE] : ahalmen_balio;
        for (int byte_balio = 0; byte_balio < Tamaina; byte_balio++) Aurrera_balio[byte_balio] = datuak[kargu_INDIZE * 512 + byte_balio];
        RECEIVED_ataka[칸] = 보낸창구[kargu_INDIZE]; aurrekoa_balio[칸] = (aurrekoa_balio[칸] + 1) % 4; elementu_ZENBATU[칸]--;
        return Tamaina;
    }
    public static int 창구읽기(int INDIZE) { int 칸 = egiaztatu(INDIZE); return 칸 < 0 ? -9 : ataka_balio[칸]; }
    public static int 주소읽기(int INDIZE) { int 칸 = egiaztatu(INDIZE); return 칸 < 0 ? -9 : helbide[칸]; }
    public static int bidaltzaile_amaiera_puntu(int INDIZE) { int 칸 = egiaztatu(INDIZE); return 칸 < 0 ? -9 : RECEIVED_ataka[칸]; }
    public static int Itxi(int INDIZE) {
        int 칸 = egiaztatu(INDIZE); if (칸 < 0) return -9;
        사용[칸] = 0; elementu_ZENBATU[칸] = 0; ataka_balio[칸] = 0; return 0;
    }
}
