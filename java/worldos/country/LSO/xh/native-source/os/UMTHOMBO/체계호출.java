// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 umsebenzisi isalathisi/길이는 fikelela_ufako_nkcukacha 전에 검사한다. */
public final class 체계호출 {
    static int[] 임시자료 = new int[1024];

    static int ULUHLU_ubude(int idilesi) {
        if (!실행관리.ikliphu(idilesi, 4)) return -14;
        int ubude_ixabiso = 실행관리.수(idilesi);
        if (ubude_ixabiso < 0 || ubude_ixabiso > (실행관리.umsebenzisi_phela - idilesi - 4) / 4) return -14;
        return ubude_ixabiso;
    }

    public static int Inkqubo_ixabiso_ufako_nkcukacha(int indeksa, int 가, int 나, int 다, int 라, int 마) {
        if (indeksa == 30) return 파일서술자관리.vula_ifayile(가, 나, 다);
        if (indeksa == 31) return 파일서술자관리.파일읽기(가, 나, 다);
        if (indeksa == 32) return 파일서술자관리.bhala_ifayile(가, 나, 다);
        if (indeksa == 33) return 파일서술자관리.vala_ifayile(가);
        if (indeksa == 34) return 파일서술자관리.khangela_ifayile(가, 나, 다);
        if (indeksa == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (indeksa == 36) return 파일서술자관리.서술자복제(가, 나, true, 0);
        if (indeksa == 37) return 파일서술자관리.파일상태읽기(가, 나);
        if (indeksa == 38) return 파일서술자관리.shenxisa_ifayile_ufako_nkcukacha_igama(가);
        if (indeksa == 39) return 파일서술자관리.isethi_ifayile_ubude(가, 나);
        if (indeksa == 40) return 파일서술자관리.서술자제어(가, 나, 다);
        if (indeksa == 41) return 파일서술자관리.통신종단점만들기(가, 나, 다);
        if (indeksa == 42) return 파일서술자관리.BOPHELELA_idilesi(가, 나, 다);
        if (indeksa == 43) return 파일서술자관리.자료전문보내기(가, 나, 다, 라, 마);
        if (indeksa == 44) return 파일서술자관리.자료전문받기(가, 나, 다, 라, 마);
        if (indeksa == 45) return 파일서술자관리.통신주소읽기(가, 나, 다);
        if (indeksa == 46) return 파일서술자관리.수신대기정하기(가, 나);
        if (indeksa == 47) {
            int 기술 = 파일서술자관리.기술찾기(가);
            if (기술 < 0) return -9;
            if (파일서술자관리.종류[기술] != 2) return -22;
            return 파일보존.ngqamanisa();
        }
        if (indeksa == 1) {
            int ubude_ixabiso = ULUHLU_ubude(가);
            if (ubude_ixabiso < 0) return ubude_ixabiso;
            if (ubude_ixabiso > 4096) return -90;
            for (int ikharakhtha_ixabiso = 0; ikharakhtha_ixabiso < ubude_ixabiso; ikharakhtha_ixabiso++) 문자단말.문자(실행관리.수(가 + 4 + ikharakhtha_ixabiso * 4) & 65535);
            return ubude_ixabiso;
        }
        if (indeksa == 2) return 실행관리.인수수;
        if (indeksa == 3) return 가 >= 0 && 가 < 실행관리.인수수 ? 실행관리.isiniki_myalelo_idilesi[가] : 0;
        if (indeksa == 10) return Inethiwekhi_fumba.Vula(가);
        if (indeksa == 11) {
            int ubude_ixabiso = ULUHLU_ubude(라);
            if (ubude_ixabiso < 0) return ubude_ixabiso;
            if (마 < 0 || 마 > ubude_ixabiso || 마 > 1024) return -90;
            for (int 위치 = 0; 위치 < 마; 위치++) 임시자료[위치] = 실행관리.수(라 + 4 + 위치 * 4) & 255;
            return Inethiwekhi_fumba.thumela(가, 나, 다, 임시자료, 마);
        }
        if (indeksa == 12) {
            int ubude_ixabiso = ULUHLU_ubude(나);
            if (ubude_ixabiso < 0) return ubude_ixabiso;
            if (다 < 0 || 다 > 2000) return -22;
            int 결과 = Inethiwekhi_fumba.받기(가, 임시자료, ubude_ixabiso < 1024 ? ubude_ixabiso : 1024, 다);
            if (결과 >= 0) for (int 위치 = 0; 위치 < 결과; 위치++) 실행관리.수쓰기(나 + 4 + 위치 * 4, 임시자료[위치]);
            return 결과;
        }
        if (indeksa == 13) return Inethiwekhi_fumba.Vala(가);
        if (indeksa == 14) return Inethiwekhi_fumba.내주소;
        if (indeksa == 15) return Inethiwekhi_fumba.untanga_idilesi(가);
        if (indeksa == 16) return Inethiwekhi_fumba.상대접속번호(가);
        if (indeksa == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            문자단말.문자(가); return 1;
        }
        if (indeksa == 20 || indeksa == 21) {
            int igama_isayizi = ULUHLU_ubude(가), iingcombolo_isayizi = ULUHLU_ubude(나);
            if (igama_isayizi < 0 || iingcombolo_isayizi < 0) return -14;
            if (igama_isayizi < 1 || igama_isayizi > 64) return -22;
            int ubude_ixabiso = 0;
            while (ubude_ixabiso < igama_isayizi && 실행관리.수(가 + 4 + ubude_ixabiso * 4) != 0) {
                imemori_uhlobo_loseto_lwefayile.Igama[ubude_ixabiso] = 실행관리.수(가 + 4 + ubude_ixabiso * 4);
                ubude_ixabiso++;
            }
            if (!imemori_uhlobo_loseto_lwefayile.jonga_igama(imemori_uhlobo_loseto_lwefayile.Igama, ubude_ixabiso)) return -22;
            if (indeksa == 20) {
                int iFayili = imemori_uhlobo_loseto_lwefayile.fumana_ufako_nkcukacha(imemori_uhlobo_loseto_lwefayile.Igama, ubude_ixabiso);
                if (iFayili < 0) return iFayili;
                int Ubukhulu = imemori_uhlobo_loseto_lwefayile.isayizi_uludwe[iFayili];
                if (Ubukhulu > iingcombolo_isayizi) return -90;
                int idilesi = isixhobo_ixabiso.ifayile_imemori() + iFayili * imemori_uhlobo_loseto_lwefayile.최대크기;
                for (int 수 = 0; 수 < Ubukhulu; 수++) 실행관리.수쓰기(나 + 4 + 수 * 4, isixhobo_ixabiso.기억읽기(idilesi + 수));
                return Ubukhulu;
            }
            if (다 < 0 || 다 > iingcombolo_isayizi) return -22;
            if (다 > imemori_uhlobo_loseto_lwefayile.최대크기) return -90;
            for (int 수 = 0; 수 < 다; 수++) imemori_uhlobo_loseto_lwefayile.hlela_ixabiso[수] = 실행관리.수(나 + 4 + 수 * 4) & 255;
            return imemori_uhlobo_loseto_lwefayile.Store_ixabiso(imemori_uhlobo_loseto_lwefayile.Igama, ubude_ixabiso, imemori_uhlobo_loseto_lwefayile.hlela_ixabiso, 다);
        }
        return -38;
    }
}
