// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ucraina.JUkrOS.시험;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Ucraina.JUkrOS.Memorie_regiune.기억공간관리자;
import Ucraina.JUkrOS.Memorie_regiune.쪽관리자;
import Ucraina.JUkrOS.입력.입력사건;
import Ucraina.JUkrOS.작업.Proces_VALUE;
import Ucraina.JUkrOS.체계호출.체계호출;
import Ucraina.JUkrOS.sistem_de_fișiere.실행파일적재기;
import Ucraina.JUkrOS.nucleu.nucleu;
import Ucraina.JUkrOS.gazdă.호스트하드웨어;
import Ucraina.JUkrOS.IRQ.개입중단관리자;
import Ucraina.JUkrOS.서술자.전역서술자표;
import Ucraina.JUkrOS.dispozitiv_de_stocare.고급기술결합장치;
import Ucraina.JUkrOS.mobil_VALUE.주변장치연결관리자;
import Ucraina.JUkrOS.rețea_Teanc.rețea_Instrumente;
import Ucraina.JUkrOS.rețea_Teanc.nivel_rețea;
import Ucraina.JUkrOS.mobil_VALUE.Ceas;
import Ucraina.JUkrOS.서술자.sarcină_Stare_segment;
import Ucraina.JUkrOS.화면.caracter_afișa;
import Ucraina.JUkrOS.sistem_de_fișiere.partiție_principală_tabel;

public final class 전체시험 {
    private static int transfera_COUNT;

    private 전체시험() {
    }

    public static void main(String[] parametru_argument) {
        호스트하드웨어 mobil_VALUE = new 호스트하드웨어();
        nucleu nucleu_VALUE = new nucleu(mobil_VALUE);
        nucleu_VALUE.Pornește();

        기억공간시험(nucleu_VALUE);
        쪽관리시험(nucleu_VALUE);
        파일과과정시험(nucleu_VALUE);
        실행파일시험(nucleu_VALUE);
        입력시험(nucleu_VALUE);
        하드웨어시험(mobil_VALUE);
        개입중단과서술자시험();
        저장장치와통신망시험();
        화면과시계시험();

        System.out.println("JUkrOS 시험 transfera_VALUE: " + transfera_COUNT);
    }

    private static void 기억공간시험(nucleu nucleu_VALUE) {
        기억공간관리자 관리자 = nucleu_VALUE.Memorie_regiune();
        int 첫주소 = 관리자.정렬할당(100, 64);
        verifica((첫주소 & 63) == 0, "alinia_VALUE aloca_Stocare");
        관리자.scriere_byte_VALUE(첫주소, (byte) 0x5a);
        verifica(관리자.바이트읽기(첫주소) == (byte) 0x5a, "물리 Memorie_regiune 읽고 Scriere");
        int 사용전 = 관리자.사용크기();
        관리자.lansa_Stocare(첫주소);
        verifica(관리자.사용크기() < 사용전, "Memorie_regiune lansa_Stocare");
    }

    private static void 쪽관리시험(nucleu nucleu_VALUE) {
        쪽관리자 관리자 = nucleu_VALUE.쪽관리();
        쪽관리자.adresa_SPAȚIU părinte_SPAȚIU = 관리자.새주소공간();
        관리자.MAP_pagina(părinte_SPAȚIU, 0x1000, true);
        관리자.scriere_byte_VALUE(părinte_SPAȚIU, 0x1010, (byte) 7);
        쪽관리자.adresa_SPAȚIU copil_SPAȚIU = 관리자.쓰기시복사복제(părinte_SPAȚIU);
        관리자.scriere_byte_VALUE(copil_SPAȚIU, 0x1010, (byte) 9);
        verifica(관리자.바이트읽기(părinte_SPAȚIU, 0x1010) == 7, "Scriere 시 copia_VALUE părinte_VALUE 격리");
        verifica(관리자.바이트읽기(copil_SPAȚIU, 0x1010) == 9, "Scriere 시 copia_VALUE copil_VALUE Scriere");
    }

