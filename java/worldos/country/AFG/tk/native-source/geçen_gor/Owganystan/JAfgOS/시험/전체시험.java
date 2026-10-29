// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Owganystan.JAfgOS.시험;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Owganystan.JAfgOS.기억공간.ýat_iş_dolandyryjy;
import Owganystan.JAfgOS.기억공간.sahypa_iş_dolandyryjy;
import Owganystan.JAfgOS.입력.입력사건;
import Owganystan.JAfgOS.작업.Proses_baha;
import Owganystan.JAfgOS.체계호출.체계호출;
import Owganystan.JAfgOS.faýl_ulgamy.실행파일적재기;
import Owganystan.JAfgOS.ýadro.ýadro;
import Owganystan.JAfgOS.esasy.호스트하드웨어;
import Owganystan.JAfgOS.IRQ.IRQ_iş_dolandyryjy;
import Owganystan.JAfgOS.서술자.전역서술자표;
import Owganystan.JAfgOS.Ammar_enjam.고급기술결합장치;
import Owganystan.JAfgOS.enjam_baha.kömekçi_enjam_şina_iş_dolandyryjy;
import Owganystan.JAfgOS.Tor_Desse.Tor_Gurallar;
import Owganystan.JAfgOS.Tor_Desse.Tor_dereje;
import Owganystan.JAfgOS.enjam_baha.sagat;
import Owganystan.JAfgOS.서술자.tabşyryk_ýagdaý_bölek;
import Owganystan.JAfgOS.화면.nyşan_ekran;
import Owganystan.JAfgOS.faýl_ulgamy.기본분할영역표;

public final class 전체시험 {
    private static int 통과수;

    private 전체시험() {
    }

    public static void main(String[] 인자) {
        호스트하드웨어 enjam_baha = new 호스트하드웨어();
        ýadro ýadro_baha = new ýadro(enjam_baha);
        ýadro_baha.Bitir();

        기억공간시험(ýadro_baha);
        쪽관리시험(ýadro_baha);
        파일과과정시험(ýadro_baha);
        실행파일시험(ýadro_baha);
        입력시험(ýadro_baha);
        하드웨어시험(enjam_baha);
        개입중단과서술자시험();
        저장장치와통신망시험();
        화면과시계시험();

        System.out.println("JAfgOS 시험 통과: " + 통과수);
    }

    private static void 기억공간시험(ýadro ýadro_baha) {
        ýat_iş_dolandyryjy iş_dolandyryjy_baha = ýadro_baha.기억공간();
        int 첫주소 = iş_dolandyryjy_baha.정렬할당(100, 64);
        barla((첫주소 & 63) == 0, "deňle_baha bölüp_aýyr_Ammar");
        iş_dolandyryjy_baha.ýaz_baýt_baha(첫주소, (byte) 0x5a);
        barla(iş_dolandyryjy_baha.바이트읽기(첫주소) == (byte) 0x5a, "물리 기억공간 읽고 Ýaz");
        int 사용전 = iş_dolandyryjy_baha.사용크기();
        iş_dolandyryjy_baha.goýbermek_Ammar(첫주소);
        barla(iş_dolandyryjy_baha.사용크기() < 사용전, "기억공간 goýbermek_Ammar");
    }

    private static void 쪽관리시험(ýadro ýadro_baha) {
        sahypa_iş_dolandyryjy iş_dolandyryjy_baha = ýadro_baha.쪽관리();
        sahypa_iş_dolandyryjy.salgy_ýer 부모공간 = iş_dolandyryjy_baha.새주소공간();
        iş_dolandyryjy_baha.kartada_görkez_sahypa(부모공간, 0x1000, true);
        iş_dolandyryjy_baha.ýaz_baýt_baha(부모공간, 0x1010, (byte) 7);
        sahypa_iş_dolandyryjy.salgy_ýer çaga_ýer = iş_dolandyryjy_baha.쓰기시복사복제(부모공간);
        iş_dolandyryjy_baha.ýaz_baýt_baha(çaga_ýer, 0x1010, (byte) 9);
        barla(iş_dolandyryjy_baha.바이트읽기(부모공간, 0x1010) == 7, "Ýaz 시 synp_baha 부모 격리");
        barla(iş_dolandyryjy_baha.바이트읽기(çaga_ýer, 0x1010) == 9, "Ýaz 시 synp_baha çaga_baha Ýaz");
    }

