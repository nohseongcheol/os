// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Lugemine 전용 Täida_käsk 묶음의 ELF32 valideerima, Argumendid Edasi_VALUE, 한 번에 한 kasutaja Joonis_VALUE Täida_käsk. */
public final class 실행관리 {
    static final int START_kasutaja_programm = 0x04000000;
    static final int kasutaja_lõpeta_kõne = 0x04400000;
    static final int pilt_lõpeta_kõne_ADDRESS = 0x04200000;
    static final int argument_START = 0x04300000;
    static int argument_COUNT = 0;
    static int[] argument_ADDRESS = new int[16];

    static boolean klipp(int ADDRESS, int 길이) {
        return ADDRESS >= START_kasutaja_programm && ADDRESS < kasutaja_lõpeta_kõne && 길이 >= 0 && 길이 <= kasutaja_lõpeta_kõne - ADDRESS;
    }

    static int number(int ADDRESS) { return Mälu_regioon.sõeluma_täisarv(ADDRESS); }
    static int 짧은수(int ADDRESS) { return seade_VALUE.기억읽기(ADDRESS) | seade_VALUE.기억읽기(ADDRESS + 1) << 8; }
    static void kirjutamine_number(int ADDRESS, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) seade_VALUE.kirjutamine_Mälu(ADDRESS + INDEX, VALUE >>> (INDEX * 8));
    }

    static int Rühm_COUNT() {
        int ADDRESS = seade_VALUE.실행묶음();
        int Suurus = seade_VALUE.실행묶음크기();
        if (Suurus < 8 || number(ADDRESS) != 0x50414b4a) return 0;
        int kaup_COUNT = number(ADDRESS + 4);
        return kaup_COUNT >= 0 && kaup_COUNT <= 32 && kaup_COUNT <= (Suurus - 8) / 24 ? kaup_COUNT : 0;
    }

    static void kirje_Loend() {
        for (int INDEX = 0; INDEX < Rühm_COUNT(); INDEX++) {
            int kirje_VALUE = seade_VALUE.실행묶음() + 8 + INDEX * 24;
            for (int märk_VALUE = 0; märk_VALUE < 16 && seade_VALUE.기억읽기(kirje_VALUE + märk_VALUE) != 0; märk_VALUE++)
                SMS_terminal.문자(seade_VALUE.기억읽기(kirje_VALUE + märk_VALUE));
            SMS_terminal.Kirjutamine("\n");
        }
    }

    static int FIND_kirje(int[] 입력, int Käivita_2, int 길이) {
        if (길이 <= 0 || 길이 >= 16) return 0;
        for (int INDEX = 0; INDEX < Rühm_COUNT(); INDEX++) {
            int kirje_VALUE = seade_VALUE.실행묶음() + 8 + INDEX * 24;
            boolean 같음 = seade_VALUE.기억읽기(kirje_VALUE + 길이) == 0;
            for (int märk_VALUE = 0; märk_VALUE < 길이; märk_VALUE++)
                if (입력[Käivita_2 + märk_VALUE] != seade_VALUE.기억읽기(kirje_VALUE + märk_VALUE)) 같음 = false;
            if (같음) return kirje_VALUE;
        }
        return 0;
    }

    static int valideerima(int Fail, int 길이) {
        if (길이 < 52 || number(Fail) != 0x464c457f || seade_VALUE.기억읽기(Fail + 4) != 1
            || seade_VALUE.기억읽기(Fail + 5) != 1 || seade_VALUE.기억읽기(Fail + 6) != 1
            || 짧은수(Fail + 16) != 2 || 짧은수(Fail + 18) != 3 || number(Fail + 20) != 1
            || 짧은수(Fail + 40) != 52 || 짧은수(Fail + 42) != 32) return -8;
        int kirje_p_VALUE = number(Fail + 24);
        int tabel_ametikoht = number(Fail + 28);
        int kaup_COUNT = 짧은수(Fail + 44);
        if (kaup_COUNT == 0 || kaup_COUNT > 16 || tabel_ametikoht < 52 || tabel_ametikoht > 길이 - kaup_COUNT * 32) return -8;
        boolean 실행가능 = false;
        for (int INDEX = 0; INDEX < kaup_COUNT; INDEX++) {
            int LOOKUP_tabel = Fail + tabel_ametikoht + INDEX * 32;
            int 종류 = number(LOOKUP_tabel);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 Ühendu/parser_48ee4b1b 미지원
            if (종류 != 1) continue;
            int Asukoht = number(LOOKUP_tabel + 4), ADDRESS = number(LOOKUP_tabel + 8), faili_maht = number(LOOKUP_tabel + 16), Mälu_suurust_muutma = number(LOOKUP_tabel + 20);
            int joondama_VALUE = number(LOOKUP_tabel + 28);
            if (ADDRESS < START_kasutaja_programm || ADDRESS >= pilt_lõpeta_kõne_ADDRESS || Mälu_suurust_muutma < 0 || Mälu_suurust_muutma > pilt_lõpeta_kõne_ADDRESS - ADDRESS
                || faili_maht < 0 || faili_maht > Mälu_suurust_muutma || Asukoht < 0 || (faili_maht > 0 && Asukoht > 길이 - faili_maht)
                || (joondama_VALUE != 0 && (joondama_VALUE < 0 || (joondama_VALUE & (joondama_VALUE - 1)) != 0
                    || ((ADDRESS - Asukoht) & (joondama_VALUE - 1)) != 0))) return -8;
            for (int esikaamera_VALUE = 0; esikaamera_VALUE < INDEX; esikaamera_VALUE++) {
                int 이전 = Fail + tabel_ametikoht + esikaamera_VALUE * 32;
                if (number(이전) == 1 && Mälu_suurust_muutma > 0 && number(이전 + 20) > 0
                    && ADDRESS < number(이전 + 8) + number(이전 + 20) && number(이전 + 8) < ADDRESS + Mälu_suurust_muutma) return -8;
            }
            if ((number(LOOKUP_tabel + 24) & 1) != 0 && kirje_p_VALUE >= ADDRESS && kirje_p_VALUE - ADDRESS < faili_maht) 실행가능 = true;
        }
        return 실행가능 ? kirje_p_VALUE : -8;
    }

    static int Täida_käsk(int[] 입력, int Käivita_2, int 길이) {
        while (Käivita_2 < 길이 && 입력[Käivita_2] == ' ') Käivita_2++;
        int 끝 = Käivita_2;
        while (끝 < 길이 && 입력[끝] != ' ') 끝++;
        int kirje_VALUE = FIND_kirje(입력, Käivita_2, 끝 - Käivita_2);
        if (kirje_VALUE == 0) return -2;
        int Asukoht = number(kirje_VALUE + 16), Suurus = number(kirje_VALUE + 20);
        if (Asukoht < 8 + Rühm_COUNT() * 24 || Suurus < 52 || Asukoht > seade_VALUE.실행묶음크기() - Suurus) return -8;
        int Fail = seade_VALUE.실행묶음() + Asukoht;
        int kirje_p_VALUE = valideerima(Fail, Suurus);
        if (kirje_p_VALUE < 0) return kirje_p_VALUE;
        seade_VALUE.kasutaja_eemaldama_Sisu();
        int tabel_ametikoht = number(Fail + 28), kaup_COUNT = 짧은수(Fail + 44);
        for (int INDEX = 0; INDEX < kaup_COUNT; INDEX++) {
            int LOOKUP_tabel = Fail + tabel_ametikoht + INDEX * 32;
            if (number(LOOKUP_tabel) != 1) continue;
            int 원본 = Fail + number(LOOKUP_tabel + 4), sihtkoht_VALUE = number(LOOKUP_tabel + 8), faili_maht = number(LOOKUP_tabel + 16);
            for (int bait_VALUE = 0; bait_VALUE < faili_maht; bait_VALUE++) seade_VALUE.kirjutamine_Mälu(sihtkoht_VALUE + bait_VALUE, seade_VALUE.기억읽기(원본 + bait_VALUE));
        }
        argument_COUNT = 0;
        int salv_VALUE = argument_START;
        while (끝 < 길이) {
            while (끝 < 길이 && 입력[끝] == ' ') 끝++;
            if (끝 == 길이) break;
            if (argument_COUNT == argument_ADDRESS.length) return -22;
            Käivita_2 = 끝;
            while (끝 < 길이 && 입력[끝] != ' ') 끝++;
            argument_ADDRESS[argument_COUNT++] = salv_VALUE;
            kirjutamine_number(salv_VALUE, 끝 - Käivita_2);
            for (int märk_VALUE = Käivita_2; märk_VALUE < 끝; märk_VALUE++) kirjutamine_number(salv_VALUE + 4 + (märk_VALUE - Käivita_2) * 4, 입력[märk_VALUE]);
            salv_VALUE += 4 + (끝 - Käivita_2) * 4;
        }
        võrk_Virn.CLEAN_Joonis();
        파일서술자관리.START_Joonis();
        int TULEMUS = seade_VALUE.sari_kasutaja_programm(kirje_p_VALUE, kasutaja_lõpeta_kõne - 16);
        파일서술자관리.CLEAN_Joonis();
        võrk_Virn.CLEAN_Joonis();
        return TULEMUS;
    }
}
