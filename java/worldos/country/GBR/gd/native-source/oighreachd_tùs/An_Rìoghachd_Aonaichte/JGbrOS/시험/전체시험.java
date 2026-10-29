// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package An_Rìoghachd_Aonaichte.JGbrOS.시험;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import An_Rìoghachd_Aonaichte.JGbrOS.기억공간.cuimhne_manaidsear;
import An_Rìoghachd_Aonaichte.JGbrOS.기억공간.duilleag_manaidsear;
import An_Rìoghachd_Aonaichte.JGbrOS.입력.입력사건;
import An_Rìoghachd_Aonaichte.JGbrOS.작업.Pròiseas_VALUE;
import An_Rìoghachd_Aonaichte.JGbrOS.체계호출.체계호출;
import An_Rìoghachd_Aonaichte.JGbrOS.siostam_fhaidhlichean.실행파일적재기;
import An_Rìoghachd_Aonaichte.JGbrOS.eitean.eitean;
import An_Rìoghachd_Aonaichte.JGbrOS.òstair.호스트하드웨어;
import An_Rìoghachd_Aonaichte.JGbrOS.interrupt.interrupt_manaidsear;
import An_Rìoghachd_Aonaichte.JGbrOS.서술자.전역서술자표;
import An_Rìoghachd_Aonaichte.JGbrOS.stòras_uidheam.고급기술결합장치;
import An_Rìoghachd_Aonaichte.JGbrOS.uidheam_VALUE.co_inneal_bus_manaidsear;
import An_Rìoghachd_Aonaichte.JGbrOS.lìonra_stac.lìonra_innealan;
import An_Rìoghachd_Aonaichte.JGbrOS.lìonra_stac.lìonra_breath;
import An_Rìoghachd_Aonaichte.JGbrOS.uidheam_VALUE.cleoc;
import An_Rìoghachd_Aonaichte.JGbrOS.서술자.saothair_cor_gearradh;
import An_Rìoghachd_Aonaichte.JGbrOS.화면.caractar_taisbean;
import An_Rìoghachd_Aonaichte.JGbrOS.siostam_fhaidhlichean.기본분할영역표;

public final class 전체시험 {
    private static int sìn_air_adhart_COUNT;

    private 전체시험() {
    }

    public static void main(String[] 인자) {
        호스트하드웨어 uidheam_VALUE = new 호스트하드웨어();
        eitean eitean_VALUE = new eitean(uidheam_VALUE);
        eitean_VALUE.ruith();

        기억공간시험(eitean_VALUE);
        쪽관리시험(eitean_VALUE);
        파일과과정시험(eitean_VALUE);
        실행파일시험(eitean_VALUE);
        입력시험(eitean_VALUE);
        하드웨어시험(uidheam_VALUE);
        개입중단과서술자시험();
        저장장치와통신망시험();
        화면과시계시험();

        System.out.println("JGbrOS 시험 sìn_air_adhart_VALUE: " + sìn_air_adhart_COUNT);
    }

    private static void 기억공간시험(eitean eitean_VALUE) {
        cuimhne_manaidsear manaidsear_VALUE = eitean_VALUE.기억공간();
        int 첫주소 = manaidsear_VALUE.정렬할당(100, 64);
        dearbh((첫주소 & 63) == 0, "co_thaobhaich_VALUE sònraich_stòras");
        manaidsear_VALUE.sgrìobh_baidht_VALUE(첫주소, (byte) 0x5a);
        dearbh(manaidsear_VALUE.바이트읽기(첫주소) == (byte) 0x5a, "물리 기억공간 읽고 sgrìobh");
        int 사용전 = manaidsear_VALUE.사용크기();
        manaidsear_VALUE.sgaoileadh_stòras(첫주소);
        dearbh(manaidsear_VALUE.사용크기() < 사용전, "기억공간 sgaoileadh_stòras");
    }

