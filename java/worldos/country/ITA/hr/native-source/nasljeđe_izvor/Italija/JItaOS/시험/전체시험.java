// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italija.JItaOS.시험;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Italija.JItaOS.Memorija_regije.Memorija_Upravitelj;
import Italija.JItaOS.Memorija_regije.dojaviti_Upravitelj;
import Italija.JItaOS.입력.입력사건;
import Italija.JItaOS.작업.Proces_VALUE;
import Italija.JItaOS.체계호출.체계호출;
import Italija.JItaOS.datotečni_sustav.실행파일적재기;
import Italija.JItaOS.jezgra_sustava.jezgra_sustava;
import Italija.JItaOS.domaćin.호스트하드웨어;
import Italija.JItaOS.IRQ.IRQ_Upravitelj;
import Italija.JItaOS.서술자.전역서술자표;
import Italija.JItaOS.uređaj_za_pohranu.고급기술결합장치;
import Italija.JItaOS.uređaj_VALUE.periferijski_uređaj_sabirnica_Upravitelj;
import Italija.JItaOS.mreža_hrpa.mreža_Alati;
import Italija.JItaOS.mreža_hrpa.mrežni_sloj;
import Italija.JItaOS.uređaj_VALUE.Sat;
import Italija.JItaOS.서술자.obaveza_Stanje_segment;
import Italija.JItaOS.화면.znak_zaslon;
import Italija.JItaOS.datotečni_sustav.primarna_particija_tablica;

public final class 전체시험 {
    private static int proslijediti_COUNT;

    private 전체시험() {
    }

    public static void main(String[] parametar_argument) {
        호스트하드웨어 uređaj_VALUE = new 호스트하드웨어();
        jezgra_sustava jezgra_sustava_VALUE = new jezgra_sustava(uređaj_VALUE);
        jezgra_sustava_VALUE.Pokreni();

        기억공간시험(jezgra_sustava_VALUE);
        쪽관리시험(jezgra_sustava_VALUE);
        파일과과정시험(jezgra_sustava_VALUE);
        실행파일시험(jezgra_sustava_VALUE);
        입력시험(jezgra_sustava_VALUE);
        하드웨어시험(uređaj_VALUE);
        개입중단과서술자시험();
        저장장치와통신망시험();
        화면과시계시험();

        System.out.println("JItaOS 시험 proslijediti_VALUE: " + proslijediti_COUNT);
    }

    private static void 기억공간시험(jezgra_sustava jezgra_sustava_VALUE) {
        Memorija_Upravitelj Upravitelj_VALUE = jezgra_sustava_VALUE.Memorija_regije();
        int 첫주소 = Upravitelj_VALUE.정렬할당(100, 64);
        provjeriti((첫주소 & 63) == 0, "poravnati_VALUE dodijeli_Pohrana");
        Upravitelj_VALUE.zapisivanje_bajt_VALUE(첫주소, (byte) 0x5a);
        provjeriti(Upravitelj_VALUE.바이트읽기(첫주소) == (byte) 0x5a, "물리 Memorija_regije 읽고 Zapisuj");
        int 사용전 = Upravitelj_VALUE.사용크기();
        Upravitelj_VALUE.izdati_Pohrana(첫주소);
        provjeriti(Upravitelj_VALUE.사용크기() < 사용전, "Memorija_regije izdati_Pohrana");
    }

    private static void 쪽관리시험(jezgra_sustava jezgra_sustava_VALUE) {
        dojaviti_Upravitelj Upravitelj_VALUE = jezgra_sustava_VALUE.쪽관리();
        dojaviti_Upravitelj.adresa_Space roditeljski_Space = Upravitelj_VALUE.새주소공간();
        Upravitelj_VALUE.MAP_dojaviti(roditeljski_Space, 0x1000, true);
        Upravitelj_VALUE.zapisivanje_bajt_VALUE(roditeljski_Space, 0x1010, (byte) 7);
        dojaviti_Upravitelj.adresa_Space dijete_Space = Upravitelj_VALUE.쓰기시복사복제(roditeljski_Space);
        Upravitelj_VALUE.zapisivanje_bajt_VALUE(dijete_Space, 0x1010, (byte) 9);
        provjeriti(Upravitelj_VALUE.바이트읽기(roditeljski_Space, 0x1010) == 7, "Zapisuj 시 instanca_VALUE roditeljski_VALUE 격리");
        provjeriti(Upravitelj_VALUE.바이트읽기(dijete_Space, 0x1010) == 9, "Zapisuj 시 instanca_VALUE dijete_VALUE Zapisuj");
    }

