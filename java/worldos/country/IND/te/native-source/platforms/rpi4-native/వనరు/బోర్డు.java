// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 యంత్రం 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class బోర్డు {
    public static native int 표시화소읽기(int 가로, int నిలువు_స్థాయి);
    public static native void వ్రాయి_ప్రదర్శన_పెల్(int 가로, int నిలువు_స్థాయి, int 색);
    public static native int వ్యవహిత_నియంత్రణ(int 종류, int చర్య);
    public static native void ముగించు_రిమోట్_ఆదేశం(int స్థితి_మూల్యం);
    public static native void రిమోట్_వేచియుండు(int స్థితి_మూల్యం);
    public static native void 직렬쓰기(int మూల్యం);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int ప్రాసెసర్_అనుమతి_స్థాయి();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int నిలువు_స్థాయి, int 색);
    public static native void తాత్కాలికంగా_నిలిపివేయి_ప్రాసెసర్();
    public static native int క్రియేట్_విధి(int సూచీ);
    public static native int విధి_స్థితి(int సూచీ);
    public static native void నిలిపి_వేయు(int స్థితి_మూల్యం);
    public static native int 씨플러스시험();
    public static native int అమలు_చెయ్_వినియోగదారు_అనువర్తనం(int సూచీ);
    public static native int తనిఖీ_వినియోగదారు_అనువర్తనం();
    public static native int 인수준비(int 개수);
    public static native int అమలు_చేయి_వినియోగదారు_ఫైలు();
    public static native int 리눅스파일실행();
    public static native int కారకం_బైట్(int సూచీ, int స్థానము, int మూల్యం);
    public static native int టెర్మినల్(int చర్య);
    public static native int నియంత్రణ_వినియోగదారు_అనువర్తనం(int చర్య);
    public static native void 입출력전환(int చర్య);
    public static native int ఫైలు_బదిలీ_సేవ(int చర్య);
    public static native int నెట్_వర్క్_లభ్యత(int ప్రవేశం_మూల్యం, int సూచీ);
    public static native int నెట్_వర్క్_సెట్టింగ్_లు(int చర్య, int ఇమెయిల్, int నిర్ధారకం_మూల్యం, int ప్రవేశద్వారం_మూల్యం);
    public static native int 응답보내기(int ఇమెయిల్, int క్రమం_మూల్యం);
    public static native int 응답읽기(int ప్రవేశం_మూల్యం);
    public static native int ప్రశ్న_సిస్టం(int ప్రవేశం_మూల్యం, int సూచీ);
    public static native void 전원끄기();
}
