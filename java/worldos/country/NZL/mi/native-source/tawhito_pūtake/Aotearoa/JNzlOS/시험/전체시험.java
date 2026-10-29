// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Aotearoa.JNzlOS.시험;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Aotearoa.JNzlOS.기억공간.Pūmahara_pouwhakahaere;
import Aotearoa.JNzlOS.기억공간.whārangi_pouwhakahaere;
import Aotearoa.JNzlOS.입력.입력사건;
import Aotearoa.JNzlOS.작업.Hātepe_uara;
import Aotearoa.JNzlOS.체계호출.체계호출;
import Aotearoa.JNzlOS.pūnaha_kōnae.실행파일적재기;
import Aotearoa.JNzlOS.kākano.kākano;
import Aotearoa.JNzlOS.taurima.호스트하드웨어;
import Aotearoa.JNzlOS.THK.THK_pouwhakahaere;
import Aotearoa.JNzlOS.서술자.전역서술자표;
import Aotearoa.JNzlOS.Rokiroki_pūkoro.고급기술결합장치;
import Aotearoa.JNzlOS.pūkoro_uara.apatoko_pahi_pouwhakahaere;
import Aotearoa.JNzlOS.whatunga_Huinga.whatunga_Ngā_Utauta;
import Aotearoa.JNzlOS.whatunga_Huinga.whatunga_apa;
import Aotearoa.JNzlOS.pūkoro_uara.Karaka;
import Aotearoa.JNzlOS.서술자.tūmahi_tūnga_tapahanga;
import Aotearoa.JNzlOS.화면.pūāhua_whakaatu;
import Aotearoa.JNzlOS.pūnaha_kōnae.기본분할영역표;

public final class 전체시험 {
    private static int whakawhiti_COUNT;

    private 전체시험() {
    }

    public static void main(String[] 인자) {
        호스트하드웨어 pūkoro_uara = new 호스트하드웨어();
        kākano kākano_uara_0611a8a8 = new kākano(pūkoro_uara);
        kākano_uara_0611a8a8.whakahaere();

        기억공간시험(kākano_uara_0611a8a8);
        쪽관리시험(kākano_uara_0611a8a8);
        파일과과정시험(kākano_uara_0611a8a8);
        실행파일시험(kākano_uara_0611a8a8);
        입력시험(kākano_uara_0611a8a8);
        하드웨어시험(pūkoro_uara);
        개입중단과서술자시험();
        저장장치와통신망시험();
        화면과시계시험();

        System.out.println("JNzlOS 시험 whakawhiti_uara: " + whakawhiti_COUNT);
    }

    private static void 기억공간시험(kākano kākano_uara_0611a8a8) {
        Pūmahara_pouwhakahaere pouwhakahaere_uara = kākano_uara_0611a8a8.기억공간();
        int 첫주소 = pouwhakahaere_uara.정렬할당(100, 64);
        manatoko((첫주소 & 63) == 0, "tiaro_uara tiritiri_Rokiroki");
        pouwhakahaere_uara.tuhi_paita_uara(첫주소, (byte) 0x5a);
        manatoko(pouwhakahaere_uara.바이트읽기(첫주소) == (byte) 0x5a, "물리 기억공간 읽고 Tuhia");
        int 사용전 = pouwhakahaere_uara.사용크기();
        pouwhakahaere_uara.tuku_Rokiroki(첫주소);
        manatoko(pouwhakahaere_uara.사용크기() < 사용전, "기억공간 tuku_Rokiroki");
    }

    private static void 쪽관리시험(kākano kākano_uara_0611a8a8) {
        whārangi_pouwhakahaere pouwhakahaere_uara = kākano_uara_0611a8a8.쪽관리();
        whārangi_pouwhakahaere.ADDRESS_wāhi 부모공간 = pouwhakahaere_uara.새주소공간();
        pouwhakahaere_uara.MAPI_whārangi(부모공간, 0x1000, true);
        pouwhakahaere_uara.tuhi_paita_uara(부모공간, 0x1010, (byte) 7);
        whārangi_pouwhakahaere.ADDRESS_wāhi tamaiti_wāhi = pouwhakahaere_uara.쓰기시복사복제(부모공간);
        pouwhakahaere_uara.tuhi_paita_uara(tamaiti_wāhi, 0x1010, (byte) 9);
        manatoko(pouwhakahaere_uara.바이트읽기(부모공간, 0x1010) == 7, "Tuhia 시 tārua_uara 부모 격리");
        manatoko(pouwhakahaere_uara.바이트읽기(tamaiti_wāhi, 0x1010) == 9, "Tuhia 시 tārua_uara tamaiti_uara Tuhia");
    }

