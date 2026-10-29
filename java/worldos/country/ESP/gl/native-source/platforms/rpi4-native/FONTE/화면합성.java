// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 화면 cortar_VALOR·띠 합성·punteiro 밑그림을 관리한다. real_datos 화면 Memoria_datos 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, 높이, 합성중, 왼경계, 위경계, 오른경계, 아래경계;
    static int punteiro_X, punteiro_Y, punteiro_forma;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] punteiro_Fondo = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void 준비(int 폭, int duración_VALOR) {
        너비 = 폭; 높이 = duración_VALOR; 합성중 = 0; punteiro_forma = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int 높이얻기() { return 높이; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int clip_VALOR(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int START_VALOR, int duración_VALOR) {
        if (START_VALOR > 2147483647 - duración_VALOR) return 2147483647;
        return START_VALOR + duración_VALOR;
    }
    public static int clip(int 가로, int Vertical_cargo, int 폭, int duración_VALOR) {
        if (너비 == 0 || 폭 <= 0 || duración_VALOR <= 0) return 0;
        int DEREITA = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(Vertical_cargo, duración_VALOR);
        int 왼쪽 = 합성중 != 0 ? 왼경계 : 0, 위쪽 = 합성중 != 0 ? 위경계 : 0;
        int 최대가로 = 합성중 != 0 ? 오른경계 : 너비, 최대세로 = 합성중 != 0 ? 아래경계 : 높이;
        if (가로 < 왼쪽) 가로 = 왼쪽;
        if (Vertical_cargo < 위쪽) Vertical_cargo = 위쪽;
        if (DEREITA > 최대가로) DEREITA = 최대가로;
        if (아래쪽 > 최대세로) 아래쪽 = 최대세로;
        if (DEREITA <= 가로 || 아래쪽 <= Vertical_cargo) return 0;
        잘린범위[0] = 가로; 잘린범위[1] = Vertical_cargo;
        잘린범위[2] = DEREITA - 가로; 잘린범위[3] = 아래쪽 - Vertical_cargo;
        return 1;
    }
    public static int Executar_2(int 가로, int Vertical_cargo, int 폭, int duración_VALOR) {
        if (합성중 != 0 || duración_VALOR > 32 || clip(가로, Vertical_cargo, 폭, duración_VALOR) == 0) return 0;
        왼경계 = 잘린범위[0]; 위경계 = 잘린범위[1];
        오른경계 = 왼경계 + 잘린범위[2]; 아래경계 = 위경계 + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean punteiro_bit(int 가로, int Vertical_cargo, int forma_VALOR) {
        if (forma_VALOR == 1) return 가로 >= 0 && 가로 <= Vertical_cargo / 2 && Vertical_cargo < 16;
        if (forma_VALOR == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - Vertical_cargo; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && Vertical_cargo >= 2 && Vertical_cargo <= 8 && (가로 <= 3 || Vertical_cargo <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && Vertical_cargo >= 12 && Vertical_cargo <= 18 && (가로 >= 17 || Vertical_cargo >= 17));
    }
    static int punteiro_píxel(int 가로, int Vertical_cargo) {
        if (punteiro_bit(가로, Vertical_cargo, punteiro_forma)) return 2;
        for (int Liña = -1; Liña <= 1; Liña++) for (int 칸 = -1; 칸 <= 1; 칸++)
            if (punteiro_bit(가로 + 칸, Vertical_cargo + Liña, punteiro_forma)) return 1;
        return 0;
    }
    static void mostrar_píxel(int 가로, int Vertical_cargo, int 색) {
        int 칸 = 가로 - punteiro_X, Liña = Vertical_cargo - punteiro_Y;
        if (punteiro_forma != 0 && 칸 >= 0 && Liña >= 0 && 칸 < 21 && Liña < 21) {
            punteiro_Fondo[Liña * 21 + 칸] = 색;
            int p_VALOR = punteiro_píxel(칸, Liña); if (p_VALOR != 0) 색 = p_VALOR == 2 ? 0xffffff : 0x101010;
        }
        if (Panel.표시화소읽기(가로, Vertical_cargo) != 색) {
            Panel.escribir_mostrar_píxel(가로, Vertical_cargo, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void fin() {
        if (합성중 == 0) return;
        for (int Liña = 위경계; Liña < 아래경계; Liña++) for (int 칸 = 왼경계; 칸 < 오른경계; 칸++)
            mostrar_píxel(칸, Liña, 완성그림[(Liña - 위경계) * 1920 + 칸]);
        합성중 = 0;
    }
    public static int píxel(int 가로, int Vertical_cargo, int 색) {
        if (가로 < 0 || Vertical_cargo < 0 || 가로 >= 너비 || Vertical_cargo >= 높이) return 0;
        if (합성중 != 0) {
            if (가로 >= 왼경계 && 가로 < 오른경계 && Vertical_cargo >= 위경계 && Vertical_cargo < 아래경계)
                완성그림[(Vertical_cargo - 위경계) * 1920 + 가로] = 색;
        } else mostrar_píxel(가로, Vertical_cargo, 색);
        return 0;
    }
    public static void 사각그림(int 가로, int Vertical_cargo, int 폭, int duración_VALOR, int 색) {
        if (clip(가로, Vertical_cargo, 폭, duración_VALOR) == 0) return;
        가로 = 잘린범위[0]; Vertical_cargo = 잘린범위[1]; 폭 = 잘린범위[2]; duración_VALOR = 잘린범위[3];
        for (int Liña = Vertical_cargo; Liña < Vertical_cargo + duración_VALOR; Liña++) for (int 칸 = 가로; 칸 < 가로 + 폭; 칸++) {
            if (합성중 != 0) 완성그림[(Liña - 위경계) * 1920 + 칸] = 색;
            else mostrar_píxel(칸, Liña, 색);
        }
    }
    public static void punteiro(int 가로, int Vertical_cargo, int forma_VALOR) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (forma_VALOR >= 2 ? 10 : 0), 새세로 = Vertical_cargo - (forma_VALOR >= 2 ? 10 : 0);
        if (punteiro_forma == forma_VALOR && punteiro_X == 새가로 && punteiro_Y == 새세로) return;
        if (punteiro_forma != 0) for (int Liña = 0; Liña < 21; Liña++) for (int 칸 = 0; 칸 < 21; 칸++) {
            int 가 = punteiro_X + 칸, 세 = punteiro_Y + Liña;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) Panel.escribir_mostrar_píxel(가, 세, punteiro_Fondo[Liña * 21 + 칸]);
        }
        punteiro_forma = forma_VALOR; punteiro_X = 새가로; punteiro_Y = 새세로;
        if (forma_VALOR != 0) for (int Liña = 0; Liña < 21; Liña++) for (int 칸 = 0; 칸 < 21; 칸++) {
            int 가 = punteiro_X + 칸, 세 = punteiro_Y + Liña;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) {
                punteiro_Fondo[Liña * 21 + 칸] = Panel.표시화소읽기(가, 세);
                int p_VALOR = punteiro_píxel(칸, Liña); if (p_VALOR != 0) Panel.escribir_mostrar_píxel(가, 세, p_VALOR == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
