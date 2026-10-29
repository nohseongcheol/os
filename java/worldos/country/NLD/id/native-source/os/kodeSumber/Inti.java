// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** aktual_data awal_mesin 후 호출되는 Java entri_p. JVM과 host 운영체제에 의존하지 않는다. */
public final class Inti {
    static int total_VALUE(int 끝) {
        int SUM_VALUE = 0;
        for (int INDEX = 1; INDEX <= 끝; INDEX++) SUM_VALUE += INDEX;
        return SUM_VALUE;
    }

    static boolean pengujian() {
        int[] 값들 = new int[4];
        값들[2] = total_VALUE(10);
        int 음수 = -7;
        int 최소 = 0x80000000;
        int Divisi_KR = -1;
        int INDEX = Memori_wilayah.alokasi_Storage();
        boolean teruskan_VALUE = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / Divisi_KR == 최소
            && 최소 % Divisi_KR == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && INDEX >= 0 && Memori_wilayah.kembalikan_KR(INDEX) && !Memori_wilayah.kembalikan_KR(INDEX);
        SMS_Terminal.Tulis(teruskan_VALUE ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return teruskan_VALUE;
    }

    public static void jalankan() {
        SMS_Terminal.Siapkan();
        SMS_Terminal.Tulis("JKOROS NATIVE JAVA\n");
        SMS_Terminal.Tulis("자바 기계어 kernel_VALUE jalankan\n");
        if (Ponsel_VALUE.부팅표식() != 0x2badb002) {
            SMS_Terminal.Tulis("BAD MULTIBOOT MAGIC\n");
            Ponsel_VALUE.정지();
        }
        if (!pengujian()) Ponsel_VALUE.정지();
        if (Memori_wilayah.UPPER_Memori_ukuran() < 15360) {
            SMS_Terminal.Tulis("At least 16 MiB RAM required\n");
            Ponsel_VALUE.정지();
        }
        Ponsel_VALUE.Siapkan_pengguna_apl();
        SMS_Terminal.Tulis("USER ELF: ring 3 / paging / int 0x80\n");
        jaringan_driver.Siapkan();
        jaringan_tumpuk.CLEAN_Proses();
        Memori_sistem_berkas.Siapkan();
        파일보존.Siapkan();
        PenafsirPerintah.jalankan();
    }
}
