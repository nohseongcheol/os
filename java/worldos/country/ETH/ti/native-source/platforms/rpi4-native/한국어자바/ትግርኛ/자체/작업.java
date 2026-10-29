// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ትግርኛ.자체;
/** 작업 ፈትሊ_ዋጋ: 하나의 ተግብር_ትእዛዝ ወሓዚ_ዋጋ. 자체 JVM 안에서 ትእዛዝ 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 ኣኺድ(실행할일 ዕማም_ስጉምቲ) { 작업가닥 ፈትሊ_ዋጋ = new 작업가닥(ዕማም_ስጉምቲ); ፈትሊ_ዋጋ.ጀምር_ዕማም(); return ፈትሊ_ዋጋ; }
    public static void 기다리기(작업가닥 ፈትሊ_ዋጋ) throws 대기중단예외 { ፈትሊ_ዋጋ.기다리기(); }
    public static boolean 살아있는가(작업가닥 ፈትሊ_ዋጋ) { return ፈትሊ_ዋጋ.살아있는가(); }
    public static void አግድ_ዕማም() { 작업가닥.አግድ_ዕማም(); }
}
