// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 interaktiv Shell 문법. 파이프는 순차 Utfør_kommando, 환경은 같은 셸에서 공유한다. */
public final class Shell_syntaks {
    static int[] KILDE = new int[4 * 4096], 종류 = new int[4 * 128], Kjør_2 = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] variabel_navn = new int[16 * 32], variabel_data = new int[16 * 256], 이름길이 = new int[16], VERDI_lengde = new int[16];
    static int[] skript_VERDI = new int[4 * 16384];
    static int status_VERDI, 깊이, 쓴수;
    static boolean 연결중, skript_avslutte_en_samtale, filtype_feil;
    static boolean navn_tegn(int tegnkode) { return tegnkode >= 'a' && tegnkode <= 'z' || tegnkode >= 'A' && tegnkode <= 'Z' || tegnkode == '_' || tegnkode >= 128; }
    static boolean 이름뒤(int tegnkode) { return navn_tegn(tegnkode) || tegnkode >= '0' && tegnkode <= '9'; }
    static void feil(String Tekst) { Tavle.입출력전환(0); 단말.Skriv("Kommando dele_opp_VERDI: "); 단말.Skriv(Tekst); 단말.문자(10); status_VERDI = 2; }
    static int Les(int oppføring_ANTALL, int 중첩깊이) {
        int betalt_INDEKS = 0, total_ANTALL = 0, grunnlag_plassere = 중첩깊이 * 4096, spesialtegn = 중첩깊이 * 128;
        while (betalt_INDEKS < oppføring_ANTALL) {
            while (betalt_INDEKS < oppføring_ANTALL && (KILDE[grunnlag_plassere + betalt_INDEKS] == 32 || KILDE[grunnlag_plassere + betalt_INDEKS] == 9)) betalt_INDEKS++;
            if (betalt_INDEKS == oppføring_ANTALL || KILDE[grunnlag_plassere + betalt_INDEKS] == '#') break;
            if (total_ANTALL == 128) { feil("낱말이 너무 많습니다"); return -1; }
            int START_plassere = betalt_INDEKS, tegnkode = KILDE[grunnlag_plassere + betalt_INDEKS], 자료종류 = 0;
            if (tegnkode == ';') { 자료종류 = 1; betalt_INDEKS++; }
            else if (tegnkode == '&') { if (betalt_INDEKS + 1 >= oppføring_ANTALL || KILDE[grunnlag_plassere + betalt_INDEKS + 1] != '&') { feil("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } 자료종류 = 2; betalt_INDEKS += 2; }
            else if (tegnkode == '|') { betalt_INDEKS++; 자료종류 = betalt_INDEKS < oppføring_ANTALL && KILDE[grunnlag_plassere + betalt_INDEKS] == '|' ? 3 : 4; if (자료종류 == 3) betalt_INDEKS++; }
            else if (tegnkode == '>') { betalt_INDEKS++; 자료종류 = betalt_INDEKS < oppføring_ANTALL && KILDE[grunnlag_plassere + betalt_INDEKS] == '>' ? 6 : 5; if (자료종류 == 6) betalt_INDEKS++; }
            else if (tegnkode == '<') { 자료종류 = 7; betalt_INDEKS++; }
            else {
                int Sitat = 0;
                while (betalt_INDEKS < oppføring_ANTALL) {
                    tegnkode = KILDE[grunnlag_plassere + betalt_INDEKS];
                    if (tegnkode == '`' && Sitat != 39 || tegnkode == '$' && Sitat != 39 && betalt_INDEKS + 1 < oppføring_ANTALL && KILDE[grunnlag_plassere + betalt_INDEKS + 1] == '(') { feil("Kommando KR 치환은 지원하지 않습니다"); return -1; }
                    if (tegnkode == '\\' && Sitat != 39) { if (++betalt_INDEKS == oppføring_ANTALL) { feil("Linje 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } betalt_INDEKS++; continue; }
                    if (tegnkode == Sitat) { Sitat = 0; betalt_INDEKS++; continue; }
                    if (Sitat == 0 && (tegnkode == 39 || tegnkode == 34)) { Sitat = tegnkode; betalt_INDEKS++; continue; }
                    if (Sitat == 0 && (tegnkode == 32 || tegnkode == 9 || tegnkode == ';' || tegnkode == '&' || tegnkode == '|' || tegnkode == '<' || tegnkode == '>')) break;
                    betalt_INDEKS++;
                }
                if (Sitat != 0) { feil("따옴표가 닫히지 않았습니다"); return -1; }
                if (betalt_INDEKS < oppføring_ANTALL && (KILDE[grunnlag_plassere + betalt_INDEKS] == '>' || KILDE[grunnlag_plassere + betalt_INDEKS] == '<')) {
                    boolean 수치 = betalt_INDEKS > START_plassere;
                    for (int Loop_INDEKS = START_plassere; Loop_INDEKS < betalt_INDEKS; Loop_INDEKS++) if (KILDE[grunnlag_plassere + Loop_INDEKS] < '0' || KILDE[grunnlag_plassere + Loop_INDEKS] > '9') 수치 = false;
                    if (수치) { feil("번호를 지정한 Fil 서술자 I_U 전환은 지원하지 않습니다"); return -1; }
                }
            }
            종류[spesialtegn + total_ANTALL] = 자료종류; Kjør_2[spesialtegn + total_ANTALL] = START_plassere; 끝[spesialtegn + total_ANTALL] = betalt_INDEKS; total_ANTALL++;
        }
        boolean 낱말 = false;
        for (int Loop_INDEKS = 0; Loop_INDEKS < total_ANTALL; Loop_INDEKS++) {
            int 임시값 = 종류[spesialtegn + Loop_INDEKS];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++Loop_INDEKS == total_ANTALL || 종류[spesialtegn + Loop_INDEKS] != 0) { feil("I_U 전환에 Fil 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || Loop_INDEKS == total_ANTALL - 1 && 임시값 != 1) { feil("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (total_ANTALL > 0 && !낱말 && 종류[spesialtegn + total_ANTALL - 1] != 1) { feil("명령이 빠졌습니다"); return -1; }
        return total_ANTALL;
    }
    static boolean område_SMS(int[] data_MATRISE, int lokal_START, int oppføring_ANTALL, String tegn_plassere) {
        if (oppføring_ANTALL != tegn_plassere.length()) return false; for (int Loop_INDEKS = 0; Loop_INDEKS < oppføring_ANTALL; Loop_INDEKS++) if (data_MATRISE[lokal_START + Loop_INDEKS] != tegn_plassere.charAt(Loop_INDEKS)) return false; return true;
    }
    static void 넣기(int byte_data) {
        if (쓴수 >= 명령해석기.token_VERDI.length) { if (!filtype_feil) feil("변수를 펼친 명령이 너무 깁니다"); filtype_feil = true; return; }
        명령해석기.token_VERDI[쓴수++] = byte_data;
    }
    static void variabel_VERDI(int[] data_MATRISE, int START_plassere, int oppføring_ANTALL) {
        if (område_SMS(data_MATRISE, START_plassere, oppføring_ANTALL, "PWD")) { 넣기('/'); for (int Loop_INDEKS = 0; Loop_INDEKS < Minne_Filer.betalt_lengde; Loop_INDEKS++) 넣기(Minne_Filer.betalt_vare[Loop_INDEKS]); return; }
        if (område_SMS(data_MATRISE, START_plassere, oppføring_ANTALL, "HOME")) { 넣기('/'); return; }
        if (område_SMS(data_MATRISE, START_plassere, oppføring_ANTALL, "?")) {
            int data_VERDI = status_VERDI, siffer = 100; boolean 시작여부 = false;
            while (siffer > 0) { int 뒷값 = data_VERDI / siffer; if (뒷값 != 0 || 시작여부 || siffer == 1) { 넣기('0' + 뒷값); 시작여부 = true; } data_VERDI %= siffer; siffer /= 10; } return;
        }
        for (int Loop_INDEKS = 0; Loop_INDEKS < 16; Loop_INDEKS++) if (이름길이[Loop_INDEKS] == oppføring_ANTALL) {
            boolean SAMMENLIGNE = true; for (int indre_kobling_plassere = 0; indre_kobling_plassere < oppføring_ANTALL; indre_kobling_plassere++) if (variabel_navn[Loop_INDEKS * 32 + indre_kobling_plassere] != data_MATRISE[START_plassere + indre_kobling_plassere]) SAMMENLIGNE = false;
            if (SAMMENLIGNE) { for (int indre_kobling_plassere = 0; indre_kobling_plassere < VERDI_lengde[Loop_INDEKS]; indre_kobling_plassere++) 넣기(variabel_data[Loop_INDEKS * 256 + indre_kobling_plassere]); return; }
        }
    }
    static boolean ord_VERDI(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = Kjør_2[중첩깊이 * 128 + 낱말번호], avslutte_en_samtale_plassere = 끝[중첩깊이 * 128 + 낱말번호], grunnlag_plassere = 중첩깊이 * 4096, Sitat = 0;
        if (읽는자리 < avslutte_en_samtale_plassere && KILDE[grunnlag_plassere + 읽는자리] == '~' && (읽는자리 + 1 == avslutte_en_samtale_plassere || KILDE[grunnlag_plassere + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < avslutte_en_samtale_plassere) {
            int tegnkode = KILDE[grunnlag_plassere + 읽는자리++];
            if (tegnkode == Sitat) { Sitat = 0; continue; }
            if (Sitat == 0 && (tegnkode == 39 || tegnkode == 34)) { Sitat = tegnkode; continue; }
            if (tegnkode == '\\' && Sitat != 39) { int Neste_plassere = KILDE[grunnlag_plassere + 읽는자리++]; if (Sitat == 34 && Neste_plassere != '$' && Neste_plassere != '"' && Neste_plassere != '\\') 넣기('\\'); 넣기(Neste_plassere); continue; }
            if (tegnkode == '$' && Sitat != 39 && 읽는자리 < avslutte_en_samtale_plassere) {
                boolean 중괄호자리 = KILDE[grunnlag_plassere + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < avslutte_en_samtale_plassere && KILDE[grunnlag_plassere + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < avslutte_en_samtale_plassere && 이름뒤(KILDE[grunnlag_plassere + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == avslutte_en_samtale_plassere || KILDE[grunnlag_plassere + 읽는자리] != '}')) { feil("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                variabel_VERDI(KILDE, grunnlag_plassere + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(tegnkode);
        }
        return !filtype_feil;
    }
    static int miljø_Innstillinger(int argument_INDEKS, boolean fjerne) {
        int lokal_START = 명령해석기.시작점[argument_INDEKS], avslutte_en_samtale_plassere = lokal_START + 명령해석기.lengde_VERDI[argument_INDEKS], 같음자리 = lokal_START;
        while (같음자리 < avslutte_en_samtale_plassere && 명령해석기.token_VERDI[같음자리] != '=') 같음자리++;
        int oppføring_ANTALL = 같음자리 - lokal_START;
        if (oppføring_ANTALL < 1 || oppføring_ANTALL > 31 || !navn_tegn(명령해석기.token_VERDI[lokal_START]) || !fjerne && 같음자리 == avslutte_en_samtale_plassere || avslutte_en_samtale_plassere - 같음자리 - 1 > 255) return 2;
        for (int Loop_INDEKS = lokal_START; Loop_INDEKS < 같음자리; Loop_INDEKS++) if (!이름뒤(명령해석기.token_VERDI[Loop_INDEKS])) return 2;
        if (område_SMS(명령해석기.token_VERDI, lokal_START, oppføring_ANTALL, "PWD") || område_SMS(명령해석기.token_VERDI, lokal_START, oppføring_ANTALL, "HOME")) return 2;
        int 찾은여부 = -1, informasjonssystemer_tom_status = -1;
        for (int Loop_INDEKS = 0; Loop_INDEKS < 16; Loop_INDEKS++) {
            if (이름길이[Loop_INDEKS] == 0) informasjonssystemer_tom_status = Loop_INDEKS;
            if (이름길이[Loop_INDEKS] != oppføring_ANTALL) continue;
            boolean SAMMENLIGNE = true; for (int indre_kobling_plassere = 0; indre_kobling_plassere < oppføring_ANTALL; indre_kobling_plassere++) if (variabel_navn[Loop_INDEKS * 32 + indre_kobling_plassere] != 명령해석기.token_VERDI[lokal_START + indre_kobling_plassere]) SAMMENLIGNE = false;
            if (SAMMENLIGNE) 찾은여부 = Loop_INDEKS;
        }
        if (fjerne) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = informasjonssystemer_tom_status; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = oppføring_ANTALL; VERDI_lengde[찾은여부] = avslutte_en_samtale_plassere - 같음자리 - 1;
        for (int Loop_INDEKS = 0; Loop_INDEKS < oppføring_ANTALL; Loop_INDEKS++) variabel_navn[찾은여부 * 32 + Loop_INDEKS] = 명령해석기.token_VERDI[lokal_START + Loop_INDEKS];
        for (int Loop_INDEKS = 같음자리 + 1; Loop_INDEKS < avslutte_en_samtale_plassere; Loop_INDEKS++) variabel_data[찾은여부 * 256 + Loop_INDEKS - 같음자리 - 1] = 명령해석기.token_VERDI[Loop_INDEKS];
        return 0;
    }
    static void vise_miljø() {
        단말.Skriv("HOME=/\nPWD="); Minne_Filer.betalt_skrive(); 단말.문자(10);
        for (int Loop_INDEKS = 0; Loop_INDEKS < 16; Loop_INDEKS++) if (이름길이[Loop_INDEKS] > 0) {
            for (int indre_kobling_plassere = 0; indre_kobling_plassere < 이름길이[Loop_INDEKS]; indre_kobling_plassere++) Tavle.직렬쓰기(variabel_navn[Loop_INDEKS * 32 + indre_kobling_plassere]); 단말.문자('=');
            for (int indre_kobling_plassere = 0; indre_kobling_plassere < VERDI_lengde[Loop_INDEKS]; indre_kobling_plassere++) Tavle.직렬쓰기(variabel_data[Loop_INDEKS * 256 + indre_kobling_plassere]); 단말.문자(10);
        }
    }
    static void Utfør_kommando(int[] data_MATRISE, int 시작변위, int oppføring_ANTALL, int 중첩깊이) {
        if (중첩깊이 >= 4 || oppføring_ANTALL > 4096) { feil("Kommando 파일의 nesting_VERDI 또는 Linje lengde_VERDI 제한을 넘었습니다"); return; }
        for (int Loop_INDEKS = 0; Loop_INDEKS < oppføring_ANTALL; Loop_INDEKS++) KILDE[중첩깊이 * 4096 + Loop_INDEKS] = data_MATRISE[시작변위 + Loop_INDEKS];
        int total_ANTALL = Les(oppføring_ANTALL, 중첩깊이); if (total_ANTALL < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < total_ANTALL) {
            int gruppe_avslutte_en_samtale = 읽는자리;
            while (gruppe_avslutte_en_samtale < total_ANTALL && (종류[중첩깊이 * 128 + gruppe_avslutte_en_samtale] == 0 || 종류[중첩깊이 * 128 + gruppe_avslutte_en_samtale] >= 4)) gruppe_avslutte_en_samtale++;
            boolean Utfør = 조건성립 == 1 || 조건성립 == 2 && status_VERDI == 0 || 조건성립 == 3 && status_VERDI != 0;
            if (Utfør) {
                boolean Forrige_vare_INDEKS = false;
                while (읽는자리 < gruppe_avslutte_en_samtale) {
                    int Neste_plassere = 읽는자리; while (Neste_plassere < gruppe_avslutte_en_samtale && 종류[중첩깊이 * 128 + Neste_plassere] != 4) Neste_plassere++;
                    boolean KOBLE_TIL_strøm = Neste_plassere < gruppe_avslutte_en_samtale; int inndata_page = -1, produksjon_page = -1, 출력방식 = 0;
                    명령해석기.token_ANTALL = 0; 쓴수 = 0; filtype_feil = false;
                    for (int Loop_INDEKS = 읽는자리; Loop_INDEKS < Neste_plassere; Loop_INDEKS++) {
                        int 자료종류 = 종류[중첩깊이 * 128 + Loop_INDEKS];
                        if (자료종류 >= 5) { if (자료종류 == 7) { if (inndata_page >= 0) { feil("inndata_VERDI 전환이 겹쳤습니다"); return; } inndata_page = ++Loop_INDEKS; } else { if (produksjon_page >= 0) { feil("Utgang 전환이 겹쳤습니다"); return; } produksjon_page = ++Loop_INDEKS; 출력방식 = 자료종류; } continue; }
                        if (명령해석기.token_ANTALL == 32) { feil("인수가 너무 많습니다"); return; }
                        int argument_INDEKS = 명령해석기.token_ANTALL++; 명령해석기.시작점[argument_INDEKS] = 쓴수;
                        if (!ord_VERDI(Loop_INDEKS, 중첩깊이)) return;
                        명령해석기.lengde_VERDI[argument_INDEKS] = 쓴수 - 명령해석기.시작점[argument_INDEKS];
                    }
                    연결중 = Forrige_vare_INDEKS || KOBLE_TIL_strøm || inndata_page >= 0 || produksjon_page >= 0;
                    if (연결중 && (명령해석기.같음(0, "vi") || 명령해석기.같음(0, "edit") || 명령해석기.같음(0, "load") || 명령해석기.같음(0, "gui") || 명령해석기.같음(0, "terminal") || 명령해석기.같음(0, "sh") || 명령해석기.같음(0, "source"))) { feil("interaktiv 명령과 Kommando 파일은 I_U 전환이나 strøm_VERDI 연결에 쓸 nummer 없습니다"); return; }
                    셸입출력.Kjør_2(Forrige_vare_INDEKS, KOBLE_TIL_strøm);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int oppføring_plassere = 입출력바꿈 == 0 ? inndata_page : produksjon_page; if (oppføring_plassere < 0) continue;
                        int START_plassere = 쓴수; if (!ord_VERDI(oppføring_plassere, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = Minne_Filer.bane_START(쓴수 - START_plassere);
                        for (int indre_kobling_plassere = START_plassere; 처리값 >= 0 && indre_kobling_plassere < 쓴수; indre_kobling_plassere++) 처리값 = Minne_Filer.bane_byte(indre_kobling_plassere - START_plassere, 명령해석기.token_VERDI[indre_kobling_plassere]);
                        if (처리값 >= 0) 처리값 = Minne_Filer.Åpne(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); 명령해석기.feil(처리값); status_VERDI = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.inndatafil = 처리값; else 셸입출력.utdatafil = 처리값;
                    }
                    셸입출력.Tillat_interaktiv = 중첩깊이 == 0 && 읽는자리 == 0 && Neste_plassere == total_ANTALL;
                    깊이 = 중첩깊이; 명령해석기.KR = 0; Tavle.입출력전환(1);
                    명령해석기.Kommando();
                    Tavle.Terminal(3);
                    int 반환값 = 명령해석기.KR, strøm_feil = 셸입출력.feil_VERDI;
                    셸입출력.끝(); 연결중 = false;
                    status_VERDI = strøm_feil < 0 ? 1 : 반환값;
                    if (strøm_feil < 0) { 명령해석기.feil(strøm_feil); return; }
                    if (skript_avslutte_en_samtale || 반환값 == -1005) return;
                    Forrige_vare_INDEKS = true; 읽는자리 = Neste_plassere + 1;
                }
            }
            if (gruppe_avslutte_en_samtale < total_ANTALL) 조건성립 = 종류[중첩깊이 * 128 + gruppe_avslutte_en_samtale];
            읽는자리 = gruppe_avslutte_en_samtale + 1;
        }
    }
    static void Utfør_Fil() {
        if (명령해석기.token_ANTALL != 2 || 깊이 >= 3) { 명령해석기.KR = 2; 단말.Skriv("사용법: sh Fil (nesting_VERDI 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = 명령해석기.Sti(1); if (처리값 >= 0) 처리값 = Minne_Filer.Åpne(0);
        if (처리값 < 0) { 명령해석기.feil(처리값); return; }
        int oppføring_ANTALL = 0, byte_data;
        while ((byte_data = Minne_Filer.Les(처리값)) != 256 && byte_data >= 0 && oppføring_ANTALL < 16384) skript_VERDI[중첩깊이 * 16384 + oppføring_ANTALL++] = byte_data;
        Minne_Filer.Lukk(처리값); Tavle.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < oppføring_ANTALL && !skript_avslutte_en_samtale;) {
            int avslutte_en_samtale_plassere = 읽는자리; while (avslutte_en_samtale_plassere < oppføring_ANTALL && skript_VERDI[중첩깊이 * 16384 + avslutte_en_samtale_plassere] != 10) avslutte_en_samtale_plassere++;
            int gyldig_lengde = avslutte_en_samtale_plassere - 읽는자리; if (gyldig_lengde > 0 && skript_VERDI[중첩깊이 * 16384 + avslutte_en_samtale_plassere - 1] == 13) gyldig_lengde--;
            Utfør_kommando(skript_VERDI, 중첩깊이 * 16384 + 읽는자리, gyldig_lengde, 중첩깊이); 읽는자리 = avslutte_en_samtale_plassere + 1;
        }
        명령해석기.KR = status_VERDI; skript_avslutte_en_samtale = false; 깊이 = 중첩깊이 - 1;
    }
}
