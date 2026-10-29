// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Suomi.JFinOS.testit;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Suomi.JFinOS.Muisti_alue.Muisti_Valvoja;
import Suomi.JFinOS.Muisti_alue.page_Valvoja;
import Suomi.JFinOS.syöte_ARVO.syöte_tapahtuma;
import Suomi.JFinOS.작업.prosessi_ARVO;
import Suomi.JFinOS.järjestelmäkutsu.järjestelmäkutsu;
import Suomi.JFinOS.tiedostojärjestelmä.suoritettava_tiedosto_latausohjelma;
import Suomi.JFinOS.ydin.ydin;
import Suomi.JFinOS.isäntä.isäntä_laitteisto;
import Suomi.JFinOS.IRQ.IRQ_Valvoja;
import Suomi.JFinOS.서술자.전역서술자표;
import Suomi.JFinOS.tallennuslaite.고급기술결합장치;
import Suomi.JFinOS.laite_ARVO.lisälaite_väylä_Valvoja;
import Suomi.JFinOS.verkko_Pino.verkko_Työkalut;
import Suomi.JFinOS.verkko_Pino.verkkotaso;
import Suomi.JFinOS.laite_ARVO.Kello;
import Suomi.JFinOS.서술자.tehtävä_Tila_segmentti;
import Suomi.JFinOS.화면.merkki_näyttö;
import Suomi.JFinOS.tiedostojärjestelmä.ensisijainen_osio_taulukko;

public final class 전체시험 {
    private static int välittää_LASKE;

    private 전체시험() {
    }

    public static void main(String[] parametri_argumentti) {
        isäntä_laitteisto laite_ARVO = new isäntä_laitteisto();
        ydin ydin_ARVO = new ydin(laite_ARVO);
        ydin_ARVO.Suorita_2();

        testi_Muisti(ydin_ARVO);
        쪽관리시험(ydin_ARVO);
        파일과과정시험(ydin_ARVO);
        실행파일시험(ydin_ARVO);
        testi_syöte(ydin_ARVO);
        testi_laitteisto(laite_ARVO);
        개입중단과서술자시험();
        testi_Tallennus_JA_Verkot();
        화면과시계시험();

        System.out.println("JFinOS testit välittää_ARVO: " + välittää_LASKE);
    }

    private static void testi_Muisti(ydin ydin_ARVO) {
        Muisti_Valvoja Valvoja_ARVO = ydin_ARVO.Muisti_alue();
        int 첫주소 = Valvoja_ARVO.정렬할당(100, 64);
        tarkistaa((첫주소 & 63) == 0, "tasaa_ARVO jakaa_Tallennus");
        Valvoja_ARVO.kirjoitus_tavu_ARVO(첫주소, (byte) 0x5a);
        tarkistaa(Valvoja_ARVO.lukea_tavu_ARVO(첫주소) == (byte) 0x5a, "물리 Muisti_alue 읽고 Kirjoitus");
        int 사용전 = Valvoja_ARVO.사용크기();
        Valvoja_ARVO.julkaista_Tallennus(첫주소);
        tarkistaa(Valvoja_ARVO.사용크기() < 사용전, "Muisti_alue julkaista_Tallennus");
    }

    private static void 쪽관리시험(ydin ydin_ARVO) {
        page_Valvoja Valvoja_ARVO = ydin_ARVO.쪽관리();
        page_Valvoja.osoiteavaruus pää_tila = Valvoja_ARVO.새주소공간();
        Valvoja_ARVO.MAP_page(pää_tila, 0x1000, true);
        Valvoja_ARVO.kirjoitus_tavu_ARVO(pää_tila, 0x1010, (byte) 7);
        page_Valvoja.osoiteavaruus ali_tila = Valvoja_ARVO.쓰기시복사복제(pää_tila);
        Valvoja_ARVO.kirjoitus_tavu_ARVO(ali_tila, 0x1010, (byte) 9);
        tarkistaa(Valvoja_ARVO.lukea_tavu_ARVO(pää_tila, 0x1010) == 7, "Kirjoitus 시 kopioida_ARVO pää_ARVO 격리");
        tarkistaa(Valvoja_ARVO.lukea_tavu_ARVO(ali_tila, 0x1010) == 9, "Kirjoitus 시 kopioida_ARVO ali_ARVO Kirjoitus");
    }

