// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java bron_boom -> 표준 버전 49 class 컴파일러. */
public final class 자바컴파일러 {
    static int[] Bron = new int[16384], Afvoer = new int[16384], CODE_VALUE = new int[4096];
    static int[] 토큰종류 = new int[2048], kenteken_plaas = new int[2048], kenteken_lengte = new int[2048];
    static int[] konstante_VALUE = new int[4096], konstante_OFFSET = new int[512];
    static int[] 문자 = new int[512], lêer_naam_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int bron_verstel, kenteken_COUNT, Posisie, CODE_verstel, konstante_verstel, konstante_COUNT = 1, 출력크기, karakter_lengte;
    static boolean Fout;
    static int Klas_kenteken, Klas_konstante, 부모상수, CODE_konstante;
    static int[] metode_inskrywing_naam = new int[32], metode_teruggee = new int[32], metode_argument_COUNT = new int[32];
    static int[] metode_argument_naam = new int[512], metode_argument_TYPE = new int[512];
    static int[] 함수본문 = new int[32], metode_beëindig = new int[32], metode_CODE = new int[32];
    static int[] metode_lengte = new int[32], 함수지역 = new int[32], metode_naam_konstante = new int[32], 함수서술 = new int[32];
    static int[] metode_toegang = new int[32];
    static int metode_COUNT, 현재함수, lokaal_COUNT, 깊이, 식깊이;
    static int[] lokaal_naam = new int[128], lokaal_TYPE = new int[128], 지역깊이 = new int[128];

