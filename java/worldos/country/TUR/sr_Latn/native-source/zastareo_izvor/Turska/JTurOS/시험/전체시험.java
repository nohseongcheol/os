// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Turska.JTurOS.시험;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Turska.JTurOS.Memorija_oblast.Memorija_menadžer;
import Turska.JTurOS.Memorija_oblast.stranica_menadžer;
import Turska.JTurOS.입력.입력사건;
import Turska.JTurOS.작업.Proces_VALUE;
import Turska.JTurOS.체계호출.체계호출;
import Turska.JTurOS.sistem_datoteka.실행파일적재기;
import Turska.JTurOS.jezgro.jezgro;
import Turska.JTurOS.host.호스트하드웨어;
import Turska.JTurOS.IRQ.IRQ_menadžer;
import Turska.JTurOS.서술자.전역서술자표;
import Turska.JTurOS.uređaj_za_skladištenje.고급기술결합장치;
import Turska.JTurOS.uređaj_VALUE.periferijski_uređaj_magistrala_menadžer;
import Turska.JTurOS.Mreža_stek.Mreža_Alatke;
import Turska.JTurOS.Mreža_stek.sloj_mreže;
import Turska.JTurOS.uređaj_VALUE.Sat;
import Turska.JTurOS.서술자.obaveza_Status_segment;
import Turska.JTurOS.화면.znak_ekran;
import Turska.JTurOS.sistem_datoteka.primarna_particija_tabela;

public final class 전체시험 {
    private static int prebaciti_COUNT;

    private 전체시험() {
    }

    public static void main(String[] parametar_argument) {
        호스트하드웨어 uređaj_VALUE = new 호스트하드웨어();
        jezgro jezgro_VALUE = new jezgro(uređaj_VALUE);
        jezgro_VALUE.koristiti();

        기억공간시험(jezgro_VALUE);
        쪽관리시험(jezgro_VALUE);
        파일과과정시험(jezgro_VALUE);
        실행파일시험(jezgro_VALUE);
        입력시험(jezgro_VALUE);
        하드웨어시험(uređaj_VALUE);
        개입중단과서술자시험();
        저장장치와통신망시험();
        화면과시계시험();

        System.out.println("JTurOS 시험 prebaciti_VALUE: " + prebaciti_COUNT);
    }

    private static void 기억공간시험(jezgro jezgro_VALUE) {
        Memorija_menadžer menadžer_VALUE = jezgro_VALUE.Memorija_oblast();
        int 첫주소 = menadžer_VALUE.정렬할당(100, 64);
        verifikovati((첫주소 & 63) == 0, "poravnati_VALUE dodeliti_Skladište");
        menadžer_VALUE.바이트쓰기(첫주소, (byte) 0x5a);
        verifikovati(menadžer_VALUE.바이트읽기(첫주소) == (byte) 0x5a, "물리 Memorija_oblast 읽고 쓰기");
        int 사용전 = menadžer_VALUE.사용크기();
        menadžer_VALUE.izdanje_Skladište(첫주소);
        verifikovati(menadžer_VALUE.사용크기() < 사용전, "Memorija_oblast izdanje_Skladište");
    }

    private static void 쪽관리시험(jezgro jezgro_VALUE) {
        stranica_menadžer menadžer_VALUE = jezgro_VALUE.쪽관리();
        stranica_menadžer.adresa_prostor nadređen_prostor = menadžer_VALUE.새주소공간();
        menadžer_VALUE.MAP_stranica(nadređen_prostor, 0x1000, true);
        menadžer_VALUE.바이트쓰기(nadređen_prostor, 0x1010, (byte) 7);
        stranica_menadžer.adresa_prostor dete_prostor = menadžer_VALUE.쓰기시복사복제(nadređen_prostor);
        menadžer_VALUE.바이트쓰기(dete_prostor, 0x1010, (byte) 9);
        verifikovati(menadžer_VALUE.바이트읽기(nadređen_prostor, 0x1010) == 7, "쓰기 시 instanca_VALUE nadređen_VALUE 격리");
        verifikovati(menadžer_VALUE.바이트읽기(dete_prostor, 0x1010) == 9, "쓰기 시 instanca_VALUE dete_VALUE 쓰기");
    }

