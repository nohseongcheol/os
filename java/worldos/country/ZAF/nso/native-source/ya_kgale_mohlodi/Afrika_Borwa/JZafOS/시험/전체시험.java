// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Afrika_Borwa.JZafOS.시험;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Afrika_Borwa.JZafOS.기억공간.memori_molaodi;
import Afrika_Borwa.JZafOS.기억공간.letlakala_molaodi;
import Afrika_Borwa.JZafOS.입력.입력사건;
import Afrika_Borwa.JZafOS.작업.tiragalo_boleng;
import Afrika_Borwa.JZafOS.체계호출.체계호출;
import Afrika_Borwa.JZafOS.tshepedišo_ya_difaele.실행파일적재기;
import Afrika_Borwa.JZafOS.khenele.khenele;
import Afrika_Borwa.JZafOS.go_nea_ditirelo.호스트하드웨어;
import Afrika_Borwa.JZafOS.IRQ.IRQ_molaodi;
import Afrika_Borwa.JZafOS.서술자.전역서술자표;
import Afrika_Borwa.JZafOS.Bobolokelo_sedirišwa.고급기술결합장치;
import Afrika_Borwa.JZafOS.sedirišwa_boleng.pheriferale_pese_molaodi;
import Afrika_Borwa.JZafOS.Netweke_kgoboko.Netweke_Ditholosi;
import Afrika_Borwa.JZafOS.Netweke_kgoboko.Netweke_llaga;
import Afrika_Borwa.JZafOS.sedirišwa_boleng.sešupanako;
import Afrika_Borwa.JZafOS.서술자.mošomo_boemo_karolwana;
import Afrika_Borwa.JZafOS.화면.tlhaka_bontšha;
import Afrika_Borwa.JZafOS.tshepedišo_ya_difaele.기본분할영역표;

public final class 전체시험 {
    private static int 통과수;

    private 전체시험() {
    }

    public static void main(String[] 인자) {
        호스트하드웨어 sedirišwa_boleng = new 호스트하드웨어();
        khenele khenele_boleng = new khenele(sedirišwa_boleng);
        khenele_boleng.Diriša();

        기억공간시험(khenele_boleng);
        쪽관리시험(khenele_boleng);
        파일과과정시험(khenele_boleng);
        실행파일시험(khenele_boleng);
        입력시험(khenele_boleng);
        하드웨어시험(sedirišwa_boleng);
        개입중단과서술자시험();
        저장장치와통신망시험();
        화면과시계시험();

        System.out.println("JZafOS 시험 feta_boleng: " + 통과수);
    }

    private static void 기억공간시험(khenele khenele_boleng) {
        memori_molaodi molaodi_boleng = khenele_boleng.기억공간();
        int 첫주소 = molaodi_boleng.정렬할당(100, 64);
        kgonthiša((첫주소 & 63) == 0, "tsepanya_boleng aba_Bobolokelo");
        molaodi_boleng.ngwala_paete_boleng(첫주소, (byte) 0x5a);
        kgonthiša(molaodi_boleng.바이트읽기(첫주소) == (byte) 0x5a, "물리 기억공간 읽고 Ngwala");
        int 사용전 = molaodi_boleng.사용크기();
        molaodi_boleng.lokolla_Bobolokelo(첫주소);
        kgonthiša(molaodi_boleng.사용크기() < 사용전, "기억공간 lokolla_Bobolokelo");
    }

    private static void 쪽관리시험(khenele khenele_boleng) {
        letlakala_molaodi molaodi_boleng = khenele_boleng.쪽관리();
        letlakala_molaodi.atrese_sekgoba 부모공간 = molaodi_boleng.새주소공간();
        molaodi_boleng.mmepe_letlakala(부모공간, 0x1000, true);
        molaodi_boleng.ngwala_paete_boleng(부모공간, 0x1010, (byte) 7);
        letlakala_molaodi.atrese_sekgoba ngwana_sekgoba = molaodi_boleng.쓰기시복사복제(부모공간);
        molaodi_boleng.ngwala_paete_boleng(ngwana_sekgoba, 0x1010, (byte) 9);
        kgonthiša(molaodi_boleng.바이트읽기(부모공간, 0x1010) == 7, "Ngwala 시 kopiša_boleng 부모 격리");
        kgonthiša(molaodi_boleng.바이트읽기(ngwana_sekgoba, 0x1010) == 9, "Ngwala 시 kopiša_boleng ngwana_boleng Ngwala");
    }

