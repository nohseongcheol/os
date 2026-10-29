// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. Fil/operand_Stak/referere/gren 경계를 Udfør_kommando 중 검사한다. */
public final class 자바가상기계 {
    static int[] Fil = new int[16384], filnavn_sms = new int[64];
    static int[] konstant_tag = new int[512], 상가 = new int[512], konstant_SEKUND_VÆRDI = new int[512], streng_referere = new int[512];
    static int[] metode_navn_sms = new int[32], metode_Type = new int[32], metode_åbne = new int[32];
    static int[] metode_START = new int[32], metode_afslutte_et_opkald = new int[32], metode_Stak = new int[32], 함수지역 = new int[32];
    static int[] metode_argument_TÆL = new int[32], metode_argument_Type = new int[512], metode_returnere = new int[32];
    static int[] grænse_VÆRDI = new int[16384];
    static int[] lokal_VÆRDI = new int[4096], lokal_Type = new int[4096], operand_Stak_VÆRDI = new int[4096], operand_Stak_Type = new int[4096];
    static int[] ramme_metode = new int[32], ramme_placere = new int[32], ramme_Stak = new int[32];
    static int[] heap_VÆRDI = new int[8192];
    static int Størrelse, 읽기위치, konstant_TÆL, metode_TÆL, klassenavn, ramme_INDEKS = -1, heap_afslutte_et_opkald_placere = 1, returnere_Type;
    static boolean fejl;

