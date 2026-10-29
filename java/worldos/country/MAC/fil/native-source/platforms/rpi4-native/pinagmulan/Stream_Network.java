// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** kernel_VALUE 안의 연결형 byte_VALUE Stream_VALUE. Ethernet/TCP 패킷 스택이 아닌 루프백 socket patong_VALUE. */
public final class Stream_Network {
    static int[] katayuan_VALUE = new int[16], port_VALUE = new int[16], 짝 = new int[16], peer_port = new int[16], maghintay_VALUE = new int[16], 묶임 = new int[16];
    static int[] nasa_harap_VALUE = new int[16], 수 = new int[16], data = new int[16 * 1024];
    static int Susunod_item = 50000;
    static int tiyakin_kumpirmahin(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && katayuan_VALUE[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int numero_ng_port) { for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (katayuan_VALUE[Loop_INDEX] != 0 && 묶임[Loop_INDEX] != 0 && port_VALUE[Loop_INDEX] == numero_ng_port) return true; return false; }
    public static int Create_pagpasok() {
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (katayuan_VALUE[Loop_INDEX] == 0) { katayuan_VALUE[Loop_INDEX] = 1; peer_port[Loop_INDEX] = port_VALUE[Loop_INDEX] = nasa_harap_VALUE[Loop_INDEX] = 수[Loop_INDEX] = maghintay_VALUE[Loop_INDEX] = 묶임[Loop_INDEX] = 0; 짝[Loop_INDEX] = -1; return Loop_INDEX + 40; }
        return -24;
    }
    public static int 묶기(int 열린파일번호, int 통신주소, int numero_ng_port) {
        int Loop_INDEX = tiyakin_kumpirmahin(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (통신주소 != 0 && 통신주소 != 0x7f000001) return -99;
        if (katayuan_VALUE[Loop_INDEX] != 1 || numero_ng_port < 0 || numero_ng_port > 65535) return -22;
        if (numero_ng_port == 0) { do { numero_ng_port = Susunod_item++; if (Susunod_item > 65535) Susunod_item = 50000; } while (사용중(numero_ng_port)); }
        if (사용중(numero_ng_port)) return -98; port_VALUE[Loop_INDEX] = numero_ng_port; 묶임[Loop_INDEX] = 1; katayuan_VALUE[Loop_INDEX] = 2; return 0;
    }
    public static int 듣기(int 열린파일번호, int 연결대기한도) { int Loop_INDEX = tiyakin_kumpirmahin(열린파일번호); if (Loop_INDEX < 0) return -9; if (katayuan_VALUE[Loop_INDEX] != 2 || 연결대기한도 < 1) return -22; katayuan_VALUE[Loop_INDEX] = 3; return 0; }
    public static int CONNECT(int 열린파일번호, int 통신주소, int numero_ng_port) {
        int Loop_INDEX = tiyakin_kumpirmahin(열린파일번호); if (Loop_INDEX < 0) return -9; if (통신주소 != 0x7f000001) return -101;
        if (numero_ng_port < 1 || numero_ng_port > 65535 || katayuan_VALUE[Loop_INDEX] > 2) return -22;
        int 수신쪽 = -1; for (int inner_join_posisyon = 0; inner_join_posisyon < 16; inner_join_posisyon++) if (katayuan_VALUE[inner_join_posisyon] == 3 && port_VALUE[inner_join_posisyon] == numero_ng_port) 수신쪽 = inner_join_posisyon;
        if (수신쪽 < 0) return -111;
        int 대기여부 = 0; for (int inner_join_posisyon = 0; inner_join_posisyon < 16; inner_join_posisyon++) if (maghintay_VALUE[inner_join_posisyon] == 수신쪽 + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (katayuan_VALUE[Loop_INDEX] == 1) { int 처리값 = 묶기(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int 다른번호 = Create_pagpasok(); if (다른번호 < 0) return 다른번호; 다른번호 -= 40;
        katayuan_VALUE[Loop_INDEX] = katayuan_VALUE[다른번호] = 4; 짝[Loop_INDEX] = 다른번호; 짝[다른번호] = Loop_INDEX; port_VALUE[다른번호] = numero_ng_port; peer_port[Loop_INDEX] = numero_ng_port; peer_port[다른번호] = port_VALUE[Loop_INDEX]; maghintay_VALUE[다른번호] = 수신쪽 + 1; return 0;
    }
    public static int tanggapin_koneksyon(int 열린파일번호) { int Loop_INDEX = tiyakin_kumpirmahin(열린파일번호); if (Loop_INDEX < 0) return -9; if (katayuan_VALUE[Loop_INDEX] != 3) return -22; for (int inner_join_posisyon = 0; inner_join_posisyon < 16; inner_join_posisyon++) if (katayuan_VALUE[inner_join_posisyon] != 0 && maghintay_VALUE[inner_join_posisyon] == Loop_INDEX + 1) { maghintay_VALUE[inner_join_posisyon] = 0; return inner_join_posisyon + 40; } return -11; }
    public static int sumulat(int 열린파일번호, int pagpasok_COUNT) {
        int Loop_INDEX = tiyakin_kumpirmahin(열린파일번호); if (Loop_INDEX < 0) return -9; if (katayuan_VALUE[Loop_INDEX] != 4) return -107;
        if (pagpasok_COUNT < 0 || pagpasok_COUNT > 512) return -22; if (pagpasok_COUNT == 0) return 0;
        int inner_join_posisyon = 짝[Loop_INDEX]; if (inner_join_posisyon < 0) return -32; int 총수 = 1024 - 수[inner_join_posisyon]; if (총수 == 0) return -11; if (총수 > pagpasok_COUNT) 총수 = pagpasok_COUNT;
        for (int Paghahambing_posisyon = 0; Paghahambing_posisyon < 총수; Paghahambing_posisyon++) data[inner_join_posisyon * 1024 + (nasa_harap_VALUE[inner_join_posisyon] + 수[inner_join_posisyon] + Paghahambing_posisyon) % 1024] = 되돌림망.ipasa_VALUE_24592b8a[Paghahambing_posisyon]; 수[inner_join_posisyon] += 총수; return 총수;
    }
    public static int 읽기(int 열린파일번호, int pagpasok_COUNT) {
        int Loop_INDEX = tiyakin_kumpirmahin(열린파일번호); if (Loop_INDEX < 0) return -9; if (katayuan_VALUE[Loop_INDEX] != 4) return -107; if (pagpasok_COUNT < 0 || pagpasok_COUNT > 512) return -22;
        if (pagpasok_COUNT == 0) return 0; if (수[Loop_INDEX] == 0) return 짝[Loop_INDEX] < 0 ? 0 : -11; if (pagpasok_COUNT > 수[Loop_INDEX]) pagpasok_COUNT = 수[Loop_INDEX];
        for (int Paghahambing_posisyon = 0; Paghahambing_posisyon < pagpasok_COUNT; Paghahambing_posisyon++) 되돌림망.ipasa_VALUE_24592b8a[Paghahambing_posisyon] = data[Loop_INDEX * 1024 + (nasa_harap_VALUE[Loop_INDEX] + Paghahambing_posisyon) % 1024]; nasa_harap_VALUE[Loop_INDEX] = (nasa_harap_VALUE[Loop_INDEX] + pagpasok_COUNT) % 1024; 수[Loop_INDEX] -= pagpasok_COUNT; return pagpasok_COUNT;
    }
    public static int 창구읽기(int 열린파일번호) { int Loop_INDEX = tiyakin_kumpirmahin(열린파일번호); return Loop_INDEX < 0 ? -9 : port_VALUE[Loop_INDEX]; }
    public static int 상대창구읽기(int 열린파일번호) { int Loop_INDEX = tiyakin_kumpirmahin(열린파일번호); return Loop_INDEX < 0 ? -9 : peer_port[Loop_INDEX]; }
    public static int isara(int 열린파일번호) {
        int Loop_INDEX = tiyakin_kumpirmahin(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (katayuan_VALUE[Loop_INDEX] == 3) for (int inner_join_posisyon = 0; inner_join_posisyon < 16; inner_join_posisyon++) if (maghintay_VALUE[inner_join_posisyon] == Loop_INDEX + 1) { if (짝[inner_join_posisyon] >= 0) 짝[짝[inner_join_posisyon]] = -1; katayuan_VALUE[inner_join_posisyon] = maghintay_VALUE[inner_join_posisyon] = 묶임[inner_join_posisyon] = 0; }
        if (짝[Loop_INDEX] >= 0) 짝[짝[Loop_INDEX]] = -1; katayuan_VALUE[Loop_INDEX] = 묶임[Loop_INDEX] = 수[Loop_INDEX] = maghintay_VALUE[Loop_INDEX] = 0; return 0;
    }
}
