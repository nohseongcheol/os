// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 Tirisano setlhalosataelo 문법. 파이프는 순차 diragatsa_Taelo, 환경은 같은 셸에서 공유한다. */
public final class setlhalosataelo_popapolelo {
    static int[] Motswedi = new int[4 * 4096], 종류 = new int[4 * 128], dirisa = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] 변수이름 = new int[16 * 32], 변수값 = new int[16 * 256], 이름길이 = new int[16], Boleng_boleele = new int[16];
    static int[] Sekeripiti_Boleng = new int[4 * 16384];
    static int kemo_Boleng, 깊이, 쓴수;
    static boolean 연결중, Sekeripiti_kgaola, katoloso_phoso;
    static boolean leina_Letshwao(int khoutuletshwao) { return khoutuletshwao >= 'a' && khoutuletshwao <= 'z' || khoutuletshwao >= 'A' && khoutuletshwao <= 'Z' || khoutuletshwao == '_' || khoutuletshwao >= 128; }
    static boolean 이름뒤(int khoutuletshwao) { return leina_Letshwao(khoutuletshwao) || khoutuletshwao >= '0' && khoutuletshwao <= '9'; }
    static void phoso(String SMS) { 보드.입출력전환(0); 단말.kwala("Taelo go_lokolola_Boleng: "); 단말.kwala(SMS); 단말.문자(10); kemo_Boleng = 2; }
    static int 읽기(int 항목수, int 중첩깊이) {
        int ga_jaana_tshupane = 0, 총수 = 0, 기준자리 = 중첩깊이 * 4096, letshwao_le_le_kgethegileng = 중첩깊이 * 128;
        while (ga_jaana_tshupane < 항목수) {
            while (ga_jaana_tshupane < 항목수 && (Motswedi[기준자리 + ga_jaana_tshupane] == 32 || Motswedi[기준자리 + ga_jaana_tshupane] == 9)) ga_jaana_tshupane++;
            if (ga_jaana_tshupane == 항목수 || Motswedi[기준자리 + ga_jaana_tshupane] == '#') break;
            if (총수 == 128) { phoso("낱말이 너무 많습니다"); return -1; }
            int 시작자리 = ga_jaana_tshupane, khoutuletshwao = Motswedi[기준자리 + ga_jaana_tshupane], 자료종류 = 0;
            if (khoutuletshwao == ';') { 자료종류 = 1; ga_jaana_tshupane++; }
            else if (khoutuletshwao == '&') { if (ga_jaana_tshupane + 1 >= 항목수 || Motswedi[기준자리 + ga_jaana_tshupane + 1] != '&') { phoso("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } 자료종류 = 2; ga_jaana_tshupane += 2; }
            else if (khoutuletshwao == '|') { ga_jaana_tshupane++; 자료종류 = ga_jaana_tshupane < 항목수 && Motswedi[기준자리 + ga_jaana_tshupane] == '|' ? 3 : 4; if (자료종류 == 3) ga_jaana_tshupane++; }
            else if (khoutuletshwao == '>') { ga_jaana_tshupane++; 자료종류 = ga_jaana_tshupane < 항목수 && Motswedi[기준자리 + ga_jaana_tshupane] == '>' ? 6 : 5; if (자료종류 == 6) ga_jaana_tshupane++; }
            else if (khoutuletshwao == '<') { 자료종류 = 7; ga_jaana_tshupane++; }
            else {
                int 따옴표 = 0;
                while (ga_jaana_tshupane < 항목수) {
                    khoutuletshwao = Motswedi[기준자리 + ga_jaana_tshupane];
                    if (khoutuletshwao == '`' && 따옴표 != 39 || khoutuletshwao == '$' && 따옴표 != 39 && ga_jaana_tshupane + 1 < 항목수 && Motswedi[기준자리 + ga_jaana_tshupane + 1] == '(') { phoso("Taelo 결과 치환은 지원하지 않습니다"); return -1; }
                    if (khoutuletshwao == '\\' && 따옴표 != 39) { if (++ga_jaana_tshupane == 항목수) { phoso("Mola 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } ga_jaana_tshupane++; continue; }
                    if (khoutuletshwao == 따옴표) { 따옴표 = 0; ga_jaana_tshupane++; continue; }
                    if (따옴표 == 0 && (khoutuletshwao == 39 || khoutuletshwao == 34)) { 따옴표 = khoutuletshwao; ga_jaana_tshupane++; continue; }
                    if (따옴표 == 0 && (khoutuletshwao == 32 || khoutuletshwao == 9 || khoutuletshwao == ';' || khoutuletshwao == '&' || khoutuletshwao == '|' || khoutuletshwao == '<' || khoutuletshwao == '>')) break;
                    ga_jaana_tshupane++;
                }
                if (따옴표 != 0) { phoso("따옴표가 닫히지 않았습니다"); return -1; }
                if (ga_jaana_tshupane < 항목수 && (Motswedi[기준자리 + ga_jaana_tshupane] == '>' || Motswedi[기준자리 + ga_jaana_tshupane] == '<')) {
                    boolean 수치 = ga_jaana_tshupane > 시작자리;
                    for (int lupu_tshupane = 시작자리; lupu_tshupane < ga_jaana_tshupane; lupu_tshupane++) if (Motswedi[기준자리 + lupu_tshupane] < '0' || Motswedi[기준자리 + lupu_tshupane] > '9') 수치 = false;
                    if (수치) { phoso("번호를 지정한 faele 서술자 I_O 전환은 지원하지 않습니다"); return -1; }
                }
            }
            종류[letshwao_le_le_kgethegileng + 총수] = 자료종류; dirisa[letshwao_le_le_kgethegileng + 총수] = 시작자리; 끝[letshwao_le_le_kgethegileng + 총수] = ga_jaana_tshupane; 총수++;
        }
        boolean 낱말 = false;
        for (int lupu_tshupane = 0; lupu_tshupane < 총수; lupu_tshupane++) {
            int 임시값 = 종류[letshwao_le_le_kgethegileng + lupu_tshupane];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++lupu_tshupane == 총수 || 종류[letshwao_le_le_kgethegileng + lupu_tshupane] != 0) { phoso("I_O 전환에 faele 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || lupu_tshupane == 총수 - 1 && 임시값 != 1) { phoso("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (총수 > 0 && !낱말 && 종류[letshwao_le_le_kgethegileng + 총수 - 1] != 1) { phoso("명령이 빠졌습니다"); return -1; }
        return 총수;
    }
    static boolean 구간말(int[] tshedimosetso_setlhopha, int e_e_gaufi_simolola, int 항목수, String 문자위치) {
        if (항목수 != 문자위치.length()) return false; for (int lupu_tshupane = 0; lupu_tshupane < 항목수; lupu_tshupane++) if (tshedimosetso_setlhopha[e_e_gaufi_simolola + lupu_tshupane] != 문자위치.charAt(lupu_tshupane)) return false; return true;
    }
    static void 넣기(int baete_tshedimosetso) {
        if (쓴수 >= 명령해석기.papetlana_Boleng.length) { if (!katoloso_phoso) phoso("변수를 펼친 명령이 너무 깁니다"); katoloso_phoso = true; return; }
        명령해석기.papetlana_Boleng[쓴수++] = baete_tshedimosetso;
    }
    static void 변수(int[] tshedimosetso_setlhopha, int 시작자리, int 항목수) {
        if (구간말(tshedimosetso_setlhopha, 시작자리, 항목수, "PWD")) { 넣기('/'); for (int lupu_tshupane = 0; lupu_tshupane < memori_Difaele.ga_jaana_boleele; lupu_tshupane++) 넣기(memori_Difaele.ga_jaana_selwana[lupu_tshupane]); return; }
        if (구간말(tshedimosetso_setlhopha, 시작자리, 항목수, "HOME")) { 넣기('/'); return; }
        if (구간말(tshedimosetso_setlhopha, 시작자리, 항목수, "?")) {
            int tshedimosetso_Boleng = kemo_Boleng, dijite = 100; boolean 시작여부 = false;
            while (dijite > 0) { int 뒷값 = tshedimosetso_Boleng / dijite; if (뒷값 != 0 || 시작여부 || dijite == 1) { 넣기('0' + 뒷값); 시작여부 = true; } tshedimosetso_Boleng %= dijite; dijite /= 10; } return;
        }
        for (int lupu_tshupane = 0; lupu_tshupane < 16; lupu_tshupane++) if (이름길이[lupu_tshupane] == 항목수) {
            boolean 일치여부 = true; for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) if (변수이름[lupu_tshupane * 32 + 안쪽자리] != tshedimosetso_setlhopha[시작자리 + 안쪽자리]) 일치여부 = false;
            if (일치여부) { for (int 안쪽자리 = 0; 안쪽자리 < Boleng_boleele[lupu_tshupane]; 안쪽자리++) 넣기(변수값[lupu_tshupane * 256 + 안쪽자리]); return; }
        }
    }
    static boolean Lefoko_Boleng(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = dirisa[중첩깊이 * 128 + 낱말번호], 끝자리 = 끝[중첩깊이 * 128 + 낱말번호], 기준자리 = 중첩깊이 * 4096, 따옴표 = 0;
        if (읽는자리 < 끝자리 && Motswedi[기준자리 + 읽는자리] == '~' && (읽는자리 + 1 == 끝자리 || Motswedi[기준자리 + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < 끝자리) {
            int khoutuletshwao = Motswedi[기준자리 + 읽는자리++];
            if (khoutuletshwao == 따옴표) { 따옴표 = 0; continue; }
            if (따옴표 == 0 && (khoutuletshwao == 39 || khoutuletshwao == 34)) { 따옴표 = khoutuletshwao; continue; }
            if (khoutuletshwao == '\\' && 따옴표 != 39) { int 다음자리 = Motswedi[기준자리 + 읽는자리++]; if (따옴표 == 34 && 다음자리 != '$' && 다음자리 != '"' && 다음자리 != '\\') 넣기('\\'); 넣기(다음자리); continue; }
            if (khoutuletshwao == '$' && 따옴표 != 39 && 읽는자리 < 끝자리) {
                boolean 중괄호자리 = Motswedi[기준자리 + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < 끝자리 && Motswedi[기준자리 + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < 끝자리 && 이름뒤(Motswedi[기준자리 + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == 끝자리 || Motswedi[기준자리 + 읽는자리] != '}')) { phoso("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                변수(Motswedi, 기준자리 + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(khoutuletshwao);
        }
        return !katoloso_phoso;
    }
    static int 환경설정(int Thulaganyo_tshupane, boolean tlosa) {
        int e_e_gaufi_simolola = 명령해석기.시작점[Thulaganyo_tshupane], 끝자리 = e_e_gaufi_simolola + 명령해석기.boleele_Boleng[Thulaganyo_tshupane], 같음자리 = e_e_gaufi_simolola;
        while (같음자리 < 끝자리 && 명령해석기.papetlana_Boleng[같음자리] != '=') 같음자리++;
        int 항목수 = 같음자리 - e_e_gaufi_simolola;
        if (항목수 < 1 || 항목수 > 31 || !leina_Letshwao(명령해석기.papetlana_Boleng[e_e_gaufi_simolola]) || !tlosa && 같음자리 == 끝자리 || 끝자리 - 같음자리 - 1 > 255) return 2;
        for (int lupu_tshupane = e_e_gaufi_simolola; lupu_tshupane < 같음자리; lupu_tshupane++) if (!이름뒤(명령해석기.papetlana_Boleng[lupu_tshupane])) return 2;
        if (구간말(명령해석기.papetlana_Boleng, e_e_gaufi_simolola, 항목수, "PWD") || 구간말(명령해석기.papetlana_Boleng, e_e_gaufi_simolola, 항목수, "HOME")) return 2;
        int 찾은여부 = -1, 빈여부 = -1;
        for (int lupu_tshupane = 0; lupu_tshupane < 16; lupu_tshupane++) {
            if (이름길이[lupu_tshupane] == 0) 빈여부 = lupu_tshupane;
            if (이름길이[lupu_tshupane] != 항목수) continue;
            boolean 일치여부 = true; for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) if (변수이름[lupu_tshupane * 32 + 안쪽자리] != 명령해석기.papetlana_Boleng[e_e_gaufi_simolola + 안쪽자리]) 일치여부 = false;
            if (일치여부) 찾은여부 = lupu_tshupane;
        }
        if (tlosa) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = 빈여부; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = 항목수; Boleng_boleele[찾은여부] = 끝자리 - 같음자리 - 1;
        for (int lupu_tshupane = 0; lupu_tshupane < 항목수; lupu_tshupane++) 변수이름[찾은여부 * 32 + lupu_tshupane] = 명령해석기.papetlana_Boleng[e_e_gaufi_simolola + lupu_tshupane];
        for (int lupu_tshupane = 같음자리 + 1; lupu_tshupane < 끝자리; lupu_tshupane++) 변수값[찾은여부 * 256 + lupu_tshupane - 같음자리 - 1] = 명령해석기.papetlana_Boleng[lupu_tshupane];
        return 0;
    }
    static void 환경보기() {
        단말.kwala("HOME=/\nPWD="); memori_Difaele.ga_jaana_kwala(); 단말.문자(10);
        for (int lupu_tshupane = 0; lupu_tshupane < 16; lupu_tshupane++) if (이름길이[lupu_tshupane] > 0) {
            for (int 안쪽자리 = 0; 안쪽자리 < 이름길이[lupu_tshupane]; 안쪽자리++) 보드.직렬쓰기(변수이름[lupu_tshupane * 32 + 안쪽자리]); 단말.문자('=');
            for (int 안쪽자리 = 0; 안쪽자리 < Boleng_boleele[lupu_tshupane]; 안쪽자리++) 보드.직렬쓰기(변수값[lupu_tshupane * 256 + 안쪽자리]); 단말.문자(10);
        }
    }
    static void diragatsa_Taelo(int[] tshedimosetso_setlhopha, int 시작변위, int 항목수, int 중첩깊이) {
        if (중첩깊이 >= 4 || 항목수 > 4096) { phoso("Taelo 파일의 중첩 또는 Mola boleele_Boleng 제한을 넘었습니다"); return; }
        for (int lupu_tshupane = 0; lupu_tshupane < 항목수; lupu_tshupane++) Motswedi[중첩깊이 * 4096 + lupu_tshupane] = tshedimosetso_setlhopha[시작변위 + lupu_tshupane];
        int 총수 = 읽기(항목수, 중첩깊이); if (총수 < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < 총수) {
            int setlhopha_kgaola = 읽는자리;
            while (setlhopha_kgaola < 총수 && (종류[중첩깊이 * 128 + setlhopha_kgaola] == 0 || 종류[중첩깊이 * 128 + setlhopha_kgaola] >= 4)) setlhopha_kgaola++;
            boolean diragatsa = 조건성립 == 1 || 조건성립 == 2 && kemo_Boleng == 0 || 조건성립 == 3 && kemo_Boleng != 0;
            if (diragatsa) {
                boolean 이전자리 = false;
                while (읽는자리 < setlhopha_kgaola) {
                    int 다음자리 = 읽는자리; while (다음자리 < setlhopha_kgaola && 종류[중첩깊이 * 128 + 다음자리] != 4) 다음자리++;
                    boolean Golaganya_moela = 다음자리 < setlhopha_kgaola; int 입력쪽 = -1, 출력쪽 = -1, 출력방식 = 0;
                    명령해석기.토큰수 = 0; 쓴수 = 0; katoloso_phoso = false;
                    for (int lupu_tshupane = 읽는자리; lupu_tshupane < 다음자리; lupu_tshupane++) {
                        int 자료종류 = 종류[중첩깊이 * 128 + lupu_tshupane];
                        if (자료종류 >= 5) { if (자료종류 == 7) { if (입력쪽 >= 0) { phoso("입력 전환이 겹쳤습니다"); return; } 입력쪽 = ++lupu_tshupane; } else { if (출력쪽 >= 0) { phoso("출력 전환이 겹쳤습니다"); return; } 출력쪽 = ++lupu_tshupane; 출력방식 = 자료종류; } continue; }
                        if (명령해석기.토큰수 == 32) { phoso("인수가 너무 많습니다"); return; }
                        int Thulaganyo_tshupane = 명령해석기.토큰수++; 명령해석기.시작점[Thulaganyo_tshupane] = 쓴수;
                        if (!Lefoko_Boleng(lupu_tshupane, 중첩깊이)) return;
                        명령해석기.boleele_Boleng[Thulaganyo_tshupane] = 쓴수 - 명령해석기.시작점[Thulaganyo_tshupane];
                    }
                    연결중 = 이전자리 || Golaganya_moela || 입력쪽 >= 0 || 출력쪽 >= 0;
                    if (연결중 && (명령해석기.같음(0, "vi") || 명령해석기.같음(0, "edit") || 명령해석기.같음(0, "load") || 명령해석기.같음(0, "gui") || 명령해석기.같음(0, "terminal") || 명령해석기.같음(0, "sh") || 명령해석기.같음(0, "source"))) { phoso("Tirisano 명령과 Taelo 파일은 I_O 전환이나 moela_Boleng 연결에 쓸 수 없습니다"); return; }
                    셸입출력.dirisa(이전자리, Golaganya_moela);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int 항목자리 = 입출력바꿈 == 0 ? 입력쪽 : 출력쪽; if (항목자리 < 0) continue;
                        int 시작자리 = 쓴수; if (!Lefoko_Boleng(항목자리, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = memori_Difaele.tsela_simolola(쓴수 - 시작자리);
                        for (int 안쪽자리 = 시작자리; 처리값 >= 0 && 안쪽자리 < 쓴수; 안쪽자리++) 처리값 = memori_Difaele.tsela_baete(안쪽자리 - 시작자리, 명령해석기.papetlana_Boleng[안쪽자리]);
                        if (처리값 >= 0) 처리값 = memori_Difaele.bula(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); 명령해석기.phoso(처리값); kemo_Boleng = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.입력파일 = 처리값; else 셸입출력.Faele_ya_Tiro_e_e_Dirilweng = 처리값;
                    }
                    셸입출력.letla_Tirisano = 중첩깊이 == 0 && 읽는자리 == 0 && 다음자리 == 총수;
                    깊이 = 중첩깊이; 명령해석기.결과 = 0; 보드.입출력전환(1);
                    명령해석기.Taelo();
                    보드.터미널(3);
                    int 반환값 = 명령해석기.결과, moela_phoso = 셸입출력.palelo_Boleng;
                    셸입출력.끝(); 연결중 = false;
                    kemo_Boleng = moela_phoso < 0 ? 1 : 반환값;
                    if (moela_phoso < 0) { 명령해석기.phoso(moela_phoso); return; }
                    if (Sekeripiti_kgaola || 반환값 == -1005) return;
                    이전자리 = true; 읽는자리 = 다음자리 + 1;
                }
            }
            if (setlhopha_kgaola < 총수) 조건성립 = 종류[중첩깊이 * 128 + setlhopha_kgaola];
            읽는자리 = setlhopha_kgaola + 1;
        }
    }
    static void diragatsa_faele() {
        if (명령해석기.토큰수 != 2 || 깊이 >= 3) { 명령해석기.결과 = 2; 단말.kwala("사용법: sh faele (중첩 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = 명령해석기.tsela(1); if (처리값 >= 0) 처리값 = memori_Difaele.bula(0);
        if (처리값 < 0) { 명령해석기.phoso(처리값); return; }
        int 항목수 = 0, baete_tshedimosetso;
        while ((baete_tshedimosetso = memori_Difaele.읽기(처리값)) != 256 && baete_tshedimosetso >= 0 && 항목수 < 16384) Sekeripiti_Boleng[중첩깊이 * 16384 + 항목수++] = baete_tshedimosetso;
        memori_Difaele.tswala(처리값); 보드.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < 항목수 && !Sekeripiti_kgaola;) {
            int 끝자리 = 읽는자리; while (끝자리 < 항목수 && Sekeripiti_Boleng[중첩깊이 * 16384 + 끝자리] != 10) 끝자리++;
            int 유효길이 = 끝자리 - 읽는자리; if (유효길이 > 0 && Sekeripiti_Boleng[중첩깊이 * 16384 + 끝자리 - 1] == 13) 유효길이--;
            diragatsa_Taelo(Sekeripiti_Boleng, 중첩깊이 * 16384 + 읽는자리, 유효길이, 중첩깊이); 읽는자리 = 끝자리 + 1;
        }
        명령해석기.결과 = kemo_Boleng; Sekeripiti_kgaola = false; 깊이 = 중첩깊이 - 1;
    }
}
