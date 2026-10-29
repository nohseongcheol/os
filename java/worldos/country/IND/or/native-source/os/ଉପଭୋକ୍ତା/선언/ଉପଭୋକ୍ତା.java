// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros ଉପଭୋକ୍ତା ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class ଉପଭୋକ୍ତା {
    public static native int 파일서술자열기(int[] ଫାଇଲ୍_ଏଣ୍ଟ୍ରି_ନାମ, int ଖୋଲିବା_ସେଟିଂସ୍);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int ବାଇଟ୍_ମୂଲ୍ୟ);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] ନାମ, int[] ଡାଟା);
    public static native int ଲିଖନ_ବର୍ଣ୍ଣ_ମୂଲ୍ୟ(int 문자);
    public static native int ଲିଖନ_ଫାଇଲ୍(int[] ନାମ, int[] ଡାଟା, int ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ);
    public static native int ଲେଖନ୍ତୁ(String ବିଷୟ_ମୂଲ୍ୟ);
    public static native int 인수개수();
    public static native String 인수(int ଅନୁକ୍ରମଣିକା);
    public static native int 실행권한();
    public static native int ଖୋଲିବା_ନେଟ୍_ୱାର୍କ୍(int ସ୍ଥାନୀୟ_ପୋର୍ଟ);
    public static native int ପଠାନ୍ତୁ_ଡାଟା(int ହାଣ୍ଡେଲ୍_ମୂଲ୍ୟ, int ଠିକଣା, int ଲକ୍ଷସ୍ଥଳ_ପୋର୍ଟ, int[] ଡାଟା, int ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ);
    public static native int 자료받기(int ହାଣ୍ଡେଲ୍_ମୂଲ୍ୟ, int[] ଡାଟା, int 제한밀리초);
    public static native int ବନ୍ଦ_ନେଟ୍_ୱାର୍କ୍(int ହାଣ୍ଡେଲ୍_ମୂଲ୍ୟ);
    public static native int 내주소();
    public static native int 보낸주소(int ହାଣ୍ଡେଲ୍_ମୂଲ୍ୟ);
    public static native int 보낸창구(int ହାଣ୍ଡେଲ୍_ମୂଲ୍ୟ);
}
