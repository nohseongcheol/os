// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 화면 I_cut_VALUE·띠 합성·pointer 밑그림을 관리한다. totoo_data 화면 Memory_data 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, 높이, 합성중, 왼경계, 위경계, 오른경계, 아래경계;
    static int pointer_X_button, pointer_Y_button, pointer_hugis;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] pointer_wallpaper = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void Ihanda(int 폭, int haba_VALUE) {
        너비 = 폭; 높이 = haba_VALUE; 합성중 = 0; pointer_hugis = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int 높이얻기() { return 높이; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int clip_VALUE(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int Start_VALUE, int haba_VALUE) {
        if (Start_VALUE > 2147483647 - haba_VALUE) return 2147483647;
        return Start_VALUE + haba_VALUE;
    }
    public static int clip(int 가로, int archive_posisyon, int 폭, int haba_VALUE) {
        if (너비 == 0 || 폭 <= 0 || haba_VALUE <= 0) return 0;
        int RIGHT = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(archive_posisyon, haba_VALUE);
        int 왼쪽 = 합성중 != 0 ? 왼경계 : 0, 위쪽 = 합성중 != 0 ? 위경계 : 0;
        int 최대가로 = 합성중 != 0 ? 오른경계 : 너비, 최대세로 = 합성중 != 0 ? 아래경계 : 높이;
        if (가로 < 왼쪽) 가로 = 왼쪽;
        if (archive_posisyon < 위쪽) archive_posisyon = 위쪽;
        if (RIGHT > 최대가로) RIGHT = 최대가로;
        if (아래쪽 > 최대세로) 아래쪽 = 최대세로;
        if (RIGHT <= 가로 || 아래쪽 <= archive_posisyon) return 0;
        잘린범위[0] = 가로; 잘린범위[1] = archive_posisyon;
        잘린범위[2] = RIGHT - 가로; 잘린범위[3] = 아래쪽 - archive_posisyon;
        return 1;
    }
    public static int run(int 가로, int archive_posisyon, int 폭, int haba_VALUE) {
        if (합성중 != 0 || haba_VALUE > 32 || clip(가로, archive_posisyon, 폭, haba_VALUE) == 0) return 0;
        왼경계 = 잘린범위[0]; 위경계 = 잘린범위[1];
        오른경계 = 왼경계 + 잘린범위[2]; 아래경계 = 위경계 + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean pointer_bit(int 가로, int archive_posisyon, int hugis_VALUE) {
        if (hugis_VALUE == 1) return 가로 >= 0 && 가로 <= archive_posisyon / 2 && archive_posisyon < 16;
        if (hugis_VALUE == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - archive_posisyon; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && archive_posisyon >= 2 && archive_posisyon <= 8 && (가로 <= 3 || archive_posisyon <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && archive_posisyon >= 12 && archive_posisyon <= 18 && (가로 >= 17 || archive_posisyon >= 17));
    }
    static int pointer_pel(int 가로, int archive_posisyon) {
        if (pointer_bit(가로, archive_posisyon, pointer_hugis)) return 2;
        for (int linya = -1; linya <= 1; linya++) for (int espasyo_pagpasok = -1; espasyo_pagpasok <= 1; espasyo_pagpasok++)
            if (pointer_bit(가로 + espasyo_pagpasok, archive_posisyon + linya, pointer_hugis)) return 1;
        return 0;
    }
    static void display_pel(int 가로, int archive_posisyon, int 색) {
        int espasyo_pagpasok = 가로 - pointer_X_button, linya = archive_posisyon - pointer_Y_button;
        if (pointer_hugis != 0 && espasyo_pagpasok >= 0 && linya >= 0 && espasyo_pagpasok < 21 && linya < 21) {
            pointer_wallpaper[linya * 21 + espasyo_pagpasok] = 색;
            int point_VALUE = pointer_pel(espasyo_pagpasok, linya); if (point_VALUE != 0) 색 = point_VALUE == 2 ? 0xffffff : 0x101010;
        }
        if (board.표시화소읽기(가로, archive_posisyon) != 색) {
            board.sumulat_display_pel(가로, archive_posisyon, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void Tapos_Na() {
        if (합성중 == 0) return;
        for (int linya = 위경계; linya < 아래경계; linya++) for (int espasyo_pagpasok = 왼경계; espasyo_pagpasok < 오른경계; espasyo_pagpasok++)
            display_pel(espasyo_pagpasok, linya, 완성그림[(linya - 위경계) * 1920 + espasyo_pagpasok]);
        합성중 = 0;
    }
    public static int pel(int 가로, int archive_posisyon, int 색) {
        if (가로 < 0 || archive_posisyon < 0 || 가로 >= 너비 || archive_posisyon >= 높이) return 0;
        if (합성중 != 0) {
            if (가로 >= 왼경계 && 가로 < 오른경계 && archive_posisyon >= 위경계 && archive_posisyon < 아래경계)
                완성그림[(archive_posisyon - 위경계) * 1920 + 가로] = 색;
        } else display_pel(가로, archive_posisyon, 색);
        return 0;
    }
    public static void 사각그림(int 가로, int archive_posisyon, int 폭, int haba_VALUE, int 색) {
        if (clip(가로, archive_posisyon, 폭, haba_VALUE) == 0) return;
        가로 = 잘린범위[0]; archive_posisyon = 잘린범위[1]; 폭 = 잘린범위[2]; haba_VALUE = 잘린범위[3];
        for (int linya = archive_posisyon; linya < archive_posisyon + haba_VALUE; linya++) for (int espasyo_pagpasok = 가로; espasyo_pagpasok < 가로 + 폭; espasyo_pagpasok++) {
            if (합성중 != 0) 완성그림[(linya - 위경계) * 1920 + espasyo_pagpasok] = 색;
            else display_pel(espasyo_pagpasok, linya, 색);
        }
    }
    public static void pointer(int 가로, int archive_posisyon, int hugis_VALUE) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (hugis_VALUE >= 2 ? 10 : 0), 새세로 = archive_posisyon - (hugis_VALUE >= 2 ? 10 : 0);
        if (pointer_hugis == hugis_VALUE && pointer_X_button == 새가로 && pointer_Y_button == 새세로) return;
        if (pointer_hugis != 0) for (int linya = 0; linya < 21; linya++) for (int espasyo_pagpasok = 0; espasyo_pagpasok < 21; espasyo_pagpasok++) {
            int 가 = pointer_X_button + espasyo_pagpasok, 세 = pointer_Y_button + linya;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) board.sumulat_display_pel(가, 세, pointer_wallpaper[linya * 21 + espasyo_pagpasok]);
        }
        pointer_hugis = hugis_VALUE; pointer_X_button = 새가로; pointer_Y_button = 새세로;
        if (hugis_VALUE != 0) for (int linya = 0; linya < 21; linya++) for (int espasyo_pagpasok = 0; espasyo_pagpasok < 21; espasyo_pagpasok++) {
            int 가 = pointer_X_button + espasyo_pagpasok, 세 = pointer_Y_button + linya;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < 높이) {
                pointer_wallpaper[linya * 21 + espasyo_pagpasok] = board.표시화소읽기(가, 세);
                int point_VALUE = pointer_pel(espasyo_pagpasok, linya); if (point_VALUE != 0) board.sumulat_display_pel(가, 세, point_VALUE == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
