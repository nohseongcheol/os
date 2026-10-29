// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** real_dades 부팅 후 호출되는 Java introducció_p. JVM과 allotjar 운영체제에 의존하지 않는다. */
public final class nucli {
    static int total_VALOR(int 끝) {
        int SUMA_VALOR = 0;
        for (int INDEX = 1; INDEX <= 끝; INDEX++) SUMA_VALOR += INDEX;
        return SUMA_VALOR;
    }

    static boolean 시험() {
        int[] 값들 = new int[4];
        값들[2] = total_VALOR(10);
        int 음수 = -7;
        int 최소 = 0x80000000;
        int divisió_mesura = -1;
        int INDEX = 기억공간.assignar_Emmagatzematge();
        boolean transmetre_VALOR = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / divisió_mesura == 최소
            && 최소 % divisió_mesura == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && INDEX >= 0 && 기억공간.tornar_les_tasques_mesura(INDEX) && !기억공간.tornar_les_tasques_mesura(INDEX);
        SMS_Terminal.Escriptura(transmetre_VALOR ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return transmetre_VALOR;
    }

    public static void Executa_2() {
        SMS_Terminal.Prepara();
        SMS_Terminal.Escriptura("JKOROS NATIVE JAVA\n");
        SMS_Terminal.Escriptura("자바 기계어 nucli_VALOR Executa_2\n");
        if (dispositiu_VALOR.부팅표식() != 0x2badb002) {
            SMS_Terminal.Escriptura("BAD MULTIBOOT MAGIC\n");
            dispositiu_VALOR.정지();
        }
        if (!시험()) dispositiu_VALOR.정지();
        if (기억공간.MAJUSC_Memòria_canviar_la_mida() < 15360) {
            SMS_Terminal.Escriptura("At least 16 MiB RAM required\n");
            dispositiu_VALOR.정지();
        }
        dispositiu_VALOR.Prepara_usuari_programa();
        SMS_Terminal.Escriptura("USER ELF: ring 3 / paging / int 0x80\n");
        xarxa_controlador.Prepara();
        xarxa_Pila.NETEJA_Procés();
        Memòria_sistema_d_arxius.Prepara();
        파일보존.Prepara();
        명령해석기.Executa_2();
    }
}
