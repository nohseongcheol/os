// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** o_zak_VALUE 안의 연결형 bayt_VALUE oqim_VALUE. Ethernet/TCP 패킷 스택이 아닌 루프백 socket qatlam_VALUE. */
public final class oqim_Tarmoq {
    static int[] holat_VALUE_e10195a1 = new int[16], port_VALUE = new int[16], 짝 = new int[16], bir_rangli_port = new int[16], bir_daqiqa_VALUE = new int[16], 묶임 = new int[16];
    static int[] old_kamera_VALUE = new int[16], 수 = new int[16], ma_lumotlar = new int[16 * 1024];
    static int Keyingi_element = 50000;
    static int tasdiqlamoq(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && holat_VALUE_e10195a1[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int 접속번호) { for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (holat_VALUE_e10195a1[Loop_INDEX] != 0 && 묶임[Loop_INDEX] != 0 && port_VALUE[Loop_INDEX] == 접속번호) return true; return false; }
    public static int Yaratish_kiritish() {
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (holat_VALUE_e10195a1[Loop_INDEX] == 0) { holat_VALUE_e10195a1[Loop_INDEX] = 1; bir_rangli_port[Loop_INDEX] = port_VALUE[Loop_INDEX] = old_kamera_VALUE[Loop_INDEX] = 수[Loop_INDEX] = bir_daqiqa_VALUE[Loop_INDEX] = 묶임[Loop_INDEX] = 0; 짝[Loop_INDEX] = -1; return Loop_INDEX + 40; }
        return -24;
    }
    public static int 묶기(int 열린파일번호, int 통신주소, int 접속번호) {
        int Loop_INDEX = tasdiqlamoq(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (통신주소 != 0 && 통신주소 != 0x7f000001) return -99;
        if (holat_VALUE_e10195a1[Loop_INDEX] != 1 || 접속번호 < 0 || 접속번호 > 65535) return -22;
        if (접속번호 == 0) { do { 접속번호 = Keyingi_element++; if (Keyingi_element > 65535) Keyingi_element = 50000; } while (사용중(접속번호)); }
        if (사용중(접속번호)) return -98; port_VALUE[Loop_INDEX] = 접속번호; 묶임[Loop_INDEX] = 1; holat_VALUE_e10195a1[Loop_INDEX] = 2; return 0;
    }
    public static int 듣기(int 열린파일번호, int 연결대기한도) { int Loop_INDEX = tasdiqlamoq(열린파일번호); if (Loop_INDEX < 0) return -9; if (holat_VALUE_e10195a1[Loop_INDEX] != 2 || 연결대기한도 < 1) return -22; holat_VALUE_e10195a1[Loop_INDEX] = 3; return 0; }
    public static int Ulanish(int 열린파일번호, int 통신주소, int 접속번호) {
        int Loop_INDEX = tasdiqlamoq(열린파일번호); if (Loop_INDEX < 0) return -9; if (통신주소 != 0x7f000001) return -101;
        if (접속번호 < 1 || 접속번호 > 65535 || holat_VALUE_e10195a1[Loop_INDEX] > 2) return -22;
        int 수신쪽 = -1; for (int ichki_qo_shilish_holat = 0; ichki_qo_shilish_holat < 16; ichki_qo_shilish_holat++) if (holat_VALUE_e10195a1[ichki_qo_shilish_holat] == 3 && port_VALUE[ichki_qo_shilish_holat] == 접속번호) 수신쪽 = ichki_qo_shilish_holat;
        if (수신쪽 < 0) return -111;
        int 대기여부 = 0; for (int ichki_qo_shilish_holat = 0; ichki_qo_shilish_holat < 16; ichki_qo_shilish_holat++) if (bir_daqiqa_VALUE[ichki_qo_shilish_holat] == 수신쪽 + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (holat_VALUE_e10195a1[Loop_INDEX] == 1) { int 처리값 = 묶기(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int 다른번호 = Yaratish_kiritish(); if (다른번호 < 0) return 다른번호; 다른번호 -= 40;
        holat_VALUE_e10195a1[Loop_INDEX] = holat_VALUE_e10195a1[다른번호] = 4; 짝[Loop_INDEX] = 다른번호; 짝[다른번호] = Loop_INDEX; port_VALUE[다른번호] = 접속번호; bir_rangli_port[Loop_INDEX] = 접속번호; bir_rangli_port[다른번호] = port_VALUE[Loop_INDEX]; bir_daqiqa_VALUE[다른번호] = 수신쪽 + 1; return 0;
    }
    public static int qabul_qilish_aloqa(int 열린파일번호) { int Loop_INDEX = tasdiqlamoq(열린파일번호); if (Loop_INDEX < 0) return -9; if (holat_VALUE_e10195a1[Loop_INDEX] != 3) return -22; for (int ichki_qo_shilish_holat = 0; ichki_qo_shilish_holat < 16; ichki_qo_shilish_holat++) if (holat_VALUE_e10195a1[ichki_qo_shilish_holat] != 0 && bir_daqiqa_VALUE[ichki_qo_shilish_holat] == Loop_INDEX + 1) { bir_daqiqa_VALUE[ichki_qo_shilish_holat] = 0; return ichki_qo_shilish_holat + 40; } return -11; }
    public static int Yozish(int 열린파일번호, int kiritish_COUNT) {
        int Loop_INDEX = tasdiqlamoq(열린파일번호); if (Loop_INDEX < 0) return -9; if (holat_VALUE_e10195a1[Loop_INDEX] != 4) return -107;
        if (kiritish_COUNT < 0 || kiritish_COUNT > 512) return -22; if (kiritish_COUNT == 0) return 0;
        int ichki_qo_shilish_holat = 짝[Loop_INDEX]; if (ichki_qo_shilish_holat < 0) return -32; int 총수 = 1024 - 수[ichki_qo_shilish_holat]; if (총수 == 0) return -11; if (총수 > kiritish_COUNT) 총수 = kiritish_COUNT;
        for (int Taqqoslama_holat = 0; Taqqoslama_holat < 총수; Taqqoslama_holat++) ma_lumotlar[ichki_qo_shilish_holat * 1024 + (old_kamera_VALUE[ichki_qo_shilish_holat] + 수[ichki_qo_shilish_holat] + Taqqoslama_holat) % 1024] = 되돌림망.Oldinga_VALUE[Taqqoslama_holat]; 수[ichki_qo_shilish_holat] += 총수; return 총수;
    }
    public static int Oʻqish(int 열린파일번호, int kiritish_COUNT) {
        int Loop_INDEX = tasdiqlamoq(열린파일번호); if (Loop_INDEX < 0) return -9; if (holat_VALUE_e10195a1[Loop_INDEX] != 4) return -107; if (kiritish_COUNT < 0 || kiritish_COUNT > 512) return -22;
        if (kiritish_COUNT == 0) return 0; if (수[Loop_INDEX] == 0) return 짝[Loop_INDEX] < 0 ? 0 : -11; if (kiritish_COUNT > 수[Loop_INDEX]) kiritish_COUNT = 수[Loop_INDEX];
        for (int Taqqoslama_holat = 0; Taqqoslama_holat < kiritish_COUNT; Taqqoslama_holat++) 되돌림망.Oldinga_VALUE[Taqqoslama_holat] = ma_lumotlar[Loop_INDEX * 1024 + (old_kamera_VALUE[Loop_INDEX] + Taqqoslama_holat) % 1024]; old_kamera_VALUE[Loop_INDEX] = (old_kamera_VALUE[Loop_INDEX] + kiritish_COUNT) % 1024; 수[Loop_INDEX] -= kiritish_COUNT; return kiritish_COUNT;
    }
    public static int 창구읽기(int 열린파일번호) { int Loop_INDEX = tasdiqlamoq(열린파일번호); return Loop_INDEX < 0 ? -9 : port_VALUE[Loop_INDEX]; }
    public static int 상대창구읽기(int 열린파일번호) { int Loop_INDEX = tasdiqlamoq(열린파일번호); return Loop_INDEX < 0 ? -9 : bir_rangli_port[Loop_INDEX]; }
    public static int Yopish(int 열린파일번호) {
        int Loop_INDEX = tasdiqlamoq(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (holat_VALUE_e10195a1[Loop_INDEX] == 3) for (int ichki_qo_shilish_holat = 0; ichki_qo_shilish_holat < 16; ichki_qo_shilish_holat++) if (bir_daqiqa_VALUE[ichki_qo_shilish_holat] == Loop_INDEX + 1) { if (짝[ichki_qo_shilish_holat] >= 0) 짝[짝[ichki_qo_shilish_holat]] = -1; holat_VALUE_e10195a1[ichki_qo_shilish_holat] = bir_daqiqa_VALUE[ichki_qo_shilish_holat] = 묶임[ichki_qo_shilish_holat] = 0; }
        if (짝[Loop_INDEX] >= 0) 짝[짝[Loop_INDEX]] = -1; holat_VALUE_e10195a1[Loop_INDEX] = 묶임[Loop_INDEX] = 수[Loop_INDEX] = bir_daqiqa_VALUE[Loop_INDEX] = 0; return 0;
    }
}
