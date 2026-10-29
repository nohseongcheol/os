// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros cleachdaiche ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class cleachdaiche {
    public static native int 파일서술자열기(int[] faidhle_cur_a_steach_ainm, int fosgail_roghainnean);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int baidht_VALUE);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] Ainm, int[] dàta);
    public static native int sgrìobh_caractar_VALUE(int 문자);
    public static native int sgrìobh_faidhle(int[] Ainm, int[] dàta, int faid_VALUE);
    public static native int sgrìobh(String susbaint_VALUE);
    public static native int 인수개수();
    public static native String 인수(int INDEX);
    public static native int 실행권한();
    public static native int fosgail_lìonra(int ionadail_port);
    public static native int cuir_dàta(int làmhrachan_VALUE, int ADDRESS, int ceann_uidhe_port, int[] dàta, int faid_VALUE);
    public static native int 자료받기(int làmhrachan_VALUE, int[] dàta, int 제한밀리초);
    public static native int dùin_lìonra(int làmhrachan_VALUE);
    public static native int 내주소();
    public static native int 보낸주소(int làmhrachan_VALUE);
    public static native int 보낸창구(int làmhrachan_VALUE);
}
