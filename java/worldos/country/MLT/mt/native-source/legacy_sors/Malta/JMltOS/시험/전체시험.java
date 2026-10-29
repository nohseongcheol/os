// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Malta.JMltOS.시험;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Malta.JMltOS.기억공간.Memorja_maniġer;
import Malta.JMltOS.기억공간.paġna_maniġer;
import Malta.JMltOS.입력.입력사건;
import Malta.JMltOS.작업.Proċess_VALUE;
import Malta.JMltOS.체계호출.체계호출;
import Malta.JMltOS.sistema_tal_fajls.실행파일적재기;
import Malta.JMltOS.kernel.kernel;
import Malta.JMltOS.host.호스트하드웨어;
import Malta.JMltOS.IRQ.IRQ_maniġer;
import Malta.JMltOS.서술자.전역서술자표;
import Malta.JMltOS.Ħażna_mowbajl.고급기술결합장치;
import Malta.JMltOS.mowbajl_VALUE.aċċessorju_bus_maniġer;
import Malta.JMltOS.netwerk_Munzell.netwerk_Għodod;
import Malta.JMltOS.netwerk_Munzell.netwerk_saff;
import Malta.JMltOS.mowbajl_VALUE.Arloġġ;
import Malta.JMltOS.서술자.attività_stat_segment;
import Malta.JMltOS.화면.karattru_wera;
import Malta.JMltOS.sistema_tal_fajls.기본분할영역표;

public final class 전체시험 {
    private static int għadda_COUNT;

    private 전체시험() {
    }

    public static void main(String[] 인자) {
        호스트하드웨어 mowbajl_VALUE = new 호스트하드웨어();
        kernel kernel_VALUE = new kernel(mowbajl_VALUE);
        kernel_VALUE.serje();

        기억공간시험(kernel_VALUE);
        쪽관리시험(kernel_VALUE);
        파일과과정시험(kernel_VALUE);
        실행파일시험(kernel_VALUE);
        입력시험(kernel_VALUE);
        하드웨어시험(mowbajl_VALUE);
        개입중단과서술자시험();
        저장장치와통신망시험();
        화면과시계시험();

        System.out.println("JMltOS 시험 għadda_VALUE: " + għadda_COUNT);
    }

    private static void 기억공간시험(kernel kernel_VALUE) {
        Memorja_maniġer maniġer_VALUE = kernel_VALUE.기억공간();
        int 첫주소 = maniġer_VALUE.정렬할당(100, 64);
        vverifika((첫주소 & 63) == 0, "allinja_VALUE alloka_Ħażna");
        maniġer_VALUE.kiteb_byte_VALUE(첫주소, (byte) 0x5a);
        vverifika(maniġer_VALUE.바이트읽기(첫주소) == (byte) 0x5a, "물리 기억공간 읽고 kiteb");
        int 사용전 = maniġer_VALUE.사용크기();
        maniġer_VALUE.mexxi_Ħażna(첫주소);
        vverifika(maniġer_VALUE.사용크기() < 사용전, "기억공간 mexxi_Ħażna");
    }

    private static void 쪽관리시험(kernel kernel_VALUE) {
        paġna_maniġer maniġer_VALUE = kernel_VALUE.쪽관리();
        paġna_maniġer.ADDRESS_SPACE 부모공간 = maniġer_VALUE.새주소공간();
        maniġer_VALUE.MAP_paġna(부모공간, 0x1000, true);
        maniġer_VALUE.kiteb_byte_VALUE(부모공간, 0x1010, (byte) 7);
        paġna_maniġer.ADDRESS_SPACE tfal_SPACE = maniġer_VALUE.쓰기시복사복제(부모공간);
        maniġer_VALUE.kiteb_byte_VALUE(tfal_SPACE, 0x1010, (byte) 9);
        vverifika(maniġer_VALUE.바이트읽기(부모공간, 0x1010) == 7, "kiteb 시 kkopja_VALUE 부모 격리");
        vverifika(maniġer_VALUE.바이트읽기(tfal_SPACE, 0x1010) == 9, "kiteb 시 kkopja_VALUE tfal_VALUE kiteb");
    }

