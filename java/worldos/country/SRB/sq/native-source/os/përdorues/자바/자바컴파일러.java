// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java burim_degëzim -> 표준 버전 49 class 컴파일러. */
public final class 자바컴파일러 {
    static int[] BURIMI = new int[16384], 출력 = new int[16384], kod_VALUE = new int[4096];
    static int[] 토큰종류 = new int[2048], kodi_pozicioni = new int[2048], kodi_gjatësi = new int[2048];
    static int[] konstante_VALUE = new int[4096], konstante_OFFSET = new int[512];
    static int[] 문자 = new int[512], skedar_emër_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int burim_ndryshoj_përmasat, kodi_COUNT, Pozicioni, kod_ndryshoj_përmasat, konstante_ndryshoj_përmasat, konstante_COUNT = 1, 출력크기, karakter_gjatësi;
    static boolean GABIM;
    static int klasë_kodi, klasë_konstante, 부모상수, kod_konstante;
    static int[] metoda_futje_emër = new int[32], metoda_Kthe = new int[32], metoda_argument_COUNT = new int[32];
    static int[] metoda_argument_emër = new int[512], metoda_argument_TYPE = new int[512];
    static int[] metoda_trupi = new int[32], metoda_mbaroj = new int[32], metoda_kod = new int[32];
    static int[] metoda_gjatësi = new int[32], 함수지역 = new int[32], metoda_emër_konstante = new int[32], 함수서술 = new int[32];
    static int[] metoda_qasem = new int[32];
    static int metoda_COUNT, 현재함수, lokal_COUNT, 깊이, 식깊이;
    static int[] lokal_emër = new int[128], lokal_TYPE = new int[128], 지역깊이 = new int[128];

