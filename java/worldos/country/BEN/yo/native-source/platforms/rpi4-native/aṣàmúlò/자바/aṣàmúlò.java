// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 Àwọn_irinṣẹ́ 전용 SVC Darapọ̀. 기존 x86 Àwọn_irinṣẹ́ 원문을 함께 빌드한다. */
public final class aṣàmúlò {
    public static native int 파일서술자열기(int[] Orúkọ, int Àwọn_ààtò);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int iye);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] Orúkọ, int[] détà);
    public static native int kọ_fáìlì(int[] Orúkọ, int[] détà, int gígùn_iye);
    public static native int Kọ(String SMS);
    public static native int kọ_ẹyọ_ọ̀rọ̀_iye(int iye);
    public static native int 인수개수();
    public static native String 인수(int wá_atọ̀ka_àkóónú);
    public static native int 도구번호();
    public static native int 화면연결(int ìṣe, int wá_atọ̀ka_àkóónú, int 가, int 나, int 다, int 라);
    public static native int 화면글(int wá_atọ̀ka_àkóónú, int[] SMS, int gígùn_iye);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int Stream_ìdarí(int ìṣe, int 서술자, int iye);
    public static native int SOMỌ́_Stream(int 서술자, int àdírẹ́ẹ̀sì, int ojú_iye);
    public static native int ṣí_Alásopọ̀(int ojú_iye);
    public static native int í_meèlì_Alásopọ̀(int 서술자, int àdírẹ́ẹ̀sì, int ojú_iye, int[] détà, int gígùn_iye);
    public static native int 통신받기(int 서술자, int[] détà, int gígùn_iye);
    public static native int Alásopọ̀_ojú(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int 세로, int 폭, int 높이, int 색);
}
