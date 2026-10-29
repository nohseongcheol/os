// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 화면 potong_VALUE·띠 합성·penuding 밑그림을 관리한다. sebenar_data 화면 Memori_data 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, 높이, 합성중, 왼경계, 위경계, 오른경계, 아래경계;
    static int penuding_X, penuding_Y, penuding_bentuk;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] penuding_latar = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void Sediakan(int 폭, int kepanjangan_VALUE) {
        너비 = 폭; 높이 = kepanjangan_VALUE; 합성중 = 0; penuding_bentuk = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int 높이얻기() { return 높이; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int klip_VALUE(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int Mula_VALUE, int kepanjangan_VALUE) {
        if (Mula_VALUE > 2147483647 - kepanjangan_VALUE) return 2147483647;
        return Mula_VALUE + kepanjangan_VALUE;
    }
    public static int klip(int 가로, int Menegak_jawatan, int 폭, int kepanjangan_VALUE) {
        if (너비 == 0 || 폭 <= 0 || kepanjangan_VALUE <= 0) return 0;
        int RIGHT = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(Menegak_jawatan, kepanjangan_VALUE);
        int 왼쪽 = 합성중 != 0 ? 왼경계 : 0, 위쪽 = 합성중 != 0 ? 위경계 : 0;
        int 최대가로 = 합성중 != 0 ? 오른경계 : 너비, 최대세로 = 합성중 != 0 ? 아래경계 : 높이;
        if (가로 < 왼쪽) 가로 = 왼쪽;
        if (Menegak_jawatan < 위쪽) Menegak_jawatan = 위쪽;
        if (RIGHT > 최대가로) RIGHT = 최대가로;
        if (아래쪽 > 최대세로) 아래쪽 = 최대세로;
        if (RIGHT <= 가로 || 아래쪽 <= Menegak_jawatan) return 0;
        잘린범위[0] = 가로; 잘린범위[1] = Menegak_jawatan;
        잘린범위[2] = RIGHT - 가로; 잘린범위[3] = 아래쪽 - Menegak_jawatan;
        return 1;
    }
    public static int Jalan(int 가로, int Menegak_jawatan, int 폭, int kepanjangan_VALUE) {
        if (합성중 != 0 || kepanjangan_VALUE > 32 || klip(가로, Menegak_jawatan, 폭, kepanjangan_VALUE) == 0) return 0;
        왼경계 = 잘린범위[0]; 위경계 = 잘린범위[1];
        오른경계 = 왼경계 + 잘린범위[2]; 아래경계 = 위경계 + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean penuding_bit(int 가로, int Menegak_jawatan, int bentuk_VALUE) {
        if (bentuk_VALUE == 1) return 가로 >= 0 && 가로 <= Menegak_jawatan / 2 && Menegak_jawatan < 16;
        if (bentuk_VALUE == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - Menegak_jawatan; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && Menegak_jawatan >= 2 && Menegak_jawatan <= 8 && (가로 <= 3 || Menegak_jawatan <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && Menegak_jawatan >= 12 && Menegak_jawatan <= 18 && (가로 >= 17 || Menegak_jawatan >= 17));
    }
    static int penuding_pel(int 가로, int Menegak_jawatan) {
        if (penuding_bit(가로, Menegak_jawatan, penuding_bentuk)) return 2;
        for (int baris = -1; baris <= 1; baris++) for (int 칸 = -1; 칸 <= 1; 칸++)
            if (penuding_bit(가로 + 칸, Menegak_jawatan + baris, penuding_bentuk)) return 1;
        return 0;
    }
    static void papar_pel(int 가로, int Menegak_jawatan, int 색) {
        int 칸 = 가로 - penuding_X, baris = Menegak_jawatan - penuding_Y;
        if (penuding_bentuk != 0 && 칸 >= 0 && baris >= 0 && 칸 < 21 && baris < 21) {
            penuding_latar[baris * 21 + 칸] = 색;
            int p_VALUE = penuding_pel(칸, baris); if (p_VALUE != 0) 색 = p_VALUE == 2 ? 0xffffff : 0x101010;
        }
        if (Papan.표시화소읽기(가로, Menegak_jawatan) != 색) {
            Papan.tulis_papar_pel(가로, Menegak_jawatan, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void Tamat() {
        if (합성중 == 0) return;
        for (int baris = 위경계; baris < 아래경계; baris++) for (int 칸 = 왼경계; 칸 < 오른경계; 칸++)
            papar_pel(칸, baris, 완성그림[(baris - 위경계) * 1920 + 칸]);
        합성중 = 0;
    }
    public static int pel(int 가로, int Menegak_jawatan, int 색) {
        if (가로 < 0 || Menegak_jawatan < 0 || 가로 >= 너비 || Menegak_jawatan >= 높이) return 0;
        if (합성중 != 0) {
            if (가로 >= 왼경계 && 가로 < 오른경계 && Menegak_jawatan >= 위경계 && Menegak_jawatan < 아래경계)
                완성그림[(Menegak_jawatan - 위경계) * 1920 + 가로] = 색;
        } else papar_pel(가로, Menegak_jawatan, 색);
        return 0;
    }
    public static void segi_empat_tepat_isi(int 가로, int Menegak_jawatan, int 폭, int kepanjangan_VALUE, int 색) {
        if (klip(가로, Menegak_jawatan, 폭, kepanjangan_VALUE) == 0) return;
        가로 = 잘린범위[0]; Menegak_jawatan = 잘린범위[1]; 폭 = 잘린범위[2]; kepanjangan_VALUE = 잘린범위[3];
        for (int baris = Menegak_jawatan; baris < Menegak_jawatan + kepanjangan_VALUE; baris++) for (int 칸 = 가로; 칸 < 가로 + 폭; 칸++) {
            if (합성중 != 0) 완성그림[(baris - 위경계) * 1920 + 칸] = 색;
            else papar_pel(칸, baris, 색);
        }
    }
    public static void penuding(int 가로, int Menegak_jawatan, int bentuk_VALUE) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (bentuk_VALUE >= 2 ? 10 : 0), 새세로 = Menegak_jawatan - (bentuk_VALUE >= 2 ? 10 : 0);
        if (penuding_bentuk == bentuk_VALUE && penuding_X == 새가로 && penuding_Y == 새세로) return;
        if (penuding_bentuk != 0) for (int baris = 0; baris < 21; baris++) for (int 칸 = 0; 칸 < 21; 칸++) {
            int 가 = penuding_X + 칸, 세 = penuding_Y + baris;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) Papan.tulis_papar_pel(가, 세, penuding_latar[baris * 21 + 칸]);
        }
        penuding_bentuk = bentuk_VALUE; penuding_X = 새가로; penuding_Y = 새세로;
        if (bentuk_VALUE != 0) for (int baris = 0; baris < 21; baris++) for (int 칸 = 0; 칸 < 21; 칸++) {
            int 가 = penuding_X + 칸, 세 = penuding_Y + baris;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) {
                penuding_latar[baris * 21 + 칸] = Papan.표시화소읽기(가, 세);
                int p_VALUE = penuding_pel(칸, baris); if (p_VALUE != 0) Papan.tulis_papar_pel(가, 세, p_VALUE == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
