// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Türkiyə.JTurOS.시험;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Türkiyə.JTurOS.기억공간.Yaddaş_menecer;
import Türkiyə.JTurOS.기억공간.səhifə_menecer;
import Türkiyə.JTurOS.입력.입력사건;
import Türkiyə.JTurOS.작업.Proses_VALUE;
import Türkiyə.JTurOS.체계호출.체계호출;
import Türkiyə.JTurOS.fayl_sistemi.실행파일적재기;
import Türkiyə.JTurOS.nüvə.nüvə;
import Türkiyə.JTurOS.host.호스트하드웨어;
import Türkiyə.JTurOS.IRQ.IRQ_menecer;
import Türkiyə.JTurOS.서술자.전역서술자표;
import Türkiyə.JTurOS.Yaddaş_cihaz.고급기술결합장치;
import Türkiyə.JTurOS.cihaz_VALUE.əlavə_qurğu_şin_menecer;
import Türkiyə.JTurOS.Şəbəkə_Yığın.Şəbəkə_Alətlər;
import Türkiyə.JTurOS.Şəbəkə_Yığın.Şəbəkə_lay;
import Türkiyə.JTurOS.cihaz_VALUE.Saat;
import Türkiyə.JTurOS.서술자.tapşırıq_vəziyyət_seqment;
import Türkiyə.JTurOS.화면.simvol_displey;
import Türkiyə.JTurOS.fayl_sistemi.기본분할영역표;

public final class 전체시험 {
    private static int ötürmək_COUNT;

    private 전체시험() {
    }

    public static void main(String[] 인자) {
        호스트하드웨어 cihaz_VALUE = new 호스트하드웨어();
        nüvə nüvə_VALUE = new nüvə(cihaz_VALUE);
        nüvə_VALUE.İcra_Et();

        기억공간시험(nüvə_VALUE);
        쪽관리시험(nüvə_VALUE);
        파일과과정시험(nüvə_VALUE);
        실행파일시험(nüvə_VALUE);
        입력시험(nüvə_VALUE);
        하드웨어시험(cihaz_VALUE);
        개입중단과서술자시험();
        저장장치와통신망시험();
        화면과시계시험();

        System.out.println("JTurOS 시험 ötürmək_VALUE: " + ötürmək_COUNT);
    }

    private static void 기억공간시험(nüvə nüvə_VALUE) {
        Yaddaş_menecer menecer_VALUE = nüvə_VALUE.기억공간();
        int 첫주소 = menecer_VALUE.정렬할당(100, 64);
        yoxlamaq((첫주소 & 63) == 0, "düzləndirmək_VALUE ayırmaq_Yaddaş");
        menecer_VALUE.yazmaq_bayt_VALUE(첫주소, (byte) 0x5a);
        yoxlamaq(menecer_VALUE.바이트읽기(첫주소) == (byte) 0x5a, "물리 기억공간 읽고 Yazma");
        int 사용전 = menecer_VALUE.사용크기();
        menecer_VALUE.burax_Yaddaş(첫주소);
        yoxlamaq(menecer_VALUE.사용크기() < 사용전, "기억공간 burax_Yaddaş");
    }

    private static void 쪽관리시험(nüvə nüvə_VALUE) {
        səhifə_menecer menecer_VALUE = nüvə_VALUE.쪽관리();
        səhifə_menecer.ünvan_məkan 부모공간 = menecer_VALUE.새주소공간();
        menecer_VALUE.MAP_səhifə(부모공간, 0x1000, true);
        menecer_VALUE.yazmaq_bayt_VALUE(부모공간, 0x1010, (byte) 7);
        səhifə_menecer.ünvan_məkan uşaq_məkan = menecer_VALUE.쓰기시복사복제(부모공간);
        menecer_VALUE.yazmaq_bayt_VALUE(uşaq_məkan, 0x1010, (byte) 9);
        yoxlamaq(menecer_VALUE.바이트읽기(부모공간, 0x1010) == 7, "Yazma 시 nümunə_VALUE 부모 격리");
        yoxlamaq(menecer_VALUE.바이트읽기(uşaq_məkan, 0x1010) == 9, "Yazma 시 nümunə_VALUE uşaq_VALUE Yazma");
    }

