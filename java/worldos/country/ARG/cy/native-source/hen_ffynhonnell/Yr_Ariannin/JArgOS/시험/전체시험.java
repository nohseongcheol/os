// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Yr_Ariannin.JArgOS.시험;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Yr_Ariannin.JArgOS.기억공간.Cof_rheolwr;
import Yr_Ariannin.JArgOS.기억공간.tudalen_rheolwr;
import Yr_Ariannin.JArgOS.입력.입력사건;
import Yr_Ariannin.JArgOS.작업.Proses_VALUE;
import Yr_Ariannin.JArgOS.체계호출.체계호출;
import Yr_Ariannin.JArgOS.system_ffeiliau.실행파일적재기;
import Yr_Ariannin.JArgOS.cnewyllyn.cnewyllyn;
import Yr_Ariannin.JArgOS.lletya.호스트하드웨어;
import Yr_Ariannin.JArgOS.IRQ.IRQ_rheolwr;
import Yr_Ariannin.JArgOS.서술자.전역서술자표;
import Yr_Ariannin.JArgOS.Storio_dyfais.고급기술결합장치;
import Yr_Ariannin.JArgOS.dyfais_VALUE.ategolyn_bws_rheolwr;
import Yr_Ariannin.JArgOS.Rhwydwaith_pentwr.Rhwydwaith_Offer;
import Yr_Ariannin.JArgOS.Rhwydwaith_pentwr.Rhwydwaith_haen;
import Yr_Ariannin.JArgOS.dyfais_VALUE.Cloc;
import Yr_Ariannin.JArgOS.서술자.tasg_cyflwr_segment;
import Yr_Ariannin.JArgOS.화면.nod_dangos;
import Yr_Ariannin.JArgOS.system_ffeiliau.기본분할영역표;

public final class 전체시험 {
    private static int tocyn_COUNT;

    private 전체시험() {
    }

    public static void main(String[] paramedr_arg) {
        호스트하드웨어 dyfais_VALUE = new 호스트하드웨어();
        cnewyllyn cnewyllyn_VALUE = new cnewyllyn(dyfais_VALUE);
        cnewyllyn_VALUE.Gweithredu_2();

        기억공간시험(cnewyllyn_VALUE);
        쪽관리시험(cnewyllyn_VALUE);
        파일과과정시험(cnewyllyn_VALUE);
        실행파일시험(cnewyllyn_VALUE);
        입력시험(cnewyllyn_VALUE);
        하드웨어시험(dyfais_VALUE);
        개입중단과서술자시험();
        저장장치와통신망시험();
        화면과시계시험();

        System.out.println("JArgOS 시험 tocyn_VALUE: " + tocyn_COUNT);
    }

    private static void 기억공간시험(cnewyllyn cnewyllyn_VALUE) {
        Cof_rheolwr rheolwr_VALUE = cnewyllyn_VALUE.기억공간();
        int 첫주소 = rheolwr_VALUE.정렬할당(100, 64);
        dilysu((첫주소 & 63) == 0, "alinio_VALUE dyrannu_Storio");
        rheolwr_VALUE.ysgrifennu_beit_VALUE(첫주소, (byte) 0x5a);
        dilysu(rheolwr_VALUE.바이트읽기(첫주소) == (byte) 0x5a, "물리 기억공간 읽고 Ysgrifennu");
        int 사용전 = rheolwr_VALUE.사용크기();
        rheolwr_VALUE.rhyddhau_Storio(첫주소);
        dilysu(rheolwr_VALUE.사용크기() < 사용전, "기억공간 rhyddhau_Storio");
    }

    private static void 쪽관리시험(cnewyllyn cnewyllyn_VALUE) {
        tudalen_rheolwr rheolwr_VALUE = cnewyllyn_VALUE.쪽관리();
        tudalen_rheolwr.ADDRESS_lle 부모공간 = rheolwr_VALUE.새주소공간();
        rheolwr_VALUE.MAP_tudalen(부모공간, 0x1000, true);
        rheolwr_VALUE.ysgrifennu_beit_VALUE(부모공간, 0x1010, (byte) 7);
        tudalen_rheolwr.ADDRESS_lle iselfen_lle = rheolwr_VALUE.쓰기시복사복제(부모공간);
        rheolwr_VALUE.ysgrifennu_beit_VALUE(iselfen_lle, 0x1010, (byte) 9);
        dilysu(rheolwr_VALUE.바이트읽기(부모공간, 0x1010) == 7, "Ysgrifennu 시 copïo_VALUE 부모 격리");
        dilysu(rheolwr_VALUE.바이트읽기(iselfen_lle, 0x1010) == 9, "Ysgrifennu 시 copïo_VALUE iselfen_VALUE Ysgrifennu");
    }

