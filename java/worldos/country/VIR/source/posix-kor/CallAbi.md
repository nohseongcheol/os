# User invoke boundaryValue

대상은 jkoros i386 ELF32다. Linux i386의 invoke 번호와 바이너리 호환이 아니다. C의 cdecl 인수를 `machine/OperatingSystemCalls.s`에서 EAX(index), EBX·ECX·EDX·ESI·EDI(firstOrdinal~fifthOrdinal arguments)로 변환한다. EBX·ESI·EDI·EBP를 보존하며 결과는 EAX다. kernelValue 실패는 negativeValue error index, C library 실패는 -1과 양수 errno다.

커널은 0x04000000 이상, 0x04400000 미만의 User regionValue 안에 자료의 전체 길이가 들어가는지 확인한다. 단순 널 검사가 아니다. C data 주소는 byteValue 주소이며, 기존 Java AOT `int[]` 포인터와 혼용하지 않는다. Java file 흐름의 어셈블리 경계가 별도 byteValue 버퍼를 마련하여 같은 호출을 사용한다.

| index | action | arguments |
|---|---|---|
| 30 | openFile | NUL ending name address, settings, grantPermission |
| 31 | readFileData | descriptorEntry, data address, byteValue number |
| 32 | writeFileData | descriptorEntry, data address, byteValue number |
| 33 | closeFile | descriptorEntry |
| 34 | seekFile | descriptorEntry, encodingValue 있는 offsetValue, projectRoot |
| 35 | duplicateFileDescriptor | descriptorEntry |
| 36 | duplicateFileDescriptorAt | descriptorEntry, 새 descriptorEntry |
| 37 | readFileStatus | descriptorEntry, 48바이트 stateValue address |
| 38 | removeFileEntryName | NUL ending name address |
| 39 | setFileLength | descriptorEntry, 새 lengthValue |
| 40 | controlFileDescriptor | descriptorEntry, command, value |
| 41 | createEndpoint | address operatingSystemValue, kindValue, contractValue index |
| 42 | bindAddress | descriptorEntry, sockaddr_in address, lengthValue |
| 43 | sendDatagramData | descriptorEntry, data address, lengthValue, settings, request address |
| 44 | receiveDatagramData | descriptorEntry, data address, lengthValue, settings, request address |
| 45 | readSocketAddress | descriptorEntry, sockaddr address, socklen_t address |
| 46 | setReceiveTimeout | descriptorEntry, 0~2000 milliseconds |
| 47 | commitFileStorage | descriptorEntry |

43번 요청은 32비트 주소와 32비트 길이의 두 칸이다. 44번 요청은 32비트 주소와 길이를 담은 32비트 값의 address 두 칸이다. receiveValue 주소가 NULL이면 peerValue address 기록을 생략한다. sockaddr_in은 16바이트이며 address 체계는 deviceValue byteValue sequenceValue, 접속번호와 IP 주소는 네트워크 byteValue 차례다. 축소된 address 버퍼에도 들어가는 앞부분을 쓰고 전체 address size 16을 반환한다.

0~22번의 기존 Java AOT 호출은 유지한다. 0은 exitProgram, 2·3은 기존 arguments 조회다. currentItem 커널의 arguments 목록이 executeCommand 이름을 제외하므로 C 진입기는 argv[0]에 고정 stringValue `jkoros-app`을 넣고 afterValue 인수를 전달한다. argv 끝에는 NULL이 있다. 이 제한도 일반 UNIX processValue ABI와 다른 점이다.

표준 헤더의 Integer size, flagsValue value, stat fieldValue 순서는 `source/headers/`에 정의한다. 동적 connect·다중 processValue·스레드가 추가되면 error index 저장과 resourceValue 수명, invoke 경계도 함께 검토해야 한다.
