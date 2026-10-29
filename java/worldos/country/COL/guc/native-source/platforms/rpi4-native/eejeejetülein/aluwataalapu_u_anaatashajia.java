// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 atütüjiraaya aluwataalapu_u 문법. 파이프는 순차 실행, 환경은 같은 셸에서 공유한다. */
public final class aluwataalapu_u_anaatashajia {
    static int[] eejeejetülein = new int[4 * 4096], 종류 = new int[4 * 128], 시작 = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] 변수이름 = new int[16 * 32], 변수값 = new int[16 * 256], 이름길이 = new int[16], ajutuu_akaliaa = new int[16];
    static int[] script_ajutuu = new int[4 * 16384];
    static int jamakua_iparülein_ajutuu, 깊이, 쓴수;
    static boolean 연결중, script_ajattiraa, e_irukuu_ajachitia;
    static boolean 이름글자(int 문자값) { return 문자값 >= 'a' && 문자값 <= 'z' || 문자값 >= 'A' && 문자값 <= 'Z' || 문자값 == '_' || 문자값 >= 128; }
    static boolean 이름뒤(int 문자값) { return 이름글자(문자값) || 문자값 >= '0' && 문자값 <= '9'; }
    static void ajachitia(String 글) { 보드.입출력전환(0); 단말.ashajaa("aluwataaya akatajaa_ajutuu: "); 단말.ashajaa(글); 단말.문자(10); jamakua_iparülein_ajutuu = 2; }
    static int 읽기(int 항목수, int 중첩깊이) {
        int 현재자리 = 0, 총수 = 0, 기준자리 = 중첩깊이 * 4096, 특수문자 = 중첩깊이 * 128;
        while (현재자리 < 항목수) {
            while (현재자리 < 항목수 && (eejeejetülein[기준자리 + 현재자리] == 32 || eejeejetülein[기준자리 + 현재자리] == 9)) 현재자리++;
            if (현재자리 == 항목수 || eejeejetülein[기준자리 + 현재자리] == '#') break;
            if (총수 == 128) { ajachitia("낱말이 너무 많습니다"); return -1; }
            int 시작자리 = 현재자리, 문자값 = eejeejetülein[기준자리 + 현재자리], 자료종류 = 0;
            if (문자값 == ';') { 자료종류 = 1; 현재자리++; }
            else if (문자값 == '&') { if (현재자리 + 1 >= 항목수 || eejeejetülein[기준자리 + 현재자리 + 1] != '&') { ajachitia("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } 자료종류 = 2; 현재자리 += 2; }
            else if (문자값 == '|') { 현재자리++; 자료종류 = 현재자리 < 항목수 && eejeejetülein[기준자리 + 현재자리] == '|' ? 3 : 4; if (자료종류 == 3) 현재자리++; }
            else if (문자값 == '>') { 현재자리++; 자료종류 = 현재자리 < 항목수 && eejeejetülein[기준자리 + 현재자리] == '>' ? 6 : 5; if (자료종류 == 6) 현재자리++; }
            else if (문자값 == '<') { 자료종류 = 7; 현재자리++; }
            else {
                int 따옴표 = 0;
                while (현재자리 < 항목수) {
                    문자값 = eejeejetülein[기준자리 + 현재자리];
                    if (문자값 == '`' && 따옴표 != 39 || 문자값 == '$' && 따옴표 != 39 && 현재자리 + 1 < 항목수 && eejeejetülein[기준자리 + 현재자리 + 1] == '(') { ajachitia("aluwataaya 결과 치환은 지원하지 않습니다"); return -1; }
                    if (문자값 == '\\' && 따옴표 != 39) { if (++현재자리 == 항목수) { ajachitia("liinia 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } 현재자리++; continue; }
                    if (문자값 == 따옴표) { 따옴표 = 0; 현재자리++; continue; }
                    if (따옴표 == 0 && (문자값 == 39 || 문자값 == 34)) { 따옴표 = 문자값; 현재자리++; continue; }
                    if (따옴표 == 0 && (문자값 == 32 || 문자값 == 9 || 문자값 == ';' || 문자값 == '&' || 문자값 == '|' || 문자값 == '<' || 문자값 == '>')) break;
                    현재자리++;
                }
                if (따옴표 != 0) { ajachitia("따옴표가 닫히지 않았습니다"); return -1; }
                if (현재자리 < 항목수 && (eejeejetülein[기준자리 + 현재자리] == '>' || eejeejetülein[기준자리 + 현재자리] == '<')) {
                    boolean 수치 = 현재자리 > 시작자리;
                    for (int eitawaakualü_ee_iyatialujuna = 시작자리; eitawaakualü_ee_iyatialujuna < 현재자리; eitawaakualü_ee_iyatialujuna++) if (eejeejetülein[기준자리 + eitawaakualü_ee_iyatialujuna] < '0' || eejeejetülein[기준자리 + eitawaakualü_ee_iyatialujuna] > '9') 수치 = false;
                    if (수치) { ajachitia("번호를 지정한 anaajaalaa 서술자 E_A 전환은 지원하지 않습니다"); return -1; }
                }
            }
            종류[특수문자 + 총수] = 자료종류; 시작[특수문자 + 총수] = 시작자리; 끝[특수문자 + 총수] = 현재자리; 총수++;
        }
        boolean 낱말 = false;
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 총수; eitawaakualü_ee_iyatialujuna++) {
            int 임시값 = 종류[특수문자 + eitawaakualü_ee_iyatialujuna];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++eitawaakualü_ee_iyatialujuna == 총수 || 종류[특수문자 + eitawaakualü_ee_iyatialujuna] != 0) { ajachitia("E_A 전환에 anaajaalaa 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || eitawaakualü_ee_iyatialujuna == 총수 - 1 && 임시값 != 1) { ajachitia("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (총수 > 0 && !낱말 && 종류[특수문자 + 총수 - 1] != 1) { ajachitia("명령이 빠졌습니다"); return -1; }
        return 총수;
    }
    static boolean 구간말(int[] atijaaya_matüriisü, int 지역시작점, int 항목수, String 문자위치) {
        if (항목수 != 문자위치.length()) return false; for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 항목수; eitawaakualü_ee_iyatialujuna++) if (atijaaya_matüriisü[지역시작점 + eitawaakualü_ee_iyatialujuna] != 문자위치.charAt(eitawaakualü_ee_iyatialujuna)) return false; return true;
    }
    static void 넣기(int waai_atijaaya) {
        if (쓴수 >= 명령해석기.토큰.length) { if (!e_irukuu_ajachitia) ajachitia("변수를 펼친 명령이 너무 깁니다"); e_irukuu_ajachitia = true; return; }
        명령해석기.토큰[쓴수++] = waai_atijaaya;
    }
    static void 변수(int[] atijaaya_matüriisü, int 시작자리, int 항목수) {
        if (구간말(atijaaya_matüriisü, 시작자리, 항목수, "PWD")) { 넣기('/'); for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 기억파일.현재길이; eitawaakualü_ee_iyatialujuna++) 넣기(기억파일.현재[eitawaakualü_ee_iyatialujuna]); return; }
        if (구간말(atijaaya_matüriisü, 시작자리, 항목수, "HOME")) { 넣기('/'); return; }
        if (구간말(atijaaya_matüriisü, 시작자리, 항목수, "?")) {
            int atijaaya_ajutuu = jamakua_iparülein_ajutuu, 자릿값 = 100; boolean 시작여부 = false;
            while (자릿값 > 0) { int 뒷값 = atijaaya_ajutuu / 자릿값; if (뒷값 != 0 || 시작여부 || 자릿값 == 1) { 넣기('0' + 뒷값); 시작여부 = true; } atijaaya_ajutuu %= 자릿값; 자릿값 /= 10; } return;
        }
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 16; eitawaakualü_ee_iyatialujuna++) if (이름길이[eitawaakualü_ee_iyatialujuna] == 항목수) {
            boolean 일치여부 = true; for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) if (변수이름[eitawaakualü_ee_iyatialujuna * 32 + 안쪽자리] != atijaaya_matüriisü[시작자리 + 안쪽자리]) 일치여부 = false;
            if (일치여부) { for (int 안쪽자리 = 0; 안쪽자리 < ajutuu_akaliaa[eitawaakualü_ee_iyatialujuna]; 안쪽자리++) 넣기(변수값[eitawaakualü_ee_iyatialujuna * 256 + 안쪽자리]); return; }
        }
    }
    static boolean 단어(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = 시작[중첩깊이 * 128 + 낱말번호], 끝자리 = 끝[중첩깊이 * 128 + 낱말번호], 기준자리 = 중첩깊이 * 4096, 따옴표 = 0;
        if (읽는자리 < 끝자리 && eejeejetülein[기준자리 + 읽는자리] == '~' && (읽는자리 + 1 == 끝자리 || eejeejetülein[기준자리 + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < 끝자리) {
            int 문자값 = eejeejetülein[기준자리 + 읽는자리++];
            if (문자값 == 따옴표) { 따옴표 = 0; continue; }
            if (따옴표 == 0 && (문자값 == 39 || 문자값 == 34)) { 따옴표 = 문자값; continue; }
            if (문자값 == '\\' && 따옴표 != 39) { int 다음자리 = eejeejetülein[기준자리 + 읽는자리++]; if (따옴표 == 34 && 다음자리 != '$' && 다음자리 != '"' && 다음자리 != '\\') 넣기('\\'); 넣기(다음자리); continue; }
            if (문자값 == '$' && 따옴표 != 39 && 읽는자리 < 끝자리) {
                boolean 중괄호자리 = eejeejetülein[기준자리 + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < 끝자리 && eejeejetülein[기준자리 + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < 끝자리 && 이름뒤(eejeejetülein[기준자리 + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == 끝자리 || eejeejetülein[기준자리 + 읽는자리] != '}')) { ajachitia("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                변수(eejeejetülein, 기준자리 + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(문자값);
        }
        return !e_irukuu_ajachitia;
    }
    static int 환경설정(int ajutuu_ee_iyatialujuna, boolean 제거여부) {
        int 지역시작점 = 명령해석기.시작점[ajutuu_ee_iyatialujuna], 끝자리 = 지역시작점 + 명령해석기.akaliaa_ajutuu[ajutuu_ee_iyatialujuna], 같음자리 = 지역시작점;
        while (같음자리 < 끝자리 && 명령해석기.토큰[같음자리] != '=') 같음자리++;
        int 항목수 = 같음자리 - 지역시작점;
        if (항목수 < 1 || 항목수 > 31 || !이름글자(명령해석기.토큰[지역시작점]) || !제거여부 && 같음자리 == 끝자리 || 끝자리 - 같음자리 - 1 > 255) return 2;
        for (int eitawaakualü_ee_iyatialujuna = 지역시작점; eitawaakualü_ee_iyatialujuna < 같음자리; eitawaakualü_ee_iyatialujuna++) if (!이름뒤(명령해석기.토큰[eitawaakualü_ee_iyatialujuna])) return 2;
        if (구간말(명령해석기.토큰, 지역시작점, 항목수, "PWD") || 구간말(명령해석기.토큰, 지역시작점, 항목수, "HOME")) return 2;
        int 찾은여부 = -1, 빈여부 = -1;
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 16; eitawaakualü_ee_iyatialujuna++) {
            if (이름길이[eitawaakualü_ee_iyatialujuna] == 0) 빈여부 = eitawaakualü_ee_iyatialujuna;
            if (이름길이[eitawaakualü_ee_iyatialujuna] != 항목수) continue;
            boolean 일치여부 = true; for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) if (변수이름[eitawaakualü_ee_iyatialujuna * 32 + 안쪽자리] != 명령해석기.토큰[지역시작점 + 안쪽자리]) 일치여부 = false;
            if (일치여부) 찾은여부 = eitawaakualü_ee_iyatialujuna;
        }
        if (제거여부) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = 빈여부; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = 항목수; ajutuu_akaliaa[찾은여부] = 끝자리 - 같음자리 - 1;
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 항목수; eitawaakualü_ee_iyatialujuna++) 변수이름[찾은여부 * 32 + eitawaakualü_ee_iyatialujuna] = 명령해석기.토큰[지역시작점 + eitawaakualü_ee_iyatialujuna];
        for (int eitawaakualü_ee_iyatialujuna = 같음자리 + 1; eitawaakualü_ee_iyatialujuna < 끝자리; eitawaakualü_ee_iyatialujuna++) 변수값[찾은여부 * 256 + eitawaakualü_ee_iyatialujuna - 같음자리 - 1] = 명령해석기.토큰[eitawaakualü_ee_iyatialujuna];
        return 0;
    }
    static void 환경보기() {
        단말.ashajaa("HOME=/\nPWD="); 기억파일.현재쓰기(); 단말.문자(10);
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 16; eitawaakualü_ee_iyatialujuna++) if (이름길이[eitawaakualü_ee_iyatialujuna] > 0) {
            for (int 안쪽자리 = 0; 안쪽자리 < 이름길이[eitawaakualü_ee_iyatialujuna]; 안쪽자리++) 보드.직렬쓰기(변수이름[eitawaakualü_ee_iyatialujuna * 32 + 안쪽자리]); 단말.문자('=');
            for (int 안쪽자리 = 0; 안쪽자리 < ajutuu_akaliaa[eitawaakualü_ee_iyatialujuna]; 안쪽자리++) 보드.직렬쓰기(변수값[eitawaakualü_ee_iyatialujuna * 256 + 안쪽자리]); 단말.문자(10);
        }
    }
    static void 실행(int[] atijaaya_matüriisü, int 시작변위, int 항목수, int 중첩깊이) {
        if (중첩깊이 >= 4 || 항목수 > 4096) { ajachitia("aluwataaya 파일의 중첩 또는 liinia akaliaa_ajutuu 제한을 넘었습니다"); return; }
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 항목수; eitawaakualü_ee_iyatialujuna++) eejeejetülein[중첩깊이 * 4096 + eitawaakualü_ee_iyatialujuna] = atijaaya_matüriisü[시작변위 + eitawaakualü_ee_iyatialujuna];
        int 총수 = 읽기(항목수, 중첩깊이); if (총수 < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < 총수) {
            int akotchijuushi_ajattiraa = 읽는자리;
            while (akotchijuushi_ajattiraa < 총수 && (종류[중첩깊이 * 128 + akotchijuushi_ajattiraa] == 0 || 종류[중첩깊이 * 128 + akotchijuushi_ajattiraa] >= 4)) akotchijuushi_ajattiraa++;
            boolean 실행여부 = 조건성립 == 1 || 조건성립 == 2 && jamakua_iparülein_ajutuu == 0 || 조건성립 == 3 && jamakua_iparülein_ajutuu != 0;
            if (실행여부) {
                boolean 이전자리 = false;
                while (읽는자리 < akotchijuushi_ajattiraa) {
                    int 다음자리 = 읽는자리; while (다음자리 < akotchijuushi_ajattiraa && 종류[중첩깊이 * 128 + 다음자리] != 4) 다음자리++;
                    boolean a_ataa_palantüsü = 다음자리 < akotchijuushi_ajattiraa; int 입력쪽 = -1, 출력쪽 = -1, 출력방식 = 0;
                    명령해석기.토큰수 = 0; 쓴수 = 0; e_irukuu_ajachitia = false;
                    for (int eitawaakualü_ee_iyatialujuna = 읽는자리; eitawaakualü_ee_iyatialujuna < 다음자리; eitawaakualü_ee_iyatialujuna++) {
                        int 자료종류 = 종류[중첩깊이 * 128 + eitawaakualü_ee_iyatialujuna];
                        if (자료종류 >= 5) { if (자료종류 == 7) { if (입력쪽 >= 0) { ajachitia("입력 전환이 겹쳤습니다"); return; } 입력쪽 = ++eitawaakualü_ee_iyatialujuna; } else { if (출력쪽 >= 0) { ajachitia("출력 전환이 겹쳤습니다"); return; } 출력쪽 = ++eitawaakualü_ee_iyatialujuna; 출력방식 = 자료종류; } continue; }
                        if (명령해석기.토큰수 == 32) { ajachitia("인수가 너무 많습니다"); return; }
                        int ajutuu_ee_iyatialujuna = 명령해석기.토큰수++; 명령해석기.시작점[ajutuu_ee_iyatialujuna] = 쓴수;
                        if (!단어(eitawaakualü_ee_iyatialujuna, 중첩깊이)) return;
                        명령해석기.akaliaa_ajutuu[ajutuu_ee_iyatialujuna] = 쓴수 - 명령해석기.시작점[ajutuu_ee_iyatialujuna];
                    }
                    연결중 = 이전자리 || a_ataa_palantüsü || 입력쪽 >= 0 || 출력쪽 >= 0;
                    if (연결중 && (명령해석기.같음(0, "vi") || 명령해석기.같음(0, "edit") || 명령해석기.같음(0, "load") || 명령해석기.같음(0, "gui") || 명령해석기.같음(0, "terminal") || 명령해석기.같음(0, "sh") || 명령해석기.같음(0, "source"))) { ajachitia("atütüjiraaya 명령과 aluwataaya 파일은 E_A 전환이나 palantüsü_ajutuu 연결에 쓸 수 없습니다"); return; }
                    셸입출력.시작(이전자리, a_ataa_palantüsü);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int 항목자리 = 입출력바꿈 == 0 ? 입력쪽 : 출력쪽; if (항목자리 < 0) continue;
                        int 시작자리 = 쓴수; if (!단어(항목자리, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = 기억파일.wopu_a_ttaaleemüin_achuwalaa(쓴수 - 시작자리);
                        for (int 안쪽자리 = 시작자리; 처리값 >= 0 && 안쪽자리 < 쓴수; 안쪽자리++) 처리값 = 기억파일.wopu_a_ttaaleemüin_waai(안쪽자리 - 시작자리, 명령해석기.토큰[안쪽자리]);
                        if (처리값 >= 0) 처리값 = 기억파일.열기(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); 명령해석기.ajachitia(처리값); jamakua_iparülein_ajutuu = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.입력파일 = 처리값; else 셸입출력.출력파일 = 처리값;
                    }
                    셸입출력.A_tte_eraa_atütüjiraaya = 중첩깊이 == 0 && 읽는자리 == 0 && 다음자리 == 총수;
                    깊이 = 중첩깊이; 명령해석기.결과 = 0; 보드.입출력전환(1);
                    명령해석기.aluwataaya();
                    보드.터미널(3);
                    int 반환값 = 명령해석기.결과, palantüsü_ajachitia = 셸입출력.ajachitia_ajutuu;
                    셸입출력.끝(); 연결중 = false;
                    jamakua_iparülein_ajutuu = palantüsü_ajachitia < 0 ? 1 : 반환값;
                    if (palantüsü_ajachitia < 0) { 명령해석기.ajachitia(palantüsü_ajachitia); return; }
                    if (script_ajattiraa || 반환값 == -1005) return;
                    이전자리 = true; 읽는자리 = 다음자리 + 1;
                }
            }
            if (akotchijuushi_ajattiraa < 총수) 조건성립 = 종류[중첩깊이 * 128 + akotchijuushi_ajattiraa];
            읽는자리 = akotchijuushi_ajattiraa + 1;
        }
    }
    static void 파일실행() {
        if (명령해석기.토큰수 != 2 || 깊이 >= 3) { 명령해석기.결과 = 2; 단말.ashajaa("사용법: sh anaajaalaa (중첩 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = 명령해석기.wopu_a_ttaaleemüin(1); if (처리값 >= 0) 처리값 = 기억파일.열기(0);
        if (처리값 < 0) { 명령해석기.ajachitia(처리값); return; }
        int 항목수 = 0, waai_atijaaya;
        while ((waai_atijaaya = 기억파일.읽기(처리값)) != 256 && waai_atijaaya >= 0 && 항목수 < 16384) script_ajutuu[중첩깊이 * 16384 + 항목수++] = waai_atijaaya;
        기억파일.asürülaa(처리값); 보드.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < 항목수 && !script_ajattiraa;) {
            int 끝자리 = 읽는자리; while (끝자리 < 항목수 && script_ajutuu[중첩깊이 * 16384 + 끝자리] != 10) 끝자리++;
            int 유효길이 = 끝자리 - 읽는자리; if (유효길이 > 0 && script_ajutuu[중첩깊이 * 16384 + 끝자리 - 1] == 13) 유효길이--;
            실행(script_ajutuu, 중첩깊이 * 16384 + 읽는자리, 유효길이, 중첩깊이); 읽는자리 = 끝자리 + 1;
        }
        명령해석기.결과 = jamakua_iparülein_ajutuu; script_ajattiraa = false; 깊이 = 중첩깊이 - 1;
    }
}