    private static void 파일과과정시험(nüvə nüvə_VALUE) {
        byte[] Məzmun_VALUE = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        nüvə_VALUE.fayl_sistemi().파일추가("시험", Məzmun_VALUE);
        Proses_VALUE 부모 = nüvə_VALUE.첫과정();
        체계호출 호출 = nüvə_VALUE.체계호출();
        int 서술자 = 호출.Aç(부모, "/시험", 체계호출.yalnız_oxunan_bayraq);
        yoxlamaq(서술자 >= 3, "FAYL Aç");

        byte[] 받을곳 = new byte[Məzmun_VALUE.length];
        yoxlamaq(호출.Oxuma(부모, 서술자, 받을곳, 받을곳.length) == Məzmun_VALUE.length, "FAYL Oxuma");
        yoxlamaq(Arrays.equals(Məzmun_VALUE, 받을곳), "FAYL Məzmun_VALUE");
        yoxlamaq(호출.hərəkət_etdir_yerinə_qoymaq(부모, 서술자, 0, 체계호출.SEARCH_Başla) == 0, "FAYL yerinə_qoymaq hərəkət_etdir_VALUE");

        int 복제서술자 = 호출.서술자복제(부모, 서술자);
        yoxlamaq(복제서술자 >= 0, "서술자 복제");
        Proses_VALUE uşaq_VALUE = 호출.과정복제(부모);
        yoxlamaq(uşaq_VALUE.identifikator_VALUE() != 부모.identifikator_VALUE(), "Proses_VALUE identifikator_VALUE 분리");
        yoxlamaq(uşaq_VALUE.부모식별자() == 부모.identifikator_VALUE(), "부모 Proses_VALUE identifikator_VALUE");
        yoxlamaq(호출.Bağla(uşaq_VALUE, 서술자) == 0 && 부모.파일서술자().열려있음(서술자), "uşaq_VALUE Bağla 격리");

        int 이전끝 = 호출.프로그램끝늘리기(부모, 8192);
        yoxlamaq(이전끝 == 0x06000000, "proqram_f5044b9b 끝 늘리기");
        yoxlamaq(부모.프로그램끝() == 0x06002000, "proqram_f5044b9b 끝 반영");
        yoxlamaq(uşaq_VALUE.프로그램끝() == 0x06000000, "과정별 proqram_f5044b9b 끝 격리");

        uşaq_VALUE.Çıxış_proqram(7);
        yoxlamaq(호출.자식기다리기(부모, uşaq_VALUE.identifikator_VALUE(), false) == (7 << 8), "uşaq_VALUE Çıxış_proqram 기다리기");
        yoxlamaq(호출.접근가능("시험", 1) == -13, "icra_etmək_əmr icazə_VALUE 거부");
        yoxlamaq(호출.istifadəçi_identifikator() == 0 && 호출.Qrup_identifikator() == 0, "사용자와 무리 identifikator_VALUE");
        yoxlamaq("/".equals(호출.현재작업목록(2)) && 호출.SWITCH_tapşırıq_siyahısı("/") == 0, "현재 작업 daxiletmə_Siyahı");
        yoxlamaq(호출.단말인가(부모, 1), "표준 출력 단말");
        yoxlamaq("JTurOS".equals(호출.체계정보().sistem_ad()), "əməliyyat_sistemi_VALUE msinfo32_exe");
    }

