// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 화면 klippe_VALUE·띠 합성·peikar 밑그림을 관리한다. faktisk_data 화면 Minne_data 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, 높이, 합성중, 왼경계, 위경계, 오른경계, 아래경계;
    static int peikar_X, peikar_Y, peikar_figur;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] peikar_bakgrunn = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void Klargjer(int 폭, int lengd_VALUE) {
        너비 = 폭; 높이 = lengd_VALUE; 합성중 = 0; peikar_figur = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int 높이얻기() { return 높이; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int klipp_VALUE(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int START_VALUE, int lengd_VALUE) {
        if (START_VALUE > 2147483647 - lengd_VALUE) return 2147483647;
        return START_VALUE + lengd_VALUE;
    }
    public static int klipp(int 가로, int vertikalvising_plassere, int 폭, int lengd_VALUE) {
        if (너비 == 0 || 폭 <= 0 || lengd_VALUE <= 0) return 0;
        int RIGHT = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(vertikalvising_plassere, lengd_VALUE);
        int 왼쪽 = 합성중 != 0 ? 왼경계 : 0, 위쪽 = 합성중 != 0 ? 위경계 : 0;
        int 최대가로 = 합성중 != 0 ? 오른경계 : 너비, 최대세로 = 합성중 != 0 ? 아래경계 : 높이;
        if (가로 < 왼쪽) 가로 = 왼쪽;
        if (vertikalvising_plassere < 위쪽) vertikalvising_plassere = 위쪽;
        if (RIGHT > 최대가로) RIGHT = 최대가로;
        if (아래쪽 > 최대세로) 아래쪽 = 최대세로;
        if (RIGHT <= 가로 || 아래쪽 <= vertikalvising_plassere) return 0;
        잘린범위[0] = 가로; 잘린범위[1] = vertikalvising_plassere;
        잘린범위[2] = RIGHT - 가로; 잘린범위[3] = 아래쪽 - vertikalvising_plassere;
        return 1;
    }
    public static int Køyr_2(int 가로, int vertikalvising_plassere, int 폭, int lengd_VALUE) {
        if (합성중 != 0 || lengd_VALUE > 32 || klipp(가로, vertikalvising_plassere, 폭, lengd_VALUE) == 0) return 0;
        왼경계 = 잘린범위[0]; 위경계 = 잘린범위[1];
        오른경계 = 왼경계 + 잘린범위[2]; 아래경계 = 위경계 + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean peikar_bit(int 가로, int vertikalvising_plassere, int figur_VALUE) {
        if (figur_VALUE == 1) return 가로 >= 0 && 가로 <= vertikalvising_plassere / 2 && vertikalvising_plassere < 16;
        if (figur_VALUE == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - vertikalvising_plassere; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && vertikalvising_plassere >= 2 && vertikalvising_plassere <= 8 && (가로 <= 3 || vertikalvising_plassere <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && vertikalvising_plassere >= 12 && vertikalvising_plassere <= 18 && (가로 >= 17 || vertikalvising_plassere >= 17));
    }
    static int peikar_piksel(int 가로, int vertikalvising_plassere) {
        if (peikar_bit(가로, vertikalvising_plassere, peikar_figur)) return 2;
        for (int linje = -1; linje <= 1; linje++) for (int felt_oppføring = -1; felt_oppføring <= 1; felt_oppføring++)
            if (peikar_bit(가로 + felt_oppføring, vertikalvising_plassere + linje, peikar_figur)) return 1;
        return 0;
    }
    static void vise_piksel(int 가로, int vertikalvising_plassere, int 색) {
        int felt_oppføring = 가로 - peikar_X, linje = vertikalvising_plassere - peikar_Y;
        if (peikar_figur != 0 && felt_oppføring >= 0 && linje >= 0 && felt_oppføring < 21 && linje < 21) {
            peikar_bakgrunn[linje * 21 + felt_oppføring] = 색;
            int p_VALUE = peikar_piksel(felt_oppføring, linje); if (p_VALUE != 0) 색 = p_VALUE == 2 ? 0xffffff : 0x101010;
        }
        if (Tavle.표시화소읽기(가로, vertikalvising_plassere) != 색) {
            Tavle.skrive_vise_piksel(가로, vertikalvising_plassere, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void Ferdig() {
        if (합성중 == 0) return;
        for (int linje = 위경계; linje < 아래경계; linje++) for (int felt_oppføring = 왼경계; felt_oppføring < 오른경계; felt_oppføring++)
            vise_piksel(felt_oppføring, linje, 완성그림[(linje - 위경계) * 1920 + felt_oppføring]);
        합성중 = 0;
    }
    public static int piksel(int 가로, int vertikalvising_plassere, int 색) {
        if (가로 < 0 || vertikalvising_plassere < 0 || 가로 >= 너비 || vertikalvising_plassere >= 높이) return 0;
        if (합성중 != 0) {
            if (가로 >= 왼경계 && 가로 < 오른경계 && vertikalvising_plassere >= 위경계 && vertikalvising_plassere < 아래경계)
                완성그림[(vertikalvising_plassere - 위경계) * 1920 + 가로] = 색;
        } else vise_piksel(가로, vertikalvising_plassere, 색);
        return 0;
    }
    public static void 사각그림(int 가로, int vertikalvising_plassere, int 폭, int lengd_VALUE, int 색) {
        if (klipp(가로, vertikalvising_plassere, 폭, lengd_VALUE) == 0) return;
        가로 = 잘린범위[0]; vertikalvising_plassere = 잘린범위[1]; 폭 = 잘린범위[2]; lengd_VALUE = 잘린범위[3];
        for (int linje = vertikalvising_plassere; linje < vertikalvising_plassere + lengd_VALUE; linje++) for (int felt_oppføring = 가로; felt_oppføring < 가로 + 폭; felt_oppføring++) {
            if (합성중 != 0) 완성그림[(linje - 위경계) * 1920 + felt_oppføring] = 색;
            else vise_piksel(felt_oppføring, linje, 색);
        }
    }
    public static void peikar(int 가로, int vertikalvising_plassere, int figur_VALUE) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (figur_VALUE >= 2 ? 10 : 0), 새세로 = vertikalvising_plassere - (figur_VALUE >= 2 ? 10 : 0);
        if (peikar_figur == figur_VALUE && peikar_X == 새가로 && peikar_Y == 새세로) return;
        if (peikar_figur != 0) for (int linje = 0; linje < 21; linje++) for (int felt_oppføring = 0; felt_oppføring < 21; felt_oppføring++) {
            int 가 = peikar_X + felt_oppføring, 세 = peikar_Y + linje;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) Tavle.skrive_vise_piksel(가, 세, peikar_bakgrunn[linje * 21 + felt_oppføring]);
        }
        peikar_figur = figur_VALUE; peikar_X = 새가로; peikar_Y = 새세로;
        if (figur_VALUE != 0) for (int linje = 0; linje < 21; linje++) for (int felt_oppføring = 0; felt_oppføring < 21; felt_oppføring++) {
            int 가 = peikar_X + felt_oppføring, 세 = peikar_Y + linje;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) {
                peikar_bakgrunn[linje * 21 + felt_oppføring] = Tavle.표시화소읽기(가, 세);
                int p_VALUE = peikar_piksel(felt_oppføring, linje); if (p_VALUE != 0) Tavle.skrive_vise_piksel(가, 세, p_VALUE == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
