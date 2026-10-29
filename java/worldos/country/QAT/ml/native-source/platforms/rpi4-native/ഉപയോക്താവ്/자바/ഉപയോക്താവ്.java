// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 ഉപകരണങ്ങൾ 전용 SVC കണക്ടു്_ചെയ്യുക. 기존 x86 ഉപകരണങ്ങൾ 원문을 함께 빌드한다. */
public final class ഉപയോക്താവ് {
    public static native int 파일서술자열기(int[] പേരു്, int സജ്ജീകരണം);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int മൂല്യം);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] പേരു്, int[] ഡാറ്റാ);
    public static native int റൈറ്റ്_ചെയ്യുക_ഫയല്(int[] പേരു്, int[] ഡാറ്റാ, int ദൈര്_ഘ്യം_മൂല്യം);
    public static native int എഴുത്തു്(String പദാവലി);
    public static native int റൈറ്റ്_ചെയ്യുക_പ്രതീകം_മൂല്യം(int മൂല്യം);
    public static native int 인수개수();
    public static native String 인수(int സൂചിക);
    public static native int 도구번호();
    public static native int 화면연결(int നടപടി, int സൂചിക, int 가, int 나, int 다, int 라);
    public static native int 화면글(int സൂചിക, int[] പദാവലി, int ദൈര്_ഘ്യം_മൂല്യം);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int സ്ട്രീം_നിയന്ത്രണം(int നടപടി, int 서술자, int മൂല്യം);
    public static native int കണക്റ്റ്_സ്ട്രീം(int 서술자, int ഇമെയിൽ, int പോര്_ട്ട്_മൂല്യം);
    public static native int തുറക്കുക_നെറ്റ്_വർക്ക്(int പോര്_ട്ട്_മൂല്യം);
    public static native int അയയ്ക്കുക_നെറ്റ്_വർക്ക്(int 서술자, int ഇമെയിൽ, int പോര്_ട്ട്_മൂല്യം, int[] ഡാറ്റാ, int ദൈര്_ഘ്യം_മൂല്യം);
    public static native int 통신받기(int 서술자, int[] ഡാറ്റാ, int ദൈര്_ഘ്യം_മൂല്യം);
    public static native int നെറ്റ്_വർക്ക്_പോര്_ട്ട്(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int ലംബം_പദവി, int 폭, int 높이, int 색);
}
