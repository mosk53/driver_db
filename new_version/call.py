from main import hubert



class Call(hubert):
    
    def __init__(self):
        print("Call is here")
        pass

    def furz(self):
        self.hdf5()


if __name__ == "__main__":
    c = Call()
    c.furz()