    private static void 파일과과정시험(kākano kākano_uara_0611a8a8) {
        byte[] Ihirangi_uara = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        kākano_uara_0611a8a8.pūnaha_kōnae().파일추가("시험", Ihirangi_uara);
        Hātepe_uara 부모 = kākano_uara_0611a8a8.첫과정();
        체계호출 호출 = kākano_uara_0611a8a8.체계호출();
        int 서술자 = 호출.Huaki(부모, "/시험", 체계호출.pānui_anake_kara);
        manatoko(서술자 >= 3, "Kōnae Huaki");

        byte[] 받을곳 = new byte[Ihirangi_uara.length];
        manatoko(호출.Pānuitia(부모, 서술자, 받을곳, 받을곳.length) == Ihirangi_uara.length, "Kōnae Pānuitia");
        manatoko(Arrays.equals(Ihirangi_uara, 받을곳), "Kōnae Ihirangi_uara");
        manatoko(호출.nuku_tūranga(부모, 서술자, 0, 체계호출.Rapu_Start) == 0, "Kōnae tūranga nuku_uara");

        int 복제서술자 = 호출.서술자복제(부모, 서술자);
        manatoko(복제서술자 >= 0, "서술자 복제");
        Hātepe_uara tamaiti_uara = 호출.과정복제(부모);
        manatoko(tamaiti_uara.pūtāutu_uara() != 부모.pūtāutu_uara(), "Hātepe_uara pūtāutu_uara 분리");
        manatoko(tamaiti_uara.부모식별자() == 부모.pūtāutu_uara(), "부모 Hātepe_uara pūtāutu_uara");
        manatoko(호출.Kati(tamaiti_uara, 서술자) == 0 && 부모.파일서술자().열려있음(서술자), "tamaiti_uara Kati 격리");

        int 이전끝 = 호출.프로그램끝늘리기(부모, 8192);
        manatoko(이전끝 == 0x06000000, "kaupapa_f5044b9b 끝 늘리기");
        manatoko(부모.프로그램끝() == 0x06002000, "kaupapa_f5044b9b 끝 반영");
        manatoko(tamaiti_uara.프로그램끝() == 0x06000000, "과정별 kaupapa_f5044b9b 끝 격리");

        tamaiti_uara.Putaatu_kaupapa(7);
        manatoko(호출.자식기다리기(부모, tamaiti_uara.pūtāutu_uara(), false) == (7 << 8), "tamaiti_uara Putaatu_kaupapa 기다리기");
        manatoko(호출.접근가능("시험", 1) == -13, "kawe_tono mana_uru_uara 거부");
        manatoko(호출.kaiwhakamahi_pūtāutu() == 0 && 호출.rōpū_pūtāutu() == 0, "사용자와 무리 pūtāutu_uara");
        manatoko("/".equals(호출.현재작업목록(2)) && 호출.SWITCH_rārangi_tūmahi("/") == 0, "현재 작업 tāurunga_Rārangi");
        manatoko(호출.단말인가(부모, 1), "표준 출력 단말");
        manatoko("JNzlOS".equals(호출.체계정보().pūnaha_ingoa()), "pūnaha_mahi_uara msinfo32_exe");
    }

