from struct import unpack_from


# Use this space to define UDTs in the controller you need to parse.
# Since UDT datatypes are sent as byte arrays from the controller, custom parsing into the base types is necessary.

# class matched UDT in TDS template
class GeneralMessage:
    # UDT defined as 180 bytes
    def __int__(self, byteArray):
        assert isinstance(byteArray, bytes) and len(byteArray)
        with LogixUnpack as lu:
            try:
                self.Id = lu.unpack_DINT(byteArray[:3])
                self.Text = lu.unpack_STRING(byteArray[4:91])
                self.AltText = lu.unpack_STRING(byteArray[91:])

            except IndexError as e:
                raise f'General Message could not parse the passed array. Check the size of the array: {e}'


class LogixUnpack:
    @staticmethod
    def unpack_DINT(byteArray):
        return unpack_from('<H', byteArray, 0)[0]

    def unpack_STRING(self, byteArray):
        length = self.unpack_DINT(byteArray[:4])
        return str(unpack_from(f'{length[0]}s', byteArray, 4)[0], 'utf-8')
