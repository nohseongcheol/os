// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 대화형 ljuska 문법. 파이프는 순차 Izvrši_komanda, 환경은 같은 셸에서 공유한다. */
public final class ljuska_sintaksa {
    static int[] izvor = new int[4 * 4096], 종류 = new int[4 * 128], koristiti = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] promenljiva_ime = new int[16 * 32], promenljiva_podaci = new int[16 * 256], 이름길이 = new int[16], 값길이 = new int[16];
    static int[] skripta_VALUE = new int[4 * 16384];
    static int Status_VALUE, 깊이, 쓴수;
    static boolean 연결중, skripta_završiti_razgovor, ekstenzija_greška;
    static boolean ime_znak(int kôd_znaka) { return kôd_znaka >= 'a' && kôd_znaka <= 'z' || kôd_znaka >= 'A' && kôd_znaka <= 'Z' || kôd_znaka == '_' || kôd_znaka >= 128; }
    static boolean 이름뒤(int kôd_znaka) { return ime_znak(kôd_znaka) || kôd_znaka >= '0' && kôd_znaka <= '9'; }
    static void greška(String SMS) { Tabla.입출력전환(0); 단말.쓰기("komanda raščlaniti_VALUE: "); 단말.쓰기(SMS); 단말.문자(10); Status_VALUE = 2; }
    static int 읽기(int stavka_COUNT_8f7753a1, int 중첩깊이) {
        int aktuelno_INDEX = 0, ukupan_COUNT = 0, BASE_pozicija = 중첩깊이 * 4096, specijalni_znak = 중첩깊이 * 128;
        while (aktuelno_INDEX < stavka_COUNT_8f7753a1) {
            while (aktuelno_INDEX < stavka_COUNT_8f7753a1 && (izvor[BASE_pozicija + aktuelno_INDEX] == 32 || izvor[BASE_pozicija + aktuelno_INDEX] == 9)) aktuelno_INDEX++;
            if (aktuelno_INDEX == stavka_COUNT_8f7753a1 || izvor[BASE_pozicija + aktuelno_INDEX] == '#') break;
            if (ukupan_COUNT == 128) { greška("낱말이 너무 많습니다"); return -1; }
            int START_pozicija = aktuelno_INDEX, kôd_znaka = izvor[BASE_pozicija + aktuelno_INDEX], 자료종류 = 0;
            if (kôd_znaka == ';') { 자료종류 = 1; aktuelno_INDEX++; }
            else if (kôd_znaka == '&') { if (aktuelno_INDEX + 1 >= stavka_COUNT_8f7753a1 || izvor[BASE_pozicija + aktuelno_INDEX + 1] != '&') { greška("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } 자료종류 = 2; aktuelno_INDEX += 2; }
            else if (kôd_znaka == '|') { aktuelno_INDEX++; 자료종류 = aktuelno_INDEX < stavka_COUNT_8f7753a1 && izvor[BASE_pozicija + aktuelno_INDEX] == '|' ? 3 : 4; if (자료종류 == 3) aktuelno_INDEX++; }
            else if (kôd_znaka == '>') { aktuelno_INDEX++; 자료종류 = aktuelno_INDEX < stavka_COUNT_8f7753a1 && izvor[BASE_pozicija + aktuelno_INDEX] == '>' ? 6 : 5; if (자료종류 == 6) aktuelno_INDEX++; }
            else if (kôd_znaka == '<') { 자료종류 = 7; aktuelno_INDEX++; }
            else {
                int Citat = 0;
                while (aktuelno_INDEX < stavka_COUNT_8f7753a1) {
                    kôd_znaka = izvor[BASE_pozicija + aktuelno_INDEX];
                    if (kôd_znaka == '`' && Citat != 39 || kôd_znaka == '$' && Citat != 39 && aktuelno_INDEX + 1 < stavka_COUNT_8f7753a1 && izvor[BASE_pozicija + aktuelno_INDEX + 1] == '(') { greška("komanda KR 치환은 지원하지 않습니다"); return -1; }
                    if (kôd_znaka == '\\' && Citat != 39) { if (++aktuelno_INDEX == stavka_COUNT_8f7753a1) { greška("red 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } aktuelno_INDEX++; continue; }
                    if (kôd_znaka == Citat) { Citat = 0; aktuelno_INDEX++; continue; }
                    if (Citat == 0 && (kôd_znaka == 39 || kôd_znaka == 34)) { Citat = kôd_znaka; aktuelno_INDEX++; continue; }
                    if (Citat == 0 && (kôd_znaka == 32 || kôd_znaka == 9 || kôd_znaka == ';' || kôd_znaka == '&' || kôd_znaka == '|' || kôd_znaka == '<' || kôd_znaka == '>')) break;
                    aktuelno_INDEX++;
                }
                if (Citat != 0) { greška("따옴표가 닫히지 않았습니다"); return -1; }
                if (aktuelno_INDEX < stavka_COUNT_8f7753a1 && (izvor[BASE_pozicija + aktuelno_INDEX] == '>' || izvor[BASE_pozicija + aktuelno_INDEX] == '<')) {
                    boolean 수치 = aktuelno_INDEX > START_pozicija;
                    for (int Loop_INDEX = START_pozicija; Loop_INDEX < aktuelno_INDEX; Loop_INDEX++) if (izvor[BASE_pozicija + Loop_INDEX] < '0' || izvor[BASE_pozicija + Loop_INDEX] > '9') 수치 = false;
                    if (수치) { greška("번호를 지정한 Datoteka 서술자 U_I 전환은 지원하지 않습니다"); return -1; }
                }
            }
            종류[specijalni_znak + ukupan_COUNT] = 자료종류; koristiti[specijalni_znak + ukupan_COUNT] = START_pozicija; 끝[specijalni_znak + ukupan_COUNT] = aktuelno_INDEX; ukupan_COUNT++;
        }
        boolean 낱말 = false;
        for (int Loop_INDEX = 0; Loop_INDEX < ukupan_COUNT; Loop_INDEX++) {
            int 임시값 = 종류[specijalni_znak + Loop_INDEX];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++Loop_INDEX == ukupan_COUNT || 종류[specijalni_znak + Loop_INDEX] != 0) { greška("U_I 전환에 Datoteka 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || Loop_INDEX == ukupan_COUNT - 1 && 임시값 != 1) { greška("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (ukupan_COUNT > 0 && !낱말 && 종류[specijalni_znak + ukupan_COUNT - 1] != 1) { greška("명령이 빠졌습니다"); return -1; }
        return ukupan_COUNT;
    }
    static boolean opseg_SMS(int[] podaci_niz, int lokalni_START, int stavka_COUNT_8f7753a1, String znak_pozicija) {
        if (stavka_COUNT_8f7753a1 != znak_pozicija.length()) return false; for (int Loop_INDEX = 0; Loop_INDEX < stavka_COUNT_8f7753a1; Loop_INDEX++) if (podaci_niz[lokalni_START + Loop_INDEX] != znak_pozicija.charAt(Loop_INDEX)) return false; return true;
    }
    static void 넣기(int bajt_podaci) {
        if (쓴수 >= 명령해석기.token_VALUE.length) { if (!ekstenzija_greška) greška("변수를 펼친 명령이 너무 깁니다"); ekstenzija_greška = true; return; }
        명령해석기.token_VALUE[쓴수++] = bajt_podaci;
    }
    static void promenljiva_VALUE(int[] podaci_niz, int START_pozicija, int stavka_COUNT_8f7753a1) {
        if (opseg_SMS(podaci_niz, START_pozicija, stavka_COUNT_8f7753a1, "PWD")) { 넣기('/'); for (int Loop_INDEX = 0; Loop_INDEX < Memorija_Datoteke.현재길이; Loop_INDEX++) 넣기(Memorija_Datoteke.aktuelno_stavka[Loop_INDEX]); return; }
        if (opseg_SMS(podaci_niz, START_pozicija, stavka_COUNT_8f7753a1, "HOME")) { 넣기('/'); return; }
        if (opseg_SMS(podaci_niz, START_pozicija, stavka_COUNT_8f7753a1, "?")) {
            int podaci_VALUE = Status_VALUE, cifra = 100; boolean 시작여부 = false;
            while (cifra > 0) { int 뒷값 = podaci_VALUE / cifra; if (뒷값 != 0 || 시작여부 || cifra == 1) { 넣기('0' + 뒷값); 시작여부 = true; } podaci_VALUE %= cifra; cifra /= 10; } return;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] == stavka_COUNT_8f7753a1) {
            boolean MATCH = true; for (int unutrašnje_pozicija = 0; unutrašnje_pozicija < stavka_COUNT_8f7753a1; unutrašnje_pozicija++) if (promenljiva_ime[Loop_INDEX * 32 + unutrašnje_pozicija] != podaci_niz[START_pozicija + unutrašnje_pozicija]) MATCH = false;
            if (MATCH) { for (int unutrašnje_pozicija = 0; unutrašnje_pozicija < 값길이[Loop_INDEX]; unutrašnje_pozicija++) 넣기(promenljiva_podaci[Loop_INDEX * 256 + unutrašnje_pozicija]); return; }
        }
    }
    static boolean Word_VALUE(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = koristiti[중첩깊이 * 128 + 낱말번호], završiti_razgovor_pozicija = 끝[중첩깊이 * 128 + 낱말번호], BASE_pozicija = 중첩깊이 * 4096, Citat = 0;
        if (읽는자리 < završiti_razgovor_pozicija && izvor[BASE_pozicija + 읽는자리] == '~' && (읽는자리 + 1 == završiti_razgovor_pozicija || izvor[BASE_pozicija + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < završiti_razgovor_pozicija) {
            int kôd_znaka = izvor[BASE_pozicija + 읽는자리++];
            if (kôd_znaka == Citat) { Citat = 0; continue; }
            if (Citat == 0 && (kôd_znaka == 39 || kôd_znaka == 34)) { Citat = kôd_znaka; continue; }
            if (kôd_znaka == '\\' && Citat != 39) { int Dalje_pozicija = izvor[BASE_pozicija + 읽는자리++]; if (Citat == 34 && Dalje_pozicija != '$' && Dalje_pozicija != '"' && Dalje_pozicija != '\\') 넣기('\\'); 넣기(Dalje_pozicija); continue; }
            if (kôd_znaka == '$' && Citat != 39 && 읽는자리 < završiti_razgovor_pozicija) {
                boolean 중괄호자리 = izvor[BASE_pozicija + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < završiti_razgovor_pozicija && izvor[BASE_pozicija + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < završiti_razgovor_pozicija && 이름뒤(izvor[BASE_pozicija + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == završiti_razgovor_pozicija || izvor[BASE_pozicija + 읽는자리] != '}')) { greška("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                promenljiva_VALUE(izvor, BASE_pozicija + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(kôd_znaka);
        }
        return !ekstenzija_greška;
    }
    static int 환경설정(int argument_INDEX, boolean ukloniti) {
        int lokalni_START = 명령해석기.시작점[argument_INDEX], završiti_razgovor_pozicija = lokalni_START + 명령해석기.길이[argument_INDEX], 같음자리 = lokalni_START;
        while (같음자리 < završiti_razgovor_pozicija && 명령해석기.token_VALUE[같음자리] != '=') 같음자리++;
        int stavka_COUNT_8f7753a1 = 같음자리 - lokalni_START;
        if (stavka_COUNT_8f7753a1 < 1 || stavka_COUNT_8f7753a1 > 31 || !ime_znak(명령해석기.token_VALUE[lokalni_START]) || !ukloniti && 같음자리 == završiti_razgovor_pozicija || završiti_razgovor_pozicija - 같음자리 - 1 > 255) return 2;
        for (int Loop_INDEX = lokalni_START; Loop_INDEX < 같음자리; Loop_INDEX++) if (!이름뒤(명령해석기.token_VALUE[Loop_INDEX])) return 2;
        if (opseg_SMS(명령해석기.token_VALUE, lokalni_START, stavka_COUNT_8f7753a1, "PWD") || opseg_SMS(명령해석기.token_VALUE, lokalni_START, stavka_COUNT_8f7753a1, "HOME")) return 2;
        int 찾은여부 = -1, 빈여부 = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] == 0) 빈여부 = Loop_INDEX;
            if (이름길이[Loop_INDEX] != stavka_COUNT_8f7753a1) continue;
            boolean MATCH = true; for (int unutrašnje_pozicija = 0; unutrašnje_pozicija < stavka_COUNT_8f7753a1; unutrašnje_pozicija++) if (promenljiva_ime[Loop_INDEX * 32 + unutrašnje_pozicija] != 명령해석기.token_VALUE[lokalni_START + unutrašnje_pozicija]) MATCH = false;
            if (MATCH) 찾은여부 = Loop_INDEX;
        }
        if (ukloniti) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = 빈여부; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = stavka_COUNT_8f7753a1; 값길이[찾은여부] = završiti_razgovor_pozicija - 같음자리 - 1;
        for (int Loop_INDEX = 0; Loop_INDEX < stavka_COUNT_8f7753a1; Loop_INDEX++) promenljiva_ime[찾은여부 * 32 + Loop_INDEX] = 명령해석기.token_VALUE[lokalni_START + Loop_INDEX];
        for (int Loop_INDEX = 같음자리 + 1; Loop_INDEX < završiti_razgovor_pozicija; Loop_INDEX++) promenljiva_podaci[찾은여부 * 256 + Loop_INDEX - 같음자리 - 1] = 명령해석기.token_VALUE[Loop_INDEX];
        return 0;
    }
    static void 환경보기() {
        단말.쓰기("HOME=/\nPWD="); Memorija_Datoteke.현재쓰기(); 단말.문자(10);
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] > 0) {
            for (int unutrašnje_pozicija = 0; unutrašnje_pozicija < 이름길이[Loop_INDEX]; unutrašnje_pozicija++) Tabla.직렬쓰기(promenljiva_ime[Loop_INDEX * 32 + unutrašnje_pozicija]); 단말.문자('=');
            for (int unutrašnje_pozicija = 0; unutrašnje_pozicija < 값길이[Loop_INDEX]; unutrašnje_pozicija++) Tabla.직렬쓰기(promenljiva_podaci[Loop_INDEX * 256 + unutrašnje_pozicija]); 단말.문자(10);
        }
    }
    static void Izvrši_komanda(int[] podaci_niz, int 시작변위, int stavka_COUNT_8f7753a1, int 중첩깊이) {
        if (중첩깊이 >= 4 || stavka_COUNT_8f7753a1 > 4096) { greška("komanda 파일의 ugnežđivanje_VALUE 또는 red 길이 제한을 넘었습니다"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < stavka_COUNT_8f7753a1; Loop_INDEX++) izvor[중첩깊이 * 4096 + Loop_INDEX] = podaci_niz[시작변위 + Loop_INDEX];
        int ukupan_COUNT = 읽기(stavka_COUNT_8f7753a1, 중첩깊이); if (ukupan_COUNT < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < ukupan_COUNT) {
            int Grupa_završiti_razgovor = 읽는자리;
            while (Grupa_završiti_razgovor < ukupan_COUNT && (종류[중첩깊이 * 128 + Grupa_završiti_razgovor] == 0 || 종류[중첩깊이 * 128 + Grupa_završiti_razgovor] >= 4)) Grupa_završiti_razgovor++;
            boolean Izvrši = 조건성립 == 1 || 조건성립 == 2 && Status_VALUE == 0 || 조건성립 == 3 && Status_VALUE != 0;
            if (Izvrši) {
                boolean 이전자리 = false;
                while (읽는자리 < Grupa_završiti_razgovor) {
                    int Dalje_pozicija = 읽는자리; while (Dalje_pozicija < Grupa_završiti_razgovor && 종류[중첩깊이 * 128 + Dalje_pozicija] != 4) Dalje_pozicija++;
                    boolean veze_tok = Dalje_pozicija < Grupa_završiti_razgovor; int 입력쪽 = -1, 출력쪽 = -1, 출력방식 = 0;
                    명령해석기.token_COUNT = 0; 쓴수 = 0; ekstenzija_greška = false;
                    for (int Loop_INDEX = 읽는자리; Loop_INDEX < Dalje_pozicija; Loop_INDEX++) {
                        int 자료종류 = 종류[중첩깊이 * 128 + Loop_INDEX];
                        if (자료종류 >= 5) { if (자료종류 == 7) { if (입력쪽 >= 0) { greška("입력 전환이 겹쳤습니다"); return; } 입력쪽 = ++Loop_INDEX; } else { if (출력쪽 >= 0) { greška("출력 전환이 겹쳤습니다"); return; } 출력쪽 = ++Loop_INDEX; 출력방식 = 자료종류; } continue; }
                        if (명령해석기.token_COUNT == 32) { greška("인수가 너무 많습니다"); return; }
                        int argument_INDEX = 명령해석기.token_COUNT++; 명령해석기.시작점[argument_INDEX] = 쓴수;
                        if (!Word_VALUE(Loop_INDEX, 중첩깊이)) return;
                        명령해석기.길이[argument_INDEX] = 쓴수 - 명령해석기.시작점[argument_INDEX];
                    }
                    연결중 = 이전자리 || veze_tok || 입력쪽 >= 0 || 출력쪽 >= 0;
                    if (연결중 && (명령해석기.같음(0, "vi") || 명령해석기.같음(0, "edit") || 명령해석기.같음(0, "load") || 명령해석기.같음(0, "gui") || 명령해석기.같음(0, "terminal") || 명령해석기.같음(0, "sh") || 명령해석기.같음(0, "source"))) { greška("대화형 명령과 komanda 파일은 U_I 전환이나 tok_VALUE 연결에 쓸 수 없습니다"); return; }
                    셸입출력.koristiti(이전자리, veze_tok);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int stavka_pozicija = 입출력바꿈 == 0 ? 입력쪽 : 출력쪽; if (stavka_pozicija < 0) continue;
                        int START_pozicija = 쓴수; if (!Word_VALUE(stavka_pozicija, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = Memorija_Datoteke.putanja_START(쓴수 - START_pozicija);
                        for (int unutrašnje_pozicija = START_pozicija; 처리값 >= 0 && unutrašnje_pozicija < 쓴수; unutrašnje_pozicija++) 처리값 = Memorija_Datoteke.putanja_bajt(unutrašnje_pozicija - START_pozicija, 명령해석기.token_VALUE[unutrašnje_pozicija]);
                        if (처리값 >= 0) 처리값 = Memorija_Datoteke.otvoren(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); 명령해석기.greška(처리값); Status_VALUE = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.ulazna_datoteka = 처리값; else 셸입출력.izlazna_datoteka = 처리값;
                    }
                    셸입출력.대화허용 = 중첩깊이 == 0 && 읽는자리 == 0 && Dalje_pozicija == ukupan_COUNT;
                    깊이 = 중첩깊이; 명령해석기.KR = 0; Tabla.입출력전환(1);
                    명령해석기.komanda();
                    Tabla.Terminal(3);
                    int 반환값 = 명령해석기.KR, tok_greška = 셸입출력.otkazivanje_VALUE;
                    셸입출력.끝(); 연결중 = false;
                    Status_VALUE = tok_greška < 0 ? 1 : 반환값;
                    if (tok_greška < 0) { 명령해석기.greška(tok_greška); return; }
                    if (skripta_završiti_razgovor || 반환값 == -1005) return;
                    이전자리 = true; 읽는자리 = Dalje_pozicija + 1;
                }
            }
            if (Grupa_završiti_razgovor < ukupan_COUNT) 조건성립 = 종류[중첩깊이 * 128 + Grupa_završiti_razgovor];
            읽는자리 = Grupa_završiti_razgovor + 1;
        }
    }
    static void Izvrši_Datoteka() {
        if (명령해석기.token_COUNT != 2 || 깊이 >= 3) { 명령해석기.KR = 2; 단말.쓰기("사용법: sh Datoteka (ugnežđivanje_VALUE 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = 명령해석기.putanja(1); if (처리값 >= 0) 처리값 = Memorija_Datoteke.otvoren(0);
        if (처리값 < 0) { 명령해석기.greška(처리값); return; }
        int stavka_COUNT_8f7753a1 = 0, bajt_podaci;
        while ((bajt_podaci = Memorija_Datoteke.읽기(처리값)) != 256 && bajt_podaci >= 0 && stavka_COUNT_8f7753a1 < 16384) skripta_VALUE[중첩깊이 * 16384 + stavka_COUNT_8f7753a1++] = bajt_podaci;
        Memorija_Datoteke.Zatvori(처리값); Tabla.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < stavka_COUNT_8f7753a1 && !skripta_završiti_razgovor;) {
            int završiti_razgovor_pozicija = 읽는자리; while (završiti_razgovor_pozicija < stavka_COUNT_8f7753a1 && skripta_VALUE[중첩깊이 * 16384 + završiti_razgovor_pozicija] != 10) završiti_razgovor_pozicija++;
            int 유효길이 = završiti_razgovor_pozicija - 읽는자리; if (유효길이 > 0 && skripta_VALUE[중첩깊이 * 16384 + završiti_razgovor_pozicija - 1] == 13) 유효길이--;
            Izvrši_komanda(skripta_VALUE, 중첩깊이 * 16384 + 읽는자리, 유효길이, 중첩깊이); 읽는자리 = završiti_razgovor_pozicija + 1;
        }
        명령해석기.KR = Status_VALUE; skripta_završiti_razgovor = false; 깊이 = 중첩깊이 - 1;
    }
}
