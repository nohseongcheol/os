// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latvija.JLvaOS.시험;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Latvija.JLvaOS.atmiņa_reģions.기억공간관리자;
import Latvija.JLvaOS.atmiņa_reģions.쪽관리자;
import Latvija.JLvaOS.입력.입력사건;
import Latvija.JLvaOS.작업.Process_VALUE;
import Latvija.JLvaOS.체계호출.체계호출;
import Latvija.JLvaOS.failu_sistēma.izpildāms_fails_ielādētājs;
import Latvija.JLvaOS.kodols.kodols;
import Latvija.JLvaOS.viesot.호스트하드웨어;
import Latvija.JLvaOS.IRQ.개입중단관리자;
import Latvija.JLvaOS.서술자.전역서술자표;
import Latvija.JLvaOS.atmiņas_ierīce.고급기술결합장치;
import Latvija.JLvaOS.ierīce_VALUE.주변장치연결관리자;
import Latvija.JLvaOS.tīkls_kopa.tīkls_Rīki;
import Latvija.JLvaOS.tīkls_kopa.tīkla_slānis;
import Latvija.JLvaOS.ierīce_VALUE.Pulkstenis;
import Latvija.JLvaOS.서술자.uzdevums_Statuss_segments;
import Latvija.JLvaOS.화면.rakstzīme_rādīt;
import Latvija.JLvaOS.failu_sistēma.primārais_nodalījums_tabula;

public final class 전체시험 {
    private static int padot_COUNT;

    private 전체시험() {
    }

    public static void main(String[] parametrs_arg) {
        호스트하드웨어 ierīce_VALUE = new 호스트하드웨어();
        kodols kodols_VALUE = new kodols(ierīce_VALUE);
        kodols_VALUE.Palaist();

        기억공간시험(kodols_VALUE);
        쪽관리시험(kodols_VALUE);
        파일과과정시험(kodols_VALUE);
        실행파일시험(kodols_VALUE);
        입력시험(kodols_VALUE);
        하드웨어시험(ierīce_VALUE);
        개입중단과서술자시험();
        저장장치와통신망시험();
        화면과시계시험();

        System.out.println("JLvaOS 시험 padot_VALUE: " + padot_COUNT);
    }

    private static void 기억공간시험(kodols kodols_VALUE) {
        기억공간관리자 관리자 = kodols_VALUE.atmiņa_reģions();
        int 첫주소 = 관리자.정렬할당(100, 64);
        verificēt((첫주소 & 63) == 0, "līdzināt_VALUE piešķirt_Krātuve");
        관리자.rakstīšana_byte_VALUE(첫주소, (byte) 0x5a);
        verificēt(관리자.바이트읽기(첫주소) == (byte) 0x5a, "물리 atmiņa_reģions 읽고 Rakstīt");
        int 사용전 = 관리자.사용크기();
        관리자.izlaist_Krātuve(첫주소);
        verificēt(관리자.사용크기() < 사용전, "atmiņa_reģions izlaist_Krātuve");
    }

    private static void 쪽관리시험(kodols kodols_VALUE) {
        쪽관리자 관리자 = kodols_VALUE.쪽관리();
        쪽관리자.adrese_telpa vecākobjekts_telpa = 관리자.새주소공간();
        관리자.MAP_lapa(vecākobjekts_telpa, 0x1000, true);
        관리자.rakstīšana_byte_VALUE(vecākobjekts_telpa, 0x1010, (byte) 7);
        쪽관리자.adrese_telpa bērns_telpa = 관리자.쓰기시복사복제(vecākobjekts_telpa);
        관리자.rakstīšana_byte_VALUE(bērns_telpa, 0x1010, (byte) 9);
        verificēt(관리자.바이트읽기(vecākobjekts_telpa, 0x1010) == 7, "Rakstīt 시 kopēt_VALUE vecākobjekts_VALUE 격리");
        verificēt(관리자.바이트읽기(bērns_telpa, 0x1010) == 9, "Rakstīt 시 kopēt_VALUE bērns_VALUE Rakstīt");
    }

