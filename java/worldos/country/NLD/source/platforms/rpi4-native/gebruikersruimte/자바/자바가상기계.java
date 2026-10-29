// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. bestand/operand_stack/verwijzen/branch 경계를 Uitvoeren_opdracht 중 검사한다. */
public final class 자바가상기계 {
    static int[] bestand = new int[16 * 16384], tijdelijk_bestand = new int[16384], bestandsnaam_sms = new int[512];
    static int[] constante_tag = new int[8192], 상가 = new int[8192], constante_SECONDE_WAARDE = new int[8192], tekenreeks_verwijzen = new int[8192];
    static int[] methode_naam_sms = new int[512], methode_TYPE = new int[512], methode_toegang = new int[512], methode_eigenaar = new int[512];
    static int[] methode_START = new int[512], methode_beëindigen = new int[512], methode_stack = new int[512], 함수지역 = new int[512];
    static int[] methode_argument_AANTAL = new int[512], methode_argument_TYPE = new int[8192], methode_Retour = new int[512];
    static int[] grens_WAARDE = new int[16 * 16384];
    static int[] lokaal_WAARDE = new int[16384], lokaal_TYPE = new int[16384], operand_stack_WAARDE = new int[16384], operand_stack_TYPE = new int[16384];
    static int[] frame_methode = new int[128], frame_functie = new int[128], frame_stack = new int[128], frame_instructie = new int[128], initialiseren_frame = new int[128];
    static int[] les_Definitie_naam = new int[16], les_Definitie_formaat_wijzigen = new int[16], les_Definitie_bovenliggend = new int[16], les_Definitie_Status = new int[16], les_sleuf_AANTAL = new int[16], initialiseren_les_Definitie = new int[16];
    static int[] les_interface = new int[16 * 16], les_interface_AANTAL = new int[16];
    static int[] sleuf_naam = new int[512], sleuf_TYPE = new int[512], sleuf_eigenaar = new int[512], sleuf_Machtigingen = new int[512], sleuf_functie = new int[512], sleuf_gegevens = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] heap_WAARDE = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], heap_verwijzen = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], matrixelement = new int[32768], Store_geheel_getal = new int[256];
    static int Grootte, 읽기위치, methode_AANTAL, klassenaam, frame_INDEX = -1, heap_beëindigen_functie = 1, Retour_TYPE;
    static int les_Definitie_AANTAL, sleuf_AANTAL, 잡기수, 현재읽는종, 던진객체, 잠시수, weergeven_AANTAL, incasso_AANTAL;
    static int actueel_thread, aantal_threads = 1, invoer_les_Definitie;
    static int[] thread_frame = new int[4], thread_Status = new int[4], thread_object = new int[4], thread_doel = new int[4], 가닥대기 = new int[4];
    static boolean fout, wijzigingsaanvraag;
    static int[] vergrendelen_eigenaar = new int[32768], 잠금깊이 = new int[32768], frame_vergrendelen = new int[128], les_vergrendelen = new int[16], les_thread = new int[16];

    static void fout_WAARDE(String Word_sms) {
        if (fout) return;
        int gebied_CODE = 0;
        if (자바도구.같음(Word_sms, "ArithmeticException: / by zero")) gebied_CODE = 4;
        if (자바도구.같음(Word_sms, "NullPointerException") || 자바도구.같음(Word_sms, "null or invalid array")) gebied_CODE = 5;
        if (자바도구.같음(Word_sms, "ArrayIndexOutOfBoundsException")) gebied_CODE = 7;
        if (자바도구.같음(Word_sms, "StringIndexOutOfBoundsException")) gebied_CODE = 8;
        if (자바도구.같음(Word_sms, "NumberFormatException")) gebied_CODE = 10;
        if (자바도구.같음(Word_sms, "FileNotFoundException: file open failed")) gebied_CODE = 12;
        if (자바도구.같음(Word_sms, "IOException: stream closed") || 자바도구.같음(Word_sms, "IOException: read failed") || 자바도구.같음(Word_sms, "IOException: write failed")) gebied_CODE = 11;
        if (자바도구.같음(Word_sms, "ClassCastException")) gebied_CODE = 14;
        if (자바도구.같음(Word_sms, "NegativeArraySizeException")) gebied_CODE = 15;
        if (gebied_CODE != 0 && frame_INDEX >= 0) { 예외던짐(gebied_CODE, Word_sms); return; }
        gebruikersruimte.Schrijven("JVM error: "); gebruikersruimte.Schrijven(Word_sms); gebruikersruimte.schrijven_teken_WAARDE(10); fout = true;
    }
    static boolean clip(int starten, int tijdsduur_WAARDE) {
        if (starten < 0 || starten >= bestand.length || tijdsduur_WAARDE < 0) return false;
        int les_Definitie = starten / 16384;
        return starten % 16384 <= les_Definitie_formaat_wijzigen[les_Definitie] && tijdsduur_WAARDE <= les_Definitie_formaat_wijzigen[les_Definitie] - starten % 16384;
    }
    static int byte_WAARDE() {
        if (!clip(읽기위치, 1)) { fout_WAARDE("truncated class file"); return 0; }
        return bestand[읽기위치++];
    }
    static int 짧은수() { return byte_WAARDE() << 8 | byte_WAARDE(); }
    static int geheel_getal() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int tijdsduur_WAARDE) { if (!clip(읽기위치, tijdsduur_WAARDE)) fout_WAARDE("invalid attribute size"); else 읽기위치 += tijdsduur_WAARDE; }
    static boolean cheque_constante(int nummer, int soort_WAARDE) {
        if (nummer <= 0 || nummer >= constante_tag.length || constante_tag[nummer] != soort_WAARDE) { fout_WAARDE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean sms_bereik(int starten, int tijdsduur_WAARDE, String Word_sms) {
        if (!clip(starten, tijdsduur_WAARDE)) return false;
        int 읽는자리 = starten, 끝 = starten + tijdsduur_WAARDE;
        for (int lus_INDEX = 0; lus_INDEX < Word_sms.length(); lus_INDEX++) {
            int codepoint = Word_sms.charAt(lus_INDEX);
            if (codepoint > 0 && codepoint < 128) { if (읽는자리 >= 끝 || bestand[읽는자리++] != codepoint) return false; }
            else if (codepoint < 2048) {
                if (읽는자리 + 2 > 끝 || bestand[읽는자리++] != (192 | (codepoint >> 6)) || bestand[읽는자리++] != (128 | (codepoint & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || bestand[읽는자리++] != (224 | (codepoint >> 12)) || bestand[읽는자리++] != (128 | ((codepoint >> 6) & 63)) || bestand[읽는자리++] != (128 | (codepoint & 63))) return false;
        }
        return 읽는자리 == 끝;
    }
    static boolean Word_sms(int constante_WAARDE, String Word_sms) { return cheque_constante(constante_WAARDE, 1) && sms_bereik(상가[constante_WAARDE], constante_SECONDE_WAARDE[constante_WAARDE], Word_sms); }
    static boolean vereffenen_Word(int 가, int SECONDE_operand) {
        if (!cheque_constante(가, 1) || !cheque_constante(SECONDE_operand, 1) || constante_SECONDE_WAARDE[가] != constante_SECONDE_WAARDE[SECONDE_operand]) return false;
        for (int nummer = 0; nummer < constante_SECONDE_WAARDE[가]; nummer++) if (bestand[상가[가] + nummer] != bestand[상가[SECONDE_operand] + nummer]) return false;
        return true;
    }
    static int klassenaam_sms(int nummer) { return cheque_constante(nummer, 7) && cheque_constante(상가[nummer], 1) ? 상가[nummer] : 0; }
    static int verwijzen_naam(int nummer) { return cheque_constante(nummer, 12) && cheque_constante(상가[nummer], 1) ? 상가[nummer] : 0; }
    static int verwijzingstype(int nummer) { return cheque_constante(nummer, 12) && cheque_constante(constante_SECONDE_WAARDE[nummer], 1) ? constante_SECONDE_WAARDE[nummer] : 0; }
    static int 서술형(int 끝, boolean leeg_TYPE) {
        if (읽기위치 >= 끝) { fout_WAARDE("invalid descriptor"); return 0; }
        int WAARDE = byte_WAARDE();
        if (WAARDE == 'V' && leeg_TYPE) return 0;
        if (WAARDE == 'I' || WAARDE == 'B' || WAARDE == 'C' || WAARDE == 'S' || WAARDE == 'Z') return 1;
        if (WAARDE == '[') { 서술형(끝, false); return 2; }
        if (WAARDE == 'L') {
            int starten = 읽기위치;
            while (읽기위치 < 끝 && bestand[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == starten) fout_WAARDE("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        fout_WAARDE("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int FUNCTIE_WAARDE) {
        int Vorige_item = 읽기위치, nummer = methode_TYPE[FUNCTIE_WAARDE];
        if (!cheque_constante(nummer, 1)) return;
        읽기위치 = 상가[nummer]; int 끝 = 읽기위치 + constante_SECONDE_WAARDE[nummer];
        if (byte_WAARDE() != '(') fout_WAARDE("invalid method descriptor");
        int item_AANTAL = 0;
        while (!fout && 읽기위치 < 끝 && bestand[읽기위치] != ')') {
            if (item_AANTAL == 16) { fout_WAARDE("too many method arguments"); break; }
            methode_argument_TYPE[FUNCTIE_WAARDE * 16 + item_AANTAL++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || byte_WAARDE() != ')') fout_WAARDE("invalid method descriptor");
        methode_Retour[FUNCTIE_WAARDE] = 서술형(끝, true); methode_argument_AANTAL[FUNCTIE_WAARDE] = item_AANTAL;
        if (읽기위치 != 끝) fout_WAARDE("invalid method descriptor");
        읽기위치 = Vorige_item;
    }
    static int 상번호() { int WAARDE = 짧은수(); return WAARDE == 0 ? 0 : 현재읽는종 * 512 + WAARDE; }
    static int 명상수() { return methode_eigenaar[frame_methode[frame_INDEX]] * 512 + 명짧(); }
    static void overslaan_kenmerk() {
        int item_AANTAL = 짧은수();
        for (int nummer = 0; nummer < item_AANTAL && !fout; nummer++) { cheque_constante(상번호(), 1); 건너(geheel_getal()); }
    }
    static int opdracht_tijdsduur(int WAARDE) {
        if (WAARDE == 16 || WAARDE == 18 || WAARDE == 21 || WAARDE == 25 || WAARDE == 54 || WAARDE == 58 || WAARDE == 188) return 2;
        if (WAARDE == 17 || WAARDE == 19 || WAARDE == 132 || WAARDE >= 153 && WAARDE <= 167
            || WAARDE >= 178 && WAARDE <= 184 || WAARDE == 187 || WAARDE == 189 || WAARDE == 192 || WAARDE == 193 || WAARDE == 198 || WAARDE == 199) return 3;
        if (WAARDE == 185 || WAARDE == 200) return 5;
        if (WAARDE >= 0 && WAARDE <= 8 || WAARDE >= 26 && WAARDE <= 29 || WAARDE >= 42 && WAARDE <= 46 || WAARDE >= 50 && WAARDE <= 53
            || WAARDE >= 59 && WAARDE <= 62 || WAARDE >= 75 && WAARDE <= 79 || WAARDE >= 83 && WAARDE <= 95
            || WAARDE == 96 || WAARDE == 100 || WAARDE == 104 || WAARDE == 108 || WAARDE == 112 || WAARDE == 116
            || WAARDE == 120 || WAARDE == 122 || WAARDE == 124 || WAARDE == 126 || WAARDE == 128 || WAARDE == 130
            || WAARDE >= 145 && WAARDE <= 147 || WAARDE == 172 || WAARDE == 176 || WAARDE == 177 || WAARDE == 190 || WAARDE == 191
            || WAARDE == 194 || WAARDE == 195) return 1;
        return 0;
    }
    static int functie_geheel_getal(int 읽는자리) {
        if (!clip(읽는자리, 4)) { fout_WAARDE("truncated bytecode operand"); return 0; }
        return bestand[읽는자리] << 24 | bestand[읽는자리 + 1] << 16 | bestand[읽는자리 + 2] << 8 | bestand[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int starten, int 끝) {
        int WAARDE = bestand[읽는자리], tijdsduur_WAARDE = opdracht_tijdsduur(WAARDE);
        if (WAARDE == 170 || WAARDE == 171) {
            int BASIS_functie = 읽는자리 + 1;
            while ((BASIS_functie - starten) % 4 != 0) BASIS_functie++;
            if (끝 - BASIS_functie < (WAARDE == 170 ? 12 : 8)) return 0;
            int invoer_AANTAL_8f7753a1 = WAARDE == 170 ? functie_geheel_getal(BASIS_functie + 8) - functie_geheel_getal(BASIS_functie + 4) + 1 : functie_geheel_getal(BASIS_functie + 4);
            if (invoer_AANTAL_8f7753a1 < 0 || invoer_AANTAL_8f7753a1 > 2048) return 0;
            tijdsduur_WAARDE = BASIS_functie - 읽는자리 + (WAARDE == 170 ? 12 + 4 * invoer_AANTAL_8f7753a1 : 8 + 8 * invoer_AANTAL_8f7753a1);
        }
        if (WAARDE == 196 && 읽는자리 + 1 < 끝) {
            int Word_gegevens = bestand[읽는자리 + 1]; tijdsduur_WAARDE = Word_gegevens == 132 ? 6 : (Word_gegevens == 21 || Word_gegevens == 25 || Word_gegevens == 54 || Word_gegevens == 58) ? 4 : 0;
        }
        return tijdsduur_WAARDE > 0 && tijdsduur_WAARDE <= 끝 - 읽는자리 ? tijdsduur_WAARDE : 0;
    }
    static void cheque_doel_WAARDE(int doel_WAARDE, int FUNCTIE_WAARDE) {
        if (doel_WAARDE < methode_START[FUNCTIE_WAARDE] || doel_WAARDE >= methode_beëindigen[FUNCTIE_WAARDE] || grens_WAARDE[doel_WAARDE] != FUNCTIE_WAARDE + 1) fout_WAARDE("invalid branch target");
    }
    static void 클래스읽기(int les_Definitie) {
        현재읽는종 = les_Definitie; 읽기위치 = les_Definitie * 16384; Grootte = 읽기위치 + les_Definitie_formaat_wijzigen[les_Definitie];
        if (geheel_getal() != 0xcafebabe) { fout_WAARDE("not a class file"); return; }
        int 부판 = 짧은수(), versie_WAARDE = 짧은수();
        if (versie_WAARDE < 45 || versie_WAARDE > 52 || 부판 != 0) { fout_WAARDE("supported class versions: 45..52, minor 0"); return; }
        int constante_AANTAL = 짧은수(), BASIS_functie = les_Definitie * 512;
        if (constante_AANTAL < 1 || constante_AANTAL > 512) { fout_WAARDE("constant pool limit (511)"); return; }
        for (int invoer_AANTAL_8f7753a1 = 1; invoer_AANTAL_8f7753a1 < constante_AANTAL && !fout; invoer_AANTAL_8f7753a1++) {
            int nummer = BASIS_functie + invoer_AANTAL_8f7753a1, soort_WAARDE = byte_WAARDE(); constante_tag[nummer] = soort_WAARDE;
            if (soort_WAARDE == 1) { constante_SECONDE_WAARDE[nummer] = 짧은수(); 상가[nummer] = 읽기위치; 건너(constante_SECONDE_WAARDE[nummer]); }
            else if (soort_WAARDE == 3) 상가[nummer] = geheel_getal();
            else if (soort_WAARDE == 7 || soort_WAARDE == 8) 상가[nummer] = 상번호();
            else if (soort_WAARDE == 9 || soort_WAARDE == 10 || soort_WAARDE == 11 || soort_WAARDE == 12) { 상가[nummer] = 상번호(); constante_SECONDE_WAARDE[nummer] = 상번호(); }
            else fout_WAARDE("unsupported constant type");
        }
        int machtiging_WAARDE = 짧은수();
        if ((machtiging_WAARDE & (0x2000 | 0x4000)) != 0) fout_WAARDE("annotation/enum class unsupported");
        les_Definitie_naam[les_Definitie] = klassenaam_sms(상번호());
        les_Definitie_bovenliggend[les_Definitie] = klassenaam_sms(상번호());
        int interface_AANTAL = 짧은수(); if (interface_AANTAL > 16) { fout_WAARDE("interface count limit"); return; }
        les_interface_AANTAL[les_Definitie] = interface_AANTAL;
        for (int lus_INDEX = 0; lus_INDEX < interface_AANTAL; lus_INDEX++) les_interface[les_Definitie * 16 + lus_INDEX] = klassenaam_sms(상번호());
        int veld_AANTAL = 짧은수();
        if (veld_AANTAL > 512 - sleuf_AANTAL) { fout_WAARDE("field count limit (512)"); return; }
        for (int lus_INDEX = 0; lus_INDEX < veld_AANTAL && !fout; lus_INDEX++) {
            int Bestand_INDEX = sleuf_AANTAL++; sleuf_eigenaar[Bestand_INDEX] = les_Definitie; sleuf_Machtigingen[Bestand_INDEX] = 짧은수(); sleuf_naam[Bestand_INDEX] = 상번호(); sleuf_TYPE[Bestand_INDEX] = 상번호();
            cheque_constante(sleuf_naam[Bestand_INDEX], 1); cheque_constante(sleuf_TYPE[Bestand_INDEX], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[sleuf_TYPE[Bestand_INDEX]]; int gebied_CODE = 서술형(읽기위치 + constante_SECONDE_WAARDE[sleuf_TYPE[Bestand_INDEX]], false); 읽기위치 = 보존값;
            if ((sleuf_Machtigingen[Bestand_INDEX] & 8) == 0) sleuf_functie[Bestand_INDEX] = les_sleuf_AANTAL[les_Definitie]++;
            int kenmerk_gegevens = 짧은수();
            for (int inner_functie = 0; inner_functie < kenmerk_gegevens && !fout; inner_functie++) {
                int naam_constante = 상번호(), geldig_tijdsduur = geheel_getal();
                if (Word_sms(naam_constante, "ConstantValue") && geldig_tijdsduur == 2) {
                    int gegevens_WAARDE = 상번호();
                    if (gebied_CODE == 1 && cheque_constante(gegevens_WAARDE, 3)) sleuf_gegevens[Bestand_INDEX] = 상가[gegevens_WAARDE];
                    else if (gebied_CODE == 2 && cheque_constante(gegevens_WAARDE, 8)) sleuf_gegevens[Bestand_INDEX] = constante_sms(상가[gegevens_WAARDE]);
                } else 건너(geldig_tijdsduur);
            }
        }
        int item_AANTAL = 짧은수();
        if (item_AANTAL > 512 - methode_AANTAL) { fout_WAARDE("method count limit (512)"); return; }
        for (int lus_INDEX = 0; lus_INDEX < item_AANTAL && !fout; lus_INDEX++) {
            int nummer = methode_AANTAL++; methode_eigenaar[nummer] = les_Definitie;
            methode_toegang[nummer] = 짧은수(); methode_naam_sms[nummer] = 상번호(); methode_TYPE[nummer] = 상번호();
            cheque_constante(methode_naam_sms[nummer], 1); 서술읽기(nummer);
            if ((methode_toegang[nummer] & 8) == 0) {
                if (methode_argument_AANTAL[nummer] == 16) { fout_WAARDE("too many instance method arguments"); return; }
                for (int Vergelijking_functie = methode_argument_AANTAL[nummer]; Vergelijking_functie > 0; Vergelijking_functie--) methode_argument_TYPE[nummer * 16 + Vergelijking_functie] = methode_argument_TYPE[nummer * 16 + Vergelijking_functie - 1];
                methode_argument_TYPE[nummer * 16] = 2; methode_argument_AANTAL[nummer]++;
            }
            if ((methode_toegang[nummer] & 0x100) != 0) fout_WAARDE("user native method unsupported");
            if (Word_sms(methode_naam_sms[nummer], "<clinit>")) initialiseren_les_Definitie[les_Definitie] = nummer + 1;
            for (int voorkant_WAARDE = 0; voorkant_WAARDE < nummer; voorkant_WAARDE++) if (methode_eigenaar[voorkant_WAARDE] == les_Definitie && vereffenen_Word(methode_naam_sms[voorkant_WAARDE], methode_naam_sms[nummer]) && vereffenen_Word(methode_TYPE[voorkant_WAARDE], methode_TYPE[nummer])) fout_WAARDE("duplicate method");
            int kenmerk_AANTAL = 짧은수();
            for (int kenmerkwaarde = 0; kenmerkwaarde < kenmerk_AANTAL && !fout; kenmerkwaarde++) {
                int Naam = 상번호(), tijdsduur_WAARDE = geheel_getal(), starten = 읽기위치;
                if (!clip(starten, tijdsduur_WAARDE)) { fout_WAARDE("truncated method attribute"); break; }
                if (Word_sms(Naam, "Code")) {
                    if (methode_START[nummer] != 0) fout_WAARDE("duplicate Code attribute");
                    methode_stack[nummer] = 짧은수(); 함수지역[nummer] = 짧은수(); int CODE_tijdsduur = geheel_getal();
                    if (methode_stack[nummer] > 128 || 함수지역[nummer] > 128 || 함수지역[nummer] < methode_argument_AANTAL[nummer]
                        || CODE_tijdsduur < 1 || CODE_tijdsduur > 8192) fout_WAARDE("method memory limits exceeded");
                    methode_START[nummer] = 읽기위치; 건너(CODE_tijdsduur); methode_beëindigen[nummer] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { fout_WAARDE("exception table limit"); return; }
                    for (int inner_functie = 0; inner_functie < 잡는수; inner_functie++) {
                        int fout_verwijzen = 잡기수++; 잡기함수[fout_verwijzen] = nummer;
                        잡기시작[fout_verwijzen] = methode_START[nummer] + 짧은수(); 잡기끝[fout_verwijzen] = methode_START[nummer] + 짧은수();
                        잡기위치[fout_verwijzen] = methode_START[nummer] + 짧은수(); int 부호값 = 상번호(); 잡기종[fout_verwijzen] = 부호값 == 0 ? 0 : klassenaam_sms(부호값);
                    }
                    overslaan_kenmerk();
                    if (읽기위치 != starten + tijdsduur_WAARDE) fout_WAARDE("Code attribute size mismatch");
                } else 건너(tijdsduur_WAARDE);
            }
            if ((methode_toegang[nummer] & 0x400) != 0) continue;
            if (methode_START[nummer] == 0) fout_WAARDE("missing Code attribute");
            int sleuf_invoer = methode_START[nummer];
            while (sleuf_invoer < methode_beëindigen[nummer] && !fout) {
                int tijdsduur_WAARDE = 길이읽기(sleuf_invoer, methode_START[nummer], methode_beëindigen[nummer]);
                if (tijdsduur_WAARDE == 0) { fout_WAARDE("unsupported or truncated bytecode"); break; }
                grens_WAARDE[sleuf_invoer] = nummer + 1; sleuf_invoer += tijdsduur_WAARDE;
            }
            sleuf_invoer = methode_START[nummer];
            while (sleuf_invoer < methode_beëindigen[nummer] && !fout) {
                int WAARDE = bestand[sleuf_invoer];
                if (WAARDE >= 153 && WAARDE <= 167 || WAARDE == 198 || WAARDE == 199) cheque_doel_WAARDE(sleuf_invoer + (short)(bestand[sleuf_invoer + 1] << 8 | bestand[sleuf_invoer + 2]), nummer);
                if (WAARDE == 200) cheque_doel_WAARDE(sleuf_invoer + functie_geheel_getal(sleuf_invoer + 1), nummer);
                if (WAARDE == 170 || WAARDE == 171) {
                    int 읽는자리 = sleuf_invoer + 1; while ((읽는자리 - methode_START[nummer]) % 4 != 0) 읽는자리++;
                    cheque_doel_WAARDE(sleuf_invoer + functie_geheel_getal(읽는자리), nummer);
                    int invoer_AANTAL_8f7753a1 = WAARDE == 170 ? functie_geheel_getal(읽는자리 + 8) - functie_geheel_getal(읽는자리 + 4) + 1 : functie_geheel_getal(읽는자리 + 4);
                    읽는자리 += WAARDE == 170 ? 12 : 8;
                    for (int inner_functie = 0; inner_functie < invoer_AANTAL_8f7753a1; inner_functie++) cheque_doel_WAARDE(sleuf_invoer + functie_geheel_getal(읽는자리 + inner_functie * (WAARDE == 170 ? 4 : 8) + (WAARDE == 170 ? 0 : 4)), nummer);
                }
                sleuf_invoer += 길이읽기(sleuf_invoer, methode_START[nummer], methode_beëindigen[nummer]);
            }
            for (int inner_functie = 0; inner_functie < 잡기수; inner_functie++) if (잡기함수[inner_functie] == nummer) {
                cheque_doel_WAARDE(잡기시작[inner_functie], nummer); cheque_doel_WAARDE(잡기위치[inner_functie], nummer);
                if (잡기끝[inner_functie] != methode_beëindigen[nummer]) cheque_doel_WAARDE(잡기끝[inner_functie], nummer);
                if (잡기시작[inner_functie] >= 잡기끝[inner_functie]) fout_WAARDE("invalid exception range");
            }
        }
        if (!fout) overslaan_kenmerk();
        if (읽기위치 != Grootte) fout_WAARDE("extra class file data");
    }
    static int toewijzen_Opslag(int soort_WAARDE, int tijdsduur_WAARDE) { return 새기억(soort_WAARDE, tijdsduur_WAARDE); }
    static boolean object_WAARDE(int verwijzen, int soort_WAARDE) {
        if (!informatie_geldig_object(verwijzen)) return false;
        if (heap_WAARDE[verwijzen] != soort_WAARDE) { fout_WAARDE("object type mismatch"); return false; }
        return true;
    }
    static int constante_sms(int INDEX) {
        if (!cheque_constante(INDEX, 1)) return 0;
        if (tekenreeks_verwijzen[INDEX] != 0) return tekenreeks_verwijzen[INDEX];
        int verwijzen = toewijzen_Opslag(1, constante_SECONDE_WAARDE[INDEX]); if (fout) return 0;
        int 끝 = 상가[INDEX] + constante_SECONDE_WAARDE[INDEX], nummer = 상가[INDEX], tijdsduur_WAARDE = 0;
        while (nummer < 끝 && !fout) {
            int WAARDE = bestand[nummer++];
            if (WAARDE == 0) fout_WAARDE("invalid modified UTF-8");
            else if (WAARDE >= 192 && WAARDE <= 223 && nummer < 끝) {
                int Volgende_item = bestand[nummer++];
                if ((Volgende_item & 192) != 128) fout_WAARDE("invalid modified UTF-8");
                WAARDE = (WAARDE & 31) << 6 | Volgende_item & 63;
                if (WAARDE != 0 && WAARDE < 128) fout_WAARDE("overlong modified UTF-8");
            } else if (WAARDE >= 224 && WAARDE <= 239 && nummer + 1 < 끝) {
                int 가 = bestand[nummer++], SECONDE_operand = bestand[nummer++];
                if ((가 & 192) != 128 || (SECONDE_operand & 192) != 128) fout_WAARDE("invalid modified UTF-8");
                WAARDE = (WAARDE & 15) << 12 | (가 & 63) << 6 | SECONDE_operand & 63;
                if (WAARDE < 2048) fout_WAARDE("overlong modified UTF-8");
            } else if (WAARDE >= 128) fout_WAARDE("invalid modified UTF-8");
            heap_WAARDE[verwijzen + 2 + tijdsduur_WAARDE++] = WAARDE;
        }
        heap_WAARDE[verwijzen + 1] = tijdsduur_WAARDE; tekenreeks_verwijzen[INDEX] = verwijzen; return verwijzen;
    }
    static int host_teken(String WAARDE) {
        int verwijzen = toewijzen_Opslag(1, WAARDE.length()); if (fout) return 0;
        for (int nummer = 0; nummer < WAARDE.length(); nummer++) heap_WAARDE[verwijzen + 2 + nummer] = WAARDE.charAt(nummer);
        return verwijzen;
    }
    static void schrijven_sms(int verwijzen) {
        if (verwijzen == 0) { gebruikersruimte.Schrijven("null"); return; }
        if (!object_WAARDE(verwijzen, 1)) return;
        for (int nummer = 0; nummer < heap_WAARDE[verwijzen + 1]; nummer++) gebruikersruimte.schrijven_teken_WAARDE(heap_WAARDE[verwijzen + 2 + nummer]);
    }
    static int cijfer_teken(int WAARDE) {
        int verwijzen = toewijzen_Opslag(1, 11); if (fout) return 0;
        int tijdsduur_WAARDE = 0;
        if (WAARDE < 0) heap_WAARDE[verwijzen + 2 + tijdsduur_WAARDE++] = '-'; else WAARDE = -WAARDE;
        int plaatsingsindex = 1000000000; boolean starten = false;
        while (plaatsingsindex != 0) {
            int nummer = -(WAARDE / plaatsingsindex);
            if (nummer != 0 || starten || plaatsingsindex == 1) { heap_WAARDE[verwijzen + 2 + tijdsduur_WAARDE++] = '0' + nummer; starten = true; }
            WAARDE %= plaatsingsindex; plaatsingsindex /= 10;
        }
        heap_WAARDE[verwijzen + 1] = tijdsduur_WAARDE; return verwijzen;
    }
    static int 정수해독(int verwijzen) {
        if (!object_WAARDE(verwijzen, 1)) return 0;
        int tijdsduur_WAARDE = heap_WAARDE[verwijzen + 1], nummer = 0, WAARDE = 0; boolean 음수 = false;
        if (tijdsduur_WAARDE > 0 && (heap_WAARDE[verwijzen + 2] == '-' || heap_WAARDE[verwijzen + 2] == '+')) { 음수 = heap_WAARDE[verwijzen + 2] == '-'; nummer++; }
        if (nummer == tijdsduur_WAARDE) fout_WAARDE("NumberFormatException");
        for (; nummer < tijdsduur_WAARDE && !fout; nummer++) {
            int cijfer_WAARDE = heap_WAARDE[verwijzen + 2 + nummer] - '0';
            if (cijfer_WAARDE < 0 || cijfer_WAARDE > 9 || WAARDE < -214748364 || WAARDE == -214748364 && cijfer_WAARDE > (음수 ? 8 : 7)) fout_WAARDE("NumberFormatException");
            WAARDE = WAARDE * 10 - cijfer_WAARDE;
        }
        return 음수 ? WAARDE : -WAARDE;
    }
    static void 넣기(int WAARDE, int TYPE_WAARDE) {
        if (fout) return;
        if (frame_INDEX < 0 || frame_stack[frame_INDEX] >= methode_stack[frame_methode[frame_INDEX]]) { fout_WAARDE("operand stack overflow"); return; }
        int sleuf_invoer = frame_INDEX * 128 + frame_stack[frame_INDEX]++; operand_stack_WAARDE[sleuf_invoer] = WAARDE; operand_stack_TYPE[sleuf_invoer] = TYPE_WAARDE;
    }
    static int 빼기(int TYPE_WAARDE) {
        if (fout) return 0;
        if (frame_INDEX < 0 || frame_stack[frame_INDEX] < 1) { fout_WAARDE("operand stack underflow"); return 0; }
        int sleuf_invoer = frame_INDEX * 128 + --frame_stack[frame_INDEX]; Retour_TYPE = operand_stack_TYPE[sleuf_invoer];
        if (TYPE_WAARDE != 0 && Retour_TYPE != TYPE_WAARDE) fout_WAARDE("operand type mismatch");
        if (Retour_TYPE == 2) beschermen_WAARDE(operand_stack_WAARDE[sleuf_invoer]);
        return operand_stack_WAARDE[sleuf_invoer];
    }
    static void 지역읽기(int INDEX, int TYPE_WAARDE) {
        if (INDEX >= 함수지역[frame_methode[frame_INDEX]] || INDEX < 0 || lokaal_TYPE[frame_INDEX * 128 + INDEX] != TYPE_WAARDE) { fout_WAARDE("invalid or uninitialized local"); return; }
        넣기(lokaal_WAARDE[frame_INDEX * 128 + INDEX], TYPE_WAARDE);
    }
    static void schrijven_lokaal(int INDEX, int TYPE_WAARDE) {
        if (INDEX >= 함수지역[frame_methode[frame_INDEX]] || INDEX < 0) { fout_WAARDE("local index out of range"); return; }
        int WAARDE = 빼기(TYPE_WAARDE); lokaal_WAARDE[frame_INDEX * 128 + INDEX] = WAARDE; lokaal_TYPE[frame_INDEX * 128 + INDEX] = TYPE_WAARDE;
    }
    static int 명바() {
        int positie = frame_functie[frame_INDEX];
        if (positie < methode_START[frame_methode[frame_INDEX]] || positie >= methode_beëindigen[frame_methode[frame_INDEX]]) { fout_WAARDE("instruction pointer out of range"); return 0; }
        frame_functie[frame_INDEX]++; return bestand[positie];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void verplaatsen_WAARDE_83b651b8(int positie) {
        int FUNCTIE_WAARDE = frame_methode[frame_INDEX];
        if (positie < methode_START[FUNCTIE_WAARDE] || positie >= methode_beëindigen[FUNCTIE_WAARDE] || grens_WAARDE[positie] != FUNCTIE_WAARDE + 1) fout_WAARDE("invalid branch target");
        else frame_functie[frame_INDEX] = positie;
    }
    static void 호출(int FUNCTIE_WAARDE) {
        if (frame_INDEX % 32 == 31) { fout_WAARDE("call stack limit (32)"); return; }
        int Volgende_item = frame_INDEX + 1;
        for (int nummer = 0; nummer < 128; nummer++) lokaal_TYPE[Volgende_item * 128 + nummer] = 0;
        for (int nummer = methode_argument_AANTAL[FUNCTIE_WAARDE] - 1; nummer >= 0; nummer--) {
            lokaal_WAARDE[Volgende_item * 128 + nummer] = 빼기(methode_argument_TYPE[FUNCTIE_WAARDE * 16 + nummer]); lokaal_TYPE[Volgende_item * 128 + nummer] = methode_argument_TYPE[FUNCTIE_WAARDE * 16 + nummer];
        }
        if (fout) return;
        frame_INDEX = Volgende_item; initialiseren_frame[frame_INDEX] = 0; frame_methode[frame_INDEX] = FUNCTIE_WAARDE; frame_functie[frame_INDEX] = methode_START[FUNCTIE_WAARDE]; frame_stack[frame_INDEX] = 0;
    }
    static void Retour_HR(int TYPE_WAARDE) {
        if (TYPE_WAARDE != methode_Retour[frame_methode[frame_INDEX]]) { fout_WAARDE("return type mismatch"); return; }
        int WAARDE = TYPE_WAARDE == 0 ? 0 : 빼기(TYPE_WAARDE);
        if (initialiseren_frame[frame_INDEX] != 0) les_Definitie_Status[initialiseren_frame[frame_INDEX] - 1] = 2;
        if (frame_vergrendelen[frame_INDEX] != 0) { versie_vergrendelen(frame_vergrendelen[frame_INDEX]); frame_vergrendelen[frame_INDEX] = 0; }
        frame_INDEX--; if (frame_INDEX >= actueel_thread * 32 && TYPE_WAARDE != 0) 넣기(WAARDE, TYPE_WAARDE);
    }
    static int[] Stream_bestandsnaam = new int[64];
    static void Bestand_Stream_Bellen(int eigenaar_WAARDE, int Naam, int opmaak_WAARDE, int opdracht) {
        boolean tekstuitvoer = Word_sms(eigenaar_WAARDE, "java/io/FileOutputStream");
        int soort_WAARDE = tekstuitvoer ? 6 : 5;
        if (opdracht == 183 && Word_sms(Naam, "<init>")) {
            boolean 이어 = false;
            if (tekstuitvoer && Word_sms(opmaak_WAARDE, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Word_sms(opmaak_WAARDE, "(Ljava/lang/String;)V")) { fout_WAARDE("unsupported file stream constructor"); return; }
            int Bestand_invoer_naam = 빼기(2), Stream_WAARDE = 빼기(2);
            if (!object_WAARDE(Bestand_invoer_naam, 1) || !object_WAARDE(Stream_WAARDE, soort_WAARDE) || fout) return;
            if (heap_WAARDE[Stream_WAARDE + 3] != 0) { fout_WAARDE("file stream already initialized"); return; }
            int tijdsduur_WAARDE = heap_WAARDE[Bestand_invoer_naam + 1];
            if (tijdsduur_WAARDE < 1 || tijdsduur_WAARDE > 63) { fout_WAARDE("invalid file name length"); return; }
            for (int sleuf_invoer = 0; sleuf_invoer < tijdsduur_WAARDE; sleuf_invoer++) {
                int WAARDE = heap_WAARDE[Bestand_invoer_naam + 2 + sleuf_invoer];
                if (WAARDE < 1) { fout_WAARDE("invalid file stream path"); return; }
                Stream_bestandsnaam[sleuf_invoer] = WAARDE;
            }
            Stream_bestandsnaam[tijdsduur_WAARDE] = 0;
            int 서술자 = gebruikersruimte.파일서술자열기(Stream_bestandsnaam, tekstuitvoer ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { fout_WAARDE("FileNotFoundException: file open failed"); return; }
            heap_WAARDE[Stream_WAARDE + 2] = 서술자; heap_WAARDE[Stream_WAARDE + 3] = 1;
            return;
        }
        if (opdracht != 182) { fout_WAARDE("invalid file stream invocation"); return; }
        if ((tekstuitvoer && Word_sms(Naam, "write") || !tekstuitvoer && Word_sms(Naam, "read"))
            && (Word_sms(opmaak_WAARDE, tekstuitvoer ? "([B)V" : "([B)I") || Word_sms(opmaak_WAARDE, tekstuitvoer ? "([BII)V" : "([BII)I"))) {
            boolean clip_WAARDE = Word_sms(opmaak_WAARDE, tekstuitvoer ? "([BII)V" : "([BII)I");
            int invoer_AANTAL_8f7753a1 = clip_WAARDE ? 빼기(1) : 0, 시작점 = clip_WAARDE ? 빼기(1) : 0, gegevens_MATRIX = 빼기(2), object_verwijzen = 빼기(2);
            if (!object_WAARDE(gegevens_MATRIX, 20) || !object_WAARDE(object_verwijzen, soort_WAARDE)) return;
            if (!clip_WAARDE) invoer_AANTAL_8f7753a1 = heap_WAARDE[gegevens_MATRIX + 1];
            if (시작점 < 0 || invoer_AANTAL_8f7753a1 < 0 || 시작점 > heap_WAARDE[gegevens_MATRIX + 1] - invoer_AANTAL_8f7753a1) { 예외던짐(6, "file buffer bounds"); return; }
            if (heap_WAARDE[object_verwijzen + 3] == 0 || heap_WAARDE[object_verwijzen + 2] < 0) { fout_WAARDE("IOException: stream closed"); return; }
            int Voltooid_AANTAL = 0;
            while (Voltooid_AANTAL < invoer_AANTAL_8f7753a1 && !fout) {
                int 반환값 = tekstuitvoer ? gebruikersruimte.파일한바이트쓰기(heap_WAARDE[object_verwijzen + 2], heap_WAARDE[gegevens_MATRIX + 2 + 시작점 + Voltooid_AANTAL]) : gebruikersruimte.파일한바이트읽기(heap_WAARDE[object_verwijzen + 2]);
                if (반환값 < 0) { fout_WAARDE(tekstuitvoer ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!tekstuitvoer && 반환값 == 256) break;
                if (!tekstuitvoer) heap_WAARDE[gegevens_MATRIX + 2 + 시작점 + Voltooid_AANTAL] = (byte)반환값;
                Voltooid_AANTAL++;
            }
            if (!tekstuitvoer) 넣기(invoer_AANTAL_8f7753a1 != 0 && Voltooid_AANTAL == 0 ? -1 : Voltooid_AANTAL, 1);
            return;
        }
        if (tekstuitvoer && Word_sms(Naam, "flush") && Word_sms(opmaak_WAARDE, "()V")) { int object_verwijzen = 빼기(2); if (object_WAARDE(object_verwijzen, soort_WAARDE) && heap_WAARDE[object_verwijzen + 2] < 0) fout_WAARDE("IOException: stream closed"); return; }
        int Actie = -1, WAARDE = 0;
        if (Word_sms(Naam, "close") && Word_sms(opmaak_WAARDE, "()V")) Actie = 0;
        if (!tekstuitvoer && Word_sms(Naam, "read") && Word_sms(opmaak_WAARDE, "()I")) Actie = 1;
        if (tekstuitvoer && Word_sms(Naam, "write") && Word_sms(opmaak_WAARDE, "(I)V")) { Actie = 2; WAARDE = 빼기(1); }
        if (Actie < 0) { fout_WAARDE("unsupported file stream method"); return; }
        int Stream_WAARDE = 빼기(2);
        if (!object_WAARDE(Stream_WAARDE, soort_WAARDE) || fout) return;
        if (heap_WAARDE[Stream_WAARDE + 3] == 0) { fout_WAARDE("uninitialized file stream"); return; }
        int 서술자 = heap_WAARDE[Stream_WAARDE + 2];
        if (Actie == 0) {
            if (서술자 >= 0 && gebruikersruimte.파일서술자닫기(서술자) < 0) fout_WAARDE("IOException: close failed");
            heap_WAARDE[Stream_WAARDE + 2] = -1; return;
        }
        if (서술자 < 0) { fout_WAARDE("IOException: stream closed"); return; }
        if (Actie == 1) {
            int resultaat = gebruikersruimte.파일한바이트읽기(서술자);
            if (resultaat < -1) fout_WAARDE("IOException: read failed"); else 넣기(resultaat == 256 ? -1 : resultaat, 1);
        } else if (gebruikersruimte.파일한바이트쓰기(서술자, WAARDE) != 1) fout_WAARDE("IOException: write failed");
    }
    static void Bellen_methode(int INDEX, int opdracht) {
        if (INDEX <= 0 || INDEX >= constante_tag.length || (constante_tag[INDEX] != 10 && constante_tag[INDEX] != 11)) { fout_WAARDE("invalid method reference"); return; }
        int eigenaar_WAARDE = klassenaam_sms(상가[INDEX]), Naam = verwijzen_naam(constante_SECONDE_WAARDE[INDEX]), opmaak_WAARDE = verwijzingstype(constante_SECONDE_WAARDE[INDEX]);
        if (fout) return;
        if (기본호출(eigenaar_WAARDE, Naam, opmaak_WAARDE, opdracht)) return;
        if (Word_sms(eigenaar_WAARDE, "java/io/FileInputStream") || Word_sms(eigenaar_WAARDE, "java/io/FileOutputStream")) {
            Bestand_Stream_Bellen(eigenaar_WAARDE, Naam, opmaak_WAARDE, opdracht); return;
        }
        if (opdracht == 184 && Word_sms(eigenaar_WAARDE, "java/lang/Integer") && Word_sms(Naam, "parseInt") && Word_sms(opmaak_WAARDE, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (opdracht == 182 && Word_sms(eigenaar_WAARDE, "java/io/PrintStream") && (Word_sms(Naam, "println") || Word_sms(Naam, "print"))) {
            int TYPE_WAARDE = 0, WAARDE = 0;
            if (Word_sms(opmaak_WAARDE, "(I)V")) { TYPE_WAARDE = 1; WAARDE = 빼기(1); }
            else if (Word_sms(opmaak_WAARDE, "(Z)V")) { TYPE_WAARDE = 2; WAARDE = 빼기(1); }
            else if (Word_sms(opmaak_WAARDE, "(C)V")) { TYPE_WAARDE = 3; WAARDE = 빼기(1); }
            else if (Word_sms(opmaak_WAARDE, "(Ljava/lang/String;)V")) { TYPE_WAARDE = 4; WAARDE = 빼기(2); }
            else if (!Word_sms(opmaak_WAARDE, "()V") || !Word_sms(Naam, "println")) fout_WAARDE("unsupported print descriptor");
            if (빼기(2) != -1) fout_WAARDE("invalid PrintStream receiver");
            if (fout) return;
            if (TYPE_WAARDE == 1) 자바도구.schrijven_nummer(WAARDE);
            if (TYPE_WAARDE == 2) gebruikersruimte.Schrijven(WAARDE == 0 ? "false" : "true");
            if (TYPE_WAARDE == 3) gebruikersruimte.schrijven_teken_WAARDE(WAARDE & 65535);
            if (TYPE_WAARDE == 4) schrijven_sms(WAARDE);
            if (Word_sms(Naam, "println")) gebruikersruimte.schrijven_teken_WAARDE(10);
            return;
        }
        if (opdracht == 182 && Word_sms(eigenaar_WAARDE, "java/lang/String")) {
            if (Word_sms(Naam, "length") && Word_sms(opmaak_WAARDE, "()I")) {
                int verwijzen = 빼기(2); if (object_WAARDE(verwijzen, 1)) 넣기(heap_WAARDE[verwijzen + 1], 1); return;
            }
            if (Word_sms(Naam, "charAt") && Word_sms(opmaak_WAARDE, "(I)C")) {
                int subscript_WAARDE = 빼기(1), verwijzen = 빼기(2);
                if (object_WAARDE(verwijzen, 1)) {
                    if (subscript_WAARDE < 0 || subscript_WAARDE >= heap_WAARDE[verwijzen + 1]) fout_WAARDE("StringIndexOutOfBoundsException"); else 넣기(heap_WAARDE[verwijzen + 2 + subscript_WAARDE], 1);
                }
                return;
            }
        }
        if (Word_sms(eigenaar_WAARDE, "java/lang/StringBuilder")) {
            if (opdracht == 183 && Word_sms(Naam, "<init>") && Word_sms(opmaak_WAARDE, "()V")) { object_WAARDE(빼기(2), 4); return; }
            if (opdracht == 182 && Word_sms(Naam, "toString") && Word_sms(opmaak_WAARDE, "()Ljava/lang/String;")) {
                int verwijzen = 빼기(2); if (object_WAARDE(verwijzen, 4)) 넣기(heap_WAARDE[verwijzen + 2] == 0 ? host_teken("") : heap_WAARDE[verwijzen + 2], 2); return;
            }
            if (opdracht == 182 && Word_sms(Naam, "append")) {
                int tekst = 0;
                if (Word_sms(opmaak_WAARDE, "(I)Ljava/lang/StringBuilder;")) tekst = cijfer_teken(빼기(1));
                else if (Word_sms(opmaak_WAARDE, "(Z)Ljava/lang/StringBuilder;")) tekst = host_teken(빼기(1) == 0 ? "false" : "true");
                else if (Word_sms(opmaak_WAARDE, "(C)Ljava/lang/StringBuilder;")) {
                    int WAARDE = 빼기(1); tekst = toewijzen_Opslag(1, 1); if (!fout) heap_WAARDE[tekst + 2] = WAARDE & 65535;
                }
                else if (Word_sms(opmaak_WAARDE, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { tekst = 빼기(2); if (tekst == 0) tekst = host_teken("null"); }
                else { fout_WAARDE("unsupported StringBuilder append"); return; }
                int verwijzen = 빼기(2); if (!object_WAARDE(verwijzen, 4) || !object_WAARDE(tekst, 1)) return;
                int voorkant_WAARDE = heap_WAARDE[verwijzen + 2], voorkant_WAARDE_tijdsduur = voorkant_WAARDE == 0 ? 0 : heap_WAARDE[voorkant_WAARDE + 1], BACK_WAARDE_tijdsduur = heap_WAARDE[tekst + 1];
                int 새글 = toewijzen_Opslag(1, voorkant_WAARDE_tijdsduur + BACK_WAARDE_tijdsduur); if (fout) return;
                for (int nummer = 0; nummer < voorkant_WAARDE_tijdsduur; nummer++) heap_WAARDE[새글 + 2 + nummer] = heap_WAARDE[voorkant_WAARDE + 2 + nummer];
                for (int nummer = 0; nummer < BACK_WAARDE_tijdsduur; nummer++) heap_WAARDE[새글 + 2 + voorkant_WAARDE_tijdsduur + nummer] = heap_WAARDE[tekst + 2 + nummer];
                heap_WAARDE[verwijzen + 2] = 새글; 넣기(verwijzen, 2); return;
            }
        }
        int les_Definitie = Zoeken_les_Definitie(eigenaar_WAARDE); if (les_Definitie < 0 || fout) return;
        int Bestand_INDEX = Zoeken_methode(les_Definitie, Naam, opmaak_WAARDE);
        if (Bestand_INDEX < 0) {
            for (int codepoint = les_Definitie, invoer_AANTAL_8f7753a1 = 0; codepoint >= 0 && invoer_AANTAL_8f7753a1 < 16; invoer_AANTAL_8f7753a1++, codepoint = bovenliggend_les(codepoint))
                if (Word_sms(les_Definitie_bovenliggend[codepoint], "java/lang/Thread")) { 가닥호출(Naam, opmaak_WAARDE, opdracht); return; }
            fout_WAARDE("NoSuchMethodError"); return;
        }
        if (((methode_toegang[Bestand_INDEX] & 8) != 0) != (opdracht == 184)) { fout_WAARDE("method static/instance mismatch"); return; }
        if (opdracht == 184) { if (!initialiseren(methode_eigenaar[Bestand_INDEX], frame_instructie[frame_INDEX])) return; }
        else {
            int 읽는자리 = frame_stack[frame_INDEX] - methode_argument_AANTAL[Bestand_INDEX];
            if (읽는자리 < 0 || operand_stack_TYPE[frame_INDEX * 128 + 읽는자리] != 2) { fout_WAARDE("invalid method receiver"); return; }
            int object_verwijzen = operand_stack_WAARDE[frame_INDEX * 128 + 읽는자리];
            if (!informatie_geldig_object(object_verwijzen)) return;
            if (heap_WAARDE[object_verwijzen] < 32 || !종포함(heap_WAARDE[object_verwijzen] - 32, eigenaar_WAARDE)) { fout_WAARDE("method receiver type mismatch"); return; }
            if (opdracht != 183) Bestand_INDEX = Zoeken_methode(heap_WAARDE[object_verwijzen] - 32, Naam, opmaak_WAARDE);
        }
        if (Bestand_INDEX < 0 || (methode_toegang[Bestand_INDEX] & 0x400) != 0) { fout_WAARDE("AbstractMethodError"); return; }
        int vergrendelen_verwijzen = 0;
        if ((methode_toegang[Bestand_INDEX] & 32) != 0) {
            if (opdracht == 184) { int codepoint = methode_eigenaar[Bestand_INDEX]; if (les_vergrendelen[codepoint] == 0) les_vergrendelen[codepoint] = toewijzen_Opslag(8, 0); vergrendelen_verwijzen = les_vergrendelen[codepoint]; }
            else vergrendelen_verwijzen = operand_stack_WAARDE[frame_INDEX * 128 + frame_stack[frame_INDEX] - methode_argument_AANTAL[Bestand_INDEX]];
            if (!잠금얻기(vergrendelen_verwijzen)) { if (!fout) frame_functie[frame_INDEX] = frame_instructie[frame_INDEX]; return; }
        }
        호출(Bestand_INDEX); if (!fout) frame_vergrendelen[frame_INDEX] = vergrendelen_verwijzen;
    }
    static boolean 배열저장가능(int MATRIX_verwijzen, int gegevens_WAARDE) {
        if (gegevens_WAARDE == 0 || matrixelement[MATRIX_verwijzen] == 0) return true;
        boolean 성공여부 = matrixelement[MATRIX_verwijzen] == -1 ? (gegevens_WAARDE > 0 && gegevens_WAARDE < heap_beëindigen_functie && heap_WAARDE[gegevens_WAARDE] == 1) : vereffenen_object(gegevens_WAARDE, matrixelement[MATRIX_verwijzen]);
        if (!성공여부 && !fout) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int MATRIX_sleuf(int verwijzen, int subscript_WAARDE, int TYPE_WAARDE) {
        if (!object_WAARDE(verwijzen, TYPE_WAARDE)) return 0;
        if (subscript_WAARDE < 0 || subscript_WAARDE >= heap_WAARDE[verwijzen + 1]) { fout_WAARDE("ArrayIndexOutOfBoundsException"); return 0; }
        return verwijzen + 2 + subscript_WAARDE;
    }
    static void Uitvoeren_opdracht() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (fout) { if (던진객체 != 0) greep_uitzondering(); if (fout || frame_INDEX < actueel_thread * 32) break; }
            if (frame_INDEX < actueel_thread * 32 || wijzigingsaanvraag || --조각 == 0) { if (!switch_thread()) break; 조각 = 100; }
            if (frame_INDEX == 0 && les_Definitie_Status[invoer_les_Definitie] != 2 && !initialiseren(invoer_les_Definitie, frame_functie[frame_INDEX])) continue;
            if (frame_INDEX == actueel_thread * 32 && actueel_thread != 0 && (methode_toegang[frame_methode[frame_INDEX]] & 32) != 0 && frame_vergrendelen[frame_INDEX] == 0) {
                int object_verwijzen = thread_doel[actueel_thread]; if (!잠금얻기(object_verwijzen)) { if (fout) break; continue; } frame_vergrendelen[frame_INDEX] = object_verwijzen;
            }
            잠시수 = 0;
            if (--남음 == 0) { fout_WAARDE("instruction limit (500000)"); break; }
            int starten = frame_functie[frame_INDEX]; frame_instructie[frame_INDEX] = starten; int WAARDE = 명바();
            if (fout) break;
            if (WAARDE == 0) continue;
            if (WAARDE == 1) { 넣기(0, 2); continue; }
            if (WAARDE >= 2 && WAARDE <= 8) { 넣기(WAARDE - 3, 1); continue; }
            if (WAARDE == 16) { 넣기((byte)명바(), 1); continue; }
            if (WAARDE == 17) { 넣기((short)명짧(), 1); continue; }
            if (WAARDE == 18 || WAARDE == 19) {
                int nummer = methode_eigenaar[frame_methode[frame_INDEX]] * 512 + (WAARDE == 18 ? 명바() : 명짧());
                if (nummer <= 0 || nummer >= constante_tag.length) fout_WAARDE("invalid ldc constant");
                else if (constante_tag[nummer] == 3) 넣기(상가[nummer], 1);
                else if (constante_tag[nummer] == 8) 넣기(constante_sms(상가[nummer]), 2);
                else fout_WAARDE("unsupported ldc constant");
                continue;
            }
            if (WAARDE == 21 || WAARDE == 25) { 지역읽기(명바(), WAARDE == 21 ? 1 : 2); continue; }
            if (WAARDE >= 26 && WAARDE <= 29) { 지역읽기(WAARDE - 26, 1); continue; }
            if (WAARDE >= 42 && WAARDE <= 45) { 지역읽기(WAARDE - 42, 2); continue; }
            if (WAARDE == 54 || WAARDE == 58) { schrijven_lokaal(명바(), WAARDE == 54 ? 1 : 2); continue; }
            if (WAARDE >= 59 && WAARDE <= 62) { schrijven_lokaal(WAARDE - 59, 1); continue; }
            if (WAARDE >= 75 && WAARDE <= 78) { schrijven_lokaal(WAARDE - 75, 2); continue; }
            if (WAARDE == 46 || WAARDE >= 50 && WAARDE <= 53) {
                int invoer_functie_206f1c6d = 빼기(1), object_verwijzen = 빼기(2), gebied_CODE = WAARDE == 46 ? 2 : WAARDE == 50 ? 3 : WAARDE == 51 ? 20 : WAARDE == 52 ? 22 : 23;
                if (WAARDE == 51 && object_verwijzen > 0 && object_verwijzen < heap_beëindigen_functie && heap_WAARDE[object_verwijzen] == 21) gebied_CODE = 21;
                int 읽는자리 = MATRIX_sleuf(object_verwijzen, invoer_functie_206f1c6d, gebied_CODE); if (!fout) 넣기(heap_WAARDE[읽는자리], WAARDE == 50 ? 2 : 1); continue;
            }
            if (WAARDE == 79 || WAARDE >= 83 && WAARDE <= 86) {
                int invoer_verwijzen = 빼기(WAARDE == 83 ? 2 : 1), invoer_functie_206f1c6d = 빼기(1), object_verwijzen = 빼기(2), gebied_CODE = WAARDE == 79 ? 2 : WAARDE == 83 ? 3 : WAARDE == 84 ? 20 : WAARDE == 85 ? 22 : 23;
                if (WAARDE == 84 && object_verwijzen > 0 && object_verwijzen < heap_beëindigen_functie && heap_WAARDE[object_verwijzen] == 21) gebied_CODE = 21;
                int 읽는자리 = MATRIX_sleuf(object_verwijzen, invoer_functie_206f1c6d, gebied_CODE);
                if (!fout && gebied_CODE == 3 && !배열저장가능(object_verwijzen, invoer_verwijzen)) continue;
                if (!fout) heap_WAARDE[읽는자리] = gebied_CODE == 20 ? (byte)invoer_verwijzen : gebied_CODE == 21 ? invoer_verwijzen & 1 : gebied_CODE == 22 ? (char)invoer_verwijzen : gebied_CODE == 23 ? (short)invoer_verwijzen : invoer_verwijzen;
                continue;
            }
            if (WAARDE >= 87 && WAARDE <= 95) { stack_instructie(WAARDE); continue; }
            if (WAARDE == 96 || WAARDE == 100 || WAARDE == 104 || WAARDE == 108 || WAARDE == 112 || WAARDE == 120
                || WAARDE == 122 || WAARDE == 124 || WAARDE == 126 || WAARDE == 128 || WAARDE == 130) {
                int SECONDE_operand = 빼기(1), 가 = 빼기(1), resultaat = 0;
                if ((WAARDE == 108 || WAARDE == 112) && SECONDE_operand == 0) { fout_WAARDE("ArithmeticException: / by zero"); continue; }
                if (WAARDE == 96) resultaat = 가 + SECONDE_operand;
                if (WAARDE == 100) resultaat = 가 - SECONDE_operand;
                if (WAARDE == 104) resultaat = 가 * SECONDE_operand;
                if (WAARDE == 108) resultaat = 가 / SECONDE_operand;
                if (WAARDE == 112) resultaat = 가 % SECONDE_operand;
                if (WAARDE == 120) resultaat = 가 << SECONDE_operand;
                if (WAARDE == 122) resultaat = 가 >> SECONDE_operand;
                if (WAARDE == 124) resultaat = 가 >>> SECONDE_operand;
                if (WAARDE == 126) resultaat = 가 & SECONDE_operand;
                if (WAARDE == 128) resultaat = 가 | SECONDE_operand;
                if (WAARDE == 130) resultaat = 가 ^ SECONDE_operand;
                넣기(resultaat, 1); continue;
            }
            if (WAARDE == 116) { 넣기(-빼기(1), 1); continue; }
            if (WAARDE == 132) {
                int lokaal_scope = 명바(), toename_stap = (byte)명바(); 지역읽기(lokaal_scope, 1); 넣기(빼기(1) + toename_stap, 1); schrijven_lokaal(lokaal_scope, 1); continue;
            }
            if (WAARDE >= 145 && WAARDE <= 147) {
                int nummer = 빼기(1); 넣기(WAARDE == 145 ? (byte)nummer : WAARDE == 146 ? (char)nummer : (short)nummer, 1); continue;
            }
            if (WAARDE >= 153 && WAARDE <= 167 || WAARDE == 198 || WAARDE == 199) {
                int doel_WAARDE = starten + (short)명짧(); boolean 갈까 = WAARDE == 167;
                if (WAARDE >= 153 && WAARDE <= 158) {
                    int nummer = 빼기(1); 갈까 = WAARDE == 153 ? nummer == 0 : WAARDE == 154 ? nummer != 0 : WAARDE == 155 ? nummer < 0 : WAARDE == 156 ? nummer >= 0 : WAARDE == 157 ? nummer > 0 : nummer <= 0;
                } else if (WAARDE >= 159 && WAARDE <= 166) {
                    int SECONDE_operand = 빼기(WAARDE >= 165 ? 2 : 1), 가 = 빼기(WAARDE >= 165 ? 2 : 1);
                    갈까 = WAARDE == 159 || WAARDE == 165 ? 가 == SECONDE_operand : WAARDE == 160 || WAARDE == 166 ? 가 != SECONDE_operand : WAARDE == 161 ? 가 < SECONDE_operand : WAARDE == 162 ? 가 >= SECONDE_operand : WAARDE == 163 ? 가 > SECONDE_operand : 가 <= SECONDE_operand;
                } else if (WAARDE == 198 || WAARDE == 199) { int nummer = 빼기(2); 갈까 = WAARDE == 198 ? nummer == 0 : nummer != 0; }
                if (갈까) verplaatsen_WAARDE_83b651b8(doel_WAARDE); continue;
            }
            if (WAARDE == 172 || WAARDE == 176 || WAARDE == 177) { Retour_HR(WAARDE == 172 ? 1 : WAARDE == 176 ? 2 : 0); continue; }
            if (WAARDE >= 178 && WAARDE <= 181) { 필드호출(명상수(), WAARDE, starten); continue; }
            if (WAARDE >= 182 && WAARDE <= 185) {
                int 부호값 = 명상수();
                if (WAARDE == 185) { int totaal_AANTAL = 명바(); if (totaal_AANTAL == 0 || 명바() != 0) { fout_WAARDE("invalid invokeinterface operands"); continue; } }
                Bellen_methode(부호값, WAARDE); continue;
            }
            if (WAARDE == 187) { 새객체(klassenaam_sms(명상수()), starten); continue; }
            if (WAARDE == 188 || WAARDE == 189) {
                int gebied_CODE = 3, onderdeel = 0;
                if (WAARDE == 188) { int 임시값 = 명바(); gebied_CODE = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else onderdeel = klassenaam_sms(명상수());
                if (gebied_CODE == 0) { fout_WAARDE("unsupported primitive array type"); continue; }
                int geldig_tijdsduur = 빼기(1), object_verwijzen = toewijzen_Opslag(gebied_CODE, geldig_tijdsduur); if (!fout) matrixelement[object_verwijzen] = onderdeel; 넣기(object_verwijzen, 2); continue;
            }
            if (WAARDE == 190) {
                int object_verwijzen = 빼기(2);
                if (informatie_geldig_object(object_verwijzen)) { int Vergelijking_functie = heap_WAARDE[object_verwijzen]; if (Vergelijking_functie != 2 && Vergelijking_functie != 3 && (Vergelijking_functie < 20 || Vergelijking_functie > 23)) fout_WAARDE("not an array"); else 넣기(heap_WAARDE[object_verwijzen + 1], 1); }
                continue;
            }
            if (WAARDE == 191) {
                int object_verwijzen = 빼기(2); if (informatie_geldig_object(object_verwijzen)) { if (heap_WAARDE[object_verwijzen] != 9) fout_WAARDE("athrow requires supported Throwable"); else { 던진객체 = object_verwijzen; fout = true; } }
                continue;
            }
            if (WAARDE == 192 || WAARDE == 193) {
                int naam_constante = klassenaam_sms(명상수()), object_verwijzen = 빼기(2); boolean VERGELIJKEN = vereffenen_object(object_verwijzen, naam_constante);
                if (WAARDE == 193) 넣기(object_verwijzen != 0 && VERGELIJKEN ? 1 : 0, 1);
                else { if (!VERGELIJKEN && !fout) fout_WAARDE("ClassCastException"); 넣기(object_verwijzen, 2); }
                continue;
            }
            if (WAARDE == 170 || WAARDE == 171) {
                int 읽는자리 = starten + 1, Bestand_INDEX = frame_methode[frame_INDEX], toets_verwijzen = 빼기(1);
                while ((읽는자리 - methode_START[Bestand_INDEX]) % 4 != 0) 읽는자리++;
                int doel_ADRES = functie_geheel_getal(읽는자리);
                if (WAARDE == 170) { int 낮은값 = functie_geheel_getal(읽는자리 + 4), 높은값 = functie_geheel_getal(읽는자리 + 8); if (toets_verwijzen >= 낮은값 && toets_verwijzen <= 높은값) doel_ADRES = functie_geheel_getal(읽는자리 + 12 + (toets_verwijzen - 낮은값) * 4); }
                else { int totaal_AANTAL = functie_geheel_getal(읽는자리 + 4); for (int lus_INDEX = 0; lus_INDEX < totaal_AANTAL; lus_INDEX++) if (functie_geheel_getal(읽는자리 + 8 + lus_INDEX * 8) == toets_verwijzen) doel_ADRES = functie_geheel_getal(읽는자리 + 12 + lus_INDEX * 8); }
                verplaatsen_WAARDE_83b651b8(starten + doel_ADRES); continue;
            }
            if (WAARDE == 200) { verplaatsen_WAARDE_83b651b8(starten + functie_geheel_getal(starten + 1)); continue; }
            if (WAARDE == 194 || WAARDE == 195) {
                int object_verwijzen = 빼기(2);
                if (WAARDE == 195) versie_vergrendelen(object_verwijzen);
                else if (!잠금얻기(object_verwijzen) && !fout) { 넣기(object_verwijzen, 2); frame_functie[frame_INDEX] = starten; }
                continue;
            }
            if (WAARDE == 196) {
                int opdracht_CODE = 명바(), invoer_functie_206f1c6d = 명짧();
                if (opdracht_CODE == 21 || opdracht_CODE == 25) 지역읽기(invoer_functie_206f1c6d, opdracht_CODE == 21 ? 1 : 2);
                else if (opdracht_CODE == 54 || opdracht_CODE == 58) schrijven_lokaal(invoer_functie_206f1c6d, opdracht_CODE == 54 ? 1 : 2);
                else if (opdracht_CODE == 132) { int DELTA_WAARDE = (short)명짧(); 지역읽기(invoer_functie_206f1c6d, 1); 넣기(빼기(1) + DELTA_WAARDE, 1); schrijven_lokaal(invoer_functie_206f1c6d, 1); }
                else fout_WAARDE("unsupported wide opcode");
                continue;
            }
            fout_WAARDE("unsupported bytecode");
        }
    }
    static int Zoeken_les_Definitie(int Naam) {
        for (int lus_INDEX = 0; lus_INDEX < les_Definitie_AANTAL; lus_INDEX++) if (les_Definitie_naam[lus_INDEX] != 0 && vereffenen_Word(les_Definitie_naam[lus_INDEX], Naam)) return lus_INDEX;
        return load_les_Definitie(constante_sms(Naam));
    }
    static int load_les_Definitie(int naam_tekenreeks) {
        if (!object_WAARDE(naam_tekenreeks, 1)) return -1;
        int tijdsduur_WAARDE = heap_WAARDE[naam_tekenreeks + 1];
        if (tijdsduur_WAARDE < 1 || tijdsduur_WAARDE > 505 || les_Definitie_AANTAL == 16) { fout_WAARDE("class name/count limit"); return -1; }
        for (int lus_INDEX = 0; lus_INDEX < tijdsduur_WAARDE; lus_INDEX++) { int codepoint = heap_WAARDE[naam_tekenreeks + 2 + lus_INDEX]; bestandsnaam_sms[lus_INDEX] = codepoint == '/' ? '.' : codepoint; }
        bestandsnaam_sms[tijdsduur_WAARDE] = '.'; bestandsnaam_sms[tijdsduur_WAARDE + 1] = 'c'; bestandsnaam_sms[tijdsduur_WAARDE + 2] = 'l'; bestandsnaam_sms[tijdsduur_WAARDE + 3] = 'a'; bestandsnaam_sms[tijdsduur_WAARDE + 4] = 's'; bestandsnaam_sms[tijdsduur_WAARDE + 5] = 's'; bestandsnaam_sms[tijdsduur_WAARDE + 6] = 0;
        int Grootte = gebruikersruimte.파일읽기(bestandsnaam_sms, tijdelijk_bestand);
        if (Grootte < 0) { fout_WAARDE("ClassNotFoundException"); return -1; }
        int les_Definitie = les_Definitie_AANTAL++; les_Definitie_formaat_wijzigen[les_Definitie] = Grootte;
        for (int lus_INDEX = 0; lus_INDEX < Grootte; lus_INDEX++) bestand[les_Definitie * 16384 + lus_INDEX] = tijdelijk_bestand[lus_INDEX];
        클래스읽기(les_Definitie); if (fout) return -1;
        int werkelijk_gegevens = constante_sms(les_Definitie_naam[les_Definitie]);
        if (!teksten_gelijk(werkelijk_gegevens, naam_tekenreeks, true)) { fout_WAARDE("class name does not match file"); return -1; }
        int bovenliggend_WAARDE = les_Definitie_bovenliggend[les_Definitie];
        if (bovenliggend_WAARDE != 0 && !Word_sms(bovenliggend_WAARDE, "java/lang/Object") && !Word_sms(bovenliggend_WAARDE, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 opnieuw_proberen_WAARDE 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = Zoeken_les_Definitie(bovenliggend_WAARDE);
            if (fout || 위 < 0) return -1;
            int 읽는자리 = 위, fase_AANTAL = 0;
            while (읽는자리 >= 0 && fase_AANTAL++ < 16) {
                if (읽는자리 == les_Definitie) { fout_WAARDE("cyclic inheritance"); return -1; }
                읽는자리 = bovenliggend_les(읽는자리);
            }
            int 시작변위 = les_sleuf_AANTAL[위];
            for (int Bestand_INDEX = 0; Bestand_INDEX < sleuf_AANTAL; Bestand_INDEX++) if (sleuf_eigenaar[Bestand_INDEX] == les_Definitie && (sleuf_Machtigingen[Bestand_INDEX] & 8) == 0) sleuf_functie[Bestand_INDEX] += 시작변위;
            les_sleuf_AANTAL[les_Definitie] += 시작변위;
        }
        return les_Definitie;
    }
    static int bovenliggend_les(int les_Definitie) {
        int Naam = les_Definitie_bovenliggend[les_Definitie];
        for (int lus_INDEX = 0; lus_INDEX < les_Definitie_AANTAL; lus_INDEX++) if (Naam != 0 && les_Definitie_naam[lus_INDEX] != 0 && vereffenen_Word(les_Definitie_naam[lus_INDEX], Naam)) return lus_INDEX;
        return -1;
    }
    static int Zoeken_methode(int les_Definitie, int Naam, int opmaak_WAARDE) {
        for (int 깊이 = 0; les_Definitie >= 0 && 깊이 < 16; 깊이++, les_Definitie = bovenliggend_les(les_Definitie)) {
            for (int lus_INDEX = 0; lus_INDEX < methode_AANTAL; lus_INDEX++) if (methode_eigenaar[lus_INDEX] == les_Definitie && vereffenen_Word(methode_naam_sms[lus_INDEX], Naam) && vereffenen_Word(methode_TYPE[lus_INDEX], opmaak_WAARDE)) return lus_INDEX;
        }
        return -1;
    }
    static int naam_methode(int les_Definitie, String Naam, String opmaak_WAARDE) {
        for (int 깊이 = 0; les_Definitie >= 0 && 깊이 < 16; 깊이++, les_Definitie = bovenliggend_les(les_Definitie))
            for (int lus_INDEX = 0; lus_INDEX < methode_AANTAL; lus_INDEX++) if (methode_eigenaar[lus_INDEX] == les_Definitie && Word_sms(methode_naam_sms[lus_INDEX], Naam) && Word_sms(methode_TYPE[lus_INDEX], opmaak_WAARDE)) return lus_INDEX;
        return -1;
    }
    static int TYPE_soort(int Naam) { return bestand[상가[Naam]] == 'L' || bestand[상가[Naam]] == '[' ? 2 : 1; }
    static boolean initialiseren(int les_Definitie, int opdracht_START) {
        if (les_Definitie < 0 || fout) return false;
        if (les_Definitie_Status[les_Definitie] == 3) { fout_WAARDE("NoClassDefFoundError: initialization failed"); return false; }
        if (les_Definitie_Status[les_Definitie] == 1 && les_thread[les_Definitie] != actueel_thread) { frame_functie[frame_INDEX] = opdracht_START; wijzigingsaanvraag = true; return false; }
        if (les_Definitie_Status[les_Definitie] != 0) return true;
        int 위 = bovenliggend_les(les_Definitie);
        if (위 >= 0 && !initialiseren(위, opdracht_START)) return false;
        les_Definitie_Status[les_Definitie] = 1; les_thread[les_Definitie] = actueel_thread;
        if (initialiseren_les_Definitie[les_Definitie] != 0) {
            frame_functie[frame_INDEX] = opdracht_START;
            호출(initialiseren_les_Definitie[les_Definitie] - 1); if (!fout) initialiseren_frame[frame_INDEX] = les_Definitie + 1;
            return false;
        }
        les_Definitie_Status[les_Definitie] = 2; return true;
    }
    static void 필드호출(int INDEX, int opdracht, int starten) {
        if (!cheque_constante(INDEX, 9)) return;
        int eigenaar_WAARDE = klassenaam_sms(상가[INDEX]), Naam = verwijzen_naam(constante_SECONDE_WAARDE[INDEX]), opmaak_WAARDE = verwijzingstype(constante_SECONDE_WAARDE[INDEX]);
        if (Word_sms(eigenaar_WAARDE, "java/lang/System") && (Word_sms(Naam, "out") || Word_sms(Naam, "err")) && Word_sms(opmaak_WAARDE, "Ljava/io/PrintStream;") && opdracht == 178) { 넣기(-1, 2); return; }
        int les_Definitie = Zoeken_les_Definitie(eigenaar_WAARDE); if (les_Definitie < 0 || fout) return;
        int 찾음 = -1;
        for (int 읽는자리 = les_Definitie, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = bovenliggend_les(읽는자리))
            for (int Bestand_INDEX = 0; Bestand_INDEX < sleuf_AANTAL; Bestand_INDEX++) if (sleuf_eigenaar[Bestand_INDEX] == 읽는자리 && vereffenen_Word(sleuf_naam[Bestand_INDEX], Naam) && vereffenen_Word(sleuf_TYPE[Bestand_INDEX], opmaak_WAARDE)) 찾음 = Bestand_INDEX;
        if (찾음 < 0) { fout_WAARDE("NoSuchFieldError"); return; }
        boolean statisch_WAARDE = opdracht == 178 || opdracht == 179;
        if (statisch_WAARDE != ((sleuf_Machtigingen[찾음] & 8) != 0)) { fout_WAARDE("field static/instance mismatch"); return; }
        if (statisch_WAARDE && !initialiseren(sleuf_eigenaar[찾음], starten)) return;
        int TYPE_WAARDE = TYPE_soort(opmaak_WAARDE), WAARDE = 0;
        if (opdracht == 179 || opdracht == 181) WAARDE = 빼기(TYPE_WAARDE);
        if (statisch_WAARDE) { if (opdracht == 178) 넣기(sleuf_gegevens[찾음], TYPE_WAARDE); else if (!fout) sleuf_gegevens[찾음] = WAARDE; return; }
        int object_verwijzen = 빼기(2);
        if (!informatie_geldig_object(object_verwijzen)) return;
        if (heap_WAARDE[object_verwijzen] < 32 || !종포함(heap_WAARDE[object_verwijzen] - 32, eigenaar_WAARDE)) { fout_WAARDE("field receiver type mismatch"); return; }
        int 보관칸 = object_verwijzen + 2 + sleuf_functie[찾음];
        if (opdracht == 180) 넣기(heap_WAARDE[보관칸], TYPE_WAARDE);
        else if (!fout) { heap_WAARDE[보관칸] = WAARDE; heap_verwijzen[보관칸] = TYPE_WAARDE == 2 ? 1 : 0; }
    }
    static boolean 종포함(int les_Definitie, int Naam) {
        for (int 중첩깊이 = 0; les_Definitie >= 0 && 중첩깊이 < 16; 중첩깊이++, les_Definitie = bovenliggend_les(les_Definitie)) {
            if (vereffenen_Word(les_Definitie_naam[les_Definitie], Naam) || (les_Definitie_bovenliggend[les_Definitie] != 0 && vereffenen_Word(les_Definitie_bovenliggend[les_Definitie], Naam))) return true;
            for (int inner_functie = 0; inner_functie < les_interface_AANTAL[les_Definitie]; inner_functie++) if (vereffenen_Word(les_interface[les_Definitie * 16 + inner_functie], Naam)) return true;
        }
        return false;
    }
    static boolean teksten_gelijk(int 첫값, int byte_gegevens, boolean pad) {
        if (첫값 == byte_gegevens) return true;
        if (첫값 <= 0 || byte_gegevens <= 0 || heap_WAARDE[첫값] != 1 || heap_WAARDE[byte_gegevens] != 1 || heap_WAARDE[첫값 + 1] != heap_WAARDE[byte_gegevens + 1]) return false;
        for (int lus_INDEX = 0; lus_INDEX < heap_WAARDE[첫값 + 1]; lus_INDEX++) {
            int x_coördinaat = heap_WAARDE[첫값 + 2 + lus_INDEX], Y_coördinaat = heap_WAARDE[byte_gegevens + 2 + lus_INDEX];
            if (pad) { if (x_coördinaat == '.') x_coördinaat = '/'; if (Y_coördinaat == '.') Y_coördinaat = '/'; }
            if (x_coördinaat != Y_coördinaat) return false;
        }
        return true;
    }
    static boolean informatie_geldig_object(int object_verwijzen) {
        if (object_verwijzen == 0) { fout_WAARDE("NullPointerException"); return false; }
        if (object_verwijzen < 1 || object_verwijzen >= heap_beëindigen_functie || 힙폭[object_verwijzen] < 2 || heap_WAARDE[object_verwijzen] == 0) { fout_WAARDE("invalid object reference"); return false; }
        return true;
    }
    static void beschermen_WAARDE(int object_verwijzen) {
        if (object_verwijzen > 0 && object_verwijzen < heap_beëindigen_functie && 힙폭[object_verwijzen] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = object_verwijzen;
    }
    static void weergeven_WAARDE(int object_verwijzen) {
        if (object_verwijzen > 0 && object_verwijzen < heap_beëindigen_functie && 힙폭[object_verwijzen] >= 2 && heap_WAARDE[object_verwijzen] != 0 && 힙표시[object_verwijzen] == 0) {
            힙표시[object_verwijzen] = 1; 표시대기[weergeven_AANTAL++] = object_verwijzen;
        }
    }
    static void 수거() {
        weergeven_AANTAL = 0; incasso_AANTAL++;
        for (int cheque_functie = 1; cheque_functie < heap_beëindigen_functie; cheque_functie += 힙폭[cheque_functie]) 힙표시[cheque_functie] = 0;
        for (int lus_INDEX = 0; lus_INDEX < tekenreeks_verwijzen.length; lus_INDEX++) weergeven_WAARDE(tekenreeks_verwijzen[lus_INDEX]);
        for (int lus_INDEX = 0; lus_INDEX < sleuf_AANTAL; lus_INDEX++) if ((sleuf_Machtigingen[lus_INDEX] & 8) != 0 && TYPE_soort(sleuf_TYPE[lus_INDEX]) == 2) weergeven_WAARDE(sleuf_gegevens[lus_INDEX]);
        for (int 임시값 = 0; 임시값 < aantal_threads; 임시값++) {
            weergeven_WAARDE(thread_object[임시값]); weergeven_WAARDE(thread_doel[임시값]);
            int 꼭대기자리 = 임시값 == actueel_thread ? frame_INDEX : thread_frame[임시값];
            for (int Bestand_INDEX = 임시값 * 32; Bestand_INDEX <= 꼭대기자리; Bestand_INDEX++) {
                for (int inner_functie = 0; inner_functie < 함수지역[frame_methode[Bestand_INDEX]]; inner_functie++) if (lokaal_TYPE[Bestand_INDEX * 128 + inner_functie] == 2) weergeven_WAARDE(lokaal_WAARDE[Bestand_INDEX * 128 + inner_functie]);
                for (int inner_functie = 0; inner_functie < frame_stack[Bestand_INDEX]; inner_functie++) if (operand_stack_TYPE[Bestand_INDEX * 128 + inner_functie] == 2) weergeven_WAARDE(operand_stack_WAARDE[Bestand_INDEX * 128 + inner_functie]);
            }
        }
        for (int lus_INDEX = 0; lus_INDEX < scherm_verwijzen.length; lus_INDEX++) weergeven_WAARDE(scherm_verwijzen[lus_INDEX]);
        for (int lus_INDEX = 0; lus_INDEX < 나중수; lus_INDEX++) weergeven_WAARDE(나중실행[lus_INDEX]);
        for (int lus_INDEX = 0; lus_INDEX < Store_geheel_getal.length; lus_INDEX++) weergeven_WAARDE(Store_geheel_getal[lus_INDEX]);
        for (int lus_INDEX = 0; lus_INDEX < les_Definitie_AANTAL; lus_INDEX++) weergeven_WAARDE(les_vergrendelen[lus_INDEX]);
        for (int cheque_functie = 1; cheque_functie < heap_beëindigen_functie; cheque_functie += 힙폭[cheque_functie]) if (잠금깊이[cheque_functie] > 0) weergeven_WAARDE(cheque_functie);
        weergeven_WAARDE(던진객체);
        for (int lus_INDEX = 0; lus_INDEX < 잠시수; lus_INDEX++) weergeven_WAARDE(잠시참조[lus_INDEX]);
        while (weergeven_AANTAL > 0) {
            int object_verwijzen = 표시대기[--weergeven_AANTAL], gebied_CODE = heap_WAARDE[object_verwijzen];
            for (int lus_INDEX = object_verwijzen + 2; lus_INDEX < object_verwijzen + 힙폭[object_verwijzen]; lus_INDEX++) if (gebied_CODE == 3 || gebied_CODE == 4 || heap_verwijzen[lus_INDEX] != 0) weergeven_WAARDE(heap_WAARDE[lus_INDEX]);
        }
        for (int cheque_functie = 1; cheque_functie < heap_beëindigen_functie; cheque_functie += 힙폭[cheque_functie]) if (힙표시[cheque_functie] == 0) heap_WAARDE[cheque_functie] = 0;
        for (int cheque_functie = 1; cheque_functie < heap_beëindigen_functie; cheque_functie += 힙폭[cheque_functie]) if (heap_WAARDE[cheque_functie] == 0) {
            while (cheque_functie + 힙폭[cheque_functie] < heap_beëindigen_functie && heap_WAARDE[cheque_functie + 힙폭[cheque_functie]] == 0) { int Volgende_functie = cheque_functie + 힙폭[cheque_functie]; 힙폭[cheque_functie] += 힙폭[Volgende_functie]; 힙폭[Volgende_functie] = 0; }
            if (cheque_functie + 힙폭[cheque_functie] == heap_beëindigen_functie) { heap_beëindigen_functie = cheque_functie; break; }
        }
    }
    static int 새기억(int soort_WAARDE, int tijdsduur_WAARDE) {
        if (tijdsduur_WAARDE < 0) { fout_WAARDE("NegativeArraySizeException"); return 0; }
        if (tijdsduur_WAARDE > heap_WAARDE.length - 3) { fout_WAARDE("object heap exhausted"); return 0; }
        int 필요수 = tijdsduur_WAARDE + 2, object_verwijzen = 0;
        if (필요수 <= heap_WAARDE.length - heap_beëindigen_functie) { object_verwijzen = heap_beëindigen_functie; heap_beëindigen_functie += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < heap_beëindigen_functie; 읽는자리 += 힙폭[읽는자리]) if (heap_WAARDE[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { object_verwijzen = 읽는자리; break; }
            if (object_verwijzen != 0) {
                int 남은길이 = 힙폭[object_verwijzen] - 필요수;
                if (남은길이 >= 2) { 힙폭[object_verwijzen + 필요수] = 남은길이; heap_WAARDE[object_verwijzen + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= heap_WAARDE.length - heap_beëindigen_functie) { object_verwijzen = heap_beëindigen_functie; heap_beëindigen_functie += 필요수; }
        }
        if (object_verwijzen == 0) { fout_WAARDE("object heap exhausted"); return 0; }
        for (int lus_INDEX = 0; lus_INDEX < 필요수; lus_INDEX++) { heap_WAARDE[object_verwijzen + lus_INDEX] = 0; heap_verwijzen[object_verwijzen + lus_INDEX] = 0; 힙폭[object_verwijzen + lus_INDEX] = 0; }
        matrixelement[object_verwijzen] = 0;
        힙폭[object_verwijzen] = 필요수; heap_WAARDE[object_verwijzen] = soort_WAARDE; heap_WAARDE[object_verwijzen + 1] = tijdsduur_WAARDE; beschermen_WAARDE(object_verwijzen); return object_verwijzen;
    }
    static int uitzondering_les(String naam_constante) {
        if (자바도구.같음(naam_constante, "java/lang/Throwable")) return 1;
        if (자바도구.같음(naam_constante, "java/lang/Exception")) return 2;
        if (자바도구.같음(naam_constante, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(naam_constante, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(naam_constante, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(naam_constante, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(naam_constante, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(naam_constante, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(naam_constante, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(naam_constante, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(naam_constante, "java/io/IOException")) return 11;
        if (자바도구.같음(naam_constante, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(naam_constante, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(naam_constante, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(naam_constante, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int uitzondering_constante(int Naam) {
        for (int lus_INDEX = 1; lus_INDEX <= 41; lus_INDEX++) if (Word_sms(Naam, uitzondering_naam(lus_INDEX))) return lus_INDEX;
        return 0;
    }
    static String uitzondering_naam(int account_WAARDE) {
        if (account_WAARDE == 40) return "java/lang/InterruptedException";
        if (account_WAARDE == 41) return "Nederlands/Eigen/대기중단예외";
        if (account_WAARDE == 39) return "java/net/SocketException";
        if (account_WAARDE == 20) return "Nederlands/Eigen/uitzondering";
        if (account_WAARDE == 21) return "Nederlands/Eigen/uitvoerbewerking_uitzondering";
        if (account_WAARDE == 22) return "Nederlands/Eigen/I_O_uitzondering";
        if (account_WAARDE == 23) return "Nederlands/Eigen/wachten_TIMEOUT_uitzondering";
        if (account_WAARDE == 24) return "Nederlands/Eigen/ADRES_ZOEKEN_uitzondering";
        if (account_WAARDE == 25) return "Nederlands/Eigen/파일없음예외";
        if (account_WAARDE == 26) return "Nederlands/Eigen/communicatie_uitzondering";
        if (account_WAARDE == 27) return "Nederlands/Eigen/nietig_argument_uitzondering";
        if (account_WAARDE == 28) return "Nederlands/Eigen/nummer_opmaak_fout";
        if (account_WAARDE == 29) return "Nederlands/Eigen/범위예외";
        if (account_WAARDE == 30) return "Nederlands/Eigen/배열범위예외";
        if (account_WAARDE == 31) return "Nederlands/Eigen/문자열범위예외";
        if (account_WAARDE == 32) return "Nederlands/Eigen/LEEG_verwijzen_uitzondering";
        if (account_WAARDE == 33) return "Nederlands/Eigen/산술예외";
        if (account_WAARDE == 34) return "Nederlands/Eigen/Status_uitzondering";
        if (account_WAARDE == 35) return "Nederlands/Eigen/TYPE_Weergeven_uitzondering";
        if (account_WAARDE == 36) return "Nederlands/Eigen/음수배열크기예외";
        if (account_WAARDE == 37) return "Nederlands/Eigen/MATRIX_Store_fout";
        if (account_WAARDE == 38) return "Nederlands/Eigen/thread_Status_uitzondering";
        if (account_WAARDE == 1) return "java/lang/Throwable"; if (account_WAARDE == 2) return "java/lang/Exception";
        if (account_WAARDE == 3) return "java/lang/RuntimeException"; if (account_WAARDE == 4) return "java/lang/ArithmeticException";
        if (account_WAARDE == 5) return "java/lang/NullPointerException"; if (account_WAARDE == 6) return "java/lang/IndexOutOfBoundsException";
        if (account_WAARDE == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (account_WAARDE == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (account_WAARDE == 9) return "java/lang/IllegalArgumentException"; if (account_WAARDE == 10) return "java/lang/NumberFormatException";
        if (account_WAARDE == 11) return "java/io/IOException"; if (account_WAARDE == 12) return "java/io/FileNotFoundException";
        if (account_WAARDE == 17) return "java/lang/ArrayStoreException";
        if (account_WAARDE == 18) return "java/net/UnknownHostException";
        if (account_WAARDE == 19) return "java/net/SocketTimeoutException";
        if (account_WAARDE == 16) return "java/lang/IllegalThreadStateException";
        if (account_WAARDE == 13) return "java/lang/IllegalStateException"; if (account_WAARDE == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int uitzondering_bovenliggend(int account_WAARDE) {
        if (account_WAARDE == 40) return 2;
        if (account_WAARDE == 41) return 40;
        if (account_WAARDE == 39) return 11;
        if (account_WAARDE == 1) return 0;
        if (account_WAARDE == 2) return 1;
        if (account_WAARDE == 3) return 2;
        if (account_WAARDE == 4) return 3;
        if (account_WAARDE == 5) return 3;
        if (account_WAARDE == 6) return 3;
        if (account_WAARDE == 7) return 6;
        if (account_WAARDE == 8) return 6;
        if (account_WAARDE == 9) return 3;
        if (account_WAARDE == 10) return 9;
        if (account_WAARDE == 11) return 2;
        if (account_WAARDE == 12) return 11;
        if (account_WAARDE == 13) return 3;
        if (account_WAARDE == 14) return 3;
        if (account_WAARDE == 15) return 3;
        if (account_WAARDE == 16) return 9;
        if (account_WAARDE == 17) return 3;
        if (account_WAARDE == 18) return 11;
        if (account_WAARDE == 19) return 11;
        if (account_WAARDE == 20) return 2;
        if (account_WAARDE == 21) return 3;
        if (account_WAARDE == 22) return 11;
        if (account_WAARDE == 23) return 22;
        if (account_WAARDE == 24) return 22;
        if (account_WAARDE == 25) return 22;
        if (account_WAARDE == 26) return 22;
        if (account_WAARDE == 27) return 9;
        if (account_WAARDE == 28) return 27;
        if (account_WAARDE == 29) return 6;
        if (account_WAARDE == 30) return 29;
        if (account_WAARDE == 31) return 29;
        if (account_WAARDE == 32) return 5;
        if (account_WAARDE == 33) return 4;
        if (account_WAARDE == 34) return 13;
        if (account_WAARDE == 35) return 14;
        if (account_WAARDE == 36) return 15;
        if (account_WAARDE == 37) return 17;
        if (account_WAARDE == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int werkelijke_waarde, int 요구값) {
        for (int 깊이 = 0; werkelijke_waarde != 0 && 깊이 < 16; 깊이++, werkelijke_waarde = uitzondering_bovenliggend(werkelijke_waarde))
            if (werkelijke_waarde == 요구값) return true;
        return false;
    }
    static void 예외던짐(int account_WAARDE, String LEESMIJ_verwijzen) {
        int object_verwijzen = 새기억(9, 2); if (fout) return;
        heap_WAARDE[object_verwijzen + 2] = account_WAARDE; heap_WAARDE[object_verwijzen + 3] = host_teken(LEESMIJ_verwijzen); heap_verwijzen[object_verwijzen + 3] = 1;
        던진객체 = object_verwijzen; fout = true;
    }
    static boolean vereffenen_object(int object_verwijzen, int Naam) {
        if (object_verwijzen == 0) return true;
        if (!informatie_geldig_object(object_verwijzen)) return false;
        int gebied_CODE = heap_WAARDE[object_verwijzen];
        if (Word_sms(Naam, "java/lang/Object")) return true;
        if (gebied_CODE >= 32) return 종포함(gebied_CODE - 32, Naam);
        if (gebied_CODE == 9) { int doel_ADRES = uitzondering_constante(Naam); return doel_ADRES != 0 && 예외포함(heap_WAARDE[object_verwijzen + 2], doel_ADRES); }
        if (gebied_CODE == 1) return Word_sms(Naam, "java/lang/String") || Word_sms(Naam, "java/lang/CharSequence");
        if (gebied_CODE == 4) return Word_sms(Naam, "java/lang/StringBuilder") || Word_sms(Naam, "java/lang/CharSequence");
        if (gebied_CODE == 10) return Word_sms(Naam, "java/util/ArrayList") || Word_sms(Naam, "java/util/List");
        if (gebied_CODE == 11) return Word_sms(Naam, "java/util/HashMap") || Word_sms(Naam, "java/util/Map");
        if (gebied_CODE == 12) return Word_sms(Naam, "java/lang/Integer") || Word_sms(Naam, "java/lang/Number");
        if (gebied_CODE >= 24 && gebied_CODE <= 28 && heap_WAARDE[object_verwijzen + 13] != 0) return 한국어화면종(Naam) == gebied_CODE || Word_sms(Naam, "Nederlands/Eigen/scherm_element");
        if (gebied_CODE >= 24 && gebied_CODE <= 28) return (한국어화면종(Naam) == 0 && scherm_les(Naam) == gebied_CODE) || Word_sms(Naam, "java/awt/Component") || Word_sms(Naam, "java/awt/Container") || Word_sms(Naam, "javax/swing/JComponent");
        if (gebied_CODE == 29) return Word_sms(Naam, heap_WAARDE[object_verwijzen + 3] != 0 ? "Nederlands/Eigen/Actie_kennisgeving" : "java/awt/event/ActionEvent");
        if (gebied_CODE == 30) return Word_sms(Naam, "java/awt/FlowLayout") || Word_sms(Naam, "java/awt/LayoutManager");
        if (gebied_CODE == 17) return Word_sms(Naam, "java/net/Socket");
        if (gebied_CODE == 18) return Word_sms(Naam, "java/net/ServerSocket");
        if (gebied_CODE == 19) return Word_sms(Naam, heap_WAARDE[object_verwijzen + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (gebied_CODE == 14) return Word_sms(Naam, "java/net/InetAddress");
        if (gebied_CODE == 15) return Word_sms(Naam, "java/net/DatagramSocket");
        if (gebied_CODE == 16) return Word_sms(Naam, "java/net/DatagramPacket");
        if (gebied_CODE == 13) return Word_sms(Naam, heap_WAARDE[object_verwijzen + 3] != 0 ? "Nederlands/Eigen/achtergrondwerker" : "java/lang/Thread");
        if (gebied_CODE == 2) return Word_sms(Naam, "[I"); if (gebied_CODE == 20) return Word_sms(Naam, "[B"); if (gebied_CODE == 21) return Word_sms(Naam, "[Z");
        if (gebied_CODE == 22) return Word_sms(Naam, "[C"); if (gebied_CODE == 23) return Word_sms(Naam, "[S");
        if (gebied_CODE != 3) return false;
        if (Word_sms(Naam, "[Ljava/lang/Object;")) return true;
        int onderdeel = matrixelement[object_verwijzen];
        if (onderdeel == -1) return Word_sms(Naam, "[Ljava/lang/String;") || Word_sms(Naam, "[Ljava/lang/CharSequence;");
        if (onderdeel == 0) return false;
        if (배열종비교(onderdeel, Naam)) return true;
        if ((Word_sms(onderdeel, "java/lang/String") || Word_sms(onderdeel, "java/lang/StringBuilder")) && Word_sms(Naam, "[Ljava/lang/CharSequence;")) return true;
        for (int lus_INDEX = 0; lus_INDEX < les_Definitie_AANTAL; lus_INDEX++) if (vereffenen_Word(les_Definitie_naam[lus_INDEX], onderdeel)) {
            for (int codepoint = lus_INDEX, 중첩깊이 = 0; codepoint >= 0 && 중첩깊이 < 16; 중첩깊이++, codepoint = bovenliggend_les(codepoint)) {
                if (배열종비교(les_Definitie_bovenliggend[codepoint], Naam)) return true;
                for (int inner_functie = 0; inner_functie < les_interface_AANTAL[codepoint]; inner_functie++) if (배열종비교(les_interface[codepoint * 16 + inner_functie], Naam)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int naam_constante, int 형식참조) {
        int cheque_functie = 상가[형식참조], invoer_AANTAL_8f7753a1 = constante_SECONDE_WAARDE[형식참조];
        if (naam_constante == 0 || invoer_AANTAL_8f7753a1 < 4 || bestand[cheque_functie] != '[' || bestand[cheque_functie + 1] != 'L' || bestand[cheque_functie + invoer_AANTAL_8f7753a1 - 1] != ';' || constante_SECONDE_WAARDE[naam_constante] != invoer_AANTAL_8f7753a1 - 3) return false;
        for (int lus_INDEX = 0; lus_INDEX < invoer_AANTAL_8f7753a1 - 3; lus_INDEX++) if (bestand[상가[naam_constante] + lus_INDEX] != bestand[cheque_functie + 2 + lus_INDEX]) return false;
        return true;
    }
    static void greep_uitzondering() {
        if (던진객체 == 0) return;
        fout = false;
        while (frame_INDEX >= actueel_thread * 32) {
            int Bestand_INDEX = frame_methode[frame_INDEX], 읽는자리 = frame_instructie[frame_INDEX];
            for (int lus_INDEX = 0; lus_INDEX < 잡기수; lus_INDEX++) if (잡기함수[lus_INDEX] == Bestand_INDEX && 읽는자리 >= 잡기시작[lus_INDEX] && 읽는자리 < 잡기끝[lus_INDEX]
                && (잡기종[lus_INDEX] == 0 || vereffenen_object(던진객체, 잡기종[lus_INDEX]))) {
                frame_functie[frame_INDEX] = 잡기위치[lus_INDEX]; frame_stack[frame_INDEX] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (initialiseren_frame[frame_INDEX] != 0) les_Definitie_Status[initialiseren_frame[frame_INDEX] - 1] = 3;
            if (frame_vergrendelen[frame_INDEX] != 0) { versie_vergrendelen(frame_vergrendelen[frame_INDEX]); frame_vergrendelen[frame_INDEX] = 0; }
            frame_INDEX--;
        }
        gebruikersruimte.Schrijven("Uncaught ");
        if (heap_WAARDE[던진객체] == 9) { gebruikersruimte.Schrijven(uitzondering_naam(heap_WAARDE[던진객체 + 2])); gebruikersruimte.Schrijven(": "); schrijven_sms(heap_WAARDE[던진객체 + 3]); }
        else gebruikersruimte.Schrijven("user exception");
        gebruikersruimte.schrijven_teken_WAARDE(10); 던진객체 = 0; fout = true;
    }
    // 이 JVM의 operand_stack 항목은 actueel_item category-1(int/reference)만 허용한다.
    static void stack_instructie(int opdracht_CODE) {
        int 첫값 = 빼기(0), 첫형식 = Retour_TYPE;
        if (opdracht_CODE == 87) return;
        if (opdracht_CODE == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int byte_gegevens = 빼기(0), SECONDE_opmaak = Retour_TYPE;
        if (opdracht_CODE == 88) return;
        if (opdracht_CODE == 90) { 넣기(첫값, 첫형식); 넣기(byte_gegevens, SECONDE_opmaak); 넣기(첫값, 첫형식); return; }
        if (opdracht_CODE == 92) { 넣기(byte_gegevens, SECONDE_opmaak); 넣기(첫값, 첫형식); 넣기(byte_gegevens, SECONDE_opmaak); 넣기(첫값, 첫형식); return; }
        if (opdracht_CODE == 95) { 넣기(첫값, 첫형식); 넣기(byte_gegevens, SECONDE_opmaak); return; }
        int codepoint = 빼기(0), 셋째형식 = Retour_TYPE;
        if (opdracht_CODE == 91) { 넣기(첫값, 첫형식); 넣기(codepoint, 셋째형식); 넣기(byte_gegevens, SECONDE_opmaak); 넣기(첫값, 첫형식); return; }
        if (opdracht_CODE == 93) { 넣기(byte_gegevens, SECONDE_opmaak); 넣기(첫값, 첫형식); 넣기(codepoint, 셋째형식); 넣기(byte_gegevens, SECONDE_opmaak); 넣기(첫값, 첫형식); return; }
        int navolgend_WAARDE = 빼기(0), 넷째형식 = Retour_TYPE;
        넣기(byte_gegevens, SECONDE_opmaak); 넣기(첫값, 첫형식); 넣기(navolgend_WAARDE, 넷째형식); 넣기(codepoint, 셋째형식); 넣기(byte_gegevens, SECONDE_opmaak); 넣기(첫값, 첫형식);
    }
    static void 새객체(int naam_constante, int 시작점) {
        int gebied_CODE = 0, geldig_tijdsduur = 0, uitzondering_verwijzen = uitzondering_constante(naam_constante);
        if (Word_sms(naam_constante, "java/lang/StringBuilder")) { gebied_CODE = 4; geldig_tijdsduur = 1; }
        if (Word_sms(naam_constante, "java/io/FileInputStream")) { gebied_CODE = 5; geldig_tijdsduur = 2; }
        if (Word_sms(naam_constante, "java/io/FileOutputStream")) { gebied_CODE = 6; geldig_tijdsduur = 2; }
        if (uitzondering_verwijzen != 0) { gebied_CODE = 9; geldig_tijdsduur = 2; }
        if (Word_sms(naam_constante, "java/util/ArrayList")) { gebied_CODE = 10; geldig_tijdsduur = 2; }
        if (Word_sms(naam_constante, "java/util/HashMap")) { gebied_CODE = 11; geldig_tijdsduur = 2; }
        if (Word_sms(naam_constante, "java/lang/Integer")) { gebied_CODE = 12; geldig_tijdsduur = 1; }
        if (Word_sms(naam_constante, "java/net/Socket")) { gebied_CODE = 17; geldig_tijdsduur = 5; }
        if (Word_sms(naam_constante, "java/net/ServerSocket")) { gebied_CODE = 18; geldig_tijdsduur = 5; }
        if (Word_sms(naam_constante, "java/net/DatagramSocket")) { gebied_CODE = 15; geldig_tijdsduur = 3; }
        if (Word_sms(naam_constante, "java/net/DatagramPacket")) { gebied_CODE = 16; geldig_tijdsduur = 4; }
        if (Word_sms(naam_constante, "java/lang/Thread") || Word_sms(naam_constante, "Nederlands/Eigen/achtergrondwerker")) { gebied_CODE = 13; geldig_tijdsduur = 2; }
        if (Word_sms(naam_constante, "java/lang/Object")) { gebied_CODE = 8; }
        if (gebied_CODE == 0 && scherm_les(naam_constante) != 0) { gebied_CODE = scherm_les(naam_constante); geldig_tijdsduur = 12; }
        if (gebied_CODE == 0) {
            int codepoint = Zoeken_les_Definitie(naam_constante); if (codepoint < 0 || fout || !initialiseren(codepoint, 시작점)) return;
            gebied_CODE = 32 + codepoint; geldig_tijdsduur = les_sleuf_AANTAL[codepoint];
        }
        int object_verwijzen = toewijzen_Opslag(gebied_CODE, geldig_tijdsduur); if (fout) return;
        if (gebied_CODE == 13 && Word_sms(naam_constante, "Nederlands/Eigen/achtergrondwerker")) heap_WAARDE[object_verwijzen + 3] = 1;
        if (gebied_CODE >= 24 && gebied_CODE <= 28 && 한국어화면종(naam_constante) != 0) heap_WAARDE[object_verwijzen + 13] = 1;
        if (gebied_CODE == 5 || gebied_CODE == 6 || gebied_CODE == 15 || gebied_CODE == 17 || gebied_CODE == 18) heap_WAARDE[object_verwijzen + 2] = -1;
        if (gebied_CODE == 9) heap_WAARDE[object_verwijzen + 2] = uitzondering_verwijzen;
        넣기(object_verwijzen, 2);
    }
    static boolean 값같음(int 첫값, int byte_gegevens) {
        if (첫값 == byte_gegevens) return true;
        if (첫값 == 0 || byte_gegevens == 0 || 첫값 < 0 || byte_gegevens < 0 || 첫값 >= heap_beëindigen_functie || byte_gegevens >= heap_beëindigen_functie) return false;
        if (heap_WAARDE[첫값] == 1 && heap_WAARDE[byte_gegevens] == 1) return teksten_gelijk(첫값, byte_gegevens, false);
        return heap_WAARDE[첫값] == 12 && heap_WAARDE[byte_gegevens] == 12 && heap_WAARDE[첫값 + 2] == heap_WAARDE[byte_gegevens + 2];
    }
    static int 글조각(int object_verwijzen, int START_functie, int beëindigen_functie) {
        if (!object_WAARDE(object_verwijzen, 1)) return 0;
        if (START_functie < 0 || beëindigen_functie < START_functie || beëindigen_functie > heap_WAARDE[object_verwijzen + 1]) { fout_WAARDE("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = toewijzen_Opslag(1, beëindigen_functie - START_functie); if (fout) return 0;
        for (int lus_INDEX = START_functie; lus_INDEX < beëindigen_functie; lus_INDEX++) heap_WAARDE[반환값 + 2 + lus_INDEX - START_functie] = heap_WAARDE[object_verwijzen + 2 + lus_INDEX];
        return 반환값;
    }
    static int join_sms(int 첫값, int byte_gegevens) {
        if (!object_WAARDE(첫값, 1) || !object_WAARDE(byte_gegevens, 1)) return 0;
        int invoer_AANTAL_8f7753a1 = heap_WAARDE[첫값 + 1], methode_INDEX = heap_WAARDE[byte_gegevens + 1], 반환값 = toewijzen_Opslag(1, invoer_AANTAL_8f7753a1 + methode_INDEX); if (fout) return 0;
        for (int lus_INDEX = 0; lus_INDEX < invoer_AANTAL_8f7753a1; lus_INDEX++) heap_WAARDE[반환값 + 2 + lus_INDEX] = heap_WAARDE[첫값 + 2 + lus_INDEX];
        for (int lus_INDEX = 0; lus_INDEX < methode_INDEX; lus_INDEX++) heap_WAARDE[반환값 + 2 + invoer_AANTAL_8f7753a1 + lus_INDEX] = heap_WAARDE[byte_gegevens + 2 + lus_INDEX];
        return 반환값;
    }
    static boolean 기본호출(int eigenaar, int naam_constante, int 서술상수, int opdracht_CODE) {
        if (Word_sms(eigenaar, "Nederlands/Eigen/실행인수") && opdracht_CODE == 184) {
            if (Word_sms(naam_constante, "item_AANTAL") && Word_sms(서술상수, "()I")) { 넣기(gebruikersruimte.인수개수() - 1, 1); return true; }
            if (Word_sms(naam_constante, "tekst") && Word_sms(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= gebruikersruimte.인수개수() - 1) 예외던짐(29, "Uitvoeren_opdracht argumenten 범위를 벗어났습니다");
                else 넣기(host_teken(gebruikersruimte.argumenten(순번 + 1)), 2);
                return true;
            }
            fout_WAARDE("지원하지 않는 Nederlands Uitvoeren_opdracht argumenten 호출"); return true;
        }
        if (Word_sms(eigenaar, "Nederlands/Eigen/achtergrondwerker")) { Proces_thread(naam_constante, 서술상수, opdracht_CODE, true); return true; }
        if (한국어화면소유(eigenaar)) { 한국어화면호출(eigenaar, naam_constante, 서술상수, opdracht_CODE); return true; }
        if (scherm_eigenaar(eigenaar)) { 화면호출(eigenaar, naam_constante, 서술상수, opdracht_CODE); return true; }
        if (Word_sms(eigenaar, "java/net/Socket") || Word_sms(eigenaar, "java/net/ServerSocket") || Word_sms(eigenaar, "java/io/InputStream") || Word_sms(eigenaar, "java/io/OutputStream")) { 흐름호출(eigenaar, naam_constante, 서술상수, opdracht_CODE); return true; }
        if (Word_sms(eigenaar, "Nederlands/Eigen/kernel_WAARDE") && opdracht_CODE == 184) {
            if (Word_sms(naam_constante, "화면너비") && Word_sms(서술상수, "()I")) { 넣기(gebruikersruimte.화면너비(), 1); return true; }
            if (Word_sms(naam_constante, "scherm_hoogte") && Word_sms(서술상수, "()I")) { 넣기(gebruikersruimte.scherm_hoogte(), 1); return true; }
            if (Word_sms(naam_constante, "밀리초") && Word_sms(서술상수, "()I")) { 넣기(gebruikersruimte.밀리초(), 1); return true; }
            if (Word_sms(naam_constante, "그림대기") && Word_sms(서술상수, "()I")) { 넣기(gebruikersruimte.그림대기(), 1); return true; }
            if (Word_sms(naam_constante, "rechthoek") && Word_sms(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), hoogte_WAARDE = 빼기(1), 너비 = 빼기(1), Y_coördinaat = 빼기(1), x_coördinaat = 빼기(1); 넣기(gebruikersruimte.rechthoek(x_coördinaat, Y_coördinaat, 너비, hoogte_WAARDE, 색상), 1); return true; }
        }
        if (Word_sms(eigenaar, "java/net/InetAddress") || Word_sms(eigenaar, "java/net/DatagramPacket") || Word_sms(eigenaar, "java/net/DatagramSocket")) { 통신호출(eigenaar, naam_constante, 서술상수, opdracht_CODE); return true; }
        if (Word_sms(eigenaar, "java/lang/Thread")) { 가닥호출(naam_constante, 서술상수, opdracht_CODE); return true; }
        if (Word_sms(eigenaar, "java/lang/Object")) {
            if (Word_sms(naam_constante, "<init>") && Word_sms(서술상수, "()V") && opdracht_CODE == 183) { informatie_geldig_object(빼기(2)); return true; }
            if (Word_sms(naam_constante, "equals") && Word_sms(서술상수, "(Ljava/lang/Object;)Z")) { int byte_gegevens = 빼기(2), 첫값 = 빼기(2); if (informatie_geldig_object(첫값)) 넣기(첫값 == byte_gegevens ? 1 : 0, 1); return true; }
        }
        if (uitzondering_constante(eigenaar) != 0) {
            if (Word_sms(naam_constante, "<init>") && opdracht_CODE == 183 && (Word_sms(서술상수, "()V") || Word_sms(서술상수, "(Ljava/lang/String;)V"))) {
                int prompt = Word_sms(서술상수, "()V") ? 0 : 빼기(2), object_verwijzen = 빼기(2);
                if (object_WAARDE(object_verwijzen, 9)) { heap_WAARDE[object_verwijzen + 3] = prompt; heap_verwijzen[object_verwijzen + 3] = 1; } return true;
            }
            if ((Word_sms(naam_constante, "getMessage") || Word_sms(naam_constante, "설명")) && Word_sms(서술상수, "()Ljava/lang/String;")) { int object_verwijzen = 빼기(2); if (object_WAARDE(object_verwijzen, 9)) 넣기(heap_WAARDE[object_verwijzen + 3], 2); return true; }
        }
        if (Word_sms(eigenaar, "java/lang/String")) {
            if (opdracht_CODE == 182 && Word_sms(naam_constante, "getBytes") && (Word_sms(서술상수, "()[B") || Word_sms(서술상수, "(Ljava/lang/String;)[B"))) {
                int Encoding_naam = Word_sms(서술상수, "()[B") ? 0 : 빼기(2), object_verwijzen = 빼기(2);
                if (!object_WAARDE(object_verwijzen, 1)) return true;
                if (Encoding_naam != 0 && !teksten_gelijk(Encoding_naam, host_teken("UTF-8"), false) && !teksten_gelijk(Encoding_naam, host_teken("UTF8"), false) && !teksten_gelijk(Encoding_naam, host_teken("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int invoer_AANTAL_8f7753a1 = heap_WAARDE[object_verwijzen + 1], 반환값 = toewijzen_Opslag(20, invoer_AANTAL_8f7753a1 * 3), 사용수 = 0; if (fout) return true;
                for (int inner_functie = 0; inner_functie < invoer_AANTAL_8f7753a1; inner_functie++) {
                    int codepoint = heap_WAARDE[object_verwijzen + 2 + inner_functie];
                    if (codepoint >= 0xd800 && codepoint <= 0xdbff && inner_functie + 1 < invoer_AANTAL_8f7753a1 && heap_WAARDE[object_verwijzen + 3 + inner_functie] >= 0xdc00 && heap_WAARDE[object_verwijzen + 3 + inner_functie] <= 0xdfff) codepoint = 0x10000 + ((codepoint - 0xd800) << 10) + heap_WAARDE[object_verwijzen + 2 + ++inner_functie] - 0xdc00;
                    else if (codepoint >= 0xd800 && codepoint <= 0xdfff) codepoint = '?';
                    if (codepoint < 128) heap_WAARDE[반환값 + 2 + 사용수++] = codepoint;
                    else { int byte_AANTAL = codepoint < 2048 ? 2 : codepoint < 65536 ? 3 : 4; heap_WAARDE[반환값 + 2 + 사용수++] = (byte)((byte_AANTAL == 2 ? 192 : byte_AANTAL == 3 ? 224 : 240) | codepoint >> (6 * (byte_AANTAL - 1))); for (int Vergelijking_functie = byte_AANTAL - 1; Vergelijking_functie > 0; Vergelijking_functie--) heap_WAARDE[반환값 + 2 + 사용수++] = (byte)(128 | codepoint >> (6 * (Vergelijking_functie - 1)) & 63); }
                }
                heap_WAARDE[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (opdracht_CODE == 184 && Word_sms(naam_constante, "valueOf") && Word_sms(서술상수, "(I)Ljava/lang/String;")) { 넣기(cijfer_teken(빼기(1)), 2); return true; }
            if (opdracht_CODE != 182) return false;
            if (Word_sms(naam_constante, "equals") && Word_sms(서술상수, "(Ljava/lang/Object;)Z")) { int byte_gegevens = 빼기(2), 첫값 = 빼기(2); if (object_WAARDE(첫값, 1)) 넣기(teksten_gelijk(첫값, byte_gegevens, false) ? 1 : 0, 1); return true; }
            if (Word_sms(naam_constante, "isEmpty") && Word_sms(서술상수, "()Z")) { int 첫값 = 빼기(2); if (object_WAARDE(첫값, 1)) 넣기(heap_WAARDE[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Word_sms(naam_constante, "substring") && (Word_sms(서술상수, "(I)Ljava/lang/String;") || Word_sms(서술상수, "(II)Ljava/lang/String;"))) {
                boolean SECONDE_WAARDE = Word_sms(서술상수, "(II)Ljava/lang/String;"); int beëindigen_functie = SECONDE_WAARDE ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (object_WAARDE(첫값, 1)) 넣기(글조각(첫값, 시작점, SECONDE_WAARDE ? beëindigen_functie : heap_WAARDE[첫값 + 1]), 2); return true;
            }
            if (Word_sms(naam_constante, "concat") && Word_sms(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int byte_gegevens = 빼기(2), 첫값 = 빼기(2); 넣기(join_sms(첫값, byte_gegevens), 2); return true; }
            if (Word_sms(naam_constante, "hashCode") && Word_sms(서술상수, "()I")) { int 첫값 = 빼기(2), hash_WAARDE = 0; if (object_WAARDE(첫값, 1)) { for (int lus_INDEX = 0; lus_INDEX < heap_WAARDE[첫값 + 1]; lus_INDEX++) hash_WAARDE = hash_WAARDE * 31 + heap_WAARDE[첫값 + 2 + lus_INDEX]; 넣기(hash_WAARDE, 1); } return true; }
            if (Word_sms(naam_constante, "toString") && Word_sms(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (object_WAARDE(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Word_sms(eigenaar, "java/lang/Integer")) {
            if (opdracht_CODE == 184 && Word_sms(naam_constante, "valueOf") && Word_sms(서술상수, "(I)Ljava/lang/Integer;")) { int gegevens_WAARDE = 빼기(1), object_verwijzen = gegevens_WAARDE >= -128 && gegevens_WAARDE <= 127 ? Store_geheel_getal[gegevens_WAARDE + 128] : 0; if (object_verwijzen == 0) { object_verwijzen = toewijzen_Opslag(12, 1); if (!fout) { heap_WAARDE[object_verwijzen + 2] = gegevens_WAARDE; if (gegevens_WAARDE >= -128 && gegevens_WAARDE <= 127) Store_geheel_getal[gegevens_WAARDE + 128] = object_verwijzen; } } 넣기(object_verwijzen, 2); return true; }
            if (opdracht_CODE == 183 && Word_sms(naam_constante, "<init>") && Word_sms(서술상수, "(I)V")) { int gegevens_WAARDE = 빼기(1), object_verwijzen = 빼기(2); if (object_WAARDE(object_verwijzen, 12)) heap_WAARDE[object_verwijzen + 2] = gegevens_WAARDE; return true; }
            if (opdracht_CODE == 182 && Word_sms(naam_constante, "intValue") && Word_sms(서술상수, "()I")) { int object_verwijzen = 빼기(2); if (object_WAARDE(object_verwijzen, 12)) 넣기(heap_WAARDE[object_verwijzen + 2], 1); return true; }
            if (opdracht_CODE == 184 && Word_sms(naam_constante, "toString") && Word_sms(서술상수, "(I)Ljava/lang/String;")) { 넣기(cijfer_teken(빼기(1)), 2); return true; }
        }
        if (Word_sms(eigenaar, "java/lang/Math") && opdracht_CODE == 184) {
            if (Word_sms(naam_constante, "abs") && Word_sms(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((Word_sms(naam_constante, "min") || Word_sms(naam_constante, "max")) && Word_sms(서술상수, "(II)I")) { int byte_gegevens = 빼기(1), 첫값 = 빼기(1); 넣기(Word_sms(naam_constante, "min") ? (첫값 < byte_gegevens ? 첫값 : byte_gegevens) : (첫값 > byte_gegevens ? 첫값 : byte_gegevens), 1); return true; }
        }
        if (Word_sms(eigenaar, "java/lang/System") && opdracht_CODE == 184) {
            if (Word_sms(naam_constante, "gc") && Word_sms(서술상수, "()V")) { 수거(); return true; }
            if (Word_sms(naam_constante, "arraycopy") && Word_sms(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int invoer_AANTAL_8f7753a1 = 빼기(1), doel_WAARDE_INDEX = 빼기(1), byte_gegevens = 빼기(2), START_functie = 빼기(1), 첫값 = 빼기(2);
                if (informatie_geldig_object(첫값) && informatie_geldig_object(byte_gegevens)) {
                    int gebied_CODE = heap_WAARDE[첫값];
                    if (heap_WAARDE[byte_gegevens] != gebied_CODE || (gebied_CODE != 2 && gebied_CODE != 3 && (gebied_CODE < 20 || gebied_CODE > 23))) fout_WAARDE("arraycopy type mismatch");
                    else if (invoer_AANTAL_8f7753a1 < 0 || START_functie < 0 || doel_WAARDE_INDEX < 0 || START_functie > heap_WAARDE[첫값 + 1] - invoer_AANTAL_8f7753a1 || doel_WAARDE_INDEX > heap_WAARDE[byte_gegevens + 1] - invoer_AANTAL_8f7753a1) fout_WAARDE("ArrayIndexOutOfBoundsException");
                    else if (첫값 == byte_gegevens && doel_WAARDE_INDEX > START_functie) { for (int lus_INDEX = invoer_AANTAL_8f7753a1 - 1; lus_INDEX >= 0; lus_INDEX--) heap_WAARDE[byte_gegevens + 2 + doel_WAARDE_INDEX + lus_INDEX] = heap_WAARDE[첫값 + 2 + START_functie + lus_INDEX]; }
                    else { for (int lus_INDEX = 0; lus_INDEX < invoer_AANTAL_8f7753a1 && !fout; lus_INDEX++) { int gegevens_WAARDE = heap_WAARDE[첫값 + 2 + START_functie + lus_INDEX]; if (gebied_CODE != 3 || 배열저장가능(byte_gegevens, gegevens_WAARDE)) heap_WAARDE[byte_gegevens + 2 + doel_WAARDE_INDEX + lus_INDEX] = gegevens_WAARDE; } }
                }
                return true;
            }
        }
        if (Word_sms(eigenaar, "java/util/ArrayList") || Word_sms(eigenaar, "java/util/List") || Word_sms(eigenaar, "java/util/HashMap") || Word_sms(eigenaar, "java/util/Map")) {
            모음호출(eigenaar, naam_constante, 서술상수, opdracht_CODE); return true;
        }
        return false;
    }
    static void 모음늘리기(int object_verwijzen, int 필요수) {
        int Vorige_WAARDE = heap_WAARDE[object_verwijzen + 2], capaciteit_gegevens = Vorige_WAARDE == 0 ? 0 : heap_WAARDE[Vorige_WAARDE + 1];
        if (capaciteit_gegevens >= 필요수) return;
        int Volgende_functie = capaciteit_gegevens < 8 ? 8 : capaciteit_gegevens * 2; if (Volgende_functie < 필요수) Volgende_functie = 필요수;
        int gegevens_MATRIX = toewijzen_Opslag(3, Volgende_functie); if (fout) return;
        for (int lus_INDEX = 0; lus_INDEX < capaciteit_gegevens; lus_INDEX++) heap_WAARDE[gegevens_MATRIX + 2 + lus_INDEX] = heap_WAARDE[Vorige_WAARDE + 2 + lus_INDEX];
        heap_WAARDE[object_verwijzen + 2] = gegevens_MATRIX; heap_verwijzen[object_verwijzen + 2] = 1;
    }
    static void 모음호출(int eigenaar, int naam_constante, int 서술상수, int opdracht_CODE) {
        boolean 대응참조 = Word_sms(eigenaar, "java/util/HashMap") || Word_sms(eigenaar, "java/util/Map"); int gebied_CODE = 대응참조 ? 11 : 10;
        if (Word_sms(naam_constante, "<init>") && opdracht_CODE == 183 && Word_sms(서술상수, "()V")) { int object_verwijzen = 빼기(2); if (object_WAARDE(object_verwijzen, gebied_CODE)) 모음늘리기(object_verwijzen, 8); return; }
        if (opdracht_CODE != 182 && opdracht_CODE != 185) { fout_WAARDE("invalid collection invocation"); return; }
        if (Word_sms(naam_constante, "size") && Word_sms(서술상수, "()I") || Word_sms(naam_constante, "isEmpty") && Word_sms(서술상수, "()Z")) {
            int object_verwijzen = 빼기(2); if (object_WAARDE(object_verwijzen, gebied_CODE)) 넣기(Word_sms(naam_constante, "size") ? heap_WAARDE[object_verwijzen + 3] : heap_WAARDE[object_verwijzen + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Word_sms(naam_constante, "clear") && Word_sms(서술상수, "()V")) { int object_verwijzen = 빼기(2); if (object_WAARDE(object_verwijzen, gebied_CODE)) { int gegevens_MATRIX = heap_WAARDE[object_verwijzen + 2]; for (int lus_INDEX = 0; lus_INDEX < heap_WAARDE[gegevens_MATRIX + 1]; lus_INDEX++) heap_WAARDE[gegevens_MATRIX + 2 + lus_INDEX] = 0; heap_WAARDE[object_verwijzen + 3] = 0; } return; }
        if (!대응참조 && Word_sms(naam_constante, "add") && Word_sms(서술상수, "(Ljava/lang/Object;)Z")) {
            int gegevens_WAARDE = 빼기(2), object_verwijzen = 빼기(2); if (!object_WAARDE(object_verwijzen, 10)) return;
            int invoer_AANTAL_8f7753a1 = heap_WAARDE[object_verwijzen + 3]; 모음늘리기(object_verwijzen, invoer_AANTAL_8f7753a1 + 1); if (!fout) { heap_WAARDE[heap_WAARDE[object_verwijzen + 2] + 2 + invoer_AANTAL_8f7753a1] = gegevens_WAARDE; heap_WAARDE[object_verwijzen + 3] = invoer_AANTAL_8f7753a1 + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Word_sms(naam_constante, "get") || Word_sms(naam_constante, "remove")) && Word_sms(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && Word_sms(naam_constante, "set") && Word_sms(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean informatie_Toegewezen = Word_sms(naam_constante, "set"); int gegevens_WAARDE = informatie_Toegewezen ? 빼기(2) : 0, invoer_functie_206f1c6d = 빼기(1), object_verwijzen = 빼기(2);
            if (!object_WAARDE(object_verwijzen, 10)) return;
            int invoer_AANTAL_8f7753a1 = heap_WAARDE[object_verwijzen + 3], gegevens_MATRIX = heap_WAARDE[object_verwijzen + 2];
            if (invoer_functie_206f1c6d < 0 || invoer_functie_206f1c6d >= invoer_AANTAL_8f7753a1) { 예외던짐(6, "list index"); return; }
            int Vorige_WAARDE = heap_WAARDE[gegevens_MATRIX + 2 + invoer_functie_206f1c6d];
            if (informatie_Toegewezen) heap_WAARDE[gegevens_MATRIX + 2 + invoer_functie_206f1c6d] = gegevens_WAARDE;
            if (Word_sms(naam_constante, "remove")) { for (int lus_INDEX = invoer_functie_206f1c6d + 1; lus_INDEX < invoer_AANTAL_8f7753a1; lus_INDEX++) heap_WAARDE[gegevens_MATRIX + 1 + lus_INDEX] = heap_WAARDE[gegevens_MATRIX + 2 + lus_INDEX]; heap_WAARDE[gegevens_MATRIX + 1 + invoer_AANTAL_8f7753a1] = 0; heap_WAARDE[object_verwijzen + 3] = invoer_AANTAL_8f7753a1 - 1; }
            넣기(Vorige_WAARDE, 2); return;
        }
        if (대응참조 && (Word_sms(naam_constante, "get") || Word_sms(naam_constante, "remove")) && Word_sms(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_sms(naam_constante, "put") && Word_sms(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_sms(naam_constante, "containsKey") && Word_sms(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Word_sms(naam_constante, "put"), verwijderen = Word_sms(naam_constante, "remove");
            int gegevens_WAARDE = 넣기여부 ? 빼기(2) : 0, toets_verwijzen = 빼기(2), object_verwijzen = 빼기(2); if (!object_WAARDE(object_verwijzen, 11)) return;
            int invoer_AANTAL_8f7753a1 = heap_WAARDE[object_verwijzen + 3], gegevens_MATRIX = heap_WAARDE[object_verwijzen + 2], 찾은여부 = -1;
            for (int lus_INDEX = 0; lus_INDEX < invoer_AANTAL_8f7753a1; lus_INDEX++) if (값같음(toets_verwijzen, heap_WAARDE[gegevens_MATRIX + 2 + 2 * lus_INDEX])) { 찾은여부 = lus_INDEX; break; }
            int Vorige_WAARDE = 찾은여부 < 0 ? 0 : heap_WAARDE[gegevens_MATRIX + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(object_verwijzen, (invoer_AANTAL_8f7753a1 + 1) * 2); gegevens_MATRIX = heap_WAARDE[object_verwijzen + 2]; 찾은여부 = invoer_AANTAL_8f7753a1; if (!fout) heap_WAARDE[object_verwijzen + 3] = invoer_AANTAL_8f7753a1 + 1; }
                if (!fout) { heap_WAARDE[gegevens_MATRIX + 2 + 2 * 찾은여부] = toets_verwijzen; heap_WAARDE[gegevens_MATRIX + 3 + 2 * 찾은여부] = gegevens_WAARDE; }
            }
            if (verwijderen && 찾은여부 >= 0) { for (int lus_INDEX = 찾은여부 + 1; lus_INDEX < invoer_AANTAL_8f7753a1; lus_INDEX++) { heap_WAARDE[gegevens_MATRIX + 2 * lus_INDEX] = heap_WAARDE[gegevens_MATRIX + 2 + 2 * lus_INDEX]; heap_WAARDE[gegevens_MATRIX + 1 + 2 * lus_INDEX] = heap_WAARDE[gegevens_MATRIX + 3 + 2 * lus_INDEX]; } heap_WAARDE[gegevens_MATRIX + 2 * invoer_AANTAL_8f7753a1] = 0; heap_WAARDE[gegevens_MATRIX + 1 + 2 * invoer_AANTAL_8f7753a1] = 0; heap_WAARDE[object_verwijzen + 3] = invoer_AANTAL_8f7753a1 - 1; }
            if (Word_sms(naam_constante, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(Vorige_WAARDE, 2);
            return;
        }
        fout_WAARDE("unsupported collection method");
    }
    static boolean 잠금얻기(int object_verwijzen) {
        if (!informatie_geldig_object(object_verwijzen)) return false;
        if (잠금깊이[object_verwijzen] != 0 && vergrendelen_eigenaar[object_verwijzen] != actueel_thread + 1) { wijzigingsaanvraag = true; return false; }
        vergrendelen_eigenaar[object_verwijzen] = actueel_thread + 1; 잠금깊이[object_verwijzen]++; return true;
    }
    static void versie_vergrendelen(int object_verwijzen) {
        if (!informatie_geldig_object(object_verwijzen)) return;
        if (잠금깊이[object_verwijzen] == 0 || vergrendelen_eigenaar[object_verwijzen] != actueel_thread + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[object_verwijzen] == 0) vergrendelen_eigenaar[object_verwijzen] = 0;
    }
    static boolean switch_thread() {
        thread_frame[actueel_thread] = frame_INDEX;
        if (frame_INDEX < actueel_thread * 32) thread_Status[actueel_thread] = 3;
        for (int lus_INDEX = 0; lus_INDEX < aantal_threads; lus_INDEX++) if (thread_Status[lus_INDEX] == 2 && thread_Status[가닥대기[lus_INDEX]] == 3) thread_Status[lus_INDEX] = 1;
        for (int lus_INDEX = 1; lus_INDEX <= aantal_threads; lus_INDEX++) {
            int Volgende_functie = (actueel_thread + lus_INDEX) % aantal_threads;
            if (thread_Status[Volgende_functie] == 1) { actueel_thread = Volgende_functie; frame_INDEX = thread_frame[Volgende_functie]; wijzigingsaanvraag = false; return true; }
        }
        for (int lus_INDEX = 0; lus_INDEX < aantal_threads; lus_INDEX++) if (thread_Status[lus_INDEX] != 3) { fout_WAARDE("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int naam_constante, int 서술상수, int opdracht_CODE) { Proces_thread(naam_constante, 서술상수, opdracht_CODE, false); }
    static void Proces_thread(int naam_constante, int 서술상수, int opdracht_CODE, boolean Nederlands) {
        if (opdracht_CODE == 184 && Word_sms(naam_constante, Nederlands ? "RENDEMENT_taak" : "yield") && Word_sms(서술상수, "()V")) { wijzigingsaanvraag = true; return; }
        if (opdracht_CODE == 184 && Word_sms(naam_constante, "currentThread") && Word_sms(서술상수, "()Ljava/lang/Thread;")) { 넣기(thread_object[actueel_thread], 2); return; }
        if (opdracht_CODE == 183 && Word_sms(naam_constante, "<init>") && (Word_sms(서술상수, "()V") || Word_sms(서술상수, Nederlands ? "(LNederlands/Eigen/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int doel_ADRES = Word_sms(서술상수, "()V") ? 0 : 빼기(2), object_verwijzen = 빼기(2);
            if (!informatie_geldig_object(object_verwijzen)) return;
            if (heap_WAARDE[object_verwijzen] == 13) { heap_WAARDE[object_verwijzen + 2] = doel_ADRES; heap_verwijzen[object_verwijzen + 2] = 1; }
            else if (doel_ADRES != 0) fout_WAARDE("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (opdracht_CODE == 182 && (Word_sms(naam_constante, Nederlands ? "START_taak" : "start") || Word_sms(naam_constante, Nederlands ? "기다리기" : "join")) && Word_sms(서술상수, "()V") || opdracht_CODE == 182 && Word_sms(naam_constante, Nederlands ? "살아있는가" : "isAlive") && Word_sms(서술상수, "()Z")) {
            int object_verwijzen = 빼기(2); if (!informatie_geldig_object(object_verwijzen)) return;
            int account_WAARDE = -1; for (int lus_INDEX = 0; lus_INDEX < aantal_threads; lus_INDEX++) if (thread_object[lus_INDEX] == object_verwijzen) account_WAARDE = lus_INDEX;
            if (Word_sms(naam_constante, Nederlands ? "살아있는가" : "isAlive")) { 넣기(account_WAARDE >= 0 && thread_Status[account_WAARDE] != 3 ? 1 : 0, 1); return; }
            if (Word_sms(naam_constante, Nederlands ? "기다리기" : "join")) { if (account_WAARDE >= 0 && thread_Status[account_WAARDE] != 3) { 가닥대기[actueel_thread] = account_WAARDE; thread_Status[actueel_thread] = 2; wijzigingsaanvraag = true; } return; }
            if (account_WAARDE >= 0) { 예외던짐(Nederlands ? 38 : 16, "thread already started"); return; }
            if (aantal_threads == 4) { fout_WAARDE("thread limit (4 including main)"); return; }
            int doel_ADRES = heap_WAARDE[object_verwijzen] == 13 ? heap_WAARDE[object_verwijzen + 2] : object_verwijzen;
            int Bestand_INDEX = doel_ADRES > 0 && heap_WAARDE[doel_ADRES] >= 32 ? naam_methode(heap_WAARDE[doel_ADRES] - 32, Nederlands ? "Uitvoeren" : "run", "()V") : -1;
            if (doel_ADRES != 0 && Bestand_INDEX < 0) { fout_WAARDE("Runnable.run required"); return; }
            account_WAARDE = aantal_threads++; thread_object[account_WAARDE] = object_verwijzen; thread_doel[account_WAARDE] = doel_ADRES;
            int frame = account_WAARDE * 32; thread_frame[account_WAARDE] = Bestand_INDEX < 0 ? frame - 1 : frame; thread_Status[account_WAARDE] = Bestand_INDEX < 0 ? 3 : 1;
            if (Bestand_INDEX >= 0) { frame_methode[frame] = Bestand_INDEX; frame_functie[frame] = methode_START[Bestand_INDEX]; lokaal_WAARDE[frame * 128] = doel_ADRES; lokaal_TYPE[frame * 128] = 2; }
            return;
        }
        fout_WAARDE("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], ADRES_sms = new int[16];
    static int lokaal_ADRES() { return ADRES_object(0x7f000001); }
    static int ADRES_object(int WAARDE) { int object_verwijzen = toewijzen_Opslag(14, 1); if (!fout) heap_WAARDE[object_verwijzen + 2] = WAARDE; return object_verwijzen; }
    static int 주소해독(int object_verwijzen) {
        if (object_verwijzen == 0 || teksten_gelijk(object_verwijzen, host_teken("localhost"), false)) return 0x7f000001;
        if (!object_WAARDE(object_verwijzen, 1)) return 0;
        int gegevens_WAARDE = 0, totaal_AANTAL = 0, ADRES_byte = 0, 자릿수 = 0, invoer_AANTAL_8f7753a1 = heap_WAARDE[object_verwijzen + 1];
        for (int lus_INDEX = 0; lus_INDEX <= invoer_AANTAL_8f7753a1; lus_INDEX++) {
            int codepoint = lus_INDEX == invoer_AANTAL_8f7753a1 ? '.' : heap_WAARDE[object_verwijzen + 2 + lus_INDEX];
            if (codepoint == '.') { if (자릿수 == 0 || totaal_AANTAL == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } gegevens_WAARDE = gegevens_WAARDE << 8 | ADRES_byte; totaal_AANTAL++; ADRES_byte = 자릿수 = 0; }
            else { if (codepoint < '0' || codepoint > '9' || ++자릿수 > 3 || (ADRES_byte = ADRES_byte * 10 + codepoint - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (totaal_AANTAL != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return gegevens_WAARDE;
    }
    static int ADRES_teken(int gegevens_WAARDE) {
        int invoer_AANTAL_8f7753a1 = 0;
        for (int verplaatsen = 24; verplaatsen >= 0; verplaatsen -= 8) {
            int ADRES_byte = gegevens_WAARDE >>> verplaatsen & 255;
            if (ADRES_byte >= 100) ADRES_sms[invoer_AANTAL_8f7753a1++] = '0' + ADRES_byte / 100;
            if (ADRES_byte >= 10) ADRES_sms[invoer_AANTAL_8f7753a1++] = '0' + ADRES_byte / 10 % 10;
            ADRES_sms[invoer_AANTAL_8f7753a1++] = '0' + ADRES_byte % 10; if (verplaatsen != 0) ADRES_sms[invoer_AANTAL_8f7753a1++] = '.';
        }
        int object_verwijzen = toewijzen_Opslag(1, invoer_AANTAL_8f7753a1); if (!fout) for (int lus_INDEX = 0; lus_INDEX < invoer_AANTAL_8f7753a1; lus_INDEX++) heap_WAARDE[object_verwijzen + 2 + lus_INDEX] = ADRES_sms[lus_INDEX]; return object_verwijzen;
    }
    static void 통신호출(int eigenaar, int naam_constante, int 서술상수, int opdracht_CODE) {
        if (Word_sms(eigenaar, "java/net/InetAddress")) {
            if (opdracht_CODE == 184 && Word_sms(naam_constante, "getLoopbackAddress") && Word_sms(서술상수, "()Ljava/net/InetAddress;")) { 넣기(lokaal_ADRES(), 2); return; }
            if (opdracht_CODE == 184 && Word_sms(naam_constante, "getByName") && Word_sms(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int gegevens_WAARDE = 주소해독(빼기(2)); if (던진객체 == 0 && !fout) 넣기(ADRES_object(gegevens_WAARDE), 2); return;
            }
            if (opdracht_CODE == 182 && Word_sms(naam_constante, "getHostAddress") && Word_sms(서술상수, "()Ljava/lang/String;")) { int object_verwijzen = 빼기(2); if (object_WAARDE(object_verwijzen, 14)) 넣기(ADRES_teken(heap_WAARDE[object_verwijzen + 2]), 2); return; }
        }
        if (Word_sms(eigenaar, "java/net/DatagramPacket")) {
            if (opdracht_CODE == 183 && Word_sms(naam_constante, "<init>") && (Word_sms(서술상수, "([BI)V") || Word_sms(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean doel_WAARDE_verwijzen = Word_sms(서술상수, "([BILjava/net/InetAddress;I)V"); int poortnummer = doel_WAARDE_verwijzen ? 빼기(1) : 0, ADRES_verwijzen = doel_WAARDE_verwijzen ? 빼기(2) : 0;
                int invoer_AANTAL_8f7753a1 = 빼기(1), gegevens_MATRIX = 빼기(2), object_verwijzen = 빼기(2);
                if (!object_WAARDE(object_verwijzen, 16) || !object_WAARDE(gegevens_MATRIX, 20)) return;
                if (invoer_AANTAL_8f7753a1 < 0 || invoer_AANTAL_8f7753a1 > heap_WAARDE[gegevens_MATRIX + 1] || poortnummer < 0 || poortnummer > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (ADRES_verwijzen != 0 && !object_WAARDE(ADRES_verwijzen, 14)) return;
                heap_WAARDE[object_verwijzen + 2] = gegevens_MATRIX; heap_verwijzen[object_verwijzen + 2] = 1; heap_WAARDE[object_verwijzen + 3] = invoer_AANTAL_8f7753a1;
                heap_WAARDE[object_verwijzen + 4] = ADRES_verwijzen; heap_verwijzen[object_verwijzen + 4] = 1; heap_WAARDE[object_verwijzen + 5] = poortnummer; return;
            }
            if (opdracht_CODE == 182 && Word_sms(naam_constante, "setLength") && Word_sms(서술상수, "(I)V")) {
                int invoer_AANTAL_8f7753a1 = 빼기(1), object_verwijzen = 빼기(2); if (!object_WAARDE(object_verwijzen, 16)) return;
                if (invoer_AANTAL_8f7753a1 < 0 || invoer_AANTAL_8f7753a1 > heap_WAARDE[heap_WAARDE[object_verwijzen + 2] + 1]) 예외던짐(9, "invalid datagram length"); else heap_WAARDE[object_verwijzen + 3] = invoer_AANTAL_8f7753a1; return;
            }
            if (opdracht_CODE == 182 && (Word_sms(naam_constante, "getData") && Word_sms(서술상수, "()[B") || Word_sms(naam_constante, "getLength") && Word_sms(서술상수, "()I") || Word_sms(naam_constante, "getAddress") && Word_sms(서술상수, "()Ljava/net/InetAddress;") || Word_sms(naam_constante, "getPort") && Word_sms(서술상수, "()I"))) {
                int object_verwijzen = 빼기(2); if (!object_WAARDE(object_verwijzen, 16)) return;
                int invoer_functie_206f1c6d = Word_sms(naam_constante, "getData") ? 2 : Word_sms(naam_constante, "getLength") ? 3 : Word_sms(naam_constante, "getAddress") ? 4 : 5;
                넣기(heap_WAARDE[object_verwijzen + invoer_functie_206f1c6d], invoer_functie_206f1c6d == 2 || invoer_functie_206f1c6d == 4 ? 2 : 1); return;
            }
        }
        if (Word_sms(eigenaar, "java/net/DatagramSocket")) {
            if (opdracht_CODE == 183 && Word_sms(naam_constante, "<init>") && (Word_sms(서술상수, "()V") || Word_sms(서술상수, "(I)V"))) {
                int poortnummer = Word_sms(서술상수, "()V") ? 0 : 빼기(1), object_verwijzen = 빼기(2); if (!object_WAARDE(object_verwijzen, 15)) return;
                if (poortnummer < 0 || poortnummer > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = gebruikersruimte.open_net(poortnummer); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else heap_WAARDE[object_verwijzen + 2] = 열린파일번호; return;
            }
            if (opdracht_CODE == 182 && Word_sms(naam_constante, "setSoTimeout") && Word_sms(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), object_verwijzen = 빼기(2); if (!object_WAARDE(object_verwijzen, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else heap_WAARDE[object_verwijzen + 3] = 밀리초값; return;
            }
            if (opdracht_CODE == 182 && Word_sms(naam_constante, "getLocalPort") && Word_sms(서술상수, "()I")) { int object_verwijzen = 빼기(2); if (object_WAARDE(object_verwijzen, 15)) 넣기(heap_WAARDE[object_verwijzen + 2] < 0 ? -1 : gebruikersruimte.net_poort(heap_WAARDE[object_verwijzen + 2]), 1); return; }
            if (opdracht_CODE == 182 && Word_sms(naam_constante, "isClosed") && Word_sms(서술상수, "()Z")) { int object_verwijzen = 빼기(2); if (object_WAARDE(object_verwijzen, 15)) 넣기(heap_WAARDE[object_verwijzen + 2] < 0 ? 1 : 0, 1); return; }
            if (opdracht_CODE == 182 && Word_sms(naam_constante, "close") && Word_sms(서술상수, "()V")) { int object_verwijzen = 빼기(2); if (object_WAARDE(object_verwijzen, 15) && heap_WAARDE[object_verwijzen + 2] >= 0) { gebruikersruimte.파일서술자닫기(heap_WAARDE[object_verwijzen + 2]); heap_WAARDE[object_verwijzen + 2] = -1; } return; }
            if (opdracht_CODE == 182 && (Word_sms(naam_constante, "send") || Word_sms(naam_constante, "receive")) && Word_sms(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int pakket = 빼기(2), object_verwijzen = 빼기(2); if (!object_WAARDE(pakket, 16) || !object_WAARDE(object_verwijzen, 15)) return;
                int gegevens_MATRIX = heap_WAARDE[pakket + 2], geldig_tijdsduur = heap_WAARDE[pakket + 3], 열린파일번호 = heap_WAARDE[object_verwijzen + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Word_sms(naam_constante, "send")) {
                    if (!object_WAARDE(heap_WAARDE[pakket + 4], 14)) return;
                    if (geldig_tijdsduur > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int lus_INDEX = 0; lus_INDEX < geldig_tijdsduur; lus_INDEX++) 통신임시[lus_INDEX] = heap_WAARDE[gegevens_MATRIX + 2 + lus_INDEX];
                    if (gebruikersruimte.e_mailen_net(열린파일번호, heap_WAARDE[heap_WAARDE[pakket + 4] + 2], heap_WAARDE[pakket + 5], 통신임시, geldig_tijdsduur) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int invoer_AANTAL_8f7753a1 = gebruikersruimte.ontvangen_net(열린파일번호, 통신임시, geldig_tijdsduur > 512 ? 512 : geldig_tijdsduur);
                    if (invoer_AANTAL_8f7753a1 == -11) {
                        int huidige_tijd = gebruikersruimte.밀리초();
                        if (heap_WAARDE[object_verwijzen + 4] == 0) heap_WAARDE[object_verwijzen + 4] = huidige_tijd + 1;
                        if (heap_WAARDE[object_verwijzen + 3] > 0 && huidige_tijd - (heap_WAARDE[object_verwijzen + 4] - 1) >= heap_WAARDE[object_verwijzen + 3]) { heap_WAARDE[object_verwijzen + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(object_verwijzen, 2); 넣기(pakket, 2); frame_functie[frame_INDEX] = frame_instructie[frame_INDEX]; wijzigingsaanvraag = true; return;
                    }
                    heap_WAARDE[object_verwijzen + 4] = 0;
                    if (invoer_AANTAL_8f7753a1 < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int lus_INDEX = 0; lus_INDEX < invoer_AANTAL_8f7753a1; lus_INDEX++) heap_WAARDE[gegevens_MATRIX + 2 + lus_INDEX] = (byte)통신임시[lus_INDEX];
                    heap_WAARDE[pakket + 3] = invoer_AANTAL_8f7753a1; heap_WAARDE[pakket + 4] = ADRES_object(통신임시[513]); heap_verwijzen[pakket + 4] = 1; heap_WAARDE[pakket + 5] = 통신임시[512];
                }
                return;
            }
        }
        fout_WAARDE("unsupported java.net method");
    }
    static boolean 흐름대기(int object_verwijzen) {
        int huidige_tijd = gebruikersruimte.밀리초();
        if (heap_WAARDE[object_verwijzen + 5] == 0) heap_WAARDE[object_verwijzen + 5] = huidige_tijd + 1;
        if (heap_WAARDE[object_verwijzen + 3] > 0 && huidige_tijd - (heap_WAARDE[object_verwijzen + 5] - 1) >= heap_WAARDE[object_verwijzen + 3]) { heap_WAARDE[object_verwijzen + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        frame_functie[frame_INDEX] = frame_instructie[frame_INDEX]; wijzigingsaanvraag = true; return true;
    }
    static void 흐름호출(int eigenaar, int naam_constante, int 서술상수, int opdracht_CODE) {
        boolean ontvangen_page = Word_sms(eigenaar, "java/net/ServerSocket"), Stream = Word_sms(eigenaar, "java/io/InputStream") || Word_sms(eigenaar, "java/io/OutputStream");
        if (!Stream && opdracht_CODE == 183 && Word_sms(naam_constante, "<init>")) {
            boolean informatie_leeg_Status = Word_sms(서술상수, "()V"), 이름지정여부 = Word_sms(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = Word_sms(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(informatie_leeg_Status || ontvangen_page && Word_sms(서술상수, "(I)V") || !ontvangen_page && (이름지정여부 || 주소지정여부))) { fout_WAARDE("unsupported socket constructor"); return; }
            int poortnummer = informatie_leeg_Status ? 0 : 빼기(1), ADRES_verwijzen = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, object_verwijzen = 빼기(2);
            if (!object_WAARDE(object_verwijzen, ontvangen_page ? 18 : 17)) return;
            if (poortnummer < 0 || poortnummer > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !object_WAARDE(ADRES_verwijzen, 14)) return;
            int netwerk_id = 이름지정여부 ? 주소해독(ADRES_verwijzen) : 주소지정여부 ? heap_WAARDE[ADRES_verwijzen + 2] : 0x7f000001;
            if (fout || 던진객체 != 0) return;
            int 열린파일번호 = gebruikersruimte.Stream_controle(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = informatie_leeg_Status ? 0 : ontvangen_page ? gebruikersruimte.Stream_controle(1, 열린파일번호, poortnummer) : gebruikersruimte.VERBINDEN_Stream(열린파일번호, netwerk_id, poortnummer);
            if (처리값 < 0) { gebruikersruimte.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            heap_WAARDE[object_verwijzen + 2] = 열린파일번호; heap_WAARDE[object_verwijzen + 4] = poortnummer; heap_WAARDE[object_verwijzen + 6] = informatie_leeg_Status ? 0 : 1; return;
        }
        if (!Stream && Word_sms(naam_constante, "setSoTimeout") && Word_sms(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), object_verwijzen = 빼기(2); if (!object_WAARDE(object_verwijzen, ontvangen_page ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else heap_WAARDE[object_verwijzen + 3] = 밀리초값; return; }
        if (!Stream && Word_sms(naam_constante, "close") && Word_sms(서술상수, "()V")) { int object_verwijzen = 빼기(2); if (object_WAARDE(object_verwijzen, ontvangen_page ? 18 : 17) && heap_WAARDE[object_verwijzen + 2] >= 0) { gebruikersruimte.파일서술자닫기(heap_WAARDE[object_verwijzen + 2]); heap_WAARDE[object_verwijzen + 2] = -1; } return; }
        if (!Stream && (Word_sms(naam_constante, "getLocalPort") || Word_sms(naam_constante, "getPort") || Word_sms(naam_constante, "isClosed") || Word_sms(naam_constante, "isConnected"))) {
            int object_verwijzen = 빼기(2); if (!object_WAARDE(object_verwijzen, ontvangen_page ? 18 : 17)) return;
            넣기(Word_sms(naam_constante, "isClosed") ? heap_WAARDE[object_verwijzen + 2] < 0 ? 1 : 0 : Word_sms(naam_constante, "isConnected") ? heap_WAARDE[object_verwijzen + 6] : Word_sms(naam_constante, "getPort") ? heap_WAARDE[object_verwijzen + 4] : heap_WAARDE[object_verwijzen + 2] < 0 ? -1 : gebruikersruimte.Stream_controle(4, heap_WAARDE[object_verwijzen + 2], 0), 1); return;
        }
        if (ontvangen_page && Word_sms(naam_constante, "accept") && Word_sms(서술상수, "()Ljava/net/Socket;")) {
            int object_verwijzen = 빼기(2); if (!object_WAARDE(object_verwijzen, 18)) return; int 열린파일번호 = gebruikersruimte.Stream_controle(3, heap_WAARDE[object_verwijzen + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(object_verwijzen)) 넣기(object_verwijzen, 2); return; }
            heap_WAARDE[object_verwijzen + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = toewijzen_Opslag(17, 5); if (fout) { gebruikersruimte.파일서술자닫기(열린파일번호); return; } heap_WAARDE[반환값 + 2] = 열린파일번호; heap_WAARDE[반환값 + 4] = gebruikersruimte.Stream_controle(5, 열린파일번호, 0); heap_WAARDE[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!ontvangen_page && !Stream && ((Word_sms(naam_constante, "getInputStream") && Word_sms(서술상수, "()Ljava/io/InputStream;")) || (Word_sms(naam_constante, "getOutputStream") && Word_sms(서술상수, "()Ljava/io/OutputStream;")))) {
            int object_verwijzen = 빼기(2); if (!object_WAARDE(object_verwijzen, 17)) return; if (heap_WAARDE[object_verwijzen + 2] < 0 || heap_WAARDE[object_verwijzen + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = toewijzen_Opslag(19, 4); if (fout) return; heap_WAARDE[반환값 + 2] = object_verwijzen; heap_verwijzen[반환값 + 2] = 1; heap_WAARDE[반환값 + 3] = Word_sms(naam_constante, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (Stream) {
            boolean 읽기여부 = Word_sms(naam_constante, "read"), informatie_schrijven_operatie = Word_sms(naam_constante, "write"), blok = Word_sms(서술상수, "([B)I") || Word_sms(서술상수, "([B)V"), informatie_SUBMATRIX = Word_sms(서술상수, "([BII)I") || Word_sms(서술상수, "([BII)V");
            int invoer_AANTAL_8f7753a1 = informatie_SUBMATRIX ? 빼기(1) : 0, 시작변위 = informatie_SUBMATRIX ? 빼기(1) : 0, gegevens_MATRIX = blok || informatie_SUBMATRIX ? 빼기(2) : 0;
            int gegevens_WAARDE = informatie_schrijven_operatie && Word_sms(서술상수, "(I)V") ? 빼기(1) : 0, object_verwijzen = 빼기(2);
            if (!object_WAARDE(object_verwijzen, 19)) return; int bovenliggend_verwijzen = heap_WAARDE[object_verwijzen + 2], 열린파일번호 = heap_WAARDE[bovenliggend_verwijzen + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Word_sms(naam_constante, "close") && Word_sms(서술상수, "()V")) { gebruikersruimte.파일서술자닫기(열린파일번호); heap_WAARDE[bovenliggend_verwijzen + 2] = -1; return; }
            if (Word_sms(naam_constante, "flush") && Word_sms(서술상수, "()V")) return;
            if ((!읽기여부 && !informatie_schrijven_operatie) || 읽기여부 != (heap_WAARDE[object_verwijzen + 3] == 0)) { fout_WAARDE("unsupported stream operation"); return; }
            if (blok || informatie_SUBMATRIX) { if (!object_WAARDE(gegevens_MATRIX, 20)) return; if (blok) invoer_AANTAL_8f7753a1 = heap_WAARDE[gegevens_MATRIX + 1]; if (시작변위 < 0 || invoer_AANTAL_8f7753a1 < 0 || 시작변위 > heap_WAARDE[gegevens_MATRIX + 1] - invoer_AANTAL_8f7753a1) { 예외던짐(6, "stream array bounds"); return; } }
            else invoer_AANTAL_8f7753a1 = 1;
            if (invoer_AANTAL_8f7753a1 == 0) { if (읽기여부) 넣기(0, 1); return; }
            int Voltooid_AANTAL = informatie_schrijven_operatie ? heap_WAARDE[object_verwijzen + 4] : 0, 처리값 = 0;
            while (Voltooid_AANTAL < invoer_AANTAL_8f7753a1) {
                처리값 = 읽기여부 ? gebruikersruimte.파일한바이트읽기(열린파일번호) : gebruikersruimte.파일한바이트쓰기(열린파일번호, blok || informatie_SUBMATRIX ? heap_WAARDE[gegevens_MATRIX + 2 + 시작변위 + Voltooid_AANTAL] : gegevens_WAARDE);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (blok || informatie_SUBMATRIX)) heap_WAARDE[gegevens_MATRIX + 2 + 시작변위 + Voltooid_AANTAL] = (byte)처리값;
                Voltooid_AANTAL++; if (읽기여부 && !(blok || informatie_SUBMATRIX)) break;
            }
            if (처리값 == -11 && (informatie_schrijven_operatie || Voltooid_AANTAL == 0)) {
                heap_WAARDE[object_verwijzen + 4] = Voltooid_AANTAL;
                if (흐름대기(bovenliggend_verwijzen)) { 넣기(object_verwijzen, 2); if (blok || informatie_SUBMATRIX) 넣기(gegevens_MATRIX, 2); if (informatie_SUBMATRIX) { 넣기(시작변위, 1); 넣기(invoer_AANTAL_8f7753a1, 1); } if (informatie_schrijven_operatie && !(blok || informatie_SUBMATRIX)) 넣기(gegevens_WAARDE, 1); } return;
            }
            heap_WAARDE[object_verwijzen + 4] = 0; heap_WAARDE[bovenliggend_verwijzen + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(Voltooid_AANTAL == 0 && 처리값 == 256 ? -1 : blok || informatie_SUBMATRIX ? Voltooid_AANTAL : 처리값, 1); return;
        }
        fout_WAARDE("unsupported Socket/ServerSocket method");
    }
    static int[] scherm_verwijzen = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int naam_constante) {
        if (Word_sms(naam_constante, "Nederlands/Eigen/Venster")) return 24;
        if (Word_sms(naam_constante, "Nederlands/Eigen/Etiket")) return 26;
        if (Word_sms(naam_constante, "Nederlands/Eigen/knop")) return 27;
        if (Word_sms(naam_constante, "Nederlands/Eigen/tekstveld")) return 28;
        if (Word_sms(naam_constante, "Nederlands/Eigen/Actie_kennisgeving")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int naam_constante) {
        return 한국어화면종(naam_constante) != 0 || Word_sms(naam_constante, "Nederlands/Eigen/scherm_element") || Word_sms(naam_constante, "Nederlands/Eigen/gebeurtenis_wachtrij");
    }
    static int scherm_les(int naam_constante) {
        int 한국어종 = 한국어화면종(naam_constante); if (한국어종 != 0) return 한국어종;
        if (Word_sms(naam_constante, "javax/swing/JFrame")) return 24;
        if (Word_sms(naam_constante, "javax/swing/JPanel")) return 25;
        if (Word_sms(naam_constante, "javax/swing/JLabel")) return 26;
        if (Word_sms(naam_constante, "javax/swing/JButton")) return 27;
        if (Word_sms(naam_constante, "javax/swing/JTextField")) return 28;
        if (Word_sms(naam_constante, "java/awt/event/ActionEvent")) return 29;
        if (Word_sms(naam_constante, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean scherm_eigenaar(int naam_constante) {
        return scherm_les(naam_constante) != 0 || Word_sms(naam_constante, "java/awt/Component") || Word_sms(naam_constante, "java/awt/Container") || Word_sms(naam_constante, "javax/swing/JComponent") || Word_sms(naam_constante, "javax/swing/AbstractButton") || Word_sms(naam_constante, "javax/swing/text/JTextComponent") || Word_sms(naam_constante, "javax/swing/SwingUtilities");
    }
    static boolean scherm_object(int object_verwijzen) { if (!informatie_geldig_object(object_verwijzen)) return false; if (heap_WAARDE[object_verwijzen] < 24 || heap_WAARDE[object_verwijzen] > 28) { fout_WAARDE("unsupported Swing receiver"); return false; } return true; }
    static void set_scherm_teken(int object_verwijzen, int sms_verwijzen) {
        if (sms_verwijzen != 0 && !object_WAARDE(sms_verwijzen, 1)) return;
        int invoer_AANTAL_8f7753a1 = sms_verwijzen == 0 ? 0 : heap_WAARDE[sms_verwijzen + 1]; if (invoer_AANTAL_8f7753a1 > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int lus_INDEX = 0; lus_INDEX < invoer_AANTAL_8f7753a1; lus_INDEX++) 화면글임시[lus_INDEX] = heap_WAARDE[sms_verwijzen + 2 + lus_INDEX];
        if (gebruikersruimte.scherm_sms(heap_WAARDE[object_verwijzen + 2], 화면글임시, invoer_AANTAL_8f7753a1) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        heap_WAARDE[object_verwijzen + 3] = sms_verwijzen; heap_verwijzen[object_verwijzen + 3] = 1;
    }
    static int 화면문자읽기(int object_verwijzen) {
        int account_WAARDE = heap_WAARDE[object_verwijzen + 2], invoer_AANTAL_8f7753a1 = gebruikersruimte.scherm_verbinding(8, account_WAARDE, 0, 0, 0, 0), 사용수 = 0;
        if (invoer_AANTAL_8f7753a1 < 0) { fout_WAARDE("GUI text read failed"); return 0; }
        for (int lus_INDEX = 0; lus_INDEX < invoer_AANTAL_8f7753a1; lus_INDEX++) { int 부호값 = gebruikersruimte.scherm_verbinding(9, account_WAARDE, lus_INDEX, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = toewijzen_Opslag(1, 사용수); if (!fout) for (int lus_INDEX = 0; lus_INDEX < 사용수; lus_INDEX++) heap_WAARDE[반환값 + 2 + lus_INDEX] = 화면글임시[lus_INDEX]; return 반환값;
    }
    /* Nederlands 객체를 직접 만들고 kernel_WAARDE scherm 기능에 연결한다. Swing object_WAARDE/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int eigenaar, int naam_constante, int 서술상수, int opdracht_CODE) {
        if (Word_sms(eigenaar, "Nederlands/Eigen/gebeurtenis_wachtrij")) {
            if (opdracht_CODE == 184 && Word_sms(naam_constante, "나중에실행") && Word_sms(서술상수, "(LNederlands/Eigen/실행할일;)V")) {
                int taak_Actie = 빼기(2); if (!informatie_geldig_object(taak_Actie)) return;
                if (나중수 == 8) { fout_WAARDE("scherm 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = taak_Actie; return;
            }
            if (opdracht_CODE == 184 && Word_sms(naam_constante, "사건처리중인가") && Word_sms(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            fout_WAARDE("지원하지 않는 Nederlands scherm 일정 호출"); return;
        }
        if (Word_sms(eigenaar, "Nederlands/Eigen/Actie_kennisgeving")) {
            int kennisgeving = 빼기(2); if (!object_WAARDE(kennisgeving, 29) || heap_WAARDE[kennisgeving + 3] == 0) return;
            if (Word_sms(naam_constante, "gebeurtenisbron") && Word_sms(서술상수, "()LNederlands/Eigen/scherm_element;")) 넣기(heap_WAARDE[kennisgeving + 2], 2);
            else if (Word_sms(naam_constante, "opdracht_sms") && Word_sms(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(heap_WAARDE[kennisgeving + 2]), 2);
            else if (Word_sms(naam_constante, "INDEX") && Word_sms(서술상수, "()I")) 넣기(1001, 1);
            else fout_WAARDE("지원하지 않는 Nederlands Actie kennisgeving 호출"); return;
        }
        if (opdracht_CODE == 183 && Word_sms(naam_constante, "<init>")) {
            int soort_WAARDE = 한국어화면종(eigenaar), 받이 = 0, 가로 = 0, Verticaal_functie = 0, 폭 = 0, hoogte_WAARDE = 0;
            if (soort_WAARDE == 24 && Word_sms(서술상수, "(Ljava/lang/String;II)V")) {
                hoogte_WAARDE = 빼기(1); 폭 = 빼기(1); 가로 = (gebruikersruimte.화면너비() - 폭) / 2; Verticaal_functie = (gebruikersruimte.scherm_hoogte() - hoogte_WAARDE) / 2;
            } else if ((soort_WAARDE == 26 || soort_WAARDE == 28) && Word_sms(서술상수, "(Ljava/lang/String;IIII)V") || soort_WAARDE == 27 && Word_sms(서술상수, "(Ljava/lang/String;IIIILNederlands/Eigen/동작받이;)V")) {
                if (soort_WAARDE == 27) 받이 = 빼기(2);
                hoogte_WAARDE = 빼기(1); 폭 = 빼기(1); Verticaal_functie = 빼기(1); 가로 = 빼기(1);
            } else { fout_WAARDE("지원하지 않는 Nederlands scherm 생성자"); return; }
            int tekst = 빼기(2), element_WAARDE = 빼기(2); if (!scherm_object(element_WAARDE)) return;
            if (폭 < 1 || hoogte_WAARDE < 1 || 가로 < 0 || Verticaal_functie < 0 || 폭 > gebruikersruimte.화면너비() - 가로 || hoogte_WAARDE > gebruikersruimte.scherm_hoogte() - Verticaal_functie) { 예외던짐(27, "scherm 영역을 벗어난 크기입니다"); return; }
            int INDEX = gebruikersruimte.scherm_verbinding(0, soort_WAARDE - 23, 0, 0, 0, 0);
            if (INDEX < 1 || INDEX > 32) { fout_WAARDE("scherm element_WAARDE 자리가 가득 찼습니다"); return; }
            heap_WAARDE[element_WAARDE + 2] = INDEX; scherm_verwijzen[INDEX - 1] = element_WAARDE;
            heap_WAARDE[element_WAARDE + 5] = 가로; heap_WAARDE[element_WAARDE + 6] = Verticaal_functie; heap_WAARDE[element_WAARDE + 7] = 폭; heap_WAARDE[element_WAARDE + 8] = hoogte_WAARDE; heap_WAARDE[element_WAARDE + 10] = 2;
            heap_WAARDE[element_WAARDE + 4] = 받이; heap_verwijzen[element_WAARDE + 4] = 1; heap_WAARDE[element_WAARDE + 12] = 1;
            gebruikersruimte.scherm_verbinding(1, INDEX, 가로, Verticaal_functie, 폭, hoogte_WAARDE);
            if (soort_WAARDE == 24) gebruikersruimte.scherm_verbinding(7, INDEX, 2, 0, 0, 0);
            set_scherm_teken(element_WAARDE, tekst); return;
        }
        if (opdracht_CODE != 182) { fout_WAARDE("잘못된 Nederlands scherm 호출 opdracht"); return; }
        if (Word_sms(naam_constante, "schrijven_sms") && Word_sms(서술상수, "(Ljava/lang/String;)V")) {
            int tekst = 빼기(2), element_WAARDE = 빼기(2); if (scherm_object(element_WAARDE)) set_scherm_teken(element_WAARDE, tekst); return;
        }
        if (Word_sms(naam_constante, "글읽기") && Word_sms(서술상수, "()Ljava/lang/String;")) {
            int element_WAARDE = 빼기(2); if (scherm_object(element_WAARDE)) 넣기(화면문자읽기(element_WAARDE), 2); return;
        }
        if (Word_sms(naam_constante, "동작맡기기") && Word_sms(서술상수, "(LNederlands/Eigen/동작받이;)V")) {
            int 받이 = 빼기(2), element_WAARDE = 빼기(2);
            if (scherm_object(element_WAARDE)) { heap_WAARDE[element_WAARDE + 4] = 받이; heap_verwijzen[element_WAARDE + 4] = 1; heap_WAARDE[element_WAARDE + 12] = 1; } return;
        }
        if (Word_sms(naam_constante, "Toevoegen_element") && Word_sms(서술상수, "(LNederlands/Eigen/scherm_element;)V")) {
            int kind_WAARDE = 빼기(2), bovenliggend_WAARDE = 빼기(2); if (!scherm_object(kind_WAARDE) || !scherm_object(bovenliggend_WAARDE)) return;
            if (gebruikersruimte.scherm_verbinding(2, heap_WAARDE[bovenliggend_WAARDE + 2], heap_WAARDE[kind_WAARDE + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 scherm 부모입니다"); return; }
            heap_WAARDE[kind_WAARDE + 11] = bovenliggend_WAARDE; heap_verwijzen[kind_WAARDE + 11] = 1; return;
        }
        if (Word_sms(naam_constante, "자리정하기") && Word_sms(서술상수, "(IIII)V")) {
            int hoogte_WAARDE = 빼기(1), 폭 = 빼기(1), Verticaal_functie = 빼기(1), 가로 = 빼기(1), element_WAARDE = 빼기(2); if (!scherm_object(element_WAARDE)) return;
            if (gebruikersruimte.scherm_verbinding(1, heap_WAARDE[element_WAARDE + 2], 가로, Verticaal_functie, 폭, hoogte_WAARDE) < 0) { 예외던짐(27, "scherm 영역을 벗어난 자리입니다"); return; }
            heap_WAARDE[element_WAARDE + 5] = 가로; heap_WAARDE[element_WAARDE + 6] = Verticaal_functie; heap_WAARDE[element_WAARDE + 7] = 폭; heap_WAARDE[element_WAARDE + 8] = hoogte_WAARDE; return;
        }
        if ((Word_sms(naam_constante, "weergeven_venster") || Word_sms(naam_constante, "Sluiten")) && Word_sms(서술상수, "()V")) {
            boolean Zichtbaarheid_WAARDE = Word_sms(naam_constante, "weergeven_venster"); int element_WAARDE = 빼기(2); if (!scherm_object(element_WAARDE)) return;
            if (gebruikersruimte.scherm_verbinding(Zichtbaarheid_WAARDE ? 3 : 4, heap_WAARDE[element_WAARDE + 2], Zichtbaarheid_WAARDE ? 1 : 0, 0, 0, 0) < 0) { fout_WAARDE("화면은 interactief 명령에서 실행해야 합니다"); return; }
            heap_WAARDE[element_WAARDE + 9] = Zichtbaarheid_WAARDE ? 1 : 0; return;
        }
        if (Word_sms(naam_constante, "보이는가") && Word_sms(서술상수, "()Z")) { int element_WAARDE = 빼기(2); if (scherm_object(element_WAARDE)) 넣기(heap_WAARDE[element_WAARDE + 9], 1); return; }
        fout_WAARDE("지원하지 않는 Nederlands scherm methode_WAARDE");
    }
    static void 화면호출(int eigenaar, int naam_constante, int 서술상수, int opdracht_CODE) {
        if (Word_sms(eigenaar, "javax/swing/SwingUtilities")) {
            if (opdracht_CODE == 184 && Word_sms(naam_constante, "invokeLater") && Word_sms(서술상수, "(Ljava/lang/Runnable;)V")) { int object_verwijzen = 빼기(2); if (!informatie_geldig_object(object_verwijzen)) return; if (나중수 == 8) { fout_WAARDE("invokeLater queue full"); return; } 나중실행[나중수++] = object_verwijzen; return; }
            if (opdracht_CODE == 184 && Word_sms(naam_constante, "isEventDispatchThread") && Word_sms(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            fout_WAARDE("unsupported SwingUtilities method"); return;
        }
        if (Word_sms(eigenaar, "java/awt/event/ActionEvent")) {
            int object_verwijzen = 빼기(2); if (!object_WAARDE(object_verwijzen, 29)) return;
            if (Word_sms(naam_constante, "getSource") && Word_sms(서술상수, "()Ljava/lang/Object;")) 넣기(heap_WAARDE[object_verwijzen + 2], 2);
            else if (Word_sms(naam_constante, "getActionCommand") && Word_sms(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(heap_WAARDE[object_verwijzen + 2]), 2);
            else if (Word_sms(naam_constante, "getID") && Word_sms(서술상수, "()I")) 넣기(1001, 1);
            else fout_WAARDE("unsupported ActionEvent method"); return;
        }
        if (opdracht_CODE == 183 && Word_sms(naam_constante, "<init>")) {
            int KOLOMMEN = 0, sms_verwijzen = 0;
            if (Word_sms(서술상수, "(I)V")) KOLOMMEN = 빼기(1);
            else if (Word_sms(서술상수, "(Ljava/lang/String;I)V")) { KOLOMMEN = 빼기(1); sms_verwijzen = 빼기(2); }
            else if (Word_sms(서술상수, "(Ljava/lang/String;)V")) sms_verwijzen = 빼기(2);
            else if (Word_sms(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Word_sms(서술상수, "()V")) { fout_WAARDE("unsupported Swing constructor"); return; }
            int object_verwijzen = 빼기(2); if (!informatie_geldig_object(object_verwijzen)) return;
            if (heap_WAARDE[object_verwijzen] == 30) { fout_WAARDE("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!scherm_object(object_verwijzen) || KOLOMMEN < 0) return;
            int account_WAARDE = gebruikersruimte.scherm_verbinding(0, heap_WAARDE[object_verwijzen] - 23, 0, 0, 0, 0);
            if (account_WAARDE < 1 || account_WAARDE > 32) { fout_WAARDE("GUI widget slots exhausted"); return; }
            heap_WAARDE[object_verwijzen + 2] = account_WAARDE; scherm_verwijzen[account_WAARDE - 1] = object_verwijzen; heap_WAARDE[object_verwijzen + 5] = heap_WAARDE[object_verwijzen] == 24 ? 130 : 16; heap_WAARDE[object_verwijzen + 6] = heap_WAARDE[object_verwijzen] == 24 ? 110 : 16;
            heap_WAARDE[object_verwijzen + 7] = heap_WAARDE[object_verwijzen] == 24 ? 380 : 220; heap_WAARDE[object_verwijzen + 8] = heap_WAARDE[object_verwijzen] == 24 ? 240 : 28; heap_WAARDE[object_verwijzen + 10] = 1;
            set_scherm_teken(object_verwijzen, sms_verwijzen); return;
        }
        if (Word_sms(naam_constante, "setText") || Word_sms(naam_constante, "setTitle")) { int sms_verwijzen = 빼기(2), object_verwijzen = 빼기(2); if (scherm_object(object_verwijzen) && Word_sms(서술상수, "(Ljava/lang/String;)V")) set_scherm_teken(object_verwijzen, sms_verwijzen); return; }
        if (Word_sms(naam_constante, "getText") || Word_sms(naam_constante, "getTitle")) { int object_verwijzen = 빼기(2); if (scherm_object(object_verwijzen) && Word_sms(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(object_verwijzen), 2); return; }
        if (Word_sms(naam_constante, "addActionListener") && Word_sms(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int ontvangen_verwijzen = 빼기(2), object_verwijzen = 빼기(2); if (scherm_object(object_verwijzen)) { heap_WAARDE[object_verwijzen + 4] = ontvangen_verwijzen; heap_verwijzen[object_verwijzen + 4] = 1; } return; }
        if (Word_sms(naam_constante, "getContentPane") && Word_sms(서술상수, "()Ljava/awt/Container;")) { int object_verwijzen = 빼기(2); if (scherm_object(object_verwijzen)) 넣기(object_verwijzen, 2); return; }
        if (Word_sms(naam_constante, "setLayout") && Word_sms(서술상수, "(Ljava/awt/LayoutManager;)V")) { int Indeling_verwijzen = 빼기(2), object_verwijzen = 빼기(2); if (scherm_object(object_verwijzen) && Indeling_verwijzen != 0) fout_WAARDE("only absolute layout (null) is supported"); return; }
        if (Word_sms(naam_constante, "add") && (Word_sms(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || Word_sms(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean Indeling_toestand = Word_sms(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (Indeling_toestand) 빼기(2);
            int kind_verwijzen = 빼기(2), object_verwijzen = 빼기(2); if (!scherm_object(kind_verwijzen) || !scherm_object(object_verwijzen)) return;
            if (gebruikersruimte.scherm_verbinding(2, heap_WAARDE[object_verwijzen + 2], heap_WAARDE[kind_verwijzen + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            heap_WAARDE[kind_verwijzen + 11] = object_verwijzen; heap_verwijzen[kind_verwijzen + 11] = 1; if (!Indeling_toestand) 넣기(kind_verwijzen, 2); return;
        }
        if (Word_sms(naam_constante, "setBounds") && Word_sms(서술상수, "(IIII)V")) {
            int hoogte_WAARDE = 빼기(1), 너비 = 빼기(1), Y_coördinaat = 빼기(1), x_coördinaat = 빼기(1), object_verwijzen = 빼기(2); if (!scherm_object(object_verwijzen)) return;
            if (gebruikersruimte.scherm_verbinding(1, heap_WAARDE[object_verwijzen + 2], x_coördinaat, Y_coördinaat, 너비, hoogte_WAARDE) < 0) { 예외던짐(9, "GUI bounds"); return; }
            heap_WAARDE[object_verwijzen + 5] = x_coördinaat; heap_WAARDE[object_verwijzen + 6] = Y_coördinaat; heap_WAARDE[object_verwijzen + 7] = 너비; heap_WAARDE[object_verwijzen + 8] = hoogte_WAARDE; return;
        }
        if (Word_sms(naam_constante, "setSize") && Word_sms(서술상수, "(II)V")) {
            int hoogte_WAARDE = 빼기(1), 너비 = 빼기(1), object_verwijzen = 빼기(2); if (!scherm_object(object_verwijzen)) return;
            if (gebruikersruimte.scherm_verbinding(1, heap_WAARDE[object_verwijzen + 2], heap_WAARDE[object_verwijzen + 5], heap_WAARDE[object_verwijzen + 6], 너비, hoogte_WAARDE) < 0) 예외던짐(9, "GUI size"); else { heap_WAARDE[object_verwijzen + 7] = 너비; heap_WAARDE[object_verwijzen + 8] = hoogte_WAARDE; } return;
        }
        if (Word_sms(naam_constante, "setLocationRelativeTo") && Word_sms(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), object_verwijzen = 빼기(2); if (!scherm_object(object_verwijzen)) return; if (상대배치 != 0) { fout_WAARDE("only screen centering supported"); return; } heap_WAARDE[object_verwijzen + 5] = (gebruikersruimte.화면너비() - heap_WAARDE[object_verwijzen + 7]) / 2; heap_WAARDE[object_verwijzen + 6] = (gebruikersruimte.scherm_hoogte() - heap_WAARDE[object_verwijzen + 8]) / 2; gebruikersruimte.scherm_verbinding(1, heap_WAARDE[object_verwijzen + 2], heap_WAARDE[object_verwijzen + 5], heap_WAARDE[object_verwijzen + 6], heap_WAARDE[object_verwijzen + 7], heap_WAARDE[object_verwijzen + 8]); return; }
        if (Word_sms(naam_constante, "setDefaultCloseOperation") && Word_sms(서술상수, "(I)V")) { int Policy = 빼기(1), object_verwijzen = 빼기(2); if (scherm_object(object_verwijzen)) { if (Policy < 0 || Policy > 3) 예외던짐(9, "close policy"); else { heap_WAARDE[object_verwijzen + 10] = Policy; gebruikersruimte.scherm_verbinding(7, heap_WAARDE[object_verwijzen + 2], Policy, 0, 0, 0); } } return; }
        if (Word_sms(naam_constante, "setVisible") && Word_sms(서술상수, "(Z)V")) { int gegevens_WAARDE = 빼기(1), object_verwijzen = 빼기(2); if (scherm_object(object_verwijzen)) { int 처리값 = gebruikersruimte.scherm_verbinding(3, heap_WAARDE[object_verwijzen + 2], gegevens_WAARDE, 0, 0, 0); if (처리값 < 0) fout_WAARDE("Swing requires a standalone interactive command"); else heap_WAARDE[object_verwijzen + 9] = gegevens_WAARDE; } return; }
        if (Word_sms(naam_constante, "dispose") && Word_sms(서술상수, "()V")) { int object_verwijzen = 빼기(2); if (scherm_object(object_verwijzen)) { gebruikersruimte.scherm_verbinding(4, heap_WAARDE[object_verwijzen + 2], 0, 0, 0, 0); heap_WAARDE[object_verwijzen + 9] = 0; } return; }
        if (Word_sms(naam_constante, "repaint") || Word_sms(naam_constante, "validate")) { int object_verwijzen = 빼기(2); if (!scherm_object(object_verwijzen) || !Word_sms(서술상수, "()V")) return; gebruikersruimte.scherm_verbinding(1, heap_WAARDE[object_verwijzen + 2], heap_WAARDE[object_verwijzen + 5], heap_WAARDE[object_verwijzen + 6], heap_WAARDE[object_verwijzen + 7], heap_WAARDE[object_verwijzen + 8]); return; }
        if (Word_sms(naam_constante, "isVisible") && Word_sms(서술상수, "()Z")) { int object_verwijzen = 빼기(2); if (scherm_object(object_verwijzen)) 넣기(heap_WAARDE[object_verwijzen + 9], 1); return; }
        fout_WAARDE("unsupported Swing method (native subset)");
    }
    static void verzenden_gebeurtenis(int doel_ADRES, int gebeurtenis_nummer, boolean Nederlands) {
        if (doel_ADRES < 1 || heap_WAARDE[doel_ADRES] < 32) { fout_WAARDE("Java event listener required"); return; }
        int Bestand_INDEX = naam_methode(heap_WAARDE[doel_ADRES] - 32, gebeurtenis_nummer == 0 ? (Nederlands ? "Uitvoeren" : "run") : (Nederlands ? "ontvangen_Actie" : "actionPerformed"), gebeurtenis_nummer == 0 ? "()V" : (Nederlands ? "(LNederlands/Eigen/Actie_kennisgeving;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (Bestand_INDEX < 0) { fout_WAARDE("event callback missing"); return; }
        actueel_thread = 0; aantal_threads = 1; frame_INDEX = 0; thread_Status[0] = 1; frame_stack[0] = 0; frame_vergrendelen[0] = initialiseren_frame[0] = 0; wijzigingsaanvraag = false;
        for (int lus_INDEX = 0; lus_INDEX < 128; lus_INDEX++) { lokaal_WAARDE[lus_INDEX] = lokaal_TYPE[lus_INDEX] = 0; }
        frame_methode[0] = Bestand_INDEX; frame_functie[0] = methode_START[Bestand_INDEX]; lokaal_WAARDE[0] = doel_ADRES; lokaal_TYPE[0] = 2;
        if (gebeurtenis_nummer != 0) { lokaal_WAARDE[1] = gebeurtenis_nummer; lokaal_TYPE[1] = 2; }
        사건중 = true; Uitvoeren_opdracht(); 사건중 = false;
    }
    static void scherm_Evenementen() {
        while (!fout) {
            if (나중수 > 0) { int doel_ADRES = 나중실행[0], Nederlands = 나중한국어[0]; for (int lus_INDEX = 1; lus_INDEX < 나중수; lus_INDEX++) { 나중실행[lus_INDEX - 1] = 나중실행[lus_INDEX]; 나중한국어[lus_INDEX - 1] = 나중한국어[lus_INDEX]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; verzenden_gebeurtenis(doel_ADRES, 0, Nederlands != 0); continue; }
            if (gebruikersruimte.scherm_verbinding(6, 0, 0, 0, 0, 0) == 0) return;
            int gebeurtenis_nummer = gebruikersruimte.scherm_verbinding(5, 0, 0, 0, 0, 0); if (gebeurtenis_nummer == 0) continue;
            if (gebeurtenis_nummer < 0) { fout_WAARDE("GUI event I/O failed"); return; }
            int account_WAARDE = gebeurtenis_nummer & 65535; if (account_WAARDE < 1 || account_WAARDE > 32) continue; int object_verwijzen = scherm_verwijzen[account_WAARDE - 1]; if (object_verwijzen == 0) continue;
            if ((gebeurtenis_nummer & 65536) != 0) {
                if (heap_WAARDE[object_verwijzen + 10] != 0) heap_WAARDE[object_verwijzen + 9] = 0;
                if (heap_WAARDE[object_verwijzen + 10] == 3) for (int lus_INDEX = 0; lus_INDEX < 32; lus_INDEX++) if (scherm_verwijzen[lus_INDEX] != 0 && heap_WAARDE[scherm_verwijzen[lus_INDEX]] == 24) gebruikersruimte.scherm_verbinding(4, lus_INDEX + 1, 0, 0, 0, 0);
            } else if (heap_WAARDE[object_verwijzen + 4] != 0) {
                int LEESMIJ_verwijzen = toewijzen_Opslag(29, 2); if (fout) return; heap_WAARDE[LEESMIJ_verwijzen + 2] = object_verwijzen; heap_WAARDE[LEESMIJ_verwijzen + 3] = heap_WAARDE[object_verwijzen + 12]; heap_verwijzen[LEESMIJ_verwijzen + 2] = 1; verzenden_gebeurtenis(heap_WAARDE[object_verwijzen + 4], LEESMIJ_verwijzen, heap_WAARDE[object_verwijzen + 12] != 0);
            }
        }
    }
    public static int starten() {
        if (gebruikersruimte.인수개수() == 1 && 자바도구.같음(gebruikersruimte.argumenten(0), "-version")) {
            gebruikersruimte.Schrijven("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (gebruikersruimte.인수개수() < 1) { gebruikersruimte.Schrijven("Usage: java CLASS [ARGS]\n"); return 2; }
        invoer_les_Definitie = load_les_Definitie(host_teken(gebruikersruimte.argumenten(0))); if (fout || invoer_les_Definitie < 0) return 1;
        int beginpunt_WAARDE = naam_methode(invoer_les_Definitie, "starten", "()V");
        boolean 한국어진입 = beginpunt_WAARDE >= 0 && (methode_toegang[beginpunt_WAARDE] & 9) == 9;
        if (!한국어진입) beginpunt_WAARDE = naam_methode(invoer_les_Definitie, "main", "([Ljava/lang/String;)V");
        if (beginpunt_WAARDE < 0 || (methode_toegang[beginpunt_WAARDE] & 9) != 9) fout_WAARDE("public static void starten() or main(String[] args) required");
        if (fout) return 1;
        int argumenten = toewijzen_Opslag(3, gebruikersruimte.인수개수() - 1); matrixelement[argumenten] = -1;
        for (int nummer = 1; nummer < gebruikersruimte.인수개수() && !fout; nummer++) heap_WAARDE[argumenten + 1 + nummer] = host_teken(gebruikersruimte.argumenten(nummer));
        frame_INDEX = 0; frame_methode[0] = beginpunt_WAARDE; frame_functie[0] = methode_START[beginpunt_WAARDE]; lokaal_WAARDE[0] = 한국어진입 ? 0 : argumenten; lokaal_TYPE[0] = 한국어진입 ? 0 : 2;
        thread_Status[0] = 1; thread_object[0] = toewijzen_Opslag(13, 2);
        Uitvoeren_opdracht(); if (!fout) scherm_Evenementen(); return fout ? 1 : 0;
    }
}
