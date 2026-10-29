// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 대화형 kest 문법. 파이프는 순차 Täida_käsk, 환경은 같은 셸에서 공유한다. */
public final class kest_süntaks {
    static int[] ALLIKAS = new int[4 * 4096], 종류 = new int[4 * 128], Käivita_2 = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] 변수이름 = new int[16 * 32], 변수값 = new int[16 * 256], 이름길이 = new int[16], 값길이 = new int[16];
    static int[] skript_VALUE = new int[4 * 16384];
    static int Olek_VALUE, 깊이, 쓴수;
    static boolean 연결중, skript_lõpeta_kõne, laiendus_tõrge;
    static boolean nimetus_märk(int koodipunkt) { return koodipunkt >= 'a' && koodipunkt <= 'z' || koodipunkt >= 'A' && koodipunkt <= 'Z' || koodipunkt == '_' || koodipunkt >= 128; }
    static boolean 이름뒤(int koodipunkt) { return nimetus_märk(koodipunkt) || koodipunkt >= '0' && koodipunkt <= '9'; }
    static void VIGA(String Tekst) { Tahvel.입출력전환(0); 단말.Kirjutamine("Käsk sõeluma_VALUE: "); 단말.Kirjutamine(Tekst); 단말.문자(10); Olek_VALUE = 2; }
    static int Lugemine(int kirje_COUNT, int 중첩깊이) {
        int tähtaja_piires_INDEX = 0, kokku_COUNT = 0, BASE_ametikoht = 중첩깊이 * 4096, erimärk = 중첩깊이 * 128;
        while (tähtaja_piires_INDEX < kirje_COUNT) {
            while (tähtaja_piires_INDEX < kirje_COUNT && (ALLIKAS[BASE_ametikoht + tähtaja_piires_INDEX] == 32 || ALLIKAS[BASE_ametikoht + tähtaja_piires_INDEX] == 9)) tähtaja_piires_INDEX++;
            if (tähtaja_piires_INDEX == kirje_COUNT || ALLIKAS[BASE_ametikoht + tähtaja_piires_INDEX] == '#') break;
            if (kokku_COUNT == 128) { VIGA("낱말이 너무 많습니다"); return -1; }
            int START_ametikoht = tähtaja_piires_INDEX, koodipunkt = ALLIKAS[BASE_ametikoht + tähtaja_piires_INDEX], 자료종류 = 0;
            if (koodipunkt == ';') { 자료종류 = 1; tähtaja_piires_INDEX++; }
            else if (koodipunkt == '&') { if (tähtaja_piires_INDEX + 1 >= kirje_COUNT || ALLIKAS[BASE_ametikoht + tähtaja_piires_INDEX + 1] != '&') { VIGA("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } 자료종류 = 2; tähtaja_piires_INDEX += 2; }
            else if (koodipunkt == '|') { tähtaja_piires_INDEX++; 자료종류 = tähtaja_piires_INDEX < kirje_COUNT && ALLIKAS[BASE_ametikoht + tähtaja_piires_INDEX] == '|' ? 3 : 4; if (자료종류 == 3) tähtaja_piires_INDEX++; }
            else if (koodipunkt == '>') { tähtaja_piires_INDEX++; 자료종류 = tähtaja_piires_INDEX < kirje_COUNT && ALLIKAS[BASE_ametikoht + tähtaja_piires_INDEX] == '>' ? 6 : 5; if (자료종류 == 6) tähtaja_piires_INDEX++; }
            else if (koodipunkt == '<') { 자료종류 = 7; tähtaja_piires_INDEX++; }
            else {
                int Tsitaat = 0;
                while (tähtaja_piires_INDEX < kirje_COUNT) {
                    koodipunkt = ALLIKAS[BASE_ametikoht + tähtaja_piires_INDEX];
                    if (koodipunkt == '`' && Tsitaat != 39 || koodipunkt == '$' && Tsitaat != 39 && tähtaja_piires_INDEX + 1 < kirje_COUNT && ALLIKAS[BASE_ametikoht + tähtaja_piires_INDEX + 1] == '(') { VIGA("Käsk TULEMUS 치환은 지원하지 않습니다"); return -1; }
                    if (koodipunkt == '\\' && Tsitaat != 39) { if (++tähtaja_piires_INDEX == kirje_COUNT) { VIGA("Joon 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } tähtaja_piires_INDEX++; continue; }
                    if (koodipunkt == Tsitaat) { Tsitaat = 0; tähtaja_piires_INDEX++; continue; }
                    if (Tsitaat == 0 && (koodipunkt == 39 || koodipunkt == 34)) { Tsitaat = koodipunkt; tähtaja_piires_INDEX++; continue; }
                    if (Tsitaat == 0 && (koodipunkt == 32 || koodipunkt == 9 || koodipunkt == ';' || koodipunkt == '&' || koodipunkt == '|' || koodipunkt == '<' || koodipunkt == '>')) break;
                    tähtaja_piires_INDEX++;
                }
                if (Tsitaat != 0) { VIGA("따옴표가 닫히지 않았습니다"); return -1; }
                if (tähtaja_piires_INDEX < kirje_COUNT && (ALLIKAS[BASE_ametikoht + tähtaja_piires_INDEX] == '>' || ALLIKAS[BASE_ametikoht + tähtaja_piires_INDEX] == '<')) {
                    boolean 수치 = tähtaja_piires_INDEX > START_ametikoht;
                    for (int Loop_INDEX = START_ametikoht; Loop_INDEX < tähtaja_piires_INDEX; Loop_INDEX++) if (ALLIKAS[BASE_ametikoht + Loop_INDEX] < '0' || ALLIKAS[BASE_ametikoht + Loop_INDEX] > '9') 수치 = false;
                    if (수치) { VIGA("번호를 지정한 Fail 서술자 I_O 전환은 지원하지 않습니다"); return -1; }
                }
            }
            종류[erimärk + kokku_COUNT] = 자료종류; Käivita_2[erimärk + kokku_COUNT] = START_ametikoht; 끝[erimärk + kokku_COUNT] = tähtaja_piires_INDEX; kokku_COUNT++;
        }
        boolean 낱말 = false;
        for (int Loop_INDEX = 0; Loop_INDEX < kokku_COUNT; Loop_INDEX++) {
            int 임시값 = 종류[erimärk + Loop_INDEX];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++Loop_INDEX == kokku_COUNT || 종류[erimärk + Loop_INDEX] != 0) { VIGA("I_O 전환에 Fail 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || Loop_INDEX == kokku_COUNT - 1 && 임시값 != 1) { VIGA("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (kokku_COUNT > 0 && !낱말 && 종류[erimärk + kokku_COUNT - 1] != 1) { VIGA("명령이 빠졌습니다"); return -1; }
        return kokku_COUNT;
    }
    static boolean vahemik_SMS(int[] andmed_ARRAY, int kohalik_START, int kirje_COUNT, String märk_ametikoht) {
        if (kirje_COUNT != märk_ametikoht.length()) return false; for (int Loop_INDEX = 0; Loop_INDEX < kirje_COUNT; Loop_INDEX++) if (andmed_ARRAY[kohalik_START + Loop_INDEX] != märk_ametikoht.charAt(Loop_INDEX)) return false; return true;
    }
    static void 넣기(int bait_andmed) {
        if (쓴수 >= 명령해석기.luba_VALUE_eb540501.length) { if (!laiendus_tõrge) VIGA("변수를 펼친 명령이 너무 깁니다"); laiendus_tõrge = true; return; }
        명령해석기.luba_VALUE_eb540501[쓴수++] = bait_andmed;
    }
    static void 변수(int[] andmed_ARRAY, int START_ametikoht, int kirje_COUNT) {
        if (vahemik_SMS(andmed_ARRAY, START_ametikoht, kirje_COUNT, "PWD")) { 넣기('/'); for (int Loop_INDEX = 0; Loop_INDEX < Mälu_Failid.현재길이; Loop_INDEX++) 넣기(Mälu_Failid.tähtaja_piires_kaup[Loop_INDEX]); return; }
        if (vahemik_SMS(andmed_ARRAY, START_ametikoht, kirje_COUNT, "HOME")) { 넣기('/'); return; }
        if (vahemik_SMS(andmed_ARRAY, START_ametikoht, kirje_COUNT, "?")) {
            int andmed_VALUE = Olek_VALUE, number_2b3a32b5 = 100; boolean 시작여부 = false;
            while (number_2b3a32b5 > 0) { int 뒷값 = andmed_VALUE / number_2b3a32b5; if (뒷값 != 0 || 시작여부 || number_2b3a32b5 == 1) { 넣기('0' + 뒷값); 시작여부 = true; } andmed_VALUE %= number_2b3a32b5; number_2b3a32b5 /= 10; } return;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] == kirje_COUNT) {
            boolean MATCH = true; for (int sisemine_ametikoht = 0; sisemine_ametikoht < kirje_COUNT; sisemine_ametikoht++) if (변수이름[Loop_INDEX * 32 + sisemine_ametikoht] != andmed_ARRAY[START_ametikoht + sisemine_ametikoht]) MATCH = false;
            if (MATCH) { for (int sisemine_ametikoht = 0; sisemine_ametikoht < 값길이[Loop_INDEX]; sisemine_ametikoht++) 넣기(변수값[Loop_INDEX * 256 + sisemine_ametikoht]); return; }
        }
    }
    static boolean Word_VALUE(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = Käivita_2[중첩깊이 * 128 + 낱말번호], lõpeta_kõne_ametikoht = 끝[중첩깊이 * 128 + 낱말번호], BASE_ametikoht = 중첩깊이 * 4096, Tsitaat = 0;
        if (읽는자리 < lõpeta_kõne_ametikoht && ALLIKAS[BASE_ametikoht + 읽는자리] == '~' && (읽는자리 + 1 == lõpeta_kõne_ametikoht || ALLIKAS[BASE_ametikoht + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < lõpeta_kõne_ametikoht) {
            int koodipunkt = ALLIKAS[BASE_ametikoht + 읽는자리++];
            if (koodipunkt == Tsitaat) { Tsitaat = 0; continue; }
            if (Tsitaat == 0 && (koodipunkt == 39 || koodipunkt == 34)) { Tsitaat = koodipunkt; continue; }
            if (koodipunkt == '\\' && Tsitaat != 39) { int Edasi_ametikoht = ALLIKAS[BASE_ametikoht + 읽는자리++]; if (Tsitaat == 34 && Edasi_ametikoht != '$' && Edasi_ametikoht != '"' && Edasi_ametikoht != '\\') 넣기('\\'); 넣기(Edasi_ametikoht); continue; }
            if (koodipunkt == '$' && Tsitaat != 39 && 읽는자리 < lõpeta_kõne_ametikoht) {
                boolean 중괄호자리 = ALLIKAS[BASE_ametikoht + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < lõpeta_kõne_ametikoht && ALLIKAS[BASE_ametikoht + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < lõpeta_kõne_ametikoht && 이름뒤(ALLIKAS[BASE_ametikoht + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == lõpeta_kõne_ametikoht || ALLIKAS[BASE_ametikoht + 읽는자리] != '}')) { VIGA("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                변수(ALLIKAS, BASE_ametikoht + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(koodipunkt);
        }
        return !laiendus_tõrge;
    }
    static int 환경설정(int argument_INDEX, boolean eemaldama) {
        int kohalik_START = 명령해석기.시작점[argument_INDEX], lõpeta_kõne_ametikoht = kohalik_START + 명령해석기.길이[argument_INDEX], 같음자리 = kohalik_START;
        while (같음자리 < lõpeta_kõne_ametikoht && 명령해석기.luba_VALUE_eb540501[같음자리] != '=') 같음자리++;
        int kirje_COUNT = 같음자리 - kohalik_START;
        if (kirje_COUNT < 1 || kirje_COUNT > 31 || !nimetus_märk(명령해석기.luba_VALUE_eb540501[kohalik_START]) || !eemaldama && 같음자리 == lõpeta_kõne_ametikoht || lõpeta_kõne_ametikoht - 같음자리 - 1 > 255) return 2;
        for (int Loop_INDEX = kohalik_START; Loop_INDEX < 같음자리; Loop_INDEX++) if (!이름뒤(명령해석기.luba_VALUE_eb540501[Loop_INDEX])) return 2;
        if (vahemik_SMS(명령해석기.luba_VALUE_eb540501, kohalik_START, kirje_COUNT, "PWD") || vahemik_SMS(명령해석기.luba_VALUE_eb540501, kohalik_START, kirje_COUNT, "HOME")) return 2;
        int 찾은여부 = -1, 빈여부 = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] == 0) 빈여부 = Loop_INDEX;
            if (이름길이[Loop_INDEX] != kirje_COUNT) continue;
            boolean MATCH = true; for (int sisemine_ametikoht = 0; sisemine_ametikoht < kirje_COUNT; sisemine_ametikoht++) if (변수이름[Loop_INDEX * 32 + sisemine_ametikoht] != 명령해석기.luba_VALUE_eb540501[kohalik_START + sisemine_ametikoht]) MATCH = false;
            if (MATCH) 찾은여부 = Loop_INDEX;
        }
        if (eemaldama) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = 빈여부; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = kirje_COUNT; 값길이[찾은여부] = lõpeta_kõne_ametikoht - 같음자리 - 1;
        for (int Loop_INDEX = 0; Loop_INDEX < kirje_COUNT; Loop_INDEX++) 변수이름[찾은여부 * 32 + Loop_INDEX] = 명령해석기.luba_VALUE_eb540501[kohalik_START + Loop_INDEX];
        for (int Loop_INDEX = 같음자리 + 1; Loop_INDEX < lõpeta_kõne_ametikoht; Loop_INDEX++) 변수값[찾은여부 * 256 + Loop_INDEX - 같음자리 - 1] = 명령해석기.luba_VALUE_eb540501[Loop_INDEX];
        return 0;
    }
    static void 환경보기() {
        단말.Kirjutamine("HOME=/\nPWD="); Mälu_Failid.tähtaja_piires_kirjutamine(); 단말.문자(10);
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] > 0) {
            for (int sisemine_ametikoht = 0; sisemine_ametikoht < 이름길이[Loop_INDEX]; sisemine_ametikoht++) Tahvel.직렬쓰기(변수이름[Loop_INDEX * 32 + sisemine_ametikoht]); 단말.문자('=');
            for (int sisemine_ametikoht = 0; sisemine_ametikoht < 값길이[Loop_INDEX]; sisemine_ametikoht++) Tahvel.직렬쓰기(변수값[Loop_INDEX * 256 + sisemine_ametikoht]); 단말.문자(10);
        }
    }
    static void Täida_käsk(int[] andmed_ARRAY, int 시작변위, int kirje_COUNT, int 중첩깊이) {
        if (중첩깊이 >= 4 || kirje_COUNT > 4096) { VIGA("Käsk 파일의 pesastus_VALUE 또는 Joon 길이 제한을 넘었습니다"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < kirje_COUNT; Loop_INDEX++) ALLIKAS[중첩깊이 * 4096 + Loop_INDEX] = andmed_ARRAY[시작변위 + Loop_INDEX];
        int kokku_COUNT = Lugemine(kirje_COUNT, 중첩깊이); if (kokku_COUNT < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < kokku_COUNT) {
            int Rühm_lõpeta_kõne = 읽는자리;
            while (Rühm_lõpeta_kõne < kokku_COUNT && (종류[중첩깊이 * 128 + Rühm_lõpeta_kõne] == 0 || 종류[중첩깊이 * 128 + Rühm_lõpeta_kõne] >= 4)) Rühm_lõpeta_kõne++;
            boolean Täida = 조건성립 == 1 || 조건성립 == 2 && Olek_VALUE == 0 || 조건성립 == 3 && Olek_VALUE != 0;
            if (Täida) {
                boolean 이전자리 = false;
                while (읽는자리 < Rühm_lõpeta_kõne) {
                    int Edasi_ametikoht = 읽는자리; while (Edasi_ametikoht < Rühm_lõpeta_kõne && 종류[중첩깊이 * 128 + Edasi_ametikoht] != 4) Edasi_ametikoht++;
                    boolean Ühenda_voog = Edasi_ametikoht < Rühm_lõpeta_kõne; int 입력쪽 = -1, toodang_leht = -1, 출력방식 = 0;
                    명령해석기.luba_COUNT = 0; 쓴수 = 0; laiendus_tõrge = false;
                    for (int Loop_INDEX = 읽는자리; Loop_INDEX < Edasi_ametikoht; Loop_INDEX++) {
                        int 자료종류 = 종류[중첩깊이 * 128 + Loop_INDEX];
                        if (자료종류 >= 5) { if (자료종류 == 7) { if (입력쪽 >= 0) { VIGA("입력 전환이 겹쳤습니다"); return; } 입력쪽 = ++Loop_INDEX; } else { if (toodang_leht >= 0) { VIGA("Väljund 전환이 겹쳤습니다"); return; } toodang_leht = ++Loop_INDEX; 출력방식 = 자료종류; } continue; }
                        if (명령해석기.luba_COUNT == 32) { VIGA("인수가 너무 많습니다"); return; }
                        int argument_INDEX = 명령해석기.luba_COUNT++; 명령해석기.시작점[argument_INDEX] = 쓴수;
                        if (!Word_VALUE(Loop_INDEX, 중첩깊이)) return;
                        명령해석기.길이[argument_INDEX] = 쓴수 - 명령해석기.시작점[argument_INDEX];
                    }
                    연결중 = 이전자리 || Ühenda_voog || 입력쪽 >= 0 || toodang_leht >= 0;
                    if (연결중 && (명령해석기.같음(0, "vi") || 명령해석기.같음(0, "edit") || 명령해석기.같음(0, "load") || 명령해석기.같음(0, "gui") || 명령해석기.같음(0, "terminal") || 명령해석기.같음(0, "sh") || 명령해석기.같음(0, "source"))) { VIGA("대화형 명령과 Käsk 파일은 I_O 전환이나 voog_VALUE 연결에 쓸 number 없습니다"); return; }
                    셸입출력.Käivita_2(이전자리, Ühenda_voog);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int kirje_ametikoht = 입출력바꿈 == 0 ? 입력쪽 : toodang_leht; if (kirje_ametikoht < 0) continue;
                        int START_ametikoht = 쓴수; if (!Word_VALUE(kirje_ametikoht, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = Mälu_Failid.tee_START(쓴수 - START_ametikoht);
                        for (int sisemine_ametikoht = START_ametikoht; 처리값 >= 0 && sisemine_ametikoht < 쓴수; sisemine_ametikoht++) 처리값 = Mälu_Failid.tee_bait(sisemine_ametikoht - START_ametikoht, 명령해석기.luba_VALUE_eb540501[sisemine_ametikoht]);
                        if (처리값 >= 0) 처리값 = Mälu_Failid.Ava(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); 명령해석기.VIGA(처리값); Olek_VALUE = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.sisendfail = 처리값; else 셸입출력.väljundfail = 처리값;
                    }
                    셸입출력.대화허용 = 중첩깊이 == 0 && 읽는자리 == 0 && Edasi_ametikoht == kokku_COUNT;
                    깊이 = 중첩깊이; 명령해석기.TULEMUS = 0; Tahvel.입출력전환(1);
                    명령해석기.Käsk();
                    Tahvel.terminal(3);
                    int 반환값 = 명령해석기.TULEMUS, voog_tõrge = 셸입출력.tõrge_VALUE;
                    셸입출력.끝(); 연결중 = false;
                    Olek_VALUE = voog_tõrge < 0 ? 1 : 반환값;
                    if (voog_tõrge < 0) { 명령해석기.VIGA(voog_tõrge); return; }
                    if (skript_lõpeta_kõne || 반환값 == -1005) return;
                    이전자리 = true; 읽는자리 = Edasi_ametikoht + 1;
                }
            }
            if (Rühm_lõpeta_kõne < kokku_COUNT) 조건성립 = 종류[중첩깊이 * 128 + Rühm_lõpeta_kõne];
            읽는자리 = Rühm_lõpeta_kõne + 1;
        }
    }
    static void Täida_Fail() {
        if (명령해석기.luba_COUNT != 2 || 깊이 >= 3) { 명령해석기.TULEMUS = 2; 단말.Kirjutamine("사용법: sh Fail (pesastus_VALUE 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = 명령해석기.RADA(1); if (처리값 >= 0) 처리값 = Mälu_Failid.Ava(0);
        if (처리값 < 0) { 명령해석기.VIGA(처리값); return; }
        int kirje_COUNT = 0, bait_andmed;
        while ((bait_andmed = Mälu_Failid.Lugemine(처리값)) != 256 && bait_andmed >= 0 && kirje_COUNT < 16384) skript_VALUE[중첩깊이 * 16384 + kirje_COUNT++] = bait_andmed;
        Mälu_Failid.Suletud(처리값); Tahvel.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < kirje_COUNT && !skript_lõpeta_kõne;) {
            int lõpeta_kõne_ametikoht = 읽는자리; while (lõpeta_kõne_ametikoht < kirje_COUNT && skript_VALUE[중첩깊이 * 16384 + lõpeta_kõne_ametikoht] != 10) lõpeta_kõne_ametikoht++;
            int 유효길이 = lõpeta_kõne_ametikoht - 읽는자리; if (유효길이 > 0 && skript_VALUE[중첩깊이 * 16384 + lõpeta_kõne_ametikoht - 1] == 13) 유효길이--;
            Täida_käsk(skript_VALUE, 중첩깊이 * 16384 + 읽는자리, 유효길이, 중첩깊이); 읽는자리 = lõpeta_kõne_ametikoht + 1;
        }
        명령해석기.TULEMUS = Olek_VALUE; skript_lõpeta_kõne = false; 깊이 = 중첩깊이 - 1;
    }
}
