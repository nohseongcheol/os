// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 셸 내장 Nástroje. */
public final class 셸도구 {
    static int[] údaje = new int[16384];
    static int vstupný_súbor = -1;
    static int otvoriť_Súbor(int argument_INDEX, int Proces_MODE) {
        int 처리값 = 명령해석기.Cesta(argument_INDEX); return 처리값 < 0 ? 처리값 : Pamäť_Súbory.Otvoriť(Proces_MODE);
    }
    static boolean Pripraviť_vstup(int argument_INDEX) {
        vstupný_súbor = -1;
        if (argument_INDEX < 명령해석기.token_COUNT) {
            vstupný_súbor = otvoriť_Súbor(argument_INDEX, 0);
            if (vstupný_súbor < 0) { 명령해석기.chyba(vstupný_súbor); return false; }
        }
        return true;
    }
    static int Čítanie() {
        if (vstupný_súbor >= 3) return Pamäť_Súbory.Čítanie(vstupný_súbor);
        while (true) {
            int Byte_údaje = Panel.직렬읽기(); if (Byte_údaje == -2 || Byte_údaje == 4) return 256;
            if (Byte_údaje == 3) { 명령해석기.KR = 130; return 256; }
            if (Byte_údaje >= 0) return Byte_údaje; Panel.YIELD_procesor();
        }
    }
    static void Zatvoriť() { if (vstupný_súbor >= 3) Pamäť_Súbory.Zatvoriť(vstupný_súbor); vstupný_súbor = -1; }
    static void zobraziť_VALUE() {
        int 마지막자리 = 명령해석기.token_COUNT == 1 ? 2 : 명령해석기.token_COUNT;
        for (int argument_INDEX = 1; argument_INDEX < 마지막자리; argument_INDEX++) {
            if (!Pripraviť_vstup(argument_INDEX)) continue;
            int Byte_údaje; while ((Byte_údaje = Čítanie()) != 256 && Byte_údaje >= 0) Panel.직렬쓰기(Byte_údaje);
            if (Byte_údaje < 0) 명령해석기.chyba(Byte_údaje); Zatvoriť();
        }
    }
    static void Súbor_Úloha(String 동작번호) {
        if (명령해석기.token_COUNT != 2) { 명령해석기.KR = 2; 단말.Zápis("사용법: mkdir/rmdir/touch Súbor\n"); return; }
        int 처리값 = 명령해석기.Cesta(1);
        if (처리값 >= 0) {
            if (동작번호.charAt(0) == 'm') 처리값 = Pamäť_Súbory.Create_Adresár();
            else if (동작번호.charAt(0) == 'r') 처리값 = Pamäť_Súbory.odobrať_Adresár();
            else { 처리값 = Pamäť_Súbory.Otvoriť(65); if (처리값 >= 3) 처리값 = Pamäť_Súbory.Zatvoriť(처리값); }
        }
        if (처리값 < 0) 명령해석기.chyba(처리값);
    }
    static void inštancia_VALUE(boolean 이동여부) {
        if (명령해석기.token_COUNT != 3) { 명령해석기.KR = 2; 단말.Zápis("사용법: cp/mv 원본 cieľ_účastník (Súbor)\n"); return; }
        int 처리값 = 명령해석기.Cesta(1); if (처리값 >= 0) 처리값 = Pamäť_Súbory.normalizovať_VALUE();
        if (처리값 < 0) { 명령해석기.chyba(처리값); return; }
        int 원본번호 = Pamäť_Súbory.FIND_položka(); if (원본번호 < 0) { 명령해석기.chyba(-2); return; }
        int položka_COUNT_8f7753a1 = Pamäť_Súbory.dĺžka_VALUE[원본번호]; for (int Loop_INDEX = 0; Loop_INDEX < položka_COUNT_8f7753a1; Loop_INDEX++) údaje[Loop_INDEX] = Pamäť_Súbory.자료읽기(원본번호, Loop_INDEX);
        처리값 = 명령해석기.Cesta(2); if (처리값 >= 0) 처리값 = Pamäť_Súbory.normalizovať_VALUE();
        if (처리값 < 0) { 명령해석기.chyba(처리값); return; }
        if (Pamäť_Súbory.FIND_položka() == 원본번호) { if (!이동여부) 명령해석기.chyba(-22); return; }
        if (이동여부) { 처리값 = Pamäť_Súbory.Premenovať_položka(원본번호); if (처리값 < 0) 명령해석기.chyba(처리값); return; }
        int 열린파일번호 = Pamäť_Súbory.Otvoriť(577); if (열린파일번호 < 0) { 명령해석기.chyba(열린파일번호); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < položka_COUNT_8f7753a1; Loop_INDEX++) { 처리값 = Pamäť_Súbory.Zápis(열린파일번호, údaje[Loop_INDEX]); if (처리값 < 0) { 명령해석기.chyba(처리값); break; } }
        Pamäť_Súbory.Zatvoriť(열린파일번호);
    }
    static int číslica_VALUE(int argument_INDEX) {
        if (argument_INDEX >= 명령해석기.token_COUNT) return -1;
        int položka_COUNT_8f7753a1 = 0; for (int Loop_INDEX = 0; Loop_INDEX < 명령해석기.dĺžka_VALUE[argument_INDEX]; Loop_INDEX++) { int bod_kódu = 명령해석기.token_VALUE[명령해석기.시작점[argument_INDEX] + Loop_INDEX]; if (bod_kódu < '0' || bod_kódu > '9' || položka_COUNT_8f7753a1 > 10000) return -1; položka_COUNT_8f7753a1 = položka_COUNT_8f7753a1 * 10 + bod_kódu - '0'; } return položka_COUNT_8f7753a1;
    }
    static void 세기() {
        int argument_INDEX = 1, 선택번호 = 0;
        if (명령해석기.같음(1, "-c") || 명령해석기.같음(1, "-l") || 명령해석기.같음(1, "-w")) { 선택번호 = 명령해석기.같음(1, "-c") ? 1 : 명령해석기.같음(1, "-l") ? 2 : 3; argument_INDEX++; }
        if (명령해석기.token_COUNT > argument_INDEX + 1) { 명령해석기.KR = 2; 단말.Zápis("사용법: wc [-c|-l|-w] [Súbor]\n"); return; }
        if (!Pripraviť_vstup(argument_INDEX)) return;
        int Byte_COUNT = 0, 줄수 = 0, 낱말수 = 0, Byte_údaje; boolean 낱말 = false;
        while ((Byte_údaje = Čítanie()) >= 0 && Byte_údaje != 256) { Byte_COUNT++; if (Byte_údaje == 10) 줄수++; boolean priestor = Byte_údaje == 32 || Byte_údaje >= 9 && Byte_údaje <= 13; if (!priestor && !낱말) 낱말수++; 낱말 = !priestor; }
        Zatvoriť(); if (Byte_údaje < 0) { 명령해석기.chyba(Byte_údaje); return; }
        if (선택번호 != 0) 단말.수(선택번호 == 1 ? Byte_COUNT : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.수(줄수); 단말.문자(' '); 단말.수(낱말수); 단말.문자(' '); 단말.수(Byte_COUNT); } 단말.문자(10);
    }
    static void FIND_položka() {
        if (명령해석기.token_COUNT < 2 || 명령해석기.token_COUNT > 3) { 명령해석기.KR = 2; 단말.Zápis("사용법: grep 찾을문구 [Súbor]\n"); return; }
        if (!Pripraviť_vstup(2)) return;
        int položka_COUNT_8f7753a1 = 0, Byte_údaje, 일치수 = 0;
        while (true) {
            Byte_údaje = Čítanie();
            if (Byte_údaje == 10 || Byte_údaje == 256 || Byte_údaje < 0) {
                boolean 찾은여부 = false;
                for (int Loop_INDEX = 0; Loop_INDEX <= položka_COUNT_8f7753a1 - 명령해석기.dĺžka_VALUE[1]; Loop_INDEX++) {
                    boolean 같은여부 = true; for (int vnútorné_pozícia = 0; vnútorné_pozícia < 명령해석기.dĺžka_VALUE[1]; vnútorné_pozícia++) if (údaje[Loop_INDEX + vnútorné_pozícia] != 명령해석기.token_VALUE[명령해석기.시작점[1] + vnútorné_pozícia]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (položka_COUNT_8f7753a1 > 0 || Byte_údaje == 10)) { for (int Loop_INDEX = 0; Loop_INDEX < položka_COUNT_8f7753a1; Loop_INDEX++) Panel.직렬쓰기(údaje[Loop_INDEX]); 단말.문자(10); 일치수++; }
                položka_COUNT_8f7753a1 = 0; if (Byte_údaje != 10) break;
            } else if (položka_COUNT_8f7753a1 < údaje.length) údaje[položka_COUNT_8f7753a1++] = Byte_údaje;
            else { 명령해석기.chyba(-28); Zatvoriť(); return; }
        }
        Zatvoriť(); if (Byte_údaje < 0) 명령해석기.chyba(Byte_údaje); else if (명령해석기.KR == 0) 명령해석기.KR = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int argument_INDEX = 1, 줄수 = 10;
        if (명령해석기.같음(1, "-n")) { 줄수 = číslica_VALUE(2); argument_INDEX = 3; }
        if (줄수 < 0 || 명령해석기.token_COUNT > argument_INDEX + 1) { 명령해석기.KR = 2; 단말.Zápis("사용법: head/tail [-n 줄수] [Súbor]\n"); return; }
        if (!Pripraviť_vstup(argument_INDEX)) return;
        int položka_COUNT_8f7753a1 = 0, Byte_údaje;
        while ((Byte_údaje = Čítanie()) != 256 && Byte_údaje >= 0) { if (položka_COUNT_8f7753a1 == údaje.length) { 명령해석기.chyba(-28); Zatvoriť(); return; } údaje[položka_COUNT_8f7753a1++] = Byte_údaje; }
        Zatvoriť(); if (Byte_údaje < 0) { 명령해석기.chyba(Byte_údaje); return; }
        int miestny_START = 0, ukončiť_hovor_pozícia = položka_COUNT_8f7753a1;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int celkovo_COUNT = 0; for (int Loop_INDEX = položka_COUNT_8f7753a1 - 2; Loop_INDEX >= 0; Loop_INDEX--) if (údaje[Loop_INDEX] == 10 && ++celkovo_COUNT == 줄수) { miestny_START = Loop_INDEX + 1; break; } }
        else { int celkovo_COUNT = 0; for (int Loop_INDEX = 0; Loop_INDEX < položka_COUNT_8f7753a1; Loop_INDEX++) if (údaje[Loop_INDEX] == 10 && ++celkovo_COUNT == 줄수) { ukončiť_hovor_pozícia = Loop_INDEX + 1; break; } }
        for (int Loop_INDEX = miestny_START; Loop_INDEX < ukončiť_hovor_pozícia; Loop_INDEX++) Panel.직렬쓰기(údaje[Loop_INDEX]);
    }
    static void zapísať_Navždy_spolu() {
        boolean Pripojiť_f1444605 = 명령해석기.같음(1, "-a"); int argument_INDEX = Pripojiť_f1444605 ? 2 : 1;
        if (명령해석기.token_COUNT != argument_INDEX + 1) { 명령해석기.KR = 2; 단말.Zápis("사용법: tee [-a] Súbor\n"); return; }
        int 열린파일번호 = otvoriť_Súbor(argument_INDEX, Pripojiť_f1444605 ? 1089 : 577); if (열린파일번호 < 0) { 명령해석기.chyba(열린파일번호); return; }
        vstupný_súbor = -1; int Byte_údaje;
        while ((Byte_údaje = Čítanie()) != 256 && Byte_údaje >= 0) { int 처리값 = Pamäť_Súbory.Zápis(열린파일번호, Byte_údaje); if (처리값 < 0) { 명령해석기.chyba(처리값); break; } Panel.직렬쓰기(Byte_údaje); }
        Pamäť_Súbory.Zatvoriť(열린파일번호);
    }
}
