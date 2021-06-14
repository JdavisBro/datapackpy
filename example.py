import datapack
from datapack import selector

class MyPack(datapack.Datapack):
    """Description"""

    @datapack.tick
    def tick(self):
        self.command.kill(selector.entity(type="wolf"))
        self.command.teleport(selector.entity(type="bat"), selector.player(name="JdavisBro"))
        execute = self.command.execute()
        execute.ex_as(selector.entity(type="bat"))
        execute.ex_run(self.command.function(self.imabat,ret=True))

    def imabat(self):
        self.command.say("@s")

    @datapack.load
    def load(self):
        self.command.say("Welcome to MyPack")

MyPack()
