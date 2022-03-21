*** Settings ***
Library         rf_network.library.NetworkTransportLibrary
Variables       testbed.yml
Resource        test_resources.robot
Suite Setup     Connect to DUT


*** Variables ***
${dut}        csr1
${USERNAME}   cisco
${PASSWORD}   cisco


*** Keywords ***
Connect to DUT
    Log to Console  connecting ${USERNAME}@${dut}
    ${device}    Set Variable    ${testbed['devices']['${dut}']}

    Connect To  ${device['host']}  ${USERNAME}  ${PASSWORD}  ${device['platform']}  alias=${device['host']}


*** Test Cases ***

Minimum Device Version Check
    [Tags]  Device Version
    Device should have version gt 17

Device type check
    [Tags]  Device OS
    Device should have os type IOS-XE
