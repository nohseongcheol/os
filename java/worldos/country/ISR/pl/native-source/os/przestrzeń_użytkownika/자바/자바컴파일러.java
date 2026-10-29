// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java źródło_drzewo -> 표준 버전 49 class kompilator. */
public final class 자바컴파일러 {
    static int[] plik_źródłowy = new int[16384], pozycja_wyjścia = new int[16384], KOD_WARTOŚĆ = new int[4096];
    static int[] token_Rodzaj = new int[2048], token_stanowisko = new int[2048], token_długość = new int[2048];
    static int[] stała_WARTOŚĆ = new int[4096], stała_przesunąć = new int[512];
    static int[] 문자 = new int[512], nazwa_pliku_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int źródło_zmienić_rozmiar, token_ILE_LICZB, pozycja, KOD_zmienić_rozmiar, stała_zmienić_rozmiar, stała_ILE_LICZB = 1, produkt_wyjściowy_zmienić_rozmiar, znak_długość;
    static boolean błąd;
    static int Klasa_token, Klasa_stała, nadrzędny_stała, KOD_stała;
    static int[] metoda_wpis_nazwa = new int[32], metoda_Zwrot = new int[32], metoda_argument_ILE_LICZB = new int[32];
    static int[] metoda_argument_nazwa = new int[512], metoda_argument_TYP = new int[512];
    static int[] treść_metody = new int[32], metoda_Koniec = new int[32], metoda_KOD = new int[32];
    static int[] metoda_długość = new int[32], 함수지역 = new int[32], metoda_nazwa_stała = new int[32], metoda_deskryptor_stała = new int[32];
    static int[] metoda_dostęp = new int[32];
    static int metoda_ILE_LICZB, bieżący_metoda, lokalny_ILE_LICZB, 깊이, 식깊이;
    static int[] lokalny_nazwa = new int[128], lokalny_TYP = new int[128], 지역깊이 = new int[128];

