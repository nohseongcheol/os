// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 화면 izrezati_VALUE·띠 합성·pokazivač 밑그림을 관리한다. stvaran_podaci 화면 Memorija_podaci 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, 높이, 합성중, 왼경계, 위경계, 오른경계, 아래경계;
    static int pokazivač_X, pokazivač_Y, pokazivač_oblik;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] pokazivač_podloga = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void Pripremi(int 폭, int 길이) {
        너비 = 폭; 높이 = 길이; 합성중 = 0; pokazivač_oblik = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int 높이얻기() { return 높이; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int isječak_VALUE(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int START_VALUE, int 길이) {
        if (START_VALUE > 2147483647 - 길이) return 2147483647;
        return START_VALUE + 길이;
    }
    public static int isječak(int 가로, int Okomito_položaj, int 폭, int 길이) {
        if (너비 == 0 || 폭 <= 0 || 길이 <= 0) return 0;
        int RIGHT = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(Okomito_položaj, 길이);
        int 왼쪽 = 합성중 != 0 ? 왼경계 : 0, 위쪽 = 합성중 != 0 ? 위경계 : 0;
        int 최대가로 = 합성중 != 0 ? 오른경계 : 너비, 최대세로 = 합성중 != 0 ? 아래경계 : 높이;
        if (가로 < 왼쪽) 가로 = 왼쪽;
        if (Okomito_položaj < 위쪽) Okomito_položaj = 위쪽;
        if (RIGHT > 최대가로) RIGHT = 최대가로;
        if (아래쪽 > 최대세로) 아래쪽 = 최대세로;
        if (RIGHT <= 가로 || 아래쪽 <= Okomito_položaj) return 0;
        잘린범위[0] = 가로; 잘린범위[1] = Okomito_položaj;
        잘린범위[2] = RIGHT - 가로; 잘린범위[3] = 아래쪽 - Okomito_položaj;
        return 1;
    }
    public static int Pokreni(int 가로, int Okomito_položaj, int 폭, int 길이) {
        if (합성중 != 0 || 길이 > 32 || isječak(가로, Okomito_položaj, 폭, 길이) == 0) return 0;
        왼경계 = 잘린범위[0]; 위경계 = 잘린범위[1];
        오른경계 = 왼경계 + 잘린범위[2]; 아래경계 = 위경계 + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean pokazivač_bit(int 가로, int Okomito_položaj, int oblik_VALUE_f1cd655a) {
        if (oblik_VALUE_f1cd655a == 1) return 가로 >= 0 && 가로 <= Okomito_položaj / 2 && Okomito_položaj < 16;
        if (oblik_VALUE_f1cd655a == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - Okomito_položaj; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && Okomito_položaj >= 2 && Okomito_položaj <= 8 && (가로 <= 3 || Okomito_položaj <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && Okomito_položaj >= 12 && Okomito_položaj <= 18 && (가로 >= 17 || Okomito_položaj >= 17));
    }
    static int pokazivač_slikovni_element(int 가로, int Okomito_položaj) {
        if (pokazivač_bit(가로, Okomito_položaj, pokazivač_oblik)) return 2;
        for (int red = -1; red <= 1; red++) for (int 칸 = -1; 칸 <= 1; 칸++)
            if (pokazivač_bit(가로 + 칸, Okomito_položaj + red, pokazivač_oblik)) return 1;
        return 0;
    }
    static void zaslon_slikovni_element(int 가로, int Okomito_položaj, int 색) {
        int 칸 = 가로 - pokazivač_X, red = Okomito_položaj - pokazivač_Y;
        if (pokazivač_oblik != 0 && 칸 >= 0 && red >= 0 && 칸 < 21 && red < 21) {
            pokazivač_podloga[red * 21 + 칸] = 색;
            int p_VALUE = pokazivač_slikovni_element(칸, red); if (p_VALUE != 0) 색 = p_VALUE == 2 ? 0xffffff : 0x101010;
        }
        if (pano.표시화소읽기(가로, Okomito_položaj) != 색) {
            pano.zapisivanje_zaslon_slikovni_element(가로, Okomito_položaj, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void Završi() {
        if (합성중 == 0) return;
        for (int red = 위경계; red < 아래경계; red++) for (int 칸 = 왼경계; 칸 < 오른경계; 칸++)
            zaslon_slikovni_element(칸, red, 완성그림[(red - 위경계) * 1920 + 칸]);
        합성중 = 0;
    }
    public static int slikovni_element(int 가로, int Okomito_položaj, int 색) {
        if (가로 < 0 || Okomito_položaj < 0 || 가로 >= 너비 || Okomito_položaj >= 높이) return 0;
        if (합성중 != 0) {
            if (가로 >= 왼경계 && 가로 < 오른경계 && Okomito_položaj >= 위경계 && Okomito_položaj < 아래경계)
                완성그림[(Okomito_položaj - 위경계) * 1920 + 가로] = 색;
        } else zaslon_slikovni_element(가로, Okomito_položaj, 색);
        return 0;
    }
    public static void pravokutnik_ispuna(int 가로, int Okomito_položaj, int 폭, int 길이, int 색) {
        if (isječak(가로, Okomito_položaj, 폭, 길이) == 0) return;
        가로 = 잘린범위[0]; Okomito_položaj = 잘린범위[1]; 폭 = 잘린범위[2]; 길이 = 잘린범위[3];
        for (int red = Okomito_položaj; red < Okomito_položaj + 길이; red++) for (int 칸 = 가로; 칸 < 가로 + 폭; 칸++) {
            if (합성중 != 0) 완성그림[(red - 위경계) * 1920 + 칸] = 색;
            else zaslon_slikovni_element(칸, red, 색);
        }
    }
    public static void pokazivač(int 가로, int Okomito_položaj, int oblik_VALUE_f1cd655a) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (oblik_VALUE_f1cd655a >= 2 ? 10 : 0), 새세로 = Okomito_položaj - (oblik_VALUE_f1cd655a >= 2 ? 10 : 0);
        if (pokazivač_oblik == oblik_VALUE_f1cd655a && pokazivač_X == 새가로 && pokazivač_Y == 새세로) return;
        if (pokazivač_oblik != 0) for (int red = 0; red < 21; red++) for (int 칸 = 0; 칸 < 21; 칸++) {
            int 가 = pokazivač_X + 칸, 세 = pokazivač_Y + red;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) pano.zapisivanje_zaslon_slikovni_element(가, 세, pokazivač_podloga[red * 21 + 칸]);
        }
        pokazivač_oblik = oblik_VALUE_f1cd655a; pokazivač_X = 새가로; pokazivač_Y = 새세로;
        if (oblik_VALUE_f1cd655a != 0) for (int red = 0; red < 21; red++) for (int 칸 = 0; 칸 < 21; 칸++) {
            int 가 = pokazivač_X + 칸, 세 = pokazivač_Y + red;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) {
                pokazivač_podloga[red * 21 + 칸] = pano.표시화소읽기(가, 세);
                int p_VALUE = pokazivač_slikovni_element(칸, red); if (p_VALUE != 0) pano.zapisivanje_zaslon_slikovni_element(가, 세, p_VALUE == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
