// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 ìpele_iye: 단일 kánẹ́ẹ̀lì_iye 안의 IPv4/UDP 루프백 ṣàgbélọ_iye.
 * 외부 IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * parí_kókó 8개, 끝점당 전문 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class 되돌림망 {
    static int[] 사용 = new int[8];
    static int[] ojú_iye = new int[8];
    static int[] àdírẹ́ẹ̀sì = new int[8];
    static int[] 앞 = new int[8];
    static int[] 개수 = new int[8];
    static int[] 받은창구 = new int[8];
    static int[] gígùn_iye = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] détà = new int[32 * 512];
    static int[] tari_sí_iye = new int[512];
    static int 다음창구 = 49152;
    static int ridájú(int wá_atọ̀ka_àkóónú) { return wá_atọ̀ka_àkóónú >= 32 && wá_atọ̀ka_àkóónú < 40 && 사용[wá_atọ̀ka_àkóónú - 32] != 0 ? wá_atọ̀ka_àkóónú - 32 : -1; }
    static boolean 겹침(int wá_atọ̀ka_àkóónú) {
        for (int ààyè_ìfàyọkàsí_ìgbéwọlé = 0; ààyè_ìfàyọkàsí_ìgbéwọlé < 8; ààyè_ìfàyọkàsí_ìgbéwọlé++) if (사용[ààyè_ìfàyọkàsí_ìgbéwọlé] != 0 && ojú_iye[ààyè_ìfàyọkàsí_ìgbéwọlé] == wá_atọ̀ka_àkóónú) return true;
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
    public static int Ṣẹ̀dá_ìgbéwọlé(int 영역, int 종류, int iṣẹ́_iye) {
        if (영역 != 2) return -97;
        if (종류 != 2 || (iṣẹ́_iye != 0 && iṣẹ́_iye != 17)) return -93;
        for (int ààyè_ìfàyọkàsí_ìgbéwọlé = 0; ààyè_ìfàyọkàsí_ìgbéwọlé < 8; ààyè_ìfàyọkàsí_ìgbéwọlé++) if (사용[ààyè_ìfàyọkàsí_ìgbéwọlé] == 0) {
            사용[ààyè_ìfàyọkàsí_ìgbéwọlé] = 1; ojú_iye[ààyè_ìfàyọkàsí_ìgbéwọlé] = 0; àdírẹ́ẹ̀sì[ààyè_ìfàyọkàsí_ìgbéwọlé] = 0; 앞[ààyè_ìfàyọkàsí_ìgbéwọlé] = 0; 개수[ààyè_ìfàyọkàsí_ìgbéwọlé] = 0; 받은창구[ààyè_ìfàyọkàsí_ìgbéwọlé] = 0;
            return ààyè_ìfàyọkàsí_ìgbéwọlé + 32;
        }
        return -24;
    }
    public static int 묶기(int wá_atọ̀ka_àkóónú, int Alásopọ̀_àdírẹ́ẹ̀sì, int 창구번호) {
        int ààyè_ìfàyọkàsí_ìgbéwọlé = ridájú(wá_atọ̀ka_àkóónú);
        if (ààyè_ìfàyọkàsí_ìgbéwọlé < 0) return -9;
        if (Alásopọ̀_àdírẹ́ẹ̀sì != 0 && Alásopọ̀_àdírẹ́ẹ̀sì != 0x7f000001) return -99;
        if (ojú_iye[ààyè_ìfàyọkàsí_ìgbéwọlé] != 0 || 창구번호 < 0 || 창구번호 > 65535) return -22;
        if (창구번호 == 0) 창구번호 = 임시창구();
        if (창구번호 < 0) return 창구번호;
        if (겹침(창구번호)) return -98;
        ojú_iye[ààyè_ìfàyọkàsí_ìgbéwọlé] = 창구번호; àdírẹ́ẹ̀sì[ààyè_ìfàyọkàsí_ìgbéwọlé] = Alásopọ̀_àdírẹ́ẹ̀sì; return 0;
    }
    public static int 자료넣기(int wá_atọ̀ka_àkóónú, int iye) {
        if (wá_atọ̀ka_àkóónú < 0 || wá_atọ̀ka_àkóónú >= 512) return -22;
        tari_sí_iye[wá_atọ̀ka_àkóónú] = iye & 255; return 0;
    }
    public static int 자료읽기(int wá_atọ̀ka_àkóónú) { return wá_atọ̀ka_àkóónú >= 0 && wá_atọ̀ka_àkóónú < 512 ? tari_sí_iye[wá_atọ̀ka_àkóónú] : -22; }
    public static int í_meèlì(int wá_atọ̀ka_àkóónú, int Alásopọ̀_àdírẹ́ẹ̀sì, int 창구번호, int Ìwọ̀n) {
        int ààyè_ìfàyọkàsí_ìgbéwọlé = ridájú(wá_atọ̀ka_àkóónú);
        if (ààyè_ìfàyọkàsí_ìgbéwọlé < 0) return -9;
        if (Alásopọ̀_àdírẹ́ẹ̀sì != 0x7f000001) return -101;
        if (창구번호 < 1 || 창구번호 > 65535) return -22;
        if (Ìwọ̀n < 0 || Ìwọ̀n > 512) return -90;
        if (ojú_iye[ààyè_ìfàyọkàsí_ìgbéwọlé] == 0) {
            int 결과 = 묶기(wá_atọ̀ka_àkóónú, 0x7f000001, 0);
            if (결과 < 0) return 결과;
        }
        int èbúté_iye = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (사용[후보] != 0 && ojú_iye[후보] == 창구번호) èbúté_iye = 후보;
        if (èbúté_iye < 0) return -111;
        if (개수[èbúté_iye] == 4) return -11;
        int 자리 = èbúté_iye * 4 + (앞[èbúté_iye] + 개수[èbúté_iye]) % 4;
        for (int báìtì_iye = 0; báìtì_iye < Ìwọ̀n; báìtì_iye++) détà[자리 * 512 + báìtì_iye] = tari_sí_iye[báìtì_iye];
        gígùn_iye[자리] = Ìwọ̀n; 보낸창구[자리] = ojú_iye[ààyè_ìfàyọkàsí_ìgbéwọlé]; 개수[èbúté_iye]++;
        return Ìwọ̀n;
    }
    public static int 받기(int wá_atọ̀ka_àkóónú, int 용량) {
        int ààyè_ìfàyọkàsí_ìgbéwọlé = ridájú(wá_atọ̀ka_àkóónú);
        if (ààyè_ìfàyọkàsí_ìgbéwọlé < 0) return -9;
        if (용량 < 0 || 용량 > 512) return -22;
        if (개수[ààyè_ìfàyọkàsí_ìgbéwọlé] == 0) return -11;
        int 자리 = ààyè_ìfàyọkàsí_ìgbéwọlé * 4 + 앞[ààyè_ìfàyọkàsí_ìgbéwọlé];
        int Ìwọ̀n = gígùn_iye[자리] < 용량 ? gígùn_iye[자리] : 용량;
        for (int báìtì_iye = 0; báìtì_iye < Ìwọ̀n; báìtì_iye++) tari_sí_iye[báìtì_iye] = détà[자리 * 512 + báìtì_iye];
        받은창구[ààyè_ìfàyọkàsí_ìgbéwọlé] = 보낸창구[자리]; 앞[ààyè_ìfàyọkàsí_ìgbéwọlé] = (앞[ààyè_ìfàyọkàsí_ìgbéwọlé] + 1) % 4; 개수[ààyè_ìfàyọkàsí_ìgbéwọlé]--;
        return Ìwọ̀n;
    }
    public static int 창구읽기(int wá_atọ̀ka_àkóónú) { int ààyè_ìfàyọkàsí_ìgbéwọlé = ridájú(wá_atọ̀ka_àkóónú); return ààyè_ìfàyọkàsí_ìgbéwọlé < 0 ? -9 : ojú_iye[ààyè_ìfàyọkàsí_ìgbéwọlé]; }
    public static int 주소읽기(int wá_atọ̀ka_àkóónú) { int ààyè_ìfàyọkàsí_ìgbéwọlé = ridájú(wá_atọ̀ka_àkóónú); return ààyè_ìfàyọkàsí_ìgbéwọlé < 0 ? -9 : àdírẹ́ẹ̀sì[ààyè_ìfàyọkàsí_ìgbéwọlé]; }
    public static int 보낸곳(int wá_atọ̀ka_àkóónú) { int ààyè_ìfàyọkàsí_ìgbéwọlé = ridájú(wá_atọ̀ka_àkóónú); return ààyè_ìfàyọkàsí_ìgbéwọlé < 0 ? -9 : 받은창구[ààyè_ìfàyọkàsí_ìgbéwọlé]; }
    public static int Ti(int wá_atọ̀ka_àkóónú) {
        int ààyè_ìfàyọkàsí_ìgbéwọlé = ridájú(wá_atọ̀ka_àkóónú); if (ààyè_ìfàyọkàsí_ìgbéwọlé < 0) return -9;
        사용[ààyè_ìfàyọkàsí_ìgbéwọlé] = 0; 개수[ààyè_ìfàyọkàsí_ìgbéwọlé] = 0; ojú_iye[ààyè_ìfàyọkàsí_ìgbéwọlé] = 0; return 0;
    }
}
