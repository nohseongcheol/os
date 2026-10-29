// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. název_souboru/operand_Štos/odkaz/větev 경계를 Provést_příkaz 중 검사한다. */
public final class 자바가상기계 {
    static int[] název_souboru = new int[16 * 16384], dočasný_soubor = new int[16384], název_souboru_SMS = new int[512];
    static int[] konstanta_značka = new int[8192], 상가 = new int[8192], konstanta_SEKUNDA_HODNOTA = new int[8192], řetězec_odkaz = new int[8192];
    static int[] metoda_název_SMS = new int[512], metoda_TYP = new int[512], metoda_přístup = new int[512], metoda_vlastník = new int[512];
    static int[] metoda_START = new int[512], metoda_konec = new int[512], metoda_Štos = new int[512], 함수지역 = new int[512];
    static int[] metoda_argument_POČET = new int[512], metoda_argument_TYP = new int[8192], metoda_Vratka = new int[512];
    static int[] mez_HODNOTA = new int[16 * 16384];
    static int[] místní_HODNOTA = new int[16384], místní_TYP = new int[16384], operand_Štos_HODNOTA = new int[16384], operand_Štos_TYP = new int[16384];
    static int[] rámec_metoda = new int[128], rámec_pozice = new int[128], rámec_Štos = new int[128], 틀명령 = new int[128], inicializovat_rámec = new int[128];
    static int[] Třída_Definice_název = new int[16], Třída_Definice_změnit_velikost = new int[16], Třída_Definice_nadřazený = new int[16], Třída_Definice_Stav = new int[16], Třída_přihrádka_POČET = new int[16], inicializovat_Třída_Definice = new int[16];
    static int[] Třída_rozhraní = new int[16 * 16], Třída_rozhraní_POČET = new int[16];
    static int[] přihrádka_název = new int[512], přihrádka_TYP = new int[512], přihrádka_vlastník = new int[512], přihrádka_Oprávnění = new int[512], přihrádka_pozice = new int[512], přihrádka_data = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] halda_HODNOTA = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], halda_odkaz = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], prvek_pole = new int[32768], Store_integer = new int[256];
    static int Velikost, 읽기위치, metoda_POČET, název_třídy, rámec_INDEX = -1, halda_konec_pozice = 1, návratový_typ;
    static int Třída_Definice_POČET, přihrádka_POČET, 잡기수, 현재읽는종, 던진객체, 잠시수, displej_POČET, inkaso_POČET;
    static int dobrá_vlákno, počet_vláken = 1, položka_Třída_Definice;
    static int[] vlákno_rámec = new int[4], vlákno_Stav = new int[4], vlákno_objekt = new int[4], vlákno_cíl = new int[4], 가닥대기 = new int[4];
    static boolean chyba, žádost_o_změnu;
    static int[] zámek_vlastník = new int[32768], 잠금깊이 = new int[32768], rámec_zámek = new int[128], Třída_zámek = new int[16], Třída_vlákno = new int[16];

    static void selhání_HODNOTA(String Word_SMS) {
        if (chyba) return;
        int oblast_KÓD = 0;
        if (자바도구.같음(Word_SMS, "ArithmeticException: / by zero")) oblast_KÓD = 4;
        if (자바도구.같음(Word_SMS, "NullPointerException") || 자바도구.같음(Word_SMS, "null or invalid array")) oblast_KÓD = 5;
        if (자바도구.같음(Word_SMS, "ArrayIndexOutOfBoundsException")) oblast_KÓD = 7;
        if (자바도구.같음(Word_SMS, "StringIndexOutOfBoundsException")) oblast_KÓD = 8;
        if (자바도구.같음(Word_SMS, "NumberFormatException")) oblast_KÓD = 10;
        if (자바도구.같음(Word_SMS, "FileNotFoundException: file open failed")) oblast_KÓD = 12;
        if (자바도구.같음(Word_SMS, "IOException: stream closed") || 자바도구.같음(Word_SMS, "IOException: read failed") || 자바도구.같음(Word_SMS, "IOException: write failed")) oblast_KÓD = 11;
        if (자바도구.같음(Word_SMS, "ClassCastException")) oblast_KÓD = 14;
        if (자바도구.같음(Word_SMS, "NegativeArraySizeException")) oblast_KÓD = 15;
        if (oblast_KÓD != 0 && rámec_INDEX >= 0) { 예외던짐(oblast_KÓD, Word_SMS); return; }
        uživatelský_prostor.Zápis("JVM error: "); uživatelský_prostor.Zápis(Word_SMS); uživatelský_prostor.zápis_znak_HODNOTA(10); chyba = true;
    }
    static boolean oříznout(int Spustit_2, int délka_HODNOTA) {
        if (Spustit_2 < 0 || Spustit_2 >= název_souboru.length || délka_HODNOTA < 0) return false;
        int Třída_Definice = Spustit_2 / 16384;
        return Spustit_2 % 16384 <= Třída_Definice_změnit_velikost[Třída_Definice] && délka_HODNOTA <= Třída_Definice_změnit_velikost[Třída_Definice] - Spustit_2 % 16384;
    }
    static int bajt_HODNOTA() {
        if (!oříznout(읽기위치, 1)) { selhání_HODNOTA("truncated class file"); return 0; }
        return název_souboru[읽기위치++];
    }
    static int 짧은수() { return bajt_HODNOTA() << 8 | bajt_HODNOTA(); }
    static int integer() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int délka_HODNOTA) { if (!oříznout(읽기위치, délka_HODNOTA)) selhání_HODNOTA("invalid attribute size"); else 읽기위치 += délka_HODNOTA; }
    static boolean šek_konstanta(int číslo, int Druh_HODNOTA) {
        if (číslo <= 0 || číslo >= konstanta_značka.length || konstanta_značka[číslo] != Druh_HODNOTA) { selhání_HODNOTA("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean SMS_oblast(int Spustit_2, int délka_HODNOTA, String Word_SMS) {
        if (!oříznout(Spustit_2, délka_HODNOTA)) return false;
        int 읽는자리 = Spustit_2, 끝 = Spustit_2 + délka_HODNOTA;
        for (int Loop_INDEX = 0; Loop_INDEX < Word_SMS.length(); Loop_INDEX++) {
            int bod_kódu = Word_SMS.charAt(Loop_INDEX);
            if (bod_kódu > 0 && bod_kódu < 128) { if (읽는자리 >= 끝 || název_souboru[읽는자리++] != bod_kódu) return false; }
            else if (bod_kódu < 2048) {
                if (읽는자리 + 2 > 끝 || název_souboru[읽는자리++] != (192 | (bod_kódu >> 6)) || název_souboru[읽는자리++] != (128 | (bod_kódu & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || název_souboru[읽는자리++] != (224 | (bod_kódu >> 12)) || název_souboru[읽는자리++] != (128 | ((bod_kódu >> 6) & 63)) || název_souboru[읽는자리++] != (128 | (bod_kódu & 63))) return false;
        }
        return 읽는자리 == 끝;
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
    static int 상번호() { int HODNOTA = 짧은수(); return HODNOTA == 0 ? 0 : 현재읽는종 * 512 + HODNOTA; }
    static int 명상수() { return metoda_vlastník[rámec_metoda[rámec_INDEX]] * 512 + 명짧(); }
    static void přeskočit_atribut() {
        int zboží_POČET = 짧은수();
        for (int číslo = 0; číslo < zboží_POČET && !chyba; číslo++) { šek_konstanta(상번호(), 1); 건너(integer()); }
    }
    static int příkaz_délka(int HODNOTA) {
        if (HODNOTA == 16 || HODNOTA == 18 || HODNOTA == 21 || HODNOTA == 25 || HODNOTA == 54 || HODNOTA == 58 || HODNOTA == 188) return 2;
        if (HODNOTA == 17 || HODNOTA == 19 || HODNOTA == 132 || HODNOTA >= 153 && HODNOTA <= 167
            || HODNOTA >= 178 && HODNOTA <= 184 || HODNOTA == 187 || HODNOTA == 189 || HODNOTA == 192 || HODNOTA == 193 || HODNOTA == 198 || HODNOTA == 199) return 3;
        if (HODNOTA == 185 || HODNOTA == 200) return 5;
        if (HODNOTA >= 0 && HODNOTA <= 8 || HODNOTA >= 26 && HODNOTA <= 29 || HODNOTA >= 42 && HODNOTA <= 46 || HODNOTA >= 50 && HODNOTA <= 53
            || HODNOTA >= 59 && HODNOTA <= 62 || HODNOTA >= 75 && HODNOTA <= 79 || HODNOTA >= 83 && HODNOTA <= 95
            || HODNOTA == 96 || HODNOTA == 100 || HODNOTA == 104 || HODNOTA == 108 || HODNOTA == 112 || HODNOTA == 116
            || HODNOTA == 120 || HODNOTA == 122 || HODNOTA == 124 || HODNOTA == 126 || HODNOTA == 128 || HODNOTA == 130
            || HODNOTA >= 145 && HODNOTA <= 147 || HODNOTA == 172 || HODNOTA == 176 || HODNOTA == 177 || HODNOTA == 190 || HODNOTA == 191
            || HODNOTA == 194 || HODNOTA == 195) return 1;
        return 0;
    }
    static int pozice_integer(int 읽는자리) {
        if (!oříznout(읽는자리, 4)) { selhání_HODNOTA("truncated bytecode operand"); return 0; }
        return název_souboru[읽는자리] << 24 | název_souboru[읽는자리 + 1] << 16 | název_souboru[읽는자리 + 2] << 8 | název_souboru[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int Spustit_2, int 끝) {
        int HODNOTA = název_souboru[읽는자리], délka_HODNOTA = příkaz_délka(HODNOTA);
        if (HODNOTA == 170 || HODNOTA == 171) {
            int BASE_pozice = 읽는자리 + 1;
            while ((BASE_pozice - Spustit_2) % 4 != 0) BASE_pozice++;
            if (끝 - BASE_pozice < (HODNOTA == 170 ? 12 : 8)) return 0;
            int položka_POČET = HODNOTA == 170 ? pozice_integer(BASE_pozice + 8) - pozice_integer(BASE_pozice + 4) + 1 : pozice_integer(BASE_pozice + 4);
            if (položka_POČET < 0 || položka_POČET > 2048) return 0;
            délka_HODNOTA = BASE_pozice - 읽는자리 + (HODNOTA == 170 ? 12 + 4 * položka_POČET : 8 + 8 * položka_POČET);
        }
        if (HODNOTA == 196 && 읽는자리 + 1 < 끝) {
            int Word_data = název_souboru[읽는자리 + 1]; délka_HODNOTA = Word_data == 132 ? 6 : (Word_data == 21 || Word_data == 25 || Word_data == 54 || Word_data == 58) ? 4 : 0;
        }
        return délka_HODNOTA > 0 && délka_HODNOTA <= 끝 - 읽는자리 ? délka_HODNOTA : 0;
    }
    static void šek_cíl_HODNOTA(int cíl_HODNOTA, int funkce_HODNOTA) {
        if (cíl_HODNOTA < metoda_START[funkce_HODNOTA] || cíl_HODNOTA >= metoda_konec[funkce_HODNOTA] || mez_HODNOTA[cíl_HODNOTA] != funkce_HODNOTA + 1) selhání_HODNOTA("invalid branch target");
    }
    static void 클래스읽기(int Třída_Definice) {
        현재읽는종 = Třída_Definice; 읽기위치 = Třída_Definice * 16384; Velikost = 읽기위치 + Třída_Definice_změnit_velikost[Třída_Definice];
        if (integer() != 0xcafebabe) { selhání_HODNOTA("not a class file"); return; }
        int 부판 = 짧은수(), verze_HODNOTA = 짧은수();
        if (verze_HODNOTA < 45 || verze_HODNOTA > 52 || 부판 != 0) { selhání_HODNOTA("supported class versions: 45..52, minor 0"); return; }
        int konstanta_POČET = 짧은수(), BASE_pozice = Třída_Definice * 512;
        if (konstanta_POČET < 1 || konstanta_POČET > 512) { selhání_HODNOTA("constant pool limit (511)"); return; }
        for (int položka_POČET = 1; položka_POČET < konstanta_POČET && !chyba; položka_POČET++) {
            int číslo = BASE_pozice + položka_POČET, Druh_HODNOTA = bajt_HODNOTA(); konstanta_značka[číslo] = Druh_HODNOTA;
            if (Druh_HODNOTA == 1) { konstanta_SEKUNDA_HODNOTA[číslo] = 짧은수(); 상가[číslo] = 읽기위치; 건너(konstanta_SEKUNDA_HODNOTA[číslo]); }
            else if (Druh_HODNOTA == 3) 상가[číslo] = integer();
            else if (Druh_HODNOTA == 7 || Druh_HODNOTA == 8) 상가[číslo] = 상번호();
            else if (Druh_HODNOTA == 9 || Druh_HODNOTA == 10 || Druh_HODNOTA == 11 || Druh_HODNOTA == 12) { 상가[číslo] = 상번호(); konstanta_SEKUNDA_HODNOTA[číslo] = 상번호(); }
            else selhání_HODNOTA("unsupported constant type");
        }
        int oprávnění_HODNOTA = 짧은수();
        if ((oprávnění_HODNOTA & (0x2000 | 0x4000)) != 0) selhání_HODNOTA("annotation/enum class unsupported");
        Třída_Definice_název[Třída_Definice] = název_třídy_SMS(상번호());
        Třída_Definice_nadřazený[Třída_Definice] = název_třídy_SMS(상번호());
        int rozhraní_POČET = 짧은수(); if (rozhraní_POČET > 16) { selhání_HODNOTA("interface count limit"); return; }
        Třída_rozhraní_POČET[Třída_Definice] = rozhraní_POČET;
        for (int Loop_INDEX = 0; Loop_INDEX < rozhraní_POČET; Loop_INDEX++) Třída_rozhraní[Třída_Definice * 16 + Loop_INDEX] = název_třídy_SMS(상번호());
        int pole_POČET = 짧은수();
        if (pole_POČET > 512 - přihrádka_POČET) { selhání_HODNOTA("field count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < pole_POČET && !chyba; Loop_INDEX++) {
            int Soubor_INDEX = přihrádka_POČET++; přihrádka_vlastník[Soubor_INDEX] = Třída_Definice; přihrádka_Oprávnění[Soubor_INDEX] = 짧은수(); přihrádka_název[Soubor_INDEX] = 상번호(); přihrádka_TYP[Soubor_INDEX] = 상번호();
            šek_konstanta(přihrádka_název[Soubor_INDEX], 1); šek_konstanta(přihrádka_TYP[Soubor_INDEX], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[přihrádka_TYP[Soubor_INDEX]]; int oblast_KÓD = popisovač_TYP(읽기위치 + konstanta_SEKUNDA_HODNOTA[přihrádka_TYP[Soubor_INDEX]], false); 읽기위치 = 보존값;
            if ((přihrádka_Oprávnění[Soubor_INDEX] & 8) == 0) přihrádka_pozice[Soubor_INDEX] = Třída_přihrádka_POČET[Třída_Definice]++;
            int atribut_data = 짧은수();
            for (int vnitřní_pozice = 0; vnitřní_pozice < atribut_data && !chyba; vnitřní_pozice++) {
                int název_konstanta = 상번호(), platný_délka = integer();
                if (Word_SMS(název_konstanta, "ConstantValue") && platný_délka == 2) {
                    int data_HODNOTA = 상번호();
                    if (oblast_KÓD == 1 && šek_konstanta(data_HODNOTA, 3)) přihrádka_data[Soubor_INDEX] = 상가[data_HODNOTA];
                    else if (oblast_KÓD == 2 && šek_konstanta(data_HODNOTA, 8)) přihrádka_data[Soubor_INDEX] = konstanta_SMS(상가[data_HODNOTA]);
                } else 건너(platný_délka);
            }
        }
        int zboží_POČET = 짧은수();
        if (zboží_POČET > 512 - metoda_POČET) { selhání_HODNOTA("method count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < zboží_POČET && !chyba; Loop_INDEX++) {
            int číslo = metoda_POČET++; metoda_vlastník[číslo] = Třída_Definice;
            metoda_přístup[číslo] = 짧은수(); metoda_název_SMS[číslo] = 상번호(); metoda_TYP[číslo] = 상번호();
            šek_konstanta(metoda_název_SMS[číslo], 1); 서술읽기(číslo);
            if ((metoda_přístup[číslo] & 8) == 0) {
                if (metoda_argument_POČET[číslo] == 16) { selhání_HODNOTA("too many instance method arguments"); return; }
                for (int Porovnání_pozice = metoda_argument_POČET[číslo]; Porovnání_pozice > 0; Porovnání_pozice--) metoda_argument_TYP[číslo * 16 + Porovnání_pozice] = metoda_argument_TYP[číslo * 16 + Porovnání_pozice - 1];
                metoda_argument_TYP[číslo * 16] = 2; metoda_argument_POČET[číslo]++;
            }
            if ((metoda_přístup[číslo] & 0x100) != 0) selhání_HODNOTA("user native method unsupported");
            if (Word_SMS(metoda_název_SMS[číslo], "<clinit>")) inicializovat_Třída_Definice[Třída_Definice] = číslo + 1;
            for (int přední_fotoaparát_HODNOTA = 0; přední_fotoaparát_HODNOTA < číslo; přední_fotoaparát_HODNOTA++) if (metoda_vlastník[přední_fotoaparát_HODNOTA] == Třída_Definice && 같은말(metoda_název_SMS[přední_fotoaparát_HODNOTA], metoda_název_SMS[číslo]) && 같은말(metoda_TYP[přední_fotoaparát_HODNOTA], metoda_TYP[číslo])) selhání_HODNOTA("duplicate method");
            int atribut_POČET = 짧은수();
            for (int hodnota_atributu = 0; hodnota_atributu < atribut_POČET && !chyba; hodnota_atributu++) {
                int Název = 상번호(), délka_HODNOTA = integer(), Spustit_2 = 읽기위치;
                if (!oříznout(Spustit_2, délka_HODNOTA)) { selhání_HODNOTA("truncated method attribute"); break; }
                if (Word_SMS(Název, "Code")) {
                    if (metoda_START[číslo] != 0) selhání_HODNOTA("duplicate Code attribute");
                    metoda_Štos[číslo] = 짧은수(); 함수지역[číslo] = 짧은수(); int KÓD_délka = integer();
                    if (metoda_Štos[číslo] > 128 || 함수지역[číslo] > 128 || 함수지역[číslo] < metoda_argument_POČET[číslo]
                        || KÓD_délka < 1 || KÓD_délka > 8192) selhání_HODNOTA("method memory limits exceeded");
                    metoda_START[číslo] = 읽기위치; 건너(KÓD_délka); metoda_konec[číslo] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { selhání_HODNOTA("exception table limit"); return; }
                    for (int vnitřní_pozice = 0; vnitřní_pozice < 잡는수; vnitřní_pozice++) {
                        int chyba_odkaz = 잡기수++; 잡기함수[chyba_odkaz] = číslo;
                        잡기시작[chyba_odkaz] = metoda_START[číslo] + 짧은수(); 잡기끝[chyba_odkaz] = metoda_START[číslo] + 짧은수();
                        잡기위치[chyba_odkaz] = metoda_START[číslo] + 짧은수(); int 부호값 = 상번호(); 잡기종[chyba_odkaz] = 부호값 == 0 ? 0 : název_třídy_SMS(부호값);
                    }
                    přeskočit_atribut();
                    if (읽기위치 != Spustit_2 + délka_HODNOTA) selhání_HODNOTA("Code attribute size mismatch");
                } else 건너(délka_HODNOTA);
            }
            if ((metoda_přístup[číslo] & 0x400) != 0) continue;
            if (metoda_START[číslo] == 0) selhání_HODNOTA("missing Code attribute");
            int přihrádka_položka = metoda_START[číslo];
            while (přihrádka_položka < metoda_konec[číslo] && !chyba) {
                int délka_HODNOTA = 길이읽기(přihrádka_položka, metoda_START[číslo], metoda_konec[číslo]);
                if (délka_HODNOTA == 0) { selhání_HODNOTA("unsupported or truncated bytecode"); break; }
                mez_HODNOTA[přihrádka_položka] = číslo + 1; přihrádka_položka += délka_HODNOTA;
            }
            přihrádka_položka = metoda_START[číslo];
            while (přihrádka_položka < metoda_konec[číslo] && !chyba) {
                int HODNOTA = název_souboru[přihrádka_položka];
                if (HODNOTA >= 153 && HODNOTA <= 167 || HODNOTA == 198 || HODNOTA == 199) šek_cíl_HODNOTA(přihrádka_položka + (short)(název_souboru[přihrádka_položka + 1] << 8 | název_souboru[přihrádka_položka + 2]), číslo);
                if (HODNOTA == 200) šek_cíl_HODNOTA(přihrádka_položka + pozice_integer(přihrádka_položka + 1), číslo);
                if (HODNOTA == 170 || HODNOTA == 171) {
                    int 읽는자리 = přihrádka_položka + 1; while ((읽는자리 - metoda_START[číslo]) % 4 != 0) 읽는자리++;
                    šek_cíl_HODNOTA(přihrádka_položka + pozice_integer(읽는자리), číslo);
                    int položka_POČET = HODNOTA == 170 ? pozice_integer(읽는자리 + 8) - pozice_integer(읽는자리 + 4) + 1 : pozice_integer(읽는자리 + 4);
                    읽는자리 += HODNOTA == 170 ? 12 : 8;
                    for (int vnitřní_pozice = 0; vnitřní_pozice < položka_POČET; vnitřní_pozice++) šek_cíl_HODNOTA(přihrádka_položka + pozice_integer(읽는자리 + vnitřní_pozice * (HODNOTA == 170 ? 4 : 8) + (HODNOTA == 170 ? 0 : 4)), číslo);
                }
                přihrádka_položka += 길이읽기(přihrádka_položka, metoda_START[číslo], metoda_konec[číslo]);
            }
            for (int vnitřní_pozice = 0; vnitřní_pozice < 잡기수; vnitřní_pozice++) if (잡기함수[vnitřní_pozice] == číslo) {
                šek_cíl_HODNOTA(잡기시작[vnitřní_pozice], číslo); šek_cíl_HODNOTA(잡기위치[vnitřní_pozice], číslo);
                if (잡기끝[vnitřní_pozice] != metoda_konec[číslo]) šek_cíl_HODNOTA(잡기끝[vnitřní_pozice], číslo);
                if (잡기시작[vnitřní_pozice] >= 잡기끝[vnitřní_pozice]) selhání_HODNOTA("invalid exception range");
            }
        }
        if (!chyba) přeskočit_atribut();
        if (읽기위치 != Velikost) selhání_HODNOTA("extra class file data");
    }
    static int přidělit_Storage(int Druh_HODNOTA, int délka_HODNOTA) { return 새기억(Druh_HODNOTA, délka_HODNOTA); }
    static boolean objekt_HODNOTA(int odkaz, int Druh_HODNOTA) {
        if (!informační_systémy_platný_objekt(odkaz)) return false;
        if (halda_HODNOTA[odkaz] != Druh_HODNOTA) { selhání_HODNOTA("object type mismatch"); return false; }
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
        if (návratový_typ == 2) chránit_HODNOTA(operand_Štos_HODNOTA[přihrádka_položka]);
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
        if (rámec_INDEX % 32 == 31) { selhání_HODNOTA("call stack limit (32)"); return; }
        int Další_zboží = rámec_INDEX + 1;
        for (int číslo = 0; číslo < 128; číslo++) místní_TYP[Další_zboží * 128 + číslo] = 0;
        for (int číslo = metoda_argument_POČET[funkce_HODNOTA] - 1; číslo >= 0; číslo--) {
            místní_HODNOTA[Další_zboží * 128 + číslo] = 빼기(metoda_argument_TYP[funkce_HODNOTA * 16 + číslo]); místní_TYP[Další_zboží * 128 + číslo] = metoda_argument_TYP[funkce_HODNOTA * 16 + číslo];
        }
        if (chyba) return;
        rámec_INDEX = Další_zboží; inicializovat_rámec[rámec_INDEX] = 0; rámec_metoda[rámec_INDEX] = funkce_HODNOTA; rámec_pozice[rámec_INDEX] = metoda_START[funkce_HODNOTA]; rámec_Štos[rámec_INDEX] = 0;
    }
    static void Vratka_KV(int TYP_HODNOTA) {
        if (TYP_HODNOTA != metoda_Vratka[rámec_metoda[rámec_INDEX]]) { selhání_HODNOTA("return type mismatch"); return; }
        int HODNOTA = TYP_HODNOTA == 0 ? 0 : 빼기(TYP_HODNOTA);
        if (inicializovat_rámec[rámec_INDEX] != 0) Třída_Definice_Stav[inicializovat_rámec[rámec_INDEX] - 1] = 2;
        if (rámec_zámek[rámec_INDEX] != 0) { verze_zámek(rámec_zámek[rámec_INDEX]); rámec_zámek[rámec_INDEX] = 0; }
        rámec_INDEX--; if (rámec_INDEX >= dobrá_vlákno * 32 && TYP_HODNOTA != 0) 넣기(HODNOTA, TYP_HODNOTA);
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
                if (HODNOTA < 1) { selhání_HODNOTA("invalid file stream path"); return; }
                tok_název_souboru[přihrádka_položka] = HODNOTA;
            }
            tok_název_souboru[délka_HODNOTA] = 0;
            int popisovač_položka = uživatelský_prostor.otevřít_Soubor_popisovač(tok_název_souboru, výstupní_pozice ? (이어 ? 1089 : 577) : 0);
            if (popisovač_položka < 0) { selhání_HODNOTA("FileNotFoundException: file open failed"); return; }
            halda_HODNOTA[tok_HODNOTA + 2] = popisovač_položka; halda_HODNOTA[tok_HODNOTA + 3] = 1;
            return;
        }
        if (příkaz != 182) { selhání_HODNOTA("invalid file stream invocation"); return; }
        if ((výstupní_pozice && Word_SMS(Název, "write") || !výstupní_pozice && Word_SMS(Název, "read"))
            && (Word_SMS(formát_HODNOTA, výstupní_pozice ? "([B)V" : "([B)I") || Word_SMS(formát_HODNOTA, výstupní_pozice ? "([BII)V" : "([BII)I"))) {
            boolean oříznout_HODNOTA = Word_SMS(formát_HODNOTA, výstupní_pozice ? "([BII)V" : "([BII)I");
            int položka_POČET = oříznout_HODNOTA ? 빼기(1) : 0, 시작점 = oříznout_HODNOTA ? 빼기(1) : 0, data_pole = 빼기(2), objekt_odkaz = 빼기(2);
            if (!objekt_HODNOTA(data_pole, 20) || !objekt_HODNOTA(objekt_odkaz, Druh_HODNOTA)) return;
            if (!oříznout_HODNOTA) položka_POČET = halda_HODNOTA[data_pole + 1];
            if (시작점 < 0 || položka_POČET < 0 || 시작점 > halda_HODNOTA[data_pole + 1] - položka_POČET) { 예외던짐(6, "file buffer bounds"); return; }
            if (halda_HODNOTA[objekt_odkaz + 3] == 0 || halda_HODNOTA[objekt_odkaz + 2] < 0) { selhání_HODNOTA("IOException: stream closed"); return; }
            int dokončeno_POČET = 0;
            while (dokončeno_POČET < položka_POČET && !chyba) {
                int 반환값 = výstupní_pozice ? uživatelský_prostor.파일한바이트쓰기(halda_HODNOTA[objekt_odkaz + 2], halda_HODNOTA[data_pole + 2 + 시작점 + dokončeno_POČET]) : uživatelský_prostor.파일한바이트읽기(halda_HODNOTA[objekt_odkaz + 2]);
                if (반환값 < 0) { selhání_HODNOTA(výstupní_pozice ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!výstupní_pozice && 반환값 == 256) break;
                if (!výstupní_pozice) halda_HODNOTA[data_pole + 2 + 시작점 + dokončeno_POČET] = (byte)반환값;
                dokončeno_POČET++;
            }
            if (!výstupní_pozice) 넣기(položka_POČET != 0 && dokončeno_POČET == 0 ? -1 : dokončeno_POČET, 1);
            return;
        }
        if (výstupní_pozice && Word_SMS(Název, "flush") && Word_SMS(formát_HODNOTA, "()V")) { int objekt_odkaz = 빼기(2); if (objekt_HODNOTA(objekt_odkaz, Druh_HODNOTA) && halda_HODNOTA[objekt_odkaz + 2] < 0) selhání_HODNOTA("IOException: stream closed"); return; }
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
            if (VÝSLEDEK < -1) selhání_HODNOTA("IOException: read failed"); else 넣기(VÝSLEDEK == 256 ? -1 : VÝSLEDEK, 1);
        } else if (uživatelský_prostor.파일한바이트쓰기(popisovač_položka, HODNOTA) != 1) selhání_HODNOTA("IOException: write failed");
    }
    static void VOLAT_metoda(int INDEX, int příkaz) {
        if (INDEX <= 0 || INDEX >= konstanta_značka.length || (konstanta_značka[INDEX] != 10 && konstanta_značka[INDEX] != 11)) { selhání_HODNOTA("invalid method reference"); return; }
        int vlastník_HODNOTA = název_třídy_SMS(상가[INDEX]), Název = odkaz_název(konstanta_SEKUNDA_HODNOTA[INDEX]), formát_HODNOTA = odkaz_c74caca7(konstanta_SEKUNDA_HODNOTA[INDEX]);
        if (chyba) return;
        if (기본호출(vlastník_HODNOTA, Název, formát_HODNOTA, příkaz)) return;
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
        int Třída_Definice = NAJÍT_Třída_Definice(vlastník_HODNOTA); if (Třída_Definice < 0 || chyba) return;
        int Soubor_INDEX = NAJÍT_metoda(Třída_Definice, Název, formát_HODNOTA);
        if (Soubor_INDEX < 0) {
            for (int bod_kódu = Třída_Definice, položka_POČET = 0; bod_kódu >= 0 && položka_POČET < 16; položka_POČET++, bod_kódu = nadřazený_Třída(bod_kódu))
                if (Word_SMS(Třída_Definice_nadřazený[bod_kódu], "java/lang/Thread")) { 가닥호출(Název, formát_HODNOTA, příkaz); return; }
            selhání_HODNOTA("NoSuchMethodError"); return;
        }
        if (((metoda_přístup[Soubor_INDEX] & 8) != 0) != (příkaz == 184)) { selhání_HODNOTA("method static/instance mismatch"); return; }
        if (příkaz == 184) { if (!inicializovat(metoda_vlastník[Soubor_INDEX], 틀명령[rámec_INDEX])) return; }
        else {
            int 읽는자리 = rámec_Štos[rámec_INDEX] - metoda_argument_POČET[Soubor_INDEX];
            if (읽는자리 < 0 || operand_Štos_TYP[rámec_INDEX * 128 + 읽는자리] != 2) { selhání_HODNOTA("invalid method receiver"); return; }
            int objekt_odkaz = operand_Štos_HODNOTA[rámec_INDEX * 128 + 읽는자리];
            if (!informační_systémy_platný_objekt(objekt_odkaz)) return;
            if (halda_HODNOTA[objekt_odkaz] < 32 || !종포함(halda_HODNOTA[objekt_odkaz] - 32, vlastník_HODNOTA)) { selhání_HODNOTA("method receiver type mismatch"); return; }
            if (příkaz != 183) Soubor_INDEX = NAJÍT_metoda(halda_HODNOTA[objekt_odkaz] - 32, Název, formát_HODNOTA);
        }
        if (Soubor_INDEX < 0 || (metoda_přístup[Soubor_INDEX] & 0x400) != 0) { selhání_HODNOTA("AbstractMethodError"); return; }
        int zámek_odkaz = 0;
        if ((metoda_přístup[Soubor_INDEX] & 32) != 0) {
            if (příkaz == 184) { int bod_kódu = metoda_vlastník[Soubor_INDEX]; if (Třída_zámek[bod_kódu] == 0) Třída_zámek[bod_kódu] = přidělit_Storage(8, 0); zámek_odkaz = Třída_zámek[bod_kódu]; }
            else zámek_odkaz = operand_Štos_HODNOTA[rámec_INDEX * 128 + rámec_Štos[rámec_INDEX] - metoda_argument_POČET[Soubor_INDEX]];
            if (!잠금얻기(zámek_odkaz)) { if (!chyba) rámec_pozice[rámec_INDEX] = 틀명령[rámec_INDEX]; return; }
        }
        호출(Soubor_INDEX); if (!chyba) rámec_zámek[rámec_INDEX] = zámek_odkaz;
    }
    static boolean 배열저장가능(int pole_odkaz, int data_HODNOTA) {
        if (data_HODNOTA == 0 || prvek_pole[pole_odkaz] == 0) return true;
        boolean 성공여부 = prvek_pole[pole_odkaz] == -1 ? (data_HODNOTA > 0 && data_HODNOTA < halda_konec_pozice && halda_HODNOTA[data_HODNOTA] == 1) : 맞는객체(data_HODNOTA, prvek_pole[pole_odkaz]);
        if (!성공여부 && !chyba) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int pole_přihrádka(int odkaz, int dolní_index_HODNOTA, int TYP_HODNOTA) {
        if (!objekt_HODNOTA(odkaz, TYP_HODNOTA)) return 0;
        if (dolní_index_HODNOTA < 0 || dolní_index_HODNOTA >= halda_HODNOTA[odkaz + 1]) { selhání_HODNOTA("ArrayIndexOutOfBoundsException"); return 0; }
        return odkaz + 2 + dolní_index_HODNOTA;
    }
    static void Provést_příkaz() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (chyba) { if (던진객체 != 0) úchyt_výjimka(); if (chyba || rámec_INDEX < dobrá_vlákno * 32) break; }
            if (rámec_INDEX < dobrá_vlákno * 32 || žádost_o_změnu || --조각 == 0) { if (!SWITCH_vlákno()) break; 조각 = 100; }
            if (rámec_INDEX == 0 && Třída_Definice_Stav[položka_Třída_Definice] != 2 && !inicializovat(položka_Třída_Definice, rámec_pozice[rámec_INDEX])) continue;
            if (rámec_INDEX == dobrá_vlákno * 32 && dobrá_vlákno != 0 && (metoda_přístup[rámec_metoda[rámec_INDEX]] & 32) != 0 && rámec_zámek[rámec_INDEX] == 0) {
                int objekt_odkaz = vlákno_cíl[dobrá_vlákno]; if (!잠금얻기(objekt_odkaz)) { if (chyba) break; continue; } rámec_zámek[rámec_INDEX] = objekt_odkaz;
            }
            잠시수 = 0;
            if (--남음 == 0) { selhání_HODNOTA("instruction limit (500000)"); break; }
            int Spustit_2 = rámec_pozice[rámec_INDEX]; 틀명령[rámec_INDEX] = Spustit_2; int HODNOTA = 명바();
            if (chyba) break;
            if (HODNOTA == 0) continue;
            if (HODNOTA == 1) { 넣기(0, 2); continue; }
            if (HODNOTA >= 2 && HODNOTA <= 8) { 넣기(HODNOTA - 3, 1); continue; }
            if (HODNOTA == 16) { 넣기((byte)명바(), 1); continue; }
            if (HODNOTA == 17) { 넣기((short)명짧(), 1); continue; }
            if (HODNOTA == 18 || HODNOTA == 19) {
                int číslo = metoda_vlastník[rámec_metoda[rámec_INDEX]] * 512 + (HODNOTA == 18 ? 명바() : 명짧());
                if (číslo <= 0 || číslo >= konstanta_značka.length) selhání_HODNOTA("invalid ldc constant");
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
            if (HODNOTA == 46 || HODNOTA >= 50 && HODNOTA <= 53) {
                int položka_pozice = 빼기(1), objekt_odkaz = 빼기(2), oblast_KÓD = HODNOTA == 46 ? 2 : HODNOTA == 50 ? 3 : HODNOTA == 51 ? 20 : HODNOTA == 52 ? 22 : 23;
                if (HODNOTA == 51 && objekt_odkaz > 0 && objekt_odkaz < halda_konec_pozice && halda_HODNOTA[objekt_odkaz] == 21) oblast_KÓD = 21;
                int 읽는자리 = pole_přihrádka(objekt_odkaz, položka_pozice, oblast_KÓD); if (!chyba) 넣기(halda_HODNOTA[읽는자리], HODNOTA == 50 ? 2 : 1); continue;
            }
            if (HODNOTA == 79 || HODNOTA >= 83 && HODNOTA <= 86) {
                int položka_odkaz = 빼기(HODNOTA == 83 ? 2 : 1), položka_pozice = 빼기(1), objekt_odkaz = 빼기(2), oblast_KÓD = HODNOTA == 79 ? 2 : HODNOTA == 83 ? 3 : HODNOTA == 84 ? 20 : HODNOTA == 85 ? 22 : 23;
                if (HODNOTA == 84 && objekt_odkaz > 0 && objekt_odkaz < halda_konec_pozice && halda_HODNOTA[objekt_odkaz] == 21) oblast_KÓD = 21;
                int 읽는자리 = pole_přihrádka(objekt_odkaz, položka_pozice, oblast_KÓD);
                if (!chyba && oblast_KÓD == 3 && !배열저장가능(objekt_odkaz, položka_odkaz)) continue;
                if (!chyba) halda_HODNOTA[읽는자리] = oblast_KÓD == 20 ? (byte)položka_odkaz : oblast_KÓD == 21 ? položka_odkaz & 1 : oblast_KÓD == 22 ? (char)položka_odkaz : oblast_KÓD == 23 ? (short)položka_odkaz : položka_odkaz;
                continue;
            }
            if (HODNOTA >= 87 && HODNOTA <= 95) { 스택명령(HODNOTA); continue; }
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
            if (HODNOTA >= 178 && HODNOTA <= 181) { 필드호출(명상수(), HODNOTA, Spustit_2); continue; }
            if (HODNOTA >= 182 && HODNOTA <= 185) {
                int 부호값 = 명상수();
                if (HODNOTA == 185) { int celkem_POČET = 명바(); if (celkem_POČET == 0 || 명바() != 0) { selhání_HODNOTA("invalid invokeinterface operands"); continue; } }
                VOLAT_metoda(부호값, HODNOTA); continue;
            }
            if (HODNOTA == 187) { 새객체(název_třídy_SMS(명상수()), Spustit_2); continue; }
            if (HODNOTA == 188 || HODNOTA == 189) {
                int oblast_KÓD = 3, součást = 0;
                if (HODNOTA == 188) { int 임시값 = 명바(); oblast_KÓD = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else součást = název_třídy_SMS(명상수());
                if (oblast_KÓD == 0) { selhání_HODNOTA("unsupported primitive array type"); continue; }
                int platný_délka = 빼기(1), objekt_odkaz = přidělit_Storage(oblast_KÓD, platný_délka); if (!chyba) prvek_pole[objekt_odkaz] = součást; 넣기(objekt_odkaz, 2); continue;
            }
            if (HODNOTA == 190) {
                int objekt_odkaz = 빼기(2);
                if (informační_systémy_platný_objekt(objekt_odkaz)) { int Porovnání_pozice = halda_HODNOTA[objekt_odkaz]; if (Porovnání_pozice != 2 && Porovnání_pozice != 3 && (Porovnání_pozice < 20 || Porovnání_pozice > 23)) selhání_HODNOTA("not an array"); else 넣기(halda_HODNOTA[objekt_odkaz + 1], 1); }
                continue;
            }
            if (HODNOTA == 191) {
                int objekt_odkaz = 빼기(2); if (informační_systémy_platný_objekt(objekt_odkaz)) { if (halda_HODNOTA[objekt_odkaz] != 9) selhání_HODNOTA("athrow requires supported Throwable"); else { 던진객체 = objekt_odkaz; chyba = true; } }
                continue;
            }
            if (HODNOTA == 192 || HODNOTA == 193) {
                int název_konstanta = název_třídy_SMS(명상수()), objekt_odkaz = 빼기(2); boolean POZVYHLEDAT = 맞는객체(objekt_odkaz, název_konstanta);
                if (HODNOTA == 193) 넣기(objekt_odkaz != 0 && POZVYHLEDAT ? 1 : 0, 1);
                else { if (!POZVYHLEDAT && !chyba) selhání_HODNOTA("ClassCastException"); 넣기(objekt_odkaz, 2); }
                continue;
            }
            if (HODNOTA == 170 || HODNOTA == 171) {
                int 읽는자리 = Spustit_2 + 1, Soubor_INDEX = rámec_metoda[rámec_INDEX], Klíč_odkaz = 빼기(1);
                while ((읽는자리 - metoda_START[Soubor_INDEX]) % 4 != 0) 읽는자리++;
                int cíl_ODKAZ = pozice_integer(읽는자리);
                if (HODNOTA == 170) { int 낮은값 = pozice_integer(읽는자리 + 4), 높은값 = pozice_integer(읽는자리 + 8); if (Klíč_odkaz >= 낮은값 && Klíč_odkaz <= 높은값) cíl_ODKAZ = pozice_integer(읽는자리 + 12 + (Klíč_odkaz - 낮은값) * 4); }
                else { int celkem_POČET = pozice_integer(읽는자리 + 4); for (int Loop_INDEX = 0; Loop_INDEX < celkem_POČET; Loop_INDEX++) if (pozice_integer(읽는자리 + 8 + Loop_INDEX * 8) == Klíč_odkaz) cíl_ODKAZ = pozice_integer(읽는자리 + 12 + Loop_INDEX * 8); }
                přesunout_HODNOTA(Spustit_2 + cíl_ODKAZ); continue;
            }
            if (HODNOTA == 200) { přesunout_HODNOTA(Spustit_2 + pozice_integer(Spustit_2 + 1)); continue; }
            if (HODNOTA == 194 || HODNOTA == 195) {
                int objekt_odkaz = 빼기(2);
                if (HODNOTA == 195) verze_zámek(objekt_odkaz);
                else if (!잠금얻기(objekt_odkaz) && !chyba) { 넣기(objekt_odkaz, 2); rámec_pozice[rámec_INDEX] = Spustit_2; }
                continue;
            }
            if (HODNOTA == 196) {
                int příkaz_KÓD = 명바(), položka_pozice = 명짧();
                if (příkaz_KÓD == 21 || příkaz_KÓD == 25) 지역읽기(položka_pozice, příkaz_KÓD == 21 ? 1 : 2);
                else if (příkaz_KÓD == 54 || příkaz_KÓD == 58) zápis_místní(položka_pozice, příkaz_KÓD == 54 ? 1 : 2);
                else if (příkaz_KÓD == 132) { int DELTA_HODNOTA = (short)명짧(); 지역읽기(položka_pozice, 1); 넣기(빼기(1) + DELTA_HODNOTA, 1); zápis_místní(položka_pozice, 1); }
                else selhání_HODNOTA("unsupported wide opcode");
                continue;
            }
            selhání_HODNOTA("unsupported bytecode");
        }
    }
    static int NAJÍT_Třída_Definice(int Název) {
        for (int Loop_INDEX = 0; Loop_INDEX < Třída_Definice_POČET; Loop_INDEX++) if (Třída_Definice_název[Loop_INDEX] != 0 && 같은말(Třída_Definice_název[Loop_INDEX], Název)) return Loop_INDEX;
        return dávka_Třída_Definice(konstanta_SMS(Název));
    }
    static int dávka_Třída_Definice(int název_řetězec) {
        if (!objekt_HODNOTA(název_řetězec, 1)) return -1;
        int délka_HODNOTA = halda_HODNOTA[název_řetězec + 1];
        if (délka_HODNOTA < 1 || délka_HODNOTA > 505 || Třída_Definice_POČET == 16) { selhání_HODNOTA("class name/count limit"); return -1; }
        for (int Loop_INDEX = 0; Loop_INDEX < délka_HODNOTA; Loop_INDEX++) { int bod_kódu = halda_HODNOTA[název_řetězec + 2 + Loop_INDEX]; název_souboru_SMS[Loop_INDEX] = bod_kódu == '/' ? '.' : bod_kódu; }
        název_souboru_SMS[délka_HODNOTA] = '.'; název_souboru_SMS[délka_HODNOTA + 1] = 'c'; název_souboru_SMS[délka_HODNOTA + 2] = 'l'; název_souboru_SMS[délka_HODNOTA + 3] = 'a'; název_souboru_SMS[délka_HODNOTA + 4] = 's'; název_souboru_SMS[délka_HODNOTA + 5] = 's'; název_souboru_SMS[délka_HODNOTA + 6] = 0;
        int Velikost = uživatelský_prostor.파일읽기(název_souboru_SMS, dočasný_soubor);
        if (Velikost < 0) { selhání_HODNOTA("ClassNotFoundException"); return -1; }
        int Třída_Definice = Třída_Definice_POČET++; Třída_Definice_změnit_velikost[Třída_Definice] = Velikost;
        for (int Loop_INDEX = 0; Loop_INDEX < Velikost; Loop_INDEX++) název_souboru[Třída_Definice * 16384 + Loop_INDEX] = dočasný_soubor[Loop_INDEX];
        클래스읽기(Třída_Definice); if (chyba) return -1;
        int skutečný_data = konstanta_SMS(Třída_Definice_název[Třída_Definice]);
        if (!texty_stejné(skutečný_data, název_řetězec, true)) { selhání_HODNOTA("class name does not match file"); return -1; }
        int nadřazený_HODNOTA = Třída_Definice_nadřazený[Třída_Definice];
        if (nadřazený_HODNOTA != 0 && !Word_SMS(nadřazený_HODNOTA, "java/lang/Object") && !Word_SMS(nadřazený_HODNOTA, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 zkusit_znovu_HODNOTA 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = NAJÍT_Třída_Definice(nadřazený_HODNOTA);
            if (chyba || 위 < 0) return -1;
            int 읽는자리 = 위, fáze_POČET = 0;
            while (읽는자리 >= 0 && fáze_POČET++ < 16) {
                if (읽는자리 == Třída_Definice) { selhání_HODNOTA("cyclic inheritance"); return -1; }
                읽는자리 = nadřazený_Třída(읽는자리);
            }
            int 시작변위 = Třída_přihrádka_POČET[위];
            for (int Soubor_INDEX = 0; Soubor_INDEX < přihrádka_POČET; Soubor_INDEX++) if (přihrádka_vlastník[Soubor_INDEX] == Třída_Definice && (přihrádka_Oprávnění[Soubor_INDEX] & 8) == 0) přihrádka_pozice[Soubor_INDEX] += 시작변위;
            Třída_přihrádka_POČET[Třída_Definice] += 시작변위;
        }
        return Třída_Definice;
    }
    static int nadřazený_Třída(int Třída_Definice) {
        int Název = Třída_Definice_nadřazený[Třída_Definice];
        for (int Loop_INDEX = 0; Loop_INDEX < Třída_Definice_POČET; Loop_INDEX++) if (Název != 0 && Třída_Definice_název[Loop_INDEX] != 0 && 같은말(Třída_Definice_název[Loop_INDEX], Název)) return Loop_INDEX;
        return -1;
    }
    static int NAJÍT_metoda(int Třída_Definice, int Název, int formát_HODNOTA) {
        for (int 깊이 = 0; Třída_Definice >= 0 && 깊이 < 16; 깊이++, Třída_Definice = nadřazený_Třída(Třída_Definice)) {
            for (int Loop_INDEX = 0; Loop_INDEX < metoda_POČET; Loop_INDEX++) if (metoda_vlastník[Loop_INDEX] == Třída_Definice && 같은말(metoda_název_SMS[Loop_INDEX], Název) && 같은말(metoda_TYP[Loop_INDEX], formát_HODNOTA)) return Loop_INDEX;
        }
        return -1;
    }
    static int název_metoda(int Třída_Definice, String Název, String formát_HODNOTA) {
        for (int 깊이 = 0; Třída_Definice >= 0 && 깊이 < 16; 깊이++, Třída_Definice = nadřazený_Třída(Třída_Definice))
            for (int Loop_INDEX = 0; Loop_INDEX < metoda_POČET; Loop_INDEX++) if (metoda_vlastník[Loop_INDEX] == Třída_Definice && Word_SMS(metoda_název_SMS[Loop_INDEX], Název) && Word_SMS(metoda_TYP[Loop_INDEX], formát_HODNOTA)) return Loop_INDEX;
        return -1;
    }
    static int TYP_Druh(int Název) { return název_souboru[상가[Název]] == 'L' || název_souboru[상가[Název]] == '[' ? 2 : 1; }
    static boolean inicializovat(int Třída_Definice, int příkaz_START) {
        if (Třída_Definice < 0 || chyba) return false;
        if (Třída_Definice_Stav[Třída_Definice] == 3) { selhání_HODNOTA("NoClassDefFoundError: initialization failed"); return false; }
        if (Třída_Definice_Stav[Třída_Definice] == 1 && Třída_vlákno[Třída_Definice] != dobrá_vlákno) { rámec_pozice[rámec_INDEX] = příkaz_START; žádost_o_změnu = true; return false; }
        if (Třída_Definice_Stav[Třída_Definice] != 0) return true;
        int 위 = nadřazený_Třída(Třída_Definice);
        if (위 >= 0 && !inicializovat(위, příkaz_START)) return false;
        Třída_Definice_Stav[Třída_Definice] = 1; Třída_vlákno[Třída_Definice] = dobrá_vlákno;
        if (inicializovat_Třída_Definice[Třída_Definice] != 0) {
            rámec_pozice[rámec_INDEX] = příkaz_START;
            호출(inicializovat_Třída_Definice[Třída_Definice] - 1); if (!chyba) inicializovat_rámec[rámec_INDEX] = Třída_Definice + 1;
            return false;
        }
        Třída_Definice_Stav[Třída_Definice] = 2; return true;
    }
    static void 필드호출(int INDEX, int příkaz, int Spustit_2) {
        if (!šek_konstanta(INDEX, 9)) return;
        int vlastník_HODNOTA = název_třídy_SMS(상가[INDEX]), Název = odkaz_název(konstanta_SEKUNDA_HODNOTA[INDEX]), formát_HODNOTA = odkaz_c74caca7(konstanta_SEKUNDA_HODNOTA[INDEX]);
        if (Word_SMS(vlastník_HODNOTA, "java/lang/System") && (Word_SMS(Název, "out") || Word_SMS(Název, "err")) && Word_SMS(formát_HODNOTA, "Ljava/io/PrintStream;") && příkaz == 178) { 넣기(-1, 2); return; }
        int Třída_Definice = NAJÍT_Třída_Definice(vlastník_HODNOTA); if (Třída_Definice < 0 || chyba) return;
        int 찾음 = -1;
        for (int 읽는자리 = Třída_Definice, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = nadřazený_Třída(읽는자리))
            for (int Soubor_INDEX = 0; Soubor_INDEX < přihrádka_POČET; Soubor_INDEX++) if (přihrádka_vlastník[Soubor_INDEX] == 읽는자리 && 같은말(přihrádka_název[Soubor_INDEX], Název) && 같은말(přihrádka_TYP[Soubor_INDEX], formát_HODNOTA)) 찾음 = Soubor_INDEX;
        if (찾음 < 0) { selhání_HODNOTA("NoSuchFieldError"); return; }
        boolean statický_HODNOTA = příkaz == 178 || příkaz == 179;
        if (statický_HODNOTA != ((přihrádka_Oprávnění[찾음] & 8) != 0)) { selhání_HODNOTA("field static/instance mismatch"); return; }
        if (statický_HODNOTA && !inicializovat(přihrádka_vlastník[찾음], Spustit_2)) return;
        int TYP_HODNOTA = TYP_Druh(formát_HODNOTA), HODNOTA = 0;
        if (příkaz == 179 || příkaz == 181) HODNOTA = 빼기(TYP_HODNOTA);
        if (statický_HODNOTA) { if (příkaz == 178) 넣기(přihrádka_data[찾음], TYP_HODNOTA); else if (!chyba) přihrádka_data[찾음] = HODNOTA; return; }
        int objekt_odkaz = 빼기(2);
        if (!informační_systémy_platný_objekt(objekt_odkaz)) return;
        if (halda_HODNOTA[objekt_odkaz] < 32 || !종포함(halda_HODNOTA[objekt_odkaz] - 32, vlastník_HODNOTA)) { selhání_HODNOTA("field receiver type mismatch"); return; }
        int 보관칸 = objekt_odkaz + 2 + přihrádka_pozice[찾음];
        if (příkaz == 180) 넣기(halda_HODNOTA[보관칸], TYP_HODNOTA);
        else if (!chyba) { halda_HODNOTA[보관칸] = HODNOTA; halda_odkaz[보관칸] = TYP_HODNOTA == 2 ? 1 : 0; }
    }
    static boolean 종포함(int Třída_Definice, int Název) {
        for (int 중첩깊이 = 0; Třída_Definice >= 0 && 중첩깊이 < 16; 중첩깊이++, Třída_Definice = nadřazený_Třída(Třída_Definice)) {
            if (같은말(Třída_Definice_název[Třída_Definice], Název) || (Třída_Definice_nadřazený[Třída_Definice] != 0 && 같은말(Třída_Definice_nadřazený[Třída_Definice], Název))) return true;
            for (int vnitřní_pozice = 0; vnitřní_pozice < Třída_rozhraní_POČET[Třída_Definice]; vnitřní_pozice++) if (같은말(Třída_rozhraní[Třída_Definice * 16 + vnitřní_pozice], Název)) return true;
        }
        return false;
    }
    static boolean texty_stejné(int 첫값, int bajt_data, boolean cesta_2) {
        if (첫값 == bajt_data) return true;
        if (첫값 <= 0 || bajt_data <= 0 || halda_HODNOTA[첫값] != 1 || halda_HODNOTA[bajt_data] != 1 || halda_HODNOTA[첫값 + 1] != halda_HODNOTA[bajt_data + 1]) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < halda_HODNOTA[첫값 + 1]; Loop_INDEX++) {
            int souřadnice_x = halda_HODNOTA[첫값 + 2 + Loop_INDEX], Y_souřadnice = halda_HODNOTA[bajt_data + 2 + Loop_INDEX];
            if (cesta_2) { if (souřadnice_x == '.') souřadnice_x = '/'; if (Y_souřadnice == '.') Y_souřadnice = '/'; }
            if (souřadnice_x != Y_souřadnice) return false;
        }
        return true;
    }
    static boolean informační_systémy_platný_objekt(int objekt_odkaz) {
        if (objekt_odkaz == 0) { selhání_HODNOTA("NullPointerException"); return false; }
        if (objekt_odkaz < 1 || objekt_odkaz >= halda_konec_pozice || 힙폭[objekt_odkaz] < 2 || halda_HODNOTA[objekt_odkaz] == 0) { selhání_HODNOTA("invalid object reference"); return false; }
        return true;
    }
    static void chránit_HODNOTA(int objekt_odkaz) {
        if (objekt_odkaz > 0 && objekt_odkaz < halda_konec_pozice && 힙폭[objekt_odkaz] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = objekt_odkaz;
    }
    static void zobrazit_HODNOTA(int objekt_odkaz) {
        if (objekt_odkaz > 0 && objekt_odkaz < halda_konec_pozice && 힙폭[objekt_odkaz] >= 2 && halda_HODNOTA[objekt_odkaz] != 0 && 힙표시[objekt_odkaz] == 0) {
            힙표시[objekt_odkaz] = 1; 표시대기[displej_POČET++] = objekt_odkaz;
        }
    }
    static void 수거() {
        displej_POČET = 0; inkaso_POČET++;
        for (int šek_pozice = 1; šek_pozice < halda_konec_pozice; šek_pozice += 힙폭[šek_pozice]) 힙표시[šek_pozice] = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < řetězec_odkaz.length; Loop_INDEX++) zobrazit_HODNOTA(řetězec_odkaz[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < přihrádka_POČET; Loop_INDEX++) if ((přihrádka_Oprávnění[Loop_INDEX] & 8) != 0 && TYP_Druh(přihrádka_TYP[Loop_INDEX]) == 2) zobrazit_HODNOTA(přihrádka_data[Loop_INDEX]);
        for (int 임시값 = 0; 임시값 < počet_vláken; 임시값++) {
            zobrazit_HODNOTA(vlákno_objekt[임시값]); zobrazit_HODNOTA(vlákno_cíl[임시값]);
            int 꼭대기자리 = 임시값 == dobrá_vlákno ? rámec_INDEX : vlákno_rámec[임시값];
            for (int Soubor_INDEX = 임시값 * 32; Soubor_INDEX <= 꼭대기자리; Soubor_INDEX++) {
                for (int vnitřní_pozice = 0; vnitřní_pozice < 함수지역[rámec_metoda[Soubor_INDEX]]; vnitřní_pozice++) if (místní_TYP[Soubor_INDEX * 128 + vnitřní_pozice] == 2) zobrazit_HODNOTA(místní_HODNOTA[Soubor_INDEX * 128 + vnitřní_pozice]);
                for (int vnitřní_pozice = 0; vnitřní_pozice < rámec_Štos[Soubor_INDEX]; vnitřní_pozice++) if (operand_Štos_TYP[Soubor_INDEX * 128 + vnitřní_pozice] == 2) zobrazit_HODNOTA(operand_Štos_HODNOTA[Soubor_INDEX * 128 + vnitřní_pozice]);
            }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 화면참조.length; Loop_INDEX++) zobrazit_HODNOTA(화면참조[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < 나중수; Loop_INDEX++) zobrazit_HODNOTA(나중실행[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < Store_integer.length; Loop_INDEX++) zobrazit_HODNOTA(Store_integer[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < Třída_Definice_POČET; Loop_INDEX++) zobrazit_HODNOTA(Třída_zámek[Loop_INDEX]);
        for (int šek_pozice = 1; šek_pozice < halda_konec_pozice; šek_pozice += 힙폭[šek_pozice]) if (잠금깊이[šek_pozice] > 0) zobrazit_HODNOTA(šek_pozice);
        zobrazit_HODNOTA(던진객체);
        for (int Loop_INDEX = 0; Loop_INDEX < 잠시수; Loop_INDEX++) zobrazit_HODNOTA(잠시참조[Loop_INDEX]);
        while (displej_POČET > 0) {
            int objekt_odkaz = 표시대기[--displej_POČET], oblast_KÓD = halda_HODNOTA[objekt_odkaz];
            for (int Loop_INDEX = objekt_odkaz + 2; Loop_INDEX < objekt_odkaz + 힙폭[objekt_odkaz]; Loop_INDEX++) if (oblast_KÓD == 3 || oblast_KÓD == 4 || halda_odkaz[Loop_INDEX] != 0) zobrazit_HODNOTA(halda_HODNOTA[Loop_INDEX]);
        }
        for (int šek_pozice = 1; šek_pozice < halda_konec_pozice; šek_pozice += 힙폭[šek_pozice]) if (힙표시[šek_pozice] == 0) halda_HODNOTA[šek_pozice] = 0;
        for (int šek_pozice = 1; šek_pozice < halda_konec_pozice; šek_pozice += 힙폭[šek_pozice]) if (halda_HODNOTA[šek_pozice] == 0) {
            while (šek_pozice + 힙폭[šek_pozice] < halda_konec_pozice && halda_HODNOTA[šek_pozice + 힙폭[šek_pozice]] == 0) { int Další_pozice = šek_pozice + 힙폭[šek_pozice]; 힙폭[šek_pozice] += 힙폭[Další_pozice]; 힙폭[Další_pozice] = 0; }
            if (šek_pozice + 힙폭[šek_pozice] == halda_konec_pozice) { halda_konec_pozice = šek_pozice; break; }
        }
    }
    static int 새기억(int Druh_HODNOTA, int délka_HODNOTA) {
        if (délka_HODNOTA < 0) { selhání_HODNOTA("NegativeArraySizeException"); return 0; }
        if (délka_HODNOTA > halda_HODNOTA.length - 3) { selhání_HODNOTA("object heap exhausted"); return 0; }
        int 필요수 = délka_HODNOTA + 2, objekt_odkaz = 0;
        if (필요수 <= halda_HODNOTA.length - halda_konec_pozice) { objekt_odkaz = halda_konec_pozice; halda_konec_pozice += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < halda_konec_pozice; 읽는자리 += 힙폭[읽는자리]) if (halda_HODNOTA[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { objekt_odkaz = 읽는자리; break; }
            if (objekt_odkaz != 0) {
                int 남은길이 = 힙폭[objekt_odkaz] - 필요수;
                if (남은길이 >= 2) { 힙폭[objekt_odkaz + 필요수] = 남은길이; halda_HODNOTA[objekt_odkaz + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= halda_HODNOTA.length - halda_konec_pozice) { objekt_odkaz = halda_konec_pozice; halda_konec_pozice += 필요수; }
        }
        if (objekt_odkaz == 0) { selhání_HODNOTA("object heap exhausted"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < 필요수; Loop_INDEX++) { halda_HODNOTA[objekt_odkaz + Loop_INDEX] = 0; halda_odkaz[objekt_odkaz + Loop_INDEX] = 0; 힙폭[objekt_odkaz + Loop_INDEX] = 0; }
        prvek_pole[objekt_odkaz] = 0;
        힙폭[objekt_odkaz] = 필요수; halda_HODNOTA[objekt_odkaz] = Druh_HODNOTA; halda_HODNOTA[objekt_odkaz + 1] = délka_HODNOTA; chránit_HODNOTA(objekt_odkaz); return objekt_odkaz;
    }
    static int výjimka_Třída(String název_konstanta) {
        if (자바도구.같음(název_konstanta, "java/lang/Throwable")) return 1;
        if (자바도구.같음(název_konstanta, "java/lang/Exception")) return 2;
        if (자바도구.같음(název_konstanta, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(název_konstanta, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(název_konstanta, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(název_konstanta, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(název_konstanta, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(název_konstanta, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(název_konstanta, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(název_konstanta, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(název_konstanta, "java/io/IOException")) return 11;
        if (자바도구.같음(název_konstanta, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(název_konstanta, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(název_konstanta, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(název_konstanta, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int výjimka_konstanta(int Název) {
        for (int Loop_INDEX = 1; Loop_INDEX <= 41; Loop_INDEX++) if (Word_SMS(Název, výjimka_název(Loop_INDEX))) return Loop_INDEX;
        return 0;
    }
    static String výjimka_název(int účet_HODNOTA) {
        if (účet_HODNOTA == 40) return "java/lang/InterruptedException";
        if (účet_HODNOTA == 41) return "čeština/vlastní/대기중단예외";
        if (účet_HODNOTA == 39) return "java/net/SocketException";
        if (účet_HODNOTA == 20) return "čeština/vlastní/výjimka";
        if (účet_HODNOTA == 21) return "čeština/vlastní/spuštění_výjimka";
        if (účet_HODNOTA == 22) return "čeština/vlastní/vstup_a_výstup_výjimka";
        if (účet_HODNOTA == 23) return "čeština/vlastní/počkej_TIMEOUT_výjimka";
        if (účet_HODNOTA == 24) return "čeština/vlastní/ODKAZ_VYHLEDAT_výjimka";
        if (účet_HODNOTA == 25) return "čeština/vlastní/파일없음예외";
        if (účet_HODNOTA == 26) return "čeština/vlastní/komunikace_výjimka";
        if (účet_HODNOTA == 27) return "čeština/vlastní/neplatný_argument_výjimka";
        if (účet_HODNOTA == 28) return "čeština/vlastní/číslo_formát_selhání";
        if (účet_HODNOTA == 29) return "čeština/vlastní/범위예외";
        if (účet_HODNOTA == 30) return "čeština/vlastní/배열범위예외";
        if (účet_HODNOTA == 31) return "čeština/vlastní/문자열범위예외";
        if (účet_HODNOTA == 32) return "čeština/vlastní/nulový_odkaz_výjimka";
        if (účet_HODNOTA == 33) return "čeština/vlastní/산술예외";
        if (účet_HODNOTA == 34) return "čeština/vlastní/Stav_výjimka";
        if (účet_HODNOTA == 35) return "čeština/vlastní/TYP_převod_výjimka";
        if (účet_HODNOTA == 36) return "čeština/vlastní/음수배열크기예외";
        if (účet_HODNOTA == 37) return "čeština/vlastní/pole_Store_selhání";
        if (účet_HODNOTA == 38) return "čeština/vlastní/vlákno_Stav_výjimka";
        if (účet_HODNOTA == 1) return "java/lang/Throwable"; if (účet_HODNOTA == 2) return "java/lang/Exception";
        if (účet_HODNOTA == 3) return "java/lang/RuntimeException"; if (účet_HODNOTA == 4) return "java/lang/ArithmeticException";
        if (účet_HODNOTA == 5) return "java/lang/NullPointerException"; if (účet_HODNOTA == 6) return "java/lang/IndexOutOfBoundsException";
        if (účet_HODNOTA == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (účet_HODNOTA == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (účet_HODNOTA == 9) return "java/lang/IllegalArgumentException"; if (účet_HODNOTA == 10) return "java/lang/NumberFormatException";
        if (účet_HODNOTA == 11) return "java/io/IOException"; if (účet_HODNOTA == 12) return "java/io/FileNotFoundException";
        if (účet_HODNOTA == 17) return "java/lang/ArrayStoreException";
        if (účet_HODNOTA == 18) return "java/net/UnknownHostException";
        if (účet_HODNOTA == 19) return "java/net/SocketTimeoutException";
        if (účet_HODNOTA == 16) return "java/lang/IllegalThreadStateException";
        if (účet_HODNOTA == 13) return "java/lang/IllegalStateException"; if (účet_HODNOTA == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int výjimka_nadřazený(int účet_HODNOTA) {
        if (účet_HODNOTA == 40) return 2;
        if (účet_HODNOTA == 41) return 40;
        if (účet_HODNOTA == 39) return 11;
        if (účet_HODNOTA == 1) return 0;
        if (účet_HODNOTA == 2) return 1;
        if (účet_HODNOTA == 3) return 2;
        if (účet_HODNOTA == 4) return 3;
        if (účet_HODNOTA == 5) return 3;
        if (účet_HODNOTA == 6) return 3;
        if (účet_HODNOTA == 7) return 6;
        if (účet_HODNOTA == 8) return 6;
        if (účet_HODNOTA == 9) return 3;
        if (účet_HODNOTA == 10) return 9;
        if (účet_HODNOTA == 11) return 2;
        if (účet_HODNOTA == 12) return 11;
        if (účet_HODNOTA == 13) return 3;
        if (účet_HODNOTA == 14) return 3;
        if (účet_HODNOTA == 15) return 3;
        if (účet_HODNOTA == 16) return 9;
        if (účet_HODNOTA == 17) return 3;
        if (účet_HODNOTA == 18) return 11;
        if (účet_HODNOTA == 19) return 11;
        if (účet_HODNOTA == 20) return 2;
        if (účet_HODNOTA == 21) return 3;
        if (účet_HODNOTA == 22) return 11;
        if (účet_HODNOTA == 23) return 22;
        if (účet_HODNOTA == 24) return 22;
        if (účet_HODNOTA == 25) return 22;
        if (účet_HODNOTA == 26) return 22;
        if (účet_HODNOTA == 27) return 9;
        if (účet_HODNOTA == 28) return 27;
        if (účet_HODNOTA == 29) return 6;
        if (účet_HODNOTA == 30) return 29;
        if (účet_HODNOTA == 31) return 29;
        if (účet_HODNOTA == 32) return 5;
        if (účet_HODNOTA == 33) return 4;
        if (účet_HODNOTA == 34) return 13;
        if (účet_HODNOTA == 35) return 14;
        if (účet_HODNOTA == 36) return 15;
        if (účet_HODNOTA == 37) return 17;
        if (účet_HODNOTA == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int skutečná_hodnota, int 요구값) {
        for (int 깊이 = 0; skutečná_hodnota != 0 && 깊이 < 16; 깊이++, skutečná_hodnota = výjimka_nadřazený(skutečná_hodnota))
            if (skutečná_hodnota == 요구값) return true;
        return false;
    }
    static void 예외던짐(int účet_HODNOTA, String 안내참조) {
        int objekt_odkaz = 새기억(9, 2); if (chyba) return;
        halda_HODNOTA[objekt_odkaz + 2] = účet_HODNOTA; halda_HODNOTA[objekt_odkaz + 3] = hostit_znak(안내참조); halda_odkaz[objekt_odkaz + 3] = 1;
        던진객체 = objekt_odkaz; chyba = true;
    }
    static boolean 맞는객체(int objekt_odkaz, int Název) {
        if (objekt_odkaz == 0) return true;
        if (!informační_systémy_platný_objekt(objekt_odkaz)) return false;
        int oblast_KÓD = halda_HODNOTA[objekt_odkaz];
        if (Word_SMS(Název, "java/lang/Object")) return true;
        if (oblast_KÓD >= 32) return 종포함(oblast_KÓD - 32, Název);
        if (oblast_KÓD == 9) { int cíl_ODKAZ = výjimka_konstanta(Název); return cíl_ODKAZ != 0 && 예외포함(halda_HODNOTA[objekt_odkaz + 2], cíl_ODKAZ); }
        if (oblast_KÓD == 1) return Word_SMS(Název, "java/lang/String") || Word_SMS(Název, "java/lang/CharSequence");
        if (oblast_KÓD == 4) return Word_SMS(Název, "java/lang/StringBuilder") || Word_SMS(Název, "java/lang/CharSequence");
        if (oblast_KÓD == 10) return Word_SMS(Název, "java/util/ArrayList") || Word_SMS(Název, "java/util/List");
        if (oblast_KÓD == 11) return Word_SMS(Název, "java/util/HashMap") || Word_SMS(Název, "java/util/Map");
        if (oblast_KÓD == 12) return Word_SMS(Název, "java/lang/Integer") || Word_SMS(Název, "java/lang/Number");
        if (oblast_KÓD >= 24 && oblast_KÓD <= 28 && halda_HODNOTA[objekt_odkaz + 13] != 0) return 한국어화면종(Název) == oblast_KÓD || Word_SMS(Název, "čeština/vlastní/화면구성요소");
        if (oblast_KÓD >= 24 && oblast_KÓD <= 28) return (한국어화면종(Název) == 0 && 화면종(Název) == oblast_KÓD) || Word_SMS(Název, "java/awt/Component") || Word_SMS(Název, "java/awt/Container") || Word_SMS(Název, "javax/swing/JComponent");
        if (oblast_KÓD == 29) return Word_SMS(Název, halda_HODNOTA[objekt_odkaz + 3] != 0 ? "čeština/vlastní/Akce_povinnost_zvěřejnit" : "java/awt/event/ActionEvent");
        if (oblast_KÓD == 30) return Word_SMS(Název, "java/awt/FlowLayout") || Word_SMS(Název, "java/awt/LayoutManager");
        if (oblast_KÓD == 17) return Word_SMS(Název, "java/net/Socket");
        if (oblast_KÓD == 18) return Word_SMS(Název, "java/net/ServerSocket");
        if (oblast_KÓD == 19) return Word_SMS(Název, halda_HODNOTA[objekt_odkaz + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (oblast_KÓD == 14) return Word_SMS(Název, "java/net/InetAddress");
        if (oblast_KÓD == 15) return Word_SMS(Název, "java/net/DatagramSocket");
        if (oblast_KÓD == 16) return Word_SMS(Název, "java/net/DatagramPacket");
        if (oblast_KÓD == 13) return Word_SMS(Název, halda_HODNOTA[objekt_odkaz + 3] != 0 ? "čeština/vlastní/pracovník" : "java/lang/Thread");
        if (oblast_KÓD == 2) return Word_SMS(Název, "[I"); if (oblast_KÓD == 20) return Word_SMS(Název, "[B"); if (oblast_KÓD == 21) return Word_SMS(Název, "[Z");
        if (oblast_KÓD == 22) return Word_SMS(Název, "[C"); if (oblast_KÓD == 23) return Word_SMS(Název, "[S");
        if (oblast_KÓD != 3) return false;
        if (Word_SMS(Název, "[Ljava/lang/Object;")) return true;
        int součást = prvek_pole[objekt_odkaz];
        if (součást == -1) return Word_SMS(Název, "[Ljava/lang/String;") || Word_SMS(Název, "[Ljava/lang/CharSequence;");
        if (součást == 0) return false;
        if (배열종비교(součást, Název)) return true;
        if ((Word_SMS(součást, "java/lang/String") || Word_SMS(součást, "java/lang/StringBuilder")) && Word_SMS(Název, "[Ljava/lang/CharSequence;")) return true;
        for (int Loop_INDEX = 0; Loop_INDEX < Třída_Definice_POČET; Loop_INDEX++) if (같은말(Třída_Definice_název[Loop_INDEX], součást)) {
            for (int bod_kódu = Loop_INDEX, 중첩깊이 = 0; bod_kódu >= 0 && 중첩깊이 < 16; 중첩깊이++, bod_kódu = nadřazený_Třída(bod_kódu)) {
                if (배열종비교(Třída_Definice_nadřazený[bod_kódu], Název)) return true;
                for (int vnitřní_pozice = 0; vnitřní_pozice < Třída_rozhraní_POČET[bod_kódu]; vnitřní_pozice++) if (배열종비교(Třída_rozhraní[bod_kódu * 16 + vnitřní_pozice], Název)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int název_konstanta, int popisovač) {
        int šek_pozice = 상가[popisovač], položka_POČET = konstanta_SEKUNDA_HODNOTA[popisovač];
        if (název_konstanta == 0 || položka_POČET < 4 || název_souboru[šek_pozice] != '[' || název_souboru[šek_pozice + 1] != 'L' || název_souboru[šek_pozice + položka_POČET - 1] != ';' || konstanta_SEKUNDA_HODNOTA[název_konstanta] != položka_POČET - 3) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < položka_POČET - 3; Loop_INDEX++) if (název_souboru[상가[název_konstanta] + Loop_INDEX] != název_souboru[šek_pozice + 2 + Loop_INDEX]) return false;
        return true;
    }
    static void úchyt_výjimka() {
        if (던진객체 == 0) return;
        chyba = false;
        while (rámec_INDEX >= dobrá_vlákno * 32) {
            int Soubor_INDEX = rámec_metoda[rámec_INDEX], 읽는자리 = 틀명령[rámec_INDEX];
            for (int Loop_INDEX = 0; Loop_INDEX < 잡기수; Loop_INDEX++) if (잡기함수[Loop_INDEX] == Soubor_INDEX && 읽는자리 >= 잡기시작[Loop_INDEX] && 읽는자리 < 잡기끝[Loop_INDEX]
                && (잡기종[Loop_INDEX] == 0 || 맞는객체(던진객체, 잡기종[Loop_INDEX]))) {
                rámec_pozice[rámec_INDEX] = 잡기위치[Loop_INDEX]; rámec_Štos[rámec_INDEX] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (inicializovat_rámec[rámec_INDEX] != 0) Třída_Definice_Stav[inicializovat_rámec[rámec_INDEX] - 1] = 3;
            if (rámec_zámek[rámec_INDEX] != 0) { verze_zámek(rámec_zámek[rámec_INDEX]); rámec_zámek[rámec_INDEX] = 0; }
            rámec_INDEX--;
        }
        uživatelský_prostor.Zápis("Uncaught ");
        if (halda_HODNOTA[던진객체] == 9) { uživatelský_prostor.Zápis(výjimka_název(halda_HODNOTA[던진객체 + 2])); uživatelský_prostor.Zápis(": "); zápis_SMS(halda_HODNOTA[던진객체 + 3]); }
        else uživatelský_prostor.Zápis("user exception");
        uživatelský_prostor.zápis_znak_HODNOTA(10); 던진객체 = 0; chyba = true;
    }
    // 이 JVM의 operand_Štos 항목은 dobrá_zboží category-1(int/reference)만 허용한다.
    static void 스택명령(int příkaz_KÓD) {
        int 첫값 = 빼기(0), 첫형식 = návratový_typ;
        if (příkaz_KÓD == 87) return;
        if (příkaz_KÓD == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int bajt_data = 빼기(0), SEKUNDA_formát = návratový_typ;
        if (příkaz_KÓD == 88) return;
        if (příkaz_KÓD == 90) { 넣기(첫값, 첫형식); 넣기(bajt_data, SEKUNDA_formát); 넣기(첫값, 첫형식); return; }
        if (příkaz_KÓD == 92) { 넣기(bajt_data, SEKUNDA_formát); 넣기(첫값, 첫형식); 넣기(bajt_data, SEKUNDA_formát); 넣기(첫값, 첫형식); return; }
        if (příkaz_KÓD == 95) { 넣기(첫값, 첫형식); 넣기(bajt_data, SEKUNDA_formát); return; }
        int bod_kódu = 빼기(0), 셋째형식 = návratový_typ;
        if (příkaz_KÓD == 91) { 넣기(첫값, 첫형식); 넣기(bod_kódu, 셋째형식); 넣기(bajt_data, SEKUNDA_formát); 넣기(첫값, 첫형식); return; }
        if (příkaz_KÓD == 93) { 넣기(bajt_data, SEKUNDA_formát); 넣기(첫값, 첫형식); 넣기(bod_kódu, 셋째형식); 넣기(bajt_data, SEKUNDA_formát); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = návratový_typ;
        넣기(bajt_data, SEKUNDA_formát); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(bod_kódu, 셋째형식); 넣기(bajt_data, SEKUNDA_formát); 넣기(첫값, 첫형식);
    }
    static void 새객체(int název_konstanta, int 시작점) {
        int oblast_KÓD = 0, platný_délka = 0, výjimka_odkaz = výjimka_konstanta(název_konstanta);
        if (Word_SMS(název_konstanta, "java/lang/StringBuilder")) { oblast_KÓD = 4; platný_délka = 1; }
        if (Word_SMS(název_konstanta, "java/io/FileInputStream")) { oblast_KÓD = 5; platný_délka = 2; }
        if (Word_SMS(název_konstanta, "java/io/FileOutputStream")) { oblast_KÓD = 6; platný_délka = 2; }
        if (výjimka_odkaz != 0) { oblast_KÓD = 9; platný_délka = 2; }
        if (Word_SMS(název_konstanta, "java/util/ArrayList")) { oblast_KÓD = 10; platný_délka = 2; }
        if (Word_SMS(název_konstanta, "java/util/HashMap")) { oblast_KÓD = 11; platný_délka = 2; }
        if (Word_SMS(název_konstanta, "java/lang/Integer")) { oblast_KÓD = 12; platný_délka = 1; }
        if (Word_SMS(název_konstanta, "java/net/Socket")) { oblast_KÓD = 17; platný_délka = 5; }
        if (Word_SMS(název_konstanta, "java/net/ServerSocket")) { oblast_KÓD = 18; platný_délka = 5; }
        if (Word_SMS(název_konstanta, "java/net/DatagramSocket")) { oblast_KÓD = 15; platný_délka = 3; }
        if (Word_SMS(název_konstanta, "java/net/DatagramPacket")) { oblast_KÓD = 16; platný_délka = 4; }
        if (Word_SMS(název_konstanta, "java/lang/Thread") || Word_SMS(název_konstanta, "čeština/vlastní/pracovník")) { oblast_KÓD = 13; platný_délka = 2; }
        if (Word_SMS(název_konstanta, "java/lang/Object")) { oblast_KÓD = 8; }
        if (oblast_KÓD == 0 && 화면종(název_konstanta) != 0) { oblast_KÓD = 화면종(název_konstanta); platný_délka = 12; }
        if (oblast_KÓD == 0) {
            int bod_kódu = NAJÍT_Třída_Definice(název_konstanta); if (bod_kódu < 0 || chyba || !inicializovat(bod_kódu, 시작점)) return;
            oblast_KÓD = 32 + bod_kódu; platný_délka = Třída_přihrádka_POČET[bod_kódu];
        }
        int objekt_odkaz = přidělit_Storage(oblast_KÓD, platný_délka); if (chyba) return;
        if (oblast_KÓD == 13 && Word_SMS(název_konstanta, "čeština/vlastní/pracovník")) halda_HODNOTA[objekt_odkaz + 3] = 1;
        if (oblast_KÓD >= 24 && oblast_KÓD <= 28 && 한국어화면종(název_konstanta) != 0) halda_HODNOTA[objekt_odkaz + 13] = 1;
        if (oblast_KÓD == 5 || oblast_KÓD == 6 || oblast_KÓD == 15 || oblast_KÓD == 17 || oblast_KÓD == 18) halda_HODNOTA[objekt_odkaz + 2] = -1;
        if (oblast_KÓD == 9) halda_HODNOTA[objekt_odkaz + 2] = výjimka_odkaz;
        넣기(objekt_odkaz, 2);
    }
    static boolean 값같음(int 첫값, int bajt_data) {
        if (첫값 == bajt_data) return true;
        if (첫값 == 0 || bajt_data == 0 || 첫값 < 0 || bajt_data < 0 || 첫값 >= halda_konec_pozice || bajt_data >= halda_konec_pozice) return false;
        if (halda_HODNOTA[첫값] == 1 && halda_HODNOTA[bajt_data] == 1) return texty_stejné(첫값, bajt_data, false);
        return halda_HODNOTA[첫값] == 12 && halda_HODNOTA[bajt_data] == 12 && halda_HODNOTA[첫값 + 2] == halda_HODNOTA[bajt_data + 2];
    }
    static int 글조각(int objekt_odkaz, int START_pozice, int konec_pozice) {
        if (!objekt_HODNOTA(objekt_odkaz, 1)) return 0;
        if (START_pozice < 0 || konec_pozice < START_pozice || konec_pozice > halda_HODNOTA[objekt_odkaz + 1]) { selhání_HODNOTA("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = přidělit_Storage(1, konec_pozice - START_pozice); if (chyba) return 0;
        for (int Loop_INDEX = START_pozice; Loop_INDEX < konec_pozice; Loop_INDEX++) halda_HODNOTA[반환값 + 2 + Loop_INDEX - START_pozice] = halda_HODNOTA[objekt_odkaz + 2 + Loop_INDEX];
        return 반환값;
    }
    static int spojit_SMS(int 첫값, int bajt_data) {
        if (!objekt_HODNOTA(첫값, 1) || !objekt_HODNOTA(bajt_data, 1)) return 0;
        int položka_POČET = halda_HODNOTA[첫값 + 1], metoda_INDEX = halda_HODNOTA[bajt_data + 1], 반환값 = přidělit_Storage(1, položka_POČET + metoda_INDEX); if (chyba) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < položka_POČET; Loop_INDEX++) halda_HODNOTA[반환값 + 2 + Loop_INDEX] = halda_HODNOTA[첫값 + 2 + Loop_INDEX];
        for (int Loop_INDEX = 0; Loop_INDEX < metoda_INDEX; Loop_INDEX++) halda_HODNOTA[반환값 + 2 + položka_POČET + Loop_INDEX] = halda_HODNOTA[bajt_data + 2 + Loop_INDEX];
        return 반환값;
    }
    static boolean 기본호출(int vlastník, int název_konstanta, int popisovač_konstanta, int příkaz_KÓD) {
        if (Word_SMS(vlastník, "čeština/vlastní/실행인수") && příkaz_KÓD == 184) {
            if (Word_SMS(název_konstanta, "zboží_POČET") && Word_SMS(popisovač_konstanta, "()I")) { 넣기(uživatelský_prostor.인수개수() - 1, 1); return true; }
            if (Word_SMS(název_konstanta, "text") && Word_SMS(popisovač_konstanta, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= uživatelský_prostor.인수개수() - 1) 예외던짐(29, "Provést_příkaz argumenty 범위를 벗어났습니다");
                else 넣기(hostit_znak(uživatelský_prostor.argumenty(순번 + 1)), 2);
                return true;
            }
            selhání_HODNOTA("지원하지 않는 čeština Provést_příkaz argumenty 호출"); return true;
        }
        if (Word_SMS(vlastník, "čeština/vlastní/pracovník")) { Proces_vlákno(název_konstanta, popisovač_konstanta, příkaz_KÓD, true); return true; }
        if (한국어화면소유(vlastník)) { 한국어화면호출(vlastník, název_konstanta, popisovač_konstanta, příkaz_KÓD); return true; }
        if (화면소유(vlastník)) { 화면호출(vlastník, název_konstanta, popisovač_konstanta, příkaz_KÓD); return true; }
        if (Word_SMS(vlastník, "java/net/Socket") || Word_SMS(vlastník, "java/net/ServerSocket") || Word_SMS(vlastník, "java/io/InputStream") || Word_SMS(vlastník, "java/io/OutputStream")) { 흐름호출(vlastník, název_konstanta, popisovač_konstanta, příkaz_KÓD); return true; }
        if (Word_SMS(vlastník, "čeština/vlastní/jádro_HODNOTA") && příkaz_KÓD == 184) {
            if (Word_SMS(název_konstanta, "화면너비") && Word_SMS(popisovač_konstanta, "()I")) { 넣기(uživatelský_prostor.화면너비(), 1); return true; }
            if (Word_SMS(název_konstanta, "화면높이") && Word_SMS(popisovač_konstanta, "()I")) { 넣기(uživatelský_prostor.화면높이(), 1); return true; }
            if (Word_SMS(název_konstanta, "밀리초") && Word_SMS(popisovač_konstanta, "()I")) { 넣기(uživatelský_prostor.밀리초(), 1); return true; }
            if (Word_SMS(název_konstanta, "그림대기") && Word_SMS(popisovač_konstanta, "()I")) { 넣기(uživatelský_prostor.그림대기(), 1); return true; }
            if (Word_SMS(název_konstanta, "obdélník") && Word_SMS(popisovač_konstanta, "(IIIII)I")) { int 색상 = 빼기(1), výška_HODNOTA = 빼기(1), 너비 = 빼기(1), Y_souřadnice = 빼기(1), souřadnice_x = 빼기(1); 넣기(uživatelský_prostor.obdélník(souřadnice_x, Y_souřadnice, 너비, výška_HODNOTA, 색상), 1); return true; }
        }
        if (Word_SMS(vlastník, "java/net/InetAddress") || Word_SMS(vlastník, "java/net/DatagramPacket") || Word_SMS(vlastník, "java/net/DatagramSocket")) { 통신호출(vlastník, název_konstanta, popisovač_konstanta, příkaz_KÓD); return true; }
        if (Word_SMS(vlastník, "java/lang/Thread")) { 가닥호출(název_konstanta, popisovač_konstanta, příkaz_KÓD); return true; }
        if (Word_SMS(vlastník, "java/lang/Object")) {
            if (Word_SMS(název_konstanta, "<init>") && Word_SMS(popisovač_konstanta, "()V") && příkaz_KÓD == 183) { informační_systémy_platný_objekt(빼기(2)); return true; }
            if (Word_SMS(název_konstanta, "equals") && Word_SMS(popisovač_konstanta, "(Ljava/lang/Object;)Z")) { int bajt_data = 빼기(2), 첫값 = 빼기(2); if (informační_systémy_platný_objekt(첫값)) 넣기(첫값 == bajt_data ? 1 : 0, 1); return true; }
        }
        if (výjimka_konstanta(vlastník) != 0) {
            if (Word_SMS(název_konstanta, "<init>") && příkaz_KÓD == 183 && (Word_SMS(popisovač_konstanta, "()V") || Word_SMS(popisovač_konstanta, "(Ljava/lang/String;)V"))) {
                int výzva = Word_SMS(popisovač_konstanta, "()V") ? 0 : 빼기(2), objekt_odkaz = 빼기(2);
                if (objekt_HODNOTA(objekt_odkaz, 9)) { halda_HODNOTA[objekt_odkaz + 3] = výzva; halda_odkaz[objekt_odkaz + 3] = 1; } return true;
            }
            if ((Word_SMS(název_konstanta, "getMessage") || Word_SMS(název_konstanta, "설명")) && Word_SMS(popisovač_konstanta, "()Ljava/lang/String;")) { int objekt_odkaz = 빼기(2); if (objekt_HODNOTA(objekt_odkaz, 9)) 넣기(halda_HODNOTA[objekt_odkaz + 3], 2); return true; }
        }
        if (Word_SMS(vlastník, "java/lang/String")) {
            if (příkaz_KÓD == 182 && Word_SMS(název_konstanta, "getBytes") && (Word_SMS(popisovač_konstanta, "()[B") || Word_SMS(popisovač_konstanta, "(Ljava/lang/String;)[B"))) {
                int Encoding_název = Word_SMS(popisovač_konstanta, "()[B") ? 0 : 빼기(2), objekt_odkaz = 빼기(2);
                if (!objekt_HODNOTA(objekt_odkaz, 1)) return true;
                if (Encoding_název != 0 && !texty_stejné(Encoding_název, hostit_znak("UTF-8"), false) && !texty_stejné(Encoding_název, hostit_znak("UTF8"), false) && !texty_stejné(Encoding_název, hostit_znak("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int položka_POČET = halda_HODNOTA[objekt_odkaz + 1], 반환값 = přidělit_Storage(20, položka_POČET * 3), 사용수 = 0; if (chyba) return true;
                for (int vnitřní_pozice = 0; vnitřní_pozice < položka_POČET; vnitřní_pozice++) {
                    int bod_kódu = halda_HODNOTA[objekt_odkaz + 2 + vnitřní_pozice];
                    if (bod_kódu >= 0xd800 && bod_kódu <= 0xdbff && vnitřní_pozice + 1 < položka_POČET && halda_HODNOTA[objekt_odkaz + 3 + vnitřní_pozice] >= 0xdc00 && halda_HODNOTA[objekt_odkaz + 3 + vnitřní_pozice] <= 0xdfff) bod_kódu = 0x10000 + ((bod_kódu - 0xd800) << 10) + halda_HODNOTA[objekt_odkaz + 2 + ++vnitřní_pozice] - 0xdc00;
                    else if (bod_kódu >= 0xd800 && bod_kódu <= 0xdfff) bod_kódu = '?';
                    if (bod_kódu < 128) halda_HODNOTA[반환값 + 2 + 사용수++] = bod_kódu;
                    else { int bajt_POČET = bod_kódu < 2048 ? 2 : bod_kódu < 65536 ? 3 : 4; halda_HODNOTA[반환값 + 2 + 사용수++] = (byte)((bajt_POČET == 2 ? 192 : bajt_POČET == 3 ? 224 : 240) | bod_kódu >> (6 * (bajt_POČET - 1))); for (int Porovnání_pozice = bajt_POČET - 1; Porovnání_pozice > 0; Porovnání_pozice--) halda_HODNOTA[반환값 + 2 + 사용수++] = (byte)(128 | bod_kódu >> (6 * (Porovnání_pozice - 1)) & 63); }
                }
                halda_HODNOTA[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (příkaz_KÓD == 184 && Word_SMS(název_konstanta, "valueOf") && Word_SMS(popisovač_konstanta, "(I)Ljava/lang/String;")) { 넣기(číslice_znak(빼기(1)), 2); return true; }
            if (příkaz_KÓD != 182) return false;
            if (Word_SMS(název_konstanta, "equals") && Word_SMS(popisovač_konstanta, "(Ljava/lang/Object;)Z")) { int bajt_data = 빼기(2), 첫값 = 빼기(2); if (objekt_HODNOTA(첫값, 1)) 넣기(texty_stejné(첫값, bajt_data, false) ? 1 : 0, 1); return true; }
            if (Word_SMS(název_konstanta, "isEmpty") && Word_SMS(popisovač_konstanta, "()Z")) { int 첫값 = 빼기(2); if (objekt_HODNOTA(첫값, 1)) 넣기(halda_HODNOTA[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Word_SMS(název_konstanta, "substring") && (Word_SMS(popisovač_konstanta, "(I)Ljava/lang/String;") || Word_SMS(popisovač_konstanta, "(II)Ljava/lang/String;"))) {
                boolean SEKUNDA_HODNOTA = Word_SMS(popisovač_konstanta, "(II)Ljava/lang/String;"); int konec_pozice = SEKUNDA_HODNOTA ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (objekt_HODNOTA(첫값, 1)) 넣기(글조각(첫값, 시작점, SEKUNDA_HODNOTA ? konec_pozice : halda_HODNOTA[첫값 + 1]), 2); return true;
            }
            if (Word_SMS(název_konstanta, "concat") && Word_SMS(popisovač_konstanta, "(Ljava/lang/String;)Ljava/lang/String;")) { int bajt_data = 빼기(2), 첫값 = 빼기(2); 넣기(spojit_SMS(첫값, bajt_data), 2); return true; }
            if (Word_SMS(název_konstanta, "hashCode") && Word_SMS(popisovač_konstanta, "()I")) { int 첫값 = 빼기(2), hodnota_hash_HODNOTA = 0; if (objekt_HODNOTA(첫값, 1)) { for (int Loop_INDEX = 0; Loop_INDEX < halda_HODNOTA[첫값 + 1]; Loop_INDEX++) hodnota_hash_HODNOTA = hodnota_hash_HODNOTA * 31 + halda_HODNOTA[첫값 + 2 + Loop_INDEX]; 넣기(hodnota_hash_HODNOTA, 1); } return true; }
            if (Word_SMS(název_konstanta, "toString") && Word_SMS(popisovač_konstanta, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (objekt_HODNOTA(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Word_SMS(vlastník, "java/lang/Integer")) {
            if (příkaz_KÓD == 184 && Word_SMS(název_konstanta, "valueOf") && Word_SMS(popisovač_konstanta, "(I)Ljava/lang/Integer;")) { int data_HODNOTA = 빼기(1), objekt_odkaz = data_HODNOTA >= -128 && data_HODNOTA <= 127 ? Store_integer[data_HODNOTA + 128] : 0; if (objekt_odkaz == 0) { objekt_odkaz = přidělit_Storage(12, 1); if (!chyba) { halda_HODNOTA[objekt_odkaz + 2] = data_HODNOTA; if (data_HODNOTA >= -128 && data_HODNOTA <= 127) Store_integer[data_HODNOTA + 128] = objekt_odkaz; } } 넣기(objekt_odkaz, 2); return true; }
            if (příkaz_KÓD == 183 && Word_SMS(název_konstanta, "<init>") && Word_SMS(popisovač_konstanta, "(I)V")) { int data_HODNOTA = 빼기(1), objekt_odkaz = 빼기(2); if (objekt_HODNOTA(objekt_odkaz, 12)) halda_HODNOTA[objekt_odkaz + 2] = data_HODNOTA; return true; }
            if (příkaz_KÓD == 182 && Word_SMS(název_konstanta, "intValue") && Word_SMS(popisovač_konstanta, "()I")) { int objekt_odkaz = 빼기(2); if (objekt_HODNOTA(objekt_odkaz, 12)) 넣기(halda_HODNOTA[objekt_odkaz + 2], 1); return true; }
            if (příkaz_KÓD == 184 && Word_SMS(název_konstanta, "toString") && Word_SMS(popisovač_konstanta, "(I)Ljava/lang/String;")) { 넣기(číslice_znak(빼기(1)), 2); return true; }
        }
        if (Word_SMS(vlastník, "java/lang/Math") && příkaz_KÓD == 184) {
            if (Word_SMS(název_konstanta, "abs") && Word_SMS(popisovač_konstanta, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((Word_SMS(název_konstanta, "min") || Word_SMS(název_konstanta, "max")) && Word_SMS(popisovač_konstanta, "(II)I")) { int bajt_data = 빼기(1), 첫값 = 빼기(1); 넣기(Word_SMS(název_konstanta, "min") ? (첫값 < bajt_data ? 첫값 : bajt_data) : (첫값 > bajt_data ? 첫값 : bajt_data), 1); return true; }
        }
        if (Word_SMS(vlastník, "java/lang/System") && příkaz_KÓD == 184) {
            if (Word_SMS(název_konstanta, "gc") && Word_SMS(popisovač_konstanta, "()V")) { 수거(); return true; }
            if (Word_SMS(název_konstanta, "arraycopy") && Word_SMS(popisovač_konstanta, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int položka_POČET = 빼기(1), cíl_HODNOTA_INDEX = 빼기(1), bajt_data = 빼기(2), START_pozice = 빼기(1), 첫값 = 빼기(2);
                if (informační_systémy_platný_objekt(첫값) && informační_systémy_platný_objekt(bajt_data)) {
                    int oblast_KÓD = halda_HODNOTA[첫값];
                    if (halda_HODNOTA[bajt_data] != oblast_KÓD || (oblast_KÓD != 2 && oblast_KÓD != 3 && (oblast_KÓD < 20 || oblast_KÓD > 23))) selhání_HODNOTA("arraycopy type mismatch");
                    else if (položka_POČET < 0 || START_pozice < 0 || cíl_HODNOTA_INDEX < 0 || START_pozice > halda_HODNOTA[첫값 + 1] - položka_POČET || cíl_HODNOTA_INDEX > halda_HODNOTA[bajt_data + 1] - položka_POČET) selhání_HODNOTA("ArrayIndexOutOfBoundsException");
                    else if (첫값 == bajt_data && cíl_HODNOTA_INDEX > START_pozice) { for (int Loop_INDEX = položka_POČET - 1; Loop_INDEX >= 0; Loop_INDEX--) halda_HODNOTA[bajt_data + 2 + cíl_HODNOTA_INDEX + Loop_INDEX] = halda_HODNOTA[첫값 + 2 + START_pozice + Loop_INDEX]; }
                    else { for (int Loop_INDEX = 0; Loop_INDEX < položka_POČET && !chyba; Loop_INDEX++) { int data_HODNOTA = halda_HODNOTA[첫값 + 2 + START_pozice + Loop_INDEX]; if (oblast_KÓD != 3 || 배열저장가능(bajt_data, data_HODNOTA)) halda_HODNOTA[bajt_data + 2 + cíl_HODNOTA_INDEX + Loop_INDEX] = data_HODNOTA; } }
                }
                return true;
            }
        }
        if (Word_SMS(vlastník, "java/util/ArrayList") || Word_SMS(vlastník, "java/util/List") || Word_SMS(vlastník, "java/util/HashMap") || Word_SMS(vlastník, "java/util/Map")) {
            모음호출(vlastník, název_konstanta, popisovač_konstanta, příkaz_KÓD); return true;
        }
        return false;
    }
    static void 모음늘리기(int objekt_odkaz, int 필요수) {
        int Předchozí_HODNOTA = halda_HODNOTA[objekt_odkaz + 2], kapacita_data = Předchozí_HODNOTA == 0 ? 0 : halda_HODNOTA[Předchozí_HODNOTA + 1];
        if (kapacita_data >= 필요수) return;
        int Další_pozice = kapacita_data < 8 ? 8 : kapacita_data * 2; if (Další_pozice < 필요수) Další_pozice = 필요수;
        int data_pole = přidělit_Storage(3, Další_pozice); if (chyba) return;
        for (int Loop_INDEX = 0; Loop_INDEX < kapacita_data; Loop_INDEX++) halda_HODNOTA[data_pole + 2 + Loop_INDEX] = halda_HODNOTA[Předchozí_HODNOTA + 2 + Loop_INDEX];
        halda_HODNOTA[objekt_odkaz + 2] = data_pole; halda_odkaz[objekt_odkaz + 2] = 1;
    }
    static void 모음호출(int vlastník, int název_konstanta, int popisovač_konstanta, int příkaz_KÓD) {
        boolean 대응참조 = Word_SMS(vlastník, "java/util/HashMap") || Word_SMS(vlastník, "java/util/Map"); int oblast_KÓD = 대응참조 ? 11 : 10;
        if (Word_SMS(název_konstanta, "<init>") && příkaz_KÓD == 183 && Word_SMS(popisovač_konstanta, "()V")) { int objekt_odkaz = 빼기(2); if (objekt_HODNOTA(objekt_odkaz, oblast_KÓD)) 모음늘리기(objekt_odkaz, 8); return; }
        if (příkaz_KÓD != 182 && příkaz_KÓD != 185) { selhání_HODNOTA("invalid collection invocation"); return; }
        if (Word_SMS(název_konstanta, "size") && Word_SMS(popisovač_konstanta, "()I") || Word_SMS(název_konstanta, "isEmpty") && Word_SMS(popisovač_konstanta, "()Z")) {
            int objekt_odkaz = 빼기(2); if (objekt_HODNOTA(objekt_odkaz, oblast_KÓD)) 넣기(Word_SMS(název_konstanta, "size") ? halda_HODNOTA[objekt_odkaz + 3] : halda_HODNOTA[objekt_odkaz + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Word_SMS(název_konstanta, "clear") && Word_SMS(popisovač_konstanta, "()V")) { int objekt_odkaz = 빼기(2); if (objekt_HODNOTA(objekt_odkaz, oblast_KÓD)) { int data_pole = halda_HODNOTA[objekt_odkaz + 2]; for (int Loop_INDEX = 0; Loop_INDEX < halda_HODNOTA[data_pole + 1]; Loop_INDEX++) halda_HODNOTA[data_pole + 2 + Loop_INDEX] = 0; halda_HODNOTA[objekt_odkaz + 3] = 0; } return; }
        if (!대응참조 && Word_SMS(název_konstanta, "add") && Word_SMS(popisovač_konstanta, "(Ljava/lang/Object;)Z")) {
            int data_HODNOTA = 빼기(2), objekt_odkaz = 빼기(2); if (!objekt_HODNOTA(objekt_odkaz, 10)) return;
            int položka_POČET = halda_HODNOTA[objekt_odkaz + 3]; 모음늘리기(objekt_odkaz, položka_POČET + 1); if (!chyba) { halda_HODNOTA[halda_HODNOTA[objekt_odkaz + 2] + 2 + položka_POČET] = data_HODNOTA; halda_HODNOTA[objekt_odkaz + 3] = položka_POČET + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Word_SMS(název_konstanta, "get") || Word_SMS(název_konstanta, "remove")) && Word_SMS(popisovač_konstanta, "(I)Ljava/lang/Object;") || !대응참조 && Word_SMS(název_konstanta, "set") && Word_SMS(popisovač_konstanta, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean informační_systémy_Přiřazený = Word_SMS(název_konstanta, "set"); int data_HODNOTA = informační_systémy_Přiřazený ? 빼기(2) : 0, položka_pozice = 빼기(1), objekt_odkaz = 빼기(2);
            if (!objekt_HODNOTA(objekt_odkaz, 10)) return;
            int položka_POČET = halda_HODNOTA[objekt_odkaz + 3], data_pole = halda_HODNOTA[objekt_odkaz + 2];
            if (položka_pozice < 0 || položka_pozice >= položka_POČET) { 예외던짐(6, "list index"); return; }
            int Předchozí_HODNOTA = halda_HODNOTA[data_pole + 2 + položka_pozice];
            if (informační_systémy_Přiřazený) halda_HODNOTA[data_pole + 2 + položka_pozice] = data_HODNOTA;
            if (Word_SMS(název_konstanta, "remove")) { for (int Loop_INDEX = položka_pozice + 1; Loop_INDEX < položka_POČET; Loop_INDEX++) halda_HODNOTA[data_pole + 1 + Loop_INDEX] = halda_HODNOTA[data_pole + 2 + Loop_INDEX]; halda_HODNOTA[data_pole + 1 + položka_POČET] = 0; halda_HODNOTA[objekt_odkaz + 3] = položka_POČET - 1; }
            넣기(Předchozí_HODNOTA, 2); return;
        }
        if (대응참조 && (Word_SMS(název_konstanta, "get") || Word_SMS(název_konstanta, "remove")) && Word_SMS(popisovač_konstanta, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(název_konstanta, "put") && Word_SMS(popisovač_konstanta, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(název_konstanta, "containsKey") && Word_SMS(popisovač_konstanta, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Word_SMS(název_konstanta, "put"), odebrat = Word_SMS(název_konstanta, "remove");
            int data_HODNOTA = 넣기여부 ? 빼기(2) : 0, Klíč_odkaz = 빼기(2), objekt_odkaz = 빼기(2); if (!objekt_HODNOTA(objekt_odkaz, 11)) return;
            int položka_POČET = halda_HODNOTA[objekt_odkaz + 3], data_pole = halda_HODNOTA[objekt_odkaz + 2], 찾은여부 = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < položka_POČET; Loop_INDEX++) if (값같음(Klíč_odkaz, halda_HODNOTA[data_pole + 2 + 2 * Loop_INDEX])) { 찾은여부 = Loop_INDEX; break; }
            int Předchozí_HODNOTA = 찾은여부 < 0 ? 0 : halda_HODNOTA[data_pole + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(objekt_odkaz, (položka_POČET + 1) * 2); data_pole = halda_HODNOTA[objekt_odkaz + 2]; 찾은여부 = položka_POČET; if (!chyba) halda_HODNOTA[objekt_odkaz + 3] = položka_POČET + 1; }
                if (!chyba) { halda_HODNOTA[data_pole + 2 + 2 * 찾은여부] = Klíč_odkaz; halda_HODNOTA[data_pole + 3 + 2 * 찾은여부] = data_HODNOTA; }
            }
            if (odebrat && 찾은여부 >= 0) { for (int Loop_INDEX = 찾은여부 + 1; Loop_INDEX < položka_POČET; Loop_INDEX++) { halda_HODNOTA[data_pole + 2 * Loop_INDEX] = halda_HODNOTA[data_pole + 2 + 2 * Loop_INDEX]; halda_HODNOTA[data_pole + 1 + 2 * Loop_INDEX] = halda_HODNOTA[data_pole + 3 + 2 * Loop_INDEX]; } halda_HODNOTA[data_pole + 2 * položka_POČET] = 0; halda_HODNOTA[data_pole + 1 + 2 * položka_POČET] = 0; halda_HODNOTA[objekt_odkaz + 3] = položka_POČET - 1; }
            if (Word_SMS(název_konstanta, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(Předchozí_HODNOTA, 2);
            return;
        }
        selhání_HODNOTA("unsupported collection method");
    }
    static boolean 잠금얻기(int objekt_odkaz) {
        if (!informační_systémy_platný_objekt(objekt_odkaz)) return false;
        if (잠금깊이[objekt_odkaz] != 0 && zámek_vlastník[objekt_odkaz] != dobrá_vlákno + 1) { žádost_o_změnu = true; return false; }
        zámek_vlastník[objekt_odkaz] = dobrá_vlákno + 1; 잠금깊이[objekt_odkaz]++; return true;
    }
    static void verze_zámek(int objekt_odkaz) {
        if (!informační_systémy_platný_objekt(objekt_odkaz)) return;
        if (잠금깊이[objekt_odkaz] == 0 || zámek_vlastník[objekt_odkaz] != dobrá_vlákno + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[objekt_odkaz] == 0) zámek_vlastník[objekt_odkaz] = 0;
    }
    static boolean SWITCH_vlákno() {
        vlákno_rámec[dobrá_vlákno] = rámec_INDEX;
        if (rámec_INDEX < dobrá_vlákno * 32) vlákno_Stav[dobrá_vlákno] = 3;
        for (int Loop_INDEX = 0; Loop_INDEX < počet_vláken; Loop_INDEX++) if (vlákno_Stav[Loop_INDEX] == 2 && vlákno_Stav[가닥대기[Loop_INDEX]] == 3) vlákno_Stav[Loop_INDEX] = 1;
        for (int Loop_INDEX = 1; Loop_INDEX <= počet_vláken; Loop_INDEX++) {
            int Další_pozice = (dobrá_vlákno + Loop_INDEX) % počet_vláken;
            if (vlákno_Stav[Další_pozice] == 1) { dobrá_vlákno = Další_pozice; rámec_INDEX = vlákno_rámec[Další_pozice]; žádost_o_změnu = false; return true; }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < počet_vláken; Loop_INDEX++) if (vlákno_Stav[Loop_INDEX] != 3) { selhání_HODNOTA("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int název_konstanta, int popisovač_konstanta, int příkaz_KÓD) { Proces_vlákno(název_konstanta, popisovač_konstanta, příkaz_KÓD, false); }
    static void Proces_vlákno(int název_konstanta, int popisovač_konstanta, int příkaz_KÓD, boolean čeština) {
        if (příkaz_KÓD == 184 && Word_SMS(název_konstanta, čeština ? "YIELD_úkol" : "yield") && Word_SMS(popisovač_konstanta, "()V")) { žádost_o_změnu = true; return; }
        if (příkaz_KÓD == 184 && Word_SMS(název_konstanta, "currentThread") && Word_SMS(popisovač_konstanta, "()Ljava/lang/Thread;")) { 넣기(vlákno_objekt[dobrá_vlákno], 2); return; }
        if (příkaz_KÓD == 183 && Word_SMS(název_konstanta, "<init>") && (Word_SMS(popisovač_konstanta, "()V") || Word_SMS(popisovač_konstanta, čeština ? "(Lčeština/vlastní/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int cíl_ODKAZ = Word_SMS(popisovač_konstanta, "()V") ? 0 : 빼기(2), objekt_odkaz = 빼기(2);
            if (!informační_systémy_platný_objekt(objekt_odkaz)) return;
            if (halda_HODNOTA[objekt_odkaz] == 13) { halda_HODNOTA[objekt_odkaz + 2] = cíl_ODKAZ; halda_odkaz[objekt_odkaz + 2] = 1; }
            else if (cíl_ODKAZ != 0) selhání_HODNOTA("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (příkaz_KÓD == 182 && (Word_SMS(název_konstanta, čeština ? "START_úkol" : "start") || Word_SMS(název_konstanta, čeština ? "기다리기" : "join")) && Word_SMS(popisovač_konstanta, "()V") || příkaz_KÓD == 182 && Word_SMS(název_konstanta, čeština ? "살아있는가" : "isAlive") && Word_SMS(popisovač_konstanta, "()Z")) {
            int objekt_odkaz = 빼기(2); if (!informační_systémy_platný_objekt(objekt_odkaz)) return;
            int účet_HODNOTA = -1; for (int Loop_INDEX = 0; Loop_INDEX < počet_vláken; Loop_INDEX++) if (vlákno_objekt[Loop_INDEX] == objekt_odkaz) účet_HODNOTA = Loop_INDEX;
            if (Word_SMS(název_konstanta, čeština ? "살아있는가" : "isAlive")) { 넣기(účet_HODNOTA >= 0 && vlákno_Stav[účet_HODNOTA] != 3 ? 1 : 0, 1); return; }
            if (Word_SMS(název_konstanta, čeština ? "기다리기" : "join")) { if (účet_HODNOTA >= 0 && vlákno_Stav[účet_HODNOTA] != 3) { 가닥대기[dobrá_vlákno] = účet_HODNOTA; vlákno_Stav[dobrá_vlákno] = 2; žádost_o_změnu = true; } return; }
            if (účet_HODNOTA >= 0) { 예외던짐(čeština ? 38 : 16, "thread already started"); return; }
            if (počet_vláken == 4) { selhání_HODNOTA("thread limit (4 including main)"); return; }
            int cíl_ODKAZ = halda_HODNOTA[objekt_odkaz] == 13 ? halda_HODNOTA[objekt_odkaz + 2] : objekt_odkaz;
            int Soubor_INDEX = cíl_ODKAZ > 0 && halda_HODNOTA[cíl_ODKAZ] >= 32 ? název_metoda(halda_HODNOTA[cíl_ODKAZ] - 32, čeština ? "Spustit" : "run", "()V") : -1;
            if (cíl_ODKAZ != 0 && Soubor_INDEX < 0) { selhání_HODNOTA("Runnable.run required"); return; }
            účet_HODNOTA = počet_vláken++; vlákno_objekt[účet_HODNOTA] = objekt_odkaz; vlákno_cíl[účet_HODNOTA] = cíl_ODKAZ;
            int rámec = účet_HODNOTA * 32; vlákno_rámec[účet_HODNOTA] = Soubor_INDEX < 0 ? rámec - 1 : rámec; vlákno_Stav[účet_HODNOTA] = Soubor_INDEX < 0 ? 3 : 1;
            if (Soubor_INDEX >= 0) { rámec_metoda[rámec] = Soubor_INDEX; rámec_pozice[rámec] = metoda_START[Soubor_INDEX]; místní_HODNOTA[rámec * 128] = cíl_ODKAZ; místní_TYP[rámec * 128] = 2; }
            return;
        }
        selhání_HODNOTA("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], ODKAZ_SMS = new int[16];
    static int místní_ODKAZ() { return ODKAZ_objekt(0x7f000001); }
    static int ODKAZ_objekt(int HODNOTA) { int objekt_odkaz = přidělit_Storage(14, 1); if (!chyba) halda_HODNOTA[objekt_odkaz + 2] = HODNOTA; return objekt_odkaz; }
    static int 주소해독(int objekt_odkaz) {
        if (objekt_odkaz == 0 || texty_stejné(objekt_odkaz, hostit_znak("localhost"), false)) return 0x7f000001;
        if (!objekt_HODNOTA(objekt_odkaz, 1)) return 0;
        int data_HODNOTA = 0, celkem_POČET = 0, ODKAZ_bajt = 0, 자릿수 = 0, položka_POČET = halda_HODNOTA[objekt_odkaz + 1];
        for (int Loop_INDEX = 0; Loop_INDEX <= položka_POČET; Loop_INDEX++) {
            int bod_kódu = Loop_INDEX == položka_POČET ? '.' : halda_HODNOTA[objekt_odkaz + 2 + Loop_INDEX];
            if (bod_kódu == '.') { if (자릿수 == 0 || celkem_POČET == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } data_HODNOTA = data_HODNOTA << 8 | ODKAZ_bajt; celkem_POČET++; ODKAZ_bajt = 자릿수 = 0; }
            else { if (bod_kódu < '0' || bod_kódu > '9' || ++자릿수 > 3 || (ODKAZ_bajt = ODKAZ_bajt * 10 + bod_kódu - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (celkem_POČET != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return data_HODNOTA;
    }
    static int ODKAZ_znak(int data_HODNOTA) {
        int položka_POČET = 0;
        for (int posunout = 24; posunout >= 0; posunout -= 8) {
            int ODKAZ_bajt = data_HODNOTA >>> posunout & 255;
            if (ODKAZ_bajt >= 100) ODKAZ_SMS[položka_POČET++] = '0' + ODKAZ_bajt / 100;
            if (ODKAZ_bajt >= 10) ODKAZ_SMS[položka_POČET++] = '0' + ODKAZ_bajt / 10 % 10;
            ODKAZ_SMS[položka_POČET++] = '0' + ODKAZ_bajt % 10; if (posunout != 0) ODKAZ_SMS[položka_POČET++] = '.';
        }
        int objekt_odkaz = přidělit_Storage(1, položka_POČET); if (!chyba) for (int Loop_INDEX = 0; Loop_INDEX < položka_POČET; Loop_INDEX++) halda_HODNOTA[objekt_odkaz + 2 + Loop_INDEX] = ODKAZ_SMS[Loop_INDEX]; return objekt_odkaz;
    }
    static void 통신호출(int vlastník, int název_konstanta, int popisovač_konstanta, int příkaz_KÓD) {
        if (Word_SMS(vlastník, "java/net/InetAddress")) {
            if (příkaz_KÓD == 184 && Word_SMS(název_konstanta, "getLoopbackAddress") && Word_SMS(popisovač_konstanta, "()Ljava/net/InetAddress;")) { 넣기(místní_ODKAZ(), 2); return; }
            if (příkaz_KÓD == 184 && Word_SMS(název_konstanta, "getByName") && Word_SMS(popisovač_konstanta, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int data_HODNOTA = 주소해독(빼기(2)); if (던진객체 == 0 && !chyba) 넣기(ODKAZ_objekt(data_HODNOTA), 2); return;
            }
            if (příkaz_KÓD == 182 && Word_SMS(název_konstanta, "getHostAddress") && Word_SMS(popisovač_konstanta, "()Ljava/lang/String;")) { int objekt_odkaz = 빼기(2); if (objekt_HODNOTA(objekt_odkaz, 14)) 넣기(ODKAZ_znak(halda_HODNOTA[objekt_odkaz + 2]), 2); return; }
        }
        if (Word_SMS(vlastník, "java/net/DatagramPacket")) {
            if (příkaz_KÓD == 183 && Word_SMS(název_konstanta, "<init>") && (Word_SMS(popisovač_konstanta, "([BI)V") || Word_SMS(popisovač_konstanta, "([BILjava/net/InetAddress;I)V"))) {
                boolean cíl_HODNOTA_odkaz = Word_SMS(popisovač_konstanta, "([BILjava/net/InetAddress;I)V"); int číslo_portu = cíl_HODNOTA_odkaz ? 빼기(1) : 0, ODKAZ_odkaz = cíl_HODNOTA_odkaz ? 빼기(2) : 0;
                int položka_POČET = 빼기(1), data_pole = 빼기(2), objekt_odkaz = 빼기(2);
                if (!objekt_HODNOTA(objekt_odkaz, 16) || !objekt_HODNOTA(data_pole, 20)) return;
                if (položka_POČET < 0 || položka_POČET > halda_HODNOTA[data_pole + 1] || číslo_portu < 0 || číslo_portu > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (ODKAZ_odkaz != 0 && !objekt_HODNOTA(ODKAZ_odkaz, 14)) return;
                halda_HODNOTA[objekt_odkaz + 2] = data_pole; halda_odkaz[objekt_odkaz + 2] = 1; halda_HODNOTA[objekt_odkaz + 3] = položka_POČET;
                halda_HODNOTA[objekt_odkaz + 4] = ODKAZ_odkaz; halda_odkaz[objekt_odkaz + 4] = 1; halda_HODNOTA[objekt_odkaz + 5] = číslo_portu; return;
            }
            if (příkaz_KÓD == 182 && Word_SMS(název_konstanta, "setLength") && Word_SMS(popisovač_konstanta, "(I)V")) {
                int položka_POČET = 빼기(1), objekt_odkaz = 빼기(2); if (!objekt_HODNOTA(objekt_odkaz, 16)) return;
                if (položka_POČET < 0 || položka_POČET > halda_HODNOTA[halda_HODNOTA[objekt_odkaz + 2] + 1]) 예외던짐(9, "invalid datagram length"); else halda_HODNOTA[objekt_odkaz + 3] = položka_POČET; return;
            }
            if (příkaz_KÓD == 182 && (Word_SMS(název_konstanta, "getData") && Word_SMS(popisovač_konstanta, "()[B") || Word_SMS(název_konstanta, "getLength") && Word_SMS(popisovač_konstanta, "()I") || Word_SMS(název_konstanta, "getAddress") && Word_SMS(popisovač_konstanta, "()Ljava/net/InetAddress;") || Word_SMS(název_konstanta, "getPort") && Word_SMS(popisovač_konstanta, "()I"))) {
                int objekt_odkaz = 빼기(2); if (!objekt_HODNOTA(objekt_odkaz, 16)) return;
                int položka_pozice = Word_SMS(název_konstanta, "getData") ? 2 : Word_SMS(název_konstanta, "getLength") ? 3 : Word_SMS(název_konstanta, "getAddress") ? 4 : 5;
                넣기(halda_HODNOTA[objekt_odkaz + položka_pozice], položka_pozice == 2 || položka_pozice == 4 ? 2 : 1); return;
            }
        }
        if (Word_SMS(vlastník, "java/net/DatagramSocket")) {
            if (příkaz_KÓD == 183 && Word_SMS(název_konstanta, "<init>") && (Word_SMS(popisovač_konstanta, "()V") || Word_SMS(popisovač_konstanta, "(I)V"))) {
                int číslo_portu = Word_SMS(popisovač_konstanta, "()V") ? 0 : 빼기(1), objekt_odkaz = 빼기(2); if (!objekt_HODNOTA(objekt_odkaz, 15)) return;
                if (číslo_portu < 0 || číslo_portu > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = uživatelský_prostor.otevřít_síť(číslo_portu); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else halda_HODNOTA[objekt_odkaz + 2] = 열린파일번호; return;
            }
            if (příkaz_KÓD == 182 && Word_SMS(název_konstanta, "setSoTimeout") && Word_SMS(popisovač_konstanta, "(I)V")) {
                int 밀리초값 = 빼기(1), objekt_odkaz = 빼기(2); if (!objekt_HODNOTA(objekt_odkaz, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else halda_HODNOTA[objekt_odkaz + 3] = 밀리초값; return;
            }
            if (příkaz_KÓD == 182 && Word_SMS(název_konstanta, "getLocalPort") && Word_SMS(popisovač_konstanta, "()I")) { int objekt_odkaz = 빼기(2); if (objekt_HODNOTA(objekt_odkaz, 15)) 넣기(halda_HODNOTA[objekt_odkaz + 2] < 0 ? -1 : uživatelský_prostor.síť_port(halda_HODNOTA[objekt_odkaz + 2]), 1); return; }
            if (příkaz_KÓD == 182 && Word_SMS(název_konstanta, "isClosed") && Word_SMS(popisovač_konstanta, "()Z")) { int objekt_odkaz = 빼기(2); if (objekt_HODNOTA(objekt_odkaz, 15)) 넣기(halda_HODNOTA[objekt_odkaz + 2] < 0 ? 1 : 0, 1); return; }
            if (příkaz_KÓD == 182 && Word_SMS(název_konstanta, "close") && Word_SMS(popisovač_konstanta, "()V")) { int objekt_odkaz = 빼기(2); if (objekt_HODNOTA(objekt_odkaz, 15) && halda_HODNOTA[objekt_odkaz + 2] >= 0) { uživatelský_prostor.Zavřít_Soubor_popisovač(halda_HODNOTA[objekt_odkaz + 2]); halda_HODNOTA[objekt_odkaz + 2] = -1; } return; }
            if (příkaz_KÓD == 182 && (Word_SMS(název_konstanta, "send") || Word_SMS(název_konstanta, "receive")) && Word_SMS(popisovač_konstanta, "(Ljava/net/DatagramPacket;)V")) {
                int paket = 빼기(2), objekt_odkaz = 빼기(2); if (!objekt_HODNOTA(paket, 16) || !objekt_HODNOTA(objekt_odkaz, 15)) return;
                int data_pole = halda_HODNOTA[paket + 2], platný_délka = halda_HODNOTA[paket + 3], 열린파일번호 = halda_HODNOTA[objekt_odkaz + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Word_SMS(název_konstanta, "send")) {
                    if (!objekt_HODNOTA(halda_HODNOTA[paket + 4], 14)) return;
                    if (platný_délka > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < platný_délka; Loop_INDEX++) 통신임시[Loop_INDEX] = halda_HODNOTA[data_pole + 2 + Loop_INDEX];
                    if (uživatelský_prostor.poslat_síť(열린파일번호, halda_HODNOTA[halda_HODNOTA[paket + 4] + 2], halda_HODNOTA[paket + 5], 통신임시, platný_délka) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int položka_POČET = uživatelský_prostor.dostat_síť(열린파일번호, 통신임시, platný_délka > 512 ? 512 : platný_délka);
                    if (položka_POČET == -11) {
                        int aktuální_čas = uživatelský_prostor.밀리초();
                        if (halda_HODNOTA[objekt_odkaz + 4] == 0) halda_HODNOTA[objekt_odkaz + 4] = aktuální_čas + 1;
                        if (halda_HODNOTA[objekt_odkaz + 3] > 0 && aktuální_čas - (halda_HODNOTA[objekt_odkaz + 4] - 1) >= halda_HODNOTA[objekt_odkaz + 3]) { halda_HODNOTA[objekt_odkaz + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(objekt_odkaz, 2); 넣기(paket, 2); rámec_pozice[rámec_INDEX] = 틀명령[rámec_INDEX]; žádost_o_změnu = true; return;
                    }
                    halda_HODNOTA[objekt_odkaz + 4] = 0;
                    if (položka_POČET < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < položka_POČET; Loop_INDEX++) halda_HODNOTA[data_pole + 2 + Loop_INDEX] = (byte)통신임시[Loop_INDEX];
                    halda_HODNOTA[paket + 3] = položka_POČET; halda_HODNOTA[paket + 4] = ODKAZ_objekt(통신임시[513]); halda_odkaz[paket + 4] = 1; halda_HODNOTA[paket + 5] = 통신임시[512];
                }
                return;
            }
        }
        selhání_HODNOTA("unsupported java.net method");
    }
    static boolean 흐름대기(int objekt_odkaz) {
        int aktuální_čas = uživatelský_prostor.밀리초();
        if (halda_HODNOTA[objekt_odkaz + 5] == 0) halda_HODNOTA[objekt_odkaz + 5] = aktuální_čas + 1;
        if (halda_HODNOTA[objekt_odkaz + 3] > 0 && aktuální_čas - (halda_HODNOTA[objekt_odkaz + 5] - 1) >= halda_HODNOTA[objekt_odkaz + 3]) { halda_HODNOTA[objekt_odkaz + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        rámec_pozice[rámec_INDEX] = 틀명령[rámec_INDEX]; žádost_o_změnu = true; return true;
    }
    static void 흐름호출(int vlastník, int název_konstanta, int popisovač_konstanta, int příkaz_KÓD) {
        boolean dostat_stránka = Word_SMS(vlastník, "java/net/ServerSocket"), tok = Word_SMS(vlastník, "java/io/InputStream") || Word_SMS(vlastník, "java/io/OutputStream");
        if (!tok && příkaz_KÓD == 183 && Word_SMS(název_konstanta, "<init>")) {
            boolean 빈여부 = Word_SMS(popisovač_konstanta, "()V"), 이름지정여부 = Word_SMS(popisovač_konstanta, "(Ljava/lang/String;I)V"), 주소지정여부 = Word_SMS(popisovač_konstanta, "(Ljava/net/InetAddress;I)V");
            if (!(빈여부 || dostat_stránka && Word_SMS(popisovač_konstanta, "(I)V") || !dostat_stránka && (이름지정여부 || 주소지정여부))) { selhání_HODNOTA("unsupported socket constructor"); return; }
            int číslo_portu = 빈여부 ? 0 : 빼기(1), ODKAZ_odkaz = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, objekt_odkaz = 빼기(2);
            if (!objekt_HODNOTA(objekt_odkaz, dostat_stránka ? 18 : 17)) return;
            if (číslo_portu < 0 || číslo_portu > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !objekt_HODNOTA(ODKAZ_odkaz, 14)) return;
            int ID_sítě = 이름지정여부 ? 주소해독(ODKAZ_odkaz) : 주소지정여부 ? halda_HODNOTA[ODKAZ_odkaz + 2] : 0x7f000001;
            if (chyba || 던진객체 != 0) return;
            int 열린파일번호 = uživatelský_prostor.tok_řízení(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = 빈여부 ? 0 : dostat_stránka ? uživatelský_prostor.tok_řízení(1, 열린파일번호, číslo_portu) : uživatelský_prostor.spojit_tok(열린파일번호, ID_sítě, číslo_portu);
            if (처리값 < 0) { uživatelský_prostor.Zavřít_Soubor_popisovač(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            halda_HODNOTA[objekt_odkaz + 2] = 열린파일번호; halda_HODNOTA[objekt_odkaz + 4] = číslo_portu; halda_HODNOTA[objekt_odkaz + 6] = 빈여부 ? 0 : 1; return;
        }
        if (!tok && Word_SMS(název_konstanta, "setSoTimeout") && Word_SMS(popisovač_konstanta, "(I)V")) { int 밀리초값 = 빼기(1), objekt_odkaz = 빼기(2); if (!objekt_HODNOTA(objekt_odkaz, dostat_stránka ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else halda_HODNOTA[objekt_odkaz + 3] = 밀리초값; return; }
        if (!tok && Word_SMS(název_konstanta, "close") && Word_SMS(popisovač_konstanta, "()V")) { int objekt_odkaz = 빼기(2); if (objekt_HODNOTA(objekt_odkaz, dostat_stránka ? 18 : 17) && halda_HODNOTA[objekt_odkaz + 2] >= 0) { uživatelský_prostor.Zavřít_Soubor_popisovač(halda_HODNOTA[objekt_odkaz + 2]); halda_HODNOTA[objekt_odkaz + 2] = -1; } return; }
        if (!tok && (Word_SMS(název_konstanta, "getLocalPort") || Word_SMS(název_konstanta, "getPort") || Word_SMS(název_konstanta, "isClosed") || Word_SMS(název_konstanta, "isConnected"))) {
            int objekt_odkaz = 빼기(2); if (!objekt_HODNOTA(objekt_odkaz, dostat_stránka ? 18 : 17)) return;
            넣기(Word_SMS(název_konstanta, "isClosed") ? halda_HODNOTA[objekt_odkaz + 2] < 0 ? 1 : 0 : Word_SMS(název_konstanta, "isConnected") ? halda_HODNOTA[objekt_odkaz + 6] : Word_SMS(název_konstanta, "getPort") ? halda_HODNOTA[objekt_odkaz + 4] : halda_HODNOTA[objekt_odkaz + 2] < 0 ? -1 : uživatelský_prostor.tok_řízení(4, halda_HODNOTA[objekt_odkaz + 2], 0), 1); return;
        }
        if (dostat_stránka && Word_SMS(název_konstanta, "accept") && Word_SMS(popisovač_konstanta, "()Ljava/net/Socket;")) {
            int objekt_odkaz = 빼기(2); if (!objekt_HODNOTA(objekt_odkaz, 18)) return; int 열린파일번호 = uživatelský_prostor.tok_řízení(3, halda_HODNOTA[objekt_odkaz + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(objekt_odkaz)) 넣기(objekt_odkaz, 2); return; }
            halda_HODNOTA[objekt_odkaz + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = přidělit_Storage(17, 5); if (chyba) { uživatelský_prostor.Zavřít_Soubor_popisovač(열린파일번호); return; } halda_HODNOTA[반환값 + 2] = 열린파일번호; halda_HODNOTA[반환값 + 4] = uživatelský_prostor.tok_řízení(5, 열린파일번호, 0); halda_HODNOTA[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!dostat_stránka && !tok && ((Word_SMS(název_konstanta, "getInputStream") && Word_SMS(popisovač_konstanta, "()Ljava/io/InputStream;")) || (Word_SMS(název_konstanta, "getOutputStream") && Word_SMS(popisovač_konstanta, "()Ljava/io/OutputStream;")))) {
            int objekt_odkaz = 빼기(2); if (!objekt_HODNOTA(objekt_odkaz, 17)) return; if (halda_HODNOTA[objekt_odkaz + 2] < 0 || halda_HODNOTA[objekt_odkaz + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = přidělit_Storage(19, 4); if (chyba) return; halda_HODNOTA[반환값 + 2] = objekt_odkaz; halda_odkaz[반환값 + 2] = 1; halda_HODNOTA[반환값 + 3] = Word_SMS(název_konstanta, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (tok) {
            boolean 읽기여부 = Word_SMS(název_konstanta, "read"), informační_systémy_zápis_operace = Word_SMS(název_konstanta, "write"), blok = Word_SMS(popisovač_konstanta, "([B)I") || Word_SMS(popisovač_konstanta, "([B)V"), informační_systémy_SUBARRAY = Word_SMS(popisovač_konstanta, "([BII)I") || Word_SMS(popisovač_konstanta, "([BII)V");
            int položka_POČET = informační_systémy_SUBARRAY ? 빼기(1) : 0, 시작변위 = informační_systémy_SUBARRAY ? 빼기(1) : 0, data_pole = blok || informační_systémy_SUBARRAY ? 빼기(2) : 0;
            int data_HODNOTA = informační_systémy_zápis_operace && Word_SMS(popisovač_konstanta, "(I)V") ? 빼기(1) : 0, objekt_odkaz = 빼기(2);
            if (!objekt_HODNOTA(objekt_odkaz, 19)) return; int nadřazený_odkaz = halda_HODNOTA[objekt_odkaz + 2], 열린파일번호 = halda_HODNOTA[nadřazený_odkaz + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Word_SMS(název_konstanta, "close") && Word_SMS(popisovač_konstanta, "()V")) { uživatelský_prostor.Zavřít_Soubor_popisovač(열린파일번호); halda_HODNOTA[nadřazený_odkaz + 2] = -1; return; }
            if (Word_SMS(název_konstanta, "flush") && Word_SMS(popisovač_konstanta, "()V")) return;
            if ((!읽기여부 && !informační_systémy_zápis_operace) || 읽기여부 != (halda_HODNOTA[objekt_odkaz + 3] == 0)) { selhání_HODNOTA("unsupported stream operation"); return; }
            if (blok || informační_systémy_SUBARRAY) { if (!objekt_HODNOTA(data_pole, 20)) return; if (blok) položka_POČET = halda_HODNOTA[data_pole + 1]; if (시작변위 < 0 || položka_POČET < 0 || 시작변위 > halda_HODNOTA[data_pole + 1] - položka_POČET) { 예외던짐(6, "stream array bounds"); return; } }
            else položka_POČET = 1;
            if (položka_POČET == 0) { if (읽기여부) 넣기(0, 1); return; }
            int dokončeno_POČET = informační_systémy_zápis_operace ? halda_HODNOTA[objekt_odkaz + 4] : 0, 처리값 = 0;
            while (dokončeno_POČET < položka_POČET) {
                처리값 = 읽기여부 ? uživatelský_prostor.파일한바이트읽기(열린파일번호) : uživatelský_prostor.파일한바이트쓰기(열린파일번호, blok || informační_systémy_SUBARRAY ? halda_HODNOTA[data_pole + 2 + 시작변위 + dokončeno_POČET] : data_HODNOTA);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (blok || informační_systémy_SUBARRAY)) halda_HODNOTA[data_pole + 2 + 시작변위 + dokončeno_POČET] = (byte)처리값;
                dokončeno_POČET++; if (읽기여부 && !(blok || informační_systémy_SUBARRAY)) break;
            }
            if (처리값 == -11 && (informační_systémy_zápis_operace || dokončeno_POČET == 0)) {
                halda_HODNOTA[objekt_odkaz + 4] = dokončeno_POČET;
                if (흐름대기(nadřazený_odkaz)) { 넣기(objekt_odkaz, 2); if (blok || informační_systémy_SUBARRAY) 넣기(data_pole, 2); if (informační_systémy_SUBARRAY) { 넣기(시작변위, 1); 넣기(položka_POČET, 1); } if (informační_systémy_zápis_operace && !(blok || informační_systémy_SUBARRAY)) 넣기(data_HODNOTA, 1); } return;
            }
            halda_HODNOTA[objekt_odkaz + 4] = 0; halda_HODNOTA[nadřazený_odkaz + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(dokončeno_POČET == 0 && 처리값 == 256 ? -1 : blok || informační_systémy_SUBARRAY ? dokončeno_POČET : 처리값, 1); return;
        }
        selhání_HODNOTA("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int název_konstanta) {
        if (Word_SMS(název_konstanta, "čeština/vlastní/Okno")) return 24;
        if (Word_SMS(název_konstanta, "čeština/vlastní/Popisek")) return 26;
        if (Word_SMS(název_konstanta, "čeština/vlastní/tlačítko")) return 27;
        if (Word_SMS(název_konstanta, "čeština/vlastní/textové_pole")) return 28;
        if (Word_SMS(název_konstanta, "čeština/vlastní/Akce_povinnost_zvěřejnit")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int název_konstanta) {
        return 한국어화면종(název_konstanta) != 0 || Word_SMS(název_konstanta, "čeština/vlastní/화면구성요소") || Word_SMS(název_konstanta, "čeština/vlastní/událost_fronta");
    }
    static int 화면종(int název_konstanta) {
        int 한국어종 = 한국어화면종(název_konstanta); if (한국어종 != 0) return 한국어종;
        if (Word_SMS(název_konstanta, "javax/swing/JFrame")) return 24;
        if (Word_SMS(název_konstanta, "javax/swing/JPanel")) return 25;
        if (Word_SMS(název_konstanta, "javax/swing/JLabel")) return 26;
        if (Word_SMS(název_konstanta, "javax/swing/JButton")) return 27;
        if (Word_SMS(název_konstanta, "javax/swing/JTextField")) return 28;
        if (Word_SMS(název_konstanta, "java/awt/event/ActionEvent")) return 29;
        if (Word_SMS(název_konstanta, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int název_konstanta) {
        return 화면종(název_konstanta) != 0 || Word_SMS(název_konstanta, "java/awt/Component") || Word_SMS(název_konstanta, "java/awt/Container") || Word_SMS(název_konstanta, "javax/swing/JComponent") || Word_SMS(název_konstanta, "javax/swing/AbstractButton") || Word_SMS(název_konstanta, "javax/swing/text/JTextComponent") || Word_SMS(název_konstanta, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int objekt_odkaz) { if (!informační_systémy_platný_objekt(objekt_odkaz)) return false; if (halda_HODNOTA[objekt_odkaz] < 24 || halda_HODNOTA[objekt_odkaz] > 28) { selhání_HODNOTA("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int objekt_odkaz, int SMS_odkaz) {
        if (SMS_odkaz != 0 && !objekt_HODNOTA(SMS_odkaz, 1)) return;
        int položka_POČET = SMS_odkaz == 0 ? 0 : halda_HODNOTA[SMS_odkaz + 1]; if (položka_POČET > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < položka_POČET; Loop_INDEX++) 화면글임시[Loop_INDEX] = halda_HODNOTA[SMS_odkaz + 2 + Loop_INDEX];
        if (uživatelský_prostor.화면글(halda_HODNOTA[objekt_odkaz + 2], 화면글임시, položka_POČET) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        halda_HODNOTA[objekt_odkaz + 3] = SMS_odkaz; halda_odkaz[objekt_odkaz + 3] = 1;
    }
    static int 화면문자읽기(int objekt_odkaz) {
        int účet_HODNOTA = halda_HODNOTA[objekt_odkaz + 2], položka_POČET = uživatelský_prostor.화면연결(8, účet_HODNOTA, 0, 0, 0, 0), 사용수 = 0;
        if (položka_POČET < 0) { selhání_HODNOTA("GUI text read failed"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < položka_POČET; Loop_INDEX++) { int 부호값 = uživatelský_prostor.화면연결(9, účet_HODNOTA, Loop_INDEX, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = přidělit_Storage(1, 사용수); if (!chyba) for (int Loop_INDEX = 0; Loop_INDEX < 사용수; Loop_INDEX++) halda_HODNOTA[반환값 + 2 + Loop_INDEX] = 화면글임시[Loop_INDEX]; return 반환값;
    }
    /* čeština 객체를 직접 만들고 jádro_HODNOTA 화면 기능에 연결한다. Swing objekt_HODNOTA/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int vlastník, int název_konstanta, int popisovač_konstanta, int příkaz_KÓD) {
        if (Word_SMS(vlastník, "čeština/vlastní/událost_fronta")) {
            if (příkaz_KÓD == 184 && Word_SMS(název_konstanta, "나중에실행") && Word_SMS(popisovač_konstanta, "(Lčeština/vlastní/실행할일;)V")) {
                int úkol_Akce = 빼기(2); if (!informační_systémy_platný_objekt(úkol_Akce)) return;
                if (나중수 == 8) { selhání_HODNOTA("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = úkol_Akce; return;
            }
            if (příkaz_KÓD == 184 && Word_SMS(název_konstanta, "사건처리중인가") && Word_SMS(popisovač_konstanta, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            selhání_HODNOTA("지원하지 않는 čeština 화면 일정 호출"); return;
        }
        if (Word_SMS(vlastník, "čeština/vlastní/Akce_povinnost_zvěřejnit")) {
            int povinnost_zvěřejnit = 빼기(2); if (!objekt_HODNOTA(povinnost_zvěřejnit, 29) || halda_HODNOTA[povinnost_zvěřejnit + 3] == 0) return;
            if (Word_SMS(název_konstanta, "zdroj_události") && Word_SMS(popisovač_konstanta, "()Lčeština/vlastní/화면구성요소;")) 넣기(halda_HODNOTA[povinnost_zvěřejnit + 2], 2);
            else if (Word_SMS(název_konstanta, "příkaz_SMS") && Word_SMS(popisovač_konstanta, "()Ljava/lang/String;")) 넣기(화면문자읽기(halda_HODNOTA[povinnost_zvěřejnit + 2]), 2);
            else if (Word_SMS(název_konstanta, "INDEX") && Word_SMS(popisovač_konstanta, "()I")) 넣기(1001, 1);
            else selhání_HODNOTA("지원하지 않는 čeština Akce povinnost_zvěřejnit 호출"); return;
        }
        if (příkaz_KÓD == 183 && Word_SMS(název_konstanta, "<init>")) {
            int Druh_HODNOTA = 한국어화면종(vlastník), 받이 = 0, 가로 = 0, Svislá_pozice = 0, 폭 = 0, výška_HODNOTA = 0;
            if (Druh_HODNOTA == 24 && Word_SMS(popisovač_konstanta, "(Ljava/lang/String;II)V")) {
                výška_HODNOTA = 빼기(1); 폭 = 빼기(1); 가로 = (uživatelský_prostor.화면너비() - 폭) / 2; Svislá_pozice = (uživatelský_prostor.화면높이() - výška_HODNOTA) / 2;
            } else if ((Druh_HODNOTA == 26 || Druh_HODNOTA == 28) && Word_SMS(popisovač_konstanta, "(Ljava/lang/String;IIII)V") || Druh_HODNOTA == 27 && Word_SMS(popisovač_konstanta, "(Ljava/lang/String;IIIILčeština/vlastní/동작받이;)V")) {
                if (Druh_HODNOTA == 27) 받이 = 빼기(2);
                výška_HODNOTA = 빼기(1); 폭 = 빼기(1); Svislá_pozice = 빼기(1); 가로 = 빼기(1);
            } else { selhání_HODNOTA("지원하지 않는 čeština 화면 생성자"); return; }
            int text = 빼기(2), prvek_HODNOTA = 빼기(2); if (!화면객체(prvek_HODNOTA)) return;
            if (폭 < 1 || výška_HODNOTA < 1 || 가로 < 0 || Svislá_pozice < 0 || 폭 > uživatelský_prostor.화면너비() - 가로 || výška_HODNOTA > uživatelský_prostor.화면높이() - Svislá_pozice) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int INDEX = uživatelský_prostor.화면연결(0, Druh_HODNOTA - 23, 0, 0, 0, 0);
            if (INDEX < 1 || INDEX > 32) { selhání_HODNOTA("화면 prvek_HODNOTA 자리가 가득 찼습니다"); return; }
            halda_HODNOTA[prvek_HODNOTA + 2] = INDEX; 화면참조[INDEX - 1] = prvek_HODNOTA;
            halda_HODNOTA[prvek_HODNOTA + 5] = 가로; halda_HODNOTA[prvek_HODNOTA + 6] = Svislá_pozice; halda_HODNOTA[prvek_HODNOTA + 7] = 폭; halda_HODNOTA[prvek_HODNOTA + 8] = výška_HODNOTA; halda_HODNOTA[prvek_HODNOTA + 10] = 2;
            halda_HODNOTA[prvek_HODNOTA + 4] = 받이; halda_odkaz[prvek_HODNOTA + 4] = 1; halda_HODNOTA[prvek_HODNOTA + 12] = 1;
            uživatelský_prostor.화면연결(1, INDEX, 가로, Svislá_pozice, 폭, výška_HODNOTA);
            if (Druh_HODNOTA == 24) uživatelský_prostor.화면연결(7, INDEX, 2, 0, 0, 0);
            화면문자설정(prvek_HODNOTA, text); return;
        }
        if (příkaz_KÓD != 182) { selhání_HODNOTA("잘못된 čeština 화면 호출 příkaz"); return; }
        if (Word_SMS(název_konstanta, "zápis_SMS") && Word_SMS(popisovač_konstanta, "(Ljava/lang/String;)V")) {
            int text = 빼기(2), prvek_HODNOTA = 빼기(2); if (화면객체(prvek_HODNOTA)) 화면문자설정(prvek_HODNOTA, text); return;
        }
        if (Word_SMS(název_konstanta, "글읽기") && Word_SMS(popisovač_konstanta, "()Ljava/lang/String;")) {
            int prvek_HODNOTA = 빼기(2); if (화면객체(prvek_HODNOTA)) 넣기(화면문자읽기(prvek_HODNOTA), 2); return;
        }
        if (Word_SMS(název_konstanta, "동작맡기기") && Word_SMS(popisovač_konstanta, "(Lčeština/vlastní/동작받이;)V")) {
            int 받이 = 빼기(2), prvek_HODNOTA = 빼기(2);
            if (화면객체(prvek_HODNOTA)) { halda_HODNOTA[prvek_HODNOTA + 4] = 받이; halda_odkaz[prvek_HODNOTA + 4] = 1; halda_HODNOTA[prvek_HODNOTA + 12] = 1; } return;
        }
        if (Word_SMS(název_konstanta, "Přidat_prvek") && Word_SMS(popisovač_konstanta, "(Lčeština/vlastní/화면구성요소;)V")) {
            int dítě_HODNOTA = 빼기(2), nadřazený_HODNOTA = 빼기(2); if (!화면객체(dítě_HODNOTA) || !화면객체(nadřazený_HODNOTA)) return;
            if (uživatelský_prostor.화면연결(2, halda_HODNOTA[nadřazený_HODNOTA + 2], halda_HODNOTA[dítě_HODNOTA + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            halda_HODNOTA[dítě_HODNOTA + 11] = nadřazený_HODNOTA; halda_odkaz[dítě_HODNOTA + 11] = 1; return;
        }
        if (Word_SMS(název_konstanta, "자리정하기") && Word_SMS(popisovač_konstanta, "(IIII)V")) {
            int výška_HODNOTA = 빼기(1), 폭 = 빼기(1), Svislá_pozice = 빼기(1), 가로 = 빼기(1), prvek_HODNOTA = 빼기(2); if (!화면객체(prvek_HODNOTA)) return;
            if (uživatelský_prostor.화면연결(1, halda_HODNOTA[prvek_HODNOTA + 2], 가로, Svislá_pozice, 폭, výška_HODNOTA) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            halda_HODNOTA[prvek_HODNOTA + 5] = 가로; halda_HODNOTA[prvek_HODNOTA + 6] = Svislá_pozice; halda_HODNOTA[prvek_HODNOTA + 7] = 폭; halda_HODNOTA[prvek_HODNOTA + 8] = výška_HODNOTA; return;
        }
        if ((Word_SMS(název_konstanta, "zobrazit_okno") || Word_SMS(název_konstanta, "Zavřené")) && Word_SMS(popisovač_konstanta, "()V")) {
            boolean Viditelnost_HODNOTA = Word_SMS(název_konstanta, "zobrazit_okno"); int prvek_HODNOTA = 빼기(2); if (!화면객체(prvek_HODNOTA)) return;
            if (uživatelský_prostor.화면연결(Viditelnost_HODNOTA ? 3 : 4, halda_HODNOTA[prvek_HODNOTA + 2], Viditelnost_HODNOTA ? 1 : 0, 0, 0, 0) < 0) { selhání_HODNOTA("화면은 interaktivní 명령에서 실행해야 합니다"); return; }
            halda_HODNOTA[prvek_HODNOTA + 9] = Viditelnost_HODNOTA ? 1 : 0; return;
        }
        if (Word_SMS(název_konstanta, "보이는가") && Word_SMS(popisovač_konstanta, "()Z")) { int prvek_HODNOTA = 빼기(2); if (화면객체(prvek_HODNOTA)) 넣기(halda_HODNOTA[prvek_HODNOTA + 9], 1); return; }
        selhání_HODNOTA("지원하지 않는 čeština 화면 metoda_HODNOTA");
    }
    static void 화면호출(int vlastník, int název_konstanta, int popisovač_konstanta, int příkaz_KÓD) {
        if (Word_SMS(vlastník, "javax/swing/SwingUtilities")) {
            if (příkaz_KÓD == 184 && Word_SMS(název_konstanta, "invokeLater") && Word_SMS(popisovač_konstanta, "(Ljava/lang/Runnable;)V")) { int objekt_odkaz = 빼기(2); if (!informační_systémy_platný_objekt(objekt_odkaz)) return; if (나중수 == 8) { selhání_HODNOTA("invokeLater queue full"); return; } 나중실행[나중수++] = objekt_odkaz; return; }
            if (příkaz_KÓD == 184 && Word_SMS(název_konstanta, "isEventDispatchThread") && Word_SMS(popisovač_konstanta, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            selhání_HODNOTA("unsupported SwingUtilities method"); return;
        }
        if (Word_SMS(vlastník, "java/awt/event/ActionEvent")) {
            int objekt_odkaz = 빼기(2); if (!objekt_HODNOTA(objekt_odkaz, 29)) return;
            if (Word_SMS(název_konstanta, "getSource") && Word_SMS(popisovač_konstanta, "()Ljava/lang/Object;")) 넣기(halda_HODNOTA[objekt_odkaz + 2], 2);
            else if (Word_SMS(název_konstanta, "getActionCommand") && Word_SMS(popisovač_konstanta, "()Ljava/lang/String;")) 넣기(화면문자읽기(halda_HODNOTA[objekt_odkaz + 2]), 2);
            else if (Word_SMS(název_konstanta, "getID") && Word_SMS(popisovač_konstanta, "()I")) 넣기(1001, 1);
            else selhání_HODNOTA("unsupported ActionEvent method"); return;
        }
        if (příkaz_KÓD == 183 && Word_SMS(název_konstanta, "<init>")) {
            int SLOUPCE = 0, SMS_odkaz = 0;
            if (Word_SMS(popisovač_konstanta, "(I)V")) SLOUPCE = 빼기(1);
            else if (Word_SMS(popisovač_konstanta, "(Ljava/lang/String;I)V")) { SLOUPCE = 빼기(1); SMS_odkaz = 빼기(2); }
            else if (Word_SMS(popisovač_konstanta, "(Ljava/lang/String;)V")) SMS_odkaz = 빼기(2);
            else if (Word_SMS(popisovač_konstanta, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Word_SMS(popisovač_konstanta, "()V")) { selhání_HODNOTA("unsupported Swing constructor"); return; }
            int objekt_odkaz = 빼기(2); if (!informační_systémy_platný_objekt(objekt_odkaz)) return;
            if (halda_HODNOTA[objekt_odkaz] == 30) { selhání_HODNOTA("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(objekt_odkaz) || SLOUPCE < 0) return;
            int účet_HODNOTA = uživatelský_prostor.화면연결(0, halda_HODNOTA[objekt_odkaz] - 23, 0, 0, 0, 0);
            if (účet_HODNOTA < 1 || účet_HODNOTA > 32) { selhání_HODNOTA("GUI widget slots exhausted"); return; }
            halda_HODNOTA[objekt_odkaz + 2] = účet_HODNOTA; 화면참조[účet_HODNOTA - 1] = objekt_odkaz; halda_HODNOTA[objekt_odkaz + 5] = halda_HODNOTA[objekt_odkaz] == 24 ? 130 : 16; halda_HODNOTA[objekt_odkaz + 6] = halda_HODNOTA[objekt_odkaz] == 24 ? 110 : 16;
            halda_HODNOTA[objekt_odkaz + 7] = halda_HODNOTA[objekt_odkaz] == 24 ? 380 : 220; halda_HODNOTA[objekt_odkaz + 8] = halda_HODNOTA[objekt_odkaz] == 24 ? 240 : 28; halda_HODNOTA[objekt_odkaz + 10] = 1;
            화면문자설정(objekt_odkaz, SMS_odkaz); return;
        }
        if (Word_SMS(název_konstanta, "setText") || Word_SMS(název_konstanta, "setTitle")) { int SMS_odkaz = 빼기(2), objekt_odkaz = 빼기(2); if (화면객체(objekt_odkaz) && Word_SMS(popisovač_konstanta, "(Ljava/lang/String;)V")) 화면문자설정(objekt_odkaz, SMS_odkaz); return; }
        if (Word_SMS(název_konstanta, "getText") || Word_SMS(název_konstanta, "getTitle")) { int objekt_odkaz = 빼기(2); if (화면객체(objekt_odkaz) && Word_SMS(popisovač_konstanta, "()Ljava/lang/String;")) 넣기(화면문자읽기(objekt_odkaz), 2); return; }
        if (Word_SMS(název_konstanta, "addActionListener") && Word_SMS(popisovač_konstanta, "(Ljava/awt/event/ActionListener;)V")) { int dostat_odkaz = 빼기(2), objekt_odkaz = 빼기(2); if (화면객체(objekt_odkaz)) { halda_HODNOTA[objekt_odkaz + 4] = dostat_odkaz; halda_odkaz[objekt_odkaz + 4] = 1; } return; }
        if (Word_SMS(název_konstanta, "getContentPane") && Word_SMS(popisovač_konstanta, "()Ljava/awt/Container;")) { int objekt_odkaz = 빼기(2); if (화면객체(objekt_odkaz)) 넣기(objekt_odkaz, 2); return; }
        if (Word_SMS(název_konstanta, "setLayout") && Word_SMS(popisovač_konstanta, "(Ljava/awt/LayoutManager;)V")) { int Navigace_odkaz = 빼기(2), objekt_odkaz = 빼기(2); if (화면객체(objekt_odkaz) && Navigace_odkaz != 0) selhání_HODNOTA("only absolute layout (null) is supported"); return; }
        if (Word_SMS(název_konstanta, "add") && (Word_SMS(popisovač_konstanta, "(Ljava/awt/Component;)Ljava/awt/Component;") || Word_SMS(popisovač_konstanta, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean Navigace_podmínka = Word_SMS(popisovač_konstanta, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (Navigace_podmínka) 빼기(2);
            int dítě_odkaz = 빼기(2), objekt_odkaz = 빼기(2); if (!화면객체(dítě_odkaz) || !화면객체(objekt_odkaz)) return;
            if (uživatelský_prostor.화면연결(2, halda_HODNOTA[objekt_odkaz + 2], halda_HODNOTA[dítě_odkaz + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            halda_HODNOTA[dítě_odkaz + 11] = objekt_odkaz; halda_odkaz[dítě_odkaz + 11] = 1; if (!Navigace_podmínka) 넣기(dítě_odkaz, 2); return;
        }
        if (Word_SMS(název_konstanta, "setBounds") && Word_SMS(popisovač_konstanta, "(IIII)V")) {
            int výška_HODNOTA = 빼기(1), 너비 = 빼기(1), Y_souřadnice = 빼기(1), souřadnice_x = 빼기(1), objekt_odkaz = 빼기(2); if (!화면객체(objekt_odkaz)) return;
            if (uživatelský_prostor.화면연결(1, halda_HODNOTA[objekt_odkaz + 2], souřadnice_x, Y_souřadnice, 너비, výška_HODNOTA) < 0) { 예외던짐(9, "GUI bounds"); return; }
            halda_HODNOTA[objekt_odkaz + 5] = souřadnice_x; halda_HODNOTA[objekt_odkaz + 6] = Y_souřadnice; halda_HODNOTA[objekt_odkaz + 7] = 너비; halda_HODNOTA[objekt_odkaz + 8] = výška_HODNOTA; return;
        }
        if (Word_SMS(název_konstanta, "setSize") && Word_SMS(popisovač_konstanta, "(II)V")) {
            int výška_HODNOTA = 빼기(1), 너비 = 빼기(1), objekt_odkaz = 빼기(2); if (!화면객체(objekt_odkaz)) return;
            if (uživatelský_prostor.화면연결(1, halda_HODNOTA[objekt_odkaz + 2], halda_HODNOTA[objekt_odkaz + 5], halda_HODNOTA[objekt_odkaz + 6], 너비, výška_HODNOTA) < 0) 예외던짐(9, "GUI size"); else { halda_HODNOTA[objekt_odkaz + 7] = 너비; halda_HODNOTA[objekt_odkaz + 8] = výška_HODNOTA; } return;
        }
        if (Word_SMS(název_konstanta, "setLocationRelativeTo") && Word_SMS(popisovač_konstanta, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), objekt_odkaz = 빼기(2); if (!화면객체(objekt_odkaz)) return; if (상대배치 != 0) { selhání_HODNOTA("only screen centering supported"); return; } halda_HODNOTA[objekt_odkaz + 5] = (uživatelský_prostor.화면너비() - halda_HODNOTA[objekt_odkaz + 7]) / 2; halda_HODNOTA[objekt_odkaz + 6] = (uživatelský_prostor.화면높이() - halda_HODNOTA[objekt_odkaz + 8]) / 2; uživatelský_prostor.화면연결(1, halda_HODNOTA[objekt_odkaz + 2], halda_HODNOTA[objekt_odkaz + 5], halda_HODNOTA[objekt_odkaz + 6], halda_HODNOTA[objekt_odkaz + 7], halda_HODNOTA[objekt_odkaz + 8]); return; }
        if (Word_SMS(název_konstanta, "setDefaultCloseOperation") && Word_SMS(popisovač_konstanta, "(I)V")) { int Policy = 빼기(1), objekt_odkaz = 빼기(2); if (화면객체(objekt_odkaz)) { if (Policy < 0 || Policy > 3) 예외던짐(9, "close policy"); else { halda_HODNOTA[objekt_odkaz + 10] = Policy; uživatelský_prostor.화면연결(7, halda_HODNOTA[objekt_odkaz + 2], Policy, 0, 0, 0); } } return; }
        if (Word_SMS(název_konstanta, "setVisible") && Word_SMS(popisovač_konstanta, "(Z)V")) { int data_HODNOTA = 빼기(1), objekt_odkaz = 빼기(2); if (화면객체(objekt_odkaz)) { int 처리값 = uživatelský_prostor.화면연결(3, halda_HODNOTA[objekt_odkaz + 2], data_HODNOTA, 0, 0, 0); if (처리값 < 0) selhání_HODNOTA("Swing requires a standalone interactive command"); else halda_HODNOTA[objekt_odkaz + 9] = data_HODNOTA; } return; }
        if (Word_SMS(název_konstanta, "dispose") && Word_SMS(popisovač_konstanta, "()V")) { int objekt_odkaz = 빼기(2); if (화면객체(objekt_odkaz)) { uživatelský_prostor.화면연결(4, halda_HODNOTA[objekt_odkaz + 2], 0, 0, 0, 0); halda_HODNOTA[objekt_odkaz + 9] = 0; } return; }
        if (Word_SMS(název_konstanta, "repaint") || Word_SMS(název_konstanta, "validate")) { int objekt_odkaz = 빼기(2); if (!화면객체(objekt_odkaz) || !Word_SMS(popisovač_konstanta, "()V")) return; uživatelský_prostor.화면연결(1, halda_HODNOTA[objekt_odkaz + 2], halda_HODNOTA[objekt_odkaz + 5], halda_HODNOTA[objekt_odkaz + 6], halda_HODNOTA[objekt_odkaz + 7], halda_HODNOTA[objekt_odkaz + 8]); return; }
        if (Word_SMS(název_konstanta, "isVisible") && Word_SMS(popisovač_konstanta, "()Z")) { int objekt_odkaz = 빼기(2); if (화면객체(objekt_odkaz)) 넣기(halda_HODNOTA[objekt_odkaz + 9], 1); return; }
        selhání_HODNOTA("unsupported Swing method (native subset)");
    }
    static void vypravit_událost(int cíl_ODKAZ, int událost_číslo, boolean čeština) {
        if (cíl_ODKAZ < 1 || halda_HODNOTA[cíl_ODKAZ] < 32) { selhání_HODNOTA("Java event listener required"); return; }
        int Soubor_INDEX = název_metoda(halda_HODNOTA[cíl_ODKAZ] - 32, událost_číslo == 0 ? (čeština ? "Spustit" : "run") : (čeština ? "dostat_Akce" : "actionPerformed"), událost_číslo == 0 ? "()V" : (čeština ? "(Lčeština/vlastní/Akce_povinnost_zvěřejnit;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (Soubor_INDEX < 0) { selhání_HODNOTA("event callback missing"); return; }
        dobrá_vlákno = 0; počet_vláken = 1; rámec_INDEX = 0; vlákno_Stav[0] = 1; rámec_Štos[0] = 0; rámec_zámek[0] = inicializovat_rámec[0] = 0; žádost_o_změnu = false;
        for (int Loop_INDEX = 0; Loop_INDEX < 128; Loop_INDEX++) { místní_HODNOTA[Loop_INDEX] = místní_TYP[Loop_INDEX] = 0; }
        rámec_metoda[0] = Soubor_INDEX; rámec_pozice[0] = metoda_START[Soubor_INDEX]; místní_HODNOTA[0] = cíl_ODKAZ; místní_TYP[0] = 2;
        if (událost_číslo != 0) { místní_HODNOTA[1] = událost_číslo; místní_TYP[1] = 2; }
        사건중 = true; Provést_příkaz(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!chyba) {
            if (나중수 > 0) { int cíl_ODKAZ = 나중실행[0], čeština = 나중한국어[0]; for (int Loop_INDEX = 1; Loop_INDEX < 나중수; Loop_INDEX++) { 나중실행[Loop_INDEX - 1] = 나중실행[Loop_INDEX]; 나중한국어[Loop_INDEX - 1] = 나중한국어[Loop_INDEX]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; vypravit_událost(cíl_ODKAZ, 0, čeština != 0); continue; }
            if (uživatelský_prostor.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int událost_číslo = uživatelský_prostor.화면연결(5, 0, 0, 0, 0, 0); if (událost_číslo == 0) continue;
            if (událost_číslo < 0) { selhání_HODNOTA("GUI event I/O failed"); return; }
            int účet_HODNOTA = událost_číslo & 65535; if (účet_HODNOTA < 1 || účet_HODNOTA > 32) continue; int objekt_odkaz = 화면참조[účet_HODNOTA - 1]; if (objekt_odkaz == 0) continue;
            if ((událost_číslo & 65536) != 0) {
                if (halda_HODNOTA[objekt_odkaz + 10] != 0) halda_HODNOTA[objekt_odkaz + 9] = 0;
                if (halda_HODNOTA[objekt_odkaz + 10] == 3) for (int Loop_INDEX = 0; Loop_INDEX < 32; Loop_INDEX++) if (화면참조[Loop_INDEX] != 0 && halda_HODNOTA[화면참조[Loop_INDEX]] == 24) uživatelský_prostor.화면연결(4, Loop_INDEX + 1, 0, 0, 0, 0);
            } else if (halda_HODNOTA[objekt_odkaz + 4] != 0) {
                int 안내참조 = přidělit_Storage(29, 2); if (chyba) return; halda_HODNOTA[안내참조 + 2] = objekt_odkaz; halda_HODNOTA[안내참조 + 3] = halda_HODNOTA[objekt_odkaz + 12]; halda_odkaz[안내참조 + 2] = 1; vypravit_událost(halda_HODNOTA[objekt_odkaz + 4], 안내참조, halda_HODNOTA[objekt_odkaz + 12] != 0);
            }
        }
    }
    public static int Spustit_2() {
        if (uživatelský_prostor.인수개수() == 1 && 자바도구.같음(uživatelský_prostor.argumenty(0), "-version")) {
            uživatelský_prostor.Zápis("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (uživatelský_prostor.인수개수() < 1) { uživatelský_prostor.Zápis("Usage: java CLASS [ARGS]\n"); return 2; }
        položka_Třída_Definice = dávka_Třída_Definice(hostit_znak(uživatelský_prostor.argumenty(0))); if (chyba || položka_Třída_Definice < 0) return 1;
        int vstupní_bod_HODNOTA = název_metoda(položka_Třída_Definice, "Spustit_2", "()V");
        boolean 한국어진입 = vstupní_bod_HODNOTA >= 0 && (metoda_přístup[vstupní_bod_HODNOTA] & 9) == 9;
        if (!한국어진입) vstupní_bod_HODNOTA = název_metoda(položka_Třída_Definice, "main", "([Ljava/lang/String;)V");
        if (vstupní_bod_HODNOTA < 0 || (metoda_přístup[vstupní_bod_HODNOTA] & 9) != 9) selhání_HODNOTA("public static void Spustit_2() or main(String[] args) required");
        if (chyba) return 1;
        int argumenty = přidělit_Storage(3, uživatelský_prostor.인수개수() - 1); prvek_pole[argumenty] = -1;
        for (int číslo = 1; číslo < uživatelský_prostor.인수개수() && !chyba; číslo++) halda_HODNOTA[argumenty + 1 + číslo] = hostit_znak(uživatelský_prostor.argumenty(číslo));
        rámec_INDEX = 0; rámec_metoda[0] = vstupní_bod_HODNOTA; rámec_pozice[0] = metoda_START[vstupní_bod_HODNOTA]; místní_HODNOTA[0] = 한국어진입 ? 0 : argumenty; místní_TYP[0] = 한국어진입 ? 0 : 2;
        vlákno_Stav[0] = 1; vlákno_objekt[0] = přidělit_Storage(13, 2);
        Provést_příkaz(); if (!chyba) 화면사건들(); return chyba ? 1 : 0;
    }
}
