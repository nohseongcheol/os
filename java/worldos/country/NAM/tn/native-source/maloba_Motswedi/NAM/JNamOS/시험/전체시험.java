// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package NAM.JNamOS.시험;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import NAM.JNamOS.기억공간.memori_motsamaisi;
import NAM.JNamOS.기억공간.tsebe_motsamaisi;
import NAM.JNamOS.입력.입력사건;
import NAM.JNamOS.작업.Thulaganyo_Boleng;
import NAM.JNamOS.체계호출.체계호출;
import NAM.JNamOS.setsamaisadifaele.실행파일적재기;
import NAM.JNamOS.Khenele.Khenele;
import NAM.JNamOS.pinagare.호스트하드웨어;
import NAM.JNamOS.IRQ.IRQ_motsamaisi;
import NAM.JNamOS.서술자.전역서술자표;
import NAM.JNamOS.Polokelo_mobaele.고급기술결합장치;
import NAM.JNamOS.mobaele_Boleng.sethusi_setsamaisamelaetsa_motsamaisi;
import NAM.JNamOS.Neteweke_kokoanyodinepe.Neteweke_Thuluse;
import NAM.JNamOS.Neteweke_kokoanyodinepe.Neteweke_boalo;
import NAM.JNamOS.mobaele_Boleng.tshupanako;
import NAM.JNamOS.서술자.Tiro_kemo_karolo;
import NAM.JNamOS.화면.Letshwao_bontsha;
import NAM.JNamOS.setsamaisadifaele.기본분할영역표;

public final class 전체시험 {
    private static int 통과수;

    private 전체시험() {
    }

    public static void main(String[] 인자) {
        호스트하드웨어 mobaele_Boleng = new 호스트하드웨어();
        Khenele Khenele_Boleng = new Khenele(mobaele_Boleng);
        Khenele_Boleng.dirisa();

        기억공간시험(Khenele_Boleng);
        쪽관리시험(Khenele_Boleng);
        파일과과정시험(Khenele_Boleng);
        실행파일시험(Khenele_Boleng);
        입력시험(Khenele_Boleng);
        하드웨어시험(mobaele_Boleng);
        개입중단과서술자시험();
        저장장치와통신망시험();
        화면과시계시험();

        System.out.println("JNamOS 시험 fetisa_Boleng: " + 통과수);
    }

    private static void 기억공간시험(Khenele Khenele_Boleng) {
        memori_motsamaisi motsamaisi_Boleng = Khenele_Boleng.기억공간();
        int 첫주소 = motsamaisi_Boleng.정렬할당(100, 64);
        netefatsa((첫주소 & 63) == 0, "tlhamalatsa_Boleng abela_Polokelo");
        motsamaisi_Boleng.kwala_baete_Boleng(첫주소, (byte) 0x5a);
        netefatsa(motsamaisi_Boleng.바이트읽기(첫주소) == (byte) 0x5a, "물리 기억공간 읽고 kwala");
        int 사용전 = motsamaisi_Boleng.사용크기();
        motsamaisi_Boleng.ntsha_Polokelo(첫주소);
        netefatsa(motsamaisi_Boleng.사용크기() < 사용전, "기억공간 ntsha_Polokelo");
    }

    private static void 쪽관리시험(Khenele Khenele_Boleng) {
        tsebe_motsamaisi motsamaisi_Boleng = Khenele_Boleng.쪽관리();
        tsebe_motsamaisi.aterese_sebaka 부모공간 = motsamaisi_Boleng.새주소공간();
        motsamaisi_Boleng.mepa_tsebe(부모공간, 0x1000, true);
        motsamaisi_Boleng.kwala_baete_Boleng(부모공간, 0x1010, (byte) 7);
        tsebe_motsamaisi.aterese_sebaka ngwana_sebaka = motsamaisi_Boleng.쓰기시복사복제(부모공간);
        motsamaisi_Boleng.kwala_baete_Boleng(ngwana_sebaka, 0x1010, (byte) 9);
        netefatsa(motsamaisi_Boleng.바이트읽기(부모공간, 0x1010) == 7, "kwala 시 leloko_Boleng 부모 격리");
        netefatsa(motsamaisi_Boleng.바이트읽기(ngwana_sebaka, 0x1010) == 9, "kwala 시 leloko_Boleng ngwana_Boleng kwala");
    }