    private static void 파일과과정시험(jezgro jezgro_VALUE) {
        byte[] Sadržaj_VALUE = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        jezgro_VALUE.sistem_datoteka().dodati_Datoteka("시험", Sadržaj_VALUE);
        Proces_VALUE nadređen_VALUE = jezgro_VALUE.첫과정();
        체계호출 호출 = jezgro_VALUE.체계호출();
        int 서술자 = 호출.otvoren(nadređen_VALUE, "/시험", 체계호출.samo_za_čitanje_zastavica);
        verifikovati(서술자 >= 3, "Datoteka otvoren");

        byte[] primiti_odredište = new byte[Sadržaj_VALUE.length];
        verifikovati(호출.읽기(nadređen_VALUE, 서술자, primiti_odredište, primiti_odredište.length) == Sadržaj_VALUE.length, "Datoteka 읽기");
        verifikovati(Arrays.equals(Sadržaj_VALUE, primiti_odredište), "Datoteka Sadržaj_VALUE");
        verifikovati(호출.premestiti_pozicija(nadređen_VALUE, 서술자, 0, 체계호출.SEARCH_START) == 0, "Datoteka pozicija premestiti_VALUE");

        int 복제서술자 = 호출.서술자복제(nadređen_VALUE, 서술자);
        verifikovati(복제서술자 >= 0, "서술자 klon_VALUE");
        Proces_VALUE dete_VALUE = 호출.klon_Proces(nadređen_VALUE);
        verifikovati(dete_VALUE.identifikator_VALUE() != nadređen_VALUE.identifikator_VALUE(), "Proces_VALUE identifikator_VALUE 분리");
        verifikovati(dete_VALUE.nadređen_identifikator() == nadređen_VALUE.identifikator_VALUE(), "nadređen_VALUE Proces_VALUE identifikator_VALUE");
        verifikovati(호출.Zatvori(dete_VALUE, 서술자) == 0 && nadređen_VALUE.파일서술자().informatičko_odeljenje_otvoren(서술자), "dete_VALUE Zatvori 격리");

        int 이전끝 = 호출.povećanje_program_pauza(nadređen_VALUE, 8192);
        verifikovati(이전끝 == 0x06000000, "program_f5044b9b 끝 늘리기");
        verifikovati(nadređen_VALUE.program_pauza() == 0x06002000, "program_f5044b9b 끝 반영");
        verifikovati(dete_VALUE.program_pauza() == 0x06000000, "과정별 program_f5044b9b 끝 격리");

        dete_VALUE.Izađi_program(7);
        verifikovati(호출.자식기다리기(nadređen_VALUE, dete_VALUE.identifikator_VALUE(), false) == (7 << 8), "dete_VALUE Izađi_program 기다리기");
        verifikovati(호출.접근가능("시험", 1) == -13, "Izvrši_komanda dozvola_VALUE odbaciti_VALUE_e3ecc00b");
        verifikovati(호출.UID() == 0 && 호출.Grupa_identifikator() == 0, "사용자와 무리 identifikator_VALUE");
        verifikovati("/".equals(호출.aktuelno_lista_zadataka(2)) && 호출.SWITCH_lista_zadataka("/") == 0, "aktuelno_stavka 작업 stavka_Lista");
        verifikovati(호출.informatičko_odeljenje_Terminal(nadređen_VALUE, 1), "표준 출력 단말");
        verifikovati("JTurOS".equals(호출.sistem_Detalji().sistem_ime()), "operativni_sistem_VALUE msinfo32_exe");
    }

