// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Tyskland.JDeuOS.시험;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Tyskland.JDeuOS.Hukommelse_område.Hukommelse_Leder;
import Tyskland.JDeuOS.Hukommelse_område.Sidestyring;
import Tyskland.JDeuOS.input_VÆRDI.inputhændelse;
import Tyskland.JDeuOS.작업.Proces_VÆRDI;
import Tyskland.JDeuOS.체계호출.체계호출;
import Tyskland.JDeuOS.filsystem.eksekverbar_fil_indlæsningsfunktion;
import Tyskland.JDeuOS.kerne.kerne;
import Tyskland.JDeuOS.vært.vært_hardware;
import Tyskland.JDeuOS.IRQ.IRQ_Leder;
import Tyskland.JDeuOS.서술자.전역서술자표;
import Tyskland.JDeuOS.lagerenhed.고급기술결합장치;
import Tyskland.JDeuOS.enhed_VÆRDI.tilbehør_bus_Leder;
import Tyskland.JDeuOS.netværk_Stak.netværk_Værktøjer;
import Tyskland.JDeuOS.netværk_Stak.netværkslag;
import Tyskland.JDeuOS.enhed_VÆRDI.Ur;
import Tyskland.JDeuOS.서술자.job_status_segment;
import Tyskland.JDeuOS.skærmbillede.tegn_vise;
import Tyskland.JDeuOS.filsystem.primær_partition_tabel;

public final class 전체시험 {
    private static int videregive_TÆL;

    private 전체시험() {
    }

    public static void main(String[] parameter_argument) {
        vært_hardware enhed_VÆRDI = new vært_hardware();
        kerne kerne_VÆRDI = new kerne(enhed_VÆRDI);
        kerne_VÆRDI.Kør_2();

        test_Hukommelse(kerne_VÆRDI);
        쪽관리시험(kerne_VÆRDI);
        파일과과정시험(kerne_VÆRDI);
        실행파일시험(kerne_VÆRDI);
        test_input(kerne_VÆRDI);
        test_hardware(enhed_VÆRDI);
        개입중단과서술자시험();
        test_Lager_OG_Netværk();
        test_skærmbillede_OG_Ur();

        System.out.println("JDeuOS 시험 videregive_VÆRDI: " + videregive_TÆL);
    }

    private static void test_Hukommelse(kerne kerne_VÆRDI) {
        Hukommelse_Leder Leder_VÆRDI = kerne_VÆRDI.Hukommelse_område();
        int 첫주소 = Leder_VÆRDI.정렬할당(100, 64);
        bekræfte((첫주소 & 63) == 0, "justere_VÆRDI tildel_Lager");
        Leder_VÆRDI.skrive_byte_VÆRDI(첫주소, (byte) 0x5a);
        bekræfte(Leder_VÆRDI.바이트읽기(첫주소) == (byte) 0x5a, "물리 Hukommelse_område 읽고 Skrive");
        int 사용전 = Leder_VÆRDI.사용크기();
        Leder_VÆRDI.udgive_Lager(첫주소);
        bekræfte(Leder_VÆRDI.사용크기() < 사용전, "Hukommelse_område udgive_Lager");
    }

    private static void 쪽관리시험(kerne kerne_VÆRDI) {
        Sidestyring Leder_VÆRDI = kerne_VÆRDI.쪽관리();
        Sidestyring.adresseinterval overordnet_Space = Leder_VÆRDI.새주소공간();
        Leder_VÆRDI.MAP_side(overordnet_Space, 0x1000, true);
        Leder_VÆRDI.skrive_byte_VÆRDI(overordnet_Space, 0x1010, (byte) 7);
        Sidestyring.adresseinterval barn_Space = Leder_VÆRDI.쓰기시복사복제(overordnet_Space);
        Leder_VÆRDI.skrive_byte_VÆRDI(barn_Space, 0x1010, (byte) 9);
        bekræfte(Leder_VÆRDI.바이트읽기(overordnet_Space, 0x1010) == 7, "Skrive 시 kopiere_VÆRDI overordnet_VÆRDI 격리");
        bekræfte(Leder_VÆRDI.바이트읽기(barn_Space, 0x1010) == 9, "Skrive 시 kopiere_VÆRDI barn_VÆRDI Skrive");
    }

