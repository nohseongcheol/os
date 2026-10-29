// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Turqi.JTurOS.시험;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Turqi.JTurOS.기억공간.Memorie_menaxher;
import Turqi.JTurOS.기억공간.faqe_menaxher;
import Turqi.JTurOS.입력.입력사건;
import Turqi.JTurOS.작업.Proces_VALUE;
import Turqi.JTurOS.체계호출.체계호출;
import Turqi.JTurOS.sistemi_i_skedarëve.실행파일적재기;
import Turqi.JTurOS.bërthamë.bërthamë;
import Turqi.JTurOS.pritës.호스트하드웨어;
import Turqi.JTurOS.IRQ.IRQ_menaxher;
import Turqi.JTurOS.서술자.전역서술자표;
import Turqi.JTurOS.hapësira_ruajtëse_pajisje.고급기술결합장치;
import Turqi.JTurOS.pajisje_VALUE.aksesor_magjistrale_menaxher;
import Turqi.JTurOS.rrjet_Stivë.rrjet_Mjete;
import Turqi.JTurOS.rrjet_Stivë.rrjet_Shtresë;
import Turqi.JTurOS.pajisje_VALUE.Ora;
import Turqi.JTurOS.서술자.detyrë_status_segment;
import Turqi.JTurOS.화면.karakter_afishim;
import Turqi.JTurOS.sistemi_i_skedarëve.기본분할영역표;

public final class 전체시험 {
    private static int kaloj_COUNT;

    private 전체시험() {
    }

    public static void main(String[] parametër_argument) {
        호스트하드웨어 pajisje_VALUE = new 호스트하드웨어();
        bërthamë bërthamë_VALUE = new bërthamë(pajisje_VALUE);
        bërthamë_VALUE.Ekzekuto();

        기억공간시험(bërthamë_VALUE);
        쪽관리시험(bërthamë_VALUE);
        파일과과정시험(bërthamë_VALUE);
        실행파일시험(bërthamë_VALUE);
        입력시험(bërthamë_VALUE);
        하드웨어시험(pajisje_VALUE);
        개입중단과서술자시험();
        저장장치와통신망시험();
        화면과시계시험();

        System.out.println("JTurOS 시험 kaloj_VALUE: " + kaloj_COUNT);
    }

    private static void 기억공간시험(bërthamë bërthamë_VALUE) {
        Memorie_menaxher menaxher_VALUE = bërthamë_VALUE.기억공간();
        int 첫주소 = menaxher_VALUE.정렬할당(100, 64);
        verifikoj((첫주소 & 63) == 0, "drejtvendos_VALUE caktoj_hapësira_ruajtëse");
        menaxher_VALUE.shkruaj_bajt_VALUE(첫주소, (byte) 0x5a);
        verifikoj(menaxher_VALUE.바이트읽기(첫주소) == (byte) 0x5a, "물리 기억공간 읽고 Shkrimi");
        int 사용전 = menaxher_VALUE.사용크기();
        menaxher_VALUE.liroj_hapësira_ruajtëse(첫주소);
        verifikoj(menaxher_VALUE.사용크기() < 사용전, "기억공간 liroj_hapësira_ruajtëse");
    }

    private static void 쪽관리시험(bërthamë bërthamë_VALUE) {
        faqe_menaxher menaxher_VALUE = bërthamë_VALUE.쪽관리();
        faqe_menaxher.email_HAPËSIRË 부모공간 = menaxher_VALUE.새주소공간();
        menaxher_VALUE.MAP_faqe(부모공간, 0x1000, true);
        menaxher_VALUE.shkruaj_bajt_VALUE(부모공간, 0x1010, (byte) 7);
        faqe_menaxher.email_HAPËSIRË fëmijë_HAPËSIRË = menaxher_VALUE.쓰기시복사복제(부모공간);
        menaxher_VALUE.shkruaj_bajt_VALUE(fëmijë_HAPËSIRË, 0x1010, (byte) 9);
        verifikoj(menaxher_VALUE.바이트읽기(부모공간, 0x1010) == 7, "Shkrimi 시 kopjoj_VALUE 부모 격리");
        verifikoj(menaxher_VALUE.바이트읽기(fëmijë_HAPËSIRË, 0x1010) == 9, "Shkrimi 시 kopjoj_VALUE fëmijë_VALUE Shkrimi");
    }

