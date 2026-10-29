// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java kilde_træ -> 표준 버전 49 class compiler. */
public final class 자바컴파일러 {
    static int[] KILDE = new int[16384], Udgang = new int[16384], KODE_VÆRDI = new int[4096];
    static int[] 토큰종류 = new int[2048], token_placere = new int[2048], token_varighed = new int[2048];
    static int[] konstant_VÆRDI = new int[4096], konstant_FORSKYDNING = new int[512];
    static int[] 문자 = new int[512], filnavn_sms = new int[64];
    static int[] 삽입코드 = new int[16];
    static int kilde_tilpasse_størrelse, token_TÆL, Placering, KODE_tilpasse_størrelse, konstant_tilpasse_størrelse, konstant_TÆL = 1, produktoutput_tilpasse_størrelse, tegn_varighed;
    static boolean fejl;
    static int Hold_token, Hold_konstant, overordnet_konstant, KODE_konstant;
    static int[] metode_post_navn = new int[32], metode_returnere = new int[32], metode_argument_TÆL = new int[32];
    static int[] metode_argument_navn = new int[512], metode_argument_Type = new int[512];
    static int[] metode_brødtekst = new int[32], metode_afslutte_et_opkald = new int[32], metode_KODE = new int[32];
    static int[] metode_varighed = new int[32], 함수지역 = new int[32], metode_navn_konstant = new int[32], 함수서술 = new int[32];
    static int[] metode_åbne = new int[32];
    static int metode_TÆL, aktuel_metode, lokal_TÆL, 깊이, 식깊이;
    static int[] lokal_navn = new int[128], lokal_Type = new int[128], 지역깊이 = new int[128];

