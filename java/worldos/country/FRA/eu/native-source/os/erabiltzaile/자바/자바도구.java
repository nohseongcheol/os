// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 Tresnak 공통 Irteera 및 ASCII Fitxategia Izena prozesu_balio_sarrera. */
public final class 자바도구 {
    /** UTF-8 byte_balio 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 baztertu_balio. */
    static int 원문해독(int[] datuak, int luzera_balio) {
        int Irakurri = 0, Idatzi = 0;
        if (luzera_balio >= 3 && datuak[0] == 239 && datuak[1] == 187 && datuak[2] == 191) Irakurri = 3;
        while (Irakurri < luzera_balio) {
            int balio = datuak[Irakurri++], 수 = 0, 최소 = 0;
            if (balio >= 194 && balio <= 223) { 수 = 1; 최소 = 128; balio &= 31; }
            else if (balio >= 224 && balio <= 239) { 수 = 2; 최소 = 2048; balio &= 15; }
            else if (balio >= 240 && balio <= 244) { 수 = 3; 최소 = 65536; balio &= 7; }
            else if (balio >= 128 || balio < 0) return -1;
            if (수 > luzera_balio - Irakurri) return -1;
            for (int i = 0; i < 수; i++) {
                int Hurrengoa_elementu = datuak[Irakurri++]; if ((Hurrengoa_elementu & 192) != 128) return -1;
                balio = (balio << 6) | (Hurrengoa_elementu & 63);
            }
            if (balio < 최소 || balio > 0x10ffff || (balio >= 0xd800 && balio <= 0xdfff)) return -1;
            if (balio >= 65536) { balio -= 65536; datuak[Idatzi++] = 0xd800 | (balio >> 10); datuak[Idatzi++] = 0xdc00 | (balio & 1023); }
            else datuak[Idatzi++] = balio;
        }
        return Idatzi;
    }
    static void 수쓰기(int balio) {
        if (balio < 0) erabiltzaile.idatzi_karaktere_balio('-'); else balio = -balio;
        int kargu_INDIZE = 1000000000;
        boolean Exekutatu_2 = false;
        while (kargu_INDIZE != 0) {
            int 수 = -(balio / kargu_INDIZE);
            if (수 != 0 || Exekutatu_2 || kargu_INDIZE == 1) { erabiltzaile.idatzi_karaktere_balio('0' + 수); Exekutatu_2 = true; }
            balio %= kargu_INDIZE; kargu_INDIZE /= 10;
        }
    }
    static int Izena(int[] helburu_balio_a0fbc067, String 원본) {
        if (원본.length() >= helburu_balio_a0fbc067.length) return -1;
        for (int 수 = 0; 수 < helburu_balio_a0fbc067.length; 수++) helburu_balio_a0fbc067[수] = 수 < 원본.length() ? 원본.charAt(수) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String 나) {
        if (가.length() != 나.length()) return false;
        for (int 수 = 0; 수 < 가.length(); 수++) if (가.charAt(수) != 나.charAt(수)) return false;
        return true;
    }
}
