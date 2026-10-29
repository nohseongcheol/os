// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Bosna_i_Hercegovina.JBihOS.시험;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Bosna_i_Hercegovina.JBihOS.기억공간.Memorija_menadžer;
import Bosna_i_Hercegovina.JBihOS.기억공간.stranica_menadžer;
import Bosna_i_Hercegovina.JBihOS.입력.입력사건;
import Bosna_i_Hercegovina.JBihOS.작업.proces_VALUE;
import Bosna_i_Hercegovina.JBihOS.체계호출.체계호출;
import Bosna_i_Hercegovina.JBihOS.fajl_sistem.실행파일적재기;
import Bosna_i_Hercegovina.JBihOS.jezgro.jezgro;
import Bosna_i_Hercegovina.JBihOS.organizator.organizator_hardver;
import Bosna_i_Hercegovina.JBihOS.IRQ.IRQ_menadžer;
import Bosna_i_Hercegovina.JBihOS.서술자.전역서술자표;
import Bosna_i_Hercegovina.JBihOS.Pohrana_uređaj.고급기술결합장치;
import Bosna_i_Hercegovina.JBihOS.uređaj_VALUE.periferijski_uređaj_sabirnica_menadžer;
import Bosna_i_Hercegovina.JBihOS.Mreža_snop.Mreža_Alati;
import Bosna_i_Hercegovina.JBihOS.Mreža_snop.Mreža_sloj;
import Bosna_i_Hercegovina.JBihOS.uređaj_VALUE.Sat;
import Bosna_i_Hercegovina.JBihOS.서술자.zadatak_stanje_segment;
import Bosna_i_Hercegovina.JBihOS.화면.znak_ekran;
import Bosna_i_Hercegovina.JBihOS.fajl_sistem.기본분할영역표;

public final class 전체시험 {
    private static int proslijediti_COUNT;

    private 전체시험() {
    }

    public static void main(String[] parametar_argument) {
        organizator_hardver uređaj_VALUE = new organizator_hardver();
        jezgro jezgro_VALUE = new jezgro(uređaj_VALUE);
        jezgro_VALUE.Pokreni();

        기억공간시험(jezgro_VALUE);
        쪽관리시험(jezgro_VALUE);
        파일과과정시험(jezgro_VALUE);
        실행파일시험(jezgro_VALUE);
        입력시험(jezgro_VALUE);
        하드웨어시험(uređaj_VALUE);
        개입중단과서술자시험();
        저장장치와통신망시험();
        화면과시계시험();

        System.out.println("JBihOS 시험 proslijediti_VALUE: " + proslijediti_COUNT);
    }

    private static void 기억공간시험(jezgro jezgro_VALUE) {
        Memorija_menadžer menadžer_VALUE = jezgro_VALUE.기억공간();
        int 첫주소 = menadžer_VALUE.정렬할당(100, 64);
        potvrditi((첫주소 & 63) == 0, "poravnati_VALUE dodijeliti_Pohrana");
        menadžer_VALUE.pisati_bajt_VALUE(첫주소, (byte) 0x5a);
        potvrditi(menadžer_VALUE.바이트읽기(첫주소) == (byte) 0x5a, "물리 기억공간 읽고 Piši");
        int 사용전 = menadžer_VALUE.사용크기();
        menadžer_VALUE.izdanje_Pohrana(첫주소);
        potvrditi(menadžer_VALUE.사용크기() < 사용전, "기억공간 izdanje_Pohrana");
    }

    private static void 쪽관리시험(jezgro jezgro_VALUE) {
        stranica_menadžer menadžer_VALUE = jezgro_VALUE.쪽관리();
        stranica_menadžer.adresa_prostor roditelj_prostor = menadžer_VALUE.새주소공간();
        menadžer_VALUE.MAP_stranica(roditelj_prostor, 0x1000, true);
        menadžer_VALUE.pisati_bajt_VALUE(roditelj_prostor, 0x1010, (byte) 7);
        stranica_menadžer.adresa_prostor dijete_prostor = menadžer_VALUE.쓰기시복사복제(roditelj_prostor);
        menadžer_VALUE.pisati_bajt_VALUE(dijete_prostor, 0x1010, (byte) 9);
        potvrditi(menadžer_VALUE.바이트읽기(roditelj_prostor, 0x1010) == 7, "Piši 시 instanca_VALUE roditelj_VALUE 격리");
        potvrditi(menadžer_VALUE.바이트읽기(dijete_prostor, 0x1010) == 9, "Piši 시 instanca_VALUE dijete_VALUE Piši");
    }

