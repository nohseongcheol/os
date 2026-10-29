// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Curaçao.JCuwOS.systeemaanroep;

import Curaçao.JCuwOS.Geheugen_regio.Paginabeheer;
import Curaçao.JCuwOS.작업.Proces_WAARDE;
import Curaçao.JCuwOS.작업.Planner;
import Curaçao.JCuwOS.bestandssysteem.uitvoerbaar_laadprogramma;
import Curaçao.JCuwOS.bestandssysteem.bestandssysteem;
import Curaçao.JCuwOS.bestandssysteem.Bestand_info;
import Curaçao.JCuwOS.Kern.hardware_WAARDE;
import Curaçao.JCuwOS.invoer_WAARDE.invoer_Manager;
import Curaçao.JCuwOS.invoer_WAARDE.invoergebeurtenis;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class systeemaanroep {
    public static final int alleen_lezen_vlag = 0;
    public static final int Search_START = 0;
    public static final int Search_actueel = 1;
    public static final int Zoeken_invoer_beëindigen = 2;

    private final bestandssysteem bestandssysteem;
    private final Paginabeheer 쪽관리;
    private final Planner Planner;
    private final uitvoerbaar_laadprogramma laadprogramma = new uitvoerbaar_laadprogramma();
    private final hardware_WAARDE mobiel_WAARDE;
    private final invoer_Manager 입력관리;

    public systeemaanroep(bestandssysteem bestandssysteem, Paginabeheer 쪽관리, Planner Planner, hardware_WAARDE mobiel_WAARDE, invoer_Manager 입력관리) {
        this.bestandssysteem = bestandssysteem;
        this.쪽관리 = 쪽관리;
        this.Planner = Planner;
        this.mobiel_WAARDE = mobiel_WAARDE;
        this.입력관리 = 입력관리;
    }

    public int Proces_id(Proces_WAARDE actueel_Proces) {
        return actueel_Proces.id_WAARDE();
    }

    public int bovenliggend_Proces_id(Proces_WAARDE actueel_Proces) {
        return actueel_Proces.bovenliggend_id();
    }

    public int Openen(Proces_WAARDE actueel_Proces, String Naam, int vlag_WAARDE) {
        if (vlag_WAARDE != alleen_lezen_vlag) {
            return -30;
        }
        return actueel_Proces.파일서술자().Openen(Naam);
    }

    public int Lezen(Proces_WAARDE actueel_Proces, int 서술자, byte[] ontvangen_doel, int Grootte) {
        if (서술자 == 0) {
            if (Grootte <= 0 || ontvangen_doel.length == 0) {
                return 0;
            }
            invoergebeurtenis Gebeurtenis = 입력관리.Volgende_gebeurtenis();
            if (Gebeurtenis == null || Gebeurtenis.soort_gebeurtenis() != invoergebeurtenis.soort_WAARDE.toets_offline) {
                return -11;
            }
            ontvangen_doel[0] = (byte) Gebeurtenis.첫째값();
            return 1;
        }
        return actueel_Proces.파일서술자().Lezen(서술자, ontvangen_doel, Grootte);
    }

    public int Schrijven(Proces_WAARDE actueel_Proces, int 서술자, byte[] gegevens, int Grootte) {
        if (서술자 != 1 && 서술자 != 2) {
            return actueel_Proces.파일서술자().informatie_open(서술자) ? -30 : -9;
        }
        if (Grootte < 0 || Grootte > gegevens.length) {
            return -22;
        }
        mobiel_WAARDE.직렬출력(new String(gegevens, 0, Grootte, java.nio.charset.StandardCharsets.UTF_8));
        return Grootte;
    }

    public int Sluiten(Proces_WAARDE actueel_Proces, int 서술자) {
        return actueel_Proces.파일서술자().Sluiten(서술자);
    }

    public int verplaatsen_functie(Proces_WAARDE actueel_Proces, int 서술자, int 거리, int Taken_wortel) {
        return actueel_Proces.파일서술자().verplaatsen_functie(서술자, 거리, Taken_wortel);
    }

    public int 서술자복제(Proces_WAARDE actueel_Proces, int 서술자) {
        return actueel_Proces.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(Proces_WAARDE actueel_Proces, int 서술자, int 새서술자) {
        return actueel_Proces.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String Naam, int methode_MODUS) {
        Bestand_info msinfo32_exe = bestandssysteem.msinfo32_exe(Naam);
        if (msinfo32_exe == null) {
            return -2;
        }
        if ((methode_MODUS & 1) != 0 && (msinfo32_exe.vorm_soort() & 0111) == 0) {
            return -13;
        }
        if ((methode_MODUS & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int switch_Takenlijst(String Naam) {
        return "/".equals(Naam) ? 0 : -20;
    }

    public String actueel_Takenlijst(int ontvangen_formaat_wijzigen) {
        return ontvangen_formaat_wijzigen >= 2 ? "/" : null;
    }

    public int UID() { return 0; }
    public int effectief_UID() { return 0; }
    public int GID() { return 0; }
    public int effectief_GID() { return 0; }

    public int synchroniseren_Bestand(Proces_WAARDE actueel_Proces, int 서술자) {
        return actueel_Proces.파일서술자().msinfo32_exe(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // actueel_item 파일체계는 Lezen 전용이어서 밀어낼 자료가 없다.
    }

    public boolean informatie_Terminal(Proces_WAARDE actueel_Proces, int 서술자) {
        Bestand_info msinfo32_exe = actueel_Proces.파일서술자().msinfo32_exe(서술자);
        return msinfo32_exe != null && (msinfo32_exe.vorm_soort() & 0170000) == 0020000;
    }

    public int bestandsbesturing(Proces_WAARDE actueel_Proces, int 서술자, int opdracht, int parameter_argument) {
        if (opdracht == 0) {
            return actueel_Proces.파일서술자().복제서술자(서술자, parameter_argument);
        }
        if (opdracht == 1) {
            return actueel_Proces.파일서술자().실행시닫기값(서술자);
        }
        if (opdracht == 2) {
            return actueel_Proces.파일서술자().실행시닫기설정(서술자, (parameter_argument & 1) != 0);
        }
        if (opdracht == 3) {
            return actueel_Proces.파일서술자().msinfo32_exe(서술자) == null ? -9 : alleen_lezen_vlag;
        }
        if (opdracht == 4) {
            return parameter_argument == alleen_lezen_vlag ? 0 : -30;
        }
        return -22;
    }

    public int maken_invoer(String Naam, int machtiging_WAARDE) {
        return -30;
    }

    public Bestand_info 서술자정보(Proces_WAARDE actueel_Proces, int 서술자) {
        return actueel_Proces.파일서술자().msinfo32_exe(서술자);
    }

    public Systeem_Details Systeem_Details() {
        return new Systeem_Details("JCuwOS", "JCuwOS", "0.1", "Java managed kernel", "i386");
    }

    public Bestand_info Bestand_info(String Naam) {
        return bestandssysteem.msinfo32_exe(Naam);
    }

    public Proces_WAARDE kloon_Proces(Proces_WAARDE bovenliggend_WAARDE) {
        return Planner.kloon_WAARDE(bovenliggend_WAARDE);
    }

    public int 자식기다리기(Proces_WAARDE bovenliggend_WAARDE, int kind_id, boolean 기다리지않음) {
        return Planner.자식기다리기(bovenliggend_WAARDE, kind_id, 기다리지않음);
    }

    public int app_pauze(Proces_WAARDE actueel_Proces, int 새끝) {
        int Vorige_beëindigen = actueel_Proces.app_pauze();
        if (새끝 == 0) {
            return Vorige_beëindigen;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = Vorige_beëindigen / Paginabeheer.paginaformaat;
        int 끝쪽 = (새끝 + Paginabeheer.paginaformaat - 1) / Paginabeheer.paginaformaat;
        if (새끝 > Vorige_beëindigen) {
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int ADRES = INDEX * Paginabeheer.paginaformaat;
                try {
                    쪽관리.바이트읽기(actueel_Proces.adresruimte(), ADRES);
                } catch (IllegalStateException fout) {
                    쪽관리.MAP_page(actueel_Proces.adresruimte(), ADRES, true);
                }
            }
        }
        actueel_Proces.set_app_pauze(새끝);
        return 새끝;
    }

    public int toename_app_pauze(Proces_WAARDE actueel_Proces, int toename_aantal) {
        int Vorige_beëindigen = actueel_Proces.app_pauze();
        int resultaat = app_pauze(actueel_Proces, Vorige_beëindigen + toename_aantal);
        return resultaat < 0 ? resultaat : Vorige_beëindigen;
    }

    public int Uitvoeren_opdracht(Proces_WAARDE actueel_Proces, byte[] uitvoerbaar_bestand) {
        return Uitvoeren_opdracht(actueel_Proces, uitvoerbaar_bestand, new String[0], new String[0]);
    }

    public int Uitvoeren_opdracht(Proces_WAARDE actueel_Proces, byte[] uitvoerbaar_bestand, String[] parameter_argument, String[] omgeving) {
        uitvoerbaar_laadprogramma.kopie kopie_WAARDE;
        try {
            kopie_WAARDE = laadprogramma.검사(uitvoerbaar_bestand);
        } catch (IllegalArgumentException fout) {
            return -8;
        }
        if (parameter_argument == null || omgeving == null || parameter_argument.length > 16 || omgeving.length > 16) {
            return -7;
        }
        for (uitvoerbaar_laadprogramma.sectie_WAARDE sectie_WAARDE : kopie_WAARDE.구역들()) {
            if ((sectie_WAARDE.vlag_WAARDE() & 2) == 0 || sectie_WAARDE.Grootte() == 0) {
                continue;
            }
            int 첫쪽 = sectie_WAARDE.ADRES() / Paginabeheer.paginaformaat;
            int 끝쪽 = (sectie_WAARDE.ADRES() + sectie_WAARDE.Grootte() + Paginabeheer.paginaformaat - 1) / Paginabeheer.paginaformaat;
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int ADRES = INDEX * Paginabeheer.paginaformaat;
                try {
                    쪽관리.바이트읽기(actueel_Proces.adresruimte(), ADRES);
                    쪽관리.Privé_bereik_schrijven(actueel_Proces.adresruimte(), ADRES, Paginabeheer.paginaformaat);
                } catch (IllegalStateException fout) {
                    쪽관리.MAP_page(actueel_Proces.adresruimte(), ADRES, true);
                }
            }
            for (int INDEX = 0; INDEX < sectie_WAARDE.Grootte(); INDEX++) {
                byte WAARDE = sectie_WAARDE.soort_WAARDE() == 8 ? 0 : uitvoerbaar_bestand[sectie_WAARDE.Bestand_functie() + INDEX];
                쪽관리.schrijven_byte_WAARDE(actueel_Proces.adresruimte(), sectie_WAARDE.ADRES() + INDEX, WAARDE);
            }
        }
        actueel_Proces.set_uitvoerbewerking_context(kopie_WAARDE.START_ADRES(), parameter_argument, omgeving);
        actueel_Proces.파일서술자().실행시닫기();
        return 0;
    }

    public void sluiten_app(Proces_WAARDE actueel_Proces, int Status_WAARDE) {
        actueel_Proces.Einde_app(Status_WAARDE);
    }
}
