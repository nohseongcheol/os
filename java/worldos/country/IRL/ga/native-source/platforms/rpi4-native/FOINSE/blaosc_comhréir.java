// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 idirghníomhach blaosc 문법. 파이프는 순차 Rith_ordú, 환경은 같은 셸에서 공유한다. */
public final class blaosc_comhréir {
    static int[] FOINSE = new int[4 * 4096], 종류 = new int[4 * 128], Rith_2 = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] 변수이름 = new int[16 * 32], 변수값 = new int[16 * 256], 이름길이 = new int[16], VALUE_fad = new int[16];
    static int[] script_VALUE = new int[4 * 16384];
    static int staid_VALUE, 깊이, 쓴수;
    static boolean 연결중, script_cuir_deireadh_le, breisiú_earráid;
    static boolean ainm_carachtar(int pointe_cóid) { return pointe_cóid >= 'a' && pointe_cóid <= 'z' || pointe_cóid >= 'A' && pointe_cóid <= 'Z' || pointe_cóid == '_' || pointe_cóid >= 128; }
    static boolean 이름뒤(int pointe_cóid) { return ainm_carachtar(pointe_cóid) || pointe_cóid >= '0' && pointe_cóid <= '9'; }
    static void ERREÁID(String Téacs) { clár.입출력전환(0); 단말.Scríobh("Ordú parsáil_VALUE: "); 단말.Scríobh(Téacs); 단말.문자(10); staid_VALUE = 2; }
    static int Léigh(int iontráil_COUNT, int 중첩깊이) {
        int 현재자리 = 0, 총수 = 0, BASE_suíomh = 중첩깊이 * 4096, saincharactar = 중첩깊이 * 128;
        while (현재자리 < iontráil_COUNT) {
            while (현재자리 < iontráil_COUNT && (FOINSE[BASE_suíomh + 현재자리] == 32 || FOINSE[BASE_suíomh + 현재자리] == 9)) 현재자리++;
            if (현재자리 == iontráil_COUNT || FOINSE[BASE_suíomh + 현재자리] == '#') break;
            if (총수 == 128) { ERREÁID("낱말이 너무 많습니다"); return -1; }
            int Start_suíomh = 현재자리, pointe_cóid = FOINSE[BASE_suíomh + 현재자리], 자료종류 = 0;
            if (pointe_cóid == ';') { 자료종류 = 1; 현재자리++; }
            else if (pointe_cóid == '&') { if (현재자리 + 1 >= iontráil_COUNT || FOINSE[BASE_suíomh + 현재자리 + 1] != '&') { ERREÁID("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } 자료종류 = 2; 현재자리 += 2; }
            else if (pointe_cóid == '|') { 현재자리++; 자료종류 = 현재자리 < iontráil_COUNT && FOINSE[BASE_suíomh + 현재자리] == '|' ? 3 : 4; if (자료종류 == 3) 현재자리++; }
            else if (pointe_cóid == '>') { 현재자리++; 자료종류 = 현재자리 < iontráil_COUNT && FOINSE[BASE_suíomh + 현재자리] == '>' ? 6 : 5; if (자료종류 == 6) 현재자리++; }
            else if (pointe_cóid == '<') { 자료종류 = 7; 현재자리++; }
            else {
                int Athfhriotail = 0;
                while (현재자리 < iontráil_COUNT) {
                    pointe_cóid = FOINSE[BASE_suíomh + 현재자리];
                    if (pointe_cóid == '`' && Athfhriotail != 39 || pointe_cóid == '$' && Athfhriotail != 39 && 현재자리 + 1 < iontráil_COUNT && FOINSE[BASE_suíomh + 현재자리 + 1] == '(') { ERREÁID("Ordú tomhas 치환은 지원하지 않습니다"); return -1; }
                    if (pointe_cóid == '\\' && Athfhriotail != 39) { if (++현재자리 == iontráil_COUNT) { ERREÁID("Líne 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } 현재자리++; continue; }
                    if (pointe_cóid == Athfhriotail) { Athfhriotail = 0; 현재자리++; continue; }
                    if (Athfhriotail == 0 && (pointe_cóid == 39 || pointe_cóid == 34)) { Athfhriotail = pointe_cóid; 현재자리++; continue; }
                    if (Athfhriotail == 0 && (pointe_cóid == 32 || pointe_cóid == 9 || pointe_cóid == ';' || pointe_cóid == '&' || pointe_cóid == '|' || pointe_cóid == '<' || pointe_cóid == '>')) break;
                    현재자리++;
                }
                if (Athfhriotail != 0) { ERREÁID("따옴표가 닫히지 않았습니다"); return -1; }
                if (현재자리 < iontráil_COUNT && (FOINSE[BASE_suíomh + 현재자리] == '>' || FOINSE[BASE_suíomh + 현재자리] == '<')) {
                    boolean 수치 = 현재자리 > Start_suíomh;
                    for (int lúb_INDEX = Start_suíomh; lúb_INDEX < 현재자리; lúb_INDEX++) if (FOINSE[BASE_suíomh + lúb_INDEX] < '0' || FOINSE[BASE_suíomh + lúb_INDEX] > '9') 수치 = false;
                    if (수치) { ERREÁID("번호를 지정한 Comhad 서술자 I_O 전환은 지원하지 않습니다"); return -1; }
                }
            }
            종류[saincharactar + 총수] = 자료종류; Rith_2[saincharactar + 총수] = Start_suíomh; 끝[saincharactar + 총수] = 현재자리; 총수++;
        }
        boolean 낱말 = false;
        for (int lúb_INDEX = 0; lúb_INDEX < 총수; lúb_INDEX++) {
            int 임시값 = 종류[saincharactar + lúb_INDEX];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++lúb_INDEX == 총수 || 종류[saincharactar + lúb_INDEX] != 0) { ERREÁID("I_O 전환에 Comhad 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || lúb_INDEX == 총수 - 1 && 임시값 != 1) { ERREÁID("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (총수 > 0 && !낱말 && 종류[saincharactar + 총수 - 1] != 1) { ERREÁID("명령이 빠졌습니다"); return -1; }
        return 총수;
    }
    static boolean 구간말(int[] sonraí_ARRAY, int logánta_Start, int iontráil_COUNT, String carachtar_suíomh) {
        if (iontráil_COUNT != carachtar_suíomh.length()) return false; for (int lúb_INDEX = 0; lúb_INDEX < iontráil_COUNT; lúb_INDEX++) if (sonraí_ARRAY[logánta_Start + lúb_INDEX] != carachtar_suíomh.charAt(lúb_INDEX)) return false; return true;
    }
    static void 넣기(int beart_sonraí) {
        if (쓴수 >= 명령해석기.licín_VALUE.length) { if (!breisiú_earráid) ERREÁID("변수를 펼친 명령이 너무 깁니다"); breisiú_earráid = true; return; }
        명령해석기.licín_VALUE[쓴수++] = beart_sonraí;
    }
    static void 변수(int[] sonraí_ARRAY, int Start_suíomh, int iontráil_COUNT) {
        if (구간말(sonraí_ARRAY, Start_suíomh, iontráil_COUNT, "PWD")) { 넣기('/'); for (int lúb_INDEX = 0; lúb_INDEX < Cuimhne_Comhaid.현재길이; lúb_INDEX++) 넣기(Cuimhne_Comhaid.현재[lúb_INDEX]); return; }
        if (구간말(sonraí_ARRAY, Start_suíomh, iontráil_COUNT, "HOME")) { 넣기('/'); return; }
        if (구간말(sonraí_ARRAY, Start_suíomh, iontráil_COUNT, "?")) {
            int sonraí_VALUE = staid_VALUE, digit = 100; boolean 시작여부 = false;
            while (digit > 0) { int 뒷값 = sonraí_VALUE / digit; if (뒷값 != 0 || 시작여부 || digit == 1) { 넣기('0' + 뒷값); 시작여부 = true; } sonraí_VALUE %= digit; digit /= 10; } return;
        }
        for (int lúb_INDEX = 0; lúb_INDEX < 16; lúb_INDEX++) if (이름길이[lúb_INDEX] == iontráil_COUNT) {
            boolean MATCH = true; for (int comhcheangal_istigh_suíomh = 0; comhcheangal_istigh_suíomh < iontráil_COUNT; comhcheangal_istigh_suíomh++) if (변수이름[lúb_INDEX * 32 + comhcheangal_istigh_suíomh] != sonraí_ARRAY[Start_suíomh + comhcheangal_istigh_suíomh]) MATCH = false;
            if (MATCH) { for (int comhcheangal_istigh_suíomh = 0; comhcheangal_istigh_suíomh < VALUE_fad[lúb_INDEX]; comhcheangal_istigh_suíomh++) 넣기(변수값[lúb_INDEX * 256 + comhcheangal_istigh_suíomh]); return; }
        }
    }
    static boolean Word_VALUE(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = Rith_2[중첩깊이 * 128 + 낱말번호], cuir_deireadh_le_suíomh = 끝[중첩깊이 * 128 + 낱말번호], BASE_suíomh = 중첩깊이 * 4096, Athfhriotail = 0;
        if (읽는자리 < cuir_deireadh_le_suíomh && FOINSE[BASE_suíomh + 읽는자리] == '~' && (읽는자리 + 1 == cuir_deireadh_le_suíomh || FOINSE[BASE_suíomh + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < cuir_deireadh_le_suíomh) {
            int pointe_cóid = FOINSE[BASE_suíomh + 읽는자리++];
            if (pointe_cóid == Athfhriotail) { Athfhriotail = 0; continue; }
            if (Athfhriotail == 0 && (pointe_cóid == 39 || pointe_cóid == 34)) { Athfhriotail = pointe_cóid; continue; }
            if (pointe_cóid == '\\' && Athfhriotail != 39) { int Ar_aghaidh_suíomh = FOINSE[BASE_suíomh + 읽는자리++]; if (Athfhriotail == 34 && Ar_aghaidh_suíomh != '$' && Ar_aghaidh_suíomh != '"' && Ar_aghaidh_suíomh != '\\') 넣기('\\'); 넣기(Ar_aghaidh_suíomh); continue; }
            if (pointe_cóid == '$' && Athfhriotail != 39 && 읽는자리 < cuir_deireadh_le_suíomh) {
                boolean 중괄호자리 = FOINSE[BASE_suíomh + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < cuir_deireadh_le_suíomh && FOINSE[BASE_suíomh + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < cuir_deireadh_le_suíomh && 이름뒤(FOINSE[BASE_suíomh + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == cuir_deireadh_le_suíomh || FOINSE[BASE_suíomh + 읽는자리] != '}')) { ERREÁID("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                변수(FOINSE, BASE_suíomh + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(pointe_cóid);
        }
        return !breisiú_earráid;
    }
    static int 환경설정(int argóint_INDEX, boolean bain) {
        int logánta_Start = 명령해석기.시작점[argóint_INDEX], cuir_deireadh_le_suíomh = logánta_Start + 명령해석기.fad_VALUE[argóint_INDEX], 같음자리 = logánta_Start;
        while (같음자리 < cuir_deireadh_le_suíomh && 명령해석기.licín_VALUE[같음자리] != '=') 같음자리++;
        int iontráil_COUNT = 같음자리 - logánta_Start;
        if (iontráil_COUNT < 1 || iontráil_COUNT > 31 || !ainm_carachtar(명령해석기.licín_VALUE[logánta_Start]) || !bain && 같음자리 == cuir_deireadh_le_suíomh || cuir_deireadh_le_suíomh - 같음자리 - 1 > 255) return 2;
        for (int lúb_INDEX = logánta_Start; lúb_INDEX < 같음자리; lúb_INDEX++) if (!이름뒤(명령해석기.licín_VALUE[lúb_INDEX])) return 2;
        if (구간말(명령해석기.licín_VALUE, logánta_Start, iontráil_COUNT, "PWD") || 구간말(명령해석기.licín_VALUE, logánta_Start, iontráil_COUNT, "HOME")) return 2;
        int 찾은여부 = -1, teicneolaíocht_faisnéise_folamh_staid = -1;
        for (int lúb_INDEX = 0; lúb_INDEX < 16; lúb_INDEX++) {
            if (이름길이[lúb_INDEX] == 0) teicneolaíocht_faisnéise_folamh_staid = lúb_INDEX;
            if (이름길이[lúb_INDEX] != iontráil_COUNT) continue;
            boolean MATCH = true; for (int comhcheangal_istigh_suíomh = 0; comhcheangal_istigh_suíomh < iontráil_COUNT; comhcheangal_istigh_suíomh++) if (변수이름[lúb_INDEX * 32 + comhcheangal_istigh_suíomh] != 명령해석기.licín_VALUE[logánta_Start + comhcheangal_istigh_suíomh]) MATCH = false;
            if (MATCH) 찾은여부 = lúb_INDEX;
        }
        if (bain) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = teicneolaíocht_faisnéise_folamh_staid; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = iontráil_COUNT; VALUE_fad[찾은여부] = cuir_deireadh_le_suíomh - 같음자리 - 1;
        for (int lúb_INDEX = 0; lúb_INDEX < iontráil_COUNT; lúb_INDEX++) 변수이름[찾은여부 * 32 + lúb_INDEX] = 명령해석기.licín_VALUE[logánta_Start + lúb_INDEX];
        for (int lúb_INDEX = 같음자리 + 1; lúb_INDEX < cuir_deireadh_le_suíomh; lúb_INDEX++) 변수값[찾은여부 * 256 + lúb_INDEX - 같음자리 - 1] = 명령해석기.licín_VALUE[lúb_INDEX];
        return 0;
    }
    static void 환경보기() {
        단말.Scríobh("HOME=/\nPWD="); Cuimhne_Comhaid.현재쓰기(); 단말.문자(10);
        for (int lúb_INDEX = 0; lúb_INDEX < 16; lúb_INDEX++) if (이름길이[lúb_INDEX] > 0) {
            for (int comhcheangal_istigh_suíomh = 0; comhcheangal_istigh_suíomh < 이름길이[lúb_INDEX]; comhcheangal_istigh_suíomh++) clár.직렬쓰기(변수이름[lúb_INDEX * 32 + comhcheangal_istigh_suíomh]); 단말.문자('=');
            for (int comhcheangal_istigh_suíomh = 0; comhcheangal_istigh_suíomh < VALUE_fad[lúb_INDEX]; comhcheangal_istigh_suíomh++) clár.직렬쓰기(변수값[lúb_INDEX * 256 + comhcheangal_istigh_suíomh]); 단말.문자(10);
        }
    }
    static void Rith_ordú(int[] sonraí_ARRAY, int 시작변위, int iontráil_COUNT, int 중첩깊이) {
        if (중첩깊이 >= 4 || iontráil_COUNT > 4096) { ERREÁID("Ordú 파일의 중첩 또는 Líne fad_VALUE 제한을 넘었습니다"); return; }
        for (int lúb_INDEX = 0; lúb_INDEX < iontráil_COUNT; lúb_INDEX++) FOINSE[중첩깊이 * 4096 + lúb_INDEX] = sonraí_ARRAY[시작변위 + lúb_INDEX];
        int 총수 = Léigh(iontráil_COUNT, 중첩깊이); if (총수 < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < 총수) {
            int Grúpa_cuir_deireadh_le = 읽는자리;
            while (Grúpa_cuir_deireadh_le < 총수 && (종류[중첩깊이 * 128 + Grúpa_cuir_deireadh_le] == 0 || 종류[중첩깊이 * 128 + Grúpa_cuir_deireadh_le] >= 4)) Grúpa_cuir_deireadh_le++;
            boolean Rith_cc685ae5 = 조건성립 == 1 || 조건성립 == 2 && staid_VALUE == 0 || 조건성립 == 3 && staid_VALUE != 0;
            if (Rith_cc685ae5) {
                boolean 이전자리 = false;
                while (읽는자리 < Grúpa_cuir_deireadh_le) {
                    int Ar_aghaidh_suíomh = 읽는자리; while (Ar_aghaidh_suíomh < Grúpa_cuir_deireadh_le && 종류[중첩깊이 * 128 + Ar_aghaidh_suíomh] != 4) Ar_aghaidh_suíomh++;
                    boolean nasc_sruth = Ar_aghaidh_suíomh < Grúpa_cuir_deireadh_le; int 입력쪽 = -1, 출력쪽 = -1, 출력방식 = 0;
                    명령해석기.licín_COUNT = 0; 쓴수 = 0; breisiú_earráid = false;
                    for (int lúb_INDEX = 읽는자리; lúb_INDEX < Ar_aghaidh_suíomh; lúb_INDEX++) {
                        int 자료종류 = 종류[중첩깊이 * 128 + lúb_INDEX];
                        if (자료종류 >= 5) { if (자료종류 == 7) { if (입력쪽 >= 0) { ERREÁID("입력 전환이 겹쳤습니다"); return; } 입력쪽 = ++lúb_INDEX; } else { if (출력쪽 >= 0) { ERREÁID("Aschur 전환이 겹쳤습니다"); return; } 출력쪽 = ++lúb_INDEX; 출력방식 = 자료종류; } continue; }
                        if (명령해석기.licín_COUNT == 32) { ERREÁID("인수가 너무 많습니다"); return; }
                        int argóint_INDEX = 명령해석기.licín_COUNT++; 명령해석기.시작점[argóint_INDEX] = 쓴수;
                        if (!Word_VALUE(lúb_INDEX, 중첩깊이)) return;
                        명령해석기.fad_VALUE[argóint_INDEX] = 쓴수 - 명령해석기.시작점[argóint_INDEX];
                    }
                    연결중 = 이전자리 || nasc_sruth || 입력쪽 >= 0 || 출력쪽 >= 0;
                    if (연결중 && (명령해석기.같음(0, "vi") || 명령해석기.같음(0, "edit") || 명령해석기.같음(0, "load") || 명령해석기.같음(0, "gui") || 명령해석기.같음(0, "terminal") || 명령해석기.같음(0, "sh") || 명령해석기.같음(0, "source"))) { ERREÁID("idirghníomhach 명령과 Ordú 파일은 I_O 전환이나 sruth_VALUE 연결에 쓸 수 없습니다"); return; }
                    셸입출력.Rith_2(이전자리, nasc_sruth);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int iontráil_suíomh = 입출력바꿈 == 0 ? 입력쪽 : 출력쪽; if (iontráil_suíomh < 0) continue;
                        int Start_suíomh = 쓴수; if (!Word_VALUE(iontráil_suíomh, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = Cuimhne_Comhaid.cosán_Start(쓴수 - Start_suíomh);
                        for (int comhcheangal_istigh_suíomh = Start_suíomh; 처리값 >= 0 && comhcheangal_istigh_suíomh < 쓴수; comhcheangal_istigh_suíomh++) 처리값 = Cuimhne_Comhaid.cosán_beart(comhcheangal_istigh_suíomh - Start_suíomh, 명령해석기.licín_VALUE[comhcheangal_istigh_suíomh]);
                        if (처리값 >= 0) 처리값 = Cuimhne_Comhaid.Oscail(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); 명령해석기.ERREÁID(처리값); staid_VALUE = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.입력파일 = 처리값; else 셸입출력.comhad_aschuir = 처리값;
                    }
                    셸입출력.Ceadaigh_idirghníomhach = 중첩깊이 == 0 && 읽는자리 == 0 && Ar_aghaidh_suíomh == 총수;
                    깊이 = 중첩깊이; 명령해석기.tomhas = 0; clár.입출력전환(1);
                    명령해석기.Ordú();
                    clár.Teirminéal(3);
                    int 반환값 = 명령해석기.tomhas, sruth_earráid = 셸입출력.teip_VALUE;
                    셸입출력.끝(); 연결중 = false;
                    staid_VALUE = sruth_earráid < 0 ? 1 : 반환값;
                    if (sruth_earráid < 0) { 명령해석기.ERREÁID(sruth_earráid); return; }
                    if (script_cuir_deireadh_le || 반환값 == -1005) return;
                    이전자리 = true; 읽는자리 = Ar_aghaidh_suíomh + 1;
                }
            }
            if (Grúpa_cuir_deireadh_le < 총수) 조건성립 = 종류[중첩깊이 * 128 + Grúpa_cuir_deireadh_le];
            읽는자리 = Grúpa_cuir_deireadh_le + 1;
        }
    }
    static void Rith_comhad() {
        if (명령해석기.licín_COUNT != 2 || 깊이 >= 3) { 명령해석기.tomhas = 2; 단말.Scríobh("사용법: sh Comhad (중첩 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = 명령해석기.CONAIR(1); if (처리값 >= 0) 처리값 = Cuimhne_Comhaid.Oscail(0);
        if (처리값 < 0) { 명령해석기.ERREÁID(처리값); return; }
        int iontráil_COUNT = 0, beart_sonraí;
        while ((beart_sonraí = Cuimhne_Comhaid.Léigh(처리값)) != 256 && beart_sonraí >= 0 && iontráil_COUNT < 16384) script_VALUE[중첩깊이 * 16384 + iontráil_COUNT++] = beart_sonraí;
        Cuimhne_Comhaid.Dún(처리값); clár.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < iontráil_COUNT && !script_cuir_deireadh_le;) {
            int cuir_deireadh_le_suíomh = 읽는자리; while (cuir_deireadh_le_suíomh < iontráil_COUNT && script_VALUE[중첩깊이 * 16384 + cuir_deireadh_le_suíomh] != 10) cuir_deireadh_le_suíomh++;
            int 유효길이 = cuir_deireadh_le_suíomh - 읽는자리; if (유효길이 > 0 && script_VALUE[중첩깊이 * 16384 + cuir_deireadh_le_suíomh - 1] == 13) 유효길이--;
            Rith_ordú(script_VALUE, 중첩깊이 * 16384 + 읽는자리, 유효길이, 중첩깊이); 읽는자리 = cuir_deireadh_le_suíomh + 1;
        }
        명령해석기.tomhas = staid_VALUE; script_cuir_deireadh_le = false; 깊이 = 중첩깊이 - 1;
    }
}
