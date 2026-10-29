// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Lezen 전용 Uitvoeren_opdracht 묶음의 ELF32 valideren, argumenten Vooruit_WAARDE, 한 번에 한 gebruikersruimte Proces_WAARDE Uitvoeren_opdracht. */
public final class uitvoerbewerking_Manager {
    static final int START_gebruiker_app = 0x04000000;
    static final int gebruiker_beëindigen = 0x04400000;
    static final int kopie_eindadres = 0x04200000;
    static final int argument_START = 0x04300000;
    static int argument_AANTAL = 0;
    static int[] argument_ADRES = new int[16];

    static boolean clip(int ADRES, int tijdsduur_WAARDE) {
        return ADRES >= START_gebruiker_app && ADRES < gebruiker_beëindigen && tijdsduur_WAARDE >= 0 && tijdsduur_WAARDE <= gebruiker_beëindigen - ADRES;
    }

    static int nummer(int ADRES) { return Geheugen_regio.parseren_geheel_getal(ADRES); }
    static int 짧은수(int ADRES) { return mobiel_WAARDE.기억읽기(ADRES) | mobiel_WAARDE.기억읽기(ADRES + 1) << 8; }
    static void schrijven_nummer(int ADRES, int WAARDE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) mobiel_WAARDE.schrijven_Geheugen(ADRES + INDEX, WAARDE >>> (INDEX * 8));
    }

    static int Groep_AANTAL() {
        int ADRES = mobiel_WAARDE.uitvoerbaar_bundel();
        int Grootte = mobiel_WAARDE.uitvoerbaar_bundel_formaat_wijzigen();
        if (Grootte < 8 || nummer(ADRES) != 0x50414b4a) return 0;
        int item_AANTAL = nummer(ADRES + 4);
        return item_AANTAL >= 0 && item_AANTAL <= 32 && item_AANTAL <= (Grootte - 8) / 24 ? item_AANTAL : 0;
    }

    static void invoer_Lijst_f07b3200() {
        for (int INDEX = 0; INDEX < Groep_AANTAL(); INDEX++) {
            int invoer_WAARDE_962f286b = mobiel_WAARDE.uitvoerbaar_bundel() + 8 + INDEX * 24;
            for (int teken_WAARDE = 0; teken_WAARDE < 16 && mobiel_WAARDE.기억읽기(invoer_WAARDE_962f286b + teken_WAARDE) != 0; teken_WAARDE++)
                sms_Terminal.문자(mobiel_WAARDE.기억읽기(invoer_WAARDE_962f286b + teken_WAARDE));
            sms_Terminal.Schrijven("\n");
        }
    }

    static int Zoeken_invoer(int[] invoer_WAARDE, int starten, int tijdsduur_WAARDE) {
        if (tijdsduur_WAARDE <= 0 || tijdsduur_WAARDE >= 16) return 0;
        for (int INDEX = 0; INDEX < Groep_AANTAL(); INDEX++) {
            int invoer_WAARDE_962f286b = mobiel_WAARDE.uitvoerbaar_bundel() + 8 + INDEX * 24;
            boolean 같음 = mobiel_WAARDE.기억읽기(invoer_WAARDE_962f286b + tijdsduur_WAARDE) == 0;
            for (int teken_WAARDE = 0; teken_WAARDE < tijdsduur_WAARDE; teken_WAARDE++)
                if (invoer_WAARDE[starten + teken_WAARDE] != mobiel_WAARDE.기억읽기(invoer_WAARDE_962f286b + teken_WAARDE)) 같음 = false;
            if (같음) return invoer_WAARDE_962f286b;
        }
        return 0;
    }

    static int valideren(int bestand, int tijdsduur_WAARDE) {
        if (tijdsduur_WAARDE < 52 || nummer(bestand) != 0x464c457f || mobiel_WAARDE.기억읽기(bestand + 4) != 1
            || mobiel_WAARDE.기억읽기(bestand + 5) != 1 || mobiel_WAARDE.기억읽기(bestand + 6) != 1
            || 짧은수(bestand + 16) != 2 || 짧은수(bestand + 18) != 3 || nummer(bestand + 20) != 1
            || 짧은수(bestand + 40) != 52 || 짧은수(bestand + 42) != 32) return -8;
        int beginpunt_WAARDE = nummer(bestand + 24);
        int tabel_functie = nummer(bestand + 28);
        int item_AANTAL = 짧은수(bestand + 44);
        if (item_AANTAL == 0 || item_AANTAL > 16 || tabel_functie < 52 || tabel_functie > tijdsduur_WAARDE - item_AANTAL * 32) return -8;
        boolean informatie_uitvoerbaar = false;
        for (int INDEX = 0; INDEX < item_AANTAL; INDEX++) {
            int opzoektabel = bestand + tabel_functie + INDEX * 32;
            int soort_WAARDE = nummer(opzoektabel);
            if (soort_WAARDE == 2 || soort_WAARDE == 3) return -8; // 동적 Verbinden/parser_48ee4b1b 미지원
            if (soort_WAARDE != 1) continue;
            int positie = nummer(opzoektabel + 4), ADRES = nummer(opzoektabel + 8), bestandsgrootte = nummer(opzoektabel + 16), Geheugen_formaat_wijzigen = nummer(opzoektabel + 20);
            int uitlijnen_WAARDE = nummer(opzoektabel + 28);
            if (ADRES < START_gebruiker_app || ADRES >= kopie_eindadres || Geheugen_formaat_wijzigen < 0 || Geheugen_formaat_wijzigen > kopie_eindadres - ADRES
                || bestandsgrootte < 0 || bestandsgrootte > Geheugen_formaat_wijzigen || positie < 0 || (bestandsgrootte > 0 && positie > tijdsduur_WAARDE - bestandsgrootte)
                || (uitlijnen_WAARDE != 0 && (uitlijnen_WAARDE < 0 || (uitlijnen_WAARDE & (uitlijnen_WAARDE - 1)) != 0
                    || ((ADRES - positie) & (uitlijnen_WAARDE - 1)) != 0))) return -8;
            for (int voorkant_WAARDE = 0; voorkant_WAARDE < INDEX; voorkant_WAARDE++) {
                int Vorige_item = bestand + tabel_functie + voorkant_WAARDE * 32;
                if (nummer(Vorige_item) == 1 && Geheugen_formaat_wijzigen > 0 && nummer(Vorige_item + 20) > 0
                    && ADRES < nummer(Vorige_item + 8) + nummer(Vorige_item + 20) && nummer(Vorige_item + 8) < ADRES + Geheugen_formaat_wijzigen) return -8;
            }
            if ((nummer(opzoektabel + 24) & 1) != 0 && beginpunt_WAARDE >= ADRES && beginpunt_WAARDE - ADRES < bestandsgrootte) informatie_uitvoerbaar = true;
        }
        return informatie_uitvoerbaar ? beginpunt_WAARDE : -8;
    }

    static int Uitvoeren_opdracht(int[] invoer_WAARDE, int starten, int tijdsduur_WAARDE) {
        while (starten < tijdsduur_WAARDE && invoer_WAARDE[starten] == ' ') starten++;
        int 끝 = starten;
        while (끝 < tijdsduur_WAARDE && invoer_WAARDE[끝] != ' ') 끝++;
        int invoer_WAARDE_962f286b = Zoeken_invoer(invoer_WAARDE, starten, 끝 - starten);
        if (invoer_WAARDE_962f286b == 0) return -2;
        int positie = nummer(invoer_WAARDE_962f286b + 16), Grootte = nummer(invoer_WAARDE_962f286b + 20);
        if (positie < 8 + Groep_AANTAL() * 24 || Grootte < 52 || positie > mobiel_WAARDE.uitvoerbaar_bundel_formaat_wijzigen() - Grootte) return -8;
        int bestand = mobiel_WAARDE.uitvoerbaar_bundel() + positie;
        int beginpunt_WAARDE = valideren(bestand, Grootte);
        if (beginpunt_WAARDE < 0) return beginpunt_WAARDE;
        mobiel_WAARDE.gebruiker_wissen_Inhoud();
        int tabel_functie = nummer(bestand + 28), item_AANTAL = 짧은수(bestand + 44);
        for (int INDEX = 0; INDEX < item_AANTAL; INDEX++) {
            int opzoektabel = bestand + tabel_functie + INDEX * 32;
            if (nummer(opzoektabel) != 1) continue;
            int 원본 = bestand + nummer(opzoektabel + 4), doel_WAARDE = nummer(opzoektabel + 8), bestandsgrootte = nummer(opzoektabel + 16);
            for (int byte_WAARDE = 0; byte_WAARDE < bestandsgrootte; byte_WAARDE++) mobiel_WAARDE.schrijven_Geheugen(doel_WAARDE + byte_WAARDE, mobiel_WAARDE.기억읽기(원본 + byte_WAARDE));
        }
        argument_AANTAL = 0;
        int Store_WAARDE = argument_START;
        while (끝 < tijdsduur_WAARDE) {
            while (끝 < tijdsduur_WAARDE && invoer_WAARDE[끝] == ' ') 끝++;
            if (끝 == tijdsduur_WAARDE) break;
            if (argument_AANTAL == argument_ADRES.length) return -22;
            starten = 끝;
            while (끝 < tijdsduur_WAARDE && invoer_WAARDE[끝] != ' ') 끝++;
            argument_ADRES[argument_AANTAL++] = Store_WAARDE;
            schrijven_nummer(Store_WAARDE, 끝 - starten);
            for (int teken_WAARDE = starten; teken_WAARDE < 끝; teken_WAARDE++) schrijven_nummer(Store_WAARDE + 4 + (teken_WAARDE - starten) * 4, invoer_WAARDE[teken_WAARDE]);
            Store_WAARDE += 4 + (끝 - starten) * 4;
        }
        net_stack.Verscherpt_Proces();
        파일서술자관리.START_Proces();
        int resultaat = mobiel_WAARDE.uitvoeren_gebruiker_app(beginpunt_WAARDE, gebruiker_beëindigen - 16);
        파일서술자관리.Verscherpt_Proces();
        net_stack.Verscherpt_Proces();
        return resultaat;
    }
}
