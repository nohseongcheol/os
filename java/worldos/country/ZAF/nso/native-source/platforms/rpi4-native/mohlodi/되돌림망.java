// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 llaga_boleng: 단일 khenele_boleng 안의 IPv4/UDP 루프백 fetišetša_boleng.
 * 외부 IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * fetša_ntlha 8개, 끝점당 전문 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class 되돌림망 {
    static int[] 사용 = new int[8];
    static int[] phote_boleng = new int[8];
    static int[] atrese = new int[8];
    static int[] 앞 = new int[8];
    static int[] 개수 = new int[8];
    static int[] 받은창구 = new int[8];
    static int[] botelele_boleng = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] data = new int[32 * 512];
    static int[] romela_pele_boleng = new int[512];
    static int 다음창구 = 49152;
    static int kgonthiša(int lokela) { return lokela >= 32 && lokela < 40 && 사용[lokela - 32] != 0 ? lokela - 32 : -1; }
    static boolean 겹침(int lokela) {
        for (int sekgobana_go_tsenya_tshedimošo = 0; sekgobana_go_tsenya_tshedimošo < 8; sekgobana_go_tsenya_tshedimošo++) if (사용[sekgobana_go_tsenya_tshedimošo] != 0 && phote_boleng[sekgobana_go_tsenya_tshedimošo] == lokela) return true;
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
    public static int 만들기(int 영역, int 종류, int taba_boleng) {
        if (영역 != 2) return -97;
        if (종류 != 2 || (taba_boleng != 0 && taba_boleng != 17)) return -93;
        for (int sekgobana_go_tsenya_tshedimošo = 0; sekgobana_go_tsenya_tshedimošo < 8; sekgobana_go_tsenya_tshedimošo++) if (사용[sekgobana_go_tsenya_tshedimošo] == 0) {
            사용[sekgobana_go_tsenya_tshedimošo] = 1; phote_boleng[sekgobana_go_tsenya_tshedimošo] = 0; atrese[sekgobana_go_tsenya_tshedimošo] = 0; 앞[sekgobana_go_tsenya_tshedimošo] = 0; 개수[sekgobana_go_tsenya_tshedimošo] = 0; 받은창구[sekgobana_go_tsenya_tshedimošo] = 0;
            return sekgobana_go_tsenya_tshedimošo + 32;
        }
        return -24;
    }
    public static int 묶기(int lokela, int Netweke_atrese, int 창구번호) {
        int sekgobana_go_tsenya_tshedimošo = kgonthiša(lokela);
        if (sekgobana_go_tsenya_tshedimošo < 0) return -9;
        if (Netweke_atrese != 0 && Netweke_atrese != 0x7f000001) return -99;
        if (phote_boleng[sekgobana_go_tsenya_tshedimošo] != 0 || 창구번호 < 0 || 창구번호 > 65535) return -22;
        if (창구번호 == 0) 창구번호 = 임시창구();
        if (창구번호 < 0) return 창구번호;
        if (겹침(창구번호)) return -98;
        phote_boleng[sekgobana_go_tsenya_tshedimošo] = 창구번호; atrese[sekgobana_go_tsenya_tshedimošo] = Netweke_atrese; return 0;
    }
    public static int 자료넣기(int lokela, int boleng) {
        if (lokela < 0 || lokela >= 512) return -22;
        romela_pele_boleng[lokela] = boleng & 255; return 0;
    }
    public static int 자료읽기(int lokela) { return lokela >= 0 && lokela < 512 ? romela_pele_boleng[lokela] : -22; }
    public static int Romela(int lokela, int Netweke_atrese, int 창구번호, int Bogolo) {
        int sekgobana_go_tsenya_tshedimošo = kgonthiša(lokela);
        if (sekgobana_go_tsenya_tshedimošo < 0) return -9;
        if (Netweke_atrese != 0x7f000001) return -101;
        if (창구번호 < 1 || 창구번호 > 65535) return -22;
        if (Bogolo < 0 || Bogolo > 512) return -90;
        if (phote_boleng[sekgobana_go_tsenya_tshedimošo] == 0) {
            int 결과 = 묶기(lokela, 0x7f000001, 0);
            if (결과 < 0) return 결과;
        }
        int boyo_boleng = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (사용[후보] != 0 && phote_boleng[후보] == 창구번호) boyo_boleng = 후보;
        if (boyo_boleng < 0) return -111;
        if (개수[boyo_boleng] == 4) return -11;
        int 자리 = boyo_boleng * 4 + (앞[boyo_boleng] + 개수[boyo_boleng]) % 4;
        for (int paete_boleng = 0; paete_boleng < Bogolo; paete_boleng++) data[자리 * 512 + paete_boleng] = romela_pele_boleng[paete_boleng];
        botelele_boleng[자리] = Bogolo; 보낸창구[자리] = phote_boleng[sekgobana_go_tsenya_tshedimošo]; 개수[boyo_boleng]++;
        return Bogolo;
    }
    public static int 받기(int lokela, int 용량) {
        int sekgobana_go_tsenya_tshedimošo = kgonthiša(lokela);
        if (sekgobana_go_tsenya_tshedimošo < 0) return -9;
        if (용량 < 0 || 용량 > 512) return -22;
        if (개수[sekgobana_go_tsenya_tshedimošo] == 0) return -11;
        int 자리 = sekgobana_go_tsenya_tshedimošo * 4 + 앞[sekgobana_go_tsenya_tshedimošo];
        int Bogolo = botelele_boleng[자리] < 용량 ? botelele_boleng[자리] : 용량;
        for (int paete_boleng = 0; paete_boleng < Bogolo; paete_boleng++) romela_pele_boleng[paete_boleng] = data[자리 * 512 + paete_boleng];
        받은창구[sekgobana_go_tsenya_tshedimošo] = 보낸창구[자리]; 앞[sekgobana_go_tsenya_tshedimošo] = (앞[sekgobana_go_tsenya_tshedimošo] + 1) % 4; 개수[sekgobana_go_tsenya_tshedimošo]--;
        return Bogolo;
    }
    public static int 창구읽기(int lokela) { int sekgobana_go_tsenya_tshedimošo = kgonthiša(lokela); return sekgobana_go_tsenya_tshedimošo < 0 ? -9 : phote_boleng[sekgobana_go_tsenya_tshedimošo]; }
    public static int 주소읽기(int lokela) { int sekgobana_go_tsenya_tshedimošo = kgonthiša(lokela); return sekgobana_go_tsenya_tshedimošo < 0 ? -9 : atrese[sekgobana_go_tsenya_tshedimošo]; }
    public static int 보낸곳(int lokela) { int sekgobana_go_tsenya_tshedimošo = kgonthiša(lokela); return sekgobana_go_tsenya_tshedimošo < 0 ? -9 : 받은창구[sekgobana_go_tsenya_tshedimošo]; }
    public static int Tswalela(int lokela) {
        int sekgobana_go_tsenya_tshedimošo = kgonthiša(lokela); if (sekgobana_go_tsenya_tshedimošo < 0) return -9;
        사용[sekgobana_go_tsenya_tshedimošo] = 0; 개수[sekgobana_go_tsenya_tshedimošo] = 0; phote_boleng[sekgobana_go_tsenya_tshedimošo] = 0; return 0;
    }
}
