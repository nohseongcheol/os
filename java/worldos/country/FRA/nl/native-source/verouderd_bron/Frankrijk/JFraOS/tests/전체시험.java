// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Frankrijk.JFraOS.tests;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Frankrijk.JFraOS.Geheugen_regio.Geheugen_Manager;
import Frankrijk.JFraOS.Geheugen_regio.Paginabeheer;
import Frankrijk.JFraOS.invoer_WAARDE.invoergebeurtenis;
import Frankrijk.JFraOS.작업.Proces_WAARDE;
import Frankrijk.JFraOS.systeemaanroep.systeemaanroep;
import Frankrijk.JFraOS.bestandssysteem.uitvoerbaar_laadprogramma;
import Frankrijk.JFraOS.Kern.Kern;
import Frankrijk.JFraOS.host.host_hardware;
import Frankrijk.JFraOS.IRQ.IRQ_Manager;
import Frankrijk.JFraOS.서술자.전역서술자표;
import Frankrijk.JFraOS.opslagapparaat.고급기술결합장치;
import Frankrijk.JFraOS.mobiel_WAARDE.accessoire_bus_Manager;
import Frankrijk.JFraOS.net_stack.net_Hulpprogramma_s;
import Frankrijk.JFraOS.net_stack.netwerklaag;
import Frankrijk.JFraOS.mobiel_WAARDE.Klok;
import Frankrijk.JFraOS.서술자.taak_Status_segment;
import Frankrijk.JFraOS.scherm.teken_weergeven;
import Frankrijk.JFraOS.bestandssysteem.primaire_partitie_tabel;

public final class 전체시험 {
    private static int doorgeven_AANTAL;

    private 전체시험() {
    }

    public static void main(String[] parameter_argument) {
        host_hardware mobiel_WAARDE = new host_hardware();
        Kern kernel_WAARDE = new Kern(mobiel_WAARDE);
        kernel_WAARDE.starten();

        test_Geheugen(kernel_WAARDE);
        쪽관리시험(kernel_WAARDE);
        파일과과정시험(kernel_WAARDE);
        실행파일시험(kernel_WAARDE);
        test_invoer(kernel_WAARDE);
        test_hardware(mobiel_WAARDE);
        개입중단과서술자시험();
        test_Opslag_EN_Netwerken();
        test_scherm_EN_Klok();

        System.out.println("JFraOS tests doorgeven_WAARDE: " + doorgeven_AANTAL);
    }

    private static void test_Geheugen(Kern kernel_WAARDE) {
        Geheugen_Manager Manager_WAARDE = kernel_WAARDE.Geheugen_regio();
        int 첫주소 = Manager_WAARDE.정렬할당(100, 64);
        bevestigen((첫주소 & 63) == 0, "uitlijnen_WAARDE toewijzen_Opslag");
        Manager_WAARDE.schrijven_byte_WAARDE(첫주소, (byte) 0x5a);
        bevestigen(Manager_WAARDE.바이트읽기(첫주소) == (byte) 0x5a, "물리 Geheugen_regio 읽고 Schrijven");
        int 사용전 = Manager_WAARDE.사용크기();
        Manager_WAARDE.versie_Opslag(첫주소);
        bevestigen(Manager_WAARDE.사용크기() < 사용전, "Geheugen_regio versie_Opslag");
    }

    private static void 쪽관리시험(Kern kernel_WAARDE) {
        Paginabeheer Manager_WAARDE = kernel_WAARDE.쪽관리();
        Paginabeheer.adresruimte bovenliggend_Space = Manager_WAARDE.새주소공간();
        Manager_WAARDE.MAP_page(bovenliggend_Space, 0x1000, true);
        Manager_WAARDE.schrijven_byte_WAARDE(bovenliggend_Space, 0x1010, (byte) 7);
        Paginabeheer.adresruimte kind_Space = Manager_WAARDE.kloon_kopiëren_bij_schrijven(bovenliggend_Space);
        Manager_WAARDE.schrijven_byte_WAARDE(kind_Space, 0x1010, (byte) 9);
        bevestigen(Manager_WAARDE.바이트읽기(bovenliggend_Space, 0x1010) == 7, "Schrijven 시 kopiëren_WAARDE bovenliggend_WAARDE 격리");
        bevestigen(Manager_WAARDE.바이트읽기(kind_Space, 0x1010) == 9, "Schrijven 시 kopiëren_WAARDE kind_WAARDE Schrijven");
    }