    private static void 실행파일시험(nüvə nüvə_VALUE) {
        byte[] verilənlər = new byte[92];
        verilənlər[0] = 0x7f;
        verilənlər[1] = 'E';
        verilənlər[2] = 'L';
        verilənlər[3] = 'F';
        verilənlər[4] = 1;
        verilənlər[5] = 1;
        yazmaq_tam_ədəd_VALUE(verilənlər, 24, 0x04001000);
        yazmaq_tam_ədəd_VALUE(verilənlər, 32, 52);
        짧은정수쓰기(verilənlər, 46, 40);
        짧은정수쓰기(verilənlər, 48, 1);
        yazmaq_tam_ədəd_VALUE(verilənlər, 56, 8);
        yazmaq_tam_ədəd_VALUE(verilənlər, 60, 2);
        yazmaq_tam_ədəd_VALUE(verilənlər, 64, 0x04002000);
        yazmaq_tam_ədəd_VALUE(verilənlər, 72, 64);

        실행파일적재기.IMAGE IMAGE_VALUE = new 실행파일적재기().검사(verilənlər);
        yoxlamaq(IMAGE_VALUE.başlama_ünvanı() == 0x04001000, "ELF İcra_Et ünvan");
        yoxlamaq(IMAGE_VALUE.구역들().size() == 1 && IMAGE_VALUE.구역들().get(0).종류() == 8, "ELF 빈 verilənlər bölmə_VALUE_366e0bfa");
        int 서술자 = nüvə_VALUE.체계호출().Aç(nüvə_VALUE.첫과정(), "시험", 체계호출.yalnız_oxunan_bayraq);
        yoxlamaq(nüvə_VALUE.체계호출().fayl_nəzarət(nüvə_VALUE.첫과정(), 서술자, 2, 1) == 0, "icra_etmək_əmr 시 Bağla Sazlama");
        yoxlamaq(nüvə_VALUE.체계호출().icra_etmək_əmr(nüvə_VALUE.첫과정(), verilənlər, new String[] {"시험", "값"}, new String[] {"Dil=한국어"}) == 0, "ELF icra_etmək_əmr IMAGE_VALUE 적재");
        yoxlamaq(nüvə_VALUE.첫과정().실행시작주소() == 0x04001000, "icra_etmək_əmr İcra_Et ünvan 반영");
        yoxlamaq(nüvə_VALUE.첫과정().실행인자().length == 2 && nüvə_VALUE.첫과정().환경값().length == 1, "icra_etmək_əmr 인자와 환경");
        yoxlamaq(!nüvə_VALUE.첫과정().파일서술자().열려있음(서술자), "icra_etmək_əmr 시 서술자 Bağla");
        yoxlamaq(nüvə_VALUE.쪽관리().바이트읽기(nüvə_VALUE.첫과정().ünvan_məkan(), 0x04002000) == 0, "빈 verilənlər bölmə_VALUE_366e0bfa 영 ilkin_qiymət_vermək");
    }

    private static void 입력시험(nüvə nüvə_VALUE) {
        nüvə_VALUE.입력관리().키누름('가');
        nüvə_VALUE.입력관리().쥐이동(3, -2);
        입력사건 첫사건 = nüvə_VALUE.입력관리().Sonrakı_hadisə();
        입력사건 SECOND_hadisə = nüvə_VALUE.입력관리().Sonrakı_hadisə();
        yoxlamaq(첫사건.사건종류() == 입력사건.종류.키누름, "자판 hadisə");
        yoxlamaq(SECOND_hadisə.첫째값() == 3 && SECOND_hadisə.SECOND_VALUE() == -2, "쥐 hərəkət_etdir_VALUE hadisə");
    }

    private static void 하드웨어시험(호스트하드웨어 cihaz_VALUE) {
        cihaz_VALUE.yazmaq_port_bayt(0x3f8, 0xab);
        yoxlamaq(cihaz_VALUE.포트바이트읽기(0x3f8) == 0xab, "포트 giriş_çıxış 경계");
        yoxlamaq(cihaz_VALUE.직렬기록().contains("JTurOS"), "직렬 LOG_yaz");
    }

    private static void 개입중단과서술자시험() {
        IRQ_menecer menecer_VALUE = new IRQ_menecer();
        menecer_VALUE.qeydiyyatdan_keçmək_daxiletmə(0x21, Yaddaş_ünvan -> Yaddaş_ünvan + 4);
        menecer_VALUE.aktivləşdirmək();
        yoxlamaq(menecer_VALUE.paylamaq_VALUE(0x21, 100) == 104, "IRQ paylamaq_VALUE");
        menecer_VALUE.qeyri_aktiv_etmək();
        yoxlamaq(menecer_VALUE.paylamaq_VALUE(0x21, 100) == 100, "IRQ qeyri_aktiv_etmək");

        전역서술자표 서술자표 = new 전역서술자표();
        서술자표.Dəst_standart_qiymət();
        yoxlamaq(서술자표.조각들().size() == 5, "전역 서술자표");
        tapşırıq_vəziyyət_seqment tapşırıq_vəziyyət = new tapşırıq_vəziyyət_seqment();
        tapşırıq_vəziyyət.특권쌓임공간설정(0x10, 0x800000);
        yoxlamaq(tapşırıq_vəziyyət.영번쌓임조각() == 0x10 && tapşırıq_vəziyyət.영번쌓임주소() == 0x800000, "작업 vəziyyət_VALUE bölmə_VALUE_366e0bfa");
    }

