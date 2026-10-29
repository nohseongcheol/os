// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Seraa_liyon.JSleOS.시험;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Seraa_liyon.JSleOS.기억공간.teskordu_kisnoowo;
import Seraa_liyon.JSleOS.기억공간.hello_kisnoowo;
import Seraa_liyon.JSleOS.입력.입력사건;
import Seraa_liyon.JSleOS.작업.Yuɓɓo_golle_njaru;
import Seraa_liyon.JSleOS.체계호출.체계호출;
import Seraa_liyon.JSleOS.yuɓɓo_piille.실행파일적재기;
import Seraa_liyon.JSleOS.aaluude.aaluude;
import Seraa_liyon.JSleOS.njaatigi.호스트하드웨어;
import Seraa_liyon.JSleOS.telɓuru.telɓuru_kisnoowo;
import Seraa_liyon.JSleOS.서술자.전역서술자표;
import Seraa_liyon.JSleOS.저장장치.고급기술결합장치;
import Seraa_liyon.JSleOS.kaɓirgal_njaru.gollirgal_biis_kisnoowo;
import Seraa_liyon.JSleOS.통신망.통신망도구;
import Seraa_liyon.JSleOS.통신망.laylaytol_tekkeendi;
import Seraa_liyon.JSleOS.kaɓirgal_njaru.montor;
import Seraa_liyon.JSleOS.서술자.작업상태구역;
import Seraa_liyon.JSleOS.화면.alkulal_jaytino;
import Seraa_liyon.JSleOS.yuɓɓo_piille.기본분할영역표;

public final class 전체시험 {
    private static int 통과수;

    private 전체시험() {
    }

    public static void main(String[] 인자) {
        호스트하드웨어 kaɓirgal_njaru = new 호스트하드웨어();
        aaluude aaluude_njaru = new aaluude(kaɓirgal_njaru);
        aaluude_njaru.huutoraade();

        기억공간시험(aaluude_njaru);
        쪽관리시험(aaluude_njaru);
        파일과과정시험(aaluude_njaru);
        실행파일시험(aaluude_njaru);
        입력시험(aaluude_njaru);
        하드웨어시험(kaɓirgal_njaru);
        개입중단과서술자시험();
        저장장치와통신망시험();
        화면과시계시험();

        System.out.println("JSleOS 시험 통과: " + 통과수);
    }

    private static void 기억공간시험(aaluude aaluude_njaru) {
        teskordu_kisnoowo kisnoowo_njaru = aaluude_njaru.기억공간();
        int 첫주소 = kisnoowo_njaru.정렬할당(100, 64);
        ƴeewtaade((첫주소 & 63) == 0, "fonndude_njaru 할당");
        kisnoowo_njaru.winndude_oktee_njaru(첫주소, (byte) 0x5a);
        ƴeewtaade(kisnoowo_njaru.바이트읽기(첫주소) == (byte) 0x5a, "물리 기억공간 읽고 winndude");
        int 사용전 = kisnoowo_njaru.사용크기();
        kisnoowo_njaru.해제(첫주소);
        ƴeewtaade(kisnoowo_njaru.사용크기() < 사용전, "기억공간 해제");
    }

    private static void 쪽관리시험(aaluude aaluude_njaru) {
        hello_kisnoowo kisnoowo_njaru = aaluude_njaru.쪽관리();
        hello_kisnoowo.ñiiɓirde_wonorde 부모공간 = kisnoowo_njaru.새주소공간();
        kisnoowo_njaru.쪽연결(부모공간, 0x1000, true);
        kisnoowo_njaru.winndude_oktee_njaru(부모공간, 0x1010, (byte) 7);
        hello_kisnoowo.ñiiɓirde_wonorde 자식공간 = kisnoowo_njaru.쓰기시복사복제(부모공간);
        kisnoowo_njaru.winndude_oktee_njaru(자식공간, 0x1010, (byte) 9);
        ƴeewtaade(kisnoowo_njaru.바이트읽기(부모공간, 0x1010) == 7, "winndude 시 waanjitaade_njaru 부모 격리");
        ƴeewtaade(kisnoowo_njaru.바이트읽기(자식공간, 0x1010) == 9, "winndude 시 waanjitaade_njaru 자식 winndude");
    }

