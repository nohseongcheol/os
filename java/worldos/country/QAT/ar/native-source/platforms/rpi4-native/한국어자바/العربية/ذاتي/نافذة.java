// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package العربية.ذاتي;
/** ذاتي JVM과 커널의 نافذة 관리 기능에 직접 연결되는 نافذة. */
public final class نافذة extends 화면구성요소 {
    public نافذة(String نافذة_عنوان, int 폭, int ارتفاع_قيمة) {
        throw new حالة_استثناء("ذاتي JVM의 العربية نافذة إنشاء 기능이 필요합니다.");
    }
    public native void يضيف_عنصر(화면구성요소 عنصر_قيمة);
    public native void عرض_نافذة();
    public native void إغلاق();
    public native boolean 보이는가();
}
