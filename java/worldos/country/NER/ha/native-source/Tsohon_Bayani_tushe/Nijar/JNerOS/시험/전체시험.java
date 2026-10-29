// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nijar.JNerOS.시험;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Nijar.JNerOS.기억공간.Mahardatar_kwamfuta_Manaja;
import Nijar.JNerOS.기억공간.shafi_Manaja;
import Nijar.JNerOS.입력.입력사건;
import Nijar.JNerOS.작업.haryar_aikin_na_ura_Daraja;
import Nijar.JNerOS.체계호출.체계호출;
import Nijar.JNerOS.tsarin_fayil_a_kwamfuta.실행파일적재기;
import Nijar.JNerOS.Kwara.Kwara;
import Nijar.JNerOS.sauka.sauka_kayan_haɗi_na_kwamfuta;
import Nijar.JNerOS.IRQ.IRQ_Manaja;
import Nijar.JNerOS.서술자.전역서술자표;
import Nijar.JNerOS.Wurin_adana_na_ura.고급기술결합장치;
import Nijar.JNerOS.na_ura_Daraja.yan_hadin_kwamfuta_mashigi_Manaja;
import Nijar.JNerOS.Hanyar_sadarwa_tara.Hanyar_sadarwa_Kaya;
import Nijar.JNerOS.Hanyar_sadarwa_tara.Hanyar_sadarwa_Tsarkiya;
import Nijar.JNerOS.na_ura_Daraja.agogo;
import Nijar.JNerOS.서술자.aiki_Matsayi_yanki;
import Nijar.JNerOS.화면.Harafi_Nuna;
import Nijar.JNerOS.tsarin_fayil_a_kwamfuta.기본분할영역표;

public final class 전체시험 {
    private static int 통과수;

    private 전체시험() {
    }

    public static void main(String[] maaunin_Tubalin_aiki) {
        sauka_kayan_haɗi_na_kwamfuta na_ura_Daraja = new sauka_kayan_haɗi_na_kwamfuta();
        Kwara Kwara_Daraja = new Kwara(na_ura_Daraja);
        Kwara_Daraja.Tafiyar_da();

        기억공간시험(Kwara_Daraja);
        쪽관리시험(Kwara_Daraja);
        파일과과정시험(Kwara_Daraja);
        실행파일시험(Kwara_Daraja);
        입력시험(Kwara_Daraja);
        하드웨어시험(na_ura_Daraja);
        개입중단과서술자시험();
        저장장치와통신망시험();
        화면과시계시험();

        System.out.println("JNerOS 시험 통과: " + 통과수);
    }

    private static void 기억공간시험(Kwara Kwara_Daraja) {
        Mahardatar_kwamfuta_Manaja Manaja_Daraja = Kwara_Daraja.기억공간();
        int 첫주소 = Manaja_Daraja.정렬할당(100, 64);
        Tabbatar_da((첫주소 & 63) == 0, "Daidaita_Daraja kasafta_Wurin_adana");
        Manaja_Daraja.Rubuta_bayit_Daraja(첫주소, (byte) 0x5a);
        Tabbatar_da(Manaja_Daraja.바이트읽기(첫주소) == (byte) 0x5a, "물리 기억공간 읽고 Yi_Rubutu");
        int 사용전 = Manaja_Daraja.사용크기();
        Manaja_Daraja.saka_Wurin_adana(첫주소);
        Tabbatar_da(Manaja_Daraja.사용크기() < 사용전, "기억공간 saka_Wurin_adana");
    }

    private static void 쪽관리시험(Kwara Kwara_Daraja) {
        shafi_Manaja Manaja_Daraja = Kwara_Daraja.쪽관리();
        shafi_Manaja.imel_wuri 부모공간 = Manaja_Daraja.새주소공간();
        Manaja_Daraja.taswira_shafi(부모공간, 0x1000, true);
        Manaja_Daraja.Rubuta_bayit_Daraja(부모공간, 0x1010, (byte) 7);
        shafi_Manaja.imel_wuri yaro_wuri = Manaja_Daraja.쓰기시복사복제(부모공간);
        Manaja_Daraja.Rubuta_bayit_Daraja(yaro_wuri, 0x1010, (byte) 9);
        Tabbatar_da(Manaja_Daraja.바이트읽기(부모공간, 0x1010) == 7, "Yi_Rubutu 시 Kwafi_Daraja 부모 격리");
        Tabbatar_da(Manaja_Daraja.바이트읽기(yaro_wuri, 0x1010) == 9, "Yi_Rubutu 시 Kwafi_Daraja yaro_Daraja Yi_Rubutu");
    }

