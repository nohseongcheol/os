// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** tela cortar_VALOR·띠 합성·ponteiro 밑그림을 관리한다. real_dados tela Memória_dados 접근은 보드가 담당한다. */
public final class ComposiçãoEcrã {
    static int 너비, altura_VALOR, 합성중, ESQUERDA_limite_VALOR, MAIÚSCULA_limite, DIREITA_limite_VALOR, MINÚSCULA_limite_VALOR;
    static int ponteiro_X, ponteiro_Y, ponteiro_forma;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] ponteiro_Tela_de_fundo = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void Preparar(int 폭, int duração_VALOR) {
        너비 = 폭; altura_VALOR = duração_VALOR; 합성중 = 0; ponteiro_forma = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int get_altura() { return altura_VALOR; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int recortar_VALOR(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int START_VALOR, int duração_VALOR) {
        if (START_VALOR > 2147483647 - duração_VALOR) return 2147483647;
        return START_VALOR + duração_VALOR;
    }
    public static int recortar(int 가로, int Vertical_cargo, int 폭, int duração_VALOR) {
        if (너비 == 0 || 폭 <= 0 || duração_VALOR <= 0) return 0;
        int DIREITA = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(Vertical_cargo, duração_VALOR);
        int 왼쪽 = 합성중 != 0 ? ESQUERDA_limite_VALOR : 0, 위쪽 = 합성중 != 0 ? MAIÚSCULA_limite : 0;
        int 최대가로 = 합성중 != 0 ? DIREITA_limite_VALOR : 너비, 최대세로 = 합성중 != 0 ? MINÚSCULA_limite_VALOR : altura_VALOR;
        if (가로 < 왼쪽) 가로 = 왼쪽;
        if (Vertical_cargo < 위쪽) Vertical_cargo = 위쪽;
        if (DIREITA > 최대가로) DIREITA = 최대가로;
        if (아래쪽 > 최대세로) 아래쪽 = 최대세로;
        if (DIREITA <= 가로 || 아래쪽 <= Vertical_cargo) return 0;
        잘린범위[0] = 가로; 잘린범위[1] = Vertical_cargo;
        잘린범위[2] = DIREITA - 가로; 잘린범위[3] = 아래쪽 - Vertical_cargo;
        return 1;
    }
    public static int iniciar(int 가로, int Vertical_cargo, int 폭, int duração_VALOR) {
        if (합성중 != 0 || duração_VALOR > 32 || recortar(가로, Vertical_cargo, 폭, duração_VALOR) == 0) return 0;
        ESQUERDA_limite_VALOR = 잘린범위[0]; MAIÚSCULA_limite = 잘린범위[1];
        DIREITA_limite_VALOR = ESQUERDA_limite_VALOR + 잘린범위[2]; MINÚSCULA_limite_VALOR = MAIÚSCULA_limite + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean ponteiro_bit(int 가로, int Vertical_cargo, int forma_VALOR) {
        if (forma_VALOR == 1) return 가로 >= 0 && 가로 <= Vertical_cargo / 2 && Vertical_cargo < 16;
        if (forma_VALOR == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - Vertical_cargo; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && Vertical_cargo >= 2 && Vertical_cargo <= 8 && (가로 <= 3 || Vertical_cargo <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && Vertical_cargo >= 12 && Vertical_cargo <= 18 && (가로 >= 17 || Vertical_cargo >= 17));
    }
    static int ponteiro_pixel(int 가로, int Vertical_cargo) {
        if (ponteiro_bit(가로, Vertical_cargo, ponteiro_forma)) return 2;
        for (int linha_de_entrada = -1; linha_de_entrada <= 1; linha_de_entrada++) for (int slot_entrada = -1; slot_entrada <= 1; slot_entrada++)
            if (ponteiro_bit(가로 + slot_entrada, Vertical_cargo + linha_de_entrada, ponteiro_forma)) return 1;
        return 0;
    }
    static void visor_pixel(int 가로, int Vertical_cargo, int 색) {
        int slot_entrada = 가로 - ponteiro_X, linha_de_entrada = Vertical_cargo - ponteiro_Y;
        if (ponteiro_forma != 0 && slot_entrada >= 0 && linha_de_entrada >= 0 && slot_entrada < 21 && linha_de_entrada < 21) {
            ponteiro_Tela_de_fundo[linha_de_entrada * 21 + slot_entrada] = 색;
            int ponto_VALOR = ponteiro_pixel(slot_entrada, linha_de_entrada); if (ponto_VALOR != 0) 색 = ponto_VALOR == 2 ? 0xffffff : 0x101010;
        }
        if (Quadro.lerPíxelExibido(가로, Vertical_cargo) != 색) {
            Quadro.escreverPíxelExibido(가로, Vertical_cargo, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void fim() {
        if (합성중 == 0) return;
        for (int linha_de_entrada = MAIÚSCULA_limite; linha_de_entrada < MINÚSCULA_limite_VALOR; linha_de_entrada++) for (int slot_entrada = ESQUERDA_limite_VALOR; slot_entrada < DIREITA_limite_VALOR; slot_entrada++)
            visor_pixel(slot_entrada, linha_de_entrada, 완성그림[(linha_de_entrada - MAIÚSCULA_limite) * 1920 + slot_entrada]);
        합성중 = 0;
    }
    public static int pixel(int 가로, int Vertical_cargo, int 색) {
        if (가로 < 0 || Vertical_cargo < 0 || 가로 >= 너비 || Vertical_cargo >= altura_VALOR) return 0;
        if (합성중 != 0) {
            if (가로 >= ESQUERDA_limite_VALOR && 가로 < DIREITA_limite_VALOR && Vertical_cargo >= MAIÚSCULA_limite && Vertical_cargo < MINÚSCULA_limite_VALOR)
                완성그림[(Vertical_cargo - MAIÚSCULA_limite) * 1920 + 가로] = 색;
        } else visor_pixel(가로, Vertical_cargo, 색);
        return 0;
    }
    public static void retângulo_preencher(int 가로, int Vertical_cargo, int 폭, int duração_VALOR, int 색) {
        if (recortar(가로, Vertical_cargo, 폭, duração_VALOR) == 0) return;
        가로 = 잘린범위[0]; Vertical_cargo = 잘린범위[1]; 폭 = 잘린범위[2]; duração_VALOR = 잘린범위[3];
        for (int linha_de_entrada = Vertical_cargo; linha_de_entrada < Vertical_cargo + duração_VALOR; linha_de_entrada++) for (int slot_entrada = 가로; slot_entrada < 가로 + 폭; slot_entrada++) {
            if (합성중 != 0) 완성그림[(linha_de_entrada - MAIÚSCULA_limite) * 1920 + slot_entrada] = 색;
            else visor_pixel(slot_entrada, linha_de_entrada, 색);
        }
    }
    public static void ponteiro(int 가로, int Vertical_cargo, int forma_VALOR) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (forma_VALOR >= 2 ? 10 : 0), 새세로 = Vertical_cargo - (forma_VALOR >= 2 ? 10 : 0);
        if (ponteiro_forma == forma_VALOR && ponteiro_X == 새가로 && ponteiro_Y == 새세로) return;
        if (ponteiro_forma != 0) for (int linha_de_entrada = 0; linha_de_entrada < 21; linha_de_entrada++) for (int slot_entrada = 0; slot_entrada < 21; slot_entrada++) {
            int 가 = ponteiro_X + slot_entrada, 세 = ponteiro_Y + linha_de_entrada;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < altura_VALOR) Quadro.escreverPíxelExibido(가, 세, ponteiro_Tela_de_fundo[linha_de_entrada * 21 + slot_entrada]);
        }
        ponteiro_forma = forma_VALOR; ponteiro_X = 새가로; ponteiro_Y = 새세로;
        if (forma_VALOR != 0) for (int linha_de_entrada = 0; linha_de_entrada < 21; linha_de_entrada++) for (int slot_entrada = 0; slot_entrada < 21; slot_entrada++) {
            int 가 = ponteiro_X + slot_entrada, 세 = ponteiro_Y + linha_de_entrada;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < altura_VALOR) {
                ponteiro_Tela_de_fundo[linha_de_entrada * 21 + slot_entrada] = Quadro.lerPíxelExibido(가, 세);
                int ponto_VALOR = ponteiro_pixel(slot_entrada, linha_de_entrada); if (ponto_VALOR != 0) Quadro.escreverPíxelExibido(가, 세, ponto_VALOR == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
