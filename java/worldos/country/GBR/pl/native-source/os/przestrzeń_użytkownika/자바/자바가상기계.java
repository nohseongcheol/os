// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. nazwa_pliku/operand_Stos/odwołanie/gałąź_22e01337 경계를 Wykonaj_polecenie 중 검사한다. */
public final class 자바가상기계 {
    static int[] nazwa_pliku = new int[16384], nazwa_pliku_SMS = new int[64];
    static int[] stała_tag = new int[512], 상가 = new int[512], stała_SEKUNDA_WARTOŚĆ = new int[512], ciąg_odwołanie = new int[512];
    static int[] metoda_nazwa_SMS = new int[32], metoda_TYP = new int[32], metoda_dostęp = new int[32];
    static int[] metoda_START = new int[32], metoda_Koniec = new int[32], metoda_Stos = new int[32], 함수지역 = new int[32];
    static int[] metoda_argument_ILE_LICZB = new int[32], metoda_argument_TYP = new int[512], metoda_Zwrot = new int[32];
    static int[] granica_WARTOŚĆ = new int[16384];
    static int[] lokalny_WARTOŚĆ = new int[4096], lokalny_TYP = new int[4096], operand_Stos_WARTOŚĆ = new int[4096], operand_Stos_TYP = new int[4096];
    static int[] kadr_metoda = new int[32], kadr_stanowisko = new int[32], kadr_Stos = new int[32];
    static int[] sterta_WARTOŚĆ = new int[8192];
    static int Rozmiar, 읽기위치, stała_ILE_LICZB, metoda_ILE_LICZB, nazwa_klasy, kadr_INDEKS = -1, sterta_Koniec_stanowisko = 1, zwracany_typ;
    static boolean błąd;

