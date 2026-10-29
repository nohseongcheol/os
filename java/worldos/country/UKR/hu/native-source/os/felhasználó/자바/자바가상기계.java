// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. Fájl/operandus_Sor/hivatkozik/ág 경계를 végrehajt_parancs 중 검사한다. */
public final class 자바가상기계 {
    static int[] Fájl = new int[16384], fájlnév_SMS = new int[64];
    static int[] állandó_címke = new int[512], 상가 = new int[512], állandó_MPERC_ÉRTÉK = new int[512], sztring_hivatkozik = new int[512];
    static int[] metódus_név_SMS = new int[32], metódus_beír = new int[32], metódus_hozzáfér = new int[32];
    static int[] metódus_START = new int[32], metódus_megszüntet = new int[32], metódus_Sor = new int[32], 함수지역 = new int[32];
    static int[] metódus_argumentum_DARAB = new int[32], metódus_argumentum_beír = new int[512], metódus_visszaküld = new int[32];
    static int[] határ_ÉRTÉK = new int[16384];
    static int[] helyi_ÉRTÉK = new int[4096], helyi_beír = new int[4096], operandus_Sor_ÉRTÉK = new int[4096], operandus_Sor_beír = new int[4096];
    static int[] doboz_metódus = new int[32], doboz_pozíció = new int[32], doboz_Sor = new int[32];
    static int[] halommemória_ÉRTÉK = new int[8192];
    static int Méret, 읽기위치, állandó_DARAB, metódus_DARAB, osztálynév, doboz_INDEX = -1, halommemória_megszüntet_pozíció = 1, visszaküld_beír;
    static boolean HIBA;

