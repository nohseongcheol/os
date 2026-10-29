// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. Súbor/operand_Vrstvy/zdroj/vetva 경계를 Vykonať_príkaz 중 검사한다. */
public final class 자바가상기계 {
    static int[] Súbor = new int[16384], názov_súboru_SMS = new int[64];
    static int[] konštanta_značka = new int[512], 상가 = new int[512], konštanta_SECOND_VALUE = new int[512], reťazec_zdroj = new int[512];
    static int[] metóda_názov_SMS = new int[32], metóda_Typ = new int[32], metóda_prístup = new int[32];
    static int[] metóda_START = new int[32], metóda_ukončiť_hovor = new int[32], metóda_Vrstvy = new int[32], 함수지역 = new int[32];
    static int[] metóda_argument_COUNT = new int[32], metóda_argument_Typ = new int[512], metóda_vrátiť = new int[32];
    static int[] 경계 = new int[16384];
    static int[] miestny_VALUE = new int[4096], miestny_Typ = new int[4096], operand_Vrstvy_VALUE = new int[4096], operand_Vrstvy_Typ = new int[4096];
    static int[] rám_metóda = new int[32], rám_pozícia = new int[32], rám_Vrstvy = new int[32];
    static int[] halda_VALUE = new int[8192];
    static int Veľkosť, 읽기위치, konštanta_COUNT, metóda_COUNT, názov_triedy, rám_INDEX = -1, halda_ukončiť_hovor_pozícia = 1, vrátiť_Typ;
    static boolean chyba;

