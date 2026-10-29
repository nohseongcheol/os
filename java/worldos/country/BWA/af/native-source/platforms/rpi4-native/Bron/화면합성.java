// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 화면 sny_VALUE·띠 합성·wyser 밑그림을 관리한다. werklik_data 화면 Geheue_data 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, 높이, 합성중, 왼경계, 위경계, 오른경계, 아래경계;
    static int wyser_X, wyser_Y, wyser_vorm;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] wyser_muur = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void Maak_gereed(int 폭, int lengte_VALUE) {
        너비 = 폭; 높이 = lengte_VALUE; 합성중 = 0; wyser_vorm = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int 높이얻기() { return 높이; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int snit_VALUE(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int BEGIN_VALUE, int lengte_VALUE) {
        if (BEGIN_VALUE > 2147483647 - lengte_VALUE) return 2147483647;
        return BEGIN_VALUE + lengte_VALUE;
    }
    public static int snit(int 가로, int Vertikaal_plaas, int 폭, int lengte_VALUE) {
        if (너비 == 0 || 폭 <= 0 || lengte_VALUE <= 0) return 0;
        int RIGHT = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(Vertikaal_plaas, lengte_VALUE);
        int 왼쪽 = 합성중 != 0 ? 왼경계 : 0, 위쪽 = 합성중 != 0 ? 위경계 : 0;
        int 최대가로 = 합성중 != 0 ? 오른경계 : 너비, 최대세로 = 합성중 != 0 ? 아래경계 : 높이;
        if (가로 < 왼쪽) 가로 = 왼쪽;
        if (Vertikaal_plaas < 위쪽) Vertikaal_plaas = 위쪽;
        if (RIGHT > 최대가로) RIGHT = 최대가로;
        if (아래쪽 > 최대세로) 아래쪽 = 최대세로;
        if (RIGHT <= 가로 || 아래쪽 <= Vertikaal_plaas) return 0;
        잘린범위[0] = 가로; 잘린범위[1] = Vertikaal_plaas;
        잘린범위[2] = RIGHT - 가로; 잘린범위[3] = 아래쪽 - Vertikaal_plaas;
        return 1;
    }
    public static int Loop(int 가로, int Vertikaal_plaas, int 폭, int lengte_VALUE) {
        if (합성중 != 0 || lengte_VALUE > 32 || snit(가로, Vertikaal_plaas, 폭, lengte_VALUE) == 0) return 0;
        왼경계 = 잘린범위[0]; 위경계 = 잘린범위[1];
        오른경계 = 왼경계 + 잘린범위[2]; 아래경계 = 위경계 + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean wyser_bis(int 가로, int Vertikaal_plaas, int vorm_VALUE) {
        if (vorm_VALUE == 1) return 가로 >= 0 && 가로 <= Vertikaal_plaas / 2 && Vertikaal_plaas < 16;
        if (vorm_VALUE == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - Vertikaal_plaas; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && Vertikaal_plaas >= 2 && Vertikaal_plaas <= 8 && (가로 <= 3 || Vertikaal_plaas <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && Vertikaal_plaas >= 12 && Vertikaal_plaas <= 18 && (가로 >= 17 || Vertikaal_plaas >= 17));
    }
    static int wyser_pieksel(int 가로, int Vertikaal_plaas) {
        if (wyser_bis(가로, Vertikaal_plaas, wyser_vorm)) return 2;
        for (int lyn = -1; lyn <= 1; lyn++) for (int gleuf_inskrywing = -1; gleuf_inskrywing <= 1; gleuf_inskrywing++)
            if (wyser_bis(가로 + gleuf_inskrywing, Vertikaal_plaas + lyn, wyser_vorm)) return 1;
        return 0;
    }
    static void wys_pieksel(int 가로, int Vertikaal_plaas, int 색) {
        int gleuf_inskrywing = 가로 - wyser_X, lyn = Vertikaal_plaas - wyser_Y;
        if (wyser_vorm != 0 && gleuf_inskrywing >= 0 && lyn >= 0 && gleuf_inskrywing < 21 && lyn < 21) {
            wyser_muur[lyn * 21 + gleuf_inskrywing] = 색;
            int p_VALUE = wyser_pieksel(gleuf_inskrywing, lyn); if (p_VALUE != 0) 색 = p_VALUE == 2 ? 0xffffff : 0x101010;
        }
        if (bord.표시화소읽기(가로, Vertikaal_plaas) != 색) {
            bord.skryf_wys_pieksel(가로, Vertikaal_plaas, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void Klaar() {
        if (합성중 == 0) return;
        for (int lyn = 위경계; lyn < 아래경계; lyn++) for (int gleuf_inskrywing = 왼경계; gleuf_inskrywing < 오른경계; gleuf_inskrywing++)
            wys_pieksel(gleuf_inskrywing, lyn, 완성그림[(lyn - 위경계) * 1920 + gleuf_inskrywing]);
        합성중 = 0;
    }
    public static int pieksel(int 가로, int Vertikaal_plaas, int 색) {
        if (가로 < 0 || Vertikaal_plaas < 0 || 가로 >= 너비 || Vertikaal_plaas >= 높이) return 0;
        if (합성중 != 0) {
            if (가로 >= 왼경계 && 가로 < 오른경계 && Vertikaal_plaas >= 위경계 && Vertikaal_plaas < 아래경계)
                완성그림[(Vertikaal_plaas - 위경계) * 1920 + 가로] = 색;
        } else wys_pieksel(가로, Vertikaal_plaas, 색);
        return 0;
    }
    public static void 사각그림(int 가로, int Vertikaal_plaas, int 폭, int lengte_VALUE, int 색) {
        if (snit(가로, Vertikaal_plaas, 폭, lengte_VALUE) == 0) return;
        가로 = 잘린범위[0]; Vertikaal_plaas = 잘린범위[1]; 폭 = 잘린범위[2]; lengte_VALUE = 잘린범위[3];
        for (int lyn = Vertikaal_plaas; lyn < Vertikaal_plaas + lengte_VALUE; lyn++) for (int gleuf_inskrywing = 가로; gleuf_inskrywing < 가로 + 폭; gleuf_inskrywing++) {
            if (합성중 != 0) 완성그림[(lyn - 위경계) * 1920 + gleuf_inskrywing] = 색;
            else wys_pieksel(gleuf_inskrywing, lyn, 색);
        }
    }
    public static void wyser(int 가로, int Vertikaal_plaas, int vorm_VALUE) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (vorm_VALUE >= 2 ? 10 : 0), 새세로 = Vertikaal_plaas - (vorm_VALUE >= 2 ? 10 : 0);
        if (wyser_vorm == vorm_VALUE && wyser_X == 새가로 && wyser_Y == 새세로) return;
        if (wyser_vorm != 0) for (int lyn = 0; lyn < 21; lyn++) for (int gleuf_inskrywing = 0; gleuf_inskrywing < 21; gleuf_inskrywing++) {
            int 가 = wyser_X + gleuf_inskrywing, 세 = wyser_Y + lyn;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) bord.skryf_wys_pieksel(가, 세, wyser_muur[lyn * 21 + gleuf_inskrywing]);
        }
        wyser_vorm = vorm_VALUE; wyser_X = 새가로; wyser_Y = 새세로;
        if (vorm_VALUE != 0) for (int lyn = 0; lyn < 21; lyn++) for (int gleuf_inskrywing = 0; gleuf_inskrywing < 21; gleuf_inskrywing++) {
            int 가 = wyser_X + gleuf_inskrywing, 세 = wyser_Y + lyn;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) {
                wyser_muur[lyn * 21 + gleuf_inskrywing] = bord.표시화소읽기(가, 세);
                int p_VALUE = wyser_pieksel(gleuf_inskrywing, lyn); if (p_VALUE != 0) bord.skryf_wys_pieksel(가, 세, p_VALUE == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
