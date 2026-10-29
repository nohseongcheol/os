// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Bẹ̀nẹ̀.JBenOS.시험;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Bẹ̀nẹ̀.JBenOS.기억공간.ibi_ìpamọ́_alákòóso;
import Bẹ̀nẹ̀.JBenOS.기억공간.ojú_ìwé_alákòóso;
import Bẹ̀nẹ̀.JBenOS.입력.입력사건;
import Bẹ̀nẹ̀.JBenOS.작업.Ìlànà_iye;
import Bẹ̀nẹ̀.JBenOS.체계호출.체계호출;
import Bẹ̀nẹ̀.JBenOS.ìlànà_ètò_fáìlì.실행파일적재기;
import Bẹ̀nẹ̀.JBenOS.kánẹ́ẹ̀lì.kánẹ́ẹ̀lì;
import Bẹ̀nẹ̀.JBenOS.olùpèsè.olùpèsè_ohun_èlò_alárídìmú;
import Bẹ̀nẹ̀.JBenOS.IRQ.IRQ_alákòóso;
import Bẹ̀nẹ̀.JBenOS.서술자.전역서술자표;
import Bẹ̀nẹ̀.JBenOS.Ibi_ìpamọ́_ohun_èlò.고급기술결합장치;
import Bẹ̀nẹ̀.JBenOS.ohun_èlò_iye.èròjà_ọ̀nà_agbédátà_alákòóso;
import Bẹ̀nẹ̀.JBenOS.Alásopọ̀_kójọ.Alásopọ̀_Àwọn_irinṣẹ́;
import Bẹ̀nẹ̀.JBenOS.Alásopọ̀_kójọ.Alásopọ̀_ìpele;
import Bẹ̀nẹ̀.JBenOS.ohun_èlò_iye.aago;
import Bẹ̀nẹ̀.JBenOS.서술자.iṣẹ́_ipò_abala;
import Bẹ̀nẹ̀.JBenOS.화면.ẹyọ_ọ̀rọ̀_ṣàfihàn;
import Bẹ̀nẹ̀.JBenOS.ìlànà_ètò_fáìlì.기본분할영역표;

public final class 전체시험 {
    private static int 통과수;

    private 전체시험() {
    }

    public static void main(String[] 인자) {
        olùpèsè_ohun_èlò_alárídìmú ohun_èlò_iye = new olùpèsè_ohun_èlò_alárídìmú();
        kánẹ́ẹ̀lì kánẹ́ẹ̀lì_iye = new kánẹ́ẹ̀lì(ohun_èlò_iye);
        kánẹ́ẹ̀lì_iye.Rọ́ọ̀nù();

        기억공간시험(kánẹ́ẹ̀lì_iye);
        쪽관리시험(kánẹ́ẹ̀lì_iye);
        파일과과정시험(kánẹ́ẹ̀lì_iye);
        실행파일시험(kánẹ́ẹ̀lì_iye);
        입력시험(kánẹ́ẹ̀lì_iye);
        하드웨어시험(ohun_èlò_iye);
        개입중단과서술자시험();
        저장장치와통신망시험();
        화면과시계시험();

        System.out.println("JBenOS 시험 fí_dátà_ránṣẹ́_iye: " + 통과수);
    }

    private static void 기억공간시험(kánẹ́ẹ̀lì kánẹ́ẹ̀lì_iye) {
        ibi_ìpamọ́_alákòóso alákòóso_iye = kánẹ́ẹ̀lì_iye.기억공간();
        int 첫주소 = alákòóso_iye.정렬할당(100, 64);
        ridájú((첫주소 & 63) == 0, "mu_dọ́gba_iye pín_Ibi_ìpamọ́");
        alákòóso_iye.kọ_báìtì_iye(첫주소, (byte) 0x5a);
        ridájú(alákòóso_iye.바이트읽기(첫주소) == (byte) 0x5a, "물리 기억공간 읽고 Kọ");
        int 사용전 = alákòóso_iye.사용크기();
        alákòóso_iye.dápadà_Ibi_ìpamọ́(첫주소);
        ridájú(alákòóso_iye.사용크기() < 사용전, "기억공간 dápadà_Ibi_ìpamọ́");
    }

