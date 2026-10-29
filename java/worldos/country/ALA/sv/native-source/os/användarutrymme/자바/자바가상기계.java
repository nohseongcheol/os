// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. filnamn/operand_Stack/referens/gren 경계를 köra_kommando 중 검사한다. */
public final class 자바가상기계 {
    static int[] filnamn = new int[16384], filnamn_SMS = new int[64];
    static int[] konstant_tagg = new int[512], 상가 = new int[512], konstant_SEKUND_värde = new int[512], sträng_referens = new int[512];
    static int[] metod_namn_SMS = new int[32], metod_Typ = new int[32], metod_ansluta = new int[32];
    static int[] metod_START = new int[32], metod_avsluta = new int[32], metod_Stack = new int[32], 함수지역 = new int[32];
    static int[] metod_argument_ANTAL = new int[32], metod_argument_Typ = new int[512], metod_Retur = new int[32];
    static int[] gräns_värde = new int[16384];
    static int[] lokal_värde = new int[4096], lokal_Typ = new int[4096], operand_Stack_värde = new int[4096], operand_Stack_Typ = new int[4096];
    static int[] ram_metod = new int[32], ram_placera = new int[32], ram_Stack = new int[32];
    static int[] heap_värde = new int[8192];
    static int Storlek, läsa_placera, konstant_ANTAL, metod_ANTAL, klassnamn, ram_INDEX = -1, heap_avsluta_placera = 1, Retur_Typ;
    static boolean fel;

