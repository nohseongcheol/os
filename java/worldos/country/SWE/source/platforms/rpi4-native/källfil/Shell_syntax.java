// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 interaktiv Shell 문법. 파이프는 순차 köra_kommando, 환경은 같은 셸에서 공유한다. */
public final class Shell_syntax {
    static int[] källfil = new int[4 * 4096], variant_värde = new int[4 * 128], Kör = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] variabel_namn = new int[16 * 32], variabel_data = new int[16 * 256], 이름길이 = new int[16], värde_längd = new int[16];
    static int[] skript_värde = new int[4 * 16384];
    static int status_värde, 깊이, 쓴수;
    static boolean 연결중, skript_avsluta, tillägg_fel;
    static boolean namn_tecken(int kodpunkt) { return kodpunkt >= 'a' && kodpunkt <= 'z' || kodpunkt >= 'A' && kodpunkt <= 'Z' || kodpunkt == '_' || kodpunkt >= 128; }
    static boolean 이름뒤(int kodpunkt) { return namn_tecken(kodpunkt) || kodpunkt >= '0' && kodpunkt <= '9'; }
    static void fel(String text) { Tavla.입출력전환(0); 단말.Skriv("kommando parsa_värde: "); 단말.Skriv(text); 단말.문자(10); status_värde = 2; }
    static int Läs(int post_ANTAL, int 중첩깊이) {
        int aktuellt_INDEX = 0, summa_ANTAL = 0, BAS_placera = 중첩깊이 * 4096, specialtecken = 중첩깊이 * 128;
        while (aktuellt_INDEX < post_ANTAL) {
            while (aktuellt_INDEX < post_ANTAL && (källfil[BAS_placera + aktuellt_INDEX] == 32 || källfil[BAS_placera + aktuellt_INDEX] == 9)) aktuellt_INDEX++;
            if (aktuellt_INDEX == post_ANTAL || källfil[BAS_placera + aktuellt_INDEX] == '#') break;
            if (summa_ANTAL == 128) { fel("낱말이 너무 많습니다"); return -1; }
            int START_placera = aktuellt_INDEX, kodpunkt = källfil[BAS_placera + aktuellt_INDEX], data_variant = 0;
            if (kodpunkt == ';') { data_variant = 1; aktuellt_INDEX++; }
            else if (kodpunkt == '&') { if (aktuellt_INDEX + 1 >= post_ANTAL || källfil[BAS_placera + aktuellt_INDEX + 1] != '&') { fel("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } data_variant = 2; aktuellt_INDEX += 2; }
            else if (kodpunkt == '|') { aktuellt_INDEX++; data_variant = aktuellt_INDEX < post_ANTAL && källfil[BAS_placera + aktuellt_INDEX] == '|' ? 3 : 4; if (data_variant == 3) aktuellt_INDEX++; }
            else if (kodpunkt == '>') { aktuellt_INDEX++; data_variant = aktuellt_INDEX < post_ANTAL && källfil[BAS_placera + aktuellt_INDEX] == '>' ? 6 : 5; if (data_variant == 6) aktuellt_INDEX++; }
            else if (kodpunkt == '<') { data_variant = 7; aktuellt_INDEX++; }
            else {
                int Citat = 0;
                while (aktuellt_INDEX < post_ANTAL) {
                    kodpunkt = källfil[BAS_placera + aktuellt_INDEX];
                    if (kodpunkt == '`' && Citat != 39 || kodpunkt == '$' && Citat != 39 && aktuellt_INDEX + 1 < post_ANTAL && källfil[BAS_placera + aktuellt_INDEX + 1] == '(') { fel("kommando RESULTAT 치환은 지원하지 않습니다"); return -1; }
                    if (kodpunkt == '\\' && Citat != 39) { if (++aktuellt_INDEX == post_ANTAL) { fel("inmatningsrad 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } aktuellt_INDEX++; continue; }
                    if (kodpunkt == Citat) { Citat = 0; aktuellt_INDEX++; continue; }
                    if (Citat == 0 && (kodpunkt == 39 || kodpunkt == 34)) { Citat = kodpunkt; aktuellt_INDEX++; continue; }
                    if (Citat == 0 && (kodpunkt == 32 || kodpunkt == 9 || kodpunkt == ';' || kodpunkt == '&' || kodpunkt == '|' || kodpunkt == '<' || kodpunkt == '>')) break;
                    aktuellt_INDEX++;
                }
                if (Citat != 0) { fel("따옴표가 닫히지 않았습니다"); return -1; }
                if (aktuellt_INDEX < post_ANTAL && (källfil[BAS_placera + aktuellt_INDEX] == '>' || källfil[BAS_placera + aktuellt_INDEX] == '<')) {
                    boolean 수치 = aktuellt_INDEX > START_placera;
                    for (int Loop_INDEX = START_placera; Loop_INDEX < aktuellt_INDEX; Loop_INDEX++) if (källfil[BAS_placera + Loop_INDEX] < '0' || källfil[BAS_placera + Loop_INDEX] > '9') 수치 = false;
                    if (수치) { fel("번호를 지정한 filnamn 서술자 indata_utleverans 전환은 지원하지 않습니다"); return -1; }
                }
            }
            variant_värde[specialtecken + summa_ANTAL] = data_variant; Kör[specialtecken + summa_ANTAL] = START_placera; 끝[specialtecken + summa_ANTAL] = aktuellt_INDEX; summa_ANTAL++;
        }
        boolean 낱말 = false;
        for (int Loop_INDEX = 0; Loop_INDEX < summa_ANTAL; Loop_INDEX++) {
            int 임시값 = variant_värde[specialtecken + Loop_INDEX];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++Loop_INDEX == summa_ANTAL || variant_värde[specialtecken + Loop_INDEX] != 0) { fel("indata_utleverans 전환에 filnamn 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || Loop_INDEX == summa_ANTAL - 1 && 임시값 != 1) { fel("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (summa_ANTAL > 0 && !낱말 && variant_värde[specialtecken + summa_ANTAL - 1] != 1) { fel("명령이 빠졌습니다"); return -1; }
        return summa_ANTAL;
    }
    static boolean område_SMS(int[] data_MATRIS, int lokal_START, int post_ANTAL, String tecken_placera) {
        if (post_ANTAL != tecken_placera.length()) return false; for (int Loop_INDEX = 0; Loop_INDEX < post_ANTAL; Loop_INDEX++) if (data_MATRIS[lokal_START + Loop_INDEX] != tecken_placera.charAt(Loop_INDEX)) return false; return true;
    }
    static void 넣기(int byte_data) {
        if (쓴수 >= 명령해석기.kod_värde.length) { if (!tillägg_fel) fel("변수를 펼친 명령이 너무 깁니다"); tillägg_fel = true; return; }
        명령해석기.kod_värde[쓴수++] = byte_data;
    }
    static void variabel_värde(int[] data_MATRIS, int START_placera, int post_ANTAL) {
        if (område_SMS(data_MATRIS, START_placera, post_ANTAL, "PWD")) { 넣기('/'); for (int Loop_INDEX = 0; Loop_INDEX < Minne_Filer.aktuellt_längd; Loop_INDEX++) 넣기(Minne_Filer.aktuellt_objekt[Loop_INDEX]); return; }
        if (område_SMS(data_MATRIS, START_placera, post_ANTAL, "HOME")) { 넣기('/'); return; }
        if (område_SMS(data_MATRIS, START_placera, post_ANTAL, "?")) {
            int data_värde = status_värde, siffra = 100; boolean 시작여부 = false;
            while (siffra > 0) { int 뒷값 = data_värde / siffra; if (뒷값 != 0 || 시작여부 || siffra == 1) { 넣기('0' + 뒷값); 시작여부 = true; } data_värde %= siffra; siffra /= 10; } return;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] == post_ANTAL) {
            boolean PASSA = true; for (int inre_koppling_placera = 0; inre_koppling_placera < post_ANTAL; inre_koppling_placera++) if (variabel_namn[Loop_INDEX * 32 + inre_koppling_placera] != data_MATRIS[START_placera + inre_koppling_placera]) PASSA = false;
            if (PASSA) { for (int inre_koppling_placera = 0; inre_koppling_placera < värde_längd[Loop_INDEX]; inre_koppling_placera++) 넣기(variabel_data[Loop_INDEX * 256 + inre_koppling_placera]); return; }
        }
    }
    static boolean Ord_värde(int 낱말번호, int 중첩깊이) {
        int läsa_markör = Kör[중첩깊이 * 128 + 낱말번호], avsluta_placera = 끝[중첩깊이 * 128 + 낱말번호], BAS_placera = 중첩깊이 * 4096, Citat = 0;
        if (läsa_markör < avsluta_placera && källfil[BAS_placera + läsa_markör] == '~' && (läsa_markör + 1 == avsluta_placera || källfil[BAS_placera + läsa_markör + 1] == '/')) { 넣기('/'); läsa_markör++; }
        while (läsa_markör < avsluta_placera) {
            int kodpunkt = källfil[BAS_placera + läsa_markör++];
            if (kodpunkt == Citat) { Citat = 0; continue; }
            if (Citat == 0 && (kodpunkt == 39 || kodpunkt == 34)) { Citat = kodpunkt; continue; }
            if (kodpunkt == '\\' && Citat != 39) { int Nästa_placera = källfil[BAS_placera + läsa_markör++]; if (Citat == 34 && Nästa_placera != '$' && Nästa_placera != '"' && Nästa_placera != '\\') 넣기('\\'); 넣기(Nästa_placera); continue; }
            if (kodpunkt == '$' && Citat != 39 && läsa_markör < avsluta_placera) {
                boolean 중괄호자리 = källfil[BAS_placera + läsa_markör] == '{'; if (중괄호자리) läsa_markör++;
                int 처음자리 = läsa_markör;
                if (läsa_markör < avsluta_placera && källfil[BAS_placera + läsa_markör] == '?') läsa_markör++;
                else while (läsa_markör < avsluta_placera && 이름뒤(källfil[BAS_placera + läsa_markör])) läsa_markör++;
                if (중괄호자리 && (läsa_markör == avsluta_placera || källfil[BAS_placera + läsa_markör] != '}')) { fel("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (läsa_markör == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                variabel_värde(källfil, BAS_placera + 처음자리, läsa_markör - 처음자리); if (중괄호자리) läsa_markör++; continue;
            }
            넣기(kodpunkt);
        }
        return !tillägg_fel;
    }
    static int miljö_Inställningar(int argument_INDEX, boolean ta_bort) {
        int lokal_START = 명령해석기.시작점[argument_INDEX], avsluta_placera = lokal_START + 명령해석기.längd_värde[argument_INDEX], 같음자리 = lokal_START;
        while (같음자리 < avsluta_placera && 명령해석기.kod_värde[같음자리] != '=') 같음자리++;
        int post_ANTAL = 같음자리 - lokal_START;
        if (post_ANTAL < 1 || post_ANTAL > 31 || !namn_tecken(명령해석기.kod_värde[lokal_START]) || !ta_bort && 같음자리 == avsluta_placera || avsluta_placera - 같음자리 - 1 > 255) return 2;
        for (int Loop_INDEX = lokal_START; Loop_INDEX < 같음자리; Loop_INDEX++) if (!이름뒤(명령해석기.kod_värde[Loop_INDEX])) return 2;
        if (område_SMS(명령해석기.kod_värde, lokal_START, post_ANTAL, "PWD") || område_SMS(명령해석기.kod_värde, lokal_START, post_ANTAL, "HOME")) return 2;
        int 찾은여부 = -1, 빈여부 = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] == 0) 빈여부 = Loop_INDEX;
            if (이름길이[Loop_INDEX] != post_ANTAL) continue;
            boolean PASSA = true; for (int inre_koppling_placera = 0; inre_koppling_placera < post_ANTAL; inre_koppling_placera++) if (variabel_namn[Loop_INDEX * 32 + inre_koppling_placera] != 명령해석기.kod_värde[lokal_START + inre_koppling_placera]) PASSA = false;
            if (PASSA) 찾은여부 = Loop_INDEX;
        }
        if (ta_bort) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = 빈여부; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = post_ANTAL; värde_längd[찾은여부] = avsluta_placera - 같음자리 - 1;
        for (int Loop_INDEX = 0; Loop_INDEX < post_ANTAL; Loop_INDEX++) variabel_namn[찾은여부 * 32 + Loop_INDEX] = 명령해석기.kod_värde[lokal_START + Loop_INDEX];
        for (int Loop_INDEX = 같음자리 + 1; Loop_INDEX < avsluta_placera; Loop_INDEX++) variabel_data[찾은여부 * 256 + Loop_INDEX - 같음자리 - 1] = 명령해석기.kod_värde[Loop_INDEX];
        return 0;
    }
    static void visa_miljö() {
        단말.Skriv("HOME=/\nPWD="); Minne_Filer.aktuellt_skriva(); 단말.문자(10);
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] > 0) {
            for (int inre_koppling_placera = 0; inre_koppling_placera < 이름길이[Loop_INDEX]; inre_koppling_placera++) Tavla.직렬쓰기(variabel_namn[Loop_INDEX * 32 + inre_koppling_placera]); 단말.문자('=');
            for (int inre_koppling_placera = 0; inre_koppling_placera < värde_längd[Loop_INDEX]; inre_koppling_placera++) Tavla.직렬쓰기(variabel_data[Loop_INDEX * 256 + inre_koppling_placera]); 단말.문자(10);
        }
    }
    static void köra_kommando(int[] data_MATRIS, int 시작변위, int post_ANTAL, int 중첩깊이) {
        if (중첩깊이 >= 4 || post_ANTAL > 4096) { fel("kommando 파일의 kapsling_värde 또는 inmatningsrad längd_värde 제한을 넘었습니다"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < post_ANTAL; Loop_INDEX++) källfil[중첩깊이 * 4096 + Loop_INDEX] = data_MATRIS[시작변위 + Loop_INDEX];
        int summa_ANTAL = Läs(post_ANTAL, 중첩깊이); if (summa_ANTAL < 0) return;
        int läsa_markör = 0, 조건성립 = 1;
        while (läsa_markör < summa_ANTAL) {
            int grupp_avsluta = läsa_markör;
            while (grupp_avsluta < summa_ANTAL && (variant_värde[중첩깊이 * 128 + grupp_avsluta] == 0 || variant_värde[중첩깊이 * 128 + grupp_avsluta] >= 4)) grupp_avsluta++;
            boolean köra = 조건성립 == 1 || 조건성립 == 2 && status_värde == 0 || 조건성립 == 3 && status_värde != 0;
            if (köra) {
                boolean Föregående_objekt_INDEX = false;
                while (läsa_markör < grupp_avsluta) {
                    int Nästa_placera = läsa_markör; while (Nästa_placera < grupp_avsluta && variant_värde[중첩깊이 * 128 + Nästa_placera] != 4) Nästa_placera++;
                    boolean ANSLUT_flöde = Nästa_placera < grupp_avsluta; int indata_page = -1, utleverans_page = -1, 출력방식 = 0;
                    명령해석기.kod_ANTAL = 0; 쓴수 = 0; tillägg_fel = false;
                    for (int Loop_INDEX = läsa_markör; Loop_INDEX < Nästa_placera; Loop_INDEX++) {
                        int data_variant = variant_värde[중첩깊이 * 128 + Loop_INDEX];
                        if (data_variant >= 5) { if (data_variant == 7) { if (indata_page >= 0) { fel("indata_värde 전환이 겹쳤습니다"); return; } indata_page = ++Loop_INDEX; } else { if (utleverans_page >= 0) { fel("utmatningsposition 전환이 겹쳤습니다"); return; } utleverans_page = ++Loop_INDEX; 출력방식 = data_variant; } continue; }
                        if (명령해석기.kod_ANTAL == 32) { fel("인수가 너무 많습니다"); return; }
                        int argument_INDEX = 명령해석기.kod_ANTAL++; 명령해석기.시작점[argument_INDEX] = 쓴수;
                        if (!Ord_värde(Loop_INDEX, 중첩깊이)) return;
                        명령해석기.längd_värde[argument_INDEX] = 쓴수 - 명령해석기.시작점[argument_INDEX];
                    }
                    연결중 = Föregående_objekt_INDEX || ANSLUT_flöde || indata_page >= 0 || utleverans_page >= 0;
                    if (연결중 && (명령해석기.같음(0, "vi") || 명령해석기.같음(0, "edit") || 명령해석기.같음(0, "load") || 명령해석기.같음(0, "gui") || 명령해석기.같음(0, "terminal") || 명령해석기.같음(0, "sh") || 명령해석기.같음(0, "source"))) { fel("interaktiv 명령과 kommando 파일은 indata_utleverans 전환이나 flöde_värde 연결에 쓸 nummer 없습니다"); return; }
                    셸입출력.Kör(Föregående_objekt_INDEX, ANSLUT_flöde);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int post_placera = 입출력바꿈 == 0 ? indata_page : utleverans_page; if (post_placera < 0) continue;
                        int START_placera = 쓴수; if (!Ord_värde(post_placera, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = Minne_Filer.väg_START(쓴수 - START_placera);
                        for (int inre_koppling_placera = START_placera; 처리값 >= 0 && inre_koppling_placera < 쓴수; inre_koppling_placera++) 처리값 = Minne_Filer.väg_byte(inre_koppling_placera - START_placera, 명령해석기.kod_värde[inre_koppling_placera]);
                        if (처리값 >= 0) 처리값 = Minne_Filer.Öppna(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); 명령해석기.fel(처리값); status_värde = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.indatafil = 처리값; else 셸입출력.utdatafil = 처리값;
                    }
                    셸입출력.Tillåt_interaktiv = 중첩깊이 == 0 && läsa_markör == 0 && Nästa_placera == summa_ANTAL;
                    깊이 = 중첩깊이; 명령해석기.RESULTAT = 0; Tavla.입출력전환(1);
                    명령해석기.kommando();
                    Tavla.kommandotolk(3);
                    int 반환값 = 명령해석기.RESULTAT, flöde_fel = 셸입출력.fel_värde;
                    셸입출력.끝(); 연결중 = false;
                    status_värde = flöde_fel < 0 ? 1 : 반환값;
                    if (flöde_fel < 0) { 명령해석기.fel(flöde_fel); return; }
                    if (skript_avsluta || 반환값 == -1005) return;
                    Föregående_objekt_INDEX = true; läsa_markör = Nästa_placera + 1;
                }
            }
            if (grupp_avsluta < summa_ANTAL) 조건성립 = variant_värde[중첩깊이 * 128 + grupp_avsluta];
            läsa_markör = grupp_avsluta + 1;
        }
    }
    static void köra_fil() {
        if (명령해석기.kod_ANTAL != 2 || 깊이 >= 3) { 명령해석기.RESULTAT = 2; 단말.Skriv("사용법: sh filnamn (kapsling_värde 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = 명령해석기.sökväg_2(1); if (처리값 >= 0) 처리값 = Minne_Filer.Öppna(0);
        if (처리값 < 0) { 명령해석기.fel(처리값); return; }
        int post_ANTAL = 0, byte_data;
        while ((byte_data = Minne_Filer.Läs(처리값)) != 256 && byte_data >= 0 && post_ANTAL < 16384) skript_värde[중첩깊이 * 16384 + post_ANTAL++] = byte_data;
        Minne_Filer.Stäng(처리값); Tavla.입출력전환(0);
        for (int läsa_markör = 0; läsa_markör < post_ANTAL && !skript_avsluta;) {
            int avsluta_placera = läsa_markör; while (avsluta_placera < post_ANTAL && skript_värde[중첩깊이 * 16384 + avsluta_placera] != 10) avsluta_placera++;
            int giltig_längd = avsluta_placera - läsa_markör; if (giltig_längd > 0 && skript_värde[중첩깊이 * 16384 + avsluta_placera - 1] == 13) giltig_längd--;
            köra_kommando(skript_värde, 중첩깊이 * 16384 + läsa_markör, giltig_längd, 중첩깊이); läsa_markör = avsluta_placera + 1;
        }
        명령해석기.RESULTAT = status_värde; skript_avsluta = false; 깊이 = 중첩깊이 - 1;
    }
}
