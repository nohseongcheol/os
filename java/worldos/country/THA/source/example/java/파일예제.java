// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 파일예제 {
    public static void เรียกใช้งาน() throws ไทย.เอง.รับเข้า_ส่งออก_ข้อยกเว้น {
        ไทย.เอง.แฟ้ม.เขียน("java.txt", "JAVA แฟ้ม: ไทย 😀\n");
        ไทย.เอง.ข้อความออก.เขียน(ไทย.เอง.แฟ้ม.อ่าน("java.txt"));
    }
}
