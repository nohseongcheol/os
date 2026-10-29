// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 interactief Shell 문법. 파이프는 순차 Uitvoeren_opdracht, 환경은 같은 셸에서 공유한다. */
public final class Shell_syntaxis {
    static int[] broncode = new int[4 * 4096], soort_WAARDE = new int[4 * 128], starten = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] variabele_naam = new int[16 * 32], variabele_gegevens = new int[16 * 256], 이름길이 = new int[16], WAARDE_tijdsduur = new int[16];
    static int[] script_WAARDE = new int[4 * 16384];
    static int Status_WAARDE, 깊이, 쓴수;
    static boolean 연결중, script_beëindigen, extensie_fout;
    static boolean naam_teken(int codepoint) { return codepoint >= 'a' && codepoint <= 'z' || codepoint >= 'A' && codepoint <= 'Z' || codepoint == '_' || codepoint >= 128; }
    static boolean 이름뒤(int codepoint) { return naam_teken(codepoint) || codepoint >= '0' && codepoint <= '9'; }
    static void fout(String tekst) { Bord.입출력전환(0); 단말.Schrijven("opdracht parseren_WAARDE: "); 단말.Schrijven(tekst); 단말.문자(10); Status_WAARDE = 2; }
    static int Lezen(int invoer_AANTAL_8f7753a1, int 중첩깊이) {
        int actueel_INDEX = 0, totaal_AANTAL = 0, BASIS_functie = 중첩깊이 * 4096, speciaal_teken = 중첩깊이 * 128;
        while (actueel_INDEX < invoer_AANTAL_8f7753a1) {
            while (actueel_INDEX < invoer_AANTAL_8f7753a1 && (broncode[BASIS_functie + actueel_INDEX] == 32 || broncode[BASIS_functie + actueel_INDEX] == 9)) actueel_INDEX++;
            if (actueel_INDEX == invoer_AANTAL_8f7753a1 || broncode[BASIS_functie + actueel_INDEX] == '#') break;
            if (totaal_AANTAL == 128) { fout("낱말이 너무 많습니다"); return -1; }
            int START_functie = actueel_INDEX, codepoint = broncode[BASIS_functie + actueel_INDEX], gegevens_soort = 0;
            if (codepoint == ';') { gegevens_soort = 1; actueel_INDEX++; }
            else if (codepoint == '&') { if (actueel_INDEX + 1 >= invoer_AANTAL_8f7753a1 || broncode[BASIS_functie + actueel_INDEX + 1] != '&') { fout("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } gegevens_soort = 2; actueel_INDEX += 2; }
            else if (codepoint == '|') { actueel_INDEX++; gegevens_soort = actueel_INDEX < invoer_AANTAL_8f7753a1 && broncode[BASIS_functie + actueel_INDEX] == '|' ? 3 : 4; if (gegevens_soort == 3) actueel_INDEX++; }
            else if (codepoint == '>') { actueel_INDEX++; gegevens_soort = actueel_INDEX < invoer_AANTAL_8f7753a1 && broncode[BASIS_functie + actueel_INDEX] == '>' ? 6 : 5; if (gegevens_soort == 6) actueel_INDEX++; }
            else if (codepoint == '<') { gegevens_soort = 7; actueel_INDEX++; }
            else {
                int Citaat = 0;
                while (actueel_INDEX < invoer_AANTAL_8f7753a1) {
                    codepoint = broncode[BASIS_functie + actueel_INDEX];
                    if (codepoint == '`' && Citaat != 39 || codepoint == '$' && Citaat != 39 && actueel_INDEX + 1 < invoer_AANTAL_8f7753a1 && broncode[BASIS_functie + actueel_INDEX + 1] == '(') { fout("opdracht resultaat 치환은 지원하지 않습니다"); return -1; }
                    if (codepoint == '\\' && Citaat != 39) { if (++actueel_INDEX == invoer_AANTAL_8f7753a1) { fout("invoerregel 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } actueel_INDEX++; continue; }
                    if (codepoint == Citaat) { Citaat = 0; actueel_INDEX++; continue; }
                    if (Citaat == 0 && (codepoint == 39 || codepoint == 34)) { Citaat = codepoint; actueel_INDEX++; continue; }
                    if (Citaat == 0 && (codepoint == 32 || codepoint == 9 || codepoint == ';' || codepoint == '&' || codepoint == '|' || codepoint == '<' || codepoint == '>')) break;
                    actueel_INDEX++;
                }
                if (Citaat != 0) { fout("따옴표가 닫히지 않았습니다"); return -1; }
                if (actueel_INDEX < invoer_AANTAL_8f7753a1 && (broncode[BASIS_functie + actueel_INDEX] == '>' || broncode[BASIS_functie + actueel_INDEX] == '<')) {
                    boolean 수치 = actueel_INDEX > START_functie;
                    for (int lus_INDEX = START_functie; lus_INDEX < actueel_INDEX; lus_INDEX++) if (broncode[BASIS_functie + lus_INDEX] < '0' || broncode[BASIS_functie + lus_INDEX] > '9') 수치 = false;
                    if (수치) { fout("번호를 지정한 bestand 서술자 I_O 전환은 지원하지 않습니다"); return -1; }
                }
            }
            soort_WAARDE[speciaal_teken + totaal_AANTAL] = gegevens_soort; starten[speciaal_teken + totaal_AANTAL] = START_functie; 끝[speciaal_teken + totaal_AANTAL] = actueel_INDEX; totaal_AANTAL++;
        }
        boolean 낱말 = false;
        for (int lus_INDEX = 0; lus_INDEX < totaal_AANTAL; lus_INDEX++) {
            int 임시값 = soort_WAARDE[speciaal_teken + lus_INDEX];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++lus_INDEX == totaal_AANTAL || soort_WAARDE[speciaal_teken + lus_INDEX] != 0) { fout("I_O 전환에 bestand 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || lus_INDEX == totaal_AANTAL - 1 && 임시값 != 1) { fout("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (totaal_AANTAL > 0 && !낱말 && soort_WAARDE[speciaal_teken + totaal_AANTAL - 1] != 1) { fout("명령이 빠졌습니다"); return -1; }
        return totaal_AANTAL;
    }
    static boolean bereik_sms(int[] gegevens_MATRIX, int lokaal_START, int invoer_AANTAL_8f7753a1, String teken_functie) {
        if (invoer_AANTAL_8f7753a1 != teken_functie.length()) return false; for (int lus_INDEX = 0; lus_INDEX < invoer_AANTAL_8f7753a1; lus_INDEX++) if (gegevens_MATRIX[lokaal_START + lus_INDEX] != teken_functie.charAt(lus_INDEX)) return false; return true;
    }
    static void 넣기(int byte_gegevens) {
        if (쓴수 >= Opdrachtvertolker.token_WAARDE.length) { if (!extensie_fout) fout("변수를 펼친 명령이 너무 깁니다"); extensie_fout = true; return; }
        Opdrachtvertolker.token_WAARDE[쓴수++] = byte_gegevens;
    }
    static void variabele_WAARDE(int[] gegevens_MATRIX, int START_functie, int invoer_AANTAL_8f7753a1) {
        if (bereik_sms(gegevens_MATRIX, START_functie, invoer_AANTAL_8f7753a1, "PWD")) { 넣기('/'); for (int lus_INDEX = 0; lus_INDEX < GeheugenBestanden.actueel_tijdsduur; lus_INDEX++) 넣기(GeheugenBestanden.actueel_item[lus_INDEX]); return; }
        if (bereik_sms(gegevens_MATRIX, START_functie, invoer_AANTAL_8f7753a1, "HOME")) { 넣기('/'); return; }
        if (bereik_sms(gegevens_MATRIX, START_functie, invoer_AANTAL_8f7753a1, "?")) {
            int gegevens_WAARDE = Status_WAARDE, cijfer = 100; boolean 시작여부 = false;
            while (cijfer > 0) { int navolgend_WAARDE = gegevens_WAARDE / cijfer; if (navolgend_WAARDE != 0 || 시작여부 || cijfer == 1) { 넣기('0' + navolgend_WAARDE); 시작여부 = true; } gegevens_WAARDE %= cijfer; cijfer /= 10; } return;
        }
        for (int lus_INDEX = 0; lus_INDEX < 16; lus_INDEX++) if (이름길이[lus_INDEX] == invoer_AANTAL_8f7753a1) {
            boolean VERGELIJKEN = true; for (int inner_functie = 0; inner_functie < invoer_AANTAL_8f7753a1; inner_functie++) if (variabele_naam[lus_INDEX * 32 + inner_functie] != gegevens_MATRIX[START_functie + inner_functie]) VERGELIJKEN = false;
            if (VERGELIJKEN) { for (int inner_functie = 0; inner_functie < WAARDE_tijdsduur[lus_INDEX]; inner_functie++) 넣기(variabele_gegevens[lus_INDEX * 256 + inner_functie]); return; }
        }
    }
    static boolean Word_WAARDE(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = starten[중첩깊이 * 128 + 낱말번호], beëindigen_functie = 끝[중첩깊이 * 128 + 낱말번호], BASIS_functie = 중첩깊이 * 4096, Citaat = 0;
        if (읽는자리 < beëindigen_functie && broncode[BASIS_functie + 읽는자리] == '~' && (읽는자리 + 1 == beëindigen_functie || broncode[BASIS_functie + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < beëindigen_functie) {
            int codepoint = broncode[BASIS_functie + 읽는자리++];
            if (codepoint == Citaat) { Citaat = 0; continue; }
            if (Citaat == 0 && (codepoint == 39 || codepoint == 34)) { Citaat = codepoint; continue; }
            if (codepoint == '\\' && Citaat != 39) { int Volgende_functie = broncode[BASIS_functie + 읽는자리++]; if (Citaat == 34 && Volgende_functie != '$' && Volgende_functie != '"' && Volgende_functie != '\\') 넣기('\\'); 넣기(Volgende_functie); continue; }
            if (codepoint == '$' && Citaat != 39 && 읽는자리 < beëindigen_functie) {
                boolean 중괄호자리 = broncode[BASIS_functie + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < beëindigen_functie && broncode[BASIS_functie + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < beëindigen_functie && 이름뒤(broncode[BASIS_functie + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == beëindigen_functie || broncode[BASIS_functie + 읽는자리] != '}')) { fout("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                variabele_WAARDE(broncode, BASIS_functie + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(codepoint);
        }
        return !extensie_fout;
    }
    static int omgeving_Instellingen(int argument_INDEX, boolean verwijderen) {
        int lokaal_START = Opdrachtvertolker.시작점[argument_INDEX], beëindigen_functie = lokaal_START + Opdrachtvertolker.tijdsduur_WAARDE[argument_INDEX], 같음자리 = lokaal_START;
        while (같음자리 < beëindigen_functie && Opdrachtvertolker.token_WAARDE[같음자리] != '=') 같음자리++;
        int invoer_AANTAL_8f7753a1 = 같음자리 - lokaal_START;
        if (invoer_AANTAL_8f7753a1 < 1 || invoer_AANTAL_8f7753a1 > 31 || !naam_teken(Opdrachtvertolker.token_WAARDE[lokaal_START]) || !verwijderen && 같음자리 == beëindigen_functie || beëindigen_functie - 같음자리 - 1 > 255) return 2;
        for (int lus_INDEX = lokaal_START; lus_INDEX < 같음자리; lus_INDEX++) if (!이름뒤(Opdrachtvertolker.token_WAARDE[lus_INDEX])) return 2;
        if (bereik_sms(Opdrachtvertolker.token_WAARDE, lokaal_START, invoer_AANTAL_8f7753a1, "PWD") || bereik_sms(Opdrachtvertolker.token_WAARDE, lokaal_START, invoer_AANTAL_8f7753a1, "HOME")) return 2;
        int 찾은여부 = -1, informatie_leeg_Status = -1;
        for (int lus_INDEX = 0; lus_INDEX < 16; lus_INDEX++) {
            if (이름길이[lus_INDEX] == 0) informatie_leeg_Status = lus_INDEX;
            if (이름길이[lus_INDEX] != invoer_AANTAL_8f7753a1) continue;
            boolean VERGELIJKEN = true; for (int inner_functie = 0; inner_functie < invoer_AANTAL_8f7753a1; inner_functie++) if (variabele_naam[lus_INDEX * 32 + inner_functie] != Opdrachtvertolker.token_WAARDE[lokaal_START + inner_functie]) VERGELIJKEN = false;
            if (VERGELIJKEN) 찾은여부 = lus_INDEX;
        }
        if (verwijderen) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = informatie_leeg_Status; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = invoer_AANTAL_8f7753a1; WAARDE_tijdsduur[찾은여부] = beëindigen_functie - 같음자리 - 1;
        for (int lus_INDEX = 0; lus_INDEX < invoer_AANTAL_8f7753a1; lus_INDEX++) variabele_naam[찾은여부 * 32 + lus_INDEX] = Opdrachtvertolker.token_WAARDE[lokaal_START + lus_INDEX];
        for (int lus_INDEX = 같음자리 + 1; lus_INDEX < beëindigen_functie; lus_INDEX++) variabele_gegevens[찾은여부 * 256 + lus_INDEX - 같음자리 - 1] = Opdrachtvertolker.token_WAARDE[lus_INDEX];
        return 0;
    }
    static void weergeven_omgeving() {
        단말.Schrijven("HOME=/\nPWD="); GeheugenBestanden.actueel_schrijven(); 단말.문자(10);
        for (int lus_INDEX = 0; lus_INDEX < 16; lus_INDEX++) if (이름길이[lus_INDEX] > 0) {
            for (int inner_functie = 0; inner_functie < 이름길이[lus_INDEX]; inner_functie++) Bord.직렬쓰기(variabele_naam[lus_INDEX * 32 + inner_functie]); 단말.문자('=');
            for (int inner_functie = 0; inner_functie < WAARDE_tijdsduur[lus_INDEX]; inner_functie++) Bord.직렬쓰기(variabele_gegevens[lus_INDEX * 256 + inner_functie]); 단말.문자(10);
        }
    }
    static void Uitvoeren_opdracht(int[] gegevens_MATRIX, int 시작변위, int invoer_AANTAL_8f7753a1, int 중첩깊이) {
        if (중첩깊이 >= 4 || invoer_AANTAL_8f7753a1 > 4096) { fout("opdracht 파일의 nesting_WAARDE 또는 invoerregel tijdsduur_WAARDE 제한을 넘었습니다"); return; }
        for (int lus_INDEX = 0; lus_INDEX < invoer_AANTAL_8f7753a1; lus_INDEX++) broncode[중첩깊이 * 4096 + lus_INDEX] = gegevens_MATRIX[시작변위 + lus_INDEX];
        int totaal_AANTAL = Lezen(invoer_AANTAL_8f7753a1, 중첩깊이); if (totaal_AANTAL < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < totaal_AANTAL) {
            int Groep_beëindigen = 읽는자리;
            while (Groep_beëindigen < totaal_AANTAL && (soort_WAARDE[중첩깊이 * 128 + Groep_beëindigen] == 0 || soort_WAARDE[중첩깊이 * 128 + Groep_beëindigen] >= 4)) Groep_beëindigen++;
            boolean Uitvoeren_cc685ae5 = 조건성립 == 1 || 조건성립 == 2 && Status_WAARDE == 0 || 조건성립 == 3 && Status_WAARDE != 0;
            if (Uitvoeren_cc685ae5) {
                boolean Vorige_item_INDEX = false;
                while (읽는자리 < Groep_beëindigen) {
                    int Volgende_functie = 읽는자리; while (Volgende_functie < Groep_beëindigen && soort_WAARDE[중첩깊이 * 128 + Volgende_functie] != 4) Volgende_functie++;
                    boolean VERBINDEN_Stream = Volgende_functie < Groep_beëindigen; int invoer_page = -1, uitvoer_page = -1, 출력방식 = 0;
                    Opdrachtvertolker.token_AANTAL = 0; 쓴수 = 0; extensie_fout = false;
                    for (int lus_INDEX = 읽는자리; lus_INDEX < Volgende_functie; lus_INDEX++) {
                        int gegevens_soort = soort_WAARDE[중첩깊이 * 128 + lus_INDEX];
                        if (gegevens_soort >= 5) { if (gegevens_soort == 7) { if (invoer_page >= 0) { fout("invoer_WAARDE 전환이 겹쳤습니다"); return; } invoer_page = ++lus_INDEX; } else { if (uitvoer_page >= 0) { fout("tekstuitvoer 전환이 겹쳤습니다"); return; } uitvoer_page = ++lus_INDEX; 출력방식 = gegevens_soort; } continue; }
                        if (Opdrachtvertolker.token_AANTAL == 32) { fout("인수가 너무 많습니다"); return; }
                        int argument_INDEX = Opdrachtvertolker.token_AANTAL++; Opdrachtvertolker.시작점[argument_INDEX] = 쓴수;
                        if (!Word_WAARDE(lus_INDEX, 중첩깊이)) return;
                        Opdrachtvertolker.tijdsduur_WAARDE[argument_INDEX] = 쓴수 - Opdrachtvertolker.시작점[argument_INDEX];
                    }
                    연결중 = Vorige_item_INDEX || VERBINDEN_Stream || invoer_page >= 0 || uitvoer_page >= 0;
                    if (연결중 && (Opdrachtvertolker.같음(0, "vi") || Opdrachtvertolker.같음(0, "edit") || Opdrachtvertolker.같음(0, "load") || Opdrachtvertolker.같음(0, "gui") || Opdrachtvertolker.같음(0, "terminal") || Opdrachtvertolker.같음(0, "sh") || Opdrachtvertolker.같음(0, "source"))) { fout("interactief 명령과 opdracht 파일은 I_O 전환이나 Stream_WAARDE 연결에 쓸 nummer 없습니다"); return; }
                    셸입출력.starten(Vorige_item_INDEX, VERBINDEN_Stream);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int invoer_functie_206f1c6d = 입출력바꿈 == 0 ? invoer_page : uitvoer_page; if (invoer_functie_206f1c6d < 0) continue;
                        int START_functie = 쓴수; if (!Word_WAARDE(invoer_functie_206f1c6d, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = GeheugenBestanden.pad_START(쓴수 - START_functie);
                        for (int inner_functie = START_functie; 처리값 >= 0 && inner_functie < 쓴수; inner_functie++) 처리값 = GeheugenBestanden.pad_byte(inner_functie - START_functie, Opdrachtvertolker.token_WAARDE[inner_functie]);
                        if (처리값 >= 0) 처리값 = GeheugenBestanden.Openen(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); Opdrachtvertolker.fout(처리값); Status_WAARDE = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.invoerbestand = 처리값; else 셸입출력.uitvoerbestand = 처리값;
                    }
                    셸입출력.Toestaan_interactief = 중첩깊이 == 0 && 읽는자리 == 0 && Volgende_functie == totaal_AANTAL;
                    깊이 = 중첩깊이; Opdrachtvertolker.resultaat = 0; Bord.입출력전환(1);
                    Opdrachtvertolker.opdracht();
                    Bord.terminal(3);
                    int 반환값 = Opdrachtvertolker.resultaat, Stream_fout = 셸입출력.fout_WAARDE;
                    셸입출력.끝(); 연결중 = false;
                    Status_WAARDE = Stream_fout < 0 ? 1 : 반환값;
                    if (Stream_fout < 0) { Opdrachtvertolker.fout(Stream_fout); return; }
                    if (script_beëindigen || 반환값 == -1005) return;
                    Vorige_item_INDEX = true; 읽는자리 = Volgende_functie + 1;
                }
            }
            if (Groep_beëindigen < totaal_AANTAL) 조건성립 = soort_WAARDE[중첩깊이 * 128 + Groep_beëindigen];
            읽는자리 = Groep_beëindigen + 1;
        }
    }
    static void Uitvoeren_Bestand() {
        if (Opdrachtvertolker.token_AANTAL != 2 || 깊이 >= 3) { Opdrachtvertolker.resultaat = 2; 단말.Schrijven("사용법: sh bestand (nesting_WAARDE 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = Opdrachtvertolker.pad(1); if (처리값 >= 0) 처리값 = GeheugenBestanden.Openen(0);
        if (처리값 < 0) { Opdrachtvertolker.fout(처리값); return; }
        int invoer_AANTAL_8f7753a1 = 0, byte_gegevens;
        while ((byte_gegevens = GeheugenBestanden.Lezen(처리값)) != 256 && byte_gegevens >= 0 && invoer_AANTAL_8f7753a1 < 16384) script_WAARDE[중첩깊이 * 16384 + invoer_AANTAL_8f7753a1++] = byte_gegevens;
        GeheugenBestanden.Sluiten(처리값); Bord.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < invoer_AANTAL_8f7753a1 && !script_beëindigen;) {
            int beëindigen_functie = 읽는자리; while (beëindigen_functie < invoer_AANTAL_8f7753a1 && script_WAARDE[중첩깊이 * 16384 + beëindigen_functie] != 10) beëindigen_functie++;
            int geldig_tijdsduur = beëindigen_functie - 읽는자리; if (geldig_tijdsduur > 0 && script_WAARDE[중첩깊이 * 16384 + beëindigen_functie - 1] == 13) geldig_tijdsduur--;
            Uitvoeren_opdracht(script_WAARDE, 중첩깊이 * 16384 + 읽는자리, geldig_tijdsduur, 중첩깊이); 읽는자리 = beëindigen_functie + 1;
        }
        Opdrachtvertolker.resultaat = Status_WAARDE; script_beëindigen = false; 깊이 = 중첩깊이 - 1;
    }
}