    private static void 파일과과정시험(bërthamë bërthamë_VALUE) {
        byte[] Përmbajtje_VALUE = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        bërthamë_VALUE.sistemi_i_skedarëve().파일추가("시험", Përmbajtje_VALUE);
        Proces_VALUE 부모 = bërthamë_VALUE.첫과정();
        체계호출 호출 = bërthamë_VALUE.체계호출();
        int 서술자 = 호출.Hap(부모, "/시험", 체계호출.vetëm_për_lexim_flamur);
        verifikoj(서술자 >= 3, "Kartelë Hap");

        byte[] 받을곳 = new byte[Përmbajtje_VALUE.length];
        verifikoj(호출.Leximi(부모, 서술자, 받을곳, 받을곳.length) == Përmbajtje_VALUE.length, "Kartelë Leximi");
        verifikoj(Arrays.equals(Përmbajtje_VALUE, 받을곳), "Kartelë Përmbajtje_VALUE");
        verifikoj(호출.lëviz_pozicioni(부모, 서술자, 0, 체계호출.Kërkim_nis) == 0, "Kartelë Pozicioni lëviz_VALUE");

        int 복제서술자 = 호출.서술자복제(부모, 서술자);
        verifikoj(복제서술자 >= 0, "서술자 복제");
        Proces_VALUE fëmijë_VALUE = 호출.과정복제(부모);
        verifikoj(fëmijë_VALUE.identifikues_VALUE() != 부모.identifikues_VALUE(), "Proces_VALUE identifikues_VALUE 분리");
        verifikoj(fëmijë_VALUE.부모식별자() == 부모.identifikues_VALUE(), "부모 Proces_VALUE identifikues_VALUE");
        verifikoj(호출.Mbyll(fëmijë_VALUE, 서술자) == 0 && 부모.파일서술자().teknologjia_e_informacionit_hap(서술자), "fëmijë_VALUE Mbyll 격리");

        int 이전끝 = 호출.프로그램끝늘리기(부모, 8192);
        verifikoj(이전끝 == 0x06000000, "program_f5044b9b 끝 늘리기");
        verifikoj(부모.프로그램끝() == 0x06002000, "program_f5044b9b 끝 반영");
        verifikoj(fëmijë_VALUE.프로그램끝() == 0x06000000, "과정별 program_f5044b9b 끝 격리");

        fëmijë_VALUE.dal_program(7);
        verifikoj(호출.자식기다리기(부모, fëmijë_VALUE.identifikues_VALUE(), false) == (7 << 8), "fëmijë_VALUE dal_program 기다리기");
        verifikoj(호출.접근가능("시험", 1) == -13, "zbatoj_komandë leje_VALUE refuzo_VALUE");
        verifikoj(호출.përdorues_identifikues() == 0 && 호출.grup_identifikues() == 0, "사용자와 무리 identifikues_VALUE");
        verifikoj("/".equals(호출.현재작업목록(2)) && 호출.SWITCH_lista_e_detyrave("/") == 0, "현재 작업 futje_Listë");
        verifikoj(호출.teknologjia_e_informacionit_Terminali(부모, 1), "표준 출력 단말");
        verifikoj("JTurOS".equals(호출.체계정보().sistem_emër()), "sistem_operativ_VALUE msinfo32_exe");
    }

