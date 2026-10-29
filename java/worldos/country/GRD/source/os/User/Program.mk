# 이름은 셸에서 사용하는 ASCII file name, Java classValue/함수는 한국어다.
APP_NAMES := hello udp netcheck stress javac java
APP_SOURCE_javac := User/Java/JavaTools.java User/Java/JavaCompiler.java User/Java/IdentifierRules.java
APP_ENTRY_javac := JavaCompiler.run
APP_SOURCE_java := User/Java/JavaTools.java User/Java/JavaMachine.java
APP_ENTRY_java := JavaMachine.run
APP_SOURCE_hello := User/examples/Greeting.java
APP_ENTRY_hello := Greeting.run
APP_SOURCE_udp := User/examples/DataCommunication.java
APP_ENTRY_udp := DataCommunication.run
APP_SOURCE_netcheck := User/examples/testNetworking.java
APP_ENTRY_netcheck := testNetworking.run
APP_SOURCE_stress := User/examples/networkLoop.java
APP_ENTRY_stress := networkLoop.run
