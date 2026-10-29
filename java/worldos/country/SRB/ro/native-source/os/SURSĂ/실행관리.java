// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Citire 전용 executa_comandă 묶음의 ELF32 valida, Argumente Înainte_VALUE, 한 번에 한 utilizator Proces_VALUE executa_comandă. */
public final class 실행관리 {
    static final int buta_utilizator_program = 0x04000000;
    static final int utilizator_termina_un_apel = 0x04400000;
    static final int IMAGE_termina_un_apel_adresa = 0x04200000;
    static final int argument_buta = 0x04300000;
    static int argument_COUNT = 0;
    static int[] argument_adresa = new int[16];

    static boolean clip(int adresa, int lungime_VALUE) {
        return adresa >= buta_utilizator_program && adresa < utilizator_termina_un_apel && lungime_VALUE >= 0 && lungime_VALUE <= utilizator_termina_un_apel - adresa;
    }

    static int 수(int adresa) { return Memorie_regiune.analiza_întreg(adresa); }
    static int 짧은수(int adresa) { return mobil_VALUE.기억읽기(adresa) | mobil_VALUE.기억읽기(adresa + 1) << 8; }
    static void 수쓰기(int adresa, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) mobil_VALUE.scriere_Memorie(adresa + INDEX, VALUE >>> (INDEX * 8));
    }

    static int grup_COUNT() {
        int adresa = mobil_VALUE.실행묶음();
        int Mărime = mobil_VALUE.실행묶음크기();
        if (Mărime < 8 || 수(adresa) != 0x50414b4a) return 0;
        int element_COUNT = 수(adresa + 4);
        return element_COUNT >= 0 && element_COUNT <= 32 && element_COUNT <= (Mărime - 8) / 24 ? element_COUNT : 0;
    }

    static void intrare_Listă() {
        for (int INDEX = 0; INDEX < grup_COUNT(); INDEX++) {
            int intrare_VALUE = mobil_VALUE.실행묶음() + 8 + INDEX * 24;
            for (int caracter_VALUE = 0; caracter_VALUE < 16 && mobil_VALUE.기억읽기(intrare_VALUE + caracter_VALUE) != 0; caracter_VALUE++)
                SMS_Terminal.문자(mobil_VALUE.기억읽기(intrare_VALUE + caracter_VALUE));
            SMS_Terminal.Scriere("\n");
        }
    }

    static int FIND_intrare(int[] 입력, int Pornește, int lungime_VALUE) {
        if (lungime_VALUE <= 0 || lungime_VALUE >= 16) return 0;
        for (int INDEX = 0; INDEX < grup_COUNT(); INDEX++) {
            int intrare_VALUE = mobil_VALUE.실행묶음() + 8 + INDEX * 24;
            boolean 같음 = mobil_VALUE.기억읽기(intrare_VALUE + lungime_VALUE) == 0;
            for (int caracter_VALUE = 0; caracter_VALUE < lungime_VALUE; caracter_VALUE++)
                if (입력[Pornește + caracter_VALUE] != mobil_VALUE.기억읽기(intrare_VALUE + caracter_VALUE)) 같음 = false;
            if (같음) return intrare_VALUE;
        }
        return 0;
    }

    static int valida(int Fișier, int lungime_VALUE) {
        if (lungime_VALUE < 52 || 수(Fișier) != 0x464c457f || mobil_VALUE.기억읽기(Fișier + 4) != 1
            || mobil_VALUE.기억읽기(Fișier + 5) != 1 || mobil_VALUE.기억읽기(Fișier + 6) != 1
            || 짧은수(Fișier + 16) != 2 || 짧은수(Fișier + 18) != 3 || 수(Fișier + 20) != 1
            || 짧은수(Fișier + 40) != 52 || 짧은수(Fișier + 42) != 32) return -8;
        int intrare_p_VALUE = 수(Fișier + 24);
        int tabel_poziție = 수(Fișier + 28);
        int element_COUNT = 짧은수(Fișier + 44);
        if (element_COUNT == 0 || element_COUNT > 16 || tabel_poziție < 52 || tabel_poziție > lungime_VALUE - element_COUNT * 32) return -8;
        boolean 실행가능 = false;
        for (int INDEX = 0; INDEX < element_COUNT; INDEX++) {
            int tabel_de_căutare = Fișier + tabel_poziție + INDEX * 32;
            int 종류 = 수(tabel_de_căutare);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 Conectează/parser_48ee4b1b 미지원
            if (종류 != 1) continue;
            int Poziție = 수(tabel_de_căutare + 4), adresa = 수(tabel_de_căutare + 8), dimensiune_fișier = 수(tabel_de_căutare + 16), Memorie_dimensiona = 수(tabel_de_căutare + 20);
            int alinia_VALUE = 수(tabel_de_căutare + 28);
            if (adresa < buta_utilizator_program || adresa >= IMAGE_termina_un_apel_adresa || Memorie_dimensiona < 0 || Memorie_dimensiona > IMAGE_termina_un_apel_adresa - adresa
                || dimensiune_fișier < 0 || dimensiune_fișier > Memorie_dimensiona || Poziție < 0 || (dimensiune_fișier > 0 && Poziție > lungime_VALUE - dimensiune_fișier)
                || (alinia_VALUE != 0 && (alinia_VALUE < 0 || (alinia_VALUE & (alinia_VALUE - 1)) != 0
                    || ((adresa - Poziție) & (alinia_VALUE - 1)) != 0))) return -8;
            for (int frontală_VALUE = 0; frontală_VALUE < INDEX; frontală_VALUE++) {
                int Anteriorul_element = Fișier + tabel_poziție + frontală_VALUE * 32;
                if (수(Anteriorul_element) == 1 && Memorie_dimensiona > 0 && 수(Anteriorul_element + 20) > 0
                    && adresa < 수(Anteriorul_element + 8) + 수(Anteriorul_element + 20) && 수(Anteriorul_element + 8) < adresa + Memorie_dimensiona) return -8;
            }
            if ((수(tabel_de_căutare + 24) & 1) != 0 && intrare_p_VALUE >= adresa && intrare_p_VALUE - adresa < dimensiune_fișier) 실행가능 = true;
        }
        return 실행가능 ? intrare_p_VALUE : -8;
    }

    static int executa_comandă(int[] 입력, int Pornește, int lungime_VALUE) {
        while (Pornește < lungime_VALUE && 입력[Pornește] == ' ') Pornește++;
        int 끝 = Pornește;
        while (끝 < lungime_VALUE && 입력[끝] != ' ') 끝++;
        int intrare_VALUE = FIND_intrare(입력, Pornește, 끝 - Pornește);
        if (intrare_VALUE == 0) return -2;
        int Poziție = 수(intrare_VALUE + 16), Mărime = 수(intrare_VALUE + 20);
        if (Poziție < 8 + grup_COUNT() * 24 || Mărime < 52 || Poziție > mobil_VALUE.실행묶음크기() - Mărime) return -8;
        int Fișier = mobil_VALUE.실행묶음() + Poziție;
        int intrare_p_VALUE = valida(Fișier, Mărime);
        if (intrare_p_VALUE < 0) return intrare_p_VALUE;
        mobil_VALUE.utilizator_goli_TOC();
        int tabel_poziție = 수(Fișier + 28), element_COUNT = 짧은수(Fișier + 44);
        for (int INDEX = 0; INDEX < element_COUNT; INDEX++) {
            int tabel_de_căutare = Fișier + tabel_poziție + INDEX * 32;
            if (수(tabel_de_căutare) != 1) continue;
            int 원본 = Fișier + 수(tabel_de_căutare + 4), destinație_VALUE = 수(tabel_de_căutare + 8), dimensiune_fișier = 수(tabel_de_căutare + 16);
            for (int byte_VALUE = 0; byte_VALUE < dimensiune_fișier; byte_VALUE++) mobil_VALUE.scriere_Memorie(destinație_VALUE + byte_VALUE, mobil_VALUE.기억읽기(원본 + byte_VALUE));
        }
        argument_COUNT = 0;
        int Store_VALUE = argument_buta;
        while (끝 < lungime_VALUE) {
            while (끝 < lungime_VALUE && 입력[끝] == ' ') 끝++;
            if (끝 == lungime_VALUE) break;
            if (argument_COUNT == argument_adresa.length) return -22;
            Pornește = 끝;
            while (끝 < lungime_VALUE && 입력[끝] != ' ') 끝++;
            argument_adresa[argument_COUNT++] = Store_VALUE;
            수쓰기(Store_VALUE, 끝 - Pornește);
            for (int caracter_VALUE = Pornește; caracter_VALUE < 끝; caracter_VALUE++) 수쓰기(Store_VALUE + 4 + (caracter_VALUE - Pornește) * 4, 입력[caracter_VALUE]);
            Store_VALUE += 4 + (끝 - Pornește) * 4;
        }
        rețea_Teanc.CLEAN_Proces();
        파일서술자관리.buta_Proces();
        int KR = mobil_VALUE.rula_utilizator_program(intrare_p_VALUE, utilizator_termina_un_apel - 16);
        파일서술자관리.CLEAN_Proces();
        rețea_Teanc.CLEAN_Proces();
        return KR;
    }
}
