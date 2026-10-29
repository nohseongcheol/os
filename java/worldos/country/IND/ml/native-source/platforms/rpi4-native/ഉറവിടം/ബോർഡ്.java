// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 മെഷീൻ 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class ബോർഡ് {
    public static native int 표시화소읽기(int 가로, int ലംബം_പദവി);
    public static native void റൈറ്റ്_ചെയ്യുക_പ്രദര്_ശനം_പെല്(int 가로, int ലംബം_പദവി, int 색);
    public static native int ഷാഡോയിംഗ്(int 종류, int നടപടി);
    public static native void അവസാനിപ്പിക്കുക_വിദൂര_കമാന്_ഡ്(int അവസ്ഥ_മൂല്യം);
    public static native void വിദൂര_കാക്കുക(int അവസ്ഥ_മൂല്യം);
    public static native void 직렬쓰기(int മൂല്യം);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int പ്രോസസ്സര്_അനുമതി_നില();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int ലംബം_പദവി, int 색);
    public static native void താല്_ക്കാലികമായി_നിര്_ത്തുക_പ്രോസസ്സര്();
    public static native int സൃഷ്_ടിക്കുക_ചുമതല(int സൂചിക);
    public static native int ചുമതല_അവസ്ഥ(int സൂചിക);
    public static native void നിര്_ത്തുക(int അവസ്ഥ_മൂല്യം);
    public static native int 씨플러스시험();
    public static native int റണ്_ഉപയോക്താവ്_പ്രോഗ്രാം(int സൂചിക);
    public static native int ചെക്ക്_ഉപയോക്താവ്_പ്രോഗ്രാം();
    public static native int 인수준비(int 개수);
    public static native int നടപ്പാക്കുക_ഉപയോക്താവ്_ഫയല്();
    public static native int 리눅스파일실행();
    public static native int ആര്_ഗ്യുമെന്_റ്_బైట్(int സൂചിക, int സ്ഥാനം, int മൂല്യം);
    public static native int ടെ_ര്മിനല്(int നടപടി);
    public static native int നിയന്ത്രണം_ഉപയോക്താവ്_പ്രോഗ്രാം(int നടപടി);
    public static native void 입출력전환(int നടപടി);
    public static native int ഫയല്_കൈമാറുക_സേവനം(int നടപടി);
    public static native int നെറ്റ്_വർക്ക്_അവസ്ഥ(int എന്_ട്രി_മൂല്യം, int സൂചിക);
    public static native int നെറ്റ്_വർക്ക്_ക്രമീകരണം(int നടപടി, int ഇമെയിൽ, int മുഖംമൂടി_മൂല്യം, int ഗെയ്റ്റ്_വെ_മൂല്യം);
    public static native int 응답보내기(int ഇമെയിൽ, int ക്രമം_മൂല്യം);
    public static native int 응답읽기(int എന്_ട്രി_മൂല്യം);
    public static native int ചോദ്യം_సిస్టమ్(int എന്_ട്രി_മൂല്യം, int സൂചിക);
    public static native void 전원끄기();
}
