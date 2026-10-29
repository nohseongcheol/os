// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Læse 전용 Udfør_kommando 묶음의 ELF32 bekræfte_5fb2b747, Argumenter Frem_VÆRDI, 한 번에 한 bruger Proces_VÆRDI Udfør_kommando. */
public final class udførelse_Leder {
    static final int START_bruger_app = 0x04000000;
    static final int bruger_afslutte_et_opkald = 0x04400000;
    static final int Image_afslutte_et_opkald_mail = 0x04200000;
    static final int argument_START = 0x04300000;
    static int argument_TÆL = 0;
    static int[] argument_mail = new int[16];

    static boolean klippe(int mail, int varighed_VÆRDI) {
        return mail >= START_bruger_app && mail < bruger_afslutte_et_opkald && varighed_VÆRDI >= 0 && varighed_VÆRDI <= bruger_afslutte_et_opkald - mail;
    }

    static int tal(int mail) { return Hukommelse_område.opdele_tekst_heltal(mail); }
    static int 짧은수(int mail) { return enhed_VÆRDI.기억읽기(mail) | enhed_VÆRDI.기억읽기(mail + 1) << 8; }
    static void skrive_tal(int mail, int VÆRDI) {
        for (int INDEKS = 0; INDEKS < 4; INDEKS++) enhed_VÆRDI.skrive_Hukommelse(mail + INDEKS, VÆRDI >>> (INDEKS * 8));
    }

    static int gruppe_TÆL() {
        int mail = enhed_VÆRDI.eksekverbar_fil_bundt();
        int Størrelse = enhed_VÆRDI.eksekverbar_fil_bundt_tilpasse_størrelse();
        if (Størrelse < 8 || tal(mail) != 0x50414b4a) return 0;
        int vare_TÆL = tal(mail + 4);
        return vare_TÆL >= 0 && vare_TÆL <= 32 && vare_TÆL <= (Størrelse - 8) / 24 ? vare_TÆL : 0;
    }

    static void post_Liste() {
        for (int INDEKS = 0; INDEKS < gruppe_TÆL(); INDEKS++) {
            int post_VÆRDI_962f286b = enhed_VÆRDI.eksekverbar_fil_bundt() + 8 + INDEKS * 24;
            for (int tegn_VÆRDI = 0; tegn_VÆRDI < 16 && enhed_VÆRDI.기억읽기(post_VÆRDI_962f286b + tegn_VÆRDI) != 0; tegn_VÆRDI++)
                sms_Terminal.문자(enhed_VÆRDI.기억읽기(post_VÆRDI_962f286b + tegn_VÆRDI));
            sms_Terminal.Skrive("\n");
        }
    }

    static int Søg_post(int[] input_VÆRDI, int Kør_2, int varighed_VÆRDI) {
        if (varighed_VÆRDI <= 0 || varighed_VÆRDI >= 16) return 0;
        for (int INDEKS = 0; INDEKS < gruppe_TÆL(); INDEKS++) {
            int post_VÆRDI_962f286b = enhed_VÆRDI.eksekverbar_fil_bundt() + 8 + INDEKS * 24;
            boolean 같음 = enhed_VÆRDI.기억읽기(post_VÆRDI_962f286b + varighed_VÆRDI) == 0;
            for (int tegn_VÆRDI = 0; tegn_VÆRDI < varighed_VÆRDI; tegn_VÆRDI++)
                if (input_VÆRDI[Kør_2 + tegn_VÆRDI] != enhed_VÆRDI.기억읽기(post_VÆRDI_962f286b + tegn_VÆRDI)) 같음 = false;
            if (같음) return post_VÆRDI_962f286b;
        }
        return 0;
    }

