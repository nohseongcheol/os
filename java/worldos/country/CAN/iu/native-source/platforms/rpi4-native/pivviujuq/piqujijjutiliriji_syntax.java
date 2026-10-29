// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 ilaliujjarvilik piqujijjutiliriji 문법. 파이프는 순차 실행, 환경은 같은 셸에서 공유한다. */
public final class piqujijjutiliriji_syntax {
    static int[] pivviujuq = new int[4 * 4096], 종류 = new int[4 * 128], 시작 = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] 변수이름 = new int[16 * 32], 변수값 = new int[16 * 256], 이름길이 = new int[16], atuutilik_takininga = new int[16];
    static int[] pilirijjutiralaaq_atuutilik = new int[4 * 16384];
    static int qanuilinganiq_atuutilik, 깊이, 쓴수;
    static boolean 연결중, pilirijjutiralaaq_isulittuq, uigu_tammarniq;
    static boolean atiq_immikkuuqtuq(int immikkuuqtumut_nalunaikkut) { return immikkuuqtumut_nalunaikkut >= 'a' && immikkuuqtumut_nalunaikkut <= 'z' || immikkuuqtumut_nalunaikkut >= 'A' && immikkuuqtumut_nalunaikkut <= 'Z' || immikkuuqtumut_nalunaikkut == '_' || immikkuuqtumut_nalunaikkut >= 128; }
    static boolean 이름뒤(int immikkuuqtumut_nalunaikkut) { return atiq_immikkuuqtuq(immikkuuqtumut_nalunaikkut) || immikkuuqtumut_nalunaikkut >= '0' && immikkuuqtumut_nalunaikkut <= '9'; }
    static void tammarniq(String titiqqaq) { 보드.입출력전환(0); 단말.titiraq("piqujijjut agguqtuut_atuutilik: "); 단말.titiraq(titiqqaq); 단말.문자(10); qanuilinganiq_atuutilik = 2; }
    static int 읽기(int 항목수, int 중첩깊이) {
        int 현재자리 = 0, 총수 = 0, 기준자리 = 중첩깊이 * 4096, 특수문자 = 중첩깊이 * 128;
        while (현재자리 < 항목수) {
            while (현재자리 < 항목수 && (pivviujuq[기준자리 + 현재자리] == 32 || pivviujuq[기준자리 + 현재자리] == 9)) 현재자리++;
            if (현재자리 == 항목수 || pivviujuq[기준자리 + 현재자리] == '#') break;
            if (총수 == 128) { tammarniq("낱말이 너무 많습니다"); return -1; }
            int 시작자리 = 현재자리, immikkuuqtumut_nalunaikkut = pivviujuq[기준자리 + 현재자리], 자료종류 = 0;
            if (immikkuuqtumut_nalunaikkut == ';') { 자료종류 = 1; 현재자리++; }
            else if (immikkuuqtumut_nalunaikkut == '&') { if (현재자리 + 1 >= 항목수 || pivviujuq[기준자리 + 현재자리 + 1] != '&') { tammarniq("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } 자료종류 = 2; 현재자리 += 2; }
            else if (immikkuuqtumut_nalunaikkut == '|') { 현재자리++; 자료종류 = 현재자리 < 항목수 && pivviujuq[기준자리 + 현재자리] == '|' ? 3 : 4; if (자료종류 == 3) 현재자리++; }
            else if (immikkuuqtumut_nalunaikkut == '>') { 현재자리++; 자료종류 = 현재자리 < 항목수 && pivviujuq[기준자리 + 현재자리] == '>' ? 6 : 5; if (자료종류 == 6) 현재자리++; }
            else if (immikkuuqtumut_nalunaikkut == '<') { 자료종류 = 7; 현재자리++; }
            else {
                int 따옴표 = 0;
                while (현재자리 < 항목수) {
                    immikkuuqtumut_nalunaikkut = pivviujuq[기준자리 + 현재자리];
                    if (immikkuuqtumut_nalunaikkut == '`' && 따옴표 != 39 || immikkuuqtumut_nalunaikkut == '$' && 따옴표 != 39 && 현재자리 + 1 < 항목수 && pivviujuq[기준자리 + 현재자리 + 1] == '(') { tammarniq("piqujijjut 결과 치환은 지원하지 않습니다"); return -1; }
                    if (immikkuuqtumut_nalunaikkut == '\\' && 따옴표 != 39) { if (++현재자리 == 항목수) { tammarniq("titikutaak 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } 현재자리++; continue; }
                    if (immikkuuqtumut_nalunaikkut == 따옴표) { 따옴표 = 0; 현재자리++; continue; }
                    if (따옴표 == 0 && (immikkuuqtumut_nalunaikkut == 39 || immikkuuqtumut_nalunaikkut == 34)) { 따옴표 = immikkuuqtumut_nalunaikkut; 현재자리++; continue; }
                    if (따옴표 == 0 && (immikkuuqtumut_nalunaikkut == 32 || immikkuuqtumut_nalunaikkut == 9 || immikkuuqtumut_nalunaikkut == ';' || immikkuuqtumut_nalunaikkut == '&' || immikkuuqtumut_nalunaikkut == '|' || immikkuuqtumut_nalunaikkut == '<' || immikkuuqtumut_nalunaikkut == '>')) break;
                    현재자리++;
                }
                if (따옴표 != 0) { tammarniq("따옴표가 닫히지 않았습니다"); return -1; }
                if (현재자리 < 항목수 && (pivviujuq[기준자리 + 현재자리] == '>' || pivviujuq[기준자리 + 현재자리] == '<')) {
                    boolean 수치 = 현재자리 > 시작자리;
                    for (int piliqqittaajuq_nalunaiqsimavik = 시작자리; piliqqittaajuq_nalunaiqsimavik < 현재자리; piliqqittaajuq_nalunaiqsimavik++) if (pivviujuq[기준자리 + piliqqittaajuq_nalunaiqsimavik] < '0' || pivviujuq[기준자리 + piliqqittaajuq_nalunaiqsimavik] > '9') 수치 = false;
                    if (수치) { tammarniq("번호를 지정한 ini 서술자 I_O 전환은 지원하지 않습니다"); return -1; }
                }
            }
            종류[특수문자 + 총수] = 자료종류; 시작[특수문자 + 총수] = 시작자리; 끝[특수문자 + 총수] = 현재자리; 총수++;
        }
        boolean 낱말 = false;
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 총수; piliqqittaajuq_nalunaiqsimavik++) {
            int 임시값 = 종류[특수문자 + piliqqittaajuq_nalunaiqsimavik];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++piliqqittaajuq_nalunaiqsimavik == 총수 || 종류[특수문자 + piliqqittaajuq_nalunaiqsimavik] != 0) { tammarniq("I_O 전환에 ini 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || piliqqittaajuq_nalunaiqsimavik == 총수 - 1 && 임시값 != 1) { tammarniq("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (총수 > 0 && !낱말 && 종류[특수문자 + 총수 - 1] != 1) { tammarniq("명령이 빠졌습니다"); return -1; }
        return 총수;
    }
    static boolean 구간말(int[] titiqqat_array, int tamaani_pigiarli, int 항목수, String 문자위치) {
        if (항목수 != 문자위치.length()) return false; for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 항목수; piliqqittaajuq_nalunaiqsimavik++) if (titiqqat_array[tamaani_pigiarli + piliqqittaajuq_nalunaiqsimavik] != 문자위치.charAt(piliqqittaajuq_nalunaiqsimavik)) return false; return true;
    }
    static void 넣기(int byte_titiqqat) {
        if (쓴수 >= 명령해석기.토큰.length) { if (!uigu_tammarniq) tammarniq("변수를 펼친 명령이 너무 깁니다"); uigu_tammarniq = true; return; }
        명령해석기.토큰[쓴수++] = byte_titiqqat;
    }
    static void 변수(int[] titiqqat_array, int 시작자리, int 항목수) {
        if (구간말(titiqqat_array, 시작자리, 항목수, "PWD")) { 넣기('/'); for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 기억파일.현재길이; piliqqittaajuq_nalunaiqsimavik++) 넣기(기억파일.현재[piliqqittaajuq_nalunaiqsimavik]); return; }
        if (구간말(titiqqat_array, 시작자리, 항목수, "HOME")) { 넣기('/'); return; }
        if (구간말(titiqqat_array, 시작자리, 항목수, "?")) {
            int titiqqat_atuutilik = qanuilinganiq_atuutilik, 자릿값 = 100; boolean 시작여부 = false;
            while (자릿값 > 0) { int 뒷값 = titiqqat_atuutilik / 자릿값; if (뒷값 != 0 || 시작여부 || 자릿값 == 1) { 넣기('0' + 뒷값); 시작여부 = true; } titiqqat_atuutilik %= 자릿값; 자릿값 /= 10; } return;
        }
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 16; piliqqittaajuq_nalunaiqsimavik++) if (이름길이[piliqqittaajuq_nalunaiqsimavik] == 항목수) {
            boolean 일치여부 = true; for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) if (변수이름[piliqqittaajuq_nalunaiqsimavik * 32 + 안쪽자리] != titiqqat_array[시작자리 + 안쪽자리]) 일치여부 = false;
            if (일치여부) { for (int 안쪽자리 = 0; 안쪽자리 < atuutilik_takininga[piliqqittaajuq_nalunaiqsimavik]; 안쪽자리++) 넣기(변수값[piliqqittaajuq_nalunaiqsimavik * 256 + 안쪽자리]); return; }
        }
    }
    static boolean 단어(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = 시작[중첩깊이 * 128 + 낱말번호], 끝자리 = 끝[중첩깊이 * 128 + 낱말번호], 기준자리 = 중첩깊이 * 4096, 따옴표 = 0;
        if (읽는자리 < 끝자리 && pivviujuq[기준자리 + 읽는자리] == '~' && (읽는자리 + 1 == 끝자리 || pivviujuq[기준자리 + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < 끝자리) {
            int immikkuuqtumut_nalunaikkut = pivviujuq[기준자리 + 읽는자리++];
            if (immikkuuqtumut_nalunaikkut == 따옴표) { 따옴표 = 0; continue; }
            if (따옴표 == 0 && (immikkuuqtumut_nalunaikkut == 39 || immikkuuqtumut_nalunaikkut == 34)) { 따옴표 = immikkuuqtumut_nalunaikkut; continue; }
            if (immikkuuqtumut_nalunaikkut == '\\' && 따옴표 != 39) { int 다음자리 = pivviujuq[기준자리 + 읽는자리++]; if (따옴표 == 34 && 다음자리 != '$' && 다음자리 != '"' && 다음자리 != '\\') 넣기('\\'); 넣기(다음자리); continue; }
            if (immikkuuqtumut_nalunaikkut == '$' && 따옴표 != 39 && 읽는자리 < 끝자리) {
                boolean 중괄호자리 = pivviujuq[기준자리 + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < 끝자리 && pivviujuq[기준자리 + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < 끝자리 && 이름뒤(pivviujuq[기준자리 + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == 끝자리 || pivviujuq[기준자리 + 읽는자리] != '}')) { tammarniq("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                변수(pivviujuq, 기준자리 + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(immikkuuqtumut_nalunaikkut);
        }
        return !uigu_tammarniq;
    }
    static int 환경설정(int aturniqarnirainiq_nalunaiqsimavik, boolean sanirvalli) {
        int tamaani_pigiarli = 명령해석기.시작점[aturniqarnirainiq_nalunaiqsimavik], 끝자리 = tamaani_pigiarli + 명령해석기.takininga_atuutilik[aturniqarnirainiq_nalunaiqsimavik], 같음자리 = tamaani_pigiarli;
        while (같음자리 < 끝자리 && 명령해석기.토큰[같음자리] != '=') 같음자리++;
        int 항목수 = 같음자리 - tamaani_pigiarli;
        if (항목수 < 1 || 항목수 > 31 || !atiq_immikkuuqtuq(명령해석기.토큰[tamaani_pigiarli]) || !sanirvalli && 같음자리 == 끝자리 || 끝자리 - 같음자리 - 1 > 255) return 2;
        for (int piliqqittaajuq_nalunaiqsimavik = tamaani_pigiarli; piliqqittaajuq_nalunaiqsimavik < 같음자리; piliqqittaajuq_nalunaiqsimavik++) if (!이름뒤(명령해석기.토큰[piliqqittaajuq_nalunaiqsimavik])) return 2;
        if (구간말(명령해석기.토큰, tamaani_pigiarli, 항목수, "PWD") || 구간말(명령해석기.토큰, tamaani_pigiarli, 항목수, "HOME")) return 2;
        int 찾은여부 = -1, 빈여부 = -1;
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 16; piliqqittaajuq_nalunaiqsimavik++) {
            if (이름길이[piliqqittaajuq_nalunaiqsimavik] == 0) 빈여부 = piliqqittaajuq_nalunaiqsimavik;
            if (이름길이[piliqqittaajuq_nalunaiqsimavik] != 항목수) continue;
            boolean 일치여부 = true; for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) if (변수이름[piliqqittaajuq_nalunaiqsimavik * 32 + 안쪽자리] != 명령해석기.토큰[tamaani_pigiarli + 안쪽자리]) 일치여부 = false;
            if (일치여부) 찾은여부 = piliqqittaajuq_nalunaiqsimavik;
        }
        if (sanirvalli) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = 빈여부; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = 항목수; atuutilik_takininga[찾은여부] = 끝자리 - 같음자리 - 1;
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 항목수; piliqqittaajuq_nalunaiqsimavik++) 변수이름[찾은여부 * 32 + piliqqittaajuq_nalunaiqsimavik] = 명령해석기.토큰[tamaani_pigiarli + piliqqittaajuq_nalunaiqsimavik];
        for (int piliqqittaajuq_nalunaiqsimavik = 같음자리 + 1; piliqqittaajuq_nalunaiqsimavik < 끝자리; piliqqittaajuq_nalunaiqsimavik++) 변수값[찾은여부 * 256 + piliqqittaajuq_nalunaiqsimavik - 같음자리 - 1] = 명령해석기.토큰[piliqqittaajuq_nalunaiqsimavik];
        return 0;
    }
    static void 환경보기() {
        단말.titiraq("HOME=/\nPWD="); 기억파일.현재쓰기(); 단말.문자(10);
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 16; piliqqittaajuq_nalunaiqsimavik++) if (이름길이[piliqqittaajuq_nalunaiqsimavik] > 0) {
            for (int 안쪽자리 = 0; 안쪽자리 < 이름길이[piliqqittaajuq_nalunaiqsimavik]; 안쪽자리++) 보드.직렬쓰기(변수이름[piliqqittaajuq_nalunaiqsimavik * 32 + 안쪽자리]); 단말.문자('=');
            for (int 안쪽자리 = 0; 안쪽자리 < atuutilik_takininga[piliqqittaajuq_nalunaiqsimavik]; 안쪽자리++) 보드.직렬쓰기(변수값[piliqqittaajuq_nalunaiqsimavik * 256 + 안쪽자리]); 단말.문자(10);
        }
    }
    static void 실행(int[] titiqqat_array, int 시작변위, int 항목수, int 중첩깊이) {
        if (중첩깊이 >= 4 || 항목수 > 4096) { tammarniq("piqujijjut 파일의 중첩 또는 titikutaak takininga_atuutilik 제한을 넘었습니다"); return; }
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 항목수; piliqqittaajuq_nalunaiqsimavik++) pivviujuq[중첩깊이 * 4096 + piliqqittaajuq_nalunaiqsimavik] = titiqqat_array[시작변위 + piliqqittaajuq_nalunaiqsimavik];
        int 총수 = 읽기(항목수, 중첩깊이); if (총수 < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < 총수) {
            int katinngajut_isulittuq = 읽는자리;
            while (katinngajut_isulittuq < 총수 && (종류[중첩깊이 * 128 + katinngajut_isulittuq] == 0 || 종류[중첩깊이 * 128 + katinngajut_isulittuq] >= 4)) katinngajut_isulittuq++;
            boolean 실행여부 = 조건성립 == 1 || 조건성립 == 2 && qanuilinganiq_atuutilik == 0 || 조건성립 == 3 && qanuilinganiq_atuutilik != 0;
            if (실행여부) {
                boolean 이전자리 = false;
                while (읽는자리 < katinngajut_isulittuq) {
                    int 다음자리 = 읽는자리; while (다음자리 < katinngajut_isulittuq && 종류[중첩깊이 * 128 + 다음자리] != 4) 다음자리++;
                    boolean kasurli_ingirrania_aulataup = 다음자리 < katinngajut_isulittuq; int 입력쪽 = -1, 출력쪽 = -1, 출력방식 = 0;
                    명령해석기.토큰수 = 0; 쓴수 = 0; uigu_tammarniq = false;
                    for (int piliqqittaajuq_nalunaiqsimavik = 읽는자리; piliqqittaajuq_nalunaiqsimavik < 다음자리; piliqqittaajuq_nalunaiqsimavik++) {
                        int 자료종류 = 종류[중첩깊이 * 128 + piliqqittaajuq_nalunaiqsimavik];
                        if (자료종류 >= 5) { if (자료종류 == 7) { if (입력쪽 >= 0) { tammarniq("입력 전환이 겹쳤습니다"); return; } 입력쪽 = ++piliqqittaajuq_nalunaiqsimavik; } else { if (출력쪽 >= 0) { tammarniq("출력 전환이 겹쳤습니다"); return; } 출력쪽 = ++piliqqittaajuq_nalunaiqsimavik; 출력방식 = 자료종류; } continue; }
                        if (명령해석기.토큰수 == 32) { tammarniq("인수가 너무 많습니다"); return; }
                        int aturniqarnirainiq_nalunaiqsimavik = 명령해석기.토큰수++; 명령해석기.시작점[aturniqarnirainiq_nalunaiqsimavik] = 쓴수;
                        if (!단어(piliqqittaajuq_nalunaiqsimavik, 중첩깊이)) return;
                        명령해석기.takininga_atuutilik[aturniqarnirainiq_nalunaiqsimavik] = 쓴수 - 명령해석기.시작점[aturniqarnirainiq_nalunaiqsimavik];
                    }
                    연결중 = 이전자리 || kasurli_ingirrania_aulataup || 입력쪽 >= 0 || 출력쪽 >= 0;
                    if (연결중 && (명령해석기.같음(0, "vi") || 명령해석기.같음(0, "edit") || 명령해석기.같음(0, "load") || 명령해석기.같음(0, "gui") || 명령해석기.같음(0, "terminal") || 명령해석기.같음(0, "sh") || 명령해석기.같음(0, "source"))) { tammarniq("ilaliujjarvilik 명령과 piqujijjut 파일은 I_O 전환이나 ingirrania_aulataup_atuutilik 연결에 쓸 수 없습니다"); return; }
                    셸입출력.시작(이전자리, kasurli_ingirrania_aulataup);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int 항목자리 = 입출력바꿈 == 0 ? 입력쪽 : 출력쪽; if (항목자리 < 0) continue;
                        int 시작자리 = 쓴수; if (!단어(항목자리, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = 기억파일.aqqut_pigiarli(쓴수 - 시작자리);
                        for (int 안쪽자리 = 시작자리; 처리값 >= 0 && 안쪽자리 < 쓴수; 안쪽자리++) 처리값 = 기억파일.aqqut_byte(안쪽자리 - 시작자리, 명령해석기.토큰[안쪽자리]);
                        if (처리값 >= 0) 처리값 = 기억파일.matuirli(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); 명령해석기.tammarniq(처리값); qanuilinganiq_atuutilik = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.입력파일 = 처리값; else 셸입출력.출력파일 = 처리값;
                    }
                    셸입출력.Pijunnaqtilli_ilaliujjarvilik = 중첩깊이 == 0 && 읽는자리 == 0 && 다음자리 == 총수;
                    깊이 = 중첩깊이; 명령해석기.결과 = 0; 보드.입출력전환(1);
                    명령해석기.piqujijjut();
                    보드.터미널(3);
                    int 반환값 = 명령해석기.결과, ingirrania_aulataup_tammarniq = 셸입출력.itigaqtuq_atuutilik;
                    셸입출력.끝(); 연결중 = false;
                    qanuilinganiq_atuutilik = ingirrania_aulataup_tammarniq < 0 ? 1 : 반환값;
                    if (ingirrania_aulataup_tammarniq < 0) { 명령해석기.tammarniq(ingirrania_aulataup_tammarniq); return; }
                    if (pilirijjutiralaaq_isulittuq || 반환값 == -1005) return;
                    이전자리 = true; 읽는자리 = 다음자리 + 1;
                }
            }
            if (katinngajut_isulittuq < 총수) 조건성립 = 종류[중첩깊이 * 128 + katinngajut_isulittuq];
            읽는자리 = katinngajut_isulittuq + 1;
        }
    }
    static void 파일실행() {
        if (명령해석기.토큰수 != 2 || 깊이 >= 3) { 명령해석기.결과 = 2; 단말.titiraq("사용법: sh ini (중첩 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = 명령해석기.aqqut(1); if (처리값 >= 0) 처리값 = 기억파일.matuirli(0);
        if (처리값 < 0) { 명령해석기.tammarniq(처리값); return; }
        int 항목수 = 0, byte_titiqqat;
        while ((byte_titiqqat = 기억파일.읽기(처리값)) != 256 && byte_titiqqat >= 0 && 항목수 < 16384) pilirijjutiralaaq_atuutilik[중첩깊이 * 16384 + 항목수++] = byte_titiqqat;
        기억파일.matuli(처리값); 보드.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < 항목수 && !pilirijjutiralaaq_isulittuq;) {
            int 끝자리 = 읽는자리; while (끝자리 < 항목수 && pilirijjutiralaaq_atuutilik[중첩깊이 * 16384 + 끝자리] != 10) 끝자리++;
            int 유효길이 = 끝자리 - 읽는자리; if (유효길이 > 0 && pilirijjutiralaaq_atuutilik[중첩깊이 * 16384 + 끝자리 - 1] == 13) 유효길이--;
            실행(pilirijjutiralaaq_atuutilik, 중첩깊이 * 16384 + 읽는자리, 유효길이, 중첩깊이); 읽는자리 = 끝자리 + 1;
        }
        명령해석기.결과 = qanuilinganiq_atuutilik; pilirijjutiralaaq_isulittuq = false; 깊이 = 중첩깊이 - 1;
    }
}
