// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 화면 izgriezt_VALUE·띠 합성·rādītājs 밑그림을 관리한다. faktisks_dati 화면 atmiņa_dati 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, 높이, 합성중, 왼경계, 위경계, 오른경계, 아래경계;
    static int rādītājs_X, rādītājs_Y, rādītājs_forma;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] rādītājs_Fons = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void Sagatavot(int 폭, int 길이) {
        너비 = 폭; 높이 = 길이; 합성중 = 0; rādītājs_forma = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int 높이얻기() { return 높이; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int klips_VALUE(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int Sākt_VALUE, int 길이) {
        if (Sākt_VALUE > 2147483647 - 길이) return 2147483647;
        return Sākt_VALUE + 길이;
    }
    public static int klips(int 가로, int vertikāle_amats, int 폭, int 길이) {
        if (너비 == 0 || 폭 <= 0 || 길이 <= 0) return 0;
        int RIGHT = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(vertikāle_amats, 길이);
        int 왼쪽 = 합성중 != 0 ? 왼경계 : 0, 위쪽 = 합성중 != 0 ? 위경계 : 0;
        int 최대가로 = 합성중 != 0 ? 오른경계 : 너비, 최대세로 = 합성중 != 0 ? 아래경계 : 높이;
        if (가로 < 왼쪽) 가로 = 왼쪽;
        if (vertikāle_amats < 위쪽) vertikāle_amats = 위쪽;
        if (RIGHT > 최대가로) RIGHT = 최대가로;
        if (아래쪽 > 최대세로) 아래쪽 = 최대세로;
        if (RIGHT <= 가로 || 아래쪽 <= vertikāle_amats) return 0;
        잘린범위[0] = 가로; 잘린범위[1] = vertikāle_amats;
        잘린범위[2] = RIGHT - 가로; 잘린범위[3] = 아래쪽 - vertikāle_amats;
        return 1;
    }
    public static int Palaist(int 가로, int vertikāle_amats, int 폭, int 길이) {
        if (합성중 != 0 || 길이 > 32 || klips(가로, vertikāle_amats, 폭, 길이) == 0) return 0;
        왼경계 = 잘린범위[0]; 위경계 = 잘린범위[1];
        오른경계 = 왼경계 + 잘린범위[2]; 아래경계 = 위경계 + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean rādītājs_bit(int 가로, int vertikāle_amats, int forma_VALUE) {
        if (forma_VALUE == 1) return 가로 >= 0 && 가로 <= vertikāle_amats / 2 && vertikāle_amats < 16;
        if (forma_VALUE == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - vertikāle_amats; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && vertikāle_amats >= 2 && vertikāle_amats <= 8 && (가로 <= 3 || vertikāle_amats <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && vertikāle_amats >= 12 && vertikāle_amats <= 18 && (가로 >= 17 || vertikāle_amats >= 17));
    }
    static int rādītājs_attēla_elements(int 가로, int vertikāle_amats) {
        if (rādītājs_bit(가로, vertikāle_amats, rādītājs_forma)) return 2;
        for (int Līniju = -1; Līniju <= 1; Līniju++) for (int 칸 = -1; 칸 <= 1; 칸++)
            if (rādītājs_bit(가로 + 칸, vertikāle_amats + Līniju, rādītājs_forma)) return 1;
        return 0;
    }
    static void rādīt_attēla_elements(int 가로, int vertikāle_amats, int 색) {
        int 칸 = 가로 - rādītājs_X, Līniju = vertikāle_amats - rādītājs_Y;
        if (rādītājs_forma != 0 && 칸 >= 0 && Līniju >= 0 && 칸 < 21 && Līniju < 21) {
            rādītājs_Fons[Līniju * 21 + 칸] = 색;
            int p_VALUE = rādītājs_attēla_elements(칸, Līniju); if (p_VALUE != 0) 색 = p_VALUE == 2 ? 0xffffff : 0x101010;
        }
        if (Panelis.표시화소읽기(가로, vertikāle_amats) != 색) {
            Panelis.rakstīšana_rādīt_attēla_elements(가로, vertikāle_amats, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void beigas() {
        if (합성중 == 0) return;
        for (int Līniju = 위경계; Līniju < 아래경계; Līniju++) for (int 칸 = 왼경계; 칸 < 오른경계; 칸++)
            rādīt_attēla_elements(칸, Līniju, 완성그림[(Līniju - 위경계) * 1920 + 칸]);
        합성중 = 0;
    }
    public static int attēla_elements(int 가로, int vertikāle_amats, int 색) {
        if (가로 < 0 || vertikāle_amats < 0 || 가로 >= 너비 || vertikāle_amats >= 높이) return 0;
        if (합성중 != 0) {
            if (가로 >= 왼경계 && 가로 < 오른경계 && vertikāle_amats >= 위경계 && vertikāle_amats < 아래경계)
                완성그림[(vertikāle_amats - 위경계) * 1920 + 가로] = 색;
        } else rādīt_attēla_elements(가로, vertikāle_amats, 색);
        return 0;
    }
    public static void taisnstūris_aizpildīt(int 가로, int vertikāle_amats, int 폭, int 길이, int 색) {
        if (klips(가로, vertikāle_amats, 폭, 길이) == 0) return;
        가로 = 잘린범위[0]; vertikāle_amats = 잘린범위[1]; 폭 = 잘린범위[2]; 길이 = 잘린범위[3];
        for (int Līniju = vertikāle_amats; Līniju < vertikāle_amats + 길이; Līniju++) for (int 칸 = 가로; 칸 < 가로 + 폭; 칸++) {
            if (합성중 != 0) 완성그림[(Līniju - 위경계) * 1920 + 칸] = 색;
            else rādīt_attēla_elements(칸, Līniju, 색);
        }
    }
    public static void rādītājs(int 가로, int vertikāle_amats, int forma_VALUE) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (forma_VALUE >= 2 ? 10 : 0), 새세로 = vertikāle_amats - (forma_VALUE >= 2 ? 10 : 0);
        if (rādītājs_forma == forma_VALUE && rādītājs_X == 새가로 && rādītājs_Y == 새세로) return;
        if (rādītājs_forma != 0) for (int Līniju = 0; Līniju < 21; Līniju++) for (int 칸 = 0; 칸 < 21; 칸++) {
            int 가 = rādītājs_X + 칸, 세 = rādītājs_Y + Līniju;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) Panelis.rakstīšana_rādīt_attēla_elements(가, 세, rādītājs_Fons[Līniju * 21 + 칸]);
        }
        rādītājs_forma = forma_VALUE; rādītājs_X = 새가로; rādītājs_Y = 새세로;
        if (forma_VALUE != 0) for (int Līniju = 0; Līniju < 21; Līniju++) for (int 칸 = 0; 칸 < 21; 칸++) {
            int 가 = rādītājs_X + 칸, 세 = rādītājs_Y + Līniju;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) {
                rādītājs_Fons[Līniju * 21 + 칸] = Panelis.표시화소읽기(가, 세);
                int p_VALUE = rādītājs_attēla_elements(칸, Līniju); if (p_VALUE != 0) Panelis.rakstīšana_rādīt_attēla_elements(가, 세, p_VALUE == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