    private static void 파일과과정시험(kerne kerne_VÆRDI) {
        byte[] Indhold_VÆRDI = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        kerne_VÆRDI.filsystem().tilføj_fil("시험", Indhold_VÆRDI);
        Proces_VÆRDI overordnet_VÆRDI = kerne_VÆRDI.첫과정();
        체계호출 호출 = kerne_VÆRDI.체계호출();
        int 서술자 = 호출.Åbn(overordnet_VÆRDI, "/시험", 체계호출.skrivebeskyttet_flag);
        bekræfte(서술자 >= 3, "Fil Åbn");

        byte[] modtage_destination = new byte[Indhold_VÆRDI.length];
        bekræfte(호출.Læse(overordnet_VÆRDI, 서술자, modtage_destination, modtage_destination.length) == Indhold_VÆRDI.length, "Fil Læse");
        bekræfte(Arrays.equals(Indhold_VÆRDI, modtage_destination), "Fil Indhold_VÆRDI");
        bekræfte(호출.flytte_placere(overordnet_VÆRDI, 서술자, 0, 체계호출.SØG_START) == 0, "Fil Placering flytte_VÆRDI_83b651b8");

        int 복제서술자 = 호출.서술자복제(overordnet_VÆRDI, 서술자);
        bekræfte(복제서술자 >= 0, "서술자 klon_VÆRDI");
        Proces_VÆRDI barn_VÆRDI = 호출.klon_Proces(overordnet_VÆRDI);
        bekræfte(barn_VÆRDI.identifikator_VÆRDI() != overordnet_VÆRDI.identifikator_VÆRDI(), "Proces_VÆRDI identifikator_VÆRDI 분리");
        bekræfte(barn_VÆRDI.overordnet_identifikator() == overordnet_VÆRDI.identifikator_VÆRDI(), "overordnet_VÆRDI Proces_VÆRDI identifikator_VÆRDI");
        bekræfte(호출.Luk(barn_VÆRDI, 서술자) == 0 && overordnet_VÆRDI.파일서술자().it_åben(서술자), "barn_VÆRDI Luk 격리");

        int Forrige_afslutte_et_opkald = 호출.forøgelse_app_pause(overordnet_VÆRDI, 8192);
        bekræfte(Forrige_afslutte_et_opkald == 0x06000000, "app_f5044b9b 끝 늘리기");
        bekræfte(overordnet_VÆRDI.app_pause() == 0x06002000, "app_f5044b9b 끝 반영");
        bekræfte(barn_VÆRDI.app_pause() == 0x06000000, "과정별 app_f5044b9b 끝 격리");

        barn_VÆRDI.Afslut_app(7);
        bekræfte(호출.자식기다리기(overordnet_VÆRDI, barn_VÆRDI.identifikator_VÆRDI(), false) == (7 << 8), "barn_VÆRDI Afslut_app 기다리기");
        bekræfte(호출.접근가능("시험", 1) == -13, "Udfør_kommando rettighed_VÆRDI afvise_VÆRDI");
        bekræfte(호출.UID() == 0 && 호출.gruppe_identifikator() == 0, "사용자와 무리 identifikator_VÆRDI");
        bekræfte("/".equals(호출.aktuel_Opgaveliste(2)) && 호출.SKIFT_Opgaveliste("/") == 0, "aktuel_vare 작업 post_Liste");
        bekræfte(호출.it_Terminal(overordnet_VÆRDI, 1), "표준 Udgang 단말");
        bekræfte("JDeuOS".equals(호출.System_Detaljer().System_navn()), "operativsystem_VÆRDI msinfo32_exe");
    }

