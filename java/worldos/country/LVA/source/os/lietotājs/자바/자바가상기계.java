// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. Fails/operands_kopa/Uzziņas/zars 경계를 Izpildīt_komanda 중 검사한다. */
public final class 자바가상기계 {
    static int[] Fails = new int[16384], faila_nosaukums_SMS = new int[64];
    static int[] konstante_tags = new int[512], 상가 = new int[512], konstante_SECOND_VALUE = new int[512], virkne_Uzziņas = new int[512];
    static int[] metode_nosaukums_SMS = new int[32], metode_TYPE = new int[32], metode_piekļūt = new int[32];
    static int[] metode_Sākt = new int[32], metode_beigt_zvanu = new int[32], metode_kopa = new int[32], 함수지역 = new int[32];
    static int[] metode_arg_COUNT = new int[32], metode_arg_TYPE = new int[512], metode_atdot = new int[32];
    static int[] 경계 = new int[16384];
    static int[] vietējs_VALUE = new int[4096], vietējs_TYPE = new int[4096], operands_kopa_VALUE = new int[4096], operands_kopa_TYPE = new int[4096];
    static int[] kadrs_metode = new int[32], kadrs_amats = new int[32], kadrs_kopa = new int[32];
    static int[] kaudze_VALUE = new int[8192];
    static int Izmērs, 읽기위치, konstante_COUNT, metode_COUNT, klases_nosaukums, kadrs_INDEX = -1, kaudze_beigt_zvanu_amats = 1, atdot_TYPE;
    static boolean Kļūda;

