// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 ndërvepruese pasues 문법. 파이프는 순차 zbatoj_komandë, 환경은 같은 셸에서 공유한다. */
public final class pasues_sintaksë {
    static int[] BURIMI = new int[4 * 4096], 종류 = new int[4 * 128], Ekzekuto = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] 변수이름 = new int[16 * 32], 변수값 = new int[16 * 256], 이름길이 = new int[16], VALUE_gjatësi = new int[16];
    static int[] skript_VALUE = new int[4 * 16384];
    static int status_VALUE, 깊이, 쓴수;
    static boolean 연결중, skript_mbaroj, shtesë_gabim;
    static boolean emër_karakter(int kodi_i_karakterit) { return kodi_i_karakterit >= 'a' && kodi_i_karakterit <= 'z' || kodi_i_karakterit >= 'A' && kodi_i_karakterit <= 'Z' || kodi_i_karakterit == '_' || kodi_i_karakterit >= 128; }
    static boolean 이름뒤(int kodi_i_karakterit) { return emër_karakter(kodi_i_karakterit) || kodi_i_karakterit >= '0' && kodi_i_karakterit <= '9'; }
    static void GABIM(String Teksti) { panel.입출력전환(0); 단말.Shkrimi("Komanda analizoj_VALUE: "); 단말.Shkrimi(Teksti); 단말.문자(10); status_VALUE = 2; }
    static int Leximi(int futje_COUNT, int 중첩깊이) {
        int 현재자리 = 0, 총수 = 0, BASE_pozicioni = 중첩깊이 * 4096, karakter_i_veçantë = 중첩깊이 * 128;
        while (현재자리 < futje_COUNT) {
            while (현재자리 < futje_COUNT && (BURIMI[BASE_pozicioni + 현재자리] == 32 || BURIMI[BASE_pozicioni + 현재자리] == 9)) 현재자리++;
            if (현재자리 == futje_COUNT || BURIMI[BASE_pozicioni + 현재자리] == '#') break;
            if (총수 == 128) { GABIM("낱말이 너무 많습니다"); return -1; }
            int nis_pozicioni = 현재자리, kodi_i_karakterit = BURIMI[BASE_pozicioni + 현재자리], 자료종류 = 0;
            if (kodi_i_karakterit == ';') { 자료종류 = 1; 현재자리++; }
            else if (kodi_i_karakterit == '&') { if (현재자리 + 1 >= futje_COUNT || BURIMI[BASE_pozicioni + 현재자리 + 1] != '&') { GABIM("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } 자료종류 = 2; 현재자리 += 2; }
            else if (kodi_i_karakterit == '|') { 현재자리++; 자료종류 = 현재자리 < futje_COUNT && BURIMI[BASE_pozicioni + 현재자리] == '|' ? 3 : 4; if (자료종류 == 3) 현재자리++; }
            else if (kodi_i_karakterit == '>') { 현재자리++; 자료종류 = 현재자리 < futje_COUNT && BURIMI[BASE_pozicioni + 현재자리] == '>' ? 6 : 5; if (자료종류 == 6) 현재자리++; }
            else if (kodi_i_karakterit == '<') { 자료종류 = 7; 현재자리++; }
            else {
                int Citim = 0;
                while (현재자리 < futje_COUNT) {
                    kodi_i_karakterit = BURIMI[BASE_pozicioni + 현재자리];
                    if (kodi_i_karakterit == '`' && Citim != 39 || kodi_i_karakterit == '$' && Citim != 39 && 현재자리 + 1 < futje_COUNT && BURIMI[BASE_pozicioni + 현재자리 + 1] == '(') { GABIM("Komanda llogaritje 치환은 지원하지 않습니다"); return -1; }
                    if (kodi_i_karakterit == '\\' && Citim != 39) { if (++현재자리 == futje_COUNT) { GABIM("linjë 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } 현재자리++; continue; }
                    if (kodi_i_karakterit == Citim) { Citim = 0; 현재자리++; continue; }
                    if (Citim == 0 && (kodi_i_karakterit == 39 || kodi_i_karakterit == 34)) { Citim = kodi_i_karakterit; 현재자리++; continue; }
                    if (Citim == 0 && (kodi_i_karakterit == 32 || kodi_i_karakterit == 9 || kodi_i_karakterit == ';' || kodi_i_karakterit == '&' || kodi_i_karakterit == '|' || kodi_i_karakterit == '<' || kodi_i_karakterit == '>')) break;
                    현재자리++;
                }
                if (Citim != 0) { GABIM("따옴표가 닫히지 않았습니다"); return -1; }
                if (현재자리 < futje_COUNT && (BURIMI[BASE_pozicioni + 현재자리] == '>' || BURIMI[BASE_pozicioni + 현재자리] == '<')) {
                    boolean 수치 = 현재자리 > nis_pozicioni;
                    for (int Loop_INDEX = nis_pozicioni; Loop_INDEX < 현재자리; Loop_INDEX++) if (BURIMI[BASE_pozicioni + Loop_INDEX] < '0' || BURIMI[BASE_pozicioni + Loop_INDEX] > '9') 수치 = false;
                    if (수치) { GABIM("번호를 지정한 Kartelë 서술자 I_O 전환은 지원하지 않습니다"); return -1; }
                }
            }
            종류[karakter_i_veçantë + 총수] = 자료종류; Ekzekuto[karakter_i_veçantë + 총수] = nis_pozicioni; 끝[karakter_i_veçantë + 총수] = 현재자리; 총수++;
        }
        boolean 낱말 = false;
        for (int Loop_INDEX = 0; Loop_INDEX < 총수; Loop_INDEX++) {
            int 임시값 = 종류[karakter_i_veçantë + Loop_INDEX];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++Loop_INDEX == 총수 || 종류[karakter_i_veçantë + Loop_INDEX] != 0) { GABIM("I_O 전환에 Kartelë 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || Loop_INDEX == 총수 - 1 && 임시값 != 1) { GABIM("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (총수 > 0 && !낱말 && 종류[karakter_i_veçantë + 총수 - 1] != 1) { GABIM("명령이 빠졌습니다"); return -1; }
        return 총수;
    }
    static boolean 구간말(int[] të_dhëna_ARRAY, int lokal_nis, int futje_COUNT, String karakter_pozicioni) {
        if (futje_COUNT != karakter_pozicioni.length()) return false; for (int Loop_INDEX = 0; Loop_INDEX < futje_COUNT; Loop_INDEX++) if (të_dhëna_ARRAY[lokal_nis + Loop_INDEX] != karakter_pozicioni.charAt(Loop_INDEX)) return false; return true;
    }
    static void 넣기(int bajt_të_dhëna) {
        if (쓴수 >= 명령해석기.kodi_VALUE.length) { if (!shtesë_gabim) GABIM("변수를 펼친 명령이 너무 깁니다"); shtesë_gabim = true; return; }
        명령해석기.kodi_VALUE[쓴수++] = bajt_të_dhëna;
    }
    static void 변수(int[] të_dhëna_ARRAY, int nis_pozicioni, int futje_COUNT) {
        if (구간말(të_dhëna_ARRAY, nis_pozicioni, futje_COUNT, "PWD")) { 넣기('/'); for (int Loop_INDEX = 0; Loop_INDEX < Memorie_Skedarët.현재길이; Loop_INDEX++) 넣기(Memorie_Skedarët.현재[Loop_INDEX]); return; }
        if (구간말(të_dhëna_ARRAY, nis_pozicioni, futje_COUNT, "HOME")) { 넣기('/'); return; }
        if (구간말(të_dhëna_ARRAY, nis_pozicioni, futje_COUNT, "?")) {
            int të_dhëna_VALUE = status_VALUE, shifër = 100; boolean 시작여부 = false;
            while (shifër > 0) { int 뒷값 = të_dhëna_VALUE / shifër; if (뒷값 != 0 || 시작여부 || shifër == 1) { 넣기('0' + 뒷값); 시작여부 = true; } të_dhëna_VALUE %= shifër; shifër /= 10; } return;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] == futje_COUNT) {
            boolean MATCH = true; for (int bashkim_i_brendshëm_pozicioni = 0; bashkim_i_brendshëm_pozicioni < futje_COUNT; bashkim_i_brendshëm_pozicioni++) if (변수이름[Loop_INDEX * 32 + bashkim_i_brendshëm_pozicioni] != të_dhëna_ARRAY[nis_pozicioni + bashkim_i_brendshëm_pozicioni]) MATCH = false;
            if (MATCH) { for (int bashkim_i_brendshëm_pozicioni = 0; bashkim_i_brendshëm_pozicioni < VALUE_gjatësi[Loop_INDEX]; bashkim_i_brendshëm_pozicioni++) 넣기(변수값[Loop_INDEX * 256 + bashkim_i_brendshëm_pozicioni]); return; }
        }
    }
    static boolean Word_VALUE(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = Ekzekuto[중첩깊이 * 128 + 낱말번호], mbaroj_pozicioni = 끝[중첩깊이 * 128 + 낱말번호], BASE_pozicioni = 중첩깊이 * 4096, Citim = 0;
        if (읽는자리 < mbaroj_pozicioni && BURIMI[BASE_pozicioni + 읽는자리] == '~' && (읽는자리 + 1 == mbaroj_pozicioni || BURIMI[BASE_pozicioni + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < mbaroj_pozicioni) {
            int kodi_i_karakterit = BURIMI[BASE_pozicioni + 읽는자리++];
            if (kodi_i_karakterit == Citim) { Citim = 0; continue; }
            if (Citim == 0 && (kodi_i_karakterit == 39 || kodi_i_karakterit == 34)) { Citim = kodi_i_karakterit; continue; }
            if (kodi_i_karakterit == '\\' && Citim != 39) { int Tjetër_pozicioni = BURIMI[BASE_pozicioni + 읽는자리++]; if (Citim == 34 && Tjetër_pozicioni != '$' && Tjetër_pozicioni != '"' && Tjetër_pozicioni != '\\') 넣기('\\'); 넣기(Tjetër_pozicioni); continue; }
            if (kodi_i_karakterit == '$' && Citim != 39 && 읽는자리 < mbaroj_pozicioni) {
                boolean 중괄호자리 = BURIMI[BASE_pozicioni + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < mbaroj_pozicioni && BURIMI[BASE_pozicioni + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < mbaroj_pozicioni && 이름뒤(BURIMI[BASE_pozicioni + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == mbaroj_pozicioni || BURIMI[BASE_pozicioni + 읽는자리] != '}')) { GABIM("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                변수(BURIMI, BASE_pozicioni + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(kodi_i_karakterit);
        }
        return !shtesë_gabim;
    }
    static int 환경설정(int argument_INDEX, boolean heq) {
        int lokal_nis = 명령해석기.시작점[argument_INDEX], mbaroj_pozicioni = lokal_nis + 명령해석기.gjatësi_VALUE[argument_INDEX], 같음자리 = lokal_nis;
        while (같음자리 < mbaroj_pozicioni && 명령해석기.kodi_VALUE[같음자리] != '=') 같음자리++;
        int futje_COUNT = 같음자리 - lokal_nis;
        if (futje_COUNT < 1 || futje_COUNT > 31 || !emër_karakter(명령해석기.kodi_VALUE[lokal_nis]) || !heq && 같음자리 == mbaroj_pozicioni || mbaroj_pozicioni - 같음자리 - 1 > 255) return 2;
        for (int Loop_INDEX = lokal_nis; Loop_INDEX < 같음자리; Loop_INDEX++) if (!이름뒤(명령해석기.kodi_VALUE[Loop_INDEX])) return 2;
        if (구간말(명령해석기.kodi_VALUE, lokal_nis, futje_COUNT, "PWD") || 구간말(명령해석기.kodi_VALUE, lokal_nis, futje_COUNT, "HOME")) return 2;
        int 찾은여부 = -1, teknologjia_e_informacionit_bosh_status = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] == 0) teknologjia_e_informacionit_bosh_status = Loop_INDEX;
            if (이름길이[Loop_INDEX] != futje_COUNT) continue;
            boolean MATCH = true; for (int bashkim_i_brendshëm_pozicioni = 0; bashkim_i_brendshëm_pozicioni < futje_COUNT; bashkim_i_brendshëm_pozicioni++) if (변수이름[Loop_INDEX * 32 + bashkim_i_brendshëm_pozicioni] != 명령해석기.kodi_VALUE[lokal_nis + bashkim_i_brendshëm_pozicioni]) MATCH = false;
            if (MATCH) 찾은여부 = Loop_INDEX;
        }
        if (heq) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = teknologjia_e_informacionit_bosh_status; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = futje_COUNT; VALUE_gjatësi[찾은여부] = mbaroj_pozicioni - 같음자리 - 1;
        for (int Loop_INDEX = 0; Loop_INDEX < futje_COUNT; Loop_INDEX++) 변수이름[찾은여부 * 32 + Loop_INDEX] = 명령해석기.kodi_VALUE[lokal_nis + Loop_INDEX];
        for (int Loop_INDEX = 같음자리 + 1; Loop_INDEX < mbaroj_pozicioni; Loop_INDEX++) 변수값[찾은여부 * 256 + Loop_INDEX - 같음자리 - 1] = 명령해석기.kodi_VALUE[Loop_INDEX];
        return 0;
    }
    static void 환경보기() {
        단말.Shkrimi("HOME=/\nPWD="); Memorie_Skedarët.현재쓰기(); 단말.문자(10);
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] > 0) {
            for (int bashkim_i_brendshëm_pozicioni = 0; bashkim_i_brendshëm_pozicioni < 이름길이[Loop_INDEX]; bashkim_i_brendshëm_pozicioni++) panel.직렬쓰기(변수이름[Loop_INDEX * 32 + bashkim_i_brendshëm_pozicioni]); 단말.문자('=');
            for (int bashkim_i_brendshëm_pozicioni = 0; bashkim_i_brendshëm_pozicioni < VALUE_gjatësi[Loop_INDEX]; bashkim_i_brendshëm_pozicioni++) panel.직렬쓰기(변수값[Loop_INDEX * 256 + bashkim_i_brendshëm_pozicioni]); 단말.문자(10);
        }
    }
    static void zbatoj_komandë(int[] të_dhëna_ARRAY, int 시작변위, int futje_COUNT, int 중첩깊이) {
        if (중첩깊이 >= 4 || futje_COUNT > 4096) { GABIM("Komanda 파일의 ndërthurje_VALUE 또는 linjë gjatësi_VALUE 제한을 넘었습니다"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < futje_COUNT; Loop_INDEX++) BURIMI[중첩깊이 * 4096 + Loop_INDEX] = të_dhëna_ARRAY[시작변위 + Loop_INDEX];
        int 총수 = Leximi(futje_COUNT, 중첩깊이); if (총수 < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < 총수) {
            int grup_mbaroj = 읽는자리;
            while (grup_mbaroj < 총수 && (종류[중첩깊이 * 128 + grup_mbaroj] == 0 || 종류[중첩깊이 * 128 + grup_mbaroj] >= 4)) grup_mbaroj++;
            boolean zbatoj = 조건성립 == 1 || 조건성립 == 2 && status_VALUE == 0 || 조건성립 == 3 && status_VALUE != 0;
            if (zbatoj) {
                boolean 이전자리 = false;
                while (읽는자리 < grup_mbaroj) {
                    int Tjetër_pozicioni = 읽는자리; while (Tjetër_pozicioni < grup_mbaroj && 종류[중첩깊이 * 128 + Tjetër_pozicioni] != 4) Tjetër_pozicioni++;
                    boolean Lidh_Stream = Tjetër_pozicioni < grup_mbaroj; int 입력쪽 = -1, 출력쪽 = -1, 출력방식 = 0;
                    명령해석기.kodi_COUNT = 0; 쓴수 = 0; shtesë_gabim = false;
                    for (int Loop_INDEX = 읽는자리; Loop_INDEX < Tjetër_pozicioni; Loop_INDEX++) {
                        int 자료종류 = 종류[중첩깊이 * 128 + Loop_INDEX];
                        if (자료종류 >= 5) { if (자료종류 == 7) { if (입력쪽 >= 0) { GABIM("입력 전환이 겹쳤습니다"); return; } 입력쪽 = ++Loop_INDEX; } else { if (출력쪽 >= 0) { GABIM("출력 전환이 겹쳤습니다"); return; } 출력쪽 = ++Loop_INDEX; 출력방식 = 자료종류; } continue; }
                        if (명령해석기.kodi_COUNT == 32) { GABIM("인수가 너무 많습니다"); return; }
                        int argument_INDEX = 명령해석기.kodi_COUNT++; 명령해석기.시작점[argument_INDEX] = 쓴수;
                        if (!Word_VALUE(Loop_INDEX, 중첩깊이)) return;
                        명령해석기.gjatësi_VALUE[argument_INDEX] = 쓴수 - 명령해석기.시작점[argument_INDEX];
                    }
                    연결중 = 이전자리 || Lidh_Stream || 입력쪽 >= 0 || 출력쪽 >= 0;
                    if (연결중 && (명령해석기.같음(0, "vi") || 명령해석기.같음(0, "edit") || 명령해석기.같음(0, "load") || 명령해석기.같음(0, "gui") || 명령해석기.같음(0, "terminal") || 명령해석기.같음(0, "sh") || 명령해석기.같음(0, "source"))) { GABIM("ndërvepruese 명령과 Komanda 파일은 I_O 전환이나 Stream_VALUE 연결에 쓸 수 없습니다"); return; }
                    셸입출력.Ekzekuto(이전자리, Lidh_Stream);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int futje_pozicioni = 입출력바꿈 == 0 ? 입력쪽 : 출력쪽; if (futje_pozicioni < 0) continue;
                        int nis_pozicioni = 쓴수; if (!Word_VALUE(futje_pozicioni, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = Memorie_Skedarët.shteg_nis(쓴수 - nis_pozicioni);
                        for (int bashkim_i_brendshëm_pozicioni = nis_pozicioni; 처리값 >= 0 && bashkim_i_brendshëm_pozicioni < 쓴수; bashkim_i_brendshëm_pozicioni++) 처리값 = Memorie_Skedarët.shteg_bajt(bashkim_i_brendshëm_pozicioni - nis_pozicioni, 명령해석기.kodi_VALUE[bashkim_i_brendshëm_pozicioni]);
                        if (처리값 >= 0) 처리값 = Memorie_Skedarët.Hap(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); 명령해석기.GABIM(처리값); status_VALUE = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.입력파일 = 처리값; else 셸입출력.skedari_përfundimtar = 처리값;
                    }
                    셸입출력.Lejoj_ndërvepruese = 중첩깊이 == 0 && 읽는자리 == 0 && Tjetër_pozicioni == 총수;
                    깊이 = 중첩깊이; 명령해석기.llogaritje = 0; panel.입출력전환(1);
                    명령해석기.Komanda();
                    panel.Terminali(3);
                    int 반환값 = 명령해석기.llogaritje, Stream_gabim = 셸입출력.dështim_VALUE;
                    셸입출력.끝(); 연결중 = false;
                    status_VALUE = Stream_gabim < 0 ? 1 : 반환값;
                    if (Stream_gabim < 0) { 명령해석기.GABIM(Stream_gabim); return; }
                    if (skript_mbaroj || 반환값 == -1005) return;
                    이전자리 = true; 읽는자리 = Tjetër_pozicioni + 1;
                }
            }
            if (grup_mbaroj < 총수) 조건성립 = 종류[중첩깊이 * 128 + grup_mbaroj];
            읽는자리 = grup_mbaroj + 1;
        }
    }
    static void zbatoj_skedar() {
        if (명령해석기.kodi_COUNT != 2 || 깊이 >= 3) { 명령해석기.llogaritje = 2; 단말.Shkrimi("사용법: sh Kartelë (ndërthurje_VALUE 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = 명령해석기.POZICIONI(1); if (처리값 >= 0) 처리값 = Memorie_Skedarët.Hap(0);
        if (처리값 < 0) { 명령해석기.GABIM(처리값); return; }
        int futje_COUNT = 0, bajt_të_dhëna;
        while ((bajt_të_dhëna = Memorie_Skedarët.Leximi(처리값)) != 256 && bajt_të_dhëna >= 0 && futje_COUNT < 16384) skript_VALUE[중첩깊이 * 16384 + futje_COUNT++] = bajt_të_dhëna;
        Memorie_Skedarët.Mbyll(처리값); panel.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < futje_COUNT && !skript_mbaroj;) {
            int mbaroj_pozicioni = 읽는자리; while (mbaroj_pozicioni < futje_COUNT && skript_VALUE[중첩깊이 * 16384 + mbaroj_pozicioni] != 10) mbaroj_pozicioni++;
            int 유효길이 = mbaroj_pozicioni - 읽는자리; if (유효길이 > 0 && skript_VALUE[중첩깊이 * 16384 + mbaroj_pozicioni - 1] == 13) 유효길이--;
            zbatoj_komandë(skript_VALUE, 중첩깊이 * 16384 + 읽는자리, 유효길이, 중첩깊이); 읽는자리 = mbaroj_pozicioni + 1;
        }
        명령해석기.llogaritje = status_VALUE; skript_mbaroj = false; 깊이 = 중첩깊이 - 1;
    }
}
