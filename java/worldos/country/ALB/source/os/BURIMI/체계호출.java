// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 përdorues tregues/길이는 qasem_futje 전에 검사한다. */
public final class 체계호출 {
    static int[] 임시자료 = new int[1024];

    static int ARRAY_gjatësi(int email) {
        if (!실행관리.fragment(email, 4)) return -14;
        int gjatësi_VALUE = 실행관리.수(email);
        if (gjatësi_VALUE < 0 || gjatësi_VALUE > (실행관리.përdorues_mbaroj - email - 4) / 4) return -14;
        return gjatësi_VALUE;
    }

    public static int Proces_VALUE_futje(int INDEX, int 가, int 나, int 다, int 라, int 마) {
        if (INDEX == 30) return 파일서술자관리.hap_skedar(가, 나, 다);
        if (INDEX == 31) return 파일서술자관리.파일읽기(가, 나, 다);
        if (INDEX == 32) return 파일서술자관리.shkruaj_skedar(가, 나, 다);
        if (INDEX == 33) return 파일서술자관리.mbyll_skedar(가);
        if (INDEX == 34) return 파일서술자관리.kërko_skedar(가, 나, 다);
        if (INDEX == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (INDEX == 36) return 파일서술자관리.서술자복제(가, 나, true, 0);
        if (INDEX == 37) return 파일서술자관리.파일상태읽기(가, 나);
        if (INDEX == 38) return 파일서술자관리.heq_skedar_futje_emër(가);
        if (INDEX == 39) return 파일서술자관리.bashkësi_skedar_gjatësi(가, 나);
        if (INDEX == 40) return 파일서술자관리.서술자제어(가, 나, 다);
        if (INDEX == 41) return 파일서술자관리.통신종단점만들기(가, 나, 다);
        if (INDEX == 42) return 파일서술자관리.BIND_email(가, 나, 다);
        if (INDEX == 43) return 파일서술자관리.자료전문보내기(가, 나, 다, 라, 마);
        if (INDEX == 44) return 파일서술자관리.자료전문받기(가, 나, 다, 라, 마);
        if (INDEX == 45) return 파일서술자관리.통신주소읽기(가, 나, 다);
        if (INDEX == 46) return 파일서술자관리.수신대기정하기(가, 나);
        if (INDEX == 47) {
            int 기술 = 파일서술자관리.기술찾기(가);
            if (기술 < 0) return -9;
            if (파일서술자관리.종류[기술] != 2) return -22;
            return 파일보존.sinkronizoj();
        }
        if (INDEX == 1) {
            int gjatësi_VALUE = ARRAY_gjatësi(가);
            if (gjatësi_VALUE < 0) return gjatësi_VALUE;
            if (gjatësi_VALUE > 4096) return -90;
            for (int karakter_VALUE = 0; karakter_VALUE < gjatësi_VALUE; karakter_VALUE++) SMS_Terminali.문자(실행관리.수(가 + 4 + karakter_VALUE * 4) & 65535);
            return gjatësi_VALUE;
        }
        if (INDEX == 2) return 실행관리.argument_COUNT;
        if (INDEX == 3) return 가 >= 0 && 가 < 실행관리.argument_COUNT ? 실행관리.argument_email[가] : 0;
        if (INDEX == 10) return rrjet_Stivë.Hap(가);
        if (INDEX == 11) {
            int gjatësi_VALUE = ARRAY_gjatësi(라);
            if (gjatësi_VALUE < 0) return gjatësi_VALUE;
            if (마 < 0 || 마 > gjatësi_VALUE || 마 > 1024) return -90;
            for (int Pozicioni = 0; Pozicioni < 마; Pozicioni++) 임시자료[Pozicioni] = 실행관리.수(라 + 4 + Pozicioni * 4) & 255;
            return rrjet_Stivë.dërgoj(가, 나, 다, 임시자료, 마);
        }
        if (INDEX == 12) {
            int gjatësi_VALUE = ARRAY_gjatësi(나);
            if (gjatësi_VALUE < 0) return gjatësi_VALUE;
            if (다 < 0 || 다 > 2000) return -22;
            int llogaritje = rrjet_Stivë.받기(가, 임시자료, gjatësi_VALUE < 1024 ? gjatësi_VALUE : 1024, 다);
            if (llogaritje >= 0) for (int Pozicioni = 0; Pozicioni < llogaritje; Pozicioni++) 실행관리.수쓰기(나 + 4 + Pozicioni * 4, 임시자료[Pozicioni]);
            return llogaritje;
        }
        if (INDEX == 13) return rrjet_Stivë.Mbyll(가);
        if (INDEX == 14) return rrjet_Stivë.내주소;
        if (INDEX == 15) return rrjet_Stivë.homolog_email(가);
        if (INDEX == 16) return rrjet_Stivë.homolog_numri_i_portës(가);
        if (INDEX == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            SMS_Terminali.문자(가); return 1;
        }
        if (INDEX == 20 || INDEX == 21) {
            int emër_ndryshoj_përmasat = ARRAY_gjatësi(가), të_dhëna_ndryshoj_përmasat = ARRAY_gjatësi(나);
            if (emër_ndryshoj_përmasat < 0 || të_dhëna_ndryshoj_përmasat < 0) return -14;
            if (emër_ndryshoj_përmasat < 1 || emër_ndryshoj_përmasat > 64) return -22;
            int gjatësi_VALUE = 0;
            while (gjatësi_VALUE < emër_ndryshoj_përmasat && 실행관리.수(가 + 4 + gjatësi_VALUE * 4) != 0) {
                Memorie_sistemi_i_skedarëve.Emër[gjatësi_VALUE] = 실행관리.수(가 + 4 + gjatësi_VALUE * 4);
                gjatësi_VALUE++;
            }
            if (!Memorie_sistemi_i_skedarëve.çek_emër(Memorie_sistemi_i_skedarëve.Emër, gjatësi_VALUE)) return -22;
            if (INDEX == 20) {
                int Kartelë = Memorie_sistemi_i_skedarëve.FIND_futje(Memorie_sistemi_i_skedarëve.Emër, gjatësi_VALUE);
                if (Kartelë < 0) return Kartelë;
                int Madhësi = Memorie_sistemi_i_skedarëve.ndryshoj_përmasat_Listë[Kartelë];
                if (Madhësi > të_dhëna_ndryshoj_përmasat) return -90;
                int email = pajisje_VALUE.skedar_Memorie() + Kartelë * Memorie_sistemi_i_skedarëve.최대크기;
                for (int 수 = 0; 수 < Madhësi; 수++) 실행관리.수쓰기(나 + 4 + 수 * 4, pajisje_VALUE.기억읽기(email + 수));
                return Madhësi;
            }
            if (다 < 0 || 다 > të_dhëna_ndryshoj_përmasat) return -22;
            if (다 > Memorie_sistemi_i_skedarëve.최대크기) return -90;
            for (int 수 = 0; 수 < 다; 수++) Memorie_sistemi_i_skedarëve.redaktim_VALUE[수] = 실행관리.수(나 + 4 + 수 * 4) & 255;
            return Memorie_sistemi_i_skedarëve.Store_VALUE(Memorie_sistemi_i_skedarëve.Emër, gjatësi_VALUE, Memorie_sistemi_i_skedarëve.redaktim_VALUE, 다);
        }
        return -38;
    }
}
