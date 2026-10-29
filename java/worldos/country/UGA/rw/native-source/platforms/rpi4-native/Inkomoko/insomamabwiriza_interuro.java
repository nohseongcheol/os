// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 interfacebikorana insomamabwiriza 문법. 파이프는 순차 gukora_ibwiriza, 환경은 같은 셸에서 공유한다. */
public final class insomamabwiriza_interuro {
    static int[] Inkomoko = new int[4 * 4096], 종류 = new int[4 * 128], ihuriro = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] 변수이름 = new int[16 * 32], 변수값 = new int[16 * 256], 이름길이 = new int[16], agaciro_uburebure = new int[16];
    static int[] sikiributi_agaciro = new int[4 * 16384];
    static int imimerere_agaciro, 깊이, 쓴수;
    static boolean 연결중, sikiributi_kurangiza, umugereka_ikosa;
    static boolean izina_inyuguti(int 문자값) { return 문자값 >= 'a' && 문자값 <= 'z' || 문자값 >= 'A' && 문자값 <= 'Z' || 문자값 == '_' || 문자값 >= 128; }
    static boolean 이름뒤(int 문자값) { return izina_inyuguti(문자값) || 문자값 >= '0' && 문자값 <= '9'; }
    static void IKOSA(String Umwandiko) { 보드.입출력전환(0); 단말.kwandika("Icyo_wifuza gusesengura_agaciro: "); 단말.kwandika(Umwandiko); 단말.문자(10); imimerere_agaciro = 2; }
    static int 읽기(int 항목수, int 중첩깊이) {
        int 현재자리 = 0, 총수 = 0, 기준자리 = 중첩깊이 * 4096, ikimenyetso_kidasanzwe = 중첩깊이 * 128;
        while (현재자리 < 항목수) {
            while (현재자리 < 항목수 && (Inkomoko[기준자리 + 현재자리] == 32 || Inkomoko[기준자리 + 현재자리] == 9)) 현재자리++;
            if (현재자리 == 항목수 || Inkomoko[기준자리 + 현재자리] == '#') break;
            if (총수 == 128) { IKOSA("낱말이 너무 많습니다"); return -1; }
            int 시작자리 = 현재자리, 문자값 = Inkomoko[기준자리 + 현재자리], 자료종류 = 0;
            if (문자값 == ';') { 자료종류 = 1; 현재자리++; }
            else if (문자값 == '&') { if (현재자리 + 1 >= 항목수 || Inkomoko[기준자리 + 현재자리 + 1] != '&') { IKOSA("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } 자료종류 = 2; 현재자리 += 2; }
            else if (문자값 == '|') { 현재자리++; 자료종류 = 현재자리 < 항목수 && Inkomoko[기준자리 + 현재자리] == '|' ? 3 : 4; if (자료종류 == 3) 현재자리++; }
            else if (문자값 == '>') { 현재자리++; 자료종류 = 현재자리 < 항목수 && Inkomoko[기준자리 + 현재자리] == '>' ? 6 : 5; if (자료종류 == 6) 현재자리++; }
            else if (문자값 == '<') { 자료종류 = 7; 현재자리++; }
            else {
                int 따옴표 = 0;
                while (현재자리 < 항목수) {
                    문자값 = Inkomoko[기준자리 + 현재자리];
                    if (문자값 == '`' && 따옴표 != 39 || 문자값 == '$' && 따옴표 != 39 && 현재자리 + 1 < 항목수 && Inkomoko[기준자리 + 현재자리 + 1] == '(') { IKOSA("Icyo_wifuza 결과 치환은 지원하지 않습니다"); return -1; }
                    if (문자값 == '\\' && 따옴표 != 39) { if (++현재자리 == 항목수) { IKOSA("umurongo 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } 현재자리++; continue; }
                    if (문자값 == 따옴표) { 따옴표 = 0; 현재자리++; continue; }
                    if (따옴표 == 0 && (문자값 == 39 || 문자값 == 34)) { 따옴표 = 문자값; 현재자리++; continue; }
                    if (따옴표 == 0 && (문자값 == 32 || 문자값 == 9 || 문자값 == ';' || 문자값 == '&' || 문자값 == '|' || 문자값 == '<' || 문자값 == '>')) break;
                    현재자리++;
                }
                if (따옴표 != 0) { IKOSA("따옴표가 닫히지 않았습니다"); return -1; }
                if (현재자리 < 항목수 && (Inkomoko[기준자리 + 현재자리] == '>' || Inkomoko[기준자리 + 현재자리] == '<')) {
                    boolean 수치 = 현재자리 > 시작자리;
                    for (int gukora_mu_matsinda_umugerekashakiro = 시작자리; gukora_mu_matsinda_umugerekashakiro < 현재자리; gukora_mu_matsinda_umugerekashakiro++) if (Inkomoko[기준자리 + gukora_mu_matsinda_umugerekashakiro] < '0' || Inkomoko[기준자리 + gukora_mu_matsinda_umugerekashakiro] > '9') 수치 = false;
                    if (수치) { IKOSA("번호를 지정한 Idosiye 서술자 I_O 전환은 지원하지 않습니다"); return -1; }
                }
            }
            종류[ikimenyetso_kidasanzwe + 총수] = 자료종류; ihuriro[ikimenyetso_kidasanzwe + 총수] = 시작자리; 끝[ikimenyetso_kidasanzwe + 총수] = 현재자리; 총수++;
        }
        boolean 낱말 = false;
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 총수; gukora_mu_matsinda_umugerekashakiro++) {
            int 임시값 = 종류[ikimenyetso_kidasanzwe + gukora_mu_matsinda_umugerekashakiro];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++gukora_mu_matsinda_umugerekashakiro == 총수 || 종류[ikimenyetso_kidasanzwe + gukora_mu_matsinda_umugerekashakiro] != 0) { IKOSA("I_O 전환에 Idosiye 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || gukora_mu_matsinda_umugerekashakiro == 총수 - 1 && 임시값 != 1) { IKOSA("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (총수 > 0 && !낱말 && 종류[ikimenyetso_kidasanzwe + 총수 - 1] != 1) { IKOSA("명령이 빠졌습니다"); return -1; }
        return 총수;
    }
    static boolean 구간말(int[] amakurushingiro_ARRAY, int mu_gace_Itangira, int 항목수, String 문자위치) {
        if (항목수 != 문자위치.length()) return false; for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 항목수; gukora_mu_matsinda_umugerekashakiro++) if (amakurushingiro_ARRAY[mu_gace_Itangira + gukora_mu_matsinda_umugerekashakiro] != 문자위치.charAt(gukora_mu_matsinda_umugerekashakiro)) return false; return true;
    }
    static void 넣기(int bayiti_amakurushingiro) {
        if (쓴수 >= 명령해석기.tike_agaciro.length) { if (!umugereka_ikosa) IKOSA("변수를 펼친 명령이 너무 깁니다"); umugereka_ikosa = true; return; }
        명령해석기.tike_agaciro[쓴수++] = bayiti_amakurushingiro;
    }
    static void 변수(int[] amakurushingiro_ARRAY, int 시작자리, int 항목수) {
        if (구간말(amakurushingiro_ARRAY, 시작자리, 항목수, "PWD")) { 넣기('/'); for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < ububiko_Dosiye.현재길이; gukora_mu_matsinda_umugerekashakiro++) 넣기(ububiko_Dosiye.현재[gukora_mu_matsinda_umugerekashakiro]); return; }
        if (구간말(amakurushingiro_ARRAY, 시작자리, 항목수, "HOME")) { 넣기('/'); return; }
        if (구간말(amakurushingiro_ARRAY, 시작자리, 항목수, "?")) {
            int amakurushingiro_agaciro = imimerere_agaciro, umubare = 100; boolean 시작여부 = false;
            while (umubare > 0) { int 뒷값 = amakurushingiro_agaciro / umubare; if (뒷값 != 0 || 시작여부 || umubare == 1) { 넣기('0' + 뒷값); 시작여부 = true; } amakurushingiro_agaciro %= umubare; umubare /= 10; } return;
        }
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 16; gukora_mu_matsinda_umugerekashakiro++) if (이름길이[gukora_mu_matsinda_umugerekashakiro] == 항목수) {
            boolean 일치여부 = true; for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) if (변수이름[gukora_mu_matsinda_umugerekashakiro * 32 + 안쪽자리] != amakurushingiro_ARRAY[시작자리 + 안쪽자리]) 일치여부 = false;
            if (일치여부) { for (int 안쪽자리 = 0; 안쪽자리 < agaciro_uburebure[gukora_mu_matsinda_umugerekashakiro]; 안쪽자리++) 넣기(변수값[gukora_mu_matsinda_umugerekashakiro * 256 + 안쪽자리]); return; }
        }
    }
    static boolean Ijambo_agaciro(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = ihuriro[중첩깊이 * 128 + 낱말번호], 끝자리 = 끝[중첩깊이 * 128 + 낱말번호], 기준자리 = 중첩깊이 * 4096, 따옴표 = 0;
        if (읽는자리 < 끝자리 && Inkomoko[기준자리 + 읽는자리] == '~' && (읽는자리 + 1 == 끝자리 || Inkomoko[기준자리 + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < 끝자리) {
            int 문자값 = Inkomoko[기준자리 + 읽는자리++];
            if (문자값 == 따옴표) { 따옴표 = 0; continue; }
            if (따옴표 == 0 && (문자값 == 39 || 문자값 == 34)) { 따옴표 = 문자값; continue; }
            if (문자값 == '\\' && 따옴표 != 39) { int 다음자리 = Inkomoko[기준자리 + 읽는자리++]; if (따옴표 == 34 && 다음자리 != '$' && 다음자리 != '"' && 다음자리 != '\\') 넣기('\\'); 넣기(다음자리); continue; }
            if (문자값 == '$' && 따옴표 != 39 && 읽는자리 < 끝자리) {
                boolean 중괄호자리 = Inkomoko[기준자리 + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < 끝자리 && Inkomoko[기준자리 + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < 끝자리 && 이름뒤(Inkomoko[기준자리 + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == 끝자리 || Inkomoko[기준자리 + 읽는자리] != '}')) { IKOSA("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                변수(Inkomoko, 기준자리 + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(문자값);
        }
        return !umugereka_ikosa;
    }
    static int 환경설정(int ingingo_umugerekashakiro, boolean gukuramo) {
        int mu_gace_Itangira = 명령해석기.시작점[ingingo_umugerekashakiro], 끝자리 = mu_gace_Itangira + 명령해석기.uburebure_agaciro[ingingo_umugerekashakiro], 같음자리 = mu_gace_Itangira;
        while (같음자리 < 끝자리 && 명령해석기.tike_agaciro[같음자리] != '=') 같음자리++;
        int 항목수 = 같음자리 - mu_gace_Itangira;
        if (항목수 < 1 || 항목수 > 31 || !izina_inyuguti(명령해석기.tike_agaciro[mu_gace_Itangira]) || !gukuramo && 같음자리 == 끝자리 || 끝자리 - 같음자리 - 1 > 255) return 2;
        for (int gukora_mu_matsinda_umugerekashakiro = mu_gace_Itangira; gukora_mu_matsinda_umugerekashakiro < 같음자리; gukora_mu_matsinda_umugerekashakiro++) if (!이름뒤(명령해석기.tike_agaciro[gukora_mu_matsinda_umugerekashakiro])) return 2;
        if (구간말(명령해석기.tike_agaciro, mu_gace_Itangira, 항목수, "PWD") || 구간말(명령해석기.tike_agaciro, mu_gace_Itangira, 항목수, "HOME")) return 2;
        int 찾은여부 = -1, 빈여부 = -1;
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 16; gukora_mu_matsinda_umugerekashakiro++) {
            if (이름길이[gukora_mu_matsinda_umugerekashakiro] == 0) 빈여부 = gukora_mu_matsinda_umugerekashakiro;
            if (이름길이[gukora_mu_matsinda_umugerekashakiro] != 항목수) continue;
            boolean 일치여부 = true; for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) if (변수이름[gukora_mu_matsinda_umugerekashakiro * 32 + 안쪽자리] != 명령해석기.tike_agaciro[mu_gace_Itangira + 안쪽자리]) 일치여부 = false;
            if (일치여부) 찾은여부 = gukora_mu_matsinda_umugerekashakiro;
        }
        if (gukuramo) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = 빈여부; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = 항목수; agaciro_uburebure[찾은여부] = 끝자리 - 같음자리 - 1;
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 항목수; gukora_mu_matsinda_umugerekashakiro++) 변수이름[찾은여부 * 32 + gukora_mu_matsinda_umugerekashakiro] = 명령해석기.tike_agaciro[mu_gace_Itangira + gukora_mu_matsinda_umugerekashakiro];
        for (int gukora_mu_matsinda_umugerekashakiro = 같음자리 + 1; gukora_mu_matsinda_umugerekashakiro < 끝자리; gukora_mu_matsinda_umugerekashakiro++) 변수값[찾은여부 * 256 + gukora_mu_matsinda_umugerekashakiro - 같음자리 - 1] = 명령해석기.tike_agaciro[gukora_mu_matsinda_umugerekashakiro];
        return 0;
    }
    static void 환경보기() {
        단말.kwandika("HOME=/\nPWD="); ububiko_Dosiye.현재쓰기(); 단말.문자(10);
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 16; gukora_mu_matsinda_umugerekashakiro++) if (이름길이[gukora_mu_matsinda_umugerekashakiro] > 0) {
            for (int 안쪽자리 = 0; 안쪽자리 < 이름길이[gukora_mu_matsinda_umugerekashakiro]; 안쪽자리++) 보드.직렬쓰기(변수이름[gukora_mu_matsinda_umugerekashakiro * 32 + 안쪽자리]); 단말.문자('=');
            for (int 안쪽자리 = 0; 안쪽자리 < agaciro_uburebure[gukora_mu_matsinda_umugerekashakiro]; 안쪽자리++) 보드.직렬쓰기(변수값[gukora_mu_matsinda_umugerekashakiro * 256 + 안쪽자리]); 단말.문자(10);
        }
    }
    static void gukora_ibwiriza(int[] amakurushingiro_ARRAY, int 시작변위, int 항목수, int 중첩깊이) {
        if (중첩깊이 >= 4 || 항목수 > 4096) { IKOSA("Icyo_wifuza 파일의 중첩 또는 umurongo uburebure_agaciro 제한을 넘었습니다"); return; }
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 항목수; gukora_mu_matsinda_umugerekashakiro++) Inkomoko[중첩깊이 * 4096 + gukora_mu_matsinda_umugerekashakiro] = amakurushingiro_ARRAY[시작변위 + gukora_mu_matsinda_umugerekashakiro];
        int 총수 = 읽기(항목수, 중첩깊이); if (총수 < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < 총수) {
            int itsinda_kurangiza = 읽는자리;
            while (itsinda_kurangiza < 총수 && (종류[중첩깊이 * 128 + itsinda_kurangiza] == 0 || 종류[중첩깊이 * 128 + itsinda_kurangiza] >= 4)) itsinda_kurangiza++;
            boolean gukora = 조건성립 == 1 || 조건성립 == 2 && imimerere_agaciro == 0 || 조건성립 == 3 && imimerere_agaciro != 0;
            if (gukora) {
                boolean 이전자리 = false;
                while (읽는자리 < itsinda_kurangiza) {
                    int 다음자리 = 읽는자리; while (다음자리 < itsinda_kurangiza && 종류[중첩깊이 * 128 + 다음자리] != 4) 다음자리++;
                    boolean Guhuza_Stream = 다음자리 < itsinda_kurangiza; int 입력쪽 = -1, 출력쪽 = -1, 출력방식 = 0;
                    명령해석기.토큰수 = 0; 쓴수 = 0; umugereka_ikosa = false;
                    for (int gukora_mu_matsinda_umugerekashakiro = 읽는자리; gukora_mu_matsinda_umugerekashakiro < 다음자리; gukora_mu_matsinda_umugerekashakiro++) {
                        int 자료종류 = 종류[중첩깊이 * 128 + gukora_mu_matsinda_umugerekashakiro];
                        if (자료종류 >= 5) { if (자료종류 == 7) { if (입력쪽 >= 0) { IKOSA("입력 전환이 겹쳤습니다"); return; } 입력쪽 = ++gukora_mu_matsinda_umugerekashakiro; } else { if (출력쪽 >= 0) { IKOSA("출력 전환이 겹쳤습니다"); return; } 출력쪽 = ++gukora_mu_matsinda_umugerekashakiro; 출력방식 = 자료종류; } continue; }
                        if (명령해석기.토큰수 == 32) { IKOSA("인수가 너무 많습니다"); return; }
                        int ingingo_umugerekashakiro = 명령해석기.토큰수++; 명령해석기.시작점[ingingo_umugerekashakiro] = 쓴수;
                        if (!Ijambo_agaciro(gukora_mu_matsinda_umugerekashakiro, 중첩깊이)) return;
                        명령해석기.uburebure_agaciro[ingingo_umugerekashakiro] = 쓴수 - 명령해석기.시작점[ingingo_umugerekashakiro];
                    }
                    연결중 = 이전자리 || Guhuza_Stream || 입력쪽 >= 0 || 출력쪽 >= 0;
                    if (연결중 && (명령해석기.같음(0, "vi") || 명령해석기.같음(0, "edit") || 명령해석기.같음(0, "load") || 명령해석기.같음(0, "gui") || 명령해석기.같음(0, "terminal") || 명령해석기.같음(0, "sh") || 명령해석기.같음(0, "source"))) { IKOSA("interfacebikorana 명령과 Icyo_wifuza 파일은 I_O 전환이나 Stream_agaciro 연결에 쓸 수 없습니다"); return; }
                    셸입출력.ihuriro(이전자리, Guhuza_Stream);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int 항목자리 = 입출력바꿈 == 0 ? 입력쪽 : 출력쪽; if (항목자리 < 0) continue;
                        int 시작자리 = 쓴수; if (!Ijambo_agaciro(항목자리, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = ububiko_Dosiye.inzira_Itangira(쓴수 - 시작자리);
                        for (int 안쪽자리 = 시작자리; 처리값 >= 0 && 안쪽자리 < 쓴수; 안쪽자리++) 처리값 = ububiko_Dosiye.inzira_bayiti(안쪽자리 - 시작자리, 명령해석기.tike_agaciro[안쪽자리]);
                        if (처리값 >= 0) 처리값 = ububiko_Dosiye.Gufungura(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); 명령해석기.IKOSA(처리값); imimerere_agaciro = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.입력파일 = 처리값; else 셸입출력.dosiye_yasohotse = 처리값;
                    }
                    셸입출력.Kwemerera_interfacebikorana = 중첩깊이 == 0 && 읽는자리 == 0 && 다음자리 == 총수;
                    깊이 = 중첩깊이; 명령해석기.결과 = 0; 보드.입출력전환(1);
                    명령해석기.Icyo_wifuza();
                    보드.터미널(3);
                    int 반환값 = 명령해석기.결과, Stream_ikosa = 셸입출력.kudakora_agaciro;
                    셸입출력.끝(); 연결중 = false;
                    imimerere_agaciro = Stream_ikosa < 0 ? 1 : 반환값;
                    if (Stream_ikosa < 0) { 명령해석기.IKOSA(Stream_ikosa); return; }
                    if (sikiributi_kurangiza || 반환값 == -1005) return;
                    이전자리 = true; 읽는자리 = 다음자리 + 1;
                }
            }
            if (itsinda_kurangiza < 총수) 조건성립 = 종류[중첩깊이 * 128 + itsinda_kurangiza];
            읽는자리 = itsinda_kurangiza + 1;
        }
    }
    static void gukora_dosiye() {
        if (명령해석기.토큰수 != 2 || 깊이 >= 3) { 명령해석기.결과 = 2; 단말.kwandika("사용법: sh Idosiye (중첩 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = 명령해석기.Inzira(1); if (처리값 >= 0) 처리값 = ububiko_Dosiye.Gufungura(0);
        if (처리값 < 0) { 명령해석기.IKOSA(처리값); return; }
        int 항목수 = 0, bayiti_amakurushingiro;
        while ((bayiti_amakurushingiro = ububiko_Dosiye.읽기(처리값)) != 256 && bayiti_amakurushingiro >= 0 && 항목수 < 16384) sikiributi_agaciro[중첩깊이 * 16384 + 항목수++] = bayiti_amakurushingiro;
        ububiko_Dosiye.Gufunga(처리값); 보드.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < 항목수 && !sikiributi_kurangiza;) {
            int 끝자리 = 읽는자리; while (끝자리 < 항목수 && sikiributi_agaciro[중첩깊이 * 16384 + 끝자리] != 10) 끝자리++;
            int 유효길이 = 끝자리 - 읽는자리; if (유효길이 > 0 && sikiributi_agaciro[중첩깊이 * 16384 + 끝자리 - 1] == 13) 유효길이--;
            gukora_ibwiriza(sikiributi_agaciro, 중첩깊이 * 16384 + 읽는자리, 유효길이, 중첩깊이); 읽는자리 = 끝자리 + 1;
        }
        명령해석기.결과 = imimerere_agaciro; sikiributi_kurangiza = false; 깊이 = 중첩깊이 - 1;
    }
}
