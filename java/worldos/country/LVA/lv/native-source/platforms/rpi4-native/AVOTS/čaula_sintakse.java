// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 대화형 čaula 문법. 파이프는 순차 Izpildīt_komanda, 환경은 같은 셸에서 공유한다. */
public final class čaula_sintakse {
    static int[] AVOTS = new int[4 * 4096], 종류 = new int[4 * 128], Palaist = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] mainīgais_nosaukums = new int[16 * 32], mainīgais_dati = new int[16 * 256], 이름길이 = new int[16], 값길이 = new int[16];
    static int[] skripts_VALUE = new int[4 * 16384];
    static int Statuss_VALUE, 깊이, 쓴수;
    static boolean 연결중, skripts_beigt_zvanu, paplašinājums_kļūda;
    static boolean nosaukums_rakstzīme(int koda_punkts) { return koda_punkts >= 'a' && koda_punkts <= 'z' || koda_punkts >= 'A' && koda_punkts <= 'Z' || koda_punkts == '_' || koda_punkts >= 128; }
    static boolean 이름뒤(int koda_punkts) { return nosaukums_rakstzīme(koda_punkts) || koda_punkts >= '0' && koda_punkts <= '9'; }
    static void Kļūda(String Teksts) { Panelis.입출력전환(0); 단말.Rakstīt("Komanda parsēt_VALUE: "); 단말.Rakstīt(Teksts); 단말.문자(10); Statuss_VALUE = 2; }
    static int Lasīt(int ievade_COUNT, int 중첩깊이) {
        int pašreizējais_INDEX = 0, kopsumma_COUNT = 0, BASE_amats = 중첩깊이 * 4096, speciālā_rakstzīme = 중첩깊이 * 128;
        while (pašreizējais_INDEX < ievade_COUNT) {
            while (pašreizējais_INDEX < ievade_COUNT && (AVOTS[BASE_amats + pašreizējais_INDEX] == 32 || AVOTS[BASE_amats + pašreizējais_INDEX] == 9)) pašreizējais_INDEX++;
            if (pašreizējais_INDEX == ievade_COUNT || AVOTS[BASE_amats + pašreizējais_INDEX] == '#') break;
            if (kopsumma_COUNT == 128) { Kļūda("낱말이 너무 많습니다"); return -1; }
            int Sākt_amats = pašreizējais_INDEX, koda_punkts = AVOTS[BASE_amats + pašreizējais_INDEX], 자료종류 = 0;
            if (koda_punkts == ';') { 자료종류 = 1; pašreizējais_INDEX++; }
            else if (koda_punkts == '&') { if (pašreizējais_INDEX + 1 >= ievade_COUNT || AVOTS[BASE_amats + pašreizējais_INDEX + 1] != '&') { Kļūda("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } 자료종류 = 2; pašreizējais_INDEX += 2; }
            else if (koda_punkts == '|') { pašreizējais_INDEX++; 자료종류 = pašreizējais_INDEX < ievade_COUNT && AVOTS[BASE_amats + pašreizējais_INDEX] == '|' ? 3 : 4; if (자료종류 == 3) pašreizējais_INDEX++; }
            else if (koda_punkts == '>') { pašreizējais_INDEX++; 자료종류 = pašreizējais_INDEX < ievade_COUNT && AVOTS[BASE_amats + pašreizējais_INDEX] == '>' ? 6 : 5; if (자료종류 == 6) pašreizējais_INDEX++; }
            else if (koda_punkts == '<') { 자료종류 = 7; pašreizējais_INDEX++; }
            else {
                int Citāts = 0;
                while (pašreizējais_INDEX < ievade_COUNT) {
                    koda_punkts = AVOTS[BASE_amats + pašreizējais_INDEX];
                    if (koda_punkts == '`' && Citāts != 39 || koda_punkts == '$' && Citāts != 39 && pašreizējais_INDEX + 1 < ievade_COUNT && AVOTS[BASE_amats + pašreizējais_INDEX + 1] == '(') { Kļūda("Komanda mērs 치환은 지원하지 않습니다"); return -1; }
                    if (koda_punkts == '\\' && Citāts != 39) { if (++pašreizējais_INDEX == ievade_COUNT) { Kļūda("Līniju 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } pašreizējais_INDEX++; continue; }
                    if (koda_punkts == Citāts) { Citāts = 0; pašreizējais_INDEX++; continue; }
                    if (Citāts == 0 && (koda_punkts == 39 || koda_punkts == 34)) { Citāts = koda_punkts; pašreizējais_INDEX++; continue; }
                    if (Citāts == 0 && (koda_punkts == 32 || koda_punkts == 9 || koda_punkts == ';' || koda_punkts == '&' || koda_punkts == '|' || koda_punkts == '<' || koda_punkts == '>')) break;
                    pašreizējais_INDEX++;
                }
                if (Citāts != 0) { Kļūda("따옴표가 닫히지 않았습니다"); return -1; }
                if (pašreizējais_INDEX < ievade_COUNT && (AVOTS[BASE_amats + pašreizējais_INDEX] == '>' || AVOTS[BASE_amats + pašreizējais_INDEX] == '<')) {
                    boolean 수치 = pašreizējais_INDEX > Sākt_amats;
                    for (int Loop_INDEX = Sākt_amats; Loop_INDEX < pašreizējais_INDEX; Loop_INDEX++) if (AVOTS[BASE_amats + Loop_INDEX] < '0' || AVOTS[BASE_amats + Loop_INDEX] > '9') 수치 = false;
                    if (수치) { Kļūda("번호를 지정한 Fails 서술자 ievadizvade 전환은 지원하지 않습니다"); return -1; }
                }
            }
            종류[speciālā_rakstzīme + kopsumma_COUNT] = 자료종류; Palaist[speciālā_rakstzīme + kopsumma_COUNT] = Sākt_amats; 끝[speciālā_rakstzīme + kopsumma_COUNT] = pašreizējais_INDEX; kopsumma_COUNT++;
        }
        boolean 낱말 = false;
        for (int Loop_INDEX = 0; Loop_INDEX < kopsumma_COUNT; Loop_INDEX++) {
            int 임시값 = 종류[speciālā_rakstzīme + Loop_INDEX];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++Loop_INDEX == kopsumma_COUNT || 종류[speciālā_rakstzīme + Loop_INDEX] != 0) { Kļūda("ievadizvade 전환에 Fails 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || Loop_INDEX == kopsumma_COUNT - 1 && 임시값 != 1) { Kļūda("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (kopsumma_COUNT > 0 && !낱말 && 종류[speciālā_rakstzīme + kopsumma_COUNT - 1] != 1) { Kļūda("명령이 빠졌습니다"); return -1; }
        return kopsumma_COUNT;
    }
    static boolean diapazons_SMS(int[] dati_ARRAY, int vietējs_Sākt, int ievade_COUNT, String rakstzīme_amats) {
        if (ievade_COUNT != rakstzīme_amats.length()) return false; for (int Loop_INDEX = 0; Loop_INDEX < ievade_COUNT; Loop_INDEX++) if (dati_ARRAY[vietējs_Sākt + Loop_INDEX] != rakstzīme_amats.charAt(Loop_INDEX)) return false; return true;
    }
    static void 넣기(int byte_dati) {
        if (쓴수 >= 명령해석기.daļiņa_VALUE.length) { if (!paplašinājums_kļūda) Kļūda("변수를 펼친 명령이 너무 깁니다"); paplašinājums_kļūda = true; return; }
        명령해석기.daļiņa_VALUE[쓴수++] = byte_dati;
    }
    static void mainīgais_VALUE(int[] dati_ARRAY, int Sākt_amats, int ievade_COUNT) {
        if (diapazons_SMS(dati_ARRAY, Sākt_amats, ievade_COUNT, "PWD")) { 넣기('/'); for (int Loop_INDEX = 0; Loop_INDEX < atmiņa_Faili.현재길이; Loop_INDEX++) 넣기(atmiņa_Faili.pašreizējais_krājums[Loop_INDEX]); return; }
        if (diapazons_SMS(dati_ARRAY, Sākt_amats, ievade_COUNT, "HOME")) { 넣기('/'); return; }
        if (diapazons_SMS(dati_ARRAY, Sākt_amats, ievade_COUNT, "?")) {
            int dati_VALUE = Statuss_VALUE, cipars = 100; boolean 시작여부 = false;
            while (cipars > 0) { int 뒷값 = dati_VALUE / cipars; if (뒷값 != 0 || 시작여부 || cipars == 1) { 넣기('0' + 뒷값); 시작여부 = true; } dati_VALUE %= cipars; cipars /= 10; } return;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] == ievade_COUNT) {
            boolean MATCH = true; for (int iekšējais_amats = 0; iekšējais_amats < ievade_COUNT; iekšējais_amats++) if (mainīgais_nosaukums[Loop_INDEX * 32 + iekšējais_amats] != dati_ARRAY[Sākt_amats + iekšējais_amats]) MATCH = false;
            if (MATCH) { for (int iekšējais_amats = 0; iekšējais_amats < 값길이[Loop_INDEX]; iekšējais_amats++) 넣기(mainīgais_dati[Loop_INDEX * 256 + iekšējais_amats]); return; }
        }
    }
    static boolean Word_VALUE(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = Palaist[중첩깊이 * 128 + 낱말번호], beigt_zvanu_amats = 끝[중첩깊이 * 128 + 낱말번호], BASE_amats = 중첩깊이 * 4096, Citāts = 0;
        if (읽는자리 < beigt_zvanu_amats && AVOTS[BASE_amats + 읽는자리] == '~' && (읽는자리 + 1 == beigt_zvanu_amats || AVOTS[BASE_amats + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < beigt_zvanu_amats) {
            int koda_punkts = AVOTS[BASE_amats + 읽는자리++];
            if (koda_punkts == Citāts) { Citāts = 0; continue; }
            if (Citāts == 0 && (koda_punkts == 39 || koda_punkts == 34)) { Citāts = koda_punkts; continue; }
            if (koda_punkts == '\\' && Citāts != 39) { int Tālāk_amats = AVOTS[BASE_amats + 읽는자리++]; if (Citāts == 34 && Tālāk_amats != '$' && Tālāk_amats != '"' && Tālāk_amats != '\\') 넣기('\\'); 넣기(Tālāk_amats); continue; }
            if (koda_punkts == '$' && Citāts != 39 && 읽는자리 < beigt_zvanu_amats) {
                boolean 중괄호자리 = AVOTS[BASE_amats + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < beigt_zvanu_amats && AVOTS[BASE_amats + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < beigt_zvanu_amats && 이름뒤(AVOTS[BASE_amats + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == beigt_zvanu_amats || AVOTS[BASE_amats + 읽는자리] != '}')) { Kļūda("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                mainīgais_VALUE(AVOTS, BASE_amats + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(koda_punkts);
        }
        return !paplašinājums_kļūda;
    }
    static int 환경설정(int arg_INDEX, boolean noņemt) {
        int vietējs_Sākt = 명령해석기.시작점[arg_INDEX], beigt_zvanu_amats = vietējs_Sākt + 명령해석기.길이[arg_INDEX], 같음자리 = vietējs_Sākt;
        while (같음자리 < beigt_zvanu_amats && 명령해석기.daļiņa_VALUE[같음자리] != '=') 같음자리++;
        int ievade_COUNT = 같음자리 - vietējs_Sākt;
        if (ievade_COUNT < 1 || ievade_COUNT > 31 || !nosaukums_rakstzīme(명령해석기.daļiņa_VALUE[vietējs_Sākt]) || !noņemt && 같음자리 == beigt_zvanu_amats || beigt_zvanu_amats - 같음자리 - 1 > 255) return 2;
        for (int Loop_INDEX = vietējs_Sākt; Loop_INDEX < 같음자리; Loop_INDEX++) if (!이름뒤(명령해석기.daļiņa_VALUE[Loop_INDEX])) return 2;
        if (diapazons_SMS(명령해석기.daļiņa_VALUE, vietējs_Sākt, ievade_COUNT, "PWD") || diapazons_SMS(명령해석기.daļiņa_VALUE, vietējs_Sākt, ievade_COUNT, "HOME")) return 2;
        int 찾은여부 = -1, 빈여부 = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] == 0) 빈여부 = Loop_INDEX;
            if (이름길이[Loop_INDEX] != ievade_COUNT) continue;
            boolean MATCH = true; for (int iekšējais_amats = 0; iekšējais_amats < ievade_COUNT; iekšējais_amats++) if (mainīgais_nosaukums[Loop_INDEX * 32 + iekšējais_amats] != 명령해석기.daļiņa_VALUE[vietējs_Sākt + iekšējais_amats]) MATCH = false;
            if (MATCH) 찾은여부 = Loop_INDEX;
        }
        if (noņemt) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = 빈여부; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = ievade_COUNT; 값길이[찾은여부] = beigt_zvanu_amats - 같음자리 - 1;
        for (int Loop_INDEX = 0; Loop_INDEX < ievade_COUNT; Loop_INDEX++) mainīgais_nosaukums[찾은여부 * 32 + Loop_INDEX] = 명령해석기.daļiņa_VALUE[vietējs_Sākt + Loop_INDEX];
        for (int Loop_INDEX = 같음자리 + 1; Loop_INDEX < beigt_zvanu_amats; Loop_INDEX++) mainīgais_dati[찾은여부 * 256 + Loop_INDEX - 같음자리 - 1] = 명령해석기.daļiņa_VALUE[Loop_INDEX];
        return 0;
    }
    static void 환경보기() {
        단말.Rakstīt("HOME=/\nPWD="); atmiņa_Faili.pašreizējais_rakstīšana(); 단말.문자(10);
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] > 0) {
            for (int iekšējais_amats = 0; iekšējais_amats < 이름길이[Loop_INDEX]; iekšējais_amats++) Panelis.직렬쓰기(mainīgais_nosaukums[Loop_INDEX * 32 + iekšējais_amats]); 단말.문자('=');
            for (int iekšējais_amats = 0; iekšējais_amats < 값길이[Loop_INDEX]; iekšējais_amats++) Panelis.직렬쓰기(mainīgais_dati[Loop_INDEX * 256 + iekšējais_amats]); 단말.문자(10);
        }
    }
    static void Izpildīt_komanda(int[] dati_ARRAY, int 시작변위, int ievade_COUNT, int 중첩깊이) {
        if (중첩깊이 >= 4 || ievade_COUNT > 4096) { Kļūda("Komanda 파일의 ligzda_VALUE 또는 Līniju 길이 제한을 넘었습니다"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < ievade_COUNT; Loop_INDEX++) AVOTS[중첩깊이 * 4096 + Loop_INDEX] = dati_ARRAY[시작변위 + Loop_INDEX];
        int kopsumma_COUNT = Lasīt(ievade_COUNT, 중첩깊이); if (kopsumma_COUNT < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < kopsumma_COUNT) {
            int Grupa_beigt_zvanu = 읽는자리;
            while (Grupa_beigt_zvanu < kopsumma_COUNT && (종류[중첩깊이 * 128 + Grupa_beigt_zvanu] == 0 || 종류[중첩깊이 * 128 + Grupa_beigt_zvanu] >= 4)) Grupa_beigt_zvanu++;
            boolean Izpildīt_cc685ae5 = 조건성립 == 1 || 조건성립 == 2 && Statuss_VALUE == 0 || 조건성립 == 3 && Statuss_VALUE != 0;
            if (Izpildīt_cc685ae5) {
                boolean 이전자리 = false;
                while (읽는자리 < Grupa_beigt_zvanu) {
                    int Tālāk_amats = 읽는자리; while (Tālāk_amats < Grupa_beigt_zvanu && 종류[중첩깊이 * 128 + Tālāk_amats] != 4) Tālāk_amats++;
                    boolean saziņa_Stream = Tālāk_amats < Grupa_beigt_zvanu; int 입력쪽 = -1, ražojums_lapa = -1, 출력방식 = 0;
                    명령해석기.daļiņa_COUNT = 0; 쓴수 = 0; paplašinājums_kļūda = false;
                    for (int Loop_INDEX = 읽는자리; Loop_INDEX < Tālāk_amats; Loop_INDEX++) {
                        int 자료종류 = 종류[중첩깊이 * 128 + Loop_INDEX];
                        if (자료종류 >= 5) { if (자료종류 == 7) { if (입력쪽 >= 0) { Kļūda("입력 전환이 겹쳤습니다"); return; } 입력쪽 = ++Loop_INDEX; } else { if (ražojums_lapa >= 0) { Kļūda("Izvade 전환이 겹쳤습니다"); return; } ražojums_lapa = ++Loop_INDEX; 출력방식 = 자료종류; } continue; }
                        if (명령해석기.daļiņa_COUNT == 32) { Kļūda("인수가 너무 많습니다"); return; }
                        int arg_INDEX = 명령해석기.daļiņa_COUNT++; 명령해석기.시작점[arg_INDEX] = 쓴수;
                        if (!Word_VALUE(Loop_INDEX, 중첩깊이)) return;
                        명령해석기.길이[arg_INDEX] = 쓴수 - 명령해석기.시작점[arg_INDEX];
                    }
                    연결중 = 이전자리 || saziņa_Stream || 입력쪽 >= 0 || ražojums_lapa >= 0;
                    if (연결중 && (명령해석기.같음(0, "vi") || 명령해석기.같음(0, "edit") || 명령해석기.같음(0, "load") || 명령해석기.같음(0, "gui") || 명령해석기.같음(0, "terminal") || 명령해석기.같음(0, "sh") || 명령해석기.같음(0, "source"))) { Kļūda("대화형 명령과 Komanda 파일은 ievadizvade 전환이나 Stream_VALUE 연결에 쓸 numurs 없습니다"); return; }
                    셸입출력.Palaist(이전자리, saziņa_Stream);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int ievade_amats = 입출력바꿈 == 0 ? 입력쪽 : ražojums_lapa; if (ievade_amats < 0) continue;
                        int Sākt_amats = 쓴수; if (!Word_VALUE(ievade_amats, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = atmiņa_Faili.ceļš_Sākt(쓴수 - Sākt_amats);
                        for (int iekšējais_amats = Sākt_amats; 처리값 >= 0 && iekšējais_amats < 쓴수; iekšējais_amats++) 처리값 = atmiņa_Faili.ceļš_byte(iekšējais_amats - Sākt_amats, 명령해석기.daļiņa_VALUE[iekšējais_amats]);
                        if (처리값 >= 0) 처리값 = atmiņa_Faili.Atvērt(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); 명령해석기.Kļūda(처리값); Statuss_VALUE = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.ievades_fails = 처리값; else 셸입출력.izvades_fails = 처리값;
                    }
                    셸입출력.대화허용 = 중첩깊이 == 0 && 읽는자리 == 0 && Tālāk_amats == kopsumma_COUNT;
                    깊이 = 중첩깊이; 명령해석기.mērs = 0; Panelis.입출력전환(1);
                    명령해석기.Komanda();
                    Panelis.Terminālis(3);
                    int 반환값 = 명령해석기.mērs, Stream_kļūda = 셸입출력.kļūme_VALUE;
                    셸입출력.끝(); 연결중 = false;
                    Statuss_VALUE = Stream_kļūda < 0 ? 1 : 반환값;
                    if (Stream_kļūda < 0) { 명령해석기.Kļūda(Stream_kļūda); return; }
                    if (skripts_beigt_zvanu || 반환값 == -1005) return;
                    이전자리 = true; 읽는자리 = Tālāk_amats + 1;
                }
            }
            if (Grupa_beigt_zvanu < kopsumma_COUNT) 조건성립 = 종류[중첩깊이 * 128 + Grupa_beigt_zvanu];
            읽는자리 = Grupa_beigt_zvanu + 1;
        }
    }
    static void Izpildīt_Fails() {
        if (명령해석기.daļiņa_COUNT != 2 || 깊이 >= 3) { 명령해석기.mērs = 2; 단말.Rakstīt("사용법: sh Fails (ligzda_VALUE 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = 명령해석기.CEĻŠ(1); if (처리값 >= 0) 처리값 = atmiņa_Faili.Atvērt(0);
        if (처리값 < 0) { 명령해석기.Kļūda(처리값); return; }
        int ievade_COUNT = 0, byte_dati;
        while ((byte_dati = atmiņa_Faili.Lasīt(처리값)) != 256 && byte_dati >= 0 && ievade_COUNT < 16384) skripts_VALUE[중첩깊이 * 16384 + ievade_COUNT++] = byte_dati;
        atmiņa_Faili.Aizvērt(처리값); Panelis.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < ievade_COUNT && !skripts_beigt_zvanu;) {
            int beigt_zvanu_amats = 읽는자리; while (beigt_zvanu_amats < ievade_COUNT && skripts_VALUE[중첩깊이 * 16384 + beigt_zvanu_amats] != 10) beigt_zvanu_amats++;
            int 유효길이 = beigt_zvanu_amats - 읽는자리; if (유효길이 > 0 && skripts_VALUE[중첩깊이 * 16384 + beigt_zvanu_amats - 1] == 13) 유효길이--;
            Izpildīt_komanda(skripts_VALUE, 중첩깊이 * 16384 + 읽는자리, 유효길이, 중첩깊이); 읽는자리 = beigt_zvanu_amats + 1;
        }
        명령해석기.mērs = Statuss_VALUE; skripts_beigt_zvanu = false; 깊이 = 중첩깊이 - 1;
    }
}
