// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 atuqtuq 포인터/길이는 pili_Iliniku 전에 검사한다. */
public final class 체계호출 {
    static int[] 임시자료 = new int[1024];

    static int array_takininga(int turaarut) {
        if (!실행관리.Nakatigat(turaarut, 4)) return -14;
        int takininga_atuutilik = 실행관리.수(turaarut);
        if (takininga_atuutilik < 0 || takininga_atuutilik > (실행관리.atuqtuq_isulittuq - turaarut - 4) / 4) return -14;
        return takininga_atuutilik;
    }

    public static int Pivallianiq_atuutilik_Iliniku(int nalunaiqsimavik, int 가, int 나, int 다, int 라, int 마) {
        if (nalunaiqsimavik == 30) return 파일서술자관리.matuirli_ini(가, 나, 다);
        if (nalunaiqsimavik == 31) return 파일서술자관리.파일읽기(가, 나, 다);
        if (nalunaiqsimavik == 32) return 파일서술자관리.titiraq_ini(가, 나, 다);
        if (nalunaiqsimavik == 33) return 파일서술자관리.matuli_ini(가);
        if (nalunaiqsimavik == 34) return 파일서술자관리.qinirli_ini(가, 나, 다);
        if (nalunaiqsimavik == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (nalunaiqsimavik == 36) return 파일서술자관리.서술자복제(가, 나, true, 0);
        if (nalunaiqsimavik == 37) return 파일서술자관리.파일상태읽기(가, 나);
        if (nalunaiqsimavik == 38) return 파일서술자관리.sanirvalli_ini_Iliniku_atiq(가);
        if (nalunaiqsimavik == 39) return 파일서술자관리.attiqsimaniit_ini_takininga(가, 나);
        if (nalunaiqsimavik == 40) return 파일서술자관리.서술자제어(가, 나, 다);
        if (nalunaiqsimavik == 41) return 파일서술자관리.통신종단점만들기(가, 나, 다);
        if (nalunaiqsimavik == 42) return 파일서술자관리.unittilli_turaarut(가, 나, 다);
        if (nalunaiqsimavik == 43) return 파일서술자관리.자료전문보내기(가, 나, 다, 라, 마);
        if (nalunaiqsimavik == 44) return 파일서술자관리.자료전문받기(가, 나, 다, 라, 마);
        if (nalunaiqsimavik == 45) return 파일서술자관리.통신주소읽기(가, 나, 다);
        if (nalunaiqsimavik == 46) return 파일서술자관리.수신대기정하기(가, 나);
        if (nalunaiqsimavik == 47) {
            int 기술 = 파일서술자관리.기술찾기(가);
            if (기술 < 0) return -9;
            if (파일서술자관리.종류[기술] != 2) return -22;
            return 파일보존.asiqqunniqannginniq();
        }
        if (nalunaiqsimavik == 1) {
            int takininga_atuutilik = array_takininga(가);
            if (takininga_atuutilik < 0) return takininga_atuutilik;
            if (takininga_atuutilik > 4096) return -90;
            for (int immikkuuqtuq_atuutilik = 0; immikkuuqtuq_atuutilik < takininga_atuutilik; immikkuuqtuq_atuutilik++) 문자단말.문자(실행관리.수(가 + 4 + immikkuuqtuq_atuutilik * 4) & 65535);
            return takininga_atuutilik;
        }
        if (nalunaiqsimavik == 2) return 실행관리.인수수;
        if (nalunaiqsimavik == 3) return 가 >= 0 && 가 < 실행관리.인수수 ? 실행관리.aturniqarnirainiq_turaarut[가] : 0;
        if (nalunaiqsimavik == 10) return 통신망.matuirli(가);
        if (nalunaiqsimavik == 11) {
            int takininga_atuutilik = array_takininga(라);
            if (takininga_atuutilik < 0) return takininga_atuutilik;
            if (마 < 0 || 마 > takininga_atuutilik || 마 > 1024) return -90;
            for (int 위치 = 0; 위치 < 마; 위치++) 임시자료[위치] = 실행관리.수(라 + 4 + 위치 * 4) & 255;
            return 통신망.nassiutili(가, 나, 다, 임시자료, 마);
        }
        if (nalunaiqsimavik == 12) {
            int takininga_atuutilik = array_takininga(나);
            if (takininga_atuutilik < 0) return takininga_atuutilik;
            if (다 < 0 || 다 > 2000) return -22;
            int 결과 = 통신망.받기(가, 임시자료, takininga_atuutilik < 1024 ? takininga_atuutilik : 1024, 다);
            if (결과 >= 0) for (int 위치 = 0; 위치 < 결과; 위치++) 실행관리.수쓰기(나 + 4 + 위치 * 4, 임시자료[위치]);
            return 결과;
        }
        if (nalunaiqsimavik == 13) return 통신망.matuli(가);
        if (nalunaiqsimavik == 14) return 통신망.내주소;
        if (nalunaiqsimavik == 15) return 통신망.ilagijaujuq_turaarut(가);
        if (nalunaiqsimavik == 16) return 통신망.상대접속번호(가);
        if (nalunaiqsimavik == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            문자단말.문자(가); return 1;
        }
        if (nalunaiqsimavik == 20 || nalunaiqsimavik == 21) {
            int atiq_anininga = array_takininga(가), titiqqat_anininga = array_takininga(나);
            if (atiq_anininga < 0 || titiqqat_anininga < 0) return -14;
            if (atiq_anininga < 1 || atiq_anininga > 64) return -22;
            int takininga_atuutilik = 0;
            while (takininga_atuutilik < atiq_anininga && 실행관리.수(가 + 4 + takininga_atuutilik * 4) != 0) {
                puigujjaikkut_inikkuvik.atiq[takininga_atuutilik] = 실행관리.수(가 + 4 + takininga_atuutilik * 4);
                takininga_atuutilik++;
            }
            if (!puigujjaikkut_inikkuvik.qaujigiarli_atiq(puigujjaikkut_inikkuvik.atiq, takininga_atuutilik)) return -22;
            if (nalunaiqsimavik == 20) {
                int ini = puigujjaikkut_inikkuvik.nanili_Iliniku(puigujjaikkut_inikkuvik.atiq, takininga_atuutilik);
                if (ini < 0) return ini;
                int anininga = puigujjaikkut_inikkuvik.anininga_Titiqpalliagaq[ini];
                if (anininga > titiqqat_anininga) return -90;
                int turaarut = sunakkutaaq_atuutilik.ini_puigujjaikkut() + ini * puigujjaikkut_inikkuvik.최대크기;
                for (int 수 = 0; 수 < anininga; 수++) 실행관리.수쓰기(나 + 4 + 수 * 4, sunakkutaaq_atuutilik.기억읽기(turaarut + 수));
                return anininga;
            }
            if (다 < 0 || 다 > titiqqat_anininga) return -22;
            if (다 > puigujjaikkut_inikkuvik.최대크기) return -90;
            for (int 수 = 0; 수 < 다; 수++) puigujjaikkut_inikkuvik.aaqqigiarli_atuutilik[수] = 실행관리.수(나 + 4 + 수 * 4) & 255;
            return puigujjaikkut_inikkuvik.tuqqurli_atuutilik(puigujjaikkut_inikkuvik.atiq, takininga_atuutilik, puigujjaikkut_inikkuvik.aaqqigiarli_atuutilik, 다);
        }
        return -38;
    }
}
