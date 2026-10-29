// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Madžarska.JHunOS.시험;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Madžarska.JHunOS.pomnilnik_območje.pomnilnik_Upravitelj;
import Madžarska.JHunOS.pomnilnik_območje.stran_Upravitelj;
import Madžarska.JHunOS.입력.입력사건;
import Madžarska.JHunOS.작업.Proces_VALUE;
import Madžarska.JHunOS.체계호출.체계호출;
import Madžarska.JHunOS.datotečni_sistem.실행파일적재기;
import Madžarska.JHunOS.jedro.jedro;
import Madžarska.JHunOS.gostiti.gostiti_strojna_oprema;
import Madžarska.JHunOS.prekinitev.prekinitev_Upravitelj;
import Madžarska.JHunOS.서술자.GDT;
import Madžarska.JHunOS.naprava_za_shranjevanje.고급기술결합장치;
import Madžarska.JHunOS.naprava_VALUE.zunanji_vodilo_Upravitelj;
import Madžarska.JHunOS.mreža_Sklad.mreža_Orodja;
import Madžarska.JHunOS.mreža_Sklad.omrežna_plast;
import Madžarska.JHunOS.naprava_VALUE.Ura;
import Madžarska.JHunOS.서술자.opravek_stanje_segment;
import Madžarska.JHunOS.화면.znak_zaslon;
import Madžarska.JHunOS.datotečni_sistem.primarna_particija_tabela;

public final class 전체시험 {
    private static int posredovati_COUNT;

    private 전체시험() {
    }

    public static void main(String[] parameter_argument) {
        gostiti_strojna_oprema naprava_VALUE = new gostiti_strojna_oprema();
        jedro jedro_VALUE = new jedro(naprava_VALUE);
        jedro_VALUE.Zaženi();

        preskusiti_pomnilnik(jedro_VALUE);
        쪽관리시험(jedro_VALUE);
        파일과과정시험(jedro_VALUE);
        실행파일시험(jedro_VALUE);
        입력시험(jedro_VALUE);
        preskusiti_strojna_oprema(naprava_VALUE);
        개입중단과서술자시험();
        preskusiti_Senzor_prostora_AND_Uporaba_omrežij();
        화면과시계시험();

        System.out.println("JHunOS 시험 posredovati_VALUE: " + posredovati_COUNT);
    }

    private static void preskusiti_pomnilnik(jedro jedro_VALUE) {
        pomnilnik_Upravitelj Upravitelj_VALUE = jedro_VALUE.pomnilnik_območje();
        int 첫주소 = Upravitelj_VALUE.정렬할당(100, 64);
        확인((첫주소 & 63) == 0, "poravnati_VALUE dodeliti_Senzor_prostora");
        Upravitelj_VALUE.pisati_bajt_VALUE(첫주소, (byte) 0x5a);
        확인(Upravitelj_VALUE.바이트읽기(첫주소) == (byte) 0x5a, "물리 pomnilnik_območje 읽고 Pisanje");
        int 사용전 = Upravitelj_VALUE.사용크기();
        Upravitelj_VALUE.izdaja_Senzor_prostora(첫주소);
        확인(Upravitelj_VALUE.사용크기() < 사용전, "pomnilnik_območje izdaja_Senzor_prostora");
    }

    private static void 쪽관리시험(jedro jedro_VALUE) {
        stran_Upravitelj Upravitelj_VALUE = jedro_VALUE.쪽관리();
        stran_Upravitelj.naslov_Space nadrejen_Space = Upravitelj_VALUE.새주소공간();
        Upravitelj_VALUE.MAP_stran(nadrejen_Space, 0x1000, true);
        Upravitelj_VALUE.pisati_bajt_VALUE(nadrejen_Space, 0x1010, (byte) 7);
        stran_Upravitelj.naslov_Space otrok_Space = Upravitelj_VALUE.쓰기시복사복제(nadrejen_Space);
        Upravitelj_VALUE.pisati_bajt_VALUE(otrok_Space, 0x1010, (byte) 9);
        확인(Upravitelj_VALUE.바이트읽기(nadrejen_Space, 0x1010) == 7, "Pisanje 시 kopirati_VALUE nadrejen_VALUE 격리");
        확인(Upravitelj_VALUE.바이트읽기(otrok_Space, 0x1010) == 9, "Pisanje 시 kopirati_VALUE otrok_VALUE Pisanje");
    }

