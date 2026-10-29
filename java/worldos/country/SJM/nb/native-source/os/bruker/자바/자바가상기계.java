// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. Fil/operand_stakk/referere/gren 경계를 Utfør_kommando 중 검사한다. */
public final class 자바가상기계 {
    static int[] Fil = new int[16384], filnavn_SMS = new int[64];
    static int[] konstant_kode = new int[512], 상가 = new int[512], konstant_SEKUND_VERDI = new int[512], streng_referere = new int[512];
    static int[] metode_navn_SMS = new int[32], metode_Type = new int[32], metode_tilgang = new int[32];
    static int[] metode_START = new int[32], metode_avslutte_en_samtale = new int[32], metode_stakk = new int[32], 함수지역 = new int[32];
    static int[] metode_argument_ANTALL = new int[32], metode_argument_Type = new int[512], metode_return = new int[32];
    static int[] grense_VERDI = new int[16384];
    static int[] lokal_VERDI = new int[4096], lokal_Type = new int[4096], operand_stakk_VERDI = new int[4096], operand_stakk_Type = new int[4096];
    static int[] bilde_metode = new int[32], bilde_plassere = new int[32], bilde_stakk = new int[32];
    static int[] heap_VERDI = new int[8192];
    static int Størrelse, 읽기위치, konstant_ANTALL, metode_ANTALL, klassenavn, bilde_INDEKS = -1, heap_avslutte_en_samtale_plassere = 1, return_Type;
    static boolean feil;

