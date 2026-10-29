// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 ayaleriaa_ajutuu: 단일 keetnerü_ajutuu 안의 IPv4/UDP 루프백 alate_eraa_ajutuu.
 * 외부 IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * ajattiraa_o_uchikanain 8개, 끝점당 전문 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class 되돌림망 {
    static int[] 사용 = new int[8];
    static int[] outtülee_ajutuu = new int[8];
    static int[] ejepüsee = new int[8];
    static int[] 앞 = new int[8];
    static int[] 개수 = new int[8];
    static int[] 받은창구 = new int[8];
    static int[] akaliaa_ajutuu = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] atijaaya = new int[32 * 512];
    static int[] 전달 = new int[512];
    static int 다음창구 = 49152;
    static int 확인(int ee_iyatialujuna) { return ee_iyatialujuna >= 32 && ee_iyatialujuna < 40 && 사용[ee_iyatialujuna - 32] != 0 ? ee_iyatialujuna - 32 : -1; }
    static boolean 겹침(int ee_iyatialujuna) {
        for (int 칸 = 0; 칸 < 8; 칸++) if (사용[칸] != 0 && outtülee_ajutuu[칸] == ee_iyatialujuna) return true;
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
    public static int 만들기(int 영역, int 종류, int achikii_ajutuu) {
        if (영역 != 2) return -97;
        if (종류 != 2 || (achikii_ajutuu != 0 && achikii_ajutuu != 17)) return -93;
        for (int 칸 = 0; 칸 < 8; 칸++) if (사용[칸] == 0) {
            사용[칸] = 1; outtülee_ajutuu[칸] = 0; ejepüsee[칸] = 0; 앞[칸] = 0; 개수[칸] = 0; 받은창구[칸] = 0;
            return 칸 + 32;
        }
        return -24;
    }
    public static int 묶기(int ee_iyatialujuna, int kusu_ejepüsee, int 창구번호) {
        int 칸 = 확인(ee_iyatialujuna);
        if (칸 < 0) return -9;
        if (kusu_ejepüsee != 0 && kusu_ejepüsee != 0x7f000001) return -99;
        if (outtülee_ajutuu[칸] != 0 || 창구번호 < 0 || 창구번호 > 65535) return -22;
        if (창구번호 == 0) 창구번호 = 임시창구();
        if (창구번호 < 0) return 창구번호;
        if (겹침(창구번호)) return -98;
        outtülee_ajutuu[칸] = 창구번호; ejepüsee[칸] = kusu_ejepüsee; return 0;
    }
    public static int 자료넣기(int ee_iyatialujuna, int ajutuu) {
        if (ee_iyatialujuna < 0 || ee_iyatialujuna >= 512) return -22;
        전달[ee_iyatialujuna] = ajutuu & 255; return 0;
    }
    public static int 자료읽기(int ee_iyatialujuna) { return ee_iyatialujuna >= 0 && ee_iyatialujuna < 512 ? 전달[ee_iyatialujuna] : -22; }
    public static int ajütaa(int ee_iyatialujuna, int kusu_ejepüsee, int 창구번호, int 크기) {
        int 칸 = 확인(ee_iyatialujuna);
        if (칸 < 0) return -9;
        if (kusu_ejepüsee != 0x7f000001) return -101;
        if (창구번호 < 1 || 창구번호 > 65535) return -22;
        if (크기 < 0 || 크기 > 512) return -90;
        if (outtülee_ajutuu[칸] == 0) {
            int 결과 = 묶기(ee_iyatialujuna, 0x7f000001, 0);
            if (결과 < 0) return 결과;
        }
        int jalamüinjatü_ajutuu = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (사용[후보] != 0 && outtülee_ajutuu[후보] == 창구번호) jalamüinjatü_ajutuu = 후보;
        if (jalamüinjatü_ajutuu < 0) return -111;
        if (개수[jalamüinjatü_ajutuu] == 4) return -11;
        int 자리 = jalamüinjatü_ajutuu * 4 + (앞[jalamüinjatü_ajutuu] + 개수[jalamüinjatü_ajutuu]) % 4;
        for (int waai_ajutuu = 0; waai_ajutuu < 크기; waai_ajutuu++) atijaaya[자리 * 512 + waai_ajutuu] = 전달[waai_ajutuu];
        akaliaa_ajutuu[자리] = 크기; 보낸창구[자리] = outtülee_ajutuu[칸]; 개수[jalamüinjatü_ajutuu]++;
        return 크기;
    }
    public static int 받기(int ee_iyatialujuna, int 용량) {
        int 칸 = 확인(ee_iyatialujuna);
        if (칸 < 0) return -9;
        if (용량 < 0 || 용량 > 512) return -22;
        if (개수[칸] == 0) return -11;
        int 자리 = 칸 * 4 + 앞[칸];
        int 크기 = akaliaa_ajutuu[자리] < 용량 ? akaliaa_ajutuu[자리] : 용량;
        for (int waai_ajutuu = 0; waai_ajutuu < 크기; waai_ajutuu++) 전달[waai_ajutuu] = atijaaya[자리 * 512 + waai_ajutuu];
        받은창구[칸] = 보낸창구[자리]; 앞[칸] = (앞[칸] + 1) % 4; 개수[칸]--;
        return 크기;
    }
    public static int 창구읽기(int ee_iyatialujuna) { int 칸 = 확인(ee_iyatialujuna); return 칸 < 0 ? -9 : outtülee_ajutuu[칸]; }
    public static int 주소읽기(int ee_iyatialujuna) { int 칸 = 확인(ee_iyatialujuna); return 칸 < 0 ? -9 : ejepüsee[칸]; }
    public static int 보낸곳(int ee_iyatialujuna) { int 칸 = 확인(ee_iyatialujuna); return 칸 < 0 ? -9 : 받은창구[칸]; }
    public static int asürülaa(int ee_iyatialujuna) {
        int 칸 = 확인(ee_iyatialujuna); if (칸 < 0) return -9;
        사용[칸] = 0; 개수[칸] = 0; outtülee_ajutuu[칸] = 0; return 0;
    }
}
