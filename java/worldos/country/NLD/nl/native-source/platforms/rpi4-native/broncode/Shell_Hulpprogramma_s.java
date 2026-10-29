// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 Shell 내장 hulpmiddelen. */
public final class Shell_Hulpprogramma_s {
    static int[] gegevens = new int[16384];
    static int invoerbestand = -1;
    static int open_Bestand(int argument_INDEX, int Proces_MODUS) {
        int 처리값 = Opdrachtvertolker.pad(argument_INDEX); return 처리값 < 0 ? 처리값 : GeheugenBestanden.Openen(Proces_MODUS);
    }
    static boolean Bereid_voor_invoer(int argument_INDEX) {
        invoerbestand = -1;
        if (argument_INDEX < Opdrachtvertolker.token_AANTAL) {
            invoerbestand = open_Bestand(argument_INDEX, 0);
            if (invoerbestand < 0) { Opdrachtvertolker.fout(invoerbestand); return false; }
        }
        return true;
    }
    static int Lezen() {
        if (invoerbestand >= 3) return GeheugenBestanden.Lezen(invoerbestand);
        while (true) {
            int byte_gegevens = Bord.직렬읽기(); if (byte_gegevens == -2 || byte_gegevens == 4) return 256;
            if (byte_gegevens == 3) { Opdrachtvertolker.resultaat = 130; return 256; }
            if (byte_gegevens >= 0) return byte_gegevens; Bord.RENDEMENT_CPU();
        }
    }
    static void Sluiten() { if (invoerbestand >= 3) GeheugenBestanden.Sluiten(invoerbestand); invoerbestand = -1; }
    static void Weergave_WAARDE() {
        int 마지막자리 = Opdrachtvertolker.token_AANTAL == 1 ? 2 : Opdrachtvertolker.token_AANTAL;
        for (int argument_INDEX = 1; argument_INDEX < 마지막자리; argument_INDEX++) {
            if (!Bereid_voor_invoer(argument_INDEX)) continue;
            int byte_gegevens; while ((byte_gegevens = Lezen()) != 256 && byte_gegevens >= 0) Bord.직렬쓰기(byte_gegevens);
            if (byte_gegevens < 0) Opdrachtvertolker.fout(byte_gegevens); Sluiten();
        }
    }
    static void Bestand_Taak(String Actie_nummer) {
        if (Opdrachtvertolker.token_AANTAL != 2) { Opdrachtvertolker.resultaat = 2; 단말.Schrijven("사용법: mkdir/rmdir/touch bestand\n"); return; }
        int 처리값 = Opdrachtvertolker.pad(1);
        if (처리값 >= 0) {
            if (Actie_nummer.charAt(0) == 'm') 처리값 = GeheugenBestanden.maken_map();
            else if (Actie_nummer.charAt(0) == 'r') 처리값 = GeheugenBestanden.verwijderen_map();
            else { 처리값 = GeheugenBestanden.Openen(65); if (처리값 >= 3) 처리값 = GeheugenBestanden.Sluiten(처리값); }
        }
        if (처리값 < 0) Opdrachtvertolker.fout(처리값);
    }
    static void kopiëren_WAARDE(boolean 이동여부) {
        if (Opdrachtvertolker.token_AANTAL != 3) { Opdrachtvertolker.resultaat = 2; 단말.Schrijven("사용법: cp/mv 원본 doel_eindpunt (bestand)\n"); return; }
        int 처리값 = Opdrachtvertolker.pad(1); if (처리값 >= 0) 처리값 = GeheugenBestanden.normaliseren_WAARDE();
        if (처리값 < 0) { Opdrachtvertolker.fout(처리값); return; }
        int 원본번호 = GeheugenBestanden.Zoeken_invoer(); if (원본번호 < 0) { Opdrachtvertolker.fout(-2); return; }
        int invoer_AANTAL_8f7753a1 = GeheugenBestanden.tijdsduur_WAARDE[원본번호]; for (int lus_INDEX = 0; lus_INDEX < invoer_AANTAL_8f7753a1; lus_INDEX++) gegevens[lus_INDEX] = GeheugenBestanden.자료읽기(원본번호, lus_INDEX);
        처리값 = Opdrachtvertolker.pad(2); if (처리값 >= 0) 처리값 = GeheugenBestanden.normaliseren_WAARDE();
        if (처리값 < 0) { Opdrachtvertolker.fout(처리값); return; }
        if (GeheugenBestanden.Zoeken_invoer() == 원본번호) { if (!이동여부) Opdrachtvertolker.fout(-22); return; }
        if (이동여부) { 처리값 = GeheugenBestanden.Naam_wijzigen_invoer(원본번호); if (처리값 < 0) Opdrachtvertolker.fout(처리값); return; }
        int 열린파일번호 = GeheugenBestanden.Openen(577); if (열린파일번호 < 0) { Opdrachtvertolker.fout(열린파일번호); return; }
        for (int lus_INDEX = 0; lus_INDEX < invoer_AANTAL_8f7753a1; lus_INDEX++) { 처리값 = GeheugenBestanden.Schrijven(열린파일번호, gegevens[lus_INDEX]); if (처리값 < 0) { Opdrachtvertolker.fout(처리값); break; } }
        GeheugenBestanden.Sluiten(열린파일번호);
    }
    static int cijfer_WAARDE(int argument_INDEX) {
        if (argument_INDEX >= Opdrachtvertolker.token_AANTAL) return -1;
        int invoer_AANTAL_8f7753a1 = 0; for (int lus_INDEX = 0; lus_INDEX < Opdrachtvertolker.tijdsduur_WAARDE[argument_INDEX]; lus_INDEX++) { int codepoint = Opdrachtvertolker.token_WAARDE[Opdrachtvertolker.시작점[argument_INDEX] + lus_INDEX]; if (codepoint < '0' || codepoint > '9' || invoer_AANTAL_8f7753a1 > 10000) return -1; invoer_AANTAL_8f7753a1 = invoer_AANTAL_8f7753a1 * 10 + codepoint - '0'; } return invoer_AANTAL_8f7753a1;
    }
    static void 세기() {
        int argument_INDEX = 1, 선택번호 = 0;
        if (Opdrachtvertolker.같음(1, "-c") || Opdrachtvertolker.같음(1, "-l") || Opdrachtvertolker.같음(1, "-w")) { 선택번호 = Opdrachtvertolker.같음(1, "-c") ? 1 : Opdrachtvertolker.같음(1, "-l") ? 2 : 3; argument_INDEX++; }
        if (Opdrachtvertolker.token_AANTAL > argument_INDEX + 1) { Opdrachtvertolker.resultaat = 2; 단말.Schrijven("사용법: wc [-c|-l|-w] [bestand]\n"); return; }
        if (!Bereid_voor_invoer(argument_INDEX)) return;
        int byte_AANTAL = 0, 줄수 = 0, 낱말수 = 0, byte_gegevens; boolean 낱말 = false;
        while ((byte_gegevens = Lezen()) >= 0 && byte_gegevens != 256) { byte_AANTAL++; if (byte_gegevens == 10) 줄수++; boolean Space = byte_gegevens == 32 || byte_gegevens >= 9 && byte_gegevens <= 13; if (!Space && !낱말) 낱말수++; 낱말 = !Space; }
        Sluiten(); if (byte_gegevens < 0) { Opdrachtvertolker.fout(byte_gegevens); return; }
        if (선택번호 != 0) 단말.nummer(선택번호 == 1 ? byte_AANTAL : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.nummer(줄수); 단말.문자(' '); 단말.nummer(낱말수); 단말.문자(' '); 단말.nummer(byte_AANTAL); } 단말.문자(10);
    }
    static void Zoeken_invoer() {
        if (Opdrachtvertolker.token_AANTAL < 2 || Opdrachtvertolker.token_AANTAL > 3) { Opdrachtvertolker.resultaat = 2; 단말.Schrijven("사용법: grep 찾을문구 [bestand]\n"); return; }
        if (!Bereid_voor_invoer(2)) return;
        int invoer_AANTAL_8f7753a1 = 0, byte_gegevens, 일치수 = 0;
        while (true) {
            byte_gegevens = Lezen();
            if (byte_gegevens == 10 || byte_gegevens == 256 || byte_gegevens < 0) {
                boolean 찾은여부 = false;
                for (int lus_INDEX = 0; lus_INDEX <= invoer_AANTAL_8f7753a1 - Opdrachtvertolker.tijdsduur_WAARDE[1]; lus_INDEX++) {
                    boolean 같은여부 = true; for (int inner_functie = 0; inner_functie < Opdrachtvertolker.tijdsduur_WAARDE[1]; inner_functie++) if (gegevens[lus_INDEX + inner_functie] != Opdrachtvertolker.token_WAARDE[Opdrachtvertolker.시작점[1] + inner_functie]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (invoer_AANTAL_8f7753a1 > 0 || byte_gegevens == 10)) { for (int lus_INDEX = 0; lus_INDEX < invoer_AANTAL_8f7753a1; lus_INDEX++) Bord.직렬쓰기(gegevens[lus_INDEX]); 단말.문자(10); 일치수++; }
                invoer_AANTAL_8f7753a1 = 0; if (byte_gegevens != 10) break;
            } else if (invoer_AANTAL_8f7753a1 < gegevens.length) gegevens[invoer_AANTAL_8f7753a1++] = byte_gegevens;
            else { Opdrachtvertolker.fout(-28); Sluiten(); return; }
        }
        Sluiten(); if (byte_gegevens < 0) Opdrachtvertolker.fout(byte_gegevens); else if (Opdrachtvertolker.resultaat == 0) Opdrachtvertolker.resultaat = 일치수 == 0 ? 1 : 0;
    }
    static void kop_WAARDE(boolean 뒤쪽자리) {
        int argument_INDEX = 1, 줄수 = 10;
        if (Opdrachtvertolker.같음(1, "-n")) { 줄수 = cijfer_WAARDE(2); argument_INDEX = 3; }
        if (줄수 < 0 || Opdrachtvertolker.token_AANTAL > argument_INDEX + 1) { Opdrachtvertolker.resultaat = 2; 단말.Schrijven("사용법: head/tail [-n 줄수] [bestand]\n"); return; }
        if (!Bereid_voor_invoer(argument_INDEX)) return;
        int invoer_AANTAL_8f7753a1 = 0, byte_gegevens;
        while ((byte_gegevens = Lezen()) != 256 && byte_gegevens >= 0) { if (invoer_AANTAL_8f7753a1 == gegevens.length) { Opdrachtvertolker.fout(-28); Sluiten(); return; } gegevens[invoer_AANTAL_8f7753a1++] = byte_gegevens; }
        Sluiten(); if (byte_gegevens < 0) { Opdrachtvertolker.fout(byte_gegevens); return; }
        int lokaal_START = 0, beëindigen_functie = invoer_AANTAL_8f7753a1;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int totaal_AANTAL = 0; for (int lus_INDEX = invoer_AANTAL_8f7753a1 - 2; lus_INDEX >= 0; lus_INDEX--) if (gegevens[lus_INDEX] == 10 && ++totaal_AANTAL == 줄수) { lokaal_START = lus_INDEX + 1; break; } }
        else { int totaal_AANTAL = 0; for (int lus_INDEX = 0; lus_INDEX < invoer_AANTAL_8f7753a1; lus_INDEX++) if (gegevens[lus_INDEX] == 10 && ++totaal_AANTAL == 줄수) { beëindigen_functie = lus_INDEX + 1; break; } }
        for (int lus_INDEX = lokaal_START; lus_INDEX < beëindigen_functie; lus_INDEX++) Bord.직렬쓰기(gegevens[lus_INDEX]);
    }
    static void schrijven_Samenzijn() {
        boolean toevoegen = Opdrachtvertolker.같음(1, "-a"); int argument_INDEX = toevoegen ? 2 : 1;
        if (Opdrachtvertolker.token_AANTAL != argument_INDEX + 1) { Opdrachtvertolker.resultaat = 2; 단말.Schrijven("사용법: tee [-a] bestand\n"); return; }
        int 열린파일번호 = open_Bestand(argument_INDEX, toevoegen ? 1089 : 577); if (열린파일번호 < 0) { Opdrachtvertolker.fout(열린파일번호); return; }
        invoerbestand = -1; int byte_gegevens;
        while ((byte_gegevens = Lezen()) != 256 && byte_gegevens >= 0) { int 처리값 = GeheugenBestanden.Schrijven(열린파일번호, byte_gegevens); if (처리값 < 0) { Opdrachtvertolker.fout(처리값); break; } Bord.직렬쓰기(byte_gegevens); }
        GeheugenBestanden.Sluiten(열린파일번호);
    }
}
