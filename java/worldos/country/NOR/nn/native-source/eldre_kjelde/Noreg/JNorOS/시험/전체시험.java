// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Noreg.JNorOS.시험;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Noreg.JNorOS.기억공간.Minne_leiar;
import Noreg.JNorOS.기억공간.side_leiar;
import Noreg.JNorOS.입력.입력사건;
import Noreg.JNorOS.작업.Prosess_VALUE;
import Noreg.JNorOS.체계호출.체계호출;
import Noreg.JNorOS.filsystem.실행파일적재기;
import Noreg.JNorOS.kjerne.kjerne;
import Noreg.JNorOS.vert.호스트하드웨어;
import Noreg.JNorOS.IRQ.IRQ_leiar;
import Noreg.JNorOS.서술자.전역서술자표;
import Noreg.JNorOS.Lagring_mobil.고급기술결합장치;
import Noreg.JNorOS.mobil_VALUE.ekstern_eining_buss_leiar;
import Noreg.JNorOS.Nettverk_Stabel.Nettverk_Verktøy;
import Noreg.JNorOS.Nettverk_Stabel.Nettverk_lag;
import Noreg.JNorOS.mobil_VALUE.Klokke;
import Noreg.JNorOS.서술자.oppgåve_status_segment;
import Noreg.JNorOS.화면.teikn_vise;
import Noreg.JNorOS.filsystem.기본분할영역표;

public final class 전체시험 {
    private static int sende_COUNT;

    private 전체시험() {
    }

    public static void main(String[] parameter_argument) {
        호스트하드웨어 mobil_VALUE = new 호스트하드웨어();
        kjerne kjerne_VALUE = new kjerne(mobil_VALUE);
        kjerne_VALUE.Køyr_2();

        기억공간시험(kjerne_VALUE);
        쪽관리시험(kjerne_VALUE);
        파일과과정시험(kjerne_VALUE);
        실행파일시험(kjerne_VALUE);
        입력시험(kjerne_VALUE);
        하드웨어시험(mobil_VALUE);
        개입중단과서술자시험();
        저장장치와통신망시험();
        화면과시계시험();

        System.out.println("JNorOS 시험 sende_VALUE: " + sende_COUNT);
    }

    private static void 기억공간시험(kjerne kjerne_VALUE) {
        Minne_leiar leiar_VALUE = kjerne_VALUE.기억공간();
        int 첫주소 = leiar_VALUE.정렬할당(100, 64);
        stadfeste((첫주소 & 63) == 0, "justere_VALUE tildele_Lagring");
        leiar_VALUE.skrive_byte_VALUE(첫주소, (byte) 0x5a);
        stadfeste(leiar_VALUE.바이트읽기(첫주소) == (byte) 0x5a, "물리 기억공간 읽고 Skriv");
        int 사용전 = leiar_VALUE.사용크기();
        leiar_VALUE.frigi_Lagring(첫주소);
        stadfeste(leiar_VALUE.사용크기() < 사용전, "기억공간 frigi_Lagring");
    }

    private static void 쪽관리시험(kjerne kjerne_VALUE) {
        side_leiar leiar_VALUE = kjerne_VALUE.쪽관리();
        side_leiar.ADDRESS_område forelder_område = leiar_VALUE.새주소공간();
        leiar_VALUE.MAP_side(forelder_område, 0x1000, true);
        leiar_VALUE.skrive_byte_VALUE(forelder_område, 0x1010, (byte) 7);
        side_leiar.ADDRESS_område underordna_område = leiar_VALUE.쓰기시복사복제(forelder_område);
        leiar_VALUE.skrive_byte_VALUE(underordna_område, 0x1010, (byte) 9);
        stadfeste(leiar_VALUE.바이트읽기(forelder_område, 0x1010) == 7, "Skriv 시 kopiere_VALUE forelder_VALUE 격리");
        stadfeste(leiar_VALUE.바이트읽기(underordna_område, 0x1010) == 9, "Skriv 시 kopiere_VALUE underordna_VALUE Skriv");
    }

