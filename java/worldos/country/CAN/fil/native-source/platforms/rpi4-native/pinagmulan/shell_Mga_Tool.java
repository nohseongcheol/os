// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 shell 내장 Mga_Tool. */
public final class shell_Mga_Tool {
    static int[] data = new int[16384];
    static int 입력파일 = -1;
    static int buksan_file(int argumento_INDEX, int Proseso_MODE) {
        int 처리값 = 명령해석기.path(argumento_INDEX); return 처리값 < 0 ? 처리값 : Memory_Mga_File.buksan(Proseso_MODE);
    }
    static boolean 입력준비(int argumento_INDEX) {
        입력파일 = -1;
        if (argumento_INDEX < 명령해석기.token_COUNT) {
            입력파일 = buksan_file(argumento_INDEX, 0);
            if (입력파일 < 0) { 명령해석기.error(입력파일); return false; }
        }
        return true;
    }
    static int 읽기() {
        if (입력파일 >= 3) return Memory_Mga_File.읽기(입력파일);
        while (true) {
            int byte_data = board.직렬읽기(); if (byte_data == -2 || byte_data == 4) return 256;
            if (byte_data == 3) { 명령해석기.sukat = 130; return 256; }
            if (byte_data >= 0) return byte_data; board.YIELD_CPU();
        }
    }
    static void isara() { if (입력파일 >= 3) Memory_Mga_File.isara(입력파일); 입력파일 = -1; }
    static void View_VALUE() {
        int 마지막자리 = 명령해석기.token_COUNT == 1 ? 2 : 명령해석기.token_COUNT;
        for (int argumento_INDEX = 1; argumento_INDEX < 마지막자리; argumento_INDEX++) {
            if (!입력준비(argumento_INDEX)) continue;
            int byte_data; while ((byte_data = 읽기()) != 256 && byte_data >= 0) board.직렬쓰기(byte_data);
            if (byte_data < 0) 명령해석기.error(byte_data); isara();
        }
    }
    static void file_kaso(String 동작번호) {
        if (명령해석기.token_COUNT != 2) { 명령해석기.sukat = 2; 단말.sumulat("사용법: mkdir/rmdir/touch file\n"); return; }
        int 처리값 = 명령해석기.path(1);
        if (처리값 >= 0) {
            if (동작번호.charAt(0) == 'm') 처리값 = Memory_Mga_File.Create_Directory();
            else if (동작번호.charAt(0) == 'r') 처리값 = Memory_Mga_File.tanggalin_Directory();
            else { 처리값 = Memory_Mga_File.buksan(65); if (처리값 >= 3) 처리값 = Memory_Mga_File.isara(처리값); }
        }
        if (처리값 < 0) 명령해석기.error(처리값);
    }
    static void gumawa_ng_kopya_VALUE(boolean 이동여부) {
        if (명령해석기.token_COUNT != 3) { 명령해석기.sukat = 2; 단말.sumulat("사용법: cp/mv 원본 목적지 (file)\n"); return; }
        int 처리값 = 명령해석기.path(1); if (처리값 >= 0) 처리값 = Memory_Mga_File.normalisahin_VALUE();
        if (처리값 < 0) { 명령해석기.error(처리값); return; }
        int 원본번호 = Memory_Mga_File.FIND_pagpasok(); if (원본번호 < 0) { 명령해석기.error(-2); return; }
        int pagpasok_COUNT = Memory_Mga_File.haba_VALUE[원본번호]; for (int Loop_INDEX = 0; Loop_INDEX < pagpasok_COUNT; Loop_INDEX++) data[Loop_INDEX] = Memory_Mga_File.자료읽기(원본번호, Loop_INDEX);
        처리값 = 명령해석기.path(2); if (처리값 >= 0) 처리값 = Memory_Mga_File.normalisahin_VALUE();
        if (처리값 < 0) { 명령해석기.error(처리값); return; }
        if (Memory_Mga_File.FIND_pagpasok() == 원본번호) { if (!이동여부) 명령해석기.error(-22); return; }
        if (이동여부) { 처리값 = Memory_Mga_File.이름바꾸기(원본번호); if (처리값 < 0) 명령해석기.error(처리값); return; }
        int 열린파일번호 = Memory_Mga_File.buksan(577); if (열린파일번호 < 0) { 명령해석기.error(열린파일번호); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < pagpasok_COUNT; Loop_INDEX++) { 처리값 = Memory_Mga_File.sumulat(열린파일번호, data[Loop_INDEX]); if (처리값 < 0) { 명령해석기.error(처리값); break; } }
        Memory_Mga_File.isara(열린파일번호);
    }
    static int digit_VALUE(int argumento_INDEX) {
        if (argumento_INDEX >= 명령해석기.token_COUNT) return -1;
        int pagpasok_COUNT = 0; for (int Loop_INDEX = 0; Loop_INDEX < 명령해석기.haba_VALUE[argumento_INDEX]; Loop_INDEX++) { int character_code = 명령해석기.token_VALUE[명령해석기.시작점[argumento_INDEX] + Loop_INDEX]; if (character_code < '0' || character_code > '9' || pagpasok_COUNT > 10000) return -1; pagpasok_COUNT = pagpasok_COUNT * 10 + character_code - '0'; } return pagpasok_COUNT;
    }
    static void 세기() {
        int argumento_INDEX = 1, 선택번호 = 0;
        if (명령해석기.같음(1, "-c") || 명령해석기.같음(1, "-l") || 명령해석기.같음(1, "-w")) { 선택번호 = 명령해석기.같음(1, "-c") ? 1 : 명령해석기.같음(1, "-l") ? 2 : 3; argumento_INDEX++; }
        if (명령해석기.token_COUNT > argumento_INDEX + 1) { 명령해석기.sukat = 2; 단말.sumulat("사용법: wc [-c|-l|-w] [file]\n"); return; }
        if (!입력준비(argumento_INDEX)) return;
        int byte_COUNT = 0, 줄수 = 0, 낱말수 = 0, byte_data; boolean 낱말 = false;
        while ((byte_data = 읽기()) >= 0 && byte_data != 256) { byte_COUNT++; if (byte_data == 10) 줄수++; boolean SPACE = byte_data == 32 || byte_data >= 9 && byte_data <= 13; if (!SPACE && !낱말) 낱말수++; 낱말 = !SPACE; }
        isara(); if (byte_data < 0) { 명령해석기.error(byte_data); return; }
        if (선택번호 != 0) 단말.수(선택번호 == 1 ? byte_COUNT : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.수(줄수); 단말.문자(' '); 단말.수(낱말수); 단말.문자(' '); 단말.수(byte_COUNT); } 단말.문자(10);
    }
    static void FIND_pagpasok() {
        if (명령해석기.token_COUNT < 2 || 명령해석기.token_COUNT > 3) { 명령해석기.sukat = 2; 단말.sumulat("사용법: grep 찾을문구 [file]\n"); return; }
        if (!입력준비(2)) return;
        int pagpasok_COUNT = 0, byte_data, 일치수 = 0;
        while (true) {
            byte_data = 읽기();
            if (byte_data == 10 || byte_data == 256 || byte_data < 0) {
                boolean 찾은여부 = false;
                for (int Loop_INDEX = 0; Loop_INDEX <= pagpasok_COUNT - 명령해석기.haba_VALUE[1]; Loop_INDEX++) {
                    boolean 같은여부 = true; for (int inner_join_posisyon = 0; inner_join_posisyon < 명령해석기.haba_VALUE[1]; inner_join_posisyon++) if (data[Loop_INDEX + inner_join_posisyon] != 명령해석기.token_VALUE[명령해석기.시작점[1] + inner_join_posisyon]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (pagpasok_COUNT > 0 || byte_data == 10)) { for (int Loop_INDEX = 0; Loop_INDEX < pagpasok_COUNT; Loop_INDEX++) board.직렬쓰기(data[Loop_INDEX]); 단말.문자(10); 일치수++; }
                pagpasok_COUNT = 0; if (byte_data != 10) break;
            } else if (pagpasok_COUNT < data.length) data[pagpasok_COUNT++] = byte_data;
            else { 명령해석기.error(-28); isara(); return; }
        }
        isara(); if (byte_data < 0) 명령해석기.error(byte_data); else if (명령해석기.sukat == 0) 명령해석기.sukat = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int argumento_INDEX = 1, 줄수 = 10;
        if (명령해석기.같음(1, "-n")) { 줄수 = digit_VALUE(2); argumento_INDEX = 3; }
        if (줄수 < 0 || 명령해석기.token_COUNT > argumento_INDEX + 1) { 명령해석기.sukat = 2; 단말.sumulat("사용법: head/tail [-n 줄수] [file]\n"); return; }
        if (!입력준비(argumento_INDEX)) return;
        int pagpasok_COUNT = 0, byte_data;
        while ((byte_data = 읽기()) != 256 && byte_data >= 0) { if (pagpasok_COUNT == data.length) { 명령해석기.error(-28); isara(); return; } data[pagpasok_COUNT++] = byte_data; }
        isara(); if (byte_data < 0) { 명령해석기.error(byte_data); return; }
        int lokal_Start = 0, tapusin_posisyon = pagpasok_COUNT;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int 총수 = 0; for (int Loop_INDEX = pagpasok_COUNT - 2; Loop_INDEX >= 0; Loop_INDEX--) if (data[Loop_INDEX] == 10 && ++총수 == 줄수) { lokal_Start = Loop_INDEX + 1; break; } }
        else { int 총수 = 0; for (int Loop_INDEX = 0; Loop_INDEX < pagpasok_COUNT; Loop_INDEX++) if (data[Loop_INDEX] == 10 && ++총수 == 줄수) { tapusin_posisyon = Loop_INDEX + 1; break; } }
        for (int Loop_INDEX = lokal_Start; Loop_INDEX < tapusin_posisyon; Loop_INDEX++) board.직렬쓰기(data[Loop_INDEX]);
    }
    static void 함께쓰기() {
        boolean 덧붙임여부 = 명령해석기.같음(1, "-a"); int argumento_INDEX = 덧붙임여부 ? 2 : 1;
        if (명령해석기.token_COUNT != argumento_INDEX + 1) { 명령해석기.sukat = 2; 단말.sumulat("사용법: tee [-a] file\n"); return; }
        int 열린파일번호 = buksan_file(argumento_INDEX, 덧붙임여부 ? 1089 : 577); if (열린파일번호 < 0) { 명령해석기.error(열린파일번호); return; }
        입력파일 = -1; int byte_data;
        while ((byte_data = 읽기()) != 256 && byte_data >= 0) { int 처리값 = Memory_Mga_File.sumulat(열린파일번호, byte_data); if (처리값 < 0) { 명령해석기.error(처리값); break; } board.직렬쓰기(byte_data); }
        Memory_Mga_File.isara(열린파일번호);
    }
}
