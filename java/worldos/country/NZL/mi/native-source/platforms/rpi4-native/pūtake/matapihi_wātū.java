// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 anga tūnga_uara. Kōnae 저장소는 공유하고 ara/변수/LOG_RECORD/입력은 분리한다. */
public final class matapihi_wātū {
    static int[] 보관 = new int[4 * 30000], Whakarite = new int[4];
    static int 현재, tūranga;
    static boolean 이어읽기;
    static void HUĀNGA_uara(int[] raraunga, boolean Store_uara) {
        for (int Loop_INDEX = 0; Loop_INDEX < raraunga.length; Loop_INDEX++) { if (Store_uara) 보관[tūranga++] = raraunga[Loop_INDEX]; else raraunga[Loop_INDEX] = 보관[tūranga++]; }
    }
    static int uara(int raraunga_uara, boolean 저장여부) { if (저장여부) { 보관[tūranga++] = raraunga_uara; return raraunga_uara; } return 보관[tūranga++]; }
    static void kimi_tūranga(int 보관칸, boolean 저장여부) {
        tūranga = 보관칸 * 30000;
        HUĀNGA_uara(Pūmahara_Ngā_Kōnae.현재, 저장여부); Pūmahara_Ngā_Kōnae.현재길이 = uara(Pūmahara_Ngā_Kōnae.현재길이, 저장여부);
        HUĀNGA_uara(anga_wetereo.변수이름, 저장여부); HUĀNGA_uara(anga_wetereo.변수값, 저장여부); HUĀNGA_uara(anga_wetereo.이름길이, 저장여부); HUĀNGA_uara(anga_wetereo.uara_roa, 저장여부);
        anga_wetereo.tūnga_uara = uara(anga_wetereo.tūnga_uara, 저장여부);
        HUĀNGA_uara(hononga_Pūwhakatika.LOG_RECORD, 저장여부); HUĀNGA_uara(hononga_Pūwhakatika.LOG_roa, 저장여부); HUĀNGA_uara(hononga_Pūwhakatika.Store_uara, 저장여부); HUĀNGA_uara(명령해석기.hononga, 저장여부);
        hononga_Pūwhakatika.LOG_COUNT = uara(hononga_Pūwhakatika.LOG_COUNT, 저장여부); hononga_Pūwhakatika.LOG_RECORD_mutu = uara(hononga_Pūwhakatika.LOG_RECORD_mutu, 저장여부);
        hononga_Pūwhakatika.Rapu_uara = uara(hononga_Pūwhakatika.Rapu_uara, 저장여부); hononga_Pūwhakatika.저장길이 = uara(hononga_Pūwhakatika.저장길이, 저장여부);
        hononga_Pūwhakatika.rahi = uara(hononga_Pūwhakatika.rahi, 저장여부); hononga_Pūwhakatika.pehu_uara = uara(hononga_Pūwhakatika.pehu_uara, 저장여부); hononga_Pūwhakatika.Start_matapihi = uara(hononga_Pūwhakatika.Start_matapihi, 저장여부);
        Whakarite[보관칸] = 1;
    }
    static void Hātepe_uara_tāurunga() {
        int 사건번호 = papa.Tauranga(12); if (사건번호 == 0) return;
        kimi_tūranga(현재, true);
        for (int Loop_INDEX = 0; Loop_INDEX < 4; Loop_INDEX++) {
            if ((사건번호 & (1 << (8 + Loop_INDEX))) != 0) { papa.mana_kaiwhakamahi_kaupapa(32 + Loop_INDEX); Whakarite[Loop_INDEX] = 0; }
            if ((사건번호 & (1 << (4 + Loop_INDEX))) != 0 && Loop_INDEX != 현재) Whakarite[Loop_INDEX] = 0;
        }
        int Panuku_tūranga = (사건번호 & 15) - 1; if (Panuku_tūranga < 0) Panuku_tūranga = 0;
        if (Whakarite[Panuku_tūranga] == 0) for (int Loop_INDEX = 0; Loop_INDEX < 30000; Loop_INDEX++) 보관[Panuku_tūranga * 30000 + Loop_INDEX] = 0;
        현재 = Panuku_tūranga; kimi_tūranga(현재, false); papa.Tauranga(100 + 현재); 이어읽기 = true;
        단말.Tuhia("\nTERMINAL FOCUS "); 단말.수(현재 + 1); 단말.문자(10);
    }
    static boolean 재개() {
        if (papa.mana_kaiwhakamahi_kaupapa(16 + 현재) == 0) return false;
        셸입출력.Tuku_pāhekoheko = true; 셸입출력.whakahaere(false, false); papa.입출력전환(1);
        int 처리값 = papa.mana_kaiwhakamahi_kaupapa(현재); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; anga_wetereo.tūnga_uara = 처리값 < 0 ? 126 : 처리값; 단말.Tuhia("exit "); 단말.수(처리값); 단말.문자(10); papa.Tauranga(3); }
        return true;
    }
}
