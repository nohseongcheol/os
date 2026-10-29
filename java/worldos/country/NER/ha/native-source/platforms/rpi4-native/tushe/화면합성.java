// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 화면 Yanka_Daraja·띠 합성·manuni 밑그림을 관리한다. Na_hakika_Tarin_bayani 화면 Mahardatar_kwamfuta_Tarin_bayani 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, 높이, 합성중, 왼경계, 위경계, 오른경계, 아래경계;
    static int manuni_Maɓallin_X, manuni_Maɓallin_Y, manuni_siffa;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] manuni_Bi_bango = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void Shirya(int 폭, int Tsawo_Daraja) {
        너비 = 폭; 높이 = Tsawo_Daraja; 합성중 = 0; manuni_siffa = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int 높이얻기() { return 높이; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int darfi_Daraja(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int Fara_Daraja, int Tsawo_Daraja) {
        if (Fara_Daraja > 2147483647 - Tsawo_Daraja) return 2147483647;
        return Fara_Daraja + Tsawo_Daraja;
    }
    public static int darfi(int 가로, int 세로, int 폭, int Tsawo_Daraja) {
        if (너비 == 0 || 폭 <= 0 || Tsawo_Daraja <= 0) return 0;
        int 오른쪽 = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(세로, Tsawo_Daraja);
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
    public static int Tafiyar_da(int 가로, int 세로, int 폭, int Tsawo_Daraja) {
        if (합성중 != 0 || Tsawo_Daraja > 32 || darfi(가로, 세로, 폭, Tsawo_Daraja) == 0) return 0;
        왼경계 = 잘린범위[0]; 위경계 = 잘린범위[1];
        오른경계 = 왼경계 + 잘린범위[2]; 아래경계 = 위경계 + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean manuni_bit(int 가로, int 세로, int siffa_Daraja) {
        if (siffa_Daraja == 1) return 가로 >= 0 && 가로 <= 세로 / 2 && 세로 < 16;
        if (siffa_Daraja == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - 세로; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && 세로 >= 2 && 세로 <= 8 && (가로 <= 3 || 세로 <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && 세로 >= 12 && 세로 <= 18 && (가로 >= 17 || 세로 >= 17));
    }
    static int manuni_pel(int 가로, int 세로) {
        if (manuni_bit(가로, 세로, manuni_siffa)) return 2;
        for (int Layi = -1; Layi <= 1; Layi++) for (int rami_Mashigar_bayanai = -1; rami_Mashigar_bayanai <= 1; rami_Mashigar_bayanai++)
            if (manuni_bit(가로 + rami_Mashigar_bayanai, 세로 + Layi, manuni_siffa)) return 1;
        return 0;
    }
    static void Nuna_pel(int 가로, int 세로, int 색) {
        int rami_Mashigar_bayanai = 가로 - manuni_Maɓallin_X, Layi = 세로 - manuni_Maɓallin_Y;
        if (manuni_siffa != 0 && rami_Mashigar_bayanai >= 0 && Layi >= 0 && rami_Mashigar_bayanai < 21 && Layi < 21) {
            manuni_Bi_bango[Layi * 21 + rami_Mashigar_bayanai] = 색;
            int maki_Daraja = manuni_pel(rami_Mashigar_bayanai, Layi); if (maki_Daraja != 0) 색 = maki_Daraja == 2 ? 0xffffff : 0x101010;
        }
        if (보드.표시화소읽기(가로, 세로) != 색) {
            보드.Rubuta_Nuna_pel(가로, 세로, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void Gama() {
        if (합성중 == 0) return;
        for (int Layi = 위경계; Layi < 아래경계; Layi++) for (int rami_Mashigar_bayanai = 왼경계; rami_Mashigar_bayanai < 오른경계; rami_Mashigar_bayanai++)
            Nuna_pel(rami_Mashigar_bayanai, Layi, 완성그림[(Layi - 위경계) * 1920 + rami_Mashigar_bayanai]);
        합성중 = 0;
    }
    public static int pel(int 가로, int 세로, int 색) {
        if (가로 < 0 || 세로 < 0 || 가로 >= 너비 || 세로 >= 높이) return 0;
        if (합성중 != 0) {
            if (가로 >= 왼경계 && 가로 < 오른경계 && 세로 >= 위경계 && 세로 < 아래경계)
                완성그림[(세로 - 위경계) * 1920 + 가로] = 색;
        } else Nuna_pel(가로, 세로, 색);
        return 0;
    }
    public static void 사각그림(int 가로, int 세로, int 폭, int Tsawo_Daraja, int 색) {
        if (darfi(가로, 세로, 폭, Tsawo_Daraja) == 0) return;
        가로 = 잘린범위[0]; 세로 = 잘린범위[1]; 폭 = 잘린범위[2]; Tsawo_Daraja = 잘린범위[3];
        for (int Layi = 세로; Layi < 세로 + Tsawo_Daraja; Layi++) for (int rami_Mashigar_bayanai = 가로; rami_Mashigar_bayanai < 가로 + 폭; rami_Mashigar_bayanai++) {
            if (합성중 != 0) 완성그림[(Layi - 위경계) * 1920 + rami_Mashigar_bayanai] = 색;
            else Nuna_pel(rami_Mashigar_bayanai, Layi, 색);
        }
    }
    public static void manuni(int 가로, int 세로, int siffa_Daraja) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (siffa_Daraja >= 2 ? 10 : 0), 새세로 = 세로 - (siffa_Daraja >= 2 ? 10 : 0);
        if (manuni_siffa == siffa_Daraja && manuni_Maɓallin_X == 새가로 && manuni_Maɓallin_Y == 새세로) return;
        if (manuni_siffa != 0) for (int Layi = 0; Layi < 21; Layi++) for (int rami_Mashigar_bayanai = 0; rami_Mashigar_bayanai < 21; rami_Mashigar_bayanai++) {
            int 가 = manuni_Maɓallin_X + rami_Mashigar_bayanai, 세 = manuni_Maɓallin_Y + Layi;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) 보드.Rubuta_Nuna_pel(가, 세, manuni_Bi_bango[Layi * 21 + rami_Mashigar_bayanai]);
        }
        manuni_siffa = siffa_Daraja; manuni_Maɓallin_X = 새가로; manuni_Maɓallin_Y = 새세로;
        if (siffa_Daraja != 0) for (int Layi = 0; Layi < 21; Layi++) for (int rami_Mashigar_bayanai = 0; rami_Mashigar_bayanai < 21; rami_Mashigar_bayanai++) {
            int 가 = manuni_Maɓallin_X + rami_Mashigar_bayanai, 세 = manuni_Maɓallin_Y + Layi;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) {
                manuni_Bi_bango[Layi * 21 + rami_Mashigar_bayanai] = 보드.표시화소읽기(가, 세);
                int maki_Daraja = manuni_pel(rami_Mashigar_bayanai, Layi); if (maki_Daraja != 0) 보드.Rubuta_Nuna_pel(가, 세, maki_Daraja == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
