// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. Fil/operand_Stak/referere/gren 경계를 Udfør_kommando 중 검사한다. */
public final class 자바가상기계 {
    static int[] Fil = new int[16 * 16384], midlertidig_fil = new int[16384], filnavn_sms = new int[512];
    static int[] konstant_tag = new int[8192], 상가 = new int[8192], konstant_SEKUND_VÆRDI = new int[8192], streng_referere = new int[8192];
    static int[] metode_navn_sms = new int[512], metode_Type = new int[512], metode_åbne = new int[512], metode_ejer = new int[512];
    static int[] metode_START = new int[512], metode_afslutte_et_opkald = new int[512], metode_Stak = new int[512], 함수지역 = new int[512];
    static int[] metode_argument_TÆL = new int[512], metode_argument_Type = new int[8192], metode_returnere = new int[512];
    static int[] grænse_VÆRDI = new int[16 * 16384];
    static int[] lokal_VÆRDI = new int[16384], lokal_Type = new int[16384], operand_Stak_VÆRDI = new int[16384], operand_Stak_Type = new int[16384];
    static int[] ramme_metode = new int[128], ramme_placere = new int[128], ramme_Stak = new int[128], 틀명령 = new int[128], starte_ramme = new int[128];
    static int[] Hold_Definition_navn = new int[16], Hold_Definition_tilpasse_størrelse = new int[16], Hold_Definition_overordnet = new int[16], Hold_Definition_status = new int[16], Hold_udvidelsesstik_TÆL = new int[16], starte_Hold_Definition = new int[16];
    static int[] Hold_grænseflade = new int[16 * 16], Hold_grænseflade_TÆL = new int[16];
    static int[] udvidelsesstik_navn = new int[512], udvidelsesstik_Type = new int[512], udvidelsesstik_ejer = new int[512], udvidelsesstik_Tilladelser = new int[512], udvidelsesstik_placere = new int[512], udvidelsesstik_data = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] heap_VÆRDI = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], heap_referere = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], matrixelement = new int[32768], Store_heltal = new int[256];
    static int Størrelse, 읽기위치, metode_TÆL, klassenavn, ramme_INDEKS = -1, heap_afslutte_et_opkald_placere = 1, returnere_Type;
    static int Hold_Definition_TÆL, udvidelsesstik_TÆL, 잡기수, 현재읽는종, 던진객체, 잠시수, vise_TÆL, Samling_TÆL;
    static int aktuel_tråd, Antal_tråde = 1, post_Hold_Definition;
    static int[] tråd_ramme = new int[4], tråd_status = new int[4], tråd_objekt = new int[4], tråd_mål = new int[4], 가닥대기 = new int[4];
    static boolean fejl, ændringsanmodning;
    static int[] lås_ejer = new int[32768], 잠금깊이 = new int[32768], ramme_lås = new int[128], Hold_lås = new int[16], Hold_tråd = new int[16];

    static void fejl_VÆRDI(String Ord_sms) {
        if (fejl) return;
        int område_KODE = 0;
        if (자바도구.같음(Ord_sms, "ArithmeticException: / by zero")) område_KODE = 4;
        if (자바도구.같음(Ord_sms, "NullPointerException") || 자바도구.같음(Ord_sms, "null or invalid array")) område_KODE = 5;
        if (자바도구.같음(Ord_sms, "ArrayIndexOutOfBoundsException")) område_KODE = 7;
        if (자바도구.같음(Ord_sms, "StringIndexOutOfBoundsException")) område_KODE = 8;
        if (자바도구.같음(Ord_sms, "NumberFormatException")) område_KODE = 10;
        if (자바도구.같음(Ord_sms, "FileNotFoundException: file open failed")) område_KODE = 12;
        if (자바도구.같음(Ord_sms, "IOException: stream closed") || 자바도구.같음(Ord_sms, "IOException: read failed") || 자바도구.같음(Ord_sms, "IOException: write failed")) område_KODE = 11;
        if (자바도구.같음(Ord_sms, "ClassCastException")) område_KODE = 14;
        if (자바도구.같음(Ord_sms, "NegativeArraySizeException")) område_KODE = 15;
        if (område_KODE != 0 && ramme_INDEKS >= 0) { 예외던짐(område_KODE, Ord_sms); return; }
        bruger.Skrive("JVM error: "); bruger.Skrive(Ord_sms); bruger.skrive_tegn_VÆRDI(10); fejl = true;
    }
    static boolean klippe(int Kør_2, int varighed_VÆRDI) {
        if (Kør_2 < 0 || Kør_2 >= Fil.length || varighed_VÆRDI < 0) return false;
        int Hold_Definition = Kør_2 / 16384;
        return Kør_2 % 16384 <= Hold_Definition_tilpasse_størrelse[Hold_Definition] && varighed_VÆRDI <= Hold_Definition_tilpasse_størrelse[Hold_Definition] - Kør_2 % 16384;
    }
    static int byte_VÆRDI() {
        if (!klippe(읽기위치, 1)) { fejl_VÆRDI("truncated class file"); return 0; }
        return Fil[읽기위치++];
    }
    static int 짧은수() { return byte_VÆRDI() << 8 | byte_VÆRDI(); }
    static int heltal() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int varighed_VÆRDI) { if (!klippe(읽기위치, varighed_VÆRDI)) fejl_VÆRDI("invalid attribute size"); else 읽기위치 += varighed_VÆRDI; }
    static boolean check_konstant(int tal, int 종류) {
        if (tal <= 0 || tal >= konstant_tag.length || konstant_tag[tal] != 종류) { fejl_VÆRDI("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean sms_område(int Kør_2, int varighed_VÆRDI, String Ord_sms) {
        if (!klippe(Kør_2, varighed_VÆRDI)) return false;
        int 읽는자리 = Kør_2, 끝 = Kør_2 + varighed_VÆRDI;
        for (int Loop_INDEKS = 0; Loop_INDEKS < Ord_sms.length(); Loop_INDEKS++) {
            int tegnkode = Ord_sms.charAt(Loop_INDEKS);
            if (tegnkode > 0 && tegnkode < 128) { if (읽는자리 >= 끝 || Fil[읽는자리++] != tegnkode) return false; }
            else if (tegnkode < 2048) {
                if (읽는자리 + 2 > 끝 || Fil[읽는자리++] != (192 | (tegnkode >> 6)) || Fil[읽는자리++] != (128 | (tegnkode & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || Fil[읽는자리++] != (224 | (tegnkode >> 12)) || Fil[읽는자리++] != (128 | ((tegnkode >> 6) & 63)) || Fil[읽는자리++] != (128 | (tegnkode & 63))) return false;
        }
        return 읽는자리 == 끝;
    }
    static boolean Ord_sms(int konstant_VÆRDI, String Ord_sms) { return check_konstant(konstant_VÆRDI, 1) && sms_område(상가[konstant_VÆRDI], konstant_SEKUND_VÆRDI[konstant_VÆRDI], Ord_sms); }
    static boolean afstemning_Ord(int 가, int SEKUND_operand) {
        if (!check_konstant(가, 1) || !check_konstant(SEKUND_operand, 1) || konstant_SEKUND_VÆRDI[가] != konstant_SEKUND_VÆRDI[SEKUND_operand]) return false;
        for (int tal = 0; tal < konstant_SEKUND_VÆRDI[가]; tal++) if (Fil[상가[가] + tal] != Fil[상가[SEKUND_operand] + tal]) return false;
        return true;
    }
    static int klassenavn_sms(int tal) { return check_konstant(tal, 7) && check_konstant(상가[tal], 1) ? 상가[tal] : 0; }
    static int referere_navn(int tal) { return check_konstant(tal, 12) && check_konstant(상가[tal], 1) ? 상가[tal] : 0; }
    static int referencetype(int tal) { return check_konstant(tal, 12) && check_konstant(konstant_SEKUND_VÆRDI[tal], 1) ? konstant_SEKUND_VÆRDI[tal] : 0; }
    static int 서술형(int 끝, boolean 빈형) {
        if (읽기위치 >= 끝) { fejl_VÆRDI("invalid descriptor"); return 0; }
        int VÆRDI = byte_VÆRDI();
        if (VÆRDI == 'V' && 빈형) return 0;
        if (VÆRDI == 'I' || VÆRDI == 'B' || VÆRDI == 'C' || VÆRDI == 'S' || VÆRDI == 'Z') return 1;
        if (VÆRDI == '[') { 서술형(끝, false); return 2; }
        if (VÆRDI == 'L') {
            int Kør_2 = 읽기위치;
            while (읽기위치 < 끝 && Fil[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == Kør_2) fejl_VÆRDI("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        fejl_VÆRDI("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int FUNKTION_VÆRDI) {
        int Forrige_vare = 읽기위치, tal = metode_Type[FUNKTION_VÆRDI];
        if (!check_konstant(tal, 1)) return;
        읽기위치 = 상가[tal]; int 끝 = 읽기위치 + konstant_SEKUND_VÆRDI[tal];
        if (byte_VÆRDI() != '(') fejl_VÆRDI("invalid method descriptor");
        int vare_TÆL = 0;
        while (!fejl && 읽기위치 < 끝 && Fil[읽기위치] != ')') {
            if (vare_TÆL == 16) { fejl_VÆRDI("too many method arguments"); break; }
            metode_argument_Type[FUNKTION_VÆRDI * 16 + vare_TÆL++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || byte_VÆRDI() != ')') fejl_VÆRDI("invalid method descriptor");
        metode_returnere[FUNKTION_VÆRDI] = 서술형(끝, true); metode_argument_TÆL[FUNKTION_VÆRDI] = vare_TÆL;
        if (읽기위치 != 끝) fejl_VÆRDI("invalid method descriptor");
        읽기위치 = Forrige_vare;
    }
    static int 상번호() { int VÆRDI = 짧은수(); return VÆRDI == 0 ? 0 : 현재읽는종 * 512 + VÆRDI; }
    static int 명상수() { return metode_ejer[ramme_metode[ramme_INDEKS]] * 512 + 명짧(); }
    static void springe_over_attribut() {
        int vare_TÆL = 짧은수();
        for (int tal = 0; tal < vare_TÆL && !fejl; tal++) { check_konstant(상번호(), 1); 건너(heltal()); }
    }
    static int kommando_varighed(int VÆRDI) {
        if (VÆRDI == 16 || VÆRDI == 18 || VÆRDI == 21 || VÆRDI == 25 || VÆRDI == 54 || VÆRDI == 58 || VÆRDI == 188) return 2;
        if (VÆRDI == 17 || VÆRDI == 19 || VÆRDI == 132 || VÆRDI >= 153 && VÆRDI <= 167
            || VÆRDI >= 178 && VÆRDI <= 184 || VÆRDI == 187 || VÆRDI == 189 || VÆRDI == 192 || VÆRDI == 193 || VÆRDI == 198 || VÆRDI == 199) return 3;
        if (VÆRDI == 185 || VÆRDI == 200) return 5;
        if (VÆRDI >= 0 && VÆRDI <= 8 || VÆRDI >= 26 && VÆRDI <= 29 || VÆRDI >= 42 && VÆRDI <= 46 || VÆRDI >= 50 && VÆRDI <= 53
            || VÆRDI >= 59 && VÆRDI <= 62 || VÆRDI >= 75 && VÆRDI <= 79 || VÆRDI >= 83 && VÆRDI <= 95
            || VÆRDI == 96 || VÆRDI == 100 || VÆRDI == 104 || VÆRDI == 108 || VÆRDI == 112 || VÆRDI == 116
            || VÆRDI == 120 || VÆRDI == 122 || VÆRDI == 124 || VÆRDI == 126 || VÆRDI == 128 || VÆRDI == 130
            || VÆRDI >= 145 && VÆRDI <= 147 || VÆRDI == 172 || VÆRDI == 176 || VÆRDI == 177 || VÆRDI == 190 || VÆRDI == 191
            || VÆRDI == 194 || VÆRDI == 195) return 1;
        return 0;
    }
    static int placere_heltal(int 읽는자리) {
        if (!klippe(읽는자리, 4)) { fejl_VÆRDI("truncated bytecode operand"); return 0; }
        return Fil[읽는자리] << 24 | Fil[읽는자리 + 1] << 16 | Fil[읽는자리 + 2] << 8 | Fil[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int Kør_2, int 끝) {
        int VÆRDI = Fil[읽는자리], varighed_VÆRDI = kommando_varighed(VÆRDI);
        if (VÆRDI == 170 || VÆRDI == 171) {
            int BASIS_placere = 읽는자리 + 1;
            while ((BASIS_placere - Kør_2) % 4 != 0) BASIS_placere++;
            if (끝 - BASIS_placere < (VÆRDI == 170 ? 12 : 8)) return 0;
            int post_TÆL_8f7753a1 = VÆRDI == 170 ? placere_heltal(BASIS_placere + 8) - placere_heltal(BASIS_placere + 4) + 1 : placere_heltal(BASIS_placere + 4);
            if (post_TÆL_8f7753a1 < 0 || post_TÆL_8f7753a1 > 2048) return 0;
            varighed_VÆRDI = BASIS_placere - 읽는자리 + (VÆRDI == 170 ? 12 + 4 * post_TÆL_8f7753a1 : 8 + 8 * post_TÆL_8f7753a1);
        }
        if (VÆRDI == 196 && 읽는자리 + 1 < 끝) {
            int Ord_data = Fil[읽는자리 + 1]; varighed_VÆRDI = Ord_data == 132 ? 6 : (Ord_data == 21 || Ord_data == 25 || Ord_data == 54 || Ord_data == 58) ? 4 : 0;
        }
        return varighed_VÆRDI > 0 && varighed_VÆRDI <= 끝 - 읽는자리 ? varighed_VÆRDI : 0;
    }
    static void check_destination_VÆRDI(int destination_VÆRDI, int FUNKTION_VÆRDI) {
        if (destination_VÆRDI < metode_START[FUNKTION_VÆRDI] || destination_VÆRDI >= metode_afslutte_et_opkald[FUNKTION_VÆRDI] || grænse_VÆRDI[destination_VÆRDI] != FUNKTION_VÆRDI + 1) fejl_VÆRDI("invalid branch target");
    }
    static void 클래스읽기(int Hold_Definition) {
        현재읽는종 = Hold_Definition; 읽기위치 = Hold_Definition * 16384; Størrelse = 읽기위치 + Hold_Definition_tilpasse_størrelse[Hold_Definition];
        if (heltal() != 0xcafebabe) { fejl_VÆRDI("not a class file"); return; }
        int 부판 = 짧은수(), version_VÆRDI = 짧은수();
        if (version_VÆRDI < 45 || version_VÆRDI > 52 || 부판 != 0) { fejl_VÆRDI("supported class versions: 45..52, minor 0"); return; }
        int konstant_TÆL = 짧은수(), BASIS_placere = Hold_Definition * 512;
        if (konstant_TÆL < 1 || konstant_TÆL > 512) { fejl_VÆRDI("constant pool limit (511)"); return; }
        for (int post_TÆL_8f7753a1 = 1; post_TÆL_8f7753a1 < konstant_TÆL && !fejl; post_TÆL_8f7753a1++) {
            int tal = BASIS_placere + post_TÆL_8f7753a1, 종류 = byte_VÆRDI(); konstant_tag[tal] = 종류;
            if (종류 == 1) { konstant_SEKUND_VÆRDI[tal] = 짧은수(); 상가[tal] = 읽기위치; 건너(konstant_SEKUND_VÆRDI[tal]); }
            else if (종류 == 3) 상가[tal] = heltal();
            else if (종류 == 7 || 종류 == 8) 상가[tal] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[tal] = 상번호(); konstant_SEKUND_VÆRDI[tal] = 상번호(); }
            else fejl_VÆRDI("unsupported constant type");
        }
        int rettighed_VÆRDI = 짧은수();
        if ((rettighed_VÆRDI & (0x2000 | 0x4000)) != 0) fejl_VÆRDI("annotation/enum class unsupported");
        Hold_Definition_navn[Hold_Definition] = klassenavn_sms(상번호());
        Hold_Definition_overordnet[Hold_Definition] = klassenavn_sms(상번호());
        int grænseflade_TÆL = 짧은수(); if (grænseflade_TÆL > 16) { fejl_VÆRDI("interface count limit"); return; }
        Hold_grænseflade_TÆL[Hold_Definition] = grænseflade_TÆL;
        for (int Loop_INDEKS = 0; Loop_INDEKS < grænseflade_TÆL; Loop_INDEKS++) Hold_grænseflade[Hold_Definition * 16 + Loop_INDEKS] = klassenavn_sms(상번호());
        int felt_TÆL = 짧은수();
        if (felt_TÆL > 512 - udvidelsesstik_TÆL) { fejl_VÆRDI("field count limit (512)"); return; }
        for (int Loop_INDEKS = 0; Loop_INDEKS < felt_TÆL && !fejl; Loop_INDEKS++) {
            int fil_INDEKS = udvidelsesstik_TÆL++; udvidelsesstik_ejer[fil_INDEKS] = Hold_Definition; udvidelsesstik_Tilladelser[fil_INDEKS] = 짧은수(); udvidelsesstik_navn[fil_INDEKS] = 상번호(); udvidelsesstik_Type[fil_INDEKS] = 상번호();
            check_konstant(udvidelsesstik_navn[fil_INDEKS], 1); check_konstant(udvidelsesstik_Type[fil_INDEKS], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[udvidelsesstik_Type[fil_INDEKS]]; int område_KODE = 서술형(읽기위치 + konstant_SEKUND_VÆRDI[udvidelsesstik_Type[fil_INDEKS]], false); 읽기위치 = 보존값;
            if ((udvidelsesstik_Tilladelser[fil_INDEKS] & 8) == 0) udvidelsesstik_placere[fil_INDEKS] = Hold_udvidelsesstik_TÆL[Hold_Definition]++;
            int attribut_data = 짧은수();
            for (int indre_placere = 0; indre_placere < attribut_data && !fejl; indre_placere++) {
                int navn_konstant = 상번호(), gyldig_varighed = heltal();
                if (Ord_sms(navn_konstant, "ConstantValue") && gyldig_varighed == 2) {
                    int data_VÆRDI = 상번호();
                    if (område_KODE == 1 && check_konstant(data_VÆRDI, 3)) udvidelsesstik_data[fil_INDEKS] = 상가[data_VÆRDI];
                    else if (område_KODE == 2 && check_konstant(data_VÆRDI, 8)) udvidelsesstik_data[fil_INDEKS] = konstant_sms(상가[data_VÆRDI]);
                } else 건너(gyldig_varighed);
            }
        }
        int vare_TÆL = 짧은수();
        if (vare_TÆL > 512 - metode_TÆL) { fejl_VÆRDI("method count limit (512)"); return; }
        for (int Loop_INDEKS = 0; Loop_INDEKS < vare_TÆL && !fejl; Loop_INDEKS++) {
            int tal = metode_TÆL++; metode_ejer[tal] = Hold_Definition;
            metode_åbne[tal] = 짧은수(); metode_navn_sms[tal] = 상번호(); metode_Type[tal] = 상번호();
            check_konstant(metode_navn_sms[tal], 1); 서술읽기(tal);
            if ((metode_åbne[tal] & 8) == 0) {
                if (metode_argument_TÆL[tal] == 16) { fejl_VÆRDI("too many instance method arguments"); return; }
                for (int Sammenligning_placere = metode_argument_TÆL[tal]; Sammenligning_placere > 0; Sammenligning_placere--) metode_argument_Type[tal * 16 + Sammenligning_placere] = metode_argument_Type[tal * 16 + Sammenligning_placere - 1];
                metode_argument_Type[tal * 16] = 2; metode_argument_TÆL[tal]++;
            }
            if ((metode_åbne[tal] & 0x100) != 0) fejl_VÆRDI("user native method unsupported");
            if (Ord_sms(metode_navn_sms[tal], "<clinit>")) starte_Hold_Definition[Hold_Definition] = tal + 1;
            for (int frontvendt_VÆRDI = 0; frontvendt_VÆRDI < tal; frontvendt_VÆRDI++) if (metode_ejer[frontvendt_VÆRDI] == Hold_Definition && afstemning_Ord(metode_navn_sms[frontvendt_VÆRDI], metode_navn_sms[tal]) && afstemning_Ord(metode_Type[frontvendt_VÆRDI], metode_Type[tal])) fejl_VÆRDI("duplicate method");
            int attribut_TÆL = 짧은수();
            for (int attribut_VÆRDI = 0; attribut_VÆRDI < attribut_TÆL && !fejl; attribut_VÆRDI++) {
                int Navn = 상번호(), varighed_VÆRDI = heltal(), Kør_2 = 읽기위치;
                if (!klippe(Kør_2, varighed_VÆRDI)) { fejl_VÆRDI("truncated method attribute"); break; }
                if (Ord_sms(Navn, "Code")) {
                    if (metode_START[tal] != 0) fejl_VÆRDI("duplicate Code attribute");
                    metode_Stak[tal] = 짧은수(); 함수지역[tal] = 짧은수(); int KODE_varighed = heltal();
                    if (metode_Stak[tal] > 128 || 함수지역[tal] > 128 || 함수지역[tal] < metode_argument_TÆL[tal]
                        || KODE_varighed < 1 || KODE_varighed > 8192) fejl_VÆRDI("method memory limits exceeded");
                    metode_START[tal] = 읽기위치; 건너(KODE_varighed); metode_afslutte_et_opkald[tal] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { fejl_VÆRDI("exception table limit"); return; }
                    for (int indre_placere = 0; indre_placere < 잡는수; indre_placere++) {
                        int fejl_referere = 잡기수++; 잡기함수[fejl_referere] = tal;
                        잡기시작[fejl_referere] = metode_START[tal] + 짧은수(); 잡기끝[fejl_referere] = metode_START[tal] + 짧은수();
                        잡기위치[fejl_referere] = metode_START[tal] + 짧은수(); int 부호값 = 상번호(); 잡기종[fejl_referere] = 부호값 == 0 ? 0 : klassenavn_sms(부호값);
                    }
                    springe_over_attribut();
                    if (읽기위치 != Kør_2 + varighed_VÆRDI) fejl_VÆRDI("Code attribute size mismatch");
                } else 건너(varighed_VÆRDI);
            }
            if ((metode_åbne[tal] & 0x400) != 0) continue;
            if (metode_START[tal] == 0) fejl_VÆRDI("missing Code attribute");
            int udvidelsesstik_post = metode_START[tal];
            while (udvidelsesstik_post < metode_afslutte_et_opkald[tal] && !fejl) {
                int varighed_VÆRDI = 길이읽기(udvidelsesstik_post, metode_START[tal], metode_afslutte_et_opkald[tal]);
                if (varighed_VÆRDI == 0) { fejl_VÆRDI("unsupported or truncated bytecode"); break; }
                grænse_VÆRDI[udvidelsesstik_post] = tal + 1; udvidelsesstik_post += varighed_VÆRDI;
            }
            udvidelsesstik_post = metode_START[tal];
            while (udvidelsesstik_post < metode_afslutte_et_opkald[tal] && !fejl) {
                int VÆRDI = Fil[udvidelsesstik_post];
                if (VÆRDI >= 153 && VÆRDI <= 167 || VÆRDI == 198 || VÆRDI == 199) check_destination_VÆRDI(udvidelsesstik_post + (short)(Fil[udvidelsesstik_post + 1] << 8 | Fil[udvidelsesstik_post + 2]), tal);
                if (VÆRDI == 200) check_destination_VÆRDI(udvidelsesstik_post + placere_heltal(udvidelsesstik_post + 1), tal);
                if (VÆRDI == 170 || VÆRDI == 171) {
                    int 읽는자리 = udvidelsesstik_post + 1; while ((읽는자리 - metode_START[tal]) % 4 != 0) 읽는자리++;
                    check_destination_VÆRDI(udvidelsesstik_post + placere_heltal(읽는자리), tal);
                    int post_TÆL_8f7753a1 = VÆRDI == 170 ? placere_heltal(읽는자리 + 8) - placere_heltal(읽는자리 + 4) + 1 : placere_heltal(읽는자리 + 4);
                    읽는자리 += VÆRDI == 170 ? 12 : 8;
                    for (int indre_placere = 0; indre_placere < post_TÆL_8f7753a1; indre_placere++) check_destination_VÆRDI(udvidelsesstik_post + placere_heltal(읽는자리 + indre_placere * (VÆRDI == 170 ? 4 : 8) + (VÆRDI == 170 ? 0 : 4)), tal);
                }
                udvidelsesstik_post += 길이읽기(udvidelsesstik_post, metode_START[tal], metode_afslutte_et_opkald[tal]);
            }
            for (int indre_placere = 0; indre_placere < 잡기수; indre_placere++) if (잡기함수[indre_placere] == tal) {
                check_destination_VÆRDI(잡기시작[indre_placere], tal); check_destination_VÆRDI(잡기위치[indre_placere], tal);
                if (잡기끝[indre_placere] != metode_afslutte_et_opkald[tal]) check_destination_VÆRDI(잡기끝[indre_placere], tal);
                if (잡기시작[indre_placere] >= 잡기끝[indre_placere]) fejl_VÆRDI("invalid exception range");
            }
        }
        if (!fejl) springe_over_attribut();
        if (읽기위치 != Størrelse) fejl_VÆRDI("extra class file data");
    }
    static int tildel_Lager(int 종류, int varighed_VÆRDI) { return 새기억(종류, varighed_VÆRDI); }
    static boolean objekt_VÆRDI(int referere, int 종류) {
        if (!it_gyldig_objekt(referere)) return false;
        if (heap_VÆRDI[referere] != 종류) { fejl_VÆRDI("object type mismatch"); return false; }
        return true;
    }
    static int konstant_sms(int INDEKS) {
        if (!check_konstant(INDEKS, 1)) return 0;
        if (streng_referere[INDEKS] != 0) return streng_referere[INDEKS];
        int referere = tildel_Lager(1, konstant_SEKUND_VÆRDI[INDEKS]); if (fejl) return 0;
        int 끝 = 상가[INDEKS] + konstant_SEKUND_VÆRDI[INDEKS], tal = 상가[INDEKS], varighed_VÆRDI = 0;
        while (tal < 끝 && !fejl) {
            int VÆRDI = Fil[tal++];
            if (VÆRDI == 0) fejl_VÆRDI("invalid modified UTF-8");
            else if (VÆRDI >= 192 && VÆRDI <= 223 && tal < 끝) {
                int Næste_vare = Fil[tal++];
                if ((Næste_vare & 192) != 128) fejl_VÆRDI("invalid modified UTF-8");
                VÆRDI = (VÆRDI & 31) << 6 | Næste_vare & 63;
                if (VÆRDI != 0 && VÆRDI < 128) fejl_VÆRDI("overlong modified UTF-8");
            } else if (VÆRDI >= 224 && VÆRDI <= 239 && tal + 1 < 끝) {
                int 가 = Fil[tal++], SEKUND_operand = Fil[tal++];
                if ((가 & 192) != 128 || (SEKUND_operand & 192) != 128) fejl_VÆRDI("invalid modified UTF-8");
                VÆRDI = (VÆRDI & 15) << 12 | (가 & 63) << 6 | SEKUND_operand & 63;
                if (VÆRDI < 2048) fejl_VÆRDI("overlong modified UTF-8");
            } else if (VÆRDI >= 128) fejl_VÆRDI("invalid modified UTF-8");
            heap_VÆRDI[referere + 2 + varighed_VÆRDI++] = VÆRDI;
        }
        heap_VÆRDI[referere + 1] = varighed_VÆRDI; streng_referere[INDEKS] = referere; return referere;
    }
    static int vært_tegn(String VÆRDI) {
        int referere = tildel_Lager(1, VÆRDI.length()); if (fejl) return 0;
        for (int tal = 0; tal < VÆRDI.length(); tal++) heap_VÆRDI[referere + 2 + tal] = VÆRDI.charAt(tal);
        return referere;
    }
    static void skrive_sms(int referere) {
        if (referere == 0) { bruger.Skrive("null"); return; }
        if (!objekt_VÆRDI(referere, 1)) return;
        for (int tal = 0; tal < heap_VÆRDI[referere + 1]; tal++) bruger.skrive_tegn_VÆRDI(heap_VÆRDI[referere + 2 + tal]);
    }
    static int ciffer_tegn(int VÆRDI) {
        int referere = tildel_Lager(1, 11); if (fejl) return 0;
        int varighed_VÆRDI = 0;
        if (VÆRDI < 0) heap_VÆRDI[referere + 2 + varighed_VÆRDI++] = '-'; else VÆRDI = -VÆRDI;
        int positionsindeks = 1000000000; boolean Kør_2 = false;
        while (positionsindeks != 0) {
            int tal = -(VÆRDI / positionsindeks);
            if (tal != 0 || Kør_2 || positionsindeks == 1) { heap_VÆRDI[referere + 2 + varighed_VÆRDI++] = '0' + tal; Kør_2 = true; }
            VÆRDI %= positionsindeks; positionsindeks /= 10;
        }
        heap_VÆRDI[referere + 1] = varighed_VÆRDI; return referere;
    }
    static int 정수해독(int referere) {
        if (!objekt_VÆRDI(referere, 1)) return 0;
        int varighed_VÆRDI = heap_VÆRDI[referere + 1], tal = 0, VÆRDI = 0; boolean 음수 = false;
        if (varighed_VÆRDI > 0 && (heap_VÆRDI[referere + 2] == '-' || heap_VÆRDI[referere + 2] == '+')) { 음수 = heap_VÆRDI[referere + 2] == '-'; tal++; }
        if (tal == varighed_VÆRDI) fejl_VÆRDI("NumberFormatException");
        for (; tal < varighed_VÆRDI && !fejl; tal++) {
            int ciffer_VÆRDI = heap_VÆRDI[referere + 2 + tal] - '0';
            if (ciffer_VÆRDI < 0 || ciffer_VÆRDI > 9 || VÆRDI < -214748364 || VÆRDI == -214748364 && ciffer_VÆRDI > (음수 ? 8 : 7)) fejl_VÆRDI("NumberFormatException");
            VÆRDI = VÆRDI * 10 - ciffer_VÆRDI;
        }
        return 음수 ? VÆRDI : -VÆRDI;
    }
    static void 넣기(int VÆRDI, int Type_VÆRDI) {
        if (fejl) return;
        if (ramme_INDEKS < 0 || ramme_Stak[ramme_INDEKS] >= metode_Stak[ramme_metode[ramme_INDEKS]]) { fejl_VÆRDI("operand stack overflow"); return; }
        int udvidelsesstik_post = ramme_INDEKS * 128 + ramme_Stak[ramme_INDEKS]++; operand_Stak_VÆRDI[udvidelsesstik_post] = VÆRDI; operand_Stak_Type[udvidelsesstik_post] = Type_VÆRDI;
    }
    static int 빼기(int Type_VÆRDI) {
        if (fejl) return 0;
        if (ramme_INDEKS < 0 || ramme_Stak[ramme_INDEKS] < 1) { fejl_VÆRDI("operand stack underflow"); return 0; }
        int udvidelsesstik_post = ramme_INDEKS * 128 + --ramme_Stak[ramme_INDEKS]; returnere_Type = operand_Stak_Type[udvidelsesstik_post];
        if (Type_VÆRDI != 0 && returnere_Type != Type_VÆRDI) fejl_VÆRDI("operand type mismatch");
        if (returnere_Type == 2) beskytte_VÆRDI(operand_Stak_VÆRDI[udvidelsesstik_post]);
        return operand_Stak_VÆRDI[udvidelsesstik_post];
    }
    static void 지역읽기(int INDEKS, int Type_VÆRDI) {
        if (INDEKS >= 함수지역[ramme_metode[ramme_INDEKS]] || INDEKS < 0 || lokal_Type[ramme_INDEKS * 128 + INDEKS] != Type_VÆRDI) { fejl_VÆRDI("invalid or uninitialized local"); return; }
        넣기(lokal_VÆRDI[ramme_INDEKS * 128 + INDEKS], Type_VÆRDI);
    }
    static void skrive_lokal(int INDEKS, int Type_VÆRDI) {
        if (INDEKS >= 함수지역[ramme_metode[ramme_INDEKS]] || INDEKS < 0) { fejl_VÆRDI("local index out of range"); return; }
        int VÆRDI = 빼기(Type_VÆRDI); lokal_VÆRDI[ramme_INDEKS * 128 + INDEKS] = VÆRDI; lokal_Type[ramme_INDEKS * 128 + INDEKS] = Type_VÆRDI;
    }
    static int 명바() {
        int Placering = ramme_placere[ramme_INDEKS];
        if (Placering < metode_START[ramme_metode[ramme_INDEKS]] || Placering >= metode_afslutte_et_opkald[ramme_metode[ramme_INDEKS]]) { fejl_VÆRDI("instruction pointer out of range"); return 0; }
        ramme_placere[ramme_INDEKS]++; return Fil[Placering];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void flytte_VÆRDI_83b651b8(int Placering) {
        int FUNKTION_VÆRDI = ramme_metode[ramme_INDEKS];
        if (Placering < metode_START[FUNKTION_VÆRDI] || Placering >= metode_afslutte_et_opkald[FUNKTION_VÆRDI] || grænse_VÆRDI[Placering] != FUNKTION_VÆRDI + 1) fejl_VÆRDI("invalid branch target");
        else ramme_placere[ramme_INDEKS] = Placering;
    }
    static void 호출(int FUNKTION_VÆRDI) {
        if (ramme_INDEKS % 32 == 31) { fejl_VÆRDI("call stack limit (32)"); return; }
        int Næste_vare = ramme_INDEKS + 1;
        for (int tal = 0; tal < 128; tal++) lokal_Type[Næste_vare * 128 + tal] = 0;
        for (int tal = metode_argument_TÆL[FUNKTION_VÆRDI] - 1; tal >= 0; tal--) {
            lokal_VÆRDI[Næste_vare * 128 + tal] = 빼기(metode_argument_Type[FUNKTION_VÆRDI * 16 + tal]); lokal_Type[Næste_vare * 128 + tal] = metode_argument_Type[FUNKTION_VÆRDI * 16 + tal];
        }
        if (fejl) return;
        ramme_INDEKS = Næste_vare; starte_ramme[ramme_INDEKS] = 0; ramme_metode[ramme_INDEKS] = FUNKTION_VÆRDI; ramme_placere[ramme_INDEKS] = metode_START[FUNKTION_VÆRDI]; ramme_Stak[ramme_INDEKS] = 0;
    }
    static void returnere_KR(int Type_VÆRDI) {
        if (Type_VÆRDI != metode_returnere[ramme_metode[ramme_INDEKS]]) { fejl_VÆRDI("return type mismatch"); return; }
        int VÆRDI = Type_VÆRDI == 0 ? 0 : 빼기(Type_VÆRDI);
        if (starte_ramme[ramme_INDEKS] != 0) Hold_Definition_status[starte_ramme[ramme_INDEKS] - 1] = 2;
        if (ramme_lås[ramme_INDEKS] != 0) { udgive_lås(ramme_lås[ramme_INDEKS]); ramme_lås[ramme_INDEKS] = 0; }
        ramme_INDEKS--; if (ramme_INDEKS >= aktuel_tråd * 32 && Type_VÆRDI != 0) 넣기(VÆRDI, Type_VÆRDI);
    }
    static int[] strøm_filnavn = new int[64];
    static void fil_strøm_KALD(int ejer_VÆRDI, int Navn, int format_VÆRDI, int Kommando) {
        boolean Udgang = Ord_sms(ejer_VÆRDI, "java/io/FileOutputStream");
        int 종류 = Udgang ? 6 : 5;
        if (Kommando == 183 && Ord_sms(Navn, "<init>")) {
            boolean 이어 = false;
            if (Udgang && Ord_sms(format_VÆRDI, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Ord_sms(format_VÆRDI, "(Ljava/lang/String;)V")) { fejl_VÆRDI("unsupported file stream constructor"); return; }
            int fil_post_navn = 빼기(2), strøm_VÆRDI = 빼기(2);
            if (!objekt_VÆRDI(fil_post_navn, 1) || !objekt_VÆRDI(strøm_VÆRDI, 종류) || fejl) return;
            if (heap_VÆRDI[strøm_VÆRDI + 3] != 0) { fejl_VÆRDI("file stream already initialized"); return; }
            int varighed_VÆRDI = heap_VÆRDI[fil_post_navn + 1];
            if (varighed_VÆRDI < 1 || varighed_VÆRDI > 63) { fejl_VÆRDI("invalid file name length"); return; }
            for (int udvidelsesstik_post = 0; udvidelsesstik_post < varighed_VÆRDI; udvidelsesstik_post++) {
                int VÆRDI = heap_VÆRDI[fil_post_navn + 2 + udvidelsesstik_post];
                if (VÆRDI < 1) { fejl_VÆRDI("invalid file stream path"); return; }
                strøm_filnavn[udvidelsesstik_post] = VÆRDI;
            }
            strøm_filnavn[varighed_VÆRDI] = 0;
            int 서술자 = bruger.파일서술자열기(strøm_filnavn, Udgang ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { fejl_VÆRDI("FileNotFoundException: file open failed"); return; }
            heap_VÆRDI[strøm_VÆRDI + 2] = 서술자; heap_VÆRDI[strøm_VÆRDI + 3] = 1;
            return;
        }
        if (Kommando != 182) { fejl_VÆRDI("invalid file stream invocation"); return; }
        if ((Udgang && Ord_sms(Navn, "write") || !Udgang && Ord_sms(Navn, "read"))
            && (Ord_sms(format_VÆRDI, Udgang ? "([B)V" : "([B)I") || Ord_sms(format_VÆRDI, Udgang ? "([BII)V" : "([BII)I"))) {
            boolean klippe_VÆRDI = Ord_sms(format_VÆRDI, Udgang ? "([BII)V" : "([BII)I");
            int post_TÆL_8f7753a1 = klippe_VÆRDI ? 빼기(1) : 0, 시작점 = klippe_VÆRDI ? 빼기(1) : 0, data_MATRIX = 빼기(2), objekt_referere = 빼기(2);
            if (!objekt_VÆRDI(data_MATRIX, 20) || !objekt_VÆRDI(objekt_referere, 종류)) return;
            if (!klippe_VÆRDI) post_TÆL_8f7753a1 = heap_VÆRDI[data_MATRIX + 1];
            if (시작점 < 0 || post_TÆL_8f7753a1 < 0 || 시작점 > heap_VÆRDI[data_MATRIX + 1] - post_TÆL_8f7753a1) { 예외던짐(6, "file buffer bounds"); return; }
            if (heap_VÆRDI[objekt_referere + 3] == 0 || heap_VÆRDI[objekt_referere + 2] < 0) { fejl_VÆRDI("IOException: stream closed"); return; }
            int fuldført_TÆL = 0;
            while (fuldført_TÆL < post_TÆL_8f7753a1 && !fejl) {
                int 반환값 = Udgang ? bruger.파일한바이트쓰기(heap_VÆRDI[objekt_referere + 2], heap_VÆRDI[data_MATRIX + 2 + 시작점 + fuldført_TÆL]) : bruger.파일한바이트읽기(heap_VÆRDI[objekt_referere + 2]);
                if (반환값 < 0) { fejl_VÆRDI(Udgang ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!Udgang && 반환값 == 256) break;
                if (!Udgang) heap_VÆRDI[data_MATRIX + 2 + 시작점 + fuldført_TÆL] = (byte)반환값;
                fuldført_TÆL++;
            }
            if (!Udgang) 넣기(post_TÆL_8f7753a1 != 0 && fuldført_TÆL == 0 ? -1 : fuldført_TÆL, 1);
            return;
        }
        if (Udgang && Ord_sms(Navn, "flush") && Ord_sms(format_VÆRDI, "()V")) { int objekt_referere = 빼기(2); if (objekt_VÆRDI(objekt_referere, 종류) && heap_VÆRDI[objekt_referere + 2] < 0) fejl_VÆRDI("IOException: stream closed"); return; }
        int Handling = -1, VÆRDI = 0;
        if (Ord_sms(Navn, "close") && Ord_sms(format_VÆRDI, "()V")) Handling = 0;
        if (!Udgang && Ord_sms(Navn, "read") && Ord_sms(format_VÆRDI, "()I")) Handling = 1;
        if (Udgang && Ord_sms(Navn, "write") && Ord_sms(format_VÆRDI, "(I)V")) { Handling = 2; VÆRDI = 빼기(1); }
        if (Handling < 0) { fejl_VÆRDI("unsupported file stream method"); return; }
        int strøm_VÆRDI = 빼기(2);
        if (!objekt_VÆRDI(strøm_VÆRDI, 종류) || fejl) return;
        if (heap_VÆRDI[strøm_VÆRDI + 3] == 0) { fejl_VÆRDI("uninitialized file stream"); return; }
        int 서술자 = heap_VÆRDI[strøm_VÆRDI + 2];
        if (Handling == 0) {
            if (서술자 >= 0 && bruger.파일서술자닫기(서술자) < 0) fejl_VÆRDI("IOException: close failed");
            heap_VÆRDI[strøm_VÆRDI + 2] = -1; return;
        }
        if (서술자 < 0) { fejl_VÆRDI("IOException: stream closed"); return; }
        if (Handling == 1) {
            int KR = bruger.파일한바이트읽기(서술자);
            if (KR < -1) fejl_VÆRDI("IOException: read failed"); else 넣기(KR == 256 ? -1 : KR, 1);
        } else if (bruger.파일한바이트쓰기(서술자, VÆRDI) != 1) fejl_VÆRDI("IOException: write failed");
    }
    static void KALD_metode(int INDEKS, int Kommando) {
        if (INDEKS <= 0 || INDEKS >= konstant_tag.length || (konstant_tag[INDEKS] != 10 && konstant_tag[INDEKS] != 11)) { fejl_VÆRDI("invalid method reference"); return; }
        int ejer_VÆRDI = klassenavn_sms(상가[INDEKS]), Navn = referere_navn(konstant_SEKUND_VÆRDI[INDEKS]), format_VÆRDI = referencetype(konstant_SEKUND_VÆRDI[INDEKS]);
        if (fejl) return;
        if (기본호출(ejer_VÆRDI, Navn, format_VÆRDI, Kommando)) return;
        if (Ord_sms(ejer_VÆRDI, "java/io/FileInputStream") || Ord_sms(ejer_VÆRDI, "java/io/FileOutputStream")) {
            fil_strøm_KALD(ejer_VÆRDI, Navn, format_VÆRDI, Kommando); return;
        }
        if (Kommando == 184 && Ord_sms(ejer_VÆRDI, "java/lang/Integer") && Ord_sms(Navn, "parseInt") && Ord_sms(format_VÆRDI, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (Kommando == 182 && Ord_sms(ejer_VÆRDI, "java/io/PrintStream") && (Ord_sms(Navn, "println") || Ord_sms(Navn, "print"))) {
            int Type_VÆRDI = 0, VÆRDI = 0;
            if (Ord_sms(format_VÆRDI, "(I)V")) { Type_VÆRDI = 1; VÆRDI = 빼기(1); }
            else if (Ord_sms(format_VÆRDI, "(Z)V")) { Type_VÆRDI = 2; VÆRDI = 빼기(1); }
            else if (Ord_sms(format_VÆRDI, "(C)V")) { Type_VÆRDI = 3; VÆRDI = 빼기(1); }
            else if (Ord_sms(format_VÆRDI, "(Ljava/lang/String;)V")) { Type_VÆRDI = 4; VÆRDI = 빼기(2); }
            else if (!Ord_sms(format_VÆRDI, "()V") || !Ord_sms(Navn, "println")) fejl_VÆRDI("unsupported print descriptor");
            if (빼기(2) != -1) fejl_VÆRDI("invalid PrintStream receiver");
            if (fejl) return;
            if (Type_VÆRDI == 1) 자바도구.skrive_tal(VÆRDI);
            if (Type_VÆRDI == 2) bruger.Skrive(VÆRDI == 0 ? "false" : "true");
            if (Type_VÆRDI == 3) bruger.skrive_tegn_VÆRDI(VÆRDI & 65535);
            if (Type_VÆRDI == 4) skrive_sms(VÆRDI);
            if (Ord_sms(Navn, "println")) bruger.skrive_tegn_VÆRDI(10);
            return;
        }
        if (Kommando == 182 && Ord_sms(ejer_VÆRDI, "java/lang/String")) {
            if (Ord_sms(Navn, "length") && Ord_sms(format_VÆRDI, "()I")) {
                int referere = 빼기(2); if (objekt_VÆRDI(referere, 1)) 넣기(heap_VÆRDI[referere + 1], 1); return;
            }
            if (Ord_sms(Navn, "charAt") && Ord_sms(format_VÆRDI, "(I)C")) {
                int sænket_skrift_VÆRDI = 빼기(1), referere = 빼기(2);
                if (objekt_VÆRDI(referere, 1)) {
                    if (sænket_skrift_VÆRDI < 0 || sænket_skrift_VÆRDI >= heap_VÆRDI[referere + 1]) fejl_VÆRDI("StringIndexOutOfBoundsException"); else 넣기(heap_VÆRDI[referere + 2 + sænket_skrift_VÆRDI], 1);
                }
                return;
            }
        }
        if (Ord_sms(ejer_VÆRDI, "java/lang/StringBuilder")) {
            if (Kommando == 183 && Ord_sms(Navn, "<init>") && Ord_sms(format_VÆRDI, "()V")) { objekt_VÆRDI(빼기(2), 4); return; }
            if (Kommando == 182 && Ord_sms(Navn, "toString") && Ord_sms(format_VÆRDI, "()Ljava/lang/String;")) {
                int referere = 빼기(2); if (objekt_VÆRDI(referere, 4)) 넣기(heap_VÆRDI[referere + 2] == 0 ? vært_tegn("") : heap_VÆRDI[referere + 2], 2); return;
            }
            if (Kommando == 182 && Ord_sms(Navn, "append")) {
                int Tekst = 0;
                if (Ord_sms(format_VÆRDI, "(I)Ljava/lang/StringBuilder;")) Tekst = ciffer_tegn(빼기(1));
                else if (Ord_sms(format_VÆRDI, "(Z)Ljava/lang/StringBuilder;")) Tekst = vært_tegn(빼기(1) == 0 ? "false" : "true");
                else if (Ord_sms(format_VÆRDI, "(C)Ljava/lang/StringBuilder;")) {
                    int VÆRDI = 빼기(1); Tekst = tildel_Lager(1, 1); if (!fejl) heap_VÆRDI[Tekst + 2] = VÆRDI & 65535;
                }
                else if (Ord_sms(format_VÆRDI, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { Tekst = 빼기(2); if (Tekst == 0) Tekst = vært_tegn("null"); }
                else { fejl_VÆRDI("unsupported StringBuilder append"); return; }
                int referere = 빼기(2); if (!objekt_VÆRDI(referere, 4) || !objekt_VÆRDI(Tekst, 1)) return;
                int frontvendt_VÆRDI = heap_VÆRDI[referere + 2], frontvendt_VÆRDI_varighed = frontvendt_VÆRDI == 0 ? 0 : heap_VÆRDI[frontvendt_VÆRDI + 1], BACK_VÆRDI_varighed = heap_VÆRDI[Tekst + 1];
                int 새글 = tildel_Lager(1, frontvendt_VÆRDI_varighed + BACK_VÆRDI_varighed); if (fejl) return;
                for (int tal = 0; tal < frontvendt_VÆRDI_varighed; tal++) heap_VÆRDI[새글 + 2 + tal] = heap_VÆRDI[frontvendt_VÆRDI + 2 + tal];
                for (int tal = 0; tal < BACK_VÆRDI_varighed; tal++) heap_VÆRDI[새글 + 2 + frontvendt_VÆRDI_varighed + tal] = heap_VÆRDI[Tekst + 2 + tal];
                heap_VÆRDI[referere + 2] = 새글; 넣기(referere, 2); return;
            }
        }
        int Hold_Definition = Søg_Hold_Definition(ejer_VÆRDI); if (Hold_Definition < 0 || fejl) return;
        int fil_INDEKS = Søg_metode(Hold_Definition, Navn, format_VÆRDI);
        if (fil_INDEKS < 0) {
            for (int tegnkode = Hold_Definition, post_TÆL_8f7753a1 = 0; tegnkode >= 0 && post_TÆL_8f7753a1 < 16; post_TÆL_8f7753a1++, tegnkode = overordnet_Hold(tegnkode))
                if (Ord_sms(Hold_Definition_overordnet[tegnkode], "java/lang/Thread")) { 가닥호출(Navn, format_VÆRDI, Kommando); return; }
            fejl_VÆRDI("NoSuchMethodError"); return;
        }
        if (((metode_åbne[fil_INDEKS] & 8) != 0) != (Kommando == 184)) { fejl_VÆRDI("method static/instance mismatch"); return; }
        if (Kommando == 184) { if (!starte(metode_ejer[fil_INDEKS], 틀명령[ramme_INDEKS])) return; }
        else {
            int 읽는자리 = ramme_Stak[ramme_INDEKS] - metode_argument_TÆL[fil_INDEKS];
            if (읽는자리 < 0 || operand_Stak_Type[ramme_INDEKS * 128 + 읽는자리] != 2) { fejl_VÆRDI("invalid method receiver"); return; }
            int objekt_referere = operand_Stak_VÆRDI[ramme_INDEKS * 128 + 읽는자리];
            if (!it_gyldig_objekt(objekt_referere)) return;
            if (heap_VÆRDI[objekt_referere] < 32 || !종포함(heap_VÆRDI[objekt_referere] - 32, ejer_VÆRDI)) { fejl_VÆRDI("method receiver type mismatch"); return; }
            if (Kommando != 183) fil_INDEKS = Søg_metode(heap_VÆRDI[objekt_referere] - 32, Navn, format_VÆRDI);
        }
        if (fil_INDEKS < 0 || (metode_åbne[fil_INDEKS] & 0x400) != 0) { fejl_VÆRDI("AbstractMethodError"); return; }
        int lås_referere = 0;
        if ((metode_åbne[fil_INDEKS] & 32) != 0) {
            if (Kommando == 184) { int tegnkode = metode_ejer[fil_INDEKS]; if (Hold_lås[tegnkode] == 0) Hold_lås[tegnkode] = tildel_Lager(8, 0); lås_referere = Hold_lås[tegnkode]; }
            else lås_referere = operand_Stak_VÆRDI[ramme_INDEKS * 128 + ramme_Stak[ramme_INDEKS] - metode_argument_TÆL[fil_INDEKS]];
            if (!잠금얻기(lås_referere)) { if (!fejl) ramme_placere[ramme_INDEKS] = 틀명령[ramme_INDEKS]; return; }
        }
        호출(fil_INDEKS); if (!fejl) ramme_lås[ramme_INDEKS] = lås_referere;
    }
    static boolean 배열저장가능(int MATRIX_referere, int data_VÆRDI) {
        if (data_VÆRDI == 0 || matrixelement[MATRIX_referere] == 0) return true;
        boolean 성공여부 = matrixelement[MATRIX_referere] == -1 ? (data_VÆRDI > 0 && data_VÆRDI < heap_afslutte_et_opkald_placere && heap_VÆRDI[data_VÆRDI] == 1) : afstemning_objekt(data_VÆRDI, matrixelement[MATRIX_referere]);
        if (!성공여부 && !fejl) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int MATRIX_udvidelsesstik(int referere, int sænket_skrift_VÆRDI, int Type_VÆRDI) {
        if (!objekt_VÆRDI(referere, Type_VÆRDI)) return 0;
        if (sænket_skrift_VÆRDI < 0 || sænket_skrift_VÆRDI >= heap_VÆRDI[referere + 1]) { fejl_VÆRDI("ArrayIndexOutOfBoundsException"); return 0; }
        return referere + 2 + sænket_skrift_VÆRDI;
    }
    static void Udfør_kommando() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (fejl) { if (던진객체 != 0) handle_undtagelse(); if (fejl || ramme_INDEKS < aktuel_tråd * 32) break; }
            if (ramme_INDEKS < aktuel_tråd * 32 || ændringsanmodning || --조각 == 0) { if (!SKIFT_tråd()) break; 조각 = 100; }
            if (ramme_INDEKS == 0 && Hold_Definition_status[post_Hold_Definition] != 2 && !starte(post_Hold_Definition, ramme_placere[ramme_INDEKS])) continue;
            if (ramme_INDEKS == aktuel_tråd * 32 && aktuel_tråd != 0 && (metode_åbne[ramme_metode[ramme_INDEKS]] & 32) != 0 && ramme_lås[ramme_INDEKS] == 0) {
                int objekt_referere = tråd_mål[aktuel_tråd]; if (!잠금얻기(objekt_referere)) { if (fejl) break; continue; } ramme_lås[ramme_INDEKS] = objekt_referere;
            }
            잠시수 = 0;
            if (--남음 == 0) { fejl_VÆRDI("instruction limit (500000)"); break; }
            int Kør_2 = ramme_placere[ramme_INDEKS]; 틀명령[ramme_INDEKS] = Kør_2; int VÆRDI = 명바();
            if (fejl) break;
            if (VÆRDI == 0) continue;
            if (VÆRDI == 1) { 넣기(0, 2); continue; }
            if (VÆRDI >= 2 && VÆRDI <= 8) { 넣기(VÆRDI - 3, 1); continue; }
            if (VÆRDI == 16) { 넣기((byte)명바(), 1); continue; }
            if (VÆRDI == 17) { 넣기((short)명짧(), 1); continue; }
            if (VÆRDI == 18 || VÆRDI == 19) {
                int tal = metode_ejer[ramme_metode[ramme_INDEKS]] * 512 + (VÆRDI == 18 ? 명바() : 명짧());
                if (tal <= 0 || tal >= konstant_tag.length) fejl_VÆRDI("invalid ldc constant");
                else if (konstant_tag[tal] == 3) 넣기(상가[tal], 1);
                else if (konstant_tag[tal] == 8) 넣기(konstant_sms(상가[tal]), 2);
                else fejl_VÆRDI("unsupported ldc constant");
                continue;
            }
            if (VÆRDI == 21 || VÆRDI == 25) { 지역읽기(명바(), VÆRDI == 21 ? 1 : 2); continue; }
            if (VÆRDI >= 26 && VÆRDI <= 29) { 지역읽기(VÆRDI - 26, 1); continue; }
            if (VÆRDI >= 42 && VÆRDI <= 45) { 지역읽기(VÆRDI - 42, 2); continue; }
            if (VÆRDI == 54 || VÆRDI == 58) { skrive_lokal(명바(), VÆRDI == 54 ? 1 : 2); continue; }
            if (VÆRDI >= 59 && VÆRDI <= 62) { skrive_lokal(VÆRDI - 59, 1); continue; }
            if (VÆRDI >= 75 && VÆRDI <= 78) { skrive_lokal(VÆRDI - 75, 2); continue; }
            if (VÆRDI == 46 || VÆRDI >= 50 && VÆRDI <= 53) {
                int post_placere_206f1c6d = 빼기(1), objekt_referere = 빼기(2), område_KODE = VÆRDI == 46 ? 2 : VÆRDI == 50 ? 3 : VÆRDI == 51 ? 20 : VÆRDI == 52 ? 22 : 23;
                if (VÆRDI == 51 && objekt_referere > 0 && objekt_referere < heap_afslutte_et_opkald_placere && heap_VÆRDI[objekt_referere] == 21) område_KODE = 21;
                int 읽는자리 = MATRIX_udvidelsesstik(objekt_referere, post_placere_206f1c6d, område_KODE); if (!fejl) 넣기(heap_VÆRDI[읽는자리], VÆRDI == 50 ? 2 : 1); continue;
            }
            if (VÆRDI == 79 || VÆRDI >= 83 && VÆRDI <= 86) {
                int post_referere = 빼기(VÆRDI == 83 ? 2 : 1), post_placere_206f1c6d = 빼기(1), objekt_referere = 빼기(2), område_KODE = VÆRDI == 79 ? 2 : VÆRDI == 83 ? 3 : VÆRDI == 84 ? 20 : VÆRDI == 85 ? 22 : 23;
                if (VÆRDI == 84 && objekt_referere > 0 && objekt_referere < heap_afslutte_et_opkald_placere && heap_VÆRDI[objekt_referere] == 21) område_KODE = 21;
                int 읽는자리 = MATRIX_udvidelsesstik(objekt_referere, post_placere_206f1c6d, område_KODE);
                if (!fejl && område_KODE == 3 && !배열저장가능(objekt_referere, post_referere)) continue;
                if (!fejl) heap_VÆRDI[읽는자리] = område_KODE == 20 ? (byte)post_referere : område_KODE == 21 ? post_referere & 1 : område_KODE == 22 ? (char)post_referere : område_KODE == 23 ? (short)post_referere : post_referere;
                continue;
            }
            if (VÆRDI >= 87 && VÆRDI <= 95) { 스택명령(VÆRDI); continue; }
            if (VÆRDI == 96 || VÆRDI == 100 || VÆRDI == 104 || VÆRDI == 108 || VÆRDI == 112 || VÆRDI == 120
                || VÆRDI == 122 || VÆRDI == 124 || VÆRDI == 126 || VÆRDI == 128 || VÆRDI == 130) {
                int SEKUND_operand = 빼기(1), 가 = 빼기(1), KR = 0;
                if ((VÆRDI == 108 || VÆRDI == 112) && SEKUND_operand == 0) { fejl_VÆRDI("ArithmeticException: / by zero"); continue; }
                if (VÆRDI == 96) KR = 가 + SEKUND_operand;
                if (VÆRDI == 100) KR = 가 - SEKUND_operand;
                if (VÆRDI == 104) KR = 가 * SEKUND_operand;
                if (VÆRDI == 108) KR = 가 / SEKUND_operand;
                if (VÆRDI == 112) KR = 가 % SEKUND_operand;
                if (VÆRDI == 120) KR = 가 << SEKUND_operand;
                if (VÆRDI == 122) KR = 가 >> SEKUND_operand;
                if (VÆRDI == 124) KR = 가 >>> SEKUND_operand;
                if (VÆRDI == 126) KR = 가 & SEKUND_operand;
                if (VÆRDI == 128) KR = 가 | SEKUND_operand;
                if (VÆRDI == 130) KR = 가 ^ SEKUND_operand;
                넣기(KR, 1); continue;
            }
            if (VÆRDI == 116) { 넣기(-빼기(1), 1); continue; }
            if (VÆRDI == 132) {
                int lokal_Omfang = 명바(), gradvis_forøgelse_trin = (byte)명바(); 지역읽기(lokal_Omfang, 1); 넣기(빼기(1) + gradvis_forøgelse_trin, 1); skrive_lokal(lokal_Omfang, 1); continue;
            }
            if (VÆRDI >= 145 && VÆRDI <= 147) {
                int tal = 빼기(1); 넣기(VÆRDI == 145 ? (byte)tal : VÆRDI == 146 ? (char)tal : (short)tal, 1); continue;
            }
            if (VÆRDI >= 153 && VÆRDI <= 167 || VÆRDI == 198 || VÆRDI == 199) {
                int destination_VÆRDI = Kør_2 + (short)명짧(); boolean 갈까 = VÆRDI == 167;
                if (VÆRDI >= 153 && VÆRDI <= 158) {
                    int tal = 빼기(1); 갈까 = VÆRDI == 153 ? tal == 0 : VÆRDI == 154 ? tal != 0 : VÆRDI == 155 ? tal < 0 : VÆRDI == 156 ? tal >= 0 : VÆRDI == 157 ? tal > 0 : tal <= 0;
                } else if (VÆRDI >= 159 && VÆRDI <= 166) {
                    int SEKUND_operand = 빼기(VÆRDI >= 165 ? 2 : 1), 가 = 빼기(VÆRDI >= 165 ? 2 : 1);
                    갈까 = VÆRDI == 159 || VÆRDI == 165 ? 가 == SEKUND_operand : VÆRDI == 160 || VÆRDI == 166 ? 가 != SEKUND_operand : VÆRDI == 161 ? 가 < SEKUND_operand : VÆRDI == 162 ? 가 >= SEKUND_operand : VÆRDI == 163 ? 가 > SEKUND_operand : 가 <= SEKUND_operand;
                } else if (VÆRDI == 198 || VÆRDI == 199) { int tal = 빼기(2); 갈까 = VÆRDI == 198 ? tal == 0 : tal != 0; }
                if (갈까) flytte_VÆRDI_83b651b8(destination_VÆRDI); continue;
            }
            if (VÆRDI == 172 || VÆRDI == 176 || VÆRDI == 177) { returnere_KR(VÆRDI == 172 ? 1 : VÆRDI == 176 ? 2 : 0); continue; }
            if (VÆRDI >= 178 && VÆRDI <= 181) { 필드호출(명상수(), VÆRDI, Kør_2); continue; }
            if (VÆRDI >= 182 && VÆRDI <= 185) {
                int 부호값 = 명상수();
                if (VÆRDI == 185) { int i_alt_TÆL = 명바(); if (i_alt_TÆL == 0 || 명바() != 0) { fejl_VÆRDI("invalid invokeinterface operands"); continue; } }
                KALD_metode(부호값, VÆRDI); continue;
            }
            if (VÆRDI == 187) { 새객체(klassenavn_sms(명상수()), Kør_2); continue; }
            if (VÆRDI == 188 || VÆRDI == 189) {
                int område_KODE = 3, komponent = 0;
                if (VÆRDI == 188) { int 임시값 = 명바(); område_KODE = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else komponent = klassenavn_sms(명상수());
                if (område_KODE == 0) { fejl_VÆRDI("unsupported primitive array type"); continue; }
                int gyldig_varighed = 빼기(1), objekt_referere = tildel_Lager(område_KODE, gyldig_varighed); if (!fejl) matrixelement[objekt_referere] = komponent; 넣기(objekt_referere, 2); continue;
            }
            if (VÆRDI == 190) {
                int objekt_referere = 빼기(2);
                if (it_gyldig_objekt(objekt_referere)) { int Sammenligning_placere = heap_VÆRDI[objekt_referere]; if (Sammenligning_placere != 2 && Sammenligning_placere != 3 && (Sammenligning_placere < 20 || Sammenligning_placere > 23)) fejl_VÆRDI("not an array"); else 넣기(heap_VÆRDI[objekt_referere + 1], 1); }
                continue;
            }
            if (VÆRDI == 191) {
                int objekt_referere = 빼기(2); if (it_gyldig_objekt(objekt_referere)) { if (heap_VÆRDI[objekt_referere] != 9) fejl_VÆRDI("athrow requires supported Throwable"); else { 던진객체 = objekt_referere; fejl = true; } }
                continue;
            }
            if (VÆRDI == 192 || VÆRDI == 193) {
                int navn_konstant = klassenavn_sms(명상수()), objekt_referere = 빼기(2); boolean SAMMENLIGN = afstemning_objekt(objekt_referere, navn_konstant);
                if (VÆRDI == 193) 넣기(objekt_referere != 0 && SAMMENLIGN ? 1 : 0, 1);
                else { if (!SAMMENLIGN && !fejl) fejl_VÆRDI("ClassCastException"); 넣기(objekt_referere, 2); }
                continue;
            }
            if (VÆRDI == 170 || VÆRDI == 171) {
                int 읽는자리 = Kør_2 + 1, fil_INDEKS = ramme_metode[ramme_INDEKS], tast_referere = 빼기(1);
                while ((읽는자리 - metode_START[fil_INDEKS]) % 4 != 0) 읽는자리++;
                int mål_mail = placere_heltal(읽는자리);
                if (VÆRDI == 170) { int 낮은값 = placere_heltal(읽는자리 + 4), 높은값 = placere_heltal(읽는자리 + 8); if (tast_referere >= 낮은값 && tast_referere <= 높은값) mål_mail = placere_heltal(읽는자리 + 12 + (tast_referere - 낮은값) * 4); }
                else { int i_alt_TÆL = placere_heltal(읽는자리 + 4); for (int Loop_INDEKS = 0; Loop_INDEKS < i_alt_TÆL; Loop_INDEKS++) if (placere_heltal(읽는자리 + 8 + Loop_INDEKS * 8) == tast_referere) mål_mail = placere_heltal(읽는자리 + 12 + Loop_INDEKS * 8); }
                flytte_VÆRDI_83b651b8(Kør_2 + mål_mail); continue;
            }
            if (VÆRDI == 200) { flytte_VÆRDI_83b651b8(Kør_2 + placere_heltal(Kør_2 + 1)); continue; }
            if (VÆRDI == 194 || VÆRDI == 195) {
                int objekt_referere = 빼기(2);
                if (VÆRDI == 195) udgive_lås(objekt_referere);
                else if (!잠금얻기(objekt_referere) && !fejl) { 넣기(objekt_referere, 2); ramme_placere[ramme_INDEKS] = Kør_2; }
                continue;
            }
            if (VÆRDI == 196) {
                int kommando_KODE = 명바(), post_placere_206f1c6d = 명짧();
                if (kommando_KODE == 21 || kommando_KODE == 25) 지역읽기(post_placere_206f1c6d, kommando_KODE == 21 ? 1 : 2);
                else if (kommando_KODE == 54 || kommando_KODE == 58) skrive_lokal(post_placere_206f1c6d, kommando_KODE == 54 ? 1 : 2);
                else if (kommando_KODE == 132) { int DELTA_VÆRDI = (short)명짧(); 지역읽기(post_placere_206f1c6d, 1); 넣기(빼기(1) + DELTA_VÆRDI, 1); skrive_lokal(post_placere_206f1c6d, 1); }
                else fejl_VÆRDI("unsupported wide opcode");
                continue;
            }
            fejl_VÆRDI("unsupported bytecode");
        }
    }
    static int Søg_Hold_Definition(int Navn) {
        for (int Loop_INDEKS = 0; Loop_INDEKS < Hold_Definition_TÆL; Loop_INDEKS++) if (Hold_Definition_navn[Loop_INDEKS] != 0 && afstemning_Ord(Hold_Definition_navn[Loop_INDEKS], Navn)) return Loop_INDEKS;
        return indlæse_Hold_Definition(konstant_sms(Navn));
    }
    static int indlæse_Hold_Definition(int navn_streng) {
        if (!objekt_VÆRDI(navn_streng, 1)) return -1;
        int varighed_VÆRDI = heap_VÆRDI[navn_streng + 1];
        if (varighed_VÆRDI < 1 || varighed_VÆRDI > 505 || Hold_Definition_TÆL == 16) { fejl_VÆRDI("class name/count limit"); return -1; }
        for (int Loop_INDEKS = 0; Loop_INDEKS < varighed_VÆRDI; Loop_INDEKS++) { int tegnkode = heap_VÆRDI[navn_streng + 2 + Loop_INDEKS]; filnavn_sms[Loop_INDEKS] = tegnkode == '/' ? '.' : tegnkode; }
        filnavn_sms[varighed_VÆRDI] = '.'; filnavn_sms[varighed_VÆRDI + 1] = 'c'; filnavn_sms[varighed_VÆRDI + 2] = 'l'; filnavn_sms[varighed_VÆRDI + 3] = 'a'; filnavn_sms[varighed_VÆRDI + 4] = 's'; filnavn_sms[varighed_VÆRDI + 5] = 's'; filnavn_sms[varighed_VÆRDI + 6] = 0;
        int Størrelse = bruger.파일읽기(filnavn_sms, midlertidig_fil);
        if (Størrelse < 0) { fejl_VÆRDI("ClassNotFoundException"); return -1; }
        int Hold_Definition = Hold_Definition_TÆL++; Hold_Definition_tilpasse_størrelse[Hold_Definition] = Størrelse;
        for (int Loop_INDEKS = 0; Loop_INDEKS < Størrelse; Loop_INDEKS++) Fil[Hold_Definition * 16384 + Loop_INDEKS] = midlertidig_fil[Loop_INDEKS];
        클래스읽기(Hold_Definition); if (fejl) return -1;
        int faktisk_data = konstant_sms(Hold_Definition_navn[Hold_Definition]);
        if (!글같음(faktisk_data, navn_streng, true)) { fejl_VÆRDI("class name does not match file"); return -1; }
        int overordnet_VÆRDI = Hold_Definition_overordnet[Hold_Definition];
        if (overordnet_VÆRDI != 0 && !Ord_sms(overordnet_VÆRDI, "java/lang/Object") && !Ord_sms(overordnet_VÆRDI, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 prøve_igen_VÆRDI 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = Søg_Hold_Definition(overordnet_VÆRDI);
            if (fejl || 위 < 0) return -1;
            int 읽는자리 = 위, fase_TÆL = 0;
            while (읽는자리 >= 0 && fase_TÆL++ < 16) {
                if (읽는자리 == Hold_Definition) { fejl_VÆRDI("cyclic inheritance"); return -1; }
                읽는자리 = overordnet_Hold(읽는자리);
            }
            int 시작변위 = Hold_udvidelsesstik_TÆL[위];
            for (int fil_INDEKS = 0; fil_INDEKS < udvidelsesstik_TÆL; fil_INDEKS++) if (udvidelsesstik_ejer[fil_INDEKS] == Hold_Definition && (udvidelsesstik_Tilladelser[fil_INDEKS] & 8) == 0) udvidelsesstik_placere[fil_INDEKS] += 시작변위;
            Hold_udvidelsesstik_TÆL[Hold_Definition] += 시작변위;
        }
        return Hold_Definition;
    }
    static int overordnet_Hold(int Hold_Definition) {
        int Navn = Hold_Definition_overordnet[Hold_Definition];
        for (int Loop_INDEKS = 0; Loop_INDEKS < Hold_Definition_TÆL; Loop_INDEKS++) if (Navn != 0 && Hold_Definition_navn[Loop_INDEKS] != 0 && afstemning_Ord(Hold_Definition_navn[Loop_INDEKS], Navn)) return Loop_INDEKS;
        return -1;
    }
    static int Søg_metode(int Hold_Definition, int Navn, int format_VÆRDI) {
        for (int 깊이 = 0; Hold_Definition >= 0 && 깊이 < 16; 깊이++, Hold_Definition = overordnet_Hold(Hold_Definition)) {
            for (int Loop_INDEKS = 0; Loop_INDEKS < metode_TÆL; Loop_INDEKS++) if (metode_ejer[Loop_INDEKS] == Hold_Definition && afstemning_Ord(metode_navn_sms[Loop_INDEKS], Navn) && afstemning_Ord(metode_Type[Loop_INDEKS], format_VÆRDI)) return Loop_INDEKS;
        }
        return -1;
    }
    static int navn_metode(int Hold_Definition, String Navn, String format_VÆRDI) {
        for (int 깊이 = 0; Hold_Definition >= 0 && 깊이 < 16; 깊이++, Hold_Definition = overordnet_Hold(Hold_Definition))
            for (int Loop_INDEKS = 0; Loop_INDEKS < metode_TÆL; Loop_INDEKS++) if (metode_ejer[Loop_INDEKS] == Hold_Definition && Ord_sms(metode_navn_sms[Loop_INDEKS], Navn) && Ord_sms(metode_Type[Loop_INDEKS], format_VÆRDI)) return Loop_INDEKS;
        return -1;
    }
    static int 형종류(int Navn) { return Fil[상가[Navn]] == 'L' || Fil[상가[Navn]] == '[' ? 2 : 1; }
    static boolean starte(int Hold_Definition, int kommando_START) {
        if (Hold_Definition < 0 || fejl) return false;
        if (Hold_Definition_status[Hold_Definition] == 3) { fejl_VÆRDI("NoClassDefFoundError: initialization failed"); return false; }
        if (Hold_Definition_status[Hold_Definition] == 1 && Hold_tråd[Hold_Definition] != aktuel_tråd) { ramme_placere[ramme_INDEKS] = kommando_START; ændringsanmodning = true; return false; }
        if (Hold_Definition_status[Hold_Definition] != 0) return true;
        int 위 = overordnet_Hold(Hold_Definition);
        if (위 >= 0 && !starte(위, kommando_START)) return false;
        Hold_Definition_status[Hold_Definition] = 1; Hold_tråd[Hold_Definition] = aktuel_tråd;
        if (starte_Hold_Definition[Hold_Definition] != 0) {
            ramme_placere[ramme_INDEKS] = kommando_START;
            호출(starte_Hold_Definition[Hold_Definition] - 1); if (!fejl) starte_ramme[ramme_INDEKS] = Hold_Definition + 1;
            return false;
        }
        Hold_Definition_status[Hold_Definition] = 2; return true;
    }
    static void 필드호출(int INDEKS, int Kommando, int Kør_2) {
        if (!check_konstant(INDEKS, 9)) return;
        int ejer_VÆRDI = klassenavn_sms(상가[INDEKS]), Navn = referere_navn(konstant_SEKUND_VÆRDI[INDEKS]), format_VÆRDI = referencetype(konstant_SEKUND_VÆRDI[INDEKS]);
        if (Ord_sms(ejer_VÆRDI, "java/lang/System") && (Ord_sms(Navn, "out") || Ord_sms(Navn, "err")) && Ord_sms(format_VÆRDI, "Ljava/io/PrintStream;") && Kommando == 178) { 넣기(-1, 2); return; }
        int Hold_Definition = Søg_Hold_Definition(ejer_VÆRDI); if (Hold_Definition < 0 || fejl) return;
        int 찾음 = -1;
        for (int 읽는자리 = Hold_Definition, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = overordnet_Hold(읽는자리))
            for (int fil_INDEKS = 0; fil_INDEKS < udvidelsesstik_TÆL; fil_INDEKS++) if (udvidelsesstik_ejer[fil_INDEKS] == 읽는자리 && afstemning_Ord(udvidelsesstik_navn[fil_INDEKS], Navn) && afstemning_Ord(udvidelsesstik_Type[fil_INDEKS], format_VÆRDI)) 찾음 = fil_INDEKS;
        if (찾음 < 0) { fejl_VÆRDI("NoSuchFieldError"); return; }
        boolean statisk_VÆRDI = Kommando == 178 || Kommando == 179;
        if (statisk_VÆRDI != ((udvidelsesstik_Tilladelser[찾음] & 8) != 0)) { fejl_VÆRDI("field static/instance mismatch"); return; }
        if (statisk_VÆRDI && !starte(udvidelsesstik_ejer[찾음], Kør_2)) return;
        int Type_VÆRDI = 형종류(format_VÆRDI), VÆRDI = 0;
        if (Kommando == 179 || Kommando == 181) VÆRDI = 빼기(Type_VÆRDI);
        if (statisk_VÆRDI) { if (Kommando == 178) 넣기(udvidelsesstik_data[찾음], Type_VÆRDI); else if (!fejl) udvidelsesstik_data[찾음] = VÆRDI; return; }
        int objekt_referere = 빼기(2);
        if (!it_gyldig_objekt(objekt_referere)) return;
        if (heap_VÆRDI[objekt_referere] < 32 || !종포함(heap_VÆRDI[objekt_referere] - 32, ejer_VÆRDI)) { fejl_VÆRDI("field receiver type mismatch"); return; }
        int 보관칸 = objekt_referere + 2 + udvidelsesstik_placere[찾음];
        if (Kommando == 180) 넣기(heap_VÆRDI[보관칸], Type_VÆRDI);
        else if (!fejl) { heap_VÆRDI[보관칸] = VÆRDI; heap_referere[보관칸] = Type_VÆRDI == 2 ? 1 : 0; }
    }
    static boolean 종포함(int Hold_Definition, int Navn) {
        for (int 중첩깊이 = 0; Hold_Definition >= 0 && 중첩깊이 < 16; 중첩깊이++, Hold_Definition = overordnet_Hold(Hold_Definition)) {
            if (afstemning_Ord(Hold_Definition_navn[Hold_Definition], Navn) || (Hold_Definition_overordnet[Hold_Definition] != 0 && afstemning_Ord(Hold_Definition_overordnet[Hold_Definition], Navn))) return true;
            for (int indre_placere = 0; indre_placere < Hold_grænseflade_TÆL[Hold_Definition]; indre_placere++) if (afstemning_Ord(Hold_grænseflade[Hold_Definition * 16 + indre_placere], Navn)) return true;
        }
        return false;
    }
    static boolean 글같음(int 첫값, int byte_data, boolean Sti) {
        if (첫값 == byte_data) return true;
        if (첫값 <= 0 || byte_data <= 0 || heap_VÆRDI[첫값] != 1 || heap_VÆRDI[byte_data] != 1 || heap_VÆRDI[첫값 + 1] != heap_VÆRDI[byte_data + 1]) return false;
        for (int Loop_INDEKS = 0; Loop_INDEKS < heap_VÆRDI[첫값 + 1]; Loop_INDEKS++) {
            int X_koordinat = heap_VÆRDI[첫값 + 2 + Loop_INDEKS], Y_koordinat = heap_VÆRDI[byte_data + 2 + Loop_INDEKS];
            if (Sti) { if (X_koordinat == '.') X_koordinat = '/'; if (Y_koordinat == '.') Y_koordinat = '/'; }
            if (X_koordinat != Y_koordinat) return false;
        }
        return true;
    }
    static boolean it_gyldig_objekt(int objekt_referere) {
        if (objekt_referere == 0) { fejl_VÆRDI("NullPointerException"); return false; }
        if (objekt_referere < 1 || objekt_referere >= heap_afslutte_et_opkald_placere || 힙폭[objekt_referere] < 2 || heap_VÆRDI[objekt_referere] == 0) { fejl_VÆRDI("invalid object reference"); return false; }
        return true;
    }
    static void beskytte_VÆRDI(int objekt_referere) {
        if (objekt_referere > 0 && objekt_referere < heap_afslutte_et_opkald_placere && 힙폭[objekt_referere] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = objekt_referere;
    }
    static void vise_VÆRDI(int objekt_referere) {
        if (objekt_referere > 0 && objekt_referere < heap_afslutte_et_opkald_placere && 힙폭[objekt_referere] >= 2 && heap_VÆRDI[objekt_referere] != 0 && 힙표시[objekt_referere] == 0) {
            힙표시[objekt_referere] = 1; 표시대기[vise_TÆL++] = objekt_referere;
        }
    }
    static void 수거() {
        vise_TÆL = 0; Samling_TÆL++;
        for (int check_placere = 1; check_placere < heap_afslutte_et_opkald_placere; check_placere += 힙폭[check_placere]) 힙표시[check_placere] = 0;
        for (int Loop_INDEKS = 0; Loop_INDEKS < streng_referere.length; Loop_INDEKS++) vise_VÆRDI(streng_referere[Loop_INDEKS]);
        for (int Loop_INDEKS = 0; Loop_INDEKS < udvidelsesstik_TÆL; Loop_INDEKS++) if ((udvidelsesstik_Tilladelser[Loop_INDEKS] & 8) != 0 && 형종류(udvidelsesstik_Type[Loop_INDEKS]) == 2) vise_VÆRDI(udvidelsesstik_data[Loop_INDEKS]);
        for (int 임시값 = 0; 임시값 < Antal_tråde; 임시값++) {
            vise_VÆRDI(tråd_objekt[임시값]); vise_VÆRDI(tråd_mål[임시값]);
            int 꼭대기자리 = 임시값 == aktuel_tråd ? ramme_INDEKS : tråd_ramme[임시값];
            for (int fil_INDEKS = 임시값 * 32; fil_INDEKS <= 꼭대기자리; fil_INDEKS++) {
                for (int indre_placere = 0; indre_placere < 함수지역[ramme_metode[fil_INDEKS]]; indre_placere++) if (lokal_Type[fil_INDEKS * 128 + indre_placere] == 2) vise_VÆRDI(lokal_VÆRDI[fil_INDEKS * 128 + indre_placere]);
                for (int indre_placere = 0; indre_placere < ramme_Stak[fil_INDEKS]; indre_placere++) if (operand_Stak_Type[fil_INDEKS * 128 + indre_placere] == 2) vise_VÆRDI(operand_Stak_VÆRDI[fil_INDEKS * 128 + indre_placere]);
            }
        }
        for (int Loop_INDEKS = 0; Loop_INDEKS < skærmbillede_referere.length; Loop_INDEKS++) vise_VÆRDI(skærmbillede_referere[Loop_INDEKS]);
        for (int Loop_INDEKS = 0; Loop_INDEKS < 나중수; Loop_INDEKS++) vise_VÆRDI(나중실행[Loop_INDEKS]);
        for (int Loop_INDEKS = 0; Loop_INDEKS < Store_heltal.length; Loop_INDEKS++) vise_VÆRDI(Store_heltal[Loop_INDEKS]);
        for (int Loop_INDEKS = 0; Loop_INDEKS < Hold_Definition_TÆL; Loop_INDEKS++) vise_VÆRDI(Hold_lås[Loop_INDEKS]);
        for (int check_placere = 1; check_placere < heap_afslutte_et_opkald_placere; check_placere += 힙폭[check_placere]) if (잠금깊이[check_placere] > 0) vise_VÆRDI(check_placere);
        vise_VÆRDI(던진객체);
        for (int Loop_INDEKS = 0; Loop_INDEKS < 잠시수; Loop_INDEKS++) vise_VÆRDI(잠시참조[Loop_INDEKS]);
        while (vise_TÆL > 0) {
            int objekt_referere = 표시대기[--vise_TÆL], område_KODE = heap_VÆRDI[objekt_referere];
            for (int Loop_INDEKS = objekt_referere + 2; Loop_INDEKS < objekt_referere + 힙폭[objekt_referere]; Loop_INDEKS++) if (område_KODE == 3 || område_KODE == 4 || heap_referere[Loop_INDEKS] != 0) vise_VÆRDI(heap_VÆRDI[Loop_INDEKS]);
        }
        for (int check_placere = 1; check_placere < heap_afslutte_et_opkald_placere; check_placere += 힙폭[check_placere]) if (힙표시[check_placere] == 0) heap_VÆRDI[check_placere] = 0;
        for (int check_placere = 1; check_placere < heap_afslutte_et_opkald_placere; check_placere += 힙폭[check_placere]) if (heap_VÆRDI[check_placere] == 0) {
            while (check_placere + 힙폭[check_placere] < heap_afslutte_et_opkald_placere && heap_VÆRDI[check_placere + 힙폭[check_placere]] == 0) { int Næste_placere = check_placere + 힙폭[check_placere]; 힙폭[check_placere] += 힙폭[Næste_placere]; 힙폭[Næste_placere] = 0; }
            if (check_placere + 힙폭[check_placere] == heap_afslutte_et_opkald_placere) { heap_afslutte_et_opkald_placere = check_placere; break; }
        }
    }
    static int 새기억(int 종류, int varighed_VÆRDI) {
        if (varighed_VÆRDI < 0) { fejl_VÆRDI("NegativeArraySizeException"); return 0; }
        if (varighed_VÆRDI > heap_VÆRDI.length - 3) { fejl_VÆRDI("object heap exhausted"); return 0; }
        int 필요수 = varighed_VÆRDI + 2, objekt_referere = 0;
        if (필요수 <= heap_VÆRDI.length - heap_afslutte_et_opkald_placere) { objekt_referere = heap_afslutte_et_opkald_placere; heap_afslutte_et_opkald_placere += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < heap_afslutte_et_opkald_placere; 읽는자리 += 힙폭[읽는자리]) if (heap_VÆRDI[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { objekt_referere = 읽는자리; break; }
            if (objekt_referere != 0) {
                int 남은길이 = 힙폭[objekt_referere] - 필요수;
                if (남은길이 >= 2) { 힙폭[objekt_referere + 필요수] = 남은길이; heap_VÆRDI[objekt_referere + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= heap_VÆRDI.length - heap_afslutte_et_opkald_placere) { objekt_referere = heap_afslutte_et_opkald_placere; heap_afslutte_et_opkald_placere += 필요수; }
        }
        if (objekt_referere == 0) { fejl_VÆRDI("object heap exhausted"); return 0; }
        for (int Loop_INDEKS = 0; Loop_INDEKS < 필요수; Loop_INDEKS++) { heap_VÆRDI[objekt_referere + Loop_INDEKS] = 0; heap_referere[objekt_referere + Loop_INDEKS] = 0; 힙폭[objekt_referere + Loop_INDEKS] = 0; }
        matrixelement[objekt_referere] = 0;
        힙폭[objekt_referere] = 필요수; heap_VÆRDI[objekt_referere] = 종류; heap_VÆRDI[objekt_referere + 1] = varighed_VÆRDI; beskytte_VÆRDI(objekt_referere); return objekt_referere;
    }
    static int undtagelse_Hold(String navn_konstant) {
        if (자바도구.같음(navn_konstant, "java/lang/Throwable")) return 1;
        if (자바도구.같음(navn_konstant, "java/lang/Exception")) return 2;
        if (자바도구.같음(navn_konstant, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(navn_konstant, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(navn_konstant, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(navn_konstant, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(navn_konstant, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(navn_konstant, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(navn_konstant, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(navn_konstant, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(navn_konstant, "java/io/IOException")) return 11;
        if (자바도구.같음(navn_konstant, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(navn_konstant, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(navn_konstant, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(navn_konstant, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int undtagelse_konstant(int Navn) {
        for (int Loop_INDEKS = 1; Loop_INDEKS <= 41; Loop_INDEKS++) if (Ord_sms(Navn, undtagelse_navn(Loop_INDEKS))) return Loop_INDEKS;
        return 0;
    }
    static String undtagelse_navn(int konto_VÆRDI) {
        if (konto_VÆRDI == 40) return "java/lang/InterruptedException";
        if (konto_VÆRDI == 41) return "Dansk/eget/대기중단예외";
        if (konto_VÆRDI == 39) return "java/net/SocketException";
        if (konto_VÆRDI == 20) return "Dansk/eget/undtagelse";
        if (konto_VÆRDI == 21) return "Dansk/eget/udførelse_undtagelse";
        if (konto_VÆRDI == 22) return "Dansk/eget/I_O_undtagelse";
        if (konto_VÆRDI == 23) return "Dansk/eget/vent_TIMEOUT_undtagelse";
        if (konto_VÆRDI == 24) return "Dansk/eget/mail_Opslag_undtagelse";
        if (konto_VÆRDI == 25) return "Dansk/eget/파일없음예외";
        if (konto_VÆRDI == 26) return "Dansk/eget/통신예외";
        if (konto_VÆRDI == 27) return "Dansk/eget/ugyldig_argument_undtagelse";
        if (konto_VÆRDI == 28) return "Dansk/eget/tal_format_fejl";
        if (konto_VÆRDI == 29) return "Dansk/eget/범위예외";
        if (konto_VÆRDI == 30) return "Dansk/eget/배열범위예외";
        if (konto_VÆRDI == 31) return "Dansk/eget/문자열범위예외";
        if (konto_VÆRDI == 32) return "Dansk/eget/NULL_referere_undtagelse";
        if (konto_VÆRDI == 33) return "Dansk/eget/산술예외";
        if (konto_VÆRDI == 34) return "Dansk/eget/status_undtagelse";
        if (konto_VÆRDI == 35) return "Dansk/eget/Type_Cast_undtagelse";
        if (konto_VÆRDI == 36) return "Dansk/eget/음수배열크기예외";
        if (konto_VÆRDI == 37) return "Dansk/eget/MATRIX_Store_fejl";
        if (konto_VÆRDI == 38) return "Dansk/eget/tråd_status_undtagelse";
        if (konto_VÆRDI == 1) return "java/lang/Throwable"; if (konto_VÆRDI == 2) return "java/lang/Exception";
        if (konto_VÆRDI == 3) return "java/lang/RuntimeException"; if (konto_VÆRDI == 4) return "java/lang/ArithmeticException";
        if (konto_VÆRDI == 5) return "java/lang/NullPointerException"; if (konto_VÆRDI == 6) return "java/lang/IndexOutOfBoundsException";
        if (konto_VÆRDI == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (konto_VÆRDI == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (konto_VÆRDI == 9) return "java/lang/IllegalArgumentException"; if (konto_VÆRDI == 10) return "java/lang/NumberFormatException";
        if (konto_VÆRDI == 11) return "java/io/IOException"; if (konto_VÆRDI == 12) return "java/io/FileNotFoundException";
        if (konto_VÆRDI == 17) return "java/lang/ArrayStoreException";
        if (konto_VÆRDI == 18) return "java/net/UnknownHostException";
        if (konto_VÆRDI == 19) return "java/net/SocketTimeoutException";
        if (konto_VÆRDI == 16) return "java/lang/IllegalThreadStateException";
        if (konto_VÆRDI == 13) return "java/lang/IllegalStateException"; if (konto_VÆRDI == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int undtagelse_overordnet(int konto_VÆRDI) {
        if (konto_VÆRDI == 40) return 2;
        if (konto_VÆRDI == 41) return 40;
        if (konto_VÆRDI == 39) return 11;
        if (konto_VÆRDI == 1) return 0;
        if (konto_VÆRDI == 2) return 1;
        if (konto_VÆRDI == 3) return 2;
        if (konto_VÆRDI == 4) return 3;
        if (konto_VÆRDI == 5) return 3;
        if (konto_VÆRDI == 6) return 3;
        if (konto_VÆRDI == 7) return 6;
        if (konto_VÆRDI == 8) return 6;
        if (konto_VÆRDI == 9) return 3;
        if (konto_VÆRDI == 10) return 9;
        if (konto_VÆRDI == 11) return 2;
        if (konto_VÆRDI == 12) return 11;
        if (konto_VÆRDI == 13) return 3;
        if (konto_VÆRDI == 14) return 3;
        if (konto_VÆRDI == 15) return 3;
        if (konto_VÆRDI == 16) return 9;
        if (konto_VÆRDI == 17) return 3;
        if (konto_VÆRDI == 18) return 11;
        if (konto_VÆRDI == 19) return 11;
        if (konto_VÆRDI == 20) return 2;
        if (konto_VÆRDI == 21) return 3;
        if (konto_VÆRDI == 22) return 11;
        if (konto_VÆRDI == 23) return 22;
        if (konto_VÆRDI == 24) return 22;
        if (konto_VÆRDI == 25) return 22;
        if (konto_VÆRDI == 26) return 22;
        if (konto_VÆRDI == 27) return 9;
        if (konto_VÆRDI == 28) return 27;
        if (konto_VÆRDI == 29) return 6;
        if (konto_VÆRDI == 30) return 29;
        if (konto_VÆRDI == 31) return 29;
        if (konto_VÆRDI == 32) return 5;
        if (konto_VÆRDI == 33) return 4;
        if (konto_VÆRDI == 34) return 13;
        if (konto_VÆRDI == 35) return 14;
        if (konto_VÆRDI == 36) return 15;
        if (konto_VÆRDI == 37) return 17;
        if (konto_VÆRDI == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int faktisk_værdi, int 요구값) {
        for (int 깊이 = 0; faktisk_værdi != 0 && 깊이 < 16; 깊이++, faktisk_værdi = undtagelse_overordnet(faktisk_værdi))
            if (faktisk_værdi == 요구값) return true;
        return false;
    }
    static void 예외던짐(int konto_VÆRDI, String Vigtigt_referere) {
        int objekt_referere = 새기억(9, 2); if (fejl) return;
        heap_VÆRDI[objekt_referere + 2] = konto_VÆRDI; heap_VÆRDI[objekt_referere + 3] = vært_tegn(Vigtigt_referere); heap_referere[objekt_referere + 3] = 1;
        던진객체 = objekt_referere; fejl = true;
    }
    static boolean afstemning_objekt(int objekt_referere, int Navn) {
        if (objekt_referere == 0) return true;
        if (!it_gyldig_objekt(objekt_referere)) return false;
        int område_KODE = heap_VÆRDI[objekt_referere];
        if (Ord_sms(Navn, "java/lang/Object")) return true;
        if (område_KODE >= 32) return 종포함(område_KODE - 32, Navn);
        if (område_KODE == 9) { int mål_mail = undtagelse_konstant(Navn); return mål_mail != 0 && 예외포함(heap_VÆRDI[objekt_referere + 2], mål_mail); }
        if (område_KODE == 1) return Ord_sms(Navn, "java/lang/String") || Ord_sms(Navn, "java/lang/CharSequence");
        if (område_KODE == 4) return Ord_sms(Navn, "java/lang/StringBuilder") || Ord_sms(Navn, "java/lang/CharSequence");
        if (område_KODE == 10) return Ord_sms(Navn, "java/util/ArrayList") || Ord_sms(Navn, "java/util/List");
        if (område_KODE == 11) return Ord_sms(Navn, "java/util/HashMap") || Ord_sms(Navn, "java/util/Map");
        if (område_KODE == 12) return Ord_sms(Navn, "java/lang/Integer") || Ord_sms(Navn, "java/lang/Number");
        if (område_KODE >= 24 && område_KODE <= 28 && heap_VÆRDI[objekt_referere + 13] != 0) return 한국어화면종(Navn) == område_KODE || Ord_sms(Navn, "Dansk/eget/skærmbillede_element");
        if (område_KODE >= 24 && område_KODE <= 28) return (한국어화면종(Navn) == 0 && skærmbillede_Hold(Navn) == område_KODE) || Ord_sms(Navn, "java/awt/Component") || Ord_sms(Navn, "java/awt/Container") || Ord_sms(Navn, "javax/swing/JComponent");
        if (område_KODE == 29) return Ord_sms(Navn, heap_VÆRDI[objekt_referere + 3] != 0 ? "Dansk/eget/동작알림" : "java/awt/event/ActionEvent");
        if (område_KODE == 30) return Ord_sms(Navn, "java/awt/FlowLayout") || Ord_sms(Navn, "java/awt/LayoutManager");
        if (område_KODE == 17) return Ord_sms(Navn, "java/net/Socket");
        if (område_KODE == 18) return Ord_sms(Navn, "java/net/ServerSocket");
        if (område_KODE == 19) return Ord_sms(Navn, heap_VÆRDI[objekt_referere + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (område_KODE == 14) return Ord_sms(Navn, "java/net/InetAddress");
        if (område_KODE == 15) return Ord_sms(Navn, "java/net/DatagramSocket");
        if (område_KODE == 16) return Ord_sms(Navn, "java/net/DatagramPacket");
        if (område_KODE == 13) return Ord_sms(Navn, heap_VÆRDI[objekt_referere + 3] != 0 ? "Dansk/eget/arbejder" : "java/lang/Thread");
        if (område_KODE == 2) return Ord_sms(Navn, "[I"); if (område_KODE == 20) return Ord_sms(Navn, "[B"); if (område_KODE == 21) return Ord_sms(Navn, "[Z");
        if (område_KODE == 22) return Ord_sms(Navn, "[C"); if (område_KODE == 23) return Ord_sms(Navn, "[S");
        if (område_KODE != 3) return false;
        if (Ord_sms(Navn, "[Ljava/lang/Object;")) return true;
        int komponent = matrixelement[objekt_referere];
        if (komponent == -1) return Ord_sms(Navn, "[Ljava/lang/String;") || Ord_sms(Navn, "[Ljava/lang/CharSequence;");
        if (komponent == 0) return false;
        if (배열종비교(komponent, Navn)) return true;
        if ((Ord_sms(komponent, "java/lang/String") || Ord_sms(komponent, "java/lang/StringBuilder")) && Ord_sms(Navn, "[Ljava/lang/CharSequence;")) return true;
        for (int Loop_INDEKS = 0; Loop_INDEKS < Hold_Definition_TÆL; Loop_INDEKS++) if (afstemning_Ord(Hold_Definition_navn[Loop_INDEKS], komponent)) {
            for (int tegnkode = Loop_INDEKS, 중첩깊이 = 0; tegnkode >= 0 && 중첩깊이 < 16; 중첩깊이++, tegnkode = overordnet_Hold(tegnkode)) {
                if (배열종비교(Hold_Definition_overordnet[tegnkode], Navn)) return true;
                for (int indre_placere = 0; indre_placere < Hold_grænseflade_TÆL[tegnkode]; indre_placere++) if (배열종비교(Hold_grænseflade[tegnkode * 16 + indre_placere], Navn)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int navn_konstant, int 형식참조) {
        int check_placere = 상가[형식참조], post_TÆL_8f7753a1 = konstant_SEKUND_VÆRDI[형식참조];
        if (navn_konstant == 0 || post_TÆL_8f7753a1 < 4 || Fil[check_placere] != '[' || Fil[check_placere + 1] != 'L' || Fil[check_placere + post_TÆL_8f7753a1 - 1] != ';' || konstant_SEKUND_VÆRDI[navn_konstant] != post_TÆL_8f7753a1 - 3) return false;
        for (int Loop_INDEKS = 0; Loop_INDEKS < post_TÆL_8f7753a1 - 3; Loop_INDEKS++) if (Fil[상가[navn_konstant] + Loop_INDEKS] != Fil[check_placere + 2 + Loop_INDEKS]) return false;
        return true;
    }
    static void handle_undtagelse() {
        if (던진객체 == 0) return;
        fejl = false;
        while (ramme_INDEKS >= aktuel_tråd * 32) {
            int fil_INDEKS = ramme_metode[ramme_INDEKS], 읽는자리 = 틀명령[ramme_INDEKS];
            for (int Loop_INDEKS = 0; Loop_INDEKS < 잡기수; Loop_INDEKS++) if (잡기함수[Loop_INDEKS] == fil_INDEKS && 읽는자리 >= 잡기시작[Loop_INDEKS] && 읽는자리 < 잡기끝[Loop_INDEKS]
                && (잡기종[Loop_INDEKS] == 0 || afstemning_objekt(던진객체, 잡기종[Loop_INDEKS]))) {
                ramme_placere[ramme_INDEKS] = 잡기위치[Loop_INDEKS]; ramme_Stak[ramme_INDEKS] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (starte_ramme[ramme_INDEKS] != 0) Hold_Definition_status[starte_ramme[ramme_INDEKS] - 1] = 3;
            if (ramme_lås[ramme_INDEKS] != 0) { udgive_lås(ramme_lås[ramme_INDEKS]); ramme_lås[ramme_INDEKS] = 0; }
            ramme_INDEKS--;
        }
        bruger.Skrive("Uncaught ");
        if (heap_VÆRDI[던진객체] == 9) { bruger.Skrive(undtagelse_navn(heap_VÆRDI[던진객체 + 2])); bruger.Skrive(": "); skrive_sms(heap_VÆRDI[던진객체 + 3]); }
        else bruger.Skrive("user exception");
        bruger.skrive_tegn_VÆRDI(10); 던진객체 = 0; fejl = true;
    }
    // 이 JVM의 operand_Stak 항목은 aktuel_vare category-1(int/reference)만 허용한다.
    static void 스택명령(int kommando_KODE) {
        int 첫값 = 빼기(0), 첫형식 = returnere_Type;
        if (kommando_KODE == 87) return;
        if (kommando_KODE == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int byte_data = 빼기(0), SEKUND_format = returnere_Type;
        if (kommando_KODE == 88) return;
        if (kommando_KODE == 90) { 넣기(첫값, 첫형식); 넣기(byte_data, SEKUND_format); 넣기(첫값, 첫형식); return; }
        if (kommando_KODE == 92) { 넣기(byte_data, SEKUND_format); 넣기(첫값, 첫형식); 넣기(byte_data, SEKUND_format); 넣기(첫값, 첫형식); return; }
        if (kommando_KODE == 95) { 넣기(첫값, 첫형식); 넣기(byte_data, SEKUND_format); return; }
        int tegnkode = 빼기(0), 셋째형식 = returnere_Type;
        if (kommando_KODE == 91) { 넣기(첫값, 첫형식); 넣기(tegnkode, 셋째형식); 넣기(byte_data, SEKUND_format); 넣기(첫값, 첫형식); return; }
        if (kommando_KODE == 93) { 넣기(byte_data, SEKUND_format); 넣기(첫값, 첫형식); 넣기(tegnkode, 셋째형식); 넣기(byte_data, SEKUND_format); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = returnere_Type;
        넣기(byte_data, SEKUND_format); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(tegnkode, 셋째형식); 넣기(byte_data, SEKUND_format); 넣기(첫값, 첫형식);
    }
    static void 새객체(int navn_konstant, int 시작점) {
        int område_KODE = 0, gyldig_varighed = 0, undtagelse_referere = undtagelse_konstant(navn_konstant);
        if (Ord_sms(navn_konstant, "java/lang/StringBuilder")) { område_KODE = 4; gyldig_varighed = 1; }
        if (Ord_sms(navn_konstant, "java/io/FileInputStream")) { område_KODE = 5; gyldig_varighed = 2; }
        if (Ord_sms(navn_konstant, "java/io/FileOutputStream")) { område_KODE = 6; gyldig_varighed = 2; }
        if (undtagelse_referere != 0) { område_KODE = 9; gyldig_varighed = 2; }
        if (Ord_sms(navn_konstant, "java/util/ArrayList")) { område_KODE = 10; gyldig_varighed = 2; }
        if (Ord_sms(navn_konstant, "java/util/HashMap")) { område_KODE = 11; gyldig_varighed = 2; }
        if (Ord_sms(navn_konstant, "java/lang/Integer")) { område_KODE = 12; gyldig_varighed = 1; }
        if (Ord_sms(navn_konstant, "java/net/Socket")) { område_KODE = 17; gyldig_varighed = 5; }
        if (Ord_sms(navn_konstant, "java/net/ServerSocket")) { område_KODE = 18; gyldig_varighed = 5; }
        if (Ord_sms(navn_konstant, "java/net/DatagramSocket")) { område_KODE = 15; gyldig_varighed = 3; }
        if (Ord_sms(navn_konstant, "java/net/DatagramPacket")) { område_KODE = 16; gyldig_varighed = 4; }
        if (Ord_sms(navn_konstant, "java/lang/Thread") || Ord_sms(navn_konstant, "Dansk/eget/arbejder")) { område_KODE = 13; gyldig_varighed = 2; }
        if (Ord_sms(navn_konstant, "java/lang/Object")) { område_KODE = 8; }
        if (område_KODE == 0 && skærmbillede_Hold(navn_konstant) != 0) { område_KODE = skærmbillede_Hold(navn_konstant); gyldig_varighed = 12; }
        if (område_KODE == 0) {
            int tegnkode = Søg_Hold_Definition(navn_konstant); if (tegnkode < 0 || fejl || !starte(tegnkode, 시작점)) return;
            område_KODE = 32 + tegnkode; gyldig_varighed = Hold_udvidelsesstik_TÆL[tegnkode];
        }
        int objekt_referere = tildel_Lager(område_KODE, gyldig_varighed); if (fejl) return;
        if (område_KODE == 13 && Ord_sms(navn_konstant, "Dansk/eget/arbejder")) heap_VÆRDI[objekt_referere + 3] = 1;
        if (område_KODE >= 24 && område_KODE <= 28 && 한국어화면종(navn_konstant) != 0) heap_VÆRDI[objekt_referere + 13] = 1;
        if (område_KODE == 5 || område_KODE == 6 || område_KODE == 15 || område_KODE == 17 || område_KODE == 18) heap_VÆRDI[objekt_referere + 2] = -1;
        if (område_KODE == 9) heap_VÆRDI[objekt_referere + 2] = undtagelse_referere;
        넣기(objekt_referere, 2);
    }
    static boolean 값같음(int 첫값, int byte_data) {
        if (첫값 == byte_data) return true;
        if (첫값 == 0 || byte_data == 0 || 첫값 < 0 || byte_data < 0 || 첫값 >= heap_afslutte_et_opkald_placere || byte_data >= heap_afslutte_et_opkald_placere) return false;
        if (heap_VÆRDI[첫값] == 1 && heap_VÆRDI[byte_data] == 1) return 글같음(첫값, byte_data, false);
        return heap_VÆRDI[첫값] == 12 && heap_VÆRDI[byte_data] == 12 && heap_VÆRDI[첫값 + 2] == heap_VÆRDI[byte_data + 2];
    }
    static int 글조각(int objekt_referere, int START_placere, int afslutte_et_opkald_placere) {
        if (!objekt_VÆRDI(objekt_referere, 1)) return 0;
        if (START_placere < 0 || afslutte_et_opkald_placere < START_placere || afslutte_et_opkald_placere > heap_VÆRDI[objekt_referere + 1]) { fejl_VÆRDI("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = tildel_Lager(1, afslutte_et_opkald_placere - START_placere); if (fejl) return 0;
        for (int Loop_INDEKS = START_placere; Loop_INDEKS < afslutte_et_opkald_placere; Loop_INDEKS++) heap_VÆRDI[반환값 + 2 + Loop_INDEKS - START_placere] = heap_VÆRDI[objekt_referere + 2 + Loop_INDEKS];
        return 반환값;
    }
    static int Deltag_sms(int 첫값, int byte_data) {
        if (!objekt_VÆRDI(첫값, 1) || !objekt_VÆRDI(byte_data, 1)) return 0;
        int post_TÆL_8f7753a1 = heap_VÆRDI[첫값 + 1], metode_INDEKS = heap_VÆRDI[byte_data + 1], 반환값 = tildel_Lager(1, post_TÆL_8f7753a1 + metode_INDEKS); if (fejl) return 0;
        for (int Loop_INDEKS = 0; Loop_INDEKS < post_TÆL_8f7753a1; Loop_INDEKS++) heap_VÆRDI[반환값 + 2 + Loop_INDEKS] = heap_VÆRDI[첫값 + 2 + Loop_INDEKS];
        for (int Loop_INDEKS = 0; Loop_INDEKS < metode_INDEKS; Loop_INDEKS++) heap_VÆRDI[반환값 + 2 + post_TÆL_8f7753a1 + Loop_INDEKS] = heap_VÆRDI[byte_data + 2 + Loop_INDEKS];
        return 반환값;
    }
    static boolean 기본호출(int ejer, int navn_konstant, int 서술상수, int kommando_KODE) {
        if (Ord_sms(ejer, "Dansk/eget/실행인수") && kommando_KODE == 184) {
            if (Ord_sms(navn_konstant, "vare_TÆL") && Ord_sms(서술상수, "()I")) { 넣기(bruger.인수개수() - 1, 1); return true; }
            if (Ord_sms(navn_konstant, "Tekst") && Ord_sms(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= bruger.인수개수() - 1) 예외던짐(29, "Udfør_kommando Argumenter 범위를 벗어났습니다");
                else 넣기(vært_tegn(bruger.Argumenter(순번 + 1)), 2);
                return true;
            }
            fejl_VÆRDI("지원하지 않는 Dansk Udfør_kommando Argumenter 호출"); return true;
        }
        if (Ord_sms(ejer, "Dansk/eget/arbejder")) { Proces_tråd(navn_konstant, 서술상수, kommando_KODE, true); return true; }
        if (한국어화면소유(ejer)) { 한국어화면호출(ejer, navn_konstant, 서술상수, kommando_KODE); return true; }
        if (skærmbillede_ejer(ejer)) { 화면호출(ejer, navn_konstant, 서술상수, kommando_KODE); return true; }
        if (Ord_sms(ejer, "java/net/Socket") || Ord_sms(ejer, "java/net/ServerSocket") || Ord_sms(ejer, "java/io/InputStream") || Ord_sms(ejer, "java/io/OutputStream")) { 흐름호출(ejer, navn_konstant, 서술상수, kommando_KODE); return true; }
        if (Ord_sms(ejer, "Dansk/eget/kerne_VÆRDI") && kommando_KODE == 184) {
            if (Ord_sms(navn_konstant, "화면너비") && Ord_sms(서술상수, "()I")) { 넣기(bruger.화면너비(), 1); return true; }
            if (Ord_sms(navn_konstant, "화면높이") && Ord_sms(서술상수, "()I")) { 넣기(bruger.화면높이(), 1); return true; }
            if (Ord_sms(navn_konstant, "밀리초") && Ord_sms(서술상수, "()I")) { 넣기(bruger.밀리초(), 1); return true; }
            if (Ord_sms(navn_konstant, "그림대기") && Ord_sms(서술상수, "()I")) { 넣기(bruger.그림대기(), 1); return true; }
            if (Ord_sms(navn_konstant, "rektangel") && Ord_sms(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), Y_koordinat = 빼기(1), X_koordinat = 빼기(1); 넣기(bruger.rektangel(X_koordinat, Y_koordinat, 너비, 높이, 색상), 1); return true; }
        }
        if (Ord_sms(ejer, "java/net/InetAddress") || Ord_sms(ejer, "java/net/DatagramPacket") || Ord_sms(ejer, "java/net/DatagramSocket")) { 통신호출(ejer, navn_konstant, 서술상수, kommando_KODE); return true; }
        if (Ord_sms(ejer, "java/lang/Thread")) { 가닥호출(navn_konstant, 서술상수, kommando_KODE); return true; }
        if (Ord_sms(ejer, "java/lang/Object")) {
            if (Ord_sms(navn_konstant, "<init>") && Ord_sms(서술상수, "()V") && kommando_KODE == 183) { it_gyldig_objekt(빼기(2)); return true; }
            if (Ord_sms(navn_konstant, "equals") && Ord_sms(서술상수, "(Ljava/lang/Object;)Z")) { int byte_data = 빼기(2), 첫값 = 빼기(2); if (it_gyldig_objekt(첫값)) 넣기(첫값 == byte_data ? 1 : 0, 1); return true; }
        }
        if (undtagelse_konstant(ejer) != 0) {
            if (Ord_sms(navn_konstant, "<init>") && kommando_KODE == 183 && (Ord_sms(서술상수, "()V") || Ord_sms(서술상수, "(Ljava/lang/String;)V"))) {
                int prompt = Ord_sms(서술상수, "()V") ? 0 : 빼기(2), objekt_referere = 빼기(2);
                if (objekt_VÆRDI(objekt_referere, 9)) { heap_VÆRDI[objekt_referere + 3] = prompt; heap_referere[objekt_referere + 3] = 1; } return true;
            }
            if ((Ord_sms(navn_konstant, "getMessage") || Ord_sms(navn_konstant, "설명")) && Ord_sms(서술상수, "()Ljava/lang/String;")) { int objekt_referere = 빼기(2); if (objekt_VÆRDI(objekt_referere, 9)) 넣기(heap_VÆRDI[objekt_referere + 3], 2); return true; }
        }
        if (Ord_sms(ejer, "java/lang/String")) {
            if (kommando_KODE == 182 && Ord_sms(navn_konstant, "getBytes") && (Ord_sms(서술상수, "()[B") || Ord_sms(서술상수, "(Ljava/lang/String;)[B"))) {
                int kodning_navn = Ord_sms(서술상수, "()[B") ? 0 : 빼기(2), objekt_referere = 빼기(2);
                if (!objekt_VÆRDI(objekt_referere, 1)) return true;
                if (kodning_navn != 0 && !글같음(kodning_navn, vært_tegn("UTF-8"), false) && !글같음(kodning_navn, vært_tegn("UTF8"), false) && !글같음(kodning_navn, vært_tegn("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int post_TÆL_8f7753a1 = heap_VÆRDI[objekt_referere + 1], 반환값 = tildel_Lager(20, post_TÆL_8f7753a1 * 3), 사용수 = 0; if (fejl) return true;
                for (int indre_placere = 0; indre_placere < post_TÆL_8f7753a1; indre_placere++) {
                    int tegnkode = heap_VÆRDI[objekt_referere + 2 + indre_placere];
                    if (tegnkode >= 0xd800 && tegnkode <= 0xdbff && indre_placere + 1 < post_TÆL_8f7753a1 && heap_VÆRDI[objekt_referere + 3 + indre_placere] >= 0xdc00 && heap_VÆRDI[objekt_referere + 3 + indre_placere] <= 0xdfff) tegnkode = 0x10000 + ((tegnkode - 0xd800) << 10) + heap_VÆRDI[objekt_referere + 2 + ++indre_placere] - 0xdc00;
                    else if (tegnkode >= 0xd800 && tegnkode <= 0xdfff) tegnkode = '?';
                    if (tegnkode < 128) heap_VÆRDI[반환값 + 2 + 사용수++] = tegnkode;
                    else { int byte_TÆL = tegnkode < 2048 ? 2 : tegnkode < 65536 ? 3 : 4; heap_VÆRDI[반환값 + 2 + 사용수++] = (byte)((byte_TÆL == 2 ? 192 : byte_TÆL == 3 ? 224 : 240) | tegnkode >> (6 * (byte_TÆL - 1))); for (int Sammenligning_placere = byte_TÆL - 1; Sammenligning_placere > 0; Sammenligning_placere--) heap_VÆRDI[반환값 + 2 + 사용수++] = (byte)(128 | tegnkode >> (6 * (Sammenligning_placere - 1)) & 63); }
                }
                heap_VÆRDI[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (kommando_KODE == 184 && Ord_sms(navn_konstant, "valueOf") && Ord_sms(서술상수, "(I)Ljava/lang/String;")) { 넣기(ciffer_tegn(빼기(1)), 2); return true; }
            if (kommando_KODE != 182) return false;
            if (Ord_sms(navn_konstant, "equals") && Ord_sms(서술상수, "(Ljava/lang/Object;)Z")) { int byte_data = 빼기(2), 첫값 = 빼기(2); if (objekt_VÆRDI(첫값, 1)) 넣기(글같음(첫값, byte_data, false) ? 1 : 0, 1); return true; }
            if (Ord_sms(navn_konstant, "isEmpty") && Ord_sms(서술상수, "()Z")) { int 첫값 = 빼기(2); if (objekt_VÆRDI(첫값, 1)) 넣기(heap_VÆRDI[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Ord_sms(navn_konstant, "substring") && (Ord_sms(서술상수, "(I)Ljava/lang/String;") || Ord_sms(서술상수, "(II)Ljava/lang/String;"))) {
                boolean SEKUND_VÆRDI = Ord_sms(서술상수, "(II)Ljava/lang/String;"); int afslutte_et_opkald_placere = SEKUND_VÆRDI ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (objekt_VÆRDI(첫값, 1)) 넣기(글조각(첫값, 시작점, SEKUND_VÆRDI ? afslutte_et_opkald_placere : heap_VÆRDI[첫값 + 1]), 2); return true;
            }
            if (Ord_sms(navn_konstant, "concat") && Ord_sms(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int byte_data = 빼기(2), 첫값 = 빼기(2); 넣기(Deltag_sms(첫값, byte_data), 2); return true; }
            if (Ord_sms(navn_konstant, "hashCode") && Ord_sms(서술상수, "()I")) { int 첫값 = 빼기(2), hash_VÆRDI = 0; if (objekt_VÆRDI(첫값, 1)) { for (int Loop_INDEKS = 0; Loop_INDEKS < heap_VÆRDI[첫값 + 1]; Loop_INDEKS++) hash_VÆRDI = hash_VÆRDI * 31 + heap_VÆRDI[첫값 + 2 + Loop_INDEKS]; 넣기(hash_VÆRDI, 1); } return true; }
            if (Ord_sms(navn_konstant, "toString") && Ord_sms(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (objekt_VÆRDI(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Ord_sms(ejer, "java/lang/Integer")) {
            if (kommando_KODE == 184 && Ord_sms(navn_konstant, "valueOf") && Ord_sms(서술상수, "(I)Ljava/lang/Integer;")) { int data_VÆRDI = 빼기(1), objekt_referere = data_VÆRDI >= -128 && data_VÆRDI <= 127 ? Store_heltal[data_VÆRDI + 128] : 0; if (objekt_referere == 0) { objekt_referere = tildel_Lager(12, 1); if (!fejl) { heap_VÆRDI[objekt_referere + 2] = data_VÆRDI; if (data_VÆRDI >= -128 && data_VÆRDI <= 127) Store_heltal[data_VÆRDI + 128] = objekt_referere; } } 넣기(objekt_referere, 2); return true; }
            if (kommando_KODE == 183 && Ord_sms(navn_konstant, "<init>") && Ord_sms(서술상수, "(I)V")) { int data_VÆRDI = 빼기(1), objekt_referere = 빼기(2); if (objekt_VÆRDI(objekt_referere, 12)) heap_VÆRDI[objekt_referere + 2] = data_VÆRDI; return true; }
            if (kommando_KODE == 182 && Ord_sms(navn_konstant, "intValue") && Ord_sms(서술상수, "()I")) { int objekt_referere = 빼기(2); if (objekt_VÆRDI(objekt_referere, 12)) 넣기(heap_VÆRDI[objekt_referere + 2], 1); return true; }
            if (kommando_KODE == 184 && Ord_sms(navn_konstant, "toString") && Ord_sms(서술상수, "(I)Ljava/lang/String;")) { 넣기(ciffer_tegn(빼기(1)), 2); return true; }
        }
        if (Ord_sms(ejer, "java/lang/Math") && kommando_KODE == 184) {
            if (Ord_sms(navn_konstant, "abs") && Ord_sms(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((Ord_sms(navn_konstant, "min") || Ord_sms(navn_konstant, "max")) && Ord_sms(서술상수, "(II)I")) { int byte_data = 빼기(1), 첫값 = 빼기(1); 넣기(Ord_sms(navn_konstant, "min") ? (첫값 < byte_data ? 첫값 : byte_data) : (첫값 > byte_data ? 첫값 : byte_data), 1); return true; }
        }
        if (Ord_sms(ejer, "java/lang/System") && kommando_KODE == 184) {
            if (Ord_sms(navn_konstant, "gc") && Ord_sms(서술상수, "()V")) { 수거(); return true; }
            if (Ord_sms(navn_konstant, "arraycopy") && Ord_sms(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int post_TÆL_8f7753a1 = 빼기(1), destination_VÆRDI_INDEKS = 빼기(1), byte_data = 빼기(2), START_placere = 빼기(1), 첫값 = 빼기(2);
                if (it_gyldig_objekt(첫값) && it_gyldig_objekt(byte_data)) {
                    int område_KODE = heap_VÆRDI[첫값];
                    if (heap_VÆRDI[byte_data] != område_KODE || (område_KODE != 2 && område_KODE != 3 && (område_KODE < 20 || område_KODE > 23))) fejl_VÆRDI("arraycopy type mismatch");
                    else if (post_TÆL_8f7753a1 < 0 || START_placere < 0 || destination_VÆRDI_INDEKS < 0 || START_placere > heap_VÆRDI[첫값 + 1] - post_TÆL_8f7753a1 || destination_VÆRDI_INDEKS > heap_VÆRDI[byte_data + 1] - post_TÆL_8f7753a1) fejl_VÆRDI("ArrayIndexOutOfBoundsException");
                    else if (첫값 == byte_data && destination_VÆRDI_INDEKS > START_placere) { for (int Loop_INDEKS = post_TÆL_8f7753a1 - 1; Loop_INDEKS >= 0; Loop_INDEKS--) heap_VÆRDI[byte_data + 2 + destination_VÆRDI_INDEKS + Loop_INDEKS] = heap_VÆRDI[첫값 + 2 + START_placere + Loop_INDEKS]; }
                    else { for (int Loop_INDEKS = 0; Loop_INDEKS < post_TÆL_8f7753a1 && !fejl; Loop_INDEKS++) { int data_VÆRDI = heap_VÆRDI[첫값 + 2 + START_placere + Loop_INDEKS]; if (område_KODE != 3 || 배열저장가능(byte_data, data_VÆRDI)) heap_VÆRDI[byte_data + 2 + destination_VÆRDI_INDEKS + Loop_INDEKS] = data_VÆRDI; } }
                }
                return true;
            }
        }
        if (Ord_sms(ejer, "java/util/ArrayList") || Ord_sms(ejer, "java/util/List") || Ord_sms(ejer, "java/util/HashMap") || Ord_sms(ejer, "java/util/Map")) {
            모음호출(ejer, navn_konstant, 서술상수, kommando_KODE); return true;
        }
        return false;
    }
    static void 모음늘리기(int objekt_referere, int 필요수) {
        int Forrige_VÆRDI = heap_VÆRDI[objekt_referere + 2], kapacitet_data = Forrige_VÆRDI == 0 ? 0 : heap_VÆRDI[Forrige_VÆRDI + 1];
        if (kapacitet_data >= 필요수) return;
        int Næste_placere = kapacitet_data < 8 ? 8 : kapacitet_data * 2; if (Næste_placere < 필요수) Næste_placere = 필요수;
        int data_MATRIX = tildel_Lager(3, Næste_placere); if (fejl) return;
        for (int Loop_INDEKS = 0; Loop_INDEKS < kapacitet_data; Loop_INDEKS++) heap_VÆRDI[data_MATRIX + 2 + Loop_INDEKS] = heap_VÆRDI[Forrige_VÆRDI + 2 + Loop_INDEKS];
        heap_VÆRDI[objekt_referere + 2] = data_MATRIX; heap_referere[objekt_referere + 2] = 1;
    }
    static void 모음호출(int ejer, int navn_konstant, int 서술상수, int kommando_KODE) {
        boolean 대응참조 = Ord_sms(ejer, "java/util/HashMap") || Ord_sms(ejer, "java/util/Map"); int område_KODE = 대응참조 ? 11 : 10;
        if (Ord_sms(navn_konstant, "<init>") && kommando_KODE == 183 && Ord_sms(서술상수, "()V")) { int objekt_referere = 빼기(2); if (objekt_VÆRDI(objekt_referere, område_KODE)) 모음늘리기(objekt_referere, 8); return; }
        if (kommando_KODE != 182 && kommando_KODE != 185) { fejl_VÆRDI("invalid collection invocation"); return; }
        if (Ord_sms(navn_konstant, "size") && Ord_sms(서술상수, "()I") || Ord_sms(navn_konstant, "isEmpty") && Ord_sms(서술상수, "()Z")) {
            int objekt_referere = 빼기(2); if (objekt_VÆRDI(objekt_referere, område_KODE)) 넣기(Ord_sms(navn_konstant, "size") ? heap_VÆRDI[objekt_referere + 3] : heap_VÆRDI[objekt_referere + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Ord_sms(navn_konstant, "clear") && Ord_sms(서술상수, "()V")) { int objekt_referere = 빼기(2); if (objekt_VÆRDI(objekt_referere, område_KODE)) { int data_MATRIX = heap_VÆRDI[objekt_referere + 2]; for (int Loop_INDEKS = 0; Loop_INDEKS < heap_VÆRDI[data_MATRIX + 1]; Loop_INDEKS++) heap_VÆRDI[data_MATRIX + 2 + Loop_INDEKS] = 0; heap_VÆRDI[objekt_referere + 3] = 0; } return; }
        if (!대응참조 && Ord_sms(navn_konstant, "add") && Ord_sms(서술상수, "(Ljava/lang/Object;)Z")) {
            int data_VÆRDI = 빼기(2), objekt_referere = 빼기(2); if (!objekt_VÆRDI(objekt_referere, 10)) return;
            int post_TÆL_8f7753a1 = heap_VÆRDI[objekt_referere + 3]; 모음늘리기(objekt_referere, post_TÆL_8f7753a1 + 1); if (!fejl) { heap_VÆRDI[heap_VÆRDI[objekt_referere + 2] + 2 + post_TÆL_8f7753a1] = data_VÆRDI; heap_VÆRDI[objekt_referere + 3] = post_TÆL_8f7753a1 + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Ord_sms(navn_konstant, "get") || Ord_sms(navn_konstant, "remove")) && Ord_sms(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && Ord_sms(navn_konstant, "set") && Ord_sms(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean it_Tildelt = Ord_sms(navn_konstant, "set"); int data_VÆRDI = it_Tildelt ? 빼기(2) : 0, post_placere_206f1c6d = 빼기(1), objekt_referere = 빼기(2);
            if (!objekt_VÆRDI(objekt_referere, 10)) return;
            int post_TÆL_8f7753a1 = heap_VÆRDI[objekt_referere + 3], data_MATRIX = heap_VÆRDI[objekt_referere + 2];
            if (post_placere_206f1c6d < 0 || post_placere_206f1c6d >= post_TÆL_8f7753a1) { 예외던짐(6, "list index"); return; }
            int Forrige_VÆRDI = heap_VÆRDI[data_MATRIX + 2 + post_placere_206f1c6d];
            if (it_Tildelt) heap_VÆRDI[data_MATRIX + 2 + post_placere_206f1c6d] = data_VÆRDI;
            if (Ord_sms(navn_konstant, "remove")) { for (int Loop_INDEKS = post_placere_206f1c6d + 1; Loop_INDEKS < post_TÆL_8f7753a1; Loop_INDEKS++) heap_VÆRDI[data_MATRIX + 1 + Loop_INDEKS] = heap_VÆRDI[data_MATRIX + 2 + Loop_INDEKS]; heap_VÆRDI[data_MATRIX + 1 + post_TÆL_8f7753a1] = 0; heap_VÆRDI[objekt_referere + 3] = post_TÆL_8f7753a1 - 1; }
            넣기(Forrige_VÆRDI, 2); return;
        }
        if (대응참조 && (Ord_sms(navn_konstant, "get") || Ord_sms(navn_konstant, "remove")) && Ord_sms(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Ord_sms(navn_konstant, "put") && Ord_sms(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Ord_sms(navn_konstant, "containsKey") && Ord_sms(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Ord_sms(navn_konstant, "put"), fjerne = Ord_sms(navn_konstant, "remove");
            int data_VÆRDI = 넣기여부 ? 빼기(2) : 0, tast_referere = 빼기(2), objekt_referere = 빼기(2); if (!objekt_VÆRDI(objekt_referere, 11)) return;
            int post_TÆL_8f7753a1 = heap_VÆRDI[objekt_referere + 3], data_MATRIX = heap_VÆRDI[objekt_referere + 2], 찾은여부 = -1;
            for (int Loop_INDEKS = 0; Loop_INDEKS < post_TÆL_8f7753a1; Loop_INDEKS++) if (값같음(tast_referere, heap_VÆRDI[data_MATRIX + 2 + 2 * Loop_INDEKS])) { 찾은여부 = Loop_INDEKS; break; }
            int Forrige_VÆRDI = 찾은여부 < 0 ? 0 : heap_VÆRDI[data_MATRIX + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(objekt_referere, (post_TÆL_8f7753a1 + 1) * 2); data_MATRIX = heap_VÆRDI[objekt_referere + 2]; 찾은여부 = post_TÆL_8f7753a1; if (!fejl) heap_VÆRDI[objekt_referere + 3] = post_TÆL_8f7753a1 + 1; }
                if (!fejl) { heap_VÆRDI[data_MATRIX + 2 + 2 * 찾은여부] = tast_referere; heap_VÆRDI[data_MATRIX + 3 + 2 * 찾은여부] = data_VÆRDI; }
            }
            if (fjerne && 찾은여부 >= 0) { for (int Loop_INDEKS = 찾은여부 + 1; Loop_INDEKS < post_TÆL_8f7753a1; Loop_INDEKS++) { heap_VÆRDI[data_MATRIX + 2 * Loop_INDEKS] = heap_VÆRDI[data_MATRIX + 2 + 2 * Loop_INDEKS]; heap_VÆRDI[data_MATRIX + 1 + 2 * Loop_INDEKS] = heap_VÆRDI[data_MATRIX + 3 + 2 * Loop_INDEKS]; } heap_VÆRDI[data_MATRIX + 2 * post_TÆL_8f7753a1] = 0; heap_VÆRDI[data_MATRIX + 1 + 2 * post_TÆL_8f7753a1] = 0; heap_VÆRDI[objekt_referere + 3] = post_TÆL_8f7753a1 - 1; }
            if (Ord_sms(navn_konstant, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(Forrige_VÆRDI, 2);
            return;
        }
        fejl_VÆRDI("unsupported collection method");
    }
    static boolean 잠금얻기(int objekt_referere) {
        if (!it_gyldig_objekt(objekt_referere)) return false;
        if (잠금깊이[objekt_referere] != 0 && lås_ejer[objekt_referere] != aktuel_tråd + 1) { ændringsanmodning = true; return false; }
        lås_ejer[objekt_referere] = aktuel_tråd + 1; 잠금깊이[objekt_referere]++; return true;
    }
    static void udgive_lås(int objekt_referere) {
        if (!it_gyldig_objekt(objekt_referere)) return;
        if (잠금깊이[objekt_referere] == 0 || lås_ejer[objekt_referere] != aktuel_tråd + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[objekt_referere] == 0) lås_ejer[objekt_referere] = 0;
    }
    static boolean SKIFT_tråd() {
        tråd_ramme[aktuel_tråd] = ramme_INDEKS;
        if (ramme_INDEKS < aktuel_tråd * 32) tråd_status[aktuel_tråd] = 3;
        for (int Loop_INDEKS = 0; Loop_INDEKS < Antal_tråde; Loop_INDEKS++) if (tråd_status[Loop_INDEKS] == 2 && tråd_status[가닥대기[Loop_INDEKS]] == 3) tråd_status[Loop_INDEKS] = 1;
        for (int Loop_INDEKS = 1; Loop_INDEKS <= Antal_tråde; Loop_INDEKS++) {
            int Næste_placere = (aktuel_tråd + Loop_INDEKS) % Antal_tråde;
            if (tråd_status[Næste_placere] == 1) { aktuel_tråd = Næste_placere; ramme_INDEKS = tråd_ramme[Næste_placere]; ændringsanmodning = false; return true; }
        }
        for (int Loop_INDEKS = 0; Loop_INDEKS < Antal_tråde; Loop_INDEKS++) if (tråd_status[Loop_INDEKS] != 3) { fejl_VÆRDI("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int navn_konstant, int 서술상수, int kommando_KODE) { Proces_tråd(navn_konstant, 서술상수, kommando_KODE, false); }
    static void Proces_tråd(int navn_konstant, int 서술상수, int kommando_KODE, boolean Dansk) {
        if (kommando_KODE == 184 && Ord_sms(navn_konstant, Dansk ? "AFKAST_job" : "yield") && Ord_sms(서술상수, "()V")) { ændringsanmodning = true; return; }
        if (kommando_KODE == 184 && Ord_sms(navn_konstant, "currentThread") && Ord_sms(서술상수, "()Ljava/lang/Thread;")) { 넣기(tråd_objekt[aktuel_tråd], 2); return; }
        if (kommando_KODE == 183 && Ord_sms(navn_konstant, "<init>") && (Ord_sms(서술상수, "()V") || Ord_sms(서술상수, Dansk ? "(LDansk/eget/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int mål_mail = Ord_sms(서술상수, "()V") ? 0 : 빼기(2), objekt_referere = 빼기(2);
            if (!it_gyldig_objekt(objekt_referere)) return;
            if (heap_VÆRDI[objekt_referere] == 13) { heap_VÆRDI[objekt_referere + 2] = mål_mail; heap_referere[objekt_referere + 2] = 1; }
            else if (mål_mail != 0) fejl_VÆRDI("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (kommando_KODE == 182 && (Ord_sms(navn_konstant, Dansk ? "START_job" : "start") || Ord_sms(navn_konstant, Dansk ? "기다리기" : "join")) && Ord_sms(서술상수, "()V") || kommando_KODE == 182 && Ord_sms(navn_konstant, Dansk ? "살아있는가" : "isAlive") && Ord_sms(서술상수, "()Z")) {
            int objekt_referere = 빼기(2); if (!it_gyldig_objekt(objekt_referere)) return;
            int konto_VÆRDI = -1; for (int Loop_INDEKS = 0; Loop_INDEKS < Antal_tråde; Loop_INDEKS++) if (tråd_objekt[Loop_INDEKS] == objekt_referere) konto_VÆRDI = Loop_INDEKS;
            if (Ord_sms(navn_konstant, Dansk ? "살아있는가" : "isAlive")) { 넣기(konto_VÆRDI >= 0 && tråd_status[konto_VÆRDI] != 3 ? 1 : 0, 1); return; }
            if (Ord_sms(navn_konstant, Dansk ? "기다리기" : "join")) { if (konto_VÆRDI >= 0 && tråd_status[konto_VÆRDI] != 3) { 가닥대기[aktuel_tråd] = konto_VÆRDI; tråd_status[aktuel_tråd] = 2; ændringsanmodning = true; } return; }
            if (konto_VÆRDI >= 0) { 예외던짐(Dansk ? 38 : 16, "thread already started"); return; }
            if (Antal_tråde == 4) { fejl_VÆRDI("thread limit (4 including main)"); return; }
            int mål_mail = heap_VÆRDI[objekt_referere] == 13 ? heap_VÆRDI[objekt_referere + 2] : objekt_referere;
            int fil_INDEKS = mål_mail > 0 && heap_VÆRDI[mål_mail] >= 32 ? navn_metode(heap_VÆRDI[mål_mail] - 32, Dansk ? "Kør" : "run", "()V") : -1;
            if (mål_mail != 0 && fil_INDEKS < 0) { fejl_VÆRDI("Runnable.run required"); return; }
            konto_VÆRDI = Antal_tråde++; tråd_objekt[konto_VÆRDI] = objekt_referere; tråd_mål[konto_VÆRDI] = mål_mail;
            int ramme = konto_VÆRDI * 32; tråd_ramme[konto_VÆRDI] = fil_INDEKS < 0 ? ramme - 1 : ramme; tråd_status[konto_VÆRDI] = fil_INDEKS < 0 ? 3 : 1;
            if (fil_INDEKS >= 0) { ramme_metode[ramme] = fil_INDEKS; ramme_placere[ramme] = metode_START[fil_INDEKS]; lokal_VÆRDI[ramme * 128] = mål_mail; lokal_Type[ramme * 128] = 2; }
            return;
        }
        fejl_VÆRDI("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], mail_sms = new int[16];
    static int lokal_mail() { return mail_objekt(0x7f000001); }
    static int mail_objekt(int VÆRDI) { int objekt_referere = tildel_Lager(14, 1); if (!fejl) heap_VÆRDI[objekt_referere + 2] = VÆRDI; return objekt_referere; }
    static int 주소해독(int objekt_referere) {
        if (objekt_referere == 0 || 글같음(objekt_referere, vært_tegn("localhost"), false)) return 0x7f000001;
        if (!objekt_VÆRDI(objekt_referere, 1)) return 0;
        int data_VÆRDI = 0, i_alt_TÆL = 0, mail_byte = 0, 자릿수 = 0, post_TÆL_8f7753a1 = heap_VÆRDI[objekt_referere + 1];
        for (int Loop_INDEKS = 0; Loop_INDEKS <= post_TÆL_8f7753a1; Loop_INDEKS++) {
            int tegnkode = Loop_INDEKS == post_TÆL_8f7753a1 ? '.' : heap_VÆRDI[objekt_referere + 2 + Loop_INDEKS];
            if (tegnkode == '.') { if (자릿수 == 0 || i_alt_TÆL == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } data_VÆRDI = data_VÆRDI << 8 | mail_byte; i_alt_TÆL++; mail_byte = 자릿수 = 0; }
            else { if (tegnkode < '0' || tegnkode > '9' || ++자릿수 > 3 || (mail_byte = mail_byte * 10 + tegnkode - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (i_alt_TÆL != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return data_VÆRDI;
    }
    static int mail_tegn(int data_VÆRDI) {
        int post_TÆL_8f7753a1 = 0;
        for (int flytte = 24; flytte >= 0; flytte -= 8) {
            int mail_byte = data_VÆRDI >>> flytte & 255;
            if (mail_byte >= 100) mail_sms[post_TÆL_8f7753a1++] = '0' + mail_byte / 100;
            if (mail_byte >= 10) mail_sms[post_TÆL_8f7753a1++] = '0' + mail_byte / 10 % 10;
            mail_sms[post_TÆL_8f7753a1++] = '0' + mail_byte % 10; if (flytte != 0) mail_sms[post_TÆL_8f7753a1++] = '.';
        }
        int objekt_referere = tildel_Lager(1, post_TÆL_8f7753a1); if (!fejl) for (int Loop_INDEKS = 0; Loop_INDEKS < post_TÆL_8f7753a1; Loop_INDEKS++) heap_VÆRDI[objekt_referere + 2 + Loop_INDEKS] = mail_sms[Loop_INDEKS]; return objekt_referere;
    }
    static void 통신호출(int ejer, int navn_konstant, int 서술상수, int kommando_KODE) {
        if (Ord_sms(ejer, "java/net/InetAddress")) {
            if (kommando_KODE == 184 && Ord_sms(navn_konstant, "getLoopbackAddress") && Ord_sms(서술상수, "()Ljava/net/InetAddress;")) { 넣기(lokal_mail(), 2); return; }
            if (kommando_KODE == 184 && Ord_sms(navn_konstant, "getByName") && Ord_sms(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int data_VÆRDI = 주소해독(빼기(2)); if (던진객체 == 0 && !fejl) 넣기(mail_objekt(data_VÆRDI), 2); return;
            }
            if (kommando_KODE == 182 && Ord_sms(navn_konstant, "getHostAddress") && Ord_sms(서술상수, "()Ljava/lang/String;")) { int objekt_referere = 빼기(2); if (objekt_VÆRDI(objekt_referere, 14)) 넣기(mail_tegn(heap_VÆRDI[objekt_referere + 2]), 2); return; }
        }
        if (Ord_sms(ejer, "java/net/DatagramPacket")) {
            if (kommando_KODE == 183 && Ord_sms(navn_konstant, "<init>") && (Ord_sms(서술상수, "([BI)V") || Ord_sms(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean destination_VÆRDI_referere = Ord_sms(서술상수, "([BILjava/net/InetAddress;I)V"); int portnummer = destination_VÆRDI_referere ? 빼기(1) : 0, mail_referere = destination_VÆRDI_referere ? 빼기(2) : 0;
                int post_TÆL_8f7753a1 = 빼기(1), data_MATRIX = 빼기(2), objekt_referere = 빼기(2);
                if (!objekt_VÆRDI(objekt_referere, 16) || !objekt_VÆRDI(data_MATRIX, 20)) return;
                if (post_TÆL_8f7753a1 < 0 || post_TÆL_8f7753a1 > heap_VÆRDI[data_MATRIX + 1] || portnummer < 0 || portnummer > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (mail_referere != 0 && !objekt_VÆRDI(mail_referere, 14)) return;
                heap_VÆRDI[objekt_referere + 2] = data_MATRIX; heap_referere[objekt_referere + 2] = 1; heap_VÆRDI[objekt_referere + 3] = post_TÆL_8f7753a1;
                heap_VÆRDI[objekt_referere + 4] = mail_referere; heap_referere[objekt_referere + 4] = 1; heap_VÆRDI[objekt_referere + 5] = portnummer; return;
            }
            if (kommando_KODE == 182 && Ord_sms(navn_konstant, "setLength") && Ord_sms(서술상수, "(I)V")) {
                int post_TÆL_8f7753a1 = 빼기(1), objekt_referere = 빼기(2); if (!objekt_VÆRDI(objekt_referere, 16)) return;
                if (post_TÆL_8f7753a1 < 0 || post_TÆL_8f7753a1 > heap_VÆRDI[heap_VÆRDI[objekt_referere + 2] + 1]) 예외던짐(9, "invalid datagram length"); else heap_VÆRDI[objekt_referere + 3] = post_TÆL_8f7753a1; return;
            }
            if (kommando_KODE == 182 && (Ord_sms(navn_konstant, "getData") && Ord_sms(서술상수, "()[B") || Ord_sms(navn_konstant, "getLength") && Ord_sms(서술상수, "()I") || Ord_sms(navn_konstant, "getAddress") && Ord_sms(서술상수, "()Ljava/net/InetAddress;") || Ord_sms(navn_konstant, "getPort") && Ord_sms(서술상수, "()I"))) {
                int objekt_referere = 빼기(2); if (!objekt_VÆRDI(objekt_referere, 16)) return;
                int post_placere_206f1c6d = Ord_sms(navn_konstant, "getData") ? 2 : Ord_sms(navn_konstant, "getLength") ? 3 : Ord_sms(navn_konstant, "getAddress") ? 4 : 5;
                넣기(heap_VÆRDI[objekt_referere + post_placere_206f1c6d], post_placere_206f1c6d == 2 || post_placere_206f1c6d == 4 ? 2 : 1); return;
            }
        }
        if (Ord_sms(ejer, "java/net/DatagramSocket")) {
            if (kommando_KODE == 183 && Ord_sms(navn_konstant, "<init>") && (Ord_sms(서술상수, "()V") || Ord_sms(서술상수, "(I)V"))) {
                int portnummer = Ord_sms(서술상수, "()V") ? 0 : 빼기(1), objekt_referere = 빼기(2); if (!objekt_VÆRDI(objekt_referere, 15)) return;
                if (portnummer < 0 || portnummer > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = bruger.åben_netværk(portnummer); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else heap_VÆRDI[objekt_referere + 2] = 열린파일번호; return;
            }
            if (kommando_KODE == 182 && Ord_sms(navn_konstant, "setSoTimeout") && Ord_sms(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), objekt_referere = 빼기(2); if (!objekt_VÆRDI(objekt_referere, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else heap_VÆRDI[objekt_referere + 3] = 밀리초값; return;
            }
            if (kommando_KODE == 182 && Ord_sms(navn_konstant, "getLocalPort") && Ord_sms(서술상수, "()I")) { int objekt_referere = 빼기(2); if (objekt_VÆRDI(objekt_referere, 15)) 넣기(heap_VÆRDI[objekt_referere + 2] < 0 ? -1 : bruger.netværk_port(heap_VÆRDI[objekt_referere + 2]), 1); return; }
            if (kommando_KODE == 182 && Ord_sms(navn_konstant, "isClosed") && Ord_sms(서술상수, "()Z")) { int objekt_referere = 빼기(2); if (objekt_VÆRDI(objekt_referere, 15)) 넣기(heap_VÆRDI[objekt_referere + 2] < 0 ? 1 : 0, 1); return; }
            if (kommando_KODE == 182 && Ord_sms(navn_konstant, "close") && Ord_sms(서술상수, "()V")) { int objekt_referere = 빼기(2); if (objekt_VÆRDI(objekt_referere, 15) && heap_VÆRDI[objekt_referere + 2] >= 0) { bruger.파일서술자닫기(heap_VÆRDI[objekt_referere + 2]); heap_VÆRDI[objekt_referere + 2] = -1; } return; }
            if (kommando_KODE == 182 && (Ord_sms(navn_konstant, "send") || Ord_sms(navn_konstant, "receive")) && Ord_sms(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int pakke = 빼기(2), objekt_referere = 빼기(2); if (!objekt_VÆRDI(pakke, 16) || !objekt_VÆRDI(objekt_referere, 15)) return;
                int data_MATRIX = heap_VÆRDI[pakke + 2], gyldig_varighed = heap_VÆRDI[pakke + 3], 열린파일번호 = heap_VÆRDI[objekt_referere + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Ord_sms(navn_konstant, "send")) {
                    if (!objekt_VÆRDI(heap_VÆRDI[pakke + 4], 14)) return;
                    if (gyldig_varighed > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int Loop_INDEKS = 0; Loop_INDEKS < gyldig_varighed; Loop_INDEKS++) 통신임시[Loop_INDEKS] = heap_VÆRDI[data_MATRIX + 2 + Loop_INDEKS];
                    if (bruger.maile_netværk(열린파일번호, heap_VÆRDI[heap_VÆRDI[pakke + 4] + 2], heap_VÆRDI[pakke + 5], 통신임시, gyldig_varighed) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int post_TÆL_8f7753a1 = bruger.modtage_netværk(열린파일번호, 통신임시, gyldig_varighed > 512 ? 512 : gyldig_varighed);
                    if (post_TÆL_8f7753a1 == -11) {
                        int aktuelt_klokkeslæt = bruger.밀리초();
                        if (heap_VÆRDI[objekt_referere + 4] == 0) heap_VÆRDI[objekt_referere + 4] = aktuelt_klokkeslæt + 1;
                        if (heap_VÆRDI[objekt_referere + 3] > 0 && aktuelt_klokkeslæt - (heap_VÆRDI[objekt_referere + 4] - 1) >= heap_VÆRDI[objekt_referere + 3]) { heap_VÆRDI[objekt_referere + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(objekt_referere, 2); 넣기(pakke, 2); ramme_placere[ramme_INDEKS] = 틀명령[ramme_INDEKS]; ændringsanmodning = true; return;
                    }
                    heap_VÆRDI[objekt_referere + 4] = 0;
                    if (post_TÆL_8f7753a1 < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int Loop_INDEKS = 0; Loop_INDEKS < post_TÆL_8f7753a1; Loop_INDEKS++) heap_VÆRDI[data_MATRIX + 2 + Loop_INDEKS] = (byte)통신임시[Loop_INDEKS];
                    heap_VÆRDI[pakke + 3] = post_TÆL_8f7753a1; heap_VÆRDI[pakke + 4] = mail_objekt(통신임시[513]); heap_referere[pakke + 4] = 1; heap_VÆRDI[pakke + 5] = 통신임시[512];
                }
                return;
            }
        }
        fejl_VÆRDI("unsupported java.net method");
    }
    static boolean 흐름대기(int objekt_referere) {
        int aktuelt_klokkeslæt = bruger.밀리초();
        if (heap_VÆRDI[objekt_referere + 5] == 0) heap_VÆRDI[objekt_referere + 5] = aktuelt_klokkeslæt + 1;
        if (heap_VÆRDI[objekt_referere + 3] > 0 && aktuelt_klokkeslæt - (heap_VÆRDI[objekt_referere + 5] - 1) >= heap_VÆRDI[objekt_referere + 3]) { heap_VÆRDI[objekt_referere + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        ramme_placere[ramme_INDEKS] = 틀명령[ramme_INDEKS]; ændringsanmodning = true; return true;
    }
    static void 흐름호출(int ejer, int navn_konstant, int 서술상수, int kommando_KODE) {
        boolean modtage_side = Ord_sms(ejer, "java/net/ServerSocket"), strøm = Ord_sms(ejer, "java/io/InputStream") || Ord_sms(ejer, "java/io/OutputStream");
        if (!strøm && kommando_KODE == 183 && Ord_sms(navn_konstant, "<init>")) {
            boolean 빈여부 = Ord_sms(서술상수, "()V"), 이름지정여부 = Ord_sms(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = Ord_sms(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(빈여부 || modtage_side && Ord_sms(서술상수, "(I)V") || !modtage_side && (이름지정여부 || 주소지정여부))) { fejl_VÆRDI("unsupported socket constructor"); return; }
            int portnummer = 빈여부 ? 0 : 빼기(1), mail_referere = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, objekt_referere = 빼기(2);
            if (!objekt_VÆRDI(objekt_referere, modtage_side ? 18 : 17)) return;
            if (portnummer < 0 || portnummer > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !objekt_VÆRDI(mail_referere, 14)) return;
            int netværks_id = 이름지정여부 ? 주소해독(mail_referere) : 주소지정여부 ? heap_VÆRDI[mail_referere + 2] : 0x7f000001;
            if (fejl || 던진객체 != 0) return;
            int 열린파일번호 = bruger.strøm_kontrol(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = 빈여부 ? 0 : modtage_side ? bruger.strøm_kontrol(1, 열린파일번호, portnummer) : bruger.Forbind_strøm(열린파일번호, netværks_id, portnummer);
            if (처리값 < 0) { bruger.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            heap_VÆRDI[objekt_referere + 2] = 열린파일번호; heap_VÆRDI[objekt_referere + 4] = portnummer; heap_VÆRDI[objekt_referere + 6] = 빈여부 ? 0 : 1; return;
        }
        if (!strøm && Ord_sms(navn_konstant, "setSoTimeout") && Ord_sms(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), objekt_referere = 빼기(2); if (!objekt_VÆRDI(objekt_referere, modtage_side ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else heap_VÆRDI[objekt_referere + 3] = 밀리초값; return; }
        if (!strøm && Ord_sms(navn_konstant, "close") && Ord_sms(서술상수, "()V")) { int objekt_referere = 빼기(2); if (objekt_VÆRDI(objekt_referere, modtage_side ? 18 : 17) && heap_VÆRDI[objekt_referere + 2] >= 0) { bruger.파일서술자닫기(heap_VÆRDI[objekt_referere + 2]); heap_VÆRDI[objekt_referere + 2] = -1; } return; }
        if (!strøm && (Ord_sms(navn_konstant, "getLocalPort") || Ord_sms(navn_konstant, "getPort") || Ord_sms(navn_konstant, "isClosed") || Ord_sms(navn_konstant, "isConnected"))) {
            int objekt_referere = 빼기(2); if (!objekt_VÆRDI(objekt_referere, modtage_side ? 18 : 17)) return;
            넣기(Ord_sms(navn_konstant, "isClosed") ? heap_VÆRDI[objekt_referere + 2] < 0 ? 1 : 0 : Ord_sms(navn_konstant, "isConnected") ? heap_VÆRDI[objekt_referere + 6] : Ord_sms(navn_konstant, "getPort") ? heap_VÆRDI[objekt_referere + 4] : heap_VÆRDI[objekt_referere + 2] < 0 ? -1 : bruger.strøm_kontrol(4, heap_VÆRDI[objekt_referere + 2], 0), 1); return;
        }
        if (modtage_side && Ord_sms(navn_konstant, "accept") && Ord_sms(서술상수, "()Ljava/net/Socket;")) {
            int objekt_referere = 빼기(2); if (!objekt_VÆRDI(objekt_referere, 18)) return; int 열린파일번호 = bruger.strøm_kontrol(3, heap_VÆRDI[objekt_referere + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(objekt_referere)) 넣기(objekt_referere, 2); return; }
            heap_VÆRDI[objekt_referere + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = tildel_Lager(17, 5); if (fejl) { bruger.파일서술자닫기(열린파일번호); return; } heap_VÆRDI[반환값 + 2] = 열린파일번호; heap_VÆRDI[반환값 + 4] = bruger.strøm_kontrol(5, 열린파일번호, 0); heap_VÆRDI[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!modtage_side && !strøm && ((Ord_sms(navn_konstant, "getInputStream") && Ord_sms(서술상수, "()Ljava/io/InputStream;")) || (Ord_sms(navn_konstant, "getOutputStream") && Ord_sms(서술상수, "()Ljava/io/OutputStream;")))) {
            int objekt_referere = 빼기(2); if (!objekt_VÆRDI(objekt_referere, 17)) return; if (heap_VÆRDI[objekt_referere + 2] < 0 || heap_VÆRDI[objekt_referere + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = tildel_Lager(19, 4); if (fejl) return; heap_VÆRDI[반환값 + 2] = objekt_referere; heap_referere[반환값 + 2] = 1; heap_VÆRDI[반환값 + 3] = Ord_sms(navn_konstant, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (strøm) {
            boolean 읽기여부 = Ord_sms(navn_konstant, "read"), it_skrive_kirurgi = Ord_sms(navn_konstant, "write"), blok = Ord_sms(서술상수, "([B)I") || Ord_sms(서술상수, "([B)V"), it_UNDERMATRIX = Ord_sms(서술상수, "([BII)I") || Ord_sms(서술상수, "([BII)V");
            int post_TÆL_8f7753a1 = it_UNDERMATRIX ? 빼기(1) : 0, 시작변위 = it_UNDERMATRIX ? 빼기(1) : 0, data_MATRIX = blok || it_UNDERMATRIX ? 빼기(2) : 0;
            int data_VÆRDI = it_skrive_kirurgi && Ord_sms(서술상수, "(I)V") ? 빼기(1) : 0, objekt_referere = 빼기(2);
            if (!objekt_VÆRDI(objekt_referere, 19)) return; int overordnet_referere = heap_VÆRDI[objekt_referere + 2], 열린파일번호 = heap_VÆRDI[overordnet_referere + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Ord_sms(navn_konstant, "close") && Ord_sms(서술상수, "()V")) { bruger.파일서술자닫기(열린파일번호); heap_VÆRDI[overordnet_referere + 2] = -1; return; }
            if (Ord_sms(navn_konstant, "flush") && Ord_sms(서술상수, "()V")) return;
            if ((!읽기여부 && !it_skrive_kirurgi) || 읽기여부 != (heap_VÆRDI[objekt_referere + 3] == 0)) { fejl_VÆRDI("unsupported stream operation"); return; }
            if (blok || it_UNDERMATRIX) { if (!objekt_VÆRDI(data_MATRIX, 20)) return; if (blok) post_TÆL_8f7753a1 = heap_VÆRDI[data_MATRIX + 1]; if (시작변위 < 0 || post_TÆL_8f7753a1 < 0 || 시작변위 > heap_VÆRDI[data_MATRIX + 1] - post_TÆL_8f7753a1) { 예외던짐(6, "stream array bounds"); return; } }
            else post_TÆL_8f7753a1 = 1;
            if (post_TÆL_8f7753a1 == 0) { if (읽기여부) 넣기(0, 1); return; }
            int fuldført_TÆL = it_skrive_kirurgi ? heap_VÆRDI[objekt_referere + 4] : 0, 처리값 = 0;
            while (fuldført_TÆL < post_TÆL_8f7753a1) {
                처리값 = 읽기여부 ? bruger.파일한바이트읽기(열린파일번호) : bruger.파일한바이트쓰기(열린파일번호, blok || it_UNDERMATRIX ? heap_VÆRDI[data_MATRIX + 2 + 시작변위 + fuldført_TÆL] : data_VÆRDI);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (blok || it_UNDERMATRIX)) heap_VÆRDI[data_MATRIX + 2 + 시작변위 + fuldført_TÆL] = (byte)처리값;
                fuldført_TÆL++; if (읽기여부 && !(blok || it_UNDERMATRIX)) break;
            }
            if (처리값 == -11 && (it_skrive_kirurgi || fuldført_TÆL == 0)) {
                heap_VÆRDI[objekt_referere + 4] = fuldført_TÆL;
                if (흐름대기(overordnet_referere)) { 넣기(objekt_referere, 2); if (blok || it_UNDERMATRIX) 넣기(data_MATRIX, 2); if (it_UNDERMATRIX) { 넣기(시작변위, 1); 넣기(post_TÆL_8f7753a1, 1); } if (it_skrive_kirurgi && !(blok || it_UNDERMATRIX)) 넣기(data_VÆRDI, 1); } return;
            }
            heap_VÆRDI[objekt_referere + 4] = 0; heap_VÆRDI[overordnet_referere + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(fuldført_TÆL == 0 && 처리값 == 256 ? -1 : blok || it_UNDERMATRIX ? fuldført_TÆL : 처리값, 1); return;
        }
        fejl_VÆRDI("unsupported Socket/ServerSocket method");
    }
    static int[] skærmbillede_referere = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int navn_konstant) {
        if (Ord_sms(navn_konstant, "Dansk/eget/Vindue")) return 24;
        if (Ord_sms(navn_konstant, "Dansk/eget/Etiket")) return 26;
        if (Ord_sms(navn_konstant, "Dansk/eget/knap")) return 27;
        if (Ord_sms(navn_konstant, "Dansk/eget/tekstfelt")) return 28;
        if (Ord_sms(navn_konstant, "Dansk/eget/동작알림")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int navn_konstant) {
        return 한국어화면종(navn_konstant) != 0 || Ord_sms(navn_konstant, "Dansk/eget/skærmbillede_element") || Ord_sms(navn_konstant, "Dansk/eget/hændelse_kø");
    }
    static int skærmbillede_Hold(int navn_konstant) {
        int 한국어종 = 한국어화면종(navn_konstant); if (한국어종 != 0) return 한국어종;
        if (Ord_sms(navn_konstant, "javax/swing/JFrame")) return 24;
        if (Ord_sms(navn_konstant, "javax/swing/JPanel")) return 25;
        if (Ord_sms(navn_konstant, "javax/swing/JLabel")) return 26;
        if (Ord_sms(navn_konstant, "javax/swing/JButton")) return 27;
        if (Ord_sms(navn_konstant, "javax/swing/JTextField")) return 28;
        if (Ord_sms(navn_konstant, "java/awt/event/ActionEvent")) return 29;
        if (Ord_sms(navn_konstant, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean skærmbillede_ejer(int navn_konstant) {
        return skærmbillede_Hold(navn_konstant) != 0 || Ord_sms(navn_konstant, "java/awt/Component") || Ord_sms(navn_konstant, "java/awt/Container") || Ord_sms(navn_konstant, "javax/swing/JComponent") || Ord_sms(navn_konstant, "javax/swing/AbstractButton") || Ord_sms(navn_konstant, "javax/swing/text/JTextComponent") || Ord_sms(navn_konstant, "javax/swing/SwingUtilities");
    }
    static boolean skærmbillede_objekt(int objekt_referere) { if (!it_gyldig_objekt(objekt_referere)) return false; if (heap_VÆRDI[objekt_referere] < 24 || heap_VÆRDI[objekt_referere] > 28) { fejl_VÆRDI("unsupported Swing receiver"); return false; } return true; }
    static void sæt_skærmbillede_tegn(int objekt_referere, int sms_referere) {
        if (sms_referere != 0 && !objekt_VÆRDI(sms_referere, 1)) return;
        int post_TÆL_8f7753a1 = sms_referere == 0 ? 0 : heap_VÆRDI[sms_referere + 1]; if (post_TÆL_8f7753a1 > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int Loop_INDEKS = 0; Loop_INDEKS < post_TÆL_8f7753a1; Loop_INDEKS++) 화면글임시[Loop_INDEKS] = heap_VÆRDI[sms_referere + 2 + Loop_INDEKS];
        if (bruger.skærmbillede_sms(heap_VÆRDI[objekt_referere + 2], 화면글임시, post_TÆL_8f7753a1) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        heap_VÆRDI[objekt_referere + 3] = sms_referere; heap_referere[objekt_referere + 3] = 1;
    }
    static int 화면문자읽기(int objekt_referere) {
        int konto_VÆRDI = heap_VÆRDI[objekt_referere + 2], post_TÆL_8f7753a1 = bruger.skærmbillede_forbindelse(8, konto_VÆRDI, 0, 0, 0, 0), 사용수 = 0;
        if (post_TÆL_8f7753a1 < 0) { fejl_VÆRDI("GUI text read failed"); return 0; }
        for (int Loop_INDEKS = 0; Loop_INDEKS < post_TÆL_8f7753a1; Loop_INDEKS++) { int 부호값 = bruger.skærmbillede_forbindelse(9, konto_VÆRDI, Loop_INDEKS, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = tildel_Lager(1, 사용수); if (!fejl) for (int Loop_INDEKS = 0; Loop_INDEKS < 사용수; Loop_INDEKS++) heap_VÆRDI[반환값 + 2 + Loop_INDEKS] = 화면글임시[Loop_INDEKS]; return 반환값;
    }
    /* Dansk 객체를 직접 만들고 kerne_VÆRDI skærmbillede 기능에 연결한다. Swing objekt_VÆRDI/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int ejer, int navn_konstant, int 서술상수, int kommando_KODE) {
        if (Ord_sms(ejer, "Dansk/eget/hændelse_kø")) {
            if (kommando_KODE == 184 && Ord_sms(navn_konstant, "나중에실행") && Ord_sms(서술상수, "(LDansk/eget/실행할일;)V")) {
                int job_To_do = 빼기(2); if (!it_gyldig_objekt(job_To_do)) return;
                if (나중수 == 8) { fejl_VÆRDI("skærmbillede 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = job_To_do; return;
            }
            if (kommando_KODE == 184 && Ord_sms(navn_konstant, "사건처리중인가") && Ord_sms(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            fejl_VÆRDI("지원하지 않는 Dansk skærmbillede 일정 호출"); return;
        }
        if (Ord_sms(ejer, "Dansk/eget/동작알림")) {
            int 알림 = 빼기(2); if (!objekt_VÆRDI(알림, 29) || heap_VÆRDI[알림 + 3] == 0) return;
            if (Ord_sms(navn_konstant, "hændelseskilde") && Ord_sms(서술상수, "()LDansk/eget/skærmbillede_element;")) 넣기(heap_VÆRDI[알림 + 2], 2);
            else if (Ord_sms(navn_konstant, "kommando_sms") && Ord_sms(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(heap_VÆRDI[알림 + 2]), 2);
            else if (Ord_sms(navn_konstant, "INDEKS") && Ord_sms(서술상수, "()I")) 넣기(1001, 1);
            else fejl_VÆRDI("지원하지 않는 Dansk Handling 알림 호출"); return;
        }
        if (kommando_KODE == 183 && Ord_sms(navn_konstant, "<init>")) {
            int 종류 = 한국어화면종(ejer), 받이 = 0, 가로 = 0, Lodret_placere = 0, 폭 = 0, 높이 = 0;
            if (종류 == 24 && Ord_sms(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (bruger.화면너비() - 폭) / 2; Lodret_placere = (bruger.화면높이() - 높이) / 2;
            } else if ((종류 == 26 || 종류 == 28) && Ord_sms(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && Ord_sms(서술상수, "(Ljava/lang/String;IIIILDansk/eget/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); Lodret_placere = 빼기(1); 가로 = 빼기(1);
            } else { fejl_VÆRDI("지원하지 않는 Dansk skærmbillede 생성자"); return; }
            int Tekst = 빼기(2), element_VÆRDI = 빼기(2); if (!skærmbillede_objekt(element_VÆRDI)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || Lodret_placere < 0 || 폭 > bruger.화면너비() - 가로 || 높이 > bruger.화면높이() - Lodret_placere) { 예외던짐(27, "skærmbillede 영역을 벗어난 크기입니다"); return; }
            int INDEKS = bruger.skærmbillede_forbindelse(0, 종류 - 23, 0, 0, 0, 0);
            if (INDEKS < 1 || INDEKS > 32) { fejl_VÆRDI("skærmbillede element_VÆRDI 자리가 가득 찼습니다"); return; }
            heap_VÆRDI[element_VÆRDI + 2] = INDEKS; skærmbillede_referere[INDEKS - 1] = element_VÆRDI;
            heap_VÆRDI[element_VÆRDI + 5] = 가로; heap_VÆRDI[element_VÆRDI + 6] = Lodret_placere; heap_VÆRDI[element_VÆRDI + 7] = 폭; heap_VÆRDI[element_VÆRDI + 8] = 높이; heap_VÆRDI[element_VÆRDI + 10] = 2;
            heap_VÆRDI[element_VÆRDI + 4] = 받이; heap_referere[element_VÆRDI + 4] = 1; heap_VÆRDI[element_VÆRDI + 12] = 1;
            bruger.skærmbillede_forbindelse(1, INDEKS, 가로, Lodret_placere, 폭, 높이);
            if (종류 == 24) bruger.skærmbillede_forbindelse(7, INDEKS, 2, 0, 0, 0);
            sæt_skærmbillede_tegn(element_VÆRDI, Tekst); return;
        }
        if (kommando_KODE != 182) { fejl_VÆRDI("잘못된 Dansk skærmbillede 호출 Kommando"); return; }
        if (Ord_sms(navn_konstant, "skrive_sms") && Ord_sms(서술상수, "(Ljava/lang/String;)V")) {
            int Tekst = 빼기(2), element_VÆRDI = 빼기(2); if (skærmbillede_objekt(element_VÆRDI)) sæt_skærmbillede_tegn(element_VÆRDI, Tekst); return;
        }
        if (Ord_sms(navn_konstant, "글읽기") && Ord_sms(서술상수, "()Ljava/lang/String;")) {
            int element_VÆRDI = 빼기(2); if (skærmbillede_objekt(element_VÆRDI)) 넣기(화면문자읽기(element_VÆRDI), 2); return;
        }
        if (Ord_sms(navn_konstant, "동작맡기기") && Ord_sms(서술상수, "(LDansk/eget/동작받이;)V")) {
            int 받이 = 빼기(2), element_VÆRDI = 빼기(2);
            if (skærmbillede_objekt(element_VÆRDI)) { heap_VÆRDI[element_VÆRDI + 4] = 받이; heap_referere[element_VÆRDI + 4] = 1; heap_VÆRDI[element_VÆRDI + 12] = 1; } return;
        }
        if (Ord_sms(navn_konstant, "Tilføj_element") && Ord_sms(서술상수, "(LDansk/eget/skærmbillede_element;)V")) {
            int barn_VÆRDI = 빼기(2), overordnet_VÆRDI = 빼기(2); if (!skærmbillede_objekt(barn_VÆRDI) || !skærmbillede_objekt(overordnet_VÆRDI)) return;
            if (bruger.skærmbillede_forbindelse(2, heap_VÆRDI[overordnet_VÆRDI + 2], heap_VÆRDI[barn_VÆRDI + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 skærmbillede 부모입니다"); return; }
            heap_VÆRDI[barn_VÆRDI + 11] = overordnet_VÆRDI; heap_referere[barn_VÆRDI + 11] = 1; return;
        }
        if (Ord_sms(navn_konstant, "자리정하기") && Ord_sms(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), Lodret_placere = 빼기(1), 가로 = 빼기(1), element_VÆRDI = 빼기(2); if (!skærmbillede_objekt(element_VÆRDI)) return;
            if (bruger.skærmbillede_forbindelse(1, heap_VÆRDI[element_VÆRDI + 2], 가로, Lodret_placere, 폭, 높이) < 0) { 예외던짐(27, "skærmbillede 영역을 벗어난 자리입니다"); return; }
            heap_VÆRDI[element_VÆRDI + 5] = 가로; heap_VÆRDI[element_VÆRDI + 6] = Lodret_placere; heap_VÆRDI[element_VÆRDI + 7] = 폭; heap_VÆRDI[element_VÆRDI + 8] = 높이; return;
        }
        if ((Ord_sms(navn_konstant, "vise_vindue") || Ord_sms(navn_konstant, "Luk")) && Ord_sms(서술상수, "()V")) {
            boolean synlighed_VÆRDI = Ord_sms(navn_konstant, "vise_vindue"); int element_VÆRDI = 빼기(2); if (!skærmbillede_objekt(element_VÆRDI)) return;
            if (bruger.skærmbillede_forbindelse(synlighed_VÆRDI ? 3 : 4, heap_VÆRDI[element_VÆRDI + 2], synlighed_VÆRDI ? 1 : 0, 0, 0, 0) < 0) { fejl_VÆRDI("화면은 interaktiv 명령에서 실행해야 합니다"); return; }
            heap_VÆRDI[element_VÆRDI + 9] = synlighed_VÆRDI ? 1 : 0; return;
        }
        if (Ord_sms(navn_konstant, "보이는가") && Ord_sms(서술상수, "()Z")) { int element_VÆRDI = 빼기(2); if (skærmbillede_objekt(element_VÆRDI)) 넣기(heap_VÆRDI[element_VÆRDI + 9], 1); return; }
        fejl_VÆRDI("지원하지 않는 Dansk skærmbillede metode_VÆRDI");
    }
    static void 화면호출(int ejer, int navn_konstant, int 서술상수, int kommando_KODE) {
        if (Ord_sms(ejer, "javax/swing/SwingUtilities")) {
            if (kommando_KODE == 184 && Ord_sms(navn_konstant, "invokeLater") && Ord_sms(서술상수, "(Ljava/lang/Runnable;)V")) { int objekt_referere = 빼기(2); if (!it_gyldig_objekt(objekt_referere)) return; if (나중수 == 8) { fejl_VÆRDI("invokeLater queue full"); return; } 나중실행[나중수++] = objekt_referere; return; }
            if (kommando_KODE == 184 && Ord_sms(navn_konstant, "isEventDispatchThread") && Ord_sms(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            fejl_VÆRDI("unsupported SwingUtilities method"); return;
        }
        if (Ord_sms(ejer, "java/awt/event/ActionEvent")) {
            int objekt_referere = 빼기(2); if (!objekt_VÆRDI(objekt_referere, 29)) return;
            if (Ord_sms(navn_konstant, "getSource") && Ord_sms(서술상수, "()Ljava/lang/Object;")) 넣기(heap_VÆRDI[objekt_referere + 2], 2);
            else if (Ord_sms(navn_konstant, "getActionCommand") && Ord_sms(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(heap_VÆRDI[objekt_referere + 2]), 2);
            else if (Ord_sms(navn_konstant, "getID") && Ord_sms(서술상수, "()I")) 넣기(1001, 1);
            else fejl_VÆRDI("unsupported ActionEvent method"); return;
        }
        if (kommando_KODE == 183 && Ord_sms(navn_konstant, "<init>")) {
            int KOLONNER = 0, sms_referere = 0;
            if (Ord_sms(서술상수, "(I)V")) KOLONNER = 빼기(1);
            else if (Ord_sms(서술상수, "(Ljava/lang/String;I)V")) { KOLONNER = 빼기(1); sms_referere = 빼기(2); }
            else if (Ord_sms(서술상수, "(Ljava/lang/String;)V")) sms_referere = 빼기(2);
            else if (Ord_sms(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Ord_sms(서술상수, "()V")) { fejl_VÆRDI("unsupported Swing constructor"); return; }
            int objekt_referere = 빼기(2); if (!it_gyldig_objekt(objekt_referere)) return;
            if (heap_VÆRDI[objekt_referere] == 30) { fejl_VÆRDI("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!skærmbillede_objekt(objekt_referere) || KOLONNER < 0) return;
            int konto_VÆRDI = bruger.skærmbillede_forbindelse(0, heap_VÆRDI[objekt_referere] - 23, 0, 0, 0, 0);
            if (konto_VÆRDI < 1 || konto_VÆRDI > 32) { fejl_VÆRDI("GUI widget slots exhausted"); return; }
            heap_VÆRDI[objekt_referere + 2] = konto_VÆRDI; skærmbillede_referere[konto_VÆRDI - 1] = objekt_referere; heap_VÆRDI[objekt_referere + 5] = heap_VÆRDI[objekt_referere] == 24 ? 130 : 16; heap_VÆRDI[objekt_referere + 6] = heap_VÆRDI[objekt_referere] == 24 ? 110 : 16;
            heap_VÆRDI[objekt_referere + 7] = heap_VÆRDI[objekt_referere] == 24 ? 380 : 220; heap_VÆRDI[objekt_referere + 8] = heap_VÆRDI[objekt_referere] == 24 ? 240 : 28; heap_VÆRDI[objekt_referere + 10] = 1;
            sæt_skærmbillede_tegn(objekt_referere, sms_referere); return;
        }
        if (Ord_sms(navn_konstant, "setText") || Ord_sms(navn_konstant, "setTitle")) { int sms_referere = 빼기(2), objekt_referere = 빼기(2); if (skærmbillede_objekt(objekt_referere) && Ord_sms(서술상수, "(Ljava/lang/String;)V")) sæt_skærmbillede_tegn(objekt_referere, sms_referere); return; }
        if (Ord_sms(navn_konstant, "getText") || Ord_sms(navn_konstant, "getTitle")) { int objekt_referere = 빼기(2); if (skærmbillede_objekt(objekt_referere) && Ord_sms(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(objekt_referere), 2); return; }
        if (Ord_sms(navn_konstant, "addActionListener") && Ord_sms(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int modtage_referere = 빼기(2), objekt_referere = 빼기(2); if (skærmbillede_objekt(objekt_referere)) { heap_VÆRDI[objekt_referere + 4] = modtage_referere; heap_referere[objekt_referere + 4] = 1; } return; }
        if (Ord_sms(navn_konstant, "getContentPane") && Ord_sms(서술상수, "()Ljava/awt/Container;")) { int objekt_referere = 빼기(2); if (skærmbillede_objekt(objekt_referere)) 넣기(objekt_referere, 2); return; }
        if (Ord_sms(navn_konstant, "setLayout") && Ord_sms(서술상수, "(Ljava/awt/LayoutManager;)V")) { int Layout_referere = 빼기(2), objekt_referere = 빼기(2); if (skærmbillede_objekt(objekt_referere) && Layout_referere != 0) fejl_VÆRDI("only absolute layout (null) is supported"); return; }
        if (Ord_sms(navn_konstant, "add") && (Ord_sms(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || Ord_sms(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean Layout_lidelse = Ord_sms(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (Layout_lidelse) 빼기(2);
            int barn_referere = 빼기(2), objekt_referere = 빼기(2); if (!skærmbillede_objekt(barn_referere) || !skærmbillede_objekt(objekt_referere)) return;
            if (bruger.skærmbillede_forbindelse(2, heap_VÆRDI[objekt_referere + 2], heap_VÆRDI[barn_referere + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            heap_VÆRDI[barn_referere + 11] = objekt_referere; heap_referere[barn_referere + 11] = 1; if (!Layout_lidelse) 넣기(barn_referere, 2); return;
        }
        if (Ord_sms(navn_konstant, "setBounds") && Ord_sms(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), Y_koordinat = 빼기(1), X_koordinat = 빼기(1), objekt_referere = 빼기(2); if (!skærmbillede_objekt(objekt_referere)) return;
            if (bruger.skærmbillede_forbindelse(1, heap_VÆRDI[objekt_referere + 2], X_koordinat, Y_koordinat, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            heap_VÆRDI[objekt_referere + 5] = X_koordinat; heap_VÆRDI[objekt_referere + 6] = Y_koordinat; heap_VÆRDI[objekt_referere + 7] = 너비; heap_VÆRDI[objekt_referere + 8] = 높이; return;
        }
        if (Ord_sms(navn_konstant, "setSize") && Ord_sms(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), objekt_referere = 빼기(2); if (!skærmbillede_objekt(objekt_referere)) return;
            if (bruger.skærmbillede_forbindelse(1, heap_VÆRDI[objekt_referere + 2], heap_VÆRDI[objekt_referere + 5], heap_VÆRDI[objekt_referere + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { heap_VÆRDI[objekt_referere + 7] = 너비; heap_VÆRDI[objekt_referere + 8] = 높이; } return;
        }
        if (Ord_sms(navn_konstant, "setLocationRelativeTo") && Ord_sms(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), objekt_referere = 빼기(2); if (!skærmbillede_objekt(objekt_referere)) return; if (상대배치 != 0) { fejl_VÆRDI("only screen centering supported"); return; } heap_VÆRDI[objekt_referere + 5] = (bruger.화면너비() - heap_VÆRDI[objekt_referere + 7]) / 2; heap_VÆRDI[objekt_referere + 6] = (bruger.화면높이() - heap_VÆRDI[objekt_referere + 8]) / 2; bruger.skærmbillede_forbindelse(1, heap_VÆRDI[objekt_referere + 2], heap_VÆRDI[objekt_referere + 5], heap_VÆRDI[objekt_referere + 6], heap_VÆRDI[objekt_referere + 7], heap_VÆRDI[objekt_referere + 8]); return; }
        if (Ord_sms(navn_konstant, "setDefaultCloseOperation") && Ord_sms(서술상수, "(I)V")) { int Policy = 빼기(1), objekt_referere = 빼기(2); if (skærmbillede_objekt(objekt_referere)) { if (Policy < 0 || Policy > 3) 예외던짐(9, "close policy"); else { heap_VÆRDI[objekt_referere + 10] = Policy; bruger.skærmbillede_forbindelse(7, heap_VÆRDI[objekt_referere + 2], Policy, 0, 0, 0); } } return; }
        if (Ord_sms(navn_konstant, "setVisible") && Ord_sms(서술상수, "(Z)V")) { int data_VÆRDI = 빼기(1), objekt_referere = 빼기(2); if (skærmbillede_objekt(objekt_referere)) { int 처리값 = bruger.skærmbillede_forbindelse(3, heap_VÆRDI[objekt_referere + 2], data_VÆRDI, 0, 0, 0); if (처리값 < 0) fejl_VÆRDI("Swing requires a standalone interactive command"); else heap_VÆRDI[objekt_referere + 9] = data_VÆRDI; } return; }
        if (Ord_sms(navn_konstant, "dispose") && Ord_sms(서술상수, "()V")) { int objekt_referere = 빼기(2); if (skærmbillede_objekt(objekt_referere)) { bruger.skærmbillede_forbindelse(4, heap_VÆRDI[objekt_referere + 2], 0, 0, 0, 0); heap_VÆRDI[objekt_referere + 9] = 0; } return; }
        if (Ord_sms(navn_konstant, "repaint") || Ord_sms(navn_konstant, "validate")) { int objekt_referere = 빼기(2); if (!skærmbillede_objekt(objekt_referere) || !Ord_sms(서술상수, "()V")) return; bruger.skærmbillede_forbindelse(1, heap_VÆRDI[objekt_referere + 2], heap_VÆRDI[objekt_referere + 5], heap_VÆRDI[objekt_referere + 6], heap_VÆRDI[objekt_referere + 7], heap_VÆRDI[objekt_referere + 8]); return; }
        if (Ord_sms(navn_konstant, "isVisible") && Ord_sms(서술상수, "()Z")) { int objekt_referere = 빼기(2); if (skærmbillede_objekt(objekt_referere)) 넣기(heap_VÆRDI[objekt_referere + 9], 1); return; }
        fejl_VÆRDI("unsupported Swing method (native subset)");
    }
    static void udføre_hændelse(int mål_mail, int hændelse_tal, boolean Dansk) {
        if (mål_mail < 1 || heap_VÆRDI[mål_mail] < 32) { fejl_VÆRDI("Java event listener required"); return; }
        int fil_INDEKS = navn_metode(heap_VÆRDI[mål_mail] - 32, hændelse_tal == 0 ? (Dansk ? "Kør" : "run") : (Dansk ? "modtage_To_do" : "actionPerformed"), hændelse_tal == 0 ? "()V" : (Dansk ? "(LDansk/eget/동작알림;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (fil_INDEKS < 0) { fejl_VÆRDI("event callback missing"); return; }
        aktuel_tråd = 0; Antal_tråde = 1; ramme_INDEKS = 0; tråd_status[0] = 1; ramme_Stak[0] = 0; ramme_lås[0] = starte_ramme[0] = 0; ændringsanmodning = false;
        for (int Loop_INDEKS = 0; Loop_INDEKS < 128; Loop_INDEKS++) { lokal_VÆRDI[Loop_INDEKS] = lokal_Type[Loop_INDEKS] = 0; }
        ramme_metode[0] = fil_INDEKS; ramme_placere[0] = metode_START[fil_INDEKS]; lokal_VÆRDI[0] = mål_mail; lokal_Type[0] = 2;
        if (hændelse_tal != 0) { lokal_VÆRDI[1] = hændelse_tal; lokal_Type[1] = 2; }
        사건중 = true; Udfør_kommando(); 사건중 = false;
    }
    static void skærmbillede_Events() {
        while (!fejl) {
            if (나중수 > 0) { int mål_mail = 나중실행[0], Dansk = 나중한국어[0]; for (int Loop_INDEKS = 1; Loop_INDEKS < 나중수; Loop_INDEKS++) { 나중실행[Loop_INDEKS - 1] = 나중실행[Loop_INDEKS]; 나중한국어[Loop_INDEKS - 1] = 나중한국어[Loop_INDEKS]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; udføre_hændelse(mål_mail, 0, Dansk != 0); continue; }
            if (bruger.skærmbillede_forbindelse(6, 0, 0, 0, 0, 0) == 0) return;
            int hændelse_tal = bruger.skærmbillede_forbindelse(5, 0, 0, 0, 0, 0); if (hændelse_tal == 0) continue;
            if (hændelse_tal < 0) { fejl_VÆRDI("GUI event I/O failed"); return; }
            int konto_VÆRDI = hændelse_tal & 65535; if (konto_VÆRDI < 1 || konto_VÆRDI > 32) continue; int objekt_referere = skærmbillede_referere[konto_VÆRDI - 1]; if (objekt_referere == 0) continue;
            if ((hændelse_tal & 65536) != 0) {
                if (heap_VÆRDI[objekt_referere + 10] != 0) heap_VÆRDI[objekt_referere + 9] = 0;
                if (heap_VÆRDI[objekt_referere + 10] == 3) for (int Loop_INDEKS = 0; Loop_INDEKS < 32; Loop_INDEKS++) if (skærmbillede_referere[Loop_INDEKS] != 0 && heap_VÆRDI[skærmbillede_referere[Loop_INDEKS]] == 24) bruger.skærmbillede_forbindelse(4, Loop_INDEKS + 1, 0, 0, 0, 0);
            } else if (heap_VÆRDI[objekt_referere + 4] != 0) {
                int Vigtigt_referere = tildel_Lager(29, 2); if (fejl) return; heap_VÆRDI[Vigtigt_referere + 2] = objekt_referere; heap_VÆRDI[Vigtigt_referere + 3] = heap_VÆRDI[objekt_referere + 12]; heap_referere[Vigtigt_referere + 2] = 1; udføre_hændelse(heap_VÆRDI[objekt_referere + 4], Vigtigt_referere, heap_VÆRDI[objekt_referere + 12] != 0);
            }
        }
    }
    public static int Kør_2() {
        if (bruger.인수개수() == 1 && 자바도구.같음(bruger.Argumenter(0), "-version")) {
            bruger.Skrive("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (bruger.인수개수() < 1) { bruger.Skrive("Usage: java CLASS [ARGS]\n"); return 2; }
        post_Hold_Definition = indlæse_Hold_Definition(vært_tegn(bruger.Argumenter(0))); if (fejl || post_Hold_Definition < 0) return 1;
        int indgangspunkt_VÆRDI = navn_metode(post_Hold_Definition, "Kør_2", "()V");
        boolean 한국어진입 = indgangspunkt_VÆRDI >= 0 && (metode_åbne[indgangspunkt_VÆRDI] & 9) == 9;
        if (!한국어진입) indgangspunkt_VÆRDI = navn_metode(post_Hold_Definition, "main", "([Ljava/lang/String;)V");
        if (indgangspunkt_VÆRDI < 0 || (metode_åbne[indgangspunkt_VÆRDI] & 9) != 9) fejl_VÆRDI("public static void Kør_2() or main(String[] args) required");
        if (fejl) return 1;
        int Argumenter = tildel_Lager(3, bruger.인수개수() - 1); matrixelement[Argumenter] = -1;
        for (int tal = 1; tal < bruger.인수개수() && !fejl; tal++) heap_VÆRDI[Argumenter + 1 + tal] = vært_tegn(bruger.Argumenter(tal));
        ramme_INDEKS = 0; ramme_metode[0] = indgangspunkt_VÆRDI; ramme_placere[0] = metode_START[indgangspunkt_VÆRDI]; lokal_VÆRDI[0] = 한국어진입 ? 0 : Argumenter; lokal_Type[0] = 한국어진입 ? 0 : 2;
        tråd_status[0] = 1; tråd_objekt[0] = tildel_Lager(13, 2);
        Udfør_kommando(); if (!fejl) skærmbillede_Events(); return fejl ? 1 : 0;
    }
}
