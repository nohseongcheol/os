// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 bruger markør/길이는 åbne_post 전에 검사한다. */
public final class 체계호출 {
    static int[] 임시자료 = new int[1024];

    static int MATRIX_varighed(int mail) {
        if (!udførelse_Leder.klippe(mail, 4)) return -14;
        int varighed_VÆRDI = udførelse_Leder.tal(mail);
        if (varighed_VÆRDI < 0 || varighed_VÆRDI > (udførelse_Leder.bruger_afslutte_et_opkald - mail - 4) / 4) return -14;
        return varighed_VÆRDI;
    }

    public static int Proces_VÆRDI_post(int INDEKS, int 가, int SEKUND_operand, int 다, int 라, int 마) {
        if (INDEKS == 30) return 파일서술자관리.åben_fil(가, SEKUND_operand, 다);
        if (INDEKS == 31) return 파일서술자관리.파일읽기(가, SEKUND_operand, 다);
        if (INDEKS == 32) return 파일서술자관리.skrive_fil(가, SEKUND_operand, 다);
        if (INDEKS == 33) return 파일서술자관리.Luk_fil(가);
        if (INDEKS == 34) return 파일서술자관리.søge_fil(가, SEKUND_operand, 다);
        if (INDEKS == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (INDEKS == 36) return 파일서술자관리.서술자복제(가, SEKUND_operand, true, 0);
        if (INDEKS == 37) return 파일서술자관리.파일상태읽기(가, SEKUND_operand);
        if (INDEKS == 38) return 파일서술자관리.fjerne_fil_post_navn(가);
        if (INDEKS == 39) return 파일서술자관리.sæt_fil_varighed(가, SEKUND_operand);
        if (INDEKS == 40) return 파일서술자관리.서술자제어(가, SEKUND_operand, 다);
        if (INDEKS == 41) return 파일서술자관리.åbne_slutpunkt(가, SEKUND_operand, 다);
        if (INDEKS == 42) return 파일서술자관리.BIND_mail(가, SEKUND_operand, 다);
        if (INDEKS == 43) return 파일서술자관리.maile_datagram_data(가, SEKUND_operand, 다, 라, 마);
        if (INDEKS == 44) return 파일서술자관리.modtage_datagram_data(가, SEKUND_operand, 다, 라, 마);
        if (INDEKS == 45) return 파일서술자관리.통신주소읽기(가, SEKUND_operand, 다);
        if (INDEKS == 46) return 파일서술자관리.sæt_modtage_TIMEOUT(가, SEKUND_operand);
        if (INDEKS == 47) {
            int 기술 = 파일서술자관리.기술찾기(가);
            if (기술 < 0) return -9;
            if (파일서술자관리.종류[기술] != 2) return -22;
            return 파일보존.synkronisere();
        }
        if (INDEKS == 1) {
            int varighed_VÆRDI = MATRIX_varighed(가);
            if (varighed_VÆRDI < 0) return varighed_VÆRDI;
            if (varighed_VÆRDI > 4096) return -90;
            for (int tegn_VÆRDI = 0; tegn_VÆRDI < varighed_VÆRDI; tegn_VÆRDI++) sms_Terminal.문자(udførelse_Leder.tal(가 + 4 + tegn_VÆRDI * 4) & 65535);
            return varighed_VÆRDI;
        }
        if (INDEKS == 2) return udførelse_Leder.argument_TÆL;
        if (INDEKS == 3) return 가 >= 0 && 가 < udførelse_Leder.argument_TÆL ? udførelse_Leder.argument_mail[가] : 0;
        if (INDEKS == 10) return netværk_Stak.Åbn(가);
        if (INDEKS == 11) {
            int varighed_VÆRDI = MATRIX_varighed(라);
            if (varighed_VÆRDI < 0) return varighed_VÆRDI;
            if (마 < 0 || 마 > varighed_VÆRDI || 마 > 1024) return -90;
            for (int Placering = 0; Placering < 마; Placering++) 임시자료[Placering] = udførelse_Leder.tal(라 + 4 + Placering * 4) & 255;
            return netværk_Stak.maile(가, SEKUND_operand, 다, 임시자료, 마);
        }
        if (INDEKS == 12) {
            int varighed_VÆRDI = MATRIX_varighed(SEKUND_operand);
            if (varighed_VÆRDI < 0) return varighed_VÆRDI;
            if (다 < 0 || 다 > 2000) return -22;
            int KR = netværk_Stak.modtage(가, 임시자료, varighed_VÆRDI < 1024 ? varighed_VÆRDI : 1024, 다);
            if (KR >= 0) for (int Placering = 0; Placering < KR; Placering++) udførelse_Leder.skrive_tal(SEKUND_operand + 4 + Placering * 4, 임시자료[Placering]);
            return KR;
        }
        if (INDEKS == 13) return netværk_Stak.Luk(가);
        if (INDEKS == 14) return netværk_Stak.내주소;
        if (INDEKS == 15) return netværk_Stak.peer_mail(가);
        if (INDEKS == 16) return netværk_Stak.peer_portnummer(가);
        if (INDEKS == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            sms_Terminal.문자(가); return 1;
        }
        if (INDEKS == 20 || INDEKS == 21) {
            int navn_tilpasse_størrelse = MATRIX_varighed(가), data_tilpasse_størrelse = MATRIX_varighed(SEKUND_operand);
            if (navn_tilpasse_størrelse < 0 || data_tilpasse_størrelse < 0) return -14;
            if (navn_tilpasse_størrelse < 1 || navn_tilpasse_størrelse > 64) return -22;
            int varighed_VÆRDI = 0;
            while (varighed_VÆRDI < navn_tilpasse_størrelse && udførelse_Leder.tal(가 + 4 + varighed_VÆRDI * 4) != 0) {
                Hukommelse_filsystem.Navn[varighed_VÆRDI] = udførelse_Leder.tal(가 + 4 + varighed_VÆRDI * 4);
                varighed_VÆRDI++;
            }
            if (!Hukommelse_filsystem.check_navn(Hukommelse_filsystem.Navn, varighed_VÆRDI)) return -22;
            if (INDEKS == 20) {
                int Fil = Hukommelse_filsystem.Søg_post(Hukommelse_filsystem.Navn, varighed_VÆRDI);
                if (Fil < 0) return Fil;
                int Størrelse = Hukommelse_filsystem.tilpasse_størrelse_Liste[Fil];
                if (Størrelse > data_tilpasse_størrelse) return -90;
                int mail = enhed_VÆRDI.fil_Hukommelse() + Fil * Hukommelse_filsystem.최대크기;
                for (int tal = 0; tal < Størrelse; tal++) udførelse_Leder.skrive_tal(SEKUND_operand + 4 + tal * 4, enhed_VÆRDI.기억읽기(mail + tal));
                return Størrelse;
            }
            if (다 < 0 || 다 > data_tilpasse_størrelse) return -22;
            if (다 > Hukommelse_filsystem.최대크기) return -90;
            for (int tal = 0; tal < 다; tal++) Hukommelse_filsystem.Rediger_VÆRDI[tal] = udførelse_Leder.tal(SEKUND_operand + 4 + tal * 4) & 255;
            return Hukommelse_filsystem.Store_VÆRDI(Hukommelse_filsystem.Navn, varighed_VÆRDI, Hukommelse_filsystem.Rediger_VÆRDI, 다);
        }
        return -38;
    }
}
