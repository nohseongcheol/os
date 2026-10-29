// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 ileya_ixabiso: 단일 ikheneli_ixabiso 안의 IPv4/UDP 루프백 gqithisela_ixabiso.
 * 외부 IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * phela_inqaku 8개, 끝점당 전문 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class 되돌림망 {
    static int[] 사용 = new int[8];
    static int[] iphothi_ixabiso = new int[8];
    static int[] idilesi = new int[8];
    static int[] 앞 = new int[8];
    static int[] 개수 = new int[8];
    static int[] 받은창구 = new int[8];
    static int[] ubude_ixabiso = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] iingcombolo = new int[32 * 512];
    static int[] dlulisa_ixabiso = new int[512];
    static int 다음창구 = 49152;
    static int ngqinisisa(int indeksa) { return indeksa >= 32 && indeksa < 40 && 사용[indeksa - 32] != 0 ? indeksa - 32 : -1; }
    static boolean 겹침(int indeksa) {
        for (int isithuba_ufako_nkcukacha = 0; isithuba_ufako_nkcukacha < 8; isithuba_ufako_nkcukacha++) if (사용[isithuba_ufako_nkcukacha] != 0 && iphothi_ixabiso[isithuba_ufako_nkcukacha] == indeksa) return true;
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
    public static int yila_ufako_nkcukacha(int 영역, int 종류, int isiganeko_ixabiso) {
        if (영역 != 2) return -97;
        if (종류 != 2 || (isiganeko_ixabiso != 0 && isiganeko_ixabiso != 17)) return -93;
        for (int isithuba_ufako_nkcukacha = 0; isithuba_ufako_nkcukacha < 8; isithuba_ufako_nkcukacha++) if (사용[isithuba_ufako_nkcukacha] == 0) {
            사용[isithuba_ufako_nkcukacha] = 1; iphothi_ixabiso[isithuba_ufako_nkcukacha] = 0; idilesi[isithuba_ufako_nkcukacha] = 0; 앞[isithuba_ufako_nkcukacha] = 0; 개수[isithuba_ufako_nkcukacha] = 0; 받은창구[isithuba_ufako_nkcukacha] = 0;
            return isithuba_ufako_nkcukacha + 32;
        }
        return -24;
    }
    public static int 묶기(int indeksa, int Inethiwekhi_idilesi, int 창구번호) {
        int isithuba_ufako_nkcukacha = ngqinisisa(indeksa);
        if (isithuba_ufako_nkcukacha < 0) return -9;
        if (Inethiwekhi_idilesi != 0 && Inethiwekhi_idilesi != 0x7f000001) return -99;
        if (iphothi_ixabiso[isithuba_ufako_nkcukacha] != 0 || 창구번호 < 0 || 창구번호 > 65535) return -22;
        if (창구번호 == 0) 창구번호 = 임시창구();
        if (창구번호 < 0) return 창구번호;
        if (겹침(창구번호)) return -98;
        iphothi_ixabiso[isithuba_ufako_nkcukacha] = 창구번호; idilesi[isithuba_ufako_nkcukacha] = Inethiwekhi_idilesi; return 0;
    }
    public static int 자료넣기(int indeksa, int ixabiso) {
        if (indeksa < 0 || indeksa >= 512) return -22;
        dlulisa_ixabiso[indeksa] = ixabiso & 255; return 0;
    }
    public static int 자료읽기(int indeksa) { return indeksa >= 0 && indeksa < 512 ? dlulisa_ixabiso[indeksa] : -22; }
    public static int thumela(int indeksa, int Inethiwekhi_idilesi, int 창구번호, int Ubukhulu) {
        int isithuba_ufako_nkcukacha = ngqinisisa(indeksa);
        if (isithuba_ufako_nkcukacha < 0) return -9;
        if (Inethiwekhi_idilesi != 0x7f000001) return -101;
        if (창구번호 < 1 || 창구번호 > 65535) return -22;
        if (Ubukhulu < 0 || Ubukhulu > 512) return -90;
        if (iphothi_ixabiso[isithuba_ufako_nkcukacha] == 0) {
            int 결과 = 묶기(indeksa, 0x7f000001, 0);
            if (결과 < 0) return 결과;
        }
        int indawo_ekuyiwa_kuyo_ixabiso = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (사용[후보] != 0 && iphothi_ixabiso[후보] == 창구번호) indawo_ekuyiwa_kuyo_ixabiso = 후보;
        if (indawo_ekuyiwa_kuyo_ixabiso < 0) return -111;
        if (개수[indawo_ekuyiwa_kuyo_ixabiso] == 4) return -11;
        int 자리 = indawo_ekuyiwa_kuyo_ixabiso * 4 + (앞[indawo_ekuyiwa_kuyo_ixabiso] + 개수[indawo_ekuyiwa_kuyo_ixabiso]) % 4;
        for (int ibhayithi_ixabiso = 0; ibhayithi_ixabiso < Ubukhulu; ibhayithi_ixabiso++) iingcombolo[자리 * 512 + ibhayithi_ixabiso] = dlulisa_ixabiso[ibhayithi_ixabiso];
        ubude_ixabiso[자리] = Ubukhulu; 보낸창구[자리] = iphothi_ixabiso[isithuba_ufako_nkcukacha]; 개수[indawo_ekuyiwa_kuyo_ixabiso]++;
        return Ubukhulu;
    }
    public static int 받기(int indeksa, int 용량) {
        int isithuba_ufako_nkcukacha = ngqinisisa(indeksa);
        if (isithuba_ufako_nkcukacha < 0) return -9;
        if (용량 < 0 || 용량 > 512) return -22;
        if (개수[isithuba_ufako_nkcukacha] == 0) return -11;
        int 자리 = isithuba_ufako_nkcukacha * 4 + 앞[isithuba_ufako_nkcukacha];
        int Ubukhulu = ubude_ixabiso[자리] < 용량 ? ubude_ixabiso[자리] : 용량;
        for (int ibhayithi_ixabiso = 0; ibhayithi_ixabiso < Ubukhulu; ibhayithi_ixabiso++) dlulisa_ixabiso[ibhayithi_ixabiso] = iingcombolo[자리 * 512 + ibhayithi_ixabiso];
        받은창구[isithuba_ufako_nkcukacha] = 보낸창구[자리]; 앞[isithuba_ufako_nkcukacha] = (앞[isithuba_ufako_nkcukacha] + 1) % 4; 개수[isithuba_ufako_nkcukacha]--;
        return Ubukhulu;
    }
    public static int 창구읽기(int indeksa) { int isithuba_ufako_nkcukacha = ngqinisisa(indeksa); return isithuba_ufako_nkcukacha < 0 ? -9 : iphothi_ixabiso[isithuba_ufako_nkcukacha]; }
    public static int 주소읽기(int indeksa) { int isithuba_ufako_nkcukacha = ngqinisisa(indeksa); return isithuba_ufako_nkcukacha < 0 ? -9 : idilesi[isithuba_ufako_nkcukacha]; }
    public static int 보낸곳(int indeksa) { int isithuba_ufako_nkcukacha = ngqinisisa(indeksa); return isithuba_ufako_nkcukacha < 0 ? -9 : 받은창구[isithuba_ufako_nkcukacha]; }
    public static int Vala(int indeksa) {
        int isithuba_ufako_nkcukacha = ngqinisisa(indeksa); if (isithuba_ufako_nkcukacha < 0) return -9;
        사용[isithuba_ufako_nkcukacha] = 0; 개수[isithuba_ufako_nkcukacha] = 0; iphothi_ixabiso[isithuba_ufako_nkcukacha] = 0; return 0;
    }
}