    private static void 파일과과정시험(kjerne kjerne_VALUE) {
        byte[] Innhald_VALUE = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        kjerne_VALUE.filsystem().파일추가("시험", Innhald_VALUE);
        Prosess_VALUE forelder_VALUE = kjerne_VALUE.첫과정();
        체계호출 호출 = kjerne_VALUE.체계호출();
        int 서술자 = 호출.Opna(forelder_VALUE, "/시험", 체계호출.skriveverna_flagg);
        stadfeste(서술자 >= 3, "Fil Opna");

        byte[] 받을곳 = new byte[Innhald_VALUE.length];
        stadfeste(호출.Les(forelder_VALUE, 서술자, 받을곳, 받을곳.length) == Innhald_VALUE.length, "Fil Les");
        stadfeste(Arrays.equals(Innhald_VALUE, 받을곳), "Fil Innhald_VALUE");
        stadfeste(호출.flytte_plassere(forelder_VALUE, 서술자, 0, 체계호출.Søk_START) == 0, "Fil Posisjon flytte_VALUE");

        int 복제서술자 = 호출.서술자복제(forelder_VALUE, 서술자);
        stadfeste(복제서술자 >= 0, "서술자 복제");
        Prosess_VALUE underordna_VALUE = 호출.과정복제(forelder_VALUE);
        stadfeste(underordna_VALUE.identifikator_VALUE() != forelder_VALUE.identifikator_VALUE(), "Prosess_VALUE identifikator_VALUE 분리");
        stadfeste(underordna_VALUE.forelder_identifikator() == forelder_VALUE.identifikator_VALUE(), "forelder_VALUE Prosess_VALUE identifikator_VALUE");
        stadfeste(호출.Lukk(underordna_VALUE, 서술자) == 0 && forelder_VALUE.파일서술자().informasjonsteknologi_opne(서술자), "underordna_VALUE Lukk 격리");

        int 이전끝 = 호출.프로그램끝늘리기(forelder_VALUE, 8192);
        stadfeste(이전끝 == 0x06000000, "app_f5044b9b 끝 늘리기");
        stadfeste(forelder_VALUE.app_pause() == 0x06002000, "app_f5044b9b 끝 반영");
        stadfeste(underordna_VALUE.app_pause() == 0x06000000, "과정별 app_f5044b9b 끝 격리");

        underordna_VALUE.Utgang_app(7);
        stadfeste(호출.자식기다리기(forelder_VALUE, underordna_VALUE.identifikator_VALUE(), false) == (7 << 8), "underordna_VALUE Utgang_app 기다리기");
        stadfeste(호출.접근가능("시험", 1) == -13, "Utfør_kommando løyve_VALUE avvise_VALUE");
        stadfeste(호출.UID() == 0 && 호출.gruppe_identifikator() == 0, "사용자와 무리 identifikator_VALUE");
        stadfeste("/".equals(호출.betalt_oppgåveliste(2)) && 호출.byte_oppgåveliste("/") == 0, "betalt_vare 작업 oppføring_Liste");
        stadfeste(호출.informasjonsteknologi_Terminal(forelder_VALUE, 1), "표준 Utdata 단말");
        stadfeste("JNorOS".equals(호출.system_Detaljar().system_namn()), "operativsystem_VALUE msinfo32_exe");
    }