    static void zlyhanie_VALUE(String Word_SMS) {
        if (!chyba) { používateľ.Zápis("JVM error: "); používateľ.Zápis(Word_SMS); používateľ.zapísať_znak_VALUE(10); }
        chyba = true;
    }
    static boolean klip(int Spustiť_2, int dĺžka_VALUE) { return Spustiť_2 >= 0 && dĺžka_VALUE >= 0 && Spustiť_2 <= Veľkosť - dĺžka_VALUE; }
    static int Byte_VALUE() {
        if (!klip(읽기위치, 1)) { zlyhanie_VALUE("truncated class file"); return 0; }
        return Súbor[읽기위치++];
    }
    static int 짧은수() { return Byte_VALUE() << 8 | Byte_VALUE(); }
    static int celé_číslo() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int dĺžka_VALUE) { if (!klip(읽기위치, dĺžka_VALUE)) zlyhanie_VALUE("invalid attribute size"); else 읽기위치 += dĺžka_VALUE; }
    static boolean skontrolovať_konštanta(int 수, int 종류) {
        if (수 <= 0 || 수 >= konštanta_COUNT || konštanta_značka[수] != 종류) { zlyhanie_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean SMS_rozsah(int Spustiť_2, int dĺžka_VALUE, String Word_SMS) {
        if (!klip(Spustiť_2, dĺžka_VALUE) || dĺžka_VALUE != Word_SMS.length()) return false;
        for (int 수 = 0; 수 < dĺžka_VALUE; 수++) if (Súbor[Spustiť_2 + 수] != Word_SMS.charAt(수)) return false;
        return true;
    }
    static boolean Word_SMS(int konštanta_VALUE, String Word_SMS) { return skontrolovať_konštanta(konštanta_VALUE, 1) && SMS_rozsah(상가[konštanta_VALUE], konštanta_SECOND_VALUE[konštanta_VALUE], Word_SMS); }
    static boolean 같은말(int 가, int SECOND_operand) {
        if (!skontrolovať_konštanta(가, 1) || !skontrolovať_konštanta(SECOND_operand, 1) || konštanta_SECOND_VALUE[가] != konštanta_SECOND_VALUE[SECOND_operand]) return false;
        for (int 수 = 0; 수 < konštanta_SECOND_VALUE[가]; 수++) if (Súbor[상가[가] + 수] != Súbor[상가[SECOND_operand] + 수]) return false;
        return true;
    }
    static int názov_triedy_SMS(int 수) { return skontrolovať_konštanta(수, 7) && skontrolovať_konštanta(상가[수], 1) ? 상가[수] : 0; }
    static int zdroj_názov(int 수) { return skontrolovať_konštanta(수, 12) && skontrolovať_konštanta(상가[수], 1) ? 상가[수] : 0; }
    static int referenčný_typ(int 수) { return skontrolovať_konštanta(수, 12) && skontrolovať_konštanta(konštanta_SECOND_VALUE[수], 1) ? konštanta_SECOND_VALUE[수] : 0; }
    static int 서술형(int 끝, boolean prázdny_Typ) {
        if (읽기위치 >= 끝) { zlyhanie_VALUE("invalid descriptor"); return 0; }
        int VALUE = Byte_VALUE();
        if (VALUE == 'V' && prázdny_Typ) return 0;
        if (VALUE == 'I' || VALUE == 'B' || VALUE == 'C' || VALUE == 'S' || VALUE == 'Z') return 1;
        if (VALUE == '[') { 서술형(끝, false); return 2; }
        if (VALUE == 'L') {
            int Spustiť_2 = 읽기위치;
            while (읽기위치 < 끝 && Súbor[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == Spustiť_2) zlyhanie_VALUE("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        zlyhanie_VALUE("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int funkcia_VALUE) {
        int 이전 = 읽기위치, 수 = metóda_Typ[funkcia_VALUE];
        if (!skontrolovať_konštanta(수, 1)) return;
        읽기위치 = 상가[수]; int 끝 = 읽기위치 + konštanta_SECOND_VALUE[수];
        if (Byte_VALUE() != '(') zlyhanie_VALUE("invalid method descriptor");
        int položka_COUNT = 0;
        while (!chyba && 읽기위치 < 끝 && Súbor[읽기위치] != ')') {
            if (položka_COUNT == 16) { zlyhanie_VALUE("too many method arguments"); break; }
            metóda_argument_Typ[funkcia_VALUE * 16 + položka_COUNT++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || Byte_VALUE() != ')') zlyhanie_VALUE("invalid method descriptor");
        metóda_vrátiť[funkcia_VALUE] = 서술형(끝, true); metóda_argument_COUNT[funkcia_VALUE] = položka_COUNT;
        if (읽기위치 != 끝) zlyhanie_VALUE("invalid method descriptor");
        읽기위치 = 이전;
    }
    static void 속성건너() {
        int položka_COUNT = 짧은수();
        for (int 수 = 0; 수 < položka_COUNT && !chyba; 수++) { skontrolovať_konštanta(짧은수(), 1); 건너(celé_číslo()); }
    }
    static int príkaz_dĺžka(int VALUE) {
        if (VALUE == 16 || VALUE == 18 || VALUE == 21 || VALUE == 25 || VALUE == 54 || VALUE == 58 || VALUE == 188) return 2;
        if (VALUE == 17 || VALUE == 19 || VALUE == 132 || VALUE >= 153 && VALUE <= 167
            || VALUE >= 178 && VALUE <= 184 || VALUE == 187 || VALUE == 189 || VALUE == 192 || VALUE == 198 || VALUE == 199) return 3;
        if (VALUE >= 0 && VALUE <= 8 || VALUE >= 26 && VALUE <= 29 || VALUE >= 42 && VALUE <= 46 || VALUE == 50
            || VALUE >= 59 && VALUE <= 62 || VALUE >= 75 && VALUE <= 79 || VALUE == 83 || VALUE == 87 || VALUE == 89 || VALUE == 95
            || VALUE == 96 || VALUE == 100 || VALUE == 104 || VALUE == 108 || VALUE == 112 || VALUE == 116
            || VALUE == 120 || VALUE == 122 || VALUE == 124 || VALUE == 126 || VALUE == 128 || VALUE == 130
            || VALUE >= 145 && VALUE <= 147 || VALUE == 172 || VALUE == 176 || VALUE == 177 || VALUE == 190) return 1;
        return 0;
    }
    static void 클래스읽기() {
        if (celé_číslo() != 0xcafebabe) zlyhanie_VALUE("not a class file");
        int 부판 = 짧은수(), verzia_VALUE = 짧은수();
        if (verzia_VALUE < 45 || verzia_VALUE > 52 || 부판 != 0) zlyhanie_VALUE("supported class versions: 45..52, minor 0");
        konštanta_COUNT = 짧은수();
        if (konštanta_COUNT < 1 || konštanta_COUNT > 512) { zlyhanie_VALUE("constant pool limit (511)"); return; }
        for (int 수 = 1; 수 < konštanta_COUNT && !chyba; 수++) {
            int 종류 = Byte_VALUE(); konštanta_značka[수] = 종류;
            if (종류 == 1) { konštanta_SECOND_VALUE[수] = 짧은수(); 상가[수] = 읽기위치; 건너(konštanta_SECOND_VALUE[수]); }
            else if (종류 == 3) 상가[수] = celé_číslo();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[수] = 짧은수(); konštanta_SECOND_VALUE[수] = 짧은수(); }
            else zlyhanie_VALUE("unsupported constant type");
        }
        int povolenie_VALUE = 짧은수();
        if ((povolenie_VALUE & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) zlyhanie_VALUE("unsupported class flags");
        názov_triedy = názov_triedy_SMS(짧은수());
        if (!Word_SMS(názov_triedy_SMS(짧은수()), "java/lang/Object")) zlyhanie_VALUE("inheritance unsupported");
        if (짧은수() != 0) zlyhanie_VALUE("interfaces unsupported");
        if (짧은수() != 0) zlyhanie_VALUE("fields unsupported");
        metóda_COUNT = 짧은수();
        if (metóda_COUNT < 1 || metóda_COUNT > 32) { zlyhanie_VALUE("method count limit (32)"); return; }
        for (int 수 = 0; 수 < metóda_COUNT && !chyba; 수++) {
            metóda_prístup[수] = 짧은수(); metóda_názov_SMS[수] = 짧은수(); metóda_Typ[수] = 짧은수();
            skontrolovať_konštanta(metóda_názov_SMS[수], 1); 서술읽기(수);
            if ((metóda_prístup[수] & (0x100 | 0x400 | 0x20)) != 0) zlyhanie_VALUE("native, abstract and synchronized methods unsupported");
            if ((metóda_prístup[수] & 8) == 0 && !Word_SMS(metóda_názov_SMS[수], "<init>")) zlyhanie_VALUE("instance methods unsupported");
            if (Word_SMS(metóda_názov_SMS[수], "<clinit>")) zlyhanie_VALUE("class initializers unsupported");
            for (int predný_VALUE = 0; predný_VALUE < 수; predný_VALUE++) if (같은말(metóda_názov_SMS[predný_VALUE], metóda_názov_SMS[수]) && 같은말(metóda_Typ[predný_VALUE], metóda_Typ[수])) zlyhanie_VALUE("duplicate method");
            int položka_COUNT = 짧은수();
            for (int atribút_VALUE = 0; atribút_VALUE < položka_COUNT && !chyba; atribút_VALUE++) {
                int Názov = 짧은수(), dĺžka_VALUE = celé_číslo(), Spustiť_2 = 읽기위치;
                if (!klip(Spustiť_2, dĺžka_VALUE)) { zlyhanie_VALUE("truncated method attribute"); break; }
                if (Word_SMS(Názov, "Code")) {
                    if (metóda_START[수] != 0) zlyhanie_VALUE("duplicate Code attribute");
                    metóda_Vrstvy[수] = 짧은수(); 함수지역[수] = 짧은수(); int kód_dĺžka = celé_číslo();
                    if (metóda_Vrstvy[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < metóda_argument_COUNT[수]
                        || kód_dĺžka < 1 || kód_dĺžka > 8192) zlyhanie_VALUE("method memory limits exceeded");
                    metóda_START[수] = 읽기위치; 건너(kód_dĺžka); metóda_ukončiť_hovor[수] = 읽기위치;
                    if (짧은수() != 0) zlyhanie_VALUE("exception handlers unsupported");
                    속성건너();
                    if (읽기위치 != Spustiť_2 + dĺžka_VALUE) zlyhanie_VALUE("Code attribute size mismatch");
                } else 건너(dĺžka_VALUE);
            }
            if (metóda_START[수] == 0) zlyhanie_VALUE("missing Code attribute");
            int 칸 = metóda_START[수];
            while (칸 < metóda_ukončiť_hovor[수] && !chyba) {
                int dĺžka_VALUE = príkaz_dĺžka(Súbor[칸]);
                if (dĺžka_VALUE == 0 || dĺžka_VALUE > metóda_ukončiť_hovor[수] - 칸) { zlyhanie_VALUE("unsupported or truncated bytecode"); break; }
                경계[칸] = 수 + 1; 칸 += dĺžka_VALUE;
            }
            // 실행하지 않는 경로에도 잘못된 vetva 목적지를 허용하지 않는다.
            칸 = metóda_START[수];
            while (칸 < metóda_ukončiť_hovor[수] && !chyba) {
                int VALUE = Súbor[칸];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                    int cieľ_VALUE = 칸 + (short)(Súbor[칸 + 1] << 8 | Súbor[칸 + 2]);
                    if (cieľ_VALUE < metóda_START[수] || cieľ_VALUE >= metóda_ukončiť_hovor[수] || 경계[cieľ_VALUE] != 수 + 1) zlyhanie_VALUE("invalid branch target");
                }
                칸 += príkaz_dĺžka(VALUE);
            }
        }
        if (!chyba) 속성건너();
        if (읽기위치 != Veľkosť) zlyhanie_VALUE("extra class file data");
    }
    static int vyhradiť_Úložisko(int 종류, int dĺžka_VALUE) {
        if (dĺžka_VALUE < 0 || dĺžka_VALUE > halda_VALUE.length - halda_ukončiť_hovor_pozícia - 2) { zlyhanie_VALUE("object heap exhausted or negative array size"); return 0; }
        int zdroj = halda_ukončiť_hovor_pozícia; halda_ukončiť_hovor_pozícia += dĺžka_VALUE + 2; halda_VALUE[zdroj] = 종류; halda_VALUE[zdroj + 1] = dĺžka_VALUE;
        return zdroj;
    }
    static boolean objekt_VALUE(int zdroj, int 종류) {
        if (zdroj < 1 || zdroj >= halda_ukončiť_hovor_pozícia - 1 || halda_VALUE[zdroj] != 종류) { zlyhanie_VALUE("null or invalid object reference"); return false; }
        return true;
    }
    static int konštanta_SMS(int INDEX) {
        if (!skontrolovať_konštanta(INDEX, 1)) return 0;
        if (reťazec_zdroj[INDEX] != 0) return reťazec_zdroj[INDEX];
        int zdroj = vyhradiť_Úložisko(1, konštanta_SECOND_VALUE[INDEX]); if (chyba) return 0;
        int 끝 = 상가[INDEX] + konštanta_SECOND_VALUE[INDEX], 수 = 상가[INDEX], dĺžka_VALUE = 0;
        while (수 < 끝 && !chyba) {
            int VALUE = Súbor[수++];
            if (VALUE == 0) zlyhanie_VALUE("invalid modified UTF-8");
            else if (VALUE >= 192 && VALUE <= 223 && 수 < 끝) {
                int Ďalej_položka = Súbor[수++];
                if ((Ďalej_položka & 192) != 128) zlyhanie_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 31) << 6 | Ďalej_položka & 63;
                if (VALUE != 0 && VALUE < 128) zlyhanie_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 224 && VALUE <= 239 && 수 + 1 < 끝) {
                int 가 = Súbor[수++], SECOND_operand = Súbor[수++];
                if ((가 & 192) != 128 || (SECOND_operand & 192) != 128) zlyhanie_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 15) << 12 | (가 & 63) << 6 | SECOND_operand & 63;
                if (VALUE < 2048) zlyhanie_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 128) zlyhanie_VALUE("invalid modified UTF-8");
            halda_VALUE[zdroj + 2 + dĺžka_VALUE++] = VALUE;
        }
        halda_VALUE[zdroj + 1] = dĺžka_VALUE; reťazec_zdroj[INDEX] = zdroj; return zdroj;
    }
    static int hostiteľ_znak(String VALUE) {
        int zdroj = vyhradiť_Úložisko(1, VALUE.length()); if (chyba) return 0;
        for (int 수 = 0; 수 < VALUE.length(); 수++) halda_VALUE[zdroj + 2 + 수] = VALUE.charAt(수);
        return zdroj;
    }
    static void zapísať_SMS(int zdroj) {
        if (zdroj == 0) { používateľ.Zápis("null"); return; }
        if (!objekt_VALUE(zdroj, 1)) return;
        for (int 수 = 0; 수 < halda_VALUE[zdroj + 1]; 수++) používateľ.zapísať_znak_VALUE(halda_VALUE[zdroj + 2 + 수]);
    }
    static int číslica_znak(int VALUE) {
        int zdroj = vyhradiť_Úložisko(1, 11); if (chyba) return 0;
        int dĺžka_VALUE = 0;
        if (VALUE < 0) halda_VALUE[zdroj + 2 + dĺžka_VALUE++] = '-'; else VALUE = -VALUE;
        int pozičný_index = 1000000000; boolean Spustiť_2 = false;
        while (pozičný_index != 0) {
            int 수 = -(VALUE / pozičný_index);
            if (수 != 0 || Spustiť_2 || pozičný_index == 1) { halda_VALUE[zdroj + 2 + dĺžka_VALUE++] = '0' + 수; Spustiť_2 = true; }
            VALUE %= pozičný_index; pozičný_index /= 10;
        }
        halda_VALUE[zdroj + 1] = dĺžka_VALUE; return zdroj;
    }
    static int 정수해독(int zdroj) {
        if (!objekt_VALUE(zdroj, 1)) return 0;
        int dĺžka_VALUE = halda_VALUE[zdroj + 1], 수 = 0, VALUE = 0; boolean 음수 = false;
        if (dĺžka_VALUE > 0 && (halda_VALUE[zdroj + 2] == '-' || halda_VALUE[zdroj + 2] == '+')) { 음수 = halda_VALUE[zdroj + 2] == '-'; 수++; }
        if (수 == dĺžka_VALUE) zlyhanie_VALUE("NumberFormatException");
        for (; 수 < dĺžka_VALUE && !chyba; 수++) {
            int číslica_VALUE = halda_VALUE[zdroj + 2 + 수] - '0';
            if (číslica_VALUE < 0 || číslica_VALUE > 9 || VALUE < -214748364 || VALUE == -214748364 && číslica_VALUE > (음수 ? 8 : 7)) zlyhanie_VALUE("NumberFormatException");
            VALUE = VALUE * 10 - číslica_VALUE;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static void 넣기(int VALUE, int Typ_VALUE) {
        if (chyba) return;
        if (rám_INDEX < 0 || rám_Vrstvy[rám_INDEX] >= metóda_Vrstvy[rám_metóda[rám_INDEX]]) { zlyhanie_VALUE("operand stack overflow"); return; }
        int 칸 = rám_INDEX * 128 + rám_Vrstvy[rám_INDEX]++; operand_Vrstvy_VALUE[칸] = VALUE; operand_Vrstvy_Typ[칸] = Typ_VALUE;
    }
    static int 빼기(int Typ_VALUE) {
        if (chyba) return 0;
        if (rám_INDEX < 0 || rám_Vrstvy[rám_INDEX] < 1) { zlyhanie_VALUE("operand stack underflow"); return 0; }
        int 칸 = rám_INDEX * 128 + --rám_Vrstvy[rám_INDEX]; vrátiť_Typ = operand_Vrstvy_Typ[칸];
        if (Typ_VALUE != 0 && vrátiť_Typ != Typ_VALUE) zlyhanie_VALUE("operand type mismatch");
        return operand_Vrstvy_VALUE[칸];
    }
    static void 지역읽기(int INDEX, int Typ_VALUE) {
        if (INDEX >= 함수지역[rám_metóda[rám_INDEX]] || INDEX < 0 || miestny_Typ[rám_INDEX * 128 + INDEX] != Typ_VALUE) { zlyhanie_VALUE("invalid or uninitialized local"); return; }
        넣기(miestny_VALUE[rám_INDEX * 128 + INDEX], Typ_VALUE);
    }
    static void zapísať_miestny(int INDEX, int Typ_VALUE) {
        if (INDEX >= 함수지역[rám_metóda[rám_INDEX]] || INDEX < 0) { zlyhanie_VALUE("local index out of range"); return; }
        int VALUE = 빼기(Typ_VALUE); miestny_VALUE[rám_INDEX * 128 + INDEX] = VALUE; miestny_Typ[rám_INDEX * 128 + INDEX] = Typ_VALUE;
    }
    static int 명바() {
        int Pozícia = rám_pozícia[rám_INDEX];
        if (Pozícia < metóda_START[rám_metóda[rám_INDEX]] || Pozícia >= metóda_ukončiť_hovor[rám_metóda[rám_INDEX]]) { zlyhanie_VALUE("instruction pointer out of range"); return 0; }
        rám_pozícia[rám_INDEX]++; return Súbor[Pozícia];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void premiestniť_VALUE(int Pozícia) {
        int funkcia_VALUE = rám_metóda[rám_INDEX];
        if (Pozícia < metóda_START[funkcia_VALUE] || Pozícia >= metóda_ukončiť_hovor[funkcia_VALUE] || 경계[Pozícia] != funkcia_VALUE + 1) zlyhanie_VALUE("invalid branch target");
        else rám_pozícia[rám_INDEX] = Pozícia;
    }
    static void 호출(int funkcia_VALUE) {
        if (rám_INDEX == 31) { zlyhanie_VALUE("call stack limit (32)"); return; }
        int Ďalej_položka = rám_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) miestny_Typ[Ďalej_položka * 128 + 수] = 0;
        for (int 수 = metóda_argument_COUNT[funkcia_VALUE] - 1; 수 >= 0; 수--) {
            miestny_VALUE[Ďalej_položka * 128 + 수] = 빼기(metóda_argument_Typ[funkcia_VALUE * 16 + 수]); miestny_Typ[Ďalej_položka * 128 + 수] = metóda_argument_Typ[funkcia_VALUE * 16 + 수];
        }
        rám_INDEX = Ďalej_položka; rám_metóda[rám_INDEX] = funkcia_VALUE; rám_pozícia[rám_INDEX] = metóda_START[funkcia_VALUE]; rám_Vrstvy[rám_INDEX] = 0;
    }
    static void vrátiť_KR(int Typ_VALUE) {
        if (Typ_VALUE != metóda_vrátiť[rám_metóda[rám_INDEX]]) { zlyhanie_VALUE("return type mismatch"); return; }
        int VALUE = Typ_VALUE == 0 ? 0 : 빼기(Typ_VALUE);
        rám_INDEX--; if (rám_INDEX >= 0 && Typ_VALUE != 0) 넣기(VALUE, Typ_VALUE);
    }
    static int[] Stream_názov_súboru = new int[64];
    static void Súbor_Stream_CALL(int vlastník_VALUE, int Názov, int formát_VALUE, int Príkaz) {
        boolean Výstup = Word_SMS(vlastník_VALUE, "java/io/FileOutputStream");
        int 종류 = Výstup ? 6 : 5;
        if (Príkaz == 183 && Word_SMS(Názov, "<init>")) {
            boolean 이어 = false;
            if (Výstup && Word_SMS(formát_VALUE, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Word_SMS(formát_VALUE, "(Ljava/lang/String;)V")) { zlyhanie_VALUE("unsupported file stream constructor"); return; }
            int Súbor_položka_názov = 빼기(2), Stream_VALUE = 빼기(2);
            if (!objekt_VALUE(Súbor_položka_názov, 1) || !objekt_VALUE(Stream_VALUE, 종류) || chyba) return;
            if (halda_VALUE[Stream_VALUE + 3] != 0) { zlyhanie_VALUE("file stream already initialized"); return; }
            int dĺžka_VALUE = halda_VALUE[Súbor_položka_názov + 1];
            if (dĺžka_VALUE < 1 || dĺžka_VALUE > 63) { zlyhanie_VALUE("invalid file name length"); return; }
            for (int 칸 = 0; 칸 < dĺžka_VALUE; 칸++) {
                int VALUE = halda_VALUE[Súbor_položka_názov + 2 + 칸];
                if (VALUE < 1 || VALUE > 127) { zlyhanie_VALUE("file stream paths currently require ASCII"); return; }
                Stream_názov_súboru[칸] = VALUE;
            }
            Stream_názov_súboru[dĺžka_VALUE] = 0;
            int 서술자 = používateľ.파일서술자열기(Stream_názov_súboru, Výstup ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { zlyhanie_VALUE("FileNotFoundException: file open failed"); return; }
            halda_VALUE[Stream_VALUE + 2] = 서술자; halda_VALUE[Stream_VALUE + 3] = 1;
            return;
        }
        if (Príkaz != 182) { zlyhanie_VALUE("invalid file stream invocation"); return; }
        int Akcia = -1, VALUE = 0;
        if (Word_SMS(Názov, "close") && Word_SMS(formát_VALUE, "()V")) Akcia = 0;
        if (!Výstup && Word_SMS(Názov, "read") && Word_SMS(formát_VALUE, "()I")) Akcia = 1;
        if (Výstup && Word_SMS(Názov, "write") && Word_SMS(formát_VALUE, "(I)V")) { Akcia = 2; VALUE = 빼기(1); }
        if (Akcia < 0) { zlyhanie_VALUE("unsupported file stream method"); return; }
        int Stream_VALUE = 빼기(2);
        if (!objekt_VALUE(Stream_VALUE, 종류) || chyba) return;
        if (halda_VALUE[Stream_VALUE + 3] == 0) { zlyhanie_VALUE("uninitialized file stream"); return; }
        int 서술자 = halda_VALUE[Stream_VALUE + 2];
        if (Akcia == 0) {
            if (서술자 >= 0 && používateľ.파일서술자닫기(서술자) < 0) zlyhanie_VALUE("IOException: close failed");
            halda_VALUE[Stream_VALUE + 2] = -1; return;
        }
        if (서술자 < 0) { zlyhanie_VALUE("IOException: stream closed"); return; }
        if (Akcia == 1) {
            int KR = používateľ.파일한바이트읽기(서술자);
            if (KR < -1) zlyhanie_VALUE("IOException: read failed"); else 넣기(KR, 1);
        } else if (používateľ.파일한바이트쓰기(서술자, VALUE) != 1) zlyhanie_VALUE("IOException: write failed");
    }
    static void CALL_metóda(int INDEX, int Príkaz) {
        if (!skontrolovať_konštanta(INDEX, 10)) return;
        int vlastník_VALUE = názov_triedy_SMS(상가[INDEX]), Názov = zdroj_názov(konštanta_SECOND_VALUE[INDEX]), formát_VALUE = referenčný_typ(konštanta_SECOND_VALUE[INDEX]);
        if (chyba) return;
        if (같은말(vlastník_VALUE, názov_triedy)) {
            if (Príkaz != 184) { zlyhanie_VALUE("only static user methods are supported"); return; }
            for (int 수 = 0; 수 < metóda_COUNT; 수++) if (같은말(Názov, metóda_názov_SMS[수]) && 같은말(formát_VALUE, metóda_Typ[수])) {
                if ((metóda_prístup[수] & 8) == 0) zlyhanie_VALUE("method is not static"); else 호출(수);
                return;
            }
            zlyhanie_VALUE("NoSuchMethodError"); return;
        }
        if (Word_SMS(vlastník_VALUE, "java/io/FileInputStream") || Word_SMS(vlastník_VALUE, "java/io/FileOutputStream")) {
            Súbor_Stream_CALL(vlastník_VALUE, Názov, formát_VALUE, Príkaz); return;
        }
        if (Príkaz == 184 && Word_SMS(vlastník_VALUE, "java/lang/Integer") && Word_SMS(Názov, "parseInt") && Word_SMS(formát_VALUE, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (Príkaz == 182 && Word_SMS(vlastník_VALUE, "java/io/PrintStream") && (Word_SMS(Názov, "println") || Word_SMS(Názov, "print"))) {
            int Typ_VALUE = 0, VALUE = 0;
            if (Word_SMS(formát_VALUE, "(I)V")) { Typ_VALUE = 1; VALUE = 빼기(1); }
            else if (Word_SMS(formát_VALUE, "(Z)V")) { Typ_VALUE = 2; VALUE = 빼기(1); }
            else if (Word_SMS(formát_VALUE, "(C)V")) { Typ_VALUE = 3; VALUE = 빼기(1); }
            else if (Word_SMS(formát_VALUE, "(Ljava/lang/String;)V")) { Typ_VALUE = 4; VALUE = 빼기(2); }
            else if (!Word_SMS(formát_VALUE, "()V") || !Word_SMS(Názov, "println")) zlyhanie_VALUE("unsupported print descriptor");
            if (빼기(2) != -1) zlyhanie_VALUE("invalid PrintStream receiver");
            if (chyba) return;
            if (Typ_VALUE == 1) 자바도구.수쓰기(VALUE);
            if (Typ_VALUE == 2) používateľ.Zápis(VALUE == 0 ? "false" : "true");
            if (Typ_VALUE == 3) používateľ.zapísať_znak_VALUE(VALUE & 65535);
            if (Typ_VALUE == 4) zapísať_SMS(VALUE);
            if (Word_SMS(Názov, "println")) používateľ.zapísať_znak_VALUE(10);
            return;
        }
        if (Príkaz == 182 && Word_SMS(vlastník_VALUE, "java/lang/String")) {
            if (Word_SMS(Názov, "length") && Word_SMS(formát_VALUE, "()I")) {
                int zdroj = 빼기(2); if (objekt_VALUE(zdroj, 1)) 넣기(halda_VALUE[zdroj + 1], 1); return;
            }
            if (Word_SMS(Názov, "charAt") && Word_SMS(formát_VALUE, "(I)C")) {
                int dolný_index_VALUE = 빼기(1), zdroj = 빼기(2);
                if (objekt_VALUE(zdroj, 1)) {
                    if (dolný_index_VALUE < 0 || dolný_index_VALUE >= halda_VALUE[zdroj + 1]) zlyhanie_VALUE("StringIndexOutOfBoundsException"); else 넣기(halda_VALUE[zdroj + 2 + dolný_index_VALUE], 1);
                }
                return;
            }
        }
        if (Word_SMS(vlastník_VALUE, "java/lang/StringBuilder")) {
            if (Príkaz == 183 && Word_SMS(Názov, "<init>") && Word_SMS(formát_VALUE, "()V")) { objekt_VALUE(빼기(2), 4); return; }
            if (Príkaz == 182 && Word_SMS(Názov, "toString") && Word_SMS(formát_VALUE, "()Ljava/lang/String;")) {
                int zdroj = 빼기(2); if (objekt_VALUE(zdroj, 4)) 넣기(halda_VALUE[zdroj + 2] == 0 ? hostiteľ_znak("") : halda_VALUE[zdroj + 2], 2); return;
            }
            if (Príkaz == 182 && Word_SMS(Názov, "append")) {
                int Spracovanie_textu = 0;
                if (Word_SMS(formát_VALUE, "(I)Ljava/lang/StringBuilder;")) Spracovanie_textu = číslica_znak(빼기(1));
                else if (Word_SMS(formát_VALUE, "(Z)Ljava/lang/StringBuilder;")) Spracovanie_textu = hostiteľ_znak(빼기(1) == 0 ? "false" : "true");
                else if (Word_SMS(formát_VALUE, "(C)Ljava/lang/StringBuilder;")) {
                    int VALUE = 빼기(1); Spracovanie_textu = vyhradiť_Úložisko(1, 1); if (!chyba) halda_VALUE[Spracovanie_textu + 2] = VALUE & 65535;
                }
                else if (Word_SMS(formát_VALUE, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { Spracovanie_textu = 빼기(2); if (Spracovanie_textu == 0) Spracovanie_textu = hostiteľ_znak("null"); }
                else { zlyhanie_VALUE("unsupported StringBuilder append"); return; }
                int zdroj = 빼기(2); if (!objekt_VALUE(zdroj, 4) || !objekt_VALUE(Spracovanie_textu, 1)) return;
                int predný_VALUE = halda_VALUE[zdroj + 2], predný_VALUE_dĺžka = predný_VALUE == 0 ? 0 : halda_VALUE[predný_VALUE + 1], BACK_VALUE_dĺžka = halda_VALUE[Spracovanie_textu + 1];
                int 새글 = vyhradiť_Úložisko(1, predný_VALUE_dĺžka + BACK_VALUE_dĺžka); if (chyba) return;
                for (int 수 = 0; 수 < predný_VALUE_dĺžka; 수++) halda_VALUE[새글 + 2 + 수] = halda_VALUE[predný_VALUE + 2 + 수];
                for (int 수 = 0; 수 < BACK_VALUE_dĺžka; 수++) halda_VALUE[새글 + 2 + predný_VALUE_dĺžka + 수] = halda_VALUE[Spracovanie_textu + 2 + 수];
                halda_VALUE[zdroj + 2] = 새글; 넣기(zdroj, 2); return;
            }
        }
        zlyhanie_VALUE("unsupported library method");
    }
    static int 배열칸(int zdroj, int dolný_index_VALUE, int Typ_VALUE) {
        if (!objekt_VALUE(zdroj, Typ_VALUE)) return 0;
        if (dolný_index_VALUE < 0 || dolný_index_VALUE >= halda_VALUE[zdroj + 1]) { zlyhanie_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return zdroj + 2 + dolný_index_VALUE;
    }
    static void Vykonať_príkaz() {
        int 남음 = 500000;
        while (rám_INDEX >= 0 && !chyba) {
            if (--남음 == 0) { zlyhanie_VALUE("instruction limit (500000)"); break; }
            int Spustiť_2 = rám_pozícia[rám_INDEX], VALUE = 명바();
            if (chyba) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int 수 = VALUE == 18 ? 명바() : 명짧();
                if (수 <= 0 || 수 >= konštanta_COUNT) zlyhanie_VALUE("invalid ldc constant");
                else if (konštanta_značka[수] == 3) 넣기(상가[수], 1);
                else if (konštanta_značka[수] == 8) 넣기(konštanta_SMS(상가[수]), 2);
                else zlyhanie_VALUE("unsupported ldc constant");
                continue;
            }
            if (VALUE == 21 || VALUE == 25) { 지역읽기(명바(), VALUE == 21 ? 1 : 2); continue; }
            if (VALUE >= 26 && VALUE <= 29) { 지역읽기(VALUE - 26, 1); continue; }
            if (VALUE >= 42 && VALUE <= 45) { 지역읽기(VALUE - 42, 2); continue; }
            if (VALUE == 54 || VALUE == 58) { zapísať_miestny(명바(), VALUE == 54 ? 1 : 2); continue; }
            if (VALUE >= 59 && VALUE <= 62) { zapísať_miestny(VALUE - 59, 1); continue; }
            if (VALUE >= 75 && VALUE <= 78) { zapísať_miestny(VALUE - 75, 2); continue; }
            if (VALUE == 46 || VALUE == 50) {
                int dolný_index_VALUE = 빼기(1), zdroj = 빼기(2), 칸 = 배열칸(zdroj, dolný_index_VALUE, VALUE == 46 ? 2 : 3);
                if (!chyba) 넣기(halda_VALUE[칸], VALUE == 46 ? 1 : 2); continue;
            }
            if (VALUE == 79 || VALUE == 83) {
                int položka_prvok = 빼기(VALUE == 79 ? 1 : 2), dolný_index_VALUE = 빼기(1), zdroj = 빼기(2), 칸 = 배열칸(zdroj, dolný_index_VALUE, VALUE == 79 ? 2 : 3);
                if (VALUE == 83 && položka_prvok != 0) objekt_VALUE(položka_prvok, 1);
                if (!chyba) halda_VALUE[칸] = položka_prvok; continue;
            }
            if (VALUE == 87) { 빼기(0); continue; }
            if (VALUE == 89) { int 가 = 빼기(0), Typ_VALUE = vrátiť_Typ; 넣기(가, Typ_VALUE); 넣기(가, Typ_VALUE); continue; }
            if (VALUE == 95) { int 가 = 빼기(0), 가형 = vrátiť_Typ, SECOND_operand = 빼기(0), SECOND_operand_Typ = vrátiť_Typ; 넣기(가, 가형); 넣기(SECOND_operand, SECOND_operand_Typ); continue; }
            if (VALUE == 96 || VALUE == 100 || VALUE == 104 || VALUE == 108 || VALUE == 112 || VALUE == 120
                || VALUE == 122 || VALUE == 124 || VALUE == 126 || VALUE == 128 || VALUE == 130) {
                int SECOND_operand = 빼기(1), 가 = 빼기(1), KR = 0;
                if ((VALUE == 108 || VALUE == 112) && SECOND_operand == 0) { zlyhanie_VALUE("ArithmeticException: / by zero"); continue; }
                if (VALUE == 96) KR = 가 + SECOND_operand;
                if (VALUE == 100) KR = 가 - SECOND_operand;
                if (VALUE == 104) KR = 가 * SECOND_operand;
                if (VALUE == 108) KR = 가 / SECOND_operand;
                if (VALUE == 112) KR = 가 % SECOND_operand;
                if (VALUE == 120) KR = 가 << SECOND_operand;
                if (VALUE == 122) KR = 가 >> SECOND_operand;
                if (VALUE == 124) KR = 가 >>> SECOND_operand;
                if (VALUE == 126) KR = 가 & SECOND_operand;
                if (VALUE == 128) KR = 가 | SECOND_operand;
                if (VALUE == 130) KR = 가 ^ SECOND_operand;
                넣기(KR, 1); continue;
            }
            if (VALUE == 116) { 넣기(-빼기(1), 1); continue; }
            if (VALUE == 132) {
                int miestny_Rozsah = 명바(), prírastok_krok = (byte)명바(); 지역읽기(miestny_Rozsah, 1); 넣기(빼기(1) + prírastok_krok, 1); zapísať_miestny(miestny_Rozsah, 1); continue;
            }
            if (VALUE >= 145 && VALUE <= 147) {
                int 수 = 빼기(1); 넣기(VALUE == 145 ? (byte)수 : VALUE == 146 ? (char)수 : (short)수, 1); continue;
            }
            if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                int cieľ_VALUE = Spustiť_2 + (short)명짧(); boolean 갈까 = VALUE == 167;
                if (VALUE >= 153 && VALUE <= 158) {
                    int 수 = 빼기(1); 갈까 = VALUE == 153 ? 수 == 0 : VALUE == 154 ? 수 != 0 : VALUE == 155 ? 수 < 0 : VALUE == 156 ? 수 >= 0 : VALUE == 157 ? 수 > 0 : 수 <= 0;
                } else if (VALUE >= 159 && VALUE <= 166) {
                    int SECOND_operand = 빼기(VALUE >= 165 ? 2 : 1), 가 = 빼기(VALUE >= 165 ? 2 : 1);
                    갈까 = VALUE == 159 || VALUE == 165 ? 가 == SECOND_operand : VALUE == 160 || VALUE == 166 ? 가 != SECOND_operand : VALUE == 161 ? 가 < SECOND_operand : VALUE == 162 ? 가 >= SECOND_operand : VALUE == 163 ? 가 > SECOND_operand : 가 <= SECOND_operand;
                } else if (VALUE == 198 || VALUE == 199) { int 수 = 빼기(2); 갈까 = VALUE == 198 ? 수 == 0 : 수 != 0; }
                if (갈까) premiestniť_VALUE(cieľ_VALUE); continue;
            }
            if (VALUE == 172 || VALUE == 176 || VALUE == 177) { vrátiť_KR(VALUE == 172 ? 1 : VALUE == 176 ? 2 : 0); continue; }
            if (VALUE == 178) {
                int 수 = 명짧(); if (!skontrolovať_konštanta(수, 9)) continue;
                if (!Word_SMS(názov_triedy_SMS(상가[수]), "java/lang/System") || !Word_SMS(zdroj_názov(konštanta_SECOND_VALUE[수]), "out")
                    || !Word_SMS(referenčný_typ(konštanta_SECOND_VALUE[수]), "Ljava/io/PrintStream;")) zlyhanie_VALUE("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (VALUE == 182 || VALUE == 183 || VALUE == 184) { CALL_metóda(명짧(), VALUE); continue; }
            if (VALUE == 187) {
                int Názov = názov_triedy_SMS(명짧());
                if (Word_SMS(Názov, "java/lang/StringBuilder")) 넣기(vyhradiť_Úložisko(4, 1), 2);
                else if (Word_SMS(Názov, "java/io/FileInputStream") || Word_SMS(Názov, "java/io/FileOutputStream")) {
                    int zdroj = vyhradiť_Úložisko(Word_SMS(Názov, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!chyba) { halda_VALUE[zdroj + 2] = -1; 넣기(zdroj, 2); }
                } else zlyhanie_VALUE("unsupported object construction");
                continue;
            }
            if (VALUE == 188 || VALUE == 189) {
                if (VALUE == 188) { if (명바() != 10) zlyhanie_VALUE("only int[] newarray is supported"); }
                else if (!Word_SMS(názov_triedy_SMS(명짧()), "java/lang/String")) zlyhanie_VALUE("only String[] anewarray is supported");
                int dĺžka_VALUE = 빼기(1); 넣기(vyhradiť_Úložisko(VALUE == 188 ? 2 : 3, dĺžka_VALUE), 2); continue;
            }
            if (VALUE == 190) {
                int zdroj = 빼기(2);
                if (zdroj < 1 || zdroj >= halda_ukončiť_hovor_pozícia - 1 || (halda_VALUE[zdroj] != 2 && halda_VALUE[zdroj] != 3)) zlyhanie_VALUE("null or invalid array");
                else 넣기(halda_VALUE[zdroj + 1], 1); continue;
            }
            if (VALUE == 192) {
                int Názov = názov_triedy_SMS(명짧()), zdroj = 빼기(2);
                if (!Word_SMS(Názov, "java/lang/String")) zlyhanie_VALUE("unsupported checkcast");
                else if (zdroj != 0) objekt_VALUE(zdroj, 1);
                넣기(zdroj, 2); continue;
            }
            zlyhanie_VALUE("unsupported bytecode");
        }
    }
    public static int Spustiť_2() {
        if (používateľ.인수개수() == 1 && 자바도구.같음(používateľ.Argumenty(0), "-version")) {
            používateľ.Zápis("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (používateľ.인수개수() < 1) { používateľ.Zápis("Usage: java CLASS [ARGS]\n"); return 2; }
        int dĺžka_VALUE = 자바도구.Názov(názov_súboru_SMS, používateľ.Argumenty(0));
        if (dĺžka_VALUE < 1 || dĺžka_VALUE > 57) { používateľ.Zápis("java: invalid class name\n"); return 2; }
        názov_súboru_SMS[dĺžka_VALUE] = '.'; názov_súboru_SMS[dĺžka_VALUE + 1] = 'c'; názov_súboru_SMS[dĺžka_VALUE + 2] = 'l'; názov_súboru_SMS[dĺžka_VALUE + 3] = 'a'; názov_súboru_SMS[dĺžka_VALUE + 4] = 's'; názov_súboru_SMS[dĺžka_VALUE + 5] = 's';
        Veľkosť = používateľ.파일읽기(názov_súboru_SMS, Súbor);
        if (Veľkosť < 0) { používateľ.Zápis("java: cannot read class: "); 자바도구.수쓰기(Veľkosť); používateľ.zapísať_znak_VALUE(10); return 1; }
        클래스읽기(); if (chyba) return 1;
        int znak_názov = konštanta_SMS(názov_triedy);
        if (!chyba && halda_VALUE[znak_názov + 1] != dĺžka_VALUE) zlyhanie_VALUE("class name does not match file");
        for (int 수 = 0; 수 < dĺžka_VALUE && !chyba; 수++) if (halda_VALUE[znak_názov + 2 + 수] != názov_súboru_SMS[수]) zlyhanie_VALUE("class name does not match file");
        int položka_bod_VALUE = -1;
        for (int 수 = 0; 수 < metóda_COUNT; 수++) if (Word_SMS(metóda_názov_SMS[수], "main") && Word_SMS(metóda_Typ[수], "([Ljava/lang/String;)V") && (metóda_prístup[수] & 9) == 9) položka_bod_VALUE = 수;
        if (položka_bod_VALUE < 0) zlyhanie_VALUE("public static void main(String[] args) required");
        if (chyba) return 1;
        int Argumenty = vyhradiť_Úložisko(3, používateľ.인수개수() - 1);
        for (int 수 = 1; 수 < používateľ.인수개수() && !chyba; 수++) halda_VALUE[Argumenty + 1 + 수] = hostiteľ_znak(používateľ.Argumenty(수));
        rám_INDEX = 0; rám_metóda[0] = položka_bod_VALUE; rám_pozícia[0] = metóda_START[položka_bod_VALUE]; miestny_VALUE[0] = Argumenty; miestny_Typ[0] = 2;
        Vykonať_príkaz(); return chyba ? 1 : 0;
    }
}
