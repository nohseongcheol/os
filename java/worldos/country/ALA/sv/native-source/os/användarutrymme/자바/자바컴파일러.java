// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java källa_träd -> 표준 버전 49 class kompilerare. */
public final class 자바컴파일러 {
    static int[] källfil = new int[16384], utmatningsposition = new int[16384], KOD_värde = new int[4096];
    static int[] kod_variant = new int[2048], kod_placera = new int[2048], kod_längd = new int[2048];
    static int[] konstant_värde = new int[4096], konstant_FÖRSKJUTNING = new int[512];
    static int[] 문자 = new int[512], filnamn_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int källa_storlek, kod_ANTAL, position, KOD_storlek, konstant_storlek, konstant_ANTAL = 1, utleverans_storlek, tecken_längd;
    static boolean fel;
    static int Kurs_kod, Kurs_konstant, överordnad_konstant, KOD_konstant;
    static int[] metod_post_namn = new int[32], metod_Retur = new int[32], metod_argument_ANTAL = new int[32];
    static int[] metod_argument_namn = new int[512], metod_argument_Typ = new int[512];
    static int[] metod_brödtext = new int[32], metod_avsluta = new int[32], metod_KOD = new int[32];
    static int[] metod_längd = new int[32], 함수지역 = new int[32], metod_namn_konstant = new int[32], 함수서술 = new int[32];
    static int[] metod_ansluta = new int[32];
    static int metod_ANTAL, aktuellt_metod, lokal_ANTAL, 깊이, 식깊이;
    static int[] lokal_namn = new int[128], lokal_Typ = new int[128], 지역깊이 = new int[128];

