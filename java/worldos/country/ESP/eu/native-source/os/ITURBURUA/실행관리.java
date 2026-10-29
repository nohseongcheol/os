// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Irakurri 전용 exekutatu_komando 묶음의 ELF32 baliozkotu, Argumentuak Aurrera_balio, 한 번에 한 erabiltzaile prozesu_balio exekutatu_komando. */
public final class 실행관리 {
    static final int HASI_erabiltzaile_aplik = 0x04000000;
    static final int erabiltzaile_amaitu = 0x04400000;
    static final int irudi_amaitu_helbide = 0x04200000;
    static final int arg_HASI = 0x04300000;
    static int arg_ZENBATU = 0;
    static int[] arg_helbide = new int[16];

    static boolean klip(int helbide, int luzera_balio) {
        return helbide >= HASI_erabiltzaile_aplik && helbide < erabiltzaile_amaitu && luzera_balio >= 0 && luzera_balio <= erabiltzaile_amaitu - helbide;
    }

    static int 수(int helbide) { return 기억공간.analizatu_osoko_zenbaki(helbide); }
    static int 짧은수(int helbide) { return gailu_balio.기억읽기(helbide) | gailu_balio.기억읽기(helbide + 1) << 8; }
    static void 수쓰기(int helbide, int balio) {
        for (int INDIZE = 0; INDIZE < 4; INDIZE++) gailu_balio.idatzi_Memoria(helbide + INDIZE, balio >>> (INDIZE * 8));
    }

    static int talde_ZENBATU() {
        int helbide = gailu_balio.실행묶음();
        int Tamaina = gailu_balio.실행묶음크기();
        if (Tamaina < 8 || 수(helbide) != 0x50414b4a) return 0;
        int elementu_ZENBATU = 수(helbide + 4);
        return elementu_ZENBATU >= 0 && elementu_ZENBATU <= 32 && elementu_ZENBATU <= (Tamaina - 8) / 24 ? elementu_ZENBATU : 0;
    }

    static void sarrera_Zerrenda() {
        for (int INDIZE = 0; INDIZE < talde_ZENBATU(); INDIZE++) {
            int sarrera_balio = gailu_balio.실행묶음() + 8 + INDIZE * 24;
            for (int karaktere_balio = 0; karaktere_balio < 16 && gailu_balio.기억읽기(sarrera_balio + karaktere_balio) != 0; karaktere_balio++)
                SMS_Terminal.문자(gailu_balio.기억읽기(sarrera_balio + karaktere_balio));
            SMS_Terminal.Idatzi("\n");
        }
    }

    static int Bilatu_sarrera(int[] 입력, int Exekutatu_2, int luzera_balio) {
        if (luzera_balio <= 0 || luzera_balio >= 16) return 0;
        for (int INDIZE = 0; INDIZE < talde_ZENBATU(); INDIZE++) {
            int sarrera_balio = gailu_balio.실행묶음() + 8 + INDIZE * 24;
            boolean 같음 = gailu_balio.기억읽기(sarrera_balio + luzera_balio) == 0;
            for (int karaktere_balio = 0; karaktere_balio < luzera_balio; karaktere_balio++)
                if (입력[Exekutatu_2 + karaktere_balio] != gailu_balio.기억읽기(sarrera_balio + karaktere_balio)) 같음 = false;
            if (같음) return sarrera_balio;
        }
        return 0;
    }

