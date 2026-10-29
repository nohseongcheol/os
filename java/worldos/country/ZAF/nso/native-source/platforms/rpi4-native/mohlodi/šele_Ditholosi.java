// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 šele 내장 Ditholosi. */
public final class šele_Ditholosi {
    static int[] data = new int[16384];
    static int 입력파일 = -1;
    static int bula_faele(int akumente_lokela, int tiragalo_mokgwa) {
        int 처리값 = 명령해석기.Tsejana(akumente_lokela); return 처리값 < 0 ? 처리값 : memori_Difaele.Bula(tiragalo_mokgwa);
    }
    static boolean 입력준비(int akumente_lokela) {
        입력파일 = -1;
        if (akumente_lokela < 명령해석기.토큰수) {
            입력파일 = bula_faele(akumente_lokela, 0);
            if (입력파일 < 0) { 명령해석기.Phošo(입력파일); return false; }
        }
        return true;
    }
    static int Bala() {
        if (입력파일 >= 3) return memori_Difaele.Bala(입력파일);
        while (true) {
            int paete_data = 보드.직렬읽기(); if (paete_data == -2 || paete_data == 4) return 256;
            if (paete_data == 3) { 명령해석기.결과 = 130; return 256; }
            if (paete_data >= 0) return paete_data; 보드.e_thibetšwe_CPU();
        }
    }
    static void Tswalela() { if (입력파일 >= 3) memori_Difaele.Tswalela(입력파일); 입력파일 = -1; }
    static void pogelo_boleng() {
        int 마지막자리 = 명령해석기.토큰수 == 1 ? 2 : 명령해석기.토큰수;
        for (int akumente_lokela = 1; akumente_lokela < 마지막자리; akumente_lokela++) {
            if (!입력준비(akumente_lokela)) continue;
            int paete_data; while ((paete_data = Bala()) != 256 && paete_data >= 0) 보드.직렬쓰기(paete_data);
            if (paete_data < 0) 명령해석기.Phošo(paete_data); Tswalela();
        }
    }
    static void faele_taba(String 동작번호) {
        if (명령해석기.토큰수 != 2) { 명령해석기.결과 = 2; 단말.Ngwala("사용법: mkdir/rmdir/touch Faele\n"); return; }
        int 처리값 = 명령해석기.Tsejana(1);
        if (처리값 >= 0) {
            if (동작번호.charAt(0) == 'm') 처리값 = memori_Difaele.폴더만들기();
            else if (동작번호.charAt(0) == 'r') 처리값 = memori_Difaele.tloša_lelokelelo();
            else { 처리값 = memori_Difaele.Bula(65); if (처리값 >= 3) 처리값 = memori_Difaele.Tswalela(처리값); }
        }
        if (처리값 < 0) 명령해석기.Phošo(처리값);
    }
    static void kopiša_boleng(boolean 이동여부) {
        if (명령해석기.토큰수 != 3) { 명령해석기.결과 = 2; 단말.Ngwala("사용법: cp/mv 원본 목적지 (Faele)\n"); return; }
        int 처리값 = 명령해석기.Tsejana(1); if (처리값 >= 0) 처리값 = memori_Difaele.fokotša_kopišo_boleng();
        if (처리값 < 0) { 명령해석기.Phošo(처리값); return; }
        int 원본번호 = memori_Difaele.hwetša_go_tsenya_tshedimošo(); if (원본번호 < 0) { 명령해석기.Phošo(-2); return; }
        int 항목수 = memori_Difaele.botelele_boleng[원본번호]; for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 항목수; ditaelopoeletšwa_lokela++) data[ditaelopoeletšwa_lokela] = memori_Difaele.자료읽기(원본번호, ditaelopoeletšwa_lokela);
        처리값 = 명령해석기.Tsejana(2); if (처리값 >= 0) 처리값 = memori_Difaele.fokotša_kopišo_boleng();
        if (처리값 < 0) { 명령해석기.Phošo(처리값); return; }
        if (memori_Difaele.hwetša_go_tsenya_tshedimošo() == 원본번호) { if (!이동여부) 명령해석기.Phošo(-22); return; }
        if (이동여부) { 처리값 = memori_Difaele.이름바꾸기(원본번호); if (처리값 < 0) 명령해석기.Phošo(처리값); return; }
        int 열린파일번호 = memori_Difaele.Bula(577); if (열린파일번호 < 0) { 명령해석기.Phošo(열린파일번호); return; }
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 항목수; ditaelopoeletšwa_lokela++) { 처리값 = memori_Difaele.Ngwala(열린파일번호, data[ditaelopoeletšwa_lokela]); if (처리값 < 0) { 명령해석기.Phošo(처리값); break; } }
        memori_Difaele.Tswalela(열린파일번호);
    }
    static int 숫자(int akumente_lokela) {
        if (akumente_lokela >= 명령해석기.토큰수) return -1;
        int 항목수 = 0; for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 명령해석기.botelele_boleng[akumente_lokela]; ditaelopoeletšwa_lokela++) { int khouto_ya_tlhaka = 명령해석기.thokene_boleng[명령해석기.시작점[akumente_lokela] + ditaelopoeletšwa_lokela]; if (khouto_ya_tlhaka < '0' || khouto_ya_tlhaka > '9' || 항목수 > 10000) return -1; 항목수 = 항목수 * 10 + khouto_ya_tlhaka - '0'; } return 항목수;
    }
    static void 세기() {
        int akumente_lokela = 1, 선택번호 = 0;
        if (명령해석기.같음(1, "-c") || 명령해석기.같음(1, "-l") || 명령해석기.같음(1, "-w")) { 선택번호 = 명령해석기.같음(1, "-c") ? 1 : 명령해석기.같음(1, "-l") ? 2 : 3; akumente_lokela++; }
        if (명령해석기.토큰수 > akumente_lokela + 1) { 명령해석기.결과 = 2; 단말.Ngwala("사용법: wc [-c|-l|-w] [Faele]\n"); return; }
        if (!입력준비(akumente_lokela)) return;
        int 바이트수 = 0, 줄수 = 0, 낱말수 = 0, paete_data; boolean 낱말 = false;
        while ((paete_data = Bala()) >= 0 && paete_data != 256) { 바이트수++; if (paete_data == 10) 줄수++; boolean sekgoba = paete_data == 32 || paete_data >= 9 && paete_data <= 13; if (!sekgoba && !낱말) 낱말수++; 낱말 = !sekgoba; }
        Tswalela(); if (paete_data < 0) { 명령해석기.Phošo(paete_data); return; }
        if (선택번호 != 0) 단말.수(선택번호 == 1 ? 바이트수 : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.수(줄수); 단말.문자(' '); 단말.수(낱말수); 단말.문자(' '); 단말.수(바이트수); } 단말.문자(10);
    }
    static void hwetša_go_tsenya_tshedimošo() {
        if (명령해석기.토큰수 < 2 || 명령해석기.토큰수 > 3) { 명령해석기.결과 = 2; 단말.Ngwala("사용법: grep 찾을문구 [Faele]\n"); return; }
        if (!입력준비(2)) return;
        int 항목수 = 0, paete_data, 일치수 = 0;
        while (true) {
            paete_data = Bala();
            if (paete_data == 10 || paete_data == 256 || paete_data < 0) {
                boolean 찾은여부 = false;
                for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela <= 항목수 - 명령해석기.botelele_boleng[1]; ditaelopoeletšwa_lokela++) {
                    boolean 같은여부 = true; for (int 안쪽자리 = 0; 안쪽자리 < 명령해석기.botelele_boleng[1]; 안쪽자리++) if (data[ditaelopoeletšwa_lokela + 안쪽자리] != 명령해석기.thokene_boleng[명령해석기.시작점[1] + 안쪽자리]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (항목수 > 0 || paete_data == 10)) { for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 항목수; ditaelopoeletšwa_lokela++) 보드.직렬쓰기(data[ditaelopoeletšwa_lokela]); 단말.문자(10); 일치수++; }
                항목수 = 0; if (paete_data != 10) break;
            } else if (항목수 < data.length) data[항목수++] = paete_data;
            else { 명령해석기.Phošo(-28); Tswalela(); return; }
        }
        Tswalela(); if (paete_data < 0) 명령해석기.Phošo(paete_data); else if (명령해석기.결과 == 0) 명령해석기.결과 = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int akumente_lokela = 1, 줄수 = 10;
        if (명령해석기.같음(1, "-n")) { 줄수 = 숫자(2); akumente_lokela = 3; }
        if (줄수 < 0 || 명령해석기.토큰수 > akumente_lokela + 1) { 명령해석기.결과 = 2; 단말.Ngwala("사용법: head/tail [-n 줄수] [Faele]\n"); return; }
        if (!입력준비(akumente_lokela)) return;
        int 항목수 = 0, paete_data;
        while ((paete_data = Bala()) != 256 && paete_data >= 0) { if (항목수 == data.length) { 명령해석기.Phošo(-28); Tswalela(); return; } data[항목수++] = paete_data; }
        Tswalela(); if (paete_data < 0) { 명령해석기.Phošo(paete_data); return; }
        int kgauswi_Thomišo = 0, 끝자리 = 항목수;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int 총수 = 0; for (int ditaelopoeletšwa_lokela = 항목수 - 2; ditaelopoeletšwa_lokela >= 0; ditaelopoeletšwa_lokela--) if (data[ditaelopoeletšwa_lokela] == 10 && ++총수 == 줄수) { kgauswi_Thomišo = ditaelopoeletšwa_lokela + 1; break; } }
        else { int 총수 = 0; for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 항목수; ditaelopoeletšwa_lokela++) if (data[ditaelopoeletšwa_lokela] == 10 && ++총수 == 줄수) { 끝자리 = ditaelopoeletšwa_lokela + 1; break; } }
        for (int ditaelopoeletšwa_lokela = kgauswi_Thomišo; ditaelopoeletšwa_lokela < 끝자리; ditaelopoeletšwa_lokela++) 보드.직렬쓰기(data[ditaelopoeletšwa_lokela]);
    }
    static void 함께쓰기() {
        boolean 덧붙임여부 = 명령해석기.같음(1, "-a"); int akumente_lokela = 덧붙임여부 ? 2 : 1;
        if (명령해석기.토큰수 != akumente_lokela + 1) { 명령해석기.결과 = 2; 단말.Ngwala("사용법: tee [-a] Faele\n"); return; }
        int 열린파일번호 = bula_faele(akumente_lokela, 덧붙임여부 ? 1089 : 577); if (열린파일번호 < 0) { 명령해석기.Phošo(열린파일번호); return; }
        입력파일 = -1; int paete_data;
        while ((paete_data = Bala()) != 256 && paete_data >= 0) { int 처리값 = memori_Difaele.Ngwala(열린파일번호, paete_data); if (처리값 < 0) { 명령해석기.Phošo(처리값); break; } 보드.직렬쓰기(paete_data); }
        memori_Difaele.Tswalela(열린파일번호);
    }
}
