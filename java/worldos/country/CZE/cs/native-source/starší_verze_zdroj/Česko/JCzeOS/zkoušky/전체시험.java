// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Česko.JCzeOS.zkoušky;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Česko.JCzeOS.Paměť_oblast.Paměť_Správce;
import Česko.JCzeOS.Paměť_oblast.stránka_Správce;
import Česko.JCzeOS.vstup_HODNOTA.vstup_událost;
import Česko.JCzeOS.작업.Proces_HODNOTA;
import Česko.JCzeOS.systémové_volání.systémové_volání;
import Česko.JCzeOS.systém_souborů.spustitelný_zavaděč;
import Česko.JCzeOS.jádro.jádro;
import Česko.JCzeOS.hostit.hostit_hardware;
import Česko.JCzeOS.přerušení.přerušení_Správce;
import Česko.JCzeOS.popisovač_položka.Globální_popisovač_tabulka;
import Česko.JCzeOS.úložiště.고급기술결합장치;
import Česko.JCzeOS.mobilní_HODNOTA.periferie_sběrnice_Správce;
import Česko.JCzeOS.síť_Štos.síť_Nástroje;
import Česko.JCzeOS.síť_Štos.síťová_vrstva;
import Česko.JCzeOS.mobilní_HODNOTA.Hodiny;
import Česko.JCzeOS.popisovač_položka.úkol_Stav_segment;
import Česko.JCzeOS.화면.znak_displej;
import Česko.JCzeOS.systém_souborů.primární_oddíl_tabulka;

public final class 전체시험 {
    private static int předat_POČET;

    private 전체시험() {
    }

    public static void main(String[] parametr_argument) {
        hostit_hardware mobilní_HODNOTA = new hostit_hardware();
        jádro jádro_HODNOTA = new jádro(mobilní_HODNOTA);
        jádro_HODNOTA.Spustit_2();

        test_Paměť(jádro_HODNOTA);
        쪽관리시험(jádro_HODNOTA);
        파일과과정시험(jádro_HODNOTA);
        실행파일시험(jádro_HODNOTA);
        test_vstup(jádro_HODNOTA);
        test_hardware(mobilní_HODNOTA);
        개입중단과서술자시험();
        test_Storage_A_Sítě();
        화면과시계시험();

        System.out.println("JCzeOS zkoušky předat_HODNOTA: " + předat_POČET);
    }

    private static void test_Paměť(jádro jádro_HODNOTA) {
        Paměť_Správce Správce_HODNOTA = jádro_HODNOTA.Paměť_oblast();
        int 첫주소 = Správce_HODNOTA.정렬할당(100, 64);
        ověřit((첫주소 & 63) == 0, "zarovnat_HODNOTA přidělit_Storage");
        Správce_HODNOTA.zápis_bajt_HODNOTA(첫주소, (byte) 0x5a);
        ověřit(Správce_HODNOTA.바이트읽기(첫주소) == (byte) 0x5a, "물리 Paměť_oblast 읽고 Zápis");
        int 사용전 = Správce_HODNOTA.사용크기();
        Správce_HODNOTA.verze_Storage(첫주소);
        ověřit(Správce_HODNOTA.사용크기() < 사용전, "Paměť_oblast verze_Storage");
    }

    private static void 쪽관리시험(jádro jádro_HODNOTA) {
        stránka_Správce Správce_HODNOTA = jádro_HODNOTA.쪽관리();
        stránka_Správce.adresní_prostor nadřazený_Space = Správce_HODNOTA.새주소공간();
        Správce_HODNOTA.MAP_stránka(nadřazený_Space, 0x1000, true);
        Správce_HODNOTA.zápis_bajt_HODNOTA(nadřazený_Space, 0x1010, (byte) 7);
        stránka_Správce.adresní_prostor dítě_Space = Správce_HODNOTA.쓰기시복사복제(nadřazený_Space);
        Správce_HODNOTA.zápis_bajt_HODNOTA(dítě_Space, 0x1010, (byte) 9);
        ověřit(Správce_HODNOTA.바이트읽기(nadřazený_Space, 0x1010) == 7, "Zápis 시 instance_HODNOTA nadřazený_HODNOTA 격리");
        ověřit(Správce_HODNOTA.바이트읽기(dítě_Space, 0x1010) == 9, "Zápis 시 instance_HODNOTA dítě_HODNOTA Zápis");
    }

