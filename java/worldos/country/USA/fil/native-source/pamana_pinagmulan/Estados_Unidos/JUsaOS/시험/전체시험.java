// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Estados_Unidos.JUsaOS.시험;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Estados_Unidos.JUsaOS.기억공간.Memory_tagapamahala;
import Estados_Unidos.JUsaOS.기억공간.page_tagapamahala;
import Estados_Unidos.JUsaOS.입력.입력사건;
import Estados_Unidos.JUsaOS.작업.Proseso_VALUE;
import Estados_Unidos.JUsaOS.체계호출.체계호출;
import Estados_Unidos.JUsaOS.sistema_ng_file.실행파일적재기;
import Estados_Unidos.JUsaOS.kernel.kernel;
import Estados_Unidos.JUsaOS.host.호스트하드웨어;
import Estados_Unidos.JUsaOS.IRQ.IRQ_tagapamahala;
import Estados_Unidos.JUsaOS.서술자.전역서술자표;
import Estados_Unidos.JUsaOS.Storage_device.고급기술결합장치;
import Estados_Unidos.JUsaOS.device_VALUE.aksesorya_bus_tagapamahala;
import Estados_Unidos.JUsaOS.Network_Stack.Network_Mga_Tool;
import Estados_Unidos.JUsaOS.Network_Stack.Network_patong;
import Estados_Unidos.JUsaOS.device_VALUE.Orasan;
import Estados_Unidos.JUsaOS.서술자.gawain_katayuan_bahagi;
import Estados_Unidos.JUsaOS.화면.karakter_display;
import Estados_Unidos.JUsaOS.sistema_ng_file.기본분할영역표;

public final class 전체시험 {
    private static int ipasa_COUNT;

    private 전체시험() {
    }

    public static void main(String[] parameter_argumento) {
        호스트하드웨어 device_VALUE = new 호스트하드웨어();
        kernel kernel_VALUE = new kernel(device_VALUE);
        kernel_VALUE.run();

        기억공간시험(kernel_VALUE);
        쪽관리시험(kernel_VALUE);
        파일과과정시험(kernel_VALUE);
        실행파일시험(kernel_VALUE);
        입력시험(kernel_VALUE);
        하드웨어시험(device_VALUE);
        개입중단과서술자시험();
        저장장치와통신망시험();
        화면과시계시험();

        System.out.println("JUsaOS 시험 ipasa_VALUE: " + ipasa_COUNT);
    }

    private static void 기억공간시험(kernel kernel_VALUE) {
        Memory_tagapamahala tagapamahala_VALUE = kernel_VALUE.기억공간();
        int 첫주소 = tagapamahala_VALUE.정렬할당(100, 64);
        tiyakin_kumpirmahin((첫주소 & 63) == 0, "maghanay_VALUE maglaan_Storage");
        tagapamahala_VALUE.sumulat_byte_VALUE(첫주소, (byte) 0x5a);
        tiyakin_kumpirmahin(tagapamahala_VALUE.바이트읽기(첫주소) == (byte) 0x5a, "물리 기억공간 읽고 sumulat");
        int 사용전 = tagapamahala_VALUE.사용크기();
        tagapamahala_VALUE.release_Storage(첫주소);
        tiyakin_kumpirmahin(tagapamahala_VALUE.사용크기() < 사용전, "기억공간 release_Storage");
    }

    private static void 쪽관리시험(kernel kernel_VALUE) {
        page_tagapamahala tagapamahala_VALUE = kernel_VALUE.쪽관리();
        page_tagapamahala.email_SPACE 부모공간 = tagapamahala_VALUE.새주소공간();
        tagapamahala_VALUE.MAP_page(부모공간, 0x1000, true);
        tagapamahala_VALUE.sumulat_byte_VALUE(부모공간, 0x1010, (byte) 7);
        page_tagapamahala.email_SPACE anak_SPACE = tagapamahala_VALUE.쓰기시복사복제(부모공간);
        tagapamahala_VALUE.sumulat_byte_VALUE(anak_SPACE, 0x1010, (byte) 9);
        tiyakin_kumpirmahin(tagapamahala_VALUE.바이트읽기(부모공간, 0x1010) == 7, "sumulat 시 gumawa_ng_kopya_VALUE 부모 격리");
        tiyakin_kumpirmahin(tagapamahala_VALUE.바이트읽기(anak_SPACE, 0x1010) == 9, "sumulat 시 gumawa_ng_kopya_VALUE anak_VALUE sumulat");
    }

