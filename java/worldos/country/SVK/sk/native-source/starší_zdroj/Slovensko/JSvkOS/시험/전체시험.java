// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovensko.JSvkOS.시험;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Slovensko.JSvkOS.Pamäť_oblasť.기억공간관리자;
import Slovensko.JSvkOS.Pamäť_oblasť.쪽관리자;
import Slovensko.JSvkOS.vstup_VALUE.vstup_udalosť;
import Slovensko.JSvkOS.작업.Proces_VALUE;
import Slovensko.JSvkOS.체계호출.체계호출;
import Slovensko.JSvkOS.systém_súborov.spustiteľný_súbor_zavádzací_program;
import Slovensko.JSvkOS.jadro.jadro;
import Slovensko.JSvkOS.hostiteľ.hostiteľ_hardvér;
import Slovensko.JSvkOS.IRQ.개입중단관리자;
import Slovensko.JSvkOS.서술자.전역서술자표;
import Slovensko.JSvkOS.úložné_zariadenie.고급기술결합장치;
import Slovensko.JSvkOS.telefón_VALUE.주변장치연결관리자;
import Slovensko.JSvkOS.sieť_Vrstvy.sieť_Nástroje;
import Slovensko.JSvkOS.sieť_Vrstvy.sieťová_vrstva;
import Slovensko.JSvkOS.telefón_VALUE.Hodiny;
import Slovensko.JSvkOS.서술자.úloha_Stav_segment;
import Slovensko.JSvkOS.화면.znak_displej;
import Slovensko.JSvkOS.systém_súborov.기본분할영역표;

public final class 전체시험 {
    private static int odovzdať_COUNT;

    private 전체시험() {
    }

    public static void main(String[] parameter_argument) {
        hostiteľ_hardvér telefón_VALUE = new hostiteľ_hardvér();
        jadro jadro_VALUE = new jadro(telefón_VALUE);
        jadro_VALUE.Spustiť_2();

        test_Pamäť(jadro_VALUE);
        쪽관리시험(jadro_VALUE);
        파일과과정시험(jadro_VALUE);
        실행파일시험(jadro_VALUE);
        test_vstup(jadro_VALUE);
        test_hardvér(telefón_VALUE);
        개입중단과서술자시험();
        test_Úložisko_AND_Siete();
        화면과시계시험();

        System.out.println("JSvkOS 시험 odovzdať_VALUE: " + odovzdať_COUNT);
    }

    private static void test_Pamäť(jadro jadro_VALUE) {
        기억공간관리자 관리자 = jadro_VALUE.Pamäť_oblasť();
        int 첫주소 = 관리자.정렬할당(100, 64);
        overiť((첫주소 & 63) == 0, "zarovnať_VALUE vyhradiť_Úložisko");
        관리자.zapísať_Byte_VALUE(첫주소, (byte) 0x5a);
        overiť(관리자.바이트읽기(첫주소) == (byte) 0x5a, "물리 Pamäť_oblasť 읽고 Zápis");
        int 사용전 = 관리자.사용크기();
        관리자.vydať_Úložisko(첫주소);
        overiť(관리자.사용크기() < 사용전, "Pamäť_oblasť vydať_Úložisko");
    }

    private static void 쪽관리시험(jadro jadro_VALUE) {
        쪽관리자 관리자 = jadro_VALUE.쪽관리();
        쪽관리자.adresa_priestor nadradený_priestor = 관리자.새주소공간();
        관리자.MAP_strana(nadradený_priestor, 0x1000, true);
        관리자.zapísať_Byte_VALUE(nadradený_priestor, 0x1010, (byte) 7);
        쪽관리자.adresa_priestor dieťa_priestor = 관리자.쓰기시복사복제(nadradený_priestor);
        관리자.zapísať_Byte_VALUE(dieťa_priestor, 0x1010, (byte) 9);
        overiť(관리자.바이트읽기(nadradený_priestor, 0x1010) == 7, "Zápis 시 inštancia_VALUE nadradený_VALUE 격리");
        overiť(관리자.바이트읽기(dieťa_priestor, 0x1010) == 9, "Zápis 시 inštancia_VALUE dieťa_VALUE Zápis");
    }

