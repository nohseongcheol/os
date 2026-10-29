// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中国.JChnOS.中断;

@FunctionalInterface
public interface 中断处理程序 {
    int 进程值条目(int 已保存栈地址);
}

