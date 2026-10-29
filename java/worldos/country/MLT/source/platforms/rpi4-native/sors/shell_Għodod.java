// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 shell 내장 Għodod. */
public final class shell_Għodod {
    static int[] data = new int[16384];
    static int 입력파일 = -1;
    static int fetaħ_fajl(int argument_INDEX, int Proċess_MODE) {
        int 처리값 = 명령해석기.mogħdija(argument_INDEX); return 처리값 < 0 ? 처리값 : Memorja_Fajls.fetaħ(Proċess_MODE);
    }
    static boolean 입력준비(int argument_INDEX) {
        입력파일 = -1;
        if (argument_INDEX < 명령해석기.token_COUNT) {
            입력파일 = fetaħ_fajl(argument_INDEX, 0);
            if (입력파일 < 0) { 명령해석기.żball(입력파일); return false; }
        }
        return true;
    }
    static int 읽기() {
        if (입력파일 >= 3) return Memorja_Fajls.읽기(입력파일);
        while (true) {
            int byte_data = bord.직렬읽기(); if (byte_data == -2 || byte_data == 4) return 256;
            if (byte_data == 3) { 명령해석기.miżura = 130; return 256; }
            if (byte_data >= 0) return byte_data; bord.YIELD_CPU();
        }
    }
    static void agħlaq() { if (입력파일 >= 3) Memorja_Fajls.agħlaq(입력파일); 입력파일 = -1; }
    static void wera_VALUE() {
        int 마지막자리 = 명령해석기.token_COUNT == 1 ? 2 : 명령해석기.token_COUNT;
        for (int argument_INDEX = 1; argument_INDEX < 마지막자리; argument_INDEX++) {
            if (!입력준비(argument_INDEX)) continue;
            int byte_data; while ((byte_data = 읽기()) != 256 && byte_data >= 0) bord.직렬쓰기(byte_data);
            if (byte_data < 0) 명령해석기.żball(byte_data); agħlaq();
        }
    }
    static void fajl_każ(String 동작번호) {
        if (명령해석기.token_COUNT != 2) { 명령해석기.miżura = 2; 단말.kiteb("사용법: mkdir/rmdir/touch fajl\n"); return; }
        int 처리값 = 명령해석기.mogħdija(1);
        if (처리값 >= 0) {
            if (동작번호.charAt(0) == 'm') 처리값 = Memorja_Fajls.ħalaq_direttorju();
            else if (동작번호.charAt(0) == 'r') 처리값 = Memorja_Fajls.neħħa_direttorju();
            else { 처리값 = Memorja_Fajls.fetaħ(65); if (처리값 >= 3) 처리값 = Memorja_Fajls.agħlaq(처리값); }
        }
        if (처리값 < 0) 명령해석기.żball(처리값);
    }
    static void kkopja_VALUE(boolean 이동여부) {
        if (명령해석기.token_COUNT != 3) { 명령해석기.miżura = 2; 단말.kiteb("사용법: cp/mv 원본 목적지 (fajl)\n"); return; }
        int 처리값 = 명령해석기.mogħdija(1); if (처리값 >= 0) 처리값 = Memorja_Fajls.nnormalizza_VALUE();
        if (처리값 < 0) { 명령해석기.żball(처리값); return; }
        int 원본번호 = Memorja_Fajls.sab_entrata(); if (원본번호 < 0) { 명령해석기.żball(-2); return; }
        int entrata_COUNT = Memorja_Fajls.tul_VALUE[원본번호]; for (int Loop_INDEX = 0; Loop_INDEX < entrata_COUNT; Loop_INDEX++) data[Loop_INDEX] = Memorja_Fajls.자료읽기(원본번호, Loop_INDEX);
        처리값 = 명령해석기.mogħdija(2); if (처리값 >= 0) 처리값 = Memorja_Fajls.nnormalizza_VALUE();
        if (처리값 < 0) { 명령해석기.żball(처리값); return; }
        if (Memorja_Fajls.sab_entrata() == 원본번호) { if (!이동여부) 명령해석기.żball(-22); return; }
        if (이동여부) { 처리값 = Memorja_Fajls.이름바꾸기(원본번호); if (처리값 < 0) 명령해석기.żball(처리값); return; }
        int 열린파일번호 = Memorja_Fajls.fetaħ(577); if (열린파일번호 < 0) { 명령해석기.żball(열린파일번호); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < entrata_COUNT; Loop_INDEX++) { 처리값 = Memorja_Fajls.kiteb(열린파일번호, data[Loop_INDEX]); if (처리값 < 0) { 명령해석기.żball(처리값); break; } }
        Memorja_Fajls.agħlaq(열린파일번호);
    }
    static int ċifra_VALUE(int argument_INDEX) {
        if (argument_INDEX >= 명령해석기.token_COUNT) return -1;
        int entrata_COUNT = 0; for (int Loop_INDEX = 0; Loop_INDEX < 명령해석기.tul_VALUE[argument_INDEX]; Loop_INDEX++) { int kodiċi_tal_karattru = 명령해석기.token_VALUE[명령해석기.시작점[argument_INDEX] + Loop_INDEX]; if (kodiċi_tal_karattru < '0' || kodiċi_tal_karattru > '9' || entrata_COUNT > 10000) return -1; entrata_COUNT = entrata_COUNT * 10 + kodiċi_tal_karattru - '0'; } return entrata_COUNT;
    }
    static void 세기() {
        int argument_INDEX = 1, 선택번호 = 0;
        if (명령해석기.같음(1, "-c") || 명령해석기.같음(1, "-l") || 명령해석기.같음(1, "-w")) { 선택번호 = 명령해석기.같음(1, "-c") ? 1 : 명령해석기.같음(1, "-l") ? 2 : 3; argument_INDEX++; }
        if (명령해석기.token_COUNT > argument_INDEX + 1) { 명령해석기.miżura = 2; 단말.kiteb("사용법: wc [-c|-l|-w] [fajl]\n"); return; }
        if (!입력준비(argument_INDEX)) return;
        int byte_COUNT = 0, 줄수 = 0, 낱말수 = 0, byte_data; boolean 낱말 = false;
        while ((byte_data = 읽기()) >= 0 && byte_data != 256) { byte_COUNT++; if (byte_data == 10) 줄수++; boolean SPACE = byte_data == 32 || byte_data >= 9 && byte_data <= 13; if (!SPACE && !낱말) 낱말수++; 낱말 = !SPACE; }
        agħlaq(); if (byte_data < 0) { 명령해석기.żball(byte_data); return; }
        if (선택번호 != 0) 단말.수(선택번호 == 1 ? byte_COUNT : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.수(줄수); 단말.문자(' '); 단말.수(낱말수); 단말.문자(' '); 단말.수(byte_COUNT); } 단말.문자(10);
    }
    static void sab_entrata() {
        if (명령해석기.token_COUNT < 2 || 명령해석기.token_COUNT > 3) { 명령해석기.miżura = 2; 단말.kiteb("사용법: grep 찾을문구 [fajl]\n"); return; }
        if (!입력준비(2)) return;
        int entrata_COUNT = 0, byte_data, 일치수 = 0;
        while (true) {
            byte_data = 읽기();
            if (byte_data == 10 || byte_data == 256 || byte_data < 0) {
                boolean 찾은여부 = false;
                for (int Loop_INDEX = 0; Loop_INDEX <= entrata_COUNT - 명령해석기.tul_VALUE[1]; Loop_INDEX++) {
                    boolean 같은여부 = true; for (int inner_join_pożizzjoni = 0; inner_join_pożizzjoni < 명령해석기.tul_VALUE[1]; inner_join_pożizzjoni++) if (data[Loop_INDEX + inner_join_pożizzjoni] != 명령해석기.token_VALUE[명령해석기.시작점[1] + inner_join_pożizzjoni]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (entrata_COUNT > 0 || byte_data == 10)) { for (int Loop_INDEX = 0; Loop_INDEX < entrata_COUNT; Loop_INDEX++) bord.직렬쓰기(data[Loop_INDEX]); 단말.문자(10); 일치수++; }
                entrata_COUNT = 0; if (byte_data != 10) break;
            } else if (entrata_COUNT < data.length) data[entrata_COUNT++] = byte_data;
            else { 명령해석기.żball(-28); agħlaq(); return; }
        }
        agħlaq(); if (byte_data < 0) 명령해석기.żball(byte_data); else if (명령해석기.miżura == 0) 명령해석기.miżura = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int argument_INDEX = 1, 줄수 = 10;
        if (명령해석기.같음(1, "-n")) { 줄수 = ċifra_VALUE(2); argument_INDEX = 3; }
        if (줄수 < 0 || 명령해석기.token_COUNT > argument_INDEX + 1) { 명령해석기.miżura = 2; 단말.kiteb("사용법: head/tail [-n 줄수] [fajl]\n"); return; }
        if (!입력준비(argument_INDEX)) return;
        int entrata_COUNT = 0, byte_data;
        while ((byte_data = 읽기()) != 256 && byte_data >= 0) { if (entrata_COUNT == data.length) { 명령해석기.żball(-28); agħlaq(); return; } data[entrata_COUNT++] = byte_data; }
        agħlaq(); if (byte_data < 0) { 명령해석기.żball(byte_data); return; }
        int lokali_Bidu = 0, ttermina_pożizzjoni = entrata_COUNT;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int 총수 = 0; for (int Loop_INDEX = entrata_COUNT - 2; Loop_INDEX >= 0; Loop_INDEX--) if (data[Loop_INDEX] == 10 && ++총수 == 줄수) { lokali_Bidu = Loop_INDEX + 1; break; } }
        else { int 총수 = 0; for (int Loop_INDEX = 0; Loop_INDEX < entrata_COUNT; Loop_INDEX++) if (data[Loop_INDEX] == 10 && ++총수 == 줄수) { ttermina_pożizzjoni = Loop_INDEX + 1; break; } }
        for (int Loop_INDEX = lokali_Bidu; Loop_INDEX < ttermina_pożizzjoni; Loop_INDEX++) bord.직렬쓰기(data[Loop_INDEX]);
    }
    static void 함께쓰기() {
        boolean 덧붙임여부 = 명령해석기.같음(1, "-a"); int argument_INDEX = 덧붙임여부 ? 2 : 1;
        if (명령해석기.token_COUNT != argument_INDEX + 1) { 명령해석기.miżura = 2; 단말.kiteb("사용법: tee [-a] fajl\n"); return; }
        int 열린파일번호 = fetaħ_fajl(argument_INDEX, 덧붙임여부 ? 1089 : 577); if (열린파일번호 < 0) { 명령해석기.żball(열린파일번호); return; }
        입력파일 = -1; int byte_data;
        while ((byte_data = 읽기()) != 256 && byte_data >= 0) { int 처리값 = Memorja_Fajls.kiteb(열린파일번호, byte_data); if (처리값 < 0) { 명령해석기.żball(처리값); break; } bord.직렬쓰기(byte_data); }
        Memorja_Fajls.agħlaq(열린파일번호);
    }
}
