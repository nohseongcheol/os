// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Espainia.JEspOS.시험;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Espainia.JEspOS.기억공간.Memoria_kudeatzaile;
import Espainia.JEspOS.기억공간.orri_kudeatzaile;
import Espainia.JEspOS.입력.입력사건;
import Espainia.JEspOS.작업.prozesu_balio;
import Espainia.JEspOS.체계호출.체계호출;
import Espainia.JEspOS.fitxategi_sistema.실행파일적재기;
import Espainia.JEspOS.nukleo.nukleo;
import Espainia.JEspOS.Ostalari.호스트하드웨어;
import Espainia.JEspOS.IRQ.IRQ_kudeatzaile;
import Espainia.JEspOS.서술자.전역서술자표;
import Espainia.JEspOS.biltegi_gailu.고급기술결합장치;
import Espainia.JEspOS.gailu_balio.osagarri_bus_kudeatzaile;
import Espainia.JEspOS.sare_pila.sare_Tresnak;
import Espainia.JEspOS.sare_pila.sare_maila;
import Espainia.JEspOS.gailu_balio.erloju;
import Espainia.JEspOS.서술자.ataza_Egoera_segmentu;
import Espainia.JEspOS.화면.karaktere_pantaila;
import Espainia.JEspOS.fitxategi_sistema.기본분할영역표;

public final class 전체시험 {
    private static int pasatu_ZENBATU;

    private 전체시험() {
    }

    public static void main(String[] parametro_arg) {
        호스트하드웨어 gailu_balio = new 호스트하드웨어();
        nukleo nukleo_balio = new nukleo(gailu_balio);
        nukleo_balio.Exekutatu_2();

        기억공간시험(nukleo_balio);
        쪽관리시험(nukleo_balio);
        파일과과정시험(nukleo_balio);
        실행파일시험(nukleo_balio);
        입력시험(nukleo_balio);
        하드웨어시험(gailu_balio);
        개입중단과서술자시험();
        저장장치와통신망시험();
        화면과시계시험();

        System.out.println("JEspOS 시험 pasatu_balio: " + pasatu_ZENBATU);
    }

    private static void 기억공간시험(nukleo nukleo_balio) {
        Memoria_kudeatzaile kudeatzaile_balio = nukleo_balio.기억공간();
        int 첫주소 = kudeatzaile_balio.정렬할당(100, 64);
        egiaztatu((첫주소 & 63) == 0, "lerrokatu_balio esleitu_biltegi");
        kudeatzaile_balio.idatzi_byte_balio(첫주소, (byte) 0x5a);
        egiaztatu(kudeatzaile_balio.바이트읽기(첫주소) == (byte) 0x5a, "물리 기억공간 읽고 Idatzi");
        int 사용전 = kudeatzaile_balio.사용크기();
        kudeatzaile_balio.askatu_biltegi(첫주소);
        egiaztatu(kudeatzaile_balio.사용크기() < 사용전, "기억공간 askatu_biltegi");
    }

    private static void 쪽관리시험(nukleo nukleo_balio) {
        orri_kudeatzaile kudeatzaile_balio = nukleo_balio.쪽관리();
        orri_kudeatzaile.helbide_gune 부모공간 = kudeatzaile_balio.새주소공간();
        kudeatzaile_balio.MAP_orri(부모공간, 0x1000, true);
        kudeatzaile_balio.idatzi_byte_balio(부모공간, 0x1010, (byte) 7);
        orri_kudeatzaile.helbide_gune haur_gune = kudeatzaile_balio.쓰기시복사복제(부모공간);
        kudeatzaile_balio.idatzi_byte_balio(haur_gune, 0x1010, (byte) 9);
        egiaztatu(kudeatzaile_balio.바이트읽기(부모공간, 0x1010) == 7, "Idatzi 시 kopiatu_balio 부모 격리");
        egiaztatu(kudeatzaile_balio.바이트읽기(haur_gune, 0x1010) == 9, "Idatzi 시 kopiatu_balio haur_balio Idatzi");
    }

