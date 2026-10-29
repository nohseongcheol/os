// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 mošomiši sešupi/길이는 fihlelela_go_tsenya_tshedimošo 전에 검사한다. */
public final class 체계호출 {
    static int[] 임시자료 = new int[1024];

    static int arei_botelele(int atrese) {
        if (!실행관리.setsopolwa(atrese, 4)) return -14;
        int botelele_boleng = 실행관리.수(atrese);
        if (botelele_boleng < 0 || botelele_boleng > (실행관리.mošomiši_fetša - atrese - 4) / 4) return -14;
        return botelele_boleng;
    }

    public static int tiragalo_boleng_go_tsenya_tshedimošo(int lokela, int 가, int 나, int 다, int 라, int 마) {
        if (lokela == 30) return 파일서술자관리.bula_faele(가, 나, 다);
        if (lokela == 31) return 파일서술자관리.파일읽기(가, 나, 다);
        if (lokela == 32) return 파일서술자관리.ngwala_faele(가, 나, 다);
        if (lokela == 33) return 파일서술자관리.tswalela_faele(가);
        if (lokela == 34) return 파일서술자관리.nyaka_faele(가, 나, 다);
        if (lokela == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (lokela == 36) return 파일서술자관리.서술자복제(가, 나, true, 0);
        if (lokela == 37) return 파일서술자관리.파일상태읽기(가, 나);
        if (lokela == 38) return 파일서술자관리.tloša_faele_go_tsenya_tshedimošo_leina(가);
        if (lokela == 39) return 파일서술자관리.sehlopha_faele_botelele(가, 나);
        if (lokela == 40) return 파일서술자관리.서술자제어(가, 나, 다);
        if (lokela == 41) return 파일서술자관리.통신종단점만들기(가, 나, 다);
        if (lokela == 42) return 파일서술자관리.tlama_atrese(가, 나, 다);
        if (lokela == 43) return 파일서술자관리.자료전문보내기(가, 나, 다, 라, 마);
        if (lokela == 44) return 파일서술자관리.자료전문받기(가, 나, 다, 라, 마);
        if (lokela == 45) return 파일서술자관리.통신주소읽기(가, 나, 다);
        if (lokela == 46) return 파일서술자관리.수신대기정하기(가, 나);
        if (lokela == 47) {
            int 기술 = 파일서술자관리.기술찾기(가);
            if (기술 < 0) return -9;
            if (파일서술자관리.종류[기술] != 2) return -22;
            return 파일보존.kopanya();
        }
        if (lokela == 1) {
            int botelele_boleng = arei_botelele(가);
            if (botelele_boleng < 0) return botelele_boleng;
            if (botelele_boleng > 4096) return -90;
            for (int tlhaka_boleng = 0; tlhaka_boleng < botelele_boleng; tlhaka_boleng++) 문자단말.문자(실행관리.수(가 + 4 + tlhaka_boleng * 4) & 65535);
            return botelele_boleng;
        }
        if (lokela == 2) return 실행관리.인수수;
        if (lokela == 3) return 가 >= 0 && 가 < 실행관리.인수수 ? 실행관리.akumente_atrese[가] : 0;
        if (lokela == 10) return Netweke_kgoboko.Bula(가);
        if (lokela == 11) {
            int botelele_boleng = arei_botelele(라);
            if (botelele_boleng < 0) return botelele_boleng;
            if (마 < 0 || 마 > botelele_boleng || 마 > 1024) return -90;
            for (int 위치 = 0; 위치 < 마; 위치++) 임시자료[위치] = 실행관리.수(라 + 4 + 위치 * 4) & 255;
            return Netweke_kgoboko.Romela(가, 나, 다, 임시자료, 마);
        }
        if (lokela == 12) {
            int botelele_boleng = arei_botelele(나);
            if (botelele_boleng < 0) return botelele_boleng;
            if (다 < 0 || 다 > 2000) return -22;
            int 결과 = Netweke_kgoboko.받기(가, 임시자료, botelele_boleng < 1024 ? botelele_boleng : 1024, 다);
            if (결과 >= 0) for (int 위치 = 0; 위치 < 결과; 위치++) 실행관리.수쓰기(나 + 4 + 위치 * 4, 임시자료[위치]);
            return 결과;
        }
        if (lokela == 13) return Netweke_kgoboko.Tswalela(가);
        if (lokela == 14) return Netweke_kgoboko.내주소;
        if (lokela == 15) return Netweke_kgoboko.sedirišwa_sa_legoro_le_tee_atrese(가);
        if (lokela == 16) return Netweke_kgoboko.상대접속번호(가);
        if (lokela == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            문자단말.문자(가); return 1;
        }
        if (lokela == 20 || lokela == 21) {
            int leina_bogolo = arei_botelele(가), data_bogolo = arei_botelele(나);
            if (leina_bogolo < 0 || data_bogolo < 0) return -14;
            if (leina_bogolo < 1 || leina_bogolo > 64) return -22;
            int botelele_boleng = 0;
            while (botelele_boleng < leina_bogolo && 실행관리.수(가 + 4 + botelele_boleng * 4) != 0) {
                memori_tshepedišo_ya_difaele.Leina[botelele_boleng] = 실행관리.수(가 + 4 + botelele_boleng * 4);
                botelele_boleng++;
            }
            if (!memori_tshepedišo_ya_difaele.lekola_leina(memori_tshepedišo_ya_difaele.Leina, botelele_boleng)) return -22;
            if (lokela == 20) {
                int Faele = memori_tshepedišo_ya_difaele.hwetša_go_tsenya_tshedimošo(memori_tshepedišo_ya_difaele.Leina, botelele_boleng);
                if (Faele < 0) return Faele;
                int Bogolo = memori_tshepedišo_ya_difaele.bogolo_Lenaneo[Faele];
                if (Bogolo > data_bogolo) return -90;
                int atrese = sedirišwa_boleng.faele_memori() + Faele * memori_tshepedišo_ya_difaele.최대크기;
                for (int 수 = 0; 수 < Bogolo; 수++) 실행관리.수쓰기(나 + 4 + 수 * 4, sedirišwa_boleng.기억읽기(atrese + 수));
                return Bogolo;
            }
            if (다 < 0 || 다 > data_bogolo) return -22;
            if (다 > memori_tshepedišo_ya_difaele.최대크기) return -90;
            for (int 수 = 0; 수 < 다; 수++) memori_tshepedišo_ya_difaele.rulaganya_boleng[수] = 실행관리.수(나 + 4 + 수 * 4) & 255;
            return memori_tshepedišo_ya_difaele.lota_boleng(memori_tshepedišo_ya_difaele.Leina, botelele_boleng, memori_tshepedišo_ya_difaele.rulaganya_boleng, 다);
        }
        return -38;
    }
}
