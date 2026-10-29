// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 lay_VALUE: 단일 nüvə_VALUE 안의 IPv4/UDP 루프백 ötürmə_VALUE.
 * 외부 IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * bitirmək_p 8개, 끝점당 전문 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class 되돌림망 {
    static int[] 사용 = new int[8];
    static int[] port_VALUE = new int[8];
    static int[] ünvan = new int[8];
    static int[] ön_VALUE = new int[8];
    static int[] element_COUNT = new int[8];
    static int[] RECEIVED_port = new int[8];
    static int[] uzunluq_VALUE = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] verilənlər = new int[32 * 512];
    static int[] irəli_VALUE = new int[512];
    static int 다음창구 = 49152;
    static int yoxlamaq(int INDEX) { return INDEX >= 32 && INDEX < 40 && 사용[INDEX - 32] != 0 ? INDEX - 32 : -1; }
    static boolean 겹침(int INDEX) {
        for (int slot_daxiletmə = 0; slot_daxiletmə < 8; slot_daxiletmə++) if (사용[slot_daxiletmə] != 0 && port_VALUE[slot_daxiletmə] == INDEX) return true;
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
    public static int yarat_daxiletmə(int 영역, int 종류, int müqavilə_VALUE) {
        if (영역 != 2) return -97;
        if (종류 != 2 || (müqavilə_VALUE != 0 && müqavilə_VALUE != 17)) return -93;
        for (int slot_daxiletmə = 0; slot_daxiletmə < 8; slot_daxiletmə++) if (사용[slot_daxiletmə] == 0) {
            사용[slot_daxiletmə] = 1; port_VALUE[slot_daxiletmə] = 0; ünvan[slot_daxiletmə] = 0; ön_VALUE[slot_daxiletmə] = 0; element_COUNT[slot_daxiletmə] = 0; RECEIVED_port[slot_daxiletmə] = 0;
            return slot_daxiletmə + 32;
        }
        return -24;
    }
    public static int 묶기(int INDEX, int Şəbəkə_ünvan, int 창구번호) {
        int slot_daxiletmə = yoxlamaq(INDEX);
        if (slot_daxiletmə < 0) return -9;
        if (Şəbəkə_ünvan != 0 && Şəbəkə_ünvan != 0x7f000001) return -99;
        if (port_VALUE[slot_daxiletmə] != 0 || 창구번호 < 0 || 창구번호 > 65535) return -22;
        if (창구번호 == 0) 창구번호 = 임시창구();
        if (창구번호 < 0) return 창구번호;
        if (겹침(창구번호)) return -98;
        port_VALUE[slot_daxiletmə] = 창구번호; ünvan[slot_daxiletmə] = Şəbəkə_ünvan; return 0;
    }
    public static int 자료넣기(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= 512) return -22;
        irəli_VALUE[INDEX] = VALUE & 255; return 0;
    }
    public static int 자료읽기(int INDEX) { return INDEX >= 0 && INDEX < 512 ? irəli_VALUE[INDEX] : -22; }
    public static int göndərmək(int INDEX, int Şəbəkə_ünvan, int 창구번호, int Böyüklük) {
        int slot_daxiletmə = yoxlamaq(INDEX);
        if (slot_daxiletmə < 0) return -9;
        if (Şəbəkə_ünvan != 0x7f000001) return -101;
        if (창구번호 < 1 || 창구번호 > 65535) return -22;
        if (Böyüklük < 0 || Böyüklük > 512) return -90;
        if (port_VALUE[slot_daxiletmə] == 0) {
            int ölçü = 묶기(INDEX, 0x7f000001, 0);
            if (ölçü < 0) return ölçü;
        }
        int təyinat_VALUE_a0fbc067 = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (사용[후보] != 0 && port_VALUE[후보] == 창구번호) təyinat_VALUE_a0fbc067 = 후보;
        if (təyinat_VALUE_a0fbc067 < 0) return -111;
        if (element_COUNT[təyinat_VALUE_a0fbc067] == 4) return -11;
        int yerinə_qoymaq_INDEX = təyinat_VALUE_a0fbc067 * 4 + (ön_VALUE[təyinat_VALUE_a0fbc067] + element_COUNT[təyinat_VALUE_a0fbc067]) % 4;
        for (int bayt_VALUE = 0; bayt_VALUE < Böyüklük; bayt_VALUE++) verilənlər[yerinə_qoymaq_INDEX * 512 + bayt_VALUE] = irəli_VALUE[bayt_VALUE];
        uzunluq_VALUE[yerinə_qoymaq_INDEX] = Böyüklük; 보낸창구[yerinə_qoymaq_INDEX] = port_VALUE[slot_daxiletmə]; element_COUNT[təyinat_VALUE_a0fbc067]++;
        return Böyüklük;
    }
    public static int 받기(int INDEX, int 용량) {
        int slot_daxiletmə = yoxlamaq(INDEX);
        if (slot_daxiletmə < 0) return -9;
        if (용량 < 0 || 용량 > 512) return -22;
        if (element_COUNT[slot_daxiletmə] == 0) return -11;
        int yerinə_qoymaq_INDEX = slot_daxiletmə * 4 + ön_VALUE[slot_daxiletmə];
        int Böyüklük = uzunluq_VALUE[yerinə_qoymaq_INDEX] < 용량 ? uzunluq_VALUE[yerinə_qoymaq_INDEX] : 용량;
        for (int bayt_VALUE = 0; bayt_VALUE < Böyüklük; bayt_VALUE++) irəli_VALUE[bayt_VALUE] = verilənlər[yerinə_qoymaq_INDEX * 512 + bayt_VALUE];
        RECEIVED_port[slot_daxiletmə] = 보낸창구[yerinə_qoymaq_INDEX]; ön_VALUE[slot_daxiletmə] = (ön_VALUE[slot_daxiletmə] + 1) % 4; element_COUNT[slot_daxiletmə]--;
        return Böyüklük;
    }
    public static int 창구읽기(int INDEX) { int slot_daxiletmə = yoxlamaq(INDEX); return slot_daxiletmə < 0 ? -9 : port_VALUE[slot_daxiletmə]; }
    public static int 주소읽기(int INDEX) { int slot_daxiletmə = yoxlamaq(INDEX); return slot_daxiletmə < 0 ? -9 : ünvan[slot_daxiletmə]; }
    public static int 보낸곳(int INDEX) { int slot_daxiletmə = yoxlamaq(INDEX); return slot_daxiletmə < 0 ? -9 : RECEIVED_port[slot_daxiletmə]; }
    public static int Bağla(int INDEX) {
        int slot_daxiletmə = yoxlamaq(INDEX); if (slot_daxiletmə < 0) return -9;
        사용[slot_daxiletmə] = 0; element_COUNT[slot_daxiletmə] = 0; port_VALUE[slot_daxiletmə] = 0; return 0;
    }
}
