// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. bestand/operand_stack/verwijzen/branch 경계를 Uitvoeren_opdracht 중 검사한다. */
public final class 자바가상기계 {
    static int[] bestand = new int[16384], bestandsnaam_sms = new int[64];
    static int[] constante_tag = new int[512], 상가 = new int[512], constante_SECONDE_WAARDE = new int[512], tekenreeks_verwijzen = new int[512];
    static int[] methode_naam_sms = new int[32], methode_TYPE = new int[32], methode_toegang = new int[32];
    static int[] methode_START = new int[32], methode_beëindigen = new int[32], methode_stack = new int[32], 함수지역 = new int[32];
    static int[] methode_argument_AANTAL = new int[32], methode_argument_TYPE = new int[512], methode_Retour = new int[32];
    static int[] grens_WAARDE = new int[16384];
    static int[] lokaal_WAARDE = new int[4096], lokaal_TYPE = new int[4096], operand_stack_WAARDE = new int[4096], operand_stack_TYPE = new int[4096];
    static int[] frame_methode = new int[32], frame_functie = new int[32], frame_stack = new int[32];
    static int[] heap_WAARDE = new int[8192];
    static int Grootte, 읽기위치, constante_AANTAL, methode_AANTAL, klassenaam, frame_INDEX = -1, heap_beëindigen_functie = 1, Retour_TYPE;
    static boolean fout;

