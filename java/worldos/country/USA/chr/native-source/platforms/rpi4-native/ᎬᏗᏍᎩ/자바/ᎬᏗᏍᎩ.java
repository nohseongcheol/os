// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 도구 전용 SVC ᎫᏓᎳ. 기존 x86 도구 원문을 함께 빌드한다. */
public final class ᎬᏗᏍᎩ {
    public static native int 파일서술자열기(int[] ᏚᏙᎥᎢ, int ᏕᎦᎧᎲᎢ);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int ᏧᎬᏩᎶᏗᏯ);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] ᏚᏙᎥᎢ, int[] ᎦᏟᏌᏅᎯ);
    public static native int ᎪᏪᎶᏗ_ᎠᏍᏆᏂᎪᏙᏗ(int[] ᏚᏙᎥᎢ, int[] ᎦᏟᏌᏅᎯ, int ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ);
    public static native int ᎪᏪᎶᏗ(String ᎠᎪᎵᏰᏗ);
    public static native int ᎪᏪᎶᏗ_ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ(int ᏧᎬᏩᎶᏗᏯ);
    public static native int 인수개수();
    public static native String 인수(int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ);
    public static native int 도구번호();
    public static native int 화면연결(int ᎠᏛᏁᎵᏓ, int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ, int 가, int 나, int 다, int 라);
    public static native int 화면글(int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ, int[] ᎠᎪᎵᏰᏗ, int ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int ᎤᏪᎬ_ᎠᎯᎸᏍᏗ(int ᎠᏛᏁᎵᏓ, int 서술자, int ᏧᎬᏩᎶᏗᏯ);
    public static native int ᎫᏓᎳ_ᎤᏪᎬ(int 서술자, int ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, int ᎫᏓᎸᏗ_ᏧᎬᏩᎶᏗᏯ);
    public static native int ᎯᏍᏚᎢ_ᏧᎾᏚᏓᎵ(int ᎫᏓᎸᏗ_ᏧᎬᏩᎶᏗᏯ);
    public static native int ᏫᎦᏅᏗ_ᏧᎾᏚᏓᎵ(int 서술자, int ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, int ᎫᏓᎸᏗ_ᏧᎬᏩᎶᏗᏯ, int[] ᎦᏟᏌᏅᎯ, int ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ);
    public static native int 통신받기(int 서술자, int[] ᎦᏟᏌᏅᎯ, int ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ);
    public static native int ᏧᎾᏚᏓᎵ_ᎫᏓᎸᏗ(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int 세로, int 폭, int 높이, int 색);
}
