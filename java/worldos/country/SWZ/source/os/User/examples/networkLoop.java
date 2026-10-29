// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Tests real RTL8139 receive-ring wraparound with maximum-sized and odd-length datagrams. */
public final class networkLoop {
    public static int run() {
        if (User.argumentsCount() != 1) { User.write("Usage: run stress PORT\n"); return 2; }
        String text = User.arguments(0);
        int portValue = 0;
        for (int index = 0; index < text.length(); index++) {
            if (text.charAt(index) < '0' || text.charAt(index) > '9' || portValue > 6553) return 2;
            portValue = portValue * 10 + text.charAt(index) - '0';
        }
        if (portValue < 1 || portValue > 65535) return 2;
        int handleValue = User.openNetwork(0);
        if (handleValue < 0) return 3;
        int[] data = new int[1024];
        for (int iterationOrdinal = 0; iterationOrdinal < 24; iterationOrdinal++) {
            int lengthValue = 1024 - (iterationOrdinal & 1);
            for (int index = 0; index < lengthValue; index++) data[index] = (index + iterationOrdinal) & 255;
            if (User.sendData(handleValue, 0x0a000202, portValue, data, lengthValue) != lengthValue) return 4;
            if (User.receiveData(handleValue, data, 300) != lengthValue) return 5;
            for (int index = 0; index < lengthValue; index++) if (data[index] != ((index + iterationOrdinal) & 255)) return 6;
        }
        User.closeNetwork(handleValue);
        User.write("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