    private static void 파일과과정시험(aaluude aaluude_njaru) {
        byte[] loowdi_njaru = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        aaluude_njaru.yuɓɓo_piille().파일추가("시험", loowdi_njaru);
        Yuɓɓo_golle_njaru 부모 = aaluude_njaru.첫과정();
        체계호출 호출 = aaluude_njaru.체계호출();
        int 서술자 = 호출.udditde(부모, "/시험", 체계호출.janngotooɗo_tan_maantaade);
        ƴeewtaade(서술자 >= 3, "fiilde udditde");

        byte[] 받을곳 = new byte[loowdi_njaru.length];
        ƴeewtaade(호출.읽기(부모, 서술자, 받을곳, 받을곳.length) == loowdi_njaru.length, "fiilde 읽기");
        ƴeewtaade(Arrays.equals(loowdi_njaru, 받을곳), "fiilde loowdi_njaru");
        ƴeewtaade(호출.위치옮기기(부모, 서술자, 0, 체계호출.njiilawu_huɓɓude) == 0, "fiilde 위치 dirtinde_njaru");

        int 복제서술자 = 호출.서술자복제(부모, 서술자);
        ƴeewtaade(복제서술자 >= 0, "서술자 복제");
        Yuɓɓo_golle_njaru 자식 = 호출.과정복제(부모);
        ƴeewtaade(자식.식별자() != 부모.식별자(), "Yuɓɓo_golle_njaru 식별자 분리");
        ƴeewtaade(자식.부모식별자() == 부모.식별자(), "부모 Yuɓɓo_golle_njaru 식별자");
        ƴeewtaade(호출.uddude(자식, 서술자) == 0 && 부모.파일서술자().열려있음(서술자), "자식 uddude 격리");

        int 이전끝 = 호출.프로그램끝늘리기(부모, 8192);
        ƴeewtaade(이전끝 == 0x06000000, "tafirde_f5044b9b 끝 늘리기");
        ƴeewtaade(부모.프로그램끝() == 0x06002000, "tafirde_f5044b9b 끝 반영");
        ƴeewtaade(자식.프로그램끝() == 0x06000000, "과정별 tafirde_f5044b9b 끝 격리");

        자식.yaltude_tafirde(7);
        ƴeewtaade(호출.자식기다리기(부모, 자식.식별자(), false) == (7 << 8), "자식 yaltude_tafirde 기다리기");
        ƴeewtaade(호출.접근가능("시험", 1) == -13, "실행 권한 거부");
        ƴeewtaade(호출.사용자식별자() == 0 && 호출.무리식별자() == 0, "사용자와 무리 식별자");
        ƴeewtaade("/".equals(호출.현재작업목록(2)) && 호출.waylude_golle_Doggol("/") == 0, "현재 작업 naatnugol_Doggol");
        ƴeewtaade(호출.단말인가(부모, 1), "표준 출력 단말");
        ƴeewtaade("JSleOS".equals(호출.체계정보().yuɓɓo_innde()), "yuɓɓo_kurdinɗo_njaru msinfo32_exe");
    }