    static void fejl_VÆRDI(String Ord_sms) {
        if (!fejl) { bruger.Skrive("JVM error: "); bruger.Skrive(Ord_sms); bruger.skrive_tegn_VÆRDI(10); }
        fejl = true;
    }
    static boolean klippe(int Kør_2, int varighed_VÆRDI) { return Kør_2 >= 0 && varighed_VÆRDI >= 0 && Kør_2 <= Størrelse - varighed_VÆRDI; }
    static int byte_VÆRDI() {
        if (!klippe(읽기위치, 1)) { fejl_VÆRDI("truncated class file"); return 0; }
        return Fil[읽기위치++];
    }
    static int 짧은수() { return byte_VÆRDI() << 8 | byte_VÆRDI(); }
    static int heltal() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int varighed_VÆRDI) { if (!klippe(읽기위치, varighed_VÆRDI)) fejl_VÆRDI("invalid attribute size"); else 읽기위치 += varighed_VÆRDI; }
    static boolean check_konstant(int tal, int 종류) {
        if (tal <= 0 || tal >= konstant_TÆL || konstant_tag[tal] != 종류) { fejl_VÆRDI("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean sms_område(int Kør_2, int varighed_VÆRDI, String Ord_sms) {
        if (!klippe(Kør_2, varighed_VÆRDI) || varighed_VÆRDI != Ord_sms.length()) return false;
        for (int tal = 0; tal < varighed_VÆRDI; tal++) if (Fil[Kør_2 + tal] != Ord_sms.charAt(tal)) return false;
        return true;
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
    static void springe_over_attribut() {
        int vare_TÆL = 짧은수();
        for (int tal = 0; tal < vare_TÆL && !fejl; tal++) { check_konstant(짧은수(), 1); 건너(heltal()); }
    }
    static int kommando_varighed(int VÆRDI) {
        if (VÆRDI == 16 || VÆRDI == 18 || VÆRDI == 21 || VÆRDI == 25 || VÆRDI == 54 || VÆRDI == 58 || VÆRDI == 188) return 2;
        if (VÆRDI == 17 || VÆRDI == 19 || VÆRDI == 132 || VÆRDI >= 153 && VÆRDI <= 167
            || VÆRDI >= 178 && VÆRDI <= 184 || VÆRDI == 187 || VÆRDI == 189 || VÆRDI == 192 || VÆRDI == 198 || VÆRDI == 199) return 3;
        if (VÆRDI >= 0 && VÆRDI <= 8 || VÆRDI >= 26 && VÆRDI <= 29 || VÆRDI >= 42 && VÆRDI <= 46 || VÆRDI == 50
            || VÆRDI >= 59 && VÆRDI <= 62 || VÆRDI >= 75 && VÆRDI <= 79 || VÆRDI == 83 || VÆRDI == 87 || VÆRDI == 89 || VÆRDI == 95
            || VÆRDI == 96 || VÆRDI == 100 || VÆRDI == 104 || VÆRDI == 108 || VÆRDI == 112 || VÆRDI == 116
            || VÆRDI == 120 || VÆRDI == 122 || VÆRDI == 124 || VÆRDI == 126 || VÆRDI == 128 || VÆRDI == 130
            || VÆRDI >= 145 && VÆRDI <= 147 || VÆRDI == 172 || VÆRDI == 176 || VÆRDI == 177 || VÆRDI == 190) return 1;
        return 0;
    }
    static void 클래스읽기() {
        if (heltal() != 0xcafebabe) fejl_VÆRDI("not a class file");
        int 부판 = 짧은수(), version_VÆRDI = 짧은수();
        if (version_VÆRDI < 45 || version_VÆRDI > 52 || 부판 != 0) fejl_VÆRDI("supported class versions: 45..52, minor 0");
        konstant_TÆL = 짧은수();
        if (konstant_TÆL < 1 || konstant_TÆL > 512) { fejl_VÆRDI("constant pool limit (511)"); return; }
        for (int tal = 1; tal < konstant_TÆL && !fejl; tal++) {
            int 종류 = byte_VÆRDI(); konstant_tag[tal] = 종류;
            if (종류 == 1) { konstant_SEKUND_VÆRDI[tal] = 짧은수(); 상가[tal] = 읽기위치; 건너(konstant_SEKUND_VÆRDI[tal]); }
            else if (종류 == 3) 상가[tal] = heltal();
            else if (종류 == 7 || 종류 == 8) 상가[tal] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[tal] = 짧은수(); konstant_SEKUND_VÆRDI[tal] = 짧은수(); }
            else fejl_VÆRDI("unsupported constant type");
        }
        int rettighed_VÆRDI = 짧은수();
        if ((rettighed_VÆRDI & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) fejl_VÆRDI("unsupported class flags");
        klassenavn = klassenavn_sms(짧은수());
        if (!Ord_sms(klassenavn_sms(짧은수()), "java/lang/Object")) fejl_VÆRDI("inheritance unsupported");
        if (짧은수() != 0) fejl_VÆRDI("interfaces unsupported");
        if (짧은수() != 0) fejl_VÆRDI("fields unsupported");
        metode_TÆL = 짧은수();
        if (metode_TÆL < 1 || metode_TÆL > 32) { fejl_VÆRDI("method count limit (32)"); return; }
        for (int tal = 0; tal < metode_TÆL && !fejl; tal++) {
            metode_åbne[tal] = 짧은수(); metode_navn_sms[tal] = 짧은수(); metode_Type[tal] = 짧은수();
            check_konstant(metode_navn_sms[tal], 1); 서술읽기(tal);
            if ((metode_åbne[tal] & (0x100 | 0x400 | 0x20)) != 0) fejl_VÆRDI("native, abstract and synchronized methods unsupported");
            if ((metode_åbne[tal] & 8) == 0 && !Ord_sms(metode_navn_sms[tal], "<init>")) fejl_VÆRDI("instance methods unsupported");
            if (Ord_sms(metode_navn_sms[tal], "<clinit>")) fejl_VÆRDI("class initializers unsupported");
            for (int frontvendt_VÆRDI = 0; frontvendt_VÆRDI < tal; frontvendt_VÆRDI++) if (afstemning_Ord(metode_navn_sms[frontvendt_VÆRDI], metode_navn_sms[tal]) && afstemning_Ord(metode_Type[frontvendt_VÆRDI], metode_Type[tal])) fejl_VÆRDI("duplicate method");
            int vare_TÆL = 짧은수();
            for (int attribut_VÆRDI = 0; attribut_VÆRDI < vare_TÆL && !fejl; attribut_VÆRDI++) {
                int Navn = 짧은수(), varighed_VÆRDI = heltal(), Kør_2 = 읽기위치;
                if (!klippe(Kør_2, varighed_VÆRDI)) { fejl_VÆRDI("truncated method attribute"); break; }
                if (Ord_sms(Navn, "Code")) {
                    if (metode_START[tal] != 0) fejl_VÆRDI("duplicate Code attribute");
                    metode_Stak[tal] = 짧은수(); 함수지역[tal] = 짧은수(); int KODE_varighed = heltal();
                    if (metode_Stak[tal] > 128 || 함수지역[tal] > 128 || 함수지역[tal] < metode_argument_TÆL[tal]
                        || KODE_varighed < 1 || KODE_varighed > 8192) fejl_VÆRDI("method memory limits exceeded");
                    metode_START[tal] = 읽기위치; 건너(KODE_varighed); metode_afslutte_et_opkald[tal] = 읽기위치;
                    if (짧은수() != 0) fejl_VÆRDI("exception handlers unsupported");
                    springe_over_attribut();
                    if (읽기위치 != Kør_2 + varighed_VÆRDI) fejl_VÆRDI("Code attribute size mismatch");
                } else 건너(varighed_VÆRDI);
            }
            if (metode_START[tal] == 0) fejl_VÆRDI("missing Code attribute");
            int udvidelsesstik_post = metode_START[tal];
            while (udvidelsesstik_post < metode_afslutte_et_opkald[tal] && !fejl) {
                int varighed_VÆRDI = kommando_varighed(Fil[udvidelsesstik_post]);
                if (varighed_VÆRDI == 0 || varighed_VÆRDI > metode_afslutte_et_opkald[tal] - udvidelsesstik_post) { fejl_VÆRDI("unsupported or truncated bytecode"); break; }
                grænse_VÆRDI[udvidelsesstik_post] = tal + 1; udvidelsesstik_post += varighed_VÆRDI;
            }
            // 실행하지 않는 경로에도 잘못된 gren 목적지를 허용하지 않는다.
            udvidelsesstik_post = metode_START[tal];
            while (udvidelsesstik_post < metode_afslutte_et_opkald[tal] && !fejl) {
                int VÆRDI = Fil[udvidelsesstik_post];
                if (VÆRDI >= 153 && VÆRDI <= 167 || VÆRDI == 198 || VÆRDI == 199) {
                    int destination_VÆRDI = udvidelsesstik_post + (short)(Fil[udvidelsesstik_post + 1] << 8 | Fil[udvidelsesstik_post + 2]);
                    if (destination_VÆRDI < metode_START[tal] || destination_VÆRDI >= metode_afslutte_et_opkald[tal] || grænse_VÆRDI[destination_VÆRDI] != tal + 1) fejl_VÆRDI("invalid branch target");
                }
                udvidelsesstik_post += kommando_varighed(VÆRDI);
            }
        }
        if (!fejl) springe_over_attribut();
        if (읽기위치 != Størrelse) fejl_VÆRDI("extra class file data");
    }
    static int tildel_Lager(int 종류, int varighed_VÆRDI) {
        if (varighed_VÆRDI < 0 || varighed_VÆRDI > heap_VÆRDI.length - heap_afslutte_et_opkald_placere - 2) { fejl_VÆRDI("object heap exhausted or negative array size"); return 0; }
        int referere = heap_afslutte_et_opkald_placere; heap_afslutte_et_opkald_placere += varighed_VÆRDI + 2; heap_VÆRDI[referere] = 종류; heap_VÆRDI[referere + 1] = varighed_VÆRDI;
        return referere;
    }
    static boolean objekt_VÆRDI(int referere, int 종류) {
        if (referere < 1 || referere >= heap_afslutte_et_opkald_placere - 1 || heap_VÆRDI[referere] != 종류) { fejl_VÆRDI("null or invalid object reference"); return false; }
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
        if (ramme_INDEKS == 31) { fejl_VÆRDI("call stack limit (32)"); return; }
        int Næste_vare = ramme_INDEKS + 1;
        for (int tal = 0; tal < 128; tal++) lokal_Type[Næste_vare * 128 + tal] = 0;
        for (int tal = metode_argument_TÆL[FUNKTION_VÆRDI] - 1; tal >= 0; tal--) {
            lokal_VÆRDI[Næste_vare * 128 + tal] = 빼기(metode_argument_Type[FUNKTION_VÆRDI * 16 + tal]); lokal_Type[Næste_vare * 128 + tal] = metode_argument_Type[FUNKTION_VÆRDI * 16 + tal];
        }
        ramme_INDEKS = Næste_vare; ramme_metode[ramme_INDEKS] = FUNKTION_VÆRDI; ramme_placere[ramme_INDEKS] = metode_START[FUNKTION_VÆRDI]; ramme_Stak[ramme_INDEKS] = 0;
    }
    static void returnere_KR(int Type_VÆRDI) {
        if (Type_VÆRDI != metode_returnere[ramme_metode[ramme_INDEKS]]) { fejl_VÆRDI("return type mismatch"); return; }
        int VÆRDI = Type_VÆRDI == 0 ? 0 : 빼기(Type_VÆRDI);
        ramme_INDEKS--; if (ramme_INDEKS >= 0 && Type_VÆRDI != 0) 넣기(VÆRDI, Type_VÆRDI);
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
                if (VÆRDI < 1 || VÆRDI > 127) { fejl_VÆRDI("file stream paths currently require ASCII"); return; }
                strøm_filnavn[udvidelsesstik_post] = VÆRDI;
            }
            strøm_filnavn[varighed_VÆRDI] = 0;
            int 서술자 = bruger.파일서술자열기(strøm_filnavn, Udgang ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { fejl_VÆRDI("FileNotFoundException: file open failed"); return; }
            heap_VÆRDI[strøm_VÆRDI + 2] = 서술자; heap_VÆRDI[strøm_VÆRDI + 3] = 1;
            return;
        }
        if (Kommando != 182) { fejl_VÆRDI("invalid file stream invocation"); return; }
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
            if (KR < -1) fejl_VÆRDI("IOException: read failed"); else 넣기(KR, 1);
        } else if (bruger.파일한바이트쓰기(서술자, VÆRDI) != 1) fejl_VÆRDI("IOException: write failed");
    }
    static void KALD_metode(int INDEKS, int Kommando) {
        if (!check_konstant(INDEKS, 10)) return;
        int ejer_VÆRDI = klassenavn_sms(상가[INDEKS]), Navn = referere_navn(konstant_SEKUND_VÆRDI[INDEKS]), format_VÆRDI = referencetype(konstant_SEKUND_VÆRDI[INDEKS]);
        if (fejl) return;
        if (afstemning_Ord(ejer_VÆRDI, klassenavn)) {
            if (Kommando != 184) { fejl_VÆRDI("only static user methods are supported"); return; }
            for (int tal = 0; tal < metode_TÆL; tal++) if (afstemning_Ord(Navn, metode_navn_sms[tal]) && afstemning_Ord(format_VÆRDI, metode_Type[tal])) {
                if ((metode_åbne[tal] & 8) == 0) fejl_VÆRDI("method is not static"); else 호출(tal);
                return;
            }
            fejl_VÆRDI("NoSuchMethodError"); return;
        }
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
        fejl_VÆRDI("unsupported library method");
    }
    static int MATRIX_udvidelsesstik(int referere, int sænket_skrift_VÆRDI, int Type_VÆRDI) {
        if (!objekt_VÆRDI(referere, Type_VÆRDI)) return 0;
        if (sænket_skrift_VÆRDI < 0 || sænket_skrift_VÆRDI >= heap_VÆRDI[referere + 1]) { fejl_VÆRDI("ArrayIndexOutOfBoundsException"); return 0; }
        return referere + 2 + sænket_skrift_VÆRDI;
    }
    static void Udfør_kommando() {
        int 남음 = 500000;
        while (ramme_INDEKS >= 0 && !fejl) {
            if (--남음 == 0) { fejl_VÆRDI("instruction limit (500000)"); break; }
            int Kør_2 = ramme_placere[ramme_INDEKS], VÆRDI = 명바();
            if (fejl) break;
            if (VÆRDI == 0) continue;
            if (VÆRDI == 1) { 넣기(0, 2); continue; }
            if (VÆRDI >= 2 && VÆRDI <= 8) { 넣기(VÆRDI - 3, 1); continue; }
            if (VÆRDI == 16) { 넣기((byte)명바(), 1); continue; }
            if (VÆRDI == 17) { 넣기((short)명짧(), 1); continue; }
            if (VÆRDI == 18 || VÆRDI == 19) {
                int tal = VÆRDI == 18 ? 명바() : 명짧();
                if (tal <= 0 || tal >= konstant_TÆL) fejl_VÆRDI("invalid ldc constant");
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
            if (VÆRDI == 46 || VÆRDI == 50) {
                int sænket_skrift_VÆRDI = 빼기(1), referere = 빼기(2), udvidelsesstik_post = MATRIX_udvidelsesstik(referere, sænket_skrift_VÆRDI, VÆRDI == 46 ? 2 : 3);
                if (!fejl) 넣기(heap_VÆRDI[udvidelsesstik_post], VÆRDI == 46 ? 1 : 2); continue;
            }
            if (VÆRDI == 79 || VÆRDI == 83) {
                int vare_element = 빼기(VÆRDI == 79 ? 1 : 2), sænket_skrift_VÆRDI = 빼기(1), referere = 빼기(2), udvidelsesstik_post = MATRIX_udvidelsesstik(referere, sænket_skrift_VÆRDI, VÆRDI == 79 ? 2 : 3);
                if (VÆRDI == 83 && vare_element != 0) objekt_VÆRDI(vare_element, 1);
                if (!fejl) heap_VÆRDI[udvidelsesstik_post] = vare_element; continue;
            }
            if (VÆRDI == 87) { 빼기(0); continue; }
            if (VÆRDI == 89) { int 가 = 빼기(0), Type_VÆRDI = returnere_Type; 넣기(가, Type_VÆRDI); 넣기(가, Type_VÆRDI); continue; }
            if (VÆRDI == 95) { int 가 = 빼기(0), 가형 = returnere_Type, SEKUND_operand = 빼기(0), SEKUND_operand_Type = returnere_Type; 넣기(가, 가형); 넣기(SEKUND_operand, SEKUND_operand_Type); continue; }
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
            if (VÆRDI == 178) {
                int tal = 명짧(); if (!check_konstant(tal, 9)) continue;
                if (!Ord_sms(klassenavn_sms(상가[tal]), "java/lang/System") || !Ord_sms(referere_navn(konstant_SEKUND_VÆRDI[tal]), "out")
                    || !Ord_sms(referencetype(konstant_SEKUND_VÆRDI[tal]), "Ljava/io/PrintStream;")) fejl_VÆRDI("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (VÆRDI == 182 || VÆRDI == 183 || VÆRDI == 184) { KALD_metode(명짧(), VÆRDI); continue; }
            if (VÆRDI == 187) {
                int Navn = klassenavn_sms(명짧());
                if (Ord_sms(Navn, "java/lang/StringBuilder")) 넣기(tildel_Lager(4, 1), 2);
                else if (Ord_sms(Navn, "java/io/FileInputStream") || Ord_sms(Navn, "java/io/FileOutputStream")) {
                    int referere = tildel_Lager(Ord_sms(Navn, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!fejl) { heap_VÆRDI[referere + 2] = -1; 넣기(referere, 2); }
                } else fejl_VÆRDI("unsupported object construction");
                continue;
            }
            if (VÆRDI == 188 || VÆRDI == 189) {
                if (VÆRDI == 188) { if (명바() != 10) fejl_VÆRDI("only int[] newarray is supported"); }
                else if (!Ord_sms(klassenavn_sms(명짧()), "java/lang/String")) fejl_VÆRDI("only String[] anewarray is supported");
                int varighed_VÆRDI = 빼기(1); 넣기(tildel_Lager(VÆRDI == 188 ? 2 : 3, varighed_VÆRDI), 2); continue;
            }
            if (VÆRDI == 190) {
                int referere = 빼기(2);
                if (referere < 1 || referere >= heap_afslutte_et_opkald_placere - 1 || (heap_VÆRDI[referere] != 2 && heap_VÆRDI[referere] != 3)) fejl_VÆRDI("null or invalid array");
                else 넣기(heap_VÆRDI[referere + 1], 1); continue;
            }
            if (VÆRDI == 192) {
                int Navn = klassenavn_sms(명짧()), referere = 빼기(2);
                if (!Ord_sms(Navn, "java/lang/String")) fejl_VÆRDI("unsupported checkcast");
                else if (referere != 0) objekt_VÆRDI(referere, 1);
                넣기(referere, 2); continue;
            }
            fejl_VÆRDI("unsupported bytecode");
        }
    }
    public static int Kør_2() {
        if (bruger.인수개수() == 1 && 자바도구.같음(bruger.Argumenter(0), "-version")) {
            bruger.Skrive("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (bruger.인수개수() < 1) { bruger.Skrive("Usage: java CLASS [ARGS]\n"); return 2; }
        int varighed_VÆRDI = 자바도구.Navn(filnavn_sms, bruger.Argumenter(0));
        if (varighed_VÆRDI < 1 || varighed_VÆRDI > 57) { bruger.Skrive("java: invalid class name\n"); return 2; }
        filnavn_sms[varighed_VÆRDI] = '.'; filnavn_sms[varighed_VÆRDI + 1] = 'c'; filnavn_sms[varighed_VÆRDI + 2] = 'l'; filnavn_sms[varighed_VÆRDI + 3] = 'a'; filnavn_sms[varighed_VÆRDI + 4] = 's'; filnavn_sms[varighed_VÆRDI + 5] = 's';
        Størrelse = bruger.파일읽기(filnavn_sms, Fil);
        if (Størrelse < 0) { bruger.Skrive("java: cannot read class: "); 자바도구.skrive_tal(Størrelse); bruger.skrive_tegn_VÆRDI(10); return 1; }
        클래스읽기(); if (fejl) return 1;
        int tegn_navn = konstant_sms(klassenavn);
        if (!fejl && heap_VÆRDI[tegn_navn + 1] != varighed_VÆRDI) fejl_VÆRDI("class name does not match file");
        for (int tal = 0; tal < varighed_VÆRDI && !fejl; tal++) if (heap_VÆRDI[tegn_navn + 2 + tal] != filnavn_sms[tal]) fejl_VÆRDI("class name does not match file");
        int indgangspunkt_VÆRDI = -1;
        for (int tal = 0; tal < metode_TÆL; tal++) if (Ord_sms(metode_navn_sms[tal], "main") && Ord_sms(metode_Type[tal], "([Ljava/lang/String;)V") && (metode_åbne[tal] & 9) == 9) indgangspunkt_VÆRDI = tal;
        if (indgangspunkt_VÆRDI < 0) fejl_VÆRDI("public static void main(String[] args) required");
        if (fejl) return 1;
        int Argumenter = tildel_Lager(3, bruger.인수개수() - 1);
        for (int tal = 1; tal < bruger.인수개수() && !fejl; tal++) heap_VÆRDI[Argumenter + 1 + tal] = vært_tegn(bruger.Argumenter(tal));
        ramme_INDEKS = 0; ramme_metode[0] = indgangspunkt_VÆRDI; ramme_placere[0] = metode_START[indgangspunkt_VÆRDI]; lokal_VÆRDI[0] = Argumenter; lokal_Type[0] = 2;
        Udfør_kommando(); return fejl ? 1 : 0;
    }
}
