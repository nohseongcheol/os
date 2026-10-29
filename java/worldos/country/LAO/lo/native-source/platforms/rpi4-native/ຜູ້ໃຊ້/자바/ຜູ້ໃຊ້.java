// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 ເຄື່ອງມື 전용 SVC ເຊື່ອມຕໍ່. 기존 x86 ເຄື່ອງມື 원문을 함께 빌드한다. */
public final class ຜູ້ໃຊ້ {
    public static native int 파일서술자열기(int[] ຊື່, int ການຕັ້ງຄ່າ);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int ຄ່າ);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] ຊື່, int[] ຂໍ້ມູນ);
    public static native int ຂຽນ_ຟາຍ(int[] ຊື່, int[] ຂໍ້ມູນ, int ຄວາມຍາວ_ຄ່າ);
    public static native int ຂຽນ(String ຂໍ້ຄວາມ);
    public static native int ຂຽນ_ຕົວອັກສອນ_ຄ່າ(int ຄ່າ);
    public static native int 인수개수();
    public static native String 인수(int ດັດຊະນີ);
    public static native int 도구번호();
    public static native int 화면연결(int ຄໍາສັ່ງ, int ດັດຊະນີ, int 가, int 나, int 다, int 라);
    public static native int 화면글(int ດັດຊະນີ, int[] ຂໍ້ຄວາມ, int ຄວາມຍາວ_ຄ່າ);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int ສະຕຣີມ_ຄວບຄຸມ(int ຄໍາສັ່ງ, int 서술자, int ຄ່າ);
    public static native int ເຊື່ອມຕໍ່_ສະຕຣີມ(int 서술자, int ອີເມວ, int ຜອດ_ຄ່າ);
    public static native int ສ້າງ_ເຄືອຂ່າຍ(int ຜອດ_ຄ່າ);
    public static native int ສົ່ງ_ເຄືອຂ່າຍ(int 서술자, int ອີເມວ, int ຜອດ_ຄ່າ, int[] ຂໍ້ມູນ, int ຄວາມຍາວ_ຄ່າ);
    public static native int 통신받기(int 서술자, int[] ຂໍ້ມູນ, int ຄວາມຍາວ_ຄ່າ);
    public static native int ເຄືອຂ່າຍ_ຜອດ(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int ລວງຕັ້ງ_ຈັດຕໍາແຫນ່ງ, int 폭, int 높이, int 색);
}
