// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros përdorues ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class përdorues {
    public static native int 파일서술자열기(int[] skedar_futje_emër, int hap_cilësimet);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int bajt_VALUE);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] Emër, int[] të_dhëna);
    public static native int shkruaj_karakter_VALUE(int 문자);
    public static native int shkruaj_skedar(int[] Emër, int[] të_dhëna, int gjatësi_VALUE);
    public static native int Shkrimi(String Përmbajtje_VALUE);
    public static native int 인수개수();
    public static native String Argumente(int INDEX);
    public static native int 실행권한();
    public static native int hap_rrjet(int lokal_portë);
    public static native int dërgoj_të_dhëna(int dorezë_VALUE, int email, int vendmbërritje_portë, int[] të_dhëna, int gjatësi_VALUE);
    public static native int 자료받기(int dorezë_VALUE, int[] të_dhëna, int 제한밀리초);
    public static native int mbyll_rrjet(int dorezë_VALUE);
    public static native int 내주소();
    public static native int 보낸주소(int dorezë_VALUE);
    public static native int 보낸창구(int dorezë_VALUE);
}
