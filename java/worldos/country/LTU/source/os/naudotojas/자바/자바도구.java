// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 Įrankiai 공통 Išvestis 및 ASCII Failas Pavadinimas_2 Procesas_VALUE_įrašas. */
public final class 자바도구 {
    /** UTF-8 baitas_VALUE 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 atmesti_VALUE. */
    static int 원문해독(int[] duomenys, int 길이) {
        int Skaitymas = 0, Rašymas = 0;
        if (길이 >= 3 && duomenys[0] == 239 && duomenys[1] == 187 && duomenys[2] == 191) Skaitymas = 3;
        while (Skaitymas < 길이) {
            int VALUE = duomenys[Skaitymas++], numeris = 0, 최소 = 0;
            if (VALUE >= 194 && VALUE <= 223) { numeris = 1; 최소 = 128; VALUE &= 31; }
            else if (VALUE >= 224 && VALUE <= 239) { numeris = 2; 최소 = 2048; VALUE &= 15; }
            else if (VALUE >= 240 && VALUE <= 244) { numeris = 3; 최소 = 65536; VALUE &= 7; }
            else if (VALUE >= 128 || VALUE < 0) return -1;
            if (numeris > 길이 - Skaitymas) return -1;
            for (int i = 0; i < numeris; i++) {
                int toliau_prekė = duomenys[Skaitymas++]; if ((toliau_prekė & 192) != 128) return -1;
                VALUE = (VALUE << 6) | (toliau_prekė & 63);
            }
            if (VALUE < 최소 || VALUE > 0x10ffff || (VALUE >= 0xd800 && VALUE <= 0xdfff)) return -1;
            if (VALUE >= 65536) { VALUE -= 65536; duomenys[Rašymas++] = 0xd800 | (VALUE >> 10); duomenys[Rašymas++] = 0xdc00 | (VALUE & 1023); }
            else duomenys[Rašymas++] = VALUE;
        }
        return Rašymas;
    }
    static void rašymas_numeris(int VALUE) {
        if (VALUE < 0) naudotojas.rašymas_simbolis_VALUE('-'); else VALUE = -VALUE;
        int vietos_rodyklė = 1000000000;
        boolean Paleisti = false;
        while (vietos_rodyklė != 0) {
            int numeris = -(VALUE / vietos_rodyklė);
            if (numeris != 0 || Paleisti || vietos_rodyklė == 1) { naudotojas.rašymas_simbolis_VALUE('0' + numeris); Paleisti = true; }
            VALUE %= vietos_rodyklė; vietos_rodyklė /= 10;
        }
    }
    static int Pavadinimas_2(int[] vieta_VALUE, String 원본) {
        if (원본.length() >= vieta_VALUE.length) return -1;
        for (int numeris = 0; numeris < vieta_VALUE.length; numeris++) vieta_VALUE[numeris] = numeris < 원본.length() ? 원본.charAt(numeris) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String SECOND_operandas) {
        if (가.length() != SECOND_operandas.length()) return false;
        for (int numeris = 0; numeris < 가.length(); numeris++) if (가.charAt(numeris) != SECOND_operandas.charAt(numeris)) return false;
        return true;
    }
}
