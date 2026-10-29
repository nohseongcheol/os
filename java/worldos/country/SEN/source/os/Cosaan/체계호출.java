// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 kiy_jariñoo_internet joxañukaay/길이는 jot_dugal_xabaar 전에 검사한다. */
public final class 체계호출 {
    static int[] 임시자료 = new int[1024];

    static int TABLO_diir(int dëkkuwaay) {
        if (!실행관리.kilip(dëkkuwaay, 4)) return -14;
        int diir_xëyma = 실행관리.수(dëkkuwaay);
        if (diir_xëyma < 0 || diir_xëyma > (실행관리.kiy_jariñoo_internet_jeexal - dëkkuwaay - 4) / 4) return -14;
        return diir_xëyma;
    }

    public static int yokkute_xëyma_dugal_xabaar(int àlluwa_tur, int 가, int 나, int 다, int 라, int 마) {
        if (àlluwa_tur == 30) return 파일서술자관리.sos_bara_denc(가, 나, 다);
        if (àlluwa_tur == 31) return 파일서술자관리.파일읽기(가, 나, 다);
        if (àlluwa_tur == 32) return 파일서술자관리.biir_bara_denc(가, 나, 다);
        if (àlluwa_tur == 33) return 파일서술자관리.Tej_bara_denc(가);
        if (àlluwa_tur == 34) return 파일서술자관리.seet_bara_denc(가, 나, 다);
        if (àlluwa_tur == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (àlluwa_tur == 36) return 파일서술자관리.서술자복제(가, 나, true, 0);
        if (àlluwa_tur == 37) return 파일서술자관리.파일상태읽기(가, 나);
        if (àlluwa_tur == 38) return 파일서술자관리.dandal_bara_denc_dugal_xabaar_tur(가);
        if (àlluwa_tur == 39) return 파일서술자관리.Boole_gi_bara_denc_diir(가, 나);
        if (àlluwa_tur == 40) return 파일서술자관리.서술자제어(가, 나, 다);
        if (àlluwa_tur == 41) return 파일서술자관리.통신종단점만들기(가, 나, 다);
        if (àlluwa_tur == 42) return 파일서술자관리.BIND_dëkkuwaay(가, 나, 다);
        if (àlluwa_tur == 43) return 파일서술자관리.자료전문보내기(가, 나, 다, 라, 마);
        if (àlluwa_tur == 44) return 파일서술자관리.자료전문받기(가, 나, 다, 라, 마);
        if (àlluwa_tur == 45) return 파일서술자관리.통신주소읽기(가, 나, 다);
        if (àlluwa_tur == 46) return 파일서술자관리.수신대기정하기(가, 나);
        if (àlluwa_tur == 47) {
            int 기술 = 파일서술자관리.기술찾기(가);
            if (기술 < 0) return -9;
            if (파일서술자관리.종류[기술] != 2) return -22;
            return 파일보존.lëkkale();
        }
        if (àlluwa_tur == 1) {
            int diir_xëyma = TABLO_diir(가);
            if (diir_xëyma < 0) return diir_xëyma;
            if (diir_xëyma > 4096) return -90;
            for (int Araf_xëyma = 0; Araf_xëyma < diir_xëyma; Araf_xëyma++) 문자단말.문자(실행관리.수(가 + 4 + Araf_xëyma * 4) & 65535);
            return diir_xëyma;
        }
        if (àlluwa_tur == 2) return 실행관리.인수수;
        if (àlluwa_tur == 3) return 가 >= 0 && 가 < 실행관리.인수수 ? 실행관리.Tegtal_dëkkuwaay[가] : 0;
        if (àlluwa_tur == 10) return mbaal_Tegalo.sos(가);
        if (àlluwa_tur == 11) {
            int diir_xëyma = TABLO_diir(라);
            if (diir_xëyma < 0) return diir_xëyma;
            if (마 < 0 || 마 > diir_xëyma || 마 > 1024) return -90;
            for (int 위치 = 0; 위치 < 마; 위치++) 임시자료[위치] = 실행관리.수(라 + 4 + 위치 * 4) & 255;
            return mbaal_Tegalo.Yónnee(가, 나, 다, 임시자료, 마);
        }
        if (àlluwa_tur == 12) {
            int diir_xëyma = TABLO_diir(나);
            if (diir_xëyma < 0) return diir_xëyma;
            if (다 < 0 || 다 > 2000) return -22;
            int 결과 = mbaal_Tegalo.받기(가, 임시자료, diir_xëyma < 1024 ? diir_xëyma : 1024, 다);
            if (결과 >= 0) for (int 위치 = 0; 위치 < 결과; 위치++) 실행관리.수쓰기(나 + 4 + 위치 * 4, 임시자료[위치]);
            return 결과;
        }
        if (àlluwa_tur == 13) return mbaal_Tegalo.Tej(가);
        if (àlluwa_tur == 14) return mbaal_Tegalo.내주소;
        if (àlluwa_tur == 15) return mbaal_Tegalo.Nàttangoo_dëkkuwaay(가);
        if (àlluwa_tur == 16) return mbaal_Tegalo.상대접속번호(가);
        if (àlluwa_tur == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            문자단말.문자(가); return 1;
        }
        if (àlluwa_tur == 20 || àlluwa_tur == 21) {
            int tur_tolluwaay = TABLO_diir(가), mbir_tolluwaay = TABLO_diir(나);
            if (tur_tolluwaay < 0 || mbir_tolluwaay < 0) return -14;
            if (tur_tolluwaay < 1 || tur_tolluwaay > 64) return -22;
            int diir_xëyma = 0;
            while (diir_xëyma < tur_tolluwaay && 실행관리.수(가 + 4 + diir_xëyma * 4) != 0) {
                fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.tur_253d1510[diir_xëyma] = 실행관리.수(가 + 4 + diir_xëyma * 4);
                diir_xëyma++;
            }
            if (!fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.sek_tur(fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.tur_253d1510, diir_xëyma)) return -22;
            if (àlluwa_tur == 20) {
                int bara_denc = fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.seet_dugal_xabaar(fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.tur_253d1510, diir_xëyma);
                if (bara_denc < 0) return bara_denc;
                int tolluwaay = fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.tolluwaay_lim[bara_denc];
                if (tolluwaay > mbir_tolluwaay) return -90;
                int dëkkuwaay = toftal_xëyma.bara_denc_fatlekookaay() + bara_denc * fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.최대크기;
                for (int 수 = 0; 수 < tolluwaay; 수++) 실행관리.수쓰기(나 + 4 + 수 * 4, toftal_xëyma.기억읽기(dëkkuwaay + 수));
                return tolluwaay;
            }
            if (다 < 0 || 다 > mbir_tolluwaay) return -22;
            if (다 > fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.최대크기) return -90;
            for (int 수 = 0; 수 < 다; 수++) fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.soppi_xëyma[수] = 실행관리.수(나 + 4 + 수 * 4) & 255;
            return fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.Store_xëyma(fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.tur_253d1510, diir_xëyma, fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.soppi_xëyma, 다);
        }
        return -38;
    }
}
