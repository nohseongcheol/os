// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 화면 decupa_VALUE·띠 합성·cursor 밑그림을 관리한다. real_date 화면 Memorie_date 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, 높이, 합성중, 왼경계, 위경계, 오른경계, 아래경계;
    static int cursor_X, cursor_Y, cursor_formă;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] cursor_tapet = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void Pregătiți(int 폭, int lungime_VALUE) {
        너비 = 폭; 높이 = lungime_VALUE; 합성중 = 0; cursor_formă = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int 높이얻기() { return 높이; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int clip_VALUE(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int buta_VALUE, int lungime_VALUE) {
        if (buta_VALUE > 2147483647 - lungime_VALUE) return 2147483647;
        return buta_VALUE + lungime_VALUE;
    }
    public static int clip(int 가로, int Verticală_poziție, int 폭, int lungime_VALUE) {
        if (너비 == 0 || 폭 <= 0 || lungime_VALUE <= 0) return 0;
        int RIGHT = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(Verticală_poziție, lungime_VALUE);
        int 왼쪽 = 합성중 != 0 ? 왼경계 : 0, 위쪽 = 합성중 != 0 ? 위경계 : 0;
        int 최대가로 = 합성중 != 0 ? 오른경계 : 너비, 최대세로 = 합성중 != 0 ? 아래경계 : 높이;
        if (가로 < 왼쪽) 가로 = 왼쪽;
        if (Verticală_poziție < 위쪽) Verticală_poziție = 위쪽;
        if (RIGHT > 최대가로) RIGHT = 최대가로;
        if (아래쪽 > 최대세로) 아래쪽 = 최대세로;
        if (RIGHT <= 가로 || 아래쪽 <= Verticală_poziție) return 0;
        잘린범위[0] = 가로; 잘린범위[1] = Verticală_poziție;
        잘린범위[2] = RIGHT - 가로; 잘린범위[3] = 아래쪽 - Verticală_poziție;
        return 1;
    }
    public static int Pornește(int 가로, int Verticală_poziție, int 폭, int lungime_VALUE) {
        if (합성중 != 0 || lungime_VALUE > 32 || clip(가로, Verticală_poziție, 폭, lungime_VALUE) == 0) return 0;
        왼경계 = 잘린범위[0]; 위경계 = 잘린범위[1];
        오른경계 = 왼경계 + 잘린범위[2]; 아래경계 = 위경계 + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean cursor_bit(int 가로, int Verticală_poziție, int formă_VALUE) {
        if (formă_VALUE == 1) return 가로 >= 0 && 가로 <= Verticală_poziție / 2 && Verticală_poziție < 16;
        if (formă_VALUE == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - Verticală_poziție; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && Verticală_poziție >= 2 && Verticală_poziție <= 8 && (가로 <= 3 || Verticală_poziție <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && Verticală_poziție >= 12 && Verticală_poziție <= 18 && (가로 >= 17 || Verticală_poziție >= 17));
    }
    static int cursor_element_imagine(int 가로, int Verticală_poziție) {
        if (cursor_bit(가로, Verticală_poziție, cursor_formă)) return 2;
        for (int Linie = -1; Linie <= 1; Linie++) for (int 칸 = -1; 칸 <= 1; 칸++)
            if (cursor_bit(가로 + 칸, Verticală_poziție + Linie, cursor_formă)) return 1;
        return 0;
    }
    static void afișa_element_imagine(int 가로, int Verticală_poziție, int 색) {
        int 칸 = 가로 - cursor_X, Linie = Verticală_poziție - cursor_Y;
        if (cursor_formă != 0 && 칸 >= 0 && Linie >= 0 && 칸 < 21 && Linie < 21) {
            cursor_tapet[Linie * 21 + 칸] = 색;
            int p_VALUE = cursor_element_imagine(칸, Linie); if (p_VALUE != 0) 색 = p_VALUE == 2 ? 0xffffff : 0x101010;
        }
        if (Avizier.표시화소읽기(가로, Verticală_poziție) != 색) {
            Avizier.scriere_afișa_element_imagine(가로, Verticală_poziție, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void sfârșit() {
        if (합성중 == 0) return;
        for (int Linie = 위경계; Linie < 아래경계; Linie++) for (int 칸 = 왼경계; 칸 < 오른경계; 칸++)
            afișa_element_imagine(칸, Linie, 완성그림[(Linie - 위경계) * 1920 + 칸]);
        합성중 = 0;
    }
    public static int element_imagine(int 가로, int Verticală_poziție, int 색) {
        if (가로 < 0 || Verticală_poziție < 0 || 가로 >= 너비 || Verticală_poziție >= 높이) return 0;
        if (합성중 != 0) {
            if (가로 >= 왼경계 && 가로 < 오른경계 && Verticală_poziție >= 위경계 && Verticală_poziție < 아래경계)
                완성그림[(Verticală_poziție - 위경계) * 1920 + 가로] = 색;
        } else afișa_element_imagine(가로, Verticală_poziție, 색);
        return 0;
    }
    public static void dreptunghi_umple(int 가로, int Verticală_poziție, int 폭, int lungime_VALUE, int 색) {
        if (clip(가로, Verticală_poziție, 폭, lungime_VALUE) == 0) return;
        가로 = 잘린범위[0]; Verticală_poziție = 잘린범위[1]; 폭 = 잘린범위[2]; lungime_VALUE = 잘린범위[3];
        for (int Linie = Verticală_poziție; Linie < Verticală_poziție + lungime_VALUE; Linie++) for (int 칸 = 가로; 칸 < 가로 + 폭; 칸++) {
            if (합성중 != 0) 완성그림[(Linie - 위경계) * 1920 + 칸] = 색;
            else afișa_element_imagine(칸, Linie, 색);
        }
    }
    public static void cursor(int 가로, int Verticală_poziție, int formă_VALUE) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (formă_VALUE >= 2 ? 10 : 0), 새세로 = Verticală_poziție - (formă_VALUE >= 2 ? 10 : 0);
        if (cursor_formă == formă_VALUE && cursor_X == 새가로 && cursor_Y == 새세로) return;
        if (cursor_formă != 0) for (int Linie = 0; Linie < 21; Linie++) for (int 칸 = 0; 칸 < 21; 칸++) {
            int 가 = cursor_X + 칸, 세 = cursor_Y + Linie;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) Avizier.scriere_afișa_element_imagine(가, 세, cursor_tapet[Linie * 21 + 칸]);
        }
        cursor_formă = formă_VALUE; cursor_X = 새가로; cursor_Y = 새세로;
        if (formă_VALUE != 0) for (int Linie = 0; Linie < 21; Linie++) for (int 칸 = 0; 칸 < 21; 칸++) {
            int 가 = cursor_X + 칸, 세 = cursor_Y + Linie;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) {
                cursor_tapet[Linie * 21 + 칸] = Avizier.표시화소읽기(가, 세);
                int p_VALUE = cursor_element_imagine(칸, Linie); if (p_VALUE != 0) Avizier.scriere_afișa_element_imagine(가, 세, p_VALUE == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
