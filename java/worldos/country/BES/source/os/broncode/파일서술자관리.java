// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 gebruikersruimte 과정의 파일서술자와 열린 bestand 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int lezen_schrijven_vlag = 2, maken_invoer = 64, 독점생성 = 128, wissen_Inhoud = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] open_greep = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] soort_WAARDE = new int[서술자한도], doel = new int[서술자한도];
    static int[] Bestand_functie = new int[서술자한도], open_Instellingen = new int[서술자한도], verwijzen_AANTAL = new int[서술자한도];
    static int[] net_greep = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] pad_naam = new int[64], transfer_gegevens = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return open_greep[파일서술자] - 1;
    }
    static int 빈서술자(int starten) {
        for (int INDEX = starten; INDEX < 서술자한도; INDEX++) if (open_greep[INDEX] == 0) return INDEX;
        return -24;
    }
    static int leeg_greep() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (verwijzen_AANTAL[INDEX] == 0) return INDEX;
        return -24;
    }
    static int Verbinden(int 서술자, int 기술, int Bestand_soort, int Bestand_doel, int Instellingen) {
        open_greep[서술자] = 기술 + 1; 서술자설정[서술자] = (Instellingen & 실행시닫기) != 0 ? 1 : 0;
        soort_WAARDE[기술] = Bestand_soort; doel[기술] = Bestand_doel; verwijzen_AANTAL[기술] = 1;
        open_Instellingen[기술] = Instellingen & (3 | 이어쓰기 | 기다리지않기); Bestand_functie[기술] = 0;
        net_greep[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void START_Proces() {
        Verscherpt_Proces();
        for (int INDEX = 0; INDEX < 3; INDEX++) Verbinden(INDEX, INDEX, 1, INDEX, INDEX == 0 ? 0 : 1);
    }
    static void Verscherpt_Proces() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (open_greep[INDEX] != 0) Sluiten_Bestand(INDEX);
    }
    static int Sluiten_Bestand(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        open_greep[서술자] = 0; 서술자설정[서술자] = 0;
        verwijzen_AANTAL[기술]--;
        if (verwijzen_AANTAL[기술] == 0) {
            if (soort_WAARDE[기술] == 2) Geheugen_bestandssysteem.open_AANTAL[doel[기술]]--;
            if (soort_WAARDE[기술] == 3 && net_greep[기술] != 0) net_stack.Sluiten(net_greep[기술]);
            soort_WAARDE[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 byte_WAARDE 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int ADRES) {
        if (!uitvoerbewerking_Manager.clip(ADRES, 1)) return -14;
        int positie = mobiel_WAARDE.기억읽기(ADRES) == '/' ? 1 : 0;
        for (int tijdsduur_WAARDE = 0; tijdsduur_WAARDE < 64; tijdsduur_WAARDE++) {
            if (!uitvoerbewerking_Manager.clip(ADRES + positie + tijdsduur_WAARDE, 1)) return -14;
            int WAARDE = mobiel_WAARDE.기억읽기(ADRES + positie + tijdsduur_WAARDE);
            pad_naam[tijdsduur_WAARDE] = WAARDE;
            if (WAARDE == 0) return tijdsduur_WAARDE == 0 ? -2 : (Geheugen_bestandssysteem.cheque_naam(pad_naam, tijdsduur_WAARDE) ? tijdsduur_WAARDE : -22);
            if (WAARDE == '/') return -20;
        }
        return -36;
    }
    static int open_Bestand(int naam_ADRES, int Instellingen, int toekenning_machtiging) {
        int tijdsduur_WAARDE = 경로읽기(naam_ADRES);
        if (tijdsduur_WAARDE < 0) return tijdsduur_WAARDE;
        if ((Instellingen & ~(3 | maken_invoer | 독점생성 | wissen_Inhoud | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Instellingen & 3) == 3 || ((Instellingen & wissen_Inhoud) != 0 && (Instellingen & 3) == 0)) return -22;
        int bestand = Geheugen_bestandssysteem.Zoeken_invoer(pad_naam, tijdsduur_WAARDE);
        if (bestand >= 0 && (Instellingen & (maken_invoer | 독점생성)) == (maken_invoer | 독점생성)) return -17;
        if (bestand == -2 && (Instellingen & maken_invoer) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = leeg_greep();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (bestand == -2) {
            int resultaat = Geheugen_bestandssysteem.Store_WAARDE(pad_naam, tijdsduur_WAARDE, pad_naam, 0);
            if (resultaat < 0) return resultaat;
            bestand = Geheugen_bestandssysteem.Zoeken_invoer(pad_naam, tijdsduur_WAARDE);
            Geheugen_bestandssysteem.허가들[bestand] = toekenning_machtiging & 511;
        }
        if (bestand < 0) return bestand;
        if ((Instellingen & wissen_Inhoud) != 0) Geheugen_bestandssysteem.formaat_wijzigen_Lijst[bestand] = 0;
        Geheugen_bestandssysteem.open_AANTAL[bestand]++;
        return Verbinden(서술자, 기술, 2, bestand, Instellingen);
    }
    static int 파일읽기(int 서술자, int gegevens_ADRES, int tijdsduur_WAARDE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (open_Instellingen[기술] & 3) == 1) return -9;
        if (tijdsduur_WAARDE < 0) return -22;
        if (tijdsduur_WAARDE == 0) return 0;
        if (!uitvoerbewerking_Manager.clip(gegevens_ADRES, tijdsduur_WAARDE)) return -14;
        if (soort_WAARDE[기술] == 3) return ontvangen_datagram_gegevens(서술자, gegevens_ADRES, tijdsduur_WAARDE, 0, 0);
        if (soort_WAARDE[기술] == 1) {
            int OPBRENGST_AANTAL = 0;
            while (OPBRENGST_AANTAL < tijdsduur_WAARDE) {
                int WAARDE = sms_Terminal.직렬읽기();
                if (WAARDE < 0) WAARDE = toetsenbord.Lezen();
                if (WAARDE < 0) {
                    if (OPBRENGST_AANTAL > 0) return OPBRENGST_AANTAL;
                    if ((open_Instellingen[기술] & 기다리지않기) != 0) return -11;
                    if (mobiel_WAARDE.사용자남은밀리초() <= 10) return -11;
                    net_stack.bevestigen(); mobiel_WAARDE.잠시양보();
                } else {
                    mobiel_WAARDE.schrijven_Geheugen(gegevens_ADRES + OPBRENGST_AANTAL, WAARDE); OPBRENGST_AANTAL++;
                }
            }
            return OPBRENGST_AANTAL;
        }
        int bestand = doel[기술], positie = Bestand_functie[기술];
        if (positie >= Geheugen_bestandssysteem.formaat_wijzigen_Lijst[bestand]) return 0;
        if (tijdsduur_WAARDE > Geheugen_bestandssysteem.formaat_wijzigen_Lijst[bestand] - positie) tijdsduur_WAARDE = Geheugen_bestandssysteem.formaat_wijzigen_Lijst[bestand] - positie;
        int 원본주소 = mobiel_WAARDE.Bestand_Geheugen() + bestand * Geheugen_bestandssysteem.최대크기 + positie;
        for (int INDEX = 0; INDEX < tijdsduur_WAARDE; INDEX++) mobiel_WAARDE.schrijven_Geheugen(gegevens_ADRES + INDEX, mobiel_WAARDE.기억읽기(원본주소 + INDEX));
        Bestand_functie[기술] += tijdsduur_WAARDE;
        return tijdsduur_WAARDE;
    }
    static int schrijven_Bestand(int 서술자, int gegevens_ADRES, int tijdsduur_WAARDE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (open_Instellingen[기술] & 3) == 0) return -9;
        if (tijdsduur_WAARDE < 0) return -22;
        if (tijdsduur_WAARDE == 0) return 0;
        if (!uitvoerbewerking_Manager.clip(gegevens_ADRES, tijdsduur_WAARDE)) return -14;
        if (soort_WAARDE[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 doel_WAARDE 주소가 필요하다.
        if (soort_WAARDE[기술] == 1) {
            if (tijdsduur_WAARDE > 16384) tijdsduur_WAARDE = 16384;
            for (int INDEX = 0; INDEX < tijdsduur_WAARDE; INDEX++) {
                int WAARDE = mobiel_WAARDE.기억읽기(gegevens_ADRES + INDEX);
                sms_Terminal.직렬바이트(WAARDE); sms_Terminal.scherm_teken(WAARDE);
            }
            return tijdsduur_WAARDE;
        }
        int bestand = doel[기술], Grootte = Geheugen_bestandssysteem.formaat_wijzigen_Lijst[bestand];
        int positie = (open_Instellingen[기술] & 이어쓰기) != 0 ? Grootte : Bestand_functie[기술];
        if (positie >= Geheugen_bestandssysteem.최대크기) return -27;
        if (tijdsduur_WAARDE > Geheugen_bestandssysteem.최대크기 - positie) tijdsduur_WAARDE = Geheugen_bestandssysteem.최대크기 - positie;
        int doel_ADRES_08bbd577 = mobiel_WAARDE.Bestand_Geheugen() + bestand * Geheugen_bestandssysteem.최대크기;
        for (int INDEX = Grootte; INDEX < positie; INDEX++) mobiel_WAARDE.schrijven_Geheugen(doel_ADRES_08bbd577 + INDEX, 0);
        for (int INDEX = 0; INDEX < tijdsduur_WAARDE; INDEX++) mobiel_WAARDE.schrijven_Geheugen(doel_ADRES_08bbd577 + positie + INDEX, mobiel_WAARDE.기억읽기(gegevens_ADRES + INDEX));
        Bestand_functie[기술] = positie + tijdsduur_WAARDE;
        if (positie + tijdsduur_WAARDE > Grootte) Geheugen_bestandssysteem.formaat_wijzigen_Lijst[bestand] = positie + tijdsduur_WAARDE;
        return tijdsduur_WAARDE;
    }
    static int zoeken_Bestand(int 서술자, int VERSCHUIVING_WAARDE, int Taken_wortel) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (soort_WAARDE[기술] != 2) return -29;
        if (Taken_wortel < 0 || Taken_wortel > 2) return -22;
        int Achtergrond_WAARDE = Taken_wortel == 0 ? 0 : (Taken_wortel == 1 ? Bestand_functie[기술] : Geheugen_bestandssysteem.formaat_wijzigen_Lijst[doel[기술]]);
        if (VERSCHUIVING_WAARDE > 0 && Achtergrond_WAARDE > 2147483647 - VERSCHUIVING_WAARDE) return -75;
        if (VERSCHUIVING_WAARDE < 0 && VERSCHUIVING_WAARDE < -Achtergrond_WAARDE) return -22;
        Bestand_functie[기술] = Achtergrond_WAARDE + VERSCHUIVING_WAARDE;
        return Bestand_functie[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean Toewijzen_WAARDE, int Instellingen) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return Toewijzen_WAARDE ? -9 : -22;
        if (Toewijzen_WAARDE && 서술자 == 새서술자) return 새서술자;
        if (Toewijzen_WAARDE) { if (open_greep[새서술자] != 0) Sluiten_Bestand(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        open_greep[새서술자] = 기술 + 1; 서술자설정[새서술자] = Instellingen; verwijzen_AANTAL[기술]++;
        return 새서술자;
    }
    static int verwijderen_Bestand_invoer_naam(int naam_ADRES) {
        int tijdsduur_WAARDE = 경로읽기(naam_ADRES);
        if (tijdsduur_WAARDE < 0) return tijdsduur_WAARDE;
        int bestand = Geheugen_bestandssysteem.Zoeken_invoer(pad_naam, tijdsduur_WAARDE);
        if (bestand < 0) return bestand;
        Geheugen_bestandssysteem.이름들[bestand * 64] = 0;
        return 0;
    }
    static int set_Bestand_tijdsduur(int 서술자, int tijdsduur_WAARDE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (soort_WAARDE[기술] != 2 || (open_Instellingen[기술] & 3) == 0 || tijdsduur_WAARDE < 0) return -22;
        if (tijdsduur_WAARDE > Geheugen_bestandssysteem.최대크기) return -27;
        int bestand = doel[기술], ADRES = mobiel_WAARDE.Bestand_Geheugen() + bestand * Geheugen_bestandssysteem.최대크기;
        for (int INDEX = Geheugen_bestandssysteem.formaat_wijzigen_Lijst[bestand]; INDEX < tijdsduur_WAARDE; INDEX++) mobiel_WAARDE.schrijven_Geheugen(ADRES + INDEX, 0);
        Geheugen_bestandssysteem.formaat_wijzigen_Lijst[bestand] = tijdsduur_WAARDE;
        return 0;
    }
    static int 파일상태읽기(int 서술자, int ADRES) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!uitvoerbewerking_Manager.clip(ADRES, 48)) return -14;
        for (int INDEX = 0; INDEX < 12; INDEX++) uitvoerbewerking_Manager.schrijven_nummer(ADRES + INDEX * 4, 0);
        int bestand = doel[기술], Grootte = soort_WAARDE[기술] == 2 ? Geheugen_bestandssysteem.formaat_wijzigen_Lijst[bestand] : 0;
        int toekenning_machtiging = soort_WAARDE[기술] == 2 ? Geheugen_bestandssysteem.허가들[bestand] : 438;
        uitvoerbewerking_Manager.schrijven_nummer(ADRES, 1);
        uitvoerbewerking_Manager.schrijven_nummer(ADRES + 4, soort_WAARDE[기술] == 2 ? bestand + 1 : 100 + 기술);
        uitvoerbewerking_Manager.schrijven_nummer(ADRES + 8, (soort_WAARDE[기술] == 2 ? 32768 : (soort_WAARDE[기술] == 1 ? 8192 : 49152)) | toekenning_machtiging);
        uitvoerbewerking_Manager.schrijven_nummer(ADRES + 12, soort_WAARDE[기술] == 2 && Geheugen_bestandssysteem.이름들[bestand * 64] == 0 ? 0 : 1);
        uitvoerbewerking_Manager.schrijven_nummer(ADRES + 28, Grootte); uitvoerbewerking_Manager.schrijven_nummer(ADRES + 32, 512);
        uitvoerbewerking_Manager.schrijven_nummer(ADRES + 36, (Grootte + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int opdracht, int WAARDE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (opdracht == 0 || opdracht == 1030) return 서술자복제(서술자, WAARDE, false, opdracht == 1030 ? 1 : 0);
        if (opdracht == 1) return 서술자설정[서술자];
        if (opdracht == 2) { if ((WAARDE & ~1) != 0) return -22; 서술자설정[서술자] = WAARDE; return 0; }
        if (opdracht == 3) return open_Instellingen[기술];
        if (opdracht == 4) {
            if ((WAARDE & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            open_Instellingen[기술] = (open_Instellingen[기술] & 3) | (WAARDE & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int maken_eindpunt(int 주소체계, int net_soort, int taak_nummer) {
        if (주소체계 != 2) return -97;
        if (net_soort != 2) return -93;
        if (taak_nummer != 0 && taak_nummer != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = leeg_greep();
        if (서술자 < 0 || 기술 < 0) return -24;
        return Verbinden(서술자, 기술, 3, 0, lezen_schrijven_vlag);
    }
    static int 종단점기술(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        return soort_WAARDE[기술] == 3 ? 기술 : -88;
    }
    static int ADRES_32(int ADRES) {
        return mobiel_WAARDE.기억읽기(ADRES) << 24 | mobiel_WAARDE.기억읽기(ADRES + 1) << 16
            | mobiel_WAARDE.기억읽기(ADRES + 2) << 8 | mobiel_WAARDE.기억읽기(ADRES + 3);
    }
    static int cheque_ADRES(int ADRES, int tijdsduur_WAARDE) {
        if (tijdsduur_WAARDE < 16) return -22;
        if (!uitvoerbewerking_Manager.clip(ADRES, 16)) return -14;
        return uitvoerbewerking_Manager.짧은수(ADRES) == 2 ? 0 : -97;
    }
    static int BIND_ADRES(int 서술자, int ADRES, int tijdsduur_WAARDE) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int resultaat = cheque_ADRES(ADRES, tijdsduur_WAARDE);
        if (resultaat < 0) return resultaat;
        if (net_greep[기술] != 0) return -22;
        int netwerk_id = ADRES_32(ADRES + 4);
        if (netwerk_id != 0 && netwerk_id != net_stack.내주소) return -99;
        int poortnummer = mobiel_WAARDE.기억읽기(ADRES + 2) << 8 | mobiel_WAARDE.기억읽기(ADRES + 3);
        resultaat = net_stack.Openen(poortnummer);
        if (resultaat < 0) return resultaat;
        net_greep[기술] = resultaat; doel[기술] = netwerk_id;
        return 0;
    }
    static int Auto_BIND(int 기술) {
        if (net_greep[기술] != 0) return 0;
        int resultaat = net_stack.Openen(0);
        if (resultaat < 0) return resultaat;
        net_greep[기술] = resultaat;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 aanvraag 구조체로 전달한다.
    static int e_mailen_datagram_gegevens(int 서술자, int gegevens_ADRES, int tijdsduur_WAARDE, int Instellingen, int aangevraagd_ADRES) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (Instellingen != 0) return -95;
        if (tijdsduur_WAARDE < 0 || tijdsduur_WAARDE > 1024) return -90;
        if (tijdsduur_WAARDE != 0 && !uitvoerbewerking_Manager.clip(gegevens_ADRES, tijdsduur_WAARDE)) return -14;
        if (!uitvoerbewerking_Manager.clip(aangevraagd_ADRES, 8)) return -14;
        int ADRES = uitvoerbewerking_Manager.nummer(aangevraagd_ADRES);
        int resultaat = cheque_ADRES(ADRES, uitvoerbewerking_Manager.nummer(aangevraagd_ADRES + 4));
        if (resultaat < 0) return resultaat;
        int poortnummer = mobiel_WAARDE.기억읽기(ADRES + 2) << 8 | mobiel_WAARDE.기억읽기(ADRES + 3);
        if (poortnummer == 0) return -22;
        resultaat = Auto_BIND(기술);
        if (resultaat < 0) return resultaat;
        for (int INDEX = 0; INDEX < tijdsduur_WAARDE; INDEX++) transfer_gegevens[INDEX] = mobiel_WAARDE.기억읽기(gegevens_ADRES + INDEX);
        return net_stack.e_mailen(net_greep[기술], ADRES_32(ADRES + 4), poortnummer, transfer_gegevens, tijdsduur_WAARDE);
    }
    static void schrijven_ADRES(int ADRES, int tijdsduur_WAARDE, int netwerk_id, int poortnummer) {
        for (int INDEX = 0; INDEX < tijdsduur_WAARDE && INDEX < 16; INDEX++) {
            int WAARDE = 0;
            if (INDEX == 0) WAARDE = 2;
            if (INDEX == 2) WAARDE = poortnummer >>> 8;
            if (INDEX == 3) WAARDE = poortnummer;
            if (INDEX >= 4 && INDEX < 8) WAARDE = netwerk_id >>> (56 - INDEX * 8);
            mobiel_WAARDE.schrijven_Geheugen(ADRES + INDEX, WAARDE & 255);
        }
    }
    static int ontvangen_datagram_gegevens(int 서술자, int gegevens_ADRES, int tijdsduur_WAARDE, int Instellingen, int aangevraagd_ADRES) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((Instellingen & ~64) != 0) return -95;
        if (tijdsduur_WAARDE < 0) return -22;
        if (tijdsduur_WAARDE != 0 && !uitvoerbewerking_Manager.clip(gegevens_ADRES, tijdsduur_WAARDE)) return -14;
        int ADRES = 0, ADRES_tijdsduur_ADRES = 0, ADRES_tijdsduur = 0;
        if (aangevraagd_ADRES != 0) {
            if (!uitvoerbewerking_Manager.clip(aangevraagd_ADRES, 8)) return -14;
            ADRES = uitvoerbewerking_Manager.nummer(aangevraagd_ADRES); ADRES_tijdsduur_ADRES = uitvoerbewerking_Manager.nummer(aangevraagd_ADRES + 4);
            if (ADRES != 0) {
                if (!uitvoerbewerking_Manager.clip(ADRES_tijdsduur_ADRES, 4)) return -14;
                ADRES_tijdsduur = uitvoerbewerking_Manager.nummer(ADRES_tijdsduur_ADRES);
                if (ADRES_tijdsduur < 0) return -22;
                if (!uitvoerbewerking_Manager.clip(ADRES, ADRES_tijdsduur < 16 ? ADRES_tijdsduur : 16)) return -14;
            }
        }
        int resultaat = Auto_BIND(기술);
        if (resultaat < 0) return resultaat;
        int starten = mobiel_WAARDE.밀리초();
        while (true) {
            resultaat = net_stack.ontvangen(net_greep[기술], transfer_gegevens, 1024, 0);
            if (resultaat != -11) break;
            if ((Instellingen & 64) != 0 || (open_Instellingen[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && mobiel_WAARDE.밀리초() - starten >= 수신대기밀리초[기술]) return -11;
            if (mobiel_WAARDE.사용자남은밀리초() <= 10) return -11;
            mobiel_WAARDE.잠시양보();
        }
        if (resultaat < 0) return resultaat;
        if (resultaat > tijdsduur_WAARDE) resultaat = tijdsduur_WAARDE;
        for (int INDEX = 0; INDEX < resultaat; INDEX++) mobiel_WAARDE.schrijven_Geheugen(gegevens_ADRES + INDEX, transfer_gegevens[INDEX]);
        if (ADRES != 0) {
            schrijven_ADRES(ADRES, ADRES_tijdsduur, net_stack.peer_ADRES(net_greep[기술]), net_stack.peer_poortnummer(net_greep[기술]));
            uitvoerbewerking_Manager.schrijven_nummer(ADRES_tijdsduur_ADRES, 16);
        }
        return resultaat;
    }
    static int 통신주소읽기(int 서술자, int ADRES, int tijdsduur_ADRES) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!uitvoerbewerking_Manager.clip(tijdsduur_ADRES, 4)) return -14;
        int tijdsduur_WAARDE = uitvoerbewerking_Manager.nummer(tijdsduur_ADRES);
        if (tijdsduur_WAARDE < 0) return -22;
        if (!uitvoerbewerking_Manager.clip(ADRES, tijdsduur_WAARDE < 16 ? tijdsduur_WAARDE : 16)) return -14;
        int sleuf_invoer = net_stack.INDEX(net_greep[기술]);
        schrijven_ADRES(ADRES, tijdsduur_WAARDE, doel[기술], sleuf_invoer < 0 ? 0 : net_stack.접속번호들[sleuf_invoer]);
        uitvoerbewerking_Manager.schrijven_nummer(tijdsduur_ADRES, 16);
        return 0;
    }
    static int set_ontvangen_TIMEOUT(int 서술자, int 밀리초) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (밀리초 < 0 || 밀리초 > 2000) return -22;
        수신대기밀리초[기술] = 밀리초;
        return 0;
    }
}
