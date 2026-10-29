// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros អ្នកប្រើ ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class អ្នកប្រើ {
    public static native int 파일서술자열기(int[] ឯកសារ_ការបញ្ចូល_ឈ្មោះ, int បើក_ការកំណត់);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int បៃ_តំលៃ);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] ឈ្មោះ, int[] ទិន្នន័យ);
    public static native int សរសេរ_តួអក្សរ_តំលៃ(int 문자);
    public static native int សរសេរ_ឯកសារ(int[] ឈ្មោះ, int[] ទិន្នន័យ, int ប្រវែង_តំលៃ);
    public static native int សរសេរ(String មាតិកា_តំលៃ);
    public static native int 인수개수();
    public static native String អាគុយម៉ង់(int សន្ទស្សន៏);
    public static native int 실행권한();
    public static native int បើក_ណិតវឺក(int ក្នុងតំបន់_ច្រក);
    public static native int ផ្ញើ_ទិន្នន័យ(int ការកាន់កាប់_តំលៃ, int អ៊ីម៉ែល, int ទិសដៅ_ច្រក, int[] ទិន្នន័យ, int ប្រវែង_តំលៃ);
    public static native int 자료받기(int ការកាន់កាប់_តំលៃ, int[] ទិន្នន័យ, int 제한밀리초);
    public static native int បិទ_ណិតវឺក(int ការកាន់កាប់_តំលៃ);
    public static native int 내주소();
    public static native int 보낸주소(int ការកាន់កាប់_តំលៃ);
    public static native int 보낸창구(int ការកាន់កាប់_តំលៃ);
}
