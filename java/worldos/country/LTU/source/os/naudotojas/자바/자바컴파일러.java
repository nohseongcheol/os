// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java šaltinis_medis -> 표준 버전 49 class kompiliatorius. */
public final class 자바컴파일러 {
    static int[] ŠALTINIS = new int[16384], Išvestis = new int[16384], CODE_VALUE = new int[4096];
    static int[] 토큰종류 = new int[2048], žetonas_padėtis = new int[2048], 토큰길이 = new int[2048];
    static int[] konstanta_VALUE = new int[4096], konstanta_OFFSET = new int[512];
    static int[] 문자 = new int[512], failo_vardas_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int šaltinis_dydis, žetonas_COUNT, Pozicija, CODE_dydis, konstanta_dydis, konstanta_COUNT = 1, išeiga_dydis, 문자수;
    static boolean KLAIDA;
    static int klasė_žetonas, klasė_konstanta, pirminis_konstanta, CODE_konstanta;
    static int[] metodas_įrašas_pavadinimas = new int[32], metodas_grąžinti = new int[32], metodas_argumentas_COUNT = new int[32];
    static int[] metodas_argumentas_pavadinimas = new int[512], metodas_argumentas_TYPE = new int[512];
    static int[] metodas_pranešimo_tekstas = new int[32], metodas_baigti_pokalbį = new int[32], metodas_CODE = new int[32];
    static int[] 함수길이 = new int[32], 함수지역 = new int[32], metodas_pavadinimas_konstanta = new int[32], 함수서술 = new int[32];
    static int[] metodas_prieiga = new int[32];
    static int metodas_COUNT, dabartinis_metodas, vietinis_COUNT, 깊이, 식깊이;
    static int[] vietinis_pavadinimas = new int[128], vietinis_TYPE = new int[128], 지역깊이 = new int[128];

