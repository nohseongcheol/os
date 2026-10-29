// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package COL.JColOS.시험;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import COL.JColOS.기억공간.기억공간관리자;
import COL.JColOS.기억공간.쪽관리자;
import COL.JColOS.입력.입력사건;
import COL.JColOS.작업.과정;
import COL.JColOS.체계호출.체계호출;
import COL.JColOS.a_yatawaajiraaya_anaajaalaairua.실행파일적재기;
import COL.JColOS.keetnerü.keetnerü;
import COL.JColOS.epiajatü.호스트하드웨어;
import COL.JColOS.aapiriaaipa.개입중단관리자;
import COL.JColOS.서술자.전역서술자표;
import COL.JColOS.저장장치.고급기술결합장치;
import COL.JColOS.serulaalü_ajutuu.주변장치연결관리자;
import COL.JColOS.통신망.통신망도구;
import COL.JColOS.통신망.kusu_ayaleriaa;
import COL.JColOS.serulaalü_ajutuu.ka_iyaawatia;
import COL.JColOS.서술자.작업상태구역;
import COL.JColOS.화면.jeerü_ee_iyataa;
import COL.JColOS.a_yatawaajiraaya_anaajaalaairua.기본분할영역표;

public final class 전체시험 {
    private static int 통과수;

    private 전체시험() {
    }

    public static void main(String[] 인자) {
        호스트하드웨어 serulaalü_ajutuu = new 호스트하드웨어();
        keetnerü keetnerü_ajutuu = new keetnerü(serulaalü_ajutuu);
        keetnerü_ajutuu.시작();

        기억공간시험(keetnerü_ajutuu);
        쪽관리시험(keetnerü_ajutuu);
        파일과과정시험(keetnerü_ajutuu);
        실행파일시험(keetnerü_ajutuu);
        입력시험(keetnerü_ajutuu);
        하드웨어시험(serulaalü_ajutuu);
        개입중단과서술자시험();
        저장장치와통신망시험();
        화면과시계시험();

        System.out.println("JColOS 시험 통과: " + 통과수);
    }

    private static void 기억공간시험(keetnerü keetnerü_ajutuu) {
        기억공간관리자 관리자 = keetnerü_ajutuu.기억공간();
        int 첫주소 = 관리자.정렬할당(100, 64);
        확인((첫주소 & 63) == 0, "aliniaajaa_ajutuu 할당");
        관리자.ashajaa_waai_ajutuu(첫주소, (byte) 0x5a);
        확인(관리자.바이트읽기(첫주소) == (byte) 0x5a, "물리 기억공간 읽고 ashajaa");
        int 사용전 = 관리자.사용크기();
        관리자.해제(첫주소);
        확인(관리자.사용크기() < 사용전, "기억공간 해제");
    }

    private static void 쪽관리시험(keetnerü keetnerü_ajutuu) {
        쪽관리자 관리자 = keetnerü_ajutuu.쪽관리();
        쪽관리자.ejepüsee_WAARAKATAJÜLÜ 부모공간 = 관리자.새주소공간();
        관리자.쪽연결(부모공간, 0x1000, true);
        관리자.ashajaa_waai_ajutuu(부모공간, 0x1010, (byte) 7);
        쪽관리자.ejepüsee_WAARAKATAJÜLÜ apüshii_achiiruajatü_WAARAKATAJÜLÜ = 관리자.쓰기시복사복제(부모공간);
        관리자.ashajaa_waai_ajutuu(apüshii_achiiruajatü_WAARAKATAJÜLÜ, 0x1010, (byte) 9);
        확인(관리자.바이트읽기(부모공간, 0x1010) == 7, "ashajaa 시 ashataa_ajutuu 부모 격리");
        확인(관리자.바이트읽기(apüshii_achiiruajatü_WAARAKATAJÜLÜ, 0x1010) == 9, "ashajaa 시 ashataa_ajutuu apüshii_achiiruajatü_ajutuu ashajaa");
    }