    static void fel_värde(String 이유) {
        if (!fel) {
            användarutrymme.Skriv("javac error: "); användarutrymme.Skriv(이유);
            användarutrymme.Skriv(" at line ");
            int inmatningsrad = 1, 끝 = position < kod_ANTAL ? kod_placera[position] : källa_storlek;
            for (int nummer = 0; nummer < 끝; nummer++) if (källfil[nummer] == 10) inmatningsrad++;
            자바도구.skriva_nummer(inmatningsrad); användarutrymme.skriva_tecken_värde(10);
        }
        fel = true;
    }
    static boolean tecken_värde(int värde) { return 문자이름규칙.첫글자(värde); }
    static boolean siffra_värde(int värde) { return värde >= '0' && värde <= '9'; }
    static boolean 이름같음(int 가, int SEKUND_operand) {
        if (가 < 0 || SEKUND_operand < 0 || 가 >= kod_ANTAL || SEKUND_operand >= kod_ANTAL || kod_längd[가] != kod_längd[SEKUND_operand]) return false;
        for (int nummer = 0; nummer < kod_längd[가]; nummer++) if (källfil[kod_placera[가] + nummer] != källfil[kod_placera[SEKUND_operand] + nummer]) return false;
        return true;
    }
    static boolean Ord_värde(int kod_värde, String Ord_SMS) {
        if (kod_värde < 0 || kod_värde >= kod_ANTAL || kod_längd[kod_värde] != Ord_SMS.length()) return false;
        for (int nummer = 0; nummer < Ord_SMS.length(); nummer++) if (källfil[kod_placera[kod_värde] + nummer] != Ord_SMS.charAt(nummer)) return false;
        return true;
    }
    static int variant_värde() { return position < kod_ANTAL ? kod_variant[position] : 0; }
    static boolean få(int värde) { if (variant_värde() != värde) return false; position++; return true; }
    static void krav_värde(int värde) { if (!få(värde)) fel_värde("unexpected token"); }
    static boolean TA_Ord(String Ord_SMS) { if (!Ord_värde(position, Ord_SMS)) return false; position++; return true; }
    static void 말요구(String Ord_SMS) { if (!TA_Ord(Ord_SMS)) fel_värde(Ord_SMS); }
    static int identifierare_värde() {
        int RESULTAT = position;
        if (variant_värde() != 256) fel_värde("identifier required"); else position++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int Kör = 0;
        for (int nummer = 0; nummer <= 예약어.length(); nummer++) {
            if (nummer == 예약어.length() || 예약어.charAt(nummer) == ' ') {
                boolean 같음 = nummer - Kör == kod_längd[RESULTAT];
                for (int fack_post = Kör; 같음 && fack_post < nummer; fack_post++) if (예약어.charAt(fack_post) != källfil[kod_placera[RESULTAT] + fack_post - Kör]) 같음 = false;
                if (같음) fel_värde("reserved word cannot be an identifier");
                Kör = nummer + 1;
            }
        }
        return RESULTAT;
    }
    static void klippa_värde() {
        int nummer = 0;
        while (nummer < källa_storlek && !fel) {
            int värde = källfil[nummer], Kör = nummer, variant_värde = värde;
            if (värde == 32 || värde == 9 || värde == 10 || värde == 13) { nummer++; continue; }
            if (värde == '/' && nummer + 1 < källa_storlek && källfil[nummer + 1] == '/') {
                while (nummer < källa_storlek && källfil[nummer] != 10) nummer++;
                continue;
            }
            if (värde == '/' && nummer + 1 < källa_storlek && källfil[nummer + 1] == '*') {
                nummer += 2;
                while (nummer + 1 < källa_storlek && !(källfil[nummer] == '*' && källfil[nummer + 1] == '/')) nummer++;
                if (nummer + 1 >= källa_storlek) { fel_värde("unterminated comment"); break; }
                nummer += 2; continue;
            }
            if (tecken_värde(värde)) { variant_värde = 256; while (nummer < källa_storlek && 문자이름규칙.이어진글자(källfil[nummer])) nummer++; }
            else if (siffra_värde(värde)) { variant_värde = 257; while (nummer < källa_storlek && siffra_värde(källfil[nummer])) nummer++; }
            else if (värde == '"' || värde == '\'') {
                variant_värde = värde == '"' ? 258 : 259; nummer++;
                while (nummer < källa_storlek && källfil[nummer] != värde && källfil[nummer] != 10 && källfil[nummer] != 13) {
                    if (källfil[nummer] == '\\') nummer++;
                    nummer++;
                }
                if (nummer >= källa_storlek || källfil[nummer] != värde) { fel_värde("unterminated literal"); break; }
                nummer++;
            } else {
                nummer++;
                if (nummer < källa_storlek) {
                    int Nästa_objekt = källfil[nummer];
                    if (värde == '=' && Nästa_objekt == '=') variant_värde = 300;
                    if (värde == '!' && Nästa_objekt == '=') variant_värde = 301;
                    if (värde == '<' && Nästa_objekt == '=') variant_värde = 302;
                    if (värde == '>' && Nästa_objekt == '=') variant_värde = 303;
                    if (värde == '&' && Nästa_objekt == '&') variant_värde = 304;
                    if (värde == '|' && Nästa_objekt == '|') variant_värde = 305;
                    if (värde == '+' && Nästa_objekt == '+') variant_värde = 306;
                    if (värde == '-' && Nästa_objekt == '-') variant_värde = 307;
                    if (värde == '+' && Nästa_objekt == '=') variant_värde = 308;
                    if (värde == '-' && Nästa_objekt == '=') variant_värde = 309;
                    if (värde == '*' && Nästa_objekt == '=') variant_värde = 310;
                    if (värde == '/' && Nästa_objekt == '=') variant_värde = 311;
                    if (värde == '%' && Nästa_objekt == '=') variant_värde = 312;
                    if (variant_värde >= 300) nummer++;
                }
            }
            if (kod_ANTAL == kod_variant.length - 1) { fel_värde("too many tokens (2047 maximum)"); break; }
            kod_variant[kod_ANTAL] = variant_värde; kod_placera[kod_ANTAL] = Kör; kod_längd[kod_ANTAL++] = nummer - Kör;
        }
    }
    static void skriva_konstant_byte(int värde) {
        if (konstant_storlek == konstant_värde.length) { fel_värde("constant pool too large"); return; }
        konstant_värde[konstant_storlek++] = värde & 255;
    }
    static void 상짧(int värde) { skriva_konstant_byte(värde >> 8); skriva_konstant_byte(värde); }
    static int register_konstant(int Kör) {
        for (int nummer = 1; nummer < konstant_ANTAL; nummer++) {
            int framåtvänd_värde = konstant_FÖRSKJUTNING[nummer], längd_värde = (nummer + 1 < konstant_ANTAL ? konstant_FÖRSKJUTNING[nummer + 1] : Kör) - framåtvänd_värde;
            if (längd_värde != konstant_storlek - Kör) continue;
            boolean 같음 = true;
            for (int fack_post = 0; fack_post < längd_värde; fack_post++) if (konstant_värde[framåtvänd_värde + fack_post] != konstant_värde[Kör + fack_post]) 같음 = false;
            if (같음) { konstant_storlek = Kör; return nummer; }
        }
        if (konstant_ANTAL == konstant_FÖRSKJUTNING.length) { fel_värde("too many constants"); return 0; }
        konstant_FÖRSKJUTNING[konstant_ANTAL] = Kör;
        return konstant_ANTAL++;
    }
    static void Lägga_till_SMS(int värde) {
        if (tecken_längd == 문자.length) { fel_värde("text too long"); return; }
        문자[tecken_längd++] = värde;
    }
    static void Lägga_till_Ord(String Ord_SMS) { for (int nummer = 0; nummer < Ord_SMS.length(); nummer++) Lägga_till_SMS(Ord_SMS.charAt(nummer)); }
    static int tecken_konstant() {
        int Kör = konstant_storlek; skriva_konstant_byte(1); 상짧(0);
        for (int nummer = 0; nummer < tecken_längd; nummer++) {
            int värde = 문자[nummer];
            if (värde > 0 && värde < 128) skriva_konstant_byte(värde);
            else if (värde < 2048) { skriva_konstant_byte(192 | värde >> 6); skriva_konstant_byte(128 | värde & 63); }
            else { skriva_konstant_byte(224 | värde >> 12); skriva_konstant_byte(128 | värde >> 6 & 63); skriva_konstant_byte(128 | värde & 63); }
        }
        if (fel) return 0;
        int längd_värde = konstant_storlek - Kör - 3;
        konstant_värde[Kör + 1] = längd_värde >> 8; konstant_värde[Kör + 2] = längd_värde & 255;
        return register_konstant(Kör);
    }
    static int Ord_konstant(String Ord_SMS) { tecken_längd = 0; Lägga_till_Ord(Ord_SMS); return tecken_konstant(); }
    static int kod_konstant(int kod_värde) {
        tecken_längd = 0;
        for (int nummer = 0; nummer < kod_längd[kod_värde]; nummer++) Lägga_till_SMS(källfil[kod_placera[kod_värde] + nummer]);
        return tecken_konstant();
    }
    static int referens(int variant_värde, int 가, int SEKUND_operand) {
        int Kör = konstant_storlek; skriva_konstant_byte(variant_värde); 상짧(가);
        if (variant_värde == 9 || variant_värde == 10 || variant_värde == 12) 상짧(SEKUND_operand);
        return register_konstant(Kör);
    }
    static int extern_referens(int variant_värde, String ägare_värde, String Namn, String 서술) {
        int ägare_identifierare = referens(7, Ord_konstant(ägare_värde), 0);
        int namn_ANTAL = Ord_konstant(Namn), format_ANTAL = Ord_konstant(서술);
        return referens(variant_värde, ägare_identifierare, referens(12, namn_ANTAL, format_ANTAL));
    }
    static void 내보내기(int värde) {
        if (KOD_storlek == KOD_värde.length) { fel_värde("bytecode too large"); return; }
        KOD_värde[KOD_storlek++] = värde & 255;
    }
    static void kommando(int värde, int argument) { 내보내기(värde); 내보내기(argument >> 8); 내보내기(argument); }
    static void 수상수(int värde) {
        if (värde >= -1 && värde <= 5) { 내보내기(värde + 3); return; }
        int Kör = konstant_storlek; skriva_konstant_byte(3); 상짧(värde >>> 16); 상짧(värde);
        kommando(19, register_konstant(Kör));
    }
    static int gren(int kommando) { int RESULTAT = KOD_storlek; kommando(kommando, 0); return RESULTAT; }
    static void Länk_värde(int gren, int mål_objekt) {
        if (fel) return;
        int 거리 = mål_objekt - gren;
        if (거리 < -32768 || 거리 > 32767 || gren < 0 || gren + 2 >= KOD_storlek) { fel_värde("invalid branch"); return; }
        KOD_värde[gren + 1] = 거리 >> 8 & 255; KOD_värde[gren + 2] = 거리 & 255;
    }
    static void Jämförelse_värde(int kommando) {
        int SANT_värde = gren(kommando); 내보내기(3); int 끝 = gren(167);
        Länk_värde(SANT_värde, KOD_storlek); 내보내기(4); Länk_värde(끝, KOD_storlek);
    }
    static int format_värde() {
        if (TA_Ord("void")) return 0;
        if (TA_Ord("int")) return 1;
        if (TA_Ord("boolean")) return 2;
        if (TA_Ord("char")) return 5;
        if (TA_Ord("FileInputStream")) return 6;
        if (TA_Ord("FileOutputStream")) return 7;
        if (TA_Ord("String")) { if (få('[')) { krav_värde(']'); return 4; } return 3; }
        fel_värde("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void Lägg_till_format(int Typ_värde) {
        if (Typ_värde == 0) Lägga_till_SMS('V');
        if (Typ_värde == 1) Lägga_till_SMS('I');
        if (Typ_värde == 2) Lägga_till_SMS('Z');
        if (Typ_värde == 3) Lägga_till_Ord("Ljava/lang/String;");
        if (Typ_värde == 4) Lägga_till_Ord("[Ljava/lang/String;");
        if (Typ_värde == 5) Lägga_till_SMS('C');
        if (Typ_värde == 6) Lägga_till_Ord("Ljava/io/FileInputStream;");
        if (Typ_värde == 7) Lägga_till_Ord("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws deklaration. fel_31f743d2 Process_värde_post 본문은 värd javac를 사용한다.
    static void läsa_fel_namn() {
        boolean 한국어묶음 = TA_Ord("Svenska");
        if (한국어묶음) { krav_värde('.'); 말요구("eget"); krav_värde('.'); }
        if (!한국어묶음 && (TA_Ord("Exception") || TA_Ord("IOException"))) return;
        if (TA_Ord("fel_31f743d2") || TA_Ord("körning_fel") || TA_Ord("indata_utleverans_fel") || TA_Ord("vänta_TIMEOUT_fel") || TA_Ord("ADRESS_LETAUPP_fel") || TA_Ord("파일없음예외") || TA_Ord("kommunikation_fel") || TA_Ord("ogiltig_argument_fel") || TA_Ord("nummer_format_fel") || TA_Ord("범위예외") || TA_Ord("배열범위예외") || TA_Ord("문자열범위예외") || TA_Ord("null_referens_fel") || TA_Ord("산술예외") || TA_Ord("status_fel") || TA_Ord("Typ_Sänd_fel") || TA_Ord("음수배열크기예외") || TA_Ord("MATRIS_Store_fel") || TA_Ord("tråd_status_fel") || TA_Ord("대기중단예외")) return;
        fel_värde("unsupported throws type");
    }
    static void läsa_deklaration() {
        while (TA_Ord("import")) {
            if (Ord_värde(position, "Svenska")) läsa_fel_namn();
            else {
                말요구("java"); krav_värde('.'); 말요구("io"); krav_värde('.');
                if (!(TA_Ord("FileInputStream") || TA_Ord("FileOutputStream") || TA_Ord("IOException"))) fel_värde("unsupported import");
            }
            krav_värde(';');
        }
        TA_Ord("public"); TA_Ord("final"); 말요구("class"); Kurs_kod = identifierare_värde();
        Kurs_konstant = referens(7, kod_konstant(Kurs_kod), 0);
        överordnad_konstant = referens(7, Ord_konstant("java/lang/Object"), 0); KOD_konstant = Ord_konstant("Code"); krav_värde('{');
        while (!fel && variant_värde() != '}') {
            if (metod_ANTAL == 32) { fel_värde("too many methods"); break; }
            int ansluta_post = TA_Ord("public") ? 1 : TA_Ord("private") ? 2 : 0; 말요구("static");
            int FUNKTION_värde = metod_ANTAL++;
            metod_ansluta[FUNKTION_värde] = ansluta_post | 8;
            metod_Retur[FUNKTION_värde] = format_värde(); metod_post_namn[FUNKTION_värde] = identifierare_värde(); krav_värde('(');
            for (int framåtvänd_värde = 0; framåtvänd_värde < FUNKTION_värde; framåtvänd_värde++) if (이름같음(metod_post_namn[framåtvänd_värde], metod_post_namn[FUNKTION_värde])) fel_värde("duplicate method (overloading unsupported)");
            while (!fel && variant_värde() != ')') {
                int nummer = metod_argument_ANTAL[FUNKTION_värde];
                if (nummer == 16) { fel_värde("too many parameters"); break; }
                int Typ_värde = format_värde(); if (Typ_värde == 0) fel_värde("void parameter");
                metod_argument_Typ[FUNKTION_värde * 16 + nummer] = Typ_värde; metod_argument_namn[FUNKTION_värde * 16 + nummer] = identifierare_värde();
                metod_argument_ANTAL[FUNKTION_värde]++;
                if (!få(',')) break;
            }
            krav_värde(')');
            if (TA_Ord("throws")) {
                do { läsa_fel_namn(); } while (!fel && få(','));
            }
            metod_brödtext[FUNKTION_värde] = position; krav_värde('{');
            int kapsling_värde = 1;
            while (position < kod_ANTAL && kapsling_värde > 0) {
                if (variant_värde() == '{') kapsling_värde++;
                if (variant_värde() == '}') kapsling_värde--;
                position++;
            }
            if (kapsling_värde != 0) fel_värde("unclosed method body");
            metod_avsluta[FUNKTION_värde] = position;
            metod_namn_konstant[FUNKTION_värde] = kod_konstant(metod_post_namn[FUNKTION_värde]);
            tecken_längd = 0; Lägga_till_SMS('(');
            for (int nummer = 0; nummer < metod_argument_ANTAL[FUNKTION_värde]; nummer++) Lägg_till_format(metod_argument_Typ[FUNKTION_värde * 16 + nummer]);
            Lägga_till_SMS(')'); Lägg_till_format(metod_Retur[FUNKTION_värde]); 함수서술[FUNKTION_värde] = tecken_konstant();
        }
        krav_värde('}'); if (position != kod_ANTAL) fel_värde("extra input after class");
    }
    static int Sök_lokal(int Namn) {
        for (int nummer = lokal_ANTAL - 1; nummer >= 0; nummer--) if (지역깊이[nummer] >= 0 && 이름같음(lokal_namn[nummer], Namn)) return nummer;
        fel_värde("unknown variable"); return 0;
    }
    static int Lägg_till_lokal(int Namn, int Typ_värde) {
        for (int nummer = 0; nummer < lokal_ANTAL; nummer++) if (지역깊이[nummer] >= 0 && 이름같음(lokal_namn[nummer], Namn)) fel_värde("duplicate local variable");
        if (lokal_ANTAL == 128) { fel_värde("too many locals"); return 0; }
        lokal_namn[lokal_ANTAL] = Namn; lokal_Typ[lokal_ANTAL] = Typ_värde; 지역깊이[lokal_ANTAL] = 깊이;
        return lokal_ANTAL++;
    }
    static boolean heltal_Typ(int Typ_värde) { return Typ_värde == 1 || Typ_värde == 5; }
    static void läsa_lokal(int nummer) { 내보내기(lokal_Typ[nummer] <= 2 || lokal_Typ[nummer] == 5 ? 21 : 25); 내보내기(nummer); }
    static void skriva_lokal(int nummer) { 내보내기(lokal_Typ[nummer] <= 2 || lokal_Typ[nummer] == 5 ? 54 : 58); 내보내기(nummer); }
    static void verifiera_Typ(int verklig_data, int 기대) { if (verklig_data != 기대 && !(verklig_data == 5 && 기대 == 1)) fel_värde("type mismatch"); }
    static void läsa_tecken_värde(int kod_värde) {
        tecken_längd = 0; int Kör = kod_placera[kod_värde] + 1, 끝 = kod_placera[kod_värde] + kod_längd[kod_värde] - 1;
        while (Kör < 끝 && !fel) {
            int värde = källfil[Kör++];
            if (värde == '\\') {
                if (Kör == 끝) { fel_värde("invalid escape"); break; }
                värde = källfil[Kör++];
                if (värde == 'n') värde = 10;
                else if (värde == 'r') värde = 13;
                else if (värde == 't') värde = 9;
                else if (värde == 'b') värde = 8;
                else if (värde == 'f') värde = 12;
                else if (värde != '\\' && värde != '"' && värde != '\'') fel_värde("unsupported escape");
            }
            Lägga_till_SMS(värde);
        }
    }
    static int parsa_heltal(int kod_värde, boolean 음수) {
        if (kod_längd[kod_värde] > 1 && källfil[kod_placera[kod_värde]] == '0') fel_värde("octal literals unsupported");
        int värde = 0;
        for (int nummer = 0; nummer < kod_längd[kod_värde]; nummer++) {
            int siffra_objekt = källfil[kod_placera[kod_värde] + nummer] - '0';
            if (värde < -214748364 || värde == -214748364 && siffra_objekt > (음수 ? 8 : 7)) fel_värde("integer literal out of range");
            värde = värde * 10 - siffra_objekt;
        }
        return 음수 ? värde : -värde;
    }
    static int 기본식() {
        if (TA_Ord("new")) {
            int Typ_värde = format_värde();
            if (Typ_värde != 6 && Typ_värde != 7) { fel_värde("only file streams supported by new in source"); return 0; }
            String ägare_värde = Typ_värde == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            kommando(187, referens(7, Ord_konstant(ägare_värde), 0)); 내보내기(89);
            krav_värde('('); verifiera_Typ(uttryck_värde(), 3); boolean 이어 = false;
            if (få(',')) { if (Typ_värde != 7) fel_värde("input stream constructor arguments"); verifiera_Typ(uttryck_värde(), 2); 이어 = true; }
            krav_värde(')');
            kommando(183, extern_referens(10, ägare_värde, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return Typ_värde;
        }
        if (få('(')) { int Typ_värde = uttryck_värde(); krav_värde(')'); return Typ_värde; }
        if (variant_värde() == 257) { 수상수(parsa_heltal(position++, false)); return 1; }
        if (variant_värde() == 258) { läsa_tecken_värde(position++); kommando(19, referens(8, tecken_konstant(), 0)); return 3; }
        if (variant_värde() == 259) { läsa_tecken_värde(position++); if (tecken_längd != 1) fel_värde("character literal length"); 수상수(문자[0]); return 5; }
        if (TA_Ord("true")) { 내보내기(4); return 2; }
        if (TA_Ord("false")) { 내보내기(3); return 2; }
        if (TA_Ord("Svenska")) {
            krav_värde('.'); 말요구("eget"); krav_värde('.');
            String ägare_värde = "", metod_värde = "", 서술 = ""; int 가 = 0, SEKUND_operand = 0, 다 = 0, 라 = 0, 마 = 0, RESULTAT = 0;
            if (TA_Ord("utmatningsposition")) {
                ägare_värde = "Svenska/eget/utmatningsposition"; krav_värde('.');
                if (TA_Ord("skriva_rad")) { metod_värde = "skriva_rad"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TA_Ord("Skriv")) { metod_värde = "Skriv"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TA_Ord("skriva_nummer")) { metod_värde = "skriva_nummer"; 서술 = "(I)V"; 가 = 1; }
                else fel_värde("unknown Korean output method");
            } else if (TA_Ord("문자")) {
                ägare_värde = "Svenska/eget/문자"; krav_värde('.'); 가 = 3;
                if (TA_Ord("längd_värde")) { metod_värde = "längd_värde"; 서술 = "(Ljava/lang/String;)I"; RESULTAT = 1; }
                else if (TA_Ord("kodpunkt_ANTAL")) { metod_värde = "kodpunkt_ANTAL"; 서술 = "(Ljava/lang/String;)I"; RESULTAT = 1; }
                else if (TA_Ord("parsa_heltal")) { metod_värde = "parsa_heltal"; 서술 = "(Ljava/lang/String;)I"; RESULTAT = 1; }
                else if (TA_Ord("skriva_heltal_värde")) { metod_värde = "skriva_heltal_värde"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; RESULTAT = 3; }
                else if (TA_Ord("같음")) { metod_värde = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; SEKUND_operand = 3; RESULTAT = 2; }
                else if (TA_Ord("klistra_in_SMS")) { metod_värde = "klistra_in_SMS"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; SEKUND_operand = 3; RESULTAT = 3; }
                else if (TA_Ord("klippa_värde")) { metod_värde = "klippa_värde"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; SEKUND_operand = 1; 다 = 1; RESULTAT = 3; }
                else fel_värde("unknown Korean text method");
            } else if (TA_Ord("filnamn")) {
                ägare_värde = "Svenska/eget/filnamn"; krav_värde('.'); 가 = 3;
                if (TA_Ord("Läs")) { metod_värde = "Läs"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; RESULTAT = 3; }
                else if (TA_Ord("Skriv")) { metod_värde = "Skriv"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; SEKUND_operand = 3; }
                else fel_värde("unknown Korean file method");
            } else if (TA_Ord("skärmbild")) {
                ägare_värde = "Svenska/eget/skärmbild"; krav_värde('.');
                if (TA_Ord("너비")) { metod_värde = "너비"; 서술 = "()I"; RESULTAT = 1; }
                else if (TA_Ord("높이")) { metod_värde = "높이"; 서술 = "()I"; RESULTAT = 1; }
                else if (TA_Ord("rektangel")) { metod_värde = "rektangel"; 서술 = "(IIIII)V"; 가 = 1; SEKUND_operand = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (TA_Ord("radera_post")) { metod_värde = "radera_post"; 서술 = "(I)V"; 가 = 1; }
                else if (TA_Ord("기다리기")) { metod_värde = "기다리기"; 서술 = "()V"; }
                else fel_värde("unknown Korean framebuffer method");
            } else fel_värde("unsupported Korean library class");
            krav_värde('('); if (가 != 0) verifiera_Typ(uttryck_värde(), 가);
            if (SEKUND_operand != 0) { krav_värde(','); verifiera_Typ(uttryck_värde(), SEKUND_operand); }
            if (다 != 0) { krav_värde(','); verifiera_Typ(uttryck_värde(), 다); }
            if (라 != 0) { krav_värde(','); verifiera_Typ(uttryck_värde(), 라); }
            if (마 != 0) { krav_värde(','); verifiera_Typ(uttryck_värde(), 마); }
            krav_värde(')'); kommando(184, extern_referens(10, ägare_värde, metod_värde, 서술)); return RESULTAT;
        }
        if (TA_Ord("Integer")) {
            krav_värde('.'); 말요구("parseInt"); krav_värde('('); verifiera_Typ(uttryck_värde(), 3); krav_värde(')');
            kommando(184, extern_referens(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Namn = identifierare_värde();
        if (få('(')) {
            int FUNKTION_värde = -1;
            for (int nummer = 0; nummer < metod_ANTAL; nummer++) if (이름같음(Namn, metod_post_namn[nummer])) FUNKTION_värde = nummer;
            if (FUNKTION_värde < 0) { fel_värde("unknown static method"); return 0; }
            int nummer = 0;
            while (!fel && variant_värde() != ')') {
                if (nummer >= metod_argument_ANTAL[FUNKTION_värde]) { fel_värde("too many arguments"); break; }
                verifiera_Typ(uttryck_värde(), metod_argument_Typ[FUNKTION_värde * 16 + nummer++]); if (!få(',')) break;
            }
            krav_värde(')'); if (nummer != metod_argument_ANTAL[FUNKTION_värde]) fel_värde("argument count mismatch");
            kommando(184, referens(10, Kurs_konstant, referens(12, metod_namn_konstant[FUNKTION_värde], 함수서술[FUNKTION_värde])));
            return metod_Retur[FUNKTION_värde];
        }
        int lokal_scope = Sök_lokal(Namn), Typ_värde = lokal_Typ[lokal_scope]; läsa_lokal(lokal_scope);
        while (!fel) {
            if (få('[')) { verifiera_Typ(Typ_värde, 4); verifiera_Typ(uttryck_värde(), 1); krav_värde(']'); 내보내기(50); Typ_värde = 3; }
            else if (få('.')) {
                if (Typ_värde == 6 || Typ_värde == 7) {
                    String ägare_värde = Typ_värde == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (TA_Ord("close")) { krav_värde('('); krav_värde(')'); kommando(182, extern_referens(10, ägare_värde, "close", "()V")); Typ_värde = 0; }
                    else if (Typ_värde == 6 && TA_Ord("read")) { krav_värde('('); krav_värde(')'); kommando(182, extern_referens(10, ägare_värde, "read", "()I")); Typ_värde = 1; }
                    else if (Typ_värde == 7 && TA_Ord("write")) { krav_värde('('); verifiera_Typ(uttryck_värde(), 1); krav_värde(')'); kommando(182, extern_referens(10, ägare_värde, "write", "(I)V")); Typ_värde = 0; }
                    else { fel_värde("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (Typ_värde == 4) { 내보내기(190); Typ_värde = 1; }
                else { verifiera_Typ(Typ_värde, 3); krav_värde('('); krav_värde(')'); kommando(182, extern_referens(10, "java/lang/String", "length", "()I")); Typ_värde = 1; }
            } else break;
        }
        return Typ_värde;
    }
    static int 단항() {
        if (++식깊이 > 64) { fel_värde("expression nesting too deep"); 식깊이--; return 0; }
        int Typ_värde;
        if (få('!')) { verifiera_Typ(단항(), 2); Jämförelse_värde(153); Typ_värde = 2; }
        else if (få('-')) {
            if (variant_värde() == 257) 수상수(parsa_heltal(position++, true));
            else { verifiera_Typ(단항(), 1); 내보내기(116); }
            Typ_värde = 1;
        } else if (få('+')) { verifiera_Typ(단항(), 1); Typ_värde = 1; }
        else Typ_värde = 기본식();
        식깊이--; return Typ_värde;
    }
    static int 곱식() {
        int Typ_värde = 단항();
        while (!fel && (variant_värde() == '*' || variant_värde() == '/' || variant_värde() == '%')) {
            int kodning_värde = variant_värde(); position++; verifiera_Typ(Typ_värde, 1); verifiera_Typ(단항(), 1);
            내보내기(kodning_värde == '*' ? 104 : kodning_värde == '/' ? 108 : 112); Typ_värde = 1;
        }
        return Typ_värde;
    }
    static int 합식() {
        int Typ_värde = 곱식();
        while (!fel && (variant_värde() == '+' || variant_värde() == '-')) {
            int kodning_värde = variant_värde(); position++; int gräns_värde = KOD_storlek, BACK_värdetyp = 곱식();
            if (kodning_värde == '+' && (Typ_värde == 3 || BACK_värdetyp == 3)) { 결합(gräns_värde, Typ_värde, BACK_värdetyp); Typ_värde = 3; }
            else { verifiera_Typ(Typ_värde, 1); verifiera_Typ(BACK_värdetyp, 1); 내보내기(kodning_värde == '+' ? 96 : 100); Typ_värde = 1; }
        }
        return Typ_värde;
    }
    static int ansluten_referens(int Typ_värde) {
        if (Typ_värde != 1 && Typ_värde != 2 && Typ_värde != 3 && Typ_värde != 5) fel_värde("unsupported concatenation type");
        return extern_referens(10, "java/lang/StringBuilder", "append", Typ_värde == 1 ? "(I)Ljava/lang/StringBuilder;"
            : Typ_värde == 2 ? "(Z)Ljava/lang/StringBuilder;" : Typ_värde == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int gräns_värde, int framåtvänd_värdetyp, int BACK_värdetyp) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 HÖGER KOD_värde 앞에 generera 코드를 삽입한다.
        // HÖGER uttryck_värde 내부의 peer_värde gren 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = KOD_storlek;
        kommando(187, referens(7, Ord_konstant("java/lang/StringBuilder"), 0)); 내보내기(89);
        kommando(183, extern_referens(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); kommando(182, ansluten_referens(framåtvänd_värdetyp));
        if (fel) return;
        int längd_värde = KOD_storlek - 끝;
        for (int nummer = 0; nummer < längd_värde; nummer++) 삽입코드[nummer] = KOD_värde[끝 + nummer];
        for (int nummer = 끝 - 1; nummer >= gräns_värde; nummer--) KOD_värde[nummer + längd_värde] = KOD_värde[nummer];
        for (int nummer = 0; nummer < längd_värde; nummer++) KOD_värde[gräns_värde + nummer] = 삽입코드[nummer];
        kommando(182, ansluten_referens(BACK_värdetyp)); kommando(182, extern_referens(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int Jämförelse_uttryck() {
        int Typ_värde = 합식();
        while (!fel && (variant_värde() == '<' || variant_värde() == '>' || variant_värde() == 302 || variant_värde() == 303)) {
            int kodning_värde = variant_värde(); position++; verifiera_Typ(Typ_värde, 1); verifiera_Typ(합식(), 1);
            Jämförelse_värde(kodning_värde == '<' ? 161 : kodning_värde == '>' ? 163 : kodning_värde == 302 ? 164 : 162); Typ_värde = 2;
        }
        return Typ_värde;
    }
    static int 동등식() {
        int Typ_värde = Jämförelse_uttryck();
        while (!fel && (variant_värde() == 300 || variant_värde() == 301)) {
            int kodning_värde = variant_värde(); position++; int BACK_värdetyp = Jämförelse_uttryck();
            if (Typ_värde == 0 || BACK_värdetyp == 0) fel_värde("void expression");
            if (!(heltal_Typ(Typ_värde) && heltal_Typ(BACK_värdetyp))) verifiera_Typ(BACK_värdetyp, Typ_värde);
            Jämförelse_värde((Typ_värde <= 2 || Typ_värde == 5 ? 159 : 165) + (kodning_värde == 301 ? 1 : 0)); Typ_värde = 2;
        }
        return Typ_värde;
    }
    static int AND() {
        int Typ_värde = 동등식();
        while (!fel && få(304)) {
            verifiera_Typ(Typ_värde, 2); int 가 = gren(153); verifiera_Typ(동등식(), 2); int SEKUND_operand = gren(153);
            내보내기(4); int 끝 = gren(167); Länk_värde(가, KOD_storlek); Länk_värde(SEKUND_operand, KOD_storlek); 내보내기(3); Länk_värde(끝, KOD_storlek); Typ_värde = 2;
        }
        return Typ_värde;
    }
    static int uttryck_värde() {
        int Typ_värde = AND();
        while (!fel && få(305)) {
            verifiera_Typ(Typ_värde, 2); int 가 = gren(154); verifiera_Typ(AND(), 2); int SEKUND_operand = gren(154);
            내보내기(3); int 끝 = gren(167); Länk_värde(가, KOD_storlek); Länk_värde(SEKUND_operand, KOD_storlek); 내보내기(4); Länk_värde(끝, KOD_storlek); Typ_värde = 2;
        }
        return Typ_värde;
    }
    static void uppgift_värde(boolean Tillåt_deklaration) {
        if (Ord_värde(position, "int") || Ord_värde(position, "boolean") || Ord_värde(position, "String") || Ord_värde(position, "char")
            || Ord_värde(position, "FileInputStream") || Ord_värde(position, "FileOutputStream")) {
            if (!Tillåt_deklaration) fel_värde("declaration not allowed here");
            int Typ_värde = format_värde(), Namn = identifierare_värde(); krav_värde('='); verifiera_Typ(uttryck_värde(), Typ_värde);
            skriva_lokal(Lägg_till_lokal(Namn, Typ_värde)); return;
        }
        int Namn = identifierare_värde(), lokal_scope = Sök_lokal(Namn);
        if (få('=')) { verifiera_Typ(uttryck_värde(), lokal_Typ[lokal_scope]); skriva_lokal(lokal_scope); }
        else if (variant_värde() >= 308 && variant_värde() <= 312) {
            int kodning_värde = variant_värde(); position++; läsa_lokal(lokal_scope); int gräns_värde = KOD_storlek, BACK_värdetyp = uttryck_värde();
            if (kodning_värde == 308 && lokal_Typ[lokal_scope] == 3) 결합(gräns_värde, 3, BACK_värdetyp);
            else {
                verifiera_Typ(lokal_Typ[lokal_scope], 1); verifiera_Typ(BACK_värdetyp, 1);
                내보내기(kodning_värde == 308 ? 96 : kodning_värde == 309 ? 100 : kodning_värde == 310 ? 104 : kodning_värde == 311 ? 108 : 112);
                if (lokal_Typ[lokal_scope] == 5) 내보내기(146);
            }
            skriva_lokal(lokal_scope);
        }
        else if (variant_värde() == 306 || variant_värde() == 307) {
            verifiera_Typ(lokal_Typ[lokal_scope], 1); 내보내기(132); 내보내기(lokal_scope); 내보내기(variant_värde() == 306 ? 1 : 255); position++;
            if (lokal_Typ[lokal_scope] == 5) { läsa_lokal(lokal_scope); 내보내기(146); skriva_lokal(lokal_scope); }
        } else fel_värde("assignment or postfix increment required");
    }
    static void skärmbild_utleverans() {
        말요구("System"); krav_värde('.'); 말요구("out"); krav_värde('.');
        boolean 줄바꿈 = TA_Ord("println"); if (!줄바꿈) 말요구("print"); krav_värde('(');
        kommando(178, extern_referens(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean 빈인수 = variant_värde() == ')';
        int Typ_värde = 빈인수 ? 0 : uttryck_värde(); krav_värde(')'); krav_värde(';');
        String 서술 = Typ_värde == 0 ? "()V" : Typ_värde == 1 ? "(I)V" : Typ_värde == 2 ? "(Z)V" : Typ_värde == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (Typ_värde == 4 || Typ_värde >= 6 || Typ_värde == 0 && (!줄바꿈 || !빈인수)) fel_värde("unsupported print argument");
        kommando(182, extern_referens(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean utdrag_värde() {
        if (fel) return false;
        if (깊이 > 32) { fel_värde("statement nesting too deep"); return false; }
        if (få('{')) {
            깊이++; boolean Retur_KR = false;
            while (!fel && variant_värde() != '}') { if (Retur_KR) fel_värde("unreachable statement"); Retur_KR = utdrag_värde(); }
            krav_värde('}'); for (int nummer = 0; nummer < lokal_ANTAL; nummer++) if (지역깊이[nummer] == 깊이) 지역깊이[nummer] = -1;
            깊이--; return Retur_KR;
        }
        if (få(';')) return false;
        if (TA_Ord("return")) {
            int Typ_värde = variant_värde() == ';' ? 0 : uttryck_värde(); verifiera_Typ(Typ_värde, metod_Retur[aktuellt_metod]); krav_värde(';');
            내보내기(Typ_värde == 0 ? 177 : Typ_värde <= 2 || Typ_värde == 5 ? 172 : 176); return true;
        }
        if (TA_Ord("if")) {
            krav_värde('('); verifiera_Typ(uttryck_värde(), 2); krav_värde(')'); int FALSKT_värde = gren(153);
            깊이++; boolean 가 = kontroll_utdrag(); 깊이--;
            if (TA_Ord("else")) { int 끝 = gren(167); Länk_värde(FALSKT_värde, KOD_storlek); 깊이++; boolean SEKUND_operand = kontroll_utdrag(); 깊이--; Länk_värde(끝, KOD_storlek); return 가 && SEKUND_operand; }
            Länk_värde(FALSKT_värde, KOD_storlek); return false;
        }
        if (TA_Ord("while")) {
            int Kör = KOD_storlek; krav_värde('('); verifiera_Typ(uttryck_värde(), 2); krav_värde(')'); int 끝 = gren(153);
            깊이++; kontroll_utdrag(); 깊이--; Länk_värde(gren(167), Kör); Länk_värde(끝, KOD_storlek); return false;
        }
        if (TA_Ord("for")) {
            깊이++; krav_värde('('); if (variant_värde() != ';') uppgift_värde(true); krav_värde(';');
            int villkor = KOD_storlek; if (variant_värde() == ';') 내보내기(4); else verifiera_Typ(uttryck_värde(), 2); krav_värde(';');
            int 끝 = gren(153), brödtext = gren(167), uppdatera = KOD_storlek;
            if (variant_värde() != ')') uppgift_värde(false); krav_värde(')'); Länk_värde(gren(167), villkor); Länk_värde(brödtext, KOD_storlek);
            kontroll_utdrag(); Länk_värde(gren(167), uppdatera); Länk_värde(끝, KOD_storlek);
            for (int nummer = 0; nummer < lokal_ANTAL; nummer++) if (지역깊이[nummer] == 깊이) 지역깊이[nummer] = -1;
            깊이--; return false;
        }
        if (Ord_värde(position, "System")) { skärmbild_utleverans(); return false; }
        if (variant_värde() == 256 && position + 1 < kod_ANTAL && (kod_variant[position + 1] == '(' || kod_variant[position + 1] == '.')) {
            int Typ_värde = uttryck_värde(); if (Typ_värde != 0) 내보내기(87); krav_värde(';'); return false;
        }
        uppgift_värde(true); krav_värde(';'); return false;
    }
    static boolean kontroll_utdrag() {
        if (Ord_värde(position, "int") || Ord_värde(position, "boolean") || Ord_värde(position, "char") || Ord_värde(position, "String")
            || Ord_värde(position, "FileInputStream") || Ord_värde(position, "FileOutputStream")) fel_värde("local declaration requires braces");
        return utdrag_värde();
    }
    static void 출바(int värde) { if (utleverans_storlek == utmatningsposition.length) fel_värde("class file too large"); else utmatningsposition[utleverans_storlek++] = värde & 255; }
    static void 출짧(int värde) { 출바(värde >> 8); 출바(värde); }
    static void 출정(int värde) { 출짧(värde >>> 16); 출짧(värde); }
    static void skriva_Kurs() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(konstant_ANTAL);
        for (int nummer = 0; nummer < konstant_storlek; nummer++) 출바(konstant_värde[nummer]);
        출짧(0x21); 출짧(Kurs_konstant); 출짧(överordnad_konstant); 출짧(0); 출짧(0); 출짧(metod_ANTAL);
        for (int nummer = 0; nummer < metod_ANTAL; nummer++) {
            출짧(metod_ansluta[nummer]); 출짧(metod_namn_konstant[nummer]); 출짧(함수서술[nummer]); 출짧(1); 출짧(KOD_konstant);
            출정(12 + metod_längd[nummer]); 출짧(128); 출짧(함수지역[nummer]); 출정(metod_längd[nummer]);
            for (int fack_post = 0; fack_post < metod_längd[nummer]; fack_post++) 출바(KOD_värde[metod_KOD[nummer] + fack_post]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int Kör() {
        if (användarutrymme.인수개수() == 1 && 자바도구.같음(användarutrymme.argument(0), "-version")) {
            användarutrymme.Skriv("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (användarutrymme.인수개수() != 1) { användarutrymme.Skriv("Usage: javac FILE.java\n"); return 2; }
        int namn_storlek = 자바도구.Namn(filnamn_SMS, användarutrymme.argument(0));
        if (namn_storlek < 6 || namn_storlek > 62 || filnamn_SMS[namn_storlek - 5] != '.' || filnamn_SMS[namn_storlek - 4] != 'j'
            || filnamn_SMS[namn_storlek - 3] != 'a' || filnamn_SMS[namn_storlek - 2] != 'v' || filnamn_SMS[namn_storlek - 1] != 'a') {
            användarutrymme.Skriv("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        källa_storlek = användarutrymme.läsa_fil(filnamn_SMS, källfil);
        if (källa_storlek < 0) { användarutrymme.Skriv("javac: cannot read source: "); 자바도구.skriva_nummer(källa_storlek); användarutrymme.skriva_tecken_värde(10); return 1; }
        källa_storlek = 자바도구.원문해독(källfil, källa_storlek);
        if (källa_storlek < 0) { användarutrymme.Skriv("javac error: invalid UTF-8 source\n"); return 1; }
        klippa_värde(); if (!fel) läsa_deklaration();
        if (!fel) {
            if (kod_längd[Kurs_kod] != namn_storlek - 5) fel_värde("class name must match file name");
            for (int nummer = 0; nummer < namn_storlek - 5; nummer++) if (källfil[kod_placera[Kurs_kod] + nummer] != filnamn_SMS[nummer]) fel_värde("class name must match file name");
        }
        for (aktuellt_metod = 0; aktuellt_metod < metod_ANTAL && !fel; aktuellt_metod++) {
            position = metod_brödtext[aktuellt_metod]; metod_KOD[aktuellt_metod] = KOD_storlek; lokal_ANTAL = 0; 깊이 = 0;
            for (int nummer = 0; nummer < metod_argument_ANTAL[aktuellt_metod]; nummer++) Lägg_till_lokal(metod_argument_namn[aktuellt_metod * 16 + nummer], metod_argument_Typ[aktuellt_metod * 16 + nummer]);
            boolean Retur_KR = utdrag_värde();
            if (!Retur_KR && metod_Retur[aktuellt_metod] != 0) fel_värde("missing return");
            // gren 뒤의 합류 지점은 반드시 verklig_data 명령이어야 한다 (버전 49 검증기).
            if (metod_Retur[aktuellt_metod] == 0) 내보내기(177);
            else { boolean heltal = metod_Retur[aktuellt_metod] <= 2 || metod_Retur[aktuellt_metod] == 5; 내보내기(heltal ? 3 : 1); 내보내기(heltal ? 172 : 176); }
            if (position != metod_avsluta[aktuellt_metod]) fel_värde("invalid method body");
            함수지역[aktuellt_metod] = lokal_ANTAL; metod_längd[aktuellt_metod] = KOD_storlek - metod_KOD[aktuellt_metod];
        }
        if (fel) return 1;
        skriva_Kurs(); if (fel) return 1;
        filnamn_SMS[namn_storlek - 4] = 'c'; filnamn_SMS[namn_storlek - 3] = 'l'; filnamn_SMS[namn_storlek - 2] = 'a';
        filnamn_SMS[namn_storlek - 1] = 's'; filnamn_SMS[namn_storlek] = 's'; filnamn_SMS[namn_storlek + 1] = 0;
        int RESULTAT = användarutrymme.skriva_fil(filnamn_SMS, utmatningsposition, utleverans_storlek);
        if (RESULTAT < 0) { användarutrymme.Skriv("javac: cannot save class: "); 자바도구.skriva_nummer(RESULTAT); användarutrymme.skriva_tecken_värde(10); return 1; }
        användarutrymme.Skriv("Compiled: "); for (int nummer = 0; filnamn_SMS[nummer] != 0; nummer++) användarutrymme.skriva_tecken_värde(filnamn_SMS[nummer]);
        användarutrymme.Skriv(" (JVM class version 49)\n"); return 0;
    }
}
