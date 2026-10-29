// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 jokkondirtoo laalagal 문법. 파이프는 순차 실행, 환경은 같은 셸에서 공유한다. */
public final class 셸문법 {
    static int[] sewnde = new int[4 * 4096], 종류 = new int[4 * 128], huutoraade = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] 변수이름 = new int[16 * 32], 변수값 = new int[16 * 256], 이름길이 = new int[16], njaru_njuuteendi = new int[16];
    static int[] eskript_njaru = new int[4 * 16384];
    static int ngonka_njaru, 깊이, 쓴수;
    static boolean 연결중, eskript_taƴde, timmital_juumre;
    static boolean innde_alkulal(int 문자값) { return 문자값 >= 'a' && 문자값 <= 'z' || 문자값 >= 'A' && 문자값 <= 'Z' || 문자값 == '_' || 문자값 >= 128; }
    static boolean 이름뒤(int 문자값) { return innde_alkulal(문자값) || 문자값 >= '0' && 문자값 <= '9'; }
    static void juumre(String binndi) { 보드.입출력전환(0); 단말.winndude("ginol 해석: "); 단말.winndude(binndi); 단말.문자(10); ngonka_njaru = 2; }
    static int 읽기(int 항목수, int 중첩깊이) {
        int 현재자리 = 0, 총수 = 0, 기준자리 = 중첩깊이 * 4096, 특수문자 = 중첩깊이 * 128;
        while (현재자리 < 항목수) {
            while (현재자리 < 항목수 && (sewnde[기준자리 + 현재자리] == 32 || sewnde[기준자리 + 현재자리] == 9)) 현재자리++;
            if (현재자리 == 항목수 || sewnde[기준자리 + 현재자리] == '#') break;
            if (총수 == 128) { juumre("낱말이 너무 많습니다"); return -1; }
            int 시작자리 = 현재자리, 문자값 = sewnde[기준자리 + 현재자리], 자료종류 = 0;
            if (문자값 == ';') { 자료종류 = 1; 현재자리++; }
            else if (문자값 == '&') { if (현재자리 + 1 >= 항목수 || sewnde[기준자리 + 현재자리 + 1] != '&') { juumre("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } 자료종류 = 2; 현재자리 += 2; }
            else if (문자값 == '|') { 현재자리++; 자료종류 = 현재자리 < 항목수 && sewnde[기준자리 + 현재자리] == '|' ? 3 : 4; if (자료종류 == 3) 현재자리++; }
            else if (문자값 == '>') { 현재자리++; 자료종류 = 현재자리 < 항목수 && sewnde[기준자리 + 현재자리] == '>' ? 6 : 5; if (자료종류 == 6) 현재자리++; }
            else if (문자값 == '<') { 자료종류 = 7; 현재자리++; }
            else {
                int 따옴표 = 0;
                while (현재자리 < 항목수) {
                    문자값 = sewnde[기준자리 + 현재자리];
                    if (문자값 == '`' && 따옴표 != 39 || 문자값 == '$' && 따옴표 != 39 && 현재자리 + 1 < 항목수 && sewnde[기준자리 + 현재자리 + 1] == '(') { juumre("ginol 결과 치환은 지원하지 않습니다"); return -1; }
                    if (문자값 == '\\' && 따옴표 != 39) { if (++현재자리 == 항목수) { juumre("diidol 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } 현재자리++; continue; }
                    if (문자값 == 따옴표) { 따옴표 = 0; 현재자리++; continue; }
                    if (따옴표 == 0 && (문자값 == 39 || 문자값 == 34)) { 따옴표 = 문자값; 현재자리++; continue; }
                    if (따옴표 == 0 && (문자값 == 32 || 문자값 == 9 || 문자값 == ';' || 문자값 == '&' || 문자값 == '|' || 문자값 == '<' || 문자값 == '>')) break;
                    현재자리++;
                }
                if (따옴표 != 0) { juumre("따옴표가 닫히지 않았습니다"); return -1; }
                if (현재자리 < 항목수 && (sewnde[기준자리 + 현재자리] == '>' || sewnde[기준자리 + 현재자리] == '<')) {
                    boolean 수치 = 현재자리 > 시작자리;
                    for (int kowal_joopirdu = 시작자리; kowal_joopirdu < 현재자리; kowal_joopirdu++) if (sewnde[기준자리 + kowal_joopirdu] < '0' || sewnde[기준자리 + kowal_joopirdu] > '9') 수치 = false;
                    if (수치) { juumre("번호를 지정한 fiilde 서술자 I_O 전환은 지원하지 않습니다"); return -1; }
                }
            }
            종류[특수문자 + 총수] = 자료종류; huutoraade[특수문자 + 총수] = 시작자리; 끝[특수문자 + 총수] = 현재자리; 총수++;
        }
        boolean 낱말 = false;
        for (int kowal_joopirdu = 0; kowal_joopirdu < 총수; kowal_joopirdu++) {
            int 임시값 = 종류[특수문자 + kowal_joopirdu];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++kowal_joopirdu == 총수 || 종류[특수문자 + kowal_joopirdu] != 0) { juumre("I_O 전환에 fiilde 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || kowal_joopirdu == 총수 - 1 && 임시값 != 1) { juumre("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (총수 > 0 && !낱말 && 종류[특수문자 + 총수 - 1] != 1) { juumre("명령이 빠졌습니다"); return -1; }
        return 총수;
    }
    static boolean 구간말(int[] 자료배열, int nokkuwal_huɓɓude, int 항목수, String 문자위치) {
        if (항목수 != 문자위치.length()) return false; for (int kowal_joopirdu = 0; kowal_joopirdu < 항목수; kowal_joopirdu++) if (자료배열[nokkuwal_huɓɓude + kowal_joopirdu] != 문자위치.charAt(kowal_joopirdu)) return false; return true;
    }
    static void 넣기(int oktee_keɓe) {
        if (쓴수 >= 명령해석기.토큰.length) { if (!timmital_juumre) juumre("변수를 펼친 명령이 너무 깁니다"); timmital_juumre = true; return; }
        명령해석기.토큰[쓴수++] = oktee_keɓe;
    }
    static void 변수(int[] 자료배열, int 시작자리, int 항목수) {
        if (구간말(자료배열, 시작자리, 항목수, "PWD")) { 넣기('/'); for (int kowal_joopirdu = 0; kowal_joopirdu < 기억파일.현재길이; kowal_joopirdu++) 넣기(기억파일.현재[kowal_joopirdu]); return; }
        if (구간말(자료배열, 시작자리, 항목수, "HOME")) { 넣기('/'); return; }
        if (구간말(자료배열, 시작자리, 항목수, "?")) {
            int keɓe_njaru = ngonka_njaru, 자릿값 = 100; boolean 시작여부 = false;
            while (자릿값 > 0) { int 뒷값 = keɓe_njaru / 자릿값; if (뒷값 != 0 || 시작여부 || 자릿값 == 1) { 넣기('0' + 뒷값); 시작여부 = true; } keɓe_njaru %= 자릿값; 자릿값 /= 10; } return;
        }
        for (int kowal_joopirdu = 0; kowal_joopirdu < 16; kowal_joopirdu++) if (이름길이[kowal_joopirdu] == 항목수) {
            boolean 일치여부 = true; for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) if (변수이름[kowal_joopirdu * 32 + 안쪽자리] != 자료배열[시작자리 + 안쪽자리]) 일치여부 = false;
            if (일치여부) { for (int 안쪽자리 = 0; 안쪽자리 < njaru_njuuteendi[kowal_joopirdu]; 안쪽자리++) 넣기(변수값[kowal_joopirdu * 256 + 안쪽자리]); return; }
        }
    }
    static boolean 단어(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = huutoraade[중첩깊이 * 128 + 낱말번호], 끝자리 = 끝[중첩깊이 * 128 + 낱말번호], 기준자리 = 중첩깊이 * 4096, 따옴표 = 0;
        if (읽는자리 < 끝자리 && sewnde[기준자리 + 읽는자리] == '~' && (읽는자리 + 1 == 끝자리 || sewnde[기준자리 + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < 끝자리) {
            int 문자값 = sewnde[기준자리 + 읽는자리++];
            if (문자값 == 따옴표) { 따옴표 = 0; continue; }
            if (따옴표 == 0 && (문자값 == 39 || 문자값 == 34)) { 따옴표 = 문자값; continue; }
            if (문자값 == '\\' && 따옴표 != 39) { int 다음자리 = sewnde[기준자리 + 읽는자리++]; if (따옴표 == 34 && 다음자리 != '$' && 다음자리 != '"' && 다음자리 != '\\') 넣기('\\'); 넣기(다음자리); continue; }
            if (문자값 == '$' && 따옴표 != 39 && 읽는자리 < 끝자리) {
                boolean 중괄호자리 = sewnde[기준자리 + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < 끝자리 && sewnde[기준자리 + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < 끝자리 && 이름뒤(sewnde[기준자리 + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == 끝자리 || sewnde[기준자리 + 읽는자리] != '}')) { juumre("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                변수(sewnde, 기준자리 + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(문자값);
        }
        return !timmital_juumre;
    }
    static int 환경설정(int hujja_joopirdu, boolean ittude) {
        int nokkuwal_huɓɓude = 명령해석기.시작점[hujja_joopirdu], 끝자리 = nokkuwal_huɓɓude + 명령해석기.njuuteendi_njaru[hujja_joopirdu], 같음자리 = nokkuwal_huɓɓude;
        while (같음자리 < 끝자리 && 명령해석기.토큰[같음자리] != '=') 같음자리++;
        int 항목수 = 같음자리 - nokkuwal_huɓɓude;
        if (항목수 < 1 || 항목수 > 31 || !innde_alkulal(명령해석기.토큰[nokkuwal_huɓɓude]) || !ittude && 같음자리 == 끝자리 || 끝자리 - 같음자리 - 1 > 255) return 2;
        for (int kowal_joopirdu = nokkuwal_huɓɓude; kowal_joopirdu < 같음자리; kowal_joopirdu++) if (!이름뒤(명령해석기.토큰[kowal_joopirdu])) return 2;
        if (구간말(명령해석기.토큰, nokkuwal_huɓɓude, 항목수, "PWD") || 구간말(명령해석기.토큰, nokkuwal_huɓɓude, 항목수, "HOME")) return 2;
        int 찾은여부 = -1, 빈여부 = -1;
        for (int kowal_joopirdu = 0; kowal_joopirdu < 16; kowal_joopirdu++) {
            if (이름길이[kowal_joopirdu] == 0) 빈여부 = kowal_joopirdu;
            if (이름길이[kowal_joopirdu] != 항목수) continue;
            boolean 일치여부 = true; for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) if (변수이름[kowal_joopirdu * 32 + 안쪽자리] != 명령해석기.토큰[nokkuwal_huɓɓude + 안쪽자리]) 일치여부 = false;
            if (일치여부) 찾은여부 = kowal_joopirdu;
        }
        if (ittude) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = 빈여부; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = 항목수; njaru_njuuteendi[찾은여부] = 끝자리 - 같음자리 - 1;
        for (int kowal_joopirdu = 0; kowal_joopirdu < 항목수; kowal_joopirdu++) 변수이름[찾은여부 * 32 + kowal_joopirdu] = 명령해석기.토큰[nokkuwal_huɓɓude + kowal_joopirdu];
        for (int kowal_joopirdu = 같음자리 + 1; kowal_joopirdu < 끝자리; kowal_joopirdu++) 변수값[찾은여부 * 256 + kowal_joopirdu - 같음자리 - 1] = 명령해석기.토큰[kowal_joopirdu];
        return 0;
    }
    static void 환경보기() {
        단말.winndude("HOME=/\nPWD="); 기억파일.현재쓰기(); 단말.문자(10);
        for (int kowal_joopirdu = 0; kowal_joopirdu < 16; kowal_joopirdu++) if (이름길이[kowal_joopirdu] > 0) {
            for (int 안쪽자리 = 0; 안쪽자리 < 이름길이[kowal_joopirdu]; 안쪽자리++) 보드.직렬쓰기(변수이름[kowal_joopirdu * 32 + 안쪽자리]); 단말.문자('=');
            for (int 안쪽자리 = 0; 안쪽자리 < njaru_njuuteendi[kowal_joopirdu]; 안쪽자리++) 보드.직렬쓰기(변수값[kowal_joopirdu * 256 + 안쪽자리]); 단말.문자(10);
        }
    }
    static void 실행(int[] 자료배열, int 시작변위, int 항목수, int 중첩깊이) {
        if (중첩깊이 >= 4 || 항목수 > 4096) { juumre("ginol 파일의 중첩 또는 diidol njuuteendi_njaru 제한을 넘었습니다"); return; }
        for (int kowal_joopirdu = 0; kowal_joopirdu < 항목수; kowal_joopirdu++) sewnde[중첩깊이 * 4096 + kowal_joopirdu] = 자료배열[시작변위 + kowal_joopirdu];
        int 총수 = 읽기(항목수, 중첩깊이); if (총수 < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < 총수) {
            int seto_taƴde = 읽는자리;
            while (seto_taƴde < 총수 && (종류[중첩깊이 * 128 + seto_taƴde] == 0 || 종류[중첩깊이 * 128 + seto_taƴde] >= 4)) seto_taƴde++;
            boolean 실행여부 = 조건성립 == 1 || 조건성립 == 2 && ngonka_njaru == 0 || 조건성립 == 3 && ngonka_njaru != 0;
            if (실행여부) {
                boolean 이전자리 = false;
                while (읽는자리 < seto_taƴde) {
                    int 다음자리 = 읽는자리; while (다음자리 < seto_taƴde && 종류[중첩깊이 * 128 + 다음자리] != 4) 다음자리++;
                    boolean seŋaade_waraango = 다음자리 < seto_taƴde; int 입력쪽 = -1, 출력쪽 = -1, 출력방식 = 0;
                    명령해석기.토큰수 = 0; 쓴수 = 0; timmital_juumre = false;
                    for (int kowal_joopirdu = 읽는자리; kowal_joopirdu < 다음자리; kowal_joopirdu++) {
                        int 자료종류 = 종류[중첩깊이 * 128 + kowal_joopirdu];
                        if (자료종류 >= 5) { if (자료종류 == 7) { if (입력쪽 >= 0) { juumre("입력 전환이 겹쳤습니다"); return; } 입력쪽 = ++kowal_joopirdu; } else { if (출력쪽 >= 0) { juumre("출력 전환이 겹쳤습니다"); return; } 출력쪽 = ++kowal_joopirdu; 출력방식 = 자료종류; } continue; }
                        if (명령해석기.토큰수 == 32) { juumre("인수가 너무 많습니다"); return; }
                        int hujja_joopirdu = 명령해석기.토큰수++; 명령해석기.시작점[hujja_joopirdu] = 쓴수;
                        if (!단어(kowal_joopirdu, 중첩깊이)) return;
                        명령해석기.njuuteendi_njaru[hujja_joopirdu] = 쓴수 - 명령해석기.시작점[hujja_joopirdu];
                    }
                    연결중 = 이전자리 || seŋaade_waraango || 입력쪽 >= 0 || 출력쪽 >= 0;
                    if (연결중 && (명령해석기.같음(0, "vi") || 명령해석기.같음(0, "edit") || 명령해석기.같음(0, "load") || 명령해석기.같음(0, "gui") || 명령해석기.같음(0, "terminal") || 명령해석기.같음(0, "sh") || 명령해석기.같음(0, "source"))) { juumre("jokkondirtoo 명령과 ginol 파일은 I_O 전환이나 waraango_njaru 연결에 쓸 수 없습니다"); return; }
                    셸입출력.huutoraade(이전자리, seŋaade_waraango);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int 항목자리 = 입출력바꿈 == 0 ? 입력쪽 : 출력쪽; if (항목자리 < 0) continue;
                        int 시작자리 = 쓴수; if (!단어(항목자리, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = 기억파일.laawol_huɓɓude(쓴수 - 시작자리);
                        for (int 안쪽자리 = 시작자리; 처리값 >= 0 && 안쪽자리 < 쓴수; 안쪽자리++) 처리값 = 기억파일.laawol_oktee(안쪽자리 - 시작자리, 명령해석기.토큰[안쪽자리]);
                        if (처리값 >= 0) 처리값 = 기억파일.udditde(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); 명령해석기.juumre(처리값); ngonka_njaru = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.입력파일 = 처리값; else 셸입출력.출력파일 = 처리값;
                    }
                    셸입출력.Wellit_jokkondirtoo = 중첩깊이 == 0 && 읽는자리 == 0 && 다음자리 == 총수;
                    깊이 = 중첩깊이; 명령해석기.결과 = 0; 보드.입출력전환(1);
                    명령해석기.ginol();
                    보드.터미널(3);
                    int 반환값 = 명령해석기.결과, waraango_juumre = 셸입출력.ella_njaru;
                    셸입출력.끝(); 연결중 = false;
                    ngonka_njaru = waraango_juumre < 0 ? 1 : 반환값;
                    if (waraango_juumre < 0) { 명령해석기.juumre(waraango_juumre); return; }
                    if (eskript_taƴde || 반환값 == -1005) return;
                    이전자리 = true; 읽는자리 = 다음자리 + 1;
                }
            }
            if (seto_taƴde < 총수) 조건성립 = 종류[중첩깊이 * 128 + seto_taƴde];
            읽는자리 = seto_taƴde + 1;
        }
    }
    static void 파일실행() {
        if (명령해석기.토큰수 != 2 || 깊이 >= 3) { 명령해석기.결과 = 2; 단말.winndude("사용법: sh fiilde (중첩 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = 명령해석기.laawol(1); if (처리값 >= 0) 처리값 = 기억파일.udditde(0);
        if (처리값 < 0) { 명령해석기.juumre(처리값); return; }
        int 항목수 = 0, oktee_keɓe;
        while ((oktee_keɓe = 기억파일.읽기(처리값)) != 256 && oktee_keɓe >= 0 && 항목수 < 16384) eskript_njaru[중첩깊이 * 16384 + 항목수++] = oktee_keɓe;
        기억파일.uddude(처리값); 보드.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < 항목수 && !eskript_taƴde;) {
            int 끝자리 = 읽는자리; while (끝자리 < 항목수 && eskript_njaru[중첩깊이 * 16384 + 끝자리] != 10) 끝자리++;
            int 유효길이 = 끝자리 - 읽는자리; if (유효길이 > 0 && eskript_njaru[중첩깊이 * 16384 + 끝자리 - 1] == 13) 유효길이--;
            실행(eskript_njaru, 중첩깊이 * 16384 + 읽는자리, 유효길이, 중첩깊이); 읽는자리 = 끝자리 + 1;
        }
        명령해석기.결과 = ngonka_njaru; eskript_taƴde = false; 깊이 = 중첩깊이 - 1;
    }
}
