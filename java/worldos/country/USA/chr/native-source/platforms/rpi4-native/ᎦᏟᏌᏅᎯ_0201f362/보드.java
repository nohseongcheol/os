// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 기계 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class 보드 {
    public static native int 표시화소읽기(int 가로, int 세로);
    public static native void ᎪᏪᎶᏗ_ᎬᏂᎨᏒ_ᏅᎦ_pel(int 가로, int 세로, int 색);
    public static native int ᎤᏓᏴᎳᏛ_f0c1d914(int 종류, int ᎠᏛᏁᎵᏓ);
    public static native void 원격명령끝(int ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ);
    public static native void 원격대기(int ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ);
    public static native void 직렬쓰기(int ᏧᎬᏩᎶᏗᏯ);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int 시피유권한();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int 세로, int 색);
    public static native void ᏗᏲᎯᏍᏗᎢ_CPU();
    public static native int 작업만들기(int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ);
    public static native int ᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅ(int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ);
    public static native void ᎭᎴᏫᏍᏓ(int ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ);
    public static native int 씨플러스시험();
    public static native int ᎠᎢᏎᏍᏗ_ᎬᏗᏍᎩ_ᎬᏙᏗ(int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ);
    public static native int ᎪᎯᏳᏔᏅ_ᎬᏗᏍᎩ_ᎬᏙᏗ();
    public static native int 인수준비(int 개수);
    public static native int ᎠᎴᏅᏗᏱ_ᎬᏗᏍᎩ_ᎠᏍᏆᏂᎪᏙᏗ();
    public static native int 리눅스파일실행();
    public static native int ᏗᏓᎦᏘᎸᏍᏗ_byte(int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ, int 위치, int ᏧᎬᏩᎶᏗᏯ);
    public static native int 터미널(int ᎠᏛᏁᎵᏓ);
    public static native int ᎠᎯᎸᏍᏗ_ᎬᏗᏍᎩ_ᎬᏙᏗ(int ᎠᏛᏁᎵᏓ);
    public static native void 입출력전환(int ᎠᏛᏁᎵᏓ);
    public static native int ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎢᏯᏓᏛᏁᏗ(int ᎠᏛᏁᎵᏓ);
    public static native int ᏧᎾᏚᏓᎵ_ᏄᏍᏗᏓᏅ(int Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ, int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ);
    public static native int ᏧᎾᏚᏓᎵ_ᏕᎦᎧᎲᎢ(int ᎠᏛᏁᎵᏓ, int ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, int 가림, int 관문);
    public static native int 응답보내기(int ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, int ᏗᎦᏅᏃᏙᏗ_ᏕᎦᏅᏃᏛᎢ_ᏧᎬᏩᎶᏗᏯ);
    public static native int 응답읽기(int Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ);
    public static native int ᎠᏛᏛᎲᏍᎩ_ᏄᏍᏗᏓᏅᎢ(int Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ, int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ);
    public static native void 전원끄기();
}
