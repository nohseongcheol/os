// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 화면 aqta_VALUE·띠 합성·pointer 밑그림을 관리한다. attwali_data 화면 Memorja_data 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, 높이, 합성중, 왼경계, 위경계, 오른경계, 아래경계;
    static int 포인터가로, 포인터세로, pointer_forma;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] pointer_Sfond = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void Ħejji(int 폭, int tul_VALUE) {
        너비 = 폭; 높이 = tul_VALUE; 합성중 = 0; pointer_forma = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int 높이얻기() { return 높이; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int klipp_VALUE(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int Bidu_VALUE, int tul_VALUE) {
        if (Bidu_VALUE > 2147483647 - tul_VALUE) return 2147483647;
        return Bidu_VALUE + tul_VALUE;
    }
    public static int klipp(int 가로, int Vertikali_pożizzjoni, int 폭, int tul_VALUE) {
        if (너비 == 0 || 폭 <= 0 || tul_VALUE <= 0) return 0;
        int RIGHT = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(Vertikali_pożizzjoni, tul_VALUE);
        int 왼쪽 = 합성중 != 0 ? 왼경계 : 0, 위쪽 = 합성중 != 0 ? 위경계 : 0;
        int 최대가로 = 합성중 != 0 ? 오른경계 : 너비, 최대세로 = 합성중 != 0 ? 아래경계 : 높이;
        if (가로 < 왼쪽) 가로 = 왼쪽;
        if (Vertikali_pożizzjoni < 위쪽) Vertikali_pożizzjoni = 위쪽;
        if (RIGHT > 최대가로) RIGHT = 최대가로;
        if (아래쪽 > 최대세로) 아래쪽 = 최대세로;
        if (RIGHT <= 가로 || 아래쪽 <= Vertikali_pożizzjoni) return 0;
        잘린범위[0] = 가로; 잘린범위[1] = Vertikali_pożizzjoni;
        잘린범위[2] = RIGHT - 가로; 잘린범위[3] = 아래쪽 - Vertikali_pożizzjoni;
        return 1;
    }
    public static int serje(int 가로, int Vertikali_pożizzjoni, int 폭, int tul_VALUE) {
        if (합성중 != 0 || tul_VALUE > 32 || klipp(가로, Vertikali_pożizzjoni, 폭, tul_VALUE) == 0) return 0;
        왼경계 = 잘린범위[0]; 위경계 = 잘린범위[1];
        오른경계 = 왼경계 + 잘린범위[2]; 아래경계 = 위경계 + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean pointer_bit(int 가로, int Vertikali_pożizzjoni, int forma_VALUE) {
        if (forma_VALUE == 1) return 가로 >= 0 && 가로 <= Vertikali_pożizzjoni / 2 && Vertikali_pożizzjoni < 16;
        if (forma_VALUE == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - Vertikali_pożizzjoni; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && Vertikali_pożizzjoni >= 2 && Vertikali_pożizzjoni <= 8 && (가로 <= 3 || Vertikali_pożizzjoni <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && Vertikali_pożizzjoni >= 12 && Vertikali_pożizzjoni <= 18 && (가로 >= 17 || Vertikali_pożizzjoni >= 17));
    }
    static int pointer_pel(int 가로, int Vertikali_pożizzjoni) {
        if (pointer_bit(가로, Vertikali_pożizzjoni, pointer_forma)) return 2;
        for (int linja = -1; linja <= 1; linja++) for (int slott_entrata = -1; slott_entrata <= 1; slott_entrata++)
            if (pointer_bit(가로 + slott_entrata, Vertikali_pożizzjoni + linja, pointer_forma)) return 1;
        return 0;
    }
    static void wera_pel(int 가로, int Vertikali_pożizzjoni, int 색) {
        int slott_entrata = 가로 - 포인터가로, linja = Vertikali_pożizzjoni - 포인터세로;
        if (pointer_forma != 0 && slott_entrata >= 0 && linja >= 0 && slott_entrata < 21 && linja < 21) {
            pointer_Sfond[linja * 21 + slott_entrata] = 색;
            int punt_VALUE = pointer_pel(slott_entrata, linja); if (punt_VALUE != 0) 색 = punt_VALUE == 2 ? 0xffffff : 0x101010;
        }
        if (bord.표시화소읽기(가로, Vertikali_pożizzjoni) != 색) {
            bord.kiteb_wera_pel(가로, Vertikali_pożizzjoni, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void Tmiem() {
        if (합성중 == 0) return;
        for (int linja = 위경계; linja < 아래경계; linja++) for (int slott_entrata = 왼경계; slott_entrata < 오른경계; slott_entrata++)
            wera_pel(slott_entrata, linja, 완성그림[(linja - 위경계) * 1920 + slott_entrata]);
        합성중 = 0;
    }
    public static int pel(int 가로, int Vertikali_pożizzjoni, int 색) {
        if (가로 < 0 || Vertikali_pożizzjoni < 0 || 가로 >= 너비 || Vertikali_pożizzjoni >= 높이) return 0;
        if (합성중 != 0) {
            if (가로 >= 왼경계 && 가로 < 오른경계 && Vertikali_pożizzjoni >= 위경계 && Vertikali_pożizzjoni < 아래경계)
                완성그림[(Vertikali_pożizzjoni - 위경계) * 1920 + 가로] = 색;
        } else wera_pel(가로, Vertikali_pożizzjoni, 색);
        return 0;
    }
    public static void 사각그림(int 가로, int Vertikali_pożizzjoni, int 폭, int tul_VALUE, int 색) {
        if (klipp(가로, Vertikali_pożizzjoni, 폭, tul_VALUE) == 0) return;
        가로 = 잘린범위[0]; Vertikali_pożizzjoni = 잘린범위[1]; 폭 = 잘린범위[2]; tul_VALUE = 잘린범위[3];
        for (int linja = Vertikali_pożizzjoni; linja < Vertikali_pożizzjoni + tul_VALUE; linja++) for (int slott_entrata = 가로; slott_entrata < 가로 + 폭; slott_entrata++) {
            if (합성중 != 0) 완성그림[(linja - 위경계) * 1920 + slott_entrata] = 색;
            else wera_pel(slott_entrata, linja, 색);
        }
    }
    public static void pointer(int 가로, int Vertikali_pożizzjoni, int forma_VALUE) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (forma_VALUE >= 2 ? 10 : 0), 새세로 = Vertikali_pożizzjoni - (forma_VALUE >= 2 ? 10 : 0);
        if (pointer_forma == forma_VALUE && 포인터가로 == 새가로 && 포인터세로 == 새세로) return;
        if (pointer_forma != 0) for (int linja = 0; linja < 21; linja++) for (int slott_entrata = 0; slott_entrata < 21; slott_entrata++) {
            int 가 = 포인터가로 + slott_entrata, 세 = 포인터세로 + linja;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) bord.kiteb_wera_pel(가, 세, pointer_Sfond[linja * 21 + slott_entrata]);
        }
        pointer_forma = forma_VALUE; 포인터가로 = 새가로; 포인터세로 = 새세로;
        if (forma_VALUE != 0) for (int linja = 0; linja < 21; linja++) for (int slott_entrata = 0; slott_entrata < 21; slott_entrata++) {
            int 가 = 포인터가로 + slott_entrata, 세 = 포인터세로 + linja;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) {
                pointer_Sfond[linja * 21 + slott_entrata] = bord.표시화소읽기(가, 세);
                int punt_VALUE = pointer_pel(slott_entrata, linja); if (punt_VALUE != 0) bord.kiteb_wera_pel(가, 세, punt_VALUE == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
