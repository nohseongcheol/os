// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java mohlodi_mohlare -> 표준 버전 49 class 컴파일러. */
public final class 자바컴파일러 {
    static int[] mohlodi = new int[16384], 출력 = new int[16384], 코드 = new int[4096];
    static int[] 토큰종류 = new int[2048], 토큰위치 = new int[2048], thokene_botelele = new int[2048];
    static int[] ya_go_se_fetoge_boleng = new int[4096], ya_go_se_fetoge_E_Šetšego = new int[512];
    static int[] 문자 = new int[512], faele_leina_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int mohlodi_bogolo, 토큰수, 위치, 코드크기, ya_go_se_fetoge_bogolo, 상수수 = 1, 출력크기, tlhaka_botelele;
    static boolean Phošo;
    static int legoro_thokene, legoro_ya_go_se_fetoge, 부모상수, 코드상수;
    static int[] mokgwa_go_tsenya_tshedimošo_leina = new int[32], 함수반환 = new int[32], 함수인수수 = new int[32];
    static int[] mokgwa_akumente_leina = new int[512], mokgwa_akumente_thaepa = new int[512];
    static int[] 함수본문 = new int[32], mokgwa_fetša = new int[32], 함수코드 = new int[32];
    static int[] mokgwa_botelele = new int[32], 함수지역 = new int[32], mokgwa_leina_ya_go_se_fetoge = new int[32], 함수서술 = new int[32];
    static int[] mokgwa_fihlelela = new int[32];
    static int 함수수, 현재함수, 지역수, 깊이, 식깊이;
    static int[] kgauswi_leina = new int[128], kgauswi_thaepa = new int[128], 지역깊이 = new int[128];

