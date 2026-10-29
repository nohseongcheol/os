// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java manba_daraxt -> 표준 버전 49 class 컴파일러. */
public final class 자바컴파일러 {
    static int[] manba = new int[16384], 출력 = new int[16384], kod_VALUE = new int[4096];
    static int[] 토큰종류 = new int[2048], token_holat = new int[2048], token_uzunlik = new int[2048];
    static int[] konstanta_VALUE = new int[4096], konstanta_OFFSET = new int[512];
    static int[] 문자 = new int[512], fayl_nom_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int manba_o_lcham, token_COUNT, Holati, kod_o_lcham, konstanta_o_lcham, konstanta_COUNT = 1, 출력크기, belgi_uzunlik;
    static boolean Xato;
    static int Sinf_token, Sinf_konstanta, 부모상수, kod_konstanta;
    static int[] uslub_kiritish_nom = new int[32], uslub_qaytarish = new int[32], uslub_dalil_COUNT = new int[32];
    static int[] uslub_dalil_nom = new int[512], uslub_dalil_TYPE = new int[512];
    static int[] 함수본문 = new int[32], uslub_to_xtatmoq = new int[32], uslub_kod = new int[32];
    static int[] uslub_uzunlik = new int[32], 함수지역 = new int[32], uslub_nom_konstanta = new int[32], 함수서술 = new int[32];
    static int[] uslub_kirish_huquqi = new int[32];
    static int uslub_COUNT, 현재함수, mahalliy_COUNT, 깊이, 식깊이;
    static int[] mahalliy_nom = new int[128], mahalliy_TYPE = new int[128], 지역깊이 = new int[128];