    private static void 파일과과정시험(kodols kodols_VALUE) {
        byte[] Saturs_VALUE = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        kodols_VALUE.failu_sistēma().Pievienot_Fails("시험", Saturs_VALUE);
        Process_VALUE vecākobjekts_VALUE = kodols_VALUE.첫과정();
        체계호출 호출 = kodols_VALUE.체계호출();
        int 서술자 = 호출.Atvērt(vecākobjekts_VALUE, "/시험", 체계호출.tikai_lasāms_atzīmēt_ar_karodziņu);
        verificēt(서술자 >= 3, "Fails Atvērt");

        byte[] saņemt_mērķis = new byte[Saturs_VALUE.length];
        verificēt(호출.Lasīt(vecākobjekts_VALUE, 서술자, saņemt_mērķis, saņemt_mērķis.length) == Saturs_VALUE.length, "Fails Lasīt");
        verificēt(Arrays.equals(Saturs_VALUE, saņemt_mērķis), "Fails Saturs_VALUE");
        verificēt(호출.pārvietot_amats(vecākobjekts_VALUE, 서술자, 0, 체계호출.Meklēt_Sākt) == 0, "Fails Novietojums pārvietot_VALUE");

        int 복제서술자 = 호출.서술자복제(vecākobjekts_VALUE, 서술자);
        verificēt(복제서술자 >= 0, "서술자 klons_VALUE");
        Process_VALUE bērns_VALUE = 호출.klons_Process(vecākobjekts_VALUE);
        verificēt(bērns_VALUE.identifikators_VALUE() != vecākobjekts_VALUE.identifikators_VALUE(), "Process_VALUE identifikators_VALUE 분리");
        verificēt(bērns_VALUE.vecākobjekts_identifikators() == vecākobjekts_VALUE.identifikators_VALUE(), "vecākobjekts_VALUE Process_VALUE identifikators_VALUE");
        verificēt(호출.Aizvērt(bērns_VALUE, 서술자) == 0 && vecākobjekts_VALUE.파일서술자().informācijas_tehnoloģija_atvērt(서술자), "bērns_VALUE Aizvērt 격리");

        int 이전끝 = 호출.palielinājums_programma_pārtraukt(vecākobjekts_VALUE, 8192);
        verificēt(이전끝 == 0x06000000, "programma_f5044b9b 끝 늘리기");
        verificēt(vecākobjekts_VALUE.programma_pārtraukt() == 0x06002000, "programma_f5044b9b 끝 반영");
        verificēt(bērns_VALUE.programma_pārtraukt() == 0x06000000, "과정별 programma_f5044b9b 끝 격리");

        bērns_VALUE.Iziet_programma(7);
        verificēt(호출.자식기다리기(vecākobjekts_VALUE, bērns_VALUE.identifikators_VALUE(), false) == (7 << 8), "bērns_VALUE Iziet_programma 기다리기");
        verificēt(호출.접근가능("시험", 1) == -13, "Izpildīt_komanda atļauja_VALUE noraidīt_VALUE");
        verificēt(호출.UID() == 0 && 호출.Grupa_identifikators() == 0, "사용자와 무리 identifikators_VALUE");
        verificēt("/".equals(호출.pašreizējais_uzdevumu_saraksts(2)) && 호출.SWITCH_uzdevumu_saraksts("/") == 0, "pašreizējais_krājums 작업 ievade_Saraksts");
        verificēt(호출.informācijas_tehnoloģija_Terminālis(vecākobjekts_VALUE, 1), "표준 Izvade 단말");
        verificēt("JLvaOS".equals(호출.sistēma_Detalizēti().sistēma_nosaukums()), "operētājsistēma_VALUE msinfo32_exe");
    }