    private static void 파일과과정시험(cnewyllyn cnewyllyn_VALUE) {
        byte[] Cynnwys_VALUE = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        cnewyllyn_VALUE.system_ffeiliau().파일추가("시험", Cynnwys_VALUE);
        Proses_VALUE 부모 = cnewyllyn_VALUE.첫과정();
        체계호출 호출 = cnewyllyn_VALUE.체계호출();
        int 서술자 = 호출.Agor(부모, "/시험", 체계호출.darllen_yn_unig_fflag);
        dilysu(서술자 >= 3, "Ffeil Agor");

        byte[] 받을곳 = new byte[Cynnwys_VALUE.length];
        dilysu(호출.Darllen(부모, 서술자, 받을곳, 받을곳.length) == Cynnwys_VALUE.length, "Ffeil Darllen");
        dilysu(Arrays.equals(Cynnwys_VALUE, 받을곳), "Ffeil Cynnwys_VALUE");
        dilysu(호출.symud_safle(부모, 서술자, 0, 체계호출.SEARCH_START) == 0, "Ffeil safle symud_VALUE");

        int 복제서술자 = 호출.서술자복제(부모, 서술자);
        dilysu(복제서술자 >= 0, "서술자 복제");
        Proses_VALUE iselfen_VALUE = 호출.과정복제(부모);
        dilysu(iselfen_VALUE.dynodwr_VALUE() != 부모.dynodwr_VALUE(), "Proses_VALUE dynodwr_VALUE 분리");
        dilysu(iselfen_VALUE.부모식별자() == 부모.dynodwr_VALUE(), "부모 Proses_VALUE dynodwr_VALUE");
        dilysu(호출.Cau(iselfen_VALUE, 서술자) == 0 && 부모.파일서술자().technoleg_gwybodaeth_agor(서술자), "iselfen_VALUE Cau 격리");

        int 이전끝 = 호출.프로그램끝늘리기(부모, 8192);
        dilysu(이전끝 == 0x06000000, "Rhaglen_f5044b9b 끝 늘리기");
        dilysu(부모.프로그램끝() == 0x06002000, "Rhaglen_f5044b9b 끝 반영");
        dilysu(iselfen_VALUE.프로그램끝() == 0x06000000, "과정별 Rhaglen_f5044b9b 끝 격리");

        iselfen_VALUE.gadael_Rhaglen(7);
        dilysu(호출.자식기다리기(부모, iselfen_VALUE.dynodwr_VALUE(), false) == (7 << 8), "iselfen_VALUE gadael_Rhaglen 기다리기");
        dilysu(호출.접근가능("시험", 1) == -13, "Gweithredu_gorchymyn hawl_VALUE gwrthod_VALUE");
        dilysu(호출.defnyddiwr_dynodwr() == 0 && 호출.Grŵp_dynodwr() == 0, "사용자와 무리 dynodwr_VALUE");
        dilysu("/".equals(호출.현재작업목록(2)) && 호출.newid_rhestr_tasgau("/") == 0, "현재 작업 cofnod_Rhestr");
        dilysu(호출.technoleg_gwybodaeth_Terfynell(부모, 1), "표준 Allbwn 단말");
        dilysu("JArgOS".equals(호출.체계정보().system_enw()), "system_weithredu_VALUE msinfo32_exe");
    }

