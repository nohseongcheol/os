// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. Súbor/operand_Vrstvy/zdroj/vetva 경계를 Vykonať_príkaz 중 검사한다. */
public final class 자바가상기계 {
    static int[] Súbor = new int[16 * 16384], dočasný_súbor = new int[16384], názov_súboru_SMS = new int[512];
    static int[] konštanta_značka = new int[8192], 상가 = new int[8192], konštanta_SECOND_VALUE = new int[8192], reťazec_zdroj = new int[8192];
    static int[] metóda_názov_SMS = new int[512], metóda_Typ = new int[512], metóda_prístup = new int[512], metóda_vlastník = new int[512];
    static int[] metóda_START = new int[512], metóda_ukončiť_hovor = new int[512], metóda_Vrstvy = new int[512], 함수지역 = new int[512];
    static int[] metóda_argument_COUNT = new int[512], metóda_argument_Typ = new int[8192], metóda_vrátiť = new int[512];
    static int[] 경계 = new int[16 * 16384];
    static int[] miestny_VALUE = new int[16384], miestny_Typ = new int[16384], operand_Vrstvy_VALUE = new int[16384], operand_Vrstvy_Typ = new int[16384];
    static int[] rám_metóda = new int[128], rám_pozícia = new int[128], rám_Vrstvy = new int[128], rám_inštrukcia = new int[128], incializovať_rám = new int[128];
    static int[] lekcia_Definícia_názov = new int[16], lekcia_Definícia_zmeniť_veľkosť = new int[16], lekcia_Definícia_nadradený = new int[16], lekcia_Definícia_Stav = new int[16], 종칸수 = new int[16], incializovať_lekcia_Definícia = new int[16];
    static int[] lekcia_rozhranie = new int[16 * 16], lekcia_rozhranie_COUNT = new int[16];
    static int[] 칸이름 = new int[512], 칸형 = new int[512], 칸주인 = new int[512], 칸권한 = new int[512], 칸위치 = new int[512], 칸값 = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] halda_VALUE = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], halda_zdroj = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], prvok_poľa = new int[32768], Store_celé_číslo = new int[256];
    static int Veľkosť, 읽기위치, metóda_COUNT, názov_triedy, rám_INDEX = -1, halda_ukončiť_hovor_pozícia = 1, vrátiť_Typ;
    static int lekcia_Definícia_COUNT, 칸수, 잡기수, 현재읽는종, 던진객체, 잠시수, displej_COUNT, Kolekcia_COUNT;
    static int v_termíne_splatnosti_vlákno, počet_vlákien = 1, položka_lekcia_Definícia;
    static int[] vlákno_rám = new int[4], vlákno_Stav = new int[4], vlákno_objekt = new int[4], vlákno_cieľ = new int[4], 가닥대기 = new int[4];
    static boolean chyba, zmeniť_požiadavka;
    static int[] zámok_vlastník = new int[32768], 잠금깊이 = new int[32768], rám_zámok = new int[128], lekcia_zámok = new int[16], lekcia_vlákno = new int[16];

    static void zlyhanie_VALUE(String Word_SMS) {
        if (chyba) return;
        int oblasť_kód = 0;
        if (자바도구.같음(Word_SMS, "ArithmeticException: / by zero")) oblasť_kód = 4;
        if (자바도구.같음(Word_SMS, "NullPointerException") || 자바도구.같음(Word_SMS, "null or invalid array")) oblasť_kód = 5;
        if (자바도구.같음(Word_SMS, "ArrayIndexOutOfBoundsException")) oblasť_kód = 7;
        if (자바도구.같음(Word_SMS, "StringIndexOutOfBoundsException")) oblasť_kód = 8;
        if (자바도구.같음(Word_SMS, "NumberFormatException")) oblasť_kód = 10;
        if (자바도구.같음(Word_SMS, "FileNotFoundException: file open failed")) oblasť_kód = 12;
        if (자바도구.같음(Word_SMS, "IOException: stream closed") || 자바도구.같음(Word_SMS, "IOException: read failed") || 자바도구.같음(Word_SMS, "IOException: write failed")) oblasť_kód = 11;
        if (자바도구.같음(Word_SMS, "ClassCastException")) oblasť_kód = 14;
        if (자바도구.같음(Word_SMS, "NegativeArraySizeException")) oblasť_kód = 15;
        if (oblasť_kód != 0 && rám_INDEX >= 0) { 예외던짐(oblasť_kód, Word_SMS); return; }
        používateľ.Zápis("JVM error: "); používateľ.Zápis(Word_SMS); používateľ.zapísať_znak_VALUE(10); chyba = true;
    }
    static boolean klip(int Spustiť_2, int dĺžka_VALUE) {
        if (Spustiť_2 < 0 || Spustiť_2 >= Súbor.length || dĺžka_VALUE < 0) return false;
        int lekcia_Definícia = Spustiť_2 / 16384;
        return Spustiť_2 % 16384 <= lekcia_Definícia_zmeniť_veľkosť[lekcia_Definícia] && dĺžka_VALUE <= lekcia_Definícia_zmeniť_veľkosť[lekcia_Definícia] - Spustiť_2 % 16384;
    }
    static int Byte_VALUE() {
        if (!klip(읽기위치, 1)) { zlyhanie_VALUE("truncated class file"); return 0; }
        return Súbor[읽기위치++];
    }
    static int 짧은수() { return Byte_VALUE() << 8 | Byte_VALUE(); }
    static int celé_číslo() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int dĺžka_VALUE) { if (!klip(읽기위치, dĺžka_VALUE)) zlyhanie_VALUE("invalid attribute size"); else 읽기위치 += dĺžka_VALUE; }
    static boolean skontrolovať_konštanta(int 수, int 종류) {
        if (수 <= 0 || 수 >= konštanta_značka.length || konštanta_značka[수] != 종류) { zlyhanie_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean SMS_rozsah(int Spustiť_2, int dĺžka_VALUE, String Word_SMS) {
        if (!klip(Spustiť_2, dĺžka_VALUE)) return false;
        int 읽는자리 = Spustiť_2, 끝 = Spustiť_2 + dĺžka_VALUE;
        for (int Loop_INDEX = 0; Loop_INDEX < Word_SMS.length(); Loop_INDEX++) {
            int bod_kódu = Word_SMS.charAt(Loop_INDEX);
            if (bod_kódu > 0 && bod_kódu < 128) { if (읽는자리 >= 끝 || Súbor[읽는자리++] != bod_kódu) return false; }
            else if (bod_kódu < 2048) {
                if (읽는자리 + 2 > 끝 || Súbor[읽는자리++] != (192 | (bod_kódu >> 6)) || Súbor[읽는자리++] != (128 | (bod_kódu & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || Súbor[읽는자리++] != (224 | (bod_kódu >> 12)) || Súbor[읽는자리++] != (128 | ((bod_kódu >> 6) & 63)) || Súbor[읽는자리++] != (128 | (bod_kódu & 63))) return false;
        }
        return 읽는자리 == 끝;
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
    static int 상번호() { int VALUE = 짧은수(); return VALUE == 0 ? 0 : 현재읽는종 * 512 + VALUE; }
    static int 명상수() { return metóda_vlastník[rám_metóda[rám_INDEX]] * 512 + 명짧(); }
    static void 속성건너() {
        int položka_COUNT = 짧은수();
        for (int 수 = 0; 수 < položka_COUNT && !chyba; 수++) { skontrolovať_konštanta(상번호(), 1); 건너(celé_číslo()); }
    }
    static int príkaz_dĺžka(int VALUE) {
        if (VALUE == 16 || VALUE == 18 || VALUE == 21 || VALUE == 25 || VALUE == 54 || VALUE == 58 || VALUE == 188) return 2;
        if (VALUE == 17 || VALUE == 19 || VALUE == 132 || VALUE >= 153 && VALUE <= 167
            || VALUE >= 178 && VALUE <= 184 || VALUE == 187 || VALUE == 189 || VALUE == 192 || VALUE == 193 || VALUE == 198 || VALUE == 199) return 3;
        if (VALUE == 185 || VALUE == 200) return 5;
        if (VALUE >= 0 && VALUE <= 8 || VALUE >= 26 && VALUE <= 29 || VALUE >= 42 && VALUE <= 46 || VALUE >= 50 && VALUE <= 53
            || VALUE >= 59 && VALUE <= 62 || VALUE >= 75 && VALUE <= 79 || VALUE >= 83 && VALUE <= 95
            || VALUE == 96 || VALUE == 100 || VALUE == 104 || VALUE == 108 || VALUE == 112 || VALUE == 116
            || VALUE == 120 || VALUE == 122 || VALUE == 124 || VALUE == 126 || VALUE == 128 || VALUE == 130
            || VALUE >= 145 && VALUE <= 147 || VALUE == 172 || VALUE == 176 || VALUE == 177 || VALUE == 190 || VALUE == 191
            || VALUE == 194 || VALUE == 195) return 1;
        return 0;
    }
    static int pozícia_celé_číslo(int 읽는자리) {
        if (!klip(읽는자리, 4)) { zlyhanie_VALUE("truncated bytecode operand"); return 0; }
        return Súbor[읽는자리] << 24 | Súbor[읽는자리 + 1] << 16 | Súbor[읽는자리 + 2] << 8 | Súbor[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int Spustiť_2, int 끝) {
        int VALUE = Súbor[읽는자리], dĺžka_VALUE = príkaz_dĺžka(VALUE);
        if (VALUE == 170 || VALUE == 171) {
            int BASE_pozícia = 읽는자리 + 1;
            while ((BASE_pozícia - Spustiť_2) % 4 != 0) BASE_pozícia++;
            if (끝 - BASE_pozícia < (VALUE == 170 ? 12 : 8)) return 0;
            int položka_COUNT_8f7753a1 = VALUE == 170 ? pozícia_celé_číslo(BASE_pozícia + 8) - pozícia_celé_číslo(BASE_pozícia + 4) + 1 : pozícia_celé_číslo(BASE_pozícia + 4);
            if (položka_COUNT_8f7753a1 < 0 || položka_COUNT_8f7753a1 > 2048) return 0;
            dĺžka_VALUE = BASE_pozícia - 읽는자리 + (VALUE == 170 ? 12 + 4 * položka_COUNT_8f7753a1 : 8 + 8 * položka_COUNT_8f7753a1);
        }
        if (VALUE == 196 && 읽는자리 + 1 < 끝) {
            int Word_údaje = Súbor[읽는자리 + 1]; dĺžka_VALUE = Word_údaje == 132 ? 6 : (Word_údaje == 21 || Word_údaje == 25 || Word_údaje == 54 || Word_údaje == 58) ? 4 : 0;
        }
        return dĺžka_VALUE > 0 && dĺžka_VALUE <= 끝 - 읽는자리 ? dĺžka_VALUE : 0;
    }
    static void skontrolovať_cieľ_VALUE(int cieľ_VALUE, int funkcia_VALUE) {
        if (cieľ_VALUE < metóda_START[funkcia_VALUE] || cieľ_VALUE >= metóda_ukončiť_hovor[funkcia_VALUE] || 경계[cieľ_VALUE] != funkcia_VALUE + 1) zlyhanie_VALUE("invalid branch target");
    }
    static void 클래스읽기(int lekcia_Definícia) {
        현재읽는종 = lekcia_Definícia; 읽기위치 = lekcia_Definícia * 16384; Veľkosť = 읽기위치 + lekcia_Definícia_zmeniť_veľkosť[lekcia_Definícia];
        if (celé_číslo() != 0xcafebabe) { zlyhanie_VALUE("not a class file"); return; }
        int 부판 = 짧은수(), verzia_VALUE = 짧은수();
        if (verzia_VALUE < 45 || verzia_VALUE > 52 || 부판 != 0) { zlyhanie_VALUE("supported class versions: 45..52, minor 0"); return; }
        int konštanta_COUNT = 짧은수(), BASE_pozícia = lekcia_Definícia * 512;
        if (konštanta_COUNT < 1 || konštanta_COUNT > 512) { zlyhanie_VALUE("constant pool limit (511)"); return; }
        for (int položka_COUNT_8f7753a1 = 1; položka_COUNT_8f7753a1 < konštanta_COUNT && !chyba; položka_COUNT_8f7753a1++) {
            int 수 = BASE_pozícia + položka_COUNT_8f7753a1, 종류 = Byte_VALUE(); konštanta_značka[수] = 종류;
            if (종류 == 1) { konštanta_SECOND_VALUE[수] = 짧은수(); 상가[수] = 읽기위치; 건너(konštanta_SECOND_VALUE[수]); }
            else if (종류 == 3) 상가[수] = celé_číslo();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[수] = 상번호(); konštanta_SECOND_VALUE[수] = 상번호(); }
            else zlyhanie_VALUE("unsupported constant type");
        }
        int povolenie_VALUE = 짧은수();
        if ((povolenie_VALUE & (0x2000 | 0x4000)) != 0) zlyhanie_VALUE("annotation/enum class unsupported");
        lekcia_Definícia_názov[lekcia_Definícia] = názov_triedy_SMS(상번호());
        lekcia_Definícia_nadradený[lekcia_Definícia] = názov_triedy_SMS(상번호());
        int rozhranie_COUNT = 짧은수(); if (rozhranie_COUNT > 16) { zlyhanie_VALUE("interface count limit"); return; }
        lekcia_rozhranie_COUNT[lekcia_Definícia] = rozhranie_COUNT;
        for (int Loop_INDEX = 0; Loop_INDEX < rozhranie_COUNT; Loop_INDEX++) lekcia_rozhranie[lekcia_Definícia * 16 + Loop_INDEX] = názov_triedy_SMS(상번호());
        int pole_COUNT = 짧은수();
        if (pole_COUNT > 512 - 칸수) { zlyhanie_VALUE("field count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < pole_COUNT && !chyba; Loop_INDEX++) {
            int Súbor_INDEX = 칸수++; 칸주인[Súbor_INDEX] = lekcia_Definícia; 칸권한[Súbor_INDEX] = 짧은수(); 칸이름[Súbor_INDEX] = 상번호(); 칸형[Súbor_INDEX] = 상번호();
            skontrolovať_konštanta(칸이름[Súbor_INDEX], 1); skontrolovať_konštanta(칸형[Súbor_INDEX], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[칸형[Súbor_INDEX]]; int oblasť_kód = 서술형(읽기위치 + konštanta_SECOND_VALUE[칸형[Súbor_INDEX]], false); 읽기위치 = 보존값;
            if ((칸권한[Súbor_INDEX] & 8) == 0) 칸위치[Súbor_INDEX] = 종칸수[lekcia_Definícia]++;
            int atribút_údaje = 짧은수();
            for (int vnútorné_pozícia = 0; vnútorné_pozícia < atribút_údaje && !chyba; vnútorné_pozícia++) {
                int názov_konštanta = 상번호(), 유효길이 = celé_číslo();
                if (Word_SMS(názov_konštanta, "ConstantValue") && 유효길이 == 2) {
                    int údaje_VALUE = 상번호();
                    if (oblasť_kód == 1 && skontrolovať_konštanta(údaje_VALUE, 3)) 칸값[Súbor_INDEX] = 상가[údaje_VALUE];
                    else if (oblasť_kód == 2 && skontrolovať_konštanta(údaje_VALUE, 8)) 칸값[Súbor_INDEX] = konštanta_SMS(상가[údaje_VALUE]);
                } else 건너(유효길이);
            }
        }
        int položka_COUNT = 짧은수();
        if (položka_COUNT > 512 - metóda_COUNT) { zlyhanie_VALUE("method count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < položka_COUNT && !chyba; Loop_INDEX++) {
            int 수 = metóda_COUNT++; metóda_vlastník[수] = lekcia_Definícia;
            metóda_prístup[수] = 짧은수(); metóda_názov_SMS[수] = 상번호(); metóda_Typ[수] = 상번호();
            skontrolovať_konštanta(metóda_názov_SMS[수], 1); 서술읽기(수);
            if ((metóda_prístup[수] & 8) == 0) {
                if (metóda_argument_COUNT[수] == 16) { zlyhanie_VALUE("too many instance method arguments"); return; }
                for (int Porovnanie_pozícia = metóda_argument_COUNT[수]; Porovnanie_pozícia > 0; Porovnanie_pozícia--) metóda_argument_Typ[수 * 16 + Porovnanie_pozícia] = metóda_argument_Typ[수 * 16 + Porovnanie_pozícia - 1];
                metóda_argument_Typ[수 * 16] = 2; metóda_argument_COUNT[수]++;
            }
            if ((metóda_prístup[수] & 0x100) != 0) zlyhanie_VALUE("user native method unsupported");
            if (Word_SMS(metóda_názov_SMS[수], "<clinit>")) incializovať_lekcia_Definícia[lekcia_Definícia] = 수 + 1;
            for (int predný_VALUE = 0; predný_VALUE < 수; predný_VALUE++) if (metóda_vlastník[predný_VALUE] == lekcia_Definícia && 같은말(metóda_názov_SMS[predný_VALUE], metóda_názov_SMS[수]) && 같은말(metóda_Typ[predný_VALUE], metóda_Typ[수])) zlyhanie_VALUE("duplicate method");
            int atribút_COUNT = 짧은수();
            for (int atribút_VALUE = 0; atribút_VALUE < atribút_COUNT && !chyba; atribút_VALUE++) {
                int Názov = 상번호(), dĺžka_VALUE = celé_číslo(), Spustiť_2 = 읽기위치;
                if (!klip(Spustiť_2, dĺžka_VALUE)) { zlyhanie_VALUE("truncated method attribute"); break; }
                if (Word_SMS(Názov, "Code")) {
                    if (metóda_START[수] != 0) zlyhanie_VALUE("duplicate Code attribute");
                    metóda_Vrstvy[수] = 짧은수(); 함수지역[수] = 짧은수(); int kód_dĺžka = celé_číslo();
                    if (metóda_Vrstvy[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < metóda_argument_COUNT[수]
                        || kód_dĺžka < 1 || kód_dĺžka > 8192) zlyhanie_VALUE("method memory limits exceeded");
                    metóda_START[수] = 읽기위치; 건너(kód_dĺžka); metóda_ukončiť_hovor[수] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { zlyhanie_VALUE("exception table limit"); return; }
                    for (int vnútorné_pozícia = 0; vnútorné_pozícia < 잡는수; vnútorné_pozícia++) {
                        int Chyba_zdroj = 잡기수++; 잡기함수[Chyba_zdroj] = 수;
                        잡기시작[Chyba_zdroj] = metóda_START[수] + 짧은수(); 잡기끝[Chyba_zdroj] = metóda_START[수] + 짧은수();
                        잡기위치[Chyba_zdroj] = metóda_START[수] + 짧은수(); int 부호값 = 상번호(); 잡기종[Chyba_zdroj] = 부호값 == 0 ? 0 : názov_triedy_SMS(부호값);
                    }
                    속성건너();
                    if (읽기위치 != Spustiť_2 + dĺžka_VALUE) zlyhanie_VALUE("Code attribute size mismatch");
                } else 건너(dĺžka_VALUE);
            }
            if ((metóda_prístup[수] & 0x400) != 0) continue;
            if (metóda_START[수] == 0) zlyhanie_VALUE("missing Code attribute");
            int 칸 = metóda_START[수];
            while (칸 < metóda_ukončiť_hovor[수] && !chyba) {
                int dĺžka_VALUE = 길이읽기(칸, metóda_START[수], metóda_ukončiť_hovor[수]);
                if (dĺžka_VALUE == 0) { zlyhanie_VALUE("unsupported or truncated bytecode"); break; }
                경계[칸] = 수 + 1; 칸 += dĺžka_VALUE;
            }
            칸 = metóda_START[수];
            while (칸 < metóda_ukončiť_hovor[수] && !chyba) {
                int VALUE = Súbor[칸];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) skontrolovať_cieľ_VALUE(칸 + (short)(Súbor[칸 + 1] << 8 | Súbor[칸 + 2]), 수);
                if (VALUE == 200) skontrolovať_cieľ_VALUE(칸 + pozícia_celé_číslo(칸 + 1), 수);
                if (VALUE == 170 || VALUE == 171) {
                    int 읽는자리 = 칸 + 1; while ((읽는자리 - metóda_START[수]) % 4 != 0) 읽는자리++;
                    skontrolovať_cieľ_VALUE(칸 + pozícia_celé_číslo(읽는자리), 수);
                    int položka_COUNT_8f7753a1 = VALUE == 170 ? pozícia_celé_číslo(읽는자리 + 8) - pozícia_celé_číslo(읽는자리 + 4) + 1 : pozícia_celé_číslo(읽는자리 + 4);
                    읽는자리 += VALUE == 170 ? 12 : 8;
                    for (int vnútorné_pozícia = 0; vnútorné_pozícia < položka_COUNT_8f7753a1; vnútorné_pozícia++) skontrolovať_cieľ_VALUE(칸 + pozícia_celé_číslo(읽는자리 + vnútorné_pozícia * (VALUE == 170 ? 4 : 8) + (VALUE == 170 ? 0 : 4)), 수);
                }
                칸 += 길이읽기(칸, metóda_START[수], metóda_ukončiť_hovor[수]);
            }
            for (int vnútorné_pozícia = 0; vnútorné_pozícia < 잡기수; vnútorné_pozícia++) if (잡기함수[vnútorné_pozícia] == 수) {
                skontrolovať_cieľ_VALUE(잡기시작[vnútorné_pozícia], 수); skontrolovať_cieľ_VALUE(잡기위치[vnútorné_pozícia], 수);
                if (잡기끝[vnútorné_pozícia] != metóda_ukončiť_hovor[수]) skontrolovať_cieľ_VALUE(잡기끝[vnútorné_pozícia], 수);
                if (잡기시작[vnútorné_pozícia] >= 잡기끝[vnútorné_pozícia]) zlyhanie_VALUE("invalid exception range");
            }
        }
        if (!chyba) 속성건너();
        if (읽기위치 != Veľkosť) zlyhanie_VALUE("extra class file data");
    }
    static int vyhradiť_Úložisko(int 종류, int dĺžka_VALUE) { return 새기억(종류, dĺžka_VALUE); }
    static boolean objekt_VALUE(int zdroj, int 종류) {
        if (!객체유효(zdroj)) return false;
        if (halda_VALUE[zdroj] != 종류) { zlyhanie_VALUE("object type mismatch"); return false; }
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
        if (vrátiť_Typ == 2) chrániť_VALUE(operand_Vrstvy_VALUE[칸]);
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
        if (rám_INDEX % 32 == 31) { zlyhanie_VALUE("call stack limit (32)"); return; }
        int Ďalej_položka = rám_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) miestny_Typ[Ďalej_položka * 128 + 수] = 0;
        for (int 수 = metóda_argument_COUNT[funkcia_VALUE] - 1; 수 >= 0; 수--) {
            miestny_VALUE[Ďalej_položka * 128 + 수] = 빼기(metóda_argument_Typ[funkcia_VALUE * 16 + 수]); miestny_Typ[Ďalej_položka * 128 + 수] = metóda_argument_Typ[funkcia_VALUE * 16 + 수];
        }
        if (chyba) return;
        rám_INDEX = Ďalej_položka; incializovať_rám[rám_INDEX] = 0; rám_metóda[rám_INDEX] = funkcia_VALUE; rám_pozícia[rám_INDEX] = metóda_START[funkcia_VALUE]; rám_Vrstvy[rám_INDEX] = 0;
    }
    static void vrátiť_KR(int Typ_VALUE) {
        if (Typ_VALUE != metóda_vrátiť[rám_metóda[rám_INDEX]]) { zlyhanie_VALUE("return type mismatch"); return; }
        int VALUE = Typ_VALUE == 0 ? 0 : 빼기(Typ_VALUE);
        if (incializovať_rám[rám_INDEX] != 0) lekcia_Definícia_Stav[incializovať_rám[rám_INDEX] - 1] = 2;
        if (rám_zámok[rám_INDEX] != 0) { vydať_zámok(rám_zámok[rám_INDEX]); rám_zámok[rám_INDEX] = 0; }
        rám_INDEX--; if (rám_INDEX >= v_termíne_splatnosti_vlákno * 32 && Typ_VALUE != 0) 넣기(VALUE, Typ_VALUE);
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
                if (VALUE < 1) { zlyhanie_VALUE("invalid file stream path"); return; }
                Stream_názov_súboru[칸] = VALUE;
            }
            Stream_názov_súboru[dĺžka_VALUE] = 0;
            int 서술자 = používateľ.파일서술자열기(Stream_názov_súboru, Výstup ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { zlyhanie_VALUE("FileNotFoundException: file open failed"); return; }
            halda_VALUE[Stream_VALUE + 2] = 서술자; halda_VALUE[Stream_VALUE + 3] = 1;
            return;
        }
        if (Príkaz != 182) { zlyhanie_VALUE("invalid file stream invocation"); return; }
        if ((Výstup && Word_SMS(Názov, "write") || !Výstup && Word_SMS(Názov, "read"))
            && (Word_SMS(formát_VALUE, Výstup ? "([B)V" : "([B)I") || Word_SMS(formát_VALUE, Výstup ? "([BII)V" : "([BII)I"))) {
            boolean klip_VALUE = Word_SMS(formát_VALUE, Výstup ? "([BII)V" : "([BII)I");
            int položka_COUNT_8f7753a1 = klip_VALUE ? 빼기(1) : 0, 시작점 = klip_VALUE ? 빼기(1) : 0, údaje_pole = 빼기(2), objekt_zdroj = 빼기(2);
            if (!objekt_VALUE(údaje_pole, 20) || !objekt_VALUE(objekt_zdroj, 종류)) return;
            if (!klip_VALUE) položka_COUNT_8f7753a1 = halda_VALUE[údaje_pole + 1];
            if (시작점 < 0 || položka_COUNT_8f7753a1 < 0 || 시작점 > halda_VALUE[údaje_pole + 1] - položka_COUNT_8f7753a1) { 예외던짐(6, "file buffer bounds"); return; }
            if (halda_VALUE[objekt_zdroj + 3] == 0 || halda_VALUE[objekt_zdroj + 2] < 0) { zlyhanie_VALUE("IOException: stream closed"); return; }
            int Dokončené_úlohy_COUNT = 0;
            while (Dokončené_úlohy_COUNT < položka_COUNT_8f7753a1 && !chyba) {
                int 반환값 = Výstup ? používateľ.파일한바이트쓰기(halda_VALUE[objekt_zdroj + 2], halda_VALUE[údaje_pole + 2 + 시작점 + Dokončené_úlohy_COUNT]) : používateľ.파일한바이트읽기(halda_VALUE[objekt_zdroj + 2]);
                if (반환값 < 0) { zlyhanie_VALUE(Výstup ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!Výstup && 반환값 == 256) break;
                if (!Výstup) halda_VALUE[údaje_pole + 2 + 시작점 + Dokončené_úlohy_COUNT] = (byte)반환값;
                Dokončené_úlohy_COUNT++;
            }
            if (!Výstup) 넣기(položka_COUNT_8f7753a1 != 0 && Dokončené_úlohy_COUNT == 0 ? -1 : Dokončené_úlohy_COUNT, 1);
            return;
        }
        if (Výstup && Word_SMS(Názov, "flush") && Word_SMS(formát_VALUE, "()V")) { int objekt_zdroj = 빼기(2); if (objekt_VALUE(objekt_zdroj, 종류) && halda_VALUE[objekt_zdroj + 2] < 0) zlyhanie_VALUE("IOException: stream closed"); return; }
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
            if (KR < -1) zlyhanie_VALUE("IOException: read failed"); else 넣기(KR == 256 ? -1 : KR, 1);
        } else if (používateľ.파일한바이트쓰기(서술자, VALUE) != 1) zlyhanie_VALUE("IOException: write failed");
    }
    static void CALL_metóda(int INDEX, int Príkaz) {
        if (INDEX <= 0 || INDEX >= konštanta_značka.length || (konštanta_značka[INDEX] != 10 && konštanta_značka[INDEX] != 11)) { zlyhanie_VALUE("invalid method reference"); return; }
        int vlastník_VALUE = názov_triedy_SMS(상가[INDEX]), Názov = zdroj_názov(konštanta_SECOND_VALUE[INDEX]), formát_VALUE = referenčný_typ(konštanta_SECOND_VALUE[INDEX]);
        if (chyba) return;
        if (기본호출(vlastník_VALUE, Názov, formát_VALUE, Príkaz)) return;
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
        int lekcia_Definícia = FIND_lekcia_Definícia(vlastník_VALUE); if (lekcia_Definícia < 0 || chyba) return;
        int Súbor_INDEX = FIND_metóda(lekcia_Definícia, Názov, formát_VALUE);
        if (Súbor_INDEX < 0) {
            for (int bod_kódu = lekcia_Definícia, položka_COUNT_8f7753a1 = 0; bod_kódu >= 0 && položka_COUNT_8f7753a1 < 16; položka_COUNT_8f7753a1++, bod_kódu = nadradený_lekcia(bod_kódu))
                if (Word_SMS(lekcia_Definícia_nadradený[bod_kódu], "java/lang/Thread")) { 가닥호출(Názov, formát_VALUE, Príkaz); return; }
            zlyhanie_VALUE("NoSuchMethodError"); return;
        }
        if (((metóda_prístup[Súbor_INDEX] & 8) != 0) != (Príkaz == 184)) { zlyhanie_VALUE("method static/instance mismatch"); return; }
        if (Príkaz == 184) { if (!incializovať(metóda_vlastník[Súbor_INDEX], rám_inštrukcia[rám_INDEX])) return; }
        else {
            int 읽는자리 = rám_Vrstvy[rám_INDEX] - metóda_argument_COUNT[Súbor_INDEX];
            if (읽는자리 < 0 || operand_Vrstvy_Typ[rám_INDEX * 128 + 읽는자리] != 2) { zlyhanie_VALUE("invalid method receiver"); return; }
            int objekt_zdroj = operand_Vrstvy_VALUE[rám_INDEX * 128 + 읽는자리];
            if (!객체유효(objekt_zdroj)) return;
            if (halda_VALUE[objekt_zdroj] < 32 || !종포함(halda_VALUE[objekt_zdroj] - 32, vlastník_VALUE)) { zlyhanie_VALUE("method receiver type mismatch"); return; }
            if (Príkaz != 183) Súbor_INDEX = FIND_metóda(halda_VALUE[objekt_zdroj] - 32, Názov, formát_VALUE);
        }
        if (Súbor_INDEX < 0 || (metóda_prístup[Súbor_INDEX] & 0x400) != 0) { zlyhanie_VALUE("AbstractMethodError"); return; }
        int zámok_zdroj = 0;
        if ((metóda_prístup[Súbor_INDEX] & 32) != 0) {
            if (Príkaz == 184) { int bod_kódu = metóda_vlastník[Súbor_INDEX]; if (lekcia_zámok[bod_kódu] == 0) lekcia_zámok[bod_kódu] = vyhradiť_Úložisko(8, 0); zámok_zdroj = lekcia_zámok[bod_kódu]; }
            else zámok_zdroj = operand_Vrstvy_VALUE[rám_INDEX * 128 + rám_Vrstvy[rám_INDEX] - metóda_argument_COUNT[Súbor_INDEX]];
            if (!잠금얻기(zámok_zdroj)) { if (!chyba) rám_pozícia[rám_INDEX] = rám_inštrukcia[rám_INDEX]; return; }
        }
        호출(Súbor_INDEX); if (!chyba) rám_zámok[rám_INDEX] = zámok_zdroj;
    }
    static boolean 배열저장가능(int pole_zdroj, int údaje_VALUE) {
        if (údaje_VALUE == 0 || prvok_poľa[pole_zdroj] == 0) return true;
        boolean 성공여부 = prvok_poľa[pole_zdroj] == -1 ? (údaje_VALUE > 0 && údaje_VALUE < halda_ukončiť_hovor_pozícia && halda_VALUE[údaje_VALUE] == 1) : 맞는객체(údaje_VALUE, prvok_poľa[pole_zdroj]);
        if (!성공여부 && !chyba) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int 배열칸(int zdroj, int dolný_index_VALUE, int Typ_VALUE) {
        if (!objekt_VALUE(zdroj, Typ_VALUE)) return 0;
        if (dolný_index_VALUE < 0 || dolný_index_VALUE >= halda_VALUE[zdroj + 1]) { zlyhanie_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return zdroj + 2 + dolný_index_VALUE;
    }
    static void Vykonať_príkaz() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (chyba) { if (던진객체 != 0) rukoväť_výnimka(); if (chyba || rám_INDEX < v_termíne_splatnosti_vlákno * 32) break; }
            if (rám_INDEX < v_termíne_splatnosti_vlákno * 32 || zmeniť_požiadavka || --조각 == 0) { if (!SWITCH_vlákno()) break; 조각 = 100; }
            if (rám_INDEX == 0 && lekcia_Definícia_Stav[položka_lekcia_Definícia] != 2 && !incializovať(položka_lekcia_Definícia, rám_pozícia[rám_INDEX])) continue;
            if (rám_INDEX == v_termíne_splatnosti_vlákno * 32 && v_termíne_splatnosti_vlákno != 0 && (metóda_prístup[rám_metóda[rám_INDEX]] & 32) != 0 && rám_zámok[rám_INDEX] == 0) {
                int objekt_zdroj = vlákno_cieľ[v_termíne_splatnosti_vlákno]; if (!잠금얻기(objekt_zdroj)) { if (chyba) break; continue; } rám_zámok[rám_INDEX] = objekt_zdroj;
            }
            잠시수 = 0;
            if (--남음 == 0) { zlyhanie_VALUE("instruction limit (500000)"); break; }
            int Spustiť_2 = rám_pozícia[rám_INDEX]; rám_inštrukcia[rám_INDEX] = Spustiť_2; int VALUE = 명바();
            if (chyba) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int 수 = metóda_vlastník[rám_metóda[rám_INDEX]] * 512 + (VALUE == 18 ? 명바() : 명짧());
                if (수 <= 0 || 수 >= konštanta_značka.length) zlyhanie_VALUE("invalid ldc constant");
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
            if (VALUE == 46 || VALUE >= 50 && VALUE <= 53) {
                int položka_pozícia = 빼기(1), objekt_zdroj = 빼기(2), oblasť_kód = VALUE == 46 ? 2 : VALUE == 50 ? 3 : VALUE == 51 ? 20 : VALUE == 52 ? 22 : 23;
                if (VALUE == 51 && objekt_zdroj > 0 && objekt_zdroj < halda_ukončiť_hovor_pozícia && halda_VALUE[objekt_zdroj] == 21) oblasť_kód = 21;
                int 읽는자리 = 배열칸(objekt_zdroj, položka_pozícia, oblasť_kód); if (!chyba) 넣기(halda_VALUE[읽는자리], VALUE == 50 ? 2 : 1); continue;
            }
            if (VALUE == 79 || VALUE >= 83 && VALUE <= 86) {
                int položka_zdroj = 빼기(VALUE == 83 ? 2 : 1), položka_pozícia = 빼기(1), objekt_zdroj = 빼기(2), oblasť_kód = VALUE == 79 ? 2 : VALUE == 83 ? 3 : VALUE == 84 ? 20 : VALUE == 85 ? 22 : 23;
                if (VALUE == 84 && objekt_zdroj > 0 && objekt_zdroj < halda_ukončiť_hovor_pozícia && halda_VALUE[objekt_zdroj] == 21) oblasť_kód = 21;
                int 읽는자리 = 배열칸(objekt_zdroj, položka_pozícia, oblasť_kód);
                if (!chyba && oblasť_kód == 3 && !배열저장가능(objekt_zdroj, položka_zdroj)) continue;
                if (!chyba) halda_VALUE[읽는자리] = oblasť_kód == 20 ? (byte)položka_zdroj : oblasť_kód == 21 ? položka_zdroj & 1 : oblasť_kód == 22 ? (char)položka_zdroj : oblasť_kód == 23 ? (short)položka_zdroj : položka_zdroj;
                continue;
            }
            if (VALUE >= 87 && VALUE <= 95) { Vrstvy_inštrukcia(VALUE); continue; }
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
            if (VALUE >= 178 && VALUE <= 181) { 필드호출(명상수(), VALUE, Spustiť_2); continue; }
            if (VALUE >= 182 && VALUE <= 185) {
                int 부호값 = 명상수();
                if (VALUE == 185) { int celkovo_COUNT = 명바(); if (celkovo_COUNT == 0 || 명바() != 0) { zlyhanie_VALUE("invalid invokeinterface operands"); continue; } }
                CALL_metóda(부호값, VALUE); continue;
            }
            if (VALUE == 187) { 새객체(názov_triedy_SMS(명상수()), Spustiť_2); continue; }
            if (VALUE == 188 || VALUE == 189) {
                int oblasť_kód = 3, súčasť = 0;
                if (VALUE == 188) { int 임시값 = 명바(); oblasť_kód = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else súčasť = názov_triedy_SMS(명상수());
                if (oblasť_kód == 0) { zlyhanie_VALUE("unsupported primitive array type"); continue; }
                int 유효길이 = 빼기(1), objekt_zdroj = vyhradiť_Úložisko(oblasť_kód, 유효길이); if (!chyba) prvok_poľa[objekt_zdroj] = súčasť; 넣기(objekt_zdroj, 2); continue;
            }
            if (VALUE == 190) {
                int objekt_zdroj = 빼기(2);
                if (객체유효(objekt_zdroj)) { int Porovnanie_pozícia = halda_VALUE[objekt_zdroj]; if (Porovnanie_pozícia != 2 && Porovnanie_pozícia != 3 && (Porovnanie_pozícia < 20 || Porovnanie_pozícia > 23)) zlyhanie_VALUE("not an array"); else 넣기(halda_VALUE[objekt_zdroj + 1], 1); }
                continue;
            }
            if (VALUE == 191) {
                int objekt_zdroj = 빼기(2); if (객체유효(objekt_zdroj)) { if (halda_VALUE[objekt_zdroj] != 9) zlyhanie_VALUE("athrow requires supported Throwable"); else { 던진객체 = objekt_zdroj; chyba = true; } }
                continue;
            }
            if (VALUE == 192 || VALUE == 193) {
                int názov_konštanta = názov_triedy_SMS(명상수()), objekt_zdroj = 빼기(2); boolean MATCH = 맞는객체(objekt_zdroj, názov_konštanta);
                if (VALUE == 193) 넣기(objekt_zdroj != 0 && MATCH ? 1 : 0, 1);
                else { if (!MATCH && !chyba) zlyhanie_VALUE("ClassCastException"); 넣기(objekt_zdroj, 2); }
                continue;
            }
            if (VALUE == 170 || VALUE == 171) {
                int 읽는자리 = Spustiť_2 + 1, Súbor_INDEX = rám_metóda[rám_INDEX], Kľúč_zdroj = 빼기(1);
                while ((읽는자리 - metóda_START[Súbor_INDEX]) % 4 != 0) 읽는자리++;
                int cieľ_adresa = pozícia_celé_číslo(읽는자리);
                if (VALUE == 170) { int 낮은값 = pozícia_celé_číslo(읽는자리 + 4), 높은값 = pozícia_celé_číslo(읽는자리 + 8); if (Kľúč_zdroj >= 낮은값 && Kľúč_zdroj <= 높은값) cieľ_adresa = pozícia_celé_číslo(읽는자리 + 12 + (Kľúč_zdroj - 낮은값) * 4); }
                else { int celkovo_COUNT = pozícia_celé_číslo(읽는자리 + 4); for (int Loop_INDEX = 0; Loop_INDEX < celkovo_COUNT; Loop_INDEX++) if (pozícia_celé_číslo(읽는자리 + 8 + Loop_INDEX * 8) == Kľúč_zdroj) cieľ_adresa = pozícia_celé_číslo(읽는자리 + 12 + Loop_INDEX * 8); }
                premiestniť_VALUE(Spustiť_2 + cieľ_adresa); continue;
            }
            if (VALUE == 200) { premiestniť_VALUE(Spustiť_2 + pozícia_celé_číslo(Spustiť_2 + 1)); continue; }
            if (VALUE == 194 || VALUE == 195) {
                int objekt_zdroj = 빼기(2);
                if (VALUE == 195) vydať_zámok(objekt_zdroj);
                else if (!잠금얻기(objekt_zdroj) && !chyba) { 넣기(objekt_zdroj, 2); rám_pozícia[rám_INDEX] = Spustiť_2; }
                continue;
            }
            if (VALUE == 196) {
                int príkaz_kód = 명바(), položka_pozícia = 명짧();
                if (príkaz_kód == 21 || príkaz_kód == 25) 지역읽기(položka_pozícia, príkaz_kód == 21 ? 1 : 2);
                else if (príkaz_kód == 54 || príkaz_kód == 58) zapísať_miestny(položka_pozícia, príkaz_kód == 54 ? 1 : 2);
                else if (príkaz_kód == 132) { int DELTA_VALUE = (short)명짧(); 지역읽기(položka_pozícia, 1); 넣기(빼기(1) + DELTA_VALUE, 1); zapísať_miestny(položka_pozícia, 1); }
                else zlyhanie_VALUE("unsupported wide opcode");
                continue;
            }
            zlyhanie_VALUE("unsupported bytecode");
        }
    }
    static int FIND_lekcia_Definícia(int Názov) {
        for (int Loop_INDEX = 0; Loop_INDEX < lekcia_Definícia_COUNT; Loop_INDEX++) if (lekcia_Definícia_názov[Loop_INDEX] != 0 && 같은말(lekcia_Definícia_názov[Loop_INDEX], Názov)) return Loop_INDEX;
        return dávka_lekcia_Definícia(konštanta_SMS(Názov));
    }
    static int dávka_lekcia_Definícia(int názov_reťazec) {
        if (!objekt_VALUE(názov_reťazec, 1)) return -1;
        int dĺžka_VALUE = halda_VALUE[názov_reťazec + 1];
        if (dĺžka_VALUE < 1 || dĺžka_VALUE > 505 || lekcia_Definícia_COUNT == 16) { zlyhanie_VALUE("class name/count limit"); return -1; }
        for (int Loop_INDEX = 0; Loop_INDEX < dĺžka_VALUE; Loop_INDEX++) { int bod_kódu = halda_VALUE[názov_reťazec + 2 + Loop_INDEX]; názov_súboru_SMS[Loop_INDEX] = bod_kódu == '/' ? '.' : bod_kódu; }
        názov_súboru_SMS[dĺžka_VALUE] = '.'; názov_súboru_SMS[dĺžka_VALUE + 1] = 'c'; názov_súboru_SMS[dĺžka_VALUE + 2] = 'l'; názov_súboru_SMS[dĺžka_VALUE + 3] = 'a'; názov_súboru_SMS[dĺžka_VALUE + 4] = 's'; názov_súboru_SMS[dĺžka_VALUE + 5] = 's'; názov_súboru_SMS[dĺžka_VALUE + 6] = 0;
        int Veľkosť = používateľ.파일읽기(názov_súboru_SMS, dočasný_súbor);
        if (Veľkosť < 0) { zlyhanie_VALUE("ClassNotFoundException"); return -1; }
        int lekcia_Definícia = lekcia_Definícia_COUNT++; lekcia_Definícia_zmeniť_veľkosť[lekcia_Definícia] = Veľkosť;
        for (int Loop_INDEX = 0; Loop_INDEX < Veľkosť; Loop_INDEX++) Súbor[lekcia_Definícia * 16384 + Loop_INDEX] = dočasný_súbor[Loop_INDEX];
        클래스읽기(lekcia_Definícia); if (chyba) return -1;
        int skutočný_údaje = konštanta_SMS(lekcia_Definícia_názov[lekcia_Definícia]);
        if (!글같음(skutočný_údaje, názov_reťazec, true)) { zlyhanie_VALUE("class name does not match file"); return -1; }
        int nadradený_VALUE = lekcia_Definícia_nadradený[lekcia_Definícia];
        if (nadradený_VALUE != 0 && !Word_SMS(nadradený_VALUE, "java/lang/Object") && !Word_SMS(nadradený_VALUE, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 skúsiť_znova_VALUE 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = FIND_lekcia_Definícia(nadradený_VALUE);
            if (chyba || 위 < 0) return -1;
            int 읽는자리 = 위, etapa_COUNT = 0;
            while (읽는자리 >= 0 && etapa_COUNT++ < 16) {
                if (읽는자리 == lekcia_Definícia) { zlyhanie_VALUE("cyclic inheritance"); return -1; }
                읽는자리 = nadradený_lekcia(읽는자리);
            }
            int 시작변위 = 종칸수[위];
            for (int Súbor_INDEX = 0; Súbor_INDEX < 칸수; Súbor_INDEX++) if (칸주인[Súbor_INDEX] == lekcia_Definícia && (칸권한[Súbor_INDEX] & 8) == 0) 칸위치[Súbor_INDEX] += 시작변위;
            종칸수[lekcia_Definícia] += 시작변위;
        }
        return lekcia_Definícia;
    }
    static int nadradený_lekcia(int lekcia_Definícia) {
        int Názov = lekcia_Definícia_nadradený[lekcia_Definícia];
        for (int Loop_INDEX = 0; Loop_INDEX < lekcia_Definícia_COUNT; Loop_INDEX++) if (Názov != 0 && lekcia_Definícia_názov[Loop_INDEX] != 0 && 같은말(lekcia_Definícia_názov[Loop_INDEX], Názov)) return Loop_INDEX;
        return -1;
    }
    static int FIND_metóda(int lekcia_Definícia, int Názov, int formát_VALUE) {
        for (int 깊이 = 0; lekcia_Definícia >= 0 && 깊이 < 16; 깊이++, lekcia_Definícia = nadradený_lekcia(lekcia_Definícia)) {
            for (int Loop_INDEX = 0; Loop_INDEX < metóda_COUNT; Loop_INDEX++) if (metóda_vlastník[Loop_INDEX] == lekcia_Definícia && 같은말(metóda_názov_SMS[Loop_INDEX], Názov) && 같은말(metóda_Typ[Loop_INDEX], formát_VALUE)) return Loop_INDEX;
        }
        return -1;
    }
    static int názov_metóda(int lekcia_Definícia, String Názov, String formát_VALUE) {
        for (int 깊이 = 0; lekcia_Definícia >= 0 && 깊이 < 16; 깊이++, lekcia_Definícia = nadradený_lekcia(lekcia_Definícia))
            for (int Loop_INDEX = 0; Loop_INDEX < metóda_COUNT; Loop_INDEX++) if (metóda_vlastník[Loop_INDEX] == lekcia_Definícia && Word_SMS(metóda_názov_SMS[Loop_INDEX], Názov) && Word_SMS(metóda_Typ[Loop_INDEX], formát_VALUE)) return Loop_INDEX;
        return -1;
    }
    static int 형종류(int Názov) { return Súbor[상가[Názov]] == 'L' || Súbor[상가[Názov]] == '[' ? 2 : 1; }
    static boolean incializovať(int lekcia_Definícia, int príkaz_START) {
        if (lekcia_Definícia < 0 || chyba) return false;
        if (lekcia_Definícia_Stav[lekcia_Definícia] == 3) { zlyhanie_VALUE("NoClassDefFoundError: initialization failed"); return false; }
        if (lekcia_Definícia_Stav[lekcia_Definícia] == 1 && lekcia_vlákno[lekcia_Definícia] != v_termíne_splatnosti_vlákno) { rám_pozícia[rám_INDEX] = príkaz_START; zmeniť_požiadavka = true; return false; }
        if (lekcia_Definícia_Stav[lekcia_Definícia] != 0) return true;
        int 위 = nadradený_lekcia(lekcia_Definícia);
        if (위 >= 0 && !incializovať(위, príkaz_START)) return false;
        lekcia_Definícia_Stav[lekcia_Definícia] = 1; lekcia_vlákno[lekcia_Definícia] = v_termíne_splatnosti_vlákno;
        if (incializovať_lekcia_Definícia[lekcia_Definícia] != 0) {
            rám_pozícia[rám_INDEX] = príkaz_START;
            호출(incializovať_lekcia_Definícia[lekcia_Definícia] - 1); if (!chyba) incializovať_rám[rám_INDEX] = lekcia_Definícia + 1;
            return false;
        }
        lekcia_Definícia_Stav[lekcia_Definícia] = 2; return true;
    }
    static void 필드호출(int INDEX, int Príkaz, int Spustiť_2) {
        if (!skontrolovať_konštanta(INDEX, 9)) return;
        int vlastník_VALUE = názov_triedy_SMS(상가[INDEX]), Názov = zdroj_názov(konštanta_SECOND_VALUE[INDEX]), formát_VALUE = referenčný_typ(konštanta_SECOND_VALUE[INDEX]);
        if (Word_SMS(vlastník_VALUE, "java/lang/System") && (Word_SMS(Názov, "out") || Word_SMS(Názov, "err")) && Word_SMS(formát_VALUE, "Ljava/io/PrintStream;") && Príkaz == 178) { 넣기(-1, 2); return; }
        int lekcia_Definícia = FIND_lekcia_Definícia(vlastník_VALUE); if (lekcia_Definícia < 0 || chyba) return;
        int 찾음 = -1;
        for (int 읽는자리 = lekcia_Definícia, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = nadradený_lekcia(읽는자리))
            for (int Súbor_INDEX = 0; Súbor_INDEX < 칸수; Súbor_INDEX++) if (칸주인[Súbor_INDEX] == 읽는자리 && 같은말(칸이름[Súbor_INDEX], Názov) && 같은말(칸형[Súbor_INDEX], formát_VALUE)) 찾음 = Súbor_INDEX;
        if (찾음 < 0) { zlyhanie_VALUE("NoSuchFieldError"); return; }
        boolean 정적 = Príkaz == 178 || Príkaz == 179;
        if (정적 != ((칸권한[찾음] & 8) != 0)) { zlyhanie_VALUE("field static/instance mismatch"); return; }
        if (정적 && !incializovať(칸주인[찾음], Spustiť_2)) return;
        int Typ_VALUE = 형종류(formát_VALUE), VALUE = 0;
        if (Príkaz == 179 || Príkaz == 181) VALUE = 빼기(Typ_VALUE);
        if (정적) { if (Príkaz == 178) 넣기(칸값[찾음], Typ_VALUE); else if (!chyba) 칸값[찾음] = VALUE; return; }
        int objekt_zdroj = 빼기(2);
        if (!객체유효(objekt_zdroj)) return;
        if (halda_VALUE[objekt_zdroj] < 32 || !종포함(halda_VALUE[objekt_zdroj] - 32, vlastník_VALUE)) { zlyhanie_VALUE("field receiver type mismatch"); return; }
        int 보관칸 = objekt_zdroj + 2 + 칸위치[찾음];
        if (Príkaz == 180) 넣기(halda_VALUE[보관칸], Typ_VALUE);
        else if (!chyba) { halda_VALUE[보관칸] = VALUE; halda_zdroj[보관칸] = Typ_VALUE == 2 ? 1 : 0; }
    }
    static boolean 종포함(int lekcia_Definícia, int Názov) {
        for (int 중첩깊이 = 0; lekcia_Definícia >= 0 && 중첩깊이 < 16; 중첩깊이++, lekcia_Definícia = nadradený_lekcia(lekcia_Definícia)) {
            if (같은말(lekcia_Definícia_názov[lekcia_Definícia], Názov) || (lekcia_Definícia_nadradený[lekcia_Definícia] != 0 && 같은말(lekcia_Definícia_nadradený[lekcia_Definícia], Názov))) return true;
            for (int vnútorné_pozícia = 0; vnútorné_pozícia < lekcia_rozhranie_COUNT[lekcia_Definícia]; vnútorné_pozícia++) if (같은말(lekcia_rozhranie[lekcia_Definícia * 16 + vnútorné_pozícia], Názov)) return true;
        }
        return false;
    }
    static boolean 글같음(int 첫값, int Byte_údaje, boolean Cesta) {
        if (첫값 == Byte_údaje) return true;
        if (첫값 <= 0 || Byte_údaje <= 0 || halda_VALUE[첫값] != 1 || halda_VALUE[Byte_údaje] != 1 || halda_VALUE[첫값 + 1] != halda_VALUE[Byte_údaje + 1]) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < halda_VALUE[첫값 + 1]; Loop_INDEX++) {
            int X_súradnica = halda_VALUE[첫값 + 2 + Loop_INDEX], Y_súradnica = halda_VALUE[Byte_údaje + 2 + Loop_INDEX];
            if (Cesta) { if (X_súradnica == '.') X_súradnica = '/'; if (Y_súradnica == '.') Y_súradnica = '/'; }
            if (X_súradnica != Y_súradnica) return false;
        }
        return true;
    }
    static boolean 객체유효(int objekt_zdroj) {
        if (objekt_zdroj == 0) { zlyhanie_VALUE("NullPointerException"); return false; }
        if (objekt_zdroj < 1 || objekt_zdroj >= halda_ukončiť_hovor_pozícia || 힙폭[objekt_zdroj] < 2 || halda_VALUE[objekt_zdroj] == 0) { zlyhanie_VALUE("invalid object reference"); return false; }
        return true;
    }
    static void chrániť_VALUE(int objekt_zdroj) {
        if (objekt_zdroj > 0 && objekt_zdroj < halda_ukončiť_hovor_pozícia && 힙폭[objekt_zdroj] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = objekt_zdroj;
    }
    static void zobraziť_VALUE_487749b8(int objekt_zdroj) {
        if (objekt_zdroj > 0 && objekt_zdroj < halda_ukončiť_hovor_pozícia && 힙폭[objekt_zdroj] >= 2 && halda_VALUE[objekt_zdroj] != 0 && 힙표시[objekt_zdroj] == 0) {
            힙표시[objekt_zdroj] = 1; 표시대기[displej_COUNT++] = objekt_zdroj;
        }
    }
    static void 수거() {
        displej_COUNT = 0; Kolekcia_COUNT++;
        for (int skontrolovať_pozícia = 1; skontrolovať_pozícia < halda_ukončiť_hovor_pozícia; skontrolovať_pozícia += 힙폭[skontrolovať_pozícia]) 힙표시[skontrolovať_pozícia] = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < reťazec_zdroj.length; Loop_INDEX++) zobraziť_VALUE_487749b8(reťazec_zdroj[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < 칸수; Loop_INDEX++) if ((칸권한[Loop_INDEX] & 8) != 0 && 형종류(칸형[Loop_INDEX]) == 2) zobraziť_VALUE_487749b8(칸값[Loop_INDEX]);
        for (int 임시값 = 0; 임시값 < počet_vlákien; 임시값++) {
            zobraziť_VALUE_487749b8(vlákno_objekt[임시값]); zobraziť_VALUE_487749b8(vlákno_cieľ[임시값]);
            int 꼭대기자리 = 임시값 == v_termíne_splatnosti_vlákno ? rám_INDEX : vlákno_rám[임시값];
            for (int Súbor_INDEX = 임시값 * 32; Súbor_INDEX <= 꼭대기자리; Súbor_INDEX++) {
                for (int vnútorné_pozícia = 0; vnútorné_pozícia < 함수지역[rám_metóda[Súbor_INDEX]]; vnútorné_pozícia++) if (miestny_Typ[Súbor_INDEX * 128 + vnútorné_pozícia] == 2) zobraziť_VALUE_487749b8(miestny_VALUE[Súbor_INDEX * 128 + vnútorné_pozícia]);
                for (int vnútorné_pozícia = 0; vnútorné_pozícia < rám_Vrstvy[Súbor_INDEX]; vnútorné_pozícia++) if (operand_Vrstvy_Typ[Súbor_INDEX * 128 + vnútorné_pozícia] == 2) zobraziť_VALUE_487749b8(operand_Vrstvy_VALUE[Súbor_INDEX * 128 + vnútorné_pozícia]);
            }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 화면참조.length; Loop_INDEX++) zobraziť_VALUE_487749b8(화면참조[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < 나중수; Loop_INDEX++) zobraziť_VALUE_487749b8(나중실행[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < Store_celé_číslo.length; Loop_INDEX++) zobraziť_VALUE_487749b8(Store_celé_číslo[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < lekcia_Definícia_COUNT; Loop_INDEX++) zobraziť_VALUE_487749b8(lekcia_zámok[Loop_INDEX]);
        for (int skontrolovať_pozícia = 1; skontrolovať_pozícia < halda_ukončiť_hovor_pozícia; skontrolovať_pozícia += 힙폭[skontrolovať_pozícia]) if (잠금깊이[skontrolovať_pozícia] > 0) zobraziť_VALUE_487749b8(skontrolovať_pozícia);
        zobraziť_VALUE_487749b8(던진객체);
        for (int Loop_INDEX = 0; Loop_INDEX < 잠시수; Loop_INDEX++) zobraziť_VALUE_487749b8(잠시참조[Loop_INDEX]);
        while (displej_COUNT > 0) {
            int objekt_zdroj = 표시대기[--displej_COUNT], oblasť_kód = halda_VALUE[objekt_zdroj];
            for (int Loop_INDEX = objekt_zdroj + 2; Loop_INDEX < objekt_zdroj + 힙폭[objekt_zdroj]; Loop_INDEX++) if (oblasť_kód == 3 || oblasť_kód == 4 || halda_zdroj[Loop_INDEX] != 0) zobraziť_VALUE_487749b8(halda_VALUE[Loop_INDEX]);
        }
        for (int skontrolovať_pozícia = 1; skontrolovať_pozícia < halda_ukončiť_hovor_pozícia; skontrolovať_pozícia += 힙폭[skontrolovať_pozícia]) if (힙표시[skontrolovať_pozícia] == 0) halda_VALUE[skontrolovať_pozícia] = 0;
        for (int skontrolovať_pozícia = 1; skontrolovať_pozícia < halda_ukončiť_hovor_pozícia; skontrolovať_pozícia += 힙폭[skontrolovať_pozícia]) if (halda_VALUE[skontrolovať_pozícia] == 0) {
            while (skontrolovať_pozícia + 힙폭[skontrolovať_pozícia] < halda_ukončiť_hovor_pozícia && halda_VALUE[skontrolovať_pozícia + 힙폭[skontrolovať_pozícia]] == 0) { int Ďalej_pozícia = skontrolovať_pozícia + 힙폭[skontrolovať_pozícia]; 힙폭[skontrolovať_pozícia] += 힙폭[Ďalej_pozícia]; 힙폭[Ďalej_pozícia] = 0; }
            if (skontrolovať_pozícia + 힙폭[skontrolovať_pozícia] == halda_ukončiť_hovor_pozícia) { halda_ukončiť_hovor_pozícia = skontrolovať_pozícia; break; }
        }
    }
    static int 새기억(int 종류, int dĺžka_VALUE) {
        if (dĺžka_VALUE < 0) { zlyhanie_VALUE("NegativeArraySizeException"); return 0; }
        if (dĺžka_VALUE > halda_VALUE.length - 3) { zlyhanie_VALUE("object heap exhausted"); return 0; }
        int 필요수 = dĺžka_VALUE + 2, objekt_zdroj = 0;
        if (필요수 <= halda_VALUE.length - halda_ukončiť_hovor_pozícia) { objekt_zdroj = halda_ukončiť_hovor_pozícia; halda_ukončiť_hovor_pozícia += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < halda_ukončiť_hovor_pozícia; 읽는자리 += 힙폭[읽는자리]) if (halda_VALUE[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { objekt_zdroj = 읽는자리; break; }
            if (objekt_zdroj != 0) {
                int 남은길이 = 힙폭[objekt_zdroj] - 필요수;
                if (남은길이 >= 2) { 힙폭[objekt_zdroj + 필요수] = 남은길이; halda_VALUE[objekt_zdroj + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= halda_VALUE.length - halda_ukončiť_hovor_pozícia) { objekt_zdroj = halda_ukončiť_hovor_pozícia; halda_ukončiť_hovor_pozícia += 필요수; }
        }
        if (objekt_zdroj == 0) { zlyhanie_VALUE("object heap exhausted"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < 필요수; Loop_INDEX++) { halda_VALUE[objekt_zdroj + Loop_INDEX] = 0; halda_zdroj[objekt_zdroj + Loop_INDEX] = 0; 힙폭[objekt_zdroj + Loop_INDEX] = 0; }
        prvok_poľa[objekt_zdroj] = 0;
        힙폭[objekt_zdroj] = 필요수; halda_VALUE[objekt_zdroj] = 종류; halda_VALUE[objekt_zdroj + 1] = dĺžka_VALUE; chrániť_VALUE(objekt_zdroj); return objekt_zdroj;
    }
    static int výnimka_lekcia(String názov_konštanta) {
        if (자바도구.같음(názov_konštanta, "java/lang/Throwable")) return 1;
        if (자바도구.같음(názov_konštanta, "java/lang/Exception")) return 2;
        if (자바도구.같음(názov_konštanta, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(názov_konštanta, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(názov_konštanta, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(názov_konštanta, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(názov_konštanta, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(názov_konštanta, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(názov_konštanta, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(názov_konštanta, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(názov_konštanta, "java/io/IOException")) return 11;
        if (자바도구.같음(názov_konštanta, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(názov_konštanta, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(názov_konštanta, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(názov_konštanta, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int výnimka_konštanta(int Názov) {
        for (int Loop_INDEX = 1; Loop_INDEX <= 41; Loop_INDEX++) if (Word_SMS(Názov, výnimka_názov(Loop_INDEX))) return Loop_INDEX;
        return 0;
    }
    static String výnimka_názov(int konto_VALUE) {
        if (konto_VALUE == 40) return "java/lang/InterruptedException";
        if (konto_VALUE == 41) return "Slovenský/vlastné/대기중단예외";
        if (konto_VALUE == 39) return "java/net/SocketException";
        if (konto_VALUE == 20) return "Slovenský/vlastné/výnimka";
        if (konto_VALUE == 21) return "Slovenský/vlastné/실행예외";
        if (konto_VALUE == 22) return "Slovenský/vlastné/vstup_a_výstup_výnimka";
        if (konto_VALUE == 23) return "Slovenský/vlastné/počkaj_TIMEOUT_výnimka";
        if (konto_VALUE == 24) return "Slovenský/vlastné/adresa_LOOKUP_výnimka";
        if (konto_VALUE == 25) return "Slovenský/vlastné/파일없음예외";
        if (konto_VALUE == 26) return "Slovenský/vlastné/통신예외";
        if (konto_VALUE == 27) return "Slovenský/vlastné/neplatné_argument_výnimka";
        if (konto_VALUE == 28) return "Slovenský/vlastné/숫자형식예외";
        if (konto_VALUE == 29) return "Slovenský/vlastné/범위예외";
        if (konto_VALUE == 30) return "Slovenský/vlastné/배열범위예외";
        if (konto_VALUE == 31) return "Slovenský/vlastné/문자열범위예외";
        if (konto_VALUE == 32) return "Slovenský/vlastné/NEPLATNÝ_zdroj_výnimka";
        if (konto_VALUE == 33) return "Slovenský/vlastné/산술예외";
        if (konto_VALUE == 34) return "Slovenský/vlastné/Stav_výnimka";
        if (konto_VALUE == 35) return "Slovenský/vlastné/Typ_vysielať_výnimka";
        if (konto_VALUE == 36) return "Slovenský/vlastné/음수배열크기예외";
        if (konto_VALUE == 37) return "Slovenský/vlastné/pole_Store_zlyhanie";
        if (konto_VALUE == 38) return "Slovenský/vlastné/vlákno_Stav_výnimka";
        if (konto_VALUE == 1) return "java/lang/Throwable"; if (konto_VALUE == 2) return "java/lang/Exception";
        if (konto_VALUE == 3) return "java/lang/RuntimeException"; if (konto_VALUE == 4) return "java/lang/ArithmeticException";
        if (konto_VALUE == 5) return "java/lang/NullPointerException"; if (konto_VALUE == 6) return "java/lang/IndexOutOfBoundsException";
        if (konto_VALUE == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (konto_VALUE == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (konto_VALUE == 9) return "java/lang/IllegalArgumentException"; if (konto_VALUE == 10) return "java/lang/NumberFormatException";
        if (konto_VALUE == 11) return "java/io/IOException"; if (konto_VALUE == 12) return "java/io/FileNotFoundException";
        if (konto_VALUE == 17) return "java/lang/ArrayStoreException";
        if (konto_VALUE == 18) return "java/net/UnknownHostException";
        if (konto_VALUE == 19) return "java/net/SocketTimeoutException";
        if (konto_VALUE == 16) return "java/lang/IllegalThreadStateException";
        if (konto_VALUE == 13) return "java/lang/IllegalStateException"; if (konto_VALUE == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int výnimka_nadradený(int konto_VALUE) {
        if (konto_VALUE == 40) return 2;
        if (konto_VALUE == 41) return 40;
        if (konto_VALUE == 39) return 11;
        if (konto_VALUE == 1) return 0;
        if (konto_VALUE == 2) return 1;
        if (konto_VALUE == 3) return 2;
        if (konto_VALUE == 4) return 3;
        if (konto_VALUE == 5) return 3;
        if (konto_VALUE == 6) return 3;
        if (konto_VALUE == 7) return 6;
        if (konto_VALUE == 8) return 6;
        if (konto_VALUE == 9) return 3;
        if (konto_VALUE == 10) return 9;
        if (konto_VALUE == 11) return 2;
        if (konto_VALUE == 12) return 11;
        if (konto_VALUE == 13) return 3;
        if (konto_VALUE == 14) return 3;
        if (konto_VALUE == 15) return 3;
        if (konto_VALUE == 16) return 9;
        if (konto_VALUE == 17) return 3;
        if (konto_VALUE == 18) return 11;
        if (konto_VALUE == 19) return 11;
        if (konto_VALUE == 20) return 2;
        if (konto_VALUE == 21) return 3;
        if (konto_VALUE == 22) return 11;
        if (konto_VALUE == 23) return 22;
        if (konto_VALUE == 24) return 22;
        if (konto_VALUE == 25) return 22;
        if (konto_VALUE == 26) return 22;
        if (konto_VALUE == 27) return 9;
        if (konto_VALUE == 28) return 27;
        if (konto_VALUE == 29) return 6;
        if (konto_VALUE == 30) return 29;
        if (konto_VALUE == 31) return 29;
        if (konto_VALUE == 32) return 5;
        if (konto_VALUE == 33) return 4;
        if (konto_VALUE == 34) return 13;
        if (konto_VALUE == 35) return 14;
        if (konto_VALUE == 36) return 15;
        if (konto_VALUE == 37) return 17;
        if (konto_VALUE == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int skutočná_hodnota, int 요구값) {
        for (int 깊이 = 0; skutočná_hodnota != 0 && 깊이 < 16; 깊이++, skutočná_hodnota = výnimka_nadradený(skutočná_hodnota))
            if (skutočná_hodnota == 요구값) return true;
        return false;
    }
    static void 예외던짐(int konto_VALUE, String 안내참조) {
        int objekt_zdroj = 새기억(9, 2); if (chyba) return;
        halda_VALUE[objekt_zdroj + 2] = konto_VALUE; halda_VALUE[objekt_zdroj + 3] = hostiteľ_znak(안내참조); halda_zdroj[objekt_zdroj + 3] = 1;
        던진객체 = objekt_zdroj; chyba = true;
    }
    static boolean 맞는객체(int objekt_zdroj, int Názov) {
        if (objekt_zdroj == 0) return true;
        if (!객체유효(objekt_zdroj)) return false;
        int oblasť_kód = halda_VALUE[objekt_zdroj];
        if (Word_SMS(Názov, "java/lang/Object")) return true;
        if (oblasť_kód >= 32) return 종포함(oblasť_kód - 32, Názov);
        if (oblasť_kód == 9) { int cieľ_adresa = výnimka_konštanta(Názov); return cieľ_adresa != 0 && 예외포함(halda_VALUE[objekt_zdroj + 2], cieľ_adresa); }
        if (oblasť_kód == 1) return Word_SMS(Názov, "java/lang/String") || Word_SMS(Názov, "java/lang/CharSequence");
        if (oblasť_kód == 4) return Word_SMS(Názov, "java/lang/StringBuilder") || Word_SMS(Názov, "java/lang/CharSequence");
        if (oblasť_kód == 10) return Word_SMS(Názov, "java/util/ArrayList") || Word_SMS(Názov, "java/util/List");
        if (oblasť_kód == 11) return Word_SMS(Názov, "java/util/HashMap") || Word_SMS(Názov, "java/util/Map");
        if (oblasť_kód == 12) return Word_SMS(Názov, "java/lang/Integer") || Word_SMS(Názov, "java/lang/Number");
        if (oblasť_kód >= 24 && oblasť_kód <= 28 && halda_VALUE[objekt_zdroj + 13] != 0) return 한국어화면종(Názov) == oblasť_kód || Word_SMS(Názov, "Slovenský/vlastné/화면구성요소");
        if (oblasť_kód >= 24 && oblasť_kód <= 28) return (한국어화면종(Názov) == 0 && 화면종(Názov) == oblasť_kód) || Word_SMS(Názov, "java/awt/Component") || Word_SMS(Názov, "java/awt/Container") || Word_SMS(Názov, "javax/swing/JComponent");
        if (oblasť_kód == 29) return Word_SMS(Názov, halda_VALUE[objekt_zdroj + 3] != 0 ? "Slovenský/vlastné/Akcia_upozornenie" : "java/awt/event/ActionEvent");
        if (oblasť_kód == 30) return Word_SMS(Názov, "java/awt/FlowLayout") || Word_SMS(Názov, "java/awt/LayoutManager");
        if (oblasť_kód == 17) return Word_SMS(Názov, "java/net/Socket");
        if (oblasť_kód == 18) return Word_SMS(Názov, "java/net/ServerSocket");
        if (oblasť_kód == 19) return Word_SMS(Názov, halda_VALUE[objekt_zdroj + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (oblasť_kód == 14) return Word_SMS(Názov, "java/net/InetAddress");
        if (oblasť_kód == 15) return Word_SMS(Názov, "java/net/DatagramSocket");
        if (oblasť_kód == 16) return Word_SMS(Názov, "java/net/DatagramPacket");
        if (oblasť_kód == 13) return Word_SMS(Názov, halda_VALUE[objekt_zdroj + 3] != 0 ? "Slovenský/vlastné/작업가닥" : "java/lang/Thread");
        if (oblasť_kód == 2) return Word_SMS(Názov, "[I"); if (oblasť_kód == 20) return Word_SMS(Názov, "[B"); if (oblasť_kód == 21) return Word_SMS(Názov, "[Z");
        if (oblasť_kód == 22) return Word_SMS(Názov, "[C"); if (oblasť_kód == 23) return Word_SMS(Názov, "[S");
        if (oblasť_kód != 3) return false;
        if (Word_SMS(Názov, "[Ljava/lang/Object;")) return true;
        int súčasť = prvok_poľa[objekt_zdroj];
        if (súčasť == -1) return Word_SMS(Názov, "[Ljava/lang/String;") || Word_SMS(Názov, "[Ljava/lang/CharSequence;");
        if (súčasť == 0) return false;
        if (배열종비교(súčasť, Názov)) return true;
        if ((Word_SMS(súčasť, "java/lang/String") || Word_SMS(súčasť, "java/lang/StringBuilder")) && Word_SMS(Názov, "[Ljava/lang/CharSequence;")) return true;
        for (int Loop_INDEX = 0; Loop_INDEX < lekcia_Definícia_COUNT; Loop_INDEX++) if (같은말(lekcia_Definícia_názov[Loop_INDEX], súčasť)) {
            for (int bod_kódu = Loop_INDEX, 중첩깊이 = 0; bod_kódu >= 0 && 중첩깊이 < 16; 중첩깊이++, bod_kódu = nadradený_lekcia(bod_kódu)) {
                if (배열종비교(lekcia_Definícia_nadradený[bod_kódu], Názov)) return true;
                for (int vnútorné_pozícia = 0; vnútorné_pozícia < lekcia_rozhranie_COUNT[bod_kódu]; vnútorné_pozícia++) if (배열종비교(lekcia_rozhranie[bod_kódu * 16 + vnútorné_pozícia], Názov)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int názov_konštanta, int 형식참조) {
        int skontrolovať_pozícia = 상가[형식참조], položka_COUNT_8f7753a1 = konštanta_SECOND_VALUE[형식참조];
        if (názov_konštanta == 0 || položka_COUNT_8f7753a1 < 4 || Súbor[skontrolovať_pozícia] != '[' || Súbor[skontrolovať_pozícia + 1] != 'L' || Súbor[skontrolovať_pozícia + položka_COUNT_8f7753a1 - 1] != ';' || konštanta_SECOND_VALUE[názov_konštanta] != položka_COUNT_8f7753a1 - 3) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < položka_COUNT_8f7753a1 - 3; Loop_INDEX++) if (Súbor[상가[názov_konštanta] + Loop_INDEX] != Súbor[skontrolovať_pozícia + 2 + Loop_INDEX]) return false;
        return true;
    }
    static void rukoväť_výnimka() {
        if (던진객체 == 0) return;
        chyba = false;
        while (rám_INDEX >= v_termíne_splatnosti_vlákno * 32) {
            int Súbor_INDEX = rám_metóda[rám_INDEX], 읽는자리 = rám_inštrukcia[rám_INDEX];
            for (int Loop_INDEX = 0; Loop_INDEX < 잡기수; Loop_INDEX++) if (잡기함수[Loop_INDEX] == Súbor_INDEX && 읽는자리 >= 잡기시작[Loop_INDEX] && 읽는자리 < 잡기끝[Loop_INDEX]
                && (잡기종[Loop_INDEX] == 0 || 맞는객체(던진객체, 잡기종[Loop_INDEX]))) {
                rám_pozícia[rám_INDEX] = 잡기위치[Loop_INDEX]; rám_Vrstvy[rám_INDEX] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (incializovať_rám[rám_INDEX] != 0) lekcia_Definícia_Stav[incializovať_rám[rám_INDEX] - 1] = 3;
            if (rám_zámok[rám_INDEX] != 0) { vydať_zámok(rám_zámok[rám_INDEX]); rám_zámok[rám_INDEX] = 0; }
            rám_INDEX--;
        }
        používateľ.Zápis("Uncaught ");
        if (halda_VALUE[던진객체] == 9) { používateľ.Zápis(výnimka_názov(halda_VALUE[던진객체 + 2])); používateľ.Zápis(": "); zapísať_SMS(halda_VALUE[던진객체 + 3]); }
        else používateľ.Zápis("user exception");
        používateľ.zapísať_znak_VALUE(10); 던진객체 = 0; chyba = true;
    }
    // 이 JVM의 operand_Vrstvy 항목은 v_termíne_splatnosti_položka category-1(int/reference)만 허용한다.
    static void Vrstvy_inštrukcia(int príkaz_kód) {
        int 첫값 = 빼기(0), 첫형식 = vrátiť_Typ;
        if (príkaz_kód == 87) return;
        if (príkaz_kód == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int Byte_údaje = 빼기(0), SECOND_formát = vrátiť_Typ;
        if (príkaz_kód == 88) return;
        if (príkaz_kód == 90) { 넣기(첫값, 첫형식); 넣기(Byte_údaje, SECOND_formát); 넣기(첫값, 첫형식); return; }
        if (príkaz_kód == 92) { 넣기(Byte_údaje, SECOND_formát); 넣기(첫값, 첫형식); 넣기(Byte_údaje, SECOND_formát); 넣기(첫값, 첫형식); return; }
        if (príkaz_kód == 95) { 넣기(첫값, 첫형식); 넣기(Byte_údaje, SECOND_formát); return; }
        int bod_kódu = 빼기(0), 셋째형식 = vrátiť_Typ;
        if (príkaz_kód == 91) { 넣기(첫값, 첫형식); 넣기(bod_kódu, 셋째형식); 넣기(Byte_údaje, SECOND_formát); 넣기(첫값, 첫형식); return; }
        if (príkaz_kód == 93) { 넣기(Byte_údaje, SECOND_formát); 넣기(첫값, 첫형식); 넣기(bod_kódu, 셋째형식); 넣기(Byte_údaje, SECOND_formát); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = vrátiť_Typ;
        넣기(Byte_údaje, SECOND_formát); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(bod_kódu, 셋째형식); 넣기(Byte_údaje, SECOND_formát); 넣기(첫값, 첫형식);
    }
    static void 새객체(int názov_konštanta, int 시작점) {
        int oblasť_kód = 0, 유효길이 = 0, výnimka_zdroj = výnimka_konštanta(názov_konštanta);
        if (Word_SMS(názov_konštanta, "java/lang/StringBuilder")) { oblasť_kód = 4; 유효길이 = 1; }
        if (Word_SMS(názov_konštanta, "java/io/FileInputStream")) { oblasť_kód = 5; 유효길이 = 2; }
        if (Word_SMS(názov_konštanta, "java/io/FileOutputStream")) { oblasť_kód = 6; 유효길이 = 2; }
        if (výnimka_zdroj != 0) { oblasť_kód = 9; 유효길이 = 2; }
        if (Word_SMS(názov_konštanta, "java/util/ArrayList")) { oblasť_kód = 10; 유효길이 = 2; }
        if (Word_SMS(názov_konštanta, "java/util/HashMap")) { oblasť_kód = 11; 유효길이 = 2; }
        if (Word_SMS(názov_konštanta, "java/lang/Integer")) { oblasť_kód = 12; 유효길이 = 1; }
        if (Word_SMS(názov_konštanta, "java/net/Socket")) { oblasť_kód = 17; 유효길이 = 5; }
        if (Word_SMS(názov_konštanta, "java/net/ServerSocket")) { oblasť_kód = 18; 유효길이 = 5; }
        if (Word_SMS(názov_konštanta, "java/net/DatagramSocket")) { oblasť_kód = 15; 유효길이 = 3; }
        if (Word_SMS(názov_konštanta, "java/net/DatagramPacket")) { oblasť_kód = 16; 유효길이 = 4; }
        if (Word_SMS(názov_konštanta, "java/lang/Thread") || Word_SMS(názov_konštanta, "Slovenský/vlastné/작업가닥")) { oblasť_kód = 13; 유효길이 = 2; }
        if (Word_SMS(názov_konštanta, "java/lang/Object")) { oblasť_kód = 8; }
        if (oblasť_kód == 0 && 화면종(názov_konštanta) != 0) { oblasť_kód = 화면종(názov_konštanta); 유효길이 = 12; }
        if (oblasť_kód == 0) {
            int bod_kódu = FIND_lekcia_Definícia(názov_konštanta); if (bod_kódu < 0 || chyba || !incializovať(bod_kódu, 시작점)) return;
            oblasť_kód = 32 + bod_kódu; 유효길이 = 종칸수[bod_kódu];
        }
        int objekt_zdroj = vyhradiť_Úložisko(oblasť_kód, 유효길이); if (chyba) return;
        if (oblasť_kód == 13 && Word_SMS(názov_konštanta, "Slovenský/vlastné/작업가닥")) halda_VALUE[objekt_zdroj + 3] = 1;
        if (oblasť_kód >= 24 && oblasť_kód <= 28 && 한국어화면종(názov_konštanta) != 0) halda_VALUE[objekt_zdroj + 13] = 1;
        if (oblasť_kód == 5 || oblasť_kód == 6 || oblasť_kód == 15 || oblasť_kód == 17 || oblasť_kód == 18) halda_VALUE[objekt_zdroj + 2] = -1;
        if (oblasť_kód == 9) halda_VALUE[objekt_zdroj + 2] = výnimka_zdroj;
        넣기(objekt_zdroj, 2);
    }
    static boolean 값같음(int 첫값, int Byte_údaje) {
        if (첫값 == Byte_údaje) return true;
        if (첫값 == 0 || Byte_údaje == 0 || 첫값 < 0 || Byte_údaje < 0 || 첫값 >= halda_ukončiť_hovor_pozícia || Byte_údaje >= halda_ukončiť_hovor_pozícia) return false;
        if (halda_VALUE[첫값] == 1 && halda_VALUE[Byte_údaje] == 1) return 글같음(첫값, Byte_údaje, false);
        return halda_VALUE[첫값] == 12 && halda_VALUE[Byte_údaje] == 12 && halda_VALUE[첫값 + 2] == halda_VALUE[Byte_údaje + 2];
    }
    static int 글조각(int objekt_zdroj, int START_pozícia, int ukončiť_hovor_pozícia) {
        if (!objekt_VALUE(objekt_zdroj, 1)) return 0;
        if (START_pozícia < 0 || ukončiť_hovor_pozícia < START_pozícia || ukončiť_hovor_pozícia > halda_VALUE[objekt_zdroj + 1]) { zlyhanie_VALUE("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = vyhradiť_Úložisko(1, ukončiť_hovor_pozícia - START_pozícia); if (chyba) return 0;
        for (int Loop_INDEX = START_pozícia; Loop_INDEX < ukončiť_hovor_pozícia; Loop_INDEX++) halda_VALUE[반환값 + 2 + Loop_INDEX - START_pozícia] = halda_VALUE[objekt_zdroj + 2 + Loop_INDEX];
        return 반환값;
    }
    static int spojiť_SMS(int 첫값, int Byte_údaje) {
        if (!objekt_VALUE(첫값, 1) || !objekt_VALUE(Byte_údaje, 1)) return 0;
        int položka_COUNT_8f7753a1 = halda_VALUE[첫값 + 1], metóda_INDEX = halda_VALUE[Byte_údaje + 1], 반환값 = vyhradiť_Úložisko(1, položka_COUNT_8f7753a1 + metóda_INDEX); if (chyba) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < položka_COUNT_8f7753a1; Loop_INDEX++) halda_VALUE[반환값 + 2 + Loop_INDEX] = halda_VALUE[첫값 + 2 + Loop_INDEX];
        for (int Loop_INDEX = 0; Loop_INDEX < metóda_INDEX; Loop_INDEX++) halda_VALUE[반환값 + 2 + položka_COUNT_8f7753a1 + Loop_INDEX] = halda_VALUE[Byte_údaje + 2 + Loop_INDEX];
        return 반환값;
    }
    static boolean 기본호출(int vlastník, int názov_konštanta, int 서술상수, int príkaz_kód) {
        if (Word_SMS(vlastník, "Slovenský/vlastné/실행인수") && príkaz_kód == 184) {
            if (Word_SMS(názov_konštanta, "položka_COUNT") && Word_SMS(서술상수, "()I")) { 넣기(používateľ.인수개수() - 1, 1); return true; }
            if (Word_SMS(názov_konštanta, "Spracovanie_textu") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= používateľ.인수개수() - 1) 예외던짐(29, "Vykonať_príkaz Argumenty 범위를 벗어났습니다");
                else 넣기(hostiteľ_znak(používateľ.Argumenty(순번 + 1)), 2);
                return true;
            }
            zlyhanie_VALUE("지원하지 않는 Slovenský Vykonať_príkaz Argumenty 호출"); return true;
        }
        if (Word_SMS(vlastník, "Slovenský/vlastné/작업가닥")) { Proces_vlákno(názov_konštanta, 서술상수, príkaz_kód, true); return true; }
        if (한국어화면소유(vlastník)) { 한국어화면호출(vlastník, názov_konštanta, 서술상수, príkaz_kód); return true; }
        if (화면소유(vlastník)) { 화면호출(vlastník, názov_konštanta, 서술상수, príkaz_kód); return true; }
        if (Word_SMS(vlastník, "java/net/Socket") || Word_SMS(vlastník, "java/net/ServerSocket") || Word_SMS(vlastník, "java/io/InputStream") || Word_SMS(vlastník, "java/io/OutputStream")) { 흐름호출(vlastník, názov_konštanta, 서술상수, príkaz_kód); return true; }
        if (Word_SMS(vlastník, "Slovenský/vlastné/jadro_VALUE") && príkaz_kód == 184) {
            if (Word_SMS(názov_konštanta, "화면너비") && Word_SMS(서술상수, "()I")) { 넣기(používateľ.화면너비(), 1); return true; }
            if (Word_SMS(názov_konštanta, "화면높이") && Word_SMS(서술상수, "()I")) { 넣기(používateľ.화면높이(), 1); return true; }
            if (Word_SMS(názov_konštanta, "밀리초") && Word_SMS(서술상수, "()I")) { 넣기(používateľ.밀리초(), 1); return true; }
            if (Word_SMS(názov_konštanta, "그림대기") && Word_SMS(서술상수, "()I")) { 넣기(používateľ.그림대기(), 1); return true; }
            if (Word_SMS(názov_konštanta, "obdĺžnik") && Word_SMS(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), výška_VALUE = 빼기(1), 너비 = 빼기(1), Y_súradnica = 빼기(1), X_súradnica = 빼기(1); 넣기(používateľ.obdĺžnik(X_súradnica, Y_súradnica, 너비, výška_VALUE, 색상), 1); return true; }
        }
        if (Word_SMS(vlastník, "java/net/InetAddress") || Word_SMS(vlastník, "java/net/DatagramPacket") || Word_SMS(vlastník, "java/net/DatagramSocket")) { 통신호출(vlastník, názov_konštanta, 서술상수, príkaz_kód); return true; }
        if (Word_SMS(vlastník, "java/lang/Thread")) { 가닥호출(názov_konštanta, 서술상수, príkaz_kód); return true; }
        if (Word_SMS(vlastník, "java/lang/Object")) {
            if (Word_SMS(názov_konštanta, "<init>") && Word_SMS(서술상수, "()V") && príkaz_kód == 183) { 객체유효(빼기(2)); return true; }
            if (Word_SMS(názov_konštanta, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int Byte_údaje = 빼기(2), 첫값 = 빼기(2); if (객체유효(첫값)) 넣기(첫값 == Byte_údaje ? 1 : 0, 1); return true; }
        }
        if (výnimka_konštanta(vlastník) != 0) {
            if (Word_SMS(názov_konštanta, "<init>") && príkaz_kód == 183 && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(Ljava/lang/String;)V"))) {
                int výzva = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), objekt_zdroj = 빼기(2);
                if (objekt_VALUE(objekt_zdroj, 9)) { halda_VALUE[objekt_zdroj + 3] = výzva; halda_zdroj[objekt_zdroj + 3] = 1; } return true;
            }
            if ((Word_SMS(názov_konštanta, "getMessage") || Word_SMS(názov_konštanta, "설명")) && Word_SMS(서술상수, "()Ljava/lang/String;")) { int objekt_zdroj = 빼기(2); if (objekt_VALUE(objekt_zdroj, 9)) 넣기(halda_VALUE[objekt_zdroj + 3], 2); return true; }
        }
        if (Word_SMS(vlastník, "java/lang/String")) {
            if (príkaz_kód == 182 && Word_SMS(názov_konštanta, "getBytes") && (Word_SMS(서술상수, "()[B") || Word_SMS(서술상수, "(Ljava/lang/String;)[B"))) {
                int kódovanie_názov = Word_SMS(서술상수, "()[B") ? 0 : 빼기(2), objekt_zdroj = 빼기(2);
                if (!objekt_VALUE(objekt_zdroj, 1)) return true;
                if (kódovanie_názov != 0 && !글같음(kódovanie_názov, hostiteľ_znak("UTF-8"), false) && !글같음(kódovanie_názov, hostiteľ_znak("UTF8"), false) && !글같음(kódovanie_názov, hostiteľ_znak("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int položka_COUNT_8f7753a1 = halda_VALUE[objekt_zdroj + 1], 반환값 = vyhradiť_Úložisko(20, položka_COUNT_8f7753a1 * 3), 사용수 = 0; if (chyba) return true;
                for (int vnútorné_pozícia = 0; vnútorné_pozícia < položka_COUNT_8f7753a1; vnútorné_pozícia++) {
                    int bod_kódu = halda_VALUE[objekt_zdroj + 2 + vnútorné_pozícia];
                    if (bod_kódu >= 0xd800 && bod_kódu <= 0xdbff && vnútorné_pozícia + 1 < položka_COUNT_8f7753a1 && halda_VALUE[objekt_zdroj + 3 + vnútorné_pozícia] >= 0xdc00 && halda_VALUE[objekt_zdroj + 3 + vnútorné_pozícia] <= 0xdfff) bod_kódu = 0x10000 + ((bod_kódu - 0xd800) << 10) + halda_VALUE[objekt_zdroj + 2 + ++vnútorné_pozícia] - 0xdc00;
                    else if (bod_kódu >= 0xd800 && bod_kódu <= 0xdfff) bod_kódu = '?';
                    if (bod_kódu < 128) halda_VALUE[반환값 + 2 + 사용수++] = bod_kódu;
                    else { int Byte_COUNT = bod_kódu < 2048 ? 2 : bod_kódu < 65536 ? 3 : 4; halda_VALUE[반환값 + 2 + 사용수++] = (byte)((Byte_COUNT == 2 ? 192 : Byte_COUNT == 3 ? 224 : 240) | bod_kódu >> (6 * (Byte_COUNT - 1))); for (int Porovnanie_pozícia = Byte_COUNT - 1; Porovnanie_pozícia > 0; Porovnanie_pozícia--) halda_VALUE[반환값 + 2 + 사용수++] = (byte)(128 | bod_kódu >> (6 * (Porovnanie_pozícia - 1)) & 63); }
                }
                halda_VALUE[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (príkaz_kód == 184 && Word_SMS(názov_konštanta, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(číslica_znak(빼기(1)), 2); return true; }
            if (príkaz_kód != 182) return false;
            if (Word_SMS(názov_konštanta, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int Byte_údaje = 빼기(2), 첫값 = 빼기(2); if (objekt_VALUE(첫값, 1)) 넣기(글같음(첫값, Byte_údaje, false) ? 1 : 0, 1); return true; }
            if (Word_SMS(názov_konštanta, "isEmpty") && Word_SMS(서술상수, "()Z")) { int 첫값 = 빼기(2); if (objekt_VALUE(첫값, 1)) 넣기(halda_VALUE[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Word_SMS(názov_konštanta, "substring") && (Word_SMS(서술상수, "(I)Ljava/lang/String;") || Word_SMS(서술상수, "(II)Ljava/lang/String;"))) {
                boolean SECOND_VALUE = Word_SMS(서술상수, "(II)Ljava/lang/String;"); int ukončiť_hovor_pozícia = SECOND_VALUE ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (objekt_VALUE(첫값, 1)) 넣기(글조각(첫값, 시작점, SECOND_VALUE ? ukončiť_hovor_pozícia : halda_VALUE[첫값 + 1]), 2); return true;
            }
            if (Word_SMS(názov_konštanta, "concat") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int Byte_údaje = 빼기(2), 첫값 = 빼기(2); 넣기(spojiť_SMS(첫값, Byte_údaje), 2); return true; }
            if (Word_SMS(názov_konštanta, "hashCode") && Word_SMS(서술상수, "()I")) { int 첫값 = 빼기(2), hodnota_hash_VALUE = 0; if (objekt_VALUE(첫값, 1)) { for (int Loop_INDEX = 0; Loop_INDEX < halda_VALUE[첫값 + 1]; Loop_INDEX++) hodnota_hash_VALUE = hodnota_hash_VALUE * 31 + halda_VALUE[첫값 + 2 + Loop_INDEX]; 넣기(hodnota_hash_VALUE, 1); } return true; }
            if (Word_SMS(názov_konštanta, "toString") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (objekt_VALUE(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Word_SMS(vlastník, "java/lang/Integer")) {
            if (príkaz_kód == 184 && Word_SMS(názov_konštanta, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/Integer;")) { int údaje_VALUE = 빼기(1), objekt_zdroj = údaje_VALUE >= -128 && údaje_VALUE <= 127 ? Store_celé_číslo[údaje_VALUE + 128] : 0; if (objekt_zdroj == 0) { objekt_zdroj = vyhradiť_Úložisko(12, 1); if (!chyba) { halda_VALUE[objekt_zdroj + 2] = údaje_VALUE; if (údaje_VALUE >= -128 && údaje_VALUE <= 127) Store_celé_číslo[údaje_VALUE + 128] = objekt_zdroj; } } 넣기(objekt_zdroj, 2); return true; }
            if (príkaz_kód == 183 && Word_SMS(názov_konštanta, "<init>") && Word_SMS(서술상수, "(I)V")) { int údaje_VALUE = 빼기(1), objekt_zdroj = 빼기(2); if (objekt_VALUE(objekt_zdroj, 12)) halda_VALUE[objekt_zdroj + 2] = údaje_VALUE; return true; }
            if (príkaz_kód == 182 && Word_SMS(názov_konštanta, "intValue") && Word_SMS(서술상수, "()I")) { int objekt_zdroj = 빼기(2); if (objekt_VALUE(objekt_zdroj, 12)) 넣기(halda_VALUE[objekt_zdroj + 2], 1); return true; }
            if (príkaz_kód == 184 && Word_SMS(názov_konštanta, "toString") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(číslica_znak(빼기(1)), 2); return true; }
        }
        if (Word_SMS(vlastník, "java/lang/Math") && príkaz_kód == 184) {
            if (Word_SMS(názov_konštanta, "abs") && Word_SMS(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((Word_SMS(názov_konštanta, "min") || Word_SMS(názov_konštanta, "max")) && Word_SMS(서술상수, "(II)I")) { int Byte_údaje = 빼기(1), 첫값 = 빼기(1); 넣기(Word_SMS(názov_konštanta, "min") ? (첫값 < Byte_údaje ? 첫값 : Byte_údaje) : (첫값 > Byte_údaje ? 첫값 : Byte_údaje), 1); return true; }
        }
        if (Word_SMS(vlastník, "java/lang/System") && príkaz_kód == 184) {
            if (Word_SMS(názov_konštanta, "gc") && Word_SMS(서술상수, "()V")) { 수거(); return true; }
            if (Word_SMS(názov_konštanta, "arraycopy") && Word_SMS(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int položka_COUNT_8f7753a1 = 빼기(1), cieľ_VALUE_INDEX = 빼기(1), Byte_údaje = 빼기(2), START_pozícia = 빼기(1), 첫값 = 빼기(2);
                if (객체유효(첫값) && 객체유효(Byte_údaje)) {
                    int oblasť_kód = halda_VALUE[첫값];
                    if (halda_VALUE[Byte_údaje] != oblasť_kód || (oblasť_kód != 2 && oblasť_kód != 3 && (oblasť_kód < 20 || oblasť_kód > 23))) zlyhanie_VALUE("arraycopy type mismatch");
                    else if (položka_COUNT_8f7753a1 < 0 || START_pozícia < 0 || cieľ_VALUE_INDEX < 0 || START_pozícia > halda_VALUE[첫값 + 1] - položka_COUNT_8f7753a1 || cieľ_VALUE_INDEX > halda_VALUE[Byte_údaje + 1] - položka_COUNT_8f7753a1) zlyhanie_VALUE("ArrayIndexOutOfBoundsException");
                    else if (첫값 == Byte_údaje && cieľ_VALUE_INDEX > START_pozícia) { for (int Loop_INDEX = položka_COUNT_8f7753a1 - 1; Loop_INDEX >= 0; Loop_INDEX--) halda_VALUE[Byte_údaje + 2 + cieľ_VALUE_INDEX + Loop_INDEX] = halda_VALUE[첫값 + 2 + START_pozícia + Loop_INDEX]; }
                    else { for (int Loop_INDEX = 0; Loop_INDEX < položka_COUNT_8f7753a1 && !chyba; Loop_INDEX++) { int údaje_VALUE = halda_VALUE[첫값 + 2 + START_pozícia + Loop_INDEX]; if (oblasť_kód != 3 || 배열저장가능(Byte_údaje, údaje_VALUE)) halda_VALUE[Byte_údaje + 2 + cieľ_VALUE_INDEX + Loop_INDEX] = údaje_VALUE; } }
                }
                return true;
            }
        }
        if (Word_SMS(vlastník, "java/util/ArrayList") || Word_SMS(vlastník, "java/util/List") || Word_SMS(vlastník, "java/util/HashMap") || Word_SMS(vlastník, "java/util/Map")) {
            모음호출(vlastník, názov_konštanta, 서술상수, príkaz_kód); return true;
        }
        return false;
    }
    static void 모음늘리기(int objekt_zdroj, int 필요수) {
        int 이전값 = halda_VALUE[objekt_zdroj + 2], kapacita_údaje = 이전값 == 0 ? 0 : halda_VALUE[이전값 + 1];
        if (kapacita_údaje >= 필요수) return;
        int Ďalej_pozícia = kapacita_údaje < 8 ? 8 : kapacita_údaje * 2; if (Ďalej_pozícia < 필요수) Ďalej_pozícia = 필요수;
        int údaje_pole = vyhradiť_Úložisko(3, Ďalej_pozícia); if (chyba) return;
        for (int Loop_INDEX = 0; Loop_INDEX < kapacita_údaje; Loop_INDEX++) halda_VALUE[údaje_pole + 2 + Loop_INDEX] = halda_VALUE[이전값 + 2 + Loop_INDEX];
        halda_VALUE[objekt_zdroj + 2] = údaje_pole; halda_zdroj[objekt_zdroj + 2] = 1;
    }
    static void 모음호출(int vlastník, int názov_konštanta, int 서술상수, int príkaz_kód) {
        boolean 대응참조 = Word_SMS(vlastník, "java/util/HashMap") || Word_SMS(vlastník, "java/util/Map"); int oblasť_kód = 대응참조 ? 11 : 10;
        if (Word_SMS(názov_konštanta, "<init>") && príkaz_kód == 183 && Word_SMS(서술상수, "()V")) { int objekt_zdroj = 빼기(2); if (objekt_VALUE(objekt_zdroj, oblasť_kód)) 모음늘리기(objekt_zdroj, 8); return; }
        if (príkaz_kód != 182 && príkaz_kód != 185) { zlyhanie_VALUE("invalid collection invocation"); return; }
        if (Word_SMS(názov_konštanta, "size") && Word_SMS(서술상수, "()I") || Word_SMS(názov_konštanta, "isEmpty") && Word_SMS(서술상수, "()Z")) {
            int objekt_zdroj = 빼기(2); if (objekt_VALUE(objekt_zdroj, oblasť_kód)) 넣기(Word_SMS(názov_konštanta, "size") ? halda_VALUE[objekt_zdroj + 3] : halda_VALUE[objekt_zdroj + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Word_SMS(názov_konštanta, "clear") && Word_SMS(서술상수, "()V")) { int objekt_zdroj = 빼기(2); if (objekt_VALUE(objekt_zdroj, oblasť_kód)) { int údaje_pole = halda_VALUE[objekt_zdroj + 2]; for (int Loop_INDEX = 0; Loop_INDEX < halda_VALUE[údaje_pole + 1]; Loop_INDEX++) halda_VALUE[údaje_pole + 2 + Loop_INDEX] = 0; halda_VALUE[objekt_zdroj + 3] = 0; } return; }
        if (!대응참조 && Word_SMS(názov_konštanta, "add") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            int údaje_VALUE = 빼기(2), objekt_zdroj = 빼기(2); if (!objekt_VALUE(objekt_zdroj, 10)) return;
            int položka_COUNT_8f7753a1 = halda_VALUE[objekt_zdroj + 3]; 모음늘리기(objekt_zdroj, položka_COUNT_8f7753a1 + 1); if (!chyba) { halda_VALUE[halda_VALUE[objekt_zdroj + 2] + 2 + položka_COUNT_8f7753a1] = údaje_VALUE; halda_VALUE[objekt_zdroj + 3] = položka_COUNT_8f7753a1 + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Word_SMS(názov_konštanta, "get") || Word_SMS(názov_konštanta, "remove")) && Word_SMS(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && Word_SMS(názov_konštanta, "set") && Word_SMS(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean Informačné_systémy_Priradený = Word_SMS(názov_konštanta, "set"); int údaje_VALUE = Informačné_systémy_Priradený ? 빼기(2) : 0, položka_pozícia = 빼기(1), objekt_zdroj = 빼기(2);
            if (!objekt_VALUE(objekt_zdroj, 10)) return;
            int položka_COUNT_8f7753a1 = halda_VALUE[objekt_zdroj + 3], údaje_pole = halda_VALUE[objekt_zdroj + 2];
            if (položka_pozícia < 0 || položka_pozícia >= položka_COUNT_8f7753a1) { 예외던짐(6, "list index"); return; }
            int 이전값 = halda_VALUE[údaje_pole + 2 + položka_pozícia];
            if (Informačné_systémy_Priradený) halda_VALUE[údaje_pole + 2 + položka_pozícia] = údaje_VALUE;
            if (Word_SMS(názov_konštanta, "remove")) { for (int Loop_INDEX = položka_pozícia + 1; Loop_INDEX < položka_COUNT_8f7753a1; Loop_INDEX++) halda_VALUE[údaje_pole + 1 + Loop_INDEX] = halda_VALUE[údaje_pole + 2 + Loop_INDEX]; halda_VALUE[údaje_pole + 1 + položka_COUNT_8f7753a1] = 0; halda_VALUE[objekt_zdroj + 3] = položka_COUNT_8f7753a1 - 1; }
            넣기(이전값, 2); return;
        }
        if (대응참조 && (Word_SMS(názov_konštanta, "get") || Word_SMS(názov_konštanta, "remove")) && Word_SMS(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(názov_konštanta, "put") && Word_SMS(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(názov_konštanta, "containsKey") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Word_SMS(názov_konštanta, "put"), odobrať = Word_SMS(názov_konštanta, "remove");
            int údaje_VALUE = 넣기여부 ? 빼기(2) : 0, Kľúč_zdroj = 빼기(2), objekt_zdroj = 빼기(2); if (!objekt_VALUE(objekt_zdroj, 11)) return;
            int položka_COUNT_8f7753a1 = halda_VALUE[objekt_zdroj + 3], údaje_pole = halda_VALUE[objekt_zdroj + 2], 찾은여부 = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < položka_COUNT_8f7753a1; Loop_INDEX++) if (값같음(Kľúč_zdroj, halda_VALUE[údaje_pole + 2 + 2 * Loop_INDEX])) { 찾은여부 = Loop_INDEX; break; }
            int 이전값 = 찾은여부 < 0 ? 0 : halda_VALUE[údaje_pole + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(objekt_zdroj, (položka_COUNT_8f7753a1 + 1) * 2); údaje_pole = halda_VALUE[objekt_zdroj + 2]; 찾은여부 = položka_COUNT_8f7753a1; if (!chyba) halda_VALUE[objekt_zdroj + 3] = položka_COUNT_8f7753a1 + 1; }
                if (!chyba) { halda_VALUE[údaje_pole + 2 + 2 * 찾은여부] = Kľúč_zdroj; halda_VALUE[údaje_pole + 3 + 2 * 찾은여부] = údaje_VALUE; }
            }
            if (odobrať && 찾은여부 >= 0) { for (int Loop_INDEX = 찾은여부 + 1; Loop_INDEX < položka_COUNT_8f7753a1; Loop_INDEX++) { halda_VALUE[údaje_pole + 2 * Loop_INDEX] = halda_VALUE[údaje_pole + 2 + 2 * Loop_INDEX]; halda_VALUE[údaje_pole + 1 + 2 * Loop_INDEX] = halda_VALUE[údaje_pole + 3 + 2 * Loop_INDEX]; } halda_VALUE[údaje_pole + 2 * položka_COUNT_8f7753a1] = 0; halda_VALUE[údaje_pole + 1 + 2 * položka_COUNT_8f7753a1] = 0; halda_VALUE[objekt_zdroj + 3] = položka_COUNT_8f7753a1 - 1; }
            if (Word_SMS(názov_konštanta, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(이전값, 2);
            return;
        }
        zlyhanie_VALUE("unsupported collection method");
    }
    static boolean 잠금얻기(int objekt_zdroj) {
        if (!객체유효(objekt_zdroj)) return false;
        if (잠금깊이[objekt_zdroj] != 0 && zámok_vlastník[objekt_zdroj] != v_termíne_splatnosti_vlákno + 1) { zmeniť_požiadavka = true; return false; }
        zámok_vlastník[objekt_zdroj] = v_termíne_splatnosti_vlákno + 1; 잠금깊이[objekt_zdroj]++; return true;
    }
    static void vydať_zámok(int objekt_zdroj) {
        if (!객체유효(objekt_zdroj)) return;
        if (잠금깊이[objekt_zdroj] == 0 || zámok_vlastník[objekt_zdroj] != v_termíne_splatnosti_vlákno + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[objekt_zdroj] == 0) zámok_vlastník[objekt_zdroj] = 0;
    }
    static boolean SWITCH_vlákno() {
        vlákno_rám[v_termíne_splatnosti_vlákno] = rám_INDEX;
        if (rám_INDEX < v_termíne_splatnosti_vlákno * 32) vlákno_Stav[v_termíne_splatnosti_vlákno] = 3;
        for (int Loop_INDEX = 0; Loop_INDEX < počet_vlákien; Loop_INDEX++) if (vlákno_Stav[Loop_INDEX] == 2 && vlákno_Stav[가닥대기[Loop_INDEX]] == 3) vlákno_Stav[Loop_INDEX] = 1;
        for (int Loop_INDEX = 1; Loop_INDEX <= počet_vlákien; Loop_INDEX++) {
            int Ďalej_pozícia = (v_termíne_splatnosti_vlákno + Loop_INDEX) % počet_vlákien;
            if (vlákno_Stav[Ďalej_pozícia] == 1) { v_termíne_splatnosti_vlákno = Ďalej_pozícia; rám_INDEX = vlákno_rám[Ďalej_pozícia]; zmeniť_požiadavka = false; return true; }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < počet_vlákien; Loop_INDEX++) if (vlákno_Stav[Loop_INDEX] != 3) { zlyhanie_VALUE("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int názov_konštanta, int 서술상수, int príkaz_kód) { Proces_vlákno(názov_konštanta, 서술상수, príkaz_kód, false); }
    static void Proces_vlákno(int názov_konštanta, int 서술상수, int príkaz_kód, boolean Slovenský) {
        if (príkaz_kód == 184 && Word_SMS(názov_konštanta, Slovenský ? "YIELD_úloha" : "yield") && Word_SMS(서술상수, "()V")) { zmeniť_požiadavka = true; return; }
        if (príkaz_kód == 184 && Word_SMS(názov_konštanta, "currentThread") && Word_SMS(서술상수, "()Ljava/lang/Thread;")) { 넣기(vlákno_objekt[v_termíne_splatnosti_vlákno], 2); return; }
        if (príkaz_kód == 183 && Word_SMS(názov_konštanta, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, Slovenský ? "(LSlovenský/vlastné/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int cieľ_adresa = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), objekt_zdroj = 빼기(2);
            if (!객체유효(objekt_zdroj)) return;
            if (halda_VALUE[objekt_zdroj] == 13) { halda_VALUE[objekt_zdroj + 2] = cieľ_adresa; halda_zdroj[objekt_zdroj + 2] = 1; }
            else if (cieľ_adresa != 0) zlyhanie_VALUE("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (príkaz_kód == 182 && (Word_SMS(názov_konštanta, Slovenský ? "START_úloha" : "start") || Word_SMS(názov_konštanta, Slovenský ? "기다리기" : "join")) && Word_SMS(서술상수, "()V") || príkaz_kód == 182 && Word_SMS(názov_konštanta, Slovenský ? "살아있는가" : "isAlive") && Word_SMS(서술상수, "()Z")) {
            int objekt_zdroj = 빼기(2); if (!객체유효(objekt_zdroj)) return;
            int konto_VALUE = -1; for (int Loop_INDEX = 0; Loop_INDEX < počet_vlákien; Loop_INDEX++) if (vlákno_objekt[Loop_INDEX] == objekt_zdroj) konto_VALUE = Loop_INDEX;
            if (Word_SMS(názov_konštanta, Slovenský ? "살아있는가" : "isAlive")) { 넣기(konto_VALUE >= 0 && vlákno_Stav[konto_VALUE] != 3 ? 1 : 0, 1); return; }
            if (Word_SMS(názov_konštanta, Slovenský ? "기다리기" : "join")) { if (konto_VALUE >= 0 && vlákno_Stav[konto_VALUE] != 3) { 가닥대기[v_termíne_splatnosti_vlákno] = konto_VALUE; vlákno_Stav[v_termíne_splatnosti_vlákno] = 2; zmeniť_požiadavka = true; } return; }
            if (konto_VALUE >= 0) { 예외던짐(Slovenský ? 38 : 16, "thread already started"); return; }
            if (počet_vlákien == 4) { zlyhanie_VALUE("thread limit (4 including main)"); return; }
            int cieľ_adresa = halda_VALUE[objekt_zdroj] == 13 ? halda_VALUE[objekt_zdroj + 2] : objekt_zdroj;
            int Súbor_INDEX = cieľ_adresa > 0 && halda_VALUE[cieľ_adresa] >= 32 ? názov_metóda(halda_VALUE[cieľ_adresa] - 32, Slovenský ? "Spustiť" : "run", "()V") : -1;
            if (cieľ_adresa != 0 && Súbor_INDEX < 0) { zlyhanie_VALUE("Runnable.run required"); return; }
            konto_VALUE = počet_vlákien++; vlákno_objekt[konto_VALUE] = objekt_zdroj; vlákno_cieľ[konto_VALUE] = cieľ_adresa;
            int rám = konto_VALUE * 32; vlákno_rám[konto_VALUE] = Súbor_INDEX < 0 ? rám - 1 : rám; vlákno_Stav[konto_VALUE] = Súbor_INDEX < 0 ? 3 : 1;
            if (Súbor_INDEX >= 0) { rám_metóda[rám] = Súbor_INDEX; rám_pozícia[rám] = metóda_START[Súbor_INDEX]; miestny_VALUE[rám * 128] = cieľ_adresa; miestny_Typ[rám * 128] = 2; }
            return;
        }
        zlyhanie_VALUE("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], adresa_SMS = new int[16];
    static int miestny_adresa() { return adresa_objekt(0x7f000001); }
    static int adresa_objekt(int VALUE) { int objekt_zdroj = vyhradiť_Úložisko(14, 1); if (!chyba) halda_VALUE[objekt_zdroj + 2] = VALUE; return objekt_zdroj; }
    static int 주소해독(int objekt_zdroj) {
        if (objekt_zdroj == 0 || 글같음(objekt_zdroj, hostiteľ_znak("localhost"), false)) return 0x7f000001;
        if (!objekt_VALUE(objekt_zdroj, 1)) return 0;
        int údaje_VALUE = 0, celkovo_COUNT = 0, adresa_Byte = 0, 자릿수 = 0, položka_COUNT_8f7753a1 = halda_VALUE[objekt_zdroj + 1];
        for (int Loop_INDEX = 0; Loop_INDEX <= položka_COUNT_8f7753a1; Loop_INDEX++) {
            int bod_kódu = Loop_INDEX == položka_COUNT_8f7753a1 ? '.' : halda_VALUE[objekt_zdroj + 2 + Loop_INDEX];
            if (bod_kódu == '.') { if (자릿수 == 0 || celkovo_COUNT == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } údaje_VALUE = údaje_VALUE << 8 | adresa_Byte; celkovo_COUNT++; adresa_Byte = 자릿수 = 0; }
            else { if (bod_kódu < '0' || bod_kódu > '9' || ++자릿수 > 3 || (adresa_Byte = adresa_Byte * 10 + bod_kódu - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (celkovo_COUNT != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return údaje_VALUE;
    }
    static int adresa_znak(int údaje_VALUE) {
        int položka_COUNT_8f7753a1 = 0;
        for (int 이동비트 = 24; 이동비트 >= 0; 이동비트 -= 8) {
            int adresa_Byte = údaje_VALUE >>> 이동비트 & 255;
            if (adresa_Byte >= 100) adresa_SMS[položka_COUNT_8f7753a1++] = '0' + adresa_Byte / 100;
            if (adresa_Byte >= 10) adresa_SMS[položka_COUNT_8f7753a1++] = '0' + adresa_Byte / 10 % 10;
            adresa_SMS[položka_COUNT_8f7753a1++] = '0' + adresa_Byte % 10; if (이동비트 != 0) adresa_SMS[položka_COUNT_8f7753a1++] = '.';
        }
        int objekt_zdroj = vyhradiť_Úložisko(1, položka_COUNT_8f7753a1); if (!chyba) for (int Loop_INDEX = 0; Loop_INDEX < položka_COUNT_8f7753a1; Loop_INDEX++) halda_VALUE[objekt_zdroj + 2 + Loop_INDEX] = adresa_SMS[Loop_INDEX]; return objekt_zdroj;
    }
    static void 통신호출(int vlastník, int názov_konštanta, int 서술상수, int príkaz_kód) {
        if (Word_SMS(vlastník, "java/net/InetAddress")) {
            if (príkaz_kód == 184 && Word_SMS(názov_konštanta, "getLoopbackAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;")) { 넣기(miestny_adresa(), 2); return; }
            if (príkaz_kód == 184 && Word_SMS(názov_konštanta, "getByName") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int údaje_VALUE = 주소해독(빼기(2)); if (던진객체 == 0 && !chyba) 넣기(adresa_objekt(údaje_VALUE), 2); return;
            }
            if (príkaz_kód == 182 && Word_SMS(názov_konštanta, "getHostAddress") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int objekt_zdroj = 빼기(2); if (objekt_VALUE(objekt_zdroj, 14)) 넣기(adresa_znak(halda_VALUE[objekt_zdroj + 2]), 2); return; }
        }
        if (Word_SMS(vlastník, "java/net/DatagramPacket")) {
            if (príkaz_kód == 183 && Word_SMS(názov_konštanta, "<init>") && (Word_SMS(서술상수, "([BI)V") || Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean cieľ_VALUE_zdroj = Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"); int číslo_portu = cieľ_VALUE_zdroj ? 빼기(1) : 0, adresa_zdroj = cieľ_VALUE_zdroj ? 빼기(2) : 0;
                int položka_COUNT_8f7753a1 = 빼기(1), údaje_pole = 빼기(2), objekt_zdroj = 빼기(2);
                if (!objekt_VALUE(objekt_zdroj, 16) || !objekt_VALUE(údaje_pole, 20)) return;
                if (položka_COUNT_8f7753a1 < 0 || položka_COUNT_8f7753a1 > halda_VALUE[údaje_pole + 1] || číslo_portu < 0 || číslo_portu > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (adresa_zdroj != 0 && !objekt_VALUE(adresa_zdroj, 14)) return;
                halda_VALUE[objekt_zdroj + 2] = údaje_pole; halda_zdroj[objekt_zdroj + 2] = 1; halda_VALUE[objekt_zdroj + 3] = položka_COUNT_8f7753a1;
                halda_VALUE[objekt_zdroj + 4] = adresa_zdroj; halda_zdroj[objekt_zdroj + 4] = 1; halda_VALUE[objekt_zdroj + 5] = číslo_portu; return;
            }
            if (príkaz_kód == 182 && Word_SMS(názov_konštanta, "setLength") && Word_SMS(서술상수, "(I)V")) {
                int položka_COUNT_8f7753a1 = 빼기(1), objekt_zdroj = 빼기(2); if (!objekt_VALUE(objekt_zdroj, 16)) return;
                if (položka_COUNT_8f7753a1 < 0 || položka_COUNT_8f7753a1 > halda_VALUE[halda_VALUE[objekt_zdroj + 2] + 1]) 예외던짐(9, "invalid datagram length"); else halda_VALUE[objekt_zdroj + 3] = položka_COUNT_8f7753a1; return;
            }
            if (príkaz_kód == 182 && (Word_SMS(názov_konštanta, "getData") && Word_SMS(서술상수, "()[B") || Word_SMS(názov_konštanta, "getLength") && Word_SMS(서술상수, "()I") || Word_SMS(názov_konštanta, "getAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;") || Word_SMS(názov_konštanta, "getPort") && Word_SMS(서술상수, "()I"))) {
                int objekt_zdroj = 빼기(2); if (!objekt_VALUE(objekt_zdroj, 16)) return;
                int položka_pozícia = Word_SMS(názov_konštanta, "getData") ? 2 : Word_SMS(názov_konštanta, "getLength") ? 3 : Word_SMS(názov_konštanta, "getAddress") ? 4 : 5;
                넣기(halda_VALUE[objekt_zdroj + položka_pozícia], položka_pozícia == 2 || položka_pozícia == 4 ? 2 : 1); return;
            }
        }
        if (Word_SMS(vlastník, "java/net/DatagramSocket")) {
            if (príkaz_kód == 183 && Word_SMS(názov_konštanta, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(I)V"))) {
                int číslo_portu = Word_SMS(서술상수, "()V") ? 0 : 빼기(1), objekt_zdroj = 빼기(2); if (!objekt_VALUE(objekt_zdroj, 15)) return;
                if (číslo_portu < 0 || číslo_portu > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = používateľ.otvoriť_sieť(číslo_portu); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else halda_VALUE[objekt_zdroj + 2] = 열린파일번호; return;
            }
            if (príkaz_kód == 182 && Word_SMS(názov_konštanta, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), objekt_zdroj = 빼기(2); if (!objekt_VALUE(objekt_zdroj, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else halda_VALUE[objekt_zdroj + 3] = 밀리초값; return;
            }
            if (príkaz_kód == 182 && Word_SMS(názov_konštanta, "getLocalPort") && Word_SMS(서술상수, "()I")) { int objekt_zdroj = 빼기(2); if (objekt_VALUE(objekt_zdroj, 15)) 넣기(halda_VALUE[objekt_zdroj + 2] < 0 ? -1 : používateľ.sieť_port(halda_VALUE[objekt_zdroj + 2]), 1); return; }
            if (príkaz_kód == 182 && Word_SMS(názov_konštanta, "isClosed") && Word_SMS(서술상수, "()Z")) { int objekt_zdroj = 빼기(2); if (objekt_VALUE(objekt_zdroj, 15)) 넣기(halda_VALUE[objekt_zdroj + 2] < 0 ? 1 : 0, 1); return; }
            if (príkaz_kód == 182 && Word_SMS(názov_konštanta, "close") && Word_SMS(서술상수, "()V")) { int objekt_zdroj = 빼기(2); if (objekt_VALUE(objekt_zdroj, 15) && halda_VALUE[objekt_zdroj + 2] >= 0) { používateľ.파일서술자닫기(halda_VALUE[objekt_zdroj + 2]); halda_VALUE[objekt_zdroj + 2] = -1; } return; }
            if (príkaz_kód == 182 && (Word_SMS(názov_konštanta, "send") || Word_SMS(názov_konštanta, "receive")) && Word_SMS(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int paket = 빼기(2), objekt_zdroj = 빼기(2); if (!objekt_VALUE(paket, 16) || !objekt_VALUE(objekt_zdroj, 15)) return;
                int údaje_pole = halda_VALUE[paket + 2], 유효길이 = halda_VALUE[paket + 3], 열린파일번호 = halda_VALUE[objekt_zdroj + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Word_SMS(názov_konštanta, "send")) {
                    if (!objekt_VALUE(halda_VALUE[paket + 4], 14)) return;
                    if (유효길이 > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < 유효길이; Loop_INDEX++) 통신임시[Loop_INDEX] = halda_VALUE[údaje_pole + 2 + Loop_INDEX];
                    if (používateľ.odoslať_sieť(열린파일번호, halda_VALUE[halda_VALUE[paket + 4] + 2], halda_VALUE[paket + 5], 통신임시, 유효길이) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int položka_COUNT_8f7753a1 = používateľ.dostať_sieť(열린파일번호, 통신임시, 유효길이 > 512 ? 512 : 유효길이);
                    if (položka_COUNT_8f7753a1 == -11) {
                        int v_termíne_splatnosti_čas = používateľ.밀리초();
                        if (halda_VALUE[objekt_zdroj + 4] == 0) halda_VALUE[objekt_zdroj + 4] = v_termíne_splatnosti_čas + 1;
                        if (halda_VALUE[objekt_zdroj + 3] > 0 && v_termíne_splatnosti_čas - (halda_VALUE[objekt_zdroj + 4] - 1) >= halda_VALUE[objekt_zdroj + 3]) { halda_VALUE[objekt_zdroj + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(objekt_zdroj, 2); 넣기(paket, 2); rám_pozícia[rám_INDEX] = rám_inštrukcia[rám_INDEX]; zmeniť_požiadavka = true; return;
                    }
                    halda_VALUE[objekt_zdroj + 4] = 0;
                    if (položka_COUNT_8f7753a1 < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < položka_COUNT_8f7753a1; Loop_INDEX++) halda_VALUE[údaje_pole + 2 + Loop_INDEX] = (byte)통신임시[Loop_INDEX];
                    halda_VALUE[paket + 3] = položka_COUNT_8f7753a1; halda_VALUE[paket + 4] = adresa_objekt(통신임시[513]); halda_zdroj[paket + 4] = 1; halda_VALUE[paket + 5] = 통신임시[512];
                }
                return;
            }
        }
        zlyhanie_VALUE("unsupported java.net method");
    }
    static boolean 흐름대기(int objekt_zdroj) {
        int v_termíne_splatnosti_čas = používateľ.밀리초();
        if (halda_VALUE[objekt_zdroj + 5] == 0) halda_VALUE[objekt_zdroj + 5] = v_termíne_splatnosti_čas + 1;
        if (halda_VALUE[objekt_zdroj + 3] > 0 && v_termíne_splatnosti_čas - (halda_VALUE[objekt_zdroj + 5] - 1) >= halda_VALUE[objekt_zdroj + 3]) { halda_VALUE[objekt_zdroj + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        rám_pozícia[rám_INDEX] = rám_inštrukcia[rám_INDEX]; zmeniť_požiadavka = true; return true;
    }
    static void 흐름호출(int vlastník, int názov_konštanta, int 서술상수, int príkaz_kód) {
        boolean dostať_strana = Word_SMS(vlastník, "java/net/ServerSocket"), Stream = Word_SMS(vlastník, "java/io/InputStream") || Word_SMS(vlastník, "java/io/OutputStream");
        if (!Stream && príkaz_kód == 183 && Word_SMS(názov_konštanta, "<init>")) {
            boolean Informačné_systémy_prázdny_Stav = Word_SMS(서술상수, "()V"), 이름지정여부 = Word_SMS(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = Word_SMS(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(Informačné_systémy_prázdny_Stav || dostať_strana && Word_SMS(서술상수, "(I)V") || !dostať_strana && (이름지정여부 || 주소지정여부))) { zlyhanie_VALUE("unsupported socket constructor"); return; }
            int číslo_portu = Informačné_systémy_prázdny_Stav ? 0 : 빼기(1), adresa_zdroj = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, objekt_zdroj = 빼기(2);
            if (!objekt_VALUE(objekt_zdroj, dostať_strana ? 18 : 17)) return;
            if (číslo_portu < 0 || číslo_portu > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !objekt_VALUE(adresa_zdroj, 14)) return;
            int sieťová_identifikácia = 이름지정여부 ? 주소해독(adresa_zdroj) : 주소지정여부 ? halda_VALUE[adresa_zdroj + 2] : 0x7f000001;
            if (chyba || 던진객체 != 0) return;
            int 열린파일번호 = používateľ.Stream_riadenie(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = Informačné_systémy_prázdny_Stav ? 0 : dostať_strana ? používateľ.Stream_riadenie(1, 열린파일번호, číslo_portu) : používateľ.spojiť_Stream(열린파일번호, sieťová_identifikácia, číslo_portu);
            if (처리값 < 0) { používateľ.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            halda_VALUE[objekt_zdroj + 2] = 열린파일번호; halda_VALUE[objekt_zdroj + 4] = číslo_portu; halda_VALUE[objekt_zdroj + 6] = Informačné_systémy_prázdny_Stav ? 0 : 1; return;
        }
        if (!Stream && Word_SMS(názov_konštanta, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), objekt_zdroj = 빼기(2); if (!objekt_VALUE(objekt_zdroj, dostať_strana ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else halda_VALUE[objekt_zdroj + 3] = 밀리초값; return; }
        if (!Stream && Word_SMS(názov_konštanta, "close") && Word_SMS(서술상수, "()V")) { int objekt_zdroj = 빼기(2); if (objekt_VALUE(objekt_zdroj, dostať_strana ? 18 : 17) && halda_VALUE[objekt_zdroj + 2] >= 0) { používateľ.파일서술자닫기(halda_VALUE[objekt_zdroj + 2]); halda_VALUE[objekt_zdroj + 2] = -1; } return; }
        if (!Stream && (Word_SMS(názov_konštanta, "getLocalPort") || Word_SMS(názov_konštanta, "getPort") || Word_SMS(názov_konštanta, "isClosed") || Word_SMS(názov_konštanta, "isConnected"))) {
            int objekt_zdroj = 빼기(2); if (!objekt_VALUE(objekt_zdroj, dostať_strana ? 18 : 17)) return;
            넣기(Word_SMS(názov_konštanta, "isClosed") ? halda_VALUE[objekt_zdroj + 2] < 0 ? 1 : 0 : Word_SMS(názov_konštanta, "isConnected") ? halda_VALUE[objekt_zdroj + 6] : Word_SMS(názov_konštanta, "getPort") ? halda_VALUE[objekt_zdroj + 4] : halda_VALUE[objekt_zdroj + 2] < 0 ? -1 : používateľ.Stream_riadenie(4, halda_VALUE[objekt_zdroj + 2], 0), 1); return;
        }
        if (dostať_strana && Word_SMS(názov_konštanta, "accept") && Word_SMS(서술상수, "()Ljava/net/Socket;")) {
            int objekt_zdroj = 빼기(2); if (!objekt_VALUE(objekt_zdroj, 18)) return; int 열린파일번호 = používateľ.Stream_riadenie(3, halda_VALUE[objekt_zdroj + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(objekt_zdroj)) 넣기(objekt_zdroj, 2); return; }
            halda_VALUE[objekt_zdroj + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = vyhradiť_Úložisko(17, 5); if (chyba) { používateľ.파일서술자닫기(열린파일번호); return; } halda_VALUE[반환값 + 2] = 열린파일번호; halda_VALUE[반환값 + 4] = používateľ.Stream_riadenie(5, 열린파일번호, 0); halda_VALUE[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!dostať_strana && !Stream && ((Word_SMS(názov_konštanta, "getInputStream") && Word_SMS(서술상수, "()Ljava/io/InputStream;")) || (Word_SMS(názov_konštanta, "getOutputStream") && Word_SMS(서술상수, "()Ljava/io/OutputStream;")))) {
            int objekt_zdroj = 빼기(2); if (!objekt_VALUE(objekt_zdroj, 17)) return; if (halda_VALUE[objekt_zdroj + 2] < 0 || halda_VALUE[objekt_zdroj + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = vyhradiť_Úložisko(19, 4); if (chyba) return; halda_VALUE[반환값 + 2] = objekt_zdroj; halda_zdroj[반환값 + 2] = 1; halda_VALUE[반환값 + 3] = Word_SMS(názov_konštanta, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (Stream) {
            boolean 읽기여부 = Word_SMS(názov_konštanta, "read"), Informačné_systémy_zapísať_operácia = Word_SMS(názov_konštanta, "write"), blok = Word_SMS(서술상수, "([B)I") || Word_SMS(서술상수, "([B)V"), Informačné_systémy_SUBARRAY = Word_SMS(서술상수, "([BII)I") || Word_SMS(서술상수, "([BII)V");
            int položka_COUNT_8f7753a1 = Informačné_systémy_SUBARRAY ? 빼기(1) : 0, 시작변위 = Informačné_systémy_SUBARRAY ? 빼기(1) : 0, údaje_pole = blok || Informačné_systémy_SUBARRAY ? 빼기(2) : 0;
            int údaje_VALUE = Informačné_systémy_zapísať_operácia && Word_SMS(서술상수, "(I)V") ? 빼기(1) : 0, objekt_zdroj = 빼기(2);
            if (!objekt_VALUE(objekt_zdroj, 19)) return; int nadradený_zdroj = halda_VALUE[objekt_zdroj + 2], 열린파일번호 = halda_VALUE[nadradený_zdroj + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Word_SMS(názov_konštanta, "close") && Word_SMS(서술상수, "()V")) { používateľ.파일서술자닫기(열린파일번호); halda_VALUE[nadradený_zdroj + 2] = -1; return; }
            if (Word_SMS(názov_konštanta, "flush") && Word_SMS(서술상수, "()V")) return;
            if ((!읽기여부 && !Informačné_systémy_zapísať_operácia) || 읽기여부 != (halda_VALUE[objekt_zdroj + 3] == 0)) { zlyhanie_VALUE("unsupported stream operation"); return; }
            if (blok || Informačné_systémy_SUBARRAY) { if (!objekt_VALUE(údaje_pole, 20)) return; if (blok) položka_COUNT_8f7753a1 = halda_VALUE[údaje_pole + 1]; if (시작변위 < 0 || položka_COUNT_8f7753a1 < 0 || 시작변위 > halda_VALUE[údaje_pole + 1] - položka_COUNT_8f7753a1) { 예외던짐(6, "stream array bounds"); return; } }
            else položka_COUNT_8f7753a1 = 1;
            if (položka_COUNT_8f7753a1 == 0) { if (읽기여부) 넣기(0, 1); return; }
            int Dokončené_úlohy_COUNT = Informačné_systémy_zapísať_operácia ? halda_VALUE[objekt_zdroj + 4] : 0, 처리값 = 0;
            while (Dokončené_úlohy_COUNT < položka_COUNT_8f7753a1) {
                처리값 = 읽기여부 ? používateľ.파일한바이트읽기(열린파일번호) : používateľ.파일한바이트쓰기(열린파일번호, blok || Informačné_systémy_SUBARRAY ? halda_VALUE[údaje_pole + 2 + 시작변위 + Dokončené_úlohy_COUNT] : údaje_VALUE);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (blok || Informačné_systémy_SUBARRAY)) halda_VALUE[údaje_pole + 2 + 시작변위 + Dokončené_úlohy_COUNT] = (byte)처리값;
                Dokončené_úlohy_COUNT++; if (읽기여부 && !(blok || Informačné_systémy_SUBARRAY)) break;
            }
            if (처리값 == -11 && (Informačné_systémy_zapísať_operácia || Dokončené_úlohy_COUNT == 0)) {
                halda_VALUE[objekt_zdroj + 4] = Dokončené_úlohy_COUNT;
                if (흐름대기(nadradený_zdroj)) { 넣기(objekt_zdroj, 2); if (blok || Informačné_systémy_SUBARRAY) 넣기(údaje_pole, 2); if (Informačné_systémy_SUBARRAY) { 넣기(시작변위, 1); 넣기(položka_COUNT_8f7753a1, 1); } if (Informačné_systémy_zapísať_operácia && !(blok || Informačné_systémy_SUBARRAY)) 넣기(údaje_VALUE, 1); } return;
            }
            halda_VALUE[objekt_zdroj + 4] = 0; halda_VALUE[nadradený_zdroj + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(Dokončené_úlohy_COUNT == 0 && 처리값 == 256 ? -1 : blok || Informačné_systémy_SUBARRAY ? Dokončené_úlohy_COUNT : 처리값, 1); return;
        }
        zlyhanie_VALUE("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int názov_konštanta) {
        if (Word_SMS(názov_konštanta, "Slovenský/vlastné/Okno")) return 24;
        if (Word_SMS(názov_konštanta, "Slovenský/vlastné/Nápis")) return 26;
        if (Word_SMS(názov_konštanta, "Slovenský/vlastné/Tlačidlo")) return 27;
        if (Word_SMS(názov_konštanta, "Slovenský/vlastné/textové_pole")) return 28;
        if (Word_SMS(názov_konštanta, "Slovenský/vlastné/Akcia_upozornenie")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int názov_konštanta) {
        return 한국어화면종(názov_konštanta) != 0 || Word_SMS(názov_konštanta, "Slovenský/vlastné/화면구성요소") || Word_SMS(názov_konštanta, "Slovenský/vlastné/udalosť_front");
    }
    static int 화면종(int názov_konštanta) {
        int 한국어종 = 한국어화면종(názov_konštanta); if (한국어종 != 0) return 한국어종;
        if (Word_SMS(názov_konštanta, "javax/swing/JFrame")) return 24;
        if (Word_SMS(názov_konštanta, "javax/swing/JPanel")) return 25;
        if (Word_SMS(názov_konštanta, "javax/swing/JLabel")) return 26;
        if (Word_SMS(názov_konštanta, "javax/swing/JButton")) return 27;
        if (Word_SMS(názov_konštanta, "javax/swing/JTextField")) return 28;
        if (Word_SMS(názov_konštanta, "java/awt/event/ActionEvent")) return 29;
        if (Word_SMS(názov_konštanta, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int názov_konštanta) {
        return 화면종(názov_konštanta) != 0 || Word_SMS(názov_konštanta, "java/awt/Component") || Word_SMS(názov_konštanta, "java/awt/Container") || Word_SMS(názov_konštanta, "javax/swing/JComponent") || Word_SMS(názov_konštanta, "javax/swing/AbstractButton") || Word_SMS(názov_konštanta, "javax/swing/text/JTextComponent") || Word_SMS(názov_konštanta, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int objekt_zdroj) { if (!객체유효(objekt_zdroj)) return false; if (halda_VALUE[objekt_zdroj] < 24 || halda_VALUE[objekt_zdroj] > 28) { zlyhanie_VALUE("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int objekt_zdroj, int SMS_zdroj) {
        if (SMS_zdroj != 0 && !objekt_VALUE(SMS_zdroj, 1)) return;
        int položka_COUNT_8f7753a1 = SMS_zdroj == 0 ? 0 : halda_VALUE[SMS_zdroj + 1]; if (položka_COUNT_8f7753a1 > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < položka_COUNT_8f7753a1; Loop_INDEX++) 화면글임시[Loop_INDEX] = halda_VALUE[SMS_zdroj + 2 + Loop_INDEX];
        if (používateľ.화면글(halda_VALUE[objekt_zdroj + 2], 화면글임시, položka_COUNT_8f7753a1) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        halda_VALUE[objekt_zdroj + 3] = SMS_zdroj; halda_zdroj[objekt_zdroj + 3] = 1;
    }
    static int 화면문자읽기(int objekt_zdroj) {
        int konto_VALUE = halda_VALUE[objekt_zdroj + 2], položka_COUNT_8f7753a1 = používateľ.화면연결(8, konto_VALUE, 0, 0, 0, 0), 사용수 = 0;
        if (položka_COUNT_8f7753a1 < 0) { zlyhanie_VALUE("GUI text read failed"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < položka_COUNT_8f7753a1; Loop_INDEX++) { int 부호값 = používateľ.화면연결(9, konto_VALUE, Loop_INDEX, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = vyhradiť_Úložisko(1, 사용수); if (!chyba) for (int Loop_INDEX = 0; Loop_INDEX < 사용수; Loop_INDEX++) halda_VALUE[반환값 + 2 + Loop_INDEX] = 화면글임시[Loop_INDEX]; return 반환값;
    }
    /* Slovenský 객체를 직접 만들고 jadro_VALUE 화면 기능에 연결한다. Swing objekt_VALUE/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int vlastník, int názov_konštanta, int 서술상수, int príkaz_kód) {
        if (Word_SMS(vlastník, "Slovenský/vlastné/udalosť_front")) {
            if (príkaz_kód == 184 && Word_SMS(názov_konštanta, "나중에실행") && Word_SMS(서술상수, "(LSlovenský/vlastné/실행할일;)V")) {
                int úloha_Akcia = 빼기(2); if (!객체유효(úloha_Akcia)) return;
                if (나중수 == 8) { zlyhanie_VALUE("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = úloha_Akcia; return;
            }
            if (príkaz_kód == 184 && Word_SMS(názov_konštanta, "사건처리중인가") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            zlyhanie_VALUE("지원하지 않는 Slovenský 화면 일정 호출"); return;
        }
        if (Word_SMS(vlastník, "Slovenský/vlastné/Akcia_upozornenie")) {
            int upozornenie = 빼기(2); if (!objekt_VALUE(upozornenie, 29) || halda_VALUE[upozornenie + 3] == 0) return;
            if (Word_SMS(názov_konštanta, "zdroj_udalosti") && Word_SMS(서술상수, "()LSlovenský/vlastné/화면구성요소;")) 넣기(halda_VALUE[upozornenie + 2], 2);
            else if (Word_SMS(názov_konštanta, "príkaz_SMS") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(halda_VALUE[upozornenie + 2]), 2);
            else if (Word_SMS(názov_konštanta, "INDEX") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else zlyhanie_VALUE("지원하지 않는 Slovenský Akcia upozornenie 호출"); return;
        }
        if (príkaz_kód == 183 && Word_SMS(názov_konštanta, "<init>")) {
            int 종류 = 한국어화면종(vlastník), 받이 = 0, 가로 = 0, vertikála_pozícia = 0, 폭 = 0, výška_VALUE = 0;
            if (종류 == 24 && Word_SMS(서술상수, "(Ljava/lang/String;II)V")) {
                výška_VALUE = 빼기(1); 폭 = 빼기(1); 가로 = (používateľ.화면너비() - 폭) / 2; vertikála_pozícia = (používateľ.화면높이() - výška_VALUE) / 2;
            } else if ((종류 == 26 || 종류 == 28) && Word_SMS(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && Word_SMS(서술상수, "(Ljava/lang/String;IIIILSlovenský/vlastné/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                výška_VALUE = 빼기(1); 폭 = 빼기(1); vertikála_pozícia = 빼기(1); 가로 = 빼기(1);
            } else { zlyhanie_VALUE("지원하지 않는 Slovenský 화면 생성자"); return; }
            int Spracovanie_textu = 빼기(2), prvok_VALUE = 빼기(2); if (!화면객체(prvok_VALUE)) return;
            if (폭 < 1 || výška_VALUE < 1 || 가로 < 0 || vertikála_pozícia < 0 || 폭 > používateľ.화면너비() - 가로 || výška_VALUE > používateľ.화면높이() - vertikála_pozícia) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int INDEX = používateľ.화면연결(0, 종류 - 23, 0, 0, 0, 0);
            if (INDEX < 1 || INDEX > 32) { zlyhanie_VALUE("화면 prvok_VALUE 자리가 가득 찼습니다"); return; }
            halda_VALUE[prvok_VALUE + 2] = INDEX; 화면참조[INDEX - 1] = prvok_VALUE;
            halda_VALUE[prvok_VALUE + 5] = 가로; halda_VALUE[prvok_VALUE + 6] = vertikála_pozícia; halda_VALUE[prvok_VALUE + 7] = 폭; halda_VALUE[prvok_VALUE + 8] = výška_VALUE; halda_VALUE[prvok_VALUE + 10] = 2;
            halda_VALUE[prvok_VALUE + 4] = 받이; halda_zdroj[prvok_VALUE + 4] = 1; halda_VALUE[prvok_VALUE + 12] = 1;
            používateľ.화면연결(1, INDEX, 가로, vertikála_pozícia, 폭, výška_VALUE);
            if (종류 == 24) používateľ.화면연결(7, INDEX, 2, 0, 0, 0);
            화면문자설정(prvok_VALUE, Spracovanie_textu); return;
        }
        if (príkaz_kód != 182) { zlyhanie_VALUE("잘못된 Slovenský 화면 호출 Príkaz"); return; }
        if (Word_SMS(názov_konštanta, "zapísať_SMS") && Word_SMS(서술상수, "(Ljava/lang/String;)V")) {
            int Spracovanie_textu = 빼기(2), prvok_VALUE = 빼기(2); if (화면객체(prvok_VALUE)) 화면문자설정(prvok_VALUE, Spracovanie_textu); return;
        }
        if (Word_SMS(názov_konštanta, "글읽기") && Word_SMS(서술상수, "()Ljava/lang/String;")) {
            int prvok_VALUE = 빼기(2); if (화면객체(prvok_VALUE)) 넣기(화면문자읽기(prvok_VALUE), 2); return;
        }
        if (Word_SMS(názov_konštanta, "동작맡기기") && Word_SMS(서술상수, "(LSlovenský/vlastné/동작받이;)V")) {
            int 받이 = 빼기(2), prvok_VALUE = 빼기(2);
            if (화면객체(prvok_VALUE)) { halda_VALUE[prvok_VALUE + 4] = 받이; halda_zdroj[prvok_VALUE + 4] = 1; halda_VALUE[prvok_VALUE + 12] = 1; } return;
        }
        if (Word_SMS(názov_konštanta, "Pridať_prvok") && Word_SMS(서술상수, "(LSlovenský/vlastné/화면구성요소;)V")) {
            int dieťa_VALUE = 빼기(2), nadradený_VALUE = 빼기(2); if (!화면객체(dieťa_VALUE) || !화면객체(nadradený_VALUE)) return;
            if (používateľ.화면연결(2, halda_VALUE[nadradený_VALUE + 2], halda_VALUE[dieťa_VALUE + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            halda_VALUE[dieťa_VALUE + 11] = nadradený_VALUE; halda_zdroj[dieťa_VALUE + 11] = 1; return;
        }
        if (Word_SMS(názov_konštanta, "자리정하기") && Word_SMS(서술상수, "(IIII)V")) {
            int výška_VALUE = 빼기(1), 폭 = 빼기(1), vertikála_pozícia = 빼기(1), 가로 = 빼기(1), prvok_VALUE = 빼기(2); if (!화면객체(prvok_VALUE)) return;
            if (používateľ.화면연결(1, halda_VALUE[prvok_VALUE + 2], 가로, vertikála_pozícia, 폭, výška_VALUE) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            halda_VALUE[prvok_VALUE + 5] = 가로; halda_VALUE[prvok_VALUE + 6] = vertikála_pozícia; halda_VALUE[prvok_VALUE + 7] = 폭; halda_VALUE[prvok_VALUE + 8] = výška_VALUE; return;
        }
        if ((Word_SMS(názov_konštanta, "zobraziť_okno") || Word_SMS(názov_konštanta, "Zatvoriť")) && Word_SMS(서술상수, "()V")) {
            boolean viditeľnosť_VALUE = Word_SMS(názov_konštanta, "zobraziť_okno"); int prvok_VALUE = 빼기(2); if (!화면객체(prvok_VALUE)) return;
            if (používateľ.화면연결(viditeľnosť_VALUE ? 3 : 4, halda_VALUE[prvok_VALUE + 2], viditeľnosť_VALUE ? 1 : 0, 0, 0, 0) < 0) { zlyhanie_VALUE("화면은 interaktívny 명령에서 실행해야 합니다"); return; }
            halda_VALUE[prvok_VALUE + 9] = viditeľnosť_VALUE ? 1 : 0; return;
        }
        if (Word_SMS(názov_konštanta, "보이는가") && Word_SMS(서술상수, "()Z")) { int prvok_VALUE = 빼기(2); if (화면객체(prvok_VALUE)) 넣기(halda_VALUE[prvok_VALUE + 9], 1); return; }
        zlyhanie_VALUE("지원하지 않는 Slovenský 화면 metóda_VALUE");
    }
    static void 화면호출(int vlastník, int názov_konštanta, int 서술상수, int príkaz_kód) {
        if (Word_SMS(vlastník, "javax/swing/SwingUtilities")) {
            if (príkaz_kód == 184 && Word_SMS(názov_konštanta, "invokeLater") && Word_SMS(서술상수, "(Ljava/lang/Runnable;)V")) { int objekt_zdroj = 빼기(2); if (!객체유효(objekt_zdroj)) return; if (나중수 == 8) { zlyhanie_VALUE("invokeLater queue full"); return; } 나중실행[나중수++] = objekt_zdroj; return; }
            if (príkaz_kód == 184 && Word_SMS(názov_konštanta, "isEventDispatchThread") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            zlyhanie_VALUE("unsupported SwingUtilities method"); return;
        }
        if (Word_SMS(vlastník, "java/awt/event/ActionEvent")) {
            int objekt_zdroj = 빼기(2); if (!objekt_VALUE(objekt_zdroj, 29)) return;
            if (Word_SMS(názov_konštanta, "getSource") && Word_SMS(서술상수, "()Ljava/lang/Object;")) 넣기(halda_VALUE[objekt_zdroj + 2], 2);
            else if (Word_SMS(názov_konštanta, "getActionCommand") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(halda_VALUE[objekt_zdroj + 2]), 2);
            else if (Word_SMS(názov_konštanta, "getID") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else zlyhanie_VALUE("unsupported ActionEvent method"); return;
        }
        if (príkaz_kód == 183 && Word_SMS(názov_konštanta, "<init>")) {
            int COLUMNS = 0, SMS_zdroj = 0;
            if (Word_SMS(서술상수, "(I)V")) COLUMNS = 빼기(1);
            else if (Word_SMS(서술상수, "(Ljava/lang/String;I)V")) { COLUMNS = 빼기(1); SMS_zdroj = 빼기(2); }
            else if (Word_SMS(서술상수, "(Ljava/lang/String;)V")) SMS_zdroj = 빼기(2);
            else if (Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Word_SMS(서술상수, "()V")) { zlyhanie_VALUE("unsupported Swing constructor"); return; }
            int objekt_zdroj = 빼기(2); if (!객체유효(objekt_zdroj)) return;
            if (halda_VALUE[objekt_zdroj] == 30) { zlyhanie_VALUE("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(objekt_zdroj) || COLUMNS < 0) return;
            int konto_VALUE = používateľ.화면연결(0, halda_VALUE[objekt_zdroj] - 23, 0, 0, 0, 0);
            if (konto_VALUE < 1 || konto_VALUE > 32) { zlyhanie_VALUE("GUI widget slots exhausted"); return; }
            halda_VALUE[objekt_zdroj + 2] = konto_VALUE; 화면참조[konto_VALUE - 1] = objekt_zdroj; halda_VALUE[objekt_zdroj + 5] = halda_VALUE[objekt_zdroj] == 24 ? 130 : 16; halda_VALUE[objekt_zdroj + 6] = halda_VALUE[objekt_zdroj] == 24 ? 110 : 16;
            halda_VALUE[objekt_zdroj + 7] = halda_VALUE[objekt_zdroj] == 24 ? 380 : 220; halda_VALUE[objekt_zdroj + 8] = halda_VALUE[objekt_zdroj] == 24 ? 240 : 28; halda_VALUE[objekt_zdroj + 10] = 1;
            화면문자설정(objekt_zdroj, SMS_zdroj); return;
        }
        if (Word_SMS(názov_konštanta, "setText") || Word_SMS(názov_konštanta, "setTitle")) { int SMS_zdroj = 빼기(2), objekt_zdroj = 빼기(2); if (화면객체(objekt_zdroj) && Word_SMS(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(objekt_zdroj, SMS_zdroj); return; }
        if (Word_SMS(názov_konštanta, "getText") || Word_SMS(názov_konštanta, "getTitle")) { int objekt_zdroj = 빼기(2); if (화면객체(objekt_zdroj) && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(objekt_zdroj), 2); return; }
        if (Word_SMS(názov_konštanta, "addActionListener") && Word_SMS(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int dostať_zdroj = 빼기(2), objekt_zdroj = 빼기(2); if (화면객체(objekt_zdroj)) { halda_VALUE[objekt_zdroj + 4] = dostať_zdroj; halda_zdroj[objekt_zdroj + 4] = 1; } return; }
        if (Word_SMS(názov_konštanta, "getContentPane") && Word_SMS(서술상수, "()Ljava/awt/Container;")) { int objekt_zdroj = 빼기(2); if (화면객체(objekt_zdroj)) 넣기(objekt_zdroj, 2); return; }
        if (Word_SMS(názov_konštanta, "setLayout") && Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) { int Navigácia_zdroj = 빼기(2), objekt_zdroj = 빼기(2); if (화면객체(objekt_zdroj) && Navigácia_zdroj != 0) zlyhanie_VALUE("only absolute layout (null) is supported"); return; }
        if (Word_SMS(názov_konštanta, "add") && (Word_SMS(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean Navigácia_podmienka = Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (Navigácia_podmienka) 빼기(2);
            int dieťa_zdroj = 빼기(2), objekt_zdroj = 빼기(2); if (!화면객체(dieťa_zdroj) || !화면객체(objekt_zdroj)) return;
            if (používateľ.화면연결(2, halda_VALUE[objekt_zdroj + 2], halda_VALUE[dieťa_zdroj + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            halda_VALUE[dieťa_zdroj + 11] = objekt_zdroj; halda_zdroj[dieťa_zdroj + 11] = 1; if (!Navigácia_podmienka) 넣기(dieťa_zdroj, 2); return;
        }
        if (Word_SMS(názov_konštanta, "setBounds") && Word_SMS(서술상수, "(IIII)V")) {
            int výška_VALUE = 빼기(1), 너비 = 빼기(1), Y_súradnica = 빼기(1), X_súradnica = 빼기(1), objekt_zdroj = 빼기(2); if (!화면객체(objekt_zdroj)) return;
            if (používateľ.화면연결(1, halda_VALUE[objekt_zdroj + 2], X_súradnica, Y_súradnica, 너비, výška_VALUE) < 0) { 예외던짐(9, "GUI bounds"); return; }
            halda_VALUE[objekt_zdroj + 5] = X_súradnica; halda_VALUE[objekt_zdroj + 6] = Y_súradnica; halda_VALUE[objekt_zdroj + 7] = 너비; halda_VALUE[objekt_zdroj + 8] = výška_VALUE; return;
        }
        if (Word_SMS(názov_konštanta, "setSize") && Word_SMS(서술상수, "(II)V")) {
            int výška_VALUE = 빼기(1), 너비 = 빼기(1), objekt_zdroj = 빼기(2); if (!화면객체(objekt_zdroj)) return;
            if (používateľ.화면연결(1, halda_VALUE[objekt_zdroj + 2], halda_VALUE[objekt_zdroj + 5], halda_VALUE[objekt_zdroj + 6], 너비, výška_VALUE) < 0) 예외던짐(9, "GUI size"); else { halda_VALUE[objekt_zdroj + 7] = 너비; halda_VALUE[objekt_zdroj + 8] = výška_VALUE; } return;
        }
        if (Word_SMS(názov_konštanta, "setLocationRelativeTo") && Word_SMS(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), objekt_zdroj = 빼기(2); if (!화면객체(objekt_zdroj)) return; if (상대배치 != 0) { zlyhanie_VALUE("only screen centering supported"); return; } halda_VALUE[objekt_zdroj + 5] = (používateľ.화면너비() - halda_VALUE[objekt_zdroj + 7]) / 2; halda_VALUE[objekt_zdroj + 6] = (používateľ.화면높이() - halda_VALUE[objekt_zdroj + 8]) / 2; používateľ.화면연결(1, halda_VALUE[objekt_zdroj + 2], halda_VALUE[objekt_zdroj + 5], halda_VALUE[objekt_zdroj + 6], halda_VALUE[objekt_zdroj + 7], halda_VALUE[objekt_zdroj + 8]); return; }
        if (Word_SMS(názov_konštanta, "setDefaultCloseOperation") && Word_SMS(서술상수, "(I)V")) { int politika = 빼기(1), objekt_zdroj = 빼기(2); if (화면객체(objekt_zdroj)) { if (politika < 0 || politika > 3) 예외던짐(9, "close policy"); else { halda_VALUE[objekt_zdroj + 10] = politika; používateľ.화면연결(7, halda_VALUE[objekt_zdroj + 2], politika, 0, 0, 0); } } return; }
        if (Word_SMS(názov_konštanta, "setVisible") && Word_SMS(서술상수, "(Z)V")) { int údaje_VALUE = 빼기(1), objekt_zdroj = 빼기(2); if (화면객체(objekt_zdroj)) { int 처리값 = používateľ.화면연결(3, halda_VALUE[objekt_zdroj + 2], údaje_VALUE, 0, 0, 0); if (처리값 < 0) zlyhanie_VALUE("Swing requires a standalone interactive command"); else halda_VALUE[objekt_zdroj + 9] = údaje_VALUE; } return; }
        if (Word_SMS(názov_konštanta, "dispose") && Word_SMS(서술상수, "()V")) { int objekt_zdroj = 빼기(2); if (화면객체(objekt_zdroj)) { používateľ.화면연결(4, halda_VALUE[objekt_zdroj + 2], 0, 0, 0, 0); halda_VALUE[objekt_zdroj + 9] = 0; } return; }
        if (Word_SMS(názov_konštanta, "repaint") || Word_SMS(názov_konštanta, "validate")) { int objekt_zdroj = 빼기(2); if (!화면객체(objekt_zdroj) || !Word_SMS(서술상수, "()V")) return; používateľ.화면연결(1, halda_VALUE[objekt_zdroj + 2], halda_VALUE[objekt_zdroj + 5], halda_VALUE[objekt_zdroj + 6], halda_VALUE[objekt_zdroj + 7], halda_VALUE[objekt_zdroj + 8]); return; }
        if (Word_SMS(názov_konštanta, "isVisible") && Word_SMS(서술상수, "()Z")) { int objekt_zdroj = 빼기(2); if (화면객체(objekt_zdroj)) 넣기(halda_VALUE[objekt_zdroj + 9], 1); return; }
        zlyhanie_VALUE("unsupported Swing method (native subset)");
    }
    static void expedovať_udalosť(int cieľ_adresa, int 사건번호, boolean Slovenský) {
        if (cieľ_adresa < 1 || halda_VALUE[cieľ_adresa] < 32) { zlyhanie_VALUE("Java event listener required"); return; }
        int Súbor_INDEX = názov_metóda(halda_VALUE[cieľ_adresa] - 32, 사건번호 == 0 ? (Slovenský ? "Spustiť" : "run") : (Slovenský ? "dostať_Akcia" : "actionPerformed"), 사건번호 == 0 ? "()V" : (Slovenský ? "(LSlovenský/vlastné/Akcia_upozornenie;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (Súbor_INDEX < 0) { zlyhanie_VALUE("event callback missing"); return; }
        v_termíne_splatnosti_vlákno = 0; počet_vlákien = 1; rám_INDEX = 0; vlákno_Stav[0] = 1; rám_Vrstvy[0] = 0; rám_zámok[0] = incializovať_rám[0] = 0; zmeniť_požiadavka = false;
        for (int Loop_INDEX = 0; Loop_INDEX < 128; Loop_INDEX++) { miestny_VALUE[Loop_INDEX] = miestny_Typ[Loop_INDEX] = 0; }
        rám_metóda[0] = Súbor_INDEX; rám_pozícia[0] = metóda_START[Súbor_INDEX]; miestny_VALUE[0] = cieľ_adresa; miestny_Typ[0] = 2;
        if (사건번호 != 0) { miestny_VALUE[1] = 사건번호; miestny_Typ[1] = 2; }
        사건중 = true; Vykonať_príkaz(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!chyba) {
            if (나중수 > 0) { int cieľ_adresa = 나중실행[0], Slovenský = 나중한국어[0]; for (int Loop_INDEX = 1; Loop_INDEX < 나중수; Loop_INDEX++) { 나중실행[Loop_INDEX - 1] = 나중실행[Loop_INDEX]; 나중한국어[Loop_INDEX - 1] = 나중한국어[Loop_INDEX]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; expedovať_udalosť(cieľ_adresa, 0, Slovenský != 0); continue; }
            if (používateľ.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int 사건번호 = používateľ.화면연결(5, 0, 0, 0, 0, 0); if (사건번호 == 0) continue;
            if (사건번호 < 0) { zlyhanie_VALUE("GUI event I/O failed"); return; }
            int konto_VALUE = 사건번호 & 65535; if (konto_VALUE < 1 || konto_VALUE > 32) continue; int objekt_zdroj = 화면참조[konto_VALUE - 1]; if (objekt_zdroj == 0) continue;
            if ((사건번호 & 65536) != 0) {
                if (halda_VALUE[objekt_zdroj + 10] != 0) halda_VALUE[objekt_zdroj + 9] = 0;
                if (halda_VALUE[objekt_zdroj + 10] == 3) for (int Loop_INDEX = 0; Loop_INDEX < 32; Loop_INDEX++) if (화면참조[Loop_INDEX] != 0 && halda_VALUE[화면참조[Loop_INDEX]] == 24) používateľ.화면연결(4, Loop_INDEX + 1, 0, 0, 0, 0);
            } else if (halda_VALUE[objekt_zdroj + 4] != 0) {
                int 안내참조 = vyhradiť_Úložisko(29, 2); if (chyba) return; halda_VALUE[안내참조 + 2] = objekt_zdroj; halda_VALUE[안내참조 + 3] = halda_VALUE[objekt_zdroj + 12]; halda_zdroj[안내참조 + 2] = 1; expedovať_udalosť(halda_VALUE[objekt_zdroj + 4], 안내참조, halda_VALUE[objekt_zdroj + 12] != 0);
            }
        }
    }
    public static int Spustiť_2() {
        if (používateľ.인수개수() == 1 && 자바도구.같음(používateľ.Argumenty(0), "-version")) {
            používateľ.Zápis("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (používateľ.인수개수() < 1) { používateľ.Zápis("Usage: java CLASS [ARGS]\n"); return 2; }
        položka_lekcia_Definícia = dávka_lekcia_Definícia(hostiteľ_znak(používateľ.Argumenty(0))); if (chyba || položka_lekcia_Definícia < 0) return 1;
        int položka_bod_VALUE = názov_metóda(položka_lekcia_Definícia, "Spustiť_2", "()V");
        boolean 한국어진입 = položka_bod_VALUE >= 0 && (metóda_prístup[položka_bod_VALUE] & 9) == 9;
        if (!한국어진입) položka_bod_VALUE = názov_metóda(položka_lekcia_Definícia, "main", "([Ljava/lang/String;)V");
        if (položka_bod_VALUE < 0 || (metóda_prístup[položka_bod_VALUE] & 9) != 9) zlyhanie_VALUE("public static void Spustiť_2() or main(String[] args) required");
        if (chyba) return 1;
        int Argumenty = vyhradiť_Úložisko(3, používateľ.인수개수() - 1); prvok_poľa[Argumenty] = -1;
        for (int 수 = 1; 수 < používateľ.인수개수() && !chyba; 수++) halda_VALUE[Argumenty + 1 + 수] = hostiteľ_znak(používateľ.Argumenty(수));
        rám_INDEX = 0; rám_metóda[0] = položka_bod_VALUE; rám_pozícia[0] = metóda_START[položka_bod_VALUE]; miestny_VALUE[0] = 한국어진입 ? 0 : Argumenty; miestny_Typ[0] = 한국어진입 ? 0 : 2;
        vlákno_Stav[0] = 1; vlákno_objekt[0] = vyhradiť_Úložisko(13, 2);
        Vykonať_príkaz(); if (!chyba) 화면사건들(); return chyba ? 1 : 0;
    }
}
