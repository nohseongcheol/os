// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 shell 내장 Tresnak. */
public final class shell_Tresnak {
    static int[] datuak = new int[16384];
    static int sarrerako_fitxategi = -1;
    static int ireki_fitxategi(int arg_INDIZE, int prozesu_MODA) {
        int 처리값 = 명령해석기.Bide_izena(arg_INDIZE); return 처리값 < 0 ? 처리값 : Memoria_Fitxategiak.Ireki(prozesu_MODA);
    }
    static boolean 입력준비(int arg_INDIZE) {
        sarrerako_fitxategi = -1;
        if (arg_INDIZE < 명령해석기.token_ZENBATU) {
            sarrerako_fitxategi = ireki_fitxategi(arg_INDIZE, 0);
            if (sarrerako_fitxategi < 0) { 명령해석기.errorea(sarrerako_fitxategi); return false; }
        }
        return true;
    }
    static int Irakurri() {
        if (sarrerako_fitxategi >= 3) return Memoria_Fitxategiak.Irakurri(sarrerako_fitxategi);
        while (true) {
            int byte_datuak = arbel.직렬읽기(); if (byte_datuak == -2 || byte_datuak == 4) return 256;
            if (byte_datuak == 3) { 명령해석기.EMAITZA = 130; return 256; }
            if (byte_datuak >= 0) return byte_datuak; arbel.YIELD_PUZ();
        }
    }
    static void Itxi() { if (sarrerako_fitxategi >= 3) Memoria_Fitxategiak.Itxi(sarrerako_fitxategi); sarrerako_fitxategi = -1; }
    static void ikusi_balio() {
        int 마지막자리 = 명령해석기.token_ZENBATU == 1 ? 2 : 명령해석기.token_ZENBATU;
        for (int arg_INDIZE = 1; arg_INDIZE < 마지막자리; arg_INDIZE++) {
            if (!입력준비(arg_INDIZE)) continue;
            int byte_datuak; while ((byte_datuak = Irakurri()) != 256 && byte_datuak >= 0) arbel.직렬쓰기(byte_datuak);
            if (byte_datuak < 0) 명령해석기.errorea(byte_datuak); Itxi();
        }
    }
    static void fitxategi_lan(String 동작번호) {
        if (명령해석기.token_ZENBATU != 2) { 명령해석기.EMAITZA = 2; 단말.Idatzi("사용법: mkdir/rmdir/touch Fitxategia\n"); return; }
        int 처리값 = 명령해석기.Bide_izena(1);
        if (처리값 >= 0) {
            if (동작번호.charAt(0) == 'm') 처리값 = Memoria_Fitxategiak.sortu_direktorio();
            else if (동작번호.charAt(0) == 'r') 처리값 = Memoria_Fitxategiak.kendu_direktorio();
            else { 처리값 = Memoria_Fitxategiak.Ireki(65); if (처리값 >= 3) 처리값 = Memoria_Fitxategiak.Itxi(처리값); }
        }
        if (처리값 < 0) 명령해석기.errorea(처리값);
    }
    static void kopiatu_balio(boolean 이동여부) {
        if (명령해석기.token_ZENBATU != 3) { 명령해석기.EMAITZA = 2; 단말.Idatzi("사용법: cp/mv 원본 helburu_amaiera_puntu (Fitxategia)\n"); return; }
        int 처리값 = 명령해석기.Bide_izena(1); if (처리값 >= 0) 처리값 = Memoria_Fitxategiak.normalizatu_balio();
        if (처리값 < 0) { 명령해석기.errorea(처리값); return; }
        int 원본번호 = Memoria_Fitxategiak.Bilatu_sarrera(); if (원본번호 < 0) { 명령해석기.errorea(-2); return; }
        int sarrera_ZENBATU = Memoria_Fitxategiak.luzera_balio[원본번호]; for (int Loop_INDIZE = 0; Loop_INDIZE < sarrera_ZENBATU; Loop_INDIZE++) datuak[Loop_INDIZE] = Memoria_Fitxategiak.자료읽기(원본번호, Loop_INDIZE);
        처리값 = 명령해석기.Bide_izena(2); if (처리값 >= 0) 처리값 = Memoria_Fitxategiak.normalizatu_balio();
        if (처리값 < 0) { 명령해석기.errorea(처리값); return; }
        if (Memoria_Fitxategiak.Bilatu_sarrera() == 원본번호) { if (!이동여부) 명령해석기.errorea(-22); return; }
        if (이동여부) { 처리값 = Memoria_Fitxategiak.이름바꾸기(원본번호); if (처리값 < 0) 명령해석기.errorea(처리값); return; }
        int 열린파일번호 = Memoria_Fitxategiak.Ireki(577); if (열린파일번호 < 0) { 명령해석기.errorea(열린파일번호); return; }
        for (int Loop_INDIZE = 0; Loop_INDIZE < sarrera_ZENBATU; Loop_INDIZE++) { 처리값 = Memoria_Fitxategiak.Idatzi(열린파일번호, datuak[Loop_INDIZE]); if (처리값 < 0) { 명령해석기.errorea(처리값); break; } }
        Memoria_Fitxategiak.Itxi(열린파일번호);
    }
    static int digitu_balio(int arg_INDIZE) {
        if (arg_INDIZE >= 명령해석기.token_ZENBATU) return -1;
        int sarrera_ZENBATU = 0; for (int Loop_INDIZE = 0; Loop_INDIZE < 명령해석기.luzera_balio[arg_INDIZE]; Loop_INDIZE++) { int karaktere_kode = 명령해석기.token_balio[명령해석기.시작점[arg_INDIZE] + Loop_INDIZE]; if (karaktere_kode < '0' || karaktere_kode > '9' || sarrera_ZENBATU > 10000) return -1; sarrera_ZENBATU = sarrera_ZENBATU * 10 + karaktere_kode - '0'; } return sarrera_ZENBATU;
    }
    static void 세기() {
        int arg_INDIZE = 1, 선택번호 = 0;
        if (명령해석기.같음(1, "-c") || 명령해석기.같음(1, "-l") || 명령해석기.같음(1, "-w")) { 선택번호 = 명령해석기.같음(1, "-c") ? 1 : 명령해석기.같음(1, "-l") ? 2 : 3; arg_INDIZE++; }
        if (명령해석기.token_ZENBATU > arg_INDIZE + 1) { 명령해석기.EMAITZA = 2; 단말.Idatzi("사용법: wc [-c|-l|-w] [Fitxategia]\n"); return; }
        if (!입력준비(arg_INDIZE)) return;
        int byte_ZENBATU = 0, 줄수 = 0, 낱말수 = 0, byte_datuak; boolean 낱말 = false;
        while ((byte_datuak = Irakurri()) >= 0 && byte_datuak != 256) { byte_ZENBATU++; if (byte_datuak == 10) 줄수++; boolean gune = byte_datuak == 32 || byte_datuak >= 9 && byte_datuak <= 13; if (!gune && !낱말) 낱말수++; 낱말 = !gune; }
        Itxi(); if (byte_datuak < 0) { 명령해석기.errorea(byte_datuak); return; }
        if (선택번호 != 0) 단말.수(선택번호 == 1 ? byte_ZENBATU : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.수(줄수); 단말.문자(' '); 단말.수(낱말수); 단말.문자(' '); 단말.수(byte_ZENBATU); } 단말.문자(10);
    }
    static void Bilatu_sarrera() {
        if (명령해석기.token_ZENBATU < 2 || 명령해석기.token_ZENBATU > 3) { 명령해석기.EMAITZA = 2; 단말.Idatzi("사용법: grep 찾을문구 [Fitxategia]\n"); return; }
        if (!입력준비(2)) return;
        int sarrera_ZENBATU = 0, byte_datuak, 일치수 = 0;
        while (true) {
            byte_datuak = Irakurri();
            if (byte_datuak == 10 || byte_datuak == 256 || byte_datuak < 0) {
                boolean 찾은여부 = false;
                for (int Loop_INDIZE = 0; Loop_INDIZE <= sarrera_ZENBATU - 명령해석기.luzera_balio[1]; Loop_INDIZE++) {
                    boolean 같은여부 = true; for (int barnekoa_kargu = 0; barnekoa_kargu < 명령해석기.luzera_balio[1]; barnekoa_kargu++) if (datuak[Loop_INDIZE + barnekoa_kargu] != 명령해석기.token_balio[명령해석기.시작점[1] + barnekoa_kargu]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (sarrera_ZENBATU > 0 || byte_datuak == 10)) { for (int Loop_INDIZE = 0; Loop_INDIZE < sarrera_ZENBATU; Loop_INDIZE++) arbel.직렬쓰기(datuak[Loop_INDIZE]); 단말.문자(10); 일치수++; }
                sarrera_ZENBATU = 0; if (byte_datuak != 10) break;
            } else if (sarrera_ZENBATU < datuak.length) datuak[sarrera_ZENBATU++] = byte_datuak;
            else { 명령해석기.errorea(-28); Itxi(); return; }
        }
        Itxi(); if (byte_datuak < 0) 명령해석기.errorea(byte_datuak); else if (명령해석기.EMAITZA == 0) 명령해석기.EMAITZA = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int arg_INDIZE = 1, 줄수 = 10;
        if (명령해석기.같음(1, "-n")) { 줄수 = digitu_balio(2); arg_INDIZE = 3; }
        if (줄수 < 0 || 명령해석기.token_ZENBATU > arg_INDIZE + 1) { 명령해석기.EMAITZA = 2; 단말.Idatzi("사용법: head/tail [-n 줄수] [Fitxategia]\n"); return; }
        if (!입력준비(arg_INDIZE)) return;
        int sarrera_ZENBATU = 0, byte_datuak;
        while ((byte_datuak = Irakurri()) != 256 && byte_datuak >= 0) { if (sarrera_ZENBATU == datuak.length) { 명령해석기.errorea(-28); Itxi(); return; } datuak[sarrera_ZENBATU++] = byte_datuak; }
        Itxi(); if (byte_datuak < 0) { 명령해석기.errorea(byte_datuak); return; }
        int lokal_HASI = 0, amaitu_kargu = sarrera_ZENBATU;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int 총수 = 0; for (int Loop_INDIZE = sarrera_ZENBATU - 2; Loop_INDIZE >= 0; Loop_INDIZE--) if (datuak[Loop_INDIZE] == 10 && ++총수 == 줄수) { lokal_HASI = Loop_INDIZE + 1; break; } }
        else { int 총수 = 0; for (int Loop_INDIZE = 0; Loop_INDIZE < sarrera_ZENBATU; Loop_INDIZE++) if (datuak[Loop_INDIZE] == 10 && ++총수 == 줄수) { amaitu_kargu = Loop_INDIZE + 1; break; } }
        for (int Loop_INDIZE = lokal_HASI; Loop_INDIZE < amaitu_kargu; Loop_INDIZE++) arbel.직렬쓰기(datuak[Loop_INDIZE]);
    }
    static void idatzi_Batera() {
        boolean Erantsi = 명령해석기.같음(1, "-a"); int arg_INDIZE = Erantsi ? 2 : 1;
        if (명령해석기.token_ZENBATU != arg_INDIZE + 1) { 명령해석기.EMAITZA = 2; 단말.Idatzi("사용법: tee [-a] Fitxategia\n"); return; }
        int 열린파일번호 = ireki_fitxategi(arg_INDIZE, Erantsi ? 1089 : 577); if (열린파일번호 < 0) { 명령해석기.errorea(열린파일번호); return; }
        sarrerako_fitxategi = -1; int byte_datuak;
        while ((byte_datuak = Irakurri()) != 256 && byte_datuak >= 0) { int 처리값 = Memoria_Fitxategiak.Idatzi(열린파일번호, byte_datuak); if (처리값 < 0) { 명령해석기.errorea(처리값); break; } arbel.직렬쓰기(byte_datuak); }
        Memoria_Fitxategiak.Itxi(열린파일번호);
    }
}
