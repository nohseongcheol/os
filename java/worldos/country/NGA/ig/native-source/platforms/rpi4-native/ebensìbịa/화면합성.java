// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 화면 gbubìte_valuu·띠 합성·nrụaka 밑그림을 관리한다. ǹdịnezie_datà 화면 memọrị_datà 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, 높이, 합성중, 왼경계, 위경계, 오른경계, 아래경계;
    static int 포인터가로, 포인터세로, nrụaka_ụdị;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] nrụaka_Bakgraụnd = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void Kwado(int 폭, int ogologo_valuu) {
        너비 = 폭; 높이 = ogologo_valuu; 합성중 = 0; nrụaka_ụdị = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int 높이얻기() { return 높이; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int ntipanye_valuu(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int Mbido_valuu, int ogologo_valuu) {
        if (Mbido_valuu > 2147483647 - ogologo_valuu) return 2147483647;
        return Mbido_valuu + ogologo_valuu;
    }
    public static int ntipanye(int 가로, int 세로, int 폭, int ogologo_valuu) {
        if (너비 == 0 || 폭 <= 0 || ogologo_valuu <= 0) return 0;
        int 오른쪽 = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(세로, ogologo_valuu);
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
    public static int Bido(int 가로, int 세로, int 폭, int ogologo_valuu) {
        if (합성중 != 0 || ogologo_valuu > 32 || ntipanye(가로, 세로, 폭, ogologo_valuu) == 0) return 0;
        왼경계 = 잘린범위[0]; 위경계 = 잘린범위[1];
        오른경계 = 왼경계 + 잘린범위[2]; 아래경계 = 위경계 + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean nrụaka_bit(int 가로, int 세로, int ụdị_valuu_f1cd655a) {
        if (ụdị_valuu_f1cd655a == 1) return 가로 >= 0 && 가로 <= 세로 / 2 && 세로 < 16;
        if (ụdị_valuu_f1cd655a == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - 세로; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && 세로 >= 2 && 세로 <= 8 && (가로 <= 3 || 세로 <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && 세로 >= 12 && 세로 <= 18 && (가로 >= 17 || 세로 >= 17));
    }
    static int nrụaka_pel(int 가로, int 세로) {
        if (nrụaka_bit(가로, 세로, nrụaka_ụdị)) return 2;
        for (int ahịrī = -1; ahịrī <= 1; ahịrī++) for (int oghere_ndebà = -1; oghere_ndebà <= 1; oghere_ndebà++)
            if (nrụaka_bit(가로 + oghere_ndebà, 세로 + ahịrī, nrụaka_ụdị)) return 1;
        return 0;
    }
    static void gosịpụta_pel(int 가로, int 세로, int 색) {
        int oghere_ndebà = 가로 - 포인터가로, ahịrī = 세로 - 포인터세로;
        if (nrụaka_ụdị != 0 && oghere_ndebà >= 0 && ahịrī >= 0 && oghere_ndebà < 21 && ahịrī < 21) {
            nrụaka_Bakgraụnd[ahịrī * 21 + oghere_ndebà] = 색;
            int akara_valuu = nrụaka_pel(oghere_ndebà, ahịrī); if (akara_valuu != 0) 색 = akara_valuu == 2 ? 0xffffff : 0x101010;
        }
        if (보드.표시화소읽기(가로, 세로) != 색) {
            보드.dee_gosịpụta_pel(가로, 세로, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void Gwụ() {
        if (합성중 == 0) return;
        for (int ahịrī = 위경계; ahịrī < 아래경계; ahịrī++) for (int oghere_ndebà = 왼경계; oghere_ndebà < 오른경계; oghere_ndebà++)
            gosịpụta_pel(oghere_ndebà, ahịrī, 완성그림[(ahịrī - 위경계) * 1920 + oghere_ndebà]);
        합성중 = 0;
    }
    public static int pel(int 가로, int 세로, int 색) {
        if (가로 < 0 || 세로 < 0 || 가로 >= 너비 || 세로 >= 높이) return 0;
        if (합성중 != 0) {
            if (가로 >= 왼경계 && 가로 < 오른경계 && 세로 >= 위경계 && 세로 < 아래경계)
                완성그림[(세로 - 위경계) * 1920 + 가로] = 색;
        } else gosịpụta_pel(가로, 세로, 색);
        return 0;
    }
    public static void 사각그림(int 가로, int 세로, int 폭, int ogologo_valuu, int 색) {
        if (ntipanye(가로, 세로, 폭, ogologo_valuu) == 0) return;
        가로 = 잘린범위[0]; 세로 = 잘린범위[1]; 폭 = 잘린범위[2]; ogologo_valuu = 잘린범위[3];
        for (int ahịrī = 세로; ahịrī < 세로 + ogologo_valuu; ahịrī++) for (int oghere_ndebà = 가로; oghere_ndebà < 가로 + 폭; oghere_ndebà++) {
            if (합성중 != 0) 완성그림[(ahịrī - 위경계) * 1920 + oghere_ndebà] = 색;
            else gosịpụta_pel(oghere_ndebà, ahịrī, 색);
        }
    }
    public static void nrụaka(int 가로, int 세로, int ụdị_valuu_f1cd655a) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (ụdị_valuu_f1cd655a >= 2 ? 10 : 0), 새세로 = 세로 - (ụdị_valuu_f1cd655a >= 2 ? 10 : 0);
        if (nrụaka_ụdị == ụdị_valuu_f1cd655a && 포인터가로 == 새가로 && 포인터세로 == 새세로) return;
        if (nrụaka_ụdị != 0) for (int ahịrī = 0; ahịrī < 21; ahịrī++) for (int oghere_ndebà = 0; oghere_ndebà < 21; oghere_ndebà++) {
            int 가 = 포인터가로 + oghere_ndebà, 세 = 포인터세로 + ahịrī;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) 보드.dee_gosịpụta_pel(가, 세, nrụaka_Bakgraụnd[ahịrī * 21 + oghere_ndebà]);
        }
        nrụaka_ụdị = ụdị_valuu_f1cd655a; 포인터가로 = 새가로; 포인터세로 = 새세로;
        if (ụdị_valuu_f1cd655a != 0) for (int ahịrī = 0; ahịrī < 21; ahịrī++) for (int oghere_ndebà = 0; oghere_ndebà < 21; oghere_ndebà++) {
            int 가 = 포인터가로 + oghere_ndebà, 세 = 포인터세로 + ahịrī;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) {
                nrụaka_Bakgraụnd[ahịrī * 21 + oghere_ndebà] = 보드.표시화소읽기(가, 세);
                int akara_valuu = nrụaka_pel(oghere_ndebà, ahịrī); if (akara_valuu != 0) 보드.dee_gosịpụta_pel(가, 세, akara_valuu == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