    private static void 파일과과정시험(nukleo nukleo_balio) {
        byte[] eduki_balio = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        nukleo_balio.fitxategi_sistema().Erantsi_fitxategi("시험", eduki_balio);
        prozesu_balio 부모 = nukleo_balio.첫과정();
        체계호출 호출 = nukleo_balio.체계호출();
        int 서술자 = 호출.Ireki(부모, "/시험", 체계호출.irakurtzeko_soilik_marka);
        egiaztatu(서술자 >= 3, "Fitxategia Ireki");

        byte[] 받을곳 = new byte[eduki_balio.length];
        egiaztatu(호출.Irakurri(부모, 서술자, 받을곳, 받을곳.length) == eduki_balio.length, "Fitxategia Irakurri");
        egiaztatu(Arrays.equals(eduki_balio, 받을곳), "Fitxategia eduki_balio");
        egiaztatu(호출.eraman_kargu(부모, 서술자, 0, 체계호출.BILATU_HASI) == 0, "Fitxategia Posizioa eraman_balio");

        int 복제서술자 = 호출.서술자복제(부모, 서술자);
        egiaztatu(복제서술자 >= 0, "서술자 klon_balio");
        prozesu_balio haur_balio = 호출.klon_prozesu(부모);
        egiaztatu(haur_balio.identifikatzaile_balio() != 부모.identifikatzaile_balio(), "prozesu_balio identifikatzaile_balio 분리");
        egiaztatu(haur_balio.부모식별자() == 부모.identifikatzaile_balio(), "부모 prozesu_balio identifikatzaile_balio");
        egiaztatu(호출.Itxi(haur_balio, 서술자) == 0 && 부모.파일서술자().informatika_ireki(서술자), "haur_balio Itxi 격리");

        int 이전끝 = 호출.프로그램끝늘리기(부모, 8192);
        egiaztatu(이전끝 == 0x06000000, "aplik_f5044b9b 끝 늘리기");
        egiaztatu(부모.aplik_atseden() == 0x06002000, "aplik_f5044b9b 끝 반영");
        egiaztatu(haur_balio.aplik_atseden() == 0x06000000, "과정별 aplik_f5044b9b 끝 격리");

        haur_balio.irten_aplik(7);
        egiaztatu(호출.자식기다리기(부모, haur_balio.identifikatzaile_balio(), false) == (7 << 8), "haur_balio irten_aplik 기다리기");
        egiaztatu(호출.접근가능("시험", 1) == -13, "exekutatu_komando baimen_balio baztertu_balio");
        egiaztatu(호출.erabiltzaile_ID() == 0 && 호출.talde_identifikatzaile() == 0, "사용자와 무리 identifikatzaile_balio");
        egiaztatu("/".equals(호출.현재작업목록(2)) && 호출.ALDATU_zeregin_zerrenda("/") == 0, "현재 작업 sarrera_Zerrenda");
        egiaztatu(호출.informatika_Terminal(부모, 1), "표준 Irteera 단말");
        egiaztatu("JEspOS".equals(호출.sistema_Xehetasunak().sistema_izen()), "sistema_eragile_balio msinfo32_exe");
    }