    private static void 쪽관리시험(eitean eitean_VALUE) {
        duilleag_manaidsear manaidsear_VALUE = eitean_VALUE.쪽관리();
        duilleag_manaidsear.ADDRESS_spàs 부모공간 = manaidsear_VALUE.새주소공간();
        manaidsear_VALUE.MAP_duilleag(부모공간, 0x1000, true);
        manaidsear_VALUE.sgrìobh_baidht_VALUE(부모공간, 0x1010, (byte) 7);
        duilleag_manaidsear.ADDRESS_spàs duine_cloinne_spàs = manaidsear_VALUE.쓰기시복사복제(부모공간);
        manaidsear_VALUE.sgrìobh_baidht_VALUE(duine_cloinne_spàs, 0x1010, (byte) 9);
        dearbh(manaidsear_VALUE.바이트읽기(부모공간, 0x1010) == 7, "sgrìobh 시 ionstans_VALUE 부모 격리");
        dearbh(manaidsear_VALUE.바이트읽기(duine_cloinne_spàs, 0x1010) == 9, "sgrìobh 시 ionstans_VALUE duine_cloinne_VALUE sgrìobh");
    }

    private static void 파일과과정시험(eitean eitean_VALUE) {
        byte[] susbaint_VALUE = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        eitean_VALUE.siostam_fhaidhlichean().파일추가("시험", susbaint_VALUE);
        Pròiseas_VALUE 부모 = eitean_VALUE.첫과정();
        체계호출 호출 = eitean_VALUE.체계호출();
        int 서술자 = 호출.fosgail(부모, "/시험", 체계호출.ri_leughadh_a_mhàin_bratach);
        dearbh(서술자 >= 3, "faidhle fosgail");

        byte[] 받을곳 = new byte[susbaint_VALUE.length];
        dearbh(호출.읽기(부모, 서술자, 받을곳, 받을곳.length) == susbaint_VALUE.length, "faidhle 읽기");
        dearbh(Arrays.equals(susbaint_VALUE, 받을곳), "faidhle susbaint_VALUE");
        dearbh(호출.gluais_suidhich(부모, 서술자, 0, 체계호출.lorg_Start) == 0, "faidhle suidhich gluais_VALUE");

        int 복제서술자 = 호출.서술자복제(부모, 서술자);
        dearbh(복제서술자 >= 0, "서술자 복제");
        Pròiseas_VALUE duine_cloinne_VALUE = 호출.과정복제(부모);
        dearbh(duine_cloinne_VALUE.aithnichear_VALUE() != 부모.aithnichear_VALUE(), "Pròiseas_VALUE aithnichear_VALUE 분리");
        dearbh(duine_cloinne_VALUE.부모식별자() == 부모.aithnichear_VALUE(), "부모 Pròiseas_VALUE aithnichear_VALUE");
        dearbh(호출.dùin(duine_cloinne_VALUE, 서술자) == 0 && 부모.파일서술자().열려있음(서술자), "duine_cloinne_VALUE dùin 격리");

        int 이전끝 = 호출.프로그램끝늘리기(부모, 8192);
        dearbh(이전끝 == 0x06000000, "ap_f5044b9b 끝 늘리기");
        dearbh(부모.프로그램끝() == 0x06002000, "ap_f5044b9b 끝 반영");
        dearbh(duine_cloinne_VALUE.프로그램끝() == 0x06000000, "과정별 ap_f5044b9b 끝 격리");

        duine_cloinne_VALUE.fàg_ap(7);
        dearbh(호출.자식기다리기(부모, duine_cloinne_VALUE.aithnichear_VALUE(), false) == (7 << 8), "duine_cloinne_VALUE fàg_ap 기다리기");
        dearbh(호출.접근가능("시험", 1) == -13, "gnìomhaich_àithne cead_VALUE 거부");
        dearbh(호출.cleachdaiche_aithnichear() == 0 && 호출.buidheann_aithnichear() == 0, "사용자와 무리 aithnichear_VALUE");
        dearbh("/".equals(호출.현재작업목록(2)) && 호출.SWITCH_liosta_nan_saothair("/") == 0, "현재 작업 cur_a_steach_Liosta");
        dearbh(호출.단말인가(부모, 1), "표준 출력 단말");
        dearbh("JGbrOS".equals(호출.체계정보().siostam_ainm()), "siostam_obrachaidh_VALUE msinfo32_exe");
    }