    private static void 파일과과정시험(jedro jedro_VALUE) {
        byte[] vsebina_VALUE = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        jedro_VALUE.datotečni_sistem().dodati_Datoteka("시험", vsebina_VALUE);
        Proces_VALUE nadrejen_VALUE = jedro_VALUE.첫과정();
        체계호출 호출 = jedro_VALUE.체계호출();
        int 서술자 = 호출.Odpri(nadrejen_VALUE, "/시험", 체계호출.samo_za_branje_zastavica);
        확인(서술자 >= 3, "Datoteka Odpri");

        byte[] sprejeti_sprejemati_prejeti_prejemati_cilj = new byte[vsebina_VALUE.length];
        확인(호출.Branje(nadrejen_VALUE, 서술자, sprejeti_sprejemati_prejeti_prejemati_cilj, sprejeti_sprejemati_prejeti_prejemati_cilj.length) == vsebina_VALUE.length, "Datoteka Branje");
        확인(Arrays.equals(vsebina_VALUE, sprejeti_sprejemati_prejeti_prejemati_cilj), "Datoteka vsebina_VALUE");
        확인(호출.premikati_položaj(nadrejen_VALUE, 서술자, 0, 체계호출.Išči_Start) == 0, "Datoteka Položaj premikati_VALUE");

        int 복제서술자 = 호출.서술자복제(nadrejen_VALUE, 서술자);
        확인(복제서술자 >= 0, "서술자 klon_VALUE");
        Proces_VALUE otrok_VALUE = 호출.klon_Proces(nadrejen_VALUE);
        확인(otrok_VALUE.identifikator_VALUE() != nadrejen_VALUE.identifikator_VALUE(), "Proces_VALUE identifikator_VALUE 분리");
        확인(otrok_VALUE.nadrejen_identifikator() == nadrejen_VALUE.identifikator_VALUE(), "nadrejen_VALUE Proces_VALUE identifikator_VALUE");
        확인(호출.Zapri(otrok_VALUE, 서술자) == 0 && nadrejen_VALUE.파일서술자().informacijska_tehnologija_odprto(서술자), "otrok_VALUE Zapri 격리");

        int 이전끝 = 호출.povečanje_aplikacija_odmor(nadrejen_VALUE, 8192);
        확인(이전끝 == 0x06000000, "aplikacija_f5044b9b 끝 늘리기");
        확인(nadrejen_VALUE.aplikacija_odmor() == 0x06002000, "aplikacija_f5044b9b 끝 반영");
        확인(otrok_VALUE.aplikacija_odmor() == 0x06000000, "과정별 aplikacija_f5044b9b 끝 격리");

        otrok_VALUE.Izhod_aplikacija(7);
        확인(호출.자식기다리기(nadrejen_VALUE, otrok_VALUE.identifikator_VALUE(), false) == (7 << 8), "otrok_VALUE Izhod_aplikacija 기다리기");
        확인(호출.접근가능("시험", 1) == -13, "Izvedi_ukaz dovoljenje_VALUE zavrniti_VALUE");
        확인(호출.ID_uporabnika() == 0 && 호출.Skupina_identifikator() == 0, "사용자와 무리 identifikator_VALUE");
        확인("/".equals(호출.sprotno_seznam_opravil(2)) && 호출.SWITCH_seznam_opravil("/") == 0, "sprotno_element 작업 vnos_Seznam");
        확인(호출.informacijska_tehnologija_Terminal(nadrejen_VALUE, 1), "표준 Izpis 단말");
        확인("JHunOS".equals(호출.sistem_Podrobnosti().sistem_ime()), "operacijski_sistem_VALUE msinfo32_exe");
    }

