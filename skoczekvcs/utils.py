import os
import os.path
import shutil
from difflib import Differ

# copies srcDir to destDir recursively (replacing at destination)
def copy(srcDir, destDir):
    if not os.path.exists(destDir):
        os.mkdir(destDir)
    for f in os.listdir(srcDir):
        srcFile = os.path.join(srcDir, f)
        destFile = os.path.join(destDir, f)
        if os.path.isfile(srcFile):
            shutil.copyfile(srcFile, destFile)
        elif f[0] != '.': # ignore special directories
            copy(srcFile, destFile)


# returns a list of changes from file 1 to file 2
def diff(filename1, filename2):
    d = Differ()
    with open(filename1, "r") as file1:
        with open(filename2, "r") as file2:
            result = list(d.compare(file1.readlines(), file2.readlines()))
    result2 = []
    for line in result:
        if line[0] == ' ':
            result2.append("  \n")
        elif line[0] == '-':
            result2.append("- \n")
        elif line[0] == '+':
            result2.append(line.rstrip("\r\n") + "\n")
    return result2


# apply changes to a file
def apply(dir, changes):
    result = []
    index = 0
    with open(dir, "r") as file:
        for line in file:
            if changes[index][0] == ' ':
                # unchanged line
                result.append(line)
                index += 1
            elif changes[index][0] == '-':
                # deleted line
                index += 1
            else:
                while changes[index][0] == '+':
                    # added line
                    result.append(changes[index].partition(' ')[2])
                    index += 1
    with open(dir, "w") as file:
        for line in result:
            file.write(line)
