// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 piqujijjutiliriji 내장 도구. */
public final class 셸도구 {
    static int[] titiqqat = new int[16384];
    static int 입력파일 = -1;
    static int matuirli_ini(int aturniqarnirainiq_nalunaiqsimavik, int Pivallianiq_mode) {
        int 처리값 = 명령해석기.aqqut(aturniqarnirainiq_nalunaiqsimavik); return 처리값 < 0 ? 처리값 : 기억파일.matuirli(Pivallianiq_mode);
    }
    static boolean 입력준비(int aturniqarnirainiq_nalunaiqsimavik) {
        입력파일 = -1;
        if (aturniqarnirainiq_nalunaiqsimavik < 명령해석기.토큰수) {
            입력파일 = matuirli_ini(aturniqarnirainiq_nalunaiqsimavik, 0);
            if (입력파일 < 0) { 명령해석기.tammarniq(입력파일); return false; }
        }
        return true;
    }
    static int 읽기() {
        if (입력파일 >= 3) return 기억파일.읽기(입력파일);
        while (true) {
            int byte_titiqqat = 보드.직렬읽기(); if (byte_titiqqat == -2 || byte_titiqqat == 4) return 256;
            if (byte_titiqqat == 3) { 명령해석기.결과 = 130; return 256; }
            if (byte_titiqqat >= 0) return byte_titiqqat; 보드.양보();
        }
    }
    static void matuli() { if (입력파일 >= 3) 기억파일.matuli(입력파일); 입력파일 = -1; }
    static void takussarurli_atuutilik() {
        int 마지막자리 = 명령해석기.토큰수 == 1 ? 2 : 명령해석기.토큰수;
        for (int aturniqarnirainiq_nalunaiqsimavik = 1; aturniqarnirainiq_nalunaiqsimavik < 마지막자리; aturniqarnirainiq_nalunaiqsimavik++) {
            if (!입력준비(aturniqarnirainiq_nalunaiqsimavik)) continue;
            int byte_titiqqat; while ((byte_titiqqat = 읽기()) != 256 && byte_titiqqat >= 0) 보드.직렬쓰기(byte_titiqqat);
            if (byte_titiqqat < 0) 명령해석기.tammarniq(byte_titiqqat); matuli();
        }
    }
    static void ini_pijatsaq(String 동작번호) {
        if (명령해석기.토큰수 != 2) { 명령해석기.결과 = 2; 단말.titiraq("사용법: mkdir/rmdir/touch ini\n"); return; }
        int 처리값 = 명령해석기.aqqut(1);
        if (처리값 >= 0) {
            if (동작번호.charAt(0) == 'm') 처리값 = 기억파일.폴더만들기();
            else if (동작번호.charAt(0) == 'r') 처리값 = 기억파일.sanirvalli_tukimuagutiit();
            else { 처리값 = 기억파일.matuirli(65); if (처리값 >= 3) 처리값 = 기억파일.matuli(처리값); }
        }
        if (처리값 < 0) 명령해석기.tammarniq(처리값);
    }
    static void ijjuarli_atuutilik(boolean 이동여부) {
        if (명령해석기.토큰수 != 3) { 명령해석기.결과 = 2; 단말.titiraq("사용법: cp/mv 원본 목적지 (ini)\n"); return; }
        int 처리값 = 명령해석기.aqqut(1); if (처리값 >= 0) 처리값 = 기억파일.naammasitilli_atuutilik();
        if (처리값 < 0) { 명령해석기.tammarniq(처리값); return; }
        int 원본번호 = 기억파일.nanili_Iliniku(); if (원본번호 < 0) { 명령해석기.tammarniq(-2); return; }
        int 항목수 = 기억파일.takininga_atuutilik[원본번호]; for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 항목수; piliqqittaajuq_nalunaiqsimavik++) titiqqat[piliqqittaajuq_nalunaiqsimavik] = 기억파일.자료읽기(원본번호, piliqqittaajuq_nalunaiqsimavik);
        처리값 = 명령해석기.aqqut(2); if (처리값 >= 0) 처리값 = 기억파일.naammasitilli_atuutilik();
        if (처리값 < 0) { 명령해석기.tammarniq(처리값); return; }
        if (기억파일.nanili_Iliniku() == 원본번호) { if (!이동여부) 명령해석기.tammarniq(-22); return; }
        if (이동여부) { 처리값 = 기억파일.이름바꾸기(원본번호); if (처리값 < 0) 명령해석기.tammarniq(처리값); return; }
        int 열린파일번호 = 기억파일.matuirli(577); if (열린파일번호 < 0) { 명령해석기.tammarniq(열린파일번호); return; }
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 항목수; piliqqittaajuq_nalunaiqsimavik++) { 처리값 = 기억파일.titiraq(열린파일번호, titiqqat[piliqqittaajuq_nalunaiqsimavik]); if (처리값 < 0) { 명령해석기.tammarniq(처리값); break; } }
        기억파일.matuli(열린파일번호);
    }
    static int 숫자(int aturniqarnirainiq_nalunaiqsimavik) {
        if (aturniqarnirainiq_nalunaiqsimavik >= 명령해석기.토큰수) return -1;
        int 항목수 = 0; for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 명령해석기.takininga_atuutilik[aturniqarnirainiq_nalunaiqsimavik]; piliqqittaajuq_nalunaiqsimavik++) { int immikkuuqtumut_nalunaikkut = 명령해석기.토큰[명령해석기.시작점[aturniqarnirainiq_nalunaiqsimavik] + piliqqittaajuq_nalunaiqsimavik]; if (immikkuuqtumut_nalunaikkut < '0' || immikkuuqtumut_nalunaikkut > '9' || 항목수 > 10000) return -1; 항목수 = 항목수 * 10 + immikkuuqtumut_nalunaikkut - '0'; } return 항목수;
    }
    static void 세기() {
        int aturniqarnirainiq_nalunaiqsimavik = 1, 선택번호 = 0;
        if (명령해석기.같음(1, "-c") || 명령해석기.같음(1, "-l") || 명령해석기.같음(1, "-w")) { 선택번호 = 명령해석기.같음(1, "-c") ? 1 : 명령해석기.같음(1, "-l") ? 2 : 3; aturniqarnirainiq_nalunaiqsimavik++; }
        if (명령해석기.토큰수 > aturniqarnirainiq_nalunaiqsimavik + 1) { 명령해석기.결과 = 2; 단말.titiraq("사용법: wc [-c|-l|-w] [ini]\n"); return; }
        if (!입력준비(aturniqarnirainiq_nalunaiqsimavik)) return;
        int 바이트수 = 0, 줄수 = 0, 낱말수 = 0, byte_titiqqat; boolean 낱말 = false;
        while ((byte_titiqqat = 읽기()) >= 0 && byte_titiqqat != 256) { 바이트수++; if (byte_titiqqat == 10) 줄수++; boolean SPACEBAR = byte_titiqqat == 32 || byte_titiqqat >= 9 && byte_titiqqat <= 13; if (!SPACEBAR && !낱말) 낱말수++; 낱말 = !SPACEBAR; }
        matuli(); if (byte_titiqqat < 0) { 명령해석기.tammarniq(byte_titiqqat); return; }
        if (선택번호 != 0) 단말.수(선택번호 == 1 ? 바이트수 : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.수(줄수); 단말.문자(' '); 단말.수(낱말수); 단말.문자(' '); 단말.수(바이트수); } 단말.문자(10);
    }
    static void nanili_Iliniku() {
        if (명령해석기.토큰수 < 2 || 명령해석기.토큰수 > 3) { 명령해석기.결과 = 2; 단말.titiraq("사용법: grep 찾을문구 [ini]\n"); return; }
        if (!입력준비(2)) return;
        int 항목수 = 0, byte_titiqqat, 일치수 = 0;
        while (true) {
            byte_titiqqat = 읽기();
            if (byte_titiqqat == 10 || byte_titiqqat == 256 || byte_titiqqat < 0) {
                boolean 찾은여부 = false;
                for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik <= 항목수 - 명령해석기.takininga_atuutilik[1]; piliqqittaajuq_nalunaiqsimavik++) {
                    boolean 같은여부 = true; for (int 안쪽자리 = 0; 안쪽자리 < 명령해석기.takininga_atuutilik[1]; 안쪽자리++) if (titiqqat[piliqqittaajuq_nalunaiqsimavik + 안쪽자리] != 명령해석기.토큰[명령해석기.시작점[1] + 안쪽자리]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (항목수 > 0 || byte_titiqqat == 10)) { for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 항목수; piliqqittaajuq_nalunaiqsimavik++) 보드.직렬쓰기(titiqqat[piliqqittaajuq_nalunaiqsimavik]); 단말.문자(10); 일치수++; }
                항목수 = 0; if (byte_titiqqat != 10) break;
            } else if (항목수 < titiqqat.length) titiqqat[항목수++] = byte_titiqqat;
            else { 명령해석기.tammarniq(-28); matuli(); return; }
        }
        matuli(); if (byte_titiqqat < 0) 명령해석기.tammarniq(byte_titiqqat); else if (명령해석기.결과 == 0) 명령해석기.결과 = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int aturniqarnirainiq_nalunaiqsimavik = 1, 줄수 = 10;
        if (명령해석기.같음(1, "-n")) { 줄수 = 숫자(2); aturniqarnirainiq_nalunaiqsimavik = 3; }
        if (줄수 < 0 || 명령해석기.토큰수 > aturniqarnirainiq_nalunaiqsimavik + 1) { 명령해석기.결과 = 2; 단말.titiraq("사용법: head/tail [-n 줄수] [ini]\n"); return; }
        if (!입력준비(aturniqarnirainiq_nalunaiqsimavik)) return;
        int 항목수 = 0, byte_titiqqat;
        while ((byte_titiqqat = 읽기()) != 256 && byte_titiqqat >= 0) { if (항목수 == titiqqat.length) { 명령해석기.tammarniq(-28); matuli(); return; } titiqqat[항목수++] = byte_titiqqat; }
        matuli(); if (byte_titiqqat < 0) { 명령해석기.tammarniq(byte_titiqqat); return; }
        int tamaani_pigiarli = 0, 끝자리 = 항목수;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int 총수 = 0; for (int piliqqittaajuq_nalunaiqsimavik = 항목수 - 2; piliqqittaajuq_nalunaiqsimavik >= 0; piliqqittaajuq_nalunaiqsimavik--) if (titiqqat[piliqqittaajuq_nalunaiqsimavik] == 10 && ++총수 == 줄수) { tamaani_pigiarli = piliqqittaajuq_nalunaiqsimavik + 1; break; } }
        else { int 총수 = 0; for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 항목수; piliqqittaajuq_nalunaiqsimavik++) if (titiqqat[piliqqittaajuq_nalunaiqsimavik] == 10 && ++총수 == 줄수) { 끝자리 = piliqqittaajuq_nalunaiqsimavik + 1; break; } }
        for (int piliqqittaajuq_nalunaiqsimavik = tamaani_pigiarli; piliqqittaajuq_nalunaiqsimavik < 끝자리; piliqqittaajuq_nalunaiqsimavik++) 보드.직렬쓰기(titiqqat[piliqqittaajuq_nalunaiqsimavik]);
    }
    static void 함께쓰기() {
        boolean 덧붙임여부 = 명령해석기.같음(1, "-a"); int aturniqarnirainiq_nalunaiqsimavik = 덧붙임여부 ? 2 : 1;
        if (명령해석기.토큰수 != aturniqarnirainiq_nalunaiqsimavik + 1) { 명령해석기.결과 = 2; 단말.titiraq("사용법: tee [-a] ini\n"); return; }
        int 열린파일번호 = matuirli_ini(aturniqarnirainiq_nalunaiqsimavik, 덧붙임여부 ? 1089 : 577); if (열린파일번호 < 0) { 명령해석기.tammarniq(열린파일번호); return; }
        입력파일 = -1; int byte_titiqqat;
        while ((byte_titiqqat = 읽기()) != 256 && byte_titiqqat >= 0) { int 처리값 = 기억파일.titiraq(열린파일번호, byte_titiqqat); if (처리값 < 0) { 명령해석기.tammarniq(처리값); break; } 보드.직렬쓰기(byte_titiqqat); }
        기억파일.matuli(열린파일번호);
    }
}
