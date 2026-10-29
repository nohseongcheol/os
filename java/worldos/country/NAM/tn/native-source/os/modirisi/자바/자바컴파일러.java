// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java Motswedi_sebopego_sa_tshedimosetso -> 표준 버전 49 class 컴파일러. */
public final class 자바컴파일러 {
    static int[] Motswedi = new int[16384], 출력 = new int[16384], 코드 = new int[4096];
    static int[] 토큰종류 = new int[2048], 토큰위치 = new int[2048], papetlana_boleele = new int[2048];
    static int[] tlhomameng_Boleng = new int[4096], tlhomameng_Baya_ka_Tekatekanyo = new int[512];
    static int[] 문자 = new int[512], faele_leina_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int Motswedi_lekanya, 토큰수, 위치, 코드크기, tlhomameng_lekanya, 상수수 = 1, 출력크기, Letshwao_boleele;
    static boolean phoso;
    static int mofuta_papetlana, mofuta_tlhomameng, 부모상수, 코드상수;
    static int[] mokgwa_tsenyo_leina = new int[32], 함수반환 = new int[32], 함수인수수 = new int[32];
    static int[] mokgwa_Thulaganyo_leina = new int[512], mokgwa_Thulaganyo_tlanya = new int[512];
    static int[] 함수본문 = new int[32], mokgwa_kgaola = new int[32], 함수코드 = new int[32];
    static int[] mokgwa_boleele = new int[32], 함수지역 = new int[32], mokgwa_leina_tlhomameng = new int[32], 함수서술 = new int[32];
    static int[] mokgwa_letlelesega = new int[32];
    static int 함수수, ga_jaana_mokgwa, 지역수, 깊이, 식깊이;
    static int[] e_e_gaufi_leina = new int[128], e_e_gaufi_tlanya = new int[128], 지역깊이 = new int[128];

