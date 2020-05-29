from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from otp.ai.MagicWordGlobal import *
from otp.nametag.NametagConstants import *
from pandac.PandaModules import *

lastClickedNametag = None

class MagicWordManager(DistributedObject.DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('MagicWordManager')
    neverDisable = 1

    def generate(self):
        DistributedObject.DistributedObject.generate(self)
        self.accept('magicWord', self.handleMagicWord)

    def disable(self):
        self.ignore('magicWord')
        DistributedObject.DistributedObject.disable(self)

    def handleMagicWord(self, magicWord):
        if not self.cr.wantMagicWords:
            return

        if magicWord.startswith('~~'):
            if lastClickedNametag == None:
                target = base.localAvatar
            else:
                target = lastClickedNametag
            magicWord = magicWord[2:]
        if magicWord.startswith('~'):
            target = base.localAvatar
            magicWord = magicWord[1:]

        targetId = target.doId
        self.sendUpdate('sendMagicWord', [magicWord, targetId])
        if target == base.localAvatar:
            response = spellbook.process(base.localAvatar, target, magicWord)
            if response:
                self.sendMagicWordResponse(response)

    def sendMagicWordResponse(self, response):
        self.notify.info(response)
        if response.startswith("func:"):
            response = response[5:]
            args = response.split(",")
            print args
            if args[0] == "spawnModel":
                model = loader.loadModel(args[1])
                print args[1]
                print args[2]
                print args[3]
                print args[4]
                model.reparentTo(render)
                model.setPos(float(args[2]),float(args[3]),float(args[4]))
            return
        #base.localAvatar.setSystemMessage(0, 'Spellbook: ' + str(response))
