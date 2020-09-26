
class Printable:

    def __repr__(self):
        return self.__class__.__name__+"{"+str(self.name)+"}"

    def to_bytes(self):
        return self.name.encode('utf-8')
