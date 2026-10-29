// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 מחשב 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class לוח {
    public static native int 표시화소읽기(int 가로, int אנכי_עמדה);
    public static native void כתיבה_צג_פיקסל(int 가로, int אנכי_עמדה, int 색);
    public static native int הוספת_צל(int 종류, int פעולה);
    public static native void סיים_שיחה_מרוחק_פקודה(int מצב_ערך);
    public static native void מרוחק_רק_רגע(int מצב_ערך);
    public static native void 직렬쓰기(int ערך);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int מעבד_הרשאה_רמה();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int אנכי_עמדה, int 색);
    public static native void רווח_מעבד();
    public static native int ליצור_משימה(int מדד);
    public static native int משימה_מצב(int מדד);
    public static native void עצירה(int מצב_ערך);
    public static native int 씨플러스시험();
    public static native int להפעיל_משתמש_תוכנית(int מדד);
    public static native int שיק_משתמש_תוכנית();
    public static native int 인수준비(int 개수);
    public static native int לבצע_משתמש_קובץ();
    public static native int 리눅스파일실행();
    public static native int ארגומנט_בית(int מדד, int מיקום, int ערך);
    public static native int מסוף(int פעולה);
    public static native int פקד_משתמש_תוכנית(int פעולה);
    public static native void 입출력전환(int פעולה);
    public static native int העברת_קבצים_שירות(int פעולה);
    public static native int רשת_מצב(int ערך_ערך, int מדד);
    public static native int רשת_הגדרות(int פעולה, int למען, int מסיכה_ערך, int שער_ערך);
    public static native int שלח_תגובה(int למען, int סדר_ערך);
    public static native int 응답읽기(int ערך_ערך);
    public static native int שאילתה_מערכת(int ערך_ערך, int מדד);
    public static native void 전원끄기();
}
