#!/usr/bin/python
# -*- coding=UTF-8 -*-

class sampleXml:
    def __init__(self,file):
        self.file = file
        self.xmlLst = self.readXml()
        self.xmlDict = self.xml2Dict(self.xmlLst)
    
    def readXml(self):
        try:
            fd = open(self.file)
            xmlLst = fd.readlines()
            fd.close()
            return xmlLst
        except Exception,e:
            print e
            return False

    def xml2Dict(self,xmlLst):
        xmlDict = {}
        xmlDict["attribute"] = {}
        xmlDict["data"] = []

        if xmlLst[0][0:5] == "<?xml":
            firLine = xmlLst[0].strip().split()
            for item in firLine:
                item = item.strip()
                if item.startswith("<"):
                    xmlDict["name"] = item.split()[0].replace('<','').replace('>','')
                elif '=' in item:
                    key,value = item.split('=')
                    xmlDict["attribute"][key]=value.replace('"','')
            xmlDict["data"].append(self.xml2Dict(xmlLst[1:]))
            return xmlDict

        firLine = xmlLst[0].strip().split()
        xmlDict["name"] = firLine[0].split()[0].replace('<','').replace('>','')
        for item in firLine[1:]:
            item = item.strip()
            if item.endswith('>'):
                item = item[:-1]
            if '=' in item:
                key,value = item.split('=')
                xmlDict["attribute"][key] = value.replace('"','')

        if len(xmlLst) == 1:
            return xmlDict

        nodeName = ""
        childNode = []
        for line in xmlLst[1:-1]:
            try:
                line = line.strip()
                if nodeName:
                    childNode.append(line)
                    if line == "</%s>" % nodeName:
                        xmlDict["data"].append(self.xml2Dict(childNode))
                        childNode = []
                        nodeName = ""

                elif line.endswith("/>"):
                    xmlDict["data"].append(self.xml2Dict([line]))
                else:
                    lineLst = line.split()
                    nodeName = lineLst[0].split()[0].replace('<','').replace('>','')
                    childNode.append(line)
            except Exception as e:
                print e
        return xmlDict
    
    def dict2XmlLst(self,dictionary):
        retStr = ""
        attrStr = " ".join(["%s=%s" % (key,value) for key,value in dictionary["attribute"].items()])
        if not dictionary["data"]:
            retStr = "<%s %s />" % (dictionary["name"],attrStr)
            return [retStr]

        headStr = "<%s>" % (dictionary["name"])
        endStr = "</%s>" % (dictionary["name"])
        splitStr ="\t"
        if attrStr:
            headStr = "<%s %s>" % (dictionary["name"],attrStr)
        if dictionary["name"] == "?xml":
            headStr = "<%s %s ?>" % (dictionary["name"],attrStr)
            endStr = ""
            splitStr=""

        retLst = []
        retLst.append(headStr)
        for secDict in dictionary["data"]:
            try:
                secLst = self.dict2XmlLst(secDict)
                retLst.extend([splitStr+word for word in secLst])
            except Exception as e:
                print e
        retLst.append(endStr)
        return retLst

    def write(self,fileName,xmlDict=""):
        if not xmlDict:
            xmlDict = self.xmlDict
        fd = open(fileName,'w')
        fd.write("\n".join(self.dict2XmlLst(xmlDict)))
        fd.close()

    def __del__(self):
        pass

