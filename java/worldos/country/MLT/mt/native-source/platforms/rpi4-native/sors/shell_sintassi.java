// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 interattiv shell 문법. 파이프는 순차 eżegwixxa_kmand, 환경은 같은 셸에서 공유한다. */
public final class shell_sintassi {
    static int[] sors = new int[4 * 4096], 종류 = new int[4 * 128], serje = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] 변수이름 = new int[16 * 32], 변수값 = new int[16 * 256], 이름길이 = new int[16], VALUE_tul = new int[16];
    static int[] skript_VALUE = new int[4 * 16384];
    static int stat_VALUE, 깊이, 쓴수;
    static boolean 연결중, skript_ttermina, estensjoni_żball;
    static boolean isem_karattru(int kodiċi_tal_karattru) { return kodiċi_tal_karattru >= 'a' && kodiċi_tal_karattru <= 'z' || kodiċi_tal_karattru >= 'A' && kodiċi_tal_karattru <= 'Z' || kodiċi_tal_karattru == '_' || kodiċi_tal_karattru >= 128; }
    static boolean 이름뒤(int kodiċi_tal_karattru) { return isem_karattru(kodiċi_tal_karattru) || kodiċi_tal_karattru >= '0' && kodiċi_tal_karattru <= '9'; }
    static void żball(String SMS) { bord.입출력전환(0); 단말.kiteb("kmand analizza_VALUE: "); 단말.kiteb(SMS); 단말.문자(10); stat_VALUE = 2; }
    static int 읽기(int entrata_COUNT, int 중첩깊이) {
        int 현재자리 = 0, 총수 = 0, BASE_pożizzjoni = 중첩깊이 * 4096, karattru_speċjali = 중첩깊이 * 128;
        while (현재자리 < entrata_COUNT) {
            while (현재자리 < entrata_COUNT && (sors[BASE_pożizzjoni + 현재자리] == 32 || sors[BASE_pożizzjoni + 현재자리] == 9)) 현재자리++;
            if (현재자리 == entrata_COUNT || sors[BASE_pożizzjoni + 현재자리] == '#') break;
            if (총수 == 128) { żball("낱말이 너무 많습니다"); return -1; }
            int Bidu_pożizzjoni = 현재자리, kodiċi_tal_karattru = sors[BASE_pożizzjoni + 현재자리], 자료종류 = 0;
            if (kodiċi_tal_karattru == ';') { 자료종류 = 1; 현재자리++; }
            else if (kodiċi_tal_karattru == '&') { if (현재자리 + 1 >= entrata_COUNT || sors[BASE_pożizzjoni + 현재자리 + 1] != '&') { żball("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } 자료종류 = 2; 현재자리 += 2; }
            else if (kodiċi_tal_karattru == '|') { 현재자리++; 자료종류 = 현재자리 < entrata_COUNT && sors[BASE_pożizzjoni + 현재자리] == '|' ? 3 : 4; if (자료종류 == 3) 현재자리++; }
            else if (kodiċi_tal_karattru == '>') { 현재자리++; 자료종류 = 현재자리 < entrata_COUNT && sors[BASE_pożizzjoni + 현재자리] == '>' ? 6 : 5; if (자료종류 == 6) 현재자리++; }
            else if (kodiċi_tal_karattru == '<') { 자료종류 = 7; 현재자리++; }
            else {
                int Kwotazzjoni = 0;
                while (현재자리 < entrata_COUNT) {
                    kodiċi_tal_karattru = sors[BASE_pożizzjoni + 현재자리];
                    if (kodiċi_tal_karattru == '`' && Kwotazzjoni != 39 || kodiċi_tal_karattru == '$' && Kwotazzjoni != 39 && 현재자리 + 1 < entrata_COUNT && sors[BASE_pożizzjoni + 현재자리 + 1] == '(') { żball("kmand miżura 치환은 지원하지 않습니다"); return -1; }
                    if (kodiċi_tal_karattru == '\\' && Kwotazzjoni != 39) { if (++현재자리 == entrata_COUNT) { żball("linja 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } 현재자리++; continue; }
                    if (kodiċi_tal_karattru == Kwotazzjoni) { Kwotazzjoni = 0; 현재자리++; continue; }
                    if (Kwotazzjoni == 0 && (kodiċi_tal_karattru == 39 || kodiċi_tal_karattru == 34)) { Kwotazzjoni = kodiċi_tal_karattru; 현재자리++; continue; }
                    if (Kwotazzjoni == 0 && (kodiċi_tal_karattru == 32 || kodiċi_tal_karattru == 9 || kodiċi_tal_karattru == ';' || kodiċi_tal_karattru == '&' || kodiċi_tal_karattru == '|' || kodiċi_tal_karattru == '<' || kodiċi_tal_karattru == '>')) break;
                    현재자리++;
                }
                if (Kwotazzjoni != 0) { żball("따옴표가 닫히지 않았습니다"); return -1; }
                if (현재자리 < entrata_COUNT && (sors[BASE_pożizzjoni + 현재자리] == '>' || sors[BASE_pożizzjoni + 현재자리] == '<')) {
                    boolean 수치 = 현재자리 > Bidu_pożizzjoni;
                    for (int Loop_INDEX = Bidu_pożizzjoni; Loop_INDEX < 현재자리; Loop_INDEX++) if (sors[BASE_pożizzjoni + Loop_INDEX] < '0' || sors[BASE_pożizzjoni + Loop_INDEX] > '9') 수치 = false;
                    if (수치) { żball("번호를 지정한 fajl 서술자 I_O 전환은 지원하지 않습니다"); return -1; }
                }
            }
            종류[karattru_speċjali + 총수] = 자료종류; serje[karattru_speċjali + 총수] = Bidu_pożizzjoni; 끝[karattru_speċjali + 총수] = 현재자리; 총수++;
        }
        boolean 낱말 = false;
        for (int Loop_INDEX = 0; Loop_INDEX < 총수; Loop_INDEX++) {
            int 임시값 = 종류[karattru_speċjali + Loop_INDEX];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++Loop_INDEX == 총수 || 종류[karattru_speċjali + Loop_INDEX] != 0) { żball("I_O 전환에 fajl 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || Loop_INDEX == 총수 - 1 && 임시값 != 1) { żball("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (총수 > 0 && !낱말 && 종류[karattru_speċjali + 총수 - 1] != 1) { żball("명령이 빠졌습니다"); return -1; }
        return 총수;
    }
    static boolean 구간말(int[] data_ARRAY, int lokali_Bidu, int entrata_COUNT, String karattru_pożizzjoni) {
        if (entrata_COUNT != karattru_pożizzjoni.length()) return false; for (int Loop_INDEX = 0; Loop_INDEX < entrata_COUNT; Loop_INDEX++) if (data_ARRAY[lokali_Bidu + Loop_INDEX] != karattru_pożizzjoni.charAt(Loop_INDEX)) return false; return true;
    }
    static void 넣기(int byte_data) {
        if (쓴수 >= 명령해석기.token_VALUE.length) { if (!estensjoni_żball) żball("변수를 펼친 명령이 너무 깁니다"); estensjoni_żball = true; return; }
        명령해석기.token_VALUE[쓴수++] = byte_data;
    }
    static void 변수(int[] data_ARRAY, int Bidu_pożizzjoni, int entrata_COUNT) {
        if (구간말(data_ARRAY, Bidu_pożizzjoni, entrata_COUNT, "PWD")) { 넣기('/'); for (int Loop_INDEX = 0; Loop_INDEX < Memorja_Fajls.현재길이; Loop_INDEX++) 넣기(Memorja_Fajls.현재[Loop_INDEX]); return; }
        if (구간말(data_ARRAY, Bidu_pożizzjoni, entrata_COUNT, "HOME")) { 넣기('/'); return; }
        if (구간말(data_ARRAY, Bidu_pożizzjoni, entrata_COUNT, "?")) {
            int data_VALUE = stat_VALUE, ċifra = 100; boolean 시작여부 = false;
            while (ċifra > 0) { int 뒷값 = data_VALUE / ċifra; if (뒷값 != 0 || 시작여부 || ċifra == 1) { 넣기('0' + 뒷값); 시작여부 = true; } data_VALUE %= ċifra; ċifra /= 10; } return;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] == entrata_COUNT) {
            boolean MATCH = true; for (int inner_join_pożizzjoni = 0; inner_join_pożizzjoni < entrata_COUNT; inner_join_pożizzjoni++) if (변수이름[Loop_INDEX * 32 + inner_join_pożizzjoni] != data_ARRAY[Bidu_pożizzjoni + inner_join_pożizzjoni]) MATCH = false;
            if (MATCH) { for (int inner_join_pożizzjoni = 0; inner_join_pożizzjoni < VALUE_tul[Loop_INDEX]; inner_join_pożizzjoni++) 넣기(변수값[Loop_INDEX * 256 + inner_join_pożizzjoni]); return; }
        }
    }
    static boolean Word_VALUE(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = serje[중첩깊이 * 128 + 낱말번호], ttermina_pożizzjoni = 끝[중첩깊이 * 128 + 낱말번호], BASE_pożizzjoni = 중첩깊이 * 4096, Kwotazzjoni = 0;
        if (읽는자리 < ttermina_pożizzjoni && sors[BASE_pożizzjoni + 읽는자리] == '~' && (읽는자리 + 1 == ttermina_pożizzjoni || sors[BASE_pożizzjoni + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < ttermina_pożizzjoni) {
            int kodiċi_tal_karattru = sors[BASE_pożizzjoni + 읽는자리++];
            if (kodiċi_tal_karattru == Kwotazzjoni) { Kwotazzjoni = 0; continue; }
            if (Kwotazzjoni == 0 && (kodiċi_tal_karattru == 39 || kodiċi_tal_karattru == 34)) { Kwotazzjoni = kodiċi_tal_karattru; continue; }
            if (kodiċi_tal_karattru == '\\' && Kwotazzjoni != 39) { int Li_Jmiss_pożizzjoni = sors[BASE_pożizzjoni + 읽는자리++]; if (Kwotazzjoni == 34 && Li_Jmiss_pożizzjoni != '$' && Li_Jmiss_pożizzjoni != '"' && Li_Jmiss_pożizzjoni != '\\') 넣기('\\'); 넣기(Li_Jmiss_pożizzjoni); continue; }
            if (kodiċi_tal_karattru == '$' && Kwotazzjoni != 39 && 읽는자리 < ttermina_pożizzjoni) {
                boolean 중괄호자리 = sors[BASE_pożizzjoni + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < ttermina_pożizzjoni && sors[BASE_pożizzjoni + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < ttermina_pożizzjoni && 이름뒤(sors[BASE_pożizzjoni + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == ttermina_pożizzjoni || sors[BASE_pożizzjoni + 읽는자리] != '}')) { żball("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                변수(sors, BASE_pożizzjoni + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(kodiċi_tal_karattru);
        }
        return !estensjoni_żball;
    }
    static int 환경설정(int argument_INDEX, boolean neħħa) {
        int lokali_Bidu = 명령해석기.시작점[argument_INDEX], ttermina_pożizzjoni = lokali_Bidu + 명령해석기.tul_VALUE[argument_INDEX], 같음자리 = lokali_Bidu;
        while (같음자리 < ttermina_pożizzjoni && 명령해석기.token_VALUE[같음자리] != '=') 같음자리++;
        int entrata_COUNT = 같음자리 - lokali_Bidu;
        if (entrata_COUNT < 1 || entrata_COUNT > 31 || !isem_karattru(명령해석기.token_VALUE[lokali_Bidu]) || !neħħa && 같음자리 == ttermina_pożizzjoni || ttermina_pożizzjoni - 같음자리 - 1 > 255) return 2;
        for (int Loop_INDEX = lokali_Bidu; Loop_INDEX < 같음자리; Loop_INDEX++) if (!이름뒤(명령해석기.token_VALUE[Loop_INDEX])) return 2;
        if (구간말(명령해석기.token_VALUE, lokali_Bidu, entrata_COUNT, "PWD") || 구간말(명령해석기.token_VALUE, lokali_Bidu, entrata_COUNT, "HOME")) return 2;
        int 찾은여부 = -1, 빈여부 = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] == 0) 빈여부 = Loop_INDEX;
            if (이름길이[Loop_INDEX] != entrata_COUNT) continue;
            boolean MATCH = true; for (int inner_join_pożizzjoni = 0; inner_join_pożizzjoni < entrata_COUNT; inner_join_pożizzjoni++) if (변수이름[Loop_INDEX * 32 + inner_join_pożizzjoni] != 명령해석기.token_VALUE[lokali_Bidu + inner_join_pożizzjoni]) MATCH = false;
            if (MATCH) 찾은여부 = Loop_INDEX;
        }
        if (neħħa) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = 빈여부; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = entrata_COUNT; VALUE_tul[찾은여부] = ttermina_pożizzjoni - 같음자리 - 1;
        for (int Loop_INDEX = 0; Loop_INDEX < entrata_COUNT; Loop_INDEX++) 변수이름[찾은여부 * 32 + Loop_INDEX] = 명령해석기.token_VALUE[lokali_Bidu + Loop_INDEX];
        for (int Loop_INDEX = 같음자리 + 1; Loop_INDEX < ttermina_pożizzjoni; Loop_INDEX++) 변수값[찾은여부 * 256 + Loop_INDEX - 같음자리 - 1] = 명령해석기.token_VALUE[Loop_INDEX];
        return 0;
    }
    static void 환경보기() {
        단말.kiteb("HOME=/\nPWD="); Memorja_Fajls.현재쓰기(); 단말.문자(10);
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] > 0) {
            for (int inner_join_pożizzjoni = 0; inner_join_pożizzjoni < 이름길이[Loop_INDEX]; inner_join_pożizzjoni++) bord.직렬쓰기(변수이름[Loop_INDEX * 32 + inner_join_pożizzjoni]); 단말.문자('=');
            for (int inner_join_pożizzjoni = 0; inner_join_pożizzjoni < VALUE_tul[Loop_INDEX]; inner_join_pożizzjoni++) bord.직렬쓰기(변수값[Loop_INDEX * 256 + inner_join_pożizzjoni]); 단말.문자(10);
        }
    }
    static void eżegwixxa_kmand(int[] data_ARRAY, int 시작변위, int entrata_COUNT, int 중첩깊이) {
        if (중첩깊이 >= 4 || entrata_COUNT > 4096) { żball("kmand 파일의 중첩 또는 linja tul_VALUE 제한을 넘었습니다"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < entrata_COUNT; Loop_INDEX++) sors[중첩깊이 * 4096 + Loop_INDEX] = data_ARRAY[시작변위 + Loop_INDEX];
        int 총수 = 읽기(entrata_COUNT, 중첩깊이); if (총수 < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < 총수) {
            int grupp_ttermina = 읽는자리;
            while (grupp_ttermina < 총수 && (종류[중첩깊이 * 128 + grupp_ttermina] == 0 || 종류[중첩깊이 * 128 + grupp_ttermina] >= 4)) grupp_ttermina++;
            boolean eżegwixxa = 조건성립 == 1 || 조건성립 == 2 && stat_VALUE == 0 || 조건성립 == 3 && stat_VALUE != 0;
            if (eżegwixxa) {
                boolean 이전자리 = false;
                while (읽는자리 < grupp_ttermina) {
                    int Li_Jmiss_pożizzjoni = 읽는자리; while (Li_Jmiss_pożizzjoni < grupp_ttermina && 종류[중첩깊이 * 128 + Li_Jmiss_pożizzjoni] != 4) Li_Jmiss_pożizzjoni++;
                    boolean AQBAD_Stream = Li_Jmiss_pożizzjoni < grupp_ttermina; int 입력쪽 = -1, 출력쪽 = -1, 출력방식 = 0;
                    명령해석기.token_COUNT = 0; 쓴수 = 0; estensjoni_żball = false;
                    for (int Loop_INDEX = 읽는자리; Loop_INDEX < Li_Jmiss_pożizzjoni; Loop_INDEX++) {
                        int 자료종류 = 종류[중첩깊이 * 128 + Loop_INDEX];
                        if (자료종류 >= 5) { if (자료종류 == 7) { if (입력쪽 >= 0) { żball("입력 전환이 겹쳤습니다"); return; } 입력쪽 = ++Loop_INDEX; } else { if (출력쪽 >= 0) { żball("출력 전환이 겹쳤습니다"); return; } 출력쪽 = ++Loop_INDEX; 출력방식 = 자료종류; } continue; }
                        if (명령해석기.token_COUNT == 32) { żball("인수가 너무 많습니다"); return; }
                        int argument_INDEX = 명령해석기.token_COUNT++; 명령해석기.시작점[argument_INDEX] = 쓴수;
                        if (!Word_VALUE(Loop_INDEX, 중첩깊이)) return;
                        명령해석기.tul_VALUE[argument_INDEX] = 쓴수 - 명령해석기.시작점[argument_INDEX];
                    }
                    연결중 = 이전자리 || AQBAD_Stream || 입력쪽 >= 0 || 출력쪽 >= 0;
                    if (연결중 && (명령해석기.같음(0, "vi") || 명령해석기.같음(0, "edit") || 명령해석기.같음(0, "load") || 명령해석기.같음(0, "gui") || 명령해석기.같음(0, "terminal") || 명령해석기.같음(0, "sh") || 명령해석기.같음(0, "source"))) { żball("interattiv 명령과 kmand 파일은 I_O 전환이나 Stream_VALUE 연결에 쓸 수 없습니다"); return; }
                    셸입출력.serje(이전자리, AQBAD_Stream);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int entrata_pożizzjoni = 입출력바꿈 == 0 ? 입력쪽 : 출력쪽; if (entrata_pożizzjoni < 0) continue;
                        int Bidu_pożizzjoni = 쓴수; if (!Word_VALUE(entrata_pożizzjoni, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = Memorja_Fajls.mogħdija_Bidu(쓴수 - Bidu_pożizzjoni);
                        for (int inner_join_pożizzjoni = Bidu_pożizzjoni; 처리값 >= 0 && inner_join_pożizzjoni < 쓴수; inner_join_pożizzjoni++) 처리값 = Memorja_Fajls.mogħdija_byte(inner_join_pożizzjoni - Bidu_pożizzjoni, 명령해석기.token_VALUE[inner_join_pożizzjoni]);
                        if (처리값 >= 0) 처리값 = Memorja_Fajls.fetaħ(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); 명령해석기.żball(처리값); stat_VALUE = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.입력파일 = 처리값; else 셸입출력.fajl_ta_output = 처리값;
                    }
                    셸입출력.ppermetti_interattiv = 중첩깊이 == 0 && 읽는자리 == 0 && Li_Jmiss_pożizzjoni == 총수;
                    깊이 = 중첩깊이; 명령해석기.miżura = 0; bord.입출력전환(1);
                    명령해석기.kmand();
                    bord.Terminal(3);
                    int 반환값 = 명령해석기.miżura, Stream_żball = 셸입출력.żball_VALUE;
                    셸입출력.끝(); 연결중 = false;
                    stat_VALUE = Stream_żball < 0 ? 1 : 반환값;
                    if (Stream_żball < 0) { 명령해석기.żball(Stream_żball); return; }
                    if (skript_ttermina || 반환값 == -1005) return;
                    이전자리 = true; 읽는자리 = Li_Jmiss_pożizzjoni + 1;
                }
            }
            if (grupp_ttermina < 총수) 조건성립 = 종류[중첩깊이 * 128 + grupp_ttermina];
            읽는자리 = grupp_ttermina + 1;
        }
    }
    static void eżegwixxa_fajl() {
        if (명령해석기.token_COUNT != 2 || 깊이 >= 3) { 명령해석기.miżura = 2; 단말.kiteb("사용법: sh fajl (중첩 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = 명령해석기.mogħdija(1); if (처리값 >= 0) 처리값 = Memorja_Fajls.fetaħ(0);
        if (처리값 < 0) { 명령해석기.żball(처리값); return; }
        int entrata_COUNT = 0, byte_data;
        while ((byte_data = Memorja_Fajls.읽기(처리값)) != 256 && byte_data >= 0 && entrata_COUNT < 16384) skript_VALUE[중첩깊이 * 16384 + entrata_COUNT++] = byte_data;
        Memorja_Fajls.agħlaq(처리값); bord.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < entrata_COUNT && !skript_ttermina;) {
            int ttermina_pożizzjoni = 읽는자리; while (ttermina_pożizzjoni < entrata_COUNT && skript_VALUE[중첩깊이 * 16384 + ttermina_pożizzjoni] != 10) ttermina_pożizzjoni++;
            int 유효길이 = ttermina_pożizzjoni - 읽는자리; if (유효길이 > 0 && skript_VALUE[중첩깊이 * 16384 + ttermina_pożizzjoni - 1] == 13) 유효길이--;
            eżegwixxa_kmand(skript_VALUE, 중첩깊이 * 16384 + 읽는자리, 유효길이, 중첩깊이); 읽는자리 = ttermina_pożizzjoni + 1;
        }
        명령해석기.miżura = stat_VALUE; skript_ttermina = false; 깊이 = 중첩깊이 - 1;
    }
}
