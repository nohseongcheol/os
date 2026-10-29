// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros ຜູ້ໃຊ້ ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class ຜູ້ໃຊ້ {
    public static native int 파일서술자열기(int[] ຟາຍ_ເຂົ້າໃນ_ຊື່, int ສ້າງ_ການຕັ້ງຄ່າ);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int ໄບ_ຄ່າ);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] ຊື່, int[] ຂໍ້ມູນ);
    public static native int ຂຽນ_ຕົວອັກສອນ_ຄ່າ(int 문자);
    public static native int ຂຽນ_ຟາຍ(int[] ຊື່, int[] ຂໍ້ມູນ, int ຄວາມຍາວ_ຄ່າ);
    public static native int ຂຽນ(String ເນື້ອໃນ_ຄ່າ_cb0f2404);
    public static native int 인수개수();
    public static native String 인수(int ດັດຊະນີ);
    public static native int 실행권한();
    public static native int ສ້າງ_ເຄືອຂ່າຍ(int ໃນເຄື່ອງ_ຜອດ);
    public static native int ສົ່ງ_ຂໍ້ມູນ(int ຈັດ_ການ_ຄ່າ, int ອີເມວ, int ປາຍທາງ_ຜອດ, int[] ຂໍ້ມູນ, int ຄວາມຍາວ_ຄ່າ);
    public static native int 자료받기(int ຈັດ_ການ_ຄ່າ, int[] ຂໍ້ມູນ, int 제한밀리초);
    public static native int ປິດ_ເຄືອຂ່າຍ(int ຈັດ_ການ_ຄ່າ);
    public static native int 내주소();
    public static native int 보낸주소(int ຈັດ_ການ_ຄ່າ);
    public static native int 보낸창구(int ຈັດ_ການ_ຄ່າ);
}
