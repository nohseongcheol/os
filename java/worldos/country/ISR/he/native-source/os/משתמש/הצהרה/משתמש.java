// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros משתמש ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class משתמש {
    public static native int 파일서술자열기(int[] קובץ_ערך_שם, int פתח_הגדרות);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int בית_ערך);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] שם, int[] נתונים);
    public static native int כתיבה_תו_ערך(int 문자);
    public static native int כתיבה_קובץ(int[] שם, int[] נתונים, int 길이);
    public static native int כתוב(String תוכן_ערך);
    public static native int 인수개수();
    public static native String ארגומנטים(int מדד);
    public static native int 실행권한();
    public static native int פתח_רשת(int מקומי_הסב);
    public static native int שלח_נתונים(int נקודת_אחיזה_ערך, int למען, int יעד_הסב, int[] נתונים, int 길이);
    public static native int לקבל_נתונים(int נקודת_אחיזה_ערך, int[] נתונים, int 제한밀리초);
    public static native int סגור_רשת(int נקודת_אחיזה_ערך);
    public static native int 내주소();
    public static native int 보낸주소(int נקודת_אחיזה_ערך);
    public static native int 보낸창구(int נקודת_אחיזה_ערך);
}