    private static void 파일과과정시험(jezgro jezgro_VALUE) {
        byte[] Sadržaj_VALUE = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        jezgro_VALUE.fajl_sistem().파일추가("시험", Sadržaj_VALUE);
        proces_VALUE roditelj_VALUE = jezgro_VALUE.첫과정();
        체계호출 호출 = jezgro_VALUE.체계호출();
        int 서술자 = 호출.Otvori(roditelj_VALUE, "/시험", 체계호출.samo_za_čitanje_zastavica);
        potvrditi(서술자 >= 3, "Fajl Otvori");

        byte[] 받을곳 = new byte[Sadržaj_VALUE.length];
        potvrditi(호출.Čitaj(roditelj_VALUE, 서술자, 받을곳, 받을곳.length) == Sadržaj_VALUE.length, "Fajl Čitaj");
        potvrditi(Arrays.equals(Sadržaj_VALUE, 받을곳), "Fajl Sadržaj_VALUE");
        potvrditi(호출.pomaći_položaj(roditelj_VALUE, 서술자, 0, 체계호출.Traži_START) == 0, "Fajl Pozicija pomaći_VALUE");

        int 복제서술자 = 호출.서술자복제(roditelj_VALUE, 서술자);
        potvrditi(복제서술자 >= 0, "서술자 복제");
        proces_VALUE dijete_VALUE = 호출.과정복제(roditelj_VALUE);
        potvrditi(dijete_VALUE.identifikator_VALUE() != roditelj_VALUE.identifikator_VALUE(), "proces_VALUE identifikator_VALUE 분리");
        potvrditi(dijete_VALUE.roditelj_identifikator() == roditelj_VALUE.identifikator_VALUE(), "roditelj_VALUE proces_VALUE identifikator_VALUE");
        potvrditi(호출.Zatvori(dijete_VALUE, 서술자) == 0 && roditelj_VALUE.파일서술자().odjel_za_informacijske_tehnologije_kreirati(서술자), "dijete_VALUE Zatvori 격리");

        int 이전끝 = 호출.프로그램끝늘리기(roditelj_VALUE, 8192);
        potvrditi(이전끝 == 0x06000000, "program_f5044b9b 끝 늘리기");
        potvrditi(roditelj_VALUE.프로그램끝() == 0x06002000, "program_f5044b9b 끝 반영");
        potvrditi(dijete_VALUE.프로그램끝() == 0x06000000, "과정별 program_f5044b9b 끝 격리");

        dijete_VALUE.izaći_program(7);
        potvrditi(호출.자식기다리기(roditelj_VALUE, dijete_VALUE.identifikator_VALUE(), false) == (7 << 8), "dijete_VALUE izaći_program 기다리기");
        potvrditi(호출.접근가능("시험", 1) == -13, "Izvrši_komanda dozvola_VALUE odbiti_VALUE");
        potvrditi(호출.korisnik_identifikator() == 0 && 호출.Grupa_identifikator() == 0, "사용자와 무리 identifikator_VALUE");
        potvrditi("/".equals(호출.trenutno_spisak_zadataka(2)) && 호출.SWITCH_spisak_zadataka("/") == 0, "trenutno_stavka 작업 unos_spisak");
        potvrditi(호출.odjel_za_informacijske_tehnologije_Terminal(roditelj_VALUE, 1), "표준 Ispis 단말");
        potvrditi("JBihOS".equals(호출.sistem_Detalji().sistem_naziv()), "operativni_sistem_VALUE msinfo32_exe");
    }