    static void faling_VALUE(String 이유) {
        if (!Fout) {
            gebruiker.Skryf("javac error: "); gebruiker.Skryf(이유);
            gebruiker.Skryf(" at line ");
            int lyn = 1, 끝 = Posisie < kenteken_COUNT ? kenteken_plaas[Posisie] : bron_verstel;
            for (int 수 = 0; 수 < 끝; 수++) if (Bron[수] == 10) lyn++;
            자바도구.수쓰기(lyn); gebruiker.skryf_karakter_VALUE(10);
        }
        Fout = true;
    }
    static boolean karakter_VALUE(int VALUE) { return 문자이름규칙.첫글자(VALUE); }
    static boolean syfer_VALUE(int VALUE) { return VALUE >= '0' && VALUE <= '9'; }
    static boolean 이름같음(int 가, int 나) {
        if (가 < 0 || 나 < 0 || 가 >= kenteken_COUNT || 나 >= kenteken_COUNT || kenteken_lengte[가] != kenteken_lengte[나]) return false;
        for (int 수 = 0; 수 < kenteken_lengte[가]; 수++) if (Bron[kenteken_plaas[가] + 수] != Bron[kenteken_plaas[나] + 수]) return false;
        return true;
    }
    static boolean Word_VALUE(int kenteken_VALUE, String Word_SMS) {
        if (kenteken_VALUE < 0 || kenteken_VALUE >= kenteken_COUNT || kenteken_lengte[kenteken_VALUE] != Word_SMS.length()) return false;
        for (int 수 = 0; 수 < Word_SMS.length(); 수++) if (Bron[kenteken_plaas[kenteken_VALUE] + 수] != Word_SMS.charAt(수)) return false;
        return true;
    }
    static int 종류() { return Posisie < kenteken_COUNT ? 토큰종류[Posisie] : 0; }
    static boolean 받기(int VALUE) { if (종류() != VALUE) return false; Posisie++; return true; }
    static void 요구(int VALUE) { if (!받기(VALUE)) faling_VALUE("unexpected token"); }
    static boolean TAKE_Word(String Word_SMS) { if (!Word_VALUE(Posisie, Word_SMS)) return false; Posisie++; return true; }
    static void 말요구(String Word_SMS) { if (!TAKE_Word(Word_SMS)) faling_VALUE(Word_SMS); }
    static int waarde_VALUE() {
        int maatreël = Posisie;
        if (종류() != 256) faling_VALUE("identifier required"); else Posisie++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int Loop = 0;
        for (int 수 = 0; 수 <= 예약어.length(); 수++) {
            if (수 == 예약어.length() || 예약어.charAt(수) == ' ') {
                boolean 같음 = 수 - Loop == kenteken_lengte[maatreël];
                for (int gleuf_inskrywing = Loop; 같음 && gleuf_inskrywing < 수; gleuf_inskrywing++) if (예약어.charAt(gleuf_inskrywing) != Bron[kenteken_plaas[maatreël] + gleuf_inskrywing - Loop]) 같음 = false;
                if (같음) faling_VALUE("reserved word cannot be an identifier");
                Loop = 수 + 1;
            }
        }
        return maatreël;
    }
    static void sny_VALUE() {
        int 수 = 0;
        while (수 < bron_verstel && !Fout) {
            int VALUE = Bron[수], Loop = 수, 종류 = VALUE;
            if (VALUE == 32 || VALUE == 9 || VALUE == 10 || VALUE == 13) { 수++; continue; }
            if (VALUE == '/' && 수 + 1 < bron_verstel && Bron[수 + 1] == '/') {
                while (수 < bron_verstel && Bron[수] != 10) 수++;
                continue;
            }
            if (VALUE == '/' && 수 + 1 < bron_verstel && Bron[수 + 1] == '*') {
                수 += 2;
                while (수 + 1 < bron_verstel && !(Bron[수] == '*' && Bron[수 + 1] == '/')) 수++;
                if (수 + 1 >= bron_verstel) { faling_VALUE("unterminated comment"); break; }
                수 += 2; continue;
            }
            if (karakter_VALUE(VALUE)) { 종류 = 256; while (수 < bron_verstel && 문자이름규칙.이어진글자(Bron[수])) 수++; }
            else if (syfer_VALUE(VALUE)) { 종류 = 257; while (수 < bron_verstel && syfer_VALUE(Bron[수])) 수++; }
            else if (VALUE == '"' || VALUE == '\'') {
                종류 = VALUE == '"' ? 258 : 259; 수++;
                while (수 < bron_verstel && Bron[수] != VALUE && Bron[수] != 10 && Bron[수] != 13) {
                    if (Bron[수] == '\\') 수++;
                    수++;
                }
                if (수 >= bron_verstel || Bron[수] != VALUE) { faling_VALUE("unterminated literal"); break; }
                수++;
            } else {
                수++;
                if (수 < bron_verstel) {
                    int Volgende_item = Bron[수];
                    if (VALUE == '=' && Volgende_item == '=') 종류 = 300;
                    if (VALUE == '!' && Volgende_item == '=') 종류 = 301;
                    if (VALUE == '<' && Volgende_item == '=') 종류 = 302;
                    if (VALUE == '>' && Volgende_item == '=') 종류 = 303;
                    if (VALUE == '&' && Volgende_item == '&') 종류 = 304;
                    if (VALUE == '|' && Volgende_item == '|') 종류 = 305;
                    if (VALUE == '+' && Volgende_item == '+') 종류 = 306;
                    if (VALUE == '-' && Volgende_item == '-') 종류 = 307;
                    if (VALUE == '+' && Volgende_item == '=') 종류 = 308;
                    if (VALUE == '-' && Volgende_item == '=') 종류 = 309;
                    if (VALUE == '*' && Volgende_item == '=') 종류 = 310;
                    if (VALUE == '/' && Volgende_item == '=') 종류 = 311;
                    if (VALUE == '%' && Volgende_item == '=') 종류 = 312;
                    if (종류 >= 300) 수++;
                }
            }
            if (kenteken_COUNT == 토큰종류.length - 1) { faling_VALUE("too many tokens (2047 maximum)"); break; }
            토큰종류[kenteken_COUNT] = 종류; kenteken_plaas[kenteken_COUNT] = Loop; kenteken_lengte[kenteken_COUNT++] = 수 - Loop;
        }
    }
    static void skryf_konstante_greep(int VALUE) {
        if (konstante_verstel == konstante_VALUE.length) { faling_VALUE("constant pool too large"); return; }
        konstante_VALUE[konstante_verstel++] = VALUE & 255;
    }
    static void 상짧(int VALUE) { skryf_konstante_greep(VALUE >> 8); skryf_konstante_greep(VALUE); }
    static int registreer_konstante(int Loop) {
        for (int 수 = 1; 수 < konstante_COUNT; 수++) {
            int voor_VALUE = konstante_OFFSET[수], lengte_VALUE = (수 + 1 < konstante_COUNT ? konstante_OFFSET[수 + 1] : Loop) - voor_VALUE;
            if (lengte_VALUE != konstante_verstel - Loop) continue;
            boolean 같음 = true;
            for (int gleuf_inskrywing = 0; gleuf_inskrywing < lengte_VALUE; gleuf_inskrywing++) if (konstante_VALUE[voor_VALUE + gleuf_inskrywing] != konstante_VALUE[Loop + gleuf_inskrywing]) 같음 = false;
            if (같음) { konstante_verstel = Loop; return 수; }
        }
        if (konstante_COUNT == konstante_OFFSET.length) { faling_VALUE("too many constants"); return 0; }
        konstante_OFFSET[konstante_COUNT] = Loop;
        return konstante_COUNT++;
    }
    static void 글추가(int VALUE) {
        if (karakter_lengte == 문자.length) { faling_VALUE("text too long"); return; }
        문자[karakter_lengte++] = VALUE;
    }
    static void 말추가(String Word_SMS) { for (int 수 = 0; 수 < Word_SMS.length(); 수++) 글추가(Word_SMS.charAt(수)); }
    static int karakter_konstante() {
        int Loop = konstante_verstel; skryf_konstante_greep(1); 상짧(0);
        for (int 수 = 0; 수 < karakter_lengte; 수++) {
            int VALUE = 문자[수];
            if (VALUE > 0 && VALUE < 128) skryf_konstante_greep(VALUE);
            else if (VALUE < 2048) { skryf_konstante_greep(192 | VALUE >> 6); skryf_konstante_greep(128 | VALUE & 63); }
            else { skryf_konstante_greep(224 | VALUE >> 12); skryf_konstante_greep(128 | VALUE >> 6 & 63); skryf_konstante_greep(128 | VALUE & 63); }
        }
        if (Fout) return 0;
        int lengte_VALUE = konstante_verstel - Loop - 3;
        konstante_VALUE[Loop + 1] = lengte_VALUE >> 8; konstante_VALUE[Loop + 2] = lengte_VALUE & 255;
        return registreer_konstante(Loop);
    }
    static int Word_konstante(String Word_SMS) { karakter_lengte = 0; 말추가(Word_SMS); return karakter_konstante(); }
    static int kenteken_konstante(int kenteken_VALUE) {
        karakter_lengte = 0;
        for (int 수 = 0; 수 < kenteken_lengte[kenteken_VALUE]; 수++) 글추가(Bron[kenteken_plaas[kenteken_VALUE] + 수]);
        return karakter_konstante();
    }
    static int Naslaan(int 종류, int 가, int 나) {
        int Loop = konstante_verstel; skryf_konstante_greep(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(나);
        return registreer_konstante(Loop);
    }
    static int 외부참조(int 종류, String eienaar_VALUE, String Naam, String 서술) {
        int eienaar_waarde = Naslaan(7, Word_konstante(eienaar_VALUE), 0);
        int naam_COUNT = Word_konstante(Naam), formaat_COUNT = Word_konstante(서술);
        return Naslaan(종류, eienaar_waarde, Naslaan(12, naam_COUNT, formaat_COUNT));
    }
    static void 내보내기(int VALUE) {
        if (CODE_verstel == CODE_VALUE.length) { faling_VALUE("bytecode too large"); return; }
        CODE_VALUE[CODE_verstel++] = VALUE & 255;
    }
    static void Opdrag(int VALUE, int 인수) { 내보내기(VALUE); 내보내기(인수 >> 8); 내보내기(인수); }
    static void 수상수(int VALUE) {
        if (VALUE >= -1 && VALUE <= 5) { 내보내기(VALUE + 3); return; }
        int Loop = konstante_verstel; skryf_konstante_greep(3); 상짧(VALUE >>> 16); 상짧(VALUE);
        Opdrag(19, registreer_konstante(Loop));
    }
    static int tak(int Opdrag) { int maatreël = CODE_verstel; Opdrag(Opdrag, 0); return maatreël; }
    static void Skakel_VALUE(int tak, int teiken_objek) {
        if (Fout) return;
        int 거리 = teiken_objek - tak;
        if (거리 < -32768 || 거리 > 32767 || tak < 0 || tak + 2 >= CODE_verstel) { faling_VALUE("invalid branch"); return; }
        CODE_VALUE[tak + 1] = 거리 >> 8 & 255; CODE_VALUE[tak + 2] = 거리 & 255;
    }
    static void Vergelyking_VALUE(int Opdrag) {
        int TRUE_VALUE = tak(Opdrag); 내보내기(3); int 끝 = tak(167);
        Skakel_VALUE(TRUE_VALUE, CODE_verstel); 내보내기(4); Skakel_VALUE(끝, CODE_verstel);
    }
    static int formaat_VALUE() {
        if (TAKE_Word("void")) return 0;
        if (TAKE_Word("int")) return 1;
        if (TAKE_Word("boolean")) return 2;
        if (TAKE_Word("char")) return 5;
        if (TAKE_Word("FileInputStream")) return 6;
        if (TAKE_Word("FileOutputStream")) return 7;
        if (TAKE_Word("String")) { if (받기('[')) { 요구(']'); return 4; } return 3; }
        faling_VALUE("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void byvoeg_formaat(int TYPE_VALUE) {
        if (TYPE_VALUE == 0) 글추가('V');
        if (TYPE_VALUE == 1) 글추가('I');
        if (TYPE_VALUE == 2) 글추가('Z');
        if (TYPE_VALUE == 3) 말추가("Ljava/lang/String;");
        if (TYPE_VALUE == 4) 말추가("[Ljava/lang/String;");
        if (TYPE_VALUE == 5) 글추가('C');
        if (TYPE_VALUE == 6) 말추가("Ljava/io/FileInputStream;");
        if (TYPE_VALUE == 7) 말추가("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws verklaring. uitsondering Proses_VALUE_inskrywing 본문은 hou javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = TAKE_Word("한국어");
        if (한국어묶음) { 요구('.'); 말요구("자체"); 요구('.'); }
        if (!한국어묶음 && (TAKE_Word("Exception") || TAKE_Word("IOException"))) return;
        if (TAKE_Word("uitsondering") || TAKE_Word("실행예외") || TAKE_Word("I_O_uitsondering") || TAKE_Word("wag_UITTELLING_uitsondering") || TAKE_Word("adres_LOOKUP_uitsondering") || TAKE_Word("파일없음예외") || TAKE_Word("통신예외") || TAKE_Word("ongeldig_argument_uitsondering") || TAKE_Word("숫자형식예외") || TAKE_Word("범위예외") || TAKE_Word("배열범위예외") || TAKE_Word("문자열범위예외") || TAKE_Word("nul_Naslaan_uitsondering") || TAKE_Word("산술예외") || TAKE_Word("stand_uitsondering") || TAKE_Word("TYPE_Uitsaai_uitsondering") || TAKE_Word("음수배열크기예외") || TAKE_Word("ARRAY_bêre_faling") || TAKE_Word("draad_stand_uitsondering") || TAKE_Word("대기중단예외")) return;
        faling_VALUE("unsupported throws type");
    }
    static void 선언읽기() {
        while (TAKE_Word("import")) {
            if (Word_VALUE(Posisie, "한국어")) 예외이름읽기();
            else {
                말요구("java"); 요구('.'); 말요구("io"); 요구('.');
                if (!(TAKE_Word("FileInputStream") || TAKE_Word("FileOutputStream") || TAKE_Word("IOException"))) faling_VALUE("unsupported import");
            }
            요구(';');
        }
        TAKE_Word("public"); TAKE_Word("final"); 말요구("class"); Klas_kenteken = waarde_VALUE();
        Klas_konstante = Naslaan(7, kenteken_konstante(Klas_kenteken), 0);
        부모상수 = Naslaan(7, Word_konstante("java/lang/Object"), 0); CODE_konstante = Word_konstante("Code"); 요구('{');
        while (!Fout && 종류() != '}') {
            if (metode_COUNT == 32) { faling_VALUE("too many methods"); break; }
            int toegang_inskrywing = TAKE_Word("public") ? 1 : TAKE_Word("private") ? 2 : 0; 말요구("static");
            int funksie_VALUE = metode_COUNT++;
            metode_toegang[funksie_VALUE] = toegang_inskrywing | 8;
            metode_teruggee[funksie_VALUE] = formaat_VALUE(); metode_inskrywing_naam[funksie_VALUE] = waarde_VALUE(); 요구('(');
            for (int voor_VALUE = 0; voor_VALUE < funksie_VALUE; voor_VALUE++) if (이름같음(metode_inskrywing_naam[voor_VALUE], metode_inskrywing_naam[funksie_VALUE])) faling_VALUE("duplicate method (overloading unsupported)");
            while (!Fout && 종류() != ')') {
                int 수 = metode_argument_COUNT[funksie_VALUE];
                if (수 == 16) { faling_VALUE("too many parameters"); break; }
                int TYPE_VALUE = formaat_VALUE(); if (TYPE_VALUE == 0) faling_VALUE("void parameter");
                metode_argument_TYPE[funksie_VALUE * 16 + 수] = TYPE_VALUE; metode_argument_naam[funksie_VALUE * 16 + 수] = waarde_VALUE();
                metode_argument_COUNT[funksie_VALUE]++;
                if (!받기(',')) break;
            }
            요구(')');
            if (TAKE_Word("throws")) {
                do { 예외이름읽기(); } while (!Fout && 받기(','));
            }
            함수본문[funksie_VALUE] = Posisie; 요구('{');
            int nes_VALUE = 1;
            while (Posisie < kenteken_COUNT && nes_VALUE > 0) {
                if (종류() == '{') nes_VALUE++;
                if (종류() == '}') nes_VALUE--;
                Posisie++;
            }
            if (nes_VALUE != 0) faling_VALUE("unclosed method body");
            metode_beëindig[funksie_VALUE] = Posisie;
            metode_naam_konstante[funksie_VALUE] = kenteken_konstante(metode_inskrywing_naam[funksie_VALUE]);
            karakter_lengte = 0; 글추가('(');
            for (int 수 = 0; 수 < metode_argument_COUNT[funksie_VALUE]; 수++) byvoeg_formaat(metode_argument_TYPE[funksie_VALUE * 16 + 수]);
            글추가(')'); byvoeg_formaat(metode_teruggee[funksie_VALUE]); 함수서술[funksie_VALUE] = karakter_konstante();
        }
        요구('}'); if (Posisie != kenteken_COUNT) faling_VALUE("extra input after class");
    }
    static int FIND_lokaal(int Naam) {
        for (int 수 = lokaal_COUNT - 1; 수 >= 0; 수--) if (지역깊이[수] >= 0 && 이름같음(lokaal_naam[수], Naam)) return 수;
        faling_VALUE("unknown variable"); return 0;
    }
    static int byvoeg_lokaal(int Naam, int TYPE_VALUE) {
        for (int 수 = 0; 수 < lokaal_COUNT; 수++) if (지역깊이[수] >= 0 && 이름같음(lokaal_naam[수], Naam)) faling_VALUE("duplicate local variable");
        if (lokaal_COUNT == 128) { faling_VALUE("too many locals"); return 0; }
        lokaal_naam[lokaal_COUNT] = Naam; lokaal_TYPE[lokaal_COUNT] = TYPE_VALUE; 지역깊이[lokaal_COUNT] = 깊이;
        return lokaal_COUNT++;
    }
    static boolean heelgetal_TYPE(int TYPE_VALUE) { return TYPE_VALUE == 1 || TYPE_VALUE == 5; }
    static void 지역읽기(int 수) { 내보내기(lokaal_TYPE[수] <= 2 || lokaal_TYPE[수] == 5 ? 21 : 25); 내보내기(수); }
    static void skryf_lokaal(int 수) { 내보내기(lokaal_TYPE[수] <= 2 || lokaal_TYPE[수] == 5 ? 54 : 58); 내보내기(수); }
    static void verifieer_TYPE(int werklik_data, int 기대) { if (werklik_data != 기대 && !(werklik_data == 5 && 기대 == 1)) faling_VALUE("type mismatch"); }
    static void 문자읽기(int kenteken_VALUE) {
        karakter_lengte = 0; int Loop = kenteken_plaas[kenteken_VALUE] + 1, 끝 = kenteken_plaas[kenteken_VALUE] + kenteken_lengte[kenteken_VALUE] - 1;
        while (Loop < 끝 && !Fout) {
            int VALUE = Bron[Loop++];
            if (VALUE == '\\') {
                if (Loop == 끝) { faling_VALUE("invalid escape"); break; }
                VALUE = Bron[Loop++];
                if (VALUE == 'n') VALUE = 10;
                else if (VALUE == 'r') VALUE = 13;
                else if (VALUE == 't') VALUE = 9;
                else if (VALUE == 'b') VALUE = 8;
                else if (VALUE == 'f') VALUE = 12;
                else if (VALUE != '\\' && VALUE != '"' && VALUE != '\'') faling_VALUE("unsupported escape");
            }
            글추가(VALUE);
        }
    }
    static int ontleed_heelgetal(int kenteken_VALUE, boolean 음수) {
        if (kenteken_lengte[kenteken_VALUE] > 1 && Bron[kenteken_plaas[kenteken_VALUE]] == '0') faling_VALUE("octal literals unsupported");
        int VALUE = 0;
        for (int 수 = 0; 수 < kenteken_lengte[kenteken_VALUE]; 수++) {
            int syfer_item = Bron[kenteken_plaas[kenteken_VALUE] + 수] - '0';
            if (VALUE < -214748364 || VALUE == -214748364 && syfer_item > (음수 ? 8 : 7)) faling_VALUE("integer literal out of range");
            VALUE = VALUE * 10 - syfer_item;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static int 기본식() {
        if (TAKE_Word("new")) {
            int TYPE_VALUE = formaat_VALUE();
            if (TYPE_VALUE != 6 && TYPE_VALUE != 7) { faling_VALUE("only file streams supported by new in source"); return 0; }
            String eienaar_VALUE = TYPE_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            Opdrag(187, Naslaan(7, Word_konstante(eienaar_VALUE), 0)); 내보내기(89);
            요구('('); verifieer_TYPE(uitdrukking_VALUE(), 3); boolean 이어 = false;
            if (받기(',')) { if (TYPE_VALUE != 7) faling_VALUE("input stream constructor arguments"); verifieer_TYPE(uitdrukking_VALUE(), 2); 이어 = true; }
            요구(')');
            Opdrag(183, 외부참조(10, eienaar_VALUE, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return TYPE_VALUE;
        }
        if (받기('(')) { int TYPE_VALUE = uitdrukking_VALUE(); 요구(')'); return TYPE_VALUE; }
        if (종류() == 257) { 수상수(ontleed_heelgetal(Posisie++, false)); return 1; }
        if (종류() == 258) { 문자읽기(Posisie++); Opdrag(19, Naslaan(8, karakter_konstante(), 0)); return 3; }
        if (종류() == 259) { 문자읽기(Posisie++); if (karakter_lengte != 1) faling_VALUE("character literal length"); 수상수(문자[0]); return 5; }
        if (TAKE_Word("true")) { 내보내기(4); return 2; }
        if (TAKE_Word("false")) { 내보내기(3); return 2; }
        if (TAKE_Word("한국어")) {
            요구('.'); 말요구("자체"); 요구('.');
            String eienaar_VALUE = "", metode_VALUE = "", 서술 = ""; int 가 = 0, 나 = 0, 다 = 0, 라 = 0, 마 = 0, maatreël = 0;
            if (TAKE_Word("Afvoer")) {
                eienaar_VALUE = "한국어/자체/Afvoer"; 요구('.');
                if (TAKE_Word("skryf_lyn")) { metode_VALUE = "skryf_lyn"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("Skryf")) { metode_VALUE = "Skryf"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("수쓰기")) { metode_VALUE = "수쓰기"; 서술 = "(I)V"; 가 = 1; }
                else faling_VALUE("unknown Korean output method");
            } else if (TAKE_Word("문자")) {
                eienaar_VALUE = "한국어/자체/문자"; 요구('.'); 가 = 3;
                if (TAKE_Word("lengte_VALUE")) { metode_VALUE = "lengte_VALUE"; 서술 = "(Ljava/lang/String;)I"; maatreël = 1; }
                else if (TAKE_Word("karakterkode_COUNT")) { metode_VALUE = "karakterkode_COUNT"; 서술 = "(Ljava/lang/String;)I"; maatreël = 1; }
                else if (TAKE_Word("ontleed_heelgetal")) { metode_VALUE = "ontleed_heelgetal"; 서술 = "(Ljava/lang/String;)I"; maatreël = 1; }
                else if (TAKE_Word("skryf_heelgetal_VALUE")) { metode_VALUE = "skryf_heelgetal_VALUE"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; maatreël = 3; }
                else if (TAKE_Word("같음")) { metode_VALUE = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; 나 = 3; maatreël = 2; }
                else if (TAKE_Word("plak_SMS")) { metode_VALUE = "plak_SMS"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; 나 = 3; maatreël = 3; }
                else if (TAKE_Word("sny_VALUE")) { metode_VALUE = "sny_VALUE"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; 나 = 1; 다 = 1; maatreël = 3; }
                else faling_VALUE("unknown Korean text method");
            } else if (TAKE_Word("Lêer")) {
                eienaar_VALUE = "한국어/자체/Lêer"; 요구('.'); 가 = 3;
                if (TAKE_Word("Lees")) { metode_VALUE = "Lees"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; maatreël = 3; }
                else if (TAKE_Word("Skryf")) { metode_VALUE = "Skryf"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; 나 = 3; }
                else faling_VALUE("unknown Korean file method");
            } else if (TAKE_Word("화면")) {
                eienaar_VALUE = "한국어/자체/화면"; 요구('.');
                if (TAKE_Word("너비")) { metode_VALUE = "너비"; 서술 = "()I"; maatreël = 1; }
                else if (TAKE_Word("높이")) { metode_VALUE = "높이"; 서술 = "()I"; maatreël = 1; }
                else if (TAKE_Word("사각형")) { metode_VALUE = "사각형"; 서술 = "(IIIII)V"; 가 = 1; 나 = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (TAKE_Word("vee_uit_inskrywing")) { metode_VALUE = "vee_uit_inskrywing"; 서술 = "(I)V"; 가 = 1; }
                else if (TAKE_Word("기다리기")) { metode_VALUE = "기다리기"; 서술 = "()V"; }
                else faling_VALUE("unknown Korean framebuffer method");
            } else faling_VALUE("unsupported Korean library class");
            요구('('); if (가 != 0) verifieer_TYPE(uitdrukking_VALUE(), 가);
            if (나 != 0) { 요구(','); verifieer_TYPE(uitdrukking_VALUE(), 나); }
            if (다 != 0) { 요구(','); verifieer_TYPE(uitdrukking_VALUE(), 다); }
            if (라 != 0) { 요구(','); verifieer_TYPE(uitdrukking_VALUE(), 라); }
            if (마 != 0) { 요구(','); verifieer_TYPE(uitdrukking_VALUE(), 마); }
            요구(')'); Opdrag(184, 외부참조(10, eienaar_VALUE, metode_VALUE, 서술)); return maatreël;
        }
        if (TAKE_Word("Integer")) {
            요구('.'); 말요구("parseInt"); 요구('('); verifieer_TYPE(uitdrukking_VALUE(), 3); 요구(')');
            Opdrag(184, 외부참조(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Naam = waarde_VALUE();
        if (받기('(')) {
            int funksie_VALUE = -1;
            for (int 수 = 0; 수 < metode_COUNT; 수++) if (이름같음(Naam, metode_inskrywing_naam[수])) funksie_VALUE = 수;
            if (funksie_VALUE < 0) { faling_VALUE("unknown static method"); return 0; }
            int 수 = 0;
            while (!Fout && 종류() != ')') {
                if (수 >= metode_argument_COUNT[funksie_VALUE]) { faling_VALUE("too many arguments"); break; }
                verifieer_TYPE(uitdrukking_VALUE(), metode_argument_TYPE[funksie_VALUE * 16 + 수++]); if (!받기(',')) break;
            }
            요구(')'); if (수 != metode_argument_COUNT[funksie_VALUE]) faling_VALUE("argument count mismatch");
            Opdrag(184, Naslaan(10, Klas_konstante, Naslaan(12, metode_naam_konstante[funksie_VALUE], 함수서술[funksie_VALUE])));
            return metode_teruggee[funksie_VALUE];
        }
        int lokaal_bestek = FIND_lokaal(Naam), TYPE_VALUE = lokaal_TYPE[lokaal_bestek]; 지역읽기(lokaal_bestek);
        while (!Fout) {
            if (받기('[')) { verifieer_TYPE(TYPE_VALUE, 4); verifieer_TYPE(uitdrukking_VALUE(), 1); 요구(']'); 내보내기(50); TYPE_VALUE = 3; }
            else if (받기('.')) {
                if (TYPE_VALUE == 6 || TYPE_VALUE == 7) {
                    String eienaar_VALUE = TYPE_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (TAKE_Word("close")) { 요구('('); 요구(')'); Opdrag(182, 외부참조(10, eienaar_VALUE, "close", "()V")); TYPE_VALUE = 0; }
                    else if (TYPE_VALUE == 6 && TAKE_Word("read")) { 요구('('); 요구(')'); Opdrag(182, 외부참조(10, eienaar_VALUE, "read", "()I")); TYPE_VALUE = 1; }
                    else if (TYPE_VALUE == 7 && TAKE_Word("write")) { 요구('('); verifieer_TYPE(uitdrukking_VALUE(), 1); 요구(')'); Opdrag(182, 외부참조(10, eienaar_VALUE, "write", "(I)V")); TYPE_VALUE = 0; }
                    else { faling_VALUE("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (TYPE_VALUE == 4) { 내보내기(190); TYPE_VALUE = 1; }
                else { verifieer_TYPE(TYPE_VALUE, 3); 요구('('); 요구(')'); Opdrag(182, 외부참조(10, "java/lang/String", "length", "()I")); TYPE_VALUE = 1; }
            } else break;
        }
        return TYPE_VALUE;
    }
    static int 단항() {
        if (++식깊이 > 64) { faling_VALUE("expression nesting too deep"); 식깊이--; return 0; }
        int TYPE_VALUE;
        if (받기('!')) { verifieer_TYPE(단항(), 2); Vergelyking_VALUE(153); TYPE_VALUE = 2; }
        else if (받기('-')) {
            if (종류() == 257) 수상수(ontleed_heelgetal(Posisie++, true));
            else { verifieer_TYPE(단항(), 1); 내보내기(116); }
            TYPE_VALUE = 1;
        } else if (받기('+')) { verifieer_TYPE(단항(), 1); TYPE_VALUE = 1; }
        else TYPE_VALUE = 기본식();
        식깊이--; return TYPE_VALUE;
    }
    static int 곱식() {
        int TYPE_VALUE = 단항();
        while (!Fout && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int enkodering_VALUE = 종류(); Posisie++; verifieer_TYPE(TYPE_VALUE, 1); verifieer_TYPE(단항(), 1);
            내보내기(enkodering_VALUE == '*' ? 104 : enkodering_VALUE == '/' ? 108 : 112); TYPE_VALUE = 1;
        }
        return TYPE_VALUE;
    }
    static int 합식() {
        int TYPE_VALUE = 곱식();
        while (!Fout && (종류() == '+' || 종류() == '-')) {
            int enkodering_VALUE = 종류(); Posisie++; int 경계 = CODE_verstel, TERUG_VALUE_TYPE = 곱식();
            if (enkodering_VALUE == '+' && (TYPE_VALUE == 3 || TERUG_VALUE_TYPE == 3)) { 결합(경계, TYPE_VALUE, TERUG_VALUE_TYPE); TYPE_VALUE = 3; }
            else { verifieer_TYPE(TYPE_VALUE, 1); verifieer_TYPE(TERUG_VALUE_TYPE, 1); 내보내기(enkodering_VALUE == '+' ? 96 : 100); TYPE_VALUE = 1; }
        }
        return TYPE_VALUE;
    }
    static int 붙임참조(int TYPE_VALUE) {
        if (TYPE_VALUE != 1 && TYPE_VALUE != 2 && TYPE_VALUE != 3 && TYPE_VALUE != 5) faling_VALUE("unsupported concatenation type");
        return 외부참조(10, "java/lang/StringBuilder", "append", TYPE_VALUE == 1 ? "(I)Ljava/lang/StringBuilder;"
            : TYPE_VALUE == 2 ? "(Z)Ljava/lang/StringBuilder;" : TYPE_VALUE == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int 경계, int voor_VALUE_TYPE, int TERUG_VALUE_TYPE) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 RIGHT CODE_VALUE 앞에 genereer 코드를 삽입한다.
        // RIGHT uitdrukking_VALUE 내부의 portuur_VALUE tak 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = CODE_verstel;
        Opdrag(187, Naslaan(7, Word_konstante("java/lang/StringBuilder"), 0)); 내보내기(89);
        Opdrag(183, 외부참조(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); Opdrag(182, 붙임참조(voor_VALUE_TYPE));
        if (Fout) return;
        int lengte_VALUE = CODE_verstel - 끝;
        for (int 수 = 0; 수 < lengte_VALUE; 수++) 삽입코드[수] = CODE_VALUE[끝 + 수];
        for (int 수 = 끝 - 1; 수 >= 경계; 수--) CODE_VALUE[수 + lengte_VALUE] = CODE_VALUE[수];
        for (int 수 = 0; 수 < lengte_VALUE; 수++) CODE_VALUE[경계 + 수] = 삽입코드[수];
        Opdrag(182, 붙임참조(TERUG_VALUE_TYPE)); Opdrag(182, 외부참조(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int Vergelyking_uitdrukking() {
        int TYPE_VALUE = 합식();
        while (!Fout && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int enkodering_VALUE = 종류(); Posisie++; verifieer_TYPE(TYPE_VALUE, 1); verifieer_TYPE(합식(), 1);
            Vergelyking_VALUE(enkodering_VALUE == '<' ? 161 : enkodering_VALUE == '>' ? 163 : enkodering_VALUE == 302 ? 164 : 162); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int 동등식() {
        int TYPE_VALUE = Vergelyking_uitdrukking();
        while (!Fout && (종류() == 300 || 종류() == 301)) {
            int enkodering_VALUE = 종류(); Posisie++; int TERUG_VALUE_TYPE = Vergelyking_uitdrukking();
            if (TYPE_VALUE == 0 || TERUG_VALUE_TYPE == 0) faling_VALUE("void expression");
            if (!(heelgetal_TYPE(TYPE_VALUE) && heelgetal_TYPE(TERUG_VALUE_TYPE))) verifieer_TYPE(TERUG_VALUE_TYPE, TYPE_VALUE);
            Vergelyking_VALUE((TYPE_VALUE <= 2 || TYPE_VALUE == 5 ? 159 : 165) + (enkodering_VALUE == 301 ? 1 : 0)); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int 논리곱() {
        int TYPE_VALUE = 동등식();
        while (!Fout && 받기(304)) {
            verifieer_TYPE(TYPE_VALUE, 2); int 가 = tak(153); verifieer_TYPE(동등식(), 2); int 나 = tak(153);
            내보내기(4); int 끝 = tak(167); Skakel_VALUE(가, CODE_verstel); Skakel_VALUE(나, CODE_verstel); 내보내기(3); Skakel_VALUE(끝, CODE_verstel); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int uitdrukking_VALUE() {
        int TYPE_VALUE = 논리곱();
        while (!Fout && 받기(305)) {
            verifieer_TYPE(TYPE_VALUE, 2); int 가 = tak(154); verifieer_TYPE(논리곱(), 2); int 나 = tak(154);
            내보내기(3); int 끝 = tak(167); Skakel_VALUE(가, CODE_verstel); Skakel_VALUE(나, CODE_verstel); 내보내기(4); Skakel_VALUE(끝, CODE_verstel); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static void opdrag_VALUE(boolean toelaat_verklaring) {
        if (Word_VALUE(Posisie, "int") || Word_VALUE(Posisie, "boolean") || Word_VALUE(Posisie, "String") || Word_VALUE(Posisie, "char")
            || Word_VALUE(Posisie, "FileInputStream") || Word_VALUE(Posisie, "FileOutputStream")) {
            if (!toelaat_verklaring) faling_VALUE("declaration not allowed here");
            int TYPE_VALUE = formaat_VALUE(), Naam = waarde_VALUE(); 요구('='); verifieer_TYPE(uitdrukking_VALUE(), TYPE_VALUE);
            skryf_lokaal(byvoeg_lokaal(Naam, TYPE_VALUE)); return;
        }
        int Naam = waarde_VALUE(), lokaal_bestek = FIND_lokaal(Naam);
        if (받기('=')) { verifieer_TYPE(uitdrukking_VALUE(), lokaal_TYPE[lokaal_bestek]); skryf_lokaal(lokaal_bestek); }
        else if (종류() >= 308 && 종류() <= 312) {
            int enkodering_VALUE = 종류(); Posisie++; 지역읽기(lokaal_bestek); int 경계 = CODE_verstel, TERUG_VALUE_TYPE = uitdrukking_VALUE();
            if (enkodering_VALUE == 308 && lokaal_TYPE[lokaal_bestek] == 3) 결합(경계, 3, TERUG_VALUE_TYPE);
            else {
                verifieer_TYPE(lokaal_TYPE[lokaal_bestek], 1); verifieer_TYPE(TERUG_VALUE_TYPE, 1);
                내보내기(enkodering_VALUE == 308 ? 96 : enkodering_VALUE == 309 ? 100 : enkodering_VALUE == 310 ? 104 : enkodering_VALUE == 311 ? 108 : 112);
                if (lokaal_TYPE[lokaal_bestek] == 5) 내보내기(146);
            }
            skryf_lokaal(lokaal_bestek);
        }
        else if (종류() == 306 || 종류() == 307) {
            verifieer_TYPE(lokaal_TYPE[lokaal_bestek], 1); 내보내기(132); 내보내기(lokaal_bestek); 내보내기(종류() == 306 ? 1 : 255); Posisie++;
            if (lokaal_TYPE[lokaal_bestek] == 5) { 지역읽기(lokaal_bestek); 내보내기(146); skryf_lokaal(lokaal_bestek); }
        } else faling_VALUE("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); 요구('.'); 말요구("out"); 요구('.');
        boolean 줄바꿈 = TAKE_Word("println"); if (!줄바꿈) 말요구("print"); 요구('(');
        Opdrag(178, 외부참조(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean leeg_argument = 종류() == ')';
        int TYPE_VALUE = leeg_argument ? 0 : uitdrukking_VALUE(); 요구(')'); 요구(';');
        String 서술 = TYPE_VALUE == 0 ? "()V" : TYPE_VALUE == 1 ? "(I)V" : TYPE_VALUE == 2 ? "(Z)V" : TYPE_VALUE == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (TYPE_VALUE == 4 || TYPE_VALUE >= 6 || TYPE_VALUE == 0 && (!줄바꿈 || !leeg_argument)) faling_VALUE("unsupported print argument");
        Opdrag(182, 외부참조(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean stelling_VALUE() {
        if (Fout) return false;
        if (깊이 > 32) { faling_VALUE("statement nesting too deep"); return false; }
        if (받기('{')) {
            깊이++; boolean teruggee_maatreël = false;
            while (!Fout && 종류() != '}') { if (teruggee_maatreël) faling_VALUE("unreachable statement"); teruggee_maatreël = stelling_VALUE(); }
            요구('}'); for (int 수 = 0; 수 < lokaal_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return teruggee_maatreël;
        }
        if (받기(';')) return false;
        if (TAKE_Word("return")) {
            int TYPE_VALUE = 종류() == ';' ? 0 : uitdrukking_VALUE(); verifieer_TYPE(TYPE_VALUE, metode_teruggee[현재함수]); 요구(';');
            내보내기(TYPE_VALUE == 0 ? 177 : TYPE_VALUE <= 2 || TYPE_VALUE == 5 ? 172 : 176); return true;
        }
        if (TAKE_Word("if")) {
            요구('('); verifieer_TYPE(uitdrukking_VALUE(), 2); 요구(')'); int FALSE_VALUE = tak(153);
            깊이++; boolean 가 = kontrole_stelling(); 깊이--;
            if (TAKE_Word("else")) { int 끝 = tak(167); Skakel_VALUE(FALSE_VALUE, CODE_verstel); 깊이++; boolean 나 = kontrole_stelling(); 깊이--; Skakel_VALUE(끝, CODE_verstel); return 가 && 나; }
            Skakel_VALUE(FALSE_VALUE, CODE_verstel); return false;
        }
        if (TAKE_Word("while")) {
            int Loop = CODE_verstel; 요구('('); verifieer_TYPE(uitdrukking_VALUE(), 2); 요구(')'); int 끝 = tak(153);
            깊이++; kontrole_stelling(); 깊이--; Skakel_VALUE(tak(167), Loop); Skakel_VALUE(끝, CODE_verstel); return false;
        }
        if (TAKE_Word("for")) {
            깊이++; 요구('('); if (종류() != ';') opdrag_VALUE(true); 요구(';');
            int toestand = CODE_verstel; if (종류() == ';') 내보내기(4); else verifieer_TYPE(uitdrukking_VALUE(), 2); 요구(';');
            int 끝 = tak(153), inhoudteks = tak(167), verfris = CODE_verstel;
            if (종류() != ')') opdrag_VALUE(false); 요구(')'); Skakel_VALUE(tak(167), toestand); Skakel_VALUE(inhoudteks, CODE_verstel);
            kontrole_stelling(); Skakel_VALUE(tak(167), verfris); Skakel_VALUE(끝, CODE_verstel);
            for (int 수 = 0; 수 < lokaal_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return false;
        }
        if (Word_VALUE(Posisie, "System")) { 화면출력(); return false; }
        if (종류() == 256 && Posisie + 1 < kenteken_COUNT && (토큰종류[Posisie + 1] == '(' || 토큰종류[Posisie + 1] == '.')) {
            int TYPE_VALUE = uitdrukking_VALUE(); if (TYPE_VALUE != 0) 내보내기(87); 요구(';'); return false;
        }
        opdrag_VALUE(true); 요구(';'); return false;
    }
    static boolean kontrole_stelling() {
        if (Word_VALUE(Posisie, "int") || Word_VALUE(Posisie, "boolean") || Word_VALUE(Posisie, "char") || Word_VALUE(Posisie, "String")
            || Word_VALUE(Posisie, "FileInputStream") || Word_VALUE(Posisie, "FileOutputStream")) faling_VALUE("local declaration requires braces");
        return stelling_VALUE();
    }
    static void 출바(int VALUE) { if (출력크기 == Afvoer.length) faling_VALUE("class file too large"); else Afvoer[출력크기++] = VALUE & 255; }
    static void 출짧(int VALUE) { 출바(VALUE >> 8); 출바(VALUE); }
    static void 출정(int VALUE) { 출짧(VALUE >>> 16); 출짧(VALUE); }
    static void skryf_Klas() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(konstante_COUNT);
        for (int 수 = 0; 수 < konstante_verstel; 수++) 출바(konstante_VALUE[수]);
        출짧(0x21); 출짧(Klas_konstante); 출짧(부모상수); 출짧(0); 출짧(0); 출짧(metode_COUNT);
        for (int 수 = 0; 수 < metode_COUNT; 수++) {
            출짧(metode_toegang[수]); 출짧(metode_naam_konstante[수]); 출짧(함수서술[수]); 출짧(1); 출짧(CODE_konstante);
            출정(12 + metode_lengte[수]); 출짧(128); 출짧(함수지역[수]); 출정(metode_lengte[수]);
            for (int gleuf_inskrywing = 0; gleuf_inskrywing < metode_lengte[수]; gleuf_inskrywing++) 출바(CODE_VALUE[metode_CODE[수] + gleuf_inskrywing]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int Loop() {
        if (gebruiker.인수개수() == 1 && 자바도구.같음(gebruiker.인수(0), "-version")) {
            gebruiker.Skryf("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (gebruiker.인수개수() != 1) { gebruiker.Skryf("Usage: javac FILE.java\n"); return 2; }
        int naam_verstel = 자바도구.Naam(lêer_naam_SMS, gebruiker.인수(0));
        if (naam_verstel < 6 || naam_verstel > 62 || lêer_naam_SMS[naam_verstel - 5] != '.' || lêer_naam_SMS[naam_verstel - 4] != 'j'
            || lêer_naam_SMS[naam_verstel - 3] != 'a' || lêer_naam_SMS[naam_verstel - 2] != 'v' || lêer_naam_SMS[naam_verstel - 1] != 'a') {
            gebruiker.Skryf("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        bron_verstel = gebruiker.파일읽기(lêer_naam_SMS, Bron);
        if (bron_verstel < 0) { gebruiker.Skryf("javac: cannot read source: "); 자바도구.수쓰기(bron_verstel); gebruiker.skryf_karakter_VALUE(10); return 1; }
        bron_verstel = 자바도구.원문해독(Bron, bron_verstel);
        if (bron_verstel < 0) { gebruiker.Skryf("javac error: invalid UTF-8 source\n"); return 1; }
        sny_VALUE(); if (!Fout) 선언읽기();
        if (!Fout) {
            if (kenteken_lengte[Klas_kenteken] != naam_verstel - 5) faling_VALUE("class name must match file name");
            for (int 수 = 0; 수 < naam_verstel - 5; 수++) if (Bron[kenteken_plaas[Klas_kenteken] + 수] != lêer_naam_SMS[수]) faling_VALUE("class name must match file name");
        }
        for (현재함수 = 0; 현재함수 < metode_COUNT && !Fout; 현재함수++) {
            Posisie = 함수본문[현재함수]; metode_CODE[현재함수] = CODE_verstel; lokaal_COUNT = 0; 깊이 = 0;
            for (int 수 = 0; 수 < metode_argument_COUNT[현재함수]; 수++) byvoeg_lokaal(metode_argument_naam[현재함수 * 16 + 수], metode_argument_TYPE[현재함수 * 16 + 수]);
            boolean teruggee_maatreël = stelling_VALUE();
            if (!teruggee_maatreël && metode_teruggee[현재함수] != 0) faling_VALUE("missing return");
            // tak 뒤의 합류 지점은 반드시 werklik_data 명령이어야 한다 (버전 49 검증기).
            if (metode_teruggee[현재함수] == 0) 내보내기(177);
            else { boolean heelgetal = metode_teruggee[현재함수] <= 2 || metode_teruggee[현재함수] == 5; 내보내기(heelgetal ? 3 : 1); 내보내기(heelgetal ? 172 : 176); }
            if (Posisie != metode_beëindig[현재함수]) faling_VALUE("invalid method body");
            함수지역[현재함수] = lokaal_COUNT; metode_lengte[현재함수] = CODE_verstel - metode_CODE[현재함수];
        }
        if (Fout) return 1;
        skryf_Klas(); if (Fout) return 1;
        lêer_naam_SMS[naam_verstel - 4] = 'c'; lêer_naam_SMS[naam_verstel - 3] = 'l'; lêer_naam_SMS[naam_verstel - 2] = 'a';
        lêer_naam_SMS[naam_verstel - 1] = 's'; lêer_naam_SMS[naam_verstel] = 's'; lêer_naam_SMS[naam_verstel + 1] = 0;
        int maatreël = gebruiker.skryf_lêer(lêer_naam_SMS, Afvoer, 출력크기);
        if (maatreël < 0) { gebruiker.Skryf("javac: cannot save class: "); 자바도구.수쓰기(maatreël); gebruiker.skryf_karakter_VALUE(10); return 1; }
        gebruiker.Skryf("Compiled: "); for (int 수 = 0; lêer_naam_SMS[수] != 0; 수++) gebruiker.skryf_karakter_VALUE(lêer_naam_SMS[수]);
        gebruiker.Skryf(" (JVM class version 49)\n"); return 0;
    }
}
