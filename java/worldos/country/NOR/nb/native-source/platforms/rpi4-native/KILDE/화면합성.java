// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** skjermbilde klippe_VERDI_4601577b·띠 합성·peker 밑그림을 관리한다. faktisk_data skjermbilde Minne_data 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, 높이, 합성중, VENSTRE_grense_VERDI, STORE_grense, HØYRE_grense_VERDI, SMÅ_grense_VERDI;
    static int peker_X, peker_Y, peker_figur;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] peker_bakgrunn = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void Forbered(int 폭, int lengde_VERDI) {
        너비 = 폭; 높이 = lengde_VERDI; 합성중 = 0; peker_figur = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int 높이얻기() { return 높이; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int klippe_VERDI(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int START_VERDI, int lengde_VERDI) {
        if (START_VERDI > 2147483647 - lengde_VERDI) return 2147483647;
        return START_VERDI + lengde_VERDI;
    }
    public static int klippe(int 가로, int vertikal_plassere, int 폭, int lengde_VERDI) {
        if (너비 == 0 || 폭 <= 0 || lengde_VERDI <= 0) return 0;
        int HØYRE = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(vertikal_plassere, lengde_VERDI);
        int 왼쪽 = 합성중 != 0 ? VENSTRE_grense_VERDI : 0, 위쪽 = 합성중 != 0 ? STORE_grense : 0;
        int 최대가로 = 합성중 != 0 ? HØYRE_grense_VERDI : 너비, 최대세로 = 합성중 != 0 ? SMÅ_grense_VERDI : 높이;
        if (가로 < 왼쪽) 가로 = 왼쪽;
        if (vertikal_plassere < 위쪽) vertikal_plassere = 위쪽;
        if (HØYRE > 최대가로) HØYRE = 최대가로;
        if (아래쪽 > 최대세로) 아래쪽 = 최대세로;
        if (HØYRE <= 가로 || 아래쪽 <= vertikal_plassere) return 0;
        잘린범위[0] = 가로; 잘린범위[1] = vertikal_plassere;
        잘린범위[2] = HØYRE - 가로; 잘린범위[3] = 아래쪽 - vertikal_plassere;
        return 1;
    }
    public static int Kjør_2(int 가로, int vertikal_plassere, int 폭, int lengde_VERDI) {
        if (합성중 != 0 || lengde_VERDI > 32 || klippe(가로, vertikal_plassere, 폭, lengde_VERDI) == 0) return 0;
        VENSTRE_grense_VERDI = 잘린범위[0]; STORE_grense = 잘린범위[1];
        HØYRE_grense_VERDI = VENSTRE_grense_VERDI + 잘린범위[2]; SMÅ_grense_VERDI = STORE_grense + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean peker_bit(int 가로, int vertikal_plassere, int figur_VERDI) {
        if (figur_VERDI == 1) return 가로 >= 0 && 가로 <= vertikal_plassere / 2 && vertikal_plassere < 16;
        if (figur_VERDI == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - vertikal_plassere; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && vertikal_plassere >= 2 && vertikal_plassere <= 8 && (가로 <= 3 || vertikal_plassere <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && vertikal_plassere >= 12 && vertikal_plassere <= 18 && (가로 >= 17 || vertikal_plassere >= 17));
    }
    static int peker_piksel(int 가로, int vertikal_plassere) {
        if (peker_bit(가로, vertikal_plassere, peker_figur)) return 2;
        for (int Linje = -1; Linje <= 1; Linje++) for (int åpning_oppføring = -1; åpning_oppføring <= 1; åpning_oppføring++)
            if (peker_bit(가로 + åpning_oppføring, vertikal_plassere + Linje, peker_figur)) return 1;
        return 0;
    }
    static void vise_piksel(int 가로, int vertikal_plassere, int 색) {
        int åpning_oppføring = 가로 - peker_X, Linje = vertikal_plassere - peker_Y;
        if (peker_figur != 0 && åpning_oppføring >= 0 && Linje >= 0 && åpning_oppføring < 21 && Linje < 21) {
            peker_bakgrunn[Linje * 21 + åpning_oppføring] = 색;
            int peke_VERDI = peker_piksel(åpning_oppføring, Linje); if (peke_VERDI != 0) 색 = peke_VERDI == 2 ? 0xffffff : 0x101010;
        }
        if (Tavle.표시화소읽기(가로, vertikal_plassere) != 색) {
            Tavle.skrive_vise_piksel(가로, vertikal_plassere, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void slutt() {
        if (합성중 == 0) return;
        for (int Linje = STORE_grense; Linje < SMÅ_grense_VERDI; Linje++) for (int åpning_oppføring = VENSTRE_grense_VERDI; åpning_oppføring < HØYRE_grense_VERDI; åpning_oppføring++)
            vise_piksel(åpning_oppføring, Linje, 완성그림[(Linje - STORE_grense) * 1920 + åpning_oppføring]);
        합성중 = 0;
    }
    public static int piksel(int 가로, int vertikal_plassere, int 색) {
        if (가로 < 0 || vertikal_plassere < 0 || 가로 >= 너비 || vertikal_plassere >= 높이) return 0;
        if (합성중 != 0) {
            if (가로 >= VENSTRE_grense_VERDI && 가로 < HØYRE_grense_VERDI && vertikal_plassere >= STORE_grense && vertikal_plassere < SMÅ_grense_VERDI)
                완성그림[(vertikal_plassere - STORE_grense) * 1920 + 가로] = 색;
        } else vise_piksel(가로, vertikal_plassere, 색);
        return 0;
    }
    public static void rektangel_fyll(int 가로, int vertikal_plassere, int 폭, int lengde_VERDI, int 색) {
        if (klippe(가로, vertikal_plassere, 폭, lengde_VERDI) == 0) return;
        가로 = 잘린범위[0]; vertikal_plassere = 잘린범위[1]; 폭 = 잘린범위[2]; lengde_VERDI = 잘린범위[3];
        for (int Linje = vertikal_plassere; Linje < vertikal_plassere + lengde_VERDI; Linje++) for (int åpning_oppføring = 가로; åpning_oppføring < 가로 + 폭; åpning_oppføring++) {
            if (합성중 != 0) 완성그림[(Linje - STORE_grense) * 1920 + åpning_oppføring] = 색;
            else vise_piksel(åpning_oppføring, Linje, 색);
        }
    }
    public static void peker(int 가로, int vertikal_plassere, int figur_VERDI) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (figur_VERDI >= 2 ? 10 : 0), 새세로 = vertikal_plassere - (figur_VERDI >= 2 ? 10 : 0);
        if (peker_figur == figur_VERDI && peker_X == 새가로 && peker_Y == 새세로) return;
        if (peker_figur != 0) for (int Linje = 0; Linje < 21; Linje++) for (int åpning_oppføring = 0; åpning_oppføring < 21; åpning_oppføring++) {
            int 가 = peker_X + åpning_oppføring, 세 = peker_Y + Linje;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) Tavle.skrive_vise_piksel(가, 세, peker_bakgrunn[Linje * 21 + åpning_oppføring]);
        }
        peker_figur = figur_VERDI; peker_X = 새가로; peker_Y = 새세로;
        if (figur_VERDI != 0) for (int Linje = 0; Linje < 21; Linje++) for (int åpning_oppføring = 0; åpning_oppføring < 21; åpning_oppføring++) {
            int 가 = peker_X + åpning_oppføring, 세 = peker_Y + Linje;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) {
                peker_bakgrunn[Linje * 21 + åpning_oppføring] = Tavle.표시화소읽기(가, 세);
                int peke_VERDI = peker_piksel(åpning_oppføring, Linje); if (peke_VERDI != 0) Tavle.skrive_vise_piksel(가, 세, peke_VERDI == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