    private static void 파일과과정시험(Kwara Kwara_Daraja) {
        byte[] kunshiya_Daraja = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        Kwara_Daraja.tsarin_fayil_a_kwamfuta().파일추가("시험", kunshiya_Daraja);
        haryar_aikin_na_ura_Daraja 부모 = Kwara_Daraja.첫과정();
        체계호출 호출 = Kwara_Daraja.체계호출();
        int 서술자 = 호출.Buɗe(부모, "/시험", 체계호출.karanta_kawai_Tuta);
        Tabbatar_da(서술자 >= 3, "Fayil Buɗe");

        byte[] 받을곳 = new byte[kunshiya_Daraja.length];
        Tabbatar_da(호출.Yi_Karatu(부모, 서술자, 받을곳, 받을곳.length) == kunshiya_Daraja.length, "Fayil Yi_Karatu");
        Tabbatar_da(Arrays.equals(kunshiya_Daraja, 받을곳), "Fayil kunshiya_Daraja");
        Tabbatar_da(호출.위치옮기기(부모, 서술자, 0, 체계호출.Leko_Fara) == 0, "Fayil 위치 Matsar_da_Daraja");

        int 복제서술자 = 호출.서술자복제(부모, 서술자);
        Tabbatar_da(복제서술자 >= 0, "서술자 복제");
        haryar_aikin_na_ura_Daraja yaro_Daraja = 호출.과정복제(부모);
        Tabbatar_da(yaro_Daraja.mai_ganewa_Daraja() != 부모.mai_ganewa_Daraja(), "haryar_aikin_na_ura_Daraja mai_ganewa_Daraja 분리");
        Tabbatar_da(yaro_Daraja.부모식별자() == 부모.mai_ganewa_Daraja(), "부모 haryar_aikin_na_ura_Daraja mai_ganewa_Daraja");
        Tabbatar_da(호출.Rufe(yaro_Daraja, 서술자) == 0 && 부모.파일서술자().kimiyar_bayanai_buɗe(서술자), "yaro_Daraja Rufe 격리");

        int 이전끝 = 호출.프로그램끝늘리기(부모, 8192);
        Tabbatar_da(이전끝 == 0x06000000, "Shiri_f5044b9b 끝 늘리기");
        Tabbatar_da(부모.프로그램끝() == 0x06002000, "Shiri_f5044b9b 끝 반영");
        Tabbatar_da(yaro_Daraja.프로그램끝() == 0x06000000, "과정별 Shiri_f5044b9b 끝 격리");

        yaro_Daraja.Mafita_Shiri(7);
        Tabbatar_da(호출.자식기다리기(부모, yaro_Daraja.mai_ganewa_Daraja(), false) == (7 << 8), "yaro_Daraja Mafita_Shiri 기다리기");
        Tabbatar_da(호출.접근가능("시험", 1) == -13, "gudanar_Umarni izini_Daraja kore_Daraja");
        Tabbatar_da(호출.Mai_anfani_da_kwamfuta_mai_ganewa() == 0 && 호출.gungu_mai_ganewa() == 0, "사용자와 무리 mai_ganewa_Daraja");
        Tabbatar_da("/".equals(호출.현재작업목록(2)) && 호출.Sauya_Jerin_tsarin_aiki("/") == 0, "현재 작업 Mashigar_bayanai_Jeri");
        Tabbatar_da(호출.단말인가(부모, 1), "표준 출력 단말");
        Tabbatar_da("JNerOS".equals(호출.체계정보().na_ura_Suna()), "OS_Daraja msinfo32_exe");
    }

