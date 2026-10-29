// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 erabiltzaile erakusle/길이는 atzitu_sarrera 전에 검사한다. */
public final class 체계호출 {
    static int[] 임시자료 = new int[1024];

    static int matrize_luzera(int helbide) {
        if (!실행관리.klip(helbide, 4)) return -14;
        int luzera_balio = 실행관리.수(helbide);
        if (luzera_balio < 0 || luzera_balio > (실행관리.erabiltzaile_amaitu - helbide - 4) / 4) return -14;
        return luzera_balio;
    }

    public static int prozesu_balio_sarrera(int INDIZE, int 가, int 나, int 다, int 라, int 마) {
        if (INDIZE == 30) return 파일서술자관리.ireki_fitxategi(가, 나, 다);
        if (INDIZE == 31) return 파일서술자관리.파일읽기(가, 나, 다);
        if (INDIZE == 32) return 파일서술자관리.idatzi_fitxategi(가, 나, 다);
        if (INDIZE == 33) return 파일서술자관리.itxi_fitxategi(가);
        if (INDIZE == 34) return 파일서술자관리.bilatu_fitxategi(가, 나, 다);
        if (INDIZE == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (INDIZE == 36) return 파일서술자관리.서술자복제(가, 나, true, 0);
        if (INDIZE == 37) return 파일서술자관리.파일상태읽기(가, 나);
        if (INDIZE == 38) return 파일서술자관리.kendu_fitxategi_sarrera_izen(가);
        if (INDIZE == 39) return 파일서술자관리.sorta_fitxategi_luzera(가, 나);
        if (INDIZE == 40) return 파일서술자관리.서술자제어(가, 나, 다);
        if (INDIZE == 41) return 파일서술자관리.sortu_amaiera_puntu(가, 나, 다);
        if (INDIZE == 42) return 파일서술자관리.lotu_helbide(가, 나, 다);
        if (INDIZE == 43) return 파일서술자관리.자료전문보내기(가, 나, 다, 라, 마);
        if (INDIZE == 44) return 파일서술자관리.자료전문받기(가, 나, 다, 라, 마);
        if (INDIZE == 45) return 파일서술자관리.통신주소읽기(가, 나, 다);
        if (INDIZE == 46) return 파일서술자관리.수신대기정하기(가, 나);
        if (INDIZE == 47) {
            int 기술 = 파일서술자관리.기술찾기(가);
            if (기술 < 0) return -9;
            if (파일서술자관리.종류[기술] != 2) return -22;
            return 파일보존.sinkronizatu();
        }
        if (INDIZE == 1) {
            int luzera_balio = matrize_luzera(가);
            if (luzera_balio < 0) return luzera_balio;
            if (luzera_balio > 4096) return -90;
            for (int karaktere_balio = 0; karaktere_balio < luzera_balio; karaktere_balio++) SMS_Terminal.문자(실행관리.수(가 + 4 + karaktere_balio * 4) & 65535);
            return luzera_balio;
        }
        if (INDIZE == 2) return 실행관리.arg_ZENBATU;
        if (INDIZE == 3) return 가 >= 0 && 가 < 실행관리.arg_ZENBATU ? 실행관리.arg_helbide[가] : 0;
        if (INDIZE == 10) return sare_pila.Ireki(가);
        if (INDIZE == 11) {
            int luzera_balio = matrize_luzera(라);
            if (luzera_balio < 0) return luzera_balio;
            if (마 < 0 || 마 > luzera_balio || 마 > 1024) return -90;
            for (int Posizioa = 0; Posizioa < 마; Posizioa++) 임시자료[Posizioa] = 실행관리.수(라 + 4 + Posizioa * 4) & 255;
            return sare_pila.bidali(가, 나, 다, 임시자료, 마);
        }
        if (INDIZE == 12) {
            int luzera_balio = matrize_luzera(나);
            if (luzera_balio < 0) return luzera_balio;
            if (다 < 0 || 다 > 2000) return -22;
            int EMAITZA = sare_pila.받기(가, 임시자료, luzera_balio < 1024 ? luzera_balio : 1024, 다);
            if (EMAITZA >= 0) for (int Posizioa = 0; Posizioa < EMAITZA; Posizioa++) 실행관리.수쓰기(나 + 4 + Posizioa * 4, 임시자료[Posizioa]);
            return EMAITZA;
        }
        if (INDIZE == 13) return sare_pila.Itxi(가);
        if (INDIZE == 14) return sare_pila.내주소;
        if (INDIZE == 15) return sare_pila.pareko_helbide(가);
        if (INDIZE == 16) return sare_pila.pareko_ataka_zenbaki(가);
        if (INDIZE == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            SMS_Terminal.문자(가); return 1;
        }
        if (INDIZE == 20 || INDIZE == 21) {
            int 이름크기 = matrize_luzera(가), 자료크기 = matrize_luzera(나);
            if (이름크기 < 0 || 자료크기 < 0) return -14;
            if (이름크기 < 1 || 이름크기 > 64) return -22;
            int luzera_balio = 0;
            while (luzera_balio < 이름크기 && 실행관리.수(가 + 4 + luzera_balio * 4) != 0) {
                Memoria_fitxategi_sistema.Izena[luzera_balio] = 실행관리.수(가 + 4 + luzera_balio * 4);
                luzera_balio++;
            }
            if (!Memoria_fitxategi_sistema.txeke_izen(Memoria_fitxategi_sistema.Izena, luzera_balio)) return -22;
            if (INDIZE == 20) {
                int Fitxategia = Memoria_fitxategi_sistema.Bilatu_sarrera(Memoria_fitxategi_sistema.Izena, luzera_balio);
                if (Fitxategia < 0) return Fitxategia;
                int Tamaina = Memoria_fitxategi_sistema.크기들[Fitxategia];
                if (Tamaina > 자료크기) return -90;
                int helbide = gailu_balio.fitxategi_Memoria() + Fitxategia * Memoria_fitxategi_sistema.최대크기;
                for (int 수 = 0; 수 < Tamaina; 수++) 실행관리.수쓰기(나 + 4 + 수 * 4, gailu_balio.기억읽기(helbide + 수));
                return Tamaina;
            }
            if (다 < 0 || 다 > 자료크기) return -22;
            if (다 > Memoria_fitxategi_sistema.최대크기) return -90;
            for (int 수 = 0; 수 < 다; 수++) Memoria_fitxategi_sistema.edizio_balio[수] = 실행관리.수(나 + 4 + 수 * 4) & 255;
            return Memoria_fitxategi_sistema.Store_balio(Memoria_fitxategi_sistema.Izena, luzera_balio, Memoria_fitxategi_sistema.edizio_balio, 다);
        }
        return -38;
    }
}