    private static void 실행파일시험(nukleo nukleo_balio) {
        byte[] datuak = new byte[92];
        datuak[0] = 0x7f;
        datuak[1] = 'E';
        datuak[2] = 'L';
        datuak[3] = 'F';
        datuak[4] = 1;
        datuak[5] = 1;
        idatzi_osoko_zenbaki_balio(datuak, 24, 0x04001000);
        idatzi_osoko_zenbaki_balio(datuak, 32, 52);
        짧은정수쓰기(datuak, 46, 40);
        짧은정수쓰기(datuak, 48, 1);
        idatzi_osoko_zenbaki_balio(datuak, 56, 8);
        idatzi_osoko_zenbaki_balio(datuak, 60, 2);
        idatzi_osoko_zenbaki_balio(datuak, 64, 0x04002000);
        idatzi_osoko_zenbaki_balio(datuak, 72, 64);

        실행파일적재기.irudi irudi_balio = new 실행파일적재기().검사(datuak);
        egiaztatu(irudi_balio.HASI_helbide() == 0x04001000, "ELF Exekutatu_2 helbide");
        egiaztatu(irudi_balio.구역들().size() == 1 && irudi_balio.구역들().get(0).종류() == 8, "ELF 빈 datuak sekzio_balio");
        int 서술자 = nukleo_balio.체계호출().Ireki(nukleo_balio.첫과정(), "시험", 체계호출.irakurtzeko_soilik_marka);
        egiaztatu(nukleo_balio.체계호출().fitxategi_kontrol(nukleo_balio.첫과정(), 서술자, 2, 1) == 0, "exekutatu_komando 시 Itxi Ezarpenak");
        egiaztatu(nukleo_balio.체계호출().exekutatu_komando(nukleo_balio.첫과정(), datuak, new String[] {"시험", "값"}, new String[] {"Hizkuntza=Euskara"}) == 0, "ELF exekutatu_komando irudi_balio 적재");
        egiaztatu(nukleo_balio.첫과정().실행시작주소() == 0x04001000, "exekutatu_komando Exekutatu_2 helbide 반영");
        egiaztatu(nukleo_balio.첫과정().실행인자().length == 2 && nukleo_balio.첫과정().환경값().length == 1, "exekutatu_komando 인자와 환경");
        egiaztatu(!nukleo_balio.첫과정().파일서술자().informatika_ireki(서술자), "exekutatu_komando 시 서술자 Itxi");
        egiaztatu(nukleo_balio.쪽관리().바이트읽기(nukleo_balio.첫과정().helbide_gune(), 0x04002000) == 0, "빈 datuak sekzio_balio 영 hasieratu");
    }

    private static void 입력시험(nukleo nukleo_balio) {
        nukleo_balio.입력관리().키누름('가');
        nukleo_balio.입력관리().쥐이동(3, -2);
        입력사건 첫사건 = nukleo_balio.입력관리().Hurrengoa_gertaera();
        입력사건 SEGUNDOA_gertaera = nukleo_balio.입력관리().Hurrengoa_gertaera();
        egiaztatu(첫사건.사건종류() == 입력사건.종류.키누름, "자판 Gertaera");
        egiaztatu(SEGUNDOA_gertaera.첫째값() == 3 && SEGUNDOA_gertaera.SEGUNDOA_balio() == -2, "쥐 eraman_balio Gertaera");
    }

    private static void 하드웨어시험(호스트하드웨어 gailu_balio) {
        gailu_balio.idatzi_ataka_byte(0x3f8, 0xab);
        egiaztatu(gailu_balio.포트바이트읽기(0x3f8) == 0xab, "포트 S_I 경계");
        egiaztatu(gailu_balio.직렬기록().contains("JEspOS"), "직렬 LOG_marka");
    }

    private static void 개입중단과서술자시험() {
        IRQ_kudeatzaile kudeatzaile_balio = new IRQ_kudeatzaile();
        kudeatzaile_balio.izena_eman_sarrera(0x21, biltegi_helbide -> biltegi_helbide + 4);
        kudeatzaile_balio.gaitu();
        egiaztatu(kudeatzaile_balio.banatu_balio(0x21, 100) == 104, "IRQ banatu_balio");
        kudeatzaile_balio.desaktibatu();
        egiaztatu(kudeatzaile_balio.banatu_balio(0x21, 100) == 100, "IRQ desaktibatu");

        전역서술자표 서술자표 = new 전역서술자표();
        서술자표.sorta_balio_lehenetsi();
        egiaztatu(서술자표.조각들().size() == 5, "전역 서술자표");
        ataza_Egoera_segmentu ataza_Egoera = new ataza_Egoera_segmentu();
        ataza_Egoera.특권쌓임공간설정(0x10, 0x800000);
        egiaztatu(ataza_Egoera.영번쌓임조각() == 0x10 && ataza_Egoera.영번쌓임주소() == 0x800000, "작업 Egoera_balio sekzio_balio");
    }

