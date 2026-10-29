// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** tuum_VALUE 안의 연결형 bait_VALUE voog_VALUE. Ethernet/TCP 패킷 스택이 아닌 루프백 socket kiht_VALUE. */
public final class voog_võrk {
    static int[] Olek_VALUE = new int[16], port_VALUE = new int[16], 짝 = new int[16], partner_port = new int[16], Oota_VALUE = new int[16], infotehnoloogia_piir = new int[16];
    static int[] esikaamera_VALUE = new int[16], number = new int[16], andmed = new int[16 * 1024];
    static int Edasi_kaup = 50000;
    static int kinnitama(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && Olek_VALUE[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int pordinumber) { for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (Olek_VALUE[Loop_INDEX] != 0 && infotehnoloogia_piir[Loop_INDEX] != 0 && port_VALUE[Loop_INDEX] == pordinumber) return true; return false; }
    public static int avama_kirje() {
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (Olek_VALUE[Loop_INDEX] == 0) { Olek_VALUE[Loop_INDEX] = 1; partner_port[Loop_INDEX] = port_VALUE[Loop_INDEX] = esikaamera_VALUE[Loop_INDEX] = number[Loop_INDEX] = Oota_VALUE[Loop_INDEX] = infotehnoloogia_piir[Loop_INDEX] = 0; 짝[Loop_INDEX] = -1; return Loop_INDEX + 40; }
        return -24;
    }
    public static int BIND_osaleja(int 열린파일번호, int 통신주소, int pordinumber) {
        int Loop_INDEX = kinnitama(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (통신주소 != 0 && 통신주소 != 0x7f000001) return -99;
        if (Olek_VALUE[Loop_INDEX] != 1 || pordinumber < 0 || pordinumber > 65535) return -22;
        if (pordinumber == 0) { do { pordinumber = Edasi_kaup++; if (Edasi_kaup > 65535) Edasi_kaup = 50000; } while (사용중(pordinumber)); }
        if (사용중(pordinumber)) return -98; port_VALUE[Loop_INDEX] = pordinumber; infotehnoloogia_piir[Loop_INDEX] = 1; Olek_VALUE[Loop_INDEX] = 2; return 0;
    }
    public static int jälgima_osaleja(int 열린파일번호, int 연결대기한도) { int Loop_INDEX = kinnitama(열린파일번호); if (Loop_INDEX < 0) return -9; if (Olek_VALUE[Loop_INDEX] != 2 || 연결대기한도 < 1) return -22; Olek_VALUE[Loop_INDEX] = 3; return 0; }
    public static int Ühendu(int 열린파일번호, int 통신주소, int pordinumber) {
        int Loop_INDEX = kinnitama(열린파일번호); if (Loop_INDEX < 0) return -9; if (통신주소 != 0x7f000001) return -101;
        if (pordinumber < 1 || pordinumber > 65535 || Olek_VALUE[Loop_INDEX] > 2) return -22;
        int saama_leht = -1; for (int sisemine_ametikoht = 0; sisemine_ametikoht < 16; sisemine_ametikoht++) if (Olek_VALUE[sisemine_ametikoht] == 3 && port_VALUE[sisemine_ametikoht] == pordinumber) saama_leht = sisemine_ametikoht;
        if (saama_leht < 0) return -111;
        int 대기여부 = 0; for (int sisemine_ametikoht = 0; sisemine_ametikoht < 16; sisemine_ametikoht++) if (Oota_VALUE[sisemine_ametikoht] == saama_leht + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (Olek_VALUE[Loop_INDEX] == 1) { int 처리값 = BIND_osaleja(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int Muud = avama_kirje(); if (Muud < 0) return Muud; Muud -= 40;
        Olek_VALUE[Loop_INDEX] = Olek_VALUE[Muud] = 4; 짝[Loop_INDEX] = Muud; 짝[Muud] = Loop_INDEX; port_VALUE[Muud] = pordinumber; partner_port[Loop_INDEX] = pordinumber; partner_port[Muud] = port_VALUE[Loop_INDEX]; Oota_VALUE[Muud] = saama_leht + 1; return 0;
    }
    public static int aktsepteerima_ühendus(int 열린파일번호) { int Loop_INDEX = kinnitama(열린파일번호); if (Loop_INDEX < 0) return -9; if (Olek_VALUE[Loop_INDEX] != 3) return -22; for (int sisemine_ametikoht = 0; sisemine_ametikoht < 16; sisemine_ametikoht++) if (Olek_VALUE[sisemine_ametikoht] != 0 && Oota_VALUE[sisemine_ametikoht] == Loop_INDEX + 1) { Oota_VALUE[sisemine_ametikoht] = 0; return sisemine_ametikoht + 40; } return -11; }
    public static int Kirjutamine(int 열린파일번호, int kirje_COUNT) {
        int Loop_INDEX = kinnitama(열린파일번호); if (Loop_INDEX < 0) return -9; if (Olek_VALUE[Loop_INDEX] != 4) return -107;
        if (kirje_COUNT < 0 || kirje_COUNT > 512) return -22; if (kirje_COUNT == 0) return 0;
        int sisemine_ametikoht = 짝[Loop_INDEX]; if (sisemine_ametikoht < 0) return -32; int kokku_COUNT = 1024 - number[sisemine_ametikoht]; if (kokku_COUNT == 0) return -11; if (kokku_COUNT > kirje_COUNT) kokku_COUNT = kirje_COUNT;
        for (int Võrdlus_ametikoht = 0; Võrdlus_ametikoht < kokku_COUNT; Võrdlus_ametikoht++) andmed[sisemine_ametikoht * 1024 + (esikaamera_VALUE[sisemine_ametikoht] + number[sisemine_ametikoht] + Võrdlus_ametikoht) % 1024] = tagastusliides_võrk.Edasi_VALUE[Võrdlus_ametikoht]; number[sisemine_ametikoht] += kokku_COUNT; return kokku_COUNT;
    }
    public static int Lugemine(int 열린파일번호, int kirje_COUNT) {
        int Loop_INDEX = kinnitama(열린파일번호); if (Loop_INDEX < 0) return -9; if (Olek_VALUE[Loop_INDEX] != 4) return -107; if (kirje_COUNT < 0 || kirje_COUNT > 512) return -22;
        if (kirje_COUNT == 0) return 0; if (number[Loop_INDEX] == 0) return 짝[Loop_INDEX] < 0 ? 0 : -11; if (kirje_COUNT > number[Loop_INDEX]) kirje_COUNT = number[Loop_INDEX];
        for (int Võrdlus_ametikoht = 0; Võrdlus_ametikoht < kirje_COUNT; Võrdlus_ametikoht++) tagastusliides_võrk.Edasi_VALUE[Võrdlus_ametikoht] = andmed[Loop_INDEX * 1024 + (esikaamera_VALUE[Loop_INDEX] + Võrdlus_ametikoht) % 1024]; esikaamera_VALUE[Loop_INDEX] = (esikaamera_VALUE[Loop_INDEX] + kirje_COUNT) % 1024; number[Loop_INDEX] -= kirje_COUNT; return kirje_COUNT;
    }
    public static int 창구읽기(int 열린파일번호) { int Loop_INDEX = kinnitama(열린파일번호); return Loop_INDEX < 0 ? -9 : port_VALUE[Loop_INDEX]; }
    public static int 상대창구읽기(int 열린파일번호) { int Loop_INDEX = kinnitama(열린파일번호); return Loop_INDEX < 0 ? -9 : partner_port[Loop_INDEX]; }
    public static int Suletud(int 열린파일번호) {
        int Loop_INDEX = kinnitama(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (Olek_VALUE[Loop_INDEX] == 3) for (int sisemine_ametikoht = 0; sisemine_ametikoht < 16; sisemine_ametikoht++) if (Oota_VALUE[sisemine_ametikoht] == Loop_INDEX + 1) { if (짝[sisemine_ametikoht] >= 0) 짝[짝[sisemine_ametikoht]] = -1; Olek_VALUE[sisemine_ametikoht] = Oota_VALUE[sisemine_ametikoht] = infotehnoloogia_piir[sisemine_ametikoht] = 0; }
        if (짝[Loop_INDEX] >= 0) 짝[짝[Loop_INDEX]] = -1; Olek_VALUE[Loop_INDEX] = infotehnoloogia_piir[Loop_INDEX] = number[Loop_INDEX] = Oota_VALUE[Loop_INDEX] = 0; return 0;
    }
}
