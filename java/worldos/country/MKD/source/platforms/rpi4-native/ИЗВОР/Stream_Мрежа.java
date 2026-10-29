// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** јадро_VALUE 안의 연결형 бајт_VALUE Stream_VALUE. Ethernet/TCP 패킷 스택이 아닌 루프백 socket слој_VALUE_e65604ef. */
public final class Stream_Мрежа {
    static int[] статус_VALUE = new int[16], порта_VALUE = new int[16], 짝 = new int[16], рамноправен_уред_порта = new int[16], почекај_VALUE = new int[16], 묶임 = new int[16];
    static int[] предна_VALUE = new int[16], 수 = new int[16], податоци = new int[16 * 1024];
    static int Следно_ставка = 50000;
    static int провери(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && статус_VALUE[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int број_на_порта) { for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (статус_VALUE[Loop_INDEX] != 0 && 묶임[Loop_INDEX] != 0 && порта_VALUE[Loop_INDEX] == број_на_порта) return true; return false; }
    public static int Create_внес() {
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (статус_VALUE[Loop_INDEX] == 0) { статус_VALUE[Loop_INDEX] = 1; рамноправен_уред_порта[Loop_INDEX] = порта_VALUE[Loop_INDEX] = предна_VALUE[Loop_INDEX] = 수[Loop_INDEX] = почекај_VALUE[Loop_INDEX] = 묶임[Loop_INDEX] = 0; 짝[Loop_INDEX] = -1; return Loop_INDEX + 40; }
        return -24;
    }
    public static int 묶기(int 열린파일번호, int 통신주소, int број_на_порта) {
        int Loop_INDEX = провери(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (통신주소 != 0 && 통신주소 != 0x7f000001) return -99;
        if (статус_VALUE[Loop_INDEX] != 1 || број_на_порта < 0 || број_на_порта > 65535) return -22;
        if (број_на_порта == 0) { do { број_на_порта = Следно_ставка++; if (Следно_ставка > 65535) Следно_ставка = 50000; } while (사용중(број_на_порта)); }
        if (사용중(број_на_порта)) return -98; порта_VALUE[Loop_INDEX] = број_на_порта; 묶임[Loop_INDEX] = 1; статус_VALUE[Loop_INDEX] = 2; return 0;
    }
    public static int 듣기(int 열린파일번호, int 연결대기한도) { int Loop_INDEX = провери(열린파일번호); if (Loop_INDEX < 0) return -9; if (статус_VALUE[Loop_INDEX] != 2 || 연결대기한도 < 1) return -22; статус_VALUE[Loop_INDEX] = 3; return 0; }
    public static int Врзи_се(int 열린파일번호, int 통신주소, int број_на_порта) {
        int Loop_INDEX = провери(열린파일번호); if (Loop_INDEX < 0) return -9; if (통신주소 != 0x7f000001) return -101;
        if (број_на_порта < 1 || број_на_порта > 65535 || статус_VALUE[Loop_INDEX] > 2) return -22;
        int 수신쪽 = -1; for (int внатрешно_поврзување_позиционирање = 0; внатрешно_поврзување_позиционирање < 16; внатрешно_поврзување_позиционирање++) if (статус_VALUE[внатрешно_поврзување_позиционирање] == 3 && порта_VALUE[внатрешно_поврзување_позиционирање] == број_на_порта) 수신쪽 = внатрешно_поврзување_позиционирање;
        if (수신쪽 < 0) return -111;
        int 대기여부 = 0; for (int внатрешно_поврзување_позиционирање = 0; внатрешно_поврзување_позиционирање < 16; внатрешно_поврзување_позиционирање++) if (почекај_VALUE[внатрешно_поврзување_позиционирање] == 수신쪽 + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (статус_VALUE[Loop_INDEX] == 1) { int 처리값 = 묶기(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int 다른번호 = Create_внес(); if (다른번호 < 0) return 다른번호; 다른번호 -= 40;
        статус_VALUE[Loop_INDEX] = статус_VALUE[다른번호] = 4; 짝[Loop_INDEX] = 다른번호; 짝[다른번호] = Loop_INDEX; порта_VALUE[다른번호] = број_на_порта; рамноправен_уред_порта[Loop_INDEX] = број_на_порта; рамноправен_уред_порта[다른번호] = порта_VALUE[Loop_INDEX]; почекај_VALUE[다른번호] = 수신쪽 + 1; return 0;
    }
    public static int прифати_врска(int 열린파일번호) { int Loop_INDEX = провери(열린파일번호); if (Loop_INDEX < 0) return -9; if (статус_VALUE[Loop_INDEX] != 3) return -22; for (int внатрешно_поврзување_позиционирање = 0; внатрешно_поврзување_позиционирање < 16; внатрешно_поврзување_позиционирање++) if (статус_VALUE[внатрешно_поврзување_позиционирање] != 0 && почекај_VALUE[внатрешно_поврзување_позиционирање] == Loop_INDEX + 1) { почекај_VALUE[внатрешно_поврзување_позиционирање] = 0; return внатрешно_поврзување_позиционирање + 40; } return -11; }
    public static int Запиши(int 열린파일번호, int внес_COUNT) {
        int Loop_INDEX = провери(열린파일번호); if (Loop_INDEX < 0) return -9; if (статус_VALUE[Loop_INDEX] != 4) return -107;
        if (внес_COUNT < 0 || внес_COUNT > 512) return -22; if (внес_COUNT == 0) return 0;
        int внатрешно_поврзување_позиционирање = 짝[Loop_INDEX]; if (внатрешно_поврзување_позиционирање < 0) return -32; int 총수 = 1024 - 수[внатрешно_поврзување_позиционирање]; if (총수 == 0) return -11; if (총수 > внес_COUNT) 총수 = внес_COUNT;
        for (int Споредба_позиционирање = 0; Споредба_позиционирање < 총수; Споредба_позиционирање++) податоци[внатрешно_поврзување_позиционирање * 1024 + (предна_VALUE[внатрешно_поврзување_позиционирање] + 수[внатрешно_поврзување_позиционирање] + Споредба_позиционирање) % 1024] = 되돌림망.Напред_VALUE[Споредба_позиционирање]; 수[внатрешно_поврзување_позиционирање] += 총수; return 총수;
    }
    public static int Читај(int 열린파일번호, int внес_COUNT) {
        int Loop_INDEX = провери(열린파일번호); if (Loop_INDEX < 0) return -9; if (статус_VALUE[Loop_INDEX] != 4) return -107; if (внес_COUNT < 0 || внес_COUNT > 512) return -22;
        if (внес_COUNT == 0) return 0; if (수[Loop_INDEX] == 0) return 짝[Loop_INDEX] < 0 ? 0 : -11; if (внес_COUNT > 수[Loop_INDEX]) внес_COUNT = 수[Loop_INDEX];
        for (int Споредба_позиционирање = 0; Споредба_позиционирање < внес_COUNT; Споредба_позиционирање++) 되돌림망.Напред_VALUE[Споредба_позиционирање] = податоци[Loop_INDEX * 1024 + (предна_VALUE[Loop_INDEX] + Споредба_позиционирање) % 1024]; предна_VALUE[Loop_INDEX] = (предна_VALUE[Loop_INDEX] + внес_COUNT) % 1024; 수[Loop_INDEX] -= внес_COUNT; return внес_COUNT;
    }
    public static int 창구읽기(int 열린파일번호) { int Loop_INDEX = провери(열린파일번호); return Loop_INDEX < 0 ? -9 : порта_VALUE[Loop_INDEX]; }
    public static int 상대창구읽기(int 열린파일번호) { int Loop_INDEX = провери(열린파일번호); return Loop_INDEX < 0 ? -9 : рамноправен_уред_порта[Loop_INDEX]; }
    public static int Затвори(int 열린파일번호) {
        int Loop_INDEX = провери(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (статус_VALUE[Loop_INDEX] == 3) for (int внатрешно_поврзување_позиционирање = 0; внатрешно_поврзување_позиционирање < 16; внатрешно_поврзување_позиционирање++) if (почекај_VALUE[внатрешно_поврзување_позиционирање] == Loop_INDEX + 1) { if (짝[внатрешно_поврзување_позиционирање] >= 0) 짝[짝[внатрешно_поврзување_позиционирање]] = -1; статус_VALUE[внатрешно_поврзување_позиционирање] = почекај_VALUE[внатрешно_поврзување_позиционирање] = 묶임[внатрешно_поврзување_позиционирање] = 0; }
        if (짝[Loop_INDEX] >= 0) 짝[짝[Loop_INDEX]] = -1; статус_VALUE[Loop_INDEX] = 묶임[Loop_INDEX] = 수[Loop_INDEX] = почекај_VALUE[Loop_INDEX] = 0; return 0;
    }
}
