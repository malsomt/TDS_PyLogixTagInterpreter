from struct import unpack_from


# Use this space to define UDTs in the controller you need to parse.
# Since UDT datatypes are sent as byte arrays from the controller, custom parsing into the base types is necessary.

# class matched UDT in TDS template
class GeneralMessage:
    # UDT defined as 180 bytes
    def __init__(self, byteArray):
        assert isinstance(byteArray, bytes) and len(byteArray)
        lu = LogixUnpack()
        try:
            self.Id = lu.unpack_DINT(byteArray[:3])
            self.Text = lu.unpack_STRING(byteArray[4:90])
            self.AltText = lu.unpack_STRING(byteArray[90:])

        except IndexError as e:
            raise f'General Message could not parse the passed array. Check the size of the array: {e}'

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'ID: {self.Id}\nText: {self.Text}\nAltText: {self.AltText}\n'


class GeneralMessageExt(GeneralMessage):
    def __init__(self, byteArray):
        super().__init__(byteArray)
        self.edits = False
        # Maintain
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
