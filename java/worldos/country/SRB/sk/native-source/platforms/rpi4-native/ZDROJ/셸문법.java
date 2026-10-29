// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 interaktívny 셸 문법. 파이프는 순차 Vykonať_príkaz, 환경은 같은 셸에서 공유한다. */
public final class 셸문법 {
    static int[] ZDROJ = new int[4 * 4096], 종류 = new int[4 * 128], Spustiť_2 = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] 변수이름 = new int[16 * 32], 변수값 = new int[16 * 256], 이름길이 = new int[16], VALUE_dĺžka = new int[16];
    static int[] skript_VALUE = new int[4 * 16384];
    static int Stav_VALUE, 깊이, 쓴수;
    static boolean 연결중, skript_ukončiť_hovor, prípona_Chyba;
    static boolean názov_znak(int bod_kódu) { return bod_kódu >= 'a' && bod_kódu <= 'z' || bod_kódu >= 'A' && bod_kódu <= 'Z' || bod_kódu == '_' || bod_kódu >= 128; }
    static boolean 이름뒤(int bod_kódu) { return názov_znak(bod_kódu) || bod_kódu >= '0' && bod_kódu <= '9'; }
    static void chyba(String Spracovanie_textu) { Panel.입출력전환(0); 단말.Zápis("Príkaz analyzovať_VALUE: "); 단말.Zápis(Spracovanie_textu); 단말.문자(10); Stav_VALUE = 2; }
    static int Čítanie(int položka_COUNT_8f7753a1, int 중첩깊이) {
        int v_termíne_splatnosti_INDEX = 0, celkovo_COUNT = 0, BASE_pozícia = 중첩깊이 * 4096, špeciálny_znak = 중첩깊이 * 128;
        while (v_termíne_splatnosti_INDEX < položka_COUNT_8f7753a1) {
            while (v_termíne_splatnosti_INDEX < položka_COUNT_8f7753a1 && (ZDROJ[BASE_pozícia + v_termíne_splatnosti_INDEX] == 32 || ZDROJ[BASE_pozícia + v_termíne_splatnosti_INDEX] == 9)) v_termíne_splatnosti_INDEX++;
            if (v_termíne_splatnosti_INDEX == položka_COUNT_8f7753a1 || ZDROJ[BASE_pozícia + v_termíne_splatnosti_INDEX] == '#') break;
            if (celkovo_COUNT == 128) { chyba("낱말이 너무 많습니다"); return -1; }
            int START_pozícia = v_termíne_splatnosti_INDEX, bod_kódu = ZDROJ[BASE_pozícia + v_termíne_splatnosti_INDEX], 자료종류 = 0;
            if (bod_kódu == ';') { 자료종류 = 1; v_termíne_splatnosti_INDEX++; }
            else if (bod_kódu == '&') { if (v_termíne_splatnosti_INDEX + 1 >= položka_COUNT_8f7753a1 || ZDROJ[BASE_pozícia + v_termíne_splatnosti_INDEX + 1] != '&') { chyba("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } 자료종류 = 2; v_termíne_splatnosti_INDEX += 2; }
            else if (bod_kódu == '|') { v_termíne_splatnosti_INDEX++; 자료종류 = v_termíne_splatnosti_INDEX < položka_COUNT_8f7753a1 && ZDROJ[BASE_pozícia + v_termíne_splatnosti_INDEX] == '|' ? 3 : 4; if (자료종류 == 3) v_termíne_splatnosti_INDEX++; }
            else if (bod_kódu == '>') { v_termíne_splatnosti_INDEX++; 자료종류 = v_termíne_splatnosti_INDEX < položka_COUNT_8f7753a1 && ZDROJ[BASE_pozícia + v_termíne_splatnosti_INDEX] == '>' ? 6 : 5; if (자료종류 == 6) v_termíne_splatnosti_INDEX++; }
            else if (bod_kódu == '<') { 자료종류 = 7; v_termíne_splatnosti_INDEX++; }
            else {
                int Citát = 0;
                while (v_termíne_splatnosti_INDEX < položka_COUNT_8f7753a1) {
                    bod_kódu = ZDROJ[BASE_pozícia + v_termíne_splatnosti_INDEX];
                    if (bod_kódu == '`' && Citát != 39 || bod_kódu == '$' && Citát != 39 && v_termíne_splatnosti_INDEX + 1 < položka_COUNT_8f7753a1 && ZDROJ[BASE_pozícia + v_termíne_splatnosti_INDEX + 1] == '(') { chyba("Príkaz KR 치환은 지원하지 않습니다"); return -1; }
                    if (bod_kódu == '\\' && Citát != 39) { if (++v_termíne_splatnosti_INDEX == položka_COUNT_8f7753a1) { chyba("riadok 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } v_termíne_splatnosti_INDEX++; continue; }
                    if (bod_kódu == Citát) { Citát = 0; v_termíne_splatnosti_INDEX++; continue; }
                    if (Citát == 0 && (bod_kódu == 39 || bod_kódu == 34)) { Citát = bod_kódu; v_termíne_splatnosti_INDEX++; continue; }
                    if (Citát == 0 && (bod_kódu == 32 || bod_kódu == 9 || bod_kódu == ';' || bod_kódu == '&' || bod_kódu == '|' || bod_kódu == '<' || bod_kódu == '>')) break;
                    v_termíne_splatnosti_INDEX++;
                }
                if (Citát != 0) { chyba("따옴표가 닫히지 않았습니다"); return -1; }
                if (v_termíne_splatnosti_INDEX < položka_COUNT_8f7753a1 && (ZDROJ[BASE_pozícia + v_termíne_splatnosti_INDEX] == '>' || ZDROJ[BASE_pozícia + v_termíne_splatnosti_INDEX] == '<')) {
                    boolean 수치 = v_termíne_splatnosti_INDEX > START_pozícia;
                    for (int Loop_INDEX = START_pozícia; Loop_INDEX < v_termíne_splatnosti_INDEX; Loop_INDEX++) if (ZDROJ[BASE_pozícia + Loop_INDEX] < '0' || ZDROJ[BASE_pozícia + Loop_INDEX] > '9') 수치 = false;
                    if (수치) { chyba("번호를 지정한 Súbor 서술자 vstup_a_výstup 전환은 지원하지 않습니다"); return -1; }
                }
            }
            종류[špeciálny_znak + celkovo_COUNT] = 자료종류; Spustiť_2[špeciálny_znak + celkovo_COUNT] = START_pozícia; 끝[špeciálny_znak + celkovo_COUNT] = v_termíne_splatnosti_INDEX; celkovo_COUNT++;
        }
        boolean 낱말 = false;
        for (int Loop_INDEX = 0; Loop_INDEX < celkovo_COUNT; Loop_INDEX++) {
            int 임시값 = 종류[špeciálny_znak + Loop_INDEX];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++Loop_INDEX == celkovo_COUNT || 종류[špeciálny_znak + Loop_INDEX] != 0) { chyba("vstup_a_výstup 전환에 Súbor 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || Loop_INDEX == celkovo_COUNT - 1 && 임시값 != 1) { chyba("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (celkovo_COUNT > 0 && !낱말 && 종류[špeciálny_znak + celkovo_COUNT - 1] != 1) { chyba("명령이 빠졌습니다"); return -1; }
        return celkovo_COUNT;
    }
    static boolean rozsah_SMS(int[] údaje_pole, int miestny_START, int položka_COUNT_8f7753a1, String znak_pozícia) {
        if (položka_COUNT_8f7753a1 != znak_pozícia.length()) return false; for (int Loop_INDEX = 0; Loop_INDEX < položka_COUNT_8f7753a1; Loop_INDEX++) if (údaje_pole[miestny_START + Loop_INDEX] != znak_pozícia.charAt(Loop_INDEX)) return false; return true;
    }
    static void 넣기(int Byte_údaje) {
        if (쓴수 >= 명령해석기.token_VALUE.length) { if (!prípona_Chyba) chyba("변수를 펼친 명령이 너무 깁니다"); prípona_Chyba = true; return; }
        명령해석기.token_VALUE[쓴수++] = Byte_údaje;
    }
    static void 변수(int[] údaje_pole, int START_pozícia, int položka_COUNT_8f7753a1) {
        if (rozsah_SMS(údaje_pole, START_pozícia, položka_COUNT_8f7753a1, "PWD")) { 넣기('/'); for (int Loop_INDEX = 0; Loop_INDEX < Pamäť_Súbory.v_termíne_splatnosti_dĺžka; Loop_INDEX++) 넣기(Pamäť_Súbory.v_termíne_splatnosti_položka[Loop_INDEX]); return; }
        if (rozsah_SMS(údaje_pole, START_pozícia, položka_COUNT_8f7753a1, "HOME")) { 넣기('/'); return; }
        if (rozsah_SMS(údaje_pole, START_pozícia, položka_COUNT_8f7753a1, "?")) {
            int údaje_VALUE = Stav_VALUE, číslica = 100; boolean 시작여부 = false;
            while (číslica > 0) { int 뒷값 = údaje_VALUE / číslica; if (뒷값 != 0 || 시작여부 || číslica == 1) { 넣기('0' + 뒷값); 시작여부 = true; } údaje_VALUE %= číslica; číslica /= 10; } return;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] == položka_COUNT_8f7753a1) {
            boolean MATCH = true; for (int vnútorné_pozícia = 0; vnútorné_pozícia < položka_COUNT_8f7753a1; vnútorné_pozícia++) if (변수이름[Loop_INDEX * 32 + vnútorné_pozícia] != údaje_pole[START_pozícia + vnútorné_pozícia]) MATCH = false;
            if (MATCH) { for (int vnútorné_pozícia = 0; vnútorné_pozícia < VALUE_dĺžka[Loop_INDEX]; vnútorné_pozícia++) 넣기(변수값[Loop_INDEX * 256 + vnútorné_pozícia]); return; }
        }
    }
    static boolean Word_VALUE(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = Spustiť_2[중첩깊이 * 128 + 낱말번호], ukončiť_hovor_pozícia = 끝[중첩깊이 * 128 + 낱말번호], BASE_pozícia = 중첩깊이 * 4096, Citát = 0;
        if (읽는자리 < ukončiť_hovor_pozícia && ZDROJ[BASE_pozícia + 읽는자리] == '~' && (읽는자리 + 1 == ukončiť_hovor_pozícia || ZDROJ[BASE_pozícia + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < ukončiť_hovor_pozícia) {
            int bod_kódu = ZDROJ[BASE_pozícia + 읽는자리++];
            if (bod_kódu == Citát) { Citát = 0; continue; }
            if (Citát == 0 && (bod_kódu == 39 || bod_kódu == 34)) { Citát = bod_kódu; continue; }
            if (bod_kódu == '\\' && Citát != 39) { int Ďalej_pozícia = ZDROJ[BASE_pozícia + 읽는자리++]; if (Citát == 34 && Ďalej_pozícia != '$' && Ďalej_pozícia != '"' && Ďalej_pozícia != '\\') 넣기('\\'); 넣기(Ďalej_pozícia); continue; }
            if (bod_kódu == '$' && Citát != 39 && 읽는자리 < ukončiť_hovor_pozícia) {
                boolean 중괄호자리 = ZDROJ[BASE_pozícia + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < ukončiť_hovor_pozícia && ZDROJ[BASE_pozícia + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < ukončiť_hovor_pozícia && 이름뒤(ZDROJ[BASE_pozícia + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == ukončiť_hovor_pozícia || ZDROJ[BASE_pozícia + 읽는자리] != '}')) { chyba("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                변수(ZDROJ, BASE_pozícia + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(bod_kódu);
        }
        return !prípona_Chyba;
    }
    static int 환경설정(int argument_INDEX, boolean odobrať) {
        int miestny_START = 명령해석기.시작점[argument_INDEX], ukončiť_hovor_pozícia = miestny_START + 명령해석기.dĺžka_VALUE[argument_INDEX], 같음자리 = miestny_START;
        while (같음자리 < ukončiť_hovor_pozícia && 명령해석기.token_VALUE[같음자리] != '=') 같음자리++;
        int položka_COUNT_8f7753a1 = 같음자리 - miestny_START;
        if (položka_COUNT_8f7753a1 < 1 || položka_COUNT_8f7753a1 > 31 || !názov_znak(명령해석기.token_VALUE[miestny_START]) || !odobrať && 같음자리 == ukončiť_hovor_pozícia || ukončiť_hovor_pozícia - 같음자리 - 1 > 255) return 2;
        for (int Loop_INDEX = miestny_START; Loop_INDEX < 같음자리; Loop_INDEX++) if (!이름뒤(명령해석기.token_VALUE[Loop_INDEX])) return 2;
        if (rozsah_SMS(명령해석기.token_VALUE, miestny_START, položka_COUNT_8f7753a1, "PWD") || rozsah_SMS(명령해석기.token_VALUE, miestny_START, položka_COUNT_8f7753a1, "HOME")) return 2;
        int 찾은여부 = -1, Informačné_systémy_prázdny_Stav = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] == 0) Informačné_systémy_prázdny_Stav = Loop_INDEX;
            if (이름길이[Loop_INDEX] != položka_COUNT_8f7753a1) continue;
            boolean MATCH = true; for (int vnútorné_pozícia = 0; vnútorné_pozícia < položka_COUNT_8f7753a1; vnútorné_pozícia++) if (변수이름[Loop_INDEX * 32 + vnútorné_pozícia] != 명령해석기.token_VALUE[miestny_START + vnútorné_pozícia]) MATCH = false;
            if (MATCH) 찾은여부 = Loop_INDEX;
        }
        if (odobrať) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = Informačné_systémy_prázdny_Stav; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = položka_COUNT_8f7753a1; VALUE_dĺžka[찾은여부] = ukončiť_hovor_pozícia - 같음자리 - 1;
        for (int Loop_INDEX = 0; Loop_INDEX < položka_COUNT_8f7753a1; Loop_INDEX++) 변수이름[찾은여부 * 32 + Loop_INDEX] = 명령해석기.token_VALUE[miestny_START + Loop_INDEX];
        for (int Loop_INDEX = 같음자리 + 1; Loop_INDEX < ukončiť_hovor_pozícia; Loop_INDEX++) 변수값[찾은여부 * 256 + Loop_INDEX - 같음자리 - 1] = 명령해석기.token_VALUE[Loop_INDEX];
        return 0;
    }
    static void 환경보기() {
        단말.Zápis("HOME=/\nPWD="); Pamäť_Súbory.v_termíne_splatnosti_zapísať(); 단말.문자(10);
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] > 0) {
            for (int vnútorné_pozícia = 0; vnútorné_pozícia < 이름길이[Loop_INDEX]; vnútorné_pozícia++) Panel.직렬쓰기(변수이름[Loop_INDEX * 32 + vnútorné_pozícia]); 단말.문자('=');
            for (int vnútorné_pozícia = 0; vnútorné_pozícia < VALUE_dĺžka[Loop_INDEX]; vnútorné_pozícia++) Panel.직렬쓰기(변수값[Loop_INDEX * 256 + vnútorné_pozícia]); 단말.문자(10);
        }
    }
    static void Vykonať_príkaz(int[] údaje_pole, int 시작변위, int položka_COUNT_8f7753a1, int 중첩깊이) {
        if (중첩깊이 >= 4 || položka_COUNT_8f7753a1 > 4096) { chyba("Príkaz 파일의 vnorenie_VALUE 또는 riadok dĺžka_VALUE 제한을 넘었습니다"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < položka_COUNT_8f7753a1; Loop_INDEX++) ZDROJ[중첩깊이 * 4096 + Loop_INDEX] = údaje_pole[시작변위 + Loop_INDEX];
        int celkovo_COUNT = Čítanie(položka_COUNT_8f7753a1, 중첩깊이); if (celkovo_COUNT < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < celkovo_COUNT) {
            int Skupina_ukončiť_hovor = 읽는자리;
            while (Skupina_ukončiť_hovor < celkovo_COUNT && (종류[중첩깊이 * 128 + Skupina_ukončiť_hovor] == 0 || 종류[중첩깊이 * 128 + Skupina_ukončiť_hovor] >= 4)) Skupina_ukončiť_hovor++;
            boolean Vykonať = 조건성립 == 1 || 조건성립 == 2 && Stav_VALUE == 0 || 조건성립 == 3 && Stav_VALUE != 0;
            if (Vykonať) {
                boolean 이전자리 = false;
                while (읽는자리 < Skupina_ukončiť_hovor) {
                    int Ďalej_pozícia = 읽는자리; while (Ďalej_pozícia < Skupina_ukončiť_hovor && 종류[중첩깊이 * 128 + Ďalej_pozícia] != 4) Ďalej_pozícia++;
                    boolean spojiť_Stream = Ďalej_pozícia < Skupina_ukončiť_hovor; int vstup_strana = -1, 출력쪽 = -1, 출력방식 = 0;
                    명령해석기.token_COUNT = 0; 쓴수 = 0; prípona_Chyba = false;
                    for (int Loop_INDEX = 읽는자리; Loop_INDEX < Ďalej_pozícia; Loop_INDEX++) {
                        int 자료종류 = 종류[중첩깊이 * 128 + Loop_INDEX];
                        if (자료종류 >= 5) { if (자료종류 == 7) { if (vstup_strana >= 0) { chyba("vstup_VALUE 전환이 겹쳤습니다"); return; } vstup_strana = ++Loop_INDEX; } else { if (출력쪽 >= 0) { chyba("Výstup 전환이 겹쳤습니다"); return; } 출력쪽 = ++Loop_INDEX; 출력방식 = 자료종류; } continue; }
                        if (명령해석기.token_COUNT == 32) { chyba("인수가 너무 많습니다"); return; }
                        int argument_INDEX = 명령해석기.token_COUNT++; 명령해석기.시작점[argument_INDEX] = 쓴수;
                        if (!Word_VALUE(Loop_INDEX, 중첩깊이)) return;
                        명령해석기.dĺžka_VALUE[argument_INDEX] = 쓴수 - 명령해석기.시작점[argument_INDEX];
                    }
                    연결중 = 이전자리 || spojiť_Stream || vstup_strana >= 0 || 출력쪽 >= 0;
                    if (연결중 && (명령해석기.같음(0, "vi") || 명령해석기.같음(0, "edit") || 명령해석기.같음(0, "load") || 명령해석기.같음(0, "gui") || 명령해석기.같음(0, "terminal") || 명령해석기.같음(0, "sh") || 명령해석기.같음(0, "source"))) { chyba("interaktívny 명령과 Príkaz 파일은 vstup_a_výstup 전환이나 Stream_VALUE 연결에 쓸 수 없습니다"); return; }
                    셸입출력.Spustiť_2(이전자리, spojiť_Stream);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int položka_pozícia = 입출력바꿈 == 0 ? vstup_strana : 출력쪽; if (položka_pozícia < 0) continue;
                        int START_pozícia = 쓴수; if (!Word_VALUE(položka_pozícia, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = Pamäť_Súbory.cesta_START(쓴수 - START_pozícia);
                        for (int vnútorné_pozícia = START_pozícia; 처리값 >= 0 && vnútorné_pozícia < 쓴수; vnútorné_pozícia++) 처리값 = Pamäť_Súbory.cesta_Byte(vnútorné_pozícia - START_pozícia, 명령해석기.token_VALUE[vnútorné_pozícia]);
                        if (처리값 >= 0) 처리값 = Pamäť_Súbory.Otvoriť(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); 명령해석기.chyba(처리값); Stav_VALUE = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.vstupný_súbor = 처리값; else 셸입출력.výstupný_súbor = 처리값;
                    }
                    셸입출력.Povoliť_interaktívny = 중첩깊이 == 0 && 읽는자리 == 0 && Ďalej_pozícia == celkovo_COUNT;
                    깊이 = 중첩깊이; 명령해석기.KR = 0; Panel.입출력전환(1);
                    명령해석기.Príkaz();
                    Panel.Terminál(3);
                    int 반환값 = 명령해석기.KR, Stream_Chyba = 셸입출력.zlyhanie_VALUE;
                    셸입출력.끝(); 연결중 = false;
                    Stav_VALUE = Stream_Chyba < 0 ? 1 : 반환값;
                    if (Stream_Chyba < 0) { 명령해석기.chyba(Stream_Chyba); return; }
                    if (skript_ukončiť_hovor || 반환값 == -1005) return;
                    이전자리 = true; 읽는자리 = Ďalej_pozícia + 1;
                }
            }
            if (Skupina_ukončiť_hovor < celkovo_COUNT) 조건성립 = 종류[중첩깊이 * 128 + Skupina_ukončiť_hovor];
            읽는자리 = Skupina_ukončiť_hovor + 1;
        }
    }
    static void Vykonať_Súbor() {
        if (명령해석기.token_COUNT != 2 || 깊이 >= 3) { 명령해석기.KR = 2; 단말.Zápis("사용법: sh Súbor (vnorenie_VALUE 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = 명령해석기.Cesta(1); if (처리값 >= 0) 처리값 = Pamäť_Súbory.Otvoriť(0);
        if (처리값 < 0) { 명령해석기.chyba(처리값); return; }
        int položka_COUNT_8f7753a1 = 0, Byte_údaje;
        while ((Byte_údaje = Pamäť_Súbory.Čítanie(처리값)) != 256 && Byte_údaje >= 0 && položka_COUNT_8f7753a1 < 16384) skript_VALUE[중첩깊이 * 16384 + položka_COUNT_8f7753a1++] = Byte_údaje;
        Pamäť_Súbory.Zatvoriť(처리값); Panel.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < položka_COUNT_8f7753a1 && !skript_ukončiť_hovor;) {
            int ukončiť_hovor_pozícia = 읽는자리; while (ukončiť_hovor_pozícia < položka_COUNT_8f7753a1 && skript_VALUE[중첩깊이 * 16384 + ukončiť_hovor_pozícia] != 10) ukončiť_hovor_pozícia++;
            int 유효길이 = ukončiť_hovor_pozícia - 읽는자리; if (유효길이 > 0 && skript_VALUE[중첩깊이 * 16384 + ukončiť_hovor_pozícia - 1] == 13) 유효길이--;
            Vykonať_príkaz(skript_VALUE, 중첩깊이 * 16384 + 읽는자리, 유효길이, 중첩깊이); 읽는자리 = ukončiť_hovor_pozícia + 1;
        }
        명령해석기.KR = Stav_VALUE; skript_ukončiť_hovor = false; 깊이 = 중첩깊이 - 1;
    }
}
