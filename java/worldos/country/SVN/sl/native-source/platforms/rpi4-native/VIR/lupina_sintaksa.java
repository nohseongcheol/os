// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 interaktiven lupina 문법. 파이프는 순차 Izvedi_ukaz, 환경은 같은 셸에서 공유한다. */
public final class lupina_sintaksa {
    static int[] VIR = new int[4 * 4096], 종류 = new int[4 * 128], Zaženi = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] 변수이름 = new int[16 * 32], 변수값 = new int[16 * 256], 이름길이 = new int[16], 값길이 = new int[16];
    static int[] skript_VALUE = new int[4 * 16384];
    static int stanje_VALUE, 깊이, 쓴수;
    static boolean 연결중, skript_končati_klic, 확장오류;
    static boolean ime_znak(int koda_znaka) { return koda_znaka >= 'a' && koda_znaka <= 'z' || koda_znaka >= 'A' && koda_znaka <= 'Z' || koda_znaka == '_' || koda_znaka >= 128; }
    static boolean 이름뒤(int koda_znaka) { return ime_znak(koda_znaka) || koda_znaka >= '0' && koda_znaka <= '9'; }
    static void NAPAKA(String Besedilo) { Tabla.입출력전환(0); 단말.Pisanje("Ukaz razčlenjevati_VALUE: "); 단말.Pisanje(Besedilo); 단말.문자(10); stanje_VALUE = 2; }
    static int Branje(int vnos_COUNT, int 중첩깊이) {
        int sprotno_INDEX = 0, skupaj_COUNT = 0, BASE_položaj = 중첩깊이 * 4096, poseben_znak = 중첩깊이 * 128;
        while (sprotno_INDEX < vnos_COUNT) {
            while (sprotno_INDEX < vnos_COUNT && (VIR[BASE_položaj + sprotno_INDEX] == 32 || VIR[BASE_položaj + sprotno_INDEX] == 9)) sprotno_INDEX++;
            if (sprotno_INDEX == vnos_COUNT || VIR[BASE_položaj + sprotno_INDEX] == '#') break;
            if (skupaj_COUNT == 128) { NAPAKA("낱말이 너무 많습니다"); return -1; }
            int Start_položaj = sprotno_INDEX, koda_znaka = VIR[BASE_položaj + sprotno_INDEX], 자료종류 = 0;
            if (koda_znaka == ';') { 자료종류 = 1; sprotno_INDEX++; }
            else if (koda_znaka == '&') { if (sprotno_INDEX + 1 >= vnos_COUNT || VIR[BASE_položaj + sprotno_INDEX + 1] != '&') { NAPAKA("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } 자료종류 = 2; sprotno_INDEX += 2; }
            else if (koda_znaka == '|') { sprotno_INDEX++; 자료종류 = sprotno_INDEX < vnos_COUNT && VIR[BASE_položaj + sprotno_INDEX] == '|' ? 3 : 4; if (자료종류 == 3) sprotno_INDEX++; }
            else if (koda_znaka == '>') { sprotno_INDEX++; 자료종류 = sprotno_INDEX < vnos_COUNT && VIR[BASE_položaj + sprotno_INDEX] == '>' ? 6 : 5; if (자료종류 == 6) sprotno_INDEX++; }
            else if (koda_znaka == '<') { 자료종류 = 7; sprotno_INDEX++; }
            else {
                int Navedek = 0;
                while (sprotno_INDEX < vnos_COUNT) {
                    koda_znaka = VIR[BASE_položaj + sprotno_INDEX];
                    if (koda_znaka == '`' && Navedek != 39 || koda_znaka == '$' && Navedek != 39 && sprotno_INDEX + 1 < vnos_COUNT && VIR[BASE_položaj + sprotno_INDEX + 1] == '(') { NAPAKA("Ukaz REZULTAT 치환은 지원하지 않습니다"); return -1; }
                    if (koda_znaka == '\\' && Navedek != 39) { if (++sprotno_INDEX == vnos_COUNT) { NAPAKA("Črtni 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } sprotno_INDEX++; continue; }
                    if (koda_znaka == Navedek) { Navedek = 0; sprotno_INDEX++; continue; }
                    if (Navedek == 0 && (koda_znaka == 39 || koda_znaka == 34)) { Navedek = koda_znaka; sprotno_INDEX++; continue; }
                    if (Navedek == 0 && (koda_znaka == 32 || koda_znaka == 9 || koda_znaka == ';' || koda_znaka == '&' || koda_znaka == '|' || koda_znaka == '<' || koda_znaka == '>')) break;
                    sprotno_INDEX++;
                }
                if (Navedek != 0) { NAPAKA("따옴표가 닫히지 않았습니다"); return -1; }
                if (sprotno_INDEX < vnos_COUNT && (VIR[BASE_položaj + sprotno_INDEX] == '>' || VIR[BASE_položaj + sprotno_INDEX] == '<')) {
                    boolean 수치 = sprotno_INDEX > Start_položaj;
                    for (int Loop_INDEX = Start_položaj; Loop_INDEX < sprotno_INDEX; Loop_INDEX++) if (VIR[BASE_položaj + Loop_INDEX] < '0' || VIR[BASE_položaj + Loop_INDEX] > '9') 수치 = false;
                    if (수치) { NAPAKA("번호를 지정한 Datoteka 서술자 V_I 전환은 지원하지 않습니다"); return -1; }
                }
            }
            종류[poseben_znak + skupaj_COUNT] = 자료종류; Zaženi[poseben_znak + skupaj_COUNT] = Start_položaj; 끝[poseben_znak + skupaj_COUNT] = sprotno_INDEX; skupaj_COUNT++;
        }
        boolean 낱말 = false;
        for (int Loop_INDEX = 0; Loop_INDEX < skupaj_COUNT; Loop_INDEX++) {
            int 임시값 = 종류[poseben_znak + Loop_INDEX];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++Loop_INDEX == skupaj_COUNT || 종류[poseben_znak + Loop_INDEX] != 0) { NAPAKA("V_I 전환에 Datoteka 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || Loop_INDEX == skupaj_COUNT - 1 && 임시값 != 1) { NAPAKA("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (skupaj_COUNT > 0 && !낱말 && 종류[poseben_znak + skupaj_COUNT - 1] != 1) { NAPAKA("명령이 빠졌습니다"); return -1; }
        return skupaj_COUNT;
    }
    static boolean obseg_SMS(int[] podatki_ARRAY, int lokalen_krajeven_Start, int vnos_COUNT, String znak_položaj) {
        if (vnos_COUNT != znak_položaj.length()) return false; for (int Loop_INDEX = 0; Loop_INDEX < vnos_COUNT; Loop_INDEX++) if (podatki_ARRAY[lokalen_krajeven_Start + Loop_INDEX] != znak_položaj.charAt(Loop_INDEX)) return false; return true;
    }
    static void 넣기(int bajt_podatki) {
        if (쓴수 >= 명령해석기.žeton_VALUE.length) { if (!확장오류) NAPAKA("변수를 펼친 명령이 너무 깁니다"); 확장오류 = true; return; }
        명령해석기.žeton_VALUE[쓴수++] = bajt_podatki;
    }
    static void 변수(int[] podatki_ARRAY, int Start_položaj, int vnos_COUNT) {
        if (obseg_SMS(podatki_ARRAY, Start_položaj, vnos_COUNT, "PWD")) { 넣기('/'); for (int Loop_INDEX = 0; Loop_INDEX < pomnilnik_Datoteke.현재길이; Loop_INDEX++) 넣기(pomnilnik_Datoteke.sprotno_element[Loop_INDEX]); return; }
        if (obseg_SMS(podatki_ARRAY, Start_položaj, vnos_COUNT, "HOME")) { 넣기('/'); return; }
        if (obseg_SMS(podatki_ARRAY, Start_položaj, vnos_COUNT, "?")) {
            int podatki_VALUE = stanje_VALUE, številka = 100; boolean 시작여부 = false;
            while (številka > 0) { int 뒷값 = podatki_VALUE / številka; if (뒷값 != 0 || 시작여부 || številka == 1) { 넣기('0' + 뒷값); 시작여부 = true; } podatki_VALUE %= številka; številka /= 10; } return;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] == vnos_COUNT) {
            boolean MATCH = true; for (int notranje_položaj = 0; notranje_položaj < vnos_COUNT; notranje_položaj++) if (변수이름[Loop_INDEX * 32 + notranje_položaj] != podatki_ARRAY[Start_položaj + notranje_položaj]) MATCH = false;
            if (MATCH) { for (int notranje_položaj = 0; notranje_položaj < 값길이[Loop_INDEX]; notranje_položaj++) 넣기(변수값[Loop_INDEX * 256 + notranje_položaj]); return; }
        }
    }
    static boolean Word_VALUE(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = Zaženi[중첩깊이 * 128 + 낱말번호], končati_klic_položaj = 끝[중첩깊이 * 128 + 낱말번호], BASE_položaj = 중첩깊이 * 4096, Navedek = 0;
        if (읽는자리 < končati_klic_položaj && VIR[BASE_položaj + 읽는자리] == '~' && (읽는자리 + 1 == končati_klic_položaj || VIR[BASE_položaj + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < končati_klic_položaj) {
            int koda_znaka = VIR[BASE_položaj + 읽는자리++];
            if (koda_znaka == Navedek) { Navedek = 0; continue; }
            if (Navedek == 0 && (koda_znaka == 39 || koda_znaka == 34)) { Navedek = koda_znaka; continue; }
            if (koda_znaka == '\\' && Navedek != 39) { int Naprej_položaj = VIR[BASE_položaj + 읽는자리++]; if (Navedek == 34 && Naprej_položaj != '$' && Naprej_položaj != '"' && Naprej_položaj != '\\') 넣기('\\'); 넣기(Naprej_položaj); continue; }
            if (koda_znaka == '$' && Navedek != 39 && 읽는자리 < končati_klic_položaj) {
                boolean 중괄호자리 = VIR[BASE_položaj + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < končati_klic_položaj && VIR[BASE_položaj + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < končati_klic_položaj && 이름뒤(VIR[BASE_položaj + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == končati_klic_položaj || VIR[BASE_položaj + 읽는자리] != '}')) { NAPAKA("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                변수(VIR, BASE_položaj + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(koda_znaka);
        }
        return !확장오류;
    }
    static int 환경설정(int argument_INDEX, boolean odstraniti) {
        int lokalen_krajeven_Start = 명령해석기.시작점[argument_INDEX], končati_klic_položaj = lokalen_krajeven_Start + 명령해석기.길이[argument_INDEX], 같음자리 = lokalen_krajeven_Start;
        while (같음자리 < končati_klic_položaj && 명령해석기.žeton_VALUE[같음자리] != '=') 같음자리++;
        int vnos_COUNT = 같음자리 - lokalen_krajeven_Start;
        if (vnos_COUNT < 1 || vnos_COUNT > 31 || !ime_znak(명령해석기.žeton_VALUE[lokalen_krajeven_Start]) || !odstraniti && 같음자리 == končati_klic_položaj || končati_klic_položaj - 같음자리 - 1 > 255) return 2;
        for (int Loop_INDEX = lokalen_krajeven_Start; Loop_INDEX < 같음자리; Loop_INDEX++) if (!이름뒤(명령해석기.žeton_VALUE[Loop_INDEX])) return 2;
        if (obseg_SMS(명령해석기.žeton_VALUE, lokalen_krajeven_Start, vnos_COUNT, "PWD") || obseg_SMS(명령해석기.žeton_VALUE, lokalen_krajeven_Start, vnos_COUNT, "HOME")) return 2;
        int 찾은여부 = -1, informacijska_tehnologija_prazen_stanje = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] == 0) informacijska_tehnologija_prazen_stanje = Loop_INDEX;
            if (이름길이[Loop_INDEX] != vnos_COUNT) continue;
            boolean MATCH = true; for (int notranje_položaj = 0; notranje_položaj < vnos_COUNT; notranje_položaj++) if (변수이름[Loop_INDEX * 32 + notranje_položaj] != 명령해석기.žeton_VALUE[lokalen_krajeven_Start + notranje_položaj]) MATCH = false;
            if (MATCH) 찾은여부 = Loop_INDEX;
        }
        if (odstraniti) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = informacijska_tehnologija_prazen_stanje; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = vnos_COUNT; 값길이[찾은여부] = končati_klic_položaj - 같음자리 - 1;
        for (int Loop_INDEX = 0; Loop_INDEX < vnos_COUNT; Loop_INDEX++) 변수이름[찾은여부 * 32 + Loop_INDEX] = 명령해석기.žeton_VALUE[lokalen_krajeven_Start + Loop_INDEX];
        for (int Loop_INDEX = 같음자리 + 1; Loop_INDEX < končati_klic_položaj; Loop_INDEX++) 변수값[찾은여부 * 256 + Loop_INDEX - 같음자리 - 1] = 명령해석기.žeton_VALUE[Loop_INDEX];
        return 0;
    }
    static void 환경보기() {
        단말.Pisanje("HOME=/\nPWD="); pomnilnik_Datoteke.sprotno_pisati(); 단말.문자(10);
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] > 0) {
            for (int notranje_položaj = 0; notranje_položaj < 이름길이[Loop_INDEX]; notranje_položaj++) Tabla.직렬쓰기(변수이름[Loop_INDEX * 32 + notranje_položaj]); 단말.문자('=');
            for (int notranje_položaj = 0; notranje_položaj < 값길이[Loop_INDEX]; notranje_položaj++) Tabla.직렬쓰기(변수값[Loop_INDEX * 256 + notranje_položaj]); 단말.문자(10);
        }
    }
    static void Izvedi_ukaz(int[] podatki_ARRAY, int 시작변위, int vnos_COUNT, int 중첩깊이) {
        if (중첩깊이 >= 4 || vnos_COUNT > 4096) { NAPAKA("Ukaz 파일의 ugnezdenje_VALUE 또는 Črtni 길이 제한을 넘었습니다"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < vnos_COUNT; Loop_INDEX++) VIR[중첩깊이 * 4096 + Loop_INDEX] = podatki_ARRAY[시작변위 + Loop_INDEX];
        int skupaj_COUNT = Branje(vnos_COUNT, 중첩깊이); if (skupaj_COUNT < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < skupaj_COUNT) {
            int Skupina_končati_klic = 읽는자리;
            while (Skupina_končati_klic < skupaj_COUNT && (종류[중첩깊이 * 128 + Skupina_končati_klic] == 0 || 종류[중첩깊이 * 128 + Skupina_končati_klic] >= 4)) Skupina_končati_klic++;
            boolean Izvedi_cc685ae5 = 조건성립 == 1 || 조건성립 == 2 && stanje_VALUE == 0 || 조건성립 == 3 && stanje_VALUE != 0;
            if (Izvedi_cc685ae5) {
                boolean 이전자리 = false;
                while (읽는자리 < Skupina_končati_klic) {
                    int Naprej_položaj = 읽는자리; while (Naprej_položaj < Skupina_končati_klic && 종류[중첩깊이 * 128 + Naprej_položaj] != 4) Naprej_položaj++;
                    boolean POVEŽI_tok = Naprej_položaj < Skupina_končati_klic; int 입력쪽 = -1, 출력쪽 = -1, 출력방식 = 0;
                    명령해석기.žeton_COUNT = 0; 쓴수 = 0; 확장오류 = false;
                    for (int Loop_INDEX = 읽는자리; Loop_INDEX < Naprej_položaj; Loop_INDEX++) {
                        int 자료종류 = 종류[중첩깊이 * 128 + Loop_INDEX];
                        if (자료종류 >= 5) { if (자료종류 == 7) { if (입력쪽 >= 0) { NAPAKA("입력 전환이 겹쳤습니다"); return; } 입력쪽 = ++Loop_INDEX; } else { if (출력쪽 >= 0) { NAPAKA("Izpis 전환이 겹쳤습니다"); return; } 출력쪽 = ++Loop_INDEX; 출력방식 = 자료종류; } continue; }
                        if (명령해석기.žeton_COUNT == 32) { NAPAKA("인수가 너무 많습니다"); return; }
                        int argument_INDEX = 명령해석기.žeton_COUNT++; 명령해석기.시작점[argument_INDEX] = 쓴수;
                        if (!Word_VALUE(Loop_INDEX, 중첩깊이)) return;
                        명령해석기.길이[argument_INDEX] = 쓴수 - 명령해석기.시작점[argument_INDEX];
                    }
                    연결중 = 이전자리 || POVEŽI_tok || 입력쪽 >= 0 || 출력쪽 >= 0;
                    if (연결중 && (명령해석기.같음(0, "vi") || 명령해석기.같음(0, "edit") || 명령해석기.같음(0, "load") || 명령해석기.같음(0, "gui") || 명령해석기.같음(0, "terminal") || 명령해석기.같음(0, "sh") || 명령해석기.같음(0, "source"))) { NAPAKA("interaktiven 명령과 Ukaz 파일은 V_I 전환이나 tok_VALUE 연결에 쓸 수 없습니다"); return; }
                    셸입출력.Zaženi(이전자리, POVEŽI_tok);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int vnos_položaj = 입출력바꿈 == 0 ? 입력쪽 : 출력쪽; if (vnos_položaj < 0) continue;
                        int Start_položaj = 쓴수; if (!Word_VALUE(vnos_položaj, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = pomnilnik_Datoteke.pot_Start(쓴수 - Start_položaj);
                        for (int notranje_položaj = Start_položaj; 처리값 >= 0 && notranje_položaj < 쓴수; notranje_položaj++) 처리값 = pomnilnik_Datoteke.pot_bajt(notranje_položaj - Start_položaj, 명령해석기.žeton_VALUE[notranje_položaj]);
                        if (처리값 >= 0) 처리값 = pomnilnik_Datoteke.Odpri(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); 명령해석기.NAPAKA(처리값); stanje_VALUE = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.vhodna_datoteka = 처리값; else 셸입출력.izhodna_datoteka = 처리값;
                    }
                    셸입출력.Dovoli_interaktiven = 중첩깊이 == 0 && 읽는자리 == 0 && Naprej_položaj == skupaj_COUNT;
                    깊이 = 중첩깊이; 명령해석기.REZULTAT = 0; Tabla.입출력전환(1);
                    명령해석기.Ukaz();
                    Tabla.Terminal(3);
                    int 반환값 = 명령해석기.REZULTAT, 흐름오류 = 셸입출력.napaka_VALUE;
                    셸입출력.끝(); 연결중 = false;
                    stanje_VALUE = 흐름오류 < 0 ? 1 : 반환값;
                    if (흐름오류 < 0) { 명령해석기.NAPAKA(흐름오류); return; }
                    if (skript_končati_klic || 반환값 == -1005) return;
                    이전자리 = true; 읽는자리 = Naprej_položaj + 1;
                }
            }
            if (Skupina_končati_klic < skupaj_COUNT) 조건성립 = 종류[중첩깊이 * 128 + Skupina_končati_klic];
            읽는자리 = Skupina_končati_klic + 1;
        }
    }
    static void Izvedi_Datoteka() {
        if (명령해석기.žeton_COUNT != 2 || 깊이 >= 3) { 명령해석기.REZULTAT = 2; 단말.Pisanje("사용법: sh Datoteka (ugnezdenje_VALUE 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = 명령해석기.POT(1); if (처리값 >= 0) 처리값 = pomnilnik_Datoteke.Odpri(0);
        if (처리값 < 0) { 명령해석기.NAPAKA(처리값); return; }
        int vnos_COUNT = 0, bajt_podatki;
        while ((bajt_podatki = pomnilnik_Datoteke.Branje(처리값)) != 256 && bajt_podatki >= 0 && vnos_COUNT < 16384) skript_VALUE[중첩깊이 * 16384 + vnos_COUNT++] = bajt_podatki;
        pomnilnik_Datoteke.Zapri(처리값); Tabla.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < vnos_COUNT && !skript_končati_klic;) {
            int končati_klic_položaj = 읽는자리; while (končati_klic_položaj < vnos_COUNT && skript_VALUE[중첩깊이 * 16384 + končati_klic_položaj] != 10) končati_klic_položaj++;
            int 유효길이 = končati_klic_položaj - 읽는자리; if (유효길이 > 0 && skript_VALUE[중첩깊이 * 16384 + končati_klic_položaj - 1] == 13) 유효길이--;
            Izvedi_ukaz(skript_VALUE, 중첩깊이 * 16384 + 읽는자리, 유효길이, 중첩깊이); 읽는자리 = končati_klic_položaj + 1;
        }
        명령해석기.REZULTAT = stanje_VALUE; skript_končati_klic = false; 깊이 = 중첩깊이 - 1;
    }
}
