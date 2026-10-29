// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 작업 لڑی_قدر: 하나의 نفاذ_کرو_حکم سٹریم_قدر. 자체 JVM 안에서 حکم 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 چلاؤ(실행할일 ٹاسک_کم) { 작업가닥 لڑی_قدر = new 작업가닥(ٹاسک_کم); لڑی_قدر.مکھ_ٹاسک(); return لڑی_قدر; }
    public static void 기다리기(작업가닥 لڑی_قدر) throws 대기중단예외 { لڑی_قدر.기다리기(); }
    public static boolean 살아있는가(작업가닥 لڑی_قدر) { return لڑی_قدر.살아있는가(); }
    public static void معطل_کیتا_گیا_ٹاسک() { 작업가닥.معطل_کیتا_گیا_ٹاسک(); }
}
