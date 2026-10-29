// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 화면 gearr_VALUE·띠 합성·pointeoir 밑그림을 관리한다. iarbhír_sonraí 화면 Cuimhne_sonraí 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, 높이, 합성중, 왼경계, 위경계, 오른경계, 아래경계;
    static int 포인터가로, 포인터세로, pointeoir_cruth;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] pointeoir_Cúlra = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void Ullmhaigh(int 폭, int fad_VALUE) {
        너비 = 폭; 높이 = fad_VALUE; 합성중 = 0; pointeoir_cruth = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int 높이얻기() { return 높이; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int gearrthóg_VALUE(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int Start_VALUE, int fad_VALUE) {
        if (Start_VALUE > 2147483647 - fad_VALUE) return 2147483647;
        return Start_VALUE + fad_VALUE;
    }
    public static int gearrthóg(int 가로, int Ingearach_suíomh, int 폭, int fad_VALUE) {
        if (너비 == 0 || 폭 <= 0 || fad_VALUE <= 0) return 0;
        int RIGHT = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(Ingearach_suíomh, fad_VALUE);
        int 왼쪽 = 합성중 != 0 ? 왼경계 : 0, 위쪽 = 합성중 != 0 ? 위경계 : 0;
        int 최대가로 = 합성중 != 0 ? 오른경계 : 너비, 최대세로 = 합성중 != 0 ? 아래경계 : 높이;
        if (가로 < 왼쪽) 가로 = 왼쪽;
        if (Ingearach_suíomh < 위쪽) Ingearach_suíomh = 위쪽;
        if (RIGHT > 최대가로) RIGHT = 최대가로;
        if (아래쪽 > 최대세로) 아래쪽 = 최대세로;
        if (RIGHT <= 가로 || 아래쪽 <= Ingearach_suíomh) return 0;
        잘린범위[0] = 가로; 잘린범위[1] = Ingearach_suíomh;
        잘린범위[2] = RIGHT - 가로; 잘린범위[3] = 아래쪽 - Ingearach_suíomh;
        return 1;
    }
    public static int Rith_2(int 가로, int Ingearach_suíomh, int 폭, int fad_VALUE) {
        if (합성중 != 0 || fad_VALUE > 32 || gearrthóg(가로, Ingearach_suíomh, 폭, fad_VALUE) == 0) return 0;
        왼경계 = 잘린범위[0]; 위경계 = 잘린범위[1];
        오른경계 = 왼경계 + 잘린범위[2]; 아래경계 = 위경계 + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean pointeoir_giotán(int 가로, int Ingearach_suíomh, int cruth_VALUE) {
        if (cruth_VALUE == 1) return 가로 >= 0 && 가로 <= Ingearach_suíomh / 2 && Ingearach_suíomh < 16;
        if (cruth_VALUE == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - Ingearach_suíomh; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && Ingearach_suíomh >= 2 && Ingearach_suíomh <= 8 && (가로 <= 3 || Ingearach_suíomh <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && Ingearach_suíomh >= 12 && Ingearach_suíomh <= 18 && (가로 >= 17 || Ingearach_suíomh >= 17));
    }
    static int pointeoir_picteilín(int 가로, int Ingearach_suíomh) {
        if (pointeoir_giotán(가로, Ingearach_suíomh, pointeoir_cruth)) return 2;
        for (int Líne = -1; Líne <= 1; Líne++) for (int spás_iontráil = -1; spás_iontráil <= 1; spás_iontráil++)
            if (pointeoir_giotán(가로 + spás_iontráil, Ingearach_suíomh + Líne, pointeoir_cruth)) return 1;
        return 0;
    }
    static void taispeáin_picteilín(int 가로, int Ingearach_suíomh, int 색) {
        int spás_iontráil = 가로 - 포인터가로, Líne = Ingearach_suíomh - 포인터세로;
        if (pointeoir_cruth != 0 && spás_iontráil >= 0 && Líne >= 0 && spás_iontráil < 21 && Líne < 21) {
            pointeoir_Cúlra[Líne * 21 + spás_iontráil] = 색;
            int pointe_VALUE = pointeoir_picteilín(spás_iontráil, Líne); if (pointe_VALUE != 0) 색 = pointe_VALUE == 2 ? 0xffffff : 0x101010;
        }
        if (clár.표시화소읽기(가로, Ingearach_suíomh) != 색) {
            clár.scríobh_taispeáin_picteilín(가로, Ingearach_suíomh, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void Críochnaigh() {
        if (합성중 == 0) return;
        for (int Líne = 위경계; Líne < 아래경계; Líne++) for (int spás_iontráil = 왼경계; spás_iontráil < 오른경계; spás_iontráil++)
            taispeáin_picteilín(spás_iontráil, Líne, 완성그림[(Líne - 위경계) * 1920 + spás_iontráil]);
        합성중 = 0;
    }
    public static int picteilín(int 가로, int Ingearach_suíomh, int 색) {
        if (가로 < 0 || Ingearach_suíomh < 0 || 가로 >= 너비 || Ingearach_suíomh >= 높이) return 0;
        if (합성중 != 0) {
            if (가로 >= 왼경계 && 가로 < 오른경계 && Ingearach_suíomh >= 위경계 && Ingearach_suíomh < 아래경계)
                완성그림[(Ingearach_suíomh - 위경계) * 1920 + 가로] = 색;
        } else taispeáin_picteilín(가로, Ingearach_suíomh, 색);
        return 0;
    }
    public static void 사각그림(int 가로, int Ingearach_suíomh, int 폭, int fad_VALUE, int 색) {
        if (gearrthóg(가로, Ingearach_suíomh, 폭, fad_VALUE) == 0) return;
        가로 = 잘린범위[0]; Ingearach_suíomh = 잘린범위[1]; 폭 = 잘린범위[2]; fad_VALUE = 잘린범위[3];
        for (int Líne = Ingearach_suíomh; Líne < Ingearach_suíomh + fad_VALUE; Líne++) for (int spás_iontráil = 가로; spás_iontráil < 가로 + 폭; spás_iontráil++) {
            if (합성중 != 0) 완성그림[(Líne - 위경계) * 1920 + spás_iontráil] = 색;
            else taispeáin_picteilín(spás_iontráil, Líne, 색);
        }
    }
    public static void pointeoir(int 가로, int Ingearach_suíomh, int cruth_VALUE) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (cruth_VALUE >= 2 ? 10 : 0), 새세로 = Ingearach_suíomh - (cruth_VALUE >= 2 ? 10 : 0);
        if (pointeoir_cruth == cruth_VALUE && 포인터가로 == 새가로 && 포인터세로 == 새세로) return;
        if (pointeoir_cruth != 0) for (int Líne = 0; Líne < 21; Líne++) for (int spás_iontráil = 0; spás_iontráil < 21; spás_iontráil++) {
            int 가 = 포인터가로 + spás_iontráil, 세 = 포인터세로 + Líne;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) clár.scríobh_taispeáin_picteilín(가, 세, pointeoir_Cúlra[Líne * 21 + spás_iontráil]);
        }
        pointeoir_cruth = cruth_VALUE; 포인터가로 = 새가로; 포인터세로 = 새세로;
        if (cruth_VALUE != 0) for (int Líne = 0; Líne < 21; Líne++) for (int spás_iontráil = 0; spás_iontráil < 21; spás_iontráil++) {
            int 가 = 포인터가로 + spás_iontráil, 세 = 포인터세로 + Líne;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) {
                pointeoir_Cúlra[Líne * 21 + spás_iontráil] = clár.표시화소읽기(가, 세);
                int pointe_VALUE = pointeoir_picteilín(spás_iontráil, Líne); if (pointe_VALUE != 0) clár.scríobh_taispeáin_picteilín(가, 세, pointe_VALUE == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