    private static void 실행파일시험(jedro jedro_VALUE) {
        byte[] podatki = new byte[92];
        podatki[0] = 0x7f;
        podatki[1] = 'E';
        podatki[2] = 'L';
        podatki[3] = 'F';
        podatki[4] = 1;
        podatki[5] = 1;
        pisati_celo_število_VALUE(podatki, 24, 0x04001000);
        pisati_celo_število_VALUE(podatki, 32, 52);
        짧은정수쓰기(podatki, 46, 40);
        짧은정수쓰기(podatki, 48, 1);
        pisati_celo_število_VALUE(podatki, 56, 8);
        pisati_celo_število_VALUE(podatki, 60, 2);
        pisati_celo_število_VALUE(podatki, 64, 0x04002000);
        pisati_celo_število_VALUE(podatki, 72, 64);

        실행파일적재기.IMAGE IMAGE_VALUE = new 실행파일적재기().검사(podatki);
        확인(IMAGE_VALUE.Start_naslov() == 0x04001000, "ELF Zaženi naslov");
        확인(IMAGE_VALUE.구역들().size() == 1 && IMAGE_VALUE.구역들().get(0).종류() == 8, "ELF 빈 podatki odsek_VALUE");
        int 서술자 = jedro_VALUE.체계호출().Odpri(jedro_VALUE.첫과정(), "시험", 체계호출.samo_za_branje_zastavica);
        확인(jedro_VALUE.체계호출().Datoteka_nadzor(jedro_VALUE.첫과정(), 서술자, 2, 1) == 0, "Izvedi_ukaz 시 Zapri Nastavitve");
        확인(jedro_VALUE.체계호출().Izvedi_ukaz(jedro_VALUE.첫과정(), podatki, new String[] {"시험", "값"}, new String[] {"jezik=slovenščina"}) == 0, "ELF Izvedi_ukaz IMAGE_VALUE 적재");
        확인(jedro_VALUE.첫과정().실행시작주소() == 0x04001000, "Izvedi_ukaz Zaženi naslov 반영");
        확인(jedro_VALUE.첫과정().실행인자().length == 2 && jedro_VALUE.첫과정().환경값().length == 1, "Izvedi_ukaz 인자와 환경");
        확인(!jedro_VALUE.첫과정().파일서술자().informacijska_tehnologija_odprto(서술자), "Izvedi_ukaz 시 서술자 Zapri");
        확인(jedro_VALUE.쪽관리().바이트읽기(jedro_VALUE.첫과정().naslov_Space(), 0x04002000) == 0, "빈 podatki odsek_VALUE nič_operand inicializirati");
    }

    private static void 입력시험(jedro jedro_VALUE) {
        jedro_VALUE.입력관리().Ključ_ne_deluje('가');
        jedro_VALUE.입력관리().쥐이동(3, -2);
        입력사건 첫사건 = jedro_VALUE.입력관리().Naprej_dogodek();
        입력사건 SECOND_dogodek = jedro_VALUE.입력관리().Naprej_dogodek();
        확인(첫사건.vrsta_dogodka() == 입력사건.종류.Ključ_ne_deluje, "자판 dogodek");
        확인(SECOND_dogodek.첫째값() == 3 && SECOND_dogodek.SECOND_VALUE() == -2, "쥐 premikati_VALUE dogodek");
    }

    private static void preskusiti_strojna_oprema(gostiti_strojna_oprema naprava_VALUE) {
        naprava_VALUE.pisati_vrata_bajt(0x3f8, 0xab);
        확인(naprava_VALUE.포트바이트읽기(0x3f8) == 0xab, "strojna_oprema_vrata V_I 경계");
        확인(naprava_VALUE.직렬기록().contains("JHunOS"), "직렬 LOG_zapis");
    }

    private static void 개입중단과서술자시험() {
        prekinitev_Upravitelj Upravitelj_VALUE = new prekinitev_Upravitelj();
        Upravitelj_VALUE.register_vnos(0x21, Senzor_prostora_naslov -> Senzor_prostora_naslov + 4);
        Upravitelj_VALUE.vklopiti();
        확인(Upravitelj_VALUE.distribuirati_VALUE(0x21, 100) == 104, "prekinitev distribuirati_VALUE");
        Upravitelj_VALUE.dezaktivirati();
        확인(Upravitelj_VALUE.distribuirati_VALUE(0x21, 100) == 100, "prekinitev dezaktivirati");

        GDT 서술자표 = new GDT();
        서술자표.nabor_privzeta_vrednost();
        확인(서술자표.조각들().size() == 5, "전역 서술자표");
        opravek_stanje_segment opravek_stanje = new opravek_stanje_segment();
        opravek_stanje.특권쌓임공간설정(0x10, 0x800000);
        확인(opravek_stanje.Sklad_nič_blok() == 0x10 && opravek_stanje.Sklad_nič_naslov() == 0x800000, "작업 stanje_VALUE odsek_VALUE");
    }

