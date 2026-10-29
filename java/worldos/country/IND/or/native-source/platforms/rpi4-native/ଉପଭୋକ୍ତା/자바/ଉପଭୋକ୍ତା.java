// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 ଉପକରଣସମୂହ 전용 SVC ସଂଯୋଗ_କରନ୍ତୁ. 기존 x86 ଉପକରଣସମୂହ 원문을 함께 빌드한다. */
public final class ଉପଭୋକ୍ତା {
    public static native int 파일서술자열기(int[] ନାମ, int ବିନ୍ଯାସ);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int ମୂଲ୍ୟ);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] ନାମ, int[] ଡାଟା);
    public static native int ଲିଖନ_ଫାଇଲ୍(int[] ନାମ, int[] ଡାଟା, int ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ);
    public static native int ଲେଖନ୍ତୁ(String ପାଠ୍ଯ);
    public static native int ଲିଖନ_ବର୍ଣ୍ଣ_ମୂଲ୍ୟ(int ମୂଲ୍ୟ);
    public static native int 인수개수();
    public static native String 인수(int ଅନୁକ୍ରମଣିକା);
    public static native int 도구번호();
    public static native int 화면연결(int କାମ, int ଅନୁକ୍ରମଣିକା, int 가, int 나, int 다, int 라);
    public static native int 화면글(int ଅନୁକ୍ରମଣିକା, int[] ପାଠ୍ଯ, int ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int ଷ୍ଟ୍ରିମ୍_ନିୟନ୍ତ୍ରଣ(int କାମ, int 서술자, int ମୂଲ୍ୟ);
    public static native int ସଂଯୋଗ_ଷ୍ଟ୍ରିମ୍(int 서술자, int ଠିକଣା, int ପୋର୍ଟ_ମୂଲ୍ୟ);
    public static native int ଖୋଲିବା_ନେଟ୍_ୱାର୍କ୍(int ପୋର୍ଟ_ମୂଲ୍ୟ);
    public static native int ପଠାନ୍ତୁ_ନେଟ୍_ୱାର୍କ୍(int 서술자, int ଠିକଣା, int ପୋର୍ଟ_ମୂଲ୍ୟ, int[] ଡାଟା, int ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ);
    public static native int 통신받기(int 서술자, int[] ଡାଟା, int ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ);
    public static native int ନେଟ୍_ୱାର୍କ୍_ପୋର୍ଟ(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int ଅନୁଲମ୍ବ_ସ୍ଥିତି, int 폭, int 높이, int 색);
}
