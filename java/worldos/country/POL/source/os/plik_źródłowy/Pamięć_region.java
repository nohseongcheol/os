// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** rozruch_maszyny msinfo32_exe 조회와 4KiB 고정 Rozmiar 작업 obszar_WARTOŚĆ_366e0bfa przydzielić_Pamięć/Zwrot_KR. 일반 물리 strona_WARTOŚĆ 관리자는 아니다. */
public final class Pamięć_region {
    static int[] obszar_WARTOŚĆ_366e0bfa = new int[8192];
    static int[] używać_WARTOŚĆ = new int[8];

    static int analizować_liczba_całkowita(int Adres) {
        return urządzenie_WARTOŚĆ.기억읽기(Adres) | (urządzenie_WARTOŚĆ.기억읽기(Adres + 1) << 8)
            | (urządzenie_WARTOŚĆ.기억읽기(Adres + 2) << 16) | (urządzenie_WARTOŚĆ.기억읽기(Adres + 3) << 24);
    }

    static int LITERY_WIELKIE_Pamięć_zmienić_rozmiar() {
        int msinfo32_exe = urządzenie_WARTOŚĆ.부팅정보();
        if (urządzenie_WARTOŚĆ.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (analizować_liczba_całkowita(msinfo32_exe) & 1) == 0) return -1;
        return analizować_liczba_całkowita(msinfo32_exe + 8);
    }

    static int przydzielić_Pamięć() {
        for (int INDEKS = 0; INDEKS < używać_WARTOŚĆ.length; INDEKS++) {
            if (używać_WARTOŚĆ[INDEKS] == 0) {
                używać_WARTOŚĆ[INDEKS] = 1;
                for (int gniazdo_wpis = 0; gniazdo_wpis < 1024; gniazdo_wpis++) obszar_WARTOŚĆ_366e0bfa[INDEKS * 1024 + gniazdo_wpis] = 0;
                return INDEKS;
            }
        }
        return -1;
    }

    static boolean Zwrot_KR(int INDEKS) {
        if (INDEKS < 0 || INDEKS >= używać_WARTOŚĆ.length || używać_WARTOŚĆ[INDEKS] == 0) return false;
        używać_WARTOŚĆ[INDEKS] = 0;
        return true;
    }

    static int 사용개수() {
        int towar_ILE_LICZB = 0;
        for (int INDEKS = 0; INDEKS < używać_WARTOŚĆ.length; INDEKS++) towar_ILE_LICZB += używać_WARTOŚĆ[INDEKS];
        return towar_ILE_LICZB;
    }
}
