// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 kasutaja kursor/길이는 pöördus_kirje 전에 검사한다. */
public final class 체계호출 {
    static int[] 임시자료 = new int[1024];

    static int 배열길이(int ADDRESS) {
        if (!실행관리.klipp(ADDRESS, 4)) return -14;
        int 길이 = 실행관리.number(ADDRESS);
        if (길이 < 0 || 길이 > (실행관리.kasutaja_lõpeta_kõne - ADDRESS - 4) / 4) return -14;
        return 길이;
    }

    public static int Joonis_VALUE_kirje(int INDEX, int 가, int SECOND_operand, int 다, int 라, int 마) {
        if (INDEX == 30) return 파일서술자관리.avama_Fail(가, SECOND_operand, 다);
        if (INDEX == 31) return 파일서술자관리.파일읽기(가, SECOND_operand, 다);
        if (INDEX == 32) return 파일서술자관리.kirjutamine_Fail(가, SECOND_operand, 다);
        if (INDEX == 33) return 파일서술자관리.Sule_Fail(가);
        if (INDEX == 34) return 파일서술자관리.otsima_Fail(가, SECOND_operand, 다);
        if (INDEX == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (INDEX == 36) return 파일서술자관리.서술자복제(가, SECOND_operand, true, 0);
        if (INDEX == 37) return 파일서술자관리.파일상태읽기(가, SECOND_operand);
        if (INDEX == 38) return 파일서술자관리.eemaldama_Fail_kirje_nimetus(가);
        if (INDEX == 39) return 파일서술자관리.파일길이정하기(가, SECOND_operand);
        if (INDEX == 40) return 파일서술자관리.서술자제어(가, SECOND_operand, 다);
        if (INDEX == 41) return 파일서술자관리.avama_osaleja(가, SECOND_operand, 다);
        if (INDEX == 42) return 파일서술자관리.BIND_ADDRESS(가, SECOND_operand, 다);
        if (INDEX == 43) return 파일서술자관리.saatma_datagramm_andmed(가, SECOND_operand, 다, 라, 마);
        if (INDEX == 44) return 파일서술자관리.saama_datagramm_andmed(가, SECOND_operand, 다, 라, 마);
        if (INDEX == 45) return 파일서술자관리.통신주소읽기(가, SECOND_operand, 다);
        if (INDEX == 46) return 파일서술자관리.hulk_saama_TIMEOUT(가, SECOND_operand);
        if (INDEX == 47) {
            int 기술 = 파일서술자관리.기술찾기(가);
            if (기술 < 0) return -9;
            if (파일서술자관리.종류[기술] != 2) return -22;
            return 파일보존.sünkroonima();
        }
        if (INDEX == 1) {
            int 길이 = 배열길이(가);
            if (길이 < 0) return 길이;
            if (길이 > 4096) return -90;
            for (int märk_VALUE = 0; märk_VALUE < 길이; märk_VALUE++) SMS_terminal.문자(실행관리.number(가 + 4 + märk_VALUE * 4) & 65535);
            return 길이;
        }
        if (INDEX == 2) return 실행관리.argument_COUNT;
        if (INDEX == 3) return 가 >= 0 && 가 < 실행관리.argument_COUNT ? 실행관리.argument_ADDRESS[가] : 0;
        if (INDEX == 10) return võrk_Virn.Ava(가);
        if (INDEX == 11) {
            int 길이 = 배열길이(라);
            if (길이 < 0) return 길이;
            if (마 < 0 || 마 > 길이 || 마 > 1024) return -90;
            for (int Asukoht = 0; Asukoht < 마; Asukoht++) 임시자료[Asukoht] = 실행관리.number(라 + 4 + Asukoht * 4) & 255;
            return võrk_Virn.saatma(가, SECOND_operand, 다, 임시자료, 마);
        }
        if (INDEX == 12) {
            int 길이 = 배열길이(SECOND_operand);
            if (길이 < 0) return 길이;
            if (다 < 0 || 다 > 2000) return -22;
            int TULEMUS = võrk_Virn.saama(가, 임시자료, 길이 < 1024 ? 길이 : 1024, 다);
            if (TULEMUS >= 0) for (int Asukoht = 0; Asukoht < TULEMUS; Asukoht++) 실행관리.kirjutamine_number(SECOND_operand + 4 + Asukoht * 4, 임시자료[Asukoht]);
            return TULEMUS;
        }
        if (INDEX == 13) return võrk_Virn.Suletud(가);
        if (INDEX == 14) return võrk_Virn.내주소;
        if (INDEX == 15) return võrk_Virn.partner_ADDRESS(가);
        if (INDEX == 16) return võrk_Virn.partner_pordinumber(가);
        if (INDEX == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            SMS_terminal.문자(가); return 1;
        }
        if (INDEX == 20 || INDEX == 21) {
            int nimetus_suurust_muutma = 배열길이(가), andmed_suurust_muutma = 배열길이(SECOND_operand);
            if (nimetus_suurust_muutma < 0 || andmed_suurust_muutma < 0) return -14;
            if (nimetus_suurust_muutma < 1 || nimetus_suurust_muutma > 64) return -22;
            int 길이 = 0;
            while (길이 < nimetus_suurust_muutma && 실행관리.number(가 + 4 + 길이 * 4) != 0) {
                Mälu_failisüsteem.Nimi_2[길이] = 실행관리.number(가 + 4 + 길이 * 4);
                길이++;
            }
            if (!Mälu_failisüsteem.tšekk_nimetus(Mälu_failisüsteem.Nimi_2, 길이)) return -22;
            if (INDEX == 20) {
                int Fail = Mälu_failisüsteem.FIND_kirje(Mälu_failisüsteem.Nimi_2, 길이);
                if (Fail < 0) return Fail;
                int Suurus = Mälu_failisüsteem.suurust_muutma_Loend[Fail];
                if (Suurus > andmed_suurust_muutma) return -90;
                int ADDRESS = seade_VALUE.Fail_Mälu() + Fail * Mälu_failisüsteem.최대크기;
                for (int number = 0; number < Suurus; number++) 실행관리.kirjutamine_number(SECOND_operand + 4 + number * 4, seade_VALUE.기억읽기(ADDRESS + number));
                return Suurus;
            }
            if (다 < 0 || 다 > andmed_suurust_muutma) return -22;
            if (다 > Mälu_failisüsteem.최대크기) return -90;
            for (int number = 0; number < 다; number++) Mälu_failisüsteem.muudatus_VALUE[number] = 실행관리.number(SECOND_operand + 4 + number * 4) & 255;
            return Mälu_failisüsteem.salv_VALUE(Mälu_failisüsteem.Nimi_2, 길이, Mälu_failisüsteem.muudatus_VALUE, 다);
        }
        return -38;
    }
}
