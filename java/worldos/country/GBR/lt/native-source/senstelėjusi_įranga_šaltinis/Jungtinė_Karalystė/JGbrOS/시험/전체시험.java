// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Jungtinė_Karalystė.JGbrOS.시험;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Jungtinė_Karalystė.JGbrOS.atmintis_sritis.기억공간관리자;
import Jungtinė_Karalystė.JGbrOS.atmintis_sritis.쪽관리자;
import Jungtinė_Karalystė.JGbrOS.입력.입력사건;
import Jungtinė_Karalystė.JGbrOS.작업.Procesas_VALUE;
import Jungtinė_Karalystė.JGbrOS.체계호출.체계호출;
import Jungtinė_Karalystė.JGbrOS.failų_sistema.실행파일적재기;
import Jungtinė_Karalystė.JGbrOS.branduolys.branduolys;
import Jungtinė_Karalystė.JGbrOS.organizuoti.organizuoti_aparatūra;
import Jungtinė_Karalystė.JGbrOS.IRQ.개입중단관리자;
import Jungtinė_Karalystė.JGbrOS.서술자.전역서술자표;
import Jungtinė_Karalystė.JGbrOS.saugojimo_įrenginys.고급기술결합장치;
import Jungtinė_Karalystė.JGbrOS.įrenginys_VALUE.주변장치연결관리자;
import Jungtinė_Karalystė.JGbrOS.tinklas_eilė.tinklas_Įrankiai;
import Jungtinė_Karalystė.JGbrOS.tinklas_eilė.tinklo_funkcionavimo_lygmuo;
import Jungtinė_Karalystė.JGbrOS.įrenginys_VALUE.laikrodis;
import Jungtinė_Karalystė.JGbrOS.서술자.užduotis_Būsena_segmentas;
import Jungtinė_Karalystė.JGbrOS.화면.simbolis_rodyti;
import Jungtinė_Karalystė.JGbrOS.failų_sistema.pirminis_skaidinys_lentelė;

public final class 전체시험 {
    private static int perduoti_COUNT;

    private 전체시험() {
    }

    public static void main(String[] parametras_argumentas) {
        organizuoti_aparatūra įrenginys_VALUE = new organizuoti_aparatūra();
        branduolys branduolys_VALUE = new branduolys(įrenginys_VALUE);
        branduolys_VALUE.Paleisti();

        기억공간시험(branduolys_VALUE);
        쪽관리시험(branduolys_VALUE);
        파일과과정시험(branduolys_VALUE);
        실행파일시험(branduolys_VALUE);
        입력시험(branduolys_VALUE);
        하드웨어시험(įrenginys_VALUE);
        개입중단과서술자시험();
        저장장치와통신망시험();
        화면과시계시험();

        System.out.println("JGbrOS 시험 perduoti_VALUE: " + perduoti_COUNT);
    }

    private static void 기억공간시험(branduolys branduolys_VALUE) {
        기억공간관리자 관리자 = branduolys_VALUE.atmintis_sritis();
        int 첫주소 = 관리자.정렬할당(100, 64);
        patvirtinti((첫주소 & 63) == 0, "lygiuoti_VALUE priskirti_Saugykla");
        관리자.rašymas_baitas_VALUE(첫주소, (byte) 0x5a);
        patvirtinti(관리자.바이트읽기(첫주소) == (byte) 0x5a, "물리 atmintis_sritis 읽고 Rašymas");
        int 사용전 = 관리자.사용크기();
        관리자.išleisti_Saugykla(첫주소);
        patvirtinti(관리자.사용크기() < 사용전, "atmintis_sritis išleisti_Saugykla");
    }

    private static void 쪽관리시험(branduolys branduolys_VALUE) {
        쪽관리자 관리자 = branduolys_VALUE.쪽관리();
        쪽관리자.ADDRESS_erdvė pirminis_erdvė = 관리자.새주소공간();
        관리자.MAP_puslapis(pirminis_erdvė, 0x1000, true);
        관리자.rašymas_baitas_VALUE(pirminis_erdvė, 0x1010, (byte) 7);
        쪽관리자.ADDRESS_erdvė vaikas_erdvė = 관리자.쓰기시복사복제(pirminis_erdvė);
        관리자.rašymas_baitas_VALUE(vaikas_erdvė, 0x1010, (byte) 9);
        patvirtinti(관리자.바이트읽기(pirminis_erdvė, 0x1010) == 7, "Rašymas 시 kopijuoti_VALUE pirminis_VALUE 격리");
        patvirtinti(관리자.바이트읽기(vaikas_erdvė, 0x1010) == 9, "Rašymas 시 kopijuoti_VALUE vaikas_VALUE Rašymas");
    }