    private static void 파일과과정시험(Kern kernel_WAARDE) {
        byte[] Inhoud_WAARDE = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        kernel_WAARDE.bestandssysteem().toevoegen_Bestand("tests", Inhoud_WAARDE);
        Proces_WAARDE bovenliggend_WAARDE = kernel_WAARDE.첫과정();
        systeemaanroep 호출 = kernel_WAARDE.systeemaanroep();
        int 서술자 = 호출.Openen(bovenliggend_WAARDE, "/tests", systeemaanroep.alleen_lezen_vlag);
        bevestigen(서술자 >= 3, "bestand Openen");

        byte[] ontvangen_doel = new byte[Inhoud_WAARDE.length];
        bevestigen(호출.Lezen(bovenliggend_WAARDE, 서술자, ontvangen_doel, ontvangen_doel.length) == Inhoud_WAARDE.length, "bestand Lezen");
        bevestigen(Arrays.equals(Inhoud_WAARDE, ontvangen_doel), "bestand Inhoud_WAARDE");
        bevestigen(호출.verplaatsen_functie(bovenliggend_WAARDE, 서술자, 0, systeemaanroep.Search_START) == 0, "bestand positie verplaatsen_WAARDE_83b651b8");

        int 복제서술자 = 호출.서술자복제(bovenliggend_WAARDE, 서술자);
        bevestigen(복제서술자 >= 0, "서술자 kloon_WAARDE");
        Proces_WAARDE kind_WAARDE = 호출.kloon_Proces(bovenliggend_WAARDE);
        bevestigen(kind_WAARDE.id_WAARDE() != bovenliggend_WAARDE.id_WAARDE(), "Proces_WAARDE id_WAARDE 분리");
        bevestigen(kind_WAARDE.bovenliggend_id() == bovenliggend_WAARDE.id_WAARDE(), "bovenliggend_WAARDE Proces_WAARDE id_WAARDE");
        bevestigen(호출.Sluiten(kind_WAARDE, 서술자) == 0 && bovenliggend_WAARDE.파일서술자().informatie_open(서술자), "kind_WAARDE Sluiten 격리");

        int Vorige_beëindigen = 호출.toename_app_pauze(bovenliggend_WAARDE, 8192);
        bevestigen(Vorige_beëindigen == 0x06000000, "app_f5044b9b 끝 늘리기");
        bevestigen(bovenliggend_WAARDE.app_pauze() == 0x06002000, "app_f5044b9b 끝 반영");
        bevestigen(kind_WAARDE.app_pauze() == 0x06000000, "과정별 app_f5044b9b 끝 격리");

        kind_WAARDE.Einde_app(7);
        bevestigen(호출.자식기다리기(bovenliggend_WAARDE, kind_WAARDE.id_WAARDE(), false) == (7 << 8), "kind_WAARDE Einde_app 기다리기");
        bevestigen(호출.접근가능("tests", 1) == -13, "Uitvoeren_opdracht machtiging_WAARDE weigeren_WAARDE");
        bevestigen(호출.UID() == 0 && 호출.GID() == 0, "사용자와 무리 id_WAARDE");
        bevestigen("/".equals(호출.actueel_Takenlijst(2)) && 호출.switch_Takenlijst("/") == 0, "actueel_item 작업 invoer_Lijst_f07b3200");
        bevestigen(호출.informatie_Terminal(bovenliggend_WAARDE, 1), "표준 tekstuitvoer 단말");
        bevestigen("JFraOS".equals(호출.Systeem_Details().Systeem_naam()), "besturingssysteem_WAARDE msinfo32_exe");
    }

