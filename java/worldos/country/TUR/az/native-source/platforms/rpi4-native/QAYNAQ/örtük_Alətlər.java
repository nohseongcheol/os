// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 örtük 내장 Alətlər. */
public final class örtük_Alətlər {
    static int[] verilənlər = new int[16384];
    static int 입력파일 = -1;
    static int açmaq_fayl(int arqument_INDEX, int Proses_MODE) {
        int 처리값 = 명령해석기.Cığır(arqument_INDEX); return 처리값 < 0 ? 처리값 : Yaddaş_Fayllar.Aç(Proses_MODE);
    }
    static boolean 입력준비(int arqument_INDEX) {
        입력파일 = -1;
        if (arqument_INDEX < 명령해석기.nişan_COUNT) {
            입력파일 = açmaq_fayl(arqument_INDEX, 0);
            if (입력파일 < 0) { 명령해석기.XƏTA(입력파일); return false; }
        }
        return true;
    }
    static int Oxuma() {
        if (입력파일 >= 3) return Yaddaş_Fayllar.Oxuma(입력파일);
        while (true) {
            int bayt_verilənlər = lövhə.직렬읽기(); if (bayt_verilənlər == -2 || bayt_verilənlər == 4) return 256;
            if (bayt_verilənlər == 3) { 명령해석기.ölçü = 130; return 256; }
            if (bayt_verilənlər >= 0) return bayt_verilənlər; lövhə.YIELD_CPU();
        }
    }
    static void Bağla() { if (입력파일 >= 3) Yaddaş_Fayllar.Bağla(입력파일); 입력파일 = -1; }
    static void baxmaq_VALUE() {
        int 마지막자리 = 명령해석기.nişan_COUNT == 1 ? 2 : 명령해석기.nişan_COUNT;
        for (int arqument_INDEX = 1; arqument_INDEX < 마지막자리; arqument_INDEX++) {
            if (!입력준비(arqument_INDEX)) continue;
            int bayt_verilənlər; while ((bayt_verilənlər = Oxuma()) != 256 && bayt_verilənlər >= 0) lövhə.직렬쓰기(bayt_verilənlər);
            if (bayt_verilənlər < 0) 명령해석기.XƏTA(bayt_verilənlər); Bağla();
        }
    }
    static void fayl_müqavilə(String 동작번호) {
        if (명령해석기.nişan_COUNT != 2) { 명령해석기.ölçü = 2; 단말.Yazma("사용법: mkdir/rmdir/touch FAYL\n"); return; }
        int 처리값 = 명령해석기.Cığır(1);
        if (처리값 >= 0) {
            if (동작번호.charAt(0) == 'm') 처리값 = Yaddaş_Fayllar.yarat_kataloq();
            else if (동작번호.charAt(0) == 'r') 처리값 = Yaddaş_Fayllar.silmək_kataloq();
            else { 처리값 = Yaddaş_Fayllar.Aç(65); if (처리값 >= 3) 처리값 = Yaddaş_Fayllar.Bağla(처리값); }
        }
        if (처리값 < 0) 명령해석기.XƏTA(처리값);
    }
    static void nümunə_VALUE(boolean 이동여부) {
        if (명령해석기.nişan_COUNT != 3) { 명령해석기.ölçü = 2; 단말.Yazma("사용법: cp/mv 원본 목적지 (FAYL)\n"); return; }
        int 처리값 = 명령해석기.Cığır(1); if (처리값 >= 0) 처리값 = Yaddaş_Fayllar.normallaşdırmaq_VALUE();
        if (처리값 < 0) { 명령해석기.XƏTA(처리값); return; }
        int 원본번호 = Yaddaş_Fayllar.FIND_daxiletmə(); if (원본번호 < 0) { 명령해석기.XƏTA(-2); return; }
        int daxiletmə_COUNT = Yaddaş_Fayllar.uzunluq_VALUE[원본번호]; for (int Loop_INDEX = 0; Loop_INDEX < daxiletmə_COUNT; Loop_INDEX++) verilənlər[Loop_INDEX] = Yaddaş_Fayllar.자료읽기(원본번호, Loop_INDEX);
        처리값 = 명령해석기.Cığır(2); if (처리값 >= 0) 처리값 = Yaddaş_Fayllar.normallaşdırmaq_VALUE();
        if (처리값 < 0) { 명령해석기.XƏTA(처리값); return; }
        if (Yaddaş_Fayllar.FIND_daxiletmə() == 원본번호) { if (!이동여부) 명령해석기.XƏTA(-22); return; }
        if (이동여부) { 처리값 = Yaddaş_Fayllar.이름바꾸기(원본번호); if (처리값 < 0) 명령해석기.XƏTA(처리값); return; }
        int 열린파일번호 = Yaddaş_Fayllar.Aç(577); if (열린파일번호 < 0) { 명령해석기.XƏTA(열린파일번호); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < daxiletmə_COUNT; Loop_INDEX++) { 처리값 = Yaddaş_Fayllar.Yazma(열린파일번호, verilənlər[Loop_INDEX]); if (처리값 < 0) { 명령해석기.XƏTA(처리값); break; } }
        Yaddaş_Fayllar.Bağla(열린파일번호);
    }
    static int rəqəm_VALUE(int arqument_INDEX) {
        if (arqument_INDEX >= 명령해석기.nişan_COUNT) return -1;
        int daxiletmə_COUNT = 0; for (int Loop_INDEX = 0; Loop_INDEX < 명령해석기.uzunluq_VALUE[arqument_INDEX]; Loop_INDEX++) { int simvol_kodu = 명령해석기.nişan_VALUE[명령해석기.시작점[arqument_INDEX] + Loop_INDEX]; if (simvol_kodu < '0' || simvol_kodu > '9' || daxiletmə_COUNT > 10000) return -1; daxiletmə_COUNT = daxiletmə_COUNT * 10 + simvol_kodu - '0'; } return daxiletmə_COUNT;
    }
    static void 세기() {
        int arqument_INDEX = 1, 선택번호 = 0;
        if (명령해석기.같음(1, "-c") || 명령해석기.같음(1, "-l") || 명령해석기.같음(1, "-w")) { 선택번호 = 명령해석기.같음(1, "-c") ? 1 : 명령해석기.같음(1, "-l") ? 2 : 3; arqument_INDEX++; }
        if (명령해석기.nişan_COUNT > arqument_INDEX + 1) { 명령해석기.ölçü = 2; 단말.Yazma("사용법: wc [-c|-l|-w] [FAYL]\n"); return; }
        if (!입력준비(arqument_INDEX)) return;
        int bayt_COUNT = 0, 줄수 = 0, 낱말수 = 0, bayt_verilənlər; boolean 낱말 = false;
        while ((bayt_verilənlər = Oxuma()) >= 0 && bayt_verilənlər != 256) { bayt_COUNT++; if (bayt_verilənlər == 10) 줄수++; boolean məkan = bayt_verilənlər == 32 || bayt_verilənlər >= 9 && bayt_verilənlər <= 13; if (!məkan && !낱말) 낱말수++; 낱말 = !məkan; }
        Bağla(); if (bayt_verilənlər < 0) { 명령해석기.XƏTA(bayt_verilənlər); return; }
        if (선택번호 != 0) 단말.수(선택번호 == 1 ? bayt_COUNT : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.수(줄수); 단말.문자(' '); 단말.수(낱말수); 단말.문자(' '); 단말.수(bayt_COUNT); } 단말.문자(10);
    }
    static void FIND_daxiletmə() {
        if (명령해석기.nişan_COUNT < 2 || 명령해석기.nişan_COUNT > 3) { 명령해석기.ölçü = 2; 단말.Yazma("사용법: grep 찾을문구 [FAYL]\n"); return; }
        if (!입력준비(2)) return;
        int daxiletmə_COUNT = 0, bayt_verilənlər, 일치수 = 0;
        while (true) {
            bayt_verilənlər = Oxuma();
            if (bayt_verilənlər == 10 || bayt_verilənlər == 256 || bayt_verilənlər < 0) {
                boolean 찾은여부 = false;
                for (int Loop_INDEX = 0; Loop_INDEX <= daxiletmə_COUNT - 명령해석기.uzunluq_VALUE[1]; Loop_INDEX++) {
                    boolean 같은여부 = true; for (int daxili_qoşulma_yerinə_qoymaq = 0; daxili_qoşulma_yerinə_qoymaq < 명령해석기.uzunluq_VALUE[1]; daxili_qoşulma_yerinə_qoymaq++) if (verilənlər[Loop_INDEX + daxili_qoşulma_yerinə_qoymaq] != 명령해석기.nişan_VALUE[명령해석기.시작점[1] + daxili_qoşulma_yerinə_qoymaq]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (daxiletmə_COUNT > 0 || bayt_verilənlər == 10)) { for (int Loop_INDEX = 0; Loop_INDEX < daxiletmə_COUNT; Loop_INDEX++) lövhə.직렬쓰기(verilənlər[Loop_INDEX]); 단말.문자(10); 일치수++; }
                daxiletmə_COUNT = 0; if (bayt_verilənlər != 10) break;
            } else if (daxiletmə_COUNT < verilənlər.length) verilənlər[daxiletmə_COUNT++] = bayt_verilənlər;
            else { 명령해석기.XƏTA(-28); Bağla(); return; }
        }
        Bağla(); if (bayt_verilənlər < 0) 명령해석기.XƏTA(bayt_verilənlər); else if (명령해석기.ölçü == 0) 명령해석기.ölçü = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int arqument_INDEX = 1, 줄수 = 10;
        if (명령해석기.같음(1, "-n")) { 줄수 = rəqəm_VALUE(2); arqument_INDEX = 3; }
        if (줄수 < 0 || 명령해석기.nişan_COUNT > arqument_INDEX + 1) { 명령해석기.ölçü = 2; 단말.Yazma("사용법: head/tail [-n 줄수] [FAYL]\n"); return; }
        if (!입력준비(arqument_INDEX)) return;
        int daxiletmə_COUNT = 0, bayt_verilənlər;
        while ((bayt_verilənlər = Oxuma()) != 256 && bayt_verilənlər >= 0) { if (daxiletmə_COUNT == verilənlər.length) { 명령해석기.XƏTA(-28); Bağla(); return; } verilənlər[daxiletmə_COUNT++] = bayt_verilənlər; }
        Bağla(); if (bayt_verilənlər < 0) { 명령해석기.XƏTA(bayt_verilənlər); return; }
        int lokal_Başla = 0, bitirmək_yerinə_qoymaq = daxiletmə_COUNT;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int 총수 = 0; for (int Loop_INDEX = daxiletmə_COUNT - 2; Loop_INDEX >= 0; Loop_INDEX--) if (verilənlər[Loop_INDEX] == 10 && ++총수 == 줄수) { lokal_Başla = Loop_INDEX + 1; break; } }
        else { int 총수 = 0; for (int Loop_INDEX = 0; Loop_INDEX < daxiletmə_COUNT; Loop_INDEX++) if (verilənlər[Loop_INDEX] == 10 && ++총수 == 줄수) { bitirmək_yerinə_qoymaq = Loop_INDEX + 1; break; } }
        for (int Loop_INDEX = lokal_Başla; Loop_INDEX < bitirmək_yerinə_qoymaq; Loop_INDEX++) lövhə.직렬쓰기(verilənlər[Loop_INDEX]);
    }
    static void 함께쓰기() {
        boolean 덧붙임여부 = 명령해석기.같음(1, "-a"); int arqument_INDEX = 덧붙임여부 ? 2 : 1;
        if (명령해석기.nişan_COUNT != arqument_INDEX + 1) { 명령해석기.ölçü = 2; 단말.Yazma("사용법: tee [-a] FAYL\n"); return; }
        int 열린파일번호 = açmaq_fayl(arqument_INDEX, 덧붙임여부 ? 1089 : 577); if (열린파일번호 < 0) { 명령해석기.XƏTA(열린파일번호); return; }
        입력파일 = -1; int bayt_verilənlər;
        while ((bayt_verilənlər = Oxuma()) != 256 && bayt_verilənlər >= 0) { int 처리값 = Yaddaş_Fayllar.Yazma(열린파일번호, bayt_verilənlər); if (처리값 < 0) { 명령해석기.XƏTA(처리값); break; } lövhə.직렬쓰기(bayt_verilənlər); }
        Yaddaş_Fayllar.Bağla(열린파일번호);
    }
}
