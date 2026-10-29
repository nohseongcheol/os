// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Turkmaniston.JTkmOS.시험;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Turkmaniston.JTkmOS.기억공간.Xotira_menejer;
import Turkmaniston.JTkmOS.기억공간.sahifa_menejer;
import Turkmaniston.JTkmOS.입력.입력사건;
import Turkmaniston.JTkmOS.작업.Jarayon_VALUE;
import Turkmaniston.JTkmOS.체계호출.체계호출;
import Turkmaniston.JTkmOS.fayllar_tizimi.실행파일적재기;
import Turkmaniston.JTkmOS.o_zak.o_zak;
import Turkmaniston.JTkmOS.tashkilotchi.호스트하드웨어;
import Turkmaniston.JTkmOS.IRQ.IRQ_menejer;
import Turkmaniston.JTkmOS.서술자.전역서술자표;
import Turkmaniston.JTkmOS.Xotira_qurilma.고급기술결합장치;
import Turkmaniston.JTkmOS.qurilma_VALUE.tashqi_moslama_shina_menejer;
import Turkmaniston.JTkmOS.Tarmoq_Stack.Tarmoq_Vositalar;
import Turkmaniston.JTkmOS.Tarmoq_Stack.Tarmoq_qatlam;
import Turkmaniston.JTkmOS.qurilma_VALUE.Soat;
import Turkmaniston.JTkmOS.서술자.vazifa_holat_segment;
import Turkmaniston.JTkmOS.화면.belgi_ekran;
import Turkmaniston.JTkmOS.fayllar_tizimi.기본분할영역표;

public final class 전체시험 {
    private static int 통과수;

    private 전체시험() {
    }

    public static void main(String[] 인자) {
        호스트하드웨어 qurilma_VALUE = new 호스트하드웨어();
        o_zak o_zak_VALUE = new o_zak(qurilma_VALUE);
        o_zak_VALUE.Bajarish();

        기억공간시험(o_zak_VALUE);
        쪽관리시험(o_zak_VALUE);
        파일과과정시험(o_zak_VALUE);
        실행파일시험(o_zak_VALUE);
        입력시험(o_zak_VALUE);
        하드웨어시험(qurilma_VALUE);
        개입중단과서술자시험();
        저장장치와통신망시험();
        화면과시계시험();

        System.out.println("JTkmOS 시험 통과: " + 통과수);
    }

    private static void 기억공간시험(o_zak o_zak_VALUE) {
        Xotira_menejer menejer_VALUE = o_zak_VALUE.기억공간();
        int 첫주소 = menejer_VALUE.정렬할당(100, 64);
        tasdiqlamoq((첫주소 & 63) == 0, "tenglashtirmoq_VALUE joylashtirmoq_Xotira");
        menejer_VALUE.yozmoq_bayt_VALUE(첫주소, (byte) 0x5a);
        tasdiqlamoq(menejer_VALUE.바이트읽기(첫주소) == (byte) 0x5a, "물리 기억공간 읽고 Yozish");
        int 사용전 = menejer_VALUE.사용크기();
        menejer_VALUE.nashr_Xotira(첫주소);
        tasdiqlamoq(menejer_VALUE.사용크기() < 사용전, "기억공간 nashr_Xotira");
    }

    private static void 쪽관리시험(o_zak o_zak_VALUE) {
        sahifa_menejer menejer_VALUE = o_zak_VALUE.쪽관리();
        sahifa_menejer.manzil_joy 부모공간 = menejer_VALUE.새주소공간();
        menejer_VALUE.MAP_sahifa(부모공간, 0x1000, true);
        menejer_VALUE.yozmoq_bayt_VALUE(부모공간, 0x1010, (byte) 7);
        sahifa_menejer.manzil_joy farzand_joy = menejer_VALUE.쓰기시복사복제(부모공간);
        menejer_VALUE.yozmoq_bayt_VALUE(farzand_joy, 0x1010, (byte) 9);
        tasdiqlamoq(menejer_VALUE.바이트읽기(부모공간, 0x1010) == 7, "Yozish 시 namuna_VALUE 부모 격리");
        tasdiqlamoq(menejer_VALUE.바이트읽기(farzand_joy, 0x1010) == 9, "Yozish 시 namuna_VALUE farzand_VALUE Yozish");
    }