    private static void 실행파일시험(cnewyllyn cnewyllyn_VALUE) {
        byte[] data = new byte[92];
        data[0] = 0x7f;
        data[1] = 'E';
        data[2] = 'L';
        data[3] = 'F';
        data[4] = 1;
        data[5] = 1;
        ysgrifennu_cyfanrif_VALUE(data, 24, 0x04001000);
        ysgrifennu_cyfanrif_VALUE(data, 32, 52);
        짧은정수쓰기(data, 46, 40);
        짧은정수쓰기(data, 48, 1);
        ysgrifennu_cyfanrif_VALUE(data, 56, 8);
        ysgrifennu_cyfanrif_VALUE(data, 60, 2);
        ysgrifennu_cyfanrif_VALUE(data, 64, 0x04002000);
        ysgrifennu_cyfanrif_VALUE(data, 72, 64);

        실행파일적재기.llun llun_VALUE = new 실행파일적재기().검사(data);
        dilysu(llun_VALUE.cyfeiriad_cychwyn() == 0x04001000, "ELF Gweithredu_2 ADDRESS");
        dilysu(llun_VALUE.구역들().size() == 1 && llun_VALUE.구역들().get(0).종류() == 8, "ELF 빈 data adran_VALUE");
        int 서술자 = cnewyllyn_VALUE.체계호출().Agor(cnewyllyn_VALUE.첫과정(), "시험", 체계호출.darllen_yn_unig_fflag);
        dilysu(cnewyllyn_VALUE.체계호출().ffeil_rheoli(cnewyllyn_VALUE.첫과정(), 서술자, 2, 1) == 0, "Gweithredu_gorchymyn 시 Cau Gosodiadau");
        dilysu(cnewyllyn_VALUE.체계호출().Gweithredu_gorchymyn(cnewyllyn_VALUE.첫과정(), data, new String[] {"시험", "값"}, new String[] {"Iaith=Cymraeg"}) == 0, "ELF Gweithredu_gorchymyn llun_VALUE 적재");
        dilysu(cnewyllyn_VALUE.첫과정().실행시작주소() == 0x04001000, "Gweithredu_gorchymyn Gweithredu_2 ADDRESS 반영");
        dilysu(cnewyllyn_VALUE.첫과정().실행인자().length == 2 && cnewyllyn_VALUE.첫과정().환경값().length == 1, "Gweithredu_gorchymyn 인자와 환경");
        dilysu(!cnewyllyn_VALUE.첫과정().파일서술자().technoleg_gwybodaeth_agor(서술자), "Gweithredu_gorchymyn 시 서술자 Cau");
        dilysu(cnewyllyn_VALUE.쪽관리().바이트읽기(cnewyllyn_VALUE.첫과정().ADDRESS_lle(), 0x04002000) == 0, "빈 data adran_VALUE 영 ymgychwyn");
    }

    private static void 입력시험(cnewyllyn cnewyllyn_VALUE) {
        cnewyllyn_VALUE.입력관리().키누름('가');
        cnewyllyn_VALUE.입력관리().쥐이동(3, -2);
        입력사건 첫사건 = cnewyllyn_VALUE.입력관리().Nesaf_digwyddiad();
        입력사건 SECOND_digwyddiad = cnewyllyn_VALUE.입력관리().Nesaf_digwyddiad();
        dilysu(첫사건.사건종류() == 입력사건.종류.키누름, "자판 digwyddiad");
        dilysu(SECOND_digwyddiad.첫째값() == 3 && SECOND_digwyddiad.SECOND_VALUE() == -2, "쥐 symud_VALUE digwyddiad");
    }

    private static void 하드웨어시험(호스트하드웨어 dyfais_VALUE) {
        dyfais_VALUE.ysgrifennu_porth_beit(0x3f8, 0xab);
        dilysu(dyfais_VALUE.포트바이트읽기(0x3f8) == 0xab, "포트 I_O 경계");
        dilysu(dyfais_VALUE.직렬기록().contains("JArgOS"), "직렬 LOG_rhes");
    }

    private static void 개입중단과서술자시험() {
        IRQ_rheolwr rheolwr_VALUE = new IRQ_rheolwr();
        rheolwr_VALUE.cofrestru_cofnod(0x21, Storio_ADDRESS -> Storio_ADDRESS + 4);
        rheolwr_VALUE.cychwyn();
        dilysu(rheolwr_VALUE.dosbarthu_VALUE(0x21, 100) == 104, "IRQ dosbarthu_VALUE");
        rheolwr_VALUE.analluogi();
        dilysu(rheolwr_VALUE.dosbarthu_VALUE(0x21, 100) == 100, "IRQ analluogi");

        전역서술자표 서술자표 = new 전역서술자표();
        서술자표.set_gwerth_diofyn();
        dilysu(서술자표.조각들().size() == 5, "전역 서술자표");
        tasg_cyflwr_segment tasg_cyflwr = new tasg_cyflwr_segment();
        tasg_cyflwr.특권쌓임공간설정(0x10, 0x800000);
        dilysu(tasg_cyflwr.영번쌓임조각() == 0x10 && tasg_cyflwr.영번쌓임주소() == 0x800000, "작업 cyflwr_VALUE adran_VALUE");
    }

