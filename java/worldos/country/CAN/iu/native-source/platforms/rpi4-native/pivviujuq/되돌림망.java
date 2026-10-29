// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 qaliriit_atuutilik: 단일 kernel_atuutilik 안의 IPv4/UDP 루프백 aullaaqtilli_atuutilik.
 * 외부 IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * isulittuq_puinti 8개, 끝점당 전문 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class 되돌림망 {
    static int[] 사용 = new int[8];
    static int[] kapputigaq_atuutilik = new int[8];
    static int[] turaarut = new int[8];
    static int[] 앞 = new int[8];
    static int[] 개수 = new int[8];
    static int[] 받은창구 = new int[8];
    static int[] takininga_atuutilik = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] titiqqat = new int[32 * 512];
    static int[] sivummualli_atuutilik = new int[512];
    static int 다음창구 = 49152;
    static int nalunairli_1aacb54c(int nalunaiqsimavik) { return nalunaiqsimavik >= 32 && nalunaiqsimavik < 40 && 사용[nalunaiqsimavik - 32] != 0 ? nalunaiqsimavik - 32 : -1; }
    static boolean 겹침(int nalunaiqsimavik) {
        for (int 칸 = 0; 칸 < 8; 칸++) if (사용[칸] != 0 && kapputigaq_atuutilik[칸] == nalunaiqsimavik) return true;
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
    public static int 만들기(int 영역, int 종류, int pijatsaq_atuutilik) {
        if (영역 != 2) return -97;
        if (종류 != 2 || (pijatsaq_atuutilik != 0 && pijatsaq_atuutilik != 17)) return -93;
        for (int 칸 = 0; 칸 < 8; 칸++) if (사용[칸] == 0) {
            사용[칸] = 1; kapputigaq_atuutilik[칸] = 0; turaarut[칸] = 0; 앞[칸] = 0; 개수[칸] = 0; 받은창구[칸] = 0;
            return 칸 + 32;
        }
        return -24;
    }
    public static int 묶기(int nalunaiqsimavik, int Kasuqatigiitsimajut_turaarut, int 창구번호) {
        int 칸 = nalunairli_1aacb54c(nalunaiqsimavik);
        if (칸 < 0) return -9;
        if (Kasuqatigiitsimajut_turaarut != 0 && Kasuqatigiitsimajut_turaarut != 0x7f000001) return -99;
        if (kapputigaq_atuutilik[칸] != 0 || 창구번호 < 0 || 창구번호 > 65535) return -22;
        if (창구번호 == 0) 창구번호 = 임시창구();
        if (창구번호 < 0) return 창구번호;
        if (겹침(창구번호)) return -98;
        kapputigaq_atuutilik[칸] = 창구번호; turaarut[칸] = Kasuqatigiitsimajut_turaarut; return 0;
    }
    public static int 자료넣기(int nalunaiqsimavik, int atuutilik) {
        if (nalunaiqsimavik < 0 || nalunaiqsimavik >= 512) return -22;
        sivummualli_atuutilik[nalunaiqsimavik] = atuutilik & 255; return 0;
    }
    public static int 자료읽기(int nalunaiqsimavik) { return nalunaiqsimavik >= 0 && nalunaiqsimavik < 512 ? sivummualli_atuutilik[nalunaiqsimavik] : -22; }
    public static int nassiutili(int nalunaiqsimavik, int Kasuqatigiitsimajut_turaarut, int 창구번호, int anininga) {
        int 칸 = nalunairli_1aacb54c(nalunaiqsimavik);
        if (칸 < 0) return -9;
        if (Kasuqatigiitsimajut_turaarut != 0x7f000001) return -101;
        if (창구번호 < 1 || 창구번호 > 65535) return -22;
        if (anininga < 0 || anininga > 512) return -90;
        if (kapputigaq_atuutilik[칸] == 0) {
            int 결과 = 묶기(nalunaiqsimavik, 0x7f000001, 0);
            if (결과 < 0) return 결과;
        }
        int namunngarvik_atuutilik = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (사용[후보] != 0 && kapputigaq_atuutilik[후보] == 창구번호) namunngarvik_atuutilik = 후보;
        if (namunngarvik_atuutilik < 0) return -111;
        if (개수[namunngarvik_atuutilik] == 4) return -11;
        int 자리 = namunngarvik_atuutilik * 4 + (앞[namunngarvik_atuutilik] + 개수[namunngarvik_atuutilik]) % 4;
        for (int byte_atuutilik = 0; byte_atuutilik < anininga; byte_atuutilik++) titiqqat[자리 * 512 + byte_atuutilik] = sivummualli_atuutilik[byte_atuutilik];
        takininga_atuutilik[자리] = anininga; 보낸창구[자리] = kapputigaq_atuutilik[칸]; 개수[namunngarvik_atuutilik]++;
        return anininga;
    }
    public static int 받기(int nalunaiqsimavik, int 용량) {
        int 칸 = nalunairli_1aacb54c(nalunaiqsimavik);
        if (칸 < 0) return -9;
        if (용량 < 0 || 용량 > 512) return -22;
        if (개수[칸] == 0) return -11;
        int 자리 = 칸 * 4 + 앞[칸];
        int anininga = takininga_atuutilik[자리] < 용량 ? takininga_atuutilik[자리] : 용량;
        for (int byte_atuutilik = 0; byte_atuutilik < anininga; byte_atuutilik++) sivummualli_atuutilik[byte_atuutilik] = titiqqat[자리 * 512 + byte_atuutilik];
        받은창구[칸] = 보낸창구[자리]; 앞[칸] = (앞[칸] + 1) % 4; 개수[칸]--;
        return anininga;
    }
    public static int 창구읽기(int nalunaiqsimavik) { int 칸 = nalunairli_1aacb54c(nalunaiqsimavik); return 칸 < 0 ? -9 : kapputigaq_atuutilik[칸]; }
    public static int 주소읽기(int nalunaiqsimavik) { int 칸 = nalunairli_1aacb54c(nalunaiqsimavik); return 칸 < 0 ? -9 : turaarut[칸]; }
    public static int 보낸곳(int nalunaiqsimavik) { int 칸 = nalunairli_1aacb54c(nalunaiqsimavik); return 칸 < 0 ? -9 : 받은창구[칸]; }
    public static int matuli(int nalunaiqsimavik) {
        int 칸 = nalunairli_1aacb54c(nalunaiqsimavik); if (칸 < 0) return -9;
        사용[칸] = 0; 개수[칸] = 0; kapputigaq_atuutilik[칸] = 0; return 0;
    }
}
