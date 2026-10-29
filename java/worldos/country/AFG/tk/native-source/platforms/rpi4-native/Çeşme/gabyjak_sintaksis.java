// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 interaktiw gabyjak 문법. 파이프는 순차 ýerine_ýetir_buýruk, 환경은 같은 셸에서 공유한다. */
public final class gabyjak_sintaksis {
    static int[] Çeşme = new int[4 * 4096], 종류 = new int[4 * 128], Bitir = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] 변수이름 = new int[16 * 32], 변수값 = new int[16 * 256], 이름길이 = new int[16], baha_dowamlylyk = new int[16];
    static int[] skript_baha = new int[4 * 16384];
    static int ýagdaý_baha, 깊이, 쓴수;
    static boolean 연결중, skript_tamamla, giňelme_säwlik;
    static boolean at_nyşan(int nyşanyň_kody) { return nyşanyň_kody >= 'a' && nyşanyň_kody <= 'z' || nyşanyň_kody >= 'A' && nyşanyň_kody <= 'Z' || nyşanyň_kody == '_' || nyşanyň_kody >= 128; }
    static boolean 이름뒤(int nyşanyň_kody) { return at_nyşan(nyşanyň_kody) || nyşanyň_kody >= '0' && nyşanyň_kody <= '9'; }
    static void Hata(String Metin) { 보드.입출력전환(0); 단말.Ýaz("buýruk seljer_baha: "); 단말.Ýaz(Metin); 단말.문자(10); ýagdaý_baha = 2; }
    static int Oka(int 항목수, int 중첩깊이) {
        int 현재자리 = 0, 총수 = 0, 기준자리 = 중첩깊이 * 4096, ýörite_nyşan = 중첩깊이 * 128;
        while (현재자리 < 항목수) {
            while (현재자리 < 항목수 && (Çeşme[기준자리 + 현재자리] == 32 || Çeşme[기준자리 + 현재자리] == 9)) 현재자리++;
            if (현재자리 == 항목수 || Çeşme[기준자리 + 현재자리] == '#') break;
            if (총수 == 128) { Hata("낱말이 너무 많습니다"); return -1; }
            int 시작자리 = 현재자리, nyşanyň_kody = Çeşme[기준자리 + 현재자리], 자료종류 = 0;
            if (nyşanyň_kody == ';') { 자료종류 = 1; 현재자리++; }
            else if (nyşanyň_kody == '&') { if (현재자리 + 1 >= 항목수 || Çeşme[기준자리 + 현재자리 + 1] != '&') { Hata("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } 자료종류 = 2; 현재자리 += 2; }
            else if (nyşanyň_kody == '|') { 현재자리++; 자료종류 = 현재자리 < 항목수 && Çeşme[기준자리 + 현재자리] == '|' ? 3 : 4; if (자료종류 == 3) 현재자리++; }
            else if (nyşanyň_kody == '>') { 현재자리++; 자료종류 = 현재자리 < 항목수 && Çeşme[기준자리 + 현재자리] == '>' ? 6 : 5; if (자료종류 == 6) 현재자리++; }
            else if (nyşanyň_kody == '<') { 자료종류 = 7; 현재자리++; }
            else {
                int 따옴표 = 0;
                while (현재자리 < 항목수) {
                    nyşanyň_kody = Çeşme[기준자리 + 현재자리];
                    if (nyşanyň_kody == '`' && 따옴표 != 39 || nyşanyň_kody == '$' && 따옴표 != 39 && 현재자리 + 1 < 항목수 && Çeşme[기준자리 + 현재자리 + 1] == '(') { Hata("buýruk 결과 치환은 지원하지 않습니다"); return -1; }
                    if (nyşanyň_kody == '\\' && 따옴표 != 39) { if (++현재자리 == 항목수) { Hata("setir 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } 현재자리++; continue; }
                    if (nyşanyň_kody == 따옴표) { 따옴표 = 0; 현재자리++; continue; }
                    if (따옴표 == 0 && (nyşanyň_kody == 39 || nyşanyň_kody == 34)) { 따옴표 = nyşanyň_kody; 현재자리++; continue; }
                    if (따옴표 == 0 && (nyşanyň_kody == 32 || nyşanyň_kody == 9 || nyşanyň_kody == ';' || nyşanyň_kody == '&' || nyşanyň_kody == '|' || nyşanyň_kody == '<' || nyşanyň_kody == '>')) break;
                    현재자리++;
                }
                if (따옴표 != 0) { Hata("따옴표가 닫히지 않았습니다"); return -1; }
                if (현재자리 < 항목수 && (Çeşme[기준자리 + 현재자리] == '>' || Çeşme[기준자리 + 현재자리] == '<')) {
                    boolean 수치 = 현재자리 > 시작자리;
                    for (int sikl_indeks = 시작자리; sikl_indeks < 현재자리; sikl_indeks++) if (Çeşme[기준자리 + sikl_indeks] < '0' || Çeşme[기준자리 + sikl_indeks] > '9') 수치 = false;
                    if (수치) { Hata("번호를 지정한 Faýl 서술자 I_O 전환은 지원하지 않습니다"); return -1; }
                }
            }
            종류[ýörite_nyşan + 총수] = 자료종류; Bitir[ýörite_nyşan + 총수] = 시작자리; 끝[ýörite_nyşan + 총수] = 현재자리; 총수++;
        }
        boolean 낱말 = false;
        for (int sikl_indeks = 0; sikl_indeks < 총수; sikl_indeks++) {
            int 임시값 = 종류[ýörite_nyşan + sikl_indeks];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++sikl_indeks == 총수 || 종류[ýörite_nyşan + sikl_indeks] != 0) { Hata("I_O 전환에 Faýl 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || sikl_indeks == 총수 - 1 && 임시값 != 1) { Hata("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (총수 > 0 && !낱말 && 종류[ýörite_nyşan + 총수 - 1] != 1) { Hata("명령이 빠졌습니다"); return -1; }
        return 총수;
    }
    static boolean 구간말(int[] maglumat_ARRAY, int ýerli_başlat, int 항목수, String 문자위치) {
        if (항목수 != 문자위치.length()) return false; for (int sikl_indeks = 0; sikl_indeks < 항목수; sikl_indeks++) if (maglumat_ARRAY[ýerli_başlat + sikl_indeks] != 문자위치.charAt(sikl_indeks)) return false; return true;
    }
    static void 넣기(int baýt_maglumat) {
        if (쓴수 >= 명령해석기.token_baha.length) { if (!giňelme_säwlik) Hata("변수를 펼친 명령이 너무 깁니다"); giňelme_säwlik = true; return; }
        명령해석기.token_baha[쓴수++] = baýt_maglumat;
    }
    static void 변수(int[] maglumat_ARRAY, int 시작자리, int 항목수) {
        if (구간말(maglumat_ARRAY, 시작자리, 항목수, "PWD")) { 넣기('/'); for (int sikl_indeks = 0; sikl_indeks < ýat_Faýllar.현재길이; sikl_indeks++) 넣기(ýat_Faýllar.현재[sikl_indeks]); return; }
        if (구간말(maglumat_ARRAY, 시작자리, 항목수, "HOME")) { 넣기('/'); return; }
        if (구간말(maglumat_ARRAY, 시작자리, 항목수, "?")) {
            int maglumat_baha = ýagdaý_baha, san = 100; boolean 시작여부 = false;
            while (san > 0) { int 뒷값 = maglumat_baha / san; if (뒷값 != 0 || 시작여부 || san == 1) { 넣기('0' + 뒷값); 시작여부 = true; } maglumat_baha %= san; san /= 10; } return;
        }
        for (int sikl_indeks = 0; sikl_indeks < 16; sikl_indeks++) if (이름길이[sikl_indeks] == 항목수) {
            boolean 일치여부 = true; for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) if (변수이름[sikl_indeks * 32 + 안쪽자리] != maglumat_ARRAY[시작자리 + 안쪽자리]) 일치여부 = false;
            if (일치여부) { for (int 안쪽자리 = 0; 안쪽자리 < baha_dowamlylyk[sikl_indeks]; 안쪽자리++) 넣기(변수값[sikl_indeks * 256 + 안쪽자리]); return; }
        }
    }
    static boolean Söz_baha(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = Bitir[중첩깊이 * 128 + 낱말번호], 끝자리 = 끝[중첩깊이 * 128 + 낱말번호], 기준자리 = 중첩깊이 * 4096, 따옴표 = 0;
        if (읽는자리 < 끝자리 && Çeşme[기준자리 + 읽는자리] == '~' && (읽는자리 + 1 == 끝자리 || Çeşme[기준자리 + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < 끝자리) {
            int nyşanyň_kody = Çeşme[기준자리 + 읽는자리++];
            if (nyşanyň_kody == 따옴표) { 따옴표 = 0; continue; }
            if (따옴표 == 0 && (nyşanyň_kody == 39 || nyşanyň_kody == 34)) { 따옴표 = nyşanyň_kody; continue; }
            if (nyşanyň_kody == '\\' && 따옴표 != 39) { int 다음자리 = Çeşme[기준자리 + 읽는자리++]; if (따옴표 == 34 && 다음자리 != '$' && 다음자리 != '"' && 다음자리 != '\\') 넣기('\\'); 넣기(다음자리); continue; }
            if (nyşanyň_kody == '$' && 따옴표 != 39 && 읽는자리 < 끝자리) {
                boolean 중괄호자리 = Çeşme[기준자리 + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < 끝자리 && Çeşme[기준자리 + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < 끝자리 && 이름뒤(Çeşme[기준자리 + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == 끝자리 || Çeşme[기준자리 + 읽는자리] != '}')) { Hata("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                변수(Çeşme, 기준자리 + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(nyşanyň_kody);
        }
        return !giňelme_säwlik;
    }
    static int 환경설정(int argument_indeks, boolean aýyr) {
        int ýerli_başlat = 명령해석기.시작점[argument_indeks], 끝자리 = ýerli_başlat + 명령해석기.dowamlylyk_baha[argument_indeks], 같음자리 = ýerli_başlat;
        while (같음자리 < 끝자리 && 명령해석기.token_baha[같음자리] != '=') 같음자리++;
        int 항목수 = 같음자리 - ýerli_başlat;
        if (항목수 < 1 || 항목수 > 31 || !at_nyşan(명령해석기.token_baha[ýerli_başlat]) || !aýyr && 같음자리 == 끝자리 || 끝자리 - 같음자리 - 1 > 255) return 2;
        for (int sikl_indeks = ýerli_başlat; sikl_indeks < 같음자리; sikl_indeks++) if (!이름뒤(명령해석기.token_baha[sikl_indeks])) return 2;
        if (구간말(명령해석기.token_baha, ýerli_başlat, 항목수, "PWD") || 구간말(명령해석기.token_baha, ýerli_başlat, 항목수, "HOME")) return 2;
        int 찾은여부 = -1, 빈여부 = -1;
        for (int sikl_indeks = 0; sikl_indeks < 16; sikl_indeks++) {
            if (이름길이[sikl_indeks] == 0) 빈여부 = sikl_indeks;
            if (이름길이[sikl_indeks] != 항목수) continue;
            boolean 일치여부 = true; for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) if (변수이름[sikl_indeks * 32 + 안쪽자리] != 명령해석기.token_baha[ýerli_başlat + 안쪽자리]) 일치여부 = false;
            if (일치여부) 찾은여부 = sikl_indeks;
        }
        if (aýyr) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = 빈여부; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = 항목수; baha_dowamlylyk[찾은여부] = 끝자리 - 같음자리 - 1;
        for (int sikl_indeks = 0; sikl_indeks < 항목수; sikl_indeks++) 변수이름[찾은여부 * 32 + sikl_indeks] = 명령해석기.token_baha[ýerli_başlat + sikl_indeks];
        for (int sikl_indeks = 같음자리 + 1; sikl_indeks < 끝자리; sikl_indeks++) 변수값[찾은여부 * 256 + sikl_indeks - 같음자리 - 1] = 명령해석기.token_baha[sikl_indeks];
        return 0;
    }
    static void 환경보기() {
        단말.Ýaz("HOME=/\nPWD="); ýat_Faýllar.현재쓰기(); 단말.문자(10);
        for (int sikl_indeks = 0; sikl_indeks < 16; sikl_indeks++) if (이름길이[sikl_indeks] > 0) {
            for (int 안쪽자리 = 0; 안쪽자리 < 이름길이[sikl_indeks]; 안쪽자리++) 보드.직렬쓰기(변수이름[sikl_indeks * 32 + 안쪽자리]); 단말.문자('=');
            for (int 안쪽자리 = 0; 안쪽자리 < baha_dowamlylyk[sikl_indeks]; 안쪽자리++) 보드.직렬쓰기(변수값[sikl_indeks * 256 + 안쪽자리]); 단말.문자(10);
        }
    }
    static void ýerine_ýetir_buýruk(int[] maglumat_ARRAY, int 시작변위, int 항목수, int 중첩깊이) {
        if (중첩깊이 >= 4 || 항목수 > 4096) { Hata("buýruk 파일의 중첩 또는 setir dowamlylyk_baha 제한을 넘었습니다"); return; }
        for (int sikl_indeks = 0; sikl_indeks < 항목수; sikl_indeks++) Çeşme[중첩깊이 * 4096 + sikl_indeks] = maglumat_ARRAY[시작변위 + sikl_indeks];
        int 총수 = Oka(항목수, 중첩깊이); if (총수 < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < 총수) {
            int topar_tamamla = 읽는자리;
            while (topar_tamamla < 총수 && (종류[중첩깊이 * 128 + topar_tamamla] == 0 || 종류[중첩깊이 * 128 + topar_tamamla] >= 4)) topar_tamamla++;
            boolean ýerine_ýetir = 조건성립 == 1 || 조건성립 == 2 && ýagdaý_baha == 0 || 조건성립 == 3 && ýagdaý_baha != 0;
            if (ýerine_ýetir) {
                boolean 이전자리 = false;
                while (읽는자리 < topar_tamamla) {
                    int 다음자리 = 읽는자리; while (다음자리 < topar_tamamla && 종류[중첩깊이 * 128 + 다음자리] != 4) 다음자리++;
                    boolean Birikme_Stream = 다음자리 < topar_tamamla; int 입력쪽 = -1, 출력쪽 = -1, 출력방식 = 0;
                    명령해석기.토큰수 = 0; 쓴수 = 0; giňelme_säwlik = false;
                    for (int sikl_indeks = 읽는자리; sikl_indeks < 다음자리; sikl_indeks++) {
                        int 자료종류 = 종류[중첩깊이 * 128 + sikl_indeks];
                        if (자료종류 >= 5) { if (자료종류 == 7) { if (입력쪽 >= 0) { Hata("입력 전환이 겹쳤습니다"); return; } 입력쪽 = ++sikl_indeks; } else { if (출력쪽 >= 0) { Hata("출력 전환이 겹쳤습니다"); return; } 출력쪽 = ++sikl_indeks; 출력방식 = 자료종류; } continue; }
                        if (명령해석기.토큰수 == 32) { Hata("인수가 너무 많습니다"); return; }
                        int argument_indeks = 명령해석기.토큰수++; 명령해석기.시작점[argument_indeks] = 쓴수;
                        if (!Söz_baha(sikl_indeks, 중첩깊이)) return;
                        명령해석기.dowamlylyk_baha[argument_indeks] = 쓴수 - 명령해석기.시작점[argument_indeks];
                    }
                    연결중 = 이전자리 || Birikme_Stream || 입력쪽 >= 0 || 출력쪽 >= 0;
                    if (연결중 && (명령해석기.같음(0, "vi") || 명령해석기.같음(0, "edit") || 명령해석기.같음(0, "load") || 명령해석기.같음(0, "gui") || 명령해석기.같음(0, "terminal") || 명령해석기.같음(0, "sh") || 명령해석기.같음(0, "source"))) { Hata("interaktiw 명령과 buýruk 파일은 I_O 전환이나 Stream_baha 연결에 쓸 수 없습니다"); return; }
                    셸입출력.Bitir(이전자리, Birikme_Stream);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int 항목자리 = 입출력바꿈 == 0 ? 입력쪽 : 출력쪽; if (항목자리 < 0) continue;
                        int 시작자리 = 쓴수; if (!Söz_baha(항목자리, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = ýat_Faýllar.ýol_başlat(쓴수 - 시작자리);
                        for (int 안쪽자리 = 시작자리; 처리값 >= 0 && 안쪽자리 < 쓴수; 안쪽자리++) 처리값 = ýat_Faýllar.ýol_baýt(안쪽자리 - 시작자리, 명령해석기.token_baha[안쪽자리]);
                        if (처리값 >= 0) 처리값 = ýat_Faýllar.Aç(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); 명령해석기.Hata(처리값); ýagdaý_baha = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.입력파일 = 처리값; else 셸입출력.çykyş_faýly_9ceb7bd4 = 처리값;
                    }
                    셸입출력.Rugsat_ber_interaktiw = 중첩깊이 == 0 && 읽는자리 == 0 && 다음자리 == 총수;
                    깊이 = 중첩깊이; 명령해석기.결과 = 0; 보드.입출력전환(1);
                    명령해석기.buýruk();
                    보드.터미널(3);
                    int 반환값 = 명령해석기.결과, Stream_säwlik = 셸입출력.näsazlyk_baha;
                    셸입출력.끝(); 연결중 = false;
                    ýagdaý_baha = Stream_säwlik < 0 ? 1 : 반환값;
                    if (Stream_säwlik < 0) { 명령해석기.Hata(Stream_säwlik); return; }
                    if (skript_tamamla || 반환값 == -1005) return;
                    이전자리 = true; 읽는자리 = 다음자리 + 1;
                }
            }
            if (topar_tamamla < 총수) 조건성립 = 종류[중첩깊이 * 128 + topar_tamamla];
            읽는자리 = topar_tamamla + 1;
        }
    }
    static void ýerine_ýetir_faýl() {
        if (명령해석기.토큰수 != 2 || 깊이 >= 3) { 명령해석기.결과 = 2; 단말.Ýaz("사용법: sh Faýl (중첩 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = 명령해석기.Ýol(1); if (처리값 >= 0) 처리값 = ýat_Faýllar.Aç(0);
        if (처리값 < 0) { 명령해석기.Hata(처리값); return; }
        int 항목수 = 0, baýt_maglumat;
        while ((baýt_maglumat = ýat_Faýllar.Oka(처리값)) != 256 && baýt_maglumat >= 0 && 항목수 < 16384) skript_baha[중첩깊이 * 16384 + 항목수++] = baýt_maglumat;
        ýat_Faýllar.Ýap(처리값); 보드.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < 항목수 && !skript_tamamla;) {
            int 끝자리 = 읽는자리; while (끝자리 < 항목수 && skript_baha[중첩깊이 * 16384 + 끝자리] != 10) 끝자리++;
            int 유효길이 = 끝자리 - 읽는자리; if (유효길이 > 0 && skript_baha[중첩깊이 * 16384 + 끝자리 - 1] == 13) 유효길이--;
            ýerine_ýetir_buýruk(skript_baha, 중첩깊이 * 16384 + 읽는자리, 유효길이, 중첩깊이); 읽는자리 = 끝자리 + 1;
        }
        명령해석기.결과 = ýagdaý_baha; skript_tamamla = false; 깊이 = 중첩깊이 - 1;
    }
}
