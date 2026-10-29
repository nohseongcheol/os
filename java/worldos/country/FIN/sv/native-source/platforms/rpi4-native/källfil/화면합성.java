// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** skärmbild klippa_värde·띠 합성·markör 밑그림을 관리한다. verklig_data skärmbild Minne_data 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, 높이, 합성중, VÄNSTER_gräns_värde, VERSALER_gräns, HÖGER_gräns_värde, GEMENER_gräns_värde;
    static int markör_X, markör_Y, markör_form;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] markör_Bakgrund = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void Förbereda(int 폭, int längd_värde) {
        너비 = 폭; 높이 = längd_värde; 합성중 = 0; markör_form = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int 높이얻기() { return 높이; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int klipp_värde(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int START_värde, int längd_värde) {
        if (START_värde > 2147483647 - längd_värde) return 2147483647;
        return START_värde + längd_värde;
    }
    public static int klipp(int 가로, int bransch_placera, int 폭, int längd_värde) {
        if (너비 == 0 || 폭 <= 0 || längd_värde <= 0) return 0;
        int HÖGER = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(bransch_placera, längd_värde);
        int 왼쪽 = 합성중 != 0 ? VÄNSTER_gräns_värde : 0, 위쪽 = 합성중 != 0 ? VERSALER_gräns : 0;
        int 최대가로 = 합성중 != 0 ? HÖGER_gräns_värde : 너비, 최대세로 = 합성중 != 0 ? GEMENER_gräns_värde : 높이;
        if (가로 < 왼쪽) 가로 = 왼쪽;
        if (bransch_placera < 위쪽) bransch_placera = 위쪽;
        if (HÖGER > 최대가로) HÖGER = 최대가로;
        if (아래쪽 > 최대세로) 아래쪽 = 최대세로;
        if (HÖGER <= 가로 || 아래쪽 <= bransch_placera) return 0;
        잘린범위[0] = 가로; 잘린범위[1] = bransch_placera;
        잘린범위[2] = HÖGER - 가로; 잘린범위[3] = 아래쪽 - bransch_placera;
        return 1;
    }
    public static int Kör(int 가로, int bransch_placera, int 폭, int längd_värde) {
        if (합성중 != 0 || längd_värde > 32 || klipp(가로, bransch_placera, 폭, längd_värde) == 0) return 0;
        VÄNSTER_gräns_värde = 잘린범위[0]; VERSALER_gräns = 잘린범위[1];
        HÖGER_gräns_värde = VÄNSTER_gräns_värde + 잘린범위[2]; GEMENER_gräns_värde = VERSALER_gräns + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean markör_bit(int 가로, int bransch_placera, int form_värde) {
        if (form_värde == 1) return 가로 >= 0 && 가로 <= bransch_placera / 2 && bransch_placera < 16;
        if (form_värde == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - bransch_placera; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && bransch_placera >= 2 && bransch_placera <= 8 && (가로 <= 3 || bransch_placera <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && bransch_placera >= 12 && bransch_placera <= 18 && (가로 >= 17 || bransch_placera >= 17));
    }
    static int markör_bildpunkt(int 가로, int bransch_placera) {
        if (markör_bit(가로, bransch_placera, markör_form)) return 2;
        for (int inmatningsrad = -1; inmatningsrad <= 1; inmatningsrad++) for (int fack_post = -1; fack_post <= 1; fack_post++)
            if (markör_bit(가로 + fack_post, bransch_placera + inmatningsrad, markör_form)) return 1;
        return 0;
    }
    static void visa_bildpunkt(int 가로, int bransch_placera, int 색) {
        int fack_post = 가로 - markör_X, inmatningsrad = bransch_placera - markör_Y;
        if (markör_form != 0 && fack_post >= 0 && inmatningsrad >= 0 && fack_post < 21 && inmatningsrad < 21) {
            markör_Bakgrund[inmatningsrad * 21 + fack_post] = 색;
            int peka_värde = markör_bildpunkt(fack_post, inmatningsrad); if (peka_värde != 0) 색 = peka_värde == 2 ? 0xffffff : 0x101010;
        }
        if (Tavla.läsa_visa_bildpunkt(가로, bransch_placera) != 색) {
            Tavla.skriva_visa_bildpunkt(가로, bransch_placera, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void slut() {
        if (합성중 == 0) return;
        for (int inmatningsrad = VERSALER_gräns; inmatningsrad < GEMENER_gräns_värde; inmatningsrad++) for (int fack_post = VÄNSTER_gräns_värde; fack_post < HÖGER_gräns_värde; fack_post++)
            visa_bildpunkt(fack_post, inmatningsrad, 완성그림[(inmatningsrad - VERSALER_gräns) * 1920 + fack_post]);
        합성중 = 0;
    }
    public static int bildpunkt(int 가로, int bransch_placera, int 색) {
        if (가로 < 0 || bransch_placera < 0 || 가로 >= 너비 || bransch_placera >= 높이) return 0;
        if (합성중 != 0) {
            if (가로 >= VÄNSTER_gräns_värde && 가로 < HÖGER_gräns_värde && bransch_placera >= VERSALER_gräns && bransch_placera < GEMENER_gräns_värde)
                완성그림[(bransch_placera - VERSALER_gräns) * 1920 + 가로] = 색;
        } else visa_bildpunkt(가로, bransch_placera, 색);
        return 0;
    }
    public static void rektangel_Fyll(int 가로, int bransch_placera, int 폭, int längd_värde, int 색) {
        if (klipp(가로, bransch_placera, 폭, längd_värde) == 0) return;
        가로 = 잘린범위[0]; bransch_placera = 잘린범위[1]; 폭 = 잘린범위[2]; längd_värde = 잘린범위[3];
        for (int inmatningsrad = bransch_placera; inmatningsrad < bransch_placera + längd_värde; inmatningsrad++) for (int fack_post = 가로; fack_post < 가로 + 폭; fack_post++) {
            if (합성중 != 0) 완성그림[(inmatningsrad - VERSALER_gräns) * 1920 + fack_post] = 색;
            else visa_bildpunkt(fack_post, inmatningsrad, 색);
        }
    }
    public static void markör(int 가로, int bransch_placera, int form_värde) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (form_värde >= 2 ? 10 : 0), 새세로 = bransch_placera - (form_värde >= 2 ? 10 : 0);
        if (markör_form == form_värde && markör_X == 새가로 && markör_Y == 새세로) return;
        if (markör_form != 0) for (int inmatningsrad = 0; inmatningsrad < 21; inmatningsrad++) for (int fack_post = 0; fack_post < 21; fack_post++) {
            int 가 = markör_X + fack_post, 세 = markör_Y + inmatningsrad;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) Tavla.skriva_visa_bildpunkt(가, 세, markör_Bakgrund[inmatningsrad * 21 + fack_post]);
        }
        markör_form = form_värde; markör_X = 새가로; markör_Y = 새세로;
        if (form_värde != 0) for (int inmatningsrad = 0; inmatningsrad < 21; inmatningsrad++) for (int fack_post = 0; fack_post < 21; fack_post++) {
            int 가 = markör_X + fack_post, 세 = markör_Y + inmatningsrad;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) {
                markör_Bakgrund[inmatningsrad * 21 + fack_post] = Tavla.läsa_visa_bildpunkt(가, 세);
                int peka_värde = markör_bildpunkt(fack_post, inmatningsrad); if (peka_värde != 0) Tavla.skriva_visa_bildpunkt(가, 세, peka_värde == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
