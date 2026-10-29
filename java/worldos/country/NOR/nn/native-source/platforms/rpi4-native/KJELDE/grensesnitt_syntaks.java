// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 interaktiv grensesnitt 문법. 파이프는 순차 Utfør_kommando, 환경은 같은 셸에서 공유한다. */
public final class grensesnitt_syntaks {
    static int[] KJELDE = new int[4 * 4096], 종류 = new int[4 * 128], Køyr_2 = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] variabel_namn = new int[16 * 32], variabel_data = new int[16 * 256], 이름길이 = new int[16], VALUE_lengd = new int[16];
    static int[] skript_VALUE = new int[4 * 16384];
    static int status_VALUE, 깊이, 쓴수;
    static boolean 연결중, skript_avslutte, filtype_feil;
    static boolean namn_teikn(int teiknkode) { return teiknkode >= 'a' && teiknkode <= 'z' || teiknkode >= 'A' && teiknkode <= 'Z' || teiknkode == '_' || teiknkode >= 128; }
    static boolean 이름뒤(int teiknkode) { return namn_teikn(teiknkode) || teiknkode >= '0' && teiknkode <= '9'; }
    static void FEIL(String Tekst) { Tavle.입출력전환(0); 단말.Skriv("Kommando dele_opp_VALUE: "); 단말.Skriv(Tekst); 단말.문자(10); status_VALUE = 2; }
    static int Les(int oppføring_COUNT, int 중첩깊이) {
        int betalt_INDEX = 0, 총수 = 0, BASE_plassere = 중첩깊이 * 4096, spesialteikn = 중첩깊이 * 128;
        while (betalt_INDEX < oppføring_COUNT) {
            while (betalt_INDEX < oppføring_COUNT && (KJELDE[BASE_plassere + betalt_INDEX] == 32 || KJELDE[BASE_plassere + betalt_INDEX] == 9)) betalt_INDEX++;
            if (betalt_INDEX == oppføring_COUNT || KJELDE[BASE_plassere + betalt_INDEX] == '#') break;
            if (총수 == 128) { FEIL("낱말이 너무 많습니다"); return -1; }
            int START_plassere = betalt_INDEX, teiknkode = KJELDE[BASE_plassere + betalt_INDEX], 자료종류 = 0;
            if (teiknkode == ';') { 자료종류 = 1; betalt_INDEX++; }
            else if (teiknkode == '&') { if (betalt_INDEX + 1 >= oppføring_COUNT || KJELDE[BASE_plassere + betalt_INDEX + 1] != '&') { FEIL("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } 자료종류 = 2; betalt_INDEX += 2; }
            else if (teiknkode == '|') { betalt_INDEX++; 자료종류 = betalt_INDEX < oppføring_COUNT && KJELDE[BASE_plassere + betalt_INDEX] == '|' ? 3 : 4; if (자료종류 == 3) betalt_INDEX++; }
            else if (teiknkode == '>') { betalt_INDEX++; 자료종류 = betalt_INDEX < oppføring_COUNT && KJELDE[BASE_plassere + betalt_INDEX] == '>' ? 6 : 5; if (자료종류 == 6) betalt_INDEX++; }
            else if (teiknkode == '<') { 자료종류 = 7; betalt_INDEX++; }
            else {
                int Sitat = 0;
                while (betalt_INDEX < oppføring_COUNT) {
                    teiknkode = KJELDE[BASE_plassere + betalt_INDEX];
                    if (teiknkode == '`' && Sitat != 39 || teiknkode == '$' && Sitat != 39 && betalt_INDEX + 1 < oppføring_COUNT && KJELDE[BASE_plassere + betalt_INDEX + 1] == '(') { FEIL("Kommando forretningsmål 치환은 지원하지 않습니다"); return -1; }
                    if (teiknkode == '\\' && Sitat != 39) { if (++betalt_INDEX == oppføring_COUNT) { FEIL("linje 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } betalt_INDEX++; continue; }
                    if (teiknkode == Sitat) { Sitat = 0; betalt_INDEX++; continue; }
                    if (Sitat == 0 && (teiknkode == 39 || teiknkode == 34)) { Sitat = teiknkode; betalt_INDEX++; continue; }
                    if (Sitat == 0 && (teiknkode == 32 || teiknkode == 9 || teiknkode == ';' || teiknkode == '&' || teiknkode == '|' || teiknkode == '<' || teiknkode == '>')) break;
                    betalt_INDEX++;
                }
                if (Sitat != 0) { FEIL("따옴표가 닫히지 않았습니다"); return -1; }
                if (betalt_INDEX < oppføring_COUNT && (KJELDE[BASE_plassere + betalt_INDEX] == '>' || KJELDE[BASE_plassere + betalt_INDEX] == '<')) {
                    boolean 수치 = betalt_INDEX > START_plassere;
                    for (int Loop_INDEX = START_plassere; Loop_INDEX < betalt_INDEX; Loop_INDEX++) if (KJELDE[BASE_plassere + Loop_INDEX] < '0' || KJELDE[BASE_plassere + Loop_INDEX] > '9') 수치 = false;
                    if (수치) { FEIL("번호를 지정한 Fil 서술자 I_U 전환은 지원하지 않습니다"); return -1; }
                }
            }
            종류[spesialteikn + 총수] = 자료종류; Køyr_2[spesialteikn + 총수] = START_plassere; 끝[spesialteikn + 총수] = betalt_INDEX; 총수++;
        }
        boolean 낱말 = false;
        for (int Loop_INDEX = 0; Loop_INDEX < 총수; Loop_INDEX++) {
            int 임시값 = 종류[spesialteikn + Loop_INDEX];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++Loop_INDEX == 총수 || 종류[spesialteikn + Loop_INDEX] != 0) { FEIL("I_U 전환에 Fil 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || Loop_INDEX == 총수 - 1 && 임시값 != 1) { FEIL("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (총수 > 0 && !낱말 && 종류[spesialteikn + 총수 - 1] != 1) { FEIL("명령이 빠졌습니다"); return -1; }
        return 총수;
    }
    static boolean 구간말(int[] data_ARRAY, int lokal_START, int oppføring_COUNT, String teikn_plassere) {
        if (oppføring_COUNT != teikn_plassere.length()) return false; for (int Loop_INDEX = 0; Loop_INDEX < oppføring_COUNT; Loop_INDEX++) if (data_ARRAY[lokal_START + Loop_INDEX] != teikn_plassere.charAt(Loop_INDEX)) return false; return true;
    }
    static void 넣기(int byte_data) {
        if (쓴수 >= 명령해석기.token_VALUE.length) { if (!filtype_feil) FEIL("변수를 펼친 명령이 너무 깁니다"); filtype_feil = true; return; }
        명령해석기.token_VALUE[쓴수++] = byte_data;
    }
    static void variabel_VALUE(int[] data_ARRAY, int START_plassere, int oppføring_COUNT) {
        if (구간말(data_ARRAY, START_plassere, oppføring_COUNT, "PWD")) { 넣기('/'); for (int Loop_INDEX = 0; Loop_INDEX < Minne_Filer.betalt_lengd; Loop_INDEX++) 넣기(Minne_Filer.betalt_vare[Loop_INDEX]); return; }
        if (구간말(data_ARRAY, START_plassere, oppføring_COUNT, "HOME")) { 넣기('/'); return; }
        if (구간말(data_ARRAY, START_plassere, oppføring_COUNT, "?")) {
            int data_VALUE = status_VALUE, siffer = 100; boolean 시작여부 = false;
            while (siffer > 0) { int 뒷값 = data_VALUE / siffer; if (뒷값 != 0 || 시작여부 || siffer == 1) { 넣기('0' + 뒷값); 시작여부 = true; } data_VALUE %= siffer; siffer /= 10; } return;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] == oppføring_COUNT) {
            boolean MATCH = true; for (int indre_kopling_plassere = 0; indre_kopling_plassere < oppføring_COUNT; indre_kopling_plassere++) if (variabel_namn[Loop_INDEX * 32 + indre_kopling_plassere] != data_ARRAY[START_plassere + indre_kopling_plassere]) MATCH = false;
            if (MATCH) { for (int indre_kopling_plassere = 0; indre_kopling_plassere < VALUE_lengd[Loop_INDEX]; indre_kopling_plassere++) 넣기(variabel_data[Loop_INDEX * 256 + indre_kopling_plassere]); return; }
        }
    }
    static boolean Word_VALUE(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = Køyr_2[중첩깊이 * 128 + 낱말번호], avslutte_plassere = 끝[중첩깊이 * 128 + 낱말번호], BASE_plassere = 중첩깊이 * 4096, Sitat = 0;
        if (읽는자리 < avslutte_plassere && KJELDE[BASE_plassere + 읽는자리] == '~' && (읽는자리 + 1 == avslutte_plassere || KJELDE[BASE_plassere + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < avslutte_plassere) {
            int teiknkode = KJELDE[BASE_plassere + 읽는자리++];
            if (teiknkode == Sitat) { Sitat = 0; continue; }
            if (Sitat == 0 && (teiknkode == 39 || teiknkode == 34)) { Sitat = teiknkode; continue; }
            if (teiknkode == '\\' && Sitat != 39) { int Neste_plassere = KJELDE[BASE_plassere + 읽는자리++]; if (Sitat == 34 && Neste_plassere != '$' && Neste_plassere != '"' && Neste_plassere != '\\') 넣기('\\'); 넣기(Neste_plassere); continue; }
            if (teiknkode == '$' && Sitat != 39 && 읽는자리 < avslutte_plassere) {
                boolean 중괄호자리 = KJELDE[BASE_plassere + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < avslutte_plassere && KJELDE[BASE_plassere + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < avslutte_plassere && 이름뒤(KJELDE[BASE_plassere + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == avslutte_plassere || KJELDE[BASE_plassere + 읽는자리] != '}')) { FEIL("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                variabel_VALUE(KJELDE, BASE_plassere + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(teiknkode);
        }
        return !filtype_feil;
    }
    static int 환경설정(int argument_INDEX, boolean fjerne) {
        int lokal_START = 명령해석기.시작점[argument_INDEX], avslutte_plassere = lokal_START + 명령해석기.lengd_VALUE[argument_INDEX], 같음자리 = lokal_START;
        while (같음자리 < avslutte_plassere && 명령해석기.token_VALUE[같음자리] != '=') 같음자리++;
        int oppføring_COUNT = 같음자리 - lokal_START;
        if (oppføring_COUNT < 1 || oppføring_COUNT > 31 || !namn_teikn(명령해석기.token_VALUE[lokal_START]) || !fjerne && 같음자리 == avslutte_plassere || avslutte_plassere - 같음자리 - 1 > 255) return 2;
        for (int Loop_INDEX = lokal_START; Loop_INDEX < 같음자리; Loop_INDEX++) if (!이름뒤(명령해석기.token_VALUE[Loop_INDEX])) return 2;
        if (구간말(명령해석기.token_VALUE, lokal_START, oppføring_COUNT, "PWD") || 구간말(명령해석기.token_VALUE, lokal_START, oppføring_COUNT, "HOME")) return 2;
        int 찾은여부 = -1, informasjonsteknologi_tom_status = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] == 0) informasjonsteknologi_tom_status = Loop_INDEX;
            if (이름길이[Loop_INDEX] != oppføring_COUNT) continue;
            boolean MATCH = true; for (int indre_kopling_plassere = 0; indre_kopling_plassere < oppføring_COUNT; indre_kopling_plassere++) if (variabel_namn[Loop_INDEX * 32 + indre_kopling_plassere] != 명령해석기.token_VALUE[lokal_START + indre_kopling_plassere]) MATCH = false;
            if (MATCH) 찾은여부 = Loop_INDEX;
        }
        if (fjerne) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = informasjonsteknologi_tom_status; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = oppføring_COUNT; VALUE_lengd[찾은여부] = avslutte_plassere - 같음자리 - 1;
        for (int Loop_INDEX = 0; Loop_INDEX < oppføring_COUNT; Loop_INDEX++) variabel_namn[찾은여부 * 32 + Loop_INDEX] = 명령해석기.token_VALUE[lokal_START + Loop_INDEX];
        for (int Loop_INDEX = 같음자리 + 1; Loop_INDEX < avslutte_plassere; Loop_INDEX++) variabel_data[찾은여부 * 256 + Loop_INDEX - 같음자리 - 1] = 명령해석기.token_VALUE[Loop_INDEX];
        return 0;
    }
    static void 환경보기() {
        단말.Skriv("HOME=/\nPWD="); Minne_Filer.betalt_skrive(); 단말.문자(10);
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] > 0) {
            for (int indre_kopling_plassere = 0; indre_kopling_plassere < 이름길이[Loop_INDEX]; indre_kopling_plassere++) Tavle.직렬쓰기(variabel_namn[Loop_INDEX * 32 + indre_kopling_plassere]); 단말.문자('=');
            for (int indre_kopling_plassere = 0; indre_kopling_plassere < VALUE_lengd[Loop_INDEX]; indre_kopling_plassere++) Tavle.직렬쓰기(variabel_data[Loop_INDEX * 256 + indre_kopling_plassere]); 단말.문자(10);
        }
    }
    static void Utfør_kommando(int[] data_ARRAY, int 시작변위, int oppføring_COUNT, int 중첩깊이) {
        if (중첩깊이 >= 4 || oppføring_COUNT > 4096) { FEIL("Kommando 파일의 중첩 또는 linje lengd_VALUE 제한을 넘었습니다"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < oppføring_COUNT; Loop_INDEX++) KJELDE[중첩깊이 * 4096 + Loop_INDEX] = data_ARRAY[시작변위 + Loop_INDEX];
        int 총수 = Les(oppføring_COUNT, 중첩깊이); if (총수 < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < 총수) {
            int gruppe_avslutte = 읽는자리;
            while (gruppe_avslutte < 총수 && (종류[중첩깊이 * 128 + gruppe_avslutte] == 0 || 종류[중첩깊이 * 128 + gruppe_avslutte] >= 4)) gruppe_avslutte++;
            boolean Utfør = 조건성립 == 1 || 조건성립 == 2 && status_VALUE == 0 || 조건성립 == 3 && status_VALUE != 0;
            if (Utfør) {
                boolean 이전자리 = false;
                while (읽는자리 < gruppe_avslutte) {
                    int Neste_plassere = 읽는자리; while (Neste_plassere < gruppe_avslutte && 종류[중첩깊이 * 128 + Neste_plassere] != 4) Neste_plassere++;
                    boolean KOPLE_TIL_Stream = Neste_plassere < gruppe_avslutte; int 입력쪽 = -1, 출력쪽 = -1, 출력방식 = 0;
                    명령해석기.token_COUNT = 0; 쓴수 = 0; filtype_feil = false;
                    for (int Loop_INDEX = 읽는자리; Loop_INDEX < Neste_plassere; Loop_INDEX++) {
                        int 자료종류 = 종류[중첩깊이 * 128 + Loop_INDEX];
                        if (자료종류 >= 5) { if (자료종류 == 7) { if (입력쪽 >= 0) { FEIL("입력 전환이 겹쳤습니다"); return; } 입력쪽 = ++Loop_INDEX; } else { if (출력쪽 >= 0) { FEIL("Utdata 전환이 겹쳤습니다"); return; } 출력쪽 = ++Loop_INDEX; 출력방식 = 자료종류; } continue; }
                        if (명령해석기.token_COUNT == 32) { FEIL("인수가 너무 많습니다"); return; }
                        int argument_INDEX = 명령해석기.token_COUNT++; 명령해석기.시작점[argument_INDEX] = 쓴수;
                        if (!Word_VALUE(Loop_INDEX, 중첩깊이)) return;
                        명령해석기.lengd_VALUE[argument_INDEX] = 쓴수 - 명령해석기.시작점[argument_INDEX];
                    }
                    연결중 = 이전자리 || KOPLE_TIL_Stream || 입력쪽 >= 0 || 출력쪽 >= 0;
                    if (연결중 && (명령해석기.같음(0, "vi") || 명령해석기.같음(0, "edit") || 명령해석기.같음(0, "load") || 명령해석기.같음(0, "gui") || 명령해석기.같음(0, "terminal") || 명령해석기.같음(0, "sh") || 명령해석기.같음(0, "source"))) { FEIL("interaktiv 명령과 Kommando 파일은 I_U 전환이나 Stream_VALUE 연결에 쓸 수 없습니다"); return; }
                    셸입출력.Køyr_2(이전자리, KOPLE_TIL_Stream);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int oppføring_plassere = 입출력바꿈 == 0 ? 입력쪽 : 출력쪽; if (oppføring_plassere < 0) continue;
                        int START_plassere = 쓴수; if (!Word_VALUE(oppføring_plassere, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = Minne_Filer.bane_START(쓴수 - START_plassere);
                        for (int indre_kopling_plassere = START_plassere; 처리값 >= 0 && indre_kopling_plassere < 쓴수; indre_kopling_plassere++) 처리값 = Minne_Filer.bane_byte(indre_kopling_plassere - START_plassere, 명령해석기.token_VALUE[indre_kopling_plassere]);
                        if (처리값 >= 0) 처리값 = Minne_Filer.Opna(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); 명령해석기.FEIL(처리값); status_VALUE = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.입력파일 = 처리값; else 셸입출력.utdatafil = 처리값;
                    }
                    셸입출력.Tillat_interaktiv = 중첩깊이 == 0 && 읽는자리 == 0 && Neste_plassere == 총수;
                    깊이 = 중첩깊이; 명령해석기.forretningsmål = 0; Tavle.입출력전환(1);
                    명령해석기.Kommando();
                    Tavle.Terminal(3);
                    int 반환값 = 명령해석기.forretningsmål, Stream_feil = 셸입출력.feil_VALUE;
                    셸입출력.끝(); 연결중 = false;
                    status_VALUE = Stream_feil < 0 ? 1 : 반환값;
                    if (Stream_feil < 0) { 명령해석기.FEIL(Stream_feil); return; }
                    if (skript_avslutte || 반환값 == -1005) return;
                    이전자리 = true; 읽는자리 = Neste_plassere + 1;
                }
            }
            if (gruppe_avslutte < 총수) 조건성립 = 종류[중첩깊이 * 128 + gruppe_avslutte];
            읽는자리 = gruppe_avslutte + 1;
        }
    }
    static void Utfør_fil() {
        if (명령해석기.token_COUNT != 2 || 깊이 >= 3) { 명령해석기.forretningsmål = 2; 단말.Skriv("사용법: sh Fil (중첩 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = 명령해석기.STIGE(1); if (처리값 >= 0) 처리값 = Minne_Filer.Opna(0);
        if (처리값 < 0) { 명령해석기.FEIL(처리값); return; }
        int oppføring_COUNT = 0, byte_data;
        while ((byte_data = Minne_Filer.Les(처리값)) != 256 && byte_data >= 0 && oppføring_COUNT < 16384) skript_VALUE[중첩깊이 * 16384 + oppføring_COUNT++] = byte_data;
        Minne_Filer.Lukk(처리값); Tavle.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < oppføring_COUNT && !skript_avslutte;) {
            int avslutte_plassere = 읽는자리; while (avslutte_plassere < oppføring_COUNT && skript_VALUE[중첩깊이 * 16384 + avslutte_plassere] != 10) avslutte_plassere++;
            int 유효길이 = avslutte_plassere - 읽는자리; if (유효길이 > 0 && skript_VALUE[중첩깊이 * 16384 + avslutte_plassere - 1] == 13) 유효길이--;
            Utfør_kommando(skript_VALUE, 중첩깊이 * 16384 + 읽는자리, 유효길이, 중첩깊이); 읽는자리 = avslutte_plassere + 1;
        }
        명령해석기.forretningsmål = status_VALUE; skript_avslutte = false; 깊이 = 중첩깊이 - 1;
    }
}
