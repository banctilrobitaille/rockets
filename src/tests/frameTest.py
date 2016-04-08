import unittest
from src.controller.Communication import FrameFactory

class TestFrame(unittest.TestCase):



    def testReceivedFrameCreation(self):
        from src.controller.Communication import FrameFactory
        from src.model.Frame import ReceivedFrame

        receivedFrame = FrameFactory.create(FrameFactory.FRAMETYPES['RECEIVED'], receivedData='testtesttesttesttesttest'
                                                                                              'testtesttesttesttesttest'
                                                                                              'testtesttesttesttesttest'
                                                                                              'testtesttesttesttesttest'
                                                                                              'test')

        self.assertIsInstance(receivedFrame, ReceivedFrame)


    def testSentFrameCreation(self):
        from src.controller.Communication import FrameFactory
        from src.model.Frame import SentFrame

        sentFrame = FrameFactory.create(FrameFactory.FRAMETYPES['SENT'], rocketID=0x20, command=0x01, payload=100.4)

        self.assertIsInstance(sentFrame,SentFrame)


    def testSentFrameCRC(self):
        from src.controller.Communication import FrameFactory

        expectedValue = 2183 #based on http://www.sunshine2k.de/coding/javascript/crc/crc_js.html poly 0xA001

        sentFrame = FrameFactory.create(FrameFactory.FRAMETYPES['SENT'], rocketID=0x20, command=0x01,
                                        timestamp=1459279066.356, payload=100.4)

        self.assertTrue(sentFrame.crc == expectedValue)



if __name__ == "__main__":

    unittest.main()