    private static void 쪽관리시험(kánẹ́ẹ̀lì kánẹ́ẹ̀lì_iye) {
        ojú_ìwé_alákòóso alákòóso_iye = kánẹ́ẹ̀lì_iye.쪽관리();
        ojú_ìwé_alákòóso.àdírẹ́ẹ̀sì_àlàfo 부모공간 = alákòóso_iye.새주소공간();
        alákòóso_iye.máàpù_ojú_ìwé(부모공간, 0x1000, true);
        alákòóso_iye.kọ_báìtì_iye(부모공간, 0x1010, (byte) 7);
        ojú_ìwé_alákòóso.àdírẹ́ẹ̀sì_àlàfo ọmọ_àlàfo = alákòóso_iye.쓰기시복사복제(부모공간);
        alákòóso_iye.kọ_báìtì_iye(ọmọ_àlàfo, 0x1010, (byte) 9);
        ridájú(alákòóso_iye.바이트읽기(부모공간, 0x1010) == 7, "Kọ 시 ṣẹ̀dà_iye 부모 격리");
        ridájú(alákòóso_iye.바이트읽기(ọmọ_àlàfo, 0x1010) == 9, "Kọ 시 ṣẹ̀dà_iye ọmọ_iye Kọ");
    }

    private static void 파일과과정시험(kánẹ́ẹ̀lì kánẹ́ẹ̀lì_iye) {
        byte[] Àkóónú_iye = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        kánẹ́ẹ̀lì_iye.ìlànà_ètò_fáìlì().파일추가("시험", Àkóónú_iye);
        Ìlànà_iye 부모 = kánẹ́ẹ̀lì_iye.첫과정();
        체계호출 호출 = kánẹ́ẹ̀lì_iye.체계호출();
        int 서술자 = 호출.Ṣi(부모, "/시험", 체계호출.kàn_kàá_ipe_àkíyèsí_sí);
        ridájú(서술자 >= 3, "Fáìlì Ṣi");

        byte[] 받을곳 = new byte[Àkóónú_iye.length];
        ridájú(호출.Kàá(부모, 서술자, 받을곳, 받을곳.length) == Àkóónú_iye.length, "Fáìlì Kàá");
        ridájú(Arrays.equals(Àkóónú_iye, 받을곳), "Fáìlì Àkóónú_iye");
        ridájú(호출.위치옮기기(부모, 서술자, 0, 체계호출.wákiri_bẹ̀rẹ̀) == 0, "Fáìlì 위치 gbé_iye");

        int 복제서술자 = 호출.서술자복제(부모, 서술자);
        ridájú(복제서술자 >= 0, "서술자 복제");
        Ìlànà_iye ọmọ_iye = 호출.과정복제(부모);
        ridájú(ọmọ_iye.Àfidámọ̀_iye() != 부모.Àfidámọ̀_iye(), "Ìlànà_iye Àfidámọ̀_iye 분리");
        ridájú(ọmọ_iye.부모식별자() == 부모.Àfidámọ̀_iye(), "부모 Ìlànà_iye Àfidámọ̀_iye");
        ridájú(호출.Ti(ọmọ_iye, 서술자) == 0 && 부모.파일서술자().열려있음(서술자), "ọmọ_iye Ti 격리");

        int 이전끝 = 호출.프로그램끝늘리기(부모, 8192);
        ridájú(이전끝 == 0x06000000, "àtòjọ_ètò_f5044b9b 끝 늘리기");
        ridájú(부모.프로그램끝() == 0x06002000, "àtòjọ_ètò_f5044b9b 끝 반영");
        ridájú(ọmọ_iye.프로그램끝() == 0x06000000, "과정별 àtòjọ_ètò_f5044b9b 끝 격리");

        ọmọ_iye.jáde_àtòjọ_ètò(7);
        ridájú(호출.자식기다리기(부모, ọmọ_iye.Àfidámọ̀_iye(), false) == (7 << 8), "ọmọ_iye jáde_àtòjọ_ètò 기다리기");
        ridájú(호출.접근가능("시험", 1) == -13, "ṣiṣẹ́_àṣẹ Ìyànda_iye 거부");
        ridájú(호출.aṣàmúlò_Àfidámọ̀() == 0 && 호출.Àjọṣe_Àfidámọ̀() == 0, "사용자와 무리 Àfidámọ̀_iye");
        ridájú("/".equals(호출.현재작업목록(2)) && 호출.ṣèpapòdà_àtòkọ_iṣẹ́("/") == 0, "현재 작업 ìgbéwọlé_Àtòkọ");
        ridájú(호출.단말인가(부모, 1), "표준 출력 단말");
        ridájú("JBenOS".equals(호출.체계정보().ètò_orúkọ()), "OS_iye msinfo32_exe");
    }