    private static void 파일과과정시험(khenele khenele_boleng) {
        byte[] Diteng_boleng = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        khenele_boleng.tshepedišo_ya_difaele().파일추가("시험", Diteng_boleng);
        tiragalo_boleng 부모 = khenele_boleng.첫과정();
        체계호출 호출 = khenele_boleng.체계호출();
        int 서술자 = 호출.Bula(부모, "/시험", 체계호출.balwago_fela_folaga);
        kgonthiša(서술자 >= 3, "Faele Bula");

        byte[] 받을곳 = new byte[Diteng_boleng.length];
        kgonthiša(호출.Bala(부모, 서술자, 받을곳, 받을곳.length) == Diteng_boleng.length, "Faele Bala");
        kgonthiša(Arrays.equals(Diteng_boleng, 받을곳), "Faele Diteng_boleng");
        kgonthiša(호출.위치옮기기(부모, 서술자, 0, 체계호출.Nyaka_Thomišo) == 0, "Faele 위치 šuthiša_boleng");

        int 복제서술자 = 호출.서술자복제(부모, 서술자);
        kgonthiša(복제서술자 >= 0, "서술자 복제");
        tiragalo_boleng ngwana_boleng = 호출.과정복제(부모);
        kgonthiša(ngwana_boleng.sešupi_boleng() != 부모.sešupi_boleng(), "tiragalo_boleng sešupi_boleng 분리");
        kgonthiša(ngwana_boleng.부모식별자() == 부모.sešupi_boleng(), "부모 tiragalo_boleng sešupi_boleng");
        kgonthiša(호출.Tswalela(ngwana_boleng, 서술자) == 0 && 부모.파일서술자().열려있음(서술자), "ngwana_boleng Tswalela 격리");

        int 이전끝 = 호출.프로그램끝늘리기(부모, 8192);
        kgonthiša(이전끝 == 0x06000000, "tirišo_f5044b9b 끝 늘리기");
        kgonthiša(부모.프로그램끝() == 0x06002000, "tirišo_f5044b9b 끝 반영");
        kgonthiša(ngwana_boleng.프로그램끝() == 0x06000000, "과정별 tirišo_f5044b9b 끝 격리");

        ngwana_boleng.Etšwa_tirišo(7);
        kgonthiša(호출.자식기다리기(부모, ngwana_boleng.sešupi_boleng(), false) == (7 << 8), "ngwana_boleng Etšwa_tirišo 기다리기");
        kgonthiša(호출.접근가능("시험", 1) == -13, "phethagatša_taelo tumelelo_boleng 거부");
        kgonthiša(호출.mošomiši_sešupi() == 0 && 호출.sehlopha_sešupi() == 0, "사용자와 무리 sešupi_boleng");
        kgonthiša("/".equals(호출.현재작업목록(2)) && 호출.fetogela_lenaneo_la_ditiro("/") == 0, "현재 작업 go_tsenya_tshedimošo_Lenaneo");
        kgonthiša(호출.단말인가(부모, 1), "표준 출력 단말");
        kgonthiša("JZafOS".equals(호출.체계정보().lenaneo_leina()), "tshepedišotirišo_boleng msinfo32_exe");
    }