    private static void 실행파일시험(jezgro jezgro_VALUE) {
        byte[] podaci = new byte[92];
        podaci[0] = 0x7f;
        podaci[1] = 'E';
        podaci[2] = 'L';
        podaci[3] = 'F';
        podaci[4] = 1;
        podaci[5] = 1;
        정수쓰기(podaci, 24, 0x04001000);
        정수쓰기(podaci, 32, 52);
        짧은정수쓰기(podaci, 46, 40);
        짧은정수쓰기(podaci, 48, 1);
        정수쓰기(podaci, 56, 8);
        정수쓰기(podaci, 60, 2);
        정수쓰기(podaci, 64, 0x04002000);
        정수쓰기(podaci, 72, 64);

        실행파일적재기.IMAGE IMAGE_VALUE = new 실행파일적재기().검사(podaci);
        verifikovati(IMAGE_VALUE.START_adresa() == 0x04001000, "ELF koristiti adresa");
        verifikovati(IMAGE_VALUE.구역들().size() == 1 && IMAGE_VALUE.구역들().get(0).종류() == 8, "ELF 빈 podaci odeljak_VALUE");
        int 서술자 = jezgro_VALUE.체계호출().otvoren(jezgro_VALUE.첫과정(), "시험", 체계호출.samo_za_čitanje_zastavica);
        verifikovati(jezgro_VALUE.체계호출().Datoteka_kontrola(jezgro_VALUE.첫과정(), 서술자, 2, 1) == 0, "Izvrši_komanda 시 Zatvori Postavke");
        verifikovati(jezgro_VALUE.체계호출().Izvrši_komanda(jezgro_VALUE.첫과정(), podaci, new String[] {"시험", "값"}, new String[] {"jezik=한국어"}) == 0, "ELF Izvrši_komanda IMAGE_VALUE 적재");
        verifikovati(jezgro_VALUE.첫과정().실행시작주소() == 0x04001000, "Izvrši_komanda koristiti adresa 반영");
        verifikovati(jezgro_VALUE.첫과정().실행인자().length == 2 && jezgro_VALUE.첫과정().환경값().length == 1, "Izvrši_komanda 인자와 환경");
        verifikovati(!jezgro_VALUE.첫과정().파일서술자().informatičko_odeljenje_otvoren(서술자), "Izvrši_komanda 시 서술자 Zatvori");
        verifikovati(jezgro_VALUE.쪽관리().바이트읽기(jezgro_VALUE.첫과정().adresa_prostor(), 0x04002000) == 0, "빈 podaci odeljak_VALUE nula_operand 초기화");
    }

    private static void 입력시험(jezgro jezgro_VALUE) {
        jezgro_VALUE.입력관리().Ključ_van_funkcije('가');
        jezgro_VALUE.입력관리().쥐이동(3, -2);
        입력사건 첫사건 = jezgro_VALUE.입력관리().Dalje_događaj();
        입력사건 SECOND_događaj = jezgro_VALUE.입력관리().Dalje_događaj();
        verifikovati(첫사건.vrsta_događaja() == 입력사건.종류.Ključ_van_funkcije, "자판 događaj");
        verifikovati(SECOND_događaj.첫째값() == 3 && SECOND_događaj.SECOND_VALUE() == -2, "쥐 premestiti_VALUE događaj");
    }

    private static void 하드웨어시험(호스트하드웨어 uređaj_VALUE) {
        uređaj_VALUE.포트바이트쓰기(0x3f8, 0xab);
        verifikovati(uređaj_VALUE.포트바이트읽기(0x3f8) == 0xab, "포트 U_I 경계");
        verifikovati(uređaj_VALUE.직렬기록().contains("JTurOS"), "직렬 LOG_snimi");
    }

    private static void 개입중단과서술자시험() {
        IRQ_menadžer menadžer_VALUE = new IRQ_menadžer();
        menadžer_VALUE.registar_stavka(0x21, Skladište_adresa -> Skladište_adresa + 4);
        menadžer_VALUE.omogućiti();
        verifikovati(menadžer_VALUE.distribuirati_VALUE(0x21, 100) == 104, "IRQ distribuirati_VALUE");
        menadžer_VALUE.deaktivirati();
        verifikovati(menadžer_VALUE.distribuirati_VALUE(0x21, 100) == 100, "IRQ deaktivirati");

        전역서술자표 서술자표 = new 전역서술자표();
        서술자표.skup_podrazumevana_vrednost();
        verifikovati(서술자표.조각들().size() == 5, "전역 서술자표");
        obaveza_Status_segment obaveza_Status = new obaveza_Status_segment();
        obaveza_Status.특권쌓임공간설정(0x10, 0x800000);
        verifikovati(obaveza_Status.stek_nula_blok() == 0x10 && obaveza_Status.stek_nula_adresa() == 0x800000, "작업 Status_VALUE odeljak_VALUE");
    }

