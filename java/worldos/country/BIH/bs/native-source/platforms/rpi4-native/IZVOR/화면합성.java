// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 화면 izrezati_VALUE·띠 합성·pokazivač 밑그림을 관리한다. stvaran_podaci 화면 Memorija_podaci 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, 높이, 합성중, 왼경계, 위경계, 오른경계, 아래경계;
    static int pokazivač_X, pokazivač_Y, pokazivač_oblik;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] pokazivač_poster = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void Pripremiti(int 폭, int dužina_VALUE) {
        너비 = 폭; 높이 = dužina_VALUE; 합성중 = 0; pokazivač_oblik = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int 높이얻기() { return 높이; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int isječak_VALUE(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int START_VALUE, int dužina_VALUE) {
        if (START_VALUE > 2147483647 - dužina_VALUE) return 2147483647;
        return START_VALUE + dužina_VALUE;
    }
    public static int isječak(int 가로, int Vertikalno_položaj, int 폭, int dužina_VALUE) {
        if (너비 == 0 || 폭 <= 0 || dužina_VALUE <= 0) return 0;
        int RIGHT = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(Vertikalno_položaj, dužina_VALUE);
        int 왼쪽 = 합성중 != 0 ? 왼경계 : 0, 위쪽 = 합성중 != 0 ? 위경계 : 0;
        int 최대가로 = 합성중 != 0 ? 오른경계 : 너비, 최대세로 = 합성중 != 0 ? 아래경계 : 높이;
        if (가로 < 왼쪽) 가로 = 왼쪽;
        if (Vertikalno_položaj < 위쪽) Vertikalno_položaj = 위쪽;
        if (RIGHT > 최대가로) RIGHT = 최대가로;
        if (아래쪽 > 최대세로) 아래쪽 = 최대세로;
        if (RIGHT <= 가로 || 아래쪽 <= Vertikalno_položaj) return 0;
        잘린범위[0] = 가로; 잘린범위[1] = Vertikalno_položaj;
        잘린범위[2] = RIGHT - 가로; 잘린범위[3] = 아래쪽 - Vertikalno_položaj;
        return 1;
    }
    public static int Pokreni(int 가로, int Vertikalno_položaj, int 폭, int dužina_VALUE) {
        if (합성중 != 0 || dužina_VALUE > 32 || isječak(가로, Vertikalno_položaj, 폭, dužina_VALUE) == 0) return 0;
        왼경계 = 잘린범위[0]; 위경계 = 잘린범위[1];
        오른경계 = 왼경계 + 잘린범위[2]; 아래경계 = 위경계 + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean pokazivač_bit(int 가로, int Vertikalno_položaj, int oblik_VALUE) {
        if (oblik_VALUE == 1) return 가로 >= 0 && 가로 <= Vertikalno_položaj / 2 && Vertikalno_položaj < 16;
        if (oblik_VALUE == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - Vertikalno_položaj; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && Vertikalno_položaj >= 2 && Vertikalno_položaj <= 8 && (가로 <= 3 || Vertikalno_položaj <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && Vertikalno_položaj >= 12 && Vertikalno_položaj <= 18 && (가로 >= 17 || Vertikalno_položaj >= 17));
    }
    static int pokazivač_pel(int 가로, int Vertikalno_položaj) {
        if (pokazivač_bit(가로, Vertikalno_položaj, pokazivač_oblik)) return 2;
        for (int Linija = -1; Linija <= 1; Linija++) for (int prostor_za_unos_unos = -1; prostor_za_unos_unos <= 1; prostor_za_unos_unos++)
            if (pokazivač_bit(가로 + prostor_za_unos_unos, Vertikalno_položaj + Linija, pokazivač_oblik)) return 1;
        return 0;
    }
    static void ekran_pel(int 가로, int Vertikalno_položaj, int 색) {
        int prostor_za_unos_unos = 가로 - pokazivač_X, Linija = Vertikalno_položaj - pokazivač_Y;
        if (pokazivač_oblik != 0 && prostor_za_unos_unos >= 0 && Linija >= 0 && prostor_za_unos_unos < 21 && Linija < 21) {
            pokazivač_poster[Linija * 21 + prostor_za_unos_unos] = 색;
            int p_VALUE = pokazivač_pel(prostor_za_unos_unos, Linija); if (p_VALUE != 0) 색 = p_VALUE == 2 ? 0xffffff : 0x101010;
        }
        if (ploča.표시화소읽기(가로, Vertikalno_položaj) != 색) {
            ploča.pisati_ekran_pel(가로, Vertikalno_položaj, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void Kraj() {
        if (합성중 == 0) return;
        for (int Linija = 위경계; Linija < 아래경계; Linija++) for (int prostor_za_unos_unos = 왼경계; prostor_za_unos_unos < 오른경계; prostor_za_unos_unos++)
            ekran_pel(prostor_za_unos_unos, Linija, 완성그림[(Linija - 위경계) * 1920 + prostor_za_unos_unos]);
        합성중 = 0;
    }
    public static int pel(int 가로, int Vertikalno_položaj, int 색) {
        if (가로 < 0 || Vertikalno_položaj < 0 || 가로 >= 너비 || Vertikalno_položaj >= 높이) return 0;
        if (합성중 != 0) {
            if (가로 >= 왼경계 && 가로 < 오른경계 && Vertikalno_položaj >= 위경계 && Vertikalno_položaj < 아래경계)
                완성그림[(Vertikalno_položaj - 위경계) * 1920 + 가로] = 색;
        } else ekran_pel(가로, Vertikalno_položaj, 색);
        return 0;
    }
    public static void 사각그림(int 가로, int Vertikalno_položaj, int 폭, int dužina_VALUE, int 색) {
        if (isječak(가로, Vertikalno_položaj, 폭, dužina_VALUE) == 0) return;
        가로 = 잘린범위[0]; Vertikalno_položaj = 잘린범위[1]; 폭 = 잘린범위[2]; dužina_VALUE = 잘린범위[3];
        for (int Linija = Vertikalno_položaj; Linija < Vertikalno_položaj + dužina_VALUE; Linija++) for (int prostor_za_unos_unos = 가로; prostor_za_unos_unos < 가로 + 폭; prostor_za_unos_unos++) {
            if (합성중 != 0) 완성그림[(Linija - 위경계) * 1920 + prostor_za_unos_unos] = 색;
            else ekran_pel(prostor_za_unos_unos, Linija, 색);
        }
    }
    public static void pokazivač(int 가로, int Vertikalno_položaj, int oblik_VALUE) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (oblik_VALUE >= 2 ? 10 : 0), 새세로 = Vertikalno_položaj - (oblik_VALUE >= 2 ? 10 : 0);
        if (pokazivač_oblik == oblik_VALUE && pokazivač_X == 새가로 && pokazivač_Y == 새세로) return;
        if (pokazivač_oblik != 0) for (int Linija = 0; Linija < 21; Linija++) for (int prostor_za_unos_unos = 0; prostor_za_unos_unos < 21; prostor_za_unos_unos++) {
            int 가 = pokazivač_X + prostor_za_unos_unos, 세 = pokazivač_Y + Linija;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) ploča.pisati_ekran_pel(가, 세, pokazivač_poster[Linija * 21 + prostor_za_unos_unos]);
        }
        pokazivač_oblik = oblik_VALUE; pokazivač_X = 새가로; pokazivač_Y = 새세로;
        if (oblik_VALUE != 0) for (int Linija = 0; Linija < 21; Linija++) for (int prostor_za_unos_unos = 0; prostor_za_unos_unos < 21; prostor_za_unos_unos++) {
            int 가 = pokazivač_X + prostor_za_unos_unos, 세 = pokazivač_Y + Linija;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) {
                pokazivač_poster[Linija * 21 + prostor_za_unos_unos] = ploča.표시화소읽기(가, 세);
                int p_VALUE = pokazivač_pel(prostor_za_unos_unos, Linija); if (p_VALUE != 0) ploča.pisati_ekran_pel(가, 세, p_VALUE == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
