// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Brunei.JBrnOS.ujian;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Brunei.JBrnOS.Memori_rantau.Memori_pengurus;
import Brunei.JBrnOS.Memori_rantau.halaman_pengurus;
import Brunei.JBrnOS.입력.입력사건;
import Brunei.JBrnOS.작업.Proses_VALUE;
import Brunei.JBrnOS.panggilan_sistem.panggilan_sistem;
import Brunei.JBrnOS.sistem_fail.실행파일적재기;
import Brunei.JBrnOS.kernel.kernel;
import Brunei.JBrnOS.hos.호스트하드웨어;
import Brunei.JBrnOS.IRQ.IRQ_pengurus;
import Brunei.JBrnOS.서술자.전역서술자표;
import Brunei.JBrnOS.Storan_peranti.고급기술결합장치;
import Brunei.JBrnOS.peranti_VALUE.aksesori_bas_pengurus;
import Brunei.JBrnOS.rangkaian_tindan.rangkaian_Alat;
import Brunei.JBrnOS.rangkaian_tindan.rangkaian_lapisan;
import Brunei.JBrnOS.peranti_VALUE.Jam;
import Brunei.JBrnOS.서술자.tugas_status_segmen;
import Brunei.JBrnOS.화면.aksara_papar;
import Brunei.JBrnOS.sistem_fail.기본분할영역표;

public final class 전체시험 {
    private static int hantar_COUNT;

    private 전체시험() {
    }

    public static void main(String[] parameter_argumen) {
        호스트하드웨어 peranti_VALUE = new 호스트하드웨어();
        kernel kernel_VALUE = new kernel(peranti_VALUE);
        kernel_VALUE.Jalan();

        ujian_Memori(kernel_VALUE);
        쪽관리시험(kernel_VALUE);
        파일과과정시험(kernel_VALUE);
        실행파일시험(kernel_VALUE);
        입력시험(kernel_VALUE);
        하드웨어시험(peranti_VALUE);
        개입중단과서술자시험();
        ujian_Storan_AND_Rangkaian();
        화면과시계시험();

        System.out.println("JBrnOS ujian hantar_VALUE: " + hantar_COUNT);
    }

    private static void ujian_Memori(kernel kernel_VALUE) {
        Memori_pengurus pengurus_VALUE = kernel_VALUE.Memori_rantau();
        int 첫주소 = pengurus_VALUE.정렬할당(100, 64);
        tentu_sahkan((첫주소 & 63) == 0, "jajar_VALUE peruntuk_Storan");
        pengurus_VALUE.tulis_bait_VALUE(첫주소, (byte) 0x5a);
        tentu_sahkan(pengurus_VALUE.바이트읽기(첫주소) == (byte) 0x5a, "물리 Memori_rantau 읽고 Tulis");
        int 사용전 = pengurus_VALUE.사용크기();
        pengurus_VALUE.keluaran_Storan(첫주소);
        tentu_sahkan(pengurus_VALUE.사용크기() < 사용전, "Memori_rantau keluaran_Storan");
    }

    private static void 쪽관리시험(kernel kernel_VALUE) {
        halaman_pengurus pengurus_VALUE = kernel_VALUE.쪽관리();
        halaman_pengurus.e_mel_SPACE 부모공간 = pengurus_VALUE.새주소공간();
        pengurus_VALUE.MAP_halaman(부모공간, 0x1000, true);
        pengurus_VALUE.tulis_bait_VALUE(부모공간, 0x1010, (byte) 7);
        halaman_pengurus.e_mel_SPACE anak_SPACE = pengurus_VALUE.klon_COW(부모공간);
        pengurus_VALUE.tulis_bait_VALUE(anak_SPACE, 0x1010, (byte) 9);
        tentu_sahkan(pengurus_VALUE.바이트읽기(부모공간, 0x1010) == 7, "Tulis 시 tika_VALUE 부모 격리");
        tentu_sahkan(pengurus_VALUE.바이트읽기(anak_SPACE, 0x1010) == 9, "Tulis 시 tika_VALUE anak_VALUE Tulis");
    }

