// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** real_datos 부팅 후 호출되는 Java introdución_p. JVM과 hospedar 운영체제에 의존하지 않는다. */
public final class kernel {
    static int 합계(int 끝) {
        int SUMA_VALOR = 0;
        for (int ÍNDICE = 1; ÍNDICE <= 끝; ÍNDICE++) SUMA_VALOR += ÍNDICE;
        return SUMA_VALOR;
    }

    static boolean 시험() {
        int[] 값들 = new int[4];
        값들[2] = 합계(10);
        int 음수 = -7;
        int 최소 = 0x80000000;
        int división_medida = -1;
        int ÍNDICE = 기억공간.atribuír_Almacenamento();
        boolean pass_VALOR = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / división_medida == 최소
            && 최소 % división_medida == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && ÍNDICE >= 0 && 기억공간.devolver_medida(ÍNDICE) && !기억공간.devolver_medida(ÍNDICE);
        SMS_Terminal.Escritura(pass_VALOR ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return pass_VALOR;
    }

    public static void Executar_2() {
        SMS_Terminal.준비();
        SMS_Terminal.Escritura("JKOROS NATIVE JAVA\n");
        SMS_Terminal.Escritura("자바 기계어 kernel_VALOR Executar_2\n");
        if (dispositivo_VALOR.부팅표식() != 0x2badb002) {
            SMS_Terminal.Escritura("BAD MULTIBOOT MAGIC\n");
            dispositivo_VALOR.정지();
        }
        if (!시험()) dispositivo_VALOR.정지();
        if (기억공간.위쪽기억크기() < 15360) {
            SMS_Terminal.Escritura("At least 16 MiB RAM required\n");
            dispositivo_VALOR.정지();
        }
        dispositivo_VALOR.사용자준비();
        SMS_Terminal.Escritura("USER ELF: ring 3 / paging / int 0x80\n");
        Rede_controlador.준비();
        Rede_Montón.Limpo_Proceso();
        Memoria_sistema_de_ficheiros.준비();
        파일보존.준비();
        명령해석기.Executar_2();
    }
}
