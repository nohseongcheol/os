// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 tekkeendi_njaru: 단일 aaluude_njaru 안의 IPv4/UDP 루프백 egginde_njaru.
 * 외부 IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * taƴde_toɓɓere 8개, 끝점당 전문 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class 되돌림망 {
    static int[] 사용 = new int[8];
    static int[] poor_njaru = new int[8];
    static int[] ñiiɓirde = new int[8];
    static int[] 앞 = new int[8];
    static int[] 개수 = new int[8];
    static int[] 받은창구 = new int[8];
    static int[] njuuteendi_njaru = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] keɓe = new int[32 * 512];
    static int[] yawtinde_njaru = new int[512];
    static int 다음창구 = 49152;
    static int ƴeewtaade(int joopirdu) { return joopirdu >= 32 && joopirdu < 40 && 사용[joopirdu - 32] != 0 ? joopirdu - 32 : -1; }
    static boolean 겹침(int joopirdu) {
        for (int 칸 = 0; 칸 < 8; 칸++) if (사용[칸] != 0 && poor_njaru[칸] == joopirdu) return true;
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
    public static int 만들기(int 영역, int 종류, int haaju_njaru) {
        if (영역 != 2) return -97;
        if (종류 != 2 || (haaju_njaru != 0 && haaju_njaru != 17)) return -93;
        for (int 칸 = 0; 칸 < 8; 칸++) if (사용[칸] == 0) {
            사용[칸] = 1; poor_njaru[칸] = 0; ñiiɓirde[칸] = 0; 앞[칸] = 0; 개수[칸] = 0; 받은창구[칸] = 0;
            return 칸 + 32;
        }
        return -24;
    }
    public static int 묶기(int joopirdu, int laylaytol_ñiiɓirde, int 창구번호) {
        int 칸 = ƴeewtaade(joopirdu);
        if (칸 < 0) return -9;
        if (laylaytol_ñiiɓirde != 0 && laylaytol_ñiiɓirde != 0x7f000001) return -99;
        if (poor_njaru[칸] != 0 || 창구번호 < 0 || 창구번호 > 65535) return -22;
        if (창구번호 == 0) 창구번호 = 임시창구();
        if (창구번호 < 0) return 창구번호;
        if (겹침(창구번호)) return -98;
        poor_njaru[칸] = 창구번호; ñiiɓirde[칸] = laylaytol_ñiiɓirde; return 0;
    }
    public static int 자료넣기(int joopirdu, int njaru) {
        if (joopirdu < 0 || joopirdu >= 512) return -22;
        yawtinde_njaru[joopirdu] = njaru & 255; return 0;
    }
    public static int 자료읽기(int joopirdu) { return joopirdu >= 0 && joopirdu < 512 ? yawtinde_njaru[joopirdu] : -22; }
    public static int neldude(int joopirdu, int laylaytol_ñiiɓirde, int 창구번호, int waylude_etannde) {
        int 칸 = ƴeewtaade(joopirdu);
        if (칸 < 0) return -9;
        if (laylaytol_ñiiɓirde != 0x7f000001) return -101;
        if (창구번호 < 1 || 창구번호 > 65535) return -22;
        if (waylude_etannde < 0 || waylude_etannde > 512) return -90;
        if (poor_njaru[칸] == 0) {
            int 결과 = 묶기(joopirdu, 0x7f000001, 0);
            if (결과 < 0) return 결과;
        }
        int tiindaare_njaru = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (사용[후보] != 0 && poor_njaru[후보] == 창구번호) tiindaare_njaru = 후보;
        if (tiindaare_njaru < 0) return -111;
        if (개수[tiindaare_njaru] == 4) return -11;
        int 자리 = tiindaare_njaru * 4 + (앞[tiindaare_njaru] + 개수[tiindaare_njaru]) % 4;
        for (int oktee_njaru = 0; oktee_njaru < waylude_etannde; oktee_njaru++) keɓe[자리 * 512 + oktee_njaru] = yawtinde_njaru[oktee_njaru];
        njuuteendi_njaru[자리] = waylude_etannde; 보낸창구[자리] = poor_njaru[칸]; 개수[tiindaare_njaru]++;
        return waylude_etannde;
    }
    public static int 받기(int joopirdu, int 용량) {
        int 칸 = ƴeewtaade(joopirdu);
        if (칸 < 0) return -9;
        if (용량 < 0 || 용량 > 512) return -22;
        if (개수[칸] == 0) return -11;
        int 자리 = 칸 * 4 + 앞[칸];
        int waylude_etannde = njuuteendi_njaru[자리] < 용량 ? njuuteendi_njaru[자리] : 용량;
        for (int oktee_njaru = 0; oktee_njaru < waylude_etannde; oktee_njaru++) yawtinde_njaru[oktee_njaru] = keɓe[자리 * 512 + oktee_njaru];
        받은창구[칸] = 보낸창구[자리]; 앞[칸] = (앞[칸] + 1) % 4; 개수[칸]--;
        return waylude_etannde;
    }
    public static int 창구읽기(int joopirdu) { int 칸 = ƴeewtaade(joopirdu); return 칸 < 0 ? -9 : poor_njaru[칸]; }
    public static int 주소읽기(int joopirdu) { int 칸 = ƴeewtaade(joopirdu); return 칸 < 0 ? -9 : ñiiɓirde[칸]; }
    public static int 보낸곳(int joopirdu) { int 칸 = ƴeewtaade(joopirdu); return 칸 < 0 ? -9 : 받은창구[칸]; }
    public static int uddude(int joopirdu) {
        int 칸 = ƴeewtaade(joopirdu); if (칸 < 0) return -9;
        사용[칸] = 0; 개수[칸] = 0; poor_njaru[칸] = 0; return 0;
    }
}
