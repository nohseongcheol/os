// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** skutočný_údaje 부팅 후 호출되는 Java položka_bod. JVM과 hostiteľ 운영체제에 의존하지 않는다. */
public final class jadro {
    static int celkovo_VALUE(int 끝) {
        int SUM_VALUE = 0;
        for (int INDEX = 1; INDEX <= 끝; INDEX++) SUM_VALUE += INDEX;
        return SUM_VALUE;
    }

    static boolean 시험() {
        int[] 값들 = new int[4];
        값들[2] = celkovo_VALUE(10);
        int 음수 = -7;
        int 최소 = 0x80000000;
        int delenie_KR = -1;
        int INDEX = Pamäť_oblasť.vyhradiť_Úložisko();
        boolean odovzdať_VALUE = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / delenie_KR == 최소
            && 최소 % delenie_KR == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && INDEX >= 0 && Pamäť_oblasť.vrátiť_KR(INDEX) && !Pamäť_oblasť.vrátiť_KR(INDEX);
        SMS_Terminál.Zápis(odovzdať_VALUE ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return odovzdať_VALUE;
    }

    public static void Spustiť_2() {
        SMS_Terminál.Pripraviť();
        SMS_Terminál.Zápis("JKOROS NATIVE JAVA\n");
        SMS_Terminál.Zápis("자바 기계어 jadro_VALUE Spustiť_2\n");
        if (telefón_VALUE.부팅표식() != 0x2badb002) {
            SMS_Terminál.Zápis("BAD MULTIBOOT MAGIC\n");
            telefón_VALUE.정지();
        }
        if (!시험()) telefón_VALUE.정지();
        if (Pamäť_oblasť.UPPER_Pamäť_zmeniť_veľkosť() < 15360) {
            SMS_Terminál.Zápis("At least 16 MiB RAM required\n");
            telefón_VALUE.정지();
        }
        telefón_VALUE.Pripraviť_používateľ_program();
        SMS_Terminál.Zápis("USER ELF: ring 3 / paging / int 0x80\n");
        sieť_ovládač.Pripraviť();
        sieť_Vrstvy.CLEAN_Proces();
        Pamäť_systém_súborov.Pripraviť();
        파일보존.Pripraviť();
        명령해석기.Spustiť_2();
    }
}
