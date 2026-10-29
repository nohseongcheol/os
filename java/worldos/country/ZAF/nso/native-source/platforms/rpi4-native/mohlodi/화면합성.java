// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 화면 sega_boleng·띠 합성·sešupi 밑그림을 관리한다. kgonthe_data 화면 memori_data 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, 높이, 합성중, 왼경계, 위경계, 오른경계, 아래경계;
    static int 포인터가로, 포인터세로, sešupi_sebopego;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] sešupi_Bokamorago = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void Lokišetša(int 폭, int botelele_boleng) {
        너비 = 폭; 높이 = botelele_boleng; 합성중 = 0; sešupi_sebopego = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int 높이얻기() { return 높이; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int setsopolwa_boleng(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int Thomišo_boleng, int botelele_boleng) {
        if (Thomišo_boleng > 2147483647 - botelele_boleng) return 2147483647;
        return Thomišo_boleng + botelele_boleng;
    }
    public static int setsopolwa(int 가로, int 세로, int 폭, int botelele_boleng) {
        if (너비 == 0 || 폭 <= 0 || botelele_boleng <= 0) return 0;
        int 오른쪽 = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(세로, botelele_boleng);
        int 왼쪽 = 합성중 != 0 ? 왼경계 : 0, 위쪽 = 합성중 != 0 ? 위경계 : 0;
        int 최대가로 = 합성중 != 0 ? 오른경계 : 너비, 최대세로 = 합성중 != 0 ? 아래경계 : 높이;
        if (가로 < 왼쪽) 가로 = 왼쪽;
        if (세로 < 위쪽) 세로 = 위쪽;
        if (오른쪽 > 최대가로) 오른쪽 = 최대가로;
        if (아래쪽 > 최대세로) 아래쪽 = 최대세로;
        if (오른쪽 <= 가로 || 아래쪽 <= 세로) return 0;
        잘린범위[0] = 가로; 잘린범위[1] = 세로;
        잘린범위[2] = 오른쪽 - 가로; 잘린범위[3] = 아래쪽 - 세로;
        return 1;
    }
    public static int Diriša(int 가로, int 세로, int 폭, int botelele_boleng) {
        if (합성중 != 0 || botelele_boleng > 32 || setsopolwa(가로, 세로, 폭, botelele_boleng) == 0) return 0;
        왼경계 = 잘린범위[0]; 위경계 = 잘린범위[1];
        오른경계 = 왼경계 + 잘린범위[2]; 아래경계 = 위경계 + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean sešupi_paente(int 가로, int 세로, int sebopego_boleng) {
        if (sebopego_boleng == 1) return 가로 >= 0 && 가로 <= 세로 / 2 && 세로 < 16;
        if (sebopego_boleng == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - 세로; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && 세로 >= 2 && 세로 <= 8 && (가로 <= 3 || 세로 <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && 세로 >= 12 && 세로 <= 18 && (가로 >= 17 || 세로 >= 17));
    }
    static int sešupi_phele(int 가로, int 세로) {
        if (sešupi_paente(가로, 세로, sešupi_sebopego)) return 2;
        for (int mothaladi = -1; mothaladi <= 1; mothaladi++) for (int sekgobana_go_tsenya_tshedimošo = -1; sekgobana_go_tsenya_tshedimošo <= 1; sekgobana_go_tsenya_tshedimošo++)
            if (sešupi_paente(가로 + sekgobana_go_tsenya_tshedimošo, 세로 + mothaladi, sešupi_sebopego)) return 1;
        return 0;
    }
    static void bontšha_phele(int 가로, int 세로, int 색) {
        int sekgobana_go_tsenya_tshedimošo = 가로 - 포인터가로, mothaladi = 세로 - 포인터세로;
        if (sešupi_sebopego != 0 && sekgobana_go_tsenya_tshedimošo >= 0 && mothaladi >= 0 && sekgobana_go_tsenya_tshedimošo < 21 && mothaladi < 21) {
            sešupi_Bokamorago[mothaladi * 21 + sekgobana_go_tsenya_tshedimošo] = 색;
            int ntlha_boleng = sešupi_phele(sekgobana_go_tsenya_tshedimošo, mothaladi); if (ntlha_boleng != 0) 색 = ntlha_boleng == 2 ? 0xffffff : 0x101010;
        }
        if (보드.표시화소읽기(가로, 세로) != 색) {
            보드.ngwala_bontšha_phele(가로, 세로, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void Fetša() {
        if (합성중 == 0) return;
        for (int mothaladi = 위경계; mothaladi < 아래경계; mothaladi++) for (int sekgobana_go_tsenya_tshedimošo = 왼경계; sekgobana_go_tsenya_tshedimošo < 오른경계; sekgobana_go_tsenya_tshedimošo++)
            bontšha_phele(sekgobana_go_tsenya_tshedimošo, mothaladi, 완성그림[(mothaladi - 위경계) * 1920 + sekgobana_go_tsenya_tshedimošo]);
        합성중 = 0;
    }
    public static int phele(int 가로, int 세로, int 색) {
        if (가로 < 0 || 세로 < 0 || 가로 >= 너비 || 세로 >= 높이) return 0;
        if (합성중 != 0) {
            if (가로 >= 왼경계 && 가로 < 오른경계 && 세로 >= 위경계 && 세로 < 아래경계)
                완성그림[(세로 - 위경계) * 1920 + 가로] = 색;
        } else bontšha_phele(가로, 세로, 색);
        return 0;
    }
    public static void 사각그림(int 가로, int 세로, int 폭, int botelele_boleng, int 색) {
        if (setsopolwa(가로, 세로, 폭, botelele_boleng) == 0) return;
        가로 = 잘린범위[0]; 세로 = 잘린범위[1]; 폭 = 잘린범위[2]; botelele_boleng = 잘린범위[3];
        for (int mothaladi = 세로; mothaladi < 세로 + botelele_boleng; mothaladi++) for (int sekgobana_go_tsenya_tshedimošo = 가로; sekgobana_go_tsenya_tshedimošo < 가로 + 폭; sekgobana_go_tsenya_tshedimošo++) {
            if (합성중 != 0) 완성그림[(mothaladi - 위경계) * 1920 + sekgobana_go_tsenya_tshedimošo] = 색;
            else bontšha_phele(sekgobana_go_tsenya_tshedimošo, mothaladi, 색);
        }
    }
    public static void sešupi(int 가로, int 세로, int sebopego_boleng) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (sebopego_boleng >= 2 ? 10 : 0), 새세로 = 세로 - (sebopego_boleng >= 2 ? 10 : 0);
        if (sešupi_sebopego == sebopego_boleng && 포인터가로 == 새가로 && 포인터세로 == 새세로) return;
        if (sešupi_sebopego != 0) for (int mothaladi = 0; mothaladi < 21; mothaladi++) for (int sekgobana_go_tsenya_tshedimošo = 0; sekgobana_go_tsenya_tshedimošo < 21; sekgobana_go_tsenya_tshedimošo++) {
            int 가 = 포인터가로 + sekgobana_go_tsenya_tshedimošo, 세 = 포인터세로 + mothaladi;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) 보드.ngwala_bontšha_phele(가, 세, sešupi_Bokamorago[mothaladi * 21 + sekgobana_go_tsenya_tshedimošo]);
        }
        sešupi_sebopego = sebopego_boleng; 포인터가로 = 새가로; 포인터세로 = 새세로;
        if (sebopego_boleng != 0) for (int mothaladi = 0; mothaladi < 21; mothaladi++) for (int sekgobana_go_tsenya_tshedimošo = 0; sekgobana_go_tsenya_tshedimošo < 21; sekgobana_go_tsenya_tshedimošo++) {
            int 가 = 포인터가로 + sekgobana_go_tsenya_tshedimošo, 세 = 포인터세로 + mothaladi;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) {
                sešupi_Bokamorago[mothaladi * 21 + sekgobana_go_tsenya_tshedimošo] = 보드.표시화소읽기(가, 세);
                int ntlha_boleng = sešupi_phele(sekgobana_go_tsenya_tshedimošo, mothaladi); if (ntlha_boleng != 0) 보드.ngwala_bontšha_phele(가, 세, ntlha_boleng == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
