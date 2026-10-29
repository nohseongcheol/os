// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 qobiq 내장 Vositalar. */
public final class qobiq_Vositalar {
    static int[] ma_lumotlar = new int[16384];
    static int 입력파일 = -1;
    static int ochmoq_fayl(int dalil_INDEX, int Jarayon_MODE) {
        int 처리값 = 명령해석기.yo_l(dalil_INDEX); return 처리값 < 0 ? 처리값 : Xotira_Fayllar.Ochish(Jarayon_MODE);
    }
    static boolean 입력준비(int dalil_INDEX) {
        입력파일 = -1;
        if (dalil_INDEX < 명령해석기.token_COUNT) {
            입력파일 = ochmoq_fayl(dalil_INDEX, 0);
            if (입력파일 < 0) { 명령해석기.Xato(입력파일); return false; }
        }
        return true;
    }
    static int Oʻqish() {
        if (입력파일 >= 3) return Xotira_Fayllar.Oʻqish(입력파일);
        while (true) {
            int bayt_ma_lumotlar = yozuv_taxtasi.직렬읽기(); if (bayt_ma_lumotlar == -2 || bayt_ma_lumotlar == 4) return 256;
            if (bayt_ma_lumotlar == 3) { 명령해석기.o_lchov = 130; return 256; }
            if (bayt_ma_lumotlar >= 0) return bayt_ma_lumotlar; yozuv_taxtasi.YIELD_CPU();
        }
    }
    static void Yopish() { if (입력파일 >= 3) Xotira_Fayllar.Yopish(입력파일); 입력파일 = -1; }
    static void ko_rinish_VALUE() {
        int 마지막자리 = 명령해석기.token_COUNT == 1 ? 2 : 명령해석기.token_COUNT;
        for (int dalil_INDEX = 1; dalil_INDEX < 마지막자리; dalil_INDEX++) {
            if (!입력준비(dalil_INDEX)) continue;
            int bayt_ma_lumotlar; while ((bayt_ma_lumotlar = Oʻqish()) != 256 && bayt_ma_lumotlar >= 0) yozuv_taxtasi.직렬쓰기(bayt_ma_lumotlar);
            if (bayt_ma_lumotlar < 0) 명령해석기.Xato(bayt_ma_lumotlar); Yopish();
        }
    }
    static void fayl_ish(String 동작번호) {
        if (명령해석기.token_COUNT != 2) { 명령해석기.o_lchov = 2; 단말.Yozish("사용법: mkdir/rmdir/touch Fayl\n"); return; }
        int 처리값 = 명령해석기.yo_l(1);
        if (처리값 >= 0) {
            if (동작번호.charAt(0) == 'm') 처리값 = Xotira_Fayllar.Yaratish_katalog();
            else if (동작번호.charAt(0) == 'r') 처리값 = Xotira_Fayllar.olib_tashlamoq_katalog();
            else { 처리값 = Xotira_Fayllar.Ochish(65); if (처리값 >= 3) 처리값 = Xotira_Fayllar.Yopish(처리값); }
        }
        if (처리값 < 0) 명령해석기.Xato(처리값);
    }
    static void namuna_VALUE(boolean 이동여부) {
        if (명령해석기.token_COUNT != 3) { 명령해석기.o_lchov = 2; 단말.Yozish("사용법: cp/mv 원본 목적지 (Fayl)\n"); return; }
        int 처리값 = 명령해석기.yo_l(1); if (처리값 >= 0) 처리값 = Xotira_Fayllar.normallashtirmoq_VALUE();
        if (처리값 < 0) { 명령해석기.Xato(처리값); return; }
        int 원본번호 = Xotira_Fayllar.FIND_kiritish(); if (원본번호 < 0) { 명령해석기.Xato(-2); return; }
        int kiritish_COUNT = Xotira_Fayllar.uzunlik_VALUE[원본번호]; for (int Loop_INDEX = 0; Loop_INDEX < kiritish_COUNT; Loop_INDEX++) ma_lumotlar[Loop_INDEX] = Xotira_Fayllar.자료읽기(원본번호, Loop_INDEX);
        처리값 = 명령해석기.yo_l(2); if (처리값 >= 0) 처리값 = Xotira_Fayllar.normallashtirmoq_VALUE();
        if (처리값 < 0) { 명령해석기.Xato(처리값); return; }
        if (Xotira_Fayllar.FIND_kiritish() == 원본번호) { if (!이동여부) 명령해석기.Xato(-22); return; }
        if (이동여부) { 처리값 = Xotira_Fayllar.이름바꾸기(원본번호); if (처리값 < 0) 명령해석기.Xato(처리값); return; }
        int 열린파일번호 = Xotira_Fayllar.Ochish(577); if (열린파일번호 < 0) { 명령해석기.Xato(열린파일번호); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < kiritish_COUNT; Loop_INDEX++) { 처리값 = Xotira_Fayllar.Yozish(열린파일번호, ma_lumotlar[Loop_INDEX]); if (처리값 < 0) { 명령해석기.Xato(처리값); break; } }
        Xotira_Fayllar.Yopish(열린파일번호);
    }
    static int raqam_VALUE(int dalil_INDEX) {
        if (dalil_INDEX >= 명령해석기.token_COUNT) return -1;
        int kiritish_COUNT = 0; for (int Loop_INDEX = 0; Loop_INDEX < 명령해석기.uzunlik_VALUE[dalil_INDEX]; Loop_INDEX++) { int belgi_kodi = 명령해석기.token_VALUE[명령해석기.시작점[dalil_INDEX] + Loop_INDEX]; if (belgi_kodi < '0' || belgi_kodi > '9' || kiritish_COUNT > 10000) return -1; kiritish_COUNT = kiritish_COUNT * 10 + belgi_kodi - '0'; } return kiritish_COUNT;
    }
    static void 세기() {
        int dalil_INDEX = 1, 선택번호 = 0;
        if (명령해석기.같음(1, "-c") || 명령해석기.같음(1, "-l") || 명령해석기.같음(1, "-w")) { 선택번호 = 명령해석기.같음(1, "-c") ? 1 : 명령해석기.같음(1, "-l") ? 2 : 3; dalil_INDEX++; }
        if (명령해석기.token_COUNT > dalil_INDEX + 1) { 명령해석기.o_lchov = 2; 단말.Yozish("사용법: wc [-c|-l|-w] [Fayl]\n"); return; }
        if (!입력준비(dalil_INDEX)) return;
        int bayt_COUNT = 0, 줄수 = 0, 낱말수 = 0, bayt_ma_lumotlar; boolean 낱말 = false;
        while ((bayt_ma_lumotlar = Oʻqish()) >= 0 && bayt_ma_lumotlar != 256) { bayt_COUNT++; if (bayt_ma_lumotlar == 10) 줄수++; boolean joy = bayt_ma_lumotlar == 32 || bayt_ma_lumotlar >= 9 && bayt_ma_lumotlar <= 13; if (!joy && !낱말) 낱말수++; 낱말 = !joy; }
        Yopish(); if (bayt_ma_lumotlar < 0) { 명령해석기.Xato(bayt_ma_lumotlar); return; }
        if (선택번호 != 0) 단말.수(선택번호 == 1 ? bayt_COUNT : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.수(줄수); 단말.문자(' '); 단말.수(낱말수); 단말.문자(' '); 단말.수(bayt_COUNT); } 단말.문자(10);
    }
    static void FIND_kiritish() {
        if (명령해석기.token_COUNT < 2 || 명령해석기.token_COUNT > 3) { 명령해석기.o_lchov = 2; 단말.Yozish("사용법: grep 찾을문구 [Fayl]\n"); return; }
        if (!입력준비(2)) return;
        int kiritish_COUNT = 0, bayt_ma_lumotlar, 일치수 = 0;
        while (true) {
            bayt_ma_lumotlar = Oʻqish();
            if (bayt_ma_lumotlar == 10 || bayt_ma_lumotlar == 256 || bayt_ma_lumotlar < 0) {
                boolean 찾은여부 = false;
                for (int Loop_INDEX = 0; Loop_INDEX <= kiritish_COUNT - 명령해석기.uzunlik_VALUE[1]; Loop_INDEX++) {
                    boolean 같은여부 = true; for (int ichki_qo_shilish_holat = 0; ichki_qo_shilish_holat < 명령해석기.uzunlik_VALUE[1]; ichki_qo_shilish_holat++) if (ma_lumotlar[Loop_INDEX + ichki_qo_shilish_holat] != 명령해석기.token_VALUE[명령해석기.시작점[1] + ichki_qo_shilish_holat]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (kiritish_COUNT > 0 || bayt_ma_lumotlar == 10)) { for (int Loop_INDEX = 0; Loop_INDEX < kiritish_COUNT; Loop_INDEX++) yozuv_taxtasi.직렬쓰기(ma_lumotlar[Loop_INDEX]); 단말.문자(10); 일치수++; }
                kiritish_COUNT = 0; if (bayt_ma_lumotlar != 10) break;
            } else if (kiritish_COUNT < ma_lumotlar.length) ma_lumotlar[kiritish_COUNT++] = bayt_ma_lumotlar;
            else { 명령해석기.Xato(-28); Yopish(); return; }
        }
        Yopish(); if (bayt_ma_lumotlar < 0) 명령해석기.Xato(bayt_ma_lumotlar); else if (명령해석기.o_lchov == 0) 명령해석기.o_lchov = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int dalil_INDEX = 1, 줄수 = 10;
        if (명령해석기.같음(1, "-n")) { 줄수 = raqam_VALUE(2); dalil_INDEX = 3; }
        if (줄수 < 0 || 명령해석기.token_COUNT > dalil_INDEX + 1) { 명령해석기.o_lchov = 2; 단말.Yozish("사용법: head/tail [-n 줄수] [Fayl]\n"); return; }
        if (!입력준비(dalil_INDEX)) return;
        int kiritish_COUNT = 0, bayt_ma_lumotlar;
        while ((bayt_ma_lumotlar = Oʻqish()) != 256 && bayt_ma_lumotlar >= 0) { if (kiritish_COUNT == ma_lumotlar.length) { 명령해석기.Xato(-28); Yopish(); return; } ma_lumotlar[kiritish_COUNT++] = bayt_ma_lumotlar; }
        Yopish(); if (bayt_ma_lumotlar < 0) { 명령해석기.Xato(bayt_ma_lumotlar); return; }
        int mahalliy_Start = 0, to_xtatmoq_holat = kiritish_COUNT;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int 총수 = 0; for (int Loop_INDEX = kiritish_COUNT - 2; Loop_INDEX >= 0; Loop_INDEX--) if (ma_lumotlar[Loop_INDEX] == 10 && ++총수 == 줄수) { mahalliy_Start = Loop_INDEX + 1; break; } }
        else { int 총수 = 0; for (int Loop_INDEX = 0; Loop_INDEX < kiritish_COUNT; Loop_INDEX++) if (ma_lumotlar[Loop_INDEX] == 10 && ++총수 == 줄수) { to_xtatmoq_holat = Loop_INDEX + 1; break; } }
        for (int Loop_INDEX = mahalliy_Start; Loop_INDEX < to_xtatmoq_holat; Loop_INDEX++) yozuv_taxtasi.직렬쓰기(ma_lumotlar[Loop_INDEX]);
    }
    static void 함께쓰기() {
        boolean 덧붙임여부 = 명령해석기.같음(1, "-a"); int dalil_INDEX = 덧붙임여부 ? 2 : 1;
        if (명령해석기.token_COUNT != dalil_INDEX + 1) { 명령해석기.o_lchov = 2; 단말.Yozish("사용법: tee [-a] Fayl\n"); return; }
        int 열린파일번호 = ochmoq_fayl(dalil_INDEX, 덧붙임여부 ? 1089 : 577); if (열린파일번호 < 0) { 명령해석기.Xato(열린파일번호); return; }
        입력파일 = -1; int bayt_ma_lumotlar;
        while ((bayt_ma_lumotlar = Oʻqish()) != 256 && bayt_ma_lumotlar >= 0) { int 처리값 = Xotira_Fayllar.Yozish(열린파일번호, bayt_ma_lumotlar); if (처리값 < 0) { 명령해석기.Xato(처리값); break; } yozuv_taxtasi.직렬쓰기(bayt_ma_lumotlar); }
        Xotira_Fayllar.Yopish(열린파일번호);
    }
}
