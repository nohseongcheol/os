// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Soome.JFinOS.시험;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Soome.JFinOS.Mälu_regioon.기억공간관리자;
import Soome.JFinOS.Mälu_regioon.쪽관리자;
import Soome.JFinOS.입력.입력사건;
import Soome.JFinOS.작업.Joonis_VALUE;
import Soome.JFinOS.체계호출.체계호출;
import Soome.JFinOS.failisüsteem.실행파일적재기;
import Soome.JFinOS.tuum.tuum;
import Soome.JFinOS.host.호스트하드웨어;
import Soome.JFinOS.IRQ.개입중단관리자;
import Soome.JFinOS.서술자.전역서술자표;
import Soome.JFinOS.salvesti.고급기술결합장치;
import Soome.JFinOS.seade_VALUE.주변장치연결관리자;
import Soome.JFinOS.võrk_Virn.võrk_Tööriistad;
import Soome.JFinOS.võrk_Virn.võrgukiht;
import Soome.JFinOS.seade_VALUE.Kell;
import Soome.JFinOS.서술자.tööüksus_Olek_segment;
import Soome.JFinOS.화면.märk_ekraan;
import Soome.JFinOS.failisüsteem.primaarsektsioon_tabel;

public final class 전체시험 {
    private static int edastama_COUNT;

    private 전체시험() {
    }

    public static void main(String[] parameeter_argument) {
        호스트하드웨어 seade_VALUE = new 호스트하드웨어();
        tuum tuum_VALUE = new tuum(seade_VALUE);
        tuum_VALUE.Käivita_2();

        기억공간시험(tuum_VALUE);
        쪽관리시험(tuum_VALUE);
        파일과과정시험(tuum_VALUE);
        실행파일시험(tuum_VALUE);
        입력시험(tuum_VALUE);
        하드웨어시험(seade_VALUE);
        개입중단과서술자시험();
        저장장치와통신망시험();
        화면과시계시험();

        System.out.println("JFinOS 시험 edastama_VALUE: " + edastama_COUNT);
    }

    private static void 기억공간시험(tuum tuum_VALUE) {
        기억공간관리자 관리자 = tuum_VALUE.Mälu_regioon();
        int 첫주소 = 관리자.정렬할당(100, 64);
        kinnitama((첫주소 & 63) == 0, "joondama_VALUE lisama_salvesti");
        관리자.kirjutamine_bait_VALUE(첫주소, (byte) 0x5a);
        kinnitama(관리자.바이트읽기(첫주소) == (byte) 0x5a, "물리 Mälu_regioon 읽고 Kirjutamine");
        int 사용전 = 관리자.사용크기();
        관리자.vabastama_salvesti(첫주소);
        kinnitama(관리자.사용크기() < 사용전, "Mälu_regioon vabastama_salvesti");
    }

    private static void 쪽관리시험(tuum tuum_VALUE) {
        쪽관리자 관리자 = tuum_VALUE.쪽관리();
        쪽관리자.ADDRESS_ruum ema_ruum = 관리자.새주소공간();
        관리자.MAP_leht(ema_ruum, 0x1000, true);
        관리자.kirjutamine_bait_VALUE(ema_ruum, 0x1010, (byte) 7);
        쪽관리자.ADDRESS_ruum laps_ruum = 관리자.쓰기시복사복제(ema_ruum);
        관리자.kirjutamine_bait_VALUE(laps_ruum, 0x1010, (byte) 9);
        kinnitama(관리자.바이트읽기(ema_ruum, 0x1010) == 7, "Kirjutamine 시 eksemplar_VALUE ema_VALUE 격리");
        kinnitama(관리자.바이트읽기(laps_ruum, 0x1010) == 9, "Kirjutamine 시 eksemplar_VALUE laps_VALUE Kirjutamine");
    }

