// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 akugara_agaciro: 단일 intima_agaciro 안의 IPv4/UDP 루프백 iyimura_agaciro.
 * 외부 IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * kurangiza_inota 8개, 끝점당 전문 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class 되돌림망 {
    static int[] 사용 = new int[8];
    static int[] poti_agaciro = new int[8];
    static int[] aderesi = new int[8];
    static int[] 앞 = new int[8];
    static int[] 개수 = new int[8];
    static int[] 받은창구 = new int[8];
    static int[] uburebure_agaciro = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] amakurushingiro = new int[32 * 512];
    static int[] koherereza_agaciro = new int[512];
    static int 다음창구 = 49152;
    static int gusuzuma(int umugerekashakiro) { return umugerekashakiro >= 32 && umugerekashakiro < 40 && 사용[umugerekashakiro - 32] != 0 ? umugerekashakiro - 32 : -1; }
    static boolean 겹침(int umugerekashakiro) {
        for (int umwanya_icyinjizwa = 0; umwanya_icyinjizwa < 8; umwanya_icyinjizwa++) if (사용[umwanya_icyinjizwa] != 0 && poti_agaciro[umwanya_icyinjizwa] == umugerekashakiro) return true;
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
    public static int kurema_icyinjizwa(int 영역, int 종류, int ikibazo_agaciro) {
        if (영역 != 2) return -97;
        if (종류 != 2 || (ikibazo_agaciro != 0 && ikibazo_agaciro != 17)) return -93;
        for (int umwanya_icyinjizwa = 0; umwanya_icyinjizwa < 8; umwanya_icyinjizwa++) if (사용[umwanya_icyinjizwa] == 0) {
            사용[umwanya_icyinjizwa] = 1; poti_agaciro[umwanya_icyinjizwa] = 0; aderesi[umwanya_icyinjizwa] = 0; 앞[umwanya_icyinjizwa] = 0; 개수[umwanya_icyinjizwa] = 0; 받은창구[umwanya_icyinjizwa] = 0;
            return umwanya_icyinjizwa + 32;
        }
        return -24;
    }
    public static int 묶기(int umugerekashakiro, int Urusobemiyoboro_aderesi, int 창구번호) {
        int umwanya_icyinjizwa = gusuzuma(umugerekashakiro);
        if (umwanya_icyinjizwa < 0) return -9;
        if (Urusobemiyoboro_aderesi != 0 && Urusobemiyoboro_aderesi != 0x7f000001) return -99;
        if (poti_agaciro[umwanya_icyinjizwa] != 0 || 창구번호 < 0 || 창구번호 > 65535) return -22;
        if (창구번호 == 0) 창구번호 = 임시창구();
        if (창구번호 < 0) return 창구번호;
        if (겹침(창구번호)) return -98;
        poti_agaciro[umwanya_icyinjizwa] = 창구번호; aderesi[umwanya_icyinjizwa] = Urusobemiyoboro_aderesi; return 0;
    }
    public static int 자료넣기(int umugerekashakiro, int agaciro) {
        if (umugerekashakiro < 0 || umugerekashakiro >= 512) return -22;
        koherereza_agaciro[umugerekashakiro] = agaciro & 255; return 0;
    }
    public static int 자료읽기(int umugerekashakiro) { return umugerekashakiro >= 0 && umugerekashakiro < 512 ? koherereza_agaciro[umugerekashakiro] : -22; }
    public static int kohereza(int umugerekashakiro, int Urusobemiyoboro_aderesi, int 창구번호, int Ingano) {
        int umwanya_icyinjizwa = gusuzuma(umugerekashakiro);
        if (umwanya_icyinjizwa < 0) return -9;
        if (Urusobemiyoboro_aderesi != 0x7f000001) return -101;
        if (창구번호 < 1 || 창구번호 > 65535) return -22;
        if (Ingano < 0 || Ingano > 512) return -90;
        if (poti_agaciro[umwanya_icyinjizwa] == 0) {
            int 결과 = 묶기(umugerekashakiro, 0x7f000001, 0);
            if (결과 < 0) return 결과;
        }
        int aho_ijya_agaciro = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (사용[후보] != 0 && poti_agaciro[후보] == 창구번호) aho_ijya_agaciro = 후보;
        if (aho_ijya_agaciro < 0) return -111;
        if (개수[aho_ijya_agaciro] == 4) return -11;
        int 자리 = aho_ijya_agaciro * 4 + (앞[aho_ijya_agaciro] + 개수[aho_ijya_agaciro]) % 4;
        for (int bayiti_agaciro = 0; bayiti_agaciro < Ingano; bayiti_agaciro++) amakurushingiro[자리 * 512 + bayiti_agaciro] = koherereza_agaciro[bayiti_agaciro];
        uburebure_agaciro[자리] = Ingano; 보낸창구[자리] = poti_agaciro[umwanya_icyinjizwa]; 개수[aho_ijya_agaciro]++;
        return Ingano;
    }
    public static int 받기(int umugerekashakiro, int 용량) {
        int umwanya_icyinjizwa = gusuzuma(umugerekashakiro);
        if (umwanya_icyinjizwa < 0) return -9;
        if (용량 < 0 || 용량 > 512) return -22;
        if (개수[umwanya_icyinjizwa] == 0) return -11;
        int 자리 = umwanya_icyinjizwa * 4 + 앞[umwanya_icyinjizwa];
        int Ingano = uburebure_agaciro[자리] < 용량 ? uburebure_agaciro[자리] : 용량;
        for (int bayiti_agaciro = 0; bayiti_agaciro < Ingano; bayiti_agaciro++) koherereza_agaciro[bayiti_agaciro] = amakurushingiro[자리 * 512 + bayiti_agaciro];
        받은창구[umwanya_icyinjizwa] = 보낸창구[자리]; 앞[umwanya_icyinjizwa] = (앞[umwanya_icyinjizwa] + 1) % 4; 개수[umwanya_icyinjizwa]--;
        return Ingano;
    }
    public static int 창구읽기(int umugerekashakiro) { int umwanya_icyinjizwa = gusuzuma(umugerekashakiro); return umwanya_icyinjizwa < 0 ? -9 : poti_agaciro[umwanya_icyinjizwa]; }
    public static int 주소읽기(int umugerekashakiro) { int umwanya_icyinjizwa = gusuzuma(umugerekashakiro); return umwanya_icyinjizwa < 0 ? -9 : aderesi[umwanya_icyinjizwa]; }
    public static int 보낸곳(int umugerekashakiro) { int umwanya_icyinjizwa = gusuzuma(umugerekashakiro); return umwanya_icyinjizwa < 0 ? -9 : 받은창구[umwanya_icyinjizwa]; }
    public static int Gufunga(int umugerekashakiro) {
        int umwanya_icyinjizwa = gusuzuma(umugerekashakiro); if (umwanya_icyinjizwa < 0) return -9;
        사용[umwanya_icyinjizwa] = 0; 개수[umwanya_icyinjizwa] = 0; poti_agaciro[umwanya_icyinjizwa] = 0; return 0;
    }
}