    private static void 파일과과정시험(keetnerü keetnerü_ajutuu) {
        byte[] alu_ujatüü_ajutuu = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        keetnerü_ajutuu.a_yatawaajiraaya_anaajaalaairua().파일추가("시험", alu_ujatüü_ajutuu);
        과정 부모 = keetnerü_ajutuu.첫과정();
        체계호출 호출 = keetnerü_ajutuu.체계호출();
        int 서술자 = 호출.열기(부모, "/시험", 체계호출.읽기만);
        확인(서술자 >= 3, "anaajaalaa 열기");

        byte[] 받을곳 = new byte[alu_ujatüü_ajutuu.length];
        확인(호출.읽기(부모, 서술자, 받을곳, 받을곳.length) == alu_ujatüü_ajutuu.length, "anaajaalaa 읽기");
        확인(Arrays.equals(alu_ujatüü_ajutuu, 받을곳), "anaajaalaa alu_ujatüü_ajutuu");
        확인(호출.위치옮기기(부모, 서술자, 0, 체계호출.Achajaaya_achuwalaa) == 0, "anaajaalaa 위치 이동");

        int 복제서술자 = 호출.서술자복제(부모, 서술자);
        확인(복제서술자 >= 0, "서술자 복제");
        과정 apüshii_achiiruajatü_ajutuu = 호출.과정복제(부모);
        확인(apüshii_achiiruajatü_ajutuu.식별자() != 부모.식별자(), "과정 식별자 분리");
        확인(apüshii_achiiruajatü_ajutuu.부모식별자() == 부모.식별자(), "부모 과정 식별자");
        확인(호출.asürülaa(apüshii_achiiruajatü_ajutuu, 서술자) == 0 && 부모.파일서술자().열려있음(서술자), "apüshii_achiiruajatü_ajutuu asürülaa 격리");

        int 이전끝 = 호출.프로그램끝늘리기(부모, 8192);
        확인(이전끝 == 0x06000000, "akumajiaa_f5044b9b 끝 늘리기");
        확인(부모.프로그램끝() == 0x06002000, "akumajiaa_f5044b9b 끝 반영");
        확인(apüshii_achiiruajatü_ajutuu.프로그램끝() == 0x06000000, "과정별 akumajiaa_f5044b9b 끝 격리");

        apüshii_achiiruajatü_ajutuu.aju_itaa_akumajiaa(7);
        확인(호출.자식기다리기(부모, apüshii_achiiruajatü_ajutuu.식별자(), false) == (7 << 8), "apüshii_achiiruajatü_ajutuu aju_itaa_akumajiaa 기다리기");
        확인(호출.접근가능("시험", 1) == -13, "실행 권한 거부");
        확인(호출.사용자식별자() == 0 && 호출.무리식별자() == 0, "사용자와 무리 식별자");
        확인("/".equals(호출.현재작업목록(2)) && 호출.작업목록바꾸기("/") == 0, "현재 작업 목록");
        확인(호출.단말인가(부모, 1), "표준 출력 단말");
        확인("JColOS".equals(호출.체계정보().체계이름()), "a_yatawajiraaya_a_laülaasü_ajutuu 정보");
    }

