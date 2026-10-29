// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 eadar_ghnìomhach slige 문법. 파이프는 순차 gnìomhaich_àithne, 환경은 같은 셸에서 공유한다. */
public final class 셸문법 {
    static int[] tùs = new int[4 * 4096], 종류 = new int[4 * 128], ruith = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] 변수이름 = new int[16 * 32], 변수값 = new int[16 * 256], 이름길이 = new int[16], VALUE_faid = new int[16];
    static int[] sgriobt_VALUE = new int[4 * 16384];
    static int cor_VALUE, 깊이, 쓴수;
    static boolean 연결중, sgriobt_crìochnaich, leudachan_mearachd;
    static boolean ainm_caractar(int còd_a_charactair) { return còd_a_charactair >= 'a' && còd_a_charactair <= 'z' || còd_a_charactair >= 'A' && còd_a_charactair <= 'Z' || còd_a_charactair == '_' || còd_a_charactair >= 128; }
    static boolean 이름뒤(int còd_a_charactair) { return ainm_caractar(còd_a_charactair) || còd_a_charactair >= '0' && còd_a_charactair <= '9'; }
    static void Mearachd(String SMS) { bòrd.입출력전환(0); 단말.sgrìobh("àithne 해석: "); 단말.sgrìobh(SMS); 단말.문자(10); cor_VALUE = 2; }
    static int 읽기(int cur_a_steach_COUNT, int 중첩깊이) {
        int 현재자리 = 0, 총수 = 0, BASE_suidhich = 중첩깊이 * 4096, caractar_sònraichte = 중첩깊이 * 128;
        while (현재자리 < cur_a_steach_COUNT) {
            while (현재자리 < cur_a_steach_COUNT && (tùs[BASE_suidhich + 현재자리] == 32 || tùs[BASE_suidhich + 현재자리] == 9)) 현재자리++;
            if (현재자리 == cur_a_steach_COUNT || tùs[BASE_suidhich + 현재자리] == '#') break;
            if (총수 == 128) { Mearachd("낱말이 너무 많습니다"); return -1; }
            int Start_suidhich = 현재자리, còd_a_charactair = tùs[BASE_suidhich + 현재자리], 자료종류 = 0;
            if (còd_a_charactair == ';') { 자료종류 = 1; 현재자리++; }
            else if (còd_a_charactair == '&') { if (현재자리 + 1 >= cur_a_steach_COUNT || tùs[BASE_suidhich + 현재자리 + 1] != '&') { Mearachd("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } 자료종류 = 2; 현재자리 += 2; }
            else if (còd_a_charactair == '|') { 현재자리++; 자료종류 = 현재자리 < cur_a_steach_COUNT && tùs[BASE_suidhich + 현재자리] == '|' ? 3 : 4; if (자료종류 == 3) 현재자리++; }
            else if (còd_a_charactair == '>') { 현재자리++; 자료종류 = 현재자리 < cur_a_steach_COUNT && tùs[BASE_suidhich + 현재자리] == '>' ? 6 : 5; if (자료종류 == 6) 현재자리++; }
            else if (còd_a_charactair == '<') { 자료종류 = 7; 현재자리++; }
            else {
                int comharran_labhairt = 0;
                while (현재자리 < cur_a_steach_COUNT) {
                    còd_a_charactair = tùs[BASE_suidhich + 현재자리];
                    if (còd_a_charactair == '`' && comharran_labhairt != 39 || còd_a_charactair == '$' && comharran_labhairt != 39 && 현재자리 + 1 < cur_a_steach_COUNT && tùs[BASE_suidhich + 현재자리 + 1] == '(') { Mearachd("àithne tomhas 치환은 지원하지 않습니다"); return -1; }
                    if (còd_a_charactair == '\\' && comharran_labhairt != 39) { if (++현재자리 == cur_a_steach_COUNT) { Mearachd("loidhne 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } 현재자리++; continue; }
                    if (còd_a_charactair == comharran_labhairt) { comharran_labhairt = 0; 현재자리++; continue; }
                    if (comharran_labhairt == 0 && (còd_a_charactair == 39 || còd_a_charactair == 34)) { comharran_labhairt = còd_a_charactair; 현재자리++; continue; }
                    if (comharran_labhairt == 0 && (còd_a_charactair == 32 || còd_a_charactair == 9 || còd_a_charactair == ';' || còd_a_charactair == '&' || còd_a_charactair == '|' || còd_a_charactair == '<' || còd_a_charactair == '>')) break;
                    현재자리++;
                }
                if (comharran_labhairt != 0) { Mearachd("따옴표가 닫히지 않았습니다"); return -1; }
                if (현재자리 < cur_a_steach_COUNT && (tùs[BASE_suidhich + 현재자리] == '>' || tùs[BASE_suidhich + 현재자리] == '<')) {
                    boolean 수치 = 현재자리 > Start_suidhich;
                    for (int lùb_INDEX = Start_suidhich; lùb_INDEX < 현재자리; lùb_INDEX++) if (tùs[BASE_suidhich + lùb_INDEX] < '0' || tùs[BASE_suidhich + lùb_INDEX] > '9') 수치 = false;
                    if (수치) { Mearachd("번호를 지정한 faidhle 서술자 I_O 전환은 지원하지 않습니다"); return -1; }
                }
            }
            종류[caractar_sònraichte + 총수] = 자료종류; ruith[caractar_sònraichte + 총수] = Start_suidhich; 끝[caractar_sònraichte + 총수] = 현재자리; 총수++;
        }
        boolean 낱말 = false;
        for (int lùb_INDEX = 0; lùb_INDEX < 총수; lùb_INDEX++) {
            int 임시값 = 종류[caractar_sònraichte + lùb_INDEX];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++lùb_INDEX == 총수 || 종류[caractar_sònraichte + lùb_INDEX] != 0) { Mearachd("I_O 전환에 faidhle 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || lùb_INDEX == 총수 - 1 && 임시값 != 1) { Mearachd("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (총수 > 0 && !낱말 && 종류[caractar_sònraichte + 총수 - 1] != 1) { Mearachd("명령이 빠졌습니다"); return -1; }
        return 총수;
    }
    static boolean 구간말(int[] dàta_ARRAY, int ionadail_Start, int cur_a_steach_COUNT, String caractar_suidhich) {
        if (cur_a_steach_COUNT != caractar_suidhich.length()) return false; for (int lùb_INDEX = 0; lùb_INDEX < cur_a_steach_COUNT; lùb_INDEX++) if (dàta_ARRAY[ionadail_Start + lùb_INDEX] != caractar_suidhich.charAt(lùb_INDEX)) return false; return true;
    }
    static void 넣기(int baidht_dàta) {
        if (쓴수 >= 명령해석기.tòcan_VALUE.length) { if (!leudachan_mearachd) Mearachd("변수를 펼친 명령이 너무 깁니다"); leudachan_mearachd = true; return; }
        명령해석기.tòcan_VALUE[쓴수++] = baidht_dàta;
    }
    static void 변수(int[] dàta_ARRAY, int Start_suidhich, int cur_a_steach_COUNT) {
        if (구간말(dàta_ARRAY, Start_suidhich, cur_a_steach_COUNT, "PWD")) { 넣기('/'); for (int lùb_INDEX = 0; lùb_INDEX < cuimhne_faidhlichean.현재길이; lùb_INDEX++) 넣기(cuimhne_faidhlichean.현재[lùb_INDEX]); return; }
        if (구간말(dàta_ARRAY, Start_suidhich, cur_a_steach_COUNT, "HOME")) { 넣기('/'); return; }
        if (구간말(dàta_ARRAY, Start_suidhich, cur_a_steach_COUNT, "?")) {
            int dàta_VALUE = cor_VALUE, figear = 100; boolean 시작여부 = false;
            while (figear > 0) { int 뒷값 = dàta_VALUE / figear; if (뒷값 != 0 || 시작여부 || figear == 1) { 넣기('0' + 뒷값); 시작여부 = true; } dàta_VALUE %= figear; figear /= 10; } return;
        }
        for (int lùb_INDEX = 0; lùb_INDEX < 16; lùb_INDEX++) if (이름길이[lùb_INDEX] == cur_a_steach_COUNT) {
            boolean MATCH = true; for (int Inner_Join_suidhich = 0; Inner_Join_suidhich < cur_a_steach_COUNT; Inner_Join_suidhich++) if (변수이름[lùb_INDEX * 32 + Inner_Join_suidhich] != dàta_ARRAY[Start_suidhich + Inner_Join_suidhich]) MATCH = false;
            if (MATCH) { for (int Inner_Join_suidhich = 0; Inner_Join_suidhich < VALUE_faid[lùb_INDEX]; Inner_Join_suidhich++) 넣기(변수값[lùb_INDEX * 256 + Inner_Join_suidhich]); return; }
        }
    }
    static boolean Word_VALUE(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = ruith[중첩깊이 * 128 + 낱말번호], crìochnaich_suidhich = 끝[중첩깊이 * 128 + 낱말번호], BASE_suidhich = 중첩깊이 * 4096, comharran_labhairt = 0;
        if (읽는자리 < crìochnaich_suidhich && tùs[BASE_suidhich + 읽는자리] == '~' && (읽는자리 + 1 == crìochnaich_suidhich || tùs[BASE_suidhich + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < crìochnaich_suidhich) {
            int còd_a_charactair = tùs[BASE_suidhich + 읽는자리++];
            if (còd_a_charactair == comharran_labhairt) { comharran_labhairt = 0; continue; }
            if (comharran_labhairt == 0 && (còd_a_charactair == 39 || còd_a_charactair == 34)) { comharran_labhairt = còd_a_charactair; continue; }
            if (còd_a_charactair == '\\' && comharran_labhairt != 39) { int air_adhart_suidhich = tùs[BASE_suidhich + 읽는자리++]; if (comharran_labhairt == 34 && air_adhart_suidhich != '$' && air_adhart_suidhich != '"' && air_adhart_suidhich != '\\') 넣기('\\'); 넣기(air_adhart_suidhich); continue; }
            if (còd_a_charactair == '$' && comharran_labhairt != 39 && 읽는자리 < crìochnaich_suidhich) {
                boolean 중괄호자리 = tùs[BASE_suidhich + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < crìochnaich_suidhich && tùs[BASE_suidhich + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < crìochnaich_suidhich && 이름뒤(tùs[BASE_suidhich + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == crìochnaich_suidhich || tùs[BASE_suidhich + 읽는자리] != '}')) { Mearachd("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                변수(tùs, BASE_suidhich + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(còd_a_charactair);
        }
        return !leudachan_mearachd;
    }
    static int 환경설정(int argamaid_INDEX, boolean thoir_air_falbh) {
        int ionadail_Start = 명령해석기.시작점[argamaid_INDEX], crìochnaich_suidhich = ionadail_Start + 명령해석기.faid_VALUE[argamaid_INDEX], 같음자리 = ionadail_Start;
        while (같음자리 < crìochnaich_suidhich && 명령해석기.tòcan_VALUE[같음자리] != '=') 같음자리++;
        int cur_a_steach_COUNT = 같음자리 - ionadail_Start;
        if (cur_a_steach_COUNT < 1 || cur_a_steach_COUNT > 31 || !ainm_caractar(명령해석기.tòcan_VALUE[ionadail_Start]) || !thoir_air_falbh && 같음자리 == crìochnaich_suidhich || crìochnaich_suidhich - 같음자리 - 1 > 255) return 2;
        for (int lùb_INDEX = ionadail_Start; lùb_INDEX < 같음자리; lùb_INDEX++) if (!이름뒤(명령해석기.tòcan_VALUE[lùb_INDEX])) return 2;
        if (구간말(명령해석기.tòcan_VALUE, ionadail_Start, cur_a_steach_COUNT, "PWD") || 구간말(명령해석기.tòcan_VALUE, ionadail_Start, cur_a_steach_COUNT, "HOME")) return 2;
        int 찾은여부 = -1, 빈여부 = -1;
        for (int lùb_INDEX = 0; lùb_INDEX < 16; lùb_INDEX++) {
            if (이름길이[lùb_INDEX] == 0) 빈여부 = lùb_INDEX;
            if (이름길이[lùb_INDEX] != cur_a_steach_COUNT) continue;
            boolean MATCH = true; for (int Inner_Join_suidhich = 0; Inner_Join_suidhich < cur_a_steach_COUNT; Inner_Join_suidhich++) if (변수이름[lùb_INDEX * 32 + Inner_Join_suidhich] != 명령해석기.tòcan_VALUE[ionadail_Start + Inner_Join_suidhich]) MATCH = false;
            if (MATCH) 찾은여부 = lùb_INDEX;
        }
        if (thoir_air_falbh) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = 빈여부; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = cur_a_steach_COUNT; VALUE_faid[찾은여부] = crìochnaich_suidhich - 같음자리 - 1;
        for (int lùb_INDEX = 0; lùb_INDEX < cur_a_steach_COUNT; lùb_INDEX++) 변수이름[찾은여부 * 32 + lùb_INDEX] = 명령해석기.tòcan_VALUE[ionadail_Start + lùb_INDEX];
        for (int lùb_INDEX = 같음자리 + 1; lùb_INDEX < crìochnaich_suidhich; lùb_INDEX++) 변수값[찾은여부 * 256 + lùb_INDEX - 같음자리 - 1] = 명령해석기.tòcan_VALUE[lùb_INDEX];
        return 0;
    }
    static void 환경보기() {
        단말.sgrìobh("HOME=/\nPWD="); cuimhne_faidhlichean.현재쓰기(); 단말.문자(10);
        for (int lùb_INDEX = 0; lùb_INDEX < 16; lùb_INDEX++) if (이름길이[lùb_INDEX] > 0) {
            for (int Inner_Join_suidhich = 0; Inner_Join_suidhich < 이름길이[lùb_INDEX]; Inner_Join_suidhich++) bòrd.직렬쓰기(변수이름[lùb_INDEX * 32 + Inner_Join_suidhich]); 단말.문자('=');
            for (int Inner_Join_suidhich = 0; Inner_Join_suidhich < VALUE_faid[lùb_INDEX]; Inner_Join_suidhich++) bòrd.직렬쓰기(변수값[lùb_INDEX * 256 + Inner_Join_suidhich]); 단말.문자(10);
        }
    }
    static void gnìomhaich_àithne(int[] dàta_ARRAY, int 시작변위, int cur_a_steach_COUNT, int 중첩깊이) {
        if (중첩깊이 >= 4 || cur_a_steach_COUNT > 4096) { Mearachd("àithne 파일의 중첩 또는 loidhne faid_VALUE 제한을 넘었습니다"); return; }
        for (int lùb_INDEX = 0; lùb_INDEX < cur_a_steach_COUNT; lùb_INDEX++) tùs[중첩깊이 * 4096 + lùb_INDEX] = dàta_ARRAY[시작변위 + lùb_INDEX];
        int 총수 = 읽기(cur_a_steach_COUNT, 중첩깊이); if (총수 < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < 총수) {
            int buidheann_crìochnaich = 읽는자리;
            while (buidheann_crìochnaich < 총수 && (종류[중첩깊이 * 128 + buidheann_crìochnaich] == 0 || 종류[중첩깊이 * 128 + buidheann_crìochnaich] >= 4)) buidheann_crìochnaich++;
            boolean gnìomhaich = 조건성립 == 1 || 조건성립 == 2 && cor_VALUE == 0 || 조건성립 == 3 && cor_VALUE != 0;
            if (gnìomhaich) {
                boolean 이전자리 = false;
                while (읽는자리 < buidheann_crìochnaich) {
                    int air_adhart_suidhich = 읽는자리; while (air_adhart_suidhich < buidheann_crìochnaich && 종류[중첩깊이 * 128 + air_adhart_suidhich] != 4) air_adhart_suidhich++;
                    boolean CONNECT_sruth = air_adhart_suidhich < buidheann_crìochnaich; int 입력쪽 = -1, 출력쪽 = -1, 출력방식 = 0;
                    명령해석기.tòcan_COUNT = 0; 쓴수 = 0; leudachan_mearachd = false;
                    for (int lùb_INDEX = 읽는자리; lùb_INDEX < air_adhart_suidhich; lùb_INDEX++) {
                        int 자료종류 = 종류[중첩깊이 * 128 + lùb_INDEX];
                        if (자료종류 >= 5) { if (자료종류 == 7) { if (입력쪽 >= 0) { Mearachd("입력 전환이 겹쳤습니다"); return; } 입력쪽 = ++lùb_INDEX; } else { if (출력쪽 >= 0) { Mearachd("출력 전환이 겹쳤습니다"); return; } 출력쪽 = ++lùb_INDEX; 출력방식 = 자료종류; } continue; }
                        if (명령해석기.tòcan_COUNT == 32) { Mearachd("인수가 너무 많습니다"); return; }
                        int argamaid_INDEX = 명령해석기.tòcan_COUNT++; 명령해석기.시작점[argamaid_INDEX] = 쓴수;
                        if (!Word_VALUE(lùb_INDEX, 중첩깊이)) return;
                        명령해석기.faid_VALUE[argamaid_INDEX] = 쓴수 - 명령해석기.시작점[argamaid_INDEX];
                    }
                    연결중 = 이전자리 || CONNECT_sruth || 입력쪽 >= 0 || 출력쪽 >= 0;
                    if (연결중 && (명령해석기.같음(0, "vi") || 명령해석기.같음(0, "edit") || 명령해석기.같음(0, "load") || 명령해석기.같음(0, "gui") || 명령해석기.같음(0, "terminal") || 명령해석기.같음(0, "sh") || 명령해석기.같음(0, "source"))) { Mearachd("eadar_ghnìomhach 명령과 àithne 파일은 I_O 전환이나 sruth_VALUE 연결에 쓸 수 없습니다"); return; }
                    셸입출력.ruith(이전자리, CONNECT_sruth);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int cur_a_steach_suidhich = 입출력바꿈 == 0 ? 입력쪽 : 출력쪽; if (cur_a_steach_suidhich < 0) continue;
                        int Start_suidhich = 쓴수; if (!Word_VALUE(cur_a_steach_suidhich, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = cuimhne_faidhlichean.slighe_Start(쓴수 - Start_suidhich);
                        for (int Inner_Join_suidhich = Start_suidhich; 처리값 >= 0 && Inner_Join_suidhich < 쓴수; Inner_Join_suidhich++) 처리값 = cuimhne_faidhlichean.slighe_baidht(Inner_Join_suidhich - Start_suidhich, 명령해석기.tòcan_VALUE[Inner_Join_suidhich]);
                        if (처리값 >= 0) 처리값 = cuimhne_faidhlichean.fosgail(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); 명령해석기.Mearachd(처리값); cor_VALUE = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.입력파일 = 처리값; else 셸입출력.faidhle_às_chuir = 처리값;
                    }
                    셸입출력.Ceadaich_eadar_ghnìomhach = 중첩깊이 == 0 && 읽는자리 == 0 && air_adhart_suidhich == 총수;
                    깊이 = 중첩깊이; 명령해석기.tomhas = 0; bòrd.입출력전환(1);
                    명령해석기.àithne();
                    bòrd.tèirmineal(3);
                    int 반환값 = 명령해석기.tomhas, sruth_mearachd = 셸입출력.fàilligeadh_VALUE;
                    셸입출력.끝(); 연결중 = false;
                    cor_VALUE = sruth_mearachd < 0 ? 1 : 반환값;
                    if (sruth_mearachd < 0) { 명령해석기.Mearachd(sruth_mearachd); return; }
                    if (sgriobt_crìochnaich || 반환값 == -1005) return;
                    이전자리 = true; 읽는자리 = air_adhart_suidhich + 1;
                }
            }
            if (buidheann_crìochnaich < 총수) 조건성립 = 종류[중첩깊이 * 128 + buidheann_crìochnaich];
            읽는자리 = buidheann_crìochnaich + 1;
        }
    }
    static void gnìomhaich_faidhle() {
        if (명령해석기.tòcan_COUNT != 2 || 깊이 >= 3) { 명령해석기.tomhas = 2; 단말.sgrìobh("사용법: sh faidhle (중첩 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = 명령해석기.Slighe(1); if (처리값 >= 0) 처리값 = cuimhne_faidhlichean.fosgail(0);
        if (처리값 < 0) { 명령해석기.Mearachd(처리값); return; }
        int cur_a_steach_COUNT = 0, baidht_dàta;
        while ((baidht_dàta = cuimhne_faidhlichean.읽기(처리값)) != 256 && baidht_dàta >= 0 && cur_a_steach_COUNT < 16384) sgriobt_VALUE[중첩깊이 * 16384 + cur_a_steach_COUNT++] = baidht_dàta;
        cuimhne_faidhlichean.dùin(처리값); bòrd.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < cur_a_steach_COUNT && !sgriobt_crìochnaich;) {
            int crìochnaich_suidhich = 읽는자리; while (crìochnaich_suidhich < cur_a_steach_COUNT && sgriobt_VALUE[중첩깊이 * 16384 + crìochnaich_suidhich] != 10) crìochnaich_suidhich++;
            int 유효길이 = crìochnaich_suidhich - 읽는자리; if (유효길이 > 0 && sgriobt_VALUE[중첩깊이 * 16384 + crìochnaich_suidhich - 1] == 13) 유효길이--;
            gnìomhaich_àithne(sgriobt_VALUE, 중첩깊이 * 16384 + 읽는자리, 유효길이, 중첩깊이); 읽는자리 = crìochnaich_suidhich + 1;
        }
        명령해석기.tomhas = cor_VALUE; sgriobt_crìochnaich = false; 깊이 = 중첩깊이 - 1;
    }
}
