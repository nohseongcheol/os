// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Szlovénia.JSvnOS.시험;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Szlovénia.JSvnOS.Memória_régió.Memória_kezelő;
import Szlovénia.JSvnOS.Memória_régió.lap_kezelő;
import Szlovénia.JSvnOS.bevitel_ÉRTÉK.bevitel_esemény;
import Szlovénia.JSvnOS.작업.folyamat_ÉRTÉK;
import Szlovénia.JSvnOS.체계호출.체계호출;
import Szlovénia.JSvnOS.fájlrendszer.végrehajtható_betöltő;
import Szlovénia.JSvnOS.kernel.kernel;
import Szlovénia.JSvnOS.gazda.gazda_hardver;
import Szlovénia.JSvnOS.megszakítás.megszakítás_kezelő;
import Szlovénia.JSvnOS.서술자.globális_leírótábla;
import Szlovénia.JSvnOS.tárolóeszköz.고급기술결합장치;
import Szlovénia.JSvnOS.mobil_ÉRTÉK.tartozék_busz_kezelő;
import Szlovénia.JSvnOS.hálózat_Sor.hálózat_Eszközök;
import Szlovénia.JSvnOS.hálózat_Sor.hálózati_réteg;
import Szlovénia.JSvnOS.mobil_ÉRTÉK.Óra;
import Szlovénia.JSvnOS.서술자.teendő_Állapot_szegmens;
import Szlovénia.JSvnOS.화면.karakter_kijelző;
import Szlovénia.JSvnOS.fájlrendszer.elsődleges_partíció_tábla;

public final class 전체시험 {
    private static int továbbít_DARAB;

    private 전체시험() {
    }

    public static void main(String[] paraméter_argumentum) {
        gazda_hardver mobil_ÉRTÉK = new gazda_hardver();
        kernel kernel_ÉRTÉK = new kernel(mobil_ÉRTÉK);
        kernel_ÉRTÉK.Futtatás();

        teszt_Memória(kernel_ÉRTÉK);
        쪽관리시험(kernel_ÉRTÉK);
        파일과과정시험(kernel_ÉRTÉK);
        실행파일시험(kernel_ÉRTÉK);
        teszt_bevitel(kernel_ÉRTÉK);
        teszt_hardver(mobil_ÉRTÉK);
        개입중단과서술자시험();
        teszt_tár_ÉS_hálózat();
        화면과시계시험();

        System.out.println("JSvnOS 시험 továbbít_ÉRTÉK: " + továbbít_DARAB);
    }

    private static void teszt_Memória(kernel kernel_ÉRTÉK) {
        Memória_kezelő kezelő_ÉRTÉK = kernel_ÉRTÉK.Memória_régió();
        int 첫주소 = kezelő_ÉRTÉK.정렬할당(100, 64);
        igazol((첫주소 & 63) == 0, "igazít_ÉRTÉK kioszt_tár");
        kezelő_ÉRTÉK.ír_bájt_ÉRTÉK(첫주소, (byte) 0x5a);
        igazol(kezelő_ÉRTÉK.바이트읽기(첫주소) == (byte) 0x5a, "물리 Memória_régió 읽고 Írás");
        int 사용전 = kezelő_ÉRTÉK.사용크기();
        kezelő_ÉRTÉK.kiad_tár(첫주소);
        igazol(kezelő_ÉRTÉK.사용크기() < 사용전, "Memória_régió kiad_tár");
    }

    private static void 쪽관리시험(kernel kernel_ÉRTÉK) {
        lap_kezelő kezelő_ÉRTÉK = kernel_ÉRTÉK.쪽관리();
        lap_kezelő.címtartomány szülő_tér = kezelő_ÉRTÉK.새주소공간();
        kezelő_ÉRTÉK.MAP_lap(szülő_tér, 0x1000, true);
        kezelő_ÉRTÉK.ír_bájt_ÉRTÉK(szülő_tér, 0x1010, (byte) 7);
        lap_kezelő.címtartomány gyermek_tér = kezelő_ÉRTÉK.쓰기시복사복제(szülő_tér);
        kezelő_ÉRTÉK.ír_bájt_ÉRTÉK(gyermek_tér, 0x1010, (byte) 9);
        igazol(kezelő_ÉRTÉK.바이트읽기(szülő_tér, 0x1010) == 7, "Írás 시 másol_ÉRTÉK szülő_ÉRTÉK 격리");
        igazol(kezelő_ÉRTÉK.바이트읽기(gyermek_tér, 0x1010) == 9, "Írás 시 másol_ÉRTÉK gyermek_ÉRTÉK Írás");
    }