    private static void 파일과과정시험(ýadro ýadro_baha) {
        byte[] Mazmun_baha = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        ýadro_baha.faýl_ulgamy().파일추가("시험", Mazmun_baha);
        Proses_baha 부모 = ýadro_baha.첫과정();
        체계호출 호출 = ýadro_baha.체계호출();
        int 서술자 = 호출.Aç(부모, "/시험", 체계호출.diňe_okalýan_alamat_goý);
        barla(서술자 >= 3, "Faýl Aç");

        byte[] 받을곳 = new byte[Mazmun_baha.length];
        barla(호출.Oka(부모, 서술자, 받을곳, 받을곳.length) == Mazmun_baha.length, "Faýl Oka");
        barla(Arrays.equals(Mazmun_baha, 받을곳), "Faýl Mazmun_baha");
        barla(호출.위치옮기기(부모, 서술자, 0, 체계호출.gözle_başlat) == 0, "Faýl 위치 ýerini_üýtget_baha");

        int 복제서술자 = 호출.서술자복제(부모, 서술자);
        barla(복제서술자 >= 0, "서술자 복제");
        Proses_baha çaga_baha = 호출.과정복제(부모);
        barla(çaga_baha.tanaýjy_baha() != 부모.tanaýjy_baha(), "Proses_baha tanaýjy_baha 분리");
        barla(çaga_baha.부모식별자() == 부모.tanaýjy_baha(), "부모 Proses_baha tanaýjy_baha");
        barla(호출.Ýap(çaga_baha, 서술자) == 0 && 부모.파일서술자().열려있음(서술자), "çaga_baha Ýap 격리");

        int 이전끝 = 호출.프로그램끝늘리기(부모, 8192);
        barla(이전끝 == 0x06000000, "programma_f5044b9b 끝 늘리기");
        barla(부모.프로그램끝() == 0x06002000, "programma_f5044b9b 끝 반영");
        barla(çaga_baha.프로그램끝() == 0x06000000, "과정별 programma_f5044b9b 끝 격리");

        çaga_baha.çyk_programma(7);
        barla(호출.자식기다리기(부모, çaga_baha.tanaýjy_baha(), false) == (7 << 8), "çaga_baha çyk_programma 기다리기");
        barla(호출.접근가능("시험", 1) == -13, "ýerine_ýetir_buýruk rugsat_baha 거부");
        barla(호출.ulanyjy_tanaýjy() == 0 && 호출.topar_tanaýjy() == 0, "사용자와 무리 tanaýjy_baha");
        barla("/".equals(호출.현재작업목록(2)) && 호출.calşyr_meseleleriň_sanawy("/") == 0, "현재 작업 girizmeklik_Sanaw");
        barla(호출.단말인가(부모, 1), "표준 출력 단말");
        barla("JAfgOS".equals(호출.체계정보().ulgam_at()), "operasiýa_ulgamy_baha msinfo32_exe");
    }

