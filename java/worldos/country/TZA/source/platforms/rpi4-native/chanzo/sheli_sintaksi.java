// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 ingiliani sheli 문법. 파이프는 순차 tekeleza_amri, 환경은 같은 셸에서 공유한다. */
public final class sheli_sintaksi {
    static int[] chanzo = new int[4 * 4096], 종류 = new int[4 * 128], endesha = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] 변수이름 = new int[16 * 32], 변수값 = new int[16 * 256], 이름길이 = new int[16], thamani_urefu = new int[16];
    static int[] hati_thamani = new int[4 * 16384];
    static int hali_thamani, 깊이, 쓴수;
    static boolean 연결중, hati_tamatia, kiendelezi_kosa;
    static boolean jina_kibambo(int msimbo_wa_kibambo) { return msimbo_wa_kibambo >= 'a' && msimbo_wa_kibambo <= 'z' || msimbo_wa_kibambo >= 'A' && msimbo_wa_kibambo <= 'Z' || msimbo_wa_kibambo == '_' || msimbo_wa_kibambo >= 128; }
    static boolean 이름뒤(int msimbo_wa_kibambo) { return jina_kibambo(msimbo_wa_kibambo) || msimbo_wa_kibambo >= '0' && msimbo_wa_kibambo <= '9'; }
    static void kosa(String SMS) { 보드.입출력전환(0); 단말.andika("amri changanua_thamani: "); 단말.andika(SMS); 단말.문자(10); hali_thamani = 2; }
    static int 읽기(int 항목수, int 중첩깊이) {
        int 현재자리 = 0, 총수 = 0, 기준자리 = 중첩깊이 * 4096, kibambo_spesheli = 중첩깊이 * 128;
        while (현재자리 < 항목수) {
            while (현재자리 < 항목수 && (chanzo[기준자리 + 현재자리] == 32 || chanzo[기준자리 + 현재자리] == 9)) 현재자리++;
            if (현재자리 == 항목수 || chanzo[기준자리 + 현재자리] == '#') break;
            if (총수 == 128) { kosa("낱말이 너무 많습니다"); return -1; }
            int 시작자리 = 현재자리, msimbo_wa_kibambo = chanzo[기준자리 + 현재자리], 자료종류 = 0;
            if (msimbo_wa_kibambo == ';') { 자료종류 = 1; 현재자리++; }
            else if (msimbo_wa_kibambo == '&') { if (현재자리 + 1 >= 항목수 || chanzo[기준자리 + 현재자리 + 1] != '&') { kosa("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } 자료종류 = 2; 현재자리 += 2; }
            else if (msimbo_wa_kibambo == '|') { 현재자리++; 자료종류 = 현재자리 < 항목수 && chanzo[기준자리 + 현재자리] == '|' ? 3 : 4; if (자료종류 == 3) 현재자리++; }
            else if (msimbo_wa_kibambo == '>') { 현재자리++; 자료종류 = 현재자리 < 항목수 && chanzo[기준자리 + 현재자리] == '>' ? 6 : 5; if (자료종류 == 6) 현재자리++; }
            else if (msimbo_wa_kibambo == '<') { 자료종류 = 7; 현재자리++; }
            else {
                int 따옴표 = 0;
                while (현재자리 < 항목수) {
                    msimbo_wa_kibambo = chanzo[기준자리 + 현재자리];
                    if (msimbo_wa_kibambo == '`' && 따옴표 != 39 || msimbo_wa_kibambo == '$' && 따옴표 != 39 && 현재자리 + 1 < 항목수 && chanzo[기준자리 + 현재자리 + 1] == '(') { kosa("amri 결과 치환은 지원하지 않습니다"); return -1; }
                    if (msimbo_wa_kibambo == '\\' && 따옴표 != 39) { if (++현재자리 == 항목수) { kosa("laini 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } 현재자리++; continue; }
                    if (msimbo_wa_kibambo == 따옴표) { 따옴표 = 0; 현재자리++; continue; }
                    if (따옴표 == 0 && (msimbo_wa_kibambo == 39 || msimbo_wa_kibambo == 34)) { 따옴표 = msimbo_wa_kibambo; 현재자리++; continue; }
                    if (따옴표 == 0 && (msimbo_wa_kibambo == 32 || msimbo_wa_kibambo == 9 || msimbo_wa_kibambo == ';' || msimbo_wa_kibambo == '&' || msimbo_wa_kibambo == '|' || msimbo_wa_kibambo == '<' || msimbo_wa_kibambo == '>')) break;
                    현재자리++;
                }
                if (따옴표 != 0) { kosa("따옴표가 닫히지 않았습니다"); return -1; }
                if (현재자리 < 항목수 && (chanzo[기준자리 + 현재자리] == '>' || chanzo[기준자리 + 현재자리] == '<')) {
                    boolean 수치 = 현재자리 > 시작자리;
                    for (int kitanzi_kielezo = 시작자리; kitanzi_kielezo < 현재자리; kitanzi_kielezo++) if (chanzo[기준자리 + kitanzi_kielezo] < '0' || chanzo[기준자리 + kitanzi_kielezo] > '9') 수치 = false;
                    if (수치) { kosa("번호를 지정한 faili 서술자 I_T 전환은 지원하지 않습니다"); return -1; }
                }
            }
            종류[kibambo_spesheli + 총수] = 자료종류; endesha[kibambo_spesheli + 총수] = 시작자리; 끝[kibambo_spesheli + 총수] = 현재자리; 총수++;
        }
        boolean 낱말 = false;
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < 총수; kitanzi_kielezo++) {
            int 임시값 = 종류[kibambo_spesheli + kitanzi_kielezo];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++kitanzi_kielezo == 총수 || 종류[kibambo_spesheli + kitanzi_kielezo] != 0) { kosa("I_T 전환에 faili 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || kitanzi_kielezo == 총수 - 1 && 임시값 != 1) { kosa("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (총수 > 0 && !낱말 && 종류[kibambo_spesheli + 총수 - 1] != 1) { kosa("명령이 빠졌습니다"); return -1; }
        return 총수;
    }
    static boolean 구간말(int[] data_ARRAY, int jirani_Anza, int 항목수, String 문자위치) {
        if (항목수 != 문자위치.length()) return false; for (int kitanzi_kielezo = 0; kitanzi_kielezo < 항목수; kitanzi_kielezo++) if (data_ARRAY[jirani_Anza + kitanzi_kielezo] != 문자위치.charAt(kitanzi_kielezo)) return false; return true;
    }
    static void 넣기(int baiti_data) {
        if (쓴수 >= 명령해석기.tuzo_thamani.length) { if (!kiendelezi_kosa) kosa("변수를 펼친 명령이 너무 깁니다"); kiendelezi_kosa = true; return; }
        명령해석기.tuzo_thamani[쓴수++] = baiti_data;
    }
    static void 변수(int[] data_ARRAY, int 시작자리, int 항목수) {
        if (구간말(data_ARRAY, 시작자리, 항목수, "PWD")) { 넣기('/'); for (int kitanzi_kielezo = 0; kitanzi_kielezo < kumbukumbu_Faili.현재길이; kitanzi_kielezo++) 넣기(kumbukumbu_Faili.현재[kitanzi_kielezo]); return; }
        if (구간말(data_ARRAY, 시작자리, 항목수, "HOME")) { 넣기('/'); return; }
        if (구간말(data_ARRAY, 시작자리, 항목수, "?")) {
            int data_thamani = hali_thamani, dijiti = 100; boolean 시작여부 = false;
            while (dijiti > 0) { int 뒷값 = data_thamani / dijiti; if (뒷값 != 0 || 시작여부 || dijiti == 1) { 넣기('0' + 뒷값); 시작여부 = true; } data_thamani %= dijiti; dijiti /= 10; } return;
        }
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < 16; kitanzi_kielezo++) if (이름길이[kitanzi_kielezo] == 항목수) {
            boolean 일치여부 = true; for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) if (변수이름[kitanzi_kielezo * 32 + 안쪽자리] != data_ARRAY[시작자리 + 안쪽자리]) 일치여부 = false;
            if (일치여부) { for (int 안쪽자리 = 0; 안쪽자리 < thamani_urefu[kitanzi_kielezo]; 안쪽자리++) 넣기(변수값[kitanzi_kielezo * 256 + 안쪽자리]); return; }
        }
    }
    static boolean Neno_thamani(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = endesha[중첩깊이 * 128 + 낱말번호], 끝자리 = 끝[중첩깊이 * 128 + 낱말번호], 기준자리 = 중첩깊이 * 4096, 따옴표 = 0;
        if (읽는자리 < 끝자리 && chanzo[기준자리 + 읽는자리] == '~' && (읽는자리 + 1 == 끝자리 || chanzo[기준자리 + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < 끝자리) {
            int msimbo_wa_kibambo = chanzo[기준자리 + 읽는자리++];
            if (msimbo_wa_kibambo == 따옴표) { 따옴표 = 0; continue; }
            if (따옴표 == 0 && (msimbo_wa_kibambo == 39 || msimbo_wa_kibambo == 34)) { 따옴표 = msimbo_wa_kibambo; continue; }
            if (msimbo_wa_kibambo == '\\' && 따옴표 != 39) { int 다음자리 = chanzo[기준자리 + 읽는자리++]; if (따옴표 == 34 && 다음자리 != '$' && 다음자리 != '"' && 다음자리 != '\\') 넣기('\\'); 넣기(다음자리); continue; }
            if (msimbo_wa_kibambo == '$' && 따옴표 != 39 && 읽는자리 < 끝자리) {
                boolean 중괄호자리 = chanzo[기준자리 + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < 끝자리 && chanzo[기준자리 + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < 끝자리 && 이름뒤(chanzo[기준자리 + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == 끝자리 || chanzo[기준자리 + 읽는자리] != '}')) { kosa("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                변수(chanzo, 기준자리 + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(msimbo_wa_kibambo);
        }
        return !kiendelezi_kosa;
    }
    static int 환경설정(int hoja_kielezo, boolean ondoa) {
        int jirani_Anza = 명령해석기.시작점[hoja_kielezo], 끝자리 = jirani_Anza + 명령해석기.urefu_thamani[hoja_kielezo], 같음자리 = jirani_Anza;
        while (같음자리 < 끝자리 && 명령해석기.tuzo_thamani[같음자리] != '=') 같음자리++;
        int 항목수 = 같음자리 - jirani_Anza;
        if (항목수 < 1 || 항목수 > 31 || !jina_kibambo(명령해석기.tuzo_thamani[jirani_Anza]) || !ondoa && 같음자리 == 끝자리 || 끝자리 - 같음자리 - 1 > 255) return 2;
        for (int kitanzi_kielezo = jirani_Anza; kitanzi_kielezo < 같음자리; kitanzi_kielezo++) if (!이름뒤(명령해석기.tuzo_thamani[kitanzi_kielezo])) return 2;
        if (구간말(명령해석기.tuzo_thamani, jirani_Anza, 항목수, "PWD") || 구간말(명령해석기.tuzo_thamani, jirani_Anza, 항목수, "HOME")) return 2;
        int 찾은여부 = -1, teknolojia_ya_maelezo_tupu_hali = -1;
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < 16; kitanzi_kielezo++) {
            if (이름길이[kitanzi_kielezo] == 0) teknolojia_ya_maelezo_tupu_hali = kitanzi_kielezo;
            if (이름길이[kitanzi_kielezo] != 항목수) continue;
            boolean 일치여부 = true; for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) if (변수이름[kitanzi_kielezo * 32 + 안쪽자리] != 명령해석기.tuzo_thamani[jirani_Anza + 안쪽자리]) 일치여부 = false;
            if (일치여부) 찾은여부 = kitanzi_kielezo;
        }
        if (ondoa) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = teknolojia_ya_maelezo_tupu_hali; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = 항목수; thamani_urefu[찾은여부] = 끝자리 - 같음자리 - 1;
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < 항목수; kitanzi_kielezo++) 변수이름[찾은여부 * 32 + kitanzi_kielezo] = 명령해석기.tuzo_thamani[jirani_Anza + kitanzi_kielezo];
        for (int kitanzi_kielezo = 같음자리 + 1; kitanzi_kielezo < 끝자리; kitanzi_kielezo++) 변수값[찾은여부 * 256 + kitanzi_kielezo - 같음자리 - 1] = 명령해석기.tuzo_thamani[kitanzi_kielezo];
        return 0;
    }
    static void 환경보기() {
        단말.andika("HOME=/\nPWD="); kumbukumbu_Faili.현재쓰기(); 단말.문자(10);
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < 16; kitanzi_kielezo++) if (이름길이[kitanzi_kielezo] > 0) {
            for (int 안쪽자리 = 0; 안쪽자리 < 이름길이[kitanzi_kielezo]; 안쪽자리++) 보드.직렬쓰기(변수이름[kitanzi_kielezo * 32 + 안쪽자리]); 단말.문자('=');
            for (int 안쪽자리 = 0; 안쪽자리 < thamani_urefu[kitanzi_kielezo]; 안쪽자리++) 보드.직렬쓰기(변수값[kitanzi_kielezo * 256 + 안쪽자리]); 단말.문자(10);
        }
    }
    static void tekeleza_amri(int[] data_ARRAY, int 시작변위, int 항목수, int 중첩깊이) {
        if (중첩깊이 >= 4 || 항목수 > 4096) { kosa("amri 파일의 uingiliani_thamani 또는 laini urefu_thamani 제한을 넘었습니다"); return; }
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < 항목수; kitanzi_kielezo++) chanzo[중첩깊이 * 4096 + kitanzi_kielezo] = data_ARRAY[시작변위 + kitanzi_kielezo];
        int 총수 = 읽기(항목수, 중첩깊이); if (총수 < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < 총수) {
            int Kikundi_tamatia = 읽는자리;
            while (Kikundi_tamatia < 총수 && (종류[중첩깊이 * 128 + Kikundi_tamatia] == 0 || 종류[중첩깊이 * 128 + Kikundi_tamatia] >= 4)) Kikundi_tamatia++;
            boolean tekeleza = 조건성립 == 1 || 조건성립 == 2 && hali_thamani == 0 || 조건성립 == 3 && hali_thamani != 0;
            if (tekeleza) {
                boolean 이전자리 = false;
                while (읽는자리 < Kikundi_tamatia) {
                    int 다음자리 = 읽는자리; while (다음자리 < Kikundi_tamatia && 종류[중첩깊이 * 128 + 다음자리] != 4) 다음자리++;
                    boolean UNGANISHA_Stream = 다음자리 < Kikundi_tamatia; int 입력쪽 = -1, 출력쪽 = -1, 출력방식 = 0;
                    명령해석기.토큰수 = 0; 쓴수 = 0; kiendelezi_kosa = false;
                    for (int kitanzi_kielezo = 읽는자리; kitanzi_kielezo < 다음자리; kitanzi_kielezo++) {
                        int 자료종류 = 종류[중첩깊이 * 128 + kitanzi_kielezo];
                        if (자료종류 >= 5) { if (자료종류 == 7) { if (입력쪽 >= 0) { kosa("입력 전환이 겹쳤습니다"); return; } 입력쪽 = ++kitanzi_kielezo; } else { if (출력쪽 >= 0) { kosa("출력 전환이 겹쳤습니다"); return; } 출력쪽 = ++kitanzi_kielezo; 출력방식 = 자료종류; } continue; }
                        if (명령해석기.토큰수 == 32) { kosa("인수가 너무 많습니다"); return; }
                        int hoja_kielezo = 명령해석기.토큰수++; 명령해석기.시작점[hoja_kielezo] = 쓴수;
                        if (!Neno_thamani(kitanzi_kielezo, 중첩깊이)) return;
                        명령해석기.urefu_thamani[hoja_kielezo] = 쓴수 - 명령해석기.시작점[hoja_kielezo];
                    }
                    연결중 = 이전자리 || UNGANISHA_Stream || 입력쪽 >= 0 || 출력쪽 >= 0;
                    if (연결중 && (명령해석기.같음(0, "vi") || 명령해석기.같음(0, "edit") || 명령해석기.같음(0, "load") || 명령해석기.같음(0, "gui") || 명령해석기.같음(0, "terminal") || 명령해석기.같음(0, "sh") || 명령해석기.같음(0, "source"))) { kosa("ingiliani 명령과 amri 파일은 I_T 전환이나 Stream_thamani 연결에 쓸 수 없습니다"); return; }
                    셸입출력.endesha(이전자리, UNGANISHA_Stream);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int 항목자리 = 입출력바꿈 == 0 ? 입력쪽 : 출력쪽; if (항목자리 < 0) continue;
                        int 시작자리 = 쓴수; if (!Neno_thamani(항목자리, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = kumbukumbu_Faili.njia_Anza(쓴수 - 시작자리);
                        for (int 안쪽자리 = 시작자리; 처리값 >= 0 && 안쪽자리 < 쓴수; 안쪽자리++) 처리값 = kumbukumbu_Faili.njia_baiti(안쪽자리 - 시작자리, 명령해석기.tuzo_thamani[안쪽자리]);
                        if (처리값 >= 0) 처리값 = kumbukumbu_Faili.unda(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); 명령해석기.kosa(처리값); hali_thamani = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.입력파일 = 처리값; else 셸입출력.faili_towe = 처리값;
                    }
                    셸입출력.Ruhusu_ingiliani = 중첩깊이 == 0 && 읽는자리 == 0 && 다음자리 == 총수;
                    깊이 = 중첩깊이; 명령해석기.결과 = 0; 보드.입출력전환(1);
                    명령해석기.amri();
                    보드.터미널(3);
                    int 반환값 = 명령해석기.결과, Stream_kosa = 셸입출력.kushindwa_thamani;
                    셸입출력.끝(); 연결중 = false;
                    hali_thamani = Stream_kosa < 0 ? 1 : 반환값;
                    if (Stream_kosa < 0) { 명령해석기.kosa(Stream_kosa); return; }
                    if (hati_tamatia || 반환값 == -1005) return;
                    이전자리 = true; 읽는자리 = 다음자리 + 1;
                }
            }
            if (Kikundi_tamatia < 총수) 조건성립 = 종류[중첩깊이 * 128 + Kikundi_tamatia];
            읽는자리 = Kikundi_tamatia + 1;
        }
    }
    static void tekeleza_faili() {
        if (명령해석기.토큰수 != 2 || 깊이 >= 3) { 명령해석기.결과 = 2; 단말.andika("사용법: sh faili (uingiliani_thamani 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = 명령해석기.njia(1); if (처리값 >= 0) 처리값 = kumbukumbu_Faili.unda(0);
        if (처리값 < 0) { 명령해석기.kosa(처리값); return; }
        int 항목수 = 0, baiti_data;
        while ((baiti_data = kumbukumbu_Faili.읽기(처리값)) != 256 && baiti_data >= 0 && 항목수 < 16384) hati_thamani[중첩깊이 * 16384 + 항목수++] = baiti_data;
        kumbukumbu_Faili.funga(처리값); 보드.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < 항목수 && !hati_tamatia;) {
            int 끝자리 = 읽는자리; while (끝자리 < 항목수 && hati_thamani[중첩깊이 * 16384 + 끝자리] != 10) 끝자리++;
            int 유효길이 = 끝자리 - 읽는자리; if (유효길이 > 0 && hati_thamani[중첩깊이 * 16384 + 끝자리 - 1] == 13) 유효길이--;
            tekeleza_amri(hati_thamani, 중첩깊이 * 16384 + 읽는자리, 유효길이, 중첩깊이); 읽는자리 = 끝자리 + 1;
        }
        명령해석기.결과 = hali_thamani; hati_tamatia = false; 깊이 = 중첩깊이 - 1;
    }
}
