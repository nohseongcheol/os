// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package አማርኛ.자체;
/** 자체 JVM과 커널의 መስኮት 관리 기능에 직접 연결되는 መስኮት. */
public final class መስኮት extends 화면구성요소 {
    public መስኮት(String መስኮት_ርዕስ, int 폭, int 높이) {
        throw new ዞን_ልዩነት("자체 JVM의 አማርኛ መስኮት አዘጋጅ 기능이 필요합니다.");
    }
    public native void አክል_አባል(화면구성요소 አባል_እሴት);
    public native void አሳይ_መስኮት();
    public native void መዝጊያ();
    public native boolean 보이는가();
}
