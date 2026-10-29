// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import English.Native.Connection;
import English.Native.Arguments;
import English.Native.DatagramChannel;
import English.Native.Characters;
import English.Native.Output;
import English.Native.Checks;
import English.Native.InputStream;
import English.Native.InputOutputException;

public class NetworkExample {
    public static void run() throws InputOutputException {
        // Host: python3 tools/example_echo.py --tcp-port 9000 --udp-port 9001
        Connection connect = Connection.open("10.0.2.2", Characters.parseInteger(Arguments.text(0)));
        try {
            connect.timeout(700);
            byte[] message = Characters.encode("JAVA TCP en\n");
            connect.Output().write(message);
            InputStream inputValue = connect.inputValue();
            for (int number = 0; number < Characters.byteCount(message); number++) {
                Checks.require(inputValue.read() == (message[number] & 255), "TCP reply 불일치");
            }
        } finally { connect.close(); }
        DatagramChannel endpoint = DatagramChannel.open(0);
        try {
            endpoint.timeout(700);
            endpoint.send("10.0.2.2", Characters.parseInteger(Arguments.text(1)), "JAVA UDP en");
            Checks.require(Characters.equalText(endpoint.receive(), "JAVA UDP en"), "UDP reply 불일치");
        } finally { endpoint.close(); }
        Output.writeLine("JAVA 네트워크 verify: TCP UDP en");
    }
}
