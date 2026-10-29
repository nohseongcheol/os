// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 JVM 스케줄러가 관리하는 നടപ്പാക്കുക_കമാന്_ഡ് സ്ട്രീം_മൂല്യം. 표준 Thread를 감싸지 않는다. */
public final class 작업가닥 {
    public 작업가닥(실행할일 ചുമതല_ക്രിയ) {
        throw new അവസ്ഥ_ഒഴിവാക്കൽ("자체 JVM의 한국어 작업 ത്രെഡ്_മൂല്യം സൃഷ്_ടിക്കുക 기능이 필요합니다.");
    }
    public native void ആരംഭം_ചുമതല() throws ത്രെഡ്_അവസ്ഥ_ഒഴിവാക്കൽ;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void താല്_ക്കാലികമായി_നിര്_ത്തുക_ചുമതല();
}