    private static void 파일과과정시험(jádro jádro_HODNOTA) {
        byte[] Obsah_HODNOTA = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        jádro_HODNOTA.systém_souborů().Připojit_Soubor("zkoušky", Obsah_HODNOTA);
        Proces_HODNOTA nadřazený_HODNOTA = jádro_HODNOTA.첫과정();
        systémové_volání 호출 = jádro_HODNOTA.systémové_volání();
        int popisovač_položka = 호출.Otevřít(nadřazený_HODNOTA, "/zkoušky", systémové_volání.jen_pro_čtení_příznak);
        ověřit(popisovač_položka >= 3, "název_souboru Otevřít");

        byte[] dostat_cíl = new byte[Obsah_HODNOTA.length];
        ověřit(호출.Čtení(nadřazený_HODNOTA, popisovač_položka, dostat_cíl, dostat_cíl.length) == Obsah_HODNOTA.length, "název_souboru Čtení");
        ověřit(Arrays.equals(Obsah_HODNOTA, dostat_cíl), "název_souboru Obsah_HODNOTA");
        ověřit(호출.přesunout_pozice(nadřazený_HODNOTA, popisovač_položka, 0, systémové_volání.HLEDAT_START) == 0, "název_souboru pozice přesunout_HODNOTA");

        int 복제서술자 = 호출.duplikát_popisovač(nadřazený_HODNOTA, popisovač_položka);
        ověřit(복제서술자 >= 0, "popisovač_položka klon_HODNOTA");
        Proces_HODNOTA dítě_HODNOTA = 호출.klon_Proces(nadřazený_HODNOTA);
        ověřit(dítě_HODNOTA.identifikátor_HODNOTA() != nadřazený_HODNOTA.identifikátor_HODNOTA(), "Proces_HODNOTA identifikátor_HODNOTA 분리");
        ověřit(dítě_HODNOTA.nadřazený_identifikátor() == nadřazený_HODNOTA.identifikátor_HODNOTA(), "nadřazený_HODNOTA Proces_HODNOTA identifikátor_HODNOTA");
        ověřit(호출.Zavřené(dítě_HODNOTA, popisovač_položka) == 0 && nadřazený_HODNOTA.Soubor_popisovač().informační_systémy_otevřít(popisovač_položka), "dítě_HODNOTA Zavřené 격리");

        int Předchozí_konec = 호출.zvýšení_program_přerušení(nadřazený_HODNOTA, 8192);
        ověřit(Předchozí_konec == 0x06000000, "program_f5044b9b 끝 늘리기");
        ověřit(nadřazený_HODNOTA.program_přerušení() == 0x06002000, "program_f5044b9b 끝 반영");
        ověřit(dítě_HODNOTA.program_přerušení() == 0x06000000, "과정별 program_f5044b9b 끝 격리");

        dítě_HODNOTA.Konec_program(7);
        ověřit(호출.자식기다리기(nadřazený_HODNOTA, dítě_HODNOTA.identifikátor_HODNOTA(), false) == (7 << 8), "dítě_HODNOTA Konec_program 기다리기");
        ověřit(호출.접근가능("zkoušky", 1) == -13, "Provést_příkaz oprávnění_HODNOTA odmítnout_HODNOTA");
        ověřit(호출.ID_uživatele() == 0 && 호출.ID_skupiny() == 0, "사용자와 무리 identifikátor_HODNOTA");
        ověřit("/".equals(호출.dobrá_Seznam_úkolů(2)) && 호출.SWITCH_Seznam_úkolů("/") == 0, "dobrá_zboží 작업 položka_Seznam");
        ověřit(호출.informační_systémy_Terminál(nadřazený_HODNOTA, 1), "표준 výstupní_pozice 단말");
        ověřit("JCzeOS".equals(호출.Systém_Podrobnosti().Systém_název()), "operační_systém_HODNOTA Informace_o_systému");
    }

