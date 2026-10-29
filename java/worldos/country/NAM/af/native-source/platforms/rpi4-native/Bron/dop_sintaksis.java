// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 interaktief dop 문법. 파이프는 순차 uitvoer_bevel, 환경은 같은 셸에서 공유한다. */
public final class dop_sintaksis {
    static int[] Bron = new int[4 * 4096], 종류 = new int[4 * 128], Loop = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] 변수이름 = new int[16 * 32], 변수값 = new int[16 * 256], 이름길이 = new int[16], VALUE_lengte = new int[16];
    static int[] skrip_VALUE = new int[4 * 16384];
    static int stand_VALUE, 깊이, 쓴수;
    static boolean 연결중, skrip_beëindig, uitbreiding_fout;
    static boolean naam_karakter(int karakterkode) { return karakterkode >= 'a' && karakterkode <= 'z' || karakterkode >= 'A' && karakterkode <= 'Z' || karakterkode == '_' || karakterkode >= 128; }
    static boolean 이름뒤(int karakterkode) { return naam_karakter(karakterkode) || karakterkode >= '0' && karakterkode <= '9'; }
    static void Fout(String Teks) { bord.입출력전환(0); 단말.Skryf("Opdrag ontleed_VALUE: "); 단말.Skryf(Teks); 단말.문자(10); stand_VALUE = 2; }
    static int Lees(int inskrywing_COUNT, int 중첩깊이) {
        int 현재자리 = 0, 총수 = 0, BASE_plaas = 중첩깊이 * 4096, spesiale_karakter = 중첩깊이 * 128;
        while (현재자리 < inskrywing_COUNT) {
            while (현재자리 < inskrywing_COUNT && (Bron[BASE_plaas + 현재자리] == 32 || Bron[BASE_plaas + 현재자리] == 9)) 현재자리++;
            if (현재자리 == inskrywing_COUNT || Bron[BASE_plaas + 현재자리] == '#') break;
            if (총수 == 128) { Fout("낱말이 너무 많습니다"); return -1; }
            int BEGIN_plaas = 현재자리, karakterkode = Bron[BASE_plaas + 현재자리], 자료종류 = 0;
            if (karakterkode == ';') { 자료종류 = 1; 현재자리++; }
            else if (karakterkode == '&') { if (현재자리 + 1 >= inskrywing_COUNT || Bron[BASE_plaas + 현재자리 + 1] != '&') { Fout("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } 자료종류 = 2; 현재자리 += 2; }
            else if (karakterkode == '|') { 현재자리++; 자료종류 = 현재자리 < inskrywing_COUNT && Bron[BASE_plaas + 현재자리] == '|' ? 3 : 4; if (자료종류 == 3) 현재자리++; }
            else if (karakterkode == '>') { 현재자리++; 자료종류 = 현재자리 < inskrywing_COUNT && Bron[BASE_plaas + 현재자리] == '>' ? 6 : 5; if (자료종류 == 6) 현재자리++; }
            else if (karakterkode == '<') { 자료종류 = 7; 현재자리++; }
            else {
                int Aanhaling = 0;
                while (현재자리 < inskrywing_COUNT) {
                    karakterkode = Bron[BASE_plaas + 현재자리];
                    if (karakterkode == '`' && Aanhaling != 39 || karakterkode == '$' && Aanhaling != 39 && 현재자리 + 1 < inskrywing_COUNT && Bron[BASE_plaas + 현재자리 + 1] == '(') { Fout("Opdrag maatreël 치환은 지원하지 않습니다"); return -1; }
                    if (karakterkode == '\\' && Aanhaling != 39) { if (++현재자리 == inskrywing_COUNT) { Fout("lyn 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } 현재자리++; continue; }
                    if (karakterkode == Aanhaling) { Aanhaling = 0; 현재자리++; continue; }
                    if (Aanhaling == 0 && (karakterkode == 39 || karakterkode == 34)) { Aanhaling = karakterkode; 현재자리++; continue; }
                    if (Aanhaling == 0 && (karakterkode == 32 || karakterkode == 9 || karakterkode == ';' || karakterkode == '&' || karakterkode == '|' || karakterkode == '<' || karakterkode == '>')) break;
                    현재자리++;
                }
                if (Aanhaling != 0) { Fout("따옴표가 닫히지 않았습니다"); return -1; }
                if (현재자리 < inskrywing_COUNT && (Bron[BASE_plaas + 현재자리] == '>' || Bron[BASE_plaas + 현재자리] == '<')) {
                    boolean 수치 = 현재자리 > BEGIN_plaas;
                    for (int lus_INDEX = BEGIN_plaas; lus_INDEX < 현재자리; lus_INDEX++) if (Bron[BASE_plaas + lus_INDEX] < '0' || Bron[BASE_plaas + lus_INDEX] > '9') 수치 = false;
                    if (수치) { Fout("번호를 지정한 Lêer 서술자 I_O 전환은 지원하지 않습니다"); return -1; }
                }
            }
            종류[spesiale_karakter + 총수] = 자료종류; Loop[spesiale_karakter + 총수] = BEGIN_plaas; 끝[spesiale_karakter + 총수] = 현재자리; 총수++;
        }
        boolean 낱말 = false;
        for (int lus_INDEX = 0; lus_INDEX < 총수; lus_INDEX++) {
            int 임시값 = 종류[spesiale_karakter + lus_INDEX];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++lus_INDEX == 총수 || 종류[spesiale_karakter + lus_INDEX] != 0) { Fout("I_O 전환에 Lêer 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || lus_INDEX == 총수 - 1 && 임시값 != 1) { Fout("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (총수 > 0 && !낱말 && 종류[spesiale_karakter + 총수 - 1] != 1) { Fout("명령이 빠졌습니다"); return -1; }
        return 총수;
    }
    static boolean 구간말(int[] data_ARRAY, int lokaal_BEGIN, int inskrywing_COUNT, String karakter_plaas) {
        if (inskrywing_COUNT != karakter_plaas.length()) return false; for (int lus_INDEX = 0; lus_INDEX < inskrywing_COUNT; lus_INDEX++) if (data_ARRAY[lokaal_BEGIN + lus_INDEX] != karakter_plaas.charAt(lus_INDEX)) return false; return true;
    }
    static void 넣기(int greep_data) {
        if (쓴수 >= 명령해석기.kenteken_VALUE.length) { if (!uitbreiding_fout) Fout("변수를 펼친 명령이 너무 깁니다"); uitbreiding_fout = true; return; }
        명령해석기.kenteken_VALUE[쓴수++] = greep_data;
    }
    static void 변수(int[] data_ARRAY, int BEGIN_plaas, int inskrywing_COUNT) {
        if (구간말(data_ARRAY, BEGIN_plaas, inskrywing_COUNT, "PWD")) { 넣기('/'); for (int lus_INDEX = 0; lus_INDEX < Geheue_Lêers.현재길이; lus_INDEX++) 넣기(Geheue_Lêers.현재[lus_INDEX]); return; }
        if (구간말(data_ARRAY, BEGIN_plaas, inskrywing_COUNT, "HOME")) { 넣기('/'); return; }
        if (구간말(data_ARRAY, BEGIN_plaas, inskrywing_COUNT, "?")) {
            int data_VALUE = stand_VALUE, syfer = 100; boolean 시작여부 = false;
            while (syfer > 0) { int 뒷값 = data_VALUE / syfer; if (뒷값 != 0 || 시작여부 || syfer == 1) { 넣기('0' + 뒷값); 시작여부 = true; } data_VALUE %= syfer; syfer /= 10; } return;
        }
        for (int lus_INDEX = 0; lus_INDEX < 16; lus_INDEX++) if (이름길이[lus_INDEX] == inskrywing_COUNT) {
            boolean MATCH = true; for (int binnebind_plaas = 0; binnebind_plaas < inskrywing_COUNT; binnebind_plaas++) if (변수이름[lus_INDEX * 32 + binnebind_plaas] != data_ARRAY[BEGIN_plaas + binnebind_plaas]) MATCH = false;
            if (MATCH) { for (int binnebind_plaas = 0; binnebind_plaas < VALUE_lengte[lus_INDEX]; binnebind_plaas++) 넣기(변수값[lus_INDEX * 256 + binnebind_plaas]); return; }
        }
    }
    static boolean Word_VALUE(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = Loop[중첩깊이 * 128 + 낱말번호], beëindig_plaas = 끝[중첩깊이 * 128 + 낱말번호], BASE_plaas = 중첩깊이 * 4096, Aanhaling = 0;
        if (읽는자리 < beëindig_plaas && Bron[BASE_plaas + 읽는자리] == '~' && (읽는자리 + 1 == beëindig_plaas || Bron[BASE_plaas + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < beëindig_plaas) {
            int karakterkode = Bron[BASE_plaas + 읽는자리++];
            if (karakterkode == Aanhaling) { Aanhaling = 0; continue; }
            if (Aanhaling == 0 && (karakterkode == 39 || karakterkode == 34)) { Aanhaling = karakterkode; continue; }
            if (karakterkode == '\\' && Aanhaling != 39) { int Volgende_plaas = Bron[BASE_plaas + 읽는자리++]; if (Aanhaling == 34 && Volgende_plaas != '$' && Volgende_plaas != '"' && Volgende_plaas != '\\') 넣기('\\'); 넣기(Volgende_plaas); continue; }
            if (karakterkode == '$' && Aanhaling != 39 && 읽는자리 < beëindig_plaas) {
                boolean 중괄호자리 = Bron[BASE_plaas + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < beëindig_plaas && Bron[BASE_plaas + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < beëindig_plaas && 이름뒤(Bron[BASE_plaas + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == beëindig_plaas || Bron[BASE_plaas + 읽는자리] != '}')) { Fout("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                변수(Bron, BASE_plaas + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(karakterkode);
        }
        return !uitbreiding_fout;
    }
    static int 환경설정(int argument_INDEX, boolean verwyder) {
        int lokaal_BEGIN = 명령해석기.시작점[argument_INDEX], beëindig_plaas = lokaal_BEGIN + 명령해석기.lengte_VALUE[argument_INDEX], 같음자리 = lokaal_BEGIN;
        while (같음자리 < beëindig_plaas && 명령해석기.kenteken_VALUE[같음자리] != '=') 같음자리++;
        int inskrywing_COUNT = 같음자리 - lokaal_BEGIN;
        if (inskrywing_COUNT < 1 || inskrywing_COUNT > 31 || !naam_karakter(명령해석기.kenteken_VALUE[lokaal_BEGIN]) || !verwyder && 같음자리 == beëindig_plaas || beëindig_plaas - 같음자리 - 1 > 255) return 2;
        for (int lus_INDEX = lokaal_BEGIN; lus_INDEX < 같음자리; lus_INDEX++) if (!이름뒤(명령해석기.kenteken_VALUE[lus_INDEX])) return 2;
        if (구간말(명령해석기.kenteken_VALUE, lokaal_BEGIN, inskrywing_COUNT, "PWD") || 구간말(명령해석기.kenteken_VALUE, lokaal_BEGIN, inskrywing_COUNT, "HOME")) return 2;
        int 찾은여부 = -1, 빈여부 = -1;
        for (int lus_INDEX = 0; lus_INDEX < 16; lus_INDEX++) {
            if (이름길이[lus_INDEX] == 0) 빈여부 = lus_INDEX;
            if (이름길이[lus_INDEX] != inskrywing_COUNT) continue;
            boolean MATCH = true; for (int binnebind_plaas = 0; binnebind_plaas < inskrywing_COUNT; binnebind_plaas++) if (변수이름[lus_INDEX * 32 + binnebind_plaas] != 명령해석기.kenteken_VALUE[lokaal_BEGIN + binnebind_plaas]) MATCH = false;
            if (MATCH) 찾은여부 = lus_INDEX;
        }
        if (verwyder) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = 빈여부; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = inskrywing_COUNT; VALUE_lengte[찾은여부] = beëindig_plaas - 같음자리 - 1;
        for (int lus_INDEX = 0; lus_INDEX < inskrywing_COUNT; lus_INDEX++) 변수이름[찾은여부 * 32 + lus_INDEX] = 명령해석기.kenteken_VALUE[lokaal_BEGIN + lus_INDEX];
        for (int lus_INDEX = 같음자리 + 1; lus_INDEX < beëindig_plaas; lus_INDEX++) 변수값[찾은여부 * 256 + lus_INDEX - 같음자리 - 1] = 명령해석기.kenteken_VALUE[lus_INDEX];
        return 0;
    }
    static void 환경보기() {
        단말.Skryf("HOME=/\nPWD="); Geheue_Lêers.현재쓰기(); 단말.문자(10);
        for (int lus_INDEX = 0; lus_INDEX < 16; lus_INDEX++) if (이름길이[lus_INDEX] > 0) {
            for (int binnebind_plaas = 0; binnebind_plaas < 이름길이[lus_INDEX]; binnebind_plaas++) bord.직렬쓰기(변수이름[lus_INDEX * 32 + binnebind_plaas]); 단말.문자('=');
            for (int binnebind_plaas = 0; binnebind_plaas < VALUE_lengte[lus_INDEX]; binnebind_plaas++) bord.직렬쓰기(변수값[lus_INDEX * 256 + binnebind_plaas]); 단말.문자(10);
        }
    }
    static void uitvoer_bevel(int[] data_ARRAY, int 시작변위, int inskrywing_COUNT, int 중첩깊이) {
        if (중첩깊이 >= 4 || inskrywing_COUNT > 4096) { Fout("Opdrag 파일의 nes_VALUE 또는 lyn lengte_VALUE 제한을 넘었습니다"); return; }
        for (int lus_INDEX = 0; lus_INDEX < inskrywing_COUNT; lus_INDEX++) Bron[중첩깊이 * 4096 + lus_INDEX] = data_ARRAY[시작변위 + lus_INDEX];
        int 총수 = Lees(inskrywing_COUNT, 중첩깊이); if (총수 < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < 총수) {
            int Groep_beëindig = 읽는자리;
            while (Groep_beëindig < 총수 && (종류[중첩깊이 * 128 + Groep_beëindig] == 0 || 종류[중첩깊이 * 128 + Groep_beëindig] >= 4)) Groep_beëindig++;
            boolean uitvoer = 조건성립 == 1 || 조건성립 == 2 && stand_VALUE == 0 || 조건성립 == 3 && stand_VALUE != 0;
            if (uitvoer) {
                boolean 이전자리 = false;
                while (읽는자리 < Groep_beëindig) {
                    int Volgende_plaas = 읽는자리; while (Volgende_plaas < Groep_beëindig && 종류[중첩깊이 * 128 + Volgende_plaas] != 4) Volgende_plaas++;
                    boolean KOPPEL_Stream = Volgende_plaas < Groep_beëindig; int 입력쪽 = -1, 출력쪽 = -1, 출력방식 = 0;
                    명령해석기.kenteken_COUNT = 0; 쓴수 = 0; uitbreiding_fout = false;
                    for (int lus_INDEX = 읽는자리; lus_INDEX < Volgende_plaas; lus_INDEX++) {
                        int 자료종류 = 종류[중첩깊이 * 128 + lus_INDEX];
                        if (자료종류 >= 5) { if (자료종류 == 7) { if (입력쪽 >= 0) { Fout("입력 전환이 겹쳤습니다"); return; } 입력쪽 = ++lus_INDEX; } else { if (출력쪽 >= 0) { Fout("Afvoer 전환이 겹쳤습니다"); return; } 출력쪽 = ++lus_INDEX; 출력방식 = 자료종류; } continue; }
                        if (명령해석기.kenteken_COUNT == 32) { Fout("인수가 너무 많습니다"); return; }
                        int argument_INDEX = 명령해석기.kenteken_COUNT++; 명령해석기.시작점[argument_INDEX] = 쓴수;
                        if (!Word_VALUE(lus_INDEX, 중첩깊이)) return;
                        명령해석기.lengte_VALUE[argument_INDEX] = 쓴수 - 명령해석기.시작점[argument_INDEX];
                    }
                    연결중 = 이전자리 || KOPPEL_Stream || 입력쪽 >= 0 || 출력쪽 >= 0;
                    if (연결중 && (명령해석기.같음(0, "vi") || 명령해석기.같음(0, "edit") || 명령해석기.같음(0, "load") || 명령해석기.같음(0, "gui") || 명령해석기.같음(0, "terminal") || 명령해석기.같음(0, "sh") || 명령해석기.같음(0, "source"))) { Fout("interaktief 명령과 Opdrag 파일은 I_O 전환이나 Stream_VALUE 연결에 쓸 수 없습니다"); return; }
                    셸입출력.Loop(이전자리, KOPPEL_Stream);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int inskrywing_plaas = 입출력바꿈 == 0 ? 입력쪽 : 출력쪽; if (inskrywing_plaas < 0) continue;
                        int BEGIN_plaas = 쓴수; if (!Word_VALUE(inskrywing_plaas, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = Geheue_Lêers.pad_BEGIN(쓴수 - BEGIN_plaas);
                        for (int binnebind_plaas = BEGIN_plaas; 처리값 >= 0 && binnebind_plaas < 쓴수; binnebind_plaas++) 처리값 = Geheue_Lêers.pad_greep(binnebind_plaas - BEGIN_plaas, 명령해석기.kenteken_VALUE[binnebind_plaas]);
                        if (처리값 >= 0) 처리값 = Geheue_Lêers.skep(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); 명령해석기.Fout(처리값); stand_VALUE = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.입력파일 = 처리값; else 셸입출력.afvoerlêer = 처리값;
                    }
                    셸입출력.toelaat_interaktief = 중첩깊이 == 0 && 읽는자리 == 0 && Volgende_plaas == 총수;
                    깊이 = 중첩깊이; 명령해석기.maatreël = 0; bord.입출력전환(1);
                    명령해석기.Opdrag();
                    bord.Terminaal(3);
                    int 반환값 = 명령해석기.maatreël, Stream_fout = 셸입출력.faling_VALUE;
                    셸입출력.끝(); 연결중 = false;
                    stand_VALUE = Stream_fout < 0 ? 1 : 반환값;
                    if (Stream_fout < 0) { 명령해석기.Fout(Stream_fout); return; }
                    if (skrip_beëindig || 반환값 == -1005) return;
                    이전자리 = true; 읽는자리 = Volgende_plaas + 1;
                }
            }
            if (Groep_beëindig < 총수) 조건성립 = 종류[중첩깊이 * 128 + Groep_beëindig];
            읽는자리 = Groep_beëindig + 1;
        }
    }
    static void uitvoer_lêer() {
        if (명령해석기.kenteken_COUNT != 2 || 깊이 >= 3) { 명령해석기.maatreël = 2; 단말.Skryf("사용법: sh Lêer (nes_VALUE 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = 명령해석기.Pad(1); if (처리값 >= 0) 처리값 = Geheue_Lêers.skep(0);
        if (처리값 < 0) { 명령해석기.Fout(처리값); return; }
        int inskrywing_COUNT = 0, greep_data;
        while ((greep_data = Geheue_Lêers.Lees(처리값)) != 256 && greep_data >= 0 && inskrywing_COUNT < 16384) skrip_VALUE[중첩깊이 * 16384 + inskrywing_COUNT++] = greep_data;
        Geheue_Lêers.Sluit(처리값); bord.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < inskrywing_COUNT && !skrip_beëindig;) {
            int beëindig_plaas = 읽는자리; while (beëindig_plaas < inskrywing_COUNT && skrip_VALUE[중첩깊이 * 16384 + beëindig_plaas] != 10) beëindig_plaas++;
            int 유효길이 = beëindig_plaas - 읽는자리; if (유효길이 > 0 && skrip_VALUE[중첩깊이 * 16384 + beëindig_plaas - 1] == 13) 유효길이--;
            uitvoer_bevel(skrip_VALUE, 중첩깊이 * 16384 + 읽는자리, 유효길이, 중첩깊이); 읽는자리 = beëindig_plaas + 1;
        }
        명령해석기.maatreël = stand_VALUE; skrip_beëindig = false; 깊이 = 중첩깊이 - 1;
    }
}
