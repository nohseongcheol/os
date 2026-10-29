// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Belanda.JNldOS.pengujian;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Belanda.JNldOS.Memori_wilayah.Memori_Manajer;
import Belanda.JNldOS.Memori_wilayah.halaman_Manajer;
import Belanda.JNldOS.입력.입력사건;
import Belanda.JNldOS.작업.Proses_VALUE;
import Belanda.JNldOS.panggilan_sistem.panggilan_sistem;
import Belanda.JNldOS.sistem_berkas.실행파일적재기;
import Belanda.JNldOS.Inti.Inti;
import Belanda.JNldOS.host.호스트하드웨어;
import Belanda.JNldOS.IRQ.IRQ_Manajer;
import Belanda.JNldOS.서술자.전역서술자표;
import Belanda.JNldOS.Storage_Ponsel.고급기술결합장치;
import Belanda.JNldOS.Ponsel_VALUE.aksesori_bus_Manajer;
import Belanda.JNldOS.jaringan_tumpuk.jaringan_Alat;
import Belanda.JNldOS.jaringan_tumpuk.lapisan_jaringan;
import Belanda.JNldOS.Ponsel_VALUE.Jam;
import Belanda.JNldOS.서술자.tugas_Status_segmen;
import Belanda.JNldOS.화면.karakter_tampilan;
import Belanda.JNldOS.sistem_berkas.기본분할영역표;

public final class 전체시험 {
    private static int teruskan_COUNT;

    private 전체시험() {
    }

    public static void main(String[] parameter_argumen) {
        호스트하드웨어 Ponsel_VALUE = new 호스트하드웨어();
        Inti kernel_VALUE = new Inti(Ponsel_VALUE);
        kernel_VALUE.jalankan();

        기억공간시험(kernel_VALUE);
        쪽관리시험(kernel_VALUE);
        파일과과정시험(kernel_VALUE);
        실행파일시험(kernel_VALUE);
        입력시험(kernel_VALUE);
        하드웨어시험(Ponsel_VALUE);
        개입중단과서술자시험();
        저장장치와통신망시험();
        화면과시계시험();

        System.out.println("JNldOS pengujian teruskan_VALUE: " + teruskan_COUNT);
    }

    private static void 기억공간시험(Inti kernel_VALUE) {
        Memori_Manajer Manajer_VALUE = kernel_VALUE.Memori_wilayah();
        int 첫주소 = Manajer_VALUE.정렬할당(100, 64);
        periksa((첫주소 & 63) == 0, "ratakan_VALUE alokasi_Storage");
        Manajer_VALUE.tulis_byte_VALUE(첫주소, (byte) 0x5a);
        periksa(Manajer_VALUE.바이트읽기(첫주소) == (byte) 0x5a, "물리 Memori_wilayah 읽고 Tulis");
        int 사용전 = Manajer_VALUE.사용크기();
        Manajer_VALUE.lepas_Storage(첫주소);
        periksa(Manajer_VALUE.사용크기() < 사용전, "Memori_wilayah lepas_Storage");
    }

    private static void 쪽관리시험(Inti kernel_VALUE) {
        halaman_Manajer Manajer_VALUE = kernel_VALUE.쪽관리();
        halaman_Manajer.surel_SPACE induk_SPACE = Manajer_VALUE.새주소공간();
        Manajer_VALUE.MAP_halaman(induk_SPACE, 0x1000, true);
        Manajer_VALUE.tulis_byte_VALUE(induk_SPACE, 0x1010, (byte) 7);
        halaman_Manajer.surel_SPACE turunan_SPACE = Manajer_VALUE.쓰기시복사복제(induk_SPACE);
        Manajer_VALUE.tulis_byte_VALUE(turunan_SPACE, 0x1010, (byte) 9);
        periksa(Manajer_VALUE.바이트읽기(induk_SPACE, 0x1010) == 7, "Tulis 시 salin_VALUE induk_VALUE 격리");
        periksa(Manajer_VALUE.바이트읽기(turunan_SPACE, 0x1010) == 9, "Tulis 시 salin_VALUE turunan_VALUE Tulis");
    }