    private static void 실행파일시험(khenele khenele_boleng) {
        byte[] data = new byte[92];
        data[0] = 0x7f;
        data[1] = 'E';
        data[2] = 'L';
        data[3] = 'F';
        data[4] = 1;
        data[5] = 1;
        ngwala_palotlalo_boleng(data, 24, 0x04001000);
        ngwala_palotlalo_boleng(data, 32, 52);
        짧은정수쓰기(data, 46, 40);
        짧은정수쓰기(data, 48, 1);
        ngwala_palotlalo_boleng(data, 56, 8);
        ngwala_palotlalo_boleng(data, 60, 2);
        ngwala_palotlalo_boleng(data, 64, 0x04002000);
        ngwala_palotlalo_boleng(data, 72, 64);

        실행파일적재기.seswantšho seswantšho_boleng = new 실행파일적재기().검사(data);
        kgonthiša(seswantšho_boleng.Thomišo_atrese() == 0x04001000, "ELF Diriša atrese");
        kgonthiša(seswantšho_boleng.구역들().size() == 1 && seswantšho_boleng.구역들().get(0).종류() == 8, "ELF 빈 data karolo_boleng");
        int 서술자 = khenele_boleng.체계호출().Bula(khenele_boleng.첫과정(), "시험", 체계호출.balwago_fela_folaga);
        kgonthiša(khenele_boleng.체계호출().faele_taolo(khenele_boleng.첫과정(), 서술자, 2, 1) == 0, "phethagatša_taelo 시 Tswalela Dipeakanyo");
        kgonthiša(khenele_boleng.체계호출().phethagatša_taelo(khenele_boleng.첫과정(), data, new String[] {"시험", "값"}, new String[] {"Polelo=한국어"}) == 0, "ELF phethagatša_taelo seswantšho_boleng 적재");
        kgonthiša(khenele_boleng.첫과정().실행시작주소() == 0x04001000, "phethagatša_taelo Diriša atrese 반영");
        kgonthiša(khenele_boleng.첫과정().실행인자().length == 2 && khenele_boleng.첫과정().환경값().length == 1, "phethagatša_taelo 인자와 환경");
        kgonthiša(!khenele_boleng.첫과정().파일서술자().열려있음(서술자), "phethagatša_taelo 시 서술자 Tswalela");
        kgonthiša(khenele_boleng.쪽관리().바이트읽기(khenele_boleng.첫과정().atrese_sekgoba(), 0x04002000) == 0, "빈 data karolo_boleng 영 thomiša");
    }

    private static void 입력시험(khenele khenele_boleng) {
        khenele_boleng.입력관리().키누름('가');
        khenele_boleng.입력관리().쥐이동(3, -2);
        입력사건 첫사건 = khenele_boleng.입력관리().다음사건();
        입력사건 둘째사건 = khenele_boleng.입력관리().다음사건();
        kgonthiša(첫사건.사건종류() == 입력사건.종류.키누름, "자판 tiragalo");
        kgonthiša(둘째사건.첫째값() == 3 && 둘째사건.둘째값() == -2, "쥐 šuthiša_boleng tiragalo");
    }

    private static void 하드웨어시험(호스트하드웨어 sedirišwa_boleng) {
        sedirišwa_boleng.ngwala_phote_paete(0x3f8, 0xab);
        kgonthiša(sedirišwa_boleng.포트바이트읽기(0x3f8) == 0xab, "포트 I_O 경계");
        kgonthiša(sedirišwa_boleng.직렬기록().contains("JZafOS"), "직렬 pego_rei");
    }

    private static void 개입중단과서술자시험() {
        IRQ_molaodi molaodi_boleng = new IRQ_molaodi();
        molaodi_boleng.ngwadiša_go_tsenya_tshedimošo(0x21, Bobolokelo_atrese -> Bobolokelo_atrese + 4);
        molaodi_boleng.bula();
        kgonthiša(molaodi_boleng.aba_boleng(0x21, 100) == 104, "IRQ aba_boleng");
        molaodi_boleng.dirolla();
        kgonthiša(molaodi_boleng.aba_boleng(0x21, 100) == 100, "IRQ dirolla");

        전역서술자표 서술자표 = new 전역서술자표();
        서술자표.sehlopha_setsenywa_sa_tirelwa();
        kgonthiša(서술자표.조각들().size() == 5, "전역 서술자표");
        mošomo_boemo_karolwana mošomo_boemo = new mošomo_boemo_karolwana();
        mošomo_boemo.특권쌓임공간설정(0x10, 0x800000);
        kgonthiša(mošomo_boemo.영번쌓임조각() == 0x10 && mošomo_boemo.영번쌓임주소() == 0x800000, "작업 boemo_boleng karolo_boleng");
    }

