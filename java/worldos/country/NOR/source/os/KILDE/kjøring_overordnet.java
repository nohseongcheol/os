// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Les 전용 Utfør_kommando 묶음의 ELF32 bekrefte_5fb2b747, Argumenter Frem_VERDI, 한 번에 한 bruker Prosess_VERDI Utfør_kommando. */
public final class kjøring_overordnet {
    static final int START_bruker_app = 0x04000000;
    static final int bruker_avslutte_en_samtale = 0x04400000;
    static final int BILDE_avslutte_en_samtale_e_post = 0x04200000;
    static final int argument_START = 0x04300000;
    static int argument_ANTALL = 0;
    static int[] argument_e_post = new int[16];

    static boolean klippe(int e_post, int lengde_VERDI) {
        return e_post >= START_bruker_app && e_post < bruker_avslutte_en_samtale && lengde_VERDI >= 0 && lengde_VERDI <= bruker_avslutte_en_samtale - e_post;
    }

    static int nummer(int e_post) { return Minne_område.dele_opp_heltall(e_post); }
    static int 짧은수(int e_post) { return enhet_VERDI.기억읽기(e_post) | enhet_VERDI.기억읽기(e_post + 1) << 8; }
    static void skrive_nummer(int e_post, int VERDI) {
        for (int INDEKS = 0; INDEKS < 4; INDEKS++) enhet_VERDI.skrive_Minne(e_post + INDEKS, VERDI >>> (INDEKS * 8));
    }

    static int gruppe_ANTALL() {
        int e_post = enhet_VERDI.kjørbar_fil_bunt();
        int Størrelse = enhet_VERDI.kjørbar_fil_bunt_skalere();
        if (Størrelse < 8 || nummer(e_post) != 0x50414b4a) return 0;
        int vare_ANTALL = nummer(e_post + 4);
        return vare_ANTALL >= 0 && vare_ANTALL <= 32 && vare_ANTALL <= (Størrelse - 8) / 24 ? vare_ANTALL : 0;
    }

    static void oppføring_Liste() {
        for (int INDEKS = 0; INDEKS < gruppe_ANTALL(); INDEKS++) {
            int oppføring_VERDI = enhet_VERDI.kjørbar_fil_bunt() + 8 + INDEKS * 24;
            for (int tegn_VERDI = 0; tegn_VERDI < 16 && enhet_VERDI.기억읽기(oppføring_VERDI + tegn_VERDI) != 0; tegn_VERDI++)
                SMS_Terminal.문자(enhet_VERDI.기억읽기(oppføring_VERDI + tegn_VERDI));
            SMS_Terminal.Skriv("\n");
        }
    }

    static int Søk_oppføring(int[] inndata_VERDI, int Kjør_2, int lengde_VERDI) {
        if (lengde_VERDI <= 0 || lengde_VERDI >= 16) return 0;
        for (int INDEKS = 0; INDEKS < gruppe_ANTALL(); INDEKS++) {
            int oppføring_VERDI = enhet_VERDI.kjørbar_fil_bunt() + 8 + INDEKS * 24;
            boolean 같음 = enhet_VERDI.기억읽기(oppføring_VERDI + lengde_VERDI) == 0;
            for (int tegn_VERDI = 0; tegn_VERDI < lengde_VERDI; tegn_VERDI++)
                if (inndata_VERDI[Kjør_2 + tegn_VERDI] != enhet_VERDI.기억읽기(oppføring_VERDI + tegn_VERDI)) 같음 = false;
            if (같음) return oppføring_VERDI;
        }
        return 0;
    }