    private static void 실행파일시험(eitean eitean_VALUE) {
        byte[] dàta = new byte[92];
        dàta[0] = 0x7f;
        dàta[1] = 'E';
        dàta[2] = 'L';
        dàta[3] = 'F';
        dàta[4] = 1;
        dàta[5] = 1;
        sgrìobh_àireamh_shlàn_VALUE(dàta, 24, 0x04001000);
        sgrìobh_àireamh_shlàn_VALUE(dàta, 32, 52);
        짧은정수쓰기(dàta, 46, 40);
        짧은정수쓰기(dàta, 48, 1);
        sgrìobh_àireamh_shlàn_VALUE(dàta, 56, 8);
        sgrìobh_àireamh_shlàn_VALUE(dàta, 60, 2);
        sgrìobh_àireamh_shlàn_VALUE(dàta, 64, 0x04002000);
        sgrìobh_àireamh_shlàn_VALUE(dàta, 72, 64);

        실행파일적재기.IMAGE IMAGE_VALUE = new 실행파일적재기().검사(dàta);
        dearbh(IMAGE_VALUE.Start_ADDRESS() == 0x04001000, "ELF ruith ADDRESS");
        dearbh(IMAGE_VALUE.구역들().size() == 1 && IMAGE_VALUE.구역들().get(0).종류() == 8, "ELF 빈 dàta earrann_VALUE");
        int 서술자 = eitean_VALUE.체계호출().fosgail(eitean_VALUE.첫과정(), "시험", 체계호출.ri_leughadh_a_mhàin_bratach);
        dearbh(eitean_VALUE.체계호출().faidhle_smachd(eitean_VALUE.첫과정(), 서술자, 2, 1) == 0, "gnìomhaich_àithne 시 dùin roghainnean");
        dearbh(eitean_VALUE.체계호출().gnìomhaich_àithne(eitean_VALUE.첫과정(), dàta, new String[] {"시험", "값"}, new String[] {"cànan=한국어"}) == 0, "ELF gnìomhaich_àithne IMAGE_VALUE 적재");
        dearbh(eitean_VALUE.첫과정().실행시작주소() == 0x04001000, "gnìomhaich_àithne ruith ADDRESS 반영");
        dearbh(eitean_VALUE.첫과정().실행인자().length == 2 && eitean_VALUE.첫과정().환경값().length == 1, "gnìomhaich_àithne 인자와 환경");
        dearbh(!eitean_VALUE.첫과정().파일서술자().열려있음(서술자), "gnìomhaich_àithne 시 서술자 dùin");
        dearbh(eitean_VALUE.쪽관리().바이트읽기(eitean_VALUE.첫과정().ADDRESS_spàs(), 0x04002000) == 0, "빈 dàta earrann_VALUE 영 ro_shuidhich");
    }

    private static void 입력시험(eitean eitean_VALUE) {
        eitean_VALUE.입력관리().키누름('가');
        eitean_VALUE.입력관리().쥐이동(3, -2);
        입력사건 첫사건 = eitean_VALUE.입력관리().air_adhart_tachartas();
        입력사건 SECOND_tachartas = eitean_VALUE.입력관리().air_adhart_tachartas();
        dearbh(첫사건.사건종류() == 입력사건.종류.키누름, "자판 tachartas");
        dearbh(SECOND_tachartas.첫째값() == 3 && SECOND_tachartas.SECOND_VALUE() == -2, "쥐 gluais_VALUE tachartas");
    }

    private static void 하드웨어시험(호스트하드웨어 uidheam_VALUE) {
        uidheam_VALUE.sgrìobh_port_baidht(0x3f8, 0xab);
        dearbh(uidheam_VALUE.포트바이트읽기(0x3f8) == 0xab, "포트 I_O 경계");
        dearbh(uidheam_VALUE.직렬기록().contains("JGbrOS"), "직렬 LOG_ràgh");
    }

    private static void 개입중단과서술자시험() {
        interrupt_manaidsear manaidsear_VALUE = new interrupt_manaidsear();
        manaidsear_VALUE.clàraich_cur_a_steach(0x21, stòras_ADDRESS -> stòras_ADDRESS + 4);
        manaidsear_VALUE.cuir_an_comas();
        dearbh(manaidsear_VALUE.sgaoil_VALUE(0x21, 100) == 104, "interrupt sgaoil_VALUE");
        manaidsear_VALUE.cuir_à_gnìomh();
        dearbh(manaidsear_VALUE.sgaoil_VALUE(0x21, 100) == 100, "interrupt cuir_à_gnìomh");

        전역서술자표 서술자표 = new 전역서술자표();
        서술자표.seata_luach_bunaiteach();
        dearbh(서술자표.조각들().size() == 5, "전역 서술자표");
        saothair_cor_gearradh saothair_cor = new saothair_cor_gearradh();
        saothair_cor.특권쌓임공간설정(0x10, 0x800000);
        dearbh(saothair_cor.영번쌓임조각() == 0x10 && saothair_cor.영번쌓임주소() == 0x800000, "작업 cor_VALUE earrann_VALUE");
    }

