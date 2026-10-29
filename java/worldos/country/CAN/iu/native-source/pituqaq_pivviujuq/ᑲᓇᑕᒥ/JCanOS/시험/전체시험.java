// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ᑲᓇᑕᒥ.JCanOS.시험;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import ᑲᓇᑕᒥ.JCanOS.기억공간.puigujjaikkut_aulattiji;
import ᑲᓇᑕᒥ.JCanOS.기억공간.mappigaq_aulattiji;
import ᑲᓇᑕᒥ.JCanOS.입력.입력사건;
import ᑲᓇᑕᒥ.JCanOS.작업.Pivallianiq_atuutilik;
import ᑲᓇᑕᒥ.JCanOS.체계호출.체계호출;
import ᑲᓇᑕᒥ.JCanOS.inikkuvik.실행파일적재기;
import ᑲᓇᑕᒥ.JCanOS.kernel.kernel;
import ᑲᓇᑕᒥ.JCanOS.tuttarvik.호스트하드웨어;
import ᑲᓇᑕᒥ.JCanOS.IRQ.IRQ_aulattiji;
import ᑲᓇᑕᒥ.JCanOS.서술자.전역서술자표;
import ᑲᓇᑕᒥ.JCanOS.저장장치.고급기술결합장치;
import ᑲᓇᑕᒥ.JCanOS.sunakkutaaq_atuutilik.ilagutaq_aqqusiurutiralaaq_aulattiji;
import ᑲᓇᑕᒥ.JCanOS.통신망.통신망도구;
import ᑲᓇᑕᒥ.JCanOS.통신망.Kasuqatigiitsimajut_qaliriit;
import ᑲᓇᑕᒥ.JCanOS.sunakkutaaq_atuutilik.qaujisaut;
import ᑲᓇᑕᒥ.JCanOS.서술자.작업상태구역;
import ᑲᓇᑕᒥ.JCanOS.화면.immikkuuqtuq_saqqijaarli;
import ᑲᓇᑕᒥ.JCanOS.inikkuvik.기본분할영역표;

public final class 전체시험 {
    private static int 통과수;

    private 전체시험() {
    }

    public static void main(String[] 인자) {
        호스트하드웨어 sunakkutaaq_atuutilik = new 호스트하드웨어();
        kernel kernel_atuutilik = new kernel(sunakkutaaq_atuutilik);
        kernel_atuutilik.시작();

        기억공간시험(kernel_atuutilik);
        쪽관리시험(kernel_atuutilik);
        파일과과정시험(kernel_atuutilik);
        실행파일시험(kernel_atuutilik);
        입력시험(kernel_atuutilik);
        하드웨어시험(sunakkutaaq_atuutilik);
        개입중단과서술자시험();
        저장장치와통신망시험();
        화면과시계시험();

        System.out.println("JCanOS 시험 통과: " + 통과수);
    }

    private static void 기억공간시험(kernel kernel_atuutilik) {
        puigujjaikkut_aulattiji aulattiji_atuutilik = kernel_atuutilik.기억공간();
        int 첫주소 = aulattiji_atuutilik.정렬할당(100, 64);
        nalunairli_1aacb54c((첫주소 & 63) == 0, "nalimutirli_atuutilik 할당");
        aulattiji_atuutilik.titiraq_byte_atuutilik(첫주소, (byte) 0x5a);
        nalunairli_1aacb54c(aulattiji_atuutilik.바이트읽기(첫주소) == (byte) 0x5a, "물리 기억공간 읽고 titiraq");
        int 사용전 = aulattiji_atuutilik.사용크기();
        aulattiji_atuutilik.해제(첫주소);
        nalunairli_1aacb54c(aulattiji_atuutilik.사용크기() < 사용전, "기억공간 해제");
    }

    private static void 쪽관리시험(kernel kernel_atuutilik) {
        mappigaq_aulattiji aulattiji_atuutilik = kernel_atuutilik.쪽관리();
        mappigaq_aulattiji.turaarut_SPACEBAR 부모공간 = aulattiji_atuutilik.새주소공간();
        aulattiji_atuutilik.nunannguarurli_mappigaq(부모공간, 0x1000, true);
        aulattiji_atuutilik.titiraq_byte_atuutilik(부모공간, 0x1010, (byte) 7);
        mappigaq_aulattiji.turaarut_SPACEBAR surusiq_SPACEBAR = aulattiji_atuutilik.쓰기시복사복제(부모공간);
        aulattiji_atuutilik.titiraq_byte_atuutilik(surusiq_SPACEBAR, 0x1010, (byte) 9);
        nalunairli_1aacb54c(aulattiji_atuutilik.바이트읽기(부모공간, 0x1010) == 7, "titiraq 시 ijjuarli_atuutilik 부모 격리");
        nalunairli_1aacb54c(aulattiji_atuutilik.바이트읽기(surusiq_SPACEBAR, 0x1010) == 9, "titiraq 시 ijjuarli_atuutilik surusiq_atuutilik titiraq");
    }

