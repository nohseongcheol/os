// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** sebenar_data permulaan_mesin 후 호출되는 Java titik_permulaan. JVM과 hos 운영체제에 의존하지 않는다. */
public final class kernel {
    static int 합계(int 끝) {
        int SUM_VALUE = 0;
        for (int INDEX = 1; INDEX <= 끝; INDEX++) SUM_VALUE += INDEX;
        return SUM_VALUE;
    }

    static boolean ujian() {
        int[] 값들 = new int[4];
        값들[2] = 합계(10);
        int 음수 = -7;
        int 최소 = 0x80000000;
        int divisyen_ukuran = -1;
        int INDEX = Memori_rantau.peruntuk_Storan();
        boolean hantar_VALUE = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / divisyen_ukuran == 최소
            && 최소 % divisyen_ukuran == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && INDEX >= 0 && Memori_rantau.kembalikan_ukuran(INDEX) && !Memori_rantau.kembalikan_ukuran(INDEX);
        SMS_Terminal.Tulis(hantar_VALUE ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return hantar_VALUE;
    }

    public static void Jalan() {
        SMS_Terminal.Sediakan();
        SMS_Terminal.Tulis("JKOROS NATIVE JAVA\n");
        SMS_Terminal.Tulis("자바 기계어 kernel_VALUE Jalan\n");
        if (peranti_VALUE.부팅표식() != 0x2badb002) {
            SMS_Terminal.Tulis("BAD MULTIBOOT MAGIC\n");
            peranti_VALUE.정지();
        }
        if (!ujian()) peranti_VALUE.정지();
        if (Memori_rantau.UPPER_Memori_saiz() < 15360) {
            SMS_Terminal.Tulis("At least 16 MiB RAM required\n");
            peranti_VALUE.정지();
        }
        peranti_VALUE.Sediakan_pengguna_aplikasi();
        SMS_Terminal.Tulis("USER ELF: ring 3 / paging / int 0x80\n");
        rangkaian_pemacu.Sediakan();
        rangkaian_tindan.CLEAN_Proses();
        Memori_sistem_fail.Sediakan();
        파일보존.Sediakan();
        pentafsir_perintah.Jalan();
    }
}