    private static void 파일과과정시험(jezgra_sustava jezgra_sustava_VALUE) {
        byte[] Sadržaj_VALUE = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        jezgra_sustava_VALUE.datotečni_sustav().dodati_Datoteka("시험", Sadržaj_VALUE);
        Proces_VALUE roditeljski_VALUE = jezgra_sustava_VALUE.첫과정();
        체계호출 호출 = jezgra_sustava_VALUE.체계호출();
        int 서술자 = 호출.Otvori(roditeljski_VALUE, "/시험", 체계호출.samo_za_čitanje_zastavica);
        provjeriti(서술자 >= 3, "Datoteka Otvori");

        byte[] primiti_odredište = new byte[Sadržaj_VALUE.length];
        provjeriti(호출.Čitaj(roditeljski_VALUE, 서술자, primiti_odredište, primiti_odredište.length) == Sadržaj_VALUE.length, "Datoteka Čitaj");
        provjeriti(Arrays.equals(Sadržaj_VALUE, primiti_odredište), "Datoteka Sadržaj_VALUE");
        provjeriti(호출.pomicati_se_položaj(roditeljski_VALUE, 서술자, 0, 체계호출.Traži_START) == 0, "Datoteka Položaj pomicati_se_VALUE");

        int 복제서술자 = 호출.서술자복제(roditeljski_VALUE, 서술자);
        provjeriti(복제서술자 >= 0, "서술자 klon_VALUE");
        Proces_VALUE dijete_VALUE = 호출.klon_Proces(roditeljski_VALUE);
        provjeriti(dijete_VALUE.identifikator_VALUE() != roditeljski_VALUE.identifikator_VALUE(), "Proces_VALUE identifikator_VALUE 분리");
        provjeriti(dijete_VALUE.roditeljski_identifikator() == roditeljski_VALUE.identifikator_VALUE(), "roditeljski_VALUE Proces_VALUE identifikator_VALUE");
        provjeriti(호출.Zatvori(dijete_VALUE, 서술자) == 0 && roditeljski_VALUE.파일서술자().odjel_informacijske_tehnologije_otvoreno(서술자), "dijete_VALUE Zatvori 격리");

        int 이전끝 = 호출.povećanje_program_pauza(roditeljski_VALUE, 8192);
        provjeriti(이전끝 == 0x06000000, "program_f5044b9b 끝 늘리기");
        provjeriti(roditeljski_VALUE.program_pauza() == 0x06002000, "program_f5044b9b 끝 반영");
        provjeriti(dijete_VALUE.program_pauza() == 0x06000000, "과정별 program_f5044b9b 끝 격리");

        dijete_VALUE.Izlaz_program(7);
        provjeriti(호출.자식기다리기(roditeljski_VALUE, dijete_VALUE.identifikator_VALUE(), false) == (7 << 8), "dijete_VALUE Izlaz_program 기다리기");
        provjeriti(호출.접근가능("시험", 1) == -13, "Izvrši_naredba dozvola_VALUE odbiti_VALUE");
        provjeriti(호출.UID() == 0 && 호출.Grupa_identifikator() == 0, "사용자와 무리 identifikator_VALUE");
        provjeriti("/".equals(호출.redovno_popis_zadataka(2)) && 호출.SWITCH_popis_zadataka("/") == 0, "redovno_artikl 작업 unos_Popis");
        provjeriti(호출.odjel_informacijske_tehnologije_Terminal(roditeljski_VALUE, 1), "표준 Izlaz 단말");
        provjeriti("JItaOS".equals(호출.sustav_Pojedinosti().sustav_naziv()), "operacijski_sustav_VALUE Podaci_o_sustavu");
    }

