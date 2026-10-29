// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package አማርኛ.자체;
/** 작업 ክር_እሴት: 하나의 ፈጽም_ትእዛዝ ልቀቅ_እሴት. 자체 JVM 안에서 ትእዛዝ 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 ማስኬጃ(실행할일 ተግባር_ምክር) { 작업가닥 ክር_እሴት = new 작업가닥(ተግባር_ምክር); ክር_እሴት.ጀምር_ተግባር(); return ክር_እሴት; }
    public static void 기다리기(작업가닥 ክር_እሴት) throws 대기중단예외 { ክር_እሴት.기다리기(); }
    public static boolean 살아있는가(작업가닥 ክር_እሴት) { return ክር_እሴት.살아있는가(); }
    public static void አግድ_ተግባር() { 작업가닥.አግድ_ተግባር(); }
}