    static void awaria_WARTOŚĆ(String Word_SMS) {
        if (!błąd) { przestrzeń_użytkownika.Zapis("JVM error: "); przestrzeń_użytkownika.Zapis(Word_SMS); przestrzeń_użytkownika.zapis_znak_WARTOŚĆ(10); }
        błąd = true;
    }
    static boolean obcinać(int Uruchom_2, int długość_WARTOŚĆ) { return Uruchom_2 >= 0 && długość_WARTOŚĆ >= 0 && Uruchom_2 <= Rozmiar - długość_WARTOŚĆ; }
    static int bajt_WARTOŚĆ() {
        if (!obcinać(읽기위치, 1)) { awaria_WARTOŚĆ("truncated class file"); return 0; }
        return nazwa_pliku[읽기위치++];
    }
    static int 짧은수() { return bajt_WARTOŚĆ() << 8 | bajt_WARTOŚĆ(); }
    static int liczba_całkowita() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int długość_WARTOŚĆ) { if (!obcinać(읽기위치, długość_WARTOŚĆ)) awaria_WARTOŚĆ("invalid attribute size"); else 읽기위치 += długość_WARTOŚĆ; }
    static boolean czek_stała(int identyfikator, int Rodzaj_WARTOŚĆ) {
        if (identyfikator <= 0 || identyfikator >= stała_ILE_LICZB || stała_tag[identyfikator] != Rodzaj_WARTOŚĆ) { awaria_WARTOŚĆ("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean SMS_zakres(int Uruchom_2, int długość_WARTOŚĆ, String Word_SMS) {
        if (!obcinać(Uruchom_2, długość_WARTOŚĆ) || długość_WARTOŚĆ != Word_SMS.length()) return false;
        for (int identyfikator = 0; identyfikator < długość_WARTOŚĆ; identyfikator++) if (nazwa_pliku[Uruchom_2 + identyfikator] != Word_SMS.charAt(identyfikator)) return false;
        return true;
    }
    static boolean Word_SMS(int stała_WARTOŚĆ, String Word_SMS) { return czek_stała(stała_WARTOŚĆ, 1) && SMS_zakres(상가[stała_WARTOŚĆ], stała_SEKUNDA_WARTOŚĆ[stała_WARTOŚĆ], Word_SMS); }
    static boolean 같은말(int 가, int SEKUNDA_operand) {
        if (!czek_stała(가, 1) || !czek_stała(SEKUNDA_operand, 1) || stała_SEKUNDA_WARTOŚĆ[가] != stała_SEKUNDA_WARTOŚĆ[SEKUNDA_operand]) return false;
        for (int identyfikator = 0; identyfikator < stała_SEKUNDA_WARTOŚĆ[가]; identyfikator++) if (nazwa_pliku[상가[가] + identyfikator] != nazwa_pliku[상가[SEKUNDA_operand] + identyfikator]) return false;
        return true;
    }
    static int nazwa_klasy_SMS(int identyfikator) { return czek_stała(identyfikator, 7) && czek_stała(상가[identyfikator], 1) ? 상가[identyfikator] : 0; }
    static int odwołanie_nazwa(int identyfikator) { return czek_stała(identyfikator, 12) && czek_stała(상가[identyfikator], 1) ? 상가[identyfikator] : 0; }
    static int typ_referencyjny(int identyfikator) { return czek_stała(identyfikator, 12) && czek_stała(stała_SEKUNDA_WARTOŚĆ[identyfikator], 1) ? stała_SEKUNDA_WARTOŚĆ[identyfikator] : 0; }
    static int deskryptor_TYP(int 끝, boolean 빈형) {
        if (읽기위치 >= 끝) { awaria_WARTOŚĆ("invalid descriptor"); return 0; }
        int WARTOŚĆ = bajt_WARTOŚĆ();
        if (WARTOŚĆ == 'V' && 빈형) return 0;
        if (WARTOŚĆ == 'I' || WARTOŚĆ == 'B' || WARTOŚĆ == 'C' || WARTOŚĆ == 'S' || WARTOŚĆ == 'Z') return 1;
        if (WARTOŚĆ == '[') { deskryptor_TYP(끝, false); return 2; }
        if (WARTOŚĆ == 'L') {
            int Uruchom_2 = 읽기위치;
            while (읽기위치 < 끝 && nazwa_pliku[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == Uruchom_2) awaria_WARTOŚĆ("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        awaria_WARTOŚĆ("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int FUNKCJA_WARTOŚĆ) {
        int Wstecz_towar = 읽기위치, identyfikator = metoda_TYP[FUNKCJA_WARTOŚĆ];
        if (!czek_stała(identyfikator, 1)) return;
        읽기위치 = 상가[identyfikator]; int 끝 = 읽기위치 + stała_SEKUNDA_WARTOŚĆ[identyfikator];
        if (bajt_WARTOŚĆ() != '(') awaria_WARTOŚĆ("invalid method descriptor");
        int towar_ILE_LICZB = 0;
        while (!błąd && 읽기위치 < 끝 && nazwa_pliku[읽기위치] != ')') {
            if (towar_ILE_LICZB == 16) { awaria_WARTOŚĆ("too many method arguments"); break; }
            metoda_argument_TYP[FUNKCJA_WARTOŚĆ * 16 + towar_ILE_LICZB++] = deskryptor_TYP(끝, false);
        }
        if (읽기위치 >= 끝 || bajt_WARTOŚĆ() != ')') awaria_WARTOŚĆ("invalid method descriptor");
        metoda_Zwrot[FUNKCJA_WARTOŚĆ] = deskryptor_TYP(끝, true); metoda_argument_ILE_LICZB[FUNKCJA_WARTOŚĆ] = towar_ILE_LICZB;
        if (읽기위치 != 끝) awaria_WARTOŚĆ("invalid method descriptor");
        읽기위치 = Wstecz_towar;
    }
    static void pominąć_atrybut() {
        int towar_ILE_LICZB = 짧은수();
        for (int identyfikator = 0; identyfikator < towar_ILE_LICZB && !błąd; identyfikator++) { czek_stała(짧은수(), 1); 건너(liczba_całkowita()); }
    }
    static int polecenie_długość(int WARTOŚĆ) {
        if (WARTOŚĆ == 16 || WARTOŚĆ == 18 || WARTOŚĆ == 21 || WARTOŚĆ == 25 || WARTOŚĆ == 54 || WARTOŚĆ == 58 || WARTOŚĆ == 188) return 2;
        if (WARTOŚĆ == 17 || WARTOŚĆ == 19 || WARTOŚĆ == 132 || WARTOŚĆ >= 153 && WARTOŚĆ <= 167
            || WARTOŚĆ >= 178 && WARTOŚĆ <= 184 || WARTOŚĆ == 187 || WARTOŚĆ == 189 || WARTOŚĆ == 192 || WARTOŚĆ == 198 || WARTOŚĆ == 199) return 3;
        if (WARTOŚĆ >= 0 && WARTOŚĆ <= 8 || WARTOŚĆ >= 26 && WARTOŚĆ <= 29 || WARTOŚĆ >= 42 && WARTOŚĆ <= 46 || WARTOŚĆ == 50
            || WARTOŚĆ >= 59 && WARTOŚĆ <= 62 || WARTOŚĆ >= 75 && WARTOŚĆ <= 79 || WARTOŚĆ == 83 || WARTOŚĆ == 87 || WARTOŚĆ == 89 || WARTOŚĆ == 95
            || WARTOŚĆ == 96 || WARTOŚĆ == 100 || WARTOŚĆ == 104 || WARTOŚĆ == 108 || WARTOŚĆ == 112 || WARTOŚĆ == 116
            || WARTOŚĆ == 120 || WARTOŚĆ == 122 || WARTOŚĆ == 124 || WARTOŚĆ == 126 || WARTOŚĆ == 128 || WARTOŚĆ == 130
            || WARTOŚĆ >= 145 && WARTOŚĆ <= 147 || WARTOŚĆ == 172 || WARTOŚĆ == 176 || WARTOŚĆ == 177 || WARTOŚĆ == 190) return 1;
        return 0;
    }
    static void 클래스읽기() {
        if (liczba_całkowita() != 0xcafebabe) awaria_WARTOŚĆ("not a class file");
        int 부판 = 짧은수(), wersja_WARTOŚĆ = 짧은수();
        if (wersja_WARTOŚĆ < 45 || wersja_WARTOŚĆ > 52 || 부판 != 0) awaria_WARTOŚĆ("supported class versions: 45..52, minor 0");
        stała_ILE_LICZB = 짧은수();
        if (stała_ILE_LICZB < 1 || stała_ILE_LICZB > 512) { awaria_WARTOŚĆ("constant pool limit (511)"); return; }
        for (int identyfikator = 1; identyfikator < stała_ILE_LICZB && !błąd; identyfikator++) {
            int Rodzaj_WARTOŚĆ = bajt_WARTOŚĆ(); stała_tag[identyfikator] = Rodzaj_WARTOŚĆ;
            if (Rodzaj_WARTOŚĆ == 1) { stała_SEKUNDA_WARTOŚĆ[identyfikator] = 짧은수(); 상가[identyfikator] = 읽기위치; 건너(stała_SEKUNDA_WARTOŚĆ[identyfikator]); }
            else if (Rodzaj_WARTOŚĆ == 3) 상가[identyfikator] = liczba_całkowita();
            else if (Rodzaj_WARTOŚĆ == 7 || Rodzaj_WARTOŚĆ == 8) 상가[identyfikator] = 짧은수();
            else if (Rodzaj_WARTOŚĆ == 9 || Rodzaj_WARTOŚĆ == 10 || Rodzaj_WARTOŚĆ == 12) { 상가[identyfikator] = 짧은수(); stała_SEKUNDA_WARTOŚĆ[identyfikator] = 짧은수(); }
            else awaria_WARTOŚĆ("unsupported constant type");
        }
        int pozwolenie_WARTOŚĆ = 짧은수();
        if ((pozwolenie_WARTOŚĆ & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) awaria_WARTOŚĆ("unsupported class flags");
        nazwa_klasy = nazwa_klasy_SMS(짧은수());
        if (!Word_SMS(nazwa_klasy_SMS(짧은수()), "java/lang/Object")) awaria_WARTOŚĆ("inheritance unsupported");
        if (짧은수() != 0) awaria_WARTOŚĆ("interfaces unsupported");
        if (짧은수() != 0) awaria_WARTOŚĆ("fields unsupported");
        metoda_ILE_LICZB = 짧은수();
        if (metoda_ILE_LICZB < 1 || metoda_ILE_LICZB > 32) { awaria_WARTOŚĆ("method count limit (32)"); return; }
        for (int identyfikator = 0; identyfikator < metoda_ILE_LICZB && !błąd; identyfikator++) {
            metoda_dostęp[identyfikator] = 짧은수(); metoda_nazwa_SMS[identyfikator] = 짧은수(); metoda_TYP[identyfikator] = 짧은수();
            czek_stała(metoda_nazwa_SMS[identyfikator], 1); 서술읽기(identyfikator);
            if ((metoda_dostęp[identyfikator] & (0x100 | 0x400 | 0x20)) != 0) awaria_WARTOŚĆ("native, abstract and synchronized methods unsupported");
            if ((metoda_dostęp[identyfikator] & 8) == 0 && !Word_SMS(metoda_nazwa_SMS[identyfikator], "<init>")) awaria_WARTOŚĆ("instance methods unsupported");
            if (Word_SMS(metoda_nazwa_SMS[identyfikator], "<clinit>")) awaria_WARTOŚĆ("class initializers unsupported");
            for (int przód_WARTOŚĆ = 0; przód_WARTOŚĆ < identyfikator; przód_WARTOŚĆ++) if (같은말(metoda_nazwa_SMS[przód_WARTOŚĆ], metoda_nazwa_SMS[identyfikator]) && 같은말(metoda_TYP[przód_WARTOŚĆ], metoda_TYP[identyfikator])) awaria_WARTOŚĆ("duplicate method");
            int towar_ILE_LICZB = 짧은수();
            for (int wartość_atrybutu = 0; wartość_atrybutu < towar_ILE_LICZB && !błąd; wartość_atrybutu++) {
                int Nazwa = 짧은수(), długość_WARTOŚĆ = liczba_całkowita(), Uruchom_2 = 읽기위치;
                if (!obcinać(Uruchom_2, długość_WARTOŚĆ)) { awaria_WARTOŚĆ("truncated method attribute"); break; }
                if (Word_SMS(Nazwa, "Code")) {
                    if (metoda_START[identyfikator] != 0) awaria_WARTOŚĆ("duplicate Code attribute");
                    metoda_Stos[identyfikator] = 짧은수(); 함수지역[identyfikator] = 짧은수(); int KOD_długość = liczba_całkowita();
                    if (metoda_Stos[identyfikator] > 128 || 함수지역[identyfikator] > 128 || 함수지역[identyfikator] < metoda_argument_ILE_LICZB[identyfikator]
                        || KOD_długość < 1 || KOD_długość > 8192) awaria_WARTOŚĆ("method memory limits exceeded");
                    metoda_START[identyfikator] = 읽기위치; 건너(KOD_długość); metoda_Koniec[identyfikator] = 읽기위치;
                    if (짧은수() != 0) awaria_WARTOŚĆ("exception handlers unsupported");
                    pominąć_atrybut();
                    if (읽기위치 != Uruchom_2 + długość_WARTOŚĆ) awaria_WARTOŚĆ("Code attribute size mismatch");
                } else 건너(długość_WARTOŚĆ);
            }
            if (metoda_START[identyfikator] == 0) awaria_WARTOŚĆ("missing Code attribute");
            int gniazdo_wpis = metoda_START[identyfikator];
            while (gniazdo_wpis < metoda_Koniec[identyfikator] && !błąd) {
                int długość_WARTOŚĆ = polecenie_długość(nazwa_pliku[gniazdo_wpis]);
                if (długość_WARTOŚĆ == 0 || długość_WARTOŚĆ > metoda_Koniec[identyfikator] - gniazdo_wpis) { awaria_WARTOŚĆ("unsupported or truncated bytecode"); break; }
                granica_WARTOŚĆ[gniazdo_wpis] = identyfikator + 1; gniazdo_wpis += długość_WARTOŚĆ;
            }
            // 실행하지 않는 경로에도 잘못된 gałąź_22e01337 목적지를 허용하지 않는다.
            gniazdo_wpis = metoda_START[identyfikator];
            while (gniazdo_wpis < metoda_Koniec[identyfikator] && !błąd) {
                int WARTOŚĆ = nazwa_pliku[gniazdo_wpis];
                if (WARTOŚĆ >= 153 && WARTOŚĆ <= 167 || WARTOŚĆ == 198 || WARTOŚĆ == 199) {
                    int cel_WARTOŚĆ = gniazdo_wpis + (short)(nazwa_pliku[gniazdo_wpis + 1] << 8 | nazwa_pliku[gniazdo_wpis + 2]);
                    if (cel_WARTOŚĆ < metoda_START[identyfikator] || cel_WARTOŚĆ >= metoda_Koniec[identyfikator] || granica_WARTOŚĆ[cel_WARTOŚĆ] != identyfikator + 1) awaria_WARTOŚĆ("invalid branch target");
                }
                gniazdo_wpis += polecenie_długość(WARTOŚĆ);
            }
        }
        if (!błąd) pominąć_atrybut();
        if (읽기위치 != Rozmiar) awaria_WARTOŚĆ("extra class file data");
    }
    static int przydzielić_Pamięć(int Rodzaj_WARTOŚĆ, int długość_WARTOŚĆ) {
        if (długość_WARTOŚĆ < 0 || długość_WARTOŚĆ > sterta_WARTOŚĆ.length - sterta_Koniec_stanowisko - 2) { awaria_WARTOŚĆ("object heap exhausted or negative array size"); return 0; }
        int odwołanie = sterta_Koniec_stanowisko; sterta_Koniec_stanowisko += długość_WARTOŚĆ + 2; sterta_WARTOŚĆ[odwołanie] = Rodzaj_WARTOŚĆ; sterta_WARTOŚĆ[odwołanie + 1] = długość_WARTOŚĆ;
        return odwołanie;
    }
    static boolean obiekt_WARTOŚĆ(int odwołanie, int Rodzaj_WARTOŚĆ) {
        if (odwołanie < 1 || odwołanie >= sterta_Koniec_stanowisko - 1 || sterta_WARTOŚĆ[odwołanie] != Rodzaj_WARTOŚĆ) { awaria_WARTOŚĆ("null or invalid object reference"); return false; }
        return true;
    }
    static int stała_SMS(int INDEKS) {
        if (!czek_stała(INDEKS, 1)) return 0;
        if (ciąg_odwołanie[INDEKS] != 0) return ciąg_odwołanie[INDEKS];
        int odwołanie = przydzielić_Pamięć(1, stała_SEKUNDA_WARTOŚĆ[INDEKS]); if (błąd) return 0;
        int 끝 = 상가[INDEKS] + stała_SEKUNDA_WARTOŚĆ[INDEKS], identyfikator = 상가[INDEKS], długość_WARTOŚĆ = 0;
        while (identyfikator < 끝 && !błąd) {
            int WARTOŚĆ = nazwa_pliku[identyfikator++];
            if (WARTOŚĆ == 0) awaria_WARTOŚĆ("invalid modified UTF-8");
            else if (WARTOŚĆ >= 192 && WARTOŚĆ <= 223 && identyfikator < 끝) {
                int Dalej_towar = nazwa_pliku[identyfikator++];
                if ((Dalej_towar & 192) != 128) awaria_WARTOŚĆ("invalid modified UTF-8");
                WARTOŚĆ = (WARTOŚĆ & 31) << 6 | Dalej_towar & 63;
                if (WARTOŚĆ != 0 && WARTOŚĆ < 128) awaria_WARTOŚĆ("overlong modified UTF-8");
            } else if (WARTOŚĆ >= 224 && WARTOŚĆ <= 239 && identyfikator + 1 < 끝) {
                int 가 = nazwa_pliku[identyfikator++], SEKUNDA_operand = nazwa_pliku[identyfikator++];
                if ((가 & 192) != 128 || (SEKUNDA_operand & 192) != 128) awaria_WARTOŚĆ("invalid modified UTF-8");
                WARTOŚĆ = (WARTOŚĆ & 15) << 12 | (가 & 63) << 6 | SEKUNDA_operand & 63;
                if (WARTOŚĆ < 2048) awaria_WARTOŚĆ("overlong modified UTF-8");
            } else if (WARTOŚĆ >= 128) awaria_WARTOŚĆ("invalid modified UTF-8");
            sterta_WARTOŚĆ[odwołanie + 2 + długość_WARTOŚĆ++] = WARTOŚĆ;
        }
        sterta_WARTOŚĆ[odwołanie + 1] = długość_WARTOŚĆ; ciąg_odwołanie[INDEKS] = odwołanie; return odwołanie;
    }
    static int host_znak(String WARTOŚĆ) {
        int odwołanie = przydzielić_Pamięć(1, WARTOŚĆ.length()); if (błąd) return 0;
        for (int identyfikator = 0; identyfikator < WARTOŚĆ.length(); identyfikator++) sterta_WARTOŚĆ[odwołanie + 2 + identyfikator] = WARTOŚĆ.charAt(identyfikator);
        return odwołanie;
    }
    static void zapis_SMS(int odwołanie) {
        if (odwołanie == 0) { przestrzeń_użytkownika.Zapis("null"); return; }
        if (!obiekt_WARTOŚĆ(odwołanie, 1)) return;
        for (int identyfikator = 0; identyfikator < sterta_WARTOŚĆ[odwołanie + 1]; identyfikator++) przestrzeń_użytkownika.zapis_znak_WARTOŚĆ(sterta_WARTOŚĆ[odwołanie + 2 + identyfikator]);
    }
    static int cyfra_znak(int WARTOŚĆ) {
        int odwołanie = przydzielić_Pamięć(1, 11); if (błąd) return 0;
        int długość_WARTOŚĆ = 0;
        if (WARTOŚĆ < 0) sterta_WARTOŚĆ[odwołanie + 2 + długość_WARTOŚĆ++] = '-'; else WARTOŚĆ = -WARTOŚĆ;
        int indeks_pozycji = 1000000000; boolean Uruchom_2 = false;
        while (indeks_pozycji != 0) {
            int identyfikator = -(WARTOŚĆ / indeks_pozycji);
            if (identyfikator != 0 || Uruchom_2 || indeks_pozycji == 1) { sterta_WARTOŚĆ[odwołanie + 2 + długość_WARTOŚĆ++] = '0' + identyfikator; Uruchom_2 = true; }
            WARTOŚĆ %= indeks_pozycji; indeks_pozycji /= 10;
        }
        sterta_WARTOŚĆ[odwołanie + 1] = długość_WARTOŚĆ; return odwołanie;
    }
    static int 정수해독(int odwołanie) {
        if (!obiekt_WARTOŚĆ(odwołanie, 1)) return 0;
        int długość_WARTOŚĆ = sterta_WARTOŚĆ[odwołanie + 1], identyfikator = 0, WARTOŚĆ = 0; boolean negatywny_WARTOŚĆ = false;
        if (długość_WARTOŚĆ > 0 && (sterta_WARTOŚĆ[odwołanie + 2] == '-' || sterta_WARTOŚĆ[odwołanie + 2] == '+')) { negatywny_WARTOŚĆ = sterta_WARTOŚĆ[odwołanie + 2] == '-'; identyfikator++; }
        if (identyfikator == długość_WARTOŚĆ) awaria_WARTOŚĆ("NumberFormatException");
        for (; identyfikator < długość_WARTOŚĆ && !błąd; identyfikator++) {
            int cyfra_WARTOŚĆ = sterta_WARTOŚĆ[odwołanie + 2 + identyfikator] - '0';
            if (cyfra_WARTOŚĆ < 0 || cyfra_WARTOŚĆ > 9 || WARTOŚĆ < -214748364 || WARTOŚĆ == -214748364 && cyfra_WARTOŚĆ > (negatywny_WARTOŚĆ ? 8 : 7)) awaria_WARTOŚĆ("NumberFormatException");
            WARTOŚĆ = WARTOŚĆ * 10 - cyfra_WARTOŚĆ;
        }
        return negatywny_WARTOŚĆ ? WARTOŚĆ : -WARTOŚĆ;
    }
    static void 넣기(int WARTOŚĆ, int TYP_WARTOŚĆ) {
        if (błąd) return;
        if (kadr_INDEKS < 0 || kadr_Stos[kadr_INDEKS] >= metoda_Stos[kadr_metoda[kadr_INDEKS]]) { awaria_WARTOŚĆ("operand stack overflow"); return; }
        int gniazdo_wpis = kadr_INDEKS * 128 + kadr_Stos[kadr_INDEKS]++; operand_Stos_WARTOŚĆ[gniazdo_wpis] = WARTOŚĆ; operand_Stos_TYP[gniazdo_wpis] = TYP_WARTOŚĆ;
    }
    static int 빼기(int TYP_WARTOŚĆ) {
        if (błąd) return 0;
        if (kadr_INDEKS < 0 || kadr_Stos[kadr_INDEKS] < 1) { awaria_WARTOŚĆ("operand stack underflow"); return 0; }
        int gniazdo_wpis = kadr_INDEKS * 128 + --kadr_Stos[kadr_INDEKS]; zwracany_typ = operand_Stos_TYP[gniazdo_wpis];
        if (TYP_WARTOŚĆ != 0 && zwracany_typ != TYP_WARTOŚĆ) awaria_WARTOŚĆ("operand type mismatch");
        return operand_Stos_WARTOŚĆ[gniazdo_wpis];
    }
    static void 지역읽기(int INDEKS, int TYP_WARTOŚĆ) {
        if (INDEKS >= 함수지역[kadr_metoda[kadr_INDEKS]] || INDEKS < 0 || lokalny_TYP[kadr_INDEKS * 128 + INDEKS] != TYP_WARTOŚĆ) { awaria_WARTOŚĆ("invalid or uninitialized local"); return; }
        넣기(lokalny_WARTOŚĆ[kadr_INDEKS * 128 + INDEKS], TYP_WARTOŚĆ);
    }
    static void zapis_lokalny(int INDEKS, int TYP_WARTOŚĆ) {
        if (INDEKS >= 함수지역[kadr_metoda[kadr_INDEKS]] || INDEKS < 0) { awaria_WARTOŚĆ("local index out of range"); return; }
        int WARTOŚĆ = 빼기(TYP_WARTOŚĆ); lokalny_WARTOŚĆ[kadr_INDEKS * 128 + INDEKS] = WARTOŚĆ; lokalny_TYP[kadr_INDEKS * 128 + INDEKS] = TYP_WARTOŚĆ;
    }
    static int 명바() {
        int pozycja = kadr_stanowisko[kadr_INDEKS];
        if (pozycja < metoda_START[kadr_metoda[kadr_INDEKS]] || pozycja >= metoda_Koniec[kadr_metoda[kadr_INDEKS]]) { awaria_WARTOŚĆ("instruction pointer out of range"); return 0; }
        kadr_stanowisko[kadr_INDEKS]++; return nazwa_pliku[pozycja];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void przenosić_WARTOŚĆ(int pozycja) {
        int FUNKCJA_WARTOŚĆ = kadr_metoda[kadr_INDEKS];
        if (pozycja < metoda_START[FUNKCJA_WARTOŚĆ] || pozycja >= metoda_Koniec[FUNKCJA_WARTOŚĆ] || granica_WARTOŚĆ[pozycja] != FUNKCJA_WARTOŚĆ + 1) awaria_WARTOŚĆ("invalid branch target");
        else kadr_stanowisko[kadr_INDEKS] = pozycja;
    }
    static void 호출(int FUNKCJA_WARTOŚĆ) {
        if (kadr_INDEKS == 31) { awaria_WARTOŚĆ("call stack limit (32)"); return; }
        int Dalej_towar = kadr_INDEKS + 1;
        for (int identyfikator = 0; identyfikator < 128; identyfikator++) lokalny_TYP[Dalej_towar * 128 + identyfikator] = 0;
        for (int identyfikator = metoda_argument_ILE_LICZB[FUNKCJA_WARTOŚĆ] - 1; identyfikator >= 0; identyfikator--) {
            lokalny_WARTOŚĆ[Dalej_towar * 128 + identyfikator] = 빼기(metoda_argument_TYP[FUNKCJA_WARTOŚĆ * 16 + identyfikator]); lokalny_TYP[Dalej_towar * 128 + identyfikator] = metoda_argument_TYP[FUNKCJA_WARTOŚĆ * 16 + identyfikator];
        }
        kadr_INDEKS = Dalej_towar; kadr_metoda[kadr_INDEKS] = FUNKCJA_WARTOŚĆ; kadr_stanowisko[kadr_INDEKS] = metoda_START[FUNKCJA_WARTOŚĆ]; kadr_Stos[kadr_INDEKS] = 0;
    }
    static void Zwrot_KR(int TYP_WARTOŚĆ) {
        if (TYP_WARTOŚĆ != metoda_Zwrot[kadr_metoda[kadr_INDEKS]]) { awaria_WARTOŚĆ("return type mismatch"); return; }
        int WARTOŚĆ = TYP_WARTOŚĆ == 0 ? 0 : 빼기(TYP_WARTOŚĆ);
        kadr_INDEKS--; if (kadr_INDEKS >= 0 && TYP_WARTOŚĆ != 0) 넣기(WARTOŚĆ, TYP_WARTOŚĆ);
    }
    static int[] Stream_nazwa_pliku = new int[64];
    static void Plik_Stream_Połącz(int właściciel_WARTOŚĆ, int Nazwa, int format_WARTOŚĆ, int polecenie) {
        boolean pozycja_wyjścia = Word_SMS(właściciel_WARTOŚĆ, "java/io/FileOutputStream");
        int Rodzaj_WARTOŚĆ = pozycja_wyjścia ? 6 : 5;
        if (polecenie == 183 && Word_SMS(Nazwa, "<init>")) {
            boolean 이어 = false;
            if (pozycja_wyjścia && Word_SMS(format_WARTOŚĆ, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Word_SMS(format_WARTOŚĆ, "(Ljava/lang/String;)V")) { awaria_WARTOŚĆ("unsupported file stream constructor"); return; }
            int Plik_wpis_nazwa = 빼기(2), Stream_WARTOŚĆ = 빼기(2);
            if (!obiekt_WARTOŚĆ(Plik_wpis_nazwa, 1) || !obiekt_WARTOŚĆ(Stream_WARTOŚĆ, Rodzaj_WARTOŚĆ) || błąd) return;
            if (sterta_WARTOŚĆ[Stream_WARTOŚĆ + 3] != 0) { awaria_WARTOŚĆ("file stream already initialized"); return; }
            int długość_WARTOŚĆ = sterta_WARTOŚĆ[Plik_wpis_nazwa + 1];
            if (długość_WARTOŚĆ < 1 || długość_WARTOŚĆ > 63) { awaria_WARTOŚĆ("invalid file name length"); return; }
            for (int gniazdo_wpis = 0; gniazdo_wpis < długość_WARTOŚĆ; gniazdo_wpis++) {
                int WARTOŚĆ = sterta_WARTOŚĆ[Plik_wpis_nazwa + 2 + gniazdo_wpis];
                if (WARTOŚĆ < 1 || WARTOŚĆ > 127) { awaria_WARTOŚĆ("file stream paths currently require ASCII"); return; }
                Stream_nazwa_pliku[gniazdo_wpis] = WARTOŚĆ;
            }
            Stream_nazwa_pliku[długość_WARTOŚĆ] = 0;
            int deskryptor_wpis = przestrzeń_użytkownika.otwarty_Plik_deskryptor(Stream_nazwa_pliku, pozycja_wyjścia ? (이어 ? 1089 : 577) : 0);
            if (deskryptor_wpis < 0) { awaria_WARTOŚĆ("FileNotFoundException: file open failed"); return; }
            sterta_WARTOŚĆ[Stream_WARTOŚĆ + 2] = deskryptor_wpis; sterta_WARTOŚĆ[Stream_WARTOŚĆ + 3] = 1;
            return;
        }
        if (polecenie != 182) { awaria_WARTOŚĆ("invalid file stream invocation"); return; }
        int Akcja = -1, WARTOŚĆ = 0;
        if (Word_SMS(Nazwa, "close") && Word_SMS(format_WARTOŚĆ, "()V")) Akcja = 0;
        if (!pozycja_wyjścia && Word_SMS(Nazwa, "read") && Word_SMS(format_WARTOŚĆ, "()I")) Akcja = 1;
        if (pozycja_wyjścia && Word_SMS(Nazwa, "write") && Word_SMS(format_WARTOŚĆ, "(I)V")) { Akcja = 2; WARTOŚĆ = 빼기(1); }
        if (Akcja < 0) { awaria_WARTOŚĆ("unsupported file stream method"); return; }
        int Stream_WARTOŚĆ = 빼기(2);
        if (!obiekt_WARTOŚĆ(Stream_WARTOŚĆ, Rodzaj_WARTOŚĆ) || błąd) return;
        if (sterta_WARTOŚĆ[Stream_WARTOŚĆ + 3] == 0) { awaria_WARTOŚĆ("uninitialized file stream"); return; }
        int deskryptor_wpis = sterta_WARTOŚĆ[Stream_WARTOŚĆ + 2];
        if (Akcja == 0) {
            if (deskryptor_wpis >= 0 && przestrzeń_użytkownika.Zamknij_Plik_deskryptor(deskryptor_wpis) < 0) awaria_WARTOŚĆ("IOException: close failed");
            sterta_WARTOŚĆ[Stream_WARTOŚĆ + 2] = -1; return;
        }
        if (deskryptor_wpis < 0) { awaria_WARTOŚĆ("IOException: stream closed"); return; }
        if (Akcja == 1) {
            int WYNIK = przestrzeń_użytkownika.파일한바이트읽기(deskryptor_wpis);
            if (WYNIK < -1) awaria_WARTOŚĆ("IOException: read failed"); else 넣기(WYNIK, 1);
        } else if (przestrzeń_użytkownika.파일한바이트쓰기(deskryptor_wpis, WARTOŚĆ) != 1) awaria_WARTOŚĆ("IOException: write failed");
    }
    static void Połącz_metoda(int INDEKS, int polecenie) {
        if (!czek_stała(INDEKS, 10)) return;
        int właściciel_WARTOŚĆ = nazwa_klasy_SMS(상가[INDEKS]), Nazwa = odwołanie_nazwa(stała_SEKUNDA_WARTOŚĆ[INDEKS]), format_WARTOŚĆ = typ_referencyjny(stała_SEKUNDA_WARTOŚĆ[INDEKS]);
        if (błąd) return;
        if (같은말(właściciel_WARTOŚĆ, nazwa_klasy)) {
            if (polecenie != 184) { awaria_WARTOŚĆ("only static user methods are supported"); return; }
            for (int identyfikator = 0; identyfikator < metoda_ILE_LICZB; identyfikator++) if (같은말(Nazwa, metoda_nazwa_SMS[identyfikator]) && 같은말(format_WARTOŚĆ, metoda_TYP[identyfikator])) {
                if ((metoda_dostęp[identyfikator] & 8) == 0) awaria_WARTOŚĆ("method is not static"); else 호출(identyfikator);
                return;
            }
            awaria_WARTOŚĆ("NoSuchMethodError"); return;
        }
        if (Word_SMS(właściciel_WARTOŚĆ, "java/io/FileInputStream") || Word_SMS(właściciel_WARTOŚĆ, "java/io/FileOutputStream")) {
            Plik_Stream_Połącz(właściciel_WARTOŚĆ, Nazwa, format_WARTOŚĆ, polecenie); return;
        }
        if (polecenie == 184 && Word_SMS(właściciel_WARTOŚĆ, "java/lang/Integer") && Word_SMS(Nazwa, "parseInt") && Word_SMS(format_WARTOŚĆ, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (polecenie == 182 && Word_SMS(właściciel_WARTOŚĆ, "java/io/PrintStream") && (Word_SMS(Nazwa, "println") || Word_SMS(Nazwa, "print"))) {
            int TYP_WARTOŚĆ = 0, WARTOŚĆ = 0;
            if (Word_SMS(format_WARTOŚĆ, "(I)V")) { TYP_WARTOŚĆ = 1; WARTOŚĆ = 빼기(1); }
            else if (Word_SMS(format_WARTOŚĆ, "(Z)V")) { TYP_WARTOŚĆ = 2; WARTOŚĆ = 빼기(1); }
            else if (Word_SMS(format_WARTOŚĆ, "(C)V")) { TYP_WARTOŚĆ = 3; WARTOŚĆ = 빼기(1); }
            else if (Word_SMS(format_WARTOŚĆ, "(Ljava/lang/String;)V")) { TYP_WARTOŚĆ = 4; WARTOŚĆ = 빼기(2); }
            else if (!Word_SMS(format_WARTOŚĆ, "()V") || !Word_SMS(Nazwa, "println")) awaria_WARTOŚĆ("unsupported print descriptor");
            if (빼기(2) != -1) awaria_WARTOŚĆ("invalid PrintStream receiver");
            if (błąd) return;
            if (TYP_WARTOŚĆ == 1) 자바도구.zapis_identyfikator(WARTOŚĆ);
            if (TYP_WARTOŚĆ == 2) przestrzeń_użytkownika.Zapis(WARTOŚĆ == 0 ? "false" : "true");
            if (TYP_WARTOŚĆ == 3) przestrzeń_użytkownika.zapis_znak_WARTOŚĆ(WARTOŚĆ & 65535);
            if (TYP_WARTOŚĆ == 4) zapis_SMS(WARTOŚĆ);
            if (Word_SMS(Nazwa, "println")) przestrzeń_użytkownika.zapis_znak_WARTOŚĆ(10);
            return;
        }
        if (polecenie == 182 && Word_SMS(właściciel_WARTOŚĆ, "java/lang/String")) {
            if (Word_SMS(Nazwa, "length") && Word_SMS(format_WARTOŚĆ, "()I")) {
                int odwołanie = 빼기(2); if (obiekt_WARTOŚĆ(odwołanie, 1)) 넣기(sterta_WARTOŚĆ[odwołanie + 1], 1); return;
            }
            if (Word_SMS(Nazwa, "charAt") && Word_SMS(format_WARTOŚĆ, "(I)C")) {
                int indeks_dolny_WARTOŚĆ = 빼기(1), odwołanie = 빼기(2);
                if (obiekt_WARTOŚĆ(odwołanie, 1)) {
                    if (indeks_dolny_WARTOŚĆ < 0 || indeks_dolny_WARTOŚĆ >= sterta_WARTOŚĆ[odwołanie + 1]) awaria_WARTOŚĆ("StringIndexOutOfBoundsException"); else 넣기(sterta_WARTOŚĆ[odwołanie + 2 + indeks_dolny_WARTOŚĆ], 1);
                }
                return;
            }
        }
        if (Word_SMS(właściciel_WARTOŚĆ, "java/lang/StringBuilder")) {
            if (polecenie == 183 && Word_SMS(Nazwa, "<init>") && Word_SMS(format_WARTOŚĆ, "()V")) { obiekt_WARTOŚĆ(빼기(2), 4); return; }
            if (polecenie == 182 && Word_SMS(Nazwa, "toString") && Word_SMS(format_WARTOŚĆ, "()Ljava/lang/String;")) {
                int odwołanie = 빼기(2); if (obiekt_WARTOŚĆ(odwołanie, 4)) 넣기(sterta_WARTOŚĆ[odwołanie + 2] == 0 ? host_znak("") : sterta_WARTOŚĆ[odwołanie + 2], 2); return;
            }
            if (polecenie == 182 && Word_SMS(Nazwa, "append")) {
                int tekst = 0;
                if (Word_SMS(format_WARTOŚĆ, "(I)Ljava/lang/StringBuilder;")) tekst = cyfra_znak(빼기(1));
                else if (Word_SMS(format_WARTOŚĆ, "(Z)Ljava/lang/StringBuilder;")) tekst = host_znak(빼기(1) == 0 ? "false" : "true");
                else if (Word_SMS(format_WARTOŚĆ, "(C)Ljava/lang/StringBuilder;")) {
                    int WARTOŚĆ = 빼기(1); tekst = przydzielić_Pamięć(1, 1); if (!błąd) sterta_WARTOŚĆ[tekst + 2] = WARTOŚĆ & 65535;
                }
                else if (Word_SMS(format_WARTOŚĆ, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { tekst = 빼기(2); if (tekst == 0) tekst = host_znak("null"); }
                else { awaria_WARTOŚĆ("unsupported StringBuilder append"); return; }
                int odwołanie = 빼기(2); if (!obiekt_WARTOŚĆ(odwołanie, 4) || !obiekt_WARTOŚĆ(tekst, 1)) return;
                int przód_WARTOŚĆ = sterta_WARTOŚĆ[odwołanie + 2], przód_WARTOŚĆ_długość = przód_WARTOŚĆ == 0 ? 0 : sterta_WARTOŚĆ[przód_WARTOŚĆ + 1], BACK_WARTOŚĆ_długość = sterta_WARTOŚĆ[tekst + 1];
                int 새글 = przydzielić_Pamięć(1, przód_WARTOŚĆ_długość + BACK_WARTOŚĆ_długość); if (błąd) return;
                for (int identyfikator = 0; identyfikator < przód_WARTOŚĆ_długość; identyfikator++) sterta_WARTOŚĆ[새글 + 2 + identyfikator] = sterta_WARTOŚĆ[przód_WARTOŚĆ + 2 + identyfikator];
                for (int identyfikator = 0; identyfikator < BACK_WARTOŚĆ_długość; identyfikator++) sterta_WARTOŚĆ[새글 + 2 + przód_WARTOŚĆ_długość + identyfikator] = sterta_WARTOŚĆ[tekst + 2 + identyfikator];
                sterta_WARTOŚĆ[odwołanie + 2] = 새글; 넣기(odwołanie, 2); return;
            }
        }
        awaria_WARTOŚĆ("unsupported library method");
    }
    static int TABLICA_gniazdo(int odwołanie, int indeks_dolny_WARTOŚĆ, int TYP_WARTOŚĆ) {
        if (!obiekt_WARTOŚĆ(odwołanie, TYP_WARTOŚĆ)) return 0;
        if (indeks_dolny_WARTOŚĆ < 0 || indeks_dolny_WARTOŚĆ >= sterta_WARTOŚĆ[odwołanie + 1]) { awaria_WARTOŚĆ("ArrayIndexOutOfBoundsException"); return 0; }
        return odwołanie + 2 + indeks_dolny_WARTOŚĆ;
    }
    static void Wykonaj_polecenie() {
        int 남음 = 500000;
        while (kadr_INDEKS >= 0 && !błąd) {
            if (--남음 == 0) { awaria_WARTOŚĆ("instruction limit (500000)"); break; }
            int Uruchom_2 = kadr_stanowisko[kadr_INDEKS], WARTOŚĆ = 명바();
            if (błąd) break;
            if (WARTOŚĆ == 0) continue;
            if (WARTOŚĆ == 1) { 넣기(0, 2); continue; }
            if (WARTOŚĆ >= 2 && WARTOŚĆ <= 8) { 넣기(WARTOŚĆ - 3, 1); continue; }
            if (WARTOŚĆ == 16) { 넣기((byte)명바(), 1); continue; }
            if (WARTOŚĆ == 17) { 넣기((short)명짧(), 1); continue; }
            if (WARTOŚĆ == 18 || WARTOŚĆ == 19) {
                int identyfikator = WARTOŚĆ == 18 ? 명바() : 명짧();
                if (identyfikator <= 0 || identyfikator >= stała_ILE_LICZB) awaria_WARTOŚĆ("invalid ldc constant");
                else if (stała_tag[identyfikator] == 3) 넣기(상가[identyfikator], 1);
                else if (stała_tag[identyfikator] == 8) 넣기(stała_SMS(상가[identyfikator]), 2);
                else awaria_WARTOŚĆ("unsupported ldc constant");
                continue;
            }
            if (WARTOŚĆ == 21 || WARTOŚĆ == 25) { 지역읽기(명바(), WARTOŚĆ == 21 ? 1 : 2); continue; }
            if (WARTOŚĆ >= 26 && WARTOŚĆ <= 29) { 지역읽기(WARTOŚĆ - 26, 1); continue; }
            if (WARTOŚĆ >= 42 && WARTOŚĆ <= 45) { 지역읽기(WARTOŚĆ - 42, 2); continue; }
            if (WARTOŚĆ == 54 || WARTOŚĆ == 58) { zapis_lokalny(명바(), WARTOŚĆ == 54 ? 1 : 2); continue; }
            if (WARTOŚĆ >= 59 && WARTOŚĆ <= 62) { zapis_lokalny(WARTOŚĆ - 59, 1); continue; }
            if (WARTOŚĆ >= 75 && WARTOŚĆ <= 78) { zapis_lokalny(WARTOŚĆ - 75, 2); continue; }
            if (WARTOŚĆ == 46 || WARTOŚĆ == 50) {
                int indeks_dolny_WARTOŚĆ = 빼기(1), odwołanie = 빼기(2), gniazdo_wpis = TABLICA_gniazdo(odwołanie, indeks_dolny_WARTOŚĆ, WARTOŚĆ == 46 ? 2 : 3);
                if (!błąd) 넣기(sterta_WARTOŚĆ[gniazdo_wpis], WARTOŚĆ == 46 ? 1 : 2); continue;
            }
            if (WARTOŚĆ == 79 || WARTOŚĆ == 83) {
                int towar_element = 빼기(WARTOŚĆ == 79 ? 1 : 2), indeks_dolny_WARTOŚĆ = 빼기(1), odwołanie = 빼기(2), gniazdo_wpis = TABLICA_gniazdo(odwołanie, indeks_dolny_WARTOŚĆ, WARTOŚĆ == 79 ? 2 : 3);
                if (WARTOŚĆ == 83 && towar_element != 0) obiekt_WARTOŚĆ(towar_element, 1);
                if (!błąd) sterta_WARTOŚĆ[gniazdo_wpis] = towar_element; continue;
            }
            if (WARTOŚĆ == 87) { 빼기(0); continue; }
            if (WARTOŚĆ == 89) { int 가 = 빼기(0), TYP_WARTOŚĆ = zwracany_typ; 넣기(가, TYP_WARTOŚĆ); 넣기(가, TYP_WARTOŚĆ); continue; }
            if (WARTOŚĆ == 95) { int 가 = 빼기(0), 가형 = zwracany_typ, SEKUNDA_operand = 빼기(0), SEKUNDA_operand_TYP = zwracany_typ; 넣기(가, 가형); 넣기(SEKUNDA_operand, SEKUNDA_operand_TYP); continue; }
            if (WARTOŚĆ == 96 || WARTOŚĆ == 100 || WARTOŚĆ == 104 || WARTOŚĆ == 108 || WARTOŚĆ == 112 || WARTOŚĆ == 120
                || WARTOŚĆ == 122 || WARTOŚĆ == 124 || WARTOŚĆ == 126 || WARTOŚĆ == 128 || WARTOŚĆ == 130) {
                int SEKUNDA_operand = 빼기(1), 가 = 빼기(1), WYNIK = 0;
                if ((WARTOŚĆ == 108 || WARTOŚĆ == 112) && SEKUNDA_operand == 0) { awaria_WARTOŚĆ("ArithmeticException: / by zero"); continue; }
                if (WARTOŚĆ == 96) WYNIK = 가 + SEKUNDA_operand;
                if (WARTOŚĆ == 100) WYNIK = 가 - SEKUNDA_operand;
                if (WARTOŚĆ == 104) WYNIK = 가 * SEKUNDA_operand;
                if (WARTOŚĆ == 108) WYNIK = 가 / SEKUNDA_operand;
                if (WARTOŚĆ == 112) WYNIK = 가 % SEKUNDA_operand;
                if (WARTOŚĆ == 120) WYNIK = 가 << SEKUNDA_operand;
                if (WARTOŚĆ == 122) WYNIK = 가 >> SEKUNDA_operand;
                if (WARTOŚĆ == 124) WYNIK = 가 >>> SEKUNDA_operand;
                if (WARTOŚĆ == 126) WYNIK = 가 & SEKUNDA_operand;
                if (WARTOŚĆ == 128) WYNIK = 가 | SEKUNDA_operand;
                if (WARTOŚĆ == 130) WYNIK = 가 ^ SEKUNDA_operand;
                넣기(WYNIK, 1); continue;
            }
            if (WARTOŚĆ == 116) { 넣기(-빼기(1), 1); continue; }
            if (WARTOŚĆ == 132) {
                int lokalny_Scope = 명바(), przyrost_krok = (byte)명바(); 지역읽기(lokalny_Scope, 1); 넣기(빼기(1) + przyrost_krok, 1); zapis_lokalny(lokalny_Scope, 1); continue;
            }
            if (WARTOŚĆ >= 145 && WARTOŚĆ <= 147) {
                int identyfikator = 빼기(1); 넣기(WARTOŚĆ == 145 ? (byte)identyfikator : WARTOŚĆ == 146 ? (char)identyfikator : (short)identyfikator, 1); continue;
            }
            if (WARTOŚĆ >= 153 && WARTOŚĆ <= 167 || WARTOŚĆ == 198 || WARTOŚĆ == 199) {
                int cel_WARTOŚĆ = Uruchom_2 + (short)명짧(); boolean 갈까 = WARTOŚĆ == 167;
                if (WARTOŚĆ >= 153 && WARTOŚĆ <= 158) {
                    int identyfikator = 빼기(1); 갈까 = WARTOŚĆ == 153 ? identyfikator == 0 : WARTOŚĆ == 154 ? identyfikator != 0 : WARTOŚĆ == 155 ? identyfikator < 0 : WARTOŚĆ == 156 ? identyfikator >= 0 : WARTOŚĆ == 157 ? identyfikator > 0 : identyfikator <= 0;
                } else if (WARTOŚĆ >= 159 && WARTOŚĆ <= 166) {
                    int SEKUNDA_operand = 빼기(WARTOŚĆ >= 165 ? 2 : 1), 가 = 빼기(WARTOŚĆ >= 165 ? 2 : 1);
                    갈까 = WARTOŚĆ == 159 || WARTOŚĆ == 165 ? 가 == SEKUNDA_operand : WARTOŚĆ == 160 || WARTOŚĆ == 166 ? 가 != SEKUNDA_operand : WARTOŚĆ == 161 ? 가 < SEKUNDA_operand : WARTOŚĆ == 162 ? 가 >= SEKUNDA_operand : WARTOŚĆ == 163 ? 가 > SEKUNDA_operand : 가 <= SEKUNDA_operand;
                } else if (WARTOŚĆ == 198 || WARTOŚĆ == 199) { int identyfikator = 빼기(2); 갈까 = WARTOŚĆ == 198 ? identyfikator == 0 : identyfikator != 0; }
                if (갈까) przenosić_WARTOŚĆ(cel_WARTOŚĆ); continue;
            }
            if (WARTOŚĆ == 172 || WARTOŚĆ == 176 || WARTOŚĆ == 177) { Zwrot_KR(WARTOŚĆ == 172 ? 1 : WARTOŚĆ == 176 ? 2 : 0); continue; }
            if (WARTOŚĆ == 178) {
                int identyfikator = 명짧(); if (!czek_stała(identyfikator, 9)) continue;
                if (!Word_SMS(nazwa_klasy_SMS(상가[identyfikator]), "java/lang/System") || !Word_SMS(odwołanie_nazwa(stała_SEKUNDA_WARTOŚĆ[identyfikator]), "out")
                    || !Word_SMS(typ_referencyjny(stała_SEKUNDA_WARTOŚĆ[identyfikator]), "Ljava/io/PrintStream;")) awaria_WARTOŚĆ("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (WARTOŚĆ == 182 || WARTOŚĆ == 183 || WARTOŚĆ == 184) { Połącz_metoda(명짧(), WARTOŚĆ); continue; }
            if (WARTOŚĆ == 187) {
                int Nazwa = nazwa_klasy_SMS(명짧());
                if (Word_SMS(Nazwa, "java/lang/StringBuilder")) 넣기(przydzielić_Pamięć(4, 1), 2);
                else if (Word_SMS(Nazwa, "java/io/FileInputStream") || Word_SMS(Nazwa, "java/io/FileOutputStream")) {
                    int odwołanie = przydzielić_Pamięć(Word_SMS(Nazwa, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!błąd) { sterta_WARTOŚĆ[odwołanie + 2] = -1; 넣기(odwołanie, 2); }
                } else awaria_WARTOŚĆ("unsupported object construction");
                continue;
            }
            if (WARTOŚĆ == 188 || WARTOŚĆ == 189) {
                if (WARTOŚĆ == 188) { if (명바() != 10) awaria_WARTOŚĆ("only int[] newarray is supported"); }
                else if (!Word_SMS(nazwa_klasy_SMS(명짧()), "java/lang/String")) awaria_WARTOŚĆ("only String[] anewarray is supported");
                int długość_WARTOŚĆ = 빼기(1); 넣기(przydzielić_Pamięć(WARTOŚĆ == 188 ? 2 : 3, długość_WARTOŚĆ), 2); continue;
            }
            if (WARTOŚĆ == 190) {
                int odwołanie = 빼기(2);
                if (odwołanie < 1 || odwołanie >= sterta_Koniec_stanowisko - 1 || (sterta_WARTOŚĆ[odwołanie] != 2 && sterta_WARTOŚĆ[odwołanie] != 3)) awaria_WARTOŚĆ("null or invalid array");
                else 넣기(sterta_WARTOŚĆ[odwołanie + 1], 1); continue;
            }
            if (WARTOŚĆ == 192) {
                int Nazwa = nazwa_klasy_SMS(명짧()), odwołanie = 빼기(2);
                if (!Word_SMS(Nazwa, "java/lang/String")) awaria_WARTOŚĆ("unsupported checkcast");
                else if (odwołanie != 0) obiekt_WARTOŚĆ(odwołanie, 1);
                넣기(odwołanie, 2); continue;
            }
            awaria_WARTOŚĆ("unsupported bytecode");
        }
    }
    public static int Uruchom_2() {
        if (przestrzeń_użytkownika.인수개수() == 1 && 자바도구.같음(przestrzeń_użytkownika.argumenty(0), "-version")) {
            przestrzeń_użytkownika.Zapis("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (przestrzeń_użytkownika.인수개수() < 1) { przestrzeń_użytkownika.Zapis("Usage: java CLASS [ARGS]\n"); return 2; }
        int długość_WARTOŚĆ = 자바도구.Nazwa(nazwa_pliku_SMS, przestrzeń_użytkownika.argumenty(0));
        if (długość_WARTOŚĆ < 1 || długość_WARTOŚĆ > 57) { przestrzeń_użytkownika.Zapis("java: invalid class name\n"); return 2; }
        nazwa_pliku_SMS[długość_WARTOŚĆ] = '.'; nazwa_pliku_SMS[długość_WARTOŚĆ + 1] = 'c'; nazwa_pliku_SMS[długość_WARTOŚĆ + 2] = 'l'; nazwa_pliku_SMS[długość_WARTOŚĆ + 3] = 'a'; nazwa_pliku_SMS[długość_WARTOŚĆ + 4] = 's'; nazwa_pliku_SMS[długość_WARTOŚĆ + 5] = 's';
        Rozmiar = przestrzeń_użytkownika.파일읽기(nazwa_pliku_SMS, nazwa_pliku);
        if (Rozmiar < 0) { przestrzeń_użytkownika.Zapis("java: cannot read class: "); 자바도구.zapis_identyfikator(Rozmiar); przestrzeń_użytkownika.zapis_znak_WARTOŚĆ(10); return 1; }
        클래스읽기(); if (błąd) return 1;
        int znak_nazwa = stała_SMS(nazwa_klasy);
        if (!błąd && sterta_WARTOŚĆ[znak_nazwa + 1] != długość_WARTOŚĆ) awaria_WARTOŚĆ("class name does not match file");
        for (int identyfikator = 0; identyfikator < długość_WARTOŚĆ && !błąd; identyfikator++) if (sterta_WARTOŚĆ[znak_nazwa + 2 + identyfikator] != nazwa_pliku_SMS[identyfikator]) awaria_WARTOŚĆ("class name does not match file");
        int punkt_wejścia_WARTOŚĆ = -1;
        for (int identyfikator = 0; identyfikator < metoda_ILE_LICZB; identyfikator++) if (Word_SMS(metoda_nazwa_SMS[identyfikator], "main") && Word_SMS(metoda_TYP[identyfikator], "([Ljava/lang/String;)V") && (metoda_dostęp[identyfikator] & 9) == 9) punkt_wejścia_WARTOŚĆ = identyfikator;
        if (punkt_wejścia_WARTOŚĆ < 0) awaria_WARTOŚĆ("public static void main(String[] args) required");
        if (błąd) return 1;
        int argumenty = przydzielić_Pamięć(3, przestrzeń_użytkownika.인수개수() - 1);
        for (int identyfikator = 1; identyfikator < przestrzeń_użytkownika.인수개수() && !błąd; identyfikator++) sterta_WARTOŚĆ[argumenty + 1 + identyfikator] = host_znak(przestrzeń_użytkownika.argumenty(identyfikator));
        kadr_INDEKS = 0; kadr_metoda[0] = punkt_wejścia_WARTOŚĆ; kadr_stanowisko[0] = metoda_START[punkt_wejścia_WARTOŚĆ]; lokalny_WARTOŚĆ[0] = argumenty; lokalny_TYP[0] = 2;
        Wykonaj_polecenie(); return błąd ? 1 : 0;
    }
}