    private static void 저장장치와통신망시험() {
        고급기술결합장치 Yaddaş_cihaz = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.bölmə_ölçünü_dəyişmək];
        byte[] 읽은자료 = new byte[고급기술결합장치.bölmə_ölçünü_dəyişmək];
        쓸자료[17] = 42;
        Yaddaş_cihaz.Yazma(2, 쓸자료);
        Yaddaş_cihaz.Oxuma(2, 읽은자료);
        yoxlamaq(읽은자료[17] == 42, "ATA bölmə_VALUE_366e0bfa 읽고 Yazma");

        əlavə_qurğu_şin_menecer əlavə_qurğu = new əlavə_qurğu_şin_menecer();
        əlavə_qurğu.발견(new əlavə_qurğu_şin_menecer.cihaz_VALUE(0x1022, 0x2000, 0xc000, 11));
        yoxlamaq(əlavə_qurğu.FIND_daxiletmə(0x1022, 0x2000) != null, "주변 cihaz_VALUE FIND_daxiletmə");

        byte[] Ethernet_kadr = new byte[34];
        Ethernet_kadr[12] = 0x08;
        Ethernet_kadr[13] = 0x00;
        Ethernet_kadr[14] = 0x45;
        yoxlamaq(Şəbəkə_Alətlər.Ethernet_UPPER_protokol(Ethernet_kadr) == 0x0800, "이더넷 상위 müqavilə_VALUE");
        yoxlamaq(Şəbəkə_Alətlər.상호통신망규약사판인가(Ethernet_kadr, 14), "상호통신망규약 4판");
        yoxlamaq(Şəbəkə_Alətlər.인터넷검사합(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 검사합");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        yazmaq_tam_ədəd_VALUE(첫구역, 454, 63);
        yazmaq_tam_ədəd_VALUE(첫구역, 458, 1024);
        yoxlamaq(new 기본분할영역표().Oxuma(첫구역).size() == 1, "standart_qiymət 분할 영역표");

        Şəbəkə_lay lay_VALUE = new Şəbəkə_lay();
        int[] RECEIVED_COUNT = new int[1];
        lay_VALUE.qeydiyyatdan_keçmək_istifadəçi_verilənlər_dərs(7, (verilənlər, İcra_Et, uzunluq_VALUE) -> RECEIVED_COUNT[0]++);
        byte[] kadr_INDEX = new byte[14 + 20 + 8];
        kadr_INDEX[12] = 0x08;
        kadr_INDEX[13] = 0x00;
        kadr_INDEX[14] = 0x45;
        kadr_INDEX[16] = 0;
        kadr_INDEX[17] = 28;
        kadr_INDEX[23] = 17;
        kadr_INDEX[36] = 0;
        kadr_INDEX[37] = 7;
        yoxlamaq(lay_VALUE.이더넷받기(kadr_INDEX) && RECEIVED_COUNT[0] == 1, "istifadəçi verilənlər dərs_VALUE paylamaq_VALUE");
    }

    private static void 화면과시계시험() {
        simvol_displey 화면 = new simvol_displey();
        화면.출력("가나\n다");
        yoxlamaq(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 출력");
        Saat Saat = new Saat(100);
        for (int INDEX = 0; INDEX < 10; INDEX++) {
            Saat.틱();
        }
        yoxlamaq(Saat.지난밀리초() == 100, "Saat 틱 CONVERT_VALUE");
    }

    private static void yazmaq_tam_ədəd_VALUE(byte[] verilənlər, int yerinə_qoymaq, int VALUE) {
        verilənlər[yerinə_qoymaq] = (byte) VALUE;
        verilənlər[yerinə_qoymaq + 1] = (byte) (VALUE >>> 8);
        verilənlər[yerinə_qoymaq + 2] = (byte) (VALUE >>> 16);
        verilənlər[yerinə_qoymaq + 3] = (byte) (VALUE >>> 24);
    }

    private static void 짧은정수쓰기(byte[] verilənlər, int yerinə_qoymaq, int VALUE) {
        verilənlər[yerinə_qoymaq] = (byte) VALUE;
        verilənlər[yerinə_qoymaq + 1] = (byte) (VALUE >>> 8);
    }

    private static void yoxlamaq(boolean şərt, String Ad) {
        if (!şərt) {
            throw new AssertionError("xəta_VALUE: " + Ad);
        }
        ötürmək_COUNT++;
        System.out.println("ötürmək_VALUE: " + Ad);
    }
}