    private static void 실행파일시험(bërthamë bërthamë_VALUE) {
        byte[] të_dhëna = new byte[92];
        të_dhëna[0] = 0x7f;
        të_dhëna[1] = 'E';
        të_dhëna[2] = 'L';
        të_dhëna[3] = 'F';
        të_dhëna[4] = 1;
        të_dhëna[5] = 1;
        shkruaj_numër_i_plotë_VALUE(të_dhëna, 24, 0x04001000);
        shkruaj_numër_i_plotë_VALUE(të_dhëna, 32, 52);
        짧은정수쓰기(të_dhëna, 46, 40);
        짧은정수쓰기(të_dhëna, 48, 1);
        shkruaj_numër_i_plotë_VALUE(të_dhëna, 56, 8);
        shkruaj_numër_i_plotë_VALUE(të_dhëna, 60, 2);
        shkruaj_numër_i_plotë_VALUE(të_dhëna, 64, 0x04002000);
        shkruaj_numër_i_plotë_VALUE(të_dhëna, 72, 64);

        실행파일적재기.IMAGE IMAGE_VALUE = new 실행파일적재기().검사(të_dhëna);
        verifikoj(IMAGE_VALUE.nis_email() == 0x04001000, "ELF Ekzekuto email");
        verifikoj(IMAGE_VALUE.구역들().size() == 1 && IMAGE_VALUE.구역들().get(0).종류() == 8, "ELF 빈 të_dhëna seksion_VALUE");
        int 서술자 = bërthamë_VALUE.체계호출().Hap(bërthamë_VALUE.첫과정(), "시험", 체계호출.vetëm_për_lexim_flamur);
        verifikoj(bërthamë_VALUE.체계호출().skedar_kontroll(bërthamë_VALUE.첫과정(), 서술자, 2, 1) == 0, "zbatoj_komandë 시 Mbyll Rregullime");
        verifikoj(bërthamë_VALUE.체계호출().zbatoj_komandë(bërthamë_VALUE.첫과정(), të_dhëna, new String[] {"시험", "값"}, new String[] {"Gjuha=한국어"}) == 0, "ELF zbatoj_komandë IMAGE_VALUE 적재");
        verifikoj(bërthamë_VALUE.첫과정().실행시작주소() == 0x04001000, "zbatoj_komandë Ekzekuto email 반영");
        verifikoj(bërthamë_VALUE.첫과정().실행인자().length == 2 && bërthamë_VALUE.첫과정().환경값().length == 1, "zbatoj_komandë 인자와 환경");
        verifikoj(!bërthamë_VALUE.첫과정().파일서술자().teknologjia_e_informacionit_hap(서술자), "zbatoj_komandë 시 서술자 Mbyll");
        verifikoj(bërthamë_VALUE.쪽관리().바이트읽기(bërthamë_VALUE.첫과정().email_HAPËSIRË(), 0x04002000) == 0, "빈 të_dhëna seksion_VALUE 영 filloj");
    }

    private static void 입력시험(bërthamë bërthamë_VALUE) {
        bërthamë_VALUE.입력관리().키누름('가');
        bërthamë_VALUE.입력관리().쥐이동(3, -2);
        입력사건 첫사건 = bërthamë_VALUE.입력관리().Tjetër_ngjarje();
        입력사건 SECOND_ngjarje = bërthamë_VALUE.입력관리().Tjetër_ngjarje();
        verifikoj(첫사건.사건종류() == 입력사건.종류.키누름, "자판 Ngjarje");
        verifikoj(SECOND_ngjarje.첫째값() == 3 && SECOND_ngjarje.SECOND_VALUE() == -2, "쥐 lëviz_VALUE Ngjarje");
    }

    private static void 하드웨어시험(호스트하드웨어 pajisje_VALUE) {
        pajisje_VALUE.shkruaj_portë_bajt(0x3f8, 0xab);
        verifikoj(pajisje_VALUE.포트바이트읽기(0x3f8) == 0xab, "포트 I_O 경계");
        verifikoj(pajisje_VALUE.직렬기록().contains("JTurOS"), "직렬 LOG_RECORD");
    }

    private static void 개입중단과서술자시험() {
        IRQ_menaxher menaxher_VALUE = new IRQ_menaxher();
        menaxher_VALUE.regjistroj_futje(0x21, hapësira_ruajtëse_email -> hapësira_ruajtëse_email + 4);
        menaxher_VALUE.aktivizoj();
        verifikoj(menaxher_VALUE.shpërndaj_VALUE(0x21, 100) == 104, "IRQ shpërndaj_VALUE");
        menaxher_VALUE.çaktivizoj();
        verifikoj(menaxher_VALUE.shpërndaj_VALUE(0x21, 100) == 100, "IRQ çaktivizoj");

        전역서술자표 서술자표 = new 전역서술자표();
        서술자표.bashkësi_vlerë_e_parazgjedhur();
        verifikoj(서술자표.조각들().size() == 5, "전역 서술자표");
        detyrë_status_segment detyrë_status = new detyrë_status_segment();
        detyrë_status.특권쌓임공간설정(0x10, 0x800000);
        verifikoj(detyrë_status.영번쌓임조각() == 0x10 && detyrë_status.영번쌓임주소() == 0x800000, "작업 status_VALUE seksion_VALUE");
    }

