// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 화면 wyciąć_WARTOŚĆ·띠 합성·wskaźnik 밑그림을 관리한다. rzeczywisty_dane 화면 Pamięć_dane 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, wysokość_WARTOŚĆ, 합성중, LEWY_granica_WARTOŚĆ, LITERY_WIELKIE_granica, PRAWY_granica_WARTOŚĆ, LITERY_MAŁE_granica_WARTOŚĆ;
    static int wskaźnik_X, wskaźnik_Y, wskaźnik_kształt;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] wskaźnik_Tło = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void Przygotuj(int 폭, int długość_WARTOŚĆ) {
        너비 = 폭; wysokość_WARTOŚĆ = długość_WARTOŚĆ; 합성중 = 0; wskaźnik_kształt = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int pobrać_wysokość() { return wysokość_WARTOŚĆ; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int obcinać_WARTOŚĆ(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int START_WARTOŚĆ, int długość_WARTOŚĆ) {
        if (START_WARTOŚĆ > 2147483647 - długość_WARTOŚĆ) return 2147483647;
        return START_WARTOŚĆ + długość_WARTOŚĆ;
    }
    public static int obcinać(int 가로, int gałąź_stanowisko, int 폭, int długość_WARTOŚĆ) {
        if (너비 == 0 || 폭 <= 0 || długość_WARTOŚĆ <= 0) return 0;
        int PRAWY = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(gałąź_stanowisko, długość_WARTOŚĆ);
        int 왼쪽 = 합성중 != 0 ? LEWY_granica_WARTOŚĆ : 0, 위쪽 = 합성중 != 0 ? LITERY_WIELKIE_granica : 0;
        int 최대가로 = 합성중 != 0 ? PRAWY_granica_WARTOŚĆ : 너비, 최대세로 = 합성중 != 0 ? LITERY_MAŁE_granica_WARTOŚĆ : wysokość_WARTOŚĆ;
        if (가로 < 왼쪽) 가로 = 왼쪽;
        if (gałąź_stanowisko < 위쪽) gałąź_stanowisko = 위쪽;
        if (PRAWY > 최대가로) PRAWY = 최대가로;
        if (아래쪽 > 최대세로) 아래쪽 = 최대세로;
        if (PRAWY <= 가로 || 아래쪽 <= gałąź_stanowisko) return 0;
        잘린범위[0] = 가로; 잘린범위[1] = gałąź_stanowisko;
        잘린범위[2] = PRAWY - 가로; 잘린범위[3] = 아래쪽 - gałąź_stanowisko;
        return 1;
    }
    public static int Uruchom_2(int 가로, int gałąź_stanowisko, int 폭, int długość_WARTOŚĆ) {
        if (합성중 != 0 || długość_WARTOŚĆ > 32 || obcinać(가로, gałąź_stanowisko, 폭, długość_WARTOŚĆ) == 0) return 0;
        LEWY_granica_WARTOŚĆ = 잘린범위[0]; LITERY_WIELKIE_granica = 잘린범위[1];
        PRAWY_granica_WARTOŚĆ = LEWY_granica_WARTOŚĆ + 잘린범위[2]; LITERY_MAŁE_granica_WARTOŚĆ = LITERY_WIELKIE_granica + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean wskaźnik_bit(int 가로, int gałąź_stanowisko, int kształt_WARTOŚĆ) {
        if (kształt_WARTOŚĆ == 1) return 가로 >= 0 && 가로 <= gałąź_stanowisko / 2 && gałąź_stanowisko < 16;
        if (kształt_WARTOŚĆ == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - gałąź_stanowisko; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && gałąź_stanowisko >= 2 && gałąź_stanowisko <= 8 && (가로 <= 3 || gałąź_stanowisko <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && gałąź_stanowisko >= 12 && gałąź_stanowisko <= 18 && (가로 >= 17 || gałąź_stanowisko >= 17));
    }
    static int wskaźnik_piksel(int 가로, int gałąź_stanowisko) {
        if (wskaźnik_bit(가로, gałąź_stanowisko, wskaźnik_kształt)) return 2;
        for (int wiersz_wejścia = -1; wiersz_wejścia <= 1; wiersz_wejścia++) for (int gniazdo_wpis = -1; gniazdo_wpis <= 1; gniazdo_wpis++)
            if (wskaźnik_bit(가로 + gniazdo_wpis, gałąź_stanowisko + wiersz_wejścia, wskaźnik_kształt)) return 1;
        return 0;
    }
    static void wyświetlać_piksel(int 가로, int gałąź_stanowisko, int 색) {
        int gniazdo_wpis = 가로 - wskaźnik_X, wiersz_wejścia = gałąź_stanowisko - wskaźnik_Y;
        if (wskaźnik_kształt != 0 && gniazdo_wpis >= 0 && wiersz_wejścia >= 0 && gniazdo_wpis < 21 && wiersz_wejścia < 21) {
            wskaźnik_Tło[wiersz_wejścia * 21 + gniazdo_wpis] = 색;
            int punkt_WARTOŚĆ = wskaźnik_piksel(gniazdo_wpis, wiersz_wejścia); if (punkt_WARTOŚĆ != 0) 색 = punkt_WARTOŚĆ == 2 ? 0xffffff : 0x101010;
        }
        if (Tablica.표시화소읽기(가로, gałąź_stanowisko) != 색) {
            Tablica.zapis_wyświetlać_piksel(가로, gałąź_stanowisko, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void Zakończ() {
        if (합성중 == 0) return;
        for (int wiersz_wejścia = LITERY_WIELKIE_granica; wiersz_wejścia < LITERY_MAŁE_granica_WARTOŚĆ; wiersz_wejścia++) for (int gniazdo_wpis = LEWY_granica_WARTOŚĆ; gniazdo_wpis < PRAWY_granica_WARTOŚĆ; gniazdo_wpis++)
            wyświetlać_piksel(gniazdo_wpis, wiersz_wejścia, 완성그림[(wiersz_wejścia - LITERY_WIELKIE_granica) * 1920 + gniazdo_wpis]);
        합성중 = 0;
    }
    public static int piksel(int 가로, int gałąź_stanowisko, int 색) {
        if (가로 < 0 || gałąź_stanowisko < 0 || 가로 >= 너비 || gałąź_stanowisko >= wysokość_WARTOŚĆ) return 0;
        if (합성중 != 0) {
            if (가로 >= LEWY_granica_WARTOŚĆ && 가로 < PRAWY_granica_WARTOŚĆ && gałąź_stanowisko >= LITERY_WIELKIE_granica && gałąź_stanowisko < LITERY_MAŁE_granica_WARTOŚĆ)
                완성그림[(gałąź_stanowisko - LITERY_WIELKIE_granica) * 1920 + 가로] = 색;
        } else wyświetlać_piksel(가로, gałąź_stanowisko, 색);
        return 0;
    }
    public static void prostokąt_Wypełnij(int 가로, int gałąź_stanowisko, int 폭, int długość_WARTOŚĆ, int 색) {
        if (obcinać(가로, gałąź_stanowisko, 폭, długość_WARTOŚĆ) == 0) return;
        가로 = 잘린범위[0]; gałąź_stanowisko = 잘린범위[1]; 폭 = 잘린범위[2]; długość_WARTOŚĆ = 잘린범위[3];
        for (int wiersz_wejścia = gałąź_stanowisko; wiersz_wejścia < gałąź_stanowisko + długość_WARTOŚĆ; wiersz_wejścia++) for (int gniazdo_wpis = 가로; gniazdo_wpis < 가로 + 폭; gniazdo_wpis++) {
            if (합성중 != 0) 완성그림[(wiersz_wejścia - LITERY_WIELKIE_granica) * 1920 + gniazdo_wpis] = 색;
            else wyświetlać_piksel(gniazdo_wpis, wiersz_wejścia, 색);
        }
    }
    public static void wskaźnik(int 가로, int gałąź_stanowisko, int kształt_WARTOŚĆ) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (kształt_WARTOŚĆ >= 2 ? 10 : 0), 새세로 = gałąź_stanowisko - (kształt_WARTOŚĆ >= 2 ? 10 : 0);
        if (wskaźnik_kształt == kształt_WARTOŚĆ && wskaźnik_X == 새가로 && wskaźnik_Y == 새세로) return;
        if (wskaźnik_kształt != 0) for (int wiersz_wejścia = 0; wiersz_wejścia < 21; wiersz_wejścia++) for (int gniazdo_wpis = 0; gniazdo_wpis < 21; gniazdo_wpis++) {
            int 가 = wskaźnik_X + gniazdo_wpis, 세 = wskaźnik_Y + wiersz_wejścia;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < wysokość_WARTOŚĆ) Tablica.zapis_wyświetlać_piksel(가, 세, wskaźnik_Tło[wiersz_wejścia * 21 + gniazdo_wpis]);
        }
        wskaźnik_kształt = kształt_WARTOŚĆ; wskaźnik_X = 새가로; wskaźnik_Y = 새세로;
        if (kształt_WARTOŚĆ != 0) for (int wiersz_wejścia = 0; wiersz_wejścia < 21; wiersz_wejścia++) for (int gniazdo_wpis = 0; gniazdo_wpis < 21; gniazdo_wpis++) {
            int 가 = wskaźnik_X + gniazdo_wpis, 세 = wskaźnik_Y + wiersz_wejścia;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < wysokość_WARTOŚĆ) {
                wskaźnik_Tło[wiersz_wejścia * 21 + gniazdo_wpis] = Tablica.표시화소읽기(가, 세);
                int punkt_WARTOŚĆ = wskaźnik_piksel(gniazdo_wpis, wiersz_wejścia); if (punkt_WARTOŚĆ != 0) Tablica.zapis_wyświetlać_piksel(가, 세, punkt_WARTOŚĆ == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
