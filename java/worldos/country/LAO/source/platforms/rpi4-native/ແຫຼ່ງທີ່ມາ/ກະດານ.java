// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 ເຄື່ອງຈັກ 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class ກະດານ {
    public static native int 표시화소읽기(int 가로, int ລວງຕັ້ງ_ຈັດຕໍາແຫນ່ງ);
    public static native void ຂຽນ_ສະແດງຜົນ_ເປ_ລ(int 가로, int ລວງຕັ້ງ_ຈັດຕໍາແຫນ່ງ, int 색);
    public static native int ທາງ_ໄກ_ຄວບຄຸມ(int 종류, int ຄໍາສັ່ງ);
    public static native void ຈົບ_ທາງ_ໄກ_ຄໍາສັ່ງ(int ສະຖານະ_ຄ່າ);
    public static native void ທາງ_ໄກ_ລໍຖ້າ(int ສະຖານະ_ຄ່າ);
    public static native void 직렬쓰기(int ຄ່າ);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int ຊີພີຢູ_ການອະນຸຍາດ_ລະດັບ();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int ລວງຕັ້ງ_ຈັດຕໍາແຫນ່ງ, int 색);
    public static native void ລະງັບ_ຊີພີຢູ();
    public static native int ສ້າງ_ຫນ້າວຽກ(int ດັດຊະນີ);
    public static native int ຫນ້າວຽກ_ສະຖານະ(int ດັດຊະນີ);
    public static native void ຢຸດ(int ສະຖານະ_ຄ່າ);
    public static native int 씨플러스시험();
    public static native int ແລ່ນ_ຜູ້ໃຊ້_ແອັບ(int ດັດຊະນີ);
    public static native int ເຊັກເງິນ_ຜູ້ໃຊ້_ແອັບ();
    public static native int 인수준비(int 개수);
    public static native int ປະ_ຕິ_ບັດ_ຜູ້ໃຊ້_ຟາຍ();
    public static native int 리눅스파일실행();
    public static native int ຂໍ້ພິສູດ_ໄບ(int ດັດຊະນີ, int ຈັດຕໍາແຫນ່ງ, int ຄ່າ);
    public static native int ເທີມີນໍ(int ຄໍາສັ່ງ);
    public static native int ຄວບຄຸມ_ຜູ້ໃຊ້_ແອັບ(int ຄໍາສັ່ງ);
    public static native void 입출력전환(int ຄໍາສັ່ງ);
    public static native int ຟາຍ_ໂອນ_ບໍລິການ(int ຄໍາສັ່ງ);
    public static native int ເຄືອຂ່າຍ_ສະຖານະ(int ເຂົ້າໃນ_ຄ່າ, int ດັດຊະນີ);
    public static native int ເຄືອຂ່າຍ_ການຕັ້ງຄ່າ(int ຄໍາສັ່ງ, int ອີເມວ, int ຫນ້າກາກ_ຄ່າ, int ເກດເວ_ຄ່າ);
    public static native int 응답보내기(int ອີເມວ, int ລໍາດັບ_ຄ່າ);
    public static native int 응답읽기(int ເຂົ້າໃນ_ຄ່າ);
    public static native int ຄິວຣີ_ລະບົບ(int ເຂົ້າໃນ_ຄ່າ, int ດັດຊະນີ);
    public static native void 전원끄기();
}
