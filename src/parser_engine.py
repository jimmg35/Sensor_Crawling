
# Author : @jimmg35
# Desc : black box class.


class ParserTool():
    """
        class hosts complex function for Parser 
    """

    @staticmethod
    def findUnionField_obj(union_arr, an_object):
        """ union all device meta field """
        for i in list(an_object.keys()):
            if i not in union_arr:
                union_arr.append(i)
    
    @staticmethod
    def findUnionField_att(union_arr, list_of_obj):
        """ union all device attribute field"""
        for i in list_of_obj:
            try:
                if i["key"] not in union_arr:
                    union_arr.append(i["key"])
            except:
                pass 

    @staticmethod
    def addTag2DubField(arr):
        unique = []
        for i in arr:
            if i not in unique:
                unique.append(i)

        for i in unique:
            count = 0
            for j in arr:
                if i == j:
                    count += 1
            if count != 1: # if field dub!
                arr[arr.index(i, arr.index(i)+1)] += "_DUB"

    @staticmethod
    def takeValueOfAtt(device_chunk, Adevice, union_colum):
        for i in union_colum:
            if i == "attributes":
                continue
            try:
                device_chunk[i] = Adevice[i]
            except:
                device_chunk[i] = None

    @staticmethod
    def takeValueOfAttChunk(device_chunk, Adevice, union_colum):
        for i in union_colum:
            value, status = ParserTool.checkFieldExistInAttribute(Adevice["attributes"], i)
            if status:
                device_chunk[i] = value
            else:
                device_chunk[i] = None

    @staticmethod
    def checkFieldExistInAttribute(att_chunk, att):
        flag = False
        att_index = 0
        for index, i in enumerate(att_chunk):
            try:
                if att == i["key"]:
                    flag = True
                    att_index = index
            except:
                break

        if flag:
            try:
                return att_chunk[att_index]["value"], flag
            except:
                return None, flag
        else:
            return None, False
    
    @staticmethod
    def replaceColumnName(sub, re):
        output = {}
        for i, j in zip(list(sub.keys()), list(re.keys())):
            output[j] = sub[i]
        return output