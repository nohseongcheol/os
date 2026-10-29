// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros ઉપયોગકર્તા ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class ઉપયોગકર્તા {
    public static native int 파일서술자열기(int[] ફાઇલ_પ્રવેશ_નામ, int બનાવો_સેટિંગ્સ);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int બાઇટ_મૂલ્ય);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] નામ, int[] ડેટા);
    public static native int લખો_વર્ણ_મૂલ્ય(int 문자);
    public static native int લખો_ફાઇલ(int[] નામ, int[] ડેટા, int લંબાઈ_મૂલ્ય);
    public static native int લખો(String સામગ્રી_મૂલ્ય);
    public static native int 인수개수();
    public static native String દલીલો(int અનુક્રમણિકા);
    public static native int 실행권한();
    public static native int બનાવો_નેટવર્ક(int સ્થાનિક_પૉર્ટ);
    public static native int મોકલો_ડેટા(int હેન્ડલ_મૂલ્ય, int સરનામું, int ગંતવ્ય_પૉર્ટ, int[] ડેટા, int લંબાઈ_મૂલ્ય);
    public static native int 자료받기(int હેન્ડલ_મૂલ્ય, int[] ડેટા, int 제한밀리초);
    public static native int બંધ_કરો_નેટવર્ક(int હેન્ડલ_મૂલ્ય);
    public static native int 내주소();
    public static native int 보낸주소(int હેન્ડલ_મૂલ્ય);
    public static native int 보낸창구(int હેન્ડલ_મૂલ્ય);
}
