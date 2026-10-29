// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 qatlam_VALUE: 단일 o_zak_VALUE 안의 IPv4/UDP 루프백 uzatish_VALUE.
 * 외부 IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * to_xtatmoq_nuqta 8개, 끝점당 전문 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class 되돌림망 {
    static int[] 사용 = new int[8];
    static int[] port_VALUE = new int[8];
    static int[] manzil = new int[8];
    static int[] old_kamera_VALUE = new int[8];
    static int[] element_COUNT = new int[8];
    static int[] RECEIVED_port = new int[8];
    static int[] uzunlik_VALUE = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] ma_lumotlar = new int[32 * 512];
    static int[] Oldinga_VALUE = new int[512];
    static int 다음창구 = 49152;
    static int tasdiqlamoq(int INDEX) { return INDEX >= 32 && INDEX < 40 && 사용[INDEX - 32] != 0 ? INDEX - 32 : -1; }
    static boolean 겹침(int INDEX) {
        for (int in_kiritish = 0; in_kiritish < 8; in_kiritish++) if (사용[in_kiritish] != 0 && port_VALUE[in_kiritish] == INDEX) return true;
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
    public static int Yaratish_kiritish(int 영역, int 종류, int murojaat_VALUE) {
        if (영역 != 2) return -97;
        if (종류 != 2 || (murojaat_VALUE != 0 && murojaat_VALUE != 17)) return -93;
        for (int in_kiritish = 0; in_kiritish < 8; in_kiritish++) if (사용[in_kiritish] == 0) {
            사용[in_kiritish] = 1; port_VALUE[in_kiritish] = 0; manzil[in_kiritish] = 0; old_kamera_VALUE[in_kiritish] = 0; element_COUNT[in_kiritish] = 0; RECEIVED_port[in_kiritish] = 0;
            return in_kiritish + 32;
        }
        return -24;
    }
    public static int 묶기(int INDEX, int Tarmoq_manzil, int 창구번호) {
        int in_kiritish = tasdiqlamoq(INDEX);
        if (in_kiritish < 0) return -9;
        if (Tarmoq_manzil != 0 && Tarmoq_manzil != 0x7f000001) return -99;
        if (port_VALUE[in_kiritish] != 0 || 창구번호 < 0 || 창구번호 > 65535) return -22;
        if (창구번호 == 0) 창구번호 = 임시창구();
        if (창구번호 < 0) return 창구번호;
        if (겹침(창구번호)) return -98;
        port_VALUE[in_kiritish] = 창구번호; manzil[in_kiritish] = Tarmoq_manzil; return 0;
    }
    public static int 자료넣기(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= 512) return -22;
        Oldinga_VALUE[INDEX] = VALUE & 255; return 0;
    }
    public static int 자료읽기(int INDEX) { return INDEX >= 0 && INDEX < 512 ? Oldinga_VALUE[INDEX] : -22; }
    public static int yuborish(int INDEX, int Tarmoq_manzil, int 창구번호, int Hajmi) {
        int in_kiritish = tasdiqlamoq(INDEX);
        if (in_kiritish < 0) return -9;
        if (Tarmoq_manzil != 0x7f000001) return -101;
        if (창구번호 < 1 || 창구번호 > 65535) return -22;
        if (Hajmi < 0 || Hajmi > 512) return -90;
        if (port_VALUE[in_kiritish] == 0) {
            int o_lchov = 묶기(INDEX, 0x7f000001, 0);
            if (o_lchov < 0) return o_lchov;
        }
        int ko_chirish_joyi_VALUE = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (사용[후보] != 0 && port_VALUE[후보] == 창구번호) ko_chirish_joyi_VALUE = 후보;
        if (ko_chirish_joyi_VALUE < 0) return -111;
        if (element_COUNT[ko_chirish_joyi_VALUE] == 4) return -11;
        int holat_INDEX = ko_chirish_joyi_VALUE * 4 + (old_kamera_VALUE[ko_chirish_joyi_VALUE] + element_COUNT[ko_chirish_joyi_VALUE]) % 4;
        for (int bayt_VALUE = 0; bayt_VALUE < Hajmi; bayt_VALUE++) ma_lumotlar[holat_INDEX * 512 + bayt_VALUE] = Oldinga_VALUE[bayt_VALUE];
        uzunlik_VALUE[holat_INDEX] = Hajmi; 보낸창구[holat_INDEX] = port_VALUE[in_kiritish]; element_COUNT[ko_chirish_joyi_VALUE]++;
        return Hajmi;
    }
    public static int 받기(int INDEX, int 용량) {
        int in_kiritish = tasdiqlamoq(INDEX);
        if (in_kiritish < 0) return -9;
        if (용량 < 0 || 용량 > 512) return -22;
        if (element_COUNT[in_kiritish] == 0) return -11;
        int holat_INDEX = in_kiritish * 4 + old_kamera_VALUE[in_kiritish];
        int Hajmi = uzunlik_VALUE[holat_INDEX] < 용량 ? uzunlik_VALUE[holat_INDEX] : 용량;
        for (int bayt_VALUE = 0; bayt_VALUE < Hajmi; bayt_VALUE++) Oldinga_VALUE[bayt_VALUE] = ma_lumotlar[holat_INDEX * 512 + bayt_VALUE];
        RECEIVED_port[in_kiritish] = 보낸창구[holat_INDEX]; old_kamera_VALUE[in_kiritish] = (old_kamera_VALUE[in_kiritish] + 1) % 4; element_COUNT[in_kiritish]--;
        return Hajmi;
    }
    public static int 창구읽기(int INDEX) { int in_kiritish = tasdiqlamoq(INDEX); return in_kiritish < 0 ? -9 : port_VALUE[in_kiritish]; }
    public static int 주소읽기(int INDEX) { int in_kiritish = tasdiqlamoq(INDEX); return in_kiritish < 0 ? -9 : manzil[in_kiritish]; }
    public static int 보낸곳(int INDEX) { int in_kiritish = tasdiqlamoq(INDEX); return in_kiritish < 0 ? -9 : RECEIVED_port[in_kiritish]; }
    public static int Yopish(int INDEX) {
        int in_kiritish = tasdiqlamoq(INDEX); if (in_kiritish < 0) return -9;
        사용[in_kiritish] = 0; element_COUNT[in_kiritish] = 0; port_VALUE[in_kiritish] = 0; return 0;
    }
}
