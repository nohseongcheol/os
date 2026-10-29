// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** real_ma_lumotlar 부팅 후 호출되는 Java kiritish_nuqta. JVM과 tashkilotchi 운영체제에 의존하지 않는다. */
public final class o_zak {
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
        int boʻlish_o_lchov = -1;
        int INDEX = 기억공간.joylashtirmoq_Xotira();
        boolean 통과 = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / boʻlish_o_lchov == 최소
            && 최소 % boʻlish_o_lchov == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && INDEX >= 0 && 기억공간.qaytarish_o_lchov(INDEX) && !기억공간.qaytarish_o_lchov(INDEX);
        SMS_Terminal.Yozish(통과 ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return 통과;
    }

    public static void Bajarish() {
        SMS_Terminal.Tayyorlamoq();
        SMS_Terminal.Yozish("JKOROS NATIVE JAVA\n");
        SMS_Terminal.Yozish("자바 기계어 o_zak_VALUE Bajarish\n");
        if (qurilma_VALUE.부팅표식() != 0x2badb002) {
            SMS_Terminal.Yozish("BAD MULTIBOOT MAGIC\n");
            qurilma_VALUE.정지();
        }
        if (!시험()) qurilma_VALUE.정지();
        if (기억공간.UPPER_Xotira_o_lcham() < 15360) {
            SMS_Terminal.Yozish("At least 16 MiB RAM required\n");
            qurilma_VALUE.정지();
        }
        qurilma_VALUE.Tayyorlamoq_foydalanuvchi_ilova();
        SMS_Terminal.Yozish("USER ELF: ring 3 / paging / int 0x80\n");
        Tarmoq_drayver.Tayyorlamoq();
        Tarmoq_Stack.Toza_Jarayon();
        Xotira_fayllar_tizimi.Tayyorlamoq();
        파일보존.Tayyorlamoq();
        명령해석기.Bajarish();
    }
}
