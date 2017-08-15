from os import walk
import lxml.etree
import shutil

class SSIS:
    def __init__(self,projectpath):
        self.dirpath = projectpath
        self.files = []
        self.dtsxFiles = []
        for (dirpath, dirnames, filenames) in walk(projectpath):
            self.files.extend(filenames)
            break
        for file in self.files:
            if file.split(".")[-1] == "dtsx":
                self.dtsxFiles.append(dirpath+'\\'+file)
    def backup(self,fileToCopy):
        shutil.copy(fileToCopy,fileToCopy+'.backup')
    def renameVar(self,fromName,toName):
        for file in self.dtsxFiles:
            isNeedToChange = False
            tree = lxml.etree.parse(file)
            root = tree.getroot()
            for Variables in root.findall('{www.microsoft.com/SqlServer/Dts}Variables'):
                for Variable in Variables.findall('{www.microsoft.com/SqlServer/Dts}Variable'):
                    varName = Variable.attrib['{www.microsoft.com/SqlServer/Dts}ObjectName']
                    if varName == fromName:
                        isNeedToChange = True
                        Variable.attrib['{www.microsoft.com/SqlServer/Dts}ObjectName'] = toName
                        #tree.write(file)
            for Executables in root.findall('{www.microsoft.com/SqlServer/Dts}Executables'):
                for Executable in Executables.findall('{www.microsoft.com/SqlServer/Dts}Executable'):
                    if Executable.attrib['{www.microsoft.com/SqlServer/Dts}ExecutableType'] == 'Microsoft.Pipeline':
                        objectData = Executable.find('{www.microsoft.com/SqlServer/Dts}ObjectData')
                        for prop in objectData.iter('property'):
                            try:
                                if prop.attrib['name'] == "ReadOnlyVariables":
                                    prop.text = prop.text.replace(fromName,toName)
                            except AttributeError:
                                pass
                        for prop in objectData.iter('outputColumn'):
                            for attr, val in prop.attrib.items():
                                prop.attrib[attr] = val.replace(fromName,toName)
                        for prop in objectData.iter('inputColumn'):
                            for attr, val in prop.attrib.items():
                                if attr != 'externalMetadataColumnId':
                                    prop.attrib[attr] = val.replace(fromName, toName)
                        # for prop in objectData.iter('externalMetadataColumn'):
                        #     for attr, val in prop.attrib.items():
                        #         prop.attrib[attr] = val.replace(fromName, toName)
                        for arrEl in objectData.iter('arrayElement'):
                            arrEl.text = arrEl.text.replace(fromName, toName)
            if isNeedToChange:
                self.backup(file)
                tree.write(file)