    private static void 파일과과정시험(kernel kernel_VALUE) {
        byte[] Nilalaman_VALUE = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        kernel_VALUE.sistema_ng_file().파일추가("시험", Nilalaman_VALUE);
        Proseso_VALUE 부모 = kernel_VALUE.첫과정();
        체계호출 호출 = kernel_VALUE.체계호출();
        int 서술자 = 호출.buksan(부모, "/시험", 체계호출.mababasa_lamang_i_flag);
        tiyakin_kumpirmahin(서술자 >= 3, "file buksan");

        byte[] 받을곳 = new byte[Nilalaman_VALUE.length];
        tiyakin_kumpirmahin(호출.읽기(부모, 서술자, 받을곳, 받을곳.length) == Nilalaman_VALUE.length, "file 읽기");
        tiyakin_kumpirmahin(Arrays.equals(Nilalaman_VALUE, 받을곳), "file Nilalaman_VALUE");
        tiyakin_kumpirmahin(호출.ilipat_posisyon(부모, 서술자, 0, 체계호출.SEARCH_Start) == 0, "file posisyon ilipat_VALUE");

        int 복제서술자 = 호출.서술자복제(부모, 서술자);
        tiyakin_kumpirmahin(복제서술자 >= 0, "서술자 복제");
        Proseso_VALUE anak_VALUE = 호출.과정복제(부모);
        tiyakin_kumpirmahin(anak_VALUE.tagakilala_VALUE() != 부모.tagakilala_VALUE(), "Proseso_VALUE tagakilala_VALUE 분리");
        tiyakin_kumpirmahin(anak_VALUE.부모식별자() == 부모.tagakilala_VALUE(), "부모 Proseso_VALUE tagakilala_VALUE");
        tiyakin_kumpirmahin(호출.isara(anak_VALUE, 서술자) == 0 && 부모.파일서술자().information_technology_buksan(서술자), "anak_VALUE isara 격리");

        int 이전끝 = 호출.프로그램끝늘리기(부모, 8192);
        tiyakin_kumpirmahin(이전끝 == 0x06000000, "app_f5044b9b 끝 늘리기");
        tiyakin_kumpirmahin(부모.app_break() == 0x06002000, "app_f5044b9b 끝 반영");
        tiyakin_kumpirmahin(anak_VALUE.app_break() == 0x06000000, "과정별 app_f5044b9b 끝 격리");

        anak_VALUE.Paglabas_app(7);
        tiyakin_kumpirmahin(호출.자식기다리기(부모, anak_VALUE.tagakilala_VALUE(), false) == (7 << 8), "anak_VALUE Paglabas_app 기다리기");
        tiyakin_kumpirmahin(호출.접근가능("시험", 1) == -13, "Mag_execute_utos pahintulot_VALUE tanggihan_VALUE");
        tiyakin_kumpirmahin(호출.gumagamit_tagakilala() == 0 && 호출.Grupo_tagakilala() == 0, "사용자와 무리 tagakilala_VALUE");
        tiyakin_kumpirmahin("/".equals(호출.현재작업목록(2)) && 호출.SWITCH_listahan_ng_gawain("/") == 0, "현재 작업 pagpasok_list");
        tiyakin_kumpirmahin(호출.information_technology_Terminal(부모, 1), "표준 출력 단말");
        tiyakin_kumpirmahin("JUsaOS".equals(호출.체계정보().system_pangalan()), "operating_system_VALUE msinfo32_exe");
    }

