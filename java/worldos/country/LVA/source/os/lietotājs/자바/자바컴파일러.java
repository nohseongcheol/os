// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java avots_koks -> 표준 버전 49 class kompilators. */
public final class 자바컴파일러 {
    static int[] AVOTS = new int[16384], Izvade = new int[16384], CODE_VALUE = new int[4096];
    static int[] 토큰종류 = new int[2048], daļiņa_amats = new int[2048], 토큰길이 = new int[2048];
    static int[] konstante_VALUE = new int[4096], konstante_Nobīde = new int[512];
    static int[] 문자 = new int[512], faila_nosaukums_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int avots_mainīt_izmērus, daļiņa_COUNT, Novietojums, CODE_mainīt_izmērus, konstante_mainīt_izmērus, konstante_COUNT = 1, ražojums_mainīt_izmērus, 문자수;
    static boolean Kļūda;
    static int klase_daļiņa, klase_konstante, vecākobjekts_konstante, CODE_konstante;
    static int[] metode_ievade_nosaukums = new int[32], metode_atdot = new int[32], metode_arg_COUNT = new int[32];
    static int[] metode_arg_nosaukums = new int[512], metode_arg_TYPE = new int[512];
    static int[] metode_pamatteksts = new int[32], metode_beigt_zvanu = new int[32], metode_CODE = new int[32];
    static int[] 함수길이 = new int[32], 함수지역 = new int[32], metode_nosaukums_konstante = new int[32], 함수서술 = new int[32];
    static int[] metode_piekļūt = new int[32];
    static int metode_COUNT, pašreizējais_metode, vietējs_COUNT, 깊이, 식깊이;
    static int[] vietējs_nosaukums = new int[128], vietējs_TYPE = new int[128], 지역깊이 = new int[128];

