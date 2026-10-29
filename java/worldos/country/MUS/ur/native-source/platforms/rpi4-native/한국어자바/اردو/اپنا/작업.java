// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package اردو.اپنا;
/** 작업 تھریڈ_قدر: 하나의 نفاذ_کریں_حکم بہاؤ_قدر. اپنا JVM 안에서 حکم 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 چلائیں(실행할일 ٹاسک_عمل) { 작업가닥 تھریڈ_قدر = new 작업가닥(ٹاسک_عمل); تھریڈ_قدر.ابتدا_ٹاسک(); return تھریڈ_قدر; }
    public static void 기다리기(작업가닥 تھریڈ_قدر) throws 대기중단예외 { تھریڈ_قدر.기다리기(); }
    public static boolean 살아있는가(작업가닥 تھریڈ_قدر) { return تھریڈ_قدر.살아있는가(); }
    public static void معطل_کریں_ٹاسک() { 작업가닥.معطل_کریں_ٹاسک(); }
}
