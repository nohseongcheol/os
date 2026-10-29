// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** schermata tagliare_VALORE·띠 합성·puntatore 밑그림을 관리한다. effettivo_dati schermata Memoria_dati 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, altezza_VALORE, 합성중, SINISTRA_limite_VALORE, MAIUSC_limite, DESTRA_limite_VALORE, MINUSC_limite_VALORE;
    static int puntatore_X, puntatore_Y, puntatore_forma;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] puntatore_sfondo = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void Prepara(int 폭, int durata_VALORE) {
        너비 = 폭; altezza_VALORE = durata_VALORE; 합성중 = 0; puntatore_forma = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int get_altezza() { return altezza_VALORE; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int ritagliare_VALORE(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int START_VALORE, int durata_VALORE) {
        if (START_VALORE > 2147483647 - durata_VALORE) return 2147483647;
        return START_VALORE + durata_VALORE;
    }
    public static int ritagliare(int 가로, int Verticale_funzione, int 폭, int durata_VALORE) {
        if (너비 == 0 || 폭 <= 0 || durata_VALORE <= 0) return 0;
        int DESTRA = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(Verticale_funzione, durata_VALORE);
        int 왼쪽 = 합성중 != 0 ? SINISTRA_limite_VALORE : 0, 위쪽 = 합성중 != 0 ? MAIUSC_limite : 0;
        int 최대가로 = 합성중 != 0 ? DESTRA_limite_VALORE : 너비, 최대세로 = 합성중 != 0 ? MINUSC_limite_VALORE : altezza_VALORE;
        if (가로 < 왼쪽) 가로 = 왼쪽;
        if (Verticale_funzione < 위쪽) Verticale_funzione = 위쪽;
        if (DESTRA > 최대가로) DESTRA = 최대가로;
        if (아래쪽 > 최대세로) 아래쪽 = 최대세로;
        if (DESTRA <= 가로 || 아래쪽 <= Verticale_funzione) return 0;
        잘린범위[0] = 가로; 잘린범위[1] = Verticale_funzione;
        잘린범위[2] = DESTRA - 가로; 잘린범위[3] = 아래쪽 - Verticale_funzione;
        return 1;
    }
    public static int avvia(int 가로, int Verticale_funzione, int 폭, int durata_VALORE) {
        if (합성중 != 0 || durata_VALORE > 32 || ritagliare(가로, Verticale_funzione, 폭, durata_VALORE) == 0) return 0;
        SINISTRA_limite_VALORE = 잘린범위[0]; MAIUSC_limite = 잘린범위[1];
        DESTRA_limite_VALORE = SINISTRA_limite_VALORE + 잘린범위[2]; MINUSC_limite_VALORE = MAIUSC_limite + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean puntatore_bit(int 가로, int Verticale_funzione, int forma_VALORE) {
        if (forma_VALORE == 1) return 가로 >= 0 && 가로 <= Verticale_funzione / 2 && Verticale_funzione < 16;
        if (forma_VALORE == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - Verticale_funzione; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && Verticale_funzione >= 2 && Verticale_funzione <= 8 && (가로 <= 3 || Verticale_funzione <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && Verticale_funzione >= 12 && Verticale_funzione <= 18 && (가로 >= 17 || Verticale_funzione >= 17));
    }
    static int puntatore_pixel(int 가로, int Verticale_funzione) {
        if (puntatore_bit(가로, Verticale_funzione, puntatore_forma)) return 2;
        for (int riga_di_ingresso = -1; riga_di_ingresso <= 1; riga_di_ingresso++) for (int slot_voce = -1; slot_voce <= 1; slot_voce++)
            if (puntatore_bit(가로 + slot_voce, Verticale_funzione + riga_di_ingresso, puntatore_forma)) return 1;
        return 0;
    }
    static void display_pixel(int 가로, int Verticale_funzione, int 색) {
        int slot_voce = 가로 - puntatore_X, riga_di_ingresso = Verticale_funzione - puntatore_Y;
        if (puntatore_forma != 0 && slot_voce >= 0 && riga_di_ingresso >= 0 && slot_voce < 21 && riga_di_ingresso < 21) {
            puntatore_sfondo[riga_di_ingresso * 21 + slot_voce] = 색;
            int p_VALORE = puntatore_pixel(slot_voce, riga_di_ingresso); if (p_VALORE != 0) 색 = p_VALORE == 2 ? 0xffffff : 0x101010;
        }
        if (scheda.표시화소읽기(가로, Verticale_funzione) != 색) {
            scheda.scrivere_display_pixel(가로, Verticale_funzione, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void Fine() {
        if (합성중 == 0) return;
        for (int riga_di_ingresso = MAIUSC_limite; riga_di_ingresso < MINUSC_limite_VALORE; riga_di_ingresso++) for (int slot_voce = SINISTRA_limite_VALORE; slot_voce < DESTRA_limite_VALORE; slot_voce++)
            display_pixel(slot_voce, riga_di_ingresso, 완성그림[(riga_di_ingresso - MAIUSC_limite) * 1920 + slot_voce]);
        합성중 = 0;
    }
    public static int pixel(int 가로, int Verticale_funzione, int 색) {
        if (가로 < 0 || Verticale_funzione < 0 || 가로 >= 너비 || Verticale_funzione >= altezza_VALORE) return 0;
        if (합성중 != 0) {
            if (가로 >= SINISTRA_limite_VALORE && 가로 < DESTRA_limite_VALORE && Verticale_funzione >= MAIUSC_limite && Verticale_funzione < MINUSC_limite_VALORE)
                완성그림[(Verticale_funzione - MAIUSC_limite) * 1920 + 가로] = 색;
        } else display_pixel(가로, Verticale_funzione, 색);
        return 0;
    }
    public static void rettangolo_Riempi(int 가로, int Verticale_funzione, int 폭, int durata_VALORE, int 색) {
        if (ritagliare(가로, Verticale_funzione, 폭, durata_VALORE) == 0) return;
        가로 = 잘린범위[0]; Verticale_funzione = 잘린범위[1]; 폭 = 잘린범위[2]; durata_VALORE = 잘린범위[3];
        for (int riga_di_ingresso = Verticale_funzione; riga_di_ingresso < Verticale_funzione + durata_VALORE; riga_di_ingresso++) for (int slot_voce = 가로; slot_voce < 가로 + 폭; slot_voce++) {
            if (합성중 != 0) 완성그림[(riga_di_ingresso - MAIUSC_limite) * 1920 + slot_voce] = 색;
            else display_pixel(slot_voce, riga_di_ingresso, 색);
        }
    }
    public static void puntatore(int 가로, int Verticale_funzione, int forma_VALORE) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (forma_VALORE >= 2 ? 10 : 0), 새세로 = Verticale_funzione - (forma_VALORE >= 2 ? 10 : 0);
        if (puntatore_forma == forma_VALORE && puntatore_X == 새가로 && puntatore_Y == 새세로) return;
        if (puntatore_forma != 0) for (int riga_di_ingresso = 0; riga_di_ingresso < 21; riga_di_ingresso++) for (int slot_voce = 0; slot_voce < 21; slot_voce++) {
            int 가 = puntatore_X + slot_voce, 세 = puntatore_Y + riga_di_ingresso;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < altezza_VALORE) scheda.scrivere_display_pixel(가, 세, puntatore_sfondo[riga_di_ingresso * 21 + slot_voce]);
        }
        puntatore_forma = forma_VALORE; puntatore_X = 새가로; puntatore_Y = 새세로;
        if (forma_VALORE != 0) for (int riga_di_ingresso = 0; riga_di_ingresso < 21; riga_di_ingresso++) for (int slot_voce = 0; slot_voce < 21; slot_voce++) {
            int 가 = puntatore_X + slot_voce, 세 = puntatore_Y + riga_di_ingresso;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < altezza_VALORE) {
                puntatore_sfondo[riga_di_ingresso * 21 + slot_voce] = scheda.표시화소읽기(가, 세);
                int p_VALORE = puntatore_pixel(slot_voce, riga_di_ingresso); if (p_VALORE != 0) scheda.scrivere_display_pixel(가, 세, p_VALORE == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