    private static void 파일과과정시험(nucleu nucleu_VALUE) {
        byte[] Conținut_VALUE = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        nucleu_VALUE.sistem_de_fișiere().adăuga_Fișier("시험", Conținut_VALUE);
        Proces_VALUE părinte_VALUE = nucleu_VALUE.첫과정();
        체계호출 호출 = nucleu_VALUE.체계호출();
        int 서술자 = 호출.Deschide(părinte_VALUE, "/시험", 체계호출.doar_în_citire_fanion);
        verifica(서술자 >= 3, "Fișier Deschide");

        byte[] primi_destinație = new byte[Conținut_VALUE.length];
        verifica(호출.Citire(părinte_VALUE, 서술자, primi_destinație, primi_destinație.length) == Conținut_VALUE.length, "Fișier Citire");
        verifica(Arrays.equals(Conținut_VALUE, primi_destinație), "Fișier Conținut_VALUE");
        verifica(호출.muta_poziție(părinte_VALUE, 서술자, 0, 체계호출.căuta_buta) == 0, "Fișier Poziție muta_VALUE_83b651b8");

        int 복제서술자 = 호출.서술자복제(părinte_VALUE, 서술자);
        verifica(복제서술자 >= 0, "서술자 clona_VALUE");
        Proces_VALUE copil_VALUE = 호출.clona_Proces(părinte_VALUE);
        verifica(copil_VALUE.identificator_VALUE() != părinte_VALUE.identificator_VALUE(), "Proces_VALUE identificator_VALUE 분리");
        verifica(copil_VALUE.părinte_identificator() == părinte_VALUE.identificator_VALUE(), "părinte_VALUE Proces_VALUE identificator_VALUE");
        verifica(호출.Închide(copil_VALUE, 서술자) == 0 && părinte_VALUE.파일서술자().sisteme_de_informații_crea(서술자), "copil_VALUE Închide 격리");

        int Anteriorul_termina_un_apel = 호출.intrare_în_stoc_program_pauză(părinte_VALUE, 8192);
        verifica(Anteriorul_termina_un_apel == 0x06000000, "program_f5044b9b 끝 늘리기");
        verifica(părinte_VALUE.program_pauză() == 0x06002000, "program_f5044b9b 끝 반영");
        verifica(copil_VALUE.program_pauză() == 0x06000000, "과정별 program_f5044b9b 끝 격리");

        copil_VALUE.ieși_program(7);
        verifica(호출.자식기다리기(părinte_VALUE, copil_VALUE.identificator_VALUE(), false) == (7 << 8), "copil_VALUE ieși_program 기다리기");
        verifica(호출.접근가능("시험", 1) == -13, "executa_comandă permisiune_VALUE respinge_VALUE");
        verifica(호출.UID() == 0 && 호출.grup_identificator() == 0, "사용자와 무리 identificator_VALUE");
        verifica("/".equals(호출.curent_listă_de_activități(2)) && 호출.SWITCH_listă_de_activități("/") == 0, "curent_element 작업 intrare_Listă");
        verifica(호출.sisteme_de_informații_Terminal(părinte_VALUE, 1), "표준 Rezultat 단말");
        verifica("JUkrOS".equals(호출.sistem_Detalii().sistem_nume()), "sistem_de_operare_VALUE msinfo32_exe");
    }

