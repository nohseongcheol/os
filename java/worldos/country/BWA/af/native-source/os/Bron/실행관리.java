// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Lees 전용 uitvoer_bevel 묶음의 ELF32 valideer, 인수 aanstuur_VALUE_24592b8a, 한 번에 한 gebruiker Proses_VALUE uitvoer_bevel. */
public final class 실행관리 {
    static final int BEGIN_gebruiker_program = 0x04000000;
    static final int gebruiker_beëindig = 0x04400000;
    static final int foto_beëindig_adres = 0x04200000;
    static final int argument_BEGIN = 0x04300000;
    static int argument_COUNT = 0;
    static int[] argument_adres = new int[16];

    static boolean snit(int adres, int lengte_VALUE) {
        return adres >= BEGIN_gebruiker_program && adres < gebruiker_beëindig && lengte_VALUE >= 0 && lengte_VALUE <= gebruiker_beëindig - adres;
    }

    static int 수(int adres) { return 기억공간.ontleed_heelgetal(adres); }
    static int 짧은수(int adres) { return mobiel_VALUE.기억읽기(adres) | mobiel_VALUE.기억읽기(adres + 1) << 8; }
    static void 수쓰기(int adres, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) mobiel_VALUE.skryf_Geheue(adres + INDEX, VALUE >>> (INDEX * 8));
    }

    static int Groep_COUNT() {
        int adres = mobiel_VALUE.실행묶음();
        int Grootte = mobiel_VALUE.실행묶음크기();
        if (Grootte < 8 || 수(adres) != 0x50414b4a) return 0;
        int item_COUNT = 수(adres + 4);
        return item_COUNT >= 0 && item_COUNT <= 32 && item_COUNT <= (Grootte - 8) / 24 ? item_COUNT : 0;
    }

    static void inskrywing_Lys() {
        for (int INDEX = 0; INDEX < Groep_COUNT(); INDEX++) {
            int inskrywing_VALUE = mobiel_VALUE.실행묶음() + 8 + INDEX * 24;
            for (int karakter_VALUE = 0; karakter_VALUE < 16 && mobiel_VALUE.기억읽기(inskrywing_VALUE + karakter_VALUE) != 0; karakter_VALUE++)
                SMS_Terminaal.문자(mobiel_VALUE.기억읽기(inskrywing_VALUE + karakter_VALUE));
            SMS_Terminaal.Skryf("\n");
        }
    }

    static int FIND_inskrywing(int[] 입력, int Loop, int lengte_VALUE) {
        if (lengte_VALUE <= 0 || lengte_VALUE >= 16) return 0;
        for (int INDEX = 0; INDEX < Groep_COUNT(); INDEX++) {
            int inskrywing_VALUE = mobiel_VALUE.실행묶음() + 8 + INDEX * 24;
            boolean 같음 = mobiel_VALUE.기억읽기(inskrywing_VALUE + lengte_VALUE) == 0;
            for (int karakter_VALUE = 0; karakter_VALUE < lengte_VALUE; karakter_VALUE++)
                if (입력[Loop + karakter_VALUE] != mobiel_VALUE.기억읽기(inskrywing_VALUE + karakter_VALUE)) 같음 = false;
            if (같음) return inskrywing_VALUE;
        }
        return 0;
    }

    static int valideer(int Lêer, int lengte_VALUE) {
        if (lengte_VALUE < 52 || 수(Lêer) != 0x464c457f || mobiel_VALUE.기억읽기(Lêer + 4) != 1
            || mobiel_VALUE.기억읽기(Lêer + 5) != 1 || mobiel_VALUE.기억읽기(Lêer + 6) != 1
            || 짧은수(Lêer + 16) != 2 || 짧은수(Lêer + 18) != 3 || 수(Lêer + 20) != 1
            || 짧은수(Lêer + 40) != 52 || 짧은수(Lêer + 42) != 32) return -8;
        int inskrywing_p_VALUE = 수(Lêer + 24);
        int tabel_plaas = 수(Lêer + 28);
        int item_COUNT = 짧은수(Lêer + 44);
        if (item_COUNT == 0 || item_COUNT > 16 || tabel_plaas < 52 || tabel_plaas > lengte_VALUE - item_COUNT * 32) return -8;
        boolean 실행가능 = false;
        for (int INDEX = 0; INDEX < item_COUNT; INDEX++) {
            int LOOKUP_tabel = Lêer + tabel_plaas + INDEX * 32;
            int 종류 = 수(LOOKUP_tabel);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 Koppel/ontleder_48ee4b1b 미지원
            if (종류 != 1) continue;
            int Posisie = 수(LOOKUP_tabel + 4), adres = 수(LOOKUP_tabel + 8), lêer_verstel = 수(LOOKUP_tabel + 16), Geheue_verstel = 수(LOOKUP_tabel + 20);
            int belyn_VALUE = 수(LOOKUP_tabel + 28);
            if (adres < BEGIN_gebruiker_program || adres >= foto_beëindig_adres || Geheue_verstel < 0 || Geheue_verstel > foto_beëindig_adres - adres
                || lêer_verstel < 0 || lêer_verstel > Geheue_verstel || Posisie < 0 || (lêer_verstel > 0 && Posisie > lengte_VALUE - lêer_verstel)
                || (belyn_VALUE != 0 && (belyn_VALUE < 0 || (belyn_VALUE & (belyn_VALUE - 1)) != 0
                    || ((adres - Posisie) & (belyn_VALUE - 1)) != 0))) return -8;
            for (int voor_VALUE = 0; voor_VALUE < INDEX; voor_VALUE++) {
                int 이전 = Lêer + tabel_plaas + voor_VALUE * 32;
                if (수(이전) == 1 && Geheue_verstel > 0 && 수(이전 + 20) > 0
                    && adres < 수(이전 + 8) + 수(이전 + 20) && 수(이전 + 8) < adres + Geheue_verstel) return -8;
            }
            if ((수(LOOKUP_tabel + 24) & 1) != 0 && inskrywing_p_VALUE >= adres && inskrywing_p_VALUE - adres < lêer_verstel) 실행가능 = true;
        }
        return 실행가능 ? inskrywing_p_VALUE : -8;
    }

    static int uitvoer_bevel(int[] 입력, int Loop, int lengte_VALUE) {
        while (Loop < lengte_VALUE && 입력[Loop] == ' ') Loop++;
        int 끝 = Loop;
        while (끝 < lengte_VALUE && 입력[끝] != ' ') 끝++;
        int inskrywing_VALUE = FIND_inskrywing(입력, Loop, 끝 - Loop);
        if (inskrywing_VALUE == 0) return -2;
        int Posisie = 수(inskrywing_VALUE + 16), Grootte = 수(inskrywing_VALUE + 20);
        if (Posisie < 8 + Groep_COUNT() * 24 || Grootte < 52 || Posisie > mobiel_VALUE.실행묶음크기() - Grootte) return -8;
        int Lêer = mobiel_VALUE.실행묶음() + Posisie;
        int inskrywing_p_VALUE = valideer(Lêer, Grootte);
        if (inskrywing_p_VALUE < 0) return inskrywing_p_VALUE;
        mobiel_VALUE.gebruiker_vee_uit_inhoud();
        int tabel_plaas = 수(Lêer + 28), item_COUNT = 짧은수(Lêer + 44);
        for (int INDEX = 0; INDEX < item_COUNT; INDEX++) {
            int LOOKUP_tabel = Lêer + tabel_plaas + INDEX * 32;
            if (수(LOOKUP_tabel) != 1) continue;
            int 원본 = Lêer + 수(LOOKUP_tabel + 4), bestemming_VALUE = 수(LOOKUP_tabel + 8), lêer_verstel = 수(LOOKUP_tabel + 16);
            for (int greep_VALUE = 0; greep_VALUE < lêer_verstel; greep_VALUE++) mobiel_VALUE.skryf_Geheue(bestemming_VALUE + greep_VALUE, mobiel_VALUE.기억읽기(원본 + greep_VALUE));
        }
        argument_COUNT = 0;
        int bêre_VALUE = argument_BEGIN;
        while (끝 < lengte_VALUE) {
            while (끝 < lengte_VALUE && 입력[끝] == ' ') 끝++;
            if (끝 == lengte_VALUE) break;
            if (argument_COUNT == argument_adres.length) return -22;
            Loop = 끝;
            while (끝 < lengte_VALUE && 입력[끝] != ' ') 끝++;
            argument_adres[argument_COUNT++] = bêre_VALUE;
            수쓰기(bêre_VALUE, 끝 - Loop);
            for (int karakter_VALUE = Loop; karakter_VALUE < 끝; karakter_VALUE++) 수쓰기(bêre_VALUE + 4 + (karakter_VALUE - Loop) * 4, 입력[karakter_VALUE]);
            bêre_VALUE += 4 + (끝 - Loop) * 4;
        }
        Netwerk_Stapel.CLEAN_Proses();
        파일서술자관리.BEGIN_Proses();
        int maatreël = mobiel_VALUE.ry_gebruiker_program(inskrywing_p_VALUE, gebruiker_beëindig - 16);
        파일서술자관리.CLEAN_Proses();
        Netwerk_Stapel.CLEAN_Proses();
        return maatreël;
    }
}
