// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 tabaka_thamani: 단일 kiini_thamani_0611a8a8 안의 IPv4/UDP 루프백 hamisha_thamani_630ba093.
 * 외부 IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * tamatia_pointi 8개, 끝점당 전문 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class 되돌림망 {
    static int[] 사용 = new int[8];
    static int[] kituo_thamani = new int[8];
    static int[] anwani = new int[8];
    static int[] mbele_thamani = new int[8];
    static int[] 개수 = new int[8];
    static int[] 받은창구 = new int[8];
    static int[] urefu_thamani = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] data = new int[32 * 512];
    static int[] tuma_mbele_thamani = new int[512];
    static int 다음창구 = 49152;
    static int thibitisha(int kielezo) { return kielezo >= 32 && kielezo < 40 && 사용[kielezo - 32] != 0 ? kielezo - 32 : -1; }
    static boolean 겹침(int kielezo) {
        for (int Sloti_ingizo = 0; Sloti_ingizo < 8; Sloti_ingizo++) if (사용[Sloti_ingizo] != 0 && kituo_thamani[Sloti_ingizo] == kielezo) return true;
        return false;
    }
    static int 임시창구() {
        for (int 시도 = 0; 시도 < 16; 시도++) {
            int 후보 = 다음창구++;
            if (다음창구 > 65535) 다음창구 = 49152;
            if (!겹침(후보)) return 후보;
        }
        return -98;
    }
    public static int unda_ingizo(int 영역, int 종류, int Kazi_thamani) {
        if (영역 != 2) return -97;
        if (종류 != 2 || (Kazi_thamani != 0 && Kazi_thamani != 17)) return -93;
        for (int Sloti_ingizo = 0; Sloti_ingizo < 8; Sloti_ingizo++) if (사용[Sloti_ingizo] == 0) {
            사용[Sloti_ingizo] = 1; kituo_thamani[Sloti_ingizo] = 0; anwani[Sloti_ingizo] = 0; mbele_thamani[Sloti_ingizo] = 0; 개수[Sloti_ingizo] = 0; 받은창구[Sloti_ingizo] = 0;
            return Sloti_ingizo + 32;
        }
        return -24;
    }
    public static int 묶기(int kielezo, int Mtandao_anwani, int 창구번호) {
        int Sloti_ingizo = thibitisha(kielezo);
        if (Sloti_ingizo < 0) return -9;
        if (Mtandao_anwani != 0 && Mtandao_anwani != 0x7f000001) return -99;
        if (kituo_thamani[Sloti_ingizo] != 0 || 창구번호 < 0 || 창구번호 > 65535) return -22;
        if (창구번호 == 0) 창구번호 = 임시창구();
        if (창구번호 < 0) return 창구번호;
        if (겹침(창구번호)) return -98;
        kituo_thamani[Sloti_ingizo] = 창구번호; anwani[Sloti_ingizo] = Mtandao_anwani; return 0;
    }
    public static int 자료넣기(int kielezo, int thamani) {
        if (kielezo < 0 || kielezo >= 512) return -22;
        tuma_mbele_thamani[kielezo] = thamani & 255; return 0;
    }
    public static int 자료읽기(int kielezo) { return kielezo >= 0 && kielezo < 512 ? tuma_mbele_thamani[kielezo] : -22; }
    public static int tuma(int kielezo, int Mtandao_anwani, int 창구번호, int panga_ukubwa) {
        int Sloti_ingizo = thibitisha(kielezo);
        if (Sloti_ingizo < 0) return -9;
        if (Mtandao_anwani != 0x7f000001) return -101;
        if (창구번호 < 1 || 창구번호 > 65535) return -22;
        if (panga_ukubwa < 0 || panga_ukubwa > 512) return -90;
        if (kituo_thamani[Sloti_ingizo] == 0) {
            int 결과 = 묶기(kielezo, 0x7f000001, 0);
            if (결과 < 0) return 결과;
        }
        int fikio_thamani = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (사용[후보] != 0 && kituo_thamani[후보] == 창구번호) fikio_thamani = 후보;
        if (fikio_thamani < 0) return -111;
        if (개수[fikio_thamani] == 4) return -11;
        int 자리 = fikio_thamani * 4 + (mbele_thamani[fikio_thamani] + 개수[fikio_thamani]) % 4;
        for (int baiti_thamani = 0; baiti_thamani < panga_ukubwa; baiti_thamani++) data[자리 * 512 + baiti_thamani] = tuma_mbele_thamani[baiti_thamani];
        urefu_thamani[자리] = panga_ukubwa; 보낸창구[자리] = kituo_thamani[Sloti_ingizo]; 개수[fikio_thamani]++;
        return panga_ukubwa;
    }
    public static int 받기(int kielezo, int 용량) {
        int Sloti_ingizo = thibitisha(kielezo);
        if (Sloti_ingizo < 0) return -9;
        if (용량 < 0 || 용량 > 512) return -22;
        if (개수[Sloti_ingizo] == 0) return -11;
        int 자리 = Sloti_ingizo * 4 + mbele_thamani[Sloti_ingizo];
        int panga_ukubwa = urefu_thamani[자리] < 용량 ? urefu_thamani[자리] : 용량;
        for (int baiti_thamani = 0; baiti_thamani < panga_ukubwa; baiti_thamani++) tuma_mbele_thamani[baiti_thamani] = data[자리 * 512 + baiti_thamani];
        받은창구[Sloti_ingizo] = 보낸창구[자리]; mbele_thamani[Sloti_ingizo] = (mbele_thamani[Sloti_ingizo] + 1) % 4; 개수[Sloti_ingizo]--;
        return panga_ukubwa;
    }
    public static int 창구읽기(int kielezo) { int Sloti_ingizo = thibitisha(kielezo); return Sloti_ingizo < 0 ? -9 : kituo_thamani[Sloti_ingizo]; }
    public static int 주소읽기(int kielezo) { int Sloti_ingizo = thibitisha(kielezo); return Sloti_ingizo < 0 ? -9 : anwani[Sloti_ingizo]; }
    public static int 보낸곳(int kielezo) { int Sloti_ingizo = thibitisha(kielezo); return Sloti_ingizo < 0 ? -9 : 받은창구[Sloti_ingizo]; }
    public static int funga(int kielezo) {
        int Sloti_ingizo = thibitisha(kielezo); if (Sloti_ingizo < 0) return -9;
        사용[Sloti_ingizo] = 0; 개수[Sloti_ingizo] = 0; kituo_thamani[Sloti_ingizo] = 0; return 0;
    }
}