    private static void 파일과과정시험(kernel kernel_VALUE) {
        byte[] Kontenut_VALUE = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        kernel_VALUE.sistema_tal_fajls().파일추가("시험", Kontenut_VALUE);
        Proċess_VALUE 부모 = kernel_VALUE.첫과정();
        체계호출 호출 = kernel_VALUE.체계호출();
        int 서술자 = 호출.fetaħ(부모, "/시험", 체계호출.qari_biss_mmarka);
        vverifika(서술자 >= 3, "fajl fetaħ");

        byte[] 받을곳 = new byte[Kontenut_VALUE.length];
        vverifika(호출.읽기(부모, 서술자, 받을곳, 받을곳.length) == Kontenut_VALUE.length, "fajl 읽기");
        vverifika(Arrays.equals(Kontenut_VALUE, 받을곳), "fajl Kontenut_VALUE");
        vverifika(호출.mexxi_pożizzjoni(부모, 서술자, 0, 체계호출.SEARCH_Bidu) == 0, "fajl pożizzjoni mexxi_VALUE");

        int 복제서술자 = 호출.서술자복제(부모, 서술자);
        vverifika(복제서술자 >= 0, "서술자 복제");
        Proċess_VALUE tfal_VALUE = 호출.과정복제(부모);
        vverifika(tfal_VALUE.identifikatur_VALUE() != 부모.identifikatur_VALUE(), "Proċess_VALUE identifikatur_VALUE 분리");
        vverifika(tfal_VALUE.부모식별자() == 부모.identifikatur_VALUE(), "부모 Proċess_VALUE identifikatur_VALUE");
        vverifika(호출.agħlaq(tfal_VALUE, 서술자) == 0 && 부모.파일서술자().열려있음(서술자), "tfal_VALUE agħlaq 격리");

        int 이전끝 = 호출.프로그램끝늘리기(부모, 8192);
        vverifika(이전끝 == 0x06000000, "programm_f5044b9b 끝 늘리기");
        vverifika(부모.프로그램끝() == 0x06002000, "programm_f5044b9b 끝 반영");
        vverifika(tfal_VALUE.프로그램끝() == 0x06000000, "과정별 programm_f5044b9b 끝 격리");

        tfal_VALUE.Ħruġ_programm(7);
        vverifika(호출.자식기다리기(부모, tfal_VALUE.identifikatur_VALUE(), false) == (7 << 8), "tfal_VALUE Ħruġ_programm 기다리기");
        vverifika(호출.접근가능("시험", 1) == -13, "eżegwixxa_kmand permess_VALUE 거부");
        vverifika(호출.utent_identifikatur() == 0 && 호출.grupp_identifikatur() == 0, "사용자와 무리 identifikatur_VALUE");
        vverifika("/".equals(호출.현재작업목록(2)) && 호출.qaleb_lista_ta_attivitajiet("/") == 0, "현재 작업 entrata_Lista");
        vverifika(호출.단말인가(부모, 1), "표준 출력 단말");
        vverifika("JMltOS".equals(호출.체계정보().sistema_isem()), "sistema_operattiva_VALUE msinfo32_exe");
    }