    private static void 실행파일시험(kerne kerne_VÆRDI) {
        byte[] data = new byte[92];
        data[0] = 0x7f;
        data[1] = 'E';
        data[2] = 'L';
        data[3] = 'F';
        data[4] = 1;
        data[5] = 1;
        skrive_heltal_VÆRDI(data, 24, 0x04001000);
        skrive_heltal_VÆRDI(data, 32, 52);
        짧은정수쓰기(data, 46, 40);
        짧은정수쓰기(data, 48, 1);
        skrive_heltal_VÆRDI(data, 56, 8);
        skrive_heltal_VÆRDI(data, 60, 2);
        skrive_heltal_VÆRDI(data, 64, 0x04002000);
        skrive_heltal_VÆRDI(data, 72, 64);

        eksekverbar_fil_indlæsningsfunktion.Image Image_VÆRDI = new eksekverbar_fil_indlæsningsfunktion().검사(data);
        bekræfte(Image_VÆRDI.START_mail() == 0x04001000, "ELF Kør_2 mail");
        bekræfte(Image_VÆRDI.구역들().size() == 1 && Image_VÆRDI.구역들().get(0).종류() == 8, "ELF 빈 data sektion_VÆRDI");
        int 서술자 = kerne_VÆRDI.체계호출().Åbn(kerne_VÆRDI.첫과정(), "시험", 체계호출.skrivebeskyttet_flag);
        bekræfte(kerne_VÆRDI.체계호출().fil_kontrol(kerne_VÆRDI.첫과정(), 서술자, 2, 1) == 0, "Udfør_kommando 시 Luk Indstillinger");
        bekræfte(kerne_VÆRDI.체계호출().Udfør_kommando(kerne_VÆRDI.첫과정(), data, new String[] {"시험", "값"}, new String[] {"Sprog=Dansk"}) == 0, "ELF Udfør_kommando Image_VÆRDI 적재");
        bekræfte(kerne_VÆRDI.첫과정().udførelse_START_mail() == 0x04001000, "Udfør_kommando Kør_2 mail 반영");
        bekræfte(kerne_VÆRDI.첫과정().udførelse_argument().length == 2 && kerne_VÆRDI.첫과정().miljø_VÆRDI().length == 1, "Udfør_kommando 인자와 miljø");
        bekræfte(!kerne_VÆRDI.첫과정().파일서술자().it_åben(서술자), "Udfør_kommando 시 서술자 Luk");
        bekræfte(kerne_VÆRDI.쪽관리().바이트읽기(kerne_VÆRDI.첫과정().adresseinterval(), 0x04002000) == 0, "빈 data sektion_VÆRDI nul_operand starte");
    }

    private static void test_input(kerne kerne_VÆRDI) {
        kerne_VÆRDI.입력관리().tast_nede('가');
        kerne_VÆRDI.입력관리().쥐이동(3, -2);
        inputhændelse 첫사건 = kerne_VÆRDI.입력관리().Næste_hændelse();
        inputhændelse SEKUND_hændelse = kerne_VÆRDI.입력관리().Næste_hændelse();
        bekræfte(첫사건.hændelsestype() == inputhændelse.종류.tast_nede, "자판 hændelse");
        bekræfte(SEKUND_hændelse.첫째값() == 3 && SEKUND_hændelse.SEKUND_VÆRDI() == -2, "쥐 flytte_VÆRDI_83b651b8 hændelse");
    }

    private static void test_hardware(vært_hardware enhed_VÆRDI) {
        enhed_VÆRDI.skrive_port_byte(0x3f8, 0xab);
        bekræfte(enhed_VÆRDI.포트바이트읽기(0x3f8) == 0xab, "hardware_port I_O grænse_VÆRDI");
        bekræfte(enhed_VÆRDI.직렬기록().contains("JDeuOS"), "직렬 LOG_post");
    }

    private static void 개입중단과서술자시험() {
        IRQ_Leder Leder_VÆRDI = new IRQ_Leder();
        Leder_VÆRDI.register_post(0x21, Lager_mail -> Lager_mail + 4);
        Leder_VÆRDI.slå_til();
        bekræfte(Leder_VÆRDI.fordele_VÆRDI(0x21, 100) == 104, "IRQ fordele_VÆRDI");
        Leder_VÆRDI.deaktivere();
        bekræfte(Leder_VÆRDI.fordele_VÆRDI(0x21, 100) == 100, "IRQ deaktivere");

        전역서술자표 서술자표 = new 전역서술자표();
        서술자표.sæt_standardværdi();
        bekræfte(서술자표.조각들().size() == 5, "전역 서술자표");
        job_status_segment job_status = new job_status_segment();
        job_status.특권쌓임공간설정(0x10, 0x800000);
        bekræfte(job_status.Stak_nul_blok() == 0x10 && job_status.Stak_nul_mail() == 0x800000, "작업 status_VÆRDI sektion_VÆRDI");
    }

