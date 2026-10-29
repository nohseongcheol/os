// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 úsáideoir pointeoir/길이는 rochtain_iontráil 전에 검사한다. */
public final class 체계호출 {
    static int[] 임시자료 = new int[1024];

    static int ARRAY_fad(int ADDRESS) {
        if (!실행관리.gearrthóg(ADDRESS, 4)) return -14;
        int fad_VALUE = 실행관리.수(ADDRESS);
        if (fad_VALUE < 0 || fad_VALUE > (실행관리.úsáideoir_cuir_deireadh_le - ADDRESS - 4) / 4) return -14;
        return fad_VALUE;
    }

    public static int Próiseas_VALUE_iontráil(int INDEX, int 가, int 나, int 다, int 라, int 마) {
        if (INDEX == 30) return 파일서술자관리.oscail_comhad(가, 나, 다);
        if (INDEX == 31) return 파일서술자관리.파일읽기(가, 나, 다);
        if (INDEX == 32) return 파일서술자관리.scríobh_comhad(가, 나, 다);
        if (INDEX == 33) return 파일서술자관리.dún_comhad(가);
        if (INDEX == 34) return 파일서술자관리.lorg_comhad(가, 나, 다);
        if (INDEX == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (INDEX == 36) return 파일서술자관리.서술자복제(가, 나, true, 0);
        if (INDEX == 37) return 파일서술자관리.파일상태읽기(가, 나);
        if (INDEX == 38) return 파일서술자관리.bain_comhad_iontráil_ainm(가);
        if (INDEX == 39) return 파일서술자관리.tacar_comhad_fad(가, 나);
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
            return 파일보존.sioncronaigh();
        }
        if (INDEX == 1) {
            int fad_VALUE = ARRAY_fad(가);
            if (fad_VALUE < 0) return fad_VALUE;
            if (fad_VALUE > 4096) return -90;
            for (int carachtar_VALUE = 0; carachtar_VALUE < fad_VALUE; carachtar_VALUE++) SMS_Teirminéal.문자(실행관리.수(가 + 4 + carachtar_VALUE * 4) & 65535);
            return fad_VALUE;
        }
        if (INDEX == 2) return 실행관리.argóint_COUNT;
        if (INDEX == 3) return 가 >= 0 && 가 < 실행관리.argóint_COUNT ? 실행관리.argóint_ADDRESS[가] : 0;
        if (INDEX == 10) return Líonra_Cruach.Oscail(가);
        if (INDEX == 11) {
            int fad_VALUE = ARRAY_fad(라);
            if (fad_VALUE < 0) return fad_VALUE;
            if (마 < 0 || 마 > fad_VALUE || 마 > 1024) return -90;
            for (int suíomh = 0; suíomh < 마; suíomh++) 임시자료[suíomh] = 실행관리.수(라 + 4 + suíomh * 4) & 255;
            return Líonra_Cruach.seol(가, 나, 다, 임시자료, 마);
        }
        if (INDEX == 12) {
            int fad_VALUE = ARRAY_fad(나);
            if (fad_VALUE < 0) return fad_VALUE;
            if (다 < 0 || 다 > 2000) return -22;
            int tomhas = Líonra_Cruach.받기(가, 임시자료, fad_VALUE < 1024 ? fad_VALUE : 1024, 다);
            if (tomhas >= 0) for (int suíomh = 0; suíomh < tomhas; suíomh++) 실행관리.수쓰기(나 + 4 + suíomh * 4, 임시자료[suíomh]);
            return tomhas;
        }
        if (INDEX == 13) return Líonra_Cruach.Dún(가);
        if (INDEX == 14) return Líonra_Cruach.내주소;
        if (INDEX == 15) return Líonra_Cruach.piara_ADDRESS(가);
        if (INDEX == 16) return Líonra_Cruach.piara_uimhir_phoirt(가);
        if (INDEX == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            SMS_Teirminéal.문자(가); return 1;
        }
        if (INDEX == 20 || INDEX == 21) {
            int ainm_socraigh_méid = ARRAY_fad(가), sonraí_socraigh_méid = ARRAY_fad(나);
            if (ainm_socraigh_méid < 0 || sonraí_socraigh_méid < 0) return -14;
            if (ainm_socraigh_méid < 1 || ainm_socraigh_méid > 64) return -22;
            int fad_VALUE = 0;
            while (fad_VALUE < ainm_socraigh_méid && 실행관리.수(가 + 4 + fad_VALUE * 4) != 0) {
                Cuimhne_córas_comhad.Ainm[fad_VALUE] = 실행관리.수(가 + 4 + fad_VALUE * 4);
                fad_VALUE++;
            }
            if (!Cuimhne_córas_comhad.seic_ainm(Cuimhne_córas_comhad.Ainm, fad_VALUE)) return -22;
            if (INDEX == 20) {
                int Comhad = Cuimhne_córas_comhad.FIND_iontráil(Cuimhne_córas_comhad.Ainm, fad_VALUE);
                if (Comhad < 0) return Comhad;
                int Méid = Cuimhne_córas_comhad.socraigh_méid_Liosta[Comhad];
                if (Méid > sonraí_socraigh_méid) return -90;
                int ADDRESS = gléas_VALUE.comhad_Cuimhne() + Comhad * Cuimhne_córas_comhad.최대크기;
                for (int 수 = 0; 수 < Méid; 수++) 실행관리.수쓰기(나 + 4 + 수 * 4, gléas_VALUE.기억읽기(ADDRESS + 수));
                return Méid;
            }
            if (다 < 0 || 다 > sonraí_socraigh_méid) return -22;
            if (다 > Cuimhne_córas_comhad.최대크기) return -90;
            for (int 수 = 0; 수 < 다; 수++) Cuimhne_córas_comhad.cuir_in_eagar_VALUE[수] = 실행관리.수(나 + 4 + 수 * 4) & 255;
            return Cuimhne_córas_comhad.Store_VALUE(Cuimhne_córas_comhad.Ainm, fad_VALUE, Cuimhne_córas_comhad.cuir_in_eagar_VALUE, 다);
        }
        return -38;
    }
}