    private static void 실행파일시험(kodols kodols_VALUE) {
        byte[] dati = new byte[92];
        dati[0] = 0x7f;
        dati[1] = 'E';
        dati[2] = 'L';
        dati[3] = 'F';
        dati[4] = 1;
        dati[5] = 1;
        rakstīšana_vesels_skaitlis_VALUE(dati, 24, 0x04001000);
        rakstīšana_vesels_skaitlis_VALUE(dati, 32, 52);
        짧은정수쓰기(dati, 46, 40);
        짧은정수쓰기(dati, 48, 1);
        rakstīšana_vesels_skaitlis_VALUE(dati, 56, 8);
        rakstīšana_vesels_skaitlis_VALUE(dati, 60, 2);
        rakstīšana_vesels_skaitlis_VALUE(dati, 64, 0x04002000);
        rakstīšana_vesels_skaitlis_VALUE(dati, 72, 64);

        izpildāms_fails_ielādētājs.IMAGE IMAGE_VALUE = new izpildāms_fails_ielādētājs().검사(dati);
        verificēt(IMAGE_VALUE.Sākt_adrese() == 0x04001000, "ELF Palaist adrese");
        verificēt(IMAGE_VALUE.구역들().size() == 1 && IMAGE_VALUE.구역들().get(0).종류() == 8, "ELF 빈 dati sadaļa_VALUE");
        int 서술자 = kodols_VALUE.체계호출().Atvērt(kodols_VALUE.첫과정(), "시험", 체계호출.tikai_lasāms_atzīmēt_ar_karodziņu);
        verificēt(kodols_VALUE.체계호출().Fails_vadība(kodols_VALUE.첫과정(), 서술자, 2, 1) == 0, "Izpildīt_komanda 시 Aizvērt Uzstādījumi");
        verificēt(kodols_VALUE.체계호출().Izpildīt_komanda(kodols_VALUE.첫과정(), dati, new String[] {"시험", "값"}, new String[] {"Valodas=Latviešu"}) == 0, "ELF Izpildīt_komanda IMAGE_VALUE 적재");
        verificēt(kodols_VALUE.첫과정().실행시작주소() == 0x04001000, "Izpildīt_komanda Palaist adrese 반영");
        verificēt(kodols_VALUE.첫과정().실행인자().length == 2 && kodols_VALUE.첫과정().환경값().length == 1, "Izpildīt_komanda 인자와 환경");
        verificēt(!kodols_VALUE.첫과정().파일서술자().informācijas_tehnoloģija_atvērt(서술자), "Izpildīt_komanda 시 서술자 Aizvērt");
        verificēt(kodols_VALUE.쪽관리().바이트읽기(kodols_VALUE.첫과정().adrese_telpa(), 0x04002000) == 0, "빈 dati sadaļa_VALUE nulle_operands 초기화");
    }

    private static void 입력시험(kodols kodols_VALUE) {
        kodols_VALUE.입력관리().Atslēga_nedarbojas('가');
        kodols_VALUE.입력관리().쥐이동(3, -2);
        입력사건 첫사건 = kodols_VALUE.입력관리().Tālāk_notikums();
        입력사건 SECOND_notikums = kodols_VALUE.입력관리().Tālāk_notikums();
        verificēt(첫사건.notikuma_veids() == 입력사건.종류.Atslēga_nedarbojas, "자판 Notikums");
        verificēt(SECOND_notikums.첫째값() == 3 && SECOND_notikums.SECOND_VALUE() == -2, "쥐 pārvietot_VALUE Notikums");
    }

    private static void 하드웨어시험(호스트하드웨어 ierīce_VALUE) {
        ierīce_VALUE.rakstīšana_ports_byte(0x3f8, 0xab);
        verificēt(ierīce_VALUE.포트바이트읽기(0x3f8) == 0xab, "포트 ievadizvade 경계");
        verificēt(ierīce_VALUE.직렬기록().contains("JLvaOS"), "직렬 LOG_RECORD");
    }

    private static void 개입중단과서술자시험() {
        개입중단관리자 관리자 = new 개입중단관리자();
        관리자.reģistrs_ievade(0x21, Krātuve_adrese -> Krātuve_adrese + 4);
        관리자.ieslēgt();
        verificēt(관리자.izplatīt_VALUE(0x21, 100) == 104, "IRQ izplatīt_VALUE");
        관리자.deaktivizēt();
        verificēt(관리자.izplatīt_VALUE(0x21, 100) == 100, "IRQ deaktivizēt");

        전역서술자표 서술자표 = new 전역서술자표();
        서술자표.kopa_noklusējuma_vērtība();
        verificēt(서술자표.조각들().size() == 5, "전역 서술자표");
        uzdevums_Statuss_segments uzdevums_Statuss = new uzdevums_Statuss_segments();
        uzdevums_Statuss.특권쌓임공간설정(0x10, 0x800000);
        verificēt(uzdevums_Statuss.kopa_nulle_bloks() == 0x10 && uzdevums_Statuss.kopa_nulle_adrese() == 0x800000, "작업 Statuss_VALUE sadaļa_VALUE");
    }

