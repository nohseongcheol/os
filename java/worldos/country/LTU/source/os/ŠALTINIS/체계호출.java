// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 naudotojas rodyklė/길이는 prieiga_įrašas 전에 검사한다. */
public final class 체계호출 {
    static int[] 임시자료 = new int[1024];

    static int 배열길이(int ADDRESS) {
        if (!실행관리.klipas(ADDRESS, 4)) return -14;
        int 길이 = 실행관리.numeris(ADDRESS);
        if (길이 < 0 || 길이 > (실행관리.naudotojas_baigti_pokalbį - ADDRESS - 4) / 4) return -14;
        return 길이;
    }

    public static int Procesas_VALUE_įrašas(int INDEX, int 가, int SECOND_operandas, int 다, int 라, int 마) {
        if (INDEX == 30) return 파일서술자관리.kurti_Failas(가, SECOND_operandas, 다);
        if (INDEX == 31) return 파일서술자관리.파일읽기(가, SECOND_operandas, 다);
        if (INDEX == 32) return 파일서술자관리.rašymas_Failas(가, SECOND_operandas, 다);
        if (INDEX == 33) return 파일서술자관리.Uždaryti_Failas(가);
        if (INDEX == 34) return 파일서술자관리.ieškoti_Failas(가, SECOND_operandas, 다);
        if (INDEX == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (INDEX == 36) return 파일서술자관리.서술자복제(가, SECOND_operandas, true, 0);
        if (INDEX == 37) return 파일서술자관리.파일상태읽기(가, SECOND_operandas);
        if (INDEX == 38) return 파일서술자관리.pašalinti_Failas_įrašas_pavadinimas(가);
        if (INDEX == 39) return 파일서술자관리.파일길이정하기(가, SECOND_operandas);
        if (INDEX == 40) return 파일서술자관리.서술자제어(가, SECOND_operandas, 다);
        if (INDEX == 41) return 파일서술자관리.kurti_dalyvis(가, SECOND_operandas, 다);
        if (INDEX == 42) return 파일서술자관리.BIND_ADDRESS(가, SECOND_operandas, 다);
        if (INDEX == 43) return 파일서술자관리.siųsti_paketų_kelio_schema_duomenys(가, SECOND_operandas, 다, 라, 마);
        if (INDEX == 44) return 파일서술자관리.gauti_paketų_kelio_schema_duomenys(가, SECOND_operandas, 다, 라, 마);
        if (INDEX == 45) return 파일서술자관리.통신주소읽기(가, SECOND_operandas, 다);
        if (INDEX == 46) return 파일서술자관리.rinkinys_gauti_SKIRTASIS_LAIKAS(가, SECOND_operandas);
        if (INDEX == 47) {
            int 기술 = 파일서술자관리.기술찾기(가);
            if (기술 < 0) return -9;
            if (파일서술자관리.종류[기술] != 2) return -22;
            return 파일보존.sinchronizuoti();
        }
        if (INDEX == 1) {
            int 길이 = 배열길이(가);
            if (길이 < 0) return 길이;
            if (길이 > 4096) return -90;
            for (int simbolis_VALUE_068c2631 = 0; simbolis_VALUE_068c2631 < 길이; simbolis_VALUE_068c2631++) SMS_Terminalas.문자(실행관리.numeris(가 + 4 + simbolis_VALUE_068c2631 * 4) & 65535);
            return 길이;
        }
        if (INDEX == 2) return 실행관리.argumentas_COUNT;
        if (INDEX == 3) return 가 >= 0 && 가 < 실행관리.argumentas_COUNT ? 실행관리.argumentas_ADDRESS[가] : 0;
        if (INDEX == 10) return tinklas_eilė.Atverti(가);
        if (INDEX == 11) {
            int 길이 = 배열길이(라);
            if (길이 < 0) return 길이;
            if (마 < 0 || 마 > 길이 || 마 > 1024) return -90;
            for (int Pozicija = 0; Pozicija < 마; Pozicija++) 임시자료[Pozicija] = 실행관리.numeris(라 + 4 + Pozicija * 4) & 255;
            return tinklas_eilė.siųsti(가, SECOND_operandas, 다, 임시자료, 마);
        }
        if (INDEX == 12) {
            int 길이 = 배열길이(SECOND_operandas);
            if (길이 < 0) return 길이;
            if (다 < 0 || 다 > 2000) return -22;
            int REZULTATAS = tinklas_eilė.gauti(가, 임시자료, 길이 < 1024 ? 길이 : 1024, 다);
            if (REZULTATAS >= 0) for (int Pozicija = 0; Pozicija < REZULTATAS; Pozicija++) 실행관리.rašymas_numeris(SECOND_operandas + 4 + Pozicija * 4, 임시자료[Pozicija]);
            return REZULTATAS;
        }
        if (INDEX == 13) return tinklas_eilė.Užverti(가);
        if (INDEX == 14) return tinklas_eilė.내주소;
        if (INDEX == 15) return tinklas_eilė.lygiavertis_mazgas_ADDRESS(가);
        if (INDEX == 16) return tinklas_eilė.lygiavertis_mazgas_prievado_numeris(가);
        if (INDEX == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            SMS_Terminalas.문자(가); return 1;
        }
        if (INDEX == 20 || INDEX == 21) {
            int pavadinimas_dydis = 배열길이(가), duomenys_dydis = 배열길이(SECOND_operandas);
            if (pavadinimas_dydis < 0 || duomenys_dydis < 0) return -14;
            if (pavadinimas_dydis < 1 || pavadinimas_dydis > 64) return -22;
            int 길이 = 0;
            while (길이 < pavadinimas_dydis && 실행관리.numeris(가 + 4 + 길이 * 4) != 0) {
                atmintis_failų_sistema.Pavadinimas_2[길이] = 실행관리.numeris(가 + 4 + 길이 * 4);
                길이++;
            }
            if (!atmintis_failų_sistema.čekis_pavadinimas(atmintis_failų_sistema.Pavadinimas_2, 길이)) return -22;
            if (INDEX == 20) {
                int Failas = atmintis_failų_sistema.FIND_įrašas(atmintis_failų_sistema.Pavadinimas_2, 길이);
                if (Failas < 0) return Failas;
                int Dydis = atmintis_failų_sistema.dydis_Sąrašas[Failas];
                if (Dydis > duomenys_dydis) return -90;
                int ADDRESS = įrenginys_VALUE.Failas_atmintis() + Failas * atmintis_failų_sistema.최대크기;
                for (int numeris = 0; numeris < Dydis; numeris++) 실행관리.rašymas_numeris(SECOND_operandas + 4 + numeris * 4, įrenginys_VALUE.기억읽기(ADDRESS + numeris));
                return Dydis;
            }
            if (다 < 0 || 다 > duomenys_dydis) return -22;
            if (다 > atmintis_failų_sistema.최대크기) return -90;
            for (int numeris = 0; numeris < 다; numeris++) atmintis_failų_sistema.redaguoti_VALUE[numeris] = 실행관리.numeris(SECOND_operandas + 4 + numeris * 4) & 255;
            return atmintis_failų_sistema.Store_VALUE(atmintis_failų_sistema.Pavadinimas_2, 길이, atmintis_failų_sistema.redaguoti_VALUE, 다);
        }
        return -38;
    }
}
