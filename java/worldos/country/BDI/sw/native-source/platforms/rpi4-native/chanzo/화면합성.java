// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 화면 kata_thamani·띠 합성·kielekezi 밑그림을 관리한다. halisi_data 화면 kumbukumbu_data 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, 높이, 합성중, 왼경계, 위경계, 오른경계, 아래경계;
    static int kielekezi_Kitufe_cha_X, kielekezi_Kitufe_cha_Y, kielekezi_umbo;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] kielekezi_nyuma = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void Andaa(int 폭, int urefu_thamani) {
        너비 = 폭; 높이 = urefu_thamani; 합성중 = 0; kielekezi_umbo = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int 높이얻기() { return 높이; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int dondoo_thamani(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int Anza_thamani, int urefu_thamani) {
        if (Anza_thamani > 2147483647 - urefu_thamani) return 2147483647;
        return Anza_thamani + urefu_thamani;
    }
    public static int dondoo(int 가로, int 세로, int 폭, int urefu_thamani) {
        if (너비 == 0 || 폭 <= 0 || urefu_thamani <= 0) return 0;
        int 오른쪽 = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(세로, urefu_thamani);
        int 왼쪽 = 합성중 != 0 ? 왼경계 : 0, 위쪽 = 합성중 != 0 ? 위경계 : 0;
        int 최대가로 = 합성중 != 0 ? 오른경계 : 너비, 최대세로 = 합성중 != 0 ? 아래경계 : 높이;
        if (가로 < 왼쪽) 가로 = 왼쪽;
        if (세로 < 위쪽) 세로 = 위쪽;
        if (오른쪽 > 최대가로) 오른쪽 = 최대가로;
        if (아래쪽 > 최대세로) 아래쪽 = 최대세로;
        if (오른쪽 <= 가로 || 아래쪽 <= 세로) return 0;
        잘린범위[0] = 가로; 잘린범위[1] = 세로;
        잘린범위[2] = 오른쪽 - 가로; 잘린범위[3] = 아래쪽 - 세로;
        return 1;
    }
    public static int endesha(int 가로, int 세로, int 폭, int urefu_thamani) {
        if (합성중 != 0 || urefu_thamani > 32 || dondoo(가로, 세로, 폭, urefu_thamani) == 0) return 0;
        왼경계 = 잘린범위[0]; 위경계 = 잘린범위[1];
        오른경계 = 왼경계 + 잘린범위[2]; 아래경계 = 위경계 + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean kielekezi_biti(int 가로, int 세로, int umbo_thamani) {
        if (umbo_thamani == 1) return 가로 >= 0 && 가로 <= 세로 / 2 && 세로 < 16;
        if (umbo_thamani == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - 세로; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && 세로 >= 2 && 세로 <= 8 && (가로 <= 3 || 세로 <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && 세로 >= 12 && 세로 <= 18 && (가로 >= 17 || 세로 >= 17));
    }
    static int kielekezi_elepi(int 가로, int 세로) {
        if (kielekezi_biti(가로, 세로, kielekezi_umbo)) return 2;
        for (int laini = -1; laini <= 1; laini++) for (int Sloti_ingizo = -1; Sloti_ingizo <= 1; Sloti_ingizo++)
            if (kielekezi_biti(가로 + Sloti_ingizo, 세로 + laini, kielekezi_umbo)) return 1;
        return 0;
    }
    static void onyesha_elepi(int 가로, int 세로, int 색) {
        int Sloti_ingizo = 가로 - kielekezi_Kitufe_cha_X, laini = 세로 - kielekezi_Kitufe_cha_Y;
        if (kielekezi_umbo != 0 && Sloti_ingizo >= 0 && laini >= 0 && Sloti_ingizo < 21 && laini < 21) {
            kielekezi_nyuma[laini * 21 + Sloti_ingizo] = 색;
            int pointi_thamani = kielekezi_elepi(Sloti_ingizo, laini); if (pointi_thamani != 0) 색 = pointi_thamani == 2 ? 0xffffff : 0x101010;
        }
        if (보드.표시화소읽기(가로, 세로) != 색) {
            보드.andika_onyesha_elepi(가로, 세로, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void Maliza() {
        if (합성중 == 0) return;
        for (int laini = 위경계; laini < 아래경계; laini++) for (int Sloti_ingizo = 왼경계; Sloti_ingizo < 오른경계; Sloti_ingizo++)
            onyesha_elepi(Sloti_ingizo, laini, 완성그림[(laini - 위경계) * 1920 + Sloti_ingizo]);
        합성중 = 0;
    }
    public static int elepi(int 가로, int 세로, int 색) {
        if (가로 < 0 || 세로 < 0 || 가로 >= 너비 || 세로 >= 높이) return 0;
        if (합성중 != 0) {
            if (가로 >= 왼경계 && 가로 < 오른경계 && 세로 >= 위경계 && 세로 < 아래경계)
                완성그림[(세로 - 위경계) * 1920 + 가로] = 색;
        } else onyesha_elepi(가로, 세로, 색);
        return 0;
    }
    public static void 사각그림(int 가로, int 세로, int 폭, int urefu_thamani, int 색) {
        if (dondoo(가로, 세로, 폭, urefu_thamani) == 0) return;
        가로 = 잘린범위[0]; 세로 = 잘린범위[1]; 폭 = 잘린범위[2]; urefu_thamani = 잘린범위[3];
        for (int laini = 세로; laini < 세로 + urefu_thamani; laini++) for (int Sloti_ingizo = 가로; Sloti_ingizo < 가로 + 폭; Sloti_ingizo++) {
            if (합성중 != 0) 완성그림[(laini - 위경계) * 1920 + Sloti_ingizo] = 색;
            else onyesha_elepi(Sloti_ingizo, laini, 색);
        }
    }
    public static void kielekezi(int 가로, int 세로, int umbo_thamani) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (umbo_thamani >= 2 ? 10 : 0), 새세로 = 세로 - (umbo_thamani >= 2 ? 10 : 0);
        if (kielekezi_umbo == umbo_thamani && kielekezi_Kitufe_cha_X == 새가로 && kielekezi_Kitufe_cha_Y == 새세로) return;
        if (kielekezi_umbo != 0) for (int laini = 0; laini < 21; laini++) for (int Sloti_ingizo = 0; Sloti_ingizo < 21; Sloti_ingizo++) {
            int 가 = kielekezi_Kitufe_cha_X + Sloti_ingizo, 세 = kielekezi_Kitufe_cha_Y + laini;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) 보드.andika_onyesha_elepi(가, 세, kielekezi_nyuma[laini * 21 + Sloti_ingizo]);
        }
        kielekezi_umbo = umbo_thamani; kielekezi_Kitufe_cha_X = 새가로; kielekezi_Kitufe_cha_Y = 새세로;
        if (umbo_thamani != 0) for (int laini = 0; laini < 21; laini++) for (int Sloti_ingizo = 0; Sloti_ingizo < 21; Sloti_ingizo++) {
            int 가 = kielekezi_Kitufe_cha_X + Sloti_ingizo, 세 = kielekezi_Kitufe_cha_Y + laini;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) {
                kielekezi_nyuma[laini * 21 + Sloti_ingizo] = 보드.표시화소읽기(가, 세);
                int pointi_thamani = kielekezi_elepi(Sloti_ingizo, laini); if (pointi_thamani != 0) 보드.andika_onyesha_elepi(가, 세, pointi_thamani == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
