// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 화면 lõikama_VALUE·띠 합성·kursor 밑그림을 관리한다. tegelik_andmed 화면 Mälu_andmed 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, 높이, 합성중, 왼경계, 위경계, 오른경계, 아래경계;
    static int kursor_X, kursor_Y, kursor_kujund;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] kursor_taust = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void Ettevalmistamine(int 폭, int 길이) {
        너비 = 폭; 높이 = 길이; 합성중 = 0; kursor_kujund = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int 높이얻기() { return 높이; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int klipp_VALUE(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int START_VALUE, int 길이) {
        if (START_VALUE > 2147483647 - 길이) return 2147483647;
        return START_VALUE + 길이;
    }
    public static int klipp(int 가로, int vertikaal_ametikoht, int 폭, int 길이) {
        if (너비 == 0 || 폭 <= 0 || 길이 <= 0) return 0;
        int RIGHT = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(vertikaal_ametikoht, 길이);
        int 왼쪽 = 합성중 != 0 ? 왼경계 : 0, 위쪽 = 합성중 != 0 ? 위경계 : 0;
        int 최대가로 = 합성중 != 0 ? 오른경계 : 너비, 최대세로 = 합성중 != 0 ? 아래경계 : 높이;
        if (가로 < 왼쪽) 가로 = 왼쪽;
        if (vertikaal_ametikoht < 위쪽) vertikaal_ametikoht = 위쪽;
        if (RIGHT > 최대가로) RIGHT = 최대가로;
        if (아래쪽 > 최대세로) 아래쪽 = 최대세로;
        if (RIGHT <= 가로 || 아래쪽 <= vertikaal_ametikoht) return 0;
        잘린범위[0] = 가로; 잘린범위[1] = vertikaal_ametikoht;
        잘린범위[2] = RIGHT - 가로; 잘린범위[3] = 아래쪽 - vertikaal_ametikoht;
        return 1;
    }
    public static int Käivita_2(int 가로, int vertikaal_ametikoht, int 폭, int 길이) {
        if (합성중 != 0 || 길이 > 32 || klipp(가로, vertikaal_ametikoht, 폭, 길이) == 0) return 0;
        왼경계 = 잘린범위[0]; 위경계 = 잘린범위[1];
        오른경계 = 왼경계 + 잘린범위[2]; 아래경계 = 위경계 + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean kursor_bitt(int 가로, int vertikaal_ametikoht, int kujund_VALUE) {
        if (kujund_VALUE == 1) return 가로 >= 0 && 가로 <= vertikaal_ametikoht / 2 && vertikaal_ametikoht < 16;
        if (kujund_VALUE == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - vertikaal_ametikoht; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && vertikaal_ametikoht >= 2 && vertikaal_ametikoht <= 8 && (가로 <= 3 || vertikaal_ametikoht <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && vertikaal_ametikoht >= 12 && vertikaal_ametikoht <= 18 && (가로 >= 17 || vertikaal_ametikoht >= 17));
    }
    static int kursor_piksel(int 가로, int vertikaal_ametikoht) {
        if (kursor_bitt(가로, vertikaal_ametikoht, kursor_kujund)) return 2;
        for (int Joon = -1; Joon <= 1; Joon++) for (int 칸 = -1; 칸 <= 1; 칸++)
            if (kursor_bitt(가로 + 칸, vertikaal_ametikoht + Joon, kursor_kujund)) return 1;
        return 0;
    }
    static void ekraan_piksel(int 가로, int vertikaal_ametikoht, int 색) {
        int 칸 = 가로 - kursor_X, Joon = vertikaal_ametikoht - kursor_Y;
        if (kursor_kujund != 0 && 칸 >= 0 && Joon >= 0 && 칸 < 21 && Joon < 21) {
            kursor_taust[Joon * 21 + 칸] = 색;
            int p_VALUE = kursor_piksel(칸, Joon); if (p_VALUE != 0) 색 = p_VALUE == 2 ? 0xffffff : 0x101010;
        }
        if (Tahvel.표시화소읽기(가로, vertikaal_ametikoht) != 색) {
            Tahvel.kirjutamine_ekraan_piksel(가로, vertikaal_ametikoht, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void lõpp() {
        if (합성중 == 0) return;
        for (int Joon = 위경계; Joon < 아래경계; Joon++) for (int 칸 = 왼경계; 칸 < 오른경계; 칸++)
            ekraan_piksel(칸, Joon, 완성그림[(Joon - 위경계) * 1920 + 칸]);
        합성중 = 0;
    }
    public static int piksel(int 가로, int vertikaal_ametikoht, int 색) {
        if (가로 < 0 || vertikaal_ametikoht < 0 || 가로 >= 너비 || vertikaal_ametikoht >= 높이) return 0;
        if (합성중 != 0) {
            if (가로 >= 왼경계 && 가로 < 오른경계 && vertikaal_ametikoht >= 위경계 && vertikaal_ametikoht < 아래경계)
                완성그림[(vertikaal_ametikoht - 위경계) * 1920 + 가로] = 색;
        } else ekraan_piksel(가로, vertikaal_ametikoht, 색);
        return 0;
    }
    public static void ristkülik_täide(int 가로, int vertikaal_ametikoht, int 폭, int 길이, int 색) {
        if (klipp(가로, vertikaal_ametikoht, 폭, 길이) == 0) return;
        가로 = 잘린범위[0]; vertikaal_ametikoht = 잘린범위[1]; 폭 = 잘린범위[2]; 길이 = 잘린범위[3];
        for (int Joon = vertikaal_ametikoht; Joon < vertikaal_ametikoht + 길이; Joon++) for (int 칸 = 가로; 칸 < 가로 + 폭; 칸++) {
            if (합성중 != 0) 완성그림[(Joon - 위경계) * 1920 + 칸] = 색;
            else ekraan_piksel(칸, Joon, 색);
        }
    }
    public static void kursor(int 가로, int vertikaal_ametikoht, int kujund_VALUE) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (kujund_VALUE >= 2 ? 10 : 0), 새세로 = vertikaal_ametikoht - (kujund_VALUE >= 2 ? 10 : 0);
        if (kursor_kujund == kujund_VALUE && kursor_X == 새가로 && kursor_Y == 새세로) return;
        if (kursor_kujund != 0) for (int Joon = 0; Joon < 21; Joon++) for (int 칸 = 0; 칸 < 21; 칸++) {
            int 가 = kursor_X + 칸, 세 = kursor_Y + Joon;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) Tahvel.kirjutamine_ekraan_piksel(가, 세, kursor_taust[Joon * 21 + 칸]);
        }
        kursor_kujund = kujund_VALUE; kursor_X = 새가로; kursor_Y = 새세로;
        if (kujund_VALUE != 0) for (int Joon = 0; Joon < 21; Joon++) for (int 칸 = 0; 칸 < 21; 칸++) {
            int 가 = kursor_X + 칸, 세 = kursor_Y + Joon;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) {
                kursor_taust[Joon * 21 + 칸] = Tahvel.표시화소읽기(가, 세);
                int p_VALUE = kursor_piksel(칸, Joon); if (p_VALUE != 0) Tahvel.kirjutamine_ekraan_piksel(가, 세, p_VALUE == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