    private static void 파일과과정시험(Khenele Khenele_Boleng) {
        byte[] Diteng_Boleng = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        Khenele_Boleng.setsamaisadifaele().파일추가("시험", Diteng_Boleng);
        Thulaganyo_Boleng 부모 = Khenele_Boleng.첫과정();
        체계호출 호출 = Khenele_Boleng.체계호출();
        int 서술자 = 호출.bula(부모, "/시험", 체계호출.puiso_fela_folaga);
        netefatsa(서술자 >= 3, "faele bula");

        byte[] 받을곳 = new byte[Diteng_Boleng.length];
        netefatsa(호출.읽기(부모, 서술자, 받을곳, 받을곳.length) == Diteng_Boleng.length, "faele 읽기");
        netefatsa(Arrays.equals(Diteng_Boleng, 받을곳), "faele Diteng_Boleng");
        netefatsa(호출.위치옮기기(부모, 서술자, 0, 체계호출.batla_simolola) == 0, "faele 위치 sutisa_Boleng");

        int 복제서술자 = 호출.서술자복제(부모, 서술자);
        netefatsa(복제서술자 >= 0, "서술자 복제");
        Thulaganyo_Boleng ngwana_Boleng = 호출.과정복제(부모);
        netefatsa(ngwana_Boleng.setlhaodi_Boleng() != 부모.setlhaodi_Boleng(), "Thulaganyo_Boleng setlhaodi_Boleng 분리");
        netefatsa(ngwana_Boleng.부모식별자() == 부모.setlhaodi_Boleng(), "부모 Thulaganyo_Boleng setlhaodi_Boleng");
        netefatsa(호출.tswala(ngwana_Boleng, 서술자) == 0 && 부모.파일서술자().열려있음(서술자), "ngwana_Boleng tswala 격리");

        int 이전끝 = 호출.프로그램끝늘리기(부모, 8192);
        netefatsa(이전끝 == 0x06000000, "Tiriso_f5044b9b 끝 늘리기");
        netefatsa(부모.프로그램끝() == 0x06002000, "Tiriso_f5044b9b 끝 반영");
        netefatsa(ngwana_Boleng.프로그램끝() == 0x06000000, "과정별 Tiriso_f5044b9b 끝 격리");

        ngwana_Boleng.tswaya_Tiriso(7);
        netefatsa(호출.자식기다리기(부모, ngwana_Boleng.setlhaodi_Boleng(), false) == (7 << 8), "ngwana_Boleng tswaya_Tiriso 기다리기");
        netefatsa(호출.접근가능("시험", 1) == -13, "diragatsa_Taelo tetla_Boleng 거부");
        netefatsa(호출.modirisi_setlhaodi() == 0 && 호출.setlhopha_setlhaodi() == 0, "사용자와 무리 setlhaodi_Boleng");
        netefatsa("/".equals(호출.ga_jaana_lenaneotiro(2)) && 호출.fetola_lenaneotiro("/") == 0, "ga_jaana_selwana 작업 tsenyo_lenaane");
        netefatsa(호출.단말인가(부모, 1), "표준 출력 단말");
        netefatsa("JNamOS".equals(호출.체계정보().tsamaiso_leina()), "Tsamaisotiriso_Boleng msinfo32_exe");
    }