    static void hiba_ÉRTÉK(String szó_SMS) {
        if (!HIBA) { felhasználó.Írás("JVM error: "); felhasználó.Írás(szó_SMS); felhasználó.ír_karakter_ÉRTÉK(10); }
        HIBA = true;
    }
    static boolean klip(int Futtatás, int hossz_ÉRTÉK) { return Futtatás >= 0 && hossz_ÉRTÉK >= 0 && Futtatás <= Méret - hossz_ÉRTÉK; }
    static int bájt_ÉRTÉK() {
        if (!klip(읽기위치, 1)) { hiba_ÉRTÉK("truncated class file"); return 0; }
        return Fájl[읽기위치++];
    }
    static int 짧은수() { return bájt_ÉRTÉK() << 8 | bájt_ÉRTÉK(); }
    static int egész_szám() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int hossz_ÉRTÉK) { if (!klip(읽기위치, hossz_ÉRTÉK)) hiba_ÉRTÉK("invalid attribute size"); else 읽기위치 += hossz_ÉRTÉK; }
    static boolean csekk_állandó(int szám, int Altípus_ÉRTÉK) {
        if (szám <= 0 || szám >= állandó_DARAB || állandó_címke[szám] != Altípus_ÉRTÉK) { hiba_ÉRTÉK("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean SMS_tartomány(int Futtatás, int hossz_ÉRTÉK, String szó_SMS) {
        if (!klip(Futtatás, hossz_ÉRTÉK) || hossz_ÉRTÉK != szó_SMS.length()) return false;
        for (int szám = 0; szám < hossz_ÉRTÉK; szám++) if (Fájl[Futtatás + szám] != szó_SMS.charAt(szám)) return false;
        return true;
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
    static void kihagy_attribútum() {
        int cikk_DARAB = 짧은수();
        for (int szám = 0; szám < cikk_DARAB && !HIBA; szám++) { csekk_állandó(짧은수(), 1); 건너(egész_szám()); }
    }
    static int parancs_hossz(int ÉRTÉK) {
        if (ÉRTÉK == 16 || ÉRTÉK == 18 || ÉRTÉK == 21 || ÉRTÉK == 25 || ÉRTÉK == 54 || ÉRTÉK == 58 || ÉRTÉK == 188) return 2;
        if (ÉRTÉK == 17 || ÉRTÉK == 19 || ÉRTÉK == 132 || ÉRTÉK >= 153 && ÉRTÉK <= 167
            || ÉRTÉK >= 178 && ÉRTÉK <= 184 || ÉRTÉK == 187 || ÉRTÉK == 189 || ÉRTÉK == 192 || ÉRTÉK == 198 || ÉRTÉK == 199) return 3;
        if (ÉRTÉK >= 0 && ÉRTÉK <= 8 || ÉRTÉK >= 26 && ÉRTÉK <= 29 || ÉRTÉK >= 42 && ÉRTÉK <= 46 || ÉRTÉK == 50
            || ÉRTÉK >= 59 && ÉRTÉK <= 62 || ÉRTÉK >= 75 && ÉRTÉK <= 79 || ÉRTÉK == 83 || ÉRTÉK == 87 || ÉRTÉK == 89 || ÉRTÉK == 95
            || ÉRTÉK == 96 || ÉRTÉK == 100 || ÉRTÉK == 104 || ÉRTÉK == 108 || ÉRTÉK == 112 || ÉRTÉK == 116
            || ÉRTÉK == 120 || ÉRTÉK == 122 || ÉRTÉK == 124 || ÉRTÉK == 126 || ÉRTÉK == 128 || ÉRTÉK == 130
            || ÉRTÉK >= 145 && ÉRTÉK <= 147 || ÉRTÉK == 172 || ÉRTÉK == 176 || ÉRTÉK == 177 || ÉRTÉK == 190) return 1;
        return 0;
    }
    static void 클래스읽기() {
        if (egész_szám() != 0xcafebabe) hiba_ÉRTÉK("not a class file");
        int 부판 = 짧은수(), verzió_ÉRTÉK = 짧은수();
        if (verzió_ÉRTÉK < 45 || verzió_ÉRTÉK > 52 || 부판 != 0) hiba_ÉRTÉK("supported class versions: 45..52, minor 0");
        állandó_DARAB = 짧은수();
        if (állandó_DARAB < 1 || állandó_DARAB > 512) { hiba_ÉRTÉK("constant pool limit (511)"); return; }
        for (int szám = 1; szám < állandó_DARAB && !HIBA; szám++) {
            int Altípus_ÉRTÉK = bájt_ÉRTÉK(); állandó_címke[szám] = Altípus_ÉRTÉK;
            if (Altípus_ÉRTÉK == 1) { állandó_MPERC_ÉRTÉK[szám] = 짧은수(); 상가[szám] = 읽기위치; 건너(állandó_MPERC_ÉRTÉK[szám]); }
            else if (Altípus_ÉRTÉK == 3) 상가[szám] = egész_szám();
            else if (Altípus_ÉRTÉK == 7 || Altípus_ÉRTÉK == 8) 상가[szám] = 짧은수();
            else if (Altípus_ÉRTÉK == 9 || Altípus_ÉRTÉK == 10 || Altípus_ÉRTÉK == 12) { 상가[szám] = 짧은수(); állandó_MPERC_ÉRTÉK[szám] = 짧은수(); }
            else hiba_ÉRTÉK("unsupported constant type");
        }
        int engedély_ÉRTÉK = 짧은수();
        if ((engedély_ÉRTÉK & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) hiba_ÉRTÉK("unsupported class flags");
        osztálynév = osztálynév_SMS(짧은수());
        if (!szó_SMS(osztálynév_SMS(짧은수()), "java/lang/Object")) hiba_ÉRTÉK("inheritance unsupported");
        if (짧은수() != 0) hiba_ÉRTÉK("interfaces unsupported");
        if (짧은수() != 0) hiba_ÉRTÉK("fields unsupported");
        metódus_DARAB = 짧은수();
        if (metódus_DARAB < 1 || metódus_DARAB > 32) { hiba_ÉRTÉK("method count limit (32)"); return; }
        for (int szám = 0; szám < metódus_DARAB && !HIBA; szám++) {
            metódus_hozzáfér[szám] = 짧은수(); metódus_név_SMS[szám] = 짧은수(); metódus_beír[szám] = 짧은수();
            csekk_állandó(metódus_név_SMS[szám], 1); 서술읽기(szám);
            if ((metódus_hozzáfér[szám] & (0x100 | 0x400 | 0x20)) != 0) hiba_ÉRTÉK("native, abstract and synchronized methods unsupported");
            if ((metódus_hozzáfér[szám] & 8) == 0 && !szó_SMS(metódus_név_SMS[szám], "<init>")) hiba_ÉRTÉK("instance methods unsupported");
            if (szó_SMS(metódus_név_SMS[szám], "<clinit>")) hiba_ÉRTÉK("class initializers unsupported");
            for (int elülső_kamera_ÉRTÉK = 0; elülső_kamera_ÉRTÉK < szám; elülső_kamera_ÉRTÉK++) if (같은말(metódus_név_SMS[elülső_kamera_ÉRTÉK], metódus_név_SMS[szám]) && 같은말(metódus_beír[elülső_kamera_ÉRTÉK], metódus_beír[szám])) hiba_ÉRTÉK("duplicate method");
            int cikk_DARAB = 짧은수();
            for (int attribútum_ÉRTÉK = 0; attribútum_ÉRTÉK < cikk_DARAB && !HIBA; attribútum_ÉRTÉK++) {
                int Név = 짧은수(), hossz_ÉRTÉK = egész_szám(), Futtatás = 읽기위치;
                if (!klip(Futtatás, hossz_ÉRTÉK)) { hiba_ÉRTÉK("truncated method attribute"); break; }
                if (szó_SMS(Név, "Code")) {
                    if (metódus_START[szám] != 0) hiba_ÉRTÉK("duplicate Code attribute");
                    metódus_Sor[szám] = 짧은수(); 함수지역[szám] = 짧은수(); int KÓD_hossz = egész_szám();
                    if (metódus_Sor[szám] > 128 || 함수지역[szám] > 128 || 함수지역[szám] < metódus_argumentum_DARAB[szám]
                        || KÓD_hossz < 1 || KÓD_hossz > 8192) hiba_ÉRTÉK("method memory limits exceeded");
                    metódus_START[szám] = 읽기위치; 건너(KÓD_hossz); metódus_megszüntet[szám] = 읽기위치;
                    if (짧은수() != 0) hiba_ÉRTÉK("exception handlers unsupported");
                    kihagy_attribútum();
                    if (읽기위치 != Futtatás + hossz_ÉRTÉK) hiba_ÉRTÉK("Code attribute size mismatch");
                } else 건너(hossz_ÉRTÉK);
            }
            if (metódus_START[szám] == 0) hiba_ÉRTÉK("missing Code attribute");
            int tárolóhely_bejegyzés = metódus_START[szám];
            while (tárolóhely_bejegyzés < metódus_megszüntet[szám] && !HIBA) {
                int hossz_ÉRTÉK = parancs_hossz(Fájl[tárolóhely_bejegyzés]);
                if (hossz_ÉRTÉK == 0 || hossz_ÉRTÉK > metódus_megszüntet[szám] - tárolóhely_bejegyzés) { hiba_ÉRTÉK("unsupported or truncated bytecode"); break; }
                határ_ÉRTÉK[tárolóhely_bejegyzés] = szám + 1; tárolóhely_bejegyzés += hossz_ÉRTÉK;
            }
            // 실행하지 않는 경로에도 잘못된 ág 목적지를 허용하지 않는다.
            tárolóhely_bejegyzés = metódus_START[szám];
            while (tárolóhely_bejegyzés < metódus_megszüntet[szám] && !HIBA) {
                int ÉRTÉK = Fájl[tárolóhely_bejegyzés];
                if (ÉRTÉK >= 153 && ÉRTÉK <= 167 || ÉRTÉK == 198 || ÉRTÉK == 199) {
                    int cél_ÉRTÉK = tárolóhely_bejegyzés + (short)(Fájl[tárolóhely_bejegyzés + 1] << 8 | Fájl[tárolóhely_bejegyzés + 2]);
                    if (cél_ÉRTÉK < metódus_START[szám] || cél_ÉRTÉK >= metódus_megszüntet[szám] || határ_ÉRTÉK[cél_ÉRTÉK] != szám + 1) hiba_ÉRTÉK("invalid branch target");
                }
                tárolóhely_bejegyzés += parancs_hossz(ÉRTÉK);
            }
        }
        if (!HIBA) kihagy_attribútum();
        if (읽기위치 != Méret) hiba_ÉRTÉK("extra class file data");
    }
    static int kioszt_tár(int Altípus_ÉRTÉK, int hossz_ÉRTÉK) {
        if (hossz_ÉRTÉK < 0 || hossz_ÉRTÉK > halommemória_ÉRTÉK.length - halommemória_megszüntet_pozíció - 2) { hiba_ÉRTÉK("object heap exhausted or negative array size"); return 0; }
        int hivatkozik = halommemória_megszüntet_pozíció; halommemória_megszüntet_pozíció += hossz_ÉRTÉK + 2; halommemória_ÉRTÉK[hivatkozik] = Altípus_ÉRTÉK; halommemória_ÉRTÉK[hivatkozik + 1] = hossz_ÉRTÉK;
        return hivatkozik;
    }
    static boolean objektum_ÉRTÉK(int hivatkozik, int Altípus_ÉRTÉK) {
        if (hivatkozik < 1 || hivatkozik >= halommemória_megszüntet_pozíció - 1 || halommemória_ÉRTÉK[hivatkozik] != Altípus_ÉRTÉK) { hiba_ÉRTÉK("null or invalid object reference"); return false; }
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
        if (doboz_INDEX == 31) { hiba_ÉRTÉK("call stack limit (32)"); return; }
        int Tovább_cikk = doboz_INDEX + 1;
        for (int szám = 0; szám < 128; szám++) helyi_beír[Tovább_cikk * 128 + szám] = 0;
        for (int szám = metódus_argumentum_DARAB[FÜGGVÉNY_ÉRTÉK] - 1; szám >= 0; szám--) {
            helyi_ÉRTÉK[Tovább_cikk * 128 + szám] = 빼기(metódus_argumentum_beír[FÜGGVÉNY_ÉRTÉK * 16 + szám]); helyi_beír[Tovább_cikk * 128 + szám] = metódus_argumentum_beír[FÜGGVÉNY_ÉRTÉK * 16 + szám];
        }
        doboz_INDEX = Tovább_cikk; doboz_metódus[doboz_INDEX] = FÜGGVÉNY_ÉRTÉK; doboz_pozíció[doboz_INDEX] = metódus_START[FÜGGVÉNY_ÉRTÉK]; doboz_Sor[doboz_INDEX] = 0;
    }
    static void visszaküld_KR(int beír_ÉRTÉK) {
        if (beír_ÉRTÉK != metódus_visszaküld[doboz_metódus[doboz_INDEX]]) { hiba_ÉRTÉK("return type mismatch"); return; }
        int ÉRTÉK = beír_ÉRTÉK == 0 ? 0 : 빼기(beír_ÉRTÉK);
        doboz_INDEX--; if (doboz_INDEX >= 0 && beír_ÉRTÉK != 0) 넣기(ÉRTÉK, beír_ÉRTÉK);
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
                if (ÉRTÉK < 1 || ÉRTÉK > 127) { hiba_ÉRTÉK("file stream paths currently require ASCII"); return; }
                Stream_fájlnév[tárolóhely_bejegyzés] = ÉRTÉK;
            }
            Stream_fájlnév[hossz_ÉRTÉK] = 0;
            int 서술자 = felhasználó.파일서술자열기(Stream_fájlnév, Kimenet ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { hiba_ÉRTÉK("FileNotFoundException: file open failed"); return; }
            halommemória_ÉRTÉK[Stream_ÉRTÉK + 2] = 서술자; halommemória_ÉRTÉK[Stream_ÉRTÉK + 3] = 1;
            return;
        }
        if (Parancs != 182) { hiba_ÉRTÉK("invalid file stream invocation"); return; }
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
            if (KR < -1) hiba_ÉRTÉK("IOException: read failed"); else 넣기(KR, 1);
        } else if (felhasználó.파일한바이트쓰기(서술자, ÉRTÉK) != 1) hiba_ÉRTÉK("IOException: write failed");
    }
    static void hív_metódus(int INDEX, int Parancs) {
        if (!csekk_állandó(INDEX, 10)) return;
        int tulajdonos_ÉRTÉK = osztálynév_SMS(상가[INDEX]), Név = hivatkozik_név(állandó_MPERC_ÉRTÉK[INDEX]), formáz_ÉRTÉK = referenciális_típus(állandó_MPERC_ÉRTÉK[INDEX]);
        if (HIBA) return;
        if (같은말(tulajdonos_ÉRTÉK, osztálynév)) {
            if (Parancs != 184) { hiba_ÉRTÉK("only static user methods are supported"); return; }
            for (int szám = 0; szám < metódus_DARAB; szám++) if (같은말(Név, metódus_név_SMS[szám]) && 같은말(formáz_ÉRTÉK, metódus_beír[szám])) {
                if ((metódus_hozzáfér[szám] & 8) == 0) hiba_ÉRTÉK("method is not static"); else 호출(szám);
                return;
            }
            hiba_ÉRTÉK("NoSuchMethodError"); return;
        }
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
        hiba_ÉRTÉK("unsupported library method");
    }
    static int TÖMB_tárolóhely(int hivatkozik, int alsó_index_ÉRTÉK, int beír_ÉRTÉK) {
        if (!objektum_ÉRTÉK(hivatkozik, beír_ÉRTÉK)) return 0;
        if (alsó_index_ÉRTÉK < 0 || alsó_index_ÉRTÉK >= halommemória_ÉRTÉK[hivatkozik + 1]) { hiba_ÉRTÉK("ArrayIndexOutOfBoundsException"); return 0; }
        return hivatkozik + 2 + alsó_index_ÉRTÉK;
    }
    static void végrehajt_parancs() {
        int 남음 = 500000;
        while (doboz_INDEX >= 0 && !HIBA) {
            if (--남음 == 0) { hiba_ÉRTÉK("instruction limit (500000)"); break; }
            int Futtatás = doboz_pozíció[doboz_INDEX], ÉRTÉK = 명바();
            if (HIBA) break;
            if (ÉRTÉK == 0) continue;
            if (ÉRTÉK == 1) { 넣기(0, 2); continue; }
            if (ÉRTÉK >= 2 && ÉRTÉK <= 8) { 넣기(ÉRTÉK - 3, 1); continue; }
            if (ÉRTÉK == 16) { 넣기((byte)명바(), 1); continue; }
            if (ÉRTÉK == 17) { 넣기((short)명짧(), 1); continue; }
            if (ÉRTÉK == 18 || ÉRTÉK == 19) {
                int szám = ÉRTÉK == 18 ? 명바() : 명짧();
                if (szám <= 0 || szám >= állandó_DARAB) hiba_ÉRTÉK("invalid ldc constant");
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
            if (ÉRTÉK == 46 || ÉRTÉK == 50) {
                int alsó_index_ÉRTÉK = 빼기(1), hivatkozik = 빼기(2), tárolóhely_bejegyzés = TÖMB_tárolóhely(hivatkozik, alsó_index_ÉRTÉK, ÉRTÉK == 46 ? 2 : 3);
                if (!HIBA) 넣기(halommemória_ÉRTÉK[tárolóhely_bejegyzés], ÉRTÉK == 46 ? 1 : 2); continue;
            }
            if (ÉRTÉK == 79 || ÉRTÉK == 83) {
                int cikk_elem = 빼기(ÉRTÉK == 79 ? 1 : 2), alsó_index_ÉRTÉK = 빼기(1), hivatkozik = 빼기(2), tárolóhely_bejegyzés = TÖMB_tárolóhely(hivatkozik, alsó_index_ÉRTÉK, ÉRTÉK == 79 ? 2 : 3);
                if (ÉRTÉK == 83 && cikk_elem != 0) objektum_ÉRTÉK(cikk_elem, 1);
                if (!HIBA) halommemória_ÉRTÉK[tárolóhely_bejegyzés] = cikk_elem; continue;
            }
            if (ÉRTÉK == 87) { 빼기(0); continue; }
            if (ÉRTÉK == 89) { int 가 = 빼기(0), beír_ÉRTÉK = visszaküld_beír; 넣기(가, beír_ÉRTÉK); 넣기(가, beír_ÉRTÉK); continue; }
            if (ÉRTÉK == 95) { int 가 = 빼기(0), 가형 = visszaküld_beír, MPERC_operandus = 빼기(0), MPERC_operandus_beír = visszaküld_beír; 넣기(가, 가형); 넣기(MPERC_operandus, MPERC_operandus_beír); continue; }
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
            if (ÉRTÉK == 178) {
                int szám = 명짧(); if (!csekk_állandó(szám, 9)) continue;
                if (!szó_SMS(osztálynév_SMS(상가[szám]), "java/lang/System") || !szó_SMS(hivatkozik_név(állandó_MPERC_ÉRTÉK[szám]), "out")
                    || !szó_SMS(referenciális_típus(állandó_MPERC_ÉRTÉK[szám]), "Ljava/io/PrintStream;")) hiba_ÉRTÉK("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (ÉRTÉK == 182 || ÉRTÉK == 183 || ÉRTÉK == 184) { hív_metódus(명짧(), ÉRTÉK); continue; }
            if (ÉRTÉK == 187) {
                int Név = osztálynév_SMS(명짧());
                if (szó_SMS(Név, "java/lang/StringBuilder")) 넣기(kioszt_tár(4, 1), 2);
                else if (szó_SMS(Név, "java/io/FileInputStream") || szó_SMS(Név, "java/io/FileOutputStream")) {
                    int hivatkozik = kioszt_tár(szó_SMS(Név, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!HIBA) { halommemória_ÉRTÉK[hivatkozik + 2] = -1; 넣기(hivatkozik, 2); }
                } else hiba_ÉRTÉK("unsupported object construction");
                continue;
            }
            if (ÉRTÉK == 188 || ÉRTÉK == 189) {
                if (ÉRTÉK == 188) { if (명바() != 10) hiba_ÉRTÉK("only int[] newarray is supported"); }
                else if (!szó_SMS(osztálynév_SMS(명짧()), "java/lang/String")) hiba_ÉRTÉK("only String[] anewarray is supported");
                int hossz_ÉRTÉK = 빼기(1); 넣기(kioszt_tár(ÉRTÉK == 188 ? 2 : 3, hossz_ÉRTÉK), 2); continue;
            }
            if (ÉRTÉK == 190) {
                int hivatkozik = 빼기(2);
                if (hivatkozik < 1 || hivatkozik >= halommemória_megszüntet_pozíció - 1 || (halommemória_ÉRTÉK[hivatkozik] != 2 && halommemória_ÉRTÉK[hivatkozik] != 3)) hiba_ÉRTÉK("null or invalid array");
                else 넣기(halommemória_ÉRTÉK[hivatkozik + 1], 1); continue;
            }
            if (ÉRTÉK == 192) {
                int Név = osztálynév_SMS(명짧()), hivatkozik = 빼기(2);
                if (!szó_SMS(Név, "java/lang/String")) hiba_ÉRTÉK("unsupported checkcast");
                else if (hivatkozik != 0) objektum_ÉRTÉK(hivatkozik, 1);
                넣기(hivatkozik, 2); continue;
            }
            hiba_ÉRTÉK("unsupported bytecode");
        }
    }
    public static int Futtatás() {
        if (felhasználó.인수개수() == 1 && 자바도구.같음(felhasználó.Argumentumok(0), "-version")) {
            felhasználó.Írás("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (felhasználó.인수개수() < 1) { felhasználó.Írás("Usage: java CLASS [ARGS]\n"); return 2; }
        int hossz_ÉRTÉK = 자바도구.Név(fájlnév_SMS, felhasználó.Argumentumok(0));
        if (hossz_ÉRTÉK < 1 || hossz_ÉRTÉK > 57) { felhasználó.Írás("java: invalid class name\n"); return 2; }
        fájlnév_SMS[hossz_ÉRTÉK] = '.'; fájlnév_SMS[hossz_ÉRTÉK + 1] = 'c'; fájlnév_SMS[hossz_ÉRTÉK + 2] = 'l'; fájlnév_SMS[hossz_ÉRTÉK + 3] = 'a'; fájlnév_SMS[hossz_ÉRTÉK + 4] = 's'; fájlnév_SMS[hossz_ÉRTÉK + 5] = 's';
        Méret = felhasználó.파일읽기(fájlnév_SMS, Fájl);
        if (Méret < 0) { felhasználó.Írás("java: cannot read class: "); 자바도구.ír_szám(Méret); felhasználó.ír_karakter_ÉRTÉK(10); return 1; }
        클래스읽기(); if (HIBA) return 1;
        int karakter_név = állandó_SMS(osztálynév);
        if (!HIBA && halommemória_ÉRTÉK[karakter_név + 1] != hossz_ÉRTÉK) hiba_ÉRTÉK("class name does not match file");
        for (int szám = 0; szám < hossz_ÉRTÉK && !HIBA; szám++) if (halommemória_ÉRTÉK[karakter_név + 2 + szám] != fájlnév_SMS[szám]) hiba_ÉRTÉK("class name does not match file");
        int belépési_pont_ÉRTÉK = -1;
        for (int szám = 0; szám < metódus_DARAB; szám++) if (szó_SMS(metódus_név_SMS[szám], "main") && szó_SMS(metódus_beír[szám], "([Ljava/lang/String;)V") && (metódus_hozzáfér[szám] & 9) == 9) belépési_pont_ÉRTÉK = szám;
        if (belépési_pont_ÉRTÉK < 0) hiba_ÉRTÉK("public static void main(String[] args) required");
        if (HIBA) return 1;
        int Argumentumok = kioszt_tár(3, felhasználó.인수개수() - 1);
        for (int szám = 1; szám < felhasználó.인수개수() && !HIBA; szám++) halommemória_ÉRTÉK[Argumentumok + 1 + szám] = gazda_karakter(felhasználó.Argumentumok(szám));
        doboz_INDEX = 0; doboz_metódus[0] = belépési_pont_ÉRTÉK; doboz_pozíció[0] = metódus_START[belépési_pont_ÉRTÉK]; helyi_ÉRTÉK[0] = Argumentumok; helyi_beír[0] = 2;
        végrehajt_parancs(); return HIBA ? 1 : 0;
    }
}
