// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Català.propi;
/** 작업 fil_VALOR: 하나의 Executa_ordre flux_VALOR. propi JVM 안에서 Ordre 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 Executa_2(실행할일 tasca_acció) { 작업가닥 fil_VALOR = new 작업가닥(tasca_acció); fil_VALOR.Inici_tasca(); return fil_VALOR; }
    public static void 기다리기(작업가닥 fil_VALOR) throws 대기중단예외 { fil_VALOR.기다리기(); }
    public static boolean 살아있는가(작업가닥 fil_VALOR) { return fil_VALOR.살아있는가(); }
    public static void RENDTO_tasca() { 작업가닥.RENDTO_tasca(); }
}