    private static void 파일과과정시험(ydin ydin_ARVO) {
        byte[] Sisältö_ARVO = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        ydin_ARVO.tiedostojärjestelmä().liitä_Tiedosto("testit", Sisältö_ARVO);
        prosessi_ARVO pää_ARVO = ydin_ARVO.첫과정();
        järjestelmäkutsu 호출 = ydin_ARVO.järjestelmäkutsu();
        int 서술자 = 호출.Avaa(pää_ARVO, "/testit", järjestelmäkutsu.vain_luku_merkitä);
        tarkistaa(서술자 >= 3, "tiedoston_nimi Avaa");

        byte[] saada_kohde = new byte[Sisältö_ARVO.length];
        tarkistaa(호출.Luku(pää_ARVO, 서술자, saada_kohde, saada_kohde.length) == Sisältö_ARVO.length, "tiedoston_nimi Luku");
        tarkistaa(Arrays.equals(Sisältö_ARVO, saada_kohde), "tiedoston_nimi Sisältö_ARVO");
        tarkistaa(호출.siirrä_toimi(pää_ARVO, 서술자, 0, järjestelmäkutsu.Hae_alku) == 0, "tiedoston_nimi paikka siirrä_ARVO_83b651b8");

        int 복제서술자 = 호출.서술자복제(pää_ARVO, 서술자);
        tarkistaa(복제서술자 >= 0, "서술자 klooni_ARVO");
        prosessi_ARVO ali_ARVO = 호출.klooni_prosessi(pää_ARVO);
        tarkistaa(ali_ARVO.tunniste_ARVO() != pää_ARVO.tunniste_ARVO(), "prosessi_ARVO tunniste_ARVO 분리");
        tarkistaa(ali_ARVO.pää_tunniste() == pää_ARVO.tunniste_ARVO(), "pää_ARVO prosessi_ARVO tunniste_ARVO");
        tarkistaa(호출.Sulje(ali_ARVO, 서술자) == 0 && pää_ARVO.파일서술자().tietojärjestelmät_avata(서술자), "ali_ARVO Sulje 격리");

        int Edellinen_lopettaa_puhelu = 호출.lisäys_ohjelma_tauko(pää_ARVO, 8192);
        tarkistaa(Edellinen_lopettaa_puhelu == 0x06000000, "ohjelma_f5044b9b 끝 늘리기");
        tarkistaa(pää_ARVO.ohjelma_tauko() == 0x06002000, "ohjelma_f5044b9b 끝 반영");
        tarkistaa(ali_ARVO.ohjelma_tauko() == 0x06000000, "과정별 ohjelma_f5044b9b 끝 격리");

        ali_ARVO.Lopeta_ohjelma(7);
        tarkistaa(호출.자식기다리기(pää_ARVO, ali_ARVO.tunniste_ARVO(), false) == (7 << 8), "ali_ARVO Lopeta_ohjelma 기다리기");
        tarkistaa(호출.접근가능("testit", 1) == -13, "Suorita_komento lupa_ARVO hylkää_ARVO_e3ecc00b");
        tarkistaa(호출.IUD() == 0 && 호출.Ryhmä_tunniste() == 0, "사용자와 무리 tunniste_ARVO");
        tarkistaa("/".equals(호출.nykyinen_Tehtäväluettelo(2)) && 호출.MUUTA_Tehtäväluettelo("/") == 0, "nykyinen_kohde 작업 merkintä_luettelo");
        tarkistaa(호출.tietojärjestelmät_Pääte(pää_ARVO, 1), "표준 tulostuspaikka 단말");
        tarkistaa("JFinOS".equals(호출.Järjestelmä_Tiedot().Järjestelmä_nimi()), "käyttöjärjestelmä_ARVO msinfo32_exe");
    }

