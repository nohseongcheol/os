// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 aluwataalapu_u jamakua_iparülein_ajutuu. anaajaalaa 저장소는 공유하고 wopu_a_ttaaleemüin/변수/aa_innachikimaajatü_aparatsee/입력은 분리한다. */
public final class analaaya_a_ttawo_ulu {
    static int[] 보관 = new int[4 * 30000], 준비 = new int[4];
    static int 현재, 위치;
    static boolean 이어읽기;
    static void matüriisü_ajutuu(int[] atijaaya, boolean 저장) {
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < atijaaya.length; eitawaakualü_ee_iyatialujuna++) { if (저장) 보관[위치++] = atijaaya[eitawaakualü_ee_iyatialujuna]; else atijaaya[eitawaakualü_ee_iyatialujuna] = 보관[위치++]; }
    }
    static int ajutuu(int atijaaya_ajutuu, boolean 저장여부) { if (저장여부) { 보관[위치++] = atijaaya_ajutuu; return atijaaya_ajutuu; } return 보관[위치++]; }
    static void 옮기기(int 보관칸, boolean 저장여부) {
        위치 = 보관칸 * 30000;
        matüriisü_ajutuu(기억파일.현재, 저장여부); 기억파일.현재길이 = ajutuu(기억파일.현재길이, 저장여부);
        matüriisü_ajutuu(aluwataalapu_u_anaatashajia.변수이름, 저장여부); matüriisü_ajutuu(aluwataalapu_u_anaatashajia.변수값, 저장여부); matüriisü_ajutuu(aluwataalapu_u_anaatashajia.이름길이, 저장여부); matüriisü_ajutuu(aluwataalapu_u_anaatashajia.ajutuu_akaliaa, 저장여부);
        aluwataalapu_u_anaatashajia.jamakua_iparülein_ajutuu = ajutuu(aluwataalapu_u_anaatashajia.jamakua_iparülein_ajutuu, 저장여부);
        matüriisü_ajutuu(liinia_anaatülü.aa_innachikimaajatü_aparatsee, 저장여부); matüriisü_ajutuu(liinia_anaatülü.aa_innachikimaajatü_akaliaa, 저장여부); matüriisü_ajutuu(liinia_anaatülü.저장, 저장여부); matüriisü_ajutuu(명령해석기.liinia, 저장여부);
        liinia_anaatülü.기록수 = ajutuu(liinia_anaatülü.기록수, 저장여부); liinia_anaatülü.aa_innachikimaajatü_aparatsee_ajattiraa = ajutuu(liinia_anaatülü.aa_innachikimaajatü_aparatsee_ajattiraa, 저장여부);
        liinia_anaatülü.Achajaaya_ajutuu = ajutuu(liinia_anaatülü.Achajaaya_ajutuu, 저장여부); liinia_anaatülü.저장길이 = ajutuu(liinia_anaatülü.저장길이, 저장여부);
        liinia_anaatülü.크기 = ajutuu(liinia_anaatülü.크기, 저장여부); liinia_anaatülü.ee_iyatiaa_ajutuu = ajutuu(liinia_anaatülü.ee_iyatiaa_ajutuu, 저장여부); liinia_anaatülü.achuwalaa_analaaya = ajutuu(liinia_anaatülü.achuwalaa_analaaya, 저장여부);
        준비[보관칸] = 1;
    }
    static void 처리() {
        int 사건번호 = 보드.터미널(12); if (사건번호 == 0) return;
        옮기기(현재, true);
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 4; eitawaakualü_ee_iyatialujuna++) {
            if ((사건번호 & (1 << (8 + eitawaakualü_ee_iyatialujuna))) != 0) { 보드.aa_inmajia_ka_yataayakalü_akumajiaa(32 + eitawaakualü_ee_iyatialujuna); 준비[eitawaakualü_ee_iyatialujuna] = 0; }
            if ((사건번호 & (1 << (4 + eitawaakualü_ee_iyatialujuna))) != 0 && eitawaakualü_ee_iyatialujuna != 현재) 준비[eitawaakualü_ee_iyatialujuna] = 0;
        }
        int 다음자리 = (사건번호 & 15) - 1; if (다음자리 < 0) 다음자리 = 0;
        if (준비[다음자리] == 0) for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 30000; eitawaakualü_ee_iyatialujuna++) 보관[다음자리 * 30000 + eitawaakualü_ee_iyatialujuna] = 0;
        현재 = 다음자리; 옮기기(현재, false); 보드.터미널(100 + 현재); 이어읽기 = true;
        단말.ashajaa("\nTERMINAL FOCUS "); 단말.수(현재 + 1); 단말.문자(10);
    }
    static boolean 재개() {
        if (보드.aa_inmajia_ka_yataayakalü_akumajiaa(16 + 현재) == 0) return false;
        셸입출력.A_tte_eraa_atütüjiraaya = true; 셸입출력.시작(false, false); 보드.입출력전환(1);
        int 처리값 = 보드.aa_inmajia_ka_yataayakalü_akumajiaa(현재); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; aluwataalapu_u_anaatashajia.jamakua_iparülein_ajutuu = 처리값 < 0 ? 126 : 처리값; 단말.ashajaa("exit "); 단말.수(처리값); 단말.문자(10); 보드.터미널(3); }
        return true;
    }
}
