// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 Store_WARTOŚĆ format_WARTOŚĆ. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] Plik_tabela = new int[1024];
    static int 바이트해시(int WARTOŚĆ, int dane) { return (WARTOŚĆ ^ dane) * 16777619; }
    static void czyścić_dane() {
        for (int INDEKS = 0; INDEKS < 512; INDEKS++) urządzenie_magazynujące_połączenie.obszar_dane[INDEKS] = 0;
    }
    static int tabela_liczba_całkowita(int pozycja) {
        return Plik_tabela[pozycja] | Plik_tabela[pozycja + 1] << 8 | Plik_tabela[pozycja + 2] << 16 | Plik_tabela[pozycja + 3] << 24;
    }
    static void zapis_tabela_liczba_całkowita(int pozycja, int WARTOŚĆ) {
        for (int INDEKS = 0; INDEKS < 4; INDEKS++) Plik_tabela[pozycja + INDEKS] = (WARTOŚĆ >>> (INDEKS * 8)) & 255;
    }
    static boolean czek_tabela() {
        for (int nazwa_pliku = 0; nazwa_pliku < 8; nazwa_pliku++) {
            int długość_WARTOŚĆ = 0;
            for (int gniazdo_wpis = 0; gniazdo_wpis < 64; gniazdo_wpis++) Pamięć_system_plików.Nazwa[gniazdo_wpis] = Plik_tabela[nazwa_pliku * 72 + gniazdo_wpis];
            while (długość_WARTOŚĆ < 64 && Pamięć_system_plików.Nazwa[długość_WARTOŚĆ] != 0) długość_WARTOŚĆ++;
            if (długość_WARTOŚĆ == 0) continue;
            if (!Pamięć_system_plików.czek_nazwa(Pamięć_system_plików.Nazwa, długość_WARTOŚĆ)
                || tabela_liczba_całkowita(nazwa_pliku * 72 + 64) < 0 || tabela_liczba_całkowita(nazwa_pliku * 72 + 64) > 16384) return false;
            for (int przód_WARTOŚĆ = 0; przód_WARTOŚĆ < nazwa_pliku; przód_WARTOŚĆ++) {
                boolean 같음 = Plik_tabela[przód_WARTOŚĆ * 72 + długość_WARTOŚĆ] == 0;
                for (int gniazdo_wpis = 0; gniazdo_wpis < długość_WARTOŚĆ; gniazdo_wpis++) if (Plik_tabela[przód_WARTOŚĆ * 72 + gniazdo_wpis] != Pamięć_system_plików.Nazwa[gniazdo_wpis]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int START_obszar = 1 + 보존본 * 259;
        if (urządzenie_magazynujące_połączenie.Odczyt(START_obszar) < 0 || urządzenie_magazynujące_połączenie.analizować_liczba_całkowita(0) != 0x4a4b534e) return -1;
        int 세대 = urządzenie_magazynujące_połączenie.analizować_liczba_całkowita(4), suma_kontrolna = urządzenie_magazynujące_połączenie.analizować_liczba_całkowita(8);
        if (세대 < 1 || urządzenie_magazynujące_połączenie.analizować_liczba_całkowita(12) != (세대 ^ suma_kontrolna ^ 0x4a4b534e)) return -1;
        int skrót_Plik = 0x811c9dc5;
        for (int obszar_WARTOŚĆ_366e0bfa = 0; obszar_WARTOŚĆ_366e0bfa < 258; obszar_WARTOŚĆ_366e0bfa++) {
            if (urządzenie_magazynujące_połączenie.Odczyt(START_obszar + 1 + obszar_WARTOŚĆ_366e0bfa) < 0) return -1;
            for (int gniazdo_wpis = 0; gniazdo_wpis < 512; gniazdo_wpis++) {
                int WARTOŚĆ = urządzenie_magazynujące_połączenie.obszar_dane[gniazdo_wpis];
                skrót_Plik = 바이트해시(skrót_Plik, WARTOŚĆ);
                if (obszar_WARTOŚĆ_366e0bfa < 2) Plik_tabela[obszar_WARTOŚĆ_366e0bfa * 512 + gniazdo_wpis] = WARTOŚĆ;
            }
        }
        return skrót_Plik == suma_kontrolna && czek_tabela() ? 세대 : -1;
    }
    static int Obciążenie(int 보존본) {
        int START_obszar = 1 + 보존본 * 259;
        for (int obszar_WARTOŚĆ_366e0bfa = 0; obszar_WARTOŚĆ_366e0bfa < 2; obszar_WARTOŚĆ_366e0bfa++) {
            if (urządzenie_magazynujące_połączenie.Odczyt(START_obszar + 1 + obszar_WARTOŚĆ_366e0bfa) < 0) return -5;
            for (int gniazdo_wpis = 0; gniazdo_wpis < 512; gniazdo_wpis++) Plik_tabela[obszar_WARTOŚĆ_366e0bfa * 512 + gniazdo_wpis] = urządzenie_magazynujące_połączenie.obszar_dane[gniazdo_wpis];
        }
        for (int nazwa_pliku = 0; nazwa_pliku < 8; nazwa_pliku++) {
            for (int gniazdo_wpis = 0; gniazdo_wpis < 64; gniazdo_wpis++) Pamięć_system_plików.이름들[nazwa_pliku * 64 + gniazdo_wpis] = Plik_tabela[nazwa_pliku * 72 + gniazdo_wpis];
            Pamięć_system_plików.zmienić_rozmiar_Lista[nazwa_pliku] = Plik_tabela[nazwa_pliku * 72] == 0 ? 0 : tabela_liczba_całkowita(nazwa_pliku * 72 + 64);
            Pamięć_system_plików.허가들[nazwa_pliku] = tabela_liczba_całkowita(nazwa_pliku * 72 + 68) & 511;
            for (int obszar_WARTOŚĆ_366e0bfa = 0; obszar_WARTOŚĆ_366e0bfa < 32; obszar_WARTOŚĆ_366e0bfa++) {
                if (urządzenie_magazynujące_połączenie.Odczyt(START_obszar + 3 + nazwa_pliku * 32 + obszar_WARTOŚĆ_366e0bfa) < 0) return -5;
                int Adres = urządzenie_WARTOŚĆ.Plik_Pamięć() + nazwa_pliku * 16384 + obszar_WARTOŚĆ_366e0bfa * 512;
                for (int gniazdo_wpis = 0; gniazdo_wpis < 512; gniazdo_wpis++) urządzenie_WARTOŚĆ.zapis_Pamięć(Adres + gniazdo_wpis, urządzenie_magazynujące_połączenie.obszar_dane[gniazdo_wpis]);
            }
        }
        return 0;
    }
    static void Przygotuj() {
        if (urządzenie_magazynujące_połączenie.Odczyt(0) < 0 || urządzenie_magazynujące_połączenie.analizować_liczba_całkowita(0) != 0x54534b4a
            || urządzenie_magazynujące_połączenie.analizować_liczba_całkowita(4) != 0x3145524f || urządzenie_magazynujące_połączenie.analizować_liczba_całkowita(8) != 2048
            || urządzenie_magazynujące_połączenie.analizować_liczba_całkowita(12) != 0x3153464a) {
            SMS_Terminal.Zapis("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        urządzenie_magazynujące_połączenie.systemy_informacyjne_Aktywny_9e72441a = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { SMS_Terminal.Zapis("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (Obciążenie(현재보존본) < 0) {
            SMS_Terminal.Zapis("STORE read failed; halted to preserve files\n"); urządzenie_WARTOŚĆ.정지();
        }
        SMS_Terminal.Zapis("STORE restored generation "); SMS_Terminal.zapis_identyfikator(세대번호); SMS_Terminal.문자(10);
    }
    static int synchronizować() {
        if (!urządzenie_magazynujące_połączenie.systemy_informacyjne_Aktywny_9e72441a) return -19;
        if (세대번호 == 2147483647) return -75;
        int Dalej_towar = 현재보존본 == 0 ? 1 : 0, START_obszar = 1 + Dalej_towar * 259;
        // 새 본문보다 먼저 Wstecz_towar commit을 무효화하고 urządzenie_WARTOŚĆ 캐시를 비운다.
        czyścić_dane();
        if (urządzenie_magazynujące_połączenie.Zapis(START_obszar) < 0 || urządzenie_magazynujące_połączenie.opróżnić_produkt_wyjściowy() < 0) return -5;
        for (int gniazdo_wpis = 0; gniazdo_wpis < 1024; gniazdo_wpis++) Plik_tabela[gniazdo_wpis] = 0;
        for (int nazwa_pliku = 0; nazwa_pliku < 8; nazwa_pliku++) if (Pamięć_system_plików.이름들[nazwa_pliku * 64] != 0) {
            for (int gniazdo_wpis = 0; gniazdo_wpis < 64; gniazdo_wpis++) Plik_tabela[nazwa_pliku * 72 + gniazdo_wpis] = Pamięć_system_plików.이름들[nazwa_pliku * 64 + gniazdo_wpis];
            zapis_tabela_liczba_całkowita(nazwa_pliku * 72 + 64, Pamięć_system_plików.zmienić_rozmiar_Lista[nazwa_pliku]);
            zapis_tabela_liczba_całkowita(nazwa_pliku * 72 + 68, Pamięć_system_plików.허가들[nazwa_pliku]);
        }
        int skrót_Plik = 0x811c9dc5;
        for (int obszar_WARTOŚĆ_366e0bfa = 0; obszar_WARTOŚĆ_366e0bfa < 258; obszar_WARTOŚĆ_366e0bfa++) {
            for (int gniazdo_wpis = 0; gniazdo_wpis < 512; gniazdo_wpis++) {
                int WARTOŚĆ = 0;
                if (obszar_WARTOŚĆ_366e0bfa < 2) WARTOŚĆ = Plik_tabela[obszar_WARTOŚĆ_366e0bfa * 512 + gniazdo_wpis];
                else {
                    int nazwa_pliku = (obszar_WARTOŚĆ_366e0bfa - 2) / 32, pozycja = (obszar_WARTOŚĆ_366e0bfa - 2) % 32 * 512 + gniazdo_wpis;
                    if (Plik_tabela[nazwa_pliku * 72] != 0 && pozycja < Pamięć_system_plików.zmienić_rozmiar_Lista[nazwa_pliku])
                        WARTOŚĆ = urządzenie_WARTOŚĆ.기억읽기(urządzenie_WARTOŚĆ.Plik_Pamięć() + nazwa_pliku * 16384 + pozycja);
                }
                urządzenie_magazynujące_połączenie.obszar_dane[gniazdo_wpis] = WARTOŚĆ; skrót_Plik = 바이트해시(skrót_Plik, WARTOŚĆ);
            }
            if (urządzenie_magazynujące_połączenie.Zapis(START_obszar + 1 + obszar_WARTOŚĆ_366e0bfa) < 0) return -5;
        }
        if (urządzenie_magazynujące_połączenie.opróżnić_produkt_wyjściowy() < 0) return -5;
        czyścić_dane(); urządzenie_magazynujące_połączenie.zapis_liczba_całkowita_WARTOŚĆ(0, 0x4a4b534e);
        urządzenie_magazynujące_połączenie.zapis_liczba_całkowita_WARTOŚĆ(4, 세대번호 + 1); urządzenie_magazynujące_połączenie.zapis_liczba_całkowita_WARTOŚĆ(8, skrót_Plik);
        urządzenie_magazynujące_połączenie.zapis_liczba_całkowita_WARTOŚĆ(12, (세대번호 + 1) ^ skrót_Plik ^ 0x4a4b534e);
        if (urządzenie_magazynujące_połączenie.Zapis(START_obszar) < 0 || urządzenie_magazynujące_połączenie.opróżnić_produkt_wyjściowy() < 0) return -5;
        현재보존본 = Dalej_towar; 세대번호++;
        return 0;
    }
}