    private static void 저장장치와통신망시험() {
        고급기술결합장치 Storio_dyfais = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.adran_newid_maint];
        byte[] 읽은자료 = new byte[고급기술결합장치.adran_newid_maint];
        쓸자료[17] = 42;
        Storio_dyfais.Ysgrifennu(2, 쓸자료);
        Storio_dyfais.Darllen(2, 읽은자료);
        dilysu(읽은자료[17] == 42, "ATA adran_VALUE 읽고 Ysgrifennu");

        ategolyn_bws_rheolwr ategolyn = new ategolyn_bws_rheolwr();
        ategolyn.발견(new ategolyn_bws_rheolwr.dyfais_VALUE(0x1022, 0x2000, 0xc000, 11));
        dilysu(ategolyn.FIND_cofnod(0x1022, 0x2000) != null, "주변 dyfais_VALUE FIND_cofnod");

        byte[] Ether_rwyd_ffrâm = new byte[34];
        Ether_rwyd_ffrâm[12] = 0x08;
        Ether_rwyd_ffrâm[13] = 0x00;
        Ether_rwyd_ffrâm[14] = 0x45;
        dilysu(Rhwydwaith_Offer.Ether_rwyd_UPPER_protocol(Ether_rwyd_ffrâm) == 0x0800, "이더넷 상위 tasg_VALUE");
        dilysu(Rhwydwaith_Offer.상호통신망규약사판인가(Ether_rwyd_ffrâm, 14), "상호통신망규약 4판");
        dilysu(Rhwydwaith_Offer.cwmwl_prawfswm(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 prawfswm");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        ysgrifennu_cyfanrif_VALUE(첫구역, 454, 63);
        ysgrifennu_cyfanrif_VALUE(첫구역, 458, 1024);
        dilysu(new 기본분할영역표().Darllen(첫구역).size() == 1, "gwerth_diofyn 분할 영역표");

        Rhwydwaith_haen haen_VALUE = new Rhwydwaith_haen();
        int[] RECEIVED_COUNT = new int[1];
        haen_VALUE.cofrestru_defnyddiwr_data_gwers(7, (data, Gweithredu_2, hyd_VALUE) -> RECEIVED_COUNT[0]++);
        byte[] ffrâm_INDEX = new byte[14 + 20 + 8];
        ffrâm_INDEX[12] = 0x08;
        ffrâm_INDEX[13] = 0x00;
        ffrâm_INDEX[14] = 0x45;
        ffrâm_INDEX[16] = 0;
        ffrâm_INDEX[17] = 28;
        ffrâm_INDEX[23] = 17;
        ffrâm_INDEX[36] = 0;
        ffrâm_INDEX[37] = 7;
        dilysu(haen_VALUE.이더넷받기(ffrâm_INDEX) && RECEIVED_COUNT[0] == 1, "defnyddiwr data gwers_VALUE dosbarthu_VALUE");
    }

    private static void 화면과시계시험() {
        nod_dangos 화면 = new nod_dangos();
        화면.Allbwn("가나\n다");
        dilysu(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 Allbwn");
        Cloc Cloc = new Cloc(100);
        for (int INDEX = 0; INDEX < 10; INDEX++) {
            Cloc.틱();
        }
        dilysu(Cloc.지난밀리초() == 100, "Cloc 틱 CONVERT_VALUE");
    }

    private static void ysgrifennu_cyfanrif_VALUE(byte[] data, int safle, int VALUE) {
        data[safle] = (byte) VALUE;
        data[safle + 1] = (byte) (VALUE >>> 8);
        data[safle + 2] = (byte) (VALUE >>> 16);
        data[safle + 3] = (byte) (VALUE >>> 24);
    }

    private static void 짧은정수쓰기(byte[] data, int safle, int VALUE) {
        data[safle] = (byte) VALUE;
        data[safle + 1] = (byte) (VALUE >>> 8);
    }

    private static void dilysu(boolean cyflwr, String Enw) {
        if (!cyflwr) {
            throw new AssertionError("methiant_VALUE: " + Enw);
        }
        tocyn_COUNT++;
        System.out.println("tocyn_VALUE: " + Enw);
    }
}
