// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Finland.JFinOS.tester;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Finland.JFinOS.Minne_område.Minne_Ansvarig;
import Finland.JFinOS.Minne_område.Sidhanteraren;
import Finland.JFinOS.indata_värde.inmatningshändelse;
import Finland.JFinOS.작업.Process_värde;
import Finland.JFinOS.systemanrop.systemanrop;
import Finland.JFinOS.filsystem.körbar_fil_inläsare;
import Finland.JFinOS.kärna.kärna;
import Finland.JFinOS.värd.värd_maskinvara;
import Finland.JFinOS.IRQ.IRQ_Ansvarig;
import Finland.JFinOS.서술자.GDT;
import Finland.JFinOS.lagringsenhet.고급기술결합장치;
import Finland.JFinOS.enhet_värde.tillbehör_buss_Ansvarig;
import Finland.JFinOS.nätverk_Stack.nätverk_Verktyg;
import Finland.JFinOS.nätverk_Stack.nätverksnivå;
import Finland.JFinOS.enhet_värde.Klocka;
import Finland.JFinOS.서술자.uppgift_status_segment;
import Finland.JFinOS.skärmbild.tecken_visa;
import Finland.JFinOS.filsystem.primär_partition_tabell;

public final class 전체시험 {
    private static int skicka_ANTAL;

    private 전체시험() {
    }

    public static void main(String[] parameter_argument) {
        värd_maskinvara enhet_värde = new värd_maskinvara();
        kärna kärna_värde = new kärna(enhet_värde);
        kärna_värde.Kör();

        test_Minne(kärna_värde);
        쪽관리시험(kärna_värde);
        파일과과정시험(kärna_värde);
        실행파일시험(kärna_värde);
        test_indata(kärna_värde);
        test_maskinvara(enhet_värde);
        개입중단과서술자시험();
        test_minne_AND_Nätverk();
        test_skärmbild_AND_Klocka();

        System.out.println("JFinOS tester skicka_värde: " + skicka_ANTAL);
    }

    private static void test_Minne(kärna kärna_värde) {
        Minne_Ansvarig Ansvarig_värde = kärna_värde.Minne_område();
        int 첫주소 = Ansvarig_värde.정렬할당(100, 64);
        verifiera((첫주소 & 63) == 0, "justera_värde allokera_minne");
        Ansvarig_värde.skriva_byte_värde(첫주소, (byte) 0x5a);
        verifiera(Ansvarig_värde.läsa_byte_värde(첫주소) == (byte) 0x5a, "물리 Minne_område 읽고 Skriv");
        int 사용전 = Ansvarig_värde.사용크기();
        Ansvarig_värde.släppa_minne(첫주소);
        verifiera(Ansvarig_värde.사용크기() < 사용전, "Minne_område släppa_minne");
    }

    private static void 쪽관리시험(kärna kärna_värde) {
        Sidhanteraren Ansvarig_värde = kärna_värde.쪽관리();
        Sidhanteraren.adressutrymme överordnad_Space = Ansvarig_värde.새주소공간();
        Ansvarig_värde.MAP_page(överordnad_Space, 0x1000, true);
        Ansvarig_värde.skriva_byte_värde(överordnad_Space, 0x1010, (byte) 7);
        Sidhanteraren.adressutrymme barn_Space = Ansvarig_värde.쓰기시복사복제(överordnad_Space);
        Ansvarig_värde.skriva_byte_värde(barn_Space, 0x1010, (byte) 9);
        verifiera(Ansvarig_värde.läsa_byte_värde(överordnad_Space, 0x1010) == 7, "Skriv 시 kopia_värde överordnad_värde 격리");
        verifiera(Ansvarig_värde.läsa_byte_värde(barn_Space, 0x1010) == 9, "Skriv 시 kopia_värde barn_värde Skriv");
    }

