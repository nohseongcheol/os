// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 JVM과 커널의 ଓ୍ୱିଣ୍ଡୋ 관리 기능에 직접 연결되는 ଓ୍ୱିଣ୍ଡୋ. */
public final class ଓ୍ୱିଣ୍ଡୋ extends 화면구성요소 {
    public ଓ୍ୱିଣ୍ଡୋ(String ଓ୍ୱିଣ୍ଡୋ_ଟାଇଟେଲ୍, int 폭, int 높이) {
        throw new ସ୍ଥିତି_ବ୍ୟତିକ୍ରମ("자체 JVM의 한국어 ଓ୍ୱିଣ୍ଡୋ ସୃଷ୍ଟି_କରିବା 기능이 필요합니다.");
    }
    public native void ଯୋଡ଼ିବା_ଉପାଦାନ(화면구성요소 ଉପାଦାନ_ମୂଲ୍ୟ);
    public native void ପ୍ରଦର୍ଶନ_କରିବା_ଓ୍ୱିଣ୍ଡୋ();
    public native void ବନ୍ଦ_କରନ୍ତୁ();
    public native boolean 보이는가();
}
