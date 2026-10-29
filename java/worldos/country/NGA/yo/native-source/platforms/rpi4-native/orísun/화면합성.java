// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 화면 gé_kúrò_iye·띠 합성·ìtọ́ka 밑그림을 관리한다. gangan_détà 화면 ibi_ìpamọ́_détà 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, 높이, 합성중, 왼경계, 위경계, 오른경계, 아래경계;
    static int 포인터가로, 포인터세로, ìtọ́ka_ìrísí;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] ìtọ́ka_Àgbétẹ́lẹ̀ = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void gbaradì(int 폭, int gígùn_iye) {
        너비 = 폭; 높이 = gígùn_iye; 합성중 = 0; ìtọ́ka_ìrísí = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int 높이얻기() { return 높이; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int ní_ṣókí_iye(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int bẹ̀rẹ̀_iye, int gígùn_iye) {
        if (bẹ̀rẹ̀_iye > 2147483647 - gígùn_iye) return 2147483647;
        return bẹ̀rẹ̀_iye + gígùn_iye;
    }
    public static int ní_ṣókí(int 가로, int 세로, int 폭, int gígùn_iye) {
        if (너비 == 0 || 폭 <= 0 || gígùn_iye <= 0) return 0;
        int 오른쪽 = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(세로, gígùn_iye);
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
    public static int Rọ́ọ̀nù(int 가로, int 세로, int 폭, int gígùn_iye) {
        if (합성중 != 0 || gígùn_iye > 32 || ní_ṣókí(가로, 세로, 폭, gígùn_iye) == 0) return 0;
        왼경계 = 잘린범위[0]; 위경계 = 잘린범위[1];
        오른경계 = 왼경계 + 잘린범위[2]; 아래경계 = 위경계 + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean ìtọ́ka_bíìtì(int 가로, int 세로, int ìrísí_iye) {
        if (ìrísí_iye == 1) return 가로 >= 0 && 가로 <= 세로 / 2 && 세로 < 16;
        if (ìrísí_iye == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - 세로; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && 세로 >= 2 && 세로 <= 8 && (가로 <= 3 || 세로 <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && 세로 >= 12 && 세로 <= 18 && (가로 >= 17 || 세로 >= 17));
    }
    static int ìtọ́ka_píkísẹ̀(int 가로, int 세로) {
        if (ìtọ́ka_bíìtì(가로, 세로, ìtọ́ka_ìrísí)) return 2;
        for (int ìlà = -1; ìlà <= 1; ìlà++) for (int ààyè_ìfàyọkàsí_ìgbéwọlé = -1; ààyè_ìfàyọkàsí_ìgbéwọlé <= 1; ààyè_ìfàyọkàsí_ìgbéwọlé++)
            if (ìtọ́ka_bíìtì(가로 + ààyè_ìfàyọkàsí_ìgbéwọlé, 세로 + ìlà, ìtọ́ka_ìrísí)) return 1;
        return 0;
    }
    static void ṣàfihàn_píkísẹ̀(int 가로, int 세로, int 색) {
        int ààyè_ìfàyọkàsí_ìgbéwọlé = 가로 - 포인터가로, ìlà = 세로 - 포인터세로;
        if (ìtọ́ka_ìrísí != 0 && ààyè_ìfàyọkàsí_ìgbéwọlé >= 0 && ìlà >= 0 && ààyè_ìfàyọkàsí_ìgbéwọlé < 21 && ìlà < 21) {
            ìtọ́ka_Àgbétẹ́lẹ̀[ìlà * 21 + ààyè_ìfàyọkàsí_ìgbéwọlé] = 색;
            int kókó_iye = ìtọ́ka_píkísẹ̀(ààyè_ìfàyọkàsí_ìgbéwọlé, ìlà); if (kókó_iye != 0) 색 = kókó_iye == 2 ? 0xffffff : 0x101010;
        }
        if (보드.표시화소읽기(가로, 세로) != 색) {
            보드.kọ_ṣàfihàn_píkísẹ̀(가로, 세로, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void Parí() {
        if (합성중 == 0) return;
        for (int ìlà = 위경계; ìlà < 아래경계; ìlà++) for (int ààyè_ìfàyọkàsí_ìgbéwọlé = 왼경계; ààyè_ìfàyọkàsí_ìgbéwọlé < 오른경계; ààyè_ìfàyọkàsí_ìgbéwọlé++)
            ṣàfihàn_píkísẹ̀(ààyè_ìfàyọkàsí_ìgbéwọlé, ìlà, 완성그림[(ìlà - 위경계) * 1920 + ààyè_ìfàyọkàsí_ìgbéwọlé]);
        합성중 = 0;
    }
    public static int píkísẹ̀(int 가로, int 세로, int 색) {
        if (가로 < 0 || 세로 < 0 || 가로 >= 너비 || 세로 >= 높이) return 0;
        if (합성중 != 0) {
            if (가로 >= 왼경계 && 가로 < 오른경계 && 세로 >= 위경계 && 세로 < 아래경계)
                완성그림[(세로 - 위경계) * 1920 + 가로] = 색;
        } else ṣàfihàn_píkísẹ̀(가로, 세로, 색);
        return 0;
    }
    public static void 사각그림(int 가로, int 세로, int 폭, int gígùn_iye, int 색) {
        if (ní_ṣókí(가로, 세로, 폭, gígùn_iye) == 0) return;
        가로 = 잘린범위[0]; 세로 = 잘린범위[1]; 폭 = 잘린범위[2]; gígùn_iye = 잘린범위[3];
        for (int ìlà = 세로; ìlà < 세로 + gígùn_iye; ìlà++) for (int ààyè_ìfàyọkàsí_ìgbéwọlé = 가로; ààyè_ìfàyọkàsí_ìgbéwọlé < 가로 + 폭; ààyè_ìfàyọkàsí_ìgbéwọlé++) {
            if (합성중 != 0) 완성그림[(ìlà - 위경계) * 1920 + ààyè_ìfàyọkàsí_ìgbéwọlé] = 색;
            else ṣàfihàn_píkísẹ̀(ààyè_ìfàyọkàsí_ìgbéwọlé, ìlà, 색);
        }
    }
    public static void ìtọ́ka(int 가로, int 세로, int ìrísí_iye) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (ìrísí_iye >= 2 ? 10 : 0), 새세로 = 세로 - (ìrísí_iye >= 2 ? 10 : 0);
        if (ìtọ́ka_ìrísí == ìrísí_iye && 포인터가로 == 새가로 && 포인터세로 == 새세로) return;
        if (ìtọ́ka_ìrísí != 0) for (int ìlà = 0; ìlà < 21; ìlà++) for (int ààyè_ìfàyọkàsí_ìgbéwọlé = 0; ààyè_ìfàyọkàsí_ìgbéwọlé < 21; ààyè_ìfàyọkàsí_ìgbéwọlé++) {
            int 가 = 포인터가로 + ààyè_ìfàyọkàsí_ìgbéwọlé, 세 = 포인터세로 + ìlà;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) 보드.kọ_ṣàfihàn_píkísẹ̀(가, 세, ìtọ́ka_Àgbétẹ́lẹ̀[ìlà * 21 + ààyè_ìfàyọkàsí_ìgbéwọlé]);
        }
        ìtọ́ka_ìrísí = ìrísí_iye; 포인터가로 = 새가로; 포인터세로 = 새세로;
        if (ìrísí_iye != 0) for (int ìlà = 0; ìlà < 21; ìlà++) for (int ààyè_ìfàyọkàsí_ìgbéwọlé = 0; ààyè_ìfàyọkàsí_ìgbéwọlé < 21; ààyè_ìfàyọkàsí_ìgbéwọlé++) {
            int 가 = 포인터가로 + ààyè_ìfàyọkàsí_ìgbéwọlé, 세 = 포인터세로 + ìlà;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) {
                ìtọ́ka_Àgbétẹ́lẹ̀[ìlà * 21 + ààyè_ìfàyọkàsí_ìgbéwọlé] = 보드.표시화소읽기(가, 세);
                int kókó_iye = ìtọ́ka_píkísẹ̀(ààyè_ìfàyọkàsí_ìgbéwọlé, ìlà); if (kókó_iye != 0) 보드.kọ_ṣàfihàn_píkísẹ̀(가, 세, kókó_iye == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