    private static void 실행파일시험(kākano kākano_uara_0611a8a8) {
        byte[] raraunga = new byte[92];
        raraunga[0] = 0x7f;
        raraunga[1] = 'E';
        raraunga[2] = 'L';
        raraunga[3] = 'F';
        raraunga[4] = 1;
        raraunga[5] = 1;
        tuhi_tau_tōpū_uara(raraunga, 24, 0x04001000);
        tuhi_tau_tōpū_uara(raraunga, 32, 52);
        짧은정수쓰기(raraunga, 46, 40);
        짧은정수쓰기(raraunga, 48, 1);
        tuhi_tau_tōpū_uara(raraunga, 56, 8);
        tuhi_tau_tōpū_uara(raraunga, 60, 2);
        tuhi_tau_tōpū_uara(raraunga, 64, 0x04002000);
        tuhi_tau_tōpū_uara(raraunga, 72, 64);

        실행파일적재기.IMAGE IMAGE_uara = new 실행파일적재기().검사(raraunga);
        manatoko(IMAGE_uara.Start_ADDRESS() == 0x04001000, "ELF whakahaere ADDRESS");
        manatoko(IMAGE_uara.구역들().size() == 1 && IMAGE_uara.구역들().get(0).종류() == 8, "ELF 빈 raraunga wāhanga_uara");
        int 서술자 = kākano_uara_0611a8a8.체계호출().Huaki(kākano_uara_0611a8a8.첫과정(), "시험", 체계호출.pānui_anake_kara);
        manatoko(kākano_uara_0611a8a8.체계호출().kōnae_mana(kākano_uara_0611a8a8.첫과정(), 서술자, 2, 1) == 0, "kawe_tono 시 Kati Ngā_Tautuhinga");
        manatoko(kākano_uara_0611a8a8.체계호출().kawe_tono(kākano_uara_0611a8a8.첫과정(), raraunga, new String[] {"시험", "값"}, new String[] {"reo=Reo_Māori"}) == 0, "ELF kawe_tono IMAGE_uara 적재");
        manatoko(kākano_uara_0611a8a8.첫과정().실행시작주소() == 0x04001000, "kawe_tono whakahaere ADDRESS 반영");
        manatoko(kākano_uara_0611a8a8.첫과정().실행인자().length == 2 && kākano_uara_0611a8a8.첫과정().환경값().length == 1, "kawe_tono 인자와 환경");
        manatoko(!kākano_uara_0611a8a8.첫과정().파일서술자().열려있음(서술자), "kawe_tono 시 서술자 Kati");
        manatoko(kākano_uara_0611a8a8.쪽관리().바이트읽기(kākano_uara_0611a8a8.첫과정().ADDRESS_wāhi(), 0x04002000) == 0, "빈 raraunga wāhanga_uara 영 arawhiti");
    }

    private static void 입력시험(kākano kākano_uara_0611a8a8) {
        kākano_uara_0611a8a8.입력관리().키누름('가');
        kākano_uara_0611a8a8.입력관리().쥐이동(3, -2);
        입력사건 첫사건 = kākano_uara_0611a8a8.입력관리().Panuku_hui();
        입력사건 SECOND_hui = kākano_uara_0611a8a8.입력관리().Panuku_hui();
        manatoko(첫사건.사건종류() == 입력사건.종류.키누름, "자판 hui");
        manatoko(SECOND_hui.첫째값() == 3 && SECOND_hui.SECOND_uara() == -2, "쥐 nuku_uara hui");
    }

    private static void 하드웨어시험(호스트하드웨어 pūkoro_uara) {
        pūkoro_uara.tuhi_kawe_paita(0x3f8, 0xab);
        manatoko(pūkoro_uara.포트바이트읽기(0x3f8) == 0xab, "포트 I_O 경계");
        manatoko(pūkoro_uara.직렬기록().contains("JNzlOS"), "직렬 LOG_RECORD");
    }

    private static void 개입중단과서술자시험() {
        THK_pouwhakahaere pouwhakahaere_uara = new THK_pouwhakahaere();
        pouwhakahaere_uara.rēhita_tāurunga(0x21, Rokiroki_ADDRESS -> Rokiroki_ADDRESS + 4);
        pouwhakahaere_uara.whakahohe();
        manatoko(pouwhakahaere_uara.hora_uara(0x21, 100) == 104, "THK hora_uara");
        pouwhakahaere_uara.taupāhohe();
        manatoko(pouwhakahaere_uara.hora_uara(0x21, 100) == 100, "THK taupāhohe");

        전역서술자표 서술자표 = new 전역서술자표();
        서술자표.huinga_uara_taunoa();
        manatoko(서술자표.조각들().size() == 5, "전역 서술자표");
        tūmahi_tūnga_tapahanga tūmahi_tūnga = new tūmahi_tūnga_tapahanga();
        tūmahi_tūnga.특권쌓임공간설정(0x10, 0x800000);
        manatoko(tūmahi_tūnga.영번쌓임조각() == 0x10 && tūmahi_tūnga.영번쌓임주소() == 0x800000, "작업 tūnga_uara wāhanga_uara");
    }

