// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 JVM과 커널의 ജാലകം 관리 기능에 직접 연결되는 ജാലകം. */
public final class ജാലകം extends 화면구성요소 {
    public ജാലകം(String ജാലകം_ശീർഷകം, int 폭, int 높이) {
        throw new അവസ്ഥ_ഒഴിവാക്കൽ("자체 JVM의 한국어 ജാലകം സൃഷ്_ടിക്കുക 기능이 필요합니다.");
    }
    public native void ചേ൪ക്കുക_ഘടകാംശം(화면구성요소 ഘടകാംശം_മൂല്യം);
    public native void പ്രദർശനം_ജാലകം();
    public native void അടയ്ക്കു();
    public native boolean 보이는가();
}
