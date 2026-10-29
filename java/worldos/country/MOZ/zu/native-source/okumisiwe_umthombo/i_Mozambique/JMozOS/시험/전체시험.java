// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package i_Mozambique.JMozOS.시험;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import i_Mozambique.JMozOS.기억공간.inkumbulo_imeneja;
import i_Mozambique.JMozOS.기억공간.ikhasi_imeneja;
import i_Mozambique.JMozOS.입력.입력사건;
import i_Mozambique.JMozOS.작업.Inqubo_inani;
import i_Mozambique.JMozOS.체계호출.체계호출;
import i_Mozambique.JMozOS.isistimu_yefayela.실행파일적재기;
import i_Mozambique.JMozOS.ikhenela.ikhenela;
import i_Mozambique.JMozOS.singatha.호스트하드웨어;
import i_Mozambique.JMozOS.i_IRQ.i_IRQ_imeneja;
import i_Mozambique.JMozOS.서술자.전역서술자표;
import i_Mozambique.JMozOS.Indawo_yokugcina_idivayisi.고급기술결합장치;
import i_Mozambique.JMozOS.idivayisi_inani.isesekeli_isixhumanisi_imeneja;
import i_Mozambique.JMozOS.iNethiwekhi_Isitaki.iNethiwekhi_Amathuluzi;
import i_Mozambique.JMozOS.iNethiwekhi_Isitaki.iNethiwekhi_ugqinsi;
import i_Mozambique.JMozOS.idivayisi_inani.iwashi;
import i_Mozambique.JMozOS.서술자.umsebenzi_isimo_isegimenti;
import i_Mozambique.JMozOS.화면.uhlamvusimo_bonisa;
import i_Mozambique.JMozOS.isistimu_yefayela.기본분할영역표;

public final class 전체시험 {
    private static int 통과수;

    private 전체시험() {
    }

    public static void main(String[] 인자) {
        호스트하드웨어 idivayisi_inani = new 호스트하드웨어();
        ikhenela ikhenela_inani = new ikhenela(idivayisi_inani);
        ikhenela_inani.Sebenzisa();

        기억공간시험(ikhenela_inani);
        쪽관리시험(ikhenela_inani);
        파일과과정시험(ikhenela_inani);
        실행파일시험(ikhenela_inani);
        입력시험(ikhenela_inani);
        하드웨어시험(idivayisi_inani);
        개입중단과서술자시험();
        저장장치와통신망시험();
        화면과시계시험();

        System.out.println("JMozOS 시험 dlulisa_inani: " + 통과수);
    }

    private static void 기억공간시험(ikhenela ikhenela_inani) {
        inkumbulo_imeneja imeneja_inani = ikhenela_inani.기억공간();
        int 첫주소 = imeneja_inani.정렬할당(100, 64);
        qiniseka((첫주소 & 63) == 0, "qondisa_inani abela_Indawo_yokugcina");
        imeneja_inani.bhala_ibhayithi_inani(첫주소, (byte) 0x5a);
        qiniseka(imeneja_inani.바이트읽기(첫주소) == (byte) 0x5a, "물리 기억공간 읽고 Bhala");
        int 사용전 = imeneja_inani.사용크기();
        imeneja_inani.khulula_Indawo_yokugcina(첫주소);
        qiniseka(imeneja_inani.사용크기() < 사용전, "기억공간 khulula_Indawo_yokugcina");
    }

    private static void 쪽관리시험(ikhenela ikhenela_inani) {
        ikhasi_imeneja imeneja_inani = ikhenela_inani.쪽관리();
        ikhasi_imeneja.ikheli_indawo 부모공간 = imeneja_inani.새주소공간();
        imeneja_inani.faka_kumephu_ikhasi(부모공간, 0x1000, true);
        imeneja_inani.bhala_ibhayithi_inani(부모공간, 0x1010, (byte) 7);
        ikhasi_imeneja.ikheli_indawo ingane_indawo = imeneja_inani.쓰기시복사복제(부모공간);
        imeneja_inani.bhala_ibhayithi_inani(ingane_indawo, 0x1010, (byte) 9);
        qiniseka(imeneja_inani.바이트읽기(부모공간, 0x1010) == 7, "Bhala 시 kopisha_inani 부모 격리");
        qiniseka(imeneja_inani.바이트읽기(ingane_indawo, 0x1010) == 9, "Bhala 시 kopisha_inani ingane_inani Bhala");
    }

