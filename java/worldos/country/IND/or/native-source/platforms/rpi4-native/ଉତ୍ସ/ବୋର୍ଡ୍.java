// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 ମେସିନ୍ 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class ବୋର୍ଡ୍ {
    public static native int 표시화소읽기(int 가로, int ଅନୁଲମ୍ବ_ସ୍ଥିତି);
    public static native void ଲିଖନ_ଦେଖାଇବା_ପିକ୍ସେଲ୍(int 가로, int ଅନୁଲମ୍ବ_ସ୍ଥିତି, int 색);
    public static native int ସେଡୋଇଂ(int 종류, int କାମ);
    public static native void ଶେଷ_କରନ୍ତୁ_ଦୂରବର୍ତ୍ତୀ_ନିର୍ଦ୍ଦେଶ(int ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1);
    public static native void ଦୂରବର୍ତ୍ତୀ_ଅପେକ୍ଷା(int ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1);
    public static native void 직렬쓰기(int ମୂଲ୍ୟ);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int ସଂସାଧକ_ଅନୁମତି_ସ୍ତର();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int ଅନୁଲମ୍ବ_ସ୍ଥିତି, int 색);
    public static native void ରଦ୍ଧ_ହୋଇଛି_ସଂସାଧକ();
    public static native int ସୃଷ୍ଟି_ଟାସ୍କ(int ଅନୁକ୍ରମଣିକା);
    public static native int ଟାସ୍କ_ସ୍ଥିତି(int ଅନୁକ୍ରମଣିକା);
    public static native void ଅଟକାନ୍ତୁ(int ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1);
    public static native int 씨플러스시험();
    public static native int ରନ୍_ଉପଭୋକ୍ତା_ଅନୁପ୍ରୟୋଗ(int ଅନୁକ୍ରମଣିକା);
    public static native int ପରୀକ୍ଷିତ_ଉପଭୋକ୍ତା_ଅନୁପ୍ରୟୋଗ();
    public static native int 인수준비(int 개수);
    public static native int ନିର୍ବାହ_କରିବା_ଉପଭୋକ୍ତା_ଫାଇଲ୍();
    public static native int 리눅스파일실행();
    public static native int ଯୁକ୍ତି_ବାଇଟ୍(int ଅନୁକ୍ରମଣିକା, int ଅବସ୍ଥାନ, int ମୂଲ୍ୟ);
    public static native int ଟର୍ମିନାଲ(int କାମ);
    public static native int ନିୟନ୍ତ୍ରଣ_ଉପଭୋକ୍ତା_ଅନୁପ୍ରୟୋଗ(int କାମ);
    public static native void 입출력전환(int କାମ);
    public static native int ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସେବା(int କାମ);
    public static native int ନେଟ୍_ୱାର୍କ୍_ସ୍ଥିତି(int ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ, int ଅନୁକ୍ରମଣିକା);
    public static native int ନେଟ୍_ୱାର୍କ୍_ସେଟିଂସ୍(int କାମ, int ଠିକଣା, int ମାସ୍କ_ମୂଲ୍ୟ, int ପ୍ରବେଶ_ପଥ_ମୂଲ୍ୟ);
    public static native int 응답보내기(int ଠିକଣା, int କ୍ରମ_ମୂଲ୍ୟ);
    public static native int 응답읽기(int ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ);
    public static native int ଜିଜ୍ଞାସା_ସିଷ୍ଟମ(int ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ, int ଅନୁକ୍ରମଣିକା);
    public static native void 전원끄기();
}