    private static void 실행파일시험(kernel kernel_VALUE) {
        byte[] data = new byte[92];
        data[0] = 0x7f;
        data[1] = 'E';
        data[2] = 'L';
        data[3] = 'F';
        data[4] = 1;
        data[5] = 1;
        sumulat_integer_buong_numero_VALUE(data, 24, 0x04001000);
        sumulat_integer_buong_numero_VALUE(data, 32, 52);
        짧은정수쓰기(data, 46, 40);
        짧은정수쓰기(data, 48, 1);
        sumulat_integer_buong_numero_VALUE(data, 56, 8);
        sumulat_integer_buong_numero_VALUE(data, 60, 2);
        sumulat_integer_buong_numero_VALUE(data, 64, 0x04002000);
        sumulat_integer_buong_numero_VALUE(data, 72, 64);

        실행파일적재기.IMAGE IMAGE_VALUE = new 실행파일적재기().검사(data);
        tiyakin_kumpirmahin(IMAGE_VALUE.Start_email() == 0x04001000, "ELF run email");
        tiyakin_kumpirmahin(IMAGE_VALUE.구역들().size() == 1 && IMAGE_VALUE.구역들().get(0).종류() == 8, "ELF 빈 data seksiyon_VALUE");
        int 서술자 = kernel_VALUE.체계호출().buksan(kernel_VALUE.첫과정(), "시험", 체계호출.mababasa_lamang_i_flag);
        tiyakin_kumpirmahin(kernel_VALUE.체계호출().file_control(kernel_VALUE.첫과정(), 서술자, 2, 1) == 0, "Mag_execute_utos 시 isara Mga_Setting");
        tiyakin_kumpirmahin(kernel_VALUE.체계호출().Mag_execute_utos(kernel_VALUE.첫과정(), data, new String[] {"시험", "값"}, new String[] {"Wika=한국어"}) == 0, "ELF Mag_execute_utos IMAGE_VALUE 적재");
        tiyakin_kumpirmahin(kernel_VALUE.첫과정().실행시작주소() == 0x04001000, "Mag_execute_utos run email 반영");
        tiyakin_kumpirmahin(kernel_VALUE.첫과정().실행인자().length == 2 && kernel_VALUE.첫과정().환경값().length == 1, "Mag_execute_utos 인자와 환경");
        tiyakin_kumpirmahin(!kernel_VALUE.첫과정().파일서술자().information_technology_buksan(서술자), "Mag_execute_utos 시 서술자 isara");
        tiyakin_kumpirmahin(kernel_VALUE.쪽관리().바이트읽기(kernel_VALUE.첫과정().email_SPACE(), 0x04002000) == 0, "빈 data seksiyon_VALUE 영 magsimula");
    }

    private static void 입력시험(kernel kernel_VALUE) {
        kernel_VALUE.입력관리().키누름('가');
        kernel_VALUE.입력관리().쥐이동(3, -2);
        입력사건 첫사건 = kernel_VALUE.입력관리().Susunod_kaganapan();
        입력사건 SECOND_kaganapan = kernel_VALUE.입력관리().Susunod_kaganapan();
        tiyakin_kumpirmahin(첫사건.사건종류() == 입력사건.종류.키누름, "자판 kaganapan");
        tiyakin_kumpirmahin(SECOND_kaganapan.첫째값() == 3 && SECOND_kaganapan.SECOND_VALUE() == -2, "쥐 ilipat_VALUE kaganapan");
    }

    private static void 하드웨어시험(호스트하드웨어 device_VALUE) {
        device_VALUE.sumulat_port_byte(0x3f8, 0xab);
        tiyakin_kumpirmahin(device_VALUE.포트바이트읽기(0x3f8) == 0xab, "포트 I_O 경계");
        tiyakin_kumpirmahin(device_VALUE.직렬기록().contains("JUsaOS"), "직렬 LOG_hanay");
    }

    private static void 개입중단과서술자시험() {
        IRQ_tagapamahala tagapamahala_VALUE = new IRQ_tagapamahala();
        tagapamahala_VALUE.magrehistro_pagpasok(0x21, Storage_email -> Storage_email + 4);
        tagapamahala_VALUE.i_on();
        tiyakin_kumpirmahin(tagapamahala_VALUE.ipamahagi_VALUE(0x21, 100) == 104, "IRQ ipamahagi_VALUE");
        tagapamahala_VALUE.ideaktibo();
        tiyakin_kumpirmahin(tagapamahala_VALUE.ipamahagi_VALUE(0x21, 100) == 100, "IRQ ideaktibo");

        전역서술자표 서술자표 = new 전역서술자표();
        서술자표.set_value_ng_default();
        tiyakin_kumpirmahin(서술자표.조각들().size() == 5, "전역 서술자표");
        gawain_katayuan_bahagi gawain_katayuan = new gawain_katayuan_bahagi();
        gawain_katayuan.특권쌓임공간설정(0x10, 0x800000);
        tiyakin_kumpirmahin(gawain_katayuan.영번쌓임조각() == 0x10 && gawain_katayuan.영번쌓임주소() == 0x800000, "작업 katayuan_VALUE seksiyon_VALUE");
    }