    private static void preskusiti_Senzor_prostora_AND_Uporaba_omrežij() {
        고급기술결합장치 naprava_za_shranjevanje = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.odsek_spremeniti_velikost];
        byte[] 읽은자료 = new byte[고급기술결합장치.odsek_spremeniti_velikost];
        쓸자료[17] = 42;
        naprava_za_shranjevanje.Pisanje(2, 쓸자료);
        naprava_za_shranjevanje.Branje(2, 읽은자료);
        확인(읽은자료[17] == 42, "ATA odsek_VALUE 읽고 Pisanje");

        zunanji_vodilo_Upravitelj zunanji_a0a72417 = new zunanji_vodilo_Upravitelj();
        zunanji_a0a72417.발견(new zunanji_vodilo_Upravitelj.naprava_VALUE(0x1022, 0x2000, 0xc000, 11));
        확인(zunanji_a0a72417.FIND_vnos(0x1022, 0x2000) != null, "주변 naprava_VALUE FIND_vnos");

        byte[] ethernet_okvir = new byte[34];
        ethernet_okvir[12] = 0x08;
        ethernet_okvir[13] = 0x00;
        ethernet_okvir[14] = 0x45;
        확인(mreža_Orodja.ethernet_UPPER_protokol(ethernet_okvir) == 0x0800, "이더넷 상위 primer_VALUE");
        확인(mreža_Orodja.상호통신망규약사판인가(ethernet_okvir, 14), "상호통신망규약 4판");
        확인(mreža_Orodja.oblak_kontrolna_vsota(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 kontrolna_vsota");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        pisati_celo_število_VALUE(첫구역, 454, 63);
        pisati_celo_število_VALUE(첫구역, 458, 1024);
        확인(new primarna_particija_tabela().Branje(첫구역).size() == 1, "privzeta_vrednost 분할 영역표");

        omrežna_plast sloj_VALUE = new omrežna_plast();
        int[] RECEIVED_COUNT = new int[1];
        sloj_VALUE.register_uporabnik_podatki_enota(7, (podatki, Zaženi, 길이) -> RECEIVED_COUNT[0]++);
        byte[] okvir_INDEX = new byte[14 + 20 + 8];
        okvir_INDEX[12] = 0x08;
        okvir_INDEX[13] = 0x00;
        okvir_INDEX[14] = 0x45;
        okvir_INDEX[16] = 0;
        okvir_INDEX[17] = 28;
        okvir_INDEX[23] = 17;
        okvir_INDEX[36] = 0;
        okvir_INDEX[37] = 7;
        확인(sloj_VALUE.sprejeti_sprejemati_prejeti_prejemati_ethernet(okvir_INDEX) && RECEIVED_COUNT[0] == 1, "uporabnik podatki enota_VALUE distribuirati_VALUE");
    }

    private static void 화면과시계시험() {
        znak_zaslon 화면 = new znak_zaslon();
        화면.Izpis("가나\n다");
        확인(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 Izpis");
        Ura Ura = new Ura(100);
        for (int INDEX = 0; INDEX < 10; INDEX++) {
            Ura.utrip_VALUE();
        }
        확인(Ura.지난밀리초() == 100, "Ura utrip_VALUE CONVERT_VALUE");
    }

    private static void pisati_celo_število_VALUE(byte[] podatki, int Položaj, int VALUE) {
        podatki[Položaj] = (byte) VALUE;
        podatki[Položaj + 1] = (byte) (VALUE >>> 8);
        podatki[Položaj + 2] = (byte) (VALUE >>> 16);
        podatki[Položaj + 3] = (byte) (VALUE >>> 24);
    }

    private static void 짧은정수쓰기(byte[] podatki, int Položaj, int VALUE) {
        podatki[Položaj] = (byte) VALUE;
        podatki[Položaj + 1] = (byte) (VALUE >>> 8);
    }

    private static void 확인(boolean pogoj, String Ime) {
        if (!pogoj) {
            throw new AssertionError("napaka_VALUE: " + Ime);
        }
        posredovati_COUNT++;
        System.out.println("posredovati_VALUE: " + Ime);
    }
}
