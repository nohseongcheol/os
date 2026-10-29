// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros వినియోగదారు ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class వినియోగదారు {
    public static native int 파일서술자열기(int[] ఫైలు_ప్రవేశం_పేరు, int తెరువు_సెట్టింగ్_లు);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int బైట్_మూల్యం);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] పేరు, int[] డేటా);
    public static native int వ్రాయి_అక్షరం_మూల్యం(int 문자);
    public static native int వ్రాయి_ఫైలు(int[] పేరు, int[] డేటా, int పొడవు_మూల్యం);
    public static native int వ్రాయుము(String విషయం_మూల్యం);
    public static native int 인수개수();
    public static native String 인수(int సూచీ);
    public static native int 실행권한();
    public static native int తెరువు_నెట్_వర్క్(int స్థానిక_పోర్టు);
    public static native int పంపు_డేటా(int నిర్వాహకం_మూల్యం, int ఇమెయిల్, int గమ్యం_పోర్టు, int[] డేటా, int పొడవు_మూల్యం);
    public static native int 자료받기(int నిర్వాహకం_మూల్యం, int[] డేటా, int 제한밀리초);
    public static native int మూసివేయి_నెట్_వర్క్(int నిర్వాహకం_మూల్యం);
    public static native int 내주소();
    public static native int 보낸주소(int నిర్వాహకం_మూల్యం);
    public static native int 보낸창구(int నిర్వాహకం_మూల్యం);
}