    static void dështim_VALUE(String 이유) {
        if (!GABIM) {
            përdorues.Shkrimi("javac error: "); përdorues.Shkrimi(이유);
            përdorues.Shkrimi(" at line ");
            int linjë = 1, 끝 = Pozicioni < kodi_COUNT ? kodi_pozicioni[Pozicioni] : burim_ndryshoj_përmasat;
            for (int 수 = 0; 수 < 끝; 수++) if (BURIMI[수] == 10) linjë++;
            자바도구.수쓰기(linjë); përdorues.shkruaj_karakter_VALUE(10);
        }
        GABIM = true;
    }
    static boolean karakter_VALUE(int VALUE) { return 문자이름규칙.첫글자(VALUE); }
    static boolean shifër_VALUE(int VALUE) { return VALUE >= '0' && VALUE <= '9'; }
    static boolean 이름같음(int 가, int 나) {
        if (가 < 0 || 나 < 0 || 가 >= kodi_COUNT || 나 >= kodi_COUNT || kodi_gjatësi[가] != kodi_gjatësi[나]) return false;
        for (int 수 = 0; 수 < kodi_gjatësi[가]; 수++) if (BURIMI[kodi_pozicioni[가] + 수] != BURIMI[kodi_pozicioni[나] + 수]) return false;
        return true;
    }
    static boolean Word_VALUE(int kodi_VALUE, String Word_SMS) {
        if (kodi_VALUE < 0 || kodi_VALUE >= kodi_COUNT || kodi_gjatësi[kodi_VALUE] != Word_SMS.length()) return false;
        for (int 수 = 0; 수 < Word_SMS.length(); 수++) if (BURIMI[kodi_pozicioni[kodi_VALUE] + 수] != Word_SMS.charAt(수)) return false;
        return true;
    }
    static int 종류() { return Pozicioni < kodi_COUNT ? 토큰종류[Pozicioni] : 0; }
    static boolean 받기(int VALUE) { if (종류() != VALUE) return false; Pozicioni++; return true; }
    static void 요구(int VALUE) { if (!받기(VALUE)) dështim_VALUE("unexpected token"); }
    static boolean TAKE_Word(String Word_SMS) { if (!Word_VALUE(Pozicioni, Word_SMS)) return false; Pozicioni++; return true; }
    static void 말요구(String Word_SMS) { if (!TAKE_Word(Word_SMS)) dështim_VALUE(Word_SMS); }
    static int identifikues_VALUE() {
        int llogaritje = Pozicioni;
        if (종류() != 256) dështim_VALUE("identifier required"); else Pozicioni++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int Ekzekuto = 0;
        for (int 수 = 0; 수 <= 예약어.length(); 수++) {
            if (수 == 예약어.length() || 예약어.charAt(수) == ' ') {
                boolean 같음 = 수 - Ekzekuto == kodi_gjatësi[llogaritje];
                for (int hapësirë_për_tekst_futje = Ekzekuto; 같음 && hapësirë_për_tekst_futje < 수; hapësirë_për_tekst_futje++) if (예약어.charAt(hapësirë_për_tekst_futje) != BURIMI[kodi_pozicioni[llogaritje] + hapësirë_për_tekst_futje - Ekzekuto]) 같음 = false;
                if (같음) dështim_VALUE("reserved word cannot be an identifier");
                Ekzekuto = 수 + 1;
            }
        }
        return llogaritje;
    }
    static void pres_VALUE() {
        int 수 = 0;
        while (수 < burim_ndryshoj_përmasat && !GABIM) {
            int VALUE = BURIMI[수], Ekzekuto = 수, 종류 = VALUE;
            if (VALUE == 32 || VALUE == 9 || VALUE == 10 || VALUE == 13) { 수++; continue; }
            if (VALUE == '/' && 수 + 1 < burim_ndryshoj_përmasat && BURIMI[수 + 1] == '/') {
                while (수 < burim_ndryshoj_përmasat && BURIMI[수] != 10) 수++;
                continue;
            }
            if (VALUE == '/' && 수 + 1 < burim_ndryshoj_përmasat && BURIMI[수 + 1] == '*') {
                수 += 2;
                while (수 + 1 < burim_ndryshoj_përmasat && !(BURIMI[수] == '*' && BURIMI[수 + 1] == '/')) 수++;
                if (수 + 1 >= burim_ndryshoj_përmasat) { dështim_VALUE("unterminated comment"); break; }
                수 += 2; continue;
            }
            if (karakter_VALUE(VALUE)) { 종류 = 256; while (수 < burim_ndryshoj_përmasat && 문자이름규칙.이어진글자(BURIMI[수])) 수++; }
            else if (shifër_VALUE(VALUE)) { 종류 = 257; while (수 < burim_ndryshoj_përmasat && shifër_VALUE(BURIMI[수])) 수++; }
            else if (VALUE == '"' || VALUE == '\'') {
                종류 = VALUE == '"' ? 258 : 259; 수++;
                while (수 < burim_ndryshoj_përmasat && BURIMI[수] != VALUE && BURIMI[수] != 10 && BURIMI[수] != 13) {
                    if (BURIMI[수] == '\\') 수++;
                    수++;
                }
                if (수 >= burim_ndryshoj_përmasat || BURIMI[수] != VALUE) { dështim_VALUE("unterminated literal"); break; }
                수++;
            } else {
                수++;
                if (수 < burim_ndryshoj_përmasat) {
                    int Tjetër_njësi = BURIMI[수];
                    if (VALUE == '=' && Tjetër_njësi == '=') 종류 = 300;
                    if (VALUE == '!' && Tjetër_njësi == '=') 종류 = 301;
                    if (VALUE == '<' && Tjetër_njësi == '=') 종류 = 302;
                    if (VALUE == '>' && Tjetër_njësi == '=') 종류 = 303;
                    if (VALUE == '&' && Tjetër_njësi == '&') 종류 = 304;
                    if (VALUE == '|' && Tjetër_njësi == '|') 종류 = 305;
                    if (VALUE == '+' && Tjetër_njësi == '+') 종류 = 306;
                    if (VALUE == '-' && Tjetër_njësi == '-') 종류 = 307;
                    if (VALUE == '+' && Tjetër_njësi == '=') 종류 = 308;
                    if (VALUE == '-' && Tjetër_njësi == '=') 종류 = 309;
                    if (VALUE == '*' && Tjetër_njësi == '=') 종류 = 310;
                    if (VALUE == '/' && Tjetër_njësi == '=') 종류 = 311;
                    if (VALUE == '%' && Tjetër_njësi == '=') 종류 = 312;
                    if (종류 >= 300) 수++;
                }
            }
            if (kodi_COUNT == 토큰종류.length - 1) { dështim_VALUE("too many tokens (2047 maximum)"); break; }
            토큰종류[kodi_COUNT] = 종류; kodi_pozicioni[kodi_COUNT] = Ekzekuto; kodi_gjatësi[kodi_COUNT++] = 수 - Ekzekuto;
        }
    }
    static void shkruaj_konstante_bajt(int VALUE) {
        if (konstante_ndryshoj_përmasat == konstante_VALUE.length) { dështim_VALUE("constant pool too large"); return; }
        konstante_VALUE[konstante_ndryshoj_përmasat++] = VALUE & 255;
    }
    static void 상짧(int VALUE) { shkruaj_konstante_bajt(VALUE >> 8); shkruaj_konstante_bajt(VALUE); }
    static int regjistroj_konstante(int Ekzekuto) {
        for (int 수 = 1; 수 < konstante_COUNT; 수++) {
            int e_përparme_VALUE = konstante_OFFSET[수], gjatësi_VALUE = (수 + 1 < konstante_COUNT ? konstante_OFFSET[수 + 1] : Ekzekuto) - e_përparme_VALUE;
            if (gjatësi_VALUE != konstante_ndryshoj_përmasat - Ekzekuto) continue;
            boolean 같음 = true;
            for (int hapësirë_për_tekst_futje = 0; hapësirë_për_tekst_futje < gjatësi_VALUE; hapësirë_për_tekst_futje++) if (konstante_VALUE[e_përparme_VALUE + hapësirë_për_tekst_futje] != konstante_VALUE[Ekzekuto + hapësirë_për_tekst_futje]) 같음 = false;
            if (같음) { konstante_ndryshoj_përmasat = Ekzekuto; return 수; }
        }
        if (konstante_COUNT == konstante_OFFSET.length) { dështim_VALUE("too many constants"); return 0; }
        konstante_OFFSET[konstante_COUNT] = Ekzekuto;
        return konstante_COUNT++;
    }
    static void 글추가(int VALUE) {
        if (karakter_gjatësi == 문자.length) { dështim_VALUE("text too long"); return; }
        문자[karakter_gjatësi++] = VALUE;
    }
    static void 말추가(String Word_SMS) { for (int 수 = 0; 수 < Word_SMS.length(); 수++) 글추가(Word_SMS.charAt(수)); }
    static int karakter_konstante() {
        int Ekzekuto = konstante_ndryshoj_përmasat; shkruaj_konstante_bajt(1); 상짧(0);
        for (int 수 = 0; 수 < karakter_gjatësi; 수++) {
            int VALUE = 문자[수];
            if (VALUE > 0 && VALUE < 128) shkruaj_konstante_bajt(VALUE);
            else if (VALUE < 2048) { shkruaj_konstante_bajt(192 | VALUE >> 6); shkruaj_konstante_bajt(128 | VALUE & 63); }
            else { shkruaj_konstante_bajt(224 | VALUE >> 12); shkruaj_konstante_bajt(128 | VALUE >> 6 & 63); shkruaj_konstante_bajt(128 | VALUE & 63); }
        }
        if (GABIM) return 0;
        int gjatësi_VALUE = konstante_ndryshoj_përmasat - Ekzekuto - 3;
        konstante_VALUE[Ekzekuto + 1] = gjatësi_VALUE >> 8; konstante_VALUE[Ekzekuto + 2] = gjatësi_VALUE & 255;
        return regjistroj_konstante(Ekzekuto);
    }
    static int Word_konstante(String Word_SMS) { karakter_gjatësi = 0; 말추가(Word_SMS); return karakter_konstante(); }
    static int kodi_konstante(int kodi_VALUE) {
        karakter_gjatësi = 0;
        for (int 수 = 0; 수 < kodi_gjatësi[kodi_VALUE]; 수++) 글추가(BURIMI[kodi_pozicioni[kodi_VALUE] + 수]);
        return karakter_konstante();
    }
    static int Referencë(int 종류, int 가, int 나) {
        int Ekzekuto = konstante_ndryshoj_përmasat; shkruaj_konstante_bajt(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(나);
        return regjistroj_konstante(Ekzekuto);
    }
    static int 외부참조(int 종류, String pronari_VALUE, String Emër, String 서술) {
        int pronari_identifikues = Referencë(7, Word_konstante(pronari_VALUE), 0);
        int emër_COUNT = Word_konstante(Emër), format_COUNT = Word_konstante(서술);
        return Referencë(종류, pronari_identifikues, Referencë(12, emër_COUNT, format_COUNT));
    }
    static void 내보내기(int VALUE) {
        if (kod_ndryshoj_përmasat == kod_VALUE.length) { dështim_VALUE("bytecode too large"); return; }
        kod_VALUE[kod_ndryshoj_përmasat++] = VALUE & 255;
    }
    static void Komanda(int VALUE, int Argumente) { 내보내기(VALUE); 내보내기(Argumente >> 8); 내보내기(Argumente); }
    static void 수상수(int VALUE) {
        if (VALUE >= -1 && VALUE <= 5) { 내보내기(VALUE + 3); return; }
        int Ekzekuto = konstante_ndryshoj_përmasat; shkruaj_konstante_bajt(3); 상짧(VALUE >>> 16); 상짧(VALUE);
        Komanda(19, regjistroj_konstante(Ekzekuto));
    }
    static int degë(int Komanda) { int llogaritje = kod_ndryshoj_përmasat; Komanda(Komanda, 0); return llogaritje; }
    static void lidh_VALUE(int degë, int objektiv_objekt) {
        if (GABIM) return;
        int 거리 = objektiv_objekt - degë;
        if (거리 < -32768 || 거리 > 32767 || degë < 0 || degë + 2 >= kod_ndryshoj_përmasat) { dështim_VALUE("invalid branch"); return; }
        kod_VALUE[degë + 1] = 거리 >> 8 & 255; kod_VALUE[degë + 2] = 거리 & 255;
    }
    static void Krahasim_VALUE(int Komanda) {
        int TRUE_VALUE = degë(Komanda); 내보내기(3); int 끝 = degë(167);
        lidh_VALUE(TRUE_VALUE, kod_ndryshoj_përmasat); 내보내기(4); lidh_VALUE(끝, kod_ndryshoj_përmasat);
    }
    static int format_VALUE() {
        if (TAKE_Word("void")) return 0;
        if (TAKE_Word("int")) return 1;
        if (TAKE_Word("boolean")) return 2;
        if (TAKE_Word("char")) return 5;
        if (TAKE_Word("FileInputStream")) return 6;
        if (TAKE_Word("FileOutputStream")) return 7;
        if (TAKE_Word("String")) { if (받기('[')) { 요구(']'); return 4; } return 3; }
        dështim_VALUE("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void shto_format(int TYPE_VALUE) {
        if (TYPE_VALUE == 0) 글추가('V');
        if (TYPE_VALUE == 1) 글추가('I');
        if (TYPE_VALUE == 2) 글추가('Z');
        if (TYPE_VALUE == 3) 말추가("Ljava/lang/String;");
        if (TYPE_VALUE == 4) 말추가("[Ljava/lang/String;");
        if (TYPE_VALUE == 5) 글추가('C');
        if (TYPE_VALUE == 6) 말추가("Ljava/io/FileInputStream;");
        if (TYPE_VALUE == 7) 말추가("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws deklarata. përjashtim Proces_VALUE_futje 본문은 pritës javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = TAKE_Word("한국어");
        if (한국어묶음) { 요구('.'); 말요구("자체"); 요구('.'); }
        if (!한국어묶음 && (TAKE_Word("Exception") || TAKE_Word("IOException"))) return;
        if (TAKE_Word("përjashtim") || TAKE_Word("실행예외") || TAKE_Word("I_O_përjashtim") || TAKE_Word("Prit_TIMEOUT_përjashtim") || TAKE_Word("email_LOOKUP_përjashtim") || TAKE_Word("파일없음예외") || TAKE_Word("통신예외") || TAKE_Word("i_pavlefshëm_argument_përjashtim") || TAKE_Word("숫자형식예외") || TAKE_Word("범위예외") || TAKE_Word("배열범위예외") || TAKE_Word("문자열범위예외") || TAKE_Word("NUL_Referencë_përjashtim") || TAKE_Word("산술예외") || TAKE_Word("status_përjashtim") || TAKE_Word("TYPE_Transmetim_përjashtim") || TAKE_Word("음수배열크기예외") || TAKE_Word("ARRAY_Store_dështim") || TAKE_Word("thread_status_përjashtim") || TAKE_Word("대기중단예외")) return;
        dështim_VALUE("unsupported throws type");
    }
    static void 선언읽기() {
        while (TAKE_Word("import")) {
            if (Word_VALUE(Pozicioni, "한국어")) 예외이름읽기();
            else {
                말요구("java"); 요구('.'); 말요구("io"); 요구('.');
                if (!(TAKE_Word("FileInputStream") || TAKE_Word("FileOutputStream") || TAKE_Word("IOException"))) dështim_VALUE("unsupported import");
            }
            요구(';');
        }
        TAKE_Word("public"); TAKE_Word("final"); 말요구("class"); klasë_kodi = identifikues_VALUE();
        klasë_konstante = Referencë(7, kodi_konstante(klasë_kodi), 0);
        부모상수 = Referencë(7, Word_konstante("java/lang/Object"), 0); kod_konstante = Word_konstante("Code"); 요구('{');
        while (!GABIM && 종류() != '}') {
            if (metoda_COUNT == 32) { dështim_VALUE("too many methods"); break; }
            int qasem_futje = TAKE_Word("public") ? 1 : TAKE_Word("private") ? 2 : 0; 말요구("static");
            int FUNCTION_VALUE = metoda_COUNT++;
            metoda_qasem[FUNCTION_VALUE] = qasem_futje | 8;
            metoda_Kthe[FUNCTION_VALUE] = format_VALUE(); metoda_futje_emër[FUNCTION_VALUE] = identifikues_VALUE(); 요구('(');
            for (int e_përparme_VALUE = 0; e_përparme_VALUE < FUNCTION_VALUE; e_përparme_VALUE++) if (이름같음(metoda_futje_emër[e_përparme_VALUE], metoda_futje_emër[FUNCTION_VALUE])) dështim_VALUE("duplicate method (overloading unsupported)");
            while (!GABIM && 종류() != ')') {
                int 수 = metoda_argument_COUNT[FUNCTION_VALUE];
                if (수 == 16) { dështim_VALUE("too many parameters"); break; }
                int TYPE_VALUE = format_VALUE(); if (TYPE_VALUE == 0) dështim_VALUE("void parameter");
                metoda_argument_TYPE[FUNCTION_VALUE * 16 + 수] = TYPE_VALUE; metoda_argument_emër[FUNCTION_VALUE * 16 + 수] = identifikues_VALUE();
                metoda_argument_COUNT[FUNCTION_VALUE]++;
                if (!받기(',')) break;
            }
            요구(')');
            if (TAKE_Word("throws")) {
                do { 예외이름읽기(); } while (!GABIM && 받기(','));
            }
            metoda_trupi[FUNCTION_VALUE] = Pozicioni; 요구('{');
            int ndërthurje_VALUE = 1;
            while (Pozicioni < kodi_COUNT && ndërthurje_VALUE > 0) {
                if (종류() == '{') ndërthurje_VALUE++;
                if (종류() == '}') ndërthurje_VALUE--;
                Pozicioni++;
            }
            if (ndërthurje_VALUE != 0) dështim_VALUE("unclosed method body");
            metoda_mbaroj[FUNCTION_VALUE] = Pozicioni;
            metoda_emër_konstante[FUNCTION_VALUE] = kodi_konstante(metoda_futje_emër[FUNCTION_VALUE]);
            karakter_gjatësi = 0; 글추가('(');
            for (int 수 = 0; 수 < metoda_argument_COUNT[FUNCTION_VALUE]; 수++) shto_format(metoda_argument_TYPE[FUNCTION_VALUE * 16 + 수]);
            글추가(')'); shto_format(metoda_Kthe[FUNCTION_VALUE]); 함수서술[FUNCTION_VALUE] = karakter_konstante();
        }
        요구('}'); if (Pozicioni != kodi_COUNT) dështim_VALUE("extra input after class");
    }
    static int FIND_lokal(int Emër) {
        for (int 수 = lokal_COUNT - 1; 수 >= 0; 수--) if (지역깊이[수] >= 0 && 이름같음(lokal_emër[수], Emër)) return 수;
        dështim_VALUE("unknown variable"); return 0;
    }
    static int shto_lokal(int Emër, int TYPE_VALUE) {
        for (int 수 = 0; 수 < lokal_COUNT; 수++) if (지역깊이[수] >= 0 && 이름같음(lokal_emër[수], Emër)) dështim_VALUE("duplicate local variable");
        if (lokal_COUNT == 128) { dështim_VALUE("too many locals"); return 0; }
        lokal_emër[lokal_COUNT] = Emër; lokal_TYPE[lokal_COUNT] = TYPE_VALUE; 지역깊이[lokal_COUNT] = 깊이;
        return lokal_COUNT++;
    }
    static boolean numër_i_plotë_TYPE(int TYPE_VALUE) { return TYPE_VALUE == 1 || TYPE_VALUE == 5; }
    static void 지역읽기(int 수) { 내보내기(lokal_TYPE[수] <= 2 || lokal_TYPE[수] == 5 ? 21 : 25); 내보내기(수); }
    static void shkruaj_lokal(int 수) { 내보내기(lokal_TYPE[수] <= 2 || lokal_TYPE[수] == 5 ? 54 : 58); 내보내기(수); }
    static void verifikoj_TYPE(int aktual_të_dhëna, int 기대) { if (aktual_të_dhëna != 기대 && !(aktual_të_dhëna == 5 && 기대 == 1)) dështim_VALUE("type mismatch"); }
    static void 문자읽기(int kodi_VALUE) {
        karakter_gjatësi = 0; int Ekzekuto = kodi_pozicioni[kodi_VALUE] + 1, 끝 = kodi_pozicioni[kodi_VALUE] + kodi_gjatësi[kodi_VALUE] - 1;
        while (Ekzekuto < 끝 && !GABIM) {
            int VALUE = BURIMI[Ekzekuto++];
            if (VALUE == '\\') {
                if (Ekzekuto == 끝) { dështim_VALUE("invalid escape"); break; }
                VALUE = BURIMI[Ekzekuto++];
                if (VALUE == 'n') VALUE = 10;
                else if (VALUE == 'r') VALUE = 13;
                else if (VALUE == 't') VALUE = 9;
                else if (VALUE == 'b') VALUE = 8;
                else if (VALUE == 'f') VALUE = 12;
                else if (VALUE != '\\' && VALUE != '"' && VALUE != '\'') dështim_VALUE("unsupported escape");
            }
            글추가(VALUE);
        }
    }
    static int analizoj_numër_i_plotë(int kodi_VALUE, boolean 음수) {
        if (kodi_gjatësi[kodi_VALUE] > 1 && BURIMI[kodi_pozicioni[kodi_VALUE]] == '0') dështim_VALUE("octal literals unsupported");
        int VALUE = 0;
        for (int 수 = 0; 수 < kodi_gjatësi[kodi_VALUE]; 수++) {
            int shifër_njësi = BURIMI[kodi_pozicioni[kodi_VALUE] + 수] - '0';
            if (VALUE < -214748364 || VALUE == -214748364 && shifër_njësi > (음수 ? 8 : 7)) dështim_VALUE("integer literal out of range");
            VALUE = VALUE * 10 - shifër_njësi;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static int 기본식() {
        if (TAKE_Word("new")) {
            int TYPE_VALUE = format_VALUE();
            if (TYPE_VALUE != 6 && TYPE_VALUE != 7) { dështim_VALUE("only file streams supported by new in source"); return 0; }
            String pronari_VALUE = TYPE_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            Komanda(187, Referencë(7, Word_konstante(pronari_VALUE), 0)); 내보내기(89);
            요구('('); verifikoj_TYPE(shprehje_VALUE(), 3); boolean 이어 = false;
            if (받기(',')) { if (TYPE_VALUE != 7) dështim_VALUE("input stream constructor arguments"); verifikoj_TYPE(shprehje_VALUE(), 2); 이어 = true; }
            요구(')');
            Komanda(183, 외부참조(10, pronari_VALUE, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return TYPE_VALUE;
        }
        if (받기('(')) { int TYPE_VALUE = shprehje_VALUE(); 요구(')'); return TYPE_VALUE; }
        if (종류() == 257) { 수상수(analizoj_numër_i_plotë(Pozicioni++, false)); return 1; }
        if (종류() == 258) { 문자읽기(Pozicioni++); Komanda(19, Referencë(8, karakter_konstante(), 0)); return 3; }
        if (종류() == 259) { 문자읽기(Pozicioni++); if (karakter_gjatësi != 1) dështim_VALUE("character literal length"); 수상수(문자[0]); return 5; }
        if (TAKE_Word("true")) { 내보내기(4); return 2; }
        if (TAKE_Word("false")) { 내보내기(3); return 2; }
        if (TAKE_Word("한국어")) {
            요구('.'); 말요구("자체"); 요구('.');
            String pronari_VALUE = "", metoda_VALUE = "", 서술 = ""; int 가 = 0, 나 = 0, 다 = 0, 라 = 0, 마 = 0, llogaritje = 0;
            if (TAKE_Word("출력")) {
                pronari_VALUE = "한국어/자체/출력"; 요구('.');
                if (TAKE_Word("shkruaj_linjë")) { metoda_VALUE = "shkruaj_linjë"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("Shkrimi")) { metoda_VALUE = "Shkrimi"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("수쓰기")) { metoda_VALUE = "수쓰기"; 서술 = "(I)V"; 가 = 1; }
                else dështim_VALUE("unknown Korean output method");
            } else if (TAKE_Word("문자")) {
                pronari_VALUE = "한국어/자체/문자"; 요구('.'); 가 = 3;
                if (TAKE_Word("gjatësi_VALUE")) { metoda_VALUE = "gjatësi_VALUE"; 서술 = "(Ljava/lang/String;)I"; llogaritje = 1; }
                else if (TAKE_Word("kodi_i_karakterit_COUNT")) { metoda_VALUE = "kodi_i_karakterit_COUNT"; 서술 = "(Ljava/lang/String;)I"; llogaritje = 1; }
                else if (TAKE_Word("analizoj_numër_i_plotë")) { metoda_VALUE = "analizoj_numër_i_plotë"; 서술 = "(Ljava/lang/String;)I"; llogaritje = 1; }
                else if (TAKE_Word("shkruaj_numër_i_plotë_VALUE")) { metoda_VALUE = "shkruaj_numër_i_plotë_VALUE"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; llogaritje = 3; }
                else if (TAKE_Word("같음")) { metoda_VALUE = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; 나 = 3; llogaritje = 2; }
                else if (TAKE_Word("ngjit_SMS")) { metoda_VALUE = "ngjit_SMS"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; 나 = 3; llogaritje = 3; }
                else if (TAKE_Word("pres_VALUE")) { metoda_VALUE = "pres_VALUE"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; 나 = 1; 다 = 1; llogaritje = 3; }
                else dështim_VALUE("unknown Korean text method");
            } else if (TAKE_Word("Kartelë")) {
                pronari_VALUE = "한국어/자체/Kartelë"; 요구('.'); 가 = 3;
                if (TAKE_Word("Leximi")) { metoda_VALUE = "Leximi"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; llogaritje = 3; }
                else if (TAKE_Word("Shkrimi")) { metoda_VALUE = "Shkrimi"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; 나 = 3; }
                else dështim_VALUE("unknown Korean file method");
            } else if (TAKE_Word("화면")) {
                pronari_VALUE = "한국어/자체/화면"; 요구('.');
                if (TAKE_Word("너비")) { metoda_VALUE = "너비"; 서술 = "()I"; llogaritje = 1; }
                else if (TAKE_Word("높이")) { metoda_VALUE = "높이"; 서술 = "()I"; llogaritje = 1; }
                else if (TAKE_Word("사각형")) { metoda_VALUE = "사각형"; 서술 = "(IIIII)V"; 가 = 1; 나 = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (TAKE_Word("spastroj_futje")) { metoda_VALUE = "spastroj_futje"; 서술 = "(I)V"; 가 = 1; }
                else if (TAKE_Word("기다리기")) { metoda_VALUE = "기다리기"; 서술 = "()V"; }
                else dështim_VALUE("unknown Korean framebuffer method");
            } else dështim_VALUE("unsupported Korean library class");
            요구('('); if (가 != 0) verifikoj_TYPE(shprehje_VALUE(), 가);
            if (나 != 0) { 요구(','); verifikoj_TYPE(shprehje_VALUE(), 나); }
            if (다 != 0) { 요구(','); verifikoj_TYPE(shprehje_VALUE(), 다); }
            if (라 != 0) { 요구(','); verifikoj_TYPE(shprehje_VALUE(), 라); }
            if (마 != 0) { 요구(','); verifikoj_TYPE(shprehje_VALUE(), 마); }
            요구(')'); Komanda(184, 외부참조(10, pronari_VALUE, metoda_VALUE, 서술)); return llogaritje;
        }
        if (TAKE_Word("Integer")) {
            요구('.'); 말요구("parseInt"); 요구('('); verifikoj_TYPE(shprehje_VALUE(), 3); 요구(')');
            Komanda(184, 외부참조(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Emër = identifikues_VALUE();
        if (받기('(')) {
            int FUNCTION_VALUE = -1;
            for (int 수 = 0; 수 < metoda_COUNT; 수++) if (이름같음(Emër, metoda_futje_emër[수])) FUNCTION_VALUE = 수;
            if (FUNCTION_VALUE < 0) { dështim_VALUE("unknown static method"); return 0; }
            int 수 = 0;
            while (!GABIM && 종류() != ')') {
                if (수 >= metoda_argument_COUNT[FUNCTION_VALUE]) { dështim_VALUE("too many arguments"); break; }
                verifikoj_TYPE(shprehje_VALUE(), metoda_argument_TYPE[FUNCTION_VALUE * 16 + 수++]); if (!받기(',')) break;
            }
            요구(')'); if (수 != metoda_argument_COUNT[FUNCTION_VALUE]) dështim_VALUE("argument count mismatch");
            Komanda(184, Referencë(10, klasë_konstante, Referencë(12, metoda_emër_konstante[FUNCTION_VALUE], 함수서술[FUNCTION_VALUE])));
            return metoda_Kthe[FUNCTION_VALUE];
        }
        int lokal_fushë = FIND_lokal(Emër), TYPE_VALUE = lokal_TYPE[lokal_fushë]; 지역읽기(lokal_fushë);
        while (!GABIM) {
            if (받기('[')) { verifikoj_TYPE(TYPE_VALUE, 4); verifikoj_TYPE(shprehje_VALUE(), 1); 요구(']'); 내보내기(50); TYPE_VALUE = 3; }
            else if (받기('.')) {
                if (TYPE_VALUE == 6 || TYPE_VALUE == 7) {
                    String pronari_VALUE = TYPE_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (TAKE_Word("close")) { 요구('('); 요구(')'); Komanda(182, 외부참조(10, pronari_VALUE, "close", "()V")); TYPE_VALUE = 0; }
                    else if (TYPE_VALUE == 6 && TAKE_Word("read")) { 요구('('); 요구(')'); Komanda(182, 외부참조(10, pronari_VALUE, "read", "()I")); TYPE_VALUE = 1; }
                    else if (TYPE_VALUE == 7 && TAKE_Word("write")) { 요구('('); verifikoj_TYPE(shprehje_VALUE(), 1); 요구(')'); Komanda(182, 외부참조(10, pronari_VALUE, "write", "(I)V")); TYPE_VALUE = 0; }
                    else { dështim_VALUE("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (TYPE_VALUE == 4) { 내보내기(190); TYPE_VALUE = 1; }
                else { verifikoj_TYPE(TYPE_VALUE, 3); 요구('('); 요구(')'); Komanda(182, 외부참조(10, "java/lang/String", "length", "()I")); TYPE_VALUE = 1; }
            } else break;
        }
        return TYPE_VALUE;
    }
    static int 단항() {
        if (++식깊이 > 64) { dështim_VALUE("expression nesting too deep"); 식깊이--; return 0; }
        int TYPE_VALUE;
        if (받기('!')) { verifikoj_TYPE(단항(), 2); Krahasim_VALUE(153); TYPE_VALUE = 2; }
        else if (받기('-')) {
            if (종류() == 257) 수상수(analizoj_numër_i_plotë(Pozicioni++, true));
            else { verifikoj_TYPE(단항(), 1); 내보내기(116); }
            TYPE_VALUE = 1;
        } else if (받기('+')) { verifikoj_TYPE(단항(), 1); TYPE_VALUE = 1; }
        else TYPE_VALUE = 기본식();
        식깊이--; return TYPE_VALUE;
    }
    static int 곱식() {
        int TYPE_VALUE = 단항();
        while (!GABIM && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int enkodim_VALUE = 종류(); Pozicioni++; verifikoj_TYPE(TYPE_VALUE, 1); verifikoj_TYPE(단항(), 1);
            내보내기(enkodim_VALUE == '*' ? 104 : enkodim_VALUE == '/' ? 108 : 112); TYPE_VALUE = 1;
        }
        return TYPE_VALUE;
    }
    static int 합식() {
        int TYPE_VALUE = 곱식();
        while (!GABIM && (종류() == '+' || 종류() == '-')) {
            int enkodim_VALUE = 종류(); Pozicioni++; int 경계 = kod_ndryshoj_përmasat, PAS_VALUE_TYPE = 곱식();
            if (enkodim_VALUE == '+' && (TYPE_VALUE == 3 || PAS_VALUE_TYPE == 3)) { 결합(경계, TYPE_VALUE, PAS_VALUE_TYPE); TYPE_VALUE = 3; }
            else { verifikoj_TYPE(TYPE_VALUE, 1); verifikoj_TYPE(PAS_VALUE_TYPE, 1); 내보내기(enkodim_VALUE == '+' ? 96 : 100); TYPE_VALUE = 1; }
        }
        return TYPE_VALUE;
    }
    static int 붙임참조(int TYPE_VALUE) {
        if (TYPE_VALUE != 1 && TYPE_VALUE != 2 && TYPE_VALUE != 3 && TYPE_VALUE != 5) dështim_VALUE("unsupported concatenation type");
        return 외부참조(10, "java/lang/StringBuilder", "append", TYPE_VALUE == 1 ? "(I)Ljava/lang/StringBuilder;"
            : TYPE_VALUE == 2 ? "(Z)Ljava/lang/StringBuilder;" : TYPE_VALUE == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int 경계, int e_përparme_VALUE_TYPE, int PAS_VALUE_TYPE) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 RIGHT kod_VALUE 앞에 gjeneroj 코드를 삽입한다.
        // RIGHT shprehje_VALUE 내부의 homolog_VALUE degë 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = kod_ndryshoj_përmasat;
        Komanda(187, Referencë(7, Word_konstante("java/lang/StringBuilder"), 0)); 내보내기(89);
        Komanda(183, 외부참조(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); Komanda(182, 붙임참조(e_përparme_VALUE_TYPE));
        if (GABIM) return;
        int gjatësi_VALUE = kod_ndryshoj_përmasat - 끝;
        for (int 수 = 0; 수 < gjatësi_VALUE; 수++) 삽입코드[수] = kod_VALUE[끝 + 수];
        for (int 수 = 끝 - 1; 수 >= 경계; 수--) kod_VALUE[수 + gjatësi_VALUE] = kod_VALUE[수];
        for (int 수 = 0; 수 < gjatësi_VALUE; 수++) kod_VALUE[경계 + 수] = 삽입코드[수];
        Komanda(182, 붙임참조(PAS_VALUE_TYPE)); Komanda(182, 외부참조(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int Krahasim_shprehje() {
        int TYPE_VALUE = 합식();
        while (!GABIM && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int enkodim_VALUE = 종류(); Pozicioni++; verifikoj_TYPE(TYPE_VALUE, 1); verifikoj_TYPE(합식(), 1);
            Krahasim_VALUE(enkodim_VALUE == '<' ? 161 : enkodim_VALUE == '>' ? 163 : enkodim_VALUE == 302 ? 164 : 162); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int 동등식() {
        int TYPE_VALUE = Krahasim_shprehje();
        while (!GABIM && (종류() == 300 || 종류() == 301)) {
            int enkodim_VALUE = 종류(); Pozicioni++; int PAS_VALUE_TYPE = Krahasim_shprehje();
            if (TYPE_VALUE == 0 || PAS_VALUE_TYPE == 0) dështim_VALUE("void expression");
            if (!(numër_i_plotë_TYPE(TYPE_VALUE) && numër_i_plotë_TYPE(PAS_VALUE_TYPE))) verifikoj_TYPE(PAS_VALUE_TYPE, TYPE_VALUE);
            Krahasim_VALUE((TYPE_VALUE <= 2 || TYPE_VALUE == 5 ? 159 : 165) + (enkodim_VALUE == 301 ? 1 : 0)); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int 논리곱() {
        int TYPE_VALUE = 동등식();
        while (!GABIM && 받기(304)) {
            verifikoj_TYPE(TYPE_VALUE, 2); int 가 = degë(153); verifikoj_TYPE(동등식(), 2); int 나 = degë(153);
            내보내기(4); int 끝 = degë(167); lidh_VALUE(가, kod_ndryshoj_përmasat); lidh_VALUE(나, kod_ndryshoj_përmasat); 내보내기(3); lidh_VALUE(끝, kod_ndryshoj_përmasat); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int shprehje_VALUE() {
        int TYPE_VALUE = 논리곱();
        while (!GABIM && 받기(305)) {
            verifikoj_TYPE(TYPE_VALUE, 2); int 가 = degë(154); verifikoj_TYPE(논리곱(), 2); int 나 = degë(154);
            내보내기(3); int 끝 = degë(167); lidh_VALUE(가, kod_ndryshoj_përmasat); lidh_VALUE(나, kod_ndryshoj_përmasat); 내보내기(4); lidh_VALUE(끝, kod_ndryshoj_përmasat); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static void detyrë_VALUE(boolean Lejoj_deklarata) {
        if (Word_VALUE(Pozicioni, "int") || Word_VALUE(Pozicioni, "boolean") || Word_VALUE(Pozicioni, "String") || Word_VALUE(Pozicioni, "char")
            || Word_VALUE(Pozicioni, "FileInputStream") || Word_VALUE(Pozicioni, "FileOutputStream")) {
            if (!Lejoj_deklarata) dështim_VALUE("declaration not allowed here");
            int TYPE_VALUE = format_VALUE(), Emër = identifikues_VALUE(); 요구('='); verifikoj_TYPE(shprehje_VALUE(), TYPE_VALUE);
            shkruaj_lokal(shto_lokal(Emër, TYPE_VALUE)); return;
        }
        int Emër = identifikues_VALUE(), lokal_fushë = FIND_lokal(Emër);
        if (받기('=')) { verifikoj_TYPE(shprehje_VALUE(), lokal_TYPE[lokal_fushë]); shkruaj_lokal(lokal_fushë); }
        else if (종류() >= 308 && 종류() <= 312) {
            int enkodim_VALUE = 종류(); Pozicioni++; 지역읽기(lokal_fushë); int 경계 = kod_ndryshoj_përmasat, PAS_VALUE_TYPE = shprehje_VALUE();
            if (enkodim_VALUE == 308 && lokal_TYPE[lokal_fushë] == 3) 결합(경계, 3, PAS_VALUE_TYPE);
            else {
                verifikoj_TYPE(lokal_TYPE[lokal_fushë], 1); verifikoj_TYPE(PAS_VALUE_TYPE, 1);
                내보내기(enkodim_VALUE == 308 ? 96 : enkodim_VALUE == 309 ? 100 : enkodim_VALUE == 310 ? 104 : enkodim_VALUE == 311 ? 108 : 112);
                if (lokal_TYPE[lokal_fushë] == 5) 내보내기(146);
            }
            shkruaj_lokal(lokal_fushë);
        }
        else if (종류() == 306 || 종류() == 307) {
            verifikoj_TYPE(lokal_TYPE[lokal_fushë], 1); 내보내기(132); 내보내기(lokal_fushë); 내보내기(종류() == 306 ? 1 : 255); Pozicioni++;
            if (lokal_TYPE[lokal_fushë] == 5) { 지역읽기(lokal_fushë); 내보내기(146); shkruaj_lokal(lokal_fushë); }
        } else dështim_VALUE("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); 요구('.'); 말요구("out"); 요구('.');
        boolean 줄바꿈 = TAKE_Word("println"); if (!줄바꿈) 말요구("print"); 요구('(');
        Komanda(178, 외부참조(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean bosh_argument = 종류() == ')';
        int TYPE_VALUE = bosh_argument ? 0 : shprehje_VALUE(); 요구(')'); 요구(';');
        String 서술 = TYPE_VALUE == 0 ? "()V" : TYPE_VALUE == 1 ? "(I)V" : TYPE_VALUE == 2 ? "(Z)V" : TYPE_VALUE == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (TYPE_VALUE == 4 || TYPE_VALUE >= 6 || TYPE_VALUE == 0 && (!줄바꿈 || !bosh_argument)) dështim_VALUE("unsupported print argument");
        Komanda(182, 외부참조(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean deklarim_VALUE() {
        if (GABIM) return false;
        if (깊이 > 32) { dështim_VALUE("statement nesting too deep"); return false; }
        if (받기('{')) {
            깊이++; boolean Kthe_llogaritje = false;
            while (!GABIM && 종류() != '}') { if (Kthe_llogaritje) dështim_VALUE("unreachable statement"); Kthe_llogaritje = deklarim_VALUE(); }
            요구('}'); for (int 수 = 0; 수 < lokal_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return Kthe_llogaritje;
        }
        if (받기(';')) return false;
        if (TAKE_Word("return")) {
            int TYPE_VALUE = 종류() == ';' ? 0 : shprehje_VALUE(); verifikoj_TYPE(TYPE_VALUE, metoda_Kthe[현재함수]); 요구(';');
            내보내기(TYPE_VALUE == 0 ? 177 : TYPE_VALUE <= 2 || TYPE_VALUE == 5 ? 172 : 176); return true;
        }
        if (TAKE_Word("if")) {
            요구('('); verifikoj_TYPE(shprehje_VALUE(), 2); 요구(')'); int FALSE_VALUE = degë(153);
            깊이++; boolean 가 = kontroll_deklarim(); 깊이--;
            if (TAKE_Word("else")) { int 끝 = degë(167); lidh_VALUE(FALSE_VALUE, kod_ndryshoj_përmasat); 깊이++; boolean 나 = kontroll_deklarim(); 깊이--; lidh_VALUE(끝, kod_ndryshoj_përmasat); return 가 && 나; }
            lidh_VALUE(FALSE_VALUE, kod_ndryshoj_përmasat); return false;
        }
        if (TAKE_Word("while")) {
            int Ekzekuto = kod_ndryshoj_përmasat; 요구('('); verifikoj_TYPE(shprehje_VALUE(), 2); 요구(')'); int 끝 = degë(153);
            깊이++; kontroll_deklarim(); 깊이--; lidh_VALUE(degë(167), Ekzekuto); lidh_VALUE(끝, kod_ndryshoj_përmasat); return false;
        }
        if (TAKE_Word("for")) {
            깊이++; 요구('('); if (종류() != ';') detyrë_VALUE(true); 요구(';');
            int kusht = kod_ndryshoj_përmasat; if (종류() == ';') 내보내기(4); else verifikoj_TYPE(shprehje_VALUE(), 2); 요구(';');
            int 끝 = degë(153), trupi_i_tekstit = degë(167), freskoj = kod_ndryshoj_përmasat;
            if (종류() != ')') detyrë_VALUE(false); 요구(')'); lidh_VALUE(degë(167), kusht); lidh_VALUE(trupi_i_tekstit, kod_ndryshoj_përmasat);
            kontroll_deklarim(); lidh_VALUE(degë(167), freskoj); lidh_VALUE(끝, kod_ndryshoj_përmasat);
            for (int 수 = 0; 수 < lokal_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return false;
        }
        if (Word_VALUE(Pozicioni, "System")) { 화면출력(); return false; }
        if (종류() == 256 && Pozicioni + 1 < kodi_COUNT && (토큰종류[Pozicioni + 1] == '(' || 토큰종류[Pozicioni + 1] == '.')) {
            int TYPE_VALUE = shprehje_VALUE(); if (TYPE_VALUE != 0) 내보내기(87); 요구(';'); return false;
        }
        detyrë_VALUE(true); 요구(';'); return false;
    }
    static boolean kontroll_deklarim() {
        if (Word_VALUE(Pozicioni, "int") || Word_VALUE(Pozicioni, "boolean") || Word_VALUE(Pozicioni, "char") || Word_VALUE(Pozicioni, "String")
            || Word_VALUE(Pozicioni, "FileInputStream") || Word_VALUE(Pozicioni, "FileOutputStream")) dështim_VALUE("local declaration requires braces");
        return deklarim_VALUE();
    }
    static void 출바(int VALUE) { if (출력크기 == 출력.length) dështim_VALUE("class file too large"); else 출력[출력크기++] = VALUE & 255; }
    static void 출짧(int VALUE) { 출바(VALUE >> 8); 출바(VALUE); }
    static void 출정(int VALUE) { 출짧(VALUE >>> 16); 출짧(VALUE); }
    static void shkruaj_klasë() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(konstante_COUNT);
        for (int 수 = 0; 수 < konstante_ndryshoj_përmasat; 수++) 출바(konstante_VALUE[수]);
        출짧(0x21); 출짧(klasë_konstante); 출짧(부모상수); 출짧(0); 출짧(0); 출짧(metoda_COUNT);
        for (int 수 = 0; 수 < metoda_COUNT; 수++) {
            출짧(metoda_qasem[수]); 출짧(metoda_emër_konstante[수]); 출짧(함수서술[수]); 출짧(1); 출짧(kod_konstante);
            출정(12 + metoda_gjatësi[수]); 출짧(128); 출짧(함수지역[수]); 출정(metoda_gjatësi[수]);
            for (int hapësirë_për_tekst_futje = 0; hapësirë_për_tekst_futje < metoda_gjatësi[수]; hapësirë_për_tekst_futje++) 출바(kod_VALUE[metoda_kod[수] + hapësirë_për_tekst_futje]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int Ekzekuto() {
        if (përdorues.인수개수() == 1 && 자바도구.같음(përdorues.Argumente(0), "-version")) {
            përdorues.Shkrimi("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (përdorues.인수개수() != 1) { përdorues.Shkrimi("Usage: javac FILE.java\n"); return 2; }
        int emër_ndryshoj_përmasat = 자바도구.Emër(skedar_emër_SMS, përdorues.Argumente(0));
        if (emër_ndryshoj_përmasat < 6 || emër_ndryshoj_përmasat > 62 || skedar_emër_SMS[emër_ndryshoj_përmasat - 5] != '.' || skedar_emër_SMS[emër_ndryshoj_përmasat - 4] != 'j'
            || skedar_emër_SMS[emër_ndryshoj_përmasat - 3] != 'a' || skedar_emër_SMS[emër_ndryshoj_përmasat - 2] != 'v' || skedar_emër_SMS[emër_ndryshoj_përmasat - 1] != 'a') {
            përdorues.Shkrimi("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        burim_ndryshoj_përmasat = përdorues.파일읽기(skedar_emër_SMS, BURIMI);
        if (burim_ndryshoj_përmasat < 0) { përdorues.Shkrimi("javac: cannot read source: "); 자바도구.수쓰기(burim_ndryshoj_përmasat); përdorues.shkruaj_karakter_VALUE(10); return 1; }
        burim_ndryshoj_përmasat = 자바도구.원문해독(BURIMI, burim_ndryshoj_përmasat);
        if (burim_ndryshoj_përmasat < 0) { përdorues.Shkrimi("javac error: invalid UTF-8 source\n"); return 1; }
        pres_VALUE(); if (!GABIM) 선언읽기();
        if (!GABIM) {
            if (kodi_gjatësi[klasë_kodi] != emër_ndryshoj_përmasat - 5) dështim_VALUE("class name must match file name");
            for (int 수 = 0; 수 < emër_ndryshoj_përmasat - 5; 수++) if (BURIMI[kodi_pozicioni[klasë_kodi] + 수] != skedar_emër_SMS[수]) dështim_VALUE("class name must match file name");
        }
        for (현재함수 = 0; 현재함수 < metoda_COUNT && !GABIM; 현재함수++) {
            Pozicioni = metoda_trupi[현재함수]; metoda_kod[현재함수] = kod_ndryshoj_përmasat; lokal_COUNT = 0; 깊이 = 0;
            for (int 수 = 0; 수 < metoda_argument_COUNT[현재함수]; 수++) shto_lokal(metoda_argument_emër[현재함수 * 16 + 수], metoda_argument_TYPE[현재함수 * 16 + 수]);
            boolean Kthe_llogaritje = deklarim_VALUE();
            if (!Kthe_llogaritje && metoda_Kthe[현재함수] != 0) dështim_VALUE("missing return");
            // degë 뒤의 합류 지점은 반드시 aktual_të_dhëna 명령이어야 한다 (버전 49 검증기).
            if (metoda_Kthe[현재함수] == 0) 내보내기(177);
            else { boolean numër_i_plotë = metoda_Kthe[현재함수] <= 2 || metoda_Kthe[현재함수] == 5; 내보내기(numër_i_plotë ? 3 : 1); 내보내기(numër_i_plotë ? 172 : 176); }
            if (Pozicioni != metoda_mbaroj[현재함수]) dështim_VALUE("invalid method body");
            함수지역[현재함수] = lokal_COUNT; metoda_gjatësi[현재함수] = kod_ndryshoj_përmasat - metoda_kod[현재함수];
        }
        if (GABIM) return 1;
        shkruaj_klasë(); if (GABIM) return 1;
        skedar_emër_SMS[emër_ndryshoj_përmasat - 4] = 'c'; skedar_emër_SMS[emër_ndryshoj_përmasat - 3] = 'l'; skedar_emër_SMS[emër_ndryshoj_përmasat - 2] = 'a';
        skedar_emër_SMS[emër_ndryshoj_përmasat - 1] = 's'; skedar_emër_SMS[emër_ndryshoj_përmasat] = 's'; skedar_emër_SMS[emër_ndryshoj_përmasat + 1] = 0;
        int llogaritje = përdorues.shkruaj_skedar(skedar_emër_SMS, 출력, 출력크기);
        if (llogaritje < 0) { përdorues.Shkrimi("javac: cannot save class: "); 자바도구.수쓰기(llogaritje); përdorues.shkruaj_karakter_VALUE(10); return 1; }
        përdorues.Shkrimi("Compiled: "); for (int 수 = 0; skedar_emër_SMS[수] != 0; 수++) përdorues.shkruaj_karakter_VALUE(skedar_emër_SMS[수]);
        përdorues.Shkrimi(" (JVM class version 49)\n"); return 0;
    }
}
