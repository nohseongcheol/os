// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 työkalut 공통 tulostuspaikka 및 ASCII tiedoston_nimi Nimi prosessi_ARVO_merkintä. */
public final class 자바도구 {
    /** UTF-8 tavu_ARVO 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 hylkää_ARVO_e3ecc00b. */
    static int 원문해독(int[] data, int kesto_ARVO) {
        int Luku = 0, Kirjoitus = 0;
        if (kesto_ARVO >= 3 && data[0] == 239 && data[1] == 187 && data[2] == 191) Luku = 3;
        while (Luku < kesto_ARVO) {
            int ARVO = data[Luku++], numero = 0, 최소 = 0;
            if (ARVO >= 194 && ARVO <= 223) { numero = 1; 최소 = 128; ARVO &= 31; }
            else if (ARVO >= 224 && ARVO <= 239) { numero = 2; 최소 = 2048; ARVO &= 15; }
            else if (ARVO >= 240 && ARVO <= 244) { numero = 3; 최소 = 65536; ARVO &= 7; }
            else if (ARVO >= 128 || ARVO < 0) return -1;
            if (numero > kesto_ARVO - Luku) return -1;
            for (int i = 0; i < numero; i++) {
                int Seuraava_kohde = data[Luku++]; if ((Seuraava_kohde & 192) != 128) return -1;
                ARVO = (ARVO << 6) | (Seuraava_kohde & 63);
            }
            if (ARVO < 최소 || ARVO > 0x10ffff || (ARVO >= 0xd800 && ARVO <= 0xdfff)) return -1;
            if (ARVO >= 65536) { ARVO -= 65536; data[Kirjoitus++] = 0xd800 | (ARVO >> 10); data[Kirjoitus++] = 0xdc00 | (ARVO & 1023); }
            else data[Kirjoitus++] = ARVO;
        }
        return Kirjoitus;
    }
    static void kirjoitus_numero(int ARVO) {
        if (ARVO < 0) käyttäjätila.kirjoitus_merkki_ARVO('-'); else ARVO = -ARVO;
        int sijainti = 1000000000;
        boolean Suorita_2 = false;
        while (sijainti != 0) {
            int numero = -(ARVO / sijainti);
            if (numero != 0 || Suorita_2 || sijainti == 1) { käyttäjätila.kirjoitus_merkki_ARVO('0' + numero); Suorita_2 = true; }
            ARVO %= sijainti; sijainti /= 10;
        }
    }
    static int Nimi(int[] kohde_ARVO, String 원본) {
        if (원본.length() >= kohde_ARVO.length) return -1;
        for (int numero = 0; numero < kohde_ARVO.length; numero++) kohde_ARVO[numero] = numero < 원본.length() ? 원본.charAt(numero) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String SEKUNNIT_operandi) {
        if (가.length() != SEKUNNIT_operandi.length()) return false;
        for (int numero = 0; numero < 가.length(); numero++) if (가.charAt(numero) != SEKUNNIT_operandi.charAt(numero)) return false;
        return true;
    }
}
