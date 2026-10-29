// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 화면 qirqmoq_VALUE·띠 합성·kursor 밑그림을 관리한다. real_ma_lumotlar 화면 Xotira_ma_lumotlar 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, 높이, 합성중, 왼경계, 위경계, 오른경계, 아래경계;
    static int kursor_X_tugmasi, kursor_Y_tugmasi, kursor_shakl;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] kursor_Fon = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void Tayyorlamoq(int 폭, int uzunlik_VALUE) {
        너비 = 폭; 높이 = uzunlik_VALUE; 합성중 = 0; kursor_shakl = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int 높이얻기() { return 높이; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int klip_VALUE(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int Start_VALUE, int uzunlik_VALUE) {
        if (Start_VALUE > 2147483647 - uzunlik_VALUE) return 2147483647;
        return Start_VALUE + uzunlik_VALUE;
    }
    public static int klip(int 가로, int Vertikal_holat, int 폭, int uzunlik_VALUE) {
        if (너비 == 0 || 폭 <= 0 || uzunlik_VALUE <= 0) return 0;
        int RIGHT = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(Vertikal_holat, uzunlik_VALUE);
        int 왼쪽 = 합성중 != 0 ? 왼경계 : 0, 위쪽 = 합성중 != 0 ? 위경계 : 0;
        int 최대가로 = 합성중 != 0 ? 오른경계 : 너비, 최대세로 = 합성중 != 0 ? 아래경계 : 높이;
        if (가로 < 왼쪽) 가로 = 왼쪽;
        if (Vertikal_holat < 위쪽) Vertikal_holat = 위쪽;
        if (RIGHT > 최대가로) RIGHT = 최대가로;
        if (아래쪽 > 최대세로) 아래쪽 = 최대세로;
        if (RIGHT <= 가로 || 아래쪽 <= Vertikal_holat) return 0;
        잘린범위[0] = 가로; 잘린범위[1] = Vertikal_holat;
        잘린범위[2] = RIGHT - 가로; 잘린범위[3] = 아래쪽 - Vertikal_holat;
        return 1;
    }
    public static int Bajarish(int 가로, int Vertikal_holat, int 폭, int uzunlik_VALUE) {
        if (합성중 != 0 || uzunlik_VALUE > 32 || klip(가로, Vertikal_holat, 폭, uzunlik_VALUE) == 0) return 0;
        왼경계 = 잘린범위[0]; 위경계 = 잘린범위[1];
        오른경계 = 왼경계 + 잘린범위[2]; 아래경계 = 위경계 + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean kursor_bit(int 가로, int Vertikal_holat, int shakl_VALUE) {
        if (shakl_VALUE == 1) return 가로 >= 0 && 가로 <= Vertikal_holat / 2 && Vertikal_holat < 16;
        if (shakl_VALUE == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - Vertikal_holat; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && Vertikal_holat >= 2 && Vertikal_holat <= 8 && (가로 <= 3 || Vertikal_holat <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && Vertikal_holat >= 12 && Vertikal_holat <= 18 && (가로 >= 17 || Vertikal_holat >= 17));
    }
    static int kursor_piksel(int 가로, int Vertikal_holat) {
        if (kursor_bit(가로, Vertikal_holat, kursor_shakl)) return 2;
        for (int satr = -1; satr <= 1; satr++) for (int in_kiritish = -1; in_kiritish <= 1; in_kiritish++)
            if (kursor_bit(가로 + in_kiritish, Vertikal_holat + satr, kursor_shakl)) return 1;
        return 0;
    }
    static void ekran_piksel(int 가로, int Vertikal_holat, int 색) {
        int in_kiritish = 가로 - kursor_X_tugmasi, satr = Vertikal_holat - kursor_Y_tugmasi;
        if (kursor_shakl != 0 && in_kiritish >= 0 && satr >= 0 && in_kiritish < 21 && satr < 21) {
            kursor_Fon[satr * 21 + in_kiritish] = 색;
            int nuqta_VALUE = kursor_piksel(in_kiritish, satr); if (nuqta_VALUE != 0) 색 = nuqta_VALUE == 2 ? 0xffffff : 0x101010;
        }
        if (yozuv_taxtasi.표시화소읽기(가로, Vertikal_holat) != 색) {
            yozuv_taxtasi.yozmoq_ekran_piksel(가로, Vertikal_holat, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void Tugatmoq() {
        if (합성중 == 0) return;
        for (int satr = 위경계; satr < 아래경계; satr++) for (int in_kiritish = 왼경계; in_kiritish < 오른경계; in_kiritish++)
            ekran_piksel(in_kiritish, satr, 완성그림[(satr - 위경계) * 1920 + in_kiritish]);
        합성중 = 0;
    }
    public static int piksel(int 가로, int Vertikal_holat, int 색) {
        if (가로 < 0 || Vertikal_holat < 0 || 가로 >= 너비 || Vertikal_holat >= 높이) return 0;
        if (합성중 != 0) {
            if (가로 >= 왼경계 && 가로 < 오른경계 && Vertikal_holat >= 위경계 && Vertikal_holat < 아래경계)
                완성그림[(Vertikal_holat - 위경계) * 1920 + 가로] = 색;
        } else ekran_piksel(가로, Vertikal_holat, 색);
        return 0;
    }
    public static void 사각그림(int 가로, int Vertikal_holat, int 폭, int uzunlik_VALUE, int 색) {
        if (klip(가로, Vertikal_holat, 폭, uzunlik_VALUE) == 0) return;
        가로 = 잘린범위[0]; Vertikal_holat = 잘린범위[1]; 폭 = 잘린범위[2]; uzunlik_VALUE = 잘린범위[3];
        for (int satr = Vertikal_holat; satr < Vertikal_holat + uzunlik_VALUE; satr++) for (int in_kiritish = 가로; in_kiritish < 가로 + 폭; in_kiritish++) {
            if (합성중 != 0) 완성그림[(satr - 위경계) * 1920 + in_kiritish] = 색;
            else ekran_piksel(in_kiritish, satr, 색);
        }
    }
    public static void kursor(int 가로, int Vertikal_holat, int shakl_VALUE) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (shakl_VALUE >= 2 ? 10 : 0), 새세로 = Vertikal_holat - (shakl_VALUE >= 2 ? 10 : 0);
        if (kursor_shakl == shakl_VALUE && kursor_X_tugmasi == 새가로 && kursor_Y_tugmasi == 새세로) return;
        if (kursor_shakl != 0) for (int satr = 0; satr < 21; satr++) for (int in_kiritish = 0; in_kiritish < 21; in_kiritish++) {
            int 가 = kursor_X_tugmasi + in_kiritish, 세 = kursor_Y_tugmasi + satr;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) yozuv_taxtasi.yozmoq_ekran_piksel(가, 세, kursor_Fon[satr * 21 + in_kiritish]);
        }
        kursor_shakl = shakl_VALUE; kursor_X_tugmasi = 새가로; kursor_Y_tugmasi = 새세로;
        if (shakl_VALUE != 0) for (int satr = 0; satr < 21; satr++) for (int in_kiritish = 0; in_kiritish < 21; in_kiritish++) {
            int 가 = kursor_X_tugmasi + in_kiritish, 세 = kursor_Y_tugmasi + satr;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) {
                kursor_Fon[satr * 21 + in_kiritish] = yozuv_taxtasi.표시화소읽기(가, 세);
                int nuqta_VALUE = kursor_piksel(in_kiritish, satr); if (nuqta_VALUE != 0) yozuv_taxtasi.yozmoq_ekran_piksel(가, 세, nuqta_VALUE == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
