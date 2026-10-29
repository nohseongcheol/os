// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** tényleges_adat 부팅 후 호출되는 Java belépési_pont. JVM과 gazda 운영체제에 의존하지 않는다. */
public final class kernel {
    static int összesen_ÉRTÉK(int 끝) {
        int SUM_ÉRTÉK = 0;
        for (int INDEX = 1; INDEX <= 끝; INDEX++) SUM_ÉRTÉK += INDEX;
        return SUM_ÉRTÉK;
    }

    static boolean 시험() {
        int[] 값들 = new int[4];
        값들[2] = összesen_ÉRTÉK(10);
        int 음수 = -7;
        int 최소 = 0x80000000;
        int osztás_KR = -1;
        int INDEX = Memória_régió.kioszt_tár();
        boolean továbbít_ÉRTÉK = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / osztás_KR == 최소
            && 최소 % osztás_KR == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && INDEX >= 0 && Memória_régió.visszaküld_KR(INDEX) && !Memória_régió.visszaküld_KR(INDEX);
        SMS_Terminál.Írás(továbbít_ÉRTÉK ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return továbbít_ÉRTÉK;
    }

    public static void Futtatás() {
        SMS_Terminál.Előkészítés();
        SMS_Terminál.Írás("JKOROS NATIVE JAVA\n");
        SMS_Terminál.Írás("자바 기계어 kernel_ÉRTÉK Futtatás\n");
        if (mobil_ÉRTÉK.부팅표식() != 0x2badb002) {
            SMS_Terminál.Írás("BAD MULTIBOOT MAGIC\n");
            mobil_ÉRTÉK.정지();
        }
        if (!시험()) mobil_ÉRTÉK.정지();
        if (Memória_régió.NAGYBETŰS_Memória_méretez() < 15360) {
            SMS_Terminál.Írás("At least 16 MiB RAM required\n");
            mobil_ÉRTÉK.정지();
        }
        mobil_ÉRTÉK.Előkészítés_felhasználó_app();
        SMS_Terminál.Írás("USER ELF: ring 3 / paging / int 0x80\n");
        hálózat_eszközillesztő.Előkészítés();
        hálózat_Sor.TISZTÍT_folyamat();
        Memória_fájlrendszer.Előkészítés();
        파일보존.Előkészítés();
        명령해석기.Futtatás();
    }
}