    static void awaria_WARTOŚĆ(String 이유) {
        if (!błąd) {
            przestrzeń_użytkownika.Zapis("javac error: "); przestrzeń_użytkownika.Zapis(이유);
            przestrzeń_użytkownika.Zapis(" at line ");
            int wiersz_wejścia = 1, 끝 = pozycja < token_ILE_LICZB ? token_stanowisko[pozycja] : źródło_zmienić_rozmiar;
            for (int identyfikator = 0; identyfikator < 끝; identyfikator++) if (plik_źródłowy[identyfikator] == 10) wiersz_wejścia++;
            자바도구.zapis_identyfikator(wiersz_wejścia); przestrzeń_użytkownika.zapis_znak_WARTOŚĆ(10);
        }
        błąd = true;
    }
    static boolean znak_WARTOŚĆ(int WARTOŚĆ) { return 문자이름규칙.첫글자(WARTOŚĆ); }
    static boolean cyfra_WARTOŚĆ(int WARTOŚĆ) { return WARTOŚĆ >= '0' && WARTOŚĆ <= '9'; }
    static boolean 이름같음(int 가, int SEKUNDA_operand) {
        if (가 < 0 || SEKUNDA_operand < 0 || 가 >= token_ILE_LICZB || SEKUNDA_operand >= token_ILE_LICZB || token_długość[가] != token_długość[SEKUNDA_operand]) return false;
        for (int identyfikator = 0; identyfikator < token_długość[가]; identyfikator++) if (plik_źródłowy[token_stanowisko[가] + identyfikator] != plik_źródłowy[token_stanowisko[SEKUNDA_operand] + identyfikator]) return false;
        return true;
    }
    static boolean Word_WARTOŚĆ(int token_WARTOŚĆ, String Word_SMS) {
        if (token_WARTOŚĆ < 0 || token_WARTOŚĆ >= token_ILE_LICZB || token_długość[token_WARTOŚĆ] != Word_SMS.length()) return false;
        for (int identyfikator = 0; identyfikator < Word_SMS.length(); identyfikator++) if (plik_źródłowy[token_stanowisko[token_WARTOŚĆ] + identyfikator] != Word_SMS.charAt(identyfikator)) return false;
        return true;
    }
    static int Rodzaj_WARTOŚĆ() { return pozycja < token_ILE_LICZB ? token_Rodzaj[pozycja] : 0; }
    static boolean odbierać(int WARTOŚĆ) { if (Rodzaj_WARTOŚĆ() != WARTOŚĆ) return false; pozycja++; return true; }
    static void wymaganie_WARTOŚĆ(int WARTOŚĆ) { if (!odbierać(WARTOŚĆ)) awaria_WARTOŚĆ("unexpected token"); }
    static boolean WYCINEK_Word(String Word_SMS) { if (!Word_WARTOŚĆ(pozycja, Word_SMS)) return false; pozycja++; return true; }
    static void 말요구(String Word_SMS) { if (!WYCINEK_Word(Word_SMS)) awaria_WARTOŚĆ(Word_SMS); }
    static int identyfikator_WARTOŚĆ() {
        int WYNIK = pozycja;
        if (Rodzaj_WARTOŚĆ() != 256) awaria_WARTOŚĆ("identifier required"); else pozycja++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int Uruchom_2 = 0;
        for (int identyfikator = 0; identyfikator <= 예약어.length(); identyfikator++) {
            if (identyfikator == 예약어.length() || 예약어.charAt(identyfikator) == ' ') {
                boolean 같음 = identyfikator - Uruchom_2 == token_długość[WYNIK];
                for (int gniazdo_wpis = Uruchom_2; 같음 && gniazdo_wpis < identyfikator; gniazdo_wpis++) if (예약어.charAt(gniazdo_wpis) != plik_źródłowy[token_stanowisko[WYNIK] + gniazdo_wpis - Uruchom_2]) 같음 = false;
                if (같음) awaria_WARTOŚĆ("reserved word cannot be an identifier");
                Uruchom_2 = identyfikator + 1;
            }
        }
        return WYNIK;
    }
    static void wyciąć_WARTOŚĆ() {
        int identyfikator = 0;
        while (identyfikator < źródło_zmienić_rozmiar && !błąd) {
            int WARTOŚĆ = plik_źródłowy[identyfikator], Uruchom_2 = identyfikator, Rodzaj_WARTOŚĆ = WARTOŚĆ;
            if (WARTOŚĆ == 32 || WARTOŚĆ == 9 || WARTOŚĆ == 10 || WARTOŚĆ == 13) { identyfikator++; continue; }
            if (WARTOŚĆ == '/' && identyfikator + 1 < źródło_zmienić_rozmiar && plik_źródłowy[identyfikator + 1] == '/') {
                while (identyfikator < źródło_zmienić_rozmiar && plik_źródłowy[identyfikator] != 10) identyfikator++;
                continue;
            }
            if (WARTOŚĆ == '/' && identyfikator + 1 < źródło_zmienić_rozmiar && plik_źródłowy[identyfikator + 1] == '*') {
                identyfikator += 2;
                while (identyfikator + 1 < źródło_zmienić_rozmiar && !(plik_źródłowy[identyfikator] == '*' && plik_źródłowy[identyfikator + 1] == '/')) identyfikator++;
                if (identyfikator + 1 >= źródło_zmienić_rozmiar) { awaria_WARTOŚĆ("unterminated comment"); break; }
                identyfikator += 2; continue;
            }
            if (znak_WARTOŚĆ(WARTOŚĆ)) { Rodzaj_WARTOŚĆ = 256; while (identyfikator < źródło_zmienić_rozmiar && 문자이름규칙.이어진글자(plik_źródłowy[identyfikator])) identyfikator++; }
            else if (cyfra_WARTOŚĆ(WARTOŚĆ)) { Rodzaj_WARTOŚĆ = 257; while (identyfikator < źródło_zmienić_rozmiar && cyfra_WARTOŚĆ(plik_źródłowy[identyfikator])) identyfikator++; }
            else if (WARTOŚĆ == '"' || WARTOŚĆ == '\'') {
                Rodzaj_WARTOŚĆ = WARTOŚĆ == '"' ? 258 : 259; identyfikator++;
                while (identyfikator < źródło_zmienić_rozmiar && plik_źródłowy[identyfikator] != WARTOŚĆ && plik_źródłowy[identyfikator] != 10 && plik_źródłowy[identyfikator] != 13) {
                    if (plik_źródłowy[identyfikator] == '\\') identyfikator++;
                    identyfikator++;
                }
                if (identyfikator >= źródło_zmienić_rozmiar || plik_źródłowy[identyfikator] != WARTOŚĆ) { awaria_WARTOŚĆ("unterminated literal"); break; }
                identyfikator++;
            } else {
                identyfikator++;
                if (identyfikator < źródło_zmienić_rozmiar) {
                    int Dalej_towar = plik_źródłowy[identyfikator];
                    if (WARTOŚĆ == '=' && Dalej_towar == '=') Rodzaj_WARTOŚĆ = 300;
                    if (WARTOŚĆ == '!' && Dalej_towar == '=') Rodzaj_WARTOŚĆ = 301;
                    if (WARTOŚĆ == '<' && Dalej_towar == '=') Rodzaj_WARTOŚĆ = 302;
                    if (WARTOŚĆ == '>' && Dalej_towar == '=') Rodzaj_WARTOŚĆ = 303;
                    if (WARTOŚĆ == '&' && Dalej_towar == '&') Rodzaj_WARTOŚĆ = 304;
                    if (WARTOŚĆ == '|' && Dalej_towar == '|') Rodzaj_WARTOŚĆ = 305;
                    if (WARTOŚĆ == '+' && Dalej_towar == '+') Rodzaj_WARTOŚĆ = 306;
                    if (WARTOŚĆ == '-' && Dalej_towar == '-') Rodzaj_WARTOŚĆ = 307;
                    if (WARTOŚĆ == '+' && Dalej_towar == '=') Rodzaj_WARTOŚĆ = 308;
                    if (WARTOŚĆ == '-' && Dalej_towar == '=') Rodzaj_WARTOŚĆ = 309;
                    if (WARTOŚĆ == '*' && Dalej_towar == '=') Rodzaj_WARTOŚĆ = 310;
                    if (WARTOŚĆ == '/' && Dalej_towar == '=') Rodzaj_WARTOŚĆ = 311;
                    if (WARTOŚĆ == '%' && Dalej_towar == '=') Rodzaj_WARTOŚĆ = 312;
                    if (Rodzaj_WARTOŚĆ >= 300) identyfikator++;
                }
            }
            if (token_ILE_LICZB == token_Rodzaj.length - 1) { awaria_WARTOŚĆ("too many tokens (2047 maximum)"); break; }
            token_Rodzaj[token_ILE_LICZB] = Rodzaj_WARTOŚĆ; token_stanowisko[token_ILE_LICZB] = Uruchom_2; token_długość[token_ILE_LICZB++] = identyfikator - Uruchom_2;
        }
    }
    static void zapis_stała_bajt(int WARTOŚĆ) {
        if (stała_zmienić_rozmiar == stała_WARTOŚĆ.length) { awaria_WARTOŚĆ("constant pool too large"); return; }
        stała_WARTOŚĆ[stała_zmienić_rozmiar++] = WARTOŚĆ & 255;
    }
    static void 상짧(int WARTOŚĆ) { zapis_stała_bajt(WARTOŚĆ >> 8); zapis_stała_bajt(WARTOŚĆ); }
    static int rejestr_stała(int Uruchom_2) {
        for (int identyfikator = 1; identyfikator < stała_ILE_LICZB; identyfikator++) {
            int przód_WARTOŚĆ = stała_przesunąć[identyfikator], długość_WARTOŚĆ = (identyfikator + 1 < stała_ILE_LICZB ? stała_przesunąć[identyfikator + 1] : Uruchom_2) - przód_WARTOŚĆ;
            if (długość_WARTOŚĆ != stała_zmienić_rozmiar - Uruchom_2) continue;
            boolean 같음 = true;
            for (int gniazdo_wpis = 0; gniazdo_wpis < długość_WARTOŚĆ; gniazdo_wpis++) if (stała_WARTOŚĆ[przód_WARTOŚĆ + gniazdo_wpis] != stała_WARTOŚĆ[Uruchom_2 + gniazdo_wpis]) 같음 = false;
            if (같음) { stała_zmienić_rozmiar = Uruchom_2; return identyfikator; }
        }
        if (stała_ILE_LICZB == stała_przesunąć.length) { awaria_WARTOŚĆ("too many constants"); return 0; }
        stała_przesunąć[stała_ILE_LICZB] = Uruchom_2;
        return stała_ILE_LICZB++;
    }
    static void dołączać_SMS(int WARTOŚĆ) {
        if (znak_długość == 문자.length) { awaria_WARTOŚĆ("text too long"); return; }
        문자[znak_długość++] = WARTOŚĆ;
    }
    static void dołączać_Word(String Word_SMS) { for (int identyfikator = 0; identyfikator < Word_SMS.length(); identyfikator++) dołączać_SMS(Word_SMS.charAt(identyfikator)); }
    static int znak_stała() {
        int Uruchom_2 = stała_zmienić_rozmiar; zapis_stała_bajt(1); 상짧(0);
        for (int identyfikator = 0; identyfikator < znak_długość; identyfikator++) {
            int WARTOŚĆ = 문자[identyfikator];
            if (WARTOŚĆ > 0 && WARTOŚĆ < 128) zapis_stała_bajt(WARTOŚĆ);
            else if (WARTOŚĆ < 2048) { zapis_stała_bajt(192 | WARTOŚĆ >> 6); zapis_stała_bajt(128 | WARTOŚĆ & 63); }
            else { zapis_stała_bajt(224 | WARTOŚĆ >> 12); zapis_stała_bajt(128 | WARTOŚĆ >> 6 & 63); zapis_stała_bajt(128 | WARTOŚĆ & 63); }
        }
        if (błąd) return 0;
        int długość_WARTOŚĆ = stała_zmienić_rozmiar - Uruchom_2 - 3;
        stała_WARTOŚĆ[Uruchom_2 + 1] = długość_WARTOŚĆ >> 8; stała_WARTOŚĆ[Uruchom_2 + 2] = długość_WARTOŚĆ & 255;
        return rejestr_stała(Uruchom_2);
    }
    static int Word_stała(String Word_SMS) { znak_długość = 0; dołączać_Word(Word_SMS); return znak_stała(); }
    static int token_stała(int token_WARTOŚĆ) {
        znak_długość = 0;
        for (int identyfikator = 0; identyfikator < token_długość[token_WARTOŚĆ]; identyfikator++) dołączać_SMS(plik_źródłowy[token_stanowisko[token_WARTOŚĆ] + identyfikator]);
        return znak_stała();
    }
    static int odwołanie(int Rodzaj_WARTOŚĆ, int 가, int SEKUNDA_operand) {
        int Uruchom_2 = stała_zmienić_rozmiar; zapis_stała_bajt(Rodzaj_WARTOŚĆ); 상짧(가);
        if (Rodzaj_WARTOŚĆ == 9 || Rodzaj_WARTOŚĆ == 10 || Rodzaj_WARTOŚĆ == 12) 상짧(SEKUNDA_operand);
        return rejestr_stała(Uruchom_2);
    }
    static int zewnętrzny_odwołanie(int Rodzaj_WARTOŚĆ, String właściciel_WARTOŚĆ, String Nazwa, String 서술) {
        int właściciel_identyfikator = odwołanie(7, Word_stała(właściciel_WARTOŚĆ), 0);
        int nazwa_ILE_LICZB = Word_stała(Nazwa), format_ILE_LICZB = Word_stała(서술);
        return odwołanie(Rodzaj_WARTOŚĆ, właściciel_identyfikator, odwołanie(12, nazwa_ILE_LICZB, format_ILE_LICZB));
    }
    static void 내보내기(int WARTOŚĆ) {
        if (KOD_zmienić_rozmiar == KOD_WARTOŚĆ.length) { awaria_WARTOŚĆ("bytecode too large"); return; }
        KOD_WARTOŚĆ[KOD_zmienić_rozmiar++] = WARTOŚĆ & 255;
    }
    static void polecenie(int WARTOŚĆ, int argumenty) { 내보내기(WARTOŚĆ); 내보내기(argumenty >> 8); 내보내기(argumenty); }
    static void 수상수(int WARTOŚĆ) {
        if (WARTOŚĆ >= -1 && WARTOŚĆ <= 5) { 내보내기(WARTOŚĆ + 3); return; }
        int Uruchom_2 = stała_zmienić_rozmiar; zapis_stała_bajt(3); 상짧(WARTOŚĆ >>> 16); 상짧(WARTOŚĆ);
        polecenie(19, rejestr_stała(Uruchom_2));
    }
    static int gałąź_22e01337(int polecenie) { int WYNIK = KOD_zmienić_rozmiar; polecenie(polecenie, 0); return WYNIK; }
    static void Link_WARTOŚĆ(int gałąź_22e01337, int cel_obiekt) {
        if (błąd) return;
        int 거리 = cel_obiekt - gałąź_22e01337;
        if (거리 < -32768 || 거리 > 32767 || gałąź_22e01337 < 0 || gałąź_22e01337 + 2 >= KOD_zmienić_rozmiar) { awaria_WARTOŚĆ("invalid branch"); return; }
        KOD_WARTOŚĆ[gałąź_22e01337 + 1] = 거리 >> 8 & 255; KOD_WARTOŚĆ[gałąź_22e01337 + 2] = 거리 & 255;
    }
    static void Porównanie_WARTOŚĆ(int polecenie) {
        int PRAWDA_WARTOŚĆ = gałąź_22e01337(polecenie); 내보내기(3); int 끝 = gałąź_22e01337(167);
        Link_WARTOŚĆ(PRAWDA_WARTOŚĆ, KOD_zmienić_rozmiar); 내보내기(4); Link_WARTOŚĆ(끝, KOD_zmienić_rozmiar);
    }
    static int format_WARTOŚĆ() {
        if (WYCINEK_Word("void")) return 0;
        if (WYCINEK_Word("int")) return 1;
        if (WYCINEK_Word("boolean")) return 2;
        if (WYCINEK_Word("char")) return 5;
        if (WYCINEK_Word("FileInputStream")) return 6;
        if (WYCINEK_Word("FileOutputStream")) return 7;
        if (WYCINEK_Word("String")) { if (odbierać('[')) { wymaganie_WARTOŚĆ(']'); return 4; } return 3; }
        awaria_WARTOŚĆ("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void Dodaj_format(int TYP_WARTOŚĆ) {
        if (TYP_WARTOŚĆ == 0) dołączać_SMS('V');
        if (TYP_WARTOŚĆ == 1) dołączać_SMS('I');
        if (TYP_WARTOŚĆ == 2) dołączać_SMS('Z');
        if (TYP_WARTOŚĆ == 3) dołączać_Word("Ljava/lang/String;");
        if (TYP_WARTOŚĆ == 4) dołączać_Word("[Ljava/lang/String;");
        if (TYP_WARTOŚĆ == 5) dołączać_SMS('C');
        if (TYP_WARTOŚĆ == 6) dołączać_Word("Ljava/io/FileInputStream;");
        if (TYP_WARTOŚĆ == 7) dołączać_Word("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws deklaracja. wyjątek Proces_WARTOŚĆ_wpis 본문은 host javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = WYCINEK_Word("polski");
        if (한국어묶음) { wymaganie_WARTOŚĆ('.'); 말요구("własny"); wymaganie_WARTOŚĆ('.'); }
        if (!한국어묶음 && (WYCINEK_Word("Exception") || WYCINEK_Word("IOException"))) return;
        if (WYCINEK_Word("wyjątek") || WYCINEK_Word("wykonanie_wyjątek") || WYCINEK_Word("We_Wy_wyjątek") || WYCINEK_Word("chwileczkę_TIMEOUT_wyjątek") || WYCINEK_Word("ADRES_WYSZUKAJ_wyjątek") || WYCINEK_Word("파일없음예외") || WYCINEK_Word("komunikacja_wyjątek") || WYCINEK_Word("nieważny_argument_wyjątek") || WYCINEK_Word("identyfikator_format_awaria") || WYCINEK_Word("범위예외") || WYCINEK_Word("granice_tablicy_wyjątek") || WYCINEK_Word("문자열범위예외") || WYCINEK_Word("pusta_referencja_wyjątek") || WYCINEK_Word("산술예외") || WYCINEK_Word("Stan_wyjątek") || WYCINEK_Word("TYP_koercja_wyjątek") || WYCINEK_Word("negatywny_TABLICA_zmienić_rozmiar_awaria") || WYCINEK_Word("TABLICA_Store_awaria") || WYCINEK_Word("wątek_Stan_wyjątek") || WYCINEK_Word("대기중단예외")) return;
        awaria_WARTOŚĆ("unsupported throws type");
    }
    static void 선언읽기() {
        while (WYCINEK_Word("import")) {
            if (Word_WARTOŚĆ(pozycja, "polski")) 예외이름읽기();
            else {
                말요구("java"); wymaganie_WARTOŚĆ('.'); 말요구("io"); wymaganie_WARTOŚĆ('.');
                if (!(WYCINEK_Word("FileInputStream") || WYCINEK_Word("FileOutputStream") || WYCINEK_Word("IOException"))) awaria_WARTOŚĆ("unsupported import");
            }
            wymaganie_WARTOŚĆ(';');
        }
        WYCINEK_Word("public"); WYCINEK_Word("final"); 말요구("class"); Klasa_token = identyfikator_WARTOŚĆ();
        Klasa_stała = odwołanie(7, token_stała(Klasa_token), 0);
        nadrzędny_stała = odwołanie(7, Word_stała("java/lang/Object"), 0); KOD_stała = Word_stała("Code"); wymaganie_WARTOŚĆ('{');
        while (!błąd && Rodzaj_WARTOŚĆ() != '}') {
            if (metoda_ILE_LICZB == 32) { awaria_WARTOŚĆ("too many methods"); break; }
            int dostęp_wpis = WYCINEK_Word("public") ? 1 : WYCINEK_Word("private") ? 2 : 0; 말요구("static");
            int FUNKCJA_WARTOŚĆ = metoda_ILE_LICZB++;
            metoda_dostęp[FUNKCJA_WARTOŚĆ] = dostęp_wpis | 8;
            metoda_Zwrot[FUNKCJA_WARTOŚĆ] = format_WARTOŚĆ(); metoda_wpis_nazwa[FUNKCJA_WARTOŚĆ] = identyfikator_WARTOŚĆ(); wymaganie_WARTOŚĆ('(');
            for (int przód_WARTOŚĆ = 0; przód_WARTOŚĆ < FUNKCJA_WARTOŚĆ; przód_WARTOŚĆ++) if (이름같음(metoda_wpis_nazwa[przód_WARTOŚĆ], metoda_wpis_nazwa[FUNKCJA_WARTOŚĆ])) awaria_WARTOŚĆ("duplicate method (overloading unsupported)");
            while (!błąd && Rodzaj_WARTOŚĆ() != ')') {
                int identyfikator = metoda_argument_ILE_LICZB[FUNKCJA_WARTOŚĆ];
                if (identyfikator == 16) { awaria_WARTOŚĆ("too many parameters"); break; }
                int TYP_WARTOŚĆ = format_WARTOŚĆ(); if (TYP_WARTOŚĆ == 0) awaria_WARTOŚĆ("void parameter");
                metoda_argument_TYP[FUNKCJA_WARTOŚĆ * 16 + identyfikator] = TYP_WARTOŚĆ; metoda_argument_nazwa[FUNKCJA_WARTOŚĆ * 16 + identyfikator] = identyfikator_WARTOŚĆ();
                metoda_argument_ILE_LICZB[FUNKCJA_WARTOŚĆ]++;
                if (!odbierać(',')) break;
            }
            wymaganie_WARTOŚĆ(')');
            if (WYCINEK_Word("throws")) {
                do { 예외이름읽기(); } while (!błąd && odbierać(','));
            }
            treść_metody[FUNKCJA_WARTOŚĆ] = pozycja; wymaganie_WARTOŚĆ('{');
            int zagnieżdżenie_WARTOŚĆ = 1;
            while (pozycja < token_ILE_LICZB && zagnieżdżenie_WARTOŚĆ > 0) {
                if (Rodzaj_WARTOŚĆ() == '{') zagnieżdżenie_WARTOŚĆ++;
                if (Rodzaj_WARTOŚĆ() == '}') zagnieżdżenie_WARTOŚĆ--;
                pozycja++;
            }
            if (zagnieżdżenie_WARTOŚĆ != 0) awaria_WARTOŚĆ("unclosed method body");
            metoda_Koniec[FUNKCJA_WARTOŚĆ] = pozycja;
            metoda_nazwa_stała[FUNKCJA_WARTOŚĆ] = token_stała(metoda_wpis_nazwa[FUNKCJA_WARTOŚĆ]);
            znak_długość = 0; dołączać_SMS('(');
            for (int identyfikator = 0; identyfikator < metoda_argument_ILE_LICZB[FUNKCJA_WARTOŚĆ]; identyfikator++) Dodaj_format(metoda_argument_TYP[FUNKCJA_WARTOŚĆ * 16 + identyfikator]);
            dołączać_SMS(')'); Dodaj_format(metoda_Zwrot[FUNKCJA_WARTOŚĆ]); metoda_deskryptor_stała[FUNKCJA_WARTOŚĆ] = znak_stała();
        }
        wymaganie_WARTOŚĆ('}'); if (pozycja != token_ILE_LICZB) awaria_WARTOŚĆ("extra input after class");
    }
    static int ZNAJDŹ_lokalny(int Nazwa) {
        for (int identyfikator = lokalny_ILE_LICZB - 1; identyfikator >= 0; identyfikator--) if (지역깊이[identyfikator] >= 0 && 이름같음(lokalny_nazwa[identyfikator], Nazwa)) return identyfikator;
        awaria_WARTOŚĆ("unknown variable"); return 0;
    }
    static int Dodaj_lokalny(int Nazwa, int TYP_WARTOŚĆ) {
        for (int identyfikator = 0; identyfikator < lokalny_ILE_LICZB; identyfikator++) if (지역깊이[identyfikator] >= 0 && 이름같음(lokalny_nazwa[identyfikator], Nazwa)) awaria_WARTOŚĆ("duplicate local variable");
        if (lokalny_ILE_LICZB == 128) { awaria_WARTOŚĆ("too many locals"); return 0; }
        lokalny_nazwa[lokalny_ILE_LICZB] = Nazwa; lokalny_TYP[lokalny_ILE_LICZB] = TYP_WARTOŚĆ; 지역깊이[lokalny_ILE_LICZB] = 깊이;
        return lokalny_ILE_LICZB++;
    }
    static boolean liczba_całkowita_TYP(int TYP_WARTOŚĆ) { return TYP_WARTOŚĆ == 1 || TYP_WARTOŚĆ == 5; }
    static void 지역읽기(int identyfikator) { 내보내기(lokalny_TYP[identyfikator] <= 2 || lokalny_TYP[identyfikator] == 5 ? 21 : 25); 내보내기(identyfikator); }
    static void zapis_lokalny(int identyfikator) { 내보내기(lokalny_TYP[identyfikator] <= 2 || lokalny_TYP[identyfikator] == 5 ? 54 : 58); 내보내기(identyfikator); }
    static void 형확인(int rzeczywisty_dane, int 기대) { if (rzeczywisty_dane != 기대 && !(rzeczywisty_dane == 5 && 기대 == 1)) awaria_WARTOŚĆ("type mismatch"); }
    static void 문자읽기(int token_WARTOŚĆ) {
        znak_długość = 0; int Uruchom_2 = token_stanowisko[token_WARTOŚĆ] + 1, 끝 = token_stanowisko[token_WARTOŚĆ] + token_długość[token_WARTOŚĆ] - 1;
        while (Uruchom_2 < 끝 && !błąd) {
            int WARTOŚĆ = plik_źródłowy[Uruchom_2++];
            if (WARTOŚĆ == '\\') {
                if (Uruchom_2 == 끝) { awaria_WARTOŚĆ("invalid escape"); break; }
                WARTOŚĆ = plik_źródłowy[Uruchom_2++];
                if (WARTOŚĆ == 'n') WARTOŚĆ = 10;
                else if (WARTOŚĆ == 'r') WARTOŚĆ = 13;
                else if (WARTOŚĆ == 't') WARTOŚĆ = 9;
                else if (WARTOŚĆ == 'b') WARTOŚĆ = 8;
                else if (WARTOŚĆ == 'f') WARTOŚĆ = 12;
                else if (WARTOŚĆ != '\\' && WARTOŚĆ != '"' && WARTOŚĆ != '\'') awaria_WARTOŚĆ("unsupported escape");
            }
            dołączać_SMS(WARTOŚĆ);
        }
    }
    static int analizować_liczba_całkowita(int token_WARTOŚĆ, boolean negatywny_WARTOŚĆ) {
        if (token_długość[token_WARTOŚĆ] > 1 && plik_źródłowy[token_stanowisko[token_WARTOŚĆ]] == '0') awaria_WARTOŚĆ("octal literals unsupported");
        int WARTOŚĆ = 0;
        for (int identyfikator = 0; identyfikator < token_długość[token_WARTOŚĆ]; identyfikator++) {
            int cyfra_towar = plik_źródłowy[token_stanowisko[token_WARTOŚĆ] + identyfikator] - '0';
            if (WARTOŚĆ < -214748364 || WARTOŚĆ == -214748364 && cyfra_towar > (negatywny_WARTOŚĆ ? 8 : 7)) awaria_WARTOŚĆ("integer literal out of range");
            WARTOŚĆ = WARTOŚĆ * 10 - cyfra_towar;
        }
        return negatywny_WARTOŚĆ ? WARTOŚĆ : -WARTOŚĆ;
    }
    static int 기본식() {
        if (WYCINEK_Word("new")) {
            int TYP_WARTOŚĆ = format_WARTOŚĆ();
            if (TYP_WARTOŚĆ != 6 && TYP_WARTOŚĆ != 7) { awaria_WARTOŚĆ("only file streams supported by new in source"); return 0; }
            String właściciel_WARTOŚĆ = TYP_WARTOŚĆ == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            polecenie(187, odwołanie(7, Word_stała(właściciel_WARTOŚĆ), 0)); 내보내기(89);
            wymaganie_WARTOŚĆ('('); 형확인(wyrażenie_WARTOŚĆ(), 3); boolean 이어 = false;
            if (odbierać(',')) { if (TYP_WARTOŚĆ != 7) awaria_WARTOŚĆ("input stream constructor arguments"); 형확인(wyrażenie_WARTOŚĆ(), 2); 이어 = true; }
            wymaganie_WARTOŚĆ(')');
            polecenie(183, zewnętrzny_odwołanie(10, właściciel_WARTOŚĆ, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return TYP_WARTOŚĆ;
        }
        if (odbierać('(')) { int TYP_WARTOŚĆ = wyrażenie_WARTOŚĆ(); wymaganie_WARTOŚĆ(')'); return TYP_WARTOŚĆ; }
        if (Rodzaj_WARTOŚĆ() == 257) { 수상수(analizować_liczba_całkowita(pozycja++, false)); return 1; }
        if (Rodzaj_WARTOŚĆ() == 258) { 문자읽기(pozycja++); polecenie(19, odwołanie(8, znak_stała(), 0)); return 3; }
        if (Rodzaj_WARTOŚĆ() == 259) { 문자읽기(pozycja++); if (znak_długość != 1) awaria_WARTOŚĆ("character literal length"); 수상수(문자[0]); return 5; }
        if (WYCINEK_Word("true")) { 내보내기(4); return 2; }
        if (WYCINEK_Word("false")) { 내보내기(3); return 2; }
        if (WYCINEK_Word("polski")) {
            wymaganie_WARTOŚĆ('.'); 말요구("własny"); wymaganie_WARTOŚĆ('.');
            String właściciel_WARTOŚĆ = "", metoda_WARTOŚĆ = "", 서술 = ""; int 가 = 0, SEKUNDA_operand = 0, 다 = 0, 라 = 0, 마 = 0, WYNIK = 0;
            if (WYCINEK_Word("pozycja_wyjścia")) {
                właściciel_WARTOŚĆ = "polski/własny/pozycja_wyjścia"; wymaganie_WARTOŚĆ('.');
                if (WYCINEK_Word("zapis_linia")) { metoda_WARTOŚĆ = "zapis_linia"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (WYCINEK_Word("Zapis")) { metoda_WARTOŚĆ = "Zapis"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (WYCINEK_Word("zapis_identyfikator")) { metoda_WARTOŚĆ = "zapis_identyfikator"; 서술 = "(I)V"; 가 = 1; }
                else awaria_WARTOŚĆ("unknown Korean output method");
            } else if (WYCINEK_Word("문자")) {
                właściciel_WARTOŚĆ = "polski/własny/문자"; wymaganie_WARTOŚĆ('.'); 가 = 3;
                if (WYCINEK_Word("długość_WARTOŚĆ")) { metoda_WARTOŚĆ = "długość_WARTOŚĆ"; 서술 = "(Ljava/lang/String;)I"; WYNIK = 1; }
                else if (WYCINEK_Word("kod_znaku_ILE_LICZB")) { metoda_WARTOŚĆ = "kod_znaku_ILE_LICZB"; 서술 = "(Ljava/lang/String;)I"; WYNIK = 1; }
                else if (WYCINEK_Word("analizować_liczba_całkowita")) { metoda_WARTOŚĆ = "analizować_liczba_całkowita"; 서술 = "(Ljava/lang/String;)I"; WYNIK = 1; }
                else if (WYCINEK_Word("zapis_liczba_całkowita_WARTOŚĆ")) { metoda_WARTOŚĆ = "zapis_liczba_całkowita_WARTOŚĆ"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; WYNIK = 3; }
                else if (WYCINEK_Word("같음")) { metoda_WARTOŚĆ = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; SEKUNDA_operand = 3; WYNIK = 2; }
                else if (WYCINEK_Word("wkleić_SMS")) { metoda_WARTOŚĆ = "wkleić_SMS"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; SEKUNDA_operand = 3; WYNIK = 3; }
                else if (WYCINEK_Word("wyciąć_WARTOŚĆ")) { metoda_WARTOŚĆ = "wyciąć_WARTOŚĆ"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; SEKUNDA_operand = 1; 다 = 1; WYNIK = 3; }
                else awaria_WARTOŚĆ("unknown Korean text method");
            } else if (WYCINEK_Word("nazwa_pliku")) {
                właściciel_WARTOŚĆ = "polski/własny/nazwa_pliku"; wymaganie_WARTOŚĆ('.'); 가 = 3;
                if (WYCINEK_Word("Odczyt")) { metoda_WARTOŚĆ = "Odczyt"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; WYNIK = 3; }
                else if (WYCINEK_Word("Zapis")) { metoda_WARTOŚĆ = "Zapis"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; SEKUNDA_operand = 3; }
                else awaria_WARTOŚĆ("unknown Korean file method");
            } else if (WYCINEK_Word("화면")) {
                właściciel_WARTOŚĆ = "polski/własny/화면"; wymaganie_WARTOŚĆ('.');
                if (WYCINEK_Word("너비")) { metoda_WARTOŚĆ = "너비"; 서술 = "()I"; WYNIK = 1; }
                else if (WYCINEK_Word("wysokość_WARTOŚĆ")) { metoda_WARTOŚĆ = "wysokość_WARTOŚĆ"; 서술 = "()I"; WYNIK = 1; }
                else if (WYCINEK_Word("prostokąt")) { metoda_WARTOŚĆ = "prostokąt"; 서술 = "(IIIII)V"; 가 = 1; SEKUNDA_operand = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (WYCINEK_Word("usunąć_wpis")) { metoda_WARTOŚĆ = "usunąć_wpis"; 서술 = "(I)V"; 가 = 1; }
                else if (WYCINEK_Word("기다리기")) { metoda_WARTOŚĆ = "기다리기"; 서술 = "()V"; }
                else awaria_WARTOŚĆ("unknown Korean framebuffer method");
            } else awaria_WARTOŚĆ("unsupported Korean library class");
            wymaganie_WARTOŚĆ('('); if (가 != 0) 형확인(wyrażenie_WARTOŚĆ(), 가);
            if (SEKUNDA_operand != 0) { wymaganie_WARTOŚĆ(','); 형확인(wyrażenie_WARTOŚĆ(), SEKUNDA_operand); }
            if (다 != 0) { wymaganie_WARTOŚĆ(','); 형확인(wyrażenie_WARTOŚĆ(), 다); }
            if (라 != 0) { wymaganie_WARTOŚĆ(','); 형확인(wyrażenie_WARTOŚĆ(), 라); }
            if (마 != 0) { wymaganie_WARTOŚĆ(','); 형확인(wyrażenie_WARTOŚĆ(), 마); }
            wymaganie_WARTOŚĆ(')'); polecenie(184, zewnętrzny_odwołanie(10, właściciel_WARTOŚĆ, metoda_WARTOŚĆ, 서술)); return WYNIK;
        }
        if (WYCINEK_Word("Integer")) {
            wymaganie_WARTOŚĆ('.'); 말요구("parseInt"); wymaganie_WARTOŚĆ('('); 형확인(wyrażenie_WARTOŚĆ(), 3); wymaganie_WARTOŚĆ(')');
            polecenie(184, zewnętrzny_odwołanie(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Nazwa = identyfikator_WARTOŚĆ();
        if (odbierać('(')) {
            int FUNKCJA_WARTOŚĆ = -1;
            for (int identyfikator = 0; identyfikator < metoda_ILE_LICZB; identyfikator++) if (이름같음(Nazwa, metoda_wpis_nazwa[identyfikator])) FUNKCJA_WARTOŚĆ = identyfikator;
            if (FUNKCJA_WARTOŚĆ < 0) { awaria_WARTOŚĆ("unknown static method"); return 0; }
            int identyfikator = 0;
            while (!błąd && Rodzaj_WARTOŚĆ() != ')') {
                if (identyfikator >= metoda_argument_ILE_LICZB[FUNKCJA_WARTOŚĆ]) { awaria_WARTOŚĆ("too many arguments"); break; }
                형확인(wyrażenie_WARTOŚĆ(), metoda_argument_TYP[FUNKCJA_WARTOŚĆ * 16 + identyfikator++]); if (!odbierać(',')) break;
            }
            wymaganie_WARTOŚĆ(')'); if (identyfikator != metoda_argument_ILE_LICZB[FUNKCJA_WARTOŚĆ]) awaria_WARTOŚĆ("argument count mismatch");
            polecenie(184, odwołanie(10, Klasa_stała, odwołanie(12, metoda_nazwa_stała[FUNKCJA_WARTOŚĆ], metoda_deskryptor_stała[FUNKCJA_WARTOŚĆ])));
            return metoda_Zwrot[FUNKCJA_WARTOŚĆ];
        }
        int lokalny_Scope = ZNAJDŹ_lokalny(Nazwa), TYP_WARTOŚĆ = lokalny_TYP[lokalny_Scope]; 지역읽기(lokalny_Scope);
        while (!błąd) {
            if (odbierać('[')) { 형확인(TYP_WARTOŚĆ, 4); 형확인(wyrażenie_WARTOŚĆ(), 1); wymaganie_WARTOŚĆ(']'); 내보내기(50); TYP_WARTOŚĆ = 3; }
            else if (odbierać('.')) {
                if (TYP_WARTOŚĆ == 6 || TYP_WARTOŚĆ == 7) {
                    String właściciel_WARTOŚĆ = TYP_WARTOŚĆ == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (WYCINEK_Word("close")) { wymaganie_WARTOŚĆ('('); wymaganie_WARTOŚĆ(')'); polecenie(182, zewnętrzny_odwołanie(10, właściciel_WARTOŚĆ, "close", "()V")); TYP_WARTOŚĆ = 0; }
                    else if (TYP_WARTOŚĆ == 6 && WYCINEK_Word("read")) { wymaganie_WARTOŚĆ('('); wymaganie_WARTOŚĆ(')'); polecenie(182, zewnętrzny_odwołanie(10, właściciel_WARTOŚĆ, "read", "()I")); TYP_WARTOŚĆ = 1; }
                    else if (TYP_WARTOŚĆ == 7 && WYCINEK_Word("write")) { wymaganie_WARTOŚĆ('('); 형확인(wyrażenie_WARTOŚĆ(), 1); wymaganie_WARTOŚĆ(')'); polecenie(182, zewnętrzny_odwołanie(10, właściciel_WARTOŚĆ, "write", "(I)V")); TYP_WARTOŚĆ = 0; }
                    else { awaria_WARTOŚĆ("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (TYP_WARTOŚĆ == 4) { 내보내기(190); TYP_WARTOŚĆ = 1; }
                else { 형확인(TYP_WARTOŚĆ, 3); wymaganie_WARTOŚĆ('('); wymaganie_WARTOŚĆ(')'); polecenie(182, zewnętrzny_odwołanie(10, "java/lang/String", "length", "()I")); TYP_WARTOŚĆ = 1; }
            } else break;
        }
        return TYP_WARTOŚĆ;
    }
    static int 단항() {
        if (++식깊이 > 64) { awaria_WARTOŚĆ("expression nesting too deep"); 식깊이--; return 0; }
        int TYP_WARTOŚĆ;
        if (odbierać('!')) { 형확인(단항(), 2); Porównanie_WARTOŚĆ(153); TYP_WARTOŚĆ = 2; }
        else if (odbierać('-')) {
            if (Rodzaj_WARTOŚĆ() == 257) 수상수(analizować_liczba_całkowita(pozycja++, true));
            else { 형확인(단항(), 1); 내보내기(116); }
            TYP_WARTOŚĆ = 1;
        } else if (odbierać('+')) { 형확인(단항(), 1); TYP_WARTOŚĆ = 1; }
        else TYP_WARTOŚĆ = 기본식();
        식깊이--; return TYP_WARTOŚĆ;
    }
    static int 곱식() {
        int TYP_WARTOŚĆ = 단항();
        while (!błąd && (Rodzaj_WARTOŚĆ() == '*' || Rodzaj_WARTOŚĆ() == '/' || Rodzaj_WARTOŚĆ() == '%')) {
            int Encoding_WARTOŚĆ = Rodzaj_WARTOŚĆ(); pozycja++; 형확인(TYP_WARTOŚĆ, 1); 형확인(단항(), 1);
            내보내기(Encoding_WARTOŚĆ == '*' ? 104 : Encoding_WARTOŚĆ == '/' ? 108 : 112); TYP_WARTOŚĆ = 1;
        }
        return TYP_WARTOŚĆ;
    }
    static int 합식() {
        int TYP_WARTOŚĆ = 곱식();
        while (!błąd && (Rodzaj_WARTOŚĆ() == '+' || Rodzaj_WARTOŚĆ() == '-')) {
            int Encoding_WARTOŚĆ = Rodzaj_WARTOŚĆ(); pozycja++; int granica_WARTOŚĆ = KOD_zmienić_rozmiar, BACK_typ_wartości = 곱식();
            if (Encoding_WARTOŚĆ == '+' && (TYP_WARTOŚĆ == 3 || BACK_typ_wartości == 3)) { 결합(granica_WARTOŚĆ, TYP_WARTOŚĆ, BACK_typ_wartości); TYP_WARTOŚĆ = 3; }
            else { 형확인(TYP_WARTOŚĆ, 1); 형확인(BACK_typ_wartości, 1); 내보내기(Encoding_WARTOŚĆ == '+' ? 96 : 100); TYP_WARTOŚĆ = 1; }
        }
        return TYP_WARTOŚĆ;
    }
    static int dołączone_odwołanie(int TYP_WARTOŚĆ) {
        if (TYP_WARTOŚĆ != 1 && TYP_WARTOŚĆ != 2 && TYP_WARTOŚĆ != 3 && TYP_WARTOŚĆ != 5) awaria_WARTOŚĆ("unsupported concatenation type");
        return zewnętrzny_odwołanie(10, "java/lang/StringBuilder", "append", TYP_WARTOŚĆ == 1 ? "(I)Ljava/lang/StringBuilder;"
            : TYP_WARTOŚĆ == 2 ? "(Z)Ljava/lang/StringBuilder;" : TYP_WARTOŚĆ == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int granica_WARTOŚĆ, int przód_typ_wartości, int BACK_typ_wartości) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 PRAWY KOD_WARTOŚĆ 앞에 generować 코드를 삽입한다.
        // PRAWY wyrażenie_WARTOŚĆ 내부의 węzeł_równorzędny_WARTOŚĆ gałąź_22e01337 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = KOD_zmienić_rozmiar;
        polecenie(187, odwołanie(7, Word_stała("java/lang/StringBuilder"), 0)); 내보내기(89);
        polecenie(183, zewnętrzny_odwołanie(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); polecenie(182, dołączone_odwołanie(przód_typ_wartości));
        if (błąd) return;
        int długość_WARTOŚĆ = KOD_zmienić_rozmiar - 끝;
        for (int identyfikator = 0; identyfikator < długość_WARTOŚĆ; identyfikator++) 삽입코드[identyfikator] = KOD_WARTOŚĆ[끝 + identyfikator];
        for (int identyfikator = 끝 - 1; identyfikator >= granica_WARTOŚĆ; identyfikator--) KOD_WARTOŚĆ[identyfikator + długość_WARTOŚĆ] = KOD_WARTOŚĆ[identyfikator];
        for (int identyfikator = 0; identyfikator < długość_WARTOŚĆ; identyfikator++) KOD_WARTOŚĆ[granica_WARTOŚĆ + identyfikator] = 삽입코드[identyfikator];
        polecenie(182, dołączone_odwołanie(BACK_typ_wartości)); polecenie(182, zewnętrzny_odwołanie(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int Porównanie_wyrażenie() {
        int TYP_WARTOŚĆ = 합식();
        while (!błąd && (Rodzaj_WARTOŚĆ() == '<' || Rodzaj_WARTOŚĆ() == '>' || Rodzaj_WARTOŚĆ() == 302 || Rodzaj_WARTOŚĆ() == 303)) {
            int Encoding_WARTOŚĆ = Rodzaj_WARTOŚĆ(); pozycja++; 형확인(TYP_WARTOŚĆ, 1); 형확인(합식(), 1);
            Porównanie_WARTOŚĆ(Encoding_WARTOŚĆ == '<' ? 161 : Encoding_WARTOŚĆ == '>' ? 163 : Encoding_WARTOŚĆ == 302 ? 164 : 162); TYP_WARTOŚĆ = 2;
        }
        return TYP_WARTOŚĆ;
    }
    static int 동등식() {
        int TYP_WARTOŚĆ = Porównanie_wyrażenie();
        while (!błąd && (Rodzaj_WARTOŚĆ() == 300 || Rodzaj_WARTOŚĆ() == 301)) {
            int Encoding_WARTOŚĆ = Rodzaj_WARTOŚĆ(); pozycja++; int BACK_typ_wartości = Porównanie_wyrażenie();
            if (TYP_WARTOŚĆ == 0 || BACK_typ_wartości == 0) awaria_WARTOŚĆ("void expression");
            if (!(liczba_całkowita_TYP(TYP_WARTOŚĆ) && liczba_całkowita_TYP(BACK_typ_wartości))) 형확인(BACK_typ_wartości, TYP_WARTOŚĆ);
            Porównanie_WARTOŚĆ((TYP_WARTOŚĆ <= 2 || TYP_WARTOŚĆ == 5 ? 159 : 165) + (Encoding_WARTOŚĆ == 301 ? 1 : 0)); TYP_WARTOŚĆ = 2;
        }
        return TYP_WARTOŚĆ;
    }
    static int ORAZ() {
        int TYP_WARTOŚĆ = 동등식();
        while (!błąd && odbierać(304)) {
            형확인(TYP_WARTOŚĆ, 2); int 가 = gałąź_22e01337(153); 형확인(동등식(), 2); int SEKUNDA_operand = gałąź_22e01337(153);
            내보내기(4); int 끝 = gałąź_22e01337(167); Link_WARTOŚĆ(가, KOD_zmienić_rozmiar); Link_WARTOŚĆ(SEKUNDA_operand, KOD_zmienić_rozmiar); 내보내기(3); Link_WARTOŚĆ(끝, KOD_zmienić_rozmiar); TYP_WARTOŚĆ = 2;
        }
        return TYP_WARTOŚĆ;
    }
    static int wyrażenie_WARTOŚĆ() {
        int TYP_WARTOŚĆ = ORAZ();
        while (!błąd && odbierać(305)) {
            형확인(TYP_WARTOŚĆ, 2); int 가 = gałąź_22e01337(154); 형확인(ORAZ(), 2); int SEKUNDA_operand = gałąź_22e01337(154);
            내보내기(3); int 끝 = gałąź_22e01337(167); Link_WARTOŚĆ(가, KOD_zmienić_rozmiar); Link_WARTOŚĆ(SEKUNDA_operand, KOD_zmienić_rozmiar); 내보내기(4); Link_WARTOŚĆ(끝, KOD_zmienić_rozmiar); TYP_WARTOŚĆ = 2;
        }
        return TYP_WARTOŚĆ;
    }
    static void zadanie_WARTOŚĆ(boolean Zezwalaj_deklaracja) {
        if (Word_WARTOŚĆ(pozycja, "int") || Word_WARTOŚĆ(pozycja, "boolean") || Word_WARTOŚĆ(pozycja, "String") || Word_WARTOŚĆ(pozycja, "char")
            || Word_WARTOŚĆ(pozycja, "FileInputStream") || Word_WARTOŚĆ(pozycja, "FileOutputStream")) {
            if (!Zezwalaj_deklaracja) awaria_WARTOŚĆ("declaration not allowed here");
            int TYP_WARTOŚĆ = format_WARTOŚĆ(), Nazwa = identyfikator_WARTOŚĆ(); wymaganie_WARTOŚĆ('='); 형확인(wyrażenie_WARTOŚĆ(), TYP_WARTOŚĆ);
            zapis_lokalny(Dodaj_lokalny(Nazwa, TYP_WARTOŚĆ)); return;
        }
        int Nazwa = identyfikator_WARTOŚĆ(), lokalny_Scope = ZNAJDŹ_lokalny(Nazwa);
        if (odbierać('=')) { 형확인(wyrażenie_WARTOŚĆ(), lokalny_TYP[lokalny_Scope]); zapis_lokalny(lokalny_Scope); }
        else if (Rodzaj_WARTOŚĆ() >= 308 && Rodzaj_WARTOŚĆ() <= 312) {
            int Encoding_WARTOŚĆ = Rodzaj_WARTOŚĆ(); pozycja++; 지역읽기(lokalny_Scope); int granica_WARTOŚĆ = KOD_zmienić_rozmiar, BACK_typ_wartości = wyrażenie_WARTOŚĆ();
            if (Encoding_WARTOŚĆ == 308 && lokalny_TYP[lokalny_Scope] == 3) 결합(granica_WARTOŚĆ, 3, BACK_typ_wartości);
            else {
                형확인(lokalny_TYP[lokalny_Scope], 1); 형확인(BACK_typ_wartości, 1);
                내보내기(Encoding_WARTOŚĆ == 308 ? 96 : Encoding_WARTOŚĆ == 309 ? 100 : Encoding_WARTOŚĆ == 310 ? 104 : Encoding_WARTOŚĆ == 311 ? 108 : 112);
                if (lokalny_TYP[lokalny_Scope] == 5) 내보내기(146);
            }
            zapis_lokalny(lokalny_Scope);
        }
        else if (Rodzaj_WARTOŚĆ() == 306 || Rodzaj_WARTOŚĆ() == 307) {
            형확인(lokalny_TYP[lokalny_Scope], 1); 내보내기(132); 내보내기(lokalny_Scope); 내보내기(Rodzaj_WARTOŚĆ() == 306 ? 1 : 255); pozycja++;
            if (lokalny_TYP[lokalny_Scope] == 5) { 지역읽기(lokalny_Scope); 내보내기(146); zapis_lokalny(lokalny_Scope); }
        } else awaria_WARTOŚĆ("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); wymaganie_WARTOŚĆ('.'); 말요구("out"); wymaganie_WARTOŚĆ('.');
        boolean 줄바꿈 = WYCINEK_Word("println"); if (!줄바꿈) 말요구("print"); wymaganie_WARTOŚĆ('(');
        polecenie(178, zewnętrzny_odwołanie(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean 빈인수 = Rodzaj_WARTOŚĆ() == ')';
        int TYP_WARTOŚĆ = 빈인수 ? 0 : wyrażenie_WARTOŚĆ(); wymaganie_WARTOŚĆ(')'); wymaganie_WARTOŚĆ(';');
        String 서술 = TYP_WARTOŚĆ == 0 ? "()V" : TYP_WARTOŚĆ == 1 ? "(I)V" : TYP_WARTOŚĆ == 2 ? "(Z)V" : TYP_WARTOŚĆ == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (TYP_WARTOŚĆ == 4 || TYP_WARTOŚĆ >= 6 || TYP_WARTOŚĆ == 0 && (!줄바꿈 || !빈인수)) awaria_WARTOŚĆ("unsupported print argument");
        polecenie(182, zewnętrzny_odwołanie(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean wyciąg_WARTOŚĆ() {
        if (błąd) return false;
        if (깊이 > 32) { awaria_WARTOŚĆ("statement nesting too deep"); return false; }
        if (odbierać('{')) {
            깊이++; boolean Zwrot_KR = false;
            while (!błąd && Rodzaj_WARTOŚĆ() != '}') { if (Zwrot_KR) awaria_WARTOŚĆ("unreachable statement"); Zwrot_KR = wyciąg_WARTOŚĆ(); }
            wymaganie_WARTOŚĆ('}'); for (int identyfikator = 0; identyfikator < lokalny_ILE_LICZB; identyfikator++) if (지역깊이[identyfikator] == 깊이) 지역깊이[identyfikator] = -1;
            깊이--; return Zwrot_KR;
        }
        if (odbierać(';')) return false;
        if (WYCINEK_Word("return")) {
            int TYP_WARTOŚĆ = Rodzaj_WARTOŚĆ() == ';' ? 0 : wyrażenie_WARTOŚĆ(); 형확인(TYP_WARTOŚĆ, metoda_Zwrot[bieżący_metoda]); wymaganie_WARTOŚĆ(';');
            내보내기(TYP_WARTOŚĆ == 0 ? 177 : TYP_WARTOŚĆ <= 2 || TYP_WARTOŚĆ == 5 ? 172 : 176); return true;
        }
        if (WYCINEK_Word("if")) {
            wymaganie_WARTOŚĆ('('); 형확인(wyrażenie_WARTOŚĆ(), 2); wymaganie_WARTOŚĆ(')'); int FAŁSZ_WARTOŚĆ = gałąź_22e01337(153);
            깊이++; boolean 가 = kontrola_wyciąg(); 깊이--;
            if (WYCINEK_Word("else")) { int 끝 = gałąź_22e01337(167); Link_WARTOŚĆ(FAŁSZ_WARTOŚĆ, KOD_zmienić_rozmiar); 깊이++; boolean SEKUNDA_operand = kontrola_wyciąg(); 깊이--; Link_WARTOŚĆ(끝, KOD_zmienić_rozmiar); return 가 && SEKUNDA_operand; }
            Link_WARTOŚĆ(FAŁSZ_WARTOŚĆ, KOD_zmienić_rozmiar); return false;
        }
        if (WYCINEK_Word("while")) {
            int Uruchom_2 = KOD_zmienić_rozmiar; wymaganie_WARTOŚĆ('('); 형확인(wyrażenie_WARTOŚĆ(), 2); wymaganie_WARTOŚĆ(')'); int 끝 = gałąź_22e01337(153);
            깊이++; kontrola_wyciąg(); 깊이--; Link_WARTOŚĆ(gałąź_22e01337(167), Uruchom_2); Link_WARTOŚĆ(끝, KOD_zmienić_rozmiar); return false;
        }
        if (WYCINEK_Word("for")) {
            깊이++; wymaganie_WARTOŚĆ('('); if (Rodzaj_WARTOŚĆ() != ';') zadanie_WARTOŚĆ(true); wymaganie_WARTOŚĆ(';');
            int choroba = KOD_zmienić_rozmiar; if (Rodzaj_WARTOŚĆ() == ';') 내보내기(4); else 형확인(wyrażenie_WARTOŚĆ(), 2); wymaganie_WARTOŚĆ(';');
            int 끝 = gałąź_22e01337(153), tekst_podstawowy = gałąź_22e01337(167), odświeżyć = KOD_zmienić_rozmiar;
            if (Rodzaj_WARTOŚĆ() != ')') zadanie_WARTOŚĆ(false); wymaganie_WARTOŚĆ(')'); Link_WARTOŚĆ(gałąź_22e01337(167), choroba); Link_WARTOŚĆ(tekst_podstawowy, KOD_zmienić_rozmiar);
            kontrola_wyciąg(); Link_WARTOŚĆ(gałąź_22e01337(167), odświeżyć); Link_WARTOŚĆ(끝, KOD_zmienić_rozmiar);
            for (int identyfikator = 0; identyfikator < lokalny_ILE_LICZB; identyfikator++) if (지역깊이[identyfikator] == 깊이) 지역깊이[identyfikator] = -1;
            깊이--; return false;
        }
        if (Word_WARTOŚĆ(pozycja, "System")) { 화면출력(); return false; }
        if (Rodzaj_WARTOŚĆ() == 256 && pozycja + 1 < token_ILE_LICZB && (token_Rodzaj[pozycja + 1] == '(' || token_Rodzaj[pozycja + 1] == '.')) {
            int TYP_WARTOŚĆ = wyrażenie_WARTOŚĆ(); if (TYP_WARTOŚĆ != 0) 내보내기(87); wymaganie_WARTOŚĆ(';'); return false;
        }
        zadanie_WARTOŚĆ(true); wymaganie_WARTOŚĆ(';'); return false;
    }
    static boolean kontrola_wyciąg() {
        if (Word_WARTOŚĆ(pozycja, "int") || Word_WARTOŚĆ(pozycja, "boolean") || Word_WARTOŚĆ(pozycja, "char") || Word_WARTOŚĆ(pozycja, "String")
            || Word_WARTOŚĆ(pozycja, "FileInputStream") || Word_WARTOŚĆ(pozycja, "FileOutputStream")) awaria_WARTOŚĆ("local declaration requires braces");
        return wyciąg_WARTOŚĆ();
    }
    static void 출바(int WARTOŚĆ) { if (produkt_wyjściowy_zmienić_rozmiar == pozycja_wyjścia.length) awaria_WARTOŚĆ("class file too large"); else pozycja_wyjścia[produkt_wyjściowy_zmienić_rozmiar++] = WARTOŚĆ & 255; }
    static void 출짧(int WARTOŚĆ) { 출바(WARTOŚĆ >> 8); 출바(WARTOŚĆ); }
    static void 출정(int WARTOŚĆ) { 출짧(WARTOŚĆ >>> 16); 출짧(WARTOŚĆ); }
    static void zapis_Klasa() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(stała_ILE_LICZB);
        for (int identyfikator = 0; identyfikator < stała_zmienić_rozmiar; identyfikator++) 출바(stała_WARTOŚĆ[identyfikator]);
        출짧(0x21); 출짧(Klasa_stała); 출짧(nadrzędny_stała); 출짧(0); 출짧(0); 출짧(metoda_ILE_LICZB);
        for (int identyfikator = 0; identyfikator < metoda_ILE_LICZB; identyfikator++) {
            출짧(metoda_dostęp[identyfikator]); 출짧(metoda_nazwa_stała[identyfikator]); 출짧(metoda_deskryptor_stała[identyfikator]); 출짧(1); 출짧(KOD_stała);
            출정(12 + metoda_długość[identyfikator]); 출짧(128); 출짧(함수지역[identyfikator]); 출정(metoda_długość[identyfikator]);
            for (int gniazdo_wpis = 0; gniazdo_wpis < metoda_długość[identyfikator]; gniazdo_wpis++) 출바(KOD_WARTOŚĆ[metoda_KOD[identyfikator] + gniazdo_wpis]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int Uruchom_2() {
        if (przestrzeń_użytkownika.인수개수() == 1 && 자바도구.같음(przestrzeń_użytkownika.argumenty(0), "-version")) {
            przestrzeń_użytkownika.Zapis("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (przestrzeń_użytkownika.인수개수() != 1) { przestrzeń_użytkownika.Zapis("Usage: javac FILE.java\n"); return 2; }
        int nazwa_zmienić_rozmiar = 자바도구.Nazwa(nazwa_pliku_SMS, przestrzeń_użytkownika.argumenty(0));
        if (nazwa_zmienić_rozmiar < 6 || nazwa_zmienić_rozmiar > 62 || nazwa_pliku_SMS[nazwa_zmienić_rozmiar - 5] != '.' || nazwa_pliku_SMS[nazwa_zmienić_rozmiar - 4] != 'j'
            || nazwa_pliku_SMS[nazwa_zmienić_rozmiar - 3] != 'a' || nazwa_pliku_SMS[nazwa_zmienić_rozmiar - 2] != 'v' || nazwa_pliku_SMS[nazwa_zmienić_rozmiar - 1] != 'a') {
            przestrzeń_użytkownika.Zapis("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        źródło_zmienić_rozmiar = przestrzeń_użytkownika.파일읽기(nazwa_pliku_SMS, plik_źródłowy);
        if (źródło_zmienić_rozmiar < 0) { przestrzeń_użytkownika.Zapis("javac: cannot read source: "); 자바도구.zapis_identyfikator(źródło_zmienić_rozmiar); przestrzeń_użytkownika.zapis_znak_WARTOŚĆ(10); return 1; }
        źródło_zmienić_rozmiar = 자바도구.원문해독(plik_źródłowy, źródło_zmienić_rozmiar);
        if (źródło_zmienić_rozmiar < 0) { przestrzeń_użytkownika.Zapis("javac error: invalid UTF-8 source\n"); return 1; }
        wyciąć_WARTOŚĆ(); if (!błąd) 선언읽기();
        if (!błąd) {
            if (token_długość[Klasa_token] != nazwa_zmienić_rozmiar - 5) awaria_WARTOŚĆ("class name must match file name");
            for (int identyfikator = 0; identyfikator < nazwa_zmienić_rozmiar - 5; identyfikator++) if (plik_źródłowy[token_stanowisko[Klasa_token] + identyfikator] != nazwa_pliku_SMS[identyfikator]) awaria_WARTOŚĆ("class name must match file name");
        }
        for (bieżący_metoda = 0; bieżący_metoda < metoda_ILE_LICZB && !błąd; bieżący_metoda++) {
            pozycja = treść_metody[bieżący_metoda]; metoda_KOD[bieżący_metoda] = KOD_zmienić_rozmiar; lokalny_ILE_LICZB = 0; 깊이 = 0;
            for (int identyfikator = 0; identyfikator < metoda_argument_ILE_LICZB[bieżący_metoda]; identyfikator++) Dodaj_lokalny(metoda_argument_nazwa[bieżący_metoda * 16 + identyfikator], metoda_argument_TYP[bieżący_metoda * 16 + identyfikator]);
            boolean Zwrot_KR = wyciąg_WARTOŚĆ();
            if (!Zwrot_KR && metoda_Zwrot[bieżący_metoda] != 0) awaria_WARTOŚĆ("missing return");
            // gałąź_22e01337 뒤의 합류 지점은 반드시 rzeczywisty_dane 명령이어야 한다 (버전 49 검증기).
            if (metoda_Zwrot[bieżący_metoda] == 0) 내보내기(177);
            else { boolean liczba_całkowita = metoda_Zwrot[bieżący_metoda] <= 2 || metoda_Zwrot[bieżący_metoda] == 5; 내보내기(liczba_całkowita ? 3 : 1); 내보내기(liczba_całkowita ? 172 : 176); }
            if (pozycja != metoda_Koniec[bieżący_metoda]) awaria_WARTOŚĆ("invalid method body");
            함수지역[bieżący_metoda] = lokalny_ILE_LICZB; metoda_długość[bieżący_metoda] = KOD_zmienić_rozmiar - metoda_KOD[bieżący_metoda];
        }
        if (błąd) return 1;
        zapis_Klasa(); if (błąd) return 1;
        nazwa_pliku_SMS[nazwa_zmienić_rozmiar - 4] = 'c'; nazwa_pliku_SMS[nazwa_zmienić_rozmiar - 3] = 'l'; nazwa_pliku_SMS[nazwa_zmienić_rozmiar - 2] = 'a';
        nazwa_pliku_SMS[nazwa_zmienić_rozmiar - 1] = 's'; nazwa_pliku_SMS[nazwa_zmienić_rozmiar] = 's'; nazwa_pliku_SMS[nazwa_zmienić_rozmiar + 1] = 0;
        int WYNIK = przestrzeń_użytkownika.zapis_Plik(nazwa_pliku_SMS, pozycja_wyjścia, produkt_wyjściowy_zmienić_rozmiar);
        if (WYNIK < 0) { przestrzeń_użytkownika.Zapis("javac: cannot save class: "); 자바도구.zapis_identyfikator(WYNIK); przestrzeń_użytkownika.zapis_znak_WARTOŚĆ(10); return 1; }
        przestrzeń_użytkownika.Zapis("Compiled: "); for (int identyfikator = 0; nazwa_pliku_SMS[identyfikator] != 0; identyfikator++) przestrzeń_użytkownika.zapis_znak_WARTOŚĆ(nazwa_pliku_SMS[identyfikator]);
        przestrzeń_użytkownika.Zapis(" (JVM class version 49)\n"); return 0;
    }
}