    private static void 파일과과정시험(kernel kernel_VALUE) {
        byte[] Kandungan_VALUE = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        kernel_VALUE.sistem_fail().Tambah_fail("ujian", Kandungan_VALUE);
        Proses_VALUE 부모 = kernel_VALUE.첫과정();
        panggilan_sistem 호출 = kernel_VALUE.panggilan_sistem();
        int 서술자 = 호출.Buka(부모, "/ujian", panggilan_sistem.baca_sahaja_bendera);
        tentu_sahkan(서술자 >= 3, "Fail Buka");

        byte[] 받을곳 = new byte[Kandungan_VALUE.length];
        tentu_sahkan(호출.Baca(부모, 서술자, 받을곳, 받을곳.length) == Kandungan_VALUE.length, "Fail Baca");
        tentu_sahkan(Arrays.equals(Kandungan_VALUE, 받을곳), "Fail Kandungan_VALUE");
        tentu_sahkan(호출.alih_jawatan(부모, 서술자, 0, panggilan_sistem.Cari_Mula) == 0, "Fail Kedudukan alih_VALUE");

        int 복제서술자 = 호출.서술자복제(부모, 서술자);
        tentu_sahkan(복제서술자 >= 0, "서술자 klon_VALUE");
        Proses_VALUE anak_VALUE = 호출.klon_Proses(부모);
        tentu_sahkan(anak_VALUE.식별자() != 부모.식별자(), "Proses_VALUE 식별자 분리");
        tentu_sahkan(anak_VALUE.부모식별자() == 부모.식별자(), "부모 Proses_VALUE 식별자");
        tentu_sahkan(호출.Tutup(anak_VALUE, 서술자) == 0 && 부모.파일서술자().teknologi_maklumat_buka(서술자), "anak_VALUE Tutup 격리");

        int 이전끝 = 호출.프로그램끝늘리기(부모, 8192);
        tentu_sahkan(이전끝 == 0x06000000, "aplikasi_f5044b9b 끝 늘리기");
        tentu_sahkan(부모.aplikasi_putus() == 0x06002000, "aplikasi_f5044b9b 끝 반영");
        tentu_sahkan(anak_VALUE.aplikasi_putus() == 0x06000000, "과정별 aplikasi_f5044b9b 끝 격리");

        anak_VALUE.Keluar_aplikasi(7);
        tentu_sahkan(호출.자식기다리기(부모, anak_VALUE.식별자(), false) == (7 << 8), "anak_VALUE Keluar_aplikasi 기다리기");
        tentu_sahkan(호출.접근가능("ujian", 1) == -13, "laksanakan_perintah keizinan_VALUE tolak_VALUE");
        tentu_sahkan(호출.ID_pengguna() == 0 && 호출.무리식별자() == 0, "사용자와 무리 식별자");
        tentu_sahkan("/".equals(호출.현재작업목록(2)) && 호출.tukar_senarai_tugas("/") == 0, "현재 작업 pemasukan_Senarai");
        tentu_sahkan(호출.teknologi_maklumat_Terminal(부모, 1), "표준 출력 단말");
        tentu_sahkan("JBrnOS".equals(호출.sistem_Butiran().sistem_nama()), "sistem_pengendalian_VALUE msinfo32_exe");
    }

