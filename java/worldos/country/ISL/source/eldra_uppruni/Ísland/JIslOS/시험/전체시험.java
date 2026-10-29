// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ísland.JIslOS.시험;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Ísland.JIslOS.기억공간.Minni_stjórnandi;
import Ísland.JIslOS.기억공간.síða_stjórnandi;
import Ísland.JIslOS.입력.입력사건;
import Ísland.JIslOS.작업.Ferli_VALUE;
import Ísland.JIslOS.체계호출.체계호출;
import Ísland.JIslOS.skrárkerfi.실행파일적재기;
import Ísland.JIslOS.kjarni.kjarni;
import Ísland.JIslOS.hýsa.호스트하드웨어;
import Ísland.JIslOS.IRQ.IRQ_stjórnandi;
import Ísland.JIslOS.서술자.전역서술자표;
import Ísland.JIslOS.geymsla_tæki.고급기술결합장치;
import Ísland.JIslOS.tæki_VALUE.aukabúnaður_tengibraut_stjórnandi;
import Ísland.JIslOS.Net_bunki.Net_Verkfæri;
import Ísland.JIslOS.Net_bunki.Net_lag;
import Ísland.JIslOS.tæki_VALUE.klukka;
import Ísland.JIslOS.서술자.verk_staða_hluti;
import Ísland.JIslOS.화면.stafur_birta;
import Ísland.JIslOS.skrárkerfi.기본분할영역표;

public final class 전체시험 {
    private static int senda_COUNT;

    private 전체시험() {
    }

    public static void main(String[] færibreyta_frumbreyta) {
        호스트하드웨어 tæki_VALUE = new 호스트하드웨어();
        kjarni kjarni_VALUE = new kjarni(tæki_VALUE);
        kjarni_VALUE.Keyra_2();

        기억공간시험(kjarni_VALUE);
        쪽관리시험(kjarni_VALUE);
        파일과과정시험(kjarni_VALUE);
        실행파일시험(kjarni_VALUE);
        입력시험(kjarni_VALUE);
        하드웨어시험(tæki_VALUE);
        개입중단과서술자시험();
        저장장치와통신망시험();
        화면과시계시험();

        System.out.println("JIslOS 시험 senda_VALUE: " + senda_COUNT);
    }

    private static void 기억공간시험(kjarni kjarni_VALUE) {
        Minni_stjórnandi stjórnandi_VALUE = kjarni_VALUE.기억공간();
        int 첫주소 = stjórnandi_VALUE.정렬할당(100, 64);
        sannprófa((첫주소 & 63) == 0, "stilla_VALUE úthluta_geymsla");
        stjórnandi_VALUE.skrifa_bæti_VALUE(첫주소, (byte) 0x5a);
        sannprófa(stjórnandi_VALUE.바이트읽기(첫주소) == (byte) 0x5a, "물리 기억공간 읽고 Skrift");
        int 사용전 = stjórnandi_VALUE.사용크기();
        stjórnandi_VALUE.losa_geymsla(첫주소);
        sannprófa(stjórnandi_VALUE.사용크기() < 사용전, "기억공간 losa_geymsla");
    }

    private static void 쪽관리시험(kjarni kjarni_VALUE) {
        síða_stjórnandi stjórnandi_VALUE = kjarni_VALUE.쪽관리();
        síða_stjórnandi.slóð_svæði yfireining_svæði = stjórnandi_VALUE.새주소공간();
        stjórnandi_VALUE.MAP_síða(yfireining_svæði, 0x1000, true);
        stjórnandi_VALUE.skrifa_bæti_VALUE(yfireining_svæði, 0x1010, (byte) 7);
        síða_stjórnandi.slóð_svæði barn_svæði = stjórnandi_VALUE.쓰기시복사복제(yfireining_svæði);
        stjórnandi_VALUE.skrifa_bæti_VALUE(barn_svæði, 0x1010, (byte) 9);
        sannprófa(stjórnandi_VALUE.바이트읽기(yfireining_svæði, 0x1010) == 7, "Skrift 시 afrita_VALUE yfireining_VALUE 격리");
        sannprófa(stjórnandi_VALUE.바이트읽기(barn_svæði, 0x1010) == 9, "Skrift 시 afrita_VALUE barn_VALUE Skrift");
    }

