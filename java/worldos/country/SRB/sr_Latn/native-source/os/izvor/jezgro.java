// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** stvarni_podaci 부팅 후 호출되는 Java stavka_p. JVM과 host 운영체제에 의존하지 않는다. */
public final class jezgro {
    static int ukupan_VALUE(int 끝) {
        int SUM_VALUE = 0;
        for (int INDEX = 1; INDEX <= 끝; INDEX++) SUM_VALUE += INDEX;
        return SUM_VALUE;
    }

    static boolean 시험() {
        int[] 값들 = new int[4];
        값들[2] = ukupan_VALUE(10);
        int 음수 = -7;
        int 최소 = 0x80000000;
        int deljenje_KR = -1;
        int INDEX = Memorija_oblast.dodeliti_Skladište();
        boolean prebaciti_VALUE = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / deljenje_KR == 최소
            && 최소 % deljenje_KR == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && INDEX >= 0 && Memorija_oblast.vratiti_KR(INDEX) && !Memorija_oblast.vratiti_KR(INDEX);
        SMS_Terminal.쓰기(prebaciti_VALUE ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return prebaciti_VALUE;
    }

    public static void koristiti() {
        SMS_Terminal.Pripremi();
        SMS_Terminal.쓰기("JKOROS NATIVE JAVA\n");
        SMS_Terminal.쓰기("자바 기계어 jezgro_VALUE koristiti\n");
        if (uređaj_VALUE.부팅표식() != 0x2badb002) {
            SMS_Terminal.쓰기("BAD MULTIBOOT MAGIC\n");
            uređaj_VALUE.정지();
        }
        if (!시험()) uređaj_VALUE.정지();
        if (Memorija_oblast.UPPER_Memorija_promeniti_veličinu() < 15360) {
            SMS_Terminal.쓰기("At least 16 MiB RAM required\n");
            uređaj_VALUE.정지();
        }
        uređaj_VALUE.Pripremi_korisnik_program();
        SMS_Terminal.쓰기("USER ELF: ring 3 / paging / int 0x80\n");
        Mreža_Upravljački_program.Pripremi();
        Mreža_stek.CLEAN_Proces();
        Memorija_sistem_datoteka.Pripremi();
        파일보존.Pripremi();
        명령해석기.koristiti();
    }
}
