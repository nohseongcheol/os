// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Isi_Zulu.자체;
/** 작업 uhlu_lwemilayezo_inani: 하나의 yenza_umyalo Stream_inani. 자체 JVM 안에서 Umlayelo 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 Sebenzisa(실행할일 umsebenzi_isenzo) { 작업가닥 uhlu_lwemilayezo_inani = new 작업가닥(umsebenzi_isenzo); uhlu_lwemilayezo_inani.qala_umsebenzi(); return uhlu_lwemilayezo_inani; }
    public static void 기다리기(작업가닥 uhlu_lwemilayezo_inani) throws 대기중단예외 { uhlu_lwemilayezo_inani.기다리기(); }
    public static boolean 살아있는가(작업가닥 uhlu_lwemilayezo_inani) { return uhlu_lwemilayezo_inani.살아있는가(); }
    public static void misa_okwesikhashana_umsebenzi() { 작업가닥.misa_okwesikhashana_umsebenzi(); }
}