    private static void 실행파일시험(kánẹ́ẹ̀lì kánẹ́ẹ̀lì_iye) {
        byte[] détà = new byte[92];
        détà[0] = 0x7f;
        détà[1] = 'E';
        détà[2] = 'L';
        détà[3] = 'F';
        détà[4] = 1;
        détà[5] = 1;
        kọ_nọ́ńbà_odindi_iye(détà, 24, 0x04001000);
        kọ_nọ́ńbà_odindi_iye(détà, 32, 52);
        짧은정수쓰기(détà, 46, 40);
        짧은정수쓰기(détà, 48, 1);
        kọ_nọ́ńbà_odindi_iye(détà, 56, 8);
        kọ_nọ́ńbà_odindi_iye(détà, 60, 2);
        kọ_nọ́ńbà_odindi_iye(détà, 64, 0x04002000);
        kọ_nọ́ńbà_odindi_iye(détà, 72, 64);

        실행파일적재기.àwòrán àwòrán_iye = new 실행파일적재기().검사(détà);
        ridájú(àwòrán_iye.bẹ̀rẹ̀_àdírẹ́ẹ̀sì() == 0x04001000, "ELF Rọ́ọ̀nù àdírẹ́ẹ̀sì");
        ridájú(àwòrán_iye.구역들().size() == 1 && àwòrán_iye.구역들().get(0).종류() == 8, "ELF 빈 détà abala_iye");
        int 서술자 = kánẹ́ẹ̀lì_iye.체계호출().Ṣi(kánẹ́ẹ̀lì_iye.첫과정(), "시험", 체계호출.kàn_kàá_ipe_àkíyèsí_sí);
        ridájú(kánẹ́ẹ̀lì_iye.체계호출().fáìlì_ìdarí(kánẹ́ẹ̀lì_iye.첫과정(), 서술자, 2, 1) == 0, "ṣiṣẹ́_àṣẹ 시 Ti Àwọn_ààtò");
        ridájú(kánẹ́ẹ̀lì_iye.체계호출().ṣiṣẹ́_àṣẹ(kánẹ́ẹ̀lì_iye.첫과정(), détà, new String[] {"시험", "값"}, new String[] {"Èdè=한국어"}) == 0, "ELF ṣiṣẹ́_àṣẹ àwòrán_iye 적재");
        ridájú(kánẹ́ẹ̀lì_iye.첫과정().실행시작주소() == 0x04001000, "ṣiṣẹ́_àṣẹ Rọ́ọ̀nù àdírẹ́ẹ̀sì 반영");
        ridájú(kánẹ́ẹ̀lì_iye.첫과정().실행인자().length == 2 && kánẹ́ẹ̀lì_iye.첫과정().환경값().length == 1, "ṣiṣẹ́_àṣẹ 인자와 환경");
        ridájú(!kánẹ́ẹ̀lì_iye.첫과정().파일서술자().열려있음(서술자), "ṣiṣẹ́_àṣẹ 시 서술자 Ti");
        ridájú(kánẹ́ẹ̀lì_iye.쪽관리().바이트읽기(kánẹ́ẹ̀lì_iye.첫과정().àdírẹ́ẹ̀sì_àlàfo(), 0x04002000) == 0, "빈 détà abala_iye 영 pàjùbà");
    }