    private static void 파일과과정시험(ikhenela ikhenela_inani) {
        byte[] Okuqukethwe_inani = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        ikhenela_inani.isistimu_yefayela().파일추가("시험", Okuqukethwe_inani);
        Inqubo_inani 부모 = ikhenela_inani.첫과정();
        체계호출 호출 = ikhenela_inani.체계호출();
        int 서술자 = 호출.Vula(부모, "/시험", 체계호출.fundwayo_kuphela_iflegi);
        qiniseka(서술자 >= 3, "Ihele Vula");

        byte[] 받을곳 = new byte[Okuqukethwe_inani.length];
        qiniseka(호출.Funda(부모, 서술자, 받을곳, 받을곳.length) == Okuqukethwe_inani.length, "Ihele Funda");
        qiniseka(Arrays.equals(Okuqukethwe_inani, 받을곳), "Ihele Okuqukethwe_inani");
        qiniseka(호출.위치옮기기(부모, 서술자, 0, 체계호출.Bheka_qala) == 0, "Ihele 위치 susa_inani");

        int 복제서술자 = 호출.서술자복제(부모, 서술자);
        qiniseka(복제서술자 >= 0, "서술자 복제");
        Inqubo_inani ingane_inani = 호출.과정복제(부모);
        qiniseka(ingane_inani.isivezi_inani() != 부모.isivezi_inani(), "Inqubo_inani isivezi_inani 분리");
        qiniseka(ingane_inani.부모식별자() == 부모.isivezi_inani(), "부모 Inqubo_inani isivezi_inani");
        qiniseka(호출.Vala(ingane_inani, 서술자) == 0 && 부모.파일서술자().열려있음(서술자), "ingane_inani Vala 격리");

        int 이전끝 = 호출.프로그램끝늘리기(부모, 8192);
        qiniseka(이전끝 == 0x06000000, "i_app_f5044b9b 끝 늘리기");
        qiniseka(부모.프로그램끝() == 0x06002000, "i_app_f5044b9b 끝 반영");
        qiniseka(ingane_inani.프로그램끝() == 0x06000000, "과정별 i_app_f5044b9b 끝 격리");

        ingane_inani.phuma_i_app(7);
        qiniseka(호출.자식기다리기(부모, ingane_inani.isivezi_inani(), false) == (7 << 8), "ingane_inani phuma_i_app 기다리기");
        qiniseka(호출.접근가능("시험", 1) == -13, "yenza_umyalo imvume_inani 거부");
        qiniseka(호출.umsebenzisi_isivezi() == 0 && 호출.iqoqo_isivezi() == 0, "사용자와 무리 isivezi_inani");
        qiniseka("/".equals(호출.현재작업목록(2)) && 호출.guqulela_kokunye_uhlu_lwemisebenzi("/") == 0, "현재 작업 okufakwayo_Uhlu");
        qiniseka(호출.단말인가(부모, 1), "표준 출력 단말");
        qiniseka("JMozOS".equals(호출.체계정보().isistimu_igama()), "isistimu_yokusebenza_inani I_msinfo32_exe");
    }