    private static void 실행파일시험(Khenele Khenele_Boleng) {
        byte[] tshedimosetso = new byte[92];
        tshedimosetso[0] = 0x7f;
        tshedimosetso[1] = 'E';
        tshedimosetso[2] = 'L';
        tshedimosetso[3] = 'F';
        tshedimosetso[4] = 1;
        tshedimosetso[5] = 1;
        kwala_Palotlalo_Boleng(tshedimosetso, 24, 0x04001000);
        kwala_Palotlalo_Boleng(tshedimosetso, 32, 52);
        짧은정수쓰기(tshedimosetso, 46, 40);
        짧은정수쓰기(tshedimosetso, 48, 1);
        kwala_Palotlalo_Boleng(tshedimosetso, 56, 8);
        kwala_Palotlalo_Boleng(tshedimosetso, 60, 2);
        kwala_Palotlalo_Boleng(tshedimosetso, 64, 0x04002000);
        kwala_Palotlalo_Boleng(tshedimosetso, 72, 64);

        실행파일적재기.Setshwantsho Setshwantsho_Boleng = new 실행파일적재기().검사(tshedimosetso);
        netefatsa(Setshwantsho_Boleng.simolola_aterese() == 0x04001000, "ELF dirisa aterese");
        netefatsa(Setshwantsho_Boleng.구역들().size() == 1 && Setshwantsho_Boleng.구역들().get(0).종류() == 8, "ELF 빈 tshedimosetso karolo_Boleng");
        int 서술자 = Khenele_Boleng.체계호출().bula(Khenele_Boleng.첫과정(), "시험", 체계호출.puiso_fela_folaga);
        netefatsa(Khenele_Boleng.체계호출().faele_taolo(Khenele_Boleng.첫과정(), 서술자, 2, 1) == 0, "diragatsa_Taelo 시 tswala Diseting");
        netefatsa(Khenele_Boleng.체계호출().diragatsa_Taelo(Khenele_Boleng.첫과정(), tshedimosetso, new String[] {"시험", "값"}, new String[] {"Puo=한국어"}) == 0, "ELF diragatsa_Taelo Setshwantsho_Boleng 적재");
        netefatsa(Khenele_Boleng.첫과정().실행시작주소() == 0x04001000, "diragatsa_Taelo dirisa aterese 반영");
        netefatsa(Khenele_Boleng.첫과정().실행인자().length == 2 && Khenele_Boleng.첫과정().환경값().length == 1, "diragatsa_Taelo 인자와 환경");
        netefatsa(!Khenele_Boleng.첫과정().파일서술자().열려있음(서술자), "diragatsa_Taelo 시 서술자 tswala");
        netefatsa(Khenele_Boleng.쪽관리().바이트읽기(Khenele_Boleng.첫과정().aterese_sebaka(), 0x04002000) == 0, "빈 tshedimosetso karolo_Boleng 영 go_baakanyetsa_tiriso");
    }

    private static void 입력시험(Khenele Khenele_Boleng) {
        Khenele_Boleng.입력관리().키누름('가');
        Khenele_Boleng.입력관리().쥐이동(3, -2);
        입력사건 첫사건 = Khenele_Boleng.입력관리().다음사건();
        입력사건 둘째사건 = Khenele_Boleng.입력관리().다음사건();
        netefatsa(첫사건.사건종류() == 입력사건.종류.키누름, "자판 tiragalo");
        netefatsa(둘째사건.첫째값() == 3 && 둘째사건.둘째값() == -2, "쥐 sutisa_Boleng tiragalo");
    }

    private static void 하드웨어시험(호스트하드웨어 mobaele_Boleng) {
        mobaele_Boleng.kwala_gorogisetsa_baete(0x3f8, 0xab);
        netefatsa(mobaele_Boleng.포트바이트읽기(0x3f8) == 0xab, "포트 I_O 경계");
        netefatsa(mobaele_Boleng.직렬기록().contains("JNamOS"), "직렬 rekota_mola");
    }

    private static void 개입중단과서술자시험() {
        IRQ_motsamaisi motsamaisi_Boleng = new IRQ_motsamaisi();
        motsamaisi_Boleng.kwadisa_tsenyo(0x21, Polokelo_aterese -> Polokelo_aterese + 4);
        motsamaisi_Boleng.kgontsha();
        netefatsa(motsamaisi_Boleng.aba_Boleng(0x21, 100) == 104, "IRQ aba_Boleng");
        motsamaisi_Boleng.kgontsha_go_dira();
        netefatsa(motsamaisi_Boleng.aba_Boleng(0x21, 100) == 100, "IRQ kgontsha_go_dira");

        전역서술자표 서술자표 = new 전역서술자표();
        서술자표.sete_boleng_jo_bo_rulaganyeditsweng_ruri();
        netefatsa(서술자표.조각들().size() == 5, "전역 서술자표");
        Tiro_kemo_karolo Tiro_kemo = new Tiro_kemo_karolo();
        Tiro_kemo.특권쌓임공간설정(0x10, 0x800000);
        netefatsa(Tiro_kemo.영번쌓임조각() == 0x10 && Tiro_kemo.영번쌓임주소() == 0x800000, "작업 kemo_Boleng karolo_Boleng");
    }