    static void fel_värde(String Ord_SMS) {
        if (!fel) { användarutrymme.Skriv("JVM error: "); användarutrymme.Skriv(Ord_SMS); användarutrymme.skriva_tecken_värde(10); }
        fel = true;
    }
    static boolean klipp(int Kör, int längd_värde) { return Kör >= 0 && längd_värde >= 0 && Kör <= Storlek - längd_värde; }
    static int byte_värde() {
        if (!klipp(läsa_placera, 1)) { fel_värde("truncated class file"); return 0; }
        return filnamn[läsa_placera++];
    }
    static int 짧은수() { return byte_värde() << 8 | byte_värde(); }
    static int heltal() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int längd_värde) { if (!klipp(läsa_placera, längd_värde)) fel_värde("invalid attribute size"); else läsa_placera += längd_värde; }
    static boolean check_konstant(int nummer, int variant_värde) {
        if (nummer <= 0 || nummer >= konstant_ANTAL || konstant_tagg[nummer] != variant_värde) { fel_värde("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean SMS_område(int Kör, int längd_värde, String Ord_SMS) {
        if (!klipp(Kör, längd_värde) || längd_värde != Ord_SMS.length()) return false;
        for (int nummer = 0; nummer < längd_värde; nummer++) if (filnamn[Kör + nummer] != Ord_SMS.charAt(nummer)) return false;
        return true;
    }
    static boolean Ord_SMS(int konstant_värde, String Ord_SMS) { return check_konstant(konstant_värde, 1) && SMS_område(상가[konstant_värde], konstant_SEKUND_värde[konstant_värde], Ord_SMS); }
    static boolean matchning_Ord(int 가, int SEKUND_operand) {
        if (!check_konstant(가, 1) || !check_konstant(SEKUND_operand, 1) || konstant_SEKUND_värde[가] != konstant_SEKUND_värde[SEKUND_operand]) return false;
        for (int nummer = 0; nummer < konstant_SEKUND_värde[가]; nummer++) if (filnamn[상가[가] + nummer] != filnamn[상가[SEKUND_operand] + nummer]) return false;
        return true;
    }
    static int klassnamn_SMS(int nummer) { return check_konstant(nummer, 7) && check_konstant(상가[nummer], 1) ? 상가[nummer] : 0; }
    static int referens_namn(int nummer) { return check_konstant(nummer, 12) && check_konstant(상가[nummer], 1) ? 상가[nummer] : 0; }
    static int referenstyp(int nummer) { return check_konstant(nummer, 12) && check_konstant(konstant_SEKUND_värde[nummer], 1) ? konstant_SEKUND_värde[nummer] : 0; }
    static int 서술형(int 끝, boolean 빈형) {
        if (läsa_placera >= 끝) { fel_värde("invalid descriptor"); return 0; }
        int värde = byte_värde();
        if (värde == 'V' && 빈형) return 0;
        if (värde == 'I' || värde == 'B' || värde == 'C' || värde == 'S' || värde == 'Z') return 1;
        if (värde == '[') { 서술형(끝, false); return 2; }
        if (värde == 'L') {
            int Kör = läsa_placera;
            while (läsa_placera < 끝 && filnamn[läsa_placera] != ';') läsa_placera++;
            if (läsa_placera == 끝 || läsa_placera == Kör) fel_värde("invalid reference descriptor");
            else läsa_placera++;
            return 2;
        }
        fel_värde("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int FUNKTION_värde) {
        int Föregående_objekt = läsa_placera, nummer = metod_Typ[FUNKTION_värde];
        if (!check_konstant(nummer, 1)) return;
        läsa_placera = 상가[nummer]; int 끝 = läsa_placera + konstant_SEKUND_värde[nummer];
        if (byte_värde() != '(') fel_värde("invalid method descriptor");
        int objekt_ANTAL = 0;
        while (!fel && läsa_placera < 끝 && filnamn[läsa_placera] != ')') {
            if (objekt_ANTAL == 16) { fel_värde("too many method arguments"); break; }
            metod_argument_Typ[FUNKTION_värde * 16 + objekt_ANTAL++] = 서술형(끝, false);
        }
        if (läsa_placera >= 끝 || byte_värde() != ')') fel_värde("invalid method descriptor");
        metod_Retur[FUNKTION_värde] = 서술형(끝, true); metod_argument_ANTAL[FUNKTION_värde] = objekt_ANTAL;
        if (läsa_placera != 끝) fel_värde("invalid method descriptor");
        läsa_placera = Föregående_objekt;
    }
    static void hoppa_över_attribut() {
        int objekt_ANTAL = 짧은수();
        for (int nummer = 0; nummer < objekt_ANTAL && !fel; nummer++) { check_konstant(짧은수(), 1); 건너(heltal()); }
    }
    static int kommando_längd(int värde) {
        if (värde == 16 || värde == 18 || värde == 21 || värde == 25 || värde == 54 || värde == 58 || värde == 188) return 2;
        if (värde == 17 || värde == 19 || värde == 132 || värde >= 153 && värde <= 167
            || värde >= 178 && värde <= 184 || värde == 187 || värde == 189 || värde == 192 || värde == 198 || värde == 199) return 3;
        if (värde >= 0 && värde <= 8 || värde >= 26 && värde <= 29 || värde >= 42 && värde <= 46 || värde == 50
            || värde >= 59 && värde <= 62 || värde >= 75 && värde <= 79 || värde == 83 || värde == 87 || värde == 89 || värde == 95
            || värde == 96 || värde == 100 || värde == 104 || värde == 108 || värde == 112 || värde == 116
            || värde == 120 || värde == 122 || värde == 124 || värde == 126 || värde == 128 || värde == 130
            || värde >= 145 && värde <= 147 || värde == 172 || värde == 176 || värde == 177 || värde == 190) return 1;
        return 0;
    }
    static void läsa_Kurs() {
        if (heltal() != 0xcafebabe) fel_värde("not a class file");
        int 부판 = 짧은수(), version_värde = 짧은수();
        if (version_värde < 45 || version_värde > 52 || 부판 != 0) fel_värde("supported class versions: 45..52, minor 0");
        konstant_ANTAL = 짧은수();
        if (konstant_ANTAL < 1 || konstant_ANTAL > 512) { fel_värde("constant pool limit (511)"); return; }
        for (int nummer = 1; nummer < konstant_ANTAL && !fel; nummer++) {
            int variant_värde = byte_värde(); konstant_tagg[nummer] = variant_värde;
            if (variant_värde == 1) { konstant_SEKUND_värde[nummer] = 짧은수(); 상가[nummer] = läsa_placera; 건너(konstant_SEKUND_värde[nummer]); }
            else if (variant_värde == 3) 상가[nummer] = heltal();
            else if (variant_värde == 7 || variant_värde == 8) 상가[nummer] = 짧은수();
            else if (variant_värde == 9 || variant_värde == 10 || variant_värde == 12) { 상가[nummer] = 짧은수(); konstant_SEKUND_värde[nummer] = 짧은수(); }
            else fel_värde("unsupported constant type");
        }
        int behörighet_värde = 짧은수();
        if ((behörighet_värde & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) fel_värde("unsupported class flags");
        klassnamn = klassnamn_SMS(짧은수());
        if (!Ord_SMS(klassnamn_SMS(짧은수()), "java/lang/Object")) fel_värde("inheritance unsupported");
        if (짧은수() != 0) fel_värde("interfaces unsupported");
        if (짧은수() != 0) fel_värde("fields unsupported");
        metod_ANTAL = 짧은수();
        if (metod_ANTAL < 1 || metod_ANTAL > 32) { fel_värde("method count limit (32)"); return; }
        for (int nummer = 0; nummer < metod_ANTAL && !fel; nummer++) {
            metod_ansluta[nummer] = 짧은수(); metod_namn_SMS[nummer] = 짧은수(); metod_Typ[nummer] = 짧은수();
            check_konstant(metod_namn_SMS[nummer], 1); 서술읽기(nummer);
            if ((metod_ansluta[nummer] & (0x100 | 0x400 | 0x20)) != 0) fel_värde("native, abstract and synchronized methods unsupported");
            if ((metod_ansluta[nummer] & 8) == 0 && !Ord_SMS(metod_namn_SMS[nummer], "<init>")) fel_värde("instance methods unsupported");
            if (Ord_SMS(metod_namn_SMS[nummer], "<clinit>")) fel_värde("class initializers unsupported");
            for (int framåtvänd_värde = 0; framåtvänd_värde < nummer; framåtvänd_värde++) if (matchning_Ord(metod_namn_SMS[framåtvänd_värde], metod_namn_SMS[nummer]) && matchning_Ord(metod_Typ[framåtvänd_värde], metod_Typ[nummer])) fel_värde("duplicate method");
            int objekt_ANTAL = 짧은수();
            for (int attribut_värde = 0; attribut_värde < objekt_ANTAL && !fel; attribut_värde++) {
                int Namn = 짧은수(), längd_värde = heltal(), Kör = läsa_placera;
                if (!klipp(Kör, längd_värde)) { fel_värde("truncated method attribute"); break; }
                if (Ord_SMS(Namn, "Code")) {
                    if (metod_START[nummer] != 0) fel_värde("duplicate Code attribute");
                    metod_Stack[nummer] = 짧은수(); 함수지역[nummer] = 짧은수(); int KOD_längd = heltal();
                    if (metod_Stack[nummer] > 128 || 함수지역[nummer] > 128 || 함수지역[nummer] < metod_argument_ANTAL[nummer]
                        || KOD_längd < 1 || KOD_längd > 8192) fel_värde("method memory limits exceeded");
                    metod_START[nummer] = läsa_placera; 건너(KOD_längd); metod_avsluta[nummer] = läsa_placera;
                    if (짧은수() != 0) fel_värde("exception handlers unsupported");
                    hoppa_över_attribut();
                    if (läsa_placera != Kör + längd_värde) fel_värde("Code attribute size mismatch");
                } else 건너(längd_värde);
            }
            if (metod_START[nummer] == 0) fel_värde("missing Code attribute");
            int fack_post = metod_START[nummer];
            while (fack_post < metod_avsluta[nummer] && !fel) {
                int längd_värde = kommando_längd(filnamn[fack_post]);
                if (längd_värde == 0 || längd_värde > metod_avsluta[nummer] - fack_post) { fel_värde("unsupported or truncated bytecode"); break; }
                gräns_värde[fack_post] = nummer + 1; fack_post += längd_värde;
            }
            // 실행하지 않는 경로에도 잘못된 gren 목적지를 허용하지 않는다.
            fack_post = metod_START[nummer];
            while (fack_post < metod_avsluta[nummer] && !fel) {
                int värde = filnamn[fack_post];
                if (värde >= 153 && värde <= 167 || värde == 198 || värde == 199) {
                    int mål_värde = fack_post + (short)(filnamn[fack_post + 1] << 8 | filnamn[fack_post + 2]);
                    if (mål_värde < metod_START[nummer] || mål_värde >= metod_avsluta[nummer] || gräns_värde[mål_värde] != nummer + 1) fel_värde("invalid branch target");
                }
                fack_post += kommando_längd(värde);
            }
        }
        if (!fel) hoppa_över_attribut();
        if (läsa_placera != Storlek) fel_värde("extra class file data");
    }
    static int allokera_minne(int variant_värde, int längd_värde) {
        if (längd_värde < 0 || längd_värde > heap_värde.length - heap_avsluta_placera - 2) { fel_värde("object heap exhausted or negative array size"); return 0; }
        int referens = heap_avsluta_placera; heap_avsluta_placera += längd_värde + 2; heap_värde[referens] = variant_värde; heap_värde[referens + 1] = längd_värde;
        return referens;
    }
    static boolean objekt_värde(int referens, int variant_värde) {
        if (referens < 1 || referens >= heap_avsluta_placera - 1 || heap_värde[referens] != variant_värde) { fel_värde("null or invalid object reference"); return false; }
        return true;
    }
    static int konstant_SMS(int INDEX) {
        if (!check_konstant(INDEX, 1)) return 0;
        if (sträng_referens[INDEX] != 0) return sträng_referens[INDEX];
        int referens = allokera_minne(1, konstant_SEKUND_värde[INDEX]); if (fel) return 0;
        int 끝 = 상가[INDEX] + konstant_SEKUND_värde[INDEX], nummer = 상가[INDEX], längd_värde = 0;
        while (nummer < 끝 && !fel) {
            int värde = filnamn[nummer++];
            if (värde == 0) fel_värde("invalid modified UTF-8");
            else if (värde >= 192 && värde <= 223 && nummer < 끝) {
                int Nästa_objekt = filnamn[nummer++];
                if ((Nästa_objekt & 192) != 128) fel_värde("invalid modified UTF-8");
                värde = (värde & 31) << 6 | Nästa_objekt & 63;
                if (värde != 0 && värde < 128) fel_värde("overlong modified UTF-8");
            } else if (värde >= 224 && värde <= 239 && nummer + 1 < 끝) {
                int 가 = filnamn[nummer++], SEKUND_operand = filnamn[nummer++];
                if ((가 & 192) != 128 || (SEKUND_operand & 192) != 128) fel_värde("invalid modified UTF-8");
                värde = (värde & 15) << 12 | (가 & 63) << 6 | SEKUND_operand & 63;
                if (värde < 2048) fel_värde("overlong modified UTF-8");
            } else if (värde >= 128) fel_värde("invalid modified UTF-8");
            heap_värde[referens + 2 + längd_värde++] = värde;
        }
        heap_värde[referens + 1] = längd_värde; sträng_referens[INDEX] = referens; return referens;
    }
    static int värd_tecken(String värde) {
        int referens = allokera_minne(1, värde.length()); if (fel) return 0;
        for (int nummer = 0; nummer < värde.length(); nummer++) heap_värde[referens + 2 + nummer] = värde.charAt(nummer);
        return referens;
    }
    static void skriva_SMS(int referens) {
        if (referens == 0) { användarutrymme.Skriv("null"); return; }
        if (!objekt_värde(referens, 1)) return;
        for (int nummer = 0; nummer < heap_värde[referens + 1]; nummer++) användarutrymme.skriva_tecken_värde(heap_värde[referens + 2 + nummer]);
    }
    static int siffra_tecken(int värde) {
        int referens = allokera_minne(1, 11); if (fel) return 0;
        int längd_värde = 0;
        if (värde < 0) heap_värde[referens + 2 + längd_värde++] = '-'; else värde = -värde;
        int positionsindex = 1000000000; boolean Kör = false;
        while (positionsindex != 0) {
            int nummer = -(värde / positionsindex);
            if (nummer != 0 || Kör || positionsindex == 1) { heap_värde[referens + 2 + längd_värde++] = '0' + nummer; Kör = true; }
            värde %= positionsindex; positionsindex /= 10;
        }
        heap_värde[referens + 1] = längd_värde; return referens;
    }
    static int 정수해독(int referens) {
        if (!objekt_värde(referens, 1)) return 0;
        int längd_värde = heap_värde[referens + 1], nummer = 0, värde = 0; boolean 음수 = false;
        if (längd_värde > 0 && (heap_värde[referens + 2] == '-' || heap_värde[referens + 2] == '+')) { 음수 = heap_värde[referens + 2] == '-'; nummer++; }
        if (nummer == längd_värde) fel_värde("NumberFormatException");
        for (; nummer < längd_värde && !fel; nummer++) {
            int siffra_värde = heap_värde[referens + 2 + nummer] - '0';
            if (siffra_värde < 0 || siffra_värde > 9 || värde < -214748364 || värde == -214748364 && siffra_värde > (음수 ? 8 : 7)) fel_värde("NumberFormatException");
            värde = värde * 10 - siffra_värde;
        }
        return 음수 ? värde : -värde;
    }
    static void 넣기(int värde, int Typ_värde) {
        if (fel) return;
        if (ram_INDEX < 0 || ram_Stack[ram_INDEX] >= metod_Stack[ram_metod[ram_INDEX]]) { fel_värde("operand stack overflow"); return; }
        int fack_post = ram_INDEX * 128 + ram_Stack[ram_INDEX]++; operand_Stack_värde[fack_post] = värde; operand_Stack_Typ[fack_post] = Typ_värde;
    }
    static int 빼기(int Typ_värde) {
        if (fel) return 0;
        if (ram_INDEX < 0 || ram_Stack[ram_INDEX] < 1) { fel_värde("operand stack underflow"); return 0; }
        int fack_post = ram_INDEX * 128 + --ram_Stack[ram_INDEX]; Retur_Typ = operand_Stack_Typ[fack_post];
        if (Typ_värde != 0 && Retur_Typ != Typ_värde) fel_värde("operand type mismatch");
        return operand_Stack_värde[fack_post];
    }
    static void läsa_lokal(int INDEX, int Typ_värde) {
        if (INDEX >= 함수지역[ram_metod[ram_INDEX]] || INDEX < 0 || lokal_Typ[ram_INDEX * 128 + INDEX] != Typ_värde) { fel_värde("invalid or uninitialized local"); return; }
        넣기(lokal_värde[ram_INDEX * 128 + INDEX], Typ_värde);
    }
    static void skriva_lokal(int INDEX, int Typ_värde) {
        if (INDEX >= 함수지역[ram_metod[ram_INDEX]] || INDEX < 0) { fel_värde("local index out of range"); return; }
        int värde = 빼기(Typ_värde); lokal_värde[ram_INDEX * 128 + INDEX] = värde; lokal_Typ[ram_INDEX * 128 + INDEX] = Typ_värde;
    }
    static int läsa_OP_kod_byte() {
        int position = ram_placera[ram_INDEX];
        if (position < metod_START[ram_metod[ram_INDEX]] || position >= metod_avsluta[ram_metod[ram_INDEX]]) { fel_värde("instruction pointer out of range"); return 0; }
        ram_placera[ram_INDEX]++; return filnamn[position];
    }
    static int 명짧() { return läsa_OP_kod_byte() << 8 | läsa_OP_kod_byte(); }
    static void flytta_värde(int position) {
        int FUNKTION_värde = ram_metod[ram_INDEX];
        if (position < metod_START[FUNKTION_värde] || position >= metod_avsluta[FUNKTION_värde] || gräns_värde[position] != FUNKTION_värde + 1) fel_värde("invalid branch target");
        else ram_placera[ram_INDEX] = position;
    }
    static void 호출(int FUNKTION_värde) {
        if (ram_INDEX == 31) { fel_värde("call stack limit (32)"); return; }
        int Nästa_objekt = ram_INDEX + 1;
        for (int nummer = 0; nummer < 128; nummer++) lokal_Typ[Nästa_objekt * 128 + nummer] = 0;
        for (int nummer = metod_argument_ANTAL[FUNKTION_värde] - 1; nummer >= 0; nummer--) {
            lokal_värde[Nästa_objekt * 128 + nummer] = 빼기(metod_argument_Typ[FUNKTION_värde * 16 + nummer]); lokal_Typ[Nästa_objekt * 128 + nummer] = metod_argument_Typ[FUNKTION_värde * 16 + nummer];
        }
        ram_INDEX = Nästa_objekt; ram_metod[ram_INDEX] = FUNKTION_värde; ram_placera[ram_INDEX] = metod_START[FUNKTION_värde]; ram_Stack[ram_INDEX] = 0;
    }
    static void Retur_KR(int Typ_värde) {
        if (Typ_värde != metod_Retur[ram_metod[ram_INDEX]]) { fel_värde("return type mismatch"); return; }
        int värde = Typ_värde == 0 ? 0 : 빼기(Typ_värde);
        ram_INDEX--; if (ram_INDEX >= 0 && Typ_värde != 0) 넣기(värde, Typ_värde);
    }
    static int[] flöde_filnamn = new int[64];
    static void fil_flöde_ring(int ägare_värde, int Namn, int format_värde, int kommando) {
        boolean utmatningsposition = Ord_SMS(ägare_värde, "java/io/FileOutputStream");
        int variant_värde = utmatningsposition ? 6 : 5;
        if (kommando == 183 && Ord_SMS(Namn, "<init>")) {
            boolean 이어 = false;
            if (utmatningsposition && Ord_SMS(format_värde, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Ord_SMS(format_värde, "(Ljava/lang/String;)V")) { fel_värde("unsupported file stream constructor"); return; }
            int fil_post_namn = 빼기(2), flöde_värde = 빼기(2);
            if (!objekt_värde(fil_post_namn, 1) || !objekt_värde(flöde_värde, variant_värde) || fel) return;
            if (heap_värde[flöde_värde + 3] != 0) { fel_värde("file stream already initialized"); return; }
            int längd_värde = heap_värde[fil_post_namn + 1];
            if (längd_värde < 1 || längd_värde > 63) { fel_värde("invalid file name length"); return; }
            for (int fack_post = 0; fack_post < längd_värde; fack_post++) {
                int värde = heap_värde[fil_post_namn + 2 + fack_post];
                if (värde < 1 || värde > 127) { fel_värde("file stream paths currently require ASCII"); return; }
                flöde_filnamn[fack_post] = värde;
            }
            flöde_filnamn[längd_värde] = 0;
            int 서술자 = användarutrymme.파일서술자열기(flöde_filnamn, utmatningsposition ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { fel_värde("FileNotFoundException: file open failed"); return; }
            heap_värde[flöde_värde + 2] = 서술자; heap_värde[flöde_värde + 3] = 1;
            return;
        }
        if (kommando != 182) { fel_värde("invalid file stream invocation"); return; }
        int Åtgärd = -1, värde = 0;
        if (Ord_SMS(Namn, "close") && Ord_SMS(format_värde, "()V")) Åtgärd = 0;
        if (!utmatningsposition && Ord_SMS(Namn, "read") && Ord_SMS(format_värde, "()I")) Åtgärd = 1;
        if (utmatningsposition && Ord_SMS(Namn, "write") && Ord_SMS(format_värde, "(I)V")) { Åtgärd = 2; värde = 빼기(1); }
        if (Åtgärd < 0) { fel_värde("unsupported file stream method"); return; }
        int flöde_värde = 빼기(2);
        if (!objekt_värde(flöde_värde, variant_värde) || fel) return;
        if (heap_värde[flöde_värde + 3] == 0) { fel_värde("uninitialized file stream"); return; }
        int 서술자 = heap_värde[flöde_värde + 2];
        if (Åtgärd == 0) {
            if (서술자 >= 0 && användarutrymme.파일서술자닫기(서술자) < 0) fel_värde("IOException: close failed");
            heap_värde[flöde_värde + 2] = -1; return;
        }
        if (서술자 < 0) { fel_värde("IOException: stream closed"); return; }
        if (Åtgärd == 1) {
            int RESULTAT = användarutrymme.파일한바이트읽기(서술자);
            if (RESULTAT < -1) fel_värde("IOException: read failed"); else 넣기(RESULTAT, 1);
        } else if (användarutrymme.파일한바이트쓰기(서술자, värde) != 1) fel_värde("IOException: write failed");
    }
    static void ring_metod(int INDEX, int kommando) {
        if (!check_konstant(INDEX, 10)) return;
        int ägare_värde = klassnamn_SMS(상가[INDEX]), Namn = referens_namn(konstant_SEKUND_värde[INDEX]), format_värde = referenstyp(konstant_SEKUND_värde[INDEX]);
        if (fel) return;
        if (matchning_Ord(ägare_värde, klassnamn)) {
            if (kommando != 184) { fel_värde("only static user methods are supported"); return; }
            for (int nummer = 0; nummer < metod_ANTAL; nummer++) if (matchning_Ord(Namn, metod_namn_SMS[nummer]) && matchning_Ord(format_värde, metod_Typ[nummer])) {
                if ((metod_ansluta[nummer] & 8) == 0) fel_värde("method is not static"); else 호출(nummer);
                return;
            }
            fel_värde("NoSuchMethodError"); return;
        }
        if (Ord_SMS(ägare_värde, "java/io/FileInputStream") || Ord_SMS(ägare_värde, "java/io/FileOutputStream")) {
            fil_flöde_ring(ägare_värde, Namn, format_värde, kommando); return;
        }
        if (kommando == 184 && Ord_SMS(ägare_värde, "java/lang/Integer") && Ord_SMS(Namn, "parseInt") && Ord_SMS(format_värde, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (kommando == 182 && Ord_SMS(ägare_värde, "java/io/PrintStream") && (Ord_SMS(Namn, "println") || Ord_SMS(Namn, "print"))) {
            int Typ_värde = 0, värde = 0;
            if (Ord_SMS(format_värde, "(I)V")) { Typ_värde = 1; värde = 빼기(1); }
            else if (Ord_SMS(format_värde, "(Z)V")) { Typ_värde = 2; värde = 빼기(1); }
            else if (Ord_SMS(format_värde, "(C)V")) { Typ_värde = 3; värde = 빼기(1); }
            else if (Ord_SMS(format_värde, "(Ljava/lang/String;)V")) { Typ_värde = 4; värde = 빼기(2); }
            else if (!Ord_SMS(format_värde, "()V") || !Ord_SMS(Namn, "println")) fel_värde("unsupported print descriptor");
            if (빼기(2) != -1) fel_värde("invalid PrintStream receiver");
            if (fel) return;
            if (Typ_värde == 1) 자바도구.skriva_nummer(värde);
            if (Typ_värde == 2) användarutrymme.Skriv(värde == 0 ? "false" : "true");
            if (Typ_värde == 3) användarutrymme.skriva_tecken_värde(värde & 65535);
            if (Typ_värde == 4) skriva_SMS(värde);
            if (Ord_SMS(Namn, "println")) användarutrymme.skriva_tecken_värde(10);
            return;
        }
        if (kommando == 182 && Ord_SMS(ägare_värde, "java/lang/String")) {
            if (Ord_SMS(Namn, "length") && Ord_SMS(format_värde, "()I")) {
                int referens = 빼기(2); if (objekt_värde(referens, 1)) 넣기(heap_värde[referens + 1], 1); return;
            }
            if (Ord_SMS(Namn, "charAt") && Ord_SMS(format_värde, "(I)C")) {
                int nedsänkt_text_värde = 빼기(1), referens = 빼기(2);
                if (objekt_värde(referens, 1)) {
                    if (nedsänkt_text_värde < 0 || nedsänkt_text_värde >= heap_värde[referens + 1]) fel_värde("StringIndexOutOfBoundsException"); else 넣기(heap_värde[referens + 2 + nedsänkt_text_värde], 1);
                }
                return;
            }
        }
        if (Ord_SMS(ägare_värde, "java/lang/StringBuilder")) {
            if (kommando == 183 && Ord_SMS(Namn, "<init>") && Ord_SMS(format_värde, "()V")) { objekt_värde(빼기(2), 4); return; }
            if (kommando == 182 && Ord_SMS(Namn, "toString") && Ord_SMS(format_värde, "()Ljava/lang/String;")) {
                int referens = 빼기(2); if (objekt_värde(referens, 4)) 넣기(heap_värde[referens + 2] == 0 ? värd_tecken("") : heap_värde[referens + 2], 2); return;
            }
            if (kommando == 182 && Ord_SMS(Namn, "append")) {
                int text = 0;
                if (Ord_SMS(format_värde, "(I)Ljava/lang/StringBuilder;")) text = siffra_tecken(빼기(1));
                else if (Ord_SMS(format_värde, "(Z)Ljava/lang/StringBuilder;")) text = värd_tecken(빼기(1) == 0 ? "false" : "true");
                else if (Ord_SMS(format_värde, "(C)Ljava/lang/StringBuilder;")) {
                    int värde = 빼기(1); text = allokera_minne(1, 1); if (!fel) heap_värde[text + 2] = värde & 65535;
                }
                else if (Ord_SMS(format_värde, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { text = 빼기(2); if (text == 0) text = värd_tecken("null"); }
                else { fel_värde("unsupported StringBuilder append"); return; }
                int referens = 빼기(2); if (!objekt_värde(referens, 4) || !objekt_värde(text, 1)) return;
                int framåtvänd_värde = heap_värde[referens + 2], framåtvänd_värde_längd = framåtvänd_värde == 0 ? 0 : heap_värde[framåtvänd_värde + 1], BACK_värde_längd = heap_värde[text + 1];
                int 새글 = allokera_minne(1, framåtvänd_värde_längd + BACK_värde_längd); if (fel) return;
                for (int nummer = 0; nummer < framåtvänd_värde_längd; nummer++) heap_värde[새글 + 2 + nummer] = heap_värde[framåtvänd_värde + 2 + nummer];
                for (int nummer = 0; nummer < BACK_värde_längd; nummer++) heap_värde[새글 + 2 + framåtvänd_värde_längd + nummer] = heap_värde[text + 2 + nummer];
                heap_värde[referens + 2] = 새글; 넣기(referens, 2); return;
            }
        }
        fel_värde("unsupported library method");
    }
    static int MATRIS_fack(int referens, int nedsänkt_text_värde, int Typ_värde) {
        if (!objekt_värde(referens, Typ_värde)) return 0;
        if (nedsänkt_text_värde < 0 || nedsänkt_text_värde >= heap_värde[referens + 1]) { fel_värde("ArrayIndexOutOfBoundsException"); return 0; }
        return referens + 2 + nedsänkt_text_värde;
    }
    static void köra_kommando() {
        int 남음 = 500000;
        while (ram_INDEX >= 0 && !fel) {
            if (--남음 == 0) { fel_värde("instruction limit (500000)"); break; }
            int Kör = ram_placera[ram_INDEX], värde = läsa_OP_kod_byte();
            if (fel) break;
            if (värde == 0) continue;
            if (värde == 1) { 넣기(0, 2); continue; }
            if (värde >= 2 && värde <= 8) { 넣기(värde - 3, 1); continue; }
            if (värde == 16) { 넣기((byte)läsa_OP_kod_byte(), 1); continue; }
            if (värde == 17) { 넣기((short)명짧(), 1); continue; }
            if (värde == 18 || värde == 19) {
                int nummer = värde == 18 ? läsa_OP_kod_byte() : 명짧();
                if (nummer <= 0 || nummer >= konstant_ANTAL) fel_värde("invalid ldc constant");
                else if (konstant_tagg[nummer] == 3) 넣기(상가[nummer], 1);
                else if (konstant_tagg[nummer] == 8) 넣기(konstant_SMS(상가[nummer]), 2);
                else fel_värde("unsupported ldc constant");
                continue;
            }
            if (värde == 21 || värde == 25) { läsa_lokal(läsa_OP_kod_byte(), värde == 21 ? 1 : 2); continue; }
            if (värde >= 26 && värde <= 29) { läsa_lokal(värde - 26, 1); continue; }
            if (värde >= 42 && värde <= 45) { läsa_lokal(värde - 42, 2); continue; }
            if (värde == 54 || värde == 58) { skriva_lokal(läsa_OP_kod_byte(), värde == 54 ? 1 : 2); continue; }
            if (värde >= 59 && värde <= 62) { skriva_lokal(värde - 59, 1); continue; }
            if (värde >= 75 && värde <= 78) { skriva_lokal(värde - 75, 2); continue; }
            if (värde == 46 || värde == 50) {
                int nedsänkt_text_värde = 빼기(1), referens = 빼기(2), fack_post = MATRIS_fack(referens, nedsänkt_text_värde, värde == 46 ? 2 : 3);
                if (!fel) 넣기(heap_värde[fack_post], värde == 46 ? 1 : 2); continue;
            }
            if (värde == 79 || värde == 83) {
                int objekt_element = 빼기(värde == 79 ? 1 : 2), nedsänkt_text_värde = 빼기(1), referens = 빼기(2), fack_post = MATRIS_fack(referens, nedsänkt_text_värde, värde == 79 ? 2 : 3);
                if (värde == 83 && objekt_element != 0) objekt_värde(objekt_element, 1);
                if (!fel) heap_värde[fack_post] = objekt_element; continue;
            }
            if (värde == 87) { 빼기(0); continue; }
            if (värde == 89) { int 가 = 빼기(0), Typ_värde = Retur_Typ; 넣기(가, Typ_värde); 넣기(가, Typ_värde); continue; }
            if (värde == 95) { int 가 = 빼기(0), 가형 = Retur_Typ, SEKUND_operand = 빼기(0), SEKUND_operand_Typ = Retur_Typ; 넣기(가, 가형); 넣기(SEKUND_operand, SEKUND_operand_Typ); continue; }
            if (värde == 96 || värde == 100 || värde == 104 || värde == 108 || värde == 112 || värde == 120
                || värde == 122 || värde == 124 || värde == 126 || värde == 128 || värde == 130) {
                int SEKUND_operand = 빼기(1), 가 = 빼기(1), RESULTAT = 0;
                if ((värde == 108 || värde == 112) && SEKUND_operand == 0) { fel_värde("ArithmeticException: / by zero"); continue; }
                if (värde == 96) RESULTAT = 가 + SEKUND_operand;
                if (värde == 100) RESULTAT = 가 - SEKUND_operand;
                if (värde == 104) RESULTAT = 가 * SEKUND_operand;
                if (värde == 108) RESULTAT = 가 / SEKUND_operand;
                if (värde == 112) RESULTAT = 가 % SEKUND_operand;
                if (värde == 120) RESULTAT = 가 << SEKUND_operand;
                if (värde == 122) RESULTAT = 가 >> SEKUND_operand;
                if (värde == 124) RESULTAT = 가 >>> SEKUND_operand;
                if (värde == 126) RESULTAT = 가 & SEKUND_operand;
                if (värde == 128) RESULTAT = 가 | SEKUND_operand;
                if (värde == 130) RESULTAT = 가 ^ SEKUND_operand;
                넣기(RESULTAT, 1); continue;
            }
            if (värde == 116) { 넣기(-빼기(1), 1); continue; }
            if (värde == 132) {
                int lokal_scope = läsa_OP_kod_byte(), inkrement_steg = (byte)läsa_OP_kod_byte(); läsa_lokal(lokal_scope, 1); 넣기(빼기(1) + inkrement_steg, 1); skriva_lokal(lokal_scope, 1); continue;
            }
            if (värde >= 145 && värde <= 147) {
                int nummer = 빼기(1); 넣기(värde == 145 ? (byte)nummer : värde == 146 ? (char)nummer : (short)nummer, 1); continue;
            }
            if (värde >= 153 && värde <= 167 || värde == 198 || värde == 199) {
                int mål_värde = Kör + (short)명짧(); boolean 갈까 = värde == 167;
                if (värde >= 153 && värde <= 158) {
                    int nummer = 빼기(1); 갈까 = värde == 153 ? nummer == 0 : värde == 154 ? nummer != 0 : värde == 155 ? nummer < 0 : värde == 156 ? nummer >= 0 : värde == 157 ? nummer > 0 : nummer <= 0;
                } else if (värde >= 159 && värde <= 166) {
                    int SEKUND_operand = 빼기(värde >= 165 ? 2 : 1), 가 = 빼기(värde >= 165 ? 2 : 1);
                    갈까 = värde == 159 || värde == 165 ? 가 == SEKUND_operand : värde == 160 || värde == 166 ? 가 != SEKUND_operand : värde == 161 ? 가 < SEKUND_operand : värde == 162 ? 가 >= SEKUND_operand : värde == 163 ? 가 > SEKUND_operand : 가 <= SEKUND_operand;
                } else if (värde == 198 || värde == 199) { int nummer = 빼기(2); 갈까 = värde == 198 ? nummer == 0 : nummer != 0; }
                if (갈까) flytta_värde(mål_värde); continue;
            }
            if (värde == 172 || värde == 176 || värde == 177) { Retur_KR(värde == 172 ? 1 : värde == 176 ? 2 : 0); continue; }
            if (värde == 178) {
                int nummer = 명짧(); if (!check_konstant(nummer, 9)) continue;
                if (!Ord_SMS(klassnamn_SMS(상가[nummer]), "java/lang/System") || !Ord_SMS(referens_namn(konstant_SEKUND_värde[nummer]), "out")
                    || !Ord_SMS(referenstyp(konstant_SEKUND_värde[nummer]), "Ljava/io/PrintStream;")) fel_värde("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (värde == 182 || värde == 183 || värde == 184) { ring_metod(명짧(), värde); continue; }
            if (värde == 187) {
                int Namn = klassnamn_SMS(명짧());
                if (Ord_SMS(Namn, "java/lang/StringBuilder")) 넣기(allokera_minne(4, 1), 2);
                else if (Ord_SMS(Namn, "java/io/FileInputStream") || Ord_SMS(Namn, "java/io/FileOutputStream")) {
                    int referens = allokera_minne(Ord_SMS(Namn, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!fel) { heap_värde[referens + 2] = -1; 넣기(referens, 2); }
                } else fel_värde("unsupported object construction");
                continue;
            }
            if (värde == 188 || värde == 189) {
                if (värde == 188) { if (läsa_OP_kod_byte() != 10) fel_värde("only int[] newarray is supported"); }
                else if (!Ord_SMS(klassnamn_SMS(명짧()), "java/lang/String")) fel_värde("only String[] anewarray is supported");
                int längd_värde = 빼기(1); 넣기(allokera_minne(värde == 188 ? 2 : 3, längd_värde), 2); continue;
            }
            if (värde == 190) {
                int referens = 빼기(2);
                if (referens < 1 || referens >= heap_avsluta_placera - 1 || (heap_värde[referens] != 2 && heap_värde[referens] != 3)) fel_värde("null or invalid array");
                else 넣기(heap_värde[referens + 1], 1); continue;
            }
            if (värde == 192) {
                int Namn = klassnamn_SMS(명짧()), referens = 빼기(2);
                if (!Ord_SMS(Namn, "java/lang/String")) fel_värde("unsupported checkcast");
                else if (referens != 0) objekt_värde(referens, 1);
                넣기(referens, 2); continue;
            }
            fel_värde("unsupported bytecode");
        }
    }
    public static int Kör() {
        if (användarutrymme.인수개수() == 1 && 자바도구.같음(användarutrymme.argument(0), "-version")) {
            användarutrymme.Skriv("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (användarutrymme.인수개수() < 1) { användarutrymme.Skriv("Usage: java CLASS [ARGS]\n"); return 2; }
        int längd_värde = 자바도구.Namn(filnamn_SMS, användarutrymme.argument(0));
        if (längd_värde < 1 || längd_värde > 57) { användarutrymme.Skriv("java: invalid class name\n"); return 2; }
        filnamn_SMS[längd_värde] = '.'; filnamn_SMS[längd_värde + 1] = 'c'; filnamn_SMS[längd_värde + 2] = 'l'; filnamn_SMS[längd_värde + 3] = 'a'; filnamn_SMS[längd_värde + 4] = 's'; filnamn_SMS[längd_värde + 5] = 's';
        Storlek = användarutrymme.läsa_fil(filnamn_SMS, filnamn);
        if (Storlek < 0) { användarutrymme.Skriv("java: cannot read class: "); 자바도구.skriva_nummer(Storlek); användarutrymme.skriva_tecken_värde(10); return 1; }
        läsa_Kurs(); if (fel) return 1;
        int tecken_namn = konstant_SMS(klassnamn);
        if (!fel && heap_värde[tecken_namn + 1] != längd_värde) fel_värde("class name does not match file");
        for (int nummer = 0; nummer < längd_värde && !fel; nummer++) if (heap_värde[tecken_namn + 2 + nummer] != filnamn_SMS[nummer]) fel_värde("class name does not match file");
        int startpunkt_värde = -1;
        for (int nummer = 0; nummer < metod_ANTAL; nummer++) if (Ord_SMS(metod_namn_SMS[nummer], "main") && Ord_SMS(metod_Typ[nummer], "([Ljava/lang/String;)V") && (metod_ansluta[nummer] & 9) == 9) startpunkt_värde = nummer;
        if (startpunkt_värde < 0) fel_värde("public static void main(String[] args) required");
        if (fel) return 1;
        int argument = allokera_minne(3, användarutrymme.인수개수() - 1);
        for (int nummer = 1; nummer < användarutrymme.인수개수() && !fel; nummer++) heap_värde[argument + 1 + nummer] = värd_tecken(användarutrymme.argument(nummer));
        ram_INDEX = 0; ram_metod[0] = startpunkt_värde; ram_placera[0] = metod_START[startpunkt_värde]; lokal_värde[0] = argument; lokal_Typ[0] = 2;
        köra_kommando(); return fel ? 1 : 0;
    }
}
