// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java kilde_tre -> 표준 버전 49 class kompilator. */
public final class 자바컴파일러 {
    static int[] KILDE = new int[16384], Utgang = new int[16384], KODE_VERDI = new int[4096];
    static int[] 토큰종류 = new int[2048], token_plassere = new int[2048], token_lengde = new int[2048];
    static int[] konstant_VERDI = new int[4096], konstant_FORSKYVNING = new int[512];
    static int[] 문자 = new int[512], filnavn_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int kilde_skalere, token_ANTALL, Posisjon, KODE_skalere, konstant_skalere, konstant_ANTALL = 1, produksjon_skalere, tegn_lengde;
    static boolean feil;
    static int time_token, time_konstant, overordnet_konstant, KODE_konstant;
    static int[] metode_oppføring_navn = new int[32], metode_return = new int[32], metode_argument_ANTALL = new int[32];
    static int[] metode_argument_navn = new int[512], metode_argument_Type = new int[512];
    static int[] metode_brødtekst = new int[32], metode_avslutte_en_samtale = new int[32], metode_KODE = new int[32];
    static int[] metode_lengde = new int[32], 함수지역 = new int[32], metode_navn_konstant = new int[32], 함수서술 = new int[32];
    static int[] metode_tilgang = new int[32];
    static int metode_ANTALL, betalt_metode, lokal_ANTALL, 깊이, 식깊이;
    static int[] lokal_navn = new int[128], lokal_Type = new int[128], 지역깊이 = new int[128];

