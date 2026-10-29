// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 ხელსაწყოები 전용 SVC დაკავშირება. 기존 x86 ხელსაწყოები 원문을 함께 빌드한다. */
public final class მომხმარებელი {
    public static native int 파일서술자열기(int[] სახელი, int პარამეტრები);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int მნიშვნელობა);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] სახელი, int[] მონაცემები);
    public static native int ჩაწერა_ფაილი(int[] სახელი, int[] მონაცემები, int სიგრძე_მნიშვნელობა);
    public static native int ჩაწერა(String ტექსტი);
    public static native int ჩაწერა_სიმბოლო_მნიშვნელობა(int მნიშვნელობა);
    public static native int 인수개수();
    public static native String 인수(int ინდექსი);
    public static native int 도구번호();
    public static native int 화면연결(int ქმედება, int ინდექსი, int 가, int 나, int 다, int 라);
    public static native int 화면글(int ინდექსი, int[] ტექსტი, int სიგრძე_მნიშვნელობა);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int ნაკადი_მართვა(int ქმედება, int 서술자, int მნიშვნელობა);
    public static native int დაკავშირება_ნაკადი(int 서술자, int მისამართი, int პორტი_მნიშვნელობა);
    public static native int გახსნა_ქსელი(int პორტი_მნიშვნელობა);
    public static native int გაგზავნა_ქსელი(int 서술자, int მისამართი, int პორტი_მნიშვნელობა, int[] მონაცემები, int სიგრძე_მნიშვნელობა);
    public static native int 통신받기(int 서술자, int[] მონაცემები, int სიგრძე_მნიშვნელობა);
    public static native int ქსელი_პორტი(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int ვერტიკალური_პოზიცია, int 폭, int 높이, int 색);
}
