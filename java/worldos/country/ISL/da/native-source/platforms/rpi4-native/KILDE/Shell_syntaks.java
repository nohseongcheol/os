// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 interaktiv Shell 문법. 파이프는 순차 Udfør_kommando, 환경은 같은 셸에서 공유한다. */
public final class Shell_syntaks {
    static int[] KILDE = new int[4 * 4096], 종류 = new int[4 * 128], Kør_2 = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] variabel_navn = new int[16 * 32], variabel_data = new int[16 * 256], 이름길이 = new int[16], VÆRDI_varighed = new int[16];
    static int[] script_VÆRDI = new int[4 * 16384];
    static int status_VÆRDI, 깊이, 쓴수;
    static boolean 연결중, script_afslutte_et_opkald, udvidelse_fejl;
    static boolean navn_tegn(int tegnkode) { return tegnkode >= 'a' && tegnkode <= 'z' || tegnkode >= 'A' && tegnkode <= 'Z' || tegnkode == '_' || tegnkode >= 128; }
    static boolean 이름뒤(int tegnkode) { return navn_tegn(tegnkode) || tegnkode >= '0' && tegnkode <= '9'; }
    static void fejl(String Tekst) { Tavle.입출력전환(0); 단말.Skrive("Kommando opdele_tekst_VÆRDI: "); 단말.Skrive(Tekst); 단말.문자(10); status_VÆRDI = 2; }
    static int Læse(int post_TÆL_8f7753a1, int 중첩깊이) {
        int aktuel_INDEKS = 0, i_alt_TÆL = 0, BASIS_placere = 중첩깊이 * 4096, specialtegn = 중첩깊이 * 128;
        while (aktuel_INDEKS < post_TÆL_8f7753a1) {
            while (aktuel_INDEKS < post_TÆL_8f7753a1 && (KILDE[BASIS_placere + aktuel_INDEKS] == 32 || KILDE[BASIS_placere + aktuel_INDEKS] == 9)) aktuel_INDEKS++;
            if (aktuel_INDEKS == post_TÆL_8f7753a1 || KILDE[BASIS_placere + aktuel_INDEKS] == '#') break;
            if (i_alt_TÆL == 128) { fejl("낱말이 너무 많습니다"); return -1; }
            int START_placere = aktuel_INDEKS, tegnkode = KILDE[BASIS_placere + aktuel_INDEKS], 자료종류 = 0;
            if (tegnkode == ';') { 자료종류 = 1; aktuel_INDEKS++; }
            else if (tegnkode == '&') { if (aktuel_INDEKS + 1 >= post_TÆL_8f7753a1 || KILDE[BASIS_placere + aktuel_INDEKS + 1] != '&') { fejl("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } 자료종류 = 2; aktuel_INDEKS += 2; }
            else if (tegnkode == '|') { aktuel_INDEKS++; 자료종류 = aktuel_INDEKS < post_TÆL_8f7753a1 && KILDE[BASIS_placere + aktuel_INDEKS] == '|' ? 3 : 4; if (자료종류 == 3) aktuel_INDEKS++; }
            else if (tegnkode == '>') { aktuel_INDEKS++; 자료종류 = aktuel_INDEKS < post_TÆL_8f7753a1 && KILDE[BASIS_placere + aktuel_INDEKS] == '>' ? 6 : 5; if (자료종류 == 6) aktuel_INDEKS++; }
            else if (tegnkode == '<') { 자료종류 = 7; aktuel_INDEKS++; }
            else {
                int Citat = 0;
                while (aktuel_INDEKS < post_TÆL_8f7753a1) {
                    tegnkode = KILDE[BASIS_placere + aktuel_INDEKS];
                    if (tegnkode == '`' && Citat != 39 || tegnkode == '$' && Citat != 39 && aktuel_INDEKS + 1 < post_TÆL_8f7753a1 && KILDE[BASIS_placere + aktuel_INDEKS + 1] == '(') { fejl("Kommando KR 치환은 지원하지 않습니다"); return -1; }
                    if (tegnkode == '\\' && Citat != 39) { if (++aktuel_INDEKS == post_TÆL_8f7753a1) { fejl("Linje 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } aktuel_INDEKS++; continue; }
                    if (tegnkode == Citat) { Citat = 0; aktuel_INDEKS++; continue; }
                    if (Citat == 0 && (tegnkode == 39 || tegnkode == 34)) { Citat = tegnkode; aktuel_INDEKS++; continue; }
                    if (Citat == 0 && (tegnkode == 32 || tegnkode == 9 || tegnkode == ';' || tegnkode == '&' || tegnkode == '|' || tegnkode == '<' || tegnkode == '>')) break;
                    aktuel_INDEKS++;
                }
                if (Citat != 0) { fejl("따옴표가 닫히지 않았습니다"); return -1; }
                if (aktuel_INDEKS < post_TÆL_8f7753a1 && (KILDE[BASIS_placere + aktuel_INDEKS] == '>' || KILDE[BASIS_placere + aktuel_INDEKS] == '<')) {
                    boolean 수치 = aktuel_INDEKS > START_placere;
                    for (int Loop_INDEKS = START_placere; Loop_INDEKS < aktuel_INDEKS; Loop_INDEKS++) if (KILDE[BASIS_placere + Loop_INDEKS] < '0' || KILDE[BASIS_placere + Loop_INDEKS] > '9') 수치 = false;
                    if (수치) { fejl("번호를 지정한 Fil 서술자 I_O 전환은 지원하지 않습니다"); return -1; }
                }
            }
            종류[specialtegn + i_alt_TÆL] = 자료종류; Kør_2[specialtegn + i_alt_TÆL] = START_placere; 끝[specialtegn + i_alt_TÆL] = aktuel_INDEKS; i_alt_TÆL++;
        }
        boolean 낱말 = false;
        for (int Loop_INDEKS = 0; Loop_INDEKS < i_alt_TÆL; Loop_INDEKS++) {
            int 임시값 = 종류[specialtegn + Loop_INDEKS];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++Loop_INDEKS == i_alt_TÆL || 종류[specialtegn + Loop_INDEKS] != 0) { fejl("I_O 전환에 Fil 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || Loop_INDEKS == i_alt_TÆL - 1 && 임시값 != 1) { fejl("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (i_alt_TÆL > 0 && !낱말 && 종류[specialtegn + i_alt_TÆL - 1] != 1) { fejl("명령이 빠졌습니다"); return -1; }
        return i_alt_TÆL;
    }
    static boolean område_sms(int[] data_MATRIX, int lokal_START, int post_TÆL_8f7753a1, String tegn_placere) {
        if (post_TÆL_8f7753a1 != tegn_placere.length()) return false; for (int Loop_INDEKS = 0; Loop_INDEKS < post_TÆL_8f7753a1; Loop_INDEKS++) if (data_MATRIX[lokal_START + Loop_INDEKS] != tegn_placere.charAt(Loop_INDEKS)) return false; return true;
    }
    static void 넣기(int byte_data) {
        if (쓴수 >= 명령해석기.token_VÆRDI.length) { if (!udvidelse_fejl) fejl("변수를 펼친 명령이 너무 깁니다"); udvidelse_fejl = true; return; }
        명령해석기.token_VÆRDI[쓴수++] = byte_data;
    }
    static void variabel_VÆRDI(int[] data_MATRIX, int START_placere, int post_TÆL_8f7753a1) {
        if (område_sms(data_MATRIX, START_placere, post_TÆL_8f7753a1, "PWD")) { 넣기('/'); for (int Loop_INDEKS = 0; Loop_INDEKS < Hukommelse_Filer.aktuel_varighed; Loop_INDEKS++) 넣기(Hukommelse_Filer.aktuel_vare[Loop_INDEKS]); return; }
        if (område_sms(data_MATRIX, START_placere, post_TÆL_8f7753a1, "HOME")) { 넣기('/'); return; }
        if (område_sms(data_MATRIX, START_placere, post_TÆL_8f7753a1, "?")) {
            int data_VÆRDI = status_VÆRDI, ciffer = 100; boolean 시작여부 = false;
            while (ciffer > 0) { int 뒷값 = data_VÆRDI / ciffer; if (뒷값 != 0 || 시작여부 || ciffer == 1) { 넣기('0' + 뒷값); 시작여부 = true; } data_VÆRDI %= ciffer; ciffer /= 10; } return;
        }
        for (int Loop_INDEKS = 0; Loop_INDEKS < 16; Loop_INDEKS++) if (이름길이[Loop_INDEKS] == post_TÆL_8f7753a1) {
            boolean SAMMENLIGN = true; for (int indre_placere = 0; indre_placere < post_TÆL_8f7753a1; indre_placere++) if (variabel_navn[Loop_INDEKS * 32 + indre_placere] != data_MATRIX[START_placere + indre_placere]) SAMMENLIGN = false;
            if (SAMMENLIGN) { for (int indre_placere = 0; indre_placere < VÆRDI_varighed[Loop_INDEKS]; indre_placere++) 넣기(variabel_data[Loop_INDEKS * 256 + indre_placere]); return; }
        }
    }
    static boolean Ord_VÆRDI(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = Kør_2[중첩깊이 * 128 + 낱말번호], afslutte_et_opkald_placere = 끝[중첩깊이 * 128 + 낱말번호], BASIS_placere = 중첩깊이 * 4096, Citat = 0;
        if (읽는자리 < afslutte_et_opkald_placere && KILDE[BASIS_placere + 읽는자리] == '~' && (읽는자리 + 1 == afslutte_et_opkald_placere || KILDE[BASIS_placere + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < afslutte_et_opkald_placere) {
            int tegnkode = KILDE[BASIS_placere + 읽는자리++];
            if (tegnkode == Citat) { Citat = 0; continue; }
            if (Citat == 0 && (tegnkode == 39 || tegnkode == 34)) { Citat = tegnkode; continue; }
            if (tegnkode == '\\' && Citat != 39) { int Næste_placere = KILDE[BASIS_placere + 읽는자리++]; if (Citat == 34 && Næste_placere != '$' && Næste_placere != '"' && Næste_placere != '\\') 넣기('\\'); 넣기(Næste_placere); continue; }
            if (tegnkode == '$' && Citat != 39 && 읽는자리 < afslutte_et_opkald_placere) {
                boolean 중괄호자리 = KILDE[BASIS_placere + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < afslutte_et_opkald_placere && KILDE[BASIS_placere + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < afslutte_et_opkald_placere && 이름뒤(KILDE[BASIS_placere + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == afslutte_et_opkald_placere || KILDE[BASIS_placere + 읽는자리] != '}')) { fejl("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                variabel_VÆRDI(KILDE, BASIS_placere + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(tegnkode);
        }
        return !udvidelse_fejl;
    }
    static int miljø_Indstillinger(int argument_INDEKS, boolean fjerne) {
        int lokal_START = 명령해석기.시작점[argument_INDEKS], afslutte_et_opkald_placere = lokal_START + 명령해석기.varighed_VÆRDI[argument_INDEKS], 같음자리 = lokal_START;
        while (같음자리 < afslutte_et_opkald_placere && 명령해석기.token_VÆRDI[같음자리] != '=') 같음자리++;
        int post_TÆL_8f7753a1 = 같음자리 - lokal_START;
        if (post_TÆL_8f7753a1 < 1 || post_TÆL_8f7753a1 > 31 || !navn_tegn(명령해석기.token_VÆRDI[lokal_START]) || !fjerne && 같음자리 == afslutte_et_opkald_placere || afslutte_et_opkald_placere - 같음자리 - 1 > 255) return 2;
        for (int Loop_INDEKS = lokal_START; Loop_INDEKS < 같음자리; Loop_INDEKS++) if (!이름뒤(명령해석기.token_VÆRDI[Loop_INDEKS])) return 2;
        if (område_sms(명령해석기.token_VÆRDI, lokal_START, post_TÆL_8f7753a1, "PWD") || område_sms(명령해석기.token_VÆRDI, lokal_START, post_TÆL_8f7753a1, "HOME")) return 2;
        int 찾은여부 = -1, 빈여부 = -1;
        for (int Loop_INDEKS = 0; Loop_INDEKS < 16; Loop_INDEKS++) {
            if (이름길이[Loop_INDEKS] == 0) 빈여부 = Loop_INDEKS;
            if (이름길이[Loop_INDEKS] != post_TÆL_8f7753a1) continue;
            boolean SAMMENLIGN = true; for (int indre_placere = 0; indre_placere < post_TÆL_8f7753a1; indre_placere++) if (variabel_navn[Loop_INDEKS * 32 + indre_placere] != 명령해석기.token_VÆRDI[lokal_START + indre_placere]) SAMMENLIGN = false;
            if (SAMMENLIGN) 찾은여부 = Loop_INDEKS;
        }
        if (fjerne) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = 빈여부; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = post_TÆL_8f7753a1; VÆRDI_varighed[찾은여부] = afslutte_et_opkald_placere - 같음자리 - 1;
        for (int Loop_INDEKS = 0; Loop_INDEKS < post_TÆL_8f7753a1; Loop_INDEKS++) variabel_navn[찾은여부 * 32 + Loop_INDEKS] = 명령해석기.token_VÆRDI[lokal_START + Loop_INDEKS];
        for (int Loop_INDEKS = 같음자리 + 1; Loop_INDEKS < afslutte_et_opkald_placere; Loop_INDEKS++) variabel_data[찾은여부 * 256 + Loop_INDEKS - 같음자리 - 1] = 명령해석기.token_VÆRDI[Loop_INDEKS];
        return 0;
    }
    static void vise_miljø() {
        단말.Skrive("HOME=/\nPWD="); Hukommelse_Filer.aktuel_skrive(); 단말.문자(10);
        for (int Loop_INDEKS = 0; Loop_INDEKS < 16; Loop_INDEKS++) if (이름길이[Loop_INDEKS] > 0) {
            for (int indre_placere = 0; indre_placere < 이름길이[Loop_INDEKS]; indre_placere++) Tavle.직렬쓰기(variabel_navn[Loop_INDEKS * 32 + indre_placere]); 단말.문자('=');
            for (int indre_placere = 0; indre_placere < VÆRDI_varighed[Loop_INDEKS]; indre_placere++) Tavle.직렬쓰기(variabel_data[Loop_INDEKS * 256 + indre_placere]); 단말.문자(10);
        }
    }
    static void Udfør_kommando(int[] data_MATRIX, int 시작변위, int post_TÆL_8f7753a1, int 중첩깊이) {
        if (중첩깊이 >= 4 || post_TÆL_8f7753a1 > 4096) { fejl("Kommando 파일의 indlejring_VÆRDI 또는 Linje varighed_VÆRDI 제한을 넘었습니다"); return; }
        for (int Loop_INDEKS = 0; Loop_INDEKS < post_TÆL_8f7753a1; Loop_INDEKS++) KILDE[중첩깊이 * 4096 + Loop_INDEKS] = data_MATRIX[시작변위 + Loop_INDEKS];
        int i_alt_TÆL = Læse(post_TÆL_8f7753a1, 중첩깊이); if (i_alt_TÆL < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < i_alt_TÆL) {
            int gruppe_afslutte_et_opkald = 읽는자리;
            while (gruppe_afslutte_et_opkald < i_alt_TÆL && (종류[중첩깊이 * 128 + gruppe_afslutte_et_opkald] == 0 || 종류[중첩깊이 * 128 + gruppe_afslutte_et_opkald] >= 4)) gruppe_afslutte_et_opkald++;
            boolean Udfør_cc685ae5 = 조건성립 == 1 || 조건성립 == 2 && status_VÆRDI == 0 || 조건성립 == 3 && status_VÆRDI != 0;
            if (Udfør_cc685ae5) {
                boolean Forrige_vare_INDEKS = false;
                while (읽는자리 < gruppe_afslutte_et_opkald) {
                    int Næste_placere = 읽는자리; while (Næste_placere < gruppe_afslutte_et_opkald && 종류[중첩깊이 * 128 + Næste_placere] != 4) Næste_placere++;
                    boolean Forbind_strøm = Næste_placere < gruppe_afslutte_et_opkald; int input_side = -1, produktoutput_side = -1, 출력방식 = 0;
                    명령해석기.token_TÆL = 0; 쓴수 = 0; udvidelse_fejl = false;
                    for (int Loop_INDEKS = 읽는자리; Loop_INDEKS < Næste_placere; Loop_INDEKS++) {
                        int 자료종류 = 종류[중첩깊이 * 128 + Loop_INDEKS];
                        if (자료종류 >= 5) { if (자료종류 == 7) { if (input_side >= 0) { fejl("input_VÆRDI 전환이 겹쳤습니다"); return; } input_side = ++Loop_INDEKS; } else { if (produktoutput_side >= 0) { fejl("Udgang 전환이 겹쳤습니다"); return; } produktoutput_side = ++Loop_INDEKS; 출력방식 = 자료종류; } continue; }
                        if (명령해석기.token_TÆL == 32) { fejl("인수가 너무 많습니다"); return; }
                        int argument_INDEKS = 명령해석기.token_TÆL++; 명령해석기.시작점[argument_INDEKS] = 쓴수;
                        if (!Ord_VÆRDI(Loop_INDEKS, 중첩깊이)) return;
                        명령해석기.varighed_VÆRDI[argument_INDEKS] = 쓴수 - 명령해석기.시작점[argument_INDEKS];
                    }
                    연결중 = Forrige_vare_INDEKS || Forbind_strøm || input_side >= 0 || produktoutput_side >= 0;
                    if (연결중 && (명령해석기.같음(0, "vi") || 명령해석기.같음(0, "edit") || 명령해석기.같음(0, "load") || 명령해석기.같음(0, "gui") || 명령해석기.같음(0, "terminal") || 명령해석기.같음(0, "sh") || 명령해석기.같음(0, "source"))) { fejl("interaktiv 명령과 Kommando 파일은 I_O 전환이나 strøm_VÆRDI 연결에 쓸 tal 없습니다"); return; }
                    셸입출력.Kør_2(Forrige_vare_INDEKS, Forbind_strøm);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int post_placere_206f1c6d = 입출력바꿈 == 0 ? input_side : produktoutput_side; if (post_placere_206f1c6d < 0) continue;
                        int START_placere = 쓴수; if (!Ord_VÆRDI(post_placere_206f1c6d, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = Hukommelse_Filer.sti_START(쓴수 - START_placere);
                        for (int indre_placere = START_placere; 처리값 >= 0 && indre_placere < 쓴수; indre_placere++) 처리값 = Hukommelse_Filer.sti_byte(indre_placere - START_placere, 명령해석기.token_VÆRDI[indre_placere]);
                        if (처리값 >= 0) 처리값 = Hukommelse_Filer.Åbn(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); 명령해석기.fejl(처리값); status_VÆRDI = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.inputfil = 처리값; else 셸입출력.outputfil = 처리값;
                    }
                    셸입출력.Tillad_interaktiv = 중첩깊이 == 0 && 읽는자리 == 0 && Næste_placere == i_alt_TÆL;
                    깊이 = 중첩깊이; 명령해석기.KR = 0; Tavle.입출력전환(1);
                    명령해석기.Kommando();
                    Tavle.Terminal(3);
                    int 반환값 = 명령해석기.KR, strøm_fejl = 셸입출력.fejl_VÆRDI;
                    셸입출력.끝(); 연결중 = false;
                    status_VÆRDI = strøm_fejl < 0 ? 1 : 반환값;
                    if (strøm_fejl < 0) { 명령해석기.fejl(strøm_fejl); return; }
                    if (script_afslutte_et_opkald || 반환값 == -1005) return;
                    Forrige_vare_INDEKS = true; 읽는자리 = Næste_placere + 1;
                }
            }
            if (gruppe_afslutte_et_opkald < i_alt_TÆL) 조건성립 = 종류[중첩깊이 * 128 + gruppe_afslutte_et_opkald];
            읽는자리 = gruppe_afslutte_et_opkald + 1;
        }
    }
    static void Udfør_fil() {
        if (명령해석기.token_TÆL != 2 || 깊이 >= 3) { 명령해석기.KR = 2; 단말.Skrive("사용법: sh Fil (indlejring_VÆRDI 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = 명령해석기.Sti(1); if (처리값 >= 0) 처리값 = Hukommelse_Filer.Åbn(0);
        if (처리값 < 0) { 명령해석기.fejl(처리값); return; }
        int post_TÆL_8f7753a1 = 0, byte_data;
        while ((byte_data = Hukommelse_Filer.Læse(처리값)) != 256 && byte_data >= 0 && post_TÆL_8f7753a1 < 16384) script_VÆRDI[중첩깊이 * 16384 + post_TÆL_8f7753a1++] = byte_data;
        Hukommelse_Filer.Luk(처리값); Tavle.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < post_TÆL_8f7753a1 && !script_afslutte_et_opkald;) {
            int afslutte_et_opkald_placere = 읽는자리; while (afslutte_et_opkald_placere < post_TÆL_8f7753a1 && script_VÆRDI[중첩깊이 * 16384 + afslutte_et_opkald_placere] != 10) afslutte_et_opkald_placere++;
            int gyldig_varighed = afslutte_et_opkald_placere - 읽는자리; if (gyldig_varighed > 0 && script_VÆRDI[중첩깊이 * 16384 + afslutte_et_opkald_placere - 1] == 13) gyldig_varighed--;
            Udfør_kommando(script_VÆRDI, 중첩깊이 * 16384 + 읽는자리, gyldig_varighed, 중첩깊이); 읽는자리 = afslutte_et_opkald_placere + 1;
        }
        명령해석기.KR = status_VÆRDI; script_afslutte_et_opkald = false; 깊이 = 중첩깊이 - 1;
    }
}