    private static void 저장장치와통신망시험() {
        고급기술결합장치 hapësira_ruajtëse_pajisje = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.seksion_ndryshoj_përmasat];
        byte[] 읽은자료 = new byte[고급기술결합장치.seksion_ndryshoj_përmasat];
        쓸자료[17] = 42;
        hapësira_ruajtëse_pajisje.Shkrimi(2, 쓸자료);
        hapësira_ruajtëse_pajisje.Leximi(2, 읽은자료);
        verifikoj(읽은자료[17] == 42, "ATA seksion_VALUE 읽고 Shkrimi");

        aksesor_magjistrale_menaxher aksesor = new aksesor_magjistrale_menaxher();
        aksesor.발견(new aksesor_magjistrale_menaxher.pajisje_VALUE(0x1022, 0x2000, 0xc000, 11));
        verifikoj(aksesor.FIND_futje(0x1022, 0x2000) != null, "주변 pajisje_VALUE FIND_futje");

        byte[] Eternet_kuadër = new byte[34];
        Eternet_kuadër[12] = 0x08;
        Eternet_kuadër[13] = 0x00;
        Eternet_kuadër[14] = 0x45;
        verifikoj(rrjet_Mjete.Eternet_UPPER_protokoll(Eternet_kuadër) == 0x0800, "이더넷 상위 punë_VALUE");
        verifikoj(rrjet_Mjete.상호통신망규약사판인가(Eternet_kuadër, 14), "상호통신망규약 4판");
        verifikoj(rrjet_Mjete.Internet_kontrolli_i_shumës(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 kontrolli_i_shumës");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        shkruaj_numër_i_plotë_VALUE(첫구역, 454, 63);
        shkruaj_numër_i_plotë_VALUE(첫구역, 458, 1024);
        verifikoj(new 기본분할영역표().Leximi(첫구역).size() == 1, "vlerë_e_parazgjedhur 분할 영역표");

        rrjet_Shtresë Shtresë_VALUE = new rrjet_Shtresë();
        int[] RECEIVED_COUNT = new int[1];
        Shtresë_VALUE.regjistroj_përdorues_të_dhëna_mësim(7, (të_dhëna, Ekzekuto, gjatësi_VALUE) -> RECEIVED_COUNT[0]++);
        byte[] kuadër_INDEX = new byte[14 + 20 + 8];
        kuadër_INDEX[12] = 0x08;
        kuadër_INDEX[13] = 0x00;
        kuadër_INDEX[14] = 0x45;
        kuadër_INDEX[16] = 0;
        kuadër_INDEX[17] = 28;
        kuadër_INDEX[23] = 17;
        kuadër_INDEX[36] = 0;
        kuadër_INDEX[37] = 7;
        verifikoj(Shtresë_VALUE.이더넷받기(kuadër_INDEX) && RECEIVED_COUNT[0] == 1, "përdorues të_dhëna mësim_VALUE shpërndaj_VALUE");
    }

    private static void 화면과시계시험() {
        karakter_afishim 화면 = new karakter_afishim();
        화면.출력("가나\n다");
        verifikoj(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 출력");
        Ora Ora = new Ora(100);
        for (int INDEX = 0; INDEX < 10; INDEX++) {
            Ora.틱();
        }
        verifikoj(Ora.지난밀리초() == 100, "Ora 틱 CONVERT_VALUE");
    }

    private static void shkruaj_numër_i_plotë_VALUE(byte[] të_dhëna, int Pozicioni, int VALUE) {
        të_dhëna[Pozicioni] = (byte) VALUE;
        të_dhëna[Pozicioni + 1] = (byte) (VALUE >>> 8);
        të_dhëna[Pozicioni + 2] = (byte) (VALUE >>> 16);
        të_dhëna[Pozicioni + 3] = (byte) (VALUE >>> 24);
    }

    private static void 짧은정수쓰기(byte[] të_dhëna, int Pozicioni, int VALUE) {
        të_dhëna[Pozicioni] = (byte) VALUE;
        të_dhëna[Pozicioni + 1] = (byte) (VALUE >>> 8);
    }

    private static void verifikoj(boolean kusht, String Emër) {
        if (!kusht) {
            throw new AssertionError("dështim_VALUE: " + Emër);
        }
        kaloj_COUNT++;
        System.out.println("kaloj_VALUE: " + Emër);
    }
}
