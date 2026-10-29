// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 화면 stříhat_HODNOTA·띠 합성·ukazatel 밑그림을 관리한다. skutečný_data 화면 Paměť_data 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, výška_HODNOTA, 합성중, ZLEVA_mez_HODNOTA, VELKÁ_mez, právo_mez_HODNOTA, MALÁ_mez_HODNOTA;
    static int ukazatel_X, ukazatel_Y, ukazatel_tvar;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] ukazatel_Pozadí = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void Připravit(int 폭, int délka_HODNOTA) {
        너비 = 폭; výška_HODNOTA = délka_HODNOTA; 합성중 = 0; ukazatel_tvar = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int get_výška() { return výška_HODNOTA; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int oříznout_HODNOTA(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int START_HODNOTA, int délka_HODNOTA) {
        if (START_HODNOTA > 2147483647 - délka_HODNOTA) return 2147483647;
        return START_HODNOTA + délka_HODNOTA;
    }
    public static int oříznout(int 가로, int Svislá_pozice, int 폭, int délka_HODNOTA) {
        if (너비 == 0 || 폭 <= 0 || délka_HODNOTA <= 0) return 0;
        int právo = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(Svislá_pozice, délka_HODNOTA);
        int 왼쪽 = 합성중 != 0 ? ZLEVA_mez_HODNOTA : 0, 위쪽 = 합성중 != 0 ? VELKÁ_mez : 0;
        int 최대가로 = 합성중 != 0 ? právo_mez_HODNOTA : 너비, 최대세로 = 합성중 != 0 ? MALÁ_mez_HODNOTA : výška_HODNOTA;
        if (가로 < 왼쪽) 가로 = 왼쪽;
        if (Svislá_pozice < 위쪽) Svislá_pozice = 위쪽;
        if (právo > 최대가로) právo = 최대가로;
        if (아래쪽 > 최대세로) 아래쪽 = 최대세로;
        if (právo <= 가로 || 아래쪽 <= Svislá_pozice) return 0;
        잘린범위[0] = 가로; 잘린범위[1] = Svislá_pozice;
        잘린범위[2] = právo - 가로; 잘린범위[3] = 아래쪽 - Svislá_pozice;
        return 1;
    }
    public static int Spustit_2(int 가로, int Svislá_pozice, int 폭, int délka_HODNOTA) {
        if (합성중 != 0 || délka_HODNOTA > 32 || oříznout(가로, Svislá_pozice, 폭, délka_HODNOTA) == 0) return 0;
        ZLEVA_mez_HODNOTA = 잘린범위[0]; VELKÁ_mez = 잘린범위[1];
        právo_mez_HODNOTA = ZLEVA_mez_HODNOTA + 잘린범위[2]; MALÁ_mez_HODNOTA = VELKÁ_mez + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean ukazatel_bit(int 가로, int Svislá_pozice, int tvar_HODNOTA) {
        if (tvar_HODNOTA == 1) return 가로 >= 0 && 가로 <= Svislá_pozice / 2 && Svislá_pozice < 16;
        if (tvar_HODNOTA == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - Svislá_pozice; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && Svislá_pozice >= 2 && Svislá_pozice <= 8 && (가로 <= 3 || Svislá_pozice <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && Svislá_pozice >= 12 && Svislá_pozice <= 18 && (가로 >= 17 || Svislá_pozice >= 17));
    }
    static int ukazatel_pixel(int 가로, int Svislá_pozice) {
        if (ukazatel_bit(가로, Svislá_pozice, ukazatel_tvar)) return 2;
        for (int vstupní_řádek = -1; vstupní_řádek <= 1; vstupní_řádek++) for (int přihrádka_položka = -1; přihrádka_položka <= 1; přihrádka_položka++)
            if (ukazatel_bit(가로 + přihrádka_položka, Svislá_pozice + vstupní_řádek, ukazatel_tvar)) return 1;
        return 0;
    }
    static void displej_pixel(int 가로, int Svislá_pozice, int 색) {
        int přihrádka_položka = 가로 - ukazatel_X, vstupní_řádek = Svislá_pozice - ukazatel_Y;
        if (ukazatel_tvar != 0 && přihrádka_položka >= 0 && vstupní_řádek >= 0 && přihrádka_položka < 21 && vstupní_řádek < 21) {
            ukazatel_Pozadí[vstupní_řádek * 21 + přihrádka_položka] = 색;
            int bod_HODNOTA = ukazatel_pixel(přihrádka_položka, vstupní_řádek); if (bod_HODNOTA != 0) 색 = bod_HODNOTA == 2 ? 0xffffff : 0x101010;
        }
        if (Panel.표시화소읽기(가로, Svislá_pozice) != 색) {
            Panel.zápis_displej_pixel(가로, Svislá_pozice, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void Dokončit() {
        if (합성중 == 0) return;
        for (int vstupní_řádek = VELKÁ_mez; vstupní_řádek < MALÁ_mez_HODNOTA; vstupní_řádek++) for (int přihrádka_položka = ZLEVA_mez_HODNOTA; přihrádka_položka < právo_mez_HODNOTA; přihrádka_položka++)
            displej_pixel(přihrádka_položka, vstupní_řádek, 완성그림[(vstupní_řádek - VELKÁ_mez) * 1920 + přihrádka_položka]);
        합성중 = 0;
    }
    public static int pixel(int 가로, int Svislá_pozice, int 색) {
        if (가로 < 0 || Svislá_pozice < 0 || 가로 >= 너비 || Svislá_pozice >= výška_HODNOTA) return 0;
        if (합성중 != 0) {
            if (가로 >= ZLEVA_mez_HODNOTA && 가로 < právo_mez_HODNOTA && Svislá_pozice >= VELKÁ_mez && Svislá_pozice < MALÁ_mez_HODNOTA)
                완성그림[(Svislá_pozice - VELKÁ_mez) * 1920 + 가로] = 색;
        } else displej_pixel(가로, Svislá_pozice, 색);
        return 0;
    }
    public static void obdélník_výplň(int 가로, int Svislá_pozice, int 폭, int délka_HODNOTA, int 색) {
        if (oříznout(가로, Svislá_pozice, 폭, délka_HODNOTA) == 0) return;
        가로 = 잘린범위[0]; Svislá_pozice = 잘린범위[1]; 폭 = 잘린범위[2]; délka_HODNOTA = 잘린범위[3];
        for (int vstupní_řádek = Svislá_pozice; vstupní_řádek < Svislá_pozice + délka_HODNOTA; vstupní_řádek++) for (int přihrádka_položka = 가로; přihrádka_položka < 가로 + 폭; přihrádka_položka++) {
            if (합성중 != 0) 완성그림[(vstupní_řádek - VELKÁ_mez) * 1920 + přihrádka_položka] = 색;
            else displej_pixel(přihrádka_položka, vstupní_řádek, 색);
        }
    }
    public static void ukazatel(int 가로, int Svislá_pozice, int tvar_HODNOTA) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (tvar_HODNOTA >= 2 ? 10 : 0), 새세로 = Svislá_pozice - (tvar_HODNOTA >= 2 ? 10 : 0);
        if (ukazatel_tvar == tvar_HODNOTA && ukazatel_X == 새가로 && ukazatel_Y == 새세로) return;
        if (ukazatel_tvar != 0) for (int vstupní_řádek = 0; vstupní_řádek < 21; vstupní_řádek++) for (int přihrádka_položka = 0; přihrádka_položka < 21; přihrádka_položka++) {
            int 가 = ukazatel_X + přihrádka_položka, 세 = ukazatel_Y + vstupní_řádek;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < výška_HODNOTA) Panel.zápis_displej_pixel(가, 세, ukazatel_Pozadí[vstupní_řádek * 21 + přihrádka_položka]);
        }
        ukazatel_tvar = tvar_HODNOTA; ukazatel_X = 새가로; ukazatel_Y = 새세로;
        if (tvar_HODNOTA != 0) for (int vstupní_řádek = 0; vstupní_řádek < 21; vstupní_řádek++) for (int přihrádka_položka = 0; přihrádka_položka < 21; přihrádka_položka++) {
            int 가 = ukazatel_X + přihrádka_položka, 세 = ukazatel_Y + vstupní_řádek;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < výška_HODNOTA) {
                ukazatel_Pozadí[vstupní_řádek * 21 + přihrádka_položka] = Panel.표시화소읽기(가, 세);
                int bod_HODNOTA = ukazatel_pixel(přihrádka_položka, vstupní_řádek); if (bod_HODNOTA != 0) Panel.zápis_displej_pixel(가, 세, bod_HODNOTA == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
