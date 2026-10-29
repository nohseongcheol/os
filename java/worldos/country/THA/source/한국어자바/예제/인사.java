// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import ไทย.자바.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class 인사 {
    public static void main(String[] อาร์กิวเมนต์) throws Exception {
        String ข้อความ = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path เส้นทาง = แฟ้ม.เส้นทาง("인사.txt");
        แฟ้ม.เขียน(เส้นทาง, ข้อความ);
        System.out.println(แฟ้ม.อ่าน(เส้นทาง));
        Thread งาน_ค่า = 작업.เรียกใช้งาน("인사 작업", () -> System.out.println("작업 เธรด_ค่า ดําเนินการ_คําสั่ง"));
        작업.기다리기(งาน_ค่า);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 เทอร์มินัล 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            화면.나중에(() -> 화면.หน้าต่าง("다국어 인사", new JLabel(ข้อความ), 700, 160));
        }
    }
}
