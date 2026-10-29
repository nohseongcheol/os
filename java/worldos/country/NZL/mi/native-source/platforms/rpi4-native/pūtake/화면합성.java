// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 화면 tapahi_uara·띠 합성·atatohu 밑그림을 관리한다. tūturu_raraunga 화면 Pūmahara_raraunga 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, 높이, 합성중, 왼경계, 위경계, 오른경계, 아래경계;
    static int 포인터가로, 포인터세로, atatohu_hanga;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] atatohu_Papamuri = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void Whakarite(int 폭, int roa_uara) {
        너비 = 폭; 높이 = roa_uara; 합성중 = 0; atatohu_hanga = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int 높이얻기() { return 높이; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int topenga_uara(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int Start_uara, int roa_uara) {
        if (Start_uara > 2147483647 - roa_uara) return 2147483647;
        return Start_uara + roa_uara;
    }
    public static int topenga(int 가로, int Poutū_tūranga, int 폭, int roa_uara) {
        if (너비 == 0 || 폭 <= 0 || roa_uara <= 0) return 0;
        int RIGHT = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(Poutū_tūranga, roa_uara);
        int 왼쪽 = 합성중 != 0 ? 왼경계 : 0, 위쪽 = 합성중 != 0 ? 위경계 : 0;
        int 최대가로 = 합성중 != 0 ? 오른경계 : 너비, 최대세로 = 합성중 != 0 ? 아래경계 : 높이;
        if (가로 < 왼쪽) 가로 = 왼쪽;
        if (Poutū_tūranga < 위쪽) Poutū_tūranga = 위쪽;
        if (RIGHT > 최대가로) RIGHT = 최대가로;
        if (아래쪽 > 최대세로) 아래쪽 = 최대세로;
        if (RIGHT <= 가로 || 아래쪽 <= Poutū_tūranga) return 0;
        잘린범위[0] = 가로; 잘린범위[1] = Poutū_tūranga;
        잘린범위[2] = RIGHT - 가로; 잘린범위[3] = 아래쪽 - Poutū_tūranga;
        return 1;
    }
    public static int whakahaere(int 가로, int Poutū_tūranga, int 폭, int roa_uara) {
        if (합성중 != 0 || roa_uara > 32 || topenga(가로, Poutū_tūranga, 폭, roa_uara) == 0) return 0;
        왼경계 = 잘린범위[0]; 위경계 = 잘린범위[1];
        오른경계 = 왼경계 + 잘린범위[2]; 아래경계 = 위경계 + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean atatohu_moka(int 가로, int Poutū_tūranga, int hanga_uara) {
        if (hanga_uara == 1) return 가로 >= 0 && 가로 <= Poutū_tūranga / 2 && Poutū_tūranga < 16;
        if (hanga_uara == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - Poutū_tūranga; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && Poutū_tūranga >= 2 && Poutū_tūranga <= 8 && (가로 <= 3 || Poutū_tūranga <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && Poutū_tūranga >= 12 && Poutū_tūranga <= 18 && (가로 >= 17 || Poutū_tūranga >= 17));
    }
    static int atatohu_pika(int 가로, int Poutū_tūranga) {
        if (atatohu_moka(가로, Poutū_tūranga, atatohu_hanga)) return 2;
        for (int hononga = -1; hononga <= 1; hononga++) for (int kāniwha_tāurunga = -1; kāniwha_tāurunga <= 1; kāniwha_tāurunga++)
            if (atatohu_moka(가로 + kāniwha_tāurunga, Poutū_tūranga + hononga, atatohu_hanga)) return 1;
        return 0;
    }
    static void whakaatu_pika(int 가로, int Poutū_tūranga, int 색) {
        int kāniwha_tāurunga = 가로 - 포인터가로, hononga = Poutū_tūranga - 포인터세로;
        if (atatohu_hanga != 0 && kāniwha_tāurunga >= 0 && hononga >= 0 && kāniwha_tāurunga < 21 && hononga < 21) {
            atatohu_Papamuri[hononga * 21 + kāniwha_tāurunga] = 색;
            int ira_uara = atatohu_pika(kāniwha_tāurunga, hononga); if (ira_uara != 0) 색 = ira_uara == 2 ? 0xffffff : 0x101010;
        }
        if (papa.표시화소읽기(가로, Poutū_tūranga) != 색) {
            papa.tuhi_whakaatu_pika(가로, Poutū_tūranga, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void Mutu() {
        if (합성중 == 0) return;
        for (int hononga = 위경계; hononga < 아래경계; hononga++) for (int kāniwha_tāurunga = 왼경계; kāniwha_tāurunga < 오른경계; kāniwha_tāurunga++)
            whakaatu_pika(kāniwha_tāurunga, hononga, 완성그림[(hononga - 위경계) * 1920 + kāniwha_tāurunga]);
        합성중 = 0;
    }
    public static int pika(int 가로, int Poutū_tūranga, int 색) {
        if (가로 < 0 || Poutū_tūranga < 0 || 가로 >= 너비 || Poutū_tūranga >= 높이) return 0;
        if (합성중 != 0) {
            if (가로 >= 왼경계 && 가로 < 오른경계 && Poutū_tūranga >= 위경계 && Poutū_tūranga < 아래경계)
                완성그림[(Poutū_tūranga - 위경계) * 1920 + 가로] = 색;
        } else whakaatu_pika(가로, Poutū_tūranga, 색);
        return 0;
    }
    public static void 사각그림(int 가로, int Poutū_tūranga, int 폭, int roa_uara, int 색) {
        if (topenga(가로, Poutū_tūranga, 폭, roa_uara) == 0) return;
        가로 = 잘린범위[0]; Poutū_tūranga = 잘린범위[1]; 폭 = 잘린범위[2]; roa_uara = 잘린범위[3];
        for (int hononga = Poutū_tūranga; hononga < Poutū_tūranga + roa_uara; hononga++) for (int kāniwha_tāurunga = 가로; kāniwha_tāurunga < 가로 + 폭; kāniwha_tāurunga++) {
            if (합성중 != 0) 완성그림[(hononga - 위경계) * 1920 + kāniwha_tāurunga] = 색;
            else whakaatu_pika(kāniwha_tāurunga, hononga, 색);
        }
    }
    public static void atatohu(int 가로, int Poutū_tūranga, int hanga_uara) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (hanga_uara >= 2 ? 10 : 0), 새세로 = Poutū_tūranga - (hanga_uara >= 2 ? 10 : 0);
        if (atatohu_hanga == hanga_uara && 포인터가로 == 새가로 && 포인터세로 == 새세로) return;
        if (atatohu_hanga != 0) for (int hononga = 0; hononga < 21; hononga++) for (int kāniwha_tāurunga = 0; kāniwha_tāurunga < 21; kāniwha_tāurunga++) {
            int 가 = 포인터가로 + kāniwha_tāurunga, 세 = 포인터세로 + hononga;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) papa.tuhi_whakaatu_pika(가, 세, atatohu_Papamuri[hononga * 21 + kāniwha_tāurunga]);
        }
        atatohu_hanga = hanga_uara; 포인터가로 = 새가로; 포인터세로 = 새세로;
        if (hanga_uara != 0) for (int hononga = 0; hononga < 21; hononga++) for (int kāniwha_tāurunga = 0; kāniwha_tāurunga < 21; kāniwha_tāurunga++) {
            int 가 = 포인터가로 + kāniwha_tāurunga, 세 = 포인터세로 + hononga;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) {
                atatohu_Papamuri[hononga * 21 + kāniwha_tāurunga] = papa.표시화소읽기(가, 세);
                int ira_uara = atatohu_pika(kāniwha_tāurunga, hononga); if (ira_uara != 0) papa.tuhi_whakaatu_pika(가, 세, ira_uara == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
