// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Svalbard_og_Jan_Mayen.JSjmOS.시험;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Svalbard_og_Jan_Mayen.JSjmOS.Minne_område.Minne_overordnet;
import Svalbard_og_Jan_Mayen.JSjmOS.Minne_område.Sidebehandling;
import Svalbard_og_Jan_Mayen.JSjmOS.inndata_VERDI.inndatahendelse;
import Svalbard_og_Jan_Mayen.JSjmOS.작업.Prosess_VERDI;
import Svalbard_og_Jan_Mayen.JSjmOS.체계호출.체계호출;
import Svalbard_og_Jan_Mayen.JSjmOS.filsystem.kjørbar_fil_laster;
import Svalbard_og_Jan_Mayen.JSjmOS.kjerne.kjerne;
import Svalbard_og_Jan_Mayen.JSjmOS.vert.vert_maskinvare;
import Svalbard_og_Jan_Mayen.JSjmOS.IRQ.IRQ_overordnet;
import Svalbard_og_Jan_Mayen.JSjmOS.서술자.전역서술자표;
import Svalbard_og_Jan_Mayen.JSjmOS.lagringsenhet.고급기술결합장치;
import Svalbard_og_Jan_Mayen.JSjmOS.enhet_VERDI.tilbehør_buss_overordnet;
import Svalbard_og_Jan_Mayen.JSjmOS.nettverk_stakk.nettverk_Verktøy;
import Svalbard_og_Jan_Mayen.JSjmOS.nettverk_stakk.nettverkslag;
import Svalbard_og_Jan_Mayen.JSjmOS.enhet_VERDI.Klokke;
import Svalbard_og_Jan_Mayen.JSjmOS.서술자.oppgave_status_segment;
import Svalbard_og_Jan_Mayen.JSjmOS.skjermbilde.tegn_vise;
import Svalbard_og_Jan_Mayen.JSjmOS.filsystem.primærpartisjon_tabell;

public final class 전체시험 {
    private static int sende_ANTALL;

    private 전체시험() {
    }

    public static void main(String[] parameter_argument) {
        vert_maskinvare enhet_VERDI = new vert_maskinvare();
        kjerne kjerne_VERDI = new kjerne(enhet_VERDI);
        kjerne_VERDI.Kjør_2();

        test_Minne(kjerne_VERDI);
        쪽관리시험(kjerne_VERDI);
        파일과과정시험(kjerne_VERDI);
        실행파일시험(kjerne_VERDI);
        test_inndata(kjerne_VERDI);
        test_maskinvare(enhet_VERDI);
        개입중단과서술자시험();
        test_lager_OG_Nettverk();
        test_skjermbilde_OG_Klokke();

        System.out.println("JSjmOS 시험 sende_VERDI: " + sende_ANTALL);
    }

    private static void test_Minne(kjerne kjerne_VERDI) {
        Minne_overordnet overordnet_VERDI = kjerne_VERDI.Minne_område();
        int 첫주소 = overordnet_VERDI.정렬할당(100, 64);
        bekrefte((첫주소 & 63) == 0, "justere_VERDI tildele_lager");
        overordnet_VERDI.skrive_byte_VERDI(첫주소, (byte) 0x5a);
        bekrefte(overordnet_VERDI.바이트읽기(첫주소) == (byte) 0x5a, "물리 Minne_område 읽고 Skriv");
        int 사용전 = overordnet_VERDI.사용크기();
        overordnet_VERDI.frigi_lager(첫주소);
        bekrefte(overordnet_VERDI.사용크기() < 사용전, "Minne_område frigi_lager");
    }

    private static void 쪽관리시험(kjerne kjerne_VERDI) {
        Sidebehandling overordnet_VERDI = kjerne_VERDI.쪽관리();
        Sidebehandling.adresseområde overordnet_Space = overordnet_VERDI.새주소공간();
        overordnet_VERDI.kart_page(overordnet_Space, 0x1000, true);
        overordnet_VERDI.skrive_byte_VERDI(overordnet_Space, 0x1010, (byte) 7);
        Sidebehandling.adresseområde barn_Space = overordnet_VERDI.쓰기시복사복제(overordnet_Space);
        overordnet_VERDI.skrive_byte_VERDI(barn_Space, 0x1010, (byte) 9);
        bekrefte(overordnet_VERDI.바이트읽기(overordnet_Space, 0x1010) == 7, "Skriv 시 kopiere_VERDI overordnet_VERDI_881a8172 격리");
        bekrefte(overordnet_VERDI.바이트읽기(barn_Space, 0x1010) == 9, "Skriv 시 kopiere_VERDI barn_VERDI Skriv");
    }

