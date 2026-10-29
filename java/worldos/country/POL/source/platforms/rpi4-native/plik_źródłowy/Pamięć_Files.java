// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM nazwa_pliku 64개, 파일당 16384바이트, deskryptor_wpis 16개. 모든 dane/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. negatywny_WARTOŚĆ 반환은 błąd 번호다.
 */
public final class Pamięć_Files {
    static final int Plik_ILE_LICZB = 64;
    static int[] Nazwa = new int[Plik_ILE_LICZB * 64];
    static int[] 이름길이 = new int[Plik_ILE_LICZB];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] treść_WARTOŚĆ_cb0f2404 = new int[Plik_ILE_LICZB * 4096];
    static int[] długość_WARTOŚĆ = new int[Plik_ILE_LICZB];
    static int[] odwołanie_ILE_LICZB = new int[Plik_ILE_LICZB];
    static int[] używać_WARTOŚĆ = new int[16];
    static int[] wartość_docelowa = new int[16];
    static int[] pozycja = new int[16];
    static int[] metoda_tryb = new int[16];
    static int[] ścieżka_2 = new int[64];
    static int ścieżka_długość;

    public static int 파일한도() { return Plik_ILE_LICZB; }
    static int 자료읽기(int nazwa_pliku, int indeks_pozycji) { return (treść_WARTOŚĆ_cb0f2404[nazwa_pliku * 4096 + indeks_pozycji / 4] >>> ((indeks_pozycji & 3) * 8)) & 255; }
    static void zapis_dane(int nazwa_pliku, int indeks_pozycji, int WARTOŚĆ) {
        int gniazdo_wpis = nazwa_pliku * 4096 + indeks_pozycji / 4, przenosić_WARTOŚĆ = (indeks_pozycji & 3) * 8;
        treść_WARTOŚĆ_cb0f2404[gniazdo_wpis] = (treść_WARTOŚĆ_cb0f2404[gniazdo_wpis] & ~(255 << przenosić_WARTOŚĆ)) | ((WARTOŚĆ & 255) << przenosić_WARTOŚĆ);
    }

    public static int ścieżka_START(int Rozmiar) {
        ścieżka_długość = 0;
        if (Rozmiar < 1 || Rozmiar > 63) return -36;
        ścieżka_długość = Rozmiar;
        for (int Loop_INDEKS = 0; Loop_INDEKS < Rozmiar; Loop_INDEKS++) ścieżka_2[Loop_INDEKS] = 0;
        return 0;
    }
    public static int ścieżka_bajt(int INDEKS, int WARTOŚĆ) {
        if (INDEKS < 0 || INDEKS >= ścieżka_długość || WARTOŚĆ < 1 || WARTOŚĆ > 255) return -22;
        ścieżka_2[INDEKS] = WARTOŚĆ; return 0;
    }
    static int ZNAJDŹ_wpis() {
        for (int Plik_INDEKS = 0; Plik_INDEKS < Plik_ILE_LICZB; Plik_INDEKS++) if (이름길이[Plik_INDEKS] > 0 && 이름길이[Plik_INDEKS] == Canonical_długość && 접두(Nazwa, Plik_INDEKS * 64, 이름길이[Plik_INDEKS], Canonical_WARTOŚĆ, Canonical_długość)) return Plik_INDEKS;
        return -1;
    }
    public static int Otwórz(int 플래그) {
        if (ścieżka_długość == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int Loop_INDEKS = 0; Loop_INDEKS < ścieżka_długość; Loop_INDEKS++) if (ścieżka_2[Loop_INDEKS] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int WYNIK = normalizować_WARTOŚĆ(); if (WYNIK < 0) return WYNIK;
        if (ZNAJDŹ_Katalog(Canonical_długość) >= 0) return -21;
        WYNIK = czek_nadrzędny(); if (WYNIK < 0) return WYNIK;
        int nazwa_pliku = ZNAJDŹ_wpis();
        if (nazwa_pliku >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (nazwa_pliku < 0 && (플래그 & 0x40) == 0) return -2;
        int deskryptor_wpis = -1;
        for (int Loop_INDEKS = 0; Loop_INDEKS < 16; Loop_INDEKS++) if (używać_WARTOŚĆ[Loop_INDEKS] == 0) { deskryptor_wpis = Loop_INDEKS; break; }
        if (deskryptor_wpis < 0) return -24;
        if (nazwa_pliku < 0) {
            for (int Loop_INDEKS = 0; Loop_INDEKS < Plik_ILE_LICZB; Loop_INDEKS++) if (이름길이[Loop_INDEKS] == 0 && odwołanie_ILE_LICZB[Loop_INDEKS] == 0) { nazwa_pliku = Loop_INDEKS; break; }
            if (nazwa_pliku < 0) return -28;
            이름길이[nazwa_pliku] = Canonical_długość;
            for (int Loop_INDEKS = 0; Loop_INDEKS < Canonical_długość; Loop_INDEKS++) Nazwa[nazwa_pliku * 64 + Loop_INDEKS] = Canonical_WARTOŚĆ[Loop_INDEKS];
            długość_WARTOŚĆ[nazwa_pliku] = 0;
        }
        if ((플래그 & 0x200) != 0) długość_WARTOŚĆ[nazwa_pliku] = 0;
        używać_WARTOŚĆ[deskryptor_wpis] = 1; wartość_docelowa[deskryptor_wpis] = nazwa_pliku; pozycja[deskryptor_wpis] = 0; metoda_tryb[deskryptor_wpis] = 플래그;
        odwołanie_ILE_LICZB[nazwa_pliku]++;
        return deskryptor_wpis + 3;
    }
    static int 확인(int deskryptor_wpis) {
        return deskryptor_wpis >= 3 && deskryptor_wpis < 19 && używać_WARTOŚĆ[deskryptor_wpis - 3] != 0 ? deskryptor_wpis - 3 : -1;
    }
    public static int Odczyt(int deskryptor_wpis) {
        int gniazdo_wpis = 확인(deskryptor_wpis);
        if (gniazdo_wpis < 0 || (metoda_tryb[gniazdo_wpis] & 3) == 1) return -9;
        int nazwa_pliku = wartość_docelowa[gniazdo_wpis];
        if (pozycja[gniazdo_wpis] >= długość_WARTOŚĆ[nazwa_pliku]) return 256; // EOF와 rzeczywisty_dane 0x00..0xff 구별
        return 자료읽기(nazwa_pliku, pozycja[gniazdo_wpis]++);
    }
    public static int Zapis(int deskryptor_wpis, int WARTOŚĆ) {
        int gniazdo_wpis = 확인(deskryptor_wpis);
        if (gniazdo_wpis < 0 || (metoda_tryb[gniazdo_wpis] & 3) == 0) return -9;
        int nazwa_pliku = wartość_docelowa[gniazdo_wpis];
        if ((metoda_tryb[gniazdo_wpis] & 0x400) != 0) pozycja[gniazdo_wpis] = długość_WARTOŚĆ[nazwa_pliku];
        if (pozycja[gniazdo_wpis] >= 16384) return -28;
        while (długość_WARTOŚĆ[nazwa_pliku] < pozycja[gniazdo_wpis]) zapis_dane(nazwa_pliku, długość_WARTOŚĆ[nazwa_pliku]++, 0);
        zapis_dane(nazwa_pliku, pozycja[gniazdo_wpis]++, WARTOŚĆ);
        if (długość_WARTOŚĆ[nazwa_pliku] < pozycja[gniazdo_wpis]) długość_WARTOŚĆ[nazwa_pliku] = pozycja[gniazdo_wpis];
        return 1;
    }
    public static int szukać_stanowisko(int deskryptor_wpis, int 거리, int Project_korzeń) {
        int gniazdo_wpis = 확인(deskryptor_wpis);
        if (gniazdo_wpis < 0) return -9;
        if (Project_korzeń < 0 || Project_korzeń > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (Project_korzeń == 0 ? 0 : Project_korzeń == 1 ? pozycja[gniazdo_wpis] : długość_WARTOŚĆ[wartość_docelowa[gniazdo_wpis]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        pozycja[gniazdo_wpis] = 새위치; return 새위치;
    }
    public static int Zamknięte(int deskryptor_wpis) {
        int gniazdo_wpis = 확인(deskryptor_wpis);
        if (gniazdo_wpis < 0) return -9;
        odwołanie_ILE_LICZB[wartość_docelowa[gniazdo_wpis]]--; używać_WARTOŚĆ[gniazdo_wpis] = 0; return 0;
    }
    public static int Rozmiar(int deskryptor_wpis) {
        int gniazdo_wpis = 확인(deskryptor_wpis); return gniazdo_wpis < 0 ? -9 : długość_WARTOŚĆ[wartość_docelowa[gniazdo_wpis]];
    }
    public static int set_długość(int deskryptor_wpis, int Rozmiar) {
        int gniazdo_wpis = 확인(deskryptor_wpis);
        if (gniazdo_wpis < 0 || (metoda_tryb[gniazdo_wpis] & 3) == 0) return -9;
        if (Rozmiar < 0 || Rozmiar > 16384) return -22;
        int nazwa_pliku = wartość_docelowa[gniazdo_wpis];
        while (długość_WARTOŚĆ[nazwa_pliku] < Rozmiar) zapis_dane(nazwa_pliku, długość_WARTOŚĆ[nazwa_pliku]++, 0);
        długość_WARTOŚĆ[nazwa_pliku] = Rozmiar; return 0;
    }
    public static int usunąć_wpis() {
        if (ścieżka_długość == 0) return -22;
        int WYNIK = normalizować_WARTOŚĆ(); if (WYNIK < 0) return WYNIK;
        if (ZNAJDŹ_Katalog(Canonical_długość) >= 0) return -21;
        WYNIK = czek_nadrzędny(); if (WYNIK < 0) return WYNIK;
        int nazwa_pliku = ZNAJDŹ_wpis();
        if (nazwa_pliku < 0) return -2;
        이름길이[nazwa_pliku] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void wpis_Lista() {
        ścieżka_START(1); ścieżka_bajt(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int INDEKS) {
        if (INDEKS < 0 || INDEKS >= Plik_ILE_LICZB || 이름길이[INDEKS] == 0) return 0;
        for (int Loop_INDEKS = 0; Loop_INDEKS < 이름길이[INDEKS]; Loop_INDEKS++) if (Nazwa[INDEKS * 64 + Loop_INDEKS] == '/') return 0;
        return 이름길이[INDEKS];
    }
    public static int 공개이름바이트(int INDEKS, int indeks_pozycji) {
        return INDEKS >= 0 && INDEKS < Plik_ILE_LICZB && indeks_pozycji >= 0 && indeks_pozycji < 이름길이[INDEKS] ? Nazwa[INDEKS * 64 + indeks_pozycji] : -22;
    }
    public static int 공개파일크기(int INDEKS) { return INDEKS >= 0 && INDEKS < Plik_ILE_LICZB ? długość_WARTOŚĆ[INDEKS] : -22; }
    static int[] Canonical_WARTOŚĆ = new int[64], bieżący_towar = new int[64], Katalog_nazwa = new int[16 * 64], Katalog_długość = new int[16];
    static int Canonical_długość, bieżący_długość;
    static boolean 접두(int[] 이름들, int Uruchom_2, int ścieżka_WARTOŚĆ, int[] przód_WARTOŚĆ, int interlinia_ścieżka) {
        if (ścieżka_WARTOŚĆ < interlinia_ścieżka) return false;
        for (int Loop_INDEKS = 0; Loop_INDEKS < interlinia_ścieżka; Loop_INDEKS++) if (이름들[Uruchom_2 + Loop_INDEKS] != przód_WARTOŚĆ[Loop_INDEKS]) return false;
        return true;
    }
    static int normalizować_WARTOŚĆ() {
        if (ścieżka_długość == 0) return -22;
        Canonical_długość = ścieżka_2[0] == '/' ? 0 : bieżący_długość;
        for (int Loop_INDEKS = 0; Loop_INDEKS < Canonical_długość; Loop_INDEKS++) Canonical_WARTOŚĆ[Loop_INDEKS] = bieżący_towar[Loop_INDEKS];
        int 읽는자리 = 0;
        while (읽는자리 < ścieżka_długość) {
            while (읽는자리 < ścieżka_długość && ścieżka_2[읽는자리] == '/') 읽는자리++;
            int START_stanowisko = 읽는자리; while (읽는자리 < ścieżka_długość && ścieżka_2[읽는자리] != '/') { if (ścieżka_2[읽는자리] == 0) return -22; 읽는자리++; }
            int wpis_ILE_LICZB = 읽는자리 - START_stanowisko; if (wpis_ILE_LICZB == 0 || wpis_ILE_LICZB == 1 && ścieżka_2[START_stanowisko] == '.') continue;
            if (wpis_ILE_LICZB == 2 && ścieżka_2[START_stanowisko] == '.' && ścieżka_2[START_stanowisko + 1] == '.') {
                while (Canonical_długość > 0 && Canonical_WARTOŚĆ[Canonical_długość - 1] != '/') Canonical_długość--;
                if (Canonical_długość > 0) Canonical_długość--;
                continue;
            }
            if (Canonical_długość + wpis_ILE_LICZB + (Canonical_długość == 0 ? 0 : 1) > 63) return -36;
            if (Canonical_długość > 0) Canonical_WARTOŚĆ[Canonical_długość++] = '/';
            for (int Loop_INDEKS = START_stanowisko; Loop_INDEKS < 읽는자리; Loop_INDEKS++) Canonical_WARTOŚĆ[Canonical_długość++] = ścieżka_2[Loop_INDEKS];
        }
        return 0;
    }
    static int ZNAJDŹ_Katalog(int wpis_ILE_LICZB) {
        if (wpis_ILE_LICZB == 0) return 0;
        for (int Loop_INDEKS = 1; Loop_INDEKS < 16; Loop_INDEKS++) if (Katalog_długość[Loop_INDEKS] == wpis_ILE_LICZB && 접두(Katalog_nazwa, Loop_INDEKS * 64, wpis_ILE_LICZB, Canonical_WARTOŚĆ, wpis_ILE_LICZB)) return Loop_INDEKS;
        return -1;
    }
    static int czek_nadrzędny() {
        int wpis_ILE_LICZB = Canonical_długość; while (wpis_ILE_LICZB > 0 && Canonical_WARTOŚĆ[wpis_ILE_LICZB - 1] != '/') wpis_ILE_LICZB--;
        return ZNAJDŹ_Katalog(wpis_ILE_LICZB == 0 ? 0 : wpis_ILE_LICZB - 1) < 0 ? -2 : 0;
    }
    public static int Twórca_Katalog() {
        int 처리값 = normalizować_WARTOŚĆ(); if (처리값 < 0) return 처리값;
        if (ZNAJDŹ_Katalog(Canonical_długość) >= 0 || ZNAJDŹ_wpis() >= 0) return -17;
        처리값 = czek_nadrzędny(); if (처리값 < 0) return 처리값;
        for (int Loop_INDEKS = 1; Loop_INDEKS < 16; Loop_INDEKS++) if (Katalog_długość[Loop_INDEKS] == 0) {
            Katalog_długość[Loop_INDEKS] = Canonical_długość; for (int wewnętrzne_stanowisko = 0; wewnętrzne_stanowisko < Canonical_długość; wewnętrzne_stanowisko++) Katalog_nazwa[Loop_INDEKS * 64 + wewnętrzne_stanowisko] = Canonical_WARTOŚĆ[wewnętrzne_stanowisko]; return 0;
        }
        return -28;
    }
    public static int wpis_Rodzaj() {
        int 처리값 = normalizować_WARTOŚĆ(); if (처리값 < 0) return 처리값;
        if (ZNAJDŹ_Katalog(Canonical_długość) >= 0) return 2;
        return ZNAJDŹ_wpis() >= 0 ? 1 : 0;
    }
    public static int zmienić_Katalog() {
        int 처리값 = normalizować_WARTOŚĆ(); if (처리값 < 0) return 처리값;
        if (ZNAJDŹ_Katalog(Canonical_długość) < 0) return -2;
        bieżący_długość = Canonical_długość; for (int Loop_INDEKS = 0; Loop_INDEKS < bieżący_długość; Loop_INDEKS++) bieżący_towar[Loop_INDEKS] = Canonical_WARTOŚĆ[Loop_INDEKS]; return 0;
    }
    public static int usuń_Katalog() {
        int 처리값 = normalizować_WARTOŚĆ(); if (처리값 < 0) return 처리값;
        int Katalog_identyfikator = ZNAJDŹ_Katalog(Canonical_długość); if (Katalog_identyfikator < 0) return -2; if (Katalog_identyfikator == 0) return -16;
        if (bieżący_długość == Canonical_długość && 접두(bieżący_towar, 0, bieżący_długość, Canonical_WARTOŚĆ, Canonical_długość)) return -16;
        for (int Loop_INDEKS = 0; Loop_INDEKS < Plik_ILE_LICZB; Loop_INDEKS++) {
            if (이름길이[Loop_INDEKS] > Canonical_długość && 접두(Nazwa, Loop_INDEKS * 64, 이름길이[Loop_INDEKS], Canonical_WARTOŚĆ, Canonical_długość) && Nazwa[Loop_INDEKS * 64 + Canonical_długość] == '/') return -39;
        }
        for (int Loop_INDEKS = 0; Loop_INDEKS < 16; Loop_INDEKS++) {
            if (Katalog_długość[Loop_INDEKS] > Canonical_długość && 접두(Katalog_nazwa, Loop_INDEKS * 64, Katalog_długość[Loop_INDEKS], Canonical_WARTOŚĆ, Canonical_długość) && Katalog_nazwa[Loop_INDEKS * 64 + Canonical_długość] == '/') return -39;
        }
        Katalog_długość[Katalog_identyfikator] = 0; return 0;
    }
    public static int Zmień_nazwę_wpis(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= Plik_ILE_LICZB || 이름길이[원본번호] == 0) return -2;
        int 처리값 = normalizować_WARTOŚĆ(); if (처리값 < 0) return 처리값;
        if (ZNAJDŹ_Katalog(Canonical_długość) >= 0) return -21;
        처리값 = czek_nadrzędny(); if (처리값 < 0) return 처리값;
        int Wstecz_WARTOŚĆ = ZNAJDŹ_wpis(); if (Wstecz_WARTOŚĆ == 원본번호) return 0;
        if (Wstecz_WARTOŚĆ >= 0) 이름길이[Wstecz_WARTOŚĆ] = 0;
        이름길이[원본번호] = Canonical_długość; for (int Loop_INDEKS = 0; Loop_INDEKS < Canonical_długość; Loop_INDEKS++) Nazwa[원본번호 * 64 + Loop_INDEKS] = Canonical_WARTOŚĆ[Loop_INDEKS]; return 0;
    }
    static int wpis_START(int[] dane_TABLICA, int 시작점, int wpis_ILE_LICZB) {
        if (!접두(dane_TABLICA, 시작점, wpis_ILE_LICZB, Canonical_WARTOŚĆ, Canonical_długość)) return -1;
        int START_stanowisko = Canonical_długość;
        if (START_stanowisko > 0) { if (wpis_ILE_LICZB <= START_stanowisko || dane_TABLICA[시작점 + START_stanowisko] != '/') return -1; START_stanowisko++; }
        if (wpis_ILE_LICZB <= START_stanowisko) return -1;
        for (int Loop_INDEKS = START_stanowisko; Loop_INDEKS < wpis_ILE_LICZB; Loop_INDEKS++) if (dane_TABLICA[시작점 + Loop_INDEKS] == '/') return -1;
        return START_stanowisko;
    }
    static void bieżący_zapis() { 단말.문자('/'); for (int Loop_INDEKS = 0; Loop_INDEKS < bieżący_długość; Loop_INDEKS++) Tablica.직렬쓰기(bieżący_towar[Loop_INDEKS]); }
    static int 경로목록() {
        int 처리값 = normalizować_WARTOŚĆ(); if (처리값 < 0) return 처리값;
        int Plik_wartość_docelowa = ZNAJDŹ_wpis();
        if (Plik_wartość_docelowa >= 0) { for (int Loop_INDEKS = 0; Loop_INDEKS < Canonical_długość; Loop_INDEKS++) Tablica.직렬쓰기(Canonical_WARTOŚĆ[Loop_INDEKS]); 단말.Zapis("  "); 단말.identyfikator(długość_WARTOŚĆ[Plik_wartość_docelowa]); 단말.Zapis("bajt_WARTOŚĆ(주기억 nazwa_pliku)\n"); return 0; }
        if (ZNAJDŹ_Katalog(Canonical_długość) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (Katalog_długość[뒷값] > 0) {
            int START_stanowisko = wpis_START(Katalog_nazwa, 뒷값 * 64, Katalog_długość[뒷값]); if (START_stanowisko < 0) continue;
            for (int Loop_INDEKS = START_stanowisko; Loop_INDEKS < Katalog_długość[뒷값]; Loop_INDEKS++) Tablica.직렬쓰기(Katalog_nazwa[뒷값 * 64 + Loop_INDEKS]); 단말.Zapis("/\n");
        }
        for (int Plik_INDEKS = 0; Plik_INDEKS < Plik_ILE_LICZB; Plik_INDEKS++) if (이름길이[Plik_INDEKS] > 0) {
            int START_stanowisko = wpis_START(Nazwa, Plik_INDEKS * 64, 이름길이[Plik_INDEKS]); if (START_stanowisko < 0) continue;
            for (int Loop_INDEKS = START_stanowisko; Loop_INDEKS < 이름길이[Plik_INDEKS]; Loop_INDEKS++) Tablica.직렬쓰기(Nazwa[Plik_INDEKS * 64 + Loop_INDEKS]);
            단말.Zapis("  "); 단말.identyfikator(długość_WARTOŚĆ[Plik_INDEKS]); 단말.Zapis("bajt_WARTOŚĆ(주기억 nazwa_pliku)\n");
        }
        return 0;
    }
}