    private static void 저장장치와통신망시험() {
        고급기술결합장치 Polokelo_mobaele = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.karolo_lekanya];
        byte[] 읽은자료 = new byte[고급기술결합장치.karolo_lekanya];
        쓸자료[17] = 42;
        Polokelo_mobaele.kwala(2, 쓸자료);
        Polokelo_mobaele.읽기(2, 읽은자료);
        netefatsa(읽은자료[17] == 42, "ATA karolo_Boleng 읽고 kwala");

        sethusi_setsamaisamelaetsa_motsamaisi sethusi = new sethusi_setsamaisamelaetsa_motsamaisi();
        sethusi.발견(new sethusi_setsamaisamelaetsa_motsamaisi.mobaele_Boleng(0x1022, 0x2000, 0xc000, 11));
        netefatsa(sethusi.batla_tsenyo(0x1022, 0x2000) != null, "주변 mobaele_Boleng batla_tsenyo");

        byte[] Ithanete_Foreimi = new byte[34];
        Ithanete_Foreimi[12] = 0x08;
        Ithanete_Foreimi[13] = 0x00;
        Ithanete_Foreimi[14] = 0x45;
        netefatsa(Neteweke_Thuluse.이더넷상위규약(Ithanete_Foreimi) == 0x0800, "이더넷 상위 konteraka_Boleng");
        netefatsa(Neteweke_Thuluse.상호통신망규약사판인가(Ithanete_Foreimi, 14), "상호통신망규약 4판");
        netefatsa(Neteweke_Thuluse.인터넷검사합(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 검사합");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        kwala_Palotlalo_Boleng(첫구역, 454, 63);
        kwala_Palotlalo_Boleng(첫구역, 458, 1024);
        netefatsa(new 기본분할영역표().읽기(첫구역).size() == 1, "boleng_jo_bo_rulaganyeditsweng_ruri 분할 영역표");

        Neteweke_boalo boalo_Boleng = new Neteweke_boalo();
        int[] 받은수 = new int[1];
        boalo_Boleng.kwadisa_modirisi_tshedimosetso_thuto(7, (tshedimosetso, dirisa, boleele_Boleng) -> 받은수[0]++);
        byte[] Foreimi_tshupane = new byte[14 + 20 + 8];
        Foreimi_tshupane[12] = 0x08;
        Foreimi_tshupane[13] = 0x00;
        Foreimi_tshupane[14] = 0x45;
        Foreimi_tshupane[16] = 0;
        Foreimi_tshupane[17] = 28;
        Foreimi_tshupane[23] = 17;
        Foreimi_tshupane[36] = 0;
        Foreimi_tshupane[37] = 7;
        netefatsa(boalo_Boleng.이더넷받기(Foreimi_tshupane) && 받은수[0] == 1, "modirisi tshedimosetso thuto_Boleng aba_Boleng");
    }

    private static void 화면과시계시험() {
        Letshwao_bontsha 화면 = new Letshwao_bontsha();
        화면.출력("가나\n다");
        netefatsa(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 출력");
        tshupanako tshupanako = new tshupanako(100);
        for (int tshupane = 0; tshupane < 10; tshupane++) {
            tshupanako.틱();
        }
        netefatsa(tshupanako.지난밀리초() == 100, "tshupanako 틱 변환");
    }

    private static void kwala_Palotlalo_Boleng(byte[] tshedimosetso, int 위치, int Boleng) {
        tshedimosetso[위치] = (byte) Boleng;
        tshedimosetso[위치 + 1] = (byte) (Boleng >>> 8);
        tshedimosetso[위치 + 2] = (byte) (Boleng >>> 16);
        tshedimosetso[위치 + 3] = (byte) (Boleng >>> 24);
    }

    private static void 짧은정수쓰기(byte[] tshedimosetso, int 위치, int Boleng) {
        tshedimosetso[위치] = (byte) Boleng;
        tshedimosetso[위치 + 1] = (byte) (Boleng >>> 8);
    }

    private static void netefatsa(boolean boemo, String leina) {
        if (!boemo) {
            throw new AssertionError("palelo_Boleng: " + leina);
        }
        통과수++;
        System.out.println("fetisa_Boleng: " + leina);
    }
}
