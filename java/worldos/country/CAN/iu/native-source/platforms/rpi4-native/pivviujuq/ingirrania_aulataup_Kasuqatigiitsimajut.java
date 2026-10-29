// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** kernel_atuutilik 안의 연결형 byte_atuutilik ingirrania_aulataup_atuutilik. Ethernet/TCP 패킷 스택이 아닌 루프백 socket qaliriit_atuutilik. */
public final class ingirrania_aulataup_Kasuqatigiitsimajut {
    static int[] qanuilinganiq_atuutilik = new int[16], kapputigaq_atuutilik = new int[16], 짝 = new int[16], ilagijaujuq_kapputigaq = new int[16], 대기 = new int[16], 묶임 = new int[16];
    static int[] 앞 = new int[16], 수 = new int[16], titiqqat = new int[16 * 1024];
    static int 다음 = 50000;
    static int nalunairli_1aacb54c(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && qanuilinganiq_atuutilik[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int 접속번호) { for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 16; piliqqittaajuq_nalunaiqsimavik++) if (qanuilinganiq_atuutilik[piliqqittaajuq_nalunaiqsimavik] != 0 && 묶임[piliqqittaajuq_nalunaiqsimavik] != 0 && kapputigaq_atuutilik[piliqqittaajuq_nalunaiqsimavik] == 접속번호) return true; return false; }
    public static int 만들기() {
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 16; piliqqittaajuq_nalunaiqsimavik++) if (qanuilinganiq_atuutilik[piliqqittaajuq_nalunaiqsimavik] == 0) { qanuilinganiq_atuutilik[piliqqittaajuq_nalunaiqsimavik] = 1; ilagijaujuq_kapputigaq[piliqqittaajuq_nalunaiqsimavik] = kapputigaq_atuutilik[piliqqittaajuq_nalunaiqsimavik] = 앞[piliqqittaajuq_nalunaiqsimavik] = 수[piliqqittaajuq_nalunaiqsimavik] = 대기[piliqqittaajuq_nalunaiqsimavik] = 묶임[piliqqittaajuq_nalunaiqsimavik] = 0; 짝[piliqqittaajuq_nalunaiqsimavik] = -1; return piliqqittaajuq_nalunaiqsimavik + 40; }
        return -24;
    }
    public static int 묶기(int 열린파일번호, int 통신주소, int 접속번호) {
        int piliqqittaajuq_nalunaiqsimavik = nalunairli_1aacb54c(열린파일번호); if (piliqqittaajuq_nalunaiqsimavik < 0) return -9;
        if (통신주소 != 0 && 통신주소 != 0x7f000001) return -99;
        if (qanuilinganiq_atuutilik[piliqqittaajuq_nalunaiqsimavik] != 1 || 접속번호 < 0 || 접속번호 > 65535) return -22;
        if (접속번호 == 0) { do { 접속번호 = 다음++; if (다음 > 65535) 다음 = 50000; } while (사용중(접속번호)); }
        if (사용중(접속번호)) return -98; kapputigaq_atuutilik[piliqqittaajuq_nalunaiqsimavik] = 접속번호; 묶임[piliqqittaajuq_nalunaiqsimavik] = 1; qanuilinganiq_atuutilik[piliqqittaajuq_nalunaiqsimavik] = 2; return 0;
    }
    public static int 듣기(int 열린파일번호, int 연결대기한도) { int piliqqittaajuq_nalunaiqsimavik = nalunairli_1aacb54c(열린파일번호); if (piliqqittaajuq_nalunaiqsimavik < 0) return -9; if (qanuilinganiq_atuutilik[piliqqittaajuq_nalunaiqsimavik] != 2 || 연결대기한도 < 1) return -22; qanuilinganiq_atuutilik[piliqqittaajuq_nalunaiqsimavik] = 3; return 0; }
    public static int kasurli(int 열린파일번호, int 통신주소, int 접속번호) {
        int piliqqittaajuq_nalunaiqsimavik = nalunairli_1aacb54c(열린파일번호); if (piliqqittaajuq_nalunaiqsimavik < 0) return -9; if (통신주소 != 0x7f000001) return -101;
        if (접속번호 < 1 || 접속번호 > 65535 || qanuilinganiq_atuutilik[piliqqittaajuq_nalunaiqsimavik] > 2) return -22;
        int 수신쪽 = -1; for (int 안쪽자리 = 0; 안쪽자리 < 16; 안쪽자리++) if (qanuilinganiq_atuutilik[안쪽자리] == 3 && kapputigaq_atuutilik[안쪽자리] == 접속번호) 수신쪽 = 안쪽자리;
        if (수신쪽 < 0) return -111;
        int 대기여부 = 0; for (int 안쪽자리 = 0; 안쪽자리 < 16; 안쪽자리++) if (대기[안쪽자리] == 수신쪽 + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (qanuilinganiq_atuutilik[piliqqittaajuq_nalunaiqsimavik] == 1) { int 처리값 = 묶기(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int 다른번호 = 만들기(); if (다른번호 < 0) return 다른번호; 다른번호 -= 40;
        qanuilinganiq_atuutilik[piliqqittaajuq_nalunaiqsimavik] = qanuilinganiq_atuutilik[다른번호] = 4; 짝[piliqqittaajuq_nalunaiqsimavik] = 다른번호; 짝[다른번호] = piliqqittaajuq_nalunaiqsimavik; kapputigaq_atuutilik[다른번호] = 접속번호; ilagijaujuq_kapputigaq[piliqqittaajuq_nalunaiqsimavik] = 접속번호; ilagijaujuq_kapputigaq[다른번호] = kapputigaq_atuutilik[piliqqittaajuq_nalunaiqsimavik]; 대기[다른번호] = 수신쪽 + 1; return 0;
    }
    public static int 받음(int 열린파일번호) { int piliqqittaajuq_nalunaiqsimavik = nalunairli_1aacb54c(열린파일번호); if (piliqqittaajuq_nalunaiqsimavik < 0) return -9; if (qanuilinganiq_atuutilik[piliqqittaajuq_nalunaiqsimavik] != 3) return -22; for (int 안쪽자리 = 0; 안쪽자리 < 16; 안쪽자리++) if (qanuilinganiq_atuutilik[안쪽자리] != 0 && 대기[안쪽자리] == piliqqittaajuq_nalunaiqsimavik + 1) { 대기[안쪽자리] = 0; return 안쪽자리 + 40; } return -11; }
    public static int titiraq(int 열린파일번호, int 항목수) {
        int piliqqittaajuq_nalunaiqsimavik = nalunairli_1aacb54c(열린파일번호); if (piliqqittaajuq_nalunaiqsimavik < 0) return -9; if (qanuilinganiq_atuutilik[piliqqittaajuq_nalunaiqsimavik] != 4) return -107;
        if (항목수 < 0 || 항목수 > 512) return -22; if (항목수 == 0) return 0;
        int 안쪽자리 = 짝[piliqqittaajuq_nalunaiqsimavik]; if (안쪽자리 < 0) return -32; int 총수 = 1024 - 수[안쪽자리]; if (총수 == 0) return -11; if (총수 > 항목수) 총수 = 항목수;
        for (int 비교자리 = 0; 비교자리 < 총수; 비교자리++) titiqqat[안쪽자리 * 1024 + (앞[안쪽자리] + 수[안쪽자리] + 비교자리) % 1024] = 되돌림망.sivummualli_atuutilik[비교자리]; 수[안쪽자리] += 총수; return 총수;
    }
    public static int 읽기(int 열린파일번호, int 항목수) {
        int piliqqittaajuq_nalunaiqsimavik = nalunairli_1aacb54c(열린파일번호); if (piliqqittaajuq_nalunaiqsimavik < 0) return -9; if (qanuilinganiq_atuutilik[piliqqittaajuq_nalunaiqsimavik] != 4) return -107; if (항목수 < 0 || 항목수 > 512) return -22;
        if (항목수 == 0) return 0; if (수[piliqqittaajuq_nalunaiqsimavik] == 0) return 짝[piliqqittaajuq_nalunaiqsimavik] < 0 ? 0 : -11; if (항목수 > 수[piliqqittaajuq_nalunaiqsimavik]) 항목수 = 수[piliqqittaajuq_nalunaiqsimavik];
        for (int 비교자리 = 0; 비교자리 < 항목수; 비교자리++) 되돌림망.sivummualli_atuutilik[비교자리] = titiqqat[piliqqittaajuq_nalunaiqsimavik * 1024 + (앞[piliqqittaajuq_nalunaiqsimavik] + 비교자리) % 1024]; 앞[piliqqittaajuq_nalunaiqsimavik] = (앞[piliqqittaajuq_nalunaiqsimavik] + 항목수) % 1024; 수[piliqqittaajuq_nalunaiqsimavik] -= 항목수; return 항목수;
    }
    public static int 창구읽기(int 열린파일번호) { int piliqqittaajuq_nalunaiqsimavik = nalunairli_1aacb54c(열린파일번호); return piliqqittaajuq_nalunaiqsimavik < 0 ? -9 : kapputigaq_atuutilik[piliqqittaajuq_nalunaiqsimavik]; }
    public static int 상대창구읽기(int 열린파일번호) { int piliqqittaajuq_nalunaiqsimavik = nalunairli_1aacb54c(열린파일번호); return piliqqittaajuq_nalunaiqsimavik < 0 ? -9 : ilagijaujuq_kapputigaq[piliqqittaajuq_nalunaiqsimavik]; }
    public static int matuli(int 열린파일번호) {
        int piliqqittaajuq_nalunaiqsimavik = nalunairli_1aacb54c(열린파일번호); if (piliqqittaajuq_nalunaiqsimavik < 0) return -9;
        if (qanuilinganiq_atuutilik[piliqqittaajuq_nalunaiqsimavik] == 3) for (int 안쪽자리 = 0; 안쪽자리 < 16; 안쪽자리++) if (대기[안쪽자리] == piliqqittaajuq_nalunaiqsimavik + 1) { if (짝[안쪽자리] >= 0) 짝[짝[안쪽자리]] = -1; qanuilinganiq_atuutilik[안쪽자리] = 대기[안쪽자리] = 묶임[안쪽자리] = 0; }
        if (짝[piliqqittaajuq_nalunaiqsimavik] >= 0) 짝[짝[piliqqittaajuq_nalunaiqsimavik]] = -1; qanuilinganiq_atuutilik[piliqqittaajuq_nalunaiqsimavik] = 묶임[piliqqittaajuq_nalunaiqsimavik] = 수[piliqqittaajuq_nalunaiqsimavik] = 대기[piliqqittaajuq_nalunaiqsimavik] = 0; return 0;
    }
}