    private static void 파일과과정시험(kernel kernel_atuutilik) {
        byte[] Ilulingit_atuutilik = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        kernel_atuutilik.inikkuvik().파일추가("시험", Ilulingit_atuutilik);
        Pivallianiq_atuutilik 부모 = kernel_atuutilik.첫과정();
        체계호출 호출 = kernel_atuutilik.체계호출();
        int 서술자 = 호출.matuirli(부모, "/시험", 체계호출.takugatuinnaq_ujjiqsuut);
        nalunairli_1aacb54c(서술자 >= 3, "ini matuirli");

        byte[] 받을곳 = new byte[Ilulingit_atuutilik.length];
        nalunairli_1aacb54c(호출.읽기(부모, 서술자, 받을곳, 받을곳.length) == Ilulingit_atuutilik.length, "ini 읽기");
        nalunairli_1aacb54c(Arrays.equals(Ilulingit_atuutilik, 받을곳), "ini Ilulingit_atuutilik");
        nalunairli_1aacb54c(호출.위치옮기기(부모, 서술자, 0, 체계호출.Qinirli_pigiarli) == 0, "ini 위치 nuulli_atuutilik");

        int 복제서술자 = 호출.서술자복제(부모, 서술자);
        nalunairli_1aacb54c(복제서술자 >= 0, "서술자 복제");
        Pivallianiq_atuutilik surusiq_atuutilik = 호출.과정복제(부모);
        nalunairli_1aacb54c(surusiq_atuutilik.식별자() != 부모.식별자(), "Pivallianiq_atuutilik 식별자 분리");
        nalunairli_1aacb54c(surusiq_atuutilik.부모식별자() == 부모.식별자(), "부모 Pivallianiq_atuutilik 식별자");
        nalunairli_1aacb54c(호출.matuli(surusiq_atuutilik, 서술자) == 0 && 부모.파일서술자().열려있음(서술자), "surusiq_atuutilik matuli 격리");

        int 이전끝 = 호출.프로그램끝늘리기(부모, 8192);
        nalunairli_1aacb54c(이전끝 == 0x06000000, "pilirijjut_f5044b9b 끝 늘리기");
        nalunairli_1aacb54c(부모.프로그램끝() == 0x06002000, "pilirijjut_f5044b9b 끝 반영");
        nalunairli_1aacb54c(surusiq_atuutilik.프로그램끝() == 0x06000000, "과정별 pilirijjut_f5044b9b 끝 격리");

        surusiq_atuutilik.taima_pilirijjut(7);
        nalunairli_1aacb54c(호출.자식기다리기(부모, surusiq_atuutilik.식별자(), false) == (7 << 8), "surusiq_atuutilik taima_pilirijjut 기다리기");
        nalunairli_1aacb54c(호출.접근가능("시험", 1) == -13, "실행 pijunnaqtittijjut_atuutilik 거부");
        nalunairli_1aacb54c(호출.사용자식별자() == 0 && 호출.무리식별자() == 0, "사용자와 무리 식별자");
        nalunairli_1aacb54c("/".equals(호출.현재작업목록(2)) && 호출.kipulli_piliriatsanut_titiqpalliagat("/") == 0, "현재 작업 Iliniku_Titiqpalliagaq");
        nalunairli_1aacb54c(호출.단말인가(부모, 1), "표준 출력 단말");
        nalunairli_1aacb54c("JCanOS".equals(호출.체계정보().qarasaujaq_atiq()), "qarasaujakkut_aulattijjut_atuutilik msinfo32_exe");
    }