    private static void 파일과과정시험(kärna kärna_värde) {
        byte[] Innehåll_värde = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        kärna_värde.filsystem().Lägga_till_fil("tester", Innehåll_värde);
        Process_värde överordnad_värde = kärna_värde.첫과정();
        systemanrop 호출 = kärna_värde.systemanrop();
        int 서술자 = 호출.Öppna(överordnad_värde, "/tester", systemanrop.skrivskyddad_flagga);
        verifiera(서술자 >= 3, "filnamn Öppna");

        byte[] få_mål = new byte[Innehåll_värde.length];
        verifiera(호출.Läs(överordnad_värde, 서술자, få_mål, få_mål.length) == Innehåll_värde.length, "filnamn Läs");
        verifiera(Arrays.equals(Innehåll_värde, få_mål), "filnamn Innehåll_värde");
        verifiera(호출.flytta_placera(överordnad_värde, 서술자, 0, systemanrop.SÖK_START) == 0, "filnamn position flytta_värde");

        int 복제서술자 = 호출.서술자복제(överordnad_värde, 서술자);
        verifiera(복제서술자 >= 0, "서술자 klon_värde");
        Process_värde barn_värde = 호출.klon_Process(överordnad_värde);
        verifiera(barn_värde.identifierare_värde() != överordnad_värde.identifierare_värde(), "Process_värde identifierare_värde 분리");
        verifiera(barn_värde.överordnad_identifierare() == överordnad_värde.identifierare_värde(), "överordnad_värde Process_värde identifierare_värde");
        verifiera(호출.Stäng(barn_värde, 서술자) == 0 && överordnad_värde.파일서술자().informationsteknik_skapa(서술자), "barn_värde Stäng 격리");

        int Föregående_avsluta = 호출.ökning_app_rast(överordnad_värde, 8192);
        verifiera(Föregående_avsluta == 0x06000000, "app_f5044b9b 끝 늘리기");
        verifiera(överordnad_värde.app_rast() == 0x06002000, "app_f5044b9b 끝 반영");
        verifiera(barn_värde.app_rast() == 0x06000000, "과정별 app_f5044b9b 끝 격리");

        barn_värde.Utgång_app(7);
        verifiera(호출.자식기다리기(överordnad_värde, barn_värde.identifierare_värde(), false) == (7 << 8), "barn_värde Utgång_app 기다리기");
        verifiera(호출.접근가능("tester", 1) == -13, "köra_kommando behörighet_värde avvisa_värde");
        verifiera(호출.UID() == 0 && 호출.GID() == 0, "사용자와 무리 identifierare_värde");
        verifiera("/".equals(호출.aktuellt_uppgiftslista(2)) && 호출.byta_uppgiftslista("/") == 0, "aktuellt_objekt 작업 post_ange");
        verifiera(호출.informationsteknik_Terminal(överordnad_värde, 1), "표준 utmatningsposition 단말");
        verifiera("JFinOS".equals(호출.System_Detaljer().System_namn()), "operativsystem_värde msinfo32_exe");
    }

    private static void 실행파일시험(kärna kärna_värde) {
        byte[] data = new byte[92];
        data[0] = 0x7f;
        data[1] = 'E';
        data[2] = 'L';
        data[3] = 'F';
        data[4] = 1;
        data[5] = 1;
        skriva_heltal_värde(data, 24, 0x04001000);
        skriva_heltal_värde(data, 32, 52);
        짧은정수쓰기(data, 46, 40);
        짧은정수쓰기(data, 48, 1);
        skriva_heltal_värde(data, 56, 8);
        skriva_heltal_värde(data, 60, 2);
        skriva_heltal_värde(data, 64, 0x04002000);
        skriva_heltal_värde(data, 72, 64);

        körbar_fil_inläsare.BILD BILD_värde = new körbar_fil_inläsare().검사(data);
        verifiera(BILD_värde.START_ADRESS() == 0x04001000, "ELF Kör Adress");
        verifiera(BILD_värde.구역들().size() == 1 && BILD_värde.구역들().get(0).variant_värde() == 8, "ELF 빈 data avsnitt_värde");
        int 서술자 = kärna_värde.systemanrop().Öppna(kärna_värde.첫과정(), "tester", systemanrop.skrivskyddad_flagga);
        verifiera(kärna_värde.systemanrop().filstyrning(kärna_värde.첫과정(), 서술자, 2, 1) == 0, "köra_kommando 시 Stäng Inställningar");
        verifiera(kärna_värde.systemanrop().köra_kommando(kärna_värde.첫과정(), data, new String[] {"tester", "값"}, new String[] {"Språk=Svenska"}) == 0, "ELF köra_kommando BILD_värde 적재");
        verifiera(kärna_värde.첫과정().körning_START_ADRESS() == 0x04001000, "köra_kommando Kör Adress 반영");
        verifiera(kärna_värde.첫과정().körning_argument().length == 2 && kärna_värde.첫과정().miljö_värde().length == 1, "köra_kommando 인자와 miljö");
        verifiera(!kärna_värde.첫과정().파일서술자().informationsteknik_skapa(서술자), "köra_kommando 시 서술자 Stäng");
        verifiera(kärna_värde.쪽관리().läsa_byte_värde(kärna_värde.첫과정().adressutrymme(), 0x04002000) == 0, "빈 data avsnitt_värde noll_operand starta");
    }

    private static void test_indata(kärna kärna_värde) {
        kärna_värde.입력관리().Nyckel_ur_funktion('가');
        kärna_värde.입력관리().쥐이동(3, -2);
        inmatningshändelse 첫사건 = kärna_värde.입력관리().Nästa_händelse();
        inmatningshändelse SEKUND_händelse = kärna_värde.입력관리().Nästa_händelse();
        verifiera(첫사건.händelsesort() == inmatningshändelse.variant_värde.Nyckel_ur_funktion, "자판 Händelse");
        verifiera(SEKUND_händelse.첫째값() == 3 && SEKUND_händelse.SEKUND_värde() == -2, "쥐 flytta_värde Händelse");
    }

    private static void test_maskinvara(värd_maskinvara enhet_värde) {
        enhet_värde.skriva_port_byte(0x3f8, 0xab);
        verifiera(enhet_värde.läsa_port_byte(0x3f8) == 0xab, "maskinvara_port indata_utleverans gräns_värde");
        verifiera(enhet_värde.직렬기록().contains("JFinOS"), "직렬 LOG_POST");
    }