    static void kļūme_VALUE(String 이유) {
        if (!Kļūda) {
            lietotājs.Rakstīt("javac error: "); lietotājs.Rakstīt(이유);
            lietotājs.Rakstīt(" at line ");
            int Līniju = 1, 끝 = Novietojums < daļiņa_COUNT ? daļiņa_amats[Novietojums] : avots_mainīt_izmērus;
            for (int numurs = 0; numurs < 끝; numurs++) if (AVOTS[numurs] == 10) Līniju++;
            자바도구.rakstīšana_numurs(Līniju); lietotājs.rakstīšana_rakstzīme_VALUE(10);
        }
        Kļūda = true;
    }
    static boolean rakstzīme_VALUE(int VALUE) { return 문자이름규칙.첫글자(VALUE); }
    static boolean cipars_VALUE(int VALUE) { return VALUE >= '0' && VALUE <= '9'; }
    static boolean 이름같음(int 가, int SECOND_operands) {
        if (가 < 0 || SECOND_operands < 0 || 가 >= daļiņa_COUNT || SECOND_operands >= daļiņa_COUNT || 토큰길이[가] != 토큰길이[SECOND_operands]) return false;
        for (int numurs = 0; numurs < 토큰길이[가]; numurs++) if (AVOTS[daļiņa_amats[가] + numurs] != AVOTS[daļiņa_amats[SECOND_operands] + numurs]) return false;
        return true;
    }
    static boolean Word_VALUE(int daļiņa_VALUE, String Word_SMS) {
        if (daļiņa_VALUE < 0 || daļiņa_VALUE >= daļiņa_COUNT || 토큰길이[daļiņa_VALUE] != Word_SMS.length()) return false;
        for (int numurs = 0; numurs < Word_SMS.length(); numurs++) if (AVOTS[daļiņa_amats[daļiņa_VALUE] + numurs] != Word_SMS.charAt(numurs)) return false;
        return true;
    }
    static int 종류() { return Novietojums < daļiņa_COUNT ? 토큰종류[Novietojums] : 0; }
    static boolean saņemt(int VALUE) { if (종류() != VALUE) return false; Novietojums++; return true; }
    static void prasība_VALUE(int VALUE) { if (!saņemt(VALUE)) kļūme_VALUE("unexpected token"); }
    static boolean TAKE_Word(String Word_SMS) { if (!Word_VALUE(Novietojums, Word_SMS)) return false; Novietojums++; return true; }
    static void 말요구(String Word_SMS) { if (!TAKE_Word(Word_SMS)) kļūme_VALUE(Word_SMS); }
    static int identifikators_VALUE() {
        int mērs = Novietojums;
        if (종류() != 256) kļūme_VALUE("identifier required"); else Novietojums++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int Palaist = 0;
        for (int numurs = 0; numurs <= 예약어.length(); numurs++) {
            if (numurs == 예약어.length() || 예약어.charAt(numurs) == ' ') {
                boolean 같음 = numurs - Palaist == 토큰길이[mērs];
                for (int 칸 = Palaist; 같음 && 칸 < numurs; 칸++) if (예약어.charAt(칸) != AVOTS[daļiņa_amats[mērs] + 칸 - Palaist]) 같음 = false;
                if (같음) kļūme_VALUE("reserved word cannot be an identifier");
                Palaist = numurs + 1;
            }
        }
        return mērs;
    }
    static void izgriezt_VALUE() {
        int numurs = 0;
        while (numurs < avots_mainīt_izmērus && !Kļūda) {
            int VALUE = AVOTS[numurs], Palaist = numurs, 종류 = VALUE;
            if (VALUE == 32 || VALUE == 9 || VALUE == 10 || VALUE == 13) { numurs++; continue; }
            if (VALUE == '/' && numurs + 1 < avots_mainīt_izmērus && AVOTS[numurs + 1] == '/') {
                while (numurs < avots_mainīt_izmērus && AVOTS[numurs] != 10) numurs++;
                continue;
            }
            if (VALUE == '/' && numurs + 1 < avots_mainīt_izmērus && AVOTS[numurs + 1] == '*') {
                numurs += 2;
                while (numurs + 1 < avots_mainīt_izmērus && !(AVOTS[numurs] == '*' && AVOTS[numurs + 1] == '/')) numurs++;
                if (numurs + 1 >= avots_mainīt_izmērus) { kļūme_VALUE("unterminated comment"); break; }
                numurs += 2; continue;
            }
            if (rakstzīme_VALUE(VALUE)) { 종류 = 256; while (numurs < avots_mainīt_izmērus && 문자이름규칙.이어진글자(AVOTS[numurs])) numurs++; }
            else if (cipars_VALUE(VALUE)) { 종류 = 257; while (numurs < avots_mainīt_izmērus && cipars_VALUE(AVOTS[numurs])) numurs++; }
            else if (VALUE == '"' || VALUE == '\'') {
                종류 = VALUE == '"' ? 258 : 259; numurs++;
                while (numurs < avots_mainīt_izmērus && AVOTS[numurs] != VALUE && AVOTS[numurs] != 10 && AVOTS[numurs] != 13) {
                    if (AVOTS[numurs] == '\\') numurs++;
                    numurs++;
                }
                if (numurs >= avots_mainīt_izmērus || AVOTS[numurs] != VALUE) { kļūme_VALUE("unterminated literal"); break; }
                numurs++;
            } else {
                numurs++;
                if (numurs < avots_mainīt_izmērus) {
                    int Tālāk_krājums = AVOTS[numurs];
                    if (VALUE == '=' && Tālāk_krājums == '=') 종류 = 300;
                    if (VALUE == '!' && Tālāk_krājums == '=') 종류 = 301;
                    if (VALUE == '<' && Tālāk_krājums == '=') 종류 = 302;
                    if (VALUE == '>' && Tālāk_krājums == '=') 종류 = 303;
                    if (VALUE == '&' && Tālāk_krājums == '&') 종류 = 304;
                    if (VALUE == '|' && Tālāk_krājums == '|') 종류 = 305;
                    if (VALUE == '+' && Tālāk_krājums == '+') 종류 = 306;
                    if (VALUE == '-' && Tālāk_krājums == '-') 종류 = 307;
                    if (VALUE == '+' && Tālāk_krājums == '=') 종류 = 308;
                    if (VALUE == '-' && Tālāk_krājums == '=') 종류 = 309;
                    if (VALUE == '*' && Tālāk_krājums == '=') 종류 = 310;
                    if (VALUE == '/' && Tālāk_krājums == '=') 종류 = 311;
                    if (VALUE == '%' && Tālāk_krājums == '=') 종류 = 312;
                    if (종류 >= 300) numurs++;
                }
            }
            if (daļiņa_COUNT == 토큰종류.length - 1) { kļūme_VALUE("too many tokens (2047 maximum)"); break; }
            토큰종류[daļiņa_COUNT] = 종류; daļiņa_amats[daļiņa_COUNT] = Palaist; 토큰길이[daļiņa_COUNT++] = numurs - Palaist;
        }
    }
    static void rakstīšana_konstante_byte(int VALUE) {
        if (konstante_mainīt_izmērus == konstante_VALUE.length) { kļūme_VALUE("constant pool too large"); return; }
        konstante_VALUE[konstante_mainīt_izmērus++] = VALUE & 255;
    }
    static void 상짧(int VALUE) { rakstīšana_konstante_byte(VALUE >> 8); rakstīšana_konstante_byte(VALUE); }
    static int reģistrs_konstante(int Palaist) {
        for (int numurs = 1; numurs < konstante_COUNT; numurs++) {
            int priekšējā_VALUE = konstante_Nobīde[numurs], 길이 = (numurs + 1 < konstante_COUNT ? konstante_Nobīde[numurs + 1] : Palaist) - priekšējā_VALUE;
            if (길이 != konstante_mainīt_izmērus - Palaist) continue;
            boolean 같음 = true;
            for (int 칸 = 0; 칸 < 길이; 칸++) if (konstante_VALUE[priekšējā_VALUE + 칸] != konstante_VALUE[Palaist + 칸]) 같음 = false;
            if (같음) { konstante_mainīt_izmērus = Palaist; return numurs; }
        }
        if (konstante_COUNT == konstante_Nobīde.length) { kļūme_VALUE("too many constants"); return 0; }
        konstante_Nobīde[konstante_COUNT] = Palaist;
        return konstante_COUNT++;
    }
    static void Pievienot_SMS(int VALUE) {
        if (문자수 == 문자.length) { kļūme_VALUE("text too long"); return; }
        문자[문자수++] = VALUE;
    }
    static void Pievienot_Word(String Word_SMS) { for (int numurs = 0; numurs < Word_SMS.length(); numurs++) Pievienot_SMS(Word_SMS.charAt(numurs)); }
    static int rakstzīme_konstante() {
        int Palaist = konstante_mainīt_izmērus; rakstīšana_konstante_byte(1); 상짧(0);
        for (int numurs = 0; numurs < 문자수; numurs++) {
            int VALUE = 문자[numurs];
            if (VALUE > 0 && VALUE < 128) rakstīšana_konstante_byte(VALUE);
            else if (VALUE < 2048) { rakstīšana_konstante_byte(192 | VALUE >> 6); rakstīšana_konstante_byte(128 | VALUE & 63); }
            else { rakstīšana_konstante_byte(224 | VALUE >> 12); rakstīšana_konstante_byte(128 | VALUE >> 6 & 63); rakstīšana_konstante_byte(128 | VALUE & 63); }
        }
        if (Kļūda) return 0;
        int 길이 = konstante_mainīt_izmērus - Palaist - 3;
        konstante_VALUE[Palaist + 1] = 길이 >> 8; konstante_VALUE[Palaist + 2] = 길이 & 255;
        return reģistrs_konstante(Palaist);
    }
    static int Word_konstante(String Word_SMS) { 문자수 = 0; Pievienot_Word(Word_SMS); return rakstzīme_konstante(); }
    static int daļiņa_konstante(int daļiņa_VALUE) {
        문자수 = 0;
        for (int numurs = 0; numurs < 토큰길이[daļiņa_VALUE]; numurs++) Pievienot_SMS(AVOTS[daļiņa_amats[daļiņa_VALUE] + numurs]);
        return rakstzīme_konstante();
    }
    static int Uzziņas(int 종류, int 가, int SECOND_operands) {
        int Palaist = konstante_mainīt_izmērus; rakstīšana_konstante_byte(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(SECOND_operands);
        return reģistrs_konstante(Palaist);
    }
    static int ārējs_Uzziņas(int 종류, String īpašnieks_VALUE, String Nosaukums, String 서술) {
        int īpašnieks_identifikators = Uzziņas(7, Word_konstante(īpašnieks_VALUE), 0);
        int nosaukums_COUNT = Word_konstante(Nosaukums), formāts_COUNT = Word_konstante(서술);
        return Uzziņas(종류, īpašnieks_identifikators, Uzziņas(12, nosaukums_COUNT, formāts_COUNT));
    }
    static void 내보내기(int VALUE) {
        if (CODE_mainīt_izmērus == CODE_VALUE.length) { kļūme_VALUE("bytecode too large"); return; }
        CODE_VALUE[CODE_mainīt_izmērus++] = VALUE & 255;
    }
    static void Komanda(int VALUE, int Parametri) { 내보내기(VALUE); 내보내기(Parametri >> 8); 내보내기(Parametri); }
    static void 수상수(int VALUE) {
        if (VALUE >= -1 && VALUE <= 5) { 내보내기(VALUE + 3); return; }
        int Palaist = konstante_mainīt_izmērus; rakstīšana_konstante_byte(3); 상짧(VALUE >>> 16); 상짧(VALUE);
        Komanda(19, reģistrs_konstante(Palaist));
    }
    static int zars(int Komanda) { int mērs = CODE_mainīt_izmērus; Komanda(Komanda, 0); return mērs; }
    static void Saite_VALUE(int zars, int mērķis_objekts) {
        if (Kļūda) return;
        int 거리 = mērķis_objekts - zars;
        if (거리 < -32768 || 거리 > 32767 || zars < 0 || zars + 2 >= CODE_mainīt_izmērus) { kļūme_VALUE("invalid branch"); return; }
        CODE_VALUE[zars + 1] = 거리 >> 8 & 255; CODE_VALUE[zars + 2] = 거리 & 255;
    }
    static void Salīdzinājums_VALUE(int Komanda) {
        int TRUE_VALUE = zars(Komanda); 내보내기(3); int 끝 = zars(167);
        Saite_VALUE(TRUE_VALUE, CODE_mainīt_izmērus); 내보내기(4); Saite_VALUE(끝, CODE_mainīt_izmērus);
    }
    static int formāts_VALUE() {
        if (TAKE_Word("void")) return 0;
        if (TAKE_Word("int")) return 1;
        if (TAKE_Word("boolean")) return 2;
        if (TAKE_Word("char")) return 5;
        if (TAKE_Word("FileInputStream")) return 6;
        if (TAKE_Word("FileOutputStream")) return 7;
        if (TAKE_Word("String")) { if (saņemt('[')) { prasība_VALUE(']'); return 4; } return 3; }
        kļūme_VALUE("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void Pievienot_formāts(int TYPE_VALUE) {
        if (TYPE_VALUE == 0) Pievienot_SMS('V');
        if (TYPE_VALUE == 1) Pievienot_SMS('I');
        if (TYPE_VALUE == 2) Pievienot_SMS('Z');
        if (TYPE_VALUE == 3) Pievienot_Word("Ljava/lang/String;");
        if (TYPE_VALUE == 4) Pievienot_Word("[Ljava/lang/String;");
        if (TYPE_VALUE == 5) Pievienot_SMS('C');
        if (TYPE_VALUE == 6) Pievienot_Word("Ljava/io/FileInputStream;");
        if (TYPE_VALUE == 7) Pievienot_Word("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws deklarācija. izņēmums Process_VALUE_ievade 본문은 viesot javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = TAKE_Word("Latviešu");
        if (한국어묶음) { prasība_VALUE('.'); 말요구("savs"); prasība_VALUE('.'); }
        if (!한국어묶음 && (TAKE_Word("Exception") || TAKE_Word("IOException"))) return;
        if (TAKE_Word("izņēmums") || TAKE_Word("실행예외") || TAKE_Word("ievadizvade_izņēmums") || TAKE_Word("pagaidi_NOILGUMS_izņēmums") || TAKE_Word("adrese_LOOKUP_izņēmums") || TAKE_Word("파일없음예외") || TAKE_Word("통신예외") || TAKE_Word("nederīgs_arg_izņēmums") || TAKE_Word("numurs_formāts_kļūme") || TAKE_Word("범위예외") || TAKE_Word("배열범위예외") || TAKE_Word("문자열범위예외") || TAKE_Word("NULL_Uzziņas_izņēmums") || TAKE_Word("산술예외") || TAKE_Word("Statuss_izņēmums") || TAKE_Word("TYPE_atskaņot_izņēmums") || TAKE_Word("음수배열크기예외") || TAKE_Word("ARRAY_Store_kļūme") || TAKE_Word("saruna_Statuss_izņēmums") || TAKE_Word("대기중단예외")) return;
        kļūme_VALUE("unsupported throws type");
    }
    static void 선언읽기() {
        while (TAKE_Word("import")) {
            if (Word_VALUE(Novietojums, "Latviešu")) 예외이름읽기();
            else {
                말요구("java"); prasība_VALUE('.'); 말요구("io"); prasība_VALUE('.');
                if (!(TAKE_Word("FileInputStream") || TAKE_Word("FileOutputStream") || TAKE_Word("IOException"))) kļūme_VALUE("unsupported import");
            }
            prasība_VALUE(';');
        }
        TAKE_Word("public"); TAKE_Word("final"); 말요구("class"); klase_daļiņa = identifikators_VALUE();
        klase_konstante = Uzziņas(7, daļiņa_konstante(klase_daļiņa), 0);
        vecākobjekts_konstante = Uzziņas(7, Word_konstante("java/lang/Object"), 0); CODE_konstante = Word_konstante("Code"); prasība_VALUE('{');
        while (!Kļūda && 종류() != '}') {
            if (metode_COUNT == 32) { kļūme_VALUE("too many methods"); break; }
            int piekļūt_ievade = TAKE_Word("public") ? 1 : TAKE_Word("private") ? 2 : 0; 말요구("static");
            int FUNCTION_VALUE = metode_COUNT++;
            metode_piekļūt[FUNCTION_VALUE] = piekļūt_ievade | 8;
            metode_atdot[FUNCTION_VALUE] = formāts_VALUE(); metode_ievade_nosaukums[FUNCTION_VALUE] = identifikators_VALUE(); prasība_VALUE('(');
            for (int priekšējā_VALUE = 0; priekšējā_VALUE < FUNCTION_VALUE; priekšējā_VALUE++) if (이름같음(metode_ievade_nosaukums[priekšējā_VALUE], metode_ievade_nosaukums[FUNCTION_VALUE])) kļūme_VALUE("duplicate method (overloading unsupported)");
            while (!Kļūda && 종류() != ')') {
                int numurs = metode_arg_COUNT[FUNCTION_VALUE];
                if (numurs == 16) { kļūme_VALUE("too many parameters"); break; }
                int TYPE_VALUE = formāts_VALUE(); if (TYPE_VALUE == 0) kļūme_VALUE("void parameter");
                metode_arg_TYPE[FUNCTION_VALUE * 16 + numurs] = TYPE_VALUE; metode_arg_nosaukums[FUNCTION_VALUE * 16 + numurs] = identifikators_VALUE();
                metode_arg_COUNT[FUNCTION_VALUE]++;
                if (!saņemt(',')) break;
            }
            prasība_VALUE(')');
            if (TAKE_Word("throws")) {
                do { 예외이름읽기(); } while (!Kļūda && saņemt(','));
            }
            metode_pamatteksts[FUNCTION_VALUE] = Novietojums; prasība_VALUE('{');
            int ligzda_VALUE = 1;
            while (Novietojums < daļiņa_COUNT && ligzda_VALUE > 0) {
                if (종류() == '{') ligzda_VALUE++;
                if (종류() == '}') ligzda_VALUE--;
                Novietojums++;
            }
            if (ligzda_VALUE != 0) kļūme_VALUE("unclosed method body");
            metode_beigt_zvanu[FUNCTION_VALUE] = Novietojums;
            metode_nosaukums_konstante[FUNCTION_VALUE] = daļiņa_konstante(metode_ievade_nosaukums[FUNCTION_VALUE]);
            문자수 = 0; Pievienot_SMS('(');
            for (int numurs = 0; numurs < metode_arg_COUNT[FUNCTION_VALUE]; numurs++) Pievienot_formāts(metode_arg_TYPE[FUNCTION_VALUE * 16 + numurs]);
            Pievienot_SMS(')'); Pievienot_formāts(metode_atdot[FUNCTION_VALUE]); 함수서술[FUNCTION_VALUE] = rakstzīme_konstante();
        }
        prasība_VALUE('}'); if (Novietojums != daļiņa_COUNT) kļūme_VALUE("extra input after class");
    }
    static int FIND_vietējs(int Nosaukums) {
        for (int numurs = vietējs_COUNT - 1; numurs >= 0; numurs--) if (지역깊이[numurs] >= 0 && 이름같음(vietējs_nosaukums[numurs], Nosaukums)) return numurs;
        kļūme_VALUE("unknown variable"); return 0;
    }
    static int Pievienot_vietējs(int Nosaukums, int TYPE_VALUE) {
        for (int numurs = 0; numurs < vietējs_COUNT; numurs++) if (지역깊이[numurs] >= 0 && 이름같음(vietējs_nosaukums[numurs], Nosaukums)) kļūme_VALUE("duplicate local variable");
        if (vietējs_COUNT == 128) { kļūme_VALUE("too many locals"); return 0; }
        vietējs_nosaukums[vietējs_COUNT] = Nosaukums; vietējs_TYPE[vietējs_COUNT] = TYPE_VALUE; 지역깊이[vietējs_COUNT] = 깊이;
        return vietējs_COUNT++;
    }
    static boolean vesels_skaitlis_TYPE(int TYPE_VALUE) { return TYPE_VALUE == 1 || TYPE_VALUE == 5; }
    static void 지역읽기(int numurs) { 내보내기(vietējs_TYPE[numurs] <= 2 || vietējs_TYPE[numurs] == 5 ? 21 : 25); 내보내기(numurs); }
    static void rakstīšana_vietējs(int numurs) { 내보내기(vietējs_TYPE[numurs] <= 2 || vietējs_TYPE[numurs] == 5 ? 54 : 58); 내보내기(numurs); }
    static void verificēt_TYPE(int faktisks_dati, int 기대) { if (faktisks_dati != 기대 && !(faktisks_dati == 5 && 기대 == 1)) kļūme_VALUE("type mismatch"); }
    static void 문자읽기(int daļiņa_VALUE) {
        문자수 = 0; int Palaist = daļiņa_amats[daļiņa_VALUE] + 1, 끝 = daļiņa_amats[daļiņa_VALUE] + 토큰길이[daļiņa_VALUE] - 1;
        while (Palaist < 끝 && !Kļūda) {
            int VALUE = AVOTS[Palaist++];
            if (VALUE == '\\') {
                if (Palaist == 끝) { kļūme_VALUE("invalid escape"); break; }
                VALUE = AVOTS[Palaist++];
                if (VALUE == 'n') VALUE = 10;
                else if (VALUE == 'r') VALUE = 13;
                else if (VALUE == 't') VALUE = 9;
                else if (VALUE == 'b') VALUE = 8;
                else if (VALUE == 'f') VALUE = 12;
                else if (VALUE != '\\' && VALUE != '"' && VALUE != '\'') kļūme_VALUE("unsupported escape");
            }
            Pievienot_SMS(VALUE);
        }
    }
    static int parsēt_vesels_skaitlis(int daļiņa_VALUE, boolean 음수) {
        if (토큰길이[daļiņa_VALUE] > 1 && AVOTS[daļiņa_amats[daļiņa_VALUE]] == '0') kļūme_VALUE("octal literals unsupported");
        int VALUE = 0;
        for (int numurs = 0; numurs < 토큰길이[daļiņa_VALUE]; numurs++) {
            int cipars_krājums = AVOTS[daļiņa_amats[daļiņa_VALUE] + numurs] - '0';
            if (VALUE < -214748364 || VALUE == -214748364 && cipars_krājums > (음수 ? 8 : 7)) kļūme_VALUE("integer literal out of range");
            VALUE = VALUE * 10 - cipars_krājums;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static int 기본식() {
        if (TAKE_Word("new")) {
            int TYPE_VALUE = formāts_VALUE();
            if (TYPE_VALUE != 6 && TYPE_VALUE != 7) { kļūme_VALUE("only file streams supported by new in source"); return 0; }
            String īpašnieks_VALUE = TYPE_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            Komanda(187, Uzziņas(7, Word_konstante(īpašnieks_VALUE), 0)); 내보내기(89);
            prasība_VALUE('('); verificēt_TYPE(izteiksme_VALUE(), 3); boolean 이어 = false;
            if (saņemt(',')) { if (TYPE_VALUE != 7) kļūme_VALUE("input stream constructor arguments"); verificēt_TYPE(izteiksme_VALUE(), 2); 이어 = true; }
            prasība_VALUE(')');
            Komanda(183, ārējs_Uzziņas(10, īpašnieks_VALUE, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return TYPE_VALUE;
        }
        if (saņemt('(')) { int TYPE_VALUE = izteiksme_VALUE(); prasība_VALUE(')'); return TYPE_VALUE; }
        if (종류() == 257) { 수상수(parsēt_vesels_skaitlis(Novietojums++, false)); return 1; }
        if (종류() == 258) { 문자읽기(Novietojums++); Komanda(19, Uzziņas(8, rakstzīme_konstante(), 0)); return 3; }
        if (종류() == 259) { 문자읽기(Novietojums++); if (문자수 != 1) kļūme_VALUE("character literal length"); 수상수(문자[0]); return 5; }
        if (TAKE_Word("true")) { 내보내기(4); return 2; }
        if (TAKE_Word("false")) { 내보내기(3); return 2; }
        if (TAKE_Word("Latviešu")) {
            prasība_VALUE('.'); 말요구("savs"); prasība_VALUE('.');
            String īpašnieks_VALUE = "", metode_VALUE = "", 서술 = ""; int 가 = 0, SECOND_operands = 0, 다 = 0, 라 = 0, 마 = 0, mērs = 0;
            if (TAKE_Word("Izvade")) {
                īpašnieks_VALUE = "Latviešu/savs/Izvade"; prasība_VALUE('.');
                if (TAKE_Word("rakstīšana_līnija")) { metode_VALUE = "rakstīšana_līnija"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("Rakstīt")) { metode_VALUE = "Rakstīt"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("rakstīšana_numurs")) { metode_VALUE = "rakstīšana_numurs"; 서술 = "(I)V"; 가 = 1; }
                else kļūme_VALUE("unknown Korean output method");
            } else if (TAKE_Word("문자")) {
                īpašnieks_VALUE = "Latviešu/savs/문자"; prasība_VALUE('.'); 가 = 3;
                if (TAKE_Word("길이")) { metode_VALUE = "길이"; 서술 = "(Ljava/lang/String;)I"; mērs = 1; }
                else if (TAKE_Word("koda_punkts_COUNT")) { metode_VALUE = "koda_punkts_COUNT"; 서술 = "(Ljava/lang/String;)I"; mērs = 1; }
                else if (TAKE_Word("parsēt_vesels_skaitlis")) { metode_VALUE = "parsēt_vesels_skaitlis"; 서술 = "(Ljava/lang/String;)I"; mērs = 1; }
                else if (TAKE_Word("rakstīšana_vesels_skaitlis_VALUE")) { metode_VALUE = "rakstīšana_vesels_skaitlis_VALUE"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; mērs = 3; }
                else if (TAKE_Word("같음")) { metode_VALUE = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; SECOND_operands = 3; mērs = 2; }
                else if (TAKE_Word("ielīmēt_SMS")) { metode_VALUE = "ielīmēt_SMS"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; SECOND_operands = 3; mērs = 3; }
                else if (TAKE_Word("izgriezt_VALUE")) { metode_VALUE = "izgriezt_VALUE"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; SECOND_operands = 1; 다 = 1; mērs = 3; }
                else kļūme_VALUE("unknown Korean text method");
            } else if (TAKE_Word("Fails")) {
                īpašnieks_VALUE = "Latviešu/savs/Fails"; prasība_VALUE('.'); 가 = 3;
                if (TAKE_Word("Lasīt")) { metode_VALUE = "Lasīt"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; mērs = 3; }
                else if (TAKE_Word("Rakstīt")) { metode_VALUE = "Rakstīt"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; SECOND_operands = 3; }
                else kļūme_VALUE("unknown Korean file method");
            } else if (TAKE_Word("화면")) {
                īpašnieks_VALUE = "Latviešu/savs/화면"; prasība_VALUE('.');
                if (TAKE_Word("너비")) { metode_VALUE = "너비"; 서술 = "()I"; mērs = 1; }
                else if (TAKE_Word("높이")) { metode_VALUE = "높이"; 서술 = "()I"; mērs = 1; }
                else if (TAKE_Word("taisnstūris")) { metode_VALUE = "taisnstūris"; 서술 = "(IIIII)V"; 가 = 1; SECOND_operands = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (TAKE_Word("dzēst_ievade")) { metode_VALUE = "dzēst_ievade"; 서술 = "(I)V"; 가 = 1; }
                else if (TAKE_Word("기다리기")) { metode_VALUE = "기다리기"; 서술 = "()V"; }
                else kļūme_VALUE("unknown Korean framebuffer method");
            } else kļūme_VALUE("unsupported Korean library class");
            prasība_VALUE('('); if (가 != 0) verificēt_TYPE(izteiksme_VALUE(), 가);
            if (SECOND_operands != 0) { prasība_VALUE(','); verificēt_TYPE(izteiksme_VALUE(), SECOND_operands); }
            if (다 != 0) { prasība_VALUE(','); verificēt_TYPE(izteiksme_VALUE(), 다); }
            if (라 != 0) { prasība_VALUE(','); verificēt_TYPE(izteiksme_VALUE(), 라); }
            if (마 != 0) { prasība_VALUE(','); verificēt_TYPE(izteiksme_VALUE(), 마); }
            prasība_VALUE(')'); Komanda(184, ārējs_Uzziņas(10, īpašnieks_VALUE, metode_VALUE, 서술)); return mērs;
        }
        if (TAKE_Word("Integer")) {
            prasība_VALUE('.'); 말요구("parseInt"); prasība_VALUE('('); verificēt_TYPE(izteiksme_VALUE(), 3); prasība_VALUE(')');
            Komanda(184, ārējs_Uzziņas(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Nosaukums = identifikators_VALUE();
        if (saņemt('(')) {
            int FUNCTION_VALUE = -1;
            for (int numurs = 0; numurs < metode_COUNT; numurs++) if (이름같음(Nosaukums, metode_ievade_nosaukums[numurs])) FUNCTION_VALUE = numurs;
            if (FUNCTION_VALUE < 0) { kļūme_VALUE("unknown static method"); return 0; }
            int numurs = 0;
            while (!Kļūda && 종류() != ')') {
                if (numurs >= metode_arg_COUNT[FUNCTION_VALUE]) { kļūme_VALUE("too many arguments"); break; }
                verificēt_TYPE(izteiksme_VALUE(), metode_arg_TYPE[FUNCTION_VALUE * 16 + numurs++]); if (!saņemt(',')) break;
            }
            prasība_VALUE(')'); if (numurs != metode_arg_COUNT[FUNCTION_VALUE]) kļūme_VALUE("argument count mismatch");
            Komanda(184, Uzziņas(10, klase_konstante, Uzziņas(12, metode_nosaukums_konstante[FUNCTION_VALUE], 함수서술[FUNCTION_VALUE])));
            return metode_atdot[FUNCTION_VALUE];
        }
        int vietējs_Tvērums = FIND_vietējs(Nosaukums), TYPE_VALUE = vietējs_TYPE[vietējs_Tvērums]; 지역읽기(vietējs_Tvērums);
        while (!Kļūda) {
            if (saņemt('[')) { verificēt_TYPE(TYPE_VALUE, 4); verificēt_TYPE(izteiksme_VALUE(), 1); prasība_VALUE(']'); 내보내기(50); TYPE_VALUE = 3; }
            else if (saņemt('.')) {
                if (TYPE_VALUE == 6 || TYPE_VALUE == 7) {
                    String īpašnieks_VALUE = TYPE_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (TAKE_Word("close")) { prasība_VALUE('('); prasība_VALUE(')'); Komanda(182, ārējs_Uzziņas(10, īpašnieks_VALUE, "close", "()V")); TYPE_VALUE = 0; }
                    else if (TYPE_VALUE == 6 && TAKE_Word("read")) { prasība_VALUE('('); prasība_VALUE(')'); Komanda(182, ārējs_Uzziņas(10, īpašnieks_VALUE, "read", "()I")); TYPE_VALUE = 1; }
                    else if (TYPE_VALUE == 7 && TAKE_Word("write")) { prasība_VALUE('('); verificēt_TYPE(izteiksme_VALUE(), 1); prasība_VALUE(')'); Komanda(182, ārējs_Uzziņas(10, īpašnieks_VALUE, "write", "(I)V")); TYPE_VALUE = 0; }
                    else { kļūme_VALUE("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (TYPE_VALUE == 4) { 내보내기(190); TYPE_VALUE = 1; }
                else { verificēt_TYPE(TYPE_VALUE, 3); prasība_VALUE('('); prasība_VALUE(')'); Komanda(182, ārējs_Uzziņas(10, "java/lang/String", "length", "()I")); TYPE_VALUE = 1; }
            } else break;
        }
        return TYPE_VALUE;
    }
    static int 단항() {
        if (++식깊이 > 64) { kļūme_VALUE("expression nesting too deep"); 식깊이--; return 0; }
        int TYPE_VALUE;
        if (saņemt('!')) { verificēt_TYPE(단항(), 2); Salīdzinājums_VALUE(153); TYPE_VALUE = 2; }
        else if (saņemt('-')) {
            if (종류() == 257) 수상수(parsēt_vesels_skaitlis(Novietojums++, true));
            else { verificēt_TYPE(단항(), 1); 내보내기(116); }
            TYPE_VALUE = 1;
        } else if (saņemt('+')) { verificēt_TYPE(단항(), 1); TYPE_VALUE = 1; }
        else TYPE_VALUE = 기본식();
        식깊이--; return TYPE_VALUE;
    }
    static int 곱식() {
        int TYPE_VALUE = 단항();
        while (!Kļūda && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int kodēšana_VALUE = 종류(); Novietojums++; verificēt_TYPE(TYPE_VALUE, 1); verificēt_TYPE(단항(), 1);
            내보내기(kodēšana_VALUE == '*' ? 104 : kodēšana_VALUE == '/' ? 108 : 112); TYPE_VALUE = 1;
        }
        return TYPE_VALUE;
    }
    static int 합식() {
        int TYPE_VALUE = 곱식();
        while (!Kļūda && (종류() == '+' || 종류() == '-')) {
            int kodēšana_VALUE = 종류(); Novietojums++; int 경계 = CODE_mainīt_izmērus, ATPAKAĻ_VALUE_TYPE = 곱식();
            if (kodēšana_VALUE == '+' && (TYPE_VALUE == 3 || ATPAKAĻ_VALUE_TYPE == 3)) { 결합(경계, TYPE_VALUE, ATPAKAĻ_VALUE_TYPE); TYPE_VALUE = 3; }
            else { verificēt_TYPE(TYPE_VALUE, 1); verificēt_TYPE(ATPAKAĻ_VALUE_TYPE, 1); 내보내기(kodēšana_VALUE == '+' ? 96 : 100); TYPE_VALUE = 1; }
        }
        return TYPE_VALUE;
    }
    static int 붙임참조(int TYPE_VALUE) {
        if (TYPE_VALUE != 1 && TYPE_VALUE != 2 && TYPE_VALUE != 3 && TYPE_VALUE != 5) kļūme_VALUE("unsupported concatenation type");
        return ārējs_Uzziņas(10, "java/lang/StringBuilder", "append", TYPE_VALUE == 1 ? "(I)Ljava/lang/StringBuilder;"
            : TYPE_VALUE == 2 ? "(Z)Ljava/lang/StringBuilder;" : TYPE_VALUE == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int 경계, int priekšējā_VALUE_TYPE, int ATPAKAĻ_VALUE_TYPE) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 RIGHT CODE_VALUE 앞에 ģenerēt 코드를 삽입한다.
        // RIGHT izteiksme_VALUE 내부의 vienranga_VALUE zars 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = CODE_mainīt_izmērus;
        Komanda(187, Uzziņas(7, Word_konstante("java/lang/StringBuilder"), 0)); 내보내기(89);
        Komanda(183, ārējs_Uzziņas(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); Komanda(182, 붙임참조(priekšējā_VALUE_TYPE));
        if (Kļūda) return;
        int 길이 = CODE_mainīt_izmērus - 끝;
        for (int numurs = 0; numurs < 길이; numurs++) 삽입코드[numurs] = CODE_VALUE[끝 + numurs];
        for (int numurs = 끝 - 1; numurs >= 경계; numurs--) CODE_VALUE[numurs + 길이] = CODE_VALUE[numurs];
        for (int numurs = 0; numurs < 길이; numurs++) CODE_VALUE[경계 + numurs] = 삽입코드[numurs];
        Komanda(182, 붙임참조(ATPAKAĻ_VALUE_TYPE)); Komanda(182, ārējs_Uzziņas(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int Salīdzinājums_izteiksme() {
        int TYPE_VALUE = 합식();
        while (!Kļūda && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int kodēšana_VALUE = 종류(); Novietojums++; verificēt_TYPE(TYPE_VALUE, 1); verificēt_TYPE(합식(), 1);
            Salīdzinājums_VALUE(kodēšana_VALUE == '<' ? 161 : kodēšana_VALUE == '>' ? 163 : kodēšana_VALUE == 302 ? 164 : 162); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int 동등식() {
        int TYPE_VALUE = Salīdzinājums_izteiksme();
        while (!Kļūda && (종류() == 300 || 종류() == 301)) {
            int kodēšana_VALUE = 종류(); Novietojums++; int ATPAKAĻ_VALUE_TYPE = Salīdzinājums_izteiksme();
            if (TYPE_VALUE == 0 || ATPAKAĻ_VALUE_TYPE == 0) kļūme_VALUE("void expression");
            if (!(vesels_skaitlis_TYPE(TYPE_VALUE) && vesels_skaitlis_TYPE(ATPAKAĻ_VALUE_TYPE))) verificēt_TYPE(ATPAKAĻ_VALUE_TYPE, TYPE_VALUE);
            Salīdzinājums_VALUE((TYPE_VALUE <= 2 || TYPE_VALUE == 5 ? 159 : 165) + (kodēšana_VALUE == 301 ? 1 : 0)); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int AND() {
        int TYPE_VALUE = 동등식();
        while (!Kļūda && saņemt(304)) {
            verificēt_TYPE(TYPE_VALUE, 2); int 가 = zars(153); verificēt_TYPE(동등식(), 2); int SECOND_operands = zars(153);
            내보내기(4); int 끝 = zars(167); Saite_VALUE(가, CODE_mainīt_izmērus); Saite_VALUE(SECOND_operands, CODE_mainīt_izmērus); 내보내기(3); Saite_VALUE(끝, CODE_mainīt_izmērus); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int izteiksme_VALUE() {
        int TYPE_VALUE = AND();
        while (!Kļūda && saņemt(305)) {
            verificēt_TYPE(TYPE_VALUE, 2); int 가 = zars(154); verificēt_TYPE(AND(), 2); int SECOND_operands = zars(154);
            내보내기(3); int 끝 = zars(167); Saite_VALUE(가, CODE_mainīt_izmērus); Saite_VALUE(SECOND_operands, CODE_mainīt_izmērus); 내보내기(4); Saite_VALUE(끝, CODE_mainīt_izmērus); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static void piešķire_VALUE(boolean Atļaut_deklarācija) {
        if (Word_VALUE(Novietojums, "int") || Word_VALUE(Novietojums, "boolean") || Word_VALUE(Novietojums, "String") || Word_VALUE(Novietojums, "char")
            || Word_VALUE(Novietojums, "FileInputStream") || Word_VALUE(Novietojums, "FileOutputStream")) {
            if (!Atļaut_deklarācija) kļūme_VALUE("declaration not allowed here");
            int TYPE_VALUE = formāts_VALUE(), Nosaukums = identifikators_VALUE(); prasība_VALUE('='); verificēt_TYPE(izteiksme_VALUE(), TYPE_VALUE);
            rakstīšana_vietējs(Pievienot_vietējs(Nosaukums, TYPE_VALUE)); return;
        }
        int Nosaukums = identifikators_VALUE(), vietējs_Tvērums = FIND_vietējs(Nosaukums);
        if (saņemt('=')) { verificēt_TYPE(izteiksme_VALUE(), vietējs_TYPE[vietējs_Tvērums]); rakstīšana_vietējs(vietējs_Tvērums); }
        else if (종류() >= 308 && 종류() <= 312) {
            int kodēšana_VALUE = 종류(); Novietojums++; 지역읽기(vietējs_Tvērums); int 경계 = CODE_mainīt_izmērus, ATPAKAĻ_VALUE_TYPE = izteiksme_VALUE();
            if (kodēšana_VALUE == 308 && vietējs_TYPE[vietējs_Tvērums] == 3) 결합(경계, 3, ATPAKAĻ_VALUE_TYPE);
            else {
                verificēt_TYPE(vietējs_TYPE[vietējs_Tvērums], 1); verificēt_TYPE(ATPAKAĻ_VALUE_TYPE, 1);
                내보내기(kodēšana_VALUE == 308 ? 96 : kodēšana_VALUE == 309 ? 100 : kodēšana_VALUE == 310 ? 104 : kodēšana_VALUE == 311 ? 108 : 112);
                if (vietējs_TYPE[vietējs_Tvērums] == 5) 내보내기(146);
            }
            rakstīšana_vietējs(vietējs_Tvērums);
        }
        else if (종류() == 306 || 종류() == 307) {
            verificēt_TYPE(vietējs_TYPE[vietējs_Tvērums], 1); 내보내기(132); 내보내기(vietējs_Tvērums); 내보내기(종류() == 306 ? 1 : 255); Novietojums++;
            if (vietējs_TYPE[vietējs_Tvērums] == 5) { 지역읽기(vietējs_Tvērums); 내보내기(146); rakstīšana_vietējs(vietējs_Tvērums); }
        } else kļūme_VALUE("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); prasība_VALUE('.'); 말요구("out"); prasība_VALUE('.');
        boolean 줄바꿈 = TAKE_Word("println"); if (!줄바꿈) 말요구("print"); prasība_VALUE('(');
        Komanda(178, ārējs_Uzziņas(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean 빈인수 = 종류() == ')';
        int TYPE_VALUE = 빈인수 ? 0 : izteiksme_VALUE(); prasība_VALUE(')'); prasība_VALUE(';');
        String 서술 = TYPE_VALUE == 0 ? "()V" : TYPE_VALUE == 1 ? "(I)V" : TYPE_VALUE == 2 ? "(Z)V" : TYPE_VALUE == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (TYPE_VALUE == 4 || TYPE_VALUE >= 6 || TYPE_VALUE == 0 && (!줄바꿈 || !빈인수)) kļūme_VALUE("unsupported print argument");
        Komanda(182, ārējs_Uzziņas(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean pārskats_VALUE() {
        if (Kļūda) return false;
        if (깊이 > 32) { kļūme_VALUE("statement nesting too deep"); return false; }
        if (saņemt('{')) {
            깊이++; boolean atdot_mērs = false;
            while (!Kļūda && 종류() != '}') { if (atdot_mērs) kļūme_VALUE("unreachable statement"); atdot_mērs = pārskats_VALUE(); }
            prasība_VALUE('}'); for (int numurs = 0; numurs < vietējs_COUNT; numurs++) if (지역깊이[numurs] == 깊이) 지역깊이[numurs] = -1;
            깊이--; return atdot_mērs;
        }
        if (saņemt(';')) return false;
        if (TAKE_Word("return")) {
            int TYPE_VALUE = 종류() == ';' ? 0 : izteiksme_VALUE(); verificēt_TYPE(TYPE_VALUE, metode_atdot[pašreizējais_metode]); prasība_VALUE(';');
            내보내기(TYPE_VALUE == 0 ? 177 : TYPE_VALUE <= 2 || TYPE_VALUE == 5 ? 172 : 176); return true;
        }
        if (TAKE_Word("if")) {
            prasība_VALUE('('); verificēt_TYPE(izteiksme_VALUE(), 2); prasība_VALUE(')'); int FALSE_VALUE = zars(153);
            깊이++; boolean 가 = vadība_pārskats(); 깊이--;
            if (TAKE_Word("else")) { int 끝 = zars(167); Saite_VALUE(FALSE_VALUE, CODE_mainīt_izmērus); 깊이++; boolean SECOND_operands = vadība_pārskats(); 깊이--; Saite_VALUE(끝, CODE_mainīt_izmērus); return 가 && SECOND_operands; }
            Saite_VALUE(FALSE_VALUE, CODE_mainīt_izmērus); return false;
        }
        if (TAKE_Word("while")) {
            int Palaist = CODE_mainīt_izmērus; prasība_VALUE('('); verificēt_TYPE(izteiksme_VALUE(), 2); prasība_VALUE(')'); int 끝 = zars(153);
            깊이++; vadība_pārskats(); 깊이--; Saite_VALUE(zars(167), Palaist); Saite_VALUE(끝, CODE_mainīt_izmērus); return false;
        }
        if (TAKE_Word("for")) {
            깊이++; prasība_VALUE('('); if (종류() != ';') piešķire_VALUE(true); prasība_VALUE(';');
            int nosacījums = CODE_mainīt_izmērus; if (종류() == ';') 내보내기(4); else verificēt_TYPE(izteiksme_VALUE(), 2); prasība_VALUE(';');
            int 끝 = zars(153), pamatteksts = zars(167), atsvaidzināt = CODE_mainīt_izmērus;
            if (종류() != ')') piešķire_VALUE(false); prasība_VALUE(')'); Saite_VALUE(zars(167), nosacījums); Saite_VALUE(pamatteksts, CODE_mainīt_izmērus);
            vadība_pārskats(); Saite_VALUE(zars(167), atsvaidzināt); Saite_VALUE(끝, CODE_mainīt_izmērus);
            for (int numurs = 0; numurs < vietējs_COUNT; numurs++) if (지역깊이[numurs] == 깊이) 지역깊이[numurs] = -1;
            깊이--; return false;
        }
        if (Word_VALUE(Novietojums, "System")) { 화면출력(); return false; }
        if (종류() == 256 && Novietojums + 1 < daļiņa_COUNT && (토큰종류[Novietojums + 1] == '(' || 토큰종류[Novietojums + 1] == '.')) {
            int TYPE_VALUE = izteiksme_VALUE(); if (TYPE_VALUE != 0) 내보내기(87); prasība_VALUE(';'); return false;
        }
        piešķire_VALUE(true); prasība_VALUE(';'); return false;
    }
    static boolean vadība_pārskats() {
        if (Word_VALUE(Novietojums, "int") || Word_VALUE(Novietojums, "boolean") || Word_VALUE(Novietojums, "char") || Word_VALUE(Novietojums, "String")
            || Word_VALUE(Novietojums, "FileInputStream") || Word_VALUE(Novietojums, "FileOutputStream")) kļūme_VALUE("local declaration requires braces");
        return pārskats_VALUE();
    }
    static void 출바(int VALUE) { if (ražojums_mainīt_izmērus == Izvade.length) kļūme_VALUE("class file too large"); else Izvade[ražojums_mainīt_izmērus++] = VALUE & 255; }
    static void 출짧(int VALUE) { 출바(VALUE >> 8); 출바(VALUE); }
    static void 출정(int VALUE) { 출짧(VALUE >>> 16); 출짧(VALUE); }
    static void rakstīšana_klase() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(konstante_COUNT);
        for (int numurs = 0; numurs < konstante_mainīt_izmērus; numurs++) 출바(konstante_VALUE[numurs]);
        출짧(0x21); 출짧(klase_konstante); 출짧(vecākobjekts_konstante); 출짧(0); 출짧(0); 출짧(metode_COUNT);
        for (int numurs = 0; numurs < metode_COUNT; numurs++) {
            출짧(metode_piekļūt[numurs]); 출짧(metode_nosaukums_konstante[numurs]); 출짧(함수서술[numurs]); 출짧(1); 출짧(CODE_konstante);
            출정(12 + 함수길이[numurs]); 출짧(128); 출짧(함수지역[numurs]); 출정(함수길이[numurs]);
            for (int 칸 = 0; 칸 < 함수길이[numurs]; 칸++) 출바(CODE_VALUE[metode_CODE[numurs] + 칸]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int Palaist() {
        if (lietotājs.인수개수() == 1 && 자바도구.같음(lietotājs.Parametri(0), "-version")) {
            lietotājs.Rakstīt("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (lietotājs.인수개수() != 1) { lietotājs.Rakstīt("Usage: javac FILE.java\n"); return 2; }
        int nosaukums_mainīt_izmērus = 자바도구.Nosaukums(faila_nosaukums_SMS, lietotājs.Parametri(0));
        if (nosaukums_mainīt_izmērus < 6 || nosaukums_mainīt_izmērus > 62 || faila_nosaukums_SMS[nosaukums_mainīt_izmērus - 5] != '.' || faila_nosaukums_SMS[nosaukums_mainīt_izmērus - 4] != 'j'
            || faila_nosaukums_SMS[nosaukums_mainīt_izmērus - 3] != 'a' || faila_nosaukums_SMS[nosaukums_mainīt_izmērus - 2] != 'v' || faila_nosaukums_SMS[nosaukums_mainīt_izmērus - 1] != 'a') {
            lietotājs.Rakstīt("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        avots_mainīt_izmērus = lietotājs.파일읽기(faila_nosaukums_SMS, AVOTS);
        if (avots_mainīt_izmērus < 0) { lietotājs.Rakstīt("javac: cannot read source: "); 자바도구.rakstīšana_numurs(avots_mainīt_izmērus); lietotājs.rakstīšana_rakstzīme_VALUE(10); return 1; }
        avots_mainīt_izmērus = 자바도구.원문해독(AVOTS, avots_mainīt_izmērus);
        if (avots_mainīt_izmērus < 0) { lietotājs.Rakstīt("javac error: invalid UTF-8 source\n"); return 1; }
        izgriezt_VALUE(); if (!Kļūda) 선언읽기();
        if (!Kļūda) {
            if (토큰길이[klase_daļiņa] != nosaukums_mainīt_izmērus - 5) kļūme_VALUE("class name must match file name");
            for (int numurs = 0; numurs < nosaukums_mainīt_izmērus - 5; numurs++) if (AVOTS[daļiņa_amats[klase_daļiņa] + numurs] != faila_nosaukums_SMS[numurs]) kļūme_VALUE("class name must match file name");
        }
        for (pašreizējais_metode = 0; pašreizējais_metode < metode_COUNT && !Kļūda; pašreizējais_metode++) {
            Novietojums = metode_pamatteksts[pašreizējais_metode]; metode_CODE[pašreizējais_metode] = CODE_mainīt_izmērus; vietējs_COUNT = 0; 깊이 = 0;
            for (int numurs = 0; numurs < metode_arg_COUNT[pašreizējais_metode]; numurs++) Pievienot_vietējs(metode_arg_nosaukums[pašreizējais_metode * 16 + numurs], metode_arg_TYPE[pašreizējais_metode * 16 + numurs]);
            boolean atdot_mērs = pārskats_VALUE();
            if (!atdot_mērs && metode_atdot[pašreizējais_metode] != 0) kļūme_VALUE("missing return");
            // zars 뒤의 합류 지점은 반드시 faktisks_dati 명령이어야 한다 (버전 49 검증기).
            if (metode_atdot[pašreizējais_metode] == 0) 내보내기(177);
            else { boolean vesels_skaitlis = metode_atdot[pašreizējais_metode] <= 2 || metode_atdot[pašreizējais_metode] == 5; 내보내기(vesels_skaitlis ? 3 : 1); 내보내기(vesels_skaitlis ? 172 : 176); }
            if (Novietojums != metode_beigt_zvanu[pašreizējais_metode]) kļūme_VALUE("invalid method body");
            함수지역[pašreizējais_metode] = vietējs_COUNT; 함수길이[pašreizējais_metode] = CODE_mainīt_izmērus - metode_CODE[pašreizējais_metode];
        }
        if (Kļūda) return 1;
        rakstīšana_klase(); if (Kļūda) return 1;
        faila_nosaukums_SMS[nosaukums_mainīt_izmērus - 4] = 'c'; faila_nosaukums_SMS[nosaukums_mainīt_izmērus - 3] = 'l'; faila_nosaukums_SMS[nosaukums_mainīt_izmērus - 2] = 'a';
        faila_nosaukums_SMS[nosaukums_mainīt_izmērus - 1] = 's'; faila_nosaukums_SMS[nosaukums_mainīt_izmērus] = 's'; faila_nosaukums_SMS[nosaukums_mainīt_izmērus + 1] = 0;
        int mērs = lietotājs.rakstīšana_Fails(faila_nosaukums_SMS, Izvade, ražojums_mainīt_izmērus);
        if (mērs < 0) { lietotājs.Rakstīt("javac: cannot save class: "); 자바도구.rakstīšana_numurs(mērs); lietotājs.rakstīšana_rakstzīme_VALUE(10); return 1; }
        lietotājs.Rakstīt("Compiled: "); for (int numurs = 0; faila_nosaukums_SMS[numurs] != 0; numurs++) lietotājs.rakstīšana_rakstzīme_VALUE(faila_nosaukums_SMS[numurs]);
        lietotājs.Rakstīt(" (JVM class version 49)\n"); return 0;
    }
}