    private static void 실행파일시험(Kern kernel_WAARDE) {
        byte[] gegevens = new byte[92];
        gegevens[0] = 0x7f;
        gegevens[1] = 'E';
        gegevens[2] = 'L';
        gegevens[3] = 'F';
        gegevens[4] = 1;
        gegevens[5] = 1;
        schrijven_geheel_getal_WAARDE(gegevens, 24, 0x04001000);
        schrijven_geheel_getal_WAARDE(gegevens, 32, 52);
        짧은정수쓰기(gegevens, 46, 40);
        짧은정수쓰기(gegevens, 48, 1);
        schrijven_geheel_getal_WAARDE(gegevens, 56, 8);
        schrijven_geheel_getal_WAARDE(gegevens, 60, 2);
        schrijven_geheel_getal_WAARDE(gegevens, 64, 0x04002000);
        schrijven_geheel_getal_WAARDE(gegevens, 72, 64);

        uitvoerbaar_laadprogramma.kopie kopie_WAARDE = new uitvoerbaar_laadprogramma().검사(gegevens);
        bevestigen(kopie_WAARDE.START_ADRES() == 0x04001000, "ELF starten ADRES");
        bevestigen(kopie_WAARDE.구역들().size() == 1 && kopie_WAARDE.구역들().get(0).soort_WAARDE() == 8, "ELF 빈 gegevens sectie_WAARDE");
        int 서술자 = kernel_WAARDE.systeemaanroep().Openen(kernel_WAARDE.첫과정(), "tests", systeemaanroep.alleen_lezen_vlag);
        bevestigen(kernel_WAARDE.systeemaanroep().bestandsbesturing(kernel_WAARDE.첫과정(), 서술자, 2, 1) == 0, "Uitvoeren_opdracht 시 Sluiten Instellingen");
        bevestigen(kernel_WAARDE.systeemaanroep().Uitvoeren_opdracht(kernel_WAARDE.첫과정(), gegevens, new String[] {"tests", "값"}, new String[] {"Taal=Nederlands"}) == 0, "ELF Uitvoeren_opdracht kopie_WAARDE 적재");
        bevestigen(kernel_WAARDE.첫과정().uitvoerbewerking_START_ADRES() == 0x04001000, "Uitvoeren_opdracht starten ADRES 반영");
        bevestigen(kernel_WAARDE.첫과정().uitvoerbewerking_argument().length == 2 && kernel_WAARDE.첫과정().omgeving_WAARDE().length == 1, "Uitvoeren_opdracht 인자와 omgeving");
        bevestigen(!kernel_WAARDE.첫과정().파일서술자().informatie_open(서술자), "Uitvoeren_opdracht 시 서술자 Sluiten");
        bevestigen(kernel_WAARDE.쪽관리().바이트읽기(kernel_WAARDE.첫과정().adresruimte(), 0x04002000) == 0, "빈 gegevens sectie_WAARDE nul_operand initialiseren");
    }

    private static void test_invoer(Kern kernel_WAARDE) {
        kernel_WAARDE.입력관리().toets_offline('가');
        kernel_WAARDE.입력관리().쥐이동(3, -2);
        invoergebeurtenis 첫사건 = kernel_WAARDE.입력관리().Volgende_gebeurtenis();
        invoergebeurtenis SECONDE_gebeurtenis = kernel_WAARDE.입력관리().Volgende_gebeurtenis();
        bevestigen(첫사건.soort_gebeurtenis() == invoergebeurtenis.soort_WAARDE.toets_offline, "자판 Gebeurtenis");
        bevestigen(SECONDE_gebeurtenis.첫째값() == 3 && SECONDE_gebeurtenis.SECONDE_WAARDE() == -2, "쥐 verplaatsen_WAARDE_83b651b8 Gebeurtenis");
    }

    private static void test_hardware(host_hardware mobiel_WAARDE) {
        mobiel_WAARDE.schrijven_poort_byte(0x3f8, 0xab);
        bevestigen(mobiel_WAARDE.포트바이트읽기(0x3f8) == 0xab, "hardware_poort I_O grens_WAARDE");
        bevestigen(mobiel_WAARDE.직렬기록().contains("JFraOS"), "직렬 LOG_RECORD");
    }

    private static void 개입중단과서술자시험() {
        IRQ_Manager Manager_WAARDE = new IRQ_Manager();
        Manager_WAARDE.register_invoer(0x21, Opslag_ADRES -> Opslag_ADRES + 4);
        Manager_WAARDE.inschakelen();
        bevestigen(Manager_WAARDE.verdelen_WAARDE(0x21, 100) == 104, "IRQ verdelen_WAARDE");
        Manager_WAARDE.deactiveren();
        bevestigen(Manager_WAARDE.verdelen_WAARDE(0x21, 100) == 100, "IRQ deactiveren");

        전역서술자표 서술자표 = new 전역서술자표();
        서술자표.set_standaardwaarde();
        bevestigen(서술자표.조각들().size() == 5, "전역 서술자표");
        taak_Status_segment taak_Status = new taak_Status_segment();
        taak_Status.특권쌓임공간설정(0x10, 0x800000);
        bevestigen(taak_Status.stack_nul_blok() == 0x10 && taak_Status.stack_nul_ADRES() == 0x800000, "작업 Status_WAARDE sectie_WAARDE");
    }