    static void to_xtab_qolish_VALUE(String 이유) {
        if (!Xato) {
            foydalanuvchi.Yozish("javac error: "); foydalanuvchi.Yozish(이유);
            foydalanuvchi.Yozish(" at line ");
            int satr = 1, 끝 = Holati < token_COUNT ? token_holat[Holati] : manba_o_lcham;
            for (int 수 = 0; 수 < 끝; 수++) if (manba[수] == 10) satr++;
            자바도구.수쓰기(satr); foydalanuvchi.yozmoq_belgi_VALUE(10);
        }
        Xato = true;
    }
    static boolean belgi_VALUE(int VALUE) { return 문자이름규칙.첫글자(VALUE); }
    static boolean raqam_VALUE(int VALUE) { return VALUE >= '0' && VALUE <= '9'; }
    static boolean 이름같음(int 가, int 나) {
        if (가 < 0 || 나 < 0 || 가 >= token_COUNT || 나 >= token_COUNT || token_uzunlik[가] != token_uzunlik[나]) return false;
        for (int 수 = 0; 수 < token_uzunlik[가]; 수++) if (manba[token_holat[가] + 수] != manba[token_holat[나] + 수]) return false;
        return true;
    }
    static boolean Word_VALUE(int token_VALUE, String Word_SMS) {
        if (token_VALUE < 0 || token_VALUE >= token_COUNT || token_uzunlik[token_VALUE] != Word_SMS.length()) return false;
        for (int 수 = 0; 수 < Word_SMS.length(); 수++) if (manba[token_holat[token_VALUE] + 수] != Word_SMS.charAt(수)) return false;
        return true;
    }
    static int 종류() { return Holati < token_COUNT ? 토큰종류[Holati] : 0; }
    static boolean 받기(int VALUE) { if (종류() != VALUE) return false; Holati++; return true; }
    static void 요구(int VALUE) { if (!받기(VALUE)) to_xtab_qolish_VALUE("unexpected token"); }
    static boolean TAKE_Word(String Word_SMS) { if (!Word_VALUE(Holati, Word_SMS)) return false; Holati++; return true; }
    static void 말요구(String Word_SMS) { if (!TAKE_Word(Word_SMS)) to_xtab_qolish_VALUE(Word_SMS); }
    static int identifikator_VALUE() {
        int o_lchov = Holati;
        if (종류() != 256) to_xtab_qolish_VALUE("identifier required"); else Holati++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int Bajarish = 0;
        for (int 수 = 0; 수 <= 예약어.length(); 수++) {
            if (수 == 예약어.length() || 예약어.charAt(수) == ' ') {
                boolean 같음 = 수 - Bajarish == token_uzunlik[o_lchov];
                for (int in_kiritish = Bajarish; 같음 && in_kiritish < 수; in_kiritish++) if (예약어.charAt(in_kiritish) != manba[token_holat[o_lchov] + in_kiritish - Bajarish]) 같음 = false;
                if (같음) to_xtab_qolish_VALUE("reserved word cannot be an identifier");
                Bajarish = 수 + 1;
            }
        }
        return o_lchov;
    }
    static void qirqmoq_VALUE() {
        int 수 = 0;
        while (수 < manba_o_lcham && !Xato) {
            int VALUE = manba[수], Bajarish = 수, 종류 = VALUE;
            if (VALUE == 32 || VALUE == 9 || VALUE == 10 || VALUE == 13) { 수++; continue; }
            if (VALUE == '/' && 수 + 1 < manba_o_lcham && manba[수 + 1] == '/') {
                while (수 < manba_o_lcham && manba[수] != 10) 수++;
                continue;
            }
            if (VALUE == '/' && 수 + 1 < manba_o_lcham && manba[수 + 1] == '*') {
                수 += 2;
                while (수 + 1 < manba_o_lcham && !(manba[수] == '*' && manba[수 + 1] == '/')) 수++;
                if (수 + 1 >= manba_o_lcham) { to_xtab_qolish_VALUE("unterminated comment"); break; }
                수 += 2; continue;
            }
            if (belgi_VALUE(VALUE)) { 종류 = 256; while (수 < manba_o_lcham && 문자이름규칙.이어진글자(manba[수])) 수++; }
            else if (raqam_VALUE(VALUE)) { 종류 = 257; while (수 < manba_o_lcham && raqam_VALUE(manba[수])) 수++; }
            else if (VALUE == '"' || VALUE == '\'') {
                종류 = VALUE == '"' ? 258 : 259; 수++;
                while (수 < manba_o_lcham && manba[수] != VALUE && manba[수] != 10 && manba[수] != 13) {
                    if (manba[수] == '\\') 수++;
                    수++;
                }
                if (수 >= manba_o_lcham || manba[수] != VALUE) { to_xtab_qolish_VALUE("unterminated literal"); break; }
                수++;
            } else {
                수++;
                if (수 < manba_o_lcham) {
                    int Keyingi_element = manba[수];
                    if (VALUE == '=' && Keyingi_element == '=') 종류 = 300;
                    if (VALUE == '!' && Keyingi_element == '=') 종류 = 301;
                    if (VALUE == '<' && Keyingi_element == '=') 종류 = 302;
                    if (VALUE == '>' && Keyingi_element == '=') 종류 = 303;
                    if (VALUE == '&' && Keyingi_element == '&') 종류 = 304;
                    if (VALUE == '|' && Keyingi_element == '|') 종류 = 305;
                    if (VALUE == '+' && Keyingi_element == '+') 종류 = 306;
                    if (VALUE == '-' && Keyingi_element == '-') 종류 = 307;
                    if (VALUE == '+' && Keyingi_element == '=') 종류 = 308;
                    if (VALUE == '-' && Keyingi_element == '=') 종류 = 309;
                    if (VALUE == '*' && Keyingi_element == '=') 종류 = 310;
                    if (VALUE == '/' && Keyingi_element == '=') 종류 = 311;
                    if (VALUE == '%' && Keyingi_element == '=') 종류 = 312;
                    if (종류 >= 300) 수++;
                }
            }
            if (token_COUNT == 토큰종류.length - 1) { to_xtab_qolish_VALUE("too many tokens (2047 maximum)"); break; }
            토큰종류[token_COUNT] = 종류; token_holat[token_COUNT] = Bajarish; token_uzunlik[token_COUNT++] = 수 - Bajarish;
        }
    }
    static void yozmoq_konstanta_bayt(int VALUE) {
        if (konstanta_o_lcham == konstanta_VALUE.length) { to_xtab_qolish_VALUE("constant pool too large"); return; }
        konstanta_VALUE[konstanta_o_lcham++] = VALUE & 255;
    }
    static void 상짧(int VALUE) { yozmoq_konstanta_bayt(VALUE >> 8); yozmoq_konstanta_bayt(VALUE); }
    static int 상등록(int Bajarish) {
        for (int 수 = 1; 수 < konstanta_COUNT; 수++) {
            int old_kamera_VALUE = konstanta_OFFSET[수], uzunlik_VALUE = (수 + 1 < konstanta_COUNT ? konstanta_OFFSET[수 + 1] : Bajarish) - old_kamera_VALUE;
            if (uzunlik_VALUE != konstanta_o_lcham - Bajarish) continue;
            boolean 같음 = true;
            for (int in_kiritish = 0; in_kiritish < uzunlik_VALUE; in_kiritish++) if (konstanta_VALUE[old_kamera_VALUE + in_kiritish] != konstanta_VALUE[Bajarish + in_kiritish]) 같음 = false;
            if (같음) { konstanta_o_lcham = Bajarish; return 수; }
        }
        if (konstanta_COUNT == konstanta_OFFSET.length) { to_xtab_qolish_VALUE("too many constants"); return 0; }
        konstanta_OFFSET[konstanta_COUNT] = Bajarish;
        return konstanta_COUNT++;
    }
    static void 글추가(int VALUE) {
        if (belgi_uzunlik == 문자.length) { to_xtab_qolish_VALUE("text too long"); return; }
        문자[belgi_uzunlik++] = VALUE;
    }
    static void 말추가(String Word_SMS) { for (int 수 = 0; 수 < Word_SMS.length(); 수++) 글추가(Word_SMS.charAt(수)); }
    static int belgi_konstanta() {
        int Bajarish = konstanta_o_lcham; yozmoq_konstanta_bayt(1); 상짧(0);
        for (int 수 = 0; 수 < belgi_uzunlik; 수++) {
            int VALUE = 문자[수];
            if (VALUE > 0 && VALUE < 128) yozmoq_konstanta_bayt(VALUE);
            else if (VALUE < 2048) { yozmoq_konstanta_bayt(192 | VALUE >> 6); yozmoq_konstanta_bayt(128 | VALUE & 63); }
            else { yozmoq_konstanta_bayt(224 | VALUE >> 12); yozmoq_konstanta_bayt(128 | VALUE >> 6 & 63); yozmoq_konstanta_bayt(128 | VALUE & 63); }
        }
        if (Xato) return 0;
        int uzunlik_VALUE = konstanta_o_lcham - Bajarish - 3;
        konstanta_VALUE[Bajarish + 1] = uzunlik_VALUE >> 8; konstanta_VALUE[Bajarish + 2] = uzunlik_VALUE & 255;
        return 상등록(Bajarish);
    }
    static int Word_konstanta(String Word_SMS) { belgi_uzunlik = 0; 말추가(Word_SMS); return belgi_konstanta(); }
    static int token_konstanta(int token_VALUE) {
        belgi_uzunlik = 0;
        for (int 수 = 0; 수 < token_uzunlik[token_VALUE]; 수++) 글추가(manba[token_holat[token_VALUE] + 수]);
        return belgi_konstanta();
    }
    static int Ma_lumotnomalar(int 종류, int 가, int 나) {
        int Bajarish = konstanta_o_lcham; yozmoq_konstanta_bayt(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(나);
        return 상등록(Bajarish);
    }
    static int 외부참조(int 종류, String egasi_VALUE, String Nomi, String 서술) {
        int egasi_identifikator = Ma_lumotnomalar(7, Word_konstanta(egasi_VALUE), 0);
        int nom_COUNT = Word_konstanta(Nomi), format_COUNT = Word_konstanta(서술);
        return Ma_lumotnomalar(종류, egasi_identifikator, Ma_lumotnomalar(12, nom_COUNT, format_COUNT));
    }
    static void 내보내기(int VALUE) {
        if (kod_o_lcham == kod_VALUE.length) { to_xtab_qolish_VALUE("bytecode too large"); return; }
        kod_VALUE[kod_o_lcham++] = VALUE & 255;
    }
    static void Buyruq(int VALUE, int 인수) { 내보내기(VALUE); 내보내기(인수 >> 8); 내보내기(인수); }
    static void 수상수(int VALUE) {
        if (VALUE >= -1 && VALUE <= 5) { 내보내기(VALUE + 3); return; }
        int Bajarish = konstanta_o_lcham; yozmoq_konstanta_bayt(3); 상짧(VALUE >>> 16); 상짧(VALUE);
        Buyruq(19, 상등록(Bajarish));
    }
    static int shox(int Buyruq) { int o_lchov = kod_o_lcham; Buyruq(Buyruq, 0); return o_lchov; }
    static void ulash_VALUE(int shox, int maqsad_obyekt) {
        if (Xato) return;
        int 거리 = maqsad_obyekt - shox;
        if (거리 < -32768 || 거리 > 32767 || shox < 0 || shox + 2 >= kod_o_lcham) { to_xtab_qolish_VALUE("invalid branch"); return; }
        kod_VALUE[shox + 1] = 거리 >> 8 & 255; kod_VALUE[shox + 2] = 거리 & 255;
    }
    static void Taqqoslama_VALUE(int Buyruq) {
        int TRUE_VALUE = shox(Buyruq); 내보내기(3); int 끝 = shox(167);
        ulash_VALUE(TRUE_VALUE, kod_o_lcham); 내보내기(4); ulash_VALUE(끝, kod_o_lcham);
    }
    static int format_VALUE() {
        if (TAKE_Word("void")) return 0;
        if (TAKE_Word("int")) return 1;
        if (TAKE_Word("boolean")) return 2;
        if (TAKE_Word("char")) return 5;
        if (TAKE_Word("FileInputStream")) return 6;
        if (TAKE_Word("FileOutputStream")) return 7;
        if (TAKE_Word("String")) { if (받기('[')) { 요구(']'); return 4; } return 3; }
        to_xtab_qolish_VALUE("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void qo_shmoq_format(int TYPE_VALUE) {
        if (TYPE_VALUE == 0) 글추가('V');
        if (TYPE_VALUE == 1) 글추가('I');
        if (TYPE_VALUE == 2) 글추가('Z');
        if (TYPE_VALUE == 3) 말추가("Ljava/lang/String;");
        if (TYPE_VALUE == 4) 말추가("[Ljava/lang/String;");
        if (TYPE_VALUE == 5) 글추가('C');
        if (TYPE_VALUE == 6) 말추가("Ljava/io/FileInputStream;");
        if (TYPE_VALUE == 7) 말추가("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws e_lon_qilish. istisno Jarayon_VALUE_kiritish 본문은 tashkilotchi javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = TAKE_Word("한국어");
        if (한국어묶음) { 요구('.'); 말요구("자체"); 요구('.'); }
        if (!한국어묶음 && (TAKE_Word("Exception") || TAKE_Word("IOException"))) return;
        if (TAKE_Word("istisno") || TAKE_Word("실행예외") || TAKE_Word("I_O_istisno") || TAKE_Word("bir_daqiqa_TANAFFUS_istisno") || TAKE_Word("manzil_LOOKUP_istisno") || TAKE_Word("파일없음예외") || TAKE_Word("통신예외") || TAKE_Word("xato_dalil_istisno") || TAKE_Word("숫자형식예외") || TAKE_Word("범위예외") || TAKE_Word("배열범위예외") || TAKE_Word("문자열범위예외") || TAKE_Word("nul_Ma_lumotnomalar_istisno") || TAKE_Word("산술예외") || TAKE_Word("holat_istisno") || TAKE_Word("TYPE_uzatish_istisno") || TAKE_Word("음수배열크기예외") || TAKE_Word("ARRAY_Store_to_xtab_qolish") || TAKE_Word("oqim_holat_istisno") || TAKE_Word("대기중단예외")) return;
        to_xtab_qolish_VALUE("unsupported throws type");
    }
    static void 선언읽기() {
        while (TAKE_Word("import")) {
            if (Word_VALUE(Holati, "한국어")) 예외이름읽기();
            else {
                말요구("java"); 요구('.'); 말요구("io"); 요구('.');
                if (!(TAKE_Word("FileInputStream") || TAKE_Word("FileOutputStream") || TAKE_Word("IOException"))) to_xtab_qolish_VALUE("unsupported import");
            }
            요구(';');
        }
        TAKE_Word("public"); TAKE_Word("final"); 말요구("class"); Sinf_token = identifikator_VALUE();
        Sinf_konstanta = Ma_lumotnomalar(7, token_konstanta(Sinf_token), 0);
        부모상수 = Ma_lumotnomalar(7, Word_konstanta("java/lang/Object"), 0); kod_konstanta = Word_konstanta("Code"); 요구('{');
        while (!Xato && 종류() != '}') {
            if (uslub_COUNT == 32) { to_xtab_qolish_VALUE("too many methods"); break; }
            int kirish_huquqi_kiritish = TAKE_Word("public") ? 1 : TAKE_Word("private") ? 2 : 0; 말요구("static");
            int FUNCTION_VALUE = uslub_COUNT++;
            uslub_kirish_huquqi[FUNCTION_VALUE] = kirish_huquqi_kiritish | 8;
            uslub_qaytarish[FUNCTION_VALUE] = format_VALUE(); uslub_kiritish_nom[FUNCTION_VALUE] = identifikator_VALUE(); 요구('(');
            for (int old_kamera_VALUE = 0; old_kamera_VALUE < FUNCTION_VALUE; old_kamera_VALUE++) if (이름같음(uslub_kiritish_nom[old_kamera_VALUE], uslub_kiritish_nom[FUNCTION_VALUE])) to_xtab_qolish_VALUE("duplicate method (overloading unsupported)");
            while (!Xato && 종류() != ')') {
                int 수 = uslub_dalil_COUNT[FUNCTION_VALUE];
                if (수 == 16) { to_xtab_qolish_VALUE("too many parameters"); break; }
                int TYPE_VALUE = format_VALUE(); if (TYPE_VALUE == 0) to_xtab_qolish_VALUE("void parameter");
                uslub_dalil_TYPE[FUNCTION_VALUE * 16 + 수] = TYPE_VALUE; uslub_dalil_nom[FUNCTION_VALUE * 16 + 수] = identifikator_VALUE();
                uslub_dalil_COUNT[FUNCTION_VALUE]++;
                if (!받기(',')) break;
            }
            요구(')');
            if (TAKE_Word("throws")) {
                do { 예외이름읽기(); } while (!Xato && 받기(','));
            }
            함수본문[FUNCTION_VALUE] = Holati; 요구('{');
            int ichiga_joylangan_VALUE = 1;
            while (Holati < token_COUNT && ichiga_joylangan_VALUE > 0) {
                if (종류() == '{') ichiga_joylangan_VALUE++;
                if (종류() == '}') ichiga_joylangan_VALUE--;
                Holati++;
            }
            if (ichiga_joylangan_VALUE != 0) to_xtab_qolish_VALUE("unclosed method body");
            uslub_to_xtatmoq[FUNCTION_VALUE] = Holati;
            uslub_nom_konstanta[FUNCTION_VALUE] = token_konstanta(uslub_kiritish_nom[FUNCTION_VALUE]);
            belgi_uzunlik = 0; 글추가('(');
            for (int 수 = 0; 수 < uslub_dalil_COUNT[FUNCTION_VALUE]; 수++) qo_shmoq_format(uslub_dalil_TYPE[FUNCTION_VALUE * 16 + 수]);
            글추가(')'); qo_shmoq_format(uslub_qaytarish[FUNCTION_VALUE]); 함수서술[FUNCTION_VALUE] = belgi_konstanta();
        }
        요구('}'); if (Holati != token_COUNT) to_xtab_qolish_VALUE("extra input after class");
    }
    static int FIND_mahalliy(int Nomi) {
        for (int 수 = mahalliy_COUNT - 1; 수 >= 0; 수--) if (지역깊이[수] >= 0 && 이름같음(mahalliy_nom[수], Nomi)) return 수;
        to_xtab_qolish_VALUE("unknown variable"); return 0;
    }
    static int qo_shmoq_mahalliy(int Nomi, int TYPE_VALUE) {
        for (int 수 = 0; 수 < mahalliy_COUNT; 수++) if (지역깊이[수] >= 0 && 이름같음(mahalliy_nom[수], Nomi)) to_xtab_qolish_VALUE("duplicate local variable");
        if (mahalliy_COUNT == 128) { to_xtab_qolish_VALUE("too many locals"); return 0; }
        mahalliy_nom[mahalliy_COUNT] = Nomi; mahalliy_TYPE[mahalliy_COUNT] = TYPE_VALUE; 지역깊이[mahalliy_COUNT] = 깊이;
        return mahalliy_COUNT++;
    }
    static boolean butun_son_TYPE(int TYPE_VALUE) { return TYPE_VALUE == 1 || TYPE_VALUE == 5; }
    static void 지역읽기(int 수) { 내보내기(mahalliy_TYPE[수] <= 2 || mahalliy_TYPE[수] == 5 ? 21 : 25); 내보내기(수); }
    static void yozmoq_mahalliy(int 수) { 내보내기(mahalliy_TYPE[수] <= 2 || mahalliy_TYPE[수] == 5 ? 54 : 58); 내보내기(수); }
    static void tasdiqlamoq_TYPE(int real_ma_lumotlar, int 기대) { if (real_ma_lumotlar != 기대 && !(real_ma_lumotlar == 5 && 기대 == 1)) to_xtab_qolish_VALUE("type mismatch"); }
    static void 문자읽기(int token_VALUE) {
        belgi_uzunlik = 0; int Bajarish = token_holat[token_VALUE] + 1, 끝 = token_holat[token_VALUE] + token_uzunlik[token_VALUE] - 1;
        while (Bajarish < 끝 && !Xato) {
            int VALUE = manba[Bajarish++];
            if (VALUE == '\\') {
                if (Bajarish == 끝) { to_xtab_qolish_VALUE("invalid escape"); break; }
                VALUE = manba[Bajarish++];
                if (VALUE == 'n') VALUE = 10;
                else if (VALUE == 'r') VALUE = 13;
                else if (VALUE == 't') VALUE = 9;
                else if (VALUE == 'b') VALUE = 8;
                else if (VALUE == 'f') VALUE = 12;
                else if (VALUE != '\\' && VALUE != '"' && VALUE != '\'') to_xtab_qolish_VALUE("unsupported escape");
            }
            글추가(VALUE);
        }
    }
    static int tahlil_qilmoq_butun_son(int token_VALUE, boolean 음수) {
        if (token_uzunlik[token_VALUE] > 1 && manba[token_holat[token_VALUE]] == '0') to_xtab_qolish_VALUE("octal literals unsupported");
        int VALUE = 0;
        for (int 수 = 0; 수 < token_uzunlik[token_VALUE]; 수++) {
            int raqam_element = manba[token_holat[token_VALUE] + 수] - '0';
            if (VALUE < -214748364 || VALUE == -214748364 && raqam_element > (음수 ? 8 : 7)) to_xtab_qolish_VALUE("integer literal out of range");
            VALUE = VALUE * 10 - raqam_element;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static int 기본식() {
        if (TAKE_Word("new")) {
            int TYPE_VALUE = format_VALUE();
            if (TYPE_VALUE != 6 && TYPE_VALUE != 7) { to_xtab_qolish_VALUE("only file streams supported by new in source"); return 0; }
            String egasi_VALUE = TYPE_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            Buyruq(187, Ma_lumotnomalar(7, Word_konstanta(egasi_VALUE), 0)); 내보내기(89);
            요구('('); tasdiqlamoq_TYPE(ifoda_VALUE(), 3); boolean 이어 = false;
            if (받기(',')) { if (TYPE_VALUE != 7) to_xtab_qolish_VALUE("input stream constructor arguments"); tasdiqlamoq_TYPE(ifoda_VALUE(), 2); 이어 = true; }
            요구(')');
            Buyruq(183, 외부참조(10, egasi_VALUE, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return TYPE_VALUE;
        }
        if (받기('(')) { int TYPE_VALUE = ifoda_VALUE(); 요구(')'); return TYPE_VALUE; }
        if (종류() == 257) { 수상수(tahlil_qilmoq_butun_son(Holati++, false)); return 1; }
        if (종류() == 258) { 문자읽기(Holati++); Buyruq(19, Ma_lumotnomalar(8, belgi_konstanta(), 0)); return 3; }
        if (종류() == 259) { 문자읽기(Holati++); if (belgi_uzunlik != 1) to_xtab_qolish_VALUE("character literal length"); 수상수(문자[0]); return 5; }
        if (TAKE_Word("true")) { 내보내기(4); return 2; }
        if (TAKE_Word("false")) { 내보내기(3); return 2; }
        if (TAKE_Word("한국어")) {
            요구('.'); 말요구("자체"); 요구('.');
            String egasi_VALUE = "", uslub_VALUE = "", 서술 = ""; int 가 = 0, 나 = 0, 다 = 0, 라 = 0, 마 = 0, o_lchov = 0;
            if (TAKE_Word("출력")) {
                egasi_VALUE = "한국어/자체/출력"; 요구('.');
                if (TAKE_Word("yozmoq_satr")) { uslub_VALUE = "yozmoq_satr"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("Yozish")) { uslub_VALUE = "Yozish"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("수쓰기")) { uslub_VALUE = "수쓰기"; 서술 = "(I)V"; 가 = 1; }
                else to_xtab_qolish_VALUE("unknown Korean output method");
            } else if (TAKE_Word("문자")) {
                egasi_VALUE = "한국어/자체/문자"; 요구('.'); 가 = 3;
                if (TAKE_Word("uzunlik_VALUE")) { uslub_VALUE = "uzunlik_VALUE"; 서술 = "(Ljava/lang/String;)I"; o_lchov = 1; }
                else if (TAKE_Word("belgi_kodi_COUNT")) { uslub_VALUE = "belgi_kodi_COUNT"; 서술 = "(Ljava/lang/String;)I"; o_lchov = 1; }
                else if (TAKE_Word("tahlil_qilmoq_butun_son")) { uslub_VALUE = "tahlil_qilmoq_butun_son"; 서술 = "(Ljava/lang/String;)I"; o_lchov = 1; }
                else if (TAKE_Word("yozmoq_butun_son_VALUE")) { uslub_VALUE = "yozmoq_butun_son_VALUE"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; o_lchov = 3; }
                else if (TAKE_Word("같음")) { uslub_VALUE = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; 나 = 3; o_lchov = 2; }
                else if (TAKE_Word("qo_shib_qo_ymoq_SMS")) { uslub_VALUE = "qo_shib_qo_ymoq_SMS"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; 나 = 3; o_lchov = 3; }
                else if (TAKE_Word("qirqmoq_VALUE")) { uslub_VALUE = "qirqmoq_VALUE"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; 나 = 1; 다 = 1; o_lchov = 3; }
                else to_xtab_qolish_VALUE("unknown Korean text method");
            } else if (TAKE_Word("Fayl")) {
                egasi_VALUE = "한국어/자체/Fayl"; 요구('.'); 가 = 3;
                if (TAKE_Word("Oʻqish")) { uslub_VALUE = "Oʻqish"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; o_lchov = 3; }
                else if (TAKE_Word("Yozish")) { uslub_VALUE = "Yozish"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; 나 = 3; }
                else to_xtab_qolish_VALUE("unknown Korean file method");
            } else if (TAKE_Word("화면")) {
                egasi_VALUE = "한국어/자체/화면"; 요구('.');
                if (TAKE_Word("너비")) { uslub_VALUE = "너비"; 서술 = "()I"; o_lchov = 1; }
                else if (TAKE_Word("높이")) { uslub_VALUE = "높이"; 서술 = "()I"; o_lchov = 1; }
                else if (TAKE_Word("사각형")) { uslub_VALUE = "사각형"; 서술 = "(IIIII)V"; 가 = 1; 나 = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (TAKE_Word("tozalash_kiritish")) { uslub_VALUE = "tozalash_kiritish"; 서술 = "(I)V"; 가 = 1; }
                else if (TAKE_Word("기다리기")) { uslub_VALUE = "기다리기"; 서술 = "()V"; }
                else to_xtab_qolish_VALUE("unknown Korean framebuffer method");
            } else to_xtab_qolish_VALUE("unsupported Korean library class");
            요구('('); if (가 != 0) tasdiqlamoq_TYPE(ifoda_VALUE(), 가);
            if (나 != 0) { 요구(','); tasdiqlamoq_TYPE(ifoda_VALUE(), 나); }
            if (다 != 0) { 요구(','); tasdiqlamoq_TYPE(ifoda_VALUE(), 다); }
            if (라 != 0) { 요구(','); tasdiqlamoq_TYPE(ifoda_VALUE(), 라); }
            if (마 != 0) { 요구(','); tasdiqlamoq_TYPE(ifoda_VALUE(), 마); }
            요구(')'); Buyruq(184, 외부참조(10, egasi_VALUE, uslub_VALUE, 서술)); return o_lchov;
        }
        if (TAKE_Word("Integer")) {
            요구('.'); 말요구("parseInt"); 요구('('); tasdiqlamoq_TYPE(ifoda_VALUE(), 3); 요구(')');
            Buyruq(184, 외부참조(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Nomi = identifikator_VALUE();
        if (받기('(')) {
            int FUNCTION_VALUE = -1;
            for (int 수 = 0; 수 < uslub_COUNT; 수++) if (이름같음(Nomi, uslub_kiritish_nom[수])) FUNCTION_VALUE = 수;
            if (FUNCTION_VALUE < 0) { to_xtab_qolish_VALUE("unknown static method"); return 0; }
            int 수 = 0;
            while (!Xato && 종류() != ')') {
                if (수 >= uslub_dalil_COUNT[FUNCTION_VALUE]) { to_xtab_qolish_VALUE("too many arguments"); break; }
                tasdiqlamoq_TYPE(ifoda_VALUE(), uslub_dalil_TYPE[FUNCTION_VALUE * 16 + 수++]); if (!받기(',')) break;
            }
            요구(')'); if (수 != uslub_dalil_COUNT[FUNCTION_VALUE]) to_xtab_qolish_VALUE("argument count mismatch");
            Buyruq(184, Ma_lumotnomalar(10, Sinf_konstanta, Ma_lumotnomalar(12, uslub_nom_konstanta[FUNCTION_VALUE], 함수서술[FUNCTION_VALUE])));
            return uslub_qaytarish[FUNCTION_VALUE];
        }
        int mahalliy_soha = FIND_mahalliy(Nomi), TYPE_VALUE = mahalliy_TYPE[mahalliy_soha]; 지역읽기(mahalliy_soha);
        while (!Xato) {
            if (받기('[')) { tasdiqlamoq_TYPE(TYPE_VALUE, 4); tasdiqlamoq_TYPE(ifoda_VALUE(), 1); 요구(']'); 내보내기(50); TYPE_VALUE = 3; }
            else if (받기('.')) {
                if (TYPE_VALUE == 6 || TYPE_VALUE == 7) {
                    String egasi_VALUE = TYPE_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (TAKE_Word("close")) { 요구('('); 요구(')'); Buyruq(182, 외부참조(10, egasi_VALUE, "close", "()V")); TYPE_VALUE = 0; }
                    else if (TYPE_VALUE == 6 && TAKE_Word("read")) { 요구('('); 요구(')'); Buyruq(182, 외부참조(10, egasi_VALUE, "read", "()I")); TYPE_VALUE = 1; }
                    else if (TYPE_VALUE == 7 && TAKE_Word("write")) { 요구('('); tasdiqlamoq_TYPE(ifoda_VALUE(), 1); 요구(')'); Buyruq(182, 외부참조(10, egasi_VALUE, "write", "(I)V")); TYPE_VALUE = 0; }
                    else { to_xtab_qolish_VALUE("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (TYPE_VALUE == 4) { 내보내기(190); TYPE_VALUE = 1; }
                else { tasdiqlamoq_TYPE(TYPE_VALUE, 3); 요구('('); 요구(')'); Buyruq(182, 외부참조(10, "java/lang/String", "length", "()I")); TYPE_VALUE = 1; }
            } else break;
        }
        return TYPE_VALUE;
    }
    static int 단항() {
        if (++식깊이 > 64) { to_xtab_qolish_VALUE("expression nesting too deep"); 식깊이--; return 0; }
        int TYPE_VALUE;
        if (받기('!')) { tasdiqlamoq_TYPE(단항(), 2); Taqqoslama_VALUE(153); TYPE_VALUE = 2; }
        else if (받기('-')) {
            if (종류() == 257) 수상수(tahlil_qilmoq_butun_son(Holati++, true));
            else { tasdiqlamoq_TYPE(단항(), 1); 내보내기(116); }
            TYPE_VALUE = 1;
        } else if (받기('+')) { tasdiqlamoq_TYPE(단항(), 1); TYPE_VALUE = 1; }
        else TYPE_VALUE = 기본식();
        식깊이--; return TYPE_VALUE;
    }
    static int 곱식() {
        int TYPE_VALUE = 단항();
        while (!Xato && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int kodlash_VALUE = 종류(); Holati++; tasdiqlamoq_TYPE(TYPE_VALUE, 1); tasdiqlamoq_TYPE(단항(), 1);
            내보내기(kodlash_VALUE == '*' ? 104 : kodlash_VALUE == '/' ? 108 : 112); TYPE_VALUE = 1;
        }
        return TYPE_VALUE;
    }
    static int 합식() {
        int TYPE_VALUE = 곱식();
        while (!Xato && (종류() == '+' || 종류() == '-')) {
            int kodlash_VALUE = 종류(); Holati++; int 경계 = kod_o_lcham, Orqaga_VALUE_TYPE = 곱식();
            if (kodlash_VALUE == '+' && (TYPE_VALUE == 3 || Orqaga_VALUE_TYPE == 3)) { 결합(경계, TYPE_VALUE, Orqaga_VALUE_TYPE); TYPE_VALUE = 3; }
            else { tasdiqlamoq_TYPE(TYPE_VALUE, 1); tasdiqlamoq_TYPE(Orqaga_VALUE_TYPE, 1); 내보내기(kodlash_VALUE == '+' ? 96 : 100); TYPE_VALUE = 1; }
        }
        return TYPE_VALUE;
    }
    static int 붙임참조(int TYPE_VALUE) {
        if (TYPE_VALUE != 1 && TYPE_VALUE != 2 && TYPE_VALUE != 3 && TYPE_VALUE != 5) to_xtab_qolish_VALUE("unsupported concatenation type");
        return 외부참조(10, "java/lang/StringBuilder", "append", TYPE_VALUE == 1 ? "(I)Ljava/lang/StringBuilder;"
            : TYPE_VALUE == 2 ? "(Z)Ljava/lang/StringBuilder;" : TYPE_VALUE == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int 경계, int old_kamera_VALUE_TYPE, int Orqaga_VALUE_TYPE) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 RIGHT kod_VALUE 앞에 generatsiiyalash 코드를 삽입한다.
        // RIGHT ifoda_VALUE 내부의 bir_rangli_VALUE shox 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = kod_o_lcham;
        Buyruq(187, Ma_lumotnomalar(7, Word_konstanta("java/lang/StringBuilder"), 0)); 내보내기(89);
        Buyruq(183, 외부참조(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); Buyruq(182, 붙임참조(old_kamera_VALUE_TYPE));
        if (Xato) return;
        int uzunlik_VALUE = kod_o_lcham - 끝;
        for (int 수 = 0; 수 < uzunlik_VALUE; 수++) 삽입코드[수] = kod_VALUE[끝 + 수];
        for (int 수 = 끝 - 1; 수 >= 경계; 수--) kod_VALUE[수 + uzunlik_VALUE] = kod_VALUE[수];
        for (int 수 = 0; 수 < uzunlik_VALUE; 수++) kod_VALUE[경계 + 수] = 삽입코드[수];
        Buyruq(182, 붙임참조(Orqaga_VALUE_TYPE)); Buyruq(182, 외부참조(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int Taqqoslama_ifoda() {
        int TYPE_VALUE = 합식();
        while (!Xato && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int kodlash_VALUE = 종류(); Holati++; tasdiqlamoq_TYPE(TYPE_VALUE, 1); tasdiqlamoq_TYPE(합식(), 1);
            Taqqoslama_VALUE(kodlash_VALUE == '<' ? 161 : kodlash_VALUE == '>' ? 163 : kodlash_VALUE == 302 ? 164 : 162); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int 동등식() {
        int TYPE_VALUE = Taqqoslama_ifoda();
        while (!Xato && (종류() == 300 || 종류() == 301)) {
            int kodlash_VALUE = 종류(); Holati++; int Orqaga_VALUE_TYPE = Taqqoslama_ifoda();
            if (TYPE_VALUE == 0 || Orqaga_VALUE_TYPE == 0) to_xtab_qolish_VALUE("void expression");
            if (!(butun_son_TYPE(TYPE_VALUE) && butun_son_TYPE(Orqaga_VALUE_TYPE))) tasdiqlamoq_TYPE(Orqaga_VALUE_TYPE, TYPE_VALUE);
            Taqqoslama_VALUE((TYPE_VALUE <= 2 || TYPE_VALUE == 5 ? 159 : 165) + (kodlash_VALUE == 301 ? 1 : 0)); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int 논리곱() {
        int TYPE_VALUE = 동등식();
        while (!Xato && 받기(304)) {
            tasdiqlamoq_TYPE(TYPE_VALUE, 2); int 가 = shox(153); tasdiqlamoq_TYPE(동등식(), 2); int 나 = shox(153);
            내보내기(4); int 끝 = shox(167); ulash_VALUE(가, kod_o_lcham); ulash_VALUE(나, kod_o_lcham); 내보내기(3); ulash_VALUE(끝, kod_o_lcham); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int ifoda_VALUE() {
        int TYPE_VALUE = 논리곱();
        while (!Xato && 받기(305)) {
            tasdiqlamoq_TYPE(TYPE_VALUE, 2); int 가 = shox(154); tasdiqlamoq_TYPE(논리곱(), 2); int 나 = shox(154);
            내보내기(3); int 끝 = shox(167); ulash_VALUE(가, kod_o_lcham); ulash_VALUE(나, kod_o_lcham); 내보내기(4); ulash_VALUE(끝, kod_o_lcham); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static void tayinlash_VALUE_031eac11(boolean Ruxsatnoma_e_lon_qilish) {
        if (Word_VALUE(Holati, "int") || Word_VALUE(Holati, "boolean") || Word_VALUE(Holati, "String") || Word_VALUE(Holati, "char")
            || Word_VALUE(Holati, "FileInputStream") || Word_VALUE(Holati, "FileOutputStream")) {
            if (!Ruxsatnoma_e_lon_qilish) to_xtab_qolish_VALUE("declaration not allowed here");
            int TYPE_VALUE = format_VALUE(), Nomi = identifikator_VALUE(); 요구('='); tasdiqlamoq_TYPE(ifoda_VALUE(), TYPE_VALUE);
            yozmoq_mahalliy(qo_shmoq_mahalliy(Nomi, TYPE_VALUE)); return;
        }
        int Nomi = identifikator_VALUE(), mahalliy_soha = FIND_mahalliy(Nomi);
        if (받기('=')) { tasdiqlamoq_TYPE(ifoda_VALUE(), mahalliy_TYPE[mahalliy_soha]); yozmoq_mahalliy(mahalliy_soha); }
        else if (종류() >= 308 && 종류() <= 312) {
            int kodlash_VALUE = 종류(); Holati++; 지역읽기(mahalliy_soha); int 경계 = kod_o_lcham, Orqaga_VALUE_TYPE = ifoda_VALUE();
            if (kodlash_VALUE == 308 && mahalliy_TYPE[mahalliy_soha] == 3) 결합(경계, 3, Orqaga_VALUE_TYPE);
            else {
                tasdiqlamoq_TYPE(mahalliy_TYPE[mahalliy_soha], 1); tasdiqlamoq_TYPE(Orqaga_VALUE_TYPE, 1);
                내보내기(kodlash_VALUE == 308 ? 96 : kodlash_VALUE == 309 ? 100 : kodlash_VALUE == 310 ? 104 : kodlash_VALUE == 311 ? 108 : 112);
                if (mahalliy_TYPE[mahalliy_soha] == 5) 내보내기(146);
            }
            yozmoq_mahalliy(mahalliy_soha);
        }
        else if (종류() == 306 || 종류() == 307) {
            tasdiqlamoq_TYPE(mahalliy_TYPE[mahalliy_soha], 1); 내보내기(132); 내보내기(mahalliy_soha); 내보내기(종류() == 306 ? 1 : 255); Holati++;
            if (mahalliy_TYPE[mahalliy_soha] == 5) { 지역읽기(mahalliy_soha); 내보내기(146); yozmoq_mahalliy(mahalliy_soha); }
        } else to_xtab_qolish_VALUE("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); 요구('.'); 말요구("out"); 요구('.');
        boolean 줄바꿈 = TAKE_Word("println"); if (!줄바꿈) 말요구("print"); 요구('(');
        Buyruq(178, 외부참조(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean bo_sh_dalil = 종류() == ')';
        int TYPE_VALUE = bo_sh_dalil ? 0 : ifoda_VALUE(); 요구(')'); 요구(';');
        String 서술 = TYPE_VALUE == 0 ? "()V" : TYPE_VALUE == 1 ? "(I)V" : TYPE_VALUE == 2 ? "(Z)V" : TYPE_VALUE == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (TYPE_VALUE == 4 || TYPE_VALUE >= 6 || TYPE_VALUE == 0 && (!줄바꿈 || !bo_sh_dalil)) to_xtab_qolish_VALUE("unsupported print argument");
        Buyruq(182, 외부참조(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean bayonot_VALUE() {
        if (Xato) return false;
        if (깊이 > 32) { to_xtab_qolish_VALUE("statement nesting too deep"); return false; }
        if (받기('{')) {
            깊이++; boolean qaytarish_o_lchov = false;
            while (!Xato && 종류() != '}') { if (qaytarish_o_lchov) to_xtab_qolish_VALUE("unreachable statement"); qaytarish_o_lchov = bayonot_VALUE(); }
            요구('}'); for (int 수 = 0; 수 < mahalliy_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return qaytarish_o_lchov;
        }
        if (받기(';')) return false;
        if (TAKE_Word("return")) {
            int TYPE_VALUE = 종류() == ';' ? 0 : ifoda_VALUE(); tasdiqlamoq_TYPE(TYPE_VALUE, uslub_qaytarish[현재함수]); 요구(';');
            내보내기(TYPE_VALUE == 0 ? 177 : TYPE_VALUE <= 2 || TYPE_VALUE == 5 ? 172 : 176); return true;
        }
        if (TAKE_Word("if")) {
            요구('('); tasdiqlamoq_TYPE(ifoda_VALUE(), 2); 요구(')'); int FALSE_VALUE = shox(153);
            깊이++; boolean 가 = boshqaruv_bayonot(); 깊이--;
            if (TAKE_Word("else")) { int 끝 = shox(167); ulash_VALUE(FALSE_VALUE, kod_o_lcham); 깊이++; boolean 나 = boshqaruv_bayonot(); 깊이--; ulash_VALUE(끝, kod_o_lcham); return 가 && 나; }
            ulash_VALUE(FALSE_VALUE, kod_o_lcham); return false;
        }
        if (TAKE_Word("while")) {
            int Bajarish = kod_o_lcham; 요구('('); tasdiqlamoq_TYPE(ifoda_VALUE(), 2); 요구(')'); int 끝 = shox(153);
            깊이++; boshqaruv_bayonot(); 깊이--; ulash_VALUE(shox(167), Bajarish); ulash_VALUE(끝, kod_o_lcham); return false;
        }
        if (TAKE_Word("for")) {
            깊이++; 요구('('); if (종류() != ';') tayinlash_VALUE_031eac11(true); 요구(';');
            int holat = kod_o_lcham; if (종류() == ';') 내보내기(4); else tasdiqlamoq_TYPE(ifoda_VALUE(), 2); 요구(';');
            int 끝 = shox(153), asosiy_matn = shox(167), yangilamoq = kod_o_lcham;
            if (종류() != ')') tayinlash_VALUE_031eac11(false); 요구(')'); ulash_VALUE(shox(167), holat); ulash_VALUE(asosiy_matn, kod_o_lcham);
            boshqaruv_bayonot(); ulash_VALUE(shox(167), yangilamoq); ulash_VALUE(끝, kod_o_lcham);
            for (int 수 = 0; 수 < mahalliy_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return false;
        }
        if (Word_VALUE(Holati, "System")) { 화면출력(); return false; }
        if (종류() == 256 && Holati + 1 < token_COUNT && (토큰종류[Holati + 1] == '(' || 토큰종류[Holati + 1] == '.')) {
            int TYPE_VALUE = ifoda_VALUE(); if (TYPE_VALUE != 0) 내보내기(87); 요구(';'); return false;
        }
        tayinlash_VALUE_031eac11(true); 요구(';'); return false;
    }
    static boolean boshqaruv_bayonot() {
        if (Word_VALUE(Holati, "int") || Word_VALUE(Holati, "boolean") || Word_VALUE(Holati, "char") || Word_VALUE(Holati, "String")
            || Word_VALUE(Holati, "FileInputStream") || Word_VALUE(Holati, "FileOutputStream")) to_xtab_qolish_VALUE("local declaration requires braces");
        return bayonot_VALUE();
    }
    static void 출바(int VALUE) { if (출력크기 == 출력.length) to_xtab_qolish_VALUE("class file too large"); else 출력[출력크기++] = VALUE & 255; }
    static void 출짧(int VALUE) { 출바(VALUE >> 8); 출바(VALUE); }
    static void 출정(int VALUE) { 출짧(VALUE >>> 16); 출짧(VALUE); }
    static void yozmoq_Sinf() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(konstanta_COUNT);
        for (int 수 = 0; 수 < konstanta_o_lcham; 수++) 출바(konstanta_VALUE[수]);
        출짧(0x21); 출짧(Sinf_konstanta); 출짧(부모상수); 출짧(0); 출짧(0); 출짧(uslub_COUNT);
        for (int 수 = 0; 수 < uslub_COUNT; 수++) {
            출짧(uslub_kirish_huquqi[수]); 출짧(uslub_nom_konstanta[수]); 출짧(함수서술[수]); 출짧(1); 출짧(kod_konstanta);
            출정(12 + uslub_uzunlik[수]); 출짧(128); 출짧(함수지역[수]); 출정(uslub_uzunlik[수]);
            for (int in_kiritish = 0; in_kiritish < uslub_uzunlik[수]; in_kiritish++) 출바(kod_VALUE[uslub_kod[수] + in_kiritish]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int Bajarish() {
        if (foydalanuvchi.인수개수() == 1 && 자바도구.같음(foydalanuvchi.인수(0), "-version")) {
            foydalanuvchi.Yozish("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (foydalanuvchi.인수개수() != 1) { foydalanuvchi.Yozish("Usage: javac FILE.java\n"); return 2; }
        int nom_o_lcham = 자바도구.Nomi(fayl_nom_SMS, foydalanuvchi.인수(0));
        if (nom_o_lcham < 6 || nom_o_lcham > 62 || fayl_nom_SMS[nom_o_lcham - 5] != '.' || fayl_nom_SMS[nom_o_lcham - 4] != 'j'
            || fayl_nom_SMS[nom_o_lcham - 3] != 'a' || fayl_nom_SMS[nom_o_lcham - 2] != 'v' || fayl_nom_SMS[nom_o_lcham - 1] != 'a') {
            foydalanuvchi.Yozish("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        manba_o_lcham = foydalanuvchi.파일읽기(fayl_nom_SMS, manba);
        if (manba_o_lcham < 0) { foydalanuvchi.Yozish("javac: cannot read source: "); 자바도구.수쓰기(manba_o_lcham); foydalanuvchi.yozmoq_belgi_VALUE(10); return 1; }
        manba_o_lcham = 자바도구.원문해독(manba, manba_o_lcham);
        if (manba_o_lcham < 0) { foydalanuvchi.Yozish("javac error: invalid UTF-8 source\n"); return 1; }
        qirqmoq_VALUE(); if (!Xato) 선언읽기();
        if (!Xato) {
            if (token_uzunlik[Sinf_token] != nom_o_lcham - 5) to_xtab_qolish_VALUE("class name must match file name");
            for (int 수 = 0; 수 < nom_o_lcham - 5; 수++) if (manba[token_holat[Sinf_token] + 수] != fayl_nom_SMS[수]) to_xtab_qolish_VALUE("class name must match file name");
        }
        for (현재함수 = 0; 현재함수 < uslub_COUNT && !Xato; 현재함수++) {
            Holati = 함수본문[현재함수]; uslub_kod[현재함수] = kod_o_lcham; mahalliy_COUNT = 0; 깊이 = 0;
            for (int 수 = 0; 수 < uslub_dalil_COUNT[현재함수]; 수++) qo_shmoq_mahalliy(uslub_dalil_nom[현재함수 * 16 + 수], uslub_dalil_TYPE[현재함수 * 16 + 수]);
            boolean qaytarish_o_lchov = bayonot_VALUE();
            if (!qaytarish_o_lchov && uslub_qaytarish[현재함수] != 0) to_xtab_qolish_VALUE("missing return");
            // shox 뒤의 합류 지점은 반드시 real_ma_lumotlar 명령이어야 한다 (버전 49 검증기).
            if (uslub_qaytarish[현재함수] == 0) 내보내기(177);
            else { boolean butun_son = uslub_qaytarish[현재함수] <= 2 || uslub_qaytarish[현재함수] == 5; 내보내기(butun_son ? 3 : 1); 내보내기(butun_son ? 172 : 176); }
            if (Holati != uslub_to_xtatmoq[현재함수]) to_xtab_qolish_VALUE("invalid method body");
            함수지역[현재함수] = mahalliy_COUNT; uslub_uzunlik[현재함수] = kod_o_lcham - uslub_kod[현재함수];
        }
        if (Xato) return 1;
        yozmoq_Sinf(); if (Xato) return 1;
        fayl_nom_SMS[nom_o_lcham - 4] = 'c'; fayl_nom_SMS[nom_o_lcham - 3] = 'l'; fayl_nom_SMS[nom_o_lcham - 2] = 'a';
        fayl_nom_SMS[nom_o_lcham - 1] = 's'; fayl_nom_SMS[nom_o_lcham] = 's'; fayl_nom_SMS[nom_o_lcham + 1] = 0;
        int o_lchov = foydalanuvchi.yozmoq_fayl(fayl_nom_SMS, 출력, 출력크기);
        if (o_lchov < 0) { foydalanuvchi.Yozish("javac: cannot save class: "); 자바도구.수쓰기(o_lchov); foydalanuvchi.yozmoq_belgi_VALUE(10); return 1; }
        foydalanuvchi.Yozish("Compiled: "); for (int 수 = 0; fayl_nom_SMS[수] != 0; 수++) foydalanuvchi.yozmoq_belgi_VALUE(fayl_nom_SMS[수]);
        foydalanuvchi.Yozish(" (JVM class version 49)\n"); return 0;
    }
}