    static int bekræfte_5fb2b747(int Fil, int varighed_VÆRDI) {
        if (varighed_VÆRDI < 52 || tal(Fil) != 0x464c457f || enhed_VÆRDI.기억읽기(Fil + 4) != 1
            || enhed_VÆRDI.기억읽기(Fil + 5) != 1 || enhed_VÆRDI.기억읽기(Fil + 6) != 1
            || 짧은수(Fil + 16) != 2 || 짧은수(Fil + 18) != 3 || tal(Fil + 20) != 1
            || 짧은수(Fil + 40) != 52 || 짧은수(Fil + 42) != 32) return -8;
        int indgangspunkt_VÆRDI = tal(Fil + 24);
        int tabel_placere = tal(Fil + 28);
        int vare_TÆL = 짧은수(Fil + 44);
        if (vare_TÆL == 0 || vare_TÆL > 16 || tabel_placere < 52 || tabel_placere > varighed_VÆRDI - vare_TÆL * 32) return -8;
        boolean it_eksekverbar_fil = false;
        for (int INDEKS = 0; INDEKS < vare_TÆL; INDEKS++) {
            int Opslag_tabel = Fil + tabel_placere + INDEKS * 32;
            int 종류 = tal(Opslag_tabel);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 Tilslut/parser_48ee4b1b 미지원
            if (종류 != 1) continue;
            int Placering = tal(Opslag_tabel + 4), mail = tal(Opslag_tabel + 8), filstørrelse = tal(Opslag_tabel + 16), Hukommelse_tilpasse_størrelse = tal(Opslag_tabel + 20);
            int justere_VÆRDI = tal(Opslag_tabel + 28);
            if (mail < START_bruger_app || mail >= Image_afslutte_et_opkald_mail || Hukommelse_tilpasse_størrelse < 0 || Hukommelse_tilpasse_størrelse > Image_afslutte_et_opkald_mail - mail
                || filstørrelse < 0 || filstørrelse > Hukommelse_tilpasse_størrelse || Placering < 0 || (filstørrelse > 0 && Placering > varighed_VÆRDI - filstørrelse)
                || (justere_VÆRDI != 0 && (justere_VÆRDI < 0 || (justere_VÆRDI & (justere_VÆRDI - 1)) != 0
                    || ((mail - Placering) & (justere_VÆRDI - 1)) != 0))) return -8;
            for (int frontvendt_VÆRDI = 0; frontvendt_VÆRDI < INDEKS; frontvendt_VÆRDI++) {
                int Forrige_vare = Fil + tabel_placere + frontvendt_VÆRDI * 32;
                if (tal(Forrige_vare) == 1 && Hukommelse_tilpasse_størrelse > 0 && tal(Forrige_vare + 20) > 0
                    && mail < tal(Forrige_vare + 8) + tal(Forrige_vare + 20) && tal(Forrige_vare + 8) < mail + Hukommelse_tilpasse_størrelse) return -8;
            }
            if ((tal(Opslag_tabel + 24) & 1) != 0 && indgangspunkt_VÆRDI >= mail && indgangspunkt_VÆRDI - mail < filstørrelse) it_eksekverbar_fil = true;
        }
        return it_eksekverbar_fil ? indgangspunkt_VÆRDI : -8;
    }

    static int Udfør_kommando(int[] input_VÆRDI, int Kør_2, int varighed_VÆRDI) {
        while (Kør_2 < varighed_VÆRDI && input_VÆRDI[Kør_2] == ' ') Kør_2++;
        int 끝 = Kør_2;
        while (끝 < varighed_VÆRDI && input_VÆRDI[끝] != ' ') 끝++;
        int post_VÆRDI_962f286b = Søg_post(input_VÆRDI, Kør_2, 끝 - Kør_2);
        if (post_VÆRDI_962f286b == 0) return -2;
        int Placering = tal(post_VÆRDI_962f286b + 16), Størrelse = tal(post_VÆRDI_962f286b + 20);
        if (Placering < 8 + gruppe_TÆL() * 24 || Størrelse < 52 || Placering > enhed_VÆRDI.eksekverbar_fil_bundt_tilpasse_størrelse() - Størrelse) return -8;
        int Fil = enhed_VÆRDI.eksekverbar_fil_bundt() + Placering;
        int indgangspunkt_VÆRDI = bekræfte_5fb2b747(Fil, Størrelse);
        if (indgangspunkt_VÆRDI < 0) return indgangspunkt_VÆRDI;
        enhed_VÆRDI.bruger_rydde_Indhold();
        int tabel_placere = tal(Fil + 28), vare_TÆL = 짧은수(Fil + 44);
        for (int INDEKS = 0; INDEKS < vare_TÆL; INDEKS++) {
            int Opslag_tabel = Fil + tabel_placere + INDEKS * 32;
            if (tal(Opslag_tabel) != 1) continue;
            int 원본 = Fil + tal(Opslag_tabel + 4), destination_VÆRDI = tal(Opslag_tabel + 8), filstørrelse = tal(Opslag_tabel + 16);
            for (int byte_VÆRDI = 0; byte_VÆRDI < filstørrelse; byte_VÆRDI++) enhed_VÆRDI.skrive_Hukommelse(destination_VÆRDI + byte_VÆRDI, enhed_VÆRDI.기억읽기(원본 + byte_VÆRDI));
        }
        argument_TÆL = 0;
        int Store_VÆRDI = argument_START;
        while (끝 < varighed_VÆRDI) {
            while (끝 < varighed_VÆRDI && input_VÆRDI[끝] == ' ') 끝++;
            if (끝 == varighed_VÆRDI) break;
            if (argument_TÆL == argument_mail.length) return -22;
            Kør_2 = 끝;
            while (끝 < varighed_VÆRDI && input_VÆRDI[끝] != ' ') 끝++;
            argument_mail[argument_TÆL++] = Store_VÆRDI;
            skrive_tal(Store_VÆRDI, 끝 - Kør_2);
            for (int tegn_VÆRDI = Kør_2; tegn_VÆRDI < 끝; tegn_VÆRDI++) skrive_tal(Store_VÆRDI + 4 + (tegn_VÆRDI - Kør_2) * 4, input_VÆRDI[tegn_VÆRDI]);
            Store_VÆRDI += 4 + (끝 - Kør_2) * 4;
        }
        netværk_Stak.Ren_Proces();
        파일서술자관리.START_Proces();
        int KR = enhed_VÆRDI.køre_bruger_app(indgangspunkt_VÆRDI, bruger_afslutte_et_opkald - 16);
        파일서술자관리.Ren_Proces();
        netværk_Stak.Ren_Proces();
        return KR;
    }
}