    private static void 실행파일시험(keetnerü keetnerü_ajutuu) {
        byte[] atijaaya = new byte[92];
        atijaaya[0] = 0x7f;
        atijaaya[1] = 'E';
        atijaaya[2] = 'L';
        atijaaya[3] = 'F';
        atijaaya[4] = 1;
        atijaaya[5] = 1;
        ashajaa_waneepiasü_ajutuu(atijaaya, 24, 0x04001000);
        ashajaa_waneepiasü_ajutuu(atijaaya, 32, 52);
        짧은정수쓰기(atijaaya, 46, 40);
        짧은정수쓰기(atijaaya, 48, 1);
        ashajaa_waneepiasü_ajutuu(atijaaya, 56, 8);
        ashajaa_waneepiasü_ajutuu(atijaaya, 60, 2);
        ashajaa_waneepiasü_ajutuu(atijaaya, 64, 0x04002000);
        ashajaa_waneepiasü_ajutuu(atijaaya, 72, 64);

        실행파일적재기.ayaakuaa ayaakuaa_ajutuu = new 실행파일적재기().검사(atijaaya);
        확인(ayaakuaa_ajutuu.achuwalaa_ejepüsee() == 0x04001000, "ELF 시작 ejepüsee");
        확인(ayaakuaa_ajutuu.구역들().size() == 1 && ayaakuaa_ajutuu.구역들().get(0).종류() == 8, "ELF 빈 atijaaya alüjalee_ajutuu");
        int 서술자 = keetnerü_ajutuu.체계호출().열기(keetnerü_ajutuu.첫과정(), "시험", 체계호출.읽기만);
        확인(keetnerü_ajutuu.체계호출().anaajaalaa_aa_inmajia(keetnerü_ajutuu.첫과정(), 서술자, 2, 1) == 0, "실행 시 asürülaa 설정");
        확인(keetnerü_ajutuu.체계호출().실행(keetnerü_ajutuu.첫과정(), atijaaya, new String[] {"시험", "값"}, new String[] {"anüikii_komputatooralujatü=한국어"}) == 0, "ELF 실행 ayaakuaa_ajutuu 적재");
        확인(keetnerü_ajutuu.첫과정().실행시작주소() == 0x04001000, "실행 시작 ejepüsee 반영");
        확인(keetnerü_ajutuu.첫과정().실행인자().length == 2 && keetnerü_ajutuu.첫과정().환경값().length == 1, "실행 인자와 환경");
        확인(!keetnerü_ajutuu.첫과정().파일서술자().열려있음(서술자), "실행 시 서술자 asürülaa");
        확인(keetnerü_ajutuu.쪽관리().바이트읽기(keetnerü_ajutuu.첫과정().ejepüsee_WAARAKATAJÜLÜ(), 0x04002000) == 0, "빈 atijaaya alüjalee_ajutuu 영 anaajaa");
    }

    private static void 입력시험(keetnerü keetnerü_ajutuu) {
        keetnerü_ajutuu.입력관리().키누름('가');
        keetnerü_ajutuu.입력관리().쥐이동(3, -2);
        입력사건 첫사건 = keetnerü_ajutuu.입력관리().다음사건();
        입력사건 둘째사건 = keetnerü_ajutuu.입력관리().다음사건();
        확인(첫사건.사건종류() == 입력사건.종류.키누름, "자판 kasachiki");
        확인(둘째사건.첫째값() == 3 && 둘째사건.둘째값() == -2, "쥐 이동 kasachiki");
    }

    private static void 하드웨어시험(호스트하드웨어 serulaalü_ajutuu) {
        serulaalü_ajutuu.ashajaa_outtülee_waai(0x3f8, 0xab);
        확인(serulaalü_ajutuu.포트바이트읽기(0x3f8) == 0xab, "포트 E_A 경계");
        확인(serulaalü_ajutuu.직렬기록().contains("JColOS"), "직렬 aa_innachikimaajatü_aparatsee");
    }

    private static void 개입중단과서술자시험() {
        개입중단관리자 관리자 = new 개입중단관리자();
        관리자.등록(0x21, 저장주소 -> 저장주소 + 4);
        관리자.활성화();
        확인(관리자.분배(0x21, 100) == 104, "aapiriaaipa 분배");
        관리자.비활성화();
        확인(관리자.분배(0x21, 100) == 100, "aapiriaaipa 비활성화");

        전역서술자표 서술자표 = new 전역서술자표();
        서술자표.기본값설정();
        확인(서술자표.조각들().size() == 5, "전역 서술자표");
        작업상태구역 aa_innajatü_jamakua_iparülein = new 작업상태구역();
        aa_innajatü_jamakua_iparülein.특권쌓임공간설정(0x10, 0x800000);
        확인(aa_innajatü_jamakua_iparülein.영번쌓임조각() == 0x10 && aa_innajatü_jamakua_iparülein.영번쌓임주소() == 0x800000, "작업 jamakua_iparülein_ajutuu alüjalee_ajutuu");
    }

