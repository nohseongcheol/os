// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 cleachdaiche tomhaire/길이는 inntrigeadh_cur_a_steach 전에 검사한다. */
public final class 체계호출 {
    static int[] 임시자료 = new int[1024];

    static int ARRAY_faid(int ADDRESS) {
        if (!실행관리.cliop(ADDRESS, 4)) return -14;
        int faid_VALUE = 실행관리.수(ADDRESS);
        if (faid_VALUE < 0 || faid_VALUE > (실행관리.cleachdaiche_crìochnaich - ADDRESS - 4) / 4) return -14;
        return faid_VALUE;
    }

    public static int Pròiseas_VALUE_cur_a_steach(int INDEX, int 가, int 나, int 다, int 라, int 마) {
        if (INDEX == 30) return 파일서술자관리.fosgail_faidhle(가, 나, 다);
        if (INDEX == 31) return 파일서술자관리.파일읽기(가, 나, 다);
        if (INDEX == 32) return 파일서술자관리.sgrìobh_faidhle(가, 나, 다);
        if (INDEX == 33) return 파일서술자관리.dùin_faidhle(가);
        if (INDEX == 34) return 파일서술자관리.sir_faidhle(가, 나, 다);
        if (INDEX == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (INDEX == 36) return 파일서술자관리.서술자복제(가, 나, true, 0);
        if (INDEX == 37) return 파일서술자관리.파일상태읽기(가, 나);
        if (INDEX == 38) return 파일서술자관리.thoir_air_falbh_faidhle_cur_a_steach_ainm(가);
        if (INDEX == 39) return 파일서술자관리.seata_faidhle_faid(가, 나);
        if (INDEX == 40) return 파일서술자관리.서술자제어(가, 나, 다);
        if (INDEX == 41) return 파일서술자관리.통신종단점만들기(가, 나, 다);
        if (INDEX == 42) return 파일서술자관리.BIND_ADDRESS(가, 나, 다);
        if (INDEX == 43) return 파일서술자관리.자료전문보내기(가, 나, 다, 라, 마);
        if (INDEX == 44) return 파일서술자관리.자료전문받기(가, 나, 다, 라, 마);
        if (INDEX == 45) return 파일서술자관리.통신주소읽기(가, 나, 다);
        if (INDEX == 46) return 파일서술자관리.수신대기정하기(가, 나);
        if (INDEX == 47) {
            int 기술 = 파일서술자관리.기술찾기(가);
            if (기술 < 0) return -9;
            if (파일서술자관리.종류[기술] != 2) return -22;
            return 파일보존.sioncronaich();
        }
        if (INDEX == 1) {
            int faid_VALUE = ARRAY_faid(가);
            if (faid_VALUE < 0) return faid_VALUE;
            if (faid_VALUE > 4096) return -90;
            for (int caractar_VALUE = 0; caractar_VALUE < faid_VALUE; caractar_VALUE++) SMS_tèirmineal.문자(실행관리.수(가 + 4 + caractar_VALUE * 4) & 65535);
            return faid_VALUE;
        }
        if (INDEX == 2) return 실행관리.argamaid_COUNT;
        if (INDEX == 3) return 가 >= 0 && 가 < 실행관리.argamaid_COUNT ? 실행관리.argamaid_ADDRESS[가] : 0;
        if (INDEX == 10) return lìonra_stac.fosgail(가);
        if (INDEX == 11) {
            int faid_VALUE = ARRAY_faid(라);
            if (faid_VALUE < 0) return faid_VALUE;
            if (마 < 0 || 마 > faid_VALUE || 마 > 1024) return -90;
            for (int suidhich = 0; suidhich < 마; suidhich++) 임시자료[suidhich] = 실행관리.수(라 + 4 + suidhich * 4) & 255;
            return lìonra_stac.cuir(가, 나, 다, 임시자료, 마);
        }
        if (INDEX == 12) {
            int faid_VALUE = ARRAY_faid(나);
            if (faid_VALUE < 0) return faid_VALUE;
            if (다 < 0 || 다 > 2000) return -22;
            int tomhas = lìonra_stac.받기(가, 임시자료, faid_VALUE < 1024 ? faid_VALUE : 1024, 다);
            if (tomhas >= 0) for (int suidhich = 0; suidhich < tomhas; suidhich++) 실행관리.수쓰기(나 + 4 + suidhich * 4, 임시자료[suidhich]);
            return tomhas;
        }
        if (INDEX == 13) return lìonra_stac.dùin(가);
        if (INDEX == 14) return lìonra_stac.내주소;
        if (INDEX == 15) return lìonra_stac.seise_ADDRESS(가);
        if (INDEX == 16) return lìonra_stac.상대접속번호(가);
        if (INDEX == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            SMS_tèirmineal.문자(가); return 1;
        }
        if (INDEX == 20 || INDEX == 21) {
            int ainm_atharraich_am_meud = ARRAY_faid(가), dàta_atharraich_am_meud = ARRAY_faid(나);
            if (ainm_atharraich_am_meud < 0 || dàta_atharraich_am_meud < 0) return -14;
            if (ainm_atharraich_am_meud < 1 || ainm_atharraich_am_meud > 64) return -22;
            int faid_VALUE = 0;
            while (faid_VALUE < ainm_atharraich_am_meud && 실행관리.수(가 + 4 + faid_VALUE * 4) != 0) {
                cuimhne_siostam_fhaidhlichean.Ainm[faid_VALUE] = 실행관리.수(가 + 4 + faid_VALUE * 4);
                faid_VALUE++;
            }
            if (!cuimhne_siostam_fhaidhlichean.seic_ainm(cuimhne_siostam_fhaidhlichean.Ainm, faid_VALUE)) return -22;
            if (INDEX == 20) {
                int faidhle = cuimhne_siostam_fhaidhlichean.FIND_cur_a_steach(cuimhne_siostam_fhaidhlichean.Ainm, faid_VALUE);
                if (faidhle < 0) return faidhle;
                int atharraich_am_meud = cuimhne_siostam_fhaidhlichean.atharraich_am_meud_Liosta[faidhle];
                if (atharraich_am_meud > dàta_atharraich_am_meud) return -90;
                int ADDRESS = uidheam_VALUE.faidhle_cuimhne() + faidhle * cuimhne_siostam_fhaidhlichean.최대크기;
                for (int 수 = 0; 수 < atharraich_am_meud; 수++) 실행관리.수쓰기(나 + 4 + 수 * 4, uidheam_VALUE.기억읽기(ADDRESS + 수));
                return atharraich_am_meud;
            }
            if (다 < 0 || 다 > dàta_atharraich_am_meud) return -22;
            if (다 > cuimhne_siostam_fhaidhlichean.최대크기) return -90;
            for (int 수 = 0; 수 < 다; 수++) cuimhne_siostam_fhaidhlichean.deasaich_VALUE[수] = 실행관리.수(나 + 4 + 수 * 4) & 255;
            return cuimhne_siostam_fhaidhlichean.Store_VALUE(cuimhne_siostam_fhaidhlichean.Ainm, faid_VALUE, cuimhne_siostam_fhaidhlichean.deasaich_VALUE, 다);
        }
        return -38;
    }
}