    private static void 실행파일시험(kernel kernel_VALUE) {
        byte[] data = new byte[92];
        data[0] = 0x7f;
        data[1] = 'E';
        data[2] = 'L';
        data[3] = 'F';
        data[4] = 1;
        data[5] = 1;
        kiteb_numru_sħiħ_VALUE(data, 24, 0x04001000);
        kiteb_numru_sħiħ_VALUE(data, 32, 52);
        짧은정수쓰기(data, 46, 40);
        짧은정수쓰기(data, 48, 1);
        kiteb_numru_sħiħ_VALUE(data, 56, 8);
        kiteb_numru_sħiħ_VALUE(data, 60, 2);
        kiteb_numru_sħiħ_VALUE(data, 64, 0x04002000);
        kiteb_numru_sħiħ_VALUE(data, 72, 64);

        실행파일적재기.IMAGE IMAGE_VALUE = new 실행파일적재기().검사(data);
        vverifika(IMAGE_VALUE.Bidu_ADDRESS() == 0x04001000, "ELF serje ADDRESS");
        vverifika(IMAGE_VALUE.구역들().size() == 1 && IMAGE_VALUE.구역들().get(0).종류() == 8, "ELF 빈 data taqsima_VALUE_366e0bfa");
        int 서술자 = kernel_VALUE.체계호출().fetaħ(kernel_VALUE.첫과정(), "시험", 체계호출.qari_biss_mmarka);
        vverifika(kernel_VALUE.체계호출().fajl_kontroll(kernel_VALUE.첫과정(), 서술자, 2, 1) == 0, "eżegwixxa_kmand 시 agħlaq Settings");
        vverifika(kernel_VALUE.체계호출().eżegwixxa_kmand(kernel_VALUE.첫과정(), data, new String[] {"시험", "값"}, new String[] {"Lingwa=Malti"}) == 0, "ELF eżegwixxa_kmand IMAGE_VALUE 적재");
        vverifika(kernel_VALUE.첫과정().실행시작주소() == 0x04001000, "eżegwixxa_kmand serje ADDRESS 반영");
        vverifika(kernel_VALUE.첫과정().실행인자().length == 2 && kernel_VALUE.첫과정().환경값().length == 1, "eżegwixxa_kmand 인자와 환경");
        vverifika(!kernel_VALUE.첫과정().파일서술자().열려있음(서술자), "eżegwixxa_kmand 시 서술자 agħlaq");
        vverifika(kernel_VALUE.쪽관리().바이트읽기(kernel_VALUE.첫과정().ADDRESS_SPACE(), 0x04002000) == 0, "빈 data taqsima_VALUE_366e0bfa 영 inizjala");
    }

    private static void 입력시험(kernel kernel_VALUE) {
        kernel_VALUE.입력관리().키누름('가');
        kernel_VALUE.입력관리().쥐이동(3, -2);
        입력사건 첫사건 = kernel_VALUE.입력관리().Li_Jmiss_avveniment();
        입력사건 SECOND_avveniment = kernel_VALUE.입력관리().Li_Jmiss_avveniment();
        vverifika(첫사건.사건종류() == 입력사건.종류.키누름, "자판 avveniment");
        vverifika(SECOND_avveniment.첫째값() == 3 && SECOND_avveniment.SECOND_VALUE() == -2, "쥐 mexxi_VALUE avveniment");
    }

    private static void 하드웨어시험(호스트하드웨어 mowbajl_VALUE) {
        mowbajl_VALUE.kiteb_port_byte(0x3f8, 0xab);
        vverifika(mowbajl_VALUE.포트바이트읽기(0x3f8) == 0xab, "포트 I_O 경계");
        vverifika(mowbajl_VALUE.직렬기록().contains("JMltOS"), "직렬 LOG_RECORD");
    }

    private static void 개입중단과서술자시험() {
        IRQ_maniġer maniġer_VALUE = new IRQ_maniġer();
        maniġer_VALUE.i_rreġistra_entrata(0x21, Ħażna_ADDRESS -> Ħażna_ADDRESS + 4);
        maniġer_VALUE.attiva();
        vverifika(maniġer_VALUE.qassam_VALUE(0x21, 100) == 104, "IRQ qassam_VALUE");
        maniġer_VALUE.ddiżattiva();
        vverifika(maniġer_VALUE.qassam_VALUE(0x21, 100) == 100, "IRQ ddiżattiva");

        전역서술자표 서술자표 = new 전역서술자표();
        서술자표.sett_valur_default();
        vverifika(서술자표.조각들().size() == 5, "전역 서술자표");
        attività_stat_segment attività_stat = new attività_stat_segment();
        attività_stat.특권쌓임공간설정(0x10, 0x800000);
        vverifika(attività_stat.영번쌓임조각() == 0x10 && attività_stat.영번쌓임주소() == 0x800000, "작업 stat_VALUE taqsima_VALUE_366e0bfa");
    }

