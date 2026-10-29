// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 화면 klippa_VALUE·띠 합성·bendill 밑그림을 관리한다. raun_gögn 화면 Minni_gögn 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, 높이, 합성중, 왼경계, 위경계, 오른경계, 아래경계;
    static int bendill_X, bendill_Y, bendill_form;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] bendill_veggfóður = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void Undirbúa(int 폭, int lengd_VALUE) {
        너비 = 폭; 높이 = lengd_VALUE; 합성중 = 0; bendill_form = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int 높이얻기() { return 높이; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int miðlaskrá_VALUE(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int Opna_VALUE, int lengd_VALUE) {
        if (Opna_VALUE > 2147483647 - lengd_VALUE) return 2147483647;
        return Opna_VALUE + lengd_VALUE;
    }
    public static int miðlaskrá(int 가로, int Lóðrétt_staða, int 폭, int lengd_VALUE) {
        if (너비 == 0 || 폭 <= 0 || lengd_VALUE <= 0) return 0;
        int RIGHT = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(Lóðrétt_staða, lengd_VALUE);
        int 왼쪽 = 합성중 != 0 ? 왼경계 : 0, 위쪽 = 합성중 != 0 ? 위경계 : 0;
        int 최대가로 = 합성중 != 0 ? 오른경계 : 너비, 최대세로 = 합성중 != 0 ? 아래경계 : 높이;
        if (가로 < 왼쪽) 가로 = 왼쪽;
        if (Lóðrétt_staða < 위쪽) Lóðrétt_staða = 위쪽;
        if (RIGHT > 최대가로) RIGHT = 최대가로;
        if (아래쪽 > 최대세로) 아래쪽 = 최대세로;
        if (RIGHT <= 가로 || 아래쪽 <= Lóðrétt_staða) return 0;
        잘린범위[0] = 가로; 잘린범위[1] = Lóðrétt_staða;
        잘린범위[2] = RIGHT - 가로; 잘린범위[3] = 아래쪽 - Lóðrétt_staða;
        return 1;
    }
    public static int Keyra_2(int 가로, int Lóðrétt_staða, int 폭, int lengd_VALUE) {
        if (합성중 != 0 || lengd_VALUE > 32 || miðlaskrá(가로, Lóðrétt_staða, 폭, lengd_VALUE) == 0) return 0;
        왼경계 = 잘린범위[0]; 위경계 = 잘린범위[1];
        오른경계 = 왼경계 + 잘린범위[2]; 아래경계 = 위경계 + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean bendill_biti(int 가로, int Lóðrétt_staða, int form_VALUE) {
        if (form_VALUE == 1) return 가로 >= 0 && 가로 <= Lóðrétt_staða / 2 && Lóðrétt_staða < 16;
        if (form_VALUE == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - Lóðrétt_staða; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && Lóðrétt_staða >= 2 && Lóðrétt_staða <= 8 && (가로 <= 3 || Lóðrétt_staða <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && Lóðrétt_staða >= 12 && Lóðrétt_staða <= 18 && (가로 >= 17 || Lóðrétt_staða >= 17));
    }
    static int bendill_díll(int 가로, int Lóðrétt_staða) {
        if (bendill_biti(가로, Lóðrétt_staða, bendill_form)) return 2;
        for (int Lína = -1; Lína <= 1; Lína++) for (int rauf_færsla = -1; rauf_færsla <= 1; rauf_færsla++)
            if (bendill_biti(가로 + rauf_færsla, Lóðrétt_staða + Lína, bendill_form)) return 1;
        return 0;
    }
    static void birta_díll(int 가로, int Lóðrétt_staða, int 색) {
        int rauf_færsla = 가로 - bendill_X, Lína = Lóðrétt_staða - bendill_Y;
        if (bendill_form != 0 && rauf_færsla >= 0 && Lína >= 0 && rauf_færsla < 21 && Lína < 21) {
            bendill_veggfóður[Lína * 21 + rauf_færsla] = 색;
            int P_VALUE = bendill_díll(rauf_færsla, Lína); if (P_VALUE != 0) 색 = P_VALUE == 2 ? 0xffffff : 0x101010;
        }
        if (bretti.표시화소읽기(가로, Lóðrétt_staða) != 색) {
            bretti.skrifa_birta_díll(가로, Lóðrétt_staða, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void Ljúka() {
        if (합성중 == 0) return;
        for (int Lína = 위경계; Lína < 아래경계; Lína++) for (int rauf_færsla = 왼경계; rauf_færsla < 오른경계; rauf_færsla++)
            birta_díll(rauf_færsla, Lína, 완성그림[(Lína - 위경계) * 1920 + rauf_færsla]);
        합성중 = 0;
    }
    public static int díll(int 가로, int Lóðrétt_staða, int 색) {
        if (가로 < 0 || Lóðrétt_staða < 0 || 가로 >= 너비 || Lóðrétt_staða >= 높이) return 0;
        if (합성중 != 0) {
            if (가로 >= 왼경계 && 가로 < 오른경계 && Lóðrétt_staða >= 위경계 && Lóðrétt_staða < 아래경계)
                완성그림[(Lóðrétt_staða - 위경계) * 1920 + 가로] = 색;
        } else birta_díll(가로, Lóðrétt_staða, 색);
        return 0;
    }
    public static void 사각그림(int 가로, int Lóðrétt_staða, int 폭, int lengd_VALUE, int 색) {
        if (miðlaskrá(가로, Lóðrétt_staða, 폭, lengd_VALUE) == 0) return;
        가로 = 잘린범위[0]; Lóðrétt_staða = 잘린범위[1]; 폭 = 잘린범위[2]; lengd_VALUE = 잘린범위[3];
        for (int Lína = Lóðrétt_staða; Lína < Lóðrétt_staða + lengd_VALUE; Lína++) for (int rauf_færsla = 가로; rauf_færsla < 가로 + 폭; rauf_færsla++) {
            if (합성중 != 0) 완성그림[(Lína - 위경계) * 1920 + rauf_færsla] = 색;
            else birta_díll(rauf_færsla, Lína, 색);
        }
    }
    public static void bendill(int 가로, int Lóðrétt_staða, int form_VALUE) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (form_VALUE >= 2 ? 10 : 0), 새세로 = Lóðrétt_staða - (form_VALUE >= 2 ? 10 : 0);
        if (bendill_form == form_VALUE && bendill_X == 새가로 && bendill_Y == 새세로) return;
        if (bendill_form != 0) for (int Lína = 0; Lína < 21; Lína++) for (int rauf_færsla = 0; rauf_færsla < 21; rauf_færsla++) {
            int 가 = bendill_X + rauf_færsla, 세 = bendill_Y + Lína;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) bretti.skrifa_birta_díll(가, 세, bendill_veggfóður[Lína * 21 + rauf_færsla]);
        }
        bendill_form = form_VALUE; bendill_X = 새가로; bendill_Y = 새세로;
        if (form_VALUE != 0) for (int Lína = 0; Lína < 21; Lína++) for (int rauf_færsla = 0; rauf_færsla < 21; rauf_færsla++) {
            int 가 = bendill_X + rauf_færsla, 세 = bendill_Y + Lína;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) {
                bendill_veggfóður[Lína * 21 + rauf_færsla] = bretti.표시화소읽기(가, 세);
                int P_VALUE = bendill_díll(rauf_færsla, Lína); if (P_VALUE != 0) bretti.skrifa_birta_díll(가, 세, P_VALUE == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