    private static void 파일과과정시험(kjarni kjarni_VALUE) {
        byte[] Efni_VALUE = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        kjarni_VALUE.skrárkerfi().파일추가("시험", Efni_VALUE);
        Ferli_VALUE yfireining_VALUE = kjarni_VALUE.첫과정();
        체계호출 호출 = kjarni_VALUE.체계호출();
        int 서술자 = 호출.Opna(yfireining_VALUE, "/시험", 체계호출.skrifvarið_flagg);
        sannprófa(서술자 >= 3, "Skrá Opna");

        byte[] 받을곳 = new byte[Efni_VALUE.length];
        sannprófa(호출.Lestur(yfireining_VALUE, 서술자, 받을곳, 받을곳.length) == Efni_VALUE.length, "Skrá Lestur");
        sannprófa(Arrays.equals(Efni_VALUE, 받을곳), "Skrá Efni_VALUE");
        sannprófa(호출.færa_staða(yfireining_VALUE, 서술자, 0, 체계호출.Leit_Opna) == 0, "Skrá Staðsetning færa_VALUE");

        int 복제서술자 = 호출.서술자복제(yfireining_VALUE, 서술자);
        sannprófa(복제서술자 >= 0, "서술자 복제");
        Ferli_VALUE barn_VALUE = 호출.과정복제(yfireining_VALUE);
        sannprófa(barn_VALUE.auðkenni_VALUE() != yfireining_VALUE.auðkenni_VALUE(), "Ferli_VALUE auðkenni_VALUE 분리");
        sannprófa(barn_VALUE.yfireining_auðkenni() == yfireining_VALUE.auðkenni_VALUE(), "yfireining_VALUE Ferli_VALUE auðkenni_VALUE");
        sannprófa(호출.Loka(barn_VALUE, 서술자) == 0 && yfireining_VALUE.파일서술자().upplýsingatækni_opið(서술자), "barn_VALUE Loka 격리");

        int 이전끝 = 호출.hækkun_forrit_hlé(yfireining_VALUE, 8192);
        sannprófa(이전끝 == 0x06000000, "forrit_f5044b9b 끝 늘리기");
        sannprófa(yfireining_VALUE.forrit_hlé() == 0x06002000, "forrit_f5044b9b 끝 반영");
        sannprófa(barn_VALUE.forrit_hlé() == 0x06000000, "과정별 forrit_f5044b9b 끝 격리");

        barn_VALUE.loka_forrit(7);
        sannprófa(호출.자식기다리기(yfireining_VALUE, barn_VALUE.auðkenni_VALUE(), false) == (7 << 8), "barn_VALUE loka_forrit 기다리기");
        sannprófa(호출.접근가능("시험", 1) == -13, "keyra_skipun leyfi_VALUE hafna_VALUE");
        sannprófa(호출.notandi_auðkenni() == 0 && 호출.Hópur_auðkenni() == 0, "사용자와 무리 auðkenni_VALUE");
        sannprófa("/".equals(호출.현재작업목록(2)) && 호출.SWITCH_verklisti("/") == 0, "현재 작업 færsla_Listi");
        sannprófa(호출.upplýsingatækni_Endastöð(yfireining_VALUE, 1), "표준 úttak 단말");
        sannprófa("JIslOS".equals(호출.체계정보().kerfi_heiti()), "stýrikerfi_VALUE msinfo32_exe");
    }

