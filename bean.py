class Game:
    def __init__(self,name="空",platefrom="空",language="中文",download="空",description="空"):
        self.name=name;
        self.platefrom=platefrom;
        self.language=language;
        self.download=download;
        self.description=description;
        self.name=name;
    def __str__(self):
        return "name:"+self.name+" platefrom:"+self.platefrom+" language:"+self.language+" download:"+self.download+" description:"+self.description   
