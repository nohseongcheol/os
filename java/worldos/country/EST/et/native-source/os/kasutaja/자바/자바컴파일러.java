// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java lähe_puu -> 표준 버전 49 class kompilaator. */
public final class 자바컴파일러 {
    static int[] ALLIKAS = new int[16384], Väljund = new int[16384], CODE_VALUE = new int[4096];
    static int[] 토큰종류 = new int[2048], luba_ametikoht = new int[2048], 토큰길이 = new int[2048];
    static int[] konstant_VALUE = new int[4096], konstant_nihe = new int[512];
    static int[] 문자 = new int[512], failinimi_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int lähe_suurust_muutma, luba_COUNT, Asukoht, CODE_suurust_muutma, konstant_suurust_muutma, konstant_COUNT = 1, toodang_suurust_muutma, 문자수;
    static boolean VIGA;
    static int tund_luba, tund_konstant, ema_konstant, CODE_konstant;
    static int[] meetod_kirje_nimetus = new int[32], meetod_tagasi_saatma = new int[32], meetod_argument_COUNT = new int[32];
    static int[] meetod_argument_nimetus = new int[512], meetod_argument_TYPE = new int[512];
    static int[] meetod_sisu = new int[32], meetod_lõpeta_kõne = new int[32], meetod_CODE = new int[32];
    static int[] 함수길이 = new int[32], 함수지역 = new int[32], meetod_nimetus_konstant = new int[32], 함수서술 = new int[32];
    static int[] meetod_pöördus = new int[32];
    static int meetod_COUNT, tähtaja_piires_meetod, kohalik_COUNT, 깊이, 식깊이;
    static int[] kohalik_nimetus = new int[128], kohalik_TYPE = new int[128], 지역깊이 = new int[128];

