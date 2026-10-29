// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 화면 torri_VALUE·띠 합성·pwyntydd 밑그림을 관리한다. go_iawn_data 화면 Cof_data 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, 높이, 합성중, 왼경계, 위경계, 오른경계, 아래경계;
    static int pwyntydd_X, pwyntydd_Y, pwyntydd_siâp;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] pwyntydd_Cefndir = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void Paratoi(int 폭, int hyd_VALUE) {
        너비 = 폭; 높이 = hyd_VALUE; 합성중 = 0; pwyntydd_siâp = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int 높이얻기() { return 높이; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int clip_VALUE(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int START_VALUE, int hyd_VALUE) {
        if (START_VALUE > 2147483647 - hyd_VALUE) return 2147483647;
        return START_VALUE + hyd_VALUE;
    }
    public static int clip(int 가로, int Ar_i_fyny_safle, int 폭, int hyd_VALUE) {
        if (너비 == 0 || 폭 <= 0 || hyd_VALUE <= 0) return 0;
        int RIGHT = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(Ar_i_fyny_safle, hyd_VALUE);
        int 왼쪽 = 합성중 != 0 ? 왼경계 : 0, 위쪽 = 합성중 != 0 ? 위경계 : 0;
        int 최대가로 = 합성중 != 0 ? 오른경계 : 너비, 최대세로 = 합성중 != 0 ? 아래경계 : 높이;
        if (가로 < 왼쪽) 가로 = 왼쪽;
        if (Ar_i_fyny_safle < 위쪽) Ar_i_fyny_safle = 위쪽;
        if (RIGHT > 최대가로) RIGHT = 최대가로;
        if (아래쪽 > 최대세로) 아래쪽 = 최대세로;
        if (RIGHT <= 가로 || 아래쪽 <= Ar_i_fyny_safle) return 0;
        잘린범위[0] = 가로; 잘린범위[1] = Ar_i_fyny_safle;
        잘린범위[2] = RIGHT - 가로; 잘린범위[3] = 아래쪽 - Ar_i_fyny_safle;
        return 1;
    }
    public static int Gweithredu_2(int 가로, int Ar_i_fyny_safle, int 폭, int hyd_VALUE) {
        if (합성중 != 0 || hyd_VALUE > 32 || clip(가로, Ar_i_fyny_safle, 폭, hyd_VALUE) == 0) return 0;
        왼경계 = 잘린범위[0]; 위경계 = 잘린범위[1];
        오른경계 = 왼경계 + 잘린범위[2]; 아래경계 = 위경계 + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean pwyntydd_did(int 가로, int Ar_i_fyny_safle, int siâp_VALUE) {
        if (siâp_VALUE == 1) return 가로 >= 0 && 가로 <= Ar_i_fyny_safle / 2 && Ar_i_fyny_safle < 16;
        if (siâp_VALUE == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - Ar_i_fyny_safle; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && Ar_i_fyny_safle >= 2 && Ar_i_fyny_safle <= 8 && (가로 <= 3 || Ar_i_fyny_safle <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && Ar_i_fyny_safle >= 12 && Ar_i_fyny_safle <= 18 && (가로 >= 17 || Ar_i_fyny_safle >= 17));
    }
    static int pwyntydd_pel(int 가로, int Ar_i_fyny_safle) {
        if (pwyntydd_did(가로, Ar_i_fyny_safle, pwyntydd_siâp)) return 2;
        for (int llinell = -1; llinell <= 1; llinell++) for (int slot_cofnod = -1; slot_cofnod <= 1; slot_cofnod++)
            if (pwyntydd_did(가로 + slot_cofnod, Ar_i_fyny_safle + llinell, pwyntydd_siâp)) return 1;
        return 0;
    }
    static void dangos_pel(int 가로, int Ar_i_fyny_safle, int 색) {
        int slot_cofnod = 가로 - pwyntydd_X, llinell = Ar_i_fyny_safle - pwyntydd_Y;
        if (pwyntydd_siâp != 0 && slot_cofnod >= 0 && llinell >= 0 && slot_cofnod < 21 && llinell < 21) {
            pwyntydd_Cefndir[llinell * 21 + slot_cofnod] = 색;
            int p_VALUE = pwyntydd_pel(slot_cofnod, llinell); if (p_VALUE != 0) 색 = p_VALUE == 2 ? 0xffffff : 0x101010;
        }
        if (bwrdd.표시화소읽기(가로, Ar_i_fyny_safle) != 색) {
            bwrdd.ysgrifennu_dangos_pel(가로, Ar_i_fyny_safle, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void Gorffen() {
        if (합성중 == 0) return;
        for (int llinell = 위경계; llinell < 아래경계; llinell++) for (int slot_cofnod = 왼경계; slot_cofnod < 오른경계; slot_cofnod++)
            dangos_pel(slot_cofnod, llinell, 완성그림[(llinell - 위경계) * 1920 + slot_cofnod]);
        합성중 = 0;
    }
    public static int pel(int 가로, int Ar_i_fyny_safle, int 색) {
        if (가로 < 0 || Ar_i_fyny_safle < 0 || 가로 >= 너비 || Ar_i_fyny_safle >= 높이) return 0;
        if (합성중 != 0) {
            if (가로 >= 왼경계 && 가로 < 오른경계 && Ar_i_fyny_safle >= 위경계 && Ar_i_fyny_safle < 아래경계)
                완성그림[(Ar_i_fyny_safle - 위경계) * 1920 + 가로] = 색;
        } else dangos_pel(가로, Ar_i_fyny_safle, 색);
        return 0;
    }
    public static void 사각그림(int 가로, int Ar_i_fyny_safle, int 폭, int hyd_VALUE, int 색) {
        if (clip(가로, Ar_i_fyny_safle, 폭, hyd_VALUE) == 0) return;
        가로 = 잘린범위[0]; Ar_i_fyny_safle = 잘린범위[1]; 폭 = 잘린범위[2]; hyd_VALUE = 잘린범위[3];
        for (int llinell = Ar_i_fyny_safle; llinell < Ar_i_fyny_safle + hyd_VALUE; llinell++) for (int slot_cofnod = 가로; slot_cofnod < 가로 + 폭; slot_cofnod++) {
            if (합성중 != 0) 완성그림[(llinell - 위경계) * 1920 + slot_cofnod] = 색;
            else dangos_pel(slot_cofnod, llinell, 색);
        }
    }
    public static void pwyntydd(int 가로, int Ar_i_fyny_safle, int siâp_VALUE) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (siâp_VALUE >= 2 ? 10 : 0), 새세로 = Ar_i_fyny_safle - (siâp_VALUE >= 2 ? 10 : 0);
        if (pwyntydd_siâp == siâp_VALUE && pwyntydd_X == 새가로 && pwyntydd_Y == 새세로) return;
        if (pwyntydd_siâp != 0) for (int llinell = 0; llinell < 21; llinell++) for (int slot_cofnod = 0; slot_cofnod < 21; slot_cofnod++) {
            int 가 = pwyntydd_X + slot_cofnod, 세 = pwyntydd_Y + llinell;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) bwrdd.ysgrifennu_dangos_pel(가, 세, pwyntydd_Cefndir[llinell * 21 + slot_cofnod]);
        }
        pwyntydd_siâp = siâp_VALUE; pwyntydd_X = 새가로; pwyntydd_Y = 새세로;
        if (siâp_VALUE != 0) for (int llinell = 0; llinell < 21; llinell++) for (int slot_cofnod = 0; slot_cofnod < 21; slot_cofnod++) {
            int 가 = pwyntydd_X + slot_cofnod, 세 = pwyntydd_Y + llinell;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) {
                pwyntydd_Cefndir[llinell * 21 + slot_cofnod] = bwrdd.표시화소읽기(가, 세);
                int p_VALUE = pwyntydd_pel(slot_cofnod, llinell); if (p_VALUE != 0) bwrdd.ysgrifennu_dangos_pel(가, 세, p_VALUE == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