    private static void 파일과과정시험(kjerne kjerne_VERDI) {
        byte[] Innhold_VERDI = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        kjerne_VERDI.filsystem().Tilføye_Fil("시험", Innhold_VERDI);
        Prosess_VERDI overordnet_VERDI_881a8172 = kjerne_VERDI.첫과정();
        체계호출 호출 = kjerne_VERDI.체계호출();
        int 서술자 = 호출.Åpne(overordnet_VERDI_881a8172, "/시험", 체계호출.skrivebeskyttet_flagg);
        bekrefte(서술자 >= 3, "Fil Åpne");

        byte[] motta_mål = new byte[Innhold_VERDI.length];
        bekrefte(호출.Les(overordnet_VERDI_881a8172, 서술자, motta_mål, motta_mål.length) == Innhold_VERDI.length, "Fil Les");
        bekrefte(Arrays.equals(Innhold_VERDI, motta_mål), "Fil Innhold_VERDI");
        bekrefte(호출.flytte_plassere(overordnet_VERDI_881a8172, 서술자, 0, 체계호출.SØK_START) == 0, "Fil Posisjon flytte_VERDI_83b651b8");

        int 복제서술자 = 호출.서술자복제(overordnet_VERDI_881a8172, 서술자);
        bekrefte(복제서술자 >= 0, "서술자 klon_VERDI");
        Prosess_VERDI barn_VERDI = 호출.klon_Prosess(overordnet_VERDI_881a8172);
        bekrefte(barn_VERDI.identifikator_VERDI() != overordnet_VERDI_881a8172.identifikator_VERDI(), "Prosess_VERDI identifikator_VERDI 분리");
        bekrefte(barn_VERDI.overordnet_identifikator() == overordnet_VERDI_881a8172.identifikator_VERDI(), "overordnet_VERDI_881a8172 Prosess_VERDI identifikator_VERDI");
        bekrefte(호출.Lukk(barn_VERDI, 서술자) == 0 && overordnet_VERDI_881a8172.파일서술자().informasjonssystemer_åpen(서술자), "barn_VERDI Lukk 격리");

        int Forrige_avslutte_en_samtale = 호출.økning_app_pause(overordnet_VERDI_881a8172, 8192);
        bekrefte(Forrige_avslutte_en_samtale == 0x06000000, "app_f5044b9b 끝 늘리기");
        bekrefte(overordnet_VERDI_881a8172.app_pause() == 0x06002000, "app_f5044b9b 끝 반영");
        bekrefte(barn_VERDI.app_pause() == 0x06000000, "과정별 app_f5044b9b 끝 격리");

        barn_VERDI.Utgang_app(7);
        bekrefte(호출.자식기다리기(overordnet_VERDI_881a8172, barn_VERDI.identifikator_VERDI(), false) == (7 << 8), "barn_VERDI Utgang_app 기다리기");
        bekrefte(호출.접근가능("시험", 1) == -13, "Utfør_kommando tillatelse_VERDI avvise_VERDI");
        bekrefte(호출.UID() == 0 && 호출.gruppe_identifikator() == 0, "사용자와 무리 identifikator_VERDI");
        bekrefte("/".equals(호출.betalt_Oppgaveliste(2)) && 호출.bytt_Oppgaveliste("/") == 0, "betalt_vare 작업 oppføring_Liste");
        bekrefte(호출.informasjonssystemer_Terminal(overordnet_VERDI_881a8172, 1), "표준 Utgang 단말");
        bekrefte("JSjmOS".equals(호출.System_Detaljer().System_navn()), "operativsystem_VERDI msinfo32_exe");
    }

