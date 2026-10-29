// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 kaiwhakamahi atatohu/길이는 uru_tāurunga 전에 검사한다. */
public final class 체계호출 {
    static int[] 임시자료 = new int[1024];

    static int HUĀNGA_roa(int ADDRESS) {
        if (!실행관리.topenga(ADDRESS, 4)) return -14;
        int roa_uara = 실행관리.수(ADDRESS);
        if (roa_uara < 0 || roa_uara > (실행관리.kaiwhakamahi_mutu - ADDRESS - 4) / 4) return -14;
        return roa_uara;
    }

    public static int Hātepe_uara_tāurunga(int INDEX, int 가, int 나, int 다, int 라, int 마) {
        if (INDEX == 30) return 파일서술자관리.tiwhikete_kōnae(가, 나, 다);
        if (INDEX == 31) return 파일서술자관리.파일읽기(가, 나, 다);
        if (INDEX == 32) return 파일서술자관리.tuhi_kōnae(가, 나, 다);
        if (INDEX == 33) return 파일서술자관리.kati_kōnae(가);
        if (INDEX == 34) return 파일서술자관리.kimi_kōnae(가, 나, 다);
        if (INDEX == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (INDEX == 36) return 파일서술자관리.서술자복제(가, 나, true, 0);
        if (INDEX == 37) return 파일서술자관리.파일상태읽기(가, 나);
        if (INDEX == 38) return 파일서술자관리.tango_kōnae_tāurunga_ingoa(가);
        if (INDEX == 39) return 파일서술자관리.huinga_kōnae_roa(가, 나);
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
            return 파일보존.tukutahi();
        }
        if (INDEX == 1) {
            int roa_uara = HUĀNGA_roa(가);
            if (roa_uara < 0) return roa_uara;
            if (roa_uara > 4096) return -90;
            for (int pūāhua_uara = 0; pūāhua_uara < roa_uara; pūāhua_uara++) TEXT_Tauranga.문자(실행관리.수(가 + 4 + pūāhua_uara * 4) & 65535);
            return roa_uara;
        }
        if (INDEX == 2) return 실행관리.tohenga_COUNT;
        if (INDEX == 3) return 가 >= 0 && 가 < 실행관리.tohenga_COUNT ? 실행관리.tohenga_ADDRESS[가] : 0;
        if (INDEX == 10) return whatunga_Huinga.Huaki(가);
        if (INDEX == 11) {
            int roa_uara = HUĀNGA_roa(라);
            if (roa_uara < 0) return roa_uara;
            if (마 < 0 || 마 > roa_uara || 마 > 1024) return -90;
            for (int tūranga = 0; tūranga < 마; tūranga++) 임시자료[tūranga] = 실행관리.수(라 + 4 + tūranga * 4) & 255;
            return whatunga_Huinga.tuku(가, 나, 다, 임시자료, 마);
        }
        if (INDEX == 12) {
            int roa_uara = HUĀNGA_roa(나);
            if (roa_uara < 0) return roa_uara;
            if (다 < 0 || 다 > 2000) return -22;
            int mēhua = whatunga_Huinga.받기(가, 임시자료, roa_uara < 1024 ? roa_uara : 1024, 다);
            if (mēhua >= 0) for (int tūranga = 0; tūranga < mēhua; tūranga++) 실행관리.수쓰기(나 + 4 + tūranga * 4, 임시자료[tūranga]);
            return mēhua;
        }
        if (INDEX == 13) return whatunga_Huinga.Kati(가);
        if (INDEX == 14) return whatunga_Huinga.내주소;
        if (INDEX == 15) return whatunga_Huinga.hoa_ADDRESS(가);
        if (INDEX == 16) return whatunga_Huinga.상대접속번호(가);
        if (INDEX == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            TEXT_Tauranga.문자(가); return 1;
        }
        if (INDEX == 20 || INDEX == 21) {
            int ingoa_rahi = HUĀNGA_roa(가), raraunga_rahi = HUĀNGA_roa(나);
            if (ingoa_rahi < 0 || raraunga_rahi < 0) return -14;
            if (ingoa_rahi < 1 || ingoa_rahi > 64) return -22;
            int roa_uara = 0;
            while (roa_uara < ingoa_rahi && 실행관리.수(가 + 4 + roa_uara * 4) != 0) {
                Pūmahara_pūnaha_kōnae.Ingoa[roa_uara] = 실행관리.수(가 + 4 + roa_uara * 4);
                roa_uara++;
            }
            if (!Pūmahara_pūnaha_kōnae.taki_ingoa(Pūmahara_pūnaha_kōnae.Ingoa, roa_uara)) return -22;
            if (INDEX == 20) {
                int Kōnae = Pūmahara_pūnaha_kōnae.FIND_tāurunga(Pūmahara_pūnaha_kōnae.Ingoa, roa_uara);
                if (Kōnae < 0) return Kōnae;
                int rahi = Pūmahara_pūnaha_kōnae.rahi_Rārangi[Kōnae];
                if (rahi > raraunga_rahi) return -90;
                int ADDRESS = pūkoro_uara.kōnae_Pūmahara() + Kōnae * Pūmahara_pūnaha_kōnae.최대크기;
                for (int 수 = 0; 수 < rahi; 수++) 실행관리.수쓰기(나 + 4 + 수 * 4, pūkoro_uara.기억읽기(ADDRESS + 수));
                return rahi;
            }
            if (다 < 0 || 다 > raraunga_rahi) return -22;
            if (다 > Pūmahara_pūnaha_kōnae.최대크기) return -90;
            for (int 수 = 0; 수 < 다; 수++) Pūmahara_pūnaha_kōnae.whakatika_uara[수] = 실행관리.수(나 + 4 + 수 * 4) & 255;
            return Pūmahara_pūnaha_kōnae.Store_uara(Pūmahara_pūnaha_kōnae.Ingoa, roa_uara, Pūmahara_pūnaha_kōnae.whakatika_uara, 다);
        }
        return -38;
    }
}