    private static void test_Opslag_EN_Netwerken() {
        고급기술결합장치 opslagapparaat = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.sectie_formaat_wijzigen];
        byte[] 읽은자료 = new byte[고급기술결합장치.sectie_formaat_wijzigen];
        쓸자료[17] = 42;
        opslagapparaat.Schrijven(2, 쓸자료);
        opslagapparaat.Lezen(2, 읽은자료);
        bevestigen(읽은자료[17] == 42, "ATA sectie_WAARDE 읽고 Schrijven");

        accessoire_bus_Manager accessoire = new accessoire_bus_Manager();
        accessoire.발견(new accessoire_bus_Manager.mobiel_WAARDE(0x1022, 0x2000, 0xc000, 11));
        bevestigen(accessoire.Zoeken_invoer(0x1022, 0x2000) != null, "주변 mobiel_WAARDE Zoeken_invoer");

        byte[] Ethernet_frame = new byte[34];
        Ethernet_frame[12] = 0x08;
        Ethernet_frame[13] = 0x00;
        Ethernet_frame[14] = 0x45;
        bevestigen(net_Hulpprogramma_s.Ethernet_HOOFDLETTERS_protocol(Ethernet_frame) == 0x0800, "이더넷 상위 contractwaarde");
        bevestigen(net_Hulpprogramma_s.informatie_FPA_4_protocol(Ethernet_frame, 14), "상호통신망규약 4판");
        bevestigen(net_Hulpprogramma_s.mesh_controlesom(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 controlesom");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        schrijven_geheel_getal_WAARDE(첫구역, 454, 63);
        schrijven_geheel_getal_WAARDE(첫구역, 458, 1024);
        bevestigen(new primaire_partitie_tabel().Lezen(첫구역).size() == 1, "standaardwaarde 분할 영역표");

        netwerklaag laag_WAARDE = new netwerklaag();
        int[] OPBRENGST_AANTAL = new int[1];
        laag_WAARDE.register_gebruiker_gegevens_les(7, (gegevens, starten, tijdsduur_WAARDE) -> OPBRENGST_AANTAL[0]++);
        byte[] frame_INDEX = new byte[14 + 20 + 8];
        frame_INDEX[12] = 0x08;
        frame_INDEX[13] = 0x00;
        frame_INDEX[14] = 0x45;
        frame_INDEX[16] = 0;
        frame_INDEX[17] = 28;
        frame_INDEX[23] = 17;
        frame_INDEX[36] = 0;
        frame_INDEX[37] = 7;
        bevestigen(laag_WAARDE.ontvangen_Ethernet(frame_INDEX) && OPBRENGST_AANTAL[0] == 1, "gebruikersruimte gegevens les_WAARDE_7c611f50 verdelen_WAARDE");
    }

    private static void test_scherm_EN_Klok() {
        teken_weergeven scherm = new teken_weergeven();
        scherm.tekstuitvoer("가나\n다");
        bevestigen(scherm.문자(0, 0) == '가' && scherm.문자(0, 1) == '다', "문자 scherm tekstuitvoer");
        Klok Klok = new Klok(100);
        for (int INDEX = 0; INDEX < 10; INDEX++) {
            Klok.tik_WAARDE();
        }
        bevestigen(Klok.지난밀리초() == 100, "Klok tik_WAARDE CONVERTEREN_WAARDE");
    }

    private static void schrijven_geheel_getal_WAARDE(byte[] gegevens, int positie, int WAARDE) {
        gegevens[positie] = (byte) WAARDE;
        gegevens[positie + 1] = (byte) (WAARDE >>> 8);
        gegevens[positie + 2] = (byte) (WAARDE >>> 16);
        gegevens[positie + 3] = (byte) (WAARDE >>> 24);
    }

    private static void 짧은정수쓰기(byte[] gegevens, int positie, int WAARDE) {
        gegevens[positie] = (byte) WAARDE;
        gegevens[positie + 1] = (byte) (WAARDE >>> 8);
    }

    private static void bevestigen(boolean toestand, String Naam) {
        if (!toestand) {
            throw new AssertionError("fout_WAARDE: " + Naam);
        }
        doorgeven_AANTAL++;
        System.out.println("doorgeven_WAARDE: " + Naam);
    }
}
