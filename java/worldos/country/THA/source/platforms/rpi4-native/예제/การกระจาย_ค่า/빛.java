// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 빛 {
    public static void main(String[] อาร์กิวเมนต์) throws Exception {
        int 합 = 0;
        int หมายเลข = 1;
        while (หมายเลข <= 10) {
            합 = 합 + หมายเลข;
            หมายเลข = หมายเลข + 1;
        }
        ไทย.เอง.ข้อความออก.수쓰기(합);
        ไทย.เอง.แฟ้ม.เขียน("aot.txt", "한글 AOT แฟ้ม 😀");
        ไทย.เอง.ข้อความออก.줄쓰기(ไทย.เอง.แฟ้ม.อ่าน("aot.txt"));
    }
}