    private static void 실행파일시험(jezgra_sustava jezgra_sustava_VALUE) {
        byte[] podaci = new byte[92];
        podaci[0] = 0x7f;
        podaci[1] = 'E';
        podaci[2] = 'L';
        podaci[3] = 'F';
        podaci[4] = 1;
        podaci[5] = 1;
        zapisivanje_cijeli_broj_VALUE(podaci, 24, 0x04001000);
        zapisivanje_cijeli_broj_VALUE(podaci, 32, 52);
        짧은정수쓰기(podaci, 46, 40);
        짧은정수쓰기(podaci, 48, 1);
        zapisivanje_cijeli_broj_VALUE(podaci, 56, 8);
        zapisivanje_cijeli_broj_VALUE(podaci, 60, 2);
        zapisivanje_cijeli_broj_VALUE(podaci, 64, 0x04002000);
        zapisivanje_cijeli_broj_VALUE(podaci, 72, 64);

        실행파일적재기.IMAGE IMAGE_VALUE = new 실행파일적재기().검사(podaci);
        provjeriti(IMAGE_VALUE.START_adresa() == 0x04001000, "ELF Pokreni adresa");
        provjeriti(IMAGE_VALUE.구역들().size() == 1 && IMAGE_VALUE.구역들().get(0).종류() == 8, "ELF 빈 podaci sekcija_VALUE");
        int 서술자 = jezgra_sustava_VALUE.체계호출().Otvori(jezgra_sustava_VALUE.첫과정(), "시험", 체계호출.samo_za_čitanje_zastavica);
        provjeriti(jezgra_sustava_VALUE.체계호출().Datoteka_kontrola(jezgra_sustava_VALUE.첫과정(), 서술자, 2, 1) == 0, "Izvrši_naredba 시 Zatvori Postavke");
        provjeriti(jezgra_sustava_VALUE.체계호출().Izvrši_naredba(jezgra_sustava_VALUE.첫과정(), podaci, new String[] {"시험", "값"}, new String[] {"Jezik=hrvatski"}) == 0, "ELF Izvrši_naredba IMAGE_VALUE 적재");
        provjeriti(jezgra_sustava_VALUE.첫과정().실행시작주소() == 0x04001000, "Izvrši_naredba Pokreni adresa 반영");
        provjeriti(jezgra_sustava_VALUE.첫과정().실행인자().length == 2 && jezgra_sustava_VALUE.첫과정().okruženje_VALUE().length == 1, "Izvrši_naredba 인자와 okruženje");
        provjeriti(!jezgra_sustava_VALUE.첫과정().파일서술자().odjel_informacijske_tehnologije_otvoreno(서술자), "Izvrši_naredba 시 서술자 Zatvori");
        provjeriti(jezgra_sustava_VALUE.쪽관리().바이트읽기(jezgra_sustava_VALUE.첫과정().adresa_Space(), 0x04002000) == 0, "빈 podaci sekcija_VALUE nula_operand 초기화");
    }

    private static void 입력시험(jezgra_sustava jezgra_sustava_VALUE) {
        jezgra_sustava_VALUE.입력관리().Ključ_izvan_funkcije('가');
        jezgra_sustava_VALUE.입력관리().쥐이동(3, -2);
        입력사건 첫사건 = jezgra_sustava_VALUE.입력관리().Dalje_događaj();
        입력사건 SECOND_događaj = jezgra_sustava_VALUE.입력관리().Dalje_događaj();
        provjeriti(첫사건.vrsta_događaja() == 입력사건.종류.Ključ_izvan_funkcije, "자판 Događaj");
        provjeriti(SECOND_događaj.첫째값() == 3 && SECOND_događaj.SECOND_VALUE() == -2, "쥐 pomicati_se_VALUE Događaj");
    }

    private static void 하드웨어시험(호스트하드웨어 uređaj_VALUE) {
        uređaj_VALUE.zapisivanje_prebaciti_bajt(0x3f8, 0xab);
        provjeriti(uređaj_VALUE.포트바이트읽기(0x3f8) == 0xab, "포트 U_I 경계");
        provjeriti(uređaj_VALUE.직렬기록().contains("JItaOS"), "직렬 LOG_zapis");
    }

    private static void 개입중단과서술자시험() {
        IRQ_Upravitelj Upravitelj_VALUE = new IRQ_Upravitelj();
        Upravitelj_VALUE.registar_unos(0x21, Pohrana_adresa -> Pohrana_adresa + 4);
        Upravitelj_VALUE.omogućiti();
        provjeriti(Upravitelj_VALUE.distribuirati_VALUE(0x21, 100) == 104, "IRQ distribuirati_VALUE");
        Upravitelj_VALUE.deaktivirati();
        provjeriti(Upravitelj_VALUE.distribuirati_VALUE(0x21, 100) == 100, "IRQ deaktivirati");

        전역서술자표 서술자표 = new 전역서술자표();
        서술자표.skup_zadana_vrijednost();
        provjeriti(서술자표.조각들().size() == 5, "전역 서술자표");
        obaveza_Stanje_segment obaveza_Stanje = new obaveza_Stanje_segment();
        obaveza_Stanje.특권쌓임공간설정(0x10, 0x800000);
        provjeriti(obaveza_Stanje.hrpa_nula_blok() == 0x10 && obaveza_Stanje.hrpa_nula_adresa() == 0x800000, "작업 Stanje_VALUE sekcija_VALUE");
    }

