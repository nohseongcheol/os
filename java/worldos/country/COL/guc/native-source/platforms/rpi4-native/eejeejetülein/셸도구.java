// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 aluwataalapu_u 내장 도구. */
public final class 셸도구 {
    static int[] atijaaya = new int[16384];
    static int 입력파일 = -1;
    static int 파일열기(int ajutuu_ee_iyatialujuna, int 처리방식) {
        int 처리값 = 명령해석기.wopu_a_ttaaleemüin(ajutuu_ee_iyatialujuna); return 처리값 < 0 ? 처리값 : 기억파일.열기(처리방식);
    }
    static boolean 입력준비(int ajutuu_ee_iyatialujuna) {
        입력파일 = -1;
        if (ajutuu_ee_iyatialujuna < 명령해석기.토큰수) {
            입력파일 = 파일열기(ajutuu_ee_iyatialujuna, 0);
            if (입력파일 < 0) { 명령해석기.ajachitia(입력파일); return false; }
        }
        return true;
    }
    static int 읽기() {
        if (입력파일 >= 3) return 기억파일.읽기(입력파일);
        while (true) {
            int waai_atijaaya = 보드.직렬읽기(); if (waai_atijaaya == -2 || waai_atijaaya == 4) return 256;
            if (waai_atijaaya == 3) { 명령해석기.결과 = 130; return 256; }
            if (waai_atijaaya >= 0) return waai_atijaaya; 보드.양보();
        }
    }
    static void asürülaa() { if (입력파일 >= 3) 기억파일.asürülaa(입력파일); 입력파일 = -1; }
    static void e_rajaa_ajutuu() {
        int 마지막자리 = 명령해석기.토큰수 == 1 ? 2 : 명령해석기.토큰수;
        for (int ajutuu_ee_iyatialujuna = 1; ajutuu_ee_iyatialujuna < 마지막자리; ajutuu_ee_iyatialujuna++) {
            if (!입력준비(ajutuu_ee_iyatialujuna)) continue;
            int waai_atijaaya; while ((waai_atijaaya = 읽기()) != 256 && waai_atijaaya >= 0) 보드.직렬쓰기(waai_atijaaya);
            if (waai_atijaaya < 0) 명령해석기.ajachitia(waai_atijaaya); asürülaa();
        }
    }
    static void anaajaalaa_achikii(String 동작번호) {
        if (명령해석기.토큰수 != 2) { 명령해석기.결과 = 2; 단말.ashajaa("사용법: mkdir/rmdir/touch anaajaalaa\n"); return; }
        int 처리값 = 명령해석기.wopu_a_ttaaleemüin(1);
        if (처리값 >= 0) {
            if (동작번호.charAt(0) == 'm') 처리값 = 기억파일.폴더만들기();
            else if (동작번호.charAt(0) == 'r') 처리값 = 기억파일.폴더지우기();
            else { 처리값 = 기억파일.열기(65); if (처리값 >= 3) 처리값 = 기억파일.asürülaa(처리값); }
        }
        if (처리값 < 0) 명령해석기.ajachitia(처리값);
    }
    static void ashataa_ajutuu(boolean 이동여부) {
        if (명령해석기.토큰수 != 3) { 명령해석기.결과 = 2; 단말.ashajaa("사용법: cp/mv 원본 목적지 (anaajaalaa)\n"); return; }
        int 처리값 = 명령해석기.wopu_a_ttaaleemüin(1); if (처리값 >= 0) 처리값 = 기억파일.anaajaa_ajutuu();
        if (처리값 < 0) { 명령해석기.ajachitia(처리값); return; }
        int 원본번호 = 기억파일.찾기(); if (원본번호 < 0) { 명령해석기.ajachitia(-2); return; }
        int 항목수 = 기억파일.akaliaa_ajutuu[원본번호]; for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 항목수; eitawaakualü_ee_iyatialujuna++) atijaaya[eitawaakualü_ee_iyatialujuna] = 기억파일.자료읽기(원본번호, eitawaakualü_ee_iyatialujuna);
        처리값 = 명령해석기.wopu_a_ttaaleemüin(2); if (처리값 >= 0) 처리값 = 기억파일.anaajaa_ajutuu();
        if (처리값 < 0) { 명령해석기.ajachitia(처리값); return; }
        if (기억파일.찾기() == 원본번호) { if (!이동여부) 명령해석기.ajachitia(-22); return; }
        if (이동여부) { 처리값 = 기억파일.이름바꾸기(원본번호); if (처리값 < 0) 명령해석기.ajachitia(처리값); return; }
        int 열린파일번호 = 기억파일.열기(577); if (열린파일번호 < 0) { 명령해석기.ajachitia(열린파일번호); return; }
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 항목수; eitawaakualü_ee_iyatialujuna++) { 처리값 = 기억파일.ashajaa(열린파일번호, atijaaya[eitawaakualü_ee_iyatialujuna]); if (처리값 < 0) { 명령해석기.ajachitia(처리값); break; } }
        기억파일.asürülaa(열린파일번호);
    }
    static int 숫자(int ajutuu_ee_iyatialujuna) {
        if (ajutuu_ee_iyatialujuna >= 명령해석기.토큰수) return -1;
        int 항목수 = 0; for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 명령해석기.akaliaa_ajutuu[ajutuu_ee_iyatialujuna]; eitawaakualü_ee_iyatialujuna++) { int 문자값 = 명령해석기.토큰[명령해석기.시작점[ajutuu_ee_iyatialujuna] + eitawaakualü_ee_iyatialujuna]; if (문자값 < '0' || 문자값 > '9' || 항목수 > 10000) return -1; 항목수 = 항목수 * 10 + 문자값 - '0'; } return 항목수;
    }
    static void 세기() {
        int ajutuu_ee_iyatialujuna = 1, 선택번호 = 0;
        if (명령해석기.같음(1, "-c") || 명령해석기.같음(1, "-l") || 명령해석기.같음(1, "-w")) { 선택번호 = 명령해석기.같음(1, "-c") ? 1 : 명령해석기.같음(1, "-l") ? 2 : 3; ajutuu_ee_iyatialujuna++; }
        if (명령해석기.토큰수 > ajutuu_ee_iyatialujuna + 1) { 명령해석기.결과 = 2; 단말.ashajaa("사용법: wc [-c|-l|-w] [anaajaalaa]\n"); return; }
        if (!입력준비(ajutuu_ee_iyatialujuna)) return;
        int 바이트수 = 0, 줄수 = 0, 낱말수 = 0, waai_atijaaya; boolean 낱말 = false;
        while ((waai_atijaaya = 읽기()) >= 0 && waai_atijaaya != 256) { 바이트수++; if (waai_atijaaya == 10) 줄수++; boolean WAARAKATAJÜLÜ = waai_atijaaya == 32 || waai_atijaaya >= 9 && waai_atijaaya <= 13; if (!WAARAKATAJÜLÜ && !낱말) 낱말수++; 낱말 = !WAARAKATAJÜLÜ; }
        asürülaa(); if (waai_atijaaya < 0) { 명령해석기.ajachitia(waai_atijaaya); return; }
        if (선택번호 != 0) 단말.수(선택번호 == 1 ? 바이트수 : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.수(줄수); 단말.문자(' '); 단말.수(낱말수); 단말.문자(' '); 단말.수(바이트수); } 단말.문자(10);
    }
    static void 찾기() {
        if (명령해석기.토큰수 < 2 || 명령해석기.토큰수 > 3) { 명령해석기.결과 = 2; 단말.ashajaa("사용법: grep 찾을문구 [anaajaalaa]\n"); return; }
        if (!입력준비(2)) return;
        int 항목수 = 0, waai_atijaaya, 일치수 = 0;
        while (true) {
            waai_atijaaya = 읽기();
            if (waai_atijaaya == 10 || waai_atijaaya == 256 || waai_atijaaya < 0) {
                boolean 찾은여부 = false;
                for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna <= 항목수 - 명령해석기.akaliaa_ajutuu[1]; eitawaakualü_ee_iyatialujuna++) {
                    boolean 같은여부 = true; for (int 안쪽자리 = 0; 안쪽자리 < 명령해석기.akaliaa_ajutuu[1]; 안쪽자리++) if (atijaaya[eitawaakualü_ee_iyatialujuna + 안쪽자리] != 명령해석기.토큰[명령해석기.시작점[1] + 안쪽자리]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (항목수 > 0 || waai_atijaaya == 10)) { for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 항목수; eitawaakualü_ee_iyatialujuna++) 보드.직렬쓰기(atijaaya[eitawaakualü_ee_iyatialujuna]); 단말.문자(10); 일치수++; }
                항목수 = 0; if (waai_atijaaya != 10) break;
            } else if (항목수 < atijaaya.length) atijaaya[항목수++] = waai_atijaaya;
            else { 명령해석기.ajachitia(-28); asürülaa(); return; }
        }
        asürülaa(); if (waai_atijaaya < 0) 명령해석기.ajachitia(waai_atijaaya); else if (명령해석기.결과 == 0) 명령해석기.결과 = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int ajutuu_ee_iyatialujuna = 1, 줄수 = 10;
        if (명령해석기.같음(1, "-n")) { 줄수 = 숫자(2); ajutuu_ee_iyatialujuna = 3; }
        if (줄수 < 0 || 명령해석기.토큰수 > ajutuu_ee_iyatialujuna + 1) { 명령해석기.결과 = 2; 단말.ashajaa("사용법: head/tail [-n 줄수] [anaajaalaa]\n"); return; }
        if (!입력준비(ajutuu_ee_iyatialujuna)) return;
        int 항목수 = 0, waai_atijaaya;
        while ((waai_atijaaya = 읽기()) != 256 && waai_atijaaya >= 0) { if (항목수 == atijaaya.length) { 명령해석기.ajachitia(-28); asürülaa(); return; } atijaaya[항목수++] = waai_atijaaya; }
        asürülaa(); if (waai_atijaaya < 0) { 명령해석기.ajachitia(waai_atijaaya); return; }
        int 지역시작점 = 0, 끝자리 = 항목수;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int 총수 = 0; for (int eitawaakualü_ee_iyatialujuna = 항목수 - 2; eitawaakualü_ee_iyatialujuna >= 0; eitawaakualü_ee_iyatialujuna--) if (atijaaya[eitawaakualü_ee_iyatialujuna] == 10 && ++총수 == 줄수) { 지역시작점 = eitawaakualü_ee_iyatialujuna + 1; break; } }
        else { int 총수 = 0; for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 항목수; eitawaakualü_ee_iyatialujuna++) if (atijaaya[eitawaakualü_ee_iyatialujuna] == 10 && ++총수 == 줄수) { 끝자리 = eitawaakualü_ee_iyatialujuna + 1; break; } }
        for (int eitawaakualü_ee_iyatialujuna = 지역시작점; eitawaakualü_ee_iyatialujuna < 끝자리; eitawaakualü_ee_iyatialujuna++) 보드.직렬쓰기(atijaaya[eitawaakualü_ee_iyatialujuna]);
    }
    static void 함께쓰기() {
        boolean 덧붙임여부 = 명령해석기.같음(1, "-a"); int ajutuu_ee_iyatialujuna = 덧붙임여부 ? 2 : 1;
        if (명령해석기.토큰수 != ajutuu_ee_iyatialujuna + 1) { 명령해석기.결과 = 2; 단말.ashajaa("사용법: tee [-a] anaajaalaa\n"); return; }
        int 열린파일번호 = 파일열기(ajutuu_ee_iyatialujuna, 덧붙임여부 ? 1089 : 577); if (열린파일번호 < 0) { 명령해석기.ajachitia(열린파일번호); return; }
        입력파일 = -1; int waai_atijaaya;
        while ((waai_atijaaya = 읽기()) != 256 && waai_atijaaya >= 0) { int 처리값 = 기억파일.ashajaa(열린파일번호, waai_atijaaya); if (처리값 < 0) { 명령해석기.ajachitia(처리값); break; } 보드.직렬쓰기(waai_atijaaya); }
        기억파일.asürülaa(열린파일번호);
    }
}
