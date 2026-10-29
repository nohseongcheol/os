// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** төш_VALUE 안의 연결형 байт_VALUE агым_VALUE. Ethernet/TCP 패킷 스택이 아닌 루프백 socket дәрәҗә_VALUE. */
public final class агым_Челтәр {
    static int[] халәт_VALUE = new int[16], порт_VALUE = new int[16], 짝 = new int[16], тиңдәш_порт = new int[16], 대기 = new int[16], 묶임 = new int[16];
    static int[] 앞 = new int[16], 수 = new int[16], мәгълүмат = new int[16 * 1024];
    static int Киләсе_элемент = 50000;
    static int раслау(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && халәт_VALUE[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int 접속번호) { for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (халәт_VALUE[Loop_INDEX] != 0 && 묶임[Loop_INDEX] != 0 && порт_VALUE[Loop_INDEX] == 접속번호) return true; return false; }
    public static int Төзү_кертү() {
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (халәт_VALUE[Loop_INDEX] == 0) { халәт_VALUE[Loop_INDEX] = 1; тиңдәш_порт[Loop_INDEX] = порт_VALUE[Loop_INDEX] = 앞[Loop_INDEX] = 수[Loop_INDEX] = 대기[Loop_INDEX] = 묶임[Loop_INDEX] = 0; 짝[Loop_INDEX] = -1; return Loop_INDEX + 40; }
        return -24;
    }
    public static int 묶기(int 열린파일번호, int 통신주소, int 접속번호) {
        int Loop_INDEX = раслау(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (통신주소 != 0 && 통신주소 != 0x7f000001) return -99;
        if (халәт_VALUE[Loop_INDEX] != 1 || 접속번호 < 0 || 접속번호 > 65535) return -22;
        if (접속번호 == 0) { do { 접속번호 = Киләсе_элемент++; if (Киләсе_элемент > 65535) Киләсе_элемент = 50000; } while (사용중(접속번호)); }
        if (사용중(접속번호)) return -98; порт_VALUE[Loop_INDEX] = 접속번호; 묶임[Loop_INDEX] = 1; халәт_VALUE[Loop_INDEX] = 2; return 0;
    }
    public static int 듣기(int 열린파일번호, int 연결대기한도) { int Loop_INDEX = раслау(열린파일번호); if (Loop_INDEX < 0) return -9; if (халәт_VALUE[Loop_INDEX] != 2 || 연결대기한도 < 1) return -22; халәт_VALUE[Loop_INDEX] = 3; return 0; }
    public static int ялгау(int 열린파일번호, int 통신주소, int 접속번호) {
        int Loop_INDEX = раслау(열린파일번호); if (Loop_INDEX < 0) return -9; if (통신주소 != 0x7f000001) return -101;
        if (접속번호 < 1 || 접속번호 > 65535 || халәт_VALUE[Loop_INDEX] > 2) return -22;
        int 수신쪽 = -1; for (int Эчке_берләштерү_урнаштыру = 0; Эчке_берләштерү_урнаштыру < 16; Эчке_берләштерү_урнаштыру++) if (халәт_VALUE[Эчке_берләштерү_урнаштыру] == 3 && порт_VALUE[Эчке_берләштерү_урнаштыру] == 접속번호) 수신쪽 = Эчке_берләштерү_урнаштыру;
        if (수신쪽 < 0) return -111;
        int 대기여부 = 0; for (int Эчке_берләштерү_урнаштыру = 0; Эчке_берләштерү_урнаштыру < 16; Эчке_берләштерү_урнаштыру++) if (대기[Эчке_берләштерү_урнаштыру] == 수신쪽 + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (халәт_VALUE[Loop_INDEX] == 1) { int 처리값 = 묶기(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int 다른번호 = Төзү_кертү(); if (다른번호 < 0) return 다른번호; 다른번호 -= 40;
        халәт_VALUE[Loop_INDEX] = халәт_VALUE[다른번호] = 4; 짝[Loop_INDEX] = 다른번호; 짝[다른번호] = Loop_INDEX; порт_VALUE[다른번호] = 접속번호; тиңдәш_порт[Loop_INDEX] = 접속번호; тиңдәш_порт[다른번호] = порт_VALUE[Loop_INDEX]; 대기[다른번호] = 수신쪽 + 1; return 0;
    }
    public static int кабул_итү_тоташу(int 열린파일번호) { int Loop_INDEX = раслау(열린파일번호); if (Loop_INDEX < 0) return -9; if (халәт_VALUE[Loop_INDEX] != 3) return -22; for (int Эчке_берләштерү_урнаштыру = 0; Эчке_берләштерү_урнаштыру < 16; Эчке_берләштерү_урнаштыру++) if (халәт_VALUE[Эчке_берләштерү_урнаштыру] != 0 && 대기[Эчке_берләштерү_урнаштыру] == Loop_INDEX + 1) { 대기[Эчке_берләштерү_урнаштыру] = 0; return Эчке_берләштерү_урнаштыру + 40; } return -11; }
    public static int язу(int 열린파일번호, int кертү_COUNT) {
        int Loop_INDEX = раслау(열린파일번호); if (Loop_INDEX < 0) return -9; if (халәт_VALUE[Loop_INDEX] != 4) return -107;
        if (кертү_COUNT < 0 || кертү_COUNT > 512) return -22; if (кертү_COUNT == 0) return 0;
        int Эчке_берләштерү_урнаштыру = 짝[Loop_INDEX]; if (Эчке_берләштерү_урнаштыру < 0) return -32; int 총수 = 1024 - 수[Эчке_берләштерү_урнаштыру]; if (총수 == 0) return -11; if (총수 > кертү_COUNT) 총수 = кертү_COUNT;
        for (int 비교자리 = 0; 비교자리 < 총수; 비교자리++) мәгълүмат[Эчке_берләштерү_урнаштыру * 1024 + (앞[Эчке_берләштерү_урнаштыру] + 수[Эчке_берләштерү_урнаштыру] + 비교자리) % 1024] = 되돌림망.Алга_VALUE[비교자리]; 수[Эчке_берләштерү_урнаштыру] += 총수; return 총수;
    }
    public static int 읽기(int 열린파일번호, int кертү_COUNT) {
        int Loop_INDEX = раслау(열린파일번호); if (Loop_INDEX < 0) return -9; if (халәт_VALUE[Loop_INDEX] != 4) return -107; if (кертү_COUNT < 0 || кертү_COUNT > 512) return -22;
        if (кертү_COUNT == 0) return 0; if (수[Loop_INDEX] == 0) return 짝[Loop_INDEX] < 0 ? 0 : -11; if (кертү_COUNT > 수[Loop_INDEX]) кертү_COUNT = 수[Loop_INDEX];
        for (int 비교자리 = 0; 비교자리 < кертү_COUNT; 비교자리++) 되돌림망.Алга_VALUE[비교자리] = мәгълүмат[Loop_INDEX * 1024 + (앞[Loop_INDEX] + 비교자리) % 1024]; 앞[Loop_INDEX] = (앞[Loop_INDEX] + кертү_COUNT) % 1024; 수[Loop_INDEX] -= кертү_COUNT; return кертү_COUNT;
    }
    public static int 창구읽기(int 열린파일번호) { int Loop_INDEX = раслау(열린파일번호); return Loop_INDEX < 0 ? -9 : порт_VALUE[Loop_INDEX]; }
    public static int 상대창구읽기(int 열린파일번호) { int Loop_INDEX = раслау(열린파일번호); return Loop_INDEX < 0 ? -9 : тиңдәш_порт[Loop_INDEX]; }
    public static int Yap(int 열린파일번호) {
        int Loop_INDEX = раслау(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (халәт_VALUE[Loop_INDEX] == 3) for (int Эчке_берләштерү_урнаштыру = 0; Эчке_берләштерү_урнаштыру < 16; Эчке_берләштерү_урнаштыру++) if (대기[Эчке_берләштерү_урнаштыру] == Loop_INDEX + 1) { if (짝[Эчке_берләштерү_урнаштыру] >= 0) 짝[짝[Эчке_берләштерү_урнаштыру]] = -1; халәт_VALUE[Эчке_берләштерү_урнаштыру] = 대기[Эчке_берләштерү_урнаштыру] = 묶임[Эчке_берләштерү_урнаштыру] = 0; }
        if (짝[Loop_INDEX] >= 0) 짝[짝[Loop_INDEX]] = -1; халәт_VALUE[Loop_INDEX] = 묶임[Loop_INDEX] = 수[Loop_INDEX] = 대기[Loop_INDEX] = 0; return 0;
    }
}
