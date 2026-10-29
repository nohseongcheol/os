// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 sheli hali_thamani. faili 저장소는 공유하고 njia/변수/batli_REKODI/입력은 분리한다. */
public final class dirisha_kipindi {
    static int[] 보관 = new int[4 * 30000], Andaa = new int[4];
    static int 현재, 위치;
    static boolean 이어읽기;
    static void ARRAY_thamani(int[] data, boolean Store_thamani) {
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < data.length; kitanzi_kielezo++) { if (Store_thamani) 보관[위치++] = data[kitanzi_kielezo]; else data[kitanzi_kielezo] = 보관[위치++]; }
    }
    static int thamani(int data_thamani, boolean 저장여부) { if (저장여부) { 보관[위치++] = data_thamani; return data_thamani; } return 보관[위치++]; }
    static void 옮기기(int 보관칸, boolean 저장여부) {
        위치 = 보관칸 * 30000;
        ARRAY_thamani(kumbukumbu_Faili.현재, 저장여부); kumbukumbu_Faili.현재길이 = thamani(kumbukumbu_Faili.현재길이, 저장여부);
        ARRAY_thamani(sheli_sintaksi.변수이름, 저장여부); ARRAY_thamani(sheli_sintaksi.변수값, 저장여부); ARRAY_thamani(sheli_sintaksi.이름길이, 저장여부); ARRAY_thamani(sheli_sintaksi.thamani_urefu, 저장여부);
        sheli_sintaksi.hali_thamani = thamani(sheli_sintaksi.hali_thamani, 저장여부);
        ARRAY_thamani(laini_Kihariri.batli_REKODI, 저장여부); ARRAY_thamani(laini_Kihariri.batli_urefu, 저장여부); ARRAY_thamani(laini_Kihariri.Store_thamani, 저장여부); ARRAY_thamani(명령해석기.laini, 저장여부);
        laini_Kihariri.기록수 = thamani(laini_Kihariri.기록수, 저장여부); laini_Kihariri.batli_REKODI_tamatia = thamani(laini_Kihariri.batli_REKODI_tamatia, 저장여부);
        laini_Kihariri.Duhusi_thamani = thamani(laini_Kihariri.Duhusi_thamani, 저장여부); laini_Kihariri.저장길이 = thamani(laini_Kihariri.저장길이, 저장여부);
        laini_Kihariri.panga_ukubwa = thamani(laini_Kihariri.panga_ukubwa, 저장여부); laini_Kihariri.kielekezi_thamani = thamani(laini_Kihariri.kielekezi_thamani, 저장여부); laini_Kihariri.Anza_dirisha = thamani(laini_Kihariri.Anza_dirisha, 저장여부);
        Andaa[보관칸] = 1;
    }
    static void Mchakato_thamani_ingizo() {
        int 사건번호 = 보드.터미널(12); if (사건번호 == 0) return;
        옮기기(현재, true);
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < 4; kitanzi_kielezo++) {
            if ((사건번호 & (1 << (8 + kitanzi_kielezo))) != 0) { 보드.udhibiti_mtumiaji_programu(32 + kitanzi_kielezo); Andaa[kitanzi_kielezo] = 0; }
            if ((사건번호 & (1 << (4 + kitanzi_kielezo))) != 0 && kitanzi_kielezo != 현재) Andaa[kitanzi_kielezo] = 0;
        }
        int 다음자리 = (사건번호 & 15) - 1; if (다음자리 < 0) 다음자리 = 0;
        if (Andaa[다음자리] == 0) for (int kitanzi_kielezo = 0; kitanzi_kielezo < 30000; kitanzi_kielezo++) 보관[다음자리 * 30000 + kitanzi_kielezo] = 0;
        현재 = 다음자리; 옮기기(현재, false); 보드.터미널(100 + 현재); 이어읽기 = true;
        단말.andika("\nTERMINAL FOCUS "); 단말.수(현재 + 1); 단말.문자(10);
    }
    static boolean 재개() {
        if (보드.udhibiti_mtumiaji_programu(16 + 현재) == 0) return false;
        셸입출력.Ruhusu_ingiliani = true; 셸입출력.endesha(false, false); 보드.입출력전환(1);
        int 처리값 = 보드.udhibiti_mtumiaji_programu(현재); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; sheli_sintaksi.hali_thamani = 처리값 < 0 ? 126 : 처리값; 단말.andika("exit "); 단말.수(처리값); 단말.문자(10); 보드.터미널(3); }
        return true;
    }
}
