// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class 작업 {
    private 작업() {}
    public static Thread ᎠᎢᏎᏍᏗ(String ᏚᏙᎥᎢ, Runnable ᎠᏛᏁᎵᏓ) {
        Thread ᎪᏪᎵ_ᏕᎦᏅᏃᏛᎢ_ᏧᎬᏩᎶᏗᏯ = new Thread(ᎠᏛᏁᎵᏓ, ᏚᏙᎥᎢ);
        ᎪᏪᎵ_ᏕᎦᏅᏃᏛᎢ_ᏧᎬᏩᎶᏗᏯ.start();
        return ᎪᏪᎵ_ᏕᎦᏅᏃᏛᎢ_ᏧᎬᏩᎶᏗᏯ;
    }
    public static void 기다리기(Thread ᎪᏪᎵ_ᏕᎦᏅᏃᏛᎢ_ᏧᎬᏩᎶᏗᏯ) throws InterruptedException { ᎪᏪᎵ_ᏕᎦᏅᏃᏛᎢ_ᏧᎬᏩᎶᏗᏯ.join(); }
    public static void 쉬기(long 밀리초) throws InterruptedException { Thread.sleep(밀리초); }
    /** 호출자가 shutdown()으로 자원을 반환해야 한다. */
    public static ExecutorService 작업대(int 가닥수) { return Executors.newFixedThreadPool(가닥수); }
}
