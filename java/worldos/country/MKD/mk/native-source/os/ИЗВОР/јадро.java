// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** реален_податоци 부팅 후 호출되는 Java внес_поен. JVM과 вдоми 운영체제에 의존하지 않는다. */
public final class јадро {
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
        int делење_мерка = -1;
        int INDEX = 기억공간.додели_Склад();
        boolean предава_VALUE = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / делење_мерка == 최소
            && 최소 % делење_мерка == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && INDEX >= 0 && 기억공간.반환(INDEX) && !기억공간.반환(INDEX);
        СМС_Терминал.Запиши(предава_VALUE ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return предава_VALUE;
    }

    public static void Изврши_2() {
        СМС_Терминал.Подготви();
        СМС_Терминал.Запиши("JKOROS NATIVE JAVA\n");
        СМС_Терминал.Запиши("자바 기계어 јадро_VALUE Изврши_2\n");
        if (уред_VALUE.부팅표식() != 0x2badb002) {
            СМС_Терминал.Запиши("BAD MULTIBOOT MAGIC\n");
            уред_VALUE.정지();
        }
        if (!시험()) уред_VALUE.정지();
        if (기억공간.UPPER_Меморија_големина() < 15360) {
            СМС_Терминал.Запиши("At least 16 MiB RAM required\n");
            уред_VALUE.정지();
        }
        уред_VALUE.Подготви_корисник_програма();
        СМС_Терминал.Запиши("USER ELF: ring 3 / paging / int 0x80\n");
        Мрежа_двигател.Подготви();
        Мрежа_Купче.CLEAN_Процес();
        Меморија_систем_на_датотеки.Подготви();
        파일보존.Подготви();
        명령해석기.Изврши_2();
    }
}
