// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 台灣.JTwnOS.中斷;

@FunctionalInterface
public interface 中斷處理程序 {
    int 程序值條目(int 已保存棧地址);
}

