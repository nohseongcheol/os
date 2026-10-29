// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package नेपाली.निज;
/** निज JVM 스케줄러가 관리하는 कार्यान्वयन_गर्नुहोस्_आदेश प्रवाह_मान. 표준 Thread를 감싸지 않는다. */
public final class 작업가닥 {
    public 작업가닥(실행할일 कार्य_कार्य) {
        throw new 상태예외("निज JVM의 नेपाली 작업 धागो_मान सिर्जना_गर्नुहोस् 기능이 필요합니다.");
    }
    public native void सुरु_कार्य() throws 가닥상태예외;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void स्थगन_गर्नुहोस्_कार्य();
}