    private static void 실행파일시험(Kwara Kwara_Daraja) {
        byte[] Tarin_bayani = new byte[92];
        Tarin_bayani[0] = 0x7f;
        Tarin_bayani[1] = 'E';
        Tarin_bayani[2] = 'L';
        Tarin_bayani[3] = 'F';
        Tarin_bayani[4] = 1;
        Tarin_bayani[5] = 1;
        Rubuta_Lamba_mara_Daraja(Tarin_bayani, 24, 0x04001000);
        Rubuta_Lamba_mara_Daraja(Tarin_bayani, 32, 52);
        짧은정수쓰기(Tarin_bayani, 46, 40);
        짧은정수쓰기(Tarin_bayani, 48, 1);
        Rubuta_Lamba_mara_Daraja(Tarin_bayani, 56, 8);
        Rubuta_Lamba_mara_Daraja(Tarin_bayani, 60, 2);
        Rubuta_Lamba_mara_Daraja(Tarin_bayani, 64, 0x04002000);
        Rubuta_Lamba_mara_Daraja(Tarin_bayani, 72, 64);

        실행파일적재기.Hoto Hoto_Daraja = new 실행파일적재기().검사(Tarin_bayani);
        Tabbatar_da(Hoto_Daraja.Fara_imel() == 0x04001000, "ELF Tafiyar_da imel");
        Tabbatar_da(Hoto_Daraja.구역들().size() == 1 && Hoto_Daraja.구역들().get(0).종류() == 8, "ELF 빈 Tarin_bayani Sashi_Daraja");
        int 서술자 = Kwara_Daraja.체계호출().Buɗe(Kwara_Daraja.첫과정(), "시험", 체계호출.karanta_kawai_Tuta);
        Tabbatar_da(Kwara_Daraja.체계호출().Fayil_masarrafa(Kwara_Daraja.첫과정(), 서술자, 2, 1) == 0, "gudanar_Umarni 시 Rufe Saituna");
        Tabbatar_da(Kwara_Daraja.체계호출().gudanar_Umarni(Kwara_Daraja.첫과정(), Tarin_bayani, new String[] {"시험", "값"}, new String[] {"yare=한국어"}) == 0, "ELF gudanar_Umarni Hoto_Daraja 적재");
        Tabbatar_da(Kwara_Daraja.첫과정().실행시작주소() == 0x04001000, "gudanar_Umarni Tafiyar_da imel 반영");
        Tabbatar_da(Kwara_Daraja.첫과정().실행인자().length == 2 && Kwara_Daraja.첫과정().환경값().length == 1, "gudanar_Umarni 인자와 환경");
        Tabbatar_da(!Kwara_Daraja.첫과정().파일서술자().kimiyar_bayanai_buɗe(서술자), "gudanar_Umarni 시 서술자 Rufe");
        Tabbatar_da(Kwara_Daraja.쪽관리().바이트읽기(Kwara_Daraja.첫과정().imel_wuri(), 0x04002000) == 0, "빈 Tarin_bayani Sashi_Daraja 영 Farko");
    }

    private static void 입력시험(Kwara Kwara_Daraja) {
        Kwara_Daraja.입력관리().키누름('가');
        Kwara_Daraja.입력관리().쥐이동(3, -2);
        입력사건 첫사건 = Kwara_Daraja.입력관리().다음사건();
        입력사건 둘째사건 = Kwara_Daraja.입력관리().다음사건();
        Tabbatar_da(첫사건.사건종류() == 입력사건.종류.키누름, "자판 Faruwa");
        Tabbatar_da(둘째사건.첫째값() == 3 && 둘째사건.둘째값() == -2, "쥐 Matsar_da_Daraja Faruwa");
    }

    private static void 하드웨어시험(sauka_kayan_haɗi_na_kwamfuta na_ura_Daraja) {
        na_ura_Daraja.Rubuta_fot_bayit(0x3f8, 0xab);
        Tabbatar_da(na_ura_Daraja.포트바이트읽기(0x3f8) == 0xab, "kayan_haɗi_na_kwamfuta_fot I_O 경계");
        Tabbatar_da(na_ura_Daraja.직렬기록().contains("JNerOS"), "직렬 logu_naɗa");
    }

    private static void 개입중단과서술자시험() {
        IRQ_Manaja Manaja_Daraja = new IRQ_Manaja();
        Manaja_Daraja.등록(0x21, Wurin_adana_imel -> Wurin_adana_imel + 4);
        Manaja_Daraja.kunna();
        Tabbatar_da(Manaja_Daraja.rarraba_Daraja(0x21, 100) == 104, "IRQ rarraba_Daraja");
        Manaja_Daraja.nakasa();
        Tabbatar_da(Manaja_Daraja.rarraba_Daraja(0x21, 100) == 100, "IRQ nakasa");

        전역서술자표 서술자표 = new 전역서술자표();
        서술자표.zubi_Tanadaddiyar_daraja();
        Tabbatar_da(서술자표.조각들().size() == 5, "전역 서술자표");
        aiki_Matsayi_yanki aiki_Matsayi = new aiki_Matsayi_yanki();
        aiki_Matsayi.특권쌓임공간설정(0x10, 0x800000);
        Tabbatar_da(aiki_Matsayi.영번쌓임조각() == 0x10 && aiki_Matsayi.영번쌓임주소() == 0x800000, "작업 Matsayi_Daraja Sashi_Daraja");
    }

