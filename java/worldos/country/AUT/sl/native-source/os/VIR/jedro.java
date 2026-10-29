// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** dejanski_podatki 부팅 후 호출되는 Java vnos_p. JVM과 gostiti 운영체제에 의존하지 않는다. */
public final class jedro {
    static int skupaj_VALUE(int 끝) {
        int SUM_VALUE = 0;
        for (int INDEX = 1; INDEX <= 끝; INDEX++) SUM_VALUE += INDEX;
        return SUM_VALUE;
    }

    static boolean 시험() {
        int[] 값들 = new int[4];
        값들[2] = skupaj_VALUE(10);
        int 음수 = -7;
        int 최소 = 0x80000000;
        int sektor_KR = -1;
        int INDEX = pomnilnik_območje.dodeliti_Senzor_prostora();
        boolean posredovati_VALUE = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / sektor_KR == 최소
            && 최소 % sektor_KR == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && INDEX >= 0 && pomnilnik_območje.vrni_KR(INDEX) && !pomnilnik_območje.vrni_KR(INDEX);
        SMS_Terminal.Pisanje(posredovati_VALUE ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return posredovati_VALUE;
    }

    public static void Zaženi() {
        SMS_Terminal.Pripravi();
        SMS_Terminal.Pisanje("JKOROS NATIVE JAVA\n");
        SMS_Terminal.Pisanje("자바 기계어 jedro_VALUE Zaženi\n");
        if (naprava_VALUE.부팅표식() != 0x2badb002) {
            SMS_Terminal.Pisanje("BAD MULTIBOOT MAGIC\n");
            naprava_VALUE.정지();
        }
        if (!시험()) naprava_VALUE.정지();
        if (pomnilnik_območje.UPPER_pomnilnik_spremeniti_velikost() < 15360) {
            SMS_Terminal.Pisanje("At least 16 MiB RAM required\n");
            naprava_VALUE.정지();
        }
        naprava_VALUE.Pripravi_uporabnik_aplikacija();
        SMS_Terminal.Pisanje("USER ELF: ring 3 / paging / int 0x80\n");
        mreža_gonilnik.Pripravi();
        mreža_Sklad.CLEAN_Proces();
        pomnilnik_datotečni_sistem.Pripravi();
        파일보존.Pripravi();
        명령해석기.Zaženi();
    }
}
