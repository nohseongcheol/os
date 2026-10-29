// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 મશીન 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class બોર્ડ {
    public static native int 표시화소읽기(int 가로, int ઊભી_સ્થિતિ);
    public static native void લખો_પ્રદર્શન_પેલ(int 가로, int ઊભી_સ્થિતિ, int 색);
    public static native int છાયાંકિત(int 종류, int ક્રિયા);
    public static native void અંત_કરો_રિમોટ_આદેશ(int સ્થિતિ_મૂલ્ય_e10195a1);
    public static native void રિમોટ_પ્રતીક્ષા(int સ્થિતિ_મૂલ્ય_e10195a1);
    public static native void 직렬쓰기(int મૂલ્ય);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int 시피유권한();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int ઊભી_સ્થિતિ, int 색);
    public static native void સ્થગિત_કરો_પ્રોસેસર();
    public static native int બનાવો_કાર્ય(int અનુક્રમણિકા);
    public static native int કાર્ય_સ્થિતિ(int અનુક્રમણિકા);
    public static native void અટકાવો(int સ્થિતિ_મૂલ્ય_e10195a1);
    public static native int 씨플러스시험();
    public static native int ચલાવો_ઉપયોગકર્તા_એપ્લિકેશન(int અનુક્રમણિકા);
    public static native int તપાસો_ઉપયોગકર્તા_એપ્લિકેશન();
    public static native int 인수준비(int 개수);
    public static native int અમલ_કરો_ઉપયોગકર્તા_ફાઇલ();
    public static native int 리눅스파일실행();
    public static native int દલીલ_બાઇટ(int અનુક્રમણિકા, int સ્થાન, int મૂલ્ય);
    public static native int ટર્મિનલ(int ક્રિયા);
    public static native int નિયંત્રણ_ઉપયોગકર્તા_એપ્લિકેશન(int ક્રિયા);
    public static native void 입출력전환(int ક્રિયા);
    public static native int ફાઇલ_સ્થાનાંતર_સેવા(int ક્રિયા);
    public static native int નેટવર્ક_સ્થિતિ(int પ્રવેશ_મૂલ્ય, int અનુક્રમણિકા);
    public static native int નેટવર્ક_સેટિંગ્સ(int ક્રિયા, int સરનામું, int માસ્ક_મૂલ્ય, int ગેટવે_મૂલ્ય);
    public static native int મોકલો_પ્રતિસાદ(int સરનામું, int ક્રમ_મૂલ્ય);
    public static native int 응답읽기(int પ્રવેશ_મૂલ્ય);
    public static native int ક્વેરી_સિસ્ટમ(int પ્રવેશ_મૂલ્ય, int અનુક્રમણિકા);
    public static native void 전원끄기();
}
