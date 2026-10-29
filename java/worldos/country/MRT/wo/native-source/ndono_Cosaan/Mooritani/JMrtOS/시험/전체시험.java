// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Mooritani.JMrtOS.시험;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Mooritani.JMrtOS.기억공간.fatlekookaay_doxalkat;
import Mooritani.JMrtOS.기억공간.xët_doxalkat;
import Mooritani.JMrtOS.입력.입력사건;
import Mooritani.JMrtOS.작업.yokkute_xëyma;
import Mooritani.JMrtOS.체계호출.체계호출;
import Mooritani.JMrtOS.barabu_boolebdenc_yu_ñu_bennal.실행파일적재기;
import Mooritani.JMrtOS.xoox.xoox;
import Mooritani.JMrtOS.dalal.dalal_jumtukaay;
import Mooritani.JMrtOS.dog.dog_doxalkat;
import Mooritani.JMrtOS.서술자.전역서술자표;
import Mooritani.JMrtOS.Dencukaay_toftal.고급기술결합장치;
import Mooritani.JMrtOS.toftal_xëyma.toftal_Doxkatu_diggante_doxalkat;
import Mooritani.JMrtOS.mbaal_Tegalo.mbaal_Jumtukaay_yi;
import Mooritani.JMrtOS.mbaal_Tegalo.mbaal_déggoob_wet;
import Mooritani.JMrtOS.toftal_xëyma.Yeetekaay_ak_Montar;
import Mooritani.JMrtOS.서술자.ligeey_nekkin_dog;
import Mooritani.JMrtOS.화면.Araf_laa;
import Mooritani.JMrtOS.barabu_boolebdenc_yu_ñu_bennal.기본분할영역표;

public final class 전체시험 {
    private static int 통과수;

    private 전체시험() {
    }

    public static void main(String[] 인자) {
        dalal_jumtukaay toftal_xëyma = new dalal_jumtukaay();
        xoox xoox_xëyma = new xoox(toftal_xëyma);
        xoox_xëyma.daw();

        기억공간시험(xoox_xëyma);
        쪽관리시험(xoox_xëyma);
        파일과과정시험(xoox_xëyma);
        실행파일시험(xoox_xëyma);
        입력시험(xoox_xëyma);
        하드웨어시험(toftal_xëyma);
        개입중단과서술자시험();
        저장장치와통신망시험();
        화면과시계시험();

        System.out.println("JMrtOS 시험 jox_xëyma: " + 통과수);
    }

    private static void 기억공간시험(xoox xoox_xëyma) {
        fatlekookaay_doxalkat doxalkat_xëyma = xoox_xëyma.기억공간();
        int 첫주소 = doxalkat_xëyma.정렬할당(100, 64);
        luñutu((첫주소 & 63) == 0, "Féeteel_xëyma jagleel_Dencukaay");
        doxalkat_xëyma.biir_okte_xëyma(첫주소, (byte) 0x5a);
        luñutu(doxalkat_xëyma.바이트읽기(첫주소) == (byte) 0x5a, "물리 기억공간 읽고 biir");
        int 사용전 = doxalkat_xëyma.사용크기();
        doxalkat_xëyma.yewwi_Dencukaay(첫주소);
        luñutu(doxalkat_xëyma.사용크기() < 사용전, "기억공간 yewwi_Dencukaay");
    }

    private static void 쪽관리시험(xoox xoox_xëyma) {
        xët_doxalkat doxalkat_xëyma = xoox_xëyma.쪽관리();
        xët_doxalkat.dëkkuwaay_Espace 부모공간 = doxalkat_xëyma.새주소공간();
        doxalkat_xëyma.fésal_dëkkuwaay_bi_ciw_kart_xët(부모공간, 0x1000, true);
        doxalkat_xëyma.biir_okte_xëyma(부모공간, 0x1010, (byte) 7);
        xët_doxalkat.dëkkuwaay_Espace xale_Espace = doxalkat_xëyma.쓰기시복사복제(부모공간);
        doxalkat_xëyma.biir_okte_xëyma(xale_Espace, 0x1010, (byte) 9);
        luñutu(doxalkat_xëyma.바이트읽기(부모공간, 0x1010) == 7, "biir 시 mbokk_xëyma 부모 격리");
        luñutu(doxalkat_xëyma.바이트읽기(xale_Espace, 0x1010) == 9, "biir 시 mbokk_xëyma xale_xëyma biir");
    }