    private static void test_Lager_OG_Netværk() {
        고급기술결합장치 lagerenhed = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.sektion_tilpasse_størrelse];
        byte[] 읽은자료 = new byte[고급기술결합장치.sektion_tilpasse_størrelse];
        쓸자료[17] = 42;
        lagerenhed.Skrive(2, 쓸자료);
        lagerenhed.Læse(2, 읽은자료);
        bekræfte(읽은자료[17] == 42, "ATA sektion_VÆRDI 읽고 Skrive");

        tilbehør_bus_Leder tilbehør = new tilbehør_bus_Leder();
        tilbehør.발견(new tilbehør_bus_Leder.enhed_VÆRDI(0x1022, 0x2000, 0xc000, 11));
        bekræfte(tilbehør.Søg_post(0x1022, 0x2000) != null, "주변 enhed_VÆRDI Søg_post");

        byte[] Ethernet_ramme = new byte[34];
        Ethernet_ramme[12] = 0x08;
        Ethernet_ramme[13] = 0x00;
        Ethernet_ramme[14] = 0x45;
        bekræfte(netværk_Værktøjer.Ethernet_STORE_BOGSTAVER_protokol(Ethernet_ramme) == 0x0800, "이더넷 상위 kontraktværdi");
        bekræfte(netværk_Værktøjer.it_IPV_4_protokol(Ethernet_ramme, 14), "상호통신망규약 4판");
        bekræfte(netværk_Værktøjer.net_kontrolsum(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 kontrolsum");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        skrive_heltal_VÆRDI(첫구역, 454, 63);
        skrive_heltal_VÆRDI(첫구역, 458, 1024);
        bekræfte(new primær_partition_tabel().Læse(첫구역).size() == 1, "standardværdi 분할 영역표");

        netværkslag lag_VÆRDI = new netværkslag();
        int[] MODTAGET_VED_UDLØB_TÆL = new int[1];
        lag_VÆRDI.register_bruger_data_enhed(7, (data, Kør_2, varighed_VÆRDI) -> MODTAGET_VED_UDLØB_TÆL[0]++);
        byte[] ramme_INDEKS = new byte[14 + 20 + 8];
        ramme_INDEKS[12] = 0x08;
        ramme_INDEKS[13] = 0x00;
        ramme_INDEKS[14] = 0x45;
        ramme_INDEKS[16] = 0;
        ramme_INDEKS[17] = 28;
        ramme_INDEKS[23] = 17;
        ramme_INDEKS[36] = 0;
        ramme_INDEKS[37] = 7;
        bekræfte(lag_VÆRDI.modtage_Ethernet(ramme_INDEKS) && MODTAGET_VED_UDLØB_TÆL[0] == 1, "bruger data enhed_VÆRDI_7c611f50 fordele_VÆRDI");
    }

    private static void test_skærmbillede_OG_Ur() {
        tegn_vise skærmbillede = new tegn_vise();
        skærmbillede.Udgang("가나\n다");
        bekræfte(skærmbillede.문자(0, 0) == '가' && skærmbillede.문자(0, 1) == '다', "문자 skærmbillede Udgang");
        Ur Ur = new Ur(100);
        for (int INDEKS = 0; INDEKS < 10; INDEKS++) {
            Ur.tik_VÆRDI();
        }
        bekræfte(Ur.지난밀리초() == 100, "Ur tik_VÆRDI KONVERTER_VÆRDI");
    }

    private static void skrive_heltal_VÆRDI(byte[] data, int Placering, int VÆRDI) {
        data[Placering] = (byte) VÆRDI;
        data[Placering + 1] = (byte) (VÆRDI >>> 8);
        data[Placering + 2] = (byte) (VÆRDI >>> 16);
        data[Placering + 3] = (byte) (VÆRDI >>> 24);
    }

    private static void 짧은정수쓰기(byte[] data, int Placering, int VÆRDI) {
        data[Placering] = (byte) VÆRDI;
        data[Placering + 1] = (byte) (VÆRDI >>> 8);
    }

    private static void bekræfte(boolean lidelse, String Navn) {
        if (!lidelse) {
            throw new AssertionError("fejl_VÆRDI: " + Navn);
        }
        videregive_TÆL++;
        System.out.println("videregive_VÆRDI: " + Navn);
    }
}