    private static void 실행파일시험(kjarni kjarni_VALUE) {
        byte[] gögn = new byte[92];
        gögn[0] = 0x7f;
        gögn[1] = 'E';
        gögn[2] = 'L';
        gögn[3] = 'F';
        gögn[4] = 1;
        gögn[5] = 1;
        skrifa_heiltala_VALUE(gögn, 24, 0x04001000);
        skrifa_heiltala_VALUE(gögn, 32, 52);
        짧은정수쓰기(gögn, 46, 40);
        짧은정수쓰기(gögn, 48, 1);
        skrifa_heiltala_VALUE(gögn, 56, 8);
        skrifa_heiltala_VALUE(gögn, 60, 2);
        skrifa_heiltala_VALUE(gögn, 64, 0x04002000);
        skrifa_heiltala_VALUE(gögn, 72, 64);

        실행파일적재기.mynd mynd_VALUE = new 실행파일적재기().검사(gögn);
        sannprófa(mynd_VALUE.Opna_slóð() == 0x04001000, "ELF Keyra_2 slóð");
        sannprófa(mynd_VALUE.구역들().size() == 1 && mynd_VALUE.구역들().get(0).종류() == 8, "ELF 빈 gögn hluti_VALUE");
        int 서술자 = kjarni_VALUE.체계호출().Opna(kjarni_VALUE.첫과정(), "시험", 체계호출.skrifvarið_flagg);
        sannprófa(kjarni_VALUE.체계호출().skrá_stýring(kjarni_VALUE.첫과정(), 서술자, 2, 1) == 0, "keyra_skipun 시 Loka Stillingar");
        sannprófa(kjarni_VALUE.체계호출().keyra_skipun(kjarni_VALUE.첫과정(), gögn, new String[] {"시험", "값"}, new String[] {"Tungumál=Íslenska"}) == 0, "ELF keyra_skipun mynd_VALUE 적재");
        sannprófa(kjarni_VALUE.첫과정().실행시작주소() == 0x04001000, "keyra_skipun Keyra_2 slóð 반영");
        sannprófa(kjarni_VALUE.첫과정().실행인자().length == 2 && kjarni_VALUE.첫과정().환경값().length == 1, "keyra_skipun 인자와 환경");
        sannprófa(!kjarni_VALUE.첫과정().파일서술자().upplýsingatækni_opið(서술자), "keyra_skipun 시 서술자 Loka");
        sannprófa(kjarni_VALUE.쪽관리().바이트읽기(kjarni_VALUE.첫과정().slóð_svæði(), 0x04002000) == 0, "빈 gögn hluti_VALUE 영 frumstilla");
    }

    private static void 입력시험(kjarni kjarni_VALUE) {
        kjarni_VALUE.입력관리().키누름('가');
        kjarni_VALUE.입력관리().쥐이동(3, -2);
        입력사건 첫사건 = kjarni_VALUE.입력관리().Áfram_atvik();
        입력사건 SECOND_atvik = kjarni_VALUE.입력관리().Áfram_atvik();
        sannprófa(첫사건.사건종류() == 입력사건.종류.키누름, "자판 atvik");
        sannprófa(SECOND_atvik.첫째값() == 3 && SECOND_atvik.SECOND_VALUE() == -2, "쥐 færa_VALUE atvik");
    }

    private static void 하드웨어시험(호스트하드웨어 tæki_VALUE) {
        tæki_VALUE.skrifa_gátt_bæti(0x3f8, 0xab);
        sannprófa(tæki_VALUE.포트바이트읽기(0x3f8) == 0xab, "포트 I_Ú 경계");
        sannprófa(tæki_VALUE.직렬기록().contains("JIslOS"), "직렬 LOG_lína");
    }

    private static void 개입중단과서술자시험() {
        IRQ_stjórnandi stjórnandi_VALUE = new IRQ_stjórnandi();
        stjórnandi_VALUE.skrá_færsla(0x21, geymsla_slóð -> geymsla_slóð + 4);
        stjórnandi_VALUE.kveikja();
        sannprófa(stjórnandi_VALUE.dreifa_VALUE(0x21, 100) == 104, "IRQ dreifa_VALUE");
        stjórnandi_VALUE.gera_óvirkan();
        sannprófa(stjórnandi_VALUE.dreifa_VALUE(0x21, 100) == 100, "IRQ gera_óvirkan");

        전역서술자표 서술자표 = new 전역서술자표();
        서술자표.sett_sjálfgildi();
        sannprófa(서술자표.조각들().size() == 5, "전역 서술자표");
        verk_staða_hluti verk_staða = new verk_staða_hluti();
        verk_staða.특권쌓임공간설정(0x10, 0x800000);
        sannprófa(verk_staða.영번쌓임조각() == 0x10 && verk_staða.영번쌓임주소() == 0x800000, "작업 staða_VALUE_e10195a1 hluti_VALUE");
    }