    private static void 실행파일시험(kernel kernel_VALUE) {
        byte[] data = new byte[92];
        data[0] = 0x7f;
        data[1] = 'E';
        data[2] = 'L';
        data[3] = 'F';
        data[4] = 1;
        data[5] = 1;
        tulis_integer_VALUE(data, 24, 0x04001000);
        tulis_integer_VALUE(data, 32, 52);
        짧은정수쓰기(data, 46, 40);
        짧은정수쓰기(data, 48, 1);
        tulis_integer_VALUE(data, 56, 8);
        tulis_integer_VALUE(data, 60, 2);
        tulis_integer_VALUE(data, 64, 0x04002000);
        tulis_integer_VALUE(data, 72, 64);

        실행파일적재기.imej imej_VALUE = new 실행파일적재기().검사(data);
        tentu_sahkan(imej_VALUE.alamat_mula() == 0x04001000, "ELF Jalan e_mel");
        tentu_sahkan(imej_VALUE.구역들().size() == 1 && imej_VALUE.구역들().get(0).종류() == 8, "ELF 빈 data seksyen_VALUE");
        int 서술자 = kernel_VALUE.panggilan_sistem().Buka(kernel_VALUE.첫과정(), "ujian", panggilan_sistem.baca_sahaja_bendera);
        tentu_sahkan(kernel_VALUE.panggilan_sistem().kawalan_fail(kernel_VALUE.첫과정(), 서술자, 2, 1) == 0, "laksanakan_perintah 시 Tutup Tetapan");
        tentu_sahkan(kernel_VALUE.panggilan_sistem().laksanakan_perintah(kernel_VALUE.첫과정(), data, new String[] {"ujian", "값"}, new String[] {"Bahasa=Melayu"}) == 0, "ELF laksanakan_perintah imej_VALUE 적재");
        tentu_sahkan(kernel_VALUE.첫과정().실행시작주소() == 0x04001000, "laksanakan_perintah Jalan e_mel 반영");
        tentu_sahkan(kernel_VALUE.첫과정().실행인자().length == 2 && kernel_VALUE.첫과정().persekitaran_VALUE().length == 1, "laksanakan_perintah 인자와 persekitaran");
        tentu_sahkan(!kernel_VALUE.첫과정().파일서술자().teknologi_maklumat_buka(서술자), "laksanakan_perintah 시 서술자 Tutup");
        tentu_sahkan(kernel_VALUE.쪽관리().바이트읽기(kernel_VALUE.첫과정().e_mel_SPACE(), 0x04002000) == 0, "빈 data seksyen_VALUE 영 mengasal");
    }

    private static void 입력시험(kernel kernel_VALUE) {
        kernel_VALUE.입력관리().Kunci_bawah('가');
        kernel_VALUE.입력관리().쥐이동(3, -2);
        입력사건 첫사건 = kernel_VALUE.입력관리().Seterusnya_acara();
        입력사건 SECOND_acara = kernel_VALUE.입력관리().Seterusnya_acara();
        tentu_sahkan(첫사건.jenis_peristiwa() == 입력사건.종류.Kunci_bawah, "자판 Peristiwa");
        tentu_sahkan(SECOND_acara.첫째값() == 3 && SECOND_acara.SECOND_VALUE() == -2, "쥐 alih_VALUE Peristiwa");
    }

    private static void 하드웨어시험(호스트하드웨어 peranti_VALUE) {
        peranti_VALUE.tulis_port_bait(0x3f8, 0xab);
        tentu_sahkan(peranti_VALUE.포트바이트읽기(0x3f8) == 0xab, "포트 I_O 경계");
        tentu_sahkan(peranti_VALUE.직렬기록().contains("JBrnOS"), "직렬 LOG_baris");
    }

    private static void 개입중단과서술자시험() {
        IRQ_pengurus pengurus_VALUE = new IRQ_pengurus();
        pengurus_VALUE.daftar_pemasukan(0x21, Storan_e_mel -> Storan_e_mel + 4);
        pengurus_VALUE.mendayakan();
        tentu_sahkan(pengurus_VALUE.agih_VALUE(0x21, 100) == 104, "IRQ agih_VALUE");
        pengurus_VALUE.nyahaktifkan();
        tentu_sahkan(pengurus_VALUE.agih_VALUE(0x21, 100) == 100, "IRQ nyahaktifkan");

        전역서술자표 서술자표 = new 전역서술자표();
        서술자표.set_nilai_lalai();
        tentu_sahkan(서술자표.조각들().size() == 5, "전역 서술자표");
        tugas_status_segmen tugas_status = new tugas_status_segmen();
        tugas_status.특권쌓임공간설정(0x10, 0x800000);
        tentu_sahkan(tugas_status.영번쌓임조각() == 0x10 && tugas_status.영번쌓임주소() == 0x800000, "작업 status_VALUE seksyen_VALUE");
    }