    static void fout_WAARDE(String Word_sms) {
        if (!fout) { gebruikersruimte.Schrijven("JVM error: "); gebruikersruimte.Schrijven(Word_sms); gebruikersruimte.schrijven_teken_WAARDE(10); }
        fout = true;
    }
    static boolean clip(int starten, int tijdsduur_WAARDE) { return starten >= 0 && tijdsduur_WAARDE >= 0 && starten <= Grootte - tijdsduur_WAARDE; }
    static int byte_WAARDE() {
        if (!clip(읽기위치, 1)) { fout_WAARDE("truncated class file"); return 0; }
        return bestand[읽기위치++];
    }
    static int 짧은수() { return byte_WAARDE() << 8 | byte_WAARDE(); }
    static int geheel_getal() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int tijdsduur_WAARDE) { if (!clip(읽기위치, tijdsduur_WAARDE)) fout_WAARDE("invalid attribute size"); else 읽기위치 += tijdsduur_WAARDE; }
    static boolean cheque_constante(int nummer, int soort_WAARDE) {
        if (nummer <= 0 || nummer >= constante_AANTAL || constante_tag[nummer] != soort_WAARDE) { fout_WAARDE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean sms_bereik(int starten, int tijdsduur_WAARDE, String Word_sms) {
        if (!clip(starten, tijdsduur_WAARDE) || tijdsduur_WAARDE != Word_sms.length()) return false;
        for (int nummer = 0; nummer < tijdsduur_WAARDE; nummer++) if (bestand[starten + nummer] != Word_sms.charAt(nummer)) return false;
        return true;
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
    static void overslaan_kenmerk() {
        int item_AANTAL = 짧은수();
        for (int nummer = 0; nummer < item_AANTAL && !fout; nummer++) { cheque_constante(짧은수(), 1); 건너(geheel_getal()); }
    }
    static int opdracht_tijdsduur(int WAARDE) {
        if (WAARDE == 16 || WAARDE == 18 || WAARDE == 21 || WAARDE == 25 || WAARDE == 54 || WAARDE == 58 || WAARDE == 188) return 2;
        if (WAARDE == 17 || WAARDE == 19 || WAARDE == 132 || WAARDE >= 153 && WAARDE <= 167
            || WAARDE >= 178 && WAARDE <= 184 || WAARDE == 187 || WAARDE == 189 || WAARDE == 192 || WAARDE == 198 || WAARDE == 199) return 3;
        if (WAARDE >= 0 && WAARDE <= 8 || WAARDE >= 26 && WAARDE <= 29 || WAARDE >= 42 && WAARDE <= 46 || WAARDE == 50
            || WAARDE >= 59 && WAARDE <= 62 || WAARDE >= 75 && WAARDE <= 79 || WAARDE == 83 || WAARDE == 87 || WAARDE == 89 || WAARDE == 95
            || WAARDE == 96 || WAARDE == 100 || WAARDE == 104 || WAARDE == 108 || WAARDE == 112 || WAARDE == 116
            || WAARDE == 120 || WAARDE == 122 || WAARDE == 124 || WAARDE == 126 || WAARDE == 128 || WAARDE == 130
            || WAARDE >= 145 && WAARDE <= 147 || WAARDE == 172 || WAARDE == 176 || WAARDE == 177 || WAARDE == 190) return 1;
        return 0;
    }
    static void 클래스읽기() {
        if (geheel_getal() != 0xcafebabe) fout_WAARDE("not a class file");
        int 부판 = 짧은수(), versie_WAARDE = 짧은수();
        if (versie_WAARDE < 45 || versie_WAARDE > 52 || 부판 != 0) fout_WAARDE("supported class versions: 45..52, minor 0");
        constante_AANTAL = 짧은수();
        if (constante_AANTAL < 1 || constante_AANTAL > 512) { fout_WAARDE("constant pool limit (511)"); return; }
        for (int nummer = 1; nummer < constante_AANTAL && !fout; nummer++) {
            int soort_WAARDE = byte_WAARDE(); constante_tag[nummer] = soort_WAARDE;
            if (soort_WAARDE == 1) { constante_SECONDE_WAARDE[nummer] = 짧은수(); 상가[nummer] = 읽기위치; 건너(constante_SECONDE_WAARDE[nummer]); }
            else if (soort_WAARDE == 3) 상가[nummer] = geheel_getal();
            else if (soort_WAARDE == 7 || soort_WAARDE == 8) 상가[nummer] = 짧은수();
            else if (soort_WAARDE == 9 || soort_WAARDE == 10 || soort_WAARDE == 12) { 상가[nummer] = 짧은수(); constante_SECONDE_WAARDE[nummer] = 짧은수(); }
            else fout_WAARDE("unsupported constant type");
        }
        int machtiging_WAARDE = 짧은수();
        if ((machtiging_WAARDE & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) fout_WAARDE("unsupported class flags");
        klassenaam = klassenaam_sms(짧은수());
        if (!Word_sms(klassenaam_sms(짧은수()), "java/lang/Object")) fout_WAARDE("inheritance unsupported");
        if (짧은수() != 0) fout_WAARDE("interfaces unsupported");
        if (짧은수() != 0) fout_WAARDE("fields unsupported");
        methode_AANTAL = 짧은수();
        if (methode_AANTAL < 1 || methode_AANTAL > 32) { fout_WAARDE("method count limit (32)"); return; }
        for (int nummer = 0; nummer < methode_AANTAL && !fout; nummer++) {
            methode_toegang[nummer] = 짧은수(); methode_naam_sms[nummer] = 짧은수(); methode_TYPE[nummer] = 짧은수();
            cheque_constante(methode_naam_sms[nummer], 1); 서술읽기(nummer);
            if ((methode_toegang[nummer] & (0x100 | 0x400 | 0x20)) != 0) fout_WAARDE("native, abstract and synchronized methods unsupported");
            if ((methode_toegang[nummer] & 8) == 0 && !Word_sms(methode_naam_sms[nummer], "<init>")) fout_WAARDE("instance methods unsupported");
            if (Word_sms(methode_naam_sms[nummer], "<clinit>")) fout_WAARDE("class initializers unsupported");
            for (int voorkant_WAARDE = 0; voorkant_WAARDE < nummer; voorkant_WAARDE++) if (vereffenen_Word(methode_naam_sms[voorkant_WAARDE], methode_naam_sms[nummer]) && vereffenen_Word(methode_TYPE[voorkant_WAARDE], methode_TYPE[nummer])) fout_WAARDE("duplicate method");
            int item_AANTAL = 짧은수();
            for (int kenmerkwaarde = 0; kenmerkwaarde < item_AANTAL && !fout; kenmerkwaarde++) {
                int Naam = 짧은수(), tijdsduur_WAARDE = geheel_getal(), starten = 읽기위치;
                if (!clip(starten, tijdsduur_WAARDE)) { fout_WAARDE("truncated method attribute"); break; }
                if (Word_sms(Naam, "Code")) {
                    if (methode_START[nummer] != 0) fout_WAARDE("duplicate Code attribute");
                    methode_stack[nummer] = 짧은수(); 함수지역[nummer] = 짧은수(); int CODE_tijdsduur = geheel_getal();
                    if (methode_stack[nummer] > 128 || 함수지역[nummer] > 128 || 함수지역[nummer] < methode_argument_AANTAL[nummer]
                        || CODE_tijdsduur < 1 || CODE_tijdsduur > 8192) fout_WAARDE("method memory limits exceeded");
                    methode_START[nummer] = 읽기위치; 건너(CODE_tijdsduur); methode_beëindigen[nummer] = 읽기위치;
                    if (짧은수() != 0) fout_WAARDE("exception handlers unsupported");
                    overslaan_kenmerk();
                    if (읽기위치 != starten + tijdsduur_WAARDE) fout_WAARDE("Code attribute size mismatch");
                } else 건너(tijdsduur_WAARDE);
            }
            if (methode_START[nummer] == 0) fout_WAARDE("missing Code attribute");
            int sleuf_invoer = methode_START[nummer];
            while (sleuf_invoer < methode_beëindigen[nummer] && !fout) {
                int tijdsduur_WAARDE = opdracht_tijdsduur(bestand[sleuf_invoer]);
                if (tijdsduur_WAARDE == 0 || tijdsduur_WAARDE > methode_beëindigen[nummer] - sleuf_invoer) { fout_WAARDE("unsupported or truncated bytecode"); break; }
                grens_WAARDE[sleuf_invoer] = nummer + 1; sleuf_invoer += tijdsduur_WAARDE;
            }
            // 실행하지 않는 경로에도 잘못된 branch 목적지를 허용하지 않는다.
            sleuf_invoer = methode_START[nummer];
            while (sleuf_invoer < methode_beëindigen[nummer] && !fout) {
                int WAARDE = bestand[sleuf_invoer];
                if (WAARDE >= 153 && WAARDE <= 167 || WAARDE == 198 || WAARDE == 199) {
                    int doel_WAARDE = sleuf_invoer + (short)(bestand[sleuf_invoer + 1] << 8 | bestand[sleuf_invoer + 2]);
                    if (doel_WAARDE < methode_START[nummer] || doel_WAARDE >= methode_beëindigen[nummer] || grens_WAARDE[doel_WAARDE] != nummer + 1) fout_WAARDE("invalid branch target");
                }
                sleuf_invoer += opdracht_tijdsduur(WAARDE);
            }
        }
        if (!fout) overslaan_kenmerk();
        if (읽기위치 != Grootte) fout_WAARDE("extra class file data");
    }
    static int toewijzen_Opslag(int soort_WAARDE, int tijdsduur_WAARDE) {
        if (tijdsduur_WAARDE < 0 || tijdsduur_WAARDE > heap_WAARDE.length - heap_beëindigen_functie - 2) { fout_WAARDE("object heap exhausted or negative array size"); return 0; }
        int verwijzen = heap_beëindigen_functie; heap_beëindigen_functie += tijdsduur_WAARDE + 2; heap_WAARDE[verwijzen] = soort_WAARDE; heap_WAARDE[verwijzen + 1] = tijdsduur_WAARDE;
        return verwijzen;
    }
    static boolean object_WAARDE(int verwijzen, int soort_WAARDE) {
        if (verwijzen < 1 || verwijzen >= heap_beëindigen_functie - 1 || heap_WAARDE[verwijzen] != soort_WAARDE) { fout_WAARDE("null or invalid object reference"); return false; }
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
        if (frame_INDEX == 31) { fout_WAARDE("call stack limit (32)"); return; }
        int Volgende_item = frame_INDEX + 1;
        for (int nummer = 0; nummer < 128; nummer++) lokaal_TYPE[Volgende_item * 128 + nummer] = 0;
        for (int nummer = methode_argument_AANTAL[FUNCTIE_WAARDE] - 1; nummer >= 0; nummer--) {
            lokaal_WAARDE[Volgende_item * 128 + nummer] = 빼기(methode_argument_TYPE[FUNCTIE_WAARDE * 16 + nummer]); lokaal_TYPE[Volgende_item * 128 + nummer] = methode_argument_TYPE[FUNCTIE_WAARDE * 16 + nummer];
        }
        frame_INDEX = Volgende_item; frame_methode[frame_INDEX] = FUNCTIE_WAARDE; frame_functie[frame_INDEX] = methode_START[FUNCTIE_WAARDE]; frame_stack[frame_INDEX] = 0;
    }
    static void Retour_HR(int TYPE_WAARDE) {
        if (TYPE_WAARDE != methode_Retour[frame_methode[frame_INDEX]]) { fout_WAARDE("return type mismatch"); return; }
        int WAARDE = TYPE_WAARDE == 0 ? 0 : 빼기(TYPE_WAARDE);
        frame_INDEX--; if (frame_INDEX >= 0 && TYPE_WAARDE != 0) 넣기(WAARDE, TYPE_WAARDE);
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
                if (WAARDE < 1 || WAARDE > 127) { fout_WAARDE("file stream paths currently require ASCII"); return; }
                Stream_bestandsnaam[sleuf_invoer] = WAARDE;
            }
            Stream_bestandsnaam[tijdsduur_WAARDE] = 0;
            int 서술자 = gebruikersruimte.파일서술자열기(Stream_bestandsnaam, tekstuitvoer ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { fout_WAARDE("FileNotFoundException: file open failed"); return; }
            heap_WAARDE[Stream_WAARDE + 2] = 서술자; heap_WAARDE[Stream_WAARDE + 3] = 1;
            return;
        }
        if (opdracht != 182) { fout_WAARDE("invalid file stream invocation"); return; }
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
            if (resultaat < -1) fout_WAARDE("IOException: read failed"); else 넣기(resultaat, 1);
        } else if (gebruikersruimte.파일한바이트쓰기(서술자, WAARDE) != 1) fout_WAARDE("IOException: write failed");
    }
    static void Bellen_methode(int INDEX, int opdracht) {
        if (!cheque_constante(INDEX, 10)) return;
        int eigenaar_WAARDE = klassenaam_sms(상가[INDEX]), Naam = verwijzen_naam(constante_SECONDE_WAARDE[INDEX]), opmaak_WAARDE = verwijzingstype(constante_SECONDE_WAARDE[INDEX]);
        if (fout) return;
        if (vereffenen_Word(eigenaar_WAARDE, klassenaam)) {
            if (opdracht != 184) { fout_WAARDE("only static user methods are supported"); return; }
            for (int nummer = 0; nummer < methode_AANTAL; nummer++) if (vereffenen_Word(Naam, methode_naam_sms[nummer]) && vereffenen_Word(opmaak_WAARDE, methode_TYPE[nummer])) {
                if ((methode_toegang[nummer] & 8) == 0) fout_WAARDE("method is not static"); else 호출(nummer);
                return;
            }
            fout_WAARDE("NoSuchMethodError"); return;
        }
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
        fout_WAARDE("unsupported library method");
    }
    static int MATRIX_sleuf(int verwijzen, int subscript_WAARDE, int TYPE_WAARDE) {
        if (!object_WAARDE(verwijzen, TYPE_WAARDE)) return 0;
        if (subscript_WAARDE < 0 || subscript_WAARDE >= heap_WAARDE[verwijzen + 1]) { fout_WAARDE("ArrayIndexOutOfBoundsException"); return 0; }
        return verwijzen + 2 + subscript_WAARDE;
    }
    static void Uitvoeren_opdracht() {
        int 남음 = 500000;
        while (frame_INDEX >= 0 && !fout) {
            if (--남음 == 0) { fout_WAARDE("instruction limit (500000)"); break; }
            int starten = frame_functie[frame_INDEX], WAARDE = 명바();
            if (fout) break;
            if (WAARDE == 0) continue;
            if (WAARDE == 1) { 넣기(0, 2); continue; }
            if (WAARDE >= 2 && WAARDE <= 8) { 넣기(WAARDE - 3, 1); continue; }
            if (WAARDE == 16) { 넣기((byte)명바(), 1); continue; }
            if (WAARDE == 17) { 넣기((short)명짧(), 1); continue; }
            if (WAARDE == 18 || WAARDE == 19) {
                int nummer = WAARDE == 18 ? 명바() : 명짧();
                if (nummer <= 0 || nummer >= constante_AANTAL) fout_WAARDE("invalid ldc constant");
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
            if (WAARDE == 46 || WAARDE == 50) {
                int subscript_WAARDE = 빼기(1), verwijzen = 빼기(2), sleuf_invoer = MATRIX_sleuf(verwijzen, subscript_WAARDE, WAARDE == 46 ? 2 : 3);
                if (!fout) 넣기(heap_WAARDE[sleuf_invoer], WAARDE == 46 ? 1 : 2); continue;
            }
            if (WAARDE == 79 || WAARDE == 83) {
                int item_element = 빼기(WAARDE == 79 ? 1 : 2), subscript_WAARDE = 빼기(1), verwijzen = 빼기(2), sleuf_invoer = MATRIX_sleuf(verwijzen, subscript_WAARDE, WAARDE == 79 ? 2 : 3);
                if (WAARDE == 83 && item_element != 0) object_WAARDE(item_element, 1);
                if (!fout) heap_WAARDE[sleuf_invoer] = item_element; continue;
            }
            if (WAARDE == 87) { 빼기(0); continue; }
            if (WAARDE == 89) { int 가 = 빼기(0), TYPE_WAARDE = Retour_TYPE; 넣기(가, TYPE_WAARDE); 넣기(가, TYPE_WAARDE); continue; }
            if (WAARDE == 95) { int 가 = 빼기(0), 가형 = Retour_TYPE, SECONDE_operand = 빼기(0), SECONDE_operand_TYPE = Retour_TYPE; 넣기(가, 가형); 넣기(SECONDE_operand, SECONDE_operand_TYPE); continue; }
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
            if (WAARDE == 178) {
                int nummer = 명짧(); if (!cheque_constante(nummer, 9)) continue;
                if (!Word_sms(klassenaam_sms(상가[nummer]), "java/lang/System") || !Word_sms(verwijzen_naam(constante_SECONDE_WAARDE[nummer]), "out")
                    || !Word_sms(verwijzingstype(constante_SECONDE_WAARDE[nummer]), "Ljava/io/PrintStream;")) fout_WAARDE("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (WAARDE == 182 || WAARDE == 183 || WAARDE == 184) { Bellen_methode(명짧(), WAARDE); continue; }
            if (WAARDE == 187) {
                int Naam = klassenaam_sms(명짧());
                if (Word_sms(Naam, "java/lang/StringBuilder")) 넣기(toewijzen_Opslag(4, 1), 2);
                else if (Word_sms(Naam, "java/io/FileInputStream") || Word_sms(Naam, "java/io/FileOutputStream")) {
                    int verwijzen = toewijzen_Opslag(Word_sms(Naam, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!fout) { heap_WAARDE[verwijzen + 2] = -1; 넣기(verwijzen, 2); }
                } else fout_WAARDE("unsupported object construction");
                continue;
            }
            if (WAARDE == 188 || WAARDE == 189) {
                if (WAARDE == 188) { if (명바() != 10) fout_WAARDE("only int[] newarray is supported"); }
                else if (!Word_sms(klassenaam_sms(명짧()), "java/lang/String")) fout_WAARDE("only String[] anewarray is supported");
                int tijdsduur_WAARDE = 빼기(1); 넣기(toewijzen_Opslag(WAARDE == 188 ? 2 : 3, tijdsduur_WAARDE), 2); continue;
            }
            if (WAARDE == 190) {
                int verwijzen = 빼기(2);
                if (verwijzen < 1 || verwijzen >= heap_beëindigen_functie - 1 || (heap_WAARDE[verwijzen] != 2 && heap_WAARDE[verwijzen] != 3)) fout_WAARDE("null or invalid array");
                else 넣기(heap_WAARDE[verwijzen + 1], 1); continue;
            }
            if (WAARDE == 192) {
                int Naam = klassenaam_sms(명짧()), verwijzen = 빼기(2);
                if (!Word_sms(Naam, "java/lang/String")) fout_WAARDE("unsupported checkcast");
                else if (verwijzen != 0) object_WAARDE(verwijzen, 1);
                넣기(verwijzen, 2); continue;
            }
            fout_WAARDE("unsupported bytecode");
        }
    }
    public static int starten() {
        if (gebruikersruimte.인수개수() == 1 && 자바도구.같음(gebruikersruimte.argumenten(0), "-version")) {
            gebruikersruimte.Schrijven("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (gebruikersruimte.인수개수() < 1) { gebruikersruimte.Schrijven("Usage: java CLASS [ARGS]\n"); return 2; }
        int tijdsduur_WAARDE = 자바도구.Naam(bestandsnaam_sms, gebruikersruimte.argumenten(0));
        if (tijdsduur_WAARDE < 1 || tijdsduur_WAARDE > 57) { gebruikersruimte.Schrijven("java: invalid class name\n"); return 2; }
        bestandsnaam_sms[tijdsduur_WAARDE] = '.'; bestandsnaam_sms[tijdsduur_WAARDE + 1] = 'c'; bestandsnaam_sms[tijdsduur_WAARDE + 2] = 'l'; bestandsnaam_sms[tijdsduur_WAARDE + 3] = 'a'; bestandsnaam_sms[tijdsduur_WAARDE + 4] = 's'; bestandsnaam_sms[tijdsduur_WAARDE + 5] = 's';
        Grootte = gebruikersruimte.파일읽기(bestandsnaam_sms, bestand);
        if (Grootte < 0) { gebruikersruimte.Schrijven("java: cannot read class: "); 자바도구.schrijven_nummer(Grootte); gebruikersruimte.schrijven_teken_WAARDE(10); return 1; }
        클래스읽기(); if (fout) return 1;
        int teken_naam = constante_sms(klassenaam);
        if (!fout && heap_WAARDE[teken_naam + 1] != tijdsduur_WAARDE) fout_WAARDE("class name does not match file");
        for (int nummer = 0; nummer < tijdsduur_WAARDE && !fout; nummer++) if (heap_WAARDE[teken_naam + 2 + nummer] != bestandsnaam_sms[nummer]) fout_WAARDE("class name does not match file");
        int beginpunt_WAARDE = -1;
        for (int nummer = 0; nummer < methode_AANTAL; nummer++) if (Word_sms(methode_naam_sms[nummer], "main") && Word_sms(methode_TYPE[nummer], "([Ljava/lang/String;)V") && (methode_toegang[nummer] & 9) == 9) beginpunt_WAARDE = nummer;
        if (beginpunt_WAARDE < 0) fout_WAARDE("public static void main(String[] args) required");
        if (fout) return 1;
        int argumenten = toewijzen_Opslag(3, gebruikersruimte.인수개수() - 1);
        for (int nummer = 1; nummer < gebruikersruimte.인수개수() && !fout; nummer++) heap_WAARDE[argumenten + 1 + nummer] = host_teken(gebruikersruimte.argumenten(nummer));
        frame_INDEX = 0; frame_methode[0] = beginpunt_WAARDE; frame_functie[0] = methode_START[beginpunt_WAARDE]; lokaal_WAARDE[0] = argumenten; lokaal_TYPE[0] = 2;
        Uitvoeren_opdracht(); return fout ? 1 : 0;
    }
}
