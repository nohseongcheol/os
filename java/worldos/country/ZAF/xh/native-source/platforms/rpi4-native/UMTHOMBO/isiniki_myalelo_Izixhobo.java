// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 isiniki_myalelo 내장 Izixhobo. */
public final class isiniki_myalelo_Izixhobo {
    static int[] iingcombolo = new int[16384];
    static int 입력파일 = -1;
    static int vula_ifayile(int isiniki_myalelo_indeksa, int Inkqubo_imo) {
        int 처리값 = 명령해석기.INDLELA(isiniki_myalelo_indeksa); return 처리값 < 0 ? 처리값 : imemori_Iifayile.Vula(Inkqubo_imo);
    }
    static boolean 입력준비(int isiniki_myalelo_indeksa) {
        입력파일 = -1;
        if (isiniki_myalelo_indeksa < 명령해석기.토큰수) {
            입력파일 = vula_ifayile(isiniki_myalelo_indeksa, 0);
            if (입력파일 < 0) { 명령해석기.Impazamo(입력파일); return false; }
        }
        return true;
    }
    static int Funda() {
        if (입력파일 >= 3) return imemori_Iifayile.Funda(입력파일);
        while (true) {
            int ibhayithi_iingcombolo = 보드.직렬읽기(); if (ibhayithi_iingcombolo == -2 || ibhayithi_iingcombolo == 4) return 256;
            if (ibhayithi_iingcombolo == 3) { 명령해석기.결과 = 130; return 256; }
            if (ibhayithi_iingcombolo >= 0) return ibhayithi_iingcombolo; 보드.misa_okwexeshana_i_CPU();
        }
    }
    static void Vala() { if (입력파일 >= 3) imemori_Iifayile.Vala(입력파일); 입력파일 = -1; }
    static void bona_ixabiso() {
        int 마지막자리 = 명령해석기.토큰수 == 1 ? 2 : 명령해석기.토큰수;
        for (int isiniki_myalelo_indeksa = 1; isiniki_myalelo_indeksa < 마지막자리; isiniki_myalelo_indeksa++) {
            if (!입력준비(isiniki_myalelo_indeksa)) continue;
            int ibhayithi_iingcombolo; while ((ibhayithi_iingcombolo = Funda()) != 256 && ibhayithi_iingcombolo >= 0) 보드.직렬쓰기(ibhayithi_iingcombolo);
            if (ibhayithi_iingcombolo < 0) 명령해석기.Impazamo(ibhayithi_iingcombolo); Vala();
        }
    }
    static void ifayile_isiganeko(String 동작번호) {
        if (명령해석기.토큰수 != 2) { 명령해석기.결과 = 2; 단말.Bhala("사용법: mkdir/rmdir/touch iFayili\n"); return; }
        int 처리값 = 명령해석기.INDLELA(1);
        if (처리값 >= 0) {
            if (동작번호.charAt(0) == 'm') 처리값 = imemori_Iifayile.yila_isalathisi();
            else if (동작번호.charAt(0) == 'r') 처리값 = imemori_Iifayile.shenxisa_isalathisi();
            else { 처리값 = imemori_Iifayile.Vula(65); if (처리값 >= 3) 처리값 = imemori_Iifayile.Vala(처리값); }
        }
        if (처리값 < 0) 명령해석기.Impazamo(처리값);
    }
    static void kopa_ixabiso(boolean 이동여부) {
        if (명령해석기.토큰수 != 3) { 명령해석기.결과 = 2; 단말.Bhala("사용법: cp/mv 원본 목적지 (iFayili)\n"); return; }
        int 처리값 = 명령해석기.INDLELA(1); if (처리값 >= 0) 처리값 = imemori_Iifayile.qhelekisa_ixabiso();
        if (처리값 < 0) { 명령해석기.Impazamo(처리값); return; }
        int 원본번호 = imemori_Iifayile.fumana_ufako_nkcukacha(); if (원본번호 < 0) { 명령해석기.Impazamo(-2); return; }
        int 항목수 = imemori_Iifayile.ubude_ixabiso[원본번호]; for (int iluphu_indeksa = 0; iluphu_indeksa < 항목수; iluphu_indeksa++) iingcombolo[iluphu_indeksa] = imemori_Iifayile.자료읽기(원본번호, iluphu_indeksa);
        처리값 = 명령해석기.INDLELA(2); if (처리값 >= 0) 처리값 = imemori_Iifayile.qhelekisa_ixabiso();
        if (처리값 < 0) { 명령해석기.Impazamo(처리값); return; }
        if (imemori_Iifayile.fumana_ufako_nkcukacha() == 원본번호) { if (!이동여부) 명령해석기.Impazamo(-22); return; }
        if (이동여부) { 처리값 = imemori_Iifayile.이름바꾸기(원본번호); if (처리값 < 0) 명령해석기.Impazamo(처리값); return; }
        int 열린파일번호 = imemori_Iifayile.Vula(577); if (열린파일번호 < 0) { 명령해석기.Impazamo(열린파일번호); return; }
        for (int iluphu_indeksa = 0; iluphu_indeksa < 항목수; iluphu_indeksa++) { 처리값 = imemori_Iifayile.Bhala(열린파일번호, iingcombolo[iluphu_indeksa]); if (처리값 < 0) { 명령해석기.Impazamo(처리값); break; } }
        imemori_Iifayile.Vala(열린파일번호);
    }
    static int inani_ixabiso(int isiniki_myalelo_indeksa) {
        if (isiniki_myalelo_indeksa >= 명령해석기.토큰수) return -1;
        int 항목수 = 0; for (int iluphu_indeksa = 0; iluphu_indeksa < 명령해석기.ubude_ixabiso[isiniki_myalelo_indeksa]; iluphu_indeksa++) { int ikhowudi_yekharakhtha = 명령해석기.ithokeni_ixabiso[명령해석기.시작점[isiniki_myalelo_indeksa] + iluphu_indeksa]; if (ikhowudi_yekharakhtha < '0' || ikhowudi_yekharakhtha > '9' || 항목수 > 10000) return -1; 항목수 = 항목수 * 10 + ikhowudi_yekharakhtha - '0'; } return 항목수;
    }
    static void 세기() {
        int isiniki_myalelo_indeksa = 1, 선택번호 = 0;
        if (명령해석기.같음(1, "-c") || 명령해석기.같음(1, "-l") || 명령해석기.같음(1, "-w")) { 선택번호 = 명령해석기.같음(1, "-c") ? 1 : 명령해석기.같음(1, "-l") ? 2 : 3; isiniki_myalelo_indeksa++; }
        if (명령해석기.토큰수 > isiniki_myalelo_indeksa + 1) { 명령해석기.결과 = 2; 단말.Bhala("사용법: wc [-c|-l|-w] [iFayili]\n"); return; }
        if (!입력준비(isiniki_myalelo_indeksa)) return;
        int 바이트수 = 0, 줄수 = 0, 낱말수 = 0, ibhayithi_iingcombolo; boolean 낱말 = false;
        while ((ibhayithi_iingcombolo = Funda()) >= 0 && ibhayithi_iingcombolo != 256) { 바이트수++; if (ibhayithi_iingcombolo == 10) 줄수++; boolean isithuba = ibhayithi_iingcombolo == 32 || ibhayithi_iingcombolo >= 9 && ibhayithi_iingcombolo <= 13; if (!isithuba && !낱말) 낱말수++; 낱말 = !isithuba; }
        Vala(); if (ibhayithi_iingcombolo < 0) { 명령해석기.Impazamo(ibhayithi_iingcombolo); return; }
        if (선택번호 != 0) 단말.수(선택번호 == 1 ? 바이트수 : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.수(줄수); 단말.문자(' '); 단말.수(낱말수); 단말.문자(' '); 단말.수(바이트수); } 단말.문자(10);
    }
    static void fumana_ufako_nkcukacha() {
        if (명령해석기.토큰수 < 2 || 명령해석기.토큰수 > 3) { 명령해석기.결과 = 2; 단말.Bhala("사용법: grep 찾을문구 [iFayili]\n"); return; }
        if (!입력준비(2)) return;
        int 항목수 = 0, ibhayithi_iingcombolo, 일치수 = 0;
        while (true) {
            ibhayithi_iingcombolo = Funda();
            if (ibhayithi_iingcombolo == 10 || ibhayithi_iingcombolo == 256 || ibhayithi_iingcombolo < 0) {
                boolean 찾은여부 = false;
                for (int iluphu_indeksa = 0; iluphu_indeksa <= 항목수 - 명령해석기.ubude_ixabiso[1]; iluphu_indeksa++) {
                    boolean 같은여부 = true; for (int 안쪽자리 = 0; 안쪽자리 < 명령해석기.ubude_ixabiso[1]; 안쪽자리++) if (iingcombolo[iluphu_indeksa + 안쪽자리] != 명령해석기.ithokeni_ixabiso[명령해석기.시작점[1] + 안쪽자리]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (항목수 > 0 || ibhayithi_iingcombolo == 10)) { for (int iluphu_indeksa = 0; iluphu_indeksa < 항목수; iluphu_indeksa++) 보드.직렬쓰기(iingcombolo[iluphu_indeksa]); 단말.문자(10); 일치수++; }
                항목수 = 0; if (ibhayithi_iingcombolo != 10) break;
            } else if (항목수 < iingcombolo.length) iingcombolo[항목수++] = ibhayithi_iingcombolo;
            else { 명령해석기.Impazamo(-28); Vala(); return; }
        }
        Vala(); if (ibhayithi_iingcombolo < 0) 명령해석기.Impazamo(ibhayithi_iingcombolo); else if (명령해석기.결과 == 0) 명령해석기.결과 = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int isiniki_myalelo_indeksa = 1, 줄수 = 10;
        if (명령해석기.같음(1, "-n")) { 줄수 = inani_ixabiso(2); isiniki_myalelo_indeksa = 3; }
        if (줄수 < 0 || 명령해석기.토큰수 > isiniki_myalelo_indeksa + 1) { 명령해석기.결과 = 2; 단말.Bhala("사용법: head/tail [-n 줄수] [iFayili]\n"); return; }
        if (!입력준비(isiniki_myalelo_indeksa)) return;
        int 항목수 = 0, ibhayithi_iingcombolo;
        while ((ibhayithi_iingcombolo = Funda()) != 256 && ibhayithi_iingcombolo >= 0) { if (항목수 == iingcombolo.length) { 명령해석기.Impazamo(-28); Vala(); return; } iingcombolo[항목수++] = ibhayithi_iingcombolo; }
        Vala(); if (ibhayithi_iingcombolo < 0) { 명령해석기.Impazamo(ibhayithi_iingcombolo); return; }
        int eyale_ndawo_qala = 0, 끝자리 = 항목수;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int 총수 = 0; for (int iluphu_indeksa = 항목수 - 2; iluphu_indeksa >= 0; iluphu_indeksa--) if (iingcombolo[iluphu_indeksa] == 10 && ++총수 == 줄수) { eyale_ndawo_qala = iluphu_indeksa + 1; break; } }
        else { int 총수 = 0; for (int iluphu_indeksa = 0; iluphu_indeksa < 항목수; iluphu_indeksa++) if (iingcombolo[iluphu_indeksa] == 10 && ++총수 == 줄수) { 끝자리 = iluphu_indeksa + 1; break; } }
        for (int iluphu_indeksa = eyale_ndawo_qala; iluphu_indeksa < 끝자리; iluphu_indeksa++) 보드.직렬쓰기(iingcombolo[iluphu_indeksa]);
    }
    static void 함께쓰기() {
        boolean 덧붙임여부 = 명령해석기.같음(1, "-a"); int isiniki_myalelo_indeksa = 덧붙임여부 ? 2 : 1;
        if (명령해석기.토큰수 != isiniki_myalelo_indeksa + 1) { 명령해석기.결과 = 2; 단말.Bhala("사용법: tee [-a] iFayili\n"); return; }
        int 열린파일번호 = vula_ifayile(isiniki_myalelo_indeksa, 덧붙임여부 ? 1089 : 577); if (열린파일번호 < 0) { 명령해석기.Impazamo(열린파일번호); return; }
        입력파일 = -1; int ibhayithi_iingcombolo;
        while ((ibhayithi_iingcombolo = Funda()) != 256 && ibhayithi_iingcombolo >= 0) { int 처리값 = imemori_Iifayile.Bhala(열린파일번호, ibhayithi_iingcombolo); if (처리값 < 0) { 명령해석기.Impazamo(처리값); break; } 보드.직렬쓰기(ibhayithi_iingcombolo); }
        imemori_Iifayile.Vala(열린파일번호);
    }
}
