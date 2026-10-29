// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros gumagamit ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class gumagamit {
    public static native int 파일서술자열기(int[] file_pagpasok_pangalan, int buksan_Mga_Setting);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int byte_VALUE);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] pangalan, int[] data);
    public static native int sumulat_karakter_VALUE(int 문자);
    public static native int sumulat_file(int[] pangalan, int[] data, int haba_VALUE);
    public static native int sumulat(String Nilalaman_VALUE);
    public static native int 인수개수();
    public static native String 인수(int INDEX);
    public static native int 실행권한();
    public static native int buksan_Network(int lokal_port);
    public static native int i_email_data(int hawakán_VALUE, int email, int patutunguhan_port, int[] data, int haba_VALUE);
    public static native int 자료받기(int hawakán_VALUE, int[] data, int 제한밀리초);
    public static native int isara_Network(int hawakán_VALUE);
    public static native int 내주소();
    public static native int 보낸주소(int hawakán_VALUE);
    public static native int 보낸창구(int hawakán_VALUE);
}
