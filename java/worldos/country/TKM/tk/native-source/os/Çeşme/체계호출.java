// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 ulanyjy görkeziji/길이는 ygtyýarlylyk_girizmeklik 전에 검사한다. */
public final class 체계호출 {
    static int[] 임시자료 = new int[1024];

    static int ARRAY_dowamlylyk(int salgy) {
        if (!실행관리.klip(salgy, 4)) return -14;
        int dowamlylyk_baha = 실행관리.수(salgy);
        if (dowamlylyk_baha < 0 || dowamlylyk_baha > (실행관리.ulanyjy_tamamla - salgy - 4) / 4) return -14;
        return dowamlylyk_baha;
    }

    public static int Proses_baha_girizmeklik(int indeks, int 가, int 나, int 다, int 라, int 마) {
        if (indeks == 30) return 파일서술자관리.aç_faýl(가, 나, 다);
        if (indeks == 31) return 파일서술자관리.파일읽기(가, 나, 다);
        if (indeks == 32) return 파일서술자관리.ýaz_faýl(가, 나, 다);
        if (indeks == 33) return 파일서술자관리.ýap_faýl(가);
        if (indeks == 34) return 파일서술자관리.gözle_faýl(가, 나, 다);
        if (indeks == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (indeks == 36) return 파일서술자관리.서술자복제(가, 나, true, 0);
        if (indeks == 37) return 파일서술자관리.파일상태읽기(가, 나);
        if (indeks == 38) return 파일서술자관리.aýyr_faýl_girizmeklik_at(가);
        if (indeks == 39) return 파일서술자관리.köplük_faýl_dowamlylyk(가, 나);
        if (indeks == 40) return 파일서술자관리.서술자제어(가, 나, 다);
        if (indeks == 41) return 파일서술자관리.통신종단점만들기(가, 나, 다);
        if (indeks == 42) return 파일서술자관리.BIND_salgy(가, 나, 다);
        if (indeks == 43) return 파일서술자관리.자료전문보내기(가, 나, 다, 라, 마);
        if (indeks == 44) return 파일서술자관리.자료전문받기(가, 나, 다, 라, 마);
        if (indeks == 45) return 파일서술자관리.통신주소읽기(가, 나, 다);
        if (indeks == 46) return 파일서술자관리.수신대기정하기(가, 나);
        if (indeks == 47) {
            int 기술 = 파일서술자관리.기술찾기(가);
            if (기술 < 0) return -9;
            if (파일서술자관리.종류[기술] != 2) return -22;
            return 파일보존.sinhronlaşdyr();
        }
        if (indeks == 1) {
            int dowamlylyk_baha = ARRAY_dowamlylyk(가);
            if (dowamlylyk_baha < 0) return dowamlylyk_baha;
            if (dowamlylyk_baha > 4096) return -90;
            for (int nyşan_baha_068c2631 = 0; nyşan_baha_068c2631 < dowamlylyk_baha; nyşan_baha_068c2631++) 문자단말.문자(실행관리.수(가 + 4 + nyşan_baha_068c2631 * 4) & 65535);
            return dowamlylyk_baha;
        }
        if (indeks == 2) return 실행관리.인수수;
        if (indeks == 3) return 가 >= 0 && 가 < 실행관리.인수수 ? 실행관리.argument_salgy[가] : 0;
        if (indeks == 10) return Tor_Desse.Aç(가);
        if (indeks == 11) {
            int dowamlylyk_baha = ARRAY_dowamlylyk(라);
            if (dowamlylyk_baha < 0) return dowamlylyk_baha;
            if (마 < 0 || 마 > dowamlylyk_baha || 마 > 1024) return -90;
            for (int 위치 = 0; 위치 < 마; 위치++) 임시자료[위치] = 실행관리.수(라 + 4 + 위치 * 4) & 255;
            return Tor_Desse.iber(가, 나, 다, 임시자료, 마);
        }
        if (indeks == 12) {
            int dowamlylyk_baha = ARRAY_dowamlylyk(나);
            if (dowamlylyk_baha < 0) return dowamlylyk_baha;
            if (다 < 0 || 다 > 2000) return -22;
            int 결과 = Tor_Desse.받기(가, 임시자료, dowamlylyk_baha < 1024 ? dowamlylyk_baha : 1024, 다);
            if (결과 >= 0) for (int 위치 = 0; 위치 < 결과; 위치++) 실행관리.수쓰기(나 + 4 + 위치 * 4, 임시자료[위치]);
            return 결과;
        }
        if (indeks == 13) return Tor_Desse.Ýap(가);
        if (indeks == 14) return Tor_Desse.내주소;
        if (indeks == 15) return Tor_Desse.deň_derejeli_düwün_salgy(가);
        if (indeks == 16) return Tor_Desse.상대접속번호(가);
        if (indeks == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            문자단말.문자(가); return 1;
        }
        if (indeks == 20 || indeks == 21) {
            int at_ölçegi_üýtget = ARRAY_dowamlylyk(가), maglumat_ölçegi_üýtget = ARRAY_dowamlylyk(나);
            if (at_ölçegi_üýtget < 0 || maglumat_ölçegi_üýtget < 0) return -14;
            if (at_ölçegi_üýtget < 1 || at_ölçegi_üýtget > 64) return -22;
            int dowamlylyk_baha = 0;
            while (dowamlylyk_baha < at_ölçegi_üýtget && 실행관리.수(가 + 4 + dowamlylyk_baha * 4) != 0) {
                ýat_faýl_ulgamy.Ad[dowamlylyk_baha] = 실행관리.수(가 + 4 + dowamlylyk_baha * 4);
                dowamlylyk_baha++;
            }
            if (!ýat_faýl_ulgamy.derňe_at(ýat_faýl_ulgamy.Ad, dowamlylyk_baha)) return -22;
            if (indeks == 20) {
                int Faýl = ýat_faýl_ulgamy.tap_girizmeklik(ýat_faýl_ulgamy.Ad, dowamlylyk_baha);
                if (Faýl < 0) return Faýl;
                int Ululyk = ýat_faýl_ulgamy.ölçegi_üýtget_Sanaw[Faýl];
                if (Ululyk > maglumat_ölçegi_üýtget) return -90;
                int salgy = enjam_baha.faýl_ýat() + Faýl * ýat_faýl_ulgamy.최대크기;
                for (int 수 = 0; 수 < Ululyk; 수++) 실행관리.수쓰기(나 + 4 + 수 * 4, enjam_baha.기억읽기(salgy + 수));
                return Ululyk;
            }
            if (다 < 0 || 다 > maglumat_ölçegi_üýtget) return -22;
            if (다 > ýat_faýl_ulgamy.최대크기) return -90;
            for (int 수 = 0; 수 < 다; 수++) ýat_faýl_ulgamy.redaktirle_baha[수] = 실행관리.수(나 + 4 + 수 * 4) & 255;
            return ýat_faýl_ulgamy.Store_baha(ýat_faýl_ulgamy.Ad, dowamlylyk_baha, ýat_faýl_ulgamy.redaktirle_baha, 다);
        }
        return -38;
    }
}
