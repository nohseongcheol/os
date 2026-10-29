// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros მომხმარებელი ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class მომხმარებელი {
    public static native int 파일서술자열기(int[] ფაილი_შენატანი_სახელი, int გახსნა_პარამეტრები);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int ბაიტი_მნიშვნელობა);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] სახელი, int[] მონაცემები);
    public static native int ჩაწერა_სიმბოლო_მნიშვნელობა(int 문자);
    public static native int ჩაწერა_ფაილი(int[] სახელი, int[] მონაცემები, int სიგრძე_მნიშვნელობა);
    public static native int ჩაწერა(String შიგთავსი_მნიშვნელობა);
    public static native int 인수개수();
    public static native String 인수(int ინდექსი);
    public static native int 실행권한();
    public static native int გახსნა_ქსელი(int ლოკალური_პორტი);
    public static native int გაგზავნა_მონაცემები(int სახელური_მნიშვნელობა, int მისამართი, int მიმართულება_პორტი, int[] მონაცემები, int სიგრძე_მნიშვნელობა);
    public static native int 자료받기(int სახელური_მნიშვნელობა, int[] მონაცემები, int 제한밀리초);
    public static native int დახურვა_ქსელი(int სახელური_მნიშვნელობა);
    public static native int 내주소();
    public static native int 보낸주소(int სახელური_მნიშვნელობა);
    public static native int 보낸창구(int სახელური_მნიშვნელობა);
}
