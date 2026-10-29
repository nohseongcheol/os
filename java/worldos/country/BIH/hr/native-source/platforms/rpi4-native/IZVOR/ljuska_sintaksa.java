// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 대화형 ljuska 문법. 파이프는 순차 Izvrši_naredba, 환경은 같은 셸에서 공유한다. */
public final class ljuska_sintaksa {
    static int[] IZVOR = new int[4 * 4096], 종류 = new int[4 * 128], Pokreni = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] varijabla_naziv = new int[16 * 32], varijabla_podaci = new int[16 * 256], 이름길이 = new int[16], 값길이 = new int[16];
    static int[] skripta_VALUE = new int[4 * 16384];
    static int Stanje_VALUE, 깊이, 쓴수;
    static boolean 연결중, skripta_završiti_razgovor, nastavak_pogreška;
    static boolean naziv_znak(int kodna_točka) { return kodna_točka >= 'a' && kodna_točka <= 'z' || kodna_točka >= 'A' && kodna_točka <= 'Z' || kodna_točka == '_' || kodna_točka >= 128; }
    static boolean 이름뒤(int kodna_točka) { return naziv_znak(kodna_točka) || kodna_točka >= '0' && kodna_točka <= '9'; }
    static void GREŠKA(String Tekst) { pano.입출력전환(0); 단말.Zapisuj("Naredba rastavljati_VALUE: "); 단말.Zapisuj(Tekst); 단말.문자(10); Stanje_VALUE = 2; }
    static int Čitaj(int unos_COUNT, int 중첩깊이) {
        int redovno_INDEX = 0, ukupni_zbroj_COUNT = 0, BASE_položaj = 중첩깊이 * 4096, posebni_znak = 중첩깊이 * 128;
        while (redovno_INDEX < unos_COUNT) {
            while (redovno_INDEX < unos_COUNT && (IZVOR[BASE_položaj + redovno_INDEX] == 32 || IZVOR[BASE_položaj + redovno_INDEX] == 9)) redovno_INDEX++;
            if (redovno_INDEX == unos_COUNT || IZVOR[BASE_položaj + redovno_INDEX] == '#') break;
            if (ukupni_zbroj_COUNT == 128) { GREŠKA("낱말이 너무 많습니다"); return -1; }
            int START_položaj = redovno_INDEX, kodna_točka = IZVOR[BASE_položaj + redovno_INDEX], 자료종류 = 0;
            if (kodna_točka == ';') { 자료종류 = 1; redovno_INDEX++; }
            else if (kodna_točka == '&') { if (redovno_INDEX + 1 >= unos_COUNT || IZVOR[BASE_položaj + redovno_INDEX + 1] != '&') { GREŠKA("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } 자료종류 = 2; redovno_INDEX += 2; }
            else if (kodna_točka == '|') { redovno_INDEX++; 자료종류 = redovno_INDEX < unos_COUNT && IZVOR[BASE_položaj + redovno_INDEX] == '|' ? 3 : 4; if (자료종류 == 3) redovno_INDEX++; }
            else if (kodna_točka == '>') { redovno_INDEX++; 자료종류 = redovno_INDEX < unos_COUNT && IZVOR[BASE_položaj + redovno_INDEX] == '>' ? 6 : 5; if (자료종류 == 6) redovno_INDEX++; }
            else if (kodna_točka == '<') { 자료종류 = 7; redovno_INDEX++; }
            else {
                int Citat = 0;
                while (redovno_INDEX < unos_COUNT) {
                    kodna_točka = IZVOR[BASE_položaj + redovno_INDEX];
                    if (kodna_točka == '`' && Citat != 39 || kodna_točka == '$' && Citat != 39 && redovno_INDEX + 1 < unos_COUNT && IZVOR[BASE_položaj + redovno_INDEX + 1] == '(') { GREŠKA("Naredba REZULTAT 치환은 지원하지 않습니다"); return -1; }
                    if (kodna_točka == '\\' && Citat != 39) { if (++redovno_INDEX == unos_COUNT) { GREŠKA("red 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } redovno_INDEX++; continue; }
                    if (kodna_točka == Citat) { Citat = 0; redovno_INDEX++; continue; }
                    if (Citat == 0 && (kodna_točka == 39 || kodna_točka == 34)) { Citat = kodna_točka; redovno_INDEX++; continue; }
                    if (Citat == 0 && (kodna_točka == 32 || kodna_točka == 9 || kodna_točka == ';' || kodna_točka == '&' || kodna_točka == '|' || kodna_točka == '<' || kodna_točka == '>')) break;
                    redovno_INDEX++;
                }
                if (Citat != 0) { GREŠKA("따옴표가 닫히지 않았습니다"); return -1; }
                if (redovno_INDEX < unos_COUNT && (IZVOR[BASE_položaj + redovno_INDEX] == '>' || IZVOR[BASE_položaj + redovno_INDEX] == '<')) {
                    boolean 수치 = redovno_INDEX > START_položaj;
                    for (int Loop_INDEX = START_položaj; Loop_INDEX < redovno_INDEX; Loop_INDEX++) if (IZVOR[BASE_položaj + Loop_INDEX] < '0' || IZVOR[BASE_položaj + Loop_INDEX] > '9') 수치 = false;
                    if (수치) { GREŠKA("번호를 지정한 Datoteka 서술자 U_I 전환은 지원하지 않습니다"); return -1; }
                }
            }
            종류[posebni_znak + ukupni_zbroj_COUNT] = 자료종류; Pokreni[posebni_znak + ukupni_zbroj_COUNT] = START_položaj; 끝[posebni_znak + ukupni_zbroj_COUNT] = redovno_INDEX; ukupni_zbroj_COUNT++;
        }
        boolean 낱말 = false;
        for (int Loop_INDEX = 0; Loop_INDEX < ukupni_zbroj_COUNT; Loop_INDEX++) {
            int 임시값 = 종류[posebni_znak + Loop_INDEX];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++Loop_INDEX == ukupni_zbroj_COUNT || 종류[posebni_znak + Loop_INDEX] != 0) { GREŠKA("U_I 전환에 Datoteka 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || Loop_INDEX == ukupni_zbroj_COUNT - 1 && 임시값 != 1) { GREŠKA("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (ukupni_zbroj_COUNT > 0 && !낱말 && 종류[posebni_znak + ukupni_zbroj_COUNT - 1] != 1) { GREŠKA("명령이 빠졌습니다"); return -1; }
        return ukupni_zbroj_COUNT;
    }
    static boolean raspon_SMS(int[] podaci_ARRAY, int lokalno_START, int unos_COUNT, String znak_položaj) {
        if (unos_COUNT != znak_položaj.length()) return false; for (int Loop_INDEX = 0; Loop_INDEX < unos_COUNT; Loop_INDEX++) if (podaci_ARRAY[lokalno_START + Loop_INDEX] != znak_položaj.charAt(Loop_INDEX)) return false; return true;
    }
    static void 넣기(int bajt_podaci) {
        if (쓴수 >= 명령해석기.token_VALUE.length) { if (!nastavak_pogreška) GREŠKA("변수를 펼친 명령이 너무 깁니다"); nastavak_pogreška = true; return; }
        명령해석기.token_VALUE[쓴수++] = bajt_podaci;
    }
    static void varijabla_VALUE(int[] podaci_ARRAY, int START_položaj, int unos_COUNT) {
        if (raspon_SMS(podaci_ARRAY, START_položaj, unos_COUNT, "PWD")) { 넣기('/'); for (int Loop_INDEX = 0; Loop_INDEX < Memorija_Datoteke.현재길이; Loop_INDEX++) 넣기(Memorija_Datoteke.redovno_artikl[Loop_INDEX]); return; }
        if (raspon_SMS(podaci_ARRAY, START_položaj, unos_COUNT, "HOME")) { 넣기('/'); return; }
        if (raspon_SMS(podaci_ARRAY, START_položaj, unos_COUNT, "?")) {
            int podaci_VALUE = Stanje_VALUE, znamenka = 100; boolean 시작여부 = false;
            while (znamenka > 0) { int 뒷값 = podaci_VALUE / znamenka; if (뒷값 != 0 || 시작여부 || znamenka == 1) { 넣기('0' + 뒷값); 시작여부 = true; } podaci_VALUE %= znamenka; znamenka /= 10; } return;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] == unos_COUNT) {
            boolean MATCH = true; for (int unutarnji_položaj = 0; unutarnji_položaj < unos_COUNT; unutarnji_položaj++) if (varijabla_naziv[Loop_INDEX * 32 + unutarnji_položaj] != podaci_ARRAY[START_položaj + unutarnji_položaj]) MATCH = false;
            if (MATCH) { for (int unutarnji_položaj = 0; unutarnji_položaj < 값길이[Loop_INDEX]; unutarnji_položaj++) 넣기(varijabla_podaci[Loop_INDEX * 256 + unutarnji_položaj]); return; }
        }
    }
    static boolean Word_VALUE(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = Pokreni[중첩깊이 * 128 + 낱말번호], završiti_razgovor_položaj = 끝[중첩깊이 * 128 + 낱말번호], BASE_položaj = 중첩깊이 * 4096, Citat = 0;
        if (읽는자리 < završiti_razgovor_položaj && IZVOR[BASE_položaj + 읽는자리] == '~' && (읽는자리 + 1 == završiti_razgovor_položaj || IZVOR[BASE_položaj + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < završiti_razgovor_položaj) {
            int kodna_točka = IZVOR[BASE_položaj + 읽는자리++];
            if (kodna_točka == Citat) { Citat = 0; continue; }
            if (Citat == 0 && (kodna_točka == 39 || kodna_točka == 34)) { Citat = kodna_točka; continue; }
            if (kodna_točka == '\\' && Citat != 39) { int Dalje_položaj = IZVOR[BASE_položaj + 읽는자리++]; if (Citat == 34 && Dalje_položaj != '$' && Dalje_položaj != '"' && Dalje_položaj != '\\') 넣기('\\'); 넣기(Dalje_položaj); continue; }
            if (kodna_točka == '$' && Citat != 39 && 읽는자리 < završiti_razgovor_položaj) {
                boolean 중괄호자리 = IZVOR[BASE_položaj + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < završiti_razgovor_položaj && IZVOR[BASE_položaj + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < završiti_razgovor_položaj && 이름뒤(IZVOR[BASE_položaj + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == završiti_razgovor_položaj || IZVOR[BASE_položaj + 읽는자리] != '}')) { GREŠKA("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                varijabla_VALUE(IZVOR, BASE_položaj + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(kodna_točka);
        }
        return !nastavak_pogreška;
    }
    static int okruženje_Postavke(int argument_INDEX, boolean ukloniti) {
        int lokalno_START = 명령해석기.시작점[argument_INDEX], završiti_razgovor_položaj = lokalno_START + 명령해석기.길이[argument_INDEX], 같음자리 = lokalno_START;
        while (같음자리 < završiti_razgovor_položaj && 명령해석기.token_VALUE[같음자리] != '=') 같음자리++;
        int unos_COUNT = 같음자리 - lokalno_START;
        if (unos_COUNT < 1 || unos_COUNT > 31 || !naziv_znak(명령해석기.token_VALUE[lokalno_START]) || !ukloniti && 같음자리 == završiti_razgovor_položaj || završiti_razgovor_položaj - 같음자리 - 1 > 255) return 2;
        for (int Loop_INDEX = lokalno_START; Loop_INDEX < 같음자리; Loop_INDEX++) if (!이름뒤(명령해석기.token_VALUE[Loop_INDEX])) return 2;
        if (raspon_SMS(명령해석기.token_VALUE, lokalno_START, unos_COUNT, "PWD") || raspon_SMS(명령해석기.token_VALUE, lokalno_START, unos_COUNT, "HOME")) return 2;
        int 찾은여부 = -1, 빈여부 = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] == 0) 빈여부 = Loop_INDEX;
            if (이름길이[Loop_INDEX] != unos_COUNT) continue;
            boolean MATCH = true; for (int unutarnji_položaj = 0; unutarnji_položaj < unos_COUNT; unutarnji_položaj++) if (varijabla_naziv[Loop_INDEX * 32 + unutarnji_položaj] != 명령해석기.token_VALUE[lokalno_START + unutarnji_položaj]) MATCH = false;
            if (MATCH) 찾은여부 = Loop_INDEX;
        }
        if (ukloniti) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = 빈여부; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = unos_COUNT; 값길이[찾은여부] = završiti_razgovor_položaj - 같음자리 - 1;
        for (int Loop_INDEX = 0; Loop_INDEX < unos_COUNT; Loop_INDEX++) varijabla_naziv[찾은여부 * 32 + Loop_INDEX] = 명령해석기.token_VALUE[lokalno_START + Loop_INDEX];
        for (int Loop_INDEX = 같음자리 + 1; Loop_INDEX < završiti_razgovor_položaj; Loop_INDEX++) varijabla_podaci[찾은여부 * 256 + Loop_INDEX - 같음자리 - 1] = 명령해석기.token_VALUE[Loop_INDEX];
        return 0;
    }
    static void emisija_okruženje() {
        단말.Zapisuj("HOME=/\nPWD="); Memorija_Datoteke.redovno_zapisivanje(); 단말.문자(10);
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] > 0) {
            for (int unutarnji_položaj = 0; unutarnji_položaj < 이름길이[Loop_INDEX]; unutarnji_položaj++) pano.직렬쓰기(varijabla_naziv[Loop_INDEX * 32 + unutarnji_položaj]); 단말.문자('=');
            for (int unutarnji_položaj = 0; unutarnji_položaj < 값길이[Loop_INDEX]; unutarnji_položaj++) pano.직렬쓰기(varijabla_podaci[Loop_INDEX * 256 + unutarnji_položaj]); 단말.문자(10);
        }
    }
    static void Izvrši_naredba(int[] podaci_ARRAY, int 시작변위, int unos_COUNT, int 중첩깊이) {
        if (중첩깊이 >= 4 || unos_COUNT > 4096) { GREŠKA("Naredba 파일의 ugnježđivanje_VALUE 또는 red 길이 제한을 넘었습니다"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < unos_COUNT; Loop_INDEX++) IZVOR[중첩깊이 * 4096 + Loop_INDEX] = podaci_ARRAY[시작변위 + Loop_INDEX];
        int ukupni_zbroj_COUNT = Čitaj(unos_COUNT, 중첩깊이); if (ukupni_zbroj_COUNT < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < ukupni_zbroj_COUNT) {
            int Grupa_završiti_razgovor = 읽는자리;
            while (Grupa_završiti_razgovor < ukupni_zbroj_COUNT && (종류[중첩깊이 * 128 + Grupa_završiti_razgovor] == 0 || 종류[중첩깊이 * 128 + Grupa_završiti_razgovor] >= 4)) Grupa_završiti_razgovor++;
            boolean Izvrši_cc685ae5 = 조건성립 == 1 || 조건성립 == 2 && Stanje_VALUE == 0 || 조건성립 == 3 && Stanje_VALUE != 0;
            if (Izvrši_cc685ae5) {
                boolean 이전자리 = false;
                while (읽는자리 < Grupa_završiti_razgovor) {
                    int Dalje_položaj = 읽는자리; while (Dalje_položaj < Grupa_završiti_razgovor && 종류[중첩깊이 * 128 + Dalje_položaj] != 4) Dalje_položaj++;
                    boolean CONNECT_tok = Dalje_položaj < Grupa_završiti_razgovor; int 입력쪽 = -1, 출력쪽 = -1, 출력방식 = 0;
                    명령해석기.token_COUNT = 0; 쓴수 = 0; nastavak_pogreška = false;
                    for (int Loop_INDEX = 읽는자리; Loop_INDEX < Dalje_položaj; Loop_INDEX++) {
                        int 자료종류 = 종류[중첩깊이 * 128 + Loop_INDEX];
                        if (자료종류 >= 5) { if (자료종류 == 7) { if (입력쪽 >= 0) { GREŠKA("입력 전환이 겹쳤습니다"); return; } 입력쪽 = ++Loop_INDEX; } else { if (출력쪽 >= 0) { GREŠKA("Izlaz 전환이 겹쳤습니다"); return; } 출력쪽 = ++Loop_INDEX; 출력방식 = 자료종류; } continue; }
                        if (명령해석기.token_COUNT == 32) { GREŠKA("인수가 너무 많습니다"); return; }
                        int argument_INDEX = 명령해석기.token_COUNT++; 명령해석기.시작점[argument_INDEX] = 쓴수;
                        if (!Word_VALUE(Loop_INDEX, 중첩깊이)) return;
                        명령해석기.길이[argument_INDEX] = 쓴수 - 명령해석기.시작점[argument_INDEX];
                    }
                    연결중 = 이전자리 || CONNECT_tok || 입력쪽 >= 0 || 출력쪽 >= 0;
                    if (연결중 && (명령해석기.같음(0, "vi") || 명령해석기.같음(0, "edit") || 명령해석기.같음(0, "load") || 명령해석기.같음(0, "gui") || 명령해석기.같음(0, "terminal") || 명령해석기.같음(0, "sh") || 명령해석기.같음(0, "source"))) { GREŠKA("대화형 명령과 Naredba 파일은 U_I 전환이나 tok_VALUE 연결에 쓸 수 없습니다"); return; }
                    셸입출력.Pokreni(이전자리, CONNECT_tok);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int unos_položaj = 입출력바꿈 == 0 ? 입력쪽 : 출력쪽; if (unos_položaj < 0) continue;
                        int START_položaj = 쓴수; if (!Word_VALUE(unos_položaj, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = Memorija_Datoteke.put_START(쓴수 - START_položaj);
                        for (int unutarnji_položaj = START_položaj; 처리값 >= 0 && unutarnji_položaj < 쓴수; unutarnji_položaj++) 처리값 = Memorija_Datoteke.put_bajt(unutarnji_položaj - START_položaj, 명령해석기.token_VALUE[unutarnji_položaj]);
                        if (처리값 >= 0) 처리값 = Memorija_Datoteke.Otvori(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); 명령해석기.GREŠKA(처리값); Stanje_VALUE = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.ulazna_datoteka = 처리값; else 셸입출력.izlazna_datoteka = 처리값;
                    }
                    셸입출력.대화허용 = 중첩깊이 == 0 && 읽는자리 == 0 && Dalje_položaj == ukupni_zbroj_COUNT;
                    깊이 = 중첩깊이; 명령해석기.REZULTAT = 0; pano.입출력전환(1);
                    명령해석기.Naredba();
                    pano.Terminal(3);
                    int 반환값 = 명령해석기.REZULTAT, tok_pogreška = 셸입출력.kvar_VALUE;
                    셸입출력.끝(); 연결중 = false;
                    Stanje_VALUE = tok_pogreška < 0 ? 1 : 반환값;
                    if (tok_pogreška < 0) { 명령해석기.GREŠKA(tok_pogreška); return; }
                    if (skripta_završiti_razgovor || 반환값 == -1005) return;
                    이전자리 = true; 읽는자리 = Dalje_položaj + 1;
                }
            }
            if (Grupa_završiti_razgovor < ukupni_zbroj_COUNT) 조건성립 = 종류[중첩깊이 * 128 + Grupa_završiti_razgovor];
            읽는자리 = Grupa_završiti_razgovor + 1;
        }
    }
    static void Izvrši_Datoteka() {
        if (명령해석기.token_COUNT != 2 || 깊이 >= 3) { 명령해석기.REZULTAT = 2; 단말.Zapisuj("사용법: sh Datoteka (ugnježđivanje_VALUE 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = 명령해석기.PUTANJA(1); if (처리값 >= 0) 처리값 = Memorija_Datoteke.Otvori(0);
        if (처리값 < 0) { 명령해석기.GREŠKA(처리값); return; }
        int unos_COUNT = 0, bajt_podaci;
        while ((bajt_podaci = Memorija_Datoteke.Čitaj(처리값)) != 256 && bajt_podaci >= 0 && unos_COUNT < 16384) skripta_VALUE[중첩깊이 * 16384 + unos_COUNT++] = bajt_podaci;
        Memorija_Datoteke.Zatvori(처리값); pano.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < unos_COUNT && !skripta_završiti_razgovor;) {
            int završiti_razgovor_položaj = 읽는자리; while (završiti_razgovor_položaj < unos_COUNT && skripta_VALUE[중첩깊이 * 16384 + završiti_razgovor_položaj] != 10) završiti_razgovor_položaj++;
            int 유효길이 = završiti_razgovor_položaj - 읽는자리; if (유효길이 > 0 && skripta_VALUE[중첩깊이 * 16384 + završiti_razgovor_položaj - 1] == 13) 유효길이--;
            Izvrši_naredba(skripta_VALUE, 중첩깊이 * 16384 + 읽는자리, 유효길이, 중첩깊이); 읽는자리 = završiti_razgovor_položaj + 1;
        }
        명령해석기.REZULTAT = Stanje_VALUE; skripta_završiti_razgovor = false; 깊이 = 중첩깊이 - 1;
    }
}
