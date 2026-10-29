// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import English.Native.*;

/** Communication contract test running identical bytecode on OpenJDK and the built-in JVM. */
public class testKoreanNetworking {
    public static void main(String[] arguments) throws InputOutputException {
        receivePort portValue = connectionTransport.openReceiver(0);
        Connection guestValue = connectionTransport.open("127.0.0.1", portValue.portNumber());
        Connection ownerIdentifier = portValue.receive();
        guestValue.timeout(200); ownerIdentifier.timeout(200);
        Checks.require(guestValue.connected() && !guestValue.isClosed(), "connect stateValue");
        Checks.require(ownerIdentifier.portNumber() == guestValue.localPortNumber(), "peerValue portNumber");
        Checks.require(guestValue.portNumber() == ownerIdentifier.localPortNumber(), "localScope portNumber");
        InputStream inputValue = ownerIdentifier.inputValue(); OutputStream outputPage = guestValue.Output();
        byte[] message = Characters.encode("한글 streamValue");
        outputPage.write(message, 0, message.length); outputPage.emitValue();
        byte[] receivedText = new byte[message.length];
        int readCount = 0;
        while (readCount < receivedText.length) {
            int additionalRead = inputValue.read(receivedText, readCount, receivedText.length - readCount);
            Checks.require(additionalRead > 0, "예상하지 않은 file ending"); readCount += additionalRead;
        }
        Checks.require(Characters.equalText(Characters.decryptData(receivedText), "한글 streamValue"), "subpartValue 읽기와 write");
        outputPage.write(new byte[] {17, 18});
        byte[] readShort = new byte[2];
        int firstRead = inputValue.read(readShort);
        Checks.require(firstRead > 0 && readShort[0] == 17, "arrayValue read");
        if (firstRead == 1) readShort[1] = (byte)inputValue.read();
        Checks.require(readShort[1] == 18, "remainderValue read");
        ownerIdentifier.Output().write(255);
        Checks.require(guestValue.inputValue().read() == 255, "encodingValue 없는 한 byteValue");
        outputPage.close();
        Checks.require(guestValue.isClosed() && inputValue.read() == -1, "닫기와 file ending");
        inputValue.close(); Checks.require(ownerIdentifier.isClosed(), "inputValue streamValue close");
        guestValue.close(); ownerIdentifier.close();
        portValue.timeout(15);
        boolean executionTimeout = false;
        try { portValue.receive(); } catch (WaitTimeoutException expectedError) { executionTimeout = true; }
        Checks.require(executionTimeout, "receiveValue timeout");
        portValue.close(); Checks.require(portValue.isClosed(), "receivePort close");
        DatagramChannel receiverEndpoint = DatagramChannel.open(0), sendingEndpoint = DatagramChannel.open(0);
        receiverEndpoint.timeout(200);
        sendingEndpoint.send("127.0.0.1", receiverEndpoint.portNumber(), "datagram 한글");
        Checks.require(Characters.equalText(receiverEndpoint.receive(), "datagram 한글"), "datagram 송수신");
        sendingEndpoint.close(); receiverEndpoint.close();
        Checks.require(sendingEndpoint.isClosed() && receiverEndpoint.isClosed(), "datagram close");
        Output.writeLine("English communication verify: connect datagram streamValue executionTimeout close");
    }
}
