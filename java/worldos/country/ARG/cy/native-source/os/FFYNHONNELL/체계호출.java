// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 defnyddiwr pwyntydd/길이는 mynediad_cofnod 전에 검사한다. */
public final class 체계호출 {
    static int[] 임시자료 = new int[1024];

    static int ARAE_hyd(int ADDRESS) {
        if (!실행관리.clip(ADDRESS, 4)) return -14;
        int hyd_VALUE = 실행관리.수(ADDRESS);
        if (hyd_VALUE < 0 || hyd_VALUE > (실행관리.defnyddiwr_gorffen - ADDRESS - 4) / 4) return -14;
        return hyd_VALUE;
    }

    public static int Proses_VALUE_cofnod(int INDEX, int 가, int 나, int 다, int 라, int 마) {
        if (INDEX == 30) return 파일서술자관리.agor_ffeil(가, 나, 다);
        if (INDEX == 31) return 파일서술자관리.파일읽기(가, 나, 다);
        if (INDEX == 32) return 파일서술자관리.ysgrifennu_ffeil(가, 나, 다);
        if (INDEX == 33) return 파일서술자관리.cau_ffeil(가);
        if (INDEX == 34) return 파일서술자관리.chwilio_ffeil(가, 나, 다);
        if (INDEX == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (INDEX == 36) return 파일서술자관리.서술자복제(가, 나, true, 0);
        if (INDEX == 37) return 파일서술자관리.파일상태읽기(가, 나);
        if (INDEX == 38) return 파일서술자관리.tynnu_ffeil_cofnod_enw(가);
        if (INDEX == 39) return 파일서술자관리.set_ffeil_hyd(가, 나);
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
            return 파일보존.cysoni();
        }
        if (INDEX == 1) {
            int hyd_VALUE = ARAE_hyd(가);
            if (hyd_VALUE < 0) return hyd_VALUE;
            if (hyd_VALUE > 4096) return -90;
            for (int nod_VALUE = 0; nod_VALUE < hyd_VALUE; nod_VALUE++) SMS_Terfynell.문자(실행관리.수(가 + 4 + nod_VALUE * 4) & 65535);
            return hyd_VALUE;
        }
        if (INDEX == 2) return 실행관리.arg_COUNT;
        if (INDEX == 3) return 가 >= 0 && 가 < 실행관리.arg_COUNT ? 실행관리.arg_ADDRESS[가] : 0;
        if (INDEX == 10) return Rhwydwaith_pentwr.Agor(가);
        if (INDEX == 11) {
            int hyd_VALUE = ARAE_hyd(라);
            if (hyd_VALUE < 0) return hyd_VALUE;
            if (마 < 0 || 마 > hyd_VALUE || 마 > 1024) return -90;
            for (int safle = 0; safle < 마; safle++) 임시자료[safle] = 실행관리.수(라 + 4 + safle * 4) & 255;
            return Rhwydwaith_pentwr.anfon(가, 나, 다, 임시자료, 마);
        }
        if (INDEX == 12) {
            int hyd_VALUE = ARAE_hyd(나);
            if (hyd_VALUE < 0) return hyd_VALUE;
            if (다 < 0 || 다 > 2000) return -22;
            int mesur = Rhwydwaith_pentwr.받기(가, 임시자료, hyd_VALUE < 1024 ? hyd_VALUE : 1024, 다);
            if (mesur >= 0) for (int safle = 0; safle < mesur; safle++) 실행관리.수쓰기(나 + 4 + safle * 4, 임시자료[safle]);
            return mesur;
        }
        if (INDEX == 13) return Rhwydwaith_pentwr.Cau(가);
        if (INDEX == 14) return Rhwydwaith_pentwr.내주소;
        if (INDEX == 15) return Rhwydwaith_pentwr.cymar_ADDRESS(가);
        if (INDEX == 16) return Rhwydwaith_pentwr.cymar_rhif_porth(가);
        if (INDEX == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            SMS_Terfynell.문자(가); return 1;
        }
        if (INDEX == 20 || INDEX == 21) {
            int enw_newid_maint = ARAE_hyd(가), data_newid_maint = ARAE_hyd(나);
            if (enw_newid_maint < 0 || data_newid_maint < 0) return -14;
            if (enw_newid_maint < 1 || enw_newid_maint > 64) return -22;
            int hyd_VALUE = 0;
            while (hyd_VALUE < enw_newid_maint && 실행관리.수(가 + 4 + hyd_VALUE * 4) != 0) {
                Cof_system_ffeiliau.Enw[hyd_VALUE] = 실행관리.수(가 + 4 + hyd_VALUE * 4);
                hyd_VALUE++;
            }
            if (!Cof_system_ffeiliau.gwirio_enw(Cof_system_ffeiliau.Enw, hyd_VALUE)) return -22;
            if (INDEX == 20) {
                int Ffeil = Cof_system_ffeiliau.FIND_cofnod(Cof_system_ffeiliau.Enw, hyd_VALUE);
                if (Ffeil < 0) return Ffeil;
                int Maint = Cof_system_ffeiliau.newid_maint_Rhestr[Ffeil];
                if (Maint > data_newid_maint) return -90;
                int ADDRESS = dyfais_VALUE.ffeil_Cof() + Ffeil * Cof_system_ffeiliau.최대크기;
                for (int 수 = 0; 수 < Maint; 수++) 실행관리.수쓰기(나 + 4 + 수 * 4, dyfais_VALUE.기억읽기(ADDRESS + 수));
                return Maint;
            }
            if (다 < 0 || 다 > data_newid_maint) return -22;
            if (다 > Cof_system_ffeiliau.최대크기) return -90;
            for (int 수 = 0; 수 < 다; 수++) Cof_system_ffeiliau.Golygu_VALUE[수] = 실행관리.수(나 + 4 + 수 * 4) & 255;
            return Cof_system_ffeiliau.Store_VALUE(Cof_system_ffeiliau.Enw, hyd_VALUE, Cof_system_ffeiliau.Golygu_VALUE, 다);
        }
        return -38;
    }
}
