// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Botswana.JBwaOS.시험;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Botswana.JBwaOS.기억공간.Geheue_bestuurder;
import Botswana.JBwaOS.기억공간.bladsy_bestuurder;
import Botswana.JBwaOS.입력.입력사건;
import Botswana.JBwaOS.작업.Proses_VALUE;
import Botswana.JBwaOS.체계호출.체계호출;
import Botswana.JBwaOS.lêerstelsel.실행파일적재기;
import Botswana.JBwaOS.kern.kern;
import Botswana.JBwaOS.hou.hou_hardeware;
import Botswana.JBwaOS.IRQ.IRQ_bestuurder;
import Botswana.JBwaOS.서술자.전역서술자표;
import Botswana.JBwaOS.Berging_mobiel.고급기술결합장치;
import Botswana.JBwaOS.mobiel_VALUE.randtoestel_bus_bestuurder;
import Botswana.JBwaOS.Netwerk_Stapel.Netwerk_Nutsmiddels;
import Botswana.JBwaOS.Netwerk_Stapel.Netwerk_laag;
import Botswana.JBwaOS.mobiel_VALUE.Klok;
import Botswana.JBwaOS.서술자.taak_stand_segment;
import Botswana.JBwaOS.화면.karakter_wys;
import Botswana.JBwaOS.lêerstelsel.기본분할영역표;

public final class 전체시험 {
    private static int aanstuur_COUNT;

    private 전체시험() {
    }

    public static void main(String[] 인자) {
        hou_hardeware mobiel_VALUE = new hou_hardeware();
        kern kern_VALUE = new kern(mobiel_VALUE);
        kern_VALUE.Loop();

        기억공간시험(kern_VALUE);
        쪽관리시험(kern_VALUE);
        파일과과정시험(kern_VALUE);
        실행파일시험(kern_VALUE);
        입력시험(kern_VALUE);
        하드웨어시험(mobiel_VALUE);
        개입중단과서술자시험();
        저장장치와통신망시험();
        화면과시계시험();

        System.out.println("JBwaOS 시험 aanstuur_VALUE: " + aanstuur_COUNT);
    }

    private static void 기억공간시험(kern kern_VALUE) {
        Geheue_bestuurder bestuurder_VALUE = kern_VALUE.기억공간();
        int 첫주소 = bestuurder_VALUE.정렬할당(100, 64);
        verifieer((첫주소 & 63) == 0, "belyn_VALUE toewys_Berging");
        bestuurder_VALUE.skryf_greep_VALUE(첫주소, (byte) 0x5a);
        verifieer(bestuurder_VALUE.바이트읽기(첫주소) == (byte) 0x5a, "물리 기억공간 읽고 Skryf");
        int 사용전 = bestuurder_VALUE.사용크기();
        bestuurder_VALUE.stel_vry_Berging(첫주소);
        verifieer(bestuurder_VALUE.사용크기() < 사용전, "기억공간 stel_vry_Berging");
    }

    private static void 쪽관리시험(kern kern_VALUE) {
        bladsy_bestuurder bestuurder_VALUE = kern_VALUE.쪽관리();
        bladsy_bestuurder.adres_ruimte 부모공간 = bestuurder_VALUE.새주소공간();
        bestuurder_VALUE.MAP_bladsy(부모공간, 0x1000, true);
        bestuurder_VALUE.skryf_greep_VALUE(부모공간, 0x1010, (byte) 7);
        bladsy_bestuurder.adres_ruimte kind_ruimte = bestuurder_VALUE.쓰기시복사복제(부모공간);
        bestuurder_VALUE.skryf_greep_VALUE(kind_ruimte, 0x1010, (byte) 9);
        verifieer(bestuurder_VALUE.바이트읽기(부모공간, 0x1010) == 7, "Skryf 시 geval_VALUE 부모 격리");
        verifieer(bestuurder_VALUE.바이트읽기(kind_ruimte, 0x1010) == 9, "Skryf 시 geval_VALUE kind_VALUE Skryf");
    }

