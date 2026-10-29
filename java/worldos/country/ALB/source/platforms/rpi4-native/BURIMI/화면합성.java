// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 화면 pres_VALUE·띠 합성·tregues 밑그림을 관리한다. aktual_të_dhëna 화면 Memorie_të_dhëna 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, 높이, 합성중, 왼경계, 위경계, 오른경계, 아래경계;
    static int tregues_X, tregues_Y, tregues_formë;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] tregues_Sfond = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void Përgatit(int 폭, int gjatësi_VALUE) {
        너비 = 폭; 높이 = gjatësi_VALUE; 합성중 = 0; tregues_formë = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int 높이얻기() { return 높이; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int fragment_VALUE(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int nis_VALUE, int gjatësi_VALUE) {
        if (nis_VALUE > 2147483647 - gjatësi_VALUE) return 2147483647;
        return nis_VALUE + gjatësi_VALUE;
    }
    public static int fragment(int 가로, int Vertikal_pozicioni, int 폭, int gjatësi_VALUE) {
        if (너비 == 0 || 폭 <= 0 || gjatësi_VALUE <= 0) return 0;
        int RIGHT = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(Vertikal_pozicioni, gjatësi_VALUE);
        int 왼쪽 = 합성중 != 0 ? 왼경계 : 0, 위쪽 = 합성중 != 0 ? 위경계 : 0;
        int 최대가로 = 합성중 != 0 ? 오른경계 : 너비, 최대세로 = 합성중 != 0 ? 아래경계 : 높이;
        if (가로 < 왼쪽) 가로 = 왼쪽;
        if (Vertikal_pozicioni < 위쪽) Vertikal_pozicioni = 위쪽;
        if (RIGHT > 최대가로) RIGHT = 최대가로;
        if (아래쪽 > 최대세로) 아래쪽 = 최대세로;
        if (RIGHT <= 가로 || 아래쪽 <= Vertikal_pozicioni) return 0;
        잘린범위[0] = 가로; 잘린범위[1] = Vertikal_pozicioni;
        잘린범위[2] = RIGHT - 가로; 잘린범위[3] = 아래쪽 - Vertikal_pozicioni;
        return 1;
    }
    public static int Ekzekuto(int 가로, int Vertikal_pozicioni, int 폭, int gjatësi_VALUE) {
        if (합성중 != 0 || gjatësi_VALUE > 32 || fragment(가로, Vertikal_pozicioni, 폭, gjatësi_VALUE) == 0) return 0;
        왼경계 = 잘린범위[0]; 위경계 = 잘린범위[1];
        오른경계 = 왼경계 + 잘린범위[2]; 아래경계 = 위경계 + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean tregues_bit(int 가로, int Vertikal_pozicioni, int formë_VALUE) {
        if (formë_VALUE == 1) return 가로 >= 0 && 가로 <= Vertikal_pozicioni / 2 && Vertikal_pozicioni < 16;
        if (formë_VALUE == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - Vertikal_pozicioni; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && Vertikal_pozicioni >= 2 && Vertikal_pozicioni <= 8 && (가로 <= 3 || Vertikal_pozicioni <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && Vertikal_pozicioni >= 12 && Vertikal_pozicioni <= 18 && (가로 >= 17 || Vertikal_pozicioni >= 17));
    }
    static int tregues_pikëz(int 가로, int Vertikal_pozicioni) {
        if (tregues_bit(가로, Vertikal_pozicioni, tregues_formë)) return 2;
        for (int linjë = -1; linjë <= 1; linjë++) for (int hapësirë_për_tekst_futje = -1; hapësirë_për_tekst_futje <= 1; hapësirë_për_tekst_futje++)
            if (tregues_bit(가로 + hapësirë_për_tekst_futje, Vertikal_pozicioni + linjë, tregues_formë)) return 1;
        return 0;
    }
    static void afishim_pikëz(int 가로, int Vertikal_pozicioni, int 색) {
        int hapësirë_për_tekst_futje = 가로 - tregues_X, linjë = Vertikal_pozicioni - tregues_Y;
        if (tregues_formë != 0 && hapësirë_për_tekst_futje >= 0 && linjë >= 0 && hapësirë_për_tekst_futje < 21 && linjë < 21) {
            tregues_Sfond[linjë * 21 + hapësirë_për_tekst_futje] = 색;
            int p_VALUE = tregues_pikëz(hapësirë_për_tekst_futje, linjë); if (p_VALUE != 0) 색 = p_VALUE == 2 ? 0xffffff : 0x101010;
        }
        if (panel.표시화소읽기(가로, Vertikal_pozicioni) != 색) {
            panel.shkruaj_afishim_pikëz(가로, Vertikal_pozicioni, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void Përfundo() {
        if (합성중 == 0) return;
        for (int linjë = 위경계; linjë < 아래경계; linjë++) for (int hapësirë_për_tekst_futje = 왼경계; hapësirë_për_tekst_futje < 오른경계; hapësirë_për_tekst_futje++)
            afishim_pikëz(hapësirë_për_tekst_futje, linjë, 완성그림[(linjë - 위경계) * 1920 + hapësirë_për_tekst_futje]);
        합성중 = 0;
    }
    public static int pikëz(int 가로, int Vertikal_pozicioni, int 색) {
        if (가로 < 0 || Vertikal_pozicioni < 0 || 가로 >= 너비 || Vertikal_pozicioni >= 높이) return 0;
        if (합성중 != 0) {
            if (가로 >= 왼경계 && 가로 < 오른경계 && Vertikal_pozicioni >= 위경계 && Vertikal_pozicioni < 아래경계)
                완성그림[(Vertikal_pozicioni - 위경계) * 1920 + 가로] = 색;
        } else afishim_pikëz(가로, Vertikal_pozicioni, 색);
        return 0;
    }
    public static void 사각그림(int 가로, int Vertikal_pozicioni, int 폭, int gjatësi_VALUE, int 색) {
        if (fragment(가로, Vertikal_pozicioni, 폭, gjatësi_VALUE) == 0) return;
        가로 = 잘린범위[0]; Vertikal_pozicioni = 잘린범위[1]; 폭 = 잘린범위[2]; gjatësi_VALUE = 잘린범위[3];
        for (int linjë = Vertikal_pozicioni; linjë < Vertikal_pozicioni + gjatësi_VALUE; linjë++) for (int hapësirë_për_tekst_futje = 가로; hapësirë_për_tekst_futje < 가로 + 폭; hapësirë_për_tekst_futje++) {
            if (합성중 != 0) 완성그림[(linjë - 위경계) * 1920 + hapësirë_për_tekst_futje] = 색;
            else afishim_pikëz(hapësirë_për_tekst_futje, linjë, 색);
        }
    }
    public static void tregues(int 가로, int Vertikal_pozicioni, int formë_VALUE) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (formë_VALUE >= 2 ? 10 : 0), 새세로 = Vertikal_pozicioni - (formë_VALUE >= 2 ? 10 : 0);
        if (tregues_formë == formë_VALUE && tregues_X == 새가로 && tregues_Y == 새세로) return;
        if (tregues_formë != 0) for (int linjë = 0; linjë < 21; linjë++) for (int hapësirë_për_tekst_futje = 0; hapësirë_për_tekst_futje < 21; hapësirë_për_tekst_futje++) {
            int 가 = tregues_X + hapësirë_për_tekst_futje, 세 = tregues_Y + linjë;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) panel.shkruaj_afishim_pikëz(가, 세, tregues_Sfond[linjë * 21 + hapësirë_për_tekst_futje]);
        }
        tregues_formë = formë_VALUE; tregues_X = 새가로; tregues_Y = 새세로;
        if (formë_VALUE != 0) for (int linjë = 0; linjë < 21; linjë++) for (int hapësirë_për_tekst_futje = 0; hapësirë_për_tekst_futje < 21; hapësirë_për_tekst_futje++) {
            int 가 = tregues_X + hapësirë_për_tekst_futje, 세 = tregues_Y + linjë;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) {
                tregues_Sfond[linjë * 21 + hapësirë_për_tekst_futje] = panel.표시화소읽기(가, 세);
                int p_VALUE = tregues_pikëz(hapësirë_për_tekst_futje, linjë); if (p_VALUE != 0) panel.shkruaj_afishim_pikëz(가, 세, p_VALUE == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
