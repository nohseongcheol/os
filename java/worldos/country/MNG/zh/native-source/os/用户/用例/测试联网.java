// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 测试联网 {
    public static int 运行() {
        int 首位序数 = 用户.打开网络(45000);
        if (首位序数 < 0) { 用户.写入("NETWORK UNAVAILABLE\n"); return 3; }
        int[] 数据 = new int[8];
        boolean 通过值 = 用户.打开网络(45000) == -98
            && 用户.接收数据(首位序数, 数据, 0) == -11
            && 用户.接收数据(首位序数, 数据, 50) == -110
            && 用户.接收数据(首位序数, 数据, 3000) == -22
            && 用户.发送数据(首位序数, 0x0a000202, 9, 数据, 9) == -90
            && 用户.接收数据(首位序数, null, 0) == -14
            && 用户.关闭网络(首位序数) == 0 && 用户.关闭网络(首位序数) == -9;
        用户.写入(通过值 ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return 通过值 ? 0 : 1;
    }
}
