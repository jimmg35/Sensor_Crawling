
# Author : @jimmg35
# Desc : black box class.
from typing import List


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
    def takeValueOfAttChunk(device_chunk, Adevice, union_colum, check_column):
        for i in union_colum:
            value, status = ParserTool.checkFieldExistInAttribute(Adevice["attributes"], i)
            if status:
                device_chunk[i] = value
            else:
                if i not in check_column:
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

    @staticmethod
    def getShape(matrix):
        # return row, col of a matrix
        return [len(matrix), len(matrix[0])]

    @staticmethod
    def Transpose(A):
        # transpose a matrix
        shape_A = ParserTool.getShape(A)
        if shape_A[0] != 1:
            result = []
            for i in range(0, shape_A[1]):
                v  = []
                for j in range(0, shape_A[0]):
                    v.append(A[j][i])
                result.append(v)
            return result
        else: #if A is row matrix
            return [[A[i]] for i in range(0, len(A))]