// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 화면 kirpti_VALUE·띠 합성·rodyklė 밑그림을 관리한다. faktinis_duomenys 화면 atmintis_duomenys 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, 높이, 합성중, 왼경계, 위경계, 오른경계, 아래경계;
    static int rodyklė_X, rodyklė_Y, rodyklė_figūra;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] rodyklė_Fonas = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void Parengti(int 폭, int 길이) {
        너비 = 폭; 높이 = 길이; 합성중 = 0; rodyklė_figūra = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int 높이얻기() { return 높이; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int klipas_VALUE(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int Start_VALUE, int 길이) {
        if (Start_VALUE > 2147483647 - 길이) return 2147483647;
        return Start_VALUE + 길이;
    }
    public static int klipas(int 가로, int segmentas_padėtis, int 폭, int 길이) {
        if (너비 == 0 || 폭 <= 0 || 길이 <= 0) return 0;
        int RIGHT = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(segmentas_padėtis, 길이);
        int 왼쪽 = 합성중 != 0 ? 왼경계 : 0, 위쪽 = 합성중 != 0 ? 위경계 : 0;
        int 최대가로 = 합성중 != 0 ? 오른경계 : 너비, 최대세로 = 합성중 != 0 ? 아래경계 : 높이;
        if (가로 < 왼쪽) 가로 = 왼쪽;
        if (segmentas_padėtis < 위쪽) segmentas_padėtis = 위쪽;
        if (RIGHT > 최대가로) RIGHT = 최대가로;
        if (아래쪽 > 최대세로) 아래쪽 = 최대세로;
        if (RIGHT <= 가로 || 아래쪽 <= segmentas_padėtis) return 0;
        잘린범위[0] = 가로; 잘린범위[1] = segmentas_padėtis;
        잘린범위[2] = RIGHT - 가로; 잘린범위[3] = 아래쪽 - segmentas_padėtis;
        return 1;
    }
    public static int Paleisti(int 가로, int segmentas_padėtis, int 폭, int 길이) {
        if (합성중 != 0 || 길이 > 32 || klipas(가로, segmentas_padėtis, 폭, 길이) == 0) return 0;
        왼경계 = 잘린범위[0]; 위경계 = 잘린범위[1];
        오른경계 = 왼경계 + 잘린범위[2]; 아래경계 = 위경계 + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean rodyklė_bitas(int 가로, int segmentas_padėtis, int figūra_VALUE) {
        if (figūra_VALUE == 1) return 가로 >= 0 && 가로 <= segmentas_padėtis / 2 && segmentas_padėtis < 16;
        if (figūra_VALUE == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - segmentas_padėtis; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && segmentas_padėtis >= 2 && segmentas_padėtis <= 8 && (가로 <= 3 || segmentas_padėtis <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && segmentas_padėtis >= 12 && segmentas_padėtis <= 18 && (가로 >= 17 || segmentas_padėtis >= 17));
    }
    static int rodyklė_pikselis(int 가로, int segmentas_padėtis) {
        if (rodyklė_bitas(가로, segmentas_padėtis, rodyklė_figūra)) return 2;
        for (int Eilutė = -1; Eilutė <= 1; Eilutė++) for (int 칸 = -1; 칸 <= 1; 칸++)
            if (rodyklė_bitas(가로 + 칸, segmentas_padėtis + Eilutė, rodyklė_figūra)) return 1;
        return 0;
    }
    static void rodyti_pikselis(int 가로, int segmentas_padėtis, int 색) {
        int 칸 = 가로 - rodyklė_X, Eilutė = segmentas_padėtis - rodyklė_Y;
        if (rodyklė_figūra != 0 && 칸 >= 0 && Eilutė >= 0 && 칸 < 21 && Eilutė < 21) {
            rodyklė_Fonas[Eilutė * 21 + 칸] = 색;
            int p_VALUE = rodyklė_pikselis(칸, Eilutė); if (p_VALUE != 0) 색 = p_VALUE == 2 ? 0xffffff : 0x101010;
        }
        if (Lenta.표시화소읽기(가로, segmentas_padėtis) != 색) {
            Lenta.rašymas_rodyti_pikselis(가로, segmentas_padėtis, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void Baigti() {
        if (합성중 == 0) return;
        for (int Eilutė = 위경계; Eilutė < 아래경계; Eilutė++) for (int 칸 = 왼경계; 칸 < 오른경계; 칸++)
            rodyti_pikselis(칸, Eilutė, 완성그림[(Eilutė - 위경계) * 1920 + 칸]);
        합성중 = 0;
    }
    public static int pikselis(int 가로, int segmentas_padėtis, int 색) {
        if (가로 < 0 || segmentas_padėtis < 0 || 가로 >= 너비 || segmentas_padėtis >= 높이) return 0;
        if (합성중 != 0) {
            if (가로 >= 왼경계 && 가로 < 오른경계 && segmentas_padėtis >= 위경계 && segmentas_padėtis < 아래경계)
                완성그림[(segmentas_padėtis - 위경계) * 1920 + 가로] = 색;
        } else rodyti_pikselis(가로, segmentas_padėtis, 색);
        return 0;
    }
    public static void stačiakampis_užpildas(int 가로, int segmentas_padėtis, int 폭, int 길이, int 색) {
        if (klipas(가로, segmentas_padėtis, 폭, 길이) == 0) return;
        가로 = 잘린범위[0]; segmentas_padėtis = 잘린범위[1]; 폭 = 잘린범위[2]; 길이 = 잘린범위[3];
        for (int Eilutė = segmentas_padėtis; Eilutė < segmentas_padėtis + 길이; Eilutė++) for (int 칸 = 가로; 칸 < 가로 + 폭; 칸++) {
            if (합성중 != 0) 완성그림[(Eilutė - 위경계) * 1920 + 칸] = 색;
            else rodyti_pikselis(칸, Eilutė, 색);
        }
    }
    public static void rodyklė(int 가로, int segmentas_padėtis, int figūra_VALUE) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (figūra_VALUE >= 2 ? 10 : 0), 새세로 = segmentas_padėtis - (figūra_VALUE >= 2 ? 10 : 0);
        if (rodyklė_figūra == figūra_VALUE && rodyklė_X == 새가로 && rodyklė_Y == 새세로) return;
        if (rodyklė_figūra != 0) for (int Eilutė = 0; Eilutė < 21; Eilutė++) for (int 칸 = 0; 칸 < 21; 칸++) {
            int 가 = rodyklė_X + 칸, 세 = rodyklė_Y + Eilutė;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) Lenta.rašymas_rodyti_pikselis(가, 세, rodyklė_Fonas[Eilutė * 21 + 칸]);
        }
        rodyklė_figūra = figūra_VALUE; rodyklė_X = 새가로; rodyklė_Y = 새세로;
        if (figūra_VALUE != 0) for (int Eilutė = 0; Eilutė < 21; Eilutė++) for (int 칸 = 0; 칸 < 21; 칸++) {
            int 가 = rodyklė_X + 칸, 세 = rodyklė_Y + Eilutė;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) {
                rodyklė_Fonas[Eilutė * 21 + 칸] = Lenta.표시화소읽기(가, 세);
                int p_VALUE = rodyklė_pikselis(칸, Eilutė); if (p_VALUE != 0) Lenta.rašymas_rodyti_pikselis(가, 세, p_VALUE == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
