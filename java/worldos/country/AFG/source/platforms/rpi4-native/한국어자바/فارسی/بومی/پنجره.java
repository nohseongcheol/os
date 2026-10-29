// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package فارسی.بومی;
/** بومی JVM과 커널의 پنجره 관리 기능에 직접 연결되는 پنجره. */
public final class پنجره extends 화면구성요소 {
    public پنجره(String پنجره_عنوان, int 폭, int 높이) {
        throw new وضعیت_استثنا("بومی JVM의 فارسی پنجره ایجاد 기능이 필요합니다.");
    }
    public native void افزودن_عنصر(화면구성요소 عنصر_مقدار);
    public native void نمایش_پنجره();
    public native void بستن();
    public native boolean 보이는가();
}