    static int bekrefte_5fb2b747(int Fil, int lengde_VERDI) {
        if (lengde_VERDI < 52 || nummer(Fil) != 0x464c457f || enhet_VERDI.기억읽기(Fil + 4) != 1
            || enhet_VERDI.기억읽기(Fil + 5) != 1 || enhet_VERDI.기억읽기(Fil + 6) != 1
            || 짧은수(Fil + 16) != 2 || 짧은수(Fil + 18) != 3 || nummer(Fil + 20) != 1
            || 짧은수(Fil + 40) != 52 || 짧은수(Fil + 42) != 32) return -8;
        int inngangspunkt_VERDI = nummer(Fil + 24);
        int tabell_plassere = nummer(Fil + 28);
        int vare_ANTALL = 짧은수(Fil + 44);
        if (vare_ANTALL == 0 || vare_ANTALL > 16 || tabell_plassere < 52 || tabell_plassere > lengde_VERDI - vare_ANTALL * 32) return -8;
        boolean informasjonssystemer_kjørbar_fil = false;
        for (int INDEKS = 0; INDEKS < vare_ANTALL; INDEKS++) {
            int oppslagstabell = Fil + tabell_plassere + INDEKS * 32;
            int 종류 = nummer(oppslagstabell);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 Koble_til/parser_48ee4b1b 미지원
            if (종류 != 1) continue;
            int Posisjon = nummer(oppslagstabell + 4), e_post = nummer(oppslagstabell + 8), filstørrelse = nummer(oppslagstabell + 16), Minne_skalere = nummer(oppslagstabell + 20);
            int justere_VERDI = nummer(oppslagstabell + 28);
            if (e_post < START_bruker_app || e_post >= BILDE_avslutte_en_samtale_e_post || Minne_skalere < 0 || Minne_skalere > BILDE_avslutte_en_samtale_e_post - e_post
                || filstørrelse < 0 || filstørrelse > Minne_skalere || Posisjon < 0 || (filstørrelse > 0 && Posisjon > lengde_VERDI - filstørrelse)
                || (justere_VERDI != 0 && (justere_VERDI < 0 || (justere_VERDI & (justere_VERDI - 1)) != 0
                    || ((e_post - Posisjon) & (justere_VERDI - 1)) != 0))) return -8;
            for (int frontkamera_VERDI = 0; frontkamera_VERDI < INDEKS; frontkamera_VERDI++) {
                int Forrige_vare = Fil + tabell_plassere + frontkamera_VERDI * 32;
                if (nummer(Forrige_vare) == 1 && Minne_skalere > 0 && nummer(Forrige_vare + 20) > 0
                    && e_post < nummer(Forrige_vare + 8) + nummer(Forrige_vare + 20) && nummer(Forrige_vare + 8) < e_post + Minne_skalere) return -8;
            }
            if ((nummer(oppslagstabell + 24) & 1) != 0 && inngangspunkt_VERDI >= e_post && inngangspunkt_VERDI - e_post < filstørrelse) informasjonssystemer_kjørbar_fil = true;
        }
        return informasjonssystemer_kjørbar_fil ? inngangspunkt_VERDI : -8;
    }

    static int Utfør_kommando(int[] inndata_VERDI, int Kjør_2, int lengde_VERDI) {
        while (Kjør_2 < lengde_VERDI && inndata_VERDI[Kjør_2] == ' ') Kjør_2++;
        int 끝 = Kjør_2;
        while (끝 < lengde_VERDI && inndata_VERDI[끝] != ' ') 끝++;
        int oppføring_VERDI = Søk_oppføring(inndata_VERDI, Kjør_2, 끝 - Kjør_2);
        if (oppføring_VERDI == 0) return -2;
        int Posisjon = nummer(oppføring_VERDI + 16), Størrelse = nummer(oppføring_VERDI + 20);
        if (Posisjon < 8 + gruppe_ANTALL() * 24 || Størrelse < 52 || Posisjon > enhet_VERDI.kjørbar_fil_bunt_skalere() - Størrelse) return -8;
        int Fil = enhet_VERDI.kjørbar_fil_bunt() + Posisjon;
        int inngangspunkt_VERDI = bekrefte_5fb2b747(Fil, Størrelse);
        if (inngangspunkt_VERDI < 0) return inngangspunkt_VERDI;
        enhet_VERDI.bruker_tømme_Innhold();
        int tabell_plassere = nummer(Fil + 28), vare_ANTALL = 짧은수(Fil + 44);
        for (int INDEKS = 0; INDEKS < vare_ANTALL; INDEKS++) {
            int oppslagstabell = Fil + tabell_plassere + INDEKS * 32;
            if (nummer(oppslagstabell) != 1) continue;
            int 원본 = Fil + nummer(oppslagstabell + 4), mål_VERDI = nummer(oppslagstabell + 8), filstørrelse = nummer(oppslagstabell + 16);
            for (int byte_VERDI = 0; byte_VERDI < filstørrelse; byte_VERDI++) enhet_VERDI.skrive_Minne(mål_VERDI + byte_VERDI, enhet_VERDI.기억읽기(원본 + byte_VERDI));
        }
        argument_ANTALL = 0;
        int Store_VERDI = argument_START;
        while (끝 < lengde_VERDI) {
            while (끝 < lengde_VERDI && inndata_VERDI[끝] == ' ') 끝++;
            if (끝 == lengde_VERDI) break;
            if (argument_ANTALL == argument_e_post.length) return -22;
            Kjør_2 = 끝;
            while (끝 < lengde_VERDI && inndata_VERDI[끝] != ' ') 끝++;
            argument_e_post[argument_ANTALL++] = Store_VERDI;
            skrive_nummer(Store_VERDI, 끝 - Kjør_2);
            for (int tegn_VERDI = Kjør_2; tegn_VERDI < 끝; tegn_VERDI++) skrive_nummer(Store_VERDI + 4 + (tegn_VERDI - Kjør_2) * 4, inndata_VERDI[tegn_VERDI]);
            Store_VERDI += 4 + (끝 - Kjør_2) * 4;
        }
        nettverk_stakk.RENSK_Prosess();
        파일서술자관리.START_Prosess();
        int KR = enhet_VERDI.kjøre_bruker_app(inngangspunkt_VERDI, bruker_avslutte_en_samtale - 16);
        파일서술자관리.RENSK_Prosess();
        nettverk_stakk.RENSK_Prosess();
        return KR;
    }
}
