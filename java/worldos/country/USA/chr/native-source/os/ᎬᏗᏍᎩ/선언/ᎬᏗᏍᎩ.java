// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros ᎬᏗᏍᎩ ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class ᎬᏗᏍᎩ {
    public static native int 파일서술자열기(int[] ᎠᏍᏆᏂᎪᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏚᏙᎥᎢ, int ᎯᏍᏚᎢ_ᏕᎦᎧᎲᎢ);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int byte_ᏧᎬᏩᎶᏗᏯ);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] ᏚᏙᎥᎢ, int[] ᎦᏟᏌᏅᎯ);
    public static native int ᎪᏪᎶᏗ_ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ(int 문자);
    public static native int ᎪᏪᎶᏗ_ᎠᏍᏆᏂᎪᏙᏗ(int[] ᏚᏙᎥᎢ, int[] ᎦᏟᏌᏅᎯ, int ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ);
    public static native int ᎪᏪᎶᏗ(String ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ);
    public static native int 인수개수();
    public static native String 인수(int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ);
    public static native int 실행권한();
    public static native int ᎯᏍᏚᎢ_ᏧᎾᏚᏓᎵ(int ᎡᏍᎦᏂ_ᎫᏓᎸᏗ);
    public static native int ᏫᎦᏅᏗ_ᎦᏟᏌᏅᎯ(int ᎫᎭᏢ_ᏧᎬᏩᎶᏗᏯ, int ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, int ᏮᎦᏛᎢ_ᎫᏓᎸᏗ, int[] ᎦᏟᏌᏅᎯ, int ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ);
    public static native int 자료받기(int ᎫᎭᏢ_ᏧᎬᏩᎶᏗᏯ, int[] ᎦᏟᏌᏅᎯ, int 제한밀리초);
    public static native int ᎯᏍᏚᎲᎦ_ᏧᎾᏚᏓᎵ(int ᎫᎭᏢ_ᏧᎬᏩᎶᏗᏯ);
    public static native int 내주소();
    public static native int 보낸주소(int ᎫᎭᏢ_ᏧᎬᏩᎶᏗᏯ);
    public static native int 보낸창구(int ᎫᎭᏢ_ᏧᎬᏩᎶᏗᏯ);
}