    private static void 파일과과정시험(kern kern_VALUE) {
        byte[] Inhoud_VALUE = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        kern_VALUE.lêerstelsel().파일추가("시험", Inhoud_VALUE);
        Proses_VALUE 부모 = kern_VALUE.첫과정();
        체계호출 호출 = kern_VALUE.체계호출();
        int 서술자 = 호출.skep(부모, "/시험", 체계호출.leesalleen_vlag);
        verifieer(서술자 >= 3, "Lêer skep");

        byte[] 받을곳 = new byte[Inhoud_VALUE.length];
        verifieer(호출.Lees(부모, 서술자, 받을곳, 받을곳.length) == Inhoud_VALUE.length, "Lêer Lees");
        verifieer(Arrays.equals(Inhoud_VALUE, 받을곳), "Lêer Inhoud_VALUE");
        verifieer(호출.skuif_plaas(부모, 서술자, 0, 체계호출.Soek_BEGIN) == 0, "Lêer Posisie skuif_VALUE");

        int 복제서술자 = 호출.서술자복제(부모, 서술자);
        verifieer(복제서술자 >= 0, "서술자 복제");
        Proses_VALUE kind_VALUE = 호출.과정복제(부모);
        verifieer(kind_VALUE.waarde_VALUE() != 부모.waarde_VALUE(), "Proses_VALUE waarde_VALUE 분리");
        verifieer(kind_VALUE.부모식별자() == 부모.waarde_VALUE(), "부모 Proses_VALUE waarde_VALUE");
        verifieer(호출.Sluit(kind_VALUE, 서술자) == 0 && 부모.파일서술자().열려있음(서술자), "kind_VALUE Sluit 격리");

        int 이전끝 = 호출.프로그램끝늘리기(부모, 8192);
        verifieer(이전끝 == 0x06000000, "program_f5044b9b 끝 늘리기");
        verifieer(부모.프로그램끝() == 0x06002000, "program_f5044b9b 끝 반영");
        verifieer(kind_VALUE.프로그램끝() == 0x06000000, "과정별 program_f5044b9b 끝 격리");

        kind_VALUE.Verlaat_program(7);
        verifieer(호출.자식기다리기(부모, kind_VALUE.waarde_VALUE(), false) == (7 << 8), "kind_VALUE Verlaat_program 기다리기");
        verifieer(호출.접근가능("시험", 1) == -13, "uitvoer_bevel toestemming_VALUE 거부");
        verifieer(호출.gebruiker_waarde() == 0 && 호출.Groep_waarde() == 0, "사용자와 무리 waarde_VALUE");
        verifieer("/".equals(호출.현재작업목록(2)) && 호출.SWITCH_taaklys("/") == 0, "현재 작업 inskrywing_Lys");
        verifieer(호출.단말인가(부모, 1), "표준 Afvoer 단말");
        verifieer("JBwaOS".equals(호출.체계정보().stelsel_naam()), "bedryfstelsel_VALUE Stelselinfo");
    }