    private static void 저장장치와통신망시험() {
        고급기술결합장치 uređaj_za_skladištenje = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.odeljak_promeniti_veličinu];
        byte[] 읽은자료 = new byte[고급기술결합장치.odeljak_promeniti_veličinu];
        쓸자료[17] = 42;
        uređaj_za_skladištenje.쓰기(2, 쓸자료);
        uređaj_za_skladištenje.읽기(2, 읽은자료);
        verifikovati(읽은자료[17] == 42, "ATA odeljak_VALUE 읽고 쓰기");

        periferijski_uređaj_magistrala_menadžer periferijski_uređaj = new periferijski_uređaj_magistrala_menadžer();
        periferijski_uređaj.발견(new periferijski_uređaj_magistrala_menadžer.uređaj_VALUE(0x1022, 0x2000, 0xc000, 11));
        verifikovati(periferijski_uređaj.FIND_stavka(0x1022, 0x2000) != null, "주변 uređaj_VALUE FIND_stavka");

        byte[] Ethernet_kadar = new byte[34];
        Ethernet_kadar[12] = 0x08;
        Ethernet_kadar[13] = 0x00;
        Ethernet_kadar[14] = 0x45;
        verifikovati(Mreža_Alatke.Ethernet_UPPER_protokol(Ethernet_kadar) == 0x0800, "이더넷 상위 ugovor_VALUE");
        verifikovati(Mreža_Alatke.상호통신망규약사판인가(Ethernet_kadar, 14), "상호통신망규약 4판");
        verifikovati(Mreža_Alatke.oblak_kontrolni_zbir(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 kontrolni_zbir");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        정수쓰기(첫구역, 454, 63);
        정수쓰기(첫구역, 458, 1024);
        verifikovati(new primarna_particija_tabela().읽기(첫구역).size() == 1, "podrazumevana_vrednost 분할 영역표");

        sloj_mreže sloj_VALUE = new sloj_mreže();
        int[] RECEIVED_COUNT = new int[1];
        sloj_VALUE.registar_korisnik_podaci_lekcija(7, (podaci, koristiti, 길이) -> RECEIVED_COUNT[0]++);
        byte[] kadar_INDEX = new byte[14 + 20 + 8];
        kadar_INDEX[12] = 0x08;
        kadar_INDEX[13] = 0x00;
        kadar_INDEX[14] = 0x45;
        kadar_INDEX[16] = 0;
        kadar_INDEX[17] = 28;
        kadar_INDEX[23] = 17;
        kadar_INDEX[36] = 0;
        kadar_INDEX[37] = 7;
        verifikovati(sloj_VALUE.primiti_Ethernet(kadar_INDEX) && RECEIVED_COUNT[0] == 1, "korisnik podaci lekcija_VALUE distribuirati_VALUE");
    }

    private static void 화면과시계시험() {
        znak_ekran 화면 = new znak_ekran();
        화면.출력("가나\n다");
        verifikovati(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 출력");
        Sat Sat = new Sat(100);
        for (int INDEX = 0; INDEX < 10; INDEX++) {
            Sat.틱();
        }
        verifikovati(Sat.지난밀리초() == 100, "Sat 틱 CONVERT_VALUE");
    }

    private static void 정수쓰기(byte[] podaci, int pozicija, int VALUE) {
        podaci[pozicija] = (byte) VALUE;
        podaci[pozicija + 1] = (byte) (VALUE >>> 8);
        podaci[pozicija + 2] = (byte) (VALUE >>> 16);
        podaci[pozicija + 3] = (byte) (VALUE >>> 24);
    }

    private static void 짧은정수쓰기(byte[] podaci, int pozicija, int VALUE) {
        podaci[pozicija] = (byte) VALUE;
        podaci[pozicija + 1] = (byte) (VALUE >>> 8);
    }

    private static void verifikovati(boolean stanje, String ime) {
        if (!stanje) {
            throw new AssertionError("otkazivanje_VALUE: " + ime);
        }
        prebaciti_COUNT++;
        System.out.println("prebaciti_VALUE: " + ime);
    }
}