    private static void 실행파일시험(kjerne kjerne_VALUE) {
        byte[] data = new byte[92];
        data[0] = 0x7f;
        data[1] = 'E';
        data[2] = 'L';
        data[3] = 'F';
        data[4] = 1;
        data[5] = 1;
        skrive_heiltal_VALUE(data, 24, 0x04001000);
        skrive_heiltal_VALUE(data, 32, 52);
        짧은정수쓰기(data, 46, 40);
        짧은정수쓰기(data, 48, 1);
        skrive_heiltal_VALUE(data, 56, 8);
        skrive_heiltal_VALUE(data, 60, 2);
        skrive_heiltal_VALUE(data, 64, 0x04002000);
        skrive_heiltal_VALUE(data, 72, 64);

        실행파일적재기.IMAGE IMAGE_VALUE = new 실행파일적재기().검사(data);
        stadfeste(IMAGE_VALUE.START_ADDRESS() == 0x04001000, "ELF Køyr_2 ADDRESS");
        stadfeste(IMAGE_VALUE.구역들().size() == 1 && IMAGE_VALUE.구역들().get(0).종류() == 8, "ELF 빈 data del_VALUE");
        int 서술자 = kjerne_VALUE.체계호출().Opna(kjerne_VALUE.첫과정(), "시험", 체계호출.skriveverna_flagg);
        stadfeste(kjerne_VALUE.체계호출().fil_styring(kjerne_VALUE.첫과정(), 서술자, 2, 1) == 0, "Utfør_kommando 시 Lukk Innstillingar");
        stadfeste(kjerne_VALUE.체계호출().Utfør_kommando(kjerne_VALUE.첫과정(), data, new String[] {"시험", "값"}, new String[] {"Språk=한국어"}) == 0, "ELF Utfør_kommando IMAGE_VALUE 적재");
        stadfeste(kjerne_VALUE.첫과정().실행시작주소() == 0x04001000, "Utfør_kommando Køyr_2 ADDRESS 반영");
        stadfeste(kjerne_VALUE.첫과정().실행인자().length == 2 && kjerne_VALUE.첫과정().환경값().length == 1, "Utfør_kommando 인자와 환경");
        stadfeste(!kjerne_VALUE.첫과정().파일서술자().informasjonsteknologi_opne(서술자), "Utfør_kommando 시 서술자 Lukk");
        stadfeste(kjerne_VALUE.쪽관리().바이트읽기(kjerne_VALUE.첫과정().ADDRESS_område(), 0x04002000) == 0, "빈 data del_VALUE 영 starte");
    }

    private static void 입력시험(kjerne kjerne_VALUE) {
        kjerne_VALUE.입력관리().키누름('가');
        kjerne_VALUE.입력관리().쥐이동(3, -2);
        입력사건 첫사건 = kjerne_VALUE.입력관리().Neste_hending();
        입력사건 SECOND_hending = kjerne_VALUE.입력관리().Neste_hending();
        stadfeste(첫사건.사건종류() == 입력사건.종류.키누름, "자판 Hending");
        stadfeste(SECOND_hending.첫째값() == 3 && SECOND_hending.SECOND_VALUE() == -2, "쥐 flytte_VALUE Hending");
    }

    private static void 하드웨어시험(호스트하드웨어 mobil_VALUE) {
        mobil_VALUE.skrive_port_byte(0x3f8, 0xab);
        stadfeste(mobil_VALUE.포트바이트읽기(0x3f8) == 0xab, "포트 I_U 경계");
        stadfeste(mobil_VALUE.직렬기록().contains("JNorOS"), "직렬 LOG_rad");
    }

    private static void 개입중단과서술자시험() {
        IRQ_leiar leiar_VALUE = new IRQ_leiar();
        leiar_VALUE.registrere_oppføring(0x21, Lagring_ADDRESS -> Lagring_ADDRESS + 4);
        leiar_VALUE.slå_på();
        stadfeste(leiar_VALUE.distribuere_VALUE(0x21, 100) == 104, "IRQ distribuere_VALUE");
        leiar_VALUE.deaktivere();
        stadfeste(leiar_VALUE.distribuere_VALUE(0x21, 100) == 100, "IRQ deaktivere");

        전역서술자표 서술자표 = new 전역서술자표();
        서술자표.sett_standardverdi();
        stadfeste(서술자표.조각들().size() == 5, "전역 서술자표");
        oppgåve_status_segment oppgåve_status = new oppgåve_status_segment();
        oppgåve_status.특권쌓임공간설정(0x10, 0x800000);
        stadfeste(oppgåve_status.영번쌓임조각() == 0x10 && oppgåve_status.영번쌓임주소() == 0x800000, "작업 status_VALUE del_VALUE");
    }