    private static void 실행파일시험(aaluude aaluude_njaru) {
        byte[] keɓe = new byte[92];
        keɓe[0] = 0x7f;
        keɓe[1] = 'E';
        keɓe[2] = 'L';
        keɓe[3] = 'F';
        keɓe[4] = 1;
        keɓe[5] = 1;
        정수쓰기(keɓe, 24, 0x04001000);
        정수쓰기(keɓe, 32, 52);
        짧은정수쓰기(keɓe, 46, 40);
        짧은정수쓰기(keɓe, 48, 1);
        정수쓰기(keɓe, 56, 8);
        정수쓰기(keɓe, 60, 2);
        정수쓰기(keɓe, 64, 0x04002000);
        정수쓰기(keɓe, 72, 64);

        실행파일적재기.natal natal_njaru = new 실행파일적재기().검사(keɓe);
        ƴeewtaade(natal_njaru.huɓɓude_ñiiɓirde() == 0x04001000, "ELF huutoraade ñiiɓirde");
        ƴeewtaade(natal_njaru.구역들().size() == 1 && natal_njaru.구역들().get(0).종류() == 8, "ELF 빈 keɓe taƴre_njaru");
        int 서술자 = aaluude_njaru.체계호출().udditde(aaluude_njaru.첫과정(), "시험", 체계호출.janngotooɗo_tan_maantaade);
        ƴeewtaade(aaluude_njaru.체계호출().fiilde_yuurnitorde(aaluude_njaru.첫과정(), 서술자, 2, 1) == 0, "실행 시 uddude 설정");
        ƴeewtaade(aaluude_njaru.체계호출().실행(aaluude_njaru.첫과정(), keɓe, new String[] {"시험", "값"}, new String[] {"언어=한국어"}) == 0, "ELF 실행 natal_njaru 적재");
        ƴeewtaade(aaluude_njaru.첫과정().실행시작주소() == 0x04001000, "실행 huutoraade ñiiɓirde 반영");
        ƴeewtaade(aaluude_njaru.첫과정().실행인자().length == 2 && aaluude_njaru.첫과정().환경값().length == 1, "실행 인자와 환경");
        ƴeewtaade(!aaluude_njaru.첫과정().파일서술자().열려있음(서술자), "실행 시 서술자 uddude");
        ƴeewtaade(aaluude_njaru.쪽관리().바이트읽기(aaluude_njaru.첫과정().ñiiɓirde_wonorde(), 0x04002000) == 0, "빈 keɓe taƴre_njaru 영 ɓamtinde");
    }

    private static void 입력시험(aaluude aaluude_njaru) {
        aaluude_njaru.입력관리().키누름('가');
        aaluude_njaru.입력관리().쥐이동(3, -2);
        입력사건 첫사건 = aaluude_njaru.입력관리().다음사건();
        입력사건 둘째사건 = aaluude_njaru.입력관리().다음사건();
        ƴeewtaade(첫사건.사건종류() == 입력사건.종류.키누름, "자판 saɗteende");
        ƴeewtaade(둘째사건.첫째값() == 3 && 둘째사건.둘째값() == -2, "쥐 dirtinde_njaru saɗteende");
    }

    private static void 하드웨어시험(호스트하드웨어 kaɓirgal_njaru) {
        kaɓirgal_njaru.winndude_poor_oktee(0x3f8, 0xab);
        ƴeewtaade(kaɓirgal_njaru.포트바이트읽기(0x3f8) == 0xab, "포트 I_O 경계");
        ƴeewtaade(kaɓirgal_njaru.직렬기록().contains("JSleOS"), "직렬 suurnal_winndande");
    }

    private static void 개입중단과서술자시험() {
        telɓuru_kisnoowo kisnoowo_njaru = new telɓuru_kisnoowo();
        kisnoowo_njaru.등록(0x21, 저장주소 -> 저장주소 + 4);
        kisnoowo_njaru.tonngitde();
        ƴeewtaade(kisnoowo_njaru.분배(0x21, 100) == 104, "telɓuru 분배");
        kisnoowo_njaru.비활성화();
        ƴeewtaade(kisnoowo_njaru.분배(0x21, 100) == 100, "telɓuru 비활성화");

        전역서술자표 서술자표 = new 전역서술자표();
        서술자표.기본값설정();
        ƴeewtaade(서술자표.조각들().size() == 5, "전역 서술자표");
        작업상태구역 golle_ngonka = new 작업상태구역();
        golle_ngonka.특권쌓임공간설정(0x10, 0x800000);
        ƴeewtaade(golle_ngonka.영번쌓임조각() == 0x10 && golle_ngonka.영번쌓임주소() == 0x800000, "작업 ngonka_njaru taƴre_njaru");
    }