    static void triktis_VALUE(String 이유) {
        if (!KLAIDA) {
            naudotojas.Rašymas("javac error: "); naudotojas.Rašymas(이유);
            naudotojas.Rašymas(" at line ");
            int Eilutė = 1, 끝 = Pozicija < žetonas_COUNT ? žetonas_padėtis[Pozicija] : šaltinis_dydis;
            for (int numeris = 0; numeris < 끝; numeris++) if (ŠALTINIS[numeris] == 10) Eilutė++;
            자바도구.rašymas_numeris(Eilutė); naudotojas.rašymas_simbolis_VALUE(10);
        }
        KLAIDA = true;
    }
    static boolean simbolis_VALUE_068c2631(int VALUE) { return 문자이름규칙.첫글자(VALUE); }
    static boolean skaitmuo_VALUE(int VALUE) { return VALUE >= '0' && VALUE <= '9'; }
    static boolean 이름같음(int 가, int SECOND_operandas) {
        if (가 < 0 || SECOND_operandas < 0 || 가 >= žetonas_COUNT || SECOND_operandas >= žetonas_COUNT || 토큰길이[가] != 토큰길이[SECOND_operandas]) return false;
        for (int numeris = 0; numeris < 토큰길이[가]; numeris++) if (ŠALTINIS[žetonas_padėtis[가] + numeris] != ŠALTINIS[žetonas_padėtis[SECOND_operandas] + numeris]) return false;
        return true;
    }
    static boolean Word_VALUE(int žetonas_VALUE, String Word_SMS) {
        if (žetonas_VALUE < 0 || žetonas_VALUE >= žetonas_COUNT || 토큰길이[žetonas_VALUE] != Word_SMS.length()) return false;
        for (int numeris = 0; numeris < Word_SMS.length(); numeris++) if (ŠALTINIS[žetonas_padėtis[žetonas_VALUE] + numeris] != Word_SMS.charAt(numeris)) return false;
        return true;
    }
    static int 종류() { return Pozicija < žetonas_COUNT ? 토큰종류[Pozicija] : 0; }
    static boolean gauti(int VALUE) { if (종류() != VALUE) return false; Pozicija++; return true; }
    static void reikalavimas_VALUE(int VALUE) { if (!gauti(VALUE)) triktis_VALUE("unexpected token"); }
    static boolean TAKE_Word(String Word_SMS) { if (!Word_VALUE(Pozicija, Word_SMS)) return false; Pozicija++; return true; }
    static void 말요구(String Word_SMS) { if (!TAKE_Word(Word_SMS)) triktis_VALUE(Word_SMS); }
    static int identifikatorius_VALUE() {
        int REZULTATAS = Pozicija;
        if (종류() != 256) triktis_VALUE("identifier required"); else Pozicija++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int Paleisti = 0;
        for (int numeris = 0; numeris <= 예약어.length(); numeris++) {
            if (numeris == 예약어.length() || 예약어.charAt(numeris) == ' ') {
                boolean 같음 = numeris - Paleisti == 토큰길이[REZULTATAS];
                for (int 칸 = Paleisti; 같음 && 칸 < numeris; 칸++) if (예약어.charAt(칸) != ŠALTINIS[žetonas_padėtis[REZULTATAS] + 칸 - Paleisti]) 같음 = false;
                if (같음) triktis_VALUE("reserved word cannot be an identifier");
                Paleisti = numeris + 1;
            }
        }
        return REZULTATAS;
    }
    static void kirpti_VALUE() {
        int numeris = 0;
        while (numeris < šaltinis_dydis && !KLAIDA) {
            int VALUE = ŠALTINIS[numeris], Paleisti = numeris, 종류 = VALUE;
            if (VALUE == 32 || VALUE == 9 || VALUE == 10 || VALUE == 13) { numeris++; continue; }
            if (VALUE == '/' && numeris + 1 < šaltinis_dydis && ŠALTINIS[numeris + 1] == '/') {
                while (numeris < šaltinis_dydis && ŠALTINIS[numeris] != 10) numeris++;
                continue;
            }
            if (VALUE == '/' && numeris + 1 < šaltinis_dydis && ŠALTINIS[numeris + 1] == '*') {
                numeris += 2;
                while (numeris + 1 < šaltinis_dydis && !(ŠALTINIS[numeris] == '*' && ŠALTINIS[numeris + 1] == '/')) numeris++;
                if (numeris + 1 >= šaltinis_dydis) { triktis_VALUE("unterminated comment"); break; }
                numeris += 2; continue;
            }
            if (simbolis_VALUE_068c2631(VALUE)) { 종류 = 256; while (numeris < šaltinis_dydis && 문자이름규칙.이어진글자(ŠALTINIS[numeris])) numeris++; }
            else if (skaitmuo_VALUE(VALUE)) { 종류 = 257; while (numeris < šaltinis_dydis && skaitmuo_VALUE(ŠALTINIS[numeris])) numeris++; }
            else if (VALUE == '"' || VALUE == '\'') {
                종류 = VALUE == '"' ? 258 : 259; numeris++;
                while (numeris < šaltinis_dydis && ŠALTINIS[numeris] != VALUE && ŠALTINIS[numeris] != 10 && ŠALTINIS[numeris] != 13) {
                    if (ŠALTINIS[numeris] == '\\') numeris++;
                    numeris++;
                }
                if (numeris >= šaltinis_dydis || ŠALTINIS[numeris] != VALUE) { triktis_VALUE("unterminated literal"); break; }
                numeris++;
            } else {
                numeris++;
                if (numeris < šaltinis_dydis) {
                    int toliau_prekė = ŠALTINIS[numeris];
                    if (VALUE == '=' && toliau_prekė == '=') 종류 = 300;
                    if (VALUE == '!' && toliau_prekė == '=') 종류 = 301;
                    if (VALUE == '<' && toliau_prekė == '=') 종류 = 302;
                    if (VALUE == '>' && toliau_prekė == '=') 종류 = 303;
                    if (VALUE == '&' && toliau_prekė == '&') 종류 = 304;
                    if (VALUE == '|' && toliau_prekė == '|') 종류 = 305;
                    if (VALUE == '+' && toliau_prekė == '+') 종류 = 306;
                    if (VALUE == '-' && toliau_prekė == '-') 종류 = 307;
                    if (VALUE == '+' && toliau_prekė == '=') 종류 = 308;
                    if (VALUE == '-' && toliau_prekė == '=') 종류 = 309;
                    if (VALUE == '*' && toliau_prekė == '=') 종류 = 310;
                    if (VALUE == '/' && toliau_prekė == '=') 종류 = 311;
                    if (VALUE == '%' && toliau_prekė == '=') 종류 = 312;
                    if (종류 >= 300) numeris++;
                }
            }
            if (žetonas_COUNT == 토큰종류.length - 1) { triktis_VALUE("too many tokens (2047 maximum)"); break; }
            토큰종류[žetonas_COUNT] = 종류; žetonas_padėtis[žetonas_COUNT] = Paleisti; 토큰길이[žetonas_COUNT++] = numeris - Paleisti;
        }
    }
    static void rašymas_konstanta_baitas(int VALUE) {
        if (konstanta_dydis == konstanta_VALUE.length) { triktis_VALUE("constant pool too large"); return; }
        konstanta_VALUE[konstanta_dydis++] = VALUE & 255;
    }
    static void 상짧(int VALUE) { rašymas_konstanta_baitas(VALUE >> 8); rašymas_konstanta_baitas(VALUE); }
    static int registras_konstanta(int Paleisti) {
        for (int numeris = 1; numeris < konstanta_COUNT; numeris++) {
            int priekinis_VALUE = konstanta_OFFSET[numeris], 길이 = (numeris + 1 < konstanta_COUNT ? konstanta_OFFSET[numeris + 1] : Paleisti) - priekinis_VALUE;
            if (길이 != konstanta_dydis - Paleisti) continue;
            boolean 같음 = true;
            for (int 칸 = 0; 칸 < 길이; 칸++) if (konstanta_VALUE[priekinis_VALUE + 칸] != konstanta_VALUE[Paleisti + 칸]) 같음 = false;
            if (같음) { konstanta_dydis = Paleisti; return numeris; }
        }
        if (konstanta_COUNT == konstanta_OFFSET.length) { triktis_VALUE("too many constants"); return 0; }
        konstanta_OFFSET[konstanta_COUNT] = Paleisti;
        return konstanta_COUNT++;
    }
    static void sujungti_SMS(int VALUE) {
        if (문자수 == 문자.length) { triktis_VALUE("text too long"); return; }
        문자[문자수++] = VALUE;
    }
    static void sujungti_Word(String Word_SMS) { for (int numeris = 0; numeris < Word_SMS.length(); numeris++) sujungti_SMS(Word_SMS.charAt(numeris)); }
    static int simbolis_konstanta() {
        int Paleisti = konstanta_dydis; rašymas_konstanta_baitas(1); 상짧(0);
        for (int numeris = 0; numeris < 문자수; numeris++) {
            int VALUE = 문자[numeris];
            if (VALUE > 0 && VALUE < 128) rašymas_konstanta_baitas(VALUE);
            else if (VALUE < 2048) { rašymas_konstanta_baitas(192 | VALUE >> 6); rašymas_konstanta_baitas(128 | VALUE & 63); }
            else { rašymas_konstanta_baitas(224 | VALUE >> 12); rašymas_konstanta_baitas(128 | VALUE >> 6 & 63); rašymas_konstanta_baitas(128 | VALUE & 63); }
        }
        if (KLAIDA) return 0;
        int 길이 = konstanta_dydis - Paleisti - 3;
        konstanta_VALUE[Paleisti + 1] = 길이 >> 8; konstanta_VALUE[Paleisti + 2] = 길이 & 255;
        return registras_konstanta(Paleisti);
    }
    static int Word_konstanta(String Word_SMS) { 문자수 = 0; sujungti_Word(Word_SMS); return simbolis_konstanta(); }
    static int žetonas_konstanta(int žetonas_VALUE) {
        문자수 = 0;
        for (int numeris = 0; numeris < 토큰길이[žetonas_VALUE]; numeris++) sujungti_SMS(ŠALTINIS[žetonas_padėtis[žetonas_VALUE] + numeris]);
        return simbolis_konstanta();
    }
    static int nuoroda(int 종류, int 가, int SECOND_operandas) {
        int Paleisti = konstanta_dydis; rašymas_konstanta_baitas(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(SECOND_operandas);
        return registras_konstanta(Paleisti);
    }
    static int išorinis_nuoroda(int 종류, String savininkas_VALUE, String Pavadinimas_2, String aprašas_VALUE) {
        int savininkas_identifikatorius = nuoroda(7, Word_konstanta(savininkas_VALUE), 0);
        int pavadinimas_COUNT = Word_konstanta(Pavadinimas_2), formatas_COUNT = Word_konstanta(aprašas_VALUE);
        return nuoroda(종류, savininkas_identifikatorius, nuoroda(12, pavadinimas_COUNT, formatas_COUNT));
    }
    static void 내보내기(int VALUE) {
        if (CODE_dydis == CODE_VALUE.length) { triktis_VALUE("bytecode too large"); return; }
        CODE_VALUE[CODE_dydis++] = VALUE & 255;
    }
    static void Komanda(int VALUE, int Argumentai) { 내보내기(VALUE); 내보내기(Argumentai >> 8); 내보내기(Argumentai); }
    static void 수상수(int VALUE) {
        if (VALUE >= -1 && VALUE <= 5) { 내보내기(VALUE + 3); return; }
        int Paleisti = konstanta_dydis; rašymas_konstanta_baitas(3); 상짧(VALUE >>> 16); 상짧(VALUE);
        Komanda(19, registras_konstanta(Paleisti));
    }
    static int šaka(int Komanda) { int REZULTATAS = CODE_dydis; Komanda(Komanda, 0); return REZULTATAS; }
    static void sieti_VALUE(int šaka, int tikslas_objektas) {
        if (KLAIDA) return;
        int 거리 = tikslas_objektas - šaka;
        if (거리 < -32768 || 거리 > 32767 || šaka < 0 || šaka + 2 >= CODE_dydis) { triktis_VALUE("invalid branch"); return; }
        CODE_VALUE[šaka + 1] = 거리 >> 8 & 255; CODE_VALUE[šaka + 2] = 거리 & 255;
    }
    static void Palyginimas_VALUE(int Komanda) {
        int TRUE_VALUE = šaka(Komanda); 내보내기(3); int 끝 = šaka(167);
        sieti_VALUE(TRUE_VALUE, CODE_dydis); 내보내기(4); sieti_VALUE(끝, CODE_dydis);
    }
    static int formatas_VALUE() {
        if (TAKE_Word("void")) return 0;
        if (TAKE_Word("int")) return 1;
        if (TAKE_Word("boolean")) return 2;
        if (TAKE_Word("char")) return 5;
        if (TAKE_Word("FileInputStream")) return 6;
        if (TAKE_Word("FileOutputStream")) return 7;
        if (TAKE_Word("String")) { if (gauti('[')) { reikalavimas_VALUE(']'); return 4; } return 3; }
        triktis_VALUE("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void Įtraukti_formatas(int TYPE_VALUE) {
        if (TYPE_VALUE == 0) sujungti_SMS('V');
        if (TYPE_VALUE == 1) sujungti_SMS('I');
        if (TYPE_VALUE == 2) sujungti_SMS('Z');
        if (TYPE_VALUE == 3) sujungti_Word("Ljava/lang/String;");
        if (TYPE_VALUE == 4) sujungti_Word("[Ljava/lang/String;");
        if (TYPE_VALUE == 5) sujungti_SMS('C');
        if (TYPE_VALUE == 6) sujungti_Word("Ljava/io/FileInputStream;");
        if (TYPE_VALUE == 7) sujungti_Word("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws deklaracija. išimtis Procesas_VALUE_įrašas 본문은 organizuoti javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = TAKE_Word("Lietuvių");
        if (한국어묶음) { reikalavimas_VALUE('.'); 말요구("savas"); reikalavimas_VALUE('.'); }
        if (!한국어묶음 && (TAKE_Word("Exception") || TAKE_Word("IOException"))) return;
        if (TAKE_Word("išimtis") || TAKE_Word("실행예외") || TAKE_Word("Į_I_išimtis") || TAKE_Word("Palauk_SKIRTASIS_LAIKAS_išimtis") || TAKE_Word("ADDRESS_LOOKUP_išimtis") || TAKE_Word("파일없음예외") || TAKE_Word("통신예외") || TAKE_Word("neleistinas_argumentas_išimtis") || TAKE_Word("numeris_formatas_triktis") || TAKE_Word("범위예외") || TAKE_Word("배열범위예외") || TAKE_Word("문자열범위예외") || TAKE_Word("NULL_nuoroda_išimtis") || TAKE_Word("산술예외") || TAKE_Word("Būsena_išimtis") || TAKE_Word("TYPE_perduoti_išimtis") || TAKE_Word("음수배열크기예외") || TAKE_Word("ARRAY_Store_triktis") || TAKE_Word("gija_Būsena_išimtis") || TAKE_Word("대기중단예외")) return;
        triktis_VALUE("unsupported throws type");
    }
    static void 선언읽기() {
        while (TAKE_Word("import")) {
            if (Word_VALUE(Pozicija, "Lietuvių")) 예외이름읽기();
            else {
                말요구("java"); reikalavimas_VALUE('.'); 말요구("io"); reikalavimas_VALUE('.');
                if (!(TAKE_Word("FileInputStream") || TAKE_Word("FileOutputStream") || TAKE_Word("IOException"))) triktis_VALUE("unsupported import");
            }
            reikalavimas_VALUE(';');
        }
        TAKE_Word("public"); TAKE_Word("final"); 말요구("class"); klasė_žetonas = identifikatorius_VALUE();
        klasė_konstanta = nuoroda(7, žetonas_konstanta(klasė_žetonas), 0);
        pirminis_konstanta = nuoroda(7, Word_konstanta("java/lang/Object"), 0); CODE_konstanta = Word_konstanta("Code"); reikalavimas_VALUE('{');
        while (!KLAIDA && 종류() != '}') {
            if (metodas_COUNT == 32) { triktis_VALUE("too many methods"); break; }
            int prieiga_įrašas = TAKE_Word("public") ? 1 : TAKE_Word("private") ? 2 : 0; 말요구("static");
            int FUNCTION_VALUE = metodas_COUNT++;
            metodas_prieiga[FUNCTION_VALUE] = prieiga_įrašas | 8;
            metodas_grąžinti[FUNCTION_VALUE] = formatas_VALUE(); metodas_įrašas_pavadinimas[FUNCTION_VALUE] = identifikatorius_VALUE(); reikalavimas_VALUE('(');
            for (int priekinis_VALUE = 0; priekinis_VALUE < FUNCTION_VALUE; priekinis_VALUE++) if (이름같음(metodas_įrašas_pavadinimas[priekinis_VALUE], metodas_įrašas_pavadinimas[FUNCTION_VALUE])) triktis_VALUE("duplicate method (overloading unsupported)");
            while (!KLAIDA && 종류() != ')') {
                int numeris = metodas_argumentas_COUNT[FUNCTION_VALUE];
                if (numeris == 16) { triktis_VALUE("too many parameters"); break; }
                int TYPE_VALUE = formatas_VALUE(); if (TYPE_VALUE == 0) triktis_VALUE("void parameter");
                metodas_argumentas_TYPE[FUNCTION_VALUE * 16 + numeris] = TYPE_VALUE; metodas_argumentas_pavadinimas[FUNCTION_VALUE * 16 + numeris] = identifikatorius_VALUE();
                metodas_argumentas_COUNT[FUNCTION_VALUE]++;
                if (!gauti(',')) break;
            }
            reikalavimas_VALUE(')');
            if (TAKE_Word("throws")) {
                do { 예외이름읽기(); } while (!KLAIDA && gauti(','));
            }
            metodas_pranešimo_tekstas[FUNCTION_VALUE] = Pozicija; reikalavimas_VALUE('{');
            int įdėjimas_VALUE = 1;
            while (Pozicija < žetonas_COUNT && įdėjimas_VALUE > 0) {
                if (종류() == '{') įdėjimas_VALUE++;
                if (종류() == '}') įdėjimas_VALUE--;
                Pozicija++;
            }
            if (įdėjimas_VALUE != 0) triktis_VALUE("unclosed method body");
            metodas_baigti_pokalbį[FUNCTION_VALUE] = Pozicija;
            metodas_pavadinimas_konstanta[FUNCTION_VALUE] = žetonas_konstanta(metodas_įrašas_pavadinimas[FUNCTION_VALUE]);
            문자수 = 0; sujungti_SMS('(');
            for (int numeris = 0; numeris < metodas_argumentas_COUNT[FUNCTION_VALUE]; numeris++) Įtraukti_formatas(metodas_argumentas_TYPE[FUNCTION_VALUE * 16 + numeris]);
            sujungti_SMS(')'); Įtraukti_formatas(metodas_grąžinti[FUNCTION_VALUE]); 함수서술[FUNCTION_VALUE] = simbolis_konstanta();
        }
        reikalavimas_VALUE('}'); if (Pozicija != žetonas_COUNT) triktis_VALUE("extra input after class");
    }
    static int FIND_vietinis(int Pavadinimas_2) {
        for (int numeris = vietinis_COUNT - 1; numeris >= 0; numeris--) if (지역깊이[numeris] >= 0 && 이름같음(vietinis_pavadinimas[numeris], Pavadinimas_2)) return numeris;
        triktis_VALUE("unknown variable"); return 0;
    }
    static int Įtraukti_vietinis(int Pavadinimas_2, int TYPE_VALUE) {
        for (int numeris = 0; numeris < vietinis_COUNT; numeris++) if (지역깊이[numeris] >= 0 && 이름같음(vietinis_pavadinimas[numeris], Pavadinimas_2)) triktis_VALUE("duplicate local variable");
        if (vietinis_COUNT == 128) { triktis_VALUE("too many locals"); return 0; }
        vietinis_pavadinimas[vietinis_COUNT] = Pavadinimas_2; vietinis_TYPE[vietinis_COUNT] = TYPE_VALUE; 지역깊이[vietinis_COUNT] = 깊이;
        return vietinis_COUNT++;
    }
    static boolean sveikasis_skaičius_TYPE(int TYPE_VALUE) { return TYPE_VALUE == 1 || TYPE_VALUE == 5; }
    static void 지역읽기(int numeris) { 내보내기(vietinis_TYPE[numeris] <= 2 || vietinis_TYPE[numeris] == 5 ? 21 : 25); 내보내기(numeris); }
    static void rašymas_vietinis(int numeris) { 내보내기(vietinis_TYPE[numeris] <= 2 || vietinis_TYPE[numeris] == 5 ? 54 : 58); 내보내기(numeris); }
    static void patvirtinti_TYPE(int faktinis_duomenys, int 기대) { if (faktinis_duomenys != 기대 && !(faktinis_duomenys == 5 && 기대 == 1)) triktis_VALUE("type mismatch"); }
    static void 문자읽기(int žetonas_VALUE) {
        문자수 = 0; int Paleisti = žetonas_padėtis[žetonas_VALUE] + 1, 끝 = žetonas_padėtis[žetonas_VALUE] + 토큰길이[žetonas_VALUE] - 1;
        while (Paleisti < 끝 && !KLAIDA) {
            int VALUE = ŠALTINIS[Paleisti++];
            if (VALUE == '\\') {
                if (Paleisti == 끝) { triktis_VALUE("invalid escape"); break; }
                VALUE = ŠALTINIS[Paleisti++];
                if (VALUE == 'n') VALUE = 10;
                else if (VALUE == 'r') VALUE = 13;
                else if (VALUE == 't') VALUE = 9;
                else if (VALUE == 'b') VALUE = 8;
                else if (VALUE == 'f') VALUE = 12;
                else if (VALUE != '\\' && VALUE != '"' && VALUE != '\'') triktis_VALUE("unsupported escape");
            }
            sujungti_SMS(VALUE);
        }
    }
    static int analizuoti_sintaksę_sveikasis_skaičius(int žetonas_VALUE, boolean 음수) {
        if (토큰길이[žetonas_VALUE] > 1 && ŠALTINIS[žetonas_padėtis[žetonas_VALUE]] == '0') triktis_VALUE("octal literals unsupported");
        int VALUE = 0;
        for (int numeris = 0; numeris < 토큰길이[žetonas_VALUE]; numeris++) {
            int skaitmuo_prekė = ŠALTINIS[žetonas_padėtis[žetonas_VALUE] + numeris] - '0';
            if (VALUE < -214748364 || VALUE == -214748364 && skaitmuo_prekė > (음수 ? 8 : 7)) triktis_VALUE("integer literal out of range");
            VALUE = VALUE * 10 - skaitmuo_prekė;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static int 기본식() {
        if (TAKE_Word("new")) {
            int TYPE_VALUE = formatas_VALUE();
            if (TYPE_VALUE != 6 && TYPE_VALUE != 7) { triktis_VALUE("only file streams supported by new in source"); return 0; }
            String savininkas_VALUE = TYPE_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            Komanda(187, nuoroda(7, Word_konstanta(savininkas_VALUE), 0)); 내보내기(89);
            reikalavimas_VALUE('('); patvirtinti_TYPE(reiškinys_VALUE(), 3); boolean 이어 = false;
            if (gauti(',')) { if (TYPE_VALUE != 7) triktis_VALUE("input stream constructor arguments"); patvirtinti_TYPE(reiškinys_VALUE(), 2); 이어 = true; }
            reikalavimas_VALUE(')');
            Komanda(183, išorinis_nuoroda(10, savininkas_VALUE, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return TYPE_VALUE;
        }
        if (gauti('(')) { int TYPE_VALUE = reiškinys_VALUE(); reikalavimas_VALUE(')'); return TYPE_VALUE; }
        if (종류() == 257) { 수상수(analizuoti_sintaksę_sveikasis_skaičius(Pozicija++, false)); return 1; }
        if (종류() == 258) { 문자읽기(Pozicija++); Komanda(19, nuoroda(8, simbolis_konstanta(), 0)); return 3; }
        if (종류() == 259) { 문자읽기(Pozicija++); if (문자수 != 1) triktis_VALUE("character literal length"); 수상수(문자[0]); return 5; }
        if (TAKE_Word("true")) { 내보내기(4); return 2; }
        if (TAKE_Word("false")) { 내보내기(3); return 2; }
        if (TAKE_Word("Lietuvių")) {
            reikalavimas_VALUE('.'); 말요구("savas"); reikalavimas_VALUE('.');
            String savininkas_VALUE = "", metodas_VALUE = "", aprašas_VALUE = ""; int 가 = 0, SECOND_operandas = 0, 다 = 0, 라 = 0, 마 = 0, REZULTATAS = 0;
            if (TAKE_Word("Išvestis")) {
                savininkas_VALUE = "Lietuvių/savas/Išvestis"; reikalavimas_VALUE('.');
                if (TAKE_Word("rašymas_eilutė")) { metodas_VALUE = "rašymas_eilutė"; aprašas_VALUE = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("Rašymas")) { metodas_VALUE = "Rašymas"; aprašas_VALUE = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("rašymas_numeris")) { metodas_VALUE = "rašymas_numeris"; aprašas_VALUE = "(I)V"; 가 = 1; }
                else triktis_VALUE("unknown Korean output method");
            } else if (TAKE_Word("문자")) {
                savininkas_VALUE = "Lietuvių/savas/문자"; reikalavimas_VALUE('.'); 가 = 3;
                if (TAKE_Word("길이")) { metodas_VALUE = "길이"; aprašas_VALUE = "(Ljava/lang/String;)I"; REZULTATAS = 1; }
                else if (TAKE_Word("kodo_elementas_COUNT")) { metodas_VALUE = "kodo_elementas_COUNT"; aprašas_VALUE = "(Ljava/lang/String;)I"; REZULTATAS = 1; }
                else if (TAKE_Word("analizuoti_sintaksę_sveikasis_skaičius")) { metodas_VALUE = "analizuoti_sintaksę_sveikasis_skaičius"; aprašas_VALUE = "(Ljava/lang/String;)I"; REZULTATAS = 1; }
                else if (TAKE_Word("rašymas_sveikasis_skaičius_VALUE")) { metodas_VALUE = "rašymas_sveikasis_skaičius_VALUE"; aprašas_VALUE = "(I)Ljava/lang/String;"; 가 = 1; REZULTATAS = 3; }
                else if (TAKE_Word("같음")) { metodas_VALUE = "같음"; aprašas_VALUE = "(Ljava/lang/String;Ljava/lang/String;)Z"; SECOND_operandas = 3; REZULTATAS = 2; }
                else if (TAKE_Word("Įklijuoti_SMS")) { metodas_VALUE = "Įklijuoti_SMS"; aprašas_VALUE = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; SECOND_operandas = 3; REZULTATAS = 3; }
                else if (TAKE_Word("kirpti_VALUE")) { metodas_VALUE = "kirpti_VALUE"; aprašas_VALUE = "(Ljava/lang/String;II)Ljava/lang/String;"; SECOND_operandas = 1; 다 = 1; REZULTATAS = 3; }
                else triktis_VALUE("unknown Korean text method");
            } else if (TAKE_Word("Failas")) {
                savininkas_VALUE = "Lietuvių/savas/Failas"; reikalavimas_VALUE('.'); 가 = 3;
                if (TAKE_Word("Skaitymas")) { metodas_VALUE = "Skaitymas"; aprašas_VALUE = "(Ljava/lang/String;)Ljava/lang/String;"; REZULTATAS = 3; }
                else if (TAKE_Word("Rašymas")) { metodas_VALUE = "Rašymas"; aprašas_VALUE = "(Ljava/lang/String;Ljava/lang/String;)V"; SECOND_operandas = 3; }
                else triktis_VALUE("unknown Korean file method");
            } else if (TAKE_Word("화면")) {
                savininkas_VALUE = "Lietuvių/savas/화면"; reikalavimas_VALUE('.');
                if (TAKE_Word("너비")) { metodas_VALUE = "너비"; aprašas_VALUE = "()I"; REZULTATAS = 1; }
                else if (TAKE_Word("높이")) { metodas_VALUE = "높이"; aprašas_VALUE = "()I"; REZULTATAS = 1; }
                else if (TAKE_Word("stačiakampis")) { metodas_VALUE = "stačiakampis"; aprašas_VALUE = "(IIIII)V"; 가 = 1; SECOND_operandas = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (TAKE_Word("ištrinti_įrašas")) { metodas_VALUE = "ištrinti_įrašas"; aprašas_VALUE = "(I)V"; 가 = 1; }
                else if (TAKE_Word("기다리기")) { metodas_VALUE = "기다리기"; aprašas_VALUE = "()V"; }
                else triktis_VALUE("unknown Korean framebuffer method");
            } else triktis_VALUE("unsupported Korean library class");
            reikalavimas_VALUE('('); if (가 != 0) patvirtinti_TYPE(reiškinys_VALUE(), 가);
            if (SECOND_operandas != 0) { reikalavimas_VALUE(','); patvirtinti_TYPE(reiškinys_VALUE(), SECOND_operandas); }
            if (다 != 0) { reikalavimas_VALUE(','); patvirtinti_TYPE(reiškinys_VALUE(), 다); }
            if (라 != 0) { reikalavimas_VALUE(','); patvirtinti_TYPE(reiškinys_VALUE(), 라); }
            if (마 != 0) { reikalavimas_VALUE(','); patvirtinti_TYPE(reiškinys_VALUE(), 마); }
            reikalavimas_VALUE(')'); Komanda(184, išorinis_nuoroda(10, savininkas_VALUE, metodas_VALUE, aprašas_VALUE)); return REZULTATAS;
        }
        if (TAKE_Word("Integer")) {
            reikalavimas_VALUE('.'); 말요구("parseInt"); reikalavimas_VALUE('('); patvirtinti_TYPE(reiškinys_VALUE(), 3); reikalavimas_VALUE(')');
            Komanda(184, išorinis_nuoroda(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Pavadinimas_2 = identifikatorius_VALUE();
        if (gauti('(')) {
            int FUNCTION_VALUE = -1;
            for (int numeris = 0; numeris < metodas_COUNT; numeris++) if (이름같음(Pavadinimas_2, metodas_įrašas_pavadinimas[numeris])) FUNCTION_VALUE = numeris;
            if (FUNCTION_VALUE < 0) { triktis_VALUE("unknown static method"); return 0; }
            int numeris = 0;
            while (!KLAIDA && 종류() != ')') {
                if (numeris >= metodas_argumentas_COUNT[FUNCTION_VALUE]) { triktis_VALUE("too many arguments"); break; }
                patvirtinti_TYPE(reiškinys_VALUE(), metodas_argumentas_TYPE[FUNCTION_VALUE * 16 + numeris++]); if (!gauti(',')) break;
            }
            reikalavimas_VALUE(')'); if (numeris != metodas_argumentas_COUNT[FUNCTION_VALUE]) triktis_VALUE("argument count mismatch");
            Komanda(184, nuoroda(10, klasė_konstanta, nuoroda(12, metodas_pavadinimas_konstanta[FUNCTION_VALUE], 함수서술[FUNCTION_VALUE])));
            return metodas_grąžinti[FUNCTION_VALUE];
        }
        int vietinis_Aprėptis = FIND_vietinis(Pavadinimas_2), TYPE_VALUE = vietinis_TYPE[vietinis_Aprėptis]; 지역읽기(vietinis_Aprėptis);
        while (!KLAIDA) {
            if (gauti('[')) { patvirtinti_TYPE(TYPE_VALUE, 4); patvirtinti_TYPE(reiškinys_VALUE(), 1); reikalavimas_VALUE(']'); 내보내기(50); TYPE_VALUE = 3; }
            else if (gauti('.')) {
                if (TYPE_VALUE == 6 || TYPE_VALUE == 7) {
                    String savininkas_VALUE = TYPE_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (TAKE_Word("close")) { reikalavimas_VALUE('('); reikalavimas_VALUE(')'); Komanda(182, išorinis_nuoroda(10, savininkas_VALUE, "close", "()V")); TYPE_VALUE = 0; }
                    else if (TYPE_VALUE == 6 && TAKE_Word("read")) { reikalavimas_VALUE('('); reikalavimas_VALUE(')'); Komanda(182, išorinis_nuoroda(10, savininkas_VALUE, "read", "()I")); TYPE_VALUE = 1; }
                    else if (TYPE_VALUE == 7 && TAKE_Word("write")) { reikalavimas_VALUE('('); patvirtinti_TYPE(reiškinys_VALUE(), 1); reikalavimas_VALUE(')'); Komanda(182, išorinis_nuoroda(10, savininkas_VALUE, "write", "(I)V")); TYPE_VALUE = 0; }
                    else { triktis_VALUE("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (TYPE_VALUE == 4) { 내보내기(190); TYPE_VALUE = 1; }
                else { patvirtinti_TYPE(TYPE_VALUE, 3); reikalavimas_VALUE('('); reikalavimas_VALUE(')'); Komanda(182, išorinis_nuoroda(10, "java/lang/String", "length", "()I")); TYPE_VALUE = 1; }
            } else break;
        }
        return TYPE_VALUE;
    }
    static int 단항() {
        if (++식깊이 > 64) { triktis_VALUE("expression nesting too deep"); 식깊이--; return 0; }
        int TYPE_VALUE;
        if (gauti('!')) { patvirtinti_TYPE(단항(), 2); Palyginimas_VALUE(153); TYPE_VALUE = 2; }
        else if (gauti('-')) {
            if (종류() == 257) 수상수(analizuoti_sintaksę_sveikasis_skaičius(Pozicija++, true));
            else { patvirtinti_TYPE(단항(), 1); 내보내기(116); }
            TYPE_VALUE = 1;
        } else if (gauti('+')) { patvirtinti_TYPE(단항(), 1); TYPE_VALUE = 1; }
        else TYPE_VALUE = 기본식();
        식깊이--; return TYPE_VALUE;
    }
    static int 곱식() {
        int TYPE_VALUE = 단항();
        while (!KLAIDA && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int kodavimas_VALUE = 종류(); Pozicija++; patvirtinti_TYPE(TYPE_VALUE, 1); patvirtinti_TYPE(단항(), 1);
            내보내기(kodavimas_VALUE == '*' ? 104 : kodavimas_VALUE == '/' ? 108 : 112); TYPE_VALUE = 1;
        }
        return TYPE_VALUE;
    }
    static int 합식() {
        int TYPE_VALUE = 곱식();
        while (!KLAIDA && (종류() == '+' || 종류() == '-')) {
            int kodavimas_VALUE = 종류(); Pozicija++; int 경계 = CODE_dydis, ATGAL_VALUE_TYPE = 곱식();
            if (kodavimas_VALUE == '+' && (TYPE_VALUE == 3 || ATGAL_VALUE_TYPE == 3)) { 결합(경계, TYPE_VALUE, ATGAL_VALUE_TYPE); TYPE_VALUE = 3; }
            else { patvirtinti_TYPE(TYPE_VALUE, 1); patvirtinti_TYPE(ATGAL_VALUE_TYPE, 1); 내보내기(kodavimas_VALUE == '+' ? 96 : 100); TYPE_VALUE = 1; }
        }
        return TYPE_VALUE;
    }
    static int 붙임참조(int TYPE_VALUE) {
        if (TYPE_VALUE != 1 && TYPE_VALUE != 2 && TYPE_VALUE != 3 && TYPE_VALUE != 5) triktis_VALUE("unsupported concatenation type");
        return išorinis_nuoroda(10, "java/lang/StringBuilder", "append", TYPE_VALUE == 1 ? "(I)Ljava/lang/StringBuilder;"
            : TYPE_VALUE == 2 ? "(Z)Ljava/lang/StringBuilder;" : TYPE_VALUE == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int 경계, int priekinis_VALUE_TYPE, int ATGAL_VALUE_TYPE) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 RIGHT CODE_VALUE 앞에 generuoti 코드를 삽입한다.
        // RIGHT reiškinys_VALUE 내부의 lygiavertis_mazgas_VALUE šaka 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = CODE_dydis;
        Komanda(187, nuoroda(7, Word_konstanta("java/lang/StringBuilder"), 0)); 내보내기(89);
        Komanda(183, išorinis_nuoroda(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); Komanda(182, 붙임참조(priekinis_VALUE_TYPE));
        if (KLAIDA) return;
        int 길이 = CODE_dydis - 끝;
        for (int numeris = 0; numeris < 길이; numeris++) 삽입코드[numeris] = CODE_VALUE[끝 + numeris];
        for (int numeris = 끝 - 1; numeris >= 경계; numeris--) CODE_VALUE[numeris + 길이] = CODE_VALUE[numeris];
        for (int numeris = 0; numeris < 길이; numeris++) CODE_VALUE[경계 + numeris] = 삽입코드[numeris];
        Komanda(182, 붙임참조(ATGAL_VALUE_TYPE)); Komanda(182, išorinis_nuoroda(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int Palyginimas_reiškinys() {
        int TYPE_VALUE = 합식();
        while (!KLAIDA && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int kodavimas_VALUE = 종류(); Pozicija++; patvirtinti_TYPE(TYPE_VALUE, 1); patvirtinti_TYPE(합식(), 1);
            Palyginimas_VALUE(kodavimas_VALUE == '<' ? 161 : kodavimas_VALUE == '>' ? 163 : kodavimas_VALUE == 302 ? 164 : 162); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int 동등식() {
        int TYPE_VALUE = Palyginimas_reiškinys();
        while (!KLAIDA && (종류() == 300 || 종류() == 301)) {
            int kodavimas_VALUE = 종류(); Pozicija++; int ATGAL_VALUE_TYPE = Palyginimas_reiškinys();
            if (TYPE_VALUE == 0 || ATGAL_VALUE_TYPE == 0) triktis_VALUE("void expression");
            if (!(sveikasis_skaičius_TYPE(TYPE_VALUE) && sveikasis_skaičius_TYPE(ATGAL_VALUE_TYPE))) patvirtinti_TYPE(ATGAL_VALUE_TYPE, TYPE_VALUE);
            Palyginimas_VALUE((TYPE_VALUE <= 2 || TYPE_VALUE == 5 ? 159 : 165) + (kodavimas_VALUE == 301 ? 1 : 0)); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int 논리곱() {
        int TYPE_VALUE = 동등식();
        while (!KLAIDA && gauti(304)) {
            patvirtinti_TYPE(TYPE_VALUE, 2); int 가 = šaka(153); patvirtinti_TYPE(동등식(), 2); int SECOND_operandas = šaka(153);
            내보내기(4); int 끝 = šaka(167); sieti_VALUE(가, CODE_dydis); sieti_VALUE(SECOND_operandas, CODE_dydis); 내보내기(3); sieti_VALUE(끝, CODE_dydis); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int reiškinys_VALUE() {
        int TYPE_VALUE = 논리곱();
        while (!KLAIDA && gauti(305)) {
            patvirtinti_TYPE(TYPE_VALUE, 2); int 가 = šaka(154); patvirtinti_TYPE(논리곱(), 2); int SECOND_operandas = šaka(154);
            내보내기(3); int 끝 = šaka(167); sieti_VALUE(가, CODE_dydis); sieti_VALUE(SECOND_operandas, CODE_dydis); 내보내기(4); sieti_VALUE(끝, CODE_dydis); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static void užduotis_VALUE(boolean Leisti_deklaracija) {
        if (Word_VALUE(Pozicija, "int") || Word_VALUE(Pozicija, "boolean") || Word_VALUE(Pozicija, "String") || Word_VALUE(Pozicija, "char")
            || Word_VALUE(Pozicija, "FileInputStream") || Word_VALUE(Pozicija, "FileOutputStream")) {
            if (!Leisti_deklaracija) triktis_VALUE("declaration not allowed here");
            int TYPE_VALUE = formatas_VALUE(), Pavadinimas_2 = identifikatorius_VALUE(); reikalavimas_VALUE('='); patvirtinti_TYPE(reiškinys_VALUE(), TYPE_VALUE);
            rašymas_vietinis(Įtraukti_vietinis(Pavadinimas_2, TYPE_VALUE)); return;
        }
        int Pavadinimas_2 = identifikatorius_VALUE(), vietinis_Aprėptis = FIND_vietinis(Pavadinimas_2);
        if (gauti('=')) { patvirtinti_TYPE(reiškinys_VALUE(), vietinis_TYPE[vietinis_Aprėptis]); rašymas_vietinis(vietinis_Aprėptis); }
        else if (종류() >= 308 && 종류() <= 312) {
            int kodavimas_VALUE = 종류(); Pozicija++; 지역읽기(vietinis_Aprėptis); int 경계 = CODE_dydis, ATGAL_VALUE_TYPE = reiškinys_VALUE();
            if (kodavimas_VALUE == 308 && vietinis_TYPE[vietinis_Aprėptis] == 3) 결합(경계, 3, ATGAL_VALUE_TYPE);
            else {
                patvirtinti_TYPE(vietinis_TYPE[vietinis_Aprėptis], 1); patvirtinti_TYPE(ATGAL_VALUE_TYPE, 1);
                내보내기(kodavimas_VALUE == 308 ? 96 : kodavimas_VALUE == 309 ? 100 : kodavimas_VALUE == 310 ? 104 : kodavimas_VALUE == 311 ? 108 : 112);
                if (vietinis_TYPE[vietinis_Aprėptis] == 5) 내보내기(146);
            }
            rašymas_vietinis(vietinis_Aprėptis);
        }
        else if (종류() == 306 || 종류() == 307) {
            patvirtinti_TYPE(vietinis_TYPE[vietinis_Aprėptis], 1); 내보내기(132); 내보내기(vietinis_Aprėptis); 내보내기(종류() == 306 ? 1 : 255); Pozicija++;
            if (vietinis_TYPE[vietinis_Aprėptis] == 5) { 지역읽기(vietinis_Aprėptis); 내보내기(146); rašymas_vietinis(vietinis_Aprėptis); }
        } else triktis_VALUE("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); reikalavimas_VALUE('.'); 말요구("out"); reikalavimas_VALUE('.');
        boolean 줄바꿈 = TAKE_Word("println"); if (!줄바꿈) 말요구("print"); reikalavimas_VALUE('(');
        Komanda(178, išorinis_nuoroda(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean 빈인수 = 종류() == ')';
        int TYPE_VALUE = 빈인수 ? 0 : reiškinys_VALUE(); reikalavimas_VALUE(')'); reikalavimas_VALUE(';');
        String aprašas_VALUE = TYPE_VALUE == 0 ? "()V" : TYPE_VALUE == 1 ? "(I)V" : TYPE_VALUE == 2 ? "(Z)V" : TYPE_VALUE == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (TYPE_VALUE == 4 || TYPE_VALUE >= 6 || TYPE_VALUE == 0 && (!줄바꿈 || !빈인수)) triktis_VALUE("unsupported print argument");
        Komanda(182, išorinis_nuoroda(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", aprašas_VALUE));
    }
    static boolean išrašas_VALUE() {
        if (KLAIDA) return false;
        if (깊이 > 32) { triktis_VALUE("statement nesting too deep"); return false; }
        if (gauti('{')) {
            깊이++; boolean grąžinti_KR = false;
            while (!KLAIDA && 종류() != '}') { if (grąžinti_KR) triktis_VALUE("unreachable statement"); grąžinti_KR = išrašas_VALUE(); }
            reikalavimas_VALUE('}'); for (int numeris = 0; numeris < vietinis_COUNT; numeris++) if (지역깊이[numeris] == 깊이) 지역깊이[numeris] = -1;
            깊이--; return grąžinti_KR;
        }
        if (gauti(';')) return false;
        if (TAKE_Word("return")) {
            int TYPE_VALUE = 종류() == ';' ? 0 : reiškinys_VALUE(); patvirtinti_TYPE(TYPE_VALUE, metodas_grąžinti[dabartinis_metodas]); reikalavimas_VALUE(';');
            내보내기(TYPE_VALUE == 0 ? 177 : TYPE_VALUE <= 2 || TYPE_VALUE == 5 ? 172 : 176); return true;
        }
        if (TAKE_Word("if")) {
            reikalavimas_VALUE('('); patvirtinti_TYPE(reiškinys_VALUE(), 2); reikalavimas_VALUE(')'); int FALSE_VALUE = šaka(153);
            깊이++; boolean 가 = valdymas_išrašas(); 깊이--;
            if (TAKE_Word("else")) { int 끝 = šaka(167); sieti_VALUE(FALSE_VALUE, CODE_dydis); 깊이++; boolean SECOND_operandas = valdymas_išrašas(); 깊이--; sieti_VALUE(끝, CODE_dydis); return 가 && SECOND_operandas; }
            sieti_VALUE(FALSE_VALUE, CODE_dydis); return false;
        }
        if (TAKE_Word("while")) {
            int Paleisti = CODE_dydis; reikalavimas_VALUE('('); patvirtinti_TYPE(reiškinys_VALUE(), 2); reikalavimas_VALUE(')'); int 끝 = šaka(153);
            깊이++; valdymas_išrašas(); 깊이--; sieti_VALUE(šaka(167), Paleisti); sieti_VALUE(끝, CODE_dydis); return false;
        }
        if (TAKE_Word("for")) {
            깊이++; reikalavimas_VALUE('('); if (종류() != ';') užduotis_VALUE(true); reikalavimas_VALUE(';');
            int sąlyga = CODE_dydis; if (종류() == ';') 내보내기(4); else patvirtinti_TYPE(reiškinys_VALUE(), 2); reikalavimas_VALUE(';');
            int 끝 = šaka(153), pagrindinis_tekstas = šaka(167), atnaujinti = CODE_dydis;
            if (종류() != ')') užduotis_VALUE(false); reikalavimas_VALUE(')'); sieti_VALUE(šaka(167), sąlyga); sieti_VALUE(pagrindinis_tekstas, CODE_dydis);
            valdymas_išrašas(); sieti_VALUE(šaka(167), atnaujinti); sieti_VALUE(끝, CODE_dydis);
            for (int numeris = 0; numeris < vietinis_COUNT; numeris++) if (지역깊이[numeris] == 깊이) 지역깊이[numeris] = -1;
            깊이--; return false;
        }
        if (Word_VALUE(Pozicija, "System")) { 화면출력(); return false; }
        if (종류() == 256 && Pozicija + 1 < žetonas_COUNT && (토큰종류[Pozicija + 1] == '(' || 토큰종류[Pozicija + 1] == '.')) {
            int TYPE_VALUE = reiškinys_VALUE(); if (TYPE_VALUE != 0) 내보내기(87); reikalavimas_VALUE(';'); return false;
        }
        užduotis_VALUE(true); reikalavimas_VALUE(';'); return false;
    }
    static boolean valdymas_išrašas() {
        if (Word_VALUE(Pozicija, "int") || Word_VALUE(Pozicija, "boolean") || Word_VALUE(Pozicija, "char") || Word_VALUE(Pozicija, "String")
            || Word_VALUE(Pozicija, "FileInputStream") || Word_VALUE(Pozicija, "FileOutputStream")) triktis_VALUE("local declaration requires braces");
        return išrašas_VALUE();
    }
    static void 출바(int VALUE) { if (išeiga_dydis == Išvestis.length) triktis_VALUE("class file too large"); else Išvestis[išeiga_dydis++] = VALUE & 255; }
    static void 출짧(int VALUE) { 출바(VALUE >> 8); 출바(VALUE); }
    static void 출정(int VALUE) { 출짧(VALUE >>> 16); 출짧(VALUE); }
    static void rašymas_klasė() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(konstanta_COUNT);
        for (int numeris = 0; numeris < konstanta_dydis; numeris++) 출바(konstanta_VALUE[numeris]);
        출짧(0x21); 출짧(klasė_konstanta); 출짧(pirminis_konstanta); 출짧(0); 출짧(0); 출짧(metodas_COUNT);
        for (int numeris = 0; numeris < metodas_COUNT; numeris++) {
            출짧(metodas_prieiga[numeris]); 출짧(metodas_pavadinimas_konstanta[numeris]); 출짧(함수서술[numeris]); 출짧(1); 출짧(CODE_konstanta);
            출정(12 + 함수길이[numeris]); 출짧(128); 출짧(함수지역[numeris]); 출정(함수길이[numeris]);
            for (int 칸 = 0; 칸 < 함수길이[numeris]; 칸++) 출바(CODE_VALUE[metodas_CODE[numeris] + 칸]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int Paleisti() {
        if (naudotojas.인수개수() == 1 && 자바도구.같음(naudotojas.Argumentai(0), "-version")) {
            naudotojas.Rašymas("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (naudotojas.인수개수() != 1) { naudotojas.Rašymas("Usage: javac FILE.java\n"); return 2; }
        int pavadinimas_dydis = 자바도구.Pavadinimas_2(failo_vardas_SMS, naudotojas.Argumentai(0));
        if (pavadinimas_dydis < 6 || pavadinimas_dydis > 62 || failo_vardas_SMS[pavadinimas_dydis - 5] != '.' || failo_vardas_SMS[pavadinimas_dydis - 4] != 'j'
            || failo_vardas_SMS[pavadinimas_dydis - 3] != 'a' || failo_vardas_SMS[pavadinimas_dydis - 2] != 'v' || failo_vardas_SMS[pavadinimas_dydis - 1] != 'a') {
            naudotojas.Rašymas("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        šaltinis_dydis = naudotojas.파일읽기(failo_vardas_SMS, ŠALTINIS);
        if (šaltinis_dydis < 0) { naudotojas.Rašymas("javac: cannot read source: "); 자바도구.rašymas_numeris(šaltinis_dydis); naudotojas.rašymas_simbolis_VALUE(10); return 1; }
        šaltinis_dydis = 자바도구.원문해독(ŠALTINIS, šaltinis_dydis);
        if (šaltinis_dydis < 0) { naudotojas.Rašymas("javac error: invalid UTF-8 source\n"); return 1; }
        kirpti_VALUE(); if (!KLAIDA) 선언읽기();
        if (!KLAIDA) {
            if (토큰길이[klasė_žetonas] != pavadinimas_dydis - 5) triktis_VALUE("class name must match file name");
            for (int numeris = 0; numeris < pavadinimas_dydis - 5; numeris++) if (ŠALTINIS[žetonas_padėtis[klasė_žetonas] + numeris] != failo_vardas_SMS[numeris]) triktis_VALUE("class name must match file name");
        }
        for (dabartinis_metodas = 0; dabartinis_metodas < metodas_COUNT && !KLAIDA; dabartinis_metodas++) {
            Pozicija = metodas_pranešimo_tekstas[dabartinis_metodas]; metodas_CODE[dabartinis_metodas] = CODE_dydis; vietinis_COUNT = 0; 깊이 = 0;
            for (int numeris = 0; numeris < metodas_argumentas_COUNT[dabartinis_metodas]; numeris++) Įtraukti_vietinis(metodas_argumentas_pavadinimas[dabartinis_metodas * 16 + numeris], metodas_argumentas_TYPE[dabartinis_metodas * 16 + numeris]);
            boolean grąžinti_KR = išrašas_VALUE();
            if (!grąžinti_KR && metodas_grąžinti[dabartinis_metodas] != 0) triktis_VALUE("missing return");
            // šaka 뒤의 합류 지점은 반드시 faktinis_duomenys 명령이어야 한다 (버전 49 검증기).
            if (metodas_grąžinti[dabartinis_metodas] == 0) 내보내기(177);
            else { boolean sveikasis_skaičius = metodas_grąžinti[dabartinis_metodas] <= 2 || metodas_grąžinti[dabartinis_metodas] == 5; 내보내기(sveikasis_skaičius ? 3 : 1); 내보내기(sveikasis_skaičius ? 172 : 176); }
            if (Pozicija != metodas_baigti_pokalbį[dabartinis_metodas]) triktis_VALUE("invalid method body");
            함수지역[dabartinis_metodas] = vietinis_COUNT; 함수길이[dabartinis_metodas] = CODE_dydis - metodas_CODE[dabartinis_metodas];
        }
        if (KLAIDA) return 1;
        rašymas_klasė(); if (KLAIDA) return 1;
        failo_vardas_SMS[pavadinimas_dydis - 4] = 'c'; failo_vardas_SMS[pavadinimas_dydis - 3] = 'l'; failo_vardas_SMS[pavadinimas_dydis - 2] = 'a';
        failo_vardas_SMS[pavadinimas_dydis - 1] = 's'; failo_vardas_SMS[pavadinimas_dydis] = 's'; failo_vardas_SMS[pavadinimas_dydis + 1] = 0;
        int REZULTATAS = naudotojas.rašymas_Failas(failo_vardas_SMS, Išvestis, išeiga_dydis);
        if (REZULTATAS < 0) { naudotojas.Rašymas("javac: cannot save class: "); 자바도구.rašymas_numeris(REZULTATAS); naudotojas.rašymas_simbolis_VALUE(10); return 1; }
        naudotojas.Rašymas("Compiled: "); for (int numeris = 0; failo_vardas_SMS[numeris] != 0; numeris++) naudotojas.rašymas_simbolis_VALUE(failo_vardas_SMS[numeris]);
        naudotojas.Rašymas(" (JVM class version 49)\n"); return 0;
    }
}