    private static void 파일과과정시험(jadro jadro_VALUE) {
        byte[] obsah_VALUE = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        jadro_VALUE.systém_súborov().Pripojiť_Súbor("시험", obsah_VALUE);
        Proces_VALUE nadradený_VALUE = jadro_VALUE.첫과정();
        체계호출 호출 = jadro_VALUE.체계호출();
        int 서술자 = 호출.Otvoriť(nadradený_VALUE, "/시험", 체계호출.iba_na_čítanie_príznak);
        overiť(서술자 >= 3, "Súbor Otvoriť");

        byte[] dostať_cieľ = new byte[obsah_VALUE.length];
        overiť(호출.Čítanie(nadradený_VALUE, 서술자, dostať_cieľ, dostať_cieľ.length) == obsah_VALUE.length, "Súbor Čítanie");
        overiť(Arrays.equals(obsah_VALUE, dostať_cieľ), "Súbor obsah_VALUE");
        overiť(호출.premiestniť_pozícia(nadradený_VALUE, 서술자, 0, 체계호출.Hľadať_START) == 0, "Súbor Pozícia premiestniť_VALUE");

        int 복제서술자 = 호출.서술자복제(nadradený_VALUE, 서술자);
        overiť(복제서술자 >= 0, "서술자 klon_VALUE");
        Proces_VALUE dieťa_VALUE = 호출.klon_Proces(nadradený_VALUE);
        overiť(dieťa_VALUE.identifikátor_VALUE() != nadradený_VALUE.identifikátor_VALUE(), "Proces_VALUE identifikátor_VALUE 분리");
        overiť(dieťa_VALUE.nadradený_identifikátor() == nadradený_VALUE.identifikátor_VALUE(), "nadradený_VALUE Proces_VALUE identifikátor_VALUE");
        overiť(호출.Zatvoriť(dieťa_VALUE, 서술자) == 0 && nadradený_VALUE.파일서술자().Informačné_systémy_otvoriť(서술자), "dieťa_VALUE Zatvoriť 격리");

        int 이전끝 = 호출.zvýšenie_program_prerušiť(nadradený_VALUE, 8192);
        overiť(이전끝 == 0x06000000, "program_f5044b9b 끝 늘리기");
        overiť(nadradený_VALUE.program_prerušiť() == 0x06002000, "program_f5044b9b 끝 반영");
        overiť(dieťa_VALUE.program_prerušiť() == 0x06000000, "과정별 program_f5044b9b 끝 격리");

        dieťa_VALUE.Skončiť_program(7);
        overiť(호출.자식기다리기(nadradený_VALUE, dieťa_VALUE.identifikátor_VALUE(), false) == (7 << 8), "dieťa_VALUE Skončiť_program 기다리기");
        overiť(호출.접근가능("시험", 1) == -13, "Vykonať_príkaz povolenie_VALUE odmietnuť_VALUE");
        overiť(호출.identifikácia_používateľa() == 0 && 호출.Skupina_identifikátor() == 0, "사용자와 무리 identifikátor_VALUE");
        overiť("/".equals(호출.v_termíne_splatnosti_zoznam_úloh(2)) && 호출.SWITCH_zoznam_úloh("/") == 0, "v_termíne_splatnosti_položka 작업 položka_Zoznam");
        overiť(호출.Informačné_systémy_Terminál(nadradený_VALUE, 1), "표준 Výstup 단말");
        overiť("JSvkOS".equals(호출.systém_Podrobnosti().systém_názov()), "operačný_systém_VALUE Systémové_informácie");
    }