    private static void 파일과과정시험(branduolys branduolys_VALUE) {
        byte[] Turinys_VALUE = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        branduolys_VALUE.failų_sistema().sujungti_Failas("시험", Turinys_VALUE);
        Procesas_VALUE pirminis_VALUE = branduolys_VALUE.첫과정();
        체계호출 호출 = branduolys_VALUE.체계호출();
        int 서술자 = 호출.Atverti(pirminis_VALUE, "/시험", 체계호출.tik_skaitomas_žymė);
        patvirtinti(서술자 >= 3, "Failas Atverti");

        byte[] gauti_vieta = new byte[Turinys_VALUE.length];
        patvirtinti(호출.Skaitymas(pirminis_VALUE, 서술자, gauti_vieta, gauti_vieta.length) == Turinys_VALUE.length, "Failas Skaitymas");
        patvirtinti(Arrays.equals(Turinys_VALUE, gauti_vieta), "Failas Turinys_VALUE");
        patvirtinti(호출.judėti_padėtis(pirminis_VALUE, 서술자, 0, 체계호출.Ieška_Start) == 0, "Failas Pozicija judėti_VALUE");

        int 복제서술자 = 호출.서술자복제(pirminis_VALUE, 서술자);
        patvirtinti(복제서술자 >= 0, "서술자 klonas_VALUE");
        Procesas_VALUE vaikas_VALUE = 호출.klonas_Procesas(pirminis_VALUE);
        patvirtinti(vaikas_VALUE.identifikatorius_VALUE() != pirminis_VALUE.identifikatorius_VALUE(), "Procesas_VALUE identifikatorius_VALUE 분리");
        patvirtinti(vaikas_VALUE.pirminis_identifikatorius() == pirminis_VALUE.identifikatorius_VALUE(), "pirminis_VALUE Procesas_VALUE identifikatorius_VALUE");
        patvirtinti(호출.Užverti(vaikas_VALUE, 서술자) == 0 && pirminis_VALUE.파일서술자().informacinės_technologijos_kurti(서술자), "vaikas_VALUE Užverti 격리");

        int 이전끝 = 호출.padidėjimas_programa_nutraukti(pirminis_VALUE, 8192);
        patvirtinti(이전끝 == 0x06000000, "programa_f5044b9b 끝 늘리기");
        patvirtinti(pirminis_VALUE.programa_nutraukti() == 0x06002000, "programa_f5044b9b 끝 반영");
        patvirtinti(vaikas_VALUE.programa_nutraukti() == 0x06000000, "과정별 programa_f5044b9b 끝 격리");

        vaikas_VALUE.Baigti_programa_086bb533(7);
        patvirtinti(호출.자식기다리기(pirminis_VALUE, vaikas_VALUE.identifikatorius_VALUE(), false) == (7 << 8), "vaikas_VALUE Baigti_programa_086bb533 기다리기");
        patvirtinti(호출.접근가능("시험", 1) == -13, "Vykdyti_komanda teisė_VALUE atmesti_VALUE");
        patvirtinti(호출.UID() == 0 && 호출.Grupė_identifikatorius() == 0, "사용자와 무리 identifikatorius_VALUE");
        patvirtinti("/".equals(호출.dabartinis_užduočių_sąrašas(2)) && 호출.SWITCH_užduočių_sąrašas("/") == 0, "dabartinis_prekė 작업 įrašas_Sąrašas");
        patvirtinti(호출.informacinės_technologijos_Terminalas(pirminis_VALUE, 1), "표준 Išvestis 단말");
        patvirtinti("JGbrOS".equals(호출.sistema_Išsami_informacija().sistema_pavadinimas()), "operacinė_sistema_VALUE msinfo32_exe");
    }

