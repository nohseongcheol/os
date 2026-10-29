// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. nazwa_pliku/operand_Stos/odwołanie/gałąź_22e01337 경계를 Wykonaj_polecenie 중 검사한다. */
public final class 자바가상기계 {
    static int[] nazwa_pliku = new int[16 * 16384], plik_tymczasowy = new int[16384], nazwa_pliku_SMS = new int[512];
    static int[] stała_tag = new int[8192], 상가 = new int[8192], stała_SEKUNDA_WARTOŚĆ = new int[8192], ciąg_odwołanie = new int[8192];
    static int[] metoda_nazwa_SMS = new int[512], metoda_TYP = new int[512], metoda_dostęp = new int[512], metoda_właściciel = new int[512];
    static int[] metoda_START = new int[512], metoda_Koniec = new int[512], metoda_Stos = new int[512], 함수지역 = new int[512];
    static int[] metoda_argument_ILE_LICZB = new int[512], metoda_argument_TYP = new int[8192], metoda_Zwrot = new int[512];
    static int[] granica_WARTOŚĆ = new int[16 * 16384];
    static int[] lokalny_WARTOŚĆ = new int[16384], lokalny_TYP = new int[16384], operand_Stos_WARTOŚĆ = new int[16384], operand_Stos_TYP = new int[16384];
    static int[] kadr_metoda = new int[128], kadr_stanowisko = new int[128], kadr_Stos = new int[128], kadr_instrukcja = new int[128], inicjuj_kadr = new int[128];
    static int[] Klasa_Definicja_nazwa = new int[16], Klasa_Definicja_zmienić_rozmiar = new int[16], Klasa_Definicja_nadrzędny = new int[16], Klasa_Definicja_Stan = new int[16], Klasa_gniazdo_ILE_LICZB = new int[16], inicjuj_Klasa_Definicja = new int[16];
    static int[] Klasa_interfejs = new int[16 * 16], Klasa_interfejs_ILE_LICZB = new int[16];
    static int[] gniazdo_nazwa = new int[512], gniazdo_TYP = new int[512], gniazdo_właściciel = new int[512], gniazdo_Uprawnienia = new int[512], gniazdo_stanowisko = new int[512], gniazdo_dane = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] sterta_WARTOŚĆ = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], sterta_odwołanie = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], element_tablicy = new int[32768], Store_liczba_całkowita = new int[256];
    static int Rozmiar, 읽기위치, metoda_ILE_LICZB, nazwa_klasy, kadr_INDEKS = -1, sterta_Koniec_stanowisko = 1, zwracany_typ;
    static int Klasa_Definicja_ILE_LICZB, gniazdo_ILE_LICZB, 잡기수, 현재읽는종, 던진객체, 잠시수, wyświetlać_ILE_LICZB, Kolekcja_ILE_LICZB;
    static int bieżący_wątek, liczba_wątków = 1, wpis_Klasa_Definicja;
    static int[] wątek_kadr = new int[4], wątek_Stan = new int[4], wątek_obiekt = new int[4], wątek_cel = new int[4], 가닥대기 = new int[4];
    static boolean błąd, żądanie_zmiany;
    static int[] blokada_właściciel = new int[32768], 잠금깊이 = new int[32768], kadr_blokada = new int[128], Klasa_blokada = new int[16], Klasa_wątek = new int[16];

    static void awaria_WARTOŚĆ(String Word_SMS) {
        if (błąd) return;
        int obszar_KOD = 0;
        if (자바도구.같음(Word_SMS, "ArithmeticException: / by zero")) obszar_KOD = 4;
        if (자바도구.같음(Word_SMS, "NullPointerException") || 자바도구.같음(Word_SMS, "null or invalid array")) obszar_KOD = 5;
        if (자바도구.같음(Word_SMS, "ArrayIndexOutOfBoundsException")) obszar_KOD = 7;
        if (자바도구.같음(Word_SMS, "StringIndexOutOfBoundsException")) obszar_KOD = 8;
        if (자바도구.같음(Word_SMS, "NumberFormatException")) obszar_KOD = 10;
        if (자바도구.같음(Word_SMS, "FileNotFoundException: file open failed")) obszar_KOD = 12;
        if (자바도구.같음(Word_SMS, "IOException: stream closed") || 자바도구.같음(Word_SMS, "IOException: read failed") || 자바도구.같음(Word_SMS, "IOException: write failed")) obszar_KOD = 11;
        if (자바도구.같음(Word_SMS, "ClassCastException")) obszar_KOD = 14;
        if (자바도구.같음(Word_SMS, "NegativeArraySizeException")) obszar_KOD = 15;
        if (obszar_KOD != 0 && kadr_INDEKS >= 0) { 예외던짐(obszar_KOD, Word_SMS); return; }
        przestrzeń_użytkownika.Zapis("JVM error: "); przestrzeń_użytkownika.Zapis(Word_SMS); przestrzeń_użytkownika.zapis_znak_WARTOŚĆ(10); błąd = true;
    }
    static boolean obcinać(int Uruchom_2, int długość_WARTOŚĆ) {
        if (Uruchom_2 < 0 || Uruchom_2 >= nazwa_pliku.length || długość_WARTOŚĆ < 0) return false;
        int Klasa_Definicja = Uruchom_2 / 16384;
        return Uruchom_2 % 16384 <= Klasa_Definicja_zmienić_rozmiar[Klasa_Definicja] && długość_WARTOŚĆ <= Klasa_Definicja_zmienić_rozmiar[Klasa_Definicja] - Uruchom_2 % 16384;
    }
    static int bajt_WARTOŚĆ() {
        if (!obcinać(읽기위치, 1)) { awaria_WARTOŚĆ("truncated class file"); return 0; }
        return nazwa_pliku[읽기위치++];
    }
    static int 짧은수() { return bajt_WARTOŚĆ() << 8 | bajt_WARTOŚĆ(); }
    static int liczba_całkowita() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int długość_WARTOŚĆ) { if (!obcinać(읽기위치, długość_WARTOŚĆ)) awaria_WARTOŚĆ("invalid attribute size"); else 읽기위치 += długość_WARTOŚĆ; }
    static boolean czek_stała(int identyfikator, int Rodzaj_WARTOŚĆ) {
        if (identyfikator <= 0 || identyfikator >= stała_tag.length || stała_tag[identyfikator] != Rodzaj_WARTOŚĆ) { awaria_WARTOŚĆ("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean SMS_zakres(int Uruchom_2, int długość_WARTOŚĆ, String Word_SMS) {
        if (!obcinać(Uruchom_2, długość_WARTOŚĆ)) return false;
        int 읽는자리 = Uruchom_2, 끝 = Uruchom_2 + długość_WARTOŚĆ;
        for (int Loop_INDEKS = 0; Loop_INDEKS < Word_SMS.length(); Loop_INDEKS++) {
            int kod_znaku = Word_SMS.charAt(Loop_INDEKS);
            if (kod_znaku > 0 && kod_znaku < 128) { if (읽는자리 >= 끝 || nazwa_pliku[읽는자리++] != kod_znaku) return false; }
            else if (kod_znaku < 2048) {
                if (읽는자리 + 2 > 끝 || nazwa_pliku[읽는자리++] != (192 | (kod_znaku >> 6)) || nazwa_pliku[읽는자리++] != (128 | (kod_znaku & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || nazwa_pliku[읽는자리++] != (224 | (kod_znaku >> 12)) || nazwa_pliku[읽는자리++] != (128 | ((kod_znaku >> 6) & 63)) || nazwa_pliku[읽는자리++] != (128 | (kod_znaku & 63))) return false;
        }
        return 읽는자리 == 끝;
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
    static int 상번호() { int WARTOŚĆ = 짧은수(); return WARTOŚĆ == 0 ? 0 : 현재읽는종 * 512 + WARTOŚĆ; }
    static int 명상수() { return metoda_właściciel[kadr_metoda[kadr_INDEKS]] * 512 + 명짧(); }
    static void pominąć_atrybut() {
        int towar_ILE_LICZB = 짧은수();
        for (int identyfikator = 0; identyfikator < towar_ILE_LICZB && !błąd; identyfikator++) { czek_stała(상번호(), 1); 건너(liczba_całkowita()); }
    }
    static int polecenie_długość(int WARTOŚĆ) {
        if (WARTOŚĆ == 16 || WARTOŚĆ == 18 || WARTOŚĆ == 21 || WARTOŚĆ == 25 || WARTOŚĆ == 54 || WARTOŚĆ == 58 || WARTOŚĆ == 188) return 2;
        if (WARTOŚĆ == 17 || WARTOŚĆ == 19 || WARTOŚĆ == 132 || WARTOŚĆ >= 153 && WARTOŚĆ <= 167
            || WARTOŚĆ >= 178 && WARTOŚĆ <= 184 || WARTOŚĆ == 187 || WARTOŚĆ == 189 || WARTOŚĆ == 192 || WARTOŚĆ == 193 || WARTOŚĆ == 198 || WARTOŚĆ == 199) return 3;
        if (WARTOŚĆ == 185 || WARTOŚĆ == 200) return 5;
        if (WARTOŚĆ >= 0 && WARTOŚĆ <= 8 || WARTOŚĆ >= 26 && WARTOŚĆ <= 29 || WARTOŚĆ >= 42 && WARTOŚĆ <= 46 || WARTOŚĆ >= 50 && WARTOŚĆ <= 53
            || WARTOŚĆ >= 59 && WARTOŚĆ <= 62 || WARTOŚĆ >= 75 && WARTOŚĆ <= 79 || WARTOŚĆ >= 83 && WARTOŚĆ <= 95
            || WARTOŚĆ == 96 || WARTOŚĆ == 100 || WARTOŚĆ == 104 || WARTOŚĆ == 108 || WARTOŚĆ == 112 || WARTOŚĆ == 116
            || WARTOŚĆ == 120 || WARTOŚĆ == 122 || WARTOŚĆ == 124 || WARTOŚĆ == 126 || WARTOŚĆ == 128 || WARTOŚĆ == 130
            || WARTOŚĆ >= 145 && WARTOŚĆ <= 147 || WARTOŚĆ == 172 || WARTOŚĆ == 176 || WARTOŚĆ == 177 || WARTOŚĆ == 190 || WARTOŚĆ == 191
            || WARTOŚĆ == 194 || WARTOŚĆ == 195) return 1;
        return 0;
    }
    static int stanowisko_liczba_całkowita(int 읽는자리) {
        if (!obcinać(읽는자리, 4)) { awaria_WARTOŚĆ("truncated bytecode operand"); return 0; }
        return nazwa_pliku[읽는자리] << 24 | nazwa_pliku[읽는자리 + 1] << 16 | nazwa_pliku[읽는자리 + 2] << 8 | nazwa_pliku[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int Uruchom_2, int 끝) {
        int WARTOŚĆ = nazwa_pliku[읽는자리], długość_WARTOŚĆ = polecenie_długość(WARTOŚĆ);
        if (WARTOŚĆ == 170 || WARTOŚĆ == 171) {
            int baza_stanowisko = 읽는자리 + 1;
            while ((baza_stanowisko - Uruchom_2) % 4 != 0) baza_stanowisko++;
            if (끝 - baza_stanowisko < (WARTOŚĆ == 170 ? 12 : 8)) return 0;
            int wpis_ILE_LICZB = WARTOŚĆ == 170 ? stanowisko_liczba_całkowita(baza_stanowisko + 8) - stanowisko_liczba_całkowita(baza_stanowisko + 4) + 1 : stanowisko_liczba_całkowita(baza_stanowisko + 4);
            if (wpis_ILE_LICZB < 0 || wpis_ILE_LICZB > 2048) return 0;
            długość_WARTOŚĆ = baza_stanowisko - 읽는자리 + (WARTOŚĆ == 170 ? 12 + 4 * wpis_ILE_LICZB : 8 + 8 * wpis_ILE_LICZB);
        }
        if (WARTOŚĆ == 196 && 읽는자리 + 1 < 끝) {
            int Word_dane = nazwa_pliku[읽는자리 + 1]; długość_WARTOŚĆ = Word_dane == 132 ? 6 : (Word_dane == 21 || Word_dane == 25 || Word_dane == 54 || Word_dane == 58) ? 4 : 0;
        }
        return długość_WARTOŚĆ > 0 && długość_WARTOŚĆ <= 끝 - 읽는자리 ? długość_WARTOŚĆ : 0;
    }
    static void czek_cel_WARTOŚĆ(int cel_WARTOŚĆ, int FUNKCJA_WARTOŚĆ) {
        if (cel_WARTOŚĆ < metoda_START[FUNKCJA_WARTOŚĆ] || cel_WARTOŚĆ >= metoda_Koniec[FUNKCJA_WARTOŚĆ] || granica_WARTOŚĆ[cel_WARTOŚĆ] != FUNKCJA_WARTOŚĆ + 1) awaria_WARTOŚĆ("invalid branch target");
    }
    static void 클래스읽기(int Klasa_Definicja) {
        현재읽는종 = Klasa_Definicja; 읽기위치 = Klasa_Definicja * 16384; Rozmiar = 읽기위치 + Klasa_Definicja_zmienić_rozmiar[Klasa_Definicja];
        if (liczba_całkowita() != 0xcafebabe) { awaria_WARTOŚĆ("not a class file"); return; }
        int 부판 = 짧은수(), wersja_WARTOŚĆ = 짧은수();
        if (wersja_WARTOŚĆ < 45 || wersja_WARTOŚĆ > 52 || 부판 != 0) { awaria_WARTOŚĆ("supported class versions: 45..52, minor 0"); return; }
        int stała_ILE_LICZB = 짧은수(), baza_stanowisko = Klasa_Definicja * 512;
        if (stała_ILE_LICZB < 1 || stała_ILE_LICZB > 512) { awaria_WARTOŚĆ("constant pool limit (511)"); return; }
        for (int wpis_ILE_LICZB = 1; wpis_ILE_LICZB < stała_ILE_LICZB && !błąd; wpis_ILE_LICZB++) {
            int identyfikator = baza_stanowisko + wpis_ILE_LICZB, Rodzaj_WARTOŚĆ = bajt_WARTOŚĆ(); stała_tag[identyfikator] = Rodzaj_WARTOŚĆ;
            if (Rodzaj_WARTOŚĆ == 1) { stała_SEKUNDA_WARTOŚĆ[identyfikator] = 짧은수(); 상가[identyfikator] = 읽기위치; 건너(stała_SEKUNDA_WARTOŚĆ[identyfikator]); }
            else if (Rodzaj_WARTOŚĆ == 3) 상가[identyfikator] = liczba_całkowita();
            else if (Rodzaj_WARTOŚĆ == 7 || Rodzaj_WARTOŚĆ == 8) 상가[identyfikator] = 상번호();
            else if (Rodzaj_WARTOŚĆ == 9 || Rodzaj_WARTOŚĆ == 10 || Rodzaj_WARTOŚĆ == 11 || Rodzaj_WARTOŚĆ == 12) { 상가[identyfikator] = 상번호(); stała_SEKUNDA_WARTOŚĆ[identyfikator] = 상번호(); }
            else awaria_WARTOŚĆ("unsupported constant type");
        }
        int pozwolenie_WARTOŚĆ = 짧은수();
        if ((pozwolenie_WARTOŚĆ & (0x2000 | 0x4000)) != 0) awaria_WARTOŚĆ("annotation/enum class unsupported");
        Klasa_Definicja_nazwa[Klasa_Definicja] = nazwa_klasy_SMS(상번호());
        Klasa_Definicja_nadrzędny[Klasa_Definicja] = nazwa_klasy_SMS(상번호());
        int interfejs_ILE_LICZB = 짧은수(); if (interfejs_ILE_LICZB > 16) { awaria_WARTOŚĆ("interface count limit"); return; }
        Klasa_interfejs_ILE_LICZB[Klasa_Definicja] = interfejs_ILE_LICZB;
        for (int Loop_INDEKS = 0; Loop_INDEKS < interfejs_ILE_LICZB; Loop_INDEKS++) Klasa_interfejs[Klasa_Definicja * 16 + Loop_INDEKS] = nazwa_klasy_SMS(상번호());
        int pole_ILE_LICZB = 짧은수();
        if (pole_ILE_LICZB > 512 - gniazdo_ILE_LICZB) { awaria_WARTOŚĆ("field count limit (512)"); return; }
        for (int Loop_INDEKS = 0; Loop_INDEKS < pole_ILE_LICZB && !błąd; Loop_INDEKS++) {
            int Plik_INDEKS = gniazdo_ILE_LICZB++; gniazdo_właściciel[Plik_INDEKS] = Klasa_Definicja; gniazdo_Uprawnienia[Plik_INDEKS] = 짧은수(); gniazdo_nazwa[Plik_INDEKS] = 상번호(); gniazdo_TYP[Plik_INDEKS] = 상번호();
            czek_stała(gniazdo_nazwa[Plik_INDEKS], 1); czek_stała(gniazdo_TYP[Plik_INDEKS], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[gniazdo_TYP[Plik_INDEKS]]; int obszar_KOD = deskryptor_TYP(읽기위치 + stała_SEKUNDA_WARTOŚĆ[gniazdo_TYP[Plik_INDEKS]], false); 읽기위치 = 보존값;
            if ((gniazdo_Uprawnienia[Plik_INDEKS] & 8) == 0) gniazdo_stanowisko[Plik_INDEKS] = Klasa_gniazdo_ILE_LICZB[Klasa_Definicja]++;
            int atrybut_dane = 짧은수();
            for (int wewnętrzne_stanowisko = 0; wewnętrzne_stanowisko < atrybut_dane && !błąd; wewnętrzne_stanowisko++) {
                int nazwa_stała = 상번호(), prawidłowy_długość = liczba_całkowita();
                if (Word_SMS(nazwa_stała, "ConstantValue") && prawidłowy_długość == 2) {
                    int dane_WARTOŚĆ = 상번호();
                    if (obszar_KOD == 1 && czek_stała(dane_WARTOŚĆ, 3)) gniazdo_dane[Plik_INDEKS] = 상가[dane_WARTOŚĆ];
                    else if (obszar_KOD == 2 && czek_stała(dane_WARTOŚĆ, 8)) gniazdo_dane[Plik_INDEKS] = stała_SMS(상가[dane_WARTOŚĆ]);
                } else 건너(prawidłowy_długość);
            }
        }
        int towar_ILE_LICZB = 짧은수();
        if (towar_ILE_LICZB > 512 - metoda_ILE_LICZB) { awaria_WARTOŚĆ("method count limit (512)"); return; }
        for (int Loop_INDEKS = 0; Loop_INDEKS < towar_ILE_LICZB && !błąd; Loop_INDEKS++) {
            int identyfikator = metoda_ILE_LICZB++; metoda_właściciel[identyfikator] = Klasa_Definicja;
            metoda_dostęp[identyfikator] = 짧은수(); metoda_nazwa_SMS[identyfikator] = 상번호(); metoda_TYP[identyfikator] = 상번호();
            czek_stała(metoda_nazwa_SMS[identyfikator], 1); 서술읽기(identyfikator);
            if ((metoda_dostęp[identyfikator] & 8) == 0) {
                if (metoda_argument_ILE_LICZB[identyfikator] == 16) { awaria_WARTOŚĆ("too many instance method arguments"); return; }
                for (int Porównanie_stanowisko = metoda_argument_ILE_LICZB[identyfikator]; Porównanie_stanowisko > 0; Porównanie_stanowisko--) metoda_argument_TYP[identyfikator * 16 + Porównanie_stanowisko] = metoda_argument_TYP[identyfikator * 16 + Porównanie_stanowisko - 1];
                metoda_argument_TYP[identyfikator * 16] = 2; metoda_argument_ILE_LICZB[identyfikator]++;
            }
            if ((metoda_dostęp[identyfikator] & 0x100) != 0) awaria_WARTOŚĆ("user native method unsupported");
            if (Word_SMS(metoda_nazwa_SMS[identyfikator], "<clinit>")) inicjuj_Klasa_Definicja[Klasa_Definicja] = identyfikator + 1;
            for (int przód_WARTOŚĆ = 0; przód_WARTOŚĆ < identyfikator; przód_WARTOŚĆ++) if (metoda_właściciel[przód_WARTOŚĆ] == Klasa_Definicja && 같은말(metoda_nazwa_SMS[przód_WARTOŚĆ], metoda_nazwa_SMS[identyfikator]) && 같은말(metoda_TYP[przód_WARTOŚĆ], metoda_TYP[identyfikator])) awaria_WARTOŚĆ("duplicate method");
            int atrybut_ILE_LICZB = 짧은수();
            for (int wartość_atrybutu = 0; wartość_atrybutu < atrybut_ILE_LICZB && !błąd; wartość_atrybutu++) {
                int Nazwa = 상번호(), długość_WARTOŚĆ = liczba_całkowita(), Uruchom_2 = 읽기위치;
                if (!obcinać(Uruchom_2, długość_WARTOŚĆ)) { awaria_WARTOŚĆ("truncated method attribute"); break; }
                if (Word_SMS(Nazwa, "Code")) {
                    if (metoda_START[identyfikator] != 0) awaria_WARTOŚĆ("duplicate Code attribute");
                    metoda_Stos[identyfikator] = 짧은수(); 함수지역[identyfikator] = 짧은수(); int KOD_długość = liczba_całkowita();
                    if (metoda_Stos[identyfikator] > 128 || 함수지역[identyfikator] > 128 || 함수지역[identyfikator] < metoda_argument_ILE_LICZB[identyfikator]
                        || KOD_długość < 1 || KOD_długość > 8192) awaria_WARTOŚĆ("method memory limits exceeded");
                    metoda_START[identyfikator] = 읽기위치; 건너(KOD_długość); metoda_Koniec[identyfikator] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { awaria_WARTOŚĆ("exception table limit"); return; }
                    for (int wewnętrzne_stanowisko = 0; wewnętrzne_stanowisko < 잡는수; wewnętrzne_stanowisko++) {
                        int błąd_odwołanie = 잡기수++; 잡기함수[błąd_odwołanie] = identyfikator;
                        잡기시작[błąd_odwołanie] = metoda_START[identyfikator] + 짧은수(); 잡기끝[błąd_odwołanie] = metoda_START[identyfikator] + 짧은수();
                        잡기위치[błąd_odwołanie] = metoda_START[identyfikator] + 짧은수(); int 부호값 = 상번호(); 잡기종[błąd_odwołanie] = 부호값 == 0 ? 0 : nazwa_klasy_SMS(부호값);
                    }
                    pominąć_atrybut();
                    if (읽기위치 != Uruchom_2 + długość_WARTOŚĆ) awaria_WARTOŚĆ("Code attribute size mismatch");
                } else 건너(długość_WARTOŚĆ);
            }
            if ((metoda_dostęp[identyfikator] & 0x400) != 0) continue;
            if (metoda_START[identyfikator] == 0) awaria_WARTOŚĆ("missing Code attribute");
            int gniazdo_wpis = metoda_START[identyfikator];
            while (gniazdo_wpis < metoda_Koniec[identyfikator] && !błąd) {
                int długość_WARTOŚĆ = 길이읽기(gniazdo_wpis, metoda_START[identyfikator], metoda_Koniec[identyfikator]);
                if (długość_WARTOŚĆ == 0) { awaria_WARTOŚĆ("unsupported or truncated bytecode"); break; }
                granica_WARTOŚĆ[gniazdo_wpis] = identyfikator + 1; gniazdo_wpis += długość_WARTOŚĆ;
            }
            gniazdo_wpis = metoda_START[identyfikator];
            while (gniazdo_wpis < metoda_Koniec[identyfikator] && !błąd) {
                int WARTOŚĆ = nazwa_pliku[gniazdo_wpis];
                if (WARTOŚĆ >= 153 && WARTOŚĆ <= 167 || WARTOŚĆ == 198 || WARTOŚĆ == 199) czek_cel_WARTOŚĆ(gniazdo_wpis + (short)(nazwa_pliku[gniazdo_wpis + 1] << 8 | nazwa_pliku[gniazdo_wpis + 2]), identyfikator);
                if (WARTOŚĆ == 200) czek_cel_WARTOŚĆ(gniazdo_wpis + stanowisko_liczba_całkowita(gniazdo_wpis + 1), identyfikator);
                if (WARTOŚĆ == 170 || WARTOŚĆ == 171) {
                    int 읽는자리 = gniazdo_wpis + 1; while ((읽는자리 - metoda_START[identyfikator]) % 4 != 0) 읽는자리++;
                    czek_cel_WARTOŚĆ(gniazdo_wpis + stanowisko_liczba_całkowita(읽는자리), identyfikator);
                    int wpis_ILE_LICZB = WARTOŚĆ == 170 ? stanowisko_liczba_całkowita(읽는자리 + 8) - stanowisko_liczba_całkowita(읽는자리 + 4) + 1 : stanowisko_liczba_całkowita(읽는자리 + 4);
                    읽는자리 += WARTOŚĆ == 170 ? 12 : 8;
                    for (int wewnętrzne_stanowisko = 0; wewnętrzne_stanowisko < wpis_ILE_LICZB; wewnętrzne_stanowisko++) czek_cel_WARTOŚĆ(gniazdo_wpis + stanowisko_liczba_całkowita(읽는자리 + wewnętrzne_stanowisko * (WARTOŚĆ == 170 ? 4 : 8) + (WARTOŚĆ == 170 ? 0 : 4)), identyfikator);
                }
                gniazdo_wpis += 길이읽기(gniazdo_wpis, metoda_START[identyfikator], metoda_Koniec[identyfikator]);
            }
            for (int wewnętrzne_stanowisko = 0; wewnętrzne_stanowisko < 잡기수; wewnętrzne_stanowisko++) if (잡기함수[wewnętrzne_stanowisko] == identyfikator) {
                czek_cel_WARTOŚĆ(잡기시작[wewnętrzne_stanowisko], identyfikator); czek_cel_WARTOŚĆ(잡기위치[wewnętrzne_stanowisko], identyfikator);
                if (잡기끝[wewnętrzne_stanowisko] != metoda_Koniec[identyfikator]) czek_cel_WARTOŚĆ(잡기끝[wewnętrzne_stanowisko], identyfikator);
                if (잡기시작[wewnętrzne_stanowisko] >= 잡기끝[wewnętrzne_stanowisko]) awaria_WARTOŚĆ("invalid exception range");
            }
        }
        if (!błąd) pominąć_atrybut();
        if (읽기위치 != Rozmiar) awaria_WARTOŚĆ("extra class file data");
    }
    static int przydzielić_Pamięć(int Rodzaj_WARTOŚĆ, int długość_WARTOŚĆ) { return 새기억(Rodzaj_WARTOŚĆ, długość_WARTOŚĆ); }
    static boolean obiekt_WARTOŚĆ(int odwołanie, int Rodzaj_WARTOŚĆ) {
        if (!systemy_informacyjne_prawidłowy_obiekt(odwołanie)) return false;
        if (sterta_WARTOŚĆ[odwołanie] != Rodzaj_WARTOŚĆ) { awaria_WARTOŚĆ("object type mismatch"); return false; }
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
        if (zwracany_typ == 2) chronić_WARTOŚĆ(operand_Stos_WARTOŚĆ[gniazdo_wpis]);
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
        if (kadr_INDEKS % 32 == 31) { awaria_WARTOŚĆ("call stack limit (32)"); return; }
        int Dalej_towar = kadr_INDEKS + 1;
        for (int identyfikator = 0; identyfikator < 128; identyfikator++) lokalny_TYP[Dalej_towar * 128 + identyfikator] = 0;
        for (int identyfikator = metoda_argument_ILE_LICZB[FUNKCJA_WARTOŚĆ] - 1; identyfikator >= 0; identyfikator--) {
            lokalny_WARTOŚĆ[Dalej_towar * 128 + identyfikator] = 빼기(metoda_argument_TYP[FUNKCJA_WARTOŚĆ * 16 + identyfikator]); lokalny_TYP[Dalej_towar * 128 + identyfikator] = metoda_argument_TYP[FUNKCJA_WARTOŚĆ * 16 + identyfikator];
        }
        if (błąd) return;
        kadr_INDEKS = Dalej_towar; inicjuj_kadr[kadr_INDEKS] = 0; kadr_metoda[kadr_INDEKS] = FUNKCJA_WARTOŚĆ; kadr_stanowisko[kadr_INDEKS] = metoda_START[FUNKCJA_WARTOŚĆ]; kadr_Stos[kadr_INDEKS] = 0;
    }
    static void Zwrot_KR(int TYP_WARTOŚĆ) {
        if (TYP_WARTOŚĆ != metoda_Zwrot[kadr_metoda[kadr_INDEKS]]) { awaria_WARTOŚĆ("return type mismatch"); return; }
        int WARTOŚĆ = TYP_WARTOŚĆ == 0 ? 0 : 빼기(TYP_WARTOŚĆ);
        if (inicjuj_kadr[kadr_INDEKS] != 0) Klasa_Definicja_Stan[inicjuj_kadr[kadr_INDEKS] - 1] = 2;
        if (kadr_blokada[kadr_INDEKS] != 0) { wersja_blokada(kadr_blokada[kadr_INDEKS]); kadr_blokada[kadr_INDEKS] = 0; }
        kadr_INDEKS--; if (kadr_INDEKS >= bieżący_wątek * 32 && TYP_WARTOŚĆ != 0) 넣기(WARTOŚĆ, TYP_WARTOŚĆ);
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
                if (WARTOŚĆ < 1) { awaria_WARTOŚĆ("invalid file stream path"); return; }
                Stream_nazwa_pliku[gniazdo_wpis] = WARTOŚĆ;
            }
            Stream_nazwa_pliku[długość_WARTOŚĆ] = 0;
            int deskryptor_wpis = przestrzeń_użytkownika.otwarty_Plik_deskryptor(Stream_nazwa_pliku, pozycja_wyjścia ? (이어 ? 1089 : 577) : 0);
            if (deskryptor_wpis < 0) { awaria_WARTOŚĆ("FileNotFoundException: file open failed"); return; }
            sterta_WARTOŚĆ[Stream_WARTOŚĆ + 2] = deskryptor_wpis; sterta_WARTOŚĆ[Stream_WARTOŚĆ + 3] = 1;
            return;
        }
        if (polecenie != 182) { awaria_WARTOŚĆ("invalid file stream invocation"); return; }
        if ((pozycja_wyjścia && Word_SMS(Nazwa, "write") || !pozycja_wyjścia && Word_SMS(Nazwa, "read"))
            && (Word_SMS(format_WARTOŚĆ, pozycja_wyjścia ? "([B)V" : "([B)I") || Word_SMS(format_WARTOŚĆ, pozycja_wyjścia ? "([BII)V" : "([BII)I"))) {
            boolean obcinać_WARTOŚĆ = Word_SMS(format_WARTOŚĆ, pozycja_wyjścia ? "([BII)V" : "([BII)I");
            int wpis_ILE_LICZB = obcinać_WARTOŚĆ ? 빼기(1) : 0, 시작점 = obcinać_WARTOŚĆ ? 빼기(1) : 0, dane_TABLICA = 빼기(2), obiekt_odwołanie = 빼기(2);
            if (!obiekt_WARTOŚĆ(dane_TABLICA, 20) || !obiekt_WARTOŚĆ(obiekt_odwołanie, Rodzaj_WARTOŚĆ)) return;
            if (!obcinać_WARTOŚĆ) wpis_ILE_LICZB = sterta_WARTOŚĆ[dane_TABLICA + 1];
            if (시작점 < 0 || wpis_ILE_LICZB < 0 || 시작점 > sterta_WARTOŚĆ[dane_TABLICA + 1] - wpis_ILE_LICZB) { 예외던짐(6, "file buffer bounds"); return; }
            if (sterta_WARTOŚĆ[obiekt_odwołanie + 3] == 0 || sterta_WARTOŚĆ[obiekt_odwołanie + 2] < 0) { awaria_WARTOŚĆ("IOException: stream closed"); return; }
            int Wykonane_ILE_LICZB = 0;
            while (Wykonane_ILE_LICZB < wpis_ILE_LICZB && !błąd) {
                int 반환값 = pozycja_wyjścia ? przestrzeń_użytkownika.파일한바이트쓰기(sterta_WARTOŚĆ[obiekt_odwołanie + 2], sterta_WARTOŚĆ[dane_TABLICA + 2 + 시작점 + Wykonane_ILE_LICZB]) : przestrzeń_użytkownika.파일한바이트읽기(sterta_WARTOŚĆ[obiekt_odwołanie + 2]);
                if (반환값 < 0) { awaria_WARTOŚĆ(pozycja_wyjścia ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!pozycja_wyjścia && 반환값 == 256) break;
                if (!pozycja_wyjścia) sterta_WARTOŚĆ[dane_TABLICA + 2 + 시작점 + Wykonane_ILE_LICZB] = (byte)반환값;
                Wykonane_ILE_LICZB++;
            }
            if (!pozycja_wyjścia) 넣기(wpis_ILE_LICZB != 0 && Wykonane_ILE_LICZB == 0 ? -1 : Wykonane_ILE_LICZB, 1);
            return;
        }
        if (pozycja_wyjścia && Word_SMS(Nazwa, "flush") && Word_SMS(format_WARTOŚĆ, "()V")) { int obiekt_odwołanie = 빼기(2); if (obiekt_WARTOŚĆ(obiekt_odwołanie, Rodzaj_WARTOŚĆ) && sterta_WARTOŚĆ[obiekt_odwołanie + 2] < 0) awaria_WARTOŚĆ("IOException: stream closed"); return; }
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
            if (WYNIK < -1) awaria_WARTOŚĆ("IOException: read failed"); else 넣기(WYNIK == 256 ? -1 : WYNIK, 1);
        } else if (przestrzeń_użytkownika.파일한바이트쓰기(deskryptor_wpis, WARTOŚĆ) != 1) awaria_WARTOŚĆ("IOException: write failed");
    }
    static void Połącz_metoda(int INDEKS, int polecenie) {
        if (INDEKS <= 0 || INDEKS >= stała_tag.length || (stała_tag[INDEKS] != 10 && stała_tag[INDEKS] != 11)) { awaria_WARTOŚĆ("invalid method reference"); return; }
        int właściciel_WARTOŚĆ = nazwa_klasy_SMS(상가[INDEKS]), Nazwa = odwołanie_nazwa(stała_SEKUNDA_WARTOŚĆ[INDEKS]), format_WARTOŚĆ = typ_referencyjny(stała_SEKUNDA_WARTOŚĆ[INDEKS]);
        if (błąd) return;
        if (기본호출(właściciel_WARTOŚĆ, Nazwa, format_WARTOŚĆ, polecenie)) return;
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
        int Klasa_Definicja = ZNAJDŹ_Klasa_Definicja(właściciel_WARTOŚĆ); if (Klasa_Definicja < 0 || błąd) return;
        int Plik_INDEKS = ZNAJDŹ_metoda(Klasa_Definicja, Nazwa, format_WARTOŚĆ);
        if (Plik_INDEKS < 0) {
            for (int kod_znaku = Klasa_Definicja, wpis_ILE_LICZB = 0; kod_znaku >= 0 && wpis_ILE_LICZB < 16; wpis_ILE_LICZB++, kod_znaku = nadrzędny_Klasa(kod_znaku))
                if (Word_SMS(Klasa_Definicja_nadrzędny[kod_znaku], "java/lang/Thread")) { 가닥호출(Nazwa, format_WARTOŚĆ, polecenie); return; }
            awaria_WARTOŚĆ("NoSuchMethodError"); return;
        }
        if (((metoda_dostęp[Plik_INDEKS] & 8) != 0) != (polecenie == 184)) { awaria_WARTOŚĆ("method static/instance mismatch"); return; }
        if (polecenie == 184) { if (!inicjuj(metoda_właściciel[Plik_INDEKS], kadr_instrukcja[kadr_INDEKS])) return; }
        else {
            int 읽는자리 = kadr_Stos[kadr_INDEKS] - metoda_argument_ILE_LICZB[Plik_INDEKS];
            if (읽는자리 < 0 || operand_Stos_TYP[kadr_INDEKS * 128 + 읽는자리] != 2) { awaria_WARTOŚĆ("invalid method receiver"); return; }
            int obiekt_odwołanie = operand_Stos_WARTOŚĆ[kadr_INDEKS * 128 + 읽는자리];
            if (!systemy_informacyjne_prawidłowy_obiekt(obiekt_odwołanie)) return;
            if (sterta_WARTOŚĆ[obiekt_odwołanie] < 32 || !종포함(sterta_WARTOŚĆ[obiekt_odwołanie] - 32, właściciel_WARTOŚĆ)) { awaria_WARTOŚĆ("method receiver type mismatch"); return; }
            if (polecenie != 183) Plik_INDEKS = ZNAJDŹ_metoda(sterta_WARTOŚĆ[obiekt_odwołanie] - 32, Nazwa, format_WARTOŚĆ);
        }
        if (Plik_INDEKS < 0 || (metoda_dostęp[Plik_INDEKS] & 0x400) != 0) { awaria_WARTOŚĆ("AbstractMethodError"); return; }
        int blokada_odwołanie = 0;
        if ((metoda_dostęp[Plik_INDEKS] & 32) != 0) {
            if (polecenie == 184) { int kod_znaku = metoda_właściciel[Plik_INDEKS]; if (Klasa_blokada[kod_znaku] == 0) Klasa_blokada[kod_znaku] = przydzielić_Pamięć(8, 0); blokada_odwołanie = Klasa_blokada[kod_znaku]; }
            else blokada_odwołanie = operand_Stos_WARTOŚĆ[kadr_INDEKS * 128 + kadr_Stos[kadr_INDEKS] - metoda_argument_ILE_LICZB[Plik_INDEKS]];
            if (!잠금얻기(blokada_odwołanie)) { if (!błąd) kadr_stanowisko[kadr_INDEKS] = kadr_instrukcja[kadr_INDEKS]; return; }
        }
        호출(Plik_INDEKS); if (!błąd) kadr_blokada[kadr_INDEKS] = blokada_odwołanie;
    }
    static boolean 배열저장가능(int TABLICA_odwołanie, int dane_WARTOŚĆ) {
        if (dane_WARTOŚĆ == 0 || element_tablicy[TABLICA_odwołanie] == 0) return true;
        boolean 성공여부 = element_tablicy[TABLICA_odwołanie] == -1 ? (dane_WARTOŚĆ > 0 && dane_WARTOŚĆ < sterta_Koniec_stanowisko && sterta_WARTOŚĆ[dane_WARTOŚĆ] == 1) : 맞는객체(dane_WARTOŚĆ, element_tablicy[TABLICA_odwołanie]);
        if (!성공여부 && !błąd) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int TABLICA_gniazdo(int odwołanie, int indeks_dolny_WARTOŚĆ, int TYP_WARTOŚĆ) {
        if (!obiekt_WARTOŚĆ(odwołanie, TYP_WARTOŚĆ)) return 0;
        if (indeks_dolny_WARTOŚĆ < 0 || indeks_dolny_WARTOŚĆ >= sterta_WARTOŚĆ[odwołanie + 1]) { awaria_WARTOŚĆ("ArrayIndexOutOfBoundsException"); return 0; }
        return odwołanie + 2 + indeks_dolny_WARTOŚĆ;
    }
    static void Wykonaj_polecenie() {
        int 남음 = 500000, fragment_WARTOŚĆ_652d4b53 = 100;
        while (true) {
            if (błąd) { if (던진객체 != 0) uchwyt_wyjątek(); if (błąd || kadr_INDEKS < bieżący_wątek * 32) break; }
            if (kadr_INDEKS < bieżący_wątek * 32 || żądanie_zmiany || --fragment_WARTOŚĆ_652d4b53 == 0) { if (!zmiana_wątek()) break; fragment_WARTOŚĆ_652d4b53 = 100; }
            if (kadr_INDEKS == 0 && Klasa_Definicja_Stan[wpis_Klasa_Definicja] != 2 && !inicjuj(wpis_Klasa_Definicja, kadr_stanowisko[kadr_INDEKS])) continue;
            if (kadr_INDEKS == bieżący_wątek * 32 && bieżący_wątek != 0 && (metoda_dostęp[kadr_metoda[kadr_INDEKS]] & 32) != 0 && kadr_blokada[kadr_INDEKS] == 0) {
                int obiekt_odwołanie = wątek_cel[bieżący_wątek]; if (!잠금얻기(obiekt_odwołanie)) { if (błąd) break; continue; } kadr_blokada[kadr_INDEKS] = obiekt_odwołanie;
            }
            잠시수 = 0;
            if (--남음 == 0) { awaria_WARTOŚĆ("instruction limit (500000)"); break; }
            int Uruchom_2 = kadr_stanowisko[kadr_INDEKS]; kadr_instrukcja[kadr_INDEKS] = Uruchom_2; int WARTOŚĆ = 명바();
            if (błąd) break;
            if (WARTOŚĆ == 0) continue;
            if (WARTOŚĆ == 1) { 넣기(0, 2); continue; }
            if (WARTOŚĆ >= 2 && WARTOŚĆ <= 8) { 넣기(WARTOŚĆ - 3, 1); continue; }
            if (WARTOŚĆ == 16) { 넣기((byte)명바(), 1); continue; }
            if (WARTOŚĆ == 17) { 넣기((short)명짧(), 1); continue; }
            if (WARTOŚĆ == 18 || WARTOŚĆ == 19) {
                int identyfikator = metoda_właściciel[kadr_metoda[kadr_INDEKS]] * 512 + (WARTOŚĆ == 18 ? 명바() : 명짧());
                if (identyfikator <= 0 || identyfikator >= stała_tag.length) awaria_WARTOŚĆ("invalid ldc constant");
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
            if (WARTOŚĆ == 46 || WARTOŚĆ >= 50 && WARTOŚĆ <= 53) {
                int wpis_stanowisko = 빼기(1), obiekt_odwołanie = 빼기(2), obszar_KOD = WARTOŚĆ == 46 ? 2 : WARTOŚĆ == 50 ? 3 : WARTOŚĆ == 51 ? 20 : WARTOŚĆ == 52 ? 22 : 23;
                if (WARTOŚĆ == 51 && obiekt_odwołanie > 0 && obiekt_odwołanie < sterta_Koniec_stanowisko && sterta_WARTOŚĆ[obiekt_odwołanie] == 21) obszar_KOD = 21;
                int 읽는자리 = TABLICA_gniazdo(obiekt_odwołanie, wpis_stanowisko, obszar_KOD); if (!błąd) 넣기(sterta_WARTOŚĆ[읽는자리], WARTOŚĆ == 50 ? 2 : 1); continue;
            }
            if (WARTOŚĆ == 79 || WARTOŚĆ >= 83 && WARTOŚĆ <= 86) {
                int wpis_odwołanie = 빼기(WARTOŚĆ == 83 ? 2 : 1), wpis_stanowisko = 빼기(1), obiekt_odwołanie = 빼기(2), obszar_KOD = WARTOŚĆ == 79 ? 2 : WARTOŚĆ == 83 ? 3 : WARTOŚĆ == 84 ? 20 : WARTOŚĆ == 85 ? 22 : 23;
                if (WARTOŚĆ == 84 && obiekt_odwołanie > 0 && obiekt_odwołanie < sterta_Koniec_stanowisko && sterta_WARTOŚĆ[obiekt_odwołanie] == 21) obszar_KOD = 21;
                int 읽는자리 = TABLICA_gniazdo(obiekt_odwołanie, wpis_stanowisko, obszar_KOD);
                if (!błąd && obszar_KOD == 3 && !배열저장가능(obiekt_odwołanie, wpis_odwołanie)) continue;
                if (!błąd) sterta_WARTOŚĆ[읽는자리] = obszar_KOD == 20 ? (byte)wpis_odwołanie : obszar_KOD == 21 ? wpis_odwołanie & 1 : obszar_KOD == 22 ? (char)wpis_odwołanie : obszar_KOD == 23 ? (short)wpis_odwołanie : wpis_odwołanie;
                continue;
            }
            if (WARTOŚĆ >= 87 && WARTOŚĆ <= 95) { Stos_instrukcja(WARTOŚĆ); continue; }
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
            if (WARTOŚĆ >= 178 && WARTOŚĆ <= 181) { 필드호출(명상수(), WARTOŚĆ, Uruchom_2); continue; }
            if (WARTOŚĆ >= 182 && WARTOŚĆ <= 185) {
                int 부호값 = 명상수();
                if (WARTOŚĆ == 185) { int suma_ILE_LICZB = 명바(); if (suma_ILE_LICZB == 0 || 명바() != 0) { awaria_WARTOŚĆ("invalid invokeinterface operands"); continue; } }
                Połącz_metoda(부호값, WARTOŚĆ); continue;
            }
            if (WARTOŚĆ == 187) { 새객체(nazwa_klasy_SMS(명상수()), Uruchom_2); continue; }
            if (WARTOŚĆ == 188 || WARTOŚĆ == 189) {
                int obszar_KOD = 3, składnik = 0;
                if (WARTOŚĆ == 188) { int 임시값 = 명바(); obszar_KOD = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else składnik = nazwa_klasy_SMS(명상수());
                if (obszar_KOD == 0) { awaria_WARTOŚĆ("unsupported primitive array type"); continue; }
                int prawidłowy_długość = 빼기(1), obiekt_odwołanie = przydzielić_Pamięć(obszar_KOD, prawidłowy_długość); if (!błąd) element_tablicy[obiekt_odwołanie] = składnik; 넣기(obiekt_odwołanie, 2); continue;
            }
            if (WARTOŚĆ == 190) {
                int obiekt_odwołanie = 빼기(2);
                if (systemy_informacyjne_prawidłowy_obiekt(obiekt_odwołanie)) { int Porównanie_stanowisko = sterta_WARTOŚĆ[obiekt_odwołanie]; if (Porównanie_stanowisko != 2 && Porównanie_stanowisko != 3 && (Porównanie_stanowisko < 20 || Porównanie_stanowisko > 23)) awaria_WARTOŚĆ("not an array"); else 넣기(sterta_WARTOŚĆ[obiekt_odwołanie + 1], 1); }
                continue;
            }
            if (WARTOŚĆ == 191) {
                int obiekt_odwołanie = 빼기(2); if (systemy_informacyjne_prawidłowy_obiekt(obiekt_odwołanie)) { if (sterta_WARTOŚĆ[obiekt_odwołanie] != 9) awaria_WARTOŚĆ("athrow requires supported Throwable"); else { 던진객체 = obiekt_odwołanie; błąd = true; } }
                continue;
            }
            if (WARTOŚĆ == 192 || WARTOŚĆ == 193) {
                int nazwa_stała = nazwa_klasy_SMS(명상수()), obiekt_odwołanie = 빼기(2); boolean set = 맞는객체(obiekt_odwołanie, nazwa_stała);
                if (WARTOŚĆ == 193) 넣기(obiekt_odwołanie != 0 && set ? 1 : 0, 1);
                else { if (!set && !błąd) awaria_WARTOŚĆ("ClassCastException"); 넣기(obiekt_odwołanie, 2); }
                continue;
            }
            if (WARTOŚĆ == 170 || WARTOŚĆ == 171) {
                int 읽는자리 = Uruchom_2 + 1, Plik_INDEKS = kadr_metoda[kadr_INDEKS], Klucz_odwołanie = 빼기(1);
                while ((읽는자리 - metoda_START[Plik_INDEKS]) % 4 != 0) 읽는자리++;
                int cel_ADRES = stanowisko_liczba_całkowita(읽는자리);
                if (WARTOŚĆ == 170) { int 낮은값 = stanowisko_liczba_całkowita(읽는자리 + 4), 높은값 = stanowisko_liczba_całkowita(읽는자리 + 8); if (Klucz_odwołanie >= 낮은값 && Klucz_odwołanie <= 높은값) cel_ADRES = stanowisko_liczba_całkowita(읽는자리 + 12 + (Klucz_odwołanie - 낮은값) * 4); }
                else { int suma_ILE_LICZB = stanowisko_liczba_całkowita(읽는자리 + 4); for (int Loop_INDEKS = 0; Loop_INDEKS < suma_ILE_LICZB; Loop_INDEKS++) if (stanowisko_liczba_całkowita(읽는자리 + 8 + Loop_INDEKS * 8) == Klucz_odwołanie) cel_ADRES = stanowisko_liczba_całkowita(읽는자리 + 12 + Loop_INDEKS * 8); }
                przenosić_WARTOŚĆ(Uruchom_2 + cel_ADRES); continue;
            }
            if (WARTOŚĆ == 200) { przenosić_WARTOŚĆ(Uruchom_2 + stanowisko_liczba_całkowita(Uruchom_2 + 1)); continue; }
            if (WARTOŚĆ == 194 || WARTOŚĆ == 195) {
                int obiekt_odwołanie = 빼기(2);
                if (WARTOŚĆ == 195) wersja_blokada(obiekt_odwołanie);
                else if (!잠금얻기(obiekt_odwołanie) && !błąd) { 넣기(obiekt_odwołanie, 2); kadr_stanowisko[kadr_INDEKS] = Uruchom_2; }
                continue;
            }
            if (WARTOŚĆ == 196) {
                int polecenie_KOD = 명바(), wpis_stanowisko = 명짧();
                if (polecenie_KOD == 21 || polecenie_KOD == 25) 지역읽기(wpis_stanowisko, polecenie_KOD == 21 ? 1 : 2);
                else if (polecenie_KOD == 54 || polecenie_KOD == 58) zapis_lokalny(wpis_stanowisko, polecenie_KOD == 54 ? 1 : 2);
                else if (polecenie_KOD == 132) { int CZY_RÓWNE_WARTOŚĆ = (short)명짧(); 지역읽기(wpis_stanowisko, 1); 넣기(빼기(1) + CZY_RÓWNE_WARTOŚĆ, 1); zapis_lokalny(wpis_stanowisko, 1); }
                else awaria_WARTOŚĆ("unsupported wide opcode");
                continue;
            }
            awaria_WARTOŚĆ("unsupported bytecode");
        }
    }
    static int ZNAJDŹ_Klasa_Definicja(int Nazwa) {
        for (int Loop_INDEKS = 0; Loop_INDEKS < Klasa_Definicja_ILE_LICZB; Loop_INDEKS++) if (Klasa_Definicja_nazwa[Loop_INDEKS] != 0 && 같은말(Klasa_Definicja_nazwa[Loop_INDEKS], Nazwa)) return Loop_INDEKS;
        return akta_Klasa_Definicja(stała_SMS(Nazwa));
    }
    static int akta_Klasa_Definicja(int nazwa_ciąg) {
        if (!obiekt_WARTOŚĆ(nazwa_ciąg, 1)) return -1;
        int długość_WARTOŚĆ = sterta_WARTOŚĆ[nazwa_ciąg + 1];
        if (długość_WARTOŚĆ < 1 || długość_WARTOŚĆ > 505 || Klasa_Definicja_ILE_LICZB == 16) { awaria_WARTOŚĆ("class name/count limit"); return -1; }
        for (int Loop_INDEKS = 0; Loop_INDEKS < długość_WARTOŚĆ; Loop_INDEKS++) { int kod_znaku = sterta_WARTOŚĆ[nazwa_ciąg + 2 + Loop_INDEKS]; nazwa_pliku_SMS[Loop_INDEKS] = kod_znaku == '/' ? '.' : kod_znaku; }
        nazwa_pliku_SMS[długość_WARTOŚĆ] = '.'; nazwa_pliku_SMS[długość_WARTOŚĆ + 1] = 'c'; nazwa_pliku_SMS[długość_WARTOŚĆ + 2] = 'l'; nazwa_pliku_SMS[długość_WARTOŚĆ + 3] = 'a'; nazwa_pliku_SMS[długość_WARTOŚĆ + 4] = 's'; nazwa_pliku_SMS[długość_WARTOŚĆ + 5] = 's'; nazwa_pliku_SMS[długość_WARTOŚĆ + 6] = 0;
        int Rozmiar = przestrzeń_użytkownika.파일읽기(nazwa_pliku_SMS, plik_tymczasowy);
        if (Rozmiar < 0) { awaria_WARTOŚĆ("ClassNotFoundException"); return -1; }
        int Klasa_Definicja = Klasa_Definicja_ILE_LICZB++; Klasa_Definicja_zmienić_rozmiar[Klasa_Definicja] = Rozmiar;
        for (int Loop_INDEKS = 0; Loop_INDEKS < Rozmiar; Loop_INDEKS++) nazwa_pliku[Klasa_Definicja * 16384 + Loop_INDEKS] = plik_tymczasowy[Loop_INDEKS];
        클래스읽기(Klasa_Definicja); if (błąd) return -1;
        int rzeczywisty_dane = stała_SMS(Klasa_Definicja_nazwa[Klasa_Definicja]);
        if (!teksty_równe(rzeczywisty_dane, nazwa_ciąg, true)) { awaria_WARTOŚĆ("class name does not match file"); return -1; }
        int nadrzędny_WARTOŚĆ = Klasa_Definicja_nadrzędny[Klasa_Definicja];
        if (nadrzędny_WARTOŚĆ != 0 && !Word_SMS(nadrzędny_WARTOŚĆ, "java/lang/Object") && !Word_SMS(nadrzędny_WARTOŚĆ, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 다시 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = ZNAJDŹ_Klasa_Definicja(nadrzędny_WARTOŚĆ);
            if (błąd || 위 < 0) return -1;
            int 읽는자리 = 위, etap_ILE_LICZB = 0;
            while (읽는자리 >= 0 && etap_ILE_LICZB++ < 16) {
                if (읽는자리 == Klasa_Definicja) { awaria_WARTOŚĆ("cyclic inheritance"); return -1; }
                읽는자리 = nadrzędny_Klasa(읽는자리);
            }
            int 시작변위 = Klasa_gniazdo_ILE_LICZB[위];
            for (int Plik_INDEKS = 0; Plik_INDEKS < gniazdo_ILE_LICZB; Plik_INDEKS++) if (gniazdo_właściciel[Plik_INDEKS] == Klasa_Definicja && (gniazdo_Uprawnienia[Plik_INDEKS] & 8) == 0) gniazdo_stanowisko[Plik_INDEKS] += 시작변위;
            Klasa_gniazdo_ILE_LICZB[Klasa_Definicja] += 시작변위;
        }
        return Klasa_Definicja;
    }
    static int nadrzędny_Klasa(int Klasa_Definicja) {
        int Nazwa = Klasa_Definicja_nadrzędny[Klasa_Definicja];
        for (int Loop_INDEKS = 0; Loop_INDEKS < Klasa_Definicja_ILE_LICZB; Loop_INDEKS++) if (Nazwa != 0 && Klasa_Definicja_nazwa[Loop_INDEKS] != 0 && 같은말(Klasa_Definicja_nazwa[Loop_INDEKS], Nazwa)) return Loop_INDEKS;
        return -1;
    }
    static int ZNAJDŹ_metoda(int Klasa_Definicja, int Nazwa, int format_WARTOŚĆ) {
        for (int 깊이 = 0; Klasa_Definicja >= 0 && 깊이 < 16; 깊이++, Klasa_Definicja = nadrzędny_Klasa(Klasa_Definicja)) {
            for (int Loop_INDEKS = 0; Loop_INDEKS < metoda_ILE_LICZB; Loop_INDEKS++) if (metoda_właściciel[Loop_INDEKS] == Klasa_Definicja && 같은말(metoda_nazwa_SMS[Loop_INDEKS], Nazwa) && 같은말(metoda_TYP[Loop_INDEKS], format_WARTOŚĆ)) return Loop_INDEKS;
        }
        return -1;
    }
    static int nazwa_metoda(int Klasa_Definicja, String Nazwa, String format_WARTOŚĆ) {
        for (int 깊이 = 0; Klasa_Definicja >= 0 && 깊이 < 16; 깊이++, Klasa_Definicja = nadrzędny_Klasa(Klasa_Definicja))
            for (int Loop_INDEKS = 0; Loop_INDEKS < metoda_ILE_LICZB; Loop_INDEKS++) if (metoda_właściciel[Loop_INDEKS] == Klasa_Definicja && Word_SMS(metoda_nazwa_SMS[Loop_INDEKS], Nazwa) && Word_SMS(metoda_TYP[Loop_INDEKS], format_WARTOŚĆ)) return Loop_INDEKS;
        return -1;
    }
    static int TYP_Rodzaj(int Nazwa) { return nazwa_pliku[상가[Nazwa]] == 'L' || nazwa_pliku[상가[Nazwa]] == '[' ? 2 : 1; }
    static boolean inicjuj(int Klasa_Definicja, int polecenie_START) {
        if (Klasa_Definicja < 0 || błąd) return false;
        if (Klasa_Definicja_Stan[Klasa_Definicja] == 3) { awaria_WARTOŚĆ("NoClassDefFoundError: initialization failed"); return false; }
        if (Klasa_Definicja_Stan[Klasa_Definicja] == 1 && Klasa_wątek[Klasa_Definicja] != bieżący_wątek) { kadr_stanowisko[kadr_INDEKS] = polecenie_START; żądanie_zmiany = true; return false; }
        if (Klasa_Definicja_Stan[Klasa_Definicja] != 0) return true;
        int 위 = nadrzędny_Klasa(Klasa_Definicja);
        if (위 >= 0 && !inicjuj(위, polecenie_START)) return false;
        Klasa_Definicja_Stan[Klasa_Definicja] = 1; Klasa_wątek[Klasa_Definicja] = bieżący_wątek;
        if (inicjuj_Klasa_Definicja[Klasa_Definicja] != 0) {
            kadr_stanowisko[kadr_INDEKS] = polecenie_START;
            호출(inicjuj_Klasa_Definicja[Klasa_Definicja] - 1); if (!błąd) inicjuj_kadr[kadr_INDEKS] = Klasa_Definicja + 1;
            return false;
        }
        Klasa_Definicja_Stan[Klasa_Definicja] = 2; return true;
    }
    static void 필드호출(int INDEKS, int polecenie, int Uruchom_2) {
        if (!czek_stała(INDEKS, 9)) return;
        int właściciel_WARTOŚĆ = nazwa_klasy_SMS(상가[INDEKS]), Nazwa = odwołanie_nazwa(stała_SEKUNDA_WARTOŚĆ[INDEKS]), format_WARTOŚĆ = typ_referencyjny(stała_SEKUNDA_WARTOŚĆ[INDEKS]);
        if (Word_SMS(właściciel_WARTOŚĆ, "java/lang/System") && (Word_SMS(Nazwa, "out") || Word_SMS(Nazwa, "err")) && Word_SMS(format_WARTOŚĆ, "Ljava/io/PrintStream;") && polecenie == 178) { 넣기(-1, 2); return; }
        int Klasa_Definicja = ZNAJDŹ_Klasa_Definicja(właściciel_WARTOŚĆ); if (Klasa_Definicja < 0 || błąd) return;
        int 찾음 = -1;
        for (int 읽는자리 = Klasa_Definicja, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = nadrzędny_Klasa(읽는자리))
            for (int Plik_INDEKS = 0; Plik_INDEKS < gniazdo_ILE_LICZB; Plik_INDEKS++) if (gniazdo_właściciel[Plik_INDEKS] == 읽는자리 && 같은말(gniazdo_nazwa[Plik_INDEKS], Nazwa) && 같은말(gniazdo_TYP[Plik_INDEKS], format_WARTOŚĆ)) 찾음 = Plik_INDEKS;
        if (찾음 < 0) { awaria_WARTOŚĆ("NoSuchFieldError"); return; }
        boolean statyczny_WARTOŚĆ = polecenie == 178 || polecenie == 179;
        if (statyczny_WARTOŚĆ != ((gniazdo_Uprawnienia[찾음] & 8) != 0)) { awaria_WARTOŚĆ("field static/instance mismatch"); return; }
        if (statyczny_WARTOŚĆ && !inicjuj(gniazdo_właściciel[찾음], Uruchom_2)) return;
        int TYP_WARTOŚĆ = TYP_Rodzaj(format_WARTOŚĆ), WARTOŚĆ = 0;
        if (polecenie == 179 || polecenie == 181) WARTOŚĆ = 빼기(TYP_WARTOŚĆ);
        if (statyczny_WARTOŚĆ) { if (polecenie == 178) 넣기(gniazdo_dane[찾음], TYP_WARTOŚĆ); else if (!błąd) gniazdo_dane[찾음] = WARTOŚĆ; return; }
        int obiekt_odwołanie = 빼기(2);
        if (!systemy_informacyjne_prawidłowy_obiekt(obiekt_odwołanie)) return;
        if (sterta_WARTOŚĆ[obiekt_odwołanie] < 32 || !종포함(sterta_WARTOŚĆ[obiekt_odwołanie] - 32, właściciel_WARTOŚĆ)) { awaria_WARTOŚĆ("field receiver type mismatch"); return; }
        int 보관칸 = obiekt_odwołanie + 2 + gniazdo_stanowisko[찾음];
        if (polecenie == 180) 넣기(sterta_WARTOŚĆ[보관칸], TYP_WARTOŚĆ);
        else if (!błąd) { sterta_WARTOŚĆ[보관칸] = WARTOŚĆ; sterta_odwołanie[보관칸] = TYP_WARTOŚĆ == 2 ? 1 : 0; }
    }
    static boolean 종포함(int Klasa_Definicja, int Nazwa) {
        for (int 중첩깊이 = 0; Klasa_Definicja >= 0 && 중첩깊이 < 16; 중첩깊이++, Klasa_Definicja = nadrzędny_Klasa(Klasa_Definicja)) {
            if (같은말(Klasa_Definicja_nazwa[Klasa_Definicja], Nazwa) || (Klasa_Definicja_nadrzędny[Klasa_Definicja] != 0 && 같은말(Klasa_Definicja_nadrzędny[Klasa_Definicja], Nazwa))) return true;
            for (int wewnętrzne_stanowisko = 0; wewnętrzne_stanowisko < Klasa_interfejs_ILE_LICZB[Klasa_Definicja]; wewnętrzne_stanowisko++) if (같은말(Klasa_interfejs[Klasa_Definicja * 16 + wewnętrzne_stanowisko], Nazwa)) return true;
        }
        return false;
    }
    static boolean teksty_równe(int 첫값, int bajt_dane, boolean ścieżka_2) {
        if (첫값 == bajt_dane) return true;
        if (첫값 <= 0 || bajt_dane <= 0 || sterta_WARTOŚĆ[첫값] != 1 || sterta_WARTOŚĆ[bajt_dane] != 1 || sterta_WARTOŚĆ[첫값 + 1] != sterta_WARTOŚĆ[bajt_dane + 1]) return false;
        for (int Loop_INDEKS = 0; Loop_INDEKS < sterta_WARTOŚĆ[첫값 + 1]; Loop_INDEKS++) {
            int współrzędna_X = sterta_WARTOŚĆ[첫값 + 2 + Loop_INDEKS], Y_współrzędna = sterta_WARTOŚĆ[bajt_dane + 2 + Loop_INDEKS];
            if (ścieżka_2) { if (współrzędna_X == '.') współrzędna_X = '/'; if (Y_współrzędna == '.') Y_współrzędna = '/'; }
            if (współrzędna_X != Y_współrzędna) return false;
        }
        return true;
    }
    static boolean systemy_informacyjne_prawidłowy_obiekt(int obiekt_odwołanie) {
        if (obiekt_odwołanie == 0) { awaria_WARTOŚĆ("NullPointerException"); return false; }
        if (obiekt_odwołanie < 1 || obiekt_odwołanie >= sterta_Koniec_stanowisko || 힙폭[obiekt_odwołanie] < 2 || sterta_WARTOŚĆ[obiekt_odwołanie] == 0) { awaria_WARTOŚĆ("invalid object reference"); return false; }
        return true;
    }
    static void chronić_WARTOŚĆ(int obiekt_odwołanie) {
        if (obiekt_odwołanie > 0 && obiekt_odwołanie < sterta_Koniec_stanowisko && 힙폭[obiekt_odwołanie] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = obiekt_odwołanie;
    }
    static void program_WARTOŚĆ(int obiekt_odwołanie) {
        if (obiekt_odwołanie > 0 && obiekt_odwołanie < sterta_Koniec_stanowisko && 힙폭[obiekt_odwołanie] >= 2 && sterta_WARTOŚĆ[obiekt_odwołanie] != 0 && 힙표시[obiekt_odwołanie] == 0) {
            힙표시[obiekt_odwołanie] = 1; 표시대기[wyświetlać_ILE_LICZB++] = obiekt_odwołanie;
        }
    }
    static void 수거() {
        wyświetlać_ILE_LICZB = 0; Kolekcja_ILE_LICZB++;
        for (int czek_stanowisko = 1; czek_stanowisko < sterta_Koniec_stanowisko; czek_stanowisko += 힙폭[czek_stanowisko]) 힙표시[czek_stanowisko] = 0;
        for (int Loop_INDEKS = 0; Loop_INDEKS < ciąg_odwołanie.length; Loop_INDEKS++) program_WARTOŚĆ(ciąg_odwołanie[Loop_INDEKS]);
        for (int Loop_INDEKS = 0; Loop_INDEKS < gniazdo_ILE_LICZB; Loop_INDEKS++) if ((gniazdo_Uprawnienia[Loop_INDEKS] & 8) != 0 && TYP_Rodzaj(gniazdo_TYP[Loop_INDEKS]) == 2) program_WARTOŚĆ(gniazdo_dane[Loop_INDEKS]);
        for (int 임시값 = 0; 임시값 < liczba_wątków; 임시값++) {
            program_WARTOŚĆ(wątek_obiekt[임시값]); program_WARTOŚĆ(wątek_cel[임시값]);
            int 꼭대기자리 = 임시값 == bieżący_wątek ? kadr_INDEKS : wątek_kadr[임시값];
            for (int Plik_INDEKS = 임시값 * 32; Plik_INDEKS <= 꼭대기자리; Plik_INDEKS++) {
                for (int wewnętrzne_stanowisko = 0; wewnętrzne_stanowisko < 함수지역[kadr_metoda[Plik_INDEKS]]; wewnętrzne_stanowisko++) if (lokalny_TYP[Plik_INDEKS * 128 + wewnętrzne_stanowisko] == 2) program_WARTOŚĆ(lokalny_WARTOŚĆ[Plik_INDEKS * 128 + wewnętrzne_stanowisko]);
                for (int wewnętrzne_stanowisko = 0; wewnętrzne_stanowisko < kadr_Stos[Plik_INDEKS]; wewnętrzne_stanowisko++) if (operand_Stos_TYP[Plik_INDEKS * 128 + wewnętrzne_stanowisko] == 2) program_WARTOŚĆ(operand_Stos_WARTOŚĆ[Plik_INDEKS * 128 + wewnętrzne_stanowisko]);
            }
        }
        for (int Loop_INDEKS = 0; Loop_INDEKS < 화면참조.length; Loop_INDEKS++) program_WARTOŚĆ(화면참조[Loop_INDEKS]);
        for (int Loop_INDEKS = 0; Loop_INDEKS < 나중수; Loop_INDEKS++) program_WARTOŚĆ(나중실행[Loop_INDEKS]);
        for (int Loop_INDEKS = 0; Loop_INDEKS < Store_liczba_całkowita.length; Loop_INDEKS++) program_WARTOŚĆ(Store_liczba_całkowita[Loop_INDEKS]);
        for (int Loop_INDEKS = 0; Loop_INDEKS < Klasa_Definicja_ILE_LICZB; Loop_INDEKS++) program_WARTOŚĆ(Klasa_blokada[Loop_INDEKS]);
        for (int czek_stanowisko = 1; czek_stanowisko < sterta_Koniec_stanowisko; czek_stanowisko += 힙폭[czek_stanowisko]) if (잠금깊이[czek_stanowisko] > 0) program_WARTOŚĆ(czek_stanowisko);
        program_WARTOŚĆ(던진객체);
        for (int Loop_INDEKS = 0; Loop_INDEKS < 잠시수; Loop_INDEKS++) program_WARTOŚĆ(잠시참조[Loop_INDEKS]);
        while (wyświetlać_ILE_LICZB > 0) {
            int obiekt_odwołanie = 표시대기[--wyświetlać_ILE_LICZB], obszar_KOD = sterta_WARTOŚĆ[obiekt_odwołanie];
            for (int Loop_INDEKS = obiekt_odwołanie + 2; Loop_INDEKS < obiekt_odwołanie + 힙폭[obiekt_odwołanie]; Loop_INDEKS++) if (obszar_KOD == 3 || obszar_KOD == 4 || sterta_odwołanie[Loop_INDEKS] != 0) program_WARTOŚĆ(sterta_WARTOŚĆ[Loop_INDEKS]);
        }
        for (int czek_stanowisko = 1; czek_stanowisko < sterta_Koniec_stanowisko; czek_stanowisko += 힙폭[czek_stanowisko]) if (힙표시[czek_stanowisko] == 0) sterta_WARTOŚĆ[czek_stanowisko] = 0;
        for (int czek_stanowisko = 1; czek_stanowisko < sterta_Koniec_stanowisko; czek_stanowisko += 힙폭[czek_stanowisko]) if (sterta_WARTOŚĆ[czek_stanowisko] == 0) {
            while (czek_stanowisko + 힙폭[czek_stanowisko] < sterta_Koniec_stanowisko && sterta_WARTOŚĆ[czek_stanowisko + 힙폭[czek_stanowisko]] == 0) { int Dalej_stanowisko = czek_stanowisko + 힙폭[czek_stanowisko]; 힙폭[czek_stanowisko] += 힙폭[Dalej_stanowisko]; 힙폭[Dalej_stanowisko] = 0; }
            if (czek_stanowisko + 힙폭[czek_stanowisko] == sterta_Koniec_stanowisko) { sterta_Koniec_stanowisko = czek_stanowisko; break; }
        }
    }
    static int 새기억(int Rodzaj_WARTOŚĆ, int długość_WARTOŚĆ) {
        if (długość_WARTOŚĆ < 0) { awaria_WARTOŚĆ("NegativeArraySizeException"); return 0; }
        if (długość_WARTOŚĆ > sterta_WARTOŚĆ.length - 3) { awaria_WARTOŚĆ("object heap exhausted"); return 0; }
        int 필요수 = długość_WARTOŚĆ + 2, obiekt_odwołanie = 0;
        if (필요수 <= sterta_WARTOŚĆ.length - sterta_Koniec_stanowisko) { obiekt_odwołanie = sterta_Koniec_stanowisko; sterta_Koniec_stanowisko += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < sterta_Koniec_stanowisko; 읽는자리 += 힙폭[읽는자리]) if (sterta_WARTOŚĆ[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { obiekt_odwołanie = 읽는자리; break; }
            if (obiekt_odwołanie != 0) {
                int 남은길이 = 힙폭[obiekt_odwołanie] - 필요수;
                if (남은길이 >= 2) { 힙폭[obiekt_odwołanie + 필요수] = 남은길이; sterta_WARTOŚĆ[obiekt_odwołanie + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= sterta_WARTOŚĆ.length - sterta_Koniec_stanowisko) { obiekt_odwołanie = sterta_Koniec_stanowisko; sterta_Koniec_stanowisko += 필요수; }
        }
        if (obiekt_odwołanie == 0) { awaria_WARTOŚĆ("object heap exhausted"); return 0; }
        for (int Loop_INDEKS = 0; Loop_INDEKS < 필요수; Loop_INDEKS++) { sterta_WARTOŚĆ[obiekt_odwołanie + Loop_INDEKS] = 0; sterta_odwołanie[obiekt_odwołanie + Loop_INDEKS] = 0; 힙폭[obiekt_odwołanie + Loop_INDEKS] = 0; }
        element_tablicy[obiekt_odwołanie] = 0;
        힙폭[obiekt_odwołanie] = 필요수; sterta_WARTOŚĆ[obiekt_odwołanie] = Rodzaj_WARTOŚĆ; sterta_WARTOŚĆ[obiekt_odwołanie + 1] = długość_WARTOŚĆ; chronić_WARTOŚĆ(obiekt_odwołanie); return obiekt_odwołanie;
    }
    static int wyjątek_Klasa(String nazwa_stała) {
        if (자바도구.같음(nazwa_stała, "java/lang/Throwable")) return 1;
        if (자바도구.같음(nazwa_stała, "java/lang/Exception")) return 2;
        if (자바도구.같음(nazwa_stała, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(nazwa_stała, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(nazwa_stała, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(nazwa_stała, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(nazwa_stała, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(nazwa_stała, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(nazwa_stała, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(nazwa_stała, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(nazwa_stała, "java/io/IOException")) return 11;
        if (자바도구.같음(nazwa_stała, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(nazwa_stała, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(nazwa_stała, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(nazwa_stała, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int wyjątek_stała(int Nazwa) {
        for (int Loop_INDEKS = 1; Loop_INDEKS <= 41; Loop_INDEKS++) if (Word_SMS(Nazwa, wyjątek_nazwa(Loop_INDEKS))) return Loop_INDEKS;
        return 0;
    }
    static String wyjątek_nazwa(int konto_WARTOŚĆ) {
        if (konto_WARTOŚĆ == 40) return "java/lang/InterruptedException";
        if (konto_WARTOŚĆ == 41) return "polski/własny/대기중단예외";
        if (konto_WARTOŚĆ == 39) return "java/net/SocketException";
        if (konto_WARTOŚĆ == 20) return "polski/własny/wyjątek";
        if (konto_WARTOŚĆ == 21) return "polski/własny/wykonanie_wyjątek";
        if (konto_WARTOŚĆ == 22) return "polski/własny/We_Wy_wyjątek";
        if (konto_WARTOŚĆ == 23) return "polski/własny/chwileczkę_TIMEOUT_wyjątek";
        if (konto_WARTOŚĆ == 24) return "polski/własny/ADRES_WYSZUKAJ_wyjątek";
        if (konto_WARTOŚĆ == 25) return "polski/własny/파일없음예외";
        if (konto_WARTOŚĆ == 26) return "polski/własny/komunikacja_wyjątek";
        if (konto_WARTOŚĆ == 27) return "polski/własny/nieważny_argument_wyjątek";
        if (konto_WARTOŚĆ == 28) return "polski/własny/identyfikator_format_awaria";
        if (konto_WARTOŚĆ == 29) return "polski/własny/범위예외";
        if (konto_WARTOŚĆ == 30) return "polski/własny/granice_tablicy_wyjątek";
        if (konto_WARTOŚĆ == 31) return "polski/własny/문자열범위예외";
        if (konto_WARTOŚĆ == 32) return "polski/własny/pusta_referencja_wyjątek";
        if (konto_WARTOŚĆ == 33) return "polski/własny/산술예외";
        if (konto_WARTOŚĆ == 34) return "polski/własny/Stan_wyjątek";
        if (konto_WARTOŚĆ == 35) return "polski/własny/TYP_koercja_wyjątek";
        if (konto_WARTOŚĆ == 36) return "polski/własny/negatywny_TABLICA_zmienić_rozmiar_awaria";
        if (konto_WARTOŚĆ == 37) return "polski/własny/TABLICA_Store_awaria";
        if (konto_WARTOŚĆ == 38) return "polski/własny/wątek_Stan_wyjątek";
        if (konto_WARTOŚĆ == 1) return "java/lang/Throwable"; if (konto_WARTOŚĆ == 2) return "java/lang/Exception";
        if (konto_WARTOŚĆ == 3) return "java/lang/RuntimeException"; if (konto_WARTOŚĆ == 4) return "java/lang/ArithmeticException";
        if (konto_WARTOŚĆ == 5) return "java/lang/NullPointerException"; if (konto_WARTOŚĆ == 6) return "java/lang/IndexOutOfBoundsException";
        if (konto_WARTOŚĆ == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (konto_WARTOŚĆ == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (konto_WARTOŚĆ == 9) return "java/lang/IllegalArgumentException"; if (konto_WARTOŚĆ == 10) return "java/lang/NumberFormatException";
        if (konto_WARTOŚĆ == 11) return "java/io/IOException"; if (konto_WARTOŚĆ == 12) return "java/io/FileNotFoundException";
        if (konto_WARTOŚĆ == 17) return "java/lang/ArrayStoreException";
        if (konto_WARTOŚĆ == 18) return "java/net/UnknownHostException";
        if (konto_WARTOŚĆ == 19) return "java/net/SocketTimeoutException";
        if (konto_WARTOŚĆ == 16) return "java/lang/IllegalThreadStateException";
        if (konto_WARTOŚĆ == 13) return "java/lang/IllegalStateException"; if (konto_WARTOŚĆ == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int wyjątek_nadrzędny(int konto_WARTOŚĆ) {
        if (konto_WARTOŚĆ == 40) return 2;
        if (konto_WARTOŚĆ == 41) return 40;
        if (konto_WARTOŚĆ == 39) return 11;
        if (konto_WARTOŚĆ == 1) return 0;
        if (konto_WARTOŚĆ == 2) return 1;
        if (konto_WARTOŚĆ == 3) return 2;
        if (konto_WARTOŚĆ == 4) return 3;
        if (konto_WARTOŚĆ == 5) return 3;
        if (konto_WARTOŚĆ == 6) return 3;
        if (konto_WARTOŚĆ == 7) return 6;
        if (konto_WARTOŚĆ == 8) return 6;
        if (konto_WARTOŚĆ == 9) return 3;
        if (konto_WARTOŚĆ == 10) return 9;
        if (konto_WARTOŚĆ == 11) return 2;
        if (konto_WARTOŚĆ == 12) return 11;
        if (konto_WARTOŚĆ == 13) return 3;
        if (konto_WARTOŚĆ == 14) return 3;
        if (konto_WARTOŚĆ == 15) return 3;
        if (konto_WARTOŚĆ == 16) return 9;
        if (konto_WARTOŚĆ == 17) return 3;
        if (konto_WARTOŚĆ == 18) return 11;
        if (konto_WARTOŚĆ == 19) return 11;
        if (konto_WARTOŚĆ == 20) return 2;
        if (konto_WARTOŚĆ == 21) return 3;
        if (konto_WARTOŚĆ == 22) return 11;
        if (konto_WARTOŚĆ == 23) return 22;
        if (konto_WARTOŚĆ == 24) return 22;
        if (konto_WARTOŚĆ == 25) return 22;
        if (konto_WARTOŚĆ == 26) return 22;
        if (konto_WARTOŚĆ == 27) return 9;
        if (konto_WARTOŚĆ == 28) return 27;
        if (konto_WARTOŚĆ == 29) return 6;
        if (konto_WARTOŚĆ == 30) return 29;
        if (konto_WARTOŚĆ == 31) return 29;
        if (konto_WARTOŚĆ == 32) return 5;
        if (konto_WARTOŚĆ == 33) return 4;
        if (konto_WARTOŚĆ == 34) return 13;
        if (konto_WARTOŚĆ == 35) return 14;
        if (konto_WARTOŚĆ == 36) return 15;
        if (konto_WARTOŚĆ == 37) return 17;
        if (konto_WARTOŚĆ == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int wartość_rzeczywista, int 요구값) {
        for (int 깊이 = 0; wartość_rzeczywista != 0 && 깊이 < 16; 깊이++, wartość_rzeczywista = wyjątek_nadrzędny(wartość_rzeczywista))
            if (wartość_rzeczywista == 요구값) return true;
        return false;
    }
    static void 예외던짐(int konto_WARTOŚĆ, String plik_README_odwołanie) {
        int obiekt_odwołanie = 새기억(9, 2); if (błąd) return;
        sterta_WARTOŚĆ[obiekt_odwołanie + 2] = konto_WARTOŚĆ; sterta_WARTOŚĆ[obiekt_odwołanie + 3] = host_znak(plik_README_odwołanie); sterta_odwołanie[obiekt_odwołanie + 3] = 1;
        던진객체 = obiekt_odwołanie; błąd = true;
    }
    static boolean 맞는객체(int obiekt_odwołanie, int Nazwa) {
        if (obiekt_odwołanie == 0) return true;
        if (!systemy_informacyjne_prawidłowy_obiekt(obiekt_odwołanie)) return false;
        int obszar_KOD = sterta_WARTOŚĆ[obiekt_odwołanie];
        if (Word_SMS(Nazwa, "java/lang/Object")) return true;
        if (obszar_KOD >= 32) return 종포함(obszar_KOD - 32, Nazwa);
        if (obszar_KOD == 9) { int cel_ADRES = wyjątek_stała(Nazwa); return cel_ADRES != 0 && 예외포함(sterta_WARTOŚĆ[obiekt_odwołanie + 2], cel_ADRES); }
        if (obszar_KOD == 1) return Word_SMS(Nazwa, "java/lang/String") || Word_SMS(Nazwa, "java/lang/CharSequence");
        if (obszar_KOD == 4) return Word_SMS(Nazwa, "java/lang/StringBuilder") || Word_SMS(Nazwa, "java/lang/CharSequence");
        if (obszar_KOD == 10) return Word_SMS(Nazwa, "java/util/ArrayList") || Word_SMS(Nazwa, "java/util/List");
        if (obszar_KOD == 11) return Word_SMS(Nazwa, "java/util/HashMap") || Word_SMS(Nazwa, "java/util/Map");
        if (obszar_KOD == 12) return Word_SMS(Nazwa, "java/lang/Integer") || Word_SMS(Nazwa, "java/lang/Number");
        if (obszar_KOD >= 24 && obszar_KOD <= 28 && sterta_WARTOŚĆ[obiekt_odwołanie + 13] != 0) return 한국어화면종(Nazwa) == obszar_KOD || Word_SMS(Nazwa, "polski/własny/화면구성요소");
        if (obszar_KOD >= 24 && obszar_KOD <= 28) return (한국어화면종(Nazwa) == 0 && 화면종(Nazwa) == obszar_KOD) || Word_SMS(Nazwa, "java/awt/Component") || Word_SMS(Nazwa, "java/awt/Container") || Word_SMS(Nazwa, "javax/swing/JComponent");
        if (obszar_KOD == 29) return Word_SMS(Nazwa, sterta_WARTOŚĆ[obiekt_odwołanie + 3] != 0 ? "polski/własny/akcja_powiadomienie" : "java/awt/event/ActionEvent");
        if (obszar_KOD == 30) return Word_SMS(Nazwa, "java/awt/FlowLayout") || Word_SMS(Nazwa, "java/awt/LayoutManager");
        if (obszar_KOD == 17) return Word_SMS(Nazwa, "java/net/Socket");
        if (obszar_KOD == 18) return Word_SMS(Nazwa, "java/net/ServerSocket");
        if (obszar_KOD == 19) return Word_SMS(Nazwa, sterta_WARTOŚĆ[obiekt_odwołanie + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (obszar_KOD == 14) return Word_SMS(Nazwa, "java/net/InetAddress");
        if (obszar_KOD == 15) return Word_SMS(Nazwa, "java/net/DatagramSocket");
        if (obszar_KOD == 16) return Word_SMS(Nazwa, "java/net/DatagramPacket");
        if (obszar_KOD == 13) return Word_SMS(Nazwa, sterta_WARTOŚĆ[obiekt_odwołanie + 3] != 0 ? "polski/własny/pracownik" : "java/lang/Thread");
        if (obszar_KOD == 2) return Word_SMS(Nazwa, "[I"); if (obszar_KOD == 20) return Word_SMS(Nazwa, "[B"); if (obszar_KOD == 21) return Word_SMS(Nazwa, "[Z");
        if (obszar_KOD == 22) return Word_SMS(Nazwa, "[C"); if (obszar_KOD == 23) return Word_SMS(Nazwa, "[S");
        if (obszar_KOD != 3) return false;
        if (Word_SMS(Nazwa, "[Ljava/lang/Object;")) return true;
        int składnik = element_tablicy[obiekt_odwołanie];
        if (składnik == -1) return Word_SMS(Nazwa, "[Ljava/lang/String;") || Word_SMS(Nazwa, "[Ljava/lang/CharSequence;");
        if (składnik == 0) return false;
        if (배열종비교(składnik, Nazwa)) return true;
        if ((Word_SMS(składnik, "java/lang/String") || Word_SMS(składnik, "java/lang/StringBuilder")) && Word_SMS(Nazwa, "[Ljava/lang/CharSequence;")) return true;
        for (int Loop_INDEKS = 0; Loop_INDEKS < Klasa_Definicja_ILE_LICZB; Loop_INDEKS++) if (같은말(Klasa_Definicja_nazwa[Loop_INDEKS], składnik)) {
            for (int kod_znaku = Loop_INDEKS, 중첩깊이 = 0; kod_znaku >= 0 && 중첩깊이 < 16; 중첩깊이++, kod_znaku = nadrzędny_Klasa(kod_znaku)) {
                if (배열종비교(Klasa_Definicja_nadrzędny[kod_znaku], Nazwa)) return true;
                for (int wewnętrzne_stanowisko = 0; wewnętrzne_stanowisko < Klasa_interfejs_ILE_LICZB[kod_znaku]; wewnętrzne_stanowisko++) if (배열종비교(Klasa_interfejs[kod_znaku * 16 + wewnętrzne_stanowisko], Nazwa)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int nazwa_stała, int deskryptor) {
        int czek_stanowisko = 상가[deskryptor], wpis_ILE_LICZB = stała_SEKUNDA_WARTOŚĆ[deskryptor];
        if (nazwa_stała == 0 || wpis_ILE_LICZB < 4 || nazwa_pliku[czek_stanowisko] != '[' || nazwa_pliku[czek_stanowisko + 1] != 'L' || nazwa_pliku[czek_stanowisko + wpis_ILE_LICZB - 1] != ';' || stała_SEKUNDA_WARTOŚĆ[nazwa_stała] != wpis_ILE_LICZB - 3) return false;
        for (int Loop_INDEKS = 0; Loop_INDEKS < wpis_ILE_LICZB - 3; Loop_INDEKS++) if (nazwa_pliku[상가[nazwa_stała] + Loop_INDEKS] != nazwa_pliku[czek_stanowisko + 2 + Loop_INDEKS]) return false;
        return true;
    }
    static void uchwyt_wyjątek() {
        if (던진객체 == 0) return;
        błąd = false;
        while (kadr_INDEKS >= bieżący_wątek * 32) {
            int Plik_INDEKS = kadr_metoda[kadr_INDEKS], 읽는자리 = kadr_instrukcja[kadr_INDEKS];
            for (int Loop_INDEKS = 0; Loop_INDEKS < 잡기수; Loop_INDEKS++) if (잡기함수[Loop_INDEKS] == Plik_INDEKS && 읽는자리 >= 잡기시작[Loop_INDEKS] && 읽는자리 < 잡기끝[Loop_INDEKS]
                && (잡기종[Loop_INDEKS] == 0 || 맞는객체(던진객체, 잡기종[Loop_INDEKS]))) {
                kadr_stanowisko[kadr_INDEKS] = 잡기위치[Loop_INDEKS]; kadr_Stos[kadr_INDEKS] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (inicjuj_kadr[kadr_INDEKS] != 0) Klasa_Definicja_Stan[inicjuj_kadr[kadr_INDEKS] - 1] = 3;
            if (kadr_blokada[kadr_INDEKS] != 0) { wersja_blokada(kadr_blokada[kadr_INDEKS]); kadr_blokada[kadr_INDEKS] = 0; }
            kadr_INDEKS--;
        }
        przestrzeń_użytkownika.Zapis("Uncaught ");
        if (sterta_WARTOŚĆ[던진객체] == 9) { przestrzeń_użytkownika.Zapis(wyjątek_nazwa(sterta_WARTOŚĆ[던진객체 + 2])); przestrzeń_użytkownika.Zapis(": "); zapis_SMS(sterta_WARTOŚĆ[던진객체 + 3]); }
        else przestrzeń_użytkownika.Zapis("user exception");
        przestrzeń_użytkownika.zapis_znak_WARTOŚĆ(10); 던진객체 = 0; błąd = true;
    }
    // 이 JVM의 operand_Stos 항목은 bieżący_towar category-1(int/reference)만 허용한다.
    static void Stos_instrukcja(int polecenie_KOD) {
        int 첫값 = 빼기(0), 첫형식 = zwracany_typ;
        if (polecenie_KOD == 87) return;
        if (polecenie_KOD == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int bajt_dane = 빼기(0), SEKUNDA_format = zwracany_typ;
        if (polecenie_KOD == 88) return;
        if (polecenie_KOD == 90) { 넣기(첫값, 첫형식); 넣기(bajt_dane, SEKUNDA_format); 넣기(첫값, 첫형식); return; }
        if (polecenie_KOD == 92) { 넣기(bajt_dane, SEKUNDA_format); 넣기(첫값, 첫형식); 넣기(bajt_dane, SEKUNDA_format); 넣기(첫값, 첫형식); return; }
        if (polecenie_KOD == 95) { 넣기(첫값, 첫형식); 넣기(bajt_dane, SEKUNDA_format); return; }
        int kod_znaku = 빼기(0), 셋째형식 = zwracany_typ;
        if (polecenie_KOD == 91) { 넣기(첫값, 첫형식); 넣기(kod_znaku, 셋째형식); 넣기(bajt_dane, SEKUNDA_format); 넣기(첫값, 첫형식); return; }
        if (polecenie_KOD == 93) { 넣기(bajt_dane, SEKUNDA_format); 넣기(첫값, 첫형식); 넣기(kod_znaku, 셋째형식); 넣기(bajt_dane, SEKUNDA_format); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = zwracany_typ;
        넣기(bajt_dane, SEKUNDA_format); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(kod_znaku, 셋째형식); 넣기(bajt_dane, SEKUNDA_format); 넣기(첫값, 첫형식);
    }
    static void 새객체(int nazwa_stała, int 시작점) {
        int obszar_KOD = 0, prawidłowy_długość = 0, wyjątek_odwołanie = wyjątek_stała(nazwa_stała);
        if (Word_SMS(nazwa_stała, "java/lang/StringBuilder")) { obszar_KOD = 4; prawidłowy_długość = 1; }
        if (Word_SMS(nazwa_stała, "java/io/FileInputStream")) { obszar_KOD = 5; prawidłowy_długość = 2; }
        if (Word_SMS(nazwa_stała, "java/io/FileOutputStream")) { obszar_KOD = 6; prawidłowy_długość = 2; }
        if (wyjątek_odwołanie != 0) { obszar_KOD = 9; prawidłowy_długość = 2; }
        if (Word_SMS(nazwa_stała, "java/util/ArrayList")) { obszar_KOD = 10; prawidłowy_długość = 2; }
        if (Word_SMS(nazwa_stała, "java/util/HashMap")) { obszar_KOD = 11; prawidłowy_długość = 2; }
        if (Word_SMS(nazwa_stała, "java/lang/Integer")) { obszar_KOD = 12; prawidłowy_długość = 1; }
        if (Word_SMS(nazwa_stała, "java/net/Socket")) { obszar_KOD = 17; prawidłowy_długość = 5; }
        if (Word_SMS(nazwa_stała, "java/net/ServerSocket")) { obszar_KOD = 18; prawidłowy_długość = 5; }
        if (Word_SMS(nazwa_stała, "java/net/DatagramSocket")) { obszar_KOD = 15; prawidłowy_długość = 3; }
        if (Word_SMS(nazwa_stała, "java/net/DatagramPacket")) { obszar_KOD = 16; prawidłowy_długość = 4; }
        if (Word_SMS(nazwa_stała, "java/lang/Thread") || Word_SMS(nazwa_stała, "polski/własny/pracownik")) { obszar_KOD = 13; prawidłowy_długość = 2; }
        if (Word_SMS(nazwa_stała, "java/lang/Object")) { obszar_KOD = 8; }
        if (obszar_KOD == 0 && 화면종(nazwa_stała) != 0) { obszar_KOD = 화면종(nazwa_stała); prawidłowy_długość = 12; }
        if (obszar_KOD == 0) {
            int kod_znaku = ZNAJDŹ_Klasa_Definicja(nazwa_stała); if (kod_znaku < 0 || błąd || !inicjuj(kod_znaku, 시작점)) return;
            obszar_KOD = 32 + kod_znaku; prawidłowy_długość = Klasa_gniazdo_ILE_LICZB[kod_znaku];
        }
        int obiekt_odwołanie = przydzielić_Pamięć(obszar_KOD, prawidłowy_długość); if (błąd) return;
        if (obszar_KOD == 13 && Word_SMS(nazwa_stała, "polski/własny/pracownik")) sterta_WARTOŚĆ[obiekt_odwołanie + 3] = 1;
        if (obszar_KOD >= 24 && obszar_KOD <= 28 && 한국어화면종(nazwa_stała) != 0) sterta_WARTOŚĆ[obiekt_odwołanie + 13] = 1;
        if (obszar_KOD == 5 || obszar_KOD == 6 || obszar_KOD == 15 || obszar_KOD == 17 || obszar_KOD == 18) sterta_WARTOŚĆ[obiekt_odwołanie + 2] = -1;
        if (obszar_KOD == 9) sterta_WARTOŚĆ[obiekt_odwołanie + 2] = wyjątek_odwołanie;
        넣기(obiekt_odwołanie, 2);
    }
    static boolean 값같음(int 첫값, int bajt_dane) {
        if (첫값 == bajt_dane) return true;
        if (첫값 == 0 || bajt_dane == 0 || 첫값 < 0 || bajt_dane < 0 || 첫값 >= sterta_Koniec_stanowisko || bajt_dane >= sterta_Koniec_stanowisko) return false;
        if (sterta_WARTOŚĆ[첫값] == 1 && sterta_WARTOŚĆ[bajt_dane] == 1) return teksty_równe(첫값, bajt_dane, false);
        return sterta_WARTOŚĆ[첫값] == 12 && sterta_WARTOŚĆ[bajt_dane] == 12 && sterta_WARTOŚĆ[첫값 + 2] == sterta_WARTOŚĆ[bajt_dane + 2];
    }
    static int SMS_fragment(int obiekt_odwołanie, int START_stanowisko, int Koniec_stanowisko) {
        if (!obiekt_WARTOŚĆ(obiekt_odwołanie, 1)) return 0;
        if (START_stanowisko < 0 || Koniec_stanowisko < START_stanowisko || Koniec_stanowisko > sterta_WARTOŚĆ[obiekt_odwołanie + 1]) { awaria_WARTOŚĆ("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = przydzielić_Pamięć(1, Koniec_stanowisko - START_stanowisko); if (błąd) return 0;
        for (int Loop_INDEKS = START_stanowisko; Loop_INDEKS < Koniec_stanowisko; Loop_INDEKS++) sterta_WARTOŚĆ[반환값 + 2 + Loop_INDEKS - START_stanowisko] = sterta_WARTOŚĆ[obiekt_odwołanie + 2 + Loop_INDEKS];
        return 반환값;
    }
    static int Dołącz_SMS(int 첫값, int bajt_dane) {
        if (!obiekt_WARTOŚĆ(첫값, 1) || !obiekt_WARTOŚĆ(bajt_dane, 1)) return 0;
        int wpis_ILE_LICZB = sterta_WARTOŚĆ[첫값 + 1], metoda_INDEKS = sterta_WARTOŚĆ[bajt_dane + 1], 반환값 = przydzielić_Pamięć(1, wpis_ILE_LICZB + metoda_INDEKS); if (błąd) return 0;
        for (int Loop_INDEKS = 0; Loop_INDEKS < wpis_ILE_LICZB; Loop_INDEKS++) sterta_WARTOŚĆ[반환값 + 2 + Loop_INDEKS] = sterta_WARTOŚĆ[첫값 + 2 + Loop_INDEKS];
        for (int Loop_INDEKS = 0; Loop_INDEKS < metoda_INDEKS; Loop_INDEKS++) sterta_WARTOŚĆ[반환값 + 2 + wpis_ILE_LICZB + Loop_INDEKS] = sterta_WARTOŚĆ[bajt_dane + 2 + Loop_INDEKS];
        return 반환값;
    }
    static boolean 기본호출(int właściciel, int nazwa_stała, int deskryptor_stała, int polecenie_KOD) {
        if (Word_SMS(właściciel, "polski/własny/실행인수") && polecenie_KOD == 184) {
            if (Word_SMS(nazwa_stała, "towar_ILE_LICZB") && Word_SMS(deskryptor_stała, "()I")) { 넣기(przestrzeń_użytkownika.인수개수() - 1, 1); return true; }
            if (Word_SMS(nazwa_stała, "tekst") && Word_SMS(deskryptor_stała, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= przestrzeń_użytkownika.인수개수() - 1) 예외던짐(29, "Wykonaj_polecenie argumenty 범위를 벗어났습니다");
                else 넣기(host_znak(przestrzeń_użytkownika.argumenty(순번 + 1)), 2);
                return true;
            }
            awaria_WARTOŚĆ("지원하지 않는 polski Wykonaj_polecenie argumenty 호출"); return true;
        }
        if (Word_SMS(właściciel, "polski/własny/pracownik")) { Proces_wątek(nazwa_stała, deskryptor_stała, polecenie_KOD, true); return true; }
        if (한국어화면소유(właściciel)) { 한국어화면호출(właściciel, nazwa_stała, deskryptor_stała, polecenie_KOD); return true; }
        if (화면소유(właściciel)) { 화면호출(właściciel, nazwa_stała, deskryptor_stała, polecenie_KOD); return true; }
        if (Word_SMS(właściciel, "java/net/Socket") || Word_SMS(właściciel, "java/net/ServerSocket") || Word_SMS(właściciel, "java/io/InputStream") || Word_SMS(właściciel, "java/io/OutputStream")) { 흐름호출(właściciel, nazwa_stała, deskryptor_stała, polecenie_KOD); return true; }
        if (Word_SMS(właściciel, "polski/własny/jądro_WARTOŚĆ") && polecenie_KOD == 184) {
            if (Word_SMS(nazwa_stała, "화면너비") && Word_SMS(deskryptor_stała, "()I")) { 넣기(przestrzeń_użytkownika.화면너비(), 1); return true; }
            if (Word_SMS(nazwa_stała, "화면높이") && Word_SMS(deskryptor_stała, "()I")) { 넣기(przestrzeń_użytkownika.화면높이(), 1); return true; }
            if (Word_SMS(nazwa_stała, "밀리초") && Word_SMS(deskryptor_stała, "()I")) { 넣기(przestrzeń_użytkownika.밀리초(), 1); return true; }
            if (Word_SMS(nazwa_stała, "그림대기") && Word_SMS(deskryptor_stała, "()I")) { 넣기(przestrzeń_użytkownika.그림대기(), 1); return true; }
            if (Word_SMS(nazwa_stała, "prostokąt") && Word_SMS(deskryptor_stała, "(IIIII)I")) { int 색상 = 빼기(1), wysokość_WARTOŚĆ = 빼기(1), 너비 = 빼기(1), Y_współrzędna = 빼기(1), współrzędna_X = 빼기(1); 넣기(przestrzeń_użytkownika.prostokąt(współrzędna_X, Y_współrzędna, 너비, wysokość_WARTOŚĆ, 색상), 1); return true; }
        }
        if (Word_SMS(właściciel, "java/net/InetAddress") || Word_SMS(właściciel, "java/net/DatagramPacket") || Word_SMS(właściciel, "java/net/DatagramSocket")) { 통신호출(właściciel, nazwa_stała, deskryptor_stała, polecenie_KOD); return true; }
        if (Word_SMS(właściciel, "java/lang/Thread")) { 가닥호출(nazwa_stała, deskryptor_stała, polecenie_KOD); return true; }
        if (Word_SMS(właściciel, "java/lang/Object")) {
            if (Word_SMS(nazwa_stała, "<init>") && Word_SMS(deskryptor_stała, "()V") && polecenie_KOD == 183) { systemy_informacyjne_prawidłowy_obiekt(빼기(2)); return true; }
            if (Word_SMS(nazwa_stała, "equals") && Word_SMS(deskryptor_stała, "(Ljava/lang/Object;)Z")) { int bajt_dane = 빼기(2), 첫값 = 빼기(2); if (systemy_informacyjne_prawidłowy_obiekt(첫값)) 넣기(첫값 == bajt_dane ? 1 : 0, 1); return true; }
        }
        if (wyjątek_stała(właściciel) != 0) {
            if (Word_SMS(nazwa_stała, "<init>") && polecenie_KOD == 183 && (Word_SMS(deskryptor_stała, "()V") || Word_SMS(deskryptor_stała, "(Ljava/lang/String;)V"))) {
                int monit = Word_SMS(deskryptor_stała, "()V") ? 0 : 빼기(2), obiekt_odwołanie = 빼기(2);
                if (obiekt_WARTOŚĆ(obiekt_odwołanie, 9)) { sterta_WARTOŚĆ[obiekt_odwołanie + 3] = monit; sterta_odwołanie[obiekt_odwołanie + 3] = 1; } return true;
            }
            if ((Word_SMS(nazwa_stała, "getMessage") || Word_SMS(nazwa_stała, "설명")) && Word_SMS(deskryptor_stała, "()Ljava/lang/String;")) { int obiekt_odwołanie = 빼기(2); if (obiekt_WARTOŚĆ(obiekt_odwołanie, 9)) 넣기(sterta_WARTOŚĆ[obiekt_odwołanie + 3], 2); return true; }
        }
        if (Word_SMS(właściciel, "java/lang/String")) {
            if (polecenie_KOD == 182 && Word_SMS(nazwa_stała, "getBytes") && (Word_SMS(deskryptor_stała, "()[B") || Word_SMS(deskryptor_stała, "(Ljava/lang/String;)[B"))) {
                int Encoding_nazwa = Word_SMS(deskryptor_stała, "()[B") ? 0 : 빼기(2), obiekt_odwołanie = 빼기(2);
                if (!obiekt_WARTOŚĆ(obiekt_odwołanie, 1)) return true;
                if (Encoding_nazwa != 0 && !teksty_równe(Encoding_nazwa, host_znak("UTF-8"), false) && !teksty_równe(Encoding_nazwa, host_znak("UTF8"), false) && !teksty_równe(Encoding_nazwa, host_znak("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int wpis_ILE_LICZB = sterta_WARTOŚĆ[obiekt_odwołanie + 1], 반환값 = przydzielić_Pamięć(20, wpis_ILE_LICZB * 3), 사용수 = 0; if (błąd) return true;
                for (int wewnętrzne_stanowisko = 0; wewnętrzne_stanowisko < wpis_ILE_LICZB; wewnętrzne_stanowisko++) {
                    int kod_znaku = sterta_WARTOŚĆ[obiekt_odwołanie + 2 + wewnętrzne_stanowisko];
                    if (kod_znaku >= 0xd800 && kod_znaku <= 0xdbff && wewnętrzne_stanowisko + 1 < wpis_ILE_LICZB && sterta_WARTOŚĆ[obiekt_odwołanie + 3 + wewnętrzne_stanowisko] >= 0xdc00 && sterta_WARTOŚĆ[obiekt_odwołanie + 3 + wewnętrzne_stanowisko] <= 0xdfff) kod_znaku = 0x10000 + ((kod_znaku - 0xd800) << 10) + sterta_WARTOŚĆ[obiekt_odwołanie + 2 + ++wewnętrzne_stanowisko] - 0xdc00;
                    else if (kod_znaku >= 0xd800 && kod_znaku <= 0xdfff) kod_znaku = '?';
                    if (kod_znaku < 128) sterta_WARTOŚĆ[반환값 + 2 + 사용수++] = kod_znaku;
                    else { int bajt_ILE_LICZB = kod_znaku < 2048 ? 2 : kod_znaku < 65536 ? 3 : 4; sterta_WARTOŚĆ[반환값 + 2 + 사용수++] = (byte)((bajt_ILE_LICZB == 2 ? 192 : bajt_ILE_LICZB == 3 ? 224 : 240) | kod_znaku >> (6 * (bajt_ILE_LICZB - 1))); for (int Porównanie_stanowisko = bajt_ILE_LICZB - 1; Porównanie_stanowisko > 0; Porównanie_stanowisko--) sterta_WARTOŚĆ[반환값 + 2 + 사용수++] = (byte)(128 | kod_znaku >> (6 * (Porównanie_stanowisko - 1)) & 63); }
                }
                sterta_WARTOŚĆ[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (polecenie_KOD == 184 && Word_SMS(nazwa_stała, "valueOf") && Word_SMS(deskryptor_stała, "(I)Ljava/lang/String;")) { 넣기(cyfra_znak(빼기(1)), 2); return true; }
            if (polecenie_KOD != 182) return false;
            if (Word_SMS(nazwa_stała, "equals") && Word_SMS(deskryptor_stała, "(Ljava/lang/Object;)Z")) { int bajt_dane = 빼기(2), 첫값 = 빼기(2); if (obiekt_WARTOŚĆ(첫값, 1)) 넣기(teksty_równe(첫값, bajt_dane, false) ? 1 : 0, 1); return true; }
            if (Word_SMS(nazwa_stała, "isEmpty") && Word_SMS(deskryptor_stała, "()Z")) { int 첫값 = 빼기(2); if (obiekt_WARTOŚĆ(첫값, 1)) 넣기(sterta_WARTOŚĆ[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Word_SMS(nazwa_stała, "substring") && (Word_SMS(deskryptor_stała, "(I)Ljava/lang/String;") || Word_SMS(deskryptor_stała, "(II)Ljava/lang/String;"))) {
                boolean SEKUNDA_WARTOŚĆ = Word_SMS(deskryptor_stała, "(II)Ljava/lang/String;"); int Koniec_stanowisko = SEKUNDA_WARTOŚĆ ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (obiekt_WARTOŚĆ(첫값, 1)) 넣기(SMS_fragment(첫값, 시작점, SEKUNDA_WARTOŚĆ ? Koniec_stanowisko : sterta_WARTOŚĆ[첫값 + 1]), 2); return true;
            }
            if (Word_SMS(nazwa_stała, "concat") && Word_SMS(deskryptor_stała, "(Ljava/lang/String;)Ljava/lang/String;")) { int bajt_dane = 빼기(2), 첫값 = 빼기(2); 넣기(Dołącz_SMS(첫값, bajt_dane), 2); return true; }
            if (Word_SMS(nazwa_stała, "hashCode") && Word_SMS(deskryptor_stała, "()I")) { int 첫값 = 빼기(2), skrót_WARTOŚĆ_bb8f435c = 0; if (obiekt_WARTOŚĆ(첫값, 1)) { for (int Loop_INDEKS = 0; Loop_INDEKS < sterta_WARTOŚĆ[첫값 + 1]; Loop_INDEKS++) skrót_WARTOŚĆ_bb8f435c = skrót_WARTOŚĆ_bb8f435c * 31 + sterta_WARTOŚĆ[첫값 + 2 + Loop_INDEKS]; 넣기(skrót_WARTOŚĆ_bb8f435c, 1); } return true; }
            if (Word_SMS(nazwa_stała, "toString") && Word_SMS(deskryptor_stała, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (obiekt_WARTOŚĆ(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Word_SMS(właściciel, "java/lang/Integer")) {
            if (polecenie_KOD == 184 && Word_SMS(nazwa_stała, "valueOf") && Word_SMS(deskryptor_stała, "(I)Ljava/lang/Integer;")) { int dane_WARTOŚĆ = 빼기(1), obiekt_odwołanie = dane_WARTOŚĆ >= -128 && dane_WARTOŚĆ <= 127 ? Store_liczba_całkowita[dane_WARTOŚĆ + 128] : 0; if (obiekt_odwołanie == 0) { obiekt_odwołanie = przydzielić_Pamięć(12, 1); if (!błąd) { sterta_WARTOŚĆ[obiekt_odwołanie + 2] = dane_WARTOŚĆ; if (dane_WARTOŚĆ >= -128 && dane_WARTOŚĆ <= 127) Store_liczba_całkowita[dane_WARTOŚĆ + 128] = obiekt_odwołanie; } } 넣기(obiekt_odwołanie, 2); return true; }
            if (polecenie_KOD == 183 && Word_SMS(nazwa_stała, "<init>") && Word_SMS(deskryptor_stała, "(I)V")) { int dane_WARTOŚĆ = 빼기(1), obiekt_odwołanie = 빼기(2); if (obiekt_WARTOŚĆ(obiekt_odwołanie, 12)) sterta_WARTOŚĆ[obiekt_odwołanie + 2] = dane_WARTOŚĆ; return true; }
            if (polecenie_KOD == 182 && Word_SMS(nazwa_stała, "intValue") && Word_SMS(deskryptor_stała, "()I")) { int obiekt_odwołanie = 빼기(2); if (obiekt_WARTOŚĆ(obiekt_odwołanie, 12)) 넣기(sterta_WARTOŚĆ[obiekt_odwołanie + 2], 1); return true; }
            if (polecenie_KOD == 184 && Word_SMS(nazwa_stała, "toString") && Word_SMS(deskryptor_stała, "(I)Ljava/lang/String;")) { 넣기(cyfra_znak(빼기(1)), 2); return true; }
        }
        if (Word_SMS(właściciel, "java/lang/Math") && polecenie_KOD == 184) {
            if (Word_SMS(nazwa_stała, "abs") && Word_SMS(deskryptor_stała, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((Word_SMS(nazwa_stała, "min") || Word_SMS(nazwa_stała, "max")) && Word_SMS(deskryptor_stała, "(II)I")) { int bajt_dane = 빼기(1), 첫값 = 빼기(1); 넣기(Word_SMS(nazwa_stała, "min") ? (첫값 < bajt_dane ? 첫값 : bajt_dane) : (첫값 > bajt_dane ? 첫값 : bajt_dane), 1); return true; }
        }
        if (Word_SMS(właściciel, "java/lang/System") && polecenie_KOD == 184) {
            if (Word_SMS(nazwa_stała, "gc") && Word_SMS(deskryptor_stała, "()V")) { 수거(); return true; }
            if (Word_SMS(nazwa_stała, "arraycopy") && Word_SMS(deskryptor_stała, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int wpis_ILE_LICZB = 빼기(1), cel_WARTOŚĆ_INDEKS = 빼기(1), bajt_dane = 빼기(2), START_stanowisko = 빼기(1), 첫값 = 빼기(2);
                if (systemy_informacyjne_prawidłowy_obiekt(첫값) && systemy_informacyjne_prawidłowy_obiekt(bajt_dane)) {
                    int obszar_KOD = sterta_WARTOŚĆ[첫값];
                    if (sterta_WARTOŚĆ[bajt_dane] != obszar_KOD || (obszar_KOD != 2 && obszar_KOD != 3 && (obszar_KOD < 20 || obszar_KOD > 23))) awaria_WARTOŚĆ("arraycopy type mismatch");
                    else if (wpis_ILE_LICZB < 0 || START_stanowisko < 0 || cel_WARTOŚĆ_INDEKS < 0 || START_stanowisko > sterta_WARTOŚĆ[첫값 + 1] - wpis_ILE_LICZB || cel_WARTOŚĆ_INDEKS > sterta_WARTOŚĆ[bajt_dane + 1] - wpis_ILE_LICZB) awaria_WARTOŚĆ("ArrayIndexOutOfBoundsException");
                    else if (첫값 == bajt_dane && cel_WARTOŚĆ_INDEKS > START_stanowisko) { for (int Loop_INDEKS = wpis_ILE_LICZB - 1; Loop_INDEKS >= 0; Loop_INDEKS--) sterta_WARTOŚĆ[bajt_dane + 2 + cel_WARTOŚĆ_INDEKS + Loop_INDEKS] = sterta_WARTOŚĆ[첫값 + 2 + START_stanowisko + Loop_INDEKS]; }
                    else { for (int Loop_INDEKS = 0; Loop_INDEKS < wpis_ILE_LICZB && !błąd; Loop_INDEKS++) { int dane_WARTOŚĆ = sterta_WARTOŚĆ[첫값 + 2 + START_stanowisko + Loop_INDEKS]; if (obszar_KOD != 3 || 배열저장가능(bajt_dane, dane_WARTOŚĆ)) sterta_WARTOŚĆ[bajt_dane + 2 + cel_WARTOŚĆ_INDEKS + Loop_INDEKS] = dane_WARTOŚĆ; } }
                }
                return true;
            }
        }
        if (Word_SMS(właściciel, "java/util/ArrayList") || Word_SMS(właściciel, "java/util/List") || Word_SMS(właściciel, "java/util/HashMap") || Word_SMS(właściciel, "java/util/Map")) {
            모음호출(właściciel, nazwa_stała, deskryptor_stała, polecenie_KOD); return true;
        }
        return false;
    }
    static void 모음늘리기(int obiekt_odwołanie, int 필요수) {
        int Wstecz_WARTOŚĆ = sterta_WARTOŚĆ[obiekt_odwołanie + 2], pojemność_dane = Wstecz_WARTOŚĆ == 0 ? 0 : sterta_WARTOŚĆ[Wstecz_WARTOŚĆ + 1];
        if (pojemność_dane >= 필요수) return;
        int Dalej_stanowisko = pojemność_dane < 8 ? 8 : pojemność_dane * 2; if (Dalej_stanowisko < 필요수) Dalej_stanowisko = 필요수;
        int dane_TABLICA = przydzielić_Pamięć(3, Dalej_stanowisko); if (błąd) return;
        for (int Loop_INDEKS = 0; Loop_INDEKS < pojemność_dane; Loop_INDEKS++) sterta_WARTOŚĆ[dane_TABLICA + 2 + Loop_INDEKS] = sterta_WARTOŚĆ[Wstecz_WARTOŚĆ + 2 + Loop_INDEKS];
        sterta_WARTOŚĆ[obiekt_odwołanie + 2] = dane_TABLICA; sterta_odwołanie[obiekt_odwołanie + 2] = 1;
    }
    static void 모음호출(int właściciel, int nazwa_stała, int deskryptor_stała, int polecenie_KOD) {
        boolean 대응참조 = Word_SMS(właściciel, "java/util/HashMap") || Word_SMS(właściciel, "java/util/Map"); int obszar_KOD = 대응참조 ? 11 : 10;
        if (Word_SMS(nazwa_stała, "<init>") && polecenie_KOD == 183 && Word_SMS(deskryptor_stała, "()V")) { int obiekt_odwołanie = 빼기(2); if (obiekt_WARTOŚĆ(obiekt_odwołanie, obszar_KOD)) 모음늘리기(obiekt_odwołanie, 8); return; }
        if (polecenie_KOD != 182 && polecenie_KOD != 185) { awaria_WARTOŚĆ("invalid collection invocation"); return; }
        if (Word_SMS(nazwa_stała, "size") && Word_SMS(deskryptor_stała, "()I") || Word_SMS(nazwa_stała, "isEmpty") && Word_SMS(deskryptor_stała, "()Z")) {
            int obiekt_odwołanie = 빼기(2); if (obiekt_WARTOŚĆ(obiekt_odwołanie, obszar_KOD)) 넣기(Word_SMS(nazwa_stała, "size") ? sterta_WARTOŚĆ[obiekt_odwołanie + 3] : sterta_WARTOŚĆ[obiekt_odwołanie + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Word_SMS(nazwa_stała, "clear") && Word_SMS(deskryptor_stała, "()V")) { int obiekt_odwołanie = 빼기(2); if (obiekt_WARTOŚĆ(obiekt_odwołanie, obszar_KOD)) { int dane_TABLICA = sterta_WARTOŚĆ[obiekt_odwołanie + 2]; for (int Loop_INDEKS = 0; Loop_INDEKS < sterta_WARTOŚĆ[dane_TABLICA + 1]; Loop_INDEKS++) sterta_WARTOŚĆ[dane_TABLICA + 2 + Loop_INDEKS] = 0; sterta_WARTOŚĆ[obiekt_odwołanie + 3] = 0; } return; }
        if (!대응참조 && Word_SMS(nazwa_stała, "add") && Word_SMS(deskryptor_stała, "(Ljava/lang/Object;)Z")) {
            int dane_WARTOŚĆ = 빼기(2), obiekt_odwołanie = 빼기(2); if (!obiekt_WARTOŚĆ(obiekt_odwołanie, 10)) return;
            int wpis_ILE_LICZB = sterta_WARTOŚĆ[obiekt_odwołanie + 3]; 모음늘리기(obiekt_odwołanie, wpis_ILE_LICZB + 1); if (!błąd) { sterta_WARTOŚĆ[sterta_WARTOŚĆ[obiekt_odwołanie + 2] + 2 + wpis_ILE_LICZB] = dane_WARTOŚĆ; sterta_WARTOŚĆ[obiekt_odwołanie + 3] = wpis_ILE_LICZB + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Word_SMS(nazwa_stała, "get") || Word_SMS(nazwa_stała, "remove")) && Word_SMS(deskryptor_stała, "(I)Ljava/lang/Object;") || !대응참조 && Word_SMS(nazwa_stała, "set") && Word_SMS(deskryptor_stała, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean systemy_informacyjne_Przypisano = Word_SMS(nazwa_stała, "set"); int dane_WARTOŚĆ = systemy_informacyjne_Przypisano ? 빼기(2) : 0, wpis_stanowisko = 빼기(1), obiekt_odwołanie = 빼기(2);
            if (!obiekt_WARTOŚĆ(obiekt_odwołanie, 10)) return;
            int wpis_ILE_LICZB = sterta_WARTOŚĆ[obiekt_odwołanie + 3], dane_TABLICA = sterta_WARTOŚĆ[obiekt_odwołanie + 2];
            if (wpis_stanowisko < 0 || wpis_stanowisko >= wpis_ILE_LICZB) { 예외던짐(6, "list index"); return; }
            int Wstecz_WARTOŚĆ = sterta_WARTOŚĆ[dane_TABLICA + 2 + wpis_stanowisko];
            if (systemy_informacyjne_Przypisano) sterta_WARTOŚĆ[dane_TABLICA + 2 + wpis_stanowisko] = dane_WARTOŚĆ;
            if (Word_SMS(nazwa_stała, "remove")) { for (int Loop_INDEKS = wpis_stanowisko + 1; Loop_INDEKS < wpis_ILE_LICZB; Loop_INDEKS++) sterta_WARTOŚĆ[dane_TABLICA + 1 + Loop_INDEKS] = sterta_WARTOŚĆ[dane_TABLICA + 2 + Loop_INDEKS]; sterta_WARTOŚĆ[dane_TABLICA + 1 + wpis_ILE_LICZB] = 0; sterta_WARTOŚĆ[obiekt_odwołanie + 3] = wpis_ILE_LICZB - 1; }
            넣기(Wstecz_WARTOŚĆ, 2); return;
        }
        if (대응참조 && (Word_SMS(nazwa_stała, "get") || Word_SMS(nazwa_stała, "remove")) && Word_SMS(deskryptor_stała, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(nazwa_stała, "put") && Word_SMS(deskryptor_stała, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(nazwa_stała, "containsKey") && Word_SMS(deskryptor_stała, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Word_SMS(nazwa_stała, "put"), usuń = Word_SMS(nazwa_stała, "remove");
            int dane_WARTOŚĆ = 넣기여부 ? 빼기(2) : 0, Klucz_odwołanie = 빼기(2), obiekt_odwołanie = 빼기(2); if (!obiekt_WARTOŚĆ(obiekt_odwołanie, 11)) return;
            int wpis_ILE_LICZB = sterta_WARTOŚĆ[obiekt_odwołanie + 3], dane_TABLICA = sterta_WARTOŚĆ[obiekt_odwołanie + 2], 찾은여부 = -1;
            for (int Loop_INDEKS = 0; Loop_INDEKS < wpis_ILE_LICZB; Loop_INDEKS++) if (값같음(Klucz_odwołanie, sterta_WARTOŚĆ[dane_TABLICA + 2 + 2 * Loop_INDEKS])) { 찾은여부 = Loop_INDEKS; break; }
            int Wstecz_WARTOŚĆ = 찾은여부 < 0 ? 0 : sterta_WARTOŚĆ[dane_TABLICA + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(obiekt_odwołanie, (wpis_ILE_LICZB + 1) * 2); dane_TABLICA = sterta_WARTOŚĆ[obiekt_odwołanie + 2]; 찾은여부 = wpis_ILE_LICZB; if (!błąd) sterta_WARTOŚĆ[obiekt_odwołanie + 3] = wpis_ILE_LICZB + 1; }
                if (!błąd) { sterta_WARTOŚĆ[dane_TABLICA + 2 + 2 * 찾은여부] = Klucz_odwołanie; sterta_WARTOŚĆ[dane_TABLICA + 3 + 2 * 찾은여부] = dane_WARTOŚĆ; }
            }
            if (usuń && 찾은여부 >= 0) { for (int Loop_INDEKS = 찾은여부 + 1; Loop_INDEKS < wpis_ILE_LICZB; Loop_INDEKS++) { sterta_WARTOŚĆ[dane_TABLICA + 2 * Loop_INDEKS] = sterta_WARTOŚĆ[dane_TABLICA + 2 + 2 * Loop_INDEKS]; sterta_WARTOŚĆ[dane_TABLICA + 1 + 2 * Loop_INDEKS] = sterta_WARTOŚĆ[dane_TABLICA + 3 + 2 * Loop_INDEKS]; } sterta_WARTOŚĆ[dane_TABLICA + 2 * wpis_ILE_LICZB] = 0; sterta_WARTOŚĆ[dane_TABLICA + 1 + 2 * wpis_ILE_LICZB] = 0; sterta_WARTOŚĆ[obiekt_odwołanie + 3] = wpis_ILE_LICZB - 1; }
            if (Word_SMS(nazwa_stała, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(Wstecz_WARTOŚĆ, 2);
            return;
        }
        awaria_WARTOŚĆ("unsupported collection method");
    }
    static boolean 잠금얻기(int obiekt_odwołanie) {
        if (!systemy_informacyjne_prawidłowy_obiekt(obiekt_odwołanie)) return false;
        if (잠금깊이[obiekt_odwołanie] != 0 && blokada_właściciel[obiekt_odwołanie] != bieżący_wątek + 1) { żądanie_zmiany = true; return false; }
        blokada_właściciel[obiekt_odwołanie] = bieżący_wątek + 1; 잠금깊이[obiekt_odwołanie]++; return true;
    }
    static void wersja_blokada(int obiekt_odwołanie) {
        if (!systemy_informacyjne_prawidłowy_obiekt(obiekt_odwołanie)) return;
        if (잠금깊이[obiekt_odwołanie] == 0 || blokada_właściciel[obiekt_odwołanie] != bieżący_wątek + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[obiekt_odwołanie] == 0) blokada_właściciel[obiekt_odwołanie] = 0;
    }
    static boolean zmiana_wątek() {
        wątek_kadr[bieżący_wątek] = kadr_INDEKS;
        if (kadr_INDEKS < bieżący_wątek * 32) wątek_Stan[bieżący_wątek] = 3;
        for (int Loop_INDEKS = 0; Loop_INDEKS < liczba_wątków; Loop_INDEKS++) if (wątek_Stan[Loop_INDEKS] == 2 && wątek_Stan[가닥대기[Loop_INDEKS]] == 3) wątek_Stan[Loop_INDEKS] = 1;
        for (int Loop_INDEKS = 1; Loop_INDEKS <= liczba_wątków; Loop_INDEKS++) {
            int Dalej_stanowisko = (bieżący_wątek + Loop_INDEKS) % liczba_wątków;
            if (wątek_Stan[Dalej_stanowisko] == 1) { bieżący_wątek = Dalej_stanowisko; kadr_INDEKS = wątek_kadr[Dalej_stanowisko]; żądanie_zmiany = false; return true; }
        }
        for (int Loop_INDEKS = 0; Loop_INDEKS < liczba_wątków; Loop_INDEKS++) if (wątek_Stan[Loop_INDEKS] != 3) { awaria_WARTOŚĆ("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int nazwa_stała, int deskryptor_stała, int polecenie_KOD) { Proces_wątek(nazwa_stała, deskryptor_stała, polecenie_KOD, false); }
    static void Proces_wątek(int nazwa_stała, int deskryptor_stała, int polecenie_KOD, boolean polski) {
        if (polecenie_KOD == 184 && Word_SMS(nazwa_stała, polski ? "Dochód_zadanie" : "yield") && Word_SMS(deskryptor_stała, "()V")) { żądanie_zmiany = true; return; }
        if (polecenie_KOD == 184 && Word_SMS(nazwa_stała, "currentThread") && Word_SMS(deskryptor_stała, "()Ljava/lang/Thread;")) { 넣기(wątek_obiekt[bieżący_wątek], 2); return; }
        if (polecenie_KOD == 183 && Word_SMS(nazwa_stała, "<init>") && (Word_SMS(deskryptor_stała, "()V") || Word_SMS(deskryptor_stała, polski ? "(Lpolski/własny/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int cel_ADRES = Word_SMS(deskryptor_stała, "()V") ? 0 : 빼기(2), obiekt_odwołanie = 빼기(2);
            if (!systemy_informacyjne_prawidłowy_obiekt(obiekt_odwołanie)) return;
            if (sterta_WARTOŚĆ[obiekt_odwołanie] == 13) { sterta_WARTOŚĆ[obiekt_odwołanie + 2] = cel_ADRES; sterta_odwołanie[obiekt_odwołanie + 2] = 1; }
            else if (cel_ADRES != 0) awaria_WARTOŚĆ("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (polecenie_KOD == 182 && (Word_SMS(nazwa_stała, polski ? "START_zadanie" : "start") || Word_SMS(nazwa_stała, polski ? "기다리기" : "join")) && Word_SMS(deskryptor_stała, "()V") || polecenie_KOD == 182 && Word_SMS(nazwa_stała, polski ? "살아있는가" : "isAlive") && Word_SMS(deskryptor_stała, "()Z")) {
            int obiekt_odwołanie = 빼기(2); if (!systemy_informacyjne_prawidłowy_obiekt(obiekt_odwołanie)) return;
            int konto_WARTOŚĆ = -1; for (int Loop_INDEKS = 0; Loop_INDEKS < liczba_wątków; Loop_INDEKS++) if (wątek_obiekt[Loop_INDEKS] == obiekt_odwołanie) konto_WARTOŚĆ = Loop_INDEKS;
            if (Word_SMS(nazwa_stała, polski ? "살아있는가" : "isAlive")) { 넣기(konto_WARTOŚĆ >= 0 && wątek_Stan[konto_WARTOŚĆ] != 3 ? 1 : 0, 1); return; }
            if (Word_SMS(nazwa_stała, polski ? "기다리기" : "join")) { if (konto_WARTOŚĆ >= 0 && wątek_Stan[konto_WARTOŚĆ] != 3) { 가닥대기[bieżący_wątek] = konto_WARTOŚĆ; wątek_Stan[bieżący_wątek] = 2; żądanie_zmiany = true; } return; }
            if (konto_WARTOŚĆ >= 0) { 예외던짐(polski ? 38 : 16, "thread already started"); return; }
            if (liczba_wątków == 4) { awaria_WARTOŚĆ("thread limit (4 including main)"); return; }
            int cel_ADRES = sterta_WARTOŚĆ[obiekt_odwołanie] == 13 ? sterta_WARTOŚĆ[obiekt_odwołanie + 2] : obiekt_odwołanie;
            int Plik_INDEKS = cel_ADRES > 0 && sterta_WARTOŚĆ[cel_ADRES] >= 32 ? nazwa_metoda(sterta_WARTOŚĆ[cel_ADRES] - 32, polski ? "Uruchom" : "run", "()V") : -1;
            if (cel_ADRES != 0 && Plik_INDEKS < 0) { awaria_WARTOŚĆ("Runnable.run required"); return; }
            konto_WARTOŚĆ = liczba_wątków++; wątek_obiekt[konto_WARTOŚĆ] = obiekt_odwołanie; wątek_cel[konto_WARTOŚĆ] = cel_ADRES;
            int kadr = konto_WARTOŚĆ * 32; wątek_kadr[konto_WARTOŚĆ] = Plik_INDEKS < 0 ? kadr - 1 : kadr; wątek_Stan[konto_WARTOŚĆ] = Plik_INDEKS < 0 ? 3 : 1;
            if (Plik_INDEKS >= 0) { kadr_metoda[kadr] = Plik_INDEKS; kadr_stanowisko[kadr] = metoda_START[Plik_INDEKS]; lokalny_WARTOŚĆ[kadr * 128] = cel_ADRES; lokalny_TYP[kadr * 128] = 2; }
            return;
        }
        awaria_WARTOŚĆ("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], ADRES_SMS = new int[16];
    static int lokalny_ADRES() { return ADRES_obiekt(0x7f000001); }
    static int ADRES_obiekt(int WARTOŚĆ) { int obiekt_odwołanie = przydzielić_Pamięć(14, 1); if (!błąd) sterta_WARTOŚĆ[obiekt_odwołanie + 2] = WARTOŚĆ; return obiekt_odwołanie; }
    static int 주소해독(int obiekt_odwołanie) {
        if (obiekt_odwołanie == 0 || teksty_równe(obiekt_odwołanie, host_znak("localhost"), false)) return 0x7f000001;
        if (!obiekt_WARTOŚĆ(obiekt_odwołanie, 1)) return 0;
        int dane_WARTOŚĆ = 0, suma_ILE_LICZB = 0, ADRES_bajt = 0, 자릿수 = 0, wpis_ILE_LICZB = sterta_WARTOŚĆ[obiekt_odwołanie + 1];
        for (int Loop_INDEKS = 0; Loop_INDEKS <= wpis_ILE_LICZB; Loop_INDEKS++) {
            int kod_znaku = Loop_INDEKS == wpis_ILE_LICZB ? '.' : sterta_WARTOŚĆ[obiekt_odwołanie + 2 + Loop_INDEKS];
            if (kod_znaku == '.') { if (자릿수 == 0 || suma_ILE_LICZB == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } dane_WARTOŚĆ = dane_WARTOŚĆ << 8 | ADRES_bajt; suma_ILE_LICZB++; ADRES_bajt = 자릿수 = 0; }
            else { if (kod_znaku < '0' || kod_znaku > '9' || ++자릿수 > 3 || (ADRES_bajt = ADRES_bajt * 10 + kod_znaku - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (suma_ILE_LICZB != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return dane_WARTOŚĆ;
    }
    static int ADRES_znak(int dane_WARTOŚĆ) {
        int wpis_ILE_LICZB = 0;
        for (int przesunąć = 24; przesunąć >= 0; przesunąć -= 8) {
            int ADRES_bajt = dane_WARTOŚĆ >>> przesunąć & 255;
            if (ADRES_bajt >= 100) ADRES_SMS[wpis_ILE_LICZB++] = '0' + ADRES_bajt / 100;
            if (ADRES_bajt >= 10) ADRES_SMS[wpis_ILE_LICZB++] = '0' + ADRES_bajt / 10 % 10;
            ADRES_SMS[wpis_ILE_LICZB++] = '0' + ADRES_bajt % 10; if (przesunąć != 0) ADRES_SMS[wpis_ILE_LICZB++] = '.';
        }
        int obiekt_odwołanie = przydzielić_Pamięć(1, wpis_ILE_LICZB); if (!błąd) for (int Loop_INDEKS = 0; Loop_INDEKS < wpis_ILE_LICZB; Loop_INDEKS++) sterta_WARTOŚĆ[obiekt_odwołanie + 2 + Loop_INDEKS] = ADRES_SMS[Loop_INDEKS]; return obiekt_odwołanie;
    }
    static void 통신호출(int właściciel, int nazwa_stała, int deskryptor_stała, int polecenie_KOD) {
        if (Word_SMS(właściciel, "java/net/InetAddress")) {
            if (polecenie_KOD == 184 && Word_SMS(nazwa_stała, "getLoopbackAddress") && Word_SMS(deskryptor_stała, "()Ljava/net/InetAddress;")) { 넣기(lokalny_ADRES(), 2); return; }
            if (polecenie_KOD == 184 && Word_SMS(nazwa_stała, "getByName") && Word_SMS(deskryptor_stała, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int dane_WARTOŚĆ = 주소해독(빼기(2)); if (던진객체 == 0 && !błąd) 넣기(ADRES_obiekt(dane_WARTOŚĆ), 2); return;
            }
            if (polecenie_KOD == 182 && Word_SMS(nazwa_stała, "getHostAddress") && Word_SMS(deskryptor_stała, "()Ljava/lang/String;")) { int obiekt_odwołanie = 빼기(2); if (obiekt_WARTOŚĆ(obiekt_odwołanie, 14)) 넣기(ADRES_znak(sterta_WARTOŚĆ[obiekt_odwołanie + 2]), 2); return; }
        }
        if (Word_SMS(właściciel, "java/net/DatagramPacket")) {
            if (polecenie_KOD == 183 && Word_SMS(nazwa_stała, "<init>") && (Word_SMS(deskryptor_stała, "([BI)V") || Word_SMS(deskryptor_stała, "([BILjava/net/InetAddress;I)V"))) {
                boolean cel_WARTOŚĆ_odwołanie = Word_SMS(deskryptor_stała, "([BILjava/net/InetAddress;I)V"); int numer_portu = cel_WARTOŚĆ_odwołanie ? 빼기(1) : 0, ADRES_odwołanie = cel_WARTOŚĆ_odwołanie ? 빼기(2) : 0;
                int wpis_ILE_LICZB = 빼기(1), dane_TABLICA = 빼기(2), obiekt_odwołanie = 빼기(2);
                if (!obiekt_WARTOŚĆ(obiekt_odwołanie, 16) || !obiekt_WARTOŚĆ(dane_TABLICA, 20)) return;
                if (wpis_ILE_LICZB < 0 || wpis_ILE_LICZB > sterta_WARTOŚĆ[dane_TABLICA + 1] || numer_portu < 0 || numer_portu > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (ADRES_odwołanie != 0 && !obiekt_WARTOŚĆ(ADRES_odwołanie, 14)) return;
                sterta_WARTOŚĆ[obiekt_odwołanie + 2] = dane_TABLICA; sterta_odwołanie[obiekt_odwołanie + 2] = 1; sterta_WARTOŚĆ[obiekt_odwołanie + 3] = wpis_ILE_LICZB;
                sterta_WARTOŚĆ[obiekt_odwołanie + 4] = ADRES_odwołanie; sterta_odwołanie[obiekt_odwołanie + 4] = 1; sterta_WARTOŚĆ[obiekt_odwołanie + 5] = numer_portu; return;
            }
            if (polecenie_KOD == 182 && Word_SMS(nazwa_stała, "setLength") && Word_SMS(deskryptor_stała, "(I)V")) {
                int wpis_ILE_LICZB = 빼기(1), obiekt_odwołanie = 빼기(2); if (!obiekt_WARTOŚĆ(obiekt_odwołanie, 16)) return;
                if (wpis_ILE_LICZB < 0 || wpis_ILE_LICZB > sterta_WARTOŚĆ[sterta_WARTOŚĆ[obiekt_odwołanie + 2] + 1]) 예외던짐(9, "invalid datagram length"); else sterta_WARTOŚĆ[obiekt_odwołanie + 3] = wpis_ILE_LICZB; return;
            }
            if (polecenie_KOD == 182 && (Word_SMS(nazwa_stała, "getData") && Word_SMS(deskryptor_stała, "()[B") || Word_SMS(nazwa_stała, "getLength") && Word_SMS(deskryptor_stała, "()I") || Word_SMS(nazwa_stała, "getAddress") && Word_SMS(deskryptor_stała, "()Ljava/net/InetAddress;") || Word_SMS(nazwa_stała, "getPort") && Word_SMS(deskryptor_stała, "()I"))) {
                int obiekt_odwołanie = 빼기(2); if (!obiekt_WARTOŚĆ(obiekt_odwołanie, 16)) return;
                int wpis_stanowisko = Word_SMS(nazwa_stała, "getData") ? 2 : Word_SMS(nazwa_stała, "getLength") ? 3 : Word_SMS(nazwa_stała, "getAddress") ? 4 : 5;
                넣기(sterta_WARTOŚĆ[obiekt_odwołanie + wpis_stanowisko], wpis_stanowisko == 2 || wpis_stanowisko == 4 ? 2 : 1); return;
            }
        }
        if (Word_SMS(właściciel, "java/net/DatagramSocket")) {
            if (polecenie_KOD == 183 && Word_SMS(nazwa_stała, "<init>") && (Word_SMS(deskryptor_stała, "()V") || Word_SMS(deskryptor_stała, "(I)V"))) {
                int numer_portu = Word_SMS(deskryptor_stała, "()V") ? 0 : 빼기(1), obiekt_odwołanie = 빼기(2); if (!obiekt_WARTOŚĆ(obiekt_odwołanie, 15)) return;
                if (numer_portu < 0 || numer_portu > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = przestrzeń_użytkownika.otwarty_sieć(numer_portu); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else sterta_WARTOŚĆ[obiekt_odwołanie + 2] = 열린파일번호; return;
            }
            if (polecenie_KOD == 182 && Word_SMS(nazwa_stała, "setSoTimeout") && Word_SMS(deskryptor_stała, "(I)V")) {
                int 밀리초값 = 빼기(1), obiekt_odwołanie = 빼기(2); if (!obiekt_WARTOŚĆ(obiekt_odwołanie, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else sterta_WARTOŚĆ[obiekt_odwołanie + 3] = 밀리초값; return;
            }
            if (polecenie_KOD == 182 && Word_SMS(nazwa_stała, "getLocalPort") && Word_SMS(deskryptor_stała, "()I")) { int obiekt_odwołanie = 빼기(2); if (obiekt_WARTOŚĆ(obiekt_odwołanie, 15)) 넣기(sterta_WARTOŚĆ[obiekt_odwołanie + 2] < 0 ? -1 : przestrzeń_użytkownika.sieć_port(sterta_WARTOŚĆ[obiekt_odwołanie + 2]), 1); return; }
            if (polecenie_KOD == 182 && Word_SMS(nazwa_stała, "isClosed") && Word_SMS(deskryptor_stała, "()Z")) { int obiekt_odwołanie = 빼기(2); if (obiekt_WARTOŚĆ(obiekt_odwołanie, 15)) 넣기(sterta_WARTOŚĆ[obiekt_odwołanie + 2] < 0 ? 1 : 0, 1); return; }
            if (polecenie_KOD == 182 && Word_SMS(nazwa_stała, "close") && Word_SMS(deskryptor_stała, "()V")) { int obiekt_odwołanie = 빼기(2); if (obiekt_WARTOŚĆ(obiekt_odwołanie, 15) && sterta_WARTOŚĆ[obiekt_odwołanie + 2] >= 0) { przestrzeń_użytkownika.Zamknij_Plik_deskryptor(sterta_WARTOŚĆ[obiekt_odwołanie + 2]); sterta_WARTOŚĆ[obiekt_odwołanie + 2] = -1; } return; }
            if (polecenie_KOD == 182 && (Word_SMS(nazwa_stała, "send") || Word_SMS(nazwa_stała, "receive")) && Word_SMS(deskryptor_stała, "(Ljava/net/DatagramPacket;)V")) {
                int pakiet_5cd5338b = 빼기(2), obiekt_odwołanie = 빼기(2); if (!obiekt_WARTOŚĆ(pakiet_5cd5338b, 16) || !obiekt_WARTOŚĆ(obiekt_odwołanie, 15)) return;
                int dane_TABLICA = sterta_WARTOŚĆ[pakiet_5cd5338b + 2], prawidłowy_długość = sterta_WARTOŚĆ[pakiet_5cd5338b + 3], 열린파일번호 = sterta_WARTOŚĆ[obiekt_odwołanie + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Word_SMS(nazwa_stała, "send")) {
                    if (!obiekt_WARTOŚĆ(sterta_WARTOŚĆ[pakiet_5cd5338b + 4], 14)) return;
                    if (prawidłowy_długość > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int Loop_INDEKS = 0; Loop_INDEKS < prawidłowy_długość; Loop_INDEKS++) 통신임시[Loop_INDEKS] = sterta_WARTOŚĆ[dane_TABLICA + 2 + Loop_INDEKS];
                    if (przestrzeń_użytkownika.wysłać_sieć(열린파일번호, sterta_WARTOŚĆ[sterta_WARTOŚĆ[pakiet_5cd5338b + 4] + 2], sterta_WARTOŚĆ[pakiet_5cd5338b + 5], 통신임시, prawidłowy_długość) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int wpis_ILE_LICZB = przestrzeń_użytkownika.odbierać_sieć(열린파일번호, 통신임시, prawidłowy_długość > 512 ? 512 : prawidłowy_długość);
                    if (wpis_ILE_LICZB == -11) {
                        int czas_bieżący = przestrzeń_użytkownika.밀리초();
                        if (sterta_WARTOŚĆ[obiekt_odwołanie + 4] == 0) sterta_WARTOŚĆ[obiekt_odwołanie + 4] = czas_bieżący + 1;
                        if (sterta_WARTOŚĆ[obiekt_odwołanie + 3] > 0 && czas_bieżący - (sterta_WARTOŚĆ[obiekt_odwołanie + 4] - 1) >= sterta_WARTOŚĆ[obiekt_odwołanie + 3]) { sterta_WARTOŚĆ[obiekt_odwołanie + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(obiekt_odwołanie, 2); 넣기(pakiet_5cd5338b, 2); kadr_stanowisko[kadr_INDEKS] = kadr_instrukcja[kadr_INDEKS]; żądanie_zmiany = true; return;
                    }
                    sterta_WARTOŚĆ[obiekt_odwołanie + 4] = 0;
                    if (wpis_ILE_LICZB < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int Loop_INDEKS = 0; Loop_INDEKS < wpis_ILE_LICZB; Loop_INDEKS++) sterta_WARTOŚĆ[dane_TABLICA + 2 + Loop_INDEKS] = (byte)통신임시[Loop_INDEKS];
                    sterta_WARTOŚĆ[pakiet_5cd5338b + 3] = wpis_ILE_LICZB; sterta_WARTOŚĆ[pakiet_5cd5338b + 4] = ADRES_obiekt(통신임시[513]); sterta_odwołanie[pakiet_5cd5338b + 4] = 1; sterta_WARTOŚĆ[pakiet_5cd5338b + 5] = 통신임시[512];
                }
                return;
            }
        }
        awaria_WARTOŚĆ("unsupported java.net method");
    }
    static boolean 흐름대기(int obiekt_odwołanie) {
        int czas_bieżący = przestrzeń_użytkownika.밀리초();
        if (sterta_WARTOŚĆ[obiekt_odwołanie + 5] == 0) sterta_WARTOŚĆ[obiekt_odwołanie + 5] = czas_bieżący + 1;
        if (sterta_WARTOŚĆ[obiekt_odwołanie + 3] > 0 && czas_bieżący - (sterta_WARTOŚĆ[obiekt_odwołanie + 5] - 1) >= sterta_WARTOŚĆ[obiekt_odwołanie + 3]) { sterta_WARTOŚĆ[obiekt_odwołanie + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        kadr_stanowisko[kadr_INDEKS] = kadr_instrukcja[kadr_INDEKS]; żądanie_zmiany = true; return true;
    }
    static void 흐름호출(int właściciel, int nazwa_stała, int deskryptor_stała, int polecenie_KOD) {
        boolean odbierać_strona = Word_SMS(właściciel, "java/net/ServerSocket"), Stream = Word_SMS(właściciel, "java/io/InputStream") || Word_SMS(właściciel, "java/io/OutputStream");
        if (!Stream && polecenie_KOD == 183 && Word_SMS(nazwa_stała, "<init>")) {
            boolean 빈여부 = Word_SMS(deskryptor_stała, "()V"), 이름지정여부 = Word_SMS(deskryptor_stała, "(Ljava/lang/String;I)V"), 주소지정여부 = Word_SMS(deskryptor_stała, "(Ljava/net/InetAddress;I)V");
            if (!(빈여부 || odbierać_strona && Word_SMS(deskryptor_stała, "(I)V") || !odbierać_strona && (이름지정여부 || 주소지정여부))) { awaria_WARTOŚĆ("unsupported socket constructor"); return; }
            int numer_portu = 빈여부 ? 0 : 빼기(1), ADRES_odwołanie = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, obiekt_odwołanie = 빼기(2);
            if (!obiekt_WARTOŚĆ(obiekt_odwołanie, odbierać_strona ? 18 : 17)) return;
            if (numer_portu < 0 || numer_portu > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !obiekt_WARTOŚĆ(ADRES_odwołanie, 14)) return;
            int identyfikator_sieciowy = 이름지정여부 ? 주소해독(ADRES_odwołanie) : 주소지정여부 ? sterta_WARTOŚĆ[ADRES_odwołanie + 2] : 0x7f000001;
            if (błąd || 던진객체 != 0) return;
            int 열린파일번호 = przestrzeń_użytkownika.Stream_kontrola(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = 빈여부 ? 0 : odbierać_strona ? przestrzeń_użytkownika.Stream_kontrola(1, 열린파일번호, numer_portu) : przestrzeń_użytkownika.POŁĄCZ_Stream(열린파일번호, identyfikator_sieciowy, numer_portu);
            if (처리값 < 0) { przestrzeń_użytkownika.Zamknij_Plik_deskryptor(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            sterta_WARTOŚĆ[obiekt_odwołanie + 2] = 열린파일번호; sterta_WARTOŚĆ[obiekt_odwołanie + 4] = numer_portu; sterta_WARTOŚĆ[obiekt_odwołanie + 6] = 빈여부 ? 0 : 1; return;
        }
        if (!Stream && Word_SMS(nazwa_stała, "setSoTimeout") && Word_SMS(deskryptor_stała, "(I)V")) { int 밀리초값 = 빼기(1), obiekt_odwołanie = 빼기(2); if (!obiekt_WARTOŚĆ(obiekt_odwołanie, odbierać_strona ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else sterta_WARTOŚĆ[obiekt_odwołanie + 3] = 밀리초값; return; }
        if (!Stream && Word_SMS(nazwa_stała, "close") && Word_SMS(deskryptor_stała, "()V")) { int obiekt_odwołanie = 빼기(2); if (obiekt_WARTOŚĆ(obiekt_odwołanie, odbierać_strona ? 18 : 17) && sterta_WARTOŚĆ[obiekt_odwołanie + 2] >= 0) { przestrzeń_użytkownika.Zamknij_Plik_deskryptor(sterta_WARTOŚĆ[obiekt_odwołanie + 2]); sterta_WARTOŚĆ[obiekt_odwołanie + 2] = -1; } return; }
        if (!Stream && (Word_SMS(nazwa_stała, "getLocalPort") || Word_SMS(nazwa_stała, "getPort") || Word_SMS(nazwa_stała, "isClosed") || Word_SMS(nazwa_stała, "isConnected"))) {
            int obiekt_odwołanie = 빼기(2); if (!obiekt_WARTOŚĆ(obiekt_odwołanie, odbierać_strona ? 18 : 17)) return;
            넣기(Word_SMS(nazwa_stała, "isClosed") ? sterta_WARTOŚĆ[obiekt_odwołanie + 2] < 0 ? 1 : 0 : Word_SMS(nazwa_stała, "isConnected") ? sterta_WARTOŚĆ[obiekt_odwołanie + 6] : Word_SMS(nazwa_stała, "getPort") ? sterta_WARTOŚĆ[obiekt_odwołanie + 4] : sterta_WARTOŚĆ[obiekt_odwołanie + 2] < 0 ? -1 : przestrzeń_użytkownika.Stream_kontrola(4, sterta_WARTOŚĆ[obiekt_odwołanie + 2], 0), 1); return;
        }
        if (odbierać_strona && Word_SMS(nazwa_stała, "accept") && Word_SMS(deskryptor_stała, "()Ljava/net/Socket;")) {
            int obiekt_odwołanie = 빼기(2); if (!obiekt_WARTOŚĆ(obiekt_odwołanie, 18)) return; int 열린파일번호 = przestrzeń_użytkownika.Stream_kontrola(3, sterta_WARTOŚĆ[obiekt_odwołanie + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(obiekt_odwołanie)) 넣기(obiekt_odwołanie, 2); return; }
            sterta_WARTOŚĆ[obiekt_odwołanie + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = przydzielić_Pamięć(17, 5); if (błąd) { przestrzeń_użytkownika.Zamknij_Plik_deskryptor(열린파일번호); return; } sterta_WARTOŚĆ[반환값 + 2] = 열린파일번호; sterta_WARTOŚĆ[반환값 + 4] = przestrzeń_użytkownika.Stream_kontrola(5, 열린파일번호, 0); sterta_WARTOŚĆ[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!odbierać_strona && !Stream && ((Word_SMS(nazwa_stała, "getInputStream") && Word_SMS(deskryptor_stała, "()Ljava/io/InputStream;")) || (Word_SMS(nazwa_stała, "getOutputStream") && Word_SMS(deskryptor_stała, "()Ljava/io/OutputStream;")))) {
            int obiekt_odwołanie = 빼기(2); if (!obiekt_WARTOŚĆ(obiekt_odwołanie, 17)) return; if (sterta_WARTOŚĆ[obiekt_odwołanie + 2] < 0 || sterta_WARTOŚĆ[obiekt_odwołanie + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = przydzielić_Pamięć(19, 4); if (błąd) return; sterta_WARTOŚĆ[반환값 + 2] = obiekt_odwołanie; sterta_odwołanie[반환값 + 2] = 1; sterta_WARTOŚĆ[반환값 + 3] = Word_SMS(nazwa_stała, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (Stream) {
            boolean 읽기여부 = Word_SMS(nazwa_stała, "read"), systemy_informacyjne_zapis_zabieg = Word_SMS(nazwa_stała, "write"), blok = Word_SMS(deskryptor_stała, "([B)I") || Word_SMS(deskryptor_stała, "([B)V"), systemy_informacyjne_PODTABLICA = Word_SMS(deskryptor_stała, "([BII)I") || Word_SMS(deskryptor_stała, "([BII)V");
            int wpis_ILE_LICZB = systemy_informacyjne_PODTABLICA ? 빼기(1) : 0, 시작변위 = systemy_informacyjne_PODTABLICA ? 빼기(1) : 0, dane_TABLICA = blok || systemy_informacyjne_PODTABLICA ? 빼기(2) : 0;
            int dane_WARTOŚĆ = systemy_informacyjne_zapis_zabieg && Word_SMS(deskryptor_stała, "(I)V") ? 빼기(1) : 0, obiekt_odwołanie = 빼기(2);
            if (!obiekt_WARTOŚĆ(obiekt_odwołanie, 19)) return; int nadrzędny_odwołanie = sterta_WARTOŚĆ[obiekt_odwołanie + 2], 열린파일번호 = sterta_WARTOŚĆ[nadrzędny_odwołanie + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Word_SMS(nazwa_stała, "close") && Word_SMS(deskryptor_stała, "()V")) { przestrzeń_użytkownika.Zamknij_Plik_deskryptor(열린파일번호); sterta_WARTOŚĆ[nadrzędny_odwołanie + 2] = -1; return; }
            if (Word_SMS(nazwa_stała, "flush") && Word_SMS(deskryptor_stała, "()V")) return;
            if ((!읽기여부 && !systemy_informacyjne_zapis_zabieg) || 읽기여부 != (sterta_WARTOŚĆ[obiekt_odwołanie + 3] == 0)) { awaria_WARTOŚĆ("unsupported stream operation"); return; }
            if (blok || systemy_informacyjne_PODTABLICA) { if (!obiekt_WARTOŚĆ(dane_TABLICA, 20)) return; if (blok) wpis_ILE_LICZB = sterta_WARTOŚĆ[dane_TABLICA + 1]; if (시작변위 < 0 || wpis_ILE_LICZB < 0 || 시작변위 > sterta_WARTOŚĆ[dane_TABLICA + 1] - wpis_ILE_LICZB) { 예외던짐(6, "stream array bounds"); return; } }
            else wpis_ILE_LICZB = 1;
            if (wpis_ILE_LICZB == 0) { if (읽기여부) 넣기(0, 1); return; }
            int Wykonane_ILE_LICZB = systemy_informacyjne_zapis_zabieg ? sterta_WARTOŚĆ[obiekt_odwołanie + 4] : 0, 처리값 = 0;
            while (Wykonane_ILE_LICZB < wpis_ILE_LICZB) {
                처리값 = 읽기여부 ? przestrzeń_użytkownika.파일한바이트읽기(열린파일번호) : przestrzeń_użytkownika.파일한바이트쓰기(열린파일번호, blok || systemy_informacyjne_PODTABLICA ? sterta_WARTOŚĆ[dane_TABLICA + 2 + 시작변위 + Wykonane_ILE_LICZB] : dane_WARTOŚĆ);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (blok || systemy_informacyjne_PODTABLICA)) sterta_WARTOŚĆ[dane_TABLICA + 2 + 시작변위 + Wykonane_ILE_LICZB] = (byte)처리값;
                Wykonane_ILE_LICZB++; if (읽기여부 && !(blok || systemy_informacyjne_PODTABLICA)) break;
            }
            if (처리값 == -11 && (systemy_informacyjne_zapis_zabieg || Wykonane_ILE_LICZB == 0)) {
                sterta_WARTOŚĆ[obiekt_odwołanie + 4] = Wykonane_ILE_LICZB;
                if (흐름대기(nadrzędny_odwołanie)) { 넣기(obiekt_odwołanie, 2); if (blok || systemy_informacyjne_PODTABLICA) 넣기(dane_TABLICA, 2); if (systemy_informacyjne_PODTABLICA) { 넣기(시작변위, 1); 넣기(wpis_ILE_LICZB, 1); } if (systemy_informacyjne_zapis_zabieg && !(blok || systemy_informacyjne_PODTABLICA)) 넣기(dane_WARTOŚĆ, 1); } return;
            }
            sterta_WARTOŚĆ[obiekt_odwołanie + 4] = 0; sterta_WARTOŚĆ[nadrzędny_odwołanie + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(Wykonane_ILE_LICZB == 0 && 처리값 == 256 ? -1 : blok || systemy_informacyjne_PODTABLICA ? Wykonane_ILE_LICZB : 처리값, 1); return;
        }
        awaria_WARTOŚĆ("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int nazwa_stała) {
        if (Word_SMS(nazwa_stała, "polski/własny/Okno")) return 24;
        if (Word_SMS(nazwa_stała, "polski/własny/Etykieta")) return 26;
        if (Word_SMS(nazwa_stała, "polski/własny/przycisk")) return 27;
        if (Word_SMS(nazwa_stała, "polski/własny/pole_tekstowe")) return 28;
        if (Word_SMS(nazwa_stała, "polski/własny/akcja_powiadomienie")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int nazwa_stała) {
        return 한국어화면종(nazwa_stała) != 0 || Word_SMS(nazwa_stała, "polski/własny/화면구성요소") || Word_SMS(nazwa_stała, "polski/własny/konkurs_kolejka");
    }
    static int 화면종(int nazwa_stała) {
        int 한국어종 = 한국어화면종(nazwa_stała); if (한국어종 != 0) return 한국어종;
        if (Word_SMS(nazwa_stała, "javax/swing/JFrame")) return 24;
        if (Word_SMS(nazwa_stała, "javax/swing/JPanel")) return 25;
        if (Word_SMS(nazwa_stała, "javax/swing/JLabel")) return 26;
        if (Word_SMS(nazwa_stała, "javax/swing/JButton")) return 27;
        if (Word_SMS(nazwa_stała, "javax/swing/JTextField")) return 28;
        if (Word_SMS(nazwa_stała, "java/awt/event/ActionEvent")) return 29;
        if (Word_SMS(nazwa_stała, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int nazwa_stała) {
        return 화면종(nazwa_stała) != 0 || Word_SMS(nazwa_stała, "java/awt/Component") || Word_SMS(nazwa_stała, "java/awt/Container") || Word_SMS(nazwa_stała, "javax/swing/JComponent") || Word_SMS(nazwa_stała, "javax/swing/AbstractButton") || Word_SMS(nazwa_stała, "javax/swing/text/JTextComponent") || Word_SMS(nazwa_stała, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int obiekt_odwołanie) { if (!systemy_informacyjne_prawidłowy_obiekt(obiekt_odwołanie)) return false; if (sterta_WARTOŚĆ[obiekt_odwołanie] < 24 || sterta_WARTOŚĆ[obiekt_odwołanie] > 28) { awaria_WARTOŚĆ("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int obiekt_odwołanie, int SMS_odwołanie) {
        if (SMS_odwołanie != 0 && !obiekt_WARTOŚĆ(SMS_odwołanie, 1)) return;
        int wpis_ILE_LICZB = SMS_odwołanie == 0 ? 0 : sterta_WARTOŚĆ[SMS_odwołanie + 1]; if (wpis_ILE_LICZB > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int Loop_INDEKS = 0; Loop_INDEKS < wpis_ILE_LICZB; Loop_INDEKS++) 화면글임시[Loop_INDEKS] = sterta_WARTOŚĆ[SMS_odwołanie + 2 + Loop_INDEKS];
        if (przestrzeń_użytkownika.화면글(sterta_WARTOŚĆ[obiekt_odwołanie + 2], 화면글임시, wpis_ILE_LICZB) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        sterta_WARTOŚĆ[obiekt_odwołanie + 3] = SMS_odwołanie; sterta_odwołanie[obiekt_odwołanie + 3] = 1;
    }
    static int 화면문자읽기(int obiekt_odwołanie) {
        int konto_WARTOŚĆ = sterta_WARTOŚĆ[obiekt_odwołanie + 2], wpis_ILE_LICZB = przestrzeń_użytkownika.화면연결(8, konto_WARTOŚĆ, 0, 0, 0, 0), 사용수 = 0;
        if (wpis_ILE_LICZB < 0) { awaria_WARTOŚĆ("GUI text read failed"); return 0; }
        for (int Loop_INDEKS = 0; Loop_INDEKS < wpis_ILE_LICZB; Loop_INDEKS++) { int 부호값 = przestrzeń_użytkownika.화면연결(9, konto_WARTOŚĆ, Loop_INDEKS, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = przydzielić_Pamięć(1, 사용수); if (!błąd) for (int Loop_INDEKS = 0; Loop_INDEKS < 사용수; Loop_INDEKS++) sterta_WARTOŚĆ[반환값 + 2 + Loop_INDEKS] = 화면글임시[Loop_INDEKS]; return 반환값;
    }
    /* polski 객체를 직접 만들고 jądro_WARTOŚĆ 화면 기능에 연결한다. Swing obiekt_WARTOŚĆ/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int właściciel, int nazwa_stała, int deskryptor_stała, int polecenie_KOD) {
        if (Word_SMS(właściciel, "polski/własny/konkurs_kolejka")) {
            if (polecenie_KOD == 184 && Word_SMS(nazwa_stała, "나중에실행") && Word_SMS(deskryptor_stała, "(Lpolski/własny/실행할일;)V")) {
                int zadanie_akcja = 빼기(2); if (!systemy_informacyjne_prawidłowy_obiekt(zadanie_akcja)) return;
                if (나중수 == 8) { awaria_WARTOŚĆ("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = zadanie_akcja; return;
            }
            if (polecenie_KOD == 184 && Word_SMS(nazwa_stała, "사건처리중인가") && Word_SMS(deskryptor_stała, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            awaria_WARTOŚĆ("지원하지 않는 polski 화면 일정 호출"); return;
        }
        if (Word_SMS(właściciel, "polski/własny/akcja_powiadomienie")) {
            int powiadomienie = 빼기(2); if (!obiekt_WARTOŚĆ(powiadomienie, 29) || sterta_WARTOŚĆ[powiadomienie + 3] == 0) return;
            if (Word_SMS(nazwa_stała, "źródło_zdarzenia") && Word_SMS(deskryptor_stała, "()Lpolski/własny/화면구성요소;")) 넣기(sterta_WARTOŚĆ[powiadomienie + 2], 2);
            else if (Word_SMS(nazwa_stała, "polecenie_SMS") && Word_SMS(deskryptor_stała, "()Ljava/lang/String;")) 넣기(화면문자읽기(sterta_WARTOŚĆ[powiadomienie + 2]), 2);
            else if (Word_SMS(nazwa_stała, "INDEKS") && Word_SMS(deskryptor_stała, "()I")) 넣기(1001, 1);
            else awaria_WARTOŚĆ("지원하지 않는 polski Akcja powiadomienie 호출"); return;
        }
        if (polecenie_KOD == 183 && Word_SMS(nazwa_stała, "<init>")) {
            int Rodzaj_WARTOŚĆ = 한국어화면종(właściciel), 받이 = 0, 가로 = 0, gałąź_stanowisko = 0, 폭 = 0, wysokość_WARTOŚĆ = 0;
            if (Rodzaj_WARTOŚĆ == 24 && Word_SMS(deskryptor_stała, "(Ljava/lang/String;II)V")) {
                wysokość_WARTOŚĆ = 빼기(1); 폭 = 빼기(1); 가로 = (przestrzeń_użytkownika.화면너비() - 폭) / 2; gałąź_stanowisko = (przestrzeń_użytkownika.화면높이() - wysokość_WARTOŚĆ) / 2;
            } else if ((Rodzaj_WARTOŚĆ == 26 || Rodzaj_WARTOŚĆ == 28) && Word_SMS(deskryptor_stała, "(Ljava/lang/String;IIII)V") || Rodzaj_WARTOŚĆ == 27 && Word_SMS(deskryptor_stała, "(Ljava/lang/String;IIIILpolski/własny/동작받이;)V")) {
                if (Rodzaj_WARTOŚĆ == 27) 받이 = 빼기(2);
                wysokość_WARTOŚĆ = 빼기(1); 폭 = 빼기(1); gałąź_stanowisko = 빼기(1); 가로 = 빼기(1);
            } else { awaria_WARTOŚĆ("지원하지 않는 polski 화면 생성자"); return; }
            int tekst = 빼기(2), element_WARTOŚĆ = 빼기(2); if (!화면객체(element_WARTOŚĆ)) return;
            if (폭 < 1 || wysokość_WARTOŚĆ < 1 || 가로 < 0 || gałąź_stanowisko < 0 || 폭 > przestrzeń_użytkownika.화면너비() - 가로 || wysokość_WARTOŚĆ > przestrzeń_użytkownika.화면높이() - gałąź_stanowisko) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int INDEKS = przestrzeń_użytkownika.화면연결(0, Rodzaj_WARTOŚĆ - 23, 0, 0, 0, 0);
            if (INDEKS < 1 || INDEKS > 32) { awaria_WARTOŚĆ("화면 element_WARTOŚĆ 자리가 가득 찼습니다"); return; }
            sterta_WARTOŚĆ[element_WARTOŚĆ + 2] = INDEKS; 화면참조[INDEKS - 1] = element_WARTOŚĆ;
            sterta_WARTOŚĆ[element_WARTOŚĆ + 5] = 가로; sterta_WARTOŚĆ[element_WARTOŚĆ + 6] = gałąź_stanowisko; sterta_WARTOŚĆ[element_WARTOŚĆ + 7] = 폭; sterta_WARTOŚĆ[element_WARTOŚĆ + 8] = wysokość_WARTOŚĆ; sterta_WARTOŚĆ[element_WARTOŚĆ + 10] = 2;
            sterta_WARTOŚĆ[element_WARTOŚĆ + 4] = 받이; sterta_odwołanie[element_WARTOŚĆ + 4] = 1; sterta_WARTOŚĆ[element_WARTOŚĆ + 12] = 1;
            przestrzeń_użytkownika.화면연결(1, INDEKS, 가로, gałąź_stanowisko, 폭, wysokość_WARTOŚĆ);
            if (Rodzaj_WARTOŚĆ == 24) przestrzeń_użytkownika.화면연결(7, INDEKS, 2, 0, 0, 0);
            화면문자설정(element_WARTOŚĆ, tekst); return;
        }
        if (polecenie_KOD != 182) { awaria_WARTOŚĆ("잘못된 polski 화면 호출 polecenie"); return; }
        if (Word_SMS(nazwa_stała, "zapis_SMS") && Word_SMS(deskryptor_stała, "(Ljava/lang/String;)V")) {
            int tekst = 빼기(2), element_WARTOŚĆ = 빼기(2); if (화면객체(element_WARTOŚĆ)) 화면문자설정(element_WARTOŚĆ, tekst); return;
        }
        if (Word_SMS(nazwa_stała, "글읽기") && Word_SMS(deskryptor_stała, "()Ljava/lang/String;")) {
            int element_WARTOŚĆ = 빼기(2); if (화면객체(element_WARTOŚĆ)) 넣기(화면문자읽기(element_WARTOŚĆ), 2); return;
        }
        if (Word_SMS(nazwa_stała, "동작맡기기") && Word_SMS(deskryptor_stała, "(Lpolski/własny/동작받이;)V")) {
            int 받이 = 빼기(2), element_WARTOŚĆ = 빼기(2);
            if (화면객체(element_WARTOŚĆ)) { sterta_WARTOŚĆ[element_WARTOŚĆ + 4] = 받이; sterta_odwołanie[element_WARTOŚĆ + 4] = 1; sterta_WARTOŚĆ[element_WARTOŚĆ + 12] = 1; } return;
        }
        if (Word_SMS(nazwa_stała, "Dodaj_element") && Word_SMS(deskryptor_stała, "(Lpolski/własny/화면구성요소;)V")) {
            int dziecko_WARTOŚĆ = 빼기(2), nadrzędny_WARTOŚĆ = 빼기(2); if (!화면객체(dziecko_WARTOŚĆ) || !화면객체(nadrzędny_WARTOŚĆ)) return;
            if (przestrzeń_użytkownika.화면연결(2, sterta_WARTOŚĆ[nadrzędny_WARTOŚĆ + 2], sterta_WARTOŚĆ[dziecko_WARTOŚĆ + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            sterta_WARTOŚĆ[dziecko_WARTOŚĆ + 11] = nadrzędny_WARTOŚĆ; sterta_odwołanie[dziecko_WARTOŚĆ + 11] = 1; return;
        }
        if (Word_SMS(nazwa_stała, "자리정하기") && Word_SMS(deskryptor_stała, "(IIII)V")) {
            int wysokość_WARTOŚĆ = 빼기(1), 폭 = 빼기(1), gałąź_stanowisko = 빼기(1), 가로 = 빼기(1), element_WARTOŚĆ = 빼기(2); if (!화면객체(element_WARTOŚĆ)) return;
            if (przestrzeń_użytkownika.화면연결(1, sterta_WARTOŚĆ[element_WARTOŚĆ + 2], 가로, gałąź_stanowisko, 폭, wysokość_WARTOŚĆ) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            sterta_WARTOŚĆ[element_WARTOŚĆ + 5] = 가로; sterta_WARTOŚĆ[element_WARTOŚĆ + 6] = gałąź_stanowisko; sterta_WARTOŚĆ[element_WARTOŚĆ + 7] = 폭; sterta_WARTOŚĆ[element_WARTOŚĆ + 8] = wysokość_WARTOŚĆ; return;
        }
        if ((Word_SMS(nazwa_stała, "program_okno") || Word_SMS(nazwa_stała, "Zamknięte")) && Word_SMS(deskryptor_stała, "()V")) {
            boolean Widoczność_WARTOŚĆ = Word_SMS(nazwa_stała, "program_okno"); int element_WARTOŚĆ = 빼기(2); if (!화면객체(element_WARTOŚĆ)) return;
            if (przestrzeń_użytkownika.화면연결(Widoczność_WARTOŚĆ ? 3 : 4, sterta_WARTOŚĆ[element_WARTOŚĆ + 2], Widoczność_WARTOŚĆ ? 1 : 0, 0, 0, 0) < 0) { awaria_WARTOŚĆ("화면은 interakcyjny 명령에서 실행해야 합니다"); return; }
            sterta_WARTOŚĆ[element_WARTOŚĆ + 9] = Widoczność_WARTOŚĆ ? 1 : 0; return;
        }
        if (Word_SMS(nazwa_stała, "보이는가") && Word_SMS(deskryptor_stała, "()Z")) { int element_WARTOŚĆ = 빼기(2); if (화면객체(element_WARTOŚĆ)) 넣기(sterta_WARTOŚĆ[element_WARTOŚĆ + 9], 1); return; }
        awaria_WARTOŚĆ("지원하지 않는 polski 화면 metoda_WARTOŚĆ");
    }
    static void 화면호출(int właściciel, int nazwa_stała, int deskryptor_stała, int polecenie_KOD) {
        if (Word_SMS(właściciel, "javax/swing/SwingUtilities")) {
            if (polecenie_KOD == 184 && Word_SMS(nazwa_stała, "invokeLater") && Word_SMS(deskryptor_stała, "(Ljava/lang/Runnable;)V")) { int obiekt_odwołanie = 빼기(2); if (!systemy_informacyjne_prawidłowy_obiekt(obiekt_odwołanie)) return; if (나중수 == 8) { awaria_WARTOŚĆ("invokeLater queue full"); return; } 나중실행[나중수++] = obiekt_odwołanie; return; }
            if (polecenie_KOD == 184 && Word_SMS(nazwa_stała, "isEventDispatchThread") && Word_SMS(deskryptor_stała, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            awaria_WARTOŚĆ("unsupported SwingUtilities method"); return;
        }
        if (Word_SMS(właściciel, "java/awt/event/ActionEvent")) {
            int obiekt_odwołanie = 빼기(2); if (!obiekt_WARTOŚĆ(obiekt_odwołanie, 29)) return;
            if (Word_SMS(nazwa_stała, "getSource") && Word_SMS(deskryptor_stała, "()Ljava/lang/Object;")) 넣기(sterta_WARTOŚĆ[obiekt_odwołanie + 2], 2);
            else if (Word_SMS(nazwa_stała, "getActionCommand") && Word_SMS(deskryptor_stała, "()Ljava/lang/String;")) 넣기(화면문자읽기(sterta_WARTOŚĆ[obiekt_odwołanie + 2]), 2);
            else if (Word_SMS(nazwa_stała, "getID") && Word_SMS(deskryptor_stała, "()I")) 넣기(1001, 1);
            else awaria_WARTOŚĆ("unsupported ActionEvent method"); return;
        }
        if (polecenie_KOD == 183 && Word_SMS(nazwa_stała, "<init>")) {
            int LICZBA_KOLUMN = 0, SMS_odwołanie = 0;
            if (Word_SMS(deskryptor_stała, "(I)V")) LICZBA_KOLUMN = 빼기(1);
            else if (Word_SMS(deskryptor_stała, "(Ljava/lang/String;I)V")) { LICZBA_KOLUMN = 빼기(1); SMS_odwołanie = 빼기(2); }
            else if (Word_SMS(deskryptor_stała, "(Ljava/lang/String;)V")) SMS_odwołanie = 빼기(2);
            else if (Word_SMS(deskryptor_stała, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Word_SMS(deskryptor_stała, "()V")) { awaria_WARTOŚĆ("unsupported Swing constructor"); return; }
            int obiekt_odwołanie = 빼기(2); if (!systemy_informacyjne_prawidłowy_obiekt(obiekt_odwołanie)) return;
            if (sterta_WARTOŚĆ[obiekt_odwołanie] == 30) { awaria_WARTOŚĆ("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(obiekt_odwołanie) || LICZBA_KOLUMN < 0) return;
            int konto_WARTOŚĆ = przestrzeń_użytkownika.화면연결(0, sterta_WARTOŚĆ[obiekt_odwołanie] - 23, 0, 0, 0, 0);
            if (konto_WARTOŚĆ < 1 || konto_WARTOŚĆ > 32) { awaria_WARTOŚĆ("GUI widget slots exhausted"); return; }
            sterta_WARTOŚĆ[obiekt_odwołanie + 2] = konto_WARTOŚĆ; 화면참조[konto_WARTOŚĆ - 1] = obiekt_odwołanie; sterta_WARTOŚĆ[obiekt_odwołanie + 5] = sterta_WARTOŚĆ[obiekt_odwołanie] == 24 ? 130 : 16; sterta_WARTOŚĆ[obiekt_odwołanie + 6] = sterta_WARTOŚĆ[obiekt_odwołanie] == 24 ? 110 : 16;
            sterta_WARTOŚĆ[obiekt_odwołanie + 7] = sterta_WARTOŚĆ[obiekt_odwołanie] == 24 ? 380 : 220; sterta_WARTOŚĆ[obiekt_odwołanie + 8] = sterta_WARTOŚĆ[obiekt_odwołanie] == 24 ? 240 : 28; sterta_WARTOŚĆ[obiekt_odwołanie + 10] = 1;
            화면문자설정(obiekt_odwołanie, SMS_odwołanie); return;
        }
        if (Word_SMS(nazwa_stała, "setText") || Word_SMS(nazwa_stała, "setTitle")) { int SMS_odwołanie = 빼기(2), obiekt_odwołanie = 빼기(2); if (화면객체(obiekt_odwołanie) && Word_SMS(deskryptor_stała, "(Ljava/lang/String;)V")) 화면문자설정(obiekt_odwołanie, SMS_odwołanie); return; }
        if (Word_SMS(nazwa_stała, "getText") || Word_SMS(nazwa_stała, "getTitle")) { int obiekt_odwołanie = 빼기(2); if (화면객체(obiekt_odwołanie) && Word_SMS(deskryptor_stała, "()Ljava/lang/String;")) 넣기(화면문자읽기(obiekt_odwołanie), 2); return; }
        if (Word_SMS(nazwa_stała, "addActionListener") && Word_SMS(deskryptor_stała, "(Ljava/awt/event/ActionListener;)V")) { int odbierać_odwołanie = 빼기(2), obiekt_odwołanie = 빼기(2); if (화면객체(obiekt_odwołanie)) { sterta_WARTOŚĆ[obiekt_odwołanie + 4] = odbierać_odwołanie; sterta_odwołanie[obiekt_odwołanie + 4] = 1; } return; }
        if (Word_SMS(nazwa_stała, "getContentPane") && Word_SMS(deskryptor_stała, "()Ljava/awt/Container;")) { int obiekt_odwołanie = 빼기(2); if (화면객체(obiekt_odwołanie)) 넣기(obiekt_odwołanie, 2); return; }
        if (Word_SMS(nazwa_stała, "setLayout") && Word_SMS(deskryptor_stała, "(Ljava/awt/LayoutManager;)V")) { int Układ_odwołanie = 빼기(2), obiekt_odwołanie = 빼기(2); if (화면객체(obiekt_odwołanie) && Układ_odwołanie != 0) awaria_WARTOŚĆ("only absolute layout (null) is supported"); return; }
        if (Word_SMS(nazwa_stała, "add") && (Word_SMS(deskryptor_stała, "(Ljava/awt/Component;)Ljava/awt/Component;") || Word_SMS(deskryptor_stała, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean Układ_choroba = Word_SMS(deskryptor_stała, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (Układ_choroba) 빼기(2);
            int dziecko_odwołanie = 빼기(2), obiekt_odwołanie = 빼기(2); if (!화면객체(dziecko_odwołanie) || !화면객체(obiekt_odwołanie)) return;
            if (przestrzeń_użytkownika.화면연결(2, sterta_WARTOŚĆ[obiekt_odwołanie + 2], sterta_WARTOŚĆ[dziecko_odwołanie + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            sterta_WARTOŚĆ[dziecko_odwołanie + 11] = obiekt_odwołanie; sterta_odwołanie[dziecko_odwołanie + 11] = 1; if (!Układ_choroba) 넣기(dziecko_odwołanie, 2); return;
        }
        if (Word_SMS(nazwa_stała, "setBounds") && Word_SMS(deskryptor_stała, "(IIII)V")) {
            int wysokość_WARTOŚĆ = 빼기(1), 너비 = 빼기(1), Y_współrzędna = 빼기(1), współrzędna_X = 빼기(1), obiekt_odwołanie = 빼기(2); if (!화면객체(obiekt_odwołanie)) return;
            if (przestrzeń_użytkownika.화면연결(1, sterta_WARTOŚĆ[obiekt_odwołanie + 2], współrzędna_X, Y_współrzędna, 너비, wysokość_WARTOŚĆ) < 0) { 예외던짐(9, "GUI bounds"); return; }
            sterta_WARTOŚĆ[obiekt_odwołanie + 5] = współrzędna_X; sterta_WARTOŚĆ[obiekt_odwołanie + 6] = Y_współrzędna; sterta_WARTOŚĆ[obiekt_odwołanie + 7] = 너비; sterta_WARTOŚĆ[obiekt_odwołanie + 8] = wysokość_WARTOŚĆ; return;
        }
        if (Word_SMS(nazwa_stała, "setSize") && Word_SMS(deskryptor_stała, "(II)V")) {
            int wysokość_WARTOŚĆ = 빼기(1), 너비 = 빼기(1), obiekt_odwołanie = 빼기(2); if (!화면객체(obiekt_odwołanie)) return;
            if (przestrzeń_użytkownika.화면연결(1, sterta_WARTOŚĆ[obiekt_odwołanie + 2], sterta_WARTOŚĆ[obiekt_odwołanie + 5], sterta_WARTOŚĆ[obiekt_odwołanie + 6], 너비, wysokość_WARTOŚĆ) < 0) 예외던짐(9, "GUI size"); else { sterta_WARTOŚĆ[obiekt_odwołanie + 7] = 너비; sterta_WARTOŚĆ[obiekt_odwołanie + 8] = wysokość_WARTOŚĆ; } return;
        }
        if (Word_SMS(nazwa_stała, "setLocationRelativeTo") && Word_SMS(deskryptor_stała, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), obiekt_odwołanie = 빼기(2); if (!화면객체(obiekt_odwołanie)) return; if (상대배치 != 0) { awaria_WARTOŚĆ("only screen centering supported"); return; } sterta_WARTOŚĆ[obiekt_odwołanie + 5] = (przestrzeń_użytkownika.화면너비() - sterta_WARTOŚĆ[obiekt_odwołanie + 7]) / 2; sterta_WARTOŚĆ[obiekt_odwołanie + 6] = (przestrzeń_użytkownika.화면높이() - sterta_WARTOŚĆ[obiekt_odwołanie + 8]) / 2; przestrzeń_użytkownika.화면연결(1, sterta_WARTOŚĆ[obiekt_odwołanie + 2], sterta_WARTOŚĆ[obiekt_odwołanie + 5], sterta_WARTOŚĆ[obiekt_odwołanie + 6], sterta_WARTOŚĆ[obiekt_odwołanie + 7], sterta_WARTOŚĆ[obiekt_odwołanie + 8]); return; }
        if (Word_SMS(nazwa_stała, "setDefaultCloseOperation") && Word_SMS(deskryptor_stała, "(I)V")) { int Policy = 빼기(1), obiekt_odwołanie = 빼기(2); if (화면객체(obiekt_odwołanie)) { if (Policy < 0 || Policy > 3) 예외던짐(9, "close policy"); else { sterta_WARTOŚĆ[obiekt_odwołanie + 10] = Policy; przestrzeń_użytkownika.화면연결(7, sterta_WARTOŚĆ[obiekt_odwołanie + 2], Policy, 0, 0, 0); } } return; }
        if (Word_SMS(nazwa_stała, "setVisible") && Word_SMS(deskryptor_stała, "(Z)V")) { int dane_WARTOŚĆ = 빼기(1), obiekt_odwołanie = 빼기(2); if (화면객체(obiekt_odwołanie)) { int 처리값 = przestrzeń_użytkownika.화면연결(3, sterta_WARTOŚĆ[obiekt_odwołanie + 2], dane_WARTOŚĆ, 0, 0, 0); if (처리값 < 0) awaria_WARTOŚĆ("Swing requires a standalone interactive command"); else sterta_WARTOŚĆ[obiekt_odwołanie + 9] = dane_WARTOŚĆ; } return; }
        if (Word_SMS(nazwa_stała, "dispose") && Word_SMS(deskryptor_stała, "()V")) { int obiekt_odwołanie = 빼기(2); if (화면객체(obiekt_odwołanie)) { przestrzeń_użytkownika.화면연결(4, sterta_WARTOŚĆ[obiekt_odwołanie + 2], 0, 0, 0, 0); sterta_WARTOŚĆ[obiekt_odwołanie + 9] = 0; } return; }
        if (Word_SMS(nazwa_stała, "repaint") || Word_SMS(nazwa_stała, "validate")) { int obiekt_odwołanie = 빼기(2); if (!화면객체(obiekt_odwołanie) || !Word_SMS(deskryptor_stała, "()V")) return; przestrzeń_użytkownika.화면연결(1, sterta_WARTOŚĆ[obiekt_odwołanie + 2], sterta_WARTOŚĆ[obiekt_odwołanie + 5], sterta_WARTOŚĆ[obiekt_odwołanie + 6], sterta_WARTOŚĆ[obiekt_odwołanie + 7], sterta_WARTOŚĆ[obiekt_odwołanie + 8]); return; }
        if (Word_SMS(nazwa_stała, "isVisible") && Word_SMS(deskryptor_stała, "()Z")) { int obiekt_odwołanie = 빼기(2); if (화면객체(obiekt_odwołanie)) 넣기(sterta_WARTOŚĆ[obiekt_odwołanie + 9], 1); return; }
        awaria_WARTOŚĆ("unsupported Swing method (native subset)");
    }
    static void wysłać_konkurs(int cel_ADRES, int konkurs_identyfikator, boolean polski) {
        if (cel_ADRES < 1 || sterta_WARTOŚĆ[cel_ADRES] < 32) { awaria_WARTOŚĆ("Java event listener required"); return; }
        int Plik_INDEKS = nazwa_metoda(sterta_WARTOŚĆ[cel_ADRES] - 32, konkurs_identyfikator == 0 ? (polski ? "Uruchom" : "run") : (polski ? "odbierać_akcja" : "actionPerformed"), konkurs_identyfikator == 0 ? "()V" : (polski ? "(Lpolski/własny/akcja_powiadomienie;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (Plik_INDEKS < 0) { awaria_WARTOŚĆ("event callback missing"); return; }
        bieżący_wątek = 0; liczba_wątków = 1; kadr_INDEKS = 0; wątek_Stan[0] = 1; kadr_Stos[0] = 0; kadr_blokada[0] = inicjuj_kadr[0] = 0; żądanie_zmiany = false;
        for (int Loop_INDEKS = 0; Loop_INDEKS < 128; Loop_INDEKS++) { lokalny_WARTOŚĆ[Loop_INDEKS] = lokalny_TYP[Loop_INDEKS] = 0; }
        kadr_metoda[0] = Plik_INDEKS; kadr_stanowisko[0] = metoda_START[Plik_INDEKS]; lokalny_WARTOŚĆ[0] = cel_ADRES; lokalny_TYP[0] = 2;
        if (konkurs_identyfikator != 0) { lokalny_WARTOŚĆ[1] = konkurs_identyfikator; lokalny_TYP[1] = 2; }
        사건중 = true; Wykonaj_polecenie(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!błąd) {
            if (나중수 > 0) { int cel_ADRES = 나중실행[0], polski = 나중한국어[0]; for (int Loop_INDEKS = 1; Loop_INDEKS < 나중수; Loop_INDEKS++) { 나중실행[Loop_INDEKS - 1] = 나중실행[Loop_INDEKS]; 나중한국어[Loop_INDEKS - 1] = 나중한국어[Loop_INDEKS]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; wysłać_konkurs(cel_ADRES, 0, polski != 0); continue; }
            if (przestrzeń_użytkownika.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int konkurs_identyfikator = przestrzeń_użytkownika.화면연결(5, 0, 0, 0, 0, 0); if (konkurs_identyfikator == 0) continue;
            if (konkurs_identyfikator < 0) { awaria_WARTOŚĆ("GUI event I/O failed"); return; }
            int konto_WARTOŚĆ = konkurs_identyfikator & 65535; if (konto_WARTOŚĆ < 1 || konto_WARTOŚĆ > 32) continue; int obiekt_odwołanie = 화면참조[konto_WARTOŚĆ - 1]; if (obiekt_odwołanie == 0) continue;
            if ((konkurs_identyfikator & 65536) != 0) {
                if (sterta_WARTOŚĆ[obiekt_odwołanie + 10] != 0) sterta_WARTOŚĆ[obiekt_odwołanie + 9] = 0;
                if (sterta_WARTOŚĆ[obiekt_odwołanie + 10] == 3) for (int Loop_INDEKS = 0; Loop_INDEKS < 32; Loop_INDEKS++) if (화면참조[Loop_INDEKS] != 0 && sterta_WARTOŚĆ[화면참조[Loop_INDEKS]] == 24) przestrzeń_użytkownika.화면연결(4, Loop_INDEKS + 1, 0, 0, 0, 0);
            } else if (sterta_WARTOŚĆ[obiekt_odwołanie + 4] != 0) {
                int plik_README_odwołanie = przydzielić_Pamięć(29, 2); if (błąd) return; sterta_WARTOŚĆ[plik_README_odwołanie + 2] = obiekt_odwołanie; sterta_WARTOŚĆ[plik_README_odwołanie + 3] = sterta_WARTOŚĆ[obiekt_odwołanie + 12]; sterta_odwołanie[plik_README_odwołanie + 2] = 1; wysłać_konkurs(sterta_WARTOŚĆ[obiekt_odwołanie + 4], plik_README_odwołanie, sterta_WARTOŚĆ[obiekt_odwołanie + 12] != 0);
            }
        }
    }
    public static int Uruchom_2() {
        if (przestrzeń_użytkownika.인수개수() == 1 && 자바도구.같음(przestrzeń_użytkownika.argumenty(0), "-version")) {
            przestrzeń_użytkownika.Zapis("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (przestrzeń_użytkownika.인수개수() < 1) { przestrzeń_użytkownika.Zapis("Usage: java CLASS [ARGS]\n"); return 2; }
        wpis_Klasa_Definicja = akta_Klasa_Definicja(host_znak(przestrzeń_użytkownika.argumenty(0))); if (błąd || wpis_Klasa_Definicja < 0) return 1;
        int punkt_wejścia_WARTOŚĆ = nazwa_metoda(wpis_Klasa_Definicja, "Uruchom_2", "()V");
        boolean 한국어진입 = punkt_wejścia_WARTOŚĆ >= 0 && (metoda_dostęp[punkt_wejścia_WARTOŚĆ] & 9) == 9;
        if (!한국어진입) punkt_wejścia_WARTOŚĆ = nazwa_metoda(wpis_Klasa_Definicja, "main", "([Ljava/lang/String;)V");
        if (punkt_wejścia_WARTOŚĆ < 0 || (metoda_dostęp[punkt_wejścia_WARTOŚĆ] & 9) != 9) awaria_WARTOŚĆ("public static void Uruchom_2() or main(String[] args) required");
        if (błąd) return 1;
        int argumenty = przydzielić_Pamięć(3, przestrzeń_użytkownika.인수개수() - 1); element_tablicy[argumenty] = -1;
        for (int identyfikator = 1; identyfikator < przestrzeń_użytkownika.인수개수() && !błąd; identyfikator++) sterta_WARTOŚĆ[argumenty + 1 + identyfikator] = host_znak(przestrzeń_użytkownika.argumenty(identyfikator));
        kadr_INDEKS = 0; kadr_metoda[0] = punkt_wejścia_WARTOŚĆ; kadr_stanowisko[0] = metoda_START[punkt_wejścia_WARTOŚĆ]; lokalny_WARTOŚĆ[0] = 한국어진입 ? 0 : argumenty; lokalny_TYP[0] = 한국어진입 ? 0 : 2;
        wątek_Stan[0] = 1; wątek_obiekt[0] = przydzielić_Pamięć(13, 2);
        Wykonaj_polecenie(); if (!błąd) 화면사건들(); return błąd ? 1 : 0;
    }
}
