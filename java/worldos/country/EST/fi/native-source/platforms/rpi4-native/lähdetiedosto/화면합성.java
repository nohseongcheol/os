// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 화면 leikata_ARVO_4601577b·띠 합성·osoitin 밑그림을 관리한다. todellinen_data 화면 Muisti_data 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, 높이, 합성중, VASEN_rajattu_alue_ARVO, ISOT_rajattu_alue, OIKEA_rajattu_alue_ARVO, PIENET_rajattu_alue_ARVO;
    static int osoitin_X, osoitin_Y, osoitin_muoto;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] osoitin_Tausta = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void Valmistele(int 폭, int kesto_ARVO) {
        너비 = 폭; 높이 = kesto_ARVO; 합성중 = 0; osoitin_muoto = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int 높이얻기() { return 높이; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int leikata_ARVO(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int alku_ARVO, int kesto_ARVO) {
        if (alku_ARVO > 2147483647 - kesto_ARVO) return 2147483647;
        return alku_ARVO + kesto_ARVO;
    }
    public static int leikata(int 가로, int toimiala_toimi, int 폭, int kesto_ARVO) {
        if (너비 == 0 || 폭 <= 0 || kesto_ARVO <= 0) return 0;
        int OIKEA = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(toimiala_toimi, kesto_ARVO);
        int 왼쪽 = 합성중 != 0 ? VASEN_rajattu_alue_ARVO : 0, 위쪽 = 합성중 != 0 ? ISOT_rajattu_alue : 0;
        int 최대가로 = 합성중 != 0 ? OIKEA_rajattu_alue_ARVO : 너비, 최대세로 = 합성중 != 0 ? PIENET_rajattu_alue_ARVO : 높이;
        if (가로 < 왼쪽) 가로 = 왼쪽;
        if (toimiala_toimi < 위쪽) toimiala_toimi = 위쪽;
        if (OIKEA > 최대가로) OIKEA = 최대가로;
        if (아래쪽 > 최대세로) 아래쪽 = 최대세로;
        if (OIKEA <= 가로 || 아래쪽 <= toimiala_toimi) return 0;
        잘린범위[0] = 가로; 잘린범위[1] = toimiala_toimi;
        잘린범위[2] = OIKEA - 가로; 잘린범위[3] = 아래쪽 - toimiala_toimi;
        return 1;
    }
    public static int Suorita_2(int 가로, int toimiala_toimi, int 폭, int kesto_ARVO) {
        if (합성중 != 0 || kesto_ARVO > 32 || leikata(가로, toimiala_toimi, 폭, kesto_ARVO) == 0) return 0;
        VASEN_rajattu_alue_ARVO = 잘린범위[0]; ISOT_rajattu_alue = 잘린범위[1];
        OIKEA_rajattu_alue_ARVO = VASEN_rajattu_alue_ARVO + 잘린범위[2]; PIENET_rajattu_alue_ARVO = ISOT_rajattu_alue + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean osoitin_bitti(int 가로, int toimiala_toimi, int muoto_ARVO_f1cd655a) {
        if (muoto_ARVO_f1cd655a == 1) return 가로 >= 0 && 가로 <= toimiala_toimi / 2 && toimiala_toimi < 16;
        if (muoto_ARVO_f1cd655a == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - toimiala_toimi; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && toimiala_toimi >= 2 && toimiala_toimi <= 8 && (가로 <= 3 || toimiala_toimi <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && toimiala_toimi >= 12 && toimiala_toimi <= 18 && (가로 >= 17 || toimiala_toimi >= 17));
    }
    static int osoitin_kuvapiste(int 가로, int toimiala_toimi) {
        if (osoitin_bitti(가로, toimiala_toimi, osoitin_muoto)) return 2;
        for (int syöterivi = -1; syöterivi <= 1; syöterivi++) for (int paikka_merkintä = -1; paikka_merkintä <= 1; paikka_merkintä++)
            if (osoitin_bitti(가로 + paikka_merkintä, toimiala_toimi + syöterivi, osoitin_muoto)) return 1;
        return 0;
    }
    static void näyttö_kuvapiste(int 가로, int toimiala_toimi, int 색) {
        int paikka_merkintä = 가로 - osoitin_X, syöterivi = toimiala_toimi - osoitin_Y;
        if (osoitin_muoto != 0 && paikka_merkintä >= 0 && syöterivi >= 0 && paikka_merkintä < 21 && syöterivi < 21) {
            osoitin_Tausta[syöterivi * 21 + paikka_merkintä] = 색;
            int piste_ARVO = osoitin_kuvapiste(paikka_merkintä, syöterivi); if (piste_ARVO != 0) 색 = piste_ARVO == 2 ? 0xffffff : 0x101010;
        }
        if (Taulu.lukea_näyttö_kuvapiste(가로, toimiala_toimi) != 색) {
            Taulu.kirjoitus_näyttö_kuvapiste(가로, toimiala_toimi, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void loppu() {
        if (합성중 == 0) return;
        for (int syöterivi = ISOT_rajattu_alue; syöterivi < PIENET_rajattu_alue_ARVO; syöterivi++) for (int paikka_merkintä = VASEN_rajattu_alue_ARVO; paikka_merkintä < OIKEA_rajattu_alue_ARVO; paikka_merkintä++)
            näyttö_kuvapiste(paikka_merkintä, syöterivi, 완성그림[(syöterivi - ISOT_rajattu_alue) * 1920 + paikka_merkintä]);
        합성중 = 0;
    }
    public static int kuvapiste(int 가로, int toimiala_toimi, int 색) {
        if (가로 < 0 || toimiala_toimi < 0 || 가로 >= 너비 || toimiala_toimi >= 높이) return 0;
        if (합성중 != 0) {
            if (가로 >= VASEN_rajattu_alue_ARVO && 가로 < OIKEA_rajattu_alue_ARVO && toimiala_toimi >= ISOT_rajattu_alue && toimiala_toimi < PIENET_rajattu_alue_ARVO)
                완성그림[(toimiala_toimi - ISOT_rajattu_alue) * 1920 + 가로] = 색;
        } else näyttö_kuvapiste(가로, toimiala_toimi, 색);
        return 0;
    }
    public static void suorakulmio_täyttö(int 가로, int toimiala_toimi, int 폭, int kesto_ARVO, int 색) {
        if (leikata(가로, toimiala_toimi, 폭, kesto_ARVO) == 0) return;
        가로 = 잘린범위[0]; toimiala_toimi = 잘린범위[1]; 폭 = 잘린범위[2]; kesto_ARVO = 잘린범위[3];
        for (int syöterivi = toimiala_toimi; syöterivi < toimiala_toimi + kesto_ARVO; syöterivi++) for (int paikka_merkintä = 가로; paikka_merkintä < 가로 + 폭; paikka_merkintä++) {
            if (합성중 != 0) 완성그림[(syöterivi - ISOT_rajattu_alue) * 1920 + paikka_merkintä] = 색;
            else näyttö_kuvapiste(paikka_merkintä, syöterivi, 색);
        }
    }
    public static void osoitin(int 가로, int toimiala_toimi, int muoto_ARVO_f1cd655a) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (muoto_ARVO_f1cd655a >= 2 ? 10 : 0), 새세로 = toimiala_toimi - (muoto_ARVO_f1cd655a >= 2 ? 10 : 0);
        if (osoitin_muoto == muoto_ARVO_f1cd655a && osoitin_X == 새가로 && osoitin_Y == 새세로) return;
        if (osoitin_muoto != 0) for (int syöterivi = 0; syöterivi < 21; syöterivi++) for (int paikka_merkintä = 0; paikka_merkintä < 21; paikka_merkintä++) {
            int 가 = osoitin_X + paikka_merkintä, 세 = osoitin_Y + syöterivi;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) Taulu.kirjoitus_näyttö_kuvapiste(가, 세, osoitin_Tausta[syöterivi * 21 + paikka_merkintä]);
        }
        osoitin_muoto = muoto_ARVO_f1cd655a; osoitin_X = 새가로; osoitin_Y = 새세로;
        if (muoto_ARVO_f1cd655a != 0) for (int syöterivi = 0; syöterivi < 21; syöterivi++) for (int paikka_merkintä = 0; paikka_merkintä < 21; paikka_merkintä++) {
            int 가 = osoitin_X + paikka_merkintä, 세 = osoitin_Y + syöterivi;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) {
                osoitin_Tausta[syöterivi * 21 + paikka_merkintä] = Taulu.lukea_näyttö_kuvapiste(가, 세);
                int piste_ARVO = osoitin_kuvapiste(paikka_merkintä, syöterivi); if (piste_ARVO != 0) Taulu.kirjoitus_näyttö_kuvapiste(가, 세, piste_ARVO == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