    private static void 실행파일시험(ydin ydin_ARVO) {
        byte[] data = new byte[92];
        data[0] = 0x7f;
        data[1] = 'E';
        data[2] = 'L';
        data[3] = 'F';
        data[4] = 1;
        data[5] = 1;
        kirjoitus_kokonaisluku_ARVO(data, 24, 0x04001000);
        kirjoitus_kokonaisluku_ARVO(data, 32, 52);
        짧은정수쓰기(data, 46, 40);
        짧은정수쓰기(data, 48, 1);
        kirjoitus_kokonaisluku_ARVO(data, 56, 8);
        kirjoitus_kokonaisluku_ARVO(data, 60, 2);
        kirjoitus_kokonaisluku_ARVO(data, 64, 0x04002000);
        kirjoitus_kokonaisluku_ARVO(data, 72, 64);

        suoritettava_tiedosto_latausohjelma.KUVA KUVA_ARVO = new suoritettava_tiedosto_latausohjelma().검사(data);
        tarkistaa(KUVA_ARVO.alku_OSOITE() == 0x04001000, "ELF Suorita_2 OSOITE");
        tarkistaa(KUVA_ARVO.구역들().size() == 1 && KUVA_ARVO.구역들().get(0).종류() == 8, "ELF 빈 data osa_ARVO");
        int 서술자 = ydin_ARVO.järjestelmäkutsu().Avaa(ydin_ARVO.첫과정(), "testit", järjestelmäkutsu.vain_luku_merkitä);
        tarkistaa(ydin_ARVO.järjestelmäkutsu().tiedoston_ohjaus(ydin_ARVO.첫과정(), 서술자, 2, 1) == 0, "Suorita_komento 시 Sulje Asetukset");
        tarkistaa(ydin_ARVO.järjestelmäkutsu().Suorita_komento(ydin_ARVO.첫과정(), data, new String[] {"testit", "값"}, new String[] {"Kieli=suomi"}) == 0, "ELF Suorita_komento KUVA_ARVO 적재");
        tarkistaa(ydin_ARVO.첫과정().suoritus_alku_OSOITE() == 0x04001000, "Suorita_komento Suorita_2 OSOITE 반영");
        tarkistaa(ydin_ARVO.첫과정().suoritus_argumentti().length == 2 && ydin_ARVO.첫과정().ympäristö_ARVO().length == 1, "Suorita_komento 인자와 ympäristö");
        tarkistaa(!ydin_ARVO.첫과정().파일서술자().tietojärjestelmät_avata(서술자), "Suorita_komento 시 서술자 Sulje");
        tarkistaa(ydin_ARVO.쪽관리().lukea_tavu_ARVO(ydin_ARVO.첫과정().osoiteavaruus(), 0x04002000) == 0, "빈 data osa_ARVO nolla_operandi alustaa");
    }

    private static void testi_syöte(ydin ydin_ARVO) {
        ydin_ARVO.입력관리().Avain_ei_toiminnassa('가');
        ydin_ARVO.입력관리().쥐이동(3, -2);
        syöte_tapahtuma 첫사건 = ydin_ARVO.입력관리().Seuraava_tapahtuma();
        syöte_tapahtuma SEKUNNIT_tapahtuma = ydin_ARVO.입력관리().Seuraava_tapahtuma();
        tarkistaa(첫사건.tapahtumatyyppi() == syöte_tapahtuma.종류.Avain_ei_toiminnassa, "자판 Tapahtuma");
        tarkistaa(SEKUNNIT_tapahtuma.첫째값() == 3 && SEKUNNIT_tapahtuma.SEKUNNIT_ARVO() == -2, "쥐 siirrä_ARVO_83b651b8 Tapahtuma");
    }

    private static void testi_laitteisto(isäntä_laitteisto laite_ARVO) {
        laite_ARVO.kirjoitus_portti_tavu(0x3f8, 0xab);
        tarkistaa(laite_ARVO.lukea_portti_tavu(0x3f8) == 0xab, "laitteisto_portti I_O rajattu_alue_ARVO");
        tarkistaa(laite_ARVO.직렬기록().contains("JFinOS"), "직렬 LOG_TIETUE");
    }

    private static void 개입중단과서술자시험() {
        IRQ_Valvoja Valvoja_ARVO = new IRQ_Valvoja();
        Valvoja_ARVO.rekisteri_merkintä(0x21, Tallennus_OSOITE -> Tallennus_OSOITE + 4);
        Valvoja_ARVO.ota_käyttöön();
        tarkistaa(Valvoja_ARVO.jaa_ARVO(0x21, 100) == 104, "IRQ jaa_ARVO");
        Valvoja_ARVO.poistaa_aktivointi();
        tarkistaa(Valvoja_ARVO.jaa_ARVO(0x21, 100) == 100, "IRQ poistaa_aktivointi");

        전역서술자표 서술자표 = new 전역서술자표();
        서술자표.ryhmä_oletusarvo();
        tarkistaa(서술자표.조각들().size() == 5, "전역 서술자표");
        tehtävä_Tila_segmentti tehtävä_Tila = new tehtävä_Tila_segmentti();
        tehtävä_Tila.특권쌓임공간설정(0x10, 0x800000);
        tarkistaa(tehtävä_Tila.Pino_nolla_Esto() == 0x10 && tehtävä_Tila.Pino_nolla_OSOITE() == 0x800000, "작업 Tila_ARVO osa_ARVO");
    }

