// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 duglante Wëreef 문법. 파이프는 순차 def_ndigel, 환경은 같은 셸에서 공유한다. */
public final class Wëreef_tëgg_waxin {
    static int[] Cosaan = new int[4 * 4096], 종류 = new int[4 * 128], daw = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] 변수이름 = new int[16 * 32], 변수값 = new int[16 * 256], 이름길이 = new int[16], xëyma_diir = new int[16];
    static int[] ndigali_doxalin_xëyma = new int[4 * 16384];
    static int nekkin_xëyma, 깊이, 쓴수;
    static boolean 연결중, ndigali_doxalin_jeexal, ñàmbaas_njumte;
    static boolean tur_Araf(int kotu_araf) { return kotu_araf >= 'a' && kotu_araf <= 'z' || kotu_araf >= 'A' && kotu_araf <= 'Z' || kotu_araf == '_' || kotu_araf >= 128; }
    static boolean 이름뒤(int kotu_araf) { return tur_Araf(kotu_araf) || kotu_araf >= '0' && kotu_araf <= '9'; }
    static void njumte(String Tekst) { 보드.입출력전환(0); 단말.biir("ndigel Segg_xëyma: "); 단말.biir(Tekst); 단말.문자(10); nekkin_xëyma = 2; }
    static int 읽기(int 항목수, int 중첩깊이) {
        int 현재자리 = 0, 총수 = 0, 기준자리 = 중첩깊이 * 4096, araf_bu_ràññeeku = 중첩깊이 * 128;
        while (현재자리 < 항목수) {
            while (현재자리 < 항목수 && (Cosaan[기준자리 + 현재자리] == 32 || Cosaan[기준자리 + 현재자리] == 9)) 현재자리++;
            if (현재자리 == 항목수 || Cosaan[기준자리 + 현재자리] == '#') break;
            if (총수 == 128) { njumte("낱말이 너무 많습니다"); return -1; }
            int 시작자리 = 현재자리, kotu_araf = Cosaan[기준자리 + 현재자리], 자료종류 = 0;
            if (kotu_araf == ';') { 자료종류 = 1; 현재자리++; }
            else if (kotu_araf == '&') { if (현재자리 + 1 >= 항목수 || Cosaan[기준자리 + 현재자리 + 1] != '&') { njumte("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } 자료종류 = 2; 현재자리 += 2; }
            else if (kotu_araf == '|') { 현재자리++; 자료종류 = 현재자리 < 항목수 && Cosaan[기준자리 + 현재자리] == '|' ? 3 : 4; if (자료종류 == 3) 현재자리++; }
            else if (kotu_araf == '>') { 현재자리++; 자료종류 = 현재자리 < 항목수 && Cosaan[기준자리 + 현재자리] == '>' ? 6 : 5; if (자료종류 == 6) 현재자리++; }
            else if (kotu_araf == '<') { 자료종류 = 7; 현재자리++; }
            else {
                int 따옴표 = 0;
                while (현재자리 < 항목수) {
                    kotu_araf = Cosaan[기준자리 + 현재자리];
                    if (kotu_araf == '`' && 따옴표 != 39 || kotu_araf == '$' && 따옴표 != 39 && 현재자리 + 1 < 항목수 && Cosaan[기준자리 + 현재자리 + 1] == '(') { njumte("ndigel 결과 치환은 지원하지 않습니다"); return -1; }
                    if (kotu_araf == '\\' && 따옴표 != 39) { if (++현재자리 == 항목수) { njumte("buum 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } 현재자리++; continue; }
                    if (kotu_araf == 따옴표) { 따옴표 = 0; 현재자리++; continue; }
                    if (따옴표 == 0 && (kotu_araf == 39 || kotu_araf == 34)) { 따옴표 = kotu_araf; 현재자리++; continue; }
                    if (따옴표 == 0 && (kotu_araf == 32 || kotu_araf == 9 || kotu_araf == ';' || kotu_araf == '&' || kotu_araf == '|' || kotu_araf == '<' || kotu_araf == '>')) break;
                    현재자리++;
                }
                if (따옴표 != 0) { njumte("따옴표가 닫히지 않았습니다"); return -1; }
                if (현재자리 < 항목수 && (Cosaan[기준자리 + 현재자리] == '>' || Cosaan[기준자리 + 현재자리] == '<')) {
                    boolean 수치 = 현재자리 > 시작자리;
                    for (int wërngël_àlluwa_tur = 시작자리; wërngël_àlluwa_tur < 현재자리; wërngël_àlluwa_tur++) if (Cosaan[기준자리 + wërngël_àlluwa_tur] < '0' || Cosaan[기준자리 + wërngël_àlluwa_tur] > '9') 수치 = false;
                    if (수치) { njumte("번호를 지정한 bara_denc 서술자 D_G 전환은 지원하지 않습니다"); return -1; }
                }
            }
            종류[araf_bu_ràññeeku + 총수] = 자료종류; daw[araf_bu_ràññeeku + 총수] = 시작자리; 끝[araf_bu_ràññeeku + 총수] = 현재자리; 총수++;
        }
        boolean 낱말 = false;
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 총수; wërngël_àlluwa_tur++) {
            int 임시값 = 종류[araf_bu_ràññeeku + wërngël_àlluwa_tur];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++wërngël_àlluwa_tur == 총수 || 종류[araf_bu_ràññeeku + wërngël_àlluwa_tur] != 0) { njumte("D_G 전환에 bara_denc 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || wërngël_àlluwa_tur == 총수 - 1 && 임시값 != 1) { njumte("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (총수 > 0 && !낱말 && 종류[araf_bu_ràññeeku + 총수 - 1] != 1) { njumte("명령이 빠졌습니다"); return -1; }
        return 총수;
    }
    static boolean 구간말(int[] mbir_TABLO, int dënnd_Door, int 항목수, String 문자위치) {
        if (항목수 != 문자위치.length()) return false; for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 항목수; wërngël_àlluwa_tur++) if (mbir_TABLO[dënnd_Door + wërngël_àlluwa_tur] != 문자위치.charAt(wërngël_àlluwa_tur)) return false; return true;
    }
    static void 넣기(int okte_mbir) {
        if (쓴수 >= 명령해석기.jeton_xëyma.length) { if (!ñàmbaas_njumte) njumte("변수를 펼친 명령이 너무 깁니다"); ñàmbaas_njumte = true; return; }
        명령해석기.jeton_xëyma[쓴수++] = okte_mbir;
    }
    static void 변수(int[] mbir_TABLO, int 시작자리, int 항목수) {
        if (구간말(mbir_TABLO, 시작자리, 항목수, "PWD")) { 넣기('/'); for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < fatlekookaay_Fisiye_yi.현재길이; wërngël_àlluwa_tur++) 넣기(fatlekookaay_Fisiye_yi.현재[wërngël_àlluwa_tur]); return; }
        if (구간말(mbir_TABLO, 시작자리, 항목수, "HOME")) { 넣기('/'); return; }
        if (구간말(mbir_TABLO, 시작자리, 항목수, "?")) {
            int mbir_xëyma = nekkin_xëyma, siifar = 100; boolean 시작여부 = false;
            while (siifar > 0) { int 뒷값 = mbir_xëyma / siifar; if (뒷값 != 0 || 시작여부 || siifar == 1) { 넣기('0' + 뒷값); 시작여부 = true; } mbir_xëyma %= siifar; siifar /= 10; } return;
        }
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 16; wërngël_àlluwa_tur++) if (이름길이[wërngël_àlluwa_tur] == 항목수) {
            boolean 일치여부 = true; for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) if (변수이름[wërngël_àlluwa_tur * 32 + 안쪽자리] != mbir_TABLO[시작자리 + 안쪽자리]) 일치여부 = false;
            if (일치여부) { for (int 안쪽자리 = 0; 안쪽자리 < xëyma_diir[wërngël_àlluwa_tur]; 안쪽자리++) 넣기(변수값[wërngël_àlluwa_tur * 256 + 안쪽자리]); return; }
        }
    }
    static boolean Word_xëyma(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = daw[중첩깊이 * 128 + 낱말번호], 끝자리 = 끝[중첩깊이 * 128 + 낱말번호], 기준자리 = 중첩깊이 * 4096, 따옴표 = 0;
        if (읽는자리 < 끝자리 && Cosaan[기준자리 + 읽는자리] == '~' && (읽는자리 + 1 == 끝자리 || Cosaan[기준자리 + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < 끝자리) {
            int kotu_araf = Cosaan[기준자리 + 읽는자리++];
            if (kotu_araf == 따옴표) { 따옴표 = 0; continue; }
            if (따옴표 == 0 && (kotu_araf == 39 || kotu_araf == 34)) { 따옴표 = kotu_araf; continue; }
            if (kotu_araf == '\\' && 따옴표 != 39) { int 다음자리 = Cosaan[기준자리 + 읽는자리++]; if (따옴표 == 34 && 다음자리 != '$' && 다음자리 != '"' && 다음자리 != '\\') 넣기('\\'); 넣기(다음자리); continue; }
            if (kotu_araf == '$' && 따옴표 != 39 && 읽는자리 < 끝자리) {
                boolean 중괄호자리 = Cosaan[기준자리 + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < 끝자리 && Cosaan[기준자리 + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < 끝자리 && 이름뒤(Cosaan[기준자리 + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == 끝자리 || Cosaan[기준자리 + 읽는자리] != '}')) { njumte("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                변수(Cosaan, 기준자리 + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(kotu_araf);
        }
        return !ñàmbaas_njumte;
    }
    static int 환경설정(int Tegtal_àlluwa_tur, boolean dandal) {
        int dënnd_Door = 명령해석기.시작점[Tegtal_àlluwa_tur], 끝자리 = dënnd_Door + 명령해석기.diir_xëyma[Tegtal_àlluwa_tur], 같음자리 = dënnd_Door;
        while (같음자리 < 끝자리 && 명령해석기.jeton_xëyma[같음자리] != '=') 같음자리++;
        int 항목수 = 같음자리 - dënnd_Door;
        if (항목수 < 1 || 항목수 > 31 || !tur_Araf(명령해석기.jeton_xëyma[dënnd_Door]) || !dandal && 같음자리 == 끝자리 || 끝자리 - 같음자리 - 1 > 255) return 2;
        for (int wërngël_àlluwa_tur = dënnd_Door; wërngël_àlluwa_tur < 같음자리; wërngël_àlluwa_tur++) if (!이름뒤(명령해석기.jeton_xëyma[wërngël_àlluwa_tur])) return 2;
        if (구간말(명령해석기.jeton_xëyma, dënnd_Door, 항목수, "PWD") || 구간말(명령해석기.jeton_xëyma, dënnd_Door, 항목수, "HOME")) return 2;
        int 찾은여부 = -1, 빈여부 = -1;
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 16; wërngël_àlluwa_tur++) {
            if (이름길이[wërngël_àlluwa_tur] == 0) 빈여부 = wërngël_àlluwa_tur;
            if (이름길이[wërngël_àlluwa_tur] != 항목수) continue;
            boolean 일치여부 = true; for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) if (변수이름[wërngël_àlluwa_tur * 32 + 안쪽자리] != 명령해석기.jeton_xëyma[dënnd_Door + 안쪽자리]) 일치여부 = false;
            if (일치여부) 찾은여부 = wërngël_àlluwa_tur;
        }
        if (dandal) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = 빈여부; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = 항목수; xëyma_diir[찾은여부] = 끝자리 - 같음자리 - 1;
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 항목수; wërngël_àlluwa_tur++) 변수이름[찾은여부 * 32 + wërngël_àlluwa_tur] = 명령해석기.jeton_xëyma[dënnd_Door + wërngël_àlluwa_tur];
        for (int wërngël_àlluwa_tur = 같음자리 + 1; wërngël_àlluwa_tur < 끝자리; wërngël_àlluwa_tur++) 변수값[찾은여부 * 256 + wërngël_àlluwa_tur - 같음자리 - 1] = 명령해석기.jeton_xëyma[wërngël_àlluwa_tur];
        return 0;
    }
    static void 환경보기() {
        단말.biir("HOME=/\nPWD="); fatlekookaay_Fisiye_yi.현재쓰기(); 단말.문자(10);
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 16; wërngël_àlluwa_tur++) if (이름길이[wërngël_àlluwa_tur] > 0) {
            for (int 안쪽자리 = 0; 안쪽자리 < 이름길이[wërngël_àlluwa_tur]; 안쪽자리++) 보드.직렬쓰기(변수이름[wërngël_àlluwa_tur * 32 + 안쪽자리]); 단말.문자('=');
            for (int 안쪽자리 = 0; 안쪽자리 < xëyma_diir[wërngël_àlluwa_tur]; 안쪽자리++) 보드.직렬쓰기(변수값[wërngël_àlluwa_tur * 256 + 안쪽자리]); 단말.문자(10);
        }
    }
    static void def_ndigel(int[] mbir_TABLO, int 시작변위, int 항목수, int 중첩깊이) {
        if (중첩깊이 >= 4 || 항목수 > 4096) { njumte("ndigel 파일의 중첩 또는 buum diir_xëyma 제한을 넘었습니다"); return; }
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 항목수; wërngël_àlluwa_tur++) Cosaan[중첩깊이 * 4096 + wërngël_àlluwa_tur] = mbir_TABLO[시작변위 + wërngël_àlluwa_tur];
        int 총수 = 읽기(항목수, 중첩깊이); if (총수 < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < 총수) {
            int mboolo_jeexal = 읽는자리;
            while (mboolo_jeexal < 총수 && (종류[중첩깊이 * 128 + mboolo_jeexal] == 0 || 종류[중첩깊이 * 128 + mboolo_jeexal] >= 4)) mboolo_jeexal++;
            boolean 실행여부 = 조건성립 == 1 || 조건성립 == 2 && nekkin_xëyma == 0 || 조건성립 == 3 && nekkin_xëyma != 0;
            if (실행여부) {
                boolean 이전자리 = false;
                while (읽는자리 < mboolo_jeexal) {
                    int 다음자리 = 읽는자리; while (다음자리 < mboolo_jeexal && 종류[중첩깊이 * 128 + 다음자리] != 4) 다음자리++;
                    boolean JOKKOO_dawal = 다음자리 < mboolo_jeexal; int 입력쪽 = -1, 출력쪽 = -1, 출력방식 = 0;
                    명령해석기.토큰수 = 0; 쓴수 = 0; ñàmbaas_njumte = false;
                    for (int wërngël_àlluwa_tur = 읽는자리; wërngël_àlluwa_tur < 다음자리; wërngël_àlluwa_tur++) {
                        int 자료종류 = 종류[중첩깊이 * 128 + wërngël_àlluwa_tur];
                        if (자료종류 >= 5) { if (자료종류 == 7) { if (입력쪽 >= 0) { njumte("입력 전환이 겹쳤습니다"); return; } 입력쪽 = ++wërngël_àlluwa_tur; } else { if (출력쪽 >= 0) { njumte("출력 전환이 겹쳤습니다"); return; } 출력쪽 = ++wërngël_àlluwa_tur; 출력방식 = 자료종류; } continue; }
                        if (명령해석기.토큰수 == 32) { njumte("인수가 너무 많습니다"); return; }
                        int Tegtal_àlluwa_tur = 명령해석기.토큰수++; 명령해석기.시작점[Tegtal_àlluwa_tur] = 쓴수;
                        if (!Word_xëyma(wërngël_àlluwa_tur, 중첩깊이)) return;
                        명령해석기.diir_xëyma[Tegtal_àlluwa_tur] = 쓴수 - 명령해석기.시작점[Tegtal_àlluwa_tur];
                    }
                    연결중 = 이전자리 || JOKKOO_dawal || 입력쪽 >= 0 || 출력쪽 >= 0;
                    if (연결중 && (명령해석기.같음(0, "vi") || 명령해석기.같음(0, "edit") || 명령해석기.같음(0, "load") || 명령해석기.같음(0, "gui") || 명령해석기.같음(0, "terminal") || 명령해석기.같음(0, "sh") || 명령해석기.같음(0, "source"))) { njumte("duglante 명령과 ndigel 파일은 D_G 전환이나 dawal_xëyma 연결에 쓸 수 없습니다"); return; }
                    셸입출력.daw(이전자리, JOKKOO_dawal);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int 항목자리 = 입출력바꿈 == 0 ? 입력쪽 : 출력쪽; if (항목자리 < 0) continue;
                        int 시작자리 = 쓴수; if (!Word_xëyma(항목자리, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = fatlekookaay_Fisiye_yi.Yoonu_jëmale_Door(쓴수 - 시작자리);
                        for (int 안쪽자리 = 시작자리; 처리값 >= 0 && 안쪽자리 < 쓴수; 안쪽자리++) 처리값 = fatlekookaay_Fisiye_yi.Yoonu_jëmale_okte(안쪽자리 - 시작자리, 명령해석기.jeton_xëyma[안쪽자리]);
                        if (처리값 >= 0) 처리값 = fatlekookaay_Fisiye_yi.sos(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); 명령해석기.njumte(처리값); nekkin_xëyma = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.입력파일 = 처리값; else 셸입출력.takkub_génn = 처리값;
                    }
                    셸입출력.Maye_duglante = 중첩깊이 == 0 && 읽는자리 == 0 && 다음자리 == 총수;
                    깊이 = 중첩깊이; 명령해석기.결과 = 0; 보드.입출력전환(1);
                    명령해석기.ndigel();
                    보드.터미널(3);
                    int 반환값 = 명령해석기.결과, dawal_njumte = 셸입출력.foo_xëyma;
                    셸입출력.끝(); 연결중 = false;
                    nekkin_xëyma = dawal_njumte < 0 ? 1 : 반환값;
                    if (dawal_njumte < 0) { 명령해석기.njumte(dawal_njumte); return; }
                    if (ndigali_doxalin_jeexal || 반환값 == -1005) return;
                    이전자리 = true; 읽는자리 = 다음자리 + 1;
                }
            }
            if (mboolo_jeexal < 총수) 조건성립 = 종류[중첩깊이 * 128 + mboolo_jeexal];
            읽는자리 = mboolo_jeexal + 1;
        }
    }
    static void def_bara_denc() {
        if (명령해석기.토큰수 != 2 || 깊이 >= 3) { 명령해석기.결과 = 2; 단말.biir("사용법: sh bara_denc (중첩 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = 명령해석기.Yoonu_jëmale(1); if (처리값 >= 0) 처리값 = fatlekookaay_Fisiye_yi.sos(0);
        if (처리값 < 0) { 명령해석기.njumte(처리값); return; }
        int 항목수 = 0, okte_mbir;
        while ((okte_mbir = fatlekookaay_Fisiye_yi.읽기(처리값)) != 256 && okte_mbir >= 0 && 항목수 < 16384) ndigali_doxalin_xëyma[중첩깊이 * 16384 + 항목수++] = okte_mbir;
        fatlekookaay_Fisiye_yi.Tej(처리값); 보드.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < 항목수 && !ndigali_doxalin_jeexal;) {
            int 끝자리 = 읽는자리; while (끝자리 < 항목수 && ndigali_doxalin_xëyma[중첩깊이 * 16384 + 끝자리] != 10) 끝자리++;
            int 유효길이 = 끝자리 - 읽는자리; if (유효길이 > 0 && ndigali_doxalin_xëyma[중첩깊이 * 16384 + 끝자리 - 1] == 13) 유효길이--;
            def_ndigel(ndigali_doxalin_xëyma, 중첩깊이 * 16384 + 읽는자리, 유효길이, 중첩깊이); 읽는자리 = 끝자리 + 1;
        }
        명령해석기.결과 = nekkin_xëyma; ndigali_doxalin_jeexal = false; 깊이 = 중첩깊이 - 1;
    }
}
