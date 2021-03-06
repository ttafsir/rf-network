# RF-Network

A pluggable multi-vendor network connection library for RobotFramework.


```robotframework
*** Settings ***
Library         rf_network.library.NetworkTransportLibrary
Variables       testbed.yml
Suite Setup     Connect to DUT


*** Variables ***

${dut}        csr1
${USERNAME}   cisco
${PASSWORD}   cisco


*** Test Cases ***

Minimum Device Version Check
    [Tags]  Device Version
    Device should have version gt 17

Device type check
    [Tags]  Device OS
    Device should have os type IOS-XE


*** Keywords ***

Connect to DUT
    Log to Console  connecting ${USERNAME}@${dut}
    ${device}    Set Variable    ${testbed['devices']['${dut}']}

    Connect To  ${device['host']}  ${USERNAME}  ${PASSWORD}  ${device['platform']}  alias=${device['host']}

Device should have version gt 17
    [Tags]  Version
    ${result}=  Send Command Parsed
                ...  command=show version
                ...  alias_or_index=1
                ...  connection_name=scrapli
                ...  parser=genie
    ${version}=  Set Variable  ${result}[0][version][version_short]
    Log To Console   ${version}
    Should be True  ${version} > 17

Device should have os type IOS-XE
    ${result}=  Send Command Parsed
                ...  command=show version
                ...  alias_or_index=1
                ...  connection_name=scrapli
                ...  parser=genie
    ${os}=  Set Variable  ${result}[0][version][os]
    Log To Console   ${os}
    Should Be Equal  ${os}  IOS-XE

```
