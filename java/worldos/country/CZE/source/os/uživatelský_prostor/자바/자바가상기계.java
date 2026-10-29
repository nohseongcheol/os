// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. název_souboru/operand_Štos/odkaz/větev 경계를 Provést_příkaz 중 검사한다. */
public final class 자바가상기계 {
    static int[] název_souboru = new int[16384], název_souboru_SMS = new int[64];
    static int[] konstanta_značka = new int[512], 상가 = new int[512], konstanta_SEKUNDA_HODNOTA = new int[512], řetězec_odkaz = new int[512];
    static int[] metoda_název_SMS = new int[32], metoda_TYP = new int[32], metoda_přístup = new int[32];
    static int[] metoda_START = new int[32], metoda_konec = new int[32], metoda_Štos = new int[32], 함수지역 = new int[32];
    static int[] metoda_argument_POČET = new int[32], metoda_argument_TYP = new int[512], metoda_Vratka = new int[32];
    static int[] mez_HODNOTA = new int[16384];
    static int[] místní_HODNOTA = new int[4096], místní_TYP = new int[4096], operand_Štos_HODNOTA = new int[4096], operand_Štos_TYP = new int[4096];
    static int[] rámec_metoda = new int[32], rámec_pozice = new int[32], rámec_Štos = new int[32];
    static int[] halda_HODNOTA = new int[8192];
    static int Velikost, 읽기위치, konstanta_POČET, metoda_POČET, název_třídy, rámec_INDEX = -1, halda_konec_pozice = 1, návratový_typ;
    static boolean chyba;

