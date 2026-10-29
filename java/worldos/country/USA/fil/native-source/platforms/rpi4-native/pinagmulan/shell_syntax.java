// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 tumutugon_interactive shell 문법. 파이프는 순차 Mag_execute_utos, 환경은 같은 셸에서 공유한다. */
public final class shell_syntax {
    static int[] pinagmulan = new int[4 * 4096], 종류 = new int[4 * 128], run = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] 변수이름 = new int[16 * 32], 변수값 = new int[16 * 256], 이름길이 = new int[16], VALUE_haba = new int[16];
    static int[] script_VALUE = new int[4 * 16384];
    static int katayuan_VALUE, 깊이, 쓴수;
    static boolean 연결중, script_tapusin, extension_error;
    static boolean pangalan_karakter(int character_code) { return character_code >= 'a' && character_code <= 'z' || character_code >= 'A' && character_code <= 'Z' || character_code == '_' || character_code >= 128; }
    static boolean 이름뒤(int character_code) { return pangalan_karakter(character_code) || character_code >= '0' && character_code <= '9'; }
    static void error(String SMS) { board.입출력전환(0); 단말.sumulat("utos mag_parse_VALUE: "); 단말.sumulat(SMS); 단말.문자(10); katayuan_VALUE = 2; }
    static int 읽기(int pagpasok_COUNT, int 중첩깊이) {
        int 현재자리 = 0, 총수 = 0, BASE_posisyon = 중첩깊이 * 4096, espesyal_na_character = 중첩깊이 * 128;
        while (현재자리 < pagpasok_COUNT) {
            while (현재자리 < pagpasok_COUNT && (pinagmulan[BASE_posisyon + 현재자리] == 32 || pinagmulan[BASE_posisyon + 현재자리] == 9)) 현재자리++;
            if (현재자리 == pagpasok_COUNT || pinagmulan[BASE_posisyon + 현재자리] == '#') break;
            if (총수 == 128) { error("낱말이 너무 많습니다"); return -1; }
            int Start_posisyon = 현재자리, character_code = pinagmulan[BASE_posisyon + 현재자리], 자료종류 = 0;
            if (character_code == ';') { 자료종류 = 1; 현재자리++; }
            else if (character_code == '&') { if (현재자리 + 1 >= pagpasok_COUNT || pinagmulan[BASE_posisyon + 현재자리 + 1] != '&') { error("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } 자료종류 = 2; 현재자리 += 2; }
            else if (character_code == '|') { 현재자리++; 자료종류 = 현재자리 < pagpasok_COUNT && pinagmulan[BASE_posisyon + 현재자리] == '|' ? 3 : 4; if (자료종류 == 3) 현재자리++; }
            else if (character_code == '>') { 현재자리++; 자료종류 = 현재자리 < pagpasok_COUNT && pinagmulan[BASE_posisyon + 현재자리] == '>' ? 6 : 5; if (자료종류 == 6) 현재자리++; }
            else if (character_code == '<') { 자료종류 = 7; 현재자리++; }
            else {
                int Quote = 0;
                while (현재자리 < pagpasok_COUNT) {
                    character_code = pinagmulan[BASE_posisyon + 현재자리];
                    if (character_code == '`' && Quote != 39 || character_code == '$' && Quote != 39 && 현재자리 + 1 < pagpasok_COUNT && pinagmulan[BASE_posisyon + 현재자리 + 1] == '(') { error("utos sukat 치환은 지원하지 않습니다"); return -1; }
                    if (character_code == '\\' && Quote != 39) { if (++현재자리 == pagpasok_COUNT) { error("linya 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } 현재자리++; continue; }
                    if (character_code == Quote) { Quote = 0; 현재자리++; continue; }
                    if (Quote == 0 && (character_code == 39 || character_code == 34)) { Quote = character_code; 현재자리++; continue; }
                    if (Quote == 0 && (character_code == 32 || character_code == 9 || character_code == ';' || character_code == '&' || character_code == '|' || character_code == '<' || character_code == '>')) break;
                    현재자리++;
                }
                if (Quote != 0) { error("따옴표가 닫히지 않았습니다"); return -1; }
                if (현재자리 < pagpasok_COUNT && (pinagmulan[BASE_posisyon + 현재자리] == '>' || pinagmulan[BASE_posisyon + 현재자리] == '<')) {
                    boolean 수치 = 현재자리 > Start_posisyon;
                    for (int Loop_INDEX = Start_posisyon; Loop_INDEX < 현재자리; Loop_INDEX++) if (pinagmulan[BASE_posisyon + Loop_INDEX] < '0' || pinagmulan[BASE_posisyon + Loop_INDEX] > '9') 수치 = false;
                    if (수치) { error("번호를 지정한 file 서술자 I_O 전환은 지원하지 않습니다"); return -1; }
                }
            }
            종류[espesyal_na_character + 총수] = 자료종류; run[espesyal_na_character + 총수] = Start_posisyon; 끝[espesyal_na_character + 총수] = 현재자리; 총수++;
        }
        boolean 낱말 = false;
        for (int Loop_INDEX = 0; Loop_INDEX < 총수; Loop_INDEX++) {
            int 임시값 = 종류[espesyal_na_character + Loop_INDEX];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++Loop_INDEX == 총수 || 종류[espesyal_na_character + Loop_INDEX] != 0) { error("I_O 전환에 file 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || Loop_INDEX == 총수 - 1 && 임시값 != 1) { error("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (총수 > 0 && !낱말 && 종류[espesyal_na_character + 총수 - 1] != 1) { error("명령이 빠졌습니다"); return -1; }
        return 총수;
    }
    static boolean 구간말(int[] data_ARRAY, int lokal_Start, int pagpasok_COUNT, String karakter_posisyon) {
        if (pagpasok_COUNT != karakter_posisyon.length()) return false; for (int Loop_INDEX = 0; Loop_INDEX < pagpasok_COUNT; Loop_INDEX++) if (data_ARRAY[lokal_Start + Loop_INDEX] != karakter_posisyon.charAt(Loop_INDEX)) return false; return true;
    }
    static void 넣기(int byte_data) {
        if (쓴수 >= 명령해석기.token_VALUE.length) { if (!extension_error) error("변수를 펼친 명령이 너무 깁니다"); extension_error = true; return; }
        명령해석기.token_VALUE[쓴수++] = byte_data;
    }
    static void 변수(int[] data_ARRAY, int Start_posisyon, int pagpasok_COUNT) {
        if (구간말(data_ARRAY, Start_posisyon, pagpasok_COUNT, "PWD")) { 넣기('/'); for (int Loop_INDEX = 0; Loop_INDEX < Memory_Mga_File.현재길이; Loop_INDEX++) 넣기(Memory_Mga_File.현재[Loop_INDEX]); return; }
        if (구간말(data_ARRAY, Start_posisyon, pagpasok_COUNT, "HOME")) { 넣기('/'); return; }
        if (구간말(data_ARRAY, Start_posisyon, pagpasok_COUNT, "?")) {
            int data_VALUE = katayuan_VALUE, digit = 100; boolean 시작여부 = false;
            while (digit > 0) { int 뒷값 = data_VALUE / digit; if (뒷값 != 0 || 시작여부 || digit == 1) { 넣기('0' + 뒷값); 시작여부 = true; } data_VALUE %= digit; digit /= 10; } return;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] == pagpasok_COUNT) {
            boolean MATCH = true; for (int inner_join_posisyon = 0; inner_join_posisyon < pagpasok_COUNT; inner_join_posisyon++) if (변수이름[Loop_INDEX * 32 + inner_join_posisyon] != data_ARRAY[Start_posisyon + inner_join_posisyon]) MATCH = false;
            if (MATCH) { for (int inner_join_posisyon = 0; inner_join_posisyon < VALUE_haba[Loop_INDEX]; inner_join_posisyon++) 넣기(변수값[Loop_INDEX * 256 + inner_join_posisyon]); return; }
        }
    }
    static boolean Word_VALUE(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = run[중첩깊이 * 128 + 낱말번호], tapusin_posisyon = 끝[중첩깊이 * 128 + 낱말번호], BASE_posisyon = 중첩깊이 * 4096, Quote = 0;
        if (읽는자리 < tapusin_posisyon && pinagmulan[BASE_posisyon + 읽는자리] == '~' && (읽는자리 + 1 == tapusin_posisyon || pinagmulan[BASE_posisyon + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < tapusin_posisyon) {
            int character_code = pinagmulan[BASE_posisyon + 읽는자리++];
            if (character_code == Quote) { Quote = 0; continue; }
            if (Quote == 0 && (character_code == 39 || character_code == 34)) { Quote = character_code; continue; }
            if (character_code == '\\' && Quote != 39) { int Susunod_posisyon = pinagmulan[BASE_posisyon + 읽는자리++]; if (Quote == 34 && Susunod_posisyon != '$' && Susunod_posisyon != '"' && Susunod_posisyon != '\\') 넣기('\\'); 넣기(Susunod_posisyon); continue; }
            if (character_code == '$' && Quote != 39 && 읽는자리 < tapusin_posisyon) {
                boolean 중괄호자리 = pinagmulan[BASE_posisyon + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < tapusin_posisyon && pinagmulan[BASE_posisyon + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < tapusin_posisyon && 이름뒤(pinagmulan[BASE_posisyon + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == tapusin_posisyon || pinagmulan[BASE_posisyon + 읽는자리] != '}')) { error("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                변수(pinagmulan, BASE_posisyon + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(character_code);
        }
        return !extension_error;
    }
    static int 환경설정(int argumento_INDEX, boolean tanggalin) {
        int lokal_Start = 명령해석기.시작점[argumento_INDEX], tapusin_posisyon = lokal_Start + 명령해석기.haba_VALUE[argumento_INDEX], 같음자리 = lokal_Start;
        while (같음자리 < tapusin_posisyon && 명령해석기.token_VALUE[같음자리] != '=') 같음자리++;
        int pagpasok_COUNT = 같음자리 - lokal_Start;
        if (pagpasok_COUNT < 1 || pagpasok_COUNT > 31 || !pangalan_karakter(명령해석기.token_VALUE[lokal_Start]) || !tanggalin && 같음자리 == tapusin_posisyon || tapusin_posisyon - 같음자리 - 1 > 255) return 2;
        for (int Loop_INDEX = lokal_Start; Loop_INDEX < 같음자리; Loop_INDEX++) if (!이름뒤(명령해석기.token_VALUE[Loop_INDEX])) return 2;
        if (구간말(명령해석기.token_VALUE, lokal_Start, pagpasok_COUNT, "PWD") || 구간말(명령해석기.token_VALUE, lokal_Start, pagpasok_COUNT, "HOME")) return 2;
        int 찾은여부 = -1, information_technology_walang_laman_katayuan = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] == 0) information_technology_walang_laman_katayuan = Loop_INDEX;
            if (이름길이[Loop_INDEX] != pagpasok_COUNT) continue;
            boolean MATCH = true; for (int inner_join_posisyon = 0; inner_join_posisyon < pagpasok_COUNT; inner_join_posisyon++) if (변수이름[Loop_INDEX * 32 + inner_join_posisyon] != 명령해석기.token_VALUE[lokal_Start + inner_join_posisyon]) MATCH = false;
            if (MATCH) 찾은여부 = Loop_INDEX;
        }
        if (tanggalin) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = information_technology_walang_laman_katayuan; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = pagpasok_COUNT; VALUE_haba[찾은여부] = tapusin_posisyon - 같음자리 - 1;
        for (int Loop_INDEX = 0; Loop_INDEX < pagpasok_COUNT; Loop_INDEX++) 변수이름[찾은여부 * 32 + Loop_INDEX] = 명령해석기.token_VALUE[lokal_Start + Loop_INDEX];
        for (int Loop_INDEX = 같음자리 + 1; Loop_INDEX < tapusin_posisyon; Loop_INDEX++) 변수값[찾은여부 * 256 + Loop_INDEX - 같음자리 - 1] = 명령해석기.token_VALUE[Loop_INDEX];
        return 0;
    }
    static void 환경보기() {
        단말.sumulat("HOME=/\nPWD="); Memory_Mga_File.현재쓰기(); 단말.문자(10);
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] > 0) {
            for (int inner_join_posisyon = 0; inner_join_posisyon < 이름길이[Loop_INDEX]; inner_join_posisyon++) board.직렬쓰기(변수이름[Loop_INDEX * 32 + inner_join_posisyon]); 단말.문자('=');
            for (int inner_join_posisyon = 0; inner_join_posisyon < VALUE_haba[Loop_INDEX]; inner_join_posisyon++) board.직렬쓰기(변수값[Loop_INDEX * 256 + inner_join_posisyon]); 단말.문자(10);
        }
    }
    static void Mag_execute_utos(int[] data_ARRAY, int 시작변위, int pagpasok_COUNT, int 중첩깊이) {
        if (중첩깊이 >= 4 || pagpasok_COUNT > 4096) { error("utos 파일의 nesting_VALUE 또는 linya haba_VALUE 제한을 넘었습니다"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < pagpasok_COUNT; Loop_INDEX++) pinagmulan[중첩깊이 * 4096 + Loop_INDEX] = data_ARRAY[시작변위 + Loop_INDEX];
        int 총수 = 읽기(pagpasok_COUNT, 중첩깊이); if (총수 < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < 총수) {
            int Grupo_tapusin = 읽는자리;
            while (Grupo_tapusin < 총수 && (종류[중첩깊이 * 128 + Grupo_tapusin] == 0 || 종류[중첩깊이 * 128 + Grupo_tapusin] >= 4)) Grupo_tapusin++;
            boolean Mag_execute = 조건성립 == 1 || 조건성립 == 2 && katayuan_VALUE == 0 || 조건성립 == 3 && katayuan_VALUE != 0;
            if (Mag_execute) {
                boolean 이전자리 = false;
                while (읽는자리 < Grupo_tapusin) {
                    int Susunod_posisyon = 읽는자리; while (Susunod_posisyon < Grupo_tapusin && 종류[중첩깊이 * 128 + Susunod_posisyon] != 4) Susunod_posisyon++;
                    boolean CONNECT_Stream = Susunod_posisyon < Grupo_tapusin; int 입력쪽 = -1, 출력쪽 = -1, 출력방식 = 0;
                    명령해석기.token_COUNT = 0; 쓴수 = 0; extension_error = false;
                    for (int Loop_INDEX = 읽는자리; Loop_INDEX < Susunod_posisyon; Loop_INDEX++) {
                        int 자료종류 = 종류[중첩깊이 * 128 + Loop_INDEX];
                        if (자료종류 >= 5) { if (자료종류 == 7) { if (입력쪽 >= 0) { error("입력 전환이 겹쳤습니다"); return; } 입력쪽 = ++Loop_INDEX; } else { if (출력쪽 >= 0) { error("출력 전환이 겹쳤습니다"); return; } 출력쪽 = ++Loop_INDEX; 출력방식 = 자료종류; } continue; }
                        if (명령해석기.token_COUNT == 32) { error("인수가 너무 많습니다"); return; }
                        int argumento_INDEX = 명령해석기.token_COUNT++; 명령해석기.시작점[argumento_INDEX] = 쓴수;
                        if (!Word_VALUE(Loop_INDEX, 중첩깊이)) return;
                        명령해석기.haba_VALUE[argumento_INDEX] = 쓴수 - 명령해석기.시작점[argumento_INDEX];
                    }
                    연결중 = 이전자리 || CONNECT_Stream || 입력쪽 >= 0 || 출력쪽 >= 0;
                    if (연결중 && (명령해석기.같음(0, "vi") || 명령해석기.같음(0, "edit") || 명령해석기.같음(0, "load") || 명령해석기.같음(0, "gui") || 명령해석기.같음(0, "terminal") || 명령해석기.같음(0, "sh") || 명령해석기.같음(0, "source"))) { error("tumutugon_interactive 명령과 utos 파일은 I_O 전환이나 Stream_VALUE 연결에 쓸 수 없습니다"); return; }
                    셸입출력.run(이전자리, CONNECT_Stream);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int pagpasok_posisyon = 입출력바꿈 == 0 ? 입력쪽 : 출력쪽; if (pagpasok_posisyon < 0) continue;
                        int Start_posisyon = 쓴수; if (!Word_VALUE(pagpasok_posisyon, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = Memory_Mga_File.path_Start(쓴수 - Start_posisyon);
                        for (int inner_join_posisyon = Start_posisyon; 처리값 >= 0 && inner_join_posisyon < 쓴수; inner_join_posisyon++) 처리값 = Memory_Mga_File.path_byte(inner_join_posisyon - Start_posisyon, 명령해석기.token_VALUE[inner_join_posisyon]);
                        if (처리값 >= 0) 처리값 = Memory_Mga_File.buksan(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); 명령해석기.error(처리값); katayuan_VALUE = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.입력파일 = 처리값; else 셸입출력.file_ng_output = 처리값;
                    }
                    셸입출력.payagan_tumutugon_interactive = 중첩깊이 == 0 && 읽는자리 == 0 && Susunod_posisyon == 총수;
                    깊이 = 중첩깊이; 명령해석기.sukat = 0; board.입출력전환(1);
                    명령해석기.utos();
                    board.Terminal(3);
                    int 반환값 = 명령해석기.sukat, Stream_error = 셸입출력.pagpalya_VALUE;
                    셸입출력.끝(); 연결중 = false;
                    katayuan_VALUE = Stream_error < 0 ? 1 : 반환값;
                    if (Stream_error < 0) { 명령해석기.error(Stream_error); return; }
                    if (script_tapusin || 반환값 == -1005) return;
                    이전자리 = true; 읽는자리 = Susunod_posisyon + 1;
                }
            }
            if (Grupo_tapusin < 총수) 조건성립 = 종류[중첩깊이 * 128 + Grupo_tapusin];
            읽는자리 = Grupo_tapusin + 1;
        }
    }
    static void Mag_execute_file() {
        if (명령해석기.token_COUNT != 2 || 깊이 >= 3) { 명령해석기.sukat = 2; 단말.sumulat("사용법: sh file (nesting_VALUE 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = 명령해석기.path(1); if (처리값 >= 0) 처리값 = Memory_Mga_File.buksan(0);
        if (처리값 < 0) { 명령해석기.error(처리값); return; }
        int pagpasok_COUNT = 0, byte_data;
        while ((byte_data = Memory_Mga_File.읽기(처리값)) != 256 && byte_data >= 0 && pagpasok_COUNT < 16384) script_VALUE[중첩깊이 * 16384 + pagpasok_COUNT++] = byte_data;
        Memory_Mga_File.isara(처리값); board.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < pagpasok_COUNT && !script_tapusin;) {
            int tapusin_posisyon = 읽는자리; while (tapusin_posisyon < pagpasok_COUNT && script_VALUE[중첩깊이 * 16384 + tapusin_posisyon] != 10) tapusin_posisyon++;
            int 유효길이 = tapusin_posisyon - 읽는자리; if (유효길이 > 0 && script_VALUE[중첩깊이 * 16384 + tapusin_posisyon - 1] == 13) 유효길이--;
            Mag_execute_utos(script_VALUE, 중첩깊이 * 16384 + 읽는자리, 유효길이, 중첩깊이); 읽는자리 = tapusin_posisyon + 1;
        }
        명령해석기.sukat = katayuan_VALUE; script_tapusin = false; 깊이 = 중첩깊이 - 1;
    }
}
