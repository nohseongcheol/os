// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. filnamn/operand_Stack/referens/gren 경계를 köra_kommando 중 검사한다. */
public final class 자바가상기계 {
    static int[] filnamn = new int[16 * 16384], temporär_fil = new int[16384], filnamn_SMS = new int[512];
    static int[] konstant_tagg = new int[8192], 상가 = new int[8192], konstant_SEKUND_värde = new int[8192], sträng_referens = new int[8192];
    static int[] metod_namn_SMS = new int[512], metod_Typ = new int[512], metod_ansluta = new int[512], metod_ägare = new int[512];
    static int[] metod_START = new int[512], metod_avsluta = new int[512], metod_Stack = new int[512], 함수지역 = new int[512];
    static int[] metod_argument_ANTAL = new int[512], metod_argument_Typ = new int[8192], metod_Retur = new int[512];
    static int[] gräns_värde = new int[16 * 16384];
    static int[] lokal_värde = new int[16384], lokal_Typ = new int[16384], operand_Stack_värde = new int[16384], operand_Stack_Typ = new int[16384];
    static int[] ram_metod = new int[128], ram_placera = new int[128], ram_Stack = new int[128], ram_instruktion = new int[128], starta_ram = new int[128];
    static int[] Kurs_Definition_namn = new int[16], Kurs_Definition_storlek = new int[16], Kurs_Definition_överordnad = new int[16], Kurs_Definition_status = new int[16], Kurs_fack_ANTAL = new int[16], starta_Kurs_Definition = new int[16];
    static int[] Kurs_gränssnitt = new int[16 * 16], Kurs_gränssnitt_ANTAL = new int[16];
    static int[] fack_namn = new int[512], fack_Typ = new int[512], fack_ägare = new int[512], fack_Behörigheter = new int[512], fack_placera = new int[512], fack_data = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] heap_värde = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], heap_referens = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], matriselement = new int[32768], Store_heltal = new int[256];
    static int Storlek, läsa_placera, metod_ANTAL, klassnamn, ram_INDEX = -1, heap_avsluta_placera = 1, Retur_Typ;
    static int Kurs_Definition_ANTAL, fack_ANTAL, 잡기수, 현재읽는종, 던진객체, 잠시수, visa_ANTAL, mängd_ANTAL;
    static int aktuellt_tråd, antal_trådar = 1, post_Kurs_Definition;
    static int[] tråd_ram = new int[4], tråd_status = new int[4], tråd_objekt = new int[4], tråd_mål = new int[4], 가닥대기 = new int[4];
    static boolean fel, ändringsbegäran;
    static int[] lås_ägare = new int[32768], 잠금깊이 = new int[32768], ram_lås = new int[128], Kurs_lås = new int[16], Kurs_tråd = new int[16];

    static void fel_värde(String Ord_SMS) {
        if (fel) return;
        int område_KOD = 0;
        if (자바도구.같음(Ord_SMS, "ArithmeticException: / by zero")) område_KOD = 4;
        if (자바도구.같음(Ord_SMS, "NullPointerException") || 자바도구.같음(Ord_SMS, "null or invalid array")) område_KOD = 5;
        if (자바도구.같음(Ord_SMS, "ArrayIndexOutOfBoundsException")) område_KOD = 7;
        if (자바도구.같음(Ord_SMS, "StringIndexOutOfBoundsException")) område_KOD = 8;
        if (자바도구.같음(Ord_SMS, "NumberFormatException")) område_KOD = 10;
        if (자바도구.같음(Ord_SMS, "FileNotFoundException: file open failed")) område_KOD = 12;
        if (자바도구.같음(Ord_SMS, "IOException: stream closed") || 자바도구.같음(Ord_SMS, "IOException: read failed") || 자바도구.같음(Ord_SMS, "IOException: write failed")) område_KOD = 11;
        if (자바도구.같음(Ord_SMS, "ClassCastException")) område_KOD = 14;
        if (자바도구.같음(Ord_SMS, "NegativeArraySizeException")) område_KOD = 15;
        if (område_KOD != 0 && ram_INDEX >= 0) { 예외던짐(område_KOD, Ord_SMS); return; }
        användarutrymme.Skriv("JVM error: "); användarutrymme.Skriv(Ord_SMS); användarutrymme.skriva_tecken_värde(10); fel = true;
    }
    static boolean klipp(int Kör, int längd_värde) {
        if (Kör < 0 || Kör >= filnamn.length || längd_värde < 0) return false;
        int Kurs_Definition = Kör / 16384;
        return Kör % 16384 <= Kurs_Definition_storlek[Kurs_Definition] && längd_värde <= Kurs_Definition_storlek[Kurs_Definition] - Kör % 16384;
    }
    static int byte_värde() {
        if (!klipp(läsa_placera, 1)) { fel_värde("truncated class file"); return 0; }
        return filnamn[läsa_placera++];
    }
    static int 짧은수() { return byte_värde() << 8 | byte_värde(); }
    static int heltal() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int längd_värde) { if (!klipp(läsa_placera, längd_värde)) fel_värde("invalid attribute size"); else läsa_placera += längd_värde; }
    static boolean check_konstant(int nummer, int variant_värde) {
        if (nummer <= 0 || nummer >= konstant_tagg.length || konstant_tagg[nummer] != variant_värde) { fel_värde("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean SMS_område(int Kör, int längd_värde, String Ord_SMS) {
        if (!klipp(Kör, längd_värde)) return false;
        int läsa_markör = Kör, 끝 = Kör + längd_värde;
        for (int Loop_INDEX = 0; Loop_INDEX < Ord_SMS.length(); Loop_INDEX++) {
            int kodpunkt = Ord_SMS.charAt(Loop_INDEX);
            if (kodpunkt > 0 && kodpunkt < 128) { if (läsa_markör >= 끝 || filnamn[läsa_markör++] != kodpunkt) return false; }
            else if (kodpunkt < 2048) {
                if (läsa_markör + 2 > 끝 || filnamn[läsa_markör++] != (192 | (kodpunkt >> 6)) || filnamn[läsa_markör++] != (128 | (kodpunkt & 63))) return false;
            } else if (läsa_markör + 3 > 끝 || filnamn[läsa_markör++] != (224 | (kodpunkt >> 12)) || filnamn[läsa_markör++] != (128 | ((kodpunkt >> 6) & 63)) || filnamn[läsa_markör++] != (128 | (kodpunkt & 63))) return false;
        }
        return läsa_markör == 끝;
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
    static int läsa_konstant_INDEX() { int värde = 짧은수(); return värde == 0 ? 0 : 현재읽는종 * 512 + värde; }
    static int läsa_OP_kod_konstant() { return metod_ägare[ram_metod[ram_INDEX]] * 512 + 명짧(); }
    static void hoppa_över_attribut() {
        int objekt_ANTAL = 짧은수();
        for (int nummer = 0; nummer < objekt_ANTAL && !fel; nummer++) { check_konstant(läsa_konstant_INDEX(), 1); 건너(heltal()); }
    }
    static int kommando_längd(int värde) {
        if (värde == 16 || värde == 18 || värde == 21 || värde == 25 || värde == 54 || värde == 58 || värde == 188) return 2;
        if (värde == 17 || värde == 19 || värde == 132 || värde >= 153 && värde <= 167
            || värde >= 178 && värde <= 184 || värde == 187 || värde == 189 || värde == 192 || värde == 193 || värde == 198 || värde == 199) return 3;
        if (värde == 185 || värde == 200) return 5;
        if (värde >= 0 && värde <= 8 || värde >= 26 && värde <= 29 || värde >= 42 && värde <= 46 || värde >= 50 && värde <= 53
            || värde >= 59 && värde <= 62 || värde >= 75 && värde <= 79 || värde >= 83 && värde <= 95
            || värde == 96 || värde == 100 || värde == 104 || värde == 108 || värde == 112 || värde == 116
            || värde == 120 || värde == 122 || värde == 124 || värde == 126 || värde == 128 || värde == 130
            || värde >= 145 && värde <= 147 || värde == 172 || värde == 176 || värde == 177 || värde == 190 || värde == 191
            || värde == 194 || värde == 195) return 1;
        return 0;
    }
    static int placera_heltal(int läsa_markör) {
        if (!klipp(läsa_markör, 4)) { fel_värde("truncated bytecode operand"); return 0; }
        return filnamn[läsa_markör] << 24 | filnamn[läsa_markör + 1] << 16 | filnamn[läsa_markör + 2] << 8 | filnamn[läsa_markör + 3];
    }
    static int läsa_längd(int läsa_markör, int Kör, int 끝) {
        int värde = filnamn[läsa_markör], längd_värde = kommando_längd(värde);
        if (värde == 170 || värde == 171) {
            int BAS_placera = läsa_markör + 1;
            while ((BAS_placera - Kör) % 4 != 0) BAS_placera++;
            if (끝 - BAS_placera < (värde == 170 ? 12 : 8)) return 0;
            int post_ANTAL = värde == 170 ? placera_heltal(BAS_placera + 8) - placera_heltal(BAS_placera + 4) + 1 : placera_heltal(BAS_placera + 4);
            if (post_ANTAL < 0 || post_ANTAL > 2048) return 0;
            längd_värde = BAS_placera - läsa_markör + (värde == 170 ? 12 + 4 * post_ANTAL : 8 + 8 * post_ANTAL);
        }
        if (värde == 196 && läsa_markör + 1 < 끝) {
            int Ord_data = filnamn[läsa_markör + 1]; längd_värde = Ord_data == 132 ? 6 : (Ord_data == 21 || Ord_data == 25 || Ord_data == 54 || Ord_data == 58) ? 4 : 0;
        }
        return längd_värde > 0 && längd_värde <= 끝 - läsa_markör ? längd_värde : 0;
    }
    static void check_mål_värde(int mål_värde, int FUNKTION_värde) {
        if (mål_värde < metod_START[FUNKTION_värde] || mål_värde >= metod_avsluta[FUNKTION_värde] || gräns_värde[mål_värde] != FUNKTION_värde + 1) fel_värde("invalid branch target");
    }
    static void läsa_Kurs(int Kurs_Definition) {
        현재읽는종 = Kurs_Definition; läsa_placera = Kurs_Definition * 16384; Storlek = läsa_placera + Kurs_Definition_storlek[Kurs_Definition];
        if (heltal() != 0xcafebabe) { fel_värde("not a class file"); return; }
        int 부판 = 짧은수(), version_värde = 짧은수();
        if (version_värde < 45 || version_värde > 52 || 부판 != 0) { fel_värde("supported class versions: 45..52, minor 0"); return; }
        int konstant_ANTAL = 짧은수(), BAS_placera = Kurs_Definition * 512;
        if (konstant_ANTAL < 1 || konstant_ANTAL > 512) { fel_värde("constant pool limit (511)"); return; }
        for (int post_ANTAL = 1; post_ANTAL < konstant_ANTAL && !fel; post_ANTAL++) {
            int nummer = BAS_placera + post_ANTAL, variant_värde = byte_värde(); konstant_tagg[nummer] = variant_värde;
            if (variant_värde == 1) { konstant_SEKUND_värde[nummer] = 짧은수(); 상가[nummer] = läsa_placera; 건너(konstant_SEKUND_värde[nummer]); }
            else if (variant_värde == 3) 상가[nummer] = heltal();
            else if (variant_värde == 7 || variant_värde == 8) 상가[nummer] = läsa_konstant_INDEX();
            else if (variant_värde == 9 || variant_värde == 10 || variant_värde == 11 || variant_värde == 12) { 상가[nummer] = läsa_konstant_INDEX(); konstant_SEKUND_värde[nummer] = läsa_konstant_INDEX(); }
            else fel_värde("unsupported constant type");
        }
        int behörighet_värde = 짧은수();
        if ((behörighet_värde & (0x2000 | 0x4000)) != 0) fel_värde("annotation/enum class unsupported");
        Kurs_Definition_namn[Kurs_Definition] = klassnamn_SMS(läsa_konstant_INDEX());
        Kurs_Definition_överordnad[Kurs_Definition] = klassnamn_SMS(läsa_konstant_INDEX());
        int gränssnitt_ANTAL = 짧은수(); if (gränssnitt_ANTAL > 16) { fel_värde("interface count limit"); return; }
        Kurs_gränssnitt_ANTAL[Kurs_Definition] = gränssnitt_ANTAL;
        for (int Loop_INDEX = 0; Loop_INDEX < gränssnitt_ANTAL; Loop_INDEX++) Kurs_gränssnitt[Kurs_Definition * 16 + Loop_INDEX] = klassnamn_SMS(läsa_konstant_INDEX());
        int fält_ANTAL = 짧은수();
        if (fält_ANTAL > 512 - fack_ANTAL) { fel_värde("field count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < fält_ANTAL && !fel; Loop_INDEX++) {
            int fil_INDEX = fack_ANTAL++; fack_ägare[fil_INDEX] = Kurs_Definition; fack_Behörigheter[fil_INDEX] = 짧은수(); fack_namn[fil_INDEX] = läsa_konstant_INDEX(); fack_Typ[fil_INDEX] = läsa_konstant_INDEX();
            check_konstant(fack_namn[fil_INDEX], 1); check_konstant(fack_Typ[fil_INDEX], 1);
            int 보존값 = läsa_placera; läsa_placera = 상가[fack_Typ[fil_INDEX]]; int område_KOD = 서술형(läsa_placera + konstant_SEKUND_värde[fack_Typ[fil_INDEX]], false); läsa_placera = 보존값;
            if ((fack_Behörigheter[fil_INDEX] & 8) == 0) fack_placera[fil_INDEX] = Kurs_fack_ANTAL[Kurs_Definition]++;
            int attribut_data = 짧은수();
            for (int inre_koppling_placera = 0; inre_koppling_placera < attribut_data && !fel; inre_koppling_placera++) {
                int namn_konstant = läsa_konstant_INDEX(), giltig_längd = heltal();
                if (Ord_SMS(namn_konstant, "ConstantValue") && giltig_längd == 2) {
                    int data_värde = läsa_konstant_INDEX();
                    if (område_KOD == 1 && check_konstant(data_värde, 3)) fack_data[fil_INDEX] = 상가[data_värde];
                    else if (område_KOD == 2 && check_konstant(data_värde, 8)) fack_data[fil_INDEX] = konstant_SMS(상가[data_värde]);
                } else 건너(giltig_längd);
            }
        }
        int objekt_ANTAL = 짧은수();
        if (objekt_ANTAL > 512 - metod_ANTAL) { fel_värde("method count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < objekt_ANTAL && !fel; Loop_INDEX++) {
            int nummer = metod_ANTAL++; metod_ägare[nummer] = Kurs_Definition;
            metod_ansluta[nummer] = 짧은수(); metod_namn_SMS[nummer] = läsa_konstant_INDEX(); metod_Typ[nummer] = läsa_konstant_INDEX();
            check_konstant(metod_namn_SMS[nummer], 1); 서술읽기(nummer);
            if ((metod_ansluta[nummer] & 8) == 0) {
                if (metod_argument_ANTAL[nummer] == 16) { fel_värde("too many instance method arguments"); return; }
                for (int Jämförelse_placera = metod_argument_ANTAL[nummer]; Jämförelse_placera > 0; Jämförelse_placera--) metod_argument_Typ[nummer * 16 + Jämförelse_placera] = metod_argument_Typ[nummer * 16 + Jämförelse_placera - 1];
                metod_argument_Typ[nummer * 16] = 2; metod_argument_ANTAL[nummer]++;
            }
            if ((metod_ansluta[nummer] & 0x100) != 0) fel_värde("user native method unsupported");
            if (Ord_SMS(metod_namn_SMS[nummer], "<clinit>")) starta_Kurs_Definition[Kurs_Definition] = nummer + 1;
            for (int framåtvänd_värde = 0; framåtvänd_värde < nummer; framåtvänd_värde++) if (metod_ägare[framåtvänd_värde] == Kurs_Definition && matchning_Ord(metod_namn_SMS[framåtvänd_värde], metod_namn_SMS[nummer]) && matchning_Ord(metod_Typ[framåtvänd_värde], metod_Typ[nummer])) fel_värde("duplicate method");
            int attribut_ANTAL = 짧은수();
            for (int attribut_värde = 0; attribut_värde < attribut_ANTAL && !fel; attribut_värde++) {
                int Namn = läsa_konstant_INDEX(), längd_värde = heltal(), Kör = läsa_placera;
                if (!klipp(Kör, längd_värde)) { fel_värde("truncated method attribute"); break; }
                if (Ord_SMS(Namn, "Code")) {
                    if (metod_START[nummer] != 0) fel_värde("duplicate Code attribute");
                    metod_Stack[nummer] = 짧은수(); 함수지역[nummer] = 짧은수(); int KOD_längd = heltal();
                    if (metod_Stack[nummer] > 128 || 함수지역[nummer] > 128 || 함수지역[nummer] < metod_argument_ANTAL[nummer]
                        || KOD_längd < 1 || KOD_längd > 8192) fel_värde("method memory limits exceeded");
                    metod_START[nummer] = läsa_placera; 건너(KOD_längd); metod_avsluta[nummer] = läsa_placera;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { fel_värde("exception table limit"); return; }
                    for (int inre_koppling_placera = 0; inre_koppling_placera < 잡는수; inre_koppling_placera++) {
                        int fel_referens_2dc99928 = 잡기수++; 잡기함수[fel_referens_2dc99928] = nummer;
                        잡기시작[fel_referens_2dc99928] = metod_START[nummer] + 짧은수(); 잡기끝[fel_referens_2dc99928] = metod_START[nummer] + 짧은수();
                        잡기위치[fel_referens_2dc99928] = metod_START[nummer] + 짧은수(); int 부호값 = läsa_konstant_INDEX(); 잡기종[fel_referens_2dc99928] = 부호값 == 0 ? 0 : klassnamn_SMS(부호값);
                    }
                    hoppa_över_attribut();
                    if (läsa_placera != Kör + längd_värde) fel_värde("Code attribute size mismatch");
                } else 건너(längd_värde);
            }
            if ((metod_ansluta[nummer] & 0x400) != 0) continue;
            if (metod_START[nummer] == 0) fel_värde("missing Code attribute");
            int fack_post = metod_START[nummer];
            while (fack_post < metod_avsluta[nummer] && !fel) {
                int längd_värde = läsa_längd(fack_post, metod_START[nummer], metod_avsluta[nummer]);
                if (längd_värde == 0) { fel_värde("unsupported or truncated bytecode"); break; }
                gräns_värde[fack_post] = nummer + 1; fack_post += längd_värde;
            }
            fack_post = metod_START[nummer];
            while (fack_post < metod_avsluta[nummer] && !fel) {
                int värde = filnamn[fack_post];
                if (värde >= 153 && värde <= 167 || värde == 198 || värde == 199) check_mål_värde(fack_post + (short)(filnamn[fack_post + 1] << 8 | filnamn[fack_post + 2]), nummer);
                if (värde == 200) check_mål_värde(fack_post + placera_heltal(fack_post + 1), nummer);
                if (värde == 170 || värde == 171) {
                    int läsa_markör = fack_post + 1; while ((läsa_markör - metod_START[nummer]) % 4 != 0) läsa_markör++;
                    check_mål_värde(fack_post + placera_heltal(läsa_markör), nummer);
                    int post_ANTAL = värde == 170 ? placera_heltal(läsa_markör + 8) - placera_heltal(läsa_markör + 4) + 1 : placera_heltal(läsa_markör + 4);
                    läsa_markör += värde == 170 ? 12 : 8;
                    for (int inre_koppling_placera = 0; inre_koppling_placera < post_ANTAL; inre_koppling_placera++) check_mål_värde(fack_post + placera_heltal(läsa_markör + inre_koppling_placera * (värde == 170 ? 4 : 8) + (värde == 170 ? 0 : 4)), nummer);
                }
                fack_post += läsa_längd(fack_post, metod_START[nummer], metod_avsluta[nummer]);
            }
            for (int inre_koppling_placera = 0; inre_koppling_placera < 잡기수; inre_koppling_placera++) if (잡기함수[inre_koppling_placera] == nummer) {
                check_mål_värde(잡기시작[inre_koppling_placera], nummer); check_mål_värde(잡기위치[inre_koppling_placera], nummer);
                if (잡기끝[inre_koppling_placera] != metod_avsluta[nummer]) check_mål_värde(잡기끝[inre_koppling_placera], nummer);
                if (잡기시작[inre_koppling_placera] >= 잡기끝[inre_koppling_placera]) fel_värde("invalid exception range");
            }
        }
        if (!fel) hoppa_över_attribut();
        if (läsa_placera != Storlek) fel_värde("extra class file data");
    }
    static int allokera_minne(int variant_värde, int längd_värde) { return 새기억(variant_värde, längd_värde); }
    static boolean objekt_värde(int referens, int variant_värde) {
        if (!informationsteknik_giltig_objekt(referens)) return false;
        if (heap_värde[referens] != variant_värde) { fel_värde("object type mismatch"); return false; }
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
        if (Retur_Typ == 2) skydda_värde(operand_Stack_värde[fack_post]);
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
        if (ram_INDEX % 32 == 31) { fel_värde("call stack limit (32)"); return; }
        int Nästa_objekt = ram_INDEX + 1;
        for (int nummer = 0; nummer < 128; nummer++) lokal_Typ[Nästa_objekt * 128 + nummer] = 0;
        for (int nummer = metod_argument_ANTAL[FUNKTION_värde] - 1; nummer >= 0; nummer--) {
            lokal_värde[Nästa_objekt * 128 + nummer] = 빼기(metod_argument_Typ[FUNKTION_värde * 16 + nummer]); lokal_Typ[Nästa_objekt * 128 + nummer] = metod_argument_Typ[FUNKTION_värde * 16 + nummer];
        }
        if (fel) return;
        ram_INDEX = Nästa_objekt; starta_ram[ram_INDEX] = 0; ram_metod[ram_INDEX] = FUNKTION_värde; ram_placera[ram_INDEX] = metod_START[FUNKTION_värde]; ram_Stack[ram_INDEX] = 0;
    }
    static void Retur_KR(int Typ_värde) {
        if (Typ_värde != metod_Retur[ram_metod[ram_INDEX]]) { fel_värde("return type mismatch"); return; }
        int värde = Typ_värde == 0 ? 0 : 빼기(Typ_värde);
        if (starta_ram[ram_INDEX] != 0) Kurs_Definition_status[starta_ram[ram_INDEX] - 1] = 2;
        if (ram_lås[ram_INDEX] != 0) { släppa_lås(ram_lås[ram_INDEX]); ram_lås[ram_INDEX] = 0; }
        ram_INDEX--; if (ram_INDEX >= aktuellt_tråd * 32 && Typ_värde != 0) 넣기(värde, Typ_värde);
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
                if (värde < 1) { fel_värde("invalid file stream path"); return; }
                flöde_filnamn[fack_post] = värde;
            }
            flöde_filnamn[längd_värde] = 0;
            int 서술자 = användarutrymme.파일서술자열기(flöde_filnamn, utmatningsposition ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { fel_värde("FileNotFoundException: file open failed"); return; }
            heap_värde[flöde_värde + 2] = 서술자; heap_värde[flöde_värde + 3] = 1;
            return;
        }
        if (kommando != 182) { fel_värde("invalid file stream invocation"); return; }
        if ((utmatningsposition && Ord_SMS(Namn, "write") || !utmatningsposition && Ord_SMS(Namn, "read"))
            && (Ord_SMS(format_värde, utmatningsposition ? "([B)V" : "([B)I") || Ord_SMS(format_värde, utmatningsposition ? "([BII)V" : "([BII)I"))) {
            boolean klipp_värde = Ord_SMS(format_värde, utmatningsposition ? "([BII)V" : "([BII)I");
            int post_ANTAL = klipp_värde ? 빼기(1) : 0, 시작점 = klipp_värde ? 빼기(1) : 0, data_MATRIS = 빼기(2), objekt_referens = 빼기(2);
            if (!objekt_värde(data_MATRIS, 20) || !objekt_värde(objekt_referens, variant_värde)) return;
            if (!klipp_värde) post_ANTAL = heap_värde[data_MATRIS + 1];
            if (시작점 < 0 || post_ANTAL < 0 || 시작점 > heap_värde[data_MATRIS + 1] - post_ANTAL) { 예외던짐(6, "file buffer bounds"); return; }
            if (heap_värde[objekt_referens + 3] == 0 || heap_värde[objekt_referens + 2] < 0) { fel_värde("IOException: stream closed"); return; }
            int Slutfört_ANTAL = 0;
            while (Slutfört_ANTAL < post_ANTAL && !fel) {
                int 반환값 = utmatningsposition ? användarutrymme.파일한바이트쓰기(heap_värde[objekt_referens + 2], heap_värde[data_MATRIS + 2 + 시작점 + Slutfört_ANTAL]) : användarutrymme.파일한바이트읽기(heap_värde[objekt_referens + 2]);
                if (반환값 < 0) { fel_värde(utmatningsposition ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!utmatningsposition && 반환값 == 256) break;
                if (!utmatningsposition) heap_värde[data_MATRIS + 2 + 시작점 + Slutfört_ANTAL] = (byte)반환값;
                Slutfört_ANTAL++;
            }
            if (!utmatningsposition) 넣기(post_ANTAL != 0 && Slutfört_ANTAL == 0 ? -1 : Slutfört_ANTAL, 1);
            return;
        }
        if (utmatningsposition && Ord_SMS(Namn, "flush") && Ord_SMS(format_värde, "()V")) { int objekt_referens = 빼기(2); if (objekt_värde(objekt_referens, variant_värde) && heap_värde[objekt_referens + 2] < 0) fel_värde("IOException: stream closed"); return; }
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
            if (RESULTAT < -1) fel_värde("IOException: read failed"); else 넣기(RESULTAT == 256 ? -1 : RESULTAT, 1);
        } else if (användarutrymme.파일한바이트쓰기(서술자, värde) != 1) fel_värde("IOException: write failed");
    }
    static void ring_metod(int INDEX, int kommando) {
        if (INDEX <= 0 || INDEX >= konstant_tagg.length || (konstant_tagg[INDEX] != 10 && konstant_tagg[INDEX] != 11)) { fel_värde("invalid method reference"); return; }
        int ägare_värde = klassnamn_SMS(상가[INDEX]), Namn = referens_namn(konstant_SEKUND_värde[INDEX]), format_värde = referenstyp(konstant_SEKUND_värde[INDEX]);
        if (fel) return;
        if (기본호출(ägare_värde, Namn, format_värde, kommando)) return;
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
        int Kurs_Definition = Sök_Kurs_Definition(ägare_värde); if (Kurs_Definition < 0 || fel) return;
        int fil_INDEX = Sök_metod(Kurs_Definition, Namn, format_värde);
        if (fil_INDEX < 0) {
            for (int kodpunkt = Kurs_Definition, post_ANTAL = 0; kodpunkt >= 0 && post_ANTAL < 16; post_ANTAL++, kodpunkt = överordnad_Kurs(kodpunkt))
                if (Ord_SMS(Kurs_Definition_överordnad[kodpunkt], "java/lang/Thread")) { 가닥호출(Namn, format_värde, kommando); return; }
            fel_värde("NoSuchMethodError"); return;
        }
        if (((metod_ansluta[fil_INDEX] & 8) != 0) != (kommando == 184)) { fel_värde("method static/instance mismatch"); return; }
        if (kommando == 184) { if (!starta(metod_ägare[fil_INDEX], ram_instruktion[ram_INDEX])) return; }
        else {
            int läsa_markör = ram_Stack[ram_INDEX] - metod_argument_ANTAL[fil_INDEX];
            if (läsa_markör < 0 || operand_Stack_Typ[ram_INDEX * 128 + läsa_markör] != 2) { fel_värde("invalid method receiver"); return; }
            int objekt_referens = operand_Stack_värde[ram_INDEX * 128 + läsa_markör];
            if (!informationsteknik_giltig_objekt(objekt_referens)) return;
            if (heap_värde[objekt_referens] < 32 || !종포함(heap_värde[objekt_referens] - 32, ägare_värde)) { fel_värde("method receiver type mismatch"); return; }
            if (kommando != 183) fil_INDEX = Sök_metod(heap_värde[objekt_referens] - 32, Namn, format_värde);
        }
        if (fil_INDEX < 0 || (metod_ansluta[fil_INDEX] & 0x400) != 0) { fel_värde("AbstractMethodError"); return; }
        int lås_referens = 0;
        if ((metod_ansluta[fil_INDEX] & 32) != 0) {
            if (kommando == 184) { int kodpunkt = metod_ägare[fil_INDEX]; if (Kurs_lås[kodpunkt] == 0) Kurs_lås[kodpunkt] = allokera_minne(8, 0); lås_referens = Kurs_lås[kodpunkt]; }
            else lås_referens = operand_Stack_värde[ram_INDEX * 128 + ram_Stack[ram_INDEX] - metod_argument_ANTAL[fil_INDEX]];
            if (!잠금얻기(lås_referens)) { if (!fel) ram_placera[ram_INDEX] = ram_instruktion[ram_INDEX]; return; }
        }
        호출(fil_INDEX); if (!fel) ram_lås[ram_INDEX] = lås_referens;
    }
    static boolean 배열저장가능(int MATRIS_referens, int data_värde) {
        if (data_värde == 0 || matriselement[MATRIS_referens] == 0) return true;
        boolean 성공여부 = matriselement[MATRIS_referens] == -1 ? (data_värde > 0 && data_värde < heap_avsluta_placera && heap_värde[data_värde] == 1) : matchning_objekt(data_värde, matriselement[MATRIS_referens]);
        if (!성공여부 && !fel) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int MATRIS_fack(int referens, int nedsänkt_text_värde, int Typ_värde) {
        if (!objekt_värde(referens, Typ_värde)) return 0;
        if (nedsänkt_text_värde < 0 || nedsänkt_text_värde >= heap_värde[referens + 1]) { fel_värde("ArrayIndexOutOfBoundsException"); return 0; }
        return referens + 2 + nedsänkt_text_värde;
    }
    static void köra_kommando() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (fel) { if (던진객체 != 0) handtag_fel(); if (fel || ram_INDEX < aktuellt_tråd * 32) break; }
            if (ram_INDEX < aktuellt_tråd * 32 || ändringsbegäran || --조각 == 0) { if (!byta_tråd()) break; 조각 = 100; }
            if (ram_INDEX == 0 && Kurs_Definition_status[post_Kurs_Definition] != 2 && !starta(post_Kurs_Definition, ram_placera[ram_INDEX])) continue;
            if (ram_INDEX == aktuellt_tråd * 32 && aktuellt_tråd != 0 && (metod_ansluta[ram_metod[ram_INDEX]] & 32) != 0 && ram_lås[ram_INDEX] == 0) {
                int objekt_referens = tråd_mål[aktuellt_tråd]; if (!잠금얻기(objekt_referens)) { if (fel) break; continue; } ram_lås[ram_INDEX] = objekt_referens;
            }
            잠시수 = 0;
            if (--남음 == 0) { fel_värde("instruction limit (500000)"); break; }
            int Kör = ram_placera[ram_INDEX]; ram_instruktion[ram_INDEX] = Kör; int värde = läsa_OP_kod_byte();
            if (fel) break;
            if (värde == 0) continue;
            if (värde == 1) { 넣기(0, 2); continue; }
            if (värde >= 2 && värde <= 8) { 넣기(värde - 3, 1); continue; }
            if (värde == 16) { 넣기((byte)läsa_OP_kod_byte(), 1); continue; }
            if (värde == 17) { 넣기((short)명짧(), 1); continue; }
            if (värde == 18 || värde == 19) {
                int nummer = metod_ägare[ram_metod[ram_INDEX]] * 512 + (värde == 18 ? läsa_OP_kod_byte() : 명짧());
                if (nummer <= 0 || nummer >= konstant_tagg.length) fel_värde("invalid ldc constant");
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
            if (värde == 46 || värde >= 50 && värde <= 53) {
                int post_placera = 빼기(1), objekt_referens = 빼기(2), område_KOD = värde == 46 ? 2 : värde == 50 ? 3 : värde == 51 ? 20 : värde == 52 ? 22 : 23;
                if (värde == 51 && objekt_referens > 0 && objekt_referens < heap_avsluta_placera && heap_värde[objekt_referens] == 21) område_KOD = 21;
                int läsa_markör = MATRIS_fack(objekt_referens, post_placera, område_KOD); if (!fel) 넣기(heap_värde[läsa_markör], värde == 50 ? 2 : 1); continue;
            }
            if (värde == 79 || värde >= 83 && värde <= 86) {
                int post_referens = 빼기(värde == 83 ? 2 : 1), post_placera = 빼기(1), objekt_referens = 빼기(2), område_KOD = värde == 79 ? 2 : värde == 83 ? 3 : värde == 84 ? 20 : värde == 85 ? 22 : 23;
                if (värde == 84 && objekt_referens > 0 && objekt_referens < heap_avsluta_placera && heap_värde[objekt_referens] == 21) område_KOD = 21;
                int läsa_markör = MATRIS_fack(objekt_referens, post_placera, område_KOD);
                if (!fel && område_KOD == 3 && !배열저장가능(objekt_referens, post_referens)) continue;
                if (!fel) heap_värde[läsa_markör] = område_KOD == 20 ? (byte)post_referens : område_KOD == 21 ? post_referens & 1 : område_KOD == 22 ? (char)post_referens : område_KOD == 23 ? (short)post_referens : post_referens;
                continue;
            }
            if (värde >= 87 && värde <= 95) { Stack_instruktion(värde); continue; }
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
            if (värde >= 178 && värde <= 181) { 필드호출(läsa_OP_kod_konstant(), värde, Kör); continue; }
            if (värde >= 182 && värde <= 185) {
                int 부호값 = läsa_OP_kod_konstant();
                if (värde == 185) { int summa_ANTAL = läsa_OP_kod_byte(); if (summa_ANTAL == 0 || läsa_OP_kod_byte() != 0) { fel_värde("invalid invokeinterface operands"); continue; } }
                ring_metod(부호값, värde); continue;
            }
            if (värde == 187) { 새객체(klassnamn_SMS(läsa_OP_kod_konstant()), Kör); continue; }
            if (värde == 188 || värde == 189) {
                int område_KOD = 3, komponent = 0;
                if (värde == 188) { int 임시값 = läsa_OP_kod_byte(); område_KOD = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else komponent = klassnamn_SMS(läsa_OP_kod_konstant());
                if (område_KOD == 0) { fel_värde("unsupported primitive array type"); continue; }
                int giltig_längd = 빼기(1), objekt_referens = allokera_minne(område_KOD, giltig_längd); if (!fel) matriselement[objekt_referens] = komponent; 넣기(objekt_referens, 2); continue;
            }
            if (värde == 190) {
                int objekt_referens = 빼기(2);
                if (informationsteknik_giltig_objekt(objekt_referens)) { int Jämförelse_placera = heap_värde[objekt_referens]; if (Jämförelse_placera != 2 && Jämförelse_placera != 3 && (Jämförelse_placera < 20 || Jämförelse_placera > 23)) fel_värde("not an array"); else 넣기(heap_värde[objekt_referens + 1], 1); }
                continue;
            }
            if (värde == 191) {
                int objekt_referens = 빼기(2); if (informationsteknik_giltig_objekt(objekt_referens)) { if (heap_värde[objekt_referens] != 9) fel_värde("athrow requires supported Throwable"); else { 던진객체 = objekt_referens; fel = true; } }
                continue;
            }
            if (värde == 192 || värde == 193) {
                int namn_konstant = klassnamn_SMS(läsa_OP_kod_konstant()), objekt_referens = 빼기(2); boolean PASSA = matchning_objekt(objekt_referens, namn_konstant);
                if (värde == 193) 넣기(objekt_referens != 0 && PASSA ? 1 : 0, 1);
                else { if (!PASSA && !fel) fel_värde("ClassCastException"); 넣기(objekt_referens, 2); }
                continue;
            }
            if (värde == 170 || värde == 171) {
                int läsa_markör = Kör + 1, fil_INDEX = ram_metod[ram_INDEX], Nyckel_referens = 빼기(1);
                while ((läsa_markör - metod_START[fil_INDEX]) % 4 != 0) läsa_markör++;
                int mål_ADRESS = placera_heltal(läsa_markör);
                if (värde == 170) { int 낮은값 = placera_heltal(läsa_markör + 4), 높은값 = placera_heltal(läsa_markör + 8); if (Nyckel_referens >= 낮은값 && Nyckel_referens <= 높은값) mål_ADRESS = placera_heltal(läsa_markör + 12 + (Nyckel_referens - 낮은값) * 4); }
                else { int summa_ANTAL = placera_heltal(läsa_markör + 4); for (int Loop_INDEX = 0; Loop_INDEX < summa_ANTAL; Loop_INDEX++) if (placera_heltal(läsa_markör + 8 + Loop_INDEX * 8) == Nyckel_referens) mål_ADRESS = placera_heltal(läsa_markör + 12 + Loop_INDEX * 8); }
                flytta_värde(Kör + mål_ADRESS); continue;
            }
            if (värde == 200) { flytta_värde(Kör + placera_heltal(Kör + 1)); continue; }
            if (värde == 194 || värde == 195) {
                int objekt_referens = 빼기(2);
                if (värde == 195) släppa_lås(objekt_referens);
                else if (!잠금얻기(objekt_referens) && !fel) { 넣기(objekt_referens, 2); ram_placera[ram_INDEX] = Kör; }
                continue;
            }
            if (värde == 196) {
                int kommando_KOD = läsa_OP_kod_byte(), post_placera = 명짧();
                if (kommando_KOD == 21 || kommando_KOD == 25) läsa_lokal(post_placera, kommando_KOD == 21 ? 1 : 2);
                else if (kommando_KOD == 54 || kommando_KOD == 58) skriva_lokal(post_placera, kommando_KOD == 54 ? 1 : 2);
                else if (kommando_KOD == 132) { int DELTA_värde = (short)명짧(); läsa_lokal(post_placera, 1); 넣기(빼기(1) + DELTA_värde, 1); skriva_lokal(post_placera, 1); }
                else fel_värde("unsupported wide opcode");
                continue;
            }
            fel_värde("unsupported bytecode");
        }
    }
    static int Sök_Kurs_Definition(int Namn) {
        for (int Loop_INDEX = 0; Loop_INDEX < Kurs_Definition_ANTAL; Loop_INDEX++) if (Kurs_Definition_namn[Loop_INDEX] != 0 && matchning_Ord(Kurs_Definition_namn[Loop_INDEX], Namn)) return Loop_INDEX;
        return dossier_Kurs_Definition(konstant_SMS(Namn));
    }
    static int dossier_Kurs_Definition(int namn_sträng) {
        if (!objekt_värde(namn_sträng, 1)) return -1;
        int längd_värde = heap_värde[namn_sträng + 1];
        if (längd_värde < 1 || längd_värde > 505 || Kurs_Definition_ANTAL == 16) { fel_värde("class name/count limit"); return -1; }
        for (int Loop_INDEX = 0; Loop_INDEX < längd_värde; Loop_INDEX++) { int kodpunkt = heap_värde[namn_sträng + 2 + Loop_INDEX]; filnamn_SMS[Loop_INDEX] = kodpunkt == '/' ? '.' : kodpunkt; }
        filnamn_SMS[längd_värde] = '.'; filnamn_SMS[längd_värde + 1] = 'c'; filnamn_SMS[längd_värde + 2] = 'l'; filnamn_SMS[längd_värde + 3] = 'a'; filnamn_SMS[längd_värde + 4] = 's'; filnamn_SMS[längd_värde + 5] = 's'; filnamn_SMS[längd_värde + 6] = 0;
        int Storlek = användarutrymme.läsa_fil(filnamn_SMS, temporär_fil);
        if (Storlek < 0) { fel_värde("ClassNotFoundException"); return -1; }
        int Kurs_Definition = Kurs_Definition_ANTAL++; Kurs_Definition_storlek[Kurs_Definition] = Storlek;
        for (int Loop_INDEX = 0; Loop_INDEX < Storlek; Loop_INDEX++) filnamn[Kurs_Definition * 16384 + Loop_INDEX] = temporär_fil[Loop_INDEX];
        läsa_Kurs(Kurs_Definition); if (fel) return -1;
        int verklig_data = konstant_SMS(Kurs_Definition_namn[Kurs_Definition]);
        if (!texter_lika(verklig_data, namn_sträng, true)) { fel_värde("class name does not match file"); return -1; }
        int överordnad_värde = Kurs_Definition_överordnad[Kurs_Definition];
        if (överordnad_värde != 0 && !Ord_SMS(överordnad_värde, "java/lang/Object") && !Ord_SMS(överordnad_värde, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 försöka_igen_värde 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = Sök_Kurs_Definition(överordnad_värde);
            if (fel || 위 < 0) return -1;
            int läsa_markör = 위, scen_ANTAL = 0;
            while (läsa_markör >= 0 && scen_ANTAL++ < 16) {
                if (läsa_markör == Kurs_Definition) { fel_värde("cyclic inheritance"); return -1; }
                läsa_markör = överordnad_Kurs(läsa_markör);
            }
            int 시작변위 = Kurs_fack_ANTAL[위];
            for (int fil_INDEX = 0; fil_INDEX < fack_ANTAL; fil_INDEX++) if (fack_ägare[fil_INDEX] == Kurs_Definition && (fack_Behörigheter[fil_INDEX] & 8) == 0) fack_placera[fil_INDEX] += 시작변위;
            Kurs_fack_ANTAL[Kurs_Definition] += 시작변위;
        }
        return Kurs_Definition;
    }
    static int överordnad_Kurs(int Kurs_Definition) {
        int Namn = Kurs_Definition_överordnad[Kurs_Definition];
        for (int Loop_INDEX = 0; Loop_INDEX < Kurs_Definition_ANTAL; Loop_INDEX++) if (Namn != 0 && Kurs_Definition_namn[Loop_INDEX] != 0 && matchning_Ord(Kurs_Definition_namn[Loop_INDEX], Namn)) return Loop_INDEX;
        return -1;
    }
    static int Sök_metod(int Kurs_Definition, int Namn, int format_värde) {
        for (int 깊이 = 0; Kurs_Definition >= 0 && 깊이 < 16; 깊이++, Kurs_Definition = överordnad_Kurs(Kurs_Definition)) {
            for (int Loop_INDEX = 0; Loop_INDEX < metod_ANTAL; Loop_INDEX++) if (metod_ägare[Loop_INDEX] == Kurs_Definition && matchning_Ord(metod_namn_SMS[Loop_INDEX], Namn) && matchning_Ord(metod_Typ[Loop_INDEX], format_värde)) return Loop_INDEX;
        }
        return -1;
    }
    static int namn_metod(int Kurs_Definition, String Namn, String format_värde) {
        for (int 깊이 = 0; Kurs_Definition >= 0 && 깊이 < 16; 깊이++, Kurs_Definition = överordnad_Kurs(Kurs_Definition))
            for (int Loop_INDEX = 0; Loop_INDEX < metod_ANTAL; Loop_INDEX++) if (metod_ägare[Loop_INDEX] == Kurs_Definition && Ord_SMS(metod_namn_SMS[Loop_INDEX], Namn) && Ord_SMS(metod_Typ[Loop_INDEX], format_värde)) return Loop_INDEX;
        return -1;
    }
    static int Typ_variant(int Namn) { return filnamn[상가[Namn]] == 'L' || filnamn[상가[Namn]] == '[' ? 2 : 1; }
    static boolean starta(int Kurs_Definition, int kommando_START) {
        if (Kurs_Definition < 0 || fel) return false;
        if (Kurs_Definition_status[Kurs_Definition] == 3) { fel_värde("NoClassDefFoundError: initialization failed"); return false; }
        if (Kurs_Definition_status[Kurs_Definition] == 1 && Kurs_tråd[Kurs_Definition] != aktuellt_tråd) { ram_placera[ram_INDEX] = kommando_START; ändringsbegäran = true; return false; }
        if (Kurs_Definition_status[Kurs_Definition] != 0) return true;
        int 위 = överordnad_Kurs(Kurs_Definition);
        if (위 >= 0 && !starta(위, kommando_START)) return false;
        Kurs_Definition_status[Kurs_Definition] = 1; Kurs_tråd[Kurs_Definition] = aktuellt_tråd;
        if (starta_Kurs_Definition[Kurs_Definition] != 0) {
            ram_placera[ram_INDEX] = kommando_START;
            호출(starta_Kurs_Definition[Kurs_Definition] - 1); if (!fel) starta_ram[ram_INDEX] = Kurs_Definition + 1;
            return false;
        }
        Kurs_Definition_status[Kurs_Definition] = 2; return true;
    }
    static void 필드호출(int INDEX, int kommando, int Kör) {
        if (!check_konstant(INDEX, 9)) return;
        int ägare_värde = klassnamn_SMS(상가[INDEX]), Namn = referens_namn(konstant_SEKUND_värde[INDEX]), format_värde = referenstyp(konstant_SEKUND_värde[INDEX]);
        if (Ord_SMS(ägare_värde, "java/lang/System") && (Ord_SMS(Namn, "out") || Ord_SMS(Namn, "err")) && Ord_SMS(format_värde, "Ljava/io/PrintStream;") && kommando == 178) { 넣기(-1, 2); return; }
        int Kurs_Definition = Sök_Kurs_Definition(ägare_värde); if (Kurs_Definition < 0 || fel) return;
        int 찾음 = -1;
        for (int läsa_markör = Kurs_Definition, 깊이 = 0; läsa_markör >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, läsa_markör = överordnad_Kurs(läsa_markör))
            for (int fil_INDEX = 0; fil_INDEX < fack_ANTAL; fil_INDEX++) if (fack_ägare[fil_INDEX] == läsa_markör && matchning_Ord(fack_namn[fil_INDEX], Namn) && matchning_Ord(fack_Typ[fil_INDEX], format_värde)) 찾음 = fil_INDEX;
        if (찾음 < 0) { fel_värde("NoSuchFieldError"); return; }
        boolean statisk_värde = kommando == 178 || kommando == 179;
        if (statisk_värde != ((fack_Behörigheter[찾음] & 8) != 0)) { fel_värde("field static/instance mismatch"); return; }
        if (statisk_värde && !starta(fack_ägare[찾음], Kör)) return;
        int Typ_värde = Typ_variant(format_värde), värde = 0;
        if (kommando == 179 || kommando == 181) värde = 빼기(Typ_värde);
        if (statisk_värde) { if (kommando == 178) 넣기(fack_data[찾음], Typ_värde); else if (!fel) fack_data[찾음] = värde; return; }
        int objekt_referens = 빼기(2);
        if (!informationsteknik_giltig_objekt(objekt_referens)) return;
        if (heap_värde[objekt_referens] < 32 || !종포함(heap_värde[objekt_referens] - 32, ägare_värde)) { fel_värde("field receiver type mismatch"); return; }
        int 보관칸 = objekt_referens + 2 + fack_placera[찾음];
        if (kommando == 180) 넣기(heap_värde[보관칸], Typ_värde);
        else if (!fel) { heap_värde[보관칸] = värde; heap_referens[보관칸] = Typ_värde == 2 ? 1 : 0; }
    }
    static boolean 종포함(int Kurs_Definition, int Namn) {
        for (int 중첩깊이 = 0; Kurs_Definition >= 0 && 중첩깊이 < 16; 중첩깊이++, Kurs_Definition = överordnad_Kurs(Kurs_Definition)) {
            if (matchning_Ord(Kurs_Definition_namn[Kurs_Definition], Namn) || (Kurs_Definition_överordnad[Kurs_Definition] != 0 && matchning_Ord(Kurs_Definition_överordnad[Kurs_Definition], Namn))) return true;
            for (int inre_koppling_placera = 0; inre_koppling_placera < Kurs_gränssnitt_ANTAL[Kurs_Definition]; inre_koppling_placera++) if (matchning_Ord(Kurs_gränssnitt[Kurs_Definition * 16 + inre_koppling_placera], Namn)) return true;
        }
        return false;
    }
    static boolean texter_lika(int 첫값, int byte_data, boolean sökväg_2) {
        if (첫값 == byte_data) return true;
        if (첫값 <= 0 || byte_data <= 0 || heap_värde[첫값] != 1 || heap_värde[byte_data] != 1 || heap_värde[첫값 + 1] != heap_värde[byte_data + 1]) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < heap_värde[첫값 + 1]; Loop_INDEX++) {
            int x_koordinat = heap_värde[첫값 + 2 + Loop_INDEX], Y_koordinat = heap_värde[byte_data + 2 + Loop_INDEX];
            if (sökväg_2) { if (x_koordinat == '.') x_koordinat = '/'; if (Y_koordinat == '.') Y_koordinat = '/'; }
            if (x_koordinat != Y_koordinat) return false;
        }
        return true;
    }
    static boolean informationsteknik_giltig_objekt(int objekt_referens) {
        if (objekt_referens == 0) { fel_värde("NullPointerException"); return false; }
        if (objekt_referens < 1 || objekt_referens >= heap_avsluta_placera || 힙폭[objekt_referens] < 2 || heap_värde[objekt_referens] == 0) { fel_värde("invalid object reference"); return false; }
        return true;
    }
    static void skydda_värde(int objekt_referens) {
        if (objekt_referens > 0 && objekt_referens < heap_avsluta_placera && 힙폭[objekt_referens] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = objekt_referens;
    }
    static void visa_värde(int objekt_referens) {
        if (objekt_referens > 0 && objekt_referens < heap_avsluta_placera && 힙폭[objekt_referens] >= 2 && heap_värde[objekt_referens] != 0 && 힙표시[objekt_referens] == 0) {
            힙표시[objekt_referens] = 1; 표시대기[visa_ANTAL++] = objekt_referens;
        }
    }
    static void 수거() {
        visa_ANTAL = 0; mängd_ANTAL++;
        for (int check_placera = 1; check_placera < heap_avsluta_placera; check_placera += 힙폭[check_placera]) 힙표시[check_placera] = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < sträng_referens.length; Loop_INDEX++) visa_värde(sträng_referens[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < fack_ANTAL; Loop_INDEX++) if ((fack_Behörigheter[Loop_INDEX] & 8) != 0 && Typ_variant(fack_Typ[Loop_INDEX]) == 2) visa_värde(fack_data[Loop_INDEX]);
        for (int 임시값 = 0; 임시값 < antal_trådar; 임시값++) {
            visa_värde(tråd_objekt[임시값]); visa_värde(tråd_mål[임시값]);
            int 꼭대기자리 = 임시값 == aktuellt_tråd ? ram_INDEX : tråd_ram[임시값];
            for (int fil_INDEX = 임시값 * 32; fil_INDEX <= 꼭대기자리; fil_INDEX++) {
                for (int inre_koppling_placera = 0; inre_koppling_placera < 함수지역[ram_metod[fil_INDEX]]; inre_koppling_placera++) if (lokal_Typ[fil_INDEX * 128 + inre_koppling_placera] == 2) visa_värde(lokal_värde[fil_INDEX * 128 + inre_koppling_placera]);
                for (int inre_koppling_placera = 0; inre_koppling_placera < ram_Stack[fil_INDEX]; inre_koppling_placera++) if (operand_Stack_Typ[fil_INDEX * 128 + inre_koppling_placera] == 2) visa_värde(operand_Stack_värde[fil_INDEX * 128 + inre_koppling_placera]);
            }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < skärmbild_referens.length; Loop_INDEX++) visa_värde(skärmbild_referens[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < 나중수; Loop_INDEX++) visa_värde(나중실행[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < Store_heltal.length; Loop_INDEX++) visa_värde(Store_heltal[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < Kurs_Definition_ANTAL; Loop_INDEX++) visa_värde(Kurs_lås[Loop_INDEX]);
        for (int check_placera = 1; check_placera < heap_avsluta_placera; check_placera += 힙폭[check_placera]) if (잠금깊이[check_placera] > 0) visa_värde(check_placera);
        visa_värde(던진객체);
        for (int Loop_INDEX = 0; Loop_INDEX < 잠시수; Loop_INDEX++) visa_värde(잠시참조[Loop_INDEX]);
        while (visa_ANTAL > 0) {
            int objekt_referens = 표시대기[--visa_ANTAL], område_KOD = heap_värde[objekt_referens];
            for (int Loop_INDEX = objekt_referens + 2; Loop_INDEX < objekt_referens + 힙폭[objekt_referens]; Loop_INDEX++) if (område_KOD == 3 || område_KOD == 4 || heap_referens[Loop_INDEX] != 0) visa_värde(heap_värde[Loop_INDEX]);
        }
        for (int check_placera = 1; check_placera < heap_avsluta_placera; check_placera += 힙폭[check_placera]) if (힙표시[check_placera] == 0) heap_värde[check_placera] = 0;
        for (int check_placera = 1; check_placera < heap_avsluta_placera; check_placera += 힙폭[check_placera]) if (heap_värde[check_placera] == 0) {
            while (check_placera + 힙폭[check_placera] < heap_avsluta_placera && heap_värde[check_placera + 힙폭[check_placera]] == 0) { int Nästa_placera = check_placera + 힙폭[check_placera]; 힙폭[check_placera] += 힙폭[Nästa_placera]; 힙폭[Nästa_placera] = 0; }
            if (check_placera + 힙폭[check_placera] == heap_avsluta_placera) { heap_avsluta_placera = check_placera; break; }
        }
    }
    static int 새기억(int variant_värde, int längd_värde) {
        if (längd_värde < 0) { fel_värde("NegativeArraySizeException"); return 0; }
        if (längd_värde > heap_värde.length - 3) { fel_värde("object heap exhausted"); return 0; }
        int 필요수 = längd_värde + 2, objekt_referens = 0;
        if (필요수 <= heap_värde.length - heap_avsluta_placera) { objekt_referens = heap_avsluta_placera; heap_avsluta_placera += 필요수; }
        else {
            수거();
            for (int läsa_markör = 1; läsa_markör < heap_avsluta_placera; läsa_markör += 힙폭[läsa_markör]) if (heap_värde[läsa_markör] == 0 && 힙폭[läsa_markör] >= 필요수) { objekt_referens = läsa_markör; break; }
            if (objekt_referens != 0) {
                int 남은길이 = 힙폭[objekt_referens] - 필요수;
                if (남은길이 >= 2) { 힙폭[objekt_referens + 필요수] = 남은길이; heap_värde[objekt_referens + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= heap_värde.length - heap_avsluta_placera) { objekt_referens = heap_avsluta_placera; heap_avsluta_placera += 필요수; }
        }
        if (objekt_referens == 0) { fel_värde("object heap exhausted"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < 필요수; Loop_INDEX++) { heap_värde[objekt_referens + Loop_INDEX] = 0; heap_referens[objekt_referens + Loop_INDEX] = 0; 힙폭[objekt_referens + Loop_INDEX] = 0; }
        matriselement[objekt_referens] = 0;
        힙폭[objekt_referens] = 필요수; heap_värde[objekt_referens] = variant_värde; heap_värde[objekt_referens + 1] = längd_värde; skydda_värde(objekt_referens); return objekt_referens;
    }
    static int fel_Kurs(String namn_konstant) {
        if (자바도구.같음(namn_konstant, "java/lang/Throwable")) return 1;
        if (자바도구.같음(namn_konstant, "java/lang/Exception")) return 2;
        if (자바도구.같음(namn_konstant, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(namn_konstant, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(namn_konstant, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(namn_konstant, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(namn_konstant, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(namn_konstant, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(namn_konstant, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(namn_konstant, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(namn_konstant, "java/io/IOException")) return 11;
        if (자바도구.같음(namn_konstant, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(namn_konstant, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(namn_konstant, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(namn_konstant, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int fel_konstant(int Namn) {
        for (int Loop_INDEX = 1; Loop_INDEX <= 41; Loop_INDEX++) if (Ord_SMS(Namn, fel_namn(Loop_INDEX))) return Loop_INDEX;
        return 0;
    }
    static String fel_namn(int konto_värde) {
        if (konto_värde == 40) return "java/lang/InterruptedException";
        if (konto_värde == 41) return "Svenska/eget/대기중단예외";
        if (konto_värde == 39) return "java/net/SocketException";
        if (konto_värde == 20) return "Svenska/eget/fel_31f743d2";
        if (konto_värde == 21) return "Svenska/eget/körning_fel";
        if (konto_värde == 22) return "Svenska/eget/indata_utleverans_fel";
        if (konto_värde == 23) return "Svenska/eget/vänta_TIMEOUT_fel";
        if (konto_värde == 24) return "Svenska/eget/ADRESS_LETAUPP_fel";
        if (konto_värde == 25) return "Svenska/eget/파일없음예외";
        if (konto_värde == 26) return "Svenska/eget/kommunikation_fel";
        if (konto_värde == 27) return "Svenska/eget/ogiltig_argument_fel";
        if (konto_värde == 28) return "Svenska/eget/nummer_format_fel";
        if (konto_värde == 29) return "Svenska/eget/범위예외";
        if (konto_värde == 30) return "Svenska/eget/배열범위예외";
        if (konto_värde == 31) return "Svenska/eget/문자열범위예외";
        if (konto_värde == 32) return "Svenska/eget/null_referens_fel";
        if (konto_värde == 33) return "Svenska/eget/산술예외";
        if (konto_värde == 34) return "Svenska/eget/status_fel";
        if (konto_värde == 35) return "Svenska/eget/Typ_Sänd_fel";
        if (konto_värde == 36) return "Svenska/eget/음수배열크기예외";
        if (konto_värde == 37) return "Svenska/eget/MATRIS_Store_fel";
        if (konto_värde == 38) return "Svenska/eget/tråd_status_fel";
        if (konto_värde == 1) return "java/lang/Throwable"; if (konto_värde == 2) return "java/lang/Exception";
        if (konto_värde == 3) return "java/lang/RuntimeException"; if (konto_värde == 4) return "java/lang/ArithmeticException";
        if (konto_värde == 5) return "java/lang/NullPointerException"; if (konto_värde == 6) return "java/lang/IndexOutOfBoundsException";
        if (konto_värde == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (konto_värde == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (konto_värde == 9) return "java/lang/IllegalArgumentException"; if (konto_värde == 10) return "java/lang/NumberFormatException";
        if (konto_värde == 11) return "java/io/IOException"; if (konto_värde == 12) return "java/io/FileNotFoundException";
        if (konto_värde == 17) return "java/lang/ArrayStoreException";
        if (konto_värde == 18) return "java/net/UnknownHostException";
        if (konto_värde == 19) return "java/net/SocketTimeoutException";
        if (konto_värde == 16) return "java/lang/IllegalThreadStateException";
        if (konto_värde == 13) return "java/lang/IllegalStateException"; if (konto_värde == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int fel_överordnad(int konto_värde) {
        if (konto_värde == 40) return 2;
        if (konto_värde == 41) return 40;
        if (konto_värde == 39) return 11;
        if (konto_värde == 1) return 0;
        if (konto_värde == 2) return 1;
        if (konto_värde == 3) return 2;
        if (konto_värde == 4) return 3;
        if (konto_värde == 5) return 3;
        if (konto_värde == 6) return 3;
        if (konto_värde == 7) return 6;
        if (konto_värde == 8) return 6;
        if (konto_värde == 9) return 3;
        if (konto_värde == 10) return 9;
        if (konto_värde == 11) return 2;
        if (konto_värde == 12) return 11;
        if (konto_värde == 13) return 3;
        if (konto_värde == 14) return 3;
        if (konto_värde == 15) return 3;
        if (konto_värde == 16) return 9;
        if (konto_värde == 17) return 3;
        if (konto_värde == 18) return 11;
        if (konto_värde == 19) return 11;
        if (konto_värde == 20) return 2;
        if (konto_värde == 21) return 3;
        if (konto_värde == 22) return 11;
        if (konto_värde == 23) return 22;
        if (konto_värde == 24) return 22;
        if (konto_värde == 25) return 22;
        if (konto_värde == 26) return 22;
        if (konto_värde == 27) return 9;
        if (konto_värde == 28) return 27;
        if (konto_värde == 29) return 6;
        if (konto_värde == 30) return 29;
        if (konto_värde == 31) return 29;
        if (konto_värde == 32) return 5;
        if (konto_värde == 33) return 4;
        if (konto_värde == 34) return 13;
        if (konto_värde == 35) return 14;
        if (konto_värde == 36) return 15;
        if (konto_värde == 37) return 17;
        if (konto_värde == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int faktiskt_värde, int 요구값) {
        for (int 깊이 = 0; faktiskt_värde != 0 && 깊이 < 16; 깊이++, faktiskt_värde = fel_överordnad(faktiskt_värde))
            if (faktiskt_värde == 요구값) return true;
        return false;
    }
    static void 예외던짐(int konto_värde, String VIKTIGT_referens) {
        int objekt_referens = 새기억(9, 2); if (fel) return;
        heap_värde[objekt_referens + 2] = konto_värde; heap_värde[objekt_referens + 3] = värd_tecken(VIKTIGT_referens); heap_referens[objekt_referens + 3] = 1;
        던진객체 = objekt_referens; fel = true;
    }
    static boolean matchning_objekt(int objekt_referens, int Namn) {
        if (objekt_referens == 0) return true;
        if (!informationsteknik_giltig_objekt(objekt_referens)) return false;
        int område_KOD = heap_värde[objekt_referens];
        if (Ord_SMS(Namn, "java/lang/Object")) return true;
        if (område_KOD >= 32) return 종포함(område_KOD - 32, Namn);
        if (område_KOD == 9) { int mål_ADRESS = fel_konstant(Namn); return mål_ADRESS != 0 && 예외포함(heap_värde[objekt_referens + 2], mål_ADRESS); }
        if (område_KOD == 1) return Ord_SMS(Namn, "java/lang/String") || Ord_SMS(Namn, "java/lang/CharSequence");
        if (område_KOD == 4) return Ord_SMS(Namn, "java/lang/StringBuilder") || Ord_SMS(Namn, "java/lang/CharSequence");
        if (område_KOD == 10) return Ord_SMS(Namn, "java/util/ArrayList") || Ord_SMS(Namn, "java/util/List");
        if (område_KOD == 11) return Ord_SMS(Namn, "java/util/HashMap") || Ord_SMS(Namn, "java/util/Map");
        if (område_KOD == 12) return Ord_SMS(Namn, "java/lang/Integer") || Ord_SMS(Namn, "java/lang/Number");
        if (område_KOD >= 24 && område_KOD <= 28 && heap_värde[objekt_referens + 13] != 0) return 한국어화면종(Namn) == område_KOD || Ord_SMS(Namn, "Svenska/eget/skärmbild_element");
        if (område_KOD >= 24 && område_KOD <= 28) return (한국어화면종(Namn) == 0 && skärmbild_Kurs(Namn) == område_KOD) || Ord_SMS(Namn, "java/awt/Component") || Ord_SMS(Namn, "java/awt/Container") || Ord_SMS(Namn, "javax/swing/JComponent");
        if (område_KOD == 29) return Ord_SMS(Namn, heap_värde[objekt_referens + 3] != 0 ? "Svenska/eget/동작알림" : "java/awt/event/ActionEvent");
        if (område_KOD == 30) return Ord_SMS(Namn, "java/awt/FlowLayout") || Ord_SMS(Namn, "java/awt/LayoutManager");
        if (område_KOD == 17) return Ord_SMS(Namn, "java/net/Socket");
        if (område_KOD == 18) return Ord_SMS(Namn, "java/net/ServerSocket");
        if (område_KOD == 19) return Ord_SMS(Namn, heap_värde[objekt_referens + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (område_KOD == 14) return Ord_SMS(Namn, "java/net/InetAddress");
        if (område_KOD == 15) return Ord_SMS(Namn, "java/net/DatagramSocket");
        if (område_KOD == 16) return Ord_SMS(Namn, "java/net/DatagramPacket");
        if (område_KOD == 13) return Ord_SMS(Namn, heap_värde[objekt_referens + 3] != 0 ? "Svenska/eget/arbete" : "java/lang/Thread");
        if (område_KOD == 2) return Ord_SMS(Namn, "[I"); if (område_KOD == 20) return Ord_SMS(Namn, "[B"); if (område_KOD == 21) return Ord_SMS(Namn, "[Z");
        if (område_KOD == 22) return Ord_SMS(Namn, "[C"); if (område_KOD == 23) return Ord_SMS(Namn, "[S");
        if (område_KOD != 3) return false;
        if (Ord_SMS(Namn, "[Ljava/lang/Object;")) return true;
        int komponent = matriselement[objekt_referens];
        if (komponent == -1) return Ord_SMS(Namn, "[Ljava/lang/String;") || Ord_SMS(Namn, "[Ljava/lang/CharSequence;");
        if (komponent == 0) return false;
        if (배열종비교(komponent, Namn)) return true;
        if ((Ord_SMS(komponent, "java/lang/String") || Ord_SMS(komponent, "java/lang/StringBuilder")) && Ord_SMS(Namn, "[Ljava/lang/CharSequence;")) return true;
        for (int Loop_INDEX = 0; Loop_INDEX < Kurs_Definition_ANTAL; Loop_INDEX++) if (matchning_Ord(Kurs_Definition_namn[Loop_INDEX], komponent)) {
            for (int kodpunkt = Loop_INDEX, 중첩깊이 = 0; kodpunkt >= 0 && 중첩깊이 < 16; 중첩깊이++, kodpunkt = överordnad_Kurs(kodpunkt)) {
                if (배열종비교(Kurs_Definition_överordnad[kodpunkt], Namn)) return true;
                for (int inre_koppling_placera = 0; inre_koppling_placera < Kurs_gränssnitt_ANTAL[kodpunkt]; inre_koppling_placera++) if (배열종비교(Kurs_gränssnitt[kodpunkt * 16 + inre_koppling_placera], Namn)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int namn_konstant, int 형식참조) {
        int check_placera = 상가[형식참조], post_ANTAL = konstant_SEKUND_värde[형식참조];
        if (namn_konstant == 0 || post_ANTAL < 4 || filnamn[check_placera] != '[' || filnamn[check_placera + 1] != 'L' || filnamn[check_placera + post_ANTAL - 1] != ';' || konstant_SEKUND_värde[namn_konstant] != post_ANTAL - 3) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < post_ANTAL - 3; Loop_INDEX++) if (filnamn[상가[namn_konstant] + Loop_INDEX] != filnamn[check_placera + 2 + Loop_INDEX]) return false;
        return true;
    }
    static void handtag_fel() {
        if (던진객체 == 0) return;
        fel = false;
        while (ram_INDEX >= aktuellt_tråd * 32) {
            int fil_INDEX = ram_metod[ram_INDEX], läsa_markör = ram_instruktion[ram_INDEX];
            for (int Loop_INDEX = 0; Loop_INDEX < 잡기수; Loop_INDEX++) if (잡기함수[Loop_INDEX] == fil_INDEX && läsa_markör >= 잡기시작[Loop_INDEX] && läsa_markör < 잡기끝[Loop_INDEX]
                && (잡기종[Loop_INDEX] == 0 || matchning_objekt(던진객체, 잡기종[Loop_INDEX]))) {
                ram_placera[ram_INDEX] = 잡기위치[Loop_INDEX]; ram_Stack[ram_INDEX] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (starta_ram[ram_INDEX] != 0) Kurs_Definition_status[starta_ram[ram_INDEX] - 1] = 3;
            if (ram_lås[ram_INDEX] != 0) { släppa_lås(ram_lås[ram_INDEX]); ram_lås[ram_INDEX] = 0; }
            ram_INDEX--;
        }
        användarutrymme.Skriv("Uncaught ");
        if (heap_värde[던진객체] == 9) { användarutrymme.Skriv(fel_namn(heap_värde[던진객체 + 2])); användarutrymme.Skriv(": "); skriva_SMS(heap_värde[던진객체 + 3]); }
        else användarutrymme.Skriv("user exception");
        användarutrymme.skriva_tecken_värde(10); 던진객체 = 0; fel = true;
    }
    // 이 JVM의 operand_Stack 항목은 aktuellt_objekt category-1(int/reference)만 허용한다.
    static void Stack_instruktion(int kommando_KOD) {
        int 첫값 = 빼기(0), 첫형식 = Retur_Typ;
        if (kommando_KOD == 87) return;
        if (kommando_KOD == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int byte_data = 빼기(0), SEKUND_format = Retur_Typ;
        if (kommando_KOD == 88) return;
        if (kommando_KOD == 90) { 넣기(첫값, 첫형식); 넣기(byte_data, SEKUND_format); 넣기(첫값, 첫형식); return; }
        if (kommando_KOD == 92) { 넣기(byte_data, SEKUND_format); 넣기(첫값, 첫형식); 넣기(byte_data, SEKUND_format); 넣기(첫값, 첫형식); return; }
        if (kommando_KOD == 95) { 넣기(첫값, 첫형식); 넣기(byte_data, SEKUND_format); return; }
        int kodpunkt = 빼기(0), 셋째형식 = Retur_Typ;
        if (kommando_KOD == 91) { 넣기(첫값, 첫형식); 넣기(kodpunkt, 셋째형식); 넣기(byte_data, SEKUND_format); 넣기(첫값, 첫형식); return; }
        if (kommando_KOD == 93) { 넣기(byte_data, SEKUND_format); 넣기(첫값, 첫형식); 넣기(kodpunkt, 셋째형식); 넣기(byte_data, SEKUND_format); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = Retur_Typ;
        넣기(byte_data, SEKUND_format); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(kodpunkt, 셋째형식); 넣기(byte_data, SEKUND_format); 넣기(첫값, 첫형식);
    }
    static void 새객체(int namn_konstant, int 시작점) {
        int område_KOD = 0, giltig_längd = 0, fel_referens = fel_konstant(namn_konstant);
        if (Ord_SMS(namn_konstant, "java/lang/StringBuilder")) { område_KOD = 4; giltig_längd = 1; }
        if (Ord_SMS(namn_konstant, "java/io/FileInputStream")) { område_KOD = 5; giltig_längd = 2; }
        if (Ord_SMS(namn_konstant, "java/io/FileOutputStream")) { område_KOD = 6; giltig_längd = 2; }
        if (fel_referens != 0) { område_KOD = 9; giltig_längd = 2; }
        if (Ord_SMS(namn_konstant, "java/util/ArrayList")) { område_KOD = 10; giltig_längd = 2; }
        if (Ord_SMS(namn_konstant, "java/util/HashMap")) { område_KOD = 11; giltig_längd = 2; }
        if (Ord_SMS(namn_konstant, "java/lang/Integer")) { område_KOD = 12; giltig_längd = 1; }
        if (Ord_SMS(namn_konstant, "java/net/Socket")) { område_KOD = 17; giltig_längd = 5; }
        if (Ord_SMS(namn_konstant, "java/net/ServerSocket")) { område_KOD = 18; giltig_längd = 5; }
        if (Ord_SMS(namn_konstant, "java/net/DatagramSocket")) { område_KOD = 15; giltig_längd = 3; }
        if (Ord_SMS(namn_konstant, "java/net/DatagramPacket")) { område_KOD = 16; giltig_längd = 4; }
        if (Ord_SMS(namn_konstant, "java/lang/Thread") || Ord_SMS(namn_konstant, "Svenska/eget/arbete")) { område_KOD = 13; giltig_längd = 2; }
        if (Ord_SMS(namn_konstant, "java/lang/Object")) { område_KOD = 8; }
        if (område_KOD == 0 && skärmbild_Kurs(namn_konstant) != 0) { område_KOD = skärmbild_Kurs(namn_konstant); giltig_längd = 12; }
        if (område_KOD == 0) {
            int kodpunkt = Sök_Kurs_Definition(namn_konstant); if (kodpunkt < 0 || fel || !starta(kodpunkt, 시작점)) return;
            område_KOD = 32 + kodpunkt; giltig_längd = Kurs_fack_ANTAL[kodpunkt];
        }
        int objekt_referens = allokera_minne(område_KOD, giltig_längd); if (fel) return;
        if (område_KOD == 13 && Ord_SMS(namn_konstant, "Svenska/eget/arbete")) heap_värde[objekt_referens + 3] = 1;
        if (område_KOD >= 24 && område_KOD <= 28 && 한국어화면종(namn_konstant) != 0) heap_värde[objekt_referens + 13] = 1;
        if (område_KOD == 5 || område_KOD == 6 || område_KOD == 15 || område_KOD == 17 || område_KOD == 18) heap_värde[objekt_referens + 2] = -1;
        if (område_KOD == 9) heap_värde[objekt_referens + 2] = fel_referens;
        넣기(objekt_referens, 2);
    }
    static boolean 값같음(int 첫값, int byte_data) {
        if (첫값 == byte_data) return true;
        if (첫값 == 0 || byte_data == 0 || 첫값 < 0 || byte_data < 0 || 첫값 >= heap_avsluta_placera || byte_data >= heap_avsluta_placera) return false;
        if (heap_värde[첫값] == 1 && heap_värde[byte_data] == 1) return texter_lika(첫값, byte_data, false);
        return heap_värde[첫값] == 12 && heap_värde[byte_data] == 12 && heap_värde[첫값 + 2] == heap_värde[byte_data + 2];
    }
    static int 글조각(int objekt_referens, int START_placera, int avsluta_placera) {
        if (!objekt_värde(objekt_referens, 1)) return 0;
        if (START_placera < 0 || avsluta_placera < START_placera || avsluta_placera > heap_värde[objekt_referens + 1]) { fel_värde("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = allokera_minne(1, avsluta_placera - START_placera); if (fel) return 0;
        for (int Loop_INDEX = START_placera; Loop_INDEX < avsluta_placera; Loop_INDEX++) heap_värde[반환값 + 2 + Loop_INDEX - START_placera] = heap_värde[objekt_referens + 2 + Loop_INDEX];
        return 반환값;
    }
    static int anslut_SMS(int 첫값, int byte_data) {
        if (!objekt_värde(첫값, 1) || !objekt_värde(byte_data, 1)) return 0;
        int post_ANTAL = heap_värde[첫값 + 1], metod_INDEX = heap_värde[byte_data + 1], 반환값 = allokera_minne(1, post_ANTAL + metod_INDEX); if (fel) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < post_ANTAL; Loop_INDEX++) heap_värde[반환값 + 2 + Loop_INDEX] = heap_värde[첫값 + 2 + Loop_INDEX];
        for (int Loop_INDEX = 0; Loop_INDEX < metod_INDEX; Loop_INDEX++) heap_värde[반환값 + 2 + post_ANTAL + Loop_INDEX] = heap_värde[byte_data + 2 + Loop_INDEX];
        return 반환값;
    }
    static boolean 기본호출(int ägare, int namn_konstant, int 서술상수, int kommando_KOD) {
        if (Ord_SMS(ägare, "Svenska/eget/실행인수") && kommando_KOD == 184) {
            if (Ord_SMS(namn_konstant, "objekt_ANTAL") && Ord_SMS(서술상수, "()I")) { 넣기(användarutrymme.인수개수() - 1, 1); return true; }
            if (Ord_SMS(namn_konstant, "text") && Ord_SMS(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= användarutrymme.인수개수() - 1) 예외던짐(29, "köra_kommando argument 범위를 벗어났습니다");
                else 넣기(värd_tecken(användarutrymme.argument(순번 + 1)), 2);
                return true;
            }
            fel_värde("지원하지 않는 Svenska köra_kommando argument 호출"); return true;
        }
        if (Ord_SMS(ägare, "Svenska/eget/arbete")) { Process_tråd(namn_konstant, 서술상수, kommando_KOD, true); return true; }
        if (한국어화면소유(ägare)) { 한국어화면호출(ägare, namn_konstant, 서술상수, kommando_KOD); return true; }
        if (skärmbild_ägare(ägare)) { 화면호출(ägare, namn_konstant, 서술상수, kommando_KOD); return true; }
        if (Ord_SMS(ägare, "java/net/Socket") || Ord_SMS(ägare, "java/net/ServerSocket") || Ord_SMS(ägare, "java/io/InputStream") || Ord_SMS(ägare, "java/io/OutputStream")) { 흐름호출(ägare, namn_konstant, 서술상수, kommando_KOD); return true; }
        if (Ord_SMS(ägare, "Svenska/eget/kärna_värde") && kommando_KOD == 184) {
            if (Ord_SMS(namn_konstant, "화면너비") && Ord_SMS(서술상수, "()I")) { 넣기(användarutrymme.화면너비(), 1); return true; }
            if (Ord_SMS(namn_konstant, "화면높이") && Ord_SMS(서술상수, "()I")) { 넣기(användarutrymme.화면높이(), 1); return true; }
            if (Ord_SMS(namn_konstant, "밀리초") && Ord_SMS(서술상수, "()I")) { 넣기(användarutrymme.밀리초(), 1); return true; }
            if (Ord_SMS(namn_konstant, "그림대기") && Ord_SMS(서술상수, "()I")) { 넣기(användarutrymme.그림대기(), 1); return true; }
            if (Ord_SMS(namn_konstant, "rektangel") && Ord_SMS(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), Y_koordinat = 빼기(1), x_koordinat = 빼기(1); 넣기(användarutrymme.rektangel(x_koordinat, Y_koordinat, 너비, 높이, 색상), 1); return true; }
        }
        if (Ord_SMS(ägare, "java/net/InetAddress") || Ord_SMS(ägare, "java/net/DatagramPacket") || Ord_SMS(ägare, "java/net/DatagramSocket")) { 통신호출(ägare, namn_konstant, 서술상수, kommando_KOD); return true; }
        if (Ord_SMS(ägare, "java/lang/Thread")) { 가닥호출(namn_konstant, 서술상수, kommando_KOD); return true; }
        if (Ord_SMS(ägare, "java/lang/Object")) {
            if (Ord_SMS(namn_konstant, "<init>") && Ord_SMS(서술상수, "()V") && kommando_KOD == 183) { informationsteknik_giltig_objekt(빼기(2)); return true; }
            if (Ord_SMS(namn_konstant, "equals") && Ord_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int byte_data = 빼기(2), 첫값 = 빼기(2); if (informationsteknik_giltig_objekt(첫값)) 넣기(첫값 == byte_data ? 1 : 0, 1); return true; }
        }
        if (fel_konstant(ägare) != 0) {
            if (Ord_SMS(namn_konstant, "<init>") && kommando_KOD == 183 && (Ord_SMS(서술상수, "()V") || Ord_SMS(서술상수, "(Ljava/lang/String;)V"))) {
                int fråga = Ord_SMS(서술상수, "()V") ? 0 : 빼기(2), objekt_referens = 빼기(2);
                if (objekt_värde(objekt_referens, 9)) { heap_värde[objekt_referens + 3] = fråga; heap_referens[objekt_referens + 3] = 1; } return true;
            }
            if ((Ord_SMS(namn_konstant, "getMessage") || Ord_SMS(namn_konstant, "설명")) && Ord_SMS(서술상수, "()Ljava/lang/String;")) { int objekt_referens = 빼기(2); if (objekt_värde(objekt_referens, 9)) 넣기(heap_värde[objekt_referens + 3], 2); return true; }
        }
        if (Ord_SMS(ägare, "java/lang/String")) {
            if (kommando_KOD == 182 && Ord_SMS(namn_konstant, "getBytes") && (Ord_SMS(서술상수, "()[B") || Ord_SMS(서술상수, "(Ljava/lang/String;)[B"))) {
                int kodning_namn = Ord_SMS(서술상수, "()[B") ? 0 : 빼기(2), objekt_referens = 빼기(2);
                if (!objekt_värde(objekt_referens, 1)) return true;
                if (kodning_namn != 0 && !texter_lika(kodning_namn, värd_tecken("UTF-8"), false) && !texter_lika(kodning_namn, värd_tecken("UTF8"), false) && !texter_lika(kodning_namn, värd_tecken("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int post_ANTAL = heap_värde[objekt_referens + 1], 반환값 = allokera_minne(20, post_ANTAL * 3), 사용수 = 0; if (fel) return true;
                for (int inre_koppling_placera = 0; inre_koppling_placera < post_ANTAL; inre_koppling_placera++) {
                    int kodpunkt = heap_värde[objekt_referens + 2 + inre_koppling_placera];
                    if (kodpunkt >= 0xd800 && kodpunkt <= 0xdbff && inre_koppling_placera + 1 < post_ANTAL && heap_värde[objekt_referens + 3 + inre_koppling_placera] >= 0xdc00 && heap_värde[objekt_referens + 3 + inre_koppling_placera] <= 0xdfff) kodpunkt = 0x10000 + ((kodpunkt - 0xd800) << 10) + heap_värde[objekt_referens + 2 + ++inre_koppling_placera] - 0xdc00;
                    else if (kodpunkt >= 0xd800 && kodpunkt <= 0xdfff) kodpunkt = '?';
                    if (kodpunkt < 128) heap_värde[반환값 + 2 + 사용수++] = kodpunkt;
                    else { int byte_ANTAL = kodpunkt < 2048 ? 2 : kodpunkt < 65536 ? 3 : 4; heap_värde[반환값 + 2 + 사용수++] = (byte)((byte_ANTAL == 2 ? 192 : byte_ANTAL == 3 ? 224 : 240) | kodpunkt >> (6 * (byte_ANTAL - 1))); for (int Jämförelse_placera = byte_ANTAL - 1; Jämförelse_placera > 0; Jämförelse_placera--) heap_värde[반환값 + 2 + 사용수++] = (byte)(128 | kodpunkt >> (6 * (Jämförelse_placera - 1)) & 63); }
                }
                heap_värde[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (kommando_KOD == 184 && Ord_SMS(namn_konstant, "valueOf") && Ord_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(siffra_tecken(빼기(1)), 2); return true; }
            if (kommando_KOD != 182) return false;
            if (Ord_SMS(namn_konstant, "equals") && Ord_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int byte_data = 빼기(2), 첫값 = 빼기(2); if (objekt_värde(첫값, 1)) 넣기(texter_lika(첫값, byte_data, false) ? 1 : 0, 1); return true; }
            if (Ord_SMS(namn_konstant, "isEmpty") && Ord_SMS(서술상수, "()Z")) { int 첫값 = 빼기(2); if (objekt_värde(첫값, 1)) 넣기(heap_värde[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Ord_SMS(namn_konstant, "substring") && (Ord_SMS(서술상수, "(I)Ljava/lang/String;") || Ord_SMS(서술상수, "(II)Ljava/lang/String;"))) {
                boolean SEKUND_värde = Ord_SMS(서술상수, "(II)Ljava/lang/String;"); int avsluta_placera = SEKUND_värde ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (objekt_värde(첫값, 1)) 넣기(글조각(첫값, 시작점, SEKUND_värde ? avsluta_placera : heap_värde[첫값 + 1]), 2); return true;
            }
            if (Ord_SMS(namn_konstant, "concat") && Ord_SMS(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int byte_data = 빼기(2), 첫값 = 빼기(2); 넣기(anslut_SMS(첫값, byte_data), 2); return true; }
            if (Ord_SMS(namn_konstant, "hashCode") && Ord_SMS(서술상수, "()I")) { int 첫값 = 빼기(2), hash_värde = 0; if (objekt_värde(첫값, 1)) { for (int Loop_INDEX = 0; Loop_INDEX < heap_värde[첫값 + 1]; Loop_INDEX++) hash_värde = hash_värde * 31 + heap_värde[첫값 + 2 + Loop_INDEX]; 넣기(hash_värde, 1); } return true; }
            if (Ord_SMS(namn_konstant, "toString") && Ord_SMS(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (objekt_värde(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Ord_SMS(ägare, "java/lang/Integer")) {
            if (kommando_KOD == 184 && Ord_SMS(namn_konstant, "valueOf") && Ord_SMS(서술상수, "(I)Ljava/lang/Integer;")) { int data_värde = 빼기(1), objekt_referens = data_värde >= -128 && data_värde <= 127 ? Store_heltal[data_värde + 128] : 0; if (objekt_referens == 0) { objekt_referens = allokera_minne(12, 1); if (!fel) { heap_värde[objekt_referens + 2] = data_värde; if (data_värde >= -128 && data_värde <= 127) Store_heltal[data_värde + 128] = objekt_referens; } } 넣기(objekt_referens, 2); return true; }
            if (kommando_KOD == 183 && Ord_SMS(namn_konstant, "<init>") && Ord_SMS(서술상수, "(I)V")) { int data_värde = 빼기(1), objekt_referens = 빼기(2); if (objekt_värde(objekt_referens, 12)) heap_värde[objekt_referens + 2] = data_värde; return true; }
            if (kommando_KOD == 182 && Ord_SMS(namn_konstant, "intValue") && Ord_SMS(서술상수, "()I")) { int objekt_referens = 빼기(2); if (objekt_värde(objekt_referens, 12)) 넣기(heap_värde[objekt_referens + 2], 1); return true; }
            if (kommando_KOD == 184 && Ord_SMS(namn_konstant, "toString") && Ord_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(siffra_tecken(빼기(1)), 2); return true; }
        }
        if (Ord_SMS(ägare, "java/lang/Math") && kommando_KOD == 184) {
            if (Ord_SMS(namn_konstant, "abs") && Ord_SMS(서술상수, "(I)I")) { int läsa_värde = 빼기(1); 넣기(läsa_värde < 0 ? -läsa_värde : läsa_värde, 1); return true; }
            if ((Ord_SMS(namn_konstant, "min") || Ord_SMS(namn_konstant, "max")) && Ord_SMS(서술상수, "(II)I")) { int byte_data = 빼기(1), 첫값 = 빼기(1); 넣기(Ord_SMS(namn_konstant, "min") ? (첫값 < byte_data ? 첫값 : byte_data) : (첫값 > byte_data ? 첫값 : byte_data), 1); return true; }
        }
        if (Ord_SMS(ägare, "java/lang/System") && kommando_KOD == 184) {
            if (Ord_SMS(namn_konstant, "gc") && Ord_SMS(서술상수, "()V")) { 수거(); return true; }
            if (Ord_SMS(namn_konstant, "arraycopy") && Ord_SMS(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int post_ANTAL = 빼기(1), mål_värde_INDEX = 빼기(1), byte_data = 빼기(2), START_placera = 빼기(1), 첫값 = 빼기(2);
                if (informationsteknik_giltig_objekt(첫값) && informationsteknik_giltig_objekt(byte_data)) {
                    int område_KOD = heap_värde[첫값];
                    if (heap_värde[byte_data] != område_KOD || (område_KOD != 2 && område_KOD != 3 && (område_KOD < 20 || område_KOD > 23))) fel_värde("arraycopy type mismatch");
                    else if (post_ANTAL < 0 || START_placera < 0 || mål_värde_INDEX < 0 || START_placera > heap_värde[첫값 + 1] - post_ANTAL || mål_värde_INDEX > heap_värde[byte_data + 1] - post_ANTAL) fel_värde("ArrayIndexOutOfBoundsException");
                    else if (첫값 == byte_data && mål_värde_INDEX > START_placera) { for (int Loop_INDEX = post_ANTAL - 1; Loop_INDEX >= 0; Loop_INDEX--) heap_värde[byte_data + 2 + mål_värde_INDEX + Loop_INDEX] = heap_värde[첫값 + 2 + START_placera + Loop_INDEX]; }
                    else { for (int Loop_INDEX = 0; Loop_INDEX < post_ANTAL && !fel; Loop_INDEX++) { int data_värde = heap_värde[첫값 + 2 + START_placera + Loop_INDEX]; if (område_KOD != 3 || 배열저장가능(byte_data, data_värde)) heap_värde[byte_data + 2 + mål_värde_INDEX + Loop_INDEX] = data_värde; } }
                }
                return true;
            }
        }
        if (Ord_SMS(ägare, "java/util/ArrayList") || Ord_SMS(ägare, "java/util/List") || Ord_SMS(ägare, "java/util/HashMap") || Ord_SMS(ägare, "java/util/Map")) {
            모음호출(ägare, namn_konstant, 서술상수, kommando_KOD); return true;
        }
        return false;
    }
    static void 모음늘리기(int objekt_referens, int 필요수) {
        int Föregående_värde = heap_värde[objekt_referens + 2], kapacitet_data = Föregående_värde == 0 ? 0 : heap_värde[Föregående_värde + 1];
        if (kapacitet_data >= 필요수) return;
        int Nästa_placera = kapacitet_data < 8 ? 8 : kapacitet_data * 2; if (Nästa_placera < 필요수) Nästa_placera = 필요수;
        int data_MATRIS = allokera_minne(3, Nästa_placera); if (fel) return;
        for (int Loop_INDEX = 0; Loop_INDEX < kapacitet_data; Loop_INDEX++) heap_värde[data_MATRIS + 2 + Loop_INDEX] = heap_värde[Föregående_värde + 2 + Loop_INDEX];
        heap_värde[objekt_referens + 2] = data_MATRIS; heap_referens[objekt_referens + 2] = 1;
    }
    static void 모음호출(int ägare, int namn_konstant, int 서술상수, int kommando_KOD) {
        boolean 대응참조 = Ord_SMS(ägare, "java/util/HashMap") || Ord_SMS(ägare, "java/util/Map"); int område_KOD = 대응참조 ? 11 : 10;
        if (Ord_SMS(namn_konstant, "<init>") && kommando_KOD == 183 && Ord_SMS(서술상수, "()V")) { int objekt_referens = 빼기(2); if (objekt_värde(objekt_referens, område_KOD)) 모음늘리기(objekt_referens, 8); return; }
        if (kommando_KOD != 182 && kommando_KOD != 185) { fel_värde("invalid collection invocation"); return; }
        if (Ord_SMS(namn_konstant, "size") && Ord_SMS(서술상수, "()I") || Ord_SMS(namn_konstant, "isEmpty") && Ord_SMS(서술상수, "()Z")) {
            int objekt_referens = 빼기(2); if (objekt_värde(objekt_referens, område_KOD)) 넣기(Ord_SMS(namn_konstant, "size") ? heap_värde[objekt_referens + 3] : heap_värde[objekt_referens + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Ord_SMS(namn_konstant, "clear") && Ord_SMS(서술상수, "()V")) { int objekt_referens = 빼기(2); if (objekt_värde(objekt_referens, område_KOD)) { int data_MATRIS = heap_värde[objekt_referens + 2]; for (int Loop_INDEX = 0; Loop_INDEX < heap_värde[data_MATRIS + 1]; Loop_INDEX++) heap_värde[data_MATRIS + 2 + Loop_INDEX] = 0; heap_värde[objekt_referens + 3] = 0; } return; }
        if (!대응참조 && Ord_SMS(namn_konstant, "add") && Ord_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            int data_värde = 빼기(2), objekt_referens = 빼기(2); if (!objekt_värde(objekt_referens, 10)) return;
            int post_ANTAL = heap_värde[objekt_referens + 3]; 모음늘리기(objekt_referens, post_ANTAL + 1); if (!fel) { heap_värde[heap_värde[objekt_referens + 2] + 2 + post_ANTAL] = data_värde; heap_värde[objekt_referens + 3] = post_ANTAL + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Ord_SMS(namn_konstant, "get") || Ord_SMS(namn_konstant, "remove")) && Ord_SMS(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && Ord_SMS(namn_konstant, "set") && Ord_SMS(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean informationsteknik_Tilldelad = Ord_SMS(namn_konstant, "set"); int data_värde = informationsteknik_Tilldelad ? 빼기(2) : 0, post_placera = 빼기(1), objekt_referens = 빼기(2);
            if (!objekt_värde(objekt_referens, 10)) return;
            int post_ANTAL = heap_värde[objekt_referens + 3], data_MATRIS = heap_värde[objekt_referens + 2];
            if (post_placera < 0 || post_placera >= post_ANTAL) { 예외던짐(6, "list index"); return; }
            int Föregående_värde = heap_värde[data_MATRIS + 2 + post_placera];
            if (informationsteknik_Tilldelad) heap_värde[data_MATRIS + 2 + post_placera] = data_värde;
            if (Ord_SMS(namn_konstant, "remove")) { for (int Loop_INDEX = post_placera + 1; Loop_INDEX < post_ANTAL; Loop_INDEX++) heap_värde[data_MATRIS + 1 + Loop_INDEX] = heap_värde[data_MATRIS + 2 + Loop_INDEX]; heap_värde[data_MATRIS + 1 + post_ANTAL] = 0; heap_värde[objekt_referens + 3] = post_ANTAL - 1; }
            넣기(Föregående_värde, 2); return;
        }
        if (대응참조 && (Ord_SMS(namn_konstant, "get") || Ord_SMS(namn_konstant, "remove")) && Ord_SMS(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Ord_SMS(namn_konstant, "put") && Ord_SMS(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Ord_SMS(namn_konstant, "containsKey") && Ord_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Ord_SMS(namn_konstant, "put"), ta_bort = Ord_SMS(namn_konstant, "remove");
            int data_värde = 넣기여부 ? 빼기(2) : 0, Nyckel_referens = 빼기(2), objekt_referens = 빼기(2); if (!objekt_värde(objekt_referens, 11)) return;
            int post_ANTAL = heap_värde[objekt_referens + 3], data_MATRIS = heap_värde[objekt_referens + 2], 찾은여부 = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < post_ANTAL; Loop_INDEX++) if (값같음(Nyckel_referens, heap_värde[data_MATRIS + 2 + 2 * Loop_INDEX])) { 찾은여부 = Loop_INDEX; break; }
            int Föregående_värde = 찾은여부 < 0 ? 0 : heap_värde[data_MATRIS + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(objekt_referens, (post_ANTAL + 1) * 2); data_MATRIS = heap_värde[objekt_referens + 2]; 찾은여부 = post_ANTAL; if (!fel) heap_värde[objekt_referens + 3] = post_ANTAL + 1; }
                if (!fel) { heap_värde[data_MATRIS + 2 + 2 * 찾은여부] = Nyckel_referens; heap_värde[data_MATRIS + 3 + 2 * 찾은여부] = data_värde; }
            }
            if (ta_bort && 찾은여부 >= 0) { for (int Loop_INDEX = 찾은여부 + 1; Loop_INDEX < post_ANTAL; Loop_INDEX++) { heap_värde[data_MATRIS + 2 * Loop_INDEX] = heap_värde[data_MATRIS + 2 + 2 * Loop_INDEX]; heap_värde[data_MATRIS + 1 + 2 * Loop_INDEX] = heap_värde[data_MATRIS + 3 + 2 * Loop_INDEX]; } heap_värde[data_MATRIS + 2 * post_ANTAL] = 0; heap_värde[data_MATRIS + 1 + 2 * post_ANTAL] = 0; heap_värde[objekt_referens + 3] = post_ANTAL - 1; }
            if (Ord_SMS(namn_konstant, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(Föregående_värde, 2);
            return;
        }
        fel_värde("unsupported collection method");
    }
    static boolean 잠금얻기(int objekt_referens) {
        if (!informationsteknik_giltig_objekt(objekt_referens)) return false;
        if (잠금깊이[objekt_referens] != 0 && lås_ägare[objekt_referens] != aktuellt_tråd + 1) { ändringsbegäran = true; return false; }
        lås_ägare[objekt_referens] = aktuellt_tråd + 1; 잠금깊이[objekt_referens]++; return true;
    }
    static void släppa_lås(int objekt_referens) {
        if (!informationsteknik_giltig_objekt(objekt_referens)) return;
        if (잠금깊이[objekt_referens] == 0 || lås_ägare[objekt_referens] != aktuellt_tråd + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[objekt_referens] == 0) lås_ägare[objekt_referens] = 0;
    }
    static boolean byta_tråd() {
        tråd_ram[aktuellt_tråd] = ram_INDEX;
        if (ram_INDEX < aktuellt_tråd * 32) tråd_status[aktuellt_tråd] = 3;
        for (int Loop_INDEX = 0; Loop_INDEX < antal_trådar; Loop_INDEX++) if (tråd_status[Loop_INDEX] == 2 && tråd_status[가닥대기[Loop_INDEX]] == 3) tråd_status[Loop_INDEX] = 1;
        for (int Loop_INDEX = 1; Loop_INDEX <= antal_trådar; Loop_INDEX++) {
            int Nästa_placera = (aktuellt_tråd + Loop_INDEX) % antal_trådar;
            if (tråd_status[Nästa_placera] == 1) { aktuellt_tråd = Nästa_placera; ram_INDEX = tråd_ram[Nästa_placera]; ändringsbegäran = false; return true; }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < antal_trådar; Loop_INDEX++) if (tråd_status[Loop_INDEX] != 3) { fel_värde("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int namn_konstant, int 서술상수, int kommando_KOD) { Process_tråd(namn_konstant, 서술상수, kommando_KOD, false); }
    static void Process_tråd(int namn_konstant, int 서술상수, int kommando_KOD, boolean Svenska) {
        if (kommando_KOD == 184 && Ord_SMS(namn_konstant, Svenska ? "NOMAVK_uppgift" : "yield") && Ord_SMS(서술상수, "()V")) { ändringsbegäran = true; return; }
        if (kommando_KOD == 184 && Ord_SMS(namn_konstant, "currentThread") && Ord_SMS(서술상수, "()Ljava/lang/Thread;")) { 넣기(tråd_objekt[aktuellt_tråd], 2); return; }
        if (kommando_KOD == 183 && Ord_SMS(namn_konstant, "<init>") && (Ord_SMS(서술상수, "()V") || Ord_SMS(서술상수, Svenska ? "(LSvenska/eget/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int mål_ADRESS = Ord_SMS(서술상수, "()V") ? 0 : 빼기(2), objekt_referens = 빼기(2);
            if (!informationsteknik_giltig_objekt(objekt_referens)) return;
            if (heap_värde[objekt_referens] == 13) { heap_värde[objekt_referens + 2] = mål_ADRESS; heap_referens[objekt_referens + 2] = 1; }
            else if (mål_ADRESS != 0) fel_värde("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (kommando_KOD == 182 && (Ord_SMS(namn_konstant, Svenska ? "START_uppgift" : "start") || Ord_SMS(namn_konstant, Svenska ? "기다리기" : "join")) && Ord_SMS(서술상수, "()V") || kommando_KOD == 182 && Ord_SMS(namn_konstant, Svenska ? "살아있는가" : "isAlive") && Ord_SMS(서술상수, "()Z")) {
            int objekt_referens = 빼기(2); if (!informationsteknik_giltig_objekt(objekt_referens)) return;
            int konto_värde = -1; for (int Loop_INDEX = 0; Loop_INDEX < antal_trådar; Loop_INDEX++) if (tråd_objekt[Loop_INDEX] == objekt_referens) konto_värde = Loop_INDEX;
            if (Ord_SMS(namn_konstant, Svenska ? "살아있는가" : "isAlive")) { 넣기(konto_värde >= 0 && tråd_status[konto_värde] != 3 ? 1 : 0, 1); return; }
            if (Ord_SMS(namn_konstant, Svenska ? "기다리기" : "join")) { if (konto_värde >= 0 && tråd_status[konto_värde] != 3) { 가닥대기[aktuellt_tråd] = konto_värde; tråd_status[aktuellt_tråd] = 2; ändringsbegäran = true; } return; }
            if (konto_värde >= 0) { 예외던짐(Svenska ? 38 : 16, "thread already started"); return; }
            if (antal_trådar == 4) { fel_värde("thread limit (4 including main)"); return; }
            int mål_ADRESS = heap_värde[objekt_referens] == 13 ? heap_värde[objekt_referens + 2] : objekt_referens;
            int fil_INDEX = mål_ADRESS > 0 && heap_värde[mål_ADRESS] >= 32 ? namn_metod(heap_värde[mål_ADRESS] - 32, Svenska ? "Starta" : "run", "()V") : -1;
            if (mål_ADRESS != 0 && fil_INDEX < 0) { fel_värde("Runnable.run required"); return; }
            konto_värde = antal_trådar++; tråd_objekt[konto_värde] = objekt_referens; tråd_mål[konto_värde] = mål_ADRESS;
            int ram = konto_värde * 32; tråd_ram[konto_värde] = fil_INDEX < 0 ? ram - 1 : ram; tråd_status[konto_värde] = fil_INDEX < 0 ? 3 : 1;
            if (fil_INDEX >= 0) { ram_metod[ram] = fil_INDEX; ram_placera[ram] = metod_START[fil_INDEX]; lokal_värde[ram * 128] = mål_ADRESS; lokal_Typ[ram * 128] = 2; }
            return;
        }
        fel_värde("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], ADRESS_SMS = new int[16];
    static int lokal_ADRESS() { return ADRESS_objekt(0x7f000001); }
    static int ADRESS_objekt(int värde) { int objekt_referens = allokera_minne(14, 1); if (!fel) heap_värde[objekt_referens + 2] = värde; return objekt_referens; }
    static int 주소해독(int objekt_referens) {
        if (objekt_referens == 0 || texter_lika(objekt_referens, värd_tecken("localhost"), false)) return 0x7f000001;
        if (!objekt_värde(objekt_referens, 1)) return 0;
        int data_värde = 0, summa_ANTAL = 0, ADRESS_byte = 0, 자릿수 = 0, post_ANTAL = heap_värde[objekt_referens + 1];
        for (int Loop_INDEX = 0; Loop_INDEX <= post_ANTAL; Loop_INDEX++) {
            int kodpunkt = Loop_INDEX == post_ANTAL ? '.' : heap_värde[objekt_referens + 2 + Loop_INDEX];
            if (kodpunkt == '.') { if (자릿수 == 0 || summa_ANTAL == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } data_värde = data_värde << 8 | ADRESS_byte; summa_ANTAL++; ADRESS_byte = 자릿수 = 0; }
            else { if (kodpunkt < '0' || kodpunkt > '9' || ++자릿수 > 3 || (ADRESS_byte = ADRESS_byte * 10 + kodpunkt - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (summa_ANTAL != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return data_värde;
    }
    static int ADRESS_tecken(int data_värde) {
        int post_ANTAL = 0;
        for (int skifta = 24; skifta >= 0; skifta -= 8) {
            int ADRESS_byte = data_värde >>> skifta & 255;
            if (ADRESS_byte >= 100) ADRESS_SMS[post_ANTAL++] = '0' + ADRESS_byte / 100;
            if (ADRESS_byte >= 10) ADRESS_SMS[post_ANTAL++] = '0' + ADRESS_byte / 10 % 10;
            ADRESS_SMS[post_ANTAL++] = '0' + ADRESS_byte % 10; if (skifta != 0) ADRESS_SMS[post_ANTAL++] = '.';
        }
        int objekt_referens = allokera_minne(1, post_ANTAL); if (!fel) for (int Loop_INDEX = 0; Loop_INDEX < post_ANTAL; Loop_INDEX++) heap_värde[objekt_referens + 2 + Loop_INDEX] = ADRESS_SMS[Loop_INDEX]; return objekt_referens;
    }
    static void 통신호출(int ägare, int namn_konstant, int 서술상수, int kommando_KOD) {
        if (Ord_SMS(ägare, "java/net/InetAddress")) {
            if (kommando_KOD == 184 && Ord_SMS(namn_konstant, "getLoopbackAddress") && Ord_SMS(서술상수, "()Ljava/net/InetAddress;")) { 넣기(lokal_ADRESS(), 2); return; }
            if (kommando_KOD == 184 && Ord_SMS(namn_konstant, "getByName") && Ord_SMS(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int data_värde = 주소해독(빼기(2)); if (던진객체 == 0 && !fel) 넣기(ADRESS_objekt(data_värde), 2); return;
            }
            if (kommando_KOD == 182 && Ord_SMS(namn_konstant, "getHostAddress") && Ord_SMS(서술상수, "()Ljava/lang/String;")) { int objekt_referens = 빼기(2); if (objekt_värde(objekt_referens, 14)) 넣기(ADRESS_tecken(heap_värde[objekt_referens + 2]), 2); return; }
        }
        if (Ord_SMS(ägare, "java/net/DatagramPacket")) {
            if (kommando_KOD == 183 && Ord_SMS(namn_konstant, "<init>") && (Ord_SMS(서술상수, "([BI)V") || Ord_SMS(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean mål_värde_referens = Ord_SMS(서술상수, "([BILjava/net/InetAddress;I)V"); int portnummer = mål_värde_referens ? 빼기(1) : 0, ADRESS_referens = mål_värde_referens ? 빼기(2) : 0;
                int post_ANTAL = 빼기(1), data_MATRIS = 빼기(2), objekt_referens = 빼기(2);
                if (!objekt_värde(objekt_referens, 16) || !objekt_värde(data_MATRIS, 20)) return;
                if (post_ANTAL < 0 || post_ANTAL > heap_värde[data_MATRIS + 1] || portnummer < 0 || portnummer > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (ADRESS_referens != 0 && !objekt_värde(ADRESS_referens, 14)) return;
                heap_värde[objekt_referens + 2] = data_MATRIS; heap_referens[objekt_referens + 2] = 1; heap_värde[objekt_referens + 3] = post_ANTAL;
                heap_värde[objekt_referens + 4] = ADRESS_referens; heap_referens[objekt_referens + 4] = 1; heap_värde[objekt_referens + 5] = portnummer; return;
            }
            if (kommando_KOD == 182 && Ord_SMS(namn_konstant, "setLength") && Ord_SMS(서술상수, "(I)V")) {
                int post_ANTAL = 빼기(1), objekt_referens = 빼기(2); if (!objekt_värde(objekt_referens, 16)) return;
                if (post_ANTAL < 0 || post_ANTAL > heap_värde[heap_värde[objekt_referens + 2] + 1]) 예외던짐(9, "invalid datagram length"); else heap_värde[objekt_referens + 3] = post_ANTAL; return;
            }
            if (kommando_KOD == 182 && (Ord_SMS(namn_konstant, "getData") && Ord_SMS(서술상수, "()[B") || Ord_SMS(namn_konstant, "getLength") && Ord_SMS(서술상수, "()I") || Ord_SMS(namn_konstant, "getAddress") && Ord_SMS(서술상수, "()Ljava/net/InetAddress;") || Ord_SMS(namn_konstant, "getPort") && Ord_SMS(서술상수, "()I"))) {
                int objekt_referens = 빼기(2); if (!objekt_värde(objekt_referens, 16)) return;
                int post_placera = Ord_SMS(namn_konstant, "getData") ? 2 : Ord_SMS(namn_konstant, "getLength") ? 3 : Ord_SMS(namn_konstant, "getAddress") ? 4 : 5;
                넣기(heap_värde[objekt_referens + post_placera], post_placera == 2 || post_placera == 4 ? 2 : 1); return;
            }
        }
        if (Ord_SMS(ägare, "java/net/DatagramSocket")) {
            if (kommando_KOD == 183 && Ord_SMS(namn_konstant, "<init>") && (Ord_SMS(서술상수, "()V") || Ord_SMS(서술상수, "(I)V"))) {
                int portnummer = Ord_SMS(서술상수, "()V") ? 0 : 빼기(1), objekt_referens = 빼기(2); if (!objekt_värde(objekt_referens, 15)) return;
                if (portnummer < 0 || portnummer > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = användarutrymme.skapa_nätverk(portnummer); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else heap_värde[objekt_referens + 2] = 열린파일번호; return;
            }
            if (kommando_KOD == 182 && Ord_SMS(namn_konstant, "setSoTimeout") && Ord_SMS(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), objekt_referens = 빼기(2); if (!objekt_värde(objekt_referens, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else heap_värde[objekt_referens + 3] = 밀리초값; return;
            }
            if (kommando_KOD == 182 && Ord_SMS(namn_konstant, "getLocalPort") && Ord_SMS(서술상수, "()I")) { int objekt_referens = 빼기(2); if (objekt_värde(objekt_referens, 15)) 넣기(heap_värde[objekt_referens + 2] < 0 ? -1 : användarutrymme.nätverk_port(heap_värde[objekt_referens + 2]), 1); return; }
            if (kommando_KOD == 182 && Ord_SMS(namn_konstant, "isClosed") && Ord_SMS(서술상수, "()Z")) { int objekt_referens = 빼기(2); if (objekt_värde(objekt_referens, 15)) 넣기(heap_värde[objekt_referens + 2] < 0 ? 1 : 0, 1); return; }
            if (kommando_KOD == 182 && Ord_SMS(namn_konstant, "close") && Ord_SMS(서술상수, "()V")) { int objekt_referens = 빼기(2); if (objekt_värde(objekt_referens, 15) && heap_värde[objekt_referens + 2] >= 0) { användarutrymme.파일서술자닫기(heap_värde[objekt_referens + 2]); heap_värde[objekt_referens + 2] = -1; } return; }
            if (kommando_KOD == 182 && (Ord_SMS(namn_konstant, "send") || Ord_SMS(namn_konstant, "receive")) && Ord_SMS(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int paket = 빼기(2), objekt_referens = 빼기(2); if (!objekt_värde(paket, 16) || !objekt_värde(objekt_referens, 15)) return;
                int data_MATRIS = heap_värde[paket + 2], giltig_längd = heap_värde[paket + 3], 열린파일번호 = heap_värde[objekt_referens + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Ord_SMS(namn_konstant, "send")) {
                    if (!objekt_värde(heap_värde[paket + 4], 14)) return;
                    if (giltig_längd > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < giltig_längd; Loop_INDEX++) 통신임시[Loop_INDEX] = heap_värde[data_MATRIS + 2 + Loop_INDEX];
                    if (användarutrymme.skicka_nätverk(열린파일번호, heap_värde[heap_värde[paket + 4] + 2], heap_värde[paket + 5], 통신임시, giltig_längd) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int post_ANTAL = användarutrymme.få_nätverk(열린파일번호, 통신임시, giltig_längd > 512 ? 512 : giltig_längd);
                    if (post_ANTAL == -11) {
                        int aktuell_tid = användarutrymme.밀리초();
                        if (heap_värde[objekt_referens + 4] == 0) heap_värde[objekt_referens + 4] = aktuell_tid + 1;
                        if (heap_värde[objekt_referens + 3] > 0 && aktuell_tid - (heap_värde[objekt_referens + 4] - 1) >= heap_värde[objekt_referens + 3]) { heap_värde[objekt_referens + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(objekt_referens, 2); 넣기(paket, 2); ram_placera[ram_INDEX] = ram_instruktion[ram_INDEX]; ändringsbegäran = true; return;
                    }
                    heap_värde[objekt_referens + 4] = 0;
                    if (post_ANTAL < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < post_ANTAL; Loop_INDEX++) heap_värde[data_MATRIS + 2 + Loop_INDEX] = (byte)통신임시[Loop_INDEX];
                    heap_värde[paket + 3] = post_ANTAL; heap_värde[paket + 4] = ADRESS_objekt(통신임시[513]); heap_referens[paket + 4] = 1; heap_värde[paket + 5] = 통신임시[512];
                }
                return;
            }
        }
        fel_värde("unsupported java.net method");
    }
    static boolean 흐름대기(int objekt_referens) {
        int aktuell_tid = användarutrymme.밀리초();
        if (heap_värde[objekt_referens + 5] == 0) heap_värde[objekt_referens + 5] = aktuell_tid + 1;
        if (heap_värde[objekt_referens + 3] > 0 && aktuell_tid - (heap_värde[objekt_referens + 5] - 1) >= heap_värde[objekt_referens + 3]) { heap_värde[objekt_referens + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        ram_placera[ram_INDEX] = ram_instruktion[ram_INDEX]; ändringsbegäran = true; return true;
    }
    static void 흐름호출(int ägare, int namn_konstant, int 서술상수, int kommando_KOD) {
        boolean få_page = Ord_SMS(ägare, "java/net/ServerSocket"), flöde = Ord_SMS(ägare, "java/io/InputStream") || Ord_SMS(ägare, "java/io/OutputStream");
        if (!flöde && kommando_KOD == 183 && Ord_SMS(namn_konstant, "<init>")) {
            boolean 빈여부 = Ord_SMS(서술상수, "()V"), 이름지정여부 = Ord_SMS(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = Ord_SMS(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(빈여부 || få_page && Ord_SMS(서술상수, "(I)V") || !få_page && (이름지정여부 || 주소지정여부))) { fel_värde("unsupported socket constructor"); return; }
            int portnummer = 빈여부 ? 0 : 빼기(1), ADRESS_referens = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, objekt_referens = 빼기(2);
            if (!objekt_värde(objekt_referens, få_page ? 18 : 17)) return;
            if (portnummer < 0 || portnummer > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !objekt_värde(ADRESS_referens, 14)) return;
            int Nätverks_ID = 이름지정여부 ? 주소해독(ADRESS_referens) : 주소지정여부 ? heap_värde[ADRESS_referens + 2] : 0x7f000001;
            if (fel || 던진객체 != 0) return;
            int 열린파일번호 = användarutrymme.flöde_kontroll(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = 빈여부 ? 0 : få_page ? användarutrymme.flöde_kontroll(1, 열린파일번호, portnummer) : användarutrymme.ANSLUT_flöde(열린파일번호, Nätverks_ID, portnummer);
            if (처리값 < 0) { användarutrymme.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            heap_värde[objekt_referens + 2] = 열린파일번호; heap_värde[objekt_referens + 4] = portnummer; heap_värde[objekt_referens + 6] = 빈여부 ? 0 : 1; return;
        }
        if (!flöde && Ord_SMS(namn_konstant, "setSoTimeout") && Ord_SMS(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), objekt_referens = 빼기(2); if (!objekt_värde(objekt_referens, få_page ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else heap_värde[objekt_referens + 3] = 밀리초값; return; }
        if (!flöde && Ord_SMS(namn_konstant, "close") && Ord_SMS(서술상수, "()V")) { int objekt_referens = 빼기(2); if (objekt_värde(objekt_referens, få_page ? 18 : 17) && heap_värde[objekt_referens + 2] >= 0) { användarutrymme.파일서술자닫기(heap_värde[objekt_referens + 2]); heap_värde[objekt_referens + 2] = -1; } return; }
        if (!flöde && (Ord_SMS(namn_konstant, "getLocalPort") || Ord_SMS(namn_konstant, "getPort") || Ord_SMS(namn_konstant, "isClosed") || Ord_SMS(namn_konstant, "isConnected"))) {
            int objekt_referens = 빼기(2); if (!objekt_värde(objekt_referens, få_page ? 18 : 17)) return;
            넣기(Ord_SMS(namn_konstant, "isClosed") ? heap_värde[objekt_referens + 2] < 0 ? 1 : 0 : Ord_SMS(namn_konstant, "isConnected") ? heap_värde[objekt_referens + 6] : Ord_SMS(namn_konstant, "getPort") ? heap_värde[objekt_referens + 4] : heap_värde[objekt_referens + 2] < 0 ? -1 : användarutrymme.flöde_kontroll(4, heap_värde[objekt_referens + 2], 0), 1); return;
        }
        if (få_page && Ord_SMS(namn_konstant, "accept") && Ord_SMS(서술상수, "()Ljava/net/Socket;")) {
            int objekt_referens = 빼기(2); if (!objekt_värde(objekt_referens, 18)) return; int 열린파일번호 = användarutrymme.flöde_kontroll(3, heap_värde[objekt_referens + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(objekt_referens)) 넣기(objekt_referens, 2); return; }
            heap_värde[objekt_referens + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = allokera_minne(17, 5); if (fel) { användarutrymme.파일서술자닫기(열린파일번호); return; } heap_värde[반환값 + 2] = 열린파일번호; heap_värde[반환값 + 4] = användarutrymme.flöde_kontroll(5, 열린파일번호, 0); heap_värde[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!få_page && !flöde && ((Ord_SMS(namn_konstant, "getInputStream") && Ord_SMS(서술상수, "()Ljava/io/InputStream;")) || (Ord_SMS(namn_konstant, "getOutputStream") && Ord_SMS(서술상수, "()Ljava/io/OutputStream;")))) {
            int objekt_referens = 빼기(2); if (!objekt_värde(objekt_referens, 17)) return; if (heap_värde[objekt_referens + 2] < 0 || heap_värde[objekt_referens + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = allokera_minne(19, 4); if (fel) return; heap_värde[반환값 + 2] = objekt_referens; heap_referens[반환값 + 2] = 1; heap_värde[반환값 + 3] = Ord_SMS(namn_konstant, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (flöde) {
            boolean 읽기여부 = Ord_SMS(namn_konstant, "read"), informationsteknik_skriva_åtgärd = Ord_SMS(namn_konstant, "write"), block = Ord_SMS(서술상수, "([B)I") || Ord_SMS(서술상수, "([B)V"), informationsteknik_DELMATRIS = Ord_SMS(서술상수, "([BII)I") || Ord_SMS(서술상수, "([BII)V");
            int post_ANTAL = informationsteknik_DELMATRIS ? 빼기(1) : 0, 시작변위 = informationsteknik_DELMATRIS ? 빼기(1) : 0, data_MATRIS = block || informationsteknik_DELMATRIS ? 빼기(2) : 0;
            int data_värde = informationsteknik_skriva_åtgärd && Ord_SMS(서술상수, "(I)V") ? 빼기(1) : 0, objekt_referens = 빼기(2);
            if (!objekt_värde(objekt_referens, 19)) return; int överordnad_referens = heap_värde[objekt_referens + 2], 열린파일번호 = heap_värde[överordnad_referens + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Ord_SMS(namn_konstant, "close") && Ord_SMS(서술상수, "()V")) { användarutrymme.파일서술자닫기(열린파일번호); heap_värde[överordnad_referens + 2] = -1; return; }
            if (Ord_SMS(namn_konstant, "flush") && Ord_SMS(서술상수, "()V")) return;
            if ((!읽기여부 && !informationsteknik_skriva_åtgärd) || 읽기여부 != (heap_värde[objekt_referens + 3] == 0)) { fel_värde("unsupported stream operation"); return; }
            if (block || informationsteknik_DELMATRIS) { if (!objekt_värde(data_MATRIS, 20)) return; if (block) post_ANTAL = heap_värde[data_MATRIS + 1]; if (시작변위 < 0 || post_ANTAL < 0 || 시작변위 > heap_värde[data_MATRIS + 1] - post_ANTAL) { 예외던짐(6, "stream array bounds"); return; } }
            else post_ANTAL = 1;
            if (post_ANTAL == 0) { if (읽기여부) 넣기(0, 1); return; }
            int Slutfört_ANTAL = informationsteknik_skriva_åtgärd ? heap_värde[objekt_referens + 4] : 0, 처리값 = 0;
            while (Slutfört_ANTAL < post_ANTAL) {
                처리값 = 읽기여부 ? användarutrymme.파일한바이트읽기(열린파일번호) : användarutrymme.파일한바이트쓰기(열린파일번호, block || informationsteknik_DELMATRIS ? heap_värde[data_MATRIS + 2 + 시작변위 + Slutfört_ANTAL] : data_värde);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (block || informationsteknik_DELMATRIS)) heap_värde[data_MATRIS + 2 + 시작변위 + Slutfört_ANTAL] = (byte)처리값;
                Slutfört_ANTAL++; if (읽기여부 && !(block || informationsteknik_DELMATRIS)) break;
            }
            if (처리값 == -11 && (informationsteknik_skriva_åtgärd || Slutfört_ANTAL == 0)) {
                heap_värde[objekt_referens + 4] = Slutfört_ANTAL;
                if (흐름대기(överordnad_referens)) { 넣기(objekt_referens, 2); if (block || informationsteknik_DELMATRIS) 넣기(data_MATRIS, 2); if (informationsteknik_DELMATRIS) { 넣기(시작변위, 1); 넣기(post_ANTAL, 1); } if (informationsteknik_skriva_åtgärd && !(block || informationsteknik_DELMATRIS)) 넣기(data_värde, 1); } return;
            }
            heap_värde[objekt_referens + 4] = 0; heap_värde[överordnad_referens + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(Slutfört_ANTAL == 0 && 처리값 == 256 ? -1 : block || informationsteknik_DELMATRIS ? Slutfört_ANTAL : 처리값, 1); return;
        }
        fel_värde("unsupported Socket/ServerSocket method");
    }
    static int[] skärmbild_referens = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int namn_konstant) {
        if (Ord_SMS(namn_konstant, "Svenska/eget/Fönster")) return 24;
        if (Ord_SMS(namn_konstant, "Svenska/eget/Etikett")) return 26;
        if (Ord_SMS(namn_konstant, "Svenska/eget/knapp")) return 27;
        if (Ord_SMS(namn_konstant, "Svenska/eget/textfält")) return 28;
        if (Ord_SMS(namn_konstant, "Svenska/eget/동작알림")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int namn_konstant) {
        return 한국어화면종(namn_konstant) != 0 || Ord_SMS(namn_konstant, "Svenska/eget/skärmbild_element") || Ord_SMS(namn_konstant, "Svenska/eget/händelse_kö");
    }
    static int skärmbild_Kurs(int namn_konstant) {
        int 한국어종 = 한국어화면종(namn_konstant); if (한국어종 != 0) return 한국어종;
        if (Ord_SMS(namn_konstant, "javax/swing/JFrame")) return 24;
        if (Ord_SMS(namn_konstant, "javax/swing/JPanel")) return 25;
        if (Ord_SMS(namn_konstant, "javax/swing/JLabel")) return 26;
        if (Ord_SMS(namn_konstant, "javax/swing/JButton")) return 27;
        if (Ord_SMS(namn_konstant, "javax/swing/JTextField")) return 28;
        if (Ord_SMS(namn_konstant, "java/awt/event/ActionEvent")) return 29;
        if (Ord_SMS(namn_konstant, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean skärmbild_ägare(int namn_konstant) {
        return skärmbild_Kurs(namn_konstant) != 0 || Ord_SMS(namn_konstant, "java/awt/Component") || Ord_SMS(namn_konstant, "java/awt/Container") || Ord_SMS(namn_konstant, "javax/swing/JComponent") || Ord_SMS(namn_konstant, "javax/swing/AbstractButton") || Ord_SMS(namn_konstant, "javax/swing/text/JTextComponent") || Ord_SMS(namn_konstant, "javax/swing/SwingUtilities");
    }
    static boolean skärmbild_objekt(int objekt_referens) { if (!informationsteknik_giltig_objekt(objekt_referens)) return false; if (heap_värde[objekt_referens] < 24 || heap_värde[objekt_referens] > 28) { fel_värde("unsupported Swing receiver"); return false; } return true; }
    static void uppsättning_skärmbild_tecken(int objekt_referens, int SMS_referens) {
        if (SMS_referens != 0 && !objekt_värde(SMS_referens, 1)) return;
        int post_ANTAL = SMS_referens == 0 ? 0 : heap_värde[SMS_referens + 1]; if (post_ANTAL > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < post_ANTAL; Loop_INDEX++) 화면글임시[Loop_INDEX] = heap_värde[SMS_referens + 2 + Loop_INDEX];
        if (användarutrymme.skärmbild_SMS(heap_värde[objekt_referens + 2], 화면글임시, post_ANTAL) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        heap_värde[objekt_referens + 3] = SMS_referens; heap_referens[objekt_referens + 3] = 1;
    }
    static int läsa_skärmbild_tecken(int objekt_referens) {
        int konto_värde = heap_värde[objekt_referens + 2], post_ANTAL = användarutrymme.skärmbild_kontakt(8, konto_värde, 0, 0, 0, 0), 사용수 = 0;
        if (post_ANTAL < 0) { fel_värde("GUI text read failed"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < post_ANTAL; Loop_INDEX++) { int 부호값 = användarutrymme.skärmbild_kontakt(9, konto_värde, Loop_INDEX, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = allokera_minne(1, 사용수); if (!fel) for (int Loop_INDEX = 0; Loop_INDEX < 사용수; Loop_INDEX++) heap_värde[반환값 + 2 + Loop_INDEX] = 화면글임시[Loop_INDEX]; return 반환값;
    }
    /* Svenska 객체를 직접 만들고 kärna_värde skärmbild 기능에 연결한다. Swing objekt_värde/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int ägare, int namn_konstant, int 서술상수, int kommando_KOD) {
        if (Ord_SMS(ägare, "Svenska/eget/händelse_kö")) {
            if (kommando_KOD == 184 && Ord_SMS(namn_konstant, "나중에실행") && Ord_SMS(서술상수, "(LSvenska/eget/실행할일;)V")) {
                int uppgift_Action = 빼기(2); if (!informationsteknik_giltig_objekt(uppgift_Action)) return;
                if (나중수 == 8) { fel_värde("skärmbild 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = uppgift_Action; return;
            }
            if (kommando_KOD == 184 && Ord_SMS(namn_konstant, "사건처리중인가") && Ord_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            fel_värde("지원하지 않는 Svenska skärmbild 일정 호출"); return;
        }
        if (Ord_SMS(ägare, "Svenska/eget/동작알림")) {
            int 알림 = 빼기(2); if (!objekt_värde(알림, 29) || heap_värde[알림 + 3] == 0) return;
            if (Ord_SMS(namn_konstant, "händelsekälla") && Ord_SMS(서술상수, "()LSvenska/eget/skärmbild_element;")) 넣기(heap_värde[알림 + 2], 2);
            else if (Ord_SMS(namn_konstant, "kommando_SMS") && Ord_SMS(서술상수, "()Ljava/lang/String;")) 넣기(läsa_skärmbild_tecken(heap_värde[알림 + 2]), 2);
            else if (Ord_SMS(namn_konstant, "INDEX") && Ord_SMS(서술상수, "()I")) 넣기(1001, 1);
            else fel_värde("지원하지 않는 Svenska Åtgärd 알림 호출"); return;
        }
        if (kommando_KOD == 183 && Ord_SMS(namn_konstant, "<init>")) {
            int variant_värde = 한국어화면종(ägare), 받이 = 0, 가로 = 0, bransch_placera = 0, 폭 = 0, 높이 = 0;
            if (variant_värde == 24 && Ord_SMS(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (användarutrymme.화면너비() - 폭) / 2; bransch_placera = (användarutrymme.화면높이() - 높이) / 2;
            } else if ((variant_värde == 26 || variant_värde == 28) && Ord_SMS(서술상수, "(Ljava/lang/String;IIII)V") || variant_värde == 27 && Ord_SMS(서술상수, "(Ljava/lang/String;IIIILSvenska/eget/동작받이;)V")) {
                if (variant_värde == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); bransch_placera = 빼기(1); 가로 = 빼기(1);
            } else { fel_värde("지원하지 않는 Svenska skärmbild 생성자"); return; }
            int text = 빼기(2), element_värde = 빼기(2); if (!skärmbild_objekt(element_värde)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || bransch_placera < 0 || 폭 > användarutrymme.화면너비() - 가로 || 높이 > användarutrymme.화면높이() - bransch_placera) { 예외던짐(27, "skärmbild 영역을 벗어난 크기입니다"); return; }
            int INDEX = användarutrymme.skärmbild_kontakt(0, variant_värde - 23, 0, 0, 0, 0);
            if (INDEX < 1 || INDEX > 32) { fel_värde("skärmbild element_värde 자리가 가득 찼습니다"); return; }
            heap_värde[element_värde + 2] = INDEX; skärmbild_referens[INDEX - 1] = element_värde;
            heap_värde[element_värde + 5] = 가로; heap_värde[element_värde + 6] = bransch_placera; heap_värde[element_värde + 7] = 폭; heap_värde[element_värde + 8] = 높이; heap_värde[element_värde + 10] = 2;
            heap_värde[element_värde + 4] = 받이; heap_referens[element_värde + 4] = 1; heap_värde[element_värde + 12] = 1;
            användarutrymme.skärmbild_kontakt(1, INDEX, 가로, bransch_placera, 폭, 높이);
            if (variant_värde == 24) användarutrymme.skärmbild_kontakt(7, INDEX, 2, 0, 0, 0);
            uppsättning_skärmbild_tecken(element_värde, text); return;
        }
        if (kommando_KOD != 182) { fel_värde("잘못된 Svenska skärmbild 호출 kommando"); return; }
        if (Ord_SMS(namn_konstant, "skriva_SMS") && Ord_SMS(서술상수, "(Ljava/lang/String;)V")) {
            int text = 빼기(2), element_värde = 빼기(2); if (skärmbild_objekt(element_värde)) uppsättning_skärmbild_tecken(element_värde, text); return;
        }
        if (Ord_SMS(namn_konstant, "läsa_SMS") && Ord_SMS(서술상수, "()Ljava/lang/String;")) {
            int element_värde = 빼기(2); if (skärmbild_objekt(element_värde)) 넣기(läsa_skärmbild_tecken(element_värde), 2); return;
        }
        if (Ord_SMS(namn_konstant, "동작맡기기") && Ord_SMS(서술상수, "(LSvenska/eget/동작받이;)V")) {
            int 받이 = 빼기(2), element_värde = 빼기(2);
            if (skärmbild_objekt(element_värde)) { heap_värde[element_värde + 4] = 받이; heap_referens[element_värde + 4] = 1; heap_värde[element_värde + 12] = 1; } return;
        }
        if (Ord_SMS(namn_konstant, "Lägg_till_element") && Ord_SMS(서술상수, "(LSvenska/eget/skärmbild_element;)V")) {
            int barn_värde = 빼기(2), överordnad_värde = 빼기(2); if (!skärmbild_objekt(barn_värde) || !skärmbild_objekt(överordnad_värde)) return;
            if (användarutrymme.skärmbild_kontakt(2, heap_värde[överordnad_värde + 2], heap_värde[barn_värde + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 skärmbild 부모입니다"); return; }
            heap_värde[barn_värde + 11] = överordnad_värde; heap_referens[barn_värde + 11] = 1; return;
        }
        if (Ord_SMS(namn_konstant, "자리정하기") && Ord_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), bransch_placera = 빼기(1), 가로 = 빼기(1), element_värde = 빼기(2); if (!skärmbild_objekt(element_värde)) return;
            if (användarutrymme.skärmbild_kontakt(1, heap_värde[element_värde + 2], 가로, bransch_placera, 폭, 높이) < 0) { 예외던짐(27, "skärmbild 영역을 벗어난 자리입니다"); return; }
            heap_värde[element_värde + 5] = 가로; heap_värde[element_värde + 6] = bransch_placera; heap_värde[element_värde + 7] = 폭; heap_värde[element_värde + 8] = 높이; return;
        }
        if ((Ord_SMS(namn_konstant, "visa_fönster") || Ord_SMS(namn_konstant, "Stäng")) && Ord_SMS(서술상수, "()V")) {
            boolean Synlighet_värde = Ord_SMS(namn_konstant, "visa_fönster"); int element_värde = 빼기(2); if (!skärmbild_objekt(element_värde)) return;
            if (användarutrymme.skärmbild_kontakt(Synlighet_värde ? 3 : 4, heap_värde[element_värde + 2], Synlighet_värde ? 1 : 0, 0, 0, 0) < 0) { fel_värde("화면은 interaktiv 명령에서 실행해야 합니다"); return; }
            heap_värde[element_värde + 9] = Synlighet_värde ? 1 : 0; return;
        }
        if (Ord_SMS(namn_konstant, "보이는가") && Ord_SMS(서술상수, "()Z")) { int element_värde = 빼기(2); if (skärmbild_objekt(element_värde)) 넣기(heap_värde[element_värde + 9], 1); return; }
        fel_värde("지원하지 않는 Svenska skärmbild metod_värde");
    }
    static void 화면호출(int ägare, int namn_konstant, int 서술상수, int kommando_KOD) {
        if (Ord_SMS(ägare, "javax/swing/SwingUtilities")) {
            if (kommando_KOD == 184 && Ord_SMS(namn_konstant, "invokeLater") && Ord_SMS(서술상수, "(Ljava/lang/Runnable;)V")) { int objekt_referens = 빼기(2); if (!informationsteknik_giltig_objekt(objekt_referens)) return; if (나중수 == 8) { fel_värde("invokeLater queue full"); return; } 나중실행[나중수++] = objekt_referens; return; }
            if (kommando_KOD == 184 && Ord_SMS(namn_konstant, "isEventDispatchThread") && Ord_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            fel_värde("unsupported SwingUtilities method"); return;
        }
        if (Ord_SMS(ägare, "java/awt/event/ActionEvent")) {
            int objekt_referens = 빼기(2); if (!objekt_värde(objekt_referens, 29)) return;
            if (Ord_SMS(namn_konstant, "getSource") && Ord_SMS(서술상수, "()Ljava/lang/Object;")) 넣기(heap_värde[objekt_referens + 2], 2);
            else if (Ord_SMS(namn_konstant, "getActionCommand") && Ord_SMS(서술상수, "()Ljava/lang/String;")) 넣기(läsa_skärmbild_tecken(heap_värde[objekt_referens + 2]), 2);
            else if (Ord_SMS(namn_konstant, "getID") && Ord_SMS(서술상수, "()I")) 넣기(1001, 1);
            else fel_värde("unsupported ActionEvent method"); return;
        }
        if (kommando_KOD == 183 && Ord_SMS(namn_konstant, "<init>")) {
            int KOLUMNER = 0, SMS_referens = 0;
            if (Ord_SMS(서술상수, "(I)V")) KOLUMNER = 빼기(1);
            else if (Ord_SMS(서술상수, "(Ljava/lang/String;I)V")) { KOLUMNER = 빼기(1); SMS_referens = 빼기(2); }
            else if (Ord_SMS(서술상수, "(Ljava/lang/String;)V")) SMS_referens = 빼기(2);
            else if (Ord_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Ord_SMS(서술상수, "()V")) { fel_värde("unsupported Swing constructor"); return; }
            int objekt_referens = 빼기(2); if (!informationsteknik_giltig_objekt(objekt_referens)) return;
            if (heap_värde[objekt_referens] == 30) { fel_värde("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!skärmbild_objekt(objekt_referens) || KOLUMNER < 0) return;
            int konto_värde = användarutrymme.skärmbild_kontakt(0, heap_värde[objekt_referens] - 23, 0, 0, 0, 0);
            if (konto_värde < 1 || konto_värde > 32) { fel_värde("GUI widget slots exhausted"); return; }
            heap_värde[objekt_referens + 2] = konto_värde; skärmbild_referens[konto_värde - 1] = objekt_referens; heap_värde[objekt_referens + 5] = heap_värde[objekt_referens] == 24 ? 130 : 16; heap_värde[objekt_referens + 6] = heap_värde[objekt_referens] == 24 ? 110 : 16;
            heap_värde[objekt_referens + 7] = heap_värde[objekt_referens] == 24 ? 380 : 220; heap_värde[objekt_referens + 8] = heap_värde[objekt_referens] == 24 ? 240 : 28; heap_värde[objekt_referens + 10] = 1;
            uppsättning_skärmbild_tecken(objekt_referens, SMS_referens); return;
        }
        if (Ord_SMS(namn_konstant, "setText") || Ord_SMS(namn_konstant, "setTitle")) { int SMS_referens = 빼기(2), objekt_referens = 빼기(2); if (skärmbild_objekt(objekt_referens) && Ord_SMS(서술상수, "(Ljava/lang/String;)V")) uppsättning_skärmbild_tecken(objekt_referens, SMS_referens); return; }
        if (Ord_SMS(namn_konstant, "getText") || Ord_SMS(namn_konstant, "getTitle")) { int objekt_referens = 빼기(2); if (skärmbild_objekt(objekt_referens) && Ord_SMS(서술상수, "()Ljava/lang/String;")) 넣기(läsa_skärmbild_tecken(objekt_referens), 2); return; }
        if (Ord_SMS(namn_konstant, "addActionListener") && Ord_SMS(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int få_referens = 빼기(2), objekt_referens = 빼기(2); if (skärmbild_objekt(objekt_referens)) { heap_värde[objekt_referens + 4] = få_referens; heap_referens[objekt_referens + 4] = 1; } return; }
        if (Ord_SMS(namn_konstant, "getContentPane") && Ord_SMS(서술상수, "()Ljava/awt/Container;")) { int objekt_referens = 빼기(2); if (skärmbild_objekt(objekt_referens)) 넣기(objekt_referens, 2); return; }
        if (Ord_SMS(namn_konstant, "setLayout") && Ord_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) { int Layout_referens = 빼기(2), objekt_referens = 빼기(2); if (skärmbild_objekt(objekt_referens) && Layout_referens != 0) fel_värde("only absolute layout (null) is supported"); return; }
        if (Ord_SMS(namn_konstant, "add") && (Ord_SMS(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || Ord_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean Layout_villkor = Ord_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (Layout_villkor) 빼기(2);
            int barn_referens = 빼기(2), objekt_referens = 빼기(2); if (!skärmbild_objekt(barn_referens) || !skärmbild_objekt(objekt_referens)) return;
            if (användarutrymme.skärmbild_kontakt(2, heap_värde[objekt_referens + 2], heap_värde[barn_referens + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            heap_värde[barn_referens + 11] = objekt_referens; heap_referens[barn_referens + 11] = 1; if (!Layout_villkor) 넣기(barn_referens, 2); return;
        }
        if (Ord_SMS(namn_konstant, "setBounds") && Ord_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), Y_koordinat = 빼기(1), x_koordinat = 빼기(1), objekt_referens = 빼기(2); if (!skärmbild_objekt(objekt_referens)) return;
            if (användarutrymme.skärmbild_kontakt(1, heap_värde[objekt_referens + 2], x_koordinat, Y_koordinat, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            heap_värde[objekt_referens + 5] = x_koordinat; heap_värde[objekt_referens + 6] = Y_koordinat; heap_värde[objekt_referens + 7] = 너비; heap_värde[objekt_referens + 8] = 높이; return;
        }
        if (Ord_SMS(namn_konstant, "setSize") && Ord_SMS(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), objekt_referens = 빼기(2); if (!skärmbild_objekt(objekt_referens)) return;
            if (användarutrymme.skärmbild_kontakt(1, heap_värde[objekt_referens + 2], heap_värde[objekt_referens + 5], heap_värde[objekt_referens + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { heap_värde[objekt_referens + 7] = 너비; heap_värde[objekt_referens + 8] = 높이; } return;
        }
        if (Ord_SMS(namn_konstant, "setLocationRelativeTo") && Ord_SMS(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), objekt_referens = 빼기(2); if (!skärmbild_objekt(objekt_referens)) return; if (상대배치 != 0) { fel_värde("only screen centering supported"); return; } heap_värde[objekt_referens + 5] = (användarutrymme.화면너비() - heap_värde[objekt_referens + 7]) / 2; heap_värde[objekt_referens + 6] = (användarutrymme.화면높이() - heap_värde[objekt_referens + 8]) / 2; användarutrymme.skärmbild_kontakt(1, heap_värde[objekt_referens + 2], heap_värde[objekt_referens + 5], heap_värde[objekt_referens + 6], heap_värde[objekt_referens + 7], heap_värde[objekt_referens + 8]); return; }
        if (Ord_SMS(namn_konstant, "setDefaultCloseOperation") && Ord_SMS(서술상수, "(I)V")) { int Policy = 빼기(1), objekt_referens = 빼기(2); if (skärmbild_objekt(objekt_referens)) { if (Policy < 0 || Policy > 3) 예외던짐(9, "close policy"); else { heap_värde[objekt_referens + 10] = Policy; användarutrymme.skärmbild_kontakt(7, heap_värde[objekt_referens + 2], Policy, 0, 0, 0); } } return; }
        if (Ord_SMS(namn_konstant, "setVisible") && Ord_SMS(서술상수, "(Z)V")) { int data_värde = 빼기(1), objekt_referens = 빼기(2); if (skärmbild_objekt(objekt_referens)) { int 처리값 = användarutrymme.skärmbild_kontakt(3, heap_värde[objekt_referens + 2], data_värde, 0, 0, 0); if (처리값 < 0) fel_värde("Swing requires a standalone interactive command"); else heap_värde[objekt_referens + 9] = data_värde; } return; }
        if (Ord_SMS(namn_konstant, "dispose") && Ord_SMS(서술상수, "()V")) { int objekt_referens = 빼기(2); if (skärmbild_objekt(objekt_referens)) { användarutrymme.skärmbild_kontakt(4, heap_värde[objekt_referens + 2], 0, 0, 0, 0); heap_värde[objekt_referens + 9] = 0; } return; }
        if (Ord_SMS(namn_konstant, "repaint") || Ord_SMS(namn_konstant, "validate")) { int objekt_referens = 빼기(2); if (!skärmbild_objekt(objekt_referens) || !Ord_SMS(서술상수, "()V")) return; användarutrymme.skärmbild_kontakt(1, heap_värde[objekt_referens + 2], heap_värde[objekt_referens + 5], heap_värde[objekt_referens + 6], heap_värde[objekt_referens + 7], heap_värde[objekt_referens + 8]); return; }
        if (Ord_SMS(namn_konstant, "isVisible") && Ord_SMS(서술상수, "()Z")) { int objekt_referens = 빼기(2); if (skärmbild_objekt(objekt_referens)) 넣기(heap_värde[objekt_referens + 9], 1); return; }
        fel_värde("unsupported Swing method (native subset)");
    }
    static void skicka_ut_händelse(int mål_ADRESS, int händelse_nummer, boolean Svenska) {
        if (mål_ADRESS < 1 || heap_värde[mål_ADRESS] < 32) { fel_värde("Java event listener required"); return; }
        int fil_INDEX = namn_metod(heap_värde[mål_ADRESS] - 32, händelse_nummer == 0 ? (Svenska ? "Starta" : "run") : (Svenska ? "få_Action" : "actionPerformed"), händelse_nummer == 0 ? "()V" : (Svenska ? "(LSvenska/eget/동작알림;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (fil_INDEX < 0) { fel_värde("event callback missing"); return; }
        aktuellt_tråd = 0; antal_trådar = 1; ram_INDEX = 0; tråd_status[0] = 1; ram_Stack[0] = 0; ram_lås[0] = starta_ram[0] = 0; ändringsbegäran = false;
        for (int Loop_INDEX = 0; Loop_INDEX < 128; Loop_INDEX++) { lokal_värde[Loop_INDEX] = lokal_Typ[Loop_INDEX] = 0; }
        ram_metod[0] = fil_INDEX; ram_placera[0] = metod_START[fil_INDEX]; lokal_värde[0] = mål_ADRESS; lokal_Typ[0] = 2;
        if (händelse_nummer != 0) { lokal_värde[1] = händelse_nummer; lokal_Typ[1] = 2; }
        사건중 = true; köra_kommando(); 사건중 = false;
    }
    static void skärmbild_Händelser() {
        while (!fel) {
            if (나중수 > 0) { int mål_ADRESS = 나중실행[0], Svenska = 나중한국어[0]; for (int Loop_INDEX = 1; Loop_INDEX < 나중수; Loop_INDEX++) { 나중실행[Loop_INDEX - 1] = 나중실행[Loop_INDEX]; 나중한국어[Loop_INDEX - 1] = 나중한국어[Loop_INDEX]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; skicka_ut_händelse(mål_ADRESS, 0, Svenska != 0); continue; }
            if (användarutrymme.skärmbild_kontakt(6, 0, 0, 0, 0, 0) == 0) return;
            int händelse_nummer = användarutrymme.skärmbild_kontakt(5, 0, 0, 0, 0, 0); if (händelse_nummer == 0) continue;
            if (händelse_nummer < 0) { fel_värde("GUI event I/O failed"); return; }
            int konto_värde = händelse_nummer & 65535; if (konto_värde < 1 || konto_värde > 32) continue; int objekt_referens = skärmbild_referens[konto_värde - 1]; if (objekt_referens == 0) continue;
            if ((händelse_nummer & 65536) != 0) {
                if (heap_värde[objekt_referens + 10] != 0) heap_värde[objekt_referens + 9] = 0;
                if (heap_värde[objekt_referens + 10] == 3) for (int Loop_INDEX = 0; Loop_INDEX < 32; Loop_INDEX++) if (skärmbild_referens[Loop_INDEX] != 0 && heap_värde[skärmbild_referens[Loop_INDEX]] == 24) användarutrymme.skärmbild_kontakt(4, Loop_INDEX + 1, 0, 0, 0, 0);
            } else if (heap_värde[objekt_referens + 4] != 0) {
                int VIKTIGT_referens = allokera_minne(29, 2); if (fel) return; heap_värde[VIKTIGT_referens + 2] = objekt_referens; heap_värde[VIKTIGT_referens + 3] = heap_värde[objekt_referens + 12]; heap_referens[VIKTIGT_referens + 2] = 1; skicka_ut_händelse(heap_värde[objekt_referens + 4], VIKTIGT_referens, heap_värde[objekt_referens + 12] != 0);
            }
        }
    }
    public static int Kör() {
        if (användarutrymme.인수개수() == 1 && 자바도구.같음(användarutrymme.argument(0), "-version")) {
            användarutrymme.Skriv("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (användarutrymme.인수개수() < 1) { användarutrymme.Skriv("Usage: java CLASS [ARGS]\n"); return 2; }
        post_Kurs_Definition = dossier_Kurs_Definition(värd_tecken(användarutrymme.argument(0))); if (fel || post_Kurs_Definition < 0) return 1;
        int startpunkt_värde = namn_metod(post_Kurs_Definition, "Kör", "()V");
        boolean 한국어진입 = startpunkt_värde >= 0 && (metod_ansluta[startpunkt_värde] & 9) == 9;
        if (!한국어진입) startpunkt_värde = namn_metod(post_Kurs_Definition, "main", "([Ljava/lang/String;)V");
        if (startpunkt_värde < 0 || (metod_ansluta[startpunkt_värde] & 9) != 9) fel_värde("public static void Kör() or main(String[] args) required");
        if (fel) return 1;
        int argument = allokera_minne(3, användarutrymme.인수개수() - 1); matriselement[argument] = -1;
        for (int nummer = 1; nummer < användarutrymme.인수개수() && !fel; nummer++) heap_värde[argument + 1 + nummer] = värd_tecken(användarutrymme.argument(nummer));
        ram_INDEX = 0; ram_metod[0] = startpunkt_värde; ram_placera[0] = metod_START[startpunkt_värde]; lokal_värde[0] = 한국어진입 ? 0 : argument; lokal_Typ[0] = 한국어진입 ? 0 : 2;
        tråd_status[0] = 1; tråd_objekt[0] = allokera_minne(13, 2);
        köra_kommando(); if (!fel) skärmbild_Händelser(); return fel ? 1 : 0;
    }
}
