// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 Computer 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class Board {
    public static native int 표시화소읽기(int 가로, int Vertikal_positionéieren);
    public static native void schreiwen_Bildschierm_Pel(int 가로, int Vertikal_positionéieren, int 색);
    public static native int Shadowing(int 종류, int Aktioun);
    public static native void bëennegen_extern_Befeel(int Status_VALUE);
    public static native void extern_Waart(int Status_VALUE);
    public static native void 직렬쓰기(int VALUE);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int CPU_Geneemegung_Niveau();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int Vertikal_positionéieren, int 색);
    public static native void YIELD_CPU();
    public static native int Create_To_do(int INDEX);
    public static native int To_do_Status(int INDEX);
    public static native void Stoppen(int Status_VALUE);
    public static native int 씨플러스시험();
    public static native int Laf_Benotzer_App(int INDEX);
    public static native int Scheck_Benotzer_App();
    public static native int 인수준비(int Element_COUNT);
    public static native int ausféieren_Benotzer_Fichier();
    public static native int 리눅스파일실행();
    public static native int Argument_Byte(int INDEX, int positionéieren, int VALUE);
    public static native int Terminal(int Aktioun);
    public static native int Kontroll_Benotzer_App(int Aktioun);
    public static native void 입출력전환(int Aktioun);
    public static native int Fichier_Transfer_Service(int Aktioun);
    public static native int Reseau_Status(int Agab_VALUE, int INDEX);
    public static native int Reseau_Astellungen(int Aktioun, int Adress, int Mask_VALUE, int Gateway_VALUE);
    public static native int 응답보내기(int Adress, int Reiefolleg_VALUE);
    public static native int 응답읽기(int Agab_VALUE);
    public static native int Requête_System(int Agab_VALUE, int INDEX);
    public static native void 전원끄기();
}