    private static void 실행파일시험(ýadro ýadro_baha) {
        byte[] maglumat = new byte[92];
        maglumat[0] = 0x7f;
        maglumat[1] = 'E';
        maglumat[2] = 'L';
        maglumat[3] = 'F';
        maglumat[4] = 1;
        maglumat[5] = 1;
        ýaz_bitin_baha(maglumat, 24, 0x04001000);
        ýaz_bitin_baha(maglumat, 32, 52);
        짧은정수쓰기(maglumat, 46, 40);
        짧은정수쓰기(maglumat, 48, 1);
        ýaz_bitin_baha(maglumat, 56, 8);
        ýaz_bitin_baha(maglumat, 60, 2);
        ýaz_bitin_baha(maglumat, 64, 0x04002000);
        ýaz_bitin_baha(maglumat, 72, 64);

        실행파일적재기.surat surat_baha = new 실행파일적재기().검사(maglumat);
        barla(surat_baha.başlat_salgy() == 0x04001000, "ELF Bitir salgy");
        barla(surat_baha.구역들().size() == 1 && surat_baha.구역들().get(0).종류() == 8, "ELF 빈 maglumat bölüm_baha_366e0bfa");
        int 서술자 = ýadro_baha.체계호출().Aç(ýadro_baha.첫과정(), "시험", 체계호출.diňe_okalýan_alamat_goý);
        barla(ýadro_baha.체계호출().faýl_dolandyryş(ýadro_baha.첫과정(), 서술자, 2, 1) == 0, "ýerine_ýetir_buýruk 시 Ýap Düzümler");
        barla(ýadro_baha.체계호출().ýerine_ýetir_buýruk(ýadro_baha.첫과정(), maglumat, new String[] {"시험", "값"}, new String[] {"Dil=한국어"}) == 0, "ELF ýerine_ýetir_buýruk surat_baha 적재");
        barla(ýadro_baha.첫과정().실행시작주소() == 0x04001000, "ýerine_ýetir_buýruk Bitir salgy 반영");
        barla(ýadro_baha.첫과정().실행인자().length == 2 && ýadro_baha.첫과정().환경값().length == 1, "ýerine_ýetir_buýruk 인자와 환경");
        barla(!ýadro_baha.첫과정().파일서술자().열려있음(서술자), "ýerine_ýetir_buýruk 시 서술자 Ýap");
        barla(ýadro_baha.쪽관리().바이트읽기(ýadro_baha.첫과정().salgy_ýer(), 0x04002000) == 0, "빈 maglumat bölüm_baha_366e0bfa 영 ulanyşa_taýýarla");
    }

    private static void 입력시험(ýadro ýadro_baha) {
        ýadro_baha.입력관리().키누름('가');
        ýadro_baha.입력관리().쥐이동(3, -2);
        입력사건 첫사건 = ýadro_baha.입력관리().다음사건();
        입력사건 둘째사건 = ýadro_baha.입력관리().다음사건();
        barla(첫사건.사건종류() == 입력사건.종류.키누름, "자판 waka");
        barla(둘째사건.첫째값() == 3 && 둘째사건.둘째값() == -2, "쥐 ýerini_üýtget_baha waka");
    }

    private static void 하드웨어시험(호스트하드웨어 enjam_baha) {
        enjam_baha.ýaz_port_baýt(0x3f8, 0xab);
        barla(enjam_baha.포트바이트읽기(0x3f8) == 0xab, "포트 I_O 경계");
        barla(enjam_baha.직렬기록().contains("JAfgOS"), "직렬 hasaba_alyş_setir");
    }

    private static void 개입중단과서술자시험() {
        IRQ_iş_dolandyryjy iş_dolandyryjy_baha = new IRQ_iş_dolandyryjy();
        iş_dolandyryjy_baha.등록(0x21, Ammar_salgy -> Ammar_salgy + 4);
        iş_dolandyryjy_baha.mümkinçilik_ber();
        barla(iş_dolandyryjy_baha.paýla_baha(0x21, 100) == 104, "IRQ paýla_baha");
        iş_dolandyryjy_baha.işjeňlikden_aýyr();
        barla(iş_dolandyryjy_baha.paýla_baha(0x21, 100) == 100, "IRQ işjeňlikden_aýyr");

        전역서술자표 서술자표 = new 전역서술자표();
        서술자표.köplük_öňünden_kabul_edilen_baha();
        barla(서술자표.조각들().size() == 5, "전역 서술자표");
        tabşyryk_ýagdaý_bölek tabşyryk_ýagdaý = new tabşyryk_ýagdaý_bölek();
        tabşyryk_ýagdaý.특권쌓임공간설정(0x10, 0x800000);
        barla(tabşyryk_ýagdaý.영번쌓임조각() == 0x10 && tabşyryk_ýagdaý.영번쌓임주소() == 0x800000, "작업 ýagdaý_baha bölüm_baha_366e0bfa");
    }