    private static void 저장장치와통신망시험() {
        고급기술결합장치 Wurin_adana_na_ura = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.Sashi_girma];
        byte[] 읽은자료 = new byte[고급기술결합장치.Sashi_girma];
        쓸자료[17] = 42;
        Wurin_adana_na_ura.Yi_Rubutu(2, 쓸자료);
        Wurin_adana_na_ura.Yi_Karatu(2, 읽은자료);
        Tabbatar_da(읽은자료[17] == 42, "ATA Sashi_Daraja 읽고 Yi_Rubutu");

        yan_hadin_kwamfuta_mashigi_Manaja yan_hadin_kwamfuta = new yan_hadin_kwamfuta_mashigi_Manaja();
        yan_hadin_kwamfuta.발견(new yan_hadin_kwamfuta_mashigi_Manaja.na_ura_Daraja(0x1022, 0x2000, 0xc000, 11));
        Tabbatar_da(yan_hadin_kwamfuta.nema_Mashigar_bayanai(0x1022, 0x2000) != null, "주변 na_ura_Daraja nema_Mashigar_bayanai");

        byte[] Wayar_kwamfuta_ta_yanar_gizo_allo = new byte[34];
        Wayar_kwamfuta_ta_yanar_gizo_allo[12] = 0x08;
        Wayar_kwamfuta_ta_yanar_gizo_allo[13] = 0x00;
        Wayar_kwamfuta_ta_yanar_gizo_allo[14] = 0x45;
        Tabbatar_da(Hanyar_sadarwa_Kaya.이더넷상위규약(Wayar_kwamfuta_ta_yanar_gizo_allo) == 0x0800, "이더넷 상위 Kes_Daraja");
        Tabbatar_da(Hanyar_sadarwa_Kaya.상호통신망규약사판인가(Wayar_kwamfuta_ta_yanar_gizo_allo, 14), "상호통신망규약 4판");
        Tabbatar_da(Hanyar_sadarwa_Kaya.Intanet_checksum(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 checksum");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        Rubuta_Lamba_mara_Daraja(첫구역, 454, 63);
        Rubuta_Lamba_mara_Daraja(첫구역, 458, 1024);
        Tabbatar_da(new 기본분할영역표().Yi_Karatu(첫구역).size() == 1, "Tanadaddiyar_daraja 분할 영역표");

        Hanyar_sadarwa_Tsarkiya Tsarkiya_Daraja = new Hanyar_sadarwa_Tsarkiya();
        int[] 받은수 = new int[1];
        Tsarkiya_Daraja.사용자자료단위등록(7, (Tarin_bayani, Tafiyar_da, Tsawo_Daraja) -> 받은수[0]++);
        byte[] allo_Indes = new byte[14 + 20 + 8];
        allo_Indes[12] = 0x08;
        allo_Indes[13] = 0x00;
        allo_Indes[14] = 0x45;
        allo_Indes[16] = 0;
        allo_Indes[17] = 28;
        allo_Indes[23] = 17;
        allo_Indes[36] = 0;
        allo_Indes[37] = 7;
        Tabbatar_da(Tsarkiya_Daraja.이더넷받기(allo_Indes) && 받은수[0] == 1, "Mai_anfani_da_kwamfuta Tarin_bayani darasi_Daraja rarraba_Daraja");
    }

    private static void 화면과시계시험() {
        Harafi_Nuna 화면 = new Harafi_Nuna();
        화면.출력("가나\n다");
        Tabbatar_da(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 출력");
        agogo agogo = new agogo(100);
        for (int Indes = 0; Indes < 10; Indes++) {
            agogo.틱();
        }
        Tabbatar_da(agogo.지난밀리초() == 100, "agogo 틱 변환");
    }

    private static void Rubuta_Lamba_mara_Daraja(byte[] Tarin_bayani, int 위치, int Daraja) {
        Tarin_bayani[위치] = (byte) Daraja;
        Tarin_bayani[위치 + 1] = (byte) (Daraja >>> 8);
        Tarin_bayani[위치 + 2] = (byte) (Daraja >>> 16);
        Tarin_bayani[위치 + 3] = (byte) (Daraja >>> 24);
    }

    private static void 짧은정수쓰기(byte[] Tarin_bayani, int 위치, int Daraja) {
        Tarin_bayani[위치] = (byte) Daraja;
        Tarin_bayani[위치 + 1] = (byte) (Daraja >>> 8);
    }

    private static void Tabbatar_da(boolean Yanayi, String Suna) {
        if (!Yanayi) {
            throw new AssertionError("Kasa_aiki_Daraja: " + Suna);
        }
        통과수++;
        System.out.println("통과: " + Suna);
    }
}
