// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** IPv4, ICMP, task, memory and RAM storage commands that read actual kernel state. */
public final class systemTool {
    static int addressValue;
    static boolean equalText(int index, String wordText) { return CommandInterpreter.equalText(index, wordText); }
    static int itemCount() { return CommandInterpreter.tokenCount; }
    static void failureValue(String README) { CommandInterpreter.result=2; TerminalIO.write(README); TerminalIO.Characters(10); }
    static void error(int value) { CommandInterpreter.error(value); }
    static void numberEntry(String name, int value) { TerminalIO.write(name); TerminalIO.number(value); TerminalIO.Characters(10); }
    static int digitValue(int index, int capacityLimit) {
        if (index>=itemCount() || CommandInterpreter.lengthValue[index]==0) return -1;
        int value=0;
        for (int ordinalIndex=0; ordinalIndex<CommandInterpreter.lengthValue[index]; ordinalIndex++) {
            int characterValue=CommandInterpreter.tokenValue[CommandInterpreter.startingPoint[index]+ordinalIndex]-'0';
            if (characterValue<0 || characterValue>9 || value>(capacityLimit-characterValue)/10) return -1;
            value=value*10+characterValue;
        }
        return value<=capacityLimit?value:-1;
    }
    static boolean readAddress(int index) {
        if (index>=itemCount()) return false;
        int value=0, chunkValue=0, digitCount=0, pointCount=0;
        for (int ordinalIndex=0; ordinalIndex<CommandInterpreter.lengthValue[index]; ordinalIndex++) {
            int characterValue=CommandInterpreter.tokenValue[CommandInterpreter.startingPoint[index]+ordinalIndex];
            if (characterValue=='.') { if (digitCount==0 || ++pointCount>3) return false; value=(value<<8)|chunkValue; chunkValue=digitCount=0; }
            else { if (characterValue<'0' || characterValue>'9' || ++digitCount>3) return false; chunkValue=chunkValue*10+characterValue-'0'; if(chunkValue>255)return false; }
        }
        if (pointCount!=3 || digitCount==0) return false;
        addressValue=(value<<8)|chunkValue; return true;
    }
    static void writeAddress(int value) {
        TerminalIO.number((value>>>24)&255); TerminalIO.Characters('.'); TerminalIO.number((value>>>16)&255); TerminalIO.Characters('.');
        TerminalIO.number((value>>>8)&255); TerminalIO.Characters('.'); TerminalIO.number(value&255);
    }
    static void showNetworkStatus() {
        TerminalIO.write(Board.networkStatus(20,0)!=0?"en0: ":"sl0: "); TerminalIO.write(Board.networkStatus(3,0)!=0?"UP":"DOWN");
        TerminalIO.write(Board.networkStatus(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        TerminalIO.write(Board.networkStatus(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); writeAddress(Board.networkStatus(0,0));
        TerminalIO.write(" netmask "); writeAddress(Board.networkStatus(1,0)); TerminalIO.write(" gateway "); writeAddress(Board.networkStatus(2,0)); TerminalIO.Characters(10);
        TerminalIO.write("  RX packets "); TerminalIO.number(Board.networkStatus(4,0)); TerminalIO.write(" bytes "); TerminalIO.number(Board.networkStatus(6,0));
        TerminalIO.write(" TX packets "); TerminalIO.number(Board.networkStatus(5,0)); TerminalIO.write(" bytes "); TerminalIO.number(Board.networkStatus(7,0)); TerminalIO.Characters(10);
        numberEntry("  dropped ",Board.networkStatus(8,0));
    }
    static void setAddress(int run) {
        if (itemCount()!=run+3 || !readAddress(run)) { failureValue("사용법: ipconfig set address 주소가림 gatewayValue"); return; }
        int address=addressValue;
        if(!readAddress(run+1)){failureValue("Invalid IPv4 netmask");return;} int maskValue=addressValue;
        if(!readAddress(run+2)){failureValue("Invalid IPv4 gateway");return;}
        int result=Board.networkSettings(0,address,maskValue,addressValue);
        if(result<0) { error(result); if(result==-16)TerminalIO.write("Close sockets and stop ftpd before changing address.\n"); }
        else { TerminalIO.write("IPv4 configuration applied (until reboot)\n"); showNetworkStatus(); }
    }
    static void networkCommand(boolean ipAddress) {
        if (itemCount()==1 || itemCount()==2 && (equalText(1,"show") || equalText(1,"addr") || equalText(1,"address") || equalText(1,"sl0") || equalText(1,"en0")) || itemCount()==3 && (equalText(1,"addr") || equalText(1,"address")) && equalText(2,"show")) { showNetworkStatus();return; }
        if (ipAddress && equalText(1,"route") && (itemCount()==2 || itemCount()==3&&equalText(2,"show"))) { showPath();return; }
        if (equalText(1,"set")) { setAddress(2);return; }
        if (itemCount()==2 && (equalText(1,"up") || equalText(1,"down"))) { Board.networkSettings(equalText(1,"up")?1:2,0,0,0);showNetworkStatus();return; }
        if (ipAddress && itemCount()==6 && equalText(1,"link") && equalText(2,"set") && equalText(3,"dev") && (equalText(4,"sl0")||equalText(4,"en0")) && (equalText(5,"up") || equalText(5,"down"))) { Board.networkSettings(equalText(5,"up")?1:2,0,0,0);showNetworkStatus();return; }
        failureValue("사용법: ip [addr show|route show|set address 주소가림 gatewayValue|link set dev sl0 up|down]");
    }
    static void showPath() {
        TerminalIO.write("Destination Netmask Gateway Interface\n");
        writeAddress(Board.networkStatus(0,0)&Board.networkStatus(1,0));TerminalIO.Characters(' ');writeAddress(Board.networkStatus(1,0));TerminalIO.write(Board.networkStatus(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (Board.networkStatus(2,0)!=0) {TerminalIO.write("0.0.0.0 0.0.0.0 ");writeAddress(Board.networkStatus(2,0));TerminalIO.write(Board.networkStatus(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void showNetwork() {
        TerminalIO.write("Proto Local Remote State Queued\n");
        for(int index=0;index<32;index++) {
            int typeCategory=Board.networkStatus(10,index);if(typeCategory==0)continue;
            TerminalIO.write(typeCategory==1?"TCP ":"UDP ");writeAddress(Board.networkStatus(16,index));TerminalIO.Characters(':');TerminalIO.number(Board.networkStatus(11,index));TerminalIO.Characters(' ');
            writeAddress(Board.networkStatus(12,index));TerminalIO.Characters(':');TerminalIO.number(Board.networkStatus(13,index));TerminalIO.Characters(' ');
            int stateValue=Board.networkStatus(14,index);TerminalIO.write(typeCategory==2?"DATAGRAM":stateValue==1?"LISTEN":stateValue==2?"ESTABLISHED":stateValue==3?"CLOSE_WAIT":stateValue==4?"ERROR":"UNCONNECTED");
            TerminalIO.Characters(' ');TerminalIO.number(Board.networkStatus(15,index));TerminalIO.Characters(10);
        }
        TerminalIO.write("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean waitState(int milliseconds) {
        int run=Board.milliseconds();
        while(Board.milliseconds()-run<milliseconds) {
            if(ShellIO.isInteractive()!=0){int characterValue=Board.readSerial();if(characterValue==3 || characterValue=='q' || characterValue=='Q' || characterValue==27 || characterValue==-4096)return false;}
            Board.yieldProcessor();
        }
        return true;
    }
    static void testResponse() {
        int repetitionCount=4, limitValue=1000, targetValue=-1;
        for(int positionIndex=1;positionIndex<itemCount();positionIndex++) {
            if(equalText(positionIndex,"-c")){repetitionCount=digitValue(++positionIndex,100);if(repetitionCount<1){failureValue("ping: -c 1..100");return;}}
            else if(equalText(positionIndex,"-W")){limitValue=digitValue(++positionIndex,10);if(limitValue<1){failureValue("ping: -W 1..10 seconds");return;}limitValue*=1000;}
            else if(targetValue<0)targetValue=positionIndex;else{failureValue("사용법: ping [-c repetitionCount] [-W secondsValue] IPv4");return;}
        }
        if(targetValue<0 || !readAddress(targetValue)){failureValue("ping: an IPv4 address is required (DNS is not configured)");return;}
        int address=addressValue, sentCount=0, receivedCount=0, accumulatedValue=0, minimumLimit=100000, maximumLimit=0;
        TerminalIO.write("PING ");writeAddress(address);TerminalIO.write(" 32 ICMP bytes\n");
        boolean continueProcessing=true;
        for(int orderValue=1;orderValue<=repetitionCount && continueProcessing;orderValue++) {
            int processedValue=Board.sendResponse(address,orderValue);
            if(processedValue<0){error(processedValue);break;}sentCount++;
            int run=Board.milliseconds();
            while(Board.readResponse(0)==-11 && Board.milliseconds()-run<limitValue)if(!waitState(1)){continueProcessing=false;break;}
            if(!continueProcessing)break;
            if(Board.readResponse(0)==0){
                int timeValue=Board.readResponse(1);receivedCount++;accumulatedValue+=timeValue;if(timeValue<minimumLimit)minimumLimit=timeValue;if(timeValue>maximumLimit)maximumLimit=timeValue;
                TerminalIO.write("32 bytes from ");writeAddress(address);TerminalIO.write(" seq=");TerminalIO.number(orderValue);TerminalIO.write(" ttl=");TerminalIO.number(Board.readResponse(2));TerminalIO.write(" time=");TerminalIO.number(timeValue);TerminalIO.write(" ms\n");
            }else{TerminalIO.write("Request timeout seq=");TerminalIO.number(orderValue);TerminalIO.Characters(10);}
            if(orderValue<repetitionCount)continueProcessing=waitState(200);
        }
        TerminalIO.number(sentCount);TerminalIO.write(" transmitted, ");TerminalIO.number(receivedCount);TerminalIO.write(" received, ");TerminalIO.number(sentCount==0?100:(sentCount-receivedCount)*100/sentCount);TerminalIO.write("% packet loss\n");
        if(receivedCount>0){TerminalIO.write("rtt min/avg/max = ");TerminalIO.number(minimumLimit);TerminalIO.Characters('/');TerminalIO.number(accumulatedValue/receivedCount);TerminalIO.Characters('/');TerminalIO.number(maximumLimit);TerminalIO.write(" ms\n");}
        CommandInterpreter.result=continueProcessing?(receivedCount==0?1:0):130;
    }
    static void showActivity() { TerminalIO.write("up ");TerminalIO.number(Board.milliseconds()/1000);TerminalIO.write(" seconds\n"); }
    static void showMemory() {
        numberEntry("ARM RAM KiB (firmware): ",Board.querySystem(0,0));
        numberEntry("Kernel image+BSS+stack KiB: ",Board.querySystem(1,0));
        int totalCapacity=Board.querySystem(2,0), usedCapacity=Board.querySystem(3,0);
        TerminalIO.write("AOT heap KiB total/used/free: ");TerminalIO.number(totalCapacity);TerminalIO.Characters('/');TerminalIO.number(usedCapacity);TerminalIO.Characters('/');TerminalIO.number(totalCapacity-usedCapacity);TerminalIO.Characters(10);
        numberEntry("Framebuffer KiB: ",Board.querySystem(4,0));
        numberEntry("EL0 arena+session reserve KiB: ",Board.querySystem(5,0));
        int mappedValue=0;for(int index=0;index<4;index++)mappedValue+=Board.querySystem(22,index);
        numberEntry("EL0 mapped KiB: ",mappedValue);
        TerminalIO.write("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void showTasks() {
        TerminalIO.write("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        TerminalIO.write("1 - RUN - - ");TerminalIO.number(Board.milliseconds());TerminalIO.write(" kernel/shell\n");
        for(int index=1;index<3;index++)if(Board.taskState(index)>0){TerminalIO.number(index+1);TerminalIO.write(" - READY 64 - - kernel-task\n");}
        for(int index=0;index<4;index++){
            int stateValue=Board.querySystem(20,index);if(stateValue==0)continue;
            TerminalIO.number(Board.querySystem(21,index));TerminalIO.Characters(' ');TerminalIO.number(index);TerminalIO.write(stateValue==1?" RUN ":" SUSPENDED ");
            TerminalIO.number(Board.querySystem(22,index));TerminalIO.Characters(' ');TerminalIO.number(Board.querySystem(24,index));TerminalIO.Characters(' ');TerminalIO.number(Board.querySystem(23,index));TerminalIO.Characters(' ');
            for(int positionIndex=0;positionIndex<288;positionIndex++){int byteValue=Board.querySystem(25,index+positionIndex*4);if(byteValue==0)break;Board.writeSerial(byteValue);}TerminalIO.Characters(10);
        }
    }
    static void showStorage() {
        int slotCount=0, dataCount=0;
        for(int index=0;index<MemoryFiles.fileCount;index++)if(MemoryFiles.namelen[index]>0 || MemoryFiles.referenceCount[index]>0){slotCount++;dataCount+=MemoryFiles.lengthValue[index];}
        TerminalIO.write("Filesystem Total Reserved Available Data Files Mount\nramfs ");TerminalIO.number(MemoryFiles.fileCount*16384);TerminalIO.Characters(' ');TerminalIO.number(slotCount*16384);TerminalIO.Characters(' ');TerminalIO.number((MemoryFiles.fileCount-slotCount)*16384);TerminalIO.Characters(' ');TerminalIO.number(dataCount);TerminalIO.Characters(' ');TerminalIO.number(slotCount);TerminalIO.Characters('/');TerminalIO.number(MemoryFiles.fileCount);TerminalIO.write(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void showStatus() {
        int repetitionCount=ShellIO.isInteractive()!=0?0:1;
        if(itemCount()>1){if(itemCount()!=3 || !equalText(1,"-n") || (repetitionCount=digitValue(2,1000))<1){failureValue("사용법: top [-n 1..1000]; q/Ctrl+C로 quitProgram");return;}}
        for(int sequenceValue=0;repetitionCount==0 || sequenceValue<repetitionCount;sequenceValue++){
            if(ShellIO.isInteractive()!=0 && repetitionCount==0)TerminalIO.write("\u001b[2J\u001b[H");
            showActivity();showMemory();showTasks();
            if(repetitionCount!=0 && sequenceValue+1>=repetitionCount)break;
            if(!waitState(1000))break;
        }
    }
    static String standardWord(int index) {
        if(index==0)return "ipconfig";if(index==1)return "ip";if(index==2)return "ping";if(index==3)return "route";if(index==4)return "netstat";
        if(index==5)return "ps";if(index==6)return "top";if(index==7)return "free";if(index==8)return "df";if(index==9)return "uptime";if(index==10)return "poweroff";return "help";
    }
    static void showHelp() {
        TerminalIO.write("--- Network / system commands ---\n");
        for(int index=0;index<12;index++){TerminalIO.write(standardWord(index));TerminalIO.write(" / ");TerminalIO.write(SystemCommands.wordText(index));TerminalIO.write(" : ");TerminalIO.write(SystemCommands.description(index));TerminalIO.Characters(10);}
        TerminalIO.write("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        TerminalIO.write("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        TerminalIO.write("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean executeCommand() {
        int command=-1;
        for(int index=0;index<12;index++)if(equalText(0,standardWord(index)) || equalText(0,SystemCommands.wordText(index)))command=index;
        if(equalText(0,"ifconfig"))command=0;if(equalText(0,"ss"))command=4;
        if(command<0)return false;
        if(command==11){if(equalText(1,"net") || equalText(1,"system"))showHelp();else if(equalText(1,"ko") || equalText(1,"input"))CommandInterpreter.hangulHelp();else CommandInterpreter.showHelp();return true;}
        if(command==0 || command==1)networkCommand(command==1);
        else if(command==2)testResponse();
        else if(command==6)showStatus();
        else if(itemCount()!=1){failureValue("This command takes no arguments; help system");}
        else if(command==3)showPath();else if(command==4)showNetwork();else if(command==5)showTasks();else if(command==7)showMemory();else if(command==8)showStorage();else if(command==9)showActivity();
        else if(command==10)Board.powerOff();
        return true;
    }
}