    private static void 저장장치와통신망시험() {
        고급기술결합장치 Bobolokelo_sedirišwa = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.karolo_bogolo];
        byte[] 읽은자료 = new byte[고급기술결합장치.karolo_bogolo];
        쓸자료[17] = 42;
        Bobolokelo_sedirišwa.Ngwala(2, 쓸자료);
        Bobolokelo_sedirišwa.Bala(2, 읽은자료);
        kgonthiša(읽은자료[17] == 42, "ATA karolo_boleng 읽고 Ngwala");

        pheriferale_pese_molaodi pheriferale = new pheriferale_pese_molaodi();
        pheriferale.발견(new pheriferale_pese_molaodi.sedirišwa_boleng(0x1022, 0x2000, 0xc000, 11));
        kgonthiša(pheriferale.hwetša_go_tsenya_tshedimošo(0x1022, 0x2000) != null, "주변 sedirišwa_boleng hwetša_go_tsenya_tshedimošo");

        byte[] Ethenete_freime = new byte[34];
        Ethenete_freime[12] = 0x08;
        Ethenete_freime[13] = 0x00;
        Ethenete_freime[14] = 0x45;
        kgonthiša(Netweke_Ditholosi.이더넷상위규약(Ethenete_freime) == 0x0800, "이더넷 상위 taba_boleng");
        kgonthiša(Netweke_Ditholosi.상호통신망규약사판인가(Ethenete_freime, 14), "상호통신망규약 4판");
        kgonthiša(Netweke_Ditholosi.인터넷검사합(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 검사합");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        ngwala_palotlalo_boleng(첫구역, 454, 63);
        ngwala_palotlalo_boleng(첫구역, 458, 1024);
        kgonthiša(new 기본분할영역표().Bala(첫구역).size() == 1, "setsenywa_sa_tirelwa 분할 영역표");

        Netweke_llaga llaga_boleng = new Netweke_llaga();
        int[] 받은수 = new int[1];
        llaga_boleng.ngwadiša_mošomiši_data_thutišo(7, (data, Diriša, botelele_boleng) -> 받은수[0]++);
        byte[] freime_lokela = new byte[14 + 20 + 8];
        freime_lokela[12] = 0x08;
        freime_lokela[13] = 0x00;
        freime_lokela[14] = 0x45;
        freime_lokela[16] = 0;
        freime_lokela[17] = 28;
        freime_lokela[23] = 17;
        freime_lokela[36] = 0;
        freime_lokela[37] = 7;
        kgonthiša(llaga_boleng.이더넷받기(freime_lokela) && 받은수[0] == 1, "mošomiši data thutišo_boleng aba_boleng");
    }

    private static void 화면과시계시험() {
        tlhaka_bontšha 화면 = new tlhaka_bontšha();
        화면.출력("가나\n다");
        kgonthiša(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 출력");
        sešupanako sešupanako = new sešupanako(100);
        for (int lokela = 0; lokela < 10; lokela++) {
            sešupanako.틱();
        }
        kgonthiša(sešupanako.지난밀리초() == 100, "sešupanako 틱 변환");
    }

    private static void ngwala_palotlalo_boleng(byte[] data, int 위치, int boleng) {
        data[위치] = (byte) boleng;
        data[위치 + 1] = (byte) (boleng >>> 8);
        data[위치 + 2] = (byte) (boleng >>> 16);
        data[위치 + 3] = (byte) (boleng >>> 24);
    }

    private static void 짧은정수쓰기(byte[] data, int 위치, int boleng) {
        data[위치] = (byte) boleng;
        data[위치 + 1] = (byte) (boleng >>> 8);
    }

    private static void kgonthiša(boolean seemo, String Leina) {
        if (!seemo) {
            throw new AssertionError("go_palelwa_boleng: " + Leina);
        }
        통과수++;
        System.out.println("feta_boleng: " + Leina);
    }
}
