*** Settings ***
Documentation    This test suite verifies that NTP is operational on the device under test.
Library          rf_network.library.NetworkTransportLibrary


*** Keywords ***

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
