// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 작업 ᎪᏪᎵ_ᏕᎦᏅᏃᏛᎢ_ᏧᎬᏩᎶᏗᏯ: 하나의 ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ ᎤᏪᎬ_ᏧᎬᏩᎶᏗᏯ. 자체 JVM 안에서 ᎤᏁᏤᎸᎩ 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 ᎠᎢᏎᏍᏗ(실행할일 ᏯᏛᏁᏗ_ᎠᏛᏁᎵᏓ) { 작업가닥 ᎪᏪᎵ_ᏕᎦᏅᏃᏛᎢ_ᏧᎬᏩᎶᏗᏯ = new 작업가닥(ᏯᏛᏁᏗ_ᎠᏛᏁᎵᏓ); ᎪᏪᎵ_ᏕᎦᏅᏃᏛᎢ_ᏧᎬᏩᎶᏗᏯ.ᎭᏂᎩᏍᏓ_ᏯᏛᏁᏗ(); return ᎪᏪᎵ_ᏕᎦᏅᏃᏛᎢ_ᏧᎬᏩᎶᏗᏯ; }
    public static void 기다리기(작업가닥 ᎪᏪᎵ_ᏕᎦᏅᏃᏛᎢ_ᏧᎬᏩᎶᏗᏯ) throws 대기중단예외 { ᎪᏪᎵ_ᏕᎦᏅᏃᏛᎢ_ᏧᎬᏩᎶᏗᏯ.기다리기(); }
    public static boolean 살아있는가(작업가닥 ᎪᏪᎵ_ᏕᎦᏅᏃᏛᎢ_ᏧᎬᏩᎶᏗᏯ) { return ᎪᏪᎵ_ᏕᎦᏅᏃᏛᎢ_ᏧᎬᏩᎶᏗᏯ.살아있는가(); }
    public static void ᏗᏲᎯᏍᏗᎢ_ᏯᏛᏁᏗ() { 작업가닥.ᏗᏲᎯᏍᏗᎢ_ᏯᏛᏁᏗ(); }
}
