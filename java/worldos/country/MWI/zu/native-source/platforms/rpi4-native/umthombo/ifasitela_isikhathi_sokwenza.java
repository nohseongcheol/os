// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 isihumushi_miyalelo isimo_inani. Ihele 저장소는 공유하고 Indlela_2/변수/loga_umugqa/입력은 분리한다. */
public final class ifasitela_isikhathi_sokwenza {
    static int[] 보관 = new int[4 * 30000], Hlela = new int[4];
    static int 현재, 위치;
    static boolean 이어읽기;
    static void AMALUNGU_AFANAYO_inani(int[] imininingwane, boolean Store_inani) {
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < imininingwane.length; iluphu_thola_inkomba++) { if (Store_inani) 보관[위치++] = imininingwane[iluphu_thola_inkomba]; else imininingwane[iluphu_thola_inkomba] = 보관[위치++]; }
    }
    static int inani(int imininingwane_inani, boolean 저장여부) { if (저장여부) { 보관[위치++] = imininingwane_inani; return imininingwane_inani; } return 보관[위치++]; }
    static void 옮기기(int 보관칸, boolean 저장여부) {
        위치 = 보관칸 * 30000;
        AMALUNGU_AFANAYO_inani(inkumbulo_Amafayela.현재, 저장여부); inkumbulo_Amafayela.현재길이 = inani(inkumbulo_Amafayela.현재길이, 저장여부);
        AMALUNGU_AFANAYO_inani(isihumushi_miyalelo_uhlelo_miyalelo.변수이름, 저장여부); AMALUNGU_AFANAYO_inani(isihumushi_miyalelo_uhlelo_miyalelo.변수값, 저장여부); AMALUNGU_AFANAYO_inani(isihumushi_miyalelo_uhlelo_miyalelo.이름길이, 저장여부); AMALUNGU_AFANAYO_inani(isihumushi_miyalelo_uhlelo_miyalelo.inani_ubude, 저장여부);
        isihumushi_miyalelo_uhlelo_miyalelo.isimo_inani = inani(isihumushi_miyalelo_uhlelo_miyalelo.isimo_inani, 저장여부);
        AMALUNGU_AFANAYO_inani(umugqa_Umhleli.loga_umugqa, 저장여부); AMALUNGU_AFANAYO_inani(umugqa_Umhleli.loga_ubude, 저장여부); AMALUNGU_AFANAYO_inani(umugqa_Umhleli.Store_inani, 저장여부); AMALUNGU_AFANAYO_inani(명령해석기.umugqa, 저장여부);
        umugqa_Umhleli.기록수 = inani(umugqa_Umhleli.기록수, 저장여부); umugqa_Umhleli.loga_umugqa_yekisa = inani(umugqa_Umhleli.loga_umugqa_yekisa, 저장여부);
        umugqa_Umhleli.Bheka_inani = inani(umugqa_Umhleli.Bheka_inani, 저장여부); umugqa_Umhleli.저장길이 = inani(umugqa_Umhleli.저장길이, 저장여부);
        umugqa_Umhleli.Ubungako = inani(umugqa_Umhleli.Ubungako, 저장여부); umugqa_Umhleli.isikhombisi_inani = inani(umugqa_Umhleli.isikhombisi_inani, 저장여부); umugqa_Umhleli.qala_ifasitela = inani(umugqa_Umhleli.qala_ifasitela, 저장여부);
        Hlela[보관칸] = 1;
    }
    static void Inqubo_inani_okufakwayo() {
        int 사건번호 = 보드.터미널(12); if (사건번호 == 0) return;
        옮기기(현재, true);
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 4; iluphu_thola_inkomba++) {
            if ((사건번호 & (1 << (8 + iluphu_thola_inkomba))) != 0) { 보드.isilawuli_umsebenzisi_i_app(32 + iluphu_thola_inkomba); Hlela[iluphu_thola_inkomba] = 0; }
            if ((사건번호 & (1 << (4 + iluphu_thola_inkomba))) != 0 && iluphu_thola_inkomba != 현재) Hlela[iluphu_thola_inkomba] = 0;
        }
        int 다음자리 = (사건번호 & 15) - 1; if (다음자리 < 0) 다음자리 = 0;
        if (Hlela[다음자리] == 0) for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 30000; iluphu_thola_inkomba++) 보관[다음자리 * 30000 + iluphu_thola_inkomba] = 0;
        현재 = 다음자리; 옮기기(현재, false); 보드.터미널(100 + 현재); 이어읽기 = true;
        단말.Bhala("\nTERMINAL FOCUS "); 단말.수(현재 + 1); 단말.문자(10);
    }
    static boolean 재개() {
        if (보드.isilawuli_umsebenzisi_i_app(16 + 현재) == 0) return false;
        셸입출력.vumela_ingxoxo_nekhompiyutha = true; 셸입출력.Sebenzisa(false, false); 보드.입출력전환(1);
        int 처리값 = 보드.isilawuli_umsebenzisi_i_app(현재); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; isihumushi_miyalelo_uhlelo_miyalelo.isimo_inani = 처리값 < 0 ? 126 : 처리값; 단말.Bhala("exit "); 단말.수(처리값); 단말.문자(10); 보드.터미널(3); }
        return true;
    }
}