    private static void 실행파일시험(jadro jadro_VALUE) {
        byte[] údaje = new byte[92];
        údaje[0] = 0x7f;
        údaje[1] = 'E';
        údaje[2] = 'L';
        údaje[3] = 'F';
        údaje[4] = 1;
        údaje[5] = 1;
        zapísať_celé_číslo_VALUE(údaje, 24, 0x04001000);
        zapísať_celé_číslo_VALUE(údaje, 32, 52);
        짧은정수쓰기(údaje, 46, 40);
        짧은정수쓰기(údaje, 48, 1);
        zapísať_celé_číslo_VALUE(údaje, 56, 8);
        zapísať_celé_číslo_VALUE(údaje, 60, 2);
        zapísať_celé_číslo_VALUE(údaje, 64, 0x04002000);
        zapísať_celé_číslo_VALUE(údaje, 72, 64);

        spustiteľný_súbor_zavádzací_program.IMAGE IMAGE_VALUE = new spustiteľný_súbor_zavádzací_program().검사(údaje);
        overiť(IMAGE_VALUE.START_adresa() == 0x04001000, "ELF Spustiť_2 adresa");
        overiť(IMAGE_VALUE.구역들().size() == 1 && IMAGE_VALUE.구역들().get(0).종류() == 8, "ELF 빈 údaje sekcia_VALUE");
        int 서술자 = jadro_VALUE.체계호출().Otvoriť(jadro_VALUE.첫과정(), "시험", 체계호출.iba_na_čítanie_príznak);
        overiť(jadro_VALUE.체계호출().Súbor_riadenie(jadro_VALUE.첫과정(), 서술자, 2, 1) == 0, "Vykonať_príkaz 시 Zatvoriť Nastavenia");
        overiť(jadro_VALUE.체계호출().Vykonať_príkaz(jadro_VALUE.첫과정(), údaje, new String[] {"시험", "값"}, new String[] {"Jazyky=Slovenský"}) == 0, "ELF Vykonať_príkaz IMAGE_VALUE 적재");
        overiť(jadro_VALUE.첫과정().실행시작주소() == 0x04001000, "Vykonať_príkaz Spustiť_2 adresa 반영");
        overiť(jadro_VALUE.첫과정().실행인자().length == 2 && jadro_VALUE.첫과정().환경값().length == 1, "Vykonať_príkaz 인자와 환경");
        overiť(!jadro_VALUE.첫과정().파일서술자().Informačné_systémy_otvoriť(서술자), "Vykonať_príkaz 시 서술자 Zatvoriť");
        overiť(jadro_VALUE.쪽관리().바이트읽기(jadro_VALUE.첫과정().adresa_priestor(), 0x04002000) == 0, "빈 údaje sekcia_VALUE 영 incializovať");
    }

    private static void test_vstup(jadro jadro_VALUE) {
        jadro_VALUE.입력관리().키누름('가');
        jadro_VALUE.입력관리().쥐이동(3, -2);
        vstup_udalosť 첫사건 = jadro_VALUE.입력관리().Ďalej_udalosť();
        vstup_udalosť SECOND_udalosť = jadro_VALUE.입력관리().Ďalej_udalosť();
        overiť(첫사건.druh_udalosti() == vstup_udalosť.종류.키누름, "자판 Udalosť");
        overiť(SECOND_udalosť.첫째값() == 3 && SECOND_udalosť.SECOND_VALUE() == -2, "쥐 premiestniť_VALUE Udalosť");
    }

    private static void test_hardvér(hostiteľ_hardvér telefón_VALUE) {
        telefón_VALUE.zapísať_port_Byte(0x3f8, 0xab);
        overiť(telefón_VALUE.포트바이트읽기(0x3f8) == 0xab, "hardvér_port vstup_a_výstup 경계");
        overiť(telefón_VALUE.직렬기록().contains("JSvkOS"), "직렬 LOG_RECORD");
    }

    private static void 개입중단과서술자시험() {
        개입중단관리자 관리자 = new 개입중단관리자();
        관리자.register_položka(0x21, Úložisko_adresa -> Úložisko_adresa + 4);
        관리자.zapnúť();
        overiť(관리자.distribuovať_VALUE(0x21, 100) == 104, "IRQ distribuovať_VALUE");
        관리자.deaktivovať();
        overiť(관리자.distribuovať_VALUE(0x21, 100) == 100, "IRQ deaktivovať");

        전역서술자표 서술자표 = new 전역서술자표();
        서술자표.množina_predvolená_hodnota();
        overiť(서술자표.조각들().size() == 5, "전역 서술자표");
        úloha_Stav_segment úloha_Stav = new úloha_Stav_segment();
        úloha_Stav.특권쌓임공간설정(0x10, 0x800000);
        overiť(úloha_Stav.영번쌓임조각() == 0x10 && úloha_Stav.영번쌓임주소() == 0x800000, "작업 Stav_VALUE sekcia_VALUE");
    }

