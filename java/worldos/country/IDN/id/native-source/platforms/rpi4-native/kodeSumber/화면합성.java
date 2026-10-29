// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 화면 potong_VALUE·띠 합성·pointer 밑그림을 관리한다. aktual_data 화면 Memori_data 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, 높이, 합성중, 왼경계, 위경계, 오른경계, 아래경계;
    static int pointer_X, pointer_Y, pointer_bentuk;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] pointer_wallpaper = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void Siapkan(int 폭, int panjang_VALUE) {
        너비 = 폭; 높이 = panjang_VALUE; 합성중 = 0; pointer_bentuk = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int 높이얻기() { return 높이; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int klip_VALUE(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int Mulai_VALUE, int panjang_VALUE) {
        if (Mulai_VALUE > 2147483647 - panjang_VALUE) return 2147483647;
        return Mulai_VALUE + panjang_VALUE;
    }
    public static int klip(int 가로, int Vertikal_posisi, int 폭, int panjang_VALUE) {
        if (너비 == 0 || 폭 <= 0 || panjang_VALUE <= 0) return 0;
        int RIGHT = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(Vertikal_posisi, panjang_VALUE);
        int 왼쪽 = 합성중 != 0 ? 왼경계 : 0, 위쪽 = 합성중 != 0 ? 위경계 : 0;
        int 최대가로 = 합성중 != 0 ? 오른경계 : 너비, 최대세로 = 합성중 != 0 ? 아래경계 : 높이;
        if (가로 < 왼쪽) 가로 = 왼쪽;
        if (Vertikal_posisi < 위쪽) Vertikal_posisi = 위쪽;
        if (RIGHT > 최대가로) RIGHT = 최대가로;
        if (아래쪽 > 최대세로) 아래쪽 = 최대세로;
        if (RIGHT <= 가로 || 아래쪽 <= Vertikal_posisi) return 0;
        잘린범위[0] = 가로; 잘린범위[1] = Vertikal_posisi;
        잘린범위[2] = RIGHT - 가로; 잘린범위[3] = 아래쪽 - Vertikal_posisi;
        return 1;
    }
    public static int jalankan(int 가로, int Vertikal_posisi, int 폭, int panjang_VALUE) {
        if (합성중 != 0 || panjang_VALUE > 32 || klip(가로, Vertikal_posisi, 폭, panjang_VALUE) == 0) return 0;
        왼경계 = 잘린범위[0]; 위경계 = 잘린범위[1];
        오른경계 = 왼경계 + 잘린범위[2]; 아래경계 = 위경계 + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean pointer_bit(int 가로, int Vertikal_posisi, int bentuk_VALUE) {
        if (bentuk_VALUE == 1) return 가로 >= 0 && 가로 <= Vertikal_posisi / 2 && Vertikal_posisi < 16;
        if (bentuk_VALUE == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - Vertikal_posisi; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && Vertikal_posisi >= 2 && Vertikal_posisi <= 8 && (가로 <= 3 || Vertikal_posisi <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && Vertikal_posisi >= 12 && Vertikal_posisi <= 18 && (가로 >= 17 || Vertikal_posisi >= 17));
    }
    static int pointer_elgam(int 가로, int Vertikal_posisi) {
        if (pointer_bit(가로, Vertikal_posisi, pointer_bentuk)) return 2;
        for (int baris_masukan = -1; baris_masukan <= 1; baris_masukan++) for (int slot_entri = -1; slot_entri <= 1; slot_entri++)
            if (pointer_bit(가로 + slot_entri, Vertikal_posisi + baris_masukan, pointer_bentuk)) return 1;
        return 0;
    }
    static void tampilan_elgam(int 가로, int Vertikal_posisi, int 색) {
        int slot_entri = 가로 - pointer_X, baris_masukan = Vertikal_posisi - pointer_Y;
        if (pointer_bentuk != 0 && slot_entri >= 0 && baris_masukan >= 0 && slot_entri < 21 && baris_masukan < 21) {
            pointer_wallpaper[baris_masukan * 21 + slot_entri] = 색;
            int p_VALUE = pointer_elgam(slot_entri, baris_masukan); if (p_VALUE != 0) 색 = p_VALUE == 2 ? 0xffffff : 0x101010;
        }
        if (Papan.표시화소읽기(가로, Vertikal_posisi) != 색) {
            Papan.tulis_tampilan_elgam(가로, Vertikal_posisi, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void Selesai() {
        if (합성중 == 0) return;
        for (int baris_masukan = 위경계; baris_masukan < 아래경계; baris_masukan++) for (int slot_entri = 왼경계; slot_entri < 오른경계; slot_entri++)
            tampilan_elgam(slot_entri, baris_masukan, 완성그림[(baris_masukan - 위경계) * 1920 + slot_entri]);
        합성중 = 0;
    }
    public static int elgam(int 가로, int Vertikal_posisi, int 색) {
        if (가로 < 0 || Vertikal_posisi < 0 || 가로 >= 너비 || Vertikal_posisi >= 높이) return 0;
        if (합성중 != 0) {
            if (가로 >= 왼경계 && 가로 < 오른경계 && Vertikal_posisi >= 위경계 && Vertikal_posisi < 아래경계)
                완성그림[(Vertikal_posisi - 위경계) * 1920 + 가로] = 색;
        } else tampilan_elgam(가로, Vertikal_posisi, 색);
        return 0;
    }
    public static void persegi_isi(int 가로, int Vertikal_posisi, int 폭, int panjang_VALUE, int 색) {
        if (klip(가로, Vertikal_posisi, 폭, panjang_VALUE) == 0) return;
        가로 = 잘린범위[0]; Vertikal_posisi = 잘린범위[1]; 폭 = 잘린범위[2]; panjang_VALUE = 잘린범위[3];
        for (int baris_masukan = Vertikal_posisi; baris_masukan < Vertikal_posisi + panjang_VALUE; baris_masukan++) for (int slot_entri = 가로; slot_entri < 가로 + 폭; slot_entri++) {
            if (합성중 != 0) 완성그림[(baris_masukan - 위경계) * 1920 + slot_entri] = 색;
            else tampilan_elgam(slot_entri, baris_masukan, 색);
        }
    }
    public static void pointer(int 가로, int Vertikal_posisi, int bentuk_VALUE) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (bentuk_VALUE >= 2 ? 10 : 0), 새세로 = Vertikal_posisi - (bentuk_VALUE >= 2 ? 10 : 0);
        if (pointer_bentuk == bentuk_VALUE && pointer_X == 새가로 && pointer_Y == 새세로) return;
        if (pointer_bentuk != 0) for (int baris_masukan = 0; baris_masukan < 21; baris_masukan++) for (int slot_entri = 0; slot_entri < 21; slot_entri++) {
            int 가 = pointer_X + slot_entri, 세 = pointer_Y + baris_masukan;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) Papan.tulis_tampilan_elgam(가, 세, pointer_wallpaper[baris_masukan * 21 + slot_entri]);
        }
        pointer_bentuk = bentuk_VALUE; pointer_X = 새가로; pointer_Y = 새세로;
        if (bentuk_VALUE != 0) for (int baris_masukan = 0; baris_masukan < 21; baris_masukan++) for (int slot_entri = 0; slot_entri < 21; slot_entri++) {
            int 가 = pointer_X + slot_entri, 세 = pointer_Y + baris_masukan;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) {
                pointer_wallpaper[baris_masukan * 21 + slot_entri] = Papan.표시화소읽기(가, 세);
                int p_VALUE = pointer_elgam(slot_entri, baris_masukan); if (p_VALUE != 0) Papan.tulis_tampilan_elgam(가, 세, p_VALUE == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
