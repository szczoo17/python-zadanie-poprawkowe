import os
import os.path
import shutil
import struct
from skoczekvcs import utils


class Repository:

    def __init__(self, srcDir, destDir):
        self.srcDir = srcDir
        self.destDir = destDir
        self.changelogDir = os.path.join(self.destDir, ".changelog")
        self.deletedDir = os.path.join(self.destDir, ".deleted")


    # get latest revision number from a file
    def getRevision(self):
        with open(os.path.join(self.changelogDir, "rev.dat"), "rb") as file:
            revision = struct.unpack("<i", file.read())[0]
        return revision


    # update revision number
    def __setRevision(self, revision):
        with open(os.path.join(self.changelogDir, "rev.dat"), "wb") as file:
            file.write(struct.pack("<i", revision))


    # save first revision
    def __init(self):
        utils.copy(self.srcDir, self.destDir)
        if not os.path.exists(self.changelogDir):      
            os.mkdir(self.changelogDir)
        with open(os.path.join(self.changelogDir, "rev.dat"), "wb") as file:
            file.write(struct.pack("<i", 1))


    # new revision
    def commit(self):
        if not os.path.exists(self.changelogDir): 
            self.__init()
            return
        revision = self.getRevision()
        revision += 1
        self.__setRevision(revision)

        changes = os.path.join(self.changelogDir, "r{}.txt".format(revision))
        with open(changes, "w") as file:
            for dirName, subdirList, fileList in os.walk(self.srcDir):
                dirName2 = os.path.relpath(dirName, start=self.srcDir)
                dirName2 = os.path.join(self.destDir, dirName2)

                if not os.path.exists(dirName2):
                    # directory added
                    file.write("fb {}\n".format(dirName))
                else:
                    for f in fileList:
                        f1 =  os.path.join(dirName, f)
                        f2 =  os.path.join(dirName2, f)
                        if not os.path.exists(f2):
                            # file added
                            file.write("fa {}\n".format(f1))
                        else:
                            file.write("f {}\n".format(f1))
                            for line in utils.diff(f1, f2):
                                file.write(line)
                    # find deleted files
                    for f in os.listdir(dirName2):
                        f1 =  os.path.join(dirName, f)
                        f2 =  os.path.join(dirName2, f)
                        if not os.path.exists(f1) and f[0] != '.':
                            # file deleted - move it to .deleted
                            newPath = os.path.relpath(dirName2, self.destDir)
                            newPath = os.path.join(self.deletedDir, newPath)
                            if not os.path.exists(newPath):
                                os.makedirs(newPath)
                            shutil.move(f2, os.path.join(newPath, f))
                            file.write("fd {}\n".format(f1))

        utils.copy(self.srcDir, self.destDir)


    # restore a previous revision with a given number
    def restore(self, revisionNumber):
        latestNumber = self.getRevision()
        utils.copy(self.destDir, self.srcDir)
        # revert changes done since revisionNumber
        for currentNumber in range(latestNumber, revisionNumber, -1):
            # revert changes done in currentNumber
            changes = "r{}.txt".format(currentNumber)
            changes = os.path.join(self.changelogDir, changes)
            with open(changes, "r") as changefile:
                changelines = []
                dir = None
                for line in changefile:
                    if line[0] == 'f':
                        if changelines != []:
                            utils.apply(dir, changelines)
                            changelines = []
                        (prefix, dir) = line.split()
                        if prefix == 'fd':
                            # restore a deleted file
                            deleted = os.path.relpath(dir, self.srcDir)
                            deleted = os.path.join(self.deletedDir, deleted)
                            utils.copy(deleted, dir)
                        elif prefix == 'fa':
                            # delete an added file
                            os.remove(dir)
                        elif prefix == 'fb':
                            # delete an added directory
                            shutil.rmtree(dir)
                    else:
                        changelines.append(line)
                if changelines != []:
                    utils.apply(dir, changelines)
