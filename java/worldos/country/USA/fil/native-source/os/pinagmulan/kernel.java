// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** totoo_data 부팅 후 호출되는 Java pagpasok_point. JVM과 host 운영체제에 의존하지 않는다. */
public final class kernel {
    static int 합계(int 끝) {
        int SUM_VALUE = 0;
        for (int INDEX = 1; INDEX <= 끝; INDEX++) SUM_VALUE += INDEX;
        return SUM_VALUE;
    }

    static boolean 시험() {
        int[] 값들 = new int[4];
        값들[2] = 합계(10);
        int 음수 = -7;
        int 최소 = 0x80000000;
        int division_sukat = -1;
        int INDEX = 기억공간.maglaan_Storage();
        boolean ipasa_VALUE = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / division_sukat == 최소
            && 최소 % division_sukat == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && INDEX >= 0 && 기억공간.반환(INDEX) && !기억공간.반환(INDEX);
        SMS_Terminal.sumulat(ipasa_VALUE ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return ipasa_VALUE;
    }

    public static void run() {
        SMS_Terminal.Ihanda();
        SMS_Terminal.sumulat("JKOROS NATIVE JAVA\n");
        SMS_Terminal.sumulat("자바 기계어 kernel_VALUE run\n");
        if (device_VALUE.부팅표식() != 0x2badb002) {
            SMS_Terminal.sumulat("BAD MULTIBOOT MAGIC\n");
            device_VALUE.정지();
        }
        if (!시험()) device_VALUE.정지();
        if (기억공간.UPPER_Memory_sukat() < 15360) {
            SMS_Terminal.sumulat("At least 16 MiB RAM required\n");
            device_VALUE.정지();
        }
        device_VALUE.Ihanda_gumagamit_app();
        SMS_Terminal.sumulat("USER ELF: ring 3 / paging / int 0x80\n");
        Network_driver.Ihanda();
        Network_Stack.CLEAN_Proseso();
        Memory_sistema_ng_file.Ihanda();
        파일보존.Ihanda();
        명령해석기.run();
    }
}