    private static void 파일과과정시험(xoox xoox_xëyma) {
        byte[] Këmb_xëyma = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        xoox_xëyma.barabu_boolebdenc_yu_ñu_bennal().파일추가("시험", Këmb_xëyma);
        yokkute_xëyma 부모 = xoox_xëyma.첫과정();
        체계호출 호출 = xoox_xëyma.체계호출();
        int 서술자 = 호출.sos(부모, "/시험", 체계호출.ngir_jaŋarek_la_tektalukaay);
        luñutu(서술자 >= 3, "bara_denc sos");

        byte[] 받을곳 = new byte[Këmb_xëyma.length];
        luñutu(호출.읽기(부모, 서술자, 받을곳, 받을곳.length) == Këmb_xëyma.length, "bara_denc 읽기");
        luñutu(Arrays.equals(Këmb_xëyma, 받을곳), "bara_denc Këmb_xëyma");
        luñutu(호출.위치옮기기(부모, 서술자, 0, 체계호출.Wut_Door) == 0, "bara_denc 위치 toxal_xëyma");

        int 복제서술자 = 호출.서술자복제(부모, 서술자);
        luñutu(복제서술자 >= 0, "서술자 복제");
        yokkute_xëyma xale_xëyma = 호출.과정복제(부모);
        luñutu(xale_xëyma.raññeekaay_xëyma() != 부모.raññeekaay_xëyma(), "yokkute_xëyma raññeekaay_xëyma 분리");
        luñutu(xale_xëyma.부모식별자() == 부모.raññeekaay_xëyma(), "부모 yokkute_xëyma raññeekaay_xëyma");
        luñutu(호출.Tej(xale_xëyma, 서술자) == 0 && 부모.파일서술자().열려있음(서술자), "xale_xëyma Tej 격리");

        int 이전끝 = 호출.프로그램끝늘리기(부모, 8192);
        luñutu(이전끝 == 0x06000000, "jëfekaay_f5044b9b 끝 늘리기");
        luñutu(부모.프로그램끝() == 0x06002000, "jëfekaay_f5044b9b 끝 반영");
        luñutu(xale_xëyma.프로그램끝() == 0x06000000, "과정별 jëfekaay_f5044b9b 끝 격리");

        xale_xëyma.Génn_jëfekaay(7);
        luñutu(호출.자식기다리기(부모, xale_xëyma.raññeekaay_xëyma(), false) == (7 << 8), "xale_xëyma Génn_jëfekaay 기다리기");
        luñutu(호출.접근가능("시험", 1) == -13, "def_ndigel sañ_sañ_xëyma 거부");
        luñutu(호출.kiy_jariñoo_internet_raññeekaay() == 0 && 호출.mboolo_raññeekaay() == 0, "사용자와 무리 raññeekaay_xëyma");
        luñutu("/".equals(호출.현재작업목록(2)) && 호출.jalantu_alluwa_ligeey_yi("/") == 0, "현재 작업 dugal_xabaar_lim");
        luñutu(호출.단말인가(부모, 1), "표준 출력 단말");
        luñutu("JMrtOS".equals(호출.체계정보().kureel_tur()), "doxalukaay_xëyma msinfo32_exe");
    }