    private static void 실행파일시험(ikhenela ikhenela_inani) {
        byte[] imininingwane = new byte[92];
        imininingwane[0] = 0x7f;
        imininingwane[1] = 'E';
        imininingwane[2] = 'L';
        imininingwane[3] = 'F';
        imininingwane[4] = 1;
        imininingwane[5] = 1;
        bhala_inamba_inani(imininingwane, 24, 0x04001000);
        bhala_inamba_inani(imininingwane, 32, 52);
        짧은정수쓰기(imininingwane, 46, 40);
        짧은정수쓰기(imininingwane, 48, 1);
        bhala_inamba_inani(imininingwane, 56, 8);
        bhala_inamba_inani(imininingwane, 60, 2);
        bhala_inamba_inani(imininingwane, 64, 0x04002000);
        bhala_inamba_inani(imininingwane, 72, 64);

        실행파일적재기.isithombe isithombe_inani = new 실행파일적재기().검사(imininingwane);
        qiniseka(isithombe_inani.qala_ikheli() == 0x04001000, "ELF Sebenzisa ikheli");
        qiniseka(isithombe_inani.구역들().size() == 1 && isithombe_inani.구역들().get(0).종류() == 8, "ELF 빈 imininingwane isigaba_inani");
        int 서술자 = ikhenela_inani.체계호출().Vula(ikhenela_inani.첫과정(), "시험", 체계호출.fundwayo_kuphela_iflegi);
        qiniseka(ikhenela_inani.체계호출().ifayela_isilawuli(ikhenela_inani.첫과정(), 서술자, 2, 1) == 0, "yenza_umyalo 시 Vala Izinhlelo");
        qiniseka(ikhenela_inani.체계호출().yenza_umyalo(ikhenela_inani.첫과정(), imininingwane, new String[] {"시험", "값"}, new String[] {"Ulimi=Isi_Zulu"}) == 0, "ELF yenza_umyalo isithombe_inani 적재");
        qiniseka(ikhenela_inani.첫과정().실행시작주소() == 0x04001000, "yenza_umyalo Sebenzisa ikheli 반영");
        qiniseka(ikhenela_inani.첫과정().실행인자().length == 2 && ikhenela_inani.첫과정().환경값().length == 1, "yenza_umyalo 인자와 환경");
        qiniseka(!ikhenela_inani.첫과정().파일서술자().열려있음(서술자), "yenza_umyalo 시 서술자 Vala");
        qiniseka(ikhenela_inani.쪽관리().바이트읽기(ikhenela_inani.첫과정().ikheli_indawo(), 0x04002000) == 0, "빈 imininingwane isigaba_inani 영 qalisa");
    }

    private static void 입력시험(ikhenela ikhenela_inani) {
        ikhenela_inani.입력관리().키누름('가');
        ikhenela_inani.입력관리().쥐이동(3, -2);
        입력사건 첫사건 = ikhenela_inani.입력관리().다음사건();
        입력사건 둘째사건 = ikhenela_inani.입력관리().다음사건();
        qiniseka(첫사건.사건종류() == 입력사건.종류.키누름, "자판 isigameko");
        qiniseka(둘째사건.첫째값() == 3 && 둘째사건.둘째값() == -2, "쥐 susa_inani isigameko");
    }

    private static void 하드웨어시험(호스트하드웨어 idivayisi_inani) {
        idivayisi_inani.bhala_intuba_ibhayithi(0x3f8, 0xab);
        qiniseka(idivayisi_inani.포트바이트읽기(0x3f8) == 0xab, "포트 i_I_O 경계");
        qiniseka(idivayisi_inani.직렬기록().contains("JMozOS"), "직렬 loga_umugqa");
    }

    private static void 개입중단과서술자시험() {
        i_IRQ_imeneja imeneja_inani = new i_IRQ_imeneja();
        imeneja_inani.bhalisa_okufakwayo(0x21, Indawo_yokugcina_ikheli -> Indawo_yokugcina_ikheli + 4);
        imeneja_inani.vumela();
        qiniseka(imeneja_inani.sabalalisa_inani(0x21, 100) == 104, "i_IRQ sabalalisa_inani");
        imeneja_inani.yekisa_ukusebenza();
        qiniseka(imeneja_inani.sabalalisa_inani(0x21, 100) == 100, "i_IRQ yekisa_ukusebenza");

        전역서술자표 서술자표 = new 전역서술자표();
        서술자표.isethi_inani_elimisiwe();
        qiniseka(서술자표.조각들().size() == 5, "전역 서술자표");
        umsebenzi_isimo_isegimenti umsebenzi_isimo = new umsebenzi_isimo_isegimenti();
        umsebenzi_isimo.특권쌓임공간설정(0x10, 0x800000);
        qiniseka(umsebenzi_isimo.영번쌓임조각() == 0x10 && umsebenzi_isimo.영번쌓임주소() == 0x800000, "작업 isimo_inani isigaba_inani");
    }

