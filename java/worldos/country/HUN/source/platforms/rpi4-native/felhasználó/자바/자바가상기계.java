// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. Fájl/operandus_Sor/hivatkozik/ág 경계를 végrehajt_parancs 중 검사한다. */
public final class 자바가상기계 {
    static int[] Fájl = new int[16 * 16384], ideiglenes_fájl = new int[16384], fájlnév_SMS = new int[512];
    static int[] állandó_címke = new int[8192], 상가 = new int[8192], állandó_MPERC_ÉRTÉK = new int[8192], sztring_hivatkozik = new int[8192];
    static int[] metódus_név_SMS = new int[512], metódus_beír = new int[512], metódus_hozzáfér = new int[512], metódus_tulajdonos = new int[512];
    static int[] metódus_START = new int[512], metódus_megszüntet = new int[512], metódus_Sor = new int[512], 함수지역 = new int[512];
    static int[] metódus_argumentum_DARAB = new int[512], metódus_argumentum_beír = new int[8192], metódus_visszaküld = new int[512];
    static int[] határ_ÉRTÉK = new int[16 * 16384];
    static int[] helyi_ÉRTÉK = new int[16384], helyi_beír = new int[16384], operandus_Sor_ÉRTÉK = new int[16384], operandus_Sor_beír = new int[16384];
    static int[] doboz_metódus = new int[128], doboz_pozíció = new int[128], doboz_Sor = new int[128], 틀명령 = new int[128], inicializál_doboz = new int[128];
    static int[] tanóra_Definíció_név = new int[16], tanóra_Definíció_méretez = new int[16], tanóra_Definíció_szülő = new int[16], tanóra_Definíció_Állapot = new int[16], tanóra_tárolóhely_DARAB = new int[16], inicializál_tanóra_Definíció = new int[16];
    static int[] tanóra_csatoló = new int[16 * 16], tanóra_csatoló_DARAB = new int[16];
    static int[] tárolóhely_név = new int[512], tárolóhely_beír = new int[512], tárolóhely_tulajdonos = new int[512], tárolóhely_Engedélyek = new int[512], tárolóhely_pozíció = new int[512], tárolóhely_adat = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] halommemória_ÉRTÉK = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], halommemória_hivatkozik = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], tömbelem = new int[32768], tár_egész_szám = new int[256];
    static int Méret, 읽기위치, metódus_DARAB, osztálynév, doboz_INDEX = -1, halommemória_megszüntet_pozíció = 1, visszaküld_beír;
    static int tanóra_Definíció_DARAB, tárolóhely_DARAB, 잡기수, 현재읽는종, 던진객체, 잠시수, kijelző_DARAB, sokaság_DARAB;
    static int aktuális_szál, szálak_száma = 1, bejegyzés_tanóra_Definíció;
    static int[] szál_doboz = new int[4], szál_Állapot = new int[4], szál_objektum = new int[4], szál_cél = new int[4], 가닥대기 = new int[4];
    static boolean HIBA, változáskérés;
    static int[] lezár_tulajdonos = new int[32768], 잠금깊이 = new int[32768], doboz_lezár = new int[128], tanóra_lezár = new int[16], tanóra_szál = new int[16];

    static void hiba_ÉRTÉK(String szó_SMS) {
        if (HIBA) return;
        int terület_KÓD = 0;
        if (자바도구.같음(szó_SMS, "ArithmeticException: / by zero")) terület_KÓD = 4;
        if (자바도구.같음(szó_SMS, "NullPointerException") || 자바도구.같음(szó_SMS, "null or invalid array")) terület_KÓD = 5;
        if (자바도구.같음(szó_SMS, "ArrayIndexOutOfBoundsException")) terület_KÓD = 7;
        if (자바도구.같음(szó_SMS, "StringIndexOutOfBoundsException")) terület_KÓD = 8;
        if (자바도구.같음(szó_SMS, "NumberFormatException")) terület_KÓD = 10;
        if (자바도구.같음(szó_SMS, "FileNotFoundException: file open failed")) terület_KÓD = 12;
        if (자바도구.같음(szó_SMS, "IOException: stream closed") || 자바도구.같음(szó_SMS, "IOException: read failed") || 자바도구.같음(szó_SMS, "IOException: write failed")) terület_KÓD = 11;
        if (자바도구.같음(szó_SMS, "ClassCastException")) terület_KÓD = 14;
        if (자바도구.같음(szó_SMS, "NegativeArraySizeException")) terület_KÓD = 15;
        if (terület_KÓD != 0 && doboz_INDEX >= 0) { 예외던짐(terület_KÓD, szó_SMS); return; }
        felhasználó.Írás("JVM error: "); felhasználó.Írás(szó_SMS); felhasználó.ír_karakter_ÉRTÉK(10); HIBA = true;
    }
    static boolean klip(int Futtatás, int hossz_ÉRTÉK) {
        if (Futtatás < 0 || Futtatás >= Fájl.length || hossz_ÉRTÉK < 0) return false;
        int tanóra_Definíció = Futtatás / 16384;
        return Futtatás % 16384 <= tanóra_Definíció_méretez[tanóra_Definíció] && hossz_ÉRTÉK <= tanóra_Definíció_méretez[tanóra_Definíció] - Futtatás % 16384;
    }
    static int bájt_ÉRTÉK() {
        if (!klip(읽기위치, 1)) { hiba_ÉRTÉK("truncated class file"); return 0; }
        return Fájl[읽기위치++];
    }
    static int 짧은수() { return bájt_ÉRTÉK() << 8 | bájt_ÉRTÉK(); }
    static int egész_szám() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int hossz_ÉRTÉK) { if (!klip(읽기위치, hossz_ÉRTÉK)) hiba_ÉRTÉK("invalid attribute size"); else 읽기위치 += hossz_ÉRTÉK; }
    static boolean csekk_állandó(int szám, int Altípus_ÉRTÉK) {
        if (szám <= 0 || szám >= állandó_címke.length || állandó_címke[szám] != Altípus_ÉRTÉK) { hiba_ÉRTÉK("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean SMS_tartomány(int Futtatás, int hossz_ÉRTÉK, String szó_SMS) {
        if (!klip(Futtatás, hossz_ÉRTÉK)) return false;
        int 읽는자리 = Futtatás, 끝 = Futtatás + hossz_ÉRTÉK;
        for (int Loop_INDEX = 0; Loop_INDEX < szó_SMS.length(); Loop_INDEX++) {
            int kódpont = szó_SMS.charAt(Loop_INDEX);
            if (kódpont > 0 && kódpont < 128) { if (읽는자리 >= 끝 || Fájl[읽는자리++] != kódpont) return false; }
            else if (kódpont < 2048) {
                if (읽는자리 + 2 > 끝 || Fájl[읽는자리++] != (192 | (kódpont >> 6)) || Fájl[읽는자리++] != (128 | (kódpont & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || Fájl[읽는자리++] != (224 | (kódpont >> 12)) || Fájl[읽는자리++] != (128 | ((kódpont >> 6) & 63)) || Fájl[읽는자리++] != (128 | (kódpont & 63))) return false;
        }
        return 읽는자리 == 끝;
    }
    static boolean szó_SMS(int állandó_ÉRTÉK, String szó_SMS) { return csekk_állandó(állandó_ÉRTÉK, 1) && SMS_tartomány(상가[állandó_ÉRTÉK], állandó_MPERC_ÉRTÉK[állandó_ÉRTÉK], szó_SMS); }
    static boolean 같은말(int 가, int MPERC_operandus) {
        if (!csekk_állandó(가, 1) || !csekk_állandó(MPERC_operandus, 1) || állandó_MPERC_ÉRTÉK[가] != állandó_MPERC_ÉRTÉK[MPERC_operandus]) return false;
        for (int szám = 0; szám < állandó_MPERC_ÉRTÉK[가]; szám++) if (Fájl[상가[가] + szám] != Fájl[상가[MPERC_operandus] + szám]) return false;
        return true;
    }
    static int osztálynév_SMS(int szám) { return csekk_állandó(szám, 7) && csekk_állandó(상가[szám], 1) ? 상가[szám] : 0; }
    static int hivatkozik_név(int szám) { return csekk_állandó(szám, 12) && csekk_állandó(상가[szám], 1) ? 상가[szám] : 0; }
    static int referenciális_típus(int szám) { return csekk_állandó(szám, 12) && csekk_állandó(állandó_MPERC_ÉRTÉK[szám], 1) ? állandó_MPERC_ÉRTÉK[szám] : 0; }
    static int 서술형(int 끝, boolean üres_beír) {
        if (읽기위치 >= 끝) { hiba_ÉRTÉK("invalid descriptor"); return 0; }
        int ÉRTÉK = bájt_ÉRTÉK();
        if (ÉRTÉK == 'V' && üres_beír) return 0;
        if (ÉRTÉK == 'I' || ÉRTÉK == 'B' || ÉRTÉK == 'C' || ÉRTÉK == 'S' || ÉRTÉK == 'Z') return 1;
        if (ÉRTÉK == '[') { 서술형(끝, false); return 2; }
        if (ÉRTÉK == 'L') {
            int Futtatás = 읽기위치;
            while (읽기위치 < 끝 && Fájl[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == Futtatás) hiba_ÉRTÉK("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        hiba_ÉRTÉK("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int FÜGGVÉNY_ÉRTÉK) {
        int Előző_cikk = 읽기위치, szám = metódus_beír[FÜGGVÉNY_ÉRTÉK];
        if (!csekk_állandó(szám, 1)) return;
        읽기위치 = 상가[szám]; int 끝 = 읽기위치 + állandó_MPERC_ÉRTÉK[szám];
        if (bájt_ÉRTÉK() != '(') hiba_ÉRTÉK("invalid method descriptor");
        int cikk_DARAB = 0;
        while (!HIBA && 읽기위치 < 끝 && Fájl[읽기위치] != ')') {
            if (cikk_DARAB == 16) { hiba_ÉRTÉK("too many method arguments"); break; }
            metódus_argumentum_beír[FÜGGVÉNY_ÉRTÉK * 16 + cikk_DARAB++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || bájt_ÉRTÉK() != ')') hiba_ÉRTÉK("invalid method descriptor");
        metódus_visszaküld[FÜGGVÉNY_ÉRTÉK] = 서술형(끝, true); metódus_argumentum_DARAB[FÜGGVÉNY_ÉRTÉK] = cikk_DARAB;
        if (읽기위치 != 끝) hiba_ÉRTÉK("invalid method descriptor");
        읽기위치 = Előző_cikk;
    }
    static int 상번호() { int ÉRTÉK = 짧은수(); return ÉRTÉK == 0 ? 0 : 현재읽는종 * 512 + ÉRTÉK; }
    static int 명상수() { return metódus_tulajdonos[doboz_metódus[doboz_INDEX]] * 512 + 명짧(); }
    static void kihagy_attribútum() {
        int cikk_DARAB = 짧은수();
        for (int szám = 0; szám < cikk_DARAB && !HIBA; szám++) { csekk_állandó(상번호(), 1); 건너(egész_szám()); }
    }
    static int parancs_hossz(int ÉRTÉK) {
        if (ÉRTÉK == 16 || ÉRTÉK == 18 || ÉRTÉK == 21 || ÉRTÉK == 25 || ÉRTÉK == 54 || ÉRTÉK == 58 || ÉRTÉK == 188) return 2;
        if (ÉRTÉK == 17 || ÉRTÉK == 19 || ÉRTÉK == 132 || ÉRTÉK >= 153 && ÉRTÉK <= 167
            || ÉRTÉK >= 178 && ÉRTÉK <= 184 || ÉRTÉK == 187 || ÉRTÉK == 189 || ÉRTÉK == 192 || ÉRTÉK == 193 || ÉRTÉK == 198 || ÉRTÉK == 199) return 3;
        if (ÉRTÉK == 185 || ÉRTÉK == 200) return 5;
        if (ÉRTÉK >= 0 && ÉRTÉK <= 8 || ÉRTÉK >= 26 && ÉRTÉK <= 29 || ÉRTÉK >= 42 && ÉRTÉK <= 46 || ÉRTÉK >= 50 && ÉRTÉK <= 53
            || ÉRTÉK >= 59 && ÉRTÉK <= 62 || ÉRTÉK >= 75 && ÉRTÉK <= 79 || ÉRTÉK >= 83 && ÉRTÉK <= 95
            || ÉRTÉK == 96 || ÉRTÉK == 100 || ÉRTÉK == 104 || ÉRTÉK == 108 || ÉRTÉK == 112 || ÉRTÉK == 116
            || ÉRTÉK == 120 || ÉRTÉK == 122 || ÉRTÉK == 124 || ÉRTÉK == 126 || ÉRTÉK == 128 || ÉRTÉK == 130
            || ÉRTÉK >= 145 && ÉRTÉK <= 147 || ÉRTÉK == 172 || ÉRTÉK == 176 || ÉRTÉK == 177 || ÉRTÉK == 190 || ÉRTÉK == 191
            || ÉRTÉK == 194 || ÉRTÉK == 195) return 1;
        return 0;
    }
    static int pozíció_egész_szám(int 읽는자리) {
        if (!klip(읽는자리, 4)) { hiba_ÉRTÉK("truncated bytecode operand"); return 0; }
        return Fájl[읽는자리] << 24 | Fájl[읽는자리 + 1] << 16 | Fájl[읽는자리 + 2] << 8 | Fájl[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int Futtatás, int 끝) {
        int ÉRTÉK = Fájl[읽는자리], hossz_ÉRTÉK = parancs_hossz(ÉRTÉK);
        if (ÉRTÉK == 170 || ÉRTÉK == 171) {
            int ALAP_pozíció = 읽는자리 + 1;
            while ((ALAP_pozíció - Futtatás) % 4 != 0) ALAP_pozíció++;
            if (끝 - ALAP_pozíció < (ÉRTÉK == 170 ? 12 : 8)) return 0;
            int bejegyzés_DARAB = ÉRTÉK == 170 ? pozíció_egész_szám(ALAP_pozíció + 8) - pozíció_egész_szám(ALAP_pozíció + 4) + 1 : pozíció_egész_szám(ALAP_pozíció + 4);
            if (bejegyzés_DARAB < 0 || bejegyzés_DARAB > 2048) return 0;
            hossz_ÉRTÉK = ALAP_pozíció - 읽는자리 + (ÉRTÉK == 170 ? 12 + 4 * bejegyzés_DARAB : 8 + 8 * bejegyzés_DARAB);
        }
        if (ÉRTÉK == 196 && 읽는자리 + 1 < 끝) {
            int szó_adat = Fájl[읽는자리 + 1]; hossz_ÉRTÉK = szó_adat == 132 ? 6 : (szó_adat == 21 || szó_adat == 25 || szó_adat == 54 || szó_adat == 58) ? 4 : 0;
        }
        return hossz_ÉRTÉK > 0 && hossz_ÉRTÉK <= 끝 - 읽는자리 ? hossz_ÉRTÉK : 0;
    }
    static void csekk_cél_ÉRTÉK(int cél_ÉRTÉK, int FÜGGVÉNY_ÉRTÉK) {
        if (cél_ÉRTÉK < metódus_START[FÜGGVÉNY_ÉRTÉK] || cél_ÉRTÉK >= metódus_megszüntet[FÜGGVÉNY_ÉRTÉK] || határ_ÉRTÉK[cél_ÉRTÉK] != FÜGGVÉNY_ÉRTÉK + 1) hiba_ÉRTÉK("invalid branch target");
    }
    static void 클래스읽기(int tanóra_Definíció) {
        현재읽는종 = tanóra_Definíció; 읽기위치 = tanóra_Definíció * 16384; Méret = 읽기위치 + tanóra_Definíció_méretez[tanóra_Definíció];
        if (egész_szám() != 0xcafebabe) { hiba_ÉRTÉK("not a class file"); return; }
        int 부판 = 짧은수(), verzió_ÉRTÉK = 짧은수();
        if (verzió_ÉRTÉK < 45 || verzió_ÉRTÉK > 52 || 부판 != 0) { hiba_ÉRTÉK("supported class versions: 45..52, minor 0"); return; }
        int állandó_DARAB = 짧은수(), ALAP_pozíció = tanóra_Definíció * 512;
        if (állandó_DARAB < 1 || állandó_DARAB > 512) { hiba_ÉRTÉK("constant pool limit (511)"); return; }
        for (int bejegyzés_DARAB = 1; bejegyzés_DARAB < állandó_DARAB && !HIBA; bejegyzés_DARAB++) {
            int szám = ALAP_pozíció + bejegyzés_DARAB, Altípus_ÉRTÉK = bájt_ÉRTÉK(); állandó_címke[szám] = Altípus_ÉRTÉK;
            if (Altípus_ÉRTÉK == 1) { állandó_MPERC_ÉRTÉK[szám] = 짧은수(); 상가[szám] = 읽기위치; 건너(állandó_MPERC_ÉRTÉK[szám]); }
            else if (Altípus_ÉRTÉK == 3) 상가[szám] = egész_szám();
            else if (Altípus_ÉRTÉK == 7 || Altípus_ÉRTÉK == 8) 상가[szám] = 상번호();
            else if (Altípus_ÉRTÉK == 9 || Altípus_ÉRTÉK == 10 || Altípus_ÉRTÉK == 11 || Altípus_ÉRTÉK == 12) { 상가[szám] = 상번호(); állandó_MPERC_ÉRTÉK[szám] = 상번호(); }
            else hiba_ÉRTÉK("unsupported constant type");
        }
        int engedély_ÉRTÉK = 짧은수();
        if ((engedély_ÉRTÉK & (0x2000 | 0x4000)) != 0) hiba_ÉRTÉK("annotation/enum class unsupported");
        tanóra_Definíció_név[tanóra_Definíció] = osztálynév_SMS(상번호());
        tanóra_Definíció_szülő[tanóra_Definíció] = osztálynév_SMS(상번호());
        int csatoló_DARAB = 짧은수(); if (csatoló_DARAB > 16) { hiba_ÉRTÉK("interface count limit"); return; }
        tanóra_csatoló_DARAB[tanóra_Definíció] = csatoló_DARAB;
        for (int Loop_INDEX = 0; Loop_INDEX < csatoló_DARAB; Loop_INDEX++) tanóra_csatoló[tanóra_Definíció * 16 + Loop_INDEX] = osztálynév_SMS(상번호());
        int mező_DARAB = 짧은수();
        if (mező_DARAB > 512 - tárolóhely_DARAB) { hiba_ÉRTÉK("field count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < mező_DARAB && !HIBA; Loop_INDEX++) {
            int Fájl_INDEX = tárolóhely_DARAB++; tárolóhely_tulajdonos[Fájl_INDEX] = tanóra_Definíció; tárolóhely_Engedélyek[Fájl_INDEX] = 짧은수(); tárolóhely_név[Fájl_INDEX] = 상번호(); tárolóhely_beír[Fájl_INDEX] = 상번호();
            csekk_állandó(tárolóhely_név[Fájl_INDEX], 1); csekk_állandó(tárolóhely_beír[Fájl_INDEX], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[tárolóhely_beír[Fájl_INDEX]]; int terület_KÓD = 서술형(읽기위치 + állandó_MPERC_ÉRTÉK[tárolóhely_beír[Fájl_INDEX]], false); 읽기위치 = 보존값;
            if ((tárolóhely_Engedélyek[Fájl_INDEX] & 8) == 0) tárolóhely_pozíció[Fájl_INDEX] = tanóra_tárolóhely_DARAB[tanóra_Definíció]++;
            int attribútum_adat = 짧은수();
            for (int belső_pozíció = 0; belső_pozíció < attribútum_adat && !HIBA; belső_pozíció++) {
                int név_állandó = 상번호(), érvényes_hossz = egész_szám();
                if (szó_SMS(név_állandó, "ConstantValue") && érvényes_hossz == 2) {
                    int adat_ÉRTÉK = 상번호();
                    if (terület_KÓD == 1 && csekk_állandó(adat_ÉRTÉK, 3)) tárolóhely_adat[Fájl_INDEX] = 상가[adat_ÉRTÉK];
                    else if (terület_KÓD == 2 && csekk_állandó(adat_ÉRTÉK, 8)) tárolóhely_adat[Fájl_INDEX] = állandó_SMS(상가[adat_ÉRTÉK]);
                } else 건너(érvényes_hossz);
            }
        }
        int cikk_DARAB = 짧은수();
        if (cikk_DARAB > 512 - metódus_DARAB) { hiba_ÉRTÉK("method count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < cikk_DARAB && !HIBA; Loop_INDEX++) {
            int szám = metódus_DARAB++; metódus_tulajdonos[szám] = tanóra_Definíció;
            metódus_hozzáfér[szám] = 짧은수(); metódus_név_SMS[szám] = 상번호(); metódus_beír[szám] = 상번호();
            csekk_állandó(metódus_név_SMS[szám], 1); 서술읽기(szám);
            if ((metódus_hozzáfér[szám] & 8) == 0) {
                if (metódus_argumentum_DARAB[szám] == 16) { hiba_ÉRTÉK("too many instance method arguments"); return; }
                for (int Összehasonlítás_pozíció = metódus_argumentum_DARAB[szám]; Összehasonlítás_pozíció > 0; Összehasonlítás_pozíció--) metódus_argumentum_beír[szám * 16 + Összehasonlítás_pozíció] = metódus_argumentum_beír[szám * 16 + Összehasonlítás_pozíció - 1];
                metódus_argumentum_beír[szám * 16] = 2; metódus_argumentum_DARAB[szám]++;
            }
            if ((metódus_hozzáfér[szám] & 0x100) != 0) hiba_ÉRTÉK("user native method unsupported");
            if (szó_SMS(metódus_név_SMS[szám], "<clinit>")) inicializál_tanóra_Definíció[tanóra_Definíció] = szám + 1;
            for (int elülső_kamera_ÉRTÉK = 0; elülső_kamera_ÉRTÉK < szám; elülső_kamera_ÉRTÉK++) if (metódus_tulajdonos[elülső_kamera_ÉRTÉK] == tanóra_Definíció && 같은말(metódus_név_SMS[elülső_kamera_ÉRTÉK], metódus_név_SMS[szám]) && 같은말(metódus_beír[elülső_kamera_ÉRTÉK], metódus_beír[szám])) hiba_ÉRTÉK("duplicate method");
            int attribútum_DARAB = 짧은수();
            for (int attribútum_ÉRTÉK = 0; attribútum_ÉRTÉK < attribútum_DARAB && !HIBA; attribútum_ÉRTÉK++) {
                int Név = 상번호(), hossz_ÉRTÉK = egész_szám(), Futtatás = 읽기위치;
                if (!klip(Futtatás, hossz_ÉRTÉK)) { hiba_ÉRTÉK("truncated method attribute"); break; }
                if (szó_SMS(Név, "Code")) {
                    if (metódus_START[szám] != 0) hiba_ÉRTÉK("duplicate Code attribute");
                    metódus_Sor[szám] = 짧은수(); 함수지역[szám] = 짧은수(); int KÓD_hossz = egész_szám();
                    if (metódus_Sor[szám] > 128 || 함수지역[szám] > 128 || 함수지역[szám] < metódus_argumentum_DARAB[szám]
                        || KÓD_hossz < 1 || KÓD_hossz > 8192) hiba_ÉRTÉK("method memory limits exceeded");
                    metódus_START[szám] = 읽기위치; 건너(KÓD_hossz); metódus_megszüntet[szám] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { hiba_ÉRTÉK("exception table limit"); return; }
                    for (int belső_pozíció = 0; belső_pozíció < 잡는수; belső_pozíció++) {
                        int hiba_hivatkozik = 잡기수++; 잡기함수[hiba_hivatkozik] = szám;
                        잡기시작[hiba_hivatkozik] = metódus_START[szám] + 짧은수(); 잡기끝[hiba_hivatkozik] = metódus_START[szám] + 짧은수();
                        잡기위치[hiba_hivatkozik] = metódus_START[szám] + 짧은수(); int 부호값 = 상번호(); 잡기종[hiba_hivatkozik] = 부호값 == 0 ? 0 : osztálynév_SMS(부호값);
                    }
                    kihagy_attribútum();
                    if (읽기위치 != Futtatás + hossz_ÉRTÉK) hiba_ÉRTÉK("Code attribute size mismatch");
                } else 건너(hossz_ÉRTÉK);
            }
            if ((metódus_hozzáfér[szám] & 0x400) != 0) continue;
            if (metódus_START[szám] == 0) hiba_ÉRTÉK("missing Code attribute");
            int tárolóhely_bejegyzés = metódus_START[szám];
            while (tárolóhely_bejegyzés < metódus_megszüntet[szám] && !HIBA) {
                int hossz_ÉRTÉK = 길이읽기(tárolóhely_bejegyzés, metódus_START[szám], metódus_megszüntet[szám]);
                if (hossz_ÉRTÉK == 0) { hiba_ÉRTÉK("unsupported or truncated bytecode"); break; }
                határ_ÉRTÉK[tárolóhely_bejegyzés] = szám + 1; tárolóhely_bejegyzés += hossz_ÉRTÉK;
            }
            tárolóhely_bejegyzés = metódus_START[szám];
            while (tárolóhely_bejegyzés < metódus_megszüntet[szám] && !HIBA) {
                int ÉRTÉK = Fájl[tárolóhely_bejegyzés];
                if (ÉRTÉK >= 153 && ÉRTÉK <= 167 || ÉRTÉK == 198 || ÉRTÉK == 199) csekk_cél_ÉRTÉK(tárolóhely_bejegyzés + (short)(Fájl[tárolóhely_bejegyzés + 1] << 8 | Fájl[tárolóhely_bejegyzés + 2]), szám);
                if (ÉRTÉK == 200) csekk_cél_ÉRTÉK(tárolóhely_bejegyzés + pozíció_egész_szám(tárolóhely_bejegyzés + 1), szám);
                if (ÉRTÉK == 170 || ÉRTÉK == 171) {
                    int 읽는자리 = tárolóhely_bejegyzés + 1; while ((읽는자리 - metódus_START[szám]) % 4 != 0) 읽는자리++;
                    csekk_cél_ÉRTÉK(tárolóhely_bejegyzés + pozíció_egész_szám(읽는자리), szám);
                    int bejegyzés_DARAB = ÉRTÉK == 170 ? pozíció_egész_szám(읽는자리 + 8) - pozíció_egész_szám(읽는자리 + 4) + 1 : pozíció_egész_szám(읽는자리 + 4);
                    읽는자리 += ÉRTÉK == 170 ? 12 : 8;
                    for (int belső_pozíció = 0; belső_pozíció < bejegyzés_DARAB; belső_pozíció++) csekk_cél_ÉRTÉK(tárolóhely_bejegyzés + pozíció_egész_szám(읽는자리 + belső_pozíció * (ÉRTÉK == 170 ? 4 : 8) + (ÉRTÉK == 170 ? 0 : 4)), szám);
                }
                tárolóhely_bejegyzés += 길이읽기(tárolóhely_bejegyzés, metódus_START[szám], metódus_megszüntet[szám]);
            }
            for (int belső_pozíció = 0; belső_pozíció < 잡기수; belső_pozíció++) if (잡기함수[belső_pozíció] == szám) {
                csekk_cél_ÉRTÉK(잡기시작[belső_pozíció], szám); csekk_cél_ÉRTÉK(잡기위치[belső_pozíció], szám);
                if (잡기끝[belső_pozíció] != metódus_megszüntet[szám]) csekk_cél_ÉRTÉK(잡기끝[belső_pozíció], szám);
                if (잡기시작[belső_pozíció] >= 잡기끝[belső_pozíció]) hiba_ÉRTÉK("invalid exception range");
            }
        }
        if (!HIBA) kihagy_attribútum();
        if (읽기위치 != Méret) hiba_ÉRTÉK("extra class file data");
    }
    static int kioszt_tár(int Altípus_ÉRTÉK, int hossz_ÉRTÉK) { return 새기억(Altípus_ÉRTÉK, hossz_ÉRTÉK); }
    static boolean objektum_ÉRTÉK(int hivatkozik, int Altípus_ÉRTÉK) {
        if (!informatikai_részleg_érvényes_objektum(hivatkozik)) return false;
        if (halommemória_ÉRTÉK[hivatkozik] != Altípus_ÉRTÉK) { hiba_ÉRTÉK("object type mismatch"); return false; }
        return true;
    }
    static int állandó_SMS(int INDEX) {
        if (!csekk_állandó(INDEX, 1)) return 0;
        if (sztring_hivatkozik[INDEX] != 0) return sztring_hivatkozik[INDEX];
        int hivatkozik = kioszt_tár(1, állandó_MPERC_ÉRTÉK[INDEX]); if (HIBA) return 0;
        int 끝 = 상가[INDEX] + állandó_MPERC_ÉRTÉK[INDEX], szám = 상가[INDEX], hossz_ÉRTÉK = 0;
        while (szám < 끝 && !HIBA) {
            int ÉRTÉK = Fájl[szám++];
            if (ÉRTÉK == 0) hiba_ÉRTÉK("invalid modified UTF-8");
            else if (ÉRTÉK >= 192 && ÉRTÉK <= 223 && szám < 끝) {
                int Tovább_cikk = Fájl[szám++];
                if ((Tovább_cikk & 192) != 128) hiba_ÉRTÉK("invalid modified UTF-8");
                ÉRTÉK = (ÉRTÉK & 31) << 6 | Tovább_cikk & 63;
                if (ÉRTÉK != 0 && ÉRTÉK < 128) hiba_ÉRTÉK("overlong modified UTF-8");
            } else if (ÉRTÉK >= 224 && ÉRTÉK <= 239 && szám + 1 < 끝) {
                int 가 = Fájl[szám++], MPERC_operandus = Fájl[szám++];
                if ((가 & 192) != 128 || (MPERC_operandus & 192) != 128) hiba_ÉRTÉK("invalid modified UTF-8");
                ÉRTÉK = (ÉRTÉK & 15) << 12 | (가 & 63) << 6 | MPERC_operandus & 63;
                if (ÉRTÉK < 2048) hiba_ÉRTÉK("overlong modified UTF-8");
            } else if (ÉRTÉK >= 128) hiba_ÉRTÉK("invalid modified UTF-8");
            halommemória_ÉRTÉK[hivatkozik + 2 + hossz_ÉRTÉK++] = ÉRTÉK;
        }
        halommemória_ÉRTÉK[hivatkozik + 1] = hossz_ÉRTÉK; sztring_hivatkozik[INDEX] = hivatkozik; return hivatkozik;
    }
    static int gazda_karakter(String ÉRTÉK) {
        int hivatkozik = kioszt_tár(1, ÉRTÉK.length()); if (HIBA) return 0;
        for (int szám = 0; szám < ÉRTÉK.length(); szám++) halommemória_ÉRTÉK[hivatkozik + 2 + szám] = ÉRTÉK.charAt(szám);
        return hivatkozik;
    }
    static void ír_SMS(int hivatkozik) {
        if (hivatkozik == 0) { felhasználó.Írás("null"); return; }
        if (!objektum_ÉRTÉK(hivatkozik, 1)) return;
        for (int szám = 0; szám < halommemória_ÉRTÉK[hivatkozik + 1]; szám++) felhasználó.ír_karakter_ÉRTÉK(halommemória_ÉRTÉK[hivatkozik + 2 + szám]);
    }
    static int számjegy_karakter(int ÉRTÉK) {
        int hivatkozik = kioszt_tár(1, 11); if (HIBA) return 0;
        int hossz_ÉRTÉK = 0;
        if (ÉRTÉK < 0) halommemória_ÉRTÉK[hivatkozik + 2 + hossz_ÉRTÉK++] = '-'; else ÉRTÉK = -ÉRTÉK;
        int helyzetindex = 1000000000; boolean Futtatás = false;
        while (helyzetindex != 0) {
            int szám = -(ÉRTÉK / helyzetindex);
            if (szám != 0 || Futtatás || helyzetindex == 1) { halommemória_ÉRTÉK[hivatkozik + 2 + hossz_ÉRTÉK++] = '0' + szám; Futtatás = true; }
            ÉRTÉK %= helyzetindex; helyzetindex /= 10;
        }
        halommemória_ÉRTÉK[hivatkozik + 1] = hossz_ÉRTÉK; return hivatkozik;
    }
    static int 정수해독(int hivatkozik) {
        if (!objektum_ÉRTÉK(hivatkozik, 1)) return 0;
        int hossz_ÉRTÉK = halommemória_ÉRTÉK[hivatkozik + 1], szám = 0, ÉRTÉK = 0; boolean 음수 = false;
        if (hossz_ÉRTÉK > 0 && (halommemória_ÉRTÉK[hivatkozik + 2] == '-' || halommemória_ÉRTÉK[hivatkozik + 2] == '+')) { 음수 = halommemória_ÉRTÉK[hivatkozik + 2] == '-'; szám++; }
        if (szám == hossz_ÉRTÉK) hiba_ÉRTÉK("NumberFormatException");
        for (; szám < hossz_ÉRTÉK && !HIBA; szám++) {
            int számjegy_ÉRTÉK = halommemória_ÉRTÉK[hivatkozik + 2 + szám] - '0';
            if (számjegy_ÉRTÉK < 0 || számjegy_ÉRTÉK > 9 || ÉRTÉK < -214748364 || ÉRTÉK == -214748364 && számjegy_ÉRTÉK > (음수 ? 8 : 7)) hiba_ÉRTÉK("NumberFormatException");
            ÉRTÉK = ÉRTÉK * 10 - számjegy_ÉRTÉK;
        }
        return 음수 ? ÉRTÉK : -ÉRTÉK;
    }
    static void 넣기(int ÉRTÉK, int beír_ÉRTÉK) {
        if (HIBA) return;
        if (doboz_INDEX < 0 || doboz_Sor[doboz_INDEX] >= metódus_Sor[doboz_metódus[doboz_INDEX]]) { hiba_ÉRTÉK("operand stack overflow"); return; }
        int tárolóhely_bejegyzés = doboz_INDEX * 128 + doboz_Sor[doboz_INDEX]++; operandus_Sor_ÉRTÉK[tárolóhely_bejegyzés] = ÉRTÉK; operandus_Sor_beír[tárolóhely_bejegyzés] = beír_ÉRTÉK;
    }
    static int 빼기(int beír_ÉRTÉK) {
        if (HIBA) return 0;
        if (doboz_INDEX < 0 || doboz_Sor[doboz_INDEX] < 1) { hiba_ÉRTÉK("operand stack underflow"); return 0; }
        int tárolóhely_bejegyzés = doboz_INDEX * 128 + --doboz_Sor[doboz_INDEX]; visszaküld_beír = operandus_Sor_beír[tárolóhely_bejegyzés];
        if (beír_ÉRTÉK != 0 && visszaküld_beír != beír_ÉRTÉK) hiba_ÉRTÉK("operand type mismatch");
        if (visszaküld_beír == 2) véd_ÉRTÉK(operandus_Sor_ÉRTÉK[tárolóhely_bejegyzés]);
        return operandus_Sor_ÉRTÉK[tárolóhely_bejegyzés];
    }
    static void 지역읽기(int INDEX, int beír_ÉRTÉK) {
        if (INDEX >= 함수지역[doboz_metódus[doboz_INDEX]] || INDEX < 0 || helyi_beír[doboz_INDEX * 128 + INDEX] != beír_ÉRTÉK) { hiba_ÉRTÉK("invalid or uninitialized local"); return; }
        넣기(helyi_ÉRTÉK[doboz_INDEX * 128 + INDEX], beír_ÉRTÉK);
    }
    static void ír_helyi(int INDEX, int beír_ÉRTÉK) {
        if (INDEX >= 함수지역[doboz_metódus[doboz_INDEX]] || INDEX < 0) { hiba_ÉRTÉK("local index out of range"); return; }
        int ÉRTÉK = 빼기(beír_ÉRTÉK); helyi_ÉRTÉK[doboz_INDEX * 128 + INDEX] = ÉRTÉK; helyi_beír[doboz_INDEX * 128 + INDEX] = beír_ÉRTÉK;
    }
    static int 명바() {
        int Pozíció = doboz_pozíció[doboz_INDEX];
        if (Pozíció < metódus_START[doboz_metódus[doboz_INDEX]] || Pozíció >= metódus_megszüntet[doboz_metódus[doboz_INDEX]]) { hiba_ÉRTÉK("instruction pointer out of range"); return 0; }
        doboz_pozíció[doboz_INDEX]++; return Fájl[Pozíció];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void áthelyez_ÉRTÉK(int Pozíció) {
        int FÜGGVÉNY_ÉRTÉK = doboz_metódus[doboz_INDEX];
        if (Pozíció < metódus_START[FÜGGVÉNY_ÉRTÉK] || Pozíció >= metódus_megszüntet[FÜGGVÉNY_ÉRTÉK] || határ_ÉRTÉK[Pozíció] != FÜGGVÉNY_ÉRTÉK + 1) hiba_ÉRTÉK("invalid branch target");
        else doboz_pozíció[doboz_INDEX] = Pozíció;
    }
    static void 호출(int FÜGGVÉNY_ÉRTÉK) {
        if (doboz_INDEX % 32 == 31) { hiba_ÉRTÉK("call stack limit (32)"); return; }
        int Tovább_cikk = doboz_INDEX + 1;
        for (int szám = 0; szám < 128; szám++) helyi_beír[Tovább_cikk * 128 + szám] = 0;
        for (int szám = metódus_argumentum_DARAB[FÜGGVÉNY_ÉRTÉK] - 1; szám >= 0; szám--) {
            helyi_ÉRTÉK[Tovább_cikk * 128 + szám] = 빼기(metódus_argumentum_beír[FÜGGVÉNY_ÉRTÉK * 16 + szám]); helyi_beír[Tovább_cikk * 128 + szám] = metódus_argumentum_beír[FÜGGVÉNY_ÉRTÉK * 16 + szám];
        }
        if (HIBA) return;
        doboz_INDEX = Tovább_cikk; inicializál_doboz[doboz_INDEX] = 0; doboz_metódus[doboz_INDEX] = FÜGGVÉNY_ÉRTÉK; doboz_pozíció[doboz_INDEX] = metódus_START[FÜGGVÉNY_ÉRTÉK]; doboz_Sor[doboz_INDEX] = 0;
    }
    static void visszaküld_KR(int beír_ÉRTÉK) {
        if (beír_ÉRTÉK != metódus_visszaküld[doboz_metódus[doboz_INDEX]]) { hiba_ÉRTÉK("return type mismatch"); return; }
        int ÉRTÉK = beír_ÉRTÉK == 0 ? 0 : 빼기(beír_ÉRTÉK);
        if (inicializál_doboz[doboz_INDEX] != 0) tanóra_Definíció_Állapot[inicializál_doboz[doboz_INDEX] - 1] = 2;
        if (doboz_lezár[doboz_INDEX] != 0) { kiad_lezár(doboz_lezár[doboz_INDEX]); doboz_lezár[doboz_INDEX] = 0; }
        doboz_INDEX--; if (doboz_INDEX >= aktuális_szál * 32 && beír_ÉRTÉK != 0) 넣기(ÉRTÉK, beír_ÉRTÉK);
    }
    static int[] Stream_fájlnév = new int[64];
    static void Fájl_Stream_hív(int tulajdonos_ÉRTÉK, int Név, int formáz_ÉRTÉK, int Parancs) {
        boolean Kimenet = szó_SMS(tulajdonos_ÉRTÉK, "java/io/FileOutputStream");
        int Altípus_ÉRTÉK = Kimenet ? 6 : 5;
        if (Parancs == 183 && szó_SMS(Név, "<init>")) {
            boolean 이어 = false;
            if (Kimenet && szó_SMS(formáz_ÉRTÉK, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!szó_SMS(formáz_ÉRTÉK, "(Ljava/lang/String;)V")) { hiba_ÉRTÉK("unsupported file stream constructor"); return; }
            int Fájl_bejegyzés_név = 빼기(2), Stream_ÉRTÉK = 빼기(2);
            if (!objektum_ÉRTÉK(Fájl_bejegyzés_név, 1) || !objektum_ÉRTÉK(Stream_ÉRTÉK, Altípus_ÉRTÉK) || HIBA) return;
            if (halommemória_ÉRTÉK[Stream_ÉRTÉK + 3] != 0) { hiba_ÉRTÉK("file stream already initialized"); return; }
            int hossz_ÉRTÉK = halommemória_ÉRTÉK[Fájl_bejegyzés_név + 1];
            if (hossz_ÉRTÉK < 1 || hossz_ÉRTÉK > 63) { hiba_ÉRTÉK("invalid file name length"); return; }
            for (int tárolóhely_bejegyzés = 0; tárolóhely_bejegyzés < hossz_ÉRTÉK; tárolóhely_bejegyzés++) {
                int ÉRTÉK = halommemória_ÉRTÉK[Fájl_bejegyzés_név + 2 + tárolóhely_bejegyzés];
                if (ÉRTÉK < 1) { hiba_ÉRTÉK("invalid file stream path"); return; }
                Stream_fájlnév[tárolóhely_bejegyzés] = ÉRTÉK;
            }
            Stream_fájlnév[hossz_ÉRTÉK] = 0;
            int 서술자 = felhasználó.파일서술자열기(Stream_fájlnév, Kimenet ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { hiba_ÉRTÉK("FileNotFoundException: file open failed"); return; }
            halommemória_ÉRTÉK[Stream_ÉRTÉK + 2] = 서술자; halommemória_ÉRTÉK[Stream_ÉRTÉK + 3] = 1;
            return;
        }
        if (Parancs != 182) { hiba_ÉRTÉK("invalid file stream invocation"); return; }
        if ((Kimenet && szó_SMS(Név, "write") || !Kimenet && szó_SMS(Név, "read"))
            && (szó_SMS(formáz_ÉRTÉK, Kimenet ? "([B)V" : "([B)I") || szó_SMS(formáz_ÉRTÉK, Kimenet ? "([BII)V" : "([BII)I"))) {
            boolean klip_ÉRTÉK = szó_SMS(formáz_ÉRTÉK, Kimenet ? "([BII)V" : "([BII)I");
            int bejegyzés_DARAB = klip_ÉRTÉK ? 빼기(1) : 0, 시작점 = klip_ÉRTÉK ? 빼기(1) : 0, adat_TÖMB = 빼기(2), objektum_hivatkozik = 빼기(2);
            if (!objektum_ÉRTÉK(adat_TÖMB, 20) || !objektum_ÉRTÉK(objektum_hivatkozik, Altípus_ÉRTÉK)) return;
            if (!klip_ÉRTÉK) bejegyzés_DARAB = halommemória_ÉRTÉK[adat_TÖMB + 1];
            if (시작점 < 0 || bejegyzés_DARAB < 0 || 시작점 > halommemória_ÉRTÉK[adat_TÖMB + 1] - bejegyzés_DARAB) { 예외던짐(6, "file buffer bounds"); return; }
            if (halommemória_ÉRTÉK[objektum_hivatkozik + 3] == 0 || halommemória_ÉRTÉK[objektum_hivatkozik + 2] < 0) { hiba_ÉRTÉK("IOException: stream closed"); return; }
            int Kész_DARAB = 0;
            while (Kész_DARAB < bejegyzés_DARAB && !HIBA) {
                int 반환값 = Kimenet ? felhasználó.파일한바이트쓰기(halommemória_ÉRTÉK[objektum_hivatkozik + 2], halommemória_ÉRTÉK[adat_TÖMB + 2 + 시작점 + Kész_DARAB]) : felhasználó.파일한바이트읽기(halommemória_ÉRTÉK[objektum_hivatkozik + 2]);
                if (반환값 < 0) { hiba_ÉRTÉK(Kimenet ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!Kimenet && 반환값 == 256) break;
                if (!Kimenet) halommemória_ÉRTÉK[adat_TÖMB + 2 + 시작점 + Kész_DARAB] = (byte)반환값;
                Kész_DARAB++;
            }
            if (!Kimenet) 넣기(bejegyzés_DARAB != 0 && Kész_DARAB == 0 ? -1 : Kész_DARAB, 1);
            return;
        }
        if (Kimenet && szó_SMS(Név, "flush") && szó_SMS(formáz_ÉRTÉK, "()V")) { int objektum_hivatkozik = 빼기(2); if (objektum_ÉRTÉK(objektum_hivatkozik, Altípus_ÉRTÉK) && halommemória_ÉRTÉK[objektum_hivatkozik + 2] < 0) hiba_ÉRTÉK("IOException: stream closed"); return; }
        int Művelet = -1, ÉRTÉK = 0;
        if (szó_SMS(Név, "close") && szó_SMS(formáz_ÉRTÉK, "()V")) Művelet = 0;
        if (!Kimenet && szó_SMS(Név, "read") && szó_SMS(formáz_ÉRTÉK, "()I")) Művelet = 1;
        if (Kimenet && szó_SMS(Név, "write") && szó_SMS(formáz_ÉRTÉK, "(I)V")) { Művelet = 2; ÉRTÉK = 빼기(1); }
        if (Művelet < 0) { hiba_ÉRTÉK("unsupported file stream method"); return; }
        int Stream_ÉRTÉK = 빼기(2);
        if (!objektum_ÉRTÉK(Stream_ÉRTÉK, Altípus_ÉRTÉK) || HIBA) return;
        if (halommemória_ÉRTÉK[Stream_ÉRTÉK + 3] == 0) { hiba_ÉRTÉK("uninitialized file stream"); return; }
        int 서술자 = halommemória_ÉRTÉK[Stream_ÉRTÉK + 2];
        if (Művelet == 0) {
            if (서술자 >= 0 && felhasználó.파일서술자닫기(서술자) < 0) hiba_ÉRTÉK("IOException: close failed");
            halommemória_ÉRTÉK[Stream_ÉRTÉK + 2] = -1; return;
        }
        if (서술자 < 0) { hiba_ÉRTÉK("IOException: stream closed"); return; }
        if (Művelet == 1) {
            int KR = felhasználó.파일한바이트읽기(서술자);
            if (KR < -1) hiba_ÉRTÉK("IOException: read failed"); else 넣기(KR == 256 ? -1 : KR, 1);
        } else if (felhasználó.파일한바이트쓰기(서술자, ÉRTÉK) != 1) hiba_ÉRTÉK("IOException: write failed");
    }
    static void hív_metódus(int INDEX, int Parancs) {
        if (INDEX <= 0 || INDEX >= állandó_címke.length || (állandó_címke[INDEX] != 10 && állandó_címke[INDEX] != 11)) { hiba_ÉRTÉK("invalid method reference"); return; }
        int tulajdonos_ÉRTÉK = osztálynév_SMS(상가[INDEX]), Név = hivatkozik_név(állandó_MPERC_ÉRTÉK[INDEX]), formáz_ÉRTÉK = referenciális_típus(állandó_MPERC_ÉRTÉK[INDEX]);
        if (HIBA) return;
        if (기본호출(tulajdonos_ÉRTÉK, Név, formáz_ÉRTÉK, Parancs)) return;
        if (szó_SMS(tulajdonos_ÉRTÉK, "java/io/FileInputStream") || szó_SMS(tulajdonos_ÉRTÉK, "java/io/FileOutputStream")) {
            Fájl_Stream_hív(tulajdonos_ÉRTÉK, Név, formáz_ÉRTÉK, Parancs); return;
        }
        if (Parancs == 184 && szó_SMS(tulajdonos_ÉRTÉK, "java/lang/Integer") && szó_SMS(Név, "parseInt") && szó_SMS(formáz_ÉRTÉK, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (Parancs == 182 && szó_SMS(tulajdonos_ÉRTÉK, "java/io/PrintStream") && (szó_SMS(Név, "println") || szó_SMS(Név, "print"))) {
            int beír_ÉRTÉK = 0, ÉRTÉK = 0;
            if (szó_SMS(formáz_ÉRTÉK, "(I)V")) { beír_ÉRTÉK = 1; ÉRTÉK = 빼기(1); }
            else if (szó_SMS(formáz_ÉRTÉK, "(Z)V")) { beír_ÉRTÉK = 2; ÉRTÉK = 빼기(1); }
            else if (szó_SMS(formáz_ÉRTÉK, "(C)V")) { beír_ÉRTÉK = 3; ÉRTÉK = 빼기(1); }
            else if (szó_SMS(formáz_ÉRTÉK, "(Ljava/lang/String;)V")) { beír_ÉRTÉK = 4; ÉRTÉK = 빼기(2); }
            else if (!szó_SMS(formáz_ÉRTÉK, "()V") || !szó_SMS(Név, "println")) hiba_ÉRTÉK("unsupported print descriptor");
            if (빼기(2) != -1) hiba_ÉRTÉK("invalid PrintStream receiver");
            if (HIBA) return;
            if (beír_ÉRTÉK == 1) 자바도구.ír_szám(ÉRTÉK);
            if (beír_ÉRTÉK == 2) felhasználó.Írás(ÉRTÉK == 0 ? "false" : "true");
            if (beír_ÉRTÉK == 3) felhasználó.ír_karakter_ÉRTÉK(ÉRTÉK & 65535);
            if (beír_ÉRTÉK == 4) ír_SMS(ÉRTÉK);
            if (szó_SMS(Név, "println")) felhasználó.ír_karakter_ÉRTÉK(10);
            return;
        }
        if (Parancs == 182 && szó_SMS(tulajdonos_ÉRTÉK, "java/lang/String")) {
            if (szó_SMS(Név, "length") && szó_SMS(formáz_ÉRTÉK, "()I")) {
                int hivatkozik = 빼기(2); if (objektum_ÉRTÉK(hivatkozik, 1)) 넣기(halommemória_ÉRTÉK[hivatkozik + 1], 1); return;
            }
            if (szó_SMS(Név, "charAt") && szó_SMS(formáz_ÉRTÉK, "(I)C")) {
                int alsó_index_ÉRTÉK = 빼기(1), hivatkozik = 빼기(2);
                if (objektum_ÉRTÉK(hivatkozik, 1)) {
                    if (alsó_index_ÉRTÉK < 0 || alsó_index_ÉRTÉK >= halommemória_ÉRTÉK[hivatkozik + 1]) hiba_ÉRTÉK("StringIndexOutOfBoundsException"); else 넣기(halommemória_ÉRTÉK[hivatkozik + 2 + alsó_index_ÉRTÉK], 1);
                }
                return;
            }
        }
        if (szó_SMS(tulajdonos_ÉRTÉK, "java/lang/StringBuilder")) {
            if (Parancs == 183 && szó_SMS(Név, "<init>") && szó_SMS(formáz_ÉRTÉK, "()V")) { objektum_ÉRTÉK(빼기(2), 4); return; }
            if (Parancs == 182 && szó_SMS(Név, "toString") && szó_SMS(formáz_ÉRTÉK, "()Ljava/lang/String;")) {
                int hivatkozik = 빼기(2); if (objektum_ÉRTÉK(hivatkozik, 4)) 넣기(halommemória_ÉRTÉK[hivatkozik + 2] == 0 ? gazda_karakter("") : halommemória_ÉRTÉK[hivatkozik + 2], 2); return;
            }
            if (Parancs == 182 && szó_SMS(Név, "append")) {
                int Szöveg = 0;
                if (szó_SMS(formáz_ÉRTÉK, "(I)Ljava/lang/StringBuilder;")) Szöveg = számjegy_karakter(빼기(1));
                else if (szó_SMS(formáz_ÉRTÉK, "(Z)Ljava/lang/StringBuilder;")) Szöveg = gazda_karakter(빼기(1) == 0 ? "false" : "true");
                else if (szó_SMS(formáz_ÉRTÉK, "(C)Ljava/lang/StringBuilder;")) {
                    int ÉRTÉK = 빼기(1); Szöveg = kioszt_tár(1, 1); if (!HIBA) halommemória_ÉRTÉK[Szöveg + 2] = ÉRTÉK & 65535;
                }
                else if (szó_SMS(formáz_ÉRTÉK, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { Szöveg = 빼기(2); if (Szöveg == 0) Szöveg = gazda_karakter("null"); }
                else { hiba_ÉRTÉK("unsupported StringBuilder append"); return; }
                int hivatkozik = 빼기(2); if (!objektum_ÉRTÉK(hivatkozik, 4) || !objektum_ÉRTÉK(Szöveg, 1)) return;
                int elülső_kamera_ÉRTÉK = halommemória_ÉRTÉK[hivatkozik + 2], elülső_kamera_ÉRTÉK_hossz = elülső_kamera_ÉRTÉK == 0 ? 0 : halommemória_ÉRTÉK[elülső_kamera_ÉRTÉK + 1], BACK_ÉRTÉK_hossz = halommemória_ÉRTÉK[Szöveg + 1];
                int 새글 = kioszt_tár(1, elülső_kamera_ÉRTÉK_hossz + BACK_ÉRTÉK_hossz); if (HIBA) return;
                for (int szám = 0; szám < elülső_kamera_ÉRTÉK_hossz; szám++) halommemória_ÉRTÉK[새글 + 2 + szám] = halommemória_ÉRTÉK[elülső_kamera_ÉRTÉK + 2 + szám];
                for (int szám = 0; szám < BACK_ÉRTÉK_hossz; szám++) halommemória_ÉRTÉK[새글 + 2 + elülső_kamera_ÉRTÉK_hossz + szám] = halommemória_ÉRTÉK[Szöveg + 2 + szám];
                halommemória_ÉRTÉK[hivatkozik + 2] = 새글; 넣기(hivatkozik, 2); return;
            }
        }
        int tanóra_Definíció = keres_tanóra_Definíció(tulajdonos_ÉRTÉK); if (tanóra_Definíció < 0 || HIBA) return;
        int Fájl_INDEX = keres_metódus(tanóra_Definíció, Név, formáz_ÉRTÉK);
        if (Fájl_INDEX < 0) {
            for (int kódpont = tanóra_Definíció, bejegyzés_DARAB = 0; kódpont >= 0 && bejegyzés_DARAB < 16; bejegyzés_DARAB++, kódpont = szülő_tanóra(kódpont))
                if (szó_SMS(tanóra_Definíció_szülő[kódpont], "java/lang/Thread")) { 가닥호출(Név, formáz_ÉRTÉK, Parancs); return; }
            hiba_ÉRTÉK("NoSuchMethodError"); return;
        }
        if (((metódus_hozzáfér[Fájl_INDEX] & 8) != 0) != (Parancs == 184)) { hiba_ÉRTÉK("method static/instance mismatch"); return; }
        if (Parancs == 184) { if (!inicializál(metódus_tulajdonos[Fájl_INDEX], 틀명령[doboz_INDEX])) return; }
        else {
            int 읽는자리 = doboz_Sor[doboz_INDEX] - metódus_argumentum_DARAB[Fájl_INDEX];
            if (읽는자리 < 0 || operandus_Sor_beír[doboz_INDEX * 128 + 읽는자리] != 2) { hiba_ÉRTÉK("invalid method receiver"); return; }
            int objektum_hivatkozik = operandus_Sor_ÉRTÉK[doboz_INDEX * 128 + 읽는자리];
            if (!informatikai_részleg_érvényes_objektum(objektum_hivatkozik)) return;
            if (halommemória_ÉRTÉK[objektum_hivatkozik] < 32 || !종포함(halommemória_ÉRTÉK[objektum_hivatkozik] - 32, tulajdonos_ÉRTÉK)) { hiba_ÉRTÉK("method receiver type mismatch"); return; }
            if (Parancs != 183) Fájl_INDEX = keres_metódus(halommemória_ÉRTÉK[objektum_hivatkozik] - 32, Név, formáz_ÉRTÉK);
        }
        if (Fájl_INDEX < 0 || (metódus_hozzáfér[Fájl_INDEX] & 0x400) != 0) { hiba_ÉRTÉK("AbstractMethodError"); return; }
        int lezár_hivatkozik = 0;
        if ((metódus_hozzáfér[Fájl_INDEX] & 32) != 0) {
            if (Parancs == 184) { int kódpont = metódus_tulajdonos[Fájl_INDEX]; if (tanóra_lezár[kódpont] == 0) tanóra_lezár[kódpont] = kioszt_tár(8, 0); lezár_hivatkozik = tanóra_lezár[kódpont]; }
            else lezár_hivatkozik = operandus_Sor_ÉRTÉK[doboz_INDEX * 128 + doboz_Sor[doboz_INDEX] - metódus_argumentum_DARAB[Fájl_INDEX]];
            if (!잠금얻기(lezár_hivatkozik)) { if (!HIBA) doboz_pozíció[doboz_INDEX] = 틀명령[doboz_INDEX]; return; }
        }
        호출(Fájl_INDEX); if (!HIBA) doboz_lezár[doboz_INDEX] = lezár_hivatkozik;
    }
    static boolean 배열저장가능(int TÖMB_hivatkozik, int adat_ÉRTÉK) {
        if (adat_ÉRTÉK == 0 || tömbelem[TÖMB_hivatkozik] == 0) return true;
        boolean 성공여부 = tömbelem[TÖMB_hivatkozik] == -1 ? (adat_ÉRTÉK > 0 && adat_ÉRTÉK < halommemória_megszüntet_pozíció && halommemória_ÉRTÉK[adat_ÉRTÉK] == 1) : 맞는객체(adat_ÉRTÉK, tömbelem[TÖMB_hivatkozik]);
        if (!성공여부 && !HIBA) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int TÖMB_tárolóhely(int hivatkozik, int alsó_index_ÉRTÉK, int beír_ÉRTÉK) {
        if (!objektum_ÉRTÉK(hivatkozik, beír_ÉRTÉK)) return 0;
        if (alsó_index_ÉRTÉK < 0 || alsó_index_ÉRTÉK >= halommemória_ÉRTÉK[hivatkozik + 1]) { hiba_ÉRTÉK("ArrayIndexOutOfBoundsException"); return 0; }
        return hivatkozik + 2 + alsó_index_ÉRTÉK;
    }
    static void végrehajt_parancs() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (HIBA) { if (던진객체 != 0) leíró_kivétel(); if (HIBA || doboz_INDEX < aktuális_szál * 32) break; }
            if (doboz_INDEX < aktuális_szál * 32 || változáskérés || --조각 == 0) { if (!vált_szál()) break; 조각 = 100; }
            if (doboz_INDEX == 0 && tanóra_Definíció_Állapot[bejegyzés_tanóra_Definíció] != 2 && !inicializál(bejegyzés_tanóra_Definíció, doboz_pozíció[doboz_INDEX])) continue;
            if (doboz_INDEX == aktuális_szál * 32 && aktuális_szál != 0 && (metódus_hozzáfér[doboz_metódus[doboz_INDEX]] & 32) != 0 && doboz_lezár[doboz_INDEX] == 0) {
                int objektum_hivatkozik = szál_cél[aktuális_szál]; if (!잠금얻기(objektum_hivatkozik)) { if (HIBA) break; continue; } doboz_lezár[doboz_INDEX] = objektum_hivatkozik;
            }
            잠시수 = 0;
            if (--남음 == 0) { hiba_ÉRTÉK("instruction limit (500000)"); break; }
            int Futtatás = doboz_pozíció[doboz_INDEX]; 틀명령[doboz_INDEX] = Futtatás; int ÉRTÉK = 명바();
            if (HIBA) break;
            if (ÉRTÉK == 0) continue;
            if (ÉRTÉK == 1) { 넣기(0, 2); continue; }
            if (ÉRTÉK >= 2 && ÉRTÉK <= 8) { 넣기(ÉRTÉK - 3, 1); continue; }
            if (ÉRTÉK == 16) { 넣기((byte)명바(), 1); continue; }
            if (ÉRTÉK == 17) { 넣기((short)명짧(), 1); continue; }
            if (ÉRTÉK == 18 || ÉRTÉK == 19) {
                int szám = metódus_tulajdonos[doboz_metódus[doboz_INDEX]] * 512 + (ÉRTÉK == 18 ? 명바() : 명짧());
                if (szám <= 0 || szám >= állandó_címke.length) hiba_ÉRTÉK("invalid ldc constant");
                else if (állandó_címke[szám] == 3) 넣기(상가[szám], 1);
                else if (állandó_címke[szám] == 8) 넣기(állandó_SMS(상가[szám]), 2);
                else hiba_ÉRTÉK("unsupported ldc constant");
                continue;
            }
            if (ÉRTÉK == 21 || ÉRTÉK == 25) { 지역읽기(명바(), ÉRTÉK == 21 ? 1 : 2); continue; }
            if (ÉRTÉK >= 26 && ÉRTÉK <= 29) { 지역읽기(ÉRTÉK - 26, 1); continue; }
            if (ÉRTÉK >= 42 && ÉRTÉK <= 45) { 지역읽기(ÉRTÉK - 42, 2); continue; }
            if (ÉRTÉK == 54 || ÉRTÉK == 58) { ír_helyi(명바(), ÉRTÉK == 54 ? 1 : 2); continue; }
            if (ÉRTÉK >= 59 && ÉRTÉK <= 62) { ír_helyi(ÉRTÉK - 59, 1); continue; }
            if (ÉRTÉK >= 75 && ÉRTÉK <= 78) { ír_helyi(ÉRTÉK - 75, 2); continue; }
            if (ÉRTÉK == 46 || ÉRTÉK >= 50 && ÉRTÉK <= 53) {
                int bejegyzés_pozíció = 빼기(1), objektum_hivatkozik = 빼기(2), terület_KÓD = ÉRTÉK == 46 ? 2 : ÉRTÉK == 50 ? 3 : ÉRTÉK == 51 ? 20 : ÉRTÉK == 52 ? 22 : 23;
                if (ÉRTÉK == 51 && objektum_hivatkozik > 0 && objektum_hivatkozik < halommemória_megszüntet_pozíció && halommemória_ÉRTÉK[objektum_hivatkozik] == 21) terület_KÓD = 21;
                int 읽는자리 = TÖMB_tárolóhely(objektum_hivatkozik, bejegyzés_pozíció, terület_KÓD); if (!HIBA) 넣기(halommemória_ÉRTÉK[읽는자리], ÉRTÉK == 50 ? 2 : 1); continue;
            }
            if (ÉRTÉK == 79 || ÉRTÉK >= 83 && ÉRTÉK <= 86) {
                int bejegyzés_hivatkozik = 빼기(ÉRTÉK == 83 ? 2 : 1), bejegyzés_pozíció = 빼기(1), objektum_hivatkozik = 빼기(2), terület_KÓD = ÉRTÉK == 79 ? 2 : ÉRTÉK == 83 ? 3 : ÉRTÉK == 84 ? 20 : ÉRTÉK == 85 ? 22 : 23;
                if (ÉRTÉK == 84 && objektum_hivatkozik > 0 && objektum_hivatkozik < halommemória_megszüntet_pozíció && halommemória_ÉRTÉK[objektum_hivatkozik] == 21) terület_KÓD = 21;
                int 읽는자리 = TÖMB_tárolóhely(objektum_hivatkozik, bejegyzés_pozíció, terület_KÓD);
                if (!HIBA && terület_KÓD == 3 && !배열저장가능(objektum_hivatkozik, bejegyzés_hivatkozik)) continue;
                if (!HIBA) halommemória_ÉRTÉK[읽는자리] = terület_KÓD == 20 ? (byte)bejegyzés_hivatkozik : terület_KÓD == 21 ? bejegyzés_hivatkozik & 1 : terület_KÓD == 22 ? (char)bejegyzés_hivatkozik : terület_KÓD == 23 ? (short)bejegyzés_hivatkozik : bejegyzés_hivatkozik;
                continue;
            }
            if (ÉRTÉK >= 87 && ÉRTÉK <= 95) { 스택명령(ÉRTÉK); continue; }
            if (ÉRTÉK == 96 || ÉRTÉK == 100 || ÉRTÉK == 104 || ÉRTÉK == 108 || ÉRTÉK == 112 || ÉRTÉK == 120
                || ÉRTÉK == 122 || ÉRTÉK == 124 || ÉRTÉK == 126 || ÉRTÉK == 128 || ÉRTÉK == 130) {
                int MPERC_operandus = 빼기(1), 가 = 빼기(1), KR = 0;
                if ((ÉRTÉK == 108 || ÉRTÉK == 112) && MPERC_operandus == 0) { hiba_ÉRTÉK("ArithmeticException: / by zero"); continue; }
                if (ÉRTÉK == 96) KR = 가 + MPERC_operandus;
                if (ÉRTÉK == 100) KR = 가 - MPERC_operandus;
                if (ÉRTÉK == 104) KR = 가 * MPERC_operandus;
                if (ÉRTÉK == 108) KR = 가 / MPERC_operandus;
                if (ÉRTÉK == 112) KR = 가 % MPERC_operandus;
                if (ÉRTÉK == 120) KR = 가 << MPERC_operandus;
                if (ÉRTÉK == 122) KR = 가 >> MPERC_operandus;
                if (ÉRTÉK == 124) KR = 가 >>> MPERC_operandus;
                if (ÉRTÉK == 126) KR = 가 & MPERC_operandus;
                if (ÉRTÉK == 128) KR = 가 | MPERC_operandus;
                if (ÉRTÉK == 130) KR = 가 ^ MPERC_operandus;
                넣기(KR, 1); continue;
            }
            if (ÉRTÉK == 116) { 넣기(-빼기(1), 1); continue; }
            if (ÉRTÉK == 132) {
                int helyi_hatókör = 명바(), növekmény_lépés = (byte)명바(); 지역읽기(helyi_hatókör, 1); 넣기(빼기(1) + növekmény_lépés, 1); ír_helyi(helyi_hatókör, 1); continue;
            }
            if (ÉRTÉK >= 145 && ÉRTÉK <= 147) {
                int szám = 빼기(1); 넣기(ÉRTÉK == 145 ? (byte)szám : ÉRTÉK == 146 ? (char)szám : (short)szám, 1); continue;
            }
            if (ÉRTÉK >= 153 && ÉRTÉK <= 167 || ÉRTÉK == 198 || ÉRTÉK == 199) {
                int cél_ÉRTÉK = Futtatás + (short)명짧(); boolean 갈까 = ÉRTÉK == 167;
                if (ÉRTÉK >= 153 && ÉRTÉK <= 158) {
                    int szám = 빼기(1); 갈까 = ÉRTÉK == 153 ? szám == 0 : ÉRTÉK == 154 ? szám != 0 : ÉRTÉK == 155 ? szám < 0 : ÉRTÉK == 156 ? szám >= 0 : ÉRTÉK == 157 ? szám > 0 : szám <= 0;
                } else if (ÉRTÉK >= 159 && ÉRTÉK <= 166) {
                    int MPERC_operandus = 빼기(ÉRTÉK >= 165 ? 2 : 1), 가 = 빼기(ÉRTÉK >= 165 ? 2 : 1);
                    갈까 = ÉRTÉK == 159 || ÉRTÉK == 165 ? 가 == MPERC_operandus : ÉRTÉK == 160 || ÉRTÉK == 166 ? 가 != MPERC_operandus : ÉRTÉK == 161 ? 가 < MPERC_operandus : ÉRTÉK == 162 ? 가 >= MPERC_operandus : ÉRTÉK == 163 ? 가 > MPERC_operandus : 가 <= MPERC_operandus;
                } else if (ÉRTÉK == 198 || ÉRTÉK == 199) { int szám = 빼기(2); 갈까 = ÉRTÉK == 198 ? szám == 0 : szám != 0; }
                if (갈까) áthelyez_ÉRTÉK(cél_ÉRTÉK); continue;
            }
            if (ÉRTÉK == 172 || ÉRTÉK == 176 || ÉRTÉK == 177) { visszaküld_KR(ÉRTÉK == 172 ? 1 : ÉRTÉK == 176 ? 2 : 0); continue; }
            if (ÉRTÉK >= 178 && ÉRTÉK <= 181) { 필드호출(명상수(), ÉRTÉK, Futtatás); continue; }
            if (ÉRTÉK >= 182 && ÉRTÉK <= 185) {
                int 부호값 = 명상수();
                if (ÉRTÉK == 185) { int összesen_DARAB = 명바(); if (összesen_DARAB == 0 || 명바() != 0) { hiba_ÉRTÉK("invalid invokeinterface operands"); continue; } }
                hív_metódus(부호값, ÉRTÉK); continue;
            }
            if (ÉRTÉK == 187) { 새객체(osztálynév_SMS(명상수()), Futtatás); continue; }
            if (ÉRTÉK == 188 || ÉRTÉK == 189) {
                int terület_KÓD = 3, komponens = 0;
                if (ÉRTÉK == 188) { int 임시값 = 명바(); terület_KÓD = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else komponens = osztálynév_SMS(명상수());
                if (terület_KÓD == 0) { hiba_ÉRTÉK("unsupported primitive array type"); continue; }
                int érvényes_hossz = 빼기(1), objektum_hivatkozik = kioszt_tár(terület_KÓD, érvényes_hossz); if (!HIBA) tömbelem[objektum_hivatkozik] = komponens; 넣기(objektum_hivatkozik, 2); continue;
            }
            if (ÉRTÉK == 190) {
                int objektum_hivatkozik = 빼기(2);
                if (informatikai_részleg_érvényes_objektum(objektum_hivatkozik)) { int Összehasonlítás_pozíció = halommemória_ÉRTÉK[objektum_hivatkozik]; if (Összehasonlítás_pozíció != 2 && Összehasonlítás_pozíció != 3 && (Összehasonlítás_pozíció < 20 || Összehasonlítás_pozíció > 23)) hiba_ÉRTÉK("not an array"); else 넣기(halommemória_ÉRTÉK[objektum_hivatkozik + 1], 1); }
                continue;
            }
            if (ÉRTÉK == 191) {
                int objektum_hivatkozik = 빼기(2); if (informatikai_részleg_érvényes_objektum(objektum_hivatkozik)) { if (halommemória_ÉRTÉK[objektum_hivatkozik] != 9) hiba_ÉRTÉK("athrow requires supported Throwable"); else { 던진객체 = objektum_hivatkozik; HIBA = true; } }
                continue;
            }
            if (ÉRTÉK == 192 || ÉRTÉK == 193) {
                int név_állandó = osztálynév_SMS(명상수()), objektum_hivatkozik = 빼기(2); boolean HOL_VAN = 맞는객체(objektum_hivatkozik, név_állandó);
                if (ÉRTÉK == 193) 넣기(objektum_hivatkozik != 0 && HOL_VAN ? 1 : 0, 1);
                else { if (!HOL_VAN && !HIBA) hiba_ÉRTÉK("ClassCastException"); 넣기(objektum_hivatkozik, 2); }
                continue;
            }
            if (ÉRTÉK == 170 || ÉRTÉK == 171) {
                int 읽는자리 = Futtatás + 1, Fájl_INDEX = doboz_metódus[doboz_INDEX], Kulcs_hivatkozik = 빼기(1);
                while ((읽는자리 - metódus_START[Fájl_INDEX]) % 4 != 0) 읽는자리++;
                int cél_CÍM = pozíció_egész_szám(읽는자리);
                if (ÉRTÉK == 170) { int 낮은값 = pozíció_egész_szám(읽는자리 + 4), 높은값 = pozíció_egész_szám(읽는자리 + 8); if (Kulcs_hivatkozik >= 낮은값 && Kulcs_hivatkozik <= 높은값) cél_CÍM = pozíció_egész_szám(읽는자리 + 12 + (Kulcs_hivatkozik - 낮은값) * 4); }
                else { int összesen_DARAB = pozíció_egész_szám(읽는자리 + 4); for (int Loop_INDEX = 0; Loop_INDEX < összesen_DARAB; Loop_INDEX++) if (pozíció_egész_szám(읽는자리 + 8 + Loop_INDEX * 8) == Kulcs_hivatkozik) cél_CÍM = pozíció_egész_szám(읽는자리 + 12 + Loop_INDEX * 8); }
                áthelyez_ÉRTÉK(Futtatás + cél_CÍM); continue;
            }
            if (ÉRTÉK == 200) { áthelyez_ÉRTÉK(Futtatás + pozíció_egész_szám(Futtatás + 1)); continue; }
            if (ÉRTÉK == 194 || ÉRTÉK == 195) {
                int objektum_hivatkozik = 빼기(2);
                if (ÉRTÉK == 195) kiad_lezár(objektum_hivatkozik);
                else if (!잠금얻기(objektum_hivatkozik) && !HIBA) { 넣기(objektum_hivatkozik, 2); doboz_pozíció[doboz_INDEX] = Futtatás; }
                continue;
            }
            if (ÉRTÉK == 196) {
                int parancs_KÓD = 명바(), bejegyzés_pozíció = 명짧();
                if (parancs_KÓD == 21 || parancs_KÓD == 25) 지역읽기(bejegyzés_pozíció, parancs_KÓD == 21 ? 1 : 2);
                else if (parancs_KÓD == 54 || parancs_KÓD == 58) ír_helyi(bejegyzés_pozíció, parancs_KÓD == 54 ? 1 : 2);
                else if (parancs_KÓD == 132) { int DELTA_ÉRTÉK = (short)명짧(); 지역읽기(bejegyzés_pozíció, 1); 넣기(빼기(1) + DELTA_ÉRTÉK, 1); ír_helyi(bejegyzés_pozíció, 1); }
                else hiba_ÉRTÉK("unsupported wide opcode");
                continue;
            }
            hiba_ÉRTÉK("unsupported bytecode");
        }
    }
    static int keres_tanóra_Definíció(int Név) {
        for (int Loop_INDEX = 0; Loop_INDEX < tanóra_Definíció_DARAB; Loop_INDEX++) if (tanóra_Definíció_név[Loop_INDEX] != 0 && 같은말(tanóra_Definíció_név[Loop_INDEX], Név)) return Loop_INDEX;
        return betölt_tanóra_Definíció(állandó_SMS(Név));
    }
    static int betölt_tanóra_Definíció(int név_sztring) {
        if (!objektum_ÉRTÉK(név_sztring, 1)) return -1;
        int hossz_ÉRTÉK = halommemória_ÉRTÉK[név_sztring + 1];
        if (hossz_ÉRTÉK < 1 || hossz_ÉRTÉK > 505 || tanóra_Definíció_DARAB == 16) { hiba_ÉRTÉK("class name/count limit"); return -1; }
        for (int Loop_INDEX = 0; Loop_INDEX < hossz_ÉRTÉK; Loop_INDEX++) { int kódpont = halommemória_ÉRTÉK[név_sztring + 2 + Loop_INDEX]; fájlnév_SMS[Loop_INDEX] = kódpont == '/' ? '.' : kódpont; }
        fájlnév_SMS[hossz_ÉRTÉK] = '.'; fájlnév_SMS[hossz_ÉRTÉK + 1] = 'c'; fájlnév_SMS[hossz_ÉRTÉK + 2] = 'l'; fájlnév_SMS[hossz_ÉRTÉK + 3] = 'a'; fájlnév_SMS[hossz_ÉRTÉK + 4] = 's'; fájlnév_SMS[hossz_ÉRTÉK + 5] = 's'; fájlnév_SMS[hossz_ÉRTÉK + 6] = 0;
        int Méret = felhasználó.파일읽기(fájlnév_SMS, ideiglenes_fájl);
        if (Méret < 0) { hiba_ÉRTÉK("ClassNotFoundException"); return -1; }
        int tanóra_Definíció = tanóra_Definíció_DARAB++; tanóra_Definíció_méretez[tanóra_Definíció] = Méret;
        for (int Loop_INDEX = 0; Loop_INDEX < Méret; Loop_INDEX++) Fájl[tanóra_Definíció * 16384 + Loop_INDEX] = ideiglenes_fájl[Loop_INDEX];
        클래스읽기(tanóra_Definíció); if (HIBA) return -1;
        int tényleges_adat = állandó_SMS(tanóra_Definíció_név[tanóra_Definíció]);
        if (!글같음(tényleges_adat, név_sztring, true)) { hiba_ÉRTÉK("class name does not match file"); return -1; }
        int szülő_ÉRTÉK = tanóra_Definíció_szülő[tanóra_Definíció];
        if (szülő_ÉRTÉK != 0 && !szó_SMS(szülő_ÉRTÉK, "java/lang/Object") && !szó_SMS(szülő_ÉRTÉK, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 újrapróbál_ÉRTÉK 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = keres_tanóra_Definíció(szülő_ÉRTÉK);
            if (HIBA || 위 < 0) return -1;
            int 읽는자리 = 위, fázis_DARAB = 0;
            while (읽는자리 >= 0 && fázis_DARAB++ < 16) {
                if (읽는자리 == tanóra_Definíció) { hiba_ÉRTÉK("cyclic inheritance"); return -1; }
                읽는자리 = szülő_tanóra(읽는자리);
            }
            int 시작변위 = tanóra_tárolóhely_DARAB[위];
            for (int Fájl_INDEX = 0; Fájl_INDEX < tárolóhely_DARAB; Fájl_INDEX++) if (tárolóhely_tulajdonos[Fájl_INDEX] == tanóra_Definíció && (tárolóhely_Engedélyek[Fájl_INDEX] & 8) == 0) tárolóhely_pozíció[Fájl_INDEX] += 시작변위;
            tanóra_tárolóhely_DARAB[tanóra_Definíció] += 시작변위;
        }
        return tanóra_Definíció;
    }
    static int szülő_tanóra(int tanóra_Definíció) {
        int Név = tanóra_Definíció_szülő[tanóra_Definíció];
        for (int Loop_INDEX = 0; Loop_INDEX < tanóra_Definíció_DARAB; Loop_INDEX++) if (Név != 0 && tanóra_Definíció_név[Loop_INDEX] != 0 && 같은말(tanóra_Definíció_név[Loop_INDEX], Név)) return Loop_INDEX;
        return -1;
    }
    static int keres_metódus(int tanóra_Definíció, int Név, int formáz_ÉRTÉK) {
        for (int 깊이 = 0; tanóra_Definíció >= 0 && 깊이 < 16; 깊이++, tanóra_Definíció = szülő_tanóra(tanóra_Definíció)) {
            for (int Loop_INDEX = 0; Loop_INDEX < metódus_DARAB; Loop_INDEX++) if (metódus_tulajdonos[Loop_INDEX] == tanóra_Definíció && 같은말(metódus_név_SMS[Loop_INDEX], Név) && 같은말(metódus_beír[Loop_INDEX], formáz_ÉRTÉK)) return Loop_INDEX;
        }
        return -1;
    }
    static int név_metódus(int tanóra_Definíció, String Név, String formáz_ÉRTÉK) {
        for (int 깊이 = 0; tanóra_Definíció >= 0 && 깊이 < 16; 깊이++, tanóra_Definíció = szülő_tanóra(tanóra_Definíció))
            for (int Loop_INDEX = 0; Loop_INDEX < metódus_DARAB; Loop_INDEX++) if (metódus_tulajdonos[Loop_INDEX] == tanóra_Definíció && szó_SMS(metódus_név_SMS[Loop_INDEX], Név) && szó_SMS(metódus_beír[Loop_INDEX], formáz_ÉRTÉK)) return Loop_INDEX;
        return -1;
    }
    static int beír_Altípus(int Név) { return Fájl[상가[Név]] == 'L' || Fájl[상가[Név]] == '[' ? 2 : 1; }
    static boolean inicializál(int tanóra_Definíció, int parancs_START) {
        if (tanóra_Definíció < 0 || HIBA) return false;
        if (tanóra_Definíció_Állapot[tanóra_Definíció] == 3) { hiba_ÉRTÉK("NoClassDefFoundError: initialization failed"); return false; }
        if (tanóra_Definíció_Állapot[tanóra_Definíció] == 1 && tanóra_szál[tanóra_Definíció] != aktuális_szál) { doboz_pozíció[doboz_INDEX] = parancs_START; változáskérés = true; return false; }
        if (tanóra_Definíció_Állapot[tanóra_Definíció] != 0) return true;
        int 위 = szülő_tanóra(tanóra_Definíció);
        if (위 >= 0 && !inicializál(위, parancs_START)) return false;
        tanóra_Definíció_Állapot[tanóra_Definíció] = 1; tanóra_szál[tanóra_Definíció] = aktuális_szál;
        if (inicializál_tanóra_Definíció[tanóra_Definíció] != 0) {
            doboz_pozíció[doboz_INDEX] = parancs_START;
            호출(inicializál_tanóra_Definíció[tanóra_Definíció] - 1); if (!HIBA) inicializál_doboz[doboz_INDEX] = tanóra_Definíció + 1;
            return false;
        }
        tanóra_Definíció_Állapot[tanóra_Definíció] = 2; return true;
    }
    static void 필드호출(int INDEX, int Parancs, int Futtatás) {
        if (!csekk_állandó(INDEX, 9)) return;
        int tulajdonos_ÉRTÉK = osztálynév_SMS(상가[INDEX]), Név = hivatkozik_név(állandó_MPERC_ÉRTÉK[INDEX]), formáz_ÉRTÉK = referenciális_típus(állandó_MPERC_ÉRTÉK[INDEX]);
        if (szó_SMS(tulajdonos_ÉRTÉK, "java/lang/System") && (szó_SMS(Név, "out") || szó_SMS(Név, "err")) && szó_SMS(formáz_ÉRTÉK, "Ljava/io/PrintStream;") && Parancs == 178) { 넣기(-1, 2); return; }
        int tanóra_Definíció = keres_tanóra_Definíció(tulajdonos_ÉRTÉK); if (tanóra_Definíció < 0 || HIBA) return;
        int 찾음 = -1;
        for (int 읽는자리 = tanóra_Definíció, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = szülő_tanóra(읽는자리))
            for (int Fájl_INDEX = 0; Fájl_INDEX < tárolóhely_DARAB; Fájl_INDEX++) if (tárolóhely_tulajdonos[Fájl_INDEX] == 읽는자리 && 같은말(tárolóhely_név[Fájl_INDEX], Név) && 같은말(tárolóhely_beír[Fájl_INDEX], formáz_ÉRTÉK)) 찾음 = Fájl_INDEX;
        if (찾음 < 0) { hiba_ÉRTÉK("NoSuchFieldError"); return; }
        boolean statikus_ÉRTÉK = Parancs == 178 || Parancs == 179;
        if (statikus_ÉRTÉK != ((tárolóhely_Engedélyek[찾음] & 8) != 0)) { hiba_ÉRTÉK("field static/instance mismatch"); return; }
        if (statikus_ÉRTÉK && !inicializál(tárolóhely_tulajdonos[찾음], Futtatás)) return;
        int beír_ÉRTÉK = beír_Altípus(formáz_ÉRTÉK), ÉRTÉK = 0;
        if (Parancs == 179 || Parancs == 181) ÉRTÉK = 빼기(beír_ÉRTÉK);
        if (statikus_ÉRTÉK) { if (Parancs == 178) 넣기(tárolóhely_adat[찾음], beír_ÉRTÉK); else if (!HIBA) tárolóhely_adat[찾음] = ÉRTÉK; return; }
        int objektum_hivatkozik = 빼기(2);
        if (!informatikai_részleg_érvényes_objektum(objektum_hivatkozik)) return;
        if (halommemória_ÉRTÉK[objektum_hivatkozik] < 32 || !종포함(halommemória_ÉRTÉK[objektum_hivatkozik] - 32, tulajdonos_ÉRTÉK)) { hiba_ÉRTÉK("field receiver type mismatch"); return; }
        int 보관칸 = objektum_hivatkozik + 2 + tárolóhely_pozíció[찾음];
        if (Parancs == 180) 넣기(halommemória_ÉRTÉK[보관칸], beír_ÉRTÉK);
        else if (!HIBA) { halommemória_ÉRTÉK[보관칸] = ÉRTÉK; halommemória_hivatkozik[보관칸] = beír_ÉRTÉK == 2 ? 1 : 0; }
    }
    static boolean 종포함(int tanóra_Definíció, int Név) {
        for (int 중첩깊이 = 0; tanóra_Definíció >= 0 && 중첩깊이 < 16; 중첩깊이++, tanóra_Definíció = szülő_tanóra(tanóra_Definíció)) {
            if (같은말(tanóra_Definíció_név[tanóra_Definíció], Név) || (tanóra_Definíció_szülő[tanóra_Definíció] != 0 && 같은말(tanóra_Definíció_szülő[tanóra_Definíció], Név))) return true;
            for (int belső_pozíció = 0; belső_pozíció < tanóra_csatoló_DARAB[tanóra_Definíció]; belső_pozíció++) if (같은말(tanóra_csatoló[tanóra_Definíció * 16 + belső_pozíció], Név)) return true;
        }
        return false;
    }
    static boolean 글같음(int 첫값, int bájt_adat, boolean ÚTVONAL) {
        if (첫값 == bájt_adat) return true;
        if (첫값 <= 0 || bájt_adat <= 0 || halommemória_ÉRTÉK[첫값] != 1 || halommemória_ÉRTÉK[bájt_adat] != 1 || halommemória_ÉRTÉK[첫값 + 1] != halommemória_ÉRTÉK[bájt_adat + 1]) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < halommemória_ÉRTÉK[첫값 + 1]; Loop_INDEX++) {
            int x_koordináta = halommemória_ÉRTÉK[첫값 + 2 + Loop_INDEX], Y_koordináta = halommemória_ÉRTÉK[bájt_adat + 2 + Loop_INDEX];
            if (ÚTVONAL) { if (x_koordináta == '.') x_koordináta = '/'; if (Y_koordináta == '.') Y_koordináta = '/'; }
            if (x_koordináta != Y_koordináta) return false;
        }
        return true;
    }
    static boolean informatikai_részleg_érvényes_objektum(int objektum_hivatkozik) {
        if (objektum_hivatkozik == 0) { hiba_ÉRTÉK("NullPointerException"); return false; }
        if (objektum_hivatkozik < 1 || objektum_hivatkozik >= halommemória_megszüntet_pozíció || 힙폭[objektum_hivatkozik] < 2 || halommemória_ÉRTÉK[objektum_hivatkozik] == 0) { hiba_ÉRTÉK("invalid object reference"); return false; }
        return true;
    }
    static void véd_ÉRTÉK(int objektum_hivatkozik) {
        if (objektum_hivatkozik > 0 && objektum_hivatkozik < halommemória_megszüntet_pozíció && 힙폭[objektum_hivatkozik] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = objektum_hivatkozik;
    }
    static void bemutató_ÉRTÉK(int objektum_hivatkozik) {
        if (objektum_hivatkozik > 0 && objektum_hivatkozik < halommemória_megszüntet_pozíció && 힙폭[objektum_hivatkozik] >= 2 && halommemória_ÉRTÉK[objektum_hivatkozik] != 0 && 힙표시[objektum_hivatkozik] == 0) {
            힙표시[objektum_hivatkozik] = 1; 표시대기[kijelző_DARAB++] = objektum_hivatkozik;
        }
    }
    static void 수거() {
        kijelző_DARAB = 0; sokaság_DARAB++;
        for (int csekk_pozíció = 1; csekk_pozíció < halommemória_megszüntet_pozíció; csekk_pozíció += 힙폭[csekk_pozíció]) 힙표시[csekk_pozíció] = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < sztring_hivatkozik.length; Loop_INDEX++) bemutató_ÉRTÉK(sztring_hivatkozik[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < tárolóhely_DARAB; Loop_INDEX++) if ((tárolóhely_Engedélyek[Loop_INDEX] & 8) != 0 && beír_Altípus(tárolóhely_beír[Loop_INDEX]) == 2) bemutató_ÉRTÉK(tárolóhely_adat[Loop_INDEX]);
        for (int 임시값 = 0; 임시값 < szálak_száma; 임시값++) {
            bemutató_ÉRTÉK(szál_objektum[임시값]); bemutató_ÉRTÉK(szál_cél[임시값]);
            int 꼭대기자리 = 임시값 == aktuális_szál ? doboz_INDEX : szál_doboz[임시값];
            for (int Fájl_INDEX = 임시값 * 32; Fájl_INDEX <= 꼭대기자리; Fájl_INDEX++) {
                for (int belső_pozíció = 0; belső_pozíció < 함수지역[doboz_metódus[Fájl_INDEX]]; belső_pozíció++) if (helyi_beír[Fájl_INDEX * 128 + belső_pozíció] == 2) bemutató_ÉRTÉK(helyi_ÉRTÉK[Fájl_INDEX * 128 + belső_pozíció]);
                for (int belső_pozíció = 0; belső_pozíció < doboz_Sor[Fájl_INDEX]; belső_pozíció++) if (operandus_Sor_beír[Fájl_INDEX * 128 + belső_pozíció] == 2) bemutató_ÉRTÉK(operandus_Sor_ÉRTÉK[Fájl_INDEX * 128 + belső_pozíció]);
            }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 화면참조.length; Loop_INDEX++) bemutató_ÉRTÉK(화면참조[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < 나중수; Loop_INDEX++) bemutató_ÉRTÉK(나중실행[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < tár_egész_szám.length; Loop_INDEX++) bemutató_ÉRTÉK(tár_egész_szám[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < tanóra_Definíció_DARAB; Loop_INDEX++) bemutató_ÉRTÉK(tanóra_lezár[Loop_INDEX]);
        for (int csekk_pozíció = 1; csekk_pozíció < halommemória_megszüntet_pozíció; csekk_pozíció += 힙폭[csekk_pozíció]) if (잠금깊이[csekk_pozíció] > 0) bemutató_ÉRTÉK(csekk_pozíció);
        bemutató_ÉRTÉK(던진객체);
        for (int Loop_INDEX = 0; Loop_INDEX < 잠시수; Loop_INDEX++) bemutató_ÉRTÉK(잠시참조[Loop_INDEX]);
        while (kijelző_DARAB > 0) {
            int objektum_hivatkozik = 표시대기[--kijelző_DARAB], terület_KÓD = halommemória_ÉRTÉK[objektum_hivatkozik];
            for (int Loop_INDEX = objektum_hivatkozik + 2; Loop_INDEX < objektum_hivatkozik + 힙폭[objektum_hivatkozik]; Loop_INDEX++) if (terület_KÓD == 3 || terület_KÓD == 4 || halommemória_hivatkozik[Loop_INDEX] != 0) bemutató_ÉRTÉK(halommemória_ÉRTÉK[Loop_INDEX]);
        }
        for (int csekk_pozíció = 1; csekk_pozíció < halommemória_megszüntet_pozíció; csekk_pozíció += 힙폭[csekk_pozíció]) if (힙표시[csekk_pozíció] == 0) halommemória_ÉRTÉK[csekk_pozíció] = 0;
        for (int csekk_pozíció = 1; csekk_pozíció < halommemória_megszüntet_pozíció; csekk_pozíció += 힙폭[csekk_pozíció]) if (halommemória_ÉRTÉK[csekk_pozíció] == 0) {
            while (csekk_pozíció + 힙폭[csekk_pozíció] < halommemória_megszüntet_pozíció && halommemória_ÉRTÉK[csekk_pozíció + 힙폭[csekk_pozíció]] == 0) { int Tovább_pozíció = csekk_pozíció + 힙폭[csekk_pozíció]; 힙폭[csekk_pozíció] += 힙폭[Tovább_pozíció]; 힙폭[Tovább_pozíció] = 0; }
            if (csekk_pozíció + 힙폭[csekk_pozíció] == halommemória_megszüntet_pozíció) { halommemória_megszüntet_pozíció = csekk_pozíció; break; }
        }
    }
    static int 새기억(int Altípus_ÉRTÉK, int hossz_ÉRTÉK) {
        if (hossz_ÉRTÉK < 0) { hiba_ÉRTÉK("NegativeArraySizeException"); return 0; }
        if (hossz_ÉRTÉK > halommemória_ÉRTÉK.length - 3) { hiba_ÉRTÉK("object heap exhausted"); return 0; }
        int 필요수 = hossz_ÉRTÉK + 2, objektum_hivatkozik = 0;
        if (필요수 <= halommemória_ÉRTÉK.length - halommemória_megszüntet_pozíció) { objektum_hivatkozik = halommemória_megszüntet_pozíció; halommemória_megszüntet_pozíció += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < halommemória_megszüntet_pozíció; 읽는자리 += 힙폭[읽는자리]) if (halommemória_ÉRTÉK[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { objektum_hivatkozik = 읽는자리; break; }
            if (objektum_hivatkozik != 0) {
                int 남은길이 = 힙폭[objektum_hivatkozik] - 필요수;
                if (남은길이 >= 2) { 힙폭[objektum_hivatkozik + 필요수] = 남은길이; halommemória_ÉRTÉK[objektum_hivatkozik + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= halommemória_ÉRTÉK.length - halommemória_megszüntet_pozíció) { objektum_hivatkozik = halommemória_megszüntet_pozíció; halommemória_megszüntet_pozíció += 필요수; }
        }
        if (objektum_hivatkozik == 0) { hiba_ÉRTÉK("object heap exhausted"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < 필요수; Loop_INDEX++) { halommemória_ÉRTÉK[objektum_hivatkozik + Loop_INDEX] = 0; halommemória_hivatkozik[objektum_hivatkozik + Loop_INDEX] = 0; 힙폭[objektum_hivatkozik + Loop_INDEX] = 0; }
        tömbelem[objektum_hivatkozik] = 0;
        힙폭[objektum_hivatkozik] = 필요수; halommemória_ÉRTÉK[objektum_hivatkozik] = Altípus_ÉRTÉK; halommemória_ÉRTÉK[objektum_hivatkozik + 1] = hossz_ÉRTÉK; véd_ÉRTÉK(objektum_hivatkozik); return objektum_hivatkozik;
    }
    static int kivétel_tanóra(String név_állandó) {
        if (자바도구.같음(név_állandó, "java/lang/Throwable")) return 1;
        if (자바도구.같음(név_állandó, "java/lang/Exception")) return 2;
        if (자바도구.같음(név_állandó, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(név_állandó, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(név_állandó, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(név_állandó, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(név_állandó, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(név_állandó, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(név_állandó, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(név_állandó, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(név_állandó, "java/io/IOException")) return 11;
        if (자바도구.같음(név_állandó, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(név_állandó, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(név_állandó, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(név_állandó, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int kivétel_állandó(int Név) {
        for (int Loop_INDEX = 1; Loop_INDEX <= 41; Loop_INDEX++) if (szó_SMS(Név, kivétel_név(Loop_INDEX))) return Loop_INDEX;
        return 0;
    }
    static String kivétel_név(int fiók_ÉRTÉK) {
        if (fiók_ÉRTÉK == 40) return "java/lang/InterruptedException";
        if (fiók_ÉRTÉK == 41) return "magyar/saját/대기중단예외";
        if (fiók_ÉRTÉK == 39) return "java/net/SocketException";
        if (fiók_ÉRTÉK == 20) return "magyar/saját/kivétel";
        if (fiók_ÉRTÉK == 21) return "magyar/saját/végrehajtás_kivétel";
        if (fiók_ÉRTÉK == 22) return "magyar/saját/I_O_kivétel";
        if (fiók_ÉRTÉK == 23) return "magyar/saját/várj_IDŐTÚLLÉPÉS_kivétel";
        if (fiók_ÉRTÉK == 24) return "magyar/saját/CÍM_KERES_kivétel";
        if (fiók_ÉRTÉK == 25) return "magyar/saját/파일없음예외";
        if (fiók_ÉRTÉK == 26) return "magyar/saját/kommunikáció_kivétel";
        if (fiók_ÉRTÉK == 27) return "magyar/saját/alaptalan_argumentum_kivétel";
        if (fiók_ÉRTÉK == 28) return "magyar/saját/szám_formáz_hiba";
        if (fiók_ÉRTÉK == 29) return "magyar/saját/범위예외";
        if (fiók_ÉRTÉK == 30) return "magyar/saját/배열범위예외";
        if (fiók_ÉRTÉK == 31) return "magyar/saját/문자열범위예외";
        if (fiók_ÉRTÉK == 32) return "magyar/saját/null_hivatkozik_kivétel";
        if (fiók_ÉRTÉK == 33) return "magyar/saját/산술예외";
        if (fiók_ÉRTÉK == 34) return "magyar/saját/Állapot_kivétel";
        if (fiók_ÉRTÉK == 35) return "magyar/saját/beír_Átjátszás_kivétel";
        if (fiók_ÉRTÉK == 36) return "magyar/saját/음수배열크기예외";
        if (fiók_ÉRTÉK == 37) return "magyar/saját/TÖMB_tár_hiba";
        if (fiók_ÉRTÉK == 38) return "magyar/saját/szál_Állapot_kivétel";
        if (fiók_ÉRTÉK == 1) return "java/lang/Throwable"; if (fiók_ÉRTÉK == 2) return "java/lang/Exception";
        if (fiók_ÉRTÉK == 3) return "java/lang/RuntimeException"; if (fiók_ÉRTÉK == 4) return "java/lang/ArithmeticException";
        if (fiók_ÉRTÉK == 5) return "java/lang/NullPointerException"; if (fiók_ÉRTÉK == 6) return "java/lang/IndexOutOfBoundsException";
        if (fiók_ÉRTÉK == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (fiók_ÉRTÉK == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (fiók_ÉRTÉK == 9) return "java/lang/IllegalArgumentException"; if (fiók_ÉRTÉK == 10) return "java/lang/NumberFormatException";
        if (fiók_ÉRTÉK == 11) return "java/io/IOException"; if (fiók_ÉRTÉK == 12) return "java/io/FileNotFoundException";
        if (fiók_ÉRTÉK == 17) return "java/lang/ArrayStoreException";
        if (fiók_ÉRTÉK == 18) return "java/net/UnknownHostException";
        if (fiók_ÉRTÉK == 19) return "java/net/SocketTimeoutException";
        if (fiók_ÉRTÉK == 16) return "java/lang/IllegalThreadStateException";
        if (fiók_ÉRTÉK == 13) return "java/lang/IllegalStateException"; if (fiók_ÉRTÉK == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int kivétel_szülő(int fiók_ÉRTÉK) {
        if (fiók_ÉRTÉK == 40) return 2;
        if (fiók_ÉRTÉK == 41) return 40;
        if (fiók_ÉRTÉK == 39) return 11;
        if (fiók_ÉRTÉK == 1) return 0;
        if (fiók_ÉRTÉK == 2) return 1;
        if (fiók_ÉRTÉK == 3) return 2;
        if (fiók_ÉRTÉK == 4) return 3;
        if (fiók_ÉRTÉK == 5) return 3;
        if (fiók_ÉRTÉK == 6) return 3;
        if (fiók_ÉRTÉK == 7) return 6;
        if (fiók_ÉRTÉK == 8) return 6;
        if (fiók_ÉRTÉK == 9) return 3;
        if (fiók_ÉRTÉK == 10) return 9;
        if (fiók_ÉRTÉK == 11) return 2;
        if (fiók_ÉRTÉK == 12) return 11;
        if (fiók_ÉRTÉK == 13) return 3;
        if (fiók_ÉRTÉK == 14) return 3;
        if (fiók_ÉRTÉK == 15) return 3;
        if (fiók_ÉRTÉK == 16) return 9;
        if (fiók_ÉRTÉK == 17) return 3;
        if (fiók_ÉRTÉK == 18) return 11;
        if (fiók_ÉRTÉK == 19) return 11;
        if (fiók_ÉRTÉK == 20) return 2;
        if (fiók_ÉRTÉK == 21) return 3;
        if (fiók_ÉRTÉK == 22) return 11;
        if (fiók_ÉRTÉK == 23) return 22;
        if (fiók_ÉRTÉK == 24) return 22;
        if (fiók_ÉRTÉK == 25) return 22;
        if (fiók_ÉRTÉK == 26) return 22;
        if (fiók_ÉRTÉK == 27) return 9;
        if (fiók_ÉRTÉK == 28) return 27;
        if (fiók_ÉRTÉK == 29) return 6;
        if (fiók_ÉRTÉK == 30) return 29;
        if (fiók_ÉRTÉK == 31) return 29;
        if (fiók_ÉRTÉK == 32) return 5;
        if (fiók_ÉRTÉK == 33) return 4;
        if (fiók_ÉRTÉK == 34) return 13;
        if (fiók_ÉRTÉK == 35) return 14;
        if (fiók_ÉRTÉK == 36) return 15;
        if (fiók_ÉRTÉK == 37) return 17;
        if (fiók_ÉRTÉK == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int tényleges_érték, int 요구값) {
        for (int 깊이 = 0; tényleges_érték != 0 && 깊이 < 16; 깊이++, tényleges_érték = kivétel_szülő(tényleges_érték))
            if (tényleges_érték == 요구값) return true;
        return false;
    }
    static void 예외던짐(int fiók_ÉRTÉK, String fontos_fájl_hivatkozik) {
        int objektum_hivatkozik = 새기억(9, 2); if (HIBA) return;
        halommemória_ÉRTÉK[objektum_hivatkozik + 2] = fiók_ÉRTÉK; halommemória_ÉRTÉK[objektum_hivatkozik + 3] = gazda_karakter(fontos_fájl_hivatkozik); halommemória_hivatkozik[objektum_hivatkozik + 3] = 1;
        던진객체 = objektum_hivatkozik; HIBA = true;
    }
    static boolean 맞는객체(int objektum_hivatkozik, int Név) {
        if (objektum_hivatkozik == 0) return true;
        if (!informatikai_részleg_érvényes_objektum(objektum_hivatkozik)) return false;
        int terület_KÓD = halommemória_ÉRTÉK[objektum_hivatkozik];
        if (szó_SMS(Név, "java/lang/Object")) return true;
        if (terület_KÓD >= 32) return 종포함(terület_KÓD - 32, Név);
        if (terület_KÓD == 9) { int cél_CÍM = kivétel_állandó(Név); return cél_CÍM != 0 && 예외포함(halommemória_ÉRTÉK[objektum_hivatkozik + 2], cél_CÍM); }
        if (terület_KÓD == 1) return szó_SMS(Név, "java/lang/String") || szó_SMS(Név, "java/lang/CharSequence");
        if (terület_KÓD == 4) return szó_SMS(Név, "java/lang/StringBuilder") || szó_SMS(Név, "java/lang/CharSequence");
        if (terület_KÓD == 10) return szó_SMS(Név, "java/util/ArrayList") || szó_SMS(Név, "java/util/List");
        if (terület_KÓD == 11) return szó_SMS(Név, "java/util/HashMap") || szó_SMS(Név, "java/util/Map");
        if (terület_KÓD == 12) return szó_SMS(Név, "java/lang/Integer") || szó_SMS(Név, "java/lang/Number");
        if (terület_KÓD >= 24 && terület_KÓD <= 28 && halommemória_ÉRTÉK[objektum_hivatkozik + 13] != 0) return 한국어화면종(Név) == terület_KÓD || szó_SMS(Név, "magyar/saját/화면구성요소");
        if (terület_KÓD >= 24 && terület_KÓD <= 28) return (한국어화면종(Név) == 0 && 화면종(Név) == terület_KÓD) || szó_SMS(Név, "java/awt/Component") || szó_SMS(Név, "java/awt/Container") || szó_SMS(Név, "javax/swing/JComponent");
        if (terület_KÓD == 29) return szó_SMS(Név, halommemória_ÉRTÉK[objektum_hivatkozik + 3] != 0 ? "magyar/saját/Action_alapelv" : "java/awt/event/ActionEvent");
        if (terület_KÓD == 30) return szó_SMS(Név, "java/awt/FlowLayout") || szó_SMS(Név, "java/awt/LayoutManager");
        if (terület_KÓD == 17) return szó_SMS(Név, "java/net/Socket");
        if (terület_KÓD == 18) return szó_SMS(Név, "java/net/ServerSocket");
        if (terület_KÓD == 19) return szó_SMS(Név, halommemória_ÉRTÉK[objektum_hivatkozik + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (terület_KÓD == 14) return szó_SMS(Név, "java/net/InetAddress");
        if (terület_KÓD == 15) return szó_SMS(Név, "java/net/DatagramSocket");
        if (terület_KÓD == 16) return szó_SMS(Név, "java/net/DatagramPacket");
        if (terület_KÓD == 13) return szó_SMS(Név, halommemória_ÉRTÉK[objektum_hivatkozik + 3] != 0 ? "magyar/saját/dolgozó" : "java/lang/Thread");
        if (terület_KÓD == 2) return szó_SMS(Név, "[I"); if (terület_KÓD == 20) return szó_SMS(Név, "[B"); if (terület_KÓD == 21) return szó_SMS(Név, "[Z");
        if (terület_KÓD == 22) return szó_SMS(Név, "[C"); if (terület_KÓD == 23) return szó_SMS(Név, "[S");
        if (terület_KÓD != 3) return false;
        if (szó_SMS(Név, "[Ljava/lang/Object;")) return true;
        int komponens = tömbelem[objektum_hivatkozik];
        if (komponens == -1) return szó_SMS(Név, "[Ljava/lang/String;") || szó_SMS(Név, "[Ljava/lang/CharSequence;");
        if (komponens == 0) return false;
        if (배열종비교(komponens, Név)) return true;
        if ((szó_SMS(komponens, "java/lang/String") || szó_SMS(komponens, "java/lang/StringBuilder")) && szó_SMS(Név, "[Ljava/lang/CharSequence;")) return true;
        for (int Loop_INDEX = 0; Loop_INDEX < tanóra_Definíció_DARAB; Loop_INDEX++) if (같은말(tanóra_Definíció_név[Loop_INDEX], komponens)) {
            for (int kódpont = Loop_INDEX, 중첩깊이 = 0; kódpont >= 0 && 중첩깊이 < 16; 중첩깊이++, kódpont = szülő_tanóra(kódpont)) {
                if (배열종비교(tanóra_Definíció_szülő[kódpont], Név)) return true;
                for (int belső_pozíció = 0; belső_pozíció < tanóra_csatoló_DARAB[kódpont]; belső_pozíció++) if (배열종비교(tanóra_csatoló[kódpont * 16 + belső_pozíció], Név)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int név_állandó, int 형식참조) {
        int csekk_pozíció = 상가[형식참조], bejegyzés_DARAB = állandó_MPERC_ÉRTÉK[형식참조];
        if (név_állandó == 0 || bejegyzés_DARAB < 4 || Fájl[csekk_pozíció] != '[' || Fájl[csekk_pozíció + 1] != 'L' || Fájl[csekk_pozíció + bejegyzés_DARAB - 1] != ';' || állandó_MPERC_ÉRTÉK[név_állandó] != bejegyzés_DARAB - 3) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < bejegyzés_DARAB - 3; Loop_INDEX++) if (Fájl[상가[név_állandó] + Loop_INDEX] != Fájl[csekk_pozíció + 2 + Loop_INDEX]) return false;
        return true;
    }
    static void leíró_kivétel() {
        if (던진객체 == 0) return;
        HIBA = false;
        while (doboz_INDEX >= aktuális_szál * 32) {
            int Fájl_INDEX = doboz_metódus[doboz_INDEX], 읽는자리 = 틀명령[doboz_INDEX];
            for (int Loop_INDEX = 0; Loop_INDEX < 잡기수; Loop_INDEX++) if (잡기함수[Loop_INDEX] == Fájl_INDEX && 읽는자리 >= 잡기시작[Loop_INDEX] && 읽는자리 < 잡기끝[Loop_INDEX]
                && (잡기종[Loop_INDEX] == 0 || 맞는객체(던진객체, 잡기종[Loop_INDEX]))) {
                doboz_pozíció[doboz_INDEX] = 잡기위치[Loop_INDEX]; doboz_Sor[doboz_INDEX] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (inicializál_doboz[doboz_INDEX] != 0) tanóra_Definíció_Állapot[inicializál_doboz[doboz_INDEX] - 1] = 3;
            if (doboz_lezár[doboz_INDEX] != 0) { kiad_lezár(doboz_lezár[doboz_INDEX]); doboz_lezár[doboz_INDEX] = 0; }
            doboz_INDEX--;
        }
        felhasználó.Írás("Uncaught ");
        if (halommemória_ÉRTÉK[던진객체] == 9) { felhasználó.Írás(kivétel_név(halommemória_ÉRTÉK[던진객체 + 2])); felhasználó.Írás(": "); ír_SMS(halommemória_ÉRTÉK[던진객체 + 3]); }
        else felhasználó.Írás("user exception");
        felhasználó.ír_karakter_ÉRTÉK(10); 던진객체 = 0; HIBA = true;
    }
    // 이 JVM의 operandus_Sor 항목은 aktuális_cikk category-1(int/reference)만 허용한다.
    static void 스택명령(int parancs_KÓD) {
        int 첫값 = 빼기(0), 첫형식 = visszaküld_beír;
        if (parancs_KÓD == 87) return;
        if (parancs_KÓD == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int bájt_adat = 빼기(0), MPERC_formáz = visszaküld_beír;
        if (parancs_KÓD == 88) return;
        if (parancs_KÓD == 90) { 넣기(첫값, 첫형식); 넣기(bájt_adat, MPERC_formáz); 넣기(첫값, 첫형식); return; }
        if (parancs_KÓD == 92) { 넣기(bájt_adat, MPERC_formáz); 넣기(첫값, 첫형식); 넣기(bájt_adat, MPERC_formáz); 넣기(첫값, 첫형식); return; }
        if (parancs_KÓD == 95) { 넣기(첫값, 첫형식); 넣기(bájt_adat, MPERC_formáz); return; }
        int kódpont = 빼기(0), 셋째형식 = visszaküld_beír;
        if (parancs_KÓD == 91) { 넣기(첫값, 첫형식); 넣기(kódpont, 셋째형식); 넣기(bájt_adat, MPERC_formáz); 넣기(첫값, 첫형식); return; }
        if (parancs_KÓD == 93) { 넣기(bájt_adat, MPERC_formáz); 넣기(첫값, 첫형식); 넣기(kódpont, 셋째형식); 넣기(bájt_adat, MPERC_formáz); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = visszaküld_beír;
        넣기(bájt_adat, MPERC_formáz); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(kódpont, 셋째형식); 넣기(bájt_adat, MPERC_formáz); 넣기(첫값, 첫형식);
    }
    static void 새객체(int név_állandó, int 시작점) {
        int terület_KÓD = 0, érvényes_hossz = 0, kivétel_hivatkozik = kivétel_állandó(név_állandó);
        if (szó_SMS(név_állandó, "java/lang/StringBuilder")) { terület_KÓD = 4; érvényes_hossz = 1; }
        if (szó_SMS(név_állandó, "java/io/FileInputStream")) { terület_KÓD = 5; érvényes_hossz = 2; }
        if (szó_SMS(név_állandó, "java/io/FileOutputStream")) { terület_KÓD = 6; érvényes_hossz = 2; }
        if (kivétel_hivatkozik != 0) { terület_KÓD = 9; érvényes_hossz = 2; }
        if (szó_SMS(név_állandó, "java/util/ArrayList")) { terület_KÓD = 10; érvényes_hossz = 2; }
        if (szó_SMS(név_állandó, "java/util/HashMap")) { terület_KÓD = 11; érvényes_hossz = 2; }
        if (szó_SMS(név_állandó, "java/lang/Integer")) { terület_KÓD = 12; érvényes_hossz = 1; }
        if (szó_SMS(név_állandó, "java/net/Socket")) { terület_KÓD = 17; érvényes_hossz = 5; }
        if (szó_SMS(név_állandó, "java/net/ServerSocket")) { terület_KÓD = 18; érvényes_hossz = 5; }
        if (szó_SMS(név_állandó, "java/net/DatagramSocket")) { terület_KÓD = 15; érvényes_hossz = 3; }
        if (szó_SMS(név_állandó, "java/net/DatagramPacket")) { terület_KÓD = 16; érvényes_hossz = 4; }
        if (szó_SMS(név_állandó, "java/lang/Thread") || szó_SMS(név_állandó, "magyar/saját/dolgozó")) { terület_KÓD = 13; érvényes_hossz = 2; }
        if (szó_SMS(név_állandó, "java/lang/Object")) { terület_KÓD = 8; }
        if (terület_KÓD == 0 && 화면종(név_állandó) != 0) { terület_KÓD = 화면종(név_állandó); érvényes_hossz = 12; }
        if (terület_KÓD == 0) {
            int kódpont = keres_tanóra_Definíció(név_állandó); if (kódpont < 0 || HIBA || !inicializál(kódpont, 시작점)) return;
            terület_KÓD = 32 + kódpont; érvényes_hossz = tanóra_tárolóhely_DARAB[kódpont];
        }
        int objektum_hivatkozik = kioszt_tár(terület_KÓD, érvényes_hossz); if (HIBA) return;
        if (terület_KÓD == 13 && szó_SMS(név_állandó, "magyar/saját/dolgozó")) halommemória_ÉRTÉK[objektum_hivatkozik + 3] = 1;
        if (terület_KÓD >= 24 && terület_KÓD <= 28 && 한국어화면종(név_állandó) != 0) halommemória_ÉRTÉK[objektum_hivatkozik + 13] = 1;
        if (terület_KÓD == 5 || terület_KÓD == 6 || terület_KÓD == 15 || terület_KÓD == 17 || terület_KÓD == 18) halommemória_ÉRTÉK[objektum_hivatkozik + 2] = -1;
        if (terület_KÓD == 9) halommemória_ÉRTÉK[objektum_hivatkozik + 2] = kivétel_hivatkozik;
        넣기(objektum_hivatkozik, 2);
    }
    static boolean 값같음(int 첫값, int bájt_adat) {
        if (첫값 == bájt_adat) return true;
        if (첫값 == 0 || bájt_adat == 0 || 첫값 < 0 || bájt_adat < 0 || 첫값 >= halommemória_megszüntet_pozíció || bájt_adat >= halommemória_megszüntet_pozíció) return false;
        if (halommemória_ÉRTÉK[첫값] == 1 && halommemória_ÉRTÉK[bájt_adat] == 1) return 글같음(첫값, bájt_adat, false);
        return halommemória_ÉRTÉK[첫값] == 12 && halommemória_ÉRTÉK[bájt_adat] == 12 && halommemória_ÉRTÉK[첫값 + 2] == halommemória_ÉRTÉK[bájt_adat + 2];
    }
    static int 글조각(int objektum_hivatkozik, int START_pozíció, int megszüntet_pozíció) {
        if (!objektum_ÉRTÉK(objektum_hivatkozik, 1)) return 0;
        if (START_pozíció < 0 || megszüntet_pozíció < START_pozíció || megszüntet_pozíció > halommemória_ÉRTÉK[objektum_hivatkozik + 1]) { hiba_ÉRTÉK("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = kioszt_tár(1, megszüntet_pozíció - START_pozíció); if (HIBA) return 0;
        for (int Loop_INDEX = START_pozíció; Loop_INDEX < megszüntet_pozíció; Loop_INDEX++) halommemória_ÉRTÉK[반환값 + 2 + Loop_INDEX - START_pozíció] = halommemória_ÉRTÉK[objektum_hivatkozik + 2 + Loop_INDEX];
        return 반환값;
    }
    static int Csatlakozás_SMS(int 첫값, int bájt_adat) {
        if (!objektum_ÉRTÉK(첫값, 1) || !objektum_ÉRTÉK(bájt_adat, 1)) return 0;
        int bejegyzés_DARAB = halommemória_ÉRTÉK[첫값 + 1], metódus_INDEX = halommemória_ÉRTÉK[bájt_adat + 1], 반환값 = kioszt_tár(1, bejegyzés_DARAB + metódus_INDEX); if (HIBA) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < bejegyzés_DARAB; Loop_INDEX++) halommemória_ÉRTÉK[반환값 + 2 + Loop_INDEX] = halommemória_ÉRTÉK[첫값 + 2 + Loop_INDEX];
        for (int Loop_INDEX = 0; Loop_INDEX < metódus_INDEX; Loop_INDEX++) halommemória_ÉRTÉK[반환값 + 2 + bejegyzés_DARAB + Loop_INDEX] = halommemória_ÉRTÉK[bájt_adat + 2 + Loop_INDEX];
        return 반환값;
    }
    static boolean 기본호출(int tulajdonos, int név_állandó, int 서술상수, int parancs_KÓD) {
        if (szó_SMS(tulajdonos, "magyar/saját/실행인수") && parancs_KÓD == 184) {
            if (szó_SMS(név_állandó, "cikk_DARAB") && szó_SMS(서술상수, "()I")) { 넣기(felhasználó.인수개수() - 1, 1); return true; }
            if (szó_SMS(név_állandó, "Szöveg") && szó_SMS(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= felhasználó.인수개수() - 1) 예외던짐(29, "végrehajt_parancs Argumentumok 범위를 벗어났습니다");
                else 넣기(gazda_karakter(felhasználó.Argumentumok(순번 + 1)), 2);
                return true;
            }
            hiba_ÉRTÉK("지원하지 않는 magyar végrehajt_parancs Argumentumok 호출"); return true;
        }
        if (szó_SMS(tulajdonos, "magyar/saját/dolgozó")) { folyamat_szál(név_állandó, 서술상수, parancs_KÓD, true); return true; }
        if (한국어화면소유(tulajdonos)) { 한국어화면호출(tulajdonos, név_állandó, 서술상수, parancs_KÓD); return true; }
        if (화면소유(tulajdonos)) { 화면호출(tulajdonos, név_állandó, 서술상수, parancs_KÓD); return true; }
        if (szó_SMS(tulajdonos, "java/net/Socket") || szó_SMS(tulajdonos, "java/net/ServerSocket") || szó_SMS(tulajdonos, "java/io/InputStream") || szó_SMS(tulajdonos, "java/io/OutputStream")) { 흐름호출(tulajdonos, név_állandó, 서술상수, parancs_KÓD); return true; }
        if (szó_SMS(tulajdonos, "magyar/saját/kernel_ÉRTÉK") && parancs_KÓD == 184) {
            if (szó_SMS(név_állandó, "화면너비") && szó_SMS(서술상수, "()I")) { 넣기(felhasználó.화면너비(), 1); return true; }
            if (szó_SMS(név_állandó, "화면높이") && szó_SMS(서술상수, "()I")) { 넣기(felhasználó.화면높이(), 1); return true; }
            if (szó_SMS(név_állandó, "밀리초") && szó_SMS(서술상수, "()I")) { 넣기(felhasználó.밀리초(), 1); return true; }
            if (szó_SMS(név_állandó, "그림대기") && szó_SMS(서술상수, "()I")) { 넣기(felhasználó.그림대기(), 1); return true; }
            if (szó_SMS(név_állandó, "téglalap") && szó_SMS(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), Y_koordináta = 빼기(1), x_koordináta = 빼기(1); 넣기(felhasználó.téglalap(x_koordináta, Y_koordináta, 너비, 높이, 색상), 1); return true; }
        }
        if (szó_SMS(tulajdonos, "java/net/InetAddress") || szó_SMS(tulajdonos, "java/net/DatagramPacket") || szó_SMS(tulajdonos, "java/net/DatagramSocket")) { 통신호출(tulajdonos, név_állandó, 서술상수, parancs_KÓD); return true; }
        if (szó_SMS(tulajdonos, "java/lang/Thread")) { 가닥호출(név_állandó, 서술상수, parancs_KÓD); return true; }
        if (szó_SMS(tulajdonos, "java/lang/Object")) {
            if (szó_SMS(név_állandó, "<init>") && szó_SMS(서술상수, "()V") && parancs_KÓD == 183) { informatikai_részleg_érvényes_objektum(빼기(2)); return true; }
            if (szó_SMS(név_állandó, "equals") && szó_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int bájt_adat = 빼기(2), 첫값 = 빼기(2); if (informatikai_részleg_érvényes_objektum(첫값)) 넣기(첫값 == bájt_adat ? 1 : 0, 1); return true; }
        }
        if (kivétel_állandó(tulajdonos) != 0) {
            if (szó_SMS(név_állandó, "<init>") && parancs_KÓD == 183 && (szó_SMS(서술상수, "()V") || szó_SMS(서술상수, "(Ljava/lang/String;)V"))) {
                int kér = szó_SMS(서술상수, "()V") ? 0 : 빼기(2), objektum_hivatkozik = 빼기(2);
                if (objektum_ÉRTÉK(objektum_hivatkozik, 9)) { halommemória_ÉRTÉK[objektum_hivatkozik + 3] = kér; halommemória_hivatkozik[objektum_hivatkozik + 3] = 1; } return true;
            }
            if ((szó_SMS(név_állandó, "getMessage") || szó_SMS(név_állandó, "설명")) && szó_SMS(서술상수, "()Ljava/lang/String;")) { int objektum_hivatkozik = 빼기(2); if (objektum_ÉRTÉK(objektum_hivatkozik, 9)) 넣기(halommemória_ÉRTÉK[objektum_hivatkozik + 3], 2); return true; }
        }
        if (szó_SMS(tulajdonos, "java/lang/String")) {
            if (parancs_KÓD == 182 && szó_SMS(név_állandó, "getBytes") && (szó_SMS(서술상수, "()[B") || szó_SMS(서술상수, "(Ljava/lang/String;)[B"))) {
                int kódolás_név = szó_SMS(서술상수, "()[B") ? 0 : 빼기(2), objektum_hivatkozik = 빼기(2);
                if (!objektum_ÉRTÉK(objektum_hivatkozik, 1)) return true;
                if (kódolás_név != 0 && !글같음(kódolás_név, gazda_karakter("UTF-8"), false) && !글같음(kódolás_név, gazda_karakter("UTF8"), false) && !글같음(kódolás_név, gazda_karakter("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int bejegyzés_DARAB = halommemória_ÉRTÉK[objektum_hivatkozik + 1], 반환값 = kioszt_tár(20, bejegyzés_DARAB * 3), 사용수 = 0; if (HIBA) return true;
                for (int belső_pozíció = 0; belső_pozíció < bejegyzés_DARAB; belső_pozíció++) {
                    int kódpont = halommemória_ÉRTÉK[objektum_hivatkozik + 2 + belső_pozíció];
                    if (kódpont >= 0xd800 && kódpont <= 0xdbff && belső_pozíció + 1 < bejegyzés_DARAB && halommemória_ÉRTÉK[objektum_hivatkozik + 3 + belső_pozíció] >= 0xdc00 && halommemória_ÉRTÉK[objektum_hivatkozik + 3 + belső_pozíció] <= 0xdfff) kódpont = 0x10000 + ((kódpont - 0xd800) << 10) + halommemória_ÉRTÉK[objektum_hivatkozik + 2 + ++belső_pozíció] - 0xdc00;
                    else if (kódpont >= 0xd800 && kódpont <= 0xdfff) kódpont = '?';
                    if (kódpont < 128) halommemória_ÉRTÉK[반환값 + 2 + 사용수++] = kódpont;
                    else { int bájt_DARAB = kódpont < 2048 ? 2 : kódpont < 65536 ? 3 : 4; halommemória_ÉRTÉK[반환값 + 2 + 사용수++] = (byte)((bájt_DARAB == 2 ? 192 : bájt_DARAB == 3 ? 224 : 240) | kódpont >> (6 * (bájt_DARAB - 1))); for (int Összehasonlítás_pozíció = bájt_DARAB - 1; Összehasonlítás_pozíció > 0; Összehasonlítás_pozíció--) halommemória_ÉRTÉK[반환값 + 2 + 사용수++] = (byte)(128 | kódpont >> (6 * (Összehasonlítás_pozíció - 1)) & 63); }
                }
                halommemória_ÉRTÉK[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (parancs_KÓD == 184 && szó_SMS(név_állandó, "valueOf") && szó_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(számjegy_karakter(빼기(1)), 2); return true; }
            if (parancs_KÓD != 182) return false;
            if (szó_SMS(név_állandó, "equals") && szó_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int bájt_adat = 빼기(2), 첫값 = 빼기(2); if (objektum_ÉRTÉK(첫값, 1)) 넣기(글같음(첫값, bájt_adat, false) ? 1 : 0, 1); return true; }
            if (szó_SMS(név_állandó, "isEmpty") && szó_SMS(서술상수, "()Z")) { int 첫값 = 빼기(2); if (objektum_ÉRTÉK(첫값, 1)) 넣기(halommemória_ÉRTÉK[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (szó_SMS(név_állandó, "substring") && (szó_SMS(서술상수, "(I)Ljava/lang/String;") || szó_SMS(서술상수, "(II)Ljava/lang/String;"))) {
                boolean MPERC_ÉRTÉK = szó_SMS(서술상수, "(II)Ljava/lang/String;"); int megszüntet_pozíció = MPERC_ÉRTÉK ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (objektum_ÉRTÉK(첫값, 1)) 넣기(글조각(첫값, 시작점, MPERC_ÉRTÉK ? megszüntet_pozíció : halommemória_ÉRTÉK[첫값 + 1]), 2); return true;
            }
            if (szó_SMS(név_állandó, "concat") && szó_SMS(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int bájt_adat = 빼기(2), 첫값 = 빼기(2); 넣기(Csatlakozás_SMS(첫값, bájt_adat), 2); return true; }
            if (szó_SMS(név_állandó, "hashCode") && szó_SMS(서술상수, "()I")) { int 첫값 = 빼기(2), kivonat_ÉRTÉK = 0; if (objektum_ÉRTÉK(첫값, 1)) { for (int Loop_INDEX = 0; Loop_INDEX < halommemória_ÉRTÉK[첫값 + 1]; Loop_INDEX++) kivonat_ÉRTÉK = kivonat_ÉRTÉK * 31 + halommemória_ÉRTÉK[첫값 + 2 + Loop_INDEX]; 넣기(kivonat_ÉRTÉK, 1); } return true; }
            if (szó_SMS(név_állandó, "toString") && szó_SMS(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (objektum_ÉRTÉK(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (szó_SMS(tulajdonos, "java/lang/Integer")) {
            if (parancs_KÓD == 184 && szó_SMS(név_állandó, "valueOf") && szó_SMS(서술상수, "(I)Ljava/lang/Integer;")) { int adat_ÉRTÉK = 빼기(1), objektum_hivatkozik = adat_ÉRTÉK >= -128 && adat_ÉRTÉK <= 127 ? tár_egész_szám[adat_ÉRTÉK + 128] : 0; if (objektum_hivatkozik == 0) { objektum_hivatkozik = kioszt_tár(12, 1); if (!HIBA) { halommemória_ÉRTÉK[objektum_hivatkozik + 2] = adat_ÉRTÉK; if (adat_ÉRTÉK >= -128 && adat_ÉRTÉK <= 127) tár_egész_szám[adat_ÉRTÉK + 128] = objektum_hivatkozik; } } 넣기(objektum_hivatkozik, 2); return true; }
            if (parancs_KÓD == 183 && szó_SMS(név_állandó, "<init>") && szó_SMS(서술상수, "(I)V")) { int adat_ÉRTÉK = 빼기(1), objektum_hivatkozik = 빼기(2); if (objektum_ÉRTÉK(objektum_hivatkozik, 12)) halommemória_ÉRTÉK[objektum_hivatkozik + 2] = adat_ÉRTÉK; return true; }
            if (parancs_KÓD == 182 && szó_SMS(név_állandó, "intValue") && szó_SMS(서술상수, "()I")) { int objektum_hivatkozik = 빼기(2); if (objektum_ÉRTÉK(objektum_hivatkozik, 12)) 넣기(halommemória_ÉRTÉK[objektum_hivatkozik + 2], 1); return true; }
            if (parancs_KÓD == 184 && szó_SMS(név_állandó, "toString") && szó_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(számjegy_karakter(빼기(1)), 2); return true; }
        }
        if (szó_SMS(tulajdonos, "java/lang/Math") && parancs_KÓD == 184) {
            if (szó_SMS(név_állandó, "abs") && szó_SMS(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((szó_SMS(név_állandó, "min") || szó_SMS(név_állandó, "max")) && szó_SMS(서술상수, "(II)I")) { int bájt_adat = 빼기(1), 첫값 = 빼기(1); 넣기(szó_SMS(név_állandó, "min") ? (첫값 < bájt_adat ? 첫값 : bájt_adat) : (첫값 > bájt_adat ? 첫값 : bájt_adat), 1); return true; }
        }
        if (szó_SMS(tulajdonos, "java/lang/System") && parancs_KÓD == 184) {
            if (szó_SMS(név_állandó, "gc") && szó_SMS(서술상수, "()V")) { 수거(); return true; }
            if (szó_SMS(név_állandó, "arraycopy") && szó_SMS(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int bejegyzés_DARAB = 빼기(1), cél_ÉRTÉK_INDEX = 빼기(1), bájt_adat = 빼기(2), START_pozíció = 빼기(1), 첫값 = 빼기(2);
                if (informatikai_részleg_érvényes_objektum(첫값) && informatikai_részleg_érvényes_objektum(bájt_adat)) {
                    int terület_KÓD = halommemória_ÉRTÉK[첫값];
                    if (halommemória_ÉRTÉK[bájt_adat] != terület_KÓD || (terület_KÓD != 2 && terület_KÓD != 3 && (terület_KÓD < 20 || terület_KÓD > 23))) hiba_ÉRTÉK("arraycopy type mismatch");
                    else if (bejegyzés_DARAB < 0 || START_pozíció < 0 || cél_ÉRTÉK_INDEX < 0 || START_pozíció > halommemória_ÉRTÉK[첫값 + 1] - bejegyzés_DARAB || cél_ÉRTÉK_INDEX > halommemória_ÉRTÉK[bájt_adat + 1] - bejegyzés_DARAB) hiba_ÉRTÉK("ArrayIndexOutOfBoundsException");
                    else if (첫값 == bájt_adat && cél_ÉRTÉK_INDEX > START_pozíció) { for (int Loop_INDEX = bejegyzés_DARAB - 1; Loop_INDEX >= 0; Loop_INDEX--) halommemória_ÉRTÉK[bájt_adat + 2 + cél_ÉRTÉK_INDEX + Loop_INDEX] = halommemória_ÉRTÉK[첫값 + 2 + START_pozíció + Loop_INDEX]; }
                    else { for (int Loop_INDEX = 0; Loop_INDEX < bejegyzés_DARAB && !HIBA; Loop_INDEX++) { int adat_ÉRTÉK = halommemória_ÉRTÉK[첫값 + 2 + START_pozíció + Loop_INDEX]; if (terület_KÓD != 3 || 배열저장가능(bájt_adat, adat_ÉRTÉK)) halommemória_ÉRTÉK[bájt_adat + 2 + cél_ÉRTÉK_INDEX + Loop_INDEX] = adat_ÉRTÉK; } }
                }
                return true;
            }
        }
        if (szó_SMS(tulajdonos, "java/util/ArrayList") || szó_SMS(tulajdonos, "java/util/List") || szó_SMS(tulajdonos, "java/util/HashMap") || szó_SMS(tulajdonos, "java/util/Map")) {
            모음호출(tulajdonos, név_állandó, 서술상수, parancs_KÓD); return true;
        }
        return false;
    }
    static void 모음늘리기(int objektum_hivatkozik, int 필요수) {
        int Előző_ÉRTÉK = halommemória_ÉRTÉK[objektum_hivatkozik + 2], kapacitás_adat = Előző_ÉRTÉK == 0 ? 0 : halommemória_ÉRTÉK[Előző_ÉRTÉK + 1];
        if (kapacitás_adat >= 필요수) return;
        int Tovább_pozíció = kapacitás_adat < 8 ? 8 : kapacitás_adat * 2; if (Tovább_pozíció < 필요수) Tovább_pozíció = 필요수;
        int adat_TÖMB = kioszt_tár(3, Tovább_pozíció); if (HIBA) return;
        for (int Loop_INDEX = 0; Loop_INDEX < kapacitás_adat; Loop_INDEX++) halommemória_ÉRTÉK[adat_TÖMB + 2 + Loop_INDEX] = halommemória_ÉRTÉK[Előző_ÉRTÉK + 2 + Loop_INDEX];
        halommemória_ÉRTÉK[objektum_hivatkozik + 2] = adat_TÖMB; halommemória_hivatkozik[objektum_hivatkozik + 2] = 1;
    }
    static void 모음호출(int tulajdonos, int név_állandó, int 서술상수, int parancs_KÓD) {
        boolean 대응참조 = szó_SMS(tulajdonos, "java/util/HashMap") || szó_SMS(tulajdonos, "java/util/Map"); int terület_KÓD = 대응참조 ? 11 : 10;
        if (szó_SMS(név_állandó, "<init>") && parancs_KÓD == 183 && szó_SMS(서술상수, "()V")) { int objektum_hivatkozik = 빼기(2); if (objektum_ÉRTÉK(objektum_hivatkozik, terület_KÓD)) 모음늘리기(objektum_hivatkozik, 8); return; }
        if (parancs_KÓD != 182 && parancs_KÓD != 185) { hiba_ÉRTÉK("invalid collection invocation"); return; }
        if (szó_SMS(név_állandó, "size") && szó_SMS(서술상수, "()I") || szó_SMS(név_állandó, "isEmpty") && szó_SMS(서술상수, "()Z")) {
            int objektum_hivatkozik = 빼기(2); if (objektum_ÉRTÉK(objektum_hivatkozik, terület_KÓD)) 넣기(szó_SMS(név_állandó, "size") ? halommemória_ÉRTÉK[objektum_hivatkozik + 3] : halommemória_ÉRTÉK[objektum_hivatkozik + 3] == 0 ? 1 : 0, 1); return;
        }
        if (szó_SMS(név_állandó, "clear") && szó_SMS(서술상수, "()V")) { int objektum_hivatkozik = 빼기(2); if (objektum_ÉRTÉK(objektum_hivatkozik, terület_KÓD)) { int adat_TÖMB = halommemória_ÉRTÉK[objektum_hivatkozik + 2]; for (int Loop_INDEX = 0; Loop_INDEX < halommemória_ÉRTÉK[adat_TÖMB + 1]; Loop_INDEX++) halommemória_ÉRTÉK[adat_TÖMB + 2 + Loop_INDEX] = 0; halommemória_ÉRTÉK[objektum_hivatkozik + 3] = 0; } return; }
        if (!대응참조 && szó_SMS(név_állandó, "add") && szó_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            int adat_ÉRTÉK = 빼기(2), objektum_hivatkozik = 빼기(2); if (!objektum_ÉRTÉK(objektum_hivatkozik, 10)) return;
            int bejegyzés_DARAB = halommemória_ÉRTÉK[objektum_hivatkozik + 3]; 모음늘리기(objektum_hivatkozik, bejegyzés_DARAB + 1); if (!HIBA) { halommemória_ÉRTÉK[halommemória_ÉRTÉK[objektum_hivatkozik + 2] + 2 + bejegyzés_DARAB] = adat_ÉRTÉK; halommemória_ÉRTÉK[objektum_hivatkozik + 3] = bejegyzés_DARAB + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (szó_SMS(név_állandó, "get") || szó_SMS(név_állandó, "remove")) && szó_SMS(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && szó_SMS(név_állandó, "set") && szó_SMS(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean informatikai_részleg_Hozzárendelt = szó_SMS(név_állandó, "set"); int adat_ÉRTÉK = informatikai_részleg_Hozzárendelt ? 빼기(2) : 0, bejegyzés_pozíció = 빼기(1), objektum_hivatkozik = 빼기(2);
            if (!objektum_ÉRTÉK(objektum_hivatkozik, 10)) return;
            int bejegyzés_DARAB = halommemória_ÉRTÉK[objektum_hivatkozik + 3], adat_TÖMB = halommemória_ÉRTÉK[objektum_hivatkozik + 2];
            if (bejegyzés_pozíció < 0 || bejegyzés_pozíció >= bejegyzés_DARAB) { 예외던짐(6, "list index"); return; }
            int Előző_ÉRTÉK = halommemória_ÉRTÉK[adat_TÖMB + 2 + bejegyzés_pozíció];
            if (informatikai_részleg_Hozzárendelt) halommemória_ÉRTÉK[adat_TÖMB + 2 + bejegyzés_pozíció] = adat_ÉRTÉK;
            if (szó_SMS(név_állandó, "remove")) { for (int Loop_INDEX = bejegyzés_pozíció + 1; Loop_INDEX < bejegyzés_DARAB; Loop_INDEX++) halommemória_ÉRTÉK[adat_TÖMB + 1 + Loop_INDEX] = halommemória_ÉRTÉK[adat_TÖMB + 2 + Loop_INDEX]; halommemória_ÉRTÉK[adat_TÖMB + 1 + bejegyzés_DARAB] = 0; halommemória_ÉRTÉK[objektum_hivatkozik + 3] = bejegyzés_DARAB - 1; }
            넣기(Előző_ÉRTÉK, 2); return;
        }
        if (대응참조 && (szó_SMS(név_állandó, "get") || szó_SMS(név_állandó, "remove")) && szó_SMS(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && szó_SMS(név_állandó, "put") && szó_SMS(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && szó_SMS(név_állandó, "containsKey") && szó_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = szó_SMS(név_állandó, "put"), eltávolít = szó_SMS(név_állandó, "remove");
            int adat_ÉRTÉK = 넣기여부 ? 빼기(2) : 0, Kulcs_hivatkozik = 빼기(2), objektum_hivatkozik = 빼기(2); if (!objektum_ÉRTÉK(objektum_hivatkozik, 11)) return;
            int bejegyzés_DARAB = halommemória_ÉRTÉK[objektum_hivatkozik + 3], adat_TÖMB = halommemória_ÉRTÉK[objektum_hivatkozik + 2], 찾은여부 = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < bejegyzés_DARAB; Loop_INDEX++) if (값같음(Kulcs_hivatkozik, halommemória_ÉRTÉK[adat_TÖMB + 2 + 2 * Loop_INDEX])) { 찾은여부 = Loop_INDEX; break; }
            int Előző_ÉRTÉK = 찾은여부 < 0 ? 0 : halommemória_ÉRTÉK[adat_TÖMB + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(objektum_hivatkozik, (bejegyzés_DARAB + 1) * 2); adat_TÖMB = halommemória_ÉRTÉK[objektum_hivatkozik + 2]; 찾은여부 = bejegyzés_DARAB; if (!HIBA) halommemória_ÉRTÉK[objektum_hivatkozik + 3] = bejegyzés_DARAB + 1; }
                if (!HIBA) { halommemória_ÉRTÉK[adat_TÖMB + 2 + 2 * 찾은여부] = Kulcs_hivatkozik; halommemória_ÉRTÉK[adat_TÖMB + 3 + 2 * 찾은여부] = adat_ÉRTÉK; }
            }
            if (eltávolít && 찾은여부 >= 0) { for (int Loop_INDEX = 찾은여부 + 1; Loop_INDEX < bejegyzés_DARAB; Loop_INDEX++) { halommemória_ÉRTÉK[adat_TÖMB + 2 * Loop_INDEX] = halommemória_ÉRTÉK[adat_TÖMB + 2 + 2 * Loop_INDEX]; halommemória_ÉRTÉK[adat_TÖMB + 1 + 2 * Loop_INDEX] = halommemória_ÉRTÉK[adat_TÖMB + 3 + 2 * Loop_INDEX]; } halommemória_ÉRTÉK[adat_TÖMB + 2 * bejegyzés_DARAB] = 0; halommemória_ÉRTÉK[adat_TÖMB + 1 + 2 * bejegyzés_DARAB] = 0; halommemória_ÉRTÉK[objektum_hivatkozik + 3] = bejegyzés_DARAB - 1; }
            if (szó_SMS(név_állandó, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(Előző_ÉRTÉK, 2);
            return;
        }
        hiba_ÉRTÉK("unsupported collection method");
    }
    static boolean 잠금얻기(int objektum_hivatkozik) {
        if (!informatikai_részleg_érvényes_objektum(objektum_hivatkozik)) return false;
        if (잠금깊이[objektum_hivatkozik] != 0 && lezár_tulajdonos[objektum_hivatkozik] != aktuális_szál + 1) { változáskérés = true; return false; }
        lezár_tulajdonos[objektum_hivatkozik] = aktuális_szál + 1; 잠금깊이[objektum_hivatkozik]++; return true;
    }
    static void kiad_lezár(int objektum_hivatkozik) {
        if (!informatikai_részleg_érvényes_objektum(objektum_hivatkozik)) return;
        if (잠금깊이[objektum_hivatkozik] == 0 || lezár_tulajdonos[objektum_hivatkozik] != aktuális_szál + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[objektum_hivatkozik] == 0) lezár_tulajdonos[objektum_hivatkozik] = 0;
    }
    static boolean vált_szál() {
        szál_doboz[aktuális_szál] = doboz_INDEX;
        if (doboz_INDEX < aktuális_szál * 32) szál_Állapot[aktuális_szál] = 3;
        for (int Loop_INDEX = 0; Loop_INDEX < szálak_száma; Loop_INDEX++) if (szál_Állapot[Loop_INDEX] == 2 && szál_Állapot[가닥대기[Loop_INDEX]] == 3) szál_Állapot[Loop_INDEX] = 1;
        for (int Loop_INDEX = 1; Loop_INDEX <= szálak_száma; Loop_INDEX++) {
            int Tovább_pozíció = (aktuális_szál + Loop_INDEX) % szálak_száma;
            if (szál_Állapot[Tovább_pozíció] == 1) { aktuális_szál = Tovább_pozíció; doboz_INDEX = szál_doboz[Tovább_pozíció]; változáskérés = false; return true; }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < szálak_száma; Loop_INDEX++) if (szál_Állapot[Loop_INDEX] != 3) { hiba_ÉRTÉK("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int név_állandó, int 서술상수, int parancs_KÓD) { folyamat_szál(név_állandó, 서술상수, parancs_KÓD, false); }
    static void folyamat_szál(int név_állandó, int 서술상수, int parancs_KÓD, boolean magyar) {
        if (parancs_KÓD == 184 && szó_SMS(név_állandó, magyar ? "HOZAM_teendő" : "yield") && szó_SMS(서술상수, "()V")) { változáskérés = true; return; }
        if (parancs_KÓD == 184 && szó_SMS(név_állandó, "currentThread") && szó_SMS(서술상수, "()Ljava/lang/Thread;")) { 넣기(szál_objektum[aktuális_szál], 2); return; }
        if (parancs_KÓD == 183 && szó_SMS(név_állandó, "<init>") && (szó_SMS(서술상수, "()V") || szó_SMS(서술상수, magyar ? "(Lmagyar/saját/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int cél_CÍM = szó_SMS(서술상수, "()V") ? 0 : 빼기(2), objektum_hivatkozik = 빼기(2);
            if (!informatikai_részleg_érvényes_objektum(objektum_hivatkozik)) return;
            if (halommemória_ÉRTÉK[objektum_hivatkozik] == 13) { halommemória_ÉRTÉK[objektum_hivatkozik + 2] = cél_CÍM; halommemória_hivatkozik[objektum_hivatkozik + 2] = 1; }
            else if (cél_CÍM != 0) hiba_ÉRTÉK("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (parancs_KÓD == 182 && (szó_SMS(név_állandó, magyar ? "START_teendő" : "start") || szó_SMS(név_állandó, magyar ? "기다리기" : "join")) && szó_SMS(서술상수, "()V") || parancs_KÓD == 182 && szó_SMS(név_állandó, magyar ? "살아있는가" : "isAlive") && szó_SMS(서술상수, "()Z")) {
            int objektum_hivatkozik = 빼기(2); if (!informatikai_részleg_érvényes_objektum(objektum_hivatkozik)) return;
            int fiók_ÉRTÉK = -1; for (int Loop_INDEX = 0; Loop_INDEX < szálak_száma; Loop_INDEX++) if (szál_objektum[Loop_INDEX] == objektum_hivatkozik) fiók_ÉRTÉK = Loop_INDEX;
            if (szó_SMS(név_állandó, magyar ? "살아있는가" : "isAlive")) { 넣기(fiók_ÉRTÉK >= 0 && szál_Állapot[fiók_ÉRTÉK] != 3 ? 1 : 0, 1); return; }
            if (szó_SMS(név_állandó, magyar ? "기다리기" : "join")) { if (fiók_ÉRTÉK >= 0 && szál_Állapot[fiók_ÉRTÉK] != 3) { 가닥대기[aktuális_szál] = fiók_ÉRTÉK; szál_Állapot[aktuális_szál] = 2; változáskérés = true; } return; }
            if (fiók_ÉRTÉK >= 0) { 예외던짐(magyar ? 38 : 16, "thread already started"); return; }
            if (szálak_száma == 4) { hiba_ÉRTÉK("thread limit (4 including main)"); return; }
            int cél_CÍM = halommemória_ÉRTÉK[objektum_hivatkozik] == 13 ? halommemória_ÉRTÉK[objektum_hivatkozik + 2] : objektum_hivatkozik;
            int Fájl_INDEX = cél_CÍM > 0 && halommemória_ÉRTÉK[cél_CÍM] >= 32 ? név_metódus(halommemória_ÉRTÉK[cél_CÍM] - 32, magyar ? "Végrehajtás" : "run", "()V") : -1;
            if (cél_CÍM != 0 && Fájl_INDEX < 0) { hiba_ÉRTÉK("Runnable.run required"); return; }
            fiók_ÉRTÉK = szálak_száma++; szál_objektum[fiók_ÉRTÉK] = objektum_hivatkozik; szál_cél[fiók_ÉRTÉK] = cél_CÍM;
            int doboz = fiók_ÉRTÉK * 32; szál_doboz[fiók_ÉRTÉK] = Fájl_INDEX < 0 ? doboz - 1 : doboz; szál_Állapot[fiók_ÉRTÉK] = Fájl_INDEX < 0 ? 3 : 1;
            if (Fájl_INDEX >= 0) { doboz_metódus[doboz] = Fájl_INDEX; doboz_pozíció[doboz] = metódus_START[Fájl_INDEX]; helyi_ÉRTÉK[doboz * 128] = cél_CÍM; helyi_beír[doboz * 128] = 2; }
            return;
        }
        hiba_ÉRTÉK("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], CÍM_SMS = new int[16];
    static int helyi_CÍM() { return CÍM_objektum(0x7f000001); }
    static int CÍM_objektum(int ÉRTÉK) { int objektum_hivatkozik = kioszt_tár(14, 1); if (!HIBA) halommemória_ÉRTÉK[objektum_hivatkozik + 2] = ÉRTÉK; return objektum_hivatkozik; }
    static int 주소해독(int objektum_hivatkozik) {
        if (objektum_hivatkozik == 0 || 글같음(objektum_hivatkozik, gazda_karakter("localhost"), false)) return 0x7f000001;
        if (!objektum_ÉRTÉK(objektum_hivatkozik, 1)) return 0;
        int adat_ÉRTÉK = 0, összesen_DARAB = 0, CÍM_bájt = 0, 자릿수 = 0, bejegyzés_DARAB = halommemória_ÉRTÉK[objektum_hivatkozik + 1];
        for (int Loop_INDEX = 0; Loop_INDEX <= bejegyzés_DARAB; Loop_INDEX++) {
            int kódpont = Loop_INDEX == bejegyzés_DARAB ? '.' : halommemória_ÉRTÉK[objektum_hivatkozik + 2 + Loop_INDEX];
            if (kódpont == '.') { if (자릿수 == 0 || összesen_DARAB == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } adat_ÉRTÉK = adat_ÉRTÉK << 8 | CÍM_bájt; összesen_DARAB++; CÍM_bájt = 자릿수 = 0; }
            else { if (kódpont < '0' || kódpont > '9' || ++자릿수 > 3 || (CÍM_bájt = CÍM_bájt * 10 + kódpont - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (összesen_DARAB != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return adat_ÉRTÉK;
    }
    static int CÍM_karakter(int adat_ÉRTÉK) {
        int bejegyzés_DARAB = 0;
        for (int eltol = 24; eltol >= 0; eltol -= 8) {
            int CÍM_bájt = adat_ÉRTÉK >>> eltol & 255;
            if (CÍM_bájt >= 100) CÍM_SMS[bejegyzés_DARAB++] = '0' + CÍM_bájt / 100;
            if (CÍM_bájt >= 10) CÍM_SMS[bejegyzés_DARAB++] = '0' + CÍM_bájt / 10 % 10;
            CÍM_SMS[bejegyzés_DARAB++] = '0' + CÍM_bájt % 10; if (eltol != 0) CÍM_SMS[bejegyzés_DARAB++] = '.';
        }
        int objektum_hivatkozik = kioszt_tár(1, bejegyzés_DARAB); if (!HIBA) for (int Loop_INDEX = 0; Loop_INDEX < bejegyzés_DARAB; Loop_INDEX++) halommemória_ÉRTÉK[objektum_hivatkozik + 2 + Loop_INDEX] = CÍM_SMS[Loop_INDEX]; return objektum_hivatkozik;
    }
    static void 통신호출(int tulajdonos, int név_állandó, int 서술상수, int parancs_KÓD) {
        if (szó_SMS(tulajdonos, "java/net/InetAddress")) {
            if (parancs_KÓD == 184 && szó_SMS(név_állandó, "getLoopbackAddress") && szó_SMS(서술상수, "()Ljava/net/InetAddress;")) { 넣기(helyi_CÍM(), 2); return; }
            if (parancs_KÓD == 184 && szó_SMS(név_állandó, "getByName") && szó_SMS(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int adat_ÉRTÉK = 주소해독(빼기(2)); if (던진객체 == 0 && !HIBA) 넣기(CÍM_objektum(adat_ÉRTÉK), 2); return;
            }
            if (parancs_KÓD == 182 && szó_SMS(név_állandó, "getHostAddress") && szó_SMS(서술상수, "()Ljava/lang/String;")) { int objektum_hivatkozik = 빼기(2); if (objektum_ÉRTÉK(objektum_hivatkozik, 14)) 넣기(CÍM_karakter(halommemória_ÉRTÉK[objektum_hivatkozik + 2]), 2); return; }
        }
        if (szó_SMS(tulajdonos, "java/net/DatagramPacket")) {
            if (parancs_KÓD == 183 && szó_SMS(név_állandó, "<init>") && (szó_SMS(서술상수, "([BI)V") || szó_SMS(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean cél_ÉRTÉK_hivatkozik = szó_SMS(서술상수, "([BILjava/net/InetAddress;I)V"); int portszám = cél_ÉRTÉK_hivatkozik ? 빼기(1) : 0, CÍM_hivatkozik = cél_ÉRTÉK_hivatkozik ? 빼기(2) : 0;
                int bejegyzés_DARAB = 빼기(1), adat_TÖMB = 빼기(2), objektum_hivatkozik = 빼기(2);
                if (!objektum_ÉRTÉK(objektum_hivatkozik, 16) || !objektum_ÉRTÉK(adat_TÖMB, 20)) return;
                if (bejegyzés_DARAB < 0 || bejegyzés_DARAB > halommemória_ÉRTÉK[adat_TÖMB + 1] || portszám < 0 || portszám > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (CÍM_hivatkozik != 0 && !objektum_ÉRTÉK(CÍM_hivatkozik, 14)) return;
                halommemória_ÉRTÉK[objektum_hivatkozik + 2] = adat_TÖMB; halommemória_hivatkozik[objektum_hivatkozik + 2] = 1; halommemória_ÉRTÉK[objektum_hivatkozik + 3] = bejegyzés_DARAB;
                halommemória_ÉRTÉK[objektum_hivatkozik + 4] = CÍM_hivatkozik; halommemória_hivatkozik[objektum_hivatkozik + 4] = 1; halommemória_ÉRTÉK[objektum_hivatkozik + 5] = portszám; return;
            }
            if (parancs_KÓD == 182 && szó_SMS(név_állandó, "setLength") && szó_SMS(서술상수, "(I)V")) {
                int bejegyzés_DARAB = 빼기(1), objektum_hivatkozik = 빼기(2); if (!objektum_ÉRTÉK(objektum_hivatkozik, 16)) return;
                if (bejegyzés_DARAB < 0 || bejegyzés_DARAB > halommemória_ÉRTÉK[halommemória_ÉRTÉK[objektum_hivatkozik + 2] + 1]) 예외던짐(9, "invalid datagram length"); else halommemória_ÉRTÉK[objektum_hivatkozik + 3] = bejegyzés_DARAB; return;
            }
            if (parancs_KÓD == 182 && (szó_SMS(név_állandó, "getData") && szó_SMS(서술상수, "()[B") || szó_SMS(név_állandó, "getLength") && szó_SMS(서술상수, "()I") || szó_SMS(név_állandó, "getAddress") && szó_SMS(서술상수, "()Ljava/net/InetAddress;") || szó_SMS(név_állandó, "getPort") && szó_SMS(서술상수, "()I"))) {
                int objektum_hivatkozik = 빼기(2); if (!objektum_ÉRTÉK(objektum_hivatkozik, 16)) return;
                int bejegyzés_pozíció = szó_SMS(név_állandó, "getData") ? 2 : szó_SMS(név_állandó, "getLength") ? 3 : szó_SMS(név_állandó, "getAddress") ? 4 : 5;
                넣기(halommemória_ÉRTÉK[objektum_hivatkozik + bejegyzés_pozíció], bejegyzés_pozíció == 2 || bejegyzés_pozíció == 4 ? 2 : 1); return;
            }
        }
        if (szó_SMS(tulajdonos, "java/net/DatagramSocket")) {
            if (parancs_KÓD == 183 && szó_SMS(név_állandó, "<init>") && (szó_SMS(서술상수, "()V") || szó_SMS(서술상수, "(I)V"))) {
                int portszám = szó_SMS(서술상수, "()V") ? 0 : 빼기(1), objektum_hivatkozik = 빼기(2); if (!objektum_ÉRTÉK(objektum_hivatkozik, 15)) return;
                if (portszám < 0 || portszám > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = felhasználó.készít_hálózat(portszám); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else halommemória_ÉRTÉK[objektum_hivatkozik + 2] = 열린파일번호; return;
            }
            if (parancs_KÓD == 182 && szó_SMS(név_állandó, "setSoTimeout") && szó_SMS(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), objektum_hivatkozik = 빼기(2); if (!objektum_ÉRTÉK(objektum_hivatkozik, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else halommemória_ÉRTÉK[objektum_hivatkozik + 3] = 밀리초값; return;
            }
            if (parancs_KÓD == 182 && szó_SMS(név_állandó, "getLocalPort") && szó_SMS(서술상수, "()I")) { int objektum_hivatkozik = 빼기(2); if (objektum_ÉRTÉK(objektum_hivatkozik, 15)) 넣기(halommemória_ÉRTÉK[objektum_hivatkozik + 2] < 0 ? -1 : felhasználó.hálózat_port(halommemória_ÉRTÉK[objektum_hivatkozik + 2]), 1); return; }
            if (parancs_KÓD == 182 && szó_SMS(név_állandó, "isClosed") && szó_SMS(서술상수, "()Z")) { int objektum_hivatkozik = 빼기(2); if (objektum_ÉRTÉK(objektum_hivatkozik, 15)) 넣기(halommemória_ÉRTÉK[objektum_hivatkozik + 2] < 0 ? 1 : 0, 1); return; }
            if (parancs_KÓD == 182 && szó_SMS(név_állandó, "close") && szó_SMS(서술상수, "()V")) { int objektum_hivatkozik = 빼기(2); if (objektum_ÉRTÉK(objektum_hivatkozik, 15) && halommemória_ÉRTÉK[objektum_hivatkozik + 2] >= 0) { felhasználó.파일서술자닫기(halommemória_ÉRTÉK[objektum_hivatkozik + 2]); halommemória_ÉRTÉK[objektum_hivatkozik + 2] = -1; } return; }
            if (parancs_KÓD == 182 && (szó_SMS(név_állandó, "send") || szó_SMS(név_állandó, "receive")) && szó_SMS(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int csomag = 빼기(2), objektum_hivatkozik = 빼기(2); if (!objektum_ÉRTÉK(csomag, 16) || !objektum_ÉRTÉK(objektum_hivatkozik, 15)) return;
                int adat_TÖMB = halommemória_ÉRTÉK[csomag + 2], érvényes_hossz = halommemória_ÉRTÉK[csomag + 3], 열린파일번호 = halommemória_ÉRTÉK[objektum_hivatkozik + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (szó_SMS(név_állandó, "send")) {
                    if (!objektum_ÉRTÉK(halommemória_ÉRTÉK[csomag + 4], 14)) return;
                    if (érvényes_hossz > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < érvényes_hossz; Loop_INDEX++) 통신임시[Loop_INDEX] = halommemória_ÉRTÉK[adat_TÖMB + 2 + Loop_INDEX];
                    if (felhasználó.küld_hálózat(열린파일번호, halommemória_ÉRTÉK[halommemória_ÉRTÉK[csomag + 4] + 2], halommemória_ÉRTÉK[csomag + 5], 통신임시, érvényes_hossz) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int bejegyzés_DARAB = felhasználó.fogad_hálózat(열린파일번호, 통신임시, érvényes_hossz > 512 ? 512 : érvényes_hossz);
                    if (bejegyzés_DARAB == -11) {
                        int aktuális_idő = felhasználó.밀리초();
                        if (halommemória_ÉRTÉK[objektum_hivatkozik + 4] == 0) halommemória_ÉRTÉK[objektum_hivatkozik + 4] = aktuális_idő + 1;
                        if (halommemória_ÉRTÉK[objektum_hivatkozik + 3] > 0 && aktuális_idő - (halommemória_ÉRTÉK[objektum_hivatkozik + 4] - 1) >= halommemória_ÉRTÉK[objektum_hivatkozik + 3]) { halommemória_ÉRTÉK[objektum_hivatkozik + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(objektum_hivatkozik, 2); 넣기(csomag, 2); doboz_pozíció[doboz_INDEX] = 틀명령[doboz_INDEX]; változáskérés = true; return;
                    }
                    halommemória_ÉRTÉK[objektum_hivatkozik + 4] = 0;
                    if (bejegyzés_DARAB < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < bejegyzés_DARAB; Loop_INDEX++) halommemória_ÉRTÉK[adat_TÖMB + 2 + Loop_INDEX] = (byte)통신임시[Loop_INDEX];
                    halommemória_ÉRTÉK[csomag + 3] = bejegyzés_DARAB; halommemória_ÉRTÉK[csomag + 4] = CÍM_objektum(통신임시[513]); halommemória_hivatkozik[csomag + 4] = 1; halommemória_ÉRTÉK[csomag + 5] = 통신임시[512];
                }
                return;
            }
        }
        hiba_ÉRTÉK("unsupported java.net method");
    }
    static boolean 흐름대기(int objektum_hivatkozik) {
        int aktuális_idő = felhasználó.밀리초();
        if (halommemória_ÉRTÉK[objektum_hivatkozik + 5] == 0) halommemória_ÉRTÉK[objektum_hivatkozik + 5] = aktuális_idő + 1;
        if (halommemória_ÉRTÉK[objektum_hivatkozik + 3] > 0 && aktuális_idő - (halommemória_ÉRTÉK[objektum_hivatkozik + 5] - 1) >= halommemória_ÉRTÉK[objektum_hivatkozik + 3]) { halommemória_ÉRTÉK[objektum_hivatkozik + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        doboz_pozíció[doboz_INDEX] = 틀명령[doboz_INDEX]; változáskérés = true; return true;
    }
    static void 흐름호출(int tulajdonos, int név_állandó, int 서술상수, int parancs_KÓD) {
        boolean fogad_lap = szó_SMS(tulajdonos, "java/net/ServerSocket"), Stream = szó_SMS(tulajdonos, "java/io/InputStream") || szó_SMS(tulajdonos, "java/io/OutputStream");
        if (!Stream && parancs_KÓD == 183 && szó_SMS(név_állandó, "<init>")) {
            boolean informatikai_részleg_üres_Állapot = szó_SMS(서술상수, "()V"), 이름지정여부 = szó_SMS(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = szó_SMS(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(informatikai_részleg_üres_Állapot || fogad_lap && szó_SMS(서술상수, "(I)V") || !fogad_lap && (이름지정여부 || 주소지정여부))) { hiba_ÉRTÉK("unsupported socket constructor"); return; }
            int portszám = informatikai_részleg_üres_Állapot ? 0 : 빼기(1), CÍM_hivatkozik = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, objektum_hivatkozik = 빼기(2);
            if (!objektum_ÉRTÉK(objektum_hivatkozik, fogad_lap ? 18 : 17)) return;
            if (portszám < 0 || portszám > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !objektum_ÉRTÉK(CÍM_hivatkozik, 14)) return;
            int hálózati_azonosító = 이름지정여부 ? 주소해독(CÍM_hivatkozik) : 주소지정여부 ? halommemória_ÉRTÉK[CÍM_hivatkozik + 2] : 0x7f000001;
            if (HIBA || 던진객체 != 0) return;
            int 열린파일번호 = felhasználó.Stream_vezérlő(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = informatikai_részleg_üres_Állapot ? 0 : fogad_lap ? felhasználó.Stream_vezérlő(1, 열린파일번호, portszám) : felhasználó.KAPCSOLAT_Stream(열린파일번호, hálózati_azonosító, portszám);
            if (처리값 < 0) { felhasználó.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            halommemória_ÉRTÉK[objektum_hivatkozik + 2] = 열린파일번호; halommemória_ÉRTÉK[objektum_hivatkozik + 4] = portszám; halommemória_ÉRTÉK[objektum_hivatkozik + 6] = informatikai_részleg_üres_Állapot ? 0 : 1; return;
        }
        if (!Stream && szó_SMS(név_állandó, "setSoTimeout") && szó_SMS(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), objektum_hivatkozik = 빼기(2); if (!objektum_ÉRTÉK(objektum_hivatkozik, fogad_lap ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else halommemória_ÉRTÉK[objektum_hivatkozik + 3] = 밀리초값; return; }
        if (!Stream && szó_SMS(név_állandó, "close") && szó_SMS(서술상수, "()V")) { int objektum_hivatkozik = 빼기(2); if (objektum_ÉRTÉK(objektum_hivatkozik, fogad_lap ? 18 : 17) && halommemória_ÉRTÉK[objektum_hivatkozik + 2] >= 0) { felhasználó.파일서술자닫기(halommemória_ÉRTÉK[objektum_hivatkozik + 2]); halommemória_ÉRTÉK[objektum_hivatkozik + 2] = -1; } return; }
        if (!Stream && (szó_SMS(név_állandó, "getLocalPort") || szó_SMS(név_állandó, "getPort") || szó_SMS(név_állandó, "isClosed") || szó_SMS(név_állandó, "isConnected"))) {
            int objektum_hivatkozik = 빼기(2); if (!objektum_ÉRTÉK(objektum_hivatkozik, fogad_lap ? 18 : 17)) return;
            넣기(szó_SMS(név_állandó, "isClosed") ? halommemória_ÉRTÉK[objektum_hivatkozik + 2] < 0 ? 1 : 0 : szó_SMS(név_állandó, "isConnected") ? halommemória_ÉRTÉK[objektum_hivatkozik + 6] : szó_SMS(név_állandó, "getPort") ? halommemória_ÉRTÉK[objektum_hivatkozik + 4] : halommemória_ÉRTÉK[objektum_hivatkozik + 2] < 0 ? -1 : felhasználó.Stream_vezérlő(4, halommemória_ÉRTÉK[objektum_hivatkozik + 2], 0), 1); return;
        }
        if (fogad_lap && szó_SMS(név_állandó, "accept") && szó_SMS(서술상수, "()Ljava/net/Socket;")) {
            int objektum_hivatkozik = 빼기(2); if (!objektum_ÉRTÉK(objektum_hivatkozik, 18)) return; int 열린파일번호 = felhasználó.Stream_vezérlő(3, halommemória_ÉRTÉK[objektum_hivatkozik + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(objektum_hivatkozik)) 넣기(objektum_hivatkozik, 2); return; }
            halommemória_ÉRTÉK[objektum_hivatkozik + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = kioszt_tár(17, 5); if (HIBA) { felhasználó.파일서술자닫기(열린파일번호); return; } halommemória_ÉRTÉK[반환값 + 2] = 열린파일번호; halommemória_ÉRTÉK[반환값 + 4] = felhasználó.Stream_vezérlő(5, 열린파일번호, 0); halommemória_ÉRTÉK[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!fogad_lap && !Stream && ((szó_SMS(név_állandó, "getInputStream") && szó_SMS(서술상수, "()Ljava/io/InputStream;")) || (szó_SMS(név_állandó, "getOutputStream") && szó_SMS(서술상수, "()Ljava/io/OutputStream;")))) {
            int objektum_hivatkozik = 빼기(2); if (!objektum_ÉRTÉK(objektum_hivatkozik, 17)) return; if (halommemória_ÉRTÉK[objektum_hivatkozik + 2] < 0 || halommemória_ÉRTÉK[objektum_hivatkozik + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = kioszt_tár(19, 4); if (HIBA) return; halommemória_ÉRTÉK[반환값 + 2] = objektum_hivatkozik; halommemória_hivatkozik[반환값 + 2] = 1; halommemória_ÉRTÉK[반환값 + 3] = szó_SMS(név_állandó, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (Stream) {
            boolean 읽기여부 = szó_SMS(név_állandó, "read"), informatikai_részleg_ír_műtét = szó_SMS(név_állandó, "write"), blokk = szó_SMS(서술상수, "([B)I") || szó_SMS(서술상수, "([B)V"), informatikai_részleg_RÉSZTÖMB = szó_SMS(서술상수, "([BII)I") || szó_SMS(서술상수, "([BII)V");
            int bejegyzés_DARAB = informatikai_részleg_RÉSZTÖMB ? 빼기(1) : 0, 시작변위 = informatikai_részleg_RÉSZTÖMB ? 빼기(1) : 0, adat_TÖMB = blokk || informatikai_részleg_RÉSZTÖMB ? 빼기(2) : 0;
            int adat_ÉRTÉK = informatikai_részleg_ír_műtét && szó_SMS(서술상수, "(I)V") ? 빼기(1) : 0, objektum_hivatkozik = 빼기(2);
            if (!objektum_ÉRTÉK(objektum_hivatkozik, 19)) return; int szülő_hivatkozik = halommemória_ÉRTÉK[objektum_hivatkozik + 2], 열린파일번호 = halommemória_ÉRTÉK[szülő_hivatkozik + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (szó_SMS(név_állandó, "close") && szó_SMS(서술상수, "()V")) { felhasználó.파일서술자닫기(열린파일번호); halommemória_ÉRTÉK[szülő_hivatkozik + 2] = -1; return; }
            if (szó_SMS(név_állandó, "flush") && szó_SMS(서술상수, "()V")) return;
            if ((!읽기여부 && !informatikai_részleg_ír_műtét) || 읽기여부 != (halommemória_ÉRTÉK[objektum_hivatkozik + 3] == 0)) { hiba_ÉRTÉK("unsupported stream operation"); return; }
            if (blokk || informatikai_részleg_RÉSZTÖMB) { if (!objektum_ÉRTÉK(adat_TÖMB, 20)) return; if (blokk) bejegyzés_DARAB = halommemória_ÉRTÉK[adat_TÖMB + 1]; if (시작변위 < 0 || bejegyzés_DARAB < 0 || 시작변위 > halommemória_ÉRTÉK[adat_TÖMB + 1] - bejegyzés_DARAB) { 예외던짐(6, "stream array bounds"); return; } }
            else bejegyzés_DARAB = 1;
            if (bejegyzés_DARAB == 0) { if (읽기여부) 넣기(0, 1); return; }
            int Kész_DARAB = informatikai_részleg_ír_műtét ? halommemória_ÉRTÉK[objektum_hivatkozik + 4] : 0, 처리값 = 0;
            while (Kész_DARAB < bejegyzés_DARAB) {
                처리값 = 읽기여부 ? felhasználó.파일한바이트읽기(열린파일번호) : felhasználó.파일한바이트쓰기(열린파일번호, blokk || informatikai_részleg_RÉSZTÖMB ? halommemória_ÉRTÉK[adat_TÖMB + 2 + 시작변위 + Kész_DARAB] : adat_ÉRTÉK);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (blokk || informatikai_részleg_RÉSZTÖMB)) halommemória_ÉRTÉK[adat_TÖMB + 2 + 시작변위 + Kész_DARAB] = (byte)처리값;
                Kész_DARAB++; if (읽기여부 && !(blokk || informatikai_részleg_RÉSZTÖMB)) break;
            }
            if (처리값 == -11 && (informatikai_részleg_ír_műtét || Kész_DARAB == 0)) {
                halommemória_ÉRTÉK[objektum_hivatkozik + 4] = Kész_DARAB;
                if (흐름대기(szülő_hivatkozik)) { 넣기(objektum_hivatkozik, 2); if (blokk || informatikai_részleg_RÉSZTÖMB) 넣기(adat_TÖMB, 2); if (informatikai_részleg_RÉSZTÖMB) { 넣기(시작변위, 1); 넣기(bejegyzés_DARAB, 1); } if (informatikai_részleg_ír_műtét && !(blokk || informatikai_részleg_RÉSZTÖMB)) 넣기(adat_ÉRTÉK, 1); } return;
            }
            halommemória_ÉRTÉK[objektum_hivatkozik + 4] = 0; halommemória_ÉRTÉK[szülő_hivatkozik + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(Kész_DARAB == 0 && 처리값 == 256 ? -1 : blokk || informatikai_részleg_RÉSZTÖMB ? Kész_DARAB : 처리값, 1); return;
        }
        hiba_ÉRTÉK("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int név_állandó) {
        if (szó_SMS(név_állandó, "magyar/saját/Ablak")) return 24;
        if (szó_SMS(név_állandó, "magyar/saját/Címke")) return 26;
        if (szó_SMS(név_állandó, "magyar/saját/gomb")) return 27;
        if (szó_SMS(név_állandó, "magyar/saját/szövegmező")) return 28;
        if (szó_SMS(név_állandó, "magyar/saját/Action_alapelv")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int név_állandó) {
        return 한국어화면종(név_állandó) != 0 || szó_SMS(név_állandó, "magyar/saját/화면구성요소") || szó_SMS(név_állandó, "magyar/saját/esemény_várólista");
    }
    static int 화면종(int név_állandó) {
        int 한국어종 = 한국어화면종(név_állandó); if (한국어종 != 0) return 한국어종;
        if (szó_SMS(név_állandó, "javax/swing/JFrame")) return 24;
        if (szó_SMS(név_állandó, "javax/swing/JPanel")) return 25;
        if (szó_SMS(név_állandó, "javax/swing/JLabel")) return 26;
        if (szó_SMS(név_állandó, "javax/swing/JButton")) return 27;
        if (szó_SMS(név_állandó, "javax/swing/JTextField")) return 28;
        if (szó_SMS(név_állandó, "java/awt/event/ActionEvent")) return 29;
        if (szó_SMS(név_állandó, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int név_állandó) {
        return 화면종(név_állandó) != 0 || szó_SMS(név_állandó, "java/awt/Component") || szó_SMS(név_állandó, "java/awt/Container") || szó_SMS(név_állandó, "javax/swing/JComponent") || szó_SMS(név_állandó, "javax/swing/AbstractButton") || szó_SMS(név_állandó, "javax/swing/text/JTextComponent") || szó_SMS(név_állandó, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int objektum_hivatkozik) { if (!informatikai_részleg_érvényes_objektum(objektum_hivatkozik)) return false; if (halommemória_ÉRTÉK[objektum_hivatkozik] < 24 || halommemória_ÉRTÉK[objektum_hivatkozik] > 28) { hiba_ÉRTÉK("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int objektum_hivatkozik, int SMS_hivatkozik) {
        if (SMS_hivatkozik != 0 && !objektum_ÉRTÉK(SMS_hivatkozik, 1)) return;
        int bejegyzés_DARAB = SMS_hivatkozik == 0 ? 0 : halommemória_ÉRTÉK[SMS_hivatkozik + 1]; if (bejegyzés_DARAB > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < bejegyzés_DARAB; Loop_INDEX++) 화면글임시[Loop_INDEX] = halommemória_ÉRTÉK[SMS_hivatkozik + 2 + Loop_INDEX];
        if (felhasználó.화면글(halommemória_ÉRTÉK[objektum_hivatkozik + 2], 화면글임시, bejegyzés_DARAB) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        halommemória_ÉRTÉK[objektum_hivatkozik + 3] = SMS_hivatkozik; halommemória_hivatkozik[objektum_hivatkozik + 3] = 1;
    }
    static int 화면문자읽기(int objektum_hivatkozik) {
        int fiók_ÉRTÉK = halommemória_ÉRTÉK[objektum_hivatkozik + 2], bejegyzés_DARAB = felhasználó.화면연결(8, fiók_ÉRTÉK, 0, 0, 0, 0), 사용수 = 0;
        if (bejegyzés_DARAB < 0) { hiba_ÉRTÉK("GUI text read failed"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < bejegyzés_DARAB; Loop_INDEX++) { int 부호값 = felhasználó.화면연결(9, fiók_ÉRTÉK, Loop_INDEX, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = kioszt_tár(1, 사용수); if (!HIBA) for (int Loop_INDEX = 0; Loop_INDEX < 사용수; Loop_INDEX++) halommemória_ÉRTÉK[반환값 + 2 + Loop_INDEX] = 화면글임시[Loop_INDEX]; return 반환값;
    }
    /* magyar 객체를 직접 만들고 kernel_ÉRTÉK 화면 기능에 연결한다. Swing objektum_ÉRTÉK/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int tulajdonos, int név_állandó, int 서술상수, int parancs_KÓD) {
        if (szó_SMS(tulajdonos, "magyar/saját/esemény_várólista")) {
            if (parancs_KÓD == 184 && szó_SMS(név_állandó, "나중에실행") && szó_SMS(서술상수, "(Lmagyar/saját/실행할일;)V")) {
                int teendő_Action = 빼기(2); if (!informatikai_részleg_érvényes_objektum(teendő_Action)) return;
                if (나중수 == 8) { hiba_ÉRTÉK("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = teendő_Action; return;
            }
            if (parancs_KÓD == 184 && szó_SMS(név_állandó, "사건처리중인가") && szó_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            hiba_ÉRTÉK("지원하지 않는 magyar 화면 일정 호출"); return;
        }
        if (szó_SMS(tulajdonos, "magyar/saját/Action_alapelv")) {
            int alapelv = 빼기(2); if (!objektum_ÉRTÉK(alapelv, 29) || halommemória_ÉRTÉK[alapelv + 3] == 0) return;
            if (szó_SMS(név_állandó, "eseményforrás") && szó_SMS(서술상수, "()Lmagyar/saját/화면구성요소;")) 넣기(halommemória_ÉRTÉK[alapelv + 2], 2);
            else if (szó_SMS(név_állandó, "parancs_SMS") && szó_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(halommemória_ÉRTÉK[alapelv + 2]), 2);
            else if (szó_SMS(név_állandó, "INDEX") && szó_SMS(서술상수, "()I")) 넣기(1001, 1);
            else hiba_ÉRTÉK("지원하지 않는 magyar Művelet alapelv 호출"); return;
        }
        if (parancs_KÓD == 183 && szó_SMS(név_állandó, "<init>")) {
            int Altípus_ÉRTÉK = 한국어화면종(tulajdonos), 받이 = 0, 가로 = 0, szektor_pozíció = 0, 폭 = 0, 높이 = 0;
            if (Altípus_ÉRTÉK == 24 && szó_SMS(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (felhasználó.화면너비() - 폭) / 2; szektor_pozíció = (felhasználó.화면높이() - 높이) / 2;
            } else if ((Altípus_ÉRTÉK == 26 || Altípus_ÉRTÉK == 28) && szó_SMS(서술상수, "(Ljava/lang/String;IIII)V") || Altípus_ÉRTÉK == 27 && szó_SMS(서술상수, "(Ljava/lang/String;IIIILmagyar/saját/동작받이;)V")) {
                if (Altípus_ÉRTÉK == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); szektor_pozíció = 빼기(1); 가로 = 빼기(1);
            } else { hiba_ÉRTÉK("지원하지 않는 magyar 화면 생성자"); return; }
            int Szöveg = 빼기(2), elem_ÉRTÉK = 빼기(2); if (!화면객체(elem_ÉRTÉK)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || szektor_pozíció < 0 || 폭 > felhasználó.화면너비() - 가로 || 높이 > felhasználó.화면높이() - szektor_pozíció) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int INDEX = felhasználó.화면연결(0, Altípus_ÉRTÉK - 23, 0, 0, 0, 0);
            if (INDEX < 1 || INDEX > 32) { hiba_ÉRTÉK("화면 elem_ÉRTÉK 자리가 가득 찼습니다"); return; }
            halommemória_ÉRTÉK[elem_ÉRTÉK + 2] = INDEX; 화면참조[INDEX - 1] = elem_ÉRTÉK;
            halommemória_ÉRTÉK[elem_ÉRTÉK + 5] = 가로; halommemória_ÉRTÉK[elem_ÉRTÉK + 6] = szektor_pozíció; halommemória_ÉRTÉK[elem_ÉRTÉK + 7] = 폭; halommemória_ÉRTÉK[elem_ÉRTÉK + 8] = 높이; halommemória_ÉRTÉK[elem_ÉRTÉK + 10] = 2;
            halommemória_ÉRTÉK[elem_ÉRTÉK + 4] = 받이; halommemória_hivatkozik[elem_ÉRTÉK + 4] = 1; halommemória_ÉRTÉK[elem_ÉRTÉK + 12] = 1;
            felhasználó.화면연결(1, INDEX, 가로, szektor_pozíció, 폭, 높이);
            if (Altípus_ÉRTÉK == 24) felhasználó.화면연결(7, INDEX, 2, 0, 0, 0);
            화면문자설정(elem_ÉRTÉK, Szöveg); return;
        }
        if (parancs_KÓD != 182) { hiba_ÉRTÉK("잘못된 magyar 화면 호출 Parancs"); return; }
        if (szó_SMS(név_állandó, "ír_SMS") && szó_SMS(서술상수, "(Ljava/lang/String;)V")) {
            int Szöveg = 빼기(2), elem_ÉRTÉK = 빼기(2); if (화면객체(elem_ÉRTÉK)) 화면문자설정(elem_ÉRTÉK, Szöveg); return;
        }
        if (szó_SMS(név_állandó, "글읽기") && szó_SMS(서술상수, "()Ljava/lang/String;")) {
            int elem_ÉRTÉK = 빼기(2); if (화면객체(elem_ÉRTÉK)) 넣기(화면문자읽기(elem_ÉRTÉK), 2); return;
        }
        if (szó_SMS(név_állandó, "동작맡기기") && szó_SMS(서술상수, "(Lmagyar/saját/동작받이;)V")) {
            int 받이 = 빼기(2), elem_ÉRTÉK = 빼기(2);
            if (화면객체(elem_ÉRTÉK)) { halommemória_ÉRTÉK[elem_ÉRTÉK + 4] = 받이; halommemória_hivatkozik[elem_ÉRTÉK + 4] = 1; halommemória_ÉRTÉK[elem_ÉRTÉK + 12] = 1; } return;
        }
        if (szó_SMS(név_állandó, "hozzáad_elem") && szó_SMS(서술상수, "(Lmagyar/saját/화면구성요소;)V")) {
            int gyermek_ÉRTÉK = 빼기(2), szülő_ÉRTÉK = 빼기(2); if (!화면객체(gyermek_ÉRTÉK) || !화면객체(szülő_ÉRTÉK)) return;
            if (felhasználó.화면연결(2, halommemória_ÉRTÉK[szülő_ÉRTÉK + 2], halommemória_ÉRTÉK[gyermek_ÉRTÉK + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            halommemória_ÉRTÉK[gyermek_ÉRTÉK + 11] = szülő_ÉRTÉK; halommemória_hivatkozik[gyermek_ÉRTÉK + 11] = 1; return;
        }
        if (szó_SMS(név_állandó, "자리정하기") && szó_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), szektor_pozíció = 빼기(1), 가로 = 빼기(1), elem_ÉRTÉK = 빼기(2); if (!화면객체(elem_ÉRTÉK)) return;
            if (felhasználó.화면연결(1, halommemória_ÉRTÉK[elem_ÉRTÉK + 2], 가로, szektor_pozíció, 폭, 높이) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            halommemória_ÉRTÉK[elem_ÉRTÉK + 5] = 가로; halommemória_ÉRTÉK[elem_ÉRTÉK + 6] = szektor_pozíció; halommemória_ÉRTÉK[elem_ÉRTÉK + 7] = 폭; halommemória_ÉRTÉK[elem_ÉRTÉK + 8] = 높이; return;
        }
        if ((szó_SMS(név_állandó, "bemutató_ablak") || szó_SMS(név_állandó, "Bezárás")) && szó_SMS(서술상수, "()V")) {
            boolean Láthatóság_ÉRTÉK = szó_SMS(név_állandó, "bemutató_ablak"); int elem_ÉRTÉK = 빼기(2); if (!화면객체(elem_ÉRTÉK)) return;
            if (felhasználó.화면연결(Láthatóság_ÉRTÉK ? 3 : 4, halommemória_ÉRTÉK[elem_ÉRTÉK + 2], Láthatóság_ÉRTÉK ? 1 : 0, 0, 0, 0) < 0) { hiba_ÉRTÉK("화면은 interaktív 명령에서 실행해야 합니다"); return; }
            halommemória_ÉRTÉK[elem_ÉRTÉK + 9] = Láthatóság_ÉRTÉK ? 1 : 0; return;
        }
        if (szó_SMS(név_állandó, "보이는가") && szó_SMS(서술상수, "()Z")) { int elem_ÉRTÉK = 빼기(2); if (화면객체(elem_ÉRTÉK)) 넣기(halommemória_ÉRTÉK[elem_ÉRTÉK + 9], 1); return; }
        hiba_ÉRTÉK("지원하지 않는 magyar 화면 metódus_ÉRTÉK");
    }
    static void 화면호출(int tulajdonos, int név_állandó, int 서술상수, int parancs_KÓD) {
        if (szó_SMS(tulajdonos, "javax/swing/SwingUtilities")) {
            if (parancs_KÓD == 184 && szó_SMS(név_állandó, "invokeLater") && szó_SMS(서술상수, "(Ljava/lang/Runnable;)V")) { int objektum_hivatkozik = 빼기(2); if (!informatikai_részleg_érvényes_objektum(objektum_hivatkozik)) return; if (나중수 == 8) { hiba_ÉRTÉK("invokeLater queue full"); return; } 나중실행[나중수++] = objektum_hivatkozik; return; }
            if (parancs_KÓD == 184 && szó_SMS(név_állandó, "isEventDispatchThread") && szó_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            hiba_ÉRTÉK("unsupported SwingUtilities method"); return;
        }
        if (szó_SMS(tulajdonos, "java/awt/event/ActionEvent")) {
            int objektum_hivatkozik = 빼기(2); if (!objektum_ÉRTÉK(objektum_hivatkozik, 29)) return;
            if (szó_SMS(név_állandó, "getSource") && szó_SMS(서술상수, "()Ljava/lang/Object;")) 넣기(halommemória_ÉRTÉK[objektum_hivatkozik + 2], 2);
            else if (szó_SMS(név_állandó, "getActionCommand") && szó_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(halommemória_ÉRTÉK[objektum_hivatkozik + 2]), 2);
            else if (szó_SMS(név_állandó, "getID") && szó_SMS(서술상수, "()I")) 넣기(1001, 1);
            else hiba_ÉRTÉK("unsupported ActionEvent method"); return;
        }
        if (parancs_KÓD == 183 && szó_SMS(név_állandó, "<init>")) {
            int OSZLOPOK = 0, SMS_hivatkozik = 0;
            if (szó_SMS(서술상수, "(I)V")) OSZLOPOK = 빼기(1);
            else if (szó_SMS(서술상수, "(Ljava/lang/String;I)V")) { OSZLOPOK = 빼기(1); SMS_hivatkozik = 빼기(2); }
            else if (szó_SMS(서술상수, "(Ljava/lang/String;)V")) SMS_hivatkozik = 빼기(2);
            else if (szó_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!szó_SMS(서술상수, "()V")) { hiba_ÉRTÉK("unsupported Swing constructor"); return; }
            int objektum_hivatkozik = 빼기(2); if (!informatikai_részleg_érvényes_objektum(objektum_hivatkozik)) return;
            if (halommemória_ÉRTÉK[objektum_hivatkozik] == 30) { hiba_ÉRTÉK("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(objektum_hivatkozik) || OSZLOPOK < 0) return;
            int fiók_ÉRTÉK = felhasználó.화면연결(0, halommemória_ÉRTÉK[objektum_hivatkozik] - 23, 0, 0, 0, 0);
            if (fiók_ÉRTÉK < 1 || fiók_ÉRTÉK > 32) { hiba_ÉRTÉK("GUI widget slots exhausted"); return; }
            halommemória_ÉRTÉK[objektum_hivatkozik + 2] = fiók_ÉRTÉK; 화면참조[fiók_ÉRTÉK - 1] = objektum_hivatkozik; halommemória_ÉRTÉK[objektum_hivatkozik + 5] = halommemória_ÉRTÉK[objektum_hivatkozik] == 24 ? 130 : 16; halommemória_ÉRTÉK[objektum_hivatkozik + 6] = halommemória_ÉRTÉK[objektum_hivatkozik] == 24 ? 110 : 16;
            halommemória_ÉRTÉK[objektum_hivatkozik + 7] = halommemória_ÉRTÉK[objektum_hivatkozik] == 24 ? 380 : 220; halommemória_ÉRTÉK[objektum_hivatkozik + 8] = halommemória_ÉRTÉK[objektum_hivatkozik] == 24 ? 240 : 28; halommemória_ÉRTÉK[objektum_hivatkozik + 10] = 1;
            화면문자설정(objektum_hivatkozik, SMS_hivatkozik); return;
        }
        if (szó_SMS(név_állandó, "setText") || szó_SMS(név_állandó, "setTitle")) { int SMS_hivatkozik = 빼기(2), objektum_hivatkozik = 빼기(2); if (화면객체(objektum_hivatkozik) && szó_SMS(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(objektum_hivatkozik, SMS_hivatkozik); return; }
        if (szó_SMS(név_állandó, "getText") || szó_SMS(név_állandó, "getTitle")) { int objektum_hivatkozik = 빼기(2); if (화면객체(objektum_hivatkozik) && szó_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(objektum_hivatkozik), 2); return; }
        if (szó_SMS(név_állandó, "addActionListener") && szó_SMS(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int fogad_hivatkozik = 빼기(2), objektum_hivatkozik = 빼기(2); if (화면객체(objektum_hivatkozik)) { halommemória_ÉRTÉK[objektum_hivatkozik + 4] = fogad_hivatkozik; halommemória_hivatkozik[objektum_hivatkozik + 4] = 1; } return; }
        if (szó_SMS(név_állandó, "getContentPane") && szó_SMS(서술상수, "()Ljava/awt/Container;")) { int objektum_hivatkozik = 빼기(2); if (화면객체(objektum_hivatkozik)) 넣기(objektum_hivatkozik, 2); return; }
        if (szó_SMS(név_állandó, "setLayout") && szó_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) { int Navigáció_hivatkozik = 빼기(2), objektum_hivatkozik = 빼기(2); if (화면객체(objektum_hivatkozik) && Navigáció_hivatkozik != 0) hiba_ÉRTÉK("only absolute layout (null) is supported"); return; }
        if (szó_SMS(név_állandó, "add") && (szó_SMS(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || szó_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean Navigáció_állapot = szó_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (Navigáció_állapot) 빼기(2);
            int gyermek_hivatkozik = 빼기(2), objektum_hivatkozik = 빼기(2); if (!화면객체(gyermek_hivatkozik) || !화면객체(objektum_hivatkozik)) return;
            if (felhasználó.화면연결(2, halommemória_ÉRTÉK[objektum_hivatkozik + 2], halommemória_ÉRTÉK[gyermek_hivatkozik + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            halommemória_ÉRTÉK[gyermek_hivatkozik + 11] = objektum_hivatkozik; halommemória_hivatkozik[gyermek_hivatkozik + 11] = 1; if (!Navigáció_állapot) 넣기(gyermek_hivatkozik, 2); return;
        }
        if (szó_SMS(név_állandó, "setBounds") && szó_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), Y_koordináta = 빼기(1), x_koordináta = 빼기(1), objektum_hivatkozik = 빼기(2); if (!화면객체(objektum_hivatkozik)) return;
            if (felhasználó.화면연결(1, halommemória_ÉRTÉK[objektum_hivatkozik + 2], x_koordináta, Y_koordináta, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            halommemória_ÉRTÉK[objektum_hivatkozik + 5] = x_koordináta; halommemória_ÉRTÉK[objektum_hivatkozik + 6] = Y_koordináta; halommemória_ÉRTÉK[objektum_hivatkozik + 7] = 너비; halommemória_ÉRTÉK[objektum_hivatkozik + 8] = 높이; return;
        }
        if (szó_SMS(név_állandó, "setSize") && szó_SMS(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), objektum_hivatkozik = 빼기(2); if (!화면객체(objektum_hivatkozik)) return;
            if (felhasználó.화면연결(1, halommemória_ÉRTÉK[objektum_hivatkozik + 2], halommemória_ÉRTÉK[objektum_hivatkozik + 5], halommemória_ÉRTÉK[objektum_hivatkozik + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { halommemória_ÉRTÉK[objektum_hivatkozik + 7] = 너비; halommemória_ÉRTÉK[objektum_hivatkozik + 8] = 높이; } return;
        }
        if (szó_SMS(név_állandó, "setLocationRelativeTo") && szó_SMS(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), objektum_hivatkozik = 빼기(2); if (!화면객체(objektum_hivatkozik)) return; if (상대배치 != 0) { hiba_ÉRTÉK("only screen centering supported"); return; } halommemória_ÉRTÉK[objektum_hivatkozik + 5] = (felhasználó.화면너비() - halommemória_ÉRTÉK[objektum_hivatkozik + 7]) / 2; halommemória_ÉRTÉK[objektum_hivatkozik + 6] = (felhasználó.화면높이() - halommemória_ÉRTÉK[objektum_hivatkozik + 8]) / 2; felhasználó.화면연결(1, halommemória_ÉRTÉK[objektum_hivatkozik + 2], halommemória_ÉRTÉK[objektum_hivatkozik + 5], halommemória_ÉRTÉK[objektum_hivatkozik + 6], halommemória_ÉRTÉK[objektum_hivatkozik + 7], halommemória_ÉRTÉK[objektum_hivatkozik + 8]); return; }
        if (szó_SMS(név_állandó, "setDefaultCloseOperation") && szó_SMS(서술상수, "(I)V")) { int Policy = 빼기(1), objektum_hivatkozik = 빼기(2); if (화면객체(objektum_hivatkozik)) { if (Policy < 0 || Policy > 3) 예외던짐(9, "close policy"); else { halommemória_ÉRTÉK[objektum_hivatkozik + 10] = Policy; felhasználó.화면연결(7, halommemória_ÉRTÉK[objektum_hivatkozik + 2], Policy, 0, 0, 0); } } return; }
        if (szó_SMS(név_állandó, "setVisible") && szó_SMS(서술상수, "(Z)V")) { int adat_ÉRTÉK = 빼기(1), objektum_hivatkozik = 빼기(2); if (화면객체(objektum_hivatkozik)) { int 처리값 = felhasználó.화면연결(3, halommemória_ÉRTÉK[objektum_hivatkozik + 2], adat_ÉRTÉK, 0, 0, 0); if (처리값 < 0) hiba_ÉRTÉK("Swing requires a standalone interactive command"); else halommemória_ÉRTÉK[objektum_hivatkozik + 9] = adat_ÉRTÉK; } return; }
        if (szó_SMS(név_állandó, "dispose") && szó_SMS(서술상수, "()V")) { int objektum_hivatkozik = 빼기(2); if (화면객체(objektum_hivatkozik)) { felhasználó.화면연결(4, halommemória_ÉRTÉK[objektum_hivatkozik + 2], 0, 0, 0, 0); halommemória_ÉRTÉK[objektum_hivatkozik + 9] = 0; } return; }
        if (szó_SMS(név_állandó, "repaint") || szó_SMS(név_állandó, "validate")) { int objektum_hivatkozik = 빼기(2); if (!화면객체(objektum_hivatkozik) || !szó_SMS(서술상수, "()V")) return; felhasználó.화면연결(1, halommemória_ÉRTÉK[objektum_hivatkozik + 2], halommemória_ÉRTÉK[objektum_hivatkozik + 5], halommemória_ÉRTÉK[objektum_hivatkozik + 6], halommemória_ÉRTÉK[objektum_hivatkozik + 7], halommemória_ÉRTÉK[objektum_hivatkozik + 8]); return; }
        if (szó_SMS(név_állandó, "isVisible") && szó_SMS(서술상수, "()Z")) { int objektum_hivatkozik = 빼기(2); if (화면객체(objektum_hivatkozik)) 넣기(halommemória_ÉRTÉK[objektum_hivatkozik + 9], 1); return; }
        hiba_ÉRTÉK("unsupported Swing method (native subset)");
    }
    static void elküldés_esemény(int cél_CÍM, int esemény_szám, boolean magyar) {
        if (cél_CÍM < 1 || halommemória_ÉRTÉK[cél_CÍM] < 32) { hiba_ÉRTÉK("Java event listener required"); return; }
        int Fájl_INDEX = név_metódus(halommemória_ÉRTÉK[cél_CÍM] - 32, esemény_szám == 0 ? (magyar ? "Végrehajtás" : "run") : (magyar ? "fogad_Action" : "actionPerformed"), esemény_szám == 0 ? "()V" : (magyar ? "(Lmagyar/saját/Action_alapelv;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (Fájl_INDEX < 0) { hiba_ÉRTÉK("event callback missing"); return; }
        aktuális_szál = 0; szálak_száma = 1; doboz_INDEX = 0; szál_Állapot[0] = 1; doboz_Sor[0] = 0; doboz_lezár[0] = inicializál_doboz[0] = 0; változáskérés = false;
        for (int Loop_INDEX = 0; Loop_INDEX < 128; Loop_INDEX++) { helyi_ÉRTÉK[Loop_INDEX] = helyi_beír[Loop_INDEX] = 0; }
        doboz_metódus[0] = Fájl_INDEX; doboz_pozíció[0] = metódus_START[Fájl_INDEX]; helyi_ÉRTÉK[0] = cél_CÍM; helyi_beír[0] = 2;
        if (esemény_szám != 0) { helyi_ÉRTÉK[1] = esemény_szám; helyi_beír[1] = 2; }
        사건중 = true; végrehajt_parancs(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!HIBA) {
            if (나중수 > 0) { int cél_CÍM = 나중실행[0], magyar = 나중한국어[0]; for (int Loop_INDEX = 1; Loop_INDEX < 나중수; Loop_INDEX++) { 나중실행[Loop_INDEX - 1] = 나중실행[Loop_INDEX]; 나중한국어[Loop_INDEX - 1] = 나중한국어[Loop_INDEX]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; elküldés_esemény(cél_CÍM, 0, magyar != 0); continue; }
            if (felhasználó.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int esemény_szám = felhasználó.화면연결(5, 0, 0, 0, 0, 0); if (esemény_szám == 0) continue;
            if (esemény_szám < 0) { hiba_ÉRTÉK("GUI event I/O failed"); return; }
            int fiók_ÉRTÉK = esemény_szám & 65535; if (fiók_ÉRTÉK < 1 || fiók_ÉRTÉK > 32) continue; int objektum_hivatkozik = 화면참조[fiók_ÉRTÉK - 1]; if (objektum_hivatkozik == 0) continue;
            if ((esemény_szám & 65536) != 0) {
                if (halommemória_ÉRTÉK[objektum_hivatkozik + 10] != 0) halommemória_ÉRTÉK[objektum_hivatkozik + 9] = 0;
                if (halommemória_ÉRTÉK[objektum_hivatkozik + 10] == 3) for (int Loop_INDEX = 0; Loop_INDEX < 32; Loop_INDEX++) if (화면참조[Loop_INDEX] != 0 && halommemória_ÉRTÉK[화면참조[Loop_INDEX]] == 24) felhasználó.화면연결(4, Loop_INDEX + 1, 0, 0, 0, 0);
            } else if (halommemória_ÉRTÉK[objektum_hivatkozik + 4] != 0) {
                int fontos_fájl_hivatkozik = kioszt_tár(29, 2); if (HIBA) return; halommemória_ÉRTÉK[fontos_fájl_hivatkozik + 2] = objektum_hivatkozik; halommemória_ÉRTÉK[fontos_fájl_hivatkozik + 3] = halommemória_ÉRTÉK[objektum_hivatkozik + 12]; halommemória_hivatkozik[fontos_fájl_hivatkozik + 2] = 1; elküldés_esemény(halommemória_ÉRTÉK[objektum_hivatkozik + 4], fontos_fájl_hivatkozik, halommemória_ÉRTÉK[objektum_hivatkozik + 12] != 0);
            }
        }
    }
    public static int Futtatás() {
        if (felhasználó.인수개수() == 1 && 자바도구.같음(felhasználó.Argumentumok(0), "-version")) {
            felhasználó.Írás("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (felhasználó.인수개수() < 1) { felhasználó.Írás("Usage: java CLASS [ARGS]\n"); return 2; }
        bejegyzés_tanóra_Definíció = betölt_tanóra_Definíció(gazda_karakter(felhasználó.Argumentumok(0))); if (HIBA || bejegyzés_tanóra_Definíció < 0) return 1;
        int belépési_pont_ÉRTÉK = név_metódus(bejegyzés_tanóra_Definíció, "Futtatás", "()V");
        boolean 한국어진입 = belépési_pont_ÉRTÉK >= 0 && (metódus_hozzáfér[belépési_pont_ÉRTÉK] & 9) == 9;
        if (!한국어진입) belépési_pont_ÉRTÉK = név_metódus(bejegyzés_tanóra_Definíció, "main", "([Ljava/lang/String;)V");
        if (belépési_pont_ÉRTÉK < 0 || (metódus_hozzáfér[belépési_pont_ÉRTÉK] & 9) != 9) hiba_ÉRTÉK("public static void Futtatás() or main(String[] args) required");
        if (HIBA) return 1;
        int Argumentumok = kioszt_tár(3, felhasználó.인수개수() - 1); tömbelem[Argumentumok] = -1;
        for (int szám = 1; szám < felhasználó.인수개수() && !HIBA; szám++) halommemória_ÉRTÉK[Argumentumok + 1 + szám] = gazda_karakter(felhasználó.Argumentumok(szám));
        doboz_INDEX = 0; doboz_metódus[0] = belépési_pont_ÉRTÉK; doboz_pozíció[0] = metódus_START[belépési_pont_ÉRTÉK]; helyi_ÉRTÉK[0] = 한국어진입 ? 0 : Argumentumok; helyi_beír[0] = 한국어진입 ? 0 : 2;
        szál_Állapot[0] = 1; szál_objektum[0] = kioszt_tár(13, 2);
        végrehajt_parancs(); if (!HIBA) 화면사건들(); return HIBA ? 1 : 0;
    }
}
