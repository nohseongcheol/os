// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 작업 ଧାରା_ମୂଲ୍ୟ: 하나의 ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ ଷ୍ଟ୍ରିମ୍_ମୂଲ୍ୟ. 자체 JVM 안에서 ନିର୍ଦ୍ଦେଶ 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 ଚଳାନ୍ତୁ(실행할일 ଟାସ୍କ_କ୍ରିୟା) { 작업가닥 ଧାରା_ମୂଲ୍ୟ = new 작업가닥(ଟାସ୍କ_କ୍ରିୟା); ଧାରା_ମୂଲ୍ୟ.ଆରମ୍ଭ_ଟାସ୍କ(); return ଧାରା_ମୂଲ୍ୟ; }
    public static void 기다리기(작업가닥 ଧାରା_ମୂଲ୍ୟ) throws 대기중단예외 { ଧାରା_ମୂଲ୍ୟ.기다리기(); }
    public static boolean 살아있는가(작업가닥 ଧାରା_ମୂଲ୍ୟ) { return ଧାରା_ମୂଲ୍ୟ.살아있는가(); }
    public static void ରଦ୍ଧ_ହୋଇଛି_ଟାସ୍କ() { 작업가닥.ରଦ୍ଧ_ହୋଇଛି_ଟାସ୍କ(); }
}