    static void kļūme_VALUE(String Word_SMS) {
        if (!Kļūda) { lietotājs.Rakstīt("JVM error: "); lietotājs.Rakstīt(Word_SMS); lietotājs.rakstīšana_rakstzīme_VALUE(10); }
        Kļūda = true;
    }
    static boolean klips(int Palaist, int 길이) { return Palaist >= 0 && 길이 >= 0 && Palaist <= Izmērs - 길이; }
    static int byte_VALUE() {
        if (!klips(읽기위치, 1)) { kļūme_VALUE("truncated class file"); return 0; }
        return Fails[읽기위치++];
    }
    static int 짧은수() { return byte_VALUE() << 8 | byte_VALUE(); }
    static int vesels_skaitlis() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int 길이) { if (!klips(읽기위치, 길이)) kļūme_VALUE("invalid attribute size"); else 읽기위치 += 길이; }
    static boolean čeks_konstante(int numurs, int 종류) {
        if (numurs <= 0 || numurs >= konstante_COUNT || konstante_tags[numurs] != 종류) { kļūme_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean SMS_diapazons(int Palaist, int 길이, String Word_SMS) {
        if (!klips(Palaist, 길이) || 길이 != Word_SMS.length()) return false;
        for (int numurs = 0; numurs < 길이; numurs++) if (Fails[Palaist + numurs] != Word_SMS.charAt(numurs)) return false;
        return true;
    }
    static boolean Word_SMS(int konstante_VALUE, String Word_SMS) { return čeks_konstante(konstante_VALUE, 1) && SMS_diapazons(상가[konstante_VALUE], konstante_SECOND_VALUE[konstante_VALUE], Word_SMS); }
    static boolean 같은말(int 가, int SECOND_operands) {
        if (!čeks_konstante(가, 1) || !čeks_konstante(SECOND_operands, 1) || konstante_SECOND_VALUE[가] != konstante_SECOND_VALUE[SECOND_operands]) return false;
        for (int numurs = 0; numurs < konstante_SECOND_VALUE[가]; numurs++) if (Fails[상가[가] + numurs] != Fails[상가[SECOND_operands] + numurs]) return false;
        return true;
    }
    static int klases_nosaukums_SMS(int numurs) { return čeks_konstante(numurs, 7) && čeks_konstante(상가[numurs], 1) ? 상가[numurs] : 0; }
    static int Uzziņas_nosaukums(int numurs) { return čeks_konstante(numurs, 12) && čeks_konstante(상가[numurs], 1) ? 상가[numurs] : 0; }
    static int Uzziņas_TYPE(int numurs) { return čeks_konstante(numurs, 12) && čeks_konstante(konstante_SECOND_VALUE[numurs], 1) ? konstante_SECOND_VALUE[numurs] : 0; }
    static int 서술형(int 끝, boolean 빈형) {
        if (읽기위치 >= 끝) { kļūme_VALUE("invalid descriptor"); return 0; }
        int VALUE = byte_VALUE();
        if (VALUE == 'V' && 빈형) return 0;
        if (VALUE == 'I' || VALUE == 'B' || VALUE == 'C' || VALUE == 'S' || VALUE == 'Z') return 1;
        if (VALUE == '[') { 서술형(끝, false); return 2; }
        if (VALUE == 'L') {
            int Palaist = 읽기위치;
            while (읽기위치 < 끝 && Fails[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == Palaist) kļūme_VALUE("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        kļūme_VALUE("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int FUNCTION_VALUE) {
        int 이전 = 읽기위치, numurs = metode_TYPE[FUNCTION_VALUE];
        if (!čeks_konstante(numurs, 1)) return;
        읽기위치 = 상가[numurs]; int 끝 = 읽기위치 + konstante_SECOND_VALUE[numurs];
        if (byte_VALUE() != '(') kļūme_VALUE("invalid method descriptor");
        int krājums_COUNT = 0;
        while (!Kļūda && 읽기위치 < 끝 && Fails[읽기위치] != ')') {
            if (krājums_COUNT == 16) { kļūme_VALUE("too many method arguments"); break; }
            metode_arg_TYPE[FUNCTION_VALUE * 16 + krājums_COUNT++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || byte_VALUE() != ')') kļūme_VALUE("invalid method descriptor");
        metode_atdot[FUNCTION_VALUE] = 서술형(끝, true); metode_arg_COUNT[FUNCTION_VALUE] = krājums_COUNT;
        if (읽기위치 != 끝) kļūme_VALUE("invalid method descriptor");
        읽기위치 = 이전;
    }
    static void 속성건너() {
        int krājums_COUNT = 짧은수();
        for (int numurs = 0; numurs < krājums_COUNT && !Kļūda; numurs++) { čeks_konstante(짧은수(), 1); 건너(vesels_skaitlis()); }
    }
    static int 명령길이(int VALUE) {
        if (VALUE == 16 || VALUE == 18 || VALUE == 21 || VALUE == 25 || VALUE == 54 || VALUE == 58 || VALUE == 188) return 2;
        if (VALUE == 17 || VALUE == 19 || VALUE == 132 || VALUE >= 153 && VALUE <= 167
            || VALUE >= 178 && VALUE <= 184 || VALUE == 187 || VALUE == 189 || VALUE == 192 || VALUE == 198 || VALUE == 199) return 3;
        if (VALUE >= 0 && VALUE <= 8 || VALUE >= 26 && VALUE <= 29 || VALUE >= 42 && VALUE <= 46 || VALUE == 50
            || VALUE >= 59 && VALUE <= 62 || VALUE >= 75 && VALUE <= 79 || VALUE == 83 || VALUE == 87 || VALUE == 89 || VALUE == 95
            || VALUE == 96 || VALUE == 100 || VALUE == 104 || VALUE == 108 || VALUE == 112 || VALUE == 116
            || VALUE == 120 || VALUE == 122 || VALUE == 124 || VALUE == 126 || VALUE == 128 || VALUE == 130
            || VALUE >= 145 && VALUE <= 147 || VALUE == 172 || VALUE == 176 || VALUE == 177 || VALUE == 190) return 1;
        return 0;
    }
    static void 클래스읽기() {
        if (vesels_skaitlis() != 0xcafebabe) kļūme_VALUE("not a class file");
        int 부판 = 짧은수(), versija_VALUE = 짧은수();
        if (versija_VALUE < 45 || versija_VALUE > 52 || 부판 != 0) kļūme_VALUE("supported class versions: 45..52, minor 0");
        konstante_COUNT = 짧은수();
        if (konstante_COUNT < 1 || konstante_COUNT > 512) { kļūme_VALUE("constant pool limit (511)"); return; }
        for (int numurs = 1; numurs < konstante_COUNT && !Kļūda; numurs++) {
            int 종류 = byte_VALUE(); konstante_tags[numurs] = 종류;
            if (종류 == 1) { konstante_SECOND_VALUE[numurs] = 짧은수(); 상가[numurs] = 읽기위치; 건너(konstante_SECOND_VALUE[numurs]); }
            else if (종류 == 3) 상가[numurs] = vesels_skaitlis();
            else if (종류 == 7 || 종류 == 8) 상가[numurs] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[numurs] = 짧은수(); konstante_SECOND_VALUE[numurs] = 짧은수(); }
            else kļūme_VALUE("unsupported constant type");
        }
        int atļauja_VALUE = 짧은수();
        if ((atļauja_VALUE & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) kļūme_VALUE("unsupported class flags");
        klases_nosaukums = klases_nosaukums_SMS(짧은수());
        if (!Word_SMS(klases_nosaukums_SMS(짧은수()), "java/lang/Object")) kļūme_VALUE("inheritance unsupported");
        if (짧은수() != 0) kļūme_VALUE("interfaces unsupported");
        if (짧은수() != 0) kļūme_VALUE("fields unsupported");
        metode_COUNT = 짧은수();
        if (metode_COUNT < 1 || metode_COUNT > 32) { kļūme_VALUE("method count limit (32)"); return; }
        for (int numurs = 0; numurs < metode_COUNT && !Kļūda; numurs++) {
            metode_piekļūt[numurs] = 짧은수(); metode_nosaukums_SMS[numurs] = 짧은수(); metode_TYPE[numurs] = 짧은수();
            čeks_konstante(metode_nosaukums_SMS[numurs], 1); 서술읽기(numurs);
            if ((metode_piekļūt[numurs] & (0x100 | 0x400 | 0x20)) != 0) kļūme_VALUE("native, abstract and synchronized methods unsupported");
            if ((metode_piekļūt[numurs] & 8) == 0 && !Word_SMS(metode_nosaukums_SMS[numurs], "<init>")) kļūme_VALUE("instance methods unsupported");
            if (Word_SMS(metode_nosaukums_SMS[numurs], "<clinit>")) kļūme_VALUE("class initializers unsupported");
            for (int priekšējā_VALUE = 0; priekšējā_VALUE < numurs; priekšējā_VALUE++) if (같은말(metode_nosaukums_SMS[priekšējā_VALUE], metode_nosaukums_SMS[numurs]) && 같은말(metode_TYPE[priekšējā_VALUE], metode_TYPE[numurs])) kļūme_VALUE("duplicate method");
            int krājums_COUNT = 짧은수();
            for (int atribūts_VALUE = 0; atribūts_VALUE < krājums_COUNT && !Kļūda; atribūts_VALUE++) {
                int Nosaukums = 짧은수(), 길이 = vesels_skaitlis(), Palaist = 읽기위치;
                if (!klips(Palaist, 길이)) { kļūme_VALUE("truncated method attribute"); break; }
                if (Word_SMS(Nosaukums, "Code")) {
                    if (metode_Sākt[numurs] != 0) kļūme_VALUE("duplicate Code attribute");
                    metode_kopa[numurs] = 짧은수(); 함수지역[numurs] = 짧은수(); int 코드길이 = vesels_skaitlis();
                    if (metode_kopa[numurs] > 128 || 함수지역[numurs] > 128 || 함수지역[numurs] < metode_arg_COUNT[numurs]
                        || 코드길이 < 1 || 코드길이 > 8192) kļūme_VALUE("method memory limits exceeded");
                    metode_Sākt[numurs] = 읽기위치; 건너(코드길이); metode_beigt_zvanu[numurs] = 읽기위치;
                    if (짧은수() != 0) kļūme_VALUE("exception handlers unsupported");
                    속성건너();
                    if (읽기위치 != Palaist + 길이) kļūme_VALUE("Code attribute size mismatch");
                } else 건너(길이);
            }
            if (metode_Sākt[numurs] == 0) kļūme_VALUE("missing Code attribute");
            int 칸 = metode_Sākt[numurs];
            while (칸 < metode_beigt_zvanu[numurs] && !Kļūda) {
                int 길이 = 명령길이(Fails[칸]);
                if (길이 == 0 || 길이 > metode_beigt_zvanu[numurs] - 칸) { kļūme_VALUE("unsupported or truncated bytecode"); break; }
                경계[칸] = numurs + 1; 칸 += 길이;
            }
            // 실행하지 않는 경로에도 잘못된 zars 목적지를 허용하지 않는다.
            칸 = metode_Sākt[numurs];
            while (칸 < metode_beigt_zvanu[numurs] && !Kļūda) {
                int VALUE = Fails[칸];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                    int mērķis_VALUE = 칸 + (short)(Fails[칸 + 1] << 8 | Fails[칸 + 2]);
                    if (mērķis_VALUE < metode_Sākt[numurs] || mērķis_VALUE >= metode_beigt_zvanu[numurs] || 경계[mērķis_VALUE] != numurs + 1) kļūme_VALUE("invalid branch target");
                }
                칸 += 명령길이(VALUE);
            }
        }
        if (!Kļūda) 속성건너();
        if (읽기위치 != Izmērs) kļūme_VALUE("extra class file data");
    }
    static int piešķirt_Krātuve(int 종류, int 길이) {
        if (길이 < 0 || 길이 > kaudze_VALUE.length - kaudze_beigt_zvanu_amats - 2) { kļūme_VALUE("object heap exhausted or negative array size"); return 0; }
        int Uzziņas = kaudze_beigt_zvanu_amats; kaudze_beigt_zvanu_amats += 길이 + 2; kaudze_VALUE[Uzziņas] = 종류; kaudze_VALUE[Uzziņas + 1] = 길이;
        return Uzziņas;
    }
    static boolean objekts_VALUE(int Uzziņas, int 종류) {
        if (Uzziņas < 1 || Uzziņas >= kaudze_beigt_zvanu_amats - 1 || kaudze_VALUE[Uzziņas] != 종류) { kļūme_VALUE("null or invalid object reference"); return false; }
        return true;
    }
    static int konstante_SMS(int INDEX) {
        if (!čeks_konstante(INDEX, 1)) return 0;
        if (virkne_Uzziņas[INDEX] != 0) return virkne_Uzziņas[INDEX];
        int Uzziņas = piešķirt_Krātuve(1, konstante_SECOND_VALUE[INDEX]); if (Kļūda) return 0;
        int 끝 = 상가[INDEX] + konstante_SECOND_VALUE[INDEX], numurs = 상가[INDEX], 길이 = 0;
        while (numurs < 끝 && !Kļūda) {
            int VALUE = Fails[numurs++];
            if (VALUE == 0) kļūme_VALUE("invalid modified UTF-8");
            else if (VALUE >= 192 && VALUE <= 223 && numurs < 끝) {
                int Tālāk_krājums = Fails[numurs++];
                if ((Tālāk_krājums & 192) != 128) kļūme_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 31) << 6 | Tālāk_krājums & 63;
                if (VALUE != 0 && VALUE < 128) kļūme_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 224 && VALUE <= 239 && numurs + 1 < 끝) {
                int 가 = Fails[numurs++], SECOND_operands = Fails[numurs++];
                if ((가 & 192) != 128 || (SECOND_operands & 192) != 128) kļūme_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 15) << 12 | (가 & 63) << 6 | SECOND_operands & 63;
                if (VALUE < 2048) kļūme_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 128) kļūme_VALUE("invalid modified UTF-8");
            kaudze_VALUE[Uzziņas + 2 + 길이++] = VALUE;
        }
        kaudze_VALUE[Uzziņas + 1] = 길이; virkne_Uzziņas[INDEX] = Uzziņas; return Uzziņas;
    }
    static int viesot_rakstzīme(String VALUE) {
        int Uzziņas = piešķirt_Krātuve(1, VALUE.length()); if (Kļūda) return 0;
        for (int numurs = 0; numurs < VALUE.length(); numurs++) kaudze_VALUE[Uzziņas + 2 + numurs] = VALUE.charAt(numurs);
        return Uzziņas;
    }
    static void rakstīšana_SMS(int Uzziņas) {
        if (Uzziņas == 0) { lietotājs.Rakstīt("null"); return; }
        if (!objekts_VALUE(Uzziņas, 1)) return;
        for (int numurs = 0; numurs < kaudze_VALUE[Uzziņas + 1]; numurs++) lietotājs.rakstīšana_rakstzīme_VALUE(kaudze_VALUE[Uzziņas + 2 + numurs]);
    }
    static int cipars_rakstzīme(int VALUE) {
        int Uzziņas = piešķirt_Krātuve(1, 11); if (Kļūda) return 0;
        int 길이 = 0;
        if (VALUE < 0) kaudze_VALUE[Uzziņas + 2 + 길이++] = '-'; else VALUE = -VALUE;
        int pozīcijas_indekss = 1000000000; boolean Palaist = false;
        while (pozīcijas_indekss != 0) {
            int numurs = -(VALUE / pozīcijas_indekss);
            if (numurs != 0 || Palaist || pozīcijas_indekss == 1) { kaudze_VALUE[Uzziņas + 2 + 길이++] = '0' + numurs; Palaist = true; }
            VALUE %= pozīcijas_indekss; pozīcijas_indekss /= 10;
        }
        kaudze_VALUE[Uzziņas + 1] = 길이; return Uzziņas;
    }
    static int 정수해독(int Uzziņas) {
        if (!objekts_VALUE(Uzziņas, 1)) return 0;
        int 길이 = kaudze_VALUE[Uzziņas + 1], numurs = 0, VALUE = 0; boolean 음수 = false;
        if (길이 > 0 && (kaudze_VALUE[Uzziņas + 2] == '-' || kaudze_VALUE[Uzziņas + 2] == '+')) { 음수 = kaudze_VALUE[Uzziņas + 2] == '-'; numurs++; }
        if (numurs == 길이) kļūme_VALUE("NumberFormatException");
        for (; numurs < 길이 && !Kļūda; numurs++) {
            int cipars_VALUE = kaudze_VALUE[Uzziņas + 2 + numurs] - '0';
            if (cipars_VALUE < 0 || cipars_VALUE > 9 || VALUE < -214748364 || VALUE == -214748364 && cipars_VALUE > (음수 ? 8 : 7)) kļūme_VALUE("NumberFormatException");
            VALUE = VALUE * 10 - cipars_VALUE;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static void 넣기(int VALUE, int TYPE_VALUE) {
        if (Kļūda) return;
        if (kadrs_INDEX < 0 || kadrs_kopa[kadrs_INDEX] >= metode_kopa[kadrs_metode[kadrs_INDEX]]) { kļūme_VALUE("operand stack overflow"); return; }
        int 칸 = kadrs_INDEX * 128 + kadrs_kopa[kadrs_INDEX]++; operands_kopa_VALUE[칸] = VALUE; operands_kopa_TYPE[칸] = TYPE_VALUE;
    }
    static int 빼기(int TYPE_VALUE) {
        if (Kļūda) return 0;
        if (kadrs_INDEX < 0 || kadrs_kopa[kadrs_INDEX] < 1) { kļūme_VALUE("operand stack underflow"); return 0; }
        int 칸 = kadrs_INDEX * 128 + --kadrs_kopa[kadrs_INDEX]; atdot_TYPE = operands_kopa_TYPE[칸];
        if (TYPE_VALUE != 0 && atdot_TYPE != TYPE_VALUE) kļūme_VALUE("operand type mismatch");
        return operands_kopa_VALUE[칸];
    }
    static void 지역읽기(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[kadrs_metode[kadrs_INDEX]] || INDEX < 0 || vietējs_TYPE[kadrs_INDEX * 128 + INDEX] != TYPE_VALUE) { kļūme_VALUE("invalid or uninitialized local"); return; }
        넣기(vietējs_VALUE[kadrs_INDEX * 128 + INDEX], TYPE_VALUE);
    }
    static void rakstīšana_vietējs(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[kadrs_metode[kadrs_INDEX]] || INDEX < 0) { kļūme_VALUE("local index out of range"); return; }
        int VALUE = 빼기(TYPE_VALUE); vietējs_VALUE[kadrs_INDEX * 128 + INDEX] = VALUE; vietējs_TYPE[kadrs_INDEX * 128 + INDEX] = TYPE_VALUE;
    }
    static int 명바() {
        int Novietojums = kadrs_amats[kadrs_INDEX];
        if (Novietojums < metode_Sākt[kadrs_metode[kadrs_INDEX]] || Novietojums >= metode_beigt_zvanu[kadrs_metode[kadrs_INDEX]]) { kļūme_VALUE("instruction pointer out of range"); return 0; }
        kadrs_amats[kadrs_INDEX]++; return Fails[Novietojums];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void pārvietot_VALUE(int Novietojums) {
        int FUNCTION_VALUE = kadrs_metode[kadrs_INDEX];
        if (Novietojums < metode_Sākt[FUNCTION_VALUE] || Novietojums >= metode_beigt_zvanu[FUNCTION_VALUE] || 경계[Novietojums] != FUNCTION_VALUE + 1) kļūme_VALUE("invalid branch target");
        else kadrs_amats[kadrs_INDEX] = Novietojums;
    }
    static void 호출(int FUNCTION_VALUE) {
        if (kadrs_INDEX == 31) { kļūme_VALUE("call stack limit (32)"); return; }
        int Tālāk_krājums = kadrs_INDEX + 1;
        for (int numurs = 0; numurs < 128; numurs++) vietējs_TYPE[Tālāk_krājums * 128 + numurs] = 0;
        for (int numurs = metode_arg_COUNT[FUNCTION_VALUE] - 1; numurs >= 0; numurs--) {
            vietējs_VALUE[Tālāk_krājums * 128 + numurs] = 빼기(metode_arg_TYPE[FUNCTION_VALUE * 16 + numurs]); vietējs_TYPE[Tālāk_krājums * 128 + numurs] = metode_arg_TYPE[FUNCTION_VALUE * 16 + numurs];
        }
        kadrs_INDEX = Tālāk_krājums; kadrs_metode[kadrs_INDEX] = FUNCTION_VALUE; kadrs_amats[kadrs_INDEX] = metode_Sākt[FUNCTION_VALUE]; kadrs_kopa[kadrs_INDEX] = 0;
    }
    static void atdot_mērs(int TYPE_VALUE) {
        if (TYPE_VALUE != metode_atdot[kadrs_metode[kadrs_INDEX]]) { kļūme_VALUE("return type mismatch"); return; }
        int VALUE = TYPE_VALUE == 0 ? 0 : 빼기(TYPE_VALUE);
        kadrs_INDEX--; if (kadrs_INDEX >= 0 && TYPE_VALUE != 0) 넣기(VALUE, TYPE_VALUE);
    }
    static int[] Stream_faila_nosaukums = new int[64];
    static void Fails_Stream_CALL(int īpašnieks_VALUE, int Nosaukums, int formāts_VALUE, int Komanda) {
        boolean Izvade = Word_SMS(īpašnieks_VALUE, "java/io/FileOutputStream");
        int 종류 = Izvade ? 6 : 5;
        if (Komanda == 183 && Word_SMS(Nosaukums, "<init>")) {
            boolean 이어 = false;
            if (Izvade && Word_SMS(formāts_VALUE, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Word_SMS(formāts_VALUE, "(Ljava/lang/String;)V")) { kļūme_VALUE("unsupported file stream constructor"); return; }
            int Fails_ievade_nosaukums = 빼기(2), Stream_VALUE = 빼기(2);
            if (!objekts_VALUE(Fails_ievade_nosaukums, 1) || !objekts_VALUE(Stream_VALUE, 종류) || Kļūda) return;
            if (kaudze_VALUE[Stream_VALUE + 3] != 0) { kļūme_VALUE("file stream already initialized"); return; }
            int 길이 = kaudze_VALUE[Fails_ievade_nosaukums + 1];
            if (길이 < 1 || 길이 > 63) { kļūme_VALUE("invalid file name length"); return; }
            for (int 칸 = 0; 칸 < 길이; 칸++) {
                int VALUE = kaudze_VALUE[Fails_ievade_nosaukums + 2 + 칸];
                if (VALUE < 1 || VALUE > 127) { kļūme_VALUE("file stream paths currently require ASCII"); return; }
                Stream_faila_nosaukums[칸] = VALUE;
            }
            Stream_faila_nosaukums[길이] = 0;
            int 서술자 = lietotājs.파일서술자열기(Stream_faila_nosaukums, Izvade ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { kļūme_VALUE("FileNotFoundException: file open failed"); return; }
            kaudze_VALUE[Stream_VALUE + 2] = 서술자; kaudze_VALUE[Stream_VALUE + 3] = 1;
            return;
        }
        if (Komanda != 182) { kļūme_VALUE("invalid file stream invocation"); return; }
        int Darbība = -1, VALUE = 0;
        if (Word_SMS(Nosaukums, "close") && Word_SMS(formāts_VALUE, "()V")) Darbība = 0;
        if (!Izvade && Word_SMS(Nosaukums, "read") && Word_SMS(formāts_VALUE, "()I")) Darbība = 1;
        if (Izvade && Word_SMS(Nosaukums, "write") && Word_SMS(formāts_VALUE, "(I)V")) { Darbība = 2; VALUE = 빼기(1); }
        if (Darbība < 0) { kļūme_VALUE("unsupported file stream method"); return; }
        int Stream_VALUE = 빼기(2);
        if (!objekts_VALUE(Stream_VALUE, 종류) || Kļūda) return;
        if (kaudze_VALUE[Stream_VALUE + 3] == 0) { kļūme_VALUE("uninitialized file stream"); return; }
        int 서술자 = kaudze_VALUE[Stream_VALUE + 2];
        if (Darbība == 0) {
            if (서술자 >= 0 && lietotājs.파일서술자닫기(서술자) < 0) kļūme_VALUE("IOException: close failed");
            kaudze_VALUE[Stream_VALUE + 2] = -1; return;
        }
        if (서술자 < 0) { kļūme_VALUE("IOException: stream closed"); return; }
        if (Darbība == 1) {
            int mērs = lietotājs.파일한바이트읽기(서술자);
            if (mērs < -1) kļūme_VALUE("IOException: read failed"); else 넣기(mērs, 1);
        } else if (lietotājs.파일한바이트쓰기(서술자, VALUE) != 1) kļūme_VALUE("IOException: write failed");
    }
    static void CALL_metode(int INDEX, int Komanda) {
        if (!čeks_konstante(INDEX, 10)) return;
        int īpašnieks_VALUE = klases_nosaukums_SMS(상가[INDEX]), Nosaukums = Uzziņas_nosaukums(konstante_SECOND_VALUE[INDEX]), formāts_VALUE = Uzziņas_TYPE(konstante_SECOND_VALUE[INDEX]);
        if (Kļūda) return;
        if (같은말(īpašnieks_VALUE, klases_nosaukums)) {
            if (Komanda != 184) { kļūme_VALUE("only static user methods are supported"); return; }
            for (int numurs = 0; numurs < metode_COUNT; numurs++) if (같은말(Nosaukums, metode_nosaukums_SMS[numurs]) && 같은말(formāts_VALUE, metode_TYPE[numurs])) {
                if ((metode_piekļūt[numurs] & 8) == 0) kļūme_VALUE("method is not static"); else 호출(numurs);
                return;
            }
            kļūme_VALUE("NoSuchMethodError"); return;
        }
        if (Word_SMS(īpašnieks_VALUE, "java/io/FileInputStream") || Word_SMS(īpašnieks_VALUE, "java/io/FileOutputStream")) {
            Fails_Stream_CALL(īpašnieks_VALUE, Nosaukums, formāts_VALUE, Komanda); return;
        }
        if (Komanda == 184 && Word_SMS(īpašnieks_VALUE, "java/lang/Integer") && Word_SMS(Nosaukums, "parseInt") && Word_SMS(formāts_VALUE, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (Komanda == 182 && Word_SMS(īpašnieks_VALUE, "java/io/PrintStream") && (Word_SMS(Nosaukums, "println") || Word_SMS(Nosaukums, "print"))) {
            int TYPE_VALUE = 0, VALUE = 0;
            if (Word_SMS(formāts_VALUE, "(I)V")) { TYPE_VALUE = 1; VALUE = 빼기(1); }
            else if (Word_SMS(formāts_VALUE, "(Z)V")) { TYPE_VALUE = 2; VALUE = 빼기(1); }
            else if (Word_SMS(formāts_VALUE, "(C)V")) { TYPE_VALUE = 3; VALUE = 빼기(1); }
            else if (Word_SMS(formāts_VALUE, "(Ljava/lang/String;)V")) { TYPE_VALUE = 4; VALUE = 빼기(2); }
            else if (!Word_SMS(formāts_VALUE, "()V") || !Word_SMS(Nosaukums, "println")) kļūme_VALUE("unsupported print descriptor");
            if (빼기(2) != -1) kļūme_VALUE("invalid PrintStream receiver");
            if (Kļūda) return;
            if (TYPE_VALUE == 1) 자바도구.rakstīšana_numurs(VALUE);
            if (TYPE_VALUE == 2) lietotājs.Rakstīt(VALUE == 0 ? "false" : "true");
            if (TYPE_VALUE == 3) lietotājs.rakstīšana_rakstzīme_VALUE(VALUE & 65535);
            if (TYPE_VALUE == 4) rakstīšana_SMS(VALUE);
            if (Word_SMS(Nosaukums, "println")) lietotājs.rakstīšana_rakstzīme_VALUE(10);
            return;
        }
        if (Komanda == 182 && Word_SMS(īpašnieks_VALUE, "java/lang/String")) {
            if (Word_SMS(Nosaukums, "length") && Word_SMS(formāts_VALUE, "()I")) {
                int Uzziņas = 빼기(2); if (objekts_VALUE(Uzziņas, 1)) 넣기(kaudze_VALUE[Uzziņas + 1], 1); return;
            }
            if (Word_SMS(Nosaukums, "charAt") && Word_SMS(formāts_VALUE, "(I)C")) {
                int apakšraksts_VALUE = 빼기(1), Uzziņas = 빼기(2);
                if (objekts_VALUE(Uzziņas, 1)) {
                    if (apakšraksts_VALUE < 0 || apakšraksts_VALUE >= kaudze_VALUE[Uzziņas + 1]) kļūme_VALUE("StringIndexOutOfBoundsException"); else 넣기(kaudze_VALUE[Uzziņas + 2 + apakšraksts_VALUE], 1);
                }
                return;
            }
        }
        if (Word_SMS(īpašnieks_VALUE, "java/lang/StringBuilder")) {
            if (Komanda == 183 && Word_SMS(Nosaukums, "<init>") && Word_SMS(formāts_VALUE, "()V")) { objekts_VALUE(빼기(2), 4); return; }
            if (Komanda == 182 && Word_SMS(Nosaukums, "toString") && Word_SMS(formāts_VALUE, "()Ljava/lang/String;")) {
                int Uzziņas = 빼기(2); if (objekts_VALUE(Uzziņas, 4)) 넣기(kaudze_VALUE[Uzziņas + 2] == 0 ? viesot_rakstzīme("") : kaudze_VALUE[Uzziņas + 2], 2); return;
            }
            if (Komanda == 182 && Word_SMS(Nosaukums, "append")) {
                int Teksts = 0;
                if (Word_SMS(formāts_VALUE, "(I)Ljava/lang/StringBuilder;")) Teksts = cipars_rakstzīme(빼기(1));
                else if (Word_SMS(formāts_VALUE, "(Z)Ljava/lang/StringBuilder;")) Teksts = viesot_rakstzīme(빼기(1) == 0 ? "false" : "true");
                else if (Word_SMS(formāts_VALUE, "(C)Ljava/lang/StringBuilder;")) {
                    int VALUE = 빼기(1); Teksts = piešķirt_Krātuve(1, 1); if (!Kļūda) kaudze_VALUE[Teksts + 2] = VALUE & 65535;
                }
                else if (Word_SMS(formāts_VALUE, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { Teksts = 빼기(2); if (Teksts == 0) Teksts = viesot_rakstzīme("null"); }
                else { kļūme_VALUE("unsupported StringBuilder append"); return; }
                int Uzziņas = 빼기(2); if (!objekts_VALUE(Uzziņas, 4) || !objekts_VALUE(Teksts, 1)) return;
                int priekšējā_VALUE = kaudze_VALUE[Uzziņas + 2], 앞길이 = priekšējā_VALUE == 0 ? 0 : kaudze_VALUE[priekšējā_VALUE + 1], 뒤길이 = kaudze_VALUE[Teksts + 1];
                int 새글 = piešķirt_Krātuve(1, 앞길이 + 뒤길이); if (Kļūda) return;
                for (int numurs = 0; numurs < 앞길이; numurs++) kaudze_VALUE[새글 + 2 + numurs] = kaudze_VALUE[priekšējā_VALUE + 2 + numurs];
                for (int numurs = 0; numurs < 뒤길이; numurs++) kaudze_VALUE[새글 + 2 + 앞길이 + numurs] = kaudze_VALUE[Teksts + 2 + numurs];
                kaudze_VALUE[Uzziņas + 2] = 새글; 넣기(Uzziņas, 2); return;
            }
        }
        kļūme_VALUE("unsupported library method");
    }
    static int 배열칸(int Uzziņas, int apakšraksts_VALUE, int TYPE_VALUE) {
        if (!objekts_VALUE(Uzziņas, TYPE_VALUE)) return 0;
        if (apakšraksts_VALUE < 0 || apakšraksts_VALUE >= kaudze_VALUE[Uzziņas + 1]) { kļūme_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return Uzziņas + 2 + apakšraksts_VALUE;
    }
    static void Izpildīt_komanda() {
        int 남음 = 500000;
        while (kadrs_INDEX >= 0 && !Kļūda) {
            if (--남음 == 0) { kļūme_VALUE("instruction limit (500000)"); break; }
            int Palaist = kadrs_amats[kadrs_INDEX], VALUE = 명바();
            if (Kļūda) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int numurs = VALUE == 18 ? 명바() : 명짧();
                if (numurs <= 0 || numurs >= konstante_COUNT) kļūme_VALUE("invalid ldc constant");
                else if (konstante_tags[numurs] == 3) 넣기(상가[numurs], 1);
                else if (konstante_tags[numurs] == 8) 넣기(konstante_SMS(상가[numurs]), 2);
                else kļūme_VALUE("unsupported ldc constant");
                continue;
            }
            if (VALUE == 21 || VALUE == 25) { 지역읽기(명바(), VALUE == 21 ? 1 : 2); continue; }
            if (VALUE >= 26 && VALUE <= 29) { 지역읽기(VALUE - 26, 1); continue; }
            if (VALUE >= 42 && VALUE <= 45) { 지역읽기(VALUE - 42, 2); continue; }
            if (VALUE == 54 || VALUE == 58) { rakstīšana_vietējs(명바(), VALUE == 54 ? 1 : 2); continue; }
            if (VALUE >= 59 && VALUE <= 62) { rakstīšana_vietējs(VALUE - 59, 1); continue; }
            if (VALUE >= 75 && VALUE <= 78) { rakstīšana_vietējs(VALUE - 75, 2); continue; }
            if (VALUE == 46 || VALUE == 50) {
                int apakšraksts_VALUE = 빼기(1), Uzziņas = 빼기(2), 칸 = 배열칸(Uzziņas, apakšraksts_VALUE, VALUE == 46 ? 2 : 3);
                if (!Kļūda) 넣기(kaudze_VALUE[칸], VALUE == 46 ? 1 : 2); continue;
            }
            if (VALUE == 79 || VALUE == 83) {
                int krājums_elements = 빼기(VALUE == 79 ? 1 : 2), apakšraksts_VALUE = 빼기(1), Uzziņas = 빼기(2), 칸 = 배열칸(Uzziņas, apakšraksts_VALUE, VALUE == 79 ? 2 : 3);
                if (VALUE == 83 && krājums_elements != 0) objekts_VALUE(krājums_elements, 1);
                if (!Kļūda) kaudze_VALUE[칸] = krājums_elements; continue;
            }
            if (VALUE == 87) { 빼기(0); continue; }
            if (VALUE == 89) { int 가 = 빼기(0), TYPE_VALUE = atdot_TYPE; 넣기(가, TYPE_VALUE); 넣기(가, TYPE_VALUE); continue; }
            if (VALUE == 95) { int 가 = 빼기(0), 가형 = atdot_TYPE, SECOND_operands = 빼기(0), SECOND_operands_TYPE = atdot_TYPE; 넣기(가, 가형); 넣기(SECOND_operands, SECOND_operands_TYPE); continue; }
            if (VALUE == 96 || VALUE == 100 || VALUE == 104 || VALUE == 108 || VALUE == 112 || VALUE == 120
                || VALUE == 122 || VALUE == 124 || VALUE == 126 || VALUE == 128 || VALUE == 130) {
                int SECOND_operands = 빼기(1), 가 = 빼기(1), mērs = 0;
                if ((VALUE == 108 || VALUE == 112) && SECOND_operands == 0) { kļūme_VALUE("ArithmeticException: / by zero"); continue; }
                if (VALUE == 96) mērs = 가 + SECOND_operands;
                if (VALUE == 100) mērs = 가 - SECOND_operands;
                if (VALUE == 104) mērs = 가 * SECOND_operands;
                if (VALUE == 108) mērs = 가 / SECOND_operands;
                if (VALUE == 112) mērs = 가 % SECOND_operands;
                if (VALUE == 120) mērs = 가 << SECOND_operands;
                if (VALUE == 122) mērs = 가 >> SECOND_operands;
                if (VALUE == 124) mērs = 가 >>> SECOND_operands;
                if (VALUE == 126) mērs = 가 & SECOND_operands;
                if (VALUE == 128) mērs = 가 | SECOND_operands;
                if (VALUE == 130) mērs = 가 ^ SECOND_operands;
                넣기(mērs, 1); continue;
            }
            if (VALUE == 116) { 넣기(-빼기(1), 1); continue; }
            if (VALUE == 132) {
                int vietējs_Tvērums = 명바(), palielinājums_solis = (byte)명바(); 지역읽기(vietējs_Tvērums, 1); 넣기(빼기(1) + palielinājums_solis, 1); rakstīšana_vietējs(vietējs_Tvērums, 1); continue;
            }
            if (VALUE >= 145 && VALUE <= 147) {
                int numurs = 빼기(1); 넣기(VALUE == 145 ? (byte)numurs : VALUE == 146 ? (char)numurs : (short)numurs, 1); continue;
            }
            if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                int mērķis_VALUE = Palaist + (short)명짧(); boolean 갈까 = VALUE == 167;
                if (VALUE >= 153 && VALUE <= 158) {
                    int numurs = 빼기(1); 갈까 = VALUE == 153 ? numurs == 0 : VALUE == 154 ? numurs != 0 : VALUE == 155 ? numurs < 0 : VALUE == 156 ? numurs >= 0 : VALUE == 157 ? numurs > 0 : numurs <= 0;
                } else if (VALUE >= 159 && VALUE <= 166) {
                    int SECOND_operands = 빼기(VALUE >= 165 ? 2 : 1), 가 = 빼기(VALUE >= 165 ? 2 : 1);
                    갈까 = VALUE == 159 || VALUE == 165 ? 가 == SECOND_operands : VALUE == 160 || VALUE == 166 ? 가 != SECOND_operands : VALUE == 161 ? 가 < SECOND_operands : VALUE == 162 ? 가 >= SECOND_operands : VALUE == 163 ? 가 > SECOND_operands : 가 <= SECOND_operands;
                } else if (VALUE == 198 || VALUE == 199) { int numurs = 빼기(2); 갈까 = VALUE == 198 ? numurs == 0 : numurs != 0; }
                if (갈까) pārvietot_VALUE(mērķis_VALUE); continue;
            }
            if (VALUE == 172 || VALUE == 176 || VALUE == 177) { atdot_mērs(VALUE == 172 ? 1 : VALUE == 176 ? 2 : 0); continue; }
            if (VALUE == 178) {
                int numurs = 명짧(); if (!čeks_konstante(numurs, 9)) continue;
                if (!Word_SMS(klases_nosaukums_SMS(상가[numurs]), "java/lang/System") || !Word_SMS(Uzziņas_nosaukums(konstante_SECOND_VALUE[numurs]), "out")
                    || !Word_SMS(Uzziņas_TYPE(konstante_SECOND_VALUE[numurs]), "Ljava/io/PrintStream;")) kļūme_VALUE("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (VALUE == 182 || VALUE == 183 || VALUE == 184) { CALL_metode(명짧(), VALUE); continue; }
            if (VALUE == 187) {
                int Nosaukums = klases_nosaukums_SMS(명짧());
                if (Word_SMS(Nosaukums, "java/lang/StringBuilder")) 넣기(piešķirt_Krātuve(4, 1), 2);
                else if (Word_SMS(Nosaukums, "java/io/FileInputStream") || Word_SMS(Nosaukums, "java/io/FileOutputStream")) {
                    int Uzziņas = piešķirt_Krātuve(Word_SMS(Nosaukums, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!Kļūda) { kaudze_VALUE[Uzziņas + 2] = -1; 넣기(Uzziņas, 2); }
                } else kļūme_VALUE("unsupported object construction");
                continue;
            }
            if (VALUE == 188 || VALUE == 189) {
                if (VALUE == 188) { if (명바() != 10) kļūme_VALUE("only int[] newarray is supported"); }
                else if (!Word_SMS(klases_nosaukums_SMS(명짧()), "java/lang/String")) kļūme_VALUE("only String[] anewarray is supported");
                int 길이 = 빼기(1); 넣기(piešķirt_Krātuve(VALUE == 188 ? 2 : 3, 길이), 2); continue;
            }
            if (VALUE == 190) {
                int Uzziņas = 빼기(2);
                if (Uzziņas < 1 || Uzziņas >= kaudze_beigt_zvanu_amats - 1 || (kaudze_VALUE[Uzziņas] != 2 && kaudze_VALUE[Uzziņas] != 3)) kļūme_VALUE("null or invalid array");
                else 넣기(kaudze_VALUE[Uzziņas + 1], 1); continue;
            }
            if (VALUE == 192) {
                int Nosaukums = klases_nosaukums_SMS(명짧()), Uzziņas = 빼기(2);
                if (!Word_SMS(Nosaukums, "java/lang/String")) kļūme_VALUE("unsupported checkcast");
                else if (Uzziņas != 0) objekts_VALUE(Uzziņas, 1);
                넣기(Uzziņas, 2); continue;
            }
            kļūme_VALUE("unsupported bytecode");
        }
    }
    public static int Palaist() {
        if (lietotājs.인수개수() == 1 && 자바도구.같음(lietotājs.Parametri(0), "-version")) {
            lietotājs.Rakstīt("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (lietotājs.인수개수() < 1) { lietotājs.Rakstīt("Usage: java CLASS [ARGS]\n"); return 2; }
        int 길이 = 자바도구.Nosaukums(faila_nosaukums_SMS, lietotājs.Parametri(0));
        if (길이 < 1 || 길이 > 57) { lietotājs.Rakstīt("java: invalid class name\n"); return 2; }
        faila_nosaukums_SMS[길이] = '.'; faila_nosaukums_SMS[길이 + 1] = 'c'; faila_nosaukums_SMS[길이 + 2] = 'l'; faila_nosaukums_SMS[길이 + 3] = 'a'; faila_nosaukums_SMS[길이 + 4] = 's'; faila_nosaukums_SMS[길이 + 5] = 's';
        Izmērs = lietotājs.파일읽기(faila_nosaukums_SMS, Fails);
        if (Izmērs < 0) { lietotājs.Rakstīt("java: cannot read class: "); 자바도구.rakstīšana_numurs(Izmērs); lietotājs.rakstīšana_rakstzīme_VALUE(10); return 1; }
        클래스읽기(); if (Kļūda) return 1;
        int rakstzīme_nosaukums = konstante_SMS(klases_nosaukums);
        if (!Kļūda && kaudze_VALUE[rakstzīme_nosaukums + 1] != 길이) kļūme_VALUE("class name does not match file");
        for (int numurs = 0; numurs < 길이 && !Kļūda; numurs++) if (kaudze_VALUE[rakstzīme_nosaukums + 2 + numurs] != faila_nosaukums_SMS[numurs]) kļūme_VALUE("class name does not match file");
        int ieejas_punkts_VALUE = -1;
        for (int numurs = 0; numurs < metode_COUNT; numurs++) if (Word_SMS(metode_nosaukums_SMS[numurs], "main") && Word_SMS(metode_TYPE[numurs], "([Ljava/lang/String;)V") && (metode_piekļūt[numurs] & 9) == 9) ieejas_punkts_VALUE = numurs;
        if (ieejas_punkts_VALUE < 0) kļūme_VALUE("public static void main(String[] args) required");
        if (Kļūda) return 1;
        int Parametri = piešķirt_Krātuve(3, lietotājs.인수개수() - 1);
        for (int numurs = 1; numurs < lietotājs.인수개수() && !Kļūda; numurs++) kaudze_VALUE[Parametri + 1 + numurs] = viesot_rakstzīme(lietotājs.Parametri(numurs));
        kadrs_INDEX = 0; kadrs_metode[0] = ieejas_punkts_VALUE; kadrs_amats[0] = metode_Sākt[ieejas_punkts_VALUE]; vietējs_VALUE[0] = Parametri; vietējs_TYPE[0] = 2;
        Izpildīt_komanda(); return Kļūda ? 1 : 0;
    }
}
