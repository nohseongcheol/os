// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 mtumiaji kielekezi/길이는 fikia_ingizo 전에 검사한다. */
public final class 체계호출 {
    static int[] 임시자료 = new int[1024];

    static int ARRAY_urefu(int anwani) {
        if (!실행관리.dondoo(anwani, 4)) return -14;
        int urefu_thamani = 실행관리.수(anwani);
        if (urefu_thamani < 0 || urefu_thamani > (실행관리.mtumiaji_tamatia - anwani - 4) / 4) return -14;
        return urefu_thamani;
    }

    public static int Mchakato_thamani_ingizo(int kielezo, int 가, int 나, int 다, int 라, int 마) {
        if (kielezo == 30) return 파일서술자관리.unda_faili(가, 나, 다);
        if (kielezo == 31) return 파일서술자관리.파일읽기(가, 나, 다);
        if (kielezo == 32) return 파일서술자관리.andika_faili(가, 나, 다);
        if (kielezo == 33) return 파일서술자관리.funga_faili(가);
        if (kielezo == 34) return 파일서술자관리.tafuta_faili(가, 나, 다);
        if (kielezo == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (kielezo == 36) return 파일서술자관리.서술자복제(가, 나, true, 0);
        if (kielezo == 37) return 파일서술자관리.파일상태읽기(가, 나);
        if (kielezo == 38) return 파일서술자관리.ondoa_faili_ingizo_jina(가);
        if (kielezo == 39) return 파일서술자관리.seti_faili_urefu(가, 나);
        if (kielezo == 40) return 파일서술자관리.서술자제어(가, 나, 다);
        if (kielezo == 41) return 파일서술자관리.통신종단점만들기(가, 나, 다);
        if (kielezo == 42) return 파일서술자관리.FUNGA_anwani(가, 나, 다);
        if (kielezo == 43) return 파일서술자관리.자료전문보내기(가, 나, 다, 라, 마);
        if (kielezo == 44) return 파일서술자관리.자료전문받기(가, 나, 다, 라, 마);
        if (kielezo == 45) return 파일서술자관리.통신주소읽기(가, 나, 다);
        if (kielezo == 46) return 파일서술자관리.수신대기정하기(가, 나);
        if (kielezo == 47) {
            int 기술 = 파일서술자관리.기술찾기(가);
            if (기술 < 0) return -9;
            if (파일서술자관리.종류[기술] != 2) return -22;
            return 파일보존.landanisha();
        }
        if (kielezo == 1) {
            int urefu_thamani = ARRAY_urefu(가);
            if (urefu_thamani < 0) return urefu_thamani;
            if (urefu_thamani > 4096) return -90;
            for (int kibambo_thamani = 0; kibambo_thamani < urefu_thamani; kibambo_thamani++) 문자단말.문자(실행관리.수(가 + 4 + kibambo_thamani * 4) & 65535);
            return urefu_thamani;
        }
        if (kielezo == 2) return 실행관리.인수수;
        if (kielezo == 3) return 가 >= 0 && 가 < 실행관리.인수수 ? 실행관리.hoja_anwani[가] : 0;
        if (kielezo == 10) return Mtandao_Mpororo.unda(가);
        if (kielezo == 11) {
            int urefu_thamani = ARRAY_urefu(라);
            if (urefu_thamani < 0) return urefu_thamani;
            if (마 < 0 || 마 > urefu_thamani || 마 > 1024) return -90;
            for (int 위치 = 0; 위치 < 마; 위치++) 임시자료[위치] = 실행관리.수(라 + 4 + 위치 * 4) & 255;
            return Mtandao_Mpororo.tuma(가, 나, 다, 임시자료, 마);
        }
        if (kielezo == 12) {
            int urefu_thamani = ARRAY_urefu(나);
            if (urefu_thamani < 0) return urefu_thamani;
            if (다 < 0 || 다 > 2000) return -22;
            int 결과 = Mtandao_Mpororo.받기(가, 임시자료, urefu_thamani < 1024 ? urefu_thamani : 1024, 다);
            if (결과 >= 0) for (int 위치 = 0; 위치 < 결과; 위치++) 실행관리.수쓰기(나 + 4 + 위치 * 4, 임시자료[위치]);
            return 결과;
        }
        if (kielezo == 13) return Mtandao_Mpororo.funga(가);
        if (kielezo == 14) return Mtandao_Mpororo.내주소;
        if (kielezo == 15) return Mtandao_Mpororo.kompyuta_rika_anwani(가);
        if (kielezo == 16) return Mtandao_Mpororo.kompyuta_rika_namba_ya_kituo(가);
        if (kielezo == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            문자단말.문자(가); return 1;
        }
        if (kielezo == 20 || kielezo == 21) {
            int jina_panga_ukubwa = ARRAY_urefu(가), data_panga_ukubwa = ARRAY_urefu(나);
            if (jina_panga_ukubwa < 0 || data_panga_ukubwa < 0) return -14;
            if (jina_panga_ukubwa < 1 || jina_panga_ukubwa > 64) return -22;
            int urefu_thamani = 0;
            while (urefu_thamani < jina_panga_ukubwa && 실행관리.수(가 + 4 + urefu_thamani * 4) != 0) {
                kumbukumbu_mfumo_ya_mafaili.Jina[urefu_thamani] = 실행관리.수(가 + 4 + urefu_thamani * 4);
                urefu_thamani++;
            }
            if (!kumbukumbu_mfumo_ya_mafaili.hundi_jina(kumbukumbu_mfumo_ya_mafaili.Jina, urefu_thamani)) return -22;
            if (kielezo == 20) {
                int faili = kumbukumbu_mfumo_ya_mafaili.gundua_ingizo(kumbukumbu_mfumo_ya_mafaili.Jina, urefu_thamani);
                if (faili < 0) return faili;
                int panga_ukubwa = kumbukumbu_mfumo_ya_mafaili.panga_ukubwa_Orodha[faili];
                if (panga_ukubwa > data_panga_ukubwa) return -90;
                int anwani = kifaa_thamani.faili_kumbukumbu() + faili * kumbukumbu_mfumo_ya_mafaili.최대크기;
                for (int 수 = 0; 수 < panga_ukubwa; 수++) 실행관리.수쓰기(나 + 4 + 수 * 4, kifaa_thamani.기억읽기(anwani + 수));
                return panga_ukubwa;
            }
            if (다 < 0 || 다 > data_panga_ukubwa) return -22;
            if (다 > kumbukumbu_mfumo_ya_mafaili.최대크기) return -90;
            for (int 수 = 0; 수 < 다; 수++) kumbukumbu_mfumo_ya_mafaili.hariri_thamani[수] = 실행관리.수(나 + 4 + 수 * 4) & 255;
            return kumbukumbu_mfumo_ya_mafaili.Store_thamani(kumbukumbu_mfumo_ya_mafaili.Jina, urefu_thamani, kumbukumbu_mfumo_ya_mafaili.hariri_thamani, 다);
        }
        return -38;
    }
}
