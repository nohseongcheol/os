// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 화면 strihať_VALUE·띠 합성·ukazovateľ 밑그림을 관리한다. skutočný_údaje 화면 Pamäť_údaje 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, výška_VALUE, 합성중, 왼경계, 위경계, 오른경계, 아래경계;
    static int ukazovateľ_X, ukazovateľ_Y, ukazovateľ_tvar;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] ukazovateľ_tapeta = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void Pripraviť(int 폭, int dĺžka_VALUE) {
        너비 = 폭; výška_VALUE = dĺžka_VALUE; 합성중 = 0; ukazovateľ_tvar = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int načítať_výška() { return výška_VALUE; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int klip_VALUE(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int START_VALUE, int dĺžka_VALUE) {
        if (START_VALUE > 2147483647 - dĺžka_VALUE) return 2147483647;
        return START_VALUE + dĺžka_VALUE;
    }
    public static int klip(int 가로, int vertikála_pozícia, int 폭, int dĺžka_VALUE) {
        if (너비 == 0 || 폭 <= 0 || dĺžka_VALUE <= 0) return 0;
        int RIGHT = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(vertikála_pozícia, dĺžka_VALUE);
        int 왼쪽 = 합성중 != 0 ? 왼경계 : 0, 위쪽 = 합성중 != 0 ? 위경계 : 0;
        int 최대가로 = 합성중 != 0 ? 오른경계 : 너비, 최대세로 = 합성중 != 0 ? 아래경계 : výška_VALUE;
        if (가로 < 왼쪽) 가로 = 왼쪽;
        if (vertikála_pozícia < 위쪽) vertikála_pozícia = 위쪽;
        if (RIGHT > 최대가로) RIGHT = 최대가로;
        if (아래쪽 > 최대세로) 아래쪽 = 최대세로;
        if (RIGHT <= 가로 || 아래쪽 <= vertikála_pozícia) return 0;
        잘린범위[0] = 가로; 잘린범위[1] = vertikála_pozícia;
        잘린범위[2] = RIGHT - 가로; 잘린범위[3] = 아래쪽 - vertikála_pozícia;
        return 1;
    }
    public static int Spustiť_2(int 가로, int vertikála_pozícia, int 폭, int dĺžka_VALUE) {
        if (합성중 != 0 || dĺžka_VALUE > 32 || klip(가로, vertikála_pozícia, 폭, dĺžka_VALUE) == 0) return 0;
        왼경계 = 잘린범위[0]; 위경계 = 잘린범위[1];
        오른경계 = 왼경계 + 잘린범위[2]; 아래경계 = 위경계 + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean ukazovateľ_Bit(int 가로, int vertikála_pozícia, int tvar_VALUE) {
        if (tvar_VALUE == 1) return 가로 >= 0 && 가로 <= vertikála_pozícia / 2 && vertikála_pozícia < 16;
        if (tvar_VALUE == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - vertikála_pozícia; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && vertikála_pozícia >= 2 && vertikála_pozícia <= 8 && (가로 <= 3 || vertikála_pozícia <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && vertikála_pozícia >= 12 && vertikála_pozícia <= 18 && (가로 >= 17 || vertikála_pozícia >= 17));
    }
    static int ukazovateľ_pixel(int 가로, int vertikála_pozícia) {
        if (ukazovateľ_Bit(가로, vertikála_pozícia, ukazovateľ_tvar)) return 2;
        for (int riadok = -1; riadok <= 1; riadok++) for (int 칸 = -1; 칸 <= 1; 칸++)
            if (ukazovateľ_Bit(가로 + 칸, vertikála_pozícia + riadok, ukazovateľ_tvar)) return 1;
        return 0;
    }
    static void displej_pixel(int 가로, int vertikála_pozícia, int 색) {
        int 칸 = 가로 - ukazovateľ_X, riadok = vertikála_pozícia - ukazovateľ_Y;
        if (ukazovateľ_tvar != 0 && 칸 >= 0 && riadok >= 0 && 칸 < 21 && riadok < 21) {
            ukazovateľ_tapeta[riadok * 21 + 칸] = 색;
            int bod_VALUE = ukazovateľ_pixel(칸, riadok); if (bod_VALUE != 0) 색 = bod_VALUE == 2 ? 0xffffff : 0x101010;
        }
        if (Panel.표시화소읽기(가로, vertikála_pozícia) != 색) {
            Panel.zapísať_displej_pixel(가로, vertikála_pozícia, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void Dokončiť() {
        if (합성중 == 0) return;
        for (int riadok = 위경계; riadok < 아래경계; riadok++) for (int 칸 = 왼경계; 칸 < 오른경계; 칸++)
            displej_pixel(칸, riadok, 완성그림[(riadok - 위경계) * 1920 + 칸]);
        합성중 = 0;
    }
    public static int pixel(int 가로, int vertikála_pozícia, int 색) {
        if (가로 < 0 || vertikála_pozícia < 0 || 가로 >= 너비 || vertikála_pozícia >= výška_VALUE) return 0;
        if (합성중 != 0) {
            if (가로 >= 왼경계 && 가로 < 오른경계 && vertikála_pozícia >= 위경계 && vertikála_pozícia < 아래경계)
                완성그림[(vertikála_pozícia - 위경계) * 1920 + 가로] = 색;
        } else displej_pixel(가로, vertikála_pozícia, 색);
        return 0;
    }
    public static void obdĺžnik_výplň(int 가로, int vertikála_pozícia, int 폭, int dĺžka_VALUE, int 색) {
        if (klip(가로, vertikála_pozícia, 폭, dĺžka_VALUE) == 0) return;
        가로 = 잘린범위[0]; vertikála_pozícia = 잘린범위[1]; 폭 = 잘린범위[2]; dĺžka_VALUE = 잘린범위[3];
        for (int riadok = vertikála_pozícia; riadok < vertikála_pozícia + dĺžka_VALUE; riadok++) for (int 칸 = 가로; 칸 < 가로 + 폭; 칸++) {
            if (합성중 != 0) 완성그림[(riadok - 위경계) * 1920 + 칸] = 색;
            else displej_pixel(칸, riadok, 색);
        }
    }
    public static void ukazovateľ(int 가로, int vertikála_pozícia, int tvar_VALUE) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (tvar_VALUE >= 2 ? 10 : 0), 새세로 = vertikála_pozícia - (tvar_VALUE >= 2 ? 10 : 0);
        if (ukazovateľ_tvar == tvar_VALUE && ukazovateľ_X == 새가로 && ukazovateľ_Y == 새세로) return;
        if (ukazovateľ_tvar != 0) for (int riadok = 0; riadok < 21; riadok++) for (int 칸 = 0; 칸 < 21; 칸++) {
            int 가 = ukazovateľ_X + 칸, 세 = ukazovateľ_Y + riadok;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < výška_VALUE) Panel.zapísať_displej_pixel(가, 세, ukazovateľ_tapeta[riadok * 21 + 칸]);
        }
        ukazovateľ_tvar = tvar_VALUE; ukazovateľ_X = 새가로; ukazovateľ_Y = 새세로;
        if (tvar_VALUE != 0) for (int riadok = 0; riadok < 21; riadok++) for (int 칸 = 0; 칸 < 21; 칸++) {
            int 가 = ukazovateľ_X + 칸, 세 = ukazovateľ_Y + riadok;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < výška_VALUE) {
                ukazovateľ_tapeta[riadok * 21 + 칸] = Panel.표시화소읽기(가, 세);
                int bod_VALUE = ukazovateľ_pixel(칸, riadok); if (bod_VALUE != 0) Panel.zapísať_displej_pixel(가, 세, bod_VALUE == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
