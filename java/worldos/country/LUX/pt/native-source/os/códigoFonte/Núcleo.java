// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** real_dados arranque_da_máquina 후 호출되는 Java ponto_de_entrada. JVM과 host 운영체제에 의존하지 않는다. */
public final class Núcleo {
    static int total_VALOR(int 끝) {
        int SUM_VALOR = 0;
        for (int ÍNDICE = 1; ÍNDICE <= 끝; ÍNDICE++) SUM_VALOR += ÍNDICE;
        return SUM_VALOR;
    }

    static boolean testes() {
        int[] 값들 = new int[4];
        값들[2] = total_VALOR(10);
        int negativo_VALOR = -7;
        int 최소 = 0x80000000;
        int Divisão_RC = -1;
        int ÍNDICE = Memória_região.alocar_Armazenamento();
        boolean 통과 = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && negativo_VALOR / 3 == -2 && negativo_VALOR % 3 == -1 && 최소 / Divisão_RC == 최소
            && 최소 % Divisão_RC == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && ÍNDICE >= 0 && Memória_região.devolver_RC(ÍNDICE) && !Memória_região.devolver_RC(ÍNDICE);
        SMS_Terminal.Escrita(통과 ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return 통과;
    }

    public static void iniciar() {
        SMS_Terminal.Preparar();
        SMS_Terminal.Escrita("JKOROS NATIVE JAVA\n");
        SMS_Terminal.Escrita("자바 기계어 kernel_VALOR iniciar\n");
        if (celular_VALOR.부팅표식() != 0x2badb002) {
            SMS_Terminal.Escrita("BAD MULTIBOOT MAGIC\n");
            celular_VALOR.정지();
        }
        if (!testes()) celular_VALOR.정지();
        if (Memória_região.MAIÚSCULA_Memória_dimensionar() < 15360) {
            SMS_Terminal.Escrita("At least 16 MiB RAM required\n");
            celular_VALOR.정지();
        }
        celular_VALOR.Preparar_usuário_app();
        SMS_Terminal.Escrita("USER ELF: ring 3 / paging / int 0x80\n");
        rede_driver.Preparar();
        rede_pilha.TIRAR_Processo();
        Memória_sistema_de_arquivos.Preparar();
        파일보존.Preparar();
        InterpretadorComandos.iniciar();
    }
}
