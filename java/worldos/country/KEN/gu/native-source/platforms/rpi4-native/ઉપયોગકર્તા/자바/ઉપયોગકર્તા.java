// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 ઉપકરણો 전용 SVC સંપર્ક_કરો. 기존 x86 ઉપકરણો 원문을 함께 빌드한다. */
public final class ઉપયોગકર્તા {
    public static native int 파일서술자열기(int[] નામ, int સુયોજના);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int મૂલ્ય);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] નામ, int[] ડેટા);
    public static native int લખો_ફાઇલ(int[] નામ, int[] ડેટા, int લંબાઈ_મૂલ્ય);
    public static native int લખો(String લખાણ);
    public static native int લખો_વર્ણ_મૂલ્ય(int મૂલ્ય);
    public static native int 인수개수();
    public static native String દલીલો(int અનુક્રમણિકા);
    public static native int 도구번호();
    public static native int 화면연결(int ક્રિયા, int અનુક્રમણિકા, int 가, int 나, int 다, int 라);
    public static native int 화면글(int અનુક્રમણિકા, int[] લખાણ, int લંબાઈ_મૂલ્ય);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int સ્ટ્રીમ_નિયંત્રણ(int ક્રિયા, int 서술자, int મૂલ્ય);
    public static native int કનેક્ટ_સ્ટ્રીમ(int 서술자, int સરનામું, int પૉર્ટ_મૂલ્ય);
    public static native int બનાવો_નેટવર્ક(int પૉર્ટ_મૂલ્ય);
    public static native int મોકલો_નેટવર્ક(int 서술자, int સરનામું, int પૉર્ટ_મૂલ્ય, int[] ડેટા, int લંબાઈ_મૂલ્ય);
    public static native int 통신받기(int 서술자, int[] ડેટા, int લંબાઈ_મૂલ્ય);
    public static native int નેટવર્ક_પૉર્ટ(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int ઊભી_સ્થિતિ, int 폭, int 높이, int 색);
}
