from struct import unpack_from
import pylogix


# Use this space to define UDTs in the controller you need to parse.
# Since UDT datatypes are sent as byte arrays from the controller, custom parsing into the base types is necessary.

# class matched UDT in TDS template
class GeneralMessage:
    # UDT defined as 180 bytes
    # GeneralMessage.Id : DINT
    # GeneralMessage.Text : STRING
    # GeneralMessage.AltText : STRING
    def __init__(self, byteArray):
        if byteArray is not None:
            assert isinstance(byteArray, bytes) and len(byteArray)
            lu = LogixUnpack()
            try:
                self.Id = lu.unpack_DINT(byteArray[:3])
                self.Text = lu.unpack_STRING(byteArray[4:90])
                self.AltText = lu.unpack_STRING(byteArray[90:])

            except IndexError as e:
                raise f'General Message could not parse the passed array. Check the size of the array: {e}'
        else:
            self.Id = 0
            self.Text = ''
            self.AltText = ''

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'ID: {self.Id}\nText: {self.Text}\nAltText: {self.AltText}\n'


class GeneralMessageExt(GeneralMessage):
    # GeneralMessage class extended to include edit flag and ._newXXX for use when editing table
    def __init__(self, byteArray=None):
        super().__init__(byteArray)
        self.edits = False
        # Constructor to Copy Base class values initially
        self._newId = self.Id
        self._newText = self.Text
        self._newAltText = self.AltText

    @property
    def newId(self):
        return self._newId

    @newId.setter
    def newId(self, val):
        assert isinstance(val, int)
        self._newId = val
        if self._newId == self.Id:
            self.edits = False
        else:
            self.edits = True

    @property
    def newText(self):
        return self._newText

    @newText.setter
    def newText(self, val):
        assert isinstance(val, str)
        assert len(val) <= 82  # Max message length is 82 characters
        self._newText = val
        if self._newText == self.Text:
            self.edits = False
        else:
            self.edits = True

    @property
    def newAltText(self):
        return self._newText

    @newAltText.setter
    def newAltText(self, val):
        assert isinstance(val, str)
        assert len(val) <= 82  # Max message length is 82 characters
        self._newAltText = val
        if self._newAltText == self.AltText:
            self.edits = False
        else:
            self.edits = True


class LogixUnpack:
    def __init__(self):
        pass

    def __enter__(self):
        return self

    @staticmethod
    def unpack_DINT(byteArray):
        # return DINT, no need to unpack tuple
        return unpack_from('<H', byteArray, 0)[0]

    def unpack_STRING(self, byteArray):
        length = self.unpack_DINT(byteArray[:4])
        return str(unpack_from(f'{length}s', byteArray, 4)[0], 'utf-8')


class PLCExt(pylogix.PLC):
    # Extend PLC class from pylogix to have basic flag to control threading access control on single instance
    # checking busy flag will fall on the calling thread to ensure busy is false before making the call.
    def __init__(self):
        super(PLCExt, self).__init__()
        self._busy = False

    def Read(self, tag, count=1, datatype=None):
        self._busy = True
        ret = super(PLCExt, self).Read(tag, count=count, datatype=datatype)
        self._busy = False
        return ret

    def Write(self, tag, value=None, datatype=None):
        self._busy = True
        ret = super(PLCExt, self).Write(tag, value=value, datatype=datatype)
        self._busy = False
        return ret

    @property
    def busy(self):
        return self._busy
