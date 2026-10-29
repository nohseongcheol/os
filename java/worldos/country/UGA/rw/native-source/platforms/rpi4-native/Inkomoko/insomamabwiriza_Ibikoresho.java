// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 insomamabwiriza 내장 Ibikoresho. */
public final class insomamabwiriza_Ibikoresho {
    static int[] amakurushingiro = new int[16384];
    static int 입력파일 = -1;
    static int kurema_dosiye(int ingingo_umugerekashakiro, int Inzira_uburyo) {
        int 처리값 = 명령해석기.Inzira(ingingo_umugerekashakiro); return 처리값 < 0 ? 처리값 : ububiko_Dosiye.Gufungura(Inzira_uburyo);
    }
    static boolean 입력준비(int ingingo_umugerekashakiro) {
        입력파일 = -1;
        if (ingingo_umugerekashakiro < 명령해석기.토큰수) {
            입력파일 = kurema_dosiye(ingingo_umugerekashakiro, 0);
            if (입력파일 < 0) { 명령해석기.IKOSA(입력파일); return false; }
        }
        return true;
    }
    static int 읽기() {
        if (입력파일 >= 3) return ububiko_Dosiye.읽기(입력파일);
        while (true) {
            int bayiti_amakurushingiro = 보드.직렬읽기(); if (bayiti_amakurushingiro == -2 || bayiti_amakurushingiro == 4) return 256;
            if (bayiti_amakurushingiro == 3) { 명령해석기.결과 = 130; return 256; }
            if (bayiti_amakurushingiro >= 0) return bayiti_amakurushingiro; 보드.gusubika_CPU();
        }
    }
    static void Gufunga() { if (입력파일 >= 3) ububiko_Dosiye.Gufunga(입력파일); 입력파일 = -1; }
    static void igaragaza_agaciro() {
        int 마지막자리 = 명령해석기.토큰수 == 1 ? 2 : 명령해석기.토큰수;
        for (int ingingo_umugerekashakiro = 1; ingingo_umugerekashakiro < 마지막자리; ingingo_umugerekashakiro++) {
            if (!입력준비(ingingo_umugerekashakiro)) continue;
            int bayiti_amakurushingiro; while ((bayiti_amakurushingiro = 읽기()) != 256 && bayiti_amakurushingiro >= 0) 보드.직렬쓰기(bayiti_amakurushingiro);
            if (bayiti_amakurushingiro < 0) 명령해석기.IKOSA(bayiti_amakurushingiro); Gufunga();
        }
    }
    static void dosiye_ikibazo(String 동작번호) {
        if (명령해석기.토큰수 != 2) { 명령해석기.결과 = 2; 단말.kwandika("사용법: mkdir/rmdir/touch Idosiye\n"); return; }
        int 처리값 = 명령해석기.Inzira(1);
        if (처리값 >= 0) {
            if (동작번호.charAt(0) == 'm') 처리값 = ububiko_Dosiye.kurema_ububiko();
            else if (동작번호.charAt(0) == 'r') 처리값 = ububiko_Dosiye.gukuramo_ububiko();
            else { 처리값 = ububiko_Dosiye.Gufungura(65); if (처리값 >= 3) 처리값 = ububiko_Dosiye.Gufunga(처리값); }
        }
        if (처리값 < 0) 명령해석기.IKOSA(처리값);
    }
    static void kopi_agaciro(boolean 이동여부) {
        if (명령해석기.토큰수 != 3) { 명령해석기.결과 = 2; 단말.kwandika("사용법: cp/mv 원본 목적지 (Idosiye)\n"); return; }
        int 처리값 = 명령해석기.Inzira(1); if (처리값 >= 0) 처리값 = ububiko_Dosiye.kuboneza_agaciro();
        if (처리값 < 0) { 명령해석기.IKOSA(처리값); return; }
        int 원본번호 = ububiko_Dosiye.gushaka_icyinjizwa(); if (원본번호 < 0) { 명령해석기.IKOSA(-2); return; }
        int 항목수 = ububiko_Dosiye.uburebure_agaciro[원본번호]; for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 항목수; gukora_mu_matsinda_umugerekashakiro++) amakurushingiro[gukora_mu_matsinda_umugerekashakiro] = ububiko_Dosiye.자료읽기(원본번호, gukora_mu_matsinda_umugerekashakiro);
        처리값 = 명령해석기.Inzira(2); if (처리값 >= 0) 처리값 = ububiko_Dosiye.kuboneza_agaciro();
        if (처리값 < 0) { 명령해석기.IKOSA(처리값); return; }
        if (ububiko_Dosiye.gushaka_icyinjizwa() == 원본번호) { if (!이동여부) 명령해석기.IKOSA(-22); return; }
        if (이동여부) { 처리값 = ububiko_Dosiye.이름바꾸기(원본번호); if (처리값 < 0) 명령해석기.IKOSA(처리값); return; }
        int 열린파일번호 = ububiko_Dosiye.Gufungura(577); if (열린파일번호 < 0) { 명령해석기.IKOSA(열린파일번호); return; }
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 항목수; gukora_mu_matsinda_umugerekashakiro++) { 처리값 = ububiko_Dosiye.kwandika(열린파일번호, amakurushingiro[gukora_mu_matsinda_umugerekashakiro]); if (처리값 < 0) { 명령해석기.IKOSA(처리값); break; } }
        ububiko_Dosiye.Gufunga(열린파일번호);
    }
    static int umubare_agaciro(int ingingo_umugerekashakiro) {
        if (ingingo_umugerekashakiro >= 명령해석기.토큰수) return -1;
        int 항목수 = 0; for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 명령해석기.uburebure_agaciro[ingingo_umugerekashakiro]; gukora_mu_matsinda_umugerekashakiro++) { int 문자값 = 명령해석기.tike_agaciro[명령해석기.시작점[ingingo_umugerekashakiro] + gukora_mu_matsinda_umugerekashakiro]; if (문자값 < '0' || 문자값 > '9' || 항목수 > 10000) return -1; 항목수 = 항목수 * 10 + 문자값 - '0'; } return 항목수;
    }
    static void 세기() {
        int ingingo_umugerekashakiro = 1, 선택번호 = 0;
        if (명령해석기.같음(1, "-c") || 명령해석기.같음(1, "-l") || 명령해석기.같음(1, "-w")) { 선택번호 = 명령해석기.같음(1, "-c") ? 1 : 명령해석기.같음(1, "-l") ? 2 : 3; ingingo_umugerekashakiro++; }
        if (명령해석기.토큰수 > ingingo_umugerekashakiro + 1) { 명령해석기.결과 = 2; 단말.kwandika("사용법: wc [-c|-l|-w] [Idosiye]\n"); return; }
        if (!입력준비(ingingo_umugerekashakiro)) return;
        int 바이트수 = 0, 줄수 = 0, 낱말수 = 0, bayiti_amakurushingiro; boolean 낱말 = false;
        while ((bayiti_amakurushingiro = 읽기()) >= 0 && bayiti_amakurushingiro != 256) { 바이트수++; if (bayiti_amakurushingiro == 10) 줄수++; boolean akanya = bayiti_amakurushingiro == 32 || bayiti_amakurushingiro >= 9 && bayiti_amakurushingiro <= 13; if (!akanya && !낱말) 낱말수++; 낱말 = !akanya; }
        Gufunga(); if (bayiti_amakurushingiro < 0) { 명령해석기.IKOSA(bayiti_amakurushingiro); return; }
        if (선택번호 != 0) 단말.수(선택번호 == 1 ? 바이트수 : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.수(줄수); 단말.문자(' '); 단말.수(낱말수); 단말.문자(' '); 단말.수(바이트수); } 단말.문자(10);
    }
    static void gushaka_icyinjizwa() {
        if (명령해석기.토큰수 < 2 || 명령해석기.토큰수 > 3) { 명령해석기.결과 = 2; 단말.kwandika("사용법: grep 찾을문구 [Idosiye]\n"); return; }
        if (!입력준비(2)) return;
        int 항목수 = 0, bayiti_amakurushingiro, 일치수 = 0;
        while (true) {
            bayiti_amakurushingiro = 읽기();
            if (bayiti_amakurushingiro == 10 || bayiti_amakurushingiro == 256 || bayiti_amakurushingiro < 0) {
                boolean 찾은여부 = false;
                for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro <= 항목수 - 명령해석기.uburebure_agaciro[1]; gukora_mu_matsinda_umugerekashakiro++) {
                    boolean 같은여부 = true; for (int 안쪽자리 = 0; 안쪽자리 < 명령해석기.uburebure_agaciro[1]; 안쪽자리++) if (amakurushingiro[gukora_mu_matsinda_umugerekashakiro + 안쪽자리] != 명령해석기.tike_agaciro[명령해석기.시작점[1] + 안쪽자리]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (항목수 > 0 || bayiti_amakurushingiro == 10)) { for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 항목수; gukora_mu_matsinda_umugerekashakiro++) 보드.직렬쓰기(amakurushingiro[gukora_mu_matsinda_umugerekashakiro]); 단말.문자(10); 일치수++; }
                항목수 = 0; if (bayiti_amakurushingiro != 10) break;
            } else if (항목수 < amakurushingiro.length) amakurushingiro[항목수++] = bayiti_amakurushingiro;
            else { 명령해석기.IKOSA(-28); Gufunga(); return; }
        }
        Gufunga(); if (bayiti_amakurushingiro < 0) 명령해석기.IKOSA(bayiti_amakurushingiro); else if (명령해석기.결과 == 0) 명령해석기.결과 = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int ingingo_umugerekashakiro = 1, 줄수 = 10;
        if (명령해석기.같음(1, "-n")) { 줄수 = umubare_agaciro(2); ingingo_umugerekashakiro = 3; }
        if (줄수 < 0 || 명령해석기.토큰수 > ingingo_umugerekashakiro + 1) { 명령해석기.결과 = 2; 단말.kwandika("사용법: head/tail [-n 줄수] [Idosiye]\n"); return; }
        if (!입력준비(ingingo_umugerekashakiro)) return;
        int 항목수 = 0, bayiti_amakurushingiro;
        while ((bayiti_amakurushingiro = 읽기()) != 256 && bayiti_amakurushingiro >= 0) { if (항목수 == amakurushingiro.length) { 명령해석기.IKOSA(-28); Gufunga(); return; } amakurushingiro[항목수++] = bayiti_amakurushingiro; }
        Gufunga(); if (bayiti_amakurushingiro < 0) { 명령해석기.IKOSA(bayiti_amakurushingiro); return; }
        int mu_gace_Itangira = 0, 끝자리 = 항목수;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int 총수 = 0; for (int gukora_mu_matsinda_umugerekashakiro = 항목수 - 2; gukora_mu_matsinda_umugerekashakiro >= 0; gukora_mu_matsinda_umugerekashakiro--) if (amakurushingiro[gukora_mu_matsinda_umugerekashakiro] == 10 && ++총수 == 줄수) { mu_gace_Itangira = gukora_mu_matsinda_umugerekashakiro + 1; break; } }
        else { int 총수 = 0; for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 항목수; gukora_mu_matsinda_umugerekashakiro++) if (amakurushingiro[gukora_mu_matsinda_umugerekashakiro] == 10 && ++총수 == 줄수) { 끝자리 = gukora_mu_matsinda_umugerekashakiro + 1; break; } }
        for (int gukora_mu_matsinda_umugerekashakiro = mu_gace_Itangira; gukora_mu_matsinda_umugerekashakiro < 끝자리; gukora_mu_matsinda_umugerekashakiro++) 보드.직렬쓰기(amakurushingiro[gukora_mu_matsinda_umugerekashakiro]);
    }
    static void 함께쓰기() {
        boolean 덧붙임여부 = 명령해석기.같음(1, "-a"); int ingingo_umugerekashakiro = 덧붙임여부 ? 2 : 1;
        if (명령해석기.토큰수 != ingingo_umugerekashakiro + 1) { 명령해석기.결과 = 2; 단말.kwandika("사용법: tee [-a] Idosiye\n"); return; }
        int 열린파일번호 = kurema_dosiye(ingingo_umugerekashakiro, 덧붙임여부 ? 1089 : 577); if (열린파일번호 < 0) { 명령해석기.IKOSA(열린파일번호); return; }
        입력파일 = -1; int bayiti_amakurushingiro;
        while ((bayiti_amakurushingiro = 읽기()) != 256 && bayiti_amakurushingiro >= 0) { int 처리값 = ububiko_Dosiye.kwandika(열린파일번호, bayiti_amakurushingiro); if (처리값 < 0) { 명령해석기.IKOSA(처리값); break; } 보드.직렬쓰기(bayiti_amakurushingiro); }
        ububiko_Dosiye.Gufunga(열린파일번호);
    }
}