    private static void 저장장치와통신망시험() {
        고급기술결합장치 biltegi_gailu = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.구역크기];
        byte[] 읽은자료 = new byte[고급기술결합장치.구역크기];
        쓸자료[17] = 42;
        biltegi_gailu.Idatzi(2, 쓸자료);
        biltegi_gailu.Irakurri(2, 읽은자료);
        egiaztatu(읽은자료[17] == 42, "ATA sekzio_balio 읽고 Idatzi");

        osagarri_bus_kudeatzaile osagarri = new osagarri_bus_kudeatzaile();
        osagarri.발견(new osagarri_bus_kudeatzaile.gailu_balio(0x1022, 0x2000, 0xc000, 11));
        egiaztatu(osagarri.Bilatu_sarrera(0x1022, 0x2000) != null, "주변 gailu_balio Bilatu_sarrera");

        byte[] Ethernet_marko = new byte[34];
        Ethernet_marko[12] = 0x08;
        Ethernet_marko[13] = 0x00;
        Ethernet_marko[14] = 0x45;
        egiaztatu(sare_Tresnak.Ethernet_MAIUSKULA_protokolo(Ethernet_marko) == 0x0800, "이더넷 상위 kasu_balio");
        egiaztatu(sare_Tresnak.상호통신망규약사판인가(Ethernet_marko, 14), "상호통신망규약 4판");
        egiaztatu(sare_Tresnak.hodei_kontroleko_batura(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 kontroleko_batura");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        idatzi_osoko_zenbaki_balio(첫구역, 454, 63);
        idatzi_osoko_zenbaki_balio(첫구역, 458, 1024);
        egiaztatu(new 기본분할영역표().Irakurri(첫구역).size() == 1, "balio_lehenetsi 분할 영역표");

        sare_maila maila_balio = new sare_maila();
        int[] RECEIVED_ZENBATU = new int[1];
        maila_balio.izena_eman_erabiltzaile_datuak_unitate(7, (datuak, Exekutatu_2, luzera_balio) -> RECEIVED_ZENBATU[0]++);
        byte[] marko_INDIZE = new byte[14 + 20 + 8];
        marko_INDIZE[12] = 0x08;
        marko_INDIZE[13] = 0x00;
        marko_INDIZE[14] = 0x45;
        marko_INDIZE[16] = 0;
        marko_INDIZE[17] = 28;
        marko_INDIZE[23] = 17;
        marko_INDIZE[36] = 0;
        marko_INDIZE[37] = 7;
        egiaztatu(maila_balio.이더넷받기(marko_INDIZE) && RECEIVED_ZENBATU[0] == 1, "erabiltzaile datuak unitate_balio banatu_balio");
    }

    private static void 화면과시계시험() {
        karaktere_pantaila 화면 = new karaktere_pantaila();
        화면.Irteera("가나\n다");
        egiaztatu(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 Irteera");
        erloju erloju = new erloju(100);
        for (int INDIZE = 0; INDIZE < 10; INDIZE++) {
            erloju.틱();
        }
        egiaztatu(erloju.지난밀리초() == 100, "erloju 틱 BIHURTU_balio");
    }

    private static void idatzi_osoko_zenbaki_balio(byte[] datuak, int Posizioa, int balio) {
        datuak[Posizioa] = (byte) balio;
        datuak[Posizioa + 1] = (byte) (balio >>> 8);
        datuak[Posizioa + 2] = (byte) (balio >>> 16);
        datuak[Posizioa + 3] = (byte) (balio >>> 24);
    }

    private static void 짧은정수쓰기(byte[] datuak, int Posizioa, int balio) {
        datuak[Posizioa] = (byte) balio;
        datuak[Posizioa + 1] = (byte) (balio >>> 8);
    }

    private static void egiaztatu(boolean baldintza, String Izena) {
        if (!baldintza) {
            throw new AssertionError("hutsegite_balio: " + Izena);
        }
        pasatu_ZENBATU++;
        System.out.println("pasatu_balio: " + Izena);
    }
}
