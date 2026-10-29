// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 화면 gearr_VALUE·띠 합성·tomhaire 밑그림을 관리한다. dearbh_dàta 화면 cuimhne_dàta 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, 높이, 합성중, 왼경계, 위경계, 오른경계, 아래경계;
    static int 포인터가로, 포인터세로, tomhaire_cruth;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] tomhaire_cùlaibh = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void Ullaich(int 폭, int faid_VALUE) {
        너비 = 폭; 높이 = faid_VALUE; 합성중 = 0; tomhaire_cruth = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int 높이얻기() { return 높이; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int cliop_VALUE(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int Start_VALUE, int faid_VALUE) {
        if (Start_VALUE > 2147483647 - faid_VALUE) return 2147483647;
        return Start_VALUE + faid_VALUE;
    }
    public static int cliop(int 가로, int inghearach_suidhich, int 폭, int faid_VALUE) {
        if (너비 == 0 || 폭 <= 0 || faid_VALUE <= 0) return 0;
        int RIGHT = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(inghearach_suidhich, faid_VALUE);
        int 왼쪽 = 합성중 != 0 ? 왼경계 : 0, 위쪽 = 합성중 != 0 ? 위경계 : 0;
        int 최대가로 = 합성중 != 0 ? 오른경계 : 너비, 최대세로 = 합성중 != 0 ? 아래경계 : 높이;
        if (가로 < 왼쪽) 가로 = 왼쪽;
        if (inghearach_suidhich < 위쪽) inghearach_suidhich = 위쪽;
        if (RIGHT > 최대가로) RIGHT = 최대가로;
        if (아래쪽 > 최대세로) 아래쪽 = 최대세로;
        if (RIGHT <= 가로 || 아래쪽 <= inghearach_suidhich) return 0;
        잘린범위[0] = 가로; 잘린범위[1] = inghearach_suidhich;
        잘린범위[2] = RIGHT - 가로; 잘린범위[3] = 아래쪽 - inghearach_suidhich;
        return 1;
    }
    public static int ruith(int 가로, int inghearach_suidhich, int 폭, int faid_VALUE) {
        if (합성중 != 0 || faid_VALUE > 32 || cliop(가로, inghearach_suidhich, 폭, faid_VALUE) == 0) return 0;
        왼경계 = 잘린범위[0]; 위경계 = 잘린범위[1];
        오른경계 = 왼경계 + 잘린범위[2]; 아래경계 = 위경계 + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean tomhaire_biot(int 가로, int inghearach_suidhich, int cruth_VALUE) {
        if (cruth_VALUE == 1) return 가로 >= 0 && 가로 <= inghearach_suidhich / 2 && inghearach_suidhich < 16;
        if (cruth_VALUE == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - inghearach_suidhich; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && inghearach_suidhich >= 2 && inghearach_suidhich <= 8 && (가로 <= 3 || inghearach_suidhich <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && inghearach_suidhich >= 12 && inghearach_suidhich <= 18 && (가로 >= 17 || inghearach_suidhich >= 17));
    }
    static int tomhaire_pel(int 가로, int inghearach_suidhich) {
        if (tomhaire_biot(가로, inghearach_suidhich, tomhaire_cruth)) return 2;
        for (int loidhne = -1; loidhne <= 1; loidhne++) for (int slot_cur_a_steach = -1; slot_cur_a_steach <= 1; slot_cur_a_steach++)
            if (tomhaire_biot(가로 + slot_cur_a_steach, inghearach_suidhich + loidhne, tomhaire_cruth)) return 1;
        return 0;
    }
    static void taisbean_pel(int 가로, int inghearach_suidhich, int 색) {
        int slot_cur_a_steach = 가로 - 포인터가로, loidhne = inghearach_suidhich - 포인터세로;
        if (tomhaire_cruth != 0 && slot_cur_a_steach >= 0 && loidhne >= 0 && slot_cur_a_steach < 21 && loidhne < 21) {
            tomhaire_cùlaibh[loidhne * 21 + slot_cur_a_steach] = 색;
            int puing_VALUE = tomhaire_pel(slot_cur_a_steach, loidhne); if (puing_VALUE != 0) 색 = puing_VALUE == 2 ? 0xffffff : 0x101010;
        }
        if (bòrd.표시화소읽기(가로, inghearach_suidhich) != 색) {
            bòrd.sgrìobh_taisbean_pel(가로, inghearach_suidhich, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void Coilean() {
        if (합성중 == 0) return;
        for (int loidhne = 위경계; loidhne < 아래경계; loidhne++) for (int slot_cur_a_steach = 왼경계; slot_cur_a_steach < 오른경계; slot_cur_a_steach++)
            taisbean_pel(slot_cur_a_steach, loidhne, 완성그림[(loidhne - 위경계) * 1920 + slot_cur_a_steach]);
        합성중 = 0;
    }
    public static int pel(int 가로, int inghearach_suidhich, int 색) {
        if (가로 < 0 || inghearach_suidhich < 0 || 가로 >= 너비 || inghearach_suidhich >= 높이) return 0;
        if (합성중 != 0) {
            if (가로 >= 왼경계 && 가로 < 오른경계 && inghearach_suidhich >= 위경계 && inghearach_suidhich < 아래경계)
                완성그림[(inghearach_suidhich - 위경계) * 1920 + 가로] = 색;
        } else taisbean_pel(가로, inghearach_suidhich, 색);
        return 0;
    }
    public static void 사각그림(int 가로, int inghearach_suidhich, int 폭, int faid_VALUE, int 색) {
        if (cliop(가로, inghearach_suidhich, 폭, faid_VALUE) == 0) return;
        가로 = 잘린범위[0]; inghearach_suidhich = 잘린범위[1]; 폭 = 잘린범위[2]; faid_VALUE = 잘린범위[3];
        for (int loidhne = inghearach_suidhich; loidhne < inghearach_suidhich + faid_VALUE; loidhne++) for (int slot_cur_a_steach = 가로; slot_cur_a_steach < 가로 + 폭; slot_cur_a_steach++) {
            if (합성중 != 0) 완성그림[(loidhne - 위경계) * 1920 + slot_cur_a_steach] = 색;
            else taisbean_pel(slot_cur_a_steach, loidhne, 색);
        }
    }
    public static void tomhaire(int 가로, int inghearach_suidhich, int cruth_VALUE) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (cruth_VALUE >= 2 ? 10 : 0), 새세로 = inghearach_suidhich - (cruth_VALUE >= 2 ? 10 : 0);
        if (tomhaire_cruth == cruth_VALUE && 포인터가로 == 새가로 && 포인터세로 == 새세로) return;
        if (tomhaire_cruth != 0) for (int loidhne = 0; loidhne < 21; loidhne++) for (int slot_cur_a_steach = 0; slot_cur_a_steach < 21; slot_cur_a_steach++) {
            int 가 = 포인터가로 + slot_cur_a_steach, 세 = 포인터세로 + loidhne;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) bòrd.sgrìobh_taisbean_pel(가, 세, tomhaire_cùlaibh[loidhne * 21 + slot_cur_a_steach]);
        }
        tomhaire_cruth = cruth_VALUE; 포인터가로 = 새가로; 포인터세로 = 새세로;
        if (cruth_VALUE != 0) for (int loidhne = 0; loidhne < 21; loidhne++) for (int slot_cur_a_steach = 0; slot_cur_a_steach < 21; slot_cur_a_steach++) {
            int 가 = 포인터가로 + slot_cur_a_steach, 세 = 포인터세로 + loidhne;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) {
                tomhaire_cùlaibh[loidhne * 21 + slot_cur_a_steach] = bòrd.표시화소읽기(가, 세);
                int puing_VALUE = tomhaire_pel(slot_cur_a_steach, loidhne); if (puing_VALUE != 0) bòrd.sgrìobh_taisbean_pel(가, 세, puing_VALUE == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