    static void fejl_VÆRDI(String 이유) {
        if (!fejl) {
            bruger.Skrive("javac error: "); bruger.Skrive(이유);
            bruger.Skrive(" at line ");
            int Linje = 1, 끝 = Placering < token_TÆL ? token_placere[Placering] : kilde_tilpasse_størrelse;
            for (int tal = 0; tal < 끝; tal++) if (KILDE[tal] == 10) Linje++;
            자바도구.skrive_tal(Linje); bruger.skrive_tegn_VÆRDI(10);
        }
        fejl = true;
    }
    static boolean tegn_VÆRDI(int VÆRDI) { return 문자이름규칙.첫글자(VÆRDI); }
    static boolean ciffer_VÆRDI(int VÆRDI) { return VÆRDI >= '0' && VÆRDI <= '9'; }
    static boolean 이름같음(int 가, int SEKUND_operand) {
        if (가 < 0 || SEKUND_operand < 0 || 가 >= token_TÆL || SEKUND_operand >= token_TÆL || token_varighed[가] != token_varighed[SEKUND_operand]) return false;
        for (int tal = 0; tal < token_varighed[가]; tal++) if (KILDE[token_placere[가] + tal] != KILDE[token_placere[SEKUND_operand] + tal]) return false;
        return true;
    }
    static boolean Ord_VÆRDI(int token_VÆRDI, String Ord_sms) {
        if (token_VÆRDI < 0 || token_VÆRDI >= token_TÆL || token_varighed[token_VÆRDI] != Ord_sms.length()) return false;
        for (int tal = 0; tal < Ord_sms.length(); tal++) if (KILDE[token_placere[token_VÆRDI] + tal] != Ord_sms.charAt(tal)) return false;
        return true;
    }
    static int 종류() { return Placering < token_TÆL ? 토큰종류[Placering] : 0; }
    static boolean modtage(int VÆRDI) { if (종류() != VÆRDI) return false; Placering++; return true; }
    static void krav_VÆRDI(int VÆRDI) { if (!modtage(VÆRDI)) fejl_VÆRDI("unexpected token"); }
    static boolean TAG_Ord(String Ord_sms) { if (!Ord_VÆRDI(Placering, Ord_sms)) return false; Placering++; return true; }
    static void 말요구(String Ord_sms) { if (!TAG_Ord(Ord_sms)) fejl_VÆRDI(Ord_sms); }
    static int identifikator_VÆRDI() {
        int KR = Placering;
        if (종류() != 256) fejl_VÆRDI("identifier required"); else Placering++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int Kør_2 = 0;
        for (int tal = 0; tal <= 예약어.length(); tal++) {
            if (tal == 예약어.length() || 예약어.charAt(tal) == ' ') {
                boolean 같음 = tal - Kør_2 == token_varighed[KR];
                for (int udvidelsesstik_post = Kør_2; 같음 && udvidelsesstik_post < tal; udvidelsesstik_post++) if (예약어.charAt(udvidelsesstik_post) != KILDE[token_placere[KR] + udvidelsesstik_post - Kør_2]) 같음 = false;
                if (같음) fejl_VÆRDI("reserved word cannot be an identifier");
                Kør_2 = tal + 1;
            }
        }
        return KR;
    }
    static void klip_VÆRDI() {
        int tal = 0;
        while (tal < kilde_tilpasse_størrelse && !fejl) {
            int VÆRDI = KILDE[tal], Kør_2 = tal, 종류 = VÆRDI;
            if (VÆRDI == 32 || VÆRDI == 9 || VÆRDI == 10 || VÆRDI == 13) { tal++; continue; }
            if (VÆRDI == '/' && tal + 1 < kilde_tilpasse_størrelse && KILDE[tal + 1] == '/') {
                while (tal < kilde_tilpasse_størrelse && KILDE[tal] != 10) tal++;
                continue;
            }
            if (VÆRDI == '/' && tal + 1 < kilde_tilpasse_størrelse && KILDE[tal + 1] == '*') {
                tal += 2;
                while (tal + 1 < kilde_tilpasse_størrelse && !(KILDE[tal] == '*' && KILDE[tal + 1] == '/')) tal++;
                if (tal + 1 >= kilde_tilpasse_størrelse) { fejl_VÆRDI("unterminated comment"); break; }
                tal += 2; continue;
            }
            if (tegn_VÆRDI(VÆRDI)) { 종류 = 256; while (tal < kilde_tilpasse_størrelse && 문자이름규칙.이어진글자(KILDE[tal])) tal++; }
            else if (ciffer_VÆRDI(VÆRDI)) { 종류 = 257; while (tal < kilde_tilpasse_størrelse && ciffer_VÆRDI(KILDE[tal])) tal++; }
            else if (VÆRDI == '"' || VÆRDI == '\'') {
                종류 = VÆRDI == '"' ? 258 : 259; tal++;
                while (tal < kilde_tilpasse_størrelse && KILDE[tal] != VÆRDI && KILDE[tal] != 10 && KILDE[tal] != 13) {
                    if (KILDE[tal] == '\\') tal++;
                    tal++;
                }
                if (tal >= kilde_tilpasse_størrelse || KILDE[tal] != VÆRDI) { fejl_VÆRDI("unterminated literal"); break; }
                tal++;
            } else {
                tal++;
                if (tal < kilde_tilpasse_størrelse) {
                    int Næste_vare = KILDE[tal];
                    if (VÆRDI == '=' && Næste_vare == '=') 종류 = 300;
                    if (VÆRDI == '!' && Næste_vare == '=') 종류 = 301;
                    if (VÆRDI == '<' && Næste_vare == '=') 종류 = 302;
                    if (VÆRDI == '>' && Næste_vare == '=') 종류 = 303;
                    if (VÆRDI == '&' && Næste_vare == '&') 종류 = 304;
                    if (VÆRDI == '|' && Næste_vare == '|') 종류 = 305;
                    if (VÆRDI == '+' && Næste_vare == '+') 종류 = 306;
                    if (VÆRDI == '-' && Næste_vare == '-') 종류 = 307;
                    if (VÆRDI == '+' && Næste_vare == '=') 종류 = 308;
                    if (VÆRDI == '-' && Næste_vare == '=') 종류 = 309;
                    if (VÆRDI == '*' && Næste_vare == '=') 종류 = 310;
                    if (VÆRDI == '/' && Næste_vare == '=') 종류 = 311;
                    if (VÆRDI == '%' && Næste_vare == '=') 종류 = 312;
                    if (종류 >= 300) tal++;
                }
            }
            if (token_TÆL == 토큰종류.length - 1) { fejl_VÆRDI("too many tokens (2047 maximum)"); break; }
            토큰종류[token_TÆL] = 종류; token_placere[token_TÆL] = Kør_2; token_varighed[token_TÆL++] = tal - Kør_2;
        }
    }
    static void skrive_konstant_byte(int VÆRDI) {
        if (konstant_tilpasse_størrelse == konstant_VÆRDI.length) { fejl_VÆRDI("constant pool too large"); return; }
        konstant_VÆRDI[konstant_tilpasse_størrelse++] = VÆRDI & 255;
    }
    static void 상짧(int VÆRDI) { skrive_konstant_byte(VÆRDI >> 8); skrive_konstant_byte(VÆRDI); }
    static int register_konstant(int Kør_2) {
        for (int tal = 1; tal < konstant_TÆL; tal++) {
            int frontvendt_VÆRDI = konstant_FORSKYDNING[tal], varighed_VÆRDI = (tal + 1 < konstant_TÆL ? konstant_FORSKYDNING[tal + 1] : Kør_2) - frontvendt_VÆRDI;
            if (varighed_VÆRDI != konstant_tilpasse_størrelse - Kør_2) continue;
            boolean 같음 = true;
            for (int udvidelsesstik_post = 0; udvidelsesstik_post < varighed_VÆRDI; udvidelsesstik_post++) if (konstant_VÆRDI[frontvendt_VÆRDI + udvidelsesstik_post] != konstant_VÆRDI[Kør_2 + udvidelsesstik_post]) 같음 = false;
            if (같음) { konstant_tilpasse_størrelse = Kør_2; return tal; }
        }
        if (konstant_TÆL == konstant_FORSKYDNING.length) { fejl_VÆRDI("too many constants"); return 0; }
        konstant_FORSKYDNING[konstant_TÆL] = Kør_2;
        return konstant_TÆL++;
    }
    static void tilføj_sms(int VÆRDI) {
        if (tegn_varighed == 문자.length) { fejl_VÆRDI("text too long"); return; }
        문자[tegn_varighed++] = VÆRDI;
    }
    static void tilføj_Ord(String Ord_sms) { for (int tal = 0; tal < Ord_sms.length(); tal++) tilføj_sms(Ord_sms.charAt(tal)); }
    static int tegn_konstant() {
        int Kør_2 = konstant_tilpasse_størrelse; skrive_konstant_byte(1); 상짧(0);
        for (int tal = 0; tal < tegn_varighed; tal++) {
            int VÆRDI = 문자[tal];
            if (VÆRDI > 0 && VÆRDI < 128) skrive_konstant_byte(VÆRDI);
            else if (VÆRDI < 2048) { skrive_konstant_byte(192 | VÆRDI >> 6); skrive_konstant_byte(128 | VÆRDI & 63); }
            else { skrive_konstant_byte(224 | VÆRDI >> 12); skrive_konstant_byte(128 | VÆRDI >> 6 & 63); skrive_konstant_byte(128 | VÆRDI & 63); }
        }
        if (fejl) return 0;
        int varighed_VÆRDI = konstant_tilpasse_størrelse - Kør_2 - 3;
        konstant_VÆRDI[Kør_2 + 1] = varighed_VÆRDI >> 8; konstant_VÆRDI[Kør_2 + 2] = varighed_VÆRDI & 255;
        return register_konstant(Kør_2);
    }
    static int Ord_konstant(String Ord_sms) { tegn_varighed = 0; tilføj_Ord(Ord_sms); return tegn_konstant(); }
    static int token_konstant(int token_VÆRDI) {
        tegn_varighed = 0;
        for (int tal = 0; tal < token_varighed[token_VÆRDI]; tal++) tilføj_sms(KILDE[token_placere[token_VÆRDI] + tal]);
        return tegn_konstant();
    }
    static int referere(int 종류, int 가, int SEKUND_operand) {
        int Kør_2 = konstant_tilpasse_størrelse; skrive_konstant_byte(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(SEKUND_operand);
        return register_konstant(Kør_2);
    }
    static int ekstern_referere(int 종류, String ejer_VÆRDI, String Navn, String 서술) {
        int ejer_identifikator = referere(7, Ord_konstant(ejer_VÆRDI), 0);
        int navn_TÆL = Ord_konstant(Navn), format_TÆL = Ord_konstant(서술);
        return referere(종류, ejer_identifikator, referere(12, navn_TÆL, format_TÆL));
    }
    static void 내보내기(int VÆRDI) {
        if (KODE_tilpasse_størrelse == KODE_VÆRDI.length) { fejl_VÆRDI("bytecode too large"); return; }
        KODE_VÆRDI[KODE_tilpasse_størrelse++] = VÆRDI & 255;
    }
    static void Kommando(int VÆRDI, int Argumenter) { 내보내기(VÆRDI); 내보내기(Argumenter >> 8); 내보내기(Argumenter); }
    static void 수상수(int VÆRDI) {
        if (VÆRDI >= -1 && VÆRDI <= 5) { 내보내기(VÆRDI + 3); return; }
        int Kør_2 = konstant_tilpasse_størrelse; skrive_konstant_byte(3); 상짧(VÆRDI >>> 16); 상짧(VÆRDI);
        Kommando(19, register_konstant(Kør_2));
    }
    static int gren(int Kommando) { int KR = KODE_tilpasse_størrelse; Kommando(Kommando, 0); return KR; }
    static void Link_VÆRDI(int gren, int mål_objekt) {
        if (fejl) return;
        int 거리 = mål_objekt - gren;
        if (거리 < -32768 || 거리 > 32767 || gren < 0 || gren + 2 >= KODE_tilpasse_størrelse) { fejl_VÆRDI("invalid branch"); return; }
        KODE_VÆRDI[gren + 1] = 거리 >> 8 & 255; KODE_VÆRDI[gren + 2] = 거리 & 255;
    }
    static void Sammenligning_VÆRDI(int Kommando) {
        int SAND_VÆRDI = gren(Kommando); 내보내기(3); int 끝 = gren(167);
        Link_VÆRDI(SAND_VÆRDI, KODE_tilpasse_størrelse); 내보내기(4); Link_VÆRDI(끝, KODE_tilpasse_størrelse);
    }
    static int format_VÆRDI() {
        if (TAG_Ord("void")) return 0;
        if (TAG_Ord("int")) return 1;
        if (TAG_Ord("boolean")) return 2;
        if (TAG_Ord("char")) return 5;
        if (TAG_Ord("FileInputStream")) return 6;
        if (TAG_Ord("FileOutputStream")) return 7;
        if (TAG_Ord("String")) { if (modtage('[')) { krav_VÆRDI(']'); return 4; } return 3; }
        fejl_VÆRDI("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void Tilføj_format(int Type_VÆRDI) {
        if (Type_VÆRDI == 0) tilføj_sms('V');
        if (Type_VÆRDI == 1) tilføj_sms('I');
        if (Type_VÆRDI == 2) tilføj_sms('Z');
        if (Type_VÆRDI == 3) tilføj_Ord("Ljava/lang/String;");
        if (Type_VÆRDI == 4) tilføj_Ord("[Ljava/lang/String;");
        if (Type_VÆRDI == 5) tilføj_sms('C');
        if (Type_VÆRDI == 6) tilføj_Ord("Ljava/io/FileInputStream;");
        if (Type_VÆRDI == 7) tilføj_Ord("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws erklæring. undtagelse Proces_VÆRDI_post 본문은 vært javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = TAG_Ord("Dansk");
        if (한국어묶음) { krav_VÆRDI('.'); 말요구("eget"); krav_VÆRDI('.'); }
        if (!한국어묶음 && (TAG_Ord("Exception") || TAG_Ord("IOException"))) return;
        if (TAG_Ord("undtagelse") || TAG_Ord("udførelse_undtagelse") || TAG_Ord("I_O_undtagelse") || TAG_Ord("vent_TIMEOUT_undtagelse") || TAG_Ord("mail_Opslag_undtagelse") || TAG_Ord("파일없음예외") || TAG_Ord("통신예외") || TAG_Ord("ugyldig_argument_undtagelse") || TAG_Ord("tal_format_fejl") || TAG_Ord("범위예외") || TAG_Ord("배열범위예외") || TAG_Ord("문자열범위예외") || TAG_Ord("NULL_referere_undtagelse") || TAG_Ord("산술예외") || TAG_Ord("status_undtagelse") || TAG_Ord("Type_Cast_undtagelse") || TAG_Ord("음수배열크기예외") || TAG_Ord("MATRIX_Store_fejl") || TAG_Ord("tråd_status_undtagelse") || TAG_Ord("대기중단예외")) return;
        fejl_VÆRDI("unsupported throws type");
    }
    static void 선언읽기() {
        while (TAG_Ord("import")) {
            if (Ord_VÆRDI(Placering, "Dansk")) 예외이름읽기();
            else {
                말요구("java"); krav_VÆRDI('.'); 말요구("io"); krav_VÆRDI('.');
                if (!(TAG_Ord("FileInputStream") || TAG_Ord("FileOutputStream") || TAG_Ord("IOException"))) fejl_VÆRDI("unsupported import");
            }
            krav_VÆRDI(';');
        }
        TAG_Ord("public"); TAG_Ord("final"); 말요구("class"); Hold_token = identifikator_VÆRDI();
        Hold_konstant = referere(7, token_konstant(Hold_token), 0);
        overordnet_konstant = referere(7, Ord_konstant("java/lang/Object"), 0); KODE_konstant = Ord_konstant("Code"); krav_VÆRDI('{');
        while (!fejl && 종류() != '}') {
            if (metode_TÆL == 32) { fejl_VÆRDI("too many methods"); break; }
            int åbne_post = TAG_Ord("public") ? 1 : TAG_Ord("private") ? 2 : 0; 말요구("static");
            int FUNKTION_VÆRDI = metode_TÆL++;
            metode_åbne[FUNKTION_VÆRDI] = åbne_post | 8;
            metode_returnere[FUNKTION_VÆRDI] = format_VÆRDI(); metode_post_navn[FUNKTION_VÆRDI] = identifikator_VÆRDI(); krav_VÆRDI('(');
            for (int frontvendt_VÆRDI = 0; frontvendt_VÆRDI < FUNKTION_VÆRDI; frontvendt_VÆRDI++) if (이름같음(metode_post_navn[frontvendt_VÆRDI], metode_post_navn[FUNKTION_VÆRDI])) fejl_VÆRDI("duplicate method (overloading unsupported)");
            while (!fejl && 종류() != ')') {
                int tal = metode_argument_TÆL[FUNKTION_VÆRDI];
                if (tal == 16) { fejl_VÆRDI("too many parameters"); break; }
                int Type_VÆRDI = format_VÆRDI(); if (Type_VÆRDI == 0) fejl_VÆRDI("void parameter");
                metode_argument_Type[FUNKTION_VÆRDI * 16 + tal] = Type_VÆRDI; metode_argument_navn[FUNKTION_VÆRDI * 16 + tal] = identifikator_VÆRDI();
                metode_argument_TÆL[FUNKTION_VÆRDI]++;
                if (!modtage(',')) break;
            }
            krav_VÆRDI(')');
            if (TAG_Ord("throws")) {
                do { 예외이름읽기(); } while (!fejl && modtage(','));
            }
            metode_brødtekst[FUNKTION_VÆRDI] = Placering; krav_VÆRDI('{');
            int indlejring_VÆRDI = 1;
            while (Placering < token_TÆL && indlejring_VÆRDI > 0) {
                if (종류() == '{') indlejring_VÆRDI++;
                if (종류() == '}') indlejring_VÆRDI--;
                Placering++;
            }
            if (indlejring_VÆRDI != 0) fejl_VÆRDI("unclosed method body");
            metode_afslutte_et_opkald[FUNKTION_VÆRDI] = Placering;
            metode_navn_konstant[FUNKTION_VÆRDI] = token_konstant(metode_post_navn[FUNKTION_VÆRDI]);
            tegn_varighed = 0; tilføj_sms('(');
            for (int tal = 0; tal < metode_argument_TÆL[FUNKTION_VÆRDI]; tal++) Tilføj_format(metode_argument_Type[FUNKTION_VÆRDI * 16 + tal]);
            tilføj_sms(')'); Tilføj_format(metode_returnere[FUNKTION_VÆRDI]); 함수서술[FUNKTION_VÆRDI] = tegn_konstant();
        }
        krav_VÆRDI('}'); if (Placering != token_TÆL) fejl_VÆRDI("extra input after class");
    }
    static int Søg_lokal(int Navn) {
        for (int tal = lokal_TÆL - 1; tal >= 0; tal--) if (지역깊이[tal] >= 0 && 이름같음(lokal_navn[tal], Navn)) return tal;
        fejl_VÆRDI("unknown variable"); return 0;
    }
    static int Tilføj_lokal(int Navn, int Type_VÆRDI) {
        for (int tal = 0; tal < lokal_TÆL; tal++) if (지역깊이[tal] >= 0 && 이름같음(lokal_navn[tal], Navn)) fejl_VÆRDI("duplicate local variable");
        if (lokal_TÆL == 128) { fejl_VÆRDI("too many locals"); return 0; }
        lokal_navn[lokal_TÆL] = Navn; lokal_Type[lokal_TÆL] = Type_VÆRDI; 지역깊이[lokal_TÆL] = 깊이;
        return lokal_TÆL++;
    }
    static boolean heltal_Type(int Type_VÆRDI) { return Type_VÆRDI == 1 || Type_VÆRDI == 5; }
    static void 지역읽기(int tal) { 내보내기(lokal_Type[tal] <= 2 || lokal_Type[tal] == 5 ? 21 : 25); 내보내기(tal); }
    static void skrive_lokal(int tal) { 내보내기(lokal_Type[tal] <= 2 || lokal_Type[tal] == 5 ? 54 : 58); 내보내기(tal); }
    static void bekræfte_Type(int faktisk_data, int 기대) { if (faktisk_data != 기대 && !(faktisk_data == 5 && 기대 == 1)) fejl_VÆRDI("type mismatch"); }
    static void 문자읽기(int token_VÆRDI) {
        tegn_varighed = 0; int Kør_2 = token_placere[token_VÆRDI] + 1, 끝 = token_placere[token_VÆRDI] + token_varighed[token_VÆRDI] - 1;
        while (Kør_2 < 끝 && !fejl) {
            int VÆRDI = KILDE[Kør_2++];
            if (VÆRDI == '\\') {
                if (Kør_2 == 끝) { fejl_VÆRDI("invalid escape"); break; }
                VÆRDI = KILDE[Kør_2++];
                if (VÆRDI == 'n') VÆRDI = 10;
                else if (VÆRDI == 'r') VÆRDI = 13;
                else if (VÆRDI == 't') VÆRDI = 9;
                else if (VÆRDI == 'b') VÆRDI = 8;
                else if (VÆRDI == 'f') VÆRDI = 12;
                else if (VÆRDI != '\\' && VÆRDI != '"' && VÆRDI != '\'') fejl_VÆRDI("unsupported escape");
            }
            tilføj_sms(VÆRDI);
        }
    }
    static int opdele_tekst_heltal(int token_VÆRDI, boolean 음수) {
        if (token_varighed[token_VÆRDI] > 1 && KILDE[token_placere[token_VÆRDI]] == '0') fejl_VÆRDI("octal literals unsupported");
        int VÆRDI = 0;
        for (int tal = 0; tal < token_varighed[token_VÆRDI]; tal++) {
            int ciffer_vare = KILDE[token_placere[token_VÆRDI] + tal] - '0';
            if (VÆRDI < -214748364 || VÆRDI == -214748364 && ciffer_vare > (음수 ? 8 : 7)) fejl_VÆRDI("integer literal out of range");
            VÆRDI = VÆRDI * 10 - ciffer_vare;
        }
        return 음수 ? VÆRDI : -VÆRDI;
    }
    static int 기본식() {
        if (TAG_Ord("new")) {
            int Type_VÆRDI = format_VÆRDI();
            if (Type_VÆRDI != 6 && Type_VÆRDI != 7) { fejl_VÆRDI("only file streams supported by new in source"); return 0; }
            String ejer_VÆRDI = Type_VÆRDI == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            Kommando(187, referere(7, Ord_konstant(ejer_VÆRDI), 0)); 내보내기(89);
            krav_VÆRDI('('); bekræfte_Type(udtryk_VÆRDI(), 3); boolean 이어 = false;
            if (modtage(',')) { if (Type_VÆRDI != 7) fejl_VÆRDI("input stream constructor arguments"); bekræfte_Type(udtryk_VÆRDI(), 2); 이어 = true; }
            krav_VÆRDI(')');
            Kommando(183, ekstern_referere(10, ejer_VÆRDI, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return Type_VÆRDI;
        }
        if (modtage('(')) { int Type_VÆRDI = udtryk_VÆRDI(); krav_VÆRDI(')'); return Type_VÆRDI; }
        if (종류() == 257) { 수상수(opdele_tekst_heltal(Placering++, false)); return 1; }
        if (종류() == 258) { 문자읽기(Placering++); Kommando(19, referere(8, tegn_konstant(), 0)); return 3; }
        if (종류() == 259) { 문자읽기(Placering++); if (tegn_varighed != 1) fejl_VÆRDI("character literal length"); 수상수(문자[0]); return 5; }
        if (TAG_Ord("true")) { 내보내기(4); return 2; }
        if (TAG_Ord("false")) { 내보내기(3); return 2; }
        if (TAG_Ord("Dansk")) {
            krav_VÆRDI('.'); 말요구("eget"); krav_VÆRDI('.');
            String ejer_VÆRDI = "", metode_VÆRDI = "", 서술 = ""; int 가 = 0, SEKUND_operand = 0, 다 = 0, 라 = 0, 마 = 0, KR = 0;
            if (TAG_Ord("Udgang")) {
                ejer_VÆRDI = "Dansk/eget/Udgang"; krav_VÆRDI('.');
                if (TAG_Ord("skrive_linje")) { metode_VÆRDI = "skrive_linje"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAG_Ord("Skrive")) { metode_VÆRDI = "Skrive"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAG_Ord("skrive_tal")) { metode_VÆRDI = "skrive_tal"; 서술 = "(I)V"; 가 = 1; }
                else fejl_VÆRDI("unknown Korean output method");
            } else if (TAG_Ord("문자")) {
                ejer_VÆRDI = "Dansk/eget/문자"; krav_VÆRDI('.'); 가 = 3;
                if (TAG_Ord("varighed_VÆRDI")) { metode_VÆRDI = "varighed_VÆRDI"; 서술 = "(Ljava/lang/String;)I"; KR = 1; }
                else if (TAG_Ord("tegnkode_TÆL")) { metode_VÆRDI = "tegnkode_TÆL"; 서술 = "(Ljava/lang/String;)I"; KR = 1; }
                else if (TAG_Ord("opdele_tekst_heltal")) { metode_VÆRDI = "opdele_tekst_heltal"; 서술 = "(Ljava/lang/String;)I"; KR = 1; }
                else if (TAG_Ord("skrive_heltal_VÆRDI")) { metode_VÆRDI = "skrive_heltal_VÆRDI"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; KR = 3; }
                else if (TAG_Ord("같음")) { metode_VÆRDI = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; SEKUND_operand = 3; KR = 2; }
                else if (TAG_Ord("sætte_ind_sms")) { metode_VÆRDI = "sætte_ind_sms"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; SEKUND_operand = 3; KR = 3; }
                else if (TAG_Ord("klip_VÆRDI")) { metode_VÆRDI = "klip_VÆRDI"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; SEKUND_operand = 1; 다 = 1; KR = 3; }
                else fejl_VÆRDI("unknown Korean text method");
            } else if (TAG_Ord("Fil")) {
                ejer_VÆRDI = "Dansk/eget/Fil"; krav_VÆRDI('.'); 가 = 3;
                if (TAG_Ord("Læse")) { metode_VÆRDI = "Læse"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; KR = 3; }
                else if (TAG_Ord("Skrive")) { metode_VÆRDI = "Skrive"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; SEKUND_operand = 3; }
                else fejl_VÆRDI("unknown Korean file method");
            } else if (TAG_Ord("skærmbillede")) {
                ejer_VÆRDI = "Dansk/eget/skærmbillede"; krav_VÆRDI('.');
                if (TAG_Ord("너비")) { metode_VÆRDI = "너비"; 서술 = "()I"; KR = 1; }
                else if (TAG_Ord("높이")) { metode_VÆRDI = "높이"; 서술 = "()I"; KR = 1; }
                else if (TAG_Ord("rektangel")) { metode_VÆRDI = "rektangel"; 서술 = "(IIIII)V"; 가 = 1; SEKUND_operand = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (TAG_Ord("slette_post")) { metode_VÆRDI = "slette_post"; 서술 = "(I)V"; 가 = 1; }
                else if (TAG_Ord("기다리기")) { metode_VÆRDI = "기다리기"; 서술 = "()V"; }
                else fejl_VÆRDI("unknown Korean framebuffer method");
            } else fejl_VÆRDI("unsupported Korean library class");
            krav_VÆRDI('('); if (가 != 0) bekræfte_Type(udtryk_VÆRDI(), 가);
            if (SEKUND_operand != 0) { krav_VÆRDI(','); bekræfte_Type(udtryk_VÆRDI(), SEKUND_operand); }
            if (다 != 0) { krav_VÆRDI(','); bekræfte_Type(udtryk_VÆRDI(), 다); }
            if (라 != 0) { krav_VÆRDI(','); bekræfte_Type(udtryk_VÆRDI(), 라); }
            if (마 != 0) { krav_VÆRDI(','); bekræfte_Type(udtryk_VÆRDI(), 마); }
            krav_VÆRDI(')'); Kommando(184, ekstern_referere(10, ejer_VÆRDI, metode_VÆRDI, 서술)); return KR;
        }
        if (TAG_Ord("Integer")) {
            krav_VÆRDI('.'); 말요구("parseInt"); krav_VÆRDI('('); bekræfte_Type(udtryk_VÆRDI(), 3); krav_VÆRDI(')');
            Kommando(184, ekstern_referere(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Navn = identifikator_VÆRDI();
        if (modtage('(')) {
            int FUNKTION_VÆRDI = -1;
            for (int tal = 0; tal < metode_TÆL; tal++) if (이름같음(Navn, metode_post_navn[tal])) FUNKTION_VÆRDI = tal;
            if (FUNKTION_VÆRDI < 0) { fejl_VÆRDI("unknown static method"); return 0; }
            int tal = 0;
            while (!fejl && 종류() != ')') {
                if (tal >= metode_argument_TÆL[FUNKTION_VÆRDI]) { fejl_VÆRDI("too many arguments"); break; }
                bekræfte_Type(udtryk_VÆRDI(), metode_argument_Type[FUNKTION_VÆRDI * 16 + tal++]); if (!modtage(',')) break;
            }
            krav_VÆRDI(')'); if (tal != metode_argument_TÆL[FUNKTION_VÆRDI]) fejl_VÆRDI("argument count mismatch");
            Kommando(184, referere(10, Hold_konstant, referere(12, metode_navn_konstant[FUNKTION_VÆRDI], 함수서술[FUNKTION_VÆRDI])));
            return metode_returnere[FUNKTION_VÆRDI];
        }
        int lokal_Omfang = Søg_lokal(Navn), Type_VÆRDI = lokal_Type[lokal_Omfang]; 지역읽기(lokal_Omfang);
        while (!fejl) {
            if (modtage('[')) { bekræfte_Type(Type_VÆRDI, 4); bekræfte_Type(udtryk_VÆRDI(), 1); krav_VÆRDI(']'); 내보내기(50); Type_VÆRDI = 3; }
            else if (modtage('.')) {
                if (Type_VÆRDI == 6 || Type_VÆRDI == 7) {
                    String ejer_VÆRDI = Type_VÆRDI == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (TAG_Ord("close")) { krav_VÆRDI('('); krav_VÆRDI(')'); Kommando(182, ekstern_referere(10, ejer_VÆRDI, "close", "()V")); Type_VÆRDI = 0; }
                    else if (Type_VÆRDI == 6 && TAG_Ord("read")) { krav_VÆRDI('('); krav_VÆRDI(')'); Kommando(182, ekstern_referere(10, ejer_VÆRDI, "read", "()I")); Type_VÆRDI = 1; }
                    else if (Type_VÆRDI == 7 && TAG_Ord("write")) { krav_VÆRDI('('); bekræfte_Type(udtryk_VÆRDI(), 1); krav_VÆRDI(')'); Kommando(182, ekstern_referere(10, ejer_VÆRDI, "write", "(I)V")); Type_VÆRDI = 0; }
                    else { fejl_VÆRDI("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (Type_VÆRDI == 4) { 내보내기(190); Type_VÆRDI = 1; }
                else { bekræfte_Type(Type_VÆRDI, 3); krav_VÆRDI('('); krav_VÆRDI(')'); Kommando(182, ekstern_referere(10, "java/lang/String", "length", "()I")); Type_VÆRDI = 1; }
            } else break;
        }
        return Type_VÆRDI;
    }
    static int 단항() {
        if (++식깊이 > 64) { fejl_VÆRDI("expression nesting too deep"); 식깊이--; return 0; }
        int Type_VÆRDI;
        if (modtage('!')) { bekræfte_Type(단항(), 2); Sammenligning_VÆRDI(153); Type_VÆRDI = 2; }
        else if (modtage('-')) {
            if (종류() == 257) 수상수(opdele_tekst_heltal(Placering++, true));
            else { bekræfte_Type(단항(), 1); 내보내기(116); }
            Type_VÆRDI = 1;
        } else if (modtage('+')) { bekræfte_Type(단항(), 1); Type_VÆRDI = 1; }
        else Type_VÆRDI = 기본식();
        식깊이--; return Type_VÆRDI;
    }
    static int 곱식() {
        int Type_VÆRDI = 단항();
        while (!fejl && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int kodning_VÆRDI = 종류(); Placering++; bekræfte_Type(Type_VÆRDI, 1); bekræfte_Type(단항(), 1);
            내보내기(kodning_VÆRDI == '*' ? 104 : kodning_VÆRDI == '/' ? 108 : 112); Type_VÆRDI = 1;
        }
        return Type_VÆRDI;
    }
    static int 합식() {
        int Type_VÆRDI = 곱식();
        while (!fejl && (종류() == '+' || 종류() == '-')) {
            int kodning_VÆRDI = 종류(); Placering++; int grænse_VÆRDI = KODE_tilpasse_størrelse, BACK_værditype = 곱식();
            if (kodning_VÆRDI == '+' && (Type_VÆRDI == 3 || BACK_værditype == 3)) { 결합(grænse_VÆRDI, Type_VÆRDI, BACK_værditype); Type_VÆRDI = 3; }
            else { bekræfte_Type(Type_VÆRDI, 1); bekræfte_Type(BACK_værditype, 1); 내보내기(kodning_VÆRDI == '+' ? 96 : 100); Type_VÆRDI = 1; }
        }
        return Type_VÆRDI;
    }
    static int tilsluttet_referere(int Type_VÆRDI) {
        if (Type_VÆRDI != 1 && Type_VÆRDI != 2 && Type_VÆRDI != 3 && Type_VÆRDI != 5) fejl_VÆRDI("unsupported concatenation type");
        return ekstern_referere(10, "java/lang/StringBuilder", "append", Type_VÆRDI == 1 ? "(I)Ljava/lang/StringBuilder;"
            : Type_VÆRDI == 2 ? "(Z)Ljava/lang/StringBuilder;" : Type_VÆRDI == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int grænse_VÆRDI, int frontvendt_værditype, int BACK_værditype) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 HØJRE KODE_VÆRDI 앞에 generere 코드를 삽입한다.
        // HØJRE udtryk_VÆRDI 내부의 peer_VÆRDI gren 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = KODE_tilpasse_størrelse;
        Kommando(187, referere(7, Ord_konstant("java/lang/StringBuilder"), 0)); 내보내기(89);
        Kommando(183, ekstern_referere(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); Kommando(182, tilsluttet_referere(frontvendt_værditype));
        if (fejl) return;
        int varighed_VÆRDI = KODE_tilpasse_størrelse - 끝;
        for (int tal = 0; tal < varighed_VÆRDI; tal++) 삽입코드[tal] = KODE_VÆRDI[끝 + tal];
        for (int tal = 끝 - 1; tal >= grænse_VÆRDI; tal--) KODE_VÆRDI[tal + varighed_VÆRDI] = KODE_VÆRDI[tal];
        for (int tal = 0; tal < varighed_VÆRDI; tal++) KODE_VÆRDI[grænse_VÆRDI + tal] = 삽입코드[tal];
        Kommando(182, tilsluttet_referere(BACK_værditype)); Kommando(182, ekstern_referere(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int Sammenligning_udtryk() {
        int Type_VÆRDI = 합식();
        while (!fejl && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int kodning_VÆRDI = 종류(); Placering++; bekræfte_Type(Type_VÆRDI, 1); bekræfte_Type(합식(), 1);
            Sammenligning_VÆRDI(kodning_VÆRDI == '<' ? 161 : kodning_VÆRDI == '>' ? 163 : kodning_VÆRDI == 302 ? 164 : 162); Type_VÆRDI = 2;
        }
        return Type_VÆRDI;
    }
    static int 동등식() {
        int Type_VÆRDI = Sammenligning_udtryk();
        while (!fejl && (종류() == 300 || 종류() == 301)) {
            int kodning_VÆRDI = 종류(); Placering++; int BACK_værditype = Sammenligning_udtryk();
            if (Type_VÆRDI == 0 || BACK_værditype == 0) fejl_VÆRDI("void expression");
            if (!(heltal_Type(Type_VÆRDI) && heltal_Type(BACK_værditype))) bekræfte_Type(BACK_værditype, Type_VÆRDI);
            Sammenligning_VÆRDI((Type_VÆRDI <= 2 || Type_VÆRDI == 5 ? 159 : 165) + (kodning_VÆRDI == 301 ? 1 : 0)); Type_VÆRDI = 2;
        }
        return Type_VÆRDI;
    }
    static int OG() {
        int Type_VÆRDI = 동등식();
        while (!fejl && modtage(304)) {
            bekræfte_Type(Type_VÆRDI, 2); int 가 = gren(153); bekræfte_Type(동등식(), 2); int SEKUND_operand = gren(153);
            내보내기(4); int 끝 = gren(167); Link_VÆRDI(가, KODE_tilpasse_størrelse); Link_VÆRDI(SEKUND_operand, KODE_tilpasse_størrelse); 내보내기(3); Link_VÆRDI(끝, KODE_tilpasse_størrelse); Type_VÆRDI = 2;
        }
        return Type_VÆRDI;
    }
    static int udtryk_VÆRDI() {
        int Type_VÆRDI = OG();
        while (!fejl && modtage(305)) {
            bekræfte_Type(Type_VÆRDI, 2); int 가 = gren(154); bekræfte_Type(OG(), 2); int SEKUND_operand = gren(154);
            내보내기(3); int 끝 = gren(167); Link_VÆRDI(가, KODE_tilpasse_størrelse); Link_VÆRDI(SEKUND_operand, KODE_tilpasse_størrelse); 내보내기(4); Link_VÆRDI(끝, KODE_tilpasse_størrelse); Type_VÆRDI = 2;
        }
        return Type_VÆRDI;
    }
    static void opgave_VÆRDI(boolean Tillad_erklæring) {
        if (Ord_VÆRDI(Placering, "int") || Ord_VÆRDI(Placering, "boolean") || Ord_VÆRDI(Placering, "String") || Ord_VÆRDI(Placering, "char")
            || Ord_VÆRDI(Placering, "FileInputStream") || Ord_VÆRDI(Placering, "FileOutputStream")) {
            if (!Tillad_erklæring) fejl_VÆRDI("declaration not allowed here");
            int Type_VÆRDI = format_VÆRDI(), Navn = identifikator_VÆRDI(); krav_VÆRDI('='); bekræfte_Type(udtryk_VÆRDI(), Type_VÆRDI);
            skrive_lokal(Tilføj_lokal(Navn, Type_VÆRDI)); return;
        }
        int Navn = identifikator_VÆRDI(), lokal_Omfang = Søg_lokal(Navn);
        if (modtage('=')) { bekræfte_Type(udtryk_VÆRDI(), lokal_Type[lokal_Omfang]); skrive_lokal(lokal_Omfang); }
        else if (종류() >= 308 && 종류() <= 312) {
            int kodning_VÆRDI = 종류(); Placering++; 지역읽기(lokal_Omfang); int grænse_VÆRDI = KODE_tilpasse_størrelse, BACK_værditype = udtryk_VÆRDI();
            if (kodning_VÆRDI == 308 && lokal_Type[lokal_Omfang] == 3) 결합(grænse_VÆRDI, 3, BACK_værditype);
            else {
                bekræfte_Type(lokal_Type[lokal_Omfang], 1); bekræfte_Type(BACK_værditype, 1);
                내보내기(kodning_VÆRDI == 308 ? 96 : kodning_VÆRDI == 309 ? 100 : kodning_VÆRDI == 310 ? 104 : kodning_VÆRDI == 311 ? 108 : 112);
                if (lokal_Type[lokal_Omfang] == 5) 내보내기(146);
            }
            skrive_lokal(lokal_Omfang);
        }
        else if (종류() == 306 || 종류() == 307) {
            bekræfte_Type(lokal_Type[lokal_Omfang], 1); 내보내기(132); 내보내기(lokal_Omfang); 내보내기(종류() == 306 ? 1 : 255); Placering++;
            if (lokal_Type[lokal_Omfang] == 5) { 지역읽기(lokal_Omfang); 내보내기(146); skrive_lokal(lokal_Omfang); }
        } else fejl_VÆRDI("assignment or postfix increment required");
    }
    static void skærmbillede_produktoutput() {
        말요구("System"); krav_VÆRDI('.'); 말요구("out"); krav_VÆRDI('.');
        boolean 줄바꿈 = TAG_Ord("println"); if (!줄바꿈) 말요구("print"); krav_VÆRDI('(');
        Kommando(178, ekstern_referere(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean 빈인수 = 종류() == ')';
        int Type_VÆRDI = 빈인수 ? 0 : udtryk_VÆRDI(); krav_VÆRDI(')'); krav_VÆRDI(';');
        String 서술 = Type_VÆRDI == 0 ? "()V" : Type_VÆRDI == 1 ? "(I)V" : Type_VÆRDI == 2 ? "(Z)V" : Type_VÆRDI == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (Type_VÆRDI == 4 || Type_VÆRDI >= 6 || Type_VÆRDI == 0 && (!줄바꿈 || !빈인수)) fejl_VÆRDI("unsupported print argument");
        Kommando(182, ekstern_referere(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean sætning_VÆRDI() {
        if (fejl) return false;
        if (깊이 > 32) { fejl_VÆRDI("statement nesting too deep"); return false; }
        if (modtage('{')) {
            깊이++; boolean returnere_KR = false;
            while (!fejl && 종류() != '}') { if (returnere_KR) fejl_VÆRDI("unreachable statement"); returnere_KR = sætning_VÆRDI(); }
            krav_VÆRDI('}'); for (int tal = 0; tal < lokal_TÆL; tal++) if (지역깊이[tal] == 깊이) 지역깊이[tal] = -1;
            깊이--; return returnere_KR;
        }
        if (modtage(';')) return false;
        if (TAG_Ord("return")) {
            int Type_VÆRDI = 종류() == ';' ? 0 : udtryk_VÆRDI(); bekræfte_Type(Type_VÆRDI, metode_returnere[aktuel_metode]); krav_VÆRDI(';');
            내보내기(Type_VÆRDI == 0 ? 177 : Type_VÆRDI <= 2 || Type_VÆRDI == 5 ? 172 : 176); return true;
        }
        if (TAG_Ord("if")) {
            krav_VÆRDI('('); bekræfte_Type(udtryk_VÆRDI(), 2); krav_VÆRDI(')'); int FALSK_VÆRDI = gren(153);
            깊이++; boolean 가 = kontrol_sætning(); 깊이--;
            if (TAG_Ord("else")) { int 끝 = gren(167); Link_VÆRDI(FALSK_VÆRDI, KODE_tilpasse_størrelse); 깊이++; boolean SEKUND_operand = kontrol_sætning(); 깊이--; Link_VÆRDI(끝, KODE_tilpasse_størrelse); return 가 && SEKUND_operand; }
            Link_VÆRDI(FALSK_VÆRDI, KODE_tilpasse_størrelse); return false;
        }
        if (TAG_Ord("while")) {
            int Kør_2 = KODE_tilpasse_størrelse; krav_VÆRDI('('); bekræfte_Type(udtryk_VÆRDI(), 2); krav_VÆRDI(')'); int 끝 = gren(153);
            깊이++; kontrol_sætning(); 깊이--; Link_VÆRDI(gren(167), Kør_2); Link_VÆRDI(끝, KODE_tilpasse_størrelse); return false;
        }
        if (TAG_Ord("for")) {
            깊이++; krav_VÆRDI('('); if (종류() != ';') opgave_VÆRDI(true); krav_VÆRDI(';');
            int lidelse = KODE_tilpasse_størrelse; if (종류() == ';') 내보내기(4); else bekræfte_Type(udtryk_VÆRDI(), 2); krav_VÆRDI(';');
            int 끝 = gren(153), brødtekst = gren(167), opdatere = KODE_tilpasse_størrelse;
            if (종류() != ')') opgave_VÆRDI(false); krav_VÆRDI(')'); Link_VÆRDI(gren(167), lidelse); Link_VÆRDI(brødtekst, KODE_tilpasse_størrelse);
            kontrol_sætning(); Link_VÆRDI(gren(167), opdatere); Link_VÆRDI(끝, KODE_tilpasse_størrelse);
            for (int tal = 0; tal < lokal_TÆL; tal++) if (지역깊이[tal] == 깊이) 지역깊이[tal] = -1;
            깊이--; return false;
        }
        if (Ord_VÆRDI(Placering, "System")) { skærmbillede_produktoutput(); return false; }
        if (종류() == 256 && Placering + 1 < token_TÆL && (토큰종류[Placering + 1] == '(' || 토큰종류[Placering + 1] == '.')) {
            int Type_VÆRDI = udtryk_VÆRDI(); if (Type_VÆRDI != 0) 내보내기(87); krav_VÆRDI(';'); return false;
        }
        opgave_VÆRDI(true); krav_VÆRDI(';'); return false;
    }
    static boolean kontrol_sætning() {
        if (Ord_VÆRDI(Placering, "int") || Ord_VÆRDI(Placering, "boolean") || Ord_VÆRDI(Placering, "char") || Ord_VÆRDI(Placering, "String")
            || Ord_VÆRDI(Placering, "FileInputStream") || Ord_VÆRDI(Placering, "FileOutputStream")) fejl_VÆRDI("local declaration requires braces");
        return sætning_VÆRDI();
    }
    static void 출바(int VÆRDI) { if (produktoutput_tilpasse_størrelse == Udgang.length) fejl_VÆRDI("class file too large"); else Udgang[produktoutput_tilpasse_størrelse++] = VÆRDI & 255; }
    static void 출짧(int VÆRDI) { 출바(VÆRDI >> 8); 출바(VÆRDI); }
    static void 출정(int VÆRDI) { 출짧(VÆRDI >>> 16); 출짧(VÆRDI); }
    static void skrive_Hold() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(konstant_TÆL);
        for (int tal = 0; tal < konstant_tilpasse_størrelse; tal++) 출바(konstant_VÆRDI[tal]);
        출짧(0x21); 출짧(Hold_konstant); 출짧(overordnet_konstant); 출짧(0); 출짧(0); 출짧(metode_TÆL);
        for (int tal = 0; tal < metode_TÆL; tal++) {
            출짧(metode_åbne[tal]); 출짧(metode_navn_konstant[tal]); 출짧(함수서술[tal]); 출짧(1); 출짧(KODE_konstant);
            출정(12 + metode_varighed[tal]); 출짧(128); 출짧(함수지역[tal]); 출정(metode_varighed[tal]);
            for (int udvidelsesstik_post = 0; udvidelsesstik_post < metode_varighed[tal]; udvidelsesstik_post++) 출바(KODE_VÆRDI[metode_KODE[tal] + udvidelsesstik_post]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int Kør_2() {
        if (bruger.인수개수() == 1 && 자바도구.같음(bruger.Argumenter(0), "-version")) {
            bruger.Skrive("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (bruger.인수개수() != 1) { bruger.Skrive("Usage: javac FILE.java\n"); return 2; }
        int navn_tilpasse_størrelse = 자바도구.Navn(filnavn_sms, bruger.Argumenter(0));
        if (navn_tilpasse_størrelse < 6 || navn_tilpasse_størrelse > 62 || filnavn_sms[navn_tilpasse_størrelse - 5] != '.' || filnavn_sms[navn_tilpasse_størrelse - 4] != 'j'
            || filnavn_sms[navn_tilpasse_størrelse - 3] != 'a' || filnavn_sms[navn_tilpasse_størrelse - 2] != 'v' || filnavn_sms[navn_tilpasse_størrelse - 1] != 'a') {
            bruger.Skrive("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        kilde_tilpasse_størrelse = bruger.파일읽기(filnavn_sms, KILDE);
        if (kilde_tilpasse_størrelse < 0) { bruger.Skrive("javac: cannot read source: "); 자바도구.skrive_tal(kilde_tilpasse_størrelse); bruger.skrive_tegn_VÆRDI(10); return 1; }
        kilde_tilpasse_størrelse = 자바도구.원문해독(KILDE, kilde_tilpasse_størrelse);
        if (kilde_tilpasse_størrelse < 0) { bruger.Skrive("javac error: invalid UTF-8 source\n"); return 1; }
        klip_VÆRDI(); if (!fejl) 선언읽기();
        if (!fejl) {
            if (token_varighed[Hold_token] != navn_tilpasse_størrelse - 5) fejl_VÆRDI("class name must match file name");
            for (int tal = 0; tal < navn_tilpasse_størrelse - 5; tal++) if (KILDE[token_placere[Hold_token] + tal] != filnavn_sms[tal]) fejl_VÆRDI("class name must match file name");
        }
        for (aktuel_metode = 0; aktuel_metode < metode_TÆL && !fejl; aktuel_metode++) {
            Placering = metode_brødtekst[aktuel_metode]; metode_KODE[aktuel_metode] = KODE_tilpasse_størrelse; lokal_TÆL = 0; 깊이 = 0;
            for (int tal = 0; tal < metode_argument_TÆL[aktuel_metode]; tal++) Tilføj_lokal(metode_argument_navn[aktuel_metode * 16 + tal], metode_argument_Type[aktuel_metode * 16 + tal]);
            boolean returnere_KR = sætning_VÆRDI();
            if (!returnere_KR && metode_returnere[aktuel_metode] != 0) fejl_VÆRDI("missing return");
            // gren 뒤의 합류 지점은 반드시 faktisk_data 명령이어야 한다 (버전 49 검증기).
            if (metode_returnere[aktuel_metode] == 0) 내보내기(177);
            else { boolean heltal = metode_returnere[aktuel_metode] <= 2 || metode_returnere[aktuel_metode] == 5; 내보내기(heltal ? 3 : 1); 내보내기(heltal ? 172 : 176); }
            if (Placering != metode_afslutte_et_opkald[aktuel_metode]) fejl_VÆRDI("invalid method body");
            함수지역[aktuel_metode] = lokal_TÆL; metode_varighed[aktuel_metode] = KODE_tilpasse_størrelse - metode_KODE[aktuel_metode];
        }
        if (fejl) return 1;
        skrive_Hold(); if (fejl) return 1;
        filnavn_sms[navn_tilpasse_størrelse - 4] = 'c'; filnavn_sms[navn_tilpasse_størrelse - 3] = 'l'; filnavn_sms[navn_tilpasse_størrelse - 2] = 'a';
        filnavn_sms[navn_tilpasse_størrelse - 1] = 's'; filnavn_sms[navn_tilpasse_størrelse] = 's'; filnavn_sms[navn_tilpasse_størrelse + 1] = 0;
        int KR = bruger.skrive_fil(filnavn_sms, Udgang, produktoutput_tilpasse_størrelse);
        if (KR < 0) { bruger.Skrive("javac: cannot save class: "); 자바도구.skrive_tal(KR); bruger.skrive_tegn_VÆRDI(10); return 1; }
        bruger.Skrive("Compiled: "); for (int tal = 0; filnavn_sms[tal] != 0; tal++) bruger.skrive_tegn_VÆRDI(filnavn_sms[tal]);
        bruger.Skrive(" (JVM class version 49)\n"); return 0;
    }
}