    private static void 실행파일시험(nucleu nucleu_VALUE) {
        byte[] date = new byte[92];
        date[0] = 0x7f;
        date[1] = 'E';
        date[2] = 'L';
        date[3] = 'F';
        date[4] = 1;
        date[5] = 1;
        scriere_întreg_VALUE(date, 24, 0x04001000);
        scriere_întreg_VALUE(date, 32, 52);
        짧은정수쓰기(date, 46, 40);
        짧은정수쓰기(date, 48, 1);
        scriere_întreg_VALUE(date, 56, 8);
        scriere_întreg_VALUE(date, 60, 2);
        scriere_întreg_VALUE(date, 64, 0x04002000);
        scriere_întreg_VALUE(date, 72, 64);

        실행파일적재기.IMAGE IMAGE_VALUE = new 실행파일적재기().검사(date);
        verifica(IMAGE_VALUE.buta_adresa() == 0x04001000, "ELF Pornește adresa");
        verifica(IMAGE_VALUE.구역들().size() == 1 && IMAGE_VALUE.구역들().get(0).종류() == 8, "ELF 빈 date secțiune_VALUE");
        int 서술자 = nucleu_VALUE.체계호출().Deschide(nucleu_VALUE.첫과정(), "시험", 체계호출.doar_în_citire_fanion);
        verifica(nucleu_VALUE.체계호출().Fișier_control(nucleu_VALUE.첫과정(), 서술자, 2, 1) == 0, "executa_comandă 시 Închide Setări");
        verifica(nucleu_VALUE.체계호출().executa_comandă(nucleu_VALUE.첫과정(), date, new String[] {"시험", "값"}, new String[] {"Limbi_străine=Română"}) == 0, "ELF executa_comandă IMAGE_VALUE 적재");
        verifica(nucleu_VALUE.첫과정().executare_buta_adresa() == 0x04001000, "executa_comandă Pornește adresa 반영");
        verifica(nucleu_VALUE.첫과정().executare_argument().length == 2 && nucleu_VALUE.첫과정().환경값().length == 1, "executa_comandă 인자와 환경");
        verifica(!nucleu_VALUE.첫과정().파일서술자().sisteme_de_informații_crea(서술자), "executa_comandă 시 서술자 Închide");
        verifica(nucleu_VALUE.쪽관리().바이트읽기(nucleu_VALUE.첫과정().adresa_SPAȚIU(), 0x04002000) == 0, "빈 date secțiune_VALUE zero_operand 초기화");
    }

    private static void 입력시험(nucleu nucleu_VALUE) {
        nucleu_VALUE.입력관리().Cheie_nefuncțional('가');
        nucleu_VALUE.입력관리().쥐이동(3, -2);
        입력사건 첫사건 = nucleu_VALUE.입력관리().Următorul_eveniment();
        입력사건 SECOND_eveniment = nucleu_VALUE.입력관리().Următorul_eveniment();
        verifica(첫사건.natură_eveniment() == 입력사건.종류.Cheie_nefuncțional, "자판 Eveniment");
        verifica(SECOND_eveniment.첫째값() == 3 && SECOND_eveniment.SECOND_VALUE() == -2, "쥐 muta_VALUE_83b651b8 Eveniment");
    }

    private static void 하드웨어시험(호스트하드웨어 mobil_VALUE) {
        mobil_VALUE.scriere_muta_byte(0x3f8, 0xab);
        verifica(mobil_VALUE.포트바이트읽기(0x3f8) == 0xab, "포트 I_O 경계");
        verifica(mobil_VALUE.직렬기록().contains("JUkrOS"), "직렬 LOG_RECORD");
    }

    private static void 개입중단과서술자시험() {
        개입중단관리자 관리자 = new 개입중단관리자();
        관리자.registru_intrare(0x21, Stocare_adresa -> Stocare_adresa + 4);
        관리자.activa();
        verifica(관리자.distribui_VALUE(0x21, 100) == 104, "IRQ distribui_VALUE");
        관리자.deactiva();
        verifica(관리자.distribui_VALUE(0x21, 100) == 100, "IRQ deactiva");

        전역서술자표 서술자표 = new 전역서술자표();
        서술자표.set_valoare_implicită();
        verifica(서술자표.조각들().size() == 5, "전역 서술자표");
        sarcină_Stare_segment sarcină_Stare = new sarcină_Stare_segment();
        sarcină_Stare.특권쌓임공간설정(0x10, 0x800000);
        verifica(sarcină_Stare.Teanc_zero_bloc() == 0x10 && sarcină_Stare.Teanc_zero_adresa() == 0x800000, "작업 Stare_VALUE secțiune_VALUE");
    }

