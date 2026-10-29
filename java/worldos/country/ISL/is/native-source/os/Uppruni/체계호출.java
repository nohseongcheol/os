// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 notandi bendill/길이는 aðgangur_færsla 전에 검사한다. */
public final class 체계호출 {
    static int[] 임시자료 = new int[1024];

    static int ARRAY_lengd(int slóð) {
        if (!실행관리.miðlaskrá(slóð, 4)) return -14;
        int lengd_VALUE = 실행관리.númer(slóð);
        if (lengd_VALUE < 0 || lengd_VALUE > (실행관리.notandi_ljúka - slóð - 4) / 4) return -14;
        return lengd_VALUE;
    }

    public static int Ferli_VALUE_færsla(int INDEX, int 가, int 나, int 다, int 라, int 마) {
        if (INDEX == 30) return 파일서술자관리.opið_skrá(가, 나, 다);
        if (INDEX == 31) return 파일서술자관리.파일읽기(가, 나, 다);
        if (INDEX == 32) return 파일서술자관리.skrifa_skrá(가, 나, 다);
        if (INDEX == 33) return 파일서술자관리.loka_skrá(가);
        if (INDEX == 34) return 파일서술자관리.leita_skrá(가, 나, 다);
        if (INDEX == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (INDEX == 36) return 파일서술자관리.서술자복제(가, 나, true, 0);
        if (INDEX == 37) return 파일서술자관리.파일상태읽기(가, 나);
        if (INDEX == 38) return 파일서술자관리.fjarlægja_skrá_færsla_heiti(가);
        if (INDEX == 39) return 파일서술자관리.sett_skrá_lengd(가, 나);
        if (INDEX == 40) return 파일서술자관리.서술자제어(가, 나, 다);
        if (INDEX == 41) return 파일서술자관리.stofna_endastöð(가, 나, 다);
        if (INDEX == 42) return 파일서술자관리.BIND_slóð(가, 나, 다);
        if (INDEX == 43) return 파일서술자관리.자료전문보내기(가, 나, 다, 라, 마);
        if (INDEX == 44) return 파일서술자관리.자료전문받기(가, 나, 다, 라, 마);
        if (INDEX == 45) return 파일서술자관리.통신주소읽기(가, 나, 다);
        if (INDEX == 46) return 파일서술자관리.수신대기정하기(가, 나);
        if (INDEX == 47) {
            int 기술 = 파일서술자관리.기술찾기(가);
            if (기술 < 0) return -9;
            if (파일서술자관리.종류[기술] != 2) return -22;
            return 파일보존.samstilla();
        }
        if (INDEX == 1) {
            int lengd_VALUE = ARRAY_lengd(가);
            if (lengd_VALUE < 0) return lengd_VALUE;
            if (lengd_VALUE > 4096) return -90;
            for (int stafur_VALUE = 0; stafur_VALUE < lengd_VALUE; stafur_VALUE++) SMS_Endastöð.문자(실행관리.númer(가 + 4 + stafur_VALUE * 4) & 65535);
            return lengd_VALUE;
        }
        if (INDEX == 2) return 실행관리.frumbreyta_COUNT;
        if (INDEX == 3) return 가 >= 0 && 가 < 실행관리.frumbreyta_COUNT ? 실행관리.frumbreyta_slóð[가] : 0;
        if (INDEX == 10) return Net_bunki.Opna(가);
        if (INDEX == 11) {
            int lengd_VALUE = ARRAY_lengd(라);
            if (lengd_VALUE < 0) return lengd_VALUE;
            if (마 < 0 || 마 > lengd_VALUE || 마 > 1024) return -90;
            for (int Staðsetning = 0; Staðsetning < 마; Staðsetning++) 임시자료[Staðsetning] = 실행관리.númer(라 + 4 + Staðsetning * 4) & 255;
            return Net_bunki.senda(가, 나, 다, 임시자료, 마);
        }
        if (INDEX == 12) {
            int lengd_VALUE = ARRAY_lengd(나);
            if (lengd_VALUE < 0) return lengd_VALUE;
            if (다 < 0 || 다 > 2000) return -22;
            int NIÐURSTAÐA = Net_bunki.받기(가, 임시자료, lengd_VALUE < 1024 ? lengd_VALUE : 1024, 다);
            if (NIÐURSTAÐA >= 0) for (int Staðsetning = 0; Staðsetning < NIÐURSTAÐA; Staðsetning++) 실행관리.skrifa_númer(나 + 4 + Staðsetning * 4, 임시자료[Staðsetning]);
            return NIÐURSTAÐA;
        }
        if (INDEX == 13) return Net_bunki.Loka(가);
        if (INDEX == 14) return Net_bunki.내주소;
        if (INDEX == 15) return Net_bunki.jafningi_slóð(가);
        if (INDEX == 16) return Net_bunki.jafningi_tengisnúmer(가);
        if (INDEX == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            SMS_Endastöð.문자(가); return 1;
        }
        if (INDEX == 20 || INDEX == 21) {
            int heiti_breyta_stærð = ARRAY_lengd(가), gögn_breyta_stærð = ARRAY_lengd(나);
            if (heiti_breyta_stærð < 0 || gögn_breyta_stærð < 0) return -14;
            if (heiti_breyta_stærð < 1 || heiti_breyta_stærð > 64) return -22;
            int lengd_VALUE = 0;
            while (lengd_VALUE < heiti_breyta_stærð && 실행관리.númer(가 + 4 + lengd_VALUE * 4) != 0) {
                Minni_skrárkerfi.Heiti[lengd_VALUE] = 실행관리.númer(가 + 4 + lengd_VALUE * 4);
                lengd_VALUE++;
            }
            if (!Minni_skrárkerfi.athuga_heiti(Minni_skrárkerfi.Heiti, lengd_VALUE)) return -22;
            if (INDEX == 20) {
                int Skrá = Minni_skrárkerfi.FIND_færsla(Minni_skrárkerfi.Heiti, lengd_VALUE);
                if (Skrá < 0) return Skrá;
                int Stærð = Minni_skrárkerfi.breyta_stærð_Listi[Skrá];
                if (Stærð > gögn_breyta_stærð) return -90;
                int slóð = tæki_VALUE.skrá_Minni() + Skrá * Minni_skrárkerfi.최대크기;
                for (int númer = 0; númer < Stærð; númer++) 실행관리.skrifa_númer(나 + 4 + númer * 4, tæki_VALUE.기억읽기(slóð + númer));
                return Stærð;
            }
            if (다 < 0 || 다 > gögn_breyta_stærð) return -22;
            if (다 > Minni_skrárkerfi.최대크기) return -90;
            for (int númer = 0; númer < 다; númer++) Minni_skrárkerfi.breyta_VALUE[númer] = 실행관리.númer(나 + 4 + númer * 4) & 255;
            return Minni_skrárkerfi.Store_VALUE(Minni_skrárkerfi.Heiti, lengd_VALUE, Minni_skrárkerfi.breyta_VALUE, 다);
        }
        return -38;
    }
}