    private static void 실행파일시험(branduolys branduolys_VALUE) {
        byte[] duomenys = new byte[92];
        duomenys[0] = 0x7f;
        duomenys[1] = 'E';
        duomenys[2] = 'L';
        duomenys[3] = 'F';
        duomenys[4] = 1;
        duomenys[5] = 1;
        rašymas_sveikasis_skaičius_VALUE(duomenys, 24, 0x04001000);
        rašymas_sveikasis_skaičius_VALUE(duomenys, 32, 52);
        짧은정수쓰기(duomenys, 46, 40);
        짧은정수쓰기(duomenys, 48, 1);
        rašymas_sveikasis_skaičius_VALUE(duomenys, 56, 8);
        rašymas_sveikasis_skaičius_VALUE(duomenys, 60, 2);
        rašymas_sveikasis_skaičius_VALUE(duomenys, 64, 0x04002000);
        rašymas_sveikasis_skaičius_VALUE(duomenys, 72, 64);

        실행파일적재기.IMAGE IMAGE_VALUE = new 실행파일적재기().검사(duomenys);
        patvirtinti(IMAGE_VALUE.Start_ADDRESS() == 0x04001000, "ELF Paleisti ADDRESS");
        patvirtinti(IMAGE_VALUE.구역들().size() == 1 && IMAGE_VALUE.구역들().get(0).종류() == 8, "ELF 빈 duomenys sekcija_VALUE");
        int 서술자 = branduolys_VALUE.체계호출().Atverti(branduolys_VALUE.첫과정(), "시험", 체계호출.tik_skaitomas_žymė);
        patvirtinti(branduolys_VALUE.체계호출().Failas_valdymas(branduolys_VALUE.첫과정(), 서술자, 2, 1) == 0, "Vykdyti_komanda 시 Užverti Nustatymai");
        patvirtinti(branduolys_VALUE.체계호출().Vykdyti_komanda(branduolys_VALUE.첫과정(), duomenys, new String[] {"시험", "값"}, new String[] {"Kalba=Lietuvių"}) == 0, "ELF Vykdyti_komanda IMAGE_VALUE 적재");
        patvirtinti(branduolys_VALUE.첫과정().실행시작주소() == 0x04001000, "Vykdyti_komanda Paleisti ADDRESS 반영");
        patvirtinti(branduolys_VALUE.첫과정().실행인자().length == 2 && branduolys_VALUE.첫과정().환경값().length == 1, "Vykdyti_komanda 인자와 환경");
        patvirtinti(!branduolys_VALUE.첫과정().파일서술자().informacinės_technologijos_kurti(서술자), "Vykdyti_komanda 시 서술자 Užverti");
        patvirtinti(branduolys_VALUE.쪽관리().바이트읽기(branduolys_VALUE.첫과정().ADDRESS_erdvė(), 0x04002000) == 0, "빈 duomenys sekcija_VALUE nulis_operandas 초기화");
    }

    private static void 입력시험(branduolys branduolys_VALUE) {
        branduolys_VALUE.입력관리().Raktas_neveikiantis('가');
        branduolys_VALUE.입력관리().쥐이동(3, -2);
        입력사건 첫사건 = branduolys_VALUE.입력관리().toliau_įvykis();
        입력사건 SECOND_įvykis = branduolys_VALUE.입력관리().toliau_įvykis();
        patvirtinti(첫사건.įvykio_rūšis() == 입력사건.종류.Raktas_neveikiantis, "자판 Įvykis");
        patvirtinti(SECOND_įvykis.첫째값() == 3 && SECOND_įvykis.SECOND_VALUE() == -2, "쥐 judėti_VALUE Įvykis");
    }

    private static void 하드웨어시험(organizuoti_aparatūra įrenginys_VALUE) {
        įrenginys_VALUE.rašymas_jungtis_baitas(0x3f8, 0xab);
        patvirtinti(įrenginys_VALUE.포트바이트읽기(0x3f8) == 0xab, "aparatūra_jungtis Į_I 경계");
        patvirtinti(įrenginys_VALUE.직렬기록().contains("JGbrOS"), "직렬 LOG_RECORD");
    }

    private static void 개입중단과서술자시험() {
        개입중단관리자 관리자 = new 개입중단관리자();
        관리자.registras_įrašas(0x21, Saugykla_ADDRESS -> Saugykla_ADDRESS + 4);
        관리자.įjungti();
        patvirtinti(관리자.platinti_VALUE(0x21, 100) == 104, "IRQ platinti_VALUE");
        관리자.išjungti();
        patvirtinti(관리자.platinti_VALUE(0x21, 100) == 100, "IRQ išjungti");

        전역서술자표 서술자표 = new 전역서술자표();
        서술자표.rinkinys_numatytoji_reikšmė();
        patvirtinti(서술자표.조각들().size() == 5, "전역 서술자표");
        užduotis_Būsena_segmentas užduotis_Būsena = new užduotis_Būsena_segmentas();
        užduotis_Būsena.특권쌓임공간설정(0x10, 0x800000);
        patvirtinti(užduotis_Būsena.eilė_nulis_blokas() == 0x10 && užduotis_Būsena.eilė_nulis_ADDRESS() == 0x800000, "작업 Būsena_VALUE sekcija_VALUE");
    }

