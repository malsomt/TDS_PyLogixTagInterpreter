import pylogix
from pylogix import PLC

from definitions import parse_GeneralMessageArray, GeneralMessageExt, PLCExt


def loadFaults(plc, progName):
    """
    Function is called to load the fault message tags from a specific program in the PLC.
    Returns a list of parsed 'GeneralMessage' type.
    :param plc: PLC object from pylogix PLC class
    :param progName: String of program name to load fault messages from
    :return:
    """
    assert isinstance(plc, pylogix.PLC)
    arrayLength = 0
    fullTag_fault = f'Program:{progName}.MessageArrayFault'
    # Get the length of the arrays from the tag info in the plc object
    for index, tag in enumerate(plc.TagList):
        if tag.TagName == fullTag_fault:
            arrayLength = tag.Size
        if arrayLength != 0:
            break  # Kill Loop once found
    if arrayLength == 0:
        return None  # Exit Function
    retry = True  # flag used to loop in event of failed PLC read
    attempts = 2
    while retry:
        results_fault = plc.Read(f'Program:{progName}.MessageArrayFault[0]', arrayLength)
        if results_fault.Status == 'Success':
            retry = False  # kill while loop retries
            # attempt to parse out results
            if results_fault is not None:
                return parse_GeneralMessageArray(results_fault.Value, arrayLength)
        else:
            # Occasionally a PLC read will fail due to a connection lost error.
            # Simple re-run has solved the issue, this just does this automatically
            attempts -= 1  # remove attempt token

        if attempts <= 0:
            retry = False  # kill retry attempts


def loadMessages(plc, progName):
    """
        Function is called to load the operator message tags from a specific program in the PLC.
        Returns a list of parsed 'GeneralMessage' type.
        :param plc: PLC object from pylogix PLC class
        :param progName: String of program name to load operator messages from
        :return:
        """
    arrayLength = 0
    fullTag_msgs = f'Program:{progName}.MessageArrayOperator'
    for index, tag in enumerate(plc.TagList):
        if tag.TagName == fullTag_msgs:
            arrayLength = tag.Size
        if arrayLength != 0:
            break
    if arrayLength == 0:
        return None  # Kill thread
    retry = True  # flag used to loop in event of failed PLC read
    attempts = 2
    while retry:
        results_msgs = plc.Read(f'Program:{progName}.MessageArrayOperator[0]', arrayLength)
        if results_msgs.Status == 'Success':
            retry = False  # kill while loop retries
            # attempt to parse out results
            if results_msgs is not None:
                return parse_GeneralMessageArray(results_msgs.Value, arrayLength)
        else:
            # Occasionally a PLC read will fail due to a connection lost error.
            # Simple re-run has solved the issue, this just does this automatically
            attempts -= 1  # remove attempt token

        if attempts <= 0:
            retry = False  # kill retry attempts


def sortTagList(tagList):
    tempList = []
    for msg in tagList:
        assert isinstance(msg, GeneralMessageExt)
        # Check if Tag has any data
        if msg.newId != 0 or msg.newText != '' or msg.newAltText != '':
            tempList.append(msg)
    tempList.sort(key=lambda gm: gm.newId)  # sort list by newId property of the General Messages
    fillLen = len(tagList) - len(tempList)  # find how many tags are empty
    for _ in range(fillLen):  # fill in list with blank tags
        tempList.append(GeneralMessageExt())
    return tempList


def send_faults(plc, tagList, progName):
    """

    :param plc:
    :param tagList:
    :param progName:
    :return List of message strings that failed to write
    """
    assert isinstance(plc, PLCExt)
    failureList = []  # empty List
    for index, fault in enumerate(tagList):
        assert isinstance(fault, GeneralMessageExt)
        retry = True  # flag used to loop in event of failed PLC read
        attempts = 2
        while retry:
            print(f'Sending Program:{progName}.MessageArrayFault[{index}]')
            print(attempts)
            retId = plc.Write(f'Program:{progName}.MessageArrayFault[{index}].Id', fault.newId)
            retText = plc.Write(f'Program:{progName}.MessageArrayFault[{index}].Text', fault.newText)
            retAltText = plc.Write(f'Program:{progName}.MessageArrayFault[{index}].AltText', fault.newAltText)
            if writeFailed(retId) or writeFailed(retText) or writeFailed(retAltText):
                attempts -= 1  # decrement attempt count
                retry = False if attempts <= 0 else True
                if not retry:
                    failureList.append(f'Program:{progName}.MessageArrayFault[{index}])')
            else:
                retry = False  # Kill retry, successful write
    return failureList


def send_messages(plc, tagList, progName):
    """

    :param plc: pointer to pylogx.PLC object
    :param tagList: List of tags of type GeneralMessageExt to be sent
    :param progName: Program Name of the targeted tags
    :return:
    """
    assert isinstance(plc, PLCExt)
    failureList = []
    for index, msg in enumerate(tagList):
        assert isinstance(msg, GeneralMessageExt)
        retry = True  # flag used to loop in event of failed PLC read
        attempts = 2
        while retry:
            print(f'Sending Program:{progName}.MessageArrayOperator[{index}]')
            retId = plc.Write(f'Program:{progName}.MessageArrayOperator[{index}].Id', msg.newId)
            retText = plc.Write(f'Program:{progName}.MessageArrayOperator[{index}].Text', msg.newText)
            retAltText = plc.Write(f'Program:{progName}.MessageArrayOperator[{index}].AltText', msg.newAltText)
            if writeFailed(retId) or writeFailed(retText) or writeFailed(retAltText):
                attempts -= 1  # decrement attempt count
                retry = False if attempts <= 0 else True
                if not retry:
                    failureList.append(f'Program:{progName}.MessageArrayOperator[{index}])')
            else:
                retry = False  # Kill retry, successful write
    return failureList


def writeFailed(ret):
    assert isinstance(ret, pylogix.eip.Response)
    if ret.Status == 'Success':
        return False
    else:
        return True
