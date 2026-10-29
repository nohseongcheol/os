// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 ఉపకరణాలు 전용 SVC కనెక్టుచేయి. 기존 x86 ఉపకరణాలు 원문을 함께 빌드한다. */
public final class వినియోగదారు {
    public static native int 파일서술자열기(int[] పేరు, int అమరికలు);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int మూల్యం);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] పేరు, int[] డేటా);
    public static native int వ్రాయి_ఫైలు(int[] పేరు, int[] డేటా, int పొడవు_మూల్యం);
    public static native int వ్రాయుము(String పాఠ్యము);
    public static native int వ్రాయి_అక్షరం_మూల్యం(int మూల్యం);
    public static native int 인수개수();
    public static native String 인수(int సూచీ);
    public static native int 도구번호();
    public static native int 화면연결(int చర్య, int సూచీ, int 가, int 나, int 다, int 라);
    public static native int 화면글(int సూచీ, int[] పాఠ్యము, int పొడవు_మూల్యం);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int ధార_నియంత్రణ(int చర్య, int 서술자, int మూల్యం);
    public static native int అనుసంధానించు_ధార(int 서술자, int ఇమెయిల్, int పోర్టు_మూల్యం);
    public static native int తెరువు_నెట్_వర్క్(int పోర్టు_మూల్యం);
    public static native int పంపు_నెట్_వర్క్(int 서술자, int ఇమెయిల్, int పోర్టు_మూల్యం, int[] డేటా, int పొడవు_మూల్యం);
    public static native int 통신받기(int 서술자, int[] డేటా, int పొడవు_మూల్యం);
    public static native int నెట్_వర్క్_పోర్టు(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int నిలువు_స్థాయి, int 폭, int 높이, int 색);
}