    private static void 실행파일시험(jezgro jezgro_VALUE) {
        byte[] podaci = new byte[92];
        podaci[0] = 0x7f;
        podaci[1] = 'E';
        podaci[2] = 'L';
        podaci[3] = 'F';
        podaci[4] = 1;
        podaci[5] = 1;
        pisati_cijeli_broj_VALUE(podaci, 24, 0x04001000);
        pisati_cijeli_broj_VALUE(podaci, 32, 52);
        짧은정수쓰기(podaci, 46, 40);
        짧은정수쓰기(podaci, 48, 1);
        pisati_cijeli_broj_VALUE(podaci, 56, 8);
        pisati_cijeli_broj_VALUE(podaci, 60, 2);
        pisati_cijeli_broj_VALUE(podaci, 64, 0x04002000);
        pisati_cijeli_broj_VALUE(podaci, 72, 64);

        실행파일적재기.IMAGE IMAGE_VALUE = new 실행파일적재기().검사(podaci);
        potvrditi(IMAGE_VALUE.početna_adresa() == 0x04001000, "ELF Pokreni adresa");
        potvrditi(IMAGE_VALUE.구역들().size() == 1 && IMAGE_VALUE.구역들().get(0).종류() == 8, "ELF 빈 podaci sekcija_VALUE");
        int 서술자 = jezgro_VALUE.체계호출().Otvori(jezgro_VALUE.첫과정(), "시험", 체계호출.samo_za_čitanje_zastavica);
        potvrditi(jezgro_VALUE.체계호출().fajl_kontrola(jezgro_VALUE.첫과정(), 서술자, 2, 1) == 0, "Izvrši_komanda 시 Zatvori Postavke");
        potvrditi(jezgro_VALUE.체계호출().Izvrši_komanda(jezgro_VALUE.첫과정(), podaci, new String[] {"시험", "값"}, new String[] {"Jezik=한국어"}) == 0, "ELF Izvrši_komanda IMAGE_VALUE 적재");
        potvrditi(jezgro_VALUE.첫과정().실행시작주소() == 0x04001000, "Izvrši_komanda Pokreni adresa 반영");
        potvrditi(jezgro_VALUE.첫과정().실행인자().length == 2 && jezgro_VALUE.첫과정().operativno_okruženje_VALUE().length == 1, "Izvrši_komanda 인자와 operativno_okruženje");
        potvrditi(!jezgro_VALUE.첫과정().파일서술자().odjel_za_informacijske_tehnologije_kreirati(서술자), "Izvrši_komanda 시 서술자 Zatvori");
        potvrditi(jezgro_VALUE.쪽관리().바이트읽기(jezgro_VALUE.첫과정().adresa_prostor(), 0x04002000) == 0, "빈 podaci sekcija_VALUE 영 inicijalizirati");
    }

    private static void 입력시험(jezgro jezgro_VALUE) {
        jezgro_VALUE.입력관리().키누름('가');
        jezgro_VALUE.입력관리().쥐이동(3, -2);
        입력사건 첫사건 = jezgro_VALUE.입력관리().Dalje_događaj();
        입력사건 SECOND_događaj = jezgro_VALUE.입력관리().Dalje_događaj();
        potvrditi(첫사건.사건종류() == 입력사건.종류.키누름, "자판 događaj");
        potvrditi(SECOND_događaj.첫째값() == 3 && SECOND_događaj.SECOND_VALUE() == -2, "쥐 pomaći_VALUE događaj");
    }

    private static void 하드웨어시험(organizator_hardver uređaj_VALUE) {
        uređaj_VALUE.pisati_port_bajt(0x3f8, 0xab);
        potvrditi(uređaj_VALUE.포트바이트읽기(0x3f8) == 0xab, "hardver_port U_I 경계");
        potvrditi(uređaj_VALUE.직렬기록().contains("JBihOS"), "직렬 LOG_red");
    }

    private static void 개입중단과서술자시험() {
        IRQ_menadžer menadžer_VALUE = new IRQ_menadžer();
        menadžer_VALUE.registrirati_unos(0x21, Pohrana_adresa -> Pohrana_adresa + 4);
        menadžer_VALUE.omogućiti();
        potvrditi(menadžer_VALUE.distribuirati_VALUE(0x21, 100) == 104, "IRQ distribuirati_VALUE");
        menadžer_VALUE.deaktivirati();
        potvrditi(menadžer_VALUE.distribuirati_VALUE(0x21, 100) == 100, "IRQ deaktivirati");

        전역서술자표 서술자표 = new 전역서술자표();
        서술자표.skup_zadana_vrijednost();
        potvrditi(서술자표.조각들().size() == 5, "전역 서술자표");
        zadatak_stanje_segment zadatak_stanje = new zadatak_stanje_segment();
        zadatak_stanje.특권쌓임공간설정(0x10, 0x800000);
        potvrditi(zadatak_stanje.영번쌓임조각() == 0x10 && zadatak_stanje.영번쌓임주소() == 0x800000, "작업 stanje_VALUE sekcija_VALUE");
    }

