// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Micronesia.JFsmOS.Kernel;

/** The sole boundary between the Java-managed kernel and CPU-specific code. */
public interface hardwareValue {
    void serialOutput(String contentValue);

    int readPortByte(int hardwarePortNumber);

    void writePortByte(int hardwarePortNumber, int value);

    void haltCpu();
}