    private static void 파일과과정시험(tuum tuum_VALUE) {
        byte[] Sisu_VALUE = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        tuum_VALUE.failisüsteem().Lisa_Fail("시험", Sisu_VALUE);
        Joonis_VALUE ema_VALUE = tuum_VALUE.첫과정();
        체계호출 호출 = tuum_VALUE.체계호출();
        int 서술자 = 호출.Ava(ema_VALUE, "/시험", 체계호출.kirjutuskaitstud_lipp);
        kinnitama(서술자 >= 3, "Fail Ava");

        byte[] saama_sihtkoht = new byte[Sisu_VALUE.length];
        kinnitama(호출.Lugemine(ema_VALUE, 서술자, saama_sihtkoht, saama_sihtkoht.length) == Sisu_VALUE.length, "Fail Lugemine");
        kinnitama(Arrays.equals(Sisu_VALUE, saama_sihtkoht), "Fail Sisu_VALUE");
        kinnitama(호출.liigutama_ametikoht(ema_VALUE, 서술자, 0, 체계호출.Otsi_START) == 0, "Fail Asukoht liigutama_VALUE");

        int 복제서술자 = 호출.서술자복제(ema_VALUE, 서술자);
        kinnitama(복제서술자 >= 0, "서술자 kloon_VALUE");
        Joonis_VALUE laps_VALUE = 호출.kloon_Joonis(ema_VALUE);
        kinnitama(laps_VALUE.identifikaator_VALUE() != ema_VALUE.identifikaator_VALUE(), "Joonis_VALUE identifikaator_VALUE 분리");
        kinnitama(laps_VALUE.ema_identifikaator() == ema_VALUE.identifikaator_VALUE(), "ema_VALUE Joonis_VALUE identifikaator_VALUE");
        kinnitama(호출.Suletud(laps_VALUE, 서술자) == 0 && ema_VALUE.파일서술자().infotehnoloogia_avama(서술자), "laps_VALUE Suletud 격리");

        int 이전끝 = 호출.lisandumine_programm_vaheaeg(ema_VALUE, 8192);
        kinnitama(이전끝 == 0x06000000, "programm_f5044b9b 끝 늘리기");
        kinnitama(ema_VALUE.programm_vaheaeg() == 0x06002000, "programm_f5044b9b 끝 반영");
        kinnitama(laps_VALUE.programm_vaheaeg() == 0x06000000, "과정별 programm_f5044b9b 끝 격리");

        laps_VALUE.Välju_programm(7);
        kinnitama(호출.자식기다리기(ema_VALUE, laps_VALUE.identifikaator_VALUE(), false) == (7 << 8), "laps_VALUE Välju_programm 기다리기");
        kinnitama(호출.접근가능("시험", 1) == -13, "Täida_käsk luba_VALUE keelduma_VALUE");
        kinnitama(호출.UID() == 0 && 호출.Rühm_identifikaator() == 0, "사용자와 무리 identifikaator_VALUE");
        kinnitama("/".equals(호출.tähtaja_piires_ülesandeloend(2)) && 호출.SWITCH_ülesandeloend("/") == 0, "tähtaja_piires_kaup 작업 kirje_Loend");
        kinnitama(호출.infotehnoloogia_terminal(ema_VALUE, 1), "표준 Väljund 단말");
        kinnitama("JFinOS".equals(호출.süsteem_Üksikasjad().süsteem_nimetus()), "operatsioonisüsteem_VALUE msinfo32_exe");
    }

