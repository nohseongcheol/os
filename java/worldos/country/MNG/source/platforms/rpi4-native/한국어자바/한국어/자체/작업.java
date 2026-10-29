// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 작업 яриа_утга: 하나의 Гүйцэтгэх_команд урсгал_утга. 자체 JVM 안에서 Тушаал 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 Ажиллуулах(실행할일 даалгавар_үйлдэл) { 작업가닥 яриа_утга = new 작업가닥(даалгавар_үйлдэл); яриа_утга.Эхлэл_даалгавар(); return яриа_утга; }
    public static void 기다리기(작업가닥 яриа_утга) throws 대기중단예외 { яриа_утга.기다리기(); }
    public static boolean 살아있는가(작업가닥 яриа_утга) { return яриа_утга.살아있는가(); }
    public static void түдгэлзүүлэх_даалгавар() { 작업가닥.түдгэлзүүлэх_даалгавар(); }
}
