// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 Benotzer Uweiser/길이는 Zougrëff_Agab 전에 검사한다. */
public final class 체계호출 {
    static int[] 임시자료 = new int[1024];

    static int ARRAY_Längt(int Adress) {
        if (!실행관리.Clip(Adress, 4)) return -14;
        int Längt_VALUE = 실행관리.수(Adress);
        if (Längt_VALUE < 0 || Längt_VALUE > (실행관리.Benotzer_bëennegen - Adress - 4) / 4) return -14;
        return Längt_VALUE;
    }

    public static int Prozess_VALUE_Agab(int INDEX, int 가, int 나, int 다, int 라, int 마) {
        if (INDEX == 30) return 파일서술자관리.ariichten_Fichier(가, 나, 다);
        if (INDEX == 31) return 파일서술자관리.파일읽기(가, 나, 다);
        if (INDEX == 32) return 파일서술자관리.schreiwen_Fichier(가, 나, 다);
        if (INDEX == 33) return 파일서술자관리.Clôture_Fichier(가);
        if (INDEX == 34) return 파일서술자관리.sichen_Fichier(가, 나, 다);
        if (INDEX == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (INDEX == 36) return 파일서술자관리.서술자복제(가, 나, true, 0);
        if (INDEX == 37) return 파일서술자관리.파일상태읽기(가, 나);
        if (INDEX == 38) return 파일서술자관리.ewechhuelen_Fichier_Agab_Numm(가);
        if (INDEX == 39) return 파일서술자관리.Saz_Fichier_Längt(가, 나);
        if (INDEX == 40) return 파일서술자관리.서술자제어(가, 나, 다);
        if (INDEX == 41) return 파일서술자관리.통신종단점만들기(가, 나, 다);
        if (INDEX == 42) return 파일서술자관리.BANNEN_Adress(가, 나, 다);
        if (INDEX == 43) return 파일서술자관리.자료전문보내기(가, 나, 다, 라, 마);
        if (INDEX == 44) return 파일서술자관리.자료전문받기(가, 나, 다, 라, 마);
        if (INDEX == 45) return 파일서술자관리.통신주소읽기(가, 나, 다);
        if (INDEX == 46) return 파일서술자관리.수신대기정하기(가, 나);
        if (INDEX == 47) {
            int 기술 = 파일서술자관리.기술찾기(가);
            if (기술 < 0) return -9;
            if (파일서술자관리.종류[기술] != 2) return -22;
            return 파일보존.synchroniséieren();
        }
        if (INDEX == 1) {
            int Längt_VALUE = ARRAY_Längt(가);
            if (Längt_VALUE < 0) return Längt_VALUE;
            if (Längt_VALUE > 4096) return -90;
            for (int Zeechen_VALUE = 0; Zeechen_VALUE < Längt_VALUE; Zeechen_VALUE++) SMS_Terminal.문자(실행관리.수(가 + 4 + Zeechen_VALUE * 4) & 65535);
            return Längt_VALUE;
        }
        if (INDEX == 2) return 실행관리.Argument_COUNT;
        if (INDEX == 3) return 가 >= 0 && 가 < 실행관리.Argument_COUNT ? 실행관리.Argument_Adress[가] : 0;
        if (INDEX == 10) return Reseau_Stapel.ariichten(가);
        if (INDEX == 11) {
            int Längt_VALUE = ARRAY_Längt(라);
            if (Längt_VALUE < 0) return Längt_VALUE;
            if (마 < 0 || 마 > Längt_VALUE || 마 > 1024) return -90;
            for (int positionéieren = 0; positionéieren < 마; positionéieren++) 임시자료[positionéieren] = 실행관리.수(라 + 4 + positionéieren * 4) & 255;
            return Reseau_Stapel.mailen(가, 나, 다, 임시자료, 마);
        }
        if (INDEX == 12) {
            int Längt_VALUE = ARRAY_Längt(나);
            if (Längt_VALUE < 0) return Längt_VALUE;
            if (다 < 0 || 다 > 2000) return -22;
            int Mooss = Reseau_Stapel.받기(가, 임시자료, Längt_VALUE < 1024 ? Längt_VALUE : 1024, 다);
            if (Mooss >= 0) for (int positionéieren = 0; positionéieren < Mooss; positionéieren++) 실행관리.수쓰기(나 + 4 + positionéieren * 4, 임시자료[positionéieren]);
            return Mooss;
        }
        if (INDEX == 13) return Reseau_Stapel.Clôture(가);
        if (INDEX == 14) return Reseau_Stapel.내주소;
        if (INDEX == 15) return Reseau_Stapel.Peer_Adress(가);
        if (INDEX == 16) return Reseau_Stapel.상대접속번호(가);
        if (INDEX == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            SMS_Terminal.문자(가); return 1;
        }
        if (INDEX == 20 || INDEX == 21) {
            int Numm_d_Gréisst_veränneren = ARRAY_Längt(가), Daten_d_Gréisst_veränneren = ARRAY_Längt(나);
            if (Numm_d_Gréisst_veränneren < 0 || Daten_d_Gréisst_veränneren < 0) return -14;
            if (Numm_d_Gréisst_veränneren < 1 || Numm_d_Gréisst_veränneren > 64) return -22;
            int Längt_VALUE = 0;
            while (Längt_VALUE < Numm_d_Gréisst_veränneren && 실행관리.수(가 + 4 + Längt_VALUE * 4) != 0) {
                Späicher_Fichierssystem.Numm[Längt_VALUE] = 실행관리.수(가 + 4 + Längt_VALUE * 4);
                Längt_VALUE++;
            }
            if (!Späicher_Fichierssystem.Scheck_Numm(Späicher_Fichierssystem.Numm, Längt_VALUE)) return -22;
            if (INDEX == 20) {
                int Fichier = Späicher_Fichierssystem.FIND_Agab(Späicher_Fichierssystem.Numm, Längt_VALUE);
                if (Fichier < 0) return Fichier;
                int d_Gréisst_veränneren = Späicher_Fichierssystem.d_Gréisst_veränneren_Lëscht[Fichier];
                if (d_Gréisst_veränneren > Daten_d_Gréisst_veränneren) return -90;
                int Adress = Mobil_VALUE.Fichier_Späicher() + Fichier * Späicher_Fichierssystem.최대크기;
                for (int 수 = 0; 수 < d_Gréisst_veränneren; 수++) 실행관리.수쓰기(나 + 4 + 수 * 4, Mobil_VALUE.기억읽기(Adress + 수));
                return d_Gréisst_veränneren;
            }
            if (다 < 0 || 다 > Daten_d_Gréisst_veränneren) return -22;
            if (다 > Späicher_Fichierssystem.최대크기) return -90;
            for (int 수 = 0; 수 < 다; 수++) Späicher_Fichierssystem.Editéieren_VALUE[수] = 실행관리.수(나 + 4 + 수 * 4) & 255;
            return Späicher_Fichierssystem.Store_VALUE(Späicher_Fichierssystem.Numm, Längt_VALUE, Späicher_Fichierssystem.Editéieren_VALUE, 다);
        }
        return -38;
    }
}
