// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket සේවාදායකය_අගය = new ServerSocket(9250);
        Socket අමුත්තා_අගය = new Socket("localhost", 9250);
        Socket සම්බන්ද_වන්න = සේවාදායකය_අගය.accept();
        if (සම්බන්ද_වන්න.getPort() != අමුත්තා_අගය.getLocalPort() || අමුත්තා_අගය.getPort() != සම්බන්ද_වන්න.getLocalPort()) throw new RuntimeException("තොට_අගය 불일치");
        byte[] 전문 = "한글 දහර_අගය".getBytes("UTF-8");
        අමුත්තා_අගය.getOutputStream().write(전문);
        byte[] 받은것 = new byte[100];
        int දිග_අගය = සම්බන්ද_වන්න.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(දිග_අගය == 전문.length);
        for (int i = 0; i < දිග_අගය; i++) if (받은것[i] != 전문[i]) throw new RuntimeException("අන්තර්ගතය_අගය 불일치");
        සම්බන්ද_වන්න.getOutputStream().write(42);
        System.out.println(අමුත්තා_අගය.getInputStream().read());
        අමුත්තා_අගය.close();
        System.out.println(සම්බන්ද_වන්න.getInputStream().read());
        සම්බන්ද_වන්න.close(); සේවාදායකය_අගය.close();
        ServerSocket ශූන්_ය_සේවාදායකය = new ServerSocket(9250);
        ශූන්_ය_සේවාදායකය.setSoTimeout(10);
        try { ශූන්_ය_සේවාදායකය.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("시간 제한"); }
        ශූන්_ය_සේවාදායකය.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