    private static void 저장장치와통신망시험() {
        고급기술결합장치 Ammar_enjam = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.bölüm_ölçegi_üýtget];
        byte[] 읽은자료 = new byte[고급기술결합장치.bölüm_ölçegi_üýtget];
        쓸자료[17] = 42;
        Ammar_enjam.Ýaz(2, 쓸자료);
        Ammar_enjam.Oka(2, 읽은자료);
        barla(읽은자료[17] == 42, "ATA bölüm_baha_366e0bfa 읽고 Ýaz");

        kömekçi_enjam_şina_iş_dolandyryjy kömekçi_enjam = new kömekçi_enjam_şina_iş_dolandyryjy();
        kömekçi_enjam.발견(new kömekçi_enjam_şina_iş_dolandyryjy.enjam_baha(0x1022, 0x2000, 0xc000, 11));
        barla(kömekçi_enjam.tap_girizmeklik(0x1022, 0x2000) != null, "주변 enjam_baha tap_girizmeklik");

        byte[] Ethernet_kadr = new byte[34];
        Ethernet_kadr[12] = 0x08;
        Ethernet_kadr[13] = 0x00;
        Ethernet_kadr[14] = 0x45;
        barla(Tor_Gurallar.이더넷상위규약(Ethernet_kadr) == 0x0800, "이더넷 상위 ýumuş_baha_102996da");
        barla(Tor_Gurallar.상호통신망규약사판인가(Ethernet_kadr, 14), "상호통신망규약 4판");
        barla(Tor_Gurallar.인터넷검사합(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 검사합");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        ýaz_bitin_baha(첫구역, 454, 63);
        ýaz_bitin_baha(첫구역, 458, 1024);
        barla(new 기본분할영역표().Oka(첫구역).size() == 1, "öňünden_kabul_edilen_baha 분할 영역표");

        Tor_dereje dereje_baha = new Tor_dereje();
        int[] 받은수 = new int[1];
        dereje_baha.사용자자료단위등록(7, (maglumat, Bitir, dowamlylyk_baha) -> 받은수[0]++);
        byte[] kadr_indeks = new byte[14 + 20 + 8];
        kadr_indeks[12] = 0x08;
        kadr_indeks[13] = 0x00;
        kadr_indeks[14] = 0x45;
        kadr_indeks[16] = 0;
        kadr_indeks[17] = 28;
        kadr_indeks[23] = 17;
        kadr_indeks[36] = 0;
        kadr_indeks[37] = 7;
        barla(dereje_baha.이더넷받기(kadr_indeks) && 받은수[0] == 1, "ulanyjy maglumat sapak_baha paýla_baha");
    }

    private static void 화면과시계시험() {
        nyşan_ekran 화면 = new nyşan_ekran();
        화면.출력("가나\n다");
        barla(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 출력");
        sagat sagat = new sagat(100);
        for (int indeks = 0; indeks < 10; indeks++) {
            sagat.틱();
        }
        barla(sagat.지난밀리초() == 100, "sagat 틱 변환");
    }

    private static void ýaz_bitin_baha(byte[] maglumat, int 위치, int baha) {
        maglumat[위치] = (byte) baha;
        maglumat[위치 + 1] = (byte) (baha >>> 8);
        maglumat[위치 + 2] = (byte) (baha >>> 16);
        maglumat[위치 + 3] = (byte) (baha >>> 24);
    }

    private static void 짧은정수쓰기(byte[] maglumat, int 위치, int baha) {
        maglumat[위치] = (byte) baha;
        maglumat[위치 + 1] = (byte) (baha >>> 8);
    }

    private static void barla(boolean şert, String Ad) {
        if (!şert) {
            throw new AssertionError("näsazlyk_baha: " + Ad);
        }
        통과수++;
        System.out.println("통과: " + Ad);
    }
}
