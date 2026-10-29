// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package বাংলা.নিজ;
/** নিজ JVM과 커널의 উইন্ডো 관리 기능에 직접 연결되는 উইন্ডো. */
public final class উইন্ডো extends 화면구성요소 {
    public উইন্ডো(String উইন্ডো_শিরোনাম, int 폭, int 높이) {
        throw new অবস্হা_ব্যতিক্রম("নিজ JVM의 বাংলা উইন্ডো সৃষ্টি_করুন 기능이 필요합니다.");
    }
    public native void যোগ_করা_উপাদান(화면구성요소 উপাদান_মান);
    public native void শো_উইন্ডো();
    public native void বন্ধ_করুন();
    public native boolean 보이는가();
}