    private static void 저장장치와통신망시험() {
        고급기술결합장치 저장장치 = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.taƴre_waylude_etannde];
        byte[] 읽은자료 = new byte[고급기술결합장치.taƴre_waylude_etannde];
        쓸자료[17] = 42;
        저장장치.winndude(2, 쓸자료);
        저장장치.읽기(2, 읽은자료);
        ƴeewtaade(읽은자료[17] == 42, "ATA taƴre_njaru 읽고 winndude");

        gollirgal_biis_kisnoowo gollirgal = new gollirgal_biis_kisnoowo();
        gollirgal.발견(new gollirgal_biis_kisnoowo.kaɓirgal_njaru(0x1022, 0x2000, 0xc000, 11));
        ƴeewtaade(gollirgal.yiylaade_naatnugol(0x1022, 0x2000) != null, "주변 kaɓirgal_njaru yiylaade_naatnugol");

        byte[] Ethernet_taƴtinnde = new byte[34];
        Ethernet_taƴtinnde[12] = 0x08;
        Ethernet_taƴtinnde[13] = 0x00;
        Ethernet_taƴtinnde[14] = 0x45;
        ƴeewtaade(통신망도구.이더넷상위규약(Ethernet_taƴtinnde) == 0x0800, "이더넷 상위 haaju_njaru");
        ƴeewtaade(통신망도구.상호통신망규약사판인가(Ethernet_taƴtinnde, 14), "상호통신망규약 4판");
        ƴeewtaade(통신망도구.인터넷검사합(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 검사합");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        정수쓰기(첫구역, 454, 63);
        정수쓰기(첫구역, 458, 1024);
        ƴeewtaade(new 기본분할영역표().읽기(첫구역).size() == 1, "lasli_njaru 분할 영역표");

        laylaytol_tekkeendi tekkeendi_njaru = new laylaytol_tekkeendi();
        int[] 받은수 = new int[1];
        tekkeendi_njaru.사용자자료단위등록(7, (keɓe, huutoraade, njuuteendi_njaru) -> 받은수[0]++);
        byte[] taƴtinnde_joopirdu = new byte[14 + 20 + 8];
        taƴtinnde_joopirdu[12] = 0x08;
        taƴtinnde_joopirdu[13] = 0x00;
        taƴtinnde_joopirdu[14] = 0x45;
        taƴtinnde_joopirdu[16] = 0;
        taƴtinnde_joopirdu[17] = 28;
        taƴtinnde_joopirdu[23] = 17;
        taƴtinnde_joopirdu[36] = 0;
        taƴtinnde_joopirdu[37] = 7;
        ƴeewtaade(tekkeendi_njaru.이더넷받기(taƴtinnde_joopirdu) && 받은수[0] == 1, "kuutoro keɓe ngootoñ_njaru 분배");
    }

    private static void 화면과시계시험() {
        alkulal_jaytino 화면 = new alkulal_jaytino();
        화면.출력("가나\n다");
        ƴeewtaade(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 출력");
        montor montor = new montor(100);
        for (int joopirdu = 0; joopirdu < 10; joopirdu++) {
            montor.틱();
        }
        ƴeewtaade(montor.지난밀리초() == 100, "montor 틱 변환");
    }

    private static void 정수쓰기(byte[] keɓe, int 위치, int njaru) {
        keɓe[위치] = (byte) njaru;
        keɓe[위치 + 1] = (byte) (njaru >>> 8);
        keɓe[위치 + 2] = (byte) (njaru >>> 16);
        keɓe[위치 + 3] = (byte) (njaru >>> 24);
    }

    private static void 짧은정수쓰기(byte[] keɓe, int 위치, int njaru) {
        keɓe[위치] = (byte) njaru;
        keɓe[위치 + 1] = (byte) (njaru >>> 8);
    }

    private static void ƴeewtaade(boolean ngonka, String innde) {
        if (!ngonka) {
            throw new AssertionError("ella_njaru: " + innde);
        }
        통과수++;
        System.out.println("통과: " + innde);
    }
}
