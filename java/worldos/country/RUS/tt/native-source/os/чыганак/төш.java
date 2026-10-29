// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** фактик_мәгълүмат 부팅 후 호출되는 Java кертү_балл. JVM과 хост 운영체제에 의존하지 않는다. */
public final class төш {
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
        int бүлү_үлчәм = -1;
        int INDEX = 기억공간.атап_бирү_Саклагыч();
        boolean үткәрү_VALUE = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / бүлү_үлчәм == 최소
            && 최소 % бүлү_үлчәм == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && INDEX >= 0 && 기억공간.кайтару_үлчәм(INDEX) && !기억공간.кайтару_үлчәм(INDEX);
        СМС_Терминал.язу(үткәрү_VALUE ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return үткәрү_VALUE;
    }

    public static void эшләтү() {
        СМС_Терминал.Әзерләү();
        СМС_Терминал.язу("JKOROS NATIVE JAVA\n");
        СМС_Терминал.язу("자바 기계어 төш_VALUE эшләтү\n");
        if (мобиль_VALUE.부팅표식() != 0x2badb002) {
            СМС_Терминал.язу("BAD MULTIBOOT MAGIC\n");
            мобиль_VALUE.정지();
        }
        if (!시험()) мобиль_VALUE.정지();
        if (기억공간.UPPER_Хәтер_үлчәмен_үзгәртү() < 15360) {
            СМС_Терминал.язу("At least 16 MiB RAM required\n");
            мобиль_VALUE.정지();
        }
        мобиль_VALUE.Әзерләү_кулланучы_кушымта();
        СМС_Терминал.язу("USER ELF: ring 3 / paging / int 0x80\n");
        Челтәр_драйвер.Әзерләү();
        Челтәр_Стәк.CLEAN_Процесс();
        Хәтер_файл_системасы.Әзерләү();
        파일보존.Әзерләү();
        명령해석기.эшләтү();
    }
}