    static void selhání_HODNOTA(String Word_SMS) {
        if (!chyba) { uživatelský_prostor.Zápis("JVM error: "); uživatelský_prostor.Zápis(Word_SMS); uživatelský_prostor.zápis_znak_HODNOTA(10); }
        chyba = true;
    }
    static boolean oříznout(int Spustit_2, int délka_HODNOTA) { return Spustit_2 >= 0 && délka_HODNOTA >= 0 && Spustit_2 <= Velikost - délka_HODNOTA; }
    static int bajt_HODNOTA() {
        if (!oříznout(읽기위치, 1)) { selhání_HODNOTA("truncated class file"); return 0; }
        return název_souboru[읽기위치++];
    }
    static int 짧은수() { return bajt_HODNOTA() << 8 | bajt_HODNOTA(); }
    static int integer() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int délka_HODNOTA) { if (!oříznout(읽기위치, délka_HODNOTA)) selhání_HODNOTA("invalid attribute size"); else 읽기위치 += délka_HODNOTA; }
    static boolean šek_konstanta(int číslo, int Druh_HODNOTA) {
        if (číslo <= 0 || číslo >= konstanta_POČET || konstanta_značka[číslo] != Druh_HODNOTA) { selhání_HODNOTA("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean SMS_oblast(int Spustit_2, int délka_HODNOTA, String Word_SMS) {
        if (!oříznout(Spustit_2, délka_HODNOTA) || délka_HODNOTA != Word_SMS.length()) return false;
        for (int číslo = 0; číslo < délka_HODNOTA; číslo++) if (název_souboru[Spustit_2 + číslo] != Word_SMS.charAt(číslo)) return false;
        return true;
    }
    static boolean Word_SMS(int konstanta_HODNOTA, String Word_SMS) { return šek_konstanta(konstanta_HODNOTA, 1) && SMS_oblast(상가[konstanta_HODNOTA], konstanta_SEKUNDA_HODNOTA[konstanta_HODNOTA], Word_SMS); }
    static boolean 같은말(int 가, int SEKUNDA_operand) {
        if (!šek_konstanta(가, 1) || !šek_konstanta(SEKUNDA_operand, 1) || konstanta_SEKUNDA_HODNOTA[가] != konstanta_SEKUNDA_HODNOTA[SEKUNDA_operand]) return false;
        for (int číslo = 0; číslo < konstanta_SEKUNDA_HODNOTA[가]; číslo++) if (název_souboru[상가[가] + číslo] != název_souboru[상가[SEKUNDA_operand] + číslo]) return false;
        return true;
    }
    static int název_třídy_SMS(int číslo) { return šek_konstanta(číslo, 7) && šek_konstanta(상가[číslo], 1) ? 상가[číslo] : 0; }
    static int odkaz_název(int číslo) { return šek_konstanta(číslo, 12) && šek_konstanta(상가[číslo], 1) ? 상가[číslo] : 0; }
    static int odkaz_c74caca7(int číslo) { return šek_konstanta(číslo, 12) && šek_konstanta(konstanta_SEKUNDA_HODNOTA[číslo], 1) ? konstanta_SEKUNDA_HODNOTA[číslo] : 0; }
    static int popisovač_TYP(int 끝, boolean 빈형) {
        if (읽기위치 >= 끝) { selhání_HODNOTA("invalid descriptor"); return 0; }
        int HODNOTA = bajt_HODNOTA();
        if (HODNOTA == 'V' && 빈형) return 0;
        if (HODNOTA == 'I' || HODNOTA == 'B' || HODNOTA == 'C' || HODNOTA == 'S' || HODNOTA == 'Z') return 1;
        if (HODNOTA == '[') { popisovač_TYP(끝, false); return 2; }
        if (HODNOTA == 'L') {
            int Spustit_2 = 읽기위치;
            while (읽기위치 < 끝 && název_souboru[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == Spustit_2) selhání_HODNOTA("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        selhání_HODNOTA("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int funkce_HODNOTA) {
        int Předchozí_zboží = 읽기위치, číslo = metoda_TYP[funkce_HODNOTA];
        if (!šek_konstanta(číslo, 1)) return;
        읽기위치 = 상가[číslo]; int 끝 = 읽기위치 + konstanta_SEKUNDA_HODNOTA[číslo];
        if (bajt_HODNOTA() != '(') selhání_HODNOTA("invalid method descriptor");
        int zboží_POČET = 0;
        while (!chyba && 읽기위치 < 끝 && název_souboru[읽기위치] != ')') {
            if (zboží_POČET == 16) { selhání_HODNOTA("too many method arguments"); break; }
            metoda_argument_TYP[funkce_HODNOTA * 16 + zboží_POČET++] = popisovač_TYP(끝, false);
        }
        if (읽기위치 >= 끝 || bajt_HODNOTA() != ')') selhání_HODNOTA("invalid method descriptor");
        metoda_Vratka[funkce_HODNOTA] = popisovač_TYP(끝, true); metoda_argument_POČET[funkce_HODNOTA] = zboží_POČET;
        if (읽기위치 != 끝) selhání_HODNOTA("invalid method descriptor");
        읽기위치 = Předchozí_zboží;
    }
    static void přeskočit_atribut() {
        int zboží_POČET = 짧은수();
        for (int číslo = 0; číslo < zboží_POČET && !chyba; číslo++) { šek_konstanta(짧은수(), 1); 건너(integer()); }
    }
    static int příkaz_délka(int HODNOTA) {
        if (HODNOTA == 16 || HODNOTA == 18 || HODNOTA == 21 || HODNOTA == 25 || HODNOTA == 54 || HODNOTA == 58 || HODNOTA == 188) return 2;
        if (HODNOTA == 17 || HODNOTA == 19 || HODNOTA == 132 || HODNOTA >= 153 && HODNOTA <= 167
            || HODNOTA >= 178 && HODNOTA <= 184 || HODNOTA == 187 || HODNOTA == 189 || HODNOTA == 192 || HODNOTA == 198 || HODNOTA == 199) return 3;
        if (HODNOTA >= 0 && HODNOTA <= 8 || HODNOTA >= 26 && HODNOTA <= 29 || HODNOTA >= 42 && HODNOTA <= 46 || HODNOTA == 50
            || HODNOTA >= 59 && HODNOTA <= 62 || HODNOTA >= 75 && HODNOTA <= 79 || HODNOTA == 83 || HODNOTA == 87 || HODNOTA == 89 || HODNOTA == 95
            || HODNOTA == 96 || HODNOTA == 100 || HODNOTA == 104 || HODNOTA == 108 || HODNOTA == 112 || HODNOTA == 116
            || HODNOTA == 120 || HODNOTA == 122 || HODNOTA == 124 || HODNOTA == 126 || HODNOTA == 128 || HODNOTA == 130
            || HODNOTA >= 145 && HODNOTA <= 147 || HODNOTA == 172 || HODNOTA == 176 || HODNOTA == 177 || HODNOTA == 190) return 1;
        return 0;
    }
    static void 클래스읽기() {
        if (integer() != 0xcafebabe) selhání_HODNOTA("not a class file");
        int 부판 = 짧은수(), verze_HODNOTA = 짧은수();
        if (verze_HODNOTA < 45 || verze_HODNOTA > 52 || 부판 != 0) selhání_HODNOTA("supported class versions: 45..52, minor 0");
        konstanta_POČET = 짧은수();
        if (konstanta_POČET < 1 || konstanta_POČET > 512) { selhání_HODNOTA("constant pool limit (511)"); return; }
        for (int číslo = 1; číslo < konstanta_POČET && !chyba; číslo++) {
            int Druh_HODNOTA = bajt_HODNOTA(); konstanta_značka[číslo] = Druh_HODNOTA;
            if (Druh_HODNOTA == 1) { konstanta_SEKUNDA_HODNOTA[číslo] = 짧은수(); 상가[číslo] = 읽기위치; 건너(konstanta_SEKUNDA_HODNOTA[číslo]); }
            else if (Druh_HODNOTA == 3) 상가[číslo] = integer();
            else if (Druh_HODNOTA == 7 || Druh_HODNOTA == 8) 상가[číslo] = 짧은수();
            else if (Druh_HODNOTA == 9 || Druh_HODNOTA == 10 || Druh_HODNOTA == 12) { 상가[číslo] = 짧은수(); konstanta_SEKUNDA_HODNOTA[číslo] = 짧은수(); }
            else selhání_HODNOTA("unsupported constant type");
        }
        int oprávnění_HODNOTA = 짧은수();
        if ((oprávnění_HODNOTA & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) selhání_HODNOTA("unsupported class flags");
        název_třídy = název_třídy_SMS(짧은수());
        if (!Word_SMS(název_třídy_SMS(짧은수()), "java/lang/Object")) selhání_HODNOTA("inheritance unsupported");
        if (짧은수() != 0) selhání_HODNOTA("interfaces unsupported");
        if (짧은수() != 0) selhání_HODNOTA("fields unsupported");
        metoda_POČET = 짧은수();
        if (metoda_POČET < 1 || metoda_POČET > 32) { selhání_HODNOTA("method count limit (32)"); return; }
        for (int číslo = 0; číslo < metoda_POČET && !chyba; číslo++) {
            metoda_přístup[číslo] = 짧은수(); metoda_název_SMS[číslo] = 짧은수(); metoda_TYP[číslo] = 짧은수();
            šek_konstanta(metoda_název_SMS[číslo], 1); 서술읽기(číslo);
            if ((metoda_přístup[číslo] & (0x100 | 0x400 | 0x20)) != 0) selhání_HODNOTA("native, abstract and synchronized methods unsupported");
            if ((metoda_přístup[číslo] & 8) == 0 && !Word_SMS(metoda_název_SMS[číslo], "<init>")) selhání_HODNOTA("instance methods unsupported");
            if (Word_SMS(metoda_název_SMS[číslo], "<clinit>")) selhání_HODNOTA("class initializers unsupported");
            for (int přední_fotoaparát_HODNOTA = 0; přední_fotoaparát_HODNOTA < číslo; přední_fotoaparát_HODNOTA++) if (같은말(metoda_název_SMS[přední_fotoaparát_HODNOTA], metoda_název_SMS[číslo]) && 같은말(metoda_TYP[přední_fotoaparát_HODNOTA], metoda_TYP[číslo])) selhání_HODNOTA("duplicate method");
            int zboží_POČET = 짧은수();
            for (int hodnota_atributu = 0; hodnota_atributu < zboží_POČET && !chyba; hodnota_atributu++) {
                int Název = 짧은수(), délka_HODNOTA = integer(), Spustit_2 = 읽기위치;
                if (!oříznout(Spustit_2, délka_HODNOTA)) { selhání_HODNOTA("truncated method attribute"); break; }
                if (Word_SMS(Název, "Code")) {
                    if (metoda_START[číslo] != 0) selhání_HODNOTA("duplicate Code attribute");
                    metoda_Štos[číslo] = 짧은수(); 함수지역[číslo] = 짧은수(); int KÓD_délka = integer();
                    if (metoda_Štos[číslo] > 128 || 함수지역[číslo] > 128 || 함수지역[číslo] < metoda_argument_POČET[číslo]
                        || KÓD_délka < 1 || KÓD_délka > 8192) selhání_HODNOTA("method memory limits exceeded");
                    metoda_START[číslo] = 읽기위치; 건너(KÓD_délka); metoda_konec[číslo] = 읽기위치;
                    if (짧은수() != 0) selhání_HODNOTA("exception handlers unsupported");
                    přeskočit_atribut();
                    if (읽기위치 != Spustit_2 + délka_HODNOTA) selhání_HODNOTA("Code attribute size mismatch");
                } else 건너(délka_HODNOTA);
            }
            if (metoda_START[číslo] == 0) selhání_HODNOTA("missing Code attribute");
            int přihrádka_položka = metoda_START[číslo];
            while (přihrádka_položka < metoda_konec[číslo] && !chyba) {
                int délka_HODNOTA = příkaz_délka(název_souboru[přihrádka_položka]);
                if (délka_HODNOTA == 0 || délka_HODNOTA > metoda_konec[číslo] - přihrádka_položka) { selhání_HODNOTA("unsupported or truncated bytecode"); break; }
                mez_HODNOTA[přihrádka_položka] = číslo + 1; přihrádka_položka += délka_HODNOTA;
            }
            // 실행하지 않는 경로에도 잘못된 větev 목적지를 허용하지 않는다.
            přihrádka_položka = metoda_START[číslo];
            while (přihrádka_položka < metoda_konec[číslo] && !chyba) {
                int HODNOTA = název_souboru[přihrádka_položka];
                if (HODNOTA >= 153 && HODNOTA <= 167 || HODNOTA == 198 || HODNOTA == 199) {
                    int cíl_HODNOTA = přihrádka_položka + (short)(název_souboru[přihrádka_položka + 1] << 8 | název_souboru[přihrádka_položka + 2]);
                    if (cíl_HODNOTA < metoda_START[číslo] || cíl_HODNOTA >= metoda_konec[číslo] || mez_HODNOTA[cíl_HODNOTA] != číslo + 1) selhání_HODNOTA("invalid branch target");
                }
                přihrádka_položka += příkaz_délka(HODNOTA);
            }
        }
        if (!chyba) přeskočit_atribut();
        if (읽기위치 != Velikost) selhání_HODNOTA("extra class file data");
    }
    static int přidělit_Storage(int Druh_HODNOTA, int délka_HODNOTA) {
        if (délka_HODNOTA < 0 || délka_HODNOTA > halda_HODNOTA.length - halda_konec_pozice - 2) { selhání_HODNOTA("object heap exhausted or negative array size"); return 0; }
        int odkaz = halda_konec_pozice; halda_konec_pozice += délka_HODNOTA + 2; halda_HODNOTA[odkaz] = Druh_HODNOTA; halda_HODNOTA[odkaz + 1] = délka_HODNOTA;
        return odkaz;
    }
    static boolean objekt_HODNOTA(int odkaz, int Druh_HODNOTA) {
        if (odkaz < 1 || odkaz >= halda_konec_pozice - 1 || halda_HODNOTA[odkaz] != Druh_HODNOTA) { selhání_HODNOTA("null or invalid object reference"); return false; }
        return true;
    }
    static int konstanta_SMS(int INDEX) {
        if (!šek_konstanta(INDEX, 1)) return 0;
        if (řetězec_odkaz[INDEX] != 0) return řetězec_odkaz[INDEX];
        int odkaz = přidělit_Storage(1, konstanta_SEKUNDA_HODNOTA[INDEX]); if (chyba) return 0;
        int 끝 = 상가[INDEX] + konstanta_SEKUNDA_HODNOTA[INDEX], číslo = 상가[INDEX], délka_HODNOTA = 0;
        while (číslo < 끝 && !chyba) {
            int HODNOTA = název_souboru[číslo++];
            if (HODNOTA == 0) selhání_HODNOTA("invalid modified UTF-8");
            else if (HODNOTA >= 192 && HODNOTA <= 223 && číslo < 끝) {
                int Další_zboží = název_souboru[číslo++];
                if ((Další_zboží & 192) != 128) selhání_HODNOTA("invalid modified UTF-8");
                HODNOTA = (HODNOTA & 31) << 6 | Další_zboží & 63;
                if (HODNOTA != 0 && HODNOTA < 128) selhání_HODNOTA("overlong modified UTF-8");
            } else if (HODNOTA >= 224 && HODNOTA <= 239 && číslo + 1 < 끝) {
                int 가 = název_souboru[číslo++], SEKUNDA_operand = název_souboru[číslo++];
                if ((가 & 192) != 128 || (SEKUNDA_operand & 192) != 128) selhání_HODNOTA("invalid modified UTF-8");
                HODNOTA = (HODNOTA & 15) << 12 | (가 & 63) << 6 | SEKUNDA_operand & 63;
                if (HODNOTA < 2048) selhání_HODNOTA("overlong modified UTF-8");
            } else if (HODNOTA >= 128) selhání_HODNOTA("invalid modified UTF-8");
            halda_HODNOTA[odkaz + 2 + délka_HODNOTA++] = HODNOTA;
        }
        halda_HODNOTA[odkaz + 1] = délka_HODNOTA; řetězec_odkaz[INDEX] = odkaz; return odkaz;
    }
    static int hostit_znak(String HODNOTA) {
        int odkaz = přidělit_Storage(1, HODNOTA.length()); if (chyba) return 0;
        for (int číslo = 0; číslo < HODNOTA.length(); číslo++) halda_HODNOTA[odkaz + 2 + číslo] = HODNOTA.charAt(číslo);
        return odkaz;
    }
    static void zápis_SMS(int odkaz) {
        if (odkaz == 0) { uživatelský_prostor.Zápis("null"); return; }
        if (!objekt_HODNOTA(odkaz, 1)) return;
        for (int číslo = 0; číslo < halda_HODNOTA[odkaz + 1]; číslo++) uživatelský_prostor.zápis_znak_HODNOTA(halda_HODNOTA[odkaz + 2 + číslo]);
    }
    static int číslice_znak(int HODNOTA) {
        int odkaz = přidělit_Storage(1, 11); if (chyba) return 0;
        int délka_HODNOTA = 0;
        if (HODNOTA < 0) halda_HODNOTA[odkaz + 2 + délka_HODNOTA++] = '-'; else HODNOTA = -HODNOTA;
        int poziční_index = 1000000000; boolean Spustit_2 = false;
        while (poziční_index != 0) {
            int číslo = -(HODNOTA / poziční_index);
            if (číslo != 0 || Spustit_2 || poziční_index == 1) { halda_HODNOTA[odkaz + 2 + délka_HODNOTA++] = '0' + číslo; Spustit_2 = true; }
            HODNOTA %= poziční_index; poziční_index /= 10;
        }
        halda_HODNOTA[odkaz + 1] = délka_HODNOTA; return odkaz;
    }
    static int 정수해독(int odkaz) {
        if (!objekt_HODNOTA(odkaz, 1)) return 0;
        int délka_HODNOTA = halda_HODNOTA[odkaz + 1], číslo = 0, HODNOTA = 0; boolean 음수 = false;
        if (délka_HODNOTA > 0 && (halda_HODNOTA[odkaz + 2] == '-' || halda_HODNOTA[odkaz + 2] == '+')) { 음수 = halda_HODNOTA[odkaz + 2] == '-'; číslo++; }
        if (číslo == délka_HODNOTA) selhání_HODNOTA("NumberFormatException");
        for (; číslo < délka_HODNOTA && !chyba; číslo++) {
            int číslice_HODNOTA = halda_HODNOTA[odkaz + 2 + číslo] - '0';
            if (číslice_HODNOTA < 0 || číslice_HODNOTA > 9 || HODNOTA < -214748364 || HODNOTA == -214748364 && číslice_HODNOTA > (음수 ? 8 : 7)) selhání_HODNOTA("NumberFormatException");
            HODNOTA = HODNOTA * 10 - číslice_HODNOTA;
        }
        return 음수 ? HODNOTA : -HODNOTA;
    }
    static void 넣기(int HODNOTA, int TYP_HODNOTA) {
        if (chyba) return;
        if (rámec_INDEX < 0 || rámec_Štos[rámec_INDEX] >= metoda_Štos[rámec_metoda[rámec_INDEX]]) { selhání_HODNOTA("operand stack overflow"); return; }
        int přihrádka_položka = rámec_INDEX * 128 + rámec_Štos[rámec_INDEX]++; operand_Štos_HODNOTA[přihrádka_položka] = HODNOTA; operand_Štos_TYP[přihrádka_položka] = TYP_HODNOTA;
    }
    static int 빼기(int TYP_HODNOTA) {
        if (chyba) return 0;
        if (rámec_INDEX < 0 || rámec_Štos[rámec_INDEX] < 1) { selhání_HODNOTA("operand stack underflow"); return 0; }
        int přihrádka_položka = rámec_INDEX * 128 + --rámec_Štos[rámec_INDEX]; návratový_typ = operand_Štos_TYP[přihrádka_položka];
        if (TYP_HODNOTA != 0 && návratový_typ != TYP_HODNOTA) selhání_HODNOTA("operand type mismatch");
        return operand_Štos_HODNOTA[přihrádka_položka];
    }
    static void 지역읽기(int INDEX, int TYP_HODNOTA) {
        if (INDEX >= 함수지역[rámec_metoda[rámec_INDEX]] || INDEX < 0 || místní_TYP[rámec_INDEX * 128 + INDEX] != TYP_HODNOTA) { selhání_HODNOTA("invalid or uninitialized local"); return; }
        넣기(místní_HODNOTA[rámec_INDEX * 128 + INDEX], TYP_HODNOTA);
    }
    static void zápis_místní(int INDEX, int TYP_HODNOTA) {
        if (INDEX >= 함수지역[rámec_metoda[rámec_INDEX]] || INDEX < 0) { selhání_HODNOTA("local index out of range"); return; }
        int HODNOTA = 빼기(TYP_HODNOTA); místní_HODNOTA[rámec_INDEX * 128 + INDEX] = HODNOTA; místní_TYP[rámec_INDEX * 128 + INDEX] = TYP_HODNOTA;
    }
    static int 명바() {
        int pozice = rámec_pozice[rámec_INDEX];
        if (pozice < metoda_START[rámec_metoda[rámec_INDEX]] || pozice >= metoda_konec[rámec_metoda[rámec_INDEX]]) { selhání_HODNOTA("instruction pointer out of range"); return 0; }
        rámec_pozice[rámec_INDEX]++; return název_souboru[pozice];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void přesunout_HODNOTA(int pozice) {
        int funkce_HODNOTA = rámec_metoda[rámec_INDEX];
        if (pozice < metoda_START[funkce_HODNOTA] || pozice >= metoda_konec[funkce_HODNOTA] || mez_HODNOTA[pozice] != funkce_HODNOTA + 1) selhání_HODNOTA("invalid branch target");
        else rámec_pozice[rámec_INDEX] = pozice;
    }
    static void 호출(int funkce_HODNOTA) {
        if (rámec_INDEX == 31) { selhání_HODNOTA("call stack limit (32)"); return; }
        int Další_zboží = rámec_INDEX + 1;
        for (int číslo = 0; číslo < 128; číslo++) místní_TYP[Další_zboží * 128 + číslo] = 0;
        for (int číslo = metoda_argument_POČET[funkce_HODNOTA] - 1; číslo >= 0; číslo--) {
            místní_HODNOTA[Další_zboží * 128 + číslo] = 빼기(metoda_argument_TYP[funkce_HODNOTA * 16 + číslo]); místní_TYP[Další_zboží * 128 + číslo] = metoda_argument_TYP[funkce_HODNOTA * 16 + číslo];
        }
        rámec_INDEX = Další_zboží; rámec_metoda[rámec_INDEX] = funkce_HODNOTA; rámec_pozice[rámec_INDEX] = metoda_START[funkce_HODNOTA]; rámec_Štos[rámec_INDEX] = 0;
    }
    static void Vratka_KV(int TYP_HODNOTA) {
        if (TYP_HODNOTA != metoda_Vratka[rámec_metoda[rámec_INDEX]]) { selhání_HODNOTA("return type mismatch"); return; }
        int HODNOTA = TYP_HODNOTA == 0 ? 0 : 빼기(TYP_HODNOTA);
        rámec_INDEX--; if (rámec_INDEX >= 0 && TYP_HODNOTA != 0) 넣기(HODNOTA, TYP_HODNOTA);
    }
    static int[] tok_název_souboru = new int[64];
    static void Soubor_tok_VOLAT(int vlastník_HODNOTA, int Název, int formát_HODNOTA, int příkaz) {
        boolean výstupní_pozice = Word_SMS(vlastník_HODNOTA, "java/io/FileOutputStream");
        int Druh_HODNOTA = výstupní_pozice ? 6 : 5;
        if (příkaz == 183 && Word_SMS(Název, "<init>")) {
            boolean 이어 = false;
            if (výstupní_pozice && Word_SMS(formát_HODNOTA, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Word_SMS(formát_HODNOTA, "(Ljava/lang/String;)V")) { selhání_HODNOTA("unsupported file stream constructor"); return; }
            int Soubor_položka_název = 빼기(2), tok_HODNOTA = 빼기(2);
            if (!objekt_HODNOTA(Soubor_položka_název, 1) || !objekt_HODNOTA(tok_HODNOTA, Druh_HODNOTA) || chyba) return;
            if (halda_HODNOTA[tok_HODNOTA + 3] != 0) { selhání_HODNOTA("file stream already initialized"); return; }
            int délka_HODNOTA = halda_HODNOTA[Soubor_položka_název + 1];
            if (délka_HODNOTA < 1 || délka_HODNOTA > 63) { selhání_HODNOTA("invalid file name length"); return; }
            for (int přihrádka_položka = 0; přihrádka_položka < délka_HODNOTA; přihrádka_položka++) {
                int HODNOTA = halda_HODNOTA[Soubor_položka_název + 2 + přihrádka_položka];
                if (HODNOTA < 1 || HODNOTA > 127) { selhání_HODNOTA("file stream paths currently require ASCII"); return; }
                tok_název_souboru[přihrádka_položka] = HODNOTA;
            }
            tok_název_souboru[délka_HODNOTA] = 0;
            int popisovač_položka = uživatelský_prostor.otevřít_Soubor_popisovač(tok_název_souboru, výstupní_pozice ? (이어 ? 1089 : 577) : 0);
            if (popisovač_položka < 0) { selhání_HODNOTA("FileNotFoundException: file open failed"); return; }
            halda_HODNOTA[tok_HODNOTA + 2] = popisovač_položka; halda_HODNOTA[tok_HODNOTA + 3] = 1;
            return;
        }
        if (příkaz != 182) { selhání_HODNOTA("invalid file stream invocation"); return; }
        int Akce = -1, HODNOTA = 0;
        if (Word_SMS(Název, "close") && Word_SMS(formát_HODNOTA, "()V")) Akce = 0;
        if (!výstupní_pozice && Word_SMS(Název, "read") && Word_SMS(formát_HODNOTA, "()I")) Akce = 1;
        if (výstupní_pozice && Word_SMS(Název, "write") && Word_SMS(formát_HODNOTA, "(I)V")) { Akce = 2; HODNOTA = 빼기(1); }
        if (Akce < 0) { selhání_HODNOTA("unsupported file stream method"); return; }
        int tok_HODNOTA = 빼기(2);
        if (!objekt_HODNOTA(tok_HODNOTA, Druh_HODNOTA) || chyba) return;
        if (halda_HODNOTA[tok_HODNOTA + 3] == 0) { selhání_HODNOTA("uninitialized file stream"); return; }
        int popisovač_položka = halda_HODNOTA[tok_HODNOTA + 2];
        if (Akce == 0) {
            if (popisovač_položka >= 0 && uživatelský_prostor.Zavřít_Soubor_popisovač(popisovač_položka) < 0) selhání_HODNOTA("IOException: close failed");
            halda_HODNOTA[tok_HODNOTA + 2] = -1; return;
        }
        if (popisovač_položka < 0) { selhání_HODNOTA("IOException: stream closed"); return; }
        if (Akce == 1) {
            int VÝSLEDEK = uživatelský_prostor.파일한바이트읽기(popisovač_položka);
            if (VÝSLEDEK < -1) selhání_HODNOTA("IOException: read failed"); else 넣기(VÝSLEDEK, 1);
        } else if (uživatelský_prostor.파일한바이트쓰기(popisovač_položka, HODNOTA) != 1) selhání_HODNOTA("IOException: write failed");
    }
    static void VOLAT_metoda(int INDEX, int příkaz) {
        if (!šek_konstanta(INDEX, 10)) return;
        int vlastník_HODNOTA = název_třídy_SMS(상가[INDEX]), Název = odkaz_název(konstanta_SEKUNDA_HODNOTA[INDEX]), formát_HODNOTA = odkaz_c74caca7(konstanta_SEKUNDA_HODNOTA[INDEX]);
        if (chyba) return;
        if (같은말(vlastník_HODNOTA, název_třídy)) {
            if (příkaz != 184) { selhání_HODNOTA("only static user methods are supported"); return; }
            for (int číslo = 0; číslo < metoda_POČET; číslo++) if (같은말(Název, metoda_název_SMS[číslo]) && 같은말(formát_HODNOTA, metoda_TYP[číslo])) {
                if ((metoda_přístup[číslo] & 8) == 0) selhání_HODNOTA("method is not static"); else 호출(číslo);
                return;
            }
            selhání_HODNOTA("NoSuchMethodError"); return;
        }
        if (Word_SMS(vlastník_HODNOTA, "java/io/FileInputStream") || Word_SMS(vlastník_HODNOTA, "java/io/FileOutputStream")) {
            Soubor_tok_VOLAT(vlastník_HODNOTA, Název, formát_HODNOTA, příkaz); return;
        }
        if (příkaz == 184 && Word_SMS(vlastník_HODNOTA, "java/lang/Integer") && Word_SMS(Název, "parseInt") && Word_SMS(formát_HODNOTA, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (příkaz == 182 && Word_SMS(vlastník_HODNOTA, "java/io/PrintStream") && (Word_SMS(Název, "println") || Word_SMS(Název, "print"))) {
            int TYP_HODNOTA = 0, HODNOTA = 0;
            if (Word_SMS(formát_HODNOTA, "(I)V")) { TYP_HODNOTA = 1; HODNOTA = 빼기(1); }
            else if (Word_SMS(formát_HODNOTA, "(Z)V")) { TYP_HODNOTA = 2; HODNOTA = 빼기(1); }
            else if (Word_SMS(formát_HODNOTA, "(C)V")) { TYP_HODNOTA = 3; HODNOTA = 빼기(1); }
            else if (Word_SMS(formát_HODNOTA, "(Ljava/lang/String;)V")) { TYP_HODNOTA = 4; HODNOTA = 빼기(2); }
            else if (!Word_SMS(formát_HODNOTA, "()V") || !Word_SMS(Název, "println")) selhání_HODNOTA("unsupported print descriptor");
            if (빼기(2) != -1) selhání_HODNOTA("invalid PrintStream receiver");
            if (chyba) return;
            if (TYP_HODNOTA == 1) 자바도구.zápis_číslo(HODNOTA);
            if (TYP_HODNOTA == 2) uživatelský_prostor.Zápis(HODNOTA == 0 ? "false" : "true");
            if (TYP_HODNOTA == 3) uživatelský_prostor.zápis_znak_HODNOTA(HODNOTA & 65535);
            if (TYP_HODNOTA == 4) zápis_SMS(HODNOTA);
            if (Word_SMS(Název, "println")) uživatelský_prostor.zápis_znak_HODNOTA(10);
            return;
        }
        if (příkaz == 182 && Word_SMS(vlastník_HODNOTA, "java/lang/String")) {
            if (Word_SMS(Název, "length") && Word_SMS(formát_HODNOTA, "()I")) {
                int odkaz = 빼기(2); if (objekt_HODNOTA(odkaz, 1)) 넣기(halda_HODNOTA[odkaz + 1], 1); return;
            }
            if (Word_SMS(Název, "charAt") && Word_SMS(formát_HODNOTA, "(I)C")) {
                int dolní_index_HODNOTA = 빼기(1), odkaz = 빼기(2);
                if (objekt_HODNOTA(odkaz, 1)) {
                    if (dolní_index_HODNOTA < 0 || dolní_index_HODNOTA >= halda_HODNOTA[odkaz + 1]) selhání_HODNOTA("StringIndexOutOfBoundsException"); else 넣기(halda_HODNOTA[odkaz + 2 + dolní_index_HODNOTA], 1);
                }
                return;
            }
        }
        if (Word_SMS(vlastník_HODNOTA, "java/lang/StringBuilder")) {
            if (příkaz == 183 && Word_SMS(Název, "<init>") && Word_SMS(formát_HODNOTA, "()V")) { objekt_HODNOTA(빼기(2), 4); return; }
            if (příkaz == 182 && Word_SMS(Název, "toString") && Word_SMS(formát_HODNOTA, "()Ljava/lang/String;")) {
                int odkaz = 빼기(2); if (objekt_HODNOTA(odkaz, 4)) 넣기(halda_HODNOTA[odkaz + 2] == 0 ? hostit_znak("") : halda_HODNOTA[odkaz + 2], 2); return;
            }
            if (příkaz == 182 && Word_SMS(Název, "append")) {
                int text = 0;
                if (Word_SMS(formát_HODNOTA, "(I)Ljava/lang/StringBuilder;")) text = číslice_znak(빼기(1));
                else if (Word_SMS(formát_HODNOTA, "(Z)Ljava/lang/StringBuilder;")) text = hostit_znak(빼기(1) == 0 ? "false" : "true");
                else if (Word_SMS(formát_HODNOTA, "(C)Ljava/lang/StringBuilder;")) {
                    int HODNOTA = 빼기(1); text = přidělit_Storage(1, 1); if (!chyba) halda_HODNOTA[text + 2] = HODNOTA & 65535;
                }
                else if (Word_SMS(formát_HODNOTA, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { text = 빼기(2); if (text == 0) text = hostit_znak("null"); }
                else { selhání_HODNOTA("unsupported StringBuilder append"); return; }
                int odkaz = 빼기(2); if (!objekt_HODNOTA(odkaz, 4) || !objekt_HODNOTA(text, 1)) return;
                int přední_fotoaparát_HODNOTA = halda_HODNOTA[odkaz + 2], přední_fotoaparát_HODNOTA_délka = přední_fotoaparát_HODNOTA == 0 ? 0 : halda_HODNOTA[přední_fotoaparát_HODNOTA + 1], BACK_HODNOTA_délka = halda_HODNOTA[text + 1];
                int 새글 = přidělit_Storage(1, přední_fotoaparát_HODNOTA_délka + BACK_HODNOTA_délka); if (chyba) return;
                for (int číslo = 0; číslo < přední_fotoaparát_HODNOTA_délka; číslo++) halda_HODNOTA[새글 + 2 + číslo] = halda_HODNOTA[přední_fotoaparát_HODNOTA + 2 + číslo];
                for (int číslo = 0; číslo < BACK_HODNOTA_délka; číslo++) halda_HODNOTA[새글 + 2 + přední_fotoaparát_HODNOTA_délka + číslo] = halda_HODNOTA[text + 2 + číslo];
                halda_HODNOTA[odkaz + 2] = 새글; 넣기(odkaz, 2); return;
            }
        }
        selhání_HODNOTA("unsupported library method");
    }
    static int pole_přihrádka(int odkaz, int dolní_index_HODNOTA, int TYP_HODNOTA) {
        if (!objekt_HODNOTA(odkaz, TYP_HODNOTA)) return 0;
        if (dolní_index_HODNOTA < 0 || dolní_index_HODNOTA >= halda_HODNOTA[odkaz + 1]) { selhání_HODNOTA("ArrayIndexOutOfBoundsException"); return 0; }
        return odkaz + 2 + dolní_index_HODNOTA;
    }
    static void Provést_příkaz() {
        int 남음 = 500000;
        while (rámec_INDEX >= 0 && !chyba) {
            if (--남음 == 0) { selhání_HODNOTA("instruction limit (500000)"); break; }
            int Spustit_2 = rámec_pozice[rámec_INDEX], HODNOTA = 명바();
            if (chyba) break;
            if (HODNOTA == 0) continue;
            if (HODNOTA == 1) { 넣기(0, 2); continue; }
            if (HODNOTA >= 2 && HODNOTA <= 8) { 넣기(HODNOTA - 3, 1); continue; }
            if (HODNOTA == 16) { 넣기((byte)명바(), 1); continue; }
            if (HODNOTA == 17) { 넣기((short)명짧(), 1); continue; }
            if (HODNOTA == 18 || HODNOTA == 19) {
                int číslo = HODNOTA == 18 ? 명바() : 명짧();
                if (číslo <= 0 || číslo >= konstanta_POČET) selhání_HODNOTA("invalid ldc constant");
                else if (konstanta_značka[číslo] == 3) 넣기(상가[číslo], 1);
                else if (konstanta_značka[číslo] == 8) 넣기(konstanta_SMS(상가[číslo]), 2);
                else selhání_HODNOTA("unsupported ldc constant");
                continue;
            }
            if (HODNOTA == 21 || HODNOTA == 25) { 지역읽기(명바(), HODNOTA == 21 ? 1 : 2); continue; }
            if (HODNOTA >= 26 && HODNOTA <= 29) { 지역읽기(HODNOTA - 26, 1); continue; }
            if (HODNOTA >= 42 && HODNOTA <= 45) { 지역읽기(HODNOTA - 42, 2); continue; }
            if (HODNOTA == 54 || HODNOTA == 58) { zápis_místní(명바(), HODNOTA == 54 ? 1 : 2); continue; }
            if (HODNOTA >= 59 && HODNOTA <= 62) { zápis_místní(HODNOTA - 59, 1); continue; }
            if (HODNOTA >= 75 && HODNOTA <= 78) { zápis_místní(HODNOTA - 75, 2); continue; }
            if (HODNOTA == 46 || HODNOTA == 50) {
                int dolní_index_HODNOTA = 빼기(1), odkaz = 빼기(2), přihrádka_položka = pole_přihrádka(odkaz, dolní_index_HODNOTA, HODNOTA == 46 ? 2 : 3);
                if (!chyba) 넣기(halda_HODNOTA[přihrádka_položka], HODNOTA == 46 ? 1 : 2); continue;
            }
            if (HODNOTA == 79 || HODNOTA == 83) {
                int zboží_prvek = 빼기(HODNOTA == 79 ? 1 : 2), dolní_index_HODNOTA = 빼기(1), odkaz = 빼기(2), přihrádka_položka = pole_přihrádka(odkaz, dolní_index_HODNOTA, HODNOTA == 79 ? 2 : 3);
                if (HODNOTA == 83 && zboží_prvek != 0) objekt_HODNOTA(zboží_prvek, 1);
                if (!chyba) halda_HODNOTA[přihrádka_položka] = zboží_prvek; continue;
            }
            if (HODNOTA == 87) { 빼기(0); continue; }
            if (HODNOTA == 89) { int 가 = 빼기(0), TYP_HODNOTA = návratový_typ; 넣기(가, TYP_HODNOTA); 넣기(가, TYP_HODNOTA); continue; }
            if (HODNOTA == 95) { int 가 = 빼기(0), 가형 = návratový_typ, SEKUNDA_operand = 빼기(0), SEKUNDA_operand_TYP = návratový_typ; 넣기(가, 가형); 넣기(SEKUNDA_operand, SEKUNDA_operand_TYP); continue; }
            if (HODNOTA == 96 || HODNOTA == 100 || HODNOTA == 104 || HODNOTA == 108 || HODNOTA == 112 || HODNOTA == 120
                || HODNOTA == 122 || HODNOTA == 124 || HODNOTA == 126 || HODNOTA == 128 || HODNOTA == 130) {
                int SEKUNDA_operand = 빼기(1), 가 = 빼기(1), VÝSLEDEK = 0;
                if ((HODNOTA == 108 || HODNOTA == 112) && SEKUNDA_operand == 0) { selhání_HODNOTA("ArithmeticException: / by zero"); continue; }
                if (HODNOTA == 96) VÝSLEDEK = 가 + SEKUNDA_operand;
                if (HODNOTA == 100) VÝSLEDEK = 가 - SEKUNDA_operand;
                if (HODNOTA == 104) VÝSLEDEK = 가 * SEKUNDA_operand;
                if (HODNOTA == 108) VÝSLEDEK = 가 / SEKUNDA_operand;
                if (HODNOTA == 112) VÝSLEDEK = 가 % SEKUNDA_operand;
                if (HODNOTA == 120) VÝSLEDEK = 가 << SEKUNDA_operand;
                if (HODNOTA == 122) VÝSLEDEK = 가 >> SEKUNDA_operand;
                if (HODNOTA == 124) VÝSLEDEK = 가 >>> SEKUNDA_operand;
                if (HODNOTA == 126) VÝSLEDEK = 가 & SEKUNDA_operand;
                if (HODNOTA == 128) VÝSLEDEK = 가 | SEKUNDA_operand;
                if (HODNOTA == 130) VÝSLEDEK = 가 ^ SEKUNDA_operand;
                넣기(VÝSLEDEK, 1); continue;
            }
            if (HODNOTA == 116) { 넣기(-빼기(1), 1); continue; }
            if (HODNOTA == 132) {
                int místní_obor = 명바(), 증분 = (byte)명바(); 지역읽기(místní_obor, 1); 넣기(빼기(1) + 증분, 1); zápis_místní(místní_obor, 1); continue;
            }
            if (HODNOTA >= 145 && HODNOTA <= 147) {
                int číslo = 빼기(1); 넣기(HODNOTA == 145 ? (byte)číslo : HODNOTA == 146 ? (char)číslo : (short)číslo, 1); continue;
            }
            if (HODNOTA >= 153 && HODNOTA <= 167 || HODNOTA == 198 || HODNOTA == 199) {
                int cíl_HODNOTA = Spustit_2 + (short)명짧(); boolean 갈까 = HODNOTA == 167;
                if (HODNOTA >= 153 && HODNOTA <= 158) {
                    int číslo = 빼기(1); 갈까 = HODNOTA == 153 ? číslo == 0 : HODNOTA == 154 ? číslo != 0 : HODNOTA == 155 ? číslo < 0 : HODNOTA == 156 ? číslo >= 0 : HODNOTA == 157 ? číslo > 0 : číslo <= 0;
                } else if (HODNOTA >= 159 && HODNOTA <= 166) {
                    int SEKUNDA_operand = 빼기(HODNOTA >= 165 ? 2 : 1), 가 = 빼기(HODNOTA >= 165 ? 2 : 1);
                    갈까 = HODNOTA == 159 || HODNOTA == 165 ? 가 == SEKUNDA_operand : HODNOTA == 160 || HODNOTA == 166 ? 가 != SEKUNDA_operand : HODNOTA == 161 ? 가 < SEKUNDA_operand : HODNOTA == 162 ? 가 >= SEKUNDA_operand : HODNOTA == 163 ? 가 > SEKUNDA_operand : 가 <= SEKUNDA_operand;
                } else if (HODNOTA == 198 || HODNOTA == 199) { int číslo = 빼기(2); 갈까 = HODNOTA == 198 ? číslo == 0 : číslo != 0; }
                if (갈까) přesunout_HODNOTA(cíl_HODNOTA); continue;
            }
            if (HODNOTA == 172 || HODNOTA == 176 || HODNOTA == 177) { Vratka_KV(HODNOTA == 172 ? 1 : HODNOTA == 176 ? 2 : 0); continue; }
            if (HODNOTA == 178) {
                int číslo = 명짧(); if (!šek_konstanta(číslo, 9)) continue;
                if (!Word_SMS(název_třídy_SMS(상가[číslo]), "java/lang/System") || !Word_SMS(odkaz_název(konstanta_SEKUNDA_HODNOTA[číslo]), "out")
                    || !Word_SMS(odkaz_c74caca7(konstanta_SEKUNDA_HODNOTA[číslo]), "Ljava/io/PrintStream;")) selhání_HODNOTA("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (HODNOTA == 182 || HODNOTA == 183 || HODNOTA == 184) { VOLAT_metoda(명짧(), HODNOTA); continue; }
            if (HODNOTA == 187) {
                int Název = název_třídy_SMS(명짧());
                if (Word_SMS(Název, "java/lang/StringBuilder")) 넣기(přidělit_Storage(4, 1), 2);
                else if (Word_SMS(Název, "java/io/FileInputStream") || Word_SMS(Název, "java/io/FileOutputStream")) {
                    int odkaz = přidělit_Storage(Word_SMS(Název, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!chyba) { halda_HODNOTA[odkaz + 2] = -1; 넣기(odkaz, 2); }
                } else selhání_HODNOTA("unsupported object construction");
                continue;
            }
            if (HODNOTA == 188 || HODNOTA == 189) {
                if (HODNOTA == 188) { if (명바() != 10) selhání_HODNOTA("only int[] newarray is supported"); }
                else if (!Word_SMS(název_třídy_SMS(명짧()), "java/lang/String")) selhání_HODNOTA("only String[] anewarray is supported");
                int délka_HODNOTA = 빼기(1); 넣기(přidělit_Storage(HODNOTA == 188 ? 2 : 3, délka_HODNOTA), 2); continue;
            }
            if (HODNOTA == 190) {
                int odkaz = 빼기(2);
                if (odkaz < 1 || odkaz >= halda_konec_pozice - 1 || (halda_HODNOTA[odkaz] != 2 && halda_HODNOTA[odkaz] != 3)) selhání_HODNOTA("null or invalid array");
                else 넣기(halda_HODNOTA[odkaz + 1], 1); continue;
            }
            if (HODNOTA == 192) {
                int Název = název_třídy_SMS(명짧()), odkaz = 빼기(2);
                if (!Word_SMS(Název, "java/lang/String")) selhání_HODNOTA("unsupported checkcast");
                else if (odkaz != 0) objekt_HODNOTA(odkaz, 1);
                넣기(odkaz, 2); continue;
            }
            selhání_HODNOTA("unsupported bytecode");
        }
    }
    public static int Spustit_2() {
        if (uživatelský_prostor.인수개수() == 1 && 자바도구.같음(uživatelský_prostor.argumenty(0), "-version")) {
            uživatelský_prostor.Zápis("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (uživatelský_prostor.인수개수() < 1) { uživatelský_prostor.Zápis("Usage: java CLASS [ARGS]\n"); return 2; }
        int délka_HODNOTA = 자바도구.Název(název_souboru_SMS, uživatelský_prostor.argumenty(0));
        if (délka_HODNOTA < 1 || délka_HODNOTA > 57) { uživatelský_prostor.Zápis("java: invalid class name\n"); return 2; }
        název_souboru_SMS[délka_HODNOTA] = '.'; název_souboru_SMS[délka_HODNOTA + 1] = 'c'; název_souboru_SMS[délka_HODNOTA + 2] = 'l'; název_souboru_SMS[délka_HODNOTA + 3] = 'a'; název_souboru_SMS[délka_HODNOTA + 4] = 's'; název_souboru_SMS[délka_HODNOTA + 5] = 's';
        Velikost = uživatelský_prostor.파일읽기(název_souboru_SMS, název_souboru);
        if (Velikost < 0) { uživatelský_prostor.Zápis("java: cannot read class: "); 자바도구.zápis_číslo(Velikost); uživatelský_prostor.zápis_znak_HODNOTA(10); return 1; }
        클래스읽기(); if (chyba) return 1;
        int znak_název = konstanta_SMS(název_třídy);
        if (!chyba && halda_HODNOTA[znak_název + 1] != délka_HODNOTA) selhání_HODNOTA("class name does not match file");
        for (int číslo = 0; číslo < délka_HODNOTA && !chyba; číslo++) if (halda_HODNOTA[znak_název + 2 + číslo] != název_souboru_SMS[číslo]) selhání_HODNOTA("class name does not match file");
        int vstupní_bod_HODNOTA = -1;
        for (int číslo = 0; číslo < metoda_POČET; číslo++) if (Word_SMS(metoda_název_SMS[číslo], "main") && Word_SMS(metoda_TYP[číslo], "([Ljava/lang/String;)V") && (metoda_přístup[číslo] & 9) == 9) vstupní_bod_HODNOTA = číslo;
        if (vstupní_bod_HODNOTA < 0) selhání_HODNOTA("public static void main(String[] args) required");
        if (chyba) return 1;
        int argumenty = přidělit_Storage(3, uživatelský_prostor.인수개수() - 1);
        for (int číslo = 1; číslo < uživatelský_prostor.인수개수() && !chyba; číslo++) halda_HODNOTA[argumenty + 1 + číslo] = hostit_znak(uživatelský_prostor.argumenty(číslo));
        rámec_INDEX = 0; rámec_metoda[0] = vstupní_bod_HODNOTA; rámec_pozice[0] = metoda_START[vstupní_bod_HODNOTA]; místní_HODNOTA[0] = argumenty; místní_TYP[0] = 2;
        Provést_příkaz(); return chyba ? 1 : 0;
    }
}
