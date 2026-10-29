// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 화면 gukata_agaciro·띠 합성·mwerekana 밑그림을 관리한다. nyakuri_amakurushingiro 화면 ububiko_amakurushingiro 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, 높이, 합성중, 왼경계, 위경계, 오른경계, 아래경계;
    static int 포인터가로, 포인터세로, mwerekana_ishusho;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] mwerekana_Imbuganyuma = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void Gutegura(int 폭, int uburebure_agaciro) {
        너비 = 폭; 높이 = uburebure_agaciro; 합성중 = 0; mwerekana_ishusho = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int 높이얻기() { return 높이; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int kiripu_agaciro(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int Itangira_agaciro, int uburebure_agaciro) {
        if (Itangira_agaciro > 2147483647 - uburebure_agaciro) return 2147483647;
        return Itangira_agaciro + uburebure_agaciro;
    }
    public static int kiripu(int 가로, int 세로, int 폭, int uburebure_agaciro) {
        if (너비 == 0 || 폭 <= 0 || uburebure_agaciro <= 0) return 0;
        int 오른쪽 = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(세로, uburebure_agaciro);
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
    public static int ihuriro(int 가로, int 세로, int 폭, int uburebure_agaciro) {
        if (합성중 != 0 || uburebure_agaciro > 32 || kiripu(가로, 세로, 폭, uburebure_agaciro) == 0) return 0;
        왼경계 = 잘린범위[0]; 위경계 = 잘린범위[1];
        오른경계 = 왼경계 + 잘린범위[2]; 아래경계 = 위경계 + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean mwerekana_bit(int 가로, int 세로, int ishusho_agaciro_f1cd655a) {
        if (ishusho_agaciro_f1cd655a == 1) return 가로 >= 0 && 가로 <= 세로 / 2 && 세로 < 16;
        if (ishusho_agaciro_f1cd655a == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - 세로; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && 세로 >= 2 && 세로 <= 8 && (가로 <= 3 || 세로 <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && 세로 >= 12 && 세로 <= 18 && (가로 >= 17 || 세로 >= 17));
    }
    static int mwerekana_pel(int 가로, int 세로) {
        if (mwerekana_bit(가로, 세로, mwerekana_ishusho)) return 2;
        for (int umurongo = -1; umurongo <= 1; umurongo++) for (int umwanya_icyinjizwa = -1; umwanya_icyinjizwa <= 1; umwanya_icyinjizwa++)
            if (mwerekana_bit(가로 + umwanya_icyinjizwa, 세로 + umurongo, mwerekana_ishusho)) return 1;
        return 0;
    }
    static void kwerekana_pel(int 가로, int 세로, int 색) {
        int umwanya_icyinjizwa = 가로 - 포인터가로, umurongo = 세로 - 포인터세로;
        if (mwerekana_ishusho != 0 && umwanya_icyinjizwa >= 0 && umurongo >= 0 && umwanya_icyinjizwa < 21 && umurongo < 21) {
            mwerekana_Imbuganyuma[umurongo * 21 + umwanya_icyinjizwa] = 색;
            int inota_agaciro = mwerekana_pel(umwanya_icyinjizwa, umurongo); if (inota_agaciro != 0) 색 = inota_agaciro == 2 ? 0xffffff : 0x101010;
        }
        if (보드.표시화소읽기(가로, 세로) != 색) {
            보드.kwandika_kwerekana_pel(가로, 세로, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void Kurangiza() {
        if (합성중 == 0) return;
        for (int umurongo = 위경계; umurongo < 아래경계; umurongo++) for (int umwanya_icyinjizwa = 왼경계; umwanya_icyinjizwa < 오른경계; umwanya_icyinjizwa++)
            kwerekana_pel(umwanya_icyinjizwa, umurongo, 완성그림[(umurongo - 위경계) * 1920 + umwanya_icyinjizwa]);
        합성중 = 0;
    }
    public static int pel(int 가로, int 세로, int 색) {
        if (가로 < 0 || 세로 < 0 || 가로 >= 너비 || 세로 >= 높이) return 0;
        if (합성중 != 0) {
            if (가로 >= 왼경계 && 가로 < 오른경계 && 세로 >= 위경계 && 세로 < 아래경계)
                완성그림[(세로 - 위경계) * 1920 + 가로] = 색;
        } else kwerekana_pel(가로, 세로, 색);
        return 0;
    }
    public static void 사각그림(int 가로, int 세로, int 폭, int uburebure_agaciro, int 색) {
        if (kiripu(가로, 세로, 폭, uburebure_agaciro) == 0) return;
        가로 = 잘린범위[0]; 세로 = 잘린범위[1]; 폭 = 잘린범위[2]; uburebure_agaciro = 잘린범위[3];
        for (int umurongo = 세로; umurongo < 세로 + uburebure_agaciro; umurongo++) for (int umwanya_icyinjizwa = 가로; umwanya_icyinjizwa < 가로 + 폭; umwanya_icyinjizwa++) {
            if (합성중 != 0) 완성그림[(umurongo - 위경계) * 1920 + umwanya_icyinjizwa] = 색;
            else kwerekana_pel(umwanya_icyinjizwa, umurongo, 색);
        }
    }
    public static void mwerekana(int 가로, int 세로, int ishusho_agaciro_f1cd655a) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (ishusho_agaciro_f1cd655a >= 2 ? 10 : 0), 새세로 = 세로 - (ishusho_agaciro_f1cd655a >= 2 ? 10 : 0);
        if (mwerekana_ishusho == ishusho_agaciro_f1cd655a && 포인터가로 == 새가로 && 포인터세로 == 새세로) return;
        if (mwerekana_ishusho != 0) for (int umurongo = 0; umurongo < 21; umurongo++) for (int umwanya_icyinjizwa = 0; umwanya_icyinjizwa < 21; umwanya_icyinjizwa++) {
            int 가 = 포인터가로 + umwanya_icyinjizwa, 세 = 포인터세로 + umurongo;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) 보드.kwandika_kwerekana_pel(가, 세, mwerekana_Imbuganyuma[umurongo * 21 + umwanya_icyinjizwa]);
        }
        mwerekana_ishusho = ishusho_agaciro_f1cd655a; 포인터가로 = 새가로; 포인터세로 = 새세로;
        if (ishusho_agaciro_f1cd655a != 0) for (int umurongo = 0; umurongo < 21; umurongo++) for (int umwanya_icyinjizwa = 0; umwanya_icyinjizwa < 21; umwanya_icyinjizwa++) {
            int 가 = 포인터가로 + umwanya_icyinjizwa, 세 = 포인터세로 + umurongo;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) {
                mwerekana_Imbuganyuma[umurongo * 21 + umwanya_icyinjizwa] = 보드.표시화소읽기(가, 세);
                int inota_agaciro = mwerekana_pel(umwanya_icyinjizwa, umurongo); if (inota_agaciro != 0) 보드.kwandika_kwerekana_pel(가, 세, inota_agaciro == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
