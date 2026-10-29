// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.FileInputStream;
import java.io.FileOutputStream;
public class FileDemo {
    public static void main(String[] args) throws Exception {
        FileOutputStream output = new FileOutputStream("java.txt");
        output.write(65);
        output.write(255);
        output.close();
        FileOutputStream append = new FileOutputStream("java.txt", true);
        append.write(66);
        append.close();
        FileInputStream input = new FileInputStream("java.txt");
        System.out.println(input.read());
        System.out.println(input.read());
        System.out.println(input.read());
        System.out.println(input.read());
        input.close();
        input.close();
        System.out.println("JAVA FILE IO PASS");
    }
}
