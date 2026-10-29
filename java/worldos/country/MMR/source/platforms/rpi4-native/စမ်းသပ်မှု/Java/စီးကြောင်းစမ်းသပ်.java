// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class စီးကြောင်းစမ်းသပ် {
    public static void main(String[] args) throws Exception {
        ServerSocket ဝန်ဆောင်စက်တန်ဖိုး = new ServerSocket(9250);
        Socket ဧည့်သည်တန်ဖိုး = new Socket("localhost", 9250);
        Socket ချိတ်ဆက် = ဝန်ဆောင်စက်တန်ဖိုး.accept();
        if (ချိတ်ဆက်.getPort() != ဧည့်သည်တန်ဖိုး.getLocalPort() || ဧည့်သည်တန်ဖိုး.getPort() != ချိတ်ဆက်.getLocalPort()) throw new RuntimeException("ဆက်သွယ်ပေါက်တန်ဖိုး 불일치");
        byte[] ဒေတာစာ = "한글 စီးကြောင်းတန်ဖိုး".getBytes("UTF-8");
        ဧည့်သည်တန်ဖိုး.getOutputStream().write(ဒေတာစာ);
        byte[] ရရှိအချက် = new byte[100];
        int အလျား = ချိတ်ဆက်.getInputStream().read(ရရှိအချက်, 0, ရရှိအချက်.length);
        System.out.println(အလျား == ဒေတာစာ.length);
        for (int i = 0; i < အလျား; i++) if (ရရှိအချက်[i] != ဒေတာစာ[i]) throw new RuntimeException("အကြောင်းအရာတန်ဖိုး 불일치");
        ချိတ်ဆက်.getOutputStream().write(42);
        System.out.println(ဧည့်သည်တန်ဖိုး.getInputStream().read());
        ဧည့်သည်တန်ဖိုး.close();
        System.out.println(ချိတ်ဆက်.getInputStream().read());
        ချိတ်ဆက်.close(); ဝန်ဆောင်စက်တန်ဖိုး.close();
        ServerSocket အလွတ်ဝန်ဆောင်စက် = new ServerSocket(9250);
        အလွတ်ဝန်ဆောင်စက်.setSoTimeout(10);
        try { အလွတ်ဝန်ဆောင်စက်.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("အချိန်တန်ဖိုး ကန့်သတ်ချက်တန်ဖိုး"); }
        အလွတ်ဝန်ဆောင်စက်.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