    private static void 실행파일시험(kern kern_VALUE) {
        byte[] data = new byte[92];
        data[0] = 0x7f;
        data[1] = 'E';
        data[2] = 'L';
        data[3] = 'F';
        data[4] = 1;
        data[5] = 1;
        skryf_heelgetal_VALUE(data, 24, 0x04001000);
        skryf_heelgetal_VALUE(data, 32, 52);
        짧은정수쓰기(data, 46, 40);
        짧은정수쓰기(data, 48, 1);
        skryf_heelgetal_VALUE(data, 56, 8);
        skryf_heelgetal_VALUE(data, 60, 2);
        skryf_heelgetal_VALUE(data, 64, 0x04002000);
        skryf_heelgetal_VALUE(data, 72, 64);

        실행파일적재기.foto foto_VALUE = new 실행파일적재기().검사(data);
        verifieer(foto_VALUE.BEGIN_adres() == 0x04001000, "ELF Loop adres");
        verifieer(foto_VALUE.구역들().size() == 1 && foto_VALUE.구역들().get(0).종류() == 8, "ELF 빈 data seksie_VALUE");
        int 서술자 = kern_VALUE.체계호출().skep(kern_VALUE.첫과정(), "시험", 체계호출.leesalleen_vlag);
        verifieer(kern_VALUE.체계호출().lêer_kontrole(kern_VALUE.첫과정(), 서술자, 2, 1) == 0, "uitvoer_bevel 시 Sluit Instellings");
        verifieer(kern_VALUE.체계호출().uitvoer_bevel(kern_VALUE.첫과정(), data, new String[] {"시험", "값"}, new String[] {"Taal=한국어"}) == 0, "ELF uitvoer_bevel foto_VALUE 적재");
        verifieer(kern_VALUE.첫과정().실행시작주소() == 0x04001000, "uitvoer_bevel Loop adres 반영");
        verifieer(kern_VALUE.첫과정().실행인자().length == 2 && kern_VALUE.첫과정().환경값().length == 1, "uitvoer_bevel 인자와 환경");
        verifieer(!kern_VALUE.첫과정().파일서술자().열려있음(서술자), "uitvoer_bevel 시 서술자 Sluit");
        verifieer(kern_VALUE.쪽관리().바이트읽기(kern_VALUE.첫과정().adres_ruimte(), 0x04002000) == 0, "빈 data seksie_VALUE 영 inisialiseer");
    }

    private static void 입력시험(kern kern_VALUE) {
        kern_VALUE.입력관리().키누름('가');
        kern_VALUE.입력관리().쥐이동(3, -2);
        입력사건 첫사건 = kern_VALUE.입력관리().Volgende_gebeurtenis();
        입력사건 SECOND_gebeurtenis = kern_VALUE.입력관리().Volgende_gebeurtenis();
        verifieer(첫사건.사건종류() == 입력사건.종류.키누름, "자판 gebeurtenis");
        verifieer(SECOND_gebeurtenis.첫째값() == 3 && SECOND_gebeurtenis.SECOND_VALUE() == -2, "쥐 skuif_VALUE gebeurtenis");
    }

    private static void 하드웨어시험(hou_hardeware mobiel_VALUE) {
        mobiel_VALUE.skryf_ombou_greep(0x3f8, 0xab);
        verifieer(mobiel_VALUE.포트바이트읽기(0x3f8) == 0xab, "hardeware_ombou I_O 경계");
        verifieer(mobiel_VALUE.직렬기록().contains("JBwaOS"), "직렬 LOG_ry");
    }

    private static void 개입중단과서술자시험() {
        IRQ_bestuurder bestuurder_VALUE = new IRQ_bestuurder();
        bestuurder_VALUE.registreer_inskrywing(0x21, Berging_adres -> Berging_adres + 4);
        bestuurder_VALUE.aktiveer();
        verifieer(bestuurder_VALUE.versprei_VALUE(0x21, 100) == 104, "IRQ versprei_VALUE");
        bestuurder_VALUE.deaktiveer();
        verifieer(bestuurder_VALUE.versprei_VALUE(0x21, 100) == 100, "IRQ deaktiveer");

        전역서술자표 서술자표 = new 전역서술자표();
        서술자표.stel_verstekwaarde();
        verifieer(서술자표.조각들().size() == 5, "전역 서술자표");
        taak_stand_segment taak_stand = new taak_stand_segment();
        taak_stand.특권쌓임공간설정(0x10, 0x800000);
        verifieer(taak_stand.영번쌓임조각() == 0x10 && taak_stand.영번쌓임주소() == 0x800000, "작업 stand_VALUE seksie_VALUE");
    }