    private static void 저장장치와통신망시험() {
        고급기술결합장치 dispozitiv_de_stocare = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.secțiune_dimensiona];
        byte[] 읽은자료 = new byte[고급기술결합장치.secțiune_dimensiona];
        쓸자료[17] = 42;
        dispozitiv_de_stocare.Scriere(2, 쓸자료);
        dispozitiv_de_stocare.Citire(2, 읽은자료);
        verifica(읽은자료[17] == 42, "ATA secțiune_VALUE 읽고 Scriere");

        주변장치연결관리자 accesoriu = new 주변장치연결관리자();
        accesoriu.발견(new 주변장치연결관리자.mobil_VALUE(0x1022, 0x2000, 0xc000, 11));
        verifica(accesoriu.FIND_intrare(0x1022, 0x2000) != null, "주변 mobil_VALUE FIND_intrare");

        byte[] Ethernet_cadru = new byte[34];
        Ethernet_cadru[12] = 0x08;
        Ethernet_cadru[13] = 0x00;
        Ethernet_cadru[14] = 0x45;
        verifica(rețea_Instrumente.Ethernet_UPPER_protocol(Ethernet_cadru) == 0x0800, "이더넷 상위 caz_VALUE");
        verifica(rețea_Instrumente.sisteme_de_informații_IPV_4_protocol(Ethernet_cadru, 14), "상호통신망규약 4판");
        verifica(rețea_Instrumente.cloud_sumă_de_verificare(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 sumă_de_verificare");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        scriere_întreg_VALUE(첫구역, 454, 63);
        scriere_întreg_VALUE(첫구역, 458, 1024);
        verifica(new partiție_principală_tabel().Citire(첫구역).size() == 1, "valoare_implicită 분할 영역표");

        nivel_rețea strat_VALUE = new nivel_rețea();
        int[] RECEIVED_COUNT = new int[1];
        strat_VALUE.registru_utilizator_date_lecție(7, (date, Pornește, lungime_VALUE) -> RECEIVED_COUNT[0]++);
        byte[] cadru_INDEX = new byte[14 + 20 + 8];
        cadru_INDEX[12] = 0x08;
        cadru_INDEX[13] = 0x00;
        cadru_INDEX[14] = 0x45;
        cadru_INDEX[16] = 0;
        cadru_INDEX[17] = 28;
        cadru_INDEX[23] = 17;
        cadru_INDEX[36] = 0;
        cadru_INDEX[37] = 7;
        verifica(strat_VALUE.primi_Ethernet(cadru_INDEX) && RECEIVED_COUNT[0] == 1, "utilizator date lecție_VALUE distribui_VALUE");
    }

    private static void 화면과시계시험() {
        caracter_afișa 화면 = new caracter_afișa();
        화면.Rezultat("가나\n다");
        verifica(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 Rezultat");
        Ceas Ceas = new Ceas(100);
        for (int INDEX = 0; INDEX < 10; INDEX++) {
            Ceas.gradație_VALUE();
        }
        verifica(Ceas.지난밀리초() == 100, "Ceas gradație_VALUE CONVERT_VALUE");
    }

    private static void scriere_întreg_VALUE(byte[] date, int Poziție, int VALUE) {
        date[Poziție] = (byte) VALUE;
        date[Poziție + 1] = (byte) (VALUE >>> 8);
        date[Poziție + 2] = (byte) (VALUE >>> 16);
        date[Poziție + 3] = (byte) (VALUE >>> 24);
    }

    private static void 짧은정수쓰기(byte[] date, int Poziție, int VALUE) {
        date[Poziție] = (byte) VALUE;
        date[Poziție + 1] = (byte) (VALUE >>> 8);
    }

    private static void verifica(boolean condiție, String Nume) {
        if (!condiție) {
            throw new AssertionError("eroare_VALUE: " + Nume);
        }
        transfera_COUNT++;
        System.out.println("transfera_VALUE: " + Nume);
    }
}
