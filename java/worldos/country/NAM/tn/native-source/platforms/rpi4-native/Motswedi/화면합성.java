// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 화면 sega_Boleng·띠 합성·sesupi 밑그림을 관리한다. tota_tshedimosetso 화면 memori_tshedimosetso 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, 높이, 합성중, 왼경계, 위경계, 오른경계, 아래경계;
    static int 포인터가로, 포인터세로, sesupi_popego;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] sesupi_Lemorago = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void Baakanya(int 폭, int boleele_Boleng) {
        너비 = 폭; 높이 = boleele_Boleng; 합성중 = 0; sesupi_popego = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int 높이얻기() { return 높이; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int faelekhutshwe_ya_media_Boleng(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int simolola_Boleng, int boleele_Boleng) {
        if (simolola_Boleng > 2147483647 - boleele_Boleng) return 2147483647;
        return simolola_Boleng + boleele_Boleng;
    }
    public static int faelekhutshwe_ya_media(int 가로, int 세로, int 폭, int boleele_Boleng) {
        if (너비 == 0 || 폭 <= 0 || boleele_Boleng <= 0) return 0;
        int 오른쪽 = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(세로, boleele_Boleng);
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
    public static int dirisa(int 가로, int 세로, int 폭, int boleele_Boleng) {
        if (합성중 != 0 || boleele_Boleng > 32 || faelekhutshwe_ya_media(가로, 세로, 폭, boleele_Boleng) == 0) return 0;
        왼경계 = 잘린범위[0]; 위경계 = 잘린범위[1];
        오른경계 = 왼경계 + 잘린범위[2]; 아래경계 = 위경계 + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean sesupi_bit(int 가로, int 세로, int popego_Boleng) {
        if (popego_Boleng == 1) return 가로 >= 0 && 가로 <= 세로 / 2 && 세로 < 16;
        if (popego_Boleng == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - 세로; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && 세로 >= 2 && 세로 <= 8 && (가로 <= 3 || 세로 <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && 세로 >= 12 && 세로 <= 18 && (가로 >= 17 || 세로 >= 17));
    }
    static int sesupi_phele(int 가로, int 세로) {
        if (sesupi_bit(가로, 세로, sesupi_popego)) return 2;
        for (int Mola = -1; Mola <= 1; Mola++) for (int sebaka_tsenyo = -1; sebaka_tsenyo <= 1; sebaka_tsenyo++)
            if (sesupi_bit(가로 + sebaka_tsenyo, 세로 + Mola, sesupi_popego)) return 1;
        return 0;
    }
    static void bontsha_phele(int 가로, int 세로, int 색) {
        int sebaka_tsenyo = 가로 - 포인터가로, Mola = 세로 - 포인터세로;
        if (sesupi_popego != 0 && sebaka_tsenyo >= 0 && Mola >= 0 && sebaka_tsenyo < 21 && Mola < 21) {
            sesupi_Lemorago[Mola * 21 + sebaka_tsenyo] = 색;
            int ntlha_Boleng = sesupi_phele(sebaka_tsenyo, Mola); if (ntlha_Boleng != 0) 색 = ntlha_Boleng == 2 ? 0xffffff : 0x101010;
        }
        if (보드.표시화소읽기(가로, 세로) != 색) {
            보드.kwala_bontsha_phele(가로, 세로, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void Fetsa() {
        if (합성중 == 0) return;
        for (int Mola = 위경계; Mola < 아래경계; Mola++) for (int sebaka_tsenyo = 왼경계; sebaka_tsenyo < 오른경계; sebaka_tsenyo++)
            bontsha_phele(sebaka_tsenyo, Mola, 완성그림[(Mola - 위경계) * 1920 + sebaka_tsenyo]);
        합성중 = 0;
    }
    public static int phele(int 가로, int 세로, int 색) {
        if (가로 < 0 || 세로 < 0 || 가로 >= 너비 || 세로 >= 높이) return 0;
        if (합성중 != 0) {
            if (가로 >= 왼경계 && 가로 < 오른경계 && 세로 >= 위경계 && 세로 < 아래경계)
                완성그림[(세로 - 위경계) * 1920 + 가로] = 색;
        } else bontsha_phele(가로, 세로, 색);
        return 0;
    }
    public static void 사각그림(int 가로, int 세로, int 폭, int boleele_Boleng, int 색) {
        if (faelekhutshwe_ya_media(가로, 세로, 폭, boleele_Boleng) == 0) return;
        가로 = 잘린범위[0]; 세로 = 잘린범위[1]; 폭 = 잘린범위[2]; boleele_Boleng = 잘린범위[3];
        for (int Mola = 세로; Mola < 세로 + boleele_Boleng; Mola++) for (int sebaka_tsenyo = 가로; sebaka_tsenyo < 가로 + 폭; sebaka_tsenyo++) {
            if (합성중 != 0) 완성그림[(Mola - 위경계) * 1920 + sebaka_tsenyo] = 색;
            else bontsha_phele(sebaka_tsenyo, Mola, 색);
        }
    }
    public static void sesupi(int 가로, int 세로, int popego_Boleng) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (popego_Boleng >= 2 ? 10 : 0), 새세로 = 세로 - (popego_Boleng >= 2 ? 10 : 0);
        if (sesupi_popego == popego_Boleng && 포인터가로 == 새가로 && 포인터세로 == 새세로) return;
        if (sesupi_popego != 0) for (int Mola = 0; Mola < 21; Mola++) for (int sebaka_tsenyo = 0; sebaka_tsenyo < 21; sebaka_tsenyo++) {
            int 가 = 포인터가로 + sebaka_tsenyo, 세 = 포인터세로 + Mola;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) 보드.kwala_bontsha_phele(가, 세, sesupi_Lemorago[Mola * 21 + sebaka_tsenyo]);
        }
        sesupi_popego = popego_Boleng; 포인터가로 = 새가로; 포인터세로 = 새세로;
        if (popego_Boleng != 0) for (int Mola = 0; Mola < 21; Mola++) for (int sebaka_tsenyo = 0; sebaka_tsenyo < 21; sebaka_tsenyo++) {
            int 가 = 포인터가로 + sebaka_tsenyo, 세 = 포인터세로 + Mola;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) {
                sesupi_Lemorago[Mola * 21 + sebaka_tsenyo] = 보드.표시화소읽기(가, 세);
                int ntlha_Boleng = sesupi_phele(sebaka_tsenyo, Mola); if (ntlha_Boleng != 0) 보드.kwala_bontsha_phele(가, 세, ntlha_Boleng == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
