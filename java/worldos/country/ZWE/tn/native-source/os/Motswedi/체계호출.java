// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 modirisi sesupi/길이는 letlelesega_tsenyo 전에 검사한다. */
public final class 체계호출 {
    static int[] 임시자료 = new int[1024];

    static int setlhopha_boleele(int aterese) {
        if (!실행관리.faelekhutshwe_ya_media(aterese, 4)) return -14;
        int boleele_Boleng = 실행관리.수(aterese);
        if (boleele_Boleng < 0 || boleele_Boleng > (실행관리.modirisi_kgaola - aterese - 4) / 4) return -14;
        return boleele_Boleng;
    }

    public static int Thulaganyo_Boleng_tsenyo(int tshupane, int 가, int 나, int 다, int 라, int 마) {
        if (tshupane == 30) return 파일서술자관리.bula_faele(가, 나, 다);
        if (tshupane == 31) return 파일서술자관리.파일읽기(가, 나, 다);
        if (tshupane == 32) return 파일서술자관리.kwala_faele(가, 나, 다);
        if (tshupane == 33) return 파일서술자관리.tswala_faele(가);
        if (tshupane == 34) return 파일서술자관리.batla_faele(가, 나, 다);
        if (tshupane == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (tshupane == 36) return 파일서술자관리.서술자복제(가, 나, true, 0);
        if (tshupane == 37) return 파일서술자관리.파일상태읽기(가, 나);
        if (tshupane == 38) return 파일서술자관리.tlosa_faele_tsenyo_leina(가);
        if (tshupane == 39) return 파일서술자관리.sete_faele_boleele(가, 나);
        if (tshupane == 40) return 파일서술자관리.서술자제어(가, 나, 다);
        if (tshupane == 41) return 파일서술자관리.통신종단점만들기(가, 나, 다);
        if (tshupane == 42) return 파일서술자관리.BIND_aterese(가, 나, 다);
        if (tshupane == 43) return 파일서술자관리.자료전문보내기(가, 나, 다, 라, 마);
        if (tshupane == 44) return 파일서술자관리.자료전문받기(가, 나, 다, 라, 마);
        if (tshupane == 45) return 파일서술자관리.통신주소읽기(가, 나, 다);
        if (tshupane == 46) return 파일서술자관리.수신대기정하기(가, 나);
        if (tshupane == 47) {
            int 기술 = 파일서술자관리.기술찾기(가);
            if (기술 < 0) return -9;
            if (파일서술자관리.종류[기술] != 2) return -22;
            return 파일보존.tsamaisanya();
        }
        if (tshupane == 1) {
            int boleele_Boleng = setlhopha_boleele(가);
            if (boleele_Boleng < 0) return boleele_Boleng;
            if (boleele_Boleng > 4096) return -90;
            for (int Letshwao_Boleng = 0; Letshwao_Boleng < boleele_Boleng; Letshwao_Boleng++) 문자단말.문자(실행관리.수(가 + 4 + Letshwao_Boleng * 4) & 65535);
            return boleele_Boleng;
        }
        if (tshupane == 2) return 실행관리.인수수;
        if (tshupane == 3) return 가 >= 0 && 가 < 실행관리.인수수 ? 실행관리.Thulaganyo_aterese_841f6346[가] : 0;
        if (tshupane == 10) return Neteweke_kokoanyodinepe.bula(가);
        if (tshupane == 11) {
            int boleele_Boleng = setlhopha_boleele(라);
            if (boleele_Boleng < 0) return boleele_Boleng;
            if (마 < 0 || 마 > boleele_Boleng || 마 > 1024) return -90;
            for (int 위치 = 0; 위치 < 마; 위치++) 임시자료[위치] = 실행관리.수(라 + 4 + 위치 * 4) & 255;
            return Neteweke_kokoanyodinepe.romela(가, 나, 다, 임시자료, 마);
        }
        if (tshupane == 12) {
            int boleele_Boleng = setlhopha_boleele(나);
            if (boleele_Boleng < 0) return boleele_Boleng;
            if (다 < 0 || 다 > 2000) return -22;
            int 결과 = Neteweke_kokoanyodinepe.받기(가, 임시자료, boleele_Boleng < 1024 ? boleele_Boleng : 1024, 다);
            if (결과 >= 0) for (int 위치 = 0; 위치 < 결과; 위치++) 실행관리.수쓰기(나 + 4 + 위치 * 4, 임시자료[위치]);
            return 결과;
        }
        if (tshupane == 13) return Neteweke_kokoanyodinepe.tswala(가);
        if (tshupane == 14) return Neteweke_kokoanyodinepe.내주소;
        if (tshupane == 15) return Neteweke_kokoanyodinepe.semphato_aterese(가);
        if (tshupane == 16) return Neteweke_kokoanyodinepe.상대접속번호(가);
        if (tshupane == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            문자단말.문자(가); return 1;
        }
        if (tshupane == 20 || tshupane == 21) {
            int leina_lekanya = setlhopha_boleele(가), tshedimosetso_lekanya = setlhopha_boleele(나);
            if (leina_lekanya < 0 || tshedimosetso_lekanya < 0) return -14;
            if (leina_lekanya < 1 || leina_lekanya > 64) return -22;
            int boleele_Boleng = 0;
            while (boleele_Boleng < leina_lekanya && 실행관리.수(가 + 4 + boleele_Boleng * 4) != 0) {
                memori_setsamaisadifaele.leina[boleele_Boleng] = 실행관리.수(가 + 4 + boleele_Boleng * 4);
                boleele_Boleng++;
            }
            if (!memori_setsamaisadifaele.tlhola_leina(memori_setsamaisadifaele.leina, boleele_Boleng)) return -22;
            if (tshupane == 20) {
                int faele = memori_setsamaisadifaele.batla_tsenyo(memori_setsamaisadifaele.leina, boleele_Boleng);
                if (faele < 0) return faele;
                int lekanya = memori_setsamaisadifaele.lekanya_lenaane[faele];
                if (lekanya > tshedimosetso_lekanya) return -90;
                int aterese = mobaele_Boleng.faele_memori() + faele * memori_setsamaisadifaele.최대크기;
                for (int 수 = 0; 수 < lekanya; 수++) 실행관리.수쓰기(나 + 4 + 수 * 4, mobaele_Boleng.기억읽기(aterese + 수));
                return lekanya;
            }
            if (다 < 0 || 다 > tshedimosetso_lekanya) return -22;
            if (다 > memori_setsamaisadifaele.최대크기) return -90;
            for (int 수 = 0; 수 < 다; 수++) memori_setsamaisadifaele.Tseleganya_Boleng[수] = 실행관리.수(나 + 4 + 수 * 4) & 255;
            return memori_setsamaisadifaele.Store_Boleng(memori_setsamaisadifaele.leina, boleele_Boleng, memori_setsamaisadifaele.Tseleganya_Boleng, 다);
        }
        return -38;
    }
}
