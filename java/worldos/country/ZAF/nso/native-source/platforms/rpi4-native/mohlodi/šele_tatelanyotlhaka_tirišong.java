// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 ya_kgokagano šele 문법. 파이프는 순차 phethagatša_taelo, 환경은 같은 셸에서 공유한다. */
public final class šele_tatelanyotlhaka_tirišong {
    static int[] mohlodi = new int[4 * 4096], 종류 = new int[4 * 128], Diriša = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] 변수이름 = new int[16 * 32], 변수값 = new int[16 * 256], 이름길이 = new int[16], boleng_botelele = new int[16];
    static int[] skripte_boleng = new int[4 * 16384];
    static int boemo_boleng, 깊이, 쓴수;
    static boolean 연결중, skripte_fetša, koketšo_phošo;
    static boolean leina_tlhaka(int khouto_ya_tlhaka) { return khouto_ya_tlhaka >= 'a' && khouto_ya_tlhaka <= 'z' || khouto_ya_tlhaka >= 'A' && khouto_ya_tlhaka <= 'Z' || khouto_ya_tlhaka == '_' || khouto_ya_tlhaka >= 128; }
    static boolean 이름뒤(int khouto_ya_tlhaka) { return leina_tlhaka(khouto_ya_tlhaka) || khouto_ya_tlhaka >= '0' && khouto_ya_tlhaka <= '9'; }
    static void Phošo(String Sengwalwa) { 보드.입출력전환(0); 단말.Ngwala("Taelo ripaganya_boleng: "); 단말.Ngwala(Sengwalwa); 단말.문자(10); boemo_boleng = 2; }
    static int Bala(int 항목수, int 중첩깊이) {
        int 현재자리 = 0, 총수 = 0, 기준자리 = 중첩깊이 * 4096, tlhaka_ye_e_kgethegilego = 중첩깊이 * 128;
        while (현재자리 < 항목수) {
            while (현재자리 < 항목수 && (mohlodi[기준자리 + 현재자리] == 32 || mohlodi[기준자리 + 현재자리] == 9)) 현재자리++;
            if (현재자리 == 항목수 || mohlodi[기준자리 + 현재자리] == '#') break;
            if (총수 == 128) { Phošo("낱말이 너무 많습니다"); return -1; }
            int 시작자리 = 현재자리, khouto_ya_tlhaka = mohlodi[기준자리 + 현재자리], 자료종류 = 0;
            if (khouto_ya_tlhaka == ';') { 자료종류 = 1; 현재자리++; }
            else if (khouto_ya_tlhaka == '&') { if (현재자리 + 1 >= 항목수 || mohlodi[기준자리 + 현재자리 + 1] != '&') { Phošo("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } 자료종류 = 2; 현재자리 += 2; }
            else if (khouto_ya_tlhaka == '|') { 현재자리++; 자료종류 = 현재자리 < 항목수 && mohlodi[기준자리 + 현재자리] == '|' ? 3 : 4; if (자료종류 == 3) 현재자리++; }
            else if (khouto_ya_tlhaka == '>') { 현재자리++; 자료종류 = 현재자리 < 항목수 && mohlodi[기준자리 + 현재자리] == '>' ? 6 : 5; if (자료종류 == 6) 현재자리++; }
            else if (khouto_ya_tlhaka == '<') { 자료종류 = 7; 현재자리++; }
            else {
                int 따옴표 = 0;
                while (현재자리 < 항목수) {
                    khouto_ya_tlhaka = mohlodi[기준자리 + 현재자리];
                    if (khouto_ya_tlhaka == '`' && 따옴표 != 39 || khouto_ya_tlhaka == '$' && 따옴표 != 39 && 현재자리 + 1 < 항목수 && mohlodi[기준자리 + 현재자리 + 1] == '(') { Phošo("Taelo 결과 치환은 지원하지 않습니다"); return -1; }
                    if (khouto_ya_tlhaka == '\\' && 따옴표 != 39) { if (++현재자리 == 항목수) { Phošo("mothaladi 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } 현재자리++; continue; }
                    if (khouto_ya_tlhaka == 따옴표) { 따옴표 = 0; 현재자리++; continue; }
                    if (따옴표 == 0 && (khouto_ya_tlhaka == 39 || khouto_ya_tlhaka == 34)) { 따옴표 = khouto_ya_tlhaka; 현재자리++; continue; }
                    if (따옴표 == 0 && (khouto_ya_tlhaka == 32 || khouto_ya_tlhaka == 9 || khouto_ya_tlhaka == ';' || khouto_ya_tlhaka == '&' || khouto_ya_tlhaka == '|' || khouto_ya_tlhaka == '<' || khouto_ya_tlhaka == '>')) break;
                    현재자리++;
                }
                if (따옴표 != 0) { Phošo("따옴표가 닫히지 않았습니다"); return -1; }
                if (현재자리 < 항목수 && (mohlodi[기준자리 + 현재자리] == '>' || mohlodi[기준자리 + 현재자리] == '<')) {
                    boolean 수치 = 현재자리 > 시작자리;
                    for (int ditaelopoeletšwa_lokela = 시작자리; ditaelopoeletšwa_lokela < 현재자리; ditaelopoeletšwa_lokela++) if (mohlodi[기준자리 + ditaelopoeletšwa_lokela] < '0' || mohlodi[기준자리 + ditaelopoeletšwa_lokela] > '9') 수치 = false;
                    if (수치) { Phošo("번호를 지정한 Faele 서술자 I_O 전환은 지원하지 않습니다"); return -1; }
                }
            }
            종류[tlhaka_ye_e_kgethegilego + 총수] = 자료종류; Diriša[tlhaka_ye_e_kgethegilego + 총수] = 시작자리; 끝[tlhaka_ye_e_kgethegilego + 총수] = 현재자리; 총수++;
        }
        boolean 낱말 = false;
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 총수; ditaelopoeletšwa_lokela++) {
            int 임시값 = 종류[tlhaka_ye_e_kgethegilego + ditaelopoeletšwa_lokela];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++ditaelopoeletšwa_lokela == 총수 || 종류[tlhaka_ye_e_kgethegilego + ditaelopoeletšwa_lokela] != 0) { Phošo("I_O 전환에 Faele 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || ditaelopoeletšwa_lokela == 총수 - 1 && 임시값 != 1) { Phošo("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (총수 > 0 && !낱말 && 종류[tlhaka_ye_e_kgethegilego + 총수 - 1] != 1) { Phošo("명령이 빠졌습니다"); return -1; }
        return 총수;
    }
    static boolean 구간말(int[] data_arei, int kgauswi_Thomišo, int 항목수, String 문자위치) {
        if (항목수 != 문자위치.length()) return false; for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 항목수; ditaelopoeletšwa_lokela++) if (data_arei[kgauswi_Thomišo + ditaelopoeletšwa_lokela] != 문자위치.charAt(ditaelopoeletšwa_lokela)) return false; return true;
    }
    static void 넣기(int paete_data) {
        if (쓴수 >= 명령해석기.thokene_boleng.length) { if (!koketšo_phošo) Phošo("변수를 펼친 명령이 너무 깁니다"); koketšo_phošo = true; return; }
        명령해석기.thokene_boleng[쓴수++] = paete_data;
    }
    static void 변수(int[] data_arei, int 시작자리, int 항목수) {
        if (구간말(data_arei, 시작자리, 항목수, "PWD")) { 넣기('/'); for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < memori_Difaele.현재길이; ditaelopoeletšwa_lokela++) 넣기(memori_Difaele.현재[ditaelopoeletšwa_lokela]); return; }
        if (구간말(data_arei, 시작자리, 항목수, "HOME")) { 넣기('/'); return; }
        if (구간말(data_arei, 시작자리, 항목수, "?")) {
            int data_boleng = boemo_boleng, 자릿값 = 100; boolean 시작여부 = false;
            while (자릿값 > 0) { int 뒷값 = data_boleng / 자릿값; if (뒷값 != 0 || 시작여부 || 자릿값 == 1) { 넣기('0' + 뒷값); 시작여부 = true; } data_boleng %= 자릿값; 자릿값 /= 10; } return;
        }
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 16; ditaelopoeletšwa_lokela++) if (이름길이[ditaelopoeletšwa_lokela] == 항목수) {
            boolean 일치여부 = true; for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) if (변수이름[ditaelopoeletšwa_lokela * 32 + 안쪽자리] != data_arei[시작자리 + 안쪽자리]) 일치여부 = false;
            if (일치여부) { for (int 안쪽자리 = 0; 안쪽자리 < boleng_botelele[ditaelopoeletšwa_lokela]; 안쪽자리++) 넣기(변수값[ditaelopoeletšwa_lokela * 256 + 안쪽자리]); return; }
        }
    }
    static boolean Thalokontšu_boleng(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = Diriša[중첩깊이 * 128 + 낱말번호], 끝자리 = 끝[중첩깊이 * 128 + 낱말번호], 기준자리 = 중첩깊이 * 4096, 따옴표 = 0;
        if (읽는자리 < 끝자리 && mohlodi[기준자리 + 읽는자리] == '~' && (읽는자리 + 1 == 끝자리 || mohlodi[기준자리 + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < 끝자리) {
            int khouto_ya_tlhaka = mohlodi[기준자리 + 읽는자리++];
            if (khouto_ya_tlhaka == 따옴표) { 따옴표 = 0; continue; }
            if (따옴표 == 0 && (khouto_ya_tlhaka == 39 || khouto_ya_tlhaka == 34)) { 따옴표 = khouto_ya_tlhaka; continue; }
            if (khouto_ya_tlhaka == '\\' && 따옴표 != 39) { int 다음자리 = mohlodi[기준자리 + 읽는자리++]; if (따옴표 == 34 && 다음자리 != '$' && 다음자리 != '"' && 다음자리 != '\\') 넣기('\\'); 넣기(다음자리); continue; }
            if (khouto_ya_tlhaka == '$' && 따옴표 != 39 && 읽는자리 < 끝자리) {
                boolean 중괄호자리 = mohlodi[기준자리 + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < 끝자리 && mohlodi[기준자리 + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < 끝자리 && 이름뒤(mohlodi[기준자리 + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == 끝자리 || mohlodi[기준자리 + 읽는자리] != '}')) { Phošo("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                변수(mohlodi, 기준자리 + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(khouto_ya_tlhaka);
        }
        return !koketšo_phošo;
    }
    static int 환경설정(int akumente_lokela, boolean tloša) {
        int kgauswi_Thomišo = 명령해석기.시작점[akumente_lokela], 끝자리 = kgauswi_Thomišo + 명령해석기.botelele_boleng[akumente_lokela], 같음자리 = kgauswi_Thomišo;
        while (같음자리 < 끝자리 && 명령해석기.thokene_boleng[같음자리] != '=') 같음자리++;
        int 항목수 = 같음자리 - kgauswi_Thomišo;
        if (항목수 < 1 || 항목수 > 31 || !leina_tlhaka(명령해석기.thokene_boleng[kgauswi_Thomišo]) || !tloša && 같음자리 == 끝자리 || 끝자리 - 같음자리 - 1 > 255) return 2;
        for (int ditaelopoeletšwa_lokela = kgauswi_Thomišo; ditaelopoeletšwa_lokela < 같음자리; ditaelopoeletšwa_lokela++) if (!이름뒤(명령해석기.thokene_boleng[ditaelopoeletšwa_lokela])) return 2;
        if (구간말(명령해석기.thokene_boleng, kgauswi_Thomišo, 항목수, "PWD") || 구간말(명령해석기.thokene_boleng, kgauswi_Thomišo, 항목수, "HOME")) return 2;
        int 찾은여부 = -1, 빈여부 = -1;
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 16; ditaelopoeletšwa_lokela++) {
            if (이름길이[ditaelopoeletšwa_lokela] == 0) 빈여부 = ditaelopoeletšwa_lokela;
            if (이름길이[ditaelopoeletšwa_lokela] != 항목수) continue;
            boolean 일치여부 = true; for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) if (변수이름[ditaelopoeletšwa_lokela * 32 + 안쪽자리] != 명령해석기.thokene_boleng[kgauswi_Thomišo + 안쪽자리]) 일치여부 = false;
            if (일치여부) 찾은여부 = ditaelopoeletšwa_lokela;
        }
        if (tloša) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = 빈여부; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = 항목수; boleng_botelele[찾은여부] = 끝자리 - 같음자리 - 1;
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 항목수; ditaelopoeletšwa_lokela++) 변수이름[찾은여부 * 32 + ditaelopoeletšwa_lokela] = 명령해석기.thokene_boleng[kgauswi_Thomišo + ditaelopoeletšwa_lokela];
        for (int ditaelopoeletšwa_lokela = 같음자리 + 1; ditaelopoeletšwa_lokela < 끝자리; ditaelopoeletšwa_lokela++) 변수값[찾은여부 * 256 + ditaelopoeletšwa_lokela - 같음자리 - 1] = 명령해석기.thokene_boleng[ditaelopoeletšwa_lokela];
        return 0;
    }
    static void 환경보기() {
        단말.Ngwala("HOME=/\nPWD="); memori_Difaele.현재쓰기(); 단말.문자(10);
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 16; ditaelopoeletšwa_lokela++) if (이름길이[ditaelopoeletšwa_lokela] > 0) {
            for (int 안쪽자리 = 0; 안쪽자리 < 이름길이[ditaelopoeletšwa_lokela]; 안쪽자리++) 보드.직렬쓰기(변수이름[ditaelopoeletšwa_lokela * 32 + 안쪽자리]); 단말.문자('=');
            for (int 안쪽자리 = 0; 안쪽자리 < boleng_botelele[ditaelopoeletšwa_lokela]; 안쪽자리++) 보드.직렬쓰기(변수값[ditaelopoeletšwa_lokela * 256 + 안쪽자리]); 단말.문자(10);
        }
    }
    static void phethagatša_taelo(int[] data_arei, int 시작변위, int 항목수, int 중첩깊이) {
        if (중첩깊이 >= 4 || 항목수 > 4096) { Phošo("Taelo 파일의 중첩 또는 mothaladi botelele_boleng 제한을 넘었습니다"); return; }
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 항목수; ditaelopoeletšwa_lokela++) mohlodi[중첩깊이 * 4096 + ditaelopoeletšwa_lokela] = data_arei[시작변위 + ditaelopoeletšwa_lokela];
        int 총수 = Bala(항목수, 중첩깊이); if (총수 < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < 총수) {
            int sehlopha_fetša = 읽는자리;
            while (sehlopha_fetša < 총수 && (종류[중첩깊이 * 128 + sehlopha_fetša] == 0 || 종류[중첩깊이 * 128 + sehlopha_fetša] >= 4)) sehlopha_fetša++;
            boolean phethagatša = 조건성립 == 1 || 조건성립 == 2 && boemo_boleng == 0 || 조건성립 == 3 && boemo_boleng != 0;
            if (phethagatša) {
                boolean 이전자리 = false;
                while (읽는자리 < sehlopha_fetša) {
                    int 다음자리 = 읽는자리; while (다음자리 < sehlopha_fetša && 종류[중첩깊이 * 128 + 다음자리] != 4) 다음자리++;
                    boolean KGOKAGANYA_Stream = 다음자리 < sehlopha_fetša; int 입력쪽 = -1, 출력쪽 = -1, 출력방식 = 0;
                    명령해석기.토큰수 = 0; 쓴수 = 0; koketšo_phošo = false;
                    for (int ditaelopoeletšwa_lokela = 읽는자리; ditaelopoeletšwa_lokela < 다음자리; ditaelopoeletšwa_lokela++) {
                        int 자료종류 = 종류[중첩깊이 * 128 + ditaelopoeletšwa_lokela];
                        if (자료종류 >= 5) { if (자료종류 == 7) { if (입력쪽 >= 0) { Phošo("입력 전환이 겹쳤습니다"); return; } 입력쪽 = ++ditaelopoeletšwa_lokela; } else { if (출력쪽 >= 0) { Phošo("출력 전환이 겹쳤습니다"); return; } 출력쪽 = ++ditaelopoeletšwa_lokela; 출력방식 = 자료종류; } continue; }
                        if (명령해석기.토큰수 == 32) { Phošo("인수가 너무 많습니다"); return; }
                        int akumente_lokela = 명령해석기.토큰수++; 명령해석기.시작점[akumente_lokela] = 쓴수;
                        if (!Thalokontšu_boleng(ditaelopoeletšwa_lokela, 중첩깊이)) return;
                        명령해석기.botelele_boleng[akumente_lokela] = 쓴수 - 명령해석기.시작점[akumente_lokela];
                    }
                    연결중 = 이전자리 || KGOKAGANYA_Stream || 입력쪽 >= 0 || 출력쪽 >= 0;
                    if (연결중 && (명령해석기.같음(0, "vi") || 명령해석기.같음(0, "edit") || 명령해석기.같음(0, "load") || 명령해석기.같음(0, "gui") || 명령해석기.같음(0, "terminal") || 명령해석기.같음(0, "sh") || 명령해석기.같음(0, "source"))) { Phošo("ya_kgokagano 명령과 Taelo 파일은 I_O 전환이나 Stream_boleng 연결에 쓸 수 없습니다"); return; }
                    셸입출력.Diriša(이전자리, KGOKAGANYA_Stream);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int 항목자리 = 입출력바꿈 == 0 ? 입력쪽 : 출력쪽; if (항목자리 < 0) continue;
                        int 시작자리 = 쓴수; if (!Thalokontšu_boleng(항목자리, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = memori_Difaele.tsela_Thomišo(쓴수 - 시작자리);
                        for (int 안쪽자리 = 시작자리; 처리값 >= 0 && 안쪽자리 < 쓴수; 안쪽자리++) 처리값 = memori_Difaele.tsela_paete(안쪽자리 - 시작자리, 명령해석기.thokene_boleng[안쪽자리]);
                        if (처리값 >= 0) 처리값 = memori_Difaele.Bula(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); 명령해석기.Phošo(처리값); boemo_boleng = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.입력파일 = 처리값; else 셸입출력.faele_ya_tšweletšo = 처리값;
                    }
                    셸입출력.Dumelela_ya_kgokagano = 중첩깊이 == 0 && 읽는자리 == 0 && 다음자리 == 총수;
                    깊이 = 중첩깊이; 명령해석기.결과 = 0; 보드.입출력전환(1);
                    명령해석기.Taelo();
                    보드.터미널(3);
                    int 반환값 = 명령해석기.결과, Stream_phošo = 셸입출력.go_palelwa_boleng;
                    셸입출력.끝(); 연결중 = false;
                    boemo_boleng = Stream_phošo < 0 ? 1 : 반환값;
                    if (Stream_phošo < 0) { 명령해석기.Phošo(Stream_phošo); return; }
                    if (skripte_fetša || 반환값 == -1005) return;
                    이전자리 = true; 읽는자리 = 다음자리 + 1;
                }
            }
            if (sehlopha_fetša < 총수) 조건성립 = 종류[중첩깊이 * 128 + sehlopha_fetša];
            읽는자리 = sehlopha_fetša + 1;
        }
    }
    static void phethagatša_faele() {
        if (명령해석기.토큰수 != 2 || 깊이 >= 3) { 명령해석기.결과 = 2; 단말.Ngwala("사용법: sh Faele (중첩 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = 명령해석기.Tsejana(1); if (처리값 >= 0) 처리값 = memori_Difaele.Bula(0);
        if (처리값 < 0) { 명령해석기.Phošo(처리값); return; }
        int 항목수 = 0, paete_data;
        while ((paete_data = memori_Difaele.Bala(처리값)) != 256 && paete_data >= 0 && 항목수 < 16384) skripte_boleng[중첩깊이 * 16384 + 항목수++] = paete_data;
        memori_Difaele.Tswalela(처리값); 보드.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < 항목수 && !skripte_fetša;) {
            int 끝자리 = 읽는자리; while (끝자리 < 항목수 && skripte_boleng[중첩깊이 * 16384 + 끝자리] != 10) 끝자리++;
            int 유효길이 = 끝자리 - 읽는자리; if (유효길이 > 0 && skripte_boleng[중첩깊이 * 16384 + 끝자리 - 1] == 13) 유효길이--;
            phethagatša_taelo(skripte_boleng, 중첩깊이 * 16384 + 읽는자리, 유효길이, 중첩깊이); 읽는자리 = 끝자리 + 1;
        }
        명령해석기.결과 = boemo_boleng; skripte_fetša = false; 깊이 = 중첩깊이 - 1;
    }
}
