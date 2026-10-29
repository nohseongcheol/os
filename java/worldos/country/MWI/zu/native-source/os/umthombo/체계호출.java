// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 umsebenzisi isikhombi/길이는 ungeno_okufakwayo 전에 검사한다. */
public final class 체계호출 {
    static int[] 임시자료 = new int[1024];

    static int AMALUNGU_AFANAYO_ubude(int ikheli) {
        if (!실행관리.isiqeshana(ikheli, 4)) return -14;
        int ubude_inani = 실행관리.수(ikheli);
        if (ubude_inani < 0 || ubude_inani > (실행관리.umsebenzisi_yekisa - ikheli - 4) / 4) return -14;
        return ubude_inani;
    }

    public static int Inqubo_inani_okufakwayo(int thola_inkomba, int 가, int 나, int 다, int 라, int 마) {
        if (thola_inkomba == 30) return 파일서술자관리.vula_ifayela(가, 나, 다);
        if (thola_inkomba == 31) return 파일서술자관리.파일읽기(가, 나, 다);
        if (thola_inkomba == 32) return 파일서술자관리.bhala_ifayela(가, 나, 다);
        if (thola_inkomba == 33) return 파일서술자관리.vala_ifayela(가);
        if (thola_inkomba == 34) return 파일서술자관리.cinga_ifayela(가, 나, 다);
        if (thola_inkomba == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (thola_inkomba == 36) return 파일서술자관리.서술자복제(가, 나, true, 0);
        if (thola_inkomba == 37) return 파일서술자관리.파일상태읽기(가, 나);
        if (thola_inkomba == 38) return 파일서술자관리.khipha_ifayela_okufakwayo_igama(가);
        if (thola_inkomba == 39) return 파일서술자관리.isethi_ifayela_ubude(가, 나);
        if (thola_inkomba == 40) return 파일서술자관리.서술자제어(가, 나, 다);
        if (thola_inkomba == 41) return 파일서술자관리.통신종단점만들기(가, 나, 다);
        if (thola_inkomba == 42) return 파일서술자관리.i_BIND_ikheli(가, 나, 다);
        if (thola_inkomba == 43) return 파일서술자관리.자료전문보내기(가, 나, 다, 라, 마);
        if (thola_inkomba == 44) return 파일서술자관리.자료전문받기(가, 나, 다, 라, 마);
        if (thola_inkomba == 45) return 파일서술자관리.통신주소읽기(가, 나, 다);
        if (thola_inkomba == 46) return 파일서술자관리.수신대기정하기(가, 나);
        if (thola_inkomba == 47) {
            int 기술 = 파일서술자관리.기술찾기(가);
            if (기술 < 0) return -9;
            if (파일서술자관리.종류[기술] != 2) return -22;
            return 파일보존.i_sync();
        }
        if (thola_inkomba == 1) {
            int ubude_inani = AMALUNGU_AFANAYO_ubude(가);
            if (ubude_inani < 0) return ubude_inani;
            if (ubude_inani > 4096) return -90;
            for (int uhlamvusimo_inani = 0; uhlamvusimo_inani < ubude_inani; uhlamvusimo_inani++) 문자단말.문자(실행관리.수(가 + 4 + uhlamvusimo_inani * 4) & 65535);
            return ubude_inani;
        }
        if (thola_inkomba == 2) return 실행관리.인수수;
        if (thola_inkomba == 3) return 가 >= 0 && 가 < 실행관리.인수수 ? 실행관리.i_agumenti_ikheli[가] : 0;
        if (thola_inkomba == 10) return iNethiwekhi_Isitaki.Vula(가);
        if (thola_inkomba == 11) {
            int ubude_inani = AMALUNGU_AFANAYO_ubude(라);
            if (ubude_inani < 0) return ubude_inani;
            if (마 < 0 || 마 > ubude_inani || 마 > 1024) return -90;
            for (int 위치 = 0; 위치 < 마; 위치++) 임시자료[위치] = 실행관리.수(라 + 4 + 위치 * 4) & 255;
            return iNethiwekhi_Isitaki.Thumela(가, 나, 다, 임시자료, 마);
        }
        if (thola_inkomba == 12) {
            int ubude_inani = AMALUNGU_AFANAYO_ubude(나);
            if (ubude_inani < 0) return ubude_inani;
            if (다 < 0 || 다 > 2000) return -22;
            int 결과 = iNethiwekhi_Isitaki.받기(가, 임시자료, ubude_inani < 1024 ? ubude_inani : 1024, 다);
            if (결과 >= 0) for (int 위치 = 0; 위치 < 결과; 위치++) 실행관리.수쓰기(나 + 4 + 위치 * 4, 임시자료[위치]);
            return 결과;
        }
        if (thola_inkomba == 13) return iNethiwekhi_Isitaki.Vala(가);
        if (thola_inkomba == 14) return iNethiwekhi_Isitaki.내주소;
        if (thola_inkomba == 15) return iNethiwekhi_Isitaki.untanga_ikheli(가);
        if (thola_inkomba == 16) return iNethiwekhi_Isitaki.상대접속번호(가);
        if (thola_inkomba == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            문자단말.문자(가); return 1;
        }
        if (thola_inkomba == 20 || thola_inkomba == 21) {
            int igama_linganisa = AMALUNGU_AFANAYO_ubude(가), imininingwane_linganisa = AMALUNGU_AFANAYO_ubude(나);
            if (igama_linganisa < 0 || imininingwane_linganisa < 0) return -14;
            if (igama_linganisa < 1 || igama_linganisa > 64) return -22;
            int ubude_inani = 0;
            while (ubude_inani < igama_linganisa && 실행관리.수(가 + 4 + ubude_inani * 4) != 0) {
                inkumbulo_isistimu_yefayela.Igama[ubude_inani] = 실행관리.수(가 + 4 + ubude_inani * 4);
                ubude_inani++;
            }
            if (!inkumbulo_isistimu_yefayela.hlola_igama(inkumbulo_isistimu_yefayela.Igama, ubude_inani)) return -22;
            if (thola_inkomba == 20) {
                int Ihele = inkumbulo_isistimu_yefayela.thola_okufakwayo(inkumbulo_isistimu_yefayela.Igama, ubude_inani);
                if (Ihele < 0) return Ihele;
                int Ubungako = inkumbulo_isistimu_yefayela.linganisa_Uhlu[Ihele];
                if (Ubungako > imininingwane_linganisa) return -90;
                int ikheli = idivayisi_inani.ifayela_inkumbulo() + Ihele * inkumbulo_isistimu_yefayela.최대크기;
                for (int 수 = 0; 수 < Ubungako; 수++) 실행관리.수쓰기(나 + 4 + 수 * 4, idivayisi_inani.기억읽기(ikheli + 수));
                return Ubungako;
            }
            if (다 < 0 || 다 > imininingwane_linganisa) return -22;
            if (다 > inkumbulo_isistimu_yefayela.최대크기) return -90;
            for (int 수 = 0; 수 < 다; 수++) inkumbulo_isistimu_yefayela.hlela_inani[수] = 실행관리.수(나 + 4 + 수 * 4) & 255;
            return inkumbulo_isistimu_yefayela.Store_inani(inkumbulo_isistimu_yefayela.Igama, ubude_inani, inkumbulo_isistimu_yefayela.hlela_inani, 다);
        }
        return -38;
    }
}