    private static void 저장장치와통신망시험() {
        고급기술결합장치 Ħażna_mowbajl = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.taqsima_daqqas];
        byte[] 읽은자료 = new byte[고급기술결합장치.taqsima_daqqas];
        쓸자료[17] = 42;
        Ħażna_mowbajl.kiteb(2, 쓸자료);
        Ħażna_mowbajl.읽기(2, 읽은자료);
        vverifika(읽은자료[17] == 42, "ATA taqsima_VALUE_366e0bfa 읽고 kiteb");

        aċċessorju_bus_maniġer aċċessorju = new aċċessorju_bus_maniġer();
        aċċessorju.발견(new aċċessorju_bus_maniġer.mowbajl_VALUE(0x1022, 0x2000, 0xc000, 11));
        vverifika(aċċessorju.sab_entrata(0x1022, 0x2000) != null, "주변 mowbajl_VALUE sab_entrata");

        byte[] Ethernet_frejm = new byte[34];
        Ethernet_frejm[12] = 0x08;
        Ethernet_frejm[13] = 0x00;
        Ethernet_frejm[14] = 0x45;
        vverifika(netwerk_Għodod.Ethernet_UPPER_protokoll(Ethernet_frejm) == 0x0800, "이더넷 상위 każ_VALUE");
        vverifika(netwerk_Għodod.상호통신망규약사판인가(Ethernet_frejm, 14), "상호통신망규약 4판");
        vverifika(netwerk_Għodod.인터넷검사합(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 검사합");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        kiteb_numru_sħiħ_VALUE(첫구역, 454, 63);
        kiteb_numru_sħiħ_VALUE(첫구역, 458, 1024);
        vverifika(new 기본분할영역표().읽기(첫구역).size() == 1, "valur_default 분할 영역표");

        netwerk_saff saff_VALUE = new netwerk_saff();
        int[] RECEIVED_COUNT = new int[1];
        saff_VALUE.i_rreġistra_utent_data_lezzjoni(7, (data, serje, tul_VALUE) -> RECEIVED_COUNT[0]++);
        byte[] frejm_INDEX = new byte[14 + 20 + 8];
        frejm_INDEX[12] = 0x08;
        frejm_INDEX[13] = 0x00;
        frejm_INDEX[14] = 0x45;
        frejm_INDEX[16] = 0;
        frejm_INDEX[17] = 28;
        frejm_INDEX[23] = 17;
        frejm_INDEX[36] = 0;
        frejm_INDEX[37] = 7;
        vverifika(saff_VALUE.이더넷받기(frejm_INDEX) && RECEIVED_COUNT[0] == 1, "utent data lezzjoni_VALUE qassam_VALUE");
    }

    private static void 화면과시계시험() {
        karattru_wera 화면 = new karattru_wera();
        화면.출력("가나\n다");
        vverifika(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 출력");
        Arloġġ Arloġġ = new Arloġġ(100);
        for (int INDEX = 0; INDEX < 10; INDEX++) {
            Arloġġ.틱();
        }
        vverifika(Arloġġ.지난밀리초() == 100, "Arloġġ 틱 CONVERT_VALUE");
    }

    private static void kiteb_numru_sħiħ_VALUE(byte[] data, int pożizzjoni, int VALUE) {
        data[pożizzjoni] = (byte) VALUE;
        data[pożizzjoni + 1] = (byte) (VALUE >>> 8);
        data[pożizzjoni + 2] = (byte) (VALUE >>> 16);
        data[pożizzjoni + 3] = (byte) (VALUE >>> 24);
    }

    private static void 짧은정수쓰기(byte[] data, int pożizzjoni, int VALUE) {
        data[pożizzjoni] = (byte) VALUE;
        data[pożizzjoni + 1] = (byte) (VALUE >>> 8);
    }

    private static void vverifika(boolean kondizzjoni, String isem) {
        if (!kondizzjoni) {
            throw new AssertionError("żball_VALUE: " + isem);
        }
        għadda_COUNT++;
        System.out.println("għadda_VALUE: " + isem);
    }
}
