// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** scherm knippen_WAARDE·띠 합성·wijzer 밑그림을 관리한다. werkelijk_gegevens scherm Geheugen_gegevens 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, hoogte_WAARDE, 합성중, LINKS_grens_WAARDE, HOOFDLETTERS_grens, recht_grens_WAARDE, KLEINE_LETTERS_grens_WAARDE;
    static int wijzer_X, wijzer_Y, wijzer_vorm;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] wijzer_Achtergrond = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void Bereid_voor(int 폭, int tijdsduur_WAARDE) {
        너비 = 폭; hoogte_WAARDE = tijdsduur_WAARDE; 합성중 = 0; wijzer_vorm = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int ophalen_hoogte() { return hoogte_WAARDE; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int clip_WAARDE(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int START_WAARDE, int tijdsduur_WAARDE) {
        if (START_WAARDE > 2147483647 - tijdsduur_WAARDE) return 2147483647;
        return START_WAARDE + tijdsduur_WAARDE;
    }
    public static int clip(int 가로, int Verticaal_functie, int 폭, int tijdsduur_WAARDE) {
        if (너비 == 0 || 폭 <= 0 || tijdsduur_WAARDE <= 0) return 0;
        int recht = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(Verticaal_functie, tijdsduur_WAARDE);
        int 왼쪽 = 합성중 != 0 ? LINKS_grens_WAARDE : 0, 위쪽 = 합성중 != 0 ? HOOFDLETTERS_grens : 0;
        int 최대가로 = 합성중 != 0 ? recht_grens_WAARDE : 너비, 최대세로 = 합성중 != 0 ? KLEINE_LETTERS_grens_WAARDE : hoogte_WAARDE;
        if (가로 < 왼쪽) 가로 = 왼쪽;
        if (Verticaal_functie < 위쪽) Verticaal_functie = 위쪽;
        if (recht > 최대가로) recht = 최대가로;
        if (아래쪽 > 최대세로) 아래쪽 = 최대세로;
        if (recht <= 가로 || 아래쪽 <= Verticaal_functie) return 0;
        잘린범위[0] = 가로; 잘린범위[1] = Verticaal_functie;
        잘린범위[2] = recht - 가로; 잘린범위[3] = 아래쪽 - Verticaal_functie;
        return 1;
    }
    public static int starten(int 가로, int Verticaal_functie, int 폭, int tijdsduur_WAARDE) {
        if (합성중 != 0 || tijdsduur_WAARDE > 32 || clip(가로, Verticaal_functie, 폭, tijdsduur_WAARDE) == 0) return 0;
        LINKS_grens_WAARDE = 잘린범위[0]; HOOFDLETTERS_grens = 잘린범위[1];
        recht_grens_WAARDE = LINKS_grens_WAARDE + 잘린범위[2]; KLEINE_LETTERS_grens_WAARDE = HOOFDLETTERS_grens + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean wijzer_bit(int 가로, int Verticaal_functie, int vorm_WAARDE) {
        if (vorm_WAARDE == 1) return 가로 >= 0 && 가로 <= Verticaal_functie / 2 && Verticaal_functie < 16;
        if (vorm_WAARDE == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - Verticaal_functie; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && Verticaal_functie >= 2 && Verticaal_functie <= 8 && (가로 <= 3 || Verticaal_functie <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && Verticaal_functie >= 12 && Verticaal_functie <= 18 && (가로 >= 17 || Verticaal_functie >= 17));
    }
    static int wijzer_pixel(int 가로, int Verticaal_functie) {
        if (wijzer_bit(가로, Verticaal_functie, wijzer_vorm)) return 2;
        for (int invoerregel = -1; invoerregel <= 1; invoerregel++) for (int sleuf_invoer = -1; sleuf_invoer <= 1; sleuf_invoer++)
            if (wijzer_bit(가로 + sleuf_invoer, Verticaal_functie + invoerregel, wijzer_vorm)) return 1;
        return 0;
    }
    static void weergeven_pixel(int 가로, int Verticaal_functie, int 색) {
        int sleuf_invoer = 가로 - wijzer_X, invoerregel = Verticaal_functie - wijzer_Y;
        if (wijzer_vorm != 0 && sleuf_invoer >= 0 && invoerregel >= 0 && sleuf_invoer < 21 && invoerregel < 21) {
            wijzer_Achtergrond[invoerregel * 21 + sleuf_invoer] = 색;
            int punt_WAARDE = wijzer_pixel(sleuf_invoer, invoerregel); if (punt_WAARDE != 0) 색 = punt_WAARDE == 2 ? 0xffffff : 0x101010;
        }
        if (Bord.표시화소읽기(가로, Verticaal_functie) != 색) {
            Bord.schrijven_weergeven_pixel(가로, Verticaal_functie, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void Voltooien() {
        if (합성중 == 0) return;
        for (int invoerregel = HOOFDLETTERS_grens; invoerregel < KLEINE_LETTERS_grens_WAARDE; invoerregel++) for (int sleuf_invoer = LINKS_grens_WAARDE; sleuf_invoer < recht_grens_WAARDE; sleuf_invoer++)
            weergeven_pixel(sleuf_invoer, invoerregel, 완성그림[(invoerregel - HOOFDLETTERS_grens) * 1920 + sleuf_invoer]);
        합성중 = 0;
    }
    public static int pixel(int 가로, int Verticaal_functie, int 색) {
        if (가로 < 0 || Verticaal_functie < 0 || 가로 >= 너비 || Verticaal_functie >= hoogte_WAARDE) return 0;
        if (합성중 != 0) {
            if (가로 >= LINKS_grens_WAARDE && 가로 < recht_grens_WAARDE && Verticaal_functie >= HOOFDLETTERS_grens && Verticaal_functie < KLEINE_LETTERS_grens_WAARDE)
                완성그림[(Verticaal_functie - HOOFDLETTERS_grens) * 1920 + 가로] = 색;
        } else weergeven_pixel(가로, Verticaal_functie, 색);
        return 0;
    }
    public static void rechthoek_vullen(int 가로, int Verticaal_functie, int 폭, int tijdsduur_WAARDE, int 색) {
        if (clip(가로, Verticaal_functie, 폭, tijdsduur_WAARDE) == 0) return;
        가로 = 잘린범위[0]; Verticaal_functie = 잘린범위[1]; 폭 = 잘린범위[2]; tijdsduur_WAARDE = 잘린범위[3];
        for (int invoerregel = Verticaal_functie; invoerregel < Verticaal_functie + tijdsduur_WAARDE; invoerregel++) for (int sleuf_invoer = 가로; sleuf_invoer < 가로 + 폭; sleuf_invoer++) {
            if (합성중 != 0) 완성그림[(invoerregel - HOOFDLETTERS_grens) * 1920 + sleuf_invoer] = 색;
            else weergeven_pixel(sleuf_invoer, invoerregel, 색);
        }
    }
    public static void wijzer(int 가로, int Verticaal_functie, int vorm_WAARDE) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (vorm_WAARDE >= 2 ? 10 : 0), 새세로 = Verticaal_functie - (vorm_WAARDE >= 2 ? 10 : 0);
        if (wijzer_vorm == vorm_WAARDE && wijzer_X == 새가로 && wijzer_Y == 새세로) return;
        if (wijzer_vorm != 0) for (int invoerregel = 0; invoerregel < 21; invoerregel++) for (int sleuf_invoer = 0; sleuf_invoer < 21; sleuf_invoer++) {
            int 가 = wijzer_X + sleuf_invoer, 세 = wijzer_Y + invoerregel;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < hoogte_WAARDE) Bord.schrijven_weergeven_pixel(가, 세, wijzer_Achtergrond[invoerregel * 21 + sleuf_invoer]);
        }
        wijzer_vorm = vorm_WAARDE; wijzer_X = 새가로; wijzer_Y = 새세로;
        if (vorm_WAARDE != 0) for (int invoerregel = 0; invoerregel < 21; invoerregel++) for (int sleuf_invoer = 0; sleuf_invoer < 21; sleuf_invoer++) {
            int 가 = wijzer_X + sleuf_invoer, 세 = wijzer_Y + invoerregel;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < hoogte_WAARDE) {
                wijzer_Achtergrond[invoerregel * 21 + sleuf_invoer] = Bord.표시화소읽기(가, 세);
                int punt_WAARDE = wijzer_pixel(sleuf_invoer, invoerregel); if (punt_WAARDE != 0) Bord.schrijven_weergeven_pixel(가, 세, punt_WAARDE == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
