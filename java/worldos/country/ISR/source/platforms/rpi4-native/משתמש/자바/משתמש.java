// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 כלים 전용 SVC חיבור. 기존 x86 כלים 원문을 함께 빌드한다. */
public final class משתמש {
    public static native int 파일서술자열기(int[] שם, int הגדרות);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int ערך);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] שם, int[] נתונים);
    public static native int כתיבה_קובץ(int[] שם, int[] נתונים, int 길이);
    public static native int כתוב(String טקסט);
    public static native int כתיבה_תו_ערך(int ערך);
    public static native int 인수개수();
    public static native String ארגומנטים(int מדד);
    public static native int 도구번호();
    public static native int 화면연결(int פעולה, int מדד, int 가, int 나, int 다, int 라);
    public static native int 화면글(int מדד, int[] טקסט, int 길이);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int זרם_פקד(int פעולה, int 서술자, int ערך);
    public static native int לקשר_זרם(int 서술자, int למען, int הסב_ערך);
    public static native int פתח_רשת(int הסב_ערך);
    public static native int שלח_רשת(int 서술자, int למען, int הסב_ערך, int[] נתונים, int 길이);
    public static native int לקבל_רשת(int 서술자, int[] נתונים, int 길이);
    public static native int רשת_הסב(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int מלבן(int 가로, int אנכי_עמדה, int 폭, int גובה_ערך, int 색);
}
