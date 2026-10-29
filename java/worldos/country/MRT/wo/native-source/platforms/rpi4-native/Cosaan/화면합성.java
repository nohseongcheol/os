// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 화면 dogandi_xëyma·띠 합성·joxañukaay 밑그림을 관리한다. liteew_mbir 화면 fatlekookaay_mbir 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, 높이, 합성중, 왼경계, 위경계, 오른경계, 아래경계;
    static int 포인터가로, 포인터세로, joxañukaay_mélokaan;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] joxañukaay_Njiitlay = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void jël_matuwaay(int 폭, int diir_xëyma) {
        너비 = 폭; 높이 = diir_xëyma; 합성중 = 0; joxañukaay_mélokaan = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int 높이얻기() { return 높이; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int kilip_xëyma(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int Door_xëyma, int diir_xëyma) {
        if (Door_xëyma > 2147483647 - diir_xëyma) return 2147483647;
        return Door_xëyma + diir_xëyma;
    }
    public static int kilip(int 가로, int 세로, int 폭, int diir_xëyma) {
        if (너비 == 0 || 폭 <= 0 || diir_xëyma <= 0) return 0;
        int 오른쪽 = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(세로, diir_xëyma);
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
    public static int daw(int 가로, int 세로, int 폭, int diir_xëyma) {
        if (합성중 != 0 || diir_xëyma > 32 || kilip(가로, 세로, 폭, diir_xëyma) == 0) return 0;
        왼경계 = 잘린범위[0]; 위경계 = 잘린범위[1];
        오른경계 = 왼경계 + 잘린범위[2]; 아래경계 = 위경계 + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean joxañukaay_bit(int 가로, int 세로, int mélokaan_xëyma) {
        if (mélokaan_xëyma == 1) return 가로 >= 0 && 가로 <= 세로 / 2 && 세로 < 16;
        if (mélokaan_xëyma == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - 세로; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && 세로 >= 2 && 세로 <= 8 && (가로 <= 3 || 세로 <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && 세로 >= 12 && 세로 <= 18 && (가로 >= 17 || 세로 >= 17));
    }
    static int joxañukaay_piksel(int 가로, int 세로) {
        if (joxañukaay_bit(가로, 세로, joxañukaay_mélokaan)) return 2;
        for (int buum = -1; buum <= 1; buum++) for (int xar_xar_dugal_xabaar = -1; xar_xar_dugal_xabaar <= 1; xar_xar_dugal_xabaar++)
            if (joxañukaay_bit(가로 + xar_xar_dugal_xabaar, 세로 + buum, joxañukaay_mélokaan)) return 1;
        return 0;
    }
    static void laa_piksel(int 가로, int 세로, int 색) {
        int xar_xar_dugal_xabaar = 가로 - 포인터가로, buum = 세로 - 포인터세로;
        if (joxañukaay_mélokaan != 0 && xar_xar_dugal_xabaar >= 0 && buum >= 0 && xar_xar_dugal_xabaar < 21 && buum < 21) {
            joxañukaay_Njiitlay[buum * 21 + xar_xar_dugal_xabaar] = 색;
            int Tomb_xëyma = joxañukaay_piksel(xar_xar_dugal_xabaar, buum); if (Tomb_xëyma != 0) 색 = Tomb_xëyma == 2 ? 0xffffff : 0x101010;
        }
        if (보드.표시화소읽기(가로, 세로) != 색) {
            보드.biir_laa_piksel(가로, 세로, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void Sottal() {
        if (합성중 == 0) return;
        for (int buum = 위경계; buum < 아래경계; buum++) for (int xar_xar_dugal_xabaar = 왼경계; xar_xar_dugal_xabaar < 오른경계; xar_xar_dugal_xabaar++)
            laa_piksel(xar_xar_dugal_xabaar, buum, 완성그림[(buum - 위경계) * 1920 + xar_xar_dugal_xabaar]);
        합성중 = 0;
    }
    public static int piksel(int 가로, int 세로, int 색) {
        if (가로 < 0 || 세로 < 0 || 가로 >= 너비 || 세로 >= 높이) return 0;
        if (합성중 != 0) {
            if (가로 >= 왼경계 && 가로 < 오른경계 && 세로 >= 위경계 && 세로 < 아래경계)
                완성그림[(세로 - 위경계) * 1920 + 가로] = 색;
        } else laa_piksel(가로, 세로, 색);
        return 0;
    }
    public static void 사각그림(int 가로, int 세로, int 폭, int diir_xëyma, int 색) {
        if (kilip(가로, 세로, 폭, diir_xëyma) == 0) return;
        가로 = 잘린범위[0]; 세로 = 잘린범위[1]; 폭 = 잘린범위[2]; diir_xëyma = 잘린범위[3];
        for (int buum = 세로; buum < 세로 + diir_xëyma; buum++) for (int xar_xar_dugal_xabaar = 가로; xar_xar_dugal_xabaar < 가로 + 폭; xar_xar_dugal_xabaar++) {
            if (합성중 != 0) 완성그림[(buum - 위경계) * 1920 + xar_xar_dugal_xabaar] = 색;
            else laa_piksel(xar_xar_dugal_xabaar, buum, 색);
        }
    }
    public static void joxañukaay(int 가로, int 세로, int mélokaan_xëyma) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (mélokaan_xëyma >= 2 ? 10 : 0), 새세로 = 세로 - (mélokaan_xëyma >= 2 ? 10 : 0);
        if (joxañukaay_mélokaan == mélokaan_xëyma && 포인터가로 == 새가로 && 포인터세로 == 새세로) return;
        if (joxañukaay_mélokaan != 0) for (int buum = 0; buum < 21; buum++) for (int xar_xar_dugal_xabaar = 0; xar_xar_dugal_xabaar < 21; xar_xar_dugal_xabaar++) {
            int 가 = 포인터가로 + xar_xar_dugal_xabaar, 세 = 포인터세로 + buum;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) 보드.biir_laa_piksel(가, 세, joxañukaay_Njiitlay[buum * 21 + xar_xar_dugal_xabaar]);
        }
        joxañukaay_mélokaan = mélokaan_xëyma; 포인터가로 = 새가로; 포인터세로 = 새세로;
        if (mélokaan_xëyma != 0) for (int buum = 0; buum < 21; buum++) for (int xar_xar_dugal_xabaar = 0; xar_xar_dugal_xabaar < 21; xar_xar_dugal_xabaar++) {
            int 가 = 포인터가로 + xar_xar_dugal_xabaar, 세 = 포인터세로 + buum;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) {
                joxañukaay_Njiitlay[buum * 21 + xar_xar_dugal_xabaar] = 보드.표시화소읽기(가, 세);
                int Tomb_xëyma = joxañukaay_piksel(xar_xar_dugal_xabaar, buum); if (Tomb_xëyma != 0) 보드.biir_laa_piksel(가, 세, Tomb_xëyma == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