    private static void 파일과과정시험(Inti kernel_VALUE) {
        byte[] Isi_VALUE = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        kernel_VALUE.sistem_berkas().tambah_file("pengujian", Isi_VALUE);
        Proses_VALUE induk_VALUE = kernel_VALUE.첫과정();
        panggilan_sistem 호출 = kernel_VALUE.panggilan_sistem();
        int 서술자 = 호출.Buka(induk_VALUE, "/pengujian", panggilan_sistem.baca_saja_bendera);
        periksa(서술자 >= 3, "berkas Buka");

        byte[] terima_tujuan = new byte[Isi_VALUE.length];
        periksa(호출.Baca(induk_VALUE, 서술자, terima_tujuan, terima_tujuan.length) == Isi_VALUE.length, "berkas Baca");
        periksa(Arrays.equals(Isi_VALUE, terima_tujuan), "berkas Isi_VALUE");
        periksa(호출.gerak_posisi(induk_VALUE, 서술자, 0, panggilan_sistem.Cari_Mulai) == 0, "berkas posisi gerak_VALUE");

        int 복제서술자 = 호출.서술자복제(induk_VALUE, 서술자);
        periksa(복제서술자 >= 0, "서술자 klon_VALUE");
        Proses_VALUE turunan_VALUE = 호출.klon_Proses(induk_VALUE);
        periksa(turunan_VALUE.pengidentifikasi_VALUE() != induk_VALUE.pengidentifikasi_VALUE(), "Proses_VALUE pengidentifikasi_VALUE 분리");
        periksa(turunan_VALUE.induk_pengidentifikasi() == induk_VALUE.pengidentifikasi_VALUE(), "induk_VALUE Proses_VALUE pengidentifikasi_VALUE");
        periksa(호출.Tutup(turunan_VALUE, 서술자) == 0 && induk_VALUE.파일서술자().teknologi_informasi_buat(서술자), "turunan_VALUE Tutup 격리");

        int 이전끝 = 호출.프로그램끝늘리기(induk_VALUE, 8192);
        periksa(이전끝 == 0x06000000, "apl_f5044b9b 끝 늘리기");
        periksa(induk_VALUE.apl_putus() == 0x06002000, "apl_f5044b9b 끝 반영");
        periksa(turunan_VALUE.apl_putus() == 0x06000000, "과정별 apl_f5044b9b 끝 격리");

        turunan_VALUE.Keluar_apl(7);
        periksa(호출.자식기다리기(induk_VALUE, turunan_VALUE.pengidentifikasi_VALUE(), false) == (7 << 8), "turunan_VALUE Keluar_apl 기다리기");
        periksa(호출.접근가능("pengujian", 1) == -13, "Jalankan_perintah izin_VALUE tolak_VALUE");
        periksa(호출.ID_pengguna() == 0 && 호출.grup_pengidentifikasi() == 0, "사용자와 무리 pengidentifikasi_VALUE");
        periksa("/".equals(호출.saat_ini_daftar_tugas(2)) && 호출.SWITCH_daftar_tugas("/") == 0, "saat_ini_item 작업 entri_Daftar");
        periksa(호출.teknologi_informasi_Terminal(induk_VALUE, 1), "표준 keluaranTeks 단말");
        periksa("JNldOS".equals(호출.sistem_Detail().sistem_nama()), "sistem_operasi_VALUE msinfo32_exe");
    }