    static void feil_VERDI(String 이유) {
        if (!feil) {
            bruker.Skriv("javac error: "); bruker.Skriv(이유);
            bruker.Skriv(" at line ");
            int Linje = 1, 끝 = Posisjon < token_ANTALL ? token_plassere[Posisjon] : kilde_skalere;
            for (int nummer = 0; nummer < 끝; nummer++) if (KILDE[nummer] == 10) Linje++;
            자바도구.skrive_nummer(Linje); bruker.skrive_tegn_VERDI(10);
        }
        feil = true;
    }
    static boolean tegn_VERDI(int VERDI) { return 문자이름규칙.첫글자(VERDI); }
    static boolean siffer_VERDI(int VERDI) { return VERDI >= '0' && VERDI <= '9'; }
    static boolean 이름같음(int 가, int SEKUND_operand) {
        if (가 < 0 || SEKUND_operand < 0 || 가 >= token_ANTALL || SEKUND_operand >= token_ANTALL || token_lengde[가] != token_lengde[SEKUND_operand]) return false;
        for (int nummer = 0; nummer < token_lengde[가]; nummer++) if (KILDE[token_plassere[가] + nummer] != KILDE[token_plassere[SEKUND_operand] + nummer]) return false;
        return true;
    }
    static boolean ord_VERDI(int token_VERDI, String ord_SMS) {
        if (token_VERDI < 0 || token_VERDI >= token_ANTALL || token_lengde[token_VERDI] != ord_SMS.length()) return false;
        for (int nummer = 0; nummer < ord_SMS.length(); nummer++) if (KILDE[token_plassere[token_VERDI] + nummer] != ord_SMS.charAt(nummer)) return false;
        return true;
    }
    static int 종류() { return Posisjon < token_ANTALL ? 토큰종류[Posisjon] : 0; }
    static boolean motta(int VERDI) { if (종류() != VERDI) return false; Posisjon++; return true; }
    static void krav_VERDI(int VERDI) { if (!motta(VERDI)) feil_VERDI("unexpected token"); }
    static boolean TA_ord(String ord_SMS) { if (!ord_VERDI(Posisjon, ord_SMS)) return false; Posisjon++; return true; }
    static void 말요구(String ord_SMS) { if (!TA_ord(ord_SMS)) feil_VERDI(ord_SMS); }
    static int identifikator_VERDI() {
        int KR = Posisjon;
        if (종류() != 256) feil_VERDI("identifier required"); else Posisjon++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int Kjør_2 = 0;
        for (int nummer = 0; nummer <= 예약어.length(); nummer++) {
            if (nummer == 예약어.length() || 예약어.charAt(nummer) == ' ') {
                boolean 같음 = nummer - Kjør_2 == token_lengde[KR];
                for (int åpning_oppføring = Kjør_2; 같음 && åpning_oppføring < nummer; åpning_oppføring++) if (예약어.charAt(åpning_oppføring) != KILDE[token_plassere[KR] + åpning_oppføring - Kjør_2]) 같음 = false;
                if (같음) feil_VERDI("reserved word cannot be an identifier");
                Kjør_2 = nummer + 1;
            }
        }
        return KR;
    }
    static void klippe_VERDI_4601577b() {
        int nummer = 0;
        while (nummer < kilde_skalere && !feil) {
            int VERDI = KILDE[nummer], Kjør_2 = nummer, 종류 = VERDI;
            if (VERDI == 32 || VERDI == 9 || VERDI == 10 || VERDI == 13) { nummer++; continue; }
            if (VERDI == '/' && nummer + 1 < kilde_skalere && KILDE[nummer + 1] == '/') {
                while (nummer < kilde_skalere && KILDE[nummer] != 10) nummer++;
                continue;
            }
            if (VERDI == '/' && nummer + 1 < kilde_skalere && KILDE[nummer + 1] == '*') {
                nummer += 2;
                while (nummer + 1 < kilde_skalere && !(KILDE[nummer] == '*' && KILDE[nummer + 1] == '/')) nummer++;
                if (nummer + 1 >= kilde_skalere) { feil_VERDI("unterminated comment"); break; }
                nummer += 2; continue;
            }
            if (tegn_VERDI(VERDI)) { 종류 = 256; while (nummer < kilde_skalere && 문자이름규칙.이어진글자(KILDE[nummer])) nummer++; }
            else if (siffer_VERDI(VERDI)) { 종류 = 257; while (nummer < kilde_skalere && siffer_VERDI(KILDE[nummer])) nummer++; }
            else if (VERDI == '"' || VERDI == '\'') {
                종류 = VERDI == '"' ? 258 : 259; nummer++;
                while (nummer < kilde_skalere && KILDE[nummer] != VERDI && KILDE[nummer] != 10 && KILDE[nummer] != 13) {
                    if (KILDE[nummer] == '\\') nummer++;
                    nummer++;
                }
                if (nummer >= kilde_skalere || KILDE[nummer] != VERDI) { feil_VERDI("unterminated literal"); break; }
                nummer++;
            } else {
                nummer++;
                if (nummer < kilde_skalere) {
                    int Neste_vare = KILDE[nummer];
                    if (VERDI == '=' && Neste_vare == '=') 종류 = 300;
                    if (VERDI == '!' && Neste_vare == '=') 종류 = 301;
                    if (VERDI == '<' && Neste_vare == '=') 종류 = 302;
                    if (VERDI == '>' && Neste_vare == '=') 종류 = 303;
                    if (VERDI == '&' && Neste_vare == '&') 종류 = 304;
                    if (VERDI == '|' && Neste_vare == '|') 종류 = 305;
                    if (VERDI == '+' && Neste_vare == '+') 종류 = 306;
                    if (VERDI == '-' && Neste_vare == '-') 종류 = 307;
                    if (VERDI == '+' && Neste_vare == '=') 종류 = 308;
                    if (VERDI == '-' && Neste_vare == '=') 종류 = 309;
                    if (VERDI == '*' && Neste_vare == '=') 종류 = 310;
                    if (VERDI == '/' && Neste_vare == '=') 종류 = 311;
                    if (VERDI == '%' && Neste_vare == '=') 종류 = 312;
                    if (종류 >= 300) nummer++;
                }
            }
            if (token_ANTALL == 토큰종류.length - 1) { feil_VERDI("too many tokens (2047 maximum)"); break; }
            토큰종류[token_ANTALL] = 종류; token_plassere[token_ANTALL] = Kjør_2; token_lengde[token_ANTALL++] = nummer - Kjør_2;
        }
    }
    static void skrive_konstant_byte(int VERDI) {
        if (konstant_skalere == konstant_VERDI.length) { feil_VERDI("constant pool too large"); return; }
        konstant_VERDI[konstant_skalere++] = VERDI & 255;
    }
    static void 상짧(int VERDI) { skrive_konstant_byte(VERDI >> 8); skrive_konstant_byte(VERDI); }
    static int register_konstant(int Kjør_2) {
        for (int nummer = 1; nummer < konstant_ANTALL; nummer++) {
            int frontkamera_VERDI = konstant_FORSKYVNING[nummer], lengde_VERDI = (nummer + 1 < konstant_ANTALL ? konstant_FORSKYVNING[nummer + 1] : Kjør_2) - frontkamera_VERDI;
            if (lengde_VERDI != konstant_skalere - Kjør_2) continue;
            boolean 같음 = true;
            for (int åpning_oppføring = 0; åpning_oppføring < lengde_VERDI; åpning_oppføring++) if (konstant_VERDI[frontkamera_VERDI + åpning_oppføring] != konstant_VERDI[Kjør_2 + åpning_oppføring]) 같음 = false;
            if (같음) { konstant_skalere = Kjør_2; return nummer; }
        }
        if (konstant_ANTALL == konstant_FORSKYVNING.length) { feil_VERDI("too many constants"); return 0; }
        konstant_FORSKYVNING[konstant_ANTALL] = Kjør_2;
        return konstant_ANTALL++;
    }
    static void Tilføye_SMS(int VERDI) {
        if (tegn_lengde == 문자.length) { feil_VERDI("text too long"); return; }
        문자[tegn_lengde++] = VERDI;
    }
    static void Tilføye_ord(String ord_SMS) { for (int nummer = 0; nummer < ord_SMS.length(); nummer++) Tilføye_SMS(ord_SMS.charAt(nummer)); }
    static int tegn_konstant() {
        int Kjør_2 = konstant_skalere; skrive_konstant_byte(1); 상짧(0);
        for (int nummer = 0; nummer < tegn_lengde; nummer++) {
            int VERDI = 문자[nummer];
            if (VERDI > 0 && VERDI < 128) skrive_konstant_byte(VERDI);
            else if (VERDI < 2048) { skrive_konstant_byte(192 | VERDI >> 6); skrive_konstant_byte(128 | VERDI & 63); }
            else { skrive_konstant_byte(224 | VERDI >> 12); skrive_konstant_byte(128 | VERDI >> 6 & 63); skrive_konstant_byte(128 | VERDI & 63); }
        }
        if (feil) return 0;
        int lengde_VERDI = konstant_skalere - Kjør_2 - 3;
        konstant_VERDI[Kjør_2 + 1] = lengde_VERDI >> 8; konstant_VERDI[Kjør_2 + 2] = lengde_VERDI & 255;
        return register_konstant(Kjør_2);
    }
    static int ord_konstant(String ord_SMS) { tegn_lengde = 0; Tilføye_ord(ord_SMS); return tegn_konstant(); }
    static int token_konstant(int token_VERDI) {
        tegn_lengde = 0;
        for (int nummer = 0; nummer < token_lengde[token_VERDI]; nummer++) Tilføye_SMS(KILDE[token_plassere[token_VERDI] + nummer]);
        return tegn_konstant();
    }
    static int referere(int 종류, int 가, int SEKUND_operand) {
        int Kjør_2 = konstant_skalere; skrive_konstant_byte(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(SEKUND_operand);
        return register_konstant(Kjør_2);
    }
    static int ekstern_referere(int 종류, String eier_VERDI, String Navn, String 서술) {
        int eier_identifikator = referere(7, ord_konstant(eier_VERDI), 0);
        int navn_ANTALL = ord_konstant(Navn), format_ANTALL = ord_konstant(서술);
        return referere(종류, eier_identifikator, referere(12, navn_ANTALL, format_ANTALL));
    }
    static void 내보내기(int VERDI) {
        if (KODE_skalere == KODE_VERDI.length) { feil_VERDI("bytecode too large"); return; }
        KODE_VERDI[KODE_skalere++] = VERDI & 255;
    }
    static void Kommando(int VERDI, int Argumenter) { 내보내기(VERDI); 내보내기(Argumenter >> 8); 내보내기(Argumenter); }
    static void 수상수(int VERDI) {
        if (VERDI >= -1 && VERDI <= 5) { 내보내기(VERDI + 3); return; }
        int Kjør_2 = konstant_skalere; skrive_konstant_byte(3); 상짧(VERDI >>> 16); 상짧(VERDI);
        Kommando(19, register_konstant(Kjør_2));
    }
    static int gren(int Kommando) { int KR = KODE_skalere; Kommando(Kommando, 0); return KR; }
    static void koble_VERDI(int gren, int mål_objekt) {
        if (feil) return;
        int 거리 = mål_objekt - gren;
        if (거리 < -32768 || 거리 > 32767 || gren < 0 || gren + 2 >= KODE_skalere) { feil_VERDI("invalid branch"); return; }
        KODE_VERDI[gren + 1] = 거리 >> 8 & 255; KODE_VERDI[gren + 2] = 거리 & 255;
    }
    static void Sammenligning_VERDI(int Kommando) {
        int SANN_VERDI = gren(Kommando); 내보내기(3); int 끝 = gren(167);
        koble_VERDI(SANN_VERDI, KODE_skalere); 내보내기(4); koble_VERDI(끝, KODE_skalere);
    }
    static int format_VERDI() {
        if (TA_ord("void")) return 0;
        if (TA_ord("int")) return 1;
        if (TA_ord("boolean")) return 2;
        if (TA_ord("char")) return 5;
        if (TA_ord("FileInputStream")) return 6;
        if (TA_ord("FileOutputStream")) return 7;
        if (TA_ord("String")) { if (motta('[')) { krav_VERDI(']'); return 4; } return 3; }
        feil_VERDI("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void Legg_til_format(int Type_VERDI) {
        if (Type_VERDI == 0) Tilføye_SMS('V');
        if (Type_VERDI == 1) Tilføye_SMS('I');
        if (Type_VERDI == 2) Tilføye_SMS('Z');
        if (Type_VERDI == 3) Tilføye_ord("Ljava/lang/String;");
        if (Type_VERDI == 4) Tilføye_ord("[Ljava/lang/String;");
        if (Type_VERDI == 5) Tilføye_SMS('C');
        if (Type_VERDI == 6) Tilføye_ord("Ljava/io/FileInputStream;");
        if (Type_VERDI == 7) Tilføye_ord("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws erklæring. unntak Prosess_VERDI_oppføring 본문은 vert javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = TA_ord("norsk");
        if (한국어묶음) { krav_VERDI('.'); 말요구("eget"); krav_VERDI('.'); }
        if (!한국어묶음 && (TA_ord("Exception") || TA_ord("IOException"))) return;
        if (TA_ord("unntak") || TA_ord("kjøring_unntak") || TA_ord("I_U_unntak") || TA_ord("vent_TIMEOUT_unntak") || TA_ord("e_post_Oppslag_unntak") || TA_ord("파일없음예외") || TA_ord("통신예외") || TA_ord("ugyldig_argument_unntak") || TA_ord("nummer_format_feil") || TA_ord("범위예외") || TA_ord("배열범위예외") || TA_ord("문자열범위예외") || TA_ord("NULL_referere_unntak") || TA_ord("산술예외") || TA_ord("status_unntak") || TA_ord("Type_strømme_unntak") || TA_ord("음수배열크기예외") || TA_ord("MATRISE_Store_feil") || TA_ord("tråd_status_unntak") || TA_ord("대기중단예외")) return;
        feil_VERDI("unsupported throws type");
    }
    static void 선언읽기() {
        while (TA_ord("import")) {
            if (ord_VERDI(Posisjon, "norsk")) 예외이름읽기();
            else {
                말요구("java"); krav_VERDI('.'); 말요구("io"); krav_VERDI('.');
                if (!(TA_ord("FileInputStream") || TA_ord("FileOutputStream") || TA_ord("IOException"))) feil_VERDI("unsupported import");
            }
            krav_VERDI(';');
        }
        TA_ord("public"); TA_ord("final"); 말요구("class"); time_token = identifikator_VERDI();
        time_konstant = referere(7, token_konstant(time_token), 0);
        overordnet_konstant = referere(7, ord_konstant("java/lang/Object"), 0); KODE_konstant = ord_konstant("Code"); krav_VERDI('{');
        while (!feil && 종류() != '}') {
            if (metode_ANTALL == 32) { feil_VERDI("too many methods"); break; }
            int tilgang_oppføring = TA_ord("public") ? 1 : TA_ord("private") ? 2 : 0; 말요구("static");
            int FUNKSJON_VERDI = metode_ANTALL++;
            metode_tilgang[FUNKSJON_VERDI] = tilgang_oppføring | 8;
            metode_return[FUNKSJON_VERDI] = format_VERDI(); metode_oppføring_navn[FUNKSJON_VERDI] = identifikator_VERDI(); krav_VERDI('(');
            for (int frontkamera_VERDI = 0; frontkamera_VERDI < FUNKSJON_VERDI; frontkamera_VERDI++) if (이름같음(metode_oppføring_navn[frontkamera_VERDI], metode_oppføring_navn[FUNKSJON_VERDI])) feil_VERDI("duplicate method (overloading unsupported)");
            while (!feil && 종류() != ')') {
                int nummer = metode_argument_ANTALL[FUNKSJON_VERDI];
                if (nummer == 16) { feil_VERDI("too many parameters"); break; }
                int Type_VERDI = format_VERDI(); if (Type_VERDI == 0) feil_VERDI("void parameter");
                metode_argument_Type[FUNKSJON_VERDI * 16 + nummer] = Type_VERDI; metode_argument_navn[FUNKSJON_VERDI * 16 + nummer] = identifikator_VERDI();
                metode_argument_ANTALL[FUNKSJON_VERDI]++;
                if (!motta(',')) break;
            }
            krav_VERDI(')');
            if (TA_ord("throws")) {
                do { 예외이름읽기(); } while (!feil && motta(','));
            }
            metode_brødtekst[FUNKSJON_VERDI] = Posisjon; krav_VERDI('{');
            int nesting_VERDI = 1;
            while (Posisjon < token_ANTALL && nesting_VERDI > 0) {
                if (종류() == '{') nesting_VERDI++;
                if (종류() == '}') nesting_VERDI--;
                Posisjon++;
            }
            if (nesting_VERDI != 0) feil_VERDI("unclosed method body");
            metode_avslutte_en_samtale[FUNKSJON_VERDI] = Posisjon;
            metode_navn_konstant[FUNKSJON_VERDI] = token_konstant(metode_oppføring_navn[FUNKSJON_VERDI]);
            tegn_lengde = 0; Tilføye_SMS('(');
            for (int nummer = 0; nummer < metode_argument_ANTALL[FUNKSJON_VERDI]; nummer++) Legg_til_format(metode_argument_Type[FUNKSJON_VERDI * 16 + nummer]);
            Tilføye_SMS(')'); Legg_til_format(metode_return[FUNKSJON_VERDI]); 함수서술[FUNKSJON_VERDI] = tegn_konstant();
        }
        krav_VERDI('}'); if (Posisjon != token_ANTALL) feil_VERDI("extra input after class");
    }
    static int Søk_lokal(int Navn) {
        for (int nummer = lokal_ANTALL - 1; nummer >= 0; nummer--) if (지역깊이[nummer] >= 0 && 이름같음(lokal_navn[nummer], Navn)) return nummer;
        feil_VERDI("unknown variable"); return 0;
    }
    static int Legg_til_lokal(int Navn, int Type_VERDI) {
        for (int nummer = 0; nummer < lokal_ANTALL; nummer++) if (지역깊이[nummer] >= 0 && 이름같음(lokal_navn[nummer], Navn)) feil_VERDI("duplicate local variable");
        if (lokal_ANTALL == 128) { feil_VERDI("too many locals"); return 0; }
        lokal_navn[lokal_ANTALL] = Navn; lokal_Type[lokal_ANTALL] = Type_VERDI; 지역깊이[lokal_ANTALL] = 깊이;
        return lokal_ANTALL++;
    }
    static boolean heltall_Type(int Type_VERDI) { return Type_VERDI == 1 || Type_VERDI == 5; }
    static void 지역읽기(int nummer) { 내보내기(lokal_Type[nummer] <= 2 || lokal_Type[nummer] == 5 ? 21 : 25); 내보내기(nummer); }
    static void skrive_lokal(int nummer) { 내보내기(lokal_Type[nummer] <= 2 || lokal_Type[nummer] == 5 ? 54 : 58); 내보내기(nummer); }
    static void bekrefte_Type(int faktisk_data, int 기대) { if (faktisk_data != 기대 && !(faktisk_data == 5 && 기대 == 1)) feil_VERDI("type mismatch"); }
    static void 문자읽기(int token_VERDI) {
        tegn_lengde = 0; int Kjør_2 = token_plassere[token_VERDI] + 1, 끝 = token_plassere[token_VERDI] + token_lengde[token_VERDI] - 1;
        while (Kjør_2 < 끝 && !feil) {
            int VERDI = KILDE[Kjør_2++];
            if (VERDI == '\\') {
                if (Kjør_2 == 끝) { feil_VERDI("invalid escape"); break; }
                VERDI = KILDE[Kjør_2++];
                if (VERDI == 'n') VERDI = 10;
                else if (VERDI == 'r') VERDI = 13;
                else if (VERDI == 't') VERDI = 9;
                else if (VERDI == 'b') VERDI = 8;
                else if (VERDI == 'f') VERDI = 12;
                else if (VERDI != '\\' && VERDI != '"' && VERDI != '\'') feil_VERDI("unsupported escape");
            }
            Tilføye_SMS(VERDI);
        }
    }
    static int dele_opp_heltall(int token_VERDI, boolean 음수) {
        if (token_lengde[token_VERDI] > 1 && KILDE[token_plassere[token_VERDI]] == '0') feil_VERDI("octal literals unsupported");
        int VERDI = 0;
        for (int nummer = 0; nummer < token_lengde[token_VERDI]; nummer++) {
            int siffer_vare = KILDE[token_plassere[token_VERDI] + nummer] - '0';
            if (VERDI < -214748364 || VERDI == -214748364 && siffer_vare > (음수 ? 8 : 7)) feil_VERDI("integer literal out of range");
            VERDI = VERDI * 10 - siffer_vare;
        }
        return 음수 ? VERDI : -VERDI;
    }
    static int 기본식() {
        if (TA_ord("new")) {
            int Type_VERDI = format_VERDI();
            if (Type_VERDI != 6 && Type_VERDI != 7) { feil_VERDI("only file streams supported by new in source"); return 0; }
            String eier_VERDI = Type_VERDI == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            Kommando(187, referere(7, ord_konstant(eier_VERDI), 0)); 내보내기(89);
            krav_VERDI('('); bekrefte_Type(uttrykk_VERDI(), 3); boolean 이어 = false;
            if (motta(',')) { if (Type_VERDI != 7) feil_VERDI("input stream constructor arguments"); bekrefte_Type(uttrykk_VERDI(), 2); 이어 = true; }
            krav_VERDI(')');
            Kommando(183, ekstern_referere(10, eier_VERDI, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return Type_VERDI;
        }
        if (motta('(')) { int Type_VERDI = uttrykk_VERDI(); krav_VERDI(')'); return Type_VERDI; }
        if (종류() == 257) { 수상수(dele_opp_heltall(Posisjon++, false)); return 1; }
        if (종류() == 258) { 문자읽기(Posisjon++); Kommando(19, referere(8, tegn_konstant(), 0)); return 3; }
        if (종류() == 259) { 문자읽기(Posisjon++); if (tegn_lengde != 1) feil_VERDI("character literal length"); 수상수(문자[0]); return 5; }
        if (TA_ord("true")) { 내보내기(4); return 2; }
        if (TA_ord("false")) { 내보내기(3); return 2; }
        if (TA_ord("norsk")) {
            krav_VERDI('.'); 말요구("eget"); krav_VERDI('.');
            String eier_VERDI = "", metode_VERDI = "", 서술 = ""; int 가 = 0, SEKUND_operand = 0, 다 = 0, 라 = 0, 마 = 0, KR = 0;
            if (TA_ord("Utgang")) {
                eier_VERDI = "norsk/eget/Utgang"; krav_VERDI('.');
                if (TA_ord("skrive_linje")) { metode_VERDI = "skrive_linje"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TA_ord("Skriv")) { metode_VERDI = "Skriv"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TA_ord("skrive_nummer")) { metode_VERDI = "skrive_nummer"; 서술 = "(I)V"; 가 = 1; }
                else feil_VERDI("unknown Korean output method");
            } else if (TA_ord("문자")) {
                eier_VERDI = "norsk/eget/문자"; krav_VERDI('.'); 가 = 3;
                if (TA_ord("lengde_VERDI")) { metode_VERDI = "lengde_VERDI"; 서술 = "(Ljava/lang/String;)I"; KR = 1; }
                else if (TA_ord("tegnkode_ANTALL")) { metode_VERDI = "tegnkode_ANTALL"; 서술 = "(Ljava/lang/String;)I"; KR = 1; }
                else if (TA_ord("dele_opp_heltall")) { metode_VERDI = "dele_opp_heltall"; 서술 = "(Ljava/lang/String;)I"; KR = 1; }
                else if (TA_ord("skrive_heltall_VERDI")) { metode_VERDI = "skrive_heltall_VERDI"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; KR = 3; }
                else if (TA_ord("같음")) { metode_VERDI = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; SEKUND_operand = 3; KR = 2; }
                else if (TA_ord("lime_inn_SMS")) { metode_VERDI = "lime_inn_SMS"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; SEKUND_operand = 3; KR = 3; }
                else if (TA_ord("klippe_VERDI_4601577b")) { metode_VERDI = "klippe_VERDI_4601577b"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; SEKUND_operand = 1; 다 = 1; KR = 3; }
                else feil_VERDI("unknown Korean text method");
            } else if (TA_ord("Fil")) {
                eier_VERDI = "norsk/eget/Fil"; krav_VERDI('.'); 가 = 3;
                if (TA_ord("Les")) { metode_VERDI = "Les"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; KR = 3; }
                else if (TA_ord("Skriv")) { metode_VERDI = "Skriv"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; SEKUND_operand = 3; }
                else feil_VERDI("unknown Korean file method");
            } else if (TA_ord("skjermbilde")) {
                eier_VERDI = "norsk/eget/skjermbilde"; krav_VERDI('.');
                if (TA_ord("너비")) { metode_VERDI = "너비"; 서술 = "()I"; KR = 1; }
                else if (TA_ord("높이")) { metode_VERDI = "높이"; 서술 = "()I"; KR = 1; }
                else if (TA_ord("rektangel")) { metode_VERDI = "rektangel"; 서술 = "(IIIII)V"; 가 = 1; SEKUND_operand = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (TA_ord("slette_oppføring")) { metode_VERDI = "slette_oppføring"; 서술 = "(I)V"; 가 = 1; }
                else if (TA_ord("기다리기")) { metode_VERDI = "기다리기"; 서술 = "()V"; }
                else feil_VERDI("unknown Korean framebuffer method");
            } else feil_VERDI("unsupported Korean library class");
            krav_VERDI('('); if (가 != 0) bekrefte_Type(uttrykk_VERDI(), 가);
            if (SEKUND_operand != 0) { krav_VERDI(','); bekrefte_Type(uttrykk_VERDI(), SEKUND_operand); }
            if (다 != 0) { krav_VERDI(','); bekrefte_Type(uttrykk_VERDI(), 다); }
            if (라 != 0) { krav_VERDI(','); bekrefte_Type(uttrykk_VERDI(), 라); }
            if (마 != 0) { krav_VERDI(','); bekrefte_Type(uttrykk_VERDI(), 마); }
            krav_VERDI(')'); Kommando(184, ekstern_referere(10, eier_VERDI, metode_VERDI, 서술)); return KR;
        }
        if (TA_ord("Integer")) {
            krav_VERDI('.'); 말요구("parseInt"); krav_VERDI('('); bekrefte_Type(uttrykk_VERDI(), 3); krav_VERDI(')');
            Kommando(184, ekstern_referere(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Navn = identifikator_VERDI();
        if (motta('(')) {
            int FUNKSJON_VERDI = -1;
            for (int nummer = 0; nummer < metode_ANTALL; nummer++) if (이름같음(Navn, metode_oppføring_navn[nummer])) FUNKSJON_VERDI = nummer;
            if (FUNKSJON_VERDI < 0) { feil_VERDI("unknown static method"); return 0; }
            int nummer = 0;
            while (!feil && 종류() != ')') {
                if (nummer >= metode_argument_ANTALL[FUNKSJON_VERDI]) { feil_VERDI("too many arguments"); break; }
                bekrefte_Type(uttrykk_VERDI(), metode_argument_Type[FUNKSJON_VERDI * 16 + nummer++]); if (!motta(',')) break;
            }
            krav_VERDI(')'); if (nummer != metode_argument_ANTALL[FUNKSJON_VERDI]) feil_VERDI("argument count mismatch");
            Kommando(184, referere(10, time_konstant, referere(12, metode_navn_konstant[FUNKSJON_VERDI], 함수서술[FUNKSJON_VERDI])));
            return metode_return[FUNKSJON_VERDI];
        }
        int lokal_Omfang = Søk_lokal(Navn), Type_VERDI = lokal_Type[lokal_Omfang]; 지역읽기(lokal_Omfang);
        while (!feil) {
            if (motta('[')) { bekrefte_Type(Type_VERDI, 4); bekrefte_Type(uttrykk_VERDI(), 1); krav_VERDI(']'); 내보내기(50); Type_VERDI = 3; }
            else if (motta('.')) {
                if (Type_VERDI == 6 || Type_VERDI == 7) {
                    String eier_VERDI = Type_VERDI == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (TA_ord("close")) { krav_VERDI('('); krav_VERDI(')'); Kommando(182, ekstern_referere(10, eier_VERDI, "close", "()V")); Type_VERDI = 0; }
                    else if (Type_VERDI == 6 && TA_ord("read")) { krav_VERDI('('); krav_VERDI(')'); Kommando(182, ekstern_referere(10, eier_VERDI, "read", "()I")); Type_VERDI = 1; }
                    else if (Type_VERDI == 7 && TA_ord("write")) { krav_VERDI('('); bekrefte_Type(uttrykk_VERDI(), 1); krav_VERDI(')'); Kommando(182, ekstern_referere(10, eier_VERDI, "write", "(I)V")); Type_VERDI = 0; }
                    else { feil_VERDI("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (Type_VERDI == 4) { 내보내기(190); Type_VERDI = 1; }
                else { bekrefte_Type(Type_VERDI, 3); krav_VERDI('('); krav_VERDI(')'); Kommando(182, ekstern_referere(10, "java/lang/String", "length", "()I")); Type_VERDI = 1; }
            } else break;
        }
        return Type_VERDI;
    }
    static int 단항() {
        if (++식깊이 > 64) { feil_VERDI("expression nesting too deep"); 식깊이--; return 0; }
        int Type_VERDI;
        if (motta('!')) { bekrefte_Type(단항(), 2); Sammenligning_VERDI(153); Type_VERDI = 2; }
        else if (motta('-')) {
            if (종류() == 257) 수상수(dele_opp_heltall(Posisjon++, true));
            else { bekrefte_Type(단항(), 1); 내보내기(116); }
            Type_VERDI = 1;
        } else if (motta('+')) { bekrefte_Type(단항(), 1); Type_VERDI = 1; }
        else Type_VERDI = 기본식();
        식깊이--; return Type_VERDI;
    }
    static int 곱식() {
        int Type_VERDI = 단항();
        while (!feil && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int koding_VERDI = 종류(); Posisjon++; bekrefte_Type(Type_VERDI, 1); bekrefte_Type(단항(), 1);
            내보내기(koding_VERDI == '*' ? 104 : koding_VERDI == '/' ? 108 : 112); Type_VERDI = 1;
        }
        return Type_VERDI;
    }
    static int 합식() {
        int Type_VERDI = 곱식();
        while (!feil && (종류() == '+' || 종류() == '-')) {
            int koding_VERDI = 종류(); Posisjon++; int grense_VERDI = KODE_skalere, TILBAKE_verditype = 곱식();
            if (koding_VERDI == '+' && (Type_VERDI == 3 || TILBAKE_verditype == 3)) { 결합(grense_VERDI, Type_VERDI, TILBAKE_verditype); Type_VERDI = 3; }
            else { bekrefte_Type(Type_VERDI, 1); bekrefte_Type(TILBAKE_verditype, 1); 내보내기(koding_VERDI == '+' ? 96 : 100); Type_VERDI = 1; }
        }
        return Type_VERDI;
    }
    static int tilkoblet_referere(int Type_VERDI) {
        if (Type_VERDI != 1 && Type_VERDI != 2 && Type_VERDI != 3 && Type_VERDI != 5) feil_VERDI("unsupported concatenation type");
        return ekstern_referere(10, "java/lang/StringBuilder", "append", Type_VERDI == 1 ? "(I)Ljava/lang/StringBuilder;"
            : Type_VERDI == 2 ? "(Z)Ljava/lang/StringBuilder;" : Type_VERDI == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int grense_VERDI, int frontkamera_verditype, int TILBAKE_verditype) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 HØYRE KODE_VERDI 앞에 generere 코드를 삽입한다.
        // HØYRE uttrykk_VERDI 내부의 node_VERDI_6a3b6fa7 gren 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = KODE_skalere;
        Kommando(187, referere(7, ord_konstant("java/lang/StringBuilder"), 0)); 내보내기(89);
        Kommando(183, ekstern_referere(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); Kommando(182, tilkoblet_referere(frontkamera_verditype));
        if (feil) return;
        int lengde_VERDI = KODE_skalere - 끝;
        for (int nummer = 0; nummer < lengde_VERDI; nummer++) 삽입코드[nummer] = KODE_VERDI[끝 + nummer];
        for (int nummer = 끝 - 1; nummer >= grense_VERDI; nummer--) KODE_VERDI[nummer + lengde_VERDI] = KODE_VERDI[nummer];
        for (int nummer = 0; nummer < lengde_VERDI; nummer++) KODE_VERDI[grense_VERDI + nummer] = 삽입코드[nummer];
        Kommando(182, tilkoblet_referere(TILBAKE_verditype)); Kommando(182, ekstern_referere(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int Sammenligning_uttrykk() {
        int Type_VERDI = 합식();
        while (!feil && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int koding_VERDI = 종류(); Posisjon++; bekrefte_Type(Type_VERDI, 1); bekrefte_Type(합식(), 1);
            Sammenligning_VERDI(koding_VERDI == '<' ? 161 : koding_VERDI == '>' ? 163 : koding_VERDI == 302 ? 164 : 162); Type_VERDI = 2;
        }
        return Type_VERDI;
    }
    static int 동등식() {
        int Type_VERDI = Sammenligning_uttrykk();
        while (!feil && (종류() == 300 || 종류() == 301)) {
            int koding_VERDI = 종류(); Posisjon++; int TILBAKE_verditype = Sammenligning_uttrykk();
            if (Type_VERDI == 0 || TILBAKE_verditype == 0) feil_VERDI("void expression");
            if (!(heltall_Type(Type_VERDI) && heltall_Type(TILBAKE_verditype))) bekrefte_Type(TILBAKE_verditype, Type_VERDI);
            Sammenligning_VERDI((Type_VERDI <= 2 || Type_VERDI == 5 ? 159 : 165) + (koding_VERDI == 301 ? 1 : 0)); Type_VERDI = 2;
        }
        return Type_VERDI;
    }
    static int AND() {
        int Type_VERDI = 동등식();
        while (!feil && motta(304)) {
            bekrefte_Type(Type_VERDI, 2); int 가 = gren(153); bekrefte_Type(동등식(), 2); int SEKUND_operand = gren(153);
            내보내기(4); int 끝 = gren(167); koble_VERDI(가, KODE_skalere); koble_VERDI(SEKUND_operand, KODE_skalere); 내보내기(3); koble_VERDI(끝, KODE_skalere); Type_VERDI = 2;
        }
        return Type_VERDI;
    }
    static int uttrykk_VERDI() {
        int Type_VERDI = AND();
        while (!feil && motta(305)) {
            bekrefte_Type(Type_VERDI, 2); int 가 = gren(154); bekrefte_Type(AND(), 2); int SEKUND_operand = gren(154);
            내보내기(3); int 끝 = gren(167); koble_VERDI(가, KODE_skalere); koble_VERDI(SEKUND_operand, KODE_skalere); 내보내기(4); koble_VERDI(끝, KODE_skalere); Type_VERDI = 2;
        }
        return Type_VERDI;
    }
    static void oppgave_VERDI(boolean Tillat_erklæring) {
        if (ord_VERDI(Posisjon, "int") || ord_VERDI(Posisjon, "boolean") || ord_VERDI(Posisjon, "String") || ord_VERDI(Posisjon, "char")
            || ord_VERDI(Posisjon, "FileInputStream") || ord_VERDI(Posisjon, "FileOutputStream")) {
            if (!Tillat_erklæring) feil_VERDI("declaration not allowed here");
            int Type_VERDI = format_VERDI(), Navn = identifikator_VERDI(); krav_VERDI('='); bekrefte_Type(uttrykk_VERDI(), Type_VERDI);
            skrive_lokal(Legg_til_lokal(Navn, Type_VERDI)); return;
        }
        int Navn = identifikator_VERDI(), lokal_Omfang = Søk_lokal(Navn);
        if (motta('=')) { bekrefte_Type(uttrykk_VERDI(), lokal_Type[lokal_Omfang]); skrive_lokal(lokal_Omfang); }
        else if (종류() >= 308 && 종류() <= 312) {
            int koding_VERDI = 종류(); Posisjon++; 지역읽기(lokal_Omfang); int grense_VERDI = KODE_skalere, TILBAKE_verditype = uttrykk_VERDI();
            if (koding_VERDI == 308 && lokal_Type[lokal_Omfang] == 3) 결합(grense_VERDI, 3, TILBAKE_verditype);
            else {
                bekrefte_Type(lokal_Type[lokal_Omfang], 1); bekrefte_Type(TILBAKE_verditype, 1);
                내보내기(koding_VERDI == 308 ? 96 : koding_VERDI == 309 ? 100 : koding_VERDI == 310 ? 104 : koding_VERDI == 311 ? 108 : 112);
                if (lokal_Type[lokal_Omfang] == 5) 내보내기(146);
            }
            skrive_lokal(lokal_Omfang);
        }
        else if (종류() == 306 || 종류() == 307) {
            bekrefte_Type(lokal_Type[lokal_Omfang], 1); 내보내기(132); 내보내기(lokal_Omfang); 내보내기(종류() == 306 ? 1 : 255); Posisjon++;
            if (lokal_Type[lokal_Omfang] == 5) { 지역읽기(lokal_Omfang); 내보내기(146); skrive_lokal(lokal_Omfang); }
        } else feil_VERDI("assignment or postfix increment required");
    }
    static void skjermbilde_produksjon() {
        말요구("System"); krav_VERDI('.'); 말요구("out"); krav_VERDI('.');
        boolean 줄바꿈 = TA_ord("println"); if (!줄바꿈) 말요구("print"); krav_VERDI('(');
        Kommando(178, ekstern_referere(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean tom_argument = 종류() == ')';
        int Type_VERDI = tom_argument ? 0 : uttrykk_VERDI(); krav_VERDI(')'); krav_VERDI(';');
        String 서술 = Type_VERDI == 0 ? "()V" : Type_VERDI == 1 ? "(I)V" : Type_VERDI == 2 ? "(Z)V" : Type_VERDI == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (Type_VERDI == 4 || Type_VERDI >= 6 || Type_VERDI == 0 && (!줄바꿈 || !tom_argument)) feil_VERDI("unsupported print argument");
        Kommando(182, ekstern_referere(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean kontoutdrag_VERDI() {
        if (feil) return false;
        if (깊이 > 32) { feil_VERDI("statement nesting too deep"); return false; }
        if (motta('{')) {
            깊이++; boolean return_KR = false;
            while (!feil && 종류() != '}') { if (return_KR) feil_VERDI("unreachable statement"); return_KR = kontoutdrag_VERDI(); }
            krav_VERDI('}'); for (int nummer = 0; nummer < lokal_ANTALL; nummer++) if (지역깊이[nummer] == 깊이) 지역깊이[nummer] = -1;
            깊이--; return return_KR;
        }
        if (motta(';')) return false;
        if (TA_ord("return")) {
            int Type_VERDI = 종류() == ';' ? 0 : uttrykk_VERDI(); bekrefte_Type(Type_VERDI, metode_return[betalt_metode]); krav_VERDI(';');
            내보내기(Type_VERDI == 0 ? 177 : Type_VERDI <= 2 || Type_VERDI == 5 ? 172 : 176); return true;
        }
        if (TA_ord("if")) {
            krav_VERDI('('); bekrefte_Type(uttrykk_VERDI(), 2); krav_VERDI(')'); int USANN_VERDI = gren(153);
            깊이++; boolean 가 = kontroll_kontoutdrag(); 깊이--;
            if (TA_ord("else")) { int 끝 = gren(167); koble_VERDI(USANN_VERDI, KODE_skalere); 깊이++; boolean SEKUND_operand = kontroll_kontoutdrag(); 깊이--; koble_VERDI(끝, KODE_skalere); return 가 && SEKUND_operand; }
            koble_VERDI(USANN_VERDI, KODE_skalere); return false;
        }
        if (TA_ord("while")) {
            int Kjør_2 = KODE_skalere; krav_VERDI('('); bekrefte_Type(uttrykk_VERDI(), 2); krav_VERDI(')'); int 끝 = gren(153);
            깊이++; kontroll_kontoutdrag(); 깊이--; koble_VERDI(gren(167), Kjør_2); koble_VERDI(끝, KODE_skalere); return false;
        }
        if (TA_ord("for")) {
            깊이++; krav_VERDI('('); if (종류() != ';') oppgave_VERDI(true); krav_VERDI(';');
            int vilkår = KODE_skalere; if (종류() == ';') 내보내기(4); else bekrefte_Type(uttrykk_VERDI(), 2); krav_VERDI(';');
            int 끝 = gren(153), brødtekst = gren(167), oppdatere = KODE_skalere;
            if (종류() != ')') oppgave_VERDI(false); krav_VERDI(')'); koble_VERDI(gren(167), vilkår); koble_VERDI(brødtekst, KODE_skalere);
            kontroll_kontoutdrag(); koble_VERDI(gren(167), oppdatere); koble_VERDI(끝, KODE_skalere);
            for (int nummer = 0; nummer < lokal_ANTALL; nummer++) if (지역깊이[nummer] == 깊이) 지역깊이[nummer] = -1;
            깊이--; return false;
        }
        if (ord_VERDI(Posisjon, "System")) { skjermbilde_produksjon(); return false; }
        if (종류() == 256 && Posisjon + 1 < token_ANTALL && (토큰종류[Posisjon + 1] == '(' || 토큰종류[Posisjon + 1] == '.')) {
            int Type_VERDI = uttrykk_VERDI(); if (Type_VERDI != 0) 내보내기(87); krav_VERDI(';'); return false;
        }
        oppgave_VERDI(true); krav_VERDI(';'); return false;
    }
    static boolean kontroll_kontoutdrag() {
        if (ord_VERDI(Posisjon, "int") || ord_VERDI(Posisjon, "boolean") || ord_VERDI(Posisjon, "char") || ord_VERDI(Posisjon, "String")
            || ord_VERDI(Posisjon, "FileInputStream") || ord_VERDI(Posisjon, "FileOutputStream")) feil_VERDI("local declaration requires braces");
        return kontoutdrag_VERDI();
    }
    static void 출바(int VERDI) { if (produksjon_skalere == Utgang.length) feil_VERDI("class file too large"); else Utgang[produksjon_skalere++] = VERDI & 255; }
    static void 출짧(int VERDI) { 출바(VERDI >> 8); 출바(VERDI); }
    static void 출정(int VERDI) { 출짧(VERDI >>> 16); 출짧(VERDI); }
    static void skrive_time() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(konstant_ANTALL);
        for (int nummer = 0; nummer < konstant_skalere; nummer++) 출바(konstant_VERDI[nummer]);
        출짧(0x21); 출짧(time_konstant); 출짧(overordnet_konstant); 출짧(0); 출짧(0); 출짧(metode_ANTALL);
        for (int nummer = 0; nummer < metode_ANTALL; nummer++) {
            출짧(metode_tilgang[nummer]); 출짧(metode_navn_konstant[nummer]); 출짧(함수서술[nummer]); 출짧(1); 출짧(KODE_konstant);
            출정(12 + metode_lengde[nummer]); 출짧(128); 출짧(함수지역[nummer]); 출정(metode_lengde[nummer]);
            for (int åpning_oppføring = 0; åpning_oppføring < metode_lengde[nummer]; åpning_oppføring++) 출바(KODE_VERDI[metode_KODE[nummer] + åpning_oppføring]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int Kjør_2() {
        if (bruker.인수개수() == 1 && 자바도구.같음(bruker.Argumenter(0), "-version")) {
            bruker.Skriv("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (bruker.인수개수() != 1) { bruker.Skriv("Usage: javac FILE.java\n"); return 2; }
        int navn_skalere = 자바도구.Navn(filnavn_SMS, bruker.Argumenter(0));
        if (navn_skalere < 6 || navn_skalere > 62 || filnavn_SMS[navn_skalere - 5] != '.' || filnavn_SMS[navn_skalere - 4] != 'j'
            || filnavn_SMS[navn_skalere - 3] != 'a' || filnavn_SMS[navn_skalere - 2] != 'v' || filnavn_SMS[navn_skalere - 1] != 'a') {
            bruker.Skriv("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        kilde_skalere = bruker.파일읽기(filnavn_SMS, KILDE);
        if (kilde_skalere < 0) { bruker.Skriv("javac: cannot read source: "); 자바도구.skrive_nummer(kilde_skalere); bruker.skrive_tegn_VERDI(10); return 1; }
        kilde_skalere = 자바도구.원문해독(KILDE, kilde_skalere);
        if (kilde_skalere < 0) { bruker.Skriv("javac error: invalid UTF-8 source\n"); return 1; }
        klippe_VERDI_4601577b(); if (!feil) 선언읽기();
        if (!feil) {
            if (token_lengde[time_token] != navn_skalere - 5) feil_VERDI("class name must match file name");
            for (int nummer = 0; nummer < navn_skalere - 5; nummer++) if (KILDE[token_plassere[time_token] + nummer] != filnavn_SMS[nummer]) feil_VERDI("class name must match file name");
        }
        for (betalt_metode = 0; betalt_metode < metode_ANTALL && !feil; betalt_metode++) {
            Posisjon = metode_brødtekst[betalt_metode]; metode_KODE[betalt_metode] = KODE_skalere; lokal_ANTALL = 0; 깊이 = 0;
            for (int nummer = 0; nummer < metode_argument_ANTALL[betalt_metode]; nummer++) Legg_til_lokal(metode_argument_navn[betalt_metode * 16 + nummer], metode_argument_Type[betalt_metode * 16 + nummer]);
            boolean return_KR = kontoutdrag_VERDI();
            if (!return_KR && metode_return[betalt_metode] != 0) feil_VERDI("missing return");
            // gren 뒤의 합류 지점은 반드시 faktisk_data 명령이어야 한다 (버전 49 검증기).
            if (metode_return[betalt_metode] == 0) 내보내기(177);
            else { boolean heltall = metode_return[betalt_metode] <= 2 || metode_return[betalt_metode] == 5; 내보내기(heltall ? 3 : 1); 내보내기(heltall ? 172 : 176); }
            if (Posisjon != metode_avslutte_en_samtale[betalt_metode]) feil_VERDI("invalid method body");
            함수지역[betalt_metode] = lokal_ANTALL; metode_lengde[betalt_metode] = KODE_skalere - metode_KODE[betalt_metode];
        }
        if (feil) return 1;
        skrive_time(); if (feil) return 1;
        filnavn_SMS[navn_skalere - 4] = 'c'; filnavn_SMS[navn_skalere - 3] = 'l'; filnavn_SMS[navn_skalere - 2] = 'a';
        filnavn_SMS[navn_skalere - 1] = 's'; filnavn_SMS[navn_skalere] = 's'; filnavn_SMS[navn_skalere + 1] = 0;
        int KR = bruker.skrive_Fil(filnavn_SMS, Utgang, produksjon_skalere);
        if (KR < 0) { bruker.Skriv("javac: cannot save class: "); 자바도구.skrive_nummer(KR); bruker.skrive_tegn_VERDI(10); return 1; }
        bruker.Skriv("Compiled: "); for (int nummer = 0; filnavn_SMS[nummer] != 0; nummer++) bruker.skrive_tegn_VERDI(filnavn_SMS[nummer]);
        bruker.Skriv(" (JVM class version 49)\n"); return 0;
    }
}