    private static void 저장장치와통신망시험() {
        고급기술결합장치 geymsla_tæki = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.hluti_breyta_stærð];
        byte[] 읽은자료 = new byte[고급기술결합장치.hluti_breyta_stærð];
        쓸자료[17] = 42;
        geymsla_tæki.Skrift(2, 쓸자료);
        geymsla_tæki.Lestur(2, 읽은자료);
        sannprófa(읽은자료[17] == 42, "ATA hluti_VALUE 읽고 Skrift");

        aukabúnaður_tengibraut_stjórnandi aukabúnaður = new aukabúnaður_tengibraut_stjórnandi();
        aukabúnaður.발견(new aukabúnaður_tengibraut_stjórnandi.tæki_VALUE(0x1022, 0x2000, 0xc000, 11));
        sannprófa(aukabúnaður.FIND_færsla(0x1022, 0x2000) != null, "주변 tæki_VALUE FIND_færsla");

        byte[] Ethernet_ramma = new byte[34];
        Ethernet_ramma[12] = 0x08;
        Ethernet_ramma[13] = 0x00;
        Ethernet_ramma[14] = 0x45;
        sannprófa(Net_Verkfæri.Ethernet_UPPER_samskiptaregla(Ethernet_ramma) == 0x0800, "이더넷 상위 samningsvirði");
        sannprófa(Net_Verkfæri.upplýsingatækni_verðfrávik_reiknings_4_samskiptaregla(Ethernet_ramma, 14), "상호통신망규약 4판");
        sannprófa(Net_Verkfæri.skýið_prófsumma(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 prófsumma");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        skrifa_heiltala_VALUE(첫구역, 454, 63);
        skrifa_heiltala_VALUE(첫구역, 458, 1024);
        sannprófa(new 기본분할영역표().Lestur(첫구역).size() == 1, "sjálfgildi 분할 영역표");

        Net_lag lag_VALUE = new Net_lag();
        int[] RECEIVED_COUNT = new int[1];
        lag_VALUE.skrá_notandi_gögn_eining(7, (gögn, Keyra_2, lengd_VALUE) -> RECEIVED_COUNT[0]++);
        byte[] ramma_INDEX = new byte[14 + 20 + 8];
        ramma_INDEX[12] = 0x08;
        ramma_INDEX[13] = 0x00;
        ramma_INDEX[14] = 0x45;
        ramma_INDEX[16] = 0;
        ramma_INDEX[17] = 28;
        ramma_INDEX[23] = 17;
        ramma_INDEX[36] = 0;
        ramma_INDEX[37] = 7;
        sannprófa(lag_VALUE.이더넷받기(ramma_INDEX) && RECEIVED_COUNT[0] == 1, "notandi gögn eining_VALUE_7c611f50 dreifa_VALUE");
    }

    private static void 화면과시계시험() {
        stafur_birta 화면 = new stafur_birta();
        화면.úttak("가나\n다");
        sannprófa(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 úttak");
        klukka klukka = new klukka(100);
        for (int INDEX = 0; INDEX < 10; INDEX++) {
            klukka.틱();
        }
        sannprófa(klukka.지난밀리초() == 100, "klukka 틱 CONVERT_VALUE");
    }

    private static void skrifa_heiltala_VALUE(byte[] gögn, int Staðsetning, int VALUE) {
        gögn[Staðsetning] = (byte) VALUE;
        gögn[Staðsetning + 1] = (byte) (VALUE >>> 8);
        gögn[Staðsetning + 2] = (byte) (VALUE >>> 16);
        gögn[Staðsetning + 3] = (byte) (VALUE >>> 24);
    }

    private static void 짧은정수쓰기(byte[] gögn, int Staðsetning, int VALUE) {
        gögn[Staðsetning] = (byte) VALUE;
        gögn[Staðsetning + 1] = (byte) (VALUE >>> 8);
    }

    private static void sannprófa(boolean skilyrði, String Heiti) {
        if (!skilyrði) {
            throw new AssertionError("bilun_VALUE: " + Heiti);
        }
        senda_COUNT++;
        System.out.println("senda_VALUE: " + Heiti);
    }
}
