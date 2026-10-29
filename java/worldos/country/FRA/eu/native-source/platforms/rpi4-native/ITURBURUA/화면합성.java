// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 화면 ebaki_balio·띠 합성·erakusle 밑그림을 관리한다. benetako_datuak 화면 Memoria_datuak 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, 높이, 합성중, 왼경계, 위경계, 오른경계, 아래경계;
    static int erakusle_X, erakusle_Y, erakusle_forma;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] erakusle_horma_paper = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void 준비(int 폭, int luzera_balio) {
        너비 = 폭; 높이 = luzera_balio; 합성중 = 0; erakusle_forma = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int 높이얻기() { return 높이; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int klip_balio(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int HASI_balio, int luzera_balio) {
        if (HASI_balio > 2147483647 - luzera_balio) return 2147483647;
        return HASI_balio + luzera_balio;
    }
    public static int klip(int 가로, int Bertikala_kargu, int 폭, int luzera_balio) {
        if (너비 == 0 || 폭 <= 0 || luzera_balio <= 0) return 0;
        int ESKUIN = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(Bertikala_kargu, luzera_balio);
        int 왼쪽 = 합성중 != 0 ? 왼경계 : 0, 위쪽 = 합성중 != 0 ? 위경계 : 0;
        int 최대가로 = 합성중 != 0 ? 오른경계 : 너비, 최대세로 = 합성중 != 0 ? 아래경계 : 높이;
        if (가로 < 왼쪽) 가로 = 왼쪽;
        if (Bertikala_kargu < 위쪽) Bertikala_kargu = 위쪽;
        if (ESKUIN > 최대가로) ESKUIN = 최대가로;
        if (아래쪽 > 최대세로) 아래쪽 = 최대세로;
        if (ESKUIN <= 가로 || 아래쪽 <= Bertikala_kargu) return 0;
        잘린범위[0] = 가로; 잘린범위[1] = Bertikala_kargu;
        잘린범위[2] = ESKUIN - 가로; 잘린범위[3] = 아래쪽 - Bertikala_kargu;
        return 1;
    }
    public static int Exekutatu_2(int 가로, int Bertikala_kargu, int 폭, int luzera_balio) {
        if (합성중 != 0 || luzera_balio > 32 || klip(가로, Bertikala_kargu, 폭, luzera_balio) == 0) return 0;
        왼경계 = 잘린범위[0]; 위경계 = 잘린범위[1];
        오른경계 = 왼경계 + 잘린범위[2]; 아래경계 = 위경계 + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean erakusle_bit(int 가로, int Bertikala_kargu, int forma_balio) {
        if (forma_balio == 1) return 가로 >= 0 && 가로 <= Bertikala_kargu / 2 && Bertikala_kargu < 16;
        if (forma_balio == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - Bertikala_kargu; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && Bertikala_kargu >= 2 && Bertikala_kargu <= 8 && (가로 <= 3 || Bertikala_kargu <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && Bertikala_kargu >= 12 && Bertikala_kargu <= 18 && (가로 >= 17 || Bertikala_kargu >= 17));
    }
    static int erakusle_pixel(int 가로, int Bertikala_kargu) {
        if (erakusle_bit(가로, Bertikala_kargu, erakusle_forma)) return 2;
        for (int Marra = -1; Marra <= 1; Marra++) for (int 칸 = -1; 칸 <= 1; 칸++)
            if (erakusle_bit(가로 + 칸, Bertikala_kargu + Marra, erakusle_forma)) return 1;
        return 0;
    }
    static void pantaila_pixel(int 가로, int Bertikala_kargu, int 색) {
        int 칸 = 가로 - erakusle_X, Marra = Bertikala_kargu - erakusle_Y;
        if (erakusle_forma != 0 && 칸 >= 0 && Marra >= 0 && 칸 < 21 && Marra < 21) {
            erakusle_horma_paper[Marra * 21 + 칸] = 색;
            int p_balio = erakusle_pixel(칸, Marra); if (p_balio != 0) 색 = p_balio == 2 ? 0xffffff : 0x101010;
        }
        if (arbel.표시화소읽기(가로, Bertikala_kargu) != 색) {
            arbel.idatzi_pantaila_pixel(가로, Bertikala_kargu, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void Amaitu() {
        if (합성중 == 0) return;
        for (int Marra = 위경계; Marra < 아래경계; Marra++) for (int 칸 = 왼경계; 칸 < 오른경계; 칸++)
            pantaila_pixel(칸, Marra, 완성그림[(Marra - 위경계) * 1920 + 칸]);
        합성중 = 0;
    }
    public static int pixel(int 가로, int Bertikala_kargu, int 색) {
        if (가로 < 0 || Bertikala_kargu < 0 || 가로 >= 너비 || Bertikala_kargu >= 높이) return 0;
        if (합성중 != 0) {
            if (가로 >= 왼경계 && 가로 < 오른경계 && Bertikala_kargu >= 위경계 && Bertikala_kargu < 아래경계)
                완성그림[(Bertikala_kargu - 위경계) * 1920 + 가로] = 색;
        } else pantaila_pixel(가로, Bertikala_kargu, 색);
        return 0;
    }
    public static void 사각그림(int 가로, int Bertikala_kargu, int 폭, int luzera_balio, int 색) {
        if (klip(가로, Bertikala_kargu, 폭, luzera_balio) == 0) return;
        가로 = 잘린범위[0]; Bertikala_kargu = 잘린범위[1]; 폭 = 잘린범위[2]; luzera_balio = 잘린범위[3];
        for (int Marra = Bertikala_kargu; Marra < Bertikala_kargu + luzera_balio; Marra++) for (int 칸 = 가로; 칸 < 가로 + 폭; 칸++) {
            if (합성중 != 0) 완성그림[(Marra - 위경계) * 1920 + 칸] = 색;
            else pantaila_pixel(칸, Marra, 색);
        }
    }
    public static void erakusle(int 가로, int Bertikala_kargu, int forma_balio) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (forma_balio >= 2 ? 10 : 0), 새세로 = Bertikala_kargu - (forma_balio >= 2 ? 10 : 0);
        if (erakusle_forma == forma_balio && erakusle_X == 새가로 && erakusle_Y == 새세로) return;
        if (erakusle_forma != 0) for (int Marra = 0; Marra < 21; Marra++) for (int 칸 = 0; 칸 < 21; 칸++) {
            int 가 = erakusle_X + 칸, 세 = erakusle_Y + Marra;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) arbel.idatzi_pantaila_pixel(가, 세, erakusle_horma_paper[Marra * 21 + 칸]);
        }
        erakusle_forma = forma_balio; erakusle_X = 새가로; erakusle_Y = 새세로;
        if (forma_balio != 0) for (int Marra = 0; Marra < 21; Marra++) for (int 칸 = 0; 칸 < 21; 칸++) {
            int 가 = erakusle_X + 칸, 세 = erakusle_Y + Marra;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) {
                erakusle_horma_paper[Marra * 21 + 칸] = arbel.표시화소읽기(가, 세);
                int p_balio = erakusle_pixel(칸, Marra); if (p_balio != 0) arbel.idatzi_pantaila_pixel(가, 세, p_balio == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