    private static void 실행파일시험(tuum tuum_VALUE) {
        byte[] andmed = new byte[92];
        andmed[0] = 0x7f;
        andmed[1] = 'E';
        andmed[2] = 'L';
        andmed[3] = 'F';
        andmed[4] = 1;
        andmed[5] = 1;
        kirjutamine_täisarv_VALUE(andmed, 24, 0x04001000);
        kirjutamine_täisarv_VALUE(andmed, 32, 52);
        짧은정수쓰기(andmed, 46, 40);
        짧은정수쓰기(andmed, 48, 1);
        kirjutamine_täisarv_VALUE(andmed, 56, 8);
        kirjutamine_täisarv_VALUE(andmed, 60, 2);
        kirjutamine_täisarv_VALUE(andmed, 64, 0x04002000);
        kirjutamine_täisarv_VALUE(andmed, 72, 64);

        실행파일적재기.pilt pilt_VALUE = new 실행파일적재기().검사(andmed);
        kinnitama(pilt_VALUE.START_ADDRESS() == 0x04001000, "ELF Käivita_2 ADDRESS");
        kinnitama(pilt_VALUE.구역들().size() == 1 && pilt_VALUE.구역들().get(0).종류() == 8, "ELF 빈 andmed jaotis_VALUE");
        int 서술자 = tuum_VALUE.체계호출().Ava(tuum_VALUE.첫과정(), "시험", 체계호출.kirjutuskaitstud_lipp);
        kinnitama(tuum_VALUE.체계호출().Fail_meede(tuum_VALUE.첫과정(), 서술자, 2, 1) == 0, "Täida_käsk 시 Suletud Seaded");
        kinnitama(tuum_VALUE.체계호출().Täida_käsk(tuum_VALUE.첫과정(), andmed, new String[] {"시험", "값"}, new String[] {"Keeled=Eesti"}) == 0, "ELF Täida_käsk pilt_VALUE 적재");
        kinnitama(tuum_VALUE.첫과정().실행시작주소() == 0x04001000, "Täida_käsk Käivita_2 ADDRESS 반영");
        kinnitama(tuum_VALUE.첫과정().실행인자().length == 2 && tuum_VALUE.첫과정().환경값().length == 1, "Täida_käsk 인자와 환경");
        kinnitama(!tuum_VALUE.첫과정().파일서술자().infotehnoloogia_avama(서술자), "Täida_käsk 시 서술자 Suletud");
        kinnitama(tuum_VALUE.쪽관리().바이트읽기(tuum_VALUE.첫과정().ADDRESS_ruum(), 0x04002000) == 0, "빈 andmed jaotis_VALUE null_operand 초기화");
    }

    private static void 입력시험(tuum tuum_VALUE) {
        tuum_VALUE.입력관리().Võti_rikkis('가');
        tuum_VALUE.입력관리().쥐이동(3, -2);
        입력사건 첫사건 = tuum_VALUE.입력관리().Edasi_sündmus();
        입력사건 SECOND_sündmus = tuum_VALUE.입력관리().Edasi_sündmus();
        kinnitama(첫사건.sündmuse_liik() == 입력사건.종류.Võti_rikkis, "자판 Sündmus");
        kinnitama(SECOND_sündmus.첫째값() == 3 && SECOND_sündmus.SECOND_VALUE() == -2, "쥐 liigutama_VALUE Sündmus");
    }

    private static void 하드웨어시험(호스트하드웨어 seade_VALUE) {
        seade_VALUE.kirjutamine_port_bait(0x3f8, 0xab);
        kinnitama(seade_VALUE.포트바이트읽기(0x3f8) == 0xab, "포트 I_O 경계");
        kinnitama(seade_VALUE.직렬기록().contains("JFinOS"), "직렬 LOG_kirje");
    }

    private static void 개입중단과서술자시험() {
        개입중단관리자 관리자 = new 개입중단관리자();
        관리자.register_kirje(0x21, salvesti_ADDRESS -> salvesti_ADDRESS + 4);
        관리자.lubama();
        kinnitama(관리자.laiali_jagama_VALUE(0x21, 100) == 104, "IRQ laiali_jagama_VALUE");
        관리자.inaktiveerima();
        kinnitama(관리자.laiali_jagama_VALUE(0x21, 100) == 100, "IRQ inaktiveerima");

        전역서술자표 서술자표 = new 전역서술자표();
        서술자표.hulk_vaikeväärtus();
        kinnitama(서술자표.조각들().size() == 5, "전역 서술자표");
        tööüksus_Olek_segment tööüksus_Olek = new tööüksus_Olek_segment();
        tööüksus_Olek.특권쌓임공간설정(0x10, 0x800000);
        kinnitama(tööüksus_Olek.Virn_null_plokk() == 0x10 && tööüksus_Olek.Virn_null_ADDRESS() == 0x800000, "작업 Olek_VALUE jaotis_VALUE");
    }

