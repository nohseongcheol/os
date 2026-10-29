// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 작업 ڕستە_نرخ: 하나의 جێبەجێکردن_فەرمان Stream_نرخ. 자체 JVM 안에서 فەرمان 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 ڕادان(실행할일 ئەرک_ئاکشن) { 작업가닥 ڕستە_نرخ = new 작업가닥(ئەرک_ئاکشن); ڕستە_نرخ.دەستپێك_ئەرک(); return ڕستە_نرخ; }
    public static void 기다리기(작업가닥 ڕستە_نرخ) throws 대기중단예외 { ڕستە_نرخ.기다리기(); }
    public static boolean 살아있는가(작업가닥 ڕستە_نرخ) { return ڕستە_نرخ.살아있는가(); }
    public static void هەڵپەساردن_ئەرک() { 작업가닥.هەڵپەساردن_ئەرک(); }
}
