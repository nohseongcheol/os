// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package magyar.saját;
/** 작업 szál_ÉRTÉK: 하나의 végrehajt_parancs Stream_ÉRTÉK. saját JVM 안에서 Parancs 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static dolgozó Futtatás(실행할일 teendő_Action) { dolgozó szál_ÉRTÉK = new dolgozó(teendő_Action); szál_ÉRTÉK.START_teendő(); return szál_ÉRTÉK; }
    public static void 기다리기(dolgozó szál_ÉRTÉK) throws 대기중단예외 { szál_ÉRTÉK.기다리기(); }
    public static boolean 살아있는가(dolgozó szál_ÉRTÉK) { return szál_ÉRTÉK.살아있는가(); }
    public static void HOZAM_teendő() { dolgozó.HOZAM_teendő(); }
}
