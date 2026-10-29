// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 화면 bölmək_VALUE·띠 합성·göstərici 밑그림을 관리한다. faktiki_verilənlər 화면 Yaddaş_verilənlər 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, 높이, 합성중, 왼경계, 위경계, 오른경계, 아래경계;
    static int göstərici_X, göstərici_Y, göstərici_fiqur;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] göstərici_Fon = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void Hazırla(int 폭, int uzunluq_VALUE) {
        너비 = 폭; 높이 = uzunluq_VALUE; 합성중 = 0; göstərici_fiqur = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int 높이얻기() { return 높이; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int klip_VALUE(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int Başla_VALUE, int uzunluq_VALUE) {
        if (Başla_VALUE > 2147483647 - uzunluq_VALUE) return 2147483647;
        return Başla_VALUE + uzunluq_VALUE;
    }
    public static int klip(int 가로, int Şaquli_yerinə_qoymaq, int 폭, int uzunluq_VALUE) {
        if (너비 == 0 || 폭 <= 0 || uzunluq_VALUE <= 0) return 0;
        int RIGHT = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(Şaquli_yerinə_qoymaq, uzunluq_VALUE);
        int 왼쪽 = 합성중 != 0 ? 왼경계 : 0, 위쪽 = 합성중 != 0 ? 위경계 : 0;
        int 최대가로 = 합성중 != 0 ? 오른경계 : 너비, 최대세로 = 합성중 != 0 ? 아래경계 : 높이;
        if (가로 < 왼쪽) 가로 = 왼쪽;
        if (Şaquli_yerinə_qoymaq < 위쪽) Şaquli_yerinə_qoymaq = 위쪽;
        if (RIGHT > 최대가로) RIGHT = 최대가로;
        if (아래쪽 > 최대세로) 아래쪽 = 최대세로;
        if (RIGHT <= 가로 || 아래쪽 <= Şaquli_yerinə_qoymaq) return 0;
        잘린범위[0] = 가로; 잘린범위[1] = Şaquli_yerinə_qoymaq;
        잘린범위[2] = RIGHT - 가로; 잘린범위[3] = 아래쪽 - Şaquli_yerinə_qoymaq;
        return 1;
    }
    public static int İcra_Et(int 가로, int Şaquli_yerinə_qoymaq, int 폭, int uzunluq_VALUE) {
        if (합성중 != 0 || uzunluq_VALUE > 32 || klip(가로, Şaquli_yerinə_qoymaq, 폭, uzunluq_VALUE) == 0) return 0;
        왼경계 = 잘린범위[0]; 위경계 = 잘린범위[1];
        오른경계 = 왼경계 + 잘린범위[2]; 아래경계 = 위경계 + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean göstərici_bit(int 가로, int Şaquli_yerinə_qoymaq, int fiqur_VALUE) {
        if (fiqur_VALUE == 1) return 가로 >= 0 && 가로 <= Şaquli_yerinə_qoymaq / 2 && Şaquli_yerinə_qoymaq < 16;
        if (fiqur_VALUE == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - Şaquli_yerinə_qoymaq; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && Şaquli_yerinə_qoymaq >= 2 && Şaquli_yerinə_qoymaq <= 8 && (가로 <= 3 || Şaquli_yerinə_qoymaq <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && Şaquli_yerinə_qoymaq >= 12 && Şaquli_yerinə_qoymaq <= 18 && (가로 >= 17 || Şaquli_yerinə_qoymaq >= 17));
    }
    static int göstərici_piksel(int 가로, int Şaquli_yerinə_qoymaq) {
        if (göstərici_bit(가로, Şaquli_yerinə_qoymaq, göstərici_fiqur)) return 2;
        for (int Giriş = -1; Giriş <= 1; Giriş++) for (int slot_daxiletmə = -1; slot_daxiletmə <= 1; slot_daxiletmə++)
            if (göstərici_bit(가로 + slot_daxiletmə, Şaquli_yerinə_qoymaq + Giriş, göstərici_fiqur)) return 1;
        return 0;
    }
    static void displey_piksel(int 가로, int Şaquli_yerinə_qoymaq, int 색) {
        int slot_daxiletmə = 가로 - göstərici_X, Giriş = Şaquli_yerinə_qoymaq - göstərici_Y;
        if (göstərici_fiqur != 0 && slot_daxiletmə >= 0 && Giriş >= 0 && slot_daxiletmə < 21 && Giriş < 21) {
            göstərici_Fon[Giriş * 21 + slot_daxiletmə] = 색;
            int p_VALUE = göstərici_piksel(slot_daxiletmə, Giriş); if (p_VALUE != 0) 색 = p_VALUE == 2 ? 0xffffff : 0x101010;
        }
        if (lövhə.표시화소읽기(가로, Şaquli_yerinə_qoymaq) != 색) {
            lövhə.yazmaq_displey_piksel(가로, Şaquli_yerinə_qoymaq, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void Bitir() {
        if (합성중 == 0) return;
        for (int Giriş = 위경계; Giriş < 아래경계; Giriş++) for (int slot_daxiletmə = 왼경계; slot_daxiletmə < 오른경계; slot_daxiletmə++)
            displey_piksel(slot_daxiletmə, Giriş, 완성그림[(Giriş - 위경계) * 1920 + slot_daxiletmə]);
        합성중 = 0;
    }
    public static int piksel(int 가로, int Şaquli_yerinə_qoymaq, int 색) {
        if (가로 < 0 || Şaquli_yerinə_qoymaq < 0 || 가로 >= 너비 || Şaquli_yerinə_qoymaq >= 높이) return 0;
        if (합성중 != 0) {
            if (가로 >= 왼경계 && 가로 < 오른경계 && Şaquli_yerinə_qoymaq >= 위경계 && Şaquli_yerinə_qoymaq < 아래경계)
                완성그림[(Şaquli_yerinə_qoymaq - 위경계) * 1920 + 가로] = 색;
        } else displey_piksel(가로, Şaquli_yerinə_qoymaq, 색);
        return 0;
    }
    public static void 사각그림(int 가로, int Şaquli_yerinə_qoymaq, int 폭, int uzunluq_VALUE, int 색) {
        if (klip(가로, Şaquli_yerinə_qoymaq, 폭, uzunluq_VALUE) == 0) return;
        가로 = 잘린범위[0]; Şaquli_yerinə_qoymaq = 잘린범위[1]; 폭 = 잘린범위[2]; uzunluq_VALUE = 잘린범위[3];
        for (int Giriş = Şaquli_yerinə_qoymaq; Giriş < Şaquli_yerinə_qoymaq + uzunluq_VALUE; Giriş++) for (int slot_daxiletmə = 가로; slot_daxiletmə < 가로 + 폭; slot_daxiletmə++) {
            if (합성중 != 0) 완성그림[(Giriş - 위경계) * 1920 + slot_daxiletmə] = 색;
            else displey_piksel(slot_daxiletmə, Giriş, 색);
        }
    }
    public static void göstərici(int 가로, int Şaquli_yerinə_qoymaq, int fiqur_VALUE) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (fiqur_VALUE >= 2 ? 10 : 0), 새세로 = Şaquli_yerinə_qoymaq - (fiqur_VALUE >= 2 ? 10 : 0);
        if (göstərici_fiqur == fiqur_VALUE && göstərici_X == 새가로 && göstərici_Y == 새세로) return;
        if (göstərici_fiqur != 0) for (int Giriş = 0; Giriş < 21; Giriş++) for (int slot_daxiletmə = 0; slot_daxiletmə < 21; slot_daxiletmə++) {
            int 가 = göstərici_X + slot_daxiletmə, 세 = göstərici_Y + Giriş;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) lövhə.yazmaq_displey_piksel(가, 세, göstərici_Fon[Giriş * 21 + slot_daxiletmə]);
        }
        göstərici_fiqur = fiqur_VALUE; göstərici_X = 새가로; göstərici_Y = 새세로;
        if (fiqur_VALUE != 0) for (int Giriş = 0; Giriş < 21; Giriş++) for (int slot_daxiletmə = 0; slot_daxiletmə < 21; slot_daxiletmə++) {
            int 가 = göstərici_X + slot_daxiletmə, 세 = göstərici_Y + Giriş;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) {
                göstərici_Fon[Giriş * 21 + slot_daxiletmə] = lövhə.표시화소읽기(가, 세);
                int p_VALUE = göstərici_piksel(slot_daxiletmə, Giriş); if (p_VALUE != 0) lövhə.yazmaq_displey_piksel(가, 세, p_VALUE == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