    private static void 실행파일시험(Inti kernel_VALUE) {
        byte[] data = new byte[92];
        data[0] = 0x7f;
        data[1] = 'E';
        data[2] = 'L';
        data[3] = 'F';
        data[4] = 1;
        data[5] = 1;
        tulis_bilangan_bulat_VALUE(data, 24, 0x04001000);
        tulis_bilangan_bulat_VALUE(data, 32, 52);
        짧은정수쓰기(data, 46, 40);
        짧은정수쓰기(data, 48, 1);
        tulis_bilangan_bulat_VALUE(data, 56, 8);
        tulis_bilangan_bulat_VALUE(data, 60, 2);
        tulis_bilangan_bulat_VALUE(data, 64, 0x04002000);
        tulis_bilangan_bulat_VALUE(data, 72, 64);

        실행파일적재기.foto foto_VALUE = new 실행파일적재기().검사(data);
        periksa(foto_VALUE.alamat_permulaan() == 0x04001000, "ELF jalankan surel");
        periksa(foto_VALUE.구역들().size() == 1 && foto_VALUE.구역들().get(0).종류() == 8, "ELF 빈 data seksi_VALUE");
        int 서술자 = kernel_VALUE.panggilan_sistem().Buka(kernel_VALUE.첫과정(), "pengujian", panggilan_sistem.baca_saja_bendera);
        periksa(kernel_VALUE.panggilan_sistem().kendali_berkas(kernel_VALUE.첫과정(), 서술자, 2, 1) == 0, "Jalankan_perintah 시 Tutup Konfigurasi");
        periksa(kernel_VALUE.panggilan_sistem().Jalankan_perintah(kernel_VALUE.첫과정(), data, new String[] {"pengujian", "값"}, new String[] {"Bahasa=Indonesia"}) == 0, "ELF Jalankan_perintah foto_VALUE 적재");
        periksa(kernel_VALUE.첫과정().실행시작주소() == 0x04001000, "Jalankan_perintah jalankan surel 반영");
        periksa(kernel_VALUE.첫과정().실행인자().length == 2 && kernel_VALUE.첫과정().lingkungan_VALUE().length == 1, "Jalankan_perintah 인자와 lingkungan");
        periksa(!kernel_VALUE.첫과정().파일서술자().teknologi_informasi_buat(서술자), "Jalankan_perintah 시 서술자 Tutup");
        periksa(kernel_VALUE.쪽관리().바이트읽기(kernel_VALUE.첫과정().surel_SPACE(), 0x04002000) == 0, "빈 data seksi_VALUE 영 inisialisasi");
    }

    private static void 입력시험(Inti kernel_VALUE) {
        kernel_VALUE.입력관리().Kunci_tidak_berfungsi('가');
        kernel_VALUE.입력관리().쥐이동(3, -2);
        입력사건 첫사건 = kernel_VALUE.입력관리().Berikutnya_acara();
        입력사건 SECOND_acara = kernel_VALUE.입력관리().Berikutnya_acara();
        periksa(첫사건.jenis_kejadian() == 입력사건.종류.Kunci_tidak_berfungsi, "자판 Even");
        periksa(SECOND_acara.첫째값() == 3 && SECOND_acara.SECOND_VALUE() == -2, "쥐 gerak_VALUE Even");
    }

    private static void 하드웨어시험(호스트하드웨어 Ponsel_VALUE) {
        Ponsel_VALUE.tulis_port_byte(0x3f8, 0xab);
        periksa(Ponsel_VALUE.포트바이트읽기(0x3f8) == 0xab, "포트 I_O 경계");
        periksa(Ponsel_VALUE.직렬기록().contains("JNldOS"), "직렬 LOG_baris");
    }

    private static void 개입중단과서술자시험() {
        IRQ_Manajer Manajer_VALUE = new IRQ_Manajer();
        Manajer_VALUE.daftar_entri(0x21, Storage_surel -> Storage_surel + 4);
        Manajer_VALUE.aktifkan();
        periksa(Manajer_VALUE.distribusi_VALUE(0x21, 100) == 104, "IRQ distribusi_VALUE");
        Manajer_VALUE.nonaktifkan();
        periksa(Manajer_VALUE.distribusi_VALUE(0x21, 100) == 100, "IRQ nonaktifkan");

        전역서술자표 서술자표 = new 전역서술자표();
        서술자표.set_nilai_default();
        periksa(서술자표.조각들().size() == 5, "전역 서술자표");
        tugas_Status_segmen tugas_Status = new tugas_Status_segmen();
        tugas_Status.특권쌓임공간설정(0x10, 0x800000);
        periksa(tugas_Status.영번쌓임조각() == 0x10 && tugas_Status.영번쌓임주소() == 0x800000, "작업 Status_VALUE seksi_VALUE");
    }