    private static void 저장장치와통신망시험() {
        고급기술결합장치 uređaj_za_pohranu = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.sekcija_promijeniti_veličinu];
        byte[] 읽은자료 = new byte[고급기술결합장치.sekcija_promijeniti_veličinu];
        쓸자료[17] = 42;
        uređaj_za_pohranu.Zapisuj(2, 쓸자료);
        uređaj_za_pohranu.Čitaj(2, 읽은자료);
        provjeriti(읽은자료[17] == 42, "ATA sekcija_VALUE 읽고 Zapisuj");

        periferijski_uređaj_sabirnica_Upravitelj periferijski_uređaj = new periferijski_uređaj_sabirnica_Upravitelj();
        periferijski_uređaj.발견(new periferijski_uređaj_sabirnica_Upravitelj.uređaj_VALUE(0x1022, 0x2000, 0xc000, 11));
        provjeriti(periferijski_uređaj.FIND_unos(0x1022, 0x2000) != null, "주변 uređaj_VALUE FIND_unos");

        byte[] Ethernet_kadar = new byte[34];
        Ethernet_kadar[12] = 0x08;
        Ethernet_kadar[13] = 0x00;
        Ethernet_kadar[14] = 0x45;
        provjeriti(mreža_Alati.Ethernet_UPPER_protokol(Ethernet_kadar) == 0x0800, "이더넷 상위 slučaj_VALUE");
        provjeriti(mreža_Alati.상호통신망규약사판인가(Ethernet_kadar, 14), "상호통신망규약 4판");
        provjeriti(mreža_Alati.oblak_kontrolni_zbroj(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 kontrolni_zbroj");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        zapisivanje_cijeli_broj_VALUE(첫구역, 454, 63);
        zapisivanje_cijeli_broj_VALUE(첫구역, 458, 1024);
        provjeriti(new primarna_particija_tablica().Čitaj(첫구역).size() == 1, "zadana_vrijednost 분할 영역표");

        mrežni_sloj sloj_VALUE = new mrežni_sloj();
        int[] RECEIVED_COUNT = new int[1];
        sloj_VALUE.registar_korisnik_podaci_lekcija(7, (podaci, Pokreni, 길이) -> RECEIVED_COUNT[0]++);
        byte[] kadar_INDEX = new byte[14 + 20 + 8];
        kadar_INDEX[12] = 0x08;
        kadar_INDEX[13] = 0x00;
        kadar_INDEX[14] = 0x45;
        kadar_INDEX[16] = 0;
        kadar_INDEX[17] = 28;
        kadar_INDEX[23] = 17;
        kadar_INDEX[36] = 0;
        kadar_INDEX[37] = 7;
        provjeriti(sloj_VALUE.primiti_Ethernet(kadar_INDEX) && RECEIVED_COUNT[0] == 1, "korisnik podaci lekcija_VALUE distribuirati_VALUE");
    }

    private static void 화면과시계시험() {
        znak_zaslon 화면 = new znak_zaslon();
        화면.Izlaz("가나\n다");
        provjeriti(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 Izlaz");
        Sat Sat = new Sat(100);
        for (int INDEX = 0; INDEX < 10; INDEX++) {
            Sat.otkucavanje_VALUE();
        }
        provjeriti(Sat.지난밀리초() == 100, "Sat otkucavanje_VALUE CONVERT_VALUE");
    }

    private static void zapisivanje_cijeli_broj_VALUE(byte[] podaci, int Položaj, int VALUE) {
        podaci[Položaj] = (byte) VALUE;
        podaci[Položaj + 1] = (byte) (VALUE >>> 8);
        podaci[Položaj + 2] = (byte) (VALUE >>> 16);
        podaci[Položaj + 3] = (byte) (VALUE >>> 24);
    }

    private static void 짧은정수쓰기(byte[] podaci, int Položaj, int VALUE) {
        podaci[Položaj] = (byte) VALUE;
        podaci[Položaj + 1] = (byte) (VALUE >>> 8);
    }

    private static void provjeriti(boolean uvjet, String Ime) {
        if (!uvjet) {
            throw new AssertionError("kvar_VALUE: " + Ime);
        }
        proslijediti_COUNT++;
        System.out.println("proslijediti_VALUE: " + Ime);
    }
}
