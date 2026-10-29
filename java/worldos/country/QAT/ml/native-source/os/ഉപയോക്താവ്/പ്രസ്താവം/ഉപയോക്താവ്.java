// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros ഉപയോക്താവ് ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class ഉപയോക്താവ് {
    public static native int 파일서술자열기(int[] ഫയല്_എന്_ട്രി_നാ_മം, int തുറക്കുക_ക്രമീകരണം);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int బైట్_മൂല്യം);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] പേരു്, int[] ഡാറ്റാ);
    public static native int റൈറ്റ്_ചെയ്യുക_പ്രതീകം_മൂല്യം(int 문자);
    public static native int റൈറ്റ്_ചെയ്യുക_ഫയല്(int[] പേരു്, int[] ഡാറ്റാ, int ദൈര്_ഘ്യം_മൂല്യം);
    public static native int എഴുത്തു്(String ഉള്ളടക്കം_മൂല്യം);
    public static native int 인수개수();
    public static native String 인수(int സൂചിക);
    public static native int 실행권한();
    public static native int തുറക്കുക_നെറ്റ്_വർക്ക്(int ലോക്കല്_പോര്_ട്ട്);
    public static native int അയയ്ക്കുക_ഡാറ്റാ(int കൈകാര്യംചെയ്യല്_മൂല്യം, int ഇമെയിൽ, int ഉദ്ദിഷ്ടസ്ഥാനം_പോര്_ട്ട്, int[] ഡാറ്റാ, int ദൈര്_ഘ്യം_മൂല്യം);
    public static native int 자료받기(int കൈകാര്യംചെയ്യല്_മൂല്യം, int[] ഡാറ്റാ, int 제한밀리초);
    public static native int അടയ്ക്കുക_നെറ്റ്_വർക്ക്(int കൈകാര്യംചെയ്യല്_മൂല്യം);
    public static native int 내주소();
    public static native int 보낸주소(int കൈകാര്യംചെയ്യല്_മൂല്യം);
    public static native int 보낸창구(int കൈകാര്യംചെയ്യല്_മൂല്യം);
}
