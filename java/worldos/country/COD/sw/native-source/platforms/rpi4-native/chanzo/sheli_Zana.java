// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 sheli 내장 Zana. */
public final class sheli_Zana {
    static int[] data = new int[16384];
    static int 입력파일 = -1;
    static int unda_faili(int hoja_kielezo, int Mchakato_hali_tumizi) {
        int 처리값 = 명령해석기.njia(hoja_kielezo); return 처리값 < 0 ? 처리값 : kumbukumbu_Faili.unda(Mchakato_hali_tumizi);
    }
    static boolean 입력준비(int hoja_kielezo) {
        입력파일 = -1;
        if (hoja_kielezo < 명령해석기.토큰수) {
            입력파일 = unda_faili(hoja_kielezo, 0);
            if (입력파일 < 0) { 명령해석기.kosa(입력파일); return false; }
        }
        return true;
    }
    static int 읽기() {
        if (입력파일 >= 3) return kumbukumbu_Faili.읽기(입력파일);
        while (true) {
            int baiti_data = 보드.직렬읽기(); if (baiti_data == -2 || baiti_data == 4) return 256;
            if (baiti_data == 3) { 명령해석기.결과 = 130; return 256; }
            if (baiti_data >= 0) return baiti_data; 보드.ahirisha_CPU();
        }
    }
    static void funga() { if (입력파일 >= 3) kumbukumbu_Faili.funga(입력파일); 입력파일 = -1; }
    static void Onesha_thamani() {
        int 마지막자리 = 명령해석기.토큰수 == 1 ? 2 : 명령해석기.토큰수;
        for (int hoja_kielezo = 1; hoja_kielezo < 마지막자리; hoja_kielezo++) {
            if (!입력준비(hoja_kielezo)) continue;
            int baiti_data; while ((baiti_data = 읽기()) != 256 && baiti_data >= 0) 보드.직렬쓰기(baiti_data);
            if (baiti_data < 0) 명령해석기.kosa(baiti_data); funga();
        }
    }
    static void faili_Kazi(String 동작번호) {
        if (명령해석기.토큰수 != 2) { 명령해석기.결과 = 2; 단말.andika("사용법: mkdir/rmdir/touch faili\n"); return; }
        int 처리값 = 명령해석기.njia(1);
        if (처리값 >= 0) {
            if (동작번호.charAt(0) == 'm') 처리값 = kumbukumbu_Faili.unda_Saraka();
            else if (동작번호.charAt(0) == 'r') 처리값 = kumbukumbu_Faili.ondoa_Saraka();
            else { 처리값 = kumbukumbu_Faili.unda(65); if (처리값 >= 3) 처리값 = kumbukumbu_Faili.funga(처리값); }
        }
        if (처리값 < 0) 명령해석기.kosa(처리값);
    }
    static void mfano_thamani(boolean 이동여부) {
        if (명령해석기.토큰수 != 3) { 명령해석기.결과 = 2; 단말.andika("사용법: cp/mv 원본 목적지 (faili)\n"); return; }
        int 처리값 = 명령해석기.njia(1); if (처리값 >= 0) 처리값 = kumbukumbu_Faili.kawaidisha_thamani();
        if (처리값 < 0) { 명령해석기.kosa(처리값); return; }
        int 원본번호 = kumbukumbu_Faili.gundua_ingizo(); if (원본번호 < 0) { 명령해석기.kosa(-2); return; }
        int 항목수 = kumbukumbu_Faili.urefu_thamani[원본번호]; for (int kitanzi_kielezo = 0; kitanzi_kielezo < 항목수; kitanzi_kielezo++) data[kitanzi_kielezo] = kumbukumbu_Faili.자료읽기(원본번호, kitanzi_kielezo);
        처리값 = 명령해석기.njia(2); if (처리값 >= 0) 처리값 = kumbukumbu_Faili.kawaidisha_thamani();
        if (처리값 < 0) { 명령해석기.kosa(처리값); return; }
        if (kumbukumbu_Faili.gundua_ingizo() == 원본번호) { if (!이동여부) 명령해석기.kosa(-22); return; }
        if (이동여부) { 처리값 = kumbukumbu_Faili.이름바꾸기(원본번호); if (처리값 < 0) 명령해석기.kosa(처리값); return; }
        int 열린파일번호 = kumbukumbu_Faili.unda(577); if (열린파일번호 < 0) { 명령해석기.kosa(열린파일번호); return; }
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < 항목수; kitanzi_kielezo++) { 처리값 = kumbukumbu_Faili.andika(열린파일번호, data[kitanzi_kielezo]); if (처리값 < 0) { 명령해석기.kosa(처리값); break; } }
        kumbukumbu_Faili.funga(열린파일번호);
    }
    static int dijiti_thamani(int hoja_kielezo) {
        if (hoja_kielezo >= 명령해석기.토큰수) return -1;
        int 항목수 = 0; for (int kitanzi_kielezo = 0; kitanzi_kielezo < 명령해석기.urefu_thamani[hoja_kielezo]; kitanzi_kielezo++) { int msimbo_wa_kibambo = 명령해석기.tuzo_thamani[명령해석기.시작점[hoja_kielezo] + kitanzi_kielezo]; if (msimbo_wa_kibambo < '0' || msimbo_wa_kibambo > '9' || 항목수 > 10000) return -1; 항목수 = 항목수 * 10 + msimbo_wa_kibambo - '0'; } return 항목수;
    }
    static void 세기() {
        int hoja_kielezo = 1, 선택번호 = 0;
        if (명령해석기.같음(1, "-c") || 명령해석기.같음(1, "-l") || 명령해석기.같음(1, "-w")) { 선택번호 = 명령해석기.같음(1, "-c") ? 1 : 명령해석기.같음(1, "-l") ? 2 : 3; hoja_kielezo++; }
        if (명령해석기.토큰수 > hoja_kielezo + 1) { 명령해석기.결과 = 2; 단말.andika("사용법: wc [-c|-l|-w] [faili]\n"); return; }
        if (!입력준비(hoja_kielezo)) return;
        int 바이트수 = 0, 줄수 = 0, 낱말수 = 0, baiti_data; boolean 낱말 = false;
        while ((baiti_data = 읽기()) >= 0 && baiti_data != 256) { 바이트수++; if (baiti_data == 10) 줄수++; boolean eneo = baiti_data == 32 || baiti_data >= 9 && baiti_data <= 13; if (!eneo && !낱말) 낱말수++; 낱말 = !eneo; }
        funga(); if (baiti_data < 0) { 명령해석기.kosa(baiti_data); return; }
        if (선택번호 != 0) 단말.수(선택번호 == 1 ? 바이트수 : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.수(줄수); 단말.문자(' '); 단말.수(낱말수); 단말.문자(' '); 단말.수(바이트수); } 단말.문자(10);
    }
    static void gundua_ingizo() {
        if (명령해석기.토큰수 < 2 || 명령해석기.토큰수 > 3) { 명령해석기.결과 = 2; 단말.andika("사용법: grep 찾을문구 [faili]\n"); return; }
        if (!입력준비(2)) return;
        int 항목수 = 0, baiti_data, 일치수 = 0;
        while (true) {
            baiti_data = 읽기();
            if (baiti_data == 10 || baiti_data == 256 || baiti_data < 0) {
                boolean 찾은여부 = false;
                for (int kitanzi_kielezo = 0; kitanzi_kielezo <= 항목수 - 명령해석기.urefu_thamani[1]; kitanzi_kielezo++) {
                    boolean 같은여부 = true; for (int 안쪽자리 = 0; 안쪽자리 < 명령해석기.urefu_thamani[1]; 안쪽자리++) if (data[kitanzi_kielezo + 안쪽자리] != 명령해석기.tuzo_thamani[명령해석기.시작점[1] + 안쪽자리]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (항목수 > 0 || baiti_data == 10)) { for (int kitanzi_kielezo = 0; kitanzi_kielezo < 항목수; kitanzi_kielezo++) 보드.직렬쓰기(data[kitanzi_kielezo]); 단말.문자(10); 일치수++; }
                항목수 = 0; if (baiti_data != 10) break;
            } else if (항목수 < data.length) data[항목수++] = baiti_data;
            else { 명령해석기.kosa(-28); funga(); return; }
        }
        funga(); if (baiti_data < 0) 명령해석기.kosa(baiti_data); else if (명령해석기.결과 == 0) 명령해석기.결과 = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int hoja_kielezo = 1, 줄수 = 10;
        if (명령해석기.같음(1, "-n")) { 줄수 = dijiti_thamani(2); hoja_kielezo = 3; }
        if (줄수 < 0 || 명령해석기.토큰수 > hoja_kielezo + 1) { 명령해석기.결과 = 2; 단말.andika("사용법: head/tail [-n 줄수] [faili]\n"); return; }
        if (!입력준비(hoja_kielezo)) return;
        int 항목수 = 0, baiti_data;
        while ((baiti_data = 읽기()) != 256 && baiti_data >= 0) { if (항목수 == data.length) { 명령해석기.kosa(-28); funga(); return; } data[항목수++] = baiti_data; }
        funga(); if (baiti_data < 0) { 명령해석기.kosa(baiti_data); return; }
        int jirani_Anza = 0, 끝자리 = 항목수;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int 총수 = 0; for (int kitanzi_kielezo = 항목수 - 2; kitanzi_kielezo >= 0; kitanzi_kielezo--) if (data[kitanzi_kielezo] == 10 && ++총수 == 줄수) { jirani_Anza = kitanzi_kielezo + 1; break; } }
        else { int 총수 = 0; for (int kitanzi_kielezo = 0; kitanzi_kielezo < 항목수; kitanzi_kielezo++) if (data[kitanzi_kielezo] == 10 && ++총수 == 줄수) { 끝자리 = kitanzi_kielezo + 1; break; } }
        for (int kitanzi_kielezo = jirani_Anza; kitanzi_kielezo < 끝자리; kitanzi_kielezo++) 보드.직렬쓰기(data[kitanzi_kielezo]);
    }
    static void 함께쓰기() {
        boolean 덧붙임여부 = 명령해석기.같음(1, "-a"); int hoja_kielezo = 덧붙임여부 ? 2 : 1;
        if (명령해석기.토큰수 != hoja_kielezo + 1) { 명령해석기.결과 = 2; 단말.andika("사용법: tee [-a] faili\n"); return; }
        int 열린파일번호 = unda_faili(hoja_kielezo, 덧붙임여부 ? 1089 : 577); if (열린파일번호 < 0) { 명령해석기.kosa(열린파일번호); return; }
        입력파일 = -1; int baiti_data;
        while ((baiti_data = 읽기()) != 256 && baiti_data >= 0) { int 처리값 = kumbukumbu_Faili.andika(열린파일번호, baiti_data); if (처리값 < 0) { 명령해석기.kosa(처리값); break; } 보드.직렬쓰기(baiti_data); }
        kumbukumbu_Faili.funga(열린파일번호);
    }
}
