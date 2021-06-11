import datapack
import datapack.constants as mc

class MyPack(datapack.Datapack):
    """Description"""

    @datapack.tick
    def tick(self):
        self.command.say("hi")
        self.command.kill(datapack.entity(type="wolf"))
        self.command.teleport(datapack.entity(type=mc.BAT), datapack.player(name="JdavisBro"))
        execute = self.command.execute()
        execute.ex_as(datapack.entity(type=mc.BAT))
        execute.ex_run(self.command.function(self.imabat,ret=True))

    def imabat(self):
        self.command.say("@s")

    @datapack.load
    def load(self):
        self.command.say("Welcome to MyPack")

MyPack()
