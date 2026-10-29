// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** effettivo_dati avvio_macchina 후 호출되는 Java punto_di_ingresso. JVM과 host 운영체제에 의존하지 않는다. */
public final class Nucleo {
    static int totale_VALORE(int 끝) {
        int SUM_VALORE = 0;
        for (int INDICE = 1; INDICE <= 끝; INDICE++) SUM_VALORE += INDICE;
        return SUM_VALORE;
    }

    static boolean prove() {
        int[] 값들 = new int[4];
        값들[2] = totale_VALORE(10);
        int negativo_VALORE = -7;
        int 최소 = 0x80000000;
        int Divisione_KR = -1;
        int INDICE = Memoria_area.allocare_Memoria();
        boolean passare_VALORE = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && negativo_VALORE / 3 == -2 && negativo_VALORE % 3 == -1 && 최소 / Divisione_KR == 최소
            && 최소 % Divisione_KR == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && INDICE >= 0 && Memoria_area.Reso_KR(INDICE) && !Memoria_area.Reso_KR(INDICE);
        SMS_Terminale.Scrittura(passare_VALORE ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return passare_VALORE;
    }

    public static void avvia() {
        SMS_Terminale.Prepara();
        SMS_Terminale.Scrittura("JKOROS NATIVE JAVA\n");
        SMS_Terminale.Scrittura("자바 기계어 kernel_VALORE avvia\n");
        if (cellulare_VALORE.부팅표식() != 0x2badb002) {
            SMS_Terminale.Scrittura("BAD MULTIBOOT MAGIC\n");
            cellulare_VALORE.정지();
        }
        if (!prove()) cellulare_VALORE.정지();
        if (Memoria_area.MAIUSC_Memoria_ridimensionare() < 15360) {
            SMS_Terminale.Scrittura("At least 16 MiB RAM required\n");
            cellulare_VALORE.정지();
        }
        cellulare_VALORE.Prepara_USER_app();
        SMS_Terminale.Scrittura("USER ELF: ring 3 / paging / int 0x80\n");
        rete_driver.Prepara();
        rete_Pila.LIBERA_Processi();
        Memoria_file_system.Prepara();
        파일보존.Prepara();
        InterpreteComandi.avvia();
    }
}