    private static void 파일과과정시험(o_zak o_zak_VALUE) {
        byte[] tarkib_VALUE = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        o_zak_VALUE.fayllar_tizimi().파일추가("시험", tarkib_VALUE);
        Jarayon_VALUE 부모 = o_zak_VALUE.첫과정();
        체계호출 호출 = o_zak_VALUE.체계호출();
        int 서술자 = 호출.Ochish(부모, "/시험", 체계호출.faqat_o_qish_uchun_bayroq);
        tasdiqlamoq(서술자 >= 3, "Fayl Ochish");

        byte[] 받을곳 = new byte[tarkib_VALUE.length];
        tasdiqlamoq(호출.Oʻqish(부모, 서술자, 받을곳, 받을곳.length) == tarkib_VALUE.length, "Fayl Oʻqish");
        tasdiqlamoq(Arrays.equals(tarkib_VALUE, 받을곳), "Fayl tarkib_VALUE");
        tasdiqlamoq(호출.ko_chirmoq_holat(부모, 서술자, 0, 체계호출.Izlash_Start) == 0, "Fayl Holati ko_chirmoq_VALUE");

        int 복제서술자 = 호출.서술자복제(부모, 서술자);
        tasdiqlamoq(복제서술자 >= 0, "서술자 복제");
        Jarayon_VALUE farzand_VALUE = 호출.과정복제(부모);
        tasdiqlamoq(farzand_VALUE.identifikator_VALUE() != 부모.identifikator_VALUE(), "Jarayon_VALUE identifikator_VALUE 분리");
        tasdiqlamoq(farzand_VALUE.부모식별자() == 부모.identifikator_VALUE(), "부모 Jarayon_VALUE identifikator_VALUE");
        tasdiqlamoq(호출.Yopish(farzand_VALUE, 서술자) == 0 && 부모.파일서술자().열려있음(서술자), "farzand_VALUE Yopish 격리");

        int 이전끝 = 호출.프로그램끝늘리기(부모, 8192);
        tasdiqlamoq(이전끝 == 0x06000000, "ilova_f5044b9b 끝 늘리기");
        tasdiqlamoq(부모.프로그램끝() == 0x06002000, "ilova_f5044b9b 끝 반영");
        tasdiqlamoq(farzand_VALUE.프로그램끝() == 0x06000000, "과정별 ilova_f5044b9b 끝 격리");

        farzand_VALUE.Chiqish_ilova(7);
        tasdiqlamoq(호출.자식기다리기(부모, farzand_VALUE.identifikator_VALUE(), false) == (7 << 8), "farzand_VALUE Chiqish_ilova 기다리기");
        tasdiqlamoq(호출.접근가능("시험", 1) == -13, "bajarmoq_buyruq ruxsat_VALUE_a9fa0dfa 거부");
        tasdiqlamoq(호출.foydalanuvchi_identifikator() == 0 && 호출.Guruh_identifikator() == 0, "사용자와 무리 identifikator_VALUE");
        tasdiqlamoq("/".equals(호출.현재작업목록(2)) && 호출.SWITCH_vazifalar_ro_yxati("/") == 0, "현재 작업 kiritish_Ro_yxat");
        tasdiqlamoq(호출.단말인가(부모, 1), "표준 출력 단말");
        tasdiqlamoq("JTkmOS".equals(호출.체계정보().tizim_nom()), "operatsion_tizim_VALUE msinfo32_exe");
    }

