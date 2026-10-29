// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 pāhekoheko anga 문법. 파이프는 순차 kawe_tono, 환경은 같은 셸에서 공유한다. */
public final class anga_wetereo {
    static int[] pūtake = new int[4 * 4096], 종류 = new int[4 * 128], whakahaere = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] 변수이름 = new int[16 * 32], 변수값 = new int[16 * 256], 이름길이 = new int[16], uara_roa = new int[16];
    static int[] hōtuhi_uara = new int[4 * 16384];
    static int tūnga_uara, 깊이, 쓴수;
    static boolean 연결중, hōtuhi_mutu, toronga_hapa;
    static boolean ingoa_pūāhua(int waehere_pūāhua) { return waehere_pūāhua >= 'a' && waehere_pūāhua <= 'z' || waehere_pūāhua >= 'A' && waehere_pūāhua <= 'Z' || waehere_pūāhua == '_' || waehere_pūāhua >= 128; }
    static boolean 이름뒤(int waehere_pūāhua) { return ingoa_pūāhua(waehere_pūāhua) || waehere_pūāhua >= '0' && waehere_pūāhua <= '9'; }
    static void Pōhēhē(String Ngā_kupu) { papa.입출력전환(0); 단말.Tuhia("tono poroporo_uara: "); 단말.Tuhia(Ngā_kupu); 단말.문자(10); tūnga_uara = 2; }
    static int Pānuitia(int tāurunga_COUNT, int 중첩깊이) {
        int 현재자리 = 0, 총수 = 0, BASE_tūranga = 중첩깊이 * 4096, pūāhua_motuhake = 중첩깊이 * 128;
        while (현재자리 < tāurunga_COUNT) {
            while (현재자리 < tāurunga_COUNT && (pūtake[BASE_tūranga + 현재자리] == 32 || pūtake[BASE_tūranga + 현재자리] == 9)) 현재자리++;
            if (현재자리 == tāurunga_COUNT || pūtake[BASE_tūranga + 현재자리] == '#') break;
            if (총수 == 128) { Pōhēhē("낱말이 너무 많습니다"); return -1; }
            int Start_tūranga = 현재자리, waehere_pūāhua = pūtake[BASE_tūranga + 현재자리], 자료종류 = 0;
            if (waehere_pūāhua == ';') { 자료종류 = 1; 현재자리++; }
            else if (waehere_pūāhua == '&') { if (현재자리 + 1 >= tāurunga_COUNT || pūtake[BASE_tūranga + 현재자리 + 1] != '&') { Pōhēhē("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } 자료종류 = 2; 현재자리 += 2; }
            else if (waehere_pūāhua == '|') { 현재자리++; 자료종류 = 현재자리 < tāurunga_COUNT && pūtake[BASE_tūranga + 현재자리] == '|' ? 3 : 4; if (자료종류 == 3) 현재자리++; }
            else if (waehere_pūāhua == '>') { 현재자리++; 자료종류 = 현재자리 < tāurunga_COUNT && pūtake[BASE_tūranga + 현재자리] == '>' ? 6 : 5; if (자료종류 == 6) 현재자리++; }
            else if (waehere_pūāhua == '<') { 자료종류 = 7; 현재자리++; }
            else {
                int Kī_horipū = 0;
                while (현재자리 < tāurunga_COUNT) {
                    waehere_pūāhua = pūtake[BASE_tūranga + 현재자리];
                    if (waehere_pūāhua == '`' && Kī_horipū != 39 || waehere_pūāhua == '$' && Kī_horipū != 39 && 현재자리 + 1 < tāurunga_COUNT && pūtake[BASE_tūranga + 현재자리 + 1] == '(') { Pōhēhē("tono mēhua 치환은 지원하지 않습니다"); return -1; }
                    if (waehere_pūāhua == '\\' && Kī_horipū != 39) { if (++현재자리 == tāurunga_COUNT) { Pōhēhē("hononga 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } 현재자리++; continue; }
                    if (waehere_pūāhua == Kī_horipū) { Kī_horipū = 0; 현재자리++; continue; }
                    if (Kī_horipū == 0 && (waehere_pūāhua == 39 || waehere_pūāhua == 34)) { Kī_horipū = waehere_pūāhua; 현재자리++; continue; }
                    if (Kī_horipū == 0 && (waehere_pūāhua == 32 || waehere_pūāhua == 9 || waehere_pūāhua == ';' || waehere_pūāhua == '&' || waehere_pūāhua == '|' || waehere_pūāhua == '<' || waehere_pūāhua == '>')) break;
                    현재자리++;
                }
                if (Kī_horipū != 0) { Pōhēhē("따옴표가 닫히지 않았습니다"); return -1; }
                if (현재자리 < tāurunga_COUNT && (pūtake[BASE_tūranga + 현재자리] == '>' || pūtake[BASE_tūranga + 현재자리] == '<')) {
                    boolean 수치 = 현재자리 > Start_tūranga;
                    for (int Loop_INDEX = Start_tūranga; Loop_INDEX < 현재자리; Loop_INDEX++) if (pūtake[BASE_tūranga + Loop_INDEX] < '0' || pūtake[BASE_tūranga + Loop_INDEX] > '9') 수치 = false;
                    if (수치) { Pōhēhē("번호를 지정한 Kōnae 서술자 I_O 전환은 지원하지 않습니다"); return -1; }
                }
            }
            종류[pūāhua_motuhake + 총수] = 자료종류; whakahaere[pūāhua_motuhake + 총수] = Start_tūranga; 끝[pūāhua_motuhake + 총수] = 현재자리; 총수++;
        }
        boolean 낱말 = false;
        for (int Loop_INDEX = 0; Loop_INDEX < 총수; Loop_INDEX++) {
            int 임시값 = 종류[pūāhua_motuhake + Loop_INDEX];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++Loop_INDEX == 총수 || 종류[pūāhua_motuhake + Loop_INDEX] != 0) { Pōhēhē("I_O 전환에 Kōnae 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || Loop_INDEX == 총수 - 1 && 임시값 != 1) { Pōhēhē("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (총수 > 0 && !낱말 && 종류[pūāhua_motuhake + 총수 - 1] != 1) { Pōhēhē("명령이 빠졌습니다"); return -1; }
        return 총수;
    }
    static boolean 구간말(int[] raraunga_HUĀNGA, int paetata_Start, int tāurunga_COUNT, String pūāhua_tūranga) {
        if (tāurunga_COUNT != pūāhua_tūranga.length()) return false; for (int Loop_INDEX = 0; Loop_INDEX < tāurunga_COUNT; Loop_INDEX++) if (raraunga_HUĀNGA[paetata_Start + Loop_INDEX] != pūāhua_tūranga.charAt(Loop_INDEX)) return false; return true;
    }
    static void 넣기(int paita_raraunga) {
        if (쓴수 >= 명령해석기.tohu_uara_eb540501.length) { if (!toronga_hapa) Pōhēhē("변수를 펼친 명령이 너무 깁니다"); toronga_hapa = true; return; }
        명령해석기.tohu_uara_eb540501[쓴수++] = paita_raraunga;
    }
    static void 변수(int[] raraunga_HUĀNGA, int Start_tūranga, int tāurunga_COUNT) {
        if (구간말(raraunga_HUĀNGA, Start_tūranga, tāurunga_COUNT, "PWD")) { 넣기('/'); for (int Loop_INDEX = 0; Loop_INDEX < Pūmahara_Ngā_Kōnae.현재길이; Loop_INDEX++) 넣기(Pūmahara_Ngā_Kōnae.현재[Loop_INDEX]); return; }
        if (구간말(raraunga_HUĀNGA, Start_tūranga, tāurunga_COUNT, "HOME")) { 넣기('/'); return; }
        if (구간말(raraunga_HUĀNGA, Start_tūranga, tāurunga_COUNT, "?")) {
            int raraunga_uara = tūnga_uara, mati = 100; boolean 시작여부 = false;
            while (mati > 0) { int 뒷값 = raraunga_uara / mati; if (뒷값 != 0 || 시작여부 || mati == 1) { 넣기('0' + 뒷값); 시작여부 = true; } raraunga_uara %= mati; mati /= 10; } return;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] == tāurunga_COUNT) {
            boolean MATCH = true; for (int hono_roto_tūranga = 0; hono_roto_tūranga < tāurunga_COUNT; hono_roto_tūranga++) if (변수이름[Loop_INDEX * 32 + hono_roto_tūranga] != raraunga_HUĀNGA[Start_tūranga + hono_roto_tūranga]) MATCH = false;
            if (MATCH) { for (int hono_roto_tūranga = 0; hono_roto_tūranga < uara_roa[Loop_INDEX]; hono_roto_tūranga++) 넣기(변수값[Loop_INDEX * 256 + hono_roto_tūranga]); return; }
        }
    }
    static boolean Word_uara(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = whakahaere[중첩깊이 * 128 + 낱말번호], mutu_tūranga = 끝[중첩깊이 * 128 + 낱말번호], BASE_tūranga = 중첩깊이 * 4096, Kī_horipū = 0;
        if (읽는자리 < mutu_tūranga && pūtake[BASE_tūranga + 읽는자리] == '~' && (읽는자리 + 1 == mutu_tūranga || pūtake[BASE_tūranga + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < mutu_tūranga) {
            int waehere_pūāhua = pūtake[BASE_tūranga + 읽는자리++];
            if (waehere_pūāhua == Kī_horipū) { Kī_horipū = 0; continue; }
            if (Kī_horipū == 0 && (waehere_pūāhua == 39 || waehere_pūāhua == 34)) { Kī_horipū = waehere_pūāhua; continue; }
            if (waehere_pūāhua == '\\' && Kī_horipū != 39) { int Panuku_tūranga = pūtake[BASE_tūranga + 읽는자리++]; if (Kī_horipū == 34 && Panuku_tūranga != '$' && Panuku_tūranga != '"' && Panuku_tūranga != '\\') 넣기('\\'); 넣기(Panuku_tūranga); continue; }
            if (waehere_pūāhua == '$' && Kī_horipū != 39 && 읽는자리 < mutu_tūranga) {
                boolean 중괄호자리 = pūtake[BASE_tūranga + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < mutu_tūranga && pūtake[BASE_tūranga + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < mutu_tūranga && 이름뒤(pūtake[BASE_tūranga + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == mutu_tūranga || pūtake[BASE_tūranga + 읽는자리] != '}')) { Pōhēhē("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                변수(pūtake, BASE_tūranga + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(waehere_pūāhua);
        }
        return !toronga_hapa;
    }
    static int 환경설정(int tohenga_INDEX, boolean tango) {
        int paetata_Start = 명령해석기.시작점[tohenga_INDEX], mutu_tūranga = paetata_Start + 명령해석기.roa_uara[tohenga_INDEX], 같음자리 = paetata_Start;
        while (같음자리 < mutu_tūranga && 명령해석기.tohu_uara_eb540501[같음자리] != '=') 같음자리++;
        int tāurunga_COUNT = 같음자리 - paetata_Start;
        if (tāurunga_COUNT < 1 || tāurunga_COUNT > 31 || !ingoa_pūāhua(명령해석기.tohu_uara_eb540501[paetata_Start]) || !tango && 같음자리 == mutu_tūranga || mutu_tūranga - 같음자리 - 1 > 255) return 2;
        for (int Loop_INDEX = paetata_Start; Loop_INDEX < 같음자리; Loop_INDEX++) if (!이름뒤(명령해석기.tohu_uara_eb540501[Loop_INDEX])) return 2;
        if (구간말(명령해석기.tohu_uara_eb540501, paetata_Start, tāurunga_COUNT, "PWD") || 구간말(명령해석기.tohu_uara_eb540501, paetata_Start, tāurunga_COUNT, "HOME")) return 2;
        int 찾은여부 = -1, 빈여부 = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] == 0) 빈여부 = Loop_INDEX;
            if (이름길이[Loop_INDEX] != tāurunga_COUNT) continue;
            boolean MATCH = true; for (int hono_roto_tūranga = 0; hono_roto_tūranga < tāurunga_COUNT; hono_roto_tūranga++) if (변수이름[Loop_INDEX * 32 + hono_roto_tūranga] != 명령해석기.tohu_uara_eb540501[paetata_Start + hono_roto_tūranga]) MATCH = false;
            if (MATCH) 찾은여부 = Loop_INDEX;
        }
        if (tango) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = 빈여부; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = tāurunga_COUNT; uara_roa[찾은여부] = mutu_tūranga - 같음자리 - 1;
        for (int Loop_INDEX = 0; Loop_INDEX < tāurunga_COUNT; Loop_INDEX++) 변수이름[찾은여부 * 32 + Loop_INDEX] = 명령해석기.tohu_uara_eb540501[paetata_Start + Loop_INDEX];
        for (int Loop_INDEX = 같음자리 + 1; Loop_INDEX < mutu_tūranga; Loop_INDEX++) 변수값[찾은여부 * 256 + Loop_INDEX - 같음자리 - 1] = 명령해석기.tohu_uara_eb540501[Loop_INDEX];
        return 0;
    }
    static void 환경보기() {
        단말.Tuhia("HOME=/\nPWD="); Pūmahara_Ngā_Kōnae.현재쓰기(); 단말.문자(10);
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] > 0) {
            for (int hono_roto_tūranga = 0; hono_roto_tūranga < 이름길이[Loop_INDEX]; hono_roto_tūranga++) papa.직렬쓰기(변수이름[Loop_INDEX * 32 + hono_roto_tūranga]); 단말.문자('=');
            for (int hono_roto_tūranga = 0; hono_roto_tūranga < uara_roa[Loop_INDEX]; hono_roto_tūranga++) papa.직렬쓰기(변수값[Loop_INDEX * 256 + hono_roto_tūranga]); 단말.문자(10);
        }
    }
    static void kawe_tono(int[] raraunga_HUĀNGA, int 시작변위, int tāurunga_COUNT, int 중첩깊이) {
        if (중첩깊이 >= 4 || tāurunga_COUNT > 4096) { Pōhēhē("tono 파일의 중첩 또는 hononga roa_uara 제한을 넘었습니다"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < tāurunga_COUNT; Loop_INDEX++) pūtake[중첩깊이 * 4096 + Loop_INDEX] = raraunga_HUĀNGA[시작변위 + Loop_INDEX];
        int 총수 = Pānuitia(tāurunga_COUNT, 중첩깊이); if (총수 < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < 총수) {
            int rōpū_mutu = 읽는자리;
            while (rōpū_mutu < 총수 && (종류[중첩깊이 * 128 + rōpū_mutu] == 0 || 종류[중첩깊이 * 128 + rōpū_mutu] >= 4)) rōpū_mutu++;
            boolean kawe = 조건성립 == 1 || 조건성립 == 2 && tūnga_uara == 0 || 조건성립 == 3 && tūnga_uara != 0;
            if (kawe) {
                boolean 이전자리 = false;
                while (읽는자리 < rōpū_mutu) {
                    int Panuku_tūranga = 읽는자리; while (Panuku_tūranga < rōpū_mutu && 종류[중첩깊이 * 128 + Panuku_tūranga] != 4) Panuku_tūranga++;
                    boolean TŪHONO_roma = Panuku_tūranga < rōpū_mutu; int 입력쪽 = -1, 출력쪽 = -1, 출력방식 = 0;
                    명령해석기.tohu_COUNT = 0; 쓴수 = 0; toronga_hapa = false;
                    for (int Loop_INDEX = 읽는자리; Loop_INDEX < Panuku_tūranga; Loop_INDEX++) {
                        int 자료종류 = 종류[중첩깊이 * 128 + Loop_INDEX];
                        if (자료종류 >= 5) { if (자료종류 == 7) { if (입력쪽 >= 0) { Pōhēhē("입력 전환이 겹쳤습니다"); return; } 입력쪽 = ++Loop_INDEX; } else { if (출력쪽 >= 0) { Pōhēhē("출력 전환이 겹쳤습니다"); return; } 출력쪽 = ++Loop_INDEX; 출력방식 = 자료종류; } continue; }
                        if (명령해석기.tohu_COUNT == 32) { Pōhēhē("인수가 너무 많습니다"); return; }
                        int tohenga_INDEX = 명령해석기.tohu_COUNT++; 명령해석기.시작점[tohenga_INDEX] = 쓴수;
                        if (!Word_uara(Loop_INDEX, 중첩깊이)) return;
                        명령해석기.roa_uara[tohenga_INDEX] = 쓴수 - 명령해석기.시작점[tohenga_INDEX];
                    }
                    연결중 = 이전자리 || TŪHONO_roma || 입력쪽 >= 0 || 출력쪽 >= 0;
                    if (연결중 && (명령해석기.같음(0, "vi") || 명령해석기.같음(0, "edit") || 명령해석기.같음(0, "load") || 명령해석기.같음(0, "gui") || 명령해석기.같음(0, "terminal") || 명령해석기.같음(0, "sh") || 명령해석기.같음(0, "source"))) { Pōhēhē("pāhekoheko 명령과 tono 파일은 I_O 전환이나 roma_uara 연결에 쓸 수 없습니다"); return; }
                    셸입출력.whakahaere(이전자리, TŪHONO_roma);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int tāurunga_tūranga = 입출력바꿈 == 0 ? 입력쪽 : 출력쪽; if (tāurunga_tūranga < 0) continue;
                        int Start_tūranga = 쓴수; if (!Word_uara(tāurunga_tūranga, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = Pūmahara_Ngā_Kōnae.ara_Start(쓴수 - Start_tūranga);
                        for (int hono_roto_tūranga = Start_tūranga; 처리값 >= 0 && hono_roto_tūranga < 쓴수; hono_roto_tūranga++) 처리값 = Pūmahara_Ngā_Kōnae.ara_paita(hono_roto_tūranga - Start_tūranga, 명령해석기.tohu_uara_eb540501[hono_roto_tūranga]);
                        if (처리값 >= 0) 처리값 = Pūmahara_Ngā_Kōnae.Huaki(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); 명령해석기.Pōhēhē(처리값); tūnga_uara = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.입력파일 = 처리값; else 셸입출력.kōnae_huaputa = 처리값;
                    }
                    셸입출력.Tuku_pāhekoheko = 중첩깊이 == 0 && 읽는자리 == 0 && Panuku_tūranga == 총수;
                    깊이 = 중첩깊이; 명령해석기.mēhua = 0; papa.입출력전환(1);
                    명령해석기.tono();
                    papa.Tauranga(3);
                    int 반환값 = 명령해석기.mēhua, roma_hapa = 셸입출력.rahunga_uara;
                    셸입출력.끝(); 연결중 = false;
                    tūnga_uara = roma_hapa < 0 ? 1 : 반환값;
                    if (roma_hapa < 0) { 명령해석기.Pōhēhē(roma_hapa); return; }
                    if (hōtuhi_mutu || 반환값 == -1005) return;
                    이전자리 = true; 읽는자리 = Panuku_tūranga + 1;
                }
            }
            if (rōpū_mutu < 총수) 조건성립 = 종류[중첩깊이 * 128 + rōpū_mutu];
            읽는자리 = rōpū_mutu + 1;
        }
    }
    static void kawe_kōnae() {
        if (명령해석기.tohu_COUNT != 2 || 깊이 >= 3) { 명령해석기.mēhua = 2; 단말.Tuhia("사용법: sh Kōnae (중첩 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = 명령해석기.ara(1); if (처리값 >= 0) 처리값 = Pūmahara_Ngā_Kōnae.Huaki(0);
        if (처리값 < 0) { 명령해석기.Pōhēhē(처리값); return; }
        int tāurunga_COUNT = 0, paita_raraunga;
        while ((paita_raraunga = Pūmahara_Ngā_Kōnae.Pānuitia(처리값)) != 256 && paita_raraunga >= 0 && tāurunga_COUNT < 16384) hōtuhi_uara[중첩깊이 * 16384 + tāurunga_COUNT++] = paita_raraunga;
        Pūmahara_Ngā_Kōnae.Kati(처리값); papa.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < tāurunga_COUNT && !hōtuhi_mutu;) {
            int mutu_tūranga = 읽는자리; while (mutu_tūranga < tāurunga_COUNT && hōtuhi_uara[중첩깊이 * 16384 + mutu_tūranga] != 10) mutu_tūranga++;
            int 유효길이 = mutu_tūranga - 읽는자리; if (유효길이 > 0 && hōtuhi_uara[중첩깊이 * 16384 + mutu_tūranga - 1] == 13) 유효길이--;
            kawe_tono(hōtuhi_uara, 중첩깊이 * 16384 + 읽는자리, 유효길이, 중첩깊이); 읽는자리 = mutu_tūranga + 1;
        }
        명령해석기.mēhua = tūnga_uara; hōtuhi_mutu = false; 깊이 = 중첩깊이 - 1;
    }
}
