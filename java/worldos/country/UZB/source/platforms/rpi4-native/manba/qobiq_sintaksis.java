// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 o_zaro_faol qobiq 문법. 파이프는 순차 bajarmoq_buyruq, 환경은 같은 셸에서 공유한다. */
public final class qobiq_sintaksis {
    static int[] manba = new int[4 * 4096], 종류 = new int[4 * 128], Bajarish = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] 변수이름 = new int[16 * 32], 변수값 = new int[16 * 256], 이름길이 = new int[16], VALUE_uzunlik = new int[16];
    static int[] ssenariy_VALUE = new int[4 * 16384];
    static int holat_VALUE_e10195a1, 깊이, 쓴수;
    static boolean 연결중, ssenariy_to_xtatmoq, kengaytma_xato;
    static boolean nom_belgi(int belgi_kodi) { return belgi_kodi >= 'a' && belgi_kodi <= 'z' || belgi_kodi >= 'A' && belgi_kodi <= 'Z' || belgi_kodi == '_' || belgi_kodi >= 128; }
    static boolean 이름뒤(int belgi_kodi) { return nom_belgi(belgi_kodi) || belgi_kodi >= '0' && belgi_kodi <= '9'; }
    static void Xato(String Matn) { yozuv_taxtasi.입출력전환(0); 단말.Yozish("Buyruq tahlil_qilmoq_VALUE: "); 단말.Yozish(Matn); 단말.문자(10); holat_VALUE_e10195a1 = 2; }
    static int Oʻqish(int kiritish_COUNT, int 중첩깊이) {
        int 현재자리 = 0, 총수 = 0, BASE_holat = 중첩깊이 * 4096, maxsus_belgi = 중첩깊이 * 128;
        while (현재자리 < kiritish_COUNT) {
            while (현재자리 < kiritish_COUNT && (manba[BASE_holat + 현재자리] == 32 || manba[BASE_holat + 현재자리] == 9)) 현재자리++;
            if (현재자리 == kiritish_COUNT || manba[BASE_holat + 현재자리] == '#') break;
            if (총수 == 128) { Xato("낱말이 너무 많습니다"); return -1; }
            int Start_holat = 현재자리, belgi_kodi = manba[BASE_holat + 현재자리], 자료종류 = 0;
            if (belgi_kodi == ';') { 자료종류 = 1; 현재자리++; }
            else if (belgi_kodi == '&') { if (현재자리 + 1 >= kiritish_COUNT || manba[BASE_holat + 현재자리 + 1] != '&') { Xato("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } 자료종류 = 2; 현재자리 += 2; }
            else if (belgi_kodi == '|') { 현재자리++; 자료종류 = 현재자리 < kiritish_COUNT && manba[BASE_holat + 현재자리] == '|' ? 3 : 4; if (자료종류 == 3) 현재자리++; }
            else if (belgi_kodi == '>') { 현재자리++; 자료종류 = 현재자리 < kiritish_COUNT && manba[BASE_holat + 현재자리] == '>' ? 6 : 5; if (자료종류 == 6) 현재자리++; }
            else if (belgi_kodi == '<') { 자료종류 = 7; 현재자리++; }
            else {
                int Sitata_kiritish = 0;
                while (현재자리 < kiritish_COUNT) {
                    belgi_kodi = manba[BASE_holat + 현재자리];
                    if (belgi_kodi == '`' && Sitata_kiritish != 39 || belgi_kodi == '$' && Sitata_kiritish != 39 && 현재자리 + 1 < kiritish_COUNT && manba[BASE_holat + 현재자리 + 1] == '(') { Xato("Buyruq o_lchov 치환은 지원하지 않습니다"); return -1; }
                    if (belgi_kodi == '\\' && Sitata_kiritish != 39) { if (++현재자리 == kiritish_COUNT) { Xato("satr 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } 현재자리++; continue; }
                    if (belgi_kodi == Sitata_kiritish) { Sitata_kiritish = 0; 현재자리++; continue; }
                    if (Sitata_kiritish == 0 && (belgi_kodi == 39 || belgi_kodi == 34)) { Sitata_kiritish = belgi_kodi; 현재자리++; continue; }
                    if (Sitata_kiritish == 0 && (belgi_kodi == 32 || belgi_kodi == 9 || belgi_kodi == ';' || belgi_kodi == '&' || belgi_kodi == '|' || belgi_kodi == '<' || belgi_kodi == '>')) break;
                    현재자리++;
                }
                if (Sitata_kiritish != 0) { Xato("따옴표가 닫히지 않았습니다"); return -1; }
                if (현재자리 < kiritish_COUNT && (manba[BASE_holat + 현재자리] == '>' || manba[BASE_holat + 현재자리] == '<')) {
                    boolean 수치 = 현재자리 > Start_holat;
                    for (int Loop_INDEX = Start_holat; Loop_INDEX < 현재자리; Loop_INDEX++) if (manba[BASE_holat + Loop_INDEX] < '0' || manba[BASE_holat + Loop_INDEX] > '9') 수치 = false;
                    if (수치) { Xato("번호를 지정한 Fayl 서술자 I_O 전환은 지원하지 않습니다"); return -1; }
                }
            }
            종류[maxsus_belgi + 총수] = 자료종류; Bajarish[maxsus_belgi + 총수] = Start_holat; 끝[maxsus_belgi + 총수] = 현재자리; 총수++;
        }
        boolean 낱말 = false;
        for (int Loop_INDEX = 0; Loop_INDEX < 총수; Loop_INDEX++) {
            int 임시값 = 종류[maxsus_belgi + Loop_INDEX];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++Loop_INDEX == 총수 || 종류[maxsus_belgi + Loop_INDEX] != 0) { Xato("I_O 전환에 Fayl 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || Loop_INDEX == 총수 - 1 && 임시값 != 1) { Xato("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (총수 > 0 && !낱말 && 종류[maxsus_belgi + 총수 - 1] != 1) { Xato("명령이 빠졌습니다"); return -1; }
        return 총수;
    }
    static boolean 구간말(int[] ma_lumotlar_ARRAY, int mahalliy_Start, int kiritish_COUNT, String belgi_holat) {
        if (kiritish_COUNT != belgi_holat.length()) return false; for (int Loop_INDEX = 0; Loop_INDEX < kiritish_COUNT; Loop_INDEX++) if (ma_lumotlar_ARRAY[mahalliy_Start + Loop_INDEX] != belgi_holat.charAt(Loop_INDEX)) return false; return true;
    }
    static void 넣기(int bayt_ma_lumotlar) {
        if (쓴수 >= 명령해석기.token_VALUE.length) { if (!kengaytma_xato) Xato("변수를 펼친 명령이 너무 깁니다"); kengaytma_xato = true; return; }
        명령해석기.token_VALUE[쓴수++] = bayt_ma_lumotlar;
    }
    static void 변수(int[] ma_lumotlar_ARRAY, int Start_holat, int kiritish_COUNT) {
        if (구간말(ma_lumotlar_ARRAY, Start_holat, kiritish_COUNT, "PWD")) { 넣기('/'); for (int Loop_INDEX = 0; Loop_INDEX < Xotira_Fayllar.현재길이; Loop_INDEX++) 넣기(Xotira_Fayllar.현재[Loop_INDEX]); return; }
        if (구간말(ma_lumotlar_ARRAY, Start_holat, kiritish_COUNT, "HOME")) { 넣기('/'); return; }
        if (구간말(ma_lumotlar_ARRAY, Start_holat, kiritish_COUNT, "?")) {
            int ma_lumotlar_VALUE = holat_VALUE_e10195a1, raqam = 100; boolean 시작여부 = false;
            while (raqam > 0) { int 뒷값 = ma_lumotlar_VALUE / raqam; if (뒷값 != 0 || 시작여부 || raqam == 1) { 넣기('0' + 뒷값); 시작여부 = true; } ma_lumotlar_VALUE %= raqam; raqam /= 10; } return;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] == kiritish_COUNT) {
            boolean MATCH = true; for (int ichki_qo_shilish_holat = 0; ichki_qo_shilish_holat < kiritish_COUNT; ichki_qo_shilish_holat++) if (변수이름[Loop_INDEX * 32 + ichki_qo_shilish_holat] != ma_lumotlar_ARRAY[Start_holat + ichki_qo_shilish_holat]) MATCH = false;
            if (MATCH) { for (int ichki_qo_shilish_holat = 0; ichki_qo_shilish_holat < VALUE_uzunlik[Loop_INDEX]; ichki_qo_shilish_holat++) 넣기(변수값[Loop_INDEX * 256 + ichki_qo_shilish_holat]); return; }
        }
    }
    static boolean Word_VALUE(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = Bajarish[중첩깊이 * 128 + 낱말번호], to_xtatmoq_holat = 끝[중첩깊이 * 128 + 낱말번호], BASE_holat = 중첩깊이 * 4096, Sitata_kiritish = 0;
        if (읽는자리 < to_xtatmoq_holat && manba[BASE_holat + 읽는자리] == '~' && (읽는자리 + 1 == to_xtatmoq_holat || manba[BASE_holat + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < to_xtatmoq_holat) {
            int belgi_kodi = manba[BASE_holat + 읽는자리++];
            if (belgi_kodi == Sitata_kiritish) { Sitata_kiritish = 0; continue; }
            if (Sitata_kiritish == 0 && (belgi_kodi == 39 || belgi_kodi == 34)) { Sitata_kiritish = belgi_kodi; continue; }
            if (belgi_kodi == '\\' && Sitata_kiritish != 39) { int Keyingi_holat = manba[BASE_holat + 읽는자리++]; if (Sitata_kiritish == 34 && Keyingi_holat != '$' && Keyingi_holat != '"' && Keyingi_holat != '\\') 넣기('\\'); 넣기(Keyingi_holat); continue; }
            if (belgi_kodi == '$' && Sitata_kiritish != 39 && 읽는자리 < to_xtatmoq_holat) {
                boolean 중괄호자리 = manba[BASE_holat + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < to_xtatmoq_holat && manba[BASE_holat + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < to_xtatmoq_holat && 이름뒤(manba[BASE_holat + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == to_xtatmoq_holat || manba[BASE_holat + 읽는자리] != '}')) { Xato("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                변수(manba, BASE_holat + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(belgi_kodi);
        }
        return !kengaytma_xato;
    }
    static int 환경설정(int dalil_INDEX, boolean olib_tashlamoq) {
        int mahalliy_Start = 명령해석기.시작점[dalil_INDEX], to_xtatmoq_holat = mahalliy_Start + 명령해석기.uzunlik_VALUE[dalil_INDEX], 같음자리 = mahalliy_Start;
        while (같음자리 < to_xtatmoq_holat && 명령해석기.token_VALUE[같음자리] != '=') 같음자리++;
        int kiritish_COUNT = 같음자리 - mahalliy_Start;
        if (kiritish_COUNT < 1 || kiritish_COUNT > 31 || !nom_belgi(명령해석기.token_VALUE[mahalliy_Start]) || !olib_tashlamoq && 같음자리 == to_xtatmoq_holat || to_xtatmoq_holat - 같음자리 - 1 > 255) return 2;
        for (int Loop_INDEX = mahalliy_Start; Loop_INDEX < 같음자리; Loop_INDEX++) if (!이름뒤(명령해석기.token_VALUE[Loop_INDEX])) return 2;
        if (구간말(명령해석기.token_VALUE, mahalliy_Start, kiritish_COUNT, "PWD") || 구간말(명령해석기.token_VALUE, mahalliy_Start, kiritish_COUNT, "HOME")) return 2;
        int 찾은여부 = -1, 빈여부 = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] == 0) 빈여부 = Loop_INDEX;
            if (이름길이[Loop_INDEX] != kiritish_COUNT) continue;
            boolean MATCH = true; for (int ichki_qo_shilish_holat = 0; ichki_qo_shilish_holat < kiritish_COUNT; ichki_qo_shilish_holat++) if (변수이름[Loop_INDEX * 32 + ichki_qo_shilish_holat] != 명령해석기.token_VALUE[mahalliy_Start + ichki_qo_shilish_holat]) MATCH = false;
            if (MATCH) 찾은여부 = Loop_INDEX;
        }
        if (olib_tashlamoq) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = 빈여부; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = kiritish_COUNT; VALUE_uzunlik[찾은여부] = to_xtatmoq_holat - 같음자리 - 1;
        for (int Loop_INDEX = 0; Loop_INDEX < kiritish_COUNT; Loop_INDEX++) 변수이름[찾은여부 * 32 + Loop_INDEX] = 명령해석기.token_VALUE[mahalliy_Start + Loop_INDEX];
        for (int Loop_INDEX = 같음자리 + 1; Loop_INDEX < to_xtatmoq_holat; Loop_INDEX++) 변수값[찾은여부 * 256 + Loop_INDEX - 같음자리 - 1] = 명령해석기.token_VALUE[Loop_INDEX];
        return 0;
    }
    static void 환경보기() {
        단말.Yozish("HOME=/\nPWD="); Xotira_Fayllar.현재쓰기(); 단말.문자(10);
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] > 0) {
            for (int ichki_qo_shilish_holat = 0; ichki_qo_shilish_holat < 이름길이[Loop_INDEX]; ichki_qo_shilish_holat++) yozuv_taxtasi.직렬쓰기(변수이름[Loop_INDEX * 32 + ichki_qo_shilish_holat]); 단말.문자('=');
            for (int ichki_qo_shilish_holat = 0; ichki_qo_shilish_holat < VALUE_uzunlik[Loop_INDEX]; ichki_qo_shilish_holat++) yozuv_taxtasi.직렬쓰기(변수값[Loop_INDEX * 256 + ichki_qo_shilish_holat]); 단말.문자(10);
        }
    }
    static void bajarmoq_buyruq(int[] ma_lumotlar_ARRAY, int 시작변위, int kiritish_COUNT, int 중첩깊이) {
        if (중첩깊이 >= 4 || kiritish_COUNT > 4096) { Xato("Buyruq 파일의 ichiga_joylangan_VALUE 또는 satr uzunlik_VALUE 제한을 넘었습니다"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < kiritish_COUNT; Loop_INDEX++) manba[중첩깊이 * 4096 + Loop_INDEX] = ma_lumotlar_ARRAY[시작변위 + Loop_INDEX];
        int 총수 = Oʻqish(kiritish_COUNT, 중첩깊이); if (총수 < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < 총수) {
            int Guruh_to_xtatmoq = 읽는자리;
            while (Guruh_to_xtatmoq < 총수 && (종류[중첩깊이 * 128 + Guruh_to_xtatmoq] == 0 || 종류[중첩깊이 * 128 + Guruh_to_xtatmoq] >= 4)) Guruh_to_xtatmoq++;
            boolean bajarmoq = 조건성립 == 1 || 조건성립 == 2 && holat_VALUE_e10195a1 == 0 || 조건성립 == 3 && holat_VALUE_e10195a1 != 0;
            if (bajarmoq) {
                boolean 이전자리 = false;
                while (읽는자리 < Guruh_to_xtatmoq) {
                    int Keyingi_holat = 읽는자리; while (Keyingi_holat < Guruh_to_xtatmoq && 종류[중첩깊이 * 128 + Keyingi_holat] != 4) Keyingi_holat++;
                    boolean ulash_oqim = Keyingi_holat < Guruh_to_xtatmoq; int 입력쪽 = -1, 출력쪽 = -1, 출력방식 = 0;
                    명령해석기.token_COUNT = 0; 쓴수 = 0; kengaytma_xato = false;
                    for (int Loop_INDEX = 읽는자리; Loop_INDEX < Keyingi_holat; Loop_INDEX++) {
                        int 자료종류 = 종류[중첩깊이 * 128 + Loop_INDEX];
                        if (자료종류 >= 5) { if (자료종류 == 7) { if (입력쪽 >= 0) { Xato("입력 전환이 겹쳤습니다"); return; } 입력쪽 = ++Loop_INDEX; } else { if (출력쪽 >= 0) { Xato("출력 전환이 겹쳤습니다"); return; } 출력쪽 = ++Loop_INDEX; 출력방식 = 자료종류; } continue; }
                        if (명령해석기.token_COUNT == 32) { Xato("인수가 너무 많습니다"); return; }
                        int dalil_INDEX = 명령해석기.token_COUNT++; 명령해석기.시작점[dalil_INDEX] = 쓴수;
                        if (!Word_VALUE(Loop_INDEX, 중첩깊이)) return;
                        명령해석기.uzunlik_VALUE[dalil_INDEX] = 쓴수 - 명령해석기.시작점[dalil_INDEX];
                    }
                    연결중 = 이전자리 || ulash_oqim || 입력쪽 >= 0 || 출력쪽 >= 0;
                    if (연결중 && (명령해석기.같음(0, "vi") || 명령해석기.같음(0, "edit") || 명령해석기.같음(0, "load") || 명령해석기.같음(0, "gui") || 명령해석기.같음(0, "terminal") || 명령해석기.같음(0, "sh") || 명령해석기.같음(0, "source"))) { Xato("o_zaro_faol 명령과 Buyruq 파일은 I_O 전환이나 oqim_VALUE 연결에 쓸 수 없습니다"); return; }
                    셸입출력.Bajarish(이전자리, ulash_oqim);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int kiritish_holat = 입출력바꿈 == 0 ? 입력쪽 : 출력쪽; if (kiritish_holat < 0) continue;
                        int Start_holat = 쓴수; if (!Word_VALUE(kiritish_holat, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = Xotira_Fayllar.yo_l_Start(쓴수 - Start_holat);
                        for (int ichki_qo_shilish_holat = Start_holat; 처리값 >= 0 && ichki_qo_shilish_holat < 쓴수; ichki_qo_shilish_holat++) 처리값 = Xotira_Fayllar.yo_l_bayt(ichki_qo_shilish_holat - Start_holat, 명령해석기.token_VALUE[ichki_qo_shilish_holat]);
                        if (처리값 >= 0) 처리값 = Xotira_Fayllar.Ochish(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); 명령해석기.Xato(처리값); holat_VALUE_e10195a1 = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.입력파일 = 처리값; else 셸입출력.chiqish_fayli = 처리값;
                    }
                    셸입출력.Ruxsatnoma_o_zaro_faol = 중첩깊이 == 0 && 읽는자리 == 0 && Keyingi_holat == 총수;
                    깊이 = 중첩깊이; 명령해석기.o_lchov = 0; yozuv_taxtasi.입출력전환(1);
                    명령해석기.Buyruq();
                    yozuv_taxtasi.Terminal(3);
                    int 반환값 = 명령해석기.o_lchov, oqim_xato = 셸입출력.to_xtab_qolish_VALUE;
                    셸입출력.끝(); 연결중 = false;
                    holat_VALUE_e10195a1 = oqim_xato < 0 ? 1 : 반환값;
                    if (oqim_xato < 0) { 명령해석기.Xato(oqim_xato); return; }
                    if (ssenariy_to_xtatmoq || 반환값 == -1005) return;
                    이전자리 = true; 읽는자리 = Keyingi_holat + 1;
                }
            }
            if (Guruh_to_xtatmoq < 총수) 조건성립 = 종류[중첩깊이 * 128 + Guruh_to_xtatmoq];
            읽는자리 = Guruh_to_xtatmoq + 1;
        }
    }
    static void bajarmoq_fayl() {
        if (명령해석기.token_COUNT != 2 || 깊이 >= 3) { 명령해석기.o_lchov = 2; 단말.Yozish("사용법: sh Fayl (ichiga_joylangan_VALUE 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = 명령해석기.yo_l(1); if (처리값 >= 0) 처리값 = Xotira_Fayllar.Ochish(0);
        if (처리값 < 0) { 명령해석기.Xato(처리값); return; }
        int kiritish_COUNT = 0, bayt_ma_lumotlar;
        while ((bayt_ma_lumotlar = Xotira_Fayllar.Oʻqish(처리값)) != 256 && bayt_ma_lumotlar >= 0 && kiritish_COUNT < 16384) ssenariy_VALUE[중첩깊이 * 16384 + kiritish_COUNT++] = bayt_ma_lumotlar;
        Xotira_Fayllar.Yopish(처리값); yozuv_taxtasi.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < kiritish_COUNT && !ssenariy_to_xtatmoq;) {
            int to_xtatmoq_holat = 읽는자리; while (to_xtatmoq_holat < kiritish_COUNT && ssenariy_VALUE[중첩깊이 * 16384 + to_xtatmoq_holat] != 10) to_xtatmoq_holat++;
            int 유효길이 = to_xtatmoq_holat - 읽는자리; if (유효길이 > 0 && ssenariy_VALUE[중첩깊이 * 16384 + to_xtatmoq_holat - 1] == 13) 유효길이--;
            bajarmoq_buyruq(ssenariy_VALUE, 중첩깊이 * 16384 + 읽는자리, 유효길이, 중첩깊이); 읽는자리 = to_xtatmoq_holat + 1;
        }
        명령해석기.o_lchov = holat_VALUE_e10195a1; ssenariy_to_xtatmoq = false; 깊이 = 중첩깊이 - 1;
    }
}