    private static void 실행파일시험(kjerne kjerne_VERDI) {
        byte[] data = new byte[92];
        data[0] = 0x7f;
        data[1] = 'E';
        data[2] = 'L';
        data[3] = 'F';
        data[4] = 1;
        data[5] = 1;
        skrive_heltall_VERDI(data, 24, 0x04001000);
        skrive_heltall_VERDI(data, 32, 52);
        짧은정수쓰기(data, 46, 40);
        짧은정수쓰기(data, 48, 1);
        skrive_heltall_VERDI(data, 56, 8);
        skrive_heltall_VERDI(data, 60, 2);
        skrive_heltall_VERDI(data, 64, 0x04002000);
        skrive_heltall_VERDI(data, 72, 64);

        kjørbar_fil_laster.BILDE BILDE_VERDI = new kjørbar_fil_laster().검사(data);
        bekrefte(BILDE_VERDI.START_e_post() == 0x04001000, "ELF Kjør_2 e_post");
        bekrefte(BILDE_VERDI.구역들().size() == 1 && BILDE_VERDI.구역들().get(0).종류() == 8, "ELF 빈 data inndeling_VERDI");
        int 서술자 = kjerne_VERDI.체계호출().Åpne(kjerne_VERDI.첫과정(), "시험", 체계호출.skrivebeskyttet_flagg);
        bekrefte(kjerne_VERDI.체계호출().Fil_kontroll(kjerne_VERDI.첫과정(), 서술자, 2, 1) == 0, "Utfør_kommando 시 Lukk Innstillinger");
        bekrefte(kjerne_VERDI.체계호출().Utfør_kommando(kjerne_VERDI.첫과정(), data, new String[] {"시험", "값"}, new String[] {"Språk=norsk"}) == 0, "ELF Utfør_kommando BILDE_VERDI 적재");
        bekrefte(kjerne_VERDI.첫과정().kjøring_START_e_post() == 0x04001000, "Utfør_kommando Kjør_2 e_post 반영");
        bekrefte(kjerne_VERDI.첫과정().kjøring_argument().length == 2 && kjerne_VERDI.첫과정().miljø_VERDI().length == 1, "Utfør_kommando 인자와 miljø");
        bekrefte(!kjerne_VERDI.첫과정().파일서술자().informasjonssystemer_åpen(서술자), "Utfør_kommando 시 서술자 Lukk");
        bekrefte(kjerne_VERDI.쪽관리().바이트읽기(kjerne_VERDI.첫과정().adresseområde(), 0x04002000) == 0, "빈 data inndeling_VERDI null_operand starte");
    }

    private static void test_inndata(kjerne kjerne_VERDI) {
        kjerne_VERDI.입력관리().키누름('가');
        kjerne_VERDI.입력관리().쥐이동(3, -2);
        inndatahendelse 첫사건 = kjerne_VERDI.입력관리().Neste_hendelse();
        inndatahendelse SEKUND_hendelse = kjerne_VERDI.입력관리().Neste_hendelse();
        bekrefte(첫사건.사건종류() == inndatahendelse.종류.키누름, "자판 Hendelse");
        bekrefte(SEKUND_hendelse.첫째값() == 3 && SEKUND_hendelse.SEKUND_VERDI() == -2, "쥐 flytte_VERDI_83b651b8 Hendelse");
    }

    private static void test_maskinvare(vert_maskinvare enhet_VERDI) {
        enhet_VERDI.skrive_port_byte(0x3f8, 0xab);
        bekrefte(enhet_VERDI.포트바이트읽기(0x3f8) == 0xab, "maskinvare_port I_U grense_VERDI");
        bekrefte(enhet_VERDI.직렬기록().contains("JSjmOS"), "직렬 LOG_POST");
    }

    private static void 개입중단과서술자시험() {
        IRQ_overordnet overordnet_VERDI = new IRQ_overordnet();
        overordnet_VERDI.register_oppføring(0x21, lager_e_post -> lager_e_post + 4);
        overordnet_VERDI.aktivere();
        bekrefte(overordnet_VERDI.distribuere_VERDI(0x21, 100) == 104, "IRQ distribuere_VERDI");
        overordnet_VERDI.deaktivere();
        bekrefte(overordnet_VERDI.distribuere_VERDI(0x21, 100) == 100, "IRQ deaktivere");

        전역서술자표 서술자표 = new 전역서술자표();
        서술자표.sett_standardverdi();
        bekrefte(서술자표.조각들().size() == 5, "전역 서술자표");
        oppgave_status_segment oppgave_status = new oppgave_status_segment();
        oppgave_status.특권쌓임공간설정(0x10, 0x800000);
        bekrefte(oppgave_status.stakk_null_blokk() == 0x10 && oppgave_status.stakk_null_e_post() == 0x800000, "작업 status_VERDI inndeling_VERDI");
    }