    private static void 저장장치와통신망시험() {
        고급기술결합장치 Indawo_yokugcina_idivayisi = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.isigaba_linganisa];
        byte[] 읽은자료 = new byte[고급기술결합장치.isigaba_linganisa];
        쓸자료[17] = 42;
        Indawo_yokugcina_idivayisi.Bhala(2, 쓸자료);
        Indawo_yokugcina_idivayisi.Funda(2, 읽은자료);
        qiniseka(읽은자료[17] == 42, "ATA isigaba_inani 읽고 Bhala");

        isesekeli_isixhumanisi_imeneja isesekeli = new isesekeli_isixhumanisi_imeneja();
        isesekeli.발견(new isesekeli_isixhumanisi_imeneja.idivayisi_inani(0x1022, 0x2000, 0xc000, 11));
        qiniseka(isesekeli.thola_okufakwayo(0x1022, 0x2000) != null, "주변 idivayisi_inani thola_okufakwayo");

        byte[] i_Ethernet_uhlaka = new byte[34];
        i_Ethernet_uhlaka[12] = 0x08;
        i_Ethernet_uhlaka[13] = 0x00;
        i_Ethernet_uhlaka[14] = 0x45;
        qiniseka(iNethiwekhi_Amathuluzi.이더넷상위규약(i_Ethernet_uhlaka) == 0x0800, "이더넷 상위 udaba_inani");
        qiniseka(iNethiwekhi_Amathuluzi.상호통신망규약사판인가(i_Ethernet_uhlaka, 14), "상호통신망규약 4판");
        qiniseka(iNethiwekhi_Amathuluzi.인터넷검사합(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 검사합");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        bhala_inamba_inani(첫구역, 454, 63);
        bhala_inamba_inani(첫구역, 458, 1024);
        qiniseka(new 기본분할영역표().Funda(첫구역).size() == 1, "inani_elimisiwe 분할 영역표");

        iNethiwekhi_ugqinsi ugqinsi_inani = new iNethiwekhi_ugqinsi();
        int[] 받은수 = new int[1];
        ugqinsi_inani.bhalisa_umsebenzisi_imininingwane_isifundo(7, (imininingwane, Sebenzisa, ubude_inani) -> 받은수[0]++);
        byte[] uhlaka_thola_inkomba = new byte[14 + 20 + 8];
        uhlaka_thola_inkomba[12] = 0x08;
        uhlaka_thola_inkomba[13] = 0x00;
        uhlaka_thola_inkomba[14] = 0x45;
        uhlaka_thola_inkomba[16] = 0;
        uhlaka_thola_inkomba[17] = 28;
        uhlaka_thola_inkomba[23] = 17;
        uhlaka_thola_inkomba[36] = 0;
        uhlaka_thola_inkomba[37] = 7;
        qiniseka(ugqinsi_inani.이더넷받기(uhlaka_thola_inkomba) && 받은수[0] == 1, "umsebenzisi imininingwane isifundo_inani sabalalisa_inani");
    }

    private static void 화면과시계시험() {
        uhlamvusimo_bonisa 화면 = new uhlamvusimo_bonisa();
        화면.출력("가나\n다");
        qiniseka(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 출력");
        iwashi iwashi = new iwashi(100);
        for (int thola_inkomba = 0; thola_inkomba < 10; thola_inkomba++) {
            iwashi.틱();
        }
        qiniseka(iwashi.지난밀리초() == 100, "iwashi 틱 변환");
    }

    private static void bhala_inamba_inani(byte[] imininingwane, int 위치, int inani) {
        imininingwane[위치] = (byte) inani;
        imininingwane[위치 + 1] = (byte) (inani >>> 8);
        imininingwane[위치 + 2] = (byte) (inani >>> 16);
        imininingwane[위치 + 3] = (byte) (inani >>> 24);
    }

    private static void 짧은정수쓰기(byte[] imininingwane, int 위치, int inani) {
        imininingwane[위치] = (byte) inani;
        imininingwane[위치 + 1] = (byte) (inani >>> 8);
    }

    private static void qiniseka(boolean isimo, String Igama) {
        if (!isimo) {
            throw new AssertionError("ukwehluleka_inani: " + Igama);
        }
        통과수++;
        System.out.println("dlulisa_inani: " + Igama);
    }
}
