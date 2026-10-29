// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 Tööriistad 공통 Väljund 및 ASCII Fail Nimi_2 Joonis_VALUE_kirje. */
public final class 자바도구 {
    /** UTF-8 bait_VALUE 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 keelduma_VALUE. */
    static int 원문해독(int[] andmed, int 길이) {
        int Lugemine = 0, Kirjutamine = 0;
        if (길이 >= 3 && andmed[0] == 239 && andmed[1] == 187 && andmed[2] == 191) Lugemine = 3;
        while (Lugemine < 길이) {
            int VALUE = andmed[Lugemine++], number = 0, 최소 = 0;
            if (VALUE >= 194 && VALUE <= 223) { number = 1; 최소 = 128; VALUE &= 31; }
            else if (VALUE >= 224 && VALUE <= 239) { number = 2; 최소 = 2048; VALUE &= 15; }
            else if (VALUE >= 240 && VALUE <= 244) { number = 3; 최소 = 65536; VALUE &= 7; }
            else if (VALUE >= 128 || VALUE < 0) return -1;
            if (number > 길이 - Lugemine) return -1;
            for (int i = 0; i < number; i++) {
                int Edasi_kaup = andmed[Lugemine++]; if ((Edasi_kaup & 192) != 128) return -1;
                VALUE = (VALUE << 6) | (Edasi_kaup & 63);
            }
            if (VALUE < 최소 || VALUE > 0x10ffff || (VALUE >= 0xd800 && VALUE <= 0xdfff)) return -1;
            if (VALUE >= 65536) { VALUE -= 65536; andmed[Kirjutamine++] = 0xd800 | (VALUE >> 10); andmed[Kirjutamine++] = 0xdc00 | (VALUE & 1023); }
            else andmed[Kirjutamine++] = VALUE;
        }
        return Kirjutamine;
    }
    static void kirjutamine_number(int VALUE) {
        if (VALUE < 0) kasutaja.kirjutamine_märk_VALUE('-'); else VALUE = -VALUE;
        int asukohaindeks = 1000000000;
        boolean Käivita_2 = false;
        while (asukohaindeks != 0) {
            int number = -(VALUE / asukohaindeks);
            if (number != 0 || Käivita_2 || asukohaindeks == 1) { kasutaja.kirjutamine_märk_VALUE('0' + number); Käivita_2 = true; }
            VALUE %= asukohaindeks; asukohaindeks /= 10;
        }
    }
    static int Nimi_2(int[] sihtkoht_VALUE, String 원본) {
        if (원본.length() >= sihtkoht_VALUE.length) return -1;
        for (int number = 0; number < sihtkoht_VALUE.length; number++) sihtkoht_VALUE[number] = number < 원본.length() ? 원본.charAt(number) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String SECOND_operand) {
        if (가.length() != SECOND_operand.length()) return false;
        for (int number = 0; number < 가.length(); number++) if (가.charAt(number) != SECOND_operand.charAt(number)) return false;
        return true;
    }
}