    static void go_palelwa_boleng(String 이유) {
        if (!Phošo) {
            mošomiši.Ngwala("javac error: "); mošomiši.Ngwala(이유);
            mošomiši.Ngwala(" at line ");
            int mothaladi = 1, 끝 = 위치 < 토큰수 ? 토큰위치[위치] : mohlodi_bogolo;
            for (int 수 = 0; 수 < 끝; 수++) if (mohlodi[수] == 10) mothaladi++;
            자바도구.수쓰기(mothaladi); mošomiši.ngwala_tlhaka_boleng(10);
        }
        Phošo = true;
    }
    static boolean tlhaka_boleng(int boleng) { return 문자이름규칙.첫글자(boleng); }
    static boolean 숫자(int boleng) { return boleng >= '0' && boleng <= '9'; }
    static boolean 이름같음(int 가, int 나) {
        if (가 < 0 || 나 < 0 || 가 >= 토큰수 || 나 >= 토큰수 || thokene_botelele[가] != thokene_botelele[나]) return false;
        for (int 수 = 0; 수 < thokene_botelele[가]; 수++) if (mohlodi[토큰위치[가] + 수] != mohlodi[토큰위치[나] + 수]) return false;
        return true;
    }
    static boolean Thalokontšu_boleng(int thokene_boleng, String Thalokontšu_SMS) {
        if (thokene_boleng < 0 || thokene_boleng >= 토큰수 || thokene_botelele[thokene_boleng] != Thalokontšu_SMS.length()) return false;
        for (int 수 = 0; 수 < Thalokontšu_SMS.length(); 수++) if (mohlodi[토큰위치[thokene_boleng] + 수] != Thalokontšu_SMS.charAt(수)) return false;
        return true;
    }
    static int 종류() { return 위치 < 토큰수 ? 토큰종류[위치] : 0; }
    static boolean 받기(int boleng) { if (종류() != boleng) return false; 위치++; return true; }
    static void 요구(int boleng) { if (!받기(boleng)) go_palelwa_boleng("unexpected token"); }
    static boolean 말받기(String Thalokontšu_SMS) { if (!Thalokontšu_boleng(위치, Thalokontšu_SMS)) return false; 위치++; return true; }
    static void 말요구(String Thalokontšu_SMS) { if (!말받기(Thalokontšu_SMS)) go_palelwa_boleng(Thalokontšu_SMS); }
    static int sešupi_boleng() {
        int 결과 = 위치;
        if (종류() != 256) go_palelwa_boleng("identifier required"); else 위치++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int Diriša = 0;
        for (int 수 = 0; 수 <= 예약어.length(); 수++) {
            if (수 == 예약어.length() || 예약어.charAt(수) == ' ') {
                boolean 같음 = 수 - Diriša == thokene_botelele[결과];
                for (int sekgobana_go_tsenya_tshedimošo = Diriša; 같음 && sekgobana_go_tsenya_tshedimošo < 수; sekgobana_go_tsenya_tshedimošo++) if (예약어.charAt(sekgobana_go_tsenya_tshedimošo) != mohlodi[토큰위치[결과] + sekgobana_go_tsenya_tshedimošo - Diriša]) 같음 = false;
                if (같음) go_palelwa_boleng("reserved word cannot be an identifier");
                Diriša = 수 + 1;
            }
        }
        return 결과;
    }
    static void sega_boleng() {
        int 수 = 0;
        while (수 < mohlodi_bogolo && !Phošo) {
            int boleng = mohlodi[수], Diriša = 수, 종류 = boleng;
            if (boleng == 32 || boleng == 9 || boleng == 10 || boleng == 13) { 수++; continue; }
            if (boleng == '/' && 수 + 1 < mohlodi_bogolo && mohlodi[수 + 1] == '/') {
                while (수 < mohlodi_bogolo && mohlodi[수] != 10) 수++;
                continue;
            }
            if (boleng == '/' && 수 + 1 < mohlodi_bogolo && mohlodi[수 + 1] == '*') {
                수 += 2;
                while (수 + 1 < mohlodi_bogolo && !(mohlodi[수] == '*' && mohlodi[수 + 1] == '/')) 수++;
                if (수 + 1 >= mohlodi_bogolo) { go_palelwa_boleng("unterminated comment"); break; }
                수 += 2; continue;
            }
            if (tlhaka_boleng(boleng)) { 종류 = 256; while (수 < mohlodi_bogolo && 문자이름규칙.이어진글자(mohlodi[수])) 수++; }
            else if (숫자(boleng)) { 종류 = 257; while (수 < mohlodi_bogolo && 숫자(mohlodi[수])) 수++; }
            else if (boleng == '"' || boleng == '\'') {
                종류 = boleng == '"' ? 258 : 259; 수++;
                while (수 < mohlodi_bogolo && mohlodi[수] != boleng && mohlodi[수] != 10 && mohlodi[수] != 13) {
                    if (mohlodi[수] == '\\') 수++;
                    수++;
                }
                if (수 >= mohlodi_bogolo || mohlodi[수] != boleng) { go_palelwa_boleng("unterminated literal"); break; }
                수++;
            } else {
                수++;
                if (수 < mohlodi_bogolo) {
                    int 다음 = mohlodi[수];
                    if (boleng == '=' && 다음 == '=') 종류 = 300;
                    if (boleng == '!' && 다음 == '=') 종류 = 301;
                    if (boleng == '<' && 다음 == '=') 종류 = 302;
                    if (boleng == '>' && 다음 == '=') 종류 = 303;
                    if (boleng == '&' && 다음 == '&') 종류 = 304;
                    if (boleng == '|' && 다음 == '|') 종류 = 305;
                    if (boleng == '+' && 다음 == '+') 종류 = 306;
                    if (boleng == '-' && 다음 == '-') 종류 = 307;
                    if (boleng == '+' && 다음 == '=') 종류 = 308;
                    if (boleng == '-' && 다음 == '=') 종류 = 309;
                    if (boleng == '*' && 다음 == '=') 종류 = 310;
                    if (boleng == '/' && 다음 == '=') 종류 = 311;
                    if (boleng == '%' && 다음 == '=') 종류 = 312;
                    if (종류 >= 300) 수++;
                }
            }
            if (토큰수 == 토큰종류.length - 1) { go_palelwa_boleng("too many tokens (2047 maximum)"); break; }
            토큰종류[토큰수] = 종류; 토큰위치[토큰수] = Diriša; thokene_botelele[토큰수++] = 수 - Diriša;
        }
    }
    static void ngwala_ya_go_se_fetoge_paete(int boleng) {
        if (ya_go_se_fetoge_bogolo == ya_go_se_fetoge_boleng.length) { go_palelwa_boleng("constant pool too large"); return; }
        ya_go_se_fetoge_boleng[ya_go_se_fetoge_bogolo++] = boleng & 255;
    }
    static void 상짧(int boleng) { ngwala_ya_go_se_fetoge_paete(boleng >> 8); ngwala_ya_go_se_fetoge_paete(boleng); }
    static int ngwadiša_ya_go_se_fetoge(int Diriša) {
        for (int 수 = 1; 수 < 상수수; 수++) {
            int 앞 = ya_go_se_fetoge_E_Šetšego[수], botelele_boleng = (수 + 1 < 상수수 ? ya_go_se_fetoge_E_Šetšego[수 + 1] : Diriša) - 앞;
            if (botelele_boleng != ya_go_se_fetoge_bogolo - Diriša) continue;
            boolean 같음 = true;
            for (int sekgobana_go_tsenya_tshedimošo = 0; sekgobana_go_tsenya_tshedimošo < botelele_boleng; sekgobana_go_tsenya_tshedimošo++) if (ya_go_se_fetoge_boleng[앞 + sekgobana_go_tsenya_tshedimošo] != ya_go_se_fetoge_boleng[Diriša + sekgobana_go_tsenya_tshedimošo]) 같음 = false;
            if (같음) { ya_go_se_fetoge_bogolo = Diriša; return 수; }
        }
        if (상수수 == ya_go_se_fetoge_E_Šetšego.length) { go_palelwa_boleng("too many constants"); return 0; }
        ya_go_se_fetoge_E_Šetšego[상수수] = Diriša;
        return 상수수++;
    }
    static void 글추가(int boleng) {
        if (tlhaka_botelele == 문자.length) { go_palelwa_boleng("text too long"); return; }
        문자[tlhaka_botelele++] = boleng;
    }
    static void 말추가(String Thalokontšu_SMS) { for (int 수 = 0; 수 < Thalokontšu_SMS.length(); 수++) 글추가(Thalokontšu_SMS.charAt(수)); }
    static int tlhaka_ya_go_se_fetoge() {
        int Diriša = ya_go_se_fetoge_bogolo; ngwala_ya_go_se_fetoge_paete(1); 상짧(0);
        for (int 수 = 0; 수 < tlhaka_botelele; 수++) {
            int boleng = 문자[수];
            if (boleng > 0 && boleng < 128) ngwala_ya_go_se_fetoge_paete(boleng);
            else if (boleng < 2048) { ngwala_ya_go_se_fetoge_paete(192 | boleng >> 6); ngwala_ya_go_se_fetoge_paete(128 | boleng & 63); }
            else { ngwala_ya_go_se_fetoge_paete(224 | boleng >> 12); ngwala_ya_go_se_fetoge_paete(128 | boleng >> 6 & 63); ngwala_ya_go_se_fetoge_paete(128 | boleng & 63); }
        }
        if (Phošo) return 0;
        int botelele_boleng = ya_go_se_fetoge_bogolo - Diriša - 3;
        ya_go_se_fetoge_boleng[Diriša + 1] = botelele_boleng >> 8; ya_go_se_fetoge_boleng[Diriša + 2] = botelele_boleng & 255;
        return ngwadiša_ya_go_se_fetoge(Diriša);
    }
    static int Thalokontšu_ya_go_se_fetoge(String Thalokontšu_SMS) { tlhaka_botelele = 0; 말추가(Thalokontšu_SMS); return tlhaka_ya_go_se_fetoge(); }
    static int thokene_ya_go_se_fetoge(int thokene_boleng) {
        tlhaka_botelele = 0;
        for (int 수 = 0; 수 < thokene_botelele[thokene_boleng]; 수++) 글추가(mohlodi[토큰위치[thokene_boleng] + 수]);
        return tlhaka_ya_go_se_fetoge();
    }
    static int Dipadišo(int 종류, int 가, int 나) {
        int Diriša = ya_go_se_fetoge_bogolo; ngwala_ya_go_se_fetoge_paete(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(나);
        return ngwadiša_ya_go_se_fetoge(Diriša);
    }
    static int 외부참조(int 종류, String mong_boleng, String Leina, String 서술) {
        int mong_sešupi = Dipadišo(7, Thalokontšu_ya_go_se_fetoge(mong_boleng), 0);
        int 이름수 = Thalokontšu_ya_go_se_fetoge(Leina), 형식수 = Thalokontšu_ya_go_se_fetoge(서술);
        return Dipadišo(종류, mong_sešupi, Dipadišo(12, 이름수, 형식수));
    }
    static void 내보내기(int boleng) {
        if (코드크기 == 코드.length) { go_palelwa_boleng("bytecode too large"); return; }
        코드[코드크기++] = boleng & 255;
    }
    static void Taelo(int boleng, int 인수) { 내보내기(boleng); 내보내기(인수 >> 8); 내보내기(인수); }
    static void 수상수(int boleng) {
        if (boleng >= -1 && boleng <= 5) { 내보내기(boleng + 3); return; }
        int Diriša = ya_go_se_fetoge_bogolo; ngwala_ya_go_se_fetoge_paete(3); 상짧(boleng >>> 16); 상짧(boleng);
        Taelo(19, ngwadiša_ya_go_se_fetoge(Diriša));
    }
    static int lekala(int Taelo) { int 결과 = 코드크기; Taelo(Taelo, 0); return 결과; }
    static void linke_boleng(int lekala, int nepo_selo) {
        if (Phošo) return;
        int 거리 = nepo_selo - lekala;
        if (거리 < -32768 || 거리 > 32767 || lekala < 0 || lekala + 2 >= 코드크기) { go_palelwa_boleng("invalid branch"); return; }
        코드[lekala + 1] = 거리 >> 8 & 255; 코드[lekala + 2] = 거리 & 255;
    }
    static void 비교값(int Taelo) {
        int 참 = lekala(Taelo); 내보내기(3); int 끝 = lekala(167);
        linke_boleng(참, 코드크기); 내보내기(4); linke_boleng(끝, 코드크기);
    }
    static int fomete_boleng() {
        if (말받기("void")) return 0;
        if (말받기("int")) return 1;
        if (말받기("boolean")) return 2;
        if (말받기("char")) return 5;
        if (말받기("FileInputStream")) return 6;
        if (말받기("FileOutputStream")) return 7;
        if (말받기("String")) { if (받기('[')) { 요구(']'); return 4; } return 3; }
        go_palelwa_boleng("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void oketša_fomete(int thaepa_boleng) {
        if (thaepa_boleng == 0) 글추가('V');
        if (thaepa_boleng == 1) 글추가('I');
        if (thaepa_boleng == 2) 글추가('Z');
        if (thaepa_boleng == 3) 말추가("Ljava/lang/String;");
        if (thaepa_boleng == 4) 말추가("[Ljava/lang/String;");
        if (thaepa_boleng == 5) 글추가('C');
        if (thaepa_boleng == 6) 말추가("Ljava/io/FileInputStream;");
        if (thaepa_boleng == 7) 말추가("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws 선언. 예외 tiragalo_boleng_go_tsenya_tshedimošo 본문은 go_nea_ditirelo javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = 말받기("한국어");
        if (한국어묶음) { 요구('.'); 말요구("자체"); 요구('.'); }
        if (!한국어묶음 && (말받기("Exception") || 말받기("IOException"))) return;
        if (말받기("예외") || 말받기("실행예외") || 말받기("입출력예외") || 말받기("대기시간초과예외") || 말받기("주소확인예외") || 말받기("파일없음예외") || 말받기("통신예외") || 말받기("잘못된인수예외") || 말받기("숫자형식예외") || 말받기("범위예외") || 말받기("배열범위예외") || 말받기("문자열범위예외") || 말받기("빈참조예외") || 말받기("산술예외") || 말받기("상태예외") || 말받기("형변환예외") || 말받기("음수배열크기예외") || 말받기("arei_lota_go_palelwa") || 말받기("가닥상태예외") || 말받기("대기중단예외")) return;
        go_palelwa_boleng("unsupported throws type");
    }
    static void 선언읽기() {
        while (말받기("import")) {
            if (Thalokontšu_boleng(위치, "한국어")) 예외이름읽기();
            else {
                말요구("java"); 요구('.'); 말요구("io"); 요구('.');
                if (!(말받기("FileInputStream") || 말받기("FileOutputStream") || 말받기("IOException"))) go_palelwa_boleng("unsupported import");
            }
            요구(';');
        }
        말받기("public"); 말받기("final"); 말요구("class"); legoro_thokene = sešupi_boleng();
        legoro_ya_go_se_fetoge = Dipadišo(7, thokene_ya_go_se_fetoge(legoro_thokene), 0);
        부모상수 = Dipadišo(7, Thalokontšu_ya_go_se_fetoge("java/lang/Object"), 0); 코드상수 = Thalokontšu_ya_go_se_fetoge("Code"); 요구('{');
        while (!Phošo && 종류() != '}') {
            if (함수수 == 32) { go_palelwa_boleng("too many methods"); break; }
            int fihlelela_go_tsenya_tshedimošo = 말받기("public") ? 1 : 말받기("private") ? 2 : 0; 말요구("static");
            int TIRO_boleng = 함수수++;
            mokgwa_fihlelela[TIRO_boleng] = fihlelela_go_tsenya_tshedimošo | 8;
            함수반환[TIRO_boleng] = fomete_boleng(); mokgwa_go_tsenya_tshedimošo_leina[TIRO_boleng] = sešupi_boleng(); 요구('(');
            for (int 앞 = 0; 앞 < TIRO_boleng; 앞++) if (이름같음(mokgwa_go_tsenya_tshedimošo_leina[앞], mokgwa_go_tsenya_tshedimošo_leina[TIRO_boleng])) go_palelwa_boleng("duplicate method (overloading unsupported)");
            while (!Phošo && 종류() != ')') {
                int 수 = 함수인수수[TIRO_boleng];
                if (수 == 16) { go_palelwa_boleng("too many parameters"); break; }
                int thaepa_boleng = fomete_boleng(); if (thaepa_boleng == 0) go_palelwa_boleng("void parameter");
                mokgwa_akumente_thaepa[TIRO_boleng * 16 + 수] = thaepa_boleng; mokgwa_akumente_leina[TIRO_boleng * 16 + 수] = sešupi_boleng();
                함수인수수[TIRO_boleng]++;
                if (!받기(',')) break;
            }
            요구(')');
            if (말받기("throws")) {
                do { 예외이름읽기(); } while (!Phošo && 받기(','));
            }
            함수본문[TIRO_boleng] = 위치; 요구('{');
            int 중첩 = 1;
            while (위치 < 토큰수 && 중첩 > 0) {
                if (종류() == '{') 중첩++;
                if (종류() == '}') 중첩--;
                위치++;
            }
            if (중첩 != 0) go_palelwa_boleng("unclosed method body");
            mokgwa_fetša[TIRO_boleng] = 위치;
            mokgwa_leina_ya_go_se_fetoge[TIRO_boleng] = thokene_ya_go_se_fetoge(mokgwa_go_tsenya_tshedimošo_leina[TIRO_boleng]);
            tlhaka_botelele = 0; 글추가('(');
            for (int 수 = 0; 수 < 함수인수수[TIRO_boleng]; 수++) oketša_fomete(mokgwa_akumente_thaepa[TIRO_boleng * 16 + 수]);
            글추가(')'); oketša_fomete(함수반환[TIRO_boleng]); 함수서술[TIRO_boleng] = tlhaka_ya_go_se_fetoge();
        }
        요구('}'); if (위치 != 토큰수) go_palelwa_boleng("extra input after class");
    }
    static int hwetša_kgauswi(int Leina) {
        for (int 수 = 지역수 - 1; 수 >= 0; 수--) if (지역깊이[수] >= 0 && 이름같음(kgauswi_leina[수], Leina)) return 수;
        go_palelwa_boleng("unknown variable"); return 0;
    }
    static int oketša_kgauswi(int Leina, int thaepa_boleng) {
        for (int 수 = 0; 수 < 지역수; 수++) if (지역깊이[수] >= 0 && 이름같음(kgauswi_leina[수], Leina)) go_palelwa_boleng("duplicate local variable");
        if (지역수 == 128) { go_palelwa_boleng("too many locals"); return 0; }
        kgauswi_leina[지역수] = Leina; kgauswi_thaepa[지역수] = thaepa_boleng; 지역깊이[지역수] = 깊이;
        return 지역수++;
    }
    static boolean palotlalo_thaepa(int thaepa_boleng) { return thaepa_boleng == 1 || thaepa_boleng == 5; }
    static void 지역읽기(int 수) { 내보내기(kgauswi_thaepa[수] <= 2 || kgauswi_thaepa[수] == 5 ? 21 : 25); 내보내기(수); }
    static void ngwala_kgauswi(int 수) { 내보내기(kgauswi_thaepa[수] <= 2 || kgauswi_thaepa[수] == 5 ? 54 : 58); 내보내기(수); }
    static void kgonthiša_thaepa(int kgonthe_data, int 기대) { if (kgonthe_data != 기대 && !(kgonthe_data == 5 && 기대 == 1)) go_palelwa_boleng("type mismatch"); }
    static void 문자읽기(int thokene_boleng) {
        tlhaka_botelele = 0; int Diriša = 토큰위치[thokene_boleng] + 1, 끝 = 토큰위치[thokene_boleng] + thokene_botelele[thokene_boleng] - 1;
        while (Diriša < 끝 && !Phošo) {
            int boleng = mohlodi[Diriša++];
            if (boleng == '\\') {
                if (Diriša == 끝) { go_palelwa_boleng("invalid escape"); break; }
                boleng = mohlodi[Diriša++];
                if (boleng == 'n') boleng = 10;
                else if (boleng == 'r') boleng = 13;
                else if (boleng == 't') boleng = 9;
                else if (boleng == 'b') boleng = 8;
                else if (boleng == 'f') boleng = 12;
                else if (boleng != '\\' && boleng != '"' && boleng != '\'') go_palelwa_boleng("unsupported escape");
            }
            글추가(boleng);
        }
    }
    static int ripaganya_palotlalo(int thokene_boleng, boolean 음수) {
        if (thokene_botelele[thokene_boleng] > 1 && mohlodi[토큰위치[thokene_boleng]] == '0') go_palelwa_boleng("octal literals unsupported");
        int boleng = 0;
        for (int 수 = 0; 수 < thokene_botelele[thokene_boleng]; 수++) {
            int 숫 = mohlodi[토큰위치[thokene_boleng] + 수] - '0';
            if (boleng < -214748364 || boleng == -214748364 && 숫 > (음수 ? 8 : 7)) go_palelwa_boleng("integer literal out of range");
            boleng = boleng * 10 - 숫;
        }
        return 음수 ? boleng : -boleng;
    }
    static int 기본식() {
        if (말받기("new")) {
            int thaepa_boleng = fomete_boleng();
            if (thaepa_boleng != 6 && thaepa_boleng != 7) { go_palelwa_boleng("only file streams supported by new in source"); return 0; }
            String mong_boleng = thaepa_boleng == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            Taelo(187, Dipadišo(7, Thalokontšu_ya_go_se_fetoge(mong_boleng), 0)); 내보내기(89);
            요구('('); kgonthiša_thaepa(tlhagišo_boleng(), 3); boolean 이어 = false;
            if (받기(',')) { if (thaepa_boleng != 7) go_palelwa_boleng("input stream constructor arguments"); kgonthiša_thaepa(tlhagišo_boleng(), 2); 이어 = true; }
            요구(')');
            Taelo(183, 외부참조(10, mong_boleng, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return thaepa_boleng;
        }
        if (받기('(')) { int thaepa_boleng = tlhagišo_boleng(); 요구(')'); return thaepa_boleng; }
        if (종류() == 257) { 수상수(ripaganya_palotlalo(위치++, false)); return 1; }
        if (종류() == 258) { 문자읽기(위치++); Taelo(19, Dipadišo(8, tlhaka_ya_go_se_fetoge(), 0)); return 3; }
        if (종류() == 259) { 문자읽기(위치++); if (tlhaka_botelele != 1) go_palelwa_boleng("character literal length"); 수상수(문자[0]); return 5; }
        if (말받기("true")) { 내보내기(4); return 2; }
        if (말받기("false")) { 내보내기(3); return 2; }
        if (말받기("한국어")) {
            요구('.'); 말요구("자체"); 요구('.');
            String mong_boleng = "", mokgwa_boleng = "", 서술 = ""; int 가 = 0, 나 = 0, 다 = 0, 라 = 0, 마 = 0, 결과 = 0;
            if (말받기("출력")) {
                mong_boleng = "한국어/자체/출력"; 요구('.');
                if (말받기("ngwala_mothaladi")) { mokgwa_boleng = "ngwala_mothaladi"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (말받기("Ngwala")) { mokgwa_boleng = "Ngwala"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (말받기("수쓰기")) { mokgwa_boleng = "수쓰기"; 서술 = "(I)V"; 가 = 1; }
                else go_palelwa_boleng("unknown Korean output method");
            } else if (말받기("문자")) {
                mong_boleng = "한국어/자체/문자"; 요구('.'); 가 = 3;
                if (말받기("botelele_boleng")) { mokgwa_boleng = "botelele_boleng"; 서술 = "(Ljava/lang/String;)I"; 결과 = 1; }
                else if (말받기("코드포인트수")) { mokgwa_boleng = "코드포인트수"; 서술 = "(Ljava/lang/String;)I"; 결과 = 1; }
                else if (말받기("ripaganya_palotlalo")) { mokgwa_boleng = "ripaganya_palotlalo"; 서술 = "(Ljava/lang/String;)I"; 결과 = 1; }
                else if (말받기("ngwala_palotlalo_boleng")) { mokgwa_boleng = "ngwala_palotlalo_boleng"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; 결과 = 3; }
                else if (말받기("같음")) { mokgwa_boleng = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; 나 = 3; 결과 = 2; }
                else if (말받기("pheista_SMS")) { mokgwa_boleng = "pheista_SMS"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; 나 = 3; 결과 = 3; }
                else if (말받기("sega_boleng")) { mokgwa_boleng = "sega_boleng"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; 나 = 1; 다 = 1; 결과 = 3; }
                else go_palelwa_boleng("unknown Korean text method");
            } else if (말받기("Faele")) {
                mong_boleng = "한국어/자체/Faele"; 요구('.'); 가 = 3;
                if (말받기("Bala")) { mokgwa_boleng = "Bala"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; 결과 = 3; }
                else if (말받기("Ngwala")) { mokgwa_boleng = "Ngwala"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; 나 = 3; }
                else go_palelwa_boleng("unknown Korean file method");
            } else if (말받기("화면")) {
                mong_boleng = "한국어/자체/화면"; 요구('.');
                if (말받기("너비")) { mokgwa_boleng = "너비"; 서술 = "()I"; 결과 = 1; }
                else if (말받기("높이")) { mokgwa_boleng = "높이"; 서술 = "()I"; 결과 = 1; }
                else if (말받기("사각형")) { mokgwa_boleng = "사각형"; 서술 = "(IIIII)V"; 가 = 1; 나 = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (말받기("지우기")) { mokgwa_boleng = "지우기"; 서술 = "(I)V"; 가 = 1; }
                else if (말받기("기다리기")) { mokgwa_boleng = "기다리기"; 서술 = "()V"; }
                else go_palelwa_boleng("unknown Korean framebuffer method");
            } else go_palelwa_boleng("unsupported Korean library class");
            요구('('); if (가 != 0) kgonthiša_thaepa(tlhagišo_boleng(), 가);
            if (나 != 0) { 요구(','); kgonthiša_thaepa(tlhagišo_boleng(), 나); }
            if (다 != 0) { 요구(','); kgonthiša_thaepa(tlhagišo_boleng(), 다); }
            if (라 != 0) { 요구(','); kgonthiša_thaepa(tlhagišo_boleng(), 라); }
            if (마 != 0) { 요구(','); kgonthiša_thaepa(tlhagišo_boleng(), 마); }
            요구(')'); Taelo(184, 외부참조(10, mong_boleng, mokgwa_boleng, 서술)); return 결과;
        }
        if (말받기("Integer")) {
            요구('.'); 말요구("parseInt"); 요구('('); kgonthiša_thaepa(tlhagišo_boleng(), 3); 요구(')');
            Taelo(184, 외부참조(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Leina = sešupi_boleng();
        if (받기('(')) {
            int TIRO_boleng = -1;
            for (int 수 = 0; 수 < 함수수; 수++) if (이름같음(Leina, mokgwa_go_tsenya_tshedimošo_leina[수])) TIRO_boleng = 수;
            if (TIRO_boleng < 0) { go_palelwa_boleng("unknown static method"); return 0; }
            int 수 = 0;
            while (!Phošo && 종류() != ')') {
                if (수 >= 함수인수수[TIRO_boleng]) { go_palelwa_boleng("too many arguments"); break; }
                kgonthiša_thaepa(tlhagišo_boleng(), mokgwa_akumente_thaepa[TIRO_boleng * 16 + 수++]); if (!받기(',')) break;
            }
            요구(')'); if (수 != 함수인수수[TIRO_boleng]) go_palelwa_boleng("argument count mismatch");
            Taelo(184, Dipadišo(10, legoro_ya_go_se_fetoge, Dipadišo(12, mokgwa_leina_ya_go_se_fetoge[TIRO_boleng], 함수서술[TIRO_boleng])));
            return 함수반환[TIRO_boleng];
        }
        int kgauswi_skoupo = hwetša_kgauswi(Leina), thaepa_boleng = kgauswi_thaepa[kgauswi_skoupo]; 지역읽기(kgauswi_skoupo);
        while (!Phošo) {
            if (받기('[')) { kgonthiša_thaepa(thaepa_boleng, 4); kgonthiša_thaepa(tlhagišo_boleng(), 1); 요구(']'); 내보내기(50); thaepa_boleng = 3; }
            else if (받기('.')) {
                if (thaepa_boleng == 6 || thaepa_boleng == 7) {
                    String mong_boleng = thaepa_boleng == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (말받기("close")) { 요구('('); 요구(')'); Taelo(182, 외부참조(10, mong_boleng, "close", "()V")); thaepa_boleng = 0; }
                    else if (thaepa_boleng == 6 && 말받기("read")) { 요구('('); 요구(')'); Taelo(182, 외부참조(10, mong_boleng, "read", "()I")); thaepa_boleng = 1; }
                    else if (thaepa_boleng == 7 && 말받기("write")) { 요구('('); kgonthiša_thaepa(tlhagišo_boleng(), 1); 요구(')'); Taelo(182, 외부참조(10, mong_boleng, "write", "(I)V")); thaepa_boleng = 0; }
                    else { go_palelwa_boleng("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (thaepa_boleng == 4) { 내보내기(190); thaepa_boleng = 1; }
                else { kgonthiša_thaepa(thaepa_boleng, 3); 요구('('); 요구(')'); Taelo(182, 외부참조(10, "java/lang/String", "length", "()I")); thaepa_boleng = 1; }
            } else break;
        }
        return thaepa_boleng;
    }
    static int 단항() {
        if (++식깊이 > 64) { go_palelwa_boleng("expression nesting too deep"); 식깊이--; return 0; }
        int thaepa_boleng;
        if (받기('!')) { kgonthiša_thaepa(단항(), 2); 비교값(153); thaepa_boleng = 2; }
        else if (받기('-')) {
            if (종류() == 257) 수상수(ripaganya_palotlalo(위치++, true));
            else { kgonthiša_thaepa(단항(), 1); 내보내기(116); }
            thaepa_boleng = 1;
        } else if (받기('+')) { kgonthiša_thaepa(단항(), 1); thaepa_boleng = 1; }
        else thaepa_boleng = 기본식();
        식깊이--; return thaepa_boleng;
    }
    static int 곱식() {
        int thaepa_boleng = 단항();
        while (!Phošo && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int go_enkhouta_boleng = 종류(); 위치++; kgonthiša_thaepa(thaepa_boleng, 1); kgonthiša_thaepa(단항(), 1);
            내보내기(go_enkhouta_boleng == '*' ? 104 : go_enkhouta_boleng == '/' ? 108 : 112); thaepa_boleng = 1;
        }
        return thaepa_boleng;
    }
    static int 합식() {
        int thaepa_boleng = 곱식();
        while (!Phošo && (종류() == '+' || 종류() == '-')) {
            int go_enkhouta_boleng = 종류(); 위치++; int 경계 = 코드크기, Morago_boleng_thaepa = 곱식();
            if (go_enkhouta_boleng == '+' && (thaepa_boleng == 3 || Morago_boleng_thaepa == 3)) { 결합(경계, thaepa_boleng, Morago_boleng_thaepa); thaepa_boleng = 3; }
            else { kgonthiša_thaepa(thaepa_boleng, 1); kgonthiša_thaepa(Morago_boleng_thaepa, 1); 내보내기(go_enkhouta_boleng == '+' ? 96 : 100); thaepa_boleng = 1; }
        }
        return thaepa_boleng;
    }
    static int 붙임참조(int thaepa_boleng) {
        if (thaepa_boleng != 1 && thaepa_boleng != 2 && thaepa_boleng != 3 && thaepa_boleng != 5) go_palelwa_boleng("unsupported concatenation type");
        return 외부참조(10, "java/lang/StringBuilder", "append", thaepa_boleng == 1 ? "(I)Ljava/lang/StringBuilder;"
            : thaepa_boleng == 2 ? "(Z)Ljava/lang/StringBuilder;" : thaepa_boleng == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int 경계, int 앞형, int Morago_boleng_thaepa) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 오른쪽 코드 앞에 생성 코드를 삽입한다.
        // 오른쪽 tlhagišo_boleng 내부의 sedirišwa_sa_legoro_le_tee_boleng lekala 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = 코드크기;
        Taelo(187, Dipadišo(7, Thalokontšu_ya_go_se_fetoge("java/lang/StringBuilder"), 0)); 내보내기(89);
        Taelo(183, 외부참조(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); Taelo(182, 붙임참조(앞형));
        if (Phošo) return;
        int botelele_boleng = 코드크기 - 끝;
        for (int 수 = 0; 수 < botelele_boleng; 수++) 삽입코드[수] = 코드[끝 + 수];
        for (int 수 = 끝 - 1; 수 >= 경계; 수--) 코드[수 + botelele_boleng] = 코드[수];
        for (int 수 = 0; 수 < botelele_boleng; 수++) 코드[경계 + 수] = 삽입코드[수];
        Taelo(182, 붙임참조(Morago_boleng_thaepa)); Taelo(182, 외부참조(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int 비교식() {
        int thaepa_boleng = 합식();
        while (!Phošo && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int go_enkhouta_boleng = 종류(); 위치++; kgonthiša_thaepa(thaepa_boleng, 1); kgonthiša_thaepa(합식(), 1);
            비교값(go_enkhouta_boleng == '<' ? 161 : go_enkhouta_boleng == '>' ? 163 : go_enkhouta_boleng == 302 ? 164 : 162); thaepa_boleng = 2;
        }
        return thaepa_boleng;
    }
    static int 동등식() {
        int thaepa_boleng = 비교식();
        while (!Phošo && (종류() == 300 || 종류() == 301)) {
            int go_enkhouta_boleng = 종류(); 위치++; int Morago_boleng_thaepa = 비교식();
            if (thaepa_boleng == 0 || Morago_boleng_thaepa == 0) go_palelwa_boleng("void expression");
            if (!(palotlalo_thaepa(thaepa_boleng) && palotlalo_thaepa(Morago_boleng_thaepa))) kgonthiša_thaepa(Morago_boleng_thaepa, thaepa_boleng);
            비교값((thaepa_boleng <= 2 || thaepa_boleng == 5 ? 159 : 165) + (go_enkhouta_boleng == 301 ? 1 : 0)); thaepa_boleng = 2;
        }
        return thaepa_boleng;
    }
    static int 논리곱() {
        int thaepa_boleng = 동등식();
        while (!Phošo && 받기(304)) {
            kgonthiša_thaepa(thaepa_boleng, 2); int 가 = lekala(153); kgonthiša_thaepa(동등식(), 2); int 나 = lekala(153);
            내보내기(4); int 끝 = lekala(167); linke_boleng(가, 코드크기); linke_boleng(나, 코드크기); 내보내기(3); linke_boleng(끝, 코드크기); thaepa_boleng = 2;
        }
        return thaepa_boleng;
    }
    static int tlhagišo_boleng() {
        int thaepa_boleng = 논리곱();
        while (!Phošo && 받기(305)) {
            kgonthiša_thaepa(thaepa_boleng, 2); int 가 = lekala(154); kgonthiša_thaepa(논리곱(), 2); int 나 = lekala(154);
            내보내기(3); int 끝 = lekala(167); linke_boleng(가, 코드크기); linke_boleng(나, 코드크기); 내보내기(4); linke_boleng(끝, 코드크기); thaepa_boleng = 2;
        }
        return thaepa_boleng;
    }
    static void mošomo_boleng(boolean 선언허용) {
        if (Thalokontšu_boleng(위치, "int") || Thalokontšu_boleng(위치, "boolean") || Thalokontšu_boleng(위치, "String") || Thalokontšu_boleng(위치, "char")
            || Thalokontšu_boleng(위치, "FileInputStream") || Thalokontšu_boleng(위치, "FileOutputStream")) {
            if (!선언허용) go_palelwa_boleng("declaration not allowed here");
            int thaepa_boleng = fomete_boleng(), Leina = sešupi_boleng(); 요구('='); kgonthiša_thaepa(tlhagišo_boleng(), thaepa_boleng);
            ngwala_kgauswi(oketša_kgauswi(Leina, thaepa_boleng)); return;
        }
        int Leina = sešupi_boleng(), kgauswi_skoupo = hwetša_kgauswi(Leina);
        if (받기('=')) { kgonthiša_thaepa(tlhagišo_boleng(), kgauswi_thaepa[kgauswi_skoupo]); ngwala_kgauswi(kgauswi_skoupo); }
        else if (종류() >= 308 && 종류() <= 312) {
            int go_enkhouta_boleng = 종류(); 위치++; 지역읽기(kgauswi_skoupo); int 경계 = 코드크기, Morago_boleng_thaepa = tlhagišo_boleng();
            if (go_enkhouta_boleng == 308 && kgauswi_thaepa[kgauswi_skoupo] == 3) 결합(경계, 3, Morago_boleng_thaepa);
            else {
                kgonthiša_thaepa(kgauswi_thaepa[kgauswi_skoupo], 1); kgonthiša_thaepa(Morago_boleng_thaepa, 1);
                내보내기(go_enkhouta_boleng == 308 ? 96 : go_enkhouta_boleng == 309 ? 100 : go_enkhouta_boleng == 310 ? 104 : go_enkhouta_boleng == 311 ? 108 : 112);
                if (kgauswi_thaepa[kgauswi_skoupo] == 5) 내보내기(146);
            }
            ngwala_kgauswi(kgauswi_skoupo);
        }
        else if (종류() == 306 || 종류() == 307) {
            kgonthiša_thaepa(kgauswi_thaepa[kgauswi_skoupo], 1); 내보내기(132); 내보내기(kgauswi_skoupo); 내보내기(종류() == 306 ? 1 : 255); 위치++;
            if (kgauswi_thaepa[kgauswi_skoupo] == 5) { 지역읽기(kgauswi_skoupo); 내보내기(146); ngwala_kgauswi(kgauswi_skoupo); }
        } else go_palelwa_boleng("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); 요구('.'); 말요구("out"); 요구('.');
        boolean 줄바꿈 = 말받기("println"); if (!줄바꿈) 말요구("print"); 요구('(');
        Taelo(178, 외부참조(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean hloka_selo_akumente = 종류() == ')';
        int thaepa_boleng = hloka_selo_akumente ? 0 : tlhagišo_boleng(); 요구(')'); 요구(';');
        String 서술 = thaepa_boleng == 0 ? "()V" : thaepa_boleng == 1 ? "(I)V" : thaepa_boleng == 2 ? "(Z)V" : thaepa_boleng == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (thaepa_boleng == 4 || thaepa_boleng >= 6 || thaepa_boleng == 0 && (!줄바꿈 || !hloka_selo_akumente)) go_palelwa_boleng("unsupported print argument");
        Taelo(182, 외부참조(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean setatamente_boleng() {
        if (Phošo) return false;
        if (깊이 > 32) { go_palelwa_boleng("statement nesting too deep"); return false; }
        if (받기('{')) {
            깊이++; boolean 반환 = false;
            while (!Phošo && 종류() != '}') { if (반환) go_palelwa_boleng("unreachable statement"); 반환 = setatamente_boleng(); }
            요구('}'); for (int 수 = 0; 수 < 지역수; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return 반환;
        }
        if (받기(';')) return false;
        if (말받기("return")) {
            int thaepa_boleng = 종류() == ';' ? 0 : tlhagišo_boleng(); kgonthiša_thaepa(thaepa_boleng, 함수반환[현재함수]); 요구(';');
            내보내기(thaepa_boleng == 0 ? 177 : thaepa_boleng <= 2 || thaepa_boleng == 5 ? 172 : 176); return true;
        }
        if (말받기("if")) {
            요구('('); kgonthiša_thaepa(tlhagišo_boleng(), 2); 요구(')'); int 거짓 = lekala(153);
            깊이++; boolean 가 = taolo_setatamente(); 깊이--;
            if (말받기("else")) { int 끝 = lekala(167); linke_boleng(거짓, 코드크기); 깊이++; boolean 나 = taolo_setatamente(); 깊이--; linke_boleng(끝, 코드크기); return 가 && 나; }
            linke_boleng(거짓, 코드크기); return false;
        }
        if (말받기("while")) {
            int Diriša = 코드크기; 요구('('); kgonthiša_thaepa(tlhagišo_boleng(), 2); 요구(')'); int 끝 = lekala(153);
            깊이++; taolo_setatamente(); 깊이--; linke_boleng(lekala(167), Diriša); linke_boleng(끝, 코드크기); return false;
        }
        if (말받기("for")) {
            깊이++; 요구('('); if (종류() != ';') mošomo_boleng(true); 요구(';');
            int seemo = 코드크기; if (종류() == ';') 내보내기(4); else kgonthiša_thaepa(tlhagišo_boleng(), 2); 요구(';');
            int 끝 = lekala(153), mmele_wa_sengwalwa = lekala(167), mpshafatša = 코드크기;
            if (종류() != ')') mošomo_boleng(false); 요구(')'); linke_boleng(lekala(167), seemo); linke_boleng(mmele_wa_sengwalwa, 코드크기);
            taolo_setatamente(); linke_boleng(lekala(167), mpshafatša); linke_boleng(끝, 코드크기);
            for (int 수 = 0; 수 < 지역수; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return false;
        }
        if (Thalokontšu_boleng(위치, "System")) { 화면출력(); return false; }
        if (종류() == 256 && 위치 + 1 < 토큰수 && (토큰종류[위치 + 1] == '(' || 토큰종류[위치 + 1] == '.')) {
            int thaepa_boleng = tlhagišo_boleng(); if (thaepa_boleng != 0) 내보내기(87); 요구(';'); return false;
        }
        mošomo_boleng(true); 요구(';'); return false;
    }
    static boolean taolo_setatamente() {
        if (Thalokontšu_boleng(위치, "int") || Thalokontšu_boleng(위치, "boolean") || Thalokontšu_boleng(위치, "char") || Thalokontšu_boleng(위치, "String")
            || Thalokontšu_boleng(위치, "FileInputStream") || Thalokontšu_boleng(위치, "FileOutputStream")) go_palelwa_boleng("local declaration requires braces");
        return setatamente_boleng();
    }
    static void 출바(int boleng) { if (출력크기 == 출력.length) go_palelwa_boleng("class file too large"); else 출력[출력크기++] = boleng & 255; }
    static void 출짧(int boleng) { 출바(boleng >> 8); 출바(boleng); }
    static void 출정(int boleng) { 출짧(boleng >>> 16); 출짧(boleng); }
    static void ngwala_legoro() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(상수수);
        for (int 수 = 0; 수 < ya_go_se_fetoge_bogolo; 수++) 출바(ya_go_se_fetoge_boleng[수]);
        출짧(0x21); 출짧(legoro_ya_go_se_fetoge); 출짧(부모상수); 출짧(0); 출짧(0); 출짧(함수수);
        for (int 수 = 0; 수 < 함수수; 수++) {
            출짧(mokgwa_fihlelela[수]); 출짧(mokgwa_leina_ya_go_se_fetoge[수]); 출짧(함수서술[수]); 출짧(1); 출짧(코드상수);
            출정(12 + mokgwa_botelele[수]); 출짧(128); 출짧(함수지역[수]); 출정(mokgwa_botelele[수]);
            for (int sekgobana_go_tsenya_tshedimošo = 0; sekgobana_go_tsenya_tshedimošo < mokgwa_botelele[수]; sekgobana_go_tsenya_tshedimošo++) 출바(코드[함수코드[수] + sekgobana_go_tsenya_tshedimošo]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int Diriša() {
        if (mošomiši.인수개수() == 1 && 자바도구.같음(mošomiši.인수(0), "-version")) {
            mošomiši.Ngwala("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (mošomiši.인수개수() != 1) { mošomiši.Ngwala("Usage: javac FILE.java\n"); return 2; }
        int leina_bogolo = 자바도구.Leina(faele_leina_SMS, mošomiši.인수(0));
        if (leina_bogolo < 6 || leina_bogolo > 62 || faele_leina_SMS[leina_bogolo - 5] != '.' || faele_leina_SMS[leina_bogolo - 4] != 'j'
            || faele_leina_SMS[leina_bogolo - 3] != 'a' || faele_leina_SMS[leina_bogolo - 2] != 'v' || faele_leina_SMS[leina_bogolo - 1] != 'a') {
            mošomiši.Ngwala("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        mohlodi_bogolo = mošomiši.파일읽기(faele_leina_SMS, mohlodi);
        if (mohlodi_bogolo < 0) { mošomiši.Ngwala("javac: cannot read source: "); 자바도구.수쓰기(mohlodi_bogolo); mošomiši.ngwala_tlhaka_boleng(10); return 1; }
        mohlodi_bogolo = 자바도구.원문해독(mohlodi, mohlodi_bogolo);
        if (mohlodi_bogolo < 0) { mošomiši.Ngwala("javac error: invalid UTF-8 source\n"); return 1; }
        sega_boleng(); if (!Phošo) 선언읽기();
        if (!Phošo) {
            if (thokene_botelele[legoro_thokene] != leina_bogolo - 5) go_palelwa_boleng("class name must match file name");
            for (int 수 = 0; 수 < leina_bogolo - 5; 수++) if (mohlodi[토큰위치[legoro_thokene] + 수] != faele_leina_SMS[수]) go_palelwa_boleng("class name must match file name");
        }
        for (현재함수 = 0; 현재함수 < 함수수 && !Phošo; 현재함수++) {
            위치 = 함수본문[현재함수]; 함수코드[현재함수] = 코드크기; 지역수 = 0; 깊이 = 0;
            for (int 수 = 0; 수 < 함수인수수[현재함수]; 수++) oketša_kgauswi(mokgwa_akumente_leina[현재함수 * 16 + 수], mokgwa_akumente_thaepa[현재함수 * 16 + 수]);
            boolean 반환 = setatamente_boleng();
            if (!반환 && 함수반환[현재함수] != 0) go_palelwa_boleng("missing return");
            // lekala 뒤의 합류 지점은 반드시 kgonthe_data 명령이어야 한다 (버전 49 검증기).
            if (함수반환[현재함수] == 0) 내보내기(177);
            else { boolean palotlalo = 함수반환[현재함수] <= 2 || 함수반환[현재함수] == 5; 내보내기(palotlalo ? 3 : 1); 내보내기(palotlalo ? 172 : 176); }
            if (위치 != mokgwa_fetša[현재함수]) go_palelwa_boleng("invalid method body");
            함수지역[현재함수] = 지역수; mokgwa_botelele[현재함수] = 코드크기 - 함수코드[현재함수];
        }
        if (Phošo) return 1;
        ngwala_legoro(); if (Phošo) return 1;
        faele_leina_SMS[leina_bogolo - 4] = 'c'; faele_leina_SMS[leina_bogolo - 3] = 'l'; faele_leina_SMS[leina_bogolo - 2] = 'a';
        faele_leina_SMS[leina_bogolo - 1] = 's'; faele_leina_SMS[leina_bogolo] = 's'; faele_leina_SMS[leina_bogolo + 1] = 0;
        int 결과 = mošomiši.ngwala_faele(faele_leina_SMS, 출력, 출력크기);
        if (결과 < 0) { mošomiši.Ngwala("javac: cannot save class: "); 자바도구.수쓰기(결과); mošomiši.ngwala_tlhaka_boleng(10); return 1; }
        mošomiši.Ngwala("Compiled: "); for (int 수 = 0; faele_leina_SMS[수] != 0; 수++) mošomiši.ngwala_tlhaka_boleng(faele_leina_SMS[수]);
        mošomiši.Ngwala(" (JVM class version 49)\n"); return 0;
    }
}
