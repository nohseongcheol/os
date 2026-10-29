// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Hong_Kong_SAR_China.JHkgOS.interrupt;

@FunctionalInterface
public interface InterruptHandler {
    int processValueEntry(int savedStackAddress);
}

