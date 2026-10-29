// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 Wëreef nekkin_xëyma. bara_denc 저장소는 공유하고 Yoonu_jëmale/변수/làq_Dënk/입력은 분리한다. */
public final class palanteer_lël {
    static int[] 보관 = new int[4 * 30000], jël_matuwaay = new int[4];
    static int 현재, 위치;
    static boolean 이어읽기;
    static void TABLO_xëyma(int[] mbir, boolean Store_xëyma) {
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < mbir.length; wërngël_àlluwa_tur++) { if (Store_xëyma) 보관[위치++] = mbir[wërngël_àlluwa_tur]; else mbir[wërngël_àlluwa_tur] = 보관[위치++]; }
    }
    static int xëyma(int mbir_xëyma, boolean 저장여부) { if (저장여부) { 보관[위치++] = mbir_xëyma; return mbir_xëyma; } return 보관[위치++]; }
    static void 옮기기(int 보관칸, boolean 저장여부) {
        위치 = 보관칸 * 30000;
        TABLO_xëyma(fatlekookaay_Fisiye_yi.현재, 저장여부); fatlekookaay_Fisiye_yi.현재길이 = xëyma(fatlekookaay_Fisiye_yi.현재길이, 저장여부);
        TABLO_xëyma(Wëreef_tëgg_waxin.변수이름, 저장여부); TABLO_xëyma(Wëreef_tëgg_waxin.변수값, 저장여부); TABLO_xëyma(Wëreef_tëgg_waxin.이름길이, 저장여부); TABLO_xëyma(Wëreef_tëgg_waxin.xëyma_diir, 저장여부);
        Wëreef_tëgg_waxin.nekkin_xëyma = xëyma(Wëreef_tëgg_waxin.nekkin_xëyma, 저장여부);
        TABLO_xëyma(buum_defarkat.làq_Dënk, 저장여부); TABLO_xëyma(buum_defarkat.làq_diir, 저장여부); TABLO_xëyma(buum_defarkat.Store_xëyma, 저장여부); TABLO_xëyma(명령해석기.buum, 저장여부);
        buum_defarkat.기록수 = xëyma(buum_defarkat.기록수, 저장여부); buum_defarkat.làq_Dënk_jeexal = xëyma(buum_defarkat.làq_Dënk_jeexal, 저장여부);
        buum_defarkat.Wut_xëyma = xëyma(buum_defarkat.Wut_xëyma, 저장여부); buum_defarkat.저장길이 = xëyma(buum_defarkat.저장길이, 저장여부);
        buum_defarkat.tolluwaay = xëyma(buum_defarkat.tolluwaay, 저장여부); buum_defarkat.barab_bees_mën_a_bind_xëyma = xëyma(buum_defarkat.barab_bees_mën_a_bind_xëyma, 저장여부); buum_defarkat.Door_palanteer = xëyma(buum_defarkat.Door_palanteer, 저장여부);
        jël_matuwaay[보관칸] = 1;
    }
    static void yokkute_xëyma_dugal_xabaar() {
        int 사건번호 = 보드.터미널(12); if (사건번호 == 0) return;
        옮기기(현재, true);
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 4; wërngël_àlluwa_tur++) {
            if ((사건번호 & (1 << (8 + wërngël_àlluwa_tur))) != 0) { 보드.Saytu_doxinu_ordinateur_kiy_jariñoo_internet_jëfekaay(32 + wërngël_àlluwa_tur); jël_matuwaay[wërngël_àlluwa_tur] = 0; }
            if ((사건번호 & (1 << (4 + wërngël_àlluwa_tur))) != 0 && wërngël_àlluwa_tur != 현재) jël_matuwaay[wërngël_àlluwa_tur] = 0;
        }
        int 다음자리 = (사건번호 & 15) - 1; if (다음자리 < 0) 다음자리 = 0;
        if (jël_matuwaay[다음자리] == 0) for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 30000; wërngël_àlluwa_tur++) 보관[다음자리 * 30000 + wërngël_àlluwa_tur] = 0;
        현재 = 다음자리; 옮기기(현재, false); 보드.터미널(100 + 현재); 이어읽기 = true;
        단말.biir("\nTERMINAL FOCUS "); 단말.수(현재 + 1); 단말.문자(10);
    }
    static boolean 재개() {
        if (보드.Saytu_doxinu_ordinateur_kiy_jariñoo_internet_jëfekaay(16 + 현재) == 0) return false;
        셸입출력.Maye_duglante = true; 셸입출력.daw(false, false); 보드.입출력전환(1);
        int 처리값 = 보드.Saytu_doxinu_ordinateur_kiy_jariñoo_internet_jëfekaay(현재); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; Wëreef_tëgg_waxin.nekkin_xëyma = 처리값 < 0 ? 126 : 처리값; 단말.biir("exit "); 단말.수(처리값); 단말.문자(10); 보드.터미널(3); }
        return true;
    }
}
