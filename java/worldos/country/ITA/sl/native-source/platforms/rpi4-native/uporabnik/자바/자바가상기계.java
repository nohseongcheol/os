// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. Datoteka/operand_Sklad/Gradiva/veja 경계를 Izvedi_ukaz 중 검사한다. */
public final class 자바가상기계 {
    static int[] Datoteka = new int[16 * 16384], začasna_datoteka = new int[16384], ime_datoteke_SMS = new int[512];
    static int[] konstanta_oznaka = new int[8192], 상가 = new int[8192], konstanta_SECOND_VALUE = new int[8192], niz_Gradiva = new int[8192];
    static int[] metoda_ime_SMS = new int[512], metoda_Tip = new int[512], metoda_dostop = new int[512], metoda_lastnik = new int[512];
    static int[] metoda_Start = new int[512], metoda_končati_klic = new int[512], metoda_Sklad = new int[512], 함수지역 = new int[512];
    static int[] metoda_argument_COUNT = new int[512], metoda_argument_Tip = new int[8192], metoda_vrni = new int[512];
    static int[] 경계 = new int[16 * 16384];
    static int[] lokalen_krajeven_VALUE = new int[16384], lokalen_krajeven_Tip = new int[16384], operand_Sklad_VALUE = new int[16384], operand_Sklad_Tip = new int[16384];
    static int[] okvir_metoda = new int[128], okvir_položaj = new int[128], okvir_Sklad = new int[128], okvir_navodilo = new int[128], inicializirati_okvir = new int[128];
    static int[] Razred_definicija_ime = new int[16], Razred_definicija_spremeniti_velikost = new int[16], Razred_definicija_nadrejen = new int[16], Razred_definicija_stanje = new int[16], 종칸수 = new int[16], inicializirati_Razred_definicija = new int[16];
    static int[] Razred_vmesnik = new int[16 * 16], Razred_vmesnik_COUNT = new int[16];
    static int[] 칸이름 = new int[512], 칸형 = new int[512], 칸주인 = new int[512], 칸권한 = new int[512], 칸위치 = new int[512], 칸값 = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] kopica_VALUE = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], kopica_Gradiva = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], element_polja = new int[32768], Store_celo_število = new int[256];
    static int Velikost, 읽기위치, metoda_COUNT, ime_razreda, okvir_INDEX = -1, kopica_končati_klic_položaj = 1, vrni_Tip;
    static int Razred_definicija_COUNT, 칸수, 잡기수, 현재읽는종, 던진객체, 잠시수, zaslon_COUNT, Zbirka_COUNT;
    static int sprotno_nit, nit_COUNT = 1, vnos_Razred_definicija;
    static int[] nit_okvir = new int[4], nit_stanje = new int[4], nit_predmet = new int[4], nit_cilj = new int[4], 가닥대기 = new int[4];
    static boolean NAPAKA, spremeniti_zahteva;
    static int[] zaklepanje_lastnik = new int[32768], 잠금깊이 = new int[32768], okvir_zaklepanje = new int[128], Razred_zaklepanje = new int[16], Razred_nit = new int[16];

    static void napaka_VALUE(String Word_SMS) {
        if (NAPAKA) return;
        int območje_CODE = 0;
        if (자바도구.같음(Word_SMS, "ArithmeticException: / by zero")) območje_CODE = 4;
        if (자바도구.같음(Word_SMS, "NullPointerException") || 자바도구.같음(Word_SMS, "null or invalid array")) območje_CODE = 5;
        if (자바도구.같음(Word_SMS, "ArrayIndexOutOfBoundsException")) območje_CODE = 7;
        if (자바도구.같음(Word_SMS, "StringIndexOutOfBoundsException")) območje_CODE = 8;
        if (자바도구.같음(Word_SMS, "NumberFormatException")) območje_CODE = 10;
        if (자바도구.같음(Word_SMS, "FileNotFoundException: file open failed")) območje_CODE = 12;
        if (자바도구.같음(Word_SMS, "IOException: stream closed") || 자바도구.같음(Word_SMS, "IOException: read failed") || 자바도구.같음(Word_SMS, "IOException: write failed")) območje_CODE = 11;
        if (자바도구.같음(Word_SMS, "ClassCastException")) območje_CODE = 14;
        if (자바도구.같음(Word_SMS, "NegativeArraySizeException")) območje_CODE = 15;
        if (območje_CODE != 0 && okvir_INDEX >= 0) { 예외던짐(območje_CODE, Word_SMS); return; }
        uporabnik.Pisanje("JVM error: "); uporabnik.Pisanje(Word_SMS); uporabnik.pisati_znak_VALUE(10); NAPAKA = true;
    }
    static boolean izrezek(int Zaženi, int 길이) {
        if (Zaženi < 0 || Zaženi >= Datoteka.length || 길이 < 0) return false;
        int Razred_definicija = Zaženi / 16384;
        return Zaženi % 16384 <= Razred_definicija_spremeniti_velikost[Razred_definicija] && 길이 <= Razred_definicija_spremeniti_velikost[Razred_definicija] - Zaženi % 16384;
    }
    static int bajt_VALUE() {
        if (!izrezek(읽기위치, 1)) { napaka_VALUE("truncated class file"); return 0; }
        return Datoteka[읽기위치++];
    }
    static int 짧은수() { return bajt_VALUE() << 8 | bajt_VALUE(); }
    static int celo_število() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int 길이) { if (!izrezek(읽기위치, 길이)) napaka_VALUE("invalid attribute size"); else 읽기위치 += 길이; }
    static boolean preveriti_konstanta(int 수, int 종류) {
        if (수 <= 0 || 수 >= konstanta_oznaka.length || konstanta_oznaka[수] != 종류) { napaka_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean SMS_obseg(int Zaženi, int 길이, String Word_SMS) {
        if (!izrezek(Zaženi, 길이)) return false;
        int 읽는자리 = Zaženi, 끝 = Zaženi + 길이;
        for (int Loop_INDEX = 0; Loop_INDEX < Word_SMS.length(); Loop_INDEX++) {
            int koda_znaka = Word_SMS.charAt(Loop_INDEX);
            if (koda_znaka > 0 && koda_znaka < 128) { if (읽는자리 >= 끝 || Datoteka[읽는자리++] != koda_znaka) return false; }
            else if (koda_znaka < 2048) {
                if (읽는자리 + 2 > 끝 || Datoteka[읽는자리++] != (192 | (koda_znaka >> 6)) || Datoteka[읽는자리++] != (128 | (koda_znaka & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || Datoteka[읽는자리++] != (224 | (koda_znaka >> 12)) || Datoteka[읽는자리++] != (128 | ((koda_znaka >> 6) & 63)) || Datoteka[읽는자리++] != (128 | (koda_znaka & 63))) return false;
        }
        return 읽는자리 == 끝;
    }
    static boolean Word_SMS(int konstanta_VALUE, String Word_SMS) { return preveriti_konstanta(konstanta_VALUE, 1) && SMS_obseg(상가[konstanta_VALUE], konstanta_SECOND_VALUE[konstanta_VALUE], Word_SMS); }
    static boolean 같은말(int 가, int SECOND_operand) {
        if (!preveriti_konstanta(가, 1) || !preveriti_konstanta(SECOND_operand, 1) || konstanta_SECOND_VALUE[가] != konstanta_SECOND_VALUE[SECOND_operand]) return false;
        for (int 수 = 0; 수 < konstanta_SECOND_VALUE[가]; 수++) if (Datoteka[상가[가] + 수] != Datoteka[상가[SECOND_operand] + 수]) return false;
        return true;
    }
    static int ime_razreda_SMS(int 수) { return preveriti_konstanta(수, 7) && preveriti_konstanta(상가[수], 1) ? 상가[수] : 0; }
    static int Gradiva_ime(int 수) { return preveriti_konstanta(수, 12) && preveriti_konstanta(상가[수], 1) ? 상가[수] : 0; }
    static int Gradiva_Tip(int 수) { return preveriti_konstanta(수, 12) && preveriti_konstanta(konstanta_SECOND_VALUE[수], 1) ? konstanta_SECOND_VALUE[수] : 0; }
    static int 서술형(int 끝, boolean prazen_Tip) {
        if (읽기위치 >= 끝) { napaka_VALUE("invalid descriptor"); return 0; }
        int VALUE = bajt_VALUE();
        if (VALUE == 'V' && prazen_Tip) return 0;
        if (VALUE == 'I' || VALUE == 'B' || VALUE == 'C' || VALUE == 'S' || VALUE == 'Z') return 1;
        if (VALUE == '[') { 서술형(끝, false); return 2; }
        if (VALUE == 'L') {
            int Zaženi = 읽기위치;
            while (읽기위치 < 끝 && Datoteka[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == Zaženi) napaka_VALUE("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        napaka_VALUE("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int FUNCTION_VALUE) {
        int 이전 = 읽기위치, 수 = metoda_Tip[FUNCTION_VALUE];
        if (!preveriti_konstanta(수, 1)) return;
        읽기위치 = 상가[수]; int 끝 = 읽기위치 + konstanta_SECOND_VALUE[수];
        if (bajt_VALUE() != '(') napaka_VALUE("invalid method descriptor");
        int element_COUNT = 0;
        while (!NAPAKA && 읽기위치 < 끝 && Datoteka[읽기위치] != ')') {
            if (element_COUNT == 16) { napaka_VALUE("too many method arguments"); break; }
            metoda_argument_Tip[FUNCTION_VALUE * 16 + element_COUNT++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || bajt_VALUE() != ')') napaka_VALUE("invalid method descriptor");
        metoda_vrni[FUNCTION_VALUE] = 서술형(끝, true); metoda_argument_COUNT[FUNCTION_VALUE] = element_COUNT;
        if (읽기위치 != 끝) napaka_VALUE("invalid method descriptor");
        읽기위치 = 이전;
    }
    static int 상번호() { int VALUE = 짧은수(); return VALUE == 0 ? 0 : 현재읽는종 * 512 + VALUE; }
    static int 명상수() { return metoda_lastnik[okvir_metoda[okvir_INDEX]] * 512 + 명짧(); }
    static void 속성건너() {
        int element_COUNT = 짧은수();
        for (int 수 = 0; 수 < element_COUNT && !NAPAKA; 수++) { preveriti_konstanta(상번호(), 1); 건너(celo_število()); }
    }
    static int 명령길이(int VALUE) {
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
    static int položaj_celo_število(int 읽는자리) {
        if (!izrezek(읽는자리, 4)) { napaka_VALUE("truncated bytecode operand"); return 0; }
        return Datoteka[읽는자리] << 24 | Datoteka[읽는자리 + 1] << 16 | Datoteka[읽는자리 + 2] << 8 | Datoteka[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int Zaženi, int 끝) {
        int VALUE = Datoteka[읽는자리], 길이 = 명령길이(VALUE);
        if (VALUE == 170 || VALUE == 171) {
            int BASE_položaj = 읽는자리 + 1;
            while ((BASE_položaj - Zaženi) % 4 != 0) BASE_položaj++;
            if (끝 - BASE_položaj < (VALUE == 170 ? 12 : 8)) return 0;
            int vnos_COUNT = VALUE == 170 ? položaj_celo_število(BASE_položaj + 8) - položaj_celo_število(BASE_položaj + 4) + 1 : položaj_celo_število(BASE_položaj + 4);
            if (vnos_COUNT < 0 || vnos_COUNT > 2048) return 0;
            길이 = BASE_položaj - 읽는자리 + (VALUE == 170 ? 12 + 4 * vnos_COUNT : 8 + 8 * vnos_COUNT);
        }
        if (VALUE == 196 && 읽는자리 + 1 < 끝) {
            int Word_podatki = Datoteka[읽는자리 + 1]; 길이 = Word_podatki == 132 ? 6 : (Word_podatki == 21 || Word_podatki == 25 || Word_podatki == 54 || Word_podatki == 58) ? 4 : 0;
        }
        return 길이 > 0 && 길이 <= 끝 - 읽는자리 ? 길이 : 0;
    }
    static void preveriti_cilj_VALUE(int cilj_VALUE, int FUNCTION_VALUE) {
        if (cilj_VALUE < metoda_Start[FUNCTION_VALUE] || cilj_VALUE >= metoda_končati_klic[FUNCTION_VALUE] || 경계[cilj_VALUE] != FUNCTION_VALUE + 1) napaka_VALUE("invalid branch target");
    }
    static void 클래스읽기(int Razred_definicija) {
        현재읽는종 = Razred_definicija; 읽기위치 = Razred_definicija * 16384; Velikost = 읽기위치 + Razred_definicija_spremeniti_velikost[Razred_definicija];
        if (celo_število() != 0xcafebabe) { napaka_VALUE("not a class file"); return; }
        int 부판 = 짧은수(), različica_VALUE = 짧은수();
        if (različica_VALUE < 45 || različica_VALUE > 52 || 부판 != 0) { napaka_VALUE("supported class versions: 45..52, minor 0"); return; }
        int konstanta_COUNT = 짧은수(), BASE_položaj = Razred_definicija * 512;
        if (konstanta_COUNT < 1 || konstanta_COUNT > 512) { napaka_VALUE("constant pool limit (511)"); return; }
        for (int vnos_COUNT = 1; vnos_COUNT < konstanta_COUNT && !NAPAKA; vnos_COUNT++) {
            int 수 = BASE_položaj + vnos_COUNT, 종류 = bajt_VALUE(); konstanta_oznaka[수] = 종류;
            if (종류 == 1) { konstanta_SECOND_VALUE[수] = 짧은수(); 상가[수] = 읽기위치; 건너(konstanta_SECOND_VALUE[수]); }
            else if (종류 == 3) 상가[수] = celo_število();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[수] = 상번호(); konstanta_SECOND_VALUE[수] = 상번호(); }
            else napaka_VALUE("unsupported constant type");
        }
        int dovoljenje_VALUE = 짧은수();
        if ((dovoljenje_VALUE & (0x2000 | 0x4000)) != 0) napaka_VALUE("annotation/enum class unsupported");
        Razred_definicija_ime[Razred_definicija] = ime_razreda_SMS(상번호());
        Razred_definicija_nadrejen[Razred_definicija] = ime_razreda_SMS(상번호());
        int vmesnik_COUNT = 짧은수(); if (vmesnik_COUNT > 16) { napaka_VALUE("interface count limit"); return; }
        Razred_vmesnik_COUNT[Razred_definicija] = vmesnik_COUNT;
        for (int Loop_INDEX = 0; Loop_INDEX < vmesnik_COUNT; Loop_INDEX++) Razred_vmesnik[Razred_definicija * 16 + Loop_INDEX] = ime_razreda_SMS(상번호());
        int polje_COUNT = 짧은수();
        if (polje_COUNT > 512 - 칸수) { napaka_VALUE("field count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < polje_COUNT && !NAPAKA; Loop_INDEX++) {
            int Datoteka_INDEX = 칸수++; 칸주인[Datoteka_INDEX] = Razred_definicija; 칸권한[Datoteka_INDEX] = 짧은수(); 칸이름[Datoteka_INDEX] = 상번호(); 칸형[Datoteka_INDEX] = 상번호();
            preveriti_konstanta(칸이름[Datoteka_INDEX], 1); preveriti_konstanta(칸형[Datoteka_INDEX], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[칸형[Datoteka_INDEX]]; int območje_CODE = 서술형(읽기위치 + konstanta_SECOND_VALUE[칸형[Datoteka_INDEX]], false); 읽기위치 = 보존값;
            if ((칸권한[Datoteka_INDEX] & 8) == 0) 칸위치[Datoteka_INDEX] = 종칸수[Razred_definicija]++;
            int atribut_podatki = 짧은수();
            for (int notranje_položaj = 0; notranje_položaj < atribut_podatki && !NAPAKA; notranje_položaj++) {
                int ime_konstanta = 상번호(), 유효길이 = celo_število();
                if (Word_SMS(ime_konstanta, "ConstantValue") && 유효길이 == 2) {
                    int podatki_VALUE = 상번호();
                    if (območje_CODE == 1 && preveriti_konstanta(podatki_VALUE, 3)) 칸값[Datoteka_INDEX] = 상가[podatki_VALUE];
                    else if (območje_CODE == 2 && preveriti_konstanta(podatki_VALUE, 8)) 칸값[Datoteka_INDEX] = konstanta_SMS(상가[podatki_VALUE]);
                } else 건너(유효길이);
            }
        }
        int element_COUNT = 짧은수();
        if (element_COUNT > 512 - metoda_COUNT) { napaka_VALUE("method count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < element_COUNT && !NAPAKA; Loop_INDEX++) {
            int 수 = metoda_COUNT++; metoda_lastnik[수] = Razred_definicija;
            metoda_dostop[수] = 짧은수(); metoda_ime_SMS[수] = 상번호(); metoda_Tip[수] = 상번호();
            preveriti_konstanta(metoda_ime_SMS[수], 1); 서술읽기(수);
            if ((metoda_dostop[수] & 8) == 0) {
                if (metoda_argument_COUNT[수] == 16) { napaka_VALUE("too many instance method arguments"); return; }
                for (int Primerjava_položaj = metoda_argument_COUNT[수]; Primerjava_položaj > 0; Primerjava_položaj--) metoda_argument_Tip[수 * 16 + Primerjava_položaj] = metoda_argument_Tip[수 * 16 + Primerjava_položaj - 1];
                metoda_argument_Tip[수 * 16] = 2; metoda_argument_COUNT[수]++;
            }
            if ((metoda_dostop[수] & 0x100) != 0) napaka_VALUE("user native method unsupported");
            if (Word_SMS(metoda_ime_SMS[수], "<clinit>")) inicializirati_Razred_definicija[Razred_definicija] = 수 + 1;
            for (int sprednja_VALUE = 0; sprednja_VALUE < 수; sprednja_VALUE++) if (metoda_lastnik[sprednja_VALUE] == Razred_definicija && 같은말(metoda_ime_SMS[sprednja_VALUE], metoda_ime_SMS[수]) && 같은말(metoda_Tip[sprednja_VALUE], metoda_Tip[수])) napaka_VALUE("duplicate method");
            int atribut_COUNT = 짧은수();
            for (int atribut_VALUE = 0; atribut_VALUE < atribut_COUNT && !NAPAKA; atribut_VALUE++) {
                int Ime = 상번호(), 길이 = celo_število(), Zaženi = 읽기위치;
                if (!izrezek(Zaženi, 길이)) { napaka_VALUE("truncated method attribute"); break; }
                if (Word_SMS(Ime, "Code")) {
                    if (metoda_Start[수] != 0) napaka_VALUE("duplicate Code attribute");
                    metoda_Sklad[수] = 짧은수(); 함수지역[수] = 짧은수(); int 코드길이 = celo_število();
                    if (metoda_Sklad[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < metoda_argument_COUNT[수]
                        || 코드길이 < 1 || 코드길이 > 8192) napaka_VALUE("method memory limits exceeded");
                    metoda_Start[수] = 읽기위치; 건너(코드길이); metoda_končati_klic[수] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { napaka_VALUE("exception table limit"); return; }
                    for (int notranje_položaj = 0; notranje_položaj < 잡는수; notranje_položaj++) {
                        int 오류참조 = 잡기수++; 잡기함수[오류참조] = 수;
                        잡기시작[오류참조] = metoda_Start[수] + 짧은수(); 잡기끝[오류참조] = metoda_Start[수] + 짧은수();
                        잡기위치[오류참조] = metoda_Start[수] + 짧은수(); int 부호값 = 상번호(); 잡기종[오류참조] = 부호값 == 0 ? 0 : ime_razreda_SMS(부호값);
                    }
                    속성건너();
                    if (읽기위치 != Zaženi + 길이) napaka_VALUE("Code attribute size mismatch");
                } else 건너(길이);
            }
            if ((metoda_dostop[수] & 0x400) != 0) continue;
            if (metoda_Start[수] == 0) napaka_VALUE("missing Code attribute");
            int 칸 = metoda_Start[수];
            while (칸 < metoda_končati_klic[수] && !NAPAKA) {
                int 길이 = 길이읽기(칸, metoda_Start[수], metoda_končati_klic[수]);
                if (길이 == 0) { napaka_VALUE("unsupported or truncated bytecode"); break; }
                경계[칸] = 수 + 1; 칸 += 길이;
            }
            칸 = metoda_Start[수];
            while (칸 < metoda_končati_klic[수] && !NAPAKA) {
                int VALUE = Datoteka[칸];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) preveriti_cilj_VALUE(칸 + (short)(Datoteka[칸 + 1] << 8 | Datoteka[칸 + 2]), 수);
                if (VALUE == 200) preveriti_cilj_VALUE(칸 + položaj_celo_število(칸 + 1), 수);
                if (VALUE == 170 || VALUE == 171) {
                    int 읽는자리 = 칸 + 1; while ((읽는자리 - metoda_Start[수]) % 4 != 0) 읽는자리++;
                    preveriti_cilj_VALUE(칸 + položaj_celo_število(읽는자리), 수);
                    int vnos_COUNT = VALUE == 170 ? položaj_celo_število(읽는자리 + 8) - položaj_celo_število(읽는자리 + 4) + 1 : položaj_celo_število(읽는자리 + 4);
                    읽는자리 += VALUE == 170 ? 12 : 8;
                    for (int notranje_položaj = 0; notranje_položaj < vnos_COUNT; notranje_položaj++) preveriti_cilj_VALUE(칸 + položaj_celo_število(읽는자리 + notranje_položaj * (VALUE == 170 ? 4 : 8) + (VALUE == 170 ? 0 : 4)), 수);
                }
                칸 += 길이읽기(칸, metoda_Start[수], metoda_končati_klic[수]);
            }
            for (int notranje_položaj = 0; notranje_položaj < 잡기수; notranje_položaj++) if (잡기함수[notranje_položaj] == 수) {
                preveriti_cilj_VALUE(잡기시작[notranje_položaj], 수); preveriti_cilj_VALUE(잡기위치[notranje_položaj], 수);
                if (잡기끝[notranje_položaj] != metoda_končati_klic[수]) preveriti_cilj_VALUE(잡기끝[notranje_položaj], 수);
                if (잡기시작[notranje_položaj] >= 잡기끝[notranje_položaj]) napaka_VALUE("invalid exception range");
            }
        }
        if (!NAPAKA) 속성건너();
        if (읽기위치 != Velikost) napaka_VALUE("extra class file data");
    }
    static int dodeliti_Senzor_prostora(int 종류, int 길이) { return 새기억(종류, 길이); }
    static boolean predmet_VALUE(int Gradiva, int 종류) {
        if (!객체유효(Gradiva)) return false;
        if (kopica_VALUE[Gradiva] != 종류) { napaka_VALUE("object type mismatch"); return false; }
        return true;
    }
    static int konstanta_SMS(int INDEX) {
        if (!preveriti_konstanta(INDEX, 1)) return 0;
        if (niz_Gradiva[INDEX] != 0) return niz_Gradiva[INDEX];
        int Gradiva = dodeliti_Senzor_prostora(1, konstanta_SECOND_VALUE[INDEX]); if (NAPAKA) return 0;
        int 끝 = 상가[INDEX] + konstanta_SECOND_VALUE[INDEX], 수 = 상가[INDEX], 길이 = 0;
        while (수 < 끝 && !NAPAKA) {
            int VALUE = Datoteka[수++];
            if (VALUE == 0) napaka_VALUE("invalid modified UTF-8");
            else if (VALUE >= 192 && VALUE <= 223 && 수 < 끝) {
                int Naprej_element = Datoteka[수++];
                if ((Naprej_element & 192) != 128) napaka_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 31) << 6 | Naprej_element & 63;
                if (VALUE != 0 && VALUE < 128) napaka_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 224 && VALUE <= 239 && 수 + 1 < 끝) {
                int 가 = Datoteka[수++], SECOND_operand = Datoteka[수++];
                if ((가 & 192) != 128 || (SECOND_operand & 192) != 128) napaka_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 15) << 12 | (가 & 63) << 6 | SECOND_operand & 63;
                if (VALUE < 2048) napaka_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 128) napaka_VALUE("invalid modified UTF-8");
            kopica_VALUE[Gradiva + 2 + 길이++] = VALUE;
        }
        kopica_VALUE[Gradiva + 1] = 길이; niz_Gradiva[INDEX] = Gradiva; return Gradiva;
    }
    static int gostiti_znak(String VALUE) {
        int Gradiva = dodeliti_Senzor_prostora(1, VALUE.length()); if (NAPAKA) return 0;
        for (int 수 = 0; 수 < VALUE.length(); 수++) kopica_VALUE[Gradiva + 2 + 수] = VALUE.charAt(수);
        return Gradiva;
    }
    static void pisati_SMS(int Gradiva) {
        if (Gradiva == 0) { uporabnik.Pisanje("null"); return; }
        if (!predmet_VALUE(Gradiva, 1)) return;
        for (int 수 = 0; 수 < kopica_VALUE[Gradiva + 1]; 수++) uporabnik.pisati_znak_VALUE(kopica_VALUE[Gradiva + 2 + 수]);
    }
    static int številka_znak(int VALUE) {
        int Gradiva = dodeliti_Senzor_prostora(1, 11); if (NAPAKA) return 0;
        int 길이 = 0;
        if (VALUE < 0) kopica_VALUE[Gradiva + 2 + 길이++] = '-'; else VALUE = -VALUE;
        int kazalec_mesta = 1000000000; boolean Zaženi = false;
        while (kazalec_mesta != 0) {
            int 수 = -(VALUE / kazalec_mesta);
            if (수 != 0 || Zaženi || kazalec_mesta == 1) { kopica_VALUE[Gradiva + 2 + 길이++] = '0' + 수; Zaženi = true; }
            VALUE %= kazalec_mesta; kazalec_mesta /= 10;
        }
        kopica_VALUE[Gradiva + 1] = 길이; return Gradiva;
    }
    static int 정수해독(int Gradiva) {
        if (!predmet_VALUE(Gradiva, 1)) return 0;
        int 길이 = kopica_VALUE[Gradiva + 1], 수 = 0, VALUE = 0; boolean 음수 = false;
        if (길이 > 0 && (kopica_VALUE[Gradiva + 2] == '-' || kopica_VALUE[Gradiva + 2] == '+')) { 음수 = kopica_VALUE[Gradiva + 2] == '-'; 수++; }
        if (수 == 길이) napaka_VALUE("NumberFormatException");
        for (; 수 < 길이 && !NAPAKA; 수++) {
            int številka_VALUE = kopica_VALUE[Gradiva + 2 + 수] - '0';
            if (številka_VALUE < 0 || številka_VALUE > 9 || VALUE < -214748364 || VALUE == -214748364 && številka_VALUE > (음수 ? 8 : 7)) napaka_VALUE("NumberFormatException");
            VALUE = VALUE * 10 - številka_VALUE;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static void 넣기(int VALUE, int Tip_VALUE) {
        if (NAPAKA) return;
        if (okvir_INDEX < 0 || okvir_Sklad[okvir_INDEX] >= metoda_Sklad[okvir_metoda[okvir_INDEX]]) { napaka_VALUE("operand stack overflow"); return; }
        int 칸 = okvir_INDEX * 128 + okvir_Sklad[okvir_INDEX]++; operand_Sklad_VALUE[칸] = VALUE; operand_Sklad_Tip[칸] = Tip_VALUE;
    }
    static int 빼기(int Tip_VALUE) {
        if (NAPAKA) return 0;
        if (okvir_INDEX < 0 || okvir_Sklad[okvir_INDEX] < 1) { napaka_VALUE("operand stack underflow"); return 0; }
        int 칸 = okvir_INDEX * 128 + --okvir_Sklad[okvir_INDEX]; vrni_Tip = operand_Sklad_Tip[칸];
        if (Tip_VALUE != 0 && vrni_Tip != Tip_VALUE) napaka_VALUE("operand type mismatch");
        if (vrni_Tip == 2) zaščititi_VALUE(operand_Sklad_VALUE[칸]);
        return operand_Sklad_VALUE[칸];
    }
    static void 지역읽기(int INDEX, int Tip_VALUE) {
        if (INDEX >= 함수지역[okvir_metoda[okvir_INDEX]] || INDEX < 0 || lokalen_krajeven_Tip[okvir_INDEX * 128 + INDEX] != Tip_VALUE) { napaka_VALUE("invalid or uninitialized local"); return; }
        넣기(lokalen_krajeven_VALUE[okvir_INDEX * 128 + INDEX], Tip_VALUE);
    }
    static void pisati_lokalen_krajeven(int INDEX, int Tip_VALUE) {
        if (INDEX >= 함수지역[okvir_metoda[okvir_INDEX]] || INDEX < 0) { napaka_VALUE("local index out of range"); return; }
        int VALUE = 빼기(Tip_VALUE); lokalen_krajeven_VALUE[okvir_INDEX * 128 + INDEX] = VALUE; lokalen_krajeven_Tip[okvir_INDEX * 128 + INDEX] = Tip_VALUE;
    }
    static int 명바() {
        int Položaj = okvir_položaj[okvir_INDEX];
        if (Položaj < metoda_Start[okvir_metoda[okvir_INDEX]] || Položaj >= metoda_končati_klic[okvir_metoda[okvir_INDEX]]) { napaka_VALUE("instruction pointer out of range"); return 0; }
        okvir_položaj[okvir_INDEX]++; return Datoteka[Položaj];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void premikati_VALUE(int Položaj) {
        int FUNCTION_VALUE = okvir_metoda[okvir_INDEX];
        if (Položaj < metoda_Start[FUNCTION_VALUE] || Položaj >= metoda_končati_klic[FUNCTION_VALUE] || 경계[Položaj] != FUNCTION_VALUE + 1) napaka_VALUE("invalid branch target");
        else okvir_položaj[okvir_INDEX] = Položaj;
    }
    static void 호출(int FUNCTION_VALUE) {
        if (okvir_INDEX % 32 == 31) { napaka_VALUE("call stack limit (32)"); return; }
        int Naprej_element = okvir_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) lokalen_krajeven_Tip[Naprej_element * 128 + 수] = 0;
        for (int 수 = metoda_argument_COUNT[FUNCTION_VALUE] - 1; 수 >= 0; 수--) {
            lokalen_krajeven_VALUE[Naprej_element * 128 + 수] = 빼기(metoda_argument_Tip[FUNCTION_VALUE * 16 + 수]); lokalen_krajeven_Tip[Naprej_element * 128 + 수] = metoda_argument_Tip[FUNCTION_VALUE * 16 + 수];
        }
        if (NAPAKA) return;
        okvir_INDEX = Naprej_element; inicializirati_okvir[okvir_INDEX] = 0; okvir_metoda[okvir_INDEX] = FUNCTION_VALUE; okvir_položaj[okvir_INDEX] = metoda_Start[FUNCTION_VALUE]; okvir_Sklad[okvir_INDEX] = 0;
    }
    static void vrni_KR(int Tip_VALUE) {
        if (Tip_VALUE != metoda_vrni[okvir_metoda[okvir_INDEX]]) { napaka_VALUE("return type mismatch"); return; }
        int VALUE = Tip_VALUE == 0 ? 0 : 빼기(Tip_VALUE);
        if (inicializirati_okvir[okvir_INDEX] != 0) Razred_definicija_stanje[inicializirati_okvir[okvir_INDEX] - 1] = 2;
        if (okvir_zaklepanje[okvir_INDEX] != 0) { izdaja_zaklepanje(okvir_zaklepanje[okvir_INDEX]); okvir_zaklepanje[okvir_INDEX] = 0; }
        okvir_INDEX--; if (okvir_INDEX >= sprotno_nit * 32 && Tip_VALUE != 0) 넣기(VALUE, Tip_VALUE);
    }
    static int[] tok_ime_datoteke = new int[64];
    static void Datoteka_tok_CALL(int lastnik_VALUE, int Ime, int oblika_VALUE, int Ukaz) {
        boolean Izpis = Word_SMS(lastnik_VALUE, "java/io/FileOutputStream");
        int 종류 = Izpis ? 6 : 5;
        if (Ukaz == 183 && Word_SMS(Ime, "<init>")) {
            boolean 이어 = false;
            if (Izpis && Word_SMS(oblika_VALUE, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Word_SMS(oblika_VALUE, "(Ljava/lang/String;)V")) { napaka_VALUE("unsupported file stream constructor"); return; }
            int Datoteka_vnos_ime = 빼기(2), tok_VALUE = 빼기(2);
            if (!predmet_VALUE(Datoteka_vnos_ime, 1) || !predmet_VALUE(tok_VALUE, 종류) || NAPAKA) return;
            if (kopica_VALUE[tok_VALUE + 3] != 0) { napaka_VALUE("file stream already initialized"); return; }
            int 길이 = kopica_VALUE[Datoteka_vnos_ime + 1];
            if (길이 < 1 || 길이 > 63) { napaka_VALUE("invalid file name length"); return; }
            for (int 칸 = 0; 칸 < 길이; 칸++) {
                int VALUE = kopica_VALUE[Datoteka_vnos_ime + 2 + 칸];
                if (VALUE < 1) { napaka_VALUE("invalid file stream path"); return; }
                tok_ime_datoteke[칸] = VALUE;
            }
            tok_ime_datoteke[길이] = 0;
            int 서술자 = uporabnik.파일서술자열기(tok_ime_datoteke, Izpis ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { napaka_VALUE("FileNotFoundException: file open failed"); return; }
            kopica_VALUE[tok_VALUE + 2] = 서술자; kopica_VALUE[tok_VALUE + 3] = 1;
            return;
        }
        if (Ukaz != 182) { napaka_VALUE("invalid file stream invocation"); return; }
        if ((Izpis && Word_SMS(Ime, "write") || !Izpis && Word_SMS(Ime, "read"))
            && (Word_SMS(oblika_VALUE, Izpis ? "([B)V" : "([B)I") || Word_SMS(oblika_VALUE, Izpis ? "([BII)V" : "([BII)I"))) {
            boolean izrezek_VALUE = Word_SMS(oblika_VALUE, Izpis ? "([BII)V" : "([BII)I");
            int vnos_COUNT = izrezek_VALUE ? 빼기(1) : 0, 시작점 = izrezek_VALUE ? 빼기(1) : 0, podatki_ARRAY = 빼기(2), predmet_Gradiva = 빼기(2);
            if (!predmet_VALUE(podatki_ARRAY, 20) || !predmet_VALUE(predmet_Gradiva, 종류)) return;
            if (!izrezek_VALUE) vnos_COUNT = kopica_VALUE[podatki_ARRAY + 1];
            if (시작점 < 0 || vnos_COUNT < 0 || 시작점 > kopica_VALUE[podatki_ARRAY + 1] - vnos_COUNT) { 예외던짐(6, "file buffer bounds"); return; }
            if (kopica_VALUE[predmet_Gradiva + 3] == 0 || kopica_VALUE[predmet_Gradiva + 2] < 0) { napaka_VALUE("IOException: stream closed"); return; }
            int Dokončano_COUNT = 0;
            while (Dokončano_COUNT < vnos_COUNT && !NAPAKA) {
                int 반환값 = Izpis ? uporabnik.파일한바이트쓰기(kopica_VALUE[predmet_Gradiva + 2], kopica_VALUE[podatki_ARRAY + 2 + 시작점 + Dokončano_COUNT]) : uporabnik.파일한바이트읽기(kopica_VALUE[predmet_Gradiva + 2]);
                if (반환값 < 0) { napaka_VALUE(Izpis ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!Izpis && 반환값 == 256) break;
                if (!Izpis) kopica_VALUE[podatki_ARRAY + 2 + 시작점 + Dokončano_COUNT] = (byte)반환값;
                Dokončano_COUNT++;
            }
            if (!Izpis) 넣기(vnos_COUNT != 0 && Dokončano_COUNT == 0 ? -1 : Dokončano_COUNT, 1);
            return;
        }
        if (Izpis && Word_SMS(Ime, "flush") && Word_SMS(oblika_VALUE, "()V")) { int predmet_Gradiva = 빼기(2); if (predmet_VALUE(predmet_Gradiva, 종류) && kopica_VALUE[predmet_Gradiva + 2] < 0) napaka_VALUE("IOException: stream closed"); return; }
        int Dejanje = -1, VALUE = 0;
        if (Word_SMS(Ime, "close") && Word_SMS(oblika_VALUE, "()V")) Dejanje = 0;
        if (!Izpis && Word_SMS(Ime, "read") && Word_SMS(oblika_VALUE, "()I")) Dejanje = 1;
        if (Izpis && Word_SMS(Ime, "write") && Word_SMS(oblika_VALUE, "(I)V")) { Dejanje = 2; VALUE = 빼기(1); }
        if (Dejanje < 0) { napaka_VALUE("unsupported file stream method"); return; }
        int tok_VALUE = 빼기(2);
        if (!predmet_VALUE(tok_VALUE, 종류) || NAPAKA) return;
        if (kopica_VALUE[tok_VALUE + 3] == 0) { napaka_VALUE("uninitialized file stream"); return; }
        int 서술자 = kopica_VALUE[tok_VALUE + 2];
        if (Dejanje == 0) {
            if (서술자 >= 0 && uporabnik.파일서술자닫기(서술자) < 0) napaka_VALUE("IOException: close failed");
            kopica_VALUE[tok_VALUE + 2] = -1; return;
        }
        if (서술자 < 0) { napaka_VALUE("IOException: stream closed"); return; }
        if (Dejanje == 1) {
            int REZULTAT = uporabnik.파일한바이트읽기(서술자);
            if (REZULTAT < -1) napaka_VALUE("IOException: read failed"); else 넣기(REZULTAT == 256 ? -1 : REZULTAT, 1);
        } else if (uporabnik.파일한바이트쓰기(서술자, VALUE) != 1) napaka_VALUE("IOException: write failed");
    }
    static void CALL_metoda(int INDEX, int Ukaz) {
        if (INDEX <= 0 || INDEX >= konstanta_oznaka.length || (konstanta_oznaka[INDEX] != 10 && konstanta_oznaka[INDEX] != 11)) { napaka_VALUE("invalid method reference"); return; }
        int lastnik_VALUE = ime_razreda_SMS(상가[INDEX]), Ime = Gradiva_ime(konstanta_SECOND_VALUE[INDEX]), oblika_VALUE = Gradiva_Tip(konstanta_SECOND_VALUE[INDEX]);
        if (NAPAKA) return;
        if (기본호출(lastnik_VALUE, Ime, oblika_VALUE, Ukaz)) return;
        if (Word_SMS(lastnik_VALUE, "java/io/FileInputStream") || Word_SMS(lastnik_VALUE, "java/io/FileOutputStream")) {
            Datoteka_tok_CALL(lastnik_VALUE, Ime, oblika_VALUE, Ukaz); return;
        }
        if (Ukaz == 184 && Word_SMS(lastnik_VALUE, "java/lang/Integer") && Word_SMS(Ime, "parseInt") && Word_SMS(oblika_VALUE, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (Ukaz == 182 && Word_SMS(lastnik_VALUE, "java/io/PrintStream") && (Word_SMS(Ime, "println") || Word_SMS(Ime, "print"))) {
            int Tip_VALUE = 0, VALUE = 0;
            if (Word_SMS(oblika_VALUE, "(I)V")) { Tip_VALUE = 1; VALUE = 빼기(1); }
            else if (Word_SMS(oblika_VALUE, "(Z)V")) { Tip_VALUE = 2; VALUE = 빼기(1); }
            else if (Word_SMS(oblika_VALUE, "(C)V")) { Tip_VALUE = 3; VALUE = 빼기(1); }
            else if (Word_SMS(oblika_VALUE, "(Ljava/lang/String;)V")) { Tip_VALUE = 4; VALUE = 빼기(2); }
            else if (!Word_SMS(oblika_VALUE, "()V") || !Word_SMS(Ime, "println")) napaka_VALUE("unsupported print descriptor");
            if (빼기(2) != -1) napaka_VALUE("invalid PrintStream receiver");
            if (NAPAKA) return;
            if (Tip_VALUE == 1) 자바도구.수쓰기(VALUE);
            if (Tip_VALUE == 2) uporabnik.Pisanje(VALUE == 0 ? "false" : "true");
            if (Tip_VALUE == 3) uporabnik.pisati_znak_VALUE(VALUE & 65535);
            if (Tip_VALUE == 4) pisati_SMS(VALUE);
            if (Word_SMS(Ime, "println")) uporabnik.pisati_znak_VALUE(10);
            return;
        }
        if (Ukaz == 182 && Word_SMS(lastnik_VALUE, "java/lang/String")) {
            if (Word_SMS(Ime, "length") && Word_SMS(oblika_VALUE, "()I")) {
                int Gradiva = 빼기(2); if (predmet_VALUE(Gradiva, 1)) 넣기(kopica_VALUE[Gradiva + 1], 1); return;
            }
            if (Word_SMS(Ime, "charAt") && Word_SMS(oblika_VALUE, "(I)C")) {
                int podpisano_VALUE = 빼기(1), Gradiva = 빼기(2);
                if (predmet_VALUE(Gradiva, 1)) {
                    if (podpisano_VALUE < 0 || podpisano_VALUE >= kopica_VALUE[Gradiva + 1]) napaka_VALUE("StringIndexOutOfBoundsException"); else 넣기(kopica_VALUE[Gradiva + 2 + podpisano_VALUE], 1);
                }
                return;
            }
        }
        if (Word_SMS(lastnik_VALUE, "java/lang/StringBuilder")) {
            if (Ukaz == 183 && Word_SMS(Ime, "<init>") && Word_SMS(oblika_VALUE, "()V")) { predmet_VALUE(빼기(2), 4); return; }
            if (Ukaz == 182 && Word_SMS(Ime, "toString") && Word_SMS(oblika_VALUE, "()Ljava/lang/String;")) {
                int Gradiva = 빼기(2); if (predmet_VALUE(Gradiva, 4)) 넣기(kopica_VALUE[Gradiva + 2] == 0 ? gostiti_znak("") : kopica_VALUE[Gradiva + 2], 2); return;
            }
            if (Ukaz == 182 && Word_SMS(Ime, "append")) {
                int Besedilo = 0;
                if (Word_SMS(oblika_VALUE, "(I)Ljava/lang/StringBuilder;")) Besedilo = številka_znak(빼기(1));
                else if (Word_SMS(oblika_VALUE, "(Z)Ljava/lang/StringBuilder;")) Besedilo = gostiti_znak(빼기(1) == 0 ? "false" : "true");
                else if (Word_SMS(oblika_VALUE, "(C)Ljava/lang/StringBuilder;")) {
                    int VALUE = 빼기(1); Besedilo = dodeliti_Senzor_prostora(1, 1); if (!NAPAKA) kopica_VALUE[Besedilo + 2] = VALUE & 65535;
                }
                else if (Word_SMS(oblika_VALUE, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { Besedilo = 빼기(2); if (Besedilo == 0) Besedilo = gostiti_znak("null"); }
                else { napaka_VALUE("unsupported StringBuilder append"); return; }
                int Gradiva = 빼기(2); if (!predmet_VALUE(Gradiva, 4) || !predmet_VALUE(Besedilo, 1)) return;
                int sprednja_VALUE = kopica_VALUE[Gradiva + 2], 앞길이 = sprednja_VALUE == 0 ? 0 : kopica_VALUE[sprednja_VALUE + 1], 뒤길이 = kopica_VALUE[Besedilo + 1];
                int 새글 = dodeliti_Senzor_prostora(1, 앞길이 + 뒤길이); if (NAPAKA) return;
                for (int 수 = 0; 수 < 앞길이; 수++) kopica_VALUE[새글 + 2 + 수] = kopica_VALUE[sprednja_VALUE + 2 + 수];
                for (int 수 = 0; 수 < 뒤길이; 수++) kopica_VALUE[새글 + 2 + 앞길이 + 수] = kopica_VALUE[Besedilo + 2 + 수];
                kopica_VALUE[Gradiva + 2] = 새글; 넣기(Gradiva, 2); return;
            }
        }
        int Razred_definicija = FIND_Razred_definicija(lastnik_VALUE); if (Razred_definicija < 0 || NAPAKA) return;
        int Datoteka_INDEX = FIND_metoda(Razred_definicija, Ime, oblika_VALUE);
        if (Datoteka_INDEX < 0) {
            for (int koda_znaka = Razred_definicija, vnos_COUNT = 0; koda_znaka >= 0 && vnos_COUNT < 16; vnos_COUNT++, koda_znaka = nadrejen_Razred(koda_znaka))
                if (Word_SMS(Razred_definicija_nadrejen[koda_znaka], "java/lang/Thread")) { 가닥호출(Ime, oblika_VALUE, Ukaz); return; }
            napaka_VALUE("NoSuchMethodError"); return;
        }
        if (((metoda_dostop[Datoteka_INDEX] & 8) != 0) != (Ukaz == 184)) { napaka_VALUE("method static/instance mismatch"); return; }
        if (Ukaz == 184) { if (!inicializirati(metoda_lastnik[Datoteka_INDEX], okvir_navodilo[okvir_INDEX])) return; }
        else {
            int 읽는자리 = okvir_Sklad[okvir_INDEX] - metoda_argument_COUNT[Datoteka_INDEX];
            if (읽는자리 < 0 || operand_Sklad_Tip[okvir_INDEX * 128 + 읽는자리] != 2) { napaka_VALUE("invalid method receiver"); return; }
            int predmet_Gradiva = operand_Sklad_VALUE[okvir_INDEX * 128 + 읽는자리];
            if (!객체유효(predmet_Gradiva)) return;
            if (kopica_VALUE[predmet_Gradiva] < 32 || !종포함(kopica_VALUE[predmet_Gradiva] - 32, lastnik_VALUE)) { napaka_VALUE("method receiver type mismatch"); return; }
            if (Ukaz != 183) Datoteka_INDEX = FIND_metoda(kopica_VALUE[predmet_Gradiva] - 32, Ime, oblika_VALUE);
        }
        if (Datoteka_INDEX < 0 || (metoda_dostop[Datoteka_INDEX] & 0x400) != 0) { napaka_VALUE("AbstractMethodError"); return; }
        int zaklepanje_Gradiva = 0;
        if ((metoda_dostop[Datoteka_INDEX] & 32) != 0) {
            if (Ukaz == 184) { int koda_znaka = metoda_lastnik[Datoteka_INDEX]; if (Razred_zaklepanje[koda_znaka] == 0) Razred_zaklepanje[koda_znaka] = dodeliti_Senzor_prostora(8, 0); zaklepanje_Gradiva = Razred_zaklepanje[koda_znaka]; }
            else zaklepanje_Gradiva = operand_Sklad_VALUE[okvir_INDEX * 128 + okvir_Sklad[okvir_INDEX] - metoda_argument_COUNT[Datoteka_INDEX]];
            if (!잠금얻기(zaklepanje_Gradiva)) { if (!NAPAKA) okvir_položaj[okvir_INDEX] = okvir_navodilo[okvir_INDEX]; return; }
        }
        호출(Datoteka_INDEX); if (!NAPAKA) okvir_zaklepanje[okvir_INDEX] = zaklepanje_Gradiva;
    }
    static boolean 배열저장가능(int ARRAY_Gradiva, int podatki_VALUE) {
        if (podatki_VALUE == 0 || element_polja[ARRAY_Gradiva] == 0) return true;
        boolean 성공여부 = element_polja[ARRAY_Gradiva] == -1 ? (podatki_VALUE > 0 && podatki_VALUE < kopica_končati_klic_položaj && kopica_VALUE[podatki_VALUE] == 1) : 맞는객체(podatki_VALUE, element_polja[ARRAY_Gradiva]);
        if (!성공여부 && !NAPAKA) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int 배열칸(int Gradiva, int podpisano_VALUE, int Tip_VALUE) {
        if (!predmet_VALUE(Gradiva, Tip_VALUE)) return 0;
        if (podpisano_VALUE < 0 || podpisano_VALUE >= kopica_VALUE[Gradiva + 1]) { napaka_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return Gradiva + 2 + podpisano_VALUE;
    }
    static void Izvedi_ukaz() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (NAPAKA) { if (던진객체 != 0) ročica_izjema(); if (NAPAKA || okvir_INDEX < sprotno_nit * 32) break; }
            if (okvir_INDEX < sprotno_nit * 32 || spremeniti_zahteva || --조각 == 0) { if (!SWITCH_nit()) break; 조각 = 100; }
            if (okvir_INDEX == 0 && Razred_definicija_stanje[vnos_Razred_definicija] != 2 && !inicializirati(vnos_Razred_definicija, okvir_položaj[okvir_INDEX])) continue;
            if (okvir_INDEX == sprotno_nit * 32 && sprotno_nit != 0 && (metoda_dostop[okvir_metoda[okvir_INDEX]] & 32) != 0 && okvir_zaklepanje[okvir_INDEX] == 0) {
                int predmet_Gradiva = nit_cilj[sprotno_nit]; if (!잠금얻기(predmet_Gradiva)) { if (NAPAKA) break; continue; } okvir_zaklepanje[okvir_INDEX] = predmet_Gradiva;
            }
            잠시수 = 0;
            if (--남음 == 0) { napaka_VALUE("instruction limit (500000)"); break; }
            int Zaženi = okvir_položaj[okvir_INDEX]; okvir_navodilo[okvir_INDEX] = Zaženi; int VALUE = 명바();
            if (NAPAKA) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int 수 = metoda_lastnik[okvir_metoda[okvir_INDEX]] * 512 + (VALUE == 18 ? 명바() : 명짧());
                if (수 <= 0 || 수 >= konstanta_oznaka.length) napaka_VALUE("invalid ldc constant");
                else if (konstanta_oznaka[수] == 3) 넣기(상가[수], 1);
                else if (konstanta_oznaka[수] == 8) 넣기(konstanta_SMS(상가[수]), 2);
                else napaka_VALUE("unsupported ldc constant");
                continue;
            }
            if (VALUE == 21 || VALUE == 25) { 지역읽기(명바(), VALUE == 21 ? 1 : 2); continue; }
            if (VALUE >= 26 && VALUE <= 29) { 지역읽기(VALUE - 26, 1); continue; }
            if (VALUE >= 42 && VALUE <= 45) { 지역읽기(VALUE - 42, 2); continue; }
            if (VALUE == 54 || VALUE == 58) { pisati_lokalen_krajeven(명바(), VALUE == 54 ? 1 : 2); continue; }
            if (VALUE >= 59 && VALUE <= 62) { pisati_lokalen_krajeven(VALUE - 59, 1); continue; }
            if (VALUE >= 75 && VALUE <= 78) { pisati_lokalen_krajeven(VALUE - 75, 2); continue; }
            if (VALUE == 46 || VALUE >= 50 && VALUE <= 53) {
                int vnos_položaj = 빼기(1), predmet_Gradiva = 빼기(2), območje_CODE = VALUE == 46 ? 2 : VALUE == 50 ? 3 : VALUE == 51 ? 20 : VALUE == 52 ? 22 : 23;
                if (VALUE == 51 && predmet_Gradiva > 0 && predmet_Gradiva < kopica_končati_klic_položaj && kopica_VALUE[predmet_Gradiva] == 21) območje_CODE = 21;
                int 읽는자리 = 배열칸(predmet_Gradiva, vnos_položaj, območje_CODE); if (!NAPAKA) 넣기(kopica_VALUE[읽는자리], VALUE == 50 ? 2 : 1); continue;
            }
            if (VALUE == 79 || VALUE >= 83 && VALUE <= 86) {
                int vnos_Gradiva = 빼기(VALUE == 83 ? 2 : 1), vnos_položaj = 빼기(1), predmet_Gradiva = 빼기(2), območje_CODE = VALUE == 79 ? 2 : VALUE == 83 ? 3 : VALUE == 84 ? 20 : VALUE == 85 ? 22 : 23;
                if (VALUE == 84 && predmet_Gradiva > 0 && predmet_Gradiva < kopica_končati_klic_položaj && kopica_VALUE[predmet_Gradiva] == 21) območje_CODE = 21;
                int 읽는자리 = 배열칸(predmet_Gradiva, vnos_položaj, območje_CODE);
                if (!NAPAKA && območje_CODE == 3 && !배열저장가능(predmet_Gradiva, vnos_Gradiva)) continue;
                if (!NAPAKA) kopica_VALUE[읽는자리] = območje_CODE == 20 ? (byte)vnos_Gradiva : območje_CODE == 21 ? vnos_Gradiva & 1 : območje_CODE == 22 ? (char)vnos_Gradiva : območje_CODE == 23 ? (short)vnos_Gradiva : vnos_Gradiva;
                continue;
            }
            if (VALUE >= 87 && VALUE <= 95) { Sklad_navodilo(VALUE); continue; }
            if (VALUE == 96 || VALUE == 100 || VALUE == 104 || VALUE == 108 || VALUE == 112 || VALUE == 120
                || VALUE == 122 || VALUE == 124 || VALUE == 126 || VALUE == 128 || VALUE == 130) {
                int SECOND_operand = 빼기(1), 가 = 빼기(1), REZULTAT = 0;
                if ((VALUE == 108 || VALUE == 112) && SECOND_operand == 0) { napaka_VALUE("ArithmeticException: / by zero"); continue; }
                if (VALUE == 96) REZULTAT = 가 + SECOND_operand;
                if (VALUE == 100) REZULTAT = 가 - SECOND_operand;
                if (VALUE == 104) REZULTAT = 가 * SECOND_operand;
                if (VALUE == 108) REZULTAT = 가 / SECOND_operand;
                if (VALUE == 112) REZULTAT = 가 % SECOND_operand;
                if (VALUE == 120) REZULTAT = 가 << SECOND_operand;
                if (VALUE == 122) REZULTAT = 가 >> SECOND_operand;
                if (VALUE == 124) REZULTAT = 가 >>> SECOND_operand;
                if (VALUE == 126) REZULTAT = 가 & SECOND_operand;
                if (VALUE == 128) REZULTAT = 가 | SECOND_operand;
                if (VALUE == 130) REZULTAT = 가 ^ SECOND_operand;
                넣기(REZULTAT, 1); continue;
            }
            if (VALUE == 116) { 넣기(-빼기(1), 1); continue; }
            if (VALUE == 132) {
                int lokalen_krajeven_obseg = 명바(), 증분 = (byte)명바(); 지역읽기(lokalen_krajeven_obseg, 1); 넣기(빼기(1) + 증분, 1); pisati_lokalen_krajeven(lokalen_krajeven_obseg, 1); continue;
            }
            if (VALUE >= 145 && VALUE <= 147) {
                int 수 = 빼기(1); 넣기(VALUE == 145 ? (byte)수 : VALUE == 146 ? (char)수 : (short)수, 1); continue;
            }
            if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                int cilj_VALUE = Zaženi + (short)명짧(); boolean 갈까 = VALUE == 167;
                if (VALUE >= 153 && VALUE <= 158) {
                    int 수 = 빼기(1); 갈까 = VALUE == 153 ? 수 == 0 : VALUE == 154 ? 수 != 0 : VALUE == 155 ? 수 < 0 : VALUE == 156 ? 수 >= 0 : VALUE == 157 ? 수 > 0 : 수 <= 0;
                } else if (VALUE >= 159 && VALUE <= 166) {
                    int SECOND_operand = 빼기(VALUE >= 165 ? 2 : 1), 가 = 빼기(VALUE >= 165 ? 2 : 1);
                    갈까 = VALUE == 159 || VALUE == 165 ? 가 == SECOND_operand : VALUE == 160 || VALUE == 166 ? 가 != SECOND_operand : VALUE == 161 ? 가 < SECOND_operand : VALUE == 162 ? 가 >= SECOND_operand : VALUE == 163 ? 가 > SECOND_operand : 가 <= SECOND_operand;
                } else if (VALUE == 198 || VALUE == 199) { int 수 = 빼기(2); 갈까 = VALUE == 198 ? 수 == 0 : 수 != 0; }
                if (갈까) premikati_VALUE(cilj_VALUE); continue;
            }
            if (VALUE == 172 || VALUE == 176 || VALUE == 177) { vrni_KR(VALUE == 172 ? 1 : VALUE == 176 ? 2 : 0); continue; }
            if (VALUE >= 178 && VALUE <= 181) { 필드호출(명상수(), VALUE, Zaženi); continue; }
            if (VALUE >= 182 && VALUE <= 185) {
                int 부호값 = 명상수();
                if (VALUE == 185) { int skupaj_COUNT = 명바(); if (skupaj_COUNT == 0 || 명바() != 0) { napaka_VALUE("invalid invokeinterface operands"); continue; } }
                CALL_metoda(부호값, VALUE); continue;
            }
            if (VALUE == 187) { 새객체(ime_razreda_SMS(명상수()), Zaženi); continue; }
            if (VALUE == 188 || VALUE == 189) {
                int območje_CODE = 3, komponenta = 0;
                if (VALUE == 188) { int 임시값 = 명바(); območje_CODE = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else komponenta = ime_razreda_SMS(명상수());
                if (območje_CODE == 0) { napaka_VALUE("unsupported primitive array type"); continue; }
                int 유효길이 = 빼기(1), predmet_Gradiva = dodeliti_Senzor_prostora(območje_CODE, 유효길이); if (!NAPAKA) element_polja[predmet_Gradiva] = komponenta; 넣기(predmet_Gradiva, 2); continue;
            }
            if (VALUE == 190) {
                int predmet_Gradiva = 빼기(2);
                if (객체유효(predmet_Gradiva)) { int Primerjava_položaj = kopica_VALUE[predmet_Gradiva]; if (Primerjava_položaj != 2 && Primerjava_položaj != 3 && (Primerjava_položaj < 20 || Primerjava_položaj > 23)) napaka_VALUE("not an array"); else 넣기(kopica_VALUE[predmet_Gradiva + 1], 1); }
                continue;
            }
            if (VALUE == 191) {
                int predmet_Gradiva = 빼기(2); if (객체유효(predmet_Gradiva)) { if (kopica_VALUE[predmet_Gradiva] != 9) napaka_VALUE("athrow requires supported Throwable"); else { 던진객체 = predmet_Gradiva; NAPAKA = true; } }
                continue;
            }
            if (VALUE == 192 || VALUE == 193) {
                int ime_konstanta = ime_razreda_SMS(명상수()), predmet_Gradiva = 빼기(2); boolean MATCH = 맞는객체(predmet_Gradiva, ime_konstanta);
                if (VALUE == 193) 넣기(predmet_Gradiva != 0 && MATCH ? 1 : 0, 1);
                else { if (!MATCH && !NAPAKA) napaka_VALUE("ClassCastException"); 넣기(predmet_Gradiva, 2); }
                continue;
            }
            if (VALUE == 170 || VALUE == 171) {
                int 읽는자리 = Zaženi + 1, Datoteka_INDEX = okvir_metoda[okvir_INDEX], Ključ_Gradiva = 빼기(1);
                while ((읽는자리 - metoda_Start[Datoteka_INDEX]) % 4 != 0) 읽는자리++;
                int cilj_naslov = položaj_celo_število(읽는자리);
                if (VALUE == 170) { int 낮은값 = položaj_celo_število(읽는자리 + 4), 높은값 = položaj_celo_število(읽는자리 + 8); if (Ključ_Gradiva >= 낮은값 && Ključ_Gradiva <= 높은값) cilj_naslov = položaj_celo_število(읽는자리 + 12 + (Ključ_Gradiva - 낮은값) * 4); }
                else { int skupaj_COUNT = položaj_celo_število(읽는자리 + 4); for (int Loop_INDEX = 0; Loop_INDEX < skupaj_COUNT; Loop_INDEX++) if (položaj_celo_število(읽는자리 + 8 + Loop_INDEX * 8) == Ključ_Gradiva) cilj_naslov = položaj_celo_število(읽는자리 + 12 + Loop_INDEX * 8); }
                premikati_VALUE(Zaženi + cilj_naslov); continue;
            }
            if (VALUE == 200) { premikati_VALUE(Zaženi + položaj_celo_število(Zaženi + 1)); continue; }
            if (VALUE == 194 || VALUE == 195) {
                int predmet_Gradiva = 빼기(2);
                if (VALUE == 195) izdaja_zaklepanje(predmet_Gradiva);
                else if (!잠금얻기(predmet_Gradiva) && !NAPAKA) { 넣기(predmet_Gradiva, 2); okvir_položaj[okvir_INDEX] = Zaženi; }
                continue;
            }
            if (VALUE == 196) {
                int ukaz_CODE = 명바(), vnos_položaj = 명짧();
                if (ukaz_CODE == 21 || ukaz_CODE == 25) 지역읽기(vnos_položaj, ukaz_CODE == 21 ? 1 : 2);
                else if (ukaz_CODE == 54 || ukaz_CODE == 58) pisati_lokalen_krajeven(vnos_položaj, ukaz_CODE == 54 ? 1 : 2);
                else if (ukaz_CODE == 132) { int DELTA_VALUE = (short)명짧(); 지역읽기(vnos_položaj, 1); 넣기(빼기(1) + DELTA_VALUE, 1); pisati_lokalen_krajeven(vnos_položaj, 1); }
                else napaka_VALUE("unsupported wide opcode");
                continue;
            }
            napaka_VALUE("unsupported bytecode");
        }
    }
    static int FIND_Razred_definicija(int Ime) {
        for (int Loop_INDEX = 0; Loop_INDEX < Razred_definicija_COUNT; Loop_INDEX++) if (Razred_definicija_ime[Loop_INDEX] != 0 && 같은말(Razred_definicija_ime[Loop_INDEX], Ime)) return Loop_INDEX;
        return zbirka_Razred_definicija(konstanta_SMS(Ime));
    }
    static int zbirka_Razred_definicija(int ime_niz) {
        if (!predmet_VALUE(ime_niz, 1)) return -1;
        int 길이 = kopica_VALUE[ime_niz + 1];
        if (길이 < 1 || 길이 > 505 || Razred_definicija_COUNT == 16) { napaka_VALUE("class name/count limit"); return -1; }
        for (int Loop_INDEX = 0; Loop_INDEX < 길이; Loop_INDEX++) { int koda_znaka = kopica_VALUE[ime_niz + 2 + Loop_INDEX]; ime_datoteke_SMS[Loop_INDEX] = koda_znaka == '/' ? '.' : koda_znaka; }
        ime_datoteke_SMS[길이] = '.'; ime_datoteke_SMS[길이 + 1] = 'c'; ime_datoteke_SMS[길이 + 2] = 'l'; ime_datoteke_SMS[길이 + 3] = 'a'; ime_datoteke_SMS[길이 + 4] = 's'; ime_datoteke_SMS[길이 + 5] = 's'; ime_datoteke_SMS[길이 + 6] = 0;
        int Velikost = uporabnik.파일읽기(ime_datoteke_SMS, začasna_datoteka);
        if (Velikost < 0) { napaka_VALUE("ClassNotFoundException"); return -1; }
        int Razred_definicija = Razred_definicija_COUNT++; Razred_definicija_spremeniti_velikost[Razred_definicija] = Velikost;
        for (int Loop_INDEX = 0; Loop_INDEX < Velikost; Loop_INDEX++) Datoteka[Razred_definicija * 16384 + Loop_INDEX] = začasna_datoteka[Loop_INDEX];
        클래스읽기(Razred_definicija); if (NAPAKA) return -1;
        int dejanski_podatki = konstanta_SMS(Razred_definicija_ime[Razred_definicija]);
        if (!글같음(dejanski_podatki, ime_niz, true)) { napaka_VALUE("class name does not match file"); return -1; }
        int nadrejen_VALUE = Razred_definicija_nadrejen[Razred_definicija];
        if (nadrejen_VALUE != 0 && !Word_SMS(nadrejen_VALUE, "java/lang/Object") && !Word_SMS(nadrejen_VALUE, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 znova_poskusiti_VALUE 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = FIND_Razred_definicija(nadrejen_VALUE);
            if (NAPAKA || 위 < 0) return -1;
            int 읽는자리 = 위, območje_COUNT = 0;
            while (읽는자리 >= 0 && območje_COUNT++ < 16) {
                if (읽는자리 == Razred_definicija) { napaka_VALUE("cyclic inheritance"); return -1; }
                읽는자리 = nadrejen_Razred(읽는자리);
            }
            int 시작변위 = 종칸수[위];
            for (int Datoteka_INDEX = 0; Datoteka_INDEX < 칸수; Datoteka_INDEX++) if (칸주인[Datoteka_INDEX] == Razred_definicija && (칸권한[Datoteka_INDEX] & 8) == 0) 칸위치[Datoteka_INDEX] += 시작변위;
            종칸수[Razred_definicija] += 시작변위;
        }
        return Razred_definicija;
    }
    static int nadrejen_Razred(int Razred_definicija) {
        int Ime = Razred_definicija_nadrejen[Razred_definicija];
        for (int Loop_INDEX = 0; Loop_INDEX < Razred_definicija_COUNT; Loop_INDEX++) if (Ime != 0 && Razred_definicija_ime[Loop_INDEX] != 0 && 같은말(Razred_definicija_ime[Loop_INDEX], Ime)) return Loop_INDEX;
        return -1;
    }
    static int FIND_metoda(int Razred_definicija, int Ime, int oblika_VALUE) {
        for (int 깊이 = 0; Razred_definicija >= 0 && 깊이 < 16; 깊이++, Razred_definicija = nadrejen_Razred(Razred_definicija)) {
            for (int Loop_INDEX = 0; Loop_INDEX < metoda_COUNT; Loop_INDEX++) if (metoda_lastnik[Loop_INDEX] == Razred_definicija && 같은말(metoda_ime_SMS[Loop_INDEX], Ime) && 같은말(metoda_Tip[Loop_INDEX], oblika_VALUE)) return Loop_INDEX;
        }
        return -1;
    }
    static int ime_metoda(int Razred_definicija, String Ime, String oblika_VALUE) {
        for (int 깊이 = 0; Razred_definicija >= 0 && 깊이 < 16; 깊이++, Razred_definicija = nadrejen_Razred(Razred_definicija))
            for (int Loop_INDEX = 0; Loop_INDEX < metoda_COUNT; Loop_INDEX++) if (metoda_lastnik[Loop_INDEX] == Razred_definicija && Word_SMS(metoda_ime_SMS[Loop_INDEX], Ime) && Word_SMS(metoda_Tip[Loop_INDEX], oblika_VALUE)) return Loop_INDEX;
        return -1;
    }
    static int 형종류(int Ime) { return Datoteka[상가[Ime]] == 'L' || Datoteka[상가[Ime]] == '[' ? 2 : 1; }
    static boolean inicializirati(int Razred_definicija, int ukaz_Start) {
        if (Razred_definicija < 0 || NAPAKA) return false;
        if (Razred_definicija_stanje[Razred_definicija] == 3) { napaka_VALUE("NoClassDefFoundError: initialization failed"); return false; }
        if (Razred_definicija_stanje[Razred_definicija] == 1 && Razred_nit[Razred_definicija] != sprotno_nit) { okvir_položaj[okvir_INDEX] = ukaz_Start; spremeniti_zahteva = true; return false; }
        if (Razred_definicija_stanje[Razred_definicija] != 0) return true;
        int 위 = nadrejen_Razred(Razred_definicija);
        if (위 >= 0 && !inicializirati(위, ukaz_Start)) return false;
        Razred_definicija_stanje[Razred_definicija] = 1; Razred_nit[Razred_definicija] = sprotno_nit;
        if (inicializirati_Razred_definicija[Razred_definicija] != 0) {
            okvir_položaj[okvir_INDEX] = ukaz_Start;
            호출(inicializirati_Razred_definicija[Razred_definicija] - 1); if (!NAPAKA) inicializirati_okvir[okvir_INDEX] = Razred_definicija + 1;
            return false;
        }
        Razred_definicija_stanje[Razred_definicija] = 2; return true;
    }
    static void 필드호출(int INDEX, int Ukaz, int Zaženi) {
        if (!preveriti_konstanta(INDEX, 9)) return;
        int lastnik_VALUE = ime_razreda_SMS(상가[INDEX]), Ime = Gradiva_ime(konstanta_SECOND_VALUE[INDEX]), oblika_VALUE = Gradiva_Tip(konstanta_SECOND_VALUE[INDEX]);
        if (Word_SMS(lastnik_VALUE, "java/lang/System") && (Word_SMS(Ime, "out") || Word_SMS(Ime, "err")) && Word_SMS(oblika_VALUE, "Ljava/io/PrintStream;") && Ukaz == 178) { 넣기(-1, 2); return; }
        int Razred_definicija = FIND_Razred_definicija(lastnik_VALUE); if (Razred_definicija < 0 || NAPAKA) return;
        int 찾음 = -1;
        for (int 읽는자리 = Razred_definicija, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = nadrejen_Razred(읽는자리))
            for (int Datoteka_INDEX = 0; Datoteka_INDEX < 칸수; Datoteka_INDEX++) if (칸주인[Datoteka_INDEX] == 읽는자리 && 같은말(칸이름[Datoteka_INDEX], Ime) && 같은말(칸형[Datoteka_INDEX], oblika_VALUE)) 찾음 = Datoteka_INDEX;
        if (찾음 < 0) { napaka_VALUE("NoSuchFieldError"); return; }
        boolean statičen_VALUE = Ukaz == 178 || Ukaz == 179;
        if (statičen_VALUE != ((칸권한[찾음] & 8) != 0)) { napaka_VALUE("field static/instance mismatch"); return; }
        if (statičen_VALUE && !inicializirati(칸주인[찾음], Zaženi)) return;
        int Tip_VALUE = 형종류(oblika_VALUE), VALUE = 0;
        if (Ukaz == 179 || Ukaz == 181) VALUE = 빼기(Tip_VALUE);
        if (statičen_VALUE) { if (Ukaz == 178) 넣기(칸값[찾음], Tip_VALUE); else if (!NAPAKA) 칸값[찾음] = VALUE; return; }
        int predmet_Gradiva = 빼기(2);
        if (!객체유효(predmet_Gradiva)) return;
        if (kopica_VALUE[predmet_Gradiva] < 32 || !종포함(kopica_VALUE[predmet_Gradiva] - 32, lastnik_VALUE)) { napaka_VALUE("field receiver type mismatch"); return; }
        int 보관칸 = predmet_Gradiva + 2 + 칸위치[찾음];
        if (Ukaz == 180) 넣기(kopica_VALUE[보관칸], Tip_VALUE);
        else if (!NAPAKA) { kopica_VALUE[보관칸] = VALUE; kopica_Gradiva[보관칸] = Tip_VALUE == 2 ? 1 : 0; }
    }
    static boolean 종포함(int Razred_definicija, int Ime) {
        for (int 중첩깊이 = 0; Razred_definicija >= 0 && 중첩깊이 < 16; 중첩깊이++, Razred_definicija = nadrejen_Razred(Razred_definicija)) {
            if (같은말(Razred_definicija_ime[Razred_definicija], Ime) || (Razred_definicija_nadrejen[Razred_definicija] != 0 && 같은말(Razred_definicija_nadrejen[Razred_definicija], Ime))) return true;
            for (int notranje_položaj = 0; notranje_položaj < Razred_vmesnik_COUNT[Razred_definicija]; notranje_položaj++) if (같은말(Razred_vmesnik[Razred_definicija * 16 + notranje_položaj], Ime)) return true;
        }
        return false;
    }
    static boolean 글같음(int 첫값, int bajt_podatki, boolean POT) {
        if (첫값 == bajt_podatki) return true;
        if (첫값 <= 0 || bajt_podatki <= 0 || kopica_VALUE[첫값] != 1 || kopica_VALUE[bajt_podatki] != 1 || kopica_VALUE[첫값 + 1] != kopica_VALUE[bajt_podatki + 1]) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < kopica_VALUE[첫값 + 1]; Loop_INDEX++) {
            int koordinata_x = kopica_VALUE[첫값 + 2 + Loop_INDEX], 세로좌표 = kopica_VALUE[bajt_podatki + 2 + Loop_INDEX];
            if (POT) { if (koordinata_x == '.') koordinata_x = '/'; if (세로좌표 == '.') 세로좌표 = '/'; }
            if (koordinata_x != 세로좌표) return false;
        }
        return true;
    }
    static boolean 객체유효(int predmet_Gradiva) {
        if (predmet_Gradiva == 0) { napaka_VALUE("NullPointerException"); return false; }
        if (predmet_Gradiva < 1 || predmet_Gradiva >= kopica_končati_klic_položaj || 힙폭[predmet_Gradiva] < 2 || kopica_VALUE[predmet_Gradiva] == 0) { napaka_VALUE("invalid object reference"); return false; }
        return true;
    }
    static void zaščititi_VALUE(int predmet_Gradiva) {
        if (predmet_Gradiva > 0 && predmet_Gradiva < kopica_končati_klic_položaj && 힙폭[predmet_Gradiva] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = predmet_Gradiva;
    }
    static void oddaja_VALUE_487749b8(int predmet_Gradiva) {
        if (predmet_Gradiva > 0 && predmet_Gradiva < kopica_končati_klic_položaj && 힙폭[predmet_Gradiva] >= 2 && kopica_VALUE[predmet_Gradiva] != 0 && 힙표시[predmet_Gradiva] == 0) {
            힙표시[predmet_Gradiva] = 1; 표시대기[zaslon_COUNT++] = predmet_Gradiva;
        }
    }
    static void 수거() {
        zaslon_COUNT = 0; Zbirka_COUNT++;
        for (int preveriti_položaj = 1; preveriti_položaj < kopica_končati_klic_položaj; preveriti_položaj += 힙폭[preveriti_položaj]) 힙표시[preveriti_položaj] = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < niz_Gradiva.length; Loop_INDEX++) oddaja_VALUE_487749b8(niz_Gradiva[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < 칸수; Loop_INDEX++) if ((칸권한[Loop_INDEX] & 8) != 0 && 형종류(칸형[Loop_INDEX]) == 2) oddaja_VALUE_487749b8(칸값[Loop_INDEX]);
        for (int 임시값 = 0; 임시값 < nit_COUNT; 임시값++) {
            oddaja_VALUE_487749b8(nit_predmet[임시값]); oddaja_VALUE_487749b8(nit_cilj[임시값]);
            int 꼭대기자리 = 임시값 == sprotno_nit ? okvir_INDEX : nit_okvir[임시값];
            for (int Datoteka_INDEX = 임시값 * 32; Datoteka_INDEX <= 꼭대기자리; Datoteka_INDEX++) {
                for (int notranje_položaj = 0; notranje_položaj < 함수지역[okvir_metoda[Datoteka_INDEX]]; notranje_položaj++) if (lokalen_krajeven_Tip[Datoteka_INDEX * 128 + notranje_položaj] == 2) oddaja_VALUE_487749b8(lokalen_krajeven_VALUE[Datoteka_INDEX * 128 + notranje_položaj]);
                for (int notranje_položaj = 0; notranje_položaj < okvir_Sklad[Datoteka_INDEX]; notranje_položaj++) if (operand_Sklad_Tip[Datoteka_INDEX * 128 + notranje_položaj] == 2) oddaja_VALUE_487749b8(operand_Sklad_VALUE[Datoteka_INDEX * 128 + notranje_položaj]);
            }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 화면참조.length; Loop_INDEX++) oddaja_VALUE_487749b8(화면참조[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < 나중수; Loop_INDEX++) oddaja_VALUE_487749b8(나중실행[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < Store_celo_število.length; Loop_INDEX++) oddaja_VALUE_487749b8(Store_celo_število[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < Razred_definicija_COUNT; Loop_INDEX++) oddaja_VALUE_487749b8(Razred_zaklepanje[Loop_INDEX]);
        for (int preveriti_položaj = 1; preveriti_položaj < kopica_končati_klic_položaj; preveriti_položaj += 힙폭[preveriti_položaj]) if (잠금깊이[preveriti_položaj] > 0) oddaja_VALUE_487749b8(preveriti_položaj);
        oddaja_VALUE_487749b8(던진객체);
        for (int Loop_INDEX = 0; Loop_INDEX < 잠시수; Loop_INDEX++) oddaja_VALUE_487749b8(잠시참조[Loop_INDEX]);
        while (zaslon_COUNT > 0) {
            int predmet_Gradiva = 표시대기[--zaslon_COUNT], območje_CODE = kopica_VALUE[predmet_Gradiva];
            for (int Loop_INDEX = predmet_Gradiva + 2; Loop_INDEX < predmet_Gradiva + 힙폭[predmet_Gradiva]; Loop_INDEX++) if (območje_CODE == 3 || območje_CODE == 4 || kopica_Gradiva[Loop_INDEX] != 0) oddaja_VALUE_487749b8(kopica_VALUE[Loop_INDEX]);
        }
        for (int preveriti_položaj = 1; preveriti_položaj < kopica_končati_klic_položaj; preveriti_položaj += 힙폭[preveriti_položaj]) if (힙표시[preveriti_položaj] == 0) kopica_VALUE[preveriti_položaj] = 0;
        for (int preveriti_položaj = 1; preveriti_položaj < kopica_končati_klic_položaj; preveriti_položaj += 힙폭[preveriti_položaj]) if (kopica_VALUE[preveriti_položaj] == 0) {
            while (preveriti_položaj + 힙폭[preveriti_položaj] < kopica_končati_klic_položaj && kopica_VALUE[preveriti_položaj + 힙폭[preveriti_položaj]] == 0) { int Naprej_položaj = preveriti_položaj + 힙폭[preveriti_položaj]; 힙폭[preveriti_položaj] += 힙폭[Naprej_položaj]; 힙폭[Naprej_položaj] = 0; }
            if (preveriti_položaj + 힙폭[preveriti_položaj] == kopica_končati_klic_položaj) { kopica_končati_klic_položaj = preveriti_položaj; break; }
        }
    }
    static int 새기억(int 종류, int 길이) {
        if (길이 < 0) { napaka_VALUE("NegativeArraySizeException"); return 0; }
        if (길이 > kopica_VALUE.length - 3) { napaka_VALUE("object heap exhausted"); return 0; }
        int 필요수 = 길이 + 2, predmet_Gradiva = 0;
        if (필요수 <= kopica_VALUE.length - kopica_končati_klic_položaj) { predmet_Gradiva = kopica_končati_klic_položaj; kopica_končati_klic_položaj += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < kopica_končati_klic_položaj; 읽는자리 += 힙폭[읽는자리]) if (kopica_VALUE[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { predmet_Gradiva = 읽는자리; break; }
            if (predmet_Gradiva != 0) {
                int 남은길이 = 힙폭[predmet_Gradiva] - 필요수;
                if (남은길이 >= 2) { 힙폭[predmet_Gradiva + 필요수] = 남은길이; kopica_VALUE[predmet_Gradiva + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= kopica_VALUE.length - kopica_končati_klic_položaj) { predmet_Gradiva = kopica_končati_klic_položaj; kopica_končati_klic_položaj += 필요수; }
        }
        if (predmet_Gradiva == 0) { napaka_VALUE("object heap exhausted"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < 필요수; Loop_INDEX++) { kopica_VALUE[predmet_Gradiva + Loop_INDEX] = 0; kopica_Gradiva[predmet_Gradiva + Loop_INDEX] = 0; 힙폭[predmet_Gradiva + Loop_INDEX] = 0; }
        element_polja[predmet_Gradiva] = 0;
        힙폭[predmet_Gradiva] = 필요수; kopica_VALUE[predmet_Gradiva] = 종류; kopica_VALUE[predmet_Gradiva + 1] = 길이; zaščititi_VALUE(predmet_Gradiva); return predmet_Gradiva;
    }
    static int izjema_Razred(String ime_konstanta) {
        if (자바도구.같음(ime_konstanta, "java/lang/Throwable")) return 1;
        if (자바도구.같음(ime_konstanta, "java/lang/Exception")) return 2;
        if (자바도구.같음(ime_konstanta, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(ime_konstanta, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(ime_konstanta, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(ime_konstanta, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(ime_konstanta, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(ime_konstanta, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(ime_konstanta, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(ime_konstanta, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(ime_konstanta, "java/io/IOException")) return 11;
        if (자바도구.같음(ime_konstanta, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(ime_konstanta, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(ime_konstanta, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(ime_konstanta, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int izjema_konstanta(int Ime) {
        for (int Loop_INDEX = 1; Loop_INDEX <= 41; Loop_INDEX++) if (Word_SMS(Ime, izjema_ime(Loop_INDEX))) return Loop_INDEX;
        return 0;
    }
    static String izjema_ime(int račun_VALUE) {
        if (račun_VALUE == 40) return "java/lang/InterruptedException";
        if (račun_VALUE == 41) return "slovenščina/lastno/대기중단예외";
        if (račun_VALUE == 39) return "java/net/SocketException";
        if (račun_VALUE == 20) return "slovenščina/lastno/izjema";
        if (račun_VALUE == 21) return "slovenščina/lastno/실행예외";
        if (račun_VALUE == 22) return "slovenščina/lastno/V_I_izjema";
        if (račun_VALUE == 23) return "slovenščina/lastno/počakaj_TIMEOUT_izjema";
        if (račun_VALUE == 24) return "slovenščina/lastno/naslov_LOOKUP_izjema";
        if (račun_VALUE == 25) return "slovenščina/lastno/파일없음예외";
        if (račun_VALUE == 26) return "slovenščina/lastno/통신예외";
        if (račun_VALUE == 27) return "slovenščina/lastno/neveljaven_argument_izjema";
        if (račun_VALUE == 28) return "slovenščina/lastno/숫자형식예외";
        if (račun_VALUE == 29) return "slovenščina/lastno/범위예외";
        if (račun_VALUE == 30) return "slovenščina/lastno/배열범위예외";
        if (račun_VALUE == 31) return "slovenščina/lastno/문자열범위예외";
        if (račun_VALUE == 32) return "slovenščina/lastno/NULL_Gradiva_izjema";
        if (račun_VALUE == 33) return "slovenščina/lastno/산술예외";
        if (račun_VALUE == 34) return "slovenščina/lastno/stanje_izjema";
        if (račun_VALUE == 35) return "slovenščina/lastno/Tip_pretvorba_izjema";
        if (račun_VALUE == 36) return "slovenščina/lastno/음수배열크기예외";
        if (račun_VALUE == 37) return "slovenščina/lastno/ARRAY_Store_napaka";
        if (račun_VALUE == 38) return "slovenščina/lastno/nit_stanje_izjema";
        if (račun_VALUE == 1) return "java/lang/Throwable"; if (račun_VALUE == 2) return "java/lang/Exception";
        if (račun_VALUE == 3) return "java/lang/RuntimeException"; if (račun_VALUE == 4) return "java/lang/ArithmeticException";
        if (račun_VALUE == 5) return "java/lang/NullPointerException"; if (račun_VALUE == 6) return "java/lang/IndexOutOfBoundsException";
        if (račun_VALUE == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (račun_VALUE == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (račun_VALUE == 9) return "java/lang/IllegalArgumentException"; if (račun_VALUE == 10) return "java/lang/NumberFormatException";
        if (račun_VALUE == 11) return "java/io/IOException"; if (račun_VALUE == 12) return "java/io/FileNotFoundException";
        if (račun_VALUE == 17) return "java/lang/ArrayStoreException";
        if (račun_VALUE == 18) return "java/net/UnknownHostException";
        if (račun_VALUE == 19) return "java/net/SocketTimeoutException";
        if (račun_VALUE == 16) return "java/lang/IllegalThreadStateException";
        if (račun_VALUE == 13) return "java/lang/IllegalStateException"; if (račun_VALUE == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int izjema_nadrejen(int račun_VALUE) {
        if (račun_VALUE == 40) return 2;
        if (račun_VALUE == 41) return 40;
        if (račun_VALUE == 39) return 11;
        if (račun_VALUE == 1) return 0;
        if (račun_VALUE == 2) return 1;
        if (račun_VALUE == 3) return 2;
        if (račun_VALUE == 4) return 3;
        if (račun_VALUE == 5) return 3;
        if (račun_VALUE == 6) return 3;
        if (račun_VALUE == 7) return 6;
        if (račun_VALUE == 8) return 6;
        if (račun_VALUE == 9) return 3;
        if (račun_VALUE == 10) return 9;
        if (račun_VALUE == 11) return 2;
        if (račun_VALUE == 12) return 11;
        if (račun_VALUE == 13) return 3;
        if (račun_VALUE == 14) return 3;
        if (račun_VALUE == 15) return 3;
        if (račun_VALUE == 16) return 9;
        if (račun_VALUE == 17) return 3;
        if (račun_VALUE == 18) return 11;
        if (račun_VALUE == 19) return 11;
        if (račun_VALUE == 20) return 2;
        if (račun_VALUE == 21) return 3;
        if (račun_VALUE == 22) return 11;
        if (račun_VALUE == 23) return 22;
        if (račun_VALUE == 24) return 22;
        if (račun_VALUE == 25) return 22;
        if (račun_VALUE == 26) return 22;
        if (račun_VALUE == 27) return 9;
        if (račun_VALUE == 28) return 27;
        if (račun_VALUE == 29) return 6;
        if (račun_VALUE == 30) return 29;
        if (račun_VALUE == 31) return 29;
        if (račun_VALUE == 32) return 5;
        if (račun_VALUE == 33) return 4;
        if (račun_VALUE == 34) return 13;
        if (račun_VALUE == 35) return 14;
        if (račun_VALUE == 36) return 15;
        if (račun_VALUE == 37) return 17;
        if (račun_VALUE == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int dejanska_vrednost, int 요구값) {
        for (int 깊이 = 0; dejanska_vrednost != 0 && 깊이 < 16; 깊이++, dejanska_vrednost = izjema_nadrejen(dejanska_vrednost))
            if (dejanska_vrednost == 요구값) return true;
        return false;
    }
    static void 예외던짐(int račun_VALUE, String 안내참조) {
        int predmet_Gradiva = 새기억(9, 2); if (NAPAKA) return;
        kopica_VALUE[predmet_Gradiva + 2] = račun_VALUE; kopica_VALUE[predmet_Gradiva + 3] = gostiti_znak(안내참조); kopica_Gradiva[predmet_Gradiva + 3] = 1;
        던진객체 = predmet_Gradiva; NAPAKA = true;
    }
    static boolean 맞는객체(int predmet_Gradiva, int Ime) {
        if (predmet_Gradiva == 0) return true;
        if (!객체유효(predmet_Gradiva)) return false;
        int območje_CODE = kopica_VALUE[predmet_Gradiva];
        if (Word_SMS(Ime, "java/lang/Object")) return true;
        if (območje_CODE >= 32) return 종포함(območje_CODE - 32, Ime);
        if (območje_CODE == 9) { int cilj_naslov = izjema_konstanta(Ime); return cilj_naslov != 0 && 예외포함(kopica_VALUE[predmet_Gradiva + 2], cilj_naslov); }
        if (območje_CODE == 1) return Word_SMS(Ime, "java/lang/String") || Word_SMS(Ime, "java/lang/CharSequence");
        if (območje_CODE == 4) return Word_SMS(Ime, "java/lang/StringBuilder") || Word_SMS(Ime, "java/lang/CharSequence");
        if (območje_CODE == 10) return Word_SMS(Ime, "java/util/ArrayList") || Word_SMS(Ime, "java/util/List");
        if (območje_CODE == 11) return Word_SMS(Ime, "java/util/HashMap") || Word_SMS(Ime, "java/util/Map");
        if (območje_CODE == 12) return Word_SMS(Ime, "java/lang/Integer") || Word_SMS(Ime, "java/lang/Number");
        if (območje_CODE >= 24 && območje_CODE <= 28 && kopica_VALUE[predmet_Gradiva + 13] != 0) return 한국어화면종(Ime) == območje_CODE || Word_SMS(Ime, "slovenščina/lastno/화면구성요소");
        if (območje_CODE >= 24 && območje_CODE <= 28) return (한국어화면종(Ime) == 0 && 화면종(Ime) == območje_CODE) || Word_SMS(Ime, "java/awt/Component") || Word_SMS(Ime, "java/awt/Container") || Word_SMS(Ime, "javax/swing/JComponent");
        if (območje_CODE == 29) return Word_SMS(Ime, kopica_VALUE[predmet_Gradiva + 3] != 0 ? "slovenščina/lastno/akcija_obvestilo" : "java/awt/event/ActionEvent");
        if (območje_CODE == 30) return Word_SMS(Ime, "java/awt/FlowLayout") || Word_SMS(Ime, "java/awt/LayoutManager");
        if (območje_CODE == 17) return Word_SMS(Ime, "java/net/Socket");
        if (območje_CODE == 18) return Word_SMS(Ime, "java/net/ServerSocket");
        if (območje_CODE == 19) return Word_SMS(Ime, kopica_VALUE[predmet_Gradiva + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (območje_CODE == 14) return Word_SMS(Ime, "java/net/InetAddress");
        if (območje_CODE == 15) return Word_SMS(Ime, "java/net/DatagramSocket");
        if (območje_CODE == 16) return Word_SMS(Ime, "java/net/DatagramPacket");
        if (območje_CODE == 13) return Word_SMS(Ime, kopica_VALUE[predmet_Gradiva + 3] != 0 ? "slovenščina/lastno/작업가닥" : "java/lang/Thread");
        if (območje_CODE == 2) return Word_SMS(Ime, "[I"); if (območje_CODE == 20) return Word_SMS(Ime, "[B"); if (območje_CODE == 21) return Word_SMS(Ime, "[Z");
        if (območje_CODE == 22) return Word_SMS(Ime, "[C"); if (območje_CODE == 23) return Word_SMS(Ime, "[S");
        if (območje_CODE != 3) return false;
        if (Word_SMS(Ime, "[Ljava/lang/Object;")) return true;
        int komponenta = element_polja[predmet_Gradiva];
        if (komponenta == -1) return Word_SMS(Ime, "[Ljava/lang/String;") || Word_SMS(Ime, "[Ljava/lang/CharSequence;");
        if (komponenta == 0) return false;
        if (배열종비교(komponenta, Ime)) return true;
        if ((Word_SMS(komponenta, "java/lang/String") || Word_SMS(komponenta, "java/lang/StringBuilder")) && Word_SMS(Ime, "[Ljava/lang/CharSequence;")) return true;
        for (int Loop_INDEX = 0; Loop_INDEX < Razred_definicija_COUNT; Loop_INDEX++) if (같은말(Razred_definicija_ime[Loop_INDEX], komponenta)) {
            for (int koda_znaka = Loop_INDEX, 중첩깊이 = 0; koda_znaka >= 0 && 중첩깊이 < 16; 중첩깊이++, koda_znaka = nadrejen_Razred(koda_znaka)) {
                if (배열종비교(Razred_definicija_nadrejen[koda_znaka], Ime)) return true;
                for (int notranje_položaj = 0; notranje_položaj < Razred_vmesnik_COUNT[koda_znaka]; notranje_položaj++) if (배열종비교(Razred_vmesnik[koda_znaka * 16 + notranje_položaj], Ime)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int ime_konstanta, int 형식참조) {
        int preveriti_položaj = 상가[형식참조], vnos_COUNT = konstanta_SECOND_VALUE[형식참조];
        if (ime_konstanta == 0 || vnos_COUNT < 4 || Datoteka[preveriti_položaj] != '[' || Datoteka[preveriti_položaj + 1] != 'L' || Datoteka[preveriti_položaj + vnos_COUNT - 1] != ';' || konstanta_SECOND_VALUE[ime_konstanta] != vnos_COUNT - 3) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < vnos_COUNT - 3; Loop_INDEX++) if (Datoteka[상가[ime_konstanta] + Loop_INDEX] != Datoteka[preveriti_položaj + 2 + Loop_INDEX]) return false;
        return true;
    }
    static void ročica_izjema() {
        if (던진객체 == 0) return;
        NAPAKA = false;
        while (okvir_INDEX >= sprotno_nit * 32) {
            int Datoteka_INDEX = okvir_metoda[okvir_INDEX], 읽는자리 = okvir_navodilo[okvir_INDEX];
            for (int Loop_INDEX = 0; Loop_INDEX < 잡기수; Loop_INDEX++) if (잡기함수[Loop_INDEX] == Datoteka_INDEX && 읽는자리 >= 잡기시작[Loop_INDEX] && 읽는자리 < 잡기끝[Loop_INDEX]
                && (잡기종[Loop_INDEX] == 0 || 맞는객체(던진객체, 잡기종[Loop_INDEX]))) {
                okvir_položaj[okvir_INDEX] = 잡기위치[Loop_INDEX]; okvir_Sklad[okvir_INDEX] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (inicializirati_okvir[okvir_INDEX] != 0) Razred_definicija_stanje[inicializirati_okvir[okvir_INDEX] - 1] = 3;
            if (okvir_zaklepanje[okvir_INDEX] != 0) { izdaja_zaklepanje(okvir_zaklepanje[okvir_INDEX]); okvir_zaklepanje[okvir_INDEX] = 0; }
            okvir_INDEX--;
        }
        uporabnik.Pisanje("Uncaught ");
        if (kopica_VALUE[던진객체] == 9) { uporabnik.Pisanje(izjema_ime(kopica_VALUE[던진객체 + 2])); uporabnik.Pisanje(": "); pisati_SMS(kopica_VALUE[던진객체 + 3]); }
        else uporabnik.Pisanje("user exception");
        uporabnik.pisati_znak_VALUE(10); 던진객체 = 0; NAPAKA = true;
    }
    // 이 JVM의 operand_Sklad 항목은 sprotno_element category-1(int/reference)만 허용한다.
    static void Sklad_navodilo(int ukaz_CODE) {
        int 첫값 = 빼기(0), 첫형식 = vrni_Tip;
        if (ukaz_CODE == 87) return;
        if (ukaz_CODE == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int bajt_podatki = 빼기(0), SECOND_oblika = vrni_Tip;
        if (ukaz_CODE == 88) return;
        if (ukaz_CODE == 90) { 넣기(첫값, 첫형식); 넣기(bajt_podatki, SECOND_oblika); 넣기(첫값, 첫형식); return; }
        if (ukaz_CODE == 92) { 넣기(bajt_podatki, SECOND_oblika); 넣기(첫값, 첫형식); 넣기(bajt_podatki, SECOND_oblika); 넣기(첫값, 첫형식); return; }
        if (ukaz_CODE == 95) { 넣기(첫값, 첫형식); 넣기(bajt_podatki, SECOND_oblika); return; }
        int koda_znaka = 빼기(0), 셋째형식 = vrni_Tip;
        if (ukaz_CODE == 91) { 넣기(첫값, 첫형식); 넣기(koda_znaka, 셋째형식); 넣기(bajt_podatki, SECOND_oblika); 넣기(첫값, 첫형식); return; }
        if (ukaz_CODE == 93) { 넣기(bajt_podatki, SECOND_oblika); 넣기(첫값, 첫형식); 넣기(koda_znaka, 셋째형식); 넣기(bajt_podatki, SECOND_oblika); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = vrni_Tip;
        넣기(bajt_podatki, SECOND_oblika); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(koda_znaka, 셋째형식); 넣기(bajt_podatki, SECOND_oblika); 넣기(첫값, 첫형식);
    }
    static void 새객체(int ime_konstanta, int 시작점) {
        int območje_CODE = 0, 유효길이 = 0, izjema_Gradiva = izjema_konstanta(ime_konstanta);
        if (Word_SMS(ime_konstanta, "java/lang/StringBuilder")) { območje_CODE = 4; 유효길이 = 1; }
        if (Word_SMS(ime_konstanta, "java/io/FileInputStream")) { območje_CODE = 5; 유효길이 = 2; }
        if (Word_SMS(ime_konstanta, "java/io/FileOutputStream")) { območje_CODE = 6; 유효길이 = 2; }
        if (izjema_Gradiva != 0) { območje_CODE = 9; 유효길이 = 2; }
        if (Word_SMS(ime_konstanta, "java/util/ArrayList")) { območje_CODE = 10; 유효길이 = 2; }
        if (Word_SMS(ime_konstanta, "java/util/HashMap")) { območje_CODE = 11; 유효길이 = 2; }
        if (Word_SMS(ime_konstanta, "java/lang/Integer")) { območje_CODE = 12; 유효길이 = 1; }
        if (Word_SMS(ime_konstanta, "java/net/Socket")) { območje_CODE = 17; 유효길이 = 5; }
        if (Word_SMS(ime_konstanta, "java/net/ServerSocket")) { območje_CODE = 18; 유효길이 = 5; }
        if (Word_SMS(ime_konstanta, "java/net/DatagramSocket")) { območje_CODE = 15; 유효길이 = 3; }
        if (Word_SMS(ime_konstanta, "java/net/DatagramPacket")) { območje_CODE = 16; 유효길이 = 4; }
        if (Word_SMS(ime_konstanta, "java/lang/Thread") || Word_SMS(ime_konstanta, "slovenščina/lastno/작업가닥")) { območje_CODE = 13; 유효길이 = 2; }
        if (Word_SMS(ime_konstanta, "java/lang/Object")) { območje_CODE = 8; }
        if (območje_CODE == 0 && 화면종(ime_konstanta) != 0) { območje_CODE = 화면종(ime_konstanta); 유효길이 = 12; }
        if (območje_CODE == 0) {
            int koda_znaka = FIND_Razred_definicija(ime_konstanta); if (koda_znaka < 0 || NAPAKA || !inicializirati(koda_znaka, 시작점)) return;
            območje_CODE = 32 + koda_znaka; 유효길이 = 종칸수[koda_znaka];
        }
        int predmet_Gradiva = dodeliti_Senzor_prostora(območje_CODE, 유효길이); if (NAPAKA) return;
        if (območje_CODE == 13 && Word_SMS(ime_konstanta, "slovenščina/lastno/작업가닥")) kopica_VALUE[predmet_Gradiva + 3] = 1;
        if (območje_CODE >= 24 && območje_CODE <= 28 && 한국어화면종(ime_konstanta) != 0) kopica_VALUE[predmet_Gradiva + 13] = 1;
        if (območje_CODE == 5 || območje_CODE == 6 || območje_CODE == 15 || območje_CODE == 17 || območje_CODE == 18) kopica_VALUE[predmet_Gradiva + 2] = -1;
        if (območje_CODE == 9) kopica_VALUE[predmet_Gradiva + 2] = izjema_Gradiva;
        넣기(predmet_Gradiva, 2);
    }
    static boolean 값같음(int 첫값, int bajt_podatki) {
        if (첫값 == bajt_podatki) return true;
        if (첫값 == 0 || bajt_podatki == 0 || 첫값 < 0 || bajt_podatki < 0 || 첫값 >= kopica_končati_klic_položaj || bajt_podatki >= kopica_končati_klic_položaj) return false;
        if (kopica_VALUE[첫값] == 1 && kopica_VALUE[bajt_podatki] == 1) return 글같음(첫값, bajt_podatki, false);
        return kopica_VALUE[첫값] == 12 && kopica_VALUE[bajt_podatki] == 12 && kopica_VALUE[첫값 + 2] == kopica_VALUE[bajt_podatki + 2];
    }
    static int 글조각(int predmet_Gradiva, int Start_položaj, int končati_klic_položaj) {
        if (!predmet_VALUE(predmet_Gradiva, 1)) return 0;
        if (Start_položaj < 0 || končati_klic_položaj < Start_položaj || končati_klic_položaj > kopica_VALUE[predmet_Gradiva + 1]) { napaka_VALUE("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = dodeliti_Senzor_prostora(1, končati_klic_položaj - Start_položaj); if (NAPAKA) return 0;
        for (int Loop_INDEX = Start_položaj; Loop_INDEX < končati_klic_položaj; Loop_INDEX++) kopica_VALUE[반환값 + 2 + Loop_INDEX - Start_položaj] = kopica_VALUE[predmet_Gradiva + 2 + Loop_INDEX];
        return 반환값;
    }
    static int združiti_SMS(int 첫값, int bajt_podatki) {
        if (!predmet_VALUE(첫값, 1) || !predmet_VALUE(bajt_podatki, 1)) return 0;
        int vnos_COUNT = kopica_VALUE[첫값 + 1], metoda_INDEX = kopica_VALUE[bajt_podatki + 1], 반환값 = dodeliti_Senzor_prostora(1, vnos_COUNT + metoda_INDEX); if (NAPAKA) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < vnos_COUNT; Loop_INDEX++) kopica_VALUE[반환값 + 2 + Loop_INDEX] = kopica_VALUE[첫값 + 2 + Loop_INDEX];
        for (int Loop_INDEX = 0; Loop_INDEX < metoda_INDEX; Loop_INDEX++) kopica_VALUE[반환값 + 2 + vnos_COUNT + Loop_INDEX] = kopica_VALUE[bajt_podatki + 2 + Loop_INDEX];
        return 반환값;
    }
    static boolean 기본호출(int lastnik, int ime_konstanta, int 서술상수, int ukaz_CODE) {
        if (Word_SMS(lastnik, "slovenščina/lastno/실행인수") && ukaz_CODE == 184) {
            if (Word_SMS(ime_konstanta, "element_COUNT") && Word_SMS(서술상수, "()I")) { 넣기(uporabnik.인수개수() - 1, 1); return true; }
            if (Word_SMS(ime_konstanta, "Besedilo") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= uporabnik.인수개수() - 1) 예외던짐(29, "Izvedi_ukaz Argumenti 범위를 벗어났습니다");
                else 넣기(gostiti_znak(uporabnik.Argumenti(순번 + 1)), 2);
                return true;
            }
            napaka_VALUE("지원하지 않는 slovenščina Izvedi_ukaz Argumenti 호출"); return true;
        }
        if (Word_SMS(lastnik, "slovenščina/lastno/작업가닥")) { Proces_nit(ime_konstanta, 서술상수, ukaz_CODE, true); return true; }
        if (한국어화면소유(lastnik)) { 한국어화면호출(lastnik, ime_konstanta, 서술상수, ukaz_CODE); return true; }
        if (화면소유(lastnik)) { 화면호출(lastnik, ime_konstanta, 서술상수, ukaz_CODE); return true; }
        if (Word_SMS(lastnik, "java/net/Socket") || Word_SMS(lastnik, "java/net/ServerSocket") || Word_SMS(lastnik, "java/io/InputStream") || Word_SMS(lastnik, "java/io/OutputStream")) { 흐름호출(lastnik, ime_konstanta, 서술상수, ukaz_CODE); return true; }
        if (Word_SMS(lastnik, "slovenščina/lastno/jedro_VALUE") && ukaz_CODE == 184) {
            if (Word_SMS(ime_konstanta, "화면너비") && Word_SMS(서술상수, "()I")) { 넣기(uporabnik.화면너비(), 1); return true; }
            if (Word_SMS(ime_konstanta, "화면높이") && Word_SMS(서술상수, "()I")) { 넣기(uporabnik.화면높이(), 1); return true; }
            if (Word_SMS(ime_konstanta, "밀리초") && Word_SMS(서술상수, "()I")) { 넣기(uporabnik.밀리초(), 1); return true; }
            if (Word_SMS(ime_konstanta, "그림대기") && Word_SMS(서술상수, "()I")) { 넣기(uporabnik.그림대기(), 1); return true; }
            if (Word_SMS(ime_konstanta, "pravokotnik") && Word_SMS(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), višina_VALUE = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), koordinata_x = 빼기(1); 넣기(uporabnik.pravokotnik(koordinata_x, 세로좌표, 너비, višina_VALUE, 색상), 1); return true; }
        }
        if (Word_SMS(lastnik, "java/net/InetAddress") || Word_SMS(lastnik, "java/net/DatagramPacket") || Word_SMS(lastnik, "java/net/DatagramSocket")) { 통신호출(lastnik, ime_konstanta, 서술상수, ukaz_CODE); return true; }
        if (Word_SMS(lastnik, "java/lang/Thread")) { 가닥호출(ime_konstanta, 서술상수, ukaz_CODE); return true; }
        if (Word_SMS(lastnik, "java/lang/Object")) {
            if (Word_SMS(ime_konstanta, "<init>") && Word_SMS(서술상수, "()V") && ukaz_CODE == 183) { 객체유효(빼기(2)); return true; }
            if (Word_SMS(ime_konstanta, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int bajt_podatki = 빼기(2), 첫값 = 빼기(2); if (객체유효(첫값)) 넣기(첫값 == bajt_podatki ? 1 : 0, 1); return true; }
        }
        if (izjema_konstanta(lastnik) != 0) {
            if (Word_SMS(ime_konstanta, "<init>") && ukaz_CODE == 183 && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(Ljava/lang/String;)V"))) {
                int poziv = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), predmet_Gradiva = 빼기(2);
                if (predmet_VALUE(predmet_Gradiva, 9)) { kopica_VALUE[predmet_Gradiva + 3] = poziv; kopica_Gradiva[predmet_Gradiva + 3] = 1; } return true;
            }
            if ((Word_SMS(ime_konstanta, "getMessage") || Word_SMS(ime_konstanta, "설명")) && Word_SMS(서술상수, "()Ljava/lang/String;")) { int predmet_Gradiva = 빼기(2); if (predmet_VALUE(predmet_Gradiva, 9)) 넣기(kopica_VALUE[predmet_Gradiva + 3], 2); return true; }
        }
        if (Word_SMS(lastnik, "java/lang/String")) {
            if (ukaz_CODE == 182 && Word_SMS(ime_konstanta, "getBytes") && (Word_SMS(서술상수, "()[B") || Word_SMS(서술상수, "(Ljava/lang/String;)[B"))) {
                int kodiranje_ime = Word_SMS(서술상수, "()[B") ? 0 : 빼기(2), predmet_Gradiva = 빼기(2);
                if (!predmet_VALUE(predmet_Gradiva, 1)) return true;
                if (kodiranje_ime != 0 && !글같음(kodiranje_ime, gostiti_znak("UTF-8"), false) && !글같음(kodiranje_ime, gostiti_znak("UTF8"), false) && !글같음(kodiranje_ime, gostiti_znak("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int vnos_COUNT = kopica_VALUE[predmet_Gradiva + 1], 반환값 = dodeliti_Senzor_prostora(20, vnos_COUNT * 3), 사용수 = 0; if (NAPAKA) return true;
                for (int notranje_položaj = 0; notranje_položaj < vnos_COUNT; notranje_položaj++) {
                    int koda_znaka = kopica_VALUE[predmet_Gradiva + 2 + notranje_položaj];
                    if (koda_znaka >= 0xd800 && koda_znaka <= 0xdbff && notranje_položaj + 1 < vnos_COUNT && kopica_VALUE[predmet_Gradiva + 3 + notranje_položaj] >= 0xdc00 && kopica_VALUE[predmet_Gradiva + 3 + notranje_položaj] <= 0xdfff) koda_znaka = 0x10000 + ((koda_znaka - 0xd800) << 10) + kopica_VALUE[predmet_Gradiva + 2 + ++notranje_položaj] - 0xdc00;
                    else if (koda_znaka >= 0xd800 && koda_znaka <= 0xdfff) koda_znaka = '?';
                    if (koda_znaka < 128) kopica_VALUE[반환값 + 2 + 사용수++] = koda_znaka;
                    else { int bajt_COUNT = koda_znaka < 2048 ? 2 : koda_znaka < 65536 ? 3 : 4; kopica_VALUE[반환값 + 2 + 사용수++] = (byte)((bajt_COUNT == 2 ? 192 : bajt_COUNT == 3 ? 224 : 240) | koda_znaka >> (6 * (bajt_COUNT - 1))); for (int Primerjava_položaj = bajt_COUNT - 1; Primerjava_položaj > 0; Primerjava_položaj--) kopica_VALUE[반환값 + 2 + 사용수++] = (byte)(128 | koda_znaka >> (6 * (Primerjava_položaj - 1)) & 63); }
                }
                kopica_VALUE[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (ukaz_CODE == 184 && Word_SMS(ime_konstanta, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(številka_znak(빼기(1)), 2); return true; }
            if (ukaz_CODE != 182) return false;
            if (Word_SMS(ime_konstanta, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int bajt_podatki = 빼기(2), 첫값 = 빼기(2); if (predmet_VALUE(첫값, 1)) 넣기(글같음(첫값, bajt_podatki, false) ? 1 : 0, 1); return true; }
            if (Word_SMS(ime_konstanta, "isEmpty") && Word_SMS(서술상수, "()Z")) { int 첫값 = 빼기(2); if (predmet_VALUE(첫값, 1)) 넣기(kopica_VALUE[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Word_SMS(ime_konstanta, "substring") && (Word_SMS(서술상수, "(I)Ljava/lang/String;") || Word_SMS(서술상수, "(II)Ljava/lang/String;"))) {
                boolean SECOND_VALUE = Word_SMS(서술상수, "(II)Ljava/lang/String;"); int končati_klic_položaj = SECOND_VALUE ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (predmet_VALUE(첫값, 1)) 넣기(글조각(첫값, 시작점, SECOND_VALUE ? končati_klic_položaj : kopica_VALUE[첫값 + 1]), 2); return true;
            }
            if (Word_SMS(ime_konstanta, "concat") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int bajt_podatki = 빼기(2), 첫값 = 빼기(2); 넣기(združiti_SMS(첫값, bajt_podatki), 2); return true; }
            if (Word_SMS(ime_konstanta, "hashCode") && Word_SMS(서술상수, "()I")) { int 첫값 = 빼기(2), zgoščena_vrednost_VALUE = 0; if (predmet_VALUE(첫값, 1)) { for (int Loop_INDEX = 0; Loop_INDEX < kopica_VALUE[첫값 + 1]; Loop_INDEX++) zgoščena_vrednost_VALUE = zgoščena_vrednost_VALUE * 31 + kopica_VALUE[첫값 + 2 + Loop_INDEX]; 넣기(zgoščena_vrednost_VALUE, 1); } return true; }
            if (Word_SMS(ime_konstanta, "toString") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (predmet_VALUE(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Word_SMS(lastnik, "java/lang/Integer")) {
            if (ukaz_CODE == 184 && Word_SMS(ime_konstanta, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/Integer;")) { int podatki_VALUE = 빼기(1), predmet_Gradiva = podatki_VALUE >= -128 && podatki_VALUE <= 127 ? Store_celo_število[podatki_VALUE + 128] : 0; if (predmet_Gradiva == 0) { predmet_Gradiva = dodeliti_Senzor_prostora(12, 1); if (!NAPAKA) { kopica_VALUE[predmet_Gradiva + 2] = podatki_VALUE; if (podatki_VALUE >= -128 && podatki_VALUE <= 127) Store_celo_število[podatki_VALUE + 128] = predmet_Gradiva; } } 넣기(predmet_Gradiva, 2); return true; }
            if (ukaz_CODE == 183 && Word_SMS(ime_konstanta, "<init>") && Word_SMS(서술상수, "(I)V")) { int podatki_VALUE = 빼기(1), predmet_Gradiva = 빼기(2); if (predmet_VALUE(predmet_Gradiva, 12)) kopica_VALUE[predmet_Gradiva + 2] = podatki_VALUE; return true; }
            if (ukaz_CODE == 182 && Word_SMS(ime_konstanta, "intValue") && Word_SMS(서술상수, "()I")) { int predmet_Gradiva = 빼기(2); if (predmet_VALUE(predmet_Gradiva, 12)) 넣기(kopica_VALUE[predmet_Gradiva + 2], 1); return true; }
            if (ukaz_CODE == 184 && Word_SMS(ime_konstanta, "toString") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(številka_znak(빼기(1)), 2); return true; }
        }
        if (Word_SMS(lastnik, "java/lang/Math") && ukaz_CODE == 184) {
            if (Word_SMS(ime_konstanta, "abs") && Word_SMS(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((Word_SMS(ime_konstanta, "min") || Word_SMS(ime_konstanta, "max")) && Word_SMS(서술상수, "(II)I")) { int bajt_podatki = 빼기(1), 첫값 = 빼기(1); 넣기(Word_SMS(ime_konstanta, "min") ? (첫값 < bajt_podatki ? 첫값 : bajt_podatki) : (첫값 > bajt_podatki ? 첫값 : bajt_podatki), 1); return true; }
        }
        if (Word_SMS(lastnik, "java/lang/System") && ukaz_CODE == 184) {
            if (Word_SMS(ime_konstanta, "gc") && Word_SMS(서술상수, "()V")) { 수거(); return true; }
            if (Word_SMS(ime_konstanta, "arraycopy") && Word_SMS(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int vnos_COUNT = 빼기(1), cilj_VALUE_INDEX = 빼기(1), bajt_podatki = 빼기(2), Start_položaj = 빼기(1), 첫값 = 빼기(2);
                if (객체유효(첫값) && 객체유효(bajt_podatki)) {
                    int območje_CODE = kopica_VALUE[첫값];
                    if (kopica_VALUE[bajt_podatki] != območje_CODE || (območje_CODE != 2 && območje_CODE != 3 && (območje_CODE < 20 || območje_CODE > 23))) napaka_VALUE("arraycopy type mismatch");
                    else if (vnos_COUNT < 0 || Start_položaj < 0 || cilj_VALUE_INDEX < 0 || Start_položaj > kopica_VALUE[첫값 + 1] - vnos_COUNT || cilj_VALUE_INDEX > kopica_VALUE[bajt_podatki + 1] - vnos_COUNT) napaka_VALUE("ArrayIndexOutOfBoundsException");
                    else if (첫값 == bajt_podatki && cilj_VALUE_INDEX > Start_položaj) { for (int Loop_INDEX = vnos_COUNT - 1; Loop_INDEX >= 0; Loop_INDEX--) kopica_VALUE[bajt_podatki + 2 + cilj_VALUE_INDEX + Loop_INDEX] = kopica_VALUE[첫값 + 2 + Start_položaj + Loop_INDEX]; }
                    else { for (int Loop_INDEX = 0; Loop_INDEX < vnos_COUNT && !NAPAKA; Loop_INDEX++) { int podatki_VALUE = kopica_VALUE[첫값 + 2 + Start_položaj + Loop_INDEX]; if (območje_CODE != 3 || 배열저장가능(bajt_podatki, podatki_VALUE)) kopica_VALUE[bajt_podatki + 2 + cilj_VALUE_INDEX + Loop_INDEX] = podatki_VALUE; } }
                }
                return true;
            }
        }
        if (Word_SMS(lastnik, "java/util/ArrayList") || Word_SMS(lastnik, "java/util/List") || Word_SMS(lastnik, "java/util/HashMap") || Word_SMS(lastnik, "java/util/Map")) {
            모음호출(lastnik, ime_konstanta, 서술상수, ukaz_CODE); return true;
        }
        return false;
    }
    static void 모음늘리기(int predmet_Gradiva, int 필요수) {
        int 이전값 = kopica_VALUE[predmet_Gradiva + 2], zmogljivost_podatki = 이전값 == 0 ? 0 : kopica_VALUE[이전값 + 1];
        if (zmogljivost_podatki >= 필요수) return;
        int Naprej_položaj = zmogljivost_podatki < 8 ? 8 : zmogljivost_podatki * 2; if (Naprej_položaj < 필요수) Naprej_položaj = 필요수;
        int podatki_ARRAY = dodeliti_Senzor_prostora(3, Naprej_položaj); if (NAPAKA) return;
        for (int Loop_INDEX = 0; Loop_INDEX < zmogljivost_podatki; Loop_INDEX++) kopica_VALUE[podatki_ARRAY + 2 + Loop_INDEX] = kopica_VALUE[이전값 + 2 + Loop_INDEX];
        kopica_VALUE[predmet_Gradiva + 2] = podatki_ARRAY; kopica_Gradiva[predmet_Gradiva + 2] = 1;
    }
    static void 모음호출(int lastnik, int ime_konstanta, int 서술상수, int ukaz_CODE) {
        boolean 대응참조 = Word_SMS(lastnik, "java/util/HashMap") || Word_SMS(lastnik, "java/util/Map"); int območje_CODE = 대응참조 ? 11 : 10;
        if (Word_SMS(ime_konstanta, "<init>") && ukaz_CODE == 183 && Word_SMS(서술상수, "()V")) { int predmet_Gradiva = 빼기(2); if (predmet_VALUE(predmet_Gradiva, območje_CODE)) 모음늘리기(predmet_Gradiva, 8); return; }
        if (ukaz_CODE != 182 && ukaz_CODE != 185) { napaka_VALUE("invalid collection invocation"); return; }
        if (Word_SMS(ime_konstanta, "size") && Word_SMS(서술상수, "()I") || Word_SMS(ime_konstanta, "isEmpty") && Word_SMS(서술상수, "()Z")) {
            int predmet_Gradiva = 빼기(2); if (predmet_VALUE(predmet_Gradiva, območje_CODE)) 넣기(Word_SMS(ime_konstanta, "size") ? kopica_VALUE[predmet_Gradiva + 3] : kopica_VALUE[predmet_Gradiva + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Word_SMS(ime_konstanta, "clear") && Word_SMS(서술상수, "()V")) { int predmet_Gradiva = 빼기(2); if (predmet_VALUE(predmet_Gradiva, območje_CODE)) { int podatki_ARRAY = kopica_VALUE[predmet_Gradiva + 2]; for (int Loop_INDEX = 0; Loop_INDEX < kopica_VALUE[podatki_ARRAY + 1]; Loop_INDEX++) kopica_VALUE[podatki_ARRAY + 2 + Loop_INDEX] = 0; kopica_VALUE[predmet_Gradiva + 3] = 0; } return; }
        if (!대응참조 && Word_SMS(ime_konstanta, "add") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            int podatki_VALUE = 빼기(2), predmet_Gradiva = 빼기(2); if (!predmet_VALUE(predmet_Gradiva, 10)) return;
            int vnos_COUNT = kopica_VALUE[predmet_Gradiva + 3]; 모음늘리기(predmet_Gradiva, vnos_COUNT + 1); if (!NAPAKA) { kopica_VALUE[kopica_VALUE[predmet_Gradiva + 2] + 2 + vnos_COUNT] = podatki_VALUE; kopica_VALUE[predmet_Gradiva + 3] = vnos_COUNT + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Word_SMS(ime_konstanta, "get") || Word_SMS(ime_konstanta, "remove")) && Word_SMS(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && Word_SMS(ime_konstanta, "set") && Word_SMS(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean informacijska_tehnologija_Dodeljeno = Word_SMS(ime_konstanta, "set"); int podatki_VALUE = informacijska_tehnologija_Dodeljeno ? 빼기(2) : 0, vnos_položaj = 빼기(1), predmet_Gradiva = 빼기(2);
            if (!predmet_VALUE(predmet_Gradiva, 10)) return;
            int vnos_COUNT = kopica_VALUE[predmet_Gradiva + 3], podatki_ARRAY = kopica_VALUE[predmet_Gradiva + 2];
            if (vnos_položaj < 0 || vnos_položaj >= vnos_COUNT) { 예외던짐(6, "list index"); return; }
            int 이전값 = kopica_VALUE[podatki_ARRAY + 2 + vnos_položaj];
            if (informacijska_tehnologija_Dodeljeno) kopica_VALUE[podatki_ARRAY + 2 + vnos_položaj] = podatki_VALUE;
            if (Word_SMS(ime_konstanta, "remove")) { for (int Loop_INDEX = vnos_položaj + 1; Loop_INDEX < vnos_COUNT; Loop_INDEX++) kopica_VALUE[podatki_ARRAY + 1 + Loop_INDEX] = kopica_VALUE[podatki_ARRAY + 2 + Loop_INDEX]; kopica_VALUE[podatki_ARRAY + 1 + vnos_COUNT] = 0; kopica_VALUE[predmet_Gradiva + 3] = vnos_COUNT - 1; }
            넣기(이전값, 2); return;
        }
        if (대응참조 && (Word_SMS(ime_konstanta, "get") || Word_SMS(ime_konstanta, "remove")) && Word_SMS(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(ime_konstanta, "put") && Word_SMS(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(ime_konstanta, "containsKey") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Word_SMS(ime_konstanta, "put"), odstraniti = Word_SMS(ime_konstanta, "remove");
            int podatki_VALUE = 넣기여부 ? 빼기(2) : 0, Ključ_Gradiva = 빼기(2), predmet_Gradiva = 빼기(2); if (!predmet_VALUE(predmet_Gradiva, 11)) return;
            int vnos_COUNT = kopica_VALUE[predmet_Gradiva + 3], podatki_ARRAY = kopica_VALUE[predmet_Gradiva + 2], 찾은여부 = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < vnos_COUNT; Loop_INDEX++) if (값같음(Ključ_Gradiva, kopica_VALUE[podatki_ARRAY + 2 + 2 * Loop_INDEX])) { 찾은여부 = Loop_INDEX; break; }
            int 이전값 = 찾은여부 < 0 ? 0 : kopica_VALUE[podatki_ARRAY + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(predmet_Gradiva, (vnos_COUNT + 1) * 2); podatki_ARRAY = kopica_VALUE[predmet_Gradiva + 2]; 찾은여부 = vnos_COUNT; if (!NAPAKA) kopica_VALUE[predmet_Gradiva + 3] = vnos_COUNT + 1; }
                if (!NAPAKA) { kopica_VALUE[podatki_ARRAY + 2 + 2 * 찾은여부] = Ključ_Gradiva; kopica_VALUE[podatki_ARRAY + 3 + 2 * 찾은여부] = podatki_VALUE; }
            }
            if (odstraniti && 찾은여부 >= 0) { for (int Loop_INDEX = 찾은여부 + 1; Loop_INDEX < vnos_COUNT; Loop_INDEX++) { kopica_VALUE[podatki_ARRAY + 2 * Loop_INDEX] = kopica_VALUE[podatki_ARRAY + 2 + 2 * Loop_INDEX]; kopica_VALUE[podatki_ARRAY + 1 + 2 * Loop_INDEX] = kopica_VALUE[podatki_ARRAY + 3 + 2 * Loop_INDEX]; } kopica_VALUE[podatki_ARRAY + 2 * vnos_COUNT] = 0; kopica_VALUE[podatki_ARRAY + 1 + 2 * vnos_COUNT] = 0; kopica_VALUE[predmet_Gradiva + 3] = vnos_COUNT - 1; }
            if (Word_SMS(ime_konstanta, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(이전값, 2);
            return;
        }
        napaka_VALUE("unsupported collection method");
    }
    static boolean 잠금얻기(int predmet_Gradiva) {
        if (!객체유효(predmet_Gradiva)) return false;
        if (잠금깊이[predmet_Gradiva] != 0 && zaklepanje_lastnik[predmet_Gradiva] != sprotno_nit + 1) { spremeniti_zahteva = true; return false; }
        zaklepanje_lastnik[predmet_Gradiva] = sprotno_nit + 1; 잠금깊이[predmet_Gradiva]++; return true;
    }
    static void izdaja_zaklepanje(int predmet_Gradiva) {
        if (!객체유효(predmet_Gradiva)) return;
        if (잠금깊이[predmet_Gradiva] == 0 || zaklepanje_lastnik[predmet_Gradiva] != sprotno_nit + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[predmet_Gradiva] == 0) zaklepanje_lastnik[predmet_Gradiva] = 0;
    }
    static boolean SWITCH_nit() {
        nit_okvir[sprotno_nit] = okvir_INDEX;
        if (okvir_INDEX < sprotno_nit * 32) nit_stanje[sprotno_nit] = 3;
        for (int Loop_INDEX = 0; Loop_INDEX < nit_COUNT; Loop_INDEX++) if (nit_stanje[Loop_INDEX] == 2 && nit_stanje[가닥대기[Loop_INDEX]] == 3) nit_stanje[Loop_INDEX] = 1;
        for (int Loop_INDEX = 1; Loop_INDEX <= nit_COUNT; Loop_INDEX++) {
            int Naprej_položaj = (sprotno_nit + Loop_INDEX) % nit_COUNT;
            if (nit_stanje[Naprej_položaj] == 1) { sprotno_nit = Naprej_položaj; okvir_INDEX = nit_okvir[Naprej_položaj]; spremeniti_zahteva = false; return true; }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < nit_COUNT; Loop_INDEX++) if (nit_stanje[Loop_INDEX] != 3) { napaka_VALUE("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int ime_konstanta, int 서술상수, int ukaz_CODE) { Proces_nit(ime_konstanta, 서술상수, ukaz_CODE, false); }
    static void Proces_nit(int ime_konstanta, int 서술상수, int ukaz_CODE, boolean slovenščina) {
        if (ukaz_CODE == 184 && Word_SMS(ime_konstanta, slovenščina ? "YIELD_opravek" : "yield") && Word_SMS(서술상수, "()V")) { spremeniti_zahteva = true; return; }
        if (ukaz_CODE == 184 && Word_SMS(ime_konstanta, "currentThread") && Word_SMS(서술상수, "()Ljava/lang/Thread;")) { 넣기(nit_predmet[sprotno_nit], 2); return; }
        if (ukaz_CODE == 183 && Word_SMS(ime_konstanta, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, slovenščina ? "(Lslovenščina/lastno/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int cilj_naslov = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), predmet_Gradiva = 빼기(2);
            if (!객체유효(predmet_Gradiva)) return;
            if (kopica_VALUE[predmet_Gradiva] == 13) { kopica_VALUE[predmet_Gradiva + 2] = cilj_naslov; kopica_Gradiva[predmet_Gradiva + 2] = 1; }
            else if (cilj_naslov != 0) napaka_VALUE("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (ukaz_CODE == 182 && (Word_SMS(ime_konstanta, slovenščina ? "Start_opravek" : "start") || Word_SMS(ime_konstanta, slovenščina ? "기다리기" : "join")) && Word_SMS(서술상수, "()V") || ukaz_CODE == 182 && Word_SMS(ime_konstanta, slovenščina ? "살아있는가" : "isAlive") && Word_SMS(서술상수, "()Z")) {
            int predmet_Gradiva = 빼기(2); if (!객체유효(predmet_Gradiva)) return;
            int račun_VALUE = -1; for (int Loop_INDEX = 0; Loop_INDEX < nit_COUNT; Loop_INDEX++) if (nit_predmet[Loop_INDEX] == predmet_Gradiva) račun_VALUE = Loop_INDEX;
            if (Word_SMS(ime_konstanta, slovenščina ? "살아있는가" : "isAlive")) { 넣기(račun_VALUE >= 0 && nit_stanje[račun_VALUE] != 3 ? 1 : 0, 1); return; }
            if (Word_SMS(ime_konstanta, slovenščina ? "기다리기" : "join")) { if (račun_VALUE >= 0 && nit_stanje[račun_VALUE] != 3) { 가닥대기[sprotno_nit] = račun_VALUE; nit_stanje[sprotno_nit] = 2; spremeniti_zahteva = true; } return; }
            if (račun_VALUE >= 0) { 예외던짐(slovenščina ? 38 : 16, "thread already started"); return; }
            if (nit_COUNT == 4) { napaka_VALUE("thread limit (4 including main)"); return; }
            int cilj_naslov = kopica_VALUE[predmet_Gradiva] == 13 ? kopica_VALUE[predmet_Gradiva + 2] : predmet_Gradiva;
            int Datoteka_INDEX = cilj_naslov > 0 && kopica_VALUE[cilj_naslov] >= 32 ? ime_metoda(kopica_VALUE[cilj_naslov] - 32, slovenščina ? "Izvedi" : "run", "()V") : -1;
            if (cilj_naslov != 0 && Datoteka_INDEX < 0) { napaka_VALUE("Runnable.run required"); return; }
            račun_VALUE = nit_COUNT++; nit_predmet[račun_VALUE] = predmet_Gradiva; nit_cilj[račun_VALUE] = cilj_naslov;
            int okvir = račun_VALUE * 32; nit_okvir[račun_VALUE] = Datoteka_INDEX < 0 ? okvir - 1 : okvir; nit_stanje[račun_VALUE] = Datoteka_INDEX < 0 ? 3 : 1;
            if (Datoteka_INDEX >= 0) { okvir_metoda[okvir] = Datoteka_INDEX; okvir_položaj[okvir] = metoda_Start[Datoteka_INDEX]; lokalen_krajeven_VALUE[okvir * 128] = cilj_naslov; lokalen_krajeven_Tip[okvir * 128] = 2; }
            return;
        }
        napaka_VALUE("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], naslov_SMS = new int[16];
    static int lokalen_krajeven_naslov() { return naslov_predmet(0x7f000001); }
    static int naslov_predmet(int VALUE) { int predmet_Gradiva = dodeliti_Senzor_prostora(14, 1); if (!NAPAKA) kopica_VALUE[predmet_Gradiva + 2] = VALUE; return predmet_Gradiva; }
    static int 주소해독(int predmet_Gradiva) {
        if (predmet_Gradiva == 0 || 글같음(predmet_Gradiva, gostiti_znak("localhost"), false)) return 0x7f000001;
        if (!predmet_VALUE(predmet_Gradiva, 1)) return 0;
        int podatki_VALUE = 0, skupaj_COUNT = 0, naslov_bajt = 0, 자릿수 = 0, vnos_COUNT = kopica_VALUE[predmet_Gradiva + 1];
        for (int Loop_INDEX = 0; Loop_INDEX <= vnos_COUNT; Loop_INDEX++) {
            int koda_znaka = Loop_INDEX == vnos_COUNT ? '.' : kopica_VALUE[predmet_Gradiva + 2 + Loop_INDEX];
            if (koda_znaka == '.') { if (자릿수 == 0 || skupaj_COUNT == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } podatki_VALUE = podatki_VALUE << 8 | naslov_bajt; skupaj_COUNT++; naslov_bajt = 자릿수 = 0; }
            else { if (koda_znaka < '0' || koda_znaka > '9' || ++자릿수 > 3 || (naslov_bajt = naslov_bajt * 10 + koda_znaka - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (skupaj_COUNT != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return podatki_VALUE;
    }
    static int naslov_znak(int podatki_VALUE) {
        int vnos_COUNT = 0;
        for (int 이동비트 = 24; 이동비트 >= 0; 이동비트 -= 8) {
            int naslov_bajt = podatki_VALUE >>> 이동비트 & 255;
            if (naslov_bajt >= 100) naslov_SMS[vnos_COUNT++] = '0' + naslov_bajt / 100;
            if (naslov_bajt >= 10) naslov_SMS[vnos_COUNT++] = '0' + naslov_bajt / 10 % 10;
            naslov_SMS[vnos_COUNT++] = '0' + naslov_bajt % 10; if (이동비트 != 0) naslov_SMS[vnos_COUNT++] = '.';
        }
        int predmet_Gradiva = dodeliti_Senzor_prostora(1, vnos_COUNT); if (!NAPAKA) for (int Loop_INDEX = 0; Loop_INDEX < vnos_COUNT; Loop_INDEX++) kopica_VALUE[predmet_Gradiva + 2 + Loop_INDEX] = naslov_SMS[Loop_INDEX]; return predmet_Gradiva;
    }
    static void 통신호출(int lastnik, int ime_konstanta, int 서술상수, int ukaz_CODE) {
        if (Word_SMS(lastnik, "java/net/InetAddress")) {
            if (ukaz_CODE == 184 && Word_SMS(ime_konstanta, "getLoopbackAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;")) { 넣기(lokalen_krajeven_naslov(), 2); return; }
            if (ukaz_CODE == 184 && Word_SMS(ime_konstanta, "getByName") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int podatki_VALUE = 주소해독(빼기(2)); if (던진객체 == 0 && !NAPAKA) 넣기(naslov_predmet(podatki_VALUE), 2); return;
            }
            if (ukaz_CODE == 182 && Word_SMS(ime_konstanta, "getHostAddress") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int predmet_Gradiva = 빼기(2); if (predmet_VALUE(predmet_Gradiva, 14)) 넣기(naslov_znak(kopica_VALUE[predmet_Gradiva + 2]), 2); return; }
        }
        if (Word_SMS(lastnik, "java/net/DatagramPacket")) {
            if (ukaz_CODE == 183 && Word_SMS(ime_konstanta, "<init>") && (Word_SMS(서술상수, "([BI)V") || Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean cilj_VALUE_Gradiva = Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"); int številka_vrat = cilj_VALUE_Gradiva ? 빼기(1) : 0, naslov_Gradiva = cilj_VALUE_Gradiva ? 빼기(2) : 0;
                int vnos_COUNT = 빼기(1), podatki_ARRAY = 빼기(2), predmet_Gradiva = 빼기(2);
                if (!predmet_VALUE(predmet_Gradiva, 16) || !predmet_VALUE(podatki_ARRAY, 20)) return;
                if (vnos_COUNT < 0 || vnos_COUNT > kopica_VALUE[podatki_ARRAY + 1] || številka_vrat < 0 || številka_vrat > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (naslov_Gradiva != 0 && !predmet_VALUE(naslov_Gradiva, 14)) return;
                kopica_VALUE[predmet_Gradiva + 2] = podatki_ARRAY; kopica_Gradiva[predmet_Gradiva + 2] = 1; kopica_VALUE[predmet_Gradiva + 3] = vnos_COUNT;
                kopica_VALUE[predmet_Gradiva + 4] = naslov_Gradiva; kopica_Gradiva[predmet_Gradiva + 4] = 1; kopica_VALUE[predmet_Gradiva + 5] = številka_vrat; return;
            }
            if (ukaz_CODE == 182 && Word_SMS(ime_konstanta, "setLength") && Word_SMS(서술상수, "(I)V")) {
                int vnos_COUNT = 빼기(1), predmet_Gradiva = 빼기(2); if (!predmet_VALUE(predmet_Gradiva, 16)) return;
                if (vnos_COUNT < 0 || vnos_COUNT > kopica_VALUE[kopica_VALUE[predmet_Gradiva + 2] + 1]) 예외던짐(9, "invalid datagram length"); else kopica_VALUE[predmet_Gradiva + 3] = vnos_COUNT; return;
            }
            if (ukaz_CODE == 182 && (Word_SMS(ime_konstanta, "getData") && Word_SMS(서술상수, "()[B") || Word_SMS(ime_konstanta, "getLength") && Word_SMS(서술상수, "()I") || Word_SMS(ime_konstanta, "getAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;") || Word_SMS(ime_konstanta, "getPort") && Word_SMS(서술상수, "()I"))) {
                int predmet_Gradiva = 빼기(2); if (!predmet_VALUE(predmet_Gradiva, 16)) return;
                int vnos_položaj = Word_SMS(ime_konstanta, "getData") ? 2 : Word_SMS(ime_konstanta, "getLength") ? 3 : Word_SMS(ime_konstanta, "getAddress") ? 4 : 5;
                넣기(kopica_VALUE[predmet_Gradiva + vnos_položaj], vnos_položaj == 2 || vnos_položaj == 4 ? 2 : 1); return;
            }
        }
        if (Word_SMS(lastnik, "java/net/DatagramSocket")) {
            if (ukaz_CODE == 183 && Word_SMS(ime_konstanta, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(I)V"))) {
                int številka_vrat = Word_SMS(서술상수, "()V") ? 0 : 빼기(1), predmet_Gradiva = 빼기(2); if (!predmet_VALUE(predmet_Gradiva, 15)) return;
                if (številka_vrat < 0 || številka_vrat > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = uporabnik.odprto_mreža(številka_vrat); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else kopica_VALUE[predmet_Gradiva + 2] = 열린파일번호; return;
            }
            if (ukaz_CODE == 182 && Word_SMS(ime_konstanta, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), predmet_Gradiva = 빼기(2); if (!predmet_VALUE(predmet_Gradiva, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else kopica_VALUE[predmet_Gradiva + 3] = 밀리초값; return;
            }
            if (ukaz_CODE == 182 && Word_SMS(ime_konstanta, "getLocalPort") && Word_SMS(서술상수, "()I")) { int predmet_Gradiva = 빼기(2); if (predmet_VALUE(predmet_Gradiva, 15)) 넣기(kopica_VALUE[predmet_Gradiva + 2] < 0 ? -1 : uporabnik.mreža_vrata(kopica_VALUE[predmet_Gradiva + 2]), 1); return; }
            if (ukaz_CODE == 182 && Word_SMS(ime_konstanta, "isClosed") && Word_SMS(서술상수, "()Z")) { int predmet_Gradiva = 빼기(2); if (predmet_VALUE(predmet_Gradiva, 15)) 넣기(kopica_VALUE[predmet_Gradiva + 2] < 0 ? 1 : 0, 1); return; }
            if (ukaz_CODE == 182 && Word_SMS(ime_konstanta, "close") && Word_SMS(서술상수, "()V")) { int predmet_Gradiva = 빼기(2); if (predmet_VALUE(predmet_Gradiva, 15) && kopica_VALUE[predmet_Gradiva + 2] >= 0) { uporabnik.파일서술자닫기(kopica_VALUE[predmet_Gradiva + 2]); kopica_VALUE[predmet_Gradiva + 2] = -1; } return; }
            if (ukaz_CODE == 182 && (Word_SMS(ime_konstanta, "send") || Word_SMS(ime_konstanta, "receive")) && Word_SMS(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int paket = 빼기(2), predmet_Gradiva = 빼기(2); if (!predmet_VALUE(paket, 16) || !predmet_VALUE(predmet_Gradiva, 15)) return;
                int podatki_ARRAY = kopica_VALUE[paket + 2], 유효길이 = kopica_VALUE[paket + 3], 열린파일번호 = kopica_VALUE[predmet_Gradiva + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Word_SMS(ime_konstanta, "send")) {
                    if (!predmet_VALUE(kopica_VALUE[paket + 4], 14)) return;
                    if (유효길이 > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < 유효길이; Loop_INDEX++) 통신임시[Loop_INDEX] = kopica_VALUE[podatki_ARRAY + 2 + Loop_INDEX];
                    if (uporabnik.poslati_mreža(열린파일번호, kopica_VALUE[kopica_VALUE[paket + 4] + 2], kopica_VALUE[paket + 5], 통신임시, 유효길이) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int vnos_COUNT = uporabnik.sprejeti_sprejemati_prejeti_prejemati_mreža(열린파일번호, 통신임시, 유효길이 > 512 ? 512 : 유효길이);
                    if (vnos_COUNT == -11) {
                        int sprotno_čas = uporabnik.밀리초();
                        if (kopica_VALUE[predmet_Gradiva + 4] == 0) kopica_VALUE[predmet_Gradiva + 4] = sprotno_čas + 1;
                        if (kopica_VALUE[predmet_Gradiva + 3] > 0 && sprotno_čas - (kopica_VALUE[predmet_Gradiva + 4] - 1) >= kopica_VALUE[predmet_Gradiva + 3]) { kopica_VALUE[predmet_Gradiva + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(predmet_Gradiva, 2); 넣기(paket, 2); okvir_položaj[okvir_INDEX] = okvir_navodilo[okvir_INDEX]; spremeniti_zahteva = true; return;
                    }
                    kopica_VALUE[predmet_Gradiva + 4] = 0;
                    if (vnos_COUNT < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < vnos_COUNT; Loop_INDEX++) kopica_VALUE[podatki_ARRAY + 2 + Loop_INDEX] = (byte)통신임시[Loop_INDEX];
                    kopica_VALUE[paket + 3] = vnos_COUNT; kopica_VALUE[paket + 4] = naslov_predmet(통신임시[513]); kopica_Gradiva[paket + 4] = 1; kopica_VALUE[paket + 5] = 통신임시[512];
                }
                return;
            }
        }
        napaka_VALUE("unsupported java.net method");
    }
    static boolean 흐름대기(int predmet_Gradiva) {
        int sprotno_čas = uporabnik.밀리초();
        if (kopica_VALUE[predmet_Gradiva + 5] == 0) kopica_VALUE[predmet_Gradiva + 5] = sprotno_čas + 1;
        if (kopica_VALUE[predmet_Gradiva + 3] > 0 && sprotno_čas - (kopica_VALUE[predmet_Gradiva + 5] - 1) >= kopica_VALUE[predmet_Gradiva + 3]) { kopica_VALUE[predmet_Gradiva + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        okvir_položaj[okvir_INDEX] = okvir_navodilo[okvir_INDEX]; spremeniti_zahteva = true; return true;
    }
    static void 흐름호출(int lastnik, int ime_konstanta, int 서술상수, int ukaz_CODE) {
        boolean sprejeti_sprejemati_prejeti_prejemati_stran = Word_SMS(lastnik, "java/net/ServerSocket"), tok = Word_SMS(lastnik, "java/io/InputStream") || Word_SMS(lastnik, "java/io/OutputStream");
        if (!tok && ukaz_CODE == 183 && Word_SMS(ime_konstanta, "<init>")) {
            boolean informacijska_tehnologija_prazen_stanje = Word_SMS(서술상수, "()V"), 이름지정여부 = Word_SMS(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = Word_SMS(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(informacijska_tehnologija_prazen_stanje || sprejeti_sprejemati_prejeti_prejemati_stran && Word_SMS(서술상수, "(I)V") || !sprejeti_sprejemati_prejeti_prejemati_stran && (이름지정여부 || 주소지정여부))) { napaka_VALUE("unsupported socket constructor"); return; }
            int številka_vrat = informacijska_tehnologija_prazen_stanje ? 0 : 빼기(1), naslov_Gradiva = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, predmet_Gradiva = 빼기(2);
            if (!predmet_VALUE(predmet_Gradiva, sprejeti_sprejemati_prejeti_prejemati_stran ? 18 : 17)) return;
            if (številka_vrat < 0 || številka_vrat > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !predmet_VALUE(naslov_Gradiva, 14)) return;
            int omrežni_identifikator = 이름지정여부 ? 주소해독(naslov_Gradiva) : 주소지정여부 ? kopica_VALUE[naslov_Gradiva + 2] : 0x7f000001;
            if (NAPAKA || 던진객체 != 0) return;
            int 열린파일번호 = uporabnik.tok_nadzor(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = informacijska_tehnologija_prazen_stanje ? 0 : sprejeti_sprejemati_prejeti_prejemati_stran ? uporabnik.tok_nadzor(1, 열린파일번호, številka_vrat) : uporabnik.POVEŽI_tok(열린파일번호, omrežni_identifikator, številka_vrat);
            if (처리값 < 0) { uporabnik.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            kopica_VALUE[predmet_Gradiva + 2] = 열린파일번호; kopica_VALUE[predmet_Gradiva + 4] = številka_vrat; kopica_VALUE[predmet_Gradiva + 6] = informacijska_tehnologija_prazen_stanje ? 0 : 1; return;
        }
        if (!tok && Word_SMS(ime_konstanta, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), predmet_Gradiva = 빼기(2); if (!predmet_VALUE(predmet_Gradiva, sprejeti_sprejemati_prejeti_prejemati_stran ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else kopica_VALUE[predmet_Gradiva + 3] = 밀리초값; return; }
        if (!tok && Word_SMS(ime_konstanta, "close") && Word_SMS(서술상수, "()V")) { int predmet_Gradiva = 빼기(2); if (predmet_VALUE(predmet_Gradiva, sprejeti_sprejemati_prejeti_prejemati_stran ? 18 : 17) && kopica_VALUE[predmet_Gradiva + 2] >= 0) { uporabnik.파일서술자닫기(kopica_VALUE[predmet_Gradiva + 2]); kopica_VALUE[predmet_Gradiva + 2] = -1; } return; }
        if (!tok && (Word_SMS(ime_konstanta, "getLocalPort") || Word_SMS(ime_konstanta, "getPort") || Word_SMS(ime_konstanta, "isClosed") || Word_SMS(ime_konstanta, "isConnected"))) {
            int predmet_Gradiva = 빼기(2); if (!predmet_VALUE(predmet_Gradiva, sprejeti_sprejemati_prejeti_prejemati_stran ? 18 : 17)) return;
            넣기(Word_SMS(ime_konstanta, "isClosed") ? kopica_VALUE[predmet_Gradiva + 2] < 0 ? 1 : 0 : Word_SMS(ime_konstanta, "isConnected") ? kopica_VALUE[predmet_Gradiva + 6] : Word_SMS(ime_konstanta, "getPort") ? kopica_VALUE[predmet_Gradiva + 4] : kopica_VALUE[predmet_Gradiva + 2] < 0 ? -1 : uporabnik.tok_nadzor(4, kopica_VALUE[predmet_Gradiva + 2], 0), 1); return;
        }
        if (sprejeti_sprejemati_prejeti_prejemati_stran && Word_SMS(ime_konstanta, "accept") && Word_SMS(서술상수, "()Ljava/net/Socket;")) {
            int predmet_Gradiva = 빼기(2); if (!predmet_VALUE(predmet_Gradiva, 18)) return; int 열린파일번호 = uporabnik.tok_nadzor(3, kopica_VALUE[predmet_Gradiva + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(predmet_Gradiva)) 넣기(predmet_Gradiva, 2); return; }
            kopica_VALUE[predmet_Gradiva + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = dodeliti_Senzor_prostora(17, 5); if (NAPAKA) { uporabnik.파일서술자닫기(열린파일번호); return; } kopica_VALUE[반환값 + 2] = 열린파일번호; kopica_VALUE[반환값 + 4] = uporabnik.tok_nadzor(5, 열린파일번호, 0); kopica_VALUE[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!sprejeti_sprejemati_prejeti_prejemati_stran && !tok && ((Word_SMS(ime_konstanta, "getInputStream") && Word_SMS(서술상수, "()Ljava/io/InputStream;")) || (Word_SMS(ime_konstanta, "getOutputStream") && Word_SMS(서술상수, "()Ljava/io/OutputStream;")))) {
            int predmet_Gradiva = 빼기(2); if (!predmet_VALUE(predmet_Gradiva, 17)) return; if (kopica_VALUE[predmet_Gradiva + 2] < 0 || kopica_VALUE[predmet_Gradiva + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = dodeliti_Senzor_prostora(19, 4); if (NAPAKA) return; kopica_VALUE[반환값 + 2] = predmet_Gradiva; kopica_Gradiva[반환값 + 2] = 1; kopica_VALUE[반환값 + 3] = Word_SMS(ime_konstanta, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (tok) {
            boolean 읽기여부 = Word_SMS(ime_konstanta, "read"), informacijska_tehnologija_pisati_postopek = Word_SMS(ime_konstanta, "write"), blok = Word_SMS(서술상수, "([B)I") || Word_SMS(서술상수, "([B)V"), informacijska_tehnologija_SUBARRAY = Word_SMS(서술상수, "([BII)I") || Word_SMS(서술상수, "([BII)V");
            int vnos_COUNT = informacijska_tehnologija_SUBARRAY ? 빼기(1) : 0, 시작변위 = informacijska_tehnologija_SUBARRAY ? 빼기(1) : 0, podatki_ARRAY = blok || informacijska_tehnologija_SUBARRAY ? 빼기(2) : 0;
            int podatki_VALUE = informacijska_tehnologija_pisati_postopek && Word_SMS(서술상수, "(I)V") ? 빼기(1) : 0, predmet_Gradiva = 빼기(2);
            if (!predmet_VALUE(predmet_Gradiva, 19)) return; int nadrejen_Gradiva = kopica_VALUE[predmet_Gradiva + 2], 열린파일번호 = kopica_VALUE[nadrejen_Gradiva + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Word_SMS(ime_konstanta, "close") && Word_SMS(서술상수, "()V")) { uporabnik.파일서술자닫기(열린파일번호); kopica_VALUE[nadrejen_Gradiva + 2] = -1; return; }
            if (Word_SMS(ime_konstanta, "flush") && Word_SMS(서술상수, "()V")) return;
            if ((!읽기여부 && !informacijska_tehnologija_pisati_postopek) || 읽기여부 != (kopica_VALUE[predmet_Gradiva + 3] == 0)) { napaka_VALUE("unsupported stream operation"); return; }
            if (blok || informacijska_tehnologija_SUBARRAY) { if (!predmet_VALUE(podatki_ARRAY, 20)) return; if (blok) vnos_COUNT = kopica_VALUE[podatki_ARRAY + 1]; if (시작변위 < 0 || vnos_COUNT < 0 || 시작변위 > kopica_VALUE[podatki_ARRAY + 1] - vnos_COUNT) { 예외던짐(6, "stream array bounds"); return; } }
            else vnos_COUNT = 1;
            if (vnos_COUNT == 0) { if (읽기여부) 넣기(0, 1); return; }
            int Dokončano_COUNT = informacijska_tehnologija_pisati_postopek ? kopica_VALUE[predmet_Gradiva + 4] : 0, 처리값 = 0;
            while (Dokončano_COUNT < vnos_COUNT) {
                처리값 = 읽기여부 ? uporabnik.파일한바이트읽기(열린파일번호) : uporabnik.파일한바이트쓰기(열린파일번호, blok || informacijska_tehnologija_SUBARRAY ? kopica_VALUE[podatki_ARRAY + 2 + 시작변위 + Dokončano_COUNT] : podatki_VALUE);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (blok || informacijska_tehnologija_SUBARRAY)) kopica_VALUE[podatki_ARRAY + 2 + 시작변위 + Dokončano_COUNT] = (byte)처리값;
                Dokončano_COUNT++; if (읽기여부 && !(blok || informacijska_tehnologija_SUBARRAY)) break;
            }
            if (처리값 == -11 && (informacijska_tehnologija_pisati_postopek || Dokončano_COUNT == 0)) {
                kopica_VALUE[predmet_Gradiva + 4] = Dokončano_COUNT;
                if (흐름대기(nadrejen_Gradiva)) { 넣기(predmet_Gradiva, 2); if (blok || informacijska_tehnologija_SUBARRAY) 넣기(podatki_ARRAY, 2); if (informacijska_tehnologija_SUBARRAY) { 넣기(시작변위, 1); 넣기(vnos_COUNT, 1); } if (informacijska_tehnologija_pisati_postopek && !(blok || informacijska_tehnologija_SUBARRAY)) 넣기(podatki_VALUE, 1); } return;
            }
            kopica_VALUE[predmet_Gradiva + 4] = 0; kopica_VALUE[nadrejen_Gradiva + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(Dokončano_COUNT == 0 && 처리값 == 256 ? -1 : blok || informacijska_tehnologija_SUBARRAY ? Dokončano_COUNT : 처리값, 1); return;
        }
        napaka_VALUE("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int ime_konstanta) {
        if (Word_SMS(ime_konstanta, "slovenščina/lastno/okno")) return 24;
        if (Word_SMS(ime_konstanta, "slovenščina/lastno/Oznaka")) return 26;
        if (Word_SMS(ime_konstanta, "slovenščina/lastno/Gumb")) return 27;
        if (Word_SMS(ime_konstanta, "slovenščina/lastno/SMS_polje")) return 28;
        if (Word_SMS(ime_konstanta, "slovenščina/lastno/akcija_obvestilo")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int ime_konstanta) {
        return 한국어화면종(ime_konstanta) != 0 || Word_SMS(ime_konstanta, "slovenščina/lastno/화면구성요소") || Word_SMS(ime_konstanta, "slovenščina/lastno/dogodek_čakalna_vrsta");
    }
    static int 화면종(int ime_konstanta) {
        int 한국어종 = 한국어화면종(ime_konstanta); if (한국어종 != 0) return 한국어종;
        if (Word_SMS(ime_konstanta, "javax/swing/JFrame")) return 24;
        if (Word_SMS(ime_konstanta, "javax/swing/JPanel")) return 25;
        if (Word_SMS(ime_konstanta, "javax/swing/JLabel")) return 26;
        if (Word_SMS(ime_konstanta, "javax/swing/JButton")) return 27;
        if (Word_SMS(ime_konstanta, "javax/swing/JTextField")) return 28;
        if (Word_SMS(ime_konstanta, "java/awt/event/ActionEvent")) return 29;
        if (Word_SMS(ime_konstanta, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int ime_konstanta) {
        return 화면종(ime_konstanta) != 0 || Word_SMS(ime_konstanta, "java/awt/Component") || Word_SMS(ime_konstanta, "java/awt/Container") || Word_SMS(ime_konstanta, "javax/swing/JComponent") || Word_SMS(ime_konstanta, "javax/swing/AbstractButton") || Word_SMS(ime_konstanta, "javax/swing/text/JTextComponent") || Word_SMS(ime_konstanta, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int predmet_Gradiva) { if (!객체유효(predmet_Gradiva)) return false; if (kopica_VALUE[predmet_Gradiva] < 24 || kopica_VALUE[predmet_Gradiva] > 28) { napaka_VALUE("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int predmet_Gradiva, int SMS_Gradiva) {
        if (SMS_Gradiva != 0 && !predmet_VALUE(SMS_Gradiva, 1)) return;
        int vnos_COUNT = SMS_Gradiva == 0 ? 0 : kopica_VALUE[SMS_Gradiva + 1]; if (vnos_COUNT > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < vnos_COUNT; Loop_INDEX++) 화면글임시[Loop_INDEX] = kopica_VALUE[SMS_Gradiva + 2 + Loop_INDEX];
        if (uporabnik.화면글(kopica_VALUE[predmet_Gradiva + 2], 화면글임시, vnos_COUNT) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        kopica_VALUE[predmet_Gradiva + 3] = SMS_Gradiva; kopica_Gradiva[predmet_Gradiva + 3] = 1;
    }
    static int 화면문자읽기(int predmet_Gradiva) {
        int račun_VALUE = kopica_VALUE[predmet_Gradiva + 2], vnos_COUNT = uporabnik.화면연결(8, račun_VALUE, 0, 0, 0, 0), 사용수 = 0;
        if (vnos_COUNT < 0) { napaka_VALUE("GUI text read failed"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < vnos_COUNT; Loop_INDEX++) { int 부호값 = uporabnik.화면연결(9, račun_VALUE, Loop_INDEX, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = dodeliti_Senzor_prostora(1, 사용수); if (!NAPAKA) for (int Loop_INDEX = 0; Loop_INDEX < 사용수; Loop_INDEX++) kopica_VALUE[반환값 + 2 + Loop_INDEX] = 화면글임시[Loop_INDEX]; return 반환값;
    }
    /* slovenščina 객체를 직접 만들고 jedro_VALUE 화면 기능에 연결한다. Swing predmet_VALUE/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int lastnik, int ime_konstanta, int 서술상수, int ukaz_CODE) {
        if (Word_SMS(lastnik, "slovenščina/lastno/dogodek_čakalna_vrsta")) {
            if (ukaz_CODE == 184 && Word_SMS(ime_konstanta, "나중에실행") && Word_SMS(서술상수, "(Lslovenščina/lastno/실행할일;)V")) {
                int opravek_akcija = 빼기(2); if (!객체유효(opravek_akcija)) return;
                if (나중수 == 8) { napaka_VALUE("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = opravek_akcija; return;
            }
            if (ukaz_CODE == 184 && Word_SMS(ime_konstanta, "사건처리중인가") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            napaka_VALUE("지원하지 않는 slovenščina 화면 일정 호출"); return;
        }
        if (Word_SMS(lastnik, "slovenščina/lastno/akcija_obvestilo")) {
            int obvestilo = 빼기(2); if (!predmet_VALUE(obvestilo, 29) || kopica_VALUE[obvestilo + 3] == 0) return;
            if (Word_SMS(ime_konstanta, "vir_dogodka") && Word_SMS(서술상수, "()Lslovenščina/lastno/화면구성요소;")) 넣기(kopica_VALUE[obvestilo + 2], 2);
            else if (Word_SMS(ime_konstanta, "ukaz_SMS") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(kopica_VALUE[obvestilo + 2]), 2);
            else if (Word_SMS(ime_konstanta, "INDEX") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else napaka_VALUE("지원하지 않는 slovenščina Dejanje obvestilo 호출"); return;
        }
        if (ukaz_CODE == 183 && Word_SMS(ime_konstanta, "<init>")) {
            int 종류 = 한국어화면종(lastnik), 받이 = 0, 가로 = 0, Navpično_položaj = 0, 폭 = 0, višina_VALUE = 0;
            if (종류 == 24 && Word_SMS(서술상수, "(Ljava/lang/String;II)V")) {
                višina_VALUE = 빼기(1); 폭 = 빼기(1); 가로 = (uporabnik.화면너비() - 폭) / 2; Navpično_položaj = (uporabnik.화면높이() - višina_VALUE) / 2;
            } else if ((종류 == 26 || 종류 == 28) && Word_SMS(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && Word_SMS(서술상수, "(Ljava/lang/String;IIIILslovenščina/lastno/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                višina_VALUE = 빼기(1); 폭 = 빼기(1); Navpično_položaj = 빼기(1); 가로 = 빼기(1);
            } else { napaka_VALUE("지원하지 않는 slovenščina 화면 생성자"); return; }
            int Besedilo = 빼기(2), element_VALUE = 빼기(2); if (!화면객체(element_VALUE)) return;
            if (폭 < 1 || višina_VALUE < 1 || 가로 < 0 || Navpično_položaj < 0 || 폭 > uporabnik.화면너비() - 가로 || višina_VALUE > uporabnik.화면높이() - Navpično_položaj) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int INDEX = uporabnik.화면연결(0, 종류 - 23, 0, 0, 0, 0);
            if (INDEX < 1 || INDEX > 32) { napaka_VALUE("화면 element_VALUE 자리가 가득 찼습니다"); return; }
            kopica_VALUE[element_VALUE + 2] = INDEX; 화면참조[INDEX - 1] = element_VALUE;
            kopica_VALUE[element_VALUE + 5] = 가로; kopica_VALUE[element_VALUE + 6] = Navpično_položaj; kopica_VALUE[element_VALUE + 7] = 폭; kopica_VALUE[element_VALUE + 8] = višina_VALUE; kopica_VALUE[element_VALUE + 10] = 2;
            kopica_VALUE[element_VALUE + 4] = 받이; kopica_Gradiva[element_VALUE + 4] = 1; kopica_VALUE[element_VALUE + 12] = 1;
            uporabnik.화면연결(1, INDEX, 가로, Navpično_položaj, 폭, višina_VALUE);
            if (종류 == 24) uporabnik.화면연결(7, INDEX, 2, 0, 0, 0);
            화면문자설정(element_VALUE, Besedilo); return;
        }
        if (ukaz_CODE != 182) { napaka_VALUE("잘못된 slovenščina 화면 호출 Ukaz"); return; }
        if (Word_SMS(ime_konstanta, "pisati_SMS") && Word_SMS(서술상수, "(Ljava/lang/String;)V")) {
            int Besedilo = 빼기(2), element_VALUE = 빼기(2); if (화면객체(element_VALUE)) 화면문자설정(element_VALUE, Besedilo); return;
        }
        if (Word_SMS(ime_konstanta, "글읽기") && Word_SMS(서술상수, "()Ljava/lang/String;")) {
            int element_VALUE = 빼기(2); if (화면객체(element_VALUE)) 넣기(화면문자읽기(element_VALUE), 2); return;
        }
        if (Word_SMS(ime_konstanta, "동작맡기기") && Word_SMS(서술상수, "(Lslovenščina/lastno/동작받이;)V")) {
            int 받이 = 빼기(2), element_VALUE = 빼기(2);
            if (화면객체(element_VALUE)) { kopica_VALUE[element_VALUE + 4] = 받이; kopica_Gradiva[element_VALUE + 4] = 1; kopica_VALUE[element_VALUE + 12] = 1; } return;
        }
        if (Word_SMS(ime_konstanta, "Dodaj_element") && Word_SMS(서술상수, "(Lslovenščina/lastno/화면구성요소;)V")) {
            int otrok_VALUE = 빼기(2), nadrejen_VALUE = 빼기(2); if (!화면객체(otrok_VALUE) || !화면객체(nadrejen_VALUE)) return;
            if (uporabnik.화면연결(2, kopica_VALUE[nadrejen_VALUE + 2], kopica_VALUE[otrok_VALUE + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            kopica_VALUE[otrok_VALUE + 11] = nadrejen_VALUE; kopica_Gradiva[otrok_VALUE + 11] = 1; return;
        }
        if (Word_SMS(ime_konstanta, "자리정하기") && Word_SMS(서술상수, "(IIII)V")) {
            int višina_VALUE = 빼기(1), 폭 = 빼기(1), Navpično_položaj = 빼기(1), 가로 = 빼기(1), element_VALUE = 빼기(2); if (!화면객체(element_VALUE)) return;
            if (uporabnik.화면연결(1, kopica_VALUE[element_VALUE + 2], 가로, Navpično_položaj, 폭, višina_VALUE) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            kopica_VALUE[element_VALUE + 5] = 가로; kopica_VALUE[element_VALUE + 6] = Navpično_položaj; kopica_VALUE[element_VALUE + 7] = 폭; kopica_VALUE[element_VALUE + 8] = višina_VALUE; return;
        }
        if ((Word_SMS(ime_konstanta, "oddaja_okno") || Word_SMS(ime_konstanta, "Zapri")) && Word_SMS(서술상수, "()V")) {
            boolean vidljivost_VALUE = Word_SMS(ime_konstanta, "oddaja_okno"); int element_VALUE = 빼기(2); if (!화면객체(element_VALUE)) return;
            if (uporabnik.화면연결(vidljivost_VALUE ? 3 : 4, kopica_VALUE[element_VALUE + 2], vidljivost_VALUE ? 1 : 0, 0, 0, 0) < 0) { napaka_VALUE("화면은 interaktiven 명령에서 실행해야 합니다"); return; }
            kopica_VALUE[element_VALUE + 9] = vidljivost_VALUE ? 1 : 0; return;
        }
        if (Word_SMS(ime_konstanta, "보이는가") && Word_SMS(서술상수, "()Z")) { int element_VALUE = 빼기(2); if (화면객체(element_VALUE)) 넣기(kopica_VALUE[element_VALUE + 9], 1); return; }
        napaka_VALUE("지원하지 않는 slovenščina 화면 metoda_VALUE");
    }
    static void 화면호출(int lastnik, int ime_konstanta, int 서술상수, int ukaz_CODE) {
        if (Word_SMS(lastnik, "javax/swing/SwingUtilities")) {
            if (ukaz_CODE == 184 && Word_SMS(ime_konstanta, "invokeLater") && Word_SMS(서술상수, "(Ljava/lang/Runnable;)V")) { int predmet_Gradiva = 빼기(2); if (!객체유효(predmet_Gradiva)) return; if (나중수 == 8) { napaka_VALUE("invokeLater queue full"); return; } 나중실행[나중수++] = predmet_Gradiva; return; }
            if (ukaz_CODE == 184 && Word_SMS(ime_konstanta, "isEventDispatchThread") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            napaka_VALUE("unsupported SwingUtilities method"); return;
        }
        if (Word_SMS(lastnik, "java/awt/event/ActionEvent")) {
            int predmet_Gradiva = 빼기(2); if (!predmet_VALUE(predmet_Gradiva, 29)) return;
            if (Word_SMS(ime_konstanta, "getSource") && Word_SMS(서술상수, "()Ljava/lang/Object;")) 넣기(kopica_VALUE[predmet_Gradiva + 2], 2);
            else if (Word_SMS(ime_konstanta, "getActionCommand") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(kopica_VALUE[predmet_Gradiva + 2]), 2);
            else if (Word_SMS(ime_konstanta, "getID") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else napaka_VALUE("unsupported ActionEvent method"); return;
        }
        if (ukaz_CODE == 183 && Word_SMS(ime_konstanta, "<init>")) {
            int COLUMNS = 0, SMS_Gradiva = 0;
            if (Word_SMS(서술상수, "(I)V")) COLUMNS = 빼기(1);
            else if (Word_SMS(서술상수, "(Ljava/lang/String;I)V")) { COLUMNS = 빼기(1); SMS_Gradiva = 빼기(2); }
            else if (Word_SMS(서술상수, "(Ljava/lang/String;)V")) SMS_Gradiva = 빼기(2);
            else if (Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Word_SMS(서술상수, "()V")) { napaka_VALUE("unsupported Swing constructor"); return; }
            int predmet_Gradiva = 빼기(2); if (!객체유효(predmet_Gradiva)) return;
            if (kopica_VALUE[predmet_Gradiva] == 30) { napaka_VALUE("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(predmet_Gradiva) || COLUMNS < 0) return;
            int račun_VALUE = uporabnik.화면연결(0, kopica_VALUE[predmet_Gradiva] - 23, 0, 0, 0, 0);
            if (račun_VALUE < 1 || račun_VALUE > 32) { napaka_VALUE("GUI widget slots exhausted"); return; }
            kopica_VALUE[predmet_Gradiva + 2] = račun_VALUE; 화면참조[račun_VALUE - 1] = predmet_Gradiva; kopica_VALUE[predmet_Gradiva + 5] = kopica_VALUE[predmet_Gradiva] == 24 ? 130 : 16; kopica_VALUE[predmet_Gradiva + 6] = kopica_VALUE[predmet_Gradiva] == 24 ? 110 : 16;
            kopica_VALUE[predmet_Gradiva + 7] = kopica_VALUE[predmet_Gradiva] == 24 ? 380 : 220; kopica_VALUE[predmet_Gradiva + 8] = kopica_VALUE[predmet_Gradiva] == 24 ? 240 : 28; kopica_VALUE[predmet_Gradiva + 10] = 1;
            화면문자설정(predmet_Gradiva, SMS_Gradiva); return;
        }
        if (Word_SMS(ime_konstanta, "setText") || Word_SMS(ime_konstanta, "setTitle")) { int SMS_Gradiva = 빼기(2), predmet_Gradiva = 빼기(2); if (화면객체(predmet_Gradiva) && Word_SMS(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(predmet_Gradiva, SMS_Gradiva); return; }
        if (Word_SMS(ime_konstanta, "getText") || Word_SMS(ime_konstanta, "getTitle")) { int predmet_Gradiva = 빼기(2); if (화면객체(predmet_Gradiva) && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(predmet_Gradiva), 2); return; }
        if (Word_SMS(ime_konstanta, "addActionListener") && Word_SMS(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int sprejeti_sprejemati_prejeti_prejemati_Gradiva = 빼기(2), predmet_Gradiva = 빼기(2); if (화면객체(predmet_Gradiva)) { kopica_VALUE[predmet_Gradiva + 4] = sprejeti_sprejemati_prejeti_prejemati_Gradiva; kopica_Gradiva[predmet_Gradiva + 4] = 1; } return; }
        if (Word_SMS(ime_konstanta, "getContentPane") && Word_SMS(서술상수, "()Ljava/awt/Container;")) { int predmet_Gradiva = 빼기(2); if (화면객체(predmet_Gradiva)) 넣기(predmet_Gradiva, 2); return; }
        if (Word_SMS(ime_konstanta, "setLayout") && Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) { int Krmarjenje_Gradiva = 빼기(2), predmet_Gradiva = 빼기(2); if (화면객체(predmet_Gradiva) && Krmarjenje_Gradiva != 0) napaka_VALUE("only absolute layout (null) is supported"); return; }
        if (Word_SMS(ime_konstanta, "add") && (Word_SMS(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean Krmarjenje_pogoj = Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (Krmarjenje_pogoj) 빼기(2);
            int otrok_Gradiva = 빼기(2), predmet_Gradiva = 빼기(2); if (!화면객체(otrok_Gradiva) || !화면객체(predmet_Gradiva)) return;
            if (uporabnik.화면연결(2, kopica_VALUE[predmet_Gradiva + 2], kopica_VALUE[otrok_Gradiva + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            kopica_VALUE[otrok_Gradiva + 11] = predmet_Gradiva; kopica_Gradiva[otrok_Gradiva + 11] = 1; if (!Krmarjenje_pogoj) 넣기(otrok_Gradiva, 2); return;
        }
        if (Word_SMS(ime_konstanta, "setBounds") && Word_SMS(서술상수, "(IIII)V")) {
            int višina_VALUE = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), koordinata_x = 빼기(1), predmet_Gradiva = 빼기(2); if (!화면객체(predmet_Gradiva)) return;
            if (uporabnik.화면연결(1, kopica_VALUE[predmet_Gradiva + 2], koordinata_x, 세로좌표, 너비, višina_VALUE) < 0) { 예외던짐(9, "GUI bounds"); return; }
            kopica_VALUE[predmet_Gradiva + 5] = koordinata_x; kopica_VALUE[predmet_Gradiva + 6] = 세로좌표; kopica_VALUE[predmet_Gradiva + 7] = 너비; kopica_VALUE[predmet_Gradiva + 8] = višina_VALUE; return;
        }
        if (Word_SMS(ime_konstanta, "setSize") && Word_SMS(서술상수, "(II)V")) {
            int višina_VALUE = 빼기(1), 너비 = 빼기(1), predmet_Gradiva = 빼기(2); if (!화면객체(predmet_Gradiva)) return;
            if (uporabnik.화면연결(1, kopica_VALUE[predmet_Gradiva + 2], kopica_VALUE[predmet_Gradiva + 5], kopica_VALUE[predmet_Gradiva + 6], 너비, višina_VALUE) < 0) 예외던짐(9, "GUI size"); else { kopica_VALUE[predmet_Gradiva + 7] = 너비; kopica_VALUE[predmet_Gradiva + 8] = višina_VALUE; } return;
        }
        if (Word_SMS(ime_konstanta, "setLocationRelativeTo") && Word_SMS(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), predmet_Gradiva = 빼기(2); if (!화면객체(predmet_Gradiva)) return; if (상대배치 != 0) { napaka_VALUE("only screen centering supported"); return; } kopica_VALUE[predmet_Gradiva + 5] = (uporabnik.화면너비() - kopica_VALUE[predmet_Gradiva + 7]) / 2; kopica_VALUE[predmet_Gradiva + 6] = (uporabnik.화면높이() - kopica_VALUE[predmet_Gradiva + 8]) / 2; uporabnik.화면연결(1, kopica_VALUE[predmet_Gradiva + 2], kopica_VALUE[predmet_Gradiva + 5], kopica_VALUE[predmet_Gradiva + 6], kopica_VALUE[predmet_Gradiva + 7], kopica_VALUE[predmet_Gradiva + 8]); return; }
        if (Word_SMS(ime_konstanta, "setDefaultCloseOperation") && Word_SMS(서술상수, "(I)V")) { int pravilnik = 빼기(1), predmet_Gradiva = 빼기(2); if (화면객체(predmet_Gradiva)) { if (pravilnik < 0 || pravilnik > 3) 예외던짐(9, "close policy"); else { kopica_VALUE[predmet_Gradiva + 10] = pravilnik; uporabnik.화면연결(7, kopica_VALUE[predmet_Gradiva + 2], pravilnik, 0, 0, 0); } } return; }
        if (Word_SMS(ime_konstanta, "setVisible") && Word_SMS(서술상수, "(Z)V")) { int podatki_VALUE = 빼기(1), predmet_Gradiva = 빼기(2); if (화면객체(predmet_Gradiva)) { int 처리값 = uporabnik.화면연결(3, kopica_VALUE[predmet_Gradiva + 2], podatki_VALUE, 0, 0, 0); if (처리값 < 0) napaka_VALUE("Swing requires a standalone interactive command"); else kopica_VALUE[predmet_Gradiva + 9] = podatki_VALUE; } return; }
        if (Word_SMS(ime_konstanta, "dispose") && Word_SMS(서술상수, "()V")) { int predmet_Gradiva = 빼기(2); if (화면객체(predmet_Gradiva)) { uporabnik.화면연결(4, kopica_VALUE[predmet_Gradiva + 2], 0, 0, 0, 0); kopica_VALUE[predmet_Gradiva + 9] = 0; } return; }
        if (Word_SMS(ime_konstanta, "repaint") || Word_SMS(ime_konstanta, "validate")) { int predmet_Gradiva = 빼기(2); if (!화면객체(predmet_Gradiva) || !Word_SMS(서술상수, "()V")) return; uporabnik.화면연결(1, kopica_VALUE[predmet_Gradiva + 2], kopica_VALUE[predmet_Gradiva + 5], kopica_VALUE[predmet_Gradiva + 6], kopica_VALUE[predmet_Gradiva + 7], kopica_VALUE[predmet_Gradiva + 8]); return; }
        if (Word_SMS(ime_konstanta, "isVisible") && Word_SMS(서술상수, "()Z")) { int predmet_Gradiva = 빼기(2); if (화면객체(predmet_Gradiva)) 넣기(kopica_VALUE[predmet_Gradiva + 9], 1); return; }
        napaka_VALUE("unsupported Swing method (native subset)");
    }
    static void 사건실행(int cilj_naslov, int 사건번호, boolean slovenščina) {
        if (cilj_naslov < 1 || kopica_VALUE[cilj_naslov] < 32) { napaka_VALUE("Java event listener required"); return; }
        int Datoteka_INDEX = ime_metoda(kopica_VALUE[cilj_naslov] - 32, 사건번호 == 0 ? (slovenščina ? "Izvedi" : "run") : (slovenščina ? "sprejeti_sprejemati_prejeti_prejemati_akcija" : "actionPerformed"), 사건번호 == 0 ? "()V" : (slovenščina ? "(Lslovenščina/lastno/akcija_obvestilo;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (Datoteka_INDEX < 0) { napaka_VALUE("event callback missing"); return; }
        sprotno_nit = 0; nit_COUNT = 1; okvir_INDEX = 0; nit_stanje[0] = 1; okvir_Sklad[0] = 0; okvir_zaklepanje[0] = inicializirati_okvir[0] = 0; spremeniti_zahteva = false;
        for (int Loop_INDEX = 0; Loop_INDEX < 128; Loop_INDEX++) { lokalen_krajeven_VALUE[Loop_INDEX] = lokalen_krajeven_Tip[Loop_INDEX] = 0; }
        okvir_metoda[0] = Datoteka_INDEX; okvir_položaj[0] = metoda_Start[Datoteka_INDEX]; lokalen_krajeven_VALUE[0] = cilj_naslov; lokalen_krajeven_Tip[0] = 2;
        if (사건번호 != 0) { lokalen_krajeven_VALUE[1] = 사건번호; lokalen_krajeven_Tip[1] = 2; }
        사건중 = true; Izvedi_ukaz(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!NAPAKA) {
            if (나중수 > 0) { int cilj_naslov = 나중실행[0], slovenščina = 나중한국어[0]; for (int Loop_INDEX = 1; Loop_INDEX < 나중수; Loop_INDEX++) { 나중실행[Loop_INDEX - 1] = 나중실행[Loop_INDEX]; 나중한국어[Loop_INDEX - 1] = 나중한국어[Loop_INDEX]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; 사건실행(cilj_naslov, 0, slovenščina != 0); continue; }
            if (uporabnik.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int 사건번호 = uporabnik.화면연결(5, 0, 0, 0, 0, 0); if (사건번호 == 0) continue;
            if (사건번호 < 0) { napaka_VALUE("GUI event I/O failed"); return; }
            int račun_VALUE = 사건번호 & 65535; if (račun_VALUE < 1 || račun_VALUE > 32) continue; int predmet_Gradiva = 화면참조[račun_VALUE - 1]; if (predmet_Gradiva == 0) continue;
            if ((사건번호 & 65536) != 0) {
                if (kopica_VALUE[predmet_Gradiva + 10] != 0) kopica_VALUE[predmet_Gradiva + 9] = 0;
                if (kopica_VALUE[predmet_Gradiva + 10] == 3) for (int Loop_INDEX = 0; Loop_INDEX < 32; Loop_INDEX++) if (화면참조[Loop_INDEX] != 0 && kopica_VALUE[화면참조[Loop_INDEX]] == 24) uporabnik.화면연결(4, Loop_INDEX + 1, 0, 0, 0, 0);
            } else if (kopica_VALUE[predmet_Gradiva + 4] != 0) {
                int 안내참조 = dodeliti_Senzor_prostora(29, 2); if (NAPAKA) return; kopica_VALUE[안내참조 + 2] = predmet_Gradiva; kopica_VALUE[안내참조 + 3] = kopica_VALUE[predmet_Gradiva + 12]; kopica_Gradiva[안내참조 + 2] = 1; 사건실행(kopica_VALUE[predmet_Gradiva + 4], 안내참조, kopica_VALUE[predmet_Gradiva + 12] != 0);
            }
        }
    }
    public static int Zaženi() {
        if (uporabnik.인수개수() == 1 && 자바도구.같음(uporabnik.Argumenti(0), "-version")) {
            uporabnik.Pisanje("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (uporabnik.인수개수() < 1) { uporabnik.Pisanje("Usage: java CLASS [ARGS]\n"); return 2; }
        vnos_Razred_definicija = zbirka_Razred_definicija(gostiti_znak(uporabnik.Argumenti(0))); if (NAPAKA || vnos_Razred_definicija < 0) return 1;
        int vnos_p_VALUE = ime_metoda(vnos_Razred_definicija, "Zaženi", "()V");
        boolean 한국어진입 = vnos_p_VALUE >= 0 && (metoda_dostop[vnos_p_VALUE] & 9) == 9;
        if (!한국어진입) vnos_p_VALUE = ime_metoda(vnos_Razred_definicija, "main", "([Ljava/lang/String;)V");
        if (vnos_p_VALUE < 0 || (metoda_dostop[vnos_p_VALUE] & 9) != 9) napaka_VALUE("public static void Zaženi() or main(String[] args) required");
        if (NAPAKA) return 1;
        int Argumenti = dodeliti_Senzor_prostora(3, uporabnik.인수개수() - 1); element_polja[Argumenti] = -1;
        for (int 수 = 1; 수 < uporabnik.인수개수() && !NAPAKA; 수++) kopica_VALUE[Argumenti + 1 + 수] = gostiti_znak(uporabnik.Argumenti(수));
        okvir_INDEX = 0; okvir_metoda[0] = vnos_p_VALUE; okvir_položaj[0] = metoda_Start[vnos_p_VALUE]; lokalen_krajeven_VALUE[0] = 한국어진입 ? 0 : Argumenti; lokalen_krajeven_Tip[0] = 한국어진입 ? 0 : 2;
        nit_stanje[0] = 1; nit_predmet[0] = dodeliti_Senzor_prostora(13, 2);
        Izvedi_ukaz(); if (!NAPAKA) 화면사건들(); return NAPAKA ? 1 : 0;
    }
}