    private static void 저장장치와통신망시험() {
        고급기술결합장치 stòras_uidheam = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.earrann_atharraich_am_meud];
        byte[] 읽은자료 = new byte[고급기술결합장치.earrann_atharraich_am_meud];
        쓸자료[17] = 42;
        stòras_uidheam.sgrìobh(2, 쓸자료);
        stòras_uidheam.읽기(2, 읽은자료);
        dearbh(읽은자료[17] == 42, "ATA earrann_VALUE 읽고 sgrìobh");

        co_inneal_bus_manaidsear co_inneal = new co_inneal_bus_manaidsear();
        co_inneal.발견(new co_inneal_bus_manaidsear.uidheam_VALUE(0x1022, 0x2000, 0xc000, 11));
        dearbh(co_inneal.FIND_cur_a_steach(0x1022, 0x2000) != null, "주변 uidheam_VALUE FIND_cur_a_steach");

        byte[] Ethernet_frèam = new byte[34];
        Ethernet_frèam[12] = 0x08;
        Ethernet_frèam[13] = 0x00;
        Ethernet_frèam[14] = 0x45;
        dearbh(lìonra_innealan.Ethernet_UPPER_pròtacal(Ethernet_frèam) == 0x0800, "이더넷 상위 cùis_VALUE");
        dearbh(lìonra_innealan.상호통신망규약사판인가(Ethernet_frèam, 14), "상호통신망규약 4판");
        dearbh(lìonra_innealan.인터넷검사합(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 검사합");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        sgrìobh_àireamh_shlàn_VALUE(첫구역, 454, 63);
        sgrìobh_àireamh_shlàn_VALUE(첫구역, 458, 1024);
        dearbh(new 기본분할영역표().읽기(첫구역).size() == 1, "luach_bunaiteach 분할 영역표");

        lìonra_breath breath_VALUE = new lìonra_breath();
        int[] RECEIVED_COUNT = new int[1];
        breath_VALUE.clàraich_cleachdaiche_dàta_leasan(7, (dàta, ruith, faid_VALUE) -> RECEIVED_COUNT[0]++);
        byte[] frèam_INDEX = new byte[14 + 20 + 8];
        frèam_INDEX[12] = 0x08;
        frèam_INDEX[13] = 0x00;
        frèam_INDEX[14] = 0x45;
        frèam_INDEX[16] = 0;
        frèam_INDEX[17] = 28;
        frèam_INDEX[23] = 17;
        frèam_INDEX[36] = 0;
        frèam_INDEX[37] = 7;
        dearbh(breath_VALUE.이더넷받기(frèam_INDEX) && RECEIVED_COUNT[0] == 1, "cleachdaiche dàta leasan_VALUE sgaoil_VALUE");
    }

    private static void 화면과시계시험() {
        caractar_taisbean 화면 = new caractar_taisbean();
        화면.출력("가나\n다");
        dearbh(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 출력");
        cleoc cleoc = new cleoc(100);
        for (int INDEX = 0; INDEX < 10; INDEX++) {
            cleoc.틱();
        }
        dearbh(cleoc.지난밀리초() == 100, "cleoc 틱 CONVERT_VALUE");
    }

    private static void sgrìobh_àireamh_shlàn_VALUE(byte[] dàta, int suidhich, int VALUE) {
        dàta[suidhich] = (byte) VALUE;
        dàta[suidhich + 1] = (byte) (VALUE >>> 8);
        dàta[suidhich + 2] = (byte) (VALUE >>> 16);
        dàta[suidhich + 3] = (byte) (VALUE >>> 24);
    }

    private static void 짧은정수쓰기(byte[] dàta, int suidhich, int VALUE) {
        dàta[suidhich] = (byte) VALUE;
        dàta[suidhich + 1] = (byte) (VALUE >>> 8);
    }

    private static void dearbh(boolean cumha, String Ainm) {
        if (!cumha) {
            throw new AssertionError("fàilligeadh_VALUE: " + Ainm);
        }
        sìn_air_adhart_COUNT++;
        System.out.println("sìn_air_adhart_VALUE: " + Ainm);
    }
}