    private static void ujian_Storan_AND_Rangkaian() {
        고급기술결합장치 Storan_peranti = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.seksyen_saiz];
        byte[] 읽은자료 = new byte[고급기술결합장치.seksyen_saiz];
        쓸자료[17] = 42;
        Storan_peranti.Tulis(2, 쓸자료);
        Storan_peranti.Baca(2, 읽은자료);
        tentu_sahkan(읽은자료[17] == 42, "ATA seksyen_VALUE 읽고 Tulis");

        aksesori_bas_pengurus aksesori = new aksesori_bas_pengurus();
        aksesori.발견(new aksesori_bas_pengurus.peranti_VALUE(0x1022, 0x2000, 0xc000, 11));
        tentu_sahkan(aksesori.Cari_pemasukan(0x1022, 0x2000) != null, "주변 peranti_VALUE Cari_pemasukan");

        byte[] Ethernet_bingkai = new byte[34];
        Ethernet_bingkai[12] = 0x08;
        Ethernet_bingkai[13] = 0x00;
        Ethernet_bingkai[14] = 0x45;
        tentu_sahkan(rangkaian_Alat.Ethernet_UPPER_protokol(Ethernet_bingkai) == 0x0800, "이더넷 상위 kes_VALUE");
        tentu_sahkan(rangkaian_Alat.상호통신망규약사판인가(Ethernet_bingkai, 14), "상호통신망규약 4판");
        tentu_sahkan(rangkaian_Alat.awan_hasil_tambah_semak(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 hasil_tambah_semak");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        tulis_integer_VALUE(첫구역, 454, 63);
        tulis_integer_VALUE(첫구역, 458, 1024);
        tentu_sahkan(new 기본분할영역표().Baca(첫구역).size() == 1, "nilai_lalai 분할 영역표");

        rangkaian_lapisan lapisan_VALUE = new rangkaian_lapisan();
        int[] RECEIVED_COUNT = new int[1];
        lapisan_VALUE.daftar_pengguna_data_unit(7, (data, Jalan, kepanjangan_VALUE) -> RECEIVED_COUNT[0]++);
        byte[] bingkai_INDEX = new byte[14 + 20 + 8];
        bingkai_INDEX[12] = 0x08;
        bingkai_INDEX[13] = 0x00;
        bingkai_INDEX[14] = 0x45;
        bingkai_INDEX[16] = 0;
        bingkai_INDEX[17] = 28;
        bingkai_INDEX[23] = 17;
        bingkai_INDEX[36] = 0;
        bingkai_INDEX[37] = 7;
        tentu_sahkan(lapisan_VALUE.이더넷받기(bingkai_INDEX) && RECEIVED_COUNT[0] == 1, "ruang_pengguna data unit_VALUE agih_VALUE");
    }

    private static void 화면과시계시험() {
        aksara_papar 화면 = new aksara_papar();
        화면.출력("가나\n다");
        tentu_sahkan(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 출력");
        Jam Jam = new Jam(100);
        for (int INDEX = 0; INDEX < 10; INDEX++) {
            Jam.detik_VALUE();
        }
        tentu_sahkan(Jam.지난밀리초() == 100, "Jam detik_VALUE tukar_VALUE");
    }

    private static void tulis_integer_VALUE(byte[] data, int Kedudukan, int VALUE) {
        data[Kedudukan] = (byte) VALUE;
        data[Kedudukan + 1] = (byte) (VALUE >>> 8);
        data[Kedudukan + 2] = (byte) (VALUE >>> 16);
        data[Kedudukan + 3] = (byte) (VALUE >>> 24);
    }

    private static void 짧은정수쓰기(byte[] data, int Kedudukan, int VALUE) {
        data[Kedudukan] = (byte) VALUE;
        data[Kedudukan + 1] = (byte) (VALUE >>> 8);
    }

    private static void tentu_sahkan(boolean syarat, String Nama) {
        if (!syarat) {
            throw new AssertionError("kegagalan_VALUE: " + Nama);
        }
        hantar_COUNT++;
        System.out.println("hantar_VALUE: " + Nama);
    }
}