    private static void 실행파일시험(jádro jádro_HODNOTA) {
        byte[] data = new byte[92];
        data[0] = 0x7f;
        data[1] = 'E';
        data[2] = 'L';
        data[3] = 'F';
        data[4] = 1;
        data[5] = 1;
        zápis_integer_HODNOTA(data, 24, 0x04001000);
        zápis_integer_HODNOTA(data, 32, 52);
        짧은정수쓰기(data, 46, 40);
        짧은정수쓰기(data, 48, 1);
        zápis_integer_HODNOTA(data, 56, 8);
        zápis_integer_HODNOTA(data, 60, 2);
        zápis_integer_HODNOTA(data, 64, 0x04002000);
        zápis_integer_HODNOTA(data, 72, 64);

        spustitelný_zavaděč.image image_HODNOTA = new spustitelný_zavaděč().검사(data);
        ověřit(image_HODNOTA.START_ODKAZ() == 0x04001000, "ELF Spustit_2 Adresa");
        ověřit(image_HODNOTA.구역들().size() == 1 && image_HODNOTA.구역들().get(0).Druh_HODNOTA() == 8, "ELF 빈 data oddíl_HODNOTA_366e0bfa");
        int popisovač_položka = jádro_HODNOTA.systémové_volání().Otevřít(jádro_HODNOTA.첫과정(), "zkoušky", systémové_volání.jen_pro_čtení_příznak);
        ověřit(jádro_HODNOTA.systémové_volání().řízení_souboru(jádro_HODNOTA.첫과정(), popisovač_položka, 2, 1) == 0, "Provést_příkaz 시 Zavřené Nastavení");
        ověřit(jádro_HODNOTA.systémové_volání().Provést_příkaz(jádro_HODNOTA.첫과정(), data, new String[] {"zkoušky", "값"}, new String[] {"Jazyk=čeština"}) == 0, "ELF Provést_příkaz image_HODNOTA 적재");
        ověřit(jádro_HODNOTA.첫과정().spuštění_START_ODKAZ() == 0x04001000, "Provést_příkaz Spustit_2 Adresa 반영");
        ověřit(jádro_HODNOTA.첫과정().spuštění_argument().length == 2 && jádro_HODNOTA.첫과정().prostředí_HODNOTA().length == 1, "Provést_příkaz 인자와 prostředí_5d36e09c");
        ověřit(!jádro_HODNOTA.첫과정().Soubor_popisovač().informační_systémy_otevřít(popisovač_položka), "Provést_příkaz 시 popisovač_položka Zavřené");
        ověřit(jádro_HODNOTA.쪽관리().바이트읽기(jádro_HODNOTA.첫과정().adresní_prostor(), 0x04002000) == 0, "빈 data oddíl_HODNOTA_366e0bfa nula_operand inicializovat");
    }

    private static void test_vstup(jádro jádro_HODNOTA) {
        jádro_HODNOTA.입력관리().Klíč_mimo_provoz('가');
        jádro_HODNOTA.입력관리().쥐이동(3, -2);
        vstup_událost 첫사건 = jádro_HODNOTA.입력관리().Další_událost();
        vstup_událost SEKUNDA_událost = jádro_HODNOTA.입력관리().Další_událost();
        ověřit(첫사건.událost_Druh() == vstup_událost.Druh_HODNOTA.Klíč_mimo_provoz, "자판 Události");
        ověřit(SEKUNDA_událost.첫째값() == 3 && SEKUNDA_událost.SEKUNDA_HODNOTA() == -2, "쥐 přesunout_HODNOTA Události");
    }

    private static void test_hardware(hostit_hardware mobilní_HODNOTA) {
        mobilní_HODNOTA.zápis_port_bajt(0x3f8, 0xab);
        ověřit(mobilní_HODNOTA.포트바이트읽기(0x3f8) == 0xab, "hardware_port vstup_a_výstup mez_HODNOTA");
        ověřit(mobilní_HODNOTA.직렬기록().contains("JCzeOS"), "직렬 LOGZ_ZÁZNAM");
    }

    private static void 개입중단과서술자시험() {
        přerušení_Správce Správce_HODNOTA = new přerušení_Správce();
        Správce_HODNOTA.registr_položka(0x21, Storage_ODKAZ -> Storage_ODKAZ + 4);
        Správce_HODNOTA.povolit();
        ověřit(Správce_HODNOTA.distribuovat_HODNOTA(0x21, 100) == 104, "přerušení distribuovat_HODNOTA");
        Správce_HODNOTA.pozastavit();
        ověřit(Správce_HODNOTA.distribuovat_HODNOTA(0x21, 100) == 100, "přerušení pozastavit");

        Globální_popisovač_tabulka popisovač_tabulka = new Globální_popisovač_tabulka();
        popisovač_tabulka.sada_výchozí_hodnota();
        ověřit(popisovač_tabulka.조각들().size() == 5, "전역 popisovač_tabulka");
        úkol_Stav_segment úkol_Stav = new úkol_Stav_segment();
        úkol_Stav.특권쌓임공간설정(0x10, 0x800000);
        ověřit(úkol_Stav.Štos_nula_blok() == 0x10 && úkol_Stav.Štos_nula_ODKAZ() == 0x800000, "작업 Stav_HODNOTA oddíl_HODNOTA_366e0bfa");
    }