    private static void 입력시험(kánẹ́ẹ̀lì kánẹ́ẹ̀lì_iye) {
        kánẹ́ẹ̀lì_iye.입력관리().키누름('가');
        kánẹ́ẹ̀lì_iye.입력관리().쥐이동(3, -2);
        입력사건 첫사건 = kánẹ́ẹ̀lì_iye.입력관리().다음사건();
        입력사건 둘째사건 = kánẹ́ẹ̀lì_iye.입력관리().다음사건();
        ridájú(첫사건.사건종류() == 입력사건.종류.키누름, "자판 ìgbéṣẹ̀");
        ridájú(둘째사건.첫째값() == 3 && 둘째사건.둘째값() == -2, "쥐 gbé_iye ìgbéṣẹ̀");
    }

    private static void 하드웨어시험(olùpèsè_ohun_èlò_alárídìmú ohun_èlò_iye) {
        ohun_èlò_iye.kọ_ojú_báìtì(0x3f8, 0xab);
        ridájú(ohun_èlò_iye.포트바이트읽기(0x3f8) == 0xab, "ohun_èlò_alárídìmú_ojú I_O 경계");
        ridájú(ohun_èlò_iye.직렬기록().contains("JBenOS"), "직렬 àkọsílẹ̀_ìṣe_ìlà_ìbú");
    }

    private static void 개입중단과서술자시험() {
        IRQ_alákòóso alákòóso_iye = new IRQ_alákòóso();
        alákòóso_iye.forúkọsílẹ̀_ìgbéwọlé(0x21, Ibi_ìpamọ́_àdírẹ́ẹ̀sì -> Ibi_ìpamọ́_àdírẹ́ẹ̀sì + 4);
        alákòóso_iye.mu_ṣiṣẹ́();
        ridájú(alákòóso_iye.pínkiri_iye(0x21, 100) == 104, "IRQ pínkiri_iye");
        alákòóso_iye.ìsọ_di_àìṣiṣẹ́();
        ridájú(alákòóso_iye.pínkiri_iye(0x21, 100) == 100, "IRQ ìsọ_di_àìṣiṣẹ́");

        전역서술자표 서술자표 = new 전역서술자표();
        서술자표.ọ̀wọ̀_àdáwọ̀();
        ridájú(서술자표.조각들().size() == 5, "전역 서술자표");
        iṣẹ́_ipò_abala iṣẹ́_ipò = new iṣẹ́_ipò_abala();
        iṣẹ́_ipò.특권쌓임공간설정(0x10, 0x800000);
        ridájú(iṣẹ́_ipò.영번쌓임조각() == 0x10 && iṣẹ́_ipò.영번쌓임주소() == 0x800000, "작업 ipò_iye abala_iye");
    }

    private static void 저장장치와통신망시험() {
        고급기술결합장치 Ibi_ìpamọ́_ohun_èlò = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.abala_ìwọn];
        byte[] 읽은자료 = new byte[고급기술결합장치.abala_ìwọn];
        쓸자료[17] = 42;
        Ibi_ìpamọ́_ohun_èlò.Kọ(2, 쓸자료);
        Ibi_ìpamọ́_ohun_èlò.Kàá(2, 읽은자료);
        ridájú(읽은자료[17] == 42, "ATA abala_iye 읽고 Kọ");