    private static void 실행파일시험(kernel kernel_atuutilik) {
        byte[] titiqqat = new byte[92];
        titiqqat[0] = 0x7f;
        titiqqat[1] = 'E';
        titiqqat[2] = 'L';
        titiqqat[3] = 'F';
        titiqqat[4] = 1;
        titiqqat[5] = 1;
        titiraq_naasaut_atuutilik(titiqqat, 24, 0x04001000);
        titiraq_naasaut_atuutilik(titiqqat, 32, 52);
        짧은정수쓰기(titiqqat, 46, 40);
        짧은정수쓰기(titiqqat, 48, 1);
        titiraq_naasaut_atuutilik(titiqqat, 56, 8);
        titiraq_naasaut_atuutilik(titiqqat, 60, 2);
        titiraq_naasaut_atuutilik(titiqqat, 64, 0x04002000);
        titiraq_naasaut_atuutilik(titiqqat, 72, 64);

        실행파일적재기.ajjinnguaq ajjinnguaq_atuutilik = new 실행파일적재기().검사(titiqqat);
        nalunairli_1aacb54c(ajjinnguaq_atuutilik.pigiarli_turaarut() == 0x04001000, "ELF 시작 turaarut");
        nalunairli_1aacb54c(ajjinnguaq_atuutilik.구역들().size() == 1 && ajjinnguaq_atuutilik.구역들().get(0).종류() == 8, "ELF 빈 titiqqat sukuttia_atuutilik");
        int 서술자 = kernel_atuutilik.체계호출().matuirli(kernel_atuutilik.첫과정(), "시험", 체계호출.takugatuinnaq_ujjiqsuut);
        nalunairli_1aacb54c(kernel_atuutilik.체계호출().ini_aulattivik(kernel_atuutilik.첫과정(), 서술자, 2, 1) == 0, "실행 시 matuli 설정");
        nalunairli_1aacb54c(kernel_atuutilik.체계호출().실행(kernel_atuutilik.첫과정(), titiqqat, new String[] {"시험", "값"}, new String[] {"pilirijjutinut_uqausiq=한국어"}) == 0, "ELF 실행 ajjinnguaq_atuutilik 적재");
        nalunairli_1aacb54c(kernel_atuutilik.첫과정().실행시작주소() == 0x04001000, "실행 시작 turaarut 반영");
        nalunairli_1aacb54c(kernel_atuutilik.첫과정().실행인자().length == 2 && kernel_atuutilik.첫과정().환경값().length == 1, "실행 인자와 환경");
        nalunairli_1aacb54c(!kernel_atuutilik.첫과정().파일서술자().열려있음(서술자), "실행 시 서술자 matuli");
        nalunairli_1aacb54c(kernel_atuutilik.쪽관리().바이트읽기(kernel_atuutilik.첫과정().turaarut_SPACEBAR(), 0x04002000) == 0, "빈 titiqqat sukuttia_atuutilik 영 aturunnaqsili");
    }

    private static void 입력시험(kernel kernel_atuutilik) {
        kernel_atuutilik.입력관리().키누름('가');
        kernel_atuutilik.입력관리().쥐이동(3, -2);
        입력사건 첫사건 = kernel_atuutilik.입력관리().다음사건();
        입력사건 둘째사건 = kernel_atuutilik.입력관리().다음사건();
        nalunairli_1aacb54c(첫사건.사건종류() == 입력사건.종류.키누름, "자판 piniku");
        nalunairli_1aacb54c(둘째사건.첫째값() == 3 && 둘째사건.둘째값() == -2, "쥐 nuulli_atuutilik piniku");
    }

    private static void 하드웨어시험(호스트하드웨어 sunakkutaaq_atuutilik) {
        sunakkutaaq_atuutilik.titiraq_kapputigaq_byte(0x3f8, 0xab);
        nalunairli_1aacb54c(sunakkutaaq_atuutilik.포트바이트읽기(0x3f8) == 0xab, "포트 I_O 경계");
        nalunairli_1aacb54c(sunakkutaaq_atuutilik.직렬기록().contains("JCanOS"), "직렬 papattivik_sanimukutaak");
    }

    private static void 개입중단과서술자시험() {
        IRQ_aulattiji aulattiji_atuutilik = new IRQ_aulattiji();
        aulattiji_atuutilik.등록(0x21, 저장주소 -> 저장주소 + 4);
        aulattiji_atuutilik.ikilli();
        nalunairli_1aacb54c(aulattiji_atuutilik.분배(0x21, 100) == 104, "IRQ 분배");
        aulattiji_atuutilik.비활성화();
        nalunairli_1aacb54c(aulattiji_atuutilik.분배(0x21, 100) == 100, "IRQ 비활성화");

        전역서술자표 서술자표 = new 전역서술자표();
        서술자표.attiqsimaniit_Aturniliuvagiiqtut();
        nalunairli_1aacb54c(서술자표.조각들().size() == 5, "전역 서술자표");
        작업상태구역 sujassaq_qanuilinganiq = new 작업상태구역();
        sujassaq_qanuilinganiq.특권쌓임공간설정(0x10, 0x800000);
        nalunairli_1aacb54c(sujassaq_qanuilinganiq.영번쌓임조각() == 0x10 && sujassaq_qanuilinganiq.영번쌓임주소() == 0x800000, "작업 qanuilinganiq_atuutilik sukuttia_atuutilik");
    }