    private static void 개입중단과서술자시험() {
        IRQ_Ansvarig Ansvarig_värde = new IRQ_Ansvarig();
        Ansvarig_värde.register_post(0x21, minne_ADRESS -> minne_ADRESS + 4);
        Ansvarig_värde.aktivera();
        verifiera(Ansvarig_värde.distribuera_värde(0x21, 100) == 104, "IRQ distribuera_värde");
        Ansvarig_värde.inaktivera();
        verifiera(Ansvarig_värde.distribuera_värde(0x21, 100) == 100, "IRQ inaktivera");

        GDT 서술자표 = new GDT();
        서술자표.uppsättning_standardvärde();
        verifiera(서술자표.조각들().size() == 5, "전역 서술자표");
        uppgift_status_segment uppgift_status = new uppgift_status_segment();
        uppgift_status.특권쌓임공간설정(0x10, 0x800000);
        verifiera(uppgift_status.Stack_noll_block() == 0x10 && uppgift_status.Stack_noll_ADRESS() == 0x800000, "작업 status_värde avsnitt_värde");
    }

    private static void test_minne_AND_Nätverk() {
        고급기술결합장치 lagringsenhet = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.avsnitt_storlek];
        byte[] läsa_data_värde = new byte[고급기술결합장치.avsnitt_storlek];
        쓸자료[17] = 42;
        lagringsenhet.Skriv(2, 쓸자료);
        lagringsenhet.Läs(2, läsa_data_värde);
        verifiera(läsa_data_värde[17] == 42, "ATA avsnitt_värde 읽고 Skriv");

        tillbehör_buss_Ansvarig tillbehör = new tillbehör_buss_Ansvarig();
        tillbehör.발견(new tillbehör_buss_Ansvarig.enhet_värde(0x1022, 0x2000, 0xc000, 11));
        verifiera(tillbehör.Sök_post(0x1022, 0x2000) != null, "주변 enhet_värde Sök_post");

        byte[] Ethernet_ram = new byte[34];
        Ethernet_ram[12] = 0x08;
        Ethernet_ram[13] = 0x00;
        Ethernet_ram[14] = 0x45;
        verifiera(nätverk_Verktyg.Ethernet_VERSALER_protokoll(Ethernet_ram) == 0x0800, "이더넷 상위 kontraktsvärde");
        verifiera(nätverk_Verktyg.informationsteknik_FPV_4_protokoll(Ethernet_ram, 14), "상호통신망규약 4판");
        verifiera(nätverk_Verktyg.nät_kontrollsumma(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 kontrollsumma");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        skriva_heltal_värde(첫구역, 454, 63);
        skriva_heltal_värde(첫구역, 458, 1024);
        verifiera(new primär_partition_tabell().Läs(첫구역).size() == 1, "standardvärde 분할 영역표");

        nätverksnivå nivå_värde = new nätverksnivå();
        int[] BELOPP_ANTAL = new int[1];
        nivå_värde.register_användare_data_enhet(7, (data, Kör, längd_värde) -> BELOPP_ANTAL[0]++);
        byte[] ram_INDEX = new byte[14 + 20 + 8];
        ram_INDEX[12] = 0x08;
        ram_INDEX[13] = 0x00;
        ram_INDEX[14] = 0x45;
        ram_INDEX[16] = 0;
        ram_INDEX[17] = 28;
        ram_INDEX[23] = 17;
        ram_INDEX[36] = 0;
        ram_INDEX[37] = 7;
        verifiera(nivå_värde.få_Ethernet(ram_INDEX) && BELOPP_ANTAL[0] == 1, "användarutrymme data enhet_värde_7c611f50 distribuera_värde");
    }

    private static void test_skärmbild_AND_Klocka() {
        tecken_visa skärmbild = new tecken_visa();
        skärmbild.utmatningsposition("가나\n다");
        verifiera(skärmbild.문자(0, 0) == '가' && skärmbild.문자(0, 1) == '다', "문자 skärmbild utmatningsposition");
        Klocka Klocka = new Klocka(100);
        for (int INDEX = 0; INDEX < 10; INDEX++) {
            Klocka.tick_värde();
        }
        verifiera(Klocka.지난밀리초() == 100, "Klocka tick_värde KONVERTERA_värde");
    }

    private static void skriva_heltal_värde(byte[] data, int position, int värde) {
        data[position] = (byte) värde;
        data[position + 1] = (byte) (värde >>> 8);
        data[position + 2] = (byte) (värde >>> 16);
        data[position + 3] = (byte) (värde >>> 24);
    }

    private static void 짧은정수쓰기(byte[] data, int position, int värde) {
        data[position] = (byte) värde;
        data[position + 1] = (byte) (värde >>> 8);
    }

    private static void verifiera(boolean villkor, String Namn) {
        if (!villkor) {
            throw new AssertionError("fel_värde: " + Namn);
        }
        skicka_ANTAL++;
        System.out.println("skicka_värde: " + Namn);
    }
}
