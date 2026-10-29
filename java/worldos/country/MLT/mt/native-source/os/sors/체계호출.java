// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 utent pointer/길이는 aċċess_entrata 전에 검사한다. */
public final class 체계호출 {
    static int[] 임시자료 = new int[1024];

    static int ARRAY_tul(int ADDRESS) {
        if (!실행관리.klipp(ADDRESS, 4)) return -14;
        int tul_VALUE = 실행관리.수(ADDRESS);
        if (tul_VALUE < 0 || tul_VALUE > (실행관리.utent_ttermina - ADDRESS - 4) / 4) return -14;
        return tul_VALUE;
    }

    public static int Proċess_VALUE_entrata(int INDEX, int 가, int 나, int 다, int 라, int 마) {
        if (INDEX == 30) return 파일서술자관리.fetaħ_fajl(가, 나, 다);
        if (INDEX == 31) return 파일서술자관리.파일읽기(가, 나, 다);
        if (INDEX == 32) return 파일서술자관리.kiteb_fajl(가, 나, 다);
        if (INDEX == 33) return 파일서술자관리.agħlaq_fajl(가);
        if (INDEX == 34) return 파일서술자관리.fittex_fajl(가, 나, 다);
        if (INDEX == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (INDEX == 36) return 파일서술자관리.서술자복제(가, 나, true, 0);
        if (INDEX == 37) return 파일서술자관리.파일상태읽기(가, 나);
        if (INDEX == 38) return 파일서술자관리.neħħa_fajl_entrata_isem(가);
        if (INDEX == 39) return 파일서술자관리.sett_fajl_tul(가, 나);
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
            return 파일보존.ssinkronizza();
        }
        if (INDEX == 1) {
            int tul_VALUE = ARRAY_tul(가);
            if (tul_VALUE < 0) return tul_VALUE;
            if (tul_VALUE > 4096) return -90;
            for (int karattru_VALUE = 0; karattru_VALUE < tul_VALUE; karattru_VALUE++) SMS_Terminal.문자(실행관리.수(가 + 4 + karattru_VALUE * 4) & 65535);
            return tul_VALUE;
        }
        if (INDEX == 2) return 실행관리.argument_COUNT;
        if (INDEX == 3) return 가 >= 0 && 가 < 실행관리.argument_COUNT ? 실행관리.argument_ADDRESS[가] : 0;
        if (INDEX == 10) return netwerk_Munzell.fetaħ(가);
        if (INDEX == 11) {
            int tul_VALUE = ARRAY_tul(라);
            if (tul_VALUE < 0) return tul_VALUE;
            if (마 < 0 || 마 > tul_VALUE || 마 > 1024) return -90;
            for (int pożizzjoni = 0; pożizzjoni < 마; pożizzjoni++) 임시자료[pożizzjoni] = 실행관리.수(라 + 4 + pożizzjoni * 4) & 255;
            return netwerk_Munzell.bagħat(가, 나, 다, 임시자료, 마);
        }
        if (INDEX == 12) {
            int tul_VALUE = ARRAY_tul(나);
            if (tul_VALUE < 0) return tul_VALUE;
            if (다 < 0 || 다 > 2000) return -22;
            int miżura = netwerk_Munzell.받기(가, 임시자료, tul_VALUE < 1024 ? tul_VALUE : 1024, 다);
            if (miżura >= 0) for (int pożizzjoni = 0; pożizzjoni < miżura; pożizzjoni++) 실행관리.수쓰기(나 + 4 + pożizzjoni * 4, 임시자료[pożizzjoni]);
            return miżura;
        }
        if (INDEX == 13) return netwerk_Munzell.agħlaq(가);
        if (INDEX == 14) return netwerk_Munzell.내주소;
        if (INDEX == 15) return netwerk_Munzell.peer_ADDRESS(가);
        if (INDEX == 16) return netwerk_Munzell.상대접속번호(가);
        if (INDEX == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            SMS_Terminal.문자(가); return 1;
        }
        if (INDEX == 20 || INDEX == 21) {
            int isem_daqqas = ARRAY_tul(가), data_daqqas = ARRAY_tul(나);
            if (isem_daqqas < 0 || data_daqqas < 0) return -14;
            if (isem_daqqas < 1 || isem_daqqas > 64) return -22;
            int tul_VALUE = 0;
            while (tul_VALUE < isem_daqqas && 실행관리.수(가 + 4 + tul_VALUE * 4) != 0) {
                Memorja_sistema_tal_fajls.isem[tul_VALUE] = 실행관리.수(가 + 4 + tul_VALUE * 4);
                tul_VALUE++;
            }
            if (!Memorja_sistema_tal_fajls.ċekk_isem(Memorja_sistema_tal_fajls.isem, tul_VALUE)) return -22;
            if (INDEX == 20) {
                int fajl = Memorja_sistema_tal_fajls.sab_entrata(Memorja_sistema_tal_fajls.isem, tul_VALUE);
                if (fajl < 0) return fajl;
                int daqqas = Memorja_sistema_tal_fajls.daqqas_Lista[fajl];
                if (daqqas > data_daqqas) return -90;
                int ADDRESS = mowbajl_VALUE.fajl_Memorja() + fajl * Memorja_sistema_tal_fajls.최대크기;
                for (int 수 = 0; 수 < daqqas; 수++) 실행관리.수쓰기(나 + 4 + 수 * 4, mowbajl_VALUE.기억읽기(ADDRESS + 수));
                return daqqas;
            }
            if (다 < 0 || 다 > data_daqqas) return -22;
            if (다 > Memorja_sistema_tal_fajls.최대크기) return -90;
            for (int 수 = 0; 수 < 다; 수++) Memorja_sistema_tal_fajls.editja_VALUE[수] = 실행관리.수(나 + 4 + 수 * 4) & 255;
            return Memorja_sistema_tal_fajls.Store_VALUE(Memorja_sistema_tal_fajls.isem, tul_VALUE, Memorja_sistema_tal_fajls.editja_VALUE, 다);
        }
        return -38;
    }
}
