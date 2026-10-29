// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 laalagal 내장 도구. */
public final class 셸도구 {
    static int[] keɓe = new int[16384];
    static int 입력파일 = -1;
    static int udditde_fiilde(int hujja_joopirdu, int Yuɓɓo_golle_modd) {
        int 처리값 = 명령해석기.laawol(hujja_joopirdu); return 처리값 < 0 ? 처리값 : 기억파일.udditde(Yuɓɓo_golle_modd);
    }
    static boolean 입력준비(int hujja_joopirdu) {
        입력파일 = -1;
        if (hujja_joopirdu < 명령해석기.토큰수) {
            입력파일 = udditde_fiilde(hujja_joopirdu, 0);
            if (입력파일 < 0) { 명령해석기.juumre(입력파일); return false; }
        }
        return true;
    }
    static int 읽기() {
        if (입력파일 >= 3) return 기억파일.읽기(입력파일);
        while (true) {
            int oktee_keɓe = 보드.직렬읽기(); if (oktee_keɓe == -2 || oktee_keɓe == 4) return 256;
            if (oktee_keɓe == 3) { 명령해석기.결과 = 130; return 256; }
            if (oktee_keɓe >= 0) return oktee_keɓe; 보드.양보();
        }
    }
    static void uddude() { if (입력파일 >= 3) 기억파일.uddude(입력파일); 입력파일 = -1; }
    static void kollal_njaru() {
        int 마지막자리 = 명령해석기.토큰수 == 1 ? 2 : 명령해석기.토큰수;
        for (int hujja_joopirdu = 1; hujja_joopirdu < 마지막자리; hujja_joopirdu++) {
            if (!입력준비(hujja_joopirdu)) continue;
            int oktee_keɓe; while ((oktee_keɓe = 읽기()) != 256 && oktee_keɓe >= 0) 보드.직렬쓰기(oktee_keɓe);
            if (oktee_keɓe < 0) 명령해석기.juumre(oktee_keɓe); uddude();
        }
    }
    static void fiilde_haaju(String 동작번호) {
        if (명령해석기.토큰수 != 2) { 명령해석기.결과 = 2; 단말.winndude("사용법: mkdir/rmdir/touch fiilde\n"); return; }
        int 처리값 = 명령해석기.laawol(1);
        if (처리값 >= 0) {
            if (동작번호.charAt(0) == 'm') 처리값 = 기억파일.폴더만들기();
            else if (동작번호.charAt(0) == 'r') 처리값 = 기억파일.ittude_mooftordu();
            else { 처리값 = 기억파일.udditde(65); if (처리값 >= 3) 처리값 = 기억파일.uddude(처리값); }
        }
        if (처리값 < 0) 명령해석기.juumre(처리값);
    }
    static void waanjitaade_njaru(boolean 이동여부) {
        if (명령해석기.토큰수 != 3) { 명령해석기.결과 = 2; 단말.winndude("사용법: cp/mv 원본 목적지 (fiilde)\n"); return; }
        int 처리값 = 명령해석기.laawol(1); if (처리값 >= 0) 처리값 = 기억파일.정규화();
        if (처리값 < 0) { 명령해석기.juumre(처리값); return; }
        int 원본번호 = 기억파일.yiylaade_naatnugol(); if (원본번호 < 0) { 명령해석기.juumre(-2); return; }
        int 항목수 = 기억파일.njuuteendi_njaru[원본번호]; for (int kowal_joopirdu = 0; kowal_joopirdu < 항목수; kowal_joopirdu++) keɓe[kowal_joopirdu] = 기억파일.자료읽기(원본번호, kowal_joopirdu);
        처리값 = 명령해석기.laawol(2); if (처리값 >= 0) 처리값 = 기억파일.정규화();
        if (처리값 < 0) { 명령해석기.juumre(처리값); return; }
        if (기억파일.yiylaade_naatnugol() == 원본번호) { if (!이동여부) 명령해석기.juumre(-22); return; }
        if (이동여부) { 처리값 = 기억파일.이름바꾸기(원본번호); if (처리값 < 0) 명령해석기.juumre(처리값); return; }
        int 열린파일번호 = 기억파일.udditde(577); if (열린파일번호 < 0) { 명령해석기.juumre(열린파일번호); return; }
        for (int kowal_joopirdu = 0; kowal_joopirdu < 항목수; kowal_joopirdu++) { 처리값 = 기억파일.winndude(열린파일번호, keɓe[kowal_joopirdu]); if (처리값 < 0) { 명령해석기.juumre(처리값); break; } }
        기억파일.uddude(열린파일번호);
    }
    static int 숫자(int hujja_joopirdu) {
        if (hujja_joopirdu >= 명령해석기.토큰수) return -1;
        int 항목수 = 0; for (int kowal_joopirdu = 0; kowal_joopirdu < 명령해석기.njuuteendi_njaru[hujja_joopirdu]; kowal_joopirdu++) { int 문자값 = 명령해석기.토큰[명령해석기.시작점[hujja_joopirdu] + kowal_joopirdu]; if (문자값 < '0' || 문자값 > '9' || 항목수 > 10000) return -1; 항목수 = 항목수 * 10 + 문자값 - '0'; } return 항목수;
    }
    static void 세기() {
        int hujja_joopirdu = 1, 선택번호 = 0;
        if (명령해석기.같음(1, "-c") || 명령해석기.같음(1, "-l") || 명령해석기.같음(1, "-w")) { 선택번호 = 명령해석기.같음(1, "-c") ? 1 : 명령해석기.같음(1, "-l") ? 2 : 3; hujja_joopirdu++; }
        if (명령해석기.토큰수 > hujja_joopirdu + 1) { 명령해석기.결과 = 2; 단말.winndude("사용법: wc [-c|-l|-w] [fiilde]\n"); return; }
        if (!입력준비(hujja_joopirdu)) return;
        int 바이트수 = 0, 줄수 = 0, 낱말수 = 0, oktee_keɓe; boolean 낱말 = false;
        while ((oktee_keɓe = 읽기()) >= 0 && oktee_keɓe != 256) { 바이트수++; if (oktee_keɓe == 10) 줄수++; boolean wonorde = oktee_keɓe == 32 || oktee_keɓe >= 9 && oktee_keɓe <= 13; if (!wonorde && !낱말) 낱말수++; 낱말 = !wonorde; }
        uddude(); if (oktee_keɓe < 0) { 명령해석기.juumre(oktee_keɓe); return; }
        if (선택번호 != 0) 단말.수(선택번호 == 1 ? 바이트수 : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.수(줄수); 단말.문자(' '); 단말.수(낱말수); 단말.문자(' '); 단말.수(바이트수); } 단말.문자(10);
    }
    static void yiylaade_naatnugol() {
        if (명령해석기.토큰수 < 2 || 명령해석기.토큰수 > 3) { 명령해석기.결과 = 2; 단말.winndude("사용법: grep 찾을문구 [fiilde]\n"); return; }
        if (!입력준비(2)) return;
        int 항목수 = 0, oktee_keɓe, 일치수 = 0;
        while (true) {
            oktee_keɓe = 읽기();
            if (oktee_keɓe == 10 || oktee_keɓe == 256 || oktee_keɓe < 0) {
                boolean 찾은여부 = false;
                for (int kowal_joopirdu = 0; kowal_joopirdu <= 항목수 - 명령해석기.njuuteendi_njaru[1]; kowal_joopirdu++) {
                    boolean 같은여부 = true; for (int 안쪽자리 = 0; 안쪽자리 < 명령해석기.njuuteendi_njaru[1]; 안쪽자리++) if (keɓe[kowal_joopirdu + 안쪽자리] != 명령해석기.토큰[명령해석기.시작점[1] + 안쪽자리]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (항목수 > 0 || oktee_keɓe == 10)) { for (int kowal_joopirdu = 0; kowal_joopirdu < 항목수; kowal_joopirdu++) 보드.직렬쓰기(keɓe[kowal_joopirdu]); 단말.문자(10); 일치수++; }
                항목수 = 0; if (oktee_keɓe != 10) break;
            } else if (항목수 < keɓe.length) keɓe[항목수++] = oktee_keɓe;
            else { 명령해석기.juumre(-28); uddude(); return; }
        }
        uddude(); if (oktee_keɓe < 0) 명령해석기.juumre(oktee_keɓe); else if (명령해석기.결과 == 0) 명령해석기.결과 = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int hujja_joopirdu = 1, 줄수 = 10;
        if (명령해석기.같음(1, "-n")) { 줄수 = 숫자(2); hujja_joopirdu = 3; }
        if (줄수 < 0 || 명령해석기.토큰수 > hujja_joopirdu + 1) { 명령해석기.결과 = 2; 단말.winndude("사용법: head/tail [-n 줄수] [fiilde]\n"); return; }
        if (!입력준비(hujja_joopirdu)) return;
        int 항목수 = 0, oktee_keɓe;
        while ((oktee_keɓe = 읽기()) != 256 && oktee_keɓe >= 0) { if (항목수 == keɓe.length) { 명령해석기.juumre(-28); uddude(); return; } keɓe[항목수++] = oktee_keɓe; }
        uddude(); if (oktee_keɓe < 0) { 명령해석기.juumre(oktee_keɓe); return; }
        int nokkuwal_huɓɓude = 0, 끝자리 = 항목수;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int 총수 = 0; for (int kowal_joopirdu = 항목수 - 2; kowal_joopirdu >= 0; kowal_joopirdu--) if (keɓe[kowal_joopirdu] == 10 && ++총수 == 줄수) { nokkuwal_huɓɓude = kowal_joopirdu + 1; break; } }
        else { int 총수 = 0; for (int kowal_joopirdu = 0; kowal_joopirdu < 항목수; kowal_joopirdu++) if (keɓe[kowal_joopirdu] == 10 && ++총수 == 줄수) { 끝자리 = kowal_joopirdu + 1; break; } }
        for (int kowal_joopirdu = nokkuwal_huɓɓude; kowal_joopirdu < 끝자리; kowal_joopirdu++) 보드.직렬쓰기(keɓe[kowal_joopirdu]);
    }
    static void 함께쓰기() {
        boolean 덧붙임여부 = 명령해석기.같음(1, "-a"); int hujja_joopirdu = 덧붙임여부 ? 2 : 1;
        if (명령해석기.토큰수 != hujja_joopirdu + 1) { 명령해석기.결과 = 2; 단말.winndude("사용법: tee [-a] fiilde\n"); return; }
        int 열린파일번호 = udditde_fiilde(hujja_joopirdu, 덧붙임여부 ? 1089 : 577); if (열린파일번호 < 0) { 명령해석기.juumre(열린파일번호); return; }
        입력파일 = -1; int oktee_keɓe;
        while ((oktee_keɓe = 읽기()) != 256 && oktee_keɓe >= 0) { int 처리값 = 기억파일.winndude(열린파일번호, oktee_keɓe); if (처리값 < 0) { 명령해석기.juumre(처리값); break; } 보드.직렬쓰기(oktee_keɓe); }
        기억파일.uddude(열린파일번호);
    }
}
