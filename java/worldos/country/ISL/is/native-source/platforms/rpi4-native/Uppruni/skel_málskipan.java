// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 gagnvirkur skel 문법. 파이프는 순차 keyra_skipun, 환경은 같은 셸에서 공유한다. */
public final class skel_málskipan {
    static int[] Uppruni = new int[4 * 4096], 종류 = new int[4 * 128], Keyra_2 = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] 변수이름 = new int[16 * 32], 변수값 = new int[16 * 256], 이름길이 = new int[16], VALUE_lengd = new int[16];
    static int[] forskrift_VALUE = new int[4 * 16384];
    static int staða_VALUE_e10195a1, 깊이, 쓴수;
    static boolean 연결중, forskrift_ljúka, viðbót_villa;
    static boolean heiti_stafur(int stafkóði) { return stafkóði >= 'a' && stafkóði <= 'z' || stafkóði >= 'A' && stafkóði <= 'Z' || stafkóði == '_' || stafkóði >= 128; }
    static boolean 이름뒤(int stafkóði) { return heiti_stafur(stafkóði) || stafkóði >= '0' && stafkóði <= '9'; }
    static void Villa(String Texti) { bretti.입출력전환(0); 단말.Skrift("Skipun þátta_VALUE: "); 단말.Skrift(Texti); 단말.문자(10); staða_VALUE_e10195a1 = 2; }
    static int Lestur(int færsla_COUNT, int 중첩깊이) {
        int 현재자리 = 0, samtala_COUNT = 0, BASE_staða = 중첩깊이 * 4096, sértákn = 중첩깊이 * 128;
        while (현재자리 < færsla_COUNT) {
            while (현재자리 < færsla_COUNT && (Uppruni[BASE_staða + 현재자리] == 32 || Uppruni[BASE_staða + 현재자리] == 9)) 현재자리++;
            if (현재자리 == færsla_COUNT || Uppruni[BASE_staða + 현재자리] == '#') break;
            if (samtala_COUNT == 128) { Villa("낱말이 너무 많습니다"); return -1; }
            int Opna_staða = 현재자리, stafkóði = Uppruni[BASE_staða + 현재자리], 자료종류 = 0;
            if (stafkóði == ';') { 자료종류 = 1; 현재자리++; }
            else if (stafkóði == '&') { if (현재자리 + 1 >= færsla_COUNT || Uppruni[BASE_staða + 현재자리 + 1] != '&') { Villa("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } 자료종류 = 2; 현재자리 += 2; }
            else if (stafkóði == '|') { 현재자리++; 자료종류 = 현재자리 < færsla_COUNT && Uppruni[BASE_staða + 현재자리] == '|' ? 3 : 4; if (자료종류 == 3) 현재자리++; }
            else if (stafkóði == '>') { 현재자리++; 자료종류 = 현재자리 < færsla_COUNT && Uppruni[BASE_staða + 현재자리] == '>' ? 6 : 5; if (자료종류 == 6) 현재자리++; }
            else if (stafkóði == '<') { 자료종류 = 7; 현재자리++; }
            else {
                int Tilvitnun = 0;
                while (현재자리 < færsla_COUNT) {
                    stafkóði = Uppruni[BASE_staða + 현재자리];
                    if (stafkóði == '`' && Tilvitnun != 39 || stafkóði == '$' && Tilvitnun != 39 && 현재자리 + 1 < færsla_COUNT && Uppruni[BASE_staða + 현재자리 + 1] == '(') { Villa("Skipun NIÐURSTAÐA 치환은 지원하지 않습니다"); return -1; }
                    if (stafkóði == '\\' && Tilvitnun != 39) { if (++현재자리 == færsla_COUNT) { Villa("Lína 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } 현재자리++; continue; }
                    if (stafkóði == Tilvitnun) { Tilvitnun = 0; 현재자리++; continue; }
                    if (Tilvitnun == 0 && (stafkóði == 39 || stafkóði == 34)) { Tilvitnun = stafkóði; 현재자리++; continue; }
                    if (Tilvitnun == 0 && (stafkóði == 32 || stafkóði == 9 || stafkóði == ';' || stafkóði == '&' || stafkóði == '|' || stafkóði == '<' || stafkóði == '>')) break;
                    현재자리++;
                }
                if (Tilvitnun != 0) { Villa("따옴표가 닫히지 않았습니다"); return -1; }
                if (현재자리 < færsla_COUNT && (Uppruni[BASE_staða + 현재자리] == '>' || Uppruni[BASE_staða + 현재자리] == '<')) {
                    boolean 수치 = 현재자리 > Opna_staða;
                    for (int Loop_INDEX = Opna_staða; Loop_INDEX < 현재자리; Loop_INDEX++) if (Uppruni[BASE_staða + Loop_INDEX] < '0' || Uppruni[BASE_staða + Loop_INDEX] > '9') 수치 = false;
                    if (수치) { Villa("번호를 지정한 Skrá 서술자 I_Ú 전환은 지원하지 않습니다"); return -1; }
                }
            }
            종류[sértákn + samtala_COUNT] = 자료종류; Keyra_2[sértákn + samtala_COUNT] = Opna_staða; 끝[sértákn + samtala_COUNT] = 현재자리; samtala_COUNT++;
        }
        boolean 낱말 = false;
        for (int Loop_INDEX = 0; Loop_INDEX < samtala_COUNT; Loop_INDEX++) {
            int 임시값 = 종류[sértákn + Loop_INDEX];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++Loop_INDEX == samtala_COUNT || 종류[sértákn + Loop_INDEX] != 0) { Villa("I_Ú 전환에 Skrá 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || Loop_INDEX == samtala_COUNT - 1 && 임시값 != 1) { Villa("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (samtala_COUNT > 0 && !낱말 && 종류[sértákn + samtala_COUNT - 1] != 1) { Villa("명령이 빠졌습니다"); return -1; }
        return samtala_COUNT;
    }
    static boolean 구간말(int[] gögn_ARRAY, int staðbundið_Opna, int færsla_COUNT, String stafur_staða) {
        if (færsla_COUNT != stafur_staða.length()) return false; for (int Loop_INDEX = 0; Loop_INDEX < færsla_COUNT; Loop_INDEX++) if (gögn_ARRAY[staðbundið_Opna + Loop_INDEX] != stafur_staða.charAt(Loop_INDEX)) return false; return true;
    }
    static void 넣기(int bæti_gögn) {
        if (쓴수 >= 명령해석기.tákn_VALUE_eb540501.length) { if (!viðbót_villa) Villa("변수를 펼친 명령이 너무 깁니다"); viðbót_villa = true; return; }
        명령해석기.tákn_VALUE_eb540501[쓴수++] = bæti_gögn;
    }
    static void 변수(int[] gögn_ARRAY, int Opna_staða, int færsla_COUNT) {
        if (구간말(gögn_ARRAY, Opna_staða, færsla_COUNT, "PWD")) { 넣기('/'); for (int Loop_INDEX = 0; Loop_INDEX < Minni_Skrár.현재길이; Loop_INDEX++) 넣기(Minni_Skrár.현재[Loop_INDEX]); return; }
        if (구간말(gögn_ARRAY, Opna_staða, færsla_COUNT, "HOME")) { 넣기('/'); return; }
        if (구간말(gögn_ARRAY, Opna_staða, færsla_COUNT, "?")) {
            int gögn_VALUE = staða_VALUE_e10195a1, tölustafur = 100; boolean 시작여부 = false;
            while (tölustafur > 0) { int 뒷값 = gögn_VALUE / tölustafur; if (뒷값 != 0 || 시작여부 || tölustafur == 1) { 넣기('0' + 뒷값); 시작여부 = true; } gögn_VALUE %= tölustafur; tölustafur /= 10; } return;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] == færsla_COUNT) {
            boolean MATCH = true; for (int innri_samtenging_staða = 0; innri_samtenging_staða < færsla_COUNT; innri_samtenging_staða++) if (변수이름[Loop_INDEX * 32 + innri_samtenging_staða] != gögn_ARRAY[Opna_staða + innri_samtenging_staða]) MATCH = false;
            if (MATCH) { for (int innri_samtenging_staða = 0; innri_samtenging_staða < VALUE_lengd[Loop_INDEX]; innri_samtenging_staða++) 넣기(변수값[Loop_INDEX * 256 + innri_samtenging_staða]); return; }
        }
    }
    static boolean Word_VALUE(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = Keyra_2[중첩깊이 * 128 + 낱말번호], ljúka_staða = 끝[중첩깊이 * 128 + 낱말번호], BASE_staða = 중첩깊이 * 4096, Tilvitnun = 0;
        if (읽는자리 < ljúka_staða && Uppruni[BASE_staða + 읽는자리] == '~' && (읽는자리 + 1 == ljúka_staða || Uppruni[BASE_staða + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < ljúka_staða) {
            int stafkóði = Uppruni[BASE_staða + 읽는자리++];
            if (stafkóði == Tilvitnun) { Tilvitnun = 0; continue; }
            if (Tilvitnun == 0 && (stafkóði == 39 || stafkóði == 34)) { Tilvitnun = stafkóði; continue; }
            if (stafkóði == '\\' && Tilvitnun != 39) { int Áfram_staða = Uppruni[BASE_staða + 읽는자리++]; if (Tilvitnun == 34 && Áfram_staða != '$' && Áfram_staða != '"' && Áfram_staða != '\\') 넣기('\\'); 넣기(Áfram_staða); continue; }
            if (stafkóði == '$' && Tilvitnun != 39 && 읽는자리 < ljúka_staða) {
                boolean 중괄호자리 = Uppruni[BASE_staða + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < ljúka_staða && Uppruni[BASE_staða + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < ljúka_staða && 이름뒤(Uppruni[BASE_staða + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == ljúka_staða || Uppruni[BASE_staða + 읽는자리] != '}')) { Villa("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                변수(Uppruni, BASE_staða + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(stafkóði);
        }
        return !viðbót_villa;
    }
    static int 환경설정(int frumbreyta_INDEX, boolean fjarlægja) {
        int staðbundið_Opna = 명령해석기.시작점[frumbreyta_INDEX], ljúka_staða = staðbundið_Opna + 명령해석기.lengd_VALUE[frumbreyta_INDEX], 같음자리 = staðbundið_Opna;
        while (같음자리 < ljúka_staða && 명령해석기.tákn_VALUE_eb540501[같음자리] != '=') 같음자리++;
        int færsla_COUNT = 같음자리 - staðbundið_Opna;
        if (færsla_COUNT < 1 || færsla_COUNT > 31 || !heiti_stafur(명령해석기.tákn_VALUE_eb540501[staðbundið_Opna]) || !fjarlægja && 같음자리 == ljúka_staða || ljúka_staða - 같음자리 - 1 > 255) return 2;
        for (int Loop_INDEX = staðbundið_Opna; Loop_INDEX < 같음자리; Loop_INDEX++) if (!이름뒤(명령해석기.tákn_VALUE_eb540501[Loop_INDEX])) return 2;
        if (구간말(명령해석기.tákn_VALUE_eb540501, staðbundið_Opna, færsla_COUNT, "PWD") || 구간말(명령해석기.tákn_VALUE_eb540501, staðbundið_Opna, færsla_COUNT, "HOME")) return 2;
        int 찾은여부 = -1, upplýsingatækni_autt_staða = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] == 0) upplýsingatækni_autt_staða = Loop_INDEX;
            if (이름길이[Loop_INDEX] != færsla_COUNT) continue;
            boolean MATCH = true; for (int innri_samtenging_staða = 0; innri_samtenging_staða < færsla_COUNT; innri_samtenging_staða++) if (변수이름[Loop_INDEX * 32 + innri_samtenging_staða] != 명령해석기.tákn_VALUE_eb540501[staðbundið_Opna + innri_samtenging_staða]) MATCH = false;
            if (MATCH) 찾은여부 = Loop_INDEX;
        }
        if (fjarlægja) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = upplýsingatækni_autt_staða; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = færsla_COUNT; VALUE_lengd[찾은여부] = ljúka_staða - 같음자리 - 1;
        for (int Loop_INDEX = 0; Loop_INDEX < færsla_COUNT; Loop_INDEX++) 변수이름[찾은여부 * 32 + Loop_INDEX] = 명령해석기.tákn_VALUE_eb540501[staðbundið_Opna + Loop_INDEX];
        for (int Loop_INDEX = 같음자리 + 1; Loop_INDEX < ljúka_staða; Loop_INDEX++) 변수값[찾은여부 * 256 + Loop_INDEX - 같음자리 - 1] = 명령해석기.tákn_VALUE_eb540501[Loop_INDEX];
        return 0;
    }
    static void 환경보기() {
        단말.Skrift("HOME=/\nPWD="); Minni_Skrár.현재쓰기(); 단말.문자(10);
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] > 0) {
            for (int innri_samtenging_staða = 0; innri_samtenging_staða < 이름길이[Loop_INDEX]; innri_samtenging_staða++) bretti.직렬쓰기(변수이름[Loop_INDEX * 32 + innri_samtenging_staða]); 단말.문자('=');
            for (int innri_samtenging_staða = 0; innri_samtenging_staða < VALUE_lengd[Loop_INDEX]; innri_samtenging_staða++) bretti.직렬쓰기(변수값[Loop_INDEX * 256 + innri_samtenging_staða]); 단말.문자(10);
        }
    }
    static void keyra_skipun(int[] gögn_ARRAY, int 시작변위, int færsla_COUNT, int 중첩깊이) {
        if (중첩깊이 >= 4 || færsla_COUNT > 4096) { Villa("Skipun 파일의 földun_VALUE 또는 Lína lengd_VALUE 제한을 넘었습니다"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < færsla_COUNT; Loop_INDEX++) Uppruni[중첩깊이 * 4096 + Loop_INDEX] = gögn_ARRAY[시작변위 + Loop_INDEX];
        int samtala_COUNT = Lestur(færsla_COUNT, 중첩깊이); if (samtala_COUNT < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < samtala_COUNT) {
            int Hópur_ljúka = 읽는자리;
            while (Hópur_ljúka < samtala_COUNT && (종류[중첩깊이 * 128 + Hópur_ljúka] == 0 || 종류[중첩깊이 * 128 + Hópur_ljúka] >= 4)) Hópur_ljúka++;
            boolean keyra = 조건성립 == 1 || 조건성립 == 2 && staða_VALUE_e10195a1 == 0 || 조건성립 == 3 && staða_VALUE_e10195a1 != 0;
            if (keyra) {
                boolean 이전자리 = false;
                while (읽는자리 < Hópur_ljúka) {
                    int Áfram_staða = 읽는자리; while (Áfram_staða < Hópur_ljúka && 종류[중첩깊이 * 128 + Áfram_staða] != 4) Áfram_staða++;
                    boolean TENGJA_Stream = Áfram_staða < Hópur_ljúka; int 입력쪽 = -1, úttak_síða = -1, 출력방식 = 0;
                    명령해석기.tákn_COUNT = 0; 쓴수 = 0; viðbót_villa = false;
                    for (int Loop_INDEX = 읽는자리; Loop_INDEX < Áfram_staða; Loop_INDEX++) {
                        int 자료종류 = 종류[중첩깊이 * 128 + Loop_INDEX];
                        if (자료종류 >= 5) { if (자료종류 == 7) { if (입력쪽 >= 0) { Villa("입력 전환이 겹쳤습니다"); return; } 입력쪽 = ++Loop_INDEX; } else { if (úttak_síða >= 0) { Villa("úttak 전환이 겹쳤습니다"); return; } úttak_síða = ++Loop_INDEX; 출력방식 = 자료종류; } continue; }
                        if (명령해석기.tákn_COUNT == 32) { Villa("인수가 너무 많습니다"); return; }
                        int frumbreyta_INDEX = 명령해석기.tákn_COUNT++; 명령해석기.시작점[frumbreyta_INDEX] = 쓴수;
                        if (!Word_VALUE(Loop_INDEX, 중첩깊이)) return;
                        명령해석기.lengd_VALUE[frumbreyta_INDEX] = 쓴수 - 명령해석기.시작점[frumbreyta_INDEX];
                    }
                    연결중 = 이전자리 || TENGJA_Stream || 입력쪽 >= 0 || úttak_síða >= 0;
                    if (연결중 && (명령해석기.같음(0, "vi") || 명령해석기.같음(0, "edit") || 명령해석기.같음(0, "load") || 명령해석기.같음(0, "gui") || 명령해석기.같음(0, "terminal") || 명령해석기.같음(0, "sh") || 명령해석기.같음(0, "source"))) { Villa("gagnvirkur 명령과 Skipun 파일은 I_Ú 전환이나 Stream_VALUE 연결에 쓸 númer 없습니다"); return; }
                    셸입출력.Keyra_2(이전자리, TENGJA_Stream);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int færsla_staða = 입출력바꿈 == 0 ? 입력쪽 : úttak_síða; if (færsla_staða < 0) continue;
                        int Opna_staða = 쓴수; if (!Word_VALUE(færsla_staða, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = Minni_Skrár.slóð_Opna(쓴수 - Opna_staða);
                        for (int innri_samtenging_staða = Opna_staða; 처리값 >= 0 && innri_samtenging_staða < 쓴수; innri_samtenging_staða++) 처리값 = Minni_Skrár.slóð_bæti(innri_samtenging_staða - Opna_staða, 명령해석기.tákn_VALUE_eb540501[innri_samtenging_staða]);
                        if (처리값 >= 0) 처리값 = Minni_Skrár.Opna(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); 명령해석기.Villa(처리값); staða_VALUE_e10195a1 = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.입력파일 = 처리값; else 셸입출력.úttaksskrá = 처리값;
                    }
                    셸입출력.leyfa_gagnvirkur = 중첩깊이 == 0 && 읽는자리 == 0 && Áfram_staða == samtala_COUNT;
                    깊이 = 중첩깊이; 명령해석기.NIÐURSTAÐA = 0; bretti.입출력전환(1);
                    명령해석기.Skipun();
                    bretti.Skjáhermir(3);
                    int 반환값 = 명령해석기.NIÐURSTAÐA, Stream_villa = 셸입출력.bilun_VALUE;
                    셸입출력.끝(); 연결중 = false;
                    staða_VALUE_e10195a1 = Stream_villa < 0 ? 1 : 반환값;
                    if (Stream_villa < 0) { 명령해석기.Villa(Stream_villa); return; }
                    if (forskrift_ljúka || 반환값 == -1005) return;
                    이전자리 = true; 읽는자리 = Áfram_staða + 1;
                }
            }
            if (Hópur_ljúka < samtala_COUNT) 조건성립 = 종류[중첩깊이 * 128 + Hópur_ljúka];
            읽는자리 = Hópur_ljúka + 1;
        }
    }
    static void keyra_skrá() {
        if (명령해석기.tákn_COUNT != 2 || 깊이 >= 3) { 명령해석기.NIÐURSTAÐA = 2; 단말.Skrift("사용법: sh Skrá (földun_VALUE 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = 명령해석기.SLÓÐ(1); if (처리값 >= 0) 처리값 = Minni_Skrár.Opna(0);
        if (처리값 < 0) { 명령해석기.Villa(처리값); return; }
        int færsla_COUNT = 0, bæti_gögn;
        while ((bæti_gögn = Minni_Skrár.Lestur(처리값)) != 256 && bæti_gögn >= 0 && færsla_COUNT < 16384) forskrift_VALUE[중첩깊이 * 16384 + færsla_COUNT++] = bæti_gögn;
        Minni_Skrár.Loka(처리값); bretti.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < færsla_COUNT && !forskrift_ljúka;) {
            int ljúka_staða = 읽는자리; while (ljúka_staða < færsla_COUNT && forskrift_VALUE[중첩깊이 * 16384 + ljúka_staða] != 10) ljúka_staða++;
            int 유효길이 = ljúka_staða - 읽는자리; if (유효길이 > 0 && forskrift_VALUE[중첩깊이 * 16384 + ljúka_staða - 1] == 13) 유효길이--;
            keyra_skipun(forskrift_VALUE, 중첩깊이 * 16384 + 읽는자리, 유효길이, 중첩깊이); 읽는자리 = ljúka_staða + 1;
        }
        명령해석기.NIÐURSTAÐA = staða_VALUE_e10195a1; forskrift_ljúka = false; 깊이 = 중첩깊이 - 1;
    }
}
