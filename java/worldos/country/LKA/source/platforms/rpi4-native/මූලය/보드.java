// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 යන්ත්_රය 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class 보드 {
    public static native int 표시화소읽기(int 가로, int 세로);
    public static native void ලියන්න_සංදර්ශකය_පික්සලය(int 가로, int 세로, int 색);
    public static native int ඡායාකරණය(int 종류, int ක්_රීයාව);
    public static native void නිමා_කරන්න_දුරස්ථ_විධානය(int තත්වය_අගය);
    public static native void 원격대기(int තත්වය_අගය);
    public static native void 직렬쓰기(int අගය);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int සකසුව_අවසරය_මට්ටම();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int 세로, int 색);
    public static native void අත්හිටුවන්න_සකසුව();
    public static native int සාදන්න_කාර්යය(int සූචිය);
    public static native int කාර්යය_තත්වය(int සූචිය);
    public static native void නවතන්න(int තත්වය_අගය);
    public static native int 씨플러스시험();
    public static native int ධාවනය_කරන්න_පරිශීලක_යෙදු(int සූචිය);
    public static native int චෙක්පත_පරිශීලක_යෙදු();
    public static native int 인수준비(int 개수);
    public static native int ක්_රියාත්මක_කරන්න_පරිශීලක_ගොනුව();
    public static native int 리눅스파일실행();
    public static native int විස්තාරකය_බයිටය(int සූචිය, int පිහිටීම, int අගය);
    public static native int අග්_රය(int ක්_රීයාව);
    public static native int පාලකය_පරිශීලක_යෙදු(int ක්_රීයාව);
    public static native void 입출력전환(int ක්_රීයාව);
    public static native int ගොනුව_මාරුව_සේවාව(int ක්_රීයාව);
    public static native int ජාලය_තත්වය(int පිවිසුම_අගය, int සූචිය);
    public static native int ජාලය_පසුතල(int ක්_රීයාව, int යොමුව, int වසනය_අගය, int වාහල_අගය);
    public static native int 응답보내기(int යොමුව, int අනුපිළිවෙළ_අගය);
    public static native int 응답읽기(int පිවිසුම_අගය);
    public static native int විමසුම_පද්ධතිය(int පිවිසුම_අගය, int සූචිය);
    public static native void 전원끄기();
}