    private static void 저장장치와통신망시험() {
        고급기술결합장치 Pohrana_uređaj = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.sekcija_podesiti_veličinu];
        byte[] 읽은자료 = new byte[고급기술결합장치.sekcija_podesiti_veličinu];
        쓸자료[17] = 42;
        Pohrana_uređaj.Piši(2, 쓸자료);
        Pohrana_uređaj.Čitaj(2, 읽은자료);
        potvrditi(읽은자료[17] == 42, "ATA sekcija_VALUE 읽고 Piši");

        periferijski_uređaj_sabirnica_menadžer periferijski_uređaj = new periferijski_uređaj_sabirnica_menadžer();
        periferijski_uređaj.발견(new periferijski_uređaj_sabirnica_menadžer.uređaj_VALUE(0x1022, 0x2000, 0xc000, 11));
        potvrditi(periferijski_uređaj.FIND_unos(0x1022, 0x2000) != null, "주변 uređaj_VALUE FIND_unos");

        byte[] Ethernet_kadar = new byte[34];
        Ethernet_kadar[12] = 0x08;
        Ethernet_kadar[13] = 0x00;
        Ethernet_kadar[14] = 0x45;
        potvrditi(Mreža_Alati.Ethernet_UPPER_protokol(Ethernet_kadar) == 0x0800, "이더넷 상위 slučaj_VALUE");
        potvrditi(Mreža_Alati.상호통신망규약사판인가(Ethernet_kadar, 14), "상호통신망규약 4판");
        potvrditi(Mreža_Alati.oblak_kontrolni_zbir(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 kontrolni_zbir");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        pisati_cijeli_broj_VALUE(첫구역, 454, 63);
        pisati_cijeli_broj_VALUE(첫구역, 458, 1024);
        potvrditi(new 기본분할영역표().Čitaj(첫구역).size() == 1, "zadana_vrijednost 분할 영역표");

        Mreža_sloj sloj_VALUE = new Mreža_sloj();
        int[] RECEIVED_COUNT = new int[1];
        sloj_VALUE.registrirati_korisnik_podaci_lekcija(7, (podaci, Pokreni, dužina_VALUE) -> RECEIVED_COUNT[0]++);
        byte[] kadar_INDEX = new byte[14 + 20 + 8];
        kadar_INDEX[12] = 0x08;
        kadar_INDEX[13] = 0x00;
        kadar_INDEX[14] = 0x45;
        kadar_INDEX[16] = 0;
        kadar_INDEX[17] = 28;
        kadar_INDEX[23] = 17;
        kadar_INDEX[36] = 0;
        kadar_INDEX[37] = 7;
        potvrditi(sloj_VALUE.이더넷받기(kadar_INDEX) && RECEIVED_COUNT[0] == 1, "korisnik podaci lekcija_VALUE distribuirati_VALUE");
    }

    private static void 화면과시계시험() {
        znak_ekran 화면 = new znak_ekran();
        화면.Ispis("가나\n다");
        potvrditi(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 Ispis");
        Sat Sat = new Sat(100);
        for (int INDEX = 0; INDEX < 10; INDEX++) {
            Sat.틱();
        }
        potvrditi(Sat.지난밀리초() == 100, "Sat 틱 CONVERT_VALUE");
    }

    private static void pisati_cijeli_broj_VALUE(byte[] podaci, int Pozicija, int VALUE) {
        podaci[Pozicija] = (byte) VALUE;
        podaci[Pozicija + 1] = (byte) (VALUE >>> 8);
        podaci[Pozicija + 2] = (byte) (VALUE >>> 16);
        podaci[Pozicija + 3] = (byte) (VALUE >>> 24);
    }

    private static void 짧은정수쓰기(byte[] podaci, int Pozicija, int VALUE) {
        podaci[Pozicija] = (byte) VALUE;
        podaci[Pozicija + 1] = (byte) (VALUE >>> 8);
    }

    private static void potvrditi(boolean uvjet, String Naziv) {
        if (!uvjet) {
            throw new AssertionError("neuspjeh_VALUE: " + Naziv);
        }
        proslijediti_COUNT++;
        System.out.println("proslijediti_VALUE: " + Naziv);
    }
}
