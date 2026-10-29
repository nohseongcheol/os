// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package isiXhosa.자체;
/** 작업 ithredi_ixabiso: 하나의 ukwenza_umyalelo Stream_ixabiso. 자체 JVM 안에서 Umyalelo 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 Phumeza(실행할일 umsebenzi_Isenzo) { 작업가닥 ithredi_ixabiso = new 작업가닥(umsebenzi_Isenzo); ithredi_ixabiso.qala_umsebenzi(); return ithredi_ixabiso; }
    public static void 기다리기(작업가닥 ithredi_ixabiso) throws 대기중단예외 { ithredi_ixabiso.기다리기(); }
    public static boolean 살아있는가(작업가닥 ithredi_ixabiso) { return ithredi_ixabiso.살아있는가(); }
    public static void misa_okwexeshana_umsebenzi() { 작업가닥.misa_okwexeshana_umsebenzi(); }
}