    private static void 저장장치와통신망시험() {
        고급기술결합장치 Storage_Ponsel = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.seksi_ukuran];
        byte[] 읽은자료 = new byte[고급기술결합장치.seksi_ukuran];
        쓸자료[17] = 42;
        Storage_Ponsel.Tulis(2, 쓸자료);
        Storage_Ponsel.Baca(2, 읽은자료);
        periksa(읽은자료[17] == 42, "ATA seksi_VALUE 읽고 Tulis");

        aksesori_bus_Manajer aksesori = new aksesori_bus_Manajer();
        aksesori.발견(new aksesori_bus_Manajer.Ponsel_VALUE(0x1022, 0x2000, 0xc000, 11));
        periksa(aksesori.FIND_entri(0x1022, 0x2000) != null, "주변 Ponsel_VALUE FIND_entri");

        byte[] Ethernet_bingkai = new byte[34];
        Ethernet_bingkai[12] = 0x08;
        Ethernet_bingkai[13] = 0x00;
        Ethernet_bingkai[14] = 0x45;
        periksa(jaringan_Alat.Ethernet_UPPER_protokol(Ethernet_bingkai) == 0x0800, "이더넷 상위 kasus_VALUE");
        periksa(jaringan_Alat.teknologi_informasi_IPV_4_protokol(Ethernet_bingkai, 14), "상호통신망규약 4판");
        periksa(jaringan_Alat.cloud_checksum(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 checksum");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        tulis_bilangan_bulat_VALUE(첫구역, 454, 63);
        tulis_bilangan_bulat_VALUE(첫구역, 458, 1024);
        periksa(new 기본분할영역표().Baca(첫구역).size() == 1, "nilai_default 분할 영역표");

        lapisan_jaringan lapisan_VALUE = new lapisan_jaringan();
        int[] RECEIVED_COUNT = new int[1];
        lapisan_VALUE.daftar_pengguna_data_unit(7, (data, jalankan, panjang_VALUE) -> RECEIVED_COUNT[0]++);
        byte[] bingkai_INDEX = new byte[14 + 20 + 8];
        bingkai_INDEX[12] = 0x08;
        bingkai_INDEX[13] = 0x00;
        bingkai_INDEX[14] = 0x45;
        bingkai_INDEX[16] = 0;
        bingkai_INDEX[17] = 28;
        bingkai_INDEX[23] = 17;
        bingkai_INDEX[36] = 0;
        bingkai_INDEX[37] = 7;
        periksa(lapisan_VALUE.terima_Ethernet(bingkai_INDEX) && RECEIVED_COUNT[0] == 1, "ruang_pengguna data unit_VALUE distribusi_VALUE");
    }

    private static void 화면과시계시험() {
        karakter_tampilan 화면 = new karakter_tampilan();
        화면.keluaranTeks("가나\n다");
        periksa(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 keluaranTeks");
        Jam Jam = new Jam(100);
        for (int INDEX = 0; INDEX < 10; INDEX++) {
            Jam.틱();
        }
        periksa(Jam.지난밀리초() == 100, "Jam 틱 CONVERT_VALUE");
    }

    private static void tulis_bilangan_bulat_VALUE(byte[] data, int posisi, int VALUE) {
        data[posisi] = (byte) VALUE;
        data[posisi + 1] = (byte) (VALUE >>> 8);
        data[posisi + 2] = (byte) (VALUE >>> 16);
        data[posisi + 3] = (byte) (VALUE >>> 24);
    }

    private static void 짧은정수쓰기(byte[] data, int posisi, int VALUE) {
        data[posisi] = (byte) VALUE;
        data[posisi + 1] = (byte) (VALUE >>> 8);
    }

    private static void periksa(boolean kondisi, String Nama_2) {
        if (!kondisi) {
            throw new AssertionError("kegagalan_VALUE: " + Nama_2);
        }
        teruskan_COUNT++;
        System.out.println("teruskan_VALUE: " + Nama_2);
    }
}
