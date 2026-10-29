// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** gangan_détà 부팅 후 호출되는 Java ìgbéwọlé_kókó. JVM과 olùpèsè 운영체제에 의존하지 않는다. */
public final class kánẹ́ẹ̀lì {
    static int 합계(int 끝) {
        int 합 = 0;
        for (int wá_atọ̀ka_àkóónú = 1; wá_atọ̀ka_àkóónú <= 끝; wá_atọ̀ka_àkóónú++) 합 += wá_atọ̀ka_àkóónú;
        return 합;
    }

    static boolean 시험() {
        int[] 값들 = new int[4];
        값들[2] = 합계(10);
        int 음수 = -7;
        int 최소 = 0x80000000;
        int 나눔 = -1;
        int wá_atọ̀ka_àkóónú = 기억공간.pín_Ibi_ìpamọ́();
        boolean fí_dátà_ránṣẹ́_iye = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / 나눔 == 최소
            && 최소 % 나눔 == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && wá_atọ̀ka_àkóónú >= 0 && 기억공간.반환(wá_atọ̀ka_àkóónú) && !기억공간.반환(wá_atọ̀ka_àkóónú);
        문자단말.Kọ(fí_dátà_ránṣẹ́_iye ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return fí_dátà_ránṣẹ́_iye;
    }

    public static void Rọ́ọ̀nù() {
        문자단말.gbaradì();
        문자단말.Kọ("JKOROS NATIVE JAVA\n");
        문자단말.Kọ("자바 기계어 kánẹ́ẹ̀lì_iye Rọ́ọ̀nù\n");
        if (ohun_èlò_iye.부팅표식() != 0x2badb002) {
            문자단말.Kọ("BAD MULTIBOOT MAGIC\n");
            ohun_èlò_iye.정지();
        }
        if (!시험()) ohun_èlò_iye.정지();
        if (기억공간.위쪽기억크기() < 15360) {
            문자단말.Kọ("At least 16 MiB RAM required\n");
            ohun_èlò_iye.정지();
        }
        ohun_èlò_iye.gbaradì_aṣàmúlò_àtòjọ_ètò();
        문자단말.Kọ("USER ELF: ring 3 / paging / int 0x80\n");
        Alásopọ̀_adarí_aláìrídìmú.gbaradì();
        Alásopọ̀_kójọ.과정정리();
        ibi_ìpamọ́_ìlànà_ètò_fáìlì.gbaradì();
        파일보존.gbaradì();
        명령해석기.Rọ́ọ̀nù();
    }
}