        èròjà_ọ̀nà_agbédátà_alákòóso èròjà = new èròjà_ọ̀nà_agbédátà_alákòóso();
        èròjà.발견(new èròjà_ọ̀nà_agbédátà_alákòóso.ohun_èlò_iye(0x1022, 0x2000, 0xc000, 11));
        ridájú(èròjà.wá_ìgbéwọlé(0x1022, 0x2000) != null, "주변 ohun_èlò_iye wá_ìgbéwọlé");

        byte[] Ethernet_férèmù = new byte[34];
        Ethernet_férèmù[12] = 0x08;
        Ethernet_férèmù[13] = 0x00;
        Ethernet_férèmù[14] = 0x45;
        ridájú(Alásopọ̀_Àwọn_irinṣẹ́.이더넷상위규약(Ethernet_férèmù) == 0x0800, "이더넷 상위 iṣẹ́_iye");
        ridájú(Alásopọ̀_Àwọn_irinṣẹ́.상호통신망규약사판인가(Ethernet_férèmù, 14), "상호통신망규약 4판");
        ridájú(Alásopọ̀_Àwọn_irinṣẹ́.인터넷검사합(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 검사합");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        kọ_nọ́ńbà_odindi_iye(첫구역, 454, 63);
        kọ_nọ́ńbà_odindi_iye(첫구역, 458, 1024);
        ridájú(new 기본분할영역표().Kàá(첫구역).size() == 1, "àdáwọ̀ 분할 영역표");

        Alásopọ̀_ìpele ìpele_iye = new Alásopọ̀_ìpele();
        int[] 받은수 = new int[1];
        ìpele_iye.forúkọsílẹ̀_aṣàmúlò_détà_ìkẹ́kọ̀ọ́(7, (détà, Rọ́ọ̀nù, gígùn_iye) -> 받은수[0]++);
        byte[] férèmù_wá_atọ̀ka_àkóónú = new byte[14 + 20 + 8];
        férèmù_wá_atọ̀ka_àkóónú[12] = 0x08;
        férèmù_wá_atọ̀ka_àkóónú[13] = 0x00;
        férèmù_wá_atọ̀ka_àkóónú[14] = 0x45;
        férèmù_wá_atọ̀ka_àkóónú[16] = 0;
        férèmù_wá_atọ̀ka_àkóónú[17] = 28;
        férèmù_wá_atọ̀ka_àkóónú[23] = 17;
        férèmù_wá_atọ̀ka_àkóónú[36] = 0;
        férèmù_wá_atọ̀ka_àkóónú[37] = 7;
        ridájú(ìpele_iye.이더넷받기(férèmù_wá_atọ̀ka_àkóónú) && 받은수[0] == 1, "aṣàmúlò détà ìkẹ́kọ̀ọ́_iye pínkiri_iye");
    }

    private static void 화면과시계시험() {
        ẹyọ_ọ̀rọ̀_ṣàfihàn 화면 = new ẹyọ_ọ̀rọ̀_ṣàfihàn();
        화면.출력("가나\n다");
        ridájú(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 출력");
        aago aago = new aago(100);
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < 10; wá_atọ̀ka_àkóónú++) {
            aago.틱();
        }
        ridájú(aago.지난밀리초() == 100, "aago 틱 변환");
    }

    private static void kọ_nọ́ńbà_odindi_iye(byte[] détà, int 위치, int iye) {
        détà[위치] = (byte) iye;
        détà[위치 + 1] = (byte) (iye >>> 8);
        détà[위치 + 2] = (byte) (iye >>> 16);
        détà[위치 + 3] = (byte) (iye >>> 24);
    }

    private static void 짧은정수쓰기(byte[] détà, int 위치, int iye) {
        détà[위치] = (byte) iye;
        détà[위치 + 1] = (byte) (iye >>> 8);
    }

    private static void ridájú(boolean kání, String Orúkọ) {
        if (!kání) {
            throw new AssertionError("ìkùnà_iye: " + Orúkọ);
        }
        통과수++;
        System.out.println("fí_dátà_ránṣẹ́_iye: " + Orúkọ);
    }
}