    private static void 실행파일시험(o_zak o_zak_VALUE) {
        byte[] ma_lumotlar = new byte[92];
        ma_lumotlar[0] = 0x7f;
        ma_lumotlar[1] = 'E';
        ma_lumotlar[2] = 'L';
        ma_lumotlar[3] = 'F';
        ma_lumotlar[4] = 1;
        ma_lumotlar[5] = 1;
        yozmoq_butun_son_VALUE(ma_lumotlar, 24, 0x04001000);
        yozmoq_butun_son_VALUE(ma_lumotlar, 32, 52);
        짧은정수쓰기(ma_lumotlar, 46, 40);
        짧은정수쓰기(ma_lumotlar, 48, 1);
        yozmoq_butun_son_VALUE(ma_lumotlar, 56, 8);
        yozmoq_butun_son_VALUE(ma_lumotlar, 60, 2);
        yozmoq_butun_son_VALUE(ma_lumotlar, 64, 0x04002000);
        yozmoq_butun_son_VALUE(ma_lumotlar, 72, 64);

        실행파일적재기.rasm rasm_VALUE = new 실행파일적재기().검사(ma_lumotlar);
        tasdiqlamoq(rasm_VALUE.Start_manzil() == 0x04001000, "ELF Bajarish manzil");
        tasdiqlamoq(rasm_VALUE.구역들().size() == 1 && rasm_VALUE.구역들().get(0).종류() == 8, "ELF 빈 ma_lumotlar bo_lim_VALUE_366e0bfa");
        int 서술자 = o_zak_VALUE.체계호출().Ochish(o_zak_VALUE.첫과정(), "시험", 체계호출.faqat_o_qish_uchun_bayroq);
        tasdiqlamoq(o_zak_VALUE.체계호출().fayl_boshqaruv(o_zak_VALUE.첫과정(), 서술자, 2, 1) == 0, "bajarmoq_buyruq 시 Yopish Moslamalar");
        tasdiqlamoq(o_zak_VALUE.체계호출().bajarmoq_buyruq(o_zak_VALUE.첫과정(), ma_lumotlar, new String[] {"시험", "값"}, new String[] {"Til=한국어"}) == 0, "ELF bajarmoq_buyruq rasm_VALUE 적재");
        tasdiqlamoq(o_zak_VALUE.첫과정().실행시작주소() == 0x04001000, "bajarmoq_buyruq Bajarish manzil 반영");
        tasdiqlamoq(o_zak_VALUE.첫과정().실행인자().length == 2 && o_zak_VALUE.첫과정().환경값().length == 1, "bajarmoq_buyruq 인자와 환경");
        tasdiqlamoq(!o_zak_VALUE.첫과정().파일서술자().열려있음(서술자), "bajarmoq_buyruq 시 서술자 Yopish");
        tasdiqlamoq(o_zak_VALUE.쪽관리().바이트읽기(o_zak_VALUE.첫과정().manzil_joy(), 0x04002000) == 0, "빈 ma_lumotlar bo_lim_VALUE_366e0bfa 영 ishga_tushirmoq");
    }

    private static void 입력시험(o_zak o_zak_VALUE) {
        o_zak_VALUE.입력관리().키누름('가');
        o_zak_VALUE.입력관리().쥐이동(3, -2);
        입력사건 첫사건 = o_zak_VALUE.입력관리().Keyingi_hodisa();
        입력사건 SECOND_hodisa = o_zak_VALUE.입력관리().Keyingi_hodisa();
        tasdiqlamoq(첫사건.사건종류() == 입력사건.종류.키누름, "자판 hodisa");
        tasdiqlamoq(SECOND_hodisa.첫째값() == 3 && SECOND_hodisa.SECOND_VALUE() == -2, "쥐 ko_chirmoq_VALUE hodisa");
    }

    private static void 하드웨어시험(호스트하드웨어 qurilma_VALUE) {
        qurilma_VALUE.yozmoq_port_bayt(0x3f8, 0xab);
        tasdiqlamoq(qurilma_VALUE.포트바이트읽기(0x3f8) == 0xab, "포트 I_O 경계");
        tasdiqlamoq(qurilma_VALUE.직렬기록().contains("JTkmOS"), "직렬 LOG_satr");
    }

    private static void 개입중단과서술자시험() {
        IRQ_menejer menejer_VALUE = new IRQ_menejer();
        menejer_VALUE.등록(0x21, Xotira_manzil -> Xotira_manzil + 4);
        menejer_VALUE.yoqmoq();
        tasdiqlamoq(menejer_VALUE.tarqatish_VALUE(0x21, 100) == 104, "IRQ tarqatish_VALUE");
        menejer_VALUE.o_chirmoq();
        tasdiqlamoq(menejer_VALUE.tarqatish_VALUE(0x21, 100) == 100, "IRQ o_chirmoq");

        전역서술자표 서술자표 = new 전역서술자표();
        서술자표.to_plam_sukut_bo_yicha_qiymat();
        tasdiqlamoq(서술자표.조각들().size() == 5, "전역 서술자표");
        vazifa_holat_segment vazifa_holat = new vazifa_holat_segment();
        vazifa_holat.특권쌓임공간설정(0x10, 0x800000);
        tasdiqlamoq(vazifa_holat.영번쌓임조각() == 0x10 && vazifa_holat.영번쌓임주소() == 0x800000, "작업 holat_VALUE_e10195a1 bo_lim_VALUE_366e0bfa");
    }