    static void feil_VERDI(String ord_SMS) {
        if (!feil) { bruker.Skriv("JVM error: "); bruker.Skriv(ord_SMS); bruker.skrive_tegn_VERDI(10); }
        feil = true;
    }
    static boolean klippe(int Kjør_2, int lengde_VERDI) { return Kjør_2 >= 0 && lengde_VERDI >= 0 && Kjør_2 <= Størrelse - lengde_VERDI; }
    static int byte_VERDI() {
        if (!klippe(읽기위치, 1)) { feil_VERDI("truncated class file"); return 0; }
        return Fil[읽기위치++];
    }
    static int 짧은수() { return byte_VERDI() << 8 | byte_VERDI(); }
    static int heltall() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int lengde_VERDI) { if (!klippe(읽기위치, lengde_VERDI)) feil_VERDI("invalid attribute size"); else 읽기위치 += lengde_VERDI; }
    static boolean sjekk_konstant(int nummer, int 종류) {
        if (nummer <= 0 || nummer >= konstant_ANTALL || konstant_kode[nummer] != 종류) { feil_VERDI("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean SMS_område(int Kjør_2, int lengde_VERDI, String ord_SMS) {
        if (!klippe(Kjør_2, lengde_VERDI) || lengde_VERDI != ord_SMS.length()) return false;
        for (int nummer = 0; nummer < lengde_VERDI; nummer++) if (Fil[Kjør_2 + nummer] != ord_SMS.charAt(nummer)) return false;
        return true;
    }
    static boolean ord_SMS(int konstant_VERDI, String ord_SMS) { return sjekk_konstant(konstant_VERDI, 1) && SMS_område(상가[konstant_VERDI], konstant_SEKUND_VERDI[konstant_VERDI], ord_SMS); }
    static boolean avstemming_ord(int 가, int SEKUND_operand) {
        if (!sjekk_konstant(가, 1) || !sjekk_konstant(SEKUND_operand, 1) || konstant_SEKUND_VERDI[가] != konstant_SEKUND_VERDI[SEKUND_operand]) return false;
        for (int nummer = 0; nummer < konstant_SEKUND_VERDI[가]; nummer++) if (Fil[상가[가] + nummer] != Fil[상가[SEKUND_operand] + nummer]) return false;
        return true;
    }
    static int klassenavn_SMS(int nummer) { return sjekk_konstant(nummer, 7) && sjekk_konstant(상가[nummer], 1) ? 상가[nummer] : 0; }
    static int referere_navn(int nummer) { return sjekk_konstant(nummer, 12) && sjekk_konstant(상가[nummer], 1) ? 상가[nummer] : 0; }
    static int referansetype(int nummer) { return sjekk_konstant(nummer, 12) && sjekk_konstant(konstant_SEKUND_VERDI[nummer], 1) ? konstant_SEKUND_VERDI[nummer] : 0; }
    static int 서술형(int 끝, boolean tom_Type) {
        if (읽기위치 >= 끝) { feil_VERDI("invalid descriptor"); return 0; }
        int VERDI = byte_VERDI();
        if (VERDI == 'V' && tom_Type) return 0;
        if (VERDI == 'I' || VERDI == 'B' || VERDI == 'C' || VERDI == 'S' || VERDI == 'Z') return 1;
        if (VERDI == '[') { 서술형(끝, false); return 2; }
        if (VERDI == 'L') {
            int Kjør_2 = 읽기위치;
            while (읽기위치 < 끝 && Fil[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == Kjør_2) feil_VERDI("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        feil_VERDI("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int FUNKSJON_VERDI) {
        int Forrige_vare = 읽기위치, nummer = metode_Type[FUNKSJON_VERDI];
        if (!sjekk_konstant(nummer, 1)) return;
        읽기위치 = 상가[nummer]; int 끝 = 읽기위치 + konstant_SEKUND_VERDI[nummer];
        if (byte_VERDI() != '(') feil_VERDI("invalid method descriptor");
        int vare_ANTALL = 0;
        while (!feil && 읽기위치 < 끝 && Fil[읽기위치] != ')') {
            if (vare_ANTALL == 16) { feil_VERDI("too many method arguments"); break; }
            metode_argument_Type[FUNKSJON_VERDI * 16 + vare_ANTALL++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || byte_VERDI() != ')') feil_VERDI("invalid method descriptor");
        metode_return[FUNKSJON_VERDI] = 서술형(끝, true); metode_argument_ANTALL[FUNKSJON_VERDI] = vare_ANTALL;
        if (읽기위치 != 끝) feil_VERDI("invalid method descriptor");
        읽기위치 = Forrige_vare;
    }
    static void hoppe_over_attributt() {
        int vare_ANTALL = 짧은수();
        for (int nummer = 0; nummer < vare_ANTALL && !feil; nummer++) { sjekk_konstant(짧은수(), 1); 건너(heltall()); }
    }
    static int kommando_lengde(int VERDI) {
        if (VERDI == 16 || VERDI == 18 || VERDI == 21 || VERDI == 25 || VERDI == 54 || VERDI == 58 || VERDI == 188) return 2;
        if (VERDI == 17 || VERDI == 19 || VERDI == 132 || VERDI >= 153 && VERDI <= 167
            || VERDI >= 178 && VERDI <= 184 || VERDI == 187 || VERDI == 189 || VERDI == 192 || VERDI == 198 || VERDI == 199) return 3;
        if (VERDI >= 0 && VERDI <= 8 || VERDI >= 26 && VERDI <= 29 || VERDI >= 42 && VERDI <= 46 || VERDI == 50
            || VERDI >= 59 && VERDI <= 62 || VERDI >= 75 && VERDI <= 79 || VERDI == 83 || VERDI == 87 || VERDI == 89 || VERDI == 95
            || VERDI == 96 || VERDI == 100 || VERDI == 104 || VERDI == 108 || VERDI == 112 || VERDI == 116
            || VERDI == 120 || VERDI == 122 || VERDI == 124 || VERDI == 126 || VERDI == 128 || VERDI == 130
            || VERDI >= 145 && VERDI <= 147 || VERDI == 172 || VERDI == 176 || VERDI == 177 || VERDI == 190) return 1;
        return 0;
    }
    static void 클래스읽기() {
        if (heltall() != 0xcafebabe) feil_VERDI("not a class file");
        int 부판 = 짧은수(), versjon_VERDI = 짧은수();
        if (versjon_VERDI < 45 || versjon_VERDI > 52 || 부판 != 0) feil_VERDI("supported class versions: 45..52, minor 0");
        konstant_ANTALL = 짧은수();
        if (konstant_ANTALL < 1 || konstant_ANTALL > 512) { feil_VERDI("constant pool limit (511)"); return; }
        for (int nummer = 1; nummer < konstant_ANTALL && !feil; nummer++) {
            int 종류 = byte_VERDI(); konstant_kode[nummer] = 종류;
            if (종류 == 1) { konstant_SEKUND_VERDI[nummer] = 짧은수(); 상가[nummer] = 읽기위치; 건너(konstant_SEKUND_VERDI[nummer]); }
            else if (종류 == 3) 상가[nummer] = heltall();
            else if (종류 == 7 || 종류 == 8) 상가[nummer] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[nummer] = 짧은수(); konstant_SEKUND_VERDI[nummer] = 짧은수(); }
            else feil_VERDI("unsupported constant type");
        }
        int tillatelse_VERDI = 짧은수();
        if ((tillatelse_VERDI & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) feil_VERDI("unsupported class flags");
        klassenavn = klassenavn_SMS(짧은수());
        if (!ord_SMS(klassenavn_SMS(짧은수()), "java/lang/Object")) feil_VERDI("inheritance unsupported");
        if (짧은수() != 0) feil_VERDI("interfaces unsupported");
        if (짧은수() != 0) feil_VERDI("fields unsupported");
        metode_ANTALL = 짧은수();
        if (metode_ANTALL < 1 || metode_ANTALL > 32) { feil_VERDI("method count limit (32)"); return; }
        for (int nummer = 0; nummer < metode_ANTALL && !feil; nummer++) {
            metode_tilgang[nummer] = 짧은수(); metode_navn_SMS[nummer] = 짧은수(); metode_Type[nummer] = 짧은수();
            sjekk_konstant(metode_navn_SMS[nummer], 1); 서술읽기(nummer);
            if ((metode_tilgang[nummer] & (0x100 | 0x400 | 0x20)) != 0) feil_VERDI("native, abstract and synchronized methods unsupported");
            if ((metode_tilgang[nummer] & 8) == 0 && !ord_SMS(metode_navn_SMS[nummer], "<init>")) feil_VERDI("instance methods unsupported");
            if (ord_SMS(metode_navn_SMS[nummer], "<clinit>")) feil_VERDI("class initializers unsupported");
            for (int frontkamera_VERDI = 0; frontkamera_VERDI < nummer; frontkamera_VERDI++) if (avstemming_ord(metode_navn_SMS[frontkamera_VERDI], metode_navn_SMS[nummer]) && avstemming_ord(metode_Type[frontkamera_VERDI], metode_Type[nummer])) feil_VERDI("duplicate method");
            int vare_ANTALL = 짧은수();
            for (int attributtverdi = 0; attributtverdi < vare_ANTALL && !feil; attributtverdi++) {
                int Navn = 짧은수(), lengde_VERDI = heltall(), Kjør_2 = 읽기위치;
                if (!klippe(Kjør_2, lengde_VERDI)) { feil_VERDI("truncated method attribute"); break; }
                if (ord_SMS(Navn, "Code")) {
                    if (metode_START[nummer] != 0) feil_VERDI("duplicate Code attribute");
                    metode_stakk[nummer] = 짧은수(); 함수지역[nummer] = 짧은수(); int KODE_lengde = heltall();
                    if (metode_stakk[nummer] > 128 || 함수지역[nummer] > 128 || 함수지역[nummer] < metode_argument_ANTALL[nummer]
                        || KODE_lengde < 1 || KODE_lengde > 8192) feil_VERDI("method memory limits exceeded");
                    metode_START[nummer] = 읽기위치; 건너(KODE_lengde); metode_avslutte_en_samtale[nummer] = 읽기위치;
                    if (짧은수() != 0) feil_VERDI("exception handlers unsupported");
                    hoppe_over_attributt();
                    if (읽기위치 != Kjør_2 + lengde_VERDI) feil_VERDI("Code attribute size mismatch");
                } else 건너(lengde_VERDI);
            }
            if (metode_START[nummer] == 0) feil_VERDI("missing Code attribute");
            int åpning_oppføring = metode_START[nummer];
            while (åpning_oppføring < metode_avslutte_en_samtale[nummer] && !feil) {
                int lengde_VERDI = kommando_lengde(Fil[åpning_oppføring]);
                if (lengde_VERDI == 0 || lengde_VERDI > metode_avslutte_en_samtale[nummer] - åpning_oppføring) { feil_VERDI("unsupported or truncated bytecode"); break; }
                grense_VERDI[åpning_oppføring] = nummer + 1; åpning_oppføring += lengde_VERDI;
            }
            // 실행하지 않는 경로에도 잘못된 gren 목적지를 허용하지 않는다.
            åpning_oppføring = metode_START[nummer];
            while (åpning_oppføring < metode_avslutte_en_samtale[nummer] && !feil) {
                int VERDI = Fil[åpning_oppføring];
                if (VERDI >= 153 && VERDI <= 167 || VERDI == 198 || VERDI == 199) {
                    int mål_VERDI = åpning_oppføring + (short)(Fil[åpning_oppføring + 1] << 8 | Fil[åpning_oppføring + 2]);
                    if (mål_VERDI < metode_START[nummer] || mål_VERDI >= metode_avslutte_en_samtale[nummer] || grense_VERDI[mål_VERDI] != nummer + 1) feil_VERDI("invalid branch target");
                }
                åpning_oppføring += kommando_lengde(VERDI);
            }
        }
        if (!feil) hoppe_over_attributt();
        if (읽기위치 != Størrelse) feil_VERDI("extra class file data");
    }
    static int tildele_lager(int 종류, int lengde_VERDI) {
        if (lengde_VERDI < 0 || lengde_VERDI > heap_VERDI.length - heap_avslutte_en_samtale_plassere - 2) { feil_VERDI("object heap exhausted or negative array size"); return 0; }
        int referere = heap_avslutte_en_samtale_plassere; heap_avslutte_en_samtale_plassere += lengde_VERDI + 2; heap_VERDI[referere] = 종류; heap_VERDI[referere + 1] = lengde_VERDI;
        return referere;
    }
    static boolean objekt_VERDI(int referere, int 종류) {
        if (referere < 1 || referere >= heap_avslutte_en_samtale_plassere - 1 || heap_VERDI[referere] != 종류) { feil_VERDI("null or invalid object reference"); return false; }
        return true;
    }
    static int konstant_SMS(int INDEKS) {
        if (!sjekk_konstant(INDEKS, 1)) return 0;
        if (streng_referere[INDEKS] != 0) return streng_referere[INDEKS];
        int referere = tildele_lager(1, konstant_SEKUND_VERDI[INDEKS]); if (feil) return 0;
        int 끝 = 상가[INDEKS] + konstant_SEKUND_VERDI[INDEKS], nummer = 상가[INDEKS], lengde_VERDI = 0;
        while (nummer < 끝 && !feil) {
            int VERDI = Fil[nummer++];
            if (VERDI == 0) feil_VERDI("invalid modified UTF-8");
            else if (VERDI >= 192 && VERDI <= 223 && nummer < 끝) {
                int Neste_vare = Fil[nummer++];
                if ((Neste_vare & 192) != 128) feil_VERDI("invalid modified UTF-8");
                VERDI = (VERDI & 31) << 6 | Neste_vare & 63;
                if (VERDI != 0 && VERDI < 128) feil_VERDI("overlong modified UTF-8");
            } else if (VERDI >= 224 && VERDI <= 239 && nummer + 1 < 끝) {
                int 가 = Fil[nummer++], SEKUND_operand = Fil[nummer++];
                if ((가 & 192) != 128 || (SEKUND_operand & 192) != 128) feil_VERDI("invalid modified UTF-8");
                VERDI = (VERDI & 15) << 12 | (가 & 63) << 6 | SEKUND_operand & 63;
                if (VERDI < 2048) feil_VERDI("overlong modified UTF-8");
            } else if (VERDI >= 128) feil_VERDI("invalid modified UTF-8");
            heap_VERDI[referere + 2 + lengde_VERDI++] = VERDI;
        }
        heap_VERDI[referere + 1] = lengde_VERDI; streng_referere[INDEKS] = referere; return referere;
    }
    static int vert_tegn(String VERDI) {
        int referere = tildele_lager(1, VERDI.length()); if (feil) return 0;
        for (int nummer = 0; nummer < VERDI.length(); nummer++) heap_VERDI[referere + 2 + nummer] = VERDI.charAt(nummer);
        return referere;
    }
    static void skrive_SMS(int referere) {
        if (referere == 0) { bruker.Skriv("null"); return; }
        if (!objekt_VERDI(referere, 1)) return;
        for (int nummer = 0; nummer < heap_VERDI[referere + 1]; nummer++) bruker.skrive_tegn_VERDI(heap_VERDI[referere + 2 + nummer]);
    }
    static int siffer_tegn(int VERDI) {
        int referere = tildele_lager(1, 11); if (feil) return 0;
        int lengde_VERDI = 0;
        if (VERDI < 0) heap_VERDI[referere + 2 + lengde_VERDI++] = '-'; else VERDI = -VERDI;
        int posisjonsindeks = 1000000000; boolean Kjør_2 = false;
        while (posisjonsindeks != 0) {
            int nummer = -(VERDI / posisjonsindeks);
            if (nummer != 0 || Kjør_2 || posisjonsindeks == 1) { heap_VERDI[referere + 2 + lengde_VERDI++] = '0' + nummer; Kjør_2 = true; }
            VERDI %= posisjonsindeks; posisjonsindeks /= 10;
        }
        heap_VERDI[referere + 1] = lengde_VERDI; return referere;
    }
    static int 정수해독(int referere) {
        if (!objekt_VERDI(referere, 1)) return 0;
        int lengde_VERDI = heap_VERDI[referere + 1], nummer = 0, VERDI = 0; boolean 음수 = false;
        if (lengde_VERDI > 0 && (heap_VERDI[referere + 2] == '-' || heap_VERDI[referere + 2] == '+')) { 음수 = heap_VERDI[referere + 2] == '-'; nummer++; }
        if (nummer == lengde_VERDI) feil_VERDI("NumberFormatException");
        for (; nummer < lengde_VERDI && !feil; nummer++) {
            int siffer_VERDI = heap_VERDI[referere + 2 + nummer] - '0';
            if (siffer_VERDI < 0 || siffer_VERDI > 9 || VERDI < -214748364 || VERDI == -214748364 && siffer_VERDI > (음수 ? 8 : 7)) feil_VERDI("NumberFormatException");
            VERDI = VERDI * 10 - siffer_VERDI;
        }
        return 음수 ? VERDI : -VERDI;
    }
    static void 넣기(int VERDI, int Type_VERDI) {
        if (feil) return;
        if (bilde_INDEKS < 0 || bilde_stakk[bilde_INDEKS] >= metode_stakk[bilde_metode[bilde_INDEKS]]) { feil_VERDI("operand stack overflow"); return; }
        int åpning_oppføring = bilde_INDEKS * 128 + bilde_stakk[bilde_INDEKS]++; operand_stakk_VERDI[åpning_oppføring] = VERDI; operand_stakk_Type[åpning_oppføring] = Type_VERDI;
    }
    static int 빼기(int Type_VERDI) {
        if (feil) return 0;
        if (bilde_INDEKS < 0 || bilde_stakk[bilde_INDEKS] < 1) { feil_VERDI("operand stack underflow"); return 0; }
        int åpning_oppføring = bilde_INDEKS * 128 + --bilde_stakk[bilde_INDEKS]; return_Type = operand_stakk_Type[åpning_oppføring];
        if (Type_VERDI != 0 && return_Type != Type_VERDI) feil_VERDI("operand type mismatch");
        return operand_stakk_VERDI[åpning_oppføring];
    }
    static void 지역읽기(int INDEKS, int Type_VERDI) {
        if (INDEKS >= 함수지역[bilde_metode[bilde_INDEKS]] || INDEKS < 0 || lokal_Type[bilde_INDEKS * 128 + INDEKS] != Type_VERDI) { feil_VERDI("invalid or uninitialized local"); return; }
        넣기(lokal_VERDI[bilde_INDEKS * 128 + INDEKS], Type_VERDI);
    }
    static void skrive_lokal(int INDEKS, int Type_VERDI) {
        if (INDEKS >= 함수지역[bilde_metode[bilde_INDEKS]] || INDEKS < 0) { feil_VERDI("local index out of range"); return; }
        int VERDI = 빼기(Type_VERDI); lokal_VERDI[bilde_INDEKS * 128 + INDEKS] = VERDI; lokal_Type[bilde_INDEKS * 128 + INDEKS] = Type_VERDI;
    }
    static int 명바() {
        int Posisjon = bilde_plassere[bilde_INDEKS];
        if (Posisjon < metode_START[bilde_metode[bilde_INDEKS]] || Posisjon >= metode_avslutte_en_samtale[bilde_metode[bilde_INDEKS]]) { feil_VERDI("instruction pointer out of range"); return 0; }
        bilde_plassere[bilde_INDEKS]++; return Fil[Posisjon];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void flytte_VERDI_83b651b8(int Posisjon) {
        int FUNKSJON_VERDI = bilde_metode[bilde_INDEKS];
        if (Posisjon < metode_START[FUNKSJON_VERDI] || Posisjon >= metode_avslutte_en_samtale[FUNKSJON_VERDI] || grense_VERDI[Posisjon] != FUNKSJON_VERDI + 1) feil_VERDI("invalid branch target");
        else bilde_plassere[bilde_INDEKS] = Posisjon;
    }
    static void 호출(int FUNKSJON_VERDI) {
        if (bilde_INDEKS == 31) { feil_VERDI("call stack limit (32)"); return; }
        int Neste_vare = bilde_INDEKS + 1;
        for (int nummer = 0; nummer < 128; nummer++) lokal_Type[Neste_vare * 128 + nummer] = 0;
        for (int nummer = metode_argument_ANTALL[FUNKSJON_VERDI] - 1; nummer >= 0; nummer--) {
            lokal_VERDI[Neste_vare * 128 + nummer] = 빼기(metode_argument_Type[FUNKSJON_VERDI * 16 + nummer]); lokal_Type[Neste_vare * 128 + nummer] = metode_argument_Type[FUNKSJON_VERDI * 16 + nummer];
        }
        bilde_INDEKS = Neste_vare; bilde_metode[bilde_INDEKS] = FUNKSJON_VERDI; bilde_plassere[bilde_INDEKS] = metode_START[FUNKSJON_VERDI]; bilde_stakk[bilde_INDEKS] = 0;
    }
    static void return_KR(int Type_VERDI) {
        if (Type_VERDI != metode_return[bilde_metode[bilde_INDEKS]]) { feil_VERDI("return type mismatch"); return; }
        int VERDI = Type_VERDI == 0 ? 0 : 빼기(Type_VERDI);
        bilde_INDEKS--; if (bilde_INDEKS >= 0 && Type_VERDI != 0) 넣기(VERDI, Type_VERDI);
    }
    static int[] strøm_filnavn = new int[64];
    static void Fil_strøm_Ring(int eier_VERDI, int Navn, int format_VERDI, int Kommando) {
        boolean Utgang = ord_SMS(eier_VERDI, "java/io/FileOutputStream");
        int 종류 = Utgang ? 6 : 5;
        if (Kommando == 183 && ord_SMS(Navn, "<init>")) {
            boolean 이어 = false;
            if (Utgang && ord_SMS(format_VERDI, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!ord_SMS(format_VERDI, "(Ljava/lang/String;)V")) { feil_VERDI("unsupported file stream constructor"); return; }
            int Fil_oppføring_navn = 빼기(2), strøm_VERDI = 빼기(2);
            if (!objekt_VERDI(Fil_oppføring_navn, 1) || !objekt_VERDI(strøm_VERDI, 종류) || feil) return;
            if (heap_VERDI[strøm_VERDI + 3] != 0) { feil_VERDI("file stream already initialized"); return; }
            int lengde_VERDI = heap_VERDI[Fil_oppføring_navn + 1];
            if (lengde_VERDI < 1 || lengde_VERDI > 63) { feil_VERDI("invalid file name length"); return; }
            for (int åpning_oppføring = 0; åpning_oppføring < lengde_VERDI; åpning_oppføring++) {
                int VERDI = heap_VERDI[Fil_oppføring_navn + 2 + åpning_oppføring];
                if (VERDI < 1 || VERDI > 127) { feil_VERDI("file stream paths currently require ASCII"); return; }
                strøm_filnavn[åpning_oppføring] = VERDI;
            }
            strøm_filnavn[lengde_VERDI] = 0;
            int 서술자 = bruker.파일서술자열기(strøm_filnavn, Utgang ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { feil_VERDI("FileNotFoundException: file open failed"); return; }
            heap_VERDI[strøm_VERDI + 2] = 서술자; heap_VERDI[strøm_VERDI + 3] = 1;
            return;
        }
        if (Kommando != 182) { feil_VERDI("invalid file stream invocation"); return; }
        int Handling = -1, VERDI = 0;
        if (ord_SMS(Navn, "close") && ord_SMS(format_VERDI, "()V")) Handling = 0;
        if (!Utgang && ord_SMS(Navn, "read") && ord_SMS(format_VERDI, "()I")) Handling = 1;
        if (Utgang && ord_SMS(Navn, "write") && ord_SMS(format_VERDI, "(I)V")) { Handling = 2; VERDI = 빼기(1); }
        if (Handling < 0) { feil_VERDI("unsupported file stream method"); return; }
        int strøm_VERDI = 빼기(2);
        if (!objekt_VERDI(strøm_VERDI, 종류) || feil) return;
        if (heap_VERDI[strøm_VERDI + 3] == 0) { feil_VERDI("uninitialized file stream"); return; }
        int 서술자 = heap_VERDI[strøm_VERDI + 2];
        if (Handling == 0) {
            if (서술자 >= 0 && bruker.파일서술자닫기(서술자) < 0) feil_VERDI("IOException: close failed");
            heap_VERDI[strøm_VERDI + 2] = -1; return;
        }
        if (서술자 < 0) { feil_VERDI("IOException: stream closed"); return; }
        if (Handling == 1) {
            int KR = bruker.파일한바이트읽기(서술자);
            if (KR < -1) feil_VERDI("IOException: read failed"); else 넣기(KR, 1);
        } else if (bruker.파일한바이트쓰기(서술자, VERDI) != 1) feil_VERDI("IOException: write failed");
    }
    static void Ring_metode(int INDEKS, int Kommando) {
        if (!sjekk_konstant(INDEKS, 10)) return;
        int eier_VERDI = klassenavn_SMS(상가[INDEKS]), Navn = referere_navn(konstant_SEKUND_VERDI[INDEKS]), format_VERDI = referansetype(konstant_SEKUND_VERDI[INDEKS]);
        if (feil) return;
        if (avstemming_ord(eier_VERDI, klassenavn)) {
            if (Kommando != 184) { feil_VERDI("only static user methods are supported"); return; }
            for (int nummer = 0; nummer < metode_ANTALL; nummer++) if (avstemming_ord(Navn, metode_navn_SMS[nummer]) && avstemming_ord(format_VERDI, metode_Type[nummer])) {
                if ((metode_tilgang[nummer] & 8) == 0) feil_VERDI("method is not static"); else 호출(nummer);
                return;
            }
            feil_VERDI("NoSuchMethodError"); return;
        }
        if (ord_SMS(eier_VERDI, "java/io/FileInputStream") || ord_SMS(eier_VERDI, "java/io/FileOutputStream")) {
            Fil_strøm_Ring(eier_VERDI, Navn, format_VERDI, Kommando); return;
        }
        if (Kommando == 184 && ord_SMS(eier_VERDI, "java/lang/Integer") && ord_SMS(Navn, "parseInt") && ord_SMS(format_VERDI, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (Kommando == 182 && ord_SMS(eier_VERDI, "java/io/PrintStream") && (ord_SMS(Navn, "println") || ord_SMS(Navn, "print"))) {
            int Type_VERDI = 0, VERDI = 0;
            if (ord_SMS(format_VERDI, "(I)V")) { Type_VERDI = 1; VERDI = 빼기(1); }
            else if (ord_SMS(format_VERDI, "(Z)V")) { Type_VERDI = 2; VERDI = 빼기(1); }
            else if (ord_SMS(format_VERDI, "(C)V")) { Type_VERDI = 3; VERDI = 빼기(1); }
            else if (ord_SMS(format_VERDI, "(Ljava/lang/String;)V")) { Type_VERDI = 4; VERDI = 빼기(2); }
            else if (!ord_SMS(format_VERDI, "()V") || !ord_SMS(Navn, "println")) feil_VERDI("unsupported print descriptor");
            if (빼기(2) != -1) feil_VERDI("invalid PrintStream receiver");
            if (feil) return;
            if (Type_VERDI == 1) 자바도구.skrive_nummer(VERDI);
            if (Type_VERDI == 2) bruker.Skriv(VERDI == 0 ? "false" : "true");
            if (Type_VERDI == 3) bruker.skrive_tegn_VERDI(VERDI & 65535);
            if (Type_VERDI == 4) skrive_SMS(VERDI);
            if (ord_SMS(Navn, "println")) bruker.skrive_tegn_VERDI(10);
            return;
        }
        if (Kommando == 182 && ord_SMS(eier_VERDI, "java/lang/String")) {
            if (ord_SMS(Navn, "length") && ord_SMS(format_VERDI, "()I")) {
                int referere = 빼기(2); if (objekt_VERDI(referere, 1)) 넣기(heap_VERDI[referere + 1], 1); return;
            }
            if (ord_SMS(Navn, "charAt") && ord_SMS(format_VERDI, "(I)C")) {
                int senket_skrift_VERDI = 빼기(1), referere = 빼기(2);
                if (objekt_VERDI(referere, 1)) {
                    if (senket_skrift_VERDI < 0 || senket_skrift_VERDI >= heap_VERDI[referere + 1]) feil_VERDI("StringIndexOutOfBoundsException"); else 넣기(heap_VERDI[referere + 2 + senket_skrift_VERDI], 1);
                }
                return;
            }
        }
        if (ord_SMS(eier_VERDI, "java/lang/StringBuilder")) {
            if (Kommando == 183 && ord_SMS(Navn, "<init>") && ord_SMS(format_VERDI, "()V")) { objekt_VERDI(빼기(2), 4); return; }
            if (Kommando == 182 && ord_SMS(Navn, "toString") && ord_SMS(format_VERDI, "()Ljava/lang/String;")) {
                int referere = 빼기(2); if (objekt_VERDI(referere, 4)) 넣기(heap_VERDI[referere + 2] == 0 ? vert_tegn("") : heap_VERDI[referere + 2], 2); return;
            }
            if (Kommando == 182 && ord_SMS(Navn, "append")) {
                int Tekst = 0;
                if (ord_SMS(format_VERDI, "(I)Ljava/lang/StringBuilder;")) Tekst = siffer_tegn(빼기(1));
                else if (ord_SMS(format_VERDI, "(Z)Ljava/lang/StringBuilder;")) Tekst = vert_tegn(빼기(1) == 0 ? "false" : "true");
                else if (ord_SMS(format_VERDI, "(C)Ljava/lang/StringBuilder;")) {
                    int VERDI = 빼기(1); Tekst = tildele_lager(1, 1); if (!feil) heap_VERDI[Tekst + 2] = VERDI & 65535;
                }
                else if (ord_SMS(format_VERDI, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { Tekst = 빼기(2); if (Tekst == 0) Tekst = vert_tegn("null"); }
                else { feil_VERDI("unsupported StringBuilder append"); return; }
                int referere = 빼기(2); if (!objekt_VERDI(referere, 4) || !objekt_VERDI(Tekst, 1)) return;
                int frontkamera_VERDI = heap_VERDI[referere + 2], frontkamera_VERDI_lengde = frontkamera_VERDI == 0 ? 0 : heap_VERDI[frontkamera_VERDI + 1], TILBAKE_VERDI_lengde = heap_VERDI[Tekst + 1];
                int 새글 = tildele_lager(1, frontkamera_VERDI_lengde + TILBAKE_VERDI_lengde); if (feil) return;
                for (int nummer = 0; nummer < frontkamera_VERDI_lengde; nummer++) heap_VERDI[새글 + 2 + nummer] = heap_VERDI[frontkamera_VERDI + 2 + nummer];
                for (int nummer = 0; nummer < TILBAKE_VERDI_lengde; nummer++) heap_VERDI[새글 + 2 + frontkamera_VERDI_lengde + nummer] = heap_VERDI[Tekst + 2 + nummer];
                heap_VERDI[referere + 2] = 새글; 넣기(referere, 2); return;
            }
        }
        feil_VERDI("unsupported library method");
    }
    static int MATRISE_åpning(int referere, int senket_skrift_VERDI, int Type_VERDI) {
        if (!objekt_VERDI(referere, Type_VERDI)) return 0;
        if (senket_skrift_VERDI < 0 || senket_skrift_VERDI >= heap_VERDI[referere + 1]) { feil_VERDI("ArrayIndexOutOfBoundsException"); return 0; }
        return referere + 2 + senket_skrift_VERDI;
    }
    static void Utfør_kommando() {
        int 남음 = 500000;
        while (bilde_INDEKS >= 0 && !feil) {
            if (--남음 == 0) { feil_VERDI("instruction limit (500000)"); break; }
            int Kjør_2 = bilde_plassere[bilde_INDEKS], VERDI = 명바();
            if (feil) break;
            if (VERDI == 0) continue;
            if (VERDI == 1) { 넣기(0, 2); continue; }
            if (VERDI >= 2 && VERDI <= 8) { 넣기(VERDI - 3, 1); continue; }
            if (VERDI == 16) { 넣기((byte)명바(), 1); continue; }
            if (VERDI == 17) { 넣기((short)명짧(), 1); continue; }
            if (VERDI == 18 || VERDI == 19) {
                int nummer = VERDI == 18 ? 명바() : 명짧();
                if (nummer <= 0 || nummer >= konstant_ANTALL) feil_VERDI("invalid ldc constant");
                else if (konstant_kode[nummer] == 3) 넣기(상가[nummer], 1);
                else if (konstant_kode[nummer] == 8) 넣기(konstant_SMS(상가[nummer]), 2);
                else feil_VERDI("unsupported ldc constant");
                continue;
            }
            if (VERDI == 21 || VERDI == 25) { 지역읽기(명바(), VERDI == 21 ? 1 : 2); continue; }
            if (VERDI >= 26 && VERDI <= 29) { 지역읽기(VERDI - 26, 1); continue; }
            if (VERDI >= 42 && VERDI <= 45) { 지역읽기(VERDI - 42, 2); continue; }
            if (VERDI == 54 || VERDI == 58) { skrive_lokal(명바(), VERDI == 54 ? 1 : 2); continue; }
            if (VERDI >= 59 && VERDI <= 62) { skrive_lokal(VERDI - 59, 1); continue; }
            if (VERDI >= 75 && VERDI <= 78) { skrive_lokal(VERDI - 75, 2); continue; }
            if (VERDI == 46 || VERDI == 50) {
                int senket_skrift_VERDI = 빼기(1), referere = 빼기(2), åpning_oppføring = MATRISE_åpning(referere, senket_skrift_VERDI, VERDI == 46 ? 2 : 3);
                if (!feil) 넣기(heap_VERDI[åpning_oppføring], VERDI == 46 ? 1 : 2); continue;
            }
            if (VERDI == 79 || VERDI == 83) {
                int vare_element = 빼기(VERDI == 79 ? 1 : 2), senket_skrift_VERDI = 빼기(1), referere = 빼기(2), åpning_oppføring = MATRISE_åpning(referere, senket_skrift_VERDI, VERDI == 79 ? 2 : 3);
                if (VERDI == 83 && vare_element != 0) objekt_VERDI(vare_element, 1);
                if (!feil) heap_VERDI[åpning_oppføring] = vare_element; continue;
            }
            if (VERDI == 87) { 빼기(0); continue; }
            if (VERDI == 89) { int 가 = 빼기(0), Type_VERDI = return_Type; 넣기(가, Type_VERDI); 넣기(가, Type_VERDI); continue; }
            if (VERDI == 95) { int 가 = 빼기(0), 가형 = return_Type, SEKUND_operand = 빼기(0), SEKUND_operand_Type = return_Type; 넣기(가, 가형); 넣기(SEKUND_operand, SEKUND_operand_Type); continue; }
            if (VERDI == 96 || VERDI == 100 || VERDI == 104 || VERDI == 108 || VERDI == 112 || VERDI == 120
                || VERDI == 122 || VERDI == 124 || VERDI == 126 || VERDI == 128 || VERDI == 130) {
                int SEKUND_operand = 빼기(1), 가 = 빼기(1), KR = 0;
                if ((VERDI == 108 || VERDI == 112) && SEKUND_operand == 0) { feil_VERDI("ArithmeticException: / by zero"); continue; }
                if (VERDI == 96) KR = 가 + SEKUND_operand;
                if (VERDI == 100) KR = 가 - SEKUND_operand;
                if (VERDI == 104) KR = 가 * SEKUND_operand;
                if (VERDI == 108) KR = 가 / SEKUND_operand;
                if (VERDI == 112) KR = 가 % SEKUND_operand;
                if (VERDI == 120) KR = 가 << SEKUND_operand;
                if (VERDI == 122) KR = 가 >> SEKUND_operand;
                if (VERDI == 124) KR = 가 >>> SEKUND_operand;
                if (VERDI == 126) KR = 가 & SEKUND_operand;
                if (VERDI == 128) KR = 가 | SEKUND_operand;
                if (VERDI == 130) KR = 가 ^ SEKUND_operand;
                넣기(KR, 1); continue;
            }
            if (VERDI == 116) { 넣기(-빼기(1), 1); continue; }
            if (VERDI == 132) {
                int lokal_Omfang = 명바(), øke_trinnvis_trinn = (byte)명바(); 지역읽기(lokal_Omfang, 1); 넣기(빼기(1) + øke_trinnvis_trinn, 1); skrive_lokal(lokal_Omfang, 1); continue;
            }
            if (VERDI >= 145 && VERDI <= 147) {
                int nummer = 빼기(1); 넣기(VERDI == 145 ? (byte)nummer : VERDI == 146 ? (char)nummer : (short)nummer, 1); continue;
            }
            if (VERDI >= 153 && VERDI <= 167 || VERDI == 198 || VERDI == 199) {
                int mål_VERDI = Kjør_2 + (short)명짧(); boolean 갈까 = VERDI == 167;
                if (VERDI >= 153 && VERDI <= 158) {
                    int nummer = 빼기(1); 갈까 = VERDI == 153 ? nummer == 0 : VERDI == 154 ? nummer != 0 : VERDI == 155 ? nummer < 0 : VERDI == 156 ? nummer >= 0 : VERDI == 157 ? nummer > 0 : nummer <= 0;
                } else if (VERDI >= 159 && VERDI <= 166) {
                    int SEKUND_operand = 빼기(VERDI >= 165 ? 2 : 1), 가 = 빼기(VERDI >= 165 ? 2 : 1);
                    갈까 = VERDI == 159 || VERDI == 165 ? 가 == SEKUND_operand : VERDI == 160 || VERDI == 166 ? 가 != SEKUND_operand : VERDI == 161 ? 가 < SEKUND_operand : VERDI == 162 ? 가 >= SEKUND_operand : VERDI == 163 ? 가 > SEKUND_operand : 가 <= SEKUND_operand;
                } else if (VERDI == 198 || VERDI == 199) { int nummer = 빼기(2); 갈까 = VERDI == 198 ? nummer == 0 : nummer != 0; }
                if (갈까) flytte_VERDI_83b651b8(mål_VERDI); continue;
            }
            if (VERDI == 172 || VERDI == 176 || VERDI == 177) { return_KR(VERDI == 172 ? 1 : VERDI == 176 ? 2 : 0); continue; }
            if (VERDI == 178) {
                int nummer = 명짧(); if (!sjekk_konstant(nummer, 9)) continue;
                if (!ord_SMS(klassenavn_SMS(상가[nummer]), "java/lang/System") || !ord_SMS(referere_navn(konstant_SEKUND_VERDI[nummer]), "out")
                    || !ord_SMS(referansetype(konstant_SEKUND_VERDI[nummer]), "Ljava/io/PrintStream;")) feil_VERDI("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (VERDI == 182 || VERDI == 183 || VERDI == 184) { Ring_metode(명짧(), VERDI); continue; }
            if (VERDI == 187) {
                int Navn = klassenavn_SMS(명짧());
                if (ord_SMS(Navn, "java/lang/StringBuilder")) 넣기(tildele_lager(4, 1), 2);
                else if (ord_SMS(Navn, "java/io/FileInputStream") || ord_SMS(Navn, "java/io/FileOutputStream")) {
                    int referere = tildele_lager(ord_SMS(Navn, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!feil) { heap_VERDI[referere + 2] = -1; 넣기(referere, 2); }
                } else feil_VERDI("unsupported object construction");
                continue;
            }
            if (VERDI == 188 || VERDI == 189) {
                if (VERDI == 188) { if (명바() != 10) feil_VERDI("only int[] newarray is supported"); }
                else if (!ord_SMS(klassenavn_SMS(명짧()), "java/lang/String")) feil_VERDI("only String[] anewarray is supported");
                int lengde_VERDI = 빼기(1); 넣기(tildele_lager(VERDI == 188 ? 2 : 3, lengde_VERDI), 2); continue;
            }
            if (VERDI == 190) {
                int referere = 빼기(2);
                if (referere < 1 || referere >= heap_avslutte_en_samtale_plassere - 1 || (heap_VERDI[referere] != 2 && heap_VERDI[referere] != 3)) feil_VERDI("null or invalid array");
                else 넣기(heap_VERDI[referere + 1], 1); continue;
            }
            if (VERDI == 192) {
                int Navn = klassenavn_SMS(명짧()), referere = 빼기(2);
                if (!ord_SMS(Navn, "java/lang/String")) feil_VERDI("unsupported checkcast");
                else if (referere != 0) objekt_VERDI(referere, 1);
                넣기(referere, 2); continue;
            }
            feil_VERDI("unsupported bytecode");
        }
    }
    public static int Kjør_2() {
        if (bruker.인수개수() == 1 && 자바도구.같음(bruker.Argumenter(0), "-version")) {
            bruker.Skriv("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (bruker.인수개수() < 1) { bruker.Skriv("Usage: java CLASS [ARGS]\n"); return 2; }
        int lengde_VERDI = 자바도구.Navn(filnavn_SMS, bruker.Argumenter(0));
        if (lengde_VERDI < 1 || lengde_VERDI > 57) { bruker.Skriv("java: invalid class name\n"); return 2; }
        filnavn_SMS[lengde_VERDI] = '.'; filnavn_SMS[lengde_VERDI + 1] = 'c'; filnavn_SMS[lengde_VERDI + 2] = 'l'; filnavn_SMS[lengde_VERDI + 3] = 'a'; filnavn_SMS[lengde_VERDI + 4] = 's'; filnavn_SMS[lengde_VERDI + 5] = 's';
        Størrelse = bruker.파일읽기(filnavn_SMS, Fil);
        if (Størrelse < 0) { bruker.Skriv("java: cannot read class: "); 자바도구.skrive_nummer(Størrelse); bruker.skrive_tegn_VERDI(10); return 1; }
        클래스읽기(); if (feil) return 1;
        int tegn_navn = konstant_SMS(klassenavn);
        if (!feil && heap_VERDI[tegn_navn + 1] != lengde_VERDI) feil_VERDI("class name does not match file");
        for (int nummer = 0; nummer < lengde_VERDI && !feil; nummer++) if (heap_VERDI[tegn_navn + 2 + nummer] != filnavn_SMS[nummer]) feil_VERDI("class name does not match file");
        int inngangspunkt_VERDI = -1;
        for (int nummer = 0; nummer < metode_ANTALL; nummer++) if (ord_SMS(metode_navn_SMS[nummer], "main") && ord_SMS(metode_Type[nummer], "([Ljava/lang/String;)V") && (metode_tilgang[nummer] & 9) == 9) inngangspunkt_VERDI = nummer;
        if (inngangspunkt_VERDI < 0) feil_VERDI("public static void main(String[] args) required");
        if (feil) return 1;
        int Argumenter = tildele_lager(3, bruker.인수개수() - 1);
        for (int nummer = 1; nummer < bruker.인수개수() && !feil; nummer++) heap_VERDI[Argumenter + 1 + nummer] = vert_tegn(bruker.Argumenter(nummer));
        bilde_INDEKS = 0; bilde_metode[0] = inngangspunkt_VERDI; bilde_plassere[0] = metode_START[inngangspunkt_VERDI]; lokal_VERDI[0] = Argumenter; lokal_Type[0] = 2;
        Utfør_kommando(); return feil ? 1 : 0;
    }
}