    static void tõrge_VALUE(String 이유) {
        if (!VIGA) {
            kasutaja.Kirjutamine("javac error: "); kasutaja.Kirjutamine(이유);
            kasutaja.Kirjutamine(" at line ");
            int Joon = 1, 끝 = Asukoht < luba_COUNT ? luba_ametikoht[Asukoht] : lähe_suurust_muutma;
            for (int number = 0; number < 끝; number++) if (ALLIKAS[number] == 10) Joon++;
            자바도구.kirjutamine_number(Joon); kasutaja.kirjutamine_märk_VALUE(10);
        }
        VIGA = true;
    }
    static boolean märk_VALUE(int VALUE) { return 문자이름규칙.첫글자(VALUE); }
    static boolean number_VALUE(int VALUE) { return VALUE >= '0' && VALUE <= '9'; }
    static boolean 이름같음(int 가, int SECOND_operand) {
        if (가 < 0 || SECOND_operand < 0 || 가 >= luba_COUNT || SECOND_operand >= luba_COUNT || 토큰길이[가] != 토큰길이[SECOND_operand]) return false;
        for (int number = 0; number < 토큰길이[가]; number++) if (ALLIKAS[luba_ametikoht[가] + number] != ALLIKAS[luba_ametikoht[SECOND_operand] + number]) return false;
        return true;
    }
    static boolean Word_VALUE(int luba_VALUE_eb540501, String Word_SMS) {
        if (luba_VALUE_eb540501 < 0 || luba_VALUE_eb540501 >= luba_COUNT || 토큰길이[luba_VALUE_eb540501] != Word_SMS.length()) return false;
        for (int number = 0; number < Word_SMS.length(); number++) if (ALLIKAS[luba_ametikoht[luba_VALUE_eb540501] + number] != Word_SMS.charAt(number)) return false;
        return true;
    }
    static int 종류() { return Asukoht < luba_COUNT ? 토큰종류[Asukoht] : 0; }
    static boolean saama(int VALUE) { if (종류() != VALUE) return false; Asukoht++; return true; }
    static void nõue_VALUE(int VALUE) { if (!saama(VALUE)) tõrge_VALUE("unexpected token"); }
    static boolean TAKE_Word(String Word_SMS) { if (!Word_VALUE(Asukoht, Word_SMS)) return false; Asukoht++; return true; }
    static void 말요구(String Word_SMS) { if (!TAKE_Word(Word_SMS)) tõrge_VALUE(Word_SMS); }
    static int identifikaator_VALUE() {
        int TULEMUS = Asukoht;
        if (종류() != 256) tõrge_VALUE("identifier required"); else Asukoht++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int Käivita_2 = 0;
        for (int number = 0; number <= 예약어.length(); number++) {
            if (number == 예약어.length() || 예약어.charAt(number) == ' ') {
                boolean 같음 = number - Käivita_2 == 토큰길이[TULEMUS];
                for (int 칸 = Käivita_2; 같음 && 칸 < number; 칸++) if (예약어.charAt(칸) != ALLIKAS[luba_ametikoht[TULEMUS] + 칸 - Käivita_2]) 같음 = false;
                if (같음) tõrge_VALUE("reserved word cannot be an identifier");
                Käivita_2 = number + 1;
            }
        }
        return TULEMUS;
    }
    static void lõikama_VALUE() {
        int number = 0;
        while (number < lähe_suurust_muutma && !VIGA) {
            int VALUE = ALLIKAS[number], Käivita_2 = number, 종류 = VALUE;
            if (VALUE == 32 || VALUE == 9 || VALUE == 10 || VALUE == 13) { number++; continue; }
            if (VALUE == '/' && number + 1 < lähe_suurust_muutma && ALLIKAS[number + 1] == '/') {
                while (number < lähe_suurust_muutma && ALLIKAS[number] != 10) number++;
                continue;
            }
            if (VALUE == '/' && number + 1 < lähe_suurust_muutma && ALLIKAS[number + 1] == '*') {
                number += 2;
                while (number + 1 < lähe_suurust_muutma && !(ALLIKAS[number] == '*' && ALLIKAS[number + 1] == '/')) number++;
                if (number + 1 >= lähe_suurust_muutma) { tõrge_VALUE("unterminated comment"); break; }
                number += 2; continue;
            }
            if (märk_VALUE(VALUE)) { 종류 = 256; while (number < lähe_suurust_muutma && 문자이름규칙.이어진글자(ALLIKAS[number])) number++; }
            else if (number_VALUE(VALUE)) { 종류 = 257; while (number < lähe_suurust_muutma && number_VALUE(ALLIKAS[number])) number++; }
            else if (VALUE == '"' || VALUE == '\'') {
                종류 = VALUE == '"' ? 258 : 259; number++;
                while (number < lähe_suurust_muutma && ALLIKAS[number] != VALUE && ALLIKAS[number] != 10 && ALLIKAS[number] != 13) {
                    if (ALLIKAS[number] == '\\') number++;
                    number++;
                }
                if (number >= lähe_suurust_muutma || ALLIKAS[number] != VALUE) { tõrge_VALUE("unterminated literal"); break; }
                number++;
            } else {
                number++;
                if (number < lähe_suurust_muutma) {
                    int Edasi_kaup = ALLIKAS[number];
                    if (VALUE == '=' && Edasi_kaup == '=') 종류 = 300;
                    if (VALUE == '!' && Edasi_kaup == '=') 종류 = 301;
                    if (VALUE == '<' && Edasi_kaup == '=') 종류 = 302;
                    if (VALUE == '>' && Edasi_kaup == '=') 종류 = 303;
                    if (VALUE == '&' && Edasi_kaup == '&') 종류 = 304;
                    if (VALUE == '|' && Edasi_kaup == '|') 종류 = 305;
                    if (VALUE == '+' && Edasi_kaup == '+') 종류 = 306;
                    if (VALUE == '-' && Edasi_kaup == '-') 종류 = 307;
                    if (VALUE == '+' && Edasi_kaup == '=') 종류 = 308;
                    if (VALUE == '-' && Edasi_kaup == '=') 종류 = 309;
                    if (VALUE == '*' && Edasi_kaup == '=') 종류 = 310;
                    if (VALUE == '/' && Edasi_kaup == '=') 종류 = 311;
                    if (VALUE == '%' && Edasi_kaup == '=') 종류 = 312;
                    if (종류 >= 300) number++;
                }
            }
            if (luba_COUNT == 토큰종류.length - 1) { tõrge_VALUE("too many tokens (2047 maximum)"); break; }
            토큰종류[luba_COUNT] = 종류; luba_ametikoht[luba_COUNT] = Käivita_2; 토큰길이[luba_COUNT++] = number - Käivita_2;
        }
    }
    static void kirjutamine_konstant_bait(int VALUE) {
        if (konstant_suurust_muutma == konstant_VALUE.length) { tõrge_VALUE("constant pool too large"); return; }
        konstant_VALUE[konstant_suurust_muutma++] = VALUE & 255;
    }
    static void 상짧(int VALUE) { kirjutamine_konstant_bait(VALUE >> 8); kirjutamine_konstant_bait(VALUE); }
    static int register_konstant(int Käivita_2) {
        for (int number = 1; number < konstant_COUNT; number++) {
            int esikaamera_VALUE = konstant_nihe[number], 길이 = (number + 1 < konstant_COUNT ? konstant_nihe[number + 1] : Käivita_2) - esikaamera_VALUE;
            if (길이 != konstant_suurust_muutma - Käivita_2) continue;
            boolean 같음 = true;
            for (int 칸 = 0; 칸 < 길이; 칸++) if (konstant_VALUE[esikaamera_VALUE + 칸] != konstant_VALUE[Käivita_2 + 칸]) 같음 = false;
            if (같음) { konstant_suurust_muutma = Käivita_2; return number; }
        }
        if (konstant_COUNT == konstant_nihe.length) { tõrge_VALUE("too many constants"); return 0; }
        konstant_nihe[konstant_COUNT] = Käivita_2;
        return konstant_COUNT++;
    }
    static void Lisa_SMS(int VALUE) {
        if (문자수 == 문자.length) { tõrge_VALUE("text too long"); return; }
        문자[문자수++] = VALUE;
    }
    static void Lisa_Word(String Word_SMS) { for (int number = 0; number < Word_SMS.length(); number++) Lisa_SMS(Word_SMS.charAt(number)); }
    static int märk_konstant() {
        int Käivita_2 = konstant_suurust_muutma; kirjutamine_konstant_bait(1); 상짧(0);
        for (int number = 0; number < 문자수; number++) {
            int VALUE = 문자[number];
            if (VALUE > 0 && VALUE < 128) kirjutamine_konstant_bait(VALUE);
            else if (VALUE < 2048) { kirjutamine_konstant_bait(192 | VALUE >> 6); kirjutamine_konstant_bait(128 | VALUE & 63); }
            else { kirjutamine_konstant_bait(224 | VALUE >> 12); kirjutamine_konstant_bait(128 | VALUE >> 6 & 63); kirjutamine_konstant_bait(128 | VALUE & 63); }
        }
        if (VIGA) return 0;
        int 길이 = konstant_suurust_muutma - Käivita_2 - 3;
        konstant_VALUE[Käivita_2 + 1] = 길이 >> 8; konstant_VALUE[Käivita_2 + 2] = 길이 & 255;
        return register_konstant(Käivita_2);
    }
    static int Word_konstant(String Word_SMS) { 문자수 = 0; Lisa_Word(Word_SMS); return märk_konstant(); }
    static int luba_konstant(int luba_VALUE_eb540501) {
        문자수 = 0;
        for (int number = 0; number < 토큰길이[luba_VALUE_eb540501]; number++) Lisa_SMS(ALLIKAS[luba_ametikoht[luba_VALUE_eb540501] + number]);
        return märk_konstant();
    }
    static int viide(int 종류, int 가, int SECOND_operand) {
        int Käivita_2 = konstant_suurust_muutma; kirjutamine_konstant_bait(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(SECOND_operand);
        return register_konstant(Käivita_2);
    }
    static int väline_viide(int 종류, String omanik_VALUE, String Nimi_2, String 서술) {
        int omanik_identifikaator = viide(7, Word_konstant(omanik_VALUE), 0);
        int nimetus_COUNT = Word_konstant(Nimi_2), vorming_COUNT = Word_konstant(서술);
        return viide(종류, omanik_identifikaator, viide(12, nimetus_COUNT, vorming_COUNT));
    }
    static void 내보내기(int VALUE) {
        if (CODE_suurust_muutma == CODE_VALUE.length) { tõrge_VALUE("bytecode too large"); return; }
        CODE_VALUE[CODE_suurust_muutma++] = VALUE & 255;
    }
    static void Käsk(int VALUE, int Argumendid) { 내보내기(VALUE); 내보내기(Argumendid >> 8); 내보내기(Argumendid); }
    static void 수상수(int VALUE) {
        if (VALUE >= -1 && VALUE <= 5) { 내보내기(VALUE + 3); return; }
        int Käivita_2 = konstant_suurust_muutma; kirjutamine_konstant_bait(3); 상짧(VALUE >>> 16); 상짧(VALUE);
        Käsk(19, register_konstant(Käivita_2));
    }
    static int haru(int Käsk) { int TULEMUS = CODE_suurust_muutma; Käsk(Käsk, 0); return TULEMUS; }
    static void Link_VALUE(int haru, int siht_objekt) {
        if (VIGA) return;
        int 거리 = siht_objekt - haru;
        if (거리 < -32768 || 거리 > 32767 || haru < 0 || haru + 2 >= CODE_suurust_muutma) { tõrge_VALUE("invalid branch"); return; }
        CODE_VALUE[haru + 1] = 거리 >> 8 & 255; CODE_VALUE[haru + 2] = 거리 & 255;
    }
    static void Võrdlus_VALUE(int Käsk) {
        int TRUE_VALUE = haru(Käsk); 내보내기(3); int 끝 = haru(167);
        Link_VALUE(TRUE_VALUE, CODE_suurust_muutma); 내보내기(4); Link_VALUE(끝, CODE_suurust_muutma);
    }
    static int vorming_VALUE() {
        if (TAKE_Word("void")) return 0;
        if (TAKE_Word("int")) return 1;
        if (TAKE_Word("boolean")) return 2;
        if (TAKE_Word("char")) return 5;
        if (TAKE_Word("FileInputStream")) return 6;
        if (TAKE_Word("FileOutputStream")) return 7;
        if (TAKE_Word("String")) { if (saama('[')) { nõue_VALUE(']'); return 4; } return 3; }
        tõrge_VALUE("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void Lisa_vorming(int TYPE_VALUE) {
        if (TYPE_VALUE == 0) Lisa_SMS('V');
        if (TYPE_VALUE == 1) Lisa_SMS('I');
        if (TYPE_VALUE == 2) Lisa_SMS('Z');
        if (TYPE_VALUE == 3) Lisa_Word("Ljava/lang/String;");
        if (TYPE_VALUE == 4) Lisa_Word("[Ljava/lang/String;");
        if (TYPE_VALUE == 5) Lisa_SMS('C');
        if (TYPE_VALUE == 6) Lisa_Word("Ljava/io/FileInputStream;");
        if (TYPE_VALUE == 7) Lisa_Word("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws deklaratsioon. erand Joonis_VALUE_kirje 본문은 host javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = TAKE_Word("Eesti");
        if (한국어묶음) { nõue_VALUE('.'); 말요구("oma"); nõue_VALUE('.'); }
        if (!한국어묶음 && (TAKE_Word("Exception") || TAKE_Word("IOException"))) return;
        if (TAKE_Word("erand") || TAKE_Word("실행예외") || TAKE_Word("I_O_erand") || TAKE_Word("Oota_TIMEOUT_erand") || TAKE_Word("ADDRESS_LOOKUP_erand") || TAKE_Word("파일없음예외") || TAKE_Word("통신예외") || TAKE_Word("kehtetu_argument_erand") || TAKE_Word("number_vorming_tõrge") || TAKE_Word("범위예외") || TAKE_Word("배열범위예외") || TAKE_Word("문자열범위예외") || TAKE_Word("NULL_viide_erand") || TAKE_Word("산술예외") || TAKE_Word("Olek_erand") || TAKE_Word("TYPE_esitama_erand") || TAKE_Word("음수배열크기예외") || TAKE_Word("ARRAY_salv_tõrge") || TAKE_Word("lõim_Olek_erand") || TAKE_Word("대기중단예외")) return;
        tõrge_VALUE("unsupported throws type");
    }
    static void 선언읽기() {
        while (TAKE_Word("import")) {
            if (Word_VALUE(Asukoht, "Eesti")) 예외이름읽기();
            else {
                말요구("java"); nõue_VALUE('.'); 말요구("io"); nõue_VALUE('.');
                if (!(TAKE_Word("FileInputStream") || TAKE_Word("FileOutputStream") || TAKE_Word("IOException"))) tõrge_VALUE("unsupported import");
            }
            nõue_VALUE(';');
        }
        TAKE_Word("public"); TAKE_Word("final"); 말요구("class"); tund_luba = identifikaator_VALUE();
        tund_konstant = viide(7, luba_konstant(tund_luba), 0);
        ema_konstant = viide(7, Word_konstant("java/lang/Object"), 0); CODE_konstant = Word_konstant("Code"); nõue_VALUE('{');
        while (!VIGA && 종류() != '}') {
            if (meetod_COUNT == 32) { tõrge_VALUE("too many methods"); break; }
            int pöördus_kirje = TAKE_Word("public") ? 1 : TAKE_Word("private") ? 2 : 0; 말요구("static");
            int FUNCTION_VALUE = meetod_COUNT++;
            meetod_pöördus[FUNCTION_VALUE] = pöördus_kirje | 8;
            meetod_tagasi_saatma[FUNCTION_VALUE] = vorming_VALUE(); meetod_kirje_nimetus[FUNCTION_VALUE] = identifikaator_VALUE(); nõue_VALUE('(');
            for (int esikaamera_VALUE = 0; esikaamera_VALUE < FUNCTION_VALUE; esikaamera_VALUE++) if (이름같음(meetod_kirje_nimetus[esikaamera_VALUE], meetod_kirje_nimetus[FUNCTION_VALUE])) tõrge_VALUE("duplicate method (overloading unsupported)");
            while (!VIGA && 종류() != ')') {
                int number = meetod_argument_COUNT[FUNCTION_VALUE];
                if (number == 16) { tõrge_VALUE("too many parameters"); break; }
                int TYPE_VALUE = vorming_VALUE(); if (TYPE_VALUE == 0) tõrge_VALUE("void parameter");
                meetod_argument_TYPE[FUNCTION_VALUE * 16 + number] = TYPE_VALUE; meetod_argument_nimetus[FUNCTION_VALUE * 16 + number] = identifikaator_VALUE();
                meetod_argument_COUNT[FUNCTION_VALUE]++;
                if (!saama(',')) break;
            }
            nõue_VALUE(')');
            if (TAKE_Word("throws")) {
                do { 예외이름읽기(); } while (!VIGA && saama(','));
            }
            meetod_sisu[FUNCTION_VALUE] = Asukoht; nõue_VALUE('{');
            int pesastus_VALUE = 1;
            while (Asukoht < luba_COUNT && pesastus_VALUE > 0) {
                if (종류() == '{') pesastus_VALUE++;
                if (종류() == '}') pesastus_VALUE--;
                Asukoht++;
            }
            if (pesastus_VALUE != 0) tõrge_VALUE("unclosed method body");
            meetod_lõpeta_kõne[FUNCTION_VALUE] = Asukoht;
            meetod_nimetus_konstant[FUNCTION_VALUE] = luba_konstant(meetod_kirje_nimetus[FUNCTION_VALUE]);
            문자수 = 0; Lisa_SMS('(');
            for (int number = 0; number < meetod_argument_COUNT[FUNCTION_VALUE]; number++) Lisa_vorming(meetod_argument_TYPE[FUNCTION_VALUE * 16 + number]);
            Lisa_SMS(')'); Lisa_vorming(meetod_tagasi_saatma[FUNCTION_VALUE]); 함수서술[FUNCTION_VALUE] = märk_konstant();
        }
        nõue_VALUE('}'); if (Asukoht != luba_COUNT) tõrge_VALUE("extra input after class");
    }
    static int FIND_kohalik(int Nimi_2) {
        for (int number = kohalik_COUNT - 1; number >= 0; number--) if (지역깊이[number] >= 0 && 이름같음(kohalik_nimetus[number], Nimi_2)) return number;
        tõrge_VALUE("unknown variable"); return 0;
    }
    static int Lisa_kohalik(int Nimi_2, int TYPE_VALUE) {
        for (int number = 0; number < kohalik_COUNT; number++) if (지역깊이[number] >= 0 && 이름같음(kohalik_nimetus[number], Nimi_2)) tõrge_VALUE("duplicate local variable");
        if (kohalik_COUNT == 128) { tõrge_VALUE("too many locals"); return 0; }
        kohalik_nimetus[kohalik_COUNT] = Nimi_2; kohalik_TYPE[kohalik_COUNT] = TYPE_VALUE; 지역깊이[kohalik_COUNT] = 깊이;
        return kohalik_COUNT++;
    }
    static boolean täisarv_TYPE(int TYPE_VALUE) { return TYPE_VALUE == 1 || TYPE_VALUE == 5; }
    static void 지역읽기(int number) { 내보내기(kohalik_TYPE[number] <= 2 || kohalik_TYPE[number] == 5 ? 21 : 25); 내보내기(number); }
    static void kirjutamine_kohalik(int number) { 내보내기(kohalik_TYPE[number] <= 2 || kohalik_TYPE[number] == 5 ? 54 : 58); 내보내기(number); }
    static void kinnitama_TYPE(int tegelik_andmed, int 기대) { if (tegelik_andmed != 기대 && !(tegelik_andmed == 5 && 기대 == 1)) tõrge_VALUE("type mismatch"); }
    static void 문자읽기(int luba_VALUE_eb540501) {
        문자수 = 0; int Käivita_2 = luba_ametikoht[luba_VALUE_eb540501] + 1, 끝 = luba_ametikoht[luba_VALUE_eb540501] + 토큰길이[luba_VALUE_eb540501] - 1;
        while (Käivita_2 < 끝 && !VIGA) {
            int VALUE = ALLIKAS[Käivita_2++];
            if (VALUE == '\\') {
                if (Käivita_2 == 끝) { tõrge_VALUE("invalid escape"); break; }
                VALUE = ALLIKAS[Käivita_2++];
                if (VALUE == 'n') VALUE = 10;
                else if (VALUE == 'r') VALUE = 13;
                else if (VALUE == 't') VALUE = 9;
                else if (VALUE == 'b') VALUE = 8;
                else if (VALUE == 'f') VALUE = 12;
                else if (VALUE != '\\' && VALUE != '"' && VALUE != '\'') tõrge_VALUE("unsupported escape");
            }
            Lisa_SMS(VALUE);
        }
    }
    static int sõeluma_täisarv(int luba_VALUE_eb540501, boolean 음수) {
        if (토큰길이[luba_VALUE_eb540501] > 1 && ALLIKAS[luba_ametikoht[luba_VALUE_eb540501]] == '0') tõrge_VALUE("octal literals unsupported");
        int VALUE = 0;
        for (int number = 0; number < 토큰길이[luba_VALUE_eb540501]; number++) {
            int number_kaup = ALLIKAS[luba_ametikoht[luba_VALUE_eb540501] + number] - '0';
            if (VALUE < -214748364 || VALUE == -214748364 && number_kaup > (음수 ? 8 : 7)) tõrge_VALUE("integer literal out of range");
            VALUE = VALUE * 10 - number_kaup;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static int 기본식() {
        if (TAKE_Word("new")) {
            int TYPE_VALUE = vorming_VALUE();
            if (TYPE_VALUE != 6 && TYPE_VALUE != 7) { tõrge_VALUE("only file streams supported by new in source"); return 0; }
            String omanik_VALUE = TYPE_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            Käsk(187, viide(7, Word_konstant(omanik_VALUE), 0)); 내보내기(89);
            nõue_VALUE('('); kinnitama_TYPE(avaldis_VALUE(), 3); boolean 이어 = false;
            if (saama(',')) { if (TYPE_VALUE != 7) tõrge_VALUE("input stream constructor arguments"); kinnitama_TYPE(avaldis_VALUE(), 2); 이어 = true; }
            nõue_VALUE(')');
            Käsk(183, väline_viide(10, omanik_VALUE, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return TYPE_VALUE;
        }
        if (saama('(')) { int TYPE_VALUE = avaldis_VALUE(); nõue_VALUE(')'); return TYPE_VALUE; }
        if (종류() == 257) { 수상수(sõeluma_täisarv(Asukoht++, false)); return 1; }
        if (종류() == 258) { 문자읽기(Asukoht++); Käsk(19, viide(8, märk_konstant(), 0)); return 3; }
        if (종류() == 259) { 문자읽기(Asukoht++); if (문자수 != 1) tõrge_VALUE("character literal length"); 수상수(문자[0]); return 5; }
        if (TAKE_Word("true")) { 내보내기(4); return 2; }
        if (TAKE_Word("false")) { 내보내기(3); return 2; }
        if (TAKE_Word("Eesti")) {
            nõue_VALUE('.'); 말요구("oma"); nõue_VALUE('.');
            String omanik_VALUE = "", meetod_VALUE = "", 서술 = ""; int 가 = 0, SECOND_operand = 0, 다 = 0, 라 = 0, 마 = 0, TULEMUS = 0;
            if (TAKE_Word("Väljund")) {
                omanik_VALUE = "Eesti/oma/Väljund"; nõue_VALUE('.');
                if (TAKE_Word("kirjutamine_liin")) { meetod_VALUE = "kirjutamine_liin"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("Kirjutamine")) { meetod_VALUE = "Kirjutamine"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("kirjutamine_number")) { meetod_VALUE = "kirjutamine_number"; 서술 = "(I)V"; 가 = 1; }
                else tõrge_VALUE("unknown Korean output method");
            } else if (TAKE_Word("문자")) {
                omanik_VALUE = "Eesti/oma/문자"; nõue_VALUE('.'); 가 = 3;
                if (TAKE_Word("길이")) { meetod_VALUE = "길이"; 서술 = "(Ljava/lang/String;)I"; TULEMUS = 1; }
                else if (TAKE_Word("koodipunkt_COUNT")) { meetod_VALUE = "koodipunkt_COUNT"; 서술 = "(Ljava/lang/String;)I"; TULEMUS = 1; }
                else if (TAKE_Word("sõeluma_täisarv")) { meetod_VALUE = "sõeluma_täisarv"; 서술 = "(Ljava/lang/String;)I"; TULEMUS = 1; }
                else if (TAKE_Word("kirjutamine_täisarv_VALUE")) { meetod_VALUE = "kirjutamine_täisarv_VALUE"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; TULEMUS = 3; }
                else if (TAKE_Word("같음")) { meetod_VALUE = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; SECOND_operand = 3; TULEMUS = 2; }
                else if (TAKE_Word("kleepima_SMS")) { meetod_VALUE = "kleepima_SMS"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; SECOND_operand = 3; TULEMUS = 3; }
                else if (TAKE_Word("lõikama_VALUE")) { meetod_VALUE = "lõikama_VALUE"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; SECOND_operand = 1; 다 = 1; TULEMUS = 3; }
                else tõrge_VALUE("unknown Korean text method");
            } else if (TAKE_Word("Fail")) {
                omanik_VALUE = "Eesti/oma/Fail"; nõue_VALUE('.'); 가 = 3;
                if (TAKE_Word("Lugemine")) { meetod_VALUE = "Lugemine"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; TULEMUS = 3; }
                else if (TAKE_Word("Kirjutamine")) { meetod_VALUE = "Kirjutamine"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; SECOND_operand = 3; }
                else tõrge_VALUE("unknown Korean file method");
            } else if (TAKE_Word("화면")) {
                omanik_VALUE = "Eesti/oma/화면"; nõue_VALUE('.');
                if (TAKE_Word("너비")) { meetod_VALUE = "너비"; 서술 = "()I"; TULEMUS = 1; }
                else if (TAKE_Word("높이")) { meetod_VALUE = "높이"; 서술 = "()I"; TULEMUS = 1; }
                else if (TAKE_Word("ristkülik")) { meetod_VALUE = "ristkülik"; 서술 = "(IIIII)V"; 가 = 1; SECOND_operand = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (TAKE_Word("kustutama_kirje")) { meetod_VALUE = "kustutama_kirje"; 서술 = "(I)V"; 가 = 1; }
                else if (TAKE_Word("기다리기")) { meetod_VALUE = "기다리기"; 서술 = "()V"; }
                else tõrge_VALUE("unknown Korean framebuffer method");
            } else tõrge_VALUE("unsupported Korean library class");
            nõue_VALUE('('); if (가 != 0) kinnitama_TYPE(avaldis_VALUE(), 가);
            if (SECOND_operand != 0) { nõue_VALUE(','); kinnitama_TYPE(avaldis_VALUE(), SECOND_operand); }
            if (다 != 0) { nõue_VALUE(','); kinnitama_TYPE(avaldis_VALUE(), 다); }
            if (라 != 0) { nõue_VALUE(','); kinnitama_TYPE(avaldis_VALUE(), 라); }
            if (마 != 0) { nõue_VALUE(','); kinnitama_TYPE(avaldis_VALUE(), 마); }
            nõue_VALUE(')'); Käsk(184, väline_viide(10, omanik_VALUE, meetod_VALUE, 서술)); return TULEMUS;
        }
        if (TAKE_Word("Integer")) {
            nõue_VALUE('.'); 말요구("parseInt"); nõue_VALUE('('); kinnitama_TYPE(avaldis_VALUE(), 3); nõue_VALUE(')');
            Käsk(184, väline_viide(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Nimi_2 = identifikaator_VALUE();
        if (saama('(')) {
            int FUNCTION_VALUE = -1;
            for (int number = 0; number < meetod_COUNT; number++) if (이름같음(Nimi_2, meetod_kirje_nimetus[number])) FUNCTION_VALUE = number;
            if (FUNCTION_VALUE < 0) { tõrge_VALUE("unknown static method"); return 0; }
            int number = 0;
            while (!VIGA && 종류() != ')') {
                if (number >= meetod_argument_COUNT[FUNCTION_VALUE]) { tõrge_VALUE("too many arguments"); break; }
                kinnitama_TYPE(avaldis_VALUE(), meetod_argument_TYPE[FUNCTION_VALUE * 16 + number++]); if (!saama(',')) break;
            }
            nõue_VALUE(')'); if (number != meetod_argument_COUNT[FUNCTION_VALUE]) tõrge_VALUE("argument count mismatch");
            Käsk(184, viide(10, tund_konstant, viide(12, meetod_nimetus_konstant[FUNCTION_VALUE], 함수서술[FUNCTION_VALUE])));
            return meetod_tagasi_saatma[FUNCTION_VALUE];
        }
        int kohalik_skoop = FIND_kohalik(Nimi_2), TYPE_VALUE = kohalik_TYPE[kohalik_skoop]; 지역읽기(kohalik_skoop);
        while (!VIGA) {
            if (saama('[')) { kinnitama_TYPE(TYPE_VALUE, 4); kinnitama_TYPE(avaldis_VALUE(), 1); nõue_VALUE(']'); 내보내기(50); TYPE_VALUE = 3; }
            else if (saama('.')) {
                if (TYPE_VALUE == 6 || TYPE_VALUE == 7) {
                    String omanik_VALUE = TYPE_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (TAKE_Word("close")) { nõue_VALUE('('); nõue_VALUE(')'); Käsk(182, väline_viide(10, omanik_VALUE, "close", "()V")); TYPE_VALUE = 0; }
                    else if (TYPE_VALUE == 6 && TAKE_Word("read")) { nõue_VALUE('('); nõue_VALUE(')'); Käsk(182, väline_viide(10, omanik_VALUE, "read", "()I")); TYPE_VALUE = 1; }
                    else if (TYPE_VALUE == 7 && TAKE_Word("write")) { nõue_VALUE('('); kinnitama_TYPE(avaldis_VALUE(), 1); nõue_VALUE(')'); Käsk(182, väline_viide(10, omanik_VALUE, "write", "(I)V")); TYPE_VALUE = 0; }
                    else { tõrge_VALUE("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (TYPE_VALUE == 4) { 내보내기(190); TYPE_VALUE = 1; }
                else { kinnitama_TYPE(TYPE_VALUE, 3); nõue_VALUE('('); nõue_VALUE(')'); Käsk(182, väline_viide(10, "java/lang/String", "length", "()I")); TYPE_VALUE = 1; }
            } else break;
        }
        return TYPE_VALUE;
    }
    static int 단항() {
        if (++식깊이 > 64) { tõrge_VALUE("expression nesting too deep"); 식깊이--; return 0; }
        int TYPE_VALUE;
        if (saama('!')) { kinnitama_TYPE(단항(), 2); Võrdlus_VALUE(153); TYPE_VALUE = 2; }
        else if (saama('-')) {
            if (종류() == 257) 수상수(sõeluma_täisarv(Asukoht++, true));
            else { kinnitama_TYPE(단항(), 1); 내보내기(116); }
            TYPE_VALUE = 1;
        } else if (saama('+')) { kinnitama_TYPE(단항(), 1); TYPE_VALUE = 1; }
        else TYPE_VALUE = 기본식();
        식깊이--; return TYPE_VALUE;
    }
    static int 곱식() {
        int TYPE_VALUE = 단항();
        while (!VIGA && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int kodeerimine_VALUE = 종류(); Asukoht++; kinnitama_TYPE(TYPE_VALUE, 1); kinnitama_TYPE(단항(), 1);
            내보내기(kodeerimine_VALUE == '*' ? 104 : kodeerimine_VALUE == '/' ? 108 : 112); TYPE_VALUE = 1;
        }
        return TYPE_VALUE;
    }
    static int 합식() {
        int TYPE_VALUE = 곱식();
        while (!VIGA && (종류() == '+' || 종류() == '-')) {
            int kodeerimine_VALUE = 종류(); Asukoht++; int 경계 = CODE_suurust_muutma, Tagasi_VALUE_TYPE = 곱식();
            if (kodeerimine_VALUE == '+' && (TYPE_VALUE == 3 || Tagasi_VALUE_TYPE == 3)) { 결합(경계, TYPE_VALUE, Tagasi_VALUE_TYPE); TYPE_VALUE = 3; }
            else { kinnitama_TYPE(TYPE_VALUE, 1); kinnitama_TYPE(Tagasi_VALUE_TYPE, 1); 내보내기(kodeerimine_VALUE == '+' ? 96 : 100); TYPE_VALUE = 1; }
        }
        return TYPE_VALUE;
    }
    static int 붙임참조(int TYPE_VALUE) {
        if (TYPE_VALUE != 1 && TYPE_VALUE != 2 && TYPE_VALUE != 3 && TYPE_VALUE != 5) tõrge_VALUE("unsupported concatenation type");
        return väline_viide(10, "java/lang/StringBuilder", "append", TYPE_VALUE == 1 ? "(I)Ljava/lang/StringBuilder;"
            : TYPE_VALUE == 2 ? "(Z)Ljava/lang/StringBuilder;" : TYPE_VALUE == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int 경계, int esikaamera_VALUE_TYPE, int Tagasi_VALUE_TYPE) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 RIGHT CODE_VALUE 앞에 genereerima 코드를 삽입한다.
        // RIGHT avaldis_VALUE 내부의 partner_VALUE haru 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = CODE_suurust_muutma;
        Käsk(187, viide(7, Word_konstant("java/lang/StringBuilder"), 0)); 내보내기(89);
        Käsk(183, väline_viide(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); Käsk(182, 붙임참조(esikaamera_VALUE_TYPE));
        if (VIGA) return;
        int 길이 = CODE_suurust_muutma - 끝;
        for (int number = 0; number < 길이; number++) 삽입코드[number] = CODE_VALUE[끝 + number];
        for (int number = 끝 - 1; number >= 경계; number--) CODE_VALUE[number + 길이] = CODE_VALUE[number];
        for (int number = 0; number < 길이; number++) CODE_VALUE[경계 + number] = 삽입코드[number];
        Käsk(182, 붙임참조(Tagasi_VALUE_TYPE)); Käsk(182, väline_viide(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int Võrdlus_avaldis() {
        int TYPE_VALUE = 합식();
        while (!VIGA && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int kodeerimine_VALUE = 종류(); Asukoht++; kinnitama_TYPE(TYPE_VALUE, 1); kinnitama_TYPE(합식(), 1);
            Võrdlus_VALUE(kodeerimine_VALUE == '<' ? 161 : kodeerimine_VALUE == '>' ? 163 : kodeerimine_VALUE == 302 ? 164 : 162); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int 동등식() {
        int TYPE_VALUE = Võrdlus_avaldis();
        while (!VIGA && (종류() == 300 || 종류() == 301)) {
            int kodeerimine_VALUE = 종류(); Asukoht++; int Tagasi_VALUE_TYPE = Võrdlus_avaldis();
            if (TYPE_VALUE == 0 || Tagasi_VALUE_TYPE == 0) tõrge_VALUE("void expression");
            if (!(täisarv_TYPE(TYPE_VALUE) && täisarv_TYPE(Tagasi_VALUE_TYPE))) kinnitama_TYPE(Tagasi_VALUE_TYPE, TYPE_VALUE);
            Võrdlus_VALUE((TYPE_VALUE <= 2 || TYPE_VALUE == 5 ? 159 : 165) + (kodeerimine_VALUE == 301 ? 1 : 0)); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int NING() {
        int TYPE_VALUE = 동등식();
        while (!VIGA && saama(304)) {
            kinnitama_TYPE(TYPE_VALUE, 2); int 가 = haru(153); kinnitama_TYPE(동등식(), 2); int SECOND_operand = haru(153);
            내보내기(4); int 끝 = haru(167); Link_VALUE(가, CODE_suurust_muutma); Link_VALUE(SECOND_operand, CODE_suurust_muutma); 내보내기(3); Link_VALUE(끝, CODE_suurust_muutma); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int avaldis_VALUE() {
        int TYPE_VALUE = NING();
        while (!VIGA && saama(305)) {
            kinnitama_TYPE(TYPE_VALUE, 2); int 가 = haru(154); kinnitama_TYPE(NING(), 2); int SECOND_operand = haru(154);
            내보내기(3); int 끝 = haru(167); Link_VALUE(가, CODE_suurust_muutma); Link_VALUE(SECOND_operand, CODE_suurust_muutma); 내보내기(4); Link_VALUE(끝, CODE_suurust_muutma); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static void ülesanne_VALUE(boolean Luba_deklaratsioon) {
        if (Word_VALUE(Asukoht, "int") || Word_VALUE(Asukoht, "boolean") || Word_VALUE(Asukoht, "String") || Word_VALUE(Asukoht, "char")
            || Word_VALUE(Asukoht, "FileInputStream") || Word_VALUE(Asukoht, "FileOutputStream")) {
            if (!Luba_deklaratsioon) tõrge_VALUE("declaration not allowed here");
            int TYPE_VALUE = vorming_VALUE(), Nimi_2 = identifikaator_VALUE(); nõue_VALUE('='); kinnitama_TYPE(avaldis_VALUE(), TYPE_VALUE);
            kirjutamine_kohalik(Lisa_kohalik(Nimi_2, TYPE_VALUE)); return;
        }
        int Nimi_2 = identifikaator_VALUE(), kohalik_skoop = FIND_kohalik(Nimi_2);
        if (saama('=')) { kinnitama_TYPE(avaldis_VALUE(), kohalik_TYPE[kohalik_skoop]); kirjutamine_kohalik(kohalik_skoop); }
        else if (종류() >= 308 && 종류() <= 312) {
            int kodeerimine_VALUE = 종류(); Asukoht++; 지역읽기(kohalik_skoop); int 경계 = CODE_suurust_muutma, Tagasi_VALUE_TYPE = avaldis_VALUE();
            if (kodeerimine_VALUE == 308 && kohalik_TYPE[kohalik_skoop] == 3) 결합(경계, 3, Tagasi_VALUE_TYPE);
            else {
                kinnitama_TYPE(kohalik_TYPE[kohalik_skoop], 1); kinnitama_TYPE(Tagasi_VALUE_TYPE, 1);
                내보내기(kodeerimine_VALUE == 308 ? 96 : kodeerimine_VALUE == 309 ? 100 : kodeerimine_VALUE == 310 ? 104 : kodeerimine_VALUE == 311 ? 108 : 112);
                if (kohalik_TYPE[kohalik_skoop] == 5) 내보내기(146);
            }
            kirjutamine_kohalik(kohalik_skoop);
        }
        else if (종류() == 306 || 종류() == 307) {
            kinnitama_TYPE(kohalik_TYPE[kohalik_skoop], 1); 내보내기(132); 내보내기(kohalik_skoop); 내보내기(종류() == 306 ? 1 : 255); Asukoht++;
            if (kohalik_TYPE[kohalik_skoop] == 5) { 지역읽기(kohalik_skoop); 내보내기(146); kirjutamine_kohalik(kohalik_skoop); }
        } else tõrge_VALUE("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); nõue_VALUE('.'); 말요구("out"); nõue_VALUE('.');
        boolean 줄바꿈 = TAKE_Word("println"); if (!줄바꿈) 말요구("print"); nõue_VALUE('(');
        Käsk(178, väline_viide(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean 빈인수 = 종류() == ')';
        int TYPE_VALUE = 빈인수 ? 0 : avaldis_VALUE(); nõue_VALUE(')'); nõue_VALUE(';');
        String 서술 = TYPE_VALUE == 0 ? "()V" : TYPE_VALUE == 1 ? "(I)V" : TYPE_VALUE == 2 ? "(Z)V" : TYPE_VALUE == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (TYPE_VALUE == 4 || TYPE_VALUE >= 6 || TYPE_VALUE == 0 && (!줄바꿈 || !빈인수)) tõrge_VALUE("unsupported print argument");
        Käsk(182, väline_viide(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean lause_VALUE() {
        if (VIGA) return false;
        if (깊이 > 32) { tõrge_VALUE("statement nesting too deep"); return false; }
        if (saama('{')) {
            깊이++; boolean tagasi_saatma_näitaja = false;
            while (!VIGA && 종류() != '}') { if (tagasi_saatma_näitaja) tõrge_VALUE("unreachable statement"); tagasi_saatma_näitaja = lause_VALUE(); }
            nõue_VALUE('}'); for (int number = 0; number < kohalik_COUNT; number++) if (지역깊이[number] == 깊이) 지역깊이[number] = -1;
            깊이--; return tagasi_saatma_näitaja;
        }
        if (saama(';')) return false;
        if (TAKE_Word("return")) {
            int TYPE_VALUE = 종류() == ';' ? 0 : avaldis_VALUE(); kinnitama_TYPE(TYPE_VALUE, meetod_tagasi_saatma[tähtaja_piires_meetod]); nõue_VALUE(';');
            내보내기(TYPE_VALUE == 0 ? 177 : TYPE_VALUE <= 2 || TYPE_VALUE == 5 ? 172 : 176); return true;
        }
        if (TAKE_Word("if")) {
            nõue_VALUE('('); kinnitama_TYPE(avaldis_VALUE(), 2); nõue_VALUE(')'); int FALSE_VALUE = haru(153);
            깊이++; boolean 가 = meede_lause(); 깊이--;
            if (TAKE_Word("else")) { int 끝 = haru(167); Link_VALUE(FALSE_VALUE, CODE_suurust_muutma); 깊이++; boolean SECOND_operand = meede_lause(); 깊이--; Link_VALUE(끝, CODE_suurust_muutma); return 가 && SECOND_operand; }
            Link_VALUE(FALSE_VALUE, CODE_suurust_muutma); return false;
        }
        if (TAKE_Word("while")) {
            int Käivita_2 = CODE_suurust_muutma; nõue_VALUE('('); kinnitama_TYPE(avaldis_VALUE(), 2); nõue_VALUE(')'); int 끝 = haru(153);
            깊이++; meede_lause(); 깊이--; Link_VALUE(haru(167), Käivita_2); Link_VALUE(끝, CODE_suurust_muutma); return false;
        }
        if (TAKE_Word("for")) {
            깊이++; nõue_VALUE('('); if (종류() != ';') ülesanne_VALUE(true); nõue_VALUE(';');
            int tingimus = CODE_suurust_muutma; if (종류() == ';') 내보내기(4); else kinnitama_TYPE(avaldis_VALUE(), 2); nõue_VALUE(';');
            int 끝 = haru(153), sisu_SMS = haru(167), värskendama = CODE_suurust_muutma;
            if (종류() != ')') ülesanne_VALUE(false); nõue_VALUE(')'); Link_VALUE(haru(167), tingimus); Link_VALUE(sisu_SMS, CODE_suurust_muutma);
            meede_lause(); Link_VALUE(haru(167), värskendama); Link_VALUE(끝, CODE_suurust_muutma);
            for (int number = 0; number < kohalik_COUNT; number++) if (지역깊이[number] == 깊이) 지역깊이[number] = -1;
            깊이--; return false;
        }
        if (Word_VALUE(Asukoht, "System")) { 화면출력(); return false; }
        if (종류() == 256 && Asukoht + 1 < luba_COUNT && (토큰종류[Asukoht + 1] == '(' || 토큰종류[Asukoht + 1] == '.')) {
            int TYPE_VALUE = avaldis_VALUE(); if (TYPE_VALUE != 0) 내보내기(87); nõue_VALUE(';'); return false;
        }
        ülesanne_VALUE(true); nõue_VALUE(';'); return false;
    }
    static boolean meede_lause() {
        if (Word_VALUE(Asukoht, "int") || Word_VALUE(Asukoht, "boolean") || Word_VALUE(Asukoht, "char") || Word_VALUE(Asukoht, "String")
            || Word_VALUE(Asukoht, "FileInputStream") || Word_VALUE(Asukoht, "FileOutputStream")) tõrge_VALUE("local declaration requires braces");
        return lause_VALUE();
    }
    static void 출바(int VALUE) { if (toodang_suurust_muutma == Väljund.length) tõrge_VALUE("class file too large"); else Väljund[toodang_suurust_muutma++] = VALUE & 255; }
    static void 출짧(int VALUE) { 출바(VALUE >> 8); 출바(VALUE); }
    static void 출정(int VALUE) { 출짧(VALUE >>> 16); 출짧(VALUE); }
    static void kirjutamine_tund() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(konstant_COUNT);
        for (int number = 0; number < konstant_suurust_muutma; number++) 출바(konstant_VALUE[number]);
        출짧(0x21); 출짧(tund_konstant); 출짧(ema_konstant); 출짧(0); 출짧(0); 출짧(meetod_COUNT);
        for (int number = 0; number < meetod_COUNT; number++) {
            출짧(meetod_pöördus[number]); 출짧(meetod_nimetus_konstant[number]); 출짧(함수서술[number]); 출짧(1); 출짧(CODE_konstant);
            출정(12 + 함수길이[number]); 출짧(128); 출짧(함수지역[number]); 출정(함수길이[number]);
            for (int 칸 = 0; 칸 < 함수길이[number]; 칸++) 출바(CODE_VALUE[meetod_CODE[number] + 칸]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int Käivita_2() {
        if (kasutaja.인수개수() == 1 && 자바도구.같음(kasutaja.Argumendid(0), "-version")) {
            kasutaja.Kirjutamine("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (kasutaja.인수개수() != 1) { kasutaja.Kirjutamine("Usage: javac FILE.java\n"); return 2; }
        int nimetus_suurust_muutma = 자바도구.Nimi_2(failinimi_SMS, kasutaja.Argumendid(0));
        if (nimetus_suurust_muutma < 6 || nimetus_suurust_muutma > 62 || failinimi_SMS[nimetus_suurust_muutma - 5] != '.' || failinimi_SMS[nimetus_suurust_muutma - 4] != 'j'
            || failinimi_SMS[nimetus_suurust_muutma - 3] != 'a' || failinimi_SMS[nimetus_suurust_muutma - 2] != 'v' || failinimi_SMS[nimetus_suurust_muutma - 1] != 'a') {
            kasutaja.Kirjutamine("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        lähe_suurust_muutma = kasutaja.파일읽기(failinimi_SMS, ALLIKAS);
        if (lähe_suurust_muutma < 0) { kasutaja.Kirjutamine("javac: cannot read source: "); 자바도구.kirjutamine_number(lähe_suurust_muutma); kasutaja.kirjutamine_märk_VALUE(10); return 1; }
        lähe_suurust_muutma = 자바도구.원문해독(ALLIKAS, lähe_suurust_muutma);
        if (lähe_suurust_muutma < 0) { kasutaja.Kirjutamine("javac error: invalid UTF-8 source\n"); return 1; }
        lõikama_VALUE(); if (!VIGA) 선언읽기();
        if (!VIGA) {
            if (토큰길이[tund_luba] != nimetus_suurust_muutma - 5) tõrge_VALUE("class name must match file name");
            for (int number = 0; number < nimetus_suurust_muutma - 5; number++) if (ALLIKAS[luba_ametikoht[tund_luba] + number] != failinimi_SMS[number]) tõrge_VALUE("class name must match file name");
        }
        for (tähtaja_piires_meetod = 0; tähtaja_piires_meetod < meetod_COUNT && !VIGA; tähtaja_piires_meetod++) {
            Asukoht = meetod_sisu[tähtaja_piires_meetod]; meetod_CODE[tähtaja_piires_meetod] = CODE_suurust_muutma; kohalik_COUNT = 0; 깊이 = 0;
            for (int number = 0; number < meetod_argument_COUNT[tähtaja_piires_meetod]; number++) Lisa_kohalik(meetod_argument_nimetus[tähtaja_piires_meetod * 16 + number], meetod_argument_TYPE[tähtaja_piires_meetod * 16 + number]);
            boolean tagasi_saatma_näitaja = lause_VALUE();
            if (!tagasi_saatma_näitaja && meetod_tagasi_saatma[tähtaja_piires_meetod] != 0) tõrge_VALUE("missing return");
            // haru 뒤의 합류 지점은 반드시 tegelik_andmed 명령이어야 한다 (버전 49 검증기).
            if (meetod_tagasi_saatma[tähtaja_piires_meetod] == 0) 내보내기(177);
            else { boolean täisarv = meetod_tagasi_saatma[tähtaja_piires_meetod] <= 2 || meetod_tagasi_saatma[tähtaja_piires_meetod] == 5; 내보내기(täisarv ? 3 : 1); 내보내기(täisarv ? 172 : 176); }
            if (Asukoht != meetod_lõpeta_kõne[tähtaja_piires_meetod]) tõrge_VALUE("invalid method body");
            함수지역[tähtaja_piires_meetod] = kohalik_COUNT; 함수길이[tähtaja_piires_meetod] = CODE_suurust_muutma - meetod_CODE[tähtaja_piires_meetod];
        }
        if (VIGA) return 1;
        kirjutamine_tund(); if (VIGA) return 1;
        failinimi_SMS[nimetus_suurust_muutma - 4] = 'c'; failinimi_SMS[nimetus_suurust_muutma - 3] = 'l'; failinimi_SMS[nimetus_suurust_muutma - 2] = 'a';
        failinimi_SMS[nimetus_suurust_muutma - 1] = 's'; failinimi_SMS[nimetus_suurust_muutma] = 's'; failinimi_SMS[nimetus_suurust_muutma + 1] = 0;
        int TULEMUS = kasutaja.kirjutamine_Fail(failinimi_SMS, Väljund, toodang_suurust_muutma);
        if (TULEMUS < 0) { kasutaja.Kirjutamine("javac: cannot save class: "); 자바도구.kirjutamine_number(TULEMUS); kasutaja.kirjutamine_märk_VALUE(10); return 1; }
        kasutaja.Kirjutamine("Compiled: "); for (int number = 0; failinimi_SMS[number] != 0; number++) kasutaja.kirjutamine_märk_VALUE(failinimi_SMS[number]);
        kasutaja.Kirjutamine(" (JVM class version 49)\n"); return 0;
    }
}