    private static void 파일과과정시험(kernel kernel_ÉRTÉK) {
        byte[] Tartalom_ÉRTÉK = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        kernel_ÉRTÉK.fájlrendszer().hozzáfűz_Fájl("시험", Tartalom_ÉRTÉK);
        folyamat_ÉRTÉK szülő_ÉRTÉK = kernel_ÉRTÉK.첫과정();
        체계호출 호출 = kernel_ÉRTÉK.체계호출();
        int 서술자 = 호출.Megnyitás(szülő_ÉRTÉK, "/시험", 체계호출.írásvédett_jelölő);
        igazol(서술자 >= 3, "Fájl Megnyitás");

        byte[] fogad_cél = new byte[Tartalom_ÉRTÉK.length];
        igazol(호출.Olvasás(szülő_ÉRTÉK, 서술자, fogad_cél, fogad_cél.length) == Tartalom_ÉRTÉK.length, "Fájl Olvasás");
        igazol(Arrays.equals(Tartalom_ÉRTÉK, fogad_cél), "Fájl Tartalom_ÉRTÉK");
        igazol(호출.áthelyez_pozíció(szülő_ÉRTÉK, 서술자, 0, 체계호출.keres_START) == 0, "Fájl Pozíció áthelyez_ÉRTÉK");

        int 복제서술자 = 호출.서술자복제(szülő_ÉRTÉK, 서술자);
        igazol(복제서술자 >= 0, "서술자 klón_ÉRTÉK");
        folyamat_ÉRTÉK gyermek_ÉRTÉK = 호출.klón_folyamat(szülő_ÉRTÉK);
        igazol(gyermek_ÉRTÉK.azonosító_ÉRTÉK() != szülő_ÉRTÉK.azonosító_ÉRTÉK(), "folyamat_ÉRTÉK azonosító_ÉRTÉK 분리");
        igazol(gyermek_ÉRTÉK.szülő_azonosító() == szülő_ÉRTÉK.azonosító_ÉRTÉK(), "szülő_ÉRTÉK folyamat_ÉRTÉK azonosító_ÉRTÉK");
        igazol(호출.Bezárás(gyermek_ÉRTÉK, 서술자) == 0 && szülő_ÉRTÉK.파일서술자().informatikai_részleg_készít(서술자), "gyermek_ÉRTÉK Bezárás 격리");

        int Előző_megszüntet = 호출.növelés_app_szünet(szülő_ÉRTÉK, 8192);
        igazol(Előző_megszüntet == 0x06000000, "app_f5044b9b 끝 늘리기");
        igazol(szülő_ÉRTÉK.app_szünet() == 0x06002000, "app_f5044b9b 끝 반영");
        igazol(gyermek_ÉRTÉK.app_szünet() == 0x06000000, "과정별 app_f5044b9b 끝 격리");

        gyermek_ÉRTÉK.kilép_app(7);
        igazol(호출.자식기다리기(szülő_ÉRTÉK, gyermek_ÉRTÉK.azonosító_ÉRTÉK(), false) == (7 << 8), "gyermek_ÉRTÉK kilép_app 기다리기");
        igazol(호출.접근가능("시험", 1) == -13, "végrehajt_parancs engedély_ÉRTÉK elutasít_ÉRTÉK");
        igazol(호출.felhasználóazonosító() == 0 && 호출.GID() == 0, "사용자와 무리 azonosító_ÉRTÉK");
        igazol("/".equals(호출.aktuális_Feladatlista(2)) && 호출.vált_Feladatlista("/") == 0, "aktuális_cikk 작업 bejegyzés_Lista");
        igazol(호출.informatikai_részleg_Terminál(szülő_ÉRTÉK, 1), "표준 Kimenet 단말");
        igazol("JSvnOS".equals(호출.Rendszer_Részletek().Rendszer_név()), "operációs_rendszer_ÉRTÉK msinfo32_exe");
    }