    private static void 저장장치와통신망시험() {
        고급기술결합장치 atmiņas_ierīce = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.sadaļa_mainīt_izmērus];
        byte[] 읽은자료 = new byte[고급기술결합장치.sadaļa_mainīt_izmērus];
        쓸자료[17] = 42;
        atmiņas_ierīce.Rakstīt(2, 쓸자료);
        atmiņas_ierīce.Lasīt(2, 읽은자료);
        verificēt(읽은자료[17] == 42, "ATA sadaļa_VALUE 읽고 Rakstīt");

        주변장치연결관리자 piederums = new 주변장치연결관리자();
        piederums.발견(new 주변장치연결관리자.ierīce_VALUE(0x1022, 0x2000, 0xc000, 11));
        verificēt(piederums.FIND_ievade(0x1022, 0x2000) != null, "주변 ierīce_VALUE FIND_ievade");

        byte[] Ethernet_kadrs = new byte[34];
        Ethernet_kadrs[12] = 0x08;
        Ethernet_kadrs[13] = 0x00;
        Ethernet_kadrs[14] = 0x45;
        verificēt(tīkls_Rīki.Ethernet_UPPER_protokols(Ethernet_kadrs) == 0x0800, "이더넷 상위 līguma_vērtība");
        verificēt(tīkls_Rīki.informācijas_tehnoloģija_RCN_4_protokols(Ethernet_kadrs, 14), "상호통신망규약 4판");
        verificēt(tīkls_Rīki.mākonis_kontrolsumma(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 kontrolsumma");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        rakstīšana_vesels_skaitlis_VALUE(첫구역, 454, 63);
        rakstīšana_vesels_skaitlis_VALUE(첫구역, 458, 1024);
        verificēt(new primārais_nodalījums_tabula().Lasīt(첫구역).size() == 1, "noklusējuma_vērtība 분할 영역표");

        tīkla_slānis slānis_VALUE = new tīkla_slānis();
        int[] RECEIVED_COUNT = new int[1];
        slānis_VALUE.reģistrs_lietotājs_dati_vienība(7, (dati, Palaist, 길이) -> RECEIVED_COUNT[0]++);
        byte[] kadrs_INDEX = new byte[14 + 20 + 8];
        kadrs_INDEX[12] = 0x08;
        kadrs_INDEX[13] = 0x00;
        kadrs_INDEX[14] = 0x45;
        kadrs_INDEX[16] = 0;
        kadrs_INDEX[17] = 28;
        kadrs_INDEX[23] = 17;
        kadrs_INDEX[36] = 0;
        kadrs_INDEX[37] = 7;
        verificēt(slānis_VALUE.saņemt_Ethernet(kadrs_INDEX) && RECEIVED_COUNT[0] == 1, "lietotājs dati vienība_VALUE izplatīt_VALUE");
    }

    private static void 화면과시계시험() {
        rakstzīme_rādīt 화면 = new rakstzīme_rādīt();
        화면.Izvade("가나\n다");
        verificēt(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 Izvade");
        Pulkstenis Pulkstenis = new Pulkstenis(100);
        for (int INDEX = 0; INDEX < 10; INDEX++) {
            Pulkstenis.tikšķis_VALUE();
        }
        verificēt(Pulkstenis.지난밀리초() == 100, "Pulkstenis tikšķis_VALUE CONVERT_VALUE");
    }

    private static void rakstīšana_vesels_skaitlis_VALUE(byte[] dati, int Novietojums, int VALUE) {
        dati[Novietojums] = (byte) VALUE;
        dati[Novietojums + 1] = (byte) (VALUE >>> 8);
        dati[Novietojums + 2] = (byte) (VALUE >>> 16);
        dati[Novietojums + 3] = (byte) (VALUE >>> 24);
    }

    private static void 짧은정수쓰기(byte[] dati, int Novietojums, int VALUE) {
        dati[Novietojums] = (byte) VALUE;
        dati[Novietojums + 1] = (byte) (VALUE >>> 8);
    }

    private static void verificēt(boolean nosacījums, String Nosaukums) {
        if (!nosacījums) {
            throw new AssertionError("kļūme_VALUE: " + Nosaukums);
        }
        padot_COUNT++;
        System.out.println("padot_VALUE: " + Nosaukums);
    }
}