    private static void 저장장치와통신망시험() {
        고급기술결합장치 Berging_mobiel = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.seksie_verstel];
        byte[] 읽은자료 = new byte[고급기술결합장치.seksie_verstel];
        쓸자료[17] = 42;
        Berging_mobiel.Skryf(2, 쓸자료);
        Berging_mobiel.Lees(2, 읽은자료);
        verifieer(읽은자료[17] == 42, "ATA seksie_VALUE 읽고 Skryf");

        randtoestel_bus_bestuurder randtoestel = new randtoestel_bus_bestuurder();
        randtoestel.발견(new randtoestel_bus_bestuurder.mobiel_VALUE(0x1022, 0x2000, 0xc000, 11));
        verifieer(randtoestel.FIND_inskrywing(0x1022, 0x2000) != null, "주변 mobiel_VALUE FIND_inskrywing");

        byte[] Ethernet_raam = new byte[34];
        Ethernet_raam[12] = 0x08;
        Ethernet_raam[13] = 0x00;
        Ethernet_raam[14] = 0x45;
        verifieer(Netwerk_Nutsmiddels.Ethernet_UPPER_protokol(Ethernet_raam) == 0x0800, "이더넷 상위 saak_VALUE");
        verifieer(Netwerk_Nutsmiddels.상호통신망규약사판인가(Ethernet_raam, 14), "상호통신망규약 4판");
        verifieer(Netwerk_Nutsmiddels.인터넷검사합(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 검사합");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        skryf_heelgetal_VALUE(첫구역, 454, 63);
        skryf_heelgetal_VALUE(첫구역, 458, 1024);
        verifieer(new 기본분할영역표().Lees(첫구역).size() == 1, "verstekwaarde 분할 영역표");

        Netwerk_laag laag_VALUE = new Netwerk_laag();
        int[] RECEIVED_COUNT = new int[1];
        laag_VALUE.registreer_gebruiker_data_les(7, (data, Loop, lengte_VALUE) -> RECEIVED_COUNT[0]++);
        byte[] raam_INDEX = new byte[14 + 20 + 8];
        raam_INDEX[12] = 0x08;
        raam_INDEX[13] = 0x00;
        raam_INDEX[14] = 0x45;
        raam_INDEX[16] = 0;
        raam_INDEX[17] = 28;
        raam_INDEX[23] = 17;
        raam_INDEX[36] = 0;
        raam_INDEX[37] = 7;
        verifieer(laag_VALUE.이더넷받기(raam_INDEX) && RECEIVED_COUNT[0] == 1, "gebruiker data les_VALUE versprei_VALUE");
    }

    private static void 화면과시계시험() {
        karakter_wys 화면 = new karakter_wys();
        화면.Afvoer("가나\n다");
        verifieer(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 Afvoer");
        Klok Klok = new Klok(100);
        for (int INDEX = 0; INDEX < 10; INDEX++) {
            Klok.틱();
        }
        verifieer(Klok.지난밀리초() == 100, "Klok 틱 CONVERT_VALUE");
    }

    private static void skryf_heelgetal_VALUE(byte[] data, int Posisie, int VALUE) {
        data[Posisie] = (byte) VALUE;
        data[Posisie + 1] = (byte) (VALUE >>> 8);
        data[Posisie + 2] = (byte) (VALUE >>> 16);
        data[Posisie + 3] = (byte) (VALUE >>> 24);
    }

    private static void 짧은정수쓰기(byte[] data, int Posisie, int VALUE) {
        data[Posisie] = (byte) VALUE;
        data[Posisie + 1] = (byte) (VALUE >>> 8);
    }

    private static void verifieer(boolean toestand, String Naam) {
        if (!toestand) {
            throw new AssertionError("faling_VALUE: " + Naam);
        }
        aanstuur_COUNT++;
        System.out.println("aanstuur_VALUE: " + Naam);
    }
}
