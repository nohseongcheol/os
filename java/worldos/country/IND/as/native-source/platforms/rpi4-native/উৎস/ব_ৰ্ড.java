// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 মেচিন 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class ব_ৰ্ড {
    public static native int 표시화소읽기(int 가로, int উলম্ব_স্থান_সলনি_কৰক);
    public static native void লিখক_প্রদর্শন_পিক্সেল(int 가로, int উলম্ব_স্থান_সলনি_কৰক, int 색);
    public static native int ছাঁয়াকৰণ(int 종류, int কাৰ্য্য);
    public static native void অন্ত_কৰক_দূৰবৰ্তী_আদেশ(int অৱস্থা_মান);
    public static native void 원격대기(int অৱস্থা_মান);
    public static native void 직렬쓰기(int মান);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int প্ৰচেছৰ_অনুমতি_স্তৰ();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int উলম্ব_স্থান_সলনি_কৰক, int 색);
    public static native void নিলম্বিত_প্ৰচেছৰ();
    public static native int ক্ৰিয়েট_কার্য্য(int ইনডেক্স);
    public static native int কার্য্য_অৱস্থা(int ইনডেক্স);
    public static native void বন্ধ_কৰক_2(int অৱস্থা_মান);
    public static native int 씨플러스시험();
    public static native int চলন_ব্যৱহাৰকৰ্তা_এপ্প্(int ইনডেক্স);
    public static native int পৰীক্ষণ_ব্যৱহাৰকৰ্তা_এপ্প্();
    public static native int 인수준비(int 개수);
    public static native int নিষ্পাদন_ব্যৱহাৰকৰ্তা_ফাইল();
    public static native int 리눅스파일실행();
    public static native int যুক্তি_বাইট(int ইনডেক্স, int অৱস্থান, int মান);
    public static native int টাৰ্মিনেল(int কাৰ্য্য);
    public static native int নিয়ন্ত্রণ_ব্যৱহাৰকৰ্তা_এপ্প্(int কাৰ্য্য);
    public static native void 입출력전환(int কাৰ্য্য);
    public static native int ফাইল_স্থানান্তৰণ_সেৱা(int কাৰ্য্য);
    public static native int নেটৱৰ্ক_অৱস্থা(int প্রবিষ্ট_মান, int ইনডেক্স);
    public static native int নেটৱৰ্ক_ছেটিংছ(int কাৰ্য্য, int ঠিকনা, int মাস্ক_মান, int গেটৱে_মান);
    public static native int 응답보내기(int ঠিকনা, int ক্ৰম_মান);
    public static native int 응답읽기(int প্রবিষ্ট_মান);
    public static native int কুৱেৰী_ছিষ্টেম(int প্রবিষ্ট_মান, int ইনডেক্স);
    public static native void 전원끄기();
}