    private static void test_Storage_A_Sítě() {
        고급기술결합장치 úložiště = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.oddíl_změnit_velikost];
        byte[] 읽은자료 = new byte[고급기술결합장치.oddíl_změnit_velikost];
        쓸자료[17] = 42;
        úložiště.Zápis(2, 쓸자료);
        úložiště.Čtení(2, 읽은자료);
        ověřit(읽은자료[17] == 42, "ATA oddíl_HODNOTA_366e0bfa 읽고 Zápis");

        periferie_sběrnice_Správce periferie = new periferie_sběrnice_Správce();
        periferie.발견(new periferie_sběrnice_Správce.mobilní_HODNOTA(0x1022, 0x2000, 0xc000, 11));
        ověřit(periferie.NAJÍT_položka(0x1022, 0x2000) != null, "주변 mobilní_HODNOTA NAJÍT_položka");

        byte[] síť_Ethernet_rámec = new byte[34];
        síť_Ethernet_rámec[12] = 0x08;
        síť_Ethernet_rámec[13] = 0x00;
        síť_Ethernet_rámec[14] = 0x45;
        ověřit(síť_Nástroje.síť_Ethernet_VELKÁ_protokol(síť_Ethernet_rámec) == 0x0800, "이더넷 상위 hodnota_smlouvy");
        ověřit(síť_Nástroje.informační_systémy_OCF_4_protokol(síť_Ethernet_rámec, 14), "상호통신망규약 4판");
        ověřit(síť_Nástroje.cloud_kontrolní_součet(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 kontrolní_součet");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        zápis_integer_HODNOTA(첫구역, 454, 63);
        zápis_integer_HODNOTA(첫구역, 458, 1024);
        ověřit(new primární_oddíl_tabulka().Čtení(첫구역).size() == 1, "výchozí_hodnota 분할 영역표");

        síťová_vrstva vrstva_HODNOTA = new síťová_vrstva();
        int[] RECEIVED_POČET = new int[1];
        vrstva_HODNOTA.registr_uživatel_data_lekce(7, (data, Spustit_2, délka_HODNOTA) -> RECEIVED_POČET[0]++);
        byte[] rámec_INDEX = new byte[14 + 20 + 8];
        rámec_INDEX[12] = 0x08;
        rámec_INDEX[13] = 0x00;
        rámec_INDEX[14] = 0x45;
        rámec_INDEX[16] = 0;
        rámec_INDEX[17] = 28;
        rámec_INDEX[23] = 17;
        rámec_INDEX[36] = 0;
        rámec_INDEX[37] = 7;
        ověřit(vrstva_HODNOTA.dostat_síť_Ethernet(rámec_INDEX) && RECEIVED_POČET[0] == 1, "uživatelský_prostor data lekce_HODNOTA distribuovat_HODNOTA");
    }

    private static void 화면과시계시험() {
        znak_displej 화면 = new znak_displej();
        화면.výstupní_pozice("가나\n다");
        ověřit(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 výstupní_pozice");
        Hodiny Hodiny = new Hodiny(100);
        for (int INDEX = 0; INDEX < 10; INDEX++) {
            Hodiny.틱();
        }
        ověřit(Hodiny.지난밀리초() == 100, "Hodiny 틱 CONVERT_HODNOTA");
    }

    private static void zápis_integer_HODNOTA(byte[] data, int pozice, int HODNOTA) {
        data[pozice] = (byte) HODNOTA;
        data[pozice + 1] = (byte) (HODNOTA >>> 8);
        data[pozice + 2] = (byte) (HODNOTA >>> 16);
        data[pozice + 3] = (byte) (HODNOTA >>> 24);
    }

    private static void 짧은정수쓰기(byte[] data, int pozice, int HODNOTA) {
        data[pozice] = (byte) HODNOTA;
        data[pozice + 1] = (byte) (HODNOTA >>> 8);
    }

    private static void ověřit(boolean podmínka, String Název) {
        if (!podmínka) {
            throw new AssertionError("selhání_HODNOTA: " + Název);
        }
        předat_POČET++;
        System.out.println("předat_HODNOTA: " + Název);
    }
}
