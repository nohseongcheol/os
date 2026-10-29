// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 interaktiv örtük 문법. 파이프는 순차 icra_etmək_əmr, 환경은 같은 셸에서 공유한다. */
public final class örtük_sintaksis {
    static int[] QAYNAQ = new int[4 * 4096], 종류 = new int[4 * 128], İcra_Et = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] 변수이름 = new int[16 * 32], 변수값 = new int[16 * 256], 이름길이 = new int[16], VALUE_uzunluq = new int[16];
    static int[] skript_VALUE = new int[4 * 16384];
    static int vəziyyət_VALUE, 깊이, 쓴수;
    static boolean 연결중, skript_bitirmək, genişlənmə_səhv;
    static boolean ad_simvol(int simvol_kodu) { return simvol_kodu >= 'a' && simvol_kodu <= 'z' || simvol_kodu >= 'A' && simvol_kodu <= 'Z' || simvol_kodu == '_' || simvol_kodu >= 128; }
    static boolean 이름뒤(int simvol_kodu) { return ad_simvol(simvol_kodu) || simvol_kodu >= '0' && simvol_kodu <= '9'; }
    static void XƏTA(String Mətn) { lövhə.입출력전환(0); 단말.Yazma("Əmr parselləmək_VALUE: "); 단말.Yazma(Mətn); 단말.문자(10); vəziyyət_VALUE = 2; }
    static int Oxuma(int daxiletmə_COUNT, int 중첩깊이) {
        int 현재자리 = 0, 총수 = 0, BASE_yerinə_qoymaq = 중첩깊이 * 4096, xüsusi_simvol = 중첩깊이 * 128;
        while (현재자리 < daxiletmə_COUNT) {
            while (현재자리 < daxiletmə_COUNT && (QAYNAQ[BASE_yerinə_qoymaq + 현재자리] == 32 || QAYNAQ[BASE_yerinə_qoymaq + 현재자리] == 9)) 현재자리++;
            if (현재자리 == daxiletmə_COUNT || QAYNAQ[BASE_yerinə_qoymaq + 현재자리] == '#') break;
            if (총수 == 128) { XƏTA("낱말이 너무 많습니다"); return -1; }
            int Başla_yerinə_qoymaq = 현재자리, simvol_kodu = QAYNAQ[BASE_yerinə_qoymaq + 현재자리], 자료종류 = 0;
            if (simvol_kodu == ';') { 자료종류 = 1; 현재자리++; }
            else if (simvol_kodu == '&') { if (현재자리 + 1 >= daxiletmə_COUNT || QAYNAQ[BASE_yerinə_qoymaq + 현재자리 + 1] != '&') { XƏTA("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } 자료종류 = 2; 현재자리 += 2; }
            else if (simvol_kodu == '|') { 현재자리++; 자료종류 = 현재자리 < daxiletmə_COUNT && QAYNAQ[BASE_yerinə_qoymaq + 현재자리] == '|' ? 3 : 4; if (자료종류 == 3) 현재자리++; }
            else if (simvol_kodu == '>') { 현재자리++; 자료종류 = 현재자리 < daxiletmə_COUNT && QAYNAQ[BASE_yerinə_qoymaq + 현재자리] == '>' ? 6 : 5; if (자료종류 == 6) 현재자리++; }
            else if (simvol_kodu == '<') { 자료종류 = 7; 현재자리++; }
            else {
                int Dırnaqarası = 0;
                while (현재자리 < daxiletmə_COUNT) {
                    simvol_kodu = QAYNAQ[BASE_yerinə_qoymaq + 현재자리];
                    if (simvol_kodu == '`' && Dırnaqarası != 39 || simvol_kodu == '$' && Dırnaqarası != 39 && 현재자리 + 1 < daxiletmə_COUNT && QAYNAQ[BASE_yerinə_qoymaq + 현재자리 + 1] == '(') { XƏTA("Əmr ölçü 치환은 지원하지 않습니다"); return -1; }
                    if (simvol_kodu == '\\' && Dırnaqarası != 39) { if (++현재자리 == daxiletmə_COUNT) { XƏTA("Giriş 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } 현재자리++; continue; }
                    if (simvol_kodu == Dırnaqarası) { Dırnaqarası = 0; 현재자리++; continue; }
                    if (Dırnaqarası == 0 && (simvol_kodu == 39 || simvol_kodu == 34)) { Dırnaqarası = simvol_kodu; 현재자리++; continue; }
                    if (Dırnaqarası == 0 && (simvol_kodu == 32 || simvol_kodu == 9 || simvol_kodu == ';' || simvol_kodu == '&' || simvol_kodu == '|' || simvol_kodu == '<' || simvol_kodu == '>')) break;
                    현재자리++;
                }
                if (Dırnaqarası != 0) { XƏTA("따옴표가 닫히지 않았습니다"); return -1; }
                if (현재자리 < daxiletmə_COUNT && (QAYNAQ[BASE_yerinə_qoymaq + 현재자리] == '>' || QAYNAQ[BASE_yerinə_qoymaq + 현재자리] == '<')) {
                    boolean 수치 = 현재자리 > Başla_yerinə_qoymaq;
                    for (int Loop_INDEX = Başla_yerinə_qoymaq; Loop_INDEX < 현재자리; Loop_INDEX++) if (QAYNAQ[BASE_yerinə_qoymaq + Loop_INDEX] < '0' || QAYNAQ[BASE_yerinə_qoymaq + Loop_INDEX] > '9') 수치 = false;
                    if (수치) { XƏTA("번호를 지정한 FAYL 서술자 giriş_çıxış 전환은 지원하지 않습니다"); return -1; }
                }
            }
            종류[xüsusi_simvol + 총수] = 자료종류; İcra_Et[xüsusi_simvol + 총수] = Başla_yerinə_qoymaq; 끝[xüsusi_simvol + 총수] = 현재자리; 총수++;
        }
        boolean 낱말 = false;
        for (int Loop_INDEX = 0; Loop_INDEX < 총수; Loop_INDEX++) {
            int 임시값 = 종류[xüsusi_simvol + Loop_INDEX];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++Loop_INDEX == 총수 || 종류[xüsusi_simvol + Loop_INDEX] != 0) { XƏTA("giriş_çıxış 전환에 FAYL 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || Loop_INDEX == 총수 - 1 && 임시값 != 1) { XƏTA("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (총수 > 0 && !낱말 && 종류[xüsusi_simvol + 총수 - 1] != 1) { XƏTA("명령이 빠졌습니다"); return -1; }
        return 총수;
    }
    static boolean 구간말(int[] verilənlər_ARRAY, int lokal_Başla, int daxiletmə_COUNT, String simvol_yerinə_qoymaq) {
        if (daxiletmə_COUNT != simvol_yerinə_qoymaq.length()) return false; for (int Loop_INDEX = 0; Loop_INDEX < daxiletmə_COUNT; Loop_INDEX++) if (verilənlər_ARRAY[lokal_Başla + Loop_INDEX] != simvol_yerinə_qoymaq.charAt(Loop_INDEX)) return false; return true;
    }
    static void 넣기(int bayt_verilənlər) {
        if (쓴수 >= 명령해석기.nişan_VALUE.length) { if (!genişlənmə_səhv) XƏTA("변수를 펼친 명령이 너무 깁니다"); genişlənmə_səhv = true; return; }
        명령해석기.nişan_VALUE[쓴수++] = bayt_verilənlər;
    }
    static void 변수(int[] verilənlər_ARRAY, int Başla_yerinə_qoymaq, int daxiletmə_COUNT) {
        if (구간말(verilənlər_ARRAY, Başla_yerinə_qoymaq, daxiletmə_COUNT, "PWD")) { 넣기('/'); for (int Loop_INDEX = 0; Loop_INDEX < Yaddaş_Fayllar.현재길이; Loop_INDEX++) 넣기(Yaddaş_Fayllar.현재[Loop_INDEX]); return; }
        if (구간말(verilənlər_ARRAY, Başla_yerinə_qoymaq, daxiletmə_COUNT, "HOME")) { 넣기('/'); return; }
        if (구간말(verilənlər_ARRAY, Başla_yerinə_qoymaq, daxiletmə_COUNT, "?")) {
            int verilənlər_VALUE = vəziyyət_VALUE, rəqəm = 100; boolean 시작여부 = false;
            while (rəqəm > 0) { int 뒷값 = verilənlər_VALUE / rəqəm; if (뒷값 != 0 || 시작여부 || rəqəm == 1) { 넣기('0' + 뒷값); 시작여부 = true; } verilənlər_VALUE %= rəqəm; rəqəm /= 10; } return;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] == daxiletmə_COUNT) {
            boolean MATCH = true; for (int daxili_qoşulma_yerinə_qoymaq = 0; daxili_qoşulma_yerinə_qoymaq < daxiletmə_COUNT; daxili_qoşulma_yerinə_qoymaq++) if (변수이름[Loop_INDEX * 32 + daxili_qoşulma_yerinə_qoymaq] != verilənlər_ARRAY[Başla_yerinə_qoymaq + daxili_qoşulma_yerinə_qoymaq]) MATCH = false;
            if (MATCH) { for (int daxili_qoşulma_yerinə_qoymaq = 0; daxili_qoşulma_yerinə_qoymaq < VALUE_uzunluq[Loop_INDEX]; daxili_qoşulma_yerinə_qoymaq++) 넣기(변수값[Loop_INDEX * 256 + daxili_qoşulma_yerinə_qoymaq]); return; }
        }
    }
    static boolean Söz_VALUE(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = İcra_Et[중첩깊이 * 128 + 낱말번호], bitirmək_yerinə_qoymaq = 끝[중첩깊이 * 128 + 낱말번호], BASE_yerinə_qoymaq = 중첩깊이 * 4096, Dırnaqarası = 0;
        if (읽는자리 < bitirmək_yerinə_qoymaq && QAYNAQ[BASE_yerinə_qoymaq + 읽는자리] == '~' && (읽는자리 + 1 == bitirmək_yerinə_qoymaq || QAYNAQ[BASE_yerinə_qoymaq + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < bitirmək_yerinə_qoymaq) {
            int simvol_kodu = QAYNAQ[BASE_yerinə_qoymaq + 읽는자리++];
            if (simvol_kodu == Dırnaqarası) { Dırnaqarası = 0; continue; }
            if (Dırnaqarası == 0 && (simvol_kodu == 39 || simvol_kodu == 34)) { Dırnaqarası = simvol_kodu; continue; }
            if (simvol_kodu == '\\' && Dırnaqarası != 39) { int Sonrakı_yerinə_qoymaq = QAYNAQ[BASE_yerinə_qoymaq + 읽는자리++]; if (Dırnaqarası == 34 && Sonrakı_yerinə_qoymaq != '$' && Sonrakı_yerinə_qoymaq != '"' && Sonrakı_yerinə_qoymaq != '\\') 넣기('\\'); 넣기(Sonrakı_yerinə_qoymaq); continue; }
            if (simvol_kodu == '$' && Dırnaqarası != 39 && 읽는자리 < bitirmək_yerinə_qoymaq) {
                boolean 중괄호자리 = QAYNAQ[BASE_yerinə_qoymaq + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < bitirmək_yerinə_qoymaq && QAYNAQ[BASE_yerinə_qoymaq + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < bitirmək_yerinə_qoymaq && 이름뒤(QAYNAQ[BASE_yerinə_qoymaq + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == bitirmək_yerinə_qoymaq || QAYNAQ[BASE_yerinə_qoymaq + 읽는자리] != '}')) { XƏTA("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                변수(QAYNAQ, BASE_yerinə_qoymaq + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(simvol_kodu);
        }
        return !genişlənmə_səhv;
    }
    static int 환경설정(int arqument_INDEX, boolean silmək) {
        int lokal_Başla = 명령해석기.시작점[arqument_INDEX], bitirmək_yerinə_qoymaq = lokal_Başla + 명령해석기.uzunluq_VALUE[arqument_INDEX], 같음자리 = lokal_Başla;
        while (같음자리 < bitirmək_yerinə_qoymaq && 명령해석기.nişan_VALUE[같음자리] != '=') 같음자리++;
        int daxiletmə_COUNT = 같음자리 - lokal_Başla;
        if (daxiletmə_COUNT < 1 || daxiletmə_COUNT > 31 || !ad_simvol(명령해석기.nişan_VALUE[lokal_Başla]) || !silmək && 같음자리 == bitirmək_yerinə_qoymaq || bitirmək_yerinə_qoymaq - 같음자리 - 1 > 255) return 2;
        for (int Loop_INDEX = lokal_Başla; Loop_INDEX < 같음자리; Loop_INDEX++) if (!이름뒤(명령해석기.nişan_VALUE[Loop_INDEX])) return 2;
        if (구간말(명령해석기.nişan_VALUE, lokal_Başla, daxiletmə_COUNT, "PWD") || 구간말(명령해석기.nişan_VALUE, lokal_Başla, daxiletmə_COUNT, "HOME")) return 2;
        int 찾은여부 = -1, 빈여부 = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] == 0) 빈여부 = Loop_INDEX;
            if (이름길이[Loop_INDEX] != daxiletmə_COUNT) continue;
            boolean MATCH = true; for (int daxili_qoşulma_yerinə_qoymaq = 0; daxili_qoşulma_yerinə_qoymaq < daxiletmə_COUNT; daxili_qoşulma_yerinə_qoymaq++) if (변수이름[Loop_INDEX * 32 + daxili_qoşulma_yerinə_qoymaq] != 명령해석기.nişan_VALUE[lokal_Başla + daxili_qoşulma_yerinə_qoymaq]) MATCH = false;
            if (MATCH) 찾은여부 = Loop_INDEX;
        }
        if (silmək) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = 빈여부; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = daxiletmə_COUNT; VALUE_uzunluq[찾은여부] = bitirmək_yerinə_qoymaq - 같음자리 - 1;
        for (int Loop_INDEX = 0; Loop_INDEX < daxiletmə_COUNT; Loop_INDEX++) 변수이름[찾은여부 * 32 + Loop_INDEX] = 명령해석기.nişan_VALUE[lokal_Başla + Loop_INDEX];
        for (int Loop_INDEX = 같음자리 + 1; Loop_INDEX < bitirmək_yerinə_qoymaq; Loop_INDEX++) 변수값[찾은여부 * 256 + Loop_INDEX - 같음자리 - 1] = 명령해석기.nişan_VALUE[Loop_INDEX];
        return 0;
    }
    static void 환경보기() {
        단말.Yazma("HOME=/\nPWD="); Yaddaş_Fayllar.현재쓰기(); 단말.문자(10);
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] > 0) {
            for (int daxili_qoşulma_yerinə_qoymaq = 0; daxili_qoşulma_yerinə_qoymaq < 이름길이[Loop_INDEX]; daxili_qoşulma_yerinə_qoymaq++) lövhə.직렬쓰기(변수이름[Loop_INDEX * 32 + daxili_qoşulma_yerinə_qoymaq]); 단말.문자('=');
            for (int daxili_qoşulma_yerinə_qoymaq = 0; daxili_qoşulma_yerinə_qoymaq < VALUE_uzunluq[Loop_INDEX]; daxili_qoşulma_yerinə_qoymaq++) lövhə.직렬쓰기(변수값[Loop_INDEX * 256 + daxili_qoşulma_yerinə_qoymaq]); 단말.문자(10);
        }
    }
    static void icra_etmək_əmr(int[] verilənlər_ARRAY, int 시작변위, int daxiletmə_COUNT, int 중첩깊이) {
        if (중첩깊이 >= 4 || daxiletmə_COUNT > 4096) { XƏTA("Əmr 파일의 iç_içə_yerləşdirmə_VALUE 또는 Giriş uzunluq_VALUE 제한을 넘었습니다"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < daxiletmə_COUNT; Loop_INDEX++) QAYNAQ[중첩깊이 * 4096 + Loop_INDEX] = verilənlər_ARRAY[시작변위 + Loop_INDEX];
        int 총수 = Oxuma(daxiletmə_COUNT, 중첩깊이); if (총수 < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < 총수) {
            int Qrup_bitirmək = 읽는자리;
            while (Qrup_bitirmək < 총수 && (종류[중첩깊이 * 128 + Qrup_bitirmək] == 0 || 종류[중첩깊이 * 128 + Qrup_bitirmək] >= 4)) Qrup_bitirmək++;
            boolean icra_etmək = 조건성립 == 1 || 조건성립 == 2 && vəziyyət_VALUE == 0 || 조건성립 == 3 && vəziyyət_VALUE != 0;
            if (icra_etmək) {
                boolean 이전자리 = false;
                while (읽는자리 < Qrup_bitirmək) {
                    int Sonrakı_yerinə_qoymaq = 읽는자리; while (Sonrakı_yerinə_qoymaq < Qrup_bitirmək && 종류[중첩깊이 * 128 + Sonrakı_yerinə_qoymaq] != 4) Sonrakı_yerinə_qoymaq++;
                    boolean QOŞUN_axın = Sonrakı_yerinə_qoymaq < Qrup_bitirmək; int 입력쪽 = -1, 출력쪽 = -1, 출력방식 = 0;
                    명령해석기.nişan_COUNT = 0; 쓴수 = 0; genişlənmə_səhv = false;
                    for (int Loop_INDEX = 읽는자리; Loop_INDEX < Sonrakı_yerinə_qoymaq; Loop_INDEX++) {
                        int 자료종류 = 종류[중첩깊이 * 128 + Loop_INDEX];
                        if (자료종류 >= 5) { if (자료종류 == 7) { if (입력쪽 >= 0) { XƏTA("입력 전환이 겹쳤습니다"); return; } 입력쪽 = ++Loop_INDEX; } else { if (출력쪽 >= 0) { XƏTA("출력 전환이 겹쳤습니다"); return; } 출력쪽 = ++Loop_INDEX; 출력방식 = 자료종류; } continue; }
                        if (명령해석기.nişan_COUNT == 32) { XƏTA("인수가 너무 많습니다"); return; }
                        int arqument_INDEX = 명령해석기.nişan_COUNT++; 명령해석기.시작점[arqument_INDEX] = 쓴수;
                        if (!Söz_VALUE(Loop_INDEX, 중첩깊이)) return;
                        명령해석기.uzunluq_VALUE[arqument_INDEX] = 쓴수 - 명령해석기.시작점[arqument_INDEX];
                    }
                    연결중 = 이전자리 || QOŞUN_axın || 입력쪽 >= 0 || 출력쪽 >= 0;
                    if (연결중 && (명령해석기.같음(0, "vi") || 명령해석기.같음(0, "edit") || 명령해석기.같음(0, "load") || 명령해석기.같음(0, "gui") || 명령해석기.같음(0, "terminal") || 명령해석기.같음(0, "sh") || 명령해석기.같음(0, "source"))) { XƏTA("interaktiv 명령과 Əmr 파일은 giriş_çıxış 전환이나 axın_VALUE 연결에 쓸 수 없습니다"); return; }
                    셸입출력.İcra_Et(이전자리, QOŞUN_axın);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int daxiletmə_yerinə_qoymaq = 입출력바꿈 == 0 ? 입력쪽 : 출력쪽; if (daxiletmə_yerinə_qoymaq < 0) continue;
                        int Başla_yerinə_qoymaq = 쓴수; if (!Söz_VALUE(daxiletmə_yerinə_qoymaq, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = Yaddaş_Fayllar.yol_Başla(쓴수 - Başla_yerinə_qoymaq);
                        for (int daxili_qoşulma_yerinə_qoymaq = Başla_yerinə_qoymaq; 처리값 >= 0 && daxili_qoşulma_yerinə_qoymaq < 쓴수; daxili_qoşulma_yerinə_qoymaq++) 처리값 = Yaddaş_Fayllar.yol_bayt(daxili_qoşulma_yerinə_qoymaq - Başla_yerinə_qoymaq, 명령해석기.nişan_VALUE[daxili_qoşulma_yerinə_qoymaq]);
                        if (처리값 >= 0) 처리값 = Yaddaş_Fayllar.Aç(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); 명령해석기.XƏTA(처리값); vəziyyət_VALUE = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.입력파일 = 처리값; else 셸입출력.Çıxan_fayl = 처리값;
                    }
                    셸입출력.İcazə_ver_interaktiv = 중첩깊이 == 0 && 읽는자리 == 0 && Sonrakı_yerinə_qoymaq == 총수;
                    깊이 = 중첩깊이; 명령해석기.ölçü = 0; lövhə.입출력전환(1);
                    명령해석기.Əmr();
                    lövhə.Terminal(3);
                    int 반환값 = 명령해석기.ölçü, axın_səhv = 셸입출력.xəta_VALUE;
                    셸입출력.끝(); 연결중 = false;
                    vəziyyət_VALUE = axın_səhv < 0 ? 1 : 반환값;
                    if (axın_səhv < 0) { 명령해석기.XƏTA(axın_səhv); return; }
                    if (skript_bitirmək || 반환값 == -1005) return;
                    이전자리 = true; 읽는자리 = Sonrakı_yerinə_qoymaq + 1;
                }
            }
            if (Qrup_bitirmək < 총수) 조건성립 = 종류[중첩깊이 * 128 + Qrup_bitirmək];
            읽는자리 = Qrup_bitirmək + 1;
        }
    }
    static void icra_etmək_fayl() {
        if (명령해석기.nişan_COUNT != 2 || 깊이 >= 3) { 명령해석기.ölçü = 2; 단말.Yazma("사용법: sh FAYL (iç_içə_yerləşdirmə_VALUE 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = 명령해석기.Cığır(1); if (처리값 >= 0) 처리값 = Yaddaş_Fayllar.Aç(0);
        if (처리값 < 0) { 명령해석기.XƏTA(처리값); return; }
        int daxiletmə_COUNT = 0, bayt_verilənlər;
        while ((bayt_verilənlər = Yaddaş_Fayllar.Oxuma(처리값)) != 256 && bayt_verilənlər >= 0 && daxiletmə_COUNT < 16384) skript_VALUE[중첩깊이 * 16384 + daxiletmə_COUNT++] = bayt_verilənlər;
        Yaddaş_Fayllar.Bağla(처리값); lövhə.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < daxiletmə_COUNT && !skript_bitirmək;) {
            int bitirmək_yerinə_qoymaq = 읽는자리; while (bitirmək_yerinə_qoymaq < daxiletmə_COUNT && skript_VALUE[중첩깊이 * 16384 + bitirmək_yerinə_qoymaq] != 10) bitirmək_yerinə_qoymaq++;
            int 유효길이 = bitirmək_yerinə_qoymaq - 읽는자리; if (유효길이 > 0 && skript_VALUE[중첩깊이 * 16384 + bitirmək_yerinə_qoymaq - 1] == 13) 유효길이--;
            icra_etmək_əmr(skript_VALUE, 중첩깊이 * 16384 + 읽는자리, 유효길이, 중첩깊이); 읽는자리 = bitirmək_yerinə_qoymaq + 1;
        }
        명령해석기.ölçü = vəziyyət_VALUE; skript_bitirmək = false; 깊이 = 중첩깊이 - 1;
    }
}
