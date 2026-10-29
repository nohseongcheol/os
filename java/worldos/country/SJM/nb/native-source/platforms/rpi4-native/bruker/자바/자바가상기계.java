// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. Fil/operand_stakk/referere/gren 경계를 Utfør_kommando 중 검사한다. */
public final class 자바가상기계 {
    static int[] Fil = new int[16 * 16384], midlertidig_fil = new int[16384], filnavn_SMS = new int[512];
    static int[] konstant_kode = new int[8192], 상가 = new int[8192], konstant_SEKUND_VERDI = new int[8192], streng_referere = new int[8192];
    static int[] metode_navn_SMS = new int[512], metode_Type = new int[512], metode_tilgang = new int[512], metode_eier = new int[512];
    static int[] metode_START = new int[512], metode_avslutte_en_samtale = new int[512], metode_stakk = new int[512], 함수지역 = new int[512];
    static int[] metode_argument_ANTALL = new int[512], metode_argument_Type = new int[8192], metode_return = new int[512];
    static int[] grense_VERDI = new int[16 * 16384];
    static int[] lokal_VERDI = new int[16384], lokal_Type = new int[16384], operand_stakk_VERDI = new int[16384], operand_stakk_Type = new int[16384];
    static int[] bilde_metode = new int[128], bilde_plassere = new int[128], bilde_stakk = new int[128], 틀명령 = new int[128], starte_bilde = new int[128];
    static int[] time_Definisjon_navn = new int[16], time_Definisjon_skalere = new int[16], time_Definisjon_overordnet = new int[16], time_Definisjon_status = new int[16], time_åpning_ANTALL = new int[16], starte_time_Definisjon = new int[16];
    static int[] time_grensesnitt = new int[16 * 16], time_grensesnitt_ANTALL = new int[16];
    static int[] åpning_navn = new int[512], åpning_Type = new int[512], åpning_eier = new int[512], åpning_tillatelse = new int[512], åpning_plassere = new int[512], åpning_data = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] heap_VERDI = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], heap_referere = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], matriseelement = new int[32768], Store_heltall = new int[256];
    static int Størrelse, 읽기위치, metode_ANTALL, klassenavn, bilde_INDEKS = -1, heap_avslutte_en_samtale_plassere = 1, return_Type;
    static int time_Definisjon_ANTALL, åpning_ANTALL, 잡기수, 현재읽는종, 던진객체, 잠시수, vise_ANTALL, Samling_ANTALL;
    static int betalt_tråd, Trådteller = 1, oppføring_time_Definisjon;
    static int[] tråd_bilde = new int[4], tråd_status = new int[4], tråd_objekt = new int[4], tråd_mål = new int[4], 가닥대기 = new int[4];
    static boolean feil, endringsforespørsel;
    static int[] blokkere_eier = new int[32768], 잠금깊이 = new int[32768], bilde_blokkere = new int[128], time_blokkere = new int[16], time_tråd = new int[16];

    static void feil_VERDI(String ord_SMS) {
        if (feil) return;
        int område_KODE = 0;
        if (자바도구.같음(ord_SMS, "ArithmeticException: / by zero")) område_KODE = 4;
        if (자바도구.같음(ord_SMS, "NullPointerException") || 자바도구.같음(ord_SMS, "null or invalid array")) område_KODE = 5;
        if (자바도구.같음(ord_SMS, "ArrayIndexOutOfBoundsException")) område_KODE = 7;
        if (자바도구.같음(ord_SMS, "StringIndexOutOfBoundsException")) område_KODE = 8;
        if (자바도구.같음(ord_SMS, "NumberFormatException")) område_KODE = 10;
        if (자바도구.같음(ord_SMS, "FileNotFoundException: file open failed")) område_KODE = 12;
        if (자바도구.같음(ord_SMS, "IOException: stream closed") || 자바도구.같음(ord_SMS, "IOException: read failed") || 자바도구.같음(ord_SMS, "IOException: write failed")) område_KODE = 11;
        if (자바도구.같음(ord_SMS, "ClassCastException")) område_KODE = 14;
        if (자바도구.같음(ord_SMS, "NegativeArraySizeException")) område_KODE = 15;
        if (område_KODE != 0 && bilde_INDEKS >= 0) { 예외던짐(område_KODE, ord_SMS); return; }
        bruker.Skriv("JVM error: "); bruker.Skriv(ord_SMS); bruker.skrive_tegn_VERDI(10); feil = true;
    }
    static boolean klippe(int Kjør_2, int lengde_VERDI) {
        if (Kjør_2 < 0 || Kjør_2 >= Fil.length || lengde_VERDI < 0) return false;
        int time_Definisjon = Kjør_2 / 16384;
        return Kjør_2 % 16384 <= time_Definisjon_skalere[time_Definisjon] && lengde_VERDI <= time_Definisjon_skalere[time_Definisjon] - Kjør_2 % 16384;
    }
    static int byte_VERDI() {
        if (!klippe(읽기위치, 1)) { feil_VERDI("truncated class file"); return 0; }
        return Fil[읽기위치++];
    }
    static int 짧은수() { return byte_VERDI() << 8 | byte_VERDI(); }
    static int heltall() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int lengde_VERDI) { if (!klippe(읽기위치, lengde_VERDI)) feil_VERDI("invalid attribute size"); else 읽기위치 += lengde_VERDI; }
    static boolean sjekk_konstant(int nummer, int 종류) {
        if (nummer <= 0 || nummer >= konstant_kode.length || konstant_kode[nummer] != 종류) { feil_VERDI("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean SMS_område(int Kjør_2, int lengde_VERDI, String ord_SMS) {
        if (!klippe(Kjør_2, lengde_VERDI)) return false;
        int 읽는자리 = Kjør_2, 끝 = Kjør_2 + lengde_VERDI;
        for (int Loop_INDEKS = 0; Loop_INDEKS < ord_SMS.length(); Loop_INDEKS++) {
            int tegnkode = ord_SMS.charAt(Loop_INDEKS);
            if (tegnkode > 0 && tegnkode < 128) { if (읽는자리 >= 끝 || Fil[읽는자리++] != tegnkode) return false; }
            else if (tegnkode < 2048) {
                if (읽는자리 + 2 > 끝 || Fil[읽는자리++] != (192 | (tegnkode >> 6)) || Fil[읽는자리++] != (128 | (tegnkode & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || Fil[읽는자리++] != (224 | (tegnkode >> 12)) || Fil[읽는자리++] != (128 | ((tegnkode >> 6) & 63)) || Fil[읽는자리++] != (128 | (tegnkode & 63))) return false;
        }
        return 읽는자리 == 끝;
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
    static int 상번호() { int VERDI = 짧은수(); return VERDI == 0 ? 0 : 현재읽는종 * 512 + VERDI; }
    static int 명상수() { return metode_eier[bilde_metode[bilde_INDEKS]] * 512 + 명짧(); }
    static void hoppe_over_attributt() {
        int vare_ANTALL = 짧은수();
        for (int nummer = 0; nummer < vare_ANTALL && !feil; nummer++) { sjekk_konstant(상번호(), 1); 건너(heltall()); }
    }
    static int kommando_lengde(int VERDI) {
        if (VERDI == 16 || VERDI == 18 || VERDI == 21 || VERDI == 25 || VERDI == 54 || VERDI == 58 || VERDI == 188) return 2;
        if (VERDI == 17 || VERDI == 19 || VERDI == 132 || VERDI >= 153 && VERDI <= 167
            || VERDI >= 178 && VERDI <= 184 || VERDI == 187 || VERDI == 189 || VERDI == 192 || VERDI == 193 || VERDI == 198 || VERDI == 199) return 3;
        if (VERDI == 185 || VERDI == 200) return 5;
        if (VERDI >= 0 && VERDI <= 8 || VERDI >= 26 && VERDI <= 29 || VERDI >= 42 && VERDI <= 46 || VERDI >= 50 && VERDI <= 53
            || VERDI >= 59 && VERDI <= 62 || VERDI >= 75 && VERDI <= 79 || VERDI >= 83 && VERDI <= 95
            || VERDI == 96 || VERDI == 100 || VERDI == 104 || VERDI == 108 || VERDI == 112 || VERDI == 116
            || VERDI == 120 || VERDI == 122 || VERDI == 124 || VERDI == 126 || VERDI == 128 || VERDI == 130
            || VERDI >= 145 && VERDI <= 147 || VERDI == 172 || VERDI == 176 || VERDI == 177 || VERDI == 190 || VERDI == 191
            || VERDI == 194 || VERDI == 195) return 1;
        return 0;
    }
    static int plassere_heltall(int 읽는자리) {
        if (!klippe(읽는자리, 4)) { feil_VERDI("truncated bytecode operand"); return 0; }
        return Fil[읽는자리] << 24 | Fil[읽는자리 + 1] << 16 | Fil[읽는자리 + 2] << 8 | Fil[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int Kjør_2, int 끝) {
        int VERDI = Fil[읽는자리], lengde_VERDI = kommando_lengde(VERDI);
        if (VERDI == 170 || VERDI == 171) {
            int grunnlag_plassere = 읽는자리 + 1;
            while ((grunnlag_plassere - Kjør_2) % 4 != 0) grunnlag_plassere++;
            if (끝 - grunnlag_plassere < (VERDI == 170 ? 12 : 8)) return 0;
            int oppføring_ANTALL = VERDI == 170 ? plassere_heltall(grunnlag_plassere + 8) - plassere_heltall(grunnlag_plassere + 4) + 1 : plassere_heltall(grunnlag_plassere + 4);
            if (oppføring_ANTALL < 0 || oppføring_ANTALL > 2048) return 0;
            lengde_VERDI = grunnlag_plassere - 읽는자리 + (VERDI == 170 ? 12 + 4 * oppføring_ANTALL : 8 + 8 * oppføring_ANTALL);
        }
        if (VERDI == 196 && 읽는자리 + 1 < 끝) {
            int ord_data = Fil[읽는자리 + 1]; lengde_VERDI = ord_data == 132 ? 6 : (ord_data == 21 || ord_data == 25 || ord_data == 54 || ord_data == 58) ? 4 : 0;
        }
        return lengde_VERDI > 0 && lengde_VERDI <= 끝 - 읽는자리 ? lengde_VERDI : 0;
    }
    static void sjekk_mål_VERDI(int mål_VERDI, int FUNKSJON_VERDI) {
        if (mål_VERDI < metode_START[FUNKSJON_VERDI] || mål_VERDI >= metode_avslutte_en_samtale[FUNKSJON_VERDI] || grense_VERDI[mål_VERDI] != FUNKSJON_VERDI + 1) feil_VERDI("invalid branch target");
    }
    static void 클래스읽기(int time_Definisjon) {
        현재읽는종 = time_Definisjon; 읽기위치 = time_Definisjon * 16384; Størrelse = 읽기위치 + time_Definisjon_skalere[time_Definisjon];
        if (heltall() != 0xcafebabe) { feil_VERDI("not a class file"); return; }
        int 부판 = 짧은수(), versjon_VERDI = 짧은수();
        if (versjon_VERDI < 45 || versjon_VERDI > 52 || 부판 != 0) { feil_VERDI("supported class versions: 45..52, minor 0"); return; }
        int konstant_ANTALL = 짧은수(), grunnlag_plassere = time_Definisjon * 512;
        if (konstant_ANTALL < 1 || konstant_ANTALL > 512) { feil_VERDI("constant pool limit (511)"); return; }
        for (int oppføring_ANTALL = 1; oppføring_ANTALL < konstant_ANTALL && !feil; oppføring_ANTALL++) {
            int nummer = grunnlag_plassere + oppføring_ANTALL, 종류 = byte_VERDI(); konstant_kode[nummer] = 종류;
            if (종류 == 1) { konstant_SEKUND_VERDI[nummer] = 짧은수(); 상가[nummer] = 읽기위치; 건너(konstant_SEKUND_VERDI[nummer]); }
            else if (종류 == 3) 상가[nummer] = heltall();
            else if (종류 == 7 || 종류 == 8) 상가[nummer] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[nummer] = 상번호(); konstant_SEKUND_VERDI[nummer] = 상번호(); }
            else feil_VERDI("unsupported constant type");
        }
        int tillatelse_VERDI = 짧은수();
        if ((tillatelse_VERDI & (0x2000 | 0x4000)) != 0) feil_VERDI("annotation/enum class unsupported");
        time_Definisjon_navn[time_Definisjon] = klassenavn_SMS(상번호());
        time_Definisjon_overordnet[time_Definisjon] = klassenavn_SMS(상번호());
        int grensesnitt_ANTALL = 짧은수(); if (grensesnitt_ANTALL > 16) { feil_VERDI("interface count limit"); return; }
        time_grensesnitt_ANTALL[time_Definisjon] = grensesnitt_ANTALL;
        for (int Loop_INDEKS = 0; Loop_INDEKS < grensesnitt_ANTALL; Loop_INDEKS++) time_grensesnitt[time_Definisjon * 16 + Loop_INDEKS] = klassenavn_SMS(상번호());
        int felt_ANTALL = 짧은수();
        if (felt_ANTALL > 512 - åpning_ANTALL) { feil_VERDI("field count limit (512)"); return; }
        for (int Loop_INDEKS = 0; Loop_INDEKS < felt_ANTALL && !feil; Loop_INDEKS++) {
            int Fil_INDEKS = åpning_ANTALL++; åpning_eier[Fil_INDEKS] = time_Definisjon; åpning_tillatelse[Fil_INDEKS] = 짧은수(); åpning_navn[Fil_INDEKS] = 상번호(); åpning_Type[Fil_INDEKS] = 상번호();
            sjekk_konstant(åpning_navn[Fil_INDEKS], 1); sjekk_konstant(åpning_Type[Fil_INDEKS], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[åpning_Type[Fil_INDEKS]]; int område_KODE = 서술형(읽기위치 + konstant_SEKUND_VERDI[åpning_Type[Fil_INDEKS]], false); 읽기위치 = 보존값;
            if ((åpning_tillatelse[Fil_INDEKS] & 8) == 0) åpning_plassere[Fil_INDEKS] = time_åpning_ANTALL[time_Definisjon]++;
            int attributt_data = 짧은수();
            for (int indre_kobling_plassere = 0; indre_kobling_plassere < attributt_data && !feil; indre_kobling_plassere++) {
                int navn_konstant = 상번호(), gyldig_lengde = heltall();
                if (ord_SMS(navn_konstant, "ConstantValue") && gyldig_lengde == 2) {
                    int data_VERDI = 상번호();
                    if (område_KODE == 1 && sjekk_konstant(data_VERDI, 3)) åpning_data[Fil_INDEKS] = 상가[data_VERDI];
                    else if (område_KODE == 2 && sjekk_konstant(data_VERDI, 8)) åpning_data[Fil_INDEKS] = konstant_SMS(상가[data_VERDI]);
                } else 건너(gyldig_lengde);
            }
        }
        int vare_ANTALL = 짧은수();
        if (vare_ANTALL > 512 - metode_ANTALL) { feil_VERDI("method count limit (512)"); return; }
        for (int Loop_INDEKS = 0; Loop_INDEKS < vare_ANTALL && !feil; Loop_INDEKS++) {
            int nummer = metode_ANTALL++; metode_eier[nummer] = time_Definisjon;
            metode_tilgang[nummer] = 짧은수(); metode_navn_SMS[nummer] = 상번호(); metode_Type[nummer] = 상번호();
            sjekk_konstant(metode_navn_SMS[nummer], 1); 서술읽기(nummer);
            if ((metode_tilgang[nummer] & 8) == 0) {
                if (metode_argument_ANTALL[nummer] == 16) { feil_VERDI("too many instance method arguments"); return; }
                for (int Sammenligning_plassere = metode_argument_ANTALL[nummer]; Sammenligning_plassere > 0; Sammenligning_plassere--) metode_argument_Type[nummer * 16 + Sammenligning_plassere] = metode_argument_Type[nummer * 16 + Sammenligning_plassere - 1];
                metode_argument_Type[nummer * 16] = 2; metode_argument_ANTALL[nummer]++;
            }
            if ((metode_tilgang[nummer] & 0x100) != 0) feil_VERDI("user native method unsupported");
            if (ord_SMS(metode_navn_SMS[nummer], "<clinit>")) starte_time_Definisjon[time_Definisjon] = nummer + 1;
            for (int frontkamera_VERDI = 0; frontkamera_VERDI < nummer; frontkamera_VERDI++) if (metode_eier[frontkamera_VERDI] == time_Definisjon && avstemming_ord(metode_navn_SMS[frontkamera_VERDI], metode_navn_SMS[nummer]) && avstemming_ord(metode_Type[frontkamera_VERDI], metode_Type[nummer])) feil_VERDI("duplicate method");
            int attributt_ANTALL = 짧은수();
            for (int attributtverdi = 0; attributtverdi < attributt_ANTALL && !feil; attributtverdi++) {
                int Navn = 상번호(), lengde_VERDI = heltall(), Kjør_2 = 읽기위치;
                if (!klippe(Kjør_2, lengde_VERDI)) { feil_VERDI("truncated method attribute"); break; }
                if (ord_SMS(Navn, "Code")) {
                    if (metode_START[nummer] != 0) feil_VERDI("duplicate Code attribute");
                    metode_stakk[nummer] = 짧은수(); 함수지역[nummer] = 짧은수(); int KODE_lengde = heltall();
                    if (metode_stakk[nummer] > 128 || 함수지역[nummer] > 128 || 함수지역[nummer] < metode_argument_ANTALL[nummer]
                        || KODE_lengde < 1 || KODE_lengde > 8192) feil_VERDI("method memory limits exceeded");
                    metode_START[nummer] = 읽기위치; 건너(KODE_lengde); metode_avslutte_en_samtale[nummer] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { feil_VERDI("exception table limit"); return; }
                    for (int indre_kobling_plassere = 0; indre_kobling_plassere < 잡는수; indre_kobling_plassere++) {
                        int feil_referere = 잡기수++; 잡기함수[feil_referere] = nummer;
                        잡기시작[feil_referere] = metode_START[nummer] + 짧은수(); 잡기끝[feil_referere] = metode_START[nummer] + 짧은수();
                        잡기위치[feil_referere] = metode_START[nummer] + 짧은수(); int 부호값 = 상번호(); 잡기종[feil_referere] = 부호값 == 0 ? 0 : klassenavn_SMS(부호값);
                    }
                    hoppe_over_attributt();
                    if (읽기위치 != Kjør_2 + lengde_VERDI) feil_VERDI("Code attribute size mismatch");
                } else 건너(lengde_VERDI);
            }
            if ((metode_tilgang[nummer] & 0x400) != 0) continue;
            if (metode_START[nummer] == 0) feil_VERDI("missing Code attribute");
            int åpning_oppføring = metode_START[nummer];
            while (åpning_oppføring < metode_avslutte_en_samtale[nummer] && !feil) {
                int lengde_VERDI = 길이읽기(åpning_oppføring, metode_START[nummer], metode_avslutte_en_samtale[nummer]);
                if (lengde_VERDI == 0) { feil_VERDI("unsupported or truncated bytecode"); break; }
                grense_VERDI[åpning_oppføring] = nummer + 1; åpning_oppføring += lengde_VERDI;
            }
            åpning_oppføring = metode_START[nummer];
            while (åpning_oppføring < metode_avslutte_en_samtale[nummer] && !feil) {
                int VERDI = Fil[åpning_oppføring];
                if (VERDI >= 153 && VERDI <= 167 || VERDI == 198 || VERDI == 199) sjekk_mål_VERDI(åpning_oppføring + (short)(Fil[åpning_oppføring + 1] << 8 | Fil[åpning_oppføring + 2]), nummer);
                if (VERDI == 200) sjekk_mål_VERDI(åpning_oppføring + plassere_heltall(åpning_oppføring + 1), nummer);
                if (VERDI == 170 || VERDI == 171) {
                    int 읽는자리 = åpning_oppføring + 1; while ((읽는자리 - metode_START[nummer]) % 4 != 0) 읽는자리++;
                    sjekk_mål_VERDI(åpning_oppføring + plassere_heltall(읽는자리), nummer);
                    int oppføring_ANTALL = VERDI == 170 ? plassere_heltall(읽는자리 + 8) - plassere_heltall(읽는자리 + 4) + 1 : plassere_heltall(읽는자리 + 4);
                    읽는자리 += VERDI == 170 ? 12 : 8;
                    for (int indre_kobling_plassere = 0; indre_kobling_plassere < oppføring_ANTALL; indre_kobling_plassere++) sjekk_mål_VERDI(åpning_oppføring + plassere_heltall(읽는자리 + indre_kobling_plassere * (VERDI == 170 ? 4 : 8) + (VERDI == 170 ? 0 : 4)), nummer);
                }
                åpning_oppføring += 길이읽기(åpning_oppføring, metode_START[nummer], metode_avslutte_en_samtale[nummer]);
            }
            for (int indre_kobling_plassere = 0; indre_kobling_plassere < 잡기수; indre_kobling_plassere++) if (잡기함수[indre_kobling_plassere] == nummer) {
                sjekk_mål_VERDI(잡기시작[indre_kobling_plassere], nummer); sjekk_mål_VERDI(잡기위치[indre_kobling_plassere], nummer);
                if (잡기끝[indre_kobling_plassere] != metode_avslutte_en_samtale[nummer]) sjekk_mål_VERDI(잡기끝[indre_kobling_plassere], nummer);
                if (잡기시작[indre_kobling_plassere] >= 잡기끝[indre_kobling_plassere]) feil_VERDI("invalid exception range");
            }
        }
        if (!feil) hoppe_over_attributt();
        if (읽기위치 != Størrelse) feil_VERDI("extra class file data");
    }
    static int tildele_lager(int 종류, int lengde_VERDI) { return 새기억(종류, lengde_VERDI); }
    static boolean objekt_VERDI(int referere, int 종류) {
        if (!informasjonssystemer_gyldig_objekt(referere)) return false;
        if (heap_VERDI[referere] != 종류) { feil_VERDI("object type mismatch"); return false; }
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
        if (return_Type == 2) beskytte_VERDI(operand_stakk_VERDI[åpning_oppføring]);
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
        if (bilde_INDEKS % 32 == 31) { feil_VERDI("call stack limit (32)"); return; }
        int Neste_vare = bilde_INDEKS + 1;
        for (int nummer = 0; nummer < 128; nummer++) lokal_Type[Neste_vare * 128 + nummer] = 0;
        for (int nummer = metode_argument_ANTALL[FUNKSJON_VERDI] - 1; nummer >= 0; nummer--) {
            lokal_VERDI[Neste_vare * 128 + nummer] = 빼기(metode_argument_Type[FUNKSJON_VERDI * 16 + nummer]); lokal_Type[Neste_vare * 128 + nummer] = metode_argument_Type[FUNKSJON_VERDI * 16 + nummer];
        }
        if (feil) return;
        bilde_INDEKS = Neste_vare; starte_bilde[bilde_INDEKS] = 0; bilde_metode[bilde_INDEKS] = FUNKSJON_VERDI; bilde_plassere[bilde_INDEKS] = metode_START[FUNKSJON_VERDI]; bilde_stakk[bilde_INDEKS] = 0;
    }
    static void return_KR(int Type_VERDI) {
        if (Type_VERDI != metode_return[bilde_metode[bilde_INDEKS]]) { feil_VERDI("return type mismatch"); return; }
        int VERDI = Type_VERDI == 0 ? 0 : 빼기(Type_VERDI);
        if (starte_bilde[bilde_INDEKS] != 0) time_Definisjon_status[starte_bilde[bilde_INDEKS] - 1] = 2;
        if (bilde_blokkere[bilde_INDEKS] != 0) { frigi_blokkere(bilde_blokkere[bilde_INDEKS]); bilde_blokkere[bilde_INDEKS] = 0; }
        bilde_INDEKS--; if (bilde_INDEKS >= betalt_tråd * 32 && Type_VERDI != 0) 넣기(VERDI, Type_VERDI);
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
                if (VERDI < 1) { feil_VERDI("invalid file stream path"); return; }
                strøm_filnavn[åpning_oppføring] = VERDI;
            }
            strøm_filnavn[lengde_VERDI] = 0;
            int 서술자 = bruker.파일서술자열기(strøm_filnavn, Utgang ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { feil_VERDI("FileNotFoundException: file open failed"); return; }
            heap_VERDI[strøm_VERDI + 2] = 서술자; heap_VERDI[strøm_VERDI + 3] = 1;
            return;
        }
        if (Kommando != 182) { feil_VERDI("invalid file stream invocation"); return; }
        if ((Utgang && ord_SMS(Navn, "write") || !Utgang && ord_SMS(Navn, "read"))
            && (ord_SMS(format_VERDI, Utgang ? "([B)V" : "([B)I") || ord_SMS(format_VERDI, Utgang ? "([BII)V" : "([BII)I"))) {
            boolean klippe_VERDI = ord_SMS(format_VERDI, Utgang ? "([BII)V" : "([BII)I");
            int oppføring_ANTALL = klippe_VERDI ? 빼기(1) : 0, 시작점 = klippe_VERDI ? 빼기(1) : 0, data_MATRISE = 빼기(2), objekt_referere = 빼기(2);
            if (!objekt_VERDI(data_MATRISE, 20) || !objekt_VERDI(objekt_referere, 종류)) return;
            if (!klippe_VERDI) oppføring_ANTALL = heap_VERDI[data_MATRISE + 1];
            if (시작점 < 0 || oppføring_ANTALL < 0 || 시작점 > heap_VERDI[data_MATRISE + 1] - oppføring_ANTALL) { 예외던짐(6, "file buffer bounds"); return; }
            if (heap_VERDI[objekt_referere + 3] == 0 || heap_VERDI[objekt_referere + 2] < 0) { feil_VERDI("IOException: stream closed"); return; }
            int Fullført_ANTALL = 0;
            while (Fullført_ANTALL < oppføring_ANTALL && !feil) {
                int 반환값 = Utgang ? bruker.파일한바이트쓰기(heap_VERDI[objekt_referere + 2], heap_VERDI[data_MATRISE + 2 + 시작점 + Fullført_ANTALL]) : bruker.파일한바이트읽기(heap_VERDI[objekt_referere + 2]);
                if (반환값 < 0) { feil_VERDI(Utgang ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!Utgang && 반환값 == 256) break;
                if (!Utgang) heap_VERDI[data_MATRISE + 2 + 시작점 + Fullført_ANTALL] = (byte)반환값;
                Fullført_ANTALL++;
            }
            if (!Utgang) 넣기(oppføring_ANTALL != 0 && Fullført_ANTALL == 0 ? -1 : Fullført_ANTALL, 1);
            return;
        }
        if (Utgang && ord_SMS(Navn, "flush") && ord_SMS(format_VERDI, "()V")) { int objekt_referere = 빼기(2); if (objekt_VERDI(objekt_referere, 종류) && heap_VERDI[objekt_referere + 2] < 0) feil_VERDI("IOException: stream closed"); return; }
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
            if (KR < -1) feil_VERDI("IOException: read failed"); else 넣기(KR == 256 ? -1 : KR, 1);
        } else if (bruker.파일한바이트쓰기(서술자, VERDI) != 1) feil_VERDI("IOException: write failed");
    }
    static void Ring_metode(int INDEKS, int Kommando) {
        if (INDEKS <= 0 || INDEKS >= konstant_kode.length || (konstant_kode[INDEKS] != 10 && konstant_kode[INDEKS] != 11)) { feil_VERDI("invalid method reference"); return; }
        int eier_VERDI = klassenavn_SMS(상가[INDEKS]), Navn = referere_navn(konstant_SEKUND_VERDI[INDEKS]), format_VERDI = referansetype(konstant_SEKUND_VERDI[INDEKS]);
        if (feil) return;
        if (기본호출(eier_VERDI, Navn, format_VERDI, Kommando)) return;
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
        int time_Definisjon = Søk_time_Definisjon(eier_VERDI); if (time_Definisjon < 0 || feil) return;
        int Fil_INDEKS = Søk_metode(time_Definisjon, Navn, format_VERDI);
        if (Fil_INDEKS < 0) {
            for (int tegnkode = time_Definisjon, oppføring_ANTALL = 0; tegnkode >= 0 && oppføring_ANTALL < 16; oppføring_ANTALL++, tegnkode = overordnet_time(tegnkode))
                if (ord_SMS(time_Definisjon_overordnet[tegnkode], "java/lang/Thread")) { 가닥호출(Navn, format_VERDI, Kommando); return; }
            feil_VERDI("NoSuchMethodError"); return;
        }
        if (((metode_tilgang[Fil_INDEKS] & 8) != 0) != (Kommando == 184)) { feil_VERDI("method static/instance mismatch"); return; }
        if (Kommando == 184) { if (!starte(metode_eier[Fil_INDEKS], 틀명령[bilde_INDEKS])) return; }
        else {
            int 읽는자리 = bilde_stakk[bilde_INDEKS] - metode_argument_ANTALL[Fil_INDEKS];
            if (읽는자리 < 0 || operand_stakk_Type[bilde_INDEKS * 128 + 읽는자리] != 2) { feil_VERDI("invalid method receiver"); return; }
            int objekt_referere = operand_stakk_VERDI[bilde_INDEKS * 128 + 읽는자리];
            if (!informasjonssystemer_gyldig_objekt(objekt_referere)) return;
            if (heap_VERDI[objekt_referere] < 32 || !종포함(heap_VERDI[objekt_referere] - 32, eier_VERDI)) { feil_VERDI("method receiver type mismatch"); return; }
            if (Kommando != 183) Fil_INDEKS = Søk_metode(heap_VERDI[objekt_referere] - 32, Navn, format_VERDI);
        }
        if (Fil_INDEKS < 0 || (metode_tilgang[Fil_INDEKS] & 0x400) != 0) { feil_VERDI("AbstractMethodError"); return; }
        int blokkere_referere = 0;
        if ((metode_tilgang[Fil_INDEKS] & 32) != 0) {
            if (Kommando == 184) { int tegnkode = metode_eier[Fil_INDEKS]; if (time_blokkere[tegnkode] == 0) time_blokkere[tegnkode] = tildele_lager(8, 0); blokkere_referere = time_blokkere[tegnkode]; }
            else blokkere_referere = operand_stakk_VERDI[bilde_INDEKS * 128 + bilde_stakk[bilde_INDEKS] - metode_argument_ANTALL[Fil_INDEKS]];
            if (!잠금얻기(blokkere_referere)) { if (!feil) bilde_plassere[bilde_INDEKS] = 틀명령[bilde_INDEKS]; return; }
        }
        호출(Fil_INDEKS); if (!feil) bilde_blokkere[bilde_INDEKS] = blokkere_referere;
    }
    static boolean 배열저장가능(int MATRISE_referere, int data_VERDI) {
        if (data_VERDI == 0 || matriseelement[MATRISE_referere] == 0) return true;
        boolean 성공여부 = matriseelement[MATRISE_referere] == -1 ? (data_VERDI > 0 && data_VERDI < heap_avslutte_en_samtale_plassere && heap_VERDI[data_VERDI] == 1) : avstemming_objekt(data_VERDI, matriseelement[MATRISE_referere]);
        if (!성공여부 && !feil) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int MATRISE_åpning(int referere, int senket_skrift_VERDI, int Type_VERDI) {
        if (!objekt_VERDI(referere, Type_VERDI)) return 0;
        if (senket_skrift_VERDI < 0 || senket_skrift_VERDI >= heap_VERDI[referere + 1]) { feil_VERDI("ArrayIndexOutOfBoundsException"); return 0; }
        return referere + 2 + senket_skrift_VERDI;
    }
    static void Utfør_kommando() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (feil) { if (던진객체 != 0) håndtak_unntak(); if (feil || bilde_INDEKS < betalt_tråd * 32) break; }
            if (bilde_INDEKS < betalt_tråd * 32 || endringsforespørsel || --조각 == 0) { if (!bytt_tråd()) break; 조각 = 100; }
            if (bilde_INDEKS == 0 && time_Definisjon_status[oppføring_time_Definisjon] != 2 && !starte(oppføring_time_Definisjon, bilde_plassere[bilde_INDEKS])) continue;
            if (bilde_INDEKS == betalt_tråd * 32 && betalt_tråd != 0 && (metode_tilgang[bilde_metode[bilde_INDEKS]] & 32) != 0 && bilde_blokkere[bilde_INDEKS] == 0) {
                int objekt_referere = tråd_mål[betalt_tråd]; if (!잠금얻기(objekt_referere)) { if (feil) break; continue; } bilde_blokkere[bilde_INDEKS] = objekt_referere;
            }
            잠시수 = 0;
            if (--남음 == 0) { feil_VERDI("instruction limit (500000)"); break; }
            int Kjør_2 = bilde_plassere[bilde_INDEKS]; 틀명령[bilde_INDEKS] = Kjør_2; int VERDI = 명바();
            if (feil) break;
            if (VERDI == 0) continue;
            if (VERDI == 1) { 넣기(0, 2); continue; }
            if (VERDI >= 2 && VERDI <= 8) { 넣기(VERDI - 3, 1); continue; }
            if (VERDI == 16) { 넣기((byte)명바(), 1); continue; }
            if (VERDI == 17) { 넣기((short)명짧(), 1); continue; }
            if (VERDI == 18 || VERDI == 19) {
                int nummer = metode_eier[bilde_metode[bilde_INDEKS]] * 512 + (VERDI == 18 ? 명바() : 명짧());
                if (nummer <= 0 || nummer >= konstant_kode.length) feil_VERDI("invalid ldc constant");
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
            if (VERDI == 46 || VERDI >= 50 && VERDI <= 53) {
                int oppføring_plassere = 빼기(1), objekt_referere = 빼기(2), område_KODE = VERDI == 46 ? 2 : VERDI == 50 ? 3 : VERDI == 51 ? 20 : VERDI == 52 ? 22 : 23;
                if (VERDI == 51 && objekt_referere > 0 && objekt_referere < heap_avslutte_en_samtale_plassere && heap_VERDI[objekt_referere] == 21) område_KODE = 21;
                int 읽는자리 = MATRISE_åpning(objekt_referere, oppføring_plassere, område_KODE); if (!feil) 넣기(heap_VERDI[읽는자리], VERDI == 50 ? 2 : 1); continue;
            }
            if (VERDI == 79 || VERDI >= 83 && VERDI <= 86) {
                int oppføring_referere = 빼기(VERDI == 83 ? 2 : 1), oppføring_plassere = 빼기(1), objekt_referere = 빼기(2), område_KODE = VERDI == 79 ? 2 : VERDI == 83 ? 3 : VERDI == 84 ? 20 : VERDI == 85 ? 22 : 23;
                if (VERDI == 84 && objekt_referere > 0 && objekt_referere < heap_avslutte_en_samtale_plassere && heap_VERDI[objekt_referere] == 21) område_KODE = 21;
                int 읽는자리 = MATRISE_åpning(objekt_referere, oppføring_plassere, område_KODE);
                if (!feil && område_KODE == 3 && !배열저장가능(objekt_referere, oppføring_referere)) continue;
                if (!feil) heap_VERDI[읽는자리] = område_KODE == 20 ? (byte)oppføring_referere : område_KODE == 21 ? oppføring_referere & 1 : område_KODE == 22 ? (char)oppføring_referere : område_KODE == 23 ? (short)oppføring_referere : oppføring_referere;
                continue;
            }
            if (VERDI >= 87 && VERDI <= 95) { 스택명령(VERDI); continue; }
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
            if (VERDI >= 178 && VERDI <= 181) { 필드호출(명상수(), VERDI, Kjør_2); continue; }
            if (VERDI >= 182 && VERDI <= 185) {
                int 부호값 = 명상수();
                if (VERDI == 185) { int total_ANTALL = 명바(); if (total_ANTALL == 0 || 명바() != 0) { feil_VERDI("invalid invokeinterface operands"); continue; } }
                Ring_metode(부호값, VERDI); continue;
            }
            if (VERDI == 187) { 새객체(klassenavn_SMS(명상수()), Kjør_2); continue; }
            if (VERDI == 188 || VERDI == 189) {
                int område_KODE = 3, komponent = 0;
                if (VERDI == 188) { int 임시값 = 명바(); område_KODE = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else komponent = klassenavn_SMS(명상수());
                if (område_KODE == 0) { feil_VERDI("unsupported primitive array type"); continue; }
                int gyldig_lengde = 빼기(1), objekt_referere = tildele_lager(område_KODE, gyldig_lengde); if (!feil) matriseelement[objekt_referere] = komponent; 넣기(objekt_referere, 2); continue;
            }
            if (VERDI == 190) {
                int objekt_referere = 빼기(2);
                if (informasjonssystemer_gyldig_objekt(objekt_referere)) { int Sammenligning_plassere = heap_VERDI[objekt_referere]; if (Sammenligning_plassere != 2 && Sammenligning_plassere != 3 && (Sammenligning_plassere < 20 || Sammenligning_plassere > 23)) feil_VERDI("not an array"); else 넣기(heap_VERDI[objekt_referere + 1], 1); }
                continue;
            }
            if (VERDI == 191) {
                int objekt_referere = 빼기(2); if (informasjonssystemer_gyldig_objekt(objekt_referere)) { if (heap_VERDI[objekt_referere] != 9) feil_VERDI("athrow requires supported Throwable"); else { 던진객체 = objekt_referere; feil = true; } }
                continue;
            }
            if (VERDI == 192 || VERDI == 193) {
                int navn_konstant = klassenavn_SMS(명상수()), objekt_referere = 빼기(2); boolean SAMMENLIGNE = avstemming_objekt(objekt_referere, navn_konstant);
                if (VERDI == 193) 넣기(objekt_referere != 0 && SAMMENLIGNE ? 1 : 0, 1);
                else { if (!SAMMENLIGNE && !feil) feil_VERDI("ClassCastException"); 넣기(objekt_referere, 2); }
                continue;
            }
            if (VERDI == 170 || VERDI == 171) {
                int 읽는자리 = Kjør_2 + 1, Fil_INDEKS = bilde_metode[bilde_INDEKS], tast_referere = 빼기(1);
                while ((읽는자리 - metode_START[Fil_INDEKS]) % 4 != 0) 읽는자리++;
                int mål_e_post = plassere_heltall(읽는자리);
                if (VERDI == 170) { int 낮은값 = plassere_heltall(읽는자리 + 4), 높은값 = plassere_heltall(읽는자리 + 8); if (tast_referere >= 낮은값 && tast_referere <= 높은값) mål_e_post = plassere_heltall(읽는자리 + 12 + (tast_referere - 낮은값) * 4); }
                else { int total_ANTALL = plassere_heltall(읽는자리 + 4); for (int Loop_INDEKS = 0; Loop_INDEKS < total_ANTALL; Loop_INDEKS++) if (plassere_heltall(읽는자리 + 8 + Loop_INDEKS * 8) == tast_referere) mål_e_post = plassere_heltall(읽는자리 + 12 + Loop_INDEKS * 8); }
                flytte_VERDI_83b651b8(Kjør_2 + mål_e_post); continue;
            }
            if (VERDI == 200) { flytte_VERDI_83b651b8(Kjør_2 + plassere_heltall(Kjør_2 + 1)); continue; }
            if (VERDI == 194 || VERDI == 195) {
                int objekt_referere = 빼기(2);
                if (VERDI == 195) frigi_blokkere(objekt_referere);
                else if (!잠금얻기(objekt_referere) && !feil) { 넣기(objekt_referere, 2); bilde_plassere[bilde_INDEKS] = Kjør_2; }
                continue;
            }
            if (VERDI == 196) {
                int kommando_KODE = 명바(), oppføring_plassere = 명짧();
                if (kommando_KODE == 21 || kommando_KODE == 25) 지역읽기(oppføring_plassere, kommando_KODE == 21 ? 1 : 2);
                else if (kommando_KODE == 54 || kommando_KODE == 58) skrive_lokal(oppføring_plassere, kommando_KODE == 54 ? 1 : 2);
                else if (kommando_KODE == 132) { int DELTA_VERDI = (short)명짧(); 지역읽기(oppføring_plassere, 1); 넣기(빼기(1) + DELTA_VERDI, 1); skrive_lokal(oppføring_plassere, 1); }
                else feil_VERDI("unsupported wide opcode");
                continue;
            }
            feil_VERDI("unsupported bytecode");
        }
    }
    static int Søk_time_Definisjon(int Navn) {
        for (int Loop_INDEKS = 0; Loop_INDEKS < time_Definisjon_ANTALL; Loop_INDEKS++) if (time_Definisjon_navn[Loop_INDEKS] != 0 && avstemming_ord(time_Definisjon_navn[Loop_INDEKS], Navn)) return Loop_INDEKS;
        return dossier_time_Definisjon(konstant_SMS(Navn));
    }
    static int dossier_time_Definisjon(int navn_streng) {
        if (!objekt_VERDI(navn_streng, 1)) return -1;
        int lengde_VERDI = heap_VERDI[navn_streng + 1];
        if (lengde_VERDI < 1 || lengde_VERDI > 505 || time_Definisjon_ANTALL == 16) { feil_VERDI("class name/count limit"); return -1; }
        for (int Loop_INDEKS = 0; Loop_INDEKS < lengde_VERDI; Loop_INDEKS++) { int tegnkode = heap_VERDI[navn_streng + 2 + Loop_INDEKS]; filnavn_SMS[Loop_INDEKS] = tegnkode == '/' ? '.' : tegnkode; }
        filnavn_SMS[lengde_VERDI] = '.'; filnavn_SMS[lengde_VERDI + 1] = 'c'; filnavn_SMS[lengde_VERDI + 2] = 'l'; filnavn_SMS[lengde_VERDI + 3] = 'a'; filnavn_SMS[lengde_VERDI + 4] = 's'; filnavn_SMS[lengde_VERDI + 5] = 's'; filnavn_SMS[lengde_VERDI + 6] = 0;
        int Størrelse = bruker.파일읽기(filnavn_SMS, midlertidig_fil);
        if (Størrelse < 0) { feil_VERDI("ClassNotFoundException"); return -1; }
        int time_Definisjon = time_Definisjon_ANTALL++; time_Definisjon_skalere[time_Definisjon] = Størrelse;
        for (int Loop_INDEKS = 0; Loop_INDEKS < Størrelse; Loop_INDEKS++) Fil[time_Definisjon * 16384 + Loop_INDEKS] = midlertidig_fil[Loop_INDEKS];
        클래스읽기(time_Definisjon); if (feil) return -1;
        int faktisk_data = konstant_SMS(time_Definisjon_navn[time_Definisjon]);
        if (!글같음(faktisk_data, navn_streng, true)) { feil_VERDI("class name does not match file"); return -1; }
        int overordnet_VERDI_881a8172 = time_Definisjon_overordnet[time_Definisjon];
        if (overordnet_VERDI_881a8172 != 0 && !ord_SMS(overordnet_VERDI_881a8172, "java/lang/Object") && !ord_SMS(overordnet_VERDI_881a8172, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 prøve_på_nytt_VERDI 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = Søk_time_Definisjon(overordnet_VERDI_881a8172);
            if (feil || 위 < 0) return -1;
            int 읽는자리 = 위, fase_ANTALL = 0;
            while (읽는자리 >= 0 && fase_ANTALL++ < 16) {
                if (읽는자리 == time_Definisjon) { feil_VERDI("cyclic inheritance"); return -1; }
                읽는자리 = overordnet_time(읽는자리);
            }
            int 시작변위 = time_åpning_ANTALL[위];
            for (int Fil_INDEKS = 0; Fil_INDEKS < åpning_ANTALL; Fil_INDEKS++) if (åpning_eier[Fil_INDEKS] == time_Definisjon && (åpning_tillatelse[Fil_INDEKS] & 8) == 0) åpning_plassere[Fil_INDEKS] += 시작변위;
            time_åpning_ANTALL[time_Definisjon] += 시작변위;
        }
        return time_Definisjon;
    }
    static int overordnet_time(int time_Definisjon) {
        int Navn = time_Definisjon_overordnet[time_Definisjon];
        for (int Loop_INDEKS = 0; Loop_INDEKS < time_Definisjon_ANTALL; Loop_INDEKS++) if (Navn != 0 && time_Definisjon_navn[Loop_INDEKS] != 0 && avstemming_ord(time_Definisjon_navn[Loop_INDEKS], Navn)) return Loop_INDEKS;
        return -1;
    }
    static int Søk_metode(int time_Definisjon, int Navn, int format_VERDI) {
        for (int 깊이 = 0; time_Definisjon >= 0 && 깊이 < 16; 깊이++, time_Definisjon = overordnet_time(time_Definisjon)) {
            for (int Loop_INDEKS = 0; Loop_INDEKS < metode_ANTALL; Loop_INDEKS++) if (metode_eier[Loop_INDEKS] == time_Definisjon && avstemming_ord(metode_navn_SMS[Loop_INDEKS], Navn) && avstemming_ord(metode_Type[Loop_INDEKS], format_VERDI)) return Loop_INDEKS;
        }
        return -1;
    }
    static int navn_metode(int time_Definisjon, String Navn, String format_VERDI) {
        for (int 깊이 = 0; time_Definisjon >= 0 && 깊이 < 16; 깊이++, time_Definisjon = overordnet_time(time_Definisjon))
            for (int Loop_INDEKS = 0; Loop_INDEKS < metode_ANTALL; Loop_INDEKS++) if (metode_eier[Loop_INDEKS] == time_Definisjon && ord_SMS(metode_navn_SMS[Loop_INDEKS], Navn) && ord_SMS(metode_Type[Loop_INDEKS], format_VERDI)) return Loop_INDEKS;
        return -1;
    }
    static int 형종류(int Navn) { return Fil[상가[Navn]] == 'L' || Fil[상가[Navn]] == '[' ? 2 : 1; }
    static boolean starte(int time_Definisjon, int kommando_START) {
        if (time_Definisjon < 0 || feil) return false;
        if (time_Definisjon_status[time_Definisjon] == 3) { feil_VERDI("NoClassDefFoundError: initialization failed"); return false; }
        if (time_Definisjon_status[time_Definisjon] == 1 && time_tråd[time_Definisjon] != betalt_tråd) { bilde_plassere[bilde_INDEKS] = kommando_START; endringsforespørsel = true; return false; }
        if (time_Definisjon_status[time_Definisjon] != 0) return true;
        int 위 = overordnet_time(time_Definisjon);
        if (위 >= 0 && !starte(위, kommando_START)) return false;
        time_Definisjon_status[time_Definisjon] = 1; time_tråd[time_Definisjon] = betalt_tråd;
        if (starte_time_Definisjon[time_Definisjon] != 0) {
            bilde_plassere[bilde_INDEKS] = kommando_START;
            호출(starte_time_Definisjon[time_Definisjon] - 1); if (!feil) starte_bilde[bilde_INDEKS] = time_Definisjon + 1;
            return false;
        }
        time_Definisjon_status[time_Definisjon] = 2; return true;
    }
    static void 필드호출(int INDEKS, int Kommando, int Kjør_2) {
        if (!sjekk_konstant(INDEKS, 9)) return;
        int eier_VERDI = klassenavn_SMS(상가[INDEKS]), Navn = referere_navn(konstant_SEKUND_VERDI[INDEKS]), format_VERDI = referansetype(konstant_SEKUND_VERDI[INDEKS]);
        if (ord_SMS(eier_VERDI, "java/lang/System") && (ord_SMS(Navn, "out") || ord_SMS(Navn, "err")) && ord_SMS(format_VERDI, "Ljava/io/PrintStream;") && Kommando == 178) { 넣기(-1, 2); return; }
        int time_Definisjon = Søk_time_Definisjon(eier_VERDI); if (time_Definisjon < 0 || feil) return;
        int 찾음 = -1;
        for (int 읽는자리 = time_Definisjon, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = overordnet_time(읽는자리))
            for (int Fil_INDEKS = 0; Fil_INDEKS < åpning_ANTALL; Fil_INDEKS++) if (åpning_eier[Fil_INDEKS] == 읽는자리 && avstemming_ord(åpning_navn[Fil_INDEKS], Navn) && avstemming_ord(åpning_Type[Fil_INDEKS], format_VERDI)) 찾음 = Fil_INDEKS;
        if (찾음 < 0) { feil_VERDI("NoSuchFieldError"); return; }
        boolean statisk_VERDI = Kommando == 178 || Kommando == 179;
        if (statisk_VERDI != ((åpning_tillatelse[찾음] & 8) != 0)) { feil_VERDI("field static/instance mismatch"); return; }
        if (statisk_VERDI && !starte(åpning_eier[찾음], Kjør_2)) return;
        int Type_VERDI = 형종류(format_VERDI), VERDI = 0;
        if (Kommando == 179 || Kommando == 181) VERDI = 빼기(Type_VERDI);
        if (statisk_VERDI) { if (Kommando == 178) 넣기(åpning_data[찾음], Type_VERDI); else if (!feil) åpning_data[찾음] = VERDI; return; }
        int objekt_referere = 빼기(2);
        if (!informasjonssystemer_gyldig_objekt(objekt_referere)) return;
        if (heap_VERDI[objekt_referere] < 32 || !종포함(heap_VERDI[objekt_referere] - 32, eier_VERDI)) { feil_VERDI("field receiver type mismatch"); return; }
        int 보관칸 = objekt_referere + 2 + åpning_plassere[찾음];
        if (Kommando == 180) 넣기(heap_VERDI[보관칸], Type_VERDI);
        else if (!feil) { heap_VERDI[보관칸] = VERDI; heap_referere[보관칸] = Type_VERDI == 2 ? 1 : 0; }
    }
    static boolean 종포함(int time_Definisjon, int Navn) {
        for (int 중첩깊이 = 0; time_Definisjon >= 0 && 중첩깊이 < 16; 중첩깊이++, time_Definisjon = overordnet_time(time_Definisjon)) {
            if (avstemming_ord(time_Definisjon_navn[time_Definisjon], Navn) || (time_Definisjon_overordnet[time_Definisjon] != 0 && avstemming_ord(time_Definisjon_overordnet[time_Definisjon], Navn))) return true;
            for (int indre_kobling_plassere = 0; indre_kobling_plassere < time_grensesnitt_ANTALL[time_Definisjon]; indre_kobling_plassere++) if (avstemming_ord(time_grensesnitt[time_Definisjon * 16 + indre_kobling_plassere], Navn)) return true;
        }
        return false;
    }
    static boolean 글같음(int 첫값, int byte_data, boolean Sti) {
        if (첫값 == byte_data) return true;
        if (첫값 <= 0 || byte_data <= 0 || heap_VERDI[첫값] != 1 || heap_VERDI[byte_data] != 1 || heap_VERDI[첫값 + 1] != heap_VERDI[byte_data + 1]) return false;
        for (int Loop_INDEKS = 0; Loop_INDEKS < heap_VERDI[첫값 + 1]; Loop_INDEKS++) {
            int x_koordinat = heap_VERDI[첫값 + 2 + Loop_INDEKS], Y_koordinat = heap_VERDI[byte_data + 2 + Loop_INDEKS];
            if (Sti) { if (x_koordinat == '.') x_koordinat = '/'; if (Y_koordinat == '.') Y_koordinat = '/'; }
            if (x_koordinat != Y_koordinat) return false;
        }
        return true;
    }
    static boolean informasjonssystemer_gyldig_objekt(int objekt_referere) {
        if (objekt_referere == 0) { feil_VERDI("NullPointerException"); return false; }
        if (objekt_referere < 1 || objekt_referere >= heap_avslutte_en_samtale_plassere || 힙폭[objekt_referere] < 2 || heap_VERDI[objekt_referere] == 0) { feil_VERDI("invalid object reference"); return false; }
        return true;
    }
    static void beskytte_VERDI(int objekt_referere) {
        if (objekt_referere > 0 && objekt_referere < heap_avslutte_en_samtale_plassere && 힙폭[objekt_referere] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = objekt_referere;
    }
    static void vise_VERDI_487749b8(int objekt_referere) {
        if (objekt_referere > 0 && objekt_referere < heap_avslutte_en_samtale_plassere && 힙폭[objekt_referere] >= 2 && heap_VERDI[objekt_referere] != 0 && 힙표시[objekt_referere] == 0) {
            힙표시[objekt_referere] = 1; 표시대기[vise_ANTALL++] = objekt_referere;
        }
    }
    static void 수거() {
        vise_ANTALL = 0; Samling_ANTALL++;
        for (int sjekk_plassere = 1; sjekk_plassere < heap_avslutte_en_samtale_plassere; sjekk_plassere += 힙폭[sjekk_plassere]) 힙표시[sjekk_plassere] = 0;
        for (int Loop_INDEKS = 0; Loop_INDEKS < streng_referere.length; Loop_INDEKS++) vise_VERDI_487749b8(streng_referere[Loop_INDEKS]);
        for (int Loop_INDEKS = 0; Loop_INDEKS < åpning_ANTALL; Loop_INDEKS++) if ((åpning_tillatelse[Loop_INDEKS] & 8) != 0 && 형종류(åpning_Type[Loop_INDEKS]) == 2) vise_VERDI_487749b8(åpning_data[Loop_INDEKS]);
        for (int 임시값 = 0; 임시값 < Trådteller; 임시값++) {
            vise_VERDI_487749b8(tråd_objekt[임시값]); vise_VERDI_487749b8(tråd_mål[임시값]);
            int 꼭대기자리 = 임시값 == betalt_tråd ? bilde_INDEKS : tråd_bilde[임시값];
            for (int Fil_INDEKS = 임시값 * 32; Fil_INDEKS <= 꼭대기자리; Fil_INDEKS++) {
                for (int indre_kobling_plassere = 0; indre_kobling_plassere < 함수지역[bilde_metode[Fil_INDEKS]]; indre_kobling_plassere++) if (lokal_Type[Fil_INDEKS * 128 + indre_kobling_plassere] == 2) vise_VERDI_487749b8(lokal_VERDI[Fil_INDEKS * 128 + indre_kobling_plassere]);
                for (int indre_kobling_plassere = 0; indre_kobling_plassere < bilde_stakk[Fil_INDEKS]; indre_kobling_plassere++) if (operand_stakk_Type[Fil_INDEKS * 128 + indre_kobling_plassere] == 2) vise_VERDI_487749b8(operand_stakk_VERDI[Fil_INDEKS * 128 + indre_kobling_plassere]);
            }
        }
        for (int Loop_INDEKS = 0; Loop_INDEKS < skjermbilde_referere.length; Loop_INDEKS++) vise_VERDI_487749b8(skjermbilde_referere[Loop_INDEKS]);
        for (int Loop_INDEKS = 0; Loop_INDEKS < 나중수; Loop_INDEKS++) vise_VERDI_487749b8(나중실행[Loop_INDEKS]);
        for (int Loop_INDEKS = 0; Loop_INDEKS < Store_heltall.length; Loop_INDEKS++) vise_VERDI_487749b8(Store_heltall[Loop_INDEKS]);
        for (int Loop_INDEKS = 0; Loop_INDEKS < time_Definisjon_ANTALL; Loop_INDEKS++) vise_VERDI_487749b8(time_blokkere[Loop_INDEKS]);
        for (int sjekk_plassere = 1; sjekk_plassere < heap_avslutte_en_samtale_plassere; sjekk_plassere += 힙폭[sjekk_plassere]) if (잠금깊이[sjekk_plassere] > 0) vise_VERDI_487749b8(sjekk_plassere);
        vise_VERDI_487749b8(던진객체);
        for (int Loop_INDEKS = 0; Loop_INDEKS < 잠시수; Loop_INDEKS++) vise_VERDI_487749b8(잠시참조[Loop_INDEKS]);
        while (vise_ANTALL > 0) {
            int objekt_referere = 표시대기[--vise_ANTALL], område_KODE = heap_VERDI[objekt_referere];
            for (int Loop_INDEKS = objekt_referere + 2; Loop_INDEKS < objekt_referere + 힙폭[objekt_referere]; Loop_INDEKS++) if (område_KODE == 3 || område_KODE == 4 || heap_referere[Loop_INDEKS] != 0) vise_VERDI_487749b8(heap_VERDI[Loop_INDEKS]);
        }
        for (int sjekk_plassere = 1; sjekk_plassere < heap_avslutte_en_samtale_plassere; sjekk_plassere += 힙폭[sjekk_plassere]) if (힙표시[sjekk_plassere] == 0) heap_VERDI[sjekk_plassere] = 0;
        for (int sjekk_plassere = 1; sjekk_plassere < heap_avslutte_en_samtale_plassere; sjekk_plassere += 힙폭[sjekk_plassere]) if (heap_VERDI[sjekk_plassere] == 0) {
            while (sjekk_plassere + 힙폭[sjekk_plassere] < heap_avslutte_en_samtale_plassere && heap_VERDI[sjekk_plassere + 힙폭[sjekk_plassere]] == 0) { int Neste_plassere = sjekk_plassere + 힙폭[sjekk_plassere]; 힙폭[sjekk_plassere] += 힙폭[Neste_plassere]; 힙폭[Neste_plassere] = 0; }
            if (sjekk_plassere + 힙폭[sjekk_plassere] == heap_avslutte_en_samtale_plassere) { heap_avslutte_en_samtale_plassere = sjekk_plassere; break; }
        }
    }
    static int 새기억(int 종류, int lengde_VERDI) {
        if (lengde_VERDI < 0) { feil_VERDI("NegativeArraySizeException"); return 0; }
        if (lengde_VERDI > heap_VERDI.length - 3) { feil_VERDI("object heap exhausted"); return 0; }
        int 필요수 = lengde_VERDI + 2, objekt_referere = 0;
        if (필요수 <= heap_VERDI.length - heap_avslutte_en_samtale_plassere) { objekt_referere = heap_avslutte_en_samtale_plassere; heap_avslutte_en_samtale_plassere += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < heap_avslutte_en_samtale_plassere; 읽는자리 += 힙폭[읽는자리]) if (heap_VERDI[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { objekt_referere = 읽는자리; break; }
            if (objekt_referere != 0) {
                int 남은길이 = 힙폭[objekt_referere] - 필요수;
                if (남은길이 >= 2) { 힙폭[objekt_referere + 필요수] = 남은길이; heap_VERDI[objekt_referere + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= heap_VERDI.length - heap_avslutte_en_samtale_plassere) { objekt_referere = heap_avslutte_en_samtale_plassere; heap_avslutte_en_samtale_plassere += 필요수; }
        }
        if (objekt_referere == 0) { feil_VERDI("object heap exhausted"); return 0; }
        for (int Loop_INDEKS = 0; Loop_INDEKS < 필요수; Loop_INDEKS++) { heap_VERDI[objekt_referere + Loop_INDEKS] = 0; heap_referere[objekt_referere + Loop_INDEKS] = 0; 힙폭[objekt_referere + Loop_INDEKS] = 0; }
        matriseelement[objekt_referere] = 0;
        힙폭[objekt_referere] = 필요수; heap_VERDI[objekt_referere] = 종류; heap_VERDI[objekt_referere + 1] = lengde_VERDI; beskytte_VERDI(objekt_referere); return objekt_referere;
    }
    static int unntak_time(String navn_konstant) {
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
    static int unntak_konstant(int Navn) {
        for (int Loop_INDEKS = 1; Loop_INDEKS <= 41; Loop_INDEKS++) if (ord_SMS(Navn, unntak_navn(Loop_INDEKS))) return Loop_INDEKS;
        return 0;
    }
    static String unntak_navn(int konto_VERDI) {
        if (konto_VERDI == 40) return "java/lang/InterruptedException";
        if (konto_VERDI == 41) return "norsk/eget/대기중단예외";
        if (konto_VERDI == 39) return "java/net/SocketException";
        if (konto_VERDI == 20) return "norsk/eget/unntak";
        if (konto_VERDI == 21) return "norsk/eget/kjøring_unntak";
        if (konto_VERDI == 22) return "norsk/eget/I_U_unntak";
        if (konto_VERDI == 23) return "norsk/eget/vent_TIMEOUT_unntak";
        if (konto_VERDI == 24) return "norsk/eget/e_post_Oppslag_unntak";
        if (konto_VERDI == 25) return "norsk/eget/파일없음예외";
        if (konto_VERDI == 26) return "norsk/eget/통신예외";
        if (konto_VERDI == 27) return "norsk/eget/ugyldig_argument_unntak";
        if (konto_VERDI == 28) return "norsk/eget/nummer_format_feil";
        if (konto_VERDI == 29) return "norsk/eget/범위예외";
        if (konto_VERDI == 30) return "norsk/eget/배열범위예외";
        if (konto_VERDI == 31) return "norsk/eget/문자열범위예외";
        if (konto_VERDI == 32) return "norsk/eget/NULL_referere_unntak";
        if (konto_VERDI == 33) return "norsk/eget/산술예외";
        if (konto_VERDI == 34) return "norsk/eget/status_unntak";
        if (konto_VERDI == 35) return "norsk/eget/Type_strømme_unntak";
        if (konto_VERDI == 36) return "norsk/eget/음수배열크기예외";
        if (konto_VERDI == 37) return "norsk/eget/MATRISE_Store_feil";
        if (konto_VERDI == 38) return "norsk/eget/tråd_status_unntak";
        if (konto_VERDI == 1) return "java/lang/Throwable"; if (konto_VERDI == 2) return "java/lang/Exception";
        if (konto_VERDI == 3) return "java/lang/RuntimeException"; if (konto_VERDI == 4) return "java/lang/ArithmeticException";
        if (konto_VERDI == 5) return "java/lang/NullPointerException"; if (konto_VERDI == 6) return "java/lang/IndexOutOfBoundsException";
        if (konto_VERDI == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (konto_VERDI == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (konto_VERDI == 9) return "java/lang/IllegalArgumentException"; if (konto_VERDI == 10) return "java/lang/NumberFormatException";
        if (konto_VERDI == 11) return "java/io/IOException"; if (konto_VERDI == 12) return "java/io/FileNotFoundException";
        if (konto_VERDI == 17) return "java/lang/ArrayStoreException";
        if (konto_VERDI == 18) return "java/net/UnknownHostException";
        if (konto_VERDI == 19) return "java/net/SocketTimeoutException";
        if (konto_VERDI == 16) return "java/lang/IllegalThreadStateException";
        if (konto_VERDI == 13) return "java/lang/IllegalStateException"; if (konto_VERDI == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int unntak_overordnet(int konto_VERDI) {
        if (konto_VERDI == 40) return 2;
        if (konto_VERDI == 41) return 40;
        if (konto_VERDI == 39) return 11;
        if (konto_VERDI == 1) return 0;
        if (konto_VERDI == 2) return 1;
        if (konto_VERDI == 3) return 2;
        if (konto_VERDI == 4) return 3;
        if (konto_VERDI == 5) return 3;
        if (konto_VERDI == 6) return 3;
        if (konto_VERDI == 7) return 6;
        if (konto_VERDI == 8) return 6;
        if (konto_VERDI == 9) return 3;
        if (konto_VERDI == 10) return 9;
        if (konto_VERDI == 11) return 2;
        if (konto_VERDI == 12) return 11;
        if (konto_VERDI == 13) return 3;
        if (konto_VERDI == 14) return 3;
        if (konto_VERDI == 15) return 3;
        if (konto_VERDI == 16) return 9;
        if (konto_VERDI == 17) return 3;
        if (konto_VERDI == 18) return 11;
        if (konto_VERDI == 19) return 11;
        if (konto_VERDI == 20) return 2;
        if (konto_VERDI == 21) return 3;
        if (konto_VERDI == 22) return 11;
        if (konto_VERDI == 23) return 22;
        if (konto_VERDI == 24) return 22;
        if (konto_VERDI == 25) return 22;
        if (konto_VERDI == 26) return 22;
        if (konto_VERDI == 27) return 9;
        if (konto_VERDI == 28) return 27;
        if (konto_VERDI == 29) return 6;
        if (konto_VERDI == 30) return 29;
        if (konto_VERDI == 31) return 29;
        if (konto_VERDI == 32) return 5;
        if (konto_VERDI == 33) return 4;
        if (konto_VERDI == 34) return 13;
        if (konto_VERDI == 35) return 14;
        if (konto_VERDI == 36) return 15;
        if (konto_VERDI == 37) return 17;
        if (konto_VERDI == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int faktisk_verdi, int 요구값) {
        for (int 깊이 = 0; faktisk_verdi != 0 && 깊이 < 16; 깊이++, faktisk_verdi = unntak_overordnet(faktisk_verdi))
            if (faktisk_verdi == 요구값) return true;
        return false;
    }
    static void 예외던짐(int konto_VERDI, String Viktig_fil_referere) {
        int objekt_referere = 새기억(9, 2); if (feil) return;
        heap_VERDI[objekt_referere + 2] = konto_VERDI; heap_VERDI[objekt_referere + 3] = vert_tegn(Viktig_fil_referere); heap_referere[objekt_referere + 3] = 1;
        던진객체 = objekt_referere; feil = true;
    }
    static boolean avstemming_objekt(int objekt_referere, int Navn) {
        if (objekt_referere == 0) return true;
        if (!informasjonssystemer_gyldig_objekt(objekt_referere)) return false;
        int område_KODE = heap_VERDI[objekt_referere];
        if (ord_SMS(Navn, "java/lang/Object")) return true;
        if (område_KODE >= 32) return 종포함(område_KODE - 32, Navn);
        if (område_KODE == 9) { int mål_e_post = unntak_konstant(Navn); return mål_e_post != 0 && 예외포함(heap_VERDI[objekt_referere + 2], mål_e_post); }
        if (område_KODE == 1) return ord_SMS(Navn, "java/lang/String") || ord_SMS(Navn, "java/lang/CharSequence");
        if (område_KODE == 4) return ord_SMS(Navn, "java/lang/StringBuilder") || ord_SMS(Navn, "java/lang/CharSequence");
        if (område_KODE == 10) return ord_SMS(Navn, "java/util/ArrayList") || ord_SMS(Navn, "java/util/List");
        if (område_KODE == 11) return ord_SMS(Navn, "java/util/HashMap") || ord_SMS(Navn, "java/util/Map");
        if (område_KODE == 12) return ord_SMS(Navn, "java/lang/Integer") || ord_SMS(Navn, "java/lang/Number");
        if (område_KODE >= 24 && område_KODE <= 28 && heap_VERDI[objekt_referere + 13] != 0) return 한국어화면종(Navn) == område_KODE || ord_SMS(Navn, "norsk/eget/skjermbilde_element");
        if (område_KODE >= 24 && område_KODE <= 28) return (한국어화면종(Navn) == 0 && skjermbilde_time(Navn) == område_KODE) || ord_SMS(Navn, "java/awt/Component") || ord_SMS(Navn, "java/awt/Container") || ord_SMS(Navn, "javax/swing/JComponent");
        if (område_KODE == 29) return ord_SMS(Navn, heap_VERDI[objekt_referere + 3] != 0 ? "norsk/eget/Gjøremål_notice" : "java/awt/event/ActionEvent");
        if (område_KODE == 30) return ord_SMS(Navn, "java/awt/FlowLayout") || ord_SMS(Navn, "java/awt/LayoutManager");
        if (område_KODE == 17) return ord_SMS(Navn, "java/net/Socket");
        if (område_KODE == 18) return ord_SMS(Navn, "java/net/ServerSocket");
        if (område_KODE == 19) return ord_SMS(Navn, heap_VERDI[objekt_referere + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (område_KODE == 14) return ord_SMS(Navn, "java/net/InetAddress");
        if (område_KODE == 15) return ord_SMS(Navn, "java/net/DatagramSocket");
        if (område_KODE == 16) return ord_SMS(Navn, "java/net/DatagramPacket");
        if (område_KODE == 13) return ord_SMS(Navn, heap_VERDI[objekt_referere + 3] != 0 ? "norsk/eget/arbeider" : "java/lang/Thread");
        if (område_KODE == 2) return ord_SMS(Navn, "[I"); if (område_KODE == 20) return ord_SMS(Navn, "[B"); if (område_KODE == 21) return ord_SMS(Navn, "[Z");
        if (område_KODE == 22) return ord_SMS(Navn, "[C"); if (område_KODE == 23) return ord_SMS(Navn, "[S");
        if (område_KODE != 3) return false;
        if (ord_SMS(Navn, "[Ljava/lang/Object;")) return true;
        int komponent = matriseelement[objekt_referere];
        if (komponent == -1) return ord_SMS(Navn, "[Ljava/lang/String;") || ord_SMS(Navn, "[Ljava/lang/CharSequence;");
        if (komponent == 0) return false;
        if (배열종비교(komponent, Navn)) return true;
        if ((ord_SMS(komponent, "java/lang/String") || ord_SMS(komponent, "java/lang/StringBuilder")) && ord_SMS(Navn, "[Ljava/lang/CharSequence;")) return true;
        for (int Loop_INDEKS = 0; Loop_INDEKS < time_Definisjon_ANTALL; Loop_INDEKS++) if (avstemming_ord(time_Definisjon_navn[Loop_INDEKS], komponent)) {
            for (int tegnkode = Loop_INDEKS, 중첩깊이 = 0; tegnkode >= 0 && 중첩깊이 < 16; 중첩깊이++, tegnkode = overordnet_time(tegnkode)) {
                if (배열종비교(time_Definisjon_overordnet[tegnkode], Navn)) return true;
                for (int indre_kobling_plassere = 0; indre_kobling_plassere < time_grensesnitt_ANTALL[tegnkode]; indre_kobling_plassere++) if (배열종비교(time_grensesnitt[tegnkode * 16 + indre_kobling_plassere], Navn)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int navn_konstant, int 형식참조) {
        int sjekk_plassere = 상가[형식참조], oppføring_ANTALL = konstant_SEKUND_VERDI[형식참조];
        if (navn_konstant == 0 || oppføring_ANTALL < 4 || Fil[sjekk_plassere] != '[' || Fil[sjekk_plassere + 1] != 'L' || Fil[sjekk_plassere + oppføring_ANTALL - 1] != ';' || konstant_SEKUND_VERDI[navn_konstant] != oppføring_ANTALL - 3) return false;
        for (int Loop_INDEKS = 0; Loop_INDEKS < oppføring_ANTALL - 3; Loop_INDEKS++) if (Fil[상가[navn_konstant] + Loop_INDEKS] != Fil[sjekk_plassere + 2 + Loop_INDEKS]) return false;
        return true;
    }
    static void håndtak_unntak() {
        if (던진객체 == 0) return;
        feil = false;
        while (bilde_INDEKS >= betalt_tråd * 32) {
            int Fil_INDEKS = bilde_metode[bilde_INDEKS], 읽는자리 = 틀명령[bilde_INDEKS];
            for (int Loop_INDEKS = 0; Loop_INDEKS < 잡기수; Loop_INDEKS++) if (잡기함수[Loop_INDEKS] == Fil_INDEKS && 읽는자리 >= 잡기시작[Loop_INDEKS] && 읽는자리 < 잡기끝[Loop_INDEKS]
                && (잡기종[Loop_INDEKS] == 0 || avstemming_objekt(던진객체, 잡기종[Loop_INDEKS]))) {
                bilde_plassere[bilde_INDEKS] = 잡기위치[Loop_INDEKS]; bilde_stakk[bilde_INDEKS] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (starte_bilde[bilde_INDEKS] != 0) time_Definisjon_status[starte_bilde[bilde_INDEKS] - 1] = 3;
            if (bilde_blokkere[bilde_INDEKS] != 0) { frigi_blokkere(bilde_blokkere[bilde_INDEKS]); bilde_blokkere[bilde_INDEKS] = 0; }
            bilde_INDEKS--;
        }
        bruker.Skriv("Uncaught ");
        if (heap_VERDI[던진객체] == 9) { bruker.Skriv(unntak_navn(heap_VERDI[던진객체 + 2])); bruker.Skriv(": "); skrive_SMS(heap_VERDI[던진객체 + 3]); }
        else bruker.Skriv("user exception");
        bruker.skrive_tegn_VERDI(10); 던진객체 = 0; feil = true;
    }
    // 이 JVM의 operand_stakk 항목은 betalt_vare category-1(int/reference)만 허용한다.
    static void 스택명령(int kommando_KODE) {
        int 첫값 = 빼기(0), 첫형식 = return_Type;
        if (kommando_KODE == 87) return;
        if (kommando_KODE == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int byte_data = 빼기(0), SEKUND_format = return_Type;
        if (kommando_KODE == 88) return;
        if (kommando_KODE == 90) { 넣기(첫값, 첫형식); 넣기(byte_data, SEKUND_format); 넣기(첫값, 첫형식); return; }
        if (kommando_KODE == 92) { 넣기(byte_data, SEKUND_format); 넣기(첫값, 첫형식); 넣기(byte_data, SEKUND_format); 넣기(첫값, 첫형식); return; }
        if (kommando_KODE == 95) { 넣기(첫값, 첫형식); 넣기(byte_data, SEKUND_format); return; }
        int tegnkode = 빼기(0), 셋째형식 = return_Type;
        if (kommando_KODE == 91) { 넣기(첫값, 첫형식); 넣기(tegnkode, 셋째형식); 넣기(byte_data, SEKUND_format); 넣기(첫값, 첫형식); return; }
        if (kommando_KODE == 93) { 넣기(byte_data, SEKUND_format); 넣기(첫값, 첫형식); 넣기(tegnkode, 셋째형식); 넣기(byte_data, SEKUND_format); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = return_Type;
        넣기(byte_data, SEKUND_format); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(tegnkode, 셋째형식); 넣기(byte_data, SEKUND_format); 넣기(첫값, 첫형식);
    }
    static void 새객체(int navn_konstant, int 시작점) {
        int område_KODE = 0, gyldig_lengde = 0, unntak_referere = unntak_konstant(navn_konstant);
        if (ord_SMS(navn_konstant, "java/lang/StringBuilder")) { område_KODE = 4; gyldig_lengde = 1; }
        if (ord_SMS(navn_konstant, "java/io/FileInputStream")) { område_KODE = 5; gyldig_lengde = 2; }
        if (ord_SMS(navn_konstant, "java/io/FileOutputStream")) { område_KODE = 6; gyldig_lengde = 2; }
        if (unntak_referere != 0) { område_KODE = 9; gyldig_lengde = 2; }
        if (ord_SMS(navn_konstant, "java/util/ArrayList")) { område_KODE = 10; gyldig_lengde = 2; }
        if (ord_SMS(navn_konstant, "java/util/HashMap")) { område_KODE = 11; gyldig_lengde = 2; }
        if (ord_SMS(navn_konstant, "java/lang/Integer")) { område_KODE = 12; gyldig_lengde = 1; }
        if (ord_SMS(navn_konstant, "java/net/Socket")) { område_KODE = 17; gyldig_lengde = 5; }
        if (ord_SMS(navn_konstant, "java/net/ServerSocket")) { område_KODE = 18; gyldig_lengde = 5; }
        if (ord_SMS(navn_konstant, "java/net/DatagramSocket")) { område_KODE = 15; gyldig_lengde = 3; }
        if (ord_SMS(navn_konstant, "java/net/DatagramPacket")) { område_KODE = 16; gyldig_lengde = 4; }
        if (ord_SMS(navn_konstant, "java/lang/Thread") || ord_SMS(navn_konstant, "norsk/eget/arbeider")) { område_KODE = 13; gyldig_lengde = 2; }
        if (ord_SMS(navn_konstant, "java/lang/Object")) { område_KODE = 8; }
        if (område_KODE == 0 && skjermbilde_time(navn_konstant) != 0) { område_KODE = skjermbilde_time(navn_konstant); gyldig_lengde = 12; }
        if (område_KODE == 0) {
            int tegnkode = Søk_time_Definisjon(navn_konstant); if (tegnkode < 0 || feil || !starte(tegnkode, 시작점)) return;
            område_KODE = 32 + tegnkode; gyldig_lengde = time_åpning_ANTALL[tegnkode];
        }
        int objekt_referere = tildele_lager(område_KODE, gyldig_lengde); if (feil) return;
        if (område_KODE == 13 && ord_SMS(navn_konstant, "norsk/eget/arbeider")) heap_VERDI[objekt_referere + 3] = 1;
        if (område_KODE >= 24 && område_KODE <= 28 && 한국어화면종(navn_konstant) != 0) heap_VERDI[objekt_referere + 13] = 1;
        if (område_KODE == 5 || område_KODE == 6 || område_KODE == 15 || område_KODE == 17 || område_KODE == 18) heap_VERDI[objekt_referere + 2] = -1;
        if (område_KODE == 9) heap_VERDI[objekt_referere + 2] = unntak_referere;
        넣기(objekt_referere, 2);
    }
    static boolean 값같음(int 첫값, int byte_data) {
        if (첫값 == byte_data) return true;
        if (첫값 == 0 || byte_data == 0 || 첫값 < 0 || byte_data < 0 || 첫값 >= heap_avslutte_en_samtale_plassere || byte_data >= heap_avslutte_en_samtale_plassere) return false;
        if (heap_VERDI[첫값] == 1 && heap_VERDI[byte_data] == 1) return 글같음(첫값, byte_data, false);
        return heap_VERDI[첫값] == 12 && heap_VERDI[byte_data] == 12 && heap_VERDI[첫값 + 2] == heap_VERDI[byte_data + 2];
    }
    static int 글조각(int objekt_referere, int START_plassere, int avslutte_en_samtale_plassere) {
        if (!objekt_VERDI(objekt_referere, 1)) return 0;
        if (START_plassere < 0 || avslutte_en_samtale_plassere < START_plassere || avslutte_en_samtale_plassere > heap_VERDI[objekt_referere + 1]) { feil_VERDI("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = tildele_lager(1, avslutte_en_samtale_plassere - START_plassere); if (feil) return 0;
        for (int Loop_INDEKS = START_plassere; Loop_INDEKS < avslutte_en_samtale_plassere; Loop_INDEKS++) heap_VERDI[반환값 + 2 + Loop_INDEKS - START_plassere] = heap_VERDI[objekt_referere + 2 + Loop_INDEKS];
        return 반환값;
    }
    static int bli_med_SMS(int 첫값, int byte_data) {
        if (!objekt_VERDI(첫값, 1) || !objekt_VERDI(byte_data, 1)) return 0;
        int oppføring_ANTALL = heap_VERDI[첫값 + 1], metode_INDEKS = heap_VERDI[byte_data + 1], 반환값 = tildele_lager(1, oppføring_ANTALL + metode_INDEKS); if (feil) return 0;
        for (int Loop_INDEKS = 0; Loop_INDEKS < oppføring_ANTALL; Loop_INDEKS++) heap_VERDI[반환값 + 2 + Loop_INDEKS] = heap_VERDI[첫값 + 2 + Loop_INDEKS];
        for (int Loop_INDEKS = 0; Loop_INDEKS < metode_INDEKS; Loop_INDEKS++) heap_VERDI[반환값 + 2 + oppføring_ANTALL + Loop_INDEKS] = heap_VERDI[byte_data + 2 + Loop_INDEKS];
        return 반환값;
    }
    static boolean 기본호출(int eier, int navn_konstant, int 서술상수, int kommando_KODE) {
        if (ord_SMS(eier, "norsk/eget/실행인수") && kommando_KODE == 184) {
            if (ord_SMS(navn_konstant, "vare_ANTALL") && ord_SMS(서술상수, "()I")) { 넣기(bruker.인수개수() - 1, 1); return true; }
            if (ord_SMS(navn_konstant, "Tekst") && ord_SMS(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= bruker.인수개수() - 1) 예외던짐(29, "Utfør_kommando Argumenter 범위를 벗어났습니다");
                else 넣기(vert_tegn(bruker.Argumenter(순번 + 1)), 2);
                return true;
            }
            feil_VERDI("지원하지 않는 norsk Utfør_kommando Argumenter 호출"); return true;
        }
        if (ord_SMS(eier, "norsk/eget/arbeider")) { Prosess_tråd(navn_konstant, 서술상수, kommando_KODE, true); return true; }
        if (한국어화면소유(eier)) { 한국어화면호출(eier, navn_konstant, 서술상수, kommando_KODE); return true; }
        if (skjermbilde_eier(eier)) { 화면호출(eier, navn_konstant, 서술상수, kommando_KODE); return true; }
        if (ord_SMS(eier, "java/net/Socket") || ord_SMS(eier, "java/net/ServerSocket") || ord_SMS(eier, "java/io/InputStream") || ord_SMS(eier, "java/io/OutputStream")) { 흐름호출(eier, navn_konstant, 서술상수, kommando_KODE); return true; }
        if (ord_SMS(eier, "norsk/eget/kjerne_VERDI") && kommando_KODE == 184) {
            if (ord_SMS(navn_konstant, "화면너비") && ord_SMS(서술상수, "()I")) { 넣기(bruker.화면너비(), 1); return true; }
            if (ord_SMS(navn_konstant, "화면높이") && ord_SMS(서술상수, "()I")) { 넣기(bruker.화면높이(), 1); return true; }
            if (ord_SMS(navn_konstant, "밀리초") && ord_SMS(서술상수, "()I")) { 넣기(bruker.밀리초(), 1); return true; }
            if (ord_SMS(navn_konstant, "그림대기") && ord_SMS(서술상수, "()I")) { 넣기(bruker.그림대기(), 1); return true; }
            if (ord_SMS(navn_konstant, "rektangel") && ord_SMS(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), Y_koordinat = 빼기(1), x_koordinat = 빼기(1); 넣기(bruker.rektangel(x_koordinat, Y_koordinat, 너비, 높이, 색상), 1); return true; }
        }
        if (ord_SMS(eier, "java/net/InetAddress") || ord_SMS(eier, "java/net/DatagramPacket") || ord_SMS(eier, "java/net/DatagramSocket")) { 통신호출(eier, navn_konstant, 서술상수, kommando_KODE); return true; }
        if (ord_SMS(eier, "java/lang/Thread")) { 가닥호출(navn_konstant, 서술상수, kommando_KODE); return true; }
        if (ord_SMS(eier, "java/lang/Object")) {
            if (ord_SMS(navn_konstant, "<init>") && ord_SMS(서술상수, "()V") && kommando_KODE == 183) { informasjonssystemer_gyldig_objekt(빼기(2)); return true; }
            if (ord_SMS(navn_konstant, "equals") && ord_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int byte_data = 빼기(2), 첫값 = 빼기(2); if (informasjonssystemer_gyldig_objekt(첫값)) 넣기(첫값 == byte_data ? 1 : 0, 1); return true; }
        }
        if (unntak_konstant(eier) != 0) {
            if (ord_SMS(navn_konstant, "<init>") && kommando_KODE == 183 && (ord_SMS(서술상수, "()V") || ord_SMS(서술상수, "(Ljava/lang/String;)V"))) {
                int be_om = ord_SMS(서술상수, "()V") ? 0 : 빼기(2), objekt_referere = 빼기(2);
                if (objekt_VERDI(objekt_referere, 9)) { heap_VERDI[objekt_referere + 3] = be_om; heap_referere[objekt_referere + 3] = 1; } return true;
            }
            if ((ord_SMS(navn_konstant, "getMessage") || ord_SMS(navn_konstant, "설명")) && ord_SMS(서술상수, "()Ljava/lang/String;")) { int objekt_referere = 빼기(2); if (objekt_VERDI(objekt_referere, 9)) 넣기(heap_VERDI[objekt_referere + 3], 2); return true; }
        }
        if (ord_SMS(eier, "java/lang/String")) {
            if (kommando_KODE == 182 && ord_SMS(navn_konstant, "getBytes") && (ord_SMS(서술상수, "()[B") || ord_SMS(서술상수, "(Ljava/lang/String;)[B"))) {
                int koding_navn = ord_SMS(서술상수, "()[B") ? 0 : 빼기(2), objekt_referere = 빼기(2);
                if (!objekt_VERDI(objekt_referere, 1)) return true;
                if (koding_navn != 0 && !글같음(koding_navn, vert_tegn("UTF-8"), false) && !글같음(koding_navn, vert_tegn("UTF8"), false) && !글같음(koding_navn, vert_tegn("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int oppføring_ANTALL = heap_VERDI[objekt_referere + 1], 반환값 = tildele_lager(20, oppføring_ANTALL * 3), 사용수 = 0; if (feil) return true;
                for (int indre_kobling_plassere = 0; indre_kobling_plassere < oppføring_ANTALL; indre_kobling_plassere++) {
                    int tegnkode = heap_VERDI[objekt_referere + 2 + indre_kobling_plassere];
                    if (tegnkode >= 0xd800 && tegnkode <= 0xdbff && indre_kobling_plassere + 1 < oppføring_ANTALL && heap_VERDI[objekt_referere + 3 + indre_kobling_plassere] >= 0xdc00 && heap_VERDI[objekt_referere + 3 + indre_kobling_plassere] <= 0xdfff) tegnkode = 0x10000 + ((tegnkode - 0xd800) << 10) + heap_VERDI[objekt_referere + 2 + ++indre_kobling_plassere] - 0xdc00;
                    else if (tegnkode >= 0xd800 && tegnkode <= 0xdfff) tegnkode = '?';
                    if (tegnkode < 128) heap_VERDI[반환값 + 2 + 사용수++] = tegnkode;
                    else { int byte_ANTALL = tegnkode < 2048 ? 2 : tegnkode < 65536 ? 3 : 4; heap_VERDI[반환값 + 2 + 사용수++] = (byte)((byte_ANTALL == 2 ? 192 : byte_ANTALL == 3 ? 224 : 240) | tegnkode >> (6 * (byte_ANTALL - 1))); for (int Sammenligning_plassere = byte_ANTALL - 1; Sammenligning_plassere > 0; Sammenligning_plassere--) heap_VERDI[반환값 + 2 + 사용수++] = (byte)(128 | tegnkode >> (6 * (Sammenligning_plassere - 1)) & 63); }
                }
                heap_VERDI[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (kommando_KODE == 184 && ord_SMS(navn_konstant, "valueOf") && ord_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(siffer_tegn(빼기(1)), 2); return true; }
            if (kommando_KODE != 182) return false;
            if (ord_SMS(navn_konstant, "equals") && ord_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int byte_data = 빼기(2), 첫값 = 빼기(2); if (objekt_VERDI(첫값, 1)) 넣기(글같음(첫값, byte_data, false) ? 1 : 0, 1); return true; }
            if (ord_SMS(navn_konstant, "isEmpty") && ord_SMS(서술상수, "()Z")) { int 첫값 = 빼기(2); if (objekt_VERDI(첫값, 1)) 넣기(heap_VERDI[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (ord_SMS(navn_konstant, "substring") && (ord_SMS(서술상수, "(I)Ljava/lang/String;") || ord_SMS(서술상수, "(II)Ljava/lang/String;"))) {
                boolean SEKUND_VERDI = ord_SMS(서술상수, "(II)Ljava/lang/String;"); int avslutte_en_samtale_plassere = SEKUND_VERDI ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (objekt_VERDI(첫값, 1)) 넣기(글조각(첫값, 시작점, SEKUND_VERDI ? avslutte_en_samtale_plassere : heap_VERDI[첫값 + 1]), 2); return true;
            }
            if (ord_SMS(navn_konstant, "concat") && ord_SMS(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int byte_data = 빼기(2), 첫값 = 빼기(2); 넣기(bli_med_SMS(첫값, byte_data), 2); return true; }
            if (ord_SMS(navn_konstant, "hashCode") && ord_SMS(서술상수, "()I")) { int 첫값 = 빼기(2), hash_VERDI = 0; if (objekt_VERDI(첫값, 1)) { for (int Loop_INDEKS = 0; Loop_INDEKS < heap_VERDI[첫값 + 1]; Loop_INDEKS++) hash_VERDI = hash_VERDI * 31 + heap_VERDI[첫값 + 2 + Loop_INDEKS]; 넣기(hash_VERDI, 1); } return true; }
            if (ord_SMS(navn_konstant, "toString") && ord_SMS(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (objekt_VERDI(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (ord_SMS(eier, "java/lang/Integer")) {
            if (kommando_KODE == 184 && ord_SMS(navn_konstant, "valueOf") && ord_SMS(서술상수, "(I)Ljava/lang/Integer;")) { int data_VERDI = 빼기(1), objekt_referere = data_VERDI >= -128 && data_VERDI <= 127 ? Store_heltall[data_VERDI + 128] : 0; if (objekt_referere == 0) { objekt_referere = tildele_lager(12, 1); if (!feil) { heap_VERDI[objekt_referere + 2] = data_VERDI; if (data_VERDI >= -128 && data_VERDI <= 127) Store_heltall[data_VERDI + 128] = objekt_referere; } } 넣기(objekt_referere, 2); return true; }
            if (kommando_KODE == 183 && ord_SMS(navn_konstant, "<init>") && ord_SMS(서술상수, "(I)V")) { int data_VERDI = 빼기(1), objekt_referere = 빼기(2); if (objekt_VERDI(objekt_referere, 12)) heap_VERDI[objekt_referere + 2] = data_VERDI; return true; }
            if (kommando_KODE == 182 && ord_SMS(navn_konstant, "intValue") && ord_SMS(서술상수, "()I")) { int objekt_referere = 빼기(2); if (objekt_VERDI(objekt_referere, 12)) 넣기(heap_VERDI[objekt_referere + 2], 1); return true; }
            if (kommando_KODE == 184 && ord_SMS(navn_konstant, "toString") && ord_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(siffer_tegn(빼기(1)), 2); return true; }
        }
        if (ord_SMS(eier, "java/lang/Math") && kommando_KODE == 184) {
            if (ord_SMS(navn_konstant, "abs") && ord_SMS(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((ord_SMS(navn_konstant, "min") || ord_SMS(navn_konstant, "max")) && ord_SMS(서술상수, "(II)I")) { int byte_data = 빼기(1), 첫값 = 빼기(1); 넣기(ord_SMS(navn_konstant, "min") ? (첫값 < byte_data ? 첫값 : byte_data) : (첫값 > byte_data ? 첫값 : byte_data), 1); return true; }
        }
        if (ord_SMS(eier, "java/lang/System") && kommando_KODE == 184) {
            if (ord_SMS(navn_konstant, "gc") && ord_SMS(서술상수, "()V")) { 수거(); return true; }
            if (ord_SMS(navn_konstant, "arraycopy") && ord_SMS(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int oppføring_ANTALL = 빼기(1), mål_VERDI_INDEKS = 빼기(1), byte_data = 빼기(2), START_plassere = 빼기(1), 첫값 = 빼기(2);
                if (informasjonssystemer_gyldig_objekt(첫값) && informasjonssystemer_gyldig_objekt(byte_data)) {
                    int område_KODE = heap_VERDI[첫값];
                    if (heap_VERDI[byte_data] != område_KODE || (område_KODE != 2 && område_KODE != 3 && (område_KODE < 20 || område_KODE > 23))) feil_VERDI("arraycopy type mismatch");
                    else if (oppføring_ANTALL < 0 || START_plassere < 0 || mål_VERDI_INDEKS < 0 || START_plassere > heap_VERDI[첫값 + 1] - oppføring_ANTALL || mål_VERDI_INDEKS > heap_VERDI[byte_data + 1] - oppføring_ANTALL) feil_VERDI("ArrayIndexOutOfBoundsException");
                    else if (첫값 == byte_data && mål_VERDI_INDEKS > START_plassere) { for (int Loop_INDEKS = oppføring_ANTALL - 1; Loop_INDEKS >= 0; Loop_INDEKS--) heap_VERDI[byte_data + 2 + mål_VERDI_INDEKS + Loop_INDEKS] = heap_VERDI[첫값 + 2 + START_plassere + Loop_INDEKS]; }
                    else { for (int Loop_INDEKS = 0; Loop_INDEKS < oppføring_ANTALL && !feil; Loop_INDEKS++) { int data_VERDI = heap_VERDI[첫값 + 2 + START_plassere + Loop_INDEKS]; if (område_KODE != 3 || 배열저장가능(byte_data, data_VERDI)) heap_VERDI[byte_data + 2 + mål_VERDI_INDEKS + Loop_INDEKS] = data_VERDI; } }
                }
                return true;
            }
        }
        if (ord_SMS(eier, "java/util/ArrayList") || ord_SMS(eier, "java/util/List") || ord_SMS(eier, "java/util/HashMap") || ord_SMS(eier, "java/util/Map")) {
            모음호출(eier, navn_konstant, 서술상수, kommando_KODE); return true;
        }
        return false;
    }
    static void 모음늘리기(int objekt_referere, int 필요수) {
        int Forrige_VERDI = heap_VERDI[objekt_referere + 2], kapasitet_data = Forrige_VERDI == 0 ? 0 : heap_VERDI[Forrige_VERDI + 1];
        if (kapasitet_data >= 필요수) return;
        int Neste_plassere = kapasitet_data < 8 ? 8 : kapasitet_data * 2; if (Neste_plassere < 필요수) Neste_plassere = 필요수;
        int data_MATRISE = tildele_lager(3, Neste_plassere); if (feil) return;
        for (int Loop_INDEKS = 0; Loop_INDEKS < kapasitet_data; Loop_INDEKS++) heap_VERDI[data_MATRISE + 2 + Loop_INDEKS] = heap_VERDI[Forrige_VERDI + 2 + Loop_INDEKS];
        heap_VERDI[objekt_referere + 2] = data_MATRISE; heap_referere[objekt_referere + 2] = 1;
    }
    static void 모음호출(int eier, int navn_konstant, int 서술상수, int kommando_KODE) {
        boolean 대응참조 = ord_SMS(eier, "java/util/HashMap") || ord_SMS(eier, "java/util/Map"); int område_KODE = 대응참조 ? 11 : 10;
        if (ord_SMS(navn_konstant, "<init>") && kommando_KODE == 183 && ord_SMS(서술상수, "()V")) { int objekt_referere = 빼기(2); if (objekt_VERDI(objekt_referere, område_KODE)) 모음늘리기(objekt_referere, 8); return; }
        if (kommando_KODE != 182 && kommando_KODE != 185) { feil_VERDI("invalid collection invocation"); return; }
        if (ord_SMS(navn_konstant, "size") && ord_SMS(서술상수, "()I") || ord_SMS(navn_konstant, "isEmpty") && ord_SMS(서술상수, "()Z")) {
            int objekt_referere = 빼기(2); if (objekt_VERDI(objekt_referere, område_KODE)) 넣기(ord_SMS(navn_konstant, "size") ? heap_VERDI[objekt_referere + 3] : heap_VERDI[objekt_referere + 3] == 0 ? 1 : 0, 1); return;
        }
        if (ord_SMS(navn_konstant, "clear") && ord_SMS(서술상수, "()V")) { int objekt_referere = 빼기(2); if (objekt_VERDI(objekt_referere, område_KODE)) { int data_MATRISE = heap_VERDI[objekt_referere + 2]; for (int Loop_INDEKS = 0; Loop_INDEKS < heap_VERDI[data_MATRISE + 1]; Loop_INDEKS++) heap_VERDI[data_MATRISE + 2 + Loop_INDEKS] = 0; heap_VERDI[objekt_referere + 3] = 0; } return; }
        if (!대응참조 && ord_SMS(navn_konstant, "add") && ord_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            int data_VERDI = 빼기(2), objekt_referere = 빼기(2); if (!objekt_VERDI(objekt_referere, 10)) return;
            int oppføring_ANTALL = heap_VERDI[objekt_referere + 3]; 모음늘리기(objekt_referere, oppføring_ANTALL + 1); if (!feil) { heap_VERDI[heap_VERDI[objekt_referere + 2] + 2 + oppføring_ANTALL] = data_VERDI; heap_VERDI[objekt_referere + 3] = oppføring_ANTALL + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (ord_SMS(navn_konstant, "get") || ord_SMS(navn_konstant, "remove")) && ord_SMS(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && ord_SMS(navn_konstant, "set") && ord_SMS(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean informasjonssystemer_Tilordnet = ord_SMS(navn_konstant, "set"); int data_VERDI = informasjonssystemer_Tilordnet ? 빼기(2) : 0, oppføring_plassere = 빼기(1), objekt_referere = 빼기(2);
            if (!objekt_VERDI(objekt_referere, 10)) return;
            int oppføring_ANTALL = heap_VERDI[objekt_referere + 3], data_MATRISE = heap_VERDI[objekt_referere + 2];
            if (oppføring_plassere < 0 || oppføring_plassere >= oppføring_ANTALL) { 예외던짐(6, "list index"); return; }
            int Forrige_VERDI = heap_VERDI[data_MATRISE + 2 + oppføring_plassere];
            if (informasjonssystemer_Tilordnet) heap_VERDI[data_MATRISE + 2 + oppføring_plassere] = data_VERDI;
            if (ord_SMS(navn_konstant, "remove")) { for (int Loop_INDEKS = oppføring_plassere + 1; Loop_INDEKS < oppføring_ANTALL; Loop_INDEKS++) heap_VERDI[data_MATRISE + 1 + Loop_INDEKS] = heap_VERDI[data_MATRISE + 2 + Loop_INDEKS]; heap_VERDI[data_MATRISE + 1 + oppføring_ANTALL] = 0; heap_VERDI[objekt_referere + 3] = oppføring_ANTALL - 1; }
            넣기(Forrige_VERDI, 2); return;
        }
        if (대응참조 && (ord_SMS(navn_konstant, "get") || ord_SMS(navn_konstant, "remove")) && ord_SMS(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && ord_SMS(navn_konstant, "put") && ord_SMS(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && ord_SMS(navn_konstant, "containsKey") && ord_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = ord_SMS(navn_konstant, "put"), fjerne = ord_SMS(navn_konstant, "remove");
            int data_VERDI = 넣기여부 ? 빼기(2) : 0, tast_referere = 빼기(2), objekt_referere = 빼기(2); if (!objekt_VERDI(objekt_referere, 11)) return;
            int oppføring_ANTALL = heap_VERDI[objekt_referere + 3], data_MATRISE = heap_VERDI[objekt_referere + 2], 찾은여부 = -1;
            for (int Loop_INDEKS = 0; Loop_INDEKS < oppføring_ANTALL; Loop_INDEKS++) if (값같음(tast_referere, heap_VERDI[data_MATRISE + 2 + 2 * Loop_INDEKS])) { 찾은여부 = Loop_INDEKS; break; }
            int Forrige_VERDI = 찾은여부 < 0 ? 0 : heap_VERDI[data_MATRISE + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(objekt_referere, (oppføring_ANTALL + 1) * 2); data_MATRISE = heap_VERDI[objekt_referere + 2]; 찾은여부 = oppføring_ANTALL; if (!feil) heap_VERDI[objekt_referere + 3] = oppføring_ANTALL + 1; }
                if (!feil) { heap_VERDI[data_MATRISE + 2 + 2 * 찾은여부] = tast_referere; heap_VERDI[data_MATRISE + 3 + 2 * 찾은여부] = data_VERDI; }
            }
            if (fjerne && 찾은여부 >= 0) { for (int Loop_INDEKS = 찾은여부 + 1; Loop_INDEKS < oppføring_ANTALL; Loop_INDEKS++) { heap_VERDI[data_MATRISE + 2 * Loop_INDEKS] = heap_VERDI[data_MATRISE + 2 + 2 * Loop_INDEKS]; heap_VERDI[data_MATRISE + 1 + 2 * Loop_INDEKS] = heap_VERDI[data_MATRISE + 3 + 2 * Loop_INDEKS]; } heap_VERDI[data_MATRISE + 2 * oppføring_ANTALL] = 0; heap_VERDI[data_MATRISE + 1 + 2 * oppføring_ANTALL] = 0; heap_VERDI[objekt_referere + 3] = oppføring_ANTALL - 1; }
            if (ord_SMS(navn_konstant, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(Forrige_VERDI, 2);
            return;
        }
        feil_VERDI("unsupported collection method");
    }
    static boolean 잠금얻기(int objekt_referere) {
        if (!informasjonssystemer_gyldig_objekt(objekt_referere)) return false;
        if (잠금깊이[objekt_referere] != 0 && blokkere_eier[objekt_referere] != betalt_tråd + 1) { endringsforespørsel = true; return false; }
        blokkere_eier[objekt_referere] = betalt_tråd + 1; 잠금깊이[objekt_referere]++; return true;
    }
    static void frigi_blokkere(int objekt_referere) {
        if (!informasjonssystemer_gyldig_objekt(objekt_referere)) return;
        if (잠금깊이[objekt_referere] == 0 || blokkere_eier[objekt_referere] != betalt_tråd + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[objekt_referere] == 0) blokkere_eier[objekt_referere] = 0;
    }
    static boolean bytt_tråd() {
        tråd_bilde[betalt_tråd] = bilde_INDEKS;
        if (bilde_INDEKS < betalt_tråd * 32) tråd_status[betalt_tråd] = 3;
        for (int Loop_INDEKS = 0; Loop_INDEKS < Trådteller; Loop_INDEKS++) if (tråd_status[Loop_INDEKS] == 2 && tråd_status[가닥대기[Loop_INDEKS]] == 3) tråd_status[Loop_INDEKS] = 1;
        for (int Loop_INDEKS = 1; Loop_INDEKS <= Trådteller; Loop_INDEKS++) {
            int Neste_plassere = (betalt_tråd + Loop_INDEKS) % Trådteller;
            if (tråd_status[Neste_plassere] == 1) { betalt_tråd = Neste_plassere; bilde_INDEKS = tråd_bilde[Neste_plassere]; endringsforespørsel = false; return true; }
        }
        for (int Loop_INDEKS = 0; Loop_INDEKS < Trådteller; Loop_INDEKS++) if (tråd_status[Loop_INDEKS] != 3) { feil_VERDI("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int navn_konstant, int 서술상수, int kommando_KODE) { Prosess_tråd(navn_konstant, 서술상수, kommando_KODE, false); }
    static void Prosess_tråd(int navn_konstant, int 서술상수, int kommando_KODE, boolean norsk) {
        if (kommando_KODE == 184 && ord_SMS(navn_konstant, norsk ? "AVKAST_oppgave" : "yield") && ord_SMS(서술상수, "()V")) { endringsforespørsel = true; return; }
        if (kommando_KODE == 184 && ord_SMS(navn_konstant, "currentThread") && ord_SMS(서술상수, "()Ljava/lang/Thread;")) { 넣기(tråd_objekt[betalt_tråd], 2); return; }
        if (kommando_KODE == 183 && ord_SMS(navn_konstant, "<init>") && (ord_SMS(서술상수, "()V") || ord_SMS(서술상수, norsk ? "(Lnorsk/eget/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int mål_e_post = ord_SMS(서술상수, "()V") ? 0 : 빼기(2), objekt_referere = 빼기(2);
            if (!informasjonssystemer_gyldig_objekt(objekt_referere)) return;
            if (heap_VERDI[objekt_referere] == 13) { heap_VERDI[objekt_referere + 2] = mål_e_post; heap_referere[objekt_referere + 2] = 1; }
            else if (mål_e_post != 0) feil_VERDI("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (kommando_KODE == 182 && (ord_SMS(navn_konstant, norsk ? "START_oppgave" : "start") || ord_SMS(navn_konstant, norsk ? "기다리기" : "join")) && ord_SMS(서술상수, "()V") || kommando_KODE == 182 && ord_SMS(navn_konstant, norsk ? "살아있는가" : "isAlive") && ord_SMS(서술상수, "()Z")) {
            int objekt_referere = 빼기(2); if (!informasjonssystemer_gyldig_objekt(objekt_referere)) return;
            int konto_VERDI = -1; for (int Loop_INDEKS = 0; Loop_INDEKS < Trådteller; Loop_INDEKS++) if (tråd_objekt[Loop_INDEKS] == objekt_referere) konto_VERDI = Loop_INDEKS;
            if (ord_SMS(navn_konstant, norsk ? "살아있는가" : "isAlive")) { 넣기(konto_VERDI >= 0 && tråd_status[konto_VERDI] != 3 ? 1 : 0, 1); return; }
            if (ord_SMS(navn_konstant, norsk ? "기다리기" : "join")) { if (konto_VERDI >= 0 && tråd_status[konto_VERDI] != 3) { 가닥대기[betalt_tråd] = konto_VERDI; tråd_status[betalt_tråd] = 2; endringsforespørsel = true; } return; }
            if (konto_VERDI >= 0) { 예외던짐(norsk ? 38 : 16, "thread already started"); return; }
            if (Trådteller == 4) { feil_VERDI("thread limit (4 including main)"); return; }
            int mål_e_post = heap_VERDI[objekt_referere] == 13 ? heap_VERDI[objekt_referere + 2] : objekt_referere;
            int Fil_INDEKS = mål_e_post > 0 && heap_VERDI[mål_e_post] >= 32 ? navn_metode(heap_VERDI[mål_e_post] - 32, norsk ? "Kjør" : "run", "()V") : -1;
            if (mål_e_post != 0 && Fil_INDEKS < 0) { feil_VERDI("Runnable.run required"); return; }
            konto_VERDI = Trådteller++; tråd_objekt[konto_VERDI] = objekt_referere; tråd_mål[konto_VERDI] = mål_e_post;
            int bilde = konto_VERDI * 32; tråd_bilde[konto_VERDI] = Fil_INDEKS < 0 ? bilde - 1 : bilde; tråd_status[konto_VERDI] = Fil_INDEKS < 0 ? 3 : 1;
            if (Fil_INDEKS >= 0) { bilde_metode[bilde] = Fil_INDEKS; bilde_plassere[bilde] = metode_START[Fil_INDEKS]; lokal_VERDI[bilde * 128] = mål_e_post; lokal_Type[bilde * 128] = 2; }
            return;
        }
        feil_VERDI("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], e_post_SMS = new int[16];
    static int lokal_e_post() { return e_post_objekt(0x7f000001); }
    static int e_post_objekt(int VERDI) { int objekt_referere = tildele_lager(14, 1); if (!feil) heap_VERDI[objekt_referere + 2] = VERDI; return objekt_referere; }
    static int 주소해독(int objekt_referere) {
        if (objekt_referere == 0 || 글같음(objekt_referere, vert_tegn("localhost"), false)) return 0x7f000001;
        if (!objekt_VERDI(objekt_referere, 1)) return 0;
        int data_VERDI = 0, total_ANTALL = 0, e_post_byte = 0, 자릿수 = 0, oppføring_ANTALL = heap_VERDI[objekt_referere + 1];
        for (int Loop_INDEKS = 0; Loop_INDEKS <= oppføring_ANTALL; Loop_INDEKS++) {
            int tegnkode = Loop_INDEKS == oppføring_ANTALL ? '.' : heap_VERDI[objekt_referere + 2 + Loop_INDEKS];
            if (tegnkode == '.') { if (자릿수 == 0 || total_ANTALL == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } data_VERDI = data_VERDI << 8 | e_post_byte; total_ANTALL++; e_post_byte = 자릿수 = 0; }
            else { if (tegnkode < '0' || tegnkode > '9' || ++자릿수 > 3 || (e_post_byte = e_post_byte * 10 + tegnkode - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (total_ANTALL != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return data_VERDI;
    }
    static int e_post_tegn(int data_VERDI) {
        int oppføring_ANTALL = 0;
        for (int flytte = 24; flytte >= 0; flytte -= 8) {
            int e_post_byte = data_VERDI >>> flytte & 255;
            if (e_post_byte >= 100) e_post_SMS[oppføring_ANTALL++] = '0' + e_post_byte / 100;
            if (e_post_byte >= 10) e_post_SMS[oppføring_ANTALL++] = '0' + e_post_byte / 10 % 10;
            e_post_SMS[oppføring_ANTALL++] = '0' + e_post_byte % 10; if (flytte != 0) e_post_SMS[oppføring_ANTALL++] = '.';
        }
        int objekt_referere = tildele_lager(1, oppføring_ANTALL); if (!feil) for (int Loop_INDEKS = 0; Loop_INDEKS < oppføring_ANTALL; Loop_INDEKS++) heap_VERDI[objekt_referere + 2 + Loop_INDEKS] = e_post_SMS[Loop_INDEKS]; return objekt_referere;
    }
    static void 통신호출(int eier, int navn_konstant, int 서술상수, int kommando_KODE) {
        if (ord_SMS(eier, "java/net/InetAddress")) {
            if (kommando_KODE == 184 && ord_SMS(navn_konstant, "getLoopbackAddress") && ord_SMS(서술상수, "()Ljava/net/InetAddress;")) { 넣기(lokal_e_post(), 2); return; }
            if (kommando_KODE == 184 && ord_SMS(navn_konstant, "getByName") && ord_SMS(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int data_VERDI = 주소해독(빼기(2)); if (던진객체 == 0 && !feil) 넣기(e_post_objekt(data_VERDI), 2); return;
            }
            if (kommando_KODE == 182 && ord_SMS(navn_konstant, "getHostAddress") && ord_SMS(서술상수, "()Ljava/lang/String;")) { int objekt_referere = 빼기(2); if (objekt_VERDI(objekt_referere, 14)) 넣기(e_post_tegn(heap_VERDI[objekt_referere + 2]), 2); return; }
        }
        if (ord_SMS(eier, "java/net/DatagramPacket")) {
            if (kommando_KODE == 183 && ord_SMS(navn_konstant, "<init>") && (ord_SMS(서술상수, "([BI)V") || ord_SMS(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean mål_VERDI_referere = ord_SMS(서술상수, "([BILjava/net/InetAddress;I)V"); int portnummer = mål_VERDI_referere ? 빼기(1) : 0, e_post_referere = mål_VERDI_referere ? 빼기(2) : 0;
                int oppføring_ANTALL = 빼기(1), data_MATRISE = 빼기(2), objekt_referere = 빼기(2);
                if (!objekt_VERDI(objekt_referere, 16) || !objekt_VERDI(data_MATRISE, 20)) return;
                if (oppføring_ANTALL < 0 || oppføring_ANTALL > heap_VERDI[data_MATRISE + 1] || portnummer < 0 || portnummer > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (e_post_referere != 0 && !objekt_VERDI(e_post_referere, 14)) return;
                heap_VERDI[objekt_referere + 2] = data_MATRISE; heap_referere[objekt_referere + 2] = 1; heap_VERDI[objekt_referere + 3] = oppføring_ANTALL;
                heap_VERDI[objekt_referere + 4] = e_post_referere; heap_referere[objekt_referere + 4] = 1; heap_VERDI[objekt_referere + 5] = portnummer; return;
            }
            if (kommando_KODE == 182 && ord_SMS(navn_konstant, "setLength") && ord_SMS(서술상수, "(I)V")) {
                int oppføring_ANTALL = 빼기(1), objekt_referere = 빼기(2); if (!objekt_VERDI(objekt_referere, 16)) return;
                if (oppføring_ANTALL < 0 || oppføring_ANTALL > heap_VERDI[heap_VERDI[objekt_referere + 2] + 1]) 예외던짐(9, "invalid datagram length"); else heap_VERDI[objekt_referere + 3] = oppføring_ANTALL; return;
            }
            if (kommando_KODE == 182 && (ord_SMS(navn_konstant, "getData") && ord_SMS(서술상수, "()[B") || ord_SMS(navn_konstant, "getLength") && ord_SMS(서술상수, "()I") || ord_SMS(navn_konstant, "getAddress") && ord_SMS(서술상수, "()Ljava/net/InetAddress;") || ord_SMS(navn_konstant, "getPort") && ord_SMS(서술상수, "()I"))) {
                int objekt_referere = 빼기(2); if (!objekt_VERDI(objekt_referere, 16)) return;
                int oppføring_plassere = ord_SMS(navn_konstant, "getData") ? 2 : ord_SMS(navn_konstant, "getLength") ? 3 : ord_SMS(navn_konstant, "getAddress") ? 4 : 5;
                넣기(heap_VERDI[objekt_referere + oppføring_plassere], oppføring_plassere == 2 || oppføring_plassere == 4 ? 2 : 1); return;
            }
        }
        if (ord_SMS(eier, "java/net/DatagramSocket")) {
            if (kommando_KODE == 183 && ord_SMS(navn_konstant, "<init>") && (ord_SMS(서술상수, "()V") || ord_SMS(서술상수, "(I)V"))) {
                int portnummer = ord_SMS(서술상수, "()V") ? 0 : 빼기(1), objekt_referere = 빼기(2); if (!objekt_VERDI(objekt_referere, 15)) return;
                if (portnummer < 0 || portnummer > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = bruker.åpen_nettverk(portnummer); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else heap_VERDI[objekt_referere + 2] = 열린파일번호; return;
            }
            if (kommando_KODE == 182 && ord_SMS(navn_konstant, "setSoTimeout") && ord_SMS(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), objekt_referere = 빼기(2); if (!objekt_VERDI(objekt_referere, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else heap_VERDI[objekt_referere + 3] = 밀리초값; return;
            }
            if (kommando_KODE == 182 && ord_SMS(navn_konstant, "getLocalPort") && ord_SMS(서술상수, "()I")) { int objekt_referere = 빼기(2); if (objekt_VERDI(objekt_referere, 15)) 넣기(heap_VERDI[objekt_referere + 2] < 0 ? -1 : bruker.nettverk_port(heap_VERDI[objekt_referere + 2]), 1); return; }
            if (kommando_KODE == 182 && ord_SMS(navn_konstant, "isClosed") && ord_SMS(서술상수, "()Z")) { int objekt_referere = 빼기(2); if (objekt_VERDI(objekt_referere, 15)) 넣기(heap_VERDI[objekt_referere + 2] < 0 ? 1 : 0, 1); return; }
            if (kommando_KODE == 182 && ord_SMS(navn_konstant, "close") && ord_SMS(서술상수, "()V")) { int objekt_referere = 빼기(2); if (objekt_VERDI(objekt_referere, 15) && heap_VERDI[objekt_referere + 2] >= 0) { bruker.파일서술자닫기(heap_VERDI[objekt_referere + 2]); heap_VERDI[objekt_referere + 2] = -1; } return; }
            if (kommando_KODE == 182 && (ord_SMS(navn_konstant, "send") || ord_SMS(navn_konstant, "receive")) && ord_SMS(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int pakke = 빼기(2), objekt_referere = 빼기(2); if (!objekt_VERDI(pakke, 16) || !objekt_VERDI(objekt_referere, 15)) return;
                int data_MATRISE = heap_VERDI[pakke + 2], gyldig_lengde = heap_VERDI[pakke + 3], 열린파일번호 = heap_VERDI[objekt_referere + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (ord_SMS(navn_konstant, "send")) {
                    if (!objekt_VERDI(heap_VERDI[pakke + 4], 14)) return;
                    if (gyldig_lengde > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int Loop_INDEKS = 0; Loop_INDEKS < gyldig_lengde; Loop_INDEKS++) 통신임시[Loop_INDEKS] = heap_VERDI[data_MATRISE + 2 + Loop_INDEKS];
                    if (bruker.sende_nettverk(열린파일번호, heap_VERDI[heap_VERDI[pakke + 4] + 2], heap_VERDI[pakke + 5], 통신임시, gyldig_lengde) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int oppføring_ANTALL = bruker.motta_nettverk(열린파일번호, 통신임시, gyldig_lengde > 512 ? 512 : gyldig_lengde);
                    if (oppføring_ANTALL == -11) {
                        int gjeldende_tidspunkt = bruker.밀리초();
                        if (heap_VERDI[objekt_referere + 4] == 0) heap_VERDI[objekt_referere + 4] = gjeldende_tidspunkt + 1;
                        if (heap_VERDI[objekt_referere + 3] > 0 && gjeldende_tidspunkt - (heap_VERDI[objekt_referere + 4] - 1) >= heap_VERDI[objekt_referere + 3]) { heap_VERDI[objekt_referere + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(objekt_referere, 2); 넣기(pakke, 2); bilde_plassere[bilde_INDEKS] = 틀명령[bilde_INDEKS]; endringsforespørsel = true; return;
                    }
                    heap_VERDI[objekt_referere + 4] = 0;
                    if (oppføring_ANTALL < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int Loop_INDEKS = 0; Loop_INDEKS < oppføring_ANTALL; Loop_INDEKS++) heap_VERDI[data_MATRISE + 2 + Loop_INDEKS] = (byte)통신임시[Loop_INDEKS];
                    heap_VERDI[pakke + 3] = oppføring_ANTALL; heap_VERDI[pakke + 4] = e_post_objekt(통신임시[513]); heap_referere[pakke + 4] = 1; heap_VERDI[pakke + 5] = 통신임시[512];
                }
                return;
            }
        }
        feil_VERDI("unsupported java.net method");
    }
    static boolean 흐름대기(int objekt_referere) {
        int gjeldende_tidspunkt = bruker.밀리초();
        if (heap_VERDI[objekt_referere + 5] == 0) heap_VERDI[objekt_referere + 5] = gjeldende_tidspunkt + 1;
        if (heap_VERDI[objekt_referere + 3] > 0 && gjeldende_tidspunkt - (heap_VERDI[objekt_referere + 5] - 1) >= heap_VERDI[objekt_referere + 3]) { heap_VERDI[objekt_referere + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        bilde_plassere[bilde_INDEKS] = 틀명령[bilde_INDEKS]; endringsforespørsel = true; return true;
    }
    static void 흐름호출(int eier, int navn_konstant, int 서술상수, int kommando_KODE) {
        boolean motta_page = ord_SMS(eier, "java/net/ServerSocket"), strøm = ord_SMS(eier, "java/io/InputStream") || ord_SMS(eier, "java/io/OutputStream");
        if (!strøm && kommando_KODE == 183 && ord_SMS(navn_konstant, "<init>")) {
            boolean informasjonssystemer_tom_status = ord_SMS(서술상수, "()V"), 이름지정여부 = ord_SMS(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = ord_SMS(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(informasjonssystemer_tom_status || motta_page && ord_SMS(서술상수, "(I)V") || !motta_page && (이름지정여부 || 주소지정여부))) { feil_VERDI("unsupported socket constructor"); return; }
            int portnummer = informasjonssystemer_tom_status ? 0 : 빼기(1), e_post_referere = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, objekt_referere = 빼기(2);
            if (!objekt_VERDI(objekt_referere, motta_page ? 18 : 17)) return;
            if (portnummer < 0 || portnummer > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !objekt_VERDI(e_post_referere, 14)) return;
            int nettverks_ID = 이름지정여부 ? 주소해독(e_post_referere) : 주소지정여부 ? heap_VERDI[e_post_referere + 2] : 0x7f000001;
            if (feil || 던진객체 != 0) return;
            int 열린파일번호 = bruker.strøm_kontroll(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = informasjonssystemer_tom_status ? 0 : motta_page ? bruker.strøm_kontroll(1, 열린파일번호, portnummer) : bruker.KOBLE_TIL_strøm(열린파일번호, nettverks_ID, portnummer);
            if (처리값 < 0) { bruker.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            heap_VERDI[objekt_referere + 2] = 열린파일번호; heap_VERDI[objekt_referere + 4] = portnummer; heap_VERDI[objekt_referere + 6] = informasjonssystemer_tom_status ? 0 : 1; return;
        }
        if (!strøm && ord_SMS(navn_konstant, "setSoTimeout") && ord_SMS(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), objekt_referere = 빼기(2); if (!objekt_VERDI(objekt_referere, motta_page ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else heap_VERDI[objekt_referere + 3] = 밀리초값; return; }
        if (!strøm && ord_SMS(navn_konstant, "close") && ord_SMS(서술상수, "()V")) { int objekt_referere = 빼기(2); if (objekt_VERDI(objekt_referere, motta_page ? 18 : 17) && heap_VERDI[objekt_referere + 2] >= 0) { bruker.파일서술자닫기(heap_VERDI[objekt_referere + 2]); heap_VERDI[objekt_referere + 2] = -1; } return; }
        if (!strøm && (ord_SMS(navn_konstant, "getLocalPort") || ord_SMS(navn_konstant, "getPort") || ord_SMS(navn_konstant, "isClosed") || ord_SMS(navn_konstant, "isConnected"))) {
            int objekt_referere = 빼기(2); if (!objekt_VERDI(objekt_referere, motta_page ? 18 : 17)) return;
            넣기(ord_SMS(navn_konstant, "isClosed") ? heap_VERDI[objekt_referere + 2] < 0 ? 1 : 0 : ord_SMS(navn_konstant, "isConnected") ? heap_VERDI[objekt_referere + 6] : ord_SMS(navn_konstant, "getPort") ? heap_VERDI[objekt_referere + 4] : heap_VERDI[objekt_referere + 2] < 0 ? -1 : bruker.strøm_kontroll(4, heap_VERDI[objekt_referere + 2], 0), 1); return;
        }
        if (motta_page && ord_SMS(navn_konstant, "accept") && ord_SMS(서술상수, "()Ljava/net/Socket;")) {
            int objekt_referere = 빼기(2); if (!objekt_VERDI(objekt_referere, 18)) return; int 열린파일번호 = bruker.strøm_kontroll(3, heap_VERDI[objekt_referere + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(objekt_referere)) 넣기(objekt_referere, 2); return; }
            heap_VERDI[objekt_referere + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = tildele_lager(17, 5); if (feil) { bruker.파일서술자닫기(열린파일번호); return; } heap_VERDI[반환값 + 2] = 열린파일번호; heap_VERDI[반환값 + 4] = bruker.strøm_kontroll(5, 열린파일번호, 0); heap_VERDI[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!motta_page && !strøm && ((ord_SMS(navn_konstant, "getInputStream") && ord_SMS(서술상수, "()Ljava/io/InputStream;")) || (ord_SMS(navn_konstant, "getOutputStream") && ord_SMS(서술상수, "()Ljava/io/OutputStream;")))) {
            int objekt_referere = 빼기(2); if (!objekt_VERDI(objekt_referere, 17)) return; if (heap_VERDI[objekt_referere + 2] < 0 || heap_VERDI[objekt_referere + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = tildele_lager(19, 4); if (feil) return; heap_VERDI[반환값 + 2] = objekt_referere; heap_referere[반환값 + 2] = 1; heap_VERDI[반환값 + 3] = ord_SMS(navn_konstant, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (strøm) {
            boolean 읽기여부 = ord_SMS(navn_konstant, "read"), informasjonssystemer_skrive_operasjon = ord_SMS(navn_konstant, "write"), blokk = ord_SMS(서술상수, "([B)I") || ord_SMS(서술상수, "([B)V"), informasjonssystemer_UNDERMATRISE = ord_SMS(서술상수, "([BII)I") || ord_SMS(서술상수, "([BII)V");
            int oppføring_ANTALL = informasjonssystemer_UNDERMATRISE ? 빼기(1) : 0, 시작변위 = informasjonssystemer_UNDERMATRISE ? 빼기(1) : 0, data_MATRISE = blokk || informasjonssystemer_UNDERMATRISE ? 빼기(2) : 0;
            int data_VERDI = informasjonssystemer_skrive_operasjon && ord_SMS(서술상수, "(I)V") ? 빼기(1) : 0, objekt_referere = 빼기(2);
            if (!objekt_VERDI(objekt_referere, 19)) return; int overordnet_referere = heap_VERDI[objekt_referere + 2], 열린파일번호 = heap_VERDI[overordnet_referere + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (ord_SMS(navn_konstant, "close") && ord_SMS(서술상수, "()V")) { bruker.파일서술자닫기(열린파일번호); heap_VERDI[overordnet_referere + 2] = -1; return; }
            if (ord_SMS(navn_konstant, "flush") && ord_SMS(서술상수, "()V")) return;
            if ((!읽기여부 && !informasjonssystemer_skrive_operasjon) || 읽기여부 != (heap_VERDI[objekt_referere + 3] == 0)) { feil_VERDI("unsupported stream operation"); return; }
            if (blokk || informasjonssystemer_UNDERMATRISE) { if (!objekt_VERDI(data_MATRISE, 20)) return; if (blokk) oppføring_ANTALL = heap_VERDI[data_MATRISE + 1]; if (시작변위 < 0 || oppføring_ANTALL < 0 || 시작변위 > heap_VERDI[data_MATRISE + 1] - oppføring_ANTALL) { 예외던짐(6, "stream array bounds"); return; } }
            else oppføring_ANTALL = 1;
            if (oppføring_ANTALL == 0) { if (읽기여부) 넣기(0, 1); return; }
            int Fullført_ANTALL = informasjonssystemer_skrive_operasjon ? heap_VERDI[objekt_referere + 4] : 0, 처리값 = 0;
            while (Fullført_ANTALL < oppføring_ANTALL) {
                처리값 = 읽기여부 ? bruker.파일한바이트읽기(열린파일번호) : bruker.파일한바이트쓰기(열린파일번호, blokk || informasjonssystemer_UNDERMATRISE ? heap_VERDI[data_MATRISE + 2 + 시작변위 + Fullført_ANTALL] : data_VERDI);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (blokk || informasjonssystemer_UNDERMATRISE)) heap_VERDI[data_MATRISE + 2 + 시작변위 + Fullført_ANTALL] = (byte)처리값;
                Fullført_ANTALL++; if (읽기여부 && !(blokk || informasjonssystemer_UNDERMATRISE)) break;
            }
            if (처리값 == -11 && (informasjonssystemer_skrive_operasjon || Fullført_ANTALL == 0)) {
                heap_VERDI[objekt_referere + 4] = Fullført_ANTALL;
                if (흐름대기(overordnet_referere)) { 넣기(objekt_referere, 2); if (blokk || informasjonssystemer_UNDERMATRISE) 넣기(data_MATRISE, 2); if (informasjonssystemer_UNDERMATRISE) { 넣기(시작변위, 1); 넣기(oppføring_ANTALL, 1); } if (informasjonssystemer_skrive_operasjon && !(blokk || informasjonssystemer_UNDERMATRISE)) 넣기(data_VERDI, 1); } return;
            }
            heap_VERDI[objekt_referere + 4] = 0; heap_VERDI[overordnet_referere + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(Fullført_ANTALL == 0 && 처리값 == 256 ? -1 : blokk || informasjonssystemer_UNDERMATRISE ? Fullført_ANTALL : 처리값, 1); return;
        }
        feil_VERDI("unsupported Socket/ServerSocket method");
    }
    static int[] skjermbilde_referere = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int navn_konstant) {
        if (ord_SMS(navn_konstant, "norsk/eget/Vindu")) return 24;
        if (ord_SMS(navn_konstant, "norsk/eget/Etikett")) return 26;
        if (ord_SMS(navn_konstant, "norsk/eget/Knapp")) return 27;
        if (ord_SMS(navn_konstant, "norsk/eget/tekstfelt")) return 28;
        if (ord_SMS(navn_konstant, "norsk/eget/Gjøremål_notice")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int navn_konstant) {
        return 한국어화면종(navn_konstant) != 0 || ord_SMS(navn_konstant, "norsk/eget/skjermbilde_element") || ord_SMS(navn_konstant, "norsk/eget/hendelse_kø");
    }
    static int skjermbilde_time(int navn_konstant) {
        int 한국어종 = 한국어화면종(navn_konstant); if (한국어종 != 0) return 한국어종;
        if (ord_SMS(navn_konstant, "javax/swing/JFrame")) return 24;
        if (ord_SMS(navn_konstant, "javax/swing/JPanel")) return 25;
        if (ord_SMS(navn_konstant, "javax/swing/JLabel")) return 26;
        if (ord_SMS(navn_konstant, "javax/swing/JButton")) return 27;
        if (ord_SMS(navn_konstant, "javax/swing/JTextField")) return 28;
        if (ord_SMS(navn_konstant, "java/awt/event/ActionEvent")) return 29;
        if (ord_SMS(navn_konstant, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean skjermbilde_eier(int navn_konstant) {
        return skjermbilde_time(navn_konstant) != 0 || ord_SMS(navn_konstant, "java/awt/Component") || ord_SMS(navn_konstant, "java/awt/Container") || ord_SMS(navn_konstant, "javax/swing/JComponent") || ord_SMS(navn_konstant, "javax/swing/AbstractButton") || ord_SMS(navn_konstant, "javax/swing/text/JTextComponent") || ord_SMS(navn_konstant, "javax/swing/SwingUtilities");
    }
    static boolean skjermbilde_objekt(int objekt_referere) { if (!informasjonssystemer_gyldig_objekt(objekt_referere)) return false; if (heap_VERDI[objekt_referere] < 24 || heap_VERDI[objekt_referere] > 28) { feil_VERDI("unsupported Swing receiver"); return false; } return true; }
    static void sett_skjermbilde_tegn(int objekt_referere, int SMS_referere) {
        if (SMS_referere != 0 && !objekt_VERDI(SMS_referere, 1)) return;
        int oppføring_ANTALL = SMS_referere == 0 ? 0 : heap_VERDI[SMS_referere + 1]; if (oppføring_ANTALL > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int Loop_INDEKS = 0; Loop_INDEKS < oppføring_ANTALL; Loop_INDEKS++) 화면글임시[Loop_INDEKS] = heap_VERDI[SMS_referere + 2 + Loop_INDEKS];
        if (bruker.skjermbilde_SMS(heap_VERDI[objekt_referere + 2], 화면글임시, oppføring_ANTALL) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        heap_VERDI[objekt_referere + 3] = SMS_referere; heap_referere[objekt_referere + 3] = 1;
    }
    static int 화면문자읽기(int objekt_referere) {
        int konto_VERDI = heap_VERDI[objekt_referere + 2], oppføring_ANTALL = bruker.skjermbilde_kontakt(8, konto_VERDI, 0, 0, 0, 0), 사용수 = 0;
        if (oppføring_ANTALL < 0) { feil_VERDI("GUI text read failed"); return 0; }
        for (int Loop_INDEKS = 0; Loop_INDEKS < oppføring_ANTALL; Loop_INDEKS++) { int 부호값 = bruker.skjermbilde_kontakt(9, konto_VERDI, Loop_INDEKS, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = tildele_lager(1, 사용수); if (!feil) for (int Loop_INDEKS = 0; Loop_INDEKS < 사용수; Loop_INDEKS++) heap_VERDI[반환값 + 2 + Loop_INDEKS] = 화면글임시[Loop_INDEKS]; return 반환값;
    }
    /* norsk 객체를 직접 만들고 kjerne_VERDI skjermbilde 기능에 연결한다. Swing objekt_VERDI/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int eier, int navn_konstant, int 서술상수, int kommando_KODE) {
        if (ord_SMS(eier, "norsk/eget/hendelse_kø")) {
            if (kommando_KODE == 184 && ord_SMS(navn_konstant, "나중에실행") && ord_SMS(서술상수, "(Lnorsk/eget/실행할일;)V")) {
                int oppgave_Gjøremål = 빼기(2); if (!informasjonssystemer_gyldig_objekt(oppgave_Gjøremål)) return;
                if (나중수 == 8) { feil_VERDI("skjermbilde 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = oppgave_Gjøremål; return;
            }
            if (kommando_KODE == 184 && ord_SMS(navn_konstant, "사건처리중인가") && ord_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            feil_VERDI("지원하지 않는 norsk skjermbilde 일정 호출"); return;
        }
        if (ord_SMS(eier, "norsk/eget/Gjøremål_notice")) {
            int notice = 빼기(2); if (!objekt_VERDI(notice, 29) || heap_VERDI[notice + 3] == 0) return;
            if (ord_SMS(navn_konstant, "hendelseskilde") && ord_SMS(서술상수, "()Lnorsk/eget/skjermbilde_element;")) 넣기(heap_VERDI[notice + 2], 2);
            else if (ord_SMS(navn_konstant, "kommando_SMS") && ord_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(heap_VERDI[notice + 2]), 2);
            else if (ord_SMS(navn_konstant, "INDEKS") && ord_SMS(서술상수, "()I")) 넣기(1001, 1);
            else feil_VERDI("지원하지 않는 norsk Handling notice 호출"); return;
        }
        if (kommando_KODE == 183 && ord_SMS(navn_konstant, "<init>")) {
            int 종류 = 한국어화면종(eier), 받이 = 0, 가로 = 0, vertikal_plassere = 0, 폭 = 0, 높이 = 0;
            if (종류 == 24 && ord_SMS(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (bruker.화면너비() - 폭) / 2; vertikal_plassere = (bruker.화면높이() - 높이) / 2;
            } else if ((종류 == 26 || 종류 == 28) && ord_SMS(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && ord_SMS(서술상수, "(Ljava/lang/String;IIIILnorsk/eget/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); vertikal_plassere = 빼기(1); 가로 = 빼기(1);
            } else { feil_VERDI("지원하지 않는 norsk skjermbilde 생성자"); return; }
            int Tekst = 빼기(2), element_VERDI = 빼기(2); if (!skjermbilde_objekt(element_VERDI)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || vertikal_plassere < 0 || 폭 > bruker.화면너비() - 가로 || 높이 > bruker.화면높이() - vertikal_plassere) { 예외던짐(27, "skjermbilde 영역을 벗어난 크기입니다"); return; }
            int INDEKS = bruker.skjermbilde_kontakt(0, 종류 - 23, 0, 0, 0, 0);
            if (INDEKS < 1 || INDEKS > 32) { feil_VERDI("skjermbilde element_VERDI 자리가 가득 찼습니다"); return; }
            heap_VERDI[element_VERDI + 2] = INDEKS; skjermbilde_referere[INDEKS - 1] = element_VERDI;
            heap_VERDI[element_VERDI + 5] = 가로; heap_VERDI[element_VERDI + 6] = vertikal_plassere; heap_VERDI[element_VERDI + 7] = 폭; heap_VERDI[element_VERDI + 8] = 높이; heap_VERDI[element_VERDI + 10] = 2;
            heap_VERDI[element_VERDI + 4] = 받이; heap_referere[element_VERDI + 4] = 1; heap_VERDI[element_VERDI + 12] = 1;
            bruker.skjermbilde_kontakt(1, INDEKS, 가로, vertikal_plassere, 폭, 높이);
            if (종류 == 24) bruker.skjermbilde_kontakt(7, INDEKS, 2, 0, 0, 0);
            sett_skjermbilde_tegn(element_VERDI, Tekst); return;
        }
        if (kommando_KODE != 182) { feil_VERDI("잘못된 norsk skjermbilde 호출 Kommando"); return; }
        if (ord_SMS(navn_konstant, "skrive_SMS") && ord_SMS(서술상수, "(Ljava/lang/String;)V")) {
            int Tekst = 빼기(2), element_VERDI = 빼기(2); if (skjermbilde_objekt(element_VERDI)) sett_skjermbilde_tegn(element_VERDI, Tekst); return;
        }
        if (ord_SMS(navn_konstant, "글읽기") && ord_SMS(서술상수, "()Ljava/lang/String;")) {
            int element_VERDI = 빼기(2); if (skjermbilde_objekt(element_VERDI)) 넣기(화면문자읽기(element_VERDI), 2); return;
        }
        if (ord_SMS(navn_konstant, "동작맡기기") && ord_SMS(서술상수, "(Lnorsk/eget/동작받이;)V")) {
            int 받이 = 빼기(2), element_VERDI = 빼기(2);
            if (skjermbilde_objekt(element_VERDI)) { heap_VERDI[element_VERDI + 4] = 받이; heap_referere[element_VERDI + 4] = 1; heap_VERDI[element_VERDI + 12] = 1; } return;
        }
        if (ord_SMS(navn_konstant, "Legg_til_element") && ord_SMS(서술상수, "(Lnorsk/eget/skjermbilde_element;)V")) {
            int barn_VERDI = 빼기(2), overordnet_VERDI_881a8172 = 빼기(2); if (!skjermbilde_objekt(barn_VERDI) || !skjermbilde_objekt(overordnet_VERDI_881a8172)) return;
            if (bruker.skjermbilde_kontakt(2, heap_VERDI[overordnet_VERDI_881a8172 + 2], heap_VERDI[barn_VERDI + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 skjermbilde 부모입니다"); return; }
            heap_VERDI[barn_VERDI + 11] = overordnet_VERDI_881a8172; heap_referere[barn_VERDI + 11] = 1; return;
        }
        if (ord_SMS(navn_konstant, "자리정하기") && ord_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), vertikal_plassere = 빼기(1), 가로 = 빼기(1), element_VERDI = 빼기(2); if (!skjermbilde_objekt(element_VERDI)) return;
            if (bruker.skjermbilde_kontakt(1, heap_VERDI[element_VERDI + 2], 가로, vertikal_plassere, 폭, 높이) < 0) { 예외던짐(27, "skjermbilde 영역을 벗어난 자리입니다"); return; }
            heap_VERDI[element_VERDI + 5] = 가로; heap_VERDI[element_VERDI + 6] = vertikal_plassere; heap_VERDI[element_VERDI + 7] = 폭; heap_VERDI[element_VERDI + 8] = 높이; return;
        }
        if ((ord_SMS(navn_konstant, "vise_vindu") || ord_SMS(navn_konstant, "Lukk")) && ord_SMS(서술상수, "()V")) {
            boolean synlighet_VERDI = ord_SMS(navn_konstant, "vise_vindu"); int element_VERDI = 빼기(2); if (!skjermbilde_objekt(element_VERDI)) return;
            if (bruker.skjermbilde_kontakt(synlighet_VERDI ? 3 : 4, heap_VERDI[element_VERDI + 2], synlighet_VERDI ? 1 : 0, 0, 0, 0) < 0) { feil_VERDI("화면은 interaktiv 명령에서 실행해야 합니다"); return; }
            heap_VERDI[element_VERDI + 9] = synlighet_VERDI ? 1 : 0; return;
        }
        if (ord_SMS(navn_konstant, "보이는가") && ord_SMS(서술상수, "()Z")) { int element_VERDI = 빼기(2); if (skjermbilde_objekt(element_VERDI)) 넣기(heap_VERDI[element_VERDI + 9], 1); return; }
        feil_VERDI("지원하지 않는 norsk skjermbilde metode_VERDI");
    }
    static void 화면호출(int eier, int navn_konstant, int 서술상수, int kommando_KODE) {
        if (ord_SMS(eier, "javax/swing/SwingUtilities")) {
            if (kommando_KODE == 184 && ord_SMS(navn_konstant, "invokeLater") && ord_SMS(서술상수, "(Ljava/lang/Runnable;)V")) { int objekt_referere = 빼기(2); if (!informasjonssystemer_gyldig_objekt(objekt_referere)) return; if (나중수 == 8) { feil_VERDI("invokeLater queue full"); return; } 나중실행[나중수++] = objekt_referere; return; }
            if (kommando_KODE == 184 && ord_SMS(navn_konstant, "isEventDispatchThread") && ord_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            feil_VERDI("unsupported SwingUtilities method"); return;
        }
        if (ord_SMS(eier, "java/awt/event/ActionEvent")) {
            int objekt_referere = 빼기(2); if (!objekt_VERDI(objekt_referere, 29)) return;
            if (ord_SMS(navn_konstant, "getSource") && ord_SMS(서술상수, "()Ljava/lang/Object;")) 넣기(heap_VERDI[objekt_referere + 2], 2);
            else if (ord_SMS(navn_konstant, "getActionCommand") && ord_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(heap_VERDI[objekt_referere + 2]), 2);
            else if (ord_SMS(navn_konstant, "getID") && ord_SMS(서술상수, "()I")) 넣기(1001, 1);
            else feil_VERDI("unsupported ActionEvent method"); return;
        }
        if (kommando_KODE == 183 && ord_SMS(navn_konstant, "<init>")) {
            int KOLONNER = 0, SMS_referere = 0;
            if (ord_SMS(서술상수, "(I)V")) KOLONNER = 빼기(1);
            else if (ord_SMS(서술상수, "(Ljava/lang/String;I)V")) { KOLONNER = 빼기(1); SMS_referere = 빼기(2); }
            else if (ord_SMS(서술상수, "(Ljava/lang/String;)V")) SMS_referere = 빼기(2);
            else if (ord_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!ord_SMS(서술상수, "()V")) { feil_VERDI("unsupported Swing constructor"); return; }
            int objekt_referere = 빼기(2); if (!informasjonssystemer_gyldig_objekt(objekt_referere)) return;
            if (heap_VERDI[objekt_referere] == 30) { feil_VERDI("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!skjermbilde_objekt(objekt_referere) || KOLONNER < 0) return;
            int konto_VERDI = bruker.skjermbilde_kontakt(0, heap_VERDI[objekt_referere] - 23, 0, 0, 0, 0);
            if (konto_VERDI < 1 || konto_VERDI > 32) { feil_VERDI("GUI widget slots exhausted"); return; }
            heap_VERDI[objekt_referere + 2] = konto_VERDI; skjermbilde_referere[konto_VERDI - 1] = objekt_referere; heap_VERDI[objekt_referere + 5] = heap_VERDI[objekt_referere] == 24 ? 130 : 16; heap_VERDI[objekt_referere + 6] = heap_VERDI[objekt_referere] == 24 ? 110 : 16;
            heap_VERDI[objekt_referere + 7] = heap_VERDI[objekt_referere] == 24 ? 380 : 220; heap_VERDI[objekt_referere + 8] = heap_VERDI[objekt_referere] == 24 ? 240 : 28; heap_VERDI[objekt_referere + 10] = 1;
            sett_skjermbilde_tegn(objekt_referere, SMS_referere); return;
        }
        if (ord_SMS(navn_konstant, "setText") || ord_SMS(navn_konstant, "setTitle")) { int SMS_referere = 빼기(2), objekt_referere = 빼기(2); if (skjermbilde_objekt(objekt_referere) && ord_SMS(서술상수, "(Ljava/lang/String;)V")) sett_skjermbilde_tegn(objekt_referere, SMS_referere); return; }
        if (ord_SMS(navn_konstant, "getText") || ord_SMS(navn_konstant, "getTitle")) { int objekt_referere = 빼기(2); if (skjermbilde_objekt(objekt_referere) && ord_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(objekt_referere), 2); return; }
        if (ord_SMS(navn_konstant, "addActionListener") && ord_SMS(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int motta_referere = 빼기(2), objekt_referere = 빼기(2); if (skjermbilde_objekt(objekt_referere)) { heap_VERDI[objekt_referere + 4] = motta_referere; heap_referere[objekt_referere + 4] = 1; } return; }
        if (ord_SMS(navn_konstant, "getContentPane") && ord_SMS(서술상수, "()Ljava/awt/Container;")) { int objekt_referere = 빼기(2); if (skjermbilde_objekt(objekt_referere)) 넣기(objekt_referere, 2); return; }
        if (ord_SMS(navn_konstant, "setLayout") && ord_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) { int Oppsett_referere = 빼기(2), objekt_referere = 빼기(2); if (skjermbilde_objekt(objekt_referere) && Oppsett_referere != 0) feil_VERDI("only absolute layout (null) is supported"); return; }
        if (ord_SMS(navn_konstant, "add") && (ord_SMS(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || ord_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean Oppsett_vilkår = ord_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (Oppsett_vilkår) 빼기(2);
            int barn_referere = 빼기(2), objekt_referere = 빼기(2); if (!skjermbilde_objekt(barn_referere) || !skjermbilde_objekt(objekt_referere)) return;
            if (bruker.skjermbilde_kontakt(2, heap_VERDI[objekt_referere + 2], heap_VERDI[barn_referere + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            heap_VERDI[barn_referere + 11] = objekt_referere; heap_referere[barn_referere + 11] = 1; if (!Oppsett_vilkår) 넣기(barn_referere, 2); return;
        }
        if (ord_SMS(navn_konstant, "setBounds") && ord_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), Y_koordinat = 빼기(1), x_koordinat = 빼기(1), objekt_referere = 빼기(2); if (!skjermbilde_objekt(objekt_referere)) return;
            if (bruker.skjermbilde_kontakt(1, heap_VERDI[objekt_referere + 2], x_koordinat, Y_koordinat, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            heap_VERDI[objekt_referere + 5] = x_koordinat; heap_VERDI[objekt_referere + 6] = Y_koordinat; heap_VERDI[objekt_referere + 7] = 너비; heap_VERDI[objekt_referere + 8] = 높이; return;
        }
        if (ord_SMS(navn_konstant, "setSize") && ord_SMS(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), objekt_referere = 빼기(2); if (!skjermbilde_objekt(objekt_referere)) return;
            if (bruker.skjermbilde_kontakt(1, heap_VERDI[objekt_referere + 2], heap_VERDI[objekt_referere + 5], heap_VERDI[objekt_referere + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { heap_VERDI[objekt_referere + 7] = 너비; heap_VERDI[objekt_referere + 8] = 높이; } return;
        }
        if (ord_SMS(navn_konstant, "setLocationRelativeTo") && ord_SMS(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), objekt_referere = 빼기(2); if (!skjermbilde_objekt(objekt_referere)) return; if (상대배치 != 0) { feil_VERDI("only screen centering supported"); return; } heap_VERDI[objekt_referere + 5] = (bruker.화면너비() - heap_VERDI[objekt_referere + 7]) / 2; heap_VERDI[objekt_referere + 6] = (bruker.화면높이() - heap_VERDI[objekt_referere + 8]) / 2; bruker.skjermbilde_kontakt(1, heap_VERDI[objekt_referere + 2], heap_VERDI[objekt_referere + 5], heap_VERDI[objekt_referere + 6], heap_VERDI[objekt_referere + 7], heap_VERDI[objekt_referere + 8]); return; }
        if (ord_SMS(navn_konstant, "setDefaultCloseOperation") && ord_SMS(서술상수, "(I)V")) { int Policy = 빼기(1), objekt_referere = 빼기(2); if (skjermbilde_objekt(objekt_referere)) { if (Policy < 0 || Policy > 3) 예외던짐(9, "close policy"); else { heap_VERDI[objekt_referere + 10] = Policy; bruker.skjermbilde_kontakt(7, heap_VERDI[objekt_referere + 2], Policy, 0, 0, 0); } } return; }
        if (ord_SMS(navn_konstant, "setVisible") && ord_SMS(서술상수, "(Z)V")) { int data_VERDI = 빼기(1), objekt_referere = 빼기(2); if (skjermbilde_objekt(objekt_referere)) { int 처리값 = bruker.skjermbilde_kontakt(3, heap_VERDI[objekt_referere + 2], data_VERDI, 0, 0, 0); if (처리값 < 0) feil_VERDI("Swing requires a standalone interactive command"); else heap_VERDI[objekt_referere + 9] = data_VERDI; } return; }
        if (ord_SMS(navn_konstant, "dispose") && ord_SMS(서술상수, "()V")) { int objekt_referere = 빼기(2); if (skjermbilde_objekt(objekt_referere)) { bruker.skjermbilde_kontakt(4, heap_VERDI[objekt_referere + 2], 0, 0, 0, 0); heap_VERDI[objekt_referere + 9] = 0; } return; }
        if (ord_SMS(navn_konstant, "repaint") || ord_SMS(navn_konstant, "validate")) { int objekt_referere = 빼기(2); if (!skjermbilde_objekt(objekt_referere) || !ord_SMS(서술상수, "()V")) return; bruker.skjermbilde_kontakt(1, heap_VERDI[objekt_referere + 2], heap_VERDI[objekt_referere + 5], heap_VERDI[objekt_referere + 6], heap_VERDI[objekt_referere + 7], heap_VERDI[objekt_referere + 8]); return; }
        if (ord_SMS(navn_konstant, "isVisible") && ord_SMS(서술상수, "()Z")) { int objekt_referere = 빼기(2); if (skjermbilde_objekt(objekt_referere)) 넣기(heap_VERDI[objekt_referere + 9], 1); return; }
        feil_VERDI("unsupported Swing method (native subset)");
    }
    static void fordele_hendelse(int mål_e_post, int hendelse_nummer, boolean norsk) {
        if (mål_e_post < 1 || heap_VERDI[mål_e_post] < 32) { feil_VERDI("Java event listener required"); return; }
        int Fil_INDEKS = navn_metode(heap_VERDI[mål_e_post] - 32, hendelse_nummer == 0 ? (norsk ? "Kjør" : "run") : (norsk ? "motta_Gjøremål" : "actionPerformed"), hendelse_nummer == 0 ? "()V" : (norsk ? "(Lnorsk/eget/Gjøremål_notice;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (Fil_INDEKS < 0) { feil_VERDI("event callback missing"); return; }
        betalt_tråd = 0; Trådteller = 1; bilde_INDEKS = 0; tråd_status[0] = 1; bilde_stakk[0] = 0; bilde_blokkere[0] = starte_bilde[0] = 0; endringsforespørsel = false;
        for (int Loop_INDEKS = 0; Loop_INDEKS < 128; Loop_INDEKS++) { lokal_VERDI[Loop_INDEKS] = lokal_Type[Loop_INDEKS] = 0; }
        bilde_metode[0] = Fil_INDEKS; bilde_plassere[0] = metode_START[Fil_INDEKS]; lokal_VERDI[0] = mål_e_post; lokal_Type[0] = 2;
        if (hendelse_nummer != 0) { lokal_VERDI[1] = hendelse_nummer; lokal_Type[1] = 2; }
        사건중 = true; Utfør_kommando(); 사건중 = false;
    }
    static void skjermbilde_Events() {
        while (!feil) {
            if (나중수 > 0) { int mål_e_post = 나중실행[0], norsk = 나중한국어[0]; for (int Loop_INDEKS = 1; Loop_INDEKS < 나중수; Loop_INDEKS++) { 나중실행[Loop_INDEKS - 1] = 나중실행[Loop_INDEKS]; 나중한국어[Loop_INDEKS - 1] = 나중한국어[Loop_INDEKS]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; fordele_hendelse(mål_e_post, 0, norsk != 0); continue; }
            if (bruker.skjermbilde_kontakt(6, 0, 0, 0, 0, 0) == 0) return;
            int hendelse_nummer = bruker.skjermbilde_kontakt(5, 0, 0, 0, 0, 0); if (hendelse_nummer == 0) continue;
            if (hendelse_nummer < 0) { feil_VERDI("GUI event I/O failed"); return; }
            int konto_VERDI = hendelse_nummer & 65535; if (konto_VERDI < 1 || konto_VERDI > 32) continue; int objekt_referere = skjermbilde_referere[konto_VERDI - 1]; if (objekt_referere == 0) continue;
            if ((hendelse_nummer & 65536) != 0) {
                if (heap_VERDI[objekt_referere + 10] != 0) heap_VERDI[objekt_referere + 9] = 0;
                if (heap_VERDI[objekt_referere + 10] == 3) for (int Loop_INDEKS = 0; Loop_INDEKS < 32; Loop_INDEKS++) if (skjermbilde_referere[Loop_INDEKS] != 0 && heap_VERDI[skjermbilde_referere[Loop_INDEKS]] == 24) bruker.skjermbilde_kontakt(4, Loop_INDEKS + 1, 0, 0, 0, 0);
            } else if (heap_VERDI[objekt_referere + 4] != 0) {
                int Viktig_fil_referere = tildele_lager(29, 2); if (feil) return; heap_VERDI[Viktig_fil_referere + 2] = objekt_referere; heap_VERDI[Viktig_fil_referere + 3] = heap_VERDI[objekt_referere + 12]; heap_referere[Viktig_fil_referere + 2] = 1; fordele_hendelse(heap_VERDI[objekt_referere + 4], Viktig_fil_referere, heap_VERDI[objekt_referere + 12] != 0);
            }
        }
    }
    public static int Kjør_2() {
        if (bruker.인수개수() == 1 && 자바도구.같음(bruker.Argumenter(0), "-version")) {
            bruker.Skriv("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (bruker.인수개수() < 1) { bruker.Skriv("Usage: java CLASS [ARGS]\n"); return 2; }
        oppføring_time_Definisjon = dossier_time_Definisjon(vert_tegn(bruker.Argumenter(0))); if (feil || oppføring_time_Definisjon < 0) return 1;
        int inngangspunkt_VERDI = navn_metode(oppføring_time_Definisjon, "Kjør_2", "()V");
        boolean 한국어진입 = inngangspunkt_VERDI >= 0 && (metode_tilgang[inngangspunkt_VERDI] & 9) == 9;
        if (!한국어진입) inngangspunkt_VERDI = navn_metode(oppføring_time_Definisjon, "main", "([Ljava/lang/String;)V");
        if (inngangspunkt_VERDI < 0 || (metode_tilgang[inngangspunkt_VERDI] & 9) != 9) feil_VERDI("public static void Kjør_2() or main(String[] args) required");
        if (feil) return 1;
        int Argumenter = tildele_lager(3, bruker.인수개수() - 1); matriseelement[Argumenter] = -1;
        for (int nummer = 1; nummer < bruker.인수개수() && !feil; nummer++) heap_VERDI[Argumenter + 1 + nummer] = vert_tegn(bruker.Argumenter(nummer));
        bilde_INDEKS = 0; bilde_metode[0] = inngangspunkt_VERDI; bilde_plassere[0] = metode_START[inngangspunkt_VERDI]; lokal_VERDI[0] = 한국어진입 ? 0 : Argumenter; lokal_Type[0] = 한국어진입 ? 0 : 2;
        tråd_status[0] = 1; tråd_objekt[0] = tildele_lager(13, 2);
        Utfør_kommando(); if (!feil) skjermbilde_Events(); return feil ? 1 : 0;
    }
}