    private static void 저장장치와통신망시험() {
        고급기술결합장치 저장장치 = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.sukuttia_anininga];
        byte[] 읽은자료 = new byte[고급기술결합장치.sukuttia_anininga];
        쓸자료[17] = 42;
        저장장치.titiraq(2, 쓸자료);
        저장장치.읽기(2, 읽은자료);
        nalunairli_1aacb54c(읽은자료[17] == 42, "ATA sukuttia_atuutilik 읽고 titiraq");

        ilagutaq_aqqusiurutiralaaq_aulattiji ilagutaq = new ilagutaq_aqqusiurutiralaaq_aulattiji();
        ilagutaq.발견(new ilagutaq_aqqusiurutiralaaq_aulattiji.sunakkutaaq_atuutilik(0x1022, 0x2000, 0xc000, 11));
        nalunairli_1aacb54c(ilagutaq.nanili_Iliniku(0x1022, 0x2000) != null, "주변 sunakkutaaq_atuutilik nanili_Iliniku");

        byte[] Ethernet_avalu = new byte[34];
        Ethernet_avalu[12] = 0x08;
        Ethernet_avalu[13] = 0x00;
        Ethernet_avalu[14] = 0x45;
        nalunairli_1aacb54c(통신망도구.이더넷상위규약(Ethernet_avalu) == 0x0800, "이더넷 상위 pijatsaq_atuutilik");
        nalunairli_1aacb54c(통신망도구.상호통신망규약사판인가(Ethernet_avalu, 14), "상호통신망규약 4판");
        nalunairli_1aacb54c(통신망도구.인터넷검사합(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 검사합");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        titiraq_naasaut_atuutilik(첫구역, 454, 63);
        titiraq_naasaut_atuutilik(첫구역, 458, 1024);
        nalunairli_1aacb54c(new 기본분할영역표().읽기(첫구역).size() == 1, "Aturniliuvagiiqtut 분할 영역표");

        Kasuqatigiitsimajut_qaliriit qaliriit_atuutilik = new Kasuqatigiitsimajut_qaliriit();
        int[] 받은수 = new int[1];
        qaliriit_atuutilik.사용자자료단위등록(7, (titiqqat, 시작, takininga_atuutilik) -> 받은수[0]++);
        byte[] avalu_nalunaiqsimavik = new byte[14 + 20 + 8];
        avalu_nalunaiqsimavik[12] = 0x08;
        avalu_nalunaiqsimavik[13] = 0x00;
        avalu_nalunaiqsimavik[14] = 0x45;
        avalu_nalunaiqsimavik[16] = 0;
        avalu_nalunaiqsimavik[17] = 28;
        avalu_nalunaiqsimavik[23] = 17;
        avalu_nalunaiqsimavik[36] = 0;
        avalu_nalunaiqsimavik[37] = 7;
        nalunairli_1aacb54c(qaliriit_atuutilik.이더넷받기(avalu_nalunaiqsimavik) && 받은수[0] == 1, "atuqtuq titiqqat atauttimiittut_atuutilik 분배");
    }

    private static void 화면과시계시험() {
        immikkuuqtuq_saqqijaarli 화면 = new immikkuuqtuq_saqqijaarli();
        화면.출력("가나\n다");
        nalunairli_1aacb54c(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 출력");
        qaujisaut qaujisaut = new qaujisaut(100);
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < 10; nalunaiqsimavik++) {
            qaujisaut.틱();
        }
        nalunairli_1aacb54c(qaujisaut.지난밀리초() == 100, "qaujisaut 틱 변환");
    }

    private static void titiraq_naasaut_atuutilik(byte[] titiqqat, int 위치, int atuutilik) {
        titiqqat[위치] = (byte) atuutilik;
        titiqqat[위치 + 1] = (byte) (atuutilik >>> 8);
        titiqqat[위치 + 2] = (byte) (atuutilik >>> 16);
        titiqqat[위치 + 3] = (byte) (atuutilik >>> 24);
    }

    private static void 짧은정수쓰기(byte[] titiqqat, int 위치, int atuutilik) {
        titiqqat[위치] = (byte) atuutilik;
        titiqqat[위치 + 1] = (byte) (atuutilik >>> 8);
    }

    private static void nalunairli_1aacb54c(boolean qanuinniq, String atiq) {
        if (!qanuinniq) {
            throw new AssertionError("itigaqtuq_atuutilik: " + atiq);
        }
        통과수++;
        System.out.println("통과: " + atiq);
    }
}