    private static void 실행파일시험(kernel kernel_ÉRTÉK) {
        byte[] adat = new byte[92];
        adat[0] = 0x7f;
        adat[1] = 'E';
        adat[2] = 'L';
        adat[3] = 'F';
        adat[4] = 1;
        adat[5] = 1;
        ír_egész_szám_ÉRTÉK(adat, 24, 0x04001000);
        ír_egész_szám_ÉRTÉK(adat, 32, 52);
        짧은정수쓰기(adat, 46, 40);
        짧은정수쓰기(adat, 48, 1);
        ír_egész_szám_ÉRTÉK(adat, 56, 8);
        ír_egész_szám_ÉRTÉK(adat, 60, 2);
        ír_egész_szám_ÉRTÉK(adat, 64, 0x04002000);
        ír_egész_szám_ÉRTÉK(adat, 72, 64);

        végrehajtható_betöltő.KÉP KÉP_ÉRTÉK = new végrehajtható_betöltő().검사(adat);
        igazol(KÉP_ÉRTÉK.START_CÍM() == 0x04001000, "ELF Futtatás CÍM");
        igazol(KÉP_ÉRTÉK.구역들().size() == 1 && KÉP_ÉRTÉK.구역들().get(0).Altípus_ÉRTÉK() == 8, "ELF 빈 adat szakasz_ÉRTÉK");
        int 서술자 = kernel_ÉRTÉK.체계호출().Megnyitás(kernel_ÉRTÉK.첫과정(), "시험", 체계호출.írásvédett_jelölő);
        igazol(kernel_ÉRTÉK.체계호출().Fájl_vezérlő(kernel_ÉRTÉK.첫과정(), 서술자, 2, 1) == 0, "végrehajt_parancs 시 Bezárás Beállítások");
        igazol(kernel_ÉRTÉK.체계호출().végrehajt_parancs(kernel_ÉRTÉK.첫과정(), adat, new String[] {"시험", "값"}, new String[] {"Nyelv=magyar"}) == 0, "ELF végrehajt_parancs KÉP_ÉRTÉK 적재");
        igazol(kernel_ÉRTÉK.첫과정().végrehajtás_START_CÍM() == 0x04001000, "végrehajt_parancs Futtatás CÍM 반영");
        igazol(kernel_ÉRTÉK.첫과정().végrehajtás_argumentum().length == 2 && kernel_ÉRTÉK.첫과정().környezet_ÉRTÉK_60cdc2a6().length == 1, "végrehajt_parancs 인자와 környezet_5d36e09c");
        igazol(!kernel_ÉRTÉK.첫과정().파일서술자().informatikai_részleg_készít(서술자), "végrehajt_parancs 시 서술자 Bezárás");
        igazol(kernel_ÉRTÉK.쪽관리().바이트읽기(kernel_ÉRTÉK.첫과정().címtartomány(), 0x04002000) == 0, "빈 adat szakasz_ÉRTÉK nulla_operandus inicializál");
    }

    private static void teszt_bevitel(kernel kernel_ÉRTÉK) {
        kernel_ÉRTÉK.입력관리().키누름('가');
        kernel_ÉRTÉK.입력관리().쥐이동(3, -2);
        bevitel_esemény 첫사건 = kernel_ÉRTÉK.입력관리().Tovább_esemény();
        bevitel_esemény MPERC_esemény = kernel_ÉRTÉK.입력관리().Tovább_esemény();
        igazol(첫사건.eseményfajta() == bevitel_esemény.Altípus_ÉRTÉK.키누름, "자판 Esemény");
        igazol(MPERC_esemény.첫째값() == 3 && MPERC_esemény.MPERC_ÉRTÉK() == -2, "쥐 áthelyez_ÉRTÉK Esemény");
    }

    private static void teszt_hardver(gazda_hardver mobil_ÉRTÉK) {
        mobil_ÉRTÉK.ír_port_bájt(0x3f8, 0xab);
        igazol(mobil_ÉRTÉK.포트바이트읽기(0x3f8) == 0xab, "hardver_port I_O határ_ÉRTÉK");
        igazol(mobil_ÉRTÉK.직렬기록().contains("JSvnOS"), "직렬 LOG_REKORD");
    }

    private static void 개입중단과서술자시험() {
        megszakítás_kezelő kezelő_ÉRTÉK = new megszakítás_kezelő();
        kezelő_ÉRTÉK.jegyzék_bejegyzés(0x21, tár_CÍM -> tár_CÍM + 4);
        kezelő_ÉRTÉK.bekapcsol();
        igazol(kezelő_ÉRTÉK.eloszt_ÉRTÉK(0x21, 100) == 104, "megszakítás eloszt_ÉRTÉK");
        kezelő_ÉRTÉK.inaktivál();
        igazol(kezelő_ÉRTÉK.eloszt_ÉRTÉK(0x21, 100) == 100, "megszakítás inaktivál");

        globális_leírótábla 서술자표 = new globális_leírótábla();
        서술자표.halmaz_alapértelmezett_érték();
        igazol(서술자표.조각들().size() == 5, "전역 서술자표");
        teendő_Állapot_szegmens teendő_Állapot = new teendő_Állapot_szegmens();
        teendő_Állapot.특권쌓임공간설정(0x10, 0x800000);
        igazol(teendő_Állapot.Sor_nulla_blokk() == 0x10 && teendő_Állapot.Sor_nulla_CÍM() == 0x800000, "작업 Állapot_ÉRTÉK szakasz_ÉRTÉK");
    }