    private static void 저장장치와통신망시험() {
        고급기술결합장치 Rokiroki_pūkoro = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.wāhanga_rahi];
        byte[] 읽은자료 = new byte[고급기술결합장치.wāhanga_rahi];
        쓸자료[17] = 42;
        Rokiroki_pūkoro.Tuhia(2, 쓸자료);
        Rokiroki_pūkoro.Pānuitia(2, 읽은자료);
        manatoko(읽은자료[17] == 42, "ATA wāhanga_uara 읽고 Tuhia");

        apatoko_pahi_pouwhakahaere apatoko = new apatoko_pahi_pouwhakahaere();
        apatoko.발견(new apatoko_pahi_pouwhakahaere.pūkoro_uara(0x1022, 0x2000, 0xc000, 11));
        manatoko(apatoko.FIND_tāurunga(0x1022, 0x2000) != null, "주변 pūkoro_uara FIND_tāurunga");

        byte[] Itarangi_tāpare = new byte[34];
        Itarangi_tāpare[12] = 0x08;
        Itarangi_tāpare[13] = 0x00;
        Itarangi_tāpare[14] = 0x45;
        manatoko(whatunga_Ngā_Utauta.Itarangi_UPPER_kawa(Itarangi_tāpare) == 0x0800, "이더넷 상위 kēhi_uara");
        manatoko(whatunga_Ngā_Utauta.상호통신망규약사판인가(Itarangi_tāpare, 14), "상호통신망규약 4판");
        manatoko(whatunga_Ngā_Utauta.인터넷검사합(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 검사합");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        tuhi_tau_tōpū_uara(첫구역, 454, 63);
        tuhi_tau_tōpū_uara(첫구역, 458, 1024);
        manatoko(new 기본분할영역표().Pānuitia(첫구역).size() == 1, "uara_taunoa 분할 영역표");

        whatunga_apa apa_uara = new whatunga_apa();
        int[] RECEIVED_COUNT = new int[1];
        apa_uara.rēhita_kaiwhakamahi_raraunga_ngā_wae(7, (raraunga, whakahaere, roa_uara) -> RECEIVED_COUNT[0]++);
        byte[] tāpare_INDEX = new byte[14 + 20 + 8];
        tāpare_INDEX[12] = 0x08;
        tāpare_INDEX[13] = 0x00;
        tāpare_INDEX[14] = 0x45;
        tāpare_INDEX[16] = 0;
        tāpare_INDEX[17] = 28;
        tāpare_INDEX[23] = 17;
        tāpare_INDEX[36] = 0;
        tāpare_INDEX[37] = 7;
        manatoko(apa_uara.이더넷받기(tāpare_INDEX) && RECEIVED_COUNT[0] == 1, "kaiwhakamahi raraunga ngā_wae_uara hora_uara");
    }

    private static void 화면과시계시험() {
        pūāhua_whakaatu 화면 = new pūāhua_whakaatu();
        화면.출력("가나\n다");
        manatoko(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 출력");
        Karaka Karaka = new Karaka(100);
        for (int INDEX = 0; INDEX < 10; INDEX++) {
            Karaka.틱();
        }
        manatoko(Karaka.지난밀리초() == 100, "Karaka 틱 CONVERT_uara");
    }

    private static void tuhi_tau_tōpū_uara(byte[] raraunga, int tūranga, int uara) {
        raraunga[tūranga] = (byte) uara;
        raraunga[tūranga + 1] = (byte) (uara >>> 8);
        raraunga[tūranga + 2] = (byte) (uara >>> 16);
        raraunga[tūranga + 3] = (byte) (uara >>> 24);
    }

    private static void 짧은정수쓰기(byte[] raraunga, int tūranga, int uara) {
        raraunga[tūranga] = (byte) uara;
        raraunga[tūranga + 1] = (byte) (uara >>> 8);
    }

    private static void manatoko(boolean here, String Ingoa) {
        if (!here) {
            throw new AssertionError("rahunga_uara: " + Ingoa);
        }
        whakawhiti_COUNT++;
        System.out.println("whakawhiti_uara: " + Ingoa);
    }
}
