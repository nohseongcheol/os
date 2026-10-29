// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 화면 schneiden_VALUE·띠 합성·Uweiser 밑그림을 관리한다. aktuell_Daten 화면 Späicher_Daten 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, 높이, 합성중, 왼경계, 위경계, 오른경계, 아래경계;
    static int 포인터가로, 포인터세로, Uweiser_Form;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] Uweiser_Hannergrond = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void Préparéieren(int 폭, int Längt_VALUE) {
        너비 = 폭; 높이 = Längt_VALUE; 합성중 = 0; Uweiser_Form = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int 높이얻기() { return 높이; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int Clip_VALUE(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int Start_VALUE, int Längt_VALUE) {
        if (Start_VALUE > 2147483647 - Längt_VALUE) return 2147483647;
        return Start_VALUE + Längt_VALUE;
    }
    public static int Clip(int 가로, int Vertikal_positionéieren, int 폭, int Längt_VALUE) {
        if (너비 == 0 || 폭 <= 0 || Längt_VALUE <= 0) return 0;
        int RIGHT = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(Vertikal_positionéieren, Längt_VALUE);
        int 왼쪽 = 합성중 != 0 ? 왼경계 : 0, 위쪽 = 합성중 != 0 ? 위경계 : 0;
        int 최대가로 = 합성중 != 0 ? 오른경계 : 너비, 최대세로 = 합성중 != 0 ? 아래경계 : 높이;
        if (가로 < 왼쪽) 가로 = 왼쪽;
        if (Vertikal_positionéieren < 위쪽) Vertikal_positionéieren = 위쪽;
        if (RIGHT > 최대가로) RIGHT = 최대가로;
        if (아래쪽 > 최대세로) 아래쪽 = 최대세로;
        if (RIGHT <= 가로 || 아래쪽 <= Vertikal_positionéieren) return 0;
        잘린범위[0] = 가로; 잘린범위[1] = Vertikal_positionéieren;
        잘린범위[2] = RIGHT - 가로; 잘린범위[3] = 아래쪽 - Vertikal_positionéieren;
        return 1;
    }
    public static int Laf(int 가로, int Vertikal_positionéieren, int 폭, int Längt_VALUE) {
        if (합성중 != 0 || Längt_VALUE > 32 || Clip(가로, Vertikal_positionéieren, 폭, Längt_VALUE) == 0) return 0;
        왼경계 = 잘린범위[0]; 위경계 = 잘린범위[1];
        오른경계 = 왼경계 + 잘린범위[2]; 아래경계 = 위경계 + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean Uweiser_Bit(int 가로, int Vertikal_positionéieren, int Form_VALUE) {
        if (Form_VALUE == 1) return 가로 >= 0 && 가로 <= Vertikal_positionéieren / 2 && Vertikal_positionéieren < 16;
        if (Form_VALUE == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - Vertikal_positionéieren; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && Vertikal_positionéieren >= 2 && Vertikal_positionéieren <= 8 && (가로 <= 3 || Vertikal_positionéieren <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && Vertikal_positionéieren >= 12 && Vertikal_positionéieren <= 18 && (가로 >= 17 || Vertikal_positionéieren >= 17));
    }
    static int Uweiser_Pel(int 가로, int Vertikal_positionéieren) {
        if (Uweiser_Bit(가로, Vertikal_positionéieren, Uweiser_Form)) return 2;
        for (int Zeil = -1; Zeil <= 1; Zeil++) for (int Slot_Agab = -1; Slot_Agab <= 1; Slot_Agab++)
            if (Uweiser_Bit(가로 + Slot_Agab, Vertikal_positionéieren + Zeil, Uweiser_Form)) return 1;
        return 0;
    }
    static void Bildschierm_Pel(int 가로, int Vertikal_positionéieren, int 색) {
        int Slot_Agab = 가로 - 포인터가로, Zeil = Vertikal_positionéieren - 포인터세로;
        if (Uweiser_Form != 0 && Slot_Agab >= 0 && Zeil >= 0 && Slot_Agab < 21 && Zeil < 21) {
            Uweiser_Hannergrond[Zeil * 21 + Slot_Agab] = 색;
            int Punkt_VALUE = Uweiser_Pel(Slot_Agab, Zeil); if (Punkt_VALUE != 0) 색 = Punkt_VALUE == 2 ? 0xffffff : 0x101010;
        }
        if (Board.표시화소읽기(가로, Vertikal_positionéieren) != 색) {
            Board.schreiwen_Bildschierm_Pel(가로, Vertikal_positionéieren, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void Ofschléissen() {
        if (합성중 == 0) return;
        for (int Zeil = 위경계; Zeil < 아래경계; Zeil++) for (int Slot_Agab = 왼경계; Slot_Agab < 오른경계; Slot_Agab++)
            Bildschierm_Pel(Slot_Agab, Zeil, 완성그림[(Zeil - 위경계) * 1920 + Slot_Agab]);
        합성중 = 0;
    }
    public static int Pel(int 가로, int Vertikal_positionéieren, int 색) {
        if (가로 < 0 || Vertikal_positionéieren < 0 || 가로 >= 너비 || Vertikal_positionéieren >= 높이) return 0;
        if (합성중 != 0) {
            if (가로 >= 왼경계 && 가로 < 오른경계 && Vertikal_positionéieren >= 위경계 && Vertikal_positionéieren < 아래경계)
                완성그림[(Vertikal_positionéieren - 위경계) * 1920 + 가로] = 색;
        } else Bildschierm_Pel(가로, Vertikal_positionéieren, 색);
        return 0;
    }
    public static void 사각그림(int 가로, int Vertikal_positionéieren, int 폭, int Längt_VALUE, int 색) {
        if (Clip(가로, Vertikal_positionéieren, 폭, Längt_VALUE) == 0) return;
        가로 = 잘린범위[0]; Vertikal_positionéieren = 잘린범위[1]; 폭 = 잘린범위[2]; Längt_VALUE = 잘린범위[3];
        for (int Zeil = Vertikal_positionéieren; Zeil < Vertikal_positionéieren + Längt_VALUE; Zeil++) for (int Slot_Agab = 가로; Slot_Agab < 가로 + 폭; Slot_Agab++) {
            if (합성중 != 0) 완성그림[(Zeil - 위경계) * 1920 + Slot_Agab] = 색;
            else Bildschierm_Pel(Slot_Agab, Zeil, 색);
        }
    }
    public static void Uweiser(int 가로, int Vertikal_positionéieren, int Form_VALUE) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (Form_VALUE >= 2 ? 10 : 0), 새세로 = Vertikal_positionéieren - (Form_VALUE >= 2 ? 10 : 0);
        if (Uweiser_Form == Form_VALUE && 포인터가로 == 새가로 && 포인터세로 == 새세로) return;
        if (Uweiser_Form != 0) for (int Zeil = 0; Zeil < 21; Zeil++) for (int Slot_Agab = 0; Slot_Agab < 21; Slot_Agab++) {
            int 가 = 포인터가로 + Slot_Agab, 세 = 포인터세로 + Zeil;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) Board.schreiwen_Bildschierm_Pel(가, 세, Uweiser_Hannergrond[Zeil * 21 + Slot_Agab]);
        }
        Uweiser_Form = Form_VALUE; 포인터가로 = 새가로; 포인터세로 = 새세로;
        if (Form_VALUE != 0) for (int Zeil = 0; Zeil < 21; Zeil++) for (int Slot_Agab = 0; Slot_Agab < 21; Slot_Agab++) {
            int 가 = 포인터가로 + Slot_Agab, 세 = 포인터세로 + Zeil;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) {
                Uweiser_Hannergrond[Zeil * 21 + Slot_Agab] = Board.표시화소읽기(가, 세);
                int Punkt_VALUE = Uweiser_Pel(Slot_Agab, Zeil); if (Punkt_VALUE != 0) Board.schreiwen_Bildschierm_Pel(가, 세, Punkt_VALUE == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
