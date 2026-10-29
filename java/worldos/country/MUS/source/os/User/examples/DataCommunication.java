// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class DataCommunication {
    static int digitValue(String text) {
        if (text == null || text.length() == 0) return -1;
        int result = 0;
        for (int index = 0; index < text.length(); index++) {
            int value = text.charAt(index) - '0';
            if (value < 0 || value > 9 || result > 6553) return -1;
            result = result * 10 + value;
            if (result > 65535) return -1;
        }
        return result;
    }
    static int address(String text) {
        if (text == null) return 0;
        int value = 0, result = 0, subpartValue = 0, digits = 0;
        for (int index = 0; index <= text.length(); index++) {
            int Characters = index == text.length() ? '.' : text.charAt(index);
            if (Characters == '.') {
                if (digits == 0 || subpartValue == 4) return 0;
                result = (result << 8) | value; subpartValue++; value = 0; digits = 0;
            } else {
                if (Characters < '0' || Characters > '9') return 0;
                value = value * 10 + Characters - '0';
                if (++digits > 3 || value > 255) return 0;
            }
        }
        return subpartValue == 4 ? result : 0;
    }
    public static int run() {
        if (User.argumentsCount() != 3) { User.write("Usage: run udp IP PORT TEXT\n"); return 2; }
        int address = address(User.arguments(0)), portValue = digitValue(User.arguments(1));
        String contentValue = User.arguments(2);
        if (address == 0 || portValue < 1 || contentValue.length() > 1024) { User.write("Bad destination\n"); return 2; }
        int handleValue = User.openNetwork(0);
        if (handleValue < 0) { User.write("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] data = new int[1024];
        for (int index = 0; index < contentValue.length(); index++) data[index] = contentValue.charAt(index);
        if (User.sendData(handleValue, address, portValue, data, contentValue.length()) < 0) {
            User.write("UDP SEND FAILED\n"); User.closeNetwork(handleValue); return 4;
        }
        User.write("UDP SENT\n");
        int receivedLength = User.receiveData(handleValue, data, 1500);
        boolean equalText = receivedLength == contentValue.length() && User.sentAddress(handleValue) == address && User.sentPort(handleValue) == portValue;
        if (equalText) for (int index = 0; index < receivedLength; index++) if (data[index] != contentValue.charAt(index)) equalText = false;
        User.closeNetwork(handleValue);
        if (receivedLength < 0) { User.write("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        User.write(equalText ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return equalText ? 0 : 6;
    }
}
