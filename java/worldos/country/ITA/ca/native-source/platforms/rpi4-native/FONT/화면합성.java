// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 화면 tallar_VALOR·띠 합성·punter 밑그림을 관리한다. real_dades 화면 Memòria_dades 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, 높이, 합성중, 왼경계, 위경계, 오른경계, 아래경계;
    static int punter_X, punter_Y, punter_forma;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] punter_Fons = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void Prepara(int 폭, int durada_VALOR) {
        너비 = 폭; 높이 = durada_VALOR; 합성중 = 0; punter_forma = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int 높이얻기() { return 높이; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int clip_VALOR(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int Inici_VALOR, int durada_VALOR) {
        if (Inici_VALOR > 2147483647 - durada_VALOR) return 2147483647;
        return Inici_VALOR + durada_VALOR;
    }
    public static int clip(int 가로, int Vertical_càrrec, int 폭, int durada_VALOR) {
        if (너비 == 0 || 폭 <= 0 || durada_VALOR <= 0) return 0;
        int DRETA = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(Vertical_càrrec, durada_VALOR);
        int 왼쪽 = 합성중 != 0 ? 왼경계 : 0, 위쪽 = 합성중 != 0 ? 위경계 : 0;
        int 최대가로 = 합성중 != 0 ? 오른경계 : 너비, 최대세로 = 합성중 != 0 ? 아래경계 : 높이;
        if (가로 < 왼쪽) 가로 = 왼쪽;
        if (Vertical_càrrec < 위쪽) Vertical_càrrec = 위쪽;
        if (DRETA > 최대가로) DRETA = 최대가로;
        if (아래쪽 > 최대세로) 아래쪽 = 최대세로;
        if (DRETA <= 가로 || 아래쪽 <= Vertical_càrrec) return 0;
        잘린범위[0] = 가로; 잘린범위[1] = Vertical_càrrec;
        잘린범위[2] = DRETA - 가로; 잘린범위[3] = 아래쪽 - Vertical_càrrec;
        return 1;
    }
    public static int Executa_2(int 가로, int Vertical_càrrec, int 폭, int durada_VALOR) {
        if (합성중 != 0 || durada_VALOR > 32 || clip(가로, Vertical_càrrec, 폭, durada_VALOR) == 0) return 0;
        왼경계 = 잘린범위[0]; 위경계 = 잘린범위[1];
        오른경계 = 왼경계 + 잘린범위[2]; 아래경계 = 위경계 + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean punter_bit(int 가로, int Vertical_càrrec, int forma_VALOR) {
        if (forma_VALOR == 1) return 가로 >= 0 && 가로 <= Vertical_càrrec / 2 && Vertical_càrrec < 16;
        if (forma_VALOR == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - Vertical_càrrec; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && Vertical_càrrec >= 2 && Vertical_càrrec <= 8 && (가로 <= 3 || Vertical_càrrec <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && Vertical_càrrec >= 12 && Vertical_càrrec <= 18 && (가로 >= 17 || Vertical_càrrec >= 17));
    }
    static int punter_píxel(int 가로, int Vertical_càrrec) {
        if (punter_bit(가로, Vertical_càrrec, punter_forma)) return 2;
        for (int línia = -1; línia <= 1; línia++) for (int 칸 = -1; 칸 <= 1; 칸++)
            if (punter_bit(가로 + 칸, Vertical_càrrec + línia, punter_forma)) return 1;
        return 0;
    }
    static void mostrar_píxel(int 가로, int Vertical_càrrec, int 색) {
        int 칸 = 가로 - punter_X, línia = Vertical_càrrec - punter_Y;
        if (punter_forma != 0 && 칸 >= 0 && línia >= 0 && 칸 < 21 && línia < 21) {
            punter_Fons[línia * 21 + 칸] = 색;
            int p_VALOR = punter_píxel(칸, línia); if (p_VALOR != 0) 색 = p_VALOR == 2 ? 0xffffff : 0x101010;
        }
        if (Tauler.tancar_mostrar_píxel(가로, Vertical_càrrec) != 색) {
            Tauler.escriure_mostrar_píxel(가로, Vertical_càrrec, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void fi() {
        if (합성중 == 0) return;
        for (int línia = 위경계; línia < 아래경계; línia++) for (int 칸 = 왼경계; 칸 < 오른경계; 칸++)
            mostrar_píxel(칸, línia, 완성그림[(línia - 위경계) * 1920 + 칸]);
        합성중 = 0;
    }
    public static int píxel(int 가로, int Vertical_càrrec, int 색) {
        if (가로 < 0 || Vertical_càrrec < 0 || 가로 >= 너비 || Vertical_càrrec >= 높이) return 0;
        if (합성중 != 0) {
            if (가로 >= 왼경계 && 가로 < 오른경계 && Vertical_càrrec >= 위경계 && Vertical_càrrec < 아래경계)
                완성그림[(Vertical_càrrec - 위경계) * 1920 + 가로] = 색;
        } else mostrar_píxel(가로, Vertical_càrrec, 색);
        return 0;
    }
    public static void 사각그림(int 가로, int Vertical_càrrec, int 폭, int durada_VALOR, int 색) {
        if (clip(가로, Vertical_càrrec, 폭, durada_VALOR) == 0) return;
        가로 = 잘린범위[0]; Vertical_càrrec = 잘린범위[1]; 폭 = 잘린범위[2]; durada_VALOR = 잘린범위[3];
        for (int línia = Vertical_càrrec; línia < Vertical_càrrec + durada_VALOR; línia++) for (int 칸 = 가로; 칸 < 가로 + 폭; 칸++) {
            if (합성중 != 0) 완성그림[(línia - 위경계) * 1920 + 칸] = 색;
            else mostrar_píxel(칸, línia, 색);
        }
    }
    public static void punter(int 가로, int Vertical_càrrec, int forma_VALOR) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (forma_VALOR >= 2 ? 10 : 0), 새세로 = Vertical_càrrec - (forma_VALOR >= 2 ? 10 : 0);
        if (punter_forma == forma_VALOR && punter_X == 새가로 && punter_Y == 새세로) return;
        if (punter_forma != 0) for (int línia = 0; línia < 21; línia++) for (int 칸 = 0; 칸 < 21; 칸++) {
            int 가 = punter_X + 칸, 세 = punter_Y + línia;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) Tauler.escriure_mostrar_píxel(가, 세, punter_Fons[línia * 21 + 칸]);
        }
        punter_forma = forma_VALOR; punter_X = 새가로; punter_Y = 새세로;
        if (forma_VALOR != 0) for (int línia = 0; línia < 21; línia++) for (int 칸 = 0; 칸 < 21; 칸++) {
            int 가 = punter_X + 칸, 세 = punter_Y + línia;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) {
                punter_Fons[línia * 21 + 칸] = Tauler.tancar_mostrar_píxel(가, 세);
                int p_VALOR = punter_píxel(칸, línia); if (p_VALOR != 0) Tauler.escriure_mostrar_píxel(가, 세, p_VALOR == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
