// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 화면 sika_inani·띠 합성·isikhombi 밑그림을 관리한다. ulwazi_ngokwenzekile_imininingwane 화면 inkumbulo_imininingwane 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, 높이, 합성중, 왼경계, 위경계, 오른경계, 아래경계;
    static int 포인터가로, 포인터세로, isikhombi_umumo;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] isikhombi_ngemuva = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void Hlela(int 폭, int ubude_inani) {
        너비 = 폭; 높이 = ubude_inani; 합성중 = 0; isikhombi_umumo = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int 높이얻기() { return 높이; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int isiqeshana_inani(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int qala_inani, int ubude_inani) {
        if (qala_inani > 2147483647 - ubude_inani) return 2147483647;
        return qala_inani + ubude_inani;
    }
    public static int isiqeshana(int 가로, int 세로, int 폭, int ubude_inani) {
        if (너비 == 0 || 폭 <= 0 || ubude_inani <= 0) return 0;
        int 오른쪽 = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(세로, ubude_inani);
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
    public static int Sebenzisa(int 가로, int 세로, int 폭, int ubude_inani) {
        if (합성중 != 0 || ubude_inani > 32 || isiqeshana(가로, 세로, 폭, ubude_inani) == 0) return 0;
        왼경계 = 잘린범위[0]; 위경계 = 잘린범위[1];
        오른경계 = 왼경계 + 잘린범위[2]; 아래경계 = 위경계 + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean isikhombi_ibhithi(int 가로, int 세로, int umumo_inani) {
        if (umumo_inani == 1) return 가로 >= 0 && 가로 <= 세로 / 2 && 세로 < 16;
        if (umumo_inani == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - 세로; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && 세로 >= 2 && 세로 <= 8 && (가로 <= 3 || 세로 <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && 세로 >= 12 && 세로 <= 18 && (가로 >= 17 || 세로 >= 17));
    }
    static int isikhombi_i_pel(int 가로, int 세로) {
        if (isikhombi_ibhithi(가로, 세로, isikhombi_umumo)) return 2;
        for (int umugqa = -1; umugqa <= 1; umugqa++) for (int isikhala_okufakwayo = -1; isikhala_okufakwayo <= 1; isikhala_okufakwayo++)
            if (isikhombi_ibhithi(가로 + isikhala_okufakwayo, 세로 + umugqa, isikhombi_umumo)) return 1;
        return 0;
    }
    static void bonisa_i_pel(int 가로, int 세로, int 색) {
        int isikhala_okufakwayo = 가로 - 포인터가로, umugqa = 세로 - 포인터세로;
        if (isikhombi_umumo != 0 && isikhala_okufakwayo >= 0 && umugqa >= 0 && isikhala_okufakwayo < 21 && umugqa < 21) {
            isikhombi_ngemuva[umugqa * 21 + isikhala_okufakwayo] = 색;
            int iphoyinti_inani = isikhombi_i_pel(isikhala_okufakwayo, umugqa); if (iphoyinti_inani != 0) 색 = iphoyinti_inani == 2 ? 0xffffff : 0x101010;
        }
        if (보드.표시화소읽기(가로, 세로) != 색) {
            보드.bhala_bonisa_i_pel(가로, 세로, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void Qeda() {
        if (합성중 == 0) return;
        for (int umugqa = 위경계; umugqa < 아래경계; umugqa++) for (int isikhala_okufakwayo = 왼경계; isikhala_okufakwayo < 오른경계; isikhala_okufakwayo++)
            bonisa_i_pel(isikhala_okufakwayo, umugqa, 완성그림[(umugqa - 위경계) * 1920 + isikhala_okufakwayo]);
        합성중 = 0;
    }
    public static int i_pel(int 가로, int 세로, int 색) {
        if (가로 < 0 || 세로 < 0 || 가로 >= 너비 || 세로 >= 높이) return 0;
        if (합성중 != 0) {
            if (가로 >= 왼경계 && 가로 < 오른경계 && 세로 >= 위경계 && 세로 < 아래경계)
                완성그림[(세로 - 위경계) * 1920 + 가로] = 색;
        } else bonisa_i_pel(가로, 세로, 색);
        return 0;
    }
    public static void 사각그림(int 가로, int 세로, int 폭, int ubude_inani, int 색) {
        if (isiqeshana(가로, 세로, 폭, ubude_inani) == 0) return;
        가로 = 잘린범위[0]; 세로 = 잘린범위[1]; 폭 = 잘린범위[2]; ubude_inani = 잘린범위[3];
        for (int umugqa = 세로; umugqa < 세로 + ubude_inani; umugqa++) for (int isikhala_okufakwayo = 가로; isikhala_okufakwayo < 가로 + 폭; isikhala_okufakwayo++) {
            if (합성중 != 0) 완성그림[(umugqa - 위경계) * 1920 + isikhala_okufakwayo] = 색;
            else bonisa_i_pel(isikhala_okufakwayo, umugqa, 색);
        }
    }
    public static void isikhombi(int 가로, int 세로, int umumo_inani) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (umumo_inani >= 2 ? 10 : 0), 새세로 = 세로 - (umumo_inani >= 2 ? 10 : 0);
        if (isikhombi_umumo == umumo_inani && 포인터가로 == 새가로 && 포인터세로 == 새세로) return;
        if (isikhombi_umumo != 0) for (int umugqa = 0; umugqa < 21; umugqa++) for (int isikhala_okufakwayo = 0; isikhala_okufakwayo < 21; isikhala_okufakwayo++) {
            int 가 = 포인터가로 + isikhala_okufakwayo, 세 = 포인터세로 + umugqa;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) 보드.bhala_bonisa_i_pel(가, 세, isikhombi_ngemuva[umugqa * 21 + isikhala_okufakwayo]);
        }
        isikhombi_umumo = umumo_inani; 포인터가로 = 새가로; 포인터세로 = 새세로;
        if (umumo_inani != 0) for (int umugqa = 0; umugqa < 21; umugqa++) for (int isikhala_okufakwayo = 0; isikhala_okufakwayo < 21; isikhala_okufakwayo++) {
            int 가 = 포인터가로 + isikhala_okufakwayo, 세 = 포인터세로 + umugqa;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) {
                isikhombi_ngemuva[umugqa * 21 + isikhala_okufakwayo] = 보드.표시화소읽기(가, 세);
                int iphoyinti_inani = isikhombi_i_pel(isikhala_okufakwayo, umugqa); if (iphoyinti_inani != 0) 보드.bhala_bonisa_i_pel(가, 세, iphoyinti_inani == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
