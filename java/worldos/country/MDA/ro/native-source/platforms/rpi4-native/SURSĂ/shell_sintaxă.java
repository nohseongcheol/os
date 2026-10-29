// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 대화형 shell 문법. 파이프는 순차 executa_comandă, 환경은 같은 셸에서 공유한다. */
public final class shell_sintaxă {
    static int[] SURSĂ = new int[4 * 4096], 종류 = new int[4 * 128], Pornește = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] variabilă_nume = new int[16 * 32], variabilă_date = new int[16 * 256], 이름길이 = new int[16], VALUE_lungime = new int[16];
    static int[] script_VALUE = new int[4 * 16384];
    static int Stare_VALUE, 깊이, 쓴수;
    static boolean 연결중, script_termina_un_apel, extensie_eroare;
    static boolean nume_caracter(int cod_caracter) { return cod_caracter >= 'a' && cod_caracter <= 'z' || cod_caracter >= 'A' && cod_caracter <= 'Z' || cod_caracter == '_' || cod_caracter >= 128; }
    static boolean 이름뒤(int cod_caracter) { return nume_caracter(cod_caracter) || cod_caracter >= '0' && cod_caracter <= '9'; }
    static void eroare(String SMS) { Avizier.입출력전환(0); 단말.Scriere("Comandă analiza_VALUE: "); 단말.Scriere(SMS); 단말.문자(10); Stare_VALUE = 2; }
    static int Citire(int intrare_COUNT, int 중첩깊이) {
        int curent_INDEX = 0, total_COUNT = 0, BASE_poziție = 중첩깊이 * 4096, caracter_special = 중첩깊이 * 128;
        while (curent_INDEX < intrare_COUNT) {
            while (curent_INDEX < intrare_COUNT && (SURSĂ[BASE_poziție + curent_INDEX] == 32 || SURSĂ[BASE_poziție + curent_INDEX] == 9)) curent_INDEX++;
            if (curent_INDEX == intrare_COUNT || SURSĂ[BASE_poziție + curent_INDEX] == '#') break;
            if (total_COUNT == 128) { eroare("낱말이 너무 많습니다"); return -1; }
            int buta_poziție = curent_INDEX, cod_caracter = SURSĂ[BASE_poziție + curent_INDEX], 자료종류 = 0;
            if (cod_caracter == ';') { 자료종류 = 1; curent_INDEX++; }
            else if (cod_caracter == '&') { if (curent_INDEX + 1 >= intrare_COUNT || SURSĂ[BASE_poziție + curent_INDEX + 1] != '&') { eroare("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } 자료종류 = 2; curent_INDEX += 2; }
            else if (cod_caracter == '|') { curent_INDEX++; 자료종류 = curent_INDEX < intrare_COUNT && SURSĂ[BASE_poziție + curent_INDEX] == '|' ? 3 : 4; if (자료종류 == 3) curent_INDEX++; }
            else if (cod_caracter == '>') { curent_INDEX++; 자료종류 = curent_INDEX < intrare_COUNT && SURSĂ[BASE_poziție + curent_INDEX] == '>' ? 6 : 5; if (자료종류 == 6) curent_INDEX++; }
            else if (cod_caracter == '<') { 자료종류 = 7; curent_INDEX++; }
            else {
                int Citat = 0;
                while (curent_INDEX < intrare_COUNT) {
                    cod_caracter = SURSĂ[BASE_poziție + curent_INDEX];
                    if (cod_caracter == '`' && Citat != 39 || cod_caracter == '$' && Citat != 39 && curent_INDEX + 1 < intrare_COUNT && SURSĂ[BASE_poziție + curent_INDEX + 1] == '(') { eroare("Comandă KR 치환은 지원하지 않습니다"); return -1; }
                    if (cod_caracter == '\\' && Citat != 39) { if (++curent_INDEX == intrare_COUNT) { eroare("Linie 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } curent_INDEX++; continue; }
                    if (cod_caracter == Citat) { Citat = 0; curent_INDEX++; continue; }
                    if (Citat == 0 && (cod_caracter == 39 || cod_caracter == 34)) { Citat = cod_caracter; curent_INDEX++; continue; }
                    if (Citat == 0 && (cod_caracter == 32 || cod_caracter == 9 || cod_caracter == ';' || cod_caracter == '&' || cod_caracter == '|' || cod_caracter == '<' || cod_caracter == '>')) break;
                    curent_INDEX++;
                }
                if (Citat != 0) { eroare("따옴표가 닫히지 않았습니다"); return -1; }
                if (curent_INDEX < intrare_COUNT && (SURSĂ[BASE_poziție + curent_INDEX] == '>' || SURSĂ[BASE_poziție + curent_INDEX] == '<')) {
                    boolean 수치 = curent_INDEX > buta_poziție;
                    for (int Loop_INDEX = buta_poziție; Loop_INDEX < curent_INDEX; Loop_INDEX++) if (SURSĂ[BASE_poziție + Loop_INDEX] < '0' || SURSĂ[BASE_poziție + Loop_INDEX] > '9') 수치 = false;
                    if (수치) { eroare("번호를 지정한 Fișier 서술자 I_O 전환은 지원하지 않습니다"); return -1; }
                }
            }
            종류[caracter_special + total_COUNT] = 자료종류; Pornește[caracter_special + total_COUNT] = buta_poziție; 끝[caracter_special + total_COUNT] = curent_INDEX; total_COUNT++;
        }
        boolean 낱말 = false;
        for (int Loop_INDEX = 0; Loop_INDEX < total_COUNT; Loop_INDEX++) {
            int 임시값 = 종류[caracter_special + Loop_INDEX];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++Loop_INDEX == total_COUNT || 종류[caracter_special + Loop_INDEX] != 0) { eroare("I_O 전환에 Fișier 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || Loop_INDEX == total_COUNT - 1 && 임시값 != 1) { eroare("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (total_COUNT > 0 && !낱말 && 종류[caracter_special + total_COUNT - 1] != 1) { eroare("명령이 빠졌습니다"); return -1; }
        return total_COUNT;
    }
    static boolean zonă_SMS(int[] date_ARRAY, int local_buta, int intrare_COUNT, String caracter_poziție) {
        if (intrare_COUNT != caracter_poziție.length()) return false; for (int Loop_INDEX = 0; Loop_INDEX < intrare_COUNT; Loop_INDEX++) if (date_ARRAY[local_buta + Loop_INDEX] != caracter_poziție.charAt(Loop_INDEX)) return false; return true;
    }
    static void 넣기(int byte_date) {
        if (쓴수 >= 명령해석기.token_VALUE.length) { if (!extensie_eroare) eroare("변수를 펼친 명령이 너무 깁니다"); extensie_eroare = true; return; }
        명령해석기.token_VALUE[쓴수++] = byte_date;
    }
    static void variabilă_VALUE(int[] date_ARRAY, int buta_poziție, int intrare_COUNT) {
        if (zonă_SMS(date_ARRAY, buta_poziție, intrare_COUNT, "PWD")) { 넣기('/'); for (int Loop_INDEX = 0; Loop_INDEX < Memorie_Fișiere.curent_lungime; Loop_INDEX++) 넣기(Memorie_Fișiere.curent_element[Loop_INDEX]); return; }
        if (zonă_SMS(date_ARRAY, buta_poziție, intrare_COUNT, "HOME")) { 넣기('/'); return; }
        if (zonă_SMS(date_ARRAY, buta_poziție, intrare_COUNT, "?")) {
            int date_VALUE = Stare_VALUE, cifră = 100; boolean 시작여부 = false;
            while (cifră > 0) { int 뒷값 = date_VALUE / cifră; if (뒷값 != 0 || 시작여부 || cifră == 1) { 넣기('0' + 뒷값); 시작여부 = true; } date_VALUE %= cifră; cifră /= 10; } return;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] == intrare_COUNT) {
            boolean MATCH = true; for (int internă_poziție = 0; internă_poziție < intrare_COUNT; internă_poziție++) if (variabilă_nume[Loop_INDEX * 32 + internă_poziție] != date_ARRAY[buta_poziție + internă_poziție]) MATCH = false;
            if (MATCH) { for (int internă_poziție = 0; internă_poziție < VALUE_lungime[Loop_INDEX]; internă_poziție++) 넣기(variabilă_date[Loop_INDEX * 256 + internă_poziție]); return; }
        }
    }
    static boolean Word_VALUE(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = Pornește[중첩깊이 * 128 + 낱말번호], termina_un_apel_poziție = 끝[중첩깊이 * 128 + 낱말번호], BASE_poziție = 중첩깊이 * 4096, Citat = 0;
        if (읽는자리 < termina_un_apel_poziție && SURSĂ[BASE_poziție + 읽는자리] == '~' && (읽는자리 + 1 == termina_un_apel_poziție || SURSĂ[BASE_poziție + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < termina_un_apel_poziție) {
            int cod_caracter = SURSĂ[BASE_poziție + 읽는자리++];
            if (cod_caracter == Citat) { Citat = 0; continue; }
            if (Citat == 0 && (cod_caracter == 39 || cod_caracter == 34)) { Citat = cod_caracter; continue; }
            if (cod_caracter == '\\' && Citat != 39) { int Următorul_poziție = SURSĂ[BASE_poziție + 읽는자리++]; if (Citat == 34 && Următorul_poziție != '$' && Următorul_poziție != '"' && Următorul_poziție != '\\') 넣기('\\'); 넣기(Următorul_poziție); continue; }
            if (cod_caracter == '$' && Citat != 39 && 읽는자리 < termina_un_apel_poziție) {
                boolean 중괄호자리 = SURSĂ[BASE_poziție + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < termina_un_apel_poziție && SURSĂ[BASE_poziție + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < termina_un_apel_poziție && 이름뒤(SURSĂ[BASE_poziție + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == termina_un_apel_poziție || SURSĂ[BASE_poziție + 읽는자리] != '}')) { eroare("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                variabilă_VALUE(SURSĂ, BASE_poziție + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(cod_caracter);
        }
        return !extensie_eroare;
    }
    static int 환경설정(int argument_INDEX, boolean elimina) {
        int local_buta = 명령해석기.시작점[argument_INDEX], termina_un_apel_poziție = local_buta + 명령해석기.lungime_VALUE[argument_INDEX], 같음자리 = local_buta;
        while (같음자리 < termina_un_apel_poziție && 명령해석기.token_VALUE[같음자리] != '=') 같음자리++;
        int intrare_COUNT = 같음자리 - local_buta;
        if (intrare_COUNT < 1 || intrare_COUNT > 31 || !nume_caracter(명령해석기.token_VALUE[local_buta]) || !elimina && 같음자리 == termina_un_apel_poziție || termina_un_apel_poziție - 같음자리 - 1 > 255) return 2;
        for (int Loop_INDEX = local_buta; Loop_INDEX < 같음자리; Loop_INDEX++) if (!이름뒤(명령해석기.token_VALUE[Loop_INDEX])) return 2;
        if (zonă_SMS(명령해석기.token_VALUE, local_buta, intrare_COUNT, "PWD") || zonă_SMS(명령해석기.token_VALUE, local_buta, intrare_COUNT, "HOME")) return 2;
        int 찾은여부 = -1, 빈여부 = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] == 0) 빈여부 = Loop_INDEX;
            if (이름길이[Loop_INDEX] != intrare_COUNT) continue;
            boolean MATCH = true; for (int internă_poziție = 0; internă_poziție < intrare_COUNT; internă_poziție++) if (variabilă_nume[Loop_INDEX * 32 + internă_poziție] != 명령해석기.token_VALUE[local_buta + internă_poziție]) MATCH = false;
            if (MATCH) 찾은여부 = Loop_INDEX;
        }
        if (elimina) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = 빈여부; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = intrare_COUNT; VALUE_lungime[찾은여부] = termina_un_apel_poziție - 같음자리 - 1;
        for (int Loop_INDEX = 0; Loop_INDEX < intrare_COUNT; Loop_INDEX++) variabilă_nume[찾은여부 * 32 + Loop_INDEX] = 명령해석기.token_VALUE[local_buta + Loop_INDEX];
        for (int Loop_INDEX = 같음자리 + 1; Loop_INDEX < termina_un_apel_poziție; Loop_INDEX++) variabilă_date[찾은여부 * 256 + Loop_INDEX - 같음자리 - 1] = 명령해석기.token_VALUE[Loop_INDEX];
        return 0;
    }
    static void 환경보기() {
        단말.Scriere("HOME=/\nPWD="); Memorie_Fișiere.curent_scriere(); 단말.문자(10);
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] > 0) {
            for (int internă_poziție = 0; internă_poziție < 이름길이[Loop_INDEX]; internă_poziție++) Avizier.직렬쓰기(variabilă_nume[Loop_INDEX * 32 + internă_poziție]); 단말.문자('=');
            for (int internă_poziție = 0; internă_poziție < VALUE_lungime[Loop_INDEX]; internă_poziție++) Avizier.직렬쓰기(variabilă_date[Loop_INDEX * 256 + internă_poziție]); 단말.문자(10);
        }
    }
    static void executa_comandă(int[] date_ARRAY, int 시작변위, int intrare_COUNT, int 중첩깊이) {
        if (중첩깊이 >= 4 || intrare_COUNT > 4096) { eroare("Comandă 파일의 imbricare_VALUE 또는 Linie lungime_VALUE 제한을 넘었습니다"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < intrare_COUNT; Loop_INDEX++) SURSĂ[중첩깊이 * 4096 + Loop_INDEX] = date_ARRAY[시작변위 + Loop_INDEX];
        int total_COUNT = Citire(intrare_COUNT, 중첩깊이); if (total_COUNT < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < total_COUNT) {
            int grup_termina_un_apel = 읽는자리;
            while (grup_termina_un_apel < total_COUNT && (종류[중첩깊이 * 128 + grup_termina_un_apel] == 0 || 종류[중첩깊이 * 128 + grup_termina_un_apel] >= 4)) grup_termina_un_apel++;
            boolean executa = 조건성립 == 1 || 조건성립 == 2 && Stare_VALUE == 0 || 조건성립 == 3 && Stare_VALUE != 0;
            if (executa) {
                boolean Anteriorul_element_INDEX = false;
                while (읽는자리 < grup_termina_un_apel) {
                    int Următorul_poziție = 읽는자리; while (Următorul_poziție < grup_termina_un_apel && 종류[중첩깊이 * 128 + Următorul_poziție] != 4) Următorul_poziție++;
                    boolean conecta_flux = Următorul_poziție < grup_termina_un_apel; int 입력쪽 = -1, 출력쪽 = -1, 출력방식 = 0;
                    명령해석기.token_COUNT = 0; 쓴수 = 0; extensie_eroare = false;
                    for (int Loop_INDEX = 읽는자리; Loop_INDEX < Următorul_poziție; Loop_INDEX++) {
                        int 자료종류 = 종류[중첩깊이 * 128 + Loop_INDEX];
                        if (자료종류 >= 5) { if (자료종류 == 7) { if (입력쪽 >= 0) { eroare("입력 전환이 겹쳤습니다"); return; } 입력쪽 = ++Loop_INDEX; } else { if (출력쪽 >= 0) { eroare("Rezultat 전환이 겹쳤습니다"); return; } 출력쪽 = ++Loop_INDEX; 출력방식 = 자료종류; } continue; }
                        if (명령해석기.token_COUNT == 32) { eroare("인수가 너무 많습니다"); return; }
                        int argument_INDEX = 명령해석기.token_COUNT++; 명령해석기.시작점[argument_INDEX] = 쓴수;
                        if (!Word_VALUE(Loop_INDEX, 중첩깊이)) return;
                        명령해석기.lungime_VALUE[argument_INDEX] = 쓴수 - 명령해석기.시작점[argument_INDEX];
                    }
                    연결중 = Anteriorul_element_INDEX || conecta_flux || 입력쪽 >= 0 || 출력쪽 >= 0;
                    if (연결중 && (명령해석기.같음(0, "vi") || 명령해석기.같음(0, "edit") || 명령해석기.같음(0, "load") || 명령해석기.같음(0, "gui") || 명령해석기.같음(0, "terminal") || 명령해석기.같음(0, "sh") || 명령해석기.같음(0, "source"))) { eroare("대화형 명령과 Comandă 파일은 I_O 전환이나 flux_VALUE 연결에 쓸 수 없습니다"); return; }
                    셸입출력.Pornește(Anteriorul_element_INDEX, conecta_flux);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int intrare_poziție = 입출력바꿈 == 0 ? 입력쪽 : 출력쪽; if (intrare_poziție < 0) continue;
                        int buta_poziție = 쓴수; if (!Word_VALUE(intrare_poziție, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = Memorie_Fișiere.cale_buta(쓴수 - buta_poziție);
                        for (int internă_poziție = buta_poziție; 처리값 >= 0 && internă_poziție < 쓴수; internă_poziție++) 처리값 = Memorie_Fișiere.cale_byte(internă_poziție - buta_poziție, 명령해석기.token_VALUE[internă_poziție]);
                        if (처리값 >= 0) 처리값 = Memorie_Fișiere.Deschide(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); 명령해석기.eroare(처리값); Stare_VALUE = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.fișier_de_intrare = 처리값; else 셸입출력.fișier_de_ieșire = 처리값;
                    }
                    셸입출력.대화허용 = 중첩깊이 == 0 && 읽는자리 == 0 && Următorul_poziție == total_COUNT;
                    깊이 = 중첩깊이; 명령해석기.KR = 0; Avizier.입출력전환(1);
                    명령해석기.Comandă();
                    Avizier.Terminal(3);
                    int 반환값 = 명령해석기.KR, flux_eroare = 셸입출력.eroare_VALUE;
                    셸입출력.끝(); 연결중 = false;
                    Stare_VALUE = flux_eroare < 0 ? 1 : 반환값;
                    if (flux_eroare < 0) { 명령해석기.eroare(flux_eroare); return; }
                    if (script_termina_un_apel || 반환값 == -1005) return;
                    Anteriorul_element_INDEX = true; 읽는자리 = Următorul_poziție + 1;
                }
            }
            if (grup_termina_un_apel < total_COUNT) 조건성립 = 종류[중첩깊이 * 128 + grup_termina_un_apel];
            읽는자리 = grup_termina_un_apel + 1;
        }
    }
    static void executa_Fișier() {
        if (명령해석기.token_COUNT != 2 || 깊이 >= 3) { 명령해석기.KR = 2; 단말.Scriere("사용법: sh Fișier (imbricare_VALUE 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = 명령해석기.Cale(1); if (처리값 >= 0) 처리값 = Memorie_Fișiere.Deschide(0);
        if (처리값 < 0) { 명령해석기.eroare(처리값); return; }
        int intrare_COUNT = 0, byte_date;
        while ((byte_date = Memorie_Fișiere.Citire(처리값)) != 256 && byte_date >= 0 && intrare_COUNT < 16384) script_VALUE[중첩깊이 * 16384 + intrare_COUNT++] = byte_date;
        Memorie_Fișiere.Închide(처리값); Avizier.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < intrare_COUNT && !script_termina_un_apel;) {
            int termina_un_apel_poziție = 읽는자리; while (termina_un_apel_poziție < intrare_COUNT && script_VALUE[중첩깊이 * 16384 + termina_un_apel_poziție] != 10) termina_un_apel_poziție++;
            int 유효길이 = termina_un_apel_poziție - 읽는자리; if (유효길이 > 0 && script_VALUE[중첩깊이 * 16384 + termina_un_apel_poziție - 1] == 13) 유효길이--;
            executa_comandă(script_VALUE, 중첩깊이 * 16384 + 읽는자리, 유효길이, 중첩깊이); 읽는자리 = termina_un_apel_poziție + 1;
        }
        명령해석기.KR = Stare_VALUE; script_termina_un_apel = false; 깊이 = 중첩깊이 - 1;
    }
}
