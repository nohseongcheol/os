// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 rhyngweithiol cragen 문법. 파이프는 순차 Gweithredu_gorchymyn, 환경은 같은 셸에서 공유한다. */
public final class cragen_cystrawen {
    static int[] FFYNHONNELL = new int[4 * 4096], 종류 = new int[4 * 128], Gweithredu_2 = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] 변수이름 = new int[16 * 32], 변수값 = new int[16 * 256], 이름길이 = new int[16], VALUE_hyd = new int[16];
    static int[] sgript_VALUE = new int[4 * 16384];
    static int cyflwr_VALUE, 깊이, 쓴수;
    static boolean 연결중, sgript_gorffen, estyniad_gwall;
    static boolean enw_nod(int cod_nod) { return cod_nod >= 'a' && cod_nod <= 'z' || cod_nod >= 'A' && cod_nod <= 'Z' || cod_nod == '_' || cod_nod >= 128; }
    static boolean 이름뒤(int cod_nod) { return enw_nod(cod_nod) || cod_nod >= '0' && cod_nod <= '9'; }
    static void Gwall(String Testun) { bwrdd.입출력전환(0); 단말.Ysgrifennu("Gorchymyn dosrannu_VALUE: "); 단말.Ysgrifennu(Testun); 단말.문자(10); cyflwr_VALUE = 2; }
    static int Darllen(int cofnod_COUNT, int 중첩깊이) {
        int 현재자리 = 0, 총수 = 0, BASE_safle = 중첩깊이 * 4096, nod_arbennig = 중첩깊이 * 128;
        while (현재자리 < cofnod_COUNT) {
            while (현재자리 < cofnod_COUNT && (FFYNHONNELL[BASE_safle + 현재자리] == 32 || FFYNHONNELL[BASE_safle + 현재자리] == 9)) 현재자리++;
            if (현재자리 == cofnod_COUNT || FFYNHONNELL[BASE_safle + 현재자리] == '#') break;
            if (총수 == 128) { Gwall("낱말이 너무 많습니다"); return -1; }
            int START_safle = 현재자리, cod_nod = FFYNHONNELL[BASE_safle + 현재자리], 자료종류 = 0;
            if (cod_nod == ';') { 자료종류 = 1; 현재자리++; }
            else if (cod_nod == '&') { if (현재자리 + 1 >= cofnod_COUNT || FFYNHONNELL[BASE_safle + 현재자리 + 1] != '&') { Gwall("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } 자료종류 = 2; 현재자리 += 2; }
            else if (cod_nod == '|') { 현재자리++; 자료종류 = 현재자리 < cofnod_COUNT && FFYNHONNELL[BASE_safle + 현재자리] == '|' ? 3 : 4; if (자료종류 == 3) 현재자리++; }
            else if (cod_nod == '>') { 현재자리++; 자료종류 = 현재자리 < cofnod_COUNT && FFYNHONNELL[BASE_safle + 현재자리] == '>' ? 6 : 5; if (자료종류 == 6) 현재자리++; }
            else if (cod_nod == '<') { 자료종류 = 7; 현재자리++; }
            else {
                int Dyfyniad = 0;
                while (현재자리 < cofnod_COUNT) {
                    cod_nod = FFYNHONNELL[BASE_safle + 현재자리];
                    if (cod_nod == '`' && Dyfyniad != 39 || cod_nod == '$' && Dyfyniad != 39 && 현재자리 + 1 < cofnod_COUNT && FFYNHONNELL[BASE_safle + 현재자리 + 1] == '(') { Gwall("Gorchymyn mesur 치환은 지원하지 않습니다"); return -1; }
                    if (cod_nod == '\\' && Dyfyniad != 39) { if (++현재자리 == cofnod_COUNT) { Gwall("llinell 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } 현재자리++; continue; }
                    if (cod_nod == Dyfyniad) { Dyfyniad = 0; 현재자리++; continue; }
                    if (Dyfyniad == 0 && (cod_nod == 39 || cod_nod == 34)) { Dyfyniad = cod_nod; 현재자리++; continue; }
                    if (Dyfyniad == 0 && (cod_nod == 32 || cod_nod == 9 || cod_nod == ';' || cod_nod == '&' || cod_nod == '|' || cod_nod == '<' || cod_nod == '>')) break;
                    현재자리++;
                }
                if (Dyfyniad != 0) { Gwall("따옴표가 닫히지 않았습니다"); return -1; }
                if (현재자리 < cofnod_COUNT && (FFYNHONNELL[BASE_safle + 현재자리] == '>' || FFYNHONNELL[BASE_safle + 현재자리] == '<')) {
                    boolean 수치 = 현재자리 > START_safle;
                    for (int Loop_INDEX = START_safle; Loop_INDEX < 현재자리; Loop_INDEX++) if (FFYNHONNELL[BASE_safle + Loop_INDEX] < '0' || FFYNHONNELL[BASE_safle + Loop_INDEX] > '9') 수치 = false;
                    if (수치) { Gwall("번호를 지정한 Ffeil 서술자 I_O 전환은 지원하지 않습니다"); return -1; }
                }
            }
            종류[nod_arbennig + 총수] = 자료종류; Gweithredu_2[nod_arbennig + 총수] = START_safle; 끝[nod_arbennig + 총수] = 현재자리; 총수++;
        }
        boolean 낱말 = false;
        for (int Loop_INDEX = 0; Loop_INDEX < 총수; Loop_INDEX++) {
            int 임시값 = 종류[nod_arbennig + Loop_INDEX];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++Loop_INDEX == 총수 || 종류[nod_arbennig + Loop_INDEX] != 0) { Gwall("I_O 전환에 Ffeil 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || Loop_INDEX == 총수 - 1 && 임시값 != 1) { Gwall("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (총수 > 0 && !낱말 && 종류[nod_arbennig + 총수 - 1] != 1) { Gwall("명령이 빠졌습니다"); return -1; }
        return 총수;
    }
    static boolean 구간말(int[] data_ARAE, int lleol_START, int cofnod_COUNT, String nod_safle) {
        if (cofnod_COUNT != nod_safle.length()) return false; for (int Loop_INDEX = 0; Loop_INDEX < cofnod_COUNT; Loop_INDEX++) if (data_ARAE[lleol_START + Loop_INDEX] != nod_safle.charAt(Loop_INDEX)) return false; return true;
    }
    static void 넣기(int beit_data) {
        if (쓴수 >= 명령해석기.tocyn_VALUE_eb540501.length) { if (!estyniad_gwall) Gwall("변수를 펼친 명령이 너무 깁니다"); estyniad_gwall = true; return; }
        명령해석기.tocyn_VALUE_eb540501[쓴수++] = beit_data;
    }
    static void 변수(int[] data_ARAE, int START_safle, int cofnod_COUNT) {
        if (구간말(data_ARAE, START_safle, cofnod_COUNT, "PWD")) { 넣기('/'); for (int Loop_INDEX = 0; Loop_INDEX < Cof_Ffeil.현재길이; Loop_INDEX++) 넣기(Cof_Ffeil.현재[Loop_INDEX]); return; }
        if (구간말(data_ARAE, START_safle, cofnod_COUNT, "HOME")) { 넣기('/'); return; }
        if (구간말(data_ARAE, START_safle, cofnod_COUNT, "?")) {
            int data_VALUE = cyflwr_VALUE, digid = 100; boolean 시작여부 = false;
            while (digid > 0) { int 뒷값 = data_VALUE / digid; if (뒷값 != 0 || 시작여부 || digid == 1) { 넣기('0' + 뒷값); 시작여부 = true; } data_VALUE %= digid; digid /= 10; } return;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] == cofnod_COUNT) {
            boolean MATCH = true; for (int uno_mewnol_safle = 0; uno_mewnol_safle < cofnod_COUNT; uno_mewnol_safle++) if (변수이름[Loop_INDEX * 32 + uno_mewnol_safle] != data_ARAE[START_safle + uno_mewnol_safle]) MATCH = false;
            if (MATCH) { for (int uno_mewnol_safle = 0; uno_mewnol_safle < VALUE_hyd[Loop_INDEX]; uno_mewnol_safle++) 넣기(변수값[Loop_INDEX * 256 + uno_mewnol_safle]); return; }
        }
    }
    static boolean Word_VALUE(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = Gweithredu_2[중첩깊이 * 128 + 낱말번호], gorffen_safle = 끝[중첩깊이 * 128 + 낱말번호], BASE_safle = 중첩깊이 * 4096, Dyfyniad = 0;
        if (읽는자리 < gorffen_safle && FFYNHONNELL[BASE_safle + 읽는자리] == '~' && (읽는자리 + 1 == gorffen_safle || FFYNHONNELL[BASE_safle + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < gorffen_safle) {
            int cod_nod = FFYNHONNELL[BASE_safle + 읽는자리++];
            if (cod_nod == Dyfyniad) { Dyfyniad = 0; continue; }
            if (Dyfyniad == 0 && (cod_nod == 39 || cod_nod == 34)) { Dyfyniad = cod_nod; continue; }
            if (cod_nod == '\\' && Dyfyniad != 39) { int Nesaf_safle = FFYNHONNELL[BASE_safle + 읽는자리++]; if (Dyfyniad == 34 && Nesaf_safle != '$' && Nesaf_safle != '"' && Nesaf_safle != '\\') 넣기('\\'); 넣기(Nesaf_safle); continue; }
            if (cod_nod == '$' && Dyfyniad != 39 && 읽는자리 < gorffen_safle) {
                boolean 중괄호자리 = FFYNHONNELL[BASE_safle + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < gorffen_safle && FFYNHONNELL[BASE_safle + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < gorffen_safle && 이름뒤(FFYNHONNELL[BASE_safle + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == gorffen_safle || FFYNHONNELL[BASE_safle + 읽는자리] != '}')) { Gwall("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                변수(FFYNHONNELL, BASE_safle + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(cod_nod);
        }
        return !estyniad_gwall;
    }
    static int 환경설정(int arg_INDEX, boolean tynnu) {
        int lleol_START = 명령해석기.시작점[arg_INDEX], gorffen_safle = lleol_START + 명령해석기.hyd_VALUE[arg_INDEX], 같음자리 = lleol_START;
        while (같음자리 < gorffen_safle && 명령해석기.tocyn_VALUE_eb540501[같음자리] != '=') 같음자리++;
        int cofnod_COUNT = 같음자리 - lleol_START;
        if (cofnod_COUNT < 1 || cofnod_COUNT > 31 || !enw_nod(명령해석기.tocyn_VALUE_eb540501[lleol_START]) || !tynnu && 같음자리 == gorffen_safle || gorffen_safle - 같음자리 - 1 > 255) return 2;
        for (int Loop_INDEX = lleol_START; Loop_INDEX < 같음자리; Loop_INDEX++) if (!이름뒤(명령해석기.tocyn_VALUE_eb540501[Loop_INDEX])) return 2;
        if (구간말(명령해석기.tocyn_VALUE_eb540501, lleol_START, cofnod_COUNT, "PWD") || 구간말(명령해석기.tocyn_VALUE_eb540501, lleol_START, cofnod_COUNT, "HOME")) return 2;
        int 찾은여부 = -1, technoleg_gwybodaeth_gwag_cyflwr = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] == 0) technoleg_gwybodaeth_gwag_cyflwr = Loop_INDEX;
            if (이름길이[Loop_INDEX] != cofnod_COUNT) continue;
            boolean MATCH = true; for (int uno_mewnol_safle = 0; uno_mewnol_safle < cofnod_COUNT; uno_mewnol_safle++) if (변수이름[Loop_INDEX * 32 + uno_mewnol_safle] != 명령해석기.tocyn_VALUE_eb540501[lleol_START + uno_mewnol_safle]) MATCH = false;
            if (MATCH) 찾은여부 = Loop_INDEX;
        }
        if (tynnu) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = technoleg_gwybodaeth_gwag_cyflwr; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = cofnod_COUNT; VALUE_hyd[찾은여부] = gorffen_safle - 같음자리 - 1;
        for (int Loop_INDEX = 0; Loop_INDEX < cofnod_COUNT; Loop_INDEX++) 변수이름[찾은여부 * 32 + Loop_INDEX] = 명령해석기.tocyn_VALUE_eb540501[lleol_START + Loop_INDEX];
        for (int Loop_INDEX = 같음자리 + 1; Loop_INDEX < gorffen_safle; Loop_INDEX++) 변수값[찾은여부 * 256 + Loop_INDEX - 같음자리 - 1] = 명령해석기.tocyn_VALUE_eb540501[Loop_INDEX];
        return 0;
    }
    static void 환경보기() {
        단말.Ysgrifennu("HOME=/\nPWD="); Cof_Ffeil.현재쓰기(); 단말.문자(10);
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] > 0) {
            for (int uno_mewnol_safle = 0; uno_mewnol_safle < 이름길이[Loop_INDEX]; uno_mewnol_safle++) bwrdd.직렬쓰기(변수이름[Loop_INDEX * 32 + uno_mewnol_safle]); 단말.문자('=');
            for (int uno_mewnol_safle = 0; uno_mewnol_safle < VALUE_hyd[Loop_INDEX]; uno_mewnol_safle++) bwrdd.직렬쓰기(변수값[Loop_INDEX * 256 + uno_mewnol_safle]); 단말.문자(10);
        }
    }
    static void Gweithredu_gorchymyn(int[] data_ARAE, int 시작변위, int cofnod_COUNT, int 중첩깊이) {
        if (중첩깊이 >= 4 || cofnod_COUNT > 4096) { Gwall("Gorchymyn 파일의 중첩 또는 llinell hyd_VALUE 제한을 넘었습니다"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < cofnod_COUNT; Loop_INDEX++) FFYNHONNELL[중첩깊이 * 4096 + Loop_INDEX] = data_ARAE[시작변위 + Loop_INDEX];
        int 총수 = Darllen(cofnod_COUNT, 중첩깊이); if (총수 < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < 총수) {
            int Grŵp_gorffen = 읽는자리;
            while (Grŵp_gorffen < 총수 && (종류[중첩깊이 * 128 + Grŵp_gorffen] == 0 || 종류[중첩깊이 * 128 + Grŵp_gorffen] >= 4)) Grŵp_gorffen++;
            boolean Gweithredu_cc685ae5 = 조건성립 == 1 || 조건성립 == 2 && cyflwr_VALUE == 0 || 조건성립 == 3 && cyflwr_VALUE != 0;
            if (Gweithredu_cc685ae5) {
                boolean 이전자리 = false;
                while (읽는자리 < Grŵp_gorffen) {
                    int Nesaf_safle = 읽는자리; while (Nesaf_safle < Grŵp_gorffen && 종류[중첩깊이 * 128 + Nesaf_safle] != 4) Nesaf_safle++;
                    boolean Cysylltu_ffrwd = Nesaf_safle < Grŵp_gorffen; int 입력쪽 = -1, 출력쪽 = -1, 출력방식 = 0;
                    명령해석기.tocyn_COUNT_3176ee99 = 0; 쓴수 = 0; estyniad_gwall = false;
                    for (int Loop_INDEX = 읽는자리; Loop_INDEX < Nesaf_safle; Loop_INDEX++) {
                        int 자료종류 = 종류[중첩깊이 * 128 + Loop_INDEX];
                        if (자료종류 >= 5) { if (자료종류 == 7) { if (입력쪽 >= 0) { Gwall("입력 전환이 겹쳤습니다"); return; } 입력쪽 = ++Loop_INDEX; } else { if (출력쪽 >= 0) { Gwall("Allbwn 전환이 겹쳤습니다"); return; } 출력쪽 = ++Loop_INDEX; 출력방식 = 자료종류; } continue; }
                        if (명령해석기.tocyn_COUNT_3176ee99 == 32) { Gwall("인수가 너무 많습니다"); return; }
                        int arg_INDEX = 명령해석기.tocyn_COUNT_3176ee99++; 명령해석기.시작점[arg_INDEX] = 쓴수;
                        if (!Word_VALUE(Loop_INDEX, 중첩깊이)) return;
                        명령해석기.hyd_VALUE[arg_INDEX] = 쓴수 - 명령해석기.시작점[arg_INDEX];
                    }
                    연결중 = 이전자리 || Cysylltu_ffrwd || 입력쪽 >= 0 || 출력쪽 >= 0;
                    if (연결중 && (명령해석기.같음(0, "vi") || 명령해석기.같음(0, "edit") || 명령해석기.같음(0, "load") || 명령해석기.같음(0, "gui") || 명령해석기.같음(0, "terminal") || 명령해석기.같음(0, "sh") || 명령해석기.같음(0, "source"))) { Gwall("rhyngweithiol 명령과 Gorchymyn 파일은 I_O 전환이나 ffrwd_VALUE 연결에 쓸 수 없습니다"); return; }
                    셸입출력.Gweithredu_2(이전자리, Cysylltu_ffrwd);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int cofnod_safle = 입출력바꿈 == 0 ? 입력쪽 : 출력쪽; if (cofnod_safle < 0) continue;
                        int START_safle = 쓴수; if (!Word_VALUE(cofnod_safle, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = Cof_Ffeil.llwybr_START(쓴수 - START_safle);
                        for (int uno_mewnol_safle = START_safle; 처리값 >= 0 && uno_mewnol_safle < 쓴수; uno_mewnol_safle++) 처리값 = Cof_Ffeil.llwybr_beit(uno_mewnol_safle - START_safle, 명령해석기.tocyn_VALUE_eb540501[uno_mewnol_safle]);
                        if (처리값 >= 0) 처리값 = Cof_Ffeil.Agor(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); 명령해석기.Gwall(처리값); cyflwr_VALUE = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.입력파일 = 처리값; else 셸입출력.ffeil_allbwn = 처리값;
                    }
                    셸입출력.Caniatáu_rhyngweithiol = 중첩깊이 == 0 && 읽는자리 == 0 && Nesaf_safle == 총수;
                    깊이 = 중첩깊이; 명령해석기.mesur = 0; bwrdd.입출력전환(1);
                    명령해석기.Gorchymyn();
                    bwrdd.Terfynell(3);
                    int 반환값 = 명령해석기.mesur, ffrwd_gwall = 셸입출력.methiant_VALUE;
                    셸입출력.끝(); 연결중 = false;
                    cyflwr_VALUE = ffrwd_gwall < 0 ? 1 : 반환값;
                    if (ffrwd_gwall < 0) { 명령해석기.Gwall(ffrwd_gwall); return; }
                    if (sgript_gorffen || 반환값 == -1005) return;
                    이전자리 = true; 읽는자리 = Nesaf_safle + 1;
                }
            }
            if (Grŵp_gorffen < 총수) 조건성립 = 종류[중첩깊이 * 128 + Grŵp_gorffen];
            읽는자리 = Grŵp_gorffen + 1;
        }
    }
    static void Gweithredu_ffeil() {
        if (명령해석기.tocyn_COUNT_3176ee99 != 2 || 깊이 >= 3) { 명령해석기.mesur = 2; 단말.Ysgrifennu("사용법: sh Ffeil (중첩 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = 명령해석기.LLWYBR(1); if (처리값 >= 0) 처리값 = Cof_Ffeil.Agor(0);
        if (처리값 < 0) { 명령해석기.Gwall(처리값); return; }
        int cofnod_COUNT = 0, beit_data;
        while ((beit_data = Cof_Ffeil.Darllen(처리값)) != 256 && beit_data >= 0 && cofnod_COUNT < 16384) sgript_VALUE[중첩깊이 * 16384 + cofnod_COUNT++] = beit_data;
        Cof_Ffeil.Cau(처리값); bwrdd.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < cofnod_COUNT && !sgript_gorffen;) {
            int gorffen_safle = 읽는자리; while (gorffen_safle < cofnod_COUNT && sgript_VALUE[중첩깊이 * 16384 + gorffen_safle] != 10) gorffen_safle++;
            int 유효길이 = gorffen_safle - 읽는자리; if (유효길이 > 0 && sgript_VALUE[중첩깊이 * 16384 + gorffen_safle - 1] == 13) 유효길이--;
            Gweithredu_gorchymyn(sgript_VALUE, 중첩깊이 * 16384 + 읽는자리, 유효길이, 중첩깊이); 읽는자리 = gorffen_safle + 1;
        }
        명령해석기.mesur = cyflwr_VALUE; sgript_gorffen = false; 깊이 = 중첩깊이 - 1;
    }
}