    static int baliozkotu(int Fitxategia, int luzera_balio) {
        if (luzera_balio < 52 || 수(Fitxategia) != 0x464c457f || gailu_balio.기억읽기(Fitxategia + 4) != 1
            || gailu_balio.기억읽기(Fitxategia + 5) != 1 || gailu_balio.기억읽기(Fitxategia + 6) != 1
            || 짧은수(Fitxategia + 16) != 2 || 짧은수(Fitxategia + 18) != 3 || 수(Fitxategia + 20) != 1
            || 짧은수(Fitxategia + 40) != 52 || 짧은수(Fitxategia + 42) != 32) return -8;
        int sarrera_p_balio = 수(Fitxategia + 24);
        int taula_kargu = 수(Fitxategia + 28);
        int elementu_ZENBATU = 짧은수(Fitxategia + 44);
        if (elementu_ZENBATU == 0 || elementu_ZENBATU > 16 || taula_kargu < 52 || taula_kargu > luzera_balio - elementu_ZENBATU * 32) return -8;
        boolean 실행가능 = false;
        for (int INDIZE = 0; INDIZE < elementu_ZENBATU; INDIZE++) {
            int BEGIRATU_taula = Fitxategia + taula_kargu + INDIZE * 32;
            int 종류 = 수(BEGIRATU_taula);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 Konektatu/analizatzaile_48ee4b1b 미지원
            if (종류 != 1) continue;
            int Posizioa = 수(BEGIRATU_taula + 4), helbide = 수(BEGIRATU_taula + 8), 파일크기 = 수(BEGIRATU_taula + 16), 기억크기 = 수(BEGIRATU_taula + 20);
            int lerrokatu_balio = 수(BEGIRATU_taula + 28);
            if (helbide < HASI_erabiltzaile_aplik || helbide >= irudi_amaitu_helbide || 기억크기 < 0 || 기억크기 > irudi_amaitu_helbide - helbide
                || 파일크기 < 0 || 파일크기 > 기억크기 || Posizioa < 0 || (파일크기 > 0 && Posizioa > luzera_balio - 파일크기)
                || (lerrokatu_balio != 0 && (lerrokatu_balio < 0 || (lerrokatu_balio & (lerrokatu_balio - 1)) != 0
                    || ((helbide - Posizioa) & (lerrokatu_balio - 1)) != 0))) return -8;
            for (int aurrekoa_balio = 0; aurrekoa_balio < INDIZE; aurrekoa_balio++) {
                int 이전 = Fitxategia + taula_kargu + aurrekoa_balio * 32;
                if (수(이전) == 1 && 기억크기 > 0 && 수(이전 + 20) > 0
                    && helbide < 수(이전 + 8) + 수(이전 + 20) && 수(이전 + 8) < helbide + 기억크기) return -8;
            }
            if ((수(BEGIRATU_taula + 24) & 1) != 0 && sarrera_p_balio >= helbide && sarrera_p_balio - helbide < 파일크기) 실행가능 = true;
        }
        return 실행가능 ? sarrera_p_balio : -8;
    }

    static int exekutatu_komando(int[] 입력, int Exekutatu_2, int luzera_balio) {
        while (Exekutatu_2 < luzera_balio && 입력[Exekutatu_2] == ' ') Exekutatu_2++;
        int 끝 = Exekutatu_2;
        while (끝 < luzera_balio && 입력[끝] != ' ') 끝++;
        int sarrera_balio = Bilatu_sarrera(입력, Exekutatu_2, 끝 - Exekutatu_2);
        if (sarrera_balio == 0) return -2;
        int Posizioa = 수(sarrera_balio + 16), Tamaina = 수(sarrera_balio + 20);
        if (Posizioa < 8 + talde_ZENBATU() * 24 || Tamaina < 52 || Posizioa > gailu_balio.실행묶음크기() - Tamaina) return -8;
        int Fitxategia = gailu_balio.실행묶음() + Posizioa;
        int sarrera_p_balio = baliozkotu(Fitxategia, Tamaina);
        if (sarrera_p_balio < 0) return sarrera_p_balio;
        gailu_balio.erabiltzaile_garbitu_Edukia();
        int taula_kargu = 수(Fitxategia + 28), elementu_ZENBATU = 짧은수(Fitxategia + 44);
        for (int INDIZE = 0; INDIZE < elementu_ZENBATU; INDIZE++) {
            int BEGIRATU_taula = Fitxategia + taula_kargu + INDIZE * 32;
            if (수(BEGIRATU_taula) != 1) continue;
            int 원본 = Fitxategia + 수(BEGIRATU_taula + 4), helburu_balio_a0fbc067 = 수(BEGIRATU_taula + 8), 파일크기 = 수(BEGIRATU_taula + 16);
            for (int byte_balio = 0; byte_balio < 파일크기; byte_balio++) gailu_balio.idatzi_Memoria(helburu_balio_a0fbc067 + byte_balio, gailu_balio.기억읽기(원본 + byte_balio));
        }
        arg_ZENBATU = 0;
        int Store_balio = arg_HASI;
        while (끝 < luzera_balio) {
            while (끝 < luzera_balio && 입력[끝] == ' ') 끝++;
            if (끝 == luzera_balio) break;
            if (arg_ZENBATU == arg_helbide.length) return -22;
            Exekutatu_2 = 끝;
            while (끝 < luzera_balio && 입력[끝] != ' ') 끝++;
            arg_helbide[arg_ZENBATU++] = Store_balio;
            수쓰기(Store_balio, 끝 - Exekutatu_2);
            for (int karaktere_balio = Exekutatu_2; karaktere_balio < 끝; karaktere_balio++) 수쓰기(Store_balio + 4 + (karaktere_balio - Exekutatu_2) * 4, 입력[karaktere_balio]);
            Store_balio += 4 + (끝 - Exekutatu_2) * 4;
        }
        sare_pila.GARBITU_prozesu();
        파일서술자관리.HASI_prozesu();
        int EMAITZA = gailu_balio.exekutatu_erabiltzaile_aplik(sarrera_p_balio, erabiltzaile_amaitu - 16);
        파일서술자관리.GARBITU_prozesu();
        sare_pila.GARBITU_prozesu();
        return EMAITZA;
    }
}