    private static void 저장장치와통신망시험() {
        고급기술결합장치 saugojimo_įrenginys = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.sekcija_dydis];
        byte[] 읽은자료 = new byte[고급기술결합장치.sekcija_dydis];
        쓸자료[17] = 42;
        saugojimo_įrenginys.Rašymas(2, 쓸자료);
        saugojimo_įrenginys.Skaitymas(2, 읽은자료);
        patvirtinti(읽은자료[17] == 42, "ATA sekcija_VALUE 읽고 Rašymas");

        주변장치연결관리자 reikmuo = new 주변장치연결관리자();
        reikmuo.발견(new 주변장치연결관리자.įrenginys_VALUE(0x1022, 0x2000, 0xc000, 11));
        patvirtinti(reikmuo.FIND_įrašas(0x1022, 0x2000) != null, "주변 įrenginys_VALUE FIND_įrašas");

        byte[] eternetas_kadras = new byte[34];
        eternetas_kadras[12] = 0x08;
        eternetas_kadras[13] = 0x00;
        eternetas_kadras[14] = 0x45;
        patvirtinti(tinklas_Įrankiai.eternetas_UPPER_protokolas(eternetas_kadras) == 0x0800, "이더넷 상위 sutarties_vertė");
        patvirtinti(tinklas_Įrankiai.informacinės_technologijos_SKN_4_protokolas(eternetas_kadras, 14), "상호통신망규약 4판");
        patvirtinti(tinklas_Įrankiai.debesis_kontrolinė_suma(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 kontrolinė_suma");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        rašymas_sveikasis_skaičius_VALUE(첫구역, 454, 63);
        rašymas_sveikasis_skaičius_VALUE(첫구역, 458, 1024);
        patvirtinti(new pirminis_skaidinys_lentelė().Skaitymas(첫구역).size() == 1, "numatytoji_reikšmė 분할 영역표");

        tinklo_funkcionavimo_lygmuo sluoksnis_VALUE = new tinklo_funkcionavimo_lygmuo();
        int[] RECEIVED_COUNT = new int[1];
        sluoksnis_VALUE.registras_naudotojas_duomenys_pamoka(7, (duomenys, Paleisti, 길이) -> RECEIVED_COUNT[0]++);
        byte[] kadras_INDEX = new byte[14 + 20 + 8];
        kadras_INDEX[12] = 0x08;
        kadras_INDEX[13] = 0x00;
        kadras_INDEX[14] = 0x45;
        kadras_INDEX[16] = 0;
        kadras_INDEX[17] = 28;
        kadras_INDEX[23] = 17;
        kadras_INDEX[36] = 0;
        kadras_INDEX[37] = 7;
        patvirtinti(sluoksnis_VALUE.gauti_eternetas(kadras_INDEX) && RECEIVED_COUNT[0] == 1, "naudotojas duomenys pamoka_VALUE platinti_VALUE");
    }

    private static void 화면과시계시험() {
        simbolis_rodyti 화면 = new simbolis_rodyti();
        화면.Išvestis("가나\n다");
        patvirtinti(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 Išvestis");
        laikrodis laikrodis = new laikrodis(100);
        for (int INDEX = 0; INDEX < 10; INDEX++) {
            laikrodis.tiksėjimas_VALUE();
        }
        patvirtinti(laikrodis.지난밀리초() == 100, "laikrodis tiksėjimas_VALUE CONVERT_VALUE");
    }

    private static void rašymas_sveikasis_skaičius_VALUE(byte[] duomenys, int Pozicija, int VALUE) {
        duomenys[Pozicija] = (byte) VALUE;
        duomenys[Pozicija + 1] = (byte) (VALUE >>> 8);
        duomenys[Pozicija + 2] = (byte) (VALUE >>> 16);
        duomenys[Pozicija + 3] = (byte) (VALUE >>> 24);
    }

    private static void 짧은정수쓰기(byte[] duomenys, int Pozicija, int VALUE) {
        duomenys[Pozicija] = (byte) VALUE;
        duomenys[Pozicija + 1] = (byte) (VALUE >>> 8);
    }

    private static void patvirtinti(boolean sąlyga, String Pavadinimas_2) {
        if (!sąlyga) {
            throw new AssertionError("triktis_VALUE: " + Pavadinimas_2);
        }
        perduoti_COUNT++;
        System.out.println("perduoti_VALUE: " + Pavadinimas_2);
    }
}