    private static void 실행파일시험(xoox xoox_xëyma) {
        byte[] mbir = new byte[92];
        mbir[0] = 0x7f;
        mbir[1] = 'E';
        mbir[2] = 'L';
        mbir[3] = 'F';
        mbir[4] = 1;
        mbir[5] = 1;
        biir_lëmm_xëyma(mbir, 24, 0x04001000);
        biir_lëmm_xëyma(mbir, 32, 52);
        짧은정수쓰기(mbir, 46, 40);
        짧은정수쓰기(mbir, 48, 1);
        biir_lëmm_xëyma(mbir, 56, 8);
        biir_lëmm_xëyma(mbir, 60, 2);
        biir_lëmm_xëyma(mbir, 64, 0x04002000);
        biir_lëmm_xëyma(mbir, 72, 64);

        실행파일적재기.nataal nataal_xëyma = new 실행파일적재기().검사(mbir);
        luñutu(nataal_xëyma.Door_dëkkuwaay() == 0x04001000, "ELF daw dëkkuwaay");
        luñutu(nataal_xëyma.구역들().size() == 1 && nataal_xëyma.구역들().get(0).종류() == 8, "ELF 빈 mbir dog_xëyma");
        int 서술자 = xoox_xëyma.체계호출().sos(xoox_xëyma.첫과정(), "시험", 체계호출.ngir_jaŋarek_la_tektalukaay);
        luñutu(xoox_xëyma.체계호출().bara_denc_Saytu_doxinu_ordinateur(xoox_xëyma.첫과정(), 서술자, 2, 1) == 0, "def_ndigel 시 Tej Jekkal_yi");
        luñutu(xoox_xëyma.체계호출().def_ndigel(xoox_xëyma.첫과정(), mbir, new String[] {"시험", "값"}, new String[] {"Làkk=한국어"}) == 0, "ELF def_ndigel nataal_xëyma 적재");
        luñutu(xoox_xëyma.첫과정().실행시작주소() == 0x04001000, "def_ndigel daw dëkkuwaay 반영");
        luñutu(xoox_xëyma.첫과정().실행인자().length == 2 && xoox_xëyma.첫과정().환경값().length == 1, "def_ndigel 인자와 환경");
        luñutu(!xoox_xëyma.첫과정().파일서술자().열려있음(서술자), "def_ndigel 시 서술자 Tej");
        luñutu(xoox_xëyma.쪽관리().바이트읽기(xoox_xëyma.첫과정().dëkkuwaay_Espace(), 0x04002000) == 0, "빈 mbir dog_xëyma 영 doortal");
    }

    private static void 입력시험(xoox xoox_xëyma) {
        xoox_xëyma.입력관리().키누름('가');
        xoox_xëyma.입력관리().쥐이동(3, -2);
        입력사건 첫사건 = xoox_xëyma.입력관리().다음사건();
        입력사건 둘째사건 = xoox_xëyma.입력관리().다음사건();
        luñutu(첫사건.사건종류() == 입력사건.종류.키누름, "자판 xewxew");
        luñutu(둘째사건.첫째값() == 3 && 둘째사건.둘째값() == -2, "쥐 toxal_xëyma xewxew");
    }

    private static void 하드웨어시험(dalal_jumtukaay toftal_xëyma) {
        toftal_xëyma.biir_jël_okte(0x3f8, 0xab);
        luñutu(toftal_xëyma.포트바이트읽기(0x3f8) == 0xab, "jumtukaay_jël D_G 경계");
        luñutu(toftal_xëyma.직렬기록().contains("JMrtOS"), "직렬 làq_Dënk");
    }

    private static void 개입중단과서술자시험() {
        dog_doxalkat doxalkat_xëyma = new dog_doxalkat();
        doxalkat_xëyma.bindu_dugal_xabaar(0x21, Dencukaay_dëkkuwaay -> Dencukaay_dëkkuwaay + 4);
        doxalkat_xëyma.dekkal();
        luñutu(doxalkat_xëyma.Séddale_xëyma(0x21, 100) == 104, "dog Séddale_xëyma");
        doxalkat_xëyma.dakkal();
        luñutu(doxalkat_xëyma.Séddale_xëyma(0x21, 100) == 100, "dog dakkal");

        전역서술자표 서술자표 = new 전역서술자표();
        서술자표.Boole_gi_xayma_bi_teew();
        luñutu(서술자표.조각들().size() == 5, "전역 서술자표");
        ligeey_nekkin_dog ligeey_nekkin = new ligeey_nekkin_dog();
        ligeey_nekkin.특권쌓임공간설정(0x10, 0x800000);
        luñutu(ligeey_nekkin.영번쌓임조각() == 0x10 && ligeey_nekkin.영번쌓임주소() == 0x800000, "작업 nekkin_xëyma dog_xëyma");
    }

