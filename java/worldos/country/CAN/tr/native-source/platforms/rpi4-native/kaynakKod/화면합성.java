// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 화면 kesmek_değer·띠 합성·işaretçi 밑그림을 관리한다. fiili_veri 화면 Bellek_veri 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, 높이, 합성중, SOLDAN_sınır_değer, BÜYÜKHARF_sınır, hak_sınır_değer, KÜÇÜKHARF_sınır_değer;
    static int işaretçi_X, işaretçi_Y, işaretçi_şekil;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] işaretçi_Arka_Plan = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void Hazırlan(int 폭, int süre_değer) {
        너비 = 폭; 높이 = süre_değer; 합성중 = 0; işaretçi_şekil = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int 높이얻기() { return 높이; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int klip_değer(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int Start_değer, int süre_değer) {
        if (Start_değer > 2147483647 - süre_değer) return 2147483647;
        return Start_değer + süre_değer;
    }
    public static int klip(int 가로, int Dikey_konum, int 폭, int süre_değer) {
        if (너비 == 0 || 폭 <= 0 || süre_değer <= 0) return 0;
        int hak = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(Dikey_konum, süre_değer);
        int 왼쪽 = 합성중 != 0 ? SOLDAN_sınır_değer : 0, 위쪽 = 합성중 != 0 ? BÜYÜKHARF_sınır : 0;
        int 최대가로 = 합성중 != 0 ? hak_sınır_değer : 너비, 최대세로 = 합성중 != 0 ? KÜÇÜKHARF_sınır_değer : 높이;
        if (가로 < 왼쪽) 가로 = 왼쪽;
        if (Dikey_konum < 위쪽) Dikey_konum = 위쪽;
        if (hak > 최대가로) hak = 최대가로;
        if (아래쪽 > 최대세로) 아래쪽 = 최대세로;
        if (hak <= 가로 || 아래쪽 <= Dikey_konum) return 0;
        잘린범위[0] = 가로; 잘린범위[1] = Dikey_konum;
        잘린범위[2] = hak - 가로; 잘린범위[3] = 아래쪽 - Dikey_konum;
        return 1;
    }
    public static int çalıştır(int 가로, int Dikey_konum, int 폭, int süre_değer) {
        if (합성중 != 0 || süre_değer > 32 || klip(가로, Dikey_konum, 폭, süre_değer) == 0) return 0;
        SOLDAN_sınır_değer = 잘린범위[0]; BÜYÜKHARF_sınır = 잘린범위[1];
        hak_sınır_değer = SOLDAN_sınır_değer + 잘린범위[2]; KÜÇÜKHARF_sınır_değer = BÜYÜKHARF_sınır + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean işaretçi_bit(int 가로, int Dikey_konum, int şekil_değer) {
        if (şekil_değer == 1) return 가로 >= 0 && 가로 <= Dikey_konum / 2 && Dikey_konum < 16;
        if (şekil_değer == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - Dikey_konum; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && Dikey_konum >= 2 && Dikey_konum <= 8 && (가로 <= 3 || Dikey_konum <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && Dikey_konum >= 12 && Dikey_konum <= 18 && (가로 >= 17 || Dikey_konum >= 17));
    }
    static int işaretçi_piksel(int 가로, int Dikey_konum) {
        if (işaretçi_bit(가로, Dikey_konum, işaretçi_şekil)) return 2;
        for (int girdi_satırı = -1; girdi_satırı <= 1; girdi_satırı++) for (int yuva_girdi = -1; yuva_girdi <= 1; yuva_girdi++)
            if (işaretçi_bit(가로 + yuva_girdi, Dikey_konum + girdi_satırı, işaretçi_şekil)) return 1;
        return 0;
    }
    static void monitör_piksel(int 가로, int Dikey_konum, int 색) {
        int yuva_girdi = 가로 - işaretçi_X, girdi_satırı = Dikey_konum - işaretçi_Y;
        if (işaretçi_şekil != 0 && yuva_girdi >= 0 && girdi_satırı >= 0 && yuva_girdi < 21 && girdi_satırı < 21) {
            işaretçi_Arka_Plan[girdi_satırı * 21 + yuva_girdi] = 색;
            int puan_değer = işaretçi_piksel(yuva_girdi, girdi_satırı); if (puan_değer != 0) 색 = puan_değer == 2 ? 0xffffff : 0x101010;
        }
        if (Pano.표시화소읽기(가로, Dikey_konum) != 색) {
            Pano.yazma_monitör_piksel(가로, Dikey_konum, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void Son() {
        if (합성중 == 0) return;
        for (int girdi_satırı = BÜYÜKHARF_sınır; girdi_satırı < KÜÇÜKHARF_sınır_değer; girdi_satırı++) for (int yuva_girdi = SOLDAN_sınır_değer; yuva_girdi < hak_sınır_değer; yuva_girdi++)
            monitör_piksel(yuva_girdi, girdi_satırı, 완성그림[(girdi_satırı - BÜYÜKHARF_sınır) * 1920 + yuva_girdi]);
        합성중 = 0;
    }
    public static int piksel(int 가로, int Dikey_konum, int 색) {
        if (가로 < 0 || Dikey_konum < 0 || 가로 >= 너비 || Dikey_konum >= 높이) return 0;
        if (합성중 != 0) {
            if (가로 >= SOLDAN_sınır_değer && 가로 < hak_sınır_değer && Dikey_konum >= BÜYÜKHARF_sınır && Dikey_konum < KÜÇÜKHARF_sınır_değer)
                완성그림[(Dikey_konum - BÜYÜKHARF_sınır) * 1920 + 가로] = 색;
        } else monitör_piksel(가로, Dikey_konum, 색);
        return 0;
    }
    public static void dikdörtgen_dolgu(int 가로, int Dikey_konum, int 폭, int süre_değer, int 색) {
        if (klip(가로, Dikey_konum, 폭, süre_değer) == 0) return;
        가로 = 잘린범위[0]; Dikey_konum = 잘린범위[1]; 폭 = 잘린범위[2]; süre_değer = 잘린범위[3];
        for (int girdi_satırı = Dikey_konum; girdi_satırı < Dikey_konum + süre_değer; girdi_satırı++) for (int yuva_girdi = 가로; yuva_girdi < 가로 + 폭; yuva_girdi++) {
            if (합성중 != 0) 완성그림[(girdi_satırı - BÜYÜKHARF_sınır) * 1920 + yuva_girdi] = 색;
            else monitör_piksel(yuva_girdi, girdi_satırı, 색);
        }
    }
    public static void işaretçi(int 가로, int Dikey_konum, int şekil_değer) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (şekil_değer >= 2 ? 10 : 0), 새세로 = Dikey_konum - (şekil_değer >= 2 ? 10 : 0);
        if (işaretçi_şekil == şekil_değer && işaretçi_X == 새가로 && işaretçi_Y == 새세로) return;
        if (işaretçi_şekil != 0) for (int girdi_satırı = 0; girdi_satırı < 21; girdi_satırı++) for (int yuva_girdi = 0; yuva_girdi < 21; yuva_girdi++) {
            int 가 = işaretçi_X + yuva_girdi, 세 = işaretçi_Y + girdi_satırı;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) Pano.yazma_monitör_piksel(가, 세, işaretçi_Arka_Plan[girdi_satırı * 21 + yuva_girdi]);
        }
        işaretçi_şekil = şekil_değer; işaretçi_X = 새가로; işaretçi_Y = 새세로;
        if (şekil_değer != 0) for (int girdi_satırı = 0; girdi_satırı < 21; girdi_satırı++) for (int yuva_girdi = 0; yuva_girdi < 21; yuva_girdi++) {
            int 가 = işaretçi_X + yuva_girdi, 세 = işaretçi_Y + girdi_satırı;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) {
                işaretçi_Arka_Plan[girdi_satırı * 21 + yuva_girdi] = Pano.표시화소읽기(가, 세);
                int puan_değer = işaretçi_piksel(yuva_girdi, girdi_satırı); if (puan_değer != 0) Pano.yazma_monitör_piksel(가, 세, puan_değer == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
