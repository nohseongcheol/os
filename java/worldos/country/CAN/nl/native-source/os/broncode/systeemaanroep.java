// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 gebruikersruimte wijzer/길이는 toegang_invoer 전에 검사한다. */
public final class systeemaanroep {
    static int[] 임시자료 = new int[1024];

    static int MATRIX_tijdsduur(int ADRES) {
        if (!uitvoerbewerking_Manager.clip(ADRES, 4)) return -14;
        int tijdsduur_WAARDE = uitvoerbewerking_Manager.nummer(ADRES);
        if (tijdsduur_WAARDE < 0 || tijdsduur_WAARDE > (uitvoerbewerking_Manager.gebruiker_beëindigen - ADRES - 4) / 4) return -14;
        return tijdsduur_WAARDE;
    }

    public static int Proces_WAARDE_invoer(int INDEX, int 가, int SECONDE_operand, int 다, int 라, int 마) {
        if (INDEX == 30) return 파일서술자관리.open_Bestand(가, SECONDE_operand, 다);
        if (INDEX == 31) return 파일서술자관리.파일읽기(가, SECONDE_operand, 다);
        if (INDEX == 32) return 파일서술자관리.schrijven_Bestand(가, SECONDE_operand, 다);
        if (INDEX == 33) return 파일서술자관리.Sluiten_Bestand(가);
        if (INDEX == 34) return 파일서술자관리.zoeken_Bestand(가, SECONDE_operand, 다);
        if (INDEX == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (INDEX == 36) return 파일서술자관리.서술자복제(가, SECONDE_operand, true, 0);
        if (INDEX == 37) return 파일서술자관리.파일상태읽기(가, SECONDE_operand);
        if (INDEX == 38) return 파일서술자관리.verwijderen_Bestand_invoer_naam(가);
        if (INDEX == 39) return 파일서술자관리.set_Bestand_tijdsduur(가, SECONDE_operand);
        if (INDEX == 40) return 파일서술자관리.서술자제어(가, SECONDE_operand, 다);
        if (INDEX == 41) return 파일서술자관리.maken_eindpunt(가, SECONDE_operand, 다);
        if (INDEX == 42) return 파일서술자관리.BIND_ADRES(가, SECONDE_operand, 다);
        if (INDEX == 43) return 파일서술자관리.e_mailen_datagram_gegevens(가, SECONDE_operand, 다, 라, 마);
        if (INDEX == 44) return 파일서술자관리.ontvangen_datagram_gegevens(가, SECONDE_operand, 다, 라, 마);
        if (INDEX == 45) return 파일서술자관리.통신주소읽기(가, SECONDE_operand, 다);
        if (INDEX == 46) return 파일서술자관리.set_ontvangen_TIMEOUT(가, SECONDE_operand);
        if (INDEX == 47) {
            int 기술 = 파일서술자관리.기술찾기(가);
            if (기술 < 0) return -9;
            if (파일서술자관리.soort_WAARDE[기술] != 2) return -22;
            return 파일보존.synchroniseren();
        }
        if (INDEX == 1) {
            int tijdsduur_WAARDE = MATRIX_tijdsduur(가);
            if (tijdsduur_WAARDE < 0) return tijdsduur_WAARDE;
            if (tijdsduur_WAARDE > 4096) return -90;
            for (int teken_WAARDE = 0; teken_WAARDE < tijdsduur_WAARDE; teken_WAARDE++) sms_Terminal.문자(uitvoerbewerking_Manager.nummer(가 + 4 + teken_WAARDE * 4) & 65535);
            return tijdsduur_WAARDE;
        }
        if (INDEX == 2) return uitvoerbewerking_Manager.argument_AANTAL;
        if (INDEX == 3) return 가 >= 0 && 가 < uitvoerbewerking_Manager.argument_AANTAL ? uitvoerbewerking_Manager.argument_ADRES[가] : 0;
        if (INDEX == 10) return net_stack.Openen(가);
        if (INDEX == 11) {
            int tijdsduur_WAARDE = MATRIX_tijdsduur(라);
            if (tijdsduur_WAARDE < 0) return tijdsduur_WAARDE;
            if (마 < 0 || 마 > tijdsduur_WAARDE || 마 > 1024) return -90;
            for (int positie = 0; positie < 마; positie++) 임시자료[positie] = uitvoerbewerking_Manager.nummer(라 + 4 + positie * 4) & 255;
            return net_stack.e_mailen(가, SECONDE_operand, 다, 임시자료, 마);
        }
        if (INDEX == 12) {
            int tijdsduur_WAARDE = MATRIX_tijdsduur(SECONDE_operand);
            if (tijdsduur_WAARDE < 0) return tijdsduur_WAARDE;
            if (다 < 0 || 다 > 2000) return -22;
            int resultaat = net_stack.ontvangen(가, 임시자료, tijdsduur_WAARDE < 1024 ? tijdsduur_WAARDE : 1024, 다);
            if (resultaat >= 0) for (int positie = 0; positie < resultaat; positie++) uitvoerbewerking_Manager.schrijven_nummer(SECONDE_operand + 4 + positie * 4, 임시자료[positie]);
            return resultaat;
        }
        if (INDEX == 13) return net_stack.Sluiten(가);
        if (INDEX == 14) return net_stack.내주소;
        if (INDEX == 15) return net_stack.peer_ADRES(가);
        if (INDEX == 16) return net_stack.peer_poortnummer(가);
        if (INDEX == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            sms_Terminal.문자(가); return 1;
        }
        if (INDEX == 20 || INDEX == 21) {
            int naam_formaat_wijzigen = MATRIX_tijdsduur(가), gegevens_formaat_wijzigen = MATRIX_tijdsduur(SECONDE_operand);
            if (naam_formaat_wijzigen < 0 || gegevens_formaat_wijzigen < 0) return -14;
            if (naam_formaat_wijzigen < 1 || naam_formaat_wijzigen > 64) return -22;
            int tijdsduur_WAARDE = 0;
            while (tijdsduur_WAARDE < naam_formaat_wijzigen && uitvoerbewerking_Manager.nummer(가 + 4 + tijdsduur_WAARDE * 4) != 0) {
                Geheugen_bestandssysteem.Naam[tijdsduur_WAARDE] = uitvoerbewerking_Manager.nummer(가 + 4 + tijdsduur_WAARDE * 4);
                tijdsduur_WAARDE++;
            }
            if (!Geheugen_bestandssysteem.cheque_naam(Geheugen_bestandssysteem.Naam, tijdsduur_WAARDE)) return -22;
            if (INDEX == 20) {
                int bestand = Geheugen_bestandssysteem.Zoeken_invoer(Geheugen_bestandssysteem.Naam, tijdsduur_WAARDE);
                if (bestand < 0) return bestand;
                int Grootte = Geheugen_bestandssysteem.formaat_wijzigen_Lijst[bestand];
                if (Grootte > gegevens_formaat_wijzigen) return -90;
                int ADRES = mobiel_WAARDE.Bestand_Geheugen() + bestand * Geheugen_bestandssysteem.최대크기;
                for (int nummer = 0; nummer < Grootte; nummer++) uitvoerbewerking_Manager.schrijven_nummer(SECONDE_operand + 4 + nummer * 4, mobiel_WAARDE.기억읽기(ADRES + nummer));
                return Grootte;
            }
            if (다 < 0 || 다 > gegevens_formaat_wijzigen) return -22;
            if (다 > Geheugen_bestandssysteem.최대크기) return -90;
            for (int nummer = 0; nummer < 다; nummer++) Geheugen_bestandssysteem.Bewerk_WAARDE[nummer] = uitvoerbewerking_Manager.nummer(SECONDE_operand + 4 + nummer * 4) & 255;
            return Geheugen_bestandssysteem.Store_WAARDE(Geheugen_bestandssysteem.Naam, tijdsduur_WAARDE, Geheugen_bestandssysteem.Bewerk_WAARDE, 다);
        }
        return -38;
    }
}