    private static void test_Úložisko_AND_Siete() {
        고급기술결합장치 úložné_zariadenie = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.sekcia_zmeniť_veľkosť];
        byte[] 읽은자료 = new byte[고급기술결합장치.sekcia_zmeniť_veľkosť];
        쓸자료[17] = 42;
        úložné_zariadenie.Zápis(2, 쓸자료);
        úložné_zariadenie.Čítanie(2, 읽은자료);
        overiť(읽은자료[17] == 42, "ATA sekcia_VALUE 읽고 Zápis");

        주변장치연결관리자 príslušenstvo = new 주변장치연결관리자();
        príslušenstvo.발견(new 주변장치연결관리자.telefón_VALUE(0x1022, 0x2000, 0xc000, 11));
        overiť(príslušenstvo.FIND_položka(0x1022, 0x2000) != null, "주변 telefón_VALUE FIND_položka");

        byte[] sieť_Ethernet_rám = new byte[34];
        sieť_Ethernet_rám[12] = 0x08;
        sieť_Ethernet_rám[13] = 0x00;
        sieť_Ethernet_rám[14] = 0x45;
        overiť(sieť_Nástroje.sieť_Ethernet_UPPER_protokol(sieť_Ethernet_rám) == 0x0800, "이더넷 상위 prípad_VALUE");
        overiť(sieť_Nástroje.상호통신망규약사판인가(sieť_Ethernet_rám, 14), "상호통신망규약 4판");
        overiť(sieť_Nástroje.cloud_kontrolný_súčet(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 kontrolný_súčet");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        zapísať_celé_číslo_VALUE(첫구역, 454, 63);
        zapísať_celé_číslo_VALUE(첫구역, 458, 1024);
        overiť(new 기본분할영역표().Čítanie(첫구역).size() == 1, "predvolená_hodnota 분할 영역표");

        sieťová_vrstva vrstva_VALUE = new sieťová_vrstva();
        int[] RECEIVED_COUNT = new int[1];
        vrstva_VALUE.register_používateľ_údaje_lekcia(7, (údaje, Spustiť_2, dĺžka_VALUE) -> RECEIVED_COUNT[0]++);
        byte[] rám_INDEX = new byte[14 + 20 + 8];
        rám_INDEX[12] = 0x08;
        rám_INDEX[13] = 0x00;
        rám_INDEX[14] = 0x45;
        rám_INDEX[16] = 0;
        rám_INDEX[17] = 28;
        rám_INDEX[23] = 17;
        rám_INDEX[36] = 0;
        rám_INDEX[37] = 7;
        overiť(vrstva_VALUE.dostať_sieť_Ethernet(rám_INDEX) && RECEIVED_COUNT[0] == 1, "používateľ údaje lekcia_VALUE_7c611f50 distribuovať_VALUE");
    }

    private static void 화면과시계시험() {
        znak_displej 화면 = new znak_displej();
        화면.Výstup("가나\n다");
        overiť(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 Výstup");
        Hodiny Hodiny = new Hodiny(100);
        for (int INDEX = 0; INDEX < 10; INDEX++) {
            Hodiny.틱();
        }
        overiť(Hodiny.지난밀리초() == 100, "Hodiny 틱 CONVERT_VALUE");
    }

    private static void zapísať_celé_číslo_VALUE(byte[] údaje, int Pozícia, int VALUE) {
        údaje[Pozícia] = (byte) VALUE;
        údaje[Pozícia + 1] = (byte) (VALUE >>> 8);
        údaje[Pozícia + 2] = (byte) (VALUE >>> 16);
        údaje[Pozícia + 3] = (byte) (VALUE >>> 24);
    }

    private static void 짧은정수쓰기(byte[] údaje, int Pozícia, int VALUE) {
        údaje[Pozícia] = (byte) VALUE;
        údaje[Pozícia + 1] = (byte) (VALUE >>> 8);
    }

    private static void overiť(boolean podmienka, String Názov) {
        if (!podmienka) {
            throw new AssertionError("zlyhanie_VALUE: " + Názov);
        }
        odovzdať_COUNT++;
        System.out.println("odovzdať_VALUE: " + Názov);
    }
}
