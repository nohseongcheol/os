// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 ማሽን 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class ቦርድ {
    public static native int 표시화소읽기(int 가로, int ቋሚ_በቦታ_አስቀመጠ);
    public static native void ጻፍ_ማሳያ_ፒክስል(int 가로, int ቋሚ_በቦታ_አስቀመጠ, int 색);
    public static native int ማጥላት(int 종류, int ተግባር);
    public static native void ጨርስ_የሩቅ_ትእዛዝ(int ዞን_እሴት);
    public static native void የሩቅ_መጠበቅ(int ዞን_እሴት);
    public static native void 직렬쓰기(int እሴት);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int ፕሮሰሰር_ፈቃድ_ደረጃ();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int ቋሚ_በቦታ_አስቀመጠ, int 색);
    public static native void አግድ_አሂያጅ();
    public static native int ፍጠር_ተግባር(int መረጃ_ጠቆመ);
    public static native int ተግባር_ዞን(int መረጃ_ጠቆመ);
    public static native void ማስቆሚያ(int ዞን_እሴት);
    public static native int 씨플러스시험();
    public static native int አሂድ_ተጠቃሚ_ፕሮግራም(int መረጃ_ጠቆመ);
    public static native int ቼክ_ተጠቃሚ_ፕሮግራም();
    public static native int 인수준비(int 개수);
    public static native int ፈጽም_ተጠቃሚ_ፋይል();
    public static native int 리눅스파일실행();
    public static native int ነጋሪ_እሴት_ባይት(int መረጃ_ጠቆመ, int አካባቢ, int እሴት);
    public static native int ተርሚናል(int ተግባር);
    public static native int ቁጥጥር_ተጠቃሚ_ፕሮግራም(int ተግባር);
    public static native void 입출력전환(int ተግባር);
    public static native int ፋይል_ትልልፍ_አገልግሎት(int ተግባር);
    public static native int መረብ_ዞን(int ምዝግብ_እሴት, int መረጃ_ጠቆመ);
    public static native int መረብ_ቅንብሮች(int ተግባር, int አድራሻ, int ጭንብል_እሴት, int አግባቢ_ፍኖት_እሴት);
    public static native int 응답보내기(int አድራሻ, int ቅደም_ተከተል_እሴት);
    public static native int 응답읽기(int ምዝግብ_እሴት);
    public static native int መጠይቅ_ስርዓት(int ምዝግብ_እሴት, int መረጃ_ጠቆመ);
    public static native void 전원끄기();
}
