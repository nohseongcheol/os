// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Belgium.JBelOS.networkStack;

import java.util.HashMap;
import java.util.Map;

/** Central dispatch for received Ethernet, ARP, IPv4, ICMP, UDP and TCP packets. */
public final class NetworkLayer {
    @FunctionalInterface
    public interface dataHandler {
        void processValueEntry(byte[] data, int run, int lengthValue);
    }

    private final Map<Integer, dataHandler> EthernetHandler = new HashMap<Integer, dataHandler>();
    private final Map<Integer, dataHandler> InternetProtocolHandler = new HashMap<Integer, dataHandler>();
    private final Map<Integer, dataHandler> userDataUnitHandler = new HashMap<Integer, dataHandler>();
    private final Map<Integer, dataHandler> TransmissionControlHandler = new HashMap<Integer, dataHandler>();

    public void registerEthernet(int kindValue, dataHandler Handler) {
        EthernetHandler.put(Integer.valueOf(kindValue & 0xffff), Handler);
    }

    public void registerInternetProtocol(int contractValue, dataHandler Handler) {
        InternetProtocolHandler.put(Integer.valueOf(contractValue & 0xff), Handler);
    }

    public void registerUserDataUnit(int hardwarePort, dataHandler Handler) {
        userDataUnitHandler.put(Integer.valueOf(hardwarePort & 0xffff), Handler);
    }

    public void registerTransmissionControl(int hardwarePort, dataHandler Handler) {
        TransmissionControlHandler.put(Integer.valueOf(hardwarePort & 0xffff), Handler);
    }

    public boolean receiveEthernet(byte[] frameIndex) {
        if (!NetworkTools.isEthernetFrame(frameIndex)) {
            return false;
        }
        int kindValue = NetworkTools.ethernetUpperProtocol(frameIndex);
        dataHandler DirectHandler = EthernetHandler.get(Integer.valueOf(kindValue));
        if (DirectHandler != null) {
            DirectHandler.processValueEntry(frameIndex, 14, frameIndex.length - 14);
            return true;
        }
        return kindValue == 0x0800 && receiveInternetPacket(frameIndex, 14);
    }

    private boolean receiveInternetPacket(byte[] data, int run) {
        if (!NetworkTools.isIpv4Protocol(data, run)) {
            return false;
        }
        int headerLength = (data[run] & 0x0f) * 4;
        int totalLength = NetworkTools.bigEndianShort(data, run + 2);
        if (totalLength < headerLength || run + totalLength > data.length) {
            return false;
        }
        int contractValue = data[run + 9] & 0xff;
        int contentStart = run + headerLength;
        int contentLength = totalLength - headerLength;
        dataHandler DirectHandler = InternetProtocolHandler.get(Integer.valueOf(contractValue));
        if (DirectHandler != null) {
            DirectHandler.processValueEntry(data, contentStart, contentLength);
            return true;
        }
        if (contentLength < 4) {
            return false;
        }
        int destinationPortNumber = NetworkTools.bigEndianShort(data, contentStart + 2);
        Map<Integer, dataHandler> portTable = contractValue == 17 ? userDataUnitHandler : contractValue == 6 ? TransmissionControlHandler : null;
        if (portTable == null) {
            return false;
        }
        dataHandler portHandler = portTable.get(Integer.valueOf(destinationPortNumber));
        if (portHandler == null) {
            return false;
        }
        portHandler.processValueEntry(data, contentStart, contentLength);
        return true;
    }
}

