// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 작업 පොට_අගය: 하나의 ක්_රියාත්මක_කරන්න_විධානය දහර_අගය. 자체 JVM 안에서 විධානය 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 ක්_රියාත්මක_කරන්න_2(실행할일 කාර්යය_ක්_රියාව) { 작업가닥 පොට_අගය = new 작업가닥(කාර්යය_ක්_රියාව); පොට_අගය.ඇරඹුම_කාර්යය(); return පොට_අගය; }
    public static void 기다리기(작업가닥 පොට_අගය) throws 대기중단예외 { පොට_අගය.기다리기(); }
    public static boolean 살아있는가(작업가닥 පොට_අගය) { return පොට_අගය.살아있는가(); }
    public static void අත්හිටුවන්න_කාර්යය() { 작업가닥.අත්හිටුවන්න_කාර්යය(); }
}