    private static void 저장장치와통신망시험() {
        고급기술결합장치 salvesti = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.jaotis_suurust_muutma];
        byte[] 읽은자료 = new byte[고급기술결합장치.jaotis_suurust_muutma];
        쓸자료[17] = 42;
        salvesti.Kirjutamine(2, 쓸자료);
        salvesti.Lugemine(2, 읽은자료);
        kinnitama(읽은자료[17] == 42, "ATA jaotis_VALUE 읽고 Kirjutamine");

        주변장치연결관리자 tarvik = new 주변장치연결관리자();
        tarvik.발견(new 주변장치연결관리자.seade_VALUE(0x1022, 0x2000, 0xc000, 11));
        kinnitama(tarvik.FIND_kirje(0x1022, 0x2000) != null, "주변 seade_VALUE FIND_kirje");

        byte[] Ethernet_raam = new byte[34];
        Ethernet_raam[12] = 0x08;
        Ethernet_raam[13] = 0x00;
        Ethernet_raam[14] = 0x45;
        kinnitama(võrk_Tööriistad.Ethernet_UPPER_protokoll(Ethernet_raam) == 0x0800, "이더넷 상위 lepingu_väärtus");
        kinnitama(võrk_Tööriistad.infotehnoloogia_AHH_4_protokoll(Ethernet_raam, 14), "상호통신망규약 4판");
        kinnitama(võrk_Tööriistad.pilv_kontrollsumma(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 kontrollsumma");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        kirjutamine_täisarv_VALUE(첫구역, 454, 63);
        kirjutamine_täisarv_VALUE(첫구역, 458, 1024);
        kinnitama(new primaarsektsioon_tabel().Lugemine(첫구역).size() == 1, "vaikeväärtus 분할 영역표");

        võrgukiht kiht_VALUE = new võrgukiht();
        int[] RECEIVED_COUNT = new int[1];
        kiht_VALUE.register_kasutaja_andmed_ühik(7, (andmed, Käivita_2, 길이) -> RECEIVED_COUNT[0]++);
        byte[] raam_INDEX = new byte[14 + 20 + 8];
        raam_INDEX[12] = 0x08;
        raam_INDEX[13] = 0x00;
        raam_INDEX[14] = 0x45;
        raam_INDEX[16] = 0;
        raam_INDEX[17] = 28;
        raam_INDEX[23] = 17;
        raam_INDEX[36] = 0;
        raam_INDEX[37] = 7;
        kinnitama(kiht_VALUE.saama_Ethernet(raam_INDEX) && RECEIVED_COUNT[0] == 1, "kasutaja andmed ühik_VALUE laiali_jagama_VALUE");
    }

    private static void 화면과시계시험() {
        märk_ekraan 화면 = new märk_ekraan();
        화면.Väljund("가나\n다");
        kinnitama(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 Väljund");
        Kell Kell = new Kell(100);
        for (int INDEX = 0; INDEX < 10; INDEX++) {
            Kell.tiks_VALUE();
        }
        kinnitama(Kell.지난밀리초() == 100, "Kell tiks_VALUE CONVERT_VALUE");
    }

    private static void kirjutamine_täisarv_VALUE(byte[] andmed, int Asukoht, int VALUE) {
        andmed[Asukoht] = (byte) VALUE;
        andmed[Asukoht + 1] = (byte) (VALUE >>> 8);
        andmed[Asukoht + 2] = (byte) (VALUE >>> 16);
        andmed[Asukoht + 3] = (byte) (VALUE >>> 24);
    }

    private static void 짧은정수쓰기(byte[] andmed, int Asukoht, int VALUE) {
        andmed[Asukoht] = (byte) VALUE;
        andmed[Asukoht + 1] = (byte) (VALUE >>> 8);
    }

    private static void kinnitama(boolean tingimus, String Nimi_2) {
        if (!tingimus) {
            throw new AssertionError("tõrge_VALUE: " + Nimi_2);
        }
        edastama_COUNT++;
        System.out.println("edastama_VALUE: " + Nimi_2);
    }
}