    private static void teszt_tár_ÉS_hálózat() {
        고급기술결합장치 tárolóeszköz = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.szakasz_méretez];
        byte[] 읽은자료 = new byte[고급기술결합장치.szakasz_méretez];
        쓸자료[17] = 42;
        tárolóeszköz.Írás(2, 쓸자료);
        tárolóeszköz.Olvasás(2, 읽은자료);
        igazol(읽은자료[17] == 42, "ATA szakasz_ÉRTÉK 읽고 Írás");

        tartozék_busz_kezelő tartozék = new tartozék_busz_kezelő();
        tartozék.발견(new tartozék_busz_kezelő.mobil_ÉRTÉK(0x1022, 0x2000, 0xc000, 11));
        igazol(tartozék.keres_bejegyzés(0x1022, 0x2000) != null, "주변 mobil_ÉRTÉK keres_bejegyzés");

        byte[] Ethernet_doboz = new byte[34];
        Ethernet_doboz[12] = 0x08;
        Ethernet_doboz[13] = 0x00;
        Ethernet_doboz[14] = 0x45;
        igazol(hálózat_Eszközök.Ethernet_NAGYBETŰS_protokoll(Ethernet_doboz) == 0x0800, "이더넷 상위 szerződés_értéke");
        igazol(hálózat_Eszközök.informatikai_részleg_számlázási_árkülönbözet_4_protokoll(Ethernet_doboz, 14), "상호통신망규약 4판");
        igazol(hálózat_Eszközök.háló_ellenőrzőösszeg(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 ellenőrzőösszeg");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        ír_egész_szám_ÉRTÉK(첫구역, 454, 63);
        ír_egész_szám_ÉRTÉK(첫구역, 458, 1024);
        igazol(new elsődleges_partíció_tábla().Olvasás(첫구역).size() == 1, "alapértelmezett_érték 분할 영역표");

        hálózati_réteg réteg_ÉRTÉK = new hálózati_réteg();
        int[] KAPOTT_DARAB = new int[1];
        réteg_ÉRTÉK.jegyzék_felhasználó_adat_lecke(7, (adat, Futtatás, hossz_ÉRTÉK) -> KAPOTT_DARAB[0]++);
        byte[] doboz_INDEX = new byte[14 + 20 + 8];
        doboz_INDEX[12] = 0x08;
        doboz_INDEX[13] = 0x00;
        doboz_INDEX[14] = 0x45;
        doboz_INDEX[16] = 0;
        doboz_INDEX[17] = 28;
        doboz_INDEX[23] = 17;
        doboz_INDEX[36] = 0;
        doboz_INDEX[37] = 7;
        igazol(réteg_ÉRTÉK.fogad_Ethernet(doboz_INDEX) && KAPOTT_DARAB[0] == 1, "felhasználó adat lecke_ÉRTÉK eloszt_ÉRTÉK");
    }

    private static void 화면과시계시험() {
        karakter_kijelző 화면 = new karakter_kijelző();
        화면.Kimenet("가나\n다");
        igazol(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 Kimenet");
        Óra Óra = new Óra(100);
        for (int INDEX = 0; INDEX < 10; INDEX++) {
            Óra.órajel_ÉRTÉK();
        }
        igazol(Óra.지난밀리초() == 100, "Óra órajel_ÉRTÉK konvertál_ÉRTÉK");
    }

    private static void ír_egész_szám_ÉRTÉK(byte[] adat, int Pozíció, int ÉRTÉK) {
        adat[Pozíció] = (byte) ÉRTÉK;
        adat[Pozíció + 1] = (byte) (ÉRTÉK >>> 8);
        adat[Pozíció + 2] = (byte) (ÉRTÉK >>> 16);
        adat[Pozíció + 3] = (byte) (ÉRTÉK >>> 24);
    }

    private static void 짧은정수쓰기(byte[] adat, int Pozíció, int ÉRTÉK) {
        adat[Pozíció] = (byte) ÉRTÉK;
        adat[Pozíció + 1] = (byte) (ÉRTÉK >>> 8);
    }

    private static void igazol(boolean állapot, String Név) {
        if (!állapot) {
            throw new AssertionError("hiba_ÉRTÉK: " + Név);
        }
        továbbít_DARAB++;
        System.out.println("továbbít_ÉRTÉK: " + Név);
    }
}
