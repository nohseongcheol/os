// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 화면 iseći_VALUE·띠 합성·pokazivač 밑그림을 관리한다. stvarni_podaci 화면 Memorija_podaci 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, 높이, 합성중, 왼경계, 위경계, 오른경계, 아래경계;
    static int pokazivač_X, pokazivač_Y, pokazivač_oblik;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] pokazivač_poster = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void Pripremi(int 폭, int 길이) {
        너비 = 폭; 높이 = 길이; 합성중 = 0; pokazivač_oblik = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int 높이얻기() { return 높이; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int klip_VALUE(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int START_VALUE, int 길이) {
        if (START_VALUE > 2147483647 - 길이) return 2147483647;
        return START_VALUE + 길이;
    }
    public static int klip(int 가로, int vertikala_pozicija, int 폭, int 길이) {
        if (너비 == 0 || 폭 <= 0 || 길이 <= 0) return 0;
        int RIGHT = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(vertikala_pozicija, 길이);
        int 왼쪽 = 합성중 != 0 ? 왼경계 : 0, 위쪽 = 합성중 != 0 ? 위경계 : 0;
        int 최대가로 = 합성중 != 0 ? 오른경계 : 너비, 최대세로 = 합성중 != 0 ? 아래경계 : 높이;
        if (가로 < 왼쪽) 가로 = 왼쪽;
        if (vertikala_pozicija < 위쪽) vertikala_pozicija = 위쪽;
        if (RIGHT > 최대가로) RIGHT = 최대가로;
        if (아래쪽 > 최대세로) 아래쪽 = 최대세로;
        if (RIGHT <= 가로 || 아래쪽 <= vertikala_pozicija) return 0;
        잘린범위[0] = 가로; 잘린범위[1] = vertikala_pozicija;
        잘린범위[2] = RIGHT - 가로; 잘린범위[3] = 아래쪽 - vertikala_pozicija;
        return 1;
    }
    public static int koristiti(int 가로, int vertikala_pozicija, int 폭, int 길이) {
        if (합성중 != 0 || 길이 > 32 || klip(가로, vertikala_pozicija, 폭, 길이) == 0) return 0;
        왼경계 = 잘린범위[0]; 위경계 = 잘린범위[1];
        오른경계 = 왼경계 + 잘린범위[2]; 아래경계 = 위경계 + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean pokazivač_bit(int 가로, int vertikala_pozicija, int oblik_VALUE) {
        if (oblik_VALUE == 1) return 가로 >= 0 && 가로 <= vertikala_pozicija / 2 && vertikala_pozicija < 16;
        if (oblik_VALUE == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - vertikala_pozicija; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && vertikala_pozicija >= 2 && vertikala_pozicija <= 8 && (가로 <= 3 || vertikala_pozicija <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && vertikala_pozicija >= 12 && vertikala_pozicija <= 18 && (가로 >= 17 || vertikala_pozicija >= 17));
    }
    static int pokazivač_piksel(int 가로, int vertikala_pozicija) {
        if (pokazivač_bit(가로, vertikala_pozicija, pokazivač_oblik)) return 2;
        for (int red = -1; red <= 1; red++) for (int 칸 = -1; 칸 <= 1; 칸++)
            if (pokazivač_bit(가로 + 칸, vertikala_pozicija + red, pokazivač_oblik)) return 1;
        return 0;
    }
    static void ekran_piksel(int 가로, int vertikala_pozicija, int 색) {
        int 칸 = 가로 - pokazivač_X, red = vertikala_pozicija - pokazivač_Y;
        if (pokazivač_oblik != 0 && 칸 >= 0 && red >= 0 && 칸 < 21 && red < 21) {
            pokazivač_poster[red * 21 + 칸] = 색;
            int p_VALUE = pokazivač_piksel(칸, red); if (p_VALUE != 0) 색 = p_VALUE == 2 ? 0xffffff : 0x101010;
        }
        if (Tabla.표시화소읽기(가로, vertikala_pozicija) != 색) {
            Tabla.표시화소쓰기(가로, vertikala_pozicija, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void kraj() {
        if (합성중 == 0) return;
        for (int red = 위경계; red < 아래경계; red++) for (int 칸 = 왼경계; 칸 < 오른경계; 칸++)
            ekran_piksel(칸, red, 완성그림[(red - 위경계) * 1920 + 칸]);
        합성중 = 0;
    }
    public static int piksel(int 가로, int vertikala_pozicija, int 색) {
        if (가로 < 0 || vertikala_pozicija < 0 || 가로 >= 너비 || vertikala_pozicija >= 높이) return 0;
        if (합성중 != 0) {
            if (가로 >= 왼경계 && 가로 < 오른경계 && vertikala_pozicija >= 위경계 && vertikala_pozicija < 아래경계)
                완성그림[(vertikala_pozicija - 위경계) * 1920 + 가로] = 색;
        } else ekran_piksel(가로, vertikala_pozicija, 색);
        return 0;
    }
    public static void 사각그림(int 가로, int vertikala_pozicija, int 폭, int 길이, int 색) {
        if (klip(가로, vertikala_pozicija, 폭, 길이) == 0) return;
        가로 = 잘린범위[0]; vertikala_pozicija = 잘린범위[1]; 폭 = 잘린범위[2]; 길이 = 잘린범위[3];
        for (int red = vertikala_pozicija; red < vertikala_pozicija + 길이; red++) for (int 칸 = 가로; 칸 < 가로 + 폭; 칸++) {
            if (합성중 != 0) 완성그림[(red - 위경계) * 1920 + 칸] = 색;
            else ekran_piksel(칸, red, 색);
        }
    }
    public static void pokazivač(int 가로, int vertikala_pozicija, int oblik_VALUE) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (oblik_VALUE >= 2 ? 10 : 0), 새세로 = vertikala_pozicija - (oblik_VALUE >= 2 ? 10 : 0);
        if (pokazivač_oblik == oblik_VALUE && pokazivač_X == 새가로 && pokazivač_Y == 새세로) return;
        if (pokazivač_oblik != 0) for (int red = 0; red < 21; red++) for (int 칸 = 0; 칸 < 21; 칸++) {
            int 가 = pokazivač_X + 칸, 세 = pokazivač_Y + red;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) Tabla.표시화소쓰기(가, 세, pokazivač_poster[red * 21 + 칸]);
        }
        pokazivač_oblik = oblik_VALUE; pokazivač_X = 새가로; pokazivač_Y = 새세로;
        if (oblik_VALUE != 0) for (int red = 0; red < 21; red++) for (int 칸 = 0; 칸 < 21; 칸++) {
            int 가 = pokazivač_X + 칸, 세 = pokazivač_Y + red;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) {
                pokazivač_poster[red * 21 + 칸] = Tabla.표시화소읽기(가, 세);
                int p_VALUE = pokazivač_piksel(칸, red); if (p_VALUE != 0) Tabla.표시화소쓰기(가, 세, p_VALUE == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
