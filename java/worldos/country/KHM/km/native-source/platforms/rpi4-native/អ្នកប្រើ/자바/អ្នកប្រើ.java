// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 ឧបករណ៍ 전용 SVC ភ្ជាប់. 기존 x86 ឧបករណ៍ 원문을 함께 빌드한다. */
public final class អ្នកប្រើ {
    public static native int 파일서술자열기(int[] ឈ្មោះ, int ការកំណត់);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int តំលៃ);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] ឈ្មោះ, int[] ទិន្នន័យ);
    public static native int សរសេរ_ឯកសារ(int[] ឈ្មោះ, int[] ទិន្នន័យ, int ប្រវែង_តំលៃ);
    public static native int សរសេរ(String អត្ថបទ);
    public static native int សរសេរ_តួអក្សរ_តំលៃ(int តំលៃ);
    public static native int 인수개수();
    public static native String អាគុយម៉ង់(int សន្ទស្សន៏);
    public static native int 도구번호();
    public static native int 화면연결(int អំពើ, int សន្ទស្សន៏, int 가, int 나, int 다, int 라);
    public static native int 화면글(int សន្ទស្សន៏, int[] អត្ថបទ, int ប្រវែង_តំលៃ);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int ស្ទ្រីម_អង្គបញ្ជា(int អំពើ, int 서술자, int តំលៃ);
    public static native int ភ្ជាប់_ស្ទ្រីម(int 서술자, int អ៊ីម៉ែល, int ច្រក_តំលៃ);
    public static native int បើក_ណិតវឺក(int ច្រក_តំលៃ);
    public static native int ផ្ញើ_ណិតវឺក(int 서술자, int អ៊ីម៉ែល, int ច្រក_តំលៃ, int[] ទិន្នន័យ, int ប្រវែង_តំលៃ);
    public static native int 통신받기(int 서술자, int[] ទិន្នន័យ, int ប្រវែង_តំលៃ);
    public static native int ណិតវឺក_ច្រក(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int បញ្ឈរ_កំណត់ទីតាំង, int 폭, int 높이, int 색);
}
