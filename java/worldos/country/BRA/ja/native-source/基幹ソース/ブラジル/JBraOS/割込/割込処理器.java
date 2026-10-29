// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ブラジル.JBraOS.割込;

@FunctionalInterface
public interface 割込処理器 {
    int プロセス値入口(int 保存済みスタック番地);
}