    static void palelo_Boleng(String 이유) {
        if (!phoso) {
            modirisi.kwala("javac error: "); modirisi.kwala(이유);
            modirisi.kwala(" at line ");
            int Mola = 1, 끝 = 위치 < 토큰수 ? 토큰위치[위치] : Motswedi_lekanya;
            for (int 수 = 0; 수 < 끝; 수++) if (Motswedi[수] == 10) Mola++;
            자바도구.수쓰기(Mola); modirisi.kwala_Letshwao_Boleng(10);
        }
        phoso = true;
    }
    static boolean Letshwao_Boleng(int Boleng) { return 문자이름규칙.첫글자(Boleng); }
    static boolean dijite_Boleng(int Boleng) { return Boleng >= '0' && Boleng <= '9'; }
    static boolean 이름같음(int 가, int 나) {
        if (가 < 0 || 나 < 0 || 가 >= 토큰수 || 나 >= 토큰수 || papetlana_boleele[가] != papetlana_boleele[나]) return false;
        for (int 수 = 0; 수 < papetlana_boleele[가]; 수++) if (Motswedi[토큰위치[가] + 수] != Motswedi[토큰위치[나] + 수]) return false;
        return true;
    }
    static boolean Lefoko_Boleng(int papetlana_Boleng, String Lefoko_SMS) {
        if (papetlana_Boleng < 0 || papetlana_Boleng >= 토큰수 || papetlana_boleele[papetlana_Boleng] != Lefoko_SMS.length()) return false;
        for (int 수 = 0; 수 < Lefoko_SMS.length(); 수++) if (Motswedi[토큰위치[papetlana_Boleng] + 수] != Lefoko_SMS.charAt(수)) return false;
        return true;
    }
    static int 종류() { return 위치 < 토큰수 ? 토큰종류[위치] : 0; }
    static boolean 받기(int Boleng) { if (종류() != Boleng) return false; 위치++; return true; }
    static void 요구(int Boleng) { if (!받기(Boleng)) palelo_Boleng("unexpected token"); }
    static boolean 말받기(String Lefoko_SMS) { if (!Lefoko_Boleng(위치, Lefoko_SMS)) return false; 위치++; return true; }
    static void 말요구(String Lefoko_SMS) { if (!말받기(Lefoko_SMS)) palelo_Boleng(Lefoko_SMS); }
    static int setlhaodi_Boleng() {
        int 결과 = 위치;
        if (종류() != 256) palelo_Boleng("identifier required"); else 위치++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int dirisa = 0;
        for (int 수 = 0; 수 <= 예약어.length(); 수++) {
            if (수 == 예약어.length() || 예약어.charAt(수) == ' ') {
                boolean 같음 = 수 - dirisa == papetlana_boleele[결과];
                for (int sebaka_tsenyo = dirisa; 같음 && sebaka_tsenyo < 수; sebaka_tsenyo++) if (예약어.charAt(sebaka_tsenyo) != Motswedi[토큰위치[결과] + sebaka_tsenyo - dirisa]) 같음 = false;
                if (같음) palelo_Boleng("reserved word cannot be an identifier");
                dirisa = 수 + 1;
            }
        }
        return 결과;
    }
    static void sega_Boleng() {
        int 수 = 0;
        while (수 < Motswedi_lekanya && !phoso) {
            int Boleng = Motswedi[수], dirisa = 수, 종류 = Boleng;
            if (Boleng == 32 || Boleng == 9 || Boleng == 10 || Boleng == 13) { 수++; continue; }
            if (Boleng == '/' && 수 + 1 < Motswedi_lekanya && Motswedi[수 + 1] == '/') {
                while (수 < Motswedi_lekanya && Motswedi[수] != 10) 수++;
                continue;
            }
            if (Boleng == '/' && 수 + 1 < Motswedi_lekanya && Motswedi[수 + 1] == '*') {
                수 += 2;
                while (수 + 1 < Motswedi_lekanya && !(Motswedi[수] == '*' && Motswedi[수 + 1] == '/')) 수++;
                if (수 + 1 >= Motswedi_lekanya) { palelo_Boleng("unterminated comment"); break; }
                수 += 2; continue;
            }
            if (Letshwao_Boleng(Boleng)) { 종류 = 256; while (수 < Motswedi_lekanya && 문자이름규칙.이어진글자(Motswedi[수])) 수++; }
            else if (dijite_Boleng(Boleng)) { 종류 = 257; while (수 < Motswedi_lekanya && dijite_Boleng(Motswedi[수])) 수++; }
            else if (Boleng == '"' || Boleng == '\'') {
                종류 = Boleng == '"' ? 258 : 259; 수++;
                while (수 < Motswedi_lekanya && Motswedi[수] != Boleng && Motswedi[수] != 10 && Motswedi[수] != 13) {
                    if (Motswedi[수] == '\\') 수++;
                    수++;
                }
                if (수 >= Motswedi_lekanya || Motswedi[수] != Boleng) { palelo_Boleng("unterminated literal"); break; }
                수++;
            } else {
                수++;
                if (수 < Motswedi_lekanya) {
                    int 다음 = Motswedi[수];
                    if (Boleng == '=' && 다음 == '=') 종류 = 300;
                    if (Boleng == '!' && 다음 == '=') 종류 = 301;
                    if (Boleng == '<' && 다음 == '=') 종류 = 302;
                    if (Boleng == '>' && 다음 == '=') 종류 = 303;
                    if (Boleng == '&' && 다음 == '&') 종류 = 304;
                    if (Boleng == '|' && 다음 == '|') 종류 = 305;
                    if (Boleng == '+' && 다음 == '+') 종류 = 306;
                    if (Boleng == '-' && 다음 == '-') 종류 = 307;
                    if (Boleng == '+' && 다음 == '=') 종류 = 308;
                    if (Boleng == '-' && 다음 == '=') 종류 = 309;
                    if (Boleng == '*' && 다음 == '=') 종류 = 310;
                    if (Boleng == '/' && 다음 == '=') 종류 = 311;
                    if (Boleng == '%' && 다음 == '=') 종류 = 312;
                    if (종류 >= 300) 수++;
                }
            }
            if (토큰수 == 토큰종류.length - 1) { palelo_Boleng("too many tokens (2047 maximum)"); break; }
            토큰종류[토큰수] = 종류; 토큰위치[토큰수] = dirisa; papetlana_boleele[토큰수++] = 수 - dirisa;
        }
    }
    static void kwala_tlhomameng_baete(int Boleng) {
        if (tlhomameng_lekanya == tlhomameng_Boleng.length) { palelo_Boleng("constant pool too large"); return; }
        tlhomameng_Boleng[tlhomameng_lekanya++] = Boleng & 255;
    }
    static void 상짧(int Boleng) { kwala_tlhomameng_baete(Boleng >> 8); kwala_tlhomameng_baete(Boleng); }
    static int kwadisa_tlhomameng(int dirisa) {
        for (int 수 = 1; 수 < 상수수; 수++) {
            int 앞 = tlhomameng_Baya_ka_Tekatekanyo[수], boleele_Boleng = (수 + 1 < 상수수 ? tlhomameng_Baya_ka_Tekatekanyo[수 + 1] : dirisa) - 앞;
            if (boleele_Boleng != tlhomameng_lekanya - dirisa) continue;
            boolean 같음 = true;
            for (int sebaka_tsenyo = 0; sebaka_tsenyo < boleele_Boleng; sebaka_tsenyo++) if (tlhomameng_Boleng[앞 + sebaka_tsenyo] != tlhomameng_Boleng[dirisa + sebaka_tsenyo]) 같음 = false;
            if (같음) { tlhomameng_lekanya = dirisa; return 수; }
        }
        if (상수수 == tlhomameng_Baya_ka_Tekatekanyo.length) { palelo_Boleng("too many constants"); return 0; }
        tlhomameng_Baya_ka_Tekatekanyo[상수수] = dirisa;
        return 상수수++;
    }
    static void 글추가(int Boleng) {
        if (Letshwao_boleele == 문자.length) { palelo_Boleng("text too long"); return; }
        문자[Letshwao_boleele++] = Boleng;
    }
    static void 말추가(String Lefoko_SMS) { for (int 수 = 0; 수 < Lefoko_SMS.length(); 수++) 글추가(Lefoko_SMS.charAt(수)); }
    static int Letshwao_tlhomameng() {
        int dirisa = tlhomameng_lekanya; kwala_tlhomameng_baete(1); 상짧(0);
        for (int 수 = 0; 수 < Letshwao_boleele; 수++) {
            int Boleng = 문자[수];
            if (Boleng > 0 && Boleng < 128) kwala_tlhomameng_baete(Boleng);
            else if (Boleng < 2048) { kwala_tlhomameng_baete(192 | Boleng >> 6); kwala_tlhomameng_baete(128 | Boleng & 63); }
            else { kwala_tlhomameng_baete(224 | Boleng >> 12); kwala_tlhomameng_baete(128 | Boleng >> 6 & 63); kwala_tlhomameng_baete(128 | Boleng & 63); }
        }
        if (phoso) return 0;
        int boleele_Boleng = tlhomameng_lekanya - dirisa - 3;
        tlhomameng_Boleng[dirisa + 1] = boleele_Boleng >> 8; tlhomameng_Boleng[dirisa + 2] = boleele_Boleng & 255;
        return kwadisa_tlhomameng(dirisa);
    }
    static int Lefoko_tlhomameng(String Lefoko_SMS) { Letshwao_boleele = 0; 말추가(Lefoko_SMS); return Letshwao_tlhomameng(); }
    static int papetlana_tlhomameng(int papetlana_Boleng) {
        Letshwao_boleele = 0;
        for (int 수 = 0; 수 < papetlana_boleele[papetlana_Boleng]; 수++) 글추가(Motswedi[토큰위치[papetlana_Boleng] + 수]);
        return Letshwao_tlhomameng();
    }
    static int Tshupiso(int 종류, int 가, int 나) {
        int dirisa = tlhomameng_lekanya; kwala_tlhomameng_baete(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(나);
        return kwadisa_tlhomameng(dirisa);
    }
    static int 외부참조(int 종류, String mong_Boleng, String leina, String 서술) {
        int mong_setlhaodi = Tshupiso(7, Lefoko_tlhomameng(mong_Boleng), 0);
        int 이름수 = Lefoko_tlhomameng(leina), 형식수 = Lefoko_tlhomameng(서술);
        return Tshupiso(종류, mong_setlhaodi, Tshupiso(12, 이름수, 형식수));
    }
    static void 내보내기(int Boleng) {
        if (코드크기 == 코드.length) { palelo_Boleng("bytecode too large"); return; }
        코드[코드크기++] = Boleng & 255;
    }
    static void Taelo(int Boleng, int 인수) { 내보내기(Boleng); 내보내기(인수 >> 8); 내보내기(인수); }
    static void 수상수(int Boleng) {
        if (Boleng >= -1 && Boleng <= 5) { 내보내기(Boleng + 3); return; }
        int dirisa = tlhomameng_lekanya; kwala_tlhomameng_baete(3); 상짧(Boleng >>> 16); 상짧(Boleng);
        Taelo(19, kwadisa_tlhomameng(dirisa));
    }
    static int lekala(int Taelo) { int 결과 = 코드크기; Taelo(Taelo, 0); return 결과; }
    static void Kgokagano_Boleng(int lekala, int setotwa_selwana) {
        if (phoso) return;
        int 거리 = setotwa_selwana - lekala;
        if (거리 < -32768 || 거리 > 32767 || lekala < 0 || lekala + 2 >= 코드크기) { palelo_Boleng("invalid branch"); return; }
        코드[lekala + 1] = 거리 >> 8 & 255; 코드[lekala + 2] = 거리 & 255;
    }
    static void 비교값(int Taelo) {
        int 참 = lekala(Taelo); 내보내기(3); int 끝 = lekala(167);
        Kgokagano_Boleng(참, 코드크기); 내보내기(4); Kgokagano_Boleng(끝, 코드크기);
    }
    static int fometa_Boleng() {
        if (말받기("void")) return 0;
        if (말받기("int")) return 1;
        if (말받기("boolean")) return 2;
        if (말받기("char")) return 5;
        if (말받기("FileInputStream")) return 6;
        if (말받기("FileOutputStream")) return 7;
        if (말받기("String")) { if (받기('[')) { 요구(']'); return 4; } return 3; }
        palelo_Boleng("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void tsenya_fometa(int tlanya_Boleng) {
        if (tlanya_Boleng == 0) 글추가('V');
        if (tlanya_Boleng == 1) 글추가('I');
        if (tlanya_Boleng == 2) 글추가('Z');
        if (tlanya_Boleng == 3) 말추가("Ljava/lang/String;");
        if (tlanya_Boleng == 4) 말추가("[Ljava/lang/String;");
        if (tlanya_Boleng == 5) 글추가('C');
        if (tlanya_Boleng == 6) 말추가("Ljava/io/FileInputStream;");
        if (tlanya_Boleng == 7) 말추가("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws 선언. 예외 Thulaganyo_Boleng_tsenyo 본문은 pinagare javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = 말받기("한국어");
        if (한국어묶음) { 요구('.'); 말요구("자체"); 요구('.'); }
        if (!한국어묶음 && (말받기("Exception") || 말받기("IOException"))) return;
        if (말받기("예외") || 말받기("실행예외") || 말받기("입출력예외") || 말받기("대기시간초과예외") || 말받기("주소확인예외") || 말받기("파일없음예외") || 말받기("통신예외") || 말받기("잘못된인수예외") || 말받기("숫자형식예외") || 말받기("범위예외") || 말받기("배열범위예외") || 말받기("문자열범위예외") || 말받기("빈참조예외") || 말받기("산술예외") || 말받기("상태예외") || 말받기("형변환예외") || 말받기("음수배열크기예외") || 말받기("setlhopha_Store_palelo") || 말받기("가닥상태예외") || 말받기("대기중단예외")) return;
        palelo_Boleng("unsupported throws type");
    }
    static void 선언읽기() {
        while (말받기("import")) {
            if (Lefoko_Boleng(위치, "한국어")) 예외이름읽기();
            else {
                말요구("java"); 요구('.'); 말요구("io"); 요구('.');
                if (!(말받기("FileInputStream") || 말받기("FileOutputStream") || 말받기("IOException"))) palelo_Boleng("unsupported import");
            }
            요구(';');
        }
        말받기("public"); 말받기("final"); 말요구("class"); mofuta_papetlana = setlhaodi_Boleng();
        mofuta_tlhomameng = Tshupiso(7, papetlana_tlhomameng(mofuta_papetlana), 0);
        부모상수 = Tshupiso(7, Lefoko_tlhomameng("java/lang/Object"), 0); 코드상수 = Lefoko_tlhomameng("Code"); 요구('{');
        while (!phoso && 종류() != '}') {
            if (함수수 == 32) { palelo_Boleng("too many methods"); break; }
            int letlelesega_tsenyo = 말받기("public") ? 1 : 말받기("private") ? 2 : 0; 말요구("static");
            int TIRISO_Boleng = 함수수++;
            mokgwa_letlelesega[TIRISO_Boleng] = letlelesega_tsenyo | 8;
            함수반환[TIRISO_Boleng] = fometa_Boleng(); mokgwa_tsenyo_leina[TIRISO_Boleng] = setlhaodi_Boleng(); 요구('(');
            for (int 앞 = 0; 앞 < TIRISO_Boleng; 앞++) if (이름같음(mokgwa_tsenyo_leina[앞], mokgwa_tsenyo_leina[TIRISO_Boleng])) palelo_Boleng("duplicate method (overloading unsupported)");
            while (!phoso && 종류() != ')') {
                int 수 = 함수인수수[TIRISO_Boleng];
                if (수 == 16) { palelo_Boleng("too many parameters"); break; }
                int tlanya_Boleng = fometa_Boleng(); if (tlanya_Boleng == 0) palelo_Boleng("void parameter");
                mokgwa_Thulaganyo_tlanya[TIRISO_Boleng * 16 + 수] = tlanya_Boleng; mokgwa_Thulaganyo_leina[TIRISO_Boleng * 16 + 수] = setlhaodi_Boleng();
                함수인수수[TIRISO_Boleng]++;
                if (!받기(',')) break;
            }
            요구(')');
            if (말받기("throws")) {
                do { 예외이름읽기(); } while (!phoso && 받기(','));
            }
            함수본문[TIRISO_Boleng] = 위치; 요구('{');
            int 중첩 = 1;
            while (위치 < 토큰수 && 중첩 > 0) {
                if (종류() == '{') 중첩++;
                if (종류() == '}') 중첩--;
                위치++;
            }
            if (중첩 != 0) palelo_Boleng("unclosed method body");
            mokgwa_kgaola[TIRISO_Boleng] = 위치;
            mokgwa_leina_tlhomameng[TIRISO_Boleng] = papetlana_tlhomameng(mokgwa_tsenyo_leina[TIRISO_Boleng]);
            Letshwao_boleele = 0; 글추가('(');
            for (int 수 = 0; 수 < 함수인수수[TIRISO_Boleng]; 수++) tsenya_fometa(mokgwa_Thulaganyo_tlanya[TIRISO_Boleng * 16 + 수]);
            글추가(')'); tsenya_fometa(함수반환[TIRISO_Boleng]); 함수서술[TIRISO_Boleng] = Letshwao_tlhomameng();
        }
        요구('}'); if (위치 != 토큰수) palelo_Boleng("extra input after class");
    }
    static int batla_e_e_gaufi(int leina) {
        for (int 수 = 지역수 - 1; 수 >= 0; 수--) if (지역깊이[수] >= 0 && 이름같음(e_e_gaufi_leina[수], leina)) return 수;
        palelo_Boleng("unknown variable"); return 0;
    }
    static int tsenya_e_e_gaufi(int leina, int tlanya_Boleng) {
        for (int 수 = 0; 수 < 지역수; 수++) if (지역깊이[수] >= 0 && 이름같음(e_e_gaufi_leina[수], leina)) palelo_Boleng("duplicate local variable");
        if (지역수 == 128) { palelo_Boleng("too many locals"); return 0; }
        e_e_gaufi_leina[지역수] = leina; e_e_gaufi_tlanya[지역수] = tlanya_Boleng; 지역깊이[지역수] = 깊이;
        return 지역수++;
    }
    static boolean Palotlalo_tlanya(int tlanya_Boleng) { return tlanya_Boleng == 1 || tlanya_Boleng == 5; }
    static void 지역읽기(int 수) { 내보내기(e_e_gaufi_tlanya[수] <= 2 || e_e_gaufi_tlanya[수] == 5 ? 21 : 25); 내보내기(수); }
    static void kwala_e_e_gaufi(int 수) { 내보내기(e_e_gaufi_tlanya[수] <= 2 || e_e_gaufi_tlanya[수] == 5 ? 54 : 58); 내보내기(수); }
    static void netefatsa_tlanya(int tota_tshedimosetso, int 기대) { if (tota_tshedimosetso != 기대 && !(tota_tshedimosetso == 5 && 기대 == 1)) palelo_Boleng("type mismatch"); }
    static void 문자읽기(int papetlana_Boleng) {
        Letshwao_boleele = 0; int dirisa = 토큰위치[papetlana_Boleng] + 1, 끝 = 토큰위치[papetlana_Boleng] + papetlana_boleele[papetlana_Boleng] - 1;
        while (dirisa < 끝 && !phoso) {
            int Boleng = Motswedi[dirisa++];
            if (Boleng == '\\') {
                if (dirisa == 끝) { palelo_Boleng("invalid escape"); break; }
                Boleng = Motswedi[dirisa++];
                if (Boleng == 'n') Boleng = 10;
                else if (Boleng == 'r') Boleng = 13;
                else if (Boleng == 't') Boleng = 9;
                else if (Boleng == 'b') Boleng = 8;
                else if (Boleng == 'f') Boleng = 12;
                else if (Boleng != '\\' && Boleng != '"' && Boleng != '\'') palelo_Boleng("unsupported escape");
            }
            글추가(Boleng);
        }
    }
    static int go_lokolola_Palotlalo(int papetlana_Boleng, boolean 음수) {
        if (papetlana_boleele[papetlana_Boleng] > 1 && Motswedi[토큰위치[papetlana_Boleng]] == '0') palelo_Boleng("octal literals unsupported");
        int Boleng = 0;
        for (int 수 = 0; 수 < papetlana_boleele[papetlana_Boleng]; 수++) {
            int dijite_selwana = Motswedi[토큰위치[papetlana_Boleng] + 수] - '0';
            if (Boleng < -214748364 || Boleng == -214748364 && dijite_selwana > (음수 ? 8 : 7)) palelo_Boleng("integer literal out of range");
            Boleng = Boleng * 10 - dijite_selwana;
        }
        return 음수 ? Boleng : -Boleng;
    }
    static int 기본식() {
        if (말받기("new")) {
            int tlanya_Boleng = fometa_Boleng();
            if (tlanya_Boleng != 6 && tlanya_Boleng != 7) { palelo_Boleng("only file streams supported by new in source"); return 0; }
            String mong_Boleng = tlanya_Boleng == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            Taelo(187, Tshupiso(7, Lefoko_tlhomameng(mong_Boleng), 0)); 내보내기(89);
            요구('('); netefatsa_tlanya(Tlhaloso_Boleng_eb3593ac(), 3); boolean 이어 = false;
            if (받기(',')) { if (tlanya_Boleng != 7) palelo_Boleng("input stream constructor arguments"); netefatsa_tlanya(Tlhaloso_Boleng_eb3593ac(), 2); 이어 = true; }
            요구(')');
            Taelo(183, 외부참조(10, mong_Boleng, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return tlanya_Boleng;
        }
        if (받기('(')) { int tlanya_Boleng = Tlhaloso_Boleng_eb3593ac(); 요구(')'); return tlanya_Boleng; }
        if (종류() == 257) { 수상수(go_lokolola_Palotlalo(위치++, false)); return 1; }
        if (종류() == 258) { 문자읽기(위치++); Taelo(19, Tshupiso(8, Letshwao_tlhomameng(), 0)); return 3; }
        if (종류() == 259) { 문자읽기(위치++); if (Letshwao_boleele != 1) palelo_Boleng("character literal length"); 수상수(문자[0]); return 5; }
        if (말받기("true")) { 내보내기(4); return 2; }
        if (말받기("false")) { 내보내기(3); return 2; }
        if (말받기("한국어")) {
            요구('.'); 말요구("자체"); 요구('.');
            String mong_Boleng = "", mokgwa_Boleng = "", 서술 = ""; int 가 = 0, 나 = 0, 다 = 0, 라 = 0, 마 = 0, 결과 = 0;
            if (말받기("출력")) {
                mong_Boleng = "한국어/자체/출력"; 요구('.');
                if (말받기("kwala_Mola")) { mokgwa_Boleng = "kwala_Mola"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (말받기("kwala")) { mokgwa_Boleng = "kwala"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (말받기("수쓰기")) { mokgwa_Boleng = "수쓰기"; 서술 = "(I)V"; 가 = 1; }
                else palelo_Boleng("unknown Korean output method");
            } else if (말받기("문자")) {
                mong_Boleng = "한국어/자체/문자"; 요구('.'); 가 = 3;
                if (말받기("boleele_Boleng")) { mokgwa_Boleng = "boleele_Boleng"; 서술 = "(Ljava/lang/String;)I"; 결과 = 1; }
                else if (말받기("코드포인트수")) { mokgwa_Boleng = "코드포인트수"; 서술 = "(Ljava/lang/String;)I"; 결과 = 1; }
                else if (말받기("go_lokolola_Palotlalo")) { mokgwa_Boleng = "go_lokolola_Palotlalo"; 서술 = "(Ljava/lang/String;)I"; 결과 = 1; }
                else if (말받기("kwala_Palotlalo_Boleng")) { mokgwa_Boleng = "kwala_Palotlalo_Boleng"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; 결과 = 3; }
                else if (말받기("같음")) { mokgwa_Boleng = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; 나 = 3; 결과 = 2; }
                else if (말받기("kgomaretsa_SMS")) { mokgwa_Boleng = "kgomaretsa_SMS"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; 나 = 3; 결과 = 3; }
                else if (말받기("sega_Boleng")) { mokgwa_Boleng = "sega_Boleng"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; 나 = 1; 다 = 1; 결과 = 3; }
                else palelo_Boleng("unknown Korean text method");
            } else if (말받기("faele")) {
                mong_Boleng = "한국어/자체/faele"; 요구('.'); 가 = 3;
                if (말받기("읽기")) { mokgwa_Boleng = "읽기"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; 결과 = 3; }
                else if (말받기("kwala")) { mokgwa_Boleng = "kwala"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; 나 = 3; }
                else palelo_Boleng("unknown Korean file method");
            } else if (말받기("화면")) {
                mong_Boleng = "한국어/자체/화면"; 요구('.');
                if (말받기("너비")) { mokgwa_Boleng = "너비"; 서술 = "()I"; 결과 = 1; }
                else if (말받기("높이")) { mokgwa_Boleng = "높이"; 서술 = "()I"; 결과 = 1; }
                else if (말받기("사각형")) { mokgwa_Boleng = "사각형"; 서술 = "(IIIII)V"; 가 = 1; 나 = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (말받기("지우기")) { mokgwa_Boleng = "지우기"; 서술 = "(I)V"; 가 = 1; }
                else if (말받기("기다리기")) { mokgwa_Boleng = "기다리기"; 서술 = "()V"; }
                else palelo_Boleng("unknown Korean framebuffer method");
            } else palelo_Boleng("unsupported Korean library class");
            요구('('); if (가 != 0) netefatsa_tlanya(Tlhaloso_Boleng_eb3593ac(), 가);
            if (나 != 0) { 요구(','); netefatsa_tlanya(Tlhaloso_Boleng_eb3593ac(), 나); }
            if (다 != 0) { 요구(','); netefatsa_tlanya(Tlhaloso_Boleng_eb3593ac(), 다); }
            if (라 != 0) { 요구(','); netefatsa_tlanya(Tlhaloso_Boleng_eb3593ac(), 라); }
            if (마 != 0) { 요구(','); netefatsa_tlanya(Tlhaloso_Boleng_eb3593ac(), 마); }
            요구(')'); Taelo(184, 외부참조(10, mong_Boleng, mokgwa_Boleng, 서술)); return 결과;
        }
        if (말받기("Integer")) {
            요구('.'); 말요구("parseInt"); 요구('('); netefatsa_tlanya(Tlhaloso_Boleng_eb3593ac(), 3); 요구(')');
            Taelo(184, 외부참조(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int leina = setlhaodi_Boleng();
        if (받기('(')) {
            int TIRISO_Boleng = -1;
            for (int 수 = 0; 수 < 함수수; 수++) if (이름같음(leina, mokgwa_tsenyo_leina[수])) TIRISO_Boleng = 수;
            if (TIRISO_Boleng < 0) { palelo_Boleng("unknown static method"); return 0; }
            int 수 = 0;
            while (!phoso && 종류() != ')') {
                if (수 >= 함수인수수[TIRISO_Boleng]) { palelo_Boleng("too many arguments"); break; }
                netefatsa_tlanya(Tlhaloso_Boleng_eb3593ac(), mokgwa_Thulaganyo_tlanya[TIRISO_Boleng * 16 + 수++]); if (!받기(',')) break;
            }
            요구(')'); if (수 != 함수인수수[TIRISO_Boleng]) palelo_Boleng("argument count mismatch");
            Taelo(184, Tshupiso(10, mofuta_tlhomameng, Tshupiso(12, mokgwa_leina_tlhomameng[TIRISO_Boleng], 함수서술[TIRISO_Boleng])));
            return 함수반환[TIRISO_Boleng];
        }
        int e_e_gaufi_Mothamo = batla_e_e_gaufi(leina), tlanya_Boleng = e_e_gaufi_tlanya[e_e_gaufi_Mothamo]; 지역읽기(e_e_gaufi_Mothamo);
        while (!phoso) {
            if (받기('[')) { netefatsa_tlanya(tlanya_Boleng, 4); netefatsa_tlanya(Tlhaloso_Boleng_eb3593ac(), 1); 요구(']'); 내보내기(50); tlanya_Boleng = 3; }
            else if (받기('.')) {
                if (tlanya_Boleng == 6 || tlanya_Boleng == 7) {
                    String mong_Boleng = tlanya_Boleng == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (말받기("close")) { 요구('('); 요구(')'); Taelo(182, 외부참조(10, mong_Boleng, "close", "()V")); tlanya_Boleng = 0; }
                    else if (tlanya_Boleng == 6 && 말받기("read")) { 요구('('); 요구(')'); Taelo(182, 외부참조(10, mong_Boleng, "read", "()I")); tlanya_Boleng = 1; }
                    else if (tlanya_Boleng == 7 && 말받기("write")) { 요구('('); netefatsa_tlanya(Tlhaloso_Boleng_eb3593ac(), 1); 요구(')'); Taelo(182, 외부참조(10, mong_Boleng, "write", "(I)V")); tlanya_Boleng = 0; }
                    else { palelo_Boleng("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (tlanya_Boleng == 4) { 내보내기(190); tlanya_Boleng = 1; }
                else { netefatsa_tlanya(tlanya_Boleng, 3); 요구('('); 요구(')'); Taelo(182, 외부참조(10, "java/lang/String", "length", "()I")); tlanya_Boleng = 1; }
            } else break;
        }
        return tlanya_Boleng;
    }
    static int 단항() {
        if (++식깊이 > 64) { palelo_Boleng("expression nesting too deep"); 식깊이--; return 0; }
        int tlanya_Boleng;
        if (받기('!')) { netefatsa_tlanya(단항(), 2); 비교값(153); tlanya_Boleng = 2; }
        else if (받기('-')) {
            if (종류() == 257) 수상수(go_lokolola_Palotlalo(위치++, true));
            else { netefatsa_tlanya(단항(), 1); 내보내기(116); }
            tlanya_Boleng = 1;
        } else if (받기('+')) { netefatsa_tlanya(단항(), 1); tlanya_Boleng = 1; }
        else tlanya_Boleng = 기본식();
        식깊이--; return tlanya_Boleng;
    }
    static int 곱식() {
        int tlanya_Boleng = 단항();
        while (!phoso && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int khoutufatso_Boleng = 종류(); 위치++; netefatsa_tlanya(tlanya_Boleng, 1); netefatsa_tlanya(단항(), 1);
            내보내기(khoutufatso_Boleng == '*' ? 104 : khoutufatso_Boleng == '/' ? 108 : 112); tlanya_Boleng = 1;
        }
        return tlanya_Boleng;
    }
    static int 합식() {
        int tlanya_Boleng = 곱식();
        while (!phoso && (종류() == '+' || 종류() == '-')) {
            int khoutufatso_Boleng = 종류(); 위치++; int 경계 = 코드크기, Morago_Boleng_tlanya = 곱식();
            if (khoutufatso_Boleng == '+' && (tlanya_Boleng == 3 || Morago_Boleng_tlanya == 3)) { 결합(경계, tlanya_Boleng, Morago_Boleng_tlanya); tlanya_Boleng = 3; }
            else { netefatsa_tlanya(tlanya_Boleng, 1); netefatsa_tlanya(Morago_Boleng_tlanya, 1); 내보내기(khoutufatso_Boleng == '+' ? 96 : 100); tlanya_Boleng = 1; }
        }
        return tlanya_Boleng;
    }
    static int 붙임참조(int tlanya_Boleng) {
        if (tlanya_Boleng != 1 && tlanya_Boleng != 2 && tlanya_Boleng != 3 && tlanya_Boleng != 5) palelo_Boleng("unsupported concatenation type");
        return 외부참조(10, "java/lang/StringBuilder", "append", tlanya_Boleng == 1 ? "(I)Ljava/lang/StringBuilder;"
            : tlanya_Boleng == 2 ? "(Z)Ljava/lang/StringBuilder;" : tlanya_Boleng == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int 경계, int 앞형, int Morago_Boleng_tlanya) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 오른쪽 코드 앞에 생성 코드를 삽입한다.
        // 오른쪽 Tlhaloso_Boleng_eb3593ac 내부의 semphato_Boleng lekala 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = 코드크기;
        Taelo(187, Tshupiso(7, Lefoko_tlhomameng("java/lang/StringBuilder"), 0)); 내보내기(89);
        Taelo(183, 외부참조(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); Taelo(182, 붙임참조(앞형));
        if (phoso) return;
        int boleele_Boleng = 코드크기 - 끝;
        for (int 수 = 0; 수 < boleele_Boleng; 수++) 삽입코드[수] = 코드[끝 + 수];
        for (int 수 = 끝 - 1; 수 >= 경계; 수--) 코드[수 + boleele_Boleng] = 코드[수];
        for (int 수 = 0; 수 < boleele_Boleng; 수++) 코드[경계 + 수] = 삽입코드[수];
        Taelo(182, 붙임참조(Morago_Boleng_tlanya)); Taelo(182, 외부참조(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int 비교식() {
        int tlanya_Boleng = 합식();
        while (!phoso && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int khoutufatso_Boleng = 종류(); 위치++; netefatsa_tlanya(tlanya_Boleng, 1); netefatsa_tlanya(합식(), 1);
            비교값(khoutufatso_Boleng == '<' ? 161 : khoutufatso_Boleng == '>' ? 163 : khoutufatso_Boleng == 302 ? 164 : 162); tlanya_Boleng = 2;
        }
        return tlanya_Boleng;
    }
    static int 동등식() {
        int tlanya_Boleng = 비교식();
        while (!phoso && (종류() == 300 || 종류() == 301)) {
            int khoutufatso_Boleng = 종류(); 위치++; int Morago_Boleng_tlanya = 비교식();
            if (tlanya_Boleng == 0 || Morago_Boleng_tlanya == 0) palelo_Boleng("void expression");
            if (!(Palotlalo_tlanya(tlanya_Boleng) && Palotlalo_tlanya(Morago_Boleng_tlanya))) netefatsa_tlanya(Morago_Boleng_tlanya, tlanya_Boleng);
            비교값((tlanya_Boleng <= 2 || tlanya_Boleng == 5 ? 159 : 165) + (khoutufatso_Boleng == 301 ? 1 : 0)); tlanya_Boleng = 2;
        }
        return tlanya_Boleng;
    }
    static int 논리곱() {
        int tlanya_Boleng = 동등식();
        while (!phoso && 받기(304)) {
            netefatsa_tlanya(tlanya_Boleng, 2); int 가 = lekala(153); netefatsa_tlanya(동등식(), 2); int 나 = lekala(153);
            내보내기(4); int 끝 = lekala(167); Kgokagano_Boleng(가, 코드크기); Kgokagano_Boleng(나, 코드크기); 내보내기(3); Kgokagano_Boleng(끝, 코드크기); tlanya_Boleng = 2;
        }
        return tlanya_Boleng;
    }
    static int Tlhaloso_Boleng_eb3593ac() {
        int tlanya_Boleng = 논리곱();
        while (!phoso && 받기(305)) {
            netefatsa_tlanya(tlanya_Boleng, 2); int 가 = lekala(154); netefatsa_tlanya(논리곱(), 2); int 나 = lekala(154);
            내보내기(3); int 끝 = lekala(167); Kgokagano_Boleng(가, 코드크기); Kgokagano_Boleng(나, 코드크기); 내보내기(4); Kgokagano_Boleng(끝, 코드크기); tlanya_Boleng = 2;
        }
        return tlanya_Boleng;
    }
    static void kabelotiro_Boleng(boolean 선언허용) {
        if (Lefoko_Boleng(위치, "int") || Lefoko_Boleng(위치, "boolean") || Lefoko_Boleng(위치, "String") || Lefoko_Boleng(위치, "char")
            || Lefoko_Boleng(위치, "FileInputStream") || Lefoko_Boleng(위치, "FileOutputStream")) {
            if (!선언허용) palelo_Boleng("declaration not allowed here");
            int tlanya_Boleng = fometa_Boleng(), leina = setlhaodi_Boleng(); 요구('='); netefatsa_tlanya(Tlhaloso_Boleng_eb3593ac(), tlanya_Boleng);
            kwala_e_e_gaufi(tsenya_e_e_gaufi(leina, tlanya_Boleng)); return;
        }
        int leina = setlhaodi_Boleng(), e_e_gaufi_Mothamo = batla_e_e_gaufi(leina);
        if (받기('=')) { netefatsa_tlanya(Tlhaloso_Boleng_eb3593ac(), e_e_gaufi_tlanya[e_e_gaufi_Mothamo]); kwala_e_e_gaufi(e_e_gaufi_Mothamo); }
        else if (종류() >= 308 && 종류() <= 312) {
            int khoutufatso_Boleng = 종류(); 위치++; 지역읽기(e_e_gaufi_Mothamo); int 경계 = 코드크기, Morago_Boleng_tlanya = Tlhaloso_Boleng_eb3593ac();
            if (khoutufatso_Boleng == 308 && e_e_gaufi_tlanya[e_e_gaufi_Mothamo] == 3) 결합(경계, 3, Morago_Boleng_tlanya);
            else {
                netefatsa_tlanya(e_e_gaufi_tlanya[e_e_gaufi_Mothamo], 1); netefatsa_tlanya(Morago_Boleng_tlanya, 1);
                내보내기(khoutufatso_Boleng == 308 ? 96 : khoutufatso_Boleng == 309 ? 100 : khoutufatso_Boleng == 310 ? 104 : khoutufatso_Boleng == 311 ? 108 : 112);
                if (e_e_gaufi_tlanya[e_e_gaufi_Mothamo] == 5) 내보내기(146);
            }
            kwala_e_e_gaufi(e_e_gaufi_Mothamo);
        }
        else if (종류() == 306 || 종류() == 307) {
            netefatsa_tlanya(e_e_gaufi_tlanya[e_e_gaufi_Mothamo], 1); 내보내기(132); 내보내기(e_e_gaufi_Mothamo); 내보내기(종류() == 306 ? 1 : 255); 위치++;
            if (e_e_gaufi_tlanya[e_e_gaufi_Mothamo] == 5) { 지역읽기(e_e_gaufi_Mothamo); 내보내기(146); kwala_e_e_gaufi(e_e_gaufi_Mothamo); }
        } else palelo_Boleng("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); 요구('.'); 말요구("out"); 요구('.');
        boolean 줄바꿈 = 말받기("println"); if (!줄바꿈) 말요구("print"); 요구('(');
        Taelo(178, 외부참조(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean lolea_Thulaganyo = 종류() == ')';
        int tlanya_Boleng = lolea_Thulaganyo ? 0 : Tlhaloso_Boleng_eb3593ac(); 요구(')'); 요구(';');
        String 서술 = tlanya_Boleng == 0 ? "()V" : tlanya_Boleng == 1 ? "(I)V" : tlanya_Boleng == 2 ? "(Z)V" : tlanya_Boleng == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (tlanya_Boleng == 4 || tlanya_Boleng >= 6 || tlanya_Boleng == 0 && (!줄바꿈 || !lolea_Thulaganyo)) palelo_Boleng("unsupported print argument");
        Taelo(182, 외부참조(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean polelo_Boleng() {
        if (phoso) return false;
        if (깊이 > 32) { palelo_Boleng("statement nesting too deep"); return false; }
        if (받기('{')) {
            깊이++; boolean 반환 = false;
            while (!phoso && 종류() != '}') { if (반환) palelo_Boleng("unreachable statement"); 반환 = polelo_Boleng(); }
            요구('}'); for (int 수 = 0; 수 < 지역수; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return 반환;
        }
        if (받기(';')) return false;
        if (말받기("return")) {
            int tlanya_Boleng = 종류() == ';' ? 0 : Tlhaloso_Boleng_eb3593ac(); netefatsa_tlanya(tlanya_Boleng, 함수반환[ga_jaana_mokgwa]); 요구(';');
            내보내기(tlanya_Boleng == 0 ? 177 : tlanya_Boleng <= 2 || tlanya_Boleng == 5 ? 172 : 176); return true;
        }
        if (말받기("if")) {
            요구('('); netefatsa_tlanya(Tlhaloso_Boleng_eb3593ac(), 2); 요구(')'); int 거짓 = lekala(153);
            깊이++; boolean 가 = taolo_polelo(); 깊이--;
            if (말받기("else")) { int 끝 = lekala(167); Kgokagano_Boleng(거짓, 코드크기); 깊이++; boolean 나 = taolo_polelo(); 깊이--; Kgokagano_Boleng(끝, 코드크기); return 가 && 나; }
            Kgokagano_Boleng(거짓, 코드크기); return false;
        }
        if (말받기("while")) {
            int dirisa = 코드크기; 요구('('); netefatsa_tlanya(Tlhaloso_Boleng_eb3593ac(), 2); 요구(')'); int 끝 = lekala(153);
            깊이++; taolo_polelo(); 깊이--; Kgokagano_Boleng(lekala(167), dirisa); Kgokagano_Boleng(끝, 코드크기); return false;
        }
        if (말받기("for")) {
            깊이++; 요구('('); if (종류() != ';') kabelotiro_Boleng(true); 요구(';');
            int boemo = 코드크기; if (종류() == ';') 내보내기(4); else netefatsa_tlanya(Tlhaloso_Boleng_eb3593ac(), 2); 요구(';');
            int 끝 = lekala(153), diteng_tsa_mokwalo = lekala(167), Tsosolosa = 코드크기;
            if (종류() != ')') kabelotiro_Boleng(false); 요구(')'); Kgokagano_Boleng(lekala(167), boemo); Kgokagano_Boleng(diteng_tsa_mokwalo, 코드크기);
            taolo_polelo(); Kgokagano_Boleng(lekala(167), Tsosolosa); Kgokagano_Boleng(끝, 코드크기);
            for (int 수 = 0; 수 < 지역수; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return false;
        }
        if (Lefoko_Boleng(위치, "System")) { 화면출력(); return false; }
        if (종류() == 256 && 위치 + 1 < 토큰수 && (토큰종류[위치 + 1] == '(' || 토큰종류[위치 + 1] == '.')) {
            int tlanya_Boleng = Tlhaloso_Boleng_eb3593ac(); if (tlanya_Boleng != 0) 내보내기(87); 요구(';'); return false;
        }
        kabelotiro_Boleng(true); 요구(';'); return false;
    }
    static boolean taolo_polelo() {
        if (Lefoko_Boleng(위치, "int") || Lefoko_Boleng(위치, "boolean") || Lefoko_Boleng(위치, "char") || Lefoko_Boleng(위치, "String")
            || Lefoko_Boleng(위치, "FileInputStream") || Lefoko_Boleng(위치, "FileOutputStream")) palelo_Boleng("local declaration requires braces");
        return polelo_Boleng();
    }
    static void 출바(int Boleng) { if (출력크기 == 출력.length) palelo_Boleng("class file too large"); else 출력[출력크기++] = Boleng & 255; }
    static void 출짧(int Boleng) { 출바(Boleng >> 8); 출바(Boleng); }
    static void 출정(int Boleng) { 출짧(Boleng >>> 16); 출짧(Boleng); }
    static void kwala_mofuta() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(상수수);
        for (int 수 = 0; 수 < tlhomameng_lekanya; 수++) 출바(tlhomameng_Boleng[수]);
        출짧(0x21); 출짧(mofuta_tlhomameng); 출짧(부모상수); 출짧(0); 출짧(0); 출짧(함수수);
        for (int 수 = 0; 수 < 함수수; 수++) {
            출짧(mokgwa_letlelesega[수]); 출짧(mokgwa_leina_tlhomameng[수]); 출짧(함수서술[수]); 출짧(1); 출짧(코드상수);
            출정(12 + mokgwa_boleele[수]); 출짧(128); 출짧(함수지역[수]); 출정(mokgwa_boleele[수]);
            for (int sebaka_tsenyo = 0; sebaka_tsenyo < mokgwa_boleele[수]; sebaka_tsenyo++) 출바(코드[함수코드[수] + sebaka_tsenyo]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int dirisa() {
        if (modirisi.인수개수() == 1 && 자바도구.같음(modirisi.인수(0), "-version")) {
            modirisi.kwala("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (modirisi.인수개수() != 1) { modirisi.kwala("Usage: javac FILE.java\n"); return 2; }
        int leina_lekanya = 자바도구.leina(faele_leina_SMS, modirisi.인수(0));
        if (leina_lekanya < 6 || leina_lekanya > 62 || faele_leina_SMS[leina_lekanya - 5] != '.' || faele_leina_SMS[leina_lekanya - 4] != 'j'
            || faele_leina_SMS[leina_lekanya - 3] != 'a' || faele_leina_SMS[leina_lekanya - 2] != 'v' || faele_leina_SMS[leina_lekanya - 1] != 'a') {
            modirisi.kwala("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        Motswedi_lekanya = modirisi.파일읽기(faele_leina_SMS, Motswedi);
        if (Motswedi_lekanya < 0) { modirisi.kwala("javac: cannot read source: "); 자바도구.수쓰기(Motswedi_lekanya); modirisi.kwala_Letshwao_Boleng(10); return 1; }
        Motswedi_lekanya = 자바도구.원문해독(Motswedi, Motswedi_lekanya);
        if (Motswedi_lekanya < 0) { modirisi.kwala("javac error: invalid UTF-8 source\n"); return 1; }
        sega_Boleng(); if (!phoso) 선언읽기();
        if (!phoso) {
            if (papetlana_boleele[mofuta_papetlana] != leina_lekanya - 5) palelo_Boleng("class name must match file name");
            for (int 수 = 0; 수 < leina_lekanya - 5; 수++) if (Motswedi[토큰위치[mofuta_papetlana] + 수] != faele_leina_SMS[수]) palelo_Boleng("class name must match file name");
        }
        for (ga_jaana_mokgwa = 0; ga_jaana_mokgwa < 함수수 && !phoso; ga_jaana_mokgwa++) {
            위치 = 함수본문[ga_jaana_mokgwa]; 함수코드[ga_jaana_mokgwa] = 코드크기; 지역수 = 0; 깊이 = 0;
            for (int 수 = 0; 수 < 함수인수수[ga_jaana_mokgwa]; 수++) tsenya_e_e_gaufi(mokgwa_Thulaganyo_leina[ga_jaana_mokgwa * 16 + 수], mokgwa_Thulaganyo_tlanya[ga_jaana_mokgwa * 16 + 수]);
            boolean 반환 = polelo_Boleng();
            if (!반환 && 함수반환[ga_jaana_mokgwa] != 0) palelo_Boleng("missing return");
            // lekala 뒤의 합류 지점은 반드시 tota_tshedimosetso 명령이어야 한다 (버전 49 검증기).
            if (함수반환[ga_jaana_mokgwa] == 0) 내보내기(177);
            else { boolean Palotlalo = 함수반환[ga_jaana_mokgwa] <= 2 || 함수반환[ga_jaana_mokgwa] == 5; 내보내기(Palotlalo ? 3 : 1); 내보내기(Palotlalo ? 172 : 176); }
            if (위치 != mokgwa_kgaola[ga_jaana_mokgwa]) palelo_Boleng("invalid method body");
            함수지역[ga_jaana_mokgwa] = 지역수; mokgwa_boleele[ga_jaana_mokgwa] = 코드크기 - 함수코드[ga_jaana_mokgwa];
        }
        if (phoso) return 1;
        kwala_mofuta(); if (phoso) return 1;
        faele_leina_SMS[leina_lekanya - 4] = 'c'; faele_leina_SMS[leina_lekanya - 3] = 'l'; faele_leina_SMS[leina_lekanya - 2] = 'a';
        faele_leina_SMS[leina_lekanya - 1] = 's'; faele_leina_SMS[leina_lekanya] = 's'; faele_leina_SMS[leina_lekanya + 1] = 0;
        int 결과 = modirisi.kwala_faele(faele_leina_SMS, 출력, 출력크기);
        if (결과 < 0) { modirisi.kwala("javac: cannot save class: "); 자바도구.수쓰기(결과); modirisi.kwala_Letshwao_Boleng(10); return 1; }
        modirisi.kwala("Compiled: "); for (int 수 = 0; faele_leina_SMS[수] != 0; 수++) modirisi.kwala_Letshwao_Boleng(faele_leina_SMS[수]);
        modirisi.kwala(" (JVM class version 49)\n"); return 0;
    }
}
