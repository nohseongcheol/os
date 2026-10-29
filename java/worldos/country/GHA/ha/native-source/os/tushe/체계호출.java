// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 Mai_anfani_da_kwamfuta manuni/길이는 isa_Mashigar_bayanai 전에 검사한다. */
public final class 체계호출 {
    static int[] 임시자료 = new int[1024];

    static int TSARI_Tsawo(int imel) {
        if (!실행관리.darfi(imel, 4)) return -14;
        int Tsawo_Daraja = 실행관리.수(imel);
        if (Tsawo_Daraja < 0 || Tsawo_Daraja > (실행관리.Mai_anfani_da_kwamfuta_Ƙarshe - imel - 4) / 4) return -14;
        return Tsawo_Daraja;
    }

    public static int haryar_aikin_na_ura_Daraja_Mashigar_bayanai(int Indes, int 가, int 나, int 다, int 라, int 마) {
        if (Indes == 30) return 파일서술자관리.buɗe_Fayil(가, 나, 다);
        if (Indes == 31) return 파일서술자관리.파일읽기(가, 나, 다);
        if (Indes == 32) return 파일서술자관리.Rubuta_Fayil(가, 나, 다);
        if (Indes == 33) return 파일서술자관리.Rufe_Fayil(가);
        if (Indes == 34) return 파일서술자관리.binciko_Fayil(가, 나, 다);
        if (Indes == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (Indes == 36) return 파일서술자관리.서술자복제(가, 나, true, 0);
        if (Indes == 37) return 파일서술자관리.파일상태읽기(가, 나);
        if (Indes == 38) return 파일서술자관리.Cire_Fayil_Mashigar_bayanai_Suna(가);
        if (Indes == 39) return 파일서술자관리.zubi_Fayil_Tsawo(가, 나);
        if (Indes == 40) return 파일서술자관리.서술자제어(가, 나, 다);
        if (Indes == 41) return 파일서술자관리.통신종단점만들기(가, 나, 다);
        if (Indes == 42) return 파일서술자관리.BIND_imel(가, 나, 다);
        if (Indes == 43) return 파일서술자관리.자료전문보내기(가, 나, 다, 라, 마);
        if (Indes == 44) return 파일서술자관리.자료전문받기(가, 나, 다, 라, 마);
        if (Indes == 45) return 파일서술자관리.통신주소읽기(가, 나, 다);
        if (Indes == 46) return 파일서술자관리.수신대기정하기(가, 나);
        if (Indes == 47) {
            int 기술 = 파일서술자관리.기술찾기(가);
            if (기술 < 0) return -9;
            if (파일서술자관리.종류[기술] != 2) return -22;
            return 파일보존.daidaita();
        }
        if (Indes == 1) {
            int Tsawo_Daraja = TSARI_Tsawo(가);
            if (Tsawo_Daraja < 0) return Tsawo_Daraja;
            if (Tsawo_Daraja > 4096) return -90;
            for (int Harafi_Daraja = 0; Harafi_Daraja < Tsawo_Daraja; Harafi_Daraja++) 문자단말.문자(실행관리.수(가 + 4 + Harafi_Daraja * 4) & 65535);
            return Tsawo_Daraja;
        }
        if (Indes == 2) return 실행관리.인수수;
        if (Indes == 3) return 가 >= 0 && 가 < 실행관리.인수수 ? 실행관리.Tubalin_aiki_imel[가] : 0;
        if (Indes == 10) return Hanyar_sadarwa_tara.Buɗe(가);
        if (Indes == 11) {
            int Tsawo_Daraja = TSARI_Tsawo(라);
            if (Tsawo_Daraja < 0) return Tsawo_Daraja;
            if (마 < 0 || 마 > Tsawo_Daraja || 마 > 1024) return -90;
            for (int 위치 = 0; 위치 < 마; 위치++) 임시자료[위치] = 실행관리.수(라 + 4 + 위치 * 4) & 255;
            return Hanyar_sadarwa_tara.Aika(가, 나, 다, 임시자료, 마);
        }
        if (Indes == 12) {
            int Tsawo_Daraja = TSARI_Tsawo(나);
            if (Tsawo_Daraja < 0) return Tsawo_Daraja;
            if (다 < 0 || 다 > 2000) return -22;
            int 결과 = Hanyar_sadarwa_tara.받기(가, 임시자료, Tsawo_Daraja < 1024 ? Tsawo_Daraja : 1024, 다);
            if (결과 >= 0) for (int 위치 = 0; 위치 < 결과; 위치++) 실행관리.수쓰기(나 + 4 + 위치 * 4, 임시자료[위치]);
            return 결과;
        }
        if (Indes == 13) return Hanyar_sadarwa_tara.Rufe(가);
        if (Indes == 14) return Hanyar_sadarwa_tara.내주소;
        if (Indes == 15) return Hanyar_sadarwa_tara.Fiya_imel(가);
        if (Indes == 16) return Hanyar_sadarwa_tara.Fiya_lambar_kafa(가);
        if (Indes == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            문자단말.문자(가); return 1;
        }
        if (Indes == 20 || Indes == 21) {
            int Suna_girma = TSARI_Tsawo(가), Tarin_bayani_girma = TSARI_Tsawo(나);
            if (Suna_girma < 0 || Tarin_bayani_girma < 0) return -14;
            if (Suna_girma < 1 || Suna_girma > 64) return -22;
            int Tsawo_Daraja = 0;
            while (Tsawo_Daraja < Suna_girma && 실행관리.수(가 + 4 + Tsawo_Daraja * 4) != 0) {
                Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.Suna[Tsawo_Daraja] = 실행관리.수(가 + 4 + Tsawo_Daraja * 4);
                Tsawo_Daraja++;
            }
            if (!Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.Bincika_Suna(Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.Suna, Tsawo_Daraja)) return -22;
            if (Indes == 20) {
                int Fayil = Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.nema_Mashigar_bayanai(Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.Suna, Tsawo_Daraja);
                if (Fayil < 0) return Fayil;
                int Girma = Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.girma_Jeri[Fayil];
                if (Girma > Tarin_bayani_girma) return -90;
                int imel = na_ura_Daraja.Fayil_Mahardatar_kwamfuta() + Fayil * Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.최대크기;
                for (int 수 = 0; 수 < Girma; 수++) 실행관리.수쓰기(나 + 4 + 수 * 4, na_ura_Daraja.기억읽기(imel + 수));
                return Girma;
            }
            if (다 < 0 || 다 > Tarin_bayani_girma) return -22;
            if (다 > Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.최대크기) return -90;
            for (int 수 = 0; 수 < 다; 수++) Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.gyaran_Daraja[수] = 실행관리.수(나 + 4 + 수 * 4) & 255;
            return Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.Ajiye_Daraja(Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.Suna, Tsawo_Daraja, Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.gyaran_Daraja, 다);
        }
        return -38;
    }
}
