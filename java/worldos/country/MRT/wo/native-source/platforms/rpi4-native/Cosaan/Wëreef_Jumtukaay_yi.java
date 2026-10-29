// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 Wëreef 내장 Jumtukaay_yi. */
public final class Wëreef_Jumtukaay_yi {
    static int[] mbir = new int[16384];
    static int 입력파일 = -1;
    static int sos_bara_denc(int Tegtal_àlluwa_tur, int yokkute_anam) {
        int 처리값 = 명령해석기.Yoonu_jëmale(Tegtal_àlluwa_tur); return 처리값 < 0 ? 처리값 : fatlekookaay_Fisiye_yi.sos(yokkute_anam);
    }
    static boolean 입력준비(int Tegtal_àlluwa_tur) {
        입력파일 = -1;
        if (Tegtal_àlluwa_tur < 명령해석기.토큰수) {
            입력파일 = sos_bara_denc(Tegtal_àlluwa_tur, 0);
            if (입력파일 < 0) { 명령해석기.njumte(입력파일); return false; }
        }
        return true;
    }
    static int 읽기() {
        if (입력파일 >= 3) return fatlekookaay_Fisiye_yi.읽기(입력파일);
        while (true) {
            int okte_mbir = 보드.직렬읽기(); if (okte_mbir == -2 || okte_mbir == 4) return 256;
            if (okte_mbir == 3) { 명령해석기.결과 = 130; return 256; }
            if (okte_mbir >= 0) return okte_mbir; 보드.dakkal_UC();
        }
    }
    static void Tej() { if (입력파일 >= 3) fatlekookaay_Fisiye_yi.Tej(입력파일); 입력파일 = -1; }
    static void wonin_xëyma() {
        int 마지막자리 = 명령해석기.토큰수 == 1 ? 2 : 명령해석기.토큰수;
        for (int Tegtal_àlluwa_tur = 1; Tegtal_àlluwa_tur < 마지막자리; Tegtal_àlluwa_tur++) {
            if (!입력준비(Tegtal_àlluwa_tur)) continue;
            int okte_mbir; while ((okte_mbir = 읽기()) != 256 && okte_mbir >= 0) 보드.직렬쓰기(okte_mbir);
            if (okte_mbir < 0) 명령해석기.njumte(okte_mbir); Tej();
        }
    }
    static void bara_denc_ay(String 동작번호) {
        if (명령해석기.토큰수 != 2) { 명령해석기.결과 = 2; 단말.biir("사용법: mkdir/rmdir/touch bara_denc\n"); return; }
        int 처리값 = 명령해석기.Yoonu_jëmale(1);
        if (처리값 >= 0) {
            if (동작번호.charAt(0) == 'm') 처리값 = fatlekookaay_Fisiye_yi.sos_dàmb();
            else if (동작번호.charAt(0) == 'r') 처리값 = fatlekookaay_Fisiye_yi.dandal_dàmb();
            else { 처리값 = fatlekookaay_Fisiye_yi.sos(65); if (처리값 >= 3) 처리값 = fatlekookaay_Fisiye_yi.Tej(처리값); }
        }
        if (처리값 < 0) 명령해석기.njumte(처리값);
    }
    static void mbokk_xëyma(boolean 이동여부) {
        if (명령해석기.토큰수 != 3) { 명령해석기.결과 = 2; 단말.biir("사용법: cp/mv 원본 목적지 (bara_denc)\n"); return; }
        int 처리값 = 명령해석기.Yoonu_jëmale(1); if (처리값 >= 0) 처리값 = fatlekookaay_Fisiye_yi.yonnal_xëyma();
        if (처리값 < 0) { 명령해석기.njumte(처리값); return; }
        int 원본번호 = fatlekookaay_Fisiye_yi.seet_dugal_xabaar(); if (원본번호 < 0) { 명령해석기.njumte(-2); return; }
        int 항목수 = fatlekookaay_Fisiye_yi.diir_xëyma[원본번호]; for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 항목수; wërngël_àlluwa_tur++) mbir[wërngël_àlluwa_tur] = fatlekookaay_Fisiye_yi.자료읽기(원본번호, wërngël_àlluwa_tur);
        처리값 = 명령해석기.Yoonu_jëmale(2); if (처리값 >= 0) 처리값 = fatlekookaay_Fisiye_yi.yonnal_xëyma();
        if (처리값 < 0) { 명령해석기.njumte(처리값); return; }
        if (fatlekookaay_Fisiye_yi.seet_dugal_xabaar() == 원본번호) { if (!이동여부) 명령해석기.njumte(-22); return; }
        if (이동여부) { 처리값 = fatlekookaay_Fisiye_yi.이름바꾸기(원본번호); if (처리값 < 0) 명령해석기.njumte(처리값); return; }
        int 열린파일번호 = fatlekookaay_Fisiye_yi.sos(577); if (열린파일번호 < 0) { 명령해석기.njumte(열린파일번호); return; }
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 항목수; wërngël_àlluwa_tur++) { 처리값 = fatlekookaay_Fisiye_yi.biir(열린파일번호, mbir[wërngël_àlluwa_tur]); if (처리값 < 0) { 명령해석기.njumte(처리값); break; } }
        fatlekookaay_Fisiye_yi.Tej(열린파일번호);
    }
    static int siifar_xëyma(int Tegtal_àlluwa_tur) {
        if (Tegtal_àlluwa_tur >= 명령해석기.토큰수) return -1;
        int 항목수 = 0; for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 명령해석기.diir_xëyma[Tegtal_àlluwa_tur]; wërngël_àlluwa_tur++) { int kotu_araf = 명령해석기.jeton_xëyma[명령해석기.시작점[Tegtal_àlluwa_tur] + wërngël_àlluwa_tur]; if (kotu_araf < '0' || kotu_araf > '9' || 항목수 > 10000) return -1; 항목수 = 항목수 * 10 + kotu_araf - '0'; } return 항목수;
    }
    static void 세기() {
        int Tegtal_àlluwa_tur = 1, 선택번호 = 0;
        if (명령해석기.같음(1, "-c") || 명령해석기.같음(1, "-l") || 명령해석기.같음(1, "-w")) { 선택번호 = 명령해석기.같음(1, "-c") ? 1 : 명령해석기.같음(1, "-l") ? 2 : 3; Tegtal_àlluwa_tur++; }
        if (명령해석기.토큰수 > Tegtal_àlluwa_tur + 1) { 명령해석기.결과 = 2; 단말.biir("사용법: wc [-c|-l|-w] [bara_denc]\n"); return; }
        if (!입력준비(Tegtal_àlluwa_tur)) return;
        int 바이트수 = 0, 줄수 = 0, 낱말수 = 0, okte_mbir; boolean 낱말 = false;
        while ((okte_mbir = 읽기()) >= 0 && okte_mbir != 256) { 바이트수++; if (okte_mbir == 10) 줄수++; boolean Espace = okte_mbir == 32 || okte_mbir >= 9 && okte_mbir <= 13; if (!Espace && !낱말) 낱말수++; 낱말 = !Espace; }
        Tej(); if (okte_mbir < 0) { 명령해석기.njumte(okte_mbir); return; }
        if (선택번호 != 0) 단말.수(선택번호 == 1 ? 바이트수 : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.수(줄수); 단말.문자(' '); 단말.수(낱말수); 단말.문자(' '); 단말.수(바이트수); } 단말.문자(10);
    }
    static void seet_dugal_xabaar() {
        if (명령해석기.토큰수 < 2 || 명령해석기.토큰수 > 3) { 명령해석기.결과 = 2; 단말.biir("사용법: grep 찾을문구 [bara_denc]\n"); return; }
        if (!입력준비(2)) return;
        int 항목수 = 0, okte_mbir, 일치수 = 0;
        while (true) {
            okte_mbir = 읽기();
            if (okte_mbir == 10 || okte_mbir == 256 || okte_mbir < 0) {
                boolean 찾은여부 = false;
                for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur <= 항목수 - 명령해석기.diir_xëyma[1]; wërngël_àlluwa_tur++) {
                    boolean 같은여부 = true; for (int 안쪽자리 = 0; 안쪽자리 < 명령해석기.diir_xëyma[1]; 안쪽자리++) if (mbir[wërngël_àlluwa_tur + 안쪽자리] != 명령해석기.jeton_xëyma[명령해석기.시작점[1] + 안쪽자리]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (항목수 > 0 || okte_mbir == 10)) { for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 항목수; wërngël_àlluwa_tur++) 보드.직렬쓰기(mbir[wërngël_àlluwa_tur]); 단말.문자(10); 일치수++; }
                항목수 = 0; if (okte_mbir != 10) break;
            } else if (항목수 < mbir.length) mbir[항목수++] = okte_mbir;
            else { 명령해석기.njumte(-28); Tej(); return; }
        }
        Tej(); if (okte_mbir < 0) 명령해석기.njumte(okte_mbir); else if (명령해석기.결과 == 0) 명령해석기.결과 = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int Tegtal_àlluwa_tur = 1, 줄수 = 10;
        if (명령해석기.같음(1, "-n")) { 줄수 = siifar_xëyma(2); Tegtal_àlluwa_tur = 3; }
        if (줄수 < 0 || 명령해석기.토큰수 > Tegtal_àlluwa_tur + 1) { 명령해석기.결과 = 2; 단말.biir("사용법: head/tail [-n 줄수] [bara_denc]\n"); return; }
        if (!입력준비(Tegtal_àlluwa_tur)) return;
        int 항목수 = 0, okte_mbir;
        while ((okte_mbir = 읽기()) != 256 && okte_mbir >= 0) { if (항목수 == mbir.length) { 명령해석기.njumte(-28); Tej(); return; } mbir[항목수++] = okte_mbir; }
        Tej(); if (okte_mbir < 0) { 명령해석기.njumte(okte_mbir); return; }
        int dënnd_Door = 0, 끝자리 = 항목수;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int 총수 = 0; for (int wërngël_àlluwa_tur = 항목수 - 2; wërngël_àlluwa_tur >= 0; wërngël_àlluwa_tur--) if (mbir[wërngël_àlluwa_tur] == 10 && ++총수 == 줄수) { dënnd_Door = wërngël_àlluwa_tur + 1; break; } }
        else { int 총수 = 0; for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 항목수; wërngël_àlluwa_tur++) if (mbir[wërngël_àlluwa_tur] == 10 && ++총수 == 줄수) { 끝자리 = wërngël_àlluwa_tur + 1; break; } }
        for (int wërngël_àlluwa_tur = dënnd_Door; wërngël_àlluwa_tur < 끝자리; wërngël_àlluwa_tur++) 보드.직렬쓰기(mbir[wërngël_àlluwa_tur]);
    }
    static void 함께쓰기() {
        boolean 덧붙임여부 = 명령해석기.같음(1, "-a"); int Tegtal_àlluwa_tur = 덧붙임여부 ? 2 : 1;
        if (명령해석기.토큰수 != Tegtal_àlluwa_tur + 1) { 명령해석기.결과 = 2; 단말.biir("사용법: tee [-a] bara_denc\n"); return; }
        int 열린파일번호 = sos_bara_denc(Tegtal_àlluwa_tur, 덧붙임여부 ? 1089 : 577); if (열린파일번호 < 0) { 명령해석기.njumte(열린파일번호); return; }
        입력파일 = -1; int okte_mbir;
        while ((okte_mbir = 읽기()) != 256 && okte_mbir >= 0) { int 처리값 = fatlekookaay_Fisiye_yi.biir(열린파일번호, okte_mbir); if (처리값 < 0) { 명령해석기.njumte(처리값); break; } 보드.직렬쓰기(okte_mbir); }
        fatlekookaay_Fisiye_yi.Tej(열린파일번호);
    }
}