    private static void 저장장치와통신망시험() {
        고급기술결합장치 Xotira_qurilma = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.bo_lim_o_lcham];
        byte[] 읽은자료 = new byte[고급기술결합장치.bo_lim_o_lcham];
        쓸자료[17] = 42;
        Xotira_qurilma.Yozish(2, 쓸자료);
        Xotira_qurilma.Oʻqish(2, 읽은자료);
        tasdiqlamoq(읽은자료[17] == 42, "ATA bo_lim_VALUE_366e0bfa 읽고 Yozish");

        tashqi_moslama_shina_menejer tashqi_moslama = new tashqi_moslama_shina_menejer();
        tashqi_moslama.발견(new tashqi_moslama_shina_menejer.qurilma_VALUE(0x1022, 0x2000, 0xc000, 11));
        tasdiqlamoq(tashqi_moslama.FIND_kiritish(0x1022, 0x2000) != null, "주변 qurilma_VALUE FIND_kiritish");

        byte[] Ethernet_kadr = new byte[34];
        Ethernet_kadr[12] = 0x08;
        Ethernet_kadr[13] = 0x00;
        Ethernet_kadr[14] = 0x45;
        tasdiqlamoq(Tarmoq_Vositalar.Ethernet_UPPER_bayonnoma(Ethernet_kadr) == 0x0800, "이더넷 상위 murojaat_VALUE");
        tasdiqlamoq(Tarmoq_Vositalar.상호통신망규약사판인가(Ethernet_kadr, 14), "상호통신망규약 4판");
        tasdiqlamoq(Tarmoq_Vositalar.인터넷검사합(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 검사합");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        yozmoq_butun_son_VALUE(첫구역, 454, 63);
        yozmoq_butun_son_VALUE(첫구역, 458, 1024);
        tasdiqlamoq(new 기본분할영역표().Oʻqish(첫구역).size() == 1, "sukut_bo_yicha_qiymat 분할 영역표");

        Tarmoq_qatlam qatlam_VALUE = new Tarmoq_qatlam();
        int[] RECEIVED_COUNT = new int[1];
        qatlam_VALUE.사용자자료단위등록(7, (ma_lumotlar, Bajarish, uzunlik_VALUE) -> RECEIVED_COUNT[0]++);
        byte[] kadr_INDEX = new byte[14 + 20 + 8];
        kadr_INDEX[12] = 0x08;
        kadr_INDEX[13] = 0x00;
        kadr_INDEX[14] = 0x45;
        kadr_INDEX[16] = 0;
        kadr_INDEX[17] = 28;
        kadr_INDEX[23] = 17;
        kadr_INDEX[36] = 0;
        kadr_INDEX[37] = 7;
        tasdiqlamoq(qatlam_VALUE.이더넷받기(kadr_INDEX) && RECEIVED_COUNT[0] == 1, "foydalanuvchi ma_lumotlar dars_VALUE tarqatish_VALUE");
    }

    private static void 화면과시계시험() {
        belgi_ekran 화면 = new belgi_ekran();
        화면.출력("가나\n다");
        tasdiqlamoq(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 출력");
        Soat Soat = new Soat(100);
        for (int INDEX = 0; INDEX < 10; INDEX++) {
            Soat.틱();
        }
        tasdiqlamoq(Soat.지난밀리초() == 100, "Soat 틱 CONVERT_VALUE");
    }

    private static void yozmoq_butun_son_VALUE(byte[] ma_lumotlar, int Holati, int VALUE) {
        ma_lumotlar[Holati] = (byte) VALUE;
        ma_lumotlar[Holati + 1] = (byte) (VALUE >>> 8);
        ma_lumotlar[Holati + 2] = (byte) (VALUE >>> 16);
        ma_lumotlar[Holati + 3] = (byte) (VALUE >>> 24);
    }

    private static void 짧은정수쓰기(byte[] ma_lumotlar, int Holati, int VALUE) {
        ma_lumotlar[Holati] = (byte) VALUE;
        ma_lumotlar[Holati + 1] = (byte) (VALUE >>> 8);
    }

    private static void tasdiqlamoq(boolean holat, String Nomi) {
        if (!holat) {
            throw new AssertionError("to_xtab_qolish_VALUE: " + Nomi);
        }
        통과수++;
        System.out.println("통과: " + Nomi);
    }
}