    private static void 저장장치와통신망시험() {
        고급기술결합장치 Lagring_mobil = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.del_endre_storleik];
        byte[] 읽은자료 = new byte[고급기술결합장치.del_endre_storleik];
        쓸자료[17] = 42;
        Lagring_mobil.Skriv(2, 쓸자료);
        Lagring_mobil.Les(2, 읽은자료);
        stadfeste(읽은자료[17] == 42, "ATA del_VALUE 읽고 Skriv");

        ekstern_eining_buss_leiar ekstern_eining = new ekstern_eining_buss_leiar();
        ekstern_eining.발견(new ekstern_eining_buss_leiar.mobil_VALUE(0x1022, 0x2000, 0xc000, 11));
        stadfeste(ekstern_eining.Søk_oppføring(0x1022, 0x2000) != null, "주변 mobil_VALUE Søk_oppføring");

        byte[] Ethernet_rute = new byte[34];
        Ethernet_rute[12] = 0x08;
        Ethernet_rute[13] = 0x00;
        Ethernet_rute[14] = 0x45;
        stadfeste(Nettverk_Verktøy.Ethernet_UPPER_protokoll(Ethernet_rute) == 0x0800, "이더넷 상위 sak_VALUE");
        stadfeste(Nettverk_Verktøy.상호통신망규약사판인가(Ethernet_rute, 14), "상호통신망규약 4판");
        stadfeste(Nettverk_Verktøy.sky_kontrollsum(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 kontrollsum");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        skrive_heiltal_VALUE(첫구역, 454, 63);
        skrive_heiltal_VALUE(첫구역, 458, 1024);
        stadfeste(new 기본분할영역표().Les(첫구역).size() == 1, "standardverdi 분할 영역표");

        Nettverk_lag lag_VALUE = new Nettverk_lag();
        int[] RECEIVED_COUNT = new int[1];
        lag_VALUE.registrere_brukar_data_leksjon(7, (data, Køyr_2, lengd_VALUE) -> RECEIVED_COUNT[0]++);
        byte[] rute_INDEX = new byte[14 + 20 + 8];
        rute_INDEX[12] = 0x08;
        rute_INDEX[13] = 0x00;
        rute_INDEX[14] = 0x45;
        rute_INDEX[16] = 0;
        rute_INDEX[17] = 28;
        rute_INDEX[23] = 17;
        rute_INDEX[36] = 0;
        rute_INDEX[37] = 7;
        stadfeste(lag_VALUE.이더넷받기(rute_INDEX) && RECEIVED_COUNT[0] == 1, "brukar data leksjon_VALUE distribuere_VALUE");
    }

    private static void 화면과시계시험() {
        teikn_vise 화면 = new teikn_vise();
        화면.Utdata("가나\n다");
        stadfeste(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 Utdata");
        Klokke Klokke = new Klokke(100);
        for (int INDEX = 0; INDEX < 10; INDEX++) {
            Klokke.틱();
        }
        stadfeste(Klokke.지난밀리초() == 100, "Klokke 틱 CONVERT_VALUE");
    }

    private static void skrive_heiltal_VALUE(byte[] data, int Posisjon, int VALUE) {
        data[Posisjon] = (byte) VALUE;
        data[Posisjon + 1] = (byte) (VALUE >>> 8);
        data[Posisjon + 2] = (byte) (VALUE >>> 16);
        data[Posisjon + 3] = (byte) (VALUE >>> 24);
    }

    private static void 짧은정수쓰기(byte[] data, int Posisjon, int VALUE) {
        data[Posisjon] = (byte) VALUE;
        data[Posisjon + 1] = (byte) (VALUE >>> 8);
    }

    private static void stadfeste(boolean tilstand, String Namn) {
        if (!tilstand) {
            throw new AssertionError("feil_VALUE: " + Namn);
        }
        sende_COUNT++;
        System.out.println("sende_VALUE: " + Namn);
    }
}