    private static void 저장장치와통신망시험() {
        고급기술결합장치 Dencukaay_toftal = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.dog_tolluwaay];
        byte[] 읽은자료 = new byte[고급기술결합장치.dog_tolluwaay];
        쓸자료[17] = 42;
        Dencukaay_toftal.biir(2, 쓸자료);
        Dencukaay_toftal.읽기(2, 읽은자료);
        luñutu(읽은자료[17] == 42, "ATA dog_xëyma 읽고 biir");

        toftal_Doxkatu_diggante_doxalkat toftal = new toftal_Doxkatu_diggante_doxalkat();
        toftal.발견(new toftal_Doxkatu_diggante_doxalkat.toftal_xëyma(0x1022, 0x2000, 0xc000, 11));
        luñutu(toftal.seet_dugal_xabaar(0x1022, 0x2000) != null, "주변 toftal_xëyma seet_dugal_xabaar");

        byte[] Ethernet_kadar = new byte[34];
        Ethernet_kadar[12] = 0x08;
        Ethernet_kadar[13] = 0x00;
        Ethernet_kadar[14] = 0x45;
        luñutu(mbaal_Jumtukaay_yi.이더넷상위규약(Ethernet_kadar) == 0x0800, "이더넷 상위 ay_xëyma");
        luñutu(mbaal_Jumtukaay_yi.상호통신망규약사판인가(Ethernet_kadar, 14), "상호통신망규약 4판");
        luñutu(mbaal_Jumtukaay_yi.인터넷검사합(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 검사합");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        biir_lëmm_xëyma(첫구역, 454, 63);
        biir_lëmm_xëyma(첫구역, 458, 1024);
        luñutu(new 기본분할영역표().읽기(첫구역).size() == 1, "xayma_bi_teew 분할 영역표");

        mbaal_déggoob_wet déggoob_wet_xëyma = new mbaal_déggoob_wet();
        int[] 받은수 = new int[1];
        déggoob_wet_xëyma.bindu_kiy_jariñoo_internet_mbir_sa(7, (mbir, daw, diir_xëyma) -> 받은수[0]++);
        byte[] kadar_àlluwa_tur = new byte[14 + 20 + 8];
        kadar_àlluwa_tur[12] = 0x08;
        kadar_àlluwa_tur[13] = 0x00;
        kadar_àlluwa_tur[14] = 0x45;
        kadar_àlluwa_tur[16] = 0;
        kadar_àlluwa_tur[17] = 28;
        kadar_àlluwa_tur[23] = 17;
        kadar_àlluwa_tur[36] = 0;
        kadar_àlluwa_tur[37] = 7;
        luñutu(déggoob_wet_xëyma.이더넷받기(kadar_àlluwa_tur) && 받은수[0] == 1, "kiy_jariñoo_internet mbir sa_xëyma Séddale_xëyma");
    }

    private static void 화면과시계시험() {
        Araf_laa 화면 = new Araf_laa();
        화면.출력("가나\n다");
        luñutu(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 출력");
        Yeetekaay_ak_Montar Yeetekaay_ak_Montar = new Yeetekaay_ak_Montar(100);
        for (int àlluwa_tur = 0; àlluwa_tur < 10; àlluwa_tur++) {
            Yeetekaay_ak_Montar.틱();
        }
        luñutu(Yeetekaay_ak_Montar.지난밀리초() == 100, "Yeetekaay_ak_Montar 틱 변환");
    }

    private static void biir_lëmm_xëyma(byte[] mbir, int 위치, int xëyma) {
        mbir[위치] = (byte) xëyma;
        mbir[위치 + 1] = (byte) (xëyma >>> 8);
        mbir[위치 + 2] = (byte) (xëyma >>> 16);
        mbir[위치 + 3] = (byte) (xëyma >>> 24);
    }

    private static void 짧은정수쓰기(byte[] mbir, int 위치, int xëyma) {
        mbir[위치] = (byte) xëyma;
        mbir[위치 + 1] = (byte) (xëyma >>> 8);
    }

    private static void luñutu(boolean anam, String tur_253d1510) {
        if (!anam) {
            throw new AssertionError("foo_xëyma: " + tur_253d1510);
        }
        통과수++;
        System.out.println("jox_xëyma: " + tur_253d1510);
    }
}
