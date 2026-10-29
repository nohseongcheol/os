// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros aṣàmúlò ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class aṣàmúlò {
    public static native int 파일서술자열기(int[] fáìlì_ìgbéwọlé_orúkọ, int ṣí_Àwọn_ààtò);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int báìtì_iye);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] Orúkọ, int[] détà);
    public static native int kọ_ẹyọ_ọ̀rọ̀_iye(int 문자);
    public static native int kọ_fáìlì(int[] Orúkọ, int[] détà, int gígùn_iye);
    public static native int Kọ(String Àkóónú_iye);
    public static native int 인수개수();
    public static native String 인수(int wá_atọ̀ka_àkóónú);
    public static native int 실행권한();
    public static native int ṣí_Alásopọ̀(int agbègbè_ojú);
    public static native int í_meèlì_détà(int èkù_iye, int àdírẹ́ẹ̀sì, int èbúté_ojú, int[] détà, int gígùn_iye);
    public static native int 자료받기(int èkù_iye, int[] détà, int 제한밀리초);
    public static native int pa_dé_Alásopọ̀(int èkù_iye);
    public static native int 내주소();
    public static native int 보낸주소(int èkù_iye);
    public static native int 보낸창구(int èkù_iye);
}