    private static void test_lager_OG_Nettverk() {
        고급기술결합장치 lagringsenhet = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.inndeling_skalere];
        byte[] 읽은자료 = new byte[고급기술결합장치.inndeling_skalere];
        쓸자료[17] = 42;
        lagringsenhet.Skriv(2, 쓸자료);
        lagringsenhet.Les(2, 읽은자료);
        bekrefte(읽은자료[17] == 42, "ATA inndeling_VERDI 읽고 Skriv");

        tilbehør_buss_overordnet tilbehør = new tilbehør_buss_overordnet();
        tilbehør.발견(new tilbehør_buss_overordnet.enhet_VERDI(0x1022, 0x2000, 0xc000, 11));
        bekrefte(tilbehør.Søk_oppføring(0x1022, 0x2000) != null, "주변 enhet_VERDI Søk_oppføring");

        byte[] Ethernet_bilde = new byte[34];
        Ethernet_bilde[12] = 0x08;
        Ethernet_bilde[13] = 0x00;
        Ethernet_bilde[14] = 0x45;
        bekrefte(nettverk_Verktøy.Ethernet_STORE_protokoll(Ethernet_bilde) == 0x0800, "이더넷 상위 kontraktverdi");
        bekrefte(nettverk_Verktøy.informasjonssystemer_FPA_4_protokoll(Ethernet_bilde, 14), "상호통신망규약 4판");
        bekrefte(nettverk_Verktøy.sky_kontrollsum(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 kontrollsum");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        skrive_heltall_VERDI(첫구역, 454, 63);
        skrive_heltall_VERDI(첫구역, 458, 1024);
        bekrefte(new primærpartisjon_tabell().Les(첫구역).size() == 1, "standardverdi 분할 영역표");

        nettverkslag lag_VERDI = new nettverkslag();
        int[] MOTTATT_AVKAST_ANTALL = new int[1];
        lag_VERDI.register_bruker_data_enhet(7, (data, Kjør_2, lengde_VERDI) -> MOTTATT_AVKAST_ANTALL[0]++);
        byte[] bilde_INDEKS = new byte[14 + 20 + 8];
        bilde_INDEKS[12] = 0x08;
        bilde_INDEKS[13] = 0x00;
        bilde_INDEKS[14] = 0x45;
        bilde_INDEKS[16] = 0;
        bilde_INDEKS[17] = 28;
        bilde_INDEKS[23] = 17;
        bilde_INDEKS[36] = 0;
        bilde_INDEKS[37] = 7;
        bekrefte(lag_VERDI.motta_Ethernet(bilde_INDEKS) && MOTTATT_AVKAST_ANTALL[0] == 1, "bruker data enhet_VERDI_7c611f50 distribuere_VERDI");
    }

    private static void test_skjermbilde_OG_Klokke() {
        tegn_vise skjermbilde = new tegn_vise();
        skjermbilde.Utgang("가나\n다");
        bekrefte(skjermbilde.문자(0, 0) == '가' && skjermbilde.문자(0, 1) == '다', "문자 skjermbilde Utgang");
        Klokke Klokke = new Klokke(100);
        for (int INDEKS = 0; INDEKS < 10; INDEKS++) {
            Klokke.틱();
        }
        bekrefte(Klokke.지난밀리초() == 100, "Klokke 틱 KONVERTER_VERDI");
    }

    private static void skrive_heltall_VERDI(byte[] data, int Posisjon, int VERDI) {
        data[Posisjon] = (byte) VERDI;
        data[Posisjon + 1] = (byte) (VERDI >>> 8);
        data[Posisjon + 2] = (byte) (VERDI >>> 16);
        data[Posisjon + 3] = (byte) (VERDI >>> 24);
    }

    private static void 짧은정수쓰기(byte[] data, int Posisjon, int VERDI) {
        data[Posisjon] = (byte) VERDI;
        data[Posisjon + 1] = (byte) (VERDI >>> 8);
    }

    private static void bekrefte(boolean vilkår, String Navn) {
        if (!vilkår) {
            throw new AssertionError("feil_VERDI: " + Navn);
        }
        sende_ANTALL++;
        System.out.println("sende_VERDI: " + Navn);
    }
}
