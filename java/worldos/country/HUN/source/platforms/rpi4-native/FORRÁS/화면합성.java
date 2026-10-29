// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 화면 vágás_ÉRTÉK·띠 합성·mutató 밑그림을 관리한다. tényleges_adat 화면 Memória_adat 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, 높이, 합성중, BAL_határ_ÉRTÉK, NAGYBETŰS_határ, jog_határ_ÉRTÉK, KISBETŰ_határ_ÉRTÉK;
    static int mutató_X, mutató_Y, mutató_alakzat;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] mutató_Háttér = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void Előkészítés(int 폭, int hossz_ÉRTÉK) {
        너비 = 폭; 높이 = hossz_ÉRTÉK; 합성중 = 0; mutató_alakzat = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int 높이얻기() { return 높이; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int klip_ÉRTÉK(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int START_ÉRTÉK, int hossz_ÉRTÉK) {
        if (START_ÉRTÉK > 2147483647 - hossz_ÉRTÉK) return 2147483647;
        return START_ÉRTÉK + hossz_ÉRTÉK;
    }
    public static int klip(int 가로, int szektor_pozíció, int 폭, int hossz_ÉRTÉK) {
        if (너비 == 0 || 폭 <= 0 || hossz_ÉRTÉK <= 0) return 0;
        int jog = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(szektor_pozíció, hossz_ÉRTÉK);
        int 왼쪽 = 합성중 != 0 ? BAL_határ_ÉRTÉK : 0, 위쪽 = 합성중 != 0 ? NAGYBETŰS_határ : 0;
        int 최대가로 = 합성중 != 0 ? jog_határ_ÉRTÉK : 너비, 최대세로 = 합성중 != 0 ? KISBETŰ_határ_ÉRTÉK : 높이;
        if (가로 < 왼쪽) 가로 = 왼쪽;
        if (szektor_pozíció < 위쪽) szektor_pozíció = 위쪽;
        if (jog > 최대가로) jog = 최대가로;
        if (아래쪽 > 최대세로) 아래쪽 = 최대세로;
        if (jog <= 가로 || 아래쪽 <= szektor_pozíció) return 0;
        잘린범위[0] = 가로; 잘린범위[1] = szektor_pozíció;
        잘린범위[2] = jog - 가로; 잘린범위[3] = 아래쪽 - szektor_pozíció;
        return 1;
    }
    public static int Futtatás(int 가로, int szektor_pozíció, int 폭, int hossz_ÉRTÉK) {
        if (합성중 != 0 || hossz_ÉRTÉK > 32 || klip(가로, szektor_pozíció, 폭, hossz_ÉRTÉK) == 0) return 0;
        BAL_határ_ÉRTÉK = 잘린범위[0]; NAGYBETŰS_határ = 잘린범위[1];
        jog_határ_ÉRTÉK = BAL_határ_ÉRTÉK + 잘린범위[2]; KISBETŰ_határ_ÉRTÉK = NAGYBETŰS_határ + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean mutató_bit(int 가로, int szektor_pozíció, int alakzat_ÉRTÉK) {
        if (alakzat_ÉRTÉK == 1) return 가로 >= 0 && 가로 <= szektor_pozíció / 2 && szektor_pozíció < 16;
        if (alakzat_ÉRTÉK == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - szektor_pozíció; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && szektor_pozíció >= 2 && szektor_pozíció <= 8 && (가로 <= 3 || szektor_pozíció <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && szektor_pozíció >= 12 && szektor_pozíció <= 18 && (가로 >= 17 || szektor_pozíció >= 17));
    }
    static int mutató_képpont(int 가로, int szektor_pozíció) {
        if (mutató_bit(가로, szektor_pozíció, mutató_alakzat)) return 2;
        for (int Vonal = -1; Vonal <= 1; Vonal++) for (int tárolóhely_bejegyzés = -1; tárolóhely_bejegyzés <= 1; tárolóhely_bejegyzés++)
            if (mutató_bit(가로 + tárolóhely_bejegyzés, szektor_pozíció + Vonal, mutató_alakzat)) return 1;
        return 0;
    }
    static void kijelző_képpont(int 가로, int szektor_pozíció, int 색) {
        int tárolóhely_bejegyzés = 가로 - mutató_X, Vonal = szektor_pozíció - mutató_Y;
        if (mutató_alakzat != 0 && tárolóhely_bejegyzés >= 0 && Vonal >= 0 && tárolóhely_bejegyzés < 21 && Vonal < 21) {
            mutató_Háttér[Vonal * 21 + tárolóhely_bejegyzés] = 색;
            int pont_ÉRTÉK = mutató_képpont(tárolóhely_bejegyzés, Vonal); if (pont_ÉRTÉK != 0) 색 = pont_ÉRTÉK == 2 ? 0xffffff : 0x101010;
        }
        if (fal.표시화소읽기(가로, szektor_pozíció) != 색) {
            fal.ír_kijelző_képpont(가로, szektor_pozíció, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void Befejezés() {
        if (합성중 == 0) return;
        for (int Vonal = NAGYBETŰS_határ; Vonal < KISBETŰ_határ_ÉRTÉK; Vonal++) for (int tárolóhely_bejegyzés = BAL_határ_ÉRTÉK; tárolóhely_bejegyzés < jog_határ_ÉRTÉK; tárolóhely_bejegyzés++)
            kijelző_képpont(tárolóhely_bejegyzés, Vonal, 완성그림[(Vonal - NAGYBETŰS_határ) * 1920 + tárolóhely_bejegyzés]);
        합성중 = 0;
    }
    public static int képpont(int 가로, int szektor_pozíció, int 색) {
        if (가로 < 0 || szektor_pozíció < 0 || 가로 >= 너비 || szektor_pozíció >= 높이) return 0;
        if (합성중 != 0) {
            if (가로 >= BAL_határ_ÉRTÉK && 가로 < jog_határ_ÉRTÉK && szektor_pozíció >= NAGYBETŰS_határ && szektor_pozíció < KISBETŰ_határ_ÉRTÉK)
                완성그림[(szektor_pozíció - NAGYBETŰS_határ) * 1920 + 가로] = 색;
        } else kijelző_képpont(가로, szektor_pozíció, 색);
        return 0;
    }
    public static void téglalap_kitöltés(int 가로, int szektor_pozíció, int 폭, int hossz_ÉRTÉK, int 색) {
        if (klip(가로, szektor_pozíció, 폭, hossz_ÉRTÉK) == 0) return;
        가로 = 잘린범위[0]; szektor_pozíció = 잘린범위[1]; 폭 = 잘린범위[2]; hossz_ÉRTÉK = 잘린범위[3];
        for (int Vonal = szektor_pozíció; Vonal < szektor_pozíció + hossz_ÉRTÉK; Vonal++) for (int tárolóhely_bejegyzés = 가로; tárolóhely_bejegyzés < 가로 + 폭; tárolóhely_bejegyzés++) {
            if (합성중 != 0) 완성그림[(Vonal - NAGYBETŰS_határ) * 1920 + tárolóhely_bejegyzés] = 색;
            else kijelző_képpont(tárolóhely_bejegyzés, Vonal, 색);
        }
    }
    public static void mutató(int 가로, int szektor_pozíció, int alakzat_ÉRTÉK) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (alakzat_ÉRTÉK >= 2 ? 10 : 0), 새세로 = szektor_pozíció - (alakzat_ÉRTÉK >= 2 ? 10 : 0);
        if (mutató_alakzat == alakzat_ÉRTÉK && mutató_X == 새가로 && mutató_Y == 새세로) return;
        if (mutató_alakzat != 0) for (int Vonal = 0; Vonal < 21; Vonal++) for (int tárolóhely_bejegyzés = 0; tárolóhely_bejegyzés < 21; tárolóhely_bejegyzés++) {
            int 가 = mutató_X + tárolóhely_bejegyzés, 세 = mutató_Y + Vonal;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) fal.ír_kijelző_képpont(가, 세, mutató_Háttér[Vonal * 21 + tárolóhely_bejegyzés]);
        }
        mutató_alakzat = alakzat_ÉRTÉK; mutató_X = 새가로; mutató_Y = 새세로;
        if (alakzat_ÉRTÉK != 0) for (int Vonal = 0; Vonal < 21; Vonal++) for (int tárolóhely_bejegyzés = 0; tárolóhely_bejegyzés < 21; tárolóhely_bejegyzés++) {
            int 가 = mutató_X + tárolóhely_bejegyzés, 세 = mutató_Y + Vonal;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) {
                mutató_Háttér[Vonal * 21 + tárolóhely_bejegyzés] = fal.표시화소읽기(가, 세);
                int pont_ÉRTÉK = mutató_képpont(tárolóhely_bejegyzés, Vonal); if (pont_ÉRTÉK != 0) fal.ír_kijelző_képpont(가, 세, pont_ÉRTÉK == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
