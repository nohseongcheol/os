// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** skærmbillede klip_VÆRDI·띠 합성·markør 밑그림을 관리한다. faktisk_data skærmbillede Hukommelse_data 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, 높이, 합성중, VENSTRE_grænse_VÆRDI, STORE_BOGSTAVER_grænse, HØJRE_grænse_VÆRDI, SMÅ_BOGSTAVER_grænse_VÆRDI;
    static int markør_X, markør_Y, markør_figur;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] markør_Baggrund = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void Tilrettelæg(int 폭, int varighed_VÆRDI) {
        너비 = 폭; 높이 = varighed_VÆRDI; 합성중 = 0; markør_figur = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int 높이얻기() { return 높이; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int klippe_VÆRDI(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int START_VÆRDI, int varighed_VÆRDI) {
        if (START_VÆRDI > 2147483647 - varighed_VÆRDI) return 2147483647;
        return START_VÆRDI + varighed_VÆRDI;
    }
    public static int klippe(int 가로, int Lodret_placere, int 폭, int varighed_VÆRDI) {
        if (너비 == 0 || 폭 <= 0 || varighed_VÆRDI <= 0) return 0;
        int HØJRE = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(Lodret_placere, varighed_VÆRDI);
        int 왼쪽 = 합성중 != 0 ? VENSTRE_grænse_VÆRDI : 0, 위쪽 = 합성중 != 0 ? STORE_BOGSTAVER_grænse : 0;
        int 최대가로 = 합성중 != 0 ? HØJRE_grænse_VÆRDI : 너비, 최대세로 = 합성중 != 0 ? SMÅ_BOGSTAVER_grænse_VÆRDI : 높이;
        if (가로 < 왼쪽) 가로 = 왼쪽;
        if (Lodret_placere < 위쪽) Lodret_placere = 위쪽;
        if (HØJRE > 최대가로) HØJRE = 최대가로;
        if (아래쪽 > 최대세로) 아래쪽 = 최대세로;
        if (HØJRE <= 가로 || 아래쪽 <= Lodret_placere) return 0;
        잘린범위[0] = 가로; 잘린범위[1] = Lodret_placere;
        잘린범위[2] = HØJRE - 가로; 잘린범위[3] = 아래쪽 - Lodret_placere;
        return 1;
    }
    public static int Kør_2(int 가로, int Lodret_placere, int 폭, int varighed_VÆRDI) {
        if (합성중 != 0 || varighed_VÆRDI > 32 || klippe(가로, Lodret_placere, 폭, varighed_VÆRDI) == 0) return 0;
        VENSTRE_grænse_VÆRDI = 잘린범위[0]; STORE_BOGSTAVER_grænse = 잘린범위[1];
        HØJRE_grænse_VÆRDI = VENSTRE_grænse_VÆRDI + 잘린범위[2]; SMÅ_BOGSTAVER_grænse_VÆRDI = STORE_BOGSTAVER_grænse + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean markør_bit(int 가로, int Lodret_placere, int figur_VÆRDI) {
        if (figur_VÆRDI == 1) return 가로 >= 0 && 가로 <= Lodret_placere / 2 && Lodret_placere < 16;
        if (figur_VÆRDI == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - Lodret_placere; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && Lodret_placere >= 2 && Lodret_placere <= 8 && (가로 <= 3 || Lodret_placere <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && Lodret_placere >= 12 && Lodret_placere <= 18 && (가로 >= 17 || Lodret_placere >= 17));
    }
    static int markør_pixel(int 가로, int Lodret_placere) {
        if (markør_bit(가로, Lodret_placere, markør_figur)) return 2;
        for (int Linje = -1; Linje <= 1; Linje++) for (int udvidelsesstik_post = -1; udvidelsesstik_post <= 1; udvidelsesstik_post++)
            if (markør_bit(가로 + udvidelsesstik_post, Lodret_placere + Linje, markør_figur)) return 1;
        return 0;
    }
    static void vise_pixel(int 가로, int Lodret_placere, int 색) {
        int udvidelsesstik_post = 가로 - markør_X, Linje = Lodret_placere - markør_Y;
        if (markør_figur != 0 && udvidelsesstik_post >= 0 && Linje >= 0 && udvidelsesstik_post < 21 && Linje < 21) {
            markør_Baggrund[Linje * 21 + udvidelsesstik_post] = 색;
            int pege_VÆRDI = markør_pixel(udvidelsesstik_post, Linje); if (pege_VÆRDI != 0) 색 = pege_VÆRDI == 2 ? 0xffffff : 0x101010;
        }
        if (Tavle.표시화소읽기(가로, Lodret_placere) != 색) {
            Tavle.skrive_vise_pixel(가로, Lodret_placere, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void Udfør() {
        if (합성중 == 0) return;
        for (int Linje = STORE_BOGSTAVER_grænse; Linje < SMÅ_BOGSTAVER_grænse_VÆRDI; Linje++) for (int udvidelsesstik_post = VENSTRE_grænse_VÆRDI; udvidelsesstik_post < HØJRE_grænse_VÆRDI; udvidelsesstik_post++)
            vise_pixel(udvidelsesstik_post, Linje, 완성그림[(Linje - STORE_BOGSTAVER_grænse) * 1920 + udvidelsesstik_post]);
        합성중 = 0;
    }
    public static int pixel(int 가로, int Lodret_placere, int 색) {
        if (가로 < 0 || Lodret_placere < 0 || 가로 >= 너비 || Lodret_placere >= 높이) return 0;
        if (합성중 != 0) {
            if (가로 >= VENSTRE_grænse_VÆRDI && 가로 < HØJRE_grænse_VÆRDI && Lodret_placere >= STORE_BOGSTAVER_grænse && Lodret_placere < SMÅ_BOGSTAVER_grænse_VÆRDI)
                완성그림[(Lodret_placere - STORE_BOGSTAVER_grænse) * 1920 + 가로] = 색;
        } else vise_pixel(가로, Lodret_placere, 색);
        return 0;
    }
    public static void rektangel_udfyld(int 가로, int Lodret_placere, int 폭, int varighed_VÆRDI, int 색) {
        if (klippe(가로, Lodret_placere, 폭, varighed_VÆRDI) == 0) return;
        가로 = 잘린범위[0]; Lodret_placere = 잘린범위[1]; 폭 = 잘린범위[2]; varighed_VÆRDI = 잘린범위[3];
        for (int Linje = Lodret_placere; Linje < Lodret_placere + varighed_VÆRDI; Linje++) for (int udvidelsesstik_post = 가로; udvidelsesstik_post < 가로 + 폭; udvidelsesstik_post++) {
            if (합성중 != 0) 완성그림[(Linje - STORE_BOGSTAVER_grænse) * 1920 + udvidelsesstik_post] = 색;
            else vise_pixel(udvidelsesstik_post, Linje, 색);
        }
    }
    public static void markør(int 가로, int Lodret_placere, int figur_VÆRDI) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (figur_VÆRDI >= 2 ? 10 : 0), 새세로 = Lodret_placere - (figur_VÆRDI >= 2 ? 10 : 0);
        if (markør_figur == figur_VÆRDI && markør_X == 새가로 && markør_Y == 새세로) return;
        if (markør_figur != 0) for (int Linje = 0; Linje < 21; Linje++) for (int udvidelsesstik_post = 0; udvidelsesstik_post < 21; udvidelsesstik_post++) {
            int 가 = markør_X + udvidelsesstik_post, 세 = markør_Y + Linje;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) Tavle.skrive_vise_pixel(가, 세, markør_Baggrund[Linje * 21 + udvidelsesstik_post]);
        }
        markør_figur = figur_VÆRDI; markør_X = 새가로; markør_Y = 새세로;
        if (figur_VÆRDI != 0) for (int Linje = 0; Linje < 21; Linje++) for (int udvidelsesstik_post = 0; udvidelsesstik_post < 21; udvidelsesstik_post++) {
            int 가 = markør_X + udvidelsesstik_post, 세 = markør_Y + Linje;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) {
                markør_Baggrund[Linje * 21 + udvidelsesstik_post] = Tavle.표시화소읽기(가, 세);
                int pege_VÆRDI = markør_pixel(udvidelsesstik_post, Linje); if (pege_VÆRDI != 0) Tavle.skrive_vise_pixel(가, 세, pege_VÆRDI == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
