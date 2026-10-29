// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 interaktiv Shell 문법. 파이프는 순차 ausféieren_Befeel, 환경은 같은 셸에서 공유한다. */
public final class Shell_Syntax {
    static int[] Quell = new int[4 * 4096], 종류 = new int[4 * 128], Laf = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] 변수이름 = new int[16 * 32], 변수값 = new int[16 * 256], 이름길이 = new int[16], VALUE_Längt = new int[16];
    static int[] Skript_VALUE = new int[4 * 16384];
    static int Status_VALUE, 깊이, 쓴수;
    static boolean 연결중, Skript_bëennegen, Extensioun_Feeler;
    static boolean Numm_Zeechen(int Zeechecode) { return Zeechecode >= 'a' && Zeechecode <= 'z' || Zeechecode >= 'A' && Zeechecode <= 'Z' || Zeechecode == '_' || Zeechecode >= 128; }
    static boolean 이름뒤(int Zeechecode) { return Numm_Zeechen(Zeechecode) || Zeechecode >= '0' && Zeechecode <= '9'; }
    static void Feeler(String SMS) { Board.입출력전환(0); 단말.schreiwen("Befeel analyséieren_VALUE: "); 단말.schreiwen(SMS); 단말.문자(10); Status_VALUE = 2; }
    static int 읽기(int Agab_COUNT, int 중첩깊이) {
        int 현재자리 = 0, 총수 = 0, BASE_positionéieren = 중첩깊이 * 4096, speziellt_Zeechen = 중첩깊이 * 128;
        while (현재자리 < Agab_COUNT) {
            while (현재자리 < Agab_COUNT && (Quell[BASE_positionéieren + 현재자리] == 32 || Quell[BASE_positionéieren + 현재자리] == 9)) 현재자리++;
            if (현재자리 == Agab_COUNT || Quell[BASE_positionéieren + 현재자리] == '#') break;
            if (총수 == 128) { Feeler("낱말이 너무 많습니다"); return -1; }
            int Start_positionéieren = 현재자리, Zeechecode = Quell[BASE_positionéieren + 현재자리], 자료종류 = 0;
            if (Zeechecode == ';') { 자료종류 = 1; 현재자리++; }
            else if (Zeechecode == '&') { if (현재자리 + 1 >= Agab_COUNT || Quell[BASE_positionéieren + 현재자리 + 1] != '&') { Feeler("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } 자료종류 = 2; 현재자리 += 2; }
            else if (Zeechecode == '|') { 현재자리++; 자료종류 = 현재자리 < Agab_COUNT && Quell[BASE_positionéieren + 현재자리] == '|' ? 3 : 4; if (자료종류 == 3) 현재자리++; }
            else if (Zeechecode == '>') { 현재자리++; 자료종류 = 현재자리 < Agab_COUNT && Quell[BASE_positionéieren + 현재자리] == '>' ? 6 : 5; if (자료종류 == 6) 현재자리++; }
            else if (Zeechecode == '<') { 자료종류 = 7; 현재자리++; }
            else {
                int Zitat = 0;
                while (현재자리 < Agab_COUNT) {
                    Zeechecode = Quell[BASE_positionéieren + 현재자리];
                    if (Zeechecode == '`' && Zitat != 39 || Zeechecode == '$' && Zitat != 39 && 현재자리 + 1 < Agab_COUNT && Quell[BASE_positionéieren + 현재자리 + 1] == '(') { Feeler("Befeel Mooss 치환은 지원하지 않습니다"); return -1; }
                    if (Zeechecode == '\\' && Zitat != 39) { if (++현재자리 == Agab_COUNT) { Feeler("Zeil 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } 현재자리++; continue; }
                    if (Zeechecode == Zitat) { Zitat = 0; 현재자리++; continue; }
                    if (Zitat == 0 && (Zeechecode == 39 || Zeechecode == 34)) { Zitat = Zeechecode; 현재자리++; continue; }
                    if (Zitat == 0 && (Zeechecode == 32 || Zeechecode == 9 || Zeechecode == ';' || Zeechecode == '&' || Zeechecode == '|' || Zeechecode == '<' || Zeechecode == '>')) break;
                    현재자리++;
                }
                if (Zitat != 0) { Feeler("따옴표가 닫히지 않았습니다"); return -1; }
                if (현재자리 < Agab_COUNT && (Quell[BASE_positionéieren + 현재자리] == '>' || Quell[BASE_positionéieren + 현재자리] == '<')) {
                    boolean 수치 = 현재자리 > Start_positionéieren;
                    for (int Loop_INDEX = Start_positionéieren; Loop_INDEX < 현재자리; Loop_INDEX++) if (Quell[BASE_positionéieren + Loop_INDEX] < '0' || Quell[BASE_positionéieren + Loop_INDEX] > '9') 수치 = false;
                    if (수치) { Feeler("번호를 지정한 Fichier 서술자 I_O 전환은 지원하지 않습니다"); return -1; }
                }
            }
            종류[speziellt_Zeechen + 총수] = 자료종류; Laf[speziellt_Zeechen + 총수] = Start_positionéieren; 끝[speziellt_Zeechen + 총수] = 현재자리; 총수++;
        }
        boolean 낱말 = false;
        for (int Loop_INDEX = 0; Loop_INDEX < 총수; Loop_INDEX++) {
            int 임시값 = 종류[speziellt_Zeechen + Loop_INDEX];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++Loop_INDEX == 총수 || 종류[speziellt_Zeechen + Loop_INDEX] != 0) { Feeler("I_O 전환에 Fichier 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || Loop_INDEX == 총수 - 1 && 임시값 != 1) { Feeler("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (총수 > 0 && !낱말 && 종류[speziellt_Zeechen + 총수 - 1] != 1) { Feeler("명령이 빠졌습니다"); return -1; }
        return 총수;
    }
    static boolean 구간말(int[] Daten_ARRAY, int lokal_Start, int Agab_COUNT, String Zeechen_positionéieren) {
        if (Agab_COUNT != Zeechen_positionéieren.length()) return false; for (int Loop_INDEX = 0; Loop_INDEX < Agab_COUNT; Loop_INDEX++) if (Daten_ARRAY[lokal_Start + Loop_INDEX] != Zeechen_positionéieren.charAt(Loop_INDEX)) return false; return true;
    }
    static void 넣기(int Byte_Daten) {
        if (쓴수 >= 명령해석기.Token_VALUE.length) { if (!Extensioun_Feeler) Feeler("변수를 펼친 명령이 너무 깁니다"); Extensioun_Feeler = true; return; }
        명령해석기.Token_VALUE[쓴수++] = Byte_Daten;
    }
    static void 변수(int[] Daten_ARRAY, int Start_positionéieren, int Agab_COUNT) {
        if (구간말(Daten_ARRAY, Start_positionéieren, Agab_COUNT, "PWD")) { 넣기('/'); for (int Loop_INDEX = 0; Loop_INDEX < Späicher_Fichieren.현재길이; Loop_INDEX++) 넣기(Späicher_Fichieren.현재[Loop_INDEX]); return; }
        if (구간말(Daten_ARRAY, Start_positionéieren, Agab_COUNT, "HOME")) { 넣기('/'); return; }
        if (구간말(Daten_ARRAY, Start_positionéieren, Agab_COUNT, "?")) {
            int Daten_VALUE = Status_VALUE, Ziffer = 100; boolean 시작여부 = false;
            while (Ziffer > 0) { int 뒷값 = Daten_VALUE / Ziffer; if (뒷값 != 0 || 시작여부 || Ziffer == 1) { 넣기('0' + 뒷값); 시작여부 = true; } Daten_VALUE %= Ziffer; Ziffer /= 10; } return;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] == Agab_COUNT) {
            boolean MATCH = true; for (int intern_Verknëppung_positionéieren = 0; intern_Verknëppung_positionéieren < Agab_COUNT; intern_Verknëppung_positionéieren++) if (변수이름[Loop_INDEX * 32 + intern_Verknëppung_positionéieren] != Daten_ARRAY[Start_positionéieren + intern_Verknëppung_positionéieren]) MATCH = false;
            if (MATCH) { for (int intern_Verknëppung_positionéieren = 0; intern_Verknëppung_positionéieren < VALUE_Längt[Loop_INDEX]; intern_Verknëppung_positionéieren++) 넣기(변수값[Loop_INDEX * 256 + intern_Verknëppung_positionéieren]); return; }
        }
    }
    static boolean Word_VALUE(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = Laf[중첩깊이 * 128 + 낱말번호], bëennegen_positionéieren = 끝[중첩깊이 * 128 + 낱말번호], BASE_positionéieren = 중첩깊이 * 4096, Zitat = 0;
        if (읽는자리 < bëennegen_positionéieren && Quell[BASE_positionéieren + 읽는자리] == '~' && (읽는자리 + 1 == bëennegen_positionéieren || Quell[BASE_positionéieren + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < bëennegen_positionéieren) {
            int Zeechecode = Quell[BASE_positionéieren + 읽는자리++];
            if (Zeechecode == Zitat) { Zitat = 0; continue; }
            if (Zitat == 0 && (Zeechecode == 39 || Zeechecode == 34)) { Zitat = Zeechecode; continue; }
            if (Zeechecode == '\\' && Zitat != 39) { int Weider_positionéieren = Quell[BASE_positionéieren + 읽는자리++]; if (Zitat == 34 && Weider_positionéieren != '$' && Weider_positionéieren != '"' && Weider_positionéieren != '\\') 넣기('\\'); 넣기(Weider_positionéieren); continue; }
            if (Zeechecode == '$' && Zitat != 39 && 읽는자리 < bëennegen_positionéieren) {
                boolean 중괄호자리 = Quell[BASE_positionéieren + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < bëennegen_positionéieren && Quell[BASE_positionéieren + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < bëennegen_positionéieren && 이름뒤(Quell[BASE_positionéieren + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == bëennegen_positionéieren || Quell[BASE_positionéieren + 읽는자리] != '}')) { Feeler("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                변수(Quell, BASE_positionéieren + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(Zeechecode);
        }
        return !Extensioun_Feeler;
    }
    static int 환경설정(int Argument_INDEX, boolean ewechhuelen) {
        int lokal_Start = 명령해석기.시작점[Argument_INDEX], bëennegen_positionéieren = lokal_Start + 명령해석기.Längt_VALUE[Argument_INDEX], 같음자리 = lokal_Start;
        while (같음자리 < bëennegen_positionéieren && 명령해석기.Token_VALUE[같음자리] != '=') 같음자리++;
        int Agab_COUNT = 같음자리 - lokal_Start;
        if (Agab_COUNT < 1 || Agab_COUNT > 31 || !Numm_Zeechen(명령해석기.Token_VALUE[lokal_Start]) || !ewechhuelen && 같음자리 == bëennegen_positionéieren || bëennegen_positionéieren - 같음자리 - 1 > 255) return 2;
        for (int Loop_INDEX = lokal_Start; Loop_INDEX < 같음자리; Loop_INDEX++) if (!이름뒤(명령해석기.Token_VALUE[Loop_INDEX])) return 2;
        if (구간말(명령해석기.Token_VALUE, lokal_Start, Agab_COUNT, "PWD") || 구간말(명령해석기.Token_VALUE, lokal_Start, Agab_COUNT, "HOME")) return 2;
        int 찾은여부 = -1, 빈여부 = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] == 0) 빈여부 = Loop_INDEX;
            if (이름길이[Loop_INDEX] != Agab_COUNT) continue;
            boolean MATCH = true; for (int intern_Verknëppung_positionéieren = 0; intern_Verknëppung_positionéieren < Agab_COUNT; intern_Verknëppung_positionéieren++) if (변수이름[Loop_INDEX * 32 + intern_Verknëppung_positionéieren] != 명령해석기.Token_VALUE[lokal_Start + intern_Verknëppung_positionéieren]) MATCH = false;
            if (MATCH) 찾은여부 = Loop_INDEX;
        }
        if (ewechhuelen) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = 빈여부; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = Agab_COUNT; VALUE_Längt[찾은여부] = bëennegen_positionéieren - 같음자리 - 1;
        for (int Loop_INDEX = 0; Loop_INDEX < Agab_COUNT; Loop_INDEX++) 변수이름[찾은여부 * 32 + Loop_INDEX] = 명령해석기.Token_VALUE[lokal_Start + Loop_INDEX];
        for (int Loop_INDEX = 같음자리 + 1; Loop_INDEX < bëennegen_positionéieren; Loop_INDEX++) 변수값[찾은여부 * 256 + Loop_INDEX - 같음자리 - 1] = 명령해석기.Token_VALUE[Loop_INDEX];
        return 0;
    }
    static void 환경보기() {
        단말.schreiwen("HOME=/\nPWD="); Späicher_Fichieren.현재쓰기(); 단말.문자(10);
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] > 0) {
            for (int intern_Verknëppung_positionéieren = 0; intern_Verknëppung_positionéieren < 이름길이[Loop_INDEX]; intern_Verknëppung_positionéieren++) Board.직렬쓰기(변수이름[Loop_INDEX * 32 + intern_Verknëppung_positionéieren]); 단말.문자('=');
            for (int intern_Verknëppung_positionéieren = 0; intern_Verknëppung_positionéieren < VALUE_Längt[Loop_INDEX]; intern_Verknëppung_positionéieren++) Board.직렬쓰기(변수값[Loop_INDEX * 256 + intern_Verknëppung_positionéieren]); 단말.문자(10);
        }
    }
    static void ausféieren_Befeel(int[] Daten_ARRAY, int 시작변위, int Agab_COUNT, int 중첩깊이) {
        if (중첩깊이 >= 4 || Agab_COUNT > 4096) { Feeler("Befeel 파일의 중첩 또는 Zeil Längt_VALUE 제한을 넘었습니다"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Agab_COUNT; Loop_INDEX++) Quell[중첩깊이 * 4096 + Loop_INDEX] = Daten_ARRAY[시작변위 + Loop_INDEX];
        int 총수 = 읽기(Agab_COUNT, 중첩깊이); if (총수 < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < 총수) {
            int Grupp_bëennegen = 읽는자리;
            while (Grupp_bëennegen < 총수 && (종류[중첩깊이 * 128 + Grupp_bëennegen] == 0 || 종류[중첩깊이 * 128 + Grupp_bëennegen] >= 4)) Grupp_bëennegen++;
            boolean ausféieren = 조건성립 == 1 || 조건성립 == 2 && Status_VALUE == 0 || 조건성립 == 3 && Status_VALUE != 0;
            if (ausféieren) {
                boolean 이전자리 = false;
                while (읽는자리 < Grupp_bëennegen) {
                    int Weider_positionéieren = 읽는자리; while (Weider_positionéieren < Grupp_bëennegen && 종류[중첩깊이 * 128 + Weider_positionéieren] != 4) Weider_positionéieren++;
                    boolean Verbannen_Stream = Weider_positionéieren < Grupp_bëennegen; int 입력쪽 = -1, 출력쪽 = -1, 출력방식 = 0;
                    명령해석기.Token_COUNT = 0; 쓴수 = 0; Extensioun_Feeler = false;
                    for (int Loop_INDEX = 읽는자리; Loop_INDEX < Weider_positionéieren; Loop_INDEX++) {
                        int 자료종류 = 종류[중첩깊이 * 128 + Loop_INDEX];
                        if (자료종류 >= 5) { if (자료종류 == 7) { if (입력쪽 >= 0) { Feeler("입력 전환이 겹쳤습니다"); return; } 입력쪽 = ++Loop_INDEX; } else { if (출력쪽 >= 0) { Feeler("출력 전환이 겹쳤습니다"); return; } 출력쪽 = ++Loop_INDEX; 출력방식 = 자료종류; } continue; }
                        if (명령해석기.Token_COUNT == 32) { Feeler("인수가 너무 많습니다"); return; }
                        int Argument_INDEX = 명령해석기.Token_COUNT++; 명령해석기.시작점[Argument_INDEX] = 쓴수;
                        if (!Word_VALUE(Loop_INDEX, 중첩깊이)) return;
                        명령해석기.Längt_VALUE[Argument_INDEX] = 쓴수 - 명령해석기.시작점[Argument_INDEX];
                    }
                    연결중 = 이전자리 || Verbannen_Stream || 입력쪽 >= 0 || 출력쪽 >= 0;
                    if (연결중 && (명령해석기.같음(0, "vi") || 명령해석기.같음(0, "edit") || 명령해석기.같음(0, "load") || 명령해석기.같음(0, "gui") || 명령해석기.같음(0, "terminal") || 명령해석기.같음(0, "sh") || 명령해석기.같음(0, "source"))) { Feeler("interaktiv 명령과 Befeel 파일은 I_O 전환이나 Stream_VALUE 연결에 쓸 수 없습니다"); return; }
                    셸입출력.Laf(이전자리, Verbannen_Stream);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int Agab_positionéieren = 입출력바꿈 == 0 ? 입력쪽 : 출력쪽; if (Agab_positionéieren < 0) continue;
                        int Start_positionéieren = 쓴수; if (!Word_VALUE(Agab_positionéieren, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = Späicher_Fichieren.Wee_Start(쓴수 - Start_positionéieren);
                        for (int intern_Verknëppung_positionéieren = Start_positionéieren; 처리값 >= 0 && intern_Verknëppung_positionéieren < 쓴수; intern_Verknëppung_positionéieren++) 처리값 = Späicher_Fichieren.Wee_Byte(intern_Verknëppung_positionéieren - Start_positionéieren, 명령해석기.Token_VALUE[intern_Verknëppung_positionéieren]);
                        if (처리값 >= 0) 처리값 = Späicher_Fichieren.ariichten(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); 명령해석기.Feeler(처리값); Status_VALUE = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.입력파일 = 처리값; else 셸입출력.Ausgabsfichier = 처리값;
                    }
                    셸입출력.Erlaben_interaktiv = 중첩깊이 == 0 && 읽는자리 == 0 && Weider_positionéieren == 총수;
                    깊이 = 중첩깊이; 명령해석기.Mooss = 0; Board.입출력전환(1);
                    명령해석기.Befeel();
                    Board.Terminal(3);
                    int 반환값 = 명령해석기.Mooss, Stream_Feeler = 셸입출력.Feeler_VALUE;
                    셸입출력.끝(); 연결중 = false;
                    Status_VALUE = Stream_Feeler < 0 ? 1 : 반환값;
                    if (Stream_Feeler < 0) { 명령해석기.Feeler(Stream_Feeler); return; }
                    if (Skript_bëennegen || 반환값 == -1005) return;
                    이전자리 = true; 읽는자리 = Weider_positionéieren + 1;
                }
            }
            if (Grupp_bëennegen < 총수) 조건성립 = 종류[중첩깊이 * 128 + Grupp_bëennegen];
            읽는자리 = Grupp_bëennegen + 1;
        }
    }
    static void ausféieren_Fichier() {
        if (명령해석기.Token_COUNT != 2 || 깊이 >= 3) { 명령해석기.Mooss = 2; 단말.schreiwen("사용법: sh Fichier (중첩 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = 명령해석기.Wee(1); if (처리값 >= 0) 처리값 = Späicher_Fichieren.ariichten(0);
        if (처리값 < 0) { 명령해석기.Feeler(처리값); return; }
        int Agab_COUNT = 0, Byte_Daten;
        while ((Byte_Daten = Späicher_Fichieren.읽기(처리값)) != 256 && Byte_Daten >= 0 && Agab_COUNT < 16384) Skript_VALUE[중첩깊이 * 16384 + Agab_COUNT++] = Byte_Daten;
        Späicher_Fichieren.Clôture(처리값); Board.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < Agab_COUNT && !Skript_bëennegen;) {
            int bëennegen_positionéieren = 읽는자리; while (bëennegen_positionéieren < Agab_COUNT && Skript_VALUE[중첩깊이 * 16384 + bëennegen_positionéieren] != 10) bëennegen_positionéieren++;
            int 유효길이 = bëennegen_positionéieren - 읽는자리; if (유효길이 > 0 && Skript_VALUE[중첩깊이 * 16384 + bëennegen_positionéieren - 1] == 13) 유효길이--;
            ausféieren_Befeel(Skript_VALUE, 중첩깊이 * 16384 + 읽는자리, 유효길이, 중첩깊이); 읽는자리 = bëennegen_positionéieren + 1;
        }
        명령해석기.Mooss = Status_VALUE; Skript_bëennegen = false; 깊이 = 중첩깊이 - 1;
    }
}
