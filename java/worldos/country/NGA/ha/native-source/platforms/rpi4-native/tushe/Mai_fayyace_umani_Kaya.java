// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 Mai_fayyace_umani 내장 Kaya. */
public final class Mai_fayyace_umani_Kaya {
    static int[] Tarin_bayani = new int[16384];
    static int 입력파일 = -1;
    static int buɗe_Fayil(int Tubalin_aiki_Indes, int haryar_aikin_na_ura_yanayin_aiki) {
        int 처리값 = 명령해석기.Hanyar_shiga(Tubalin_aiki_Indes); return 처리값 < 0 ? 처리값 : Mahardatar_kwamfuta_Fayiloli.Buɗe(haryar_aikin_na_ura_yanayin_aiki);
    }
    static boolean 입력준비(int Tubalin_aiki_Indes) {
        입력파일 = -1;
        if (Tubalin_aiki_Indes < 명령해석기.토큰수) {
            입력파일 = buɗe_Fayil(Tubalin_aiki_Indes, 0);
            if (입력파일 < 0) { 명령해석기.Kuskure(입력파일); return false; }
        }
        return true;
    }
    static int Yi_Karatu() {
        if (입력파일 >= 3) return Mahardatar_kwamfuta_Fayiloli.Yi_Karatu(입력파일);
        while (true) {
            int bayit_Tarin_bayani = 보드.직렬읽기(); if (bayit_Tarin_bayani == -2 || bayit_Tarin_bayani == 4) return 256;
            if (bayit_Tarin_bayani == 3) { 명령해석기.결과 = 130; return 256; }
            if (bayit_Tarin_bayani >= 0) return bayit_Tarin_bayani; 보드.ɗan_tsai_da_CPU();
        }
    }
    static void Rufe() { if (입력파일 >= 3) Mahardatar_kwamfuta_Fayiloli.Rufe(입력파일); 입력파일 = -1; }
    static void s_Daraja() {
        int 마지막자리 = 명령해석기.토큰수 == 1 ? 2 : 명령해석기.토큰수;
        for (int Tubalin_aiki_Indes = 1; Tubalin_aiki_Indes < 마지막자리; Tubalin_aiki_Indes++) {
            if (!입력준비(Tubalin_aiki_Indes)) continue;
            int bayit_Tarin_bayani; while ((bayit_Tarin_bayani = Yi_Karatu()) != 256 && bayit_Tarin_bayani >= 0) 보드.직렬쓰기(bayit_Tarin_bayani);
            if (bayit_Tarin_bayani < 0) 명령해석기.Kuskure(bayit_Tarin_bayani); Rufe();
        }
    }
    static void Fayil_Kes(String 동작번호) {
        if (명령해석기.토큰수 != 2) { 명령해석기.결과 = 2; 단말.Yi_Rubutu("사용법: mkdir/rmdir/touch Fayil\n"); return; }
        int 처리값 = 명령해석기.Hanyar_shiga(1);
        if (처리값 >= 0) {
            if (동작번호.charAt(0) == 'm') 처리값 = Mahardatar_kwamfuta_Fayiloli.ƙirƙíra_ma_ajiya();
            else if (동작번호.charAt(0) == 'r') 처리값 = Mahardatar_kwamfuta_Fayiloli.Cire_ma_ajiya();
            else { 처리값 = Mahardatar_kwamfuta_Fayiloli.Buɗe(65); if (처리값 >= 3) 처리값 = Mahardatar_kwamfuta_Fayiloli.Rufe(처리값); }
        }
        if (처리값 < 0) 명령해석기.Kuskure(처리값);
    }
    static void Kwafi_Daraja(boolean 이동여부) {
        if (명령해석기.토큰수 != 3) { 명령해석기.결과 = 2; 단말.Yi_Rubutu("사용법: cp/mv 원본 목적지 (Fayil)\n"); return; }
        int 처리값 = 명령해석기.Hanyar_shiga(1); if (처리값 >= 0) 처리값 = Mahardatar_kwamfuta_Fayiloli.Gajarta_kimar_bayanai_Daraja();
        if (처리값 < 0) { 명령해석기.Kuskure(처리값); return; }
        int 원본번호 = Mahardatar_kwamfuta_Fayiloli.nema_Mashigar_bayanai(); if (원본번호 < 0) { 명령해석기.Kuskure(-2); return; }
        int 항목수 = Mahardatar_kwamfuta_Fayiloli.Tsawo_Daraja[원본번호]; for (int Warware_Indes = 0; Warware_Indes < 항목수; Warware_Indes++) Tarin_bayani[Warware_Indes] = Mahardatar_kwamfuta_Fayiloli.자료읽기(원본번호, Warware_Indes);
        처리값 = 명령해석기.Hanyar_shiga(2); if (처리값 >= 0) 처리값 = Mahardatar_kwamfuta_Fayiloli.Gajarta_kimar_bayanai_Daraja();
        if (처리값 < 0) { 명령해석기.Kuskure(처리값); return; }
        if (Mahardatar_kwamfuta_Fayiloli.nema_Mashigar_bayanai() == 원본번호) { if (!이동여부) 명령해석기.Kuskure(-22); return; }
        if (이동여부) { 처리값 = Mahardatar_kwamfuta_Fayiloli.이름바꾸기(원본번호); if (처리값 < 0) 명령해석기.Kuskure(처리값); return; }
        int 열린파일번호 = Mahardatar_kwamfuta_Fayiloli.Buɗe(577); if (열린파일번호 < 0) { 명령해석기.Kuskure(열린파일번호); return; }
        for (int Warware_Indes = 0; Warware_Indes < 항목수; Warware_Indes++) { 처리값 = Mahardatar_kwamfuta_Fayiloli.Yi_Rubutu(열린파일번호, Tarin_bayani[Warware_Indes]); if (처리값 < 0) { 명령해석기.Kuskure(처리값); break; } }
        Mahardatar_kwamfuta_Fayiloli.Rufe(열린파일번호);
    }
    static int lamba_Daraja(int Tubalin_aiki_Indes) {
        if (Tubalin_aiki_Indes >= 명령해석기.토큰수) return -1;
        int 항목수 = 0; for (int Warware_Indes = 0; Warware_Indes < 명령해석기.Tsawo_Daraja[Tubalin_aiki_Indes]; Warware_Indes++) { int Lambar_sirrin_harafi = 명령해석기.token_Daraja[명령해석기.시작점[Tubalin_aiki_Indes] + Warware_Indes]; if (Lambar_sirrin_harafi < '0' || Lambar_sirrin_harafi > '9' || 항목수 > 10000) return -1; 항목수 = 항목수 * 10 + Lambar_sirrin_harafi - '0'; } return 항목수;
    }
    static void 세기() {
        int Tubalin_aiki_Indes = 1, zaɓe = 0;
        if (명령해석기.같음(1, "-c") || 명령해석기.같음(1, "-l") || 명령해석기.같음(1, "-w")) { zaɓe = 명령해석기.같음(1, "-c") ? 1 : 명령해석기.같음(1, "-l") ? 2 : 3; Tubalin_aiki_Indes++; }
        if (명령해석기.토큰수 > Tubalin_aiki_Indes + 1) { 명령해석기.결과 = 2; 단말.Yi_Rubutu("사용법: wc [-c|-l|-w] [Fayil]\n"); return; }
        if (!입력준비(Tubalin_aiki_Indes)) return;
        int 바이트수 = 0, 줄수 = 0, 낱말수 = 0, bayit_Tarin_bayani; boolean 낱말 = false;
        while ((bayit_Tarin_bayani = Yi_Karatu()) >= 0 && bayit_Tarin_bayani != 256) { 바이트수++; if (bayit_Tarin_bayani == 10) 줄수++; boolean wuri = bayit_Tarin_bayani == 32 || bayit_Tarin_bayani >= 9 && bayit_Tarin_bayani <= 13; if (!wuri && !낱말) 낱말수++; 낱말 = !wuri; }
        Rufe(); if (bayit_Tarin_bayani < 0) { 명령해석기.Kuskure(bayit_Tarin_bayani); return; }
        if (zaɓe != 0) 단말.수(zaɓe == 1 ? 바이트수 : zaɓe == 2 ? 줄수 : 낱말수);
        else { 단말.수(줄수); 단말.문자(' '); 단말.수(낱말수); 단말.문자(' '); 단말.수(바이트수); } 단말.문자(10);
    }
    static void nema_Mashigar_bayanai() {
        if (명령해석기.토큰수 < 2 || 명령해석기.토큰수 > 3) { 명령해석기.결과 = 2; 단말.Yi_Rubutu("사용법: grep 찾을문구 [Fayil]\n"); return; }
        if (!입력준비(2)) return;
        int 항목수 = 0, bayit_Tarin_bayani, 일치수 = 0;
        while (true) {
            bayit_Tarin_bayani = Yi_Karatu();
            if (bayit_Tarin_bayani == 10 || bayit_Tarin_bayani == 256 || bayit_Tarin_bayani < 0) {
                boolean 찾은여부 = false;
                for (int Warware_Indes = 0; Warware_Indes <= 항목수 - 명령해석기.Tsawo_Daraja[1]; Warware_Indes++) {
                    boolean 같은여부 = true; for (int 안쪽자리 = 0; 안쪽자리 < 명령해석기.Tsawo_Daraja[1]; 안쪽자리++) if (Tarin_bayani[Warware_Indes + 안쪽자리] != 명령해석기.token_Daraja[명령해석기.시작점[1] + 안쪽자리]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (항목수 > 0 || bayit_Tarin_bayani == 10)) { for (int Warware_Indes = 0; Warware_Indes < 항목수; Warware_Indes++) 보드.직렬쓰기(Tarin_bayani[Warware_Indes]); 단말.문자(10); 일치수++; }
                항목수 = 0; if (bayit_Tarin_bayani != 10) break;
            } else if (항목수 < Tarin_bayani.length) Tarin_bayani[항목수++] = bayit_Tarin_bayani;
            else { 명령해석기.Kuskure(-28); Rufe(); return; }
        }
        Rufe(); if (bayit_Tarin_bayani < 0) 명령해석기.Kuskure(bayit_Tarin_bayani); else if (명령해석기.결과 == 0) 명령해석기.결과 = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int Tubalin_aiki_Indes = 1, 줄수 = 10;
        if (명령해석기.같음(1, "-n")) { 줄수 = lamba_Daraja(2); Tubalin_aiki_Indes = 3; }
        if (줄수 < 0 || 명령해석기.토큰수 > Tubalin_aiki_Indes + 1) { 명령해석기.결과 = 2; 단말.Yi_Rubutu("사용법: head/tail [-n 줄수] [Fayil]\n"); return; }
        if (!입력준비(Tubalin_aiki_Indes)) return;
        int 항목수 = 0, bayit_Tarin_bayani;
        while ((bayit_Tarin_bayani = Yi_Karatu()) != 256 && bayit_Tarin_bayani >= 0) { if (항목수 == Tarin_bayani.length) { 명령해석기.Kuskure(-28); Rufe(); return; } Tarin_bayani[항목수++] = bayit_Tarin_bayani; }
        Rufe(); if (bayit_Tarin_bayani < 0) { 명령해석기.Kuskure(bayit_Tarin_bayani); return; }
        int na_gida_Fara = 0, 끝자리 = 항목수;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int 총수 = 0; for (int Warware_Indes = 항목수 - 2; Warware_Indes >= 0; Warware_Indes--) if (Tarin_bayani[Warware_Indes] == 10 && ++총수 == 줄수) { na_gida_Fara = Warware_Indes + 1; break; } }
        else { int 총수 = 0; for (int Warware_Indes = 0; Warware_Indes < 항목수; Warware_Indes++) if (Tarin_bayani[Warware_Indes] == 10 && ++총수 == 줄수) { 끝자리 = Warware_Indes + 1; break; } }
        for (int Warware_Indes = na_gida_Fara; Warware_Indes < 끝자리; Warware_Indes++) 보드.직렬쓰기(Tarin_bayani[Warware_Indes]);
    }
    static void 함께쓰기() {
        boolean 덧붙임여부 = 명령해석기.같음(1, "-a"); int Tubalin_aiki_Indes = 덧붙임여부 ? 2 : 1;
        if (명령해석기.토큰수 != Tubalin_aiki_Indes + 1) { 명령해석기.결과 = 2; 단말.Yi_Rubutu("사용법: tee [-a] Fayil\n"); return; }
        int 열린파일번호 = buɗe_Fayil(Tubalin_aiki_Indes, 덧붙임여부 ? 1089 : 577); if (열린파일번호 < 0) { 명령해석기.Kuskure(열린파일번호); return; }
        입력파일 = -1; int bayit_Tarin_bayani;
        while ((bayit_Tarin_bayani = Yi_Karatu()) != 256 && bayit_Tarin_bayani >= 0) { int 처리값 = Mahardatar_kwamfuta_Fayiloli.Yi_Rubutu(열린파일번호, bayit_Tarin_bayani); if (처리값 < 0) { 명령해석기.Kuskure(처리값); break; } 보드.직렬쓰기(bayit_Tarin_bayani); }
        Mahardatar_kwamfuta_Fayiloli.Rufe(열린파일번호);
    }
}
