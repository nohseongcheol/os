// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 კომპიუტერი 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class დაფა {
    public static native int 표시화소읽기(int 가로, int ვერტიკალური_პოზიცია);
    public static native void ჩაწერა_ჩვენება_პიქსელი(int 가로, int ვერტიკალური_პოზიცია, int 색);
    public static native int ჩრდილური_მართვა(int 종류, int ქმედება);
    public static native void დასასრული_დისტანციური_ბრძანება(int სტატუსი_მნიშვნელობა);
    public static native void დისტანციური_მოლოდინი(int სტატუსი_მნიშვნელობა);
    public static native void 직렬쓰기(int მნიშვნელობა);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int პროცესორი_ნებართვა_დონე();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int ვერტიკალური_პოზიცია, int 색);
    public static native void შეჩერება_პროცესორი();
    public static native int შექმნა_დავალება(int ინდექსი);
    public static native int დავალება_სტატუსი(int ინდექსი);
    public static native void შეჩერება(int სტატუსი_მნიშვნელობა);
    public static native int 씨플러스시험();
    public static native int სერია_მომხმარებელი_აპი(int ინდექსი);
    public static native int შემოწმება_მომხმარებელი_აპი();
    public static native int 인수준비(int 개수);
    public static native int შესრულება_მომხმარებელი_ფაილი();
    public static native int 리눅스파일실행();
    public static native int არგუმენტი_ბაიტი(int ინდექსი, int პოზიცია, int მნიშვნელობა);
    public static native int ტერმინალი(int ქმედება);
    public static native int მართვა_მომხმარებელი_აპი(int ქმედება);
    public static native void 입출력전환(int ქმედება);
    public static native int ფაილი_გადატანა_სერვისი(int ქმედება);
    public static native int ქსელი_სტატუსი(int შენატანი_მნიშვნელობა, int ინდექსი);
    public static native int ქსელი_პარამეტრები(int ქმედება, int მისამართი, int ნიღაბი_მნიშვნელობა, int კარიბჭე_მნიშვნელობა);
    public static native int გაგზავნა_პასუხი(int მისამართი, int დახარისხების_თანმიმდევრობა_მნიშვნელობა);
    public static native int 응답읽기(int შენატანი_მნიშვნელობა);
    public static native int მოთხოვნა_სისტემა(int შენატანი_მნიშვნელობა, int ინდექსი);
    public static native void 전원끄기();
}