    private static void 저장장치와통신망시험() {
        고급기술결합장치 저장장치 = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.구역크기];
        byte[] 읽은자료 = new byte[고급기술결합장치.구역크기];
        쓸자료[17] = 42;
        저장장치.ashajaa(2, 쓸자료);
        저장장치.읽기(2, 읽은자료);
        확인(읽은자료[17] == 42, "ATA alüjalee_ajutuu 읽고 ashajaa");

        주변장치연결관리자 korolowala_ata = new 주변장치연결관리자();
        korolowala_ata.발견(new 주변장치연결관리자.serulaalü_ajutuu(0x1022, 0x2000, 0xc000, 11));
        확인(korolowala_ata.찾기(0x1022, 0x2000) != null, "주변 serulaalü_ajutuu 찾기");

        byte[] Ethernet_otpünaa = new byte[34];
        Ethernet_otpünaa[12] = 0x08;
        Ethernet_otpünaa[13] = 0x00;
        Ethernet_otpünaa[14] = 0x45;
        확인(통신망도구.이더넷상위규약(Ethernet_otpünaa) == 0x0800, "이더넷 상위 achikii_ajutuu");
        확인(통신망도구.상호통신망규약사판인가(Ethernet_otpünaa, 14), "상호통신망규약 4판");
        확인(통신망도구.인터넷검사합(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 검사합");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        ashajaa_waneepiasü_ajutuu(첫구역, 454, 63);
        ashajaa_waneepiasü_ajutuu(첫구역, 458, 1024);
        확인(new 기본분할영역표().읽기(첫구역).size() == 1, "ajutuu_aneekuushitüjülia 분할 영역표");

        kusu_ayaleriaa ayaleriaa_ajutuu = new kusu_ayaleriaa();
        int[] 받은수 = new int[1];
        ayaleriaa_ajutuu.사용자자료단위등록(7, (atijaaya, 시작, akaliaa_ajutuu) -> 받은수[0]++);
        byte[] otpünaa_ee_iyatialujuna = new byte[14 + 20 + 8];
        otpünaa_ee_iyatialujuna[12] = 0x08;
        otpünaa_ee_iyatialujuna[13] = 0x00;
        otpünaa_ee_iyatialujuna[14] = 0x45;
        otpünaa_ee_iyatialujuna[16] = 0;
        otpünaa_ee_iyatialujuna[17] = 28;
        otpünaa_ee_iyatialujuna[23] = 17;
        otpünaa_ee_iyatialujuna[36] = 0;
        otpünaa_ee_iyatialujuna[37] = 7;
        확인(ayaleriaa_ajutuu.이더넷받기(otpünaa_ee_iyatialujuna) && 받은수[0] == 1, "ka_yataayakalü atijaaya 단위 분배");
    }

    private static void 화면과시계시험() {
        jeerü_ee_iyataa 화면 = new jeerü_ee_iyataa();
        화면.출력("가나\n다");
        확인(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 출력");
        ka_iyaawatia ka_iyaawatia = new ka_iyaawatia(100);
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < 10; ee_iyatialujuna++) {
            ka_iyaawatia.틱();
        }
        확인(ka_iyaawatia.지난밀리초() == 100, "ka_iyaawatia 틱 변환");
    }

    private static void ashajaa_waneepiasü_ajutuu(byte[] atijaaya, int 위치, int ajutuu) {
        atijaaya[위치] = (byte) ajutuu;
        atijaaya[위치 + 1] = (byte) (ajutuu >>> 8);
        atijaaya[위치 + 2] = (byte) (ajutuu >>> 16);
        atijaaya[위치 + 3] = (byte) (ajutuu >>> 24);
    }

    private static void 짧은정수쓰기(byte[] atijaaya, int 위치, int ajutuu) {
        atijaaya[위치] = (byte) ajutuu;
        atijaaya[위치 + 1] = (byte) (ajutuu >>> 8);
    }

    private static void 확인(boolean mülein, String 이름) {
        if (!mülein) {
            throw new AssertionError("ajachitia_ajutuu: " + 이름);
        }
        통과수++;
        System.out.println("통과: " + 이름);
    }
}
