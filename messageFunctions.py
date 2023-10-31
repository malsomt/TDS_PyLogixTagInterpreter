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
        # # print('Killed Fault Thread')
        # mbx = QMessageBox(QMessageBox.Information, 'Fault Message Error',
        #                   'Unable to find any "MessageArrayFault" in this component program.',
        #                   QMessageBox.Ok)
        # mbx.exec()
        return  # Exit Function
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
        # mbx = QMessageBox(QMessageBox.Information, 'Operator Message Error',
        #                   'Unable to find any "MessageArrayOperator" in this component program.',
        #                   QMessageBox.Ok)
        # mbx.exec()
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
    assert isinstance(plc, PLCExt)
    for index, fault in enumerate(tagList):
        assert isinstance(fault, GeneralMessageExt)
        print(f'Sending Program:{progName}.MessageArrayFault[{index}]')
        plc.Write(f'Program:{progName}.MessageArrayFault[{index}].Id', fault.newId)
        plc.Write(f'Program:{progName}.MessageArrayFault[{index}].Text', fault.newText)
        plc.Write(f'Program:{progName}.MessageArrayFault[{index}].AltText', fault.newAltText)


def send_messages(plc, tagList, progName):
    assert isinstance(plc, PLCExt)
    for index, msg in enumerate(tagList):
        assert isinstance(msg, GeneralMessageExt)
        print(f'Sending Program:{progName}.MessageArrayOperator[{index}]')
        plc.Write(f'Program:{progName}.MessageArrayOperator[{index}].Id', msg.newId)
        plc.Write(f'Program:{progName}.MessageArrayOperator[{index}].Text', msg.newText)
        plc.Write(f'Program:{progName}.MessageArrayOperator[{index}].AltText', msg.newAltText)