    private static void 저장장치와통신망시험() {
        고급기술결합장치 Storage_device = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.seksiyon_sukat];
        byte[] 읽은자료 = new byte[고급기술결합장치.seksiyon_sukat];
        쓸자료[17] = 42;
        Storage_device.sumulat(2, 쓸자료);
        Storage_device.읽기(2, 읽은자료);
        tiyakin_kumpirmahin(읽은자료[17] == 42, "ATA seksiyon_VALUE 읽고 sumulat");

        aksesorya_bus_tagapamahala aksesorya = new aksesorya_bus_tagapamahala();
        aksesorya.발견(new aksesorya_bus_tagapamahala.device_VALUE(0x1022, 0x2000, 0xc000, 11));
        tiyakin_kumpirmahin(aksesorya.FIND_pagpasok(0x1022, 0x2000) != null, "주변 device_VALUE FIND_pagpasok");

        byte[] Ethernet_frame = new byte[34];
        Ethernet_frame[12] = 0x08;
        Ethernet_frame[13] = 0x00;
        Ethernet_frame[14] = 0x45;
        tiyakin_kumpirmahin(Network_Mga_Tool.Ethernet_UPPER_protokol(Ethernet_frame) == 0x0800, "이더넷 상위 kaso_VALUE");
        tiyakin_kumpirmahin(Network_Mga_Tool.상호통신망규약사판인가(Ethernet_frame, 14), "상호통신망규약 4판");
        tiyakin_kumpirmahin(Network_Mga_Tool.cloud_checksum(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 checksum");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        sumulat_integer_buong_numero_VALUE(첫구역, 454, 63);
        sumulat_integer_buong_numero_VALUE(첫구역, 458, 1024);
        tiyakin_kumpirmahin(new 기본분할영역표().읽기(첫구역).size() == 1, "value_ng_default 분할 영역표");

        Network_patong patong_VALUE = new Network_patong();
        int[] RECEIVED_COUNT = new int[1];
        patong_VALUE.magrehistro_gumagamit_data_aralin(7, (data, run, haba_VALUE) -> RECEIVED_COUNT[0]++);
        byte[] frame_INDEX = new byte[14 + 20 + 8];
        frame_INDEX[12] = 0x08;
        frame_INDEX[13] = 0x00;
        frame_INDEX[14] = 0x45;
        frame_INDEX[16] = 0;
        frame_INDEX[17] = 28;
        frame_INDEX[23] = 17;
        frame_INDEX[36] = 0;
        frame_INDEX[37] = 7;
        tiyakin_kumpirmahin(patong_VALUE.이더넷받기(frame_INDEX) && RECEIVED_COUNT[0] == 1, "gumagamit data aralin_VALUE ipamahagi_VALUE");
    }

    private static void 화면과시계시험() {
        karakter_display 화면 = new karakter_display();
        화면.출력("가나\n다");
        tiyakin_kumpirmahin(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 출력");
        Orasan Orasan = new Orasan(100);
        for (int INDEX = 0; INDEX < 10; INDEX++) {
            Orasan.틱();
        }
        tiyakin_kumpirmahin(Orasan.지난밀리초() == 100, "Orasan 틱 CONVERT_VALUE");
    }

    private static void sumulat_integer_buong_numero_VALUE(byte[] data, int posisyon, int VALUE) {
        data[posisyon] = (byte) VALUE;
        data[posisyon + 1] = (byte) (VALUE >>> 8);
        data[posisyon + 2] = (byte) (VALUE >>> 16);
        data[posisyon + 3] = (byte) (VALUE >>> 24);
    }

    private static void 짧은정수쓰기(byte[] data, int posisyon, int VALUE) {
        data[posisyon] = (byte) VALUE;
        data[posisyon + 1] = (byte) (VALUE >>> 8);
    }

    private static void tiyakin_kumpirmahin(boolean kondisyon, String pangalan) {
        if (!kondisyon) {
            throw new AssertionError("pagpalya_VALUE: " + pangalan);
        }
        ipasa_COUNT++;
        System.out.println("ipasa_VALUE: " + pangalan);
    }
}