    private static void testi_Tallennus_JA_Verkot() {
        고급기술결합장치 tallennuslaite = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.osa_muuttaa_kokoa];
        byte[] lukea_data_ARVO = new byte[고급기술결합장치.osa_muuttaa_kokoa];
        쓸자료[17] = 42;
        tallennuslaite.Kirjoitus(2, 쓸자료);
        tallennuslaite.Luku(2, lukea_data_ARVO);
        tarkistaa(lukea_data_ARVO[17] == 42, "ATA osa_ARVO 읽고 Kirjoitus");

        lisälaite_väylä_Valvoja lisälaite = new lisälaite_väylä_Valvoja();
        lisälaite.발견(new lisälaite_väylä_Valvoja.laite_ARVO(0x1022, 0x2000, 0xc000, 11));
        tarkistaa(lisälaite.ETSI_merkintä(0x1022, 0x2000) != null, "주변 laite_ARVO ETSI_merkintä");

        byte[] Ethernet_kuva = new byte[34];
        Ethernet_kuva[12] = 0x08;
        Ethernet_kuva[13] = 0x00;
        Ethernet_kuva[14] = 0x45;
        tarkistaa(verkko_Työkalut.Ethernet_ISOT_protokolla(Ethernet_kuva) == 0x0800, "이더넷 상위 sopimuksen_arvo");
        tarkistaa(verkko_Työkalut.tietojärjestelmät_IPV_4_protokolla(Ethernet_kuva, 14), "상호통신망규약 4판");
        tarkistaa(verkko_Työkalut.pilvi_tarkistussumma(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 tarkistussumma");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        kirjoitus_kokonaisluku_ARVO(첫구역, 454, 63);
        kirjoitus_kokonaisluku_ARVO(첫구역, 458, 1024);
        tarkistaa(new ensisijainen_osio_taulukko().Luku(첫구역).size() == 1, "oletusarvo 분할 영역표");

        verkkotaso kerros_ARVO_e65604ef = new verkkotaso();
        int[] SAATU_HINTA_LASKE = new int[1];
        kerros_ARVO_e65604ef.rekisteri_käyttäjä_data_osio(7, (data, Suorita_2, kesto_ARVO) -> SAATU_HINTA_LASKE[0]++);
        byte[] kuva_INDEKSI = new byte[14 + 20 + 8];
        kuva_INDEKSI[12] = 0x08;
        kuva_INDEKSI[13] = 0x00;
        kuva_INDEKSI[14] = 0x45;
        kuva_INDEKSI[16] = 0;
        kuva_INDEKSI[17] = 28;
        kuva_INDEKSI[23] = 17;
        kuva_INDEKSI[36] = 0;
        kuva_INDEKSI[37] = 7;
        tarkistaa(kerros_ARVO_e65604ef.saada_Ethernet(kuva_INDEKSI) && SAATU_HINTA_LASKE[0] == 1, "käyttäjätila data osio_ARVO_7c611f50 jaa_ARVO");
    }

    private static void 화면과시계시험() {
        merkki_näyttö 화면 = new merkki_näyttö();
        화면.tulostuspaikka("가나\n다");
        tarkistaa(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 tulostuspaikka");
        Kello Kello = new Kello(100);
        for (int INDEKSI = 0; INDEKSI < 10; INDEKSI++) {
            Kello.tikitys_ARVO();
        }
        tarkistaa(Kello.지난밀리초() == 100, "Kello tikitys_ARVO MUUNNA_ARVO");
    }

    private static void kirjoitus_kokonaisluku_ARVO(byte[] data, int paikka, int ARVO) {
        data[paikka] = (byte) ARVO;
        data[paikka + 1] = (byte) (ARVO >>> 8);
        data[paikka + 2] = (byte) (ARVO >>> 16);
        data[paikka + 3] = (byte) (ARVO >>> 24);
    }

    private static void 짧은정수쓰기(byte[] data, int paikka, int ARVO) {
        data[paikka] = (byte) ARVO;
        data[paikka + 1] = (byte) (ARVO >>> 8);
    }

    private static void tarkistaa(boolean ehto, String Nimi) {
        if (!ehto) {
            throw new AssertionError("virhe_ARVO: " + Nimi);
        }
        välittää_LASKE++;
        System.out.println("välittää_ARVO: " + Nimi);
    }
}
