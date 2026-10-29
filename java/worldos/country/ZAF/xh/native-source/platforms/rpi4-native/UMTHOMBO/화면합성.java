// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 화면 sika_ixabiso·띠 합성·isalathisi 밑그림을 관리한다. eyona_yenzekileyo_iingcombolo 화면 imemori_iingcombolo 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, 높이, 합성중, 왼경계, 위경계, 오른경계, 아래경계;
    static int 포인터가로, 포인터세로, isalathisi_imilo;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] isalathisi_Ngasemva = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void lungisa(int 폭, int ubude_ixabiso) {
        너비 = 폭; 높이 = ubude_ixabiso; 합성중 = 0; isalathisi_imilo = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int 높이얻기() { return 높이; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int ikliphu_ixabiso(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int qala_ixabiso, int ubude_ixabiso) {
        if (qala_ixabiso > 2147483647 - ubude_ixabiso) return 2147483647;
        return qala_ixabiso + ubude_ixabiso;
    }
    public static int ikliphu(int 가로, int 세로, int 폭, int ubude_ixabiso) {
        if (너비 == 0 || 폭 <= 0 || ubude_ixabiso <= 0) return 0;
        int 오른쪽 = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(세로, ubude_ixabiso);
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
    public static int Phumeza(int 가로, int 세로, int 폭, int ubude_ixabiso) {
        if (합성중 != 0 || ubude_ixabiso > 32 || ikliphu(가로, 세로, 폭, ubude_ixabiso) == 0) return 0;
        왼경계 = 잘린범위[0]; 위경계 = 잘린범위[1];
        오른경계 = 왼경계 + 잘린범위[2]; 아래경계 = 위경계 + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean isalathisi_ibhithi(int 가로, int 세로, int imilo_ixabiso) {
        if (imilo_ixabiso == 1) return 가로 >= 0 && 가로 <= 세로 / 2 && 세로 < 16;
        if (imilo_ixabiso == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - 세로; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && 세로 >= 2 && 세로 <= 8 && (가로 <= 3 || 세로 <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && 세로 >= 12 && 세로 <= 18 && (가로 >= 17 || 세로 >= 17));
    }
    static int isalathisi_i_pel(int 가로, int 세로) {
        if (isalathisi_ibhithi(가로, 세로, isalathisi_imilo)) return 2;
        for (int umgca = -1; umgca <= 1; umgca++) for (int isithuba_ufako_nkcukacha = -1; isithuba_ufako_nkcukacha <= 1; isithuba_ufako_nkcukacha++)
            if (isalathisi_ibhithi(가로 + isithuba_ufako_nkcukacha, 세로 + umgca, isalathisi_imilo)) return 1;
        return 0;
    }
    static void bonisa_i_pel(int 가로, int 세로, int 색) {
        int isithuba_ufako_nkcukacha = 가로 - 포인터가로, umgca = 세로 - 포인터세로;
        if (isalathisi_imilo != 0 && isithuba_ufako_nkcukacha >= 0 && umgca >= 0 && isithuba_ufako_nkcukacha < 21 && umgca < 21) {
            isalathisi_Ngasemva[umgca * 21 + isithuba_ufako_nkcukacha] = 색;
            int inqaku_ixabiso = isalathisi_i_pel(isithuba_ufako_nkcukacha, umgca); if (inqaku_ixabiso != 0) 색 = inqaku_ixabiso == 2 ? 0xffffff : 0x101010;
        }
        if (보드.표시화소읽기(가로, 세로) != 색) {
            보드.bhala_bonisa_i_pel(가로, 세로, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void Gqiba() {
        if (합성중 == 0) return;
        for (int umgca = 위경계; umgca < 아래경계; umgca++) for (int isithuba_ufako_nkcukacha = 왼경계; isithuba_ufako_nkcukacha < 오른경계; isithuba_ufako_nkcukacha++)
            bonisa_i_pel(isithuba_ufako_nkcukacha, umgca, 완성그림[(umgca - 위경계) * 1920 + isithuba_ufako_nkcukacha]);
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
    public static void 사각그림(int 가로, int 세로, int 폭, int ubude_ixabiso, int 색) {
        if (ikliphu(가로, 세로, 폭, ubude_ixabiso) == 0) return;
        가로 = 잘린범위[0]; 세로 = 잘린범위[1]; 폭 = 잘린범위[2]; ubude_ixabiso = 잘린범위[3];
        for (int umgca = 세로; umgca < 세로 + ubude_ixabiso; umgca++) for (int isithuba_ufako_nkcukacha = 가로; isithuba_ufako_nkcukacha < 가로 + 폭; isithuba_ufako_nkcukacha++) {
            if (합성중 != 0) 완성그림[(umgca - 위경계) * 1920 + isithuba_ufako_nkcukacha] = 색;
            else bonisa_i_pel(isithuba_ufako_nkcukacha, umgca, 색);
        }
    }
    public static void isalathisi(int 가로, int 세로, int imilo_ixabiso) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (imilo_ixabiso >= 2 ? 10 : 0), 새세로 = 세로 - (imilo_ixabiso >= 2 ? 10 : 0);
        if (isalathisi_imilo == imilo_ixabiso && 포인터가로 == 새가로 && 포인터세로 == 새세로) return;
        if (isalathisi_imilo != 0) for (int umgca = 0; umgca < 21; umgca++) for (int isithuba_ufako_nkcukacha = 0; isithuba_ufako_nkcukacha < 21; isithuba_ufako_nkcukacha++) {
            int 가 = 포인터가로 + isithuba_ufako_nkcukacha, 세 = 포인터세로 + umgca;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) 보드.bhala_bonisa_i_pel(가, 세, isalathisi_Ngasemva[umgca * 21 + isithuba_ufako_nkcukacha]);
        }
        isalathisi_imilo = imilo_ixabiso; 포인터가로 = 새가로; 포인터세로 = 새세로;
        if (imilo_ixabiso != 0) for (int umgca = 0; umgca < 21; umgca++) for (int isithuba_ufako_nkcukacha = 0; isithuba_ufako_nkcukacha < 21; isithuba_ufako_nkcukacha++) {
            int 가 = 포인터가로 + isithuba_ufako_nkcukacha, 세 = 포인터세로 + umgca;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) {
                isalathisi_Ngasemva[umgca * 21 + isithuba_ufako_nkcukacha] = 보드.표시화소읽기(가, 세);
                int inqaku_ixabiso = isalathisi_i_pel(isithuba_ufako_nkcukacha, umgca); if (inqaku_ixabiso != 0) 보드.bhala_bonisa_i_pel(가, 세, inqaku_ixabiso